# Food analysis report layout

Use this layout for a complete single-food analysis. It restores the compact presentation of the supplied historical output, not its product-specific numbers or medical claims. The example placeholders are fields, not facts to copy.

Prefer one plain-text fenced report with emoji section labels and aligned `Label: value` lines, followed by a short prose bottom line outside the fence. Keep lines narrow and wrap longer explanations with a small continuation indent. Do not put Markdown bold markers inside the fence or use a wide table. If the host or user disallows fences, use plain labeled lines in this order. Emoji are optional where unsupported.

```text
🍽️ FOOD ANALYSIS
────────────────────────
[Food or product name]
Serving: [stated serving or estimated portion]
[✅/⚠️] [High/medium/low] confidence — [evidence and limits]

📊 NUTRITION (per [serving])
Calories:       [kcal]
Protein:        [g]
Carbs:          [g]
Fat:            [g]
Fiber:          [g]
Total Sugars:   [g; no FDA %DV]
Added Sugars:   [g or unknown; included in total sugars]
Sodium:         [mg]
Sat Fat:        [g if supplied]
Trans Fat:      [g if supplied]

⚡ FITNESS ALIGNMENT (FDA 2,000 kcal reference)
Calories:       [% of 2,000 kcal reference; not FDA %DV]
Protein:        [g; label %DV if supplied]
Total Fat:      [%DV (g of 78g)]
Sat Fat:        [%DV (g of 20g), if known]
Carbohydrates:  [%DV (g of 275g)]
Fiber:          [%DV (g of 28g)]
Added Sugars:   [%DV (g of 50g), or unknown]
Sodium:         [%DV (mg of 2,300mg)]
Assessment:     [practical goal fit and meal pairing]

🚩 INGREDIENT FLAGS
[✅ supported positives / ⚠️ evidenced concerns]

🏭 ULTRA-PROCESSED FOOD SCORE
NOVA Classification: [1–4, tentative range, or unknown]
Category:            [category or unknown]
Score Rationale:     [visible ingredient evidence and limits]
Additive Flags:      [identified markers or evidence limitation]

⏱️ MEAL TIMING ASSESSMENT
Timing Context: [stated context or explicitly inferred use]
Suitability:    [fit and qualifications]
Reasoning:      [brief practical explanation]
Suggestion:     [pairing or timing adjustment if useful]

🩸 BLOOD SUGAR IMPACT
Glycemic Index (GI):  [supported estimate/source or unknown]
Glycemic Load (GL):   [estimate/assumptions or not calculated]
Blood Sugar Response: [qualified expectation, not a guarantee]
Diabetes Considerations: [individual context and uncertainty]
Notes:               [serving, carbohydrate and fiber context]

💊 MEDICATION & SUPPLEMENT INTERACTIONS
[Specific supported concern for stated medication/supplement,
 or “Not assessed: medication/supplement list not supplied.”]
Consult your pharmacist or physician to confirm interactions
against your specific medication and supplement list.

📝 NOTES
[Serving-size traps, supported portion scaling and limitations]

🔄 HEALTHIER ALTERNATIVES
[Only when a meaningful concern warrants a swap or user asks]
```

Then finish with **Bottom line:** one or two sentences about overall fit, the main watch-out and the most useful action, tailored only to the stated goal or explicitly labeled inference. Do not repeat the whole report.

## Evidence and conditional fields

- Readable label values take precedence. Use approximate ranges for visual portions; do not manufacture sodium, sugar, ingredients or exact serving weights from appearance. Keep unknown fields brief rather than filling the report with guesses.
- Fitness reference math uses the skill's Reference Standards. Calories are a share of the reference energy intake, not a formal FDA %DV. Preserve a protein %DV printed on the label; if calculating grams against the 50g reference, label it “% of 50g reference,” not a verified label %DV. User targets remain separately labeled custom targets. Round sensibly and retain units and denominators.
- Keep total and added sugar separate. “All added” requires explicit supporting data. Never infer added sugars from the total or add the two together.
- Ingredient flags use the skill's grouping where it helps. Absence claims require a complete readable ingredient list and should be bounded to that list. Do not infer cross-contact clearance or brand certifications. An allergen warning is not a medical clearance.
- Do not label seed oils inherently inflammatory or portray coconut oil, honey or date paste as universally healthier. Any swap needs a supported, goal-specific benefit; quantify only with sufficient data. A NOVA 3 classification alone does not mandate alternatives, and a single ingredient swap does not establish a lower NOVA classification for a whole product. Distinguish DIY substitutions from available commercial alternatives.
- For missing ingredients, keep ingredient/NOVA sections short and say what cannot be assessed. Do not equate processing classification with an individual health outcome.
- Never output blanket “Diabetic Suitability: Safe,” guarantee no glucose spike, or imply diabetes treatment advice. Keep GI/GL unknown when evidence is insufficient instead of assigning attractive-looking numbers.
- Interaction screening requires specific medication/supplement context and reliable current sources. Do not invent a medication list, assert broad “no interactions,” or infer an interaction from a food's fat content alone. If sources are unavailable, mark the concern unverified and defer to a pharmacist/physician; never advise medication changes. Include the consultation line whenever this section is present.
- Notes may show two- or three-serving totals when useful, but do not claim a customary portion without evidence. Scaling changes amounts, not the GI of the food; discuss the changed carbohydrate load without promising a response.
- Omit alternatives when the food fits well and the user did not ask for swaps. Comparison/history tasks may use their own compact structure; a missing unusable image without sufficient text gets only the existing intake clarification, not this report.
