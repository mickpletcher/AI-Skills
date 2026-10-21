import copy
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / 'master-skills/resume-writer'
spec = importlib.util.spec_from_file_location('score_audit', SKILL / 'scripts/score_audit.py')
scorer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scorer)


def example():
    text = (SKILL / 'json-output-spec.md').read_text(encoding='utf-8')
    return json.loads(re.search(r'## Example JSON Object\s+```json\s+(.*?)```', text, re.S).group(1))


class ResumeScoringTests(unittest.TestCase):
    def test_published_example_reconciles(self):
        audit = example()
        self.assertEqual(scorer.calculate(audit), audit)
        self.assertEqual(audit['final_score'], 100)
        self.assertEqual(len(audit['principle_scores']), 7)

    def test_profile_weights_and_fixed_generic_mapping(self):
        audit = example()
        audit.pop('principle_scores')
        audit['scoring_evidence']['requirements'].append(dict(text='Python',supported=False,evidence='No supplied Python experience'))
        audit['scoring_evidence']['experience_statements'].append(dict(text='Maintained data checks.',names_specific_object=True,has_supplied_measure=False,evidence='Named checks; no metric'))
        self.assertEqual(scorer.calculate(audit)['final_score'],85)
        audit['review_context']='generic'
        result=scorer.calculate(audit)
        self.assertEqual(result['final_score'],87.5)
        self.assertEqual(result['principle_scores'][5]['source_name'],'common-patterns § Skills keyword dumps')

    def test_missing_timeline_and_qualitative_findings_add_no_penalties(self):
        audit=example()
        audit['missing_data_flags']=['MISSING_TIMELINE_CONTEXT']
        audit['notes']=['No later employment supplied','Red flags and chronology refer to the same missing context']
        result=scorer.calculate(audit)
        self.assertEqual(result['final_score'],100)
        self.assertEqual(result['major_issue_count'],0)
        audit['scoring_evidence']['chronology']={'state':'missing_dates','evidence':'Supplied role lacks start date'}
        result=scorer.calculate(audit)
        self.assertEqual(result['major_issue_count'],1)
        self.assertEqual(result['category_scores']['professionalism_and_trust'],100)

    def test_added_omitted_duplicated_or_remapped_criteria_rejected(self):
        for change in ('extra','missing','duplicate','category','source','weight'):
            with self.subTest(change=change):
                audit=example()
                entries=audit['principle_scores']
                if change=='extra':entries.append(copy.deepcopy(entries[-1]))
                elif change=='missing':entries.pop()
                elif change=='duplicate':entries[-1]=copy.deepcopy(entries[0])
                elif change=='category':entries[1]['category']='Professionalism and Trust'
                elif change=='weight':entries[-1]['weight']=True
                else:entries[-1]['source_name']='common-patterns § Action verb, object, outcome'
                with self.assertRaises(ValueError):scorer.calculate(audit)

    def test_invalid_or_cherry_picked_observation_inventories_rejected(self):
        for change in ('empty','duplicate','boolean','state','evidence','version','context'):
            with self.subTest(change=change):
                audit=example()
                data=audit['scoring_evidence']
                if change=='empty':data['requirements']=[]
                elif change=='duplicate':data['experience_statements']*=2
                elif change=='boolean':data['requirements'][0]['supported']=1
                elif change=='state':data['chronology']['state']='unexplained_gap'
                elif change=='evidence':data['privacy']['evidence']=''
                elif change=='version':audit['rubric_version']='old'
                else:audit['review_context']=[]
                with self.assertRaises(ValueError):scorer.calculate(audit)

    def test_historical_variable_ledgers_cannot_bypass_fixed_coverage(self):
        fixture=json.loads((ROOT/'evaluations/fixtures/native-human-numeric.json').read_text(encoding='utf-8'))
        for case in fixture['cases']:
            for audit in case['scoring_ledgers'].values():
                with self.assertRaisesRegex(ValueError,'rubric_version'):scorer.calculate(audit)
        audit=example()
        audit['principle_scores'].reverse()
        self.assertEqual(scorer.calculate(audit),example())

    def test_critical_and_low_confidence_caps_do_not_raise_verdict(self):
        audit=example();audit['confidence']='low'
        self.assertEqual(scorer.calculate(audit)['verdict'],'Strong')
        audit=example()
        audit['scoring_evidence']['privacy']={'state':'unsafe','evidence':'Sensitive personal identifier is present'}
        result=scorer.calculate(audit)
        self.assertEqual(result['final_score'],90)
        self.assertEqual(result['verdict'],'Strong')
        audit['scoring_evidence']['positioning']={'state':'absent','evidence':'No role direction'}
        audit['scoring_evidence']['structure']={'state':'unreadable','evidence':'No parseable sections'}
        audit['scoring_evidence']['chronology']={'state':'contradictory','evidence':'End precedes start'}
        self.assertEqual(scorer.calculate(audit)['verdict'],'High risk')

    def test_cli_derives_scores_and_rejects_tampered_final_ledgers(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'audit.json'
            command=[sys.executable,'-X','utf8',str(SKILL/'scripts/score_audit.py'),str(path)]
            audit=example();audit.pop('principle_scores')
            path.write_text(json.dumps(audit),encoding='utf-8')
            run=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',check=True)
            final=json.loads(run.stdout)
            path.write_text(json.dumps(final),encoding='utf-8')
            self.assertEqual(subprocess.run([*command,'--check'],capture_output=True).returncode,0)
            for mutation in ('score','severity','total','count'):
                bad=copy.deepcopy(final)
                if mutation=='score':bad['principle_scores'][0]['score']=2
                elif mutation=='severity':bad['principle_scores'][0]['severity']='MAJOR'
                elif mutation=='total':bad['final_score']=90
                else:bad['critical_issue_count']=False
                path.write_text(json.dumps(bad),encoding='utf-8')
                self.assertEqual(subprocess.run([*command,'--check'],capture_output=True).returncode,2)


if __name__=='__main__':
    unittest.main()
