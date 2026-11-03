"""Offline source and synthetic-contract regressions, not model or broker tests."""
import json
import re
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class NutritionBrokerContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.food = (ROOT / 'master-skills/food-analyzer/SKILL.md').read_text()
        cls.broker = (ROOT / 'master-skills/alpaca-trading/SKILL.md').read_text()
        cls.fixtures = json.loads((ROOT / 'evaluations/fixtures/nutrition-broker-corrections.json').read_text())

    def test_sugar_source_contract_and_export(self):
        for phrase in ('Total Sugars: no FDA Daily Value; report grams only',
                       'Added Sugars: 50g', 'total_sugars_g', 'added_sugars_g',
                       'Never assign an FDA %DV to total sugars or infer added sugars from total sugars',
                       'unknown, not zero', 'percent of custom target, not FDA %DV',
                       'legacy `sugar_g`', 'alias of `total_sugars_g`'):
            self.assertIn(phrase, self.food)
        self.assertNotIn('Total Sugars: 50g', self.food)

    def test_supplied_label_fixture_arithmetic(self):
        # Derive the reference denominator from the actual skill, not a duplicate constant.
        dv = Decimal(re.search(r'^- Added Sugars: (\d+)g$', self.food, re.M)[1])
        for case in self.fixtures['food_cases']:
            with self.subTest(case=case['id']):
                scale = Decimal(str(case['servings']))
                total = Decimal(str(case['total_sugars_g'])) * scale
                added = case['added_sugars_g']
                scaled_added = None if added is None else Decimal(str(added)) * scale
                percent = None if scaled_added is None else scaled_added / dv * 100
                self.assertEqual(total, Decimal(str(case['expected']['total_sugars_g'])))
                self.assertEqual(scaled_added, case['expected']['added_sugars_g'])
                self.assertEqual(percent, case['expected']['added_sugars_percent_dv'])
                self.assertIsNone(case['expected']['total_sugars_percent_dv'])

    def test_fractional_source_contract_and_authorization(self):
        for phrase in ('`market`, `limit`, `stop`, and `stop_limit`', '`time_in_force=day`',
                       'exactly one of `qty` or `notional`', 'both together are rejected',
                       'active, tradable and `fractionable=true`', 'Fractional short sales are unsupported',
                       'require `limit`, `day`, `extended_hours=true`',
                       'conflicting legacy market-only sentence', 'Verify every Alpaca capability',
                       'do not claim runtime support', 'prohibits replacing notional orders',
                       'do not assume atomic completion', 'confirmed cancellation/replacement',
                       'Paper-endpoint calls and trade round trips still change broker state and require explicit authorization',
                       'Never remove a live-trading confirmation guard', 'model output alone must not place an order'):
            self.assertIn(phrase, self.broker)
        self.assertNotIn('do not propose fractional limit logic', self.broker)
        self.assertNotIn('cancel and replace is the realistic pattern', self.broker)

    def test_supplied_fractional_contract_matrix(self):
        # A test-only contract oracle, NOT a trading implementation or broker acceptance claim.
        profile = self.broker.split('### Alpaca Capability Profile')[1].split('### Order Lifecycle')[0]
        types = set(re.findall(r'`(market|limit|stop|stop_limit)`', profile))
        tif = re.search(r'`time_in_force=(\w+)`', profile)[1]
        for case in self.fixtures['broker_cases']:
            with self.subTest(case=case['id']):
                supplied = case['contract']
                if not supplied['capability_evidence']:
                    result = 'unverified'
                elif (supplied['type'] not in types or supplied['tif'] != tif
                      or not all(supplied[k] for k in ('active', 'tradable', 'fractionable'))
                      or supplied['short'] or supplied['qty_present'] == supplied['notional_present']
                      or (supplied['extended'] and (supplied['type'] != 'limit' or not supplied['session_eligible']))):
                    result = 'reject'
                else:
                    result = 'supported_by_supplied_contract'
                self.assertEqual(result, case['expected'])
        self.assertEqual(self.fixtures['behavior_status'], 'not_run')
        self.assertEqual(self.fixtures['broker_status'], 'not_run')
