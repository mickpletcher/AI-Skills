---
name: food-analyzer
description: >
  Analyze food photos, nutrition labels, and ingredient lists. Trigger on food images,
  nutrition label scans, macro questions, glycemic questions, medication interaction checks,
  and similar food-analysis requests.
version: 1.0.0
---

# Food Analyzer

Analyze images of food, plated meals, nutrition labels, or ingredient lists and return a
structured nutritional breakdown with fitness, glycemic, processing, and interaction context.

## Trigger When

- The user starts with `fa` or `food`
- The user uploads an image of food, a meal, a label, or an ingredient list
- The user asks to analyze food, scan a label, estimate calories or macros, check blood sugar impact, or check medication compatibility

## Input Modes

Detect which mode applies from the visible input:

| Mode | What Claude Sees | Behavior |
| --- | --- | --- |
| Meal or Plate | Actual food, plated dish, restaurant item | Estimate calories and macros from visual portion heuristics |
| Nutrition Label | FDA-style Nutrition Facts panel | Extract exact values from the label |
| Ingredient List | Text ingredients | Flag allergens, additives, and processing red flags |
| Mixed | Label and product both visible | Prefer label data over visual estimates |

If no image is attached and the request depends on visual inspection, ask for a photo before proceeding.

## Output Sections

Include the sections that apply to the identified food:

- Nutrition Estimate
- Fitness Alignment
- Ingredient Flags
- NOVA Ultra-Processed Food Score
- Blood Sugar Impact
- Meal Timing Assessment
- Medication and Supplement Interactions
- Notes
- Healthier Alternatives when the food scores poorly

## Core Rules

- Use visible label data when available
- Estimate visually only when label data is not available
- State confidence clearly
- Use the FDA 2,000 kcal reference diet for percent daily values unless the user provides custom targets
- Keep medication and supplement warnings factual and end that section with a pharmacist and physician disclaimer
- Omit swap suggestions when the food scores well overall

## Output Expectations

The analysis should be structured, readable, and practical. It should cover:

- calories, protein, carbs, fat, fiber, sugar, and sodium
- percent daily values where applicable
- additive and allergen flags when ingredients are visible
- NOVA classification and the factors that drove it
- glycemic index or load estimates when relevant
- timing fit for pre-workout, post-workout, before bed, with medication, or general use
- clinically significant medication or supplement interactions
- quantified healthier swaps when needed

## Confidence Levels

- High: label clearly readable and values extracted directly
- Medium: recognizable dish and portion size reasonably visible
- Low: partial view, obscured label, layered dish, or unusual item

## Reference Standards

Use these as defaults unless the user provides custom targets:

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

Classify foods by processing level:

- NOVA 1: unprocessed or minimally processed
- NOVA 2: processed culinary ingredients
- NOVA 3: processed foods
- NOVA 4: ultra-processed foods

When ingredients are visible, scan for marker additives such as emulsifiers, artificial sweeteners, artificial colors, preservatives, industrial thickeners, flavor compounds, and modified starches. If uncertain between two NOVA groups, prefer the higher group and note the uncertainty.

## Glycemic Guidance

Use:

- Low GI: under 55
- Medium GI: 56 to 69
- High GI: 70 and above

Estimate glycemic load as `(GI x net carbs per serving) / 100` and consider modifiers such as fiber, fat, protein, vinegar, cooking method, particle size, ripeness, and food form.

## Validation Checklist

- [ ] Label data takes precedence over estimates when visible
- [ ] Percent daily values use the correct reference unless custom targets were provided
- [ ] NOVA classification includes rationale
- [ ] Blood sugar impact is explained, not just labeled
- [ ] Medication and supplement warnings stay factual and include a disclaimer
- [ ] Healthier swaps appear only when the food scores poorly
