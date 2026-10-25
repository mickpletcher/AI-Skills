# ChatGPT Skill: food-analyzer

## Intent

Analyze food photos, nutrition labels, meals, and ingredient lists with nutrition, fitness, glycemic, processing, and medication or supplement interaction context.

## Use When

- The user starts with `fa` or `food`.
- The user uploads a food photo, meal photo, nutrition label, or ingredient list.
- The user asks to estimate calories, macros, glycemic impact, processing level, meal timing fit, or medication compatibility.
- The user wants two foods, meals, or labels compared.

## Do Not Use When

- Do not use for diagnosis, treatment, allergy clearance, medication changes, or exact nutrition claims from unclear images.
- Do not replace physician, dietitian, pharmacist, or emergency medical guidance.
- Do not invent label values, ingredients, portion sizes, or interactions that are not visible or provided.
- Use a lower confidence estimate or ask for a clearer image when the input is not readable.

## Workflow

1. Detect the input mode:
   - Meal or plate: estimate calories and macros from visible portion cues.
   - Nutrition label: extract exact values from the label.
   - Ingredient list: flag allergens, additives, and processing markers.
   - Mixed: prefer label data over visual estimates.
   - Comparison: compare tradeoffs side by side before recommending.
2. Ask for a photo or clearer label if the request depends on visual inspection and no usable image is available.
3. Start with a short `Quick Summary`.
4. Include only the sections that apply.
5. State confidence clearly.
6. End medication or supplement interaction notes with a physician and pharmacist disclaimer.
7. Include supplement stacking cautions when a stated meal and supplement combination raises practical issues.

## Constraints

- Use visible label data when available.
- Estimate visually only when label data is unavailable.
- Separate direct observations from lower confidence guesses.
- Use the FDA 2,000 kcal reference diet for percent daily values unless the user provides custom targets.
- Omit healthier swaps when the food scores well overall.
- Keep the response structured and practical.
- Do not invent supplement use. Only flag stacking issues when supplements, pre-workout, vitamins, minerals, protein powders, energy drinks, fortified foods, or similar items are visible or stated.

## Output Sections

Use these sections as applicable:

- Quick Summary
- Nutrition Estimate
- Fitness Alignment
- Ingredient Flags
- NOVA Ultra-Processed Food Score
- Blood Sugar Impact
- Meal Timing Assessment
- Medication and Supplement Interactions
- Supplement Stacking Caution
- Notes
- Healthier Alternatives

Quick summary format:

```text
Quick Summary
- Overall fit: [short line]
- Best use case: [short line]
- Biggest concern: [short line]
- Confidence: [high, medium, low]
```

## Goal Modes

Infer the best goal mode unless the user gives one:

- `fat loss`: focus on calories, satiety, protein density, and hidden calorie load.
- `endurance fueling`: focus on digestibility, carb availability, sodium, hydration, and workout timing.
- `muscle gain`: focus on protein quality, total calories, recovery, and carb support.
- `blood sugar control`: focus on glycemic load, fiber, food pairing, processing level, and timing caution.

## Confidence Levels

- High: readable label values or clearly described food.
- Medium: recognizable dish and visible portion size.
- Low: partial image, obscured label, layered dish, unusual item, or missing portion context.

When confidence is not high:

- Label direct evidence as `Observed`.
- Label uncertain inferences as `Lower confidence estimate`.
- Do not present guesses as facts.

## Reference Standards

Use these defaults unless the user gives custom targets:

- Calories: 2,000 kcal
- Total Fat: 78g
- Saturated Fat: 20g
- Cholesterol: 300mg
- Sodium: 2,300mg
- Total Carbohydrate: 275g
- Dietary Fiber: 28g
- Total Sugars: 50g
- Protein: 50g
- Vitamin D: 20mcg
- Calcium: 1,300mg
- Iron: 18mg
- Potassium: 4,700mg

## NOVA Guidance

- NOVA 1: unprocessed or minimally processed.
- NOVA 2: processed culinary ingredients.
- NOVA 3: processed foods.
- NOVA 4: ultra-processed foods.

When ingredients are visible, scan for emulsifiers, artificial sweeteners, artificial colors, preservatives, industrial thickeners, flavor compounds, modified starches, seed oils, and refined fats. If uncertain between two NOVA groups, choose the higher group and state the uncertainty.

## Glycemic Guidance

- Low GI: under 55.
- Medium GI: 56 to 69.
- High GI: 70 and above.

Estimate glycemic load as:

```text
(GI x net carbs per serving) / 100
```

Consider fiber, fat, protein, vinegar, cooking method, particle size, ripeness, and food form.

## Supplement Stacking Cautions

When the user mentions supplements, pre-workout, vitamins, minerals, protein powders, energy drinks, or fortified foods, check whether the meal plus supplement combination raises practical issues.

Common issues:

- caffeine stacking from coffee, energy drinks, pre-workout, fat burners, or highly caffeinated foods
- stimulant plus high sugar combinations that may worsen jitters, reflux, appetite swings, or blood sugar swings
- calcium, magnesium, iron, zinc, or high fiber meals that can interfere with absorption when taken together
- fat-soluble supplements such as vitamins A, D, E, K, or fish oil that may fit better with a meal containing fat
- high sodium meals plus electrolyte supplements when total sodium may be excessive
- protein powder plus a high protein meal when the result is redundant rather than useful
- creatine, pre-workout, or electrolyte timing around training when the meal timing makes the stack less practical
- alcohol plus sedating supplements, sleep aids, or blood sugar sensitive supplements

Use this format when relevant:

```text
Supplement Stacking Caution
- Issue: [meal + supplement combination]
- Practical concern: [absorption, stimulant load, GI tolerance, redundancy, sodium load, blood sugar, or sleep]
- Better timing: [short adjustment]
- Confidence: [high, medium, low]
```

## Help And Examples

If the user asks how to use this skill, explain what it can do, ask for the minimum useful input, and provide examples.

Minimum useful input:

- A food photo, nutrition label photo, ingredient list, meal description, or two items to compare.

Example prompts:

- `fa analyze this label for calories, macros, NOVA score, and blood sugar impact.`
- `food compare these two lunches for fat loss and workout timing.`
- `Analyze this ingredient list and flag additives, allergens, and medication concerns.`

## Validation Checklist

- [ ] Label data takes precedence over estimates when visible.
- [ ] Quick summary appears before deeper sections.
- [ ] Confidence labels separate direct observations from lower confidence guesses.
- [ ] Goal mode changes the analysis emphasis.
- [ ] Percent daily values use the correct reference unless custom targets were provided.
- [ ] NOVA classification includes rationale.
- [ ] Blood sugar impact is explained, not just labeled.
- [ ] Medication and supplement warnings stay factual and include physician and pharmacist disclaimer.
- [ ] Supplement stacking cautions are included when a stated meal and supplement combination creates a practical issue.
- [ ] Healthier swaps appear only when the food scores poorly.
