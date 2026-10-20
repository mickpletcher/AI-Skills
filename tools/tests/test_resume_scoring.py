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
        result = scorer.calculate(audit)
        self.assertEqual(result, audit)
        self.assertEqual(result['final_score'], 68.4)
        self.assertEqual((result['critical_issue_count'], result['major_issue_count'], result['minor_issue_count']), (0, 1, 2))

    def test_targeted_and_generic_weights(self):
        audit = example()
        for entry in audit['principle_scores']:
            entry.update(score=3, severity='INFO')
        entry = copy.deepcopy(audit['principle_scores'][1])
        entry.update(principle='Numbers, everywhere, or you get an interview with nobody', source_name='Numbers, everywhere, or you get an interview with nobody', score=0)
        audit['principle_scores'].append(entry)
        result = scorer.calculate(audit)
        self.assertEqual(result['category_scores']['evidence_and_bullet_strength'], 50)
        self.assertEqual(result['final_score'], 85)
        audit['review_context'] = 'generic'
        self.assertEqual(scorer.calculate(audit)['final_score'], 82.5)

    def test_severity_and_confidence_caps_do_not_inflate_scores(self):
        for critical, confidence, expected in ((0,'high','Excellent'),(1,'high','Strong'),(2,'high','Good but inconsistent'),(3,'high','Weak'),(0,'low','Strong')):
            with self.subTest(critical=critical, confidence=confidence):
                audit = example()
                audit['confidence'] = confidence
                for index, entry in enumerate(audit['principle_scores']):
                    entry.update(score=3, severity='CRITICAL' if index < critical else 'INFO')
                result = scorer.calculate(audit)
                self.assertEqual(result['final_score'], 100)
                self.assertEqual(result['verdict'], expected)
                self.assertEqual(result['critical_issue_count'], critical)
        audit = example()
        for entry in audit['principle_scores']:
            entry.update(score=0, severity='CRITICAL')
        self.assertEqual(scorer.calculate(audit)['verdict'], 'High risk')

    def test_mapping_examples_cannot_be_cited_as_library(self):
        names=('The bullet formula is verb, work, outcome','Skills lists need proof, not just nouns','Simplicity signals judgment')
        for name in names:
            with self.subTest(name=name):
                audit=example()
                audit['principle_scores'][1].update(principle=name,source_name=name)
                with self.assertRaisesRegex(ValueError,'authoritative library'):
                    scorer.calculate(audit)

    def test_missing_pattern_and_wrong_library_mapping_rejected(self):
        for field,value in (('source_name','common-patterns § Fictional heading'),('weight',1.5)):
            audit=example(); audit['principle_scores'][-1][field]=value
            with self.assertRaises(ValueError):scorer.calculate(audit)
        for field,value in (('weight',1.0),('category','Professionalism and Trust')):
            audit=example();audit['principle_scores'][0][field]=value
            with self.assertRaisesRegex(ValueError,'Wrong category or weight'):scorer.calculate(audit)

    def test_duplicate_and_missing_category_rejected(self):
        audit=example();audit['principle_scores'].append(copy.deepcopy(audit['principle_scores'][0]))
        with self.assertRaisesRegex(ValueError,'once'):scorer.calculate(audit)
        audit=example();audit['principle_scores'].pop()
        with self.assertRaisesRegex(ValueError,'all five categories'):scorer.calculate(audit)

    def test_bad_numeric_and_structural_inputs_rejected(self):
        for field,value in (('score',True),('score',4),('score',1.5),('weight',float('nan')),('category',[]),('source_type',[])):
            with self.subTest(field=field,value=value):
                audit=example();audit['principle_scores'][0][field]=value
                with self.assertRaises(ValueError):scorer.calculate(audit)
        for audit in ([],{}, {'review_context':'targeted','principle_scores':[]}):
            with self.assertRaises(ValueError):scorer.calculate(audit)

    def test_cli_recomputes_then_checks_stale_and_valid_totals(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'audit.json'
            audit=example();audit.update(final_score=99,critical_issue_count=7)
            path.write_text(json.dumps(audit),encoding='utf-8')
            command=[sys.executable,str(SKILL/'scripts/score_audit.py'),str(path)]
            stale=subprocess.run([*command,'--check'],capture_output=True,text=True)
            self.assertEqual(stale.returncode,2)
            computed=subprocess.run(command,capture_output=True,text=True,check=True)
            fixed=json.loads(computed.stdout)
            self.assertEqual(fixed['final_score'],68.4)
            path.write_text(json.dumps(fixed),encoding='utf-8')
            self.assertEqual(subprocess.run([*command,'--check'],capture_output=True).returncode,0)
            fixed['critical_issue_count']=False
            path.write_text(json.dumps(fixed),encoding='utf-8')
            self.assertEqual(subprocess.run([*command,'--check'],capture_output=True).returncode,2)


if __name__ == '__main__':
    unittest.main()
