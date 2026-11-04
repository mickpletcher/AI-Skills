# Food Analyzer report restoration

## Change and evidence boundary

The canonical candidate now uses a compact FOOD ANALYSIS report: food/serving/confidence, nutrition, fitness reference fields, ingredient flags, NOVA classification, meal timing, blood sugar, interactions, portion notes and a concluding bottom line. A conditional alternatives section remains available. The layout is based on four owner-supplied screenshots, inspected visually; those private images and their historical product-specific claims are not included in the repository.

The layout restores presentation rather than treating an old assistant answer as verified food or medical evidence. FDA added-sugar distinctions and missing-input early return remain. The report explicitly avoids blanket diabetes clearance, generic medication clearance, invented GI values, oil/inflammation claims and automatic alternatives based only on NOVA 3. Calories use percent of energy reference, not FDA %DV. Protein reference arithmetic is distinguished from a verified label %DV.

Changes affect only the master and generated Claude/ChatGPT candidates. Shipped platform files, packages and historical acceptance are unchanged. Nothing is installed, promoted, published or activated by this change.

## Validation

The [synthetic scenarios](fixtures/food-report-layout.json) define observable format, arithmetic and safety criteria, not required exact wording. Existing nutrition arithmetic tests and migration/resource preservation tests remain applicable. Local structural and independent supplied-instruction review results are recorded below after execution. Native ChatGPT/Claude, automatic selection, actual nutrition-label image extraction and clinical accuracy are not certified by these tests.

### Local checks

- Generator regeneration and check: passed; compatibility refresh/check: 38 maps passed.
- Repository validation: 46 shipped skills, zero issues.
- Python suite: 270 tests, passed with seven environment-dependent skips. Focused migration/nutrition suite: 14 tests, passed with one skip.
- Offline evaluation harness self-test: 24 synthetic cases and 99 negative checks passed; these are not model evaluations.
- Five new scenario records parse and have distinct IDs, inputs and rubrics.
- Whitespace diff check passed. Shipped sources and archives remain unchanged.
- Generic skill-creator quick validator rejects the pre-existing `version` frontmatter field; the repository's own schema accepts it. The field is retained to preserve repository metadata.
- PowerShell is unavailable in this Linux workspace, so the three PowerShell validation/installer commands were not run here. Windows checks remain pending.

### Reference checks

Checked 2026-11-03: FDA's [Nutrition Facts guide](https://www.fda.gov/food/nutrition-facts-label/how-understand-and-use-nutrition-facts-label) distinguishes calorie guidance and nutrient %DV and explains when protein %DV is required. The University of Sydney [GI FAQ](https://glycemicindex.com/faqs/) defines low GI as 55 or below, closing the prior boundary gap; its [search instructions](https://glycemicindex.com/gi-search-instructions/) distinguish available carbohydrate per serving and glycemic load. No product-specific GI or interaction claims were validated or copied from the historical screenshots.

### Supplied-instruction behavior review

A separate assistant read the candidate and linked reference and produced four synthetic responses locally. Review found the full-label report in the intended order, correct sugar treatment and reference arithmetic, a one-sentence missing-photo request, correct doubled quantities with unknown added sugars preserved, and no blanket diabetes/medication clearance. Runtime presentation rules required plain text, so the monospace fence itself was not tested. A fifth explicit plain-text fallback artifact reused the first response; it is not an independent model sample.

Full synthetic responses and method notes remain in local validation artifacts outside Git. This is a bounded supplied-instruction review, not automatic routing, native Claude/ChatGPT integration, repeated-sample testing or new human acceptance. No real medication screening, visual label extraction or clinical claim validation was performed.

### Fixture correction, 2026-11-04

The `plain-text-host` scenario now includes the complete synthetic label transcription, so it can run in a fresh session without relying on another case's prompt. A regression test requires that input to contain the same complete label plus the plain-text rendering constraint. The test fails against the original cross-case reference and passes with the standalone input. This correction does not add a model response or change the earlier evidence limits.
