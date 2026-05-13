# IdeaForge Scoring Model

Defines the metrics, weights, scales, scoring formula, and verdict bands used in Stage 4 of the pipeline.

---

## Metrics

### Technical Feasibility
Can this be built with technology that exists today?

| Score | Meaning |
| --- | --- |
| 9-10 | Fully buildable with off-the-shelf tools. No novel engineering required. |
| 7-8 | Buildable with moderate effort. A few hard problems but clear solutions exist. |
| 5-6 | Requires significant custom development. Key dependencies exist but are not mature. |
| 3-4 | Technically possible but requires research-level effort or rare expertise. |
| 1-2 | Depends on technology that does not exist yet or is in early experimental state. |
| 0 | Not buildable with current technology. |

**Weight: 20%**

---

### Commercial Potential
Is there a realistic customer and a path to revenue?

| Score | Meaning |
| --- | --- |
| 9-10 | Clear buyer, large addressable market, strong willingness to pay. |
| 7-8 | Identifiable buyer, reasonable market size, plausible pricing model. |
| 5-6 | Possible buyers but market is niche or pricing model is unclear. |
| 3-4 | Hard to identify who pays or why. Likely a nice-to-have. |
| 1-2 | No clear buyer. Value is diffuse or captured entirely by free alternatives. |
| 0 | No commercial application. |

**Weight: 25%**

---

### Automation Potential
How much of this runs unattended after initial setup?

| Score | Meaning |
| --- | --- |
| 9-10 | Fully autonomous once deployed. Minimal ongoing human input. |
| 7-8 | Mostly automated with occasional human review or correction. |
| 5-6 | Partially automated. Meaningful manual steps remain. |
| 3-4 | Low automation. Human judgment required for most operations. |
| 1-2 | Primarily manual. Automation is marginal or cosmetic. |
| 0 | Not automatable. |

**Weight: 15%**

---

### Implementation Simplicity
How quickly can one person reach a working prototype?

| Score | Meaning |
| --- | --- |
| 9-10 | MVP in under 2 weeks solo. Minimal dependencies. |
| 7-8 | MVP in under 30 days solo with focused effort. |
| 5-6 | MVP takes 1-3 months. May need one additional skill set. |
| 3-4 | MVP takes a small team or 3-6 months solo. |
| 1-2 | Complex build requiring significant team or timeline. |
| 0 | Not implementable by an individual or small team. |

Note: Higher score = simpler to implement. This metric is not inverted in the formula.

**Weight: 15%**

---

### Market Openness
How much room exists to compete or establish a position?

| Score | Meaning |
| --- | --- |
| 9-10 | Unsolved problem. No direct competitors. Clear gap in the market. |
| 7-8 | A few solutions exist but none dominant. Meaningful differentiation is possible. |
| 5-6 | Competitive space. Strong incumbents but room for niche positioning. |
| 3-4 | Crowded. Well-funded leaders hold most of the market. |
| 1-2 | Saturated. Dominated by free or low-cost solutions. |
| 0 | Commoditized. No viable position available. |

**Weight: 10%**

---

### Patent Potential
Does this contain a novel mechanism or process that could be protected?

| Score | Meaning |
| --- | --- |
| 9-10 | Strong novel claim. Clear mechanism not previously described or filed. |
| 7-8 | Likely patentable angle. Some prior art exists but differentiation is defensible. |
| 5-6 | Possible patent with narrow claims. Heavy prior art in related areas. |
| 3-4 | Weak patent potential. Likely prior art or obvious combination of known methods. |
| 1-2 | No clear patent angle. Well-understood methods or combinations. |
| 0 | No patent potential. |

**Weight: 10%**

---

### Speed to MVP
How fast can this demonstrate real value to a real user?

| Score | Meaning |
| --- | --- |
| 9-10 | Demonstrable value in hours or days. Minimal setup required. |
| 7-8 | First usable version in under 2 weeks. |
| 5-6 | First usable version in 1-2 months. |
| 3-4 | First usable version takes 3-6 months. |
| 1-2 | MVP timeline measured in quarters. |
| 0 | No clear MVP path. |

**Weight: 5%**

---

## Formula

```
IdeaForge Score =
  (Technical Feasibility × 0.20) +
  (Commercial Potential × 0.25) +
  (Automation Potential × 0.15) +
  (Implementation Simplicity × 0.15) +
  (Market Openness × 0.10) +
  (Patent Potential × 0.10) +
  (Speed to MVP × 0.05)

Multiply result by 10 to express as a 0-100 score.
```

---

## Verdict Bands

| Score | Verdict | Meaning |
| --- | --- | --- |
| 85-100 | **High Priority** | Pursue immediately. Strong across most dimensions. |
| 70-84 | **Strong** | Worth serious development planning. One or two weak dimensions to address. |
| 55-69 | **Promising** | Real potential but needs refinement, better timing, or a clearer commercial path. |
| 40-54 | **Speculative** | Park and revisit. Conditions may improve or the framing may need a rethink. |
| Below 40 | **Low Priority** | Fundamental weakness in one or more critical dimensions. Do not invest significantly without a clear change in circumstances. |

---

## Missing Input Handling

If a key signal is missing — no market information, no technical detail, no sense of the target user — do the following:

- Score the affected metric conservatively (assume mid-to-low range).
- Flag the missing input explicitly in the output under a **Missing Signals** section.
- Do not fabricate data to complete the score.

Example flag:

```
Missing Signal: No target customer identified. Commercial Potential scored conservatively at 4/10.
Provide more context about who buys this to improve the score accuracy.
```

---

## Conservative Scoring Rules

- When uncertain between two adjacent scores, choose the lower one.
- Do not inflate scores based on enthusiasm in the user's input.
- Polished framing does not raise a score. Substance does.
- A technically excellent idea with no commercial path should score low on Commercial Potential regardless of how novel it is.
