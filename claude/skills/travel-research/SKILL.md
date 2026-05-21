---
name: travel-research
description: Research and compare destinations with deeper scoring across budget, climate, logistics, activity fit, and seasonal tradeoffs before moving into full trip planning.
---

# Travel Research Skill

## Intent

Use this skill when the user is not ready for a full itinerary yet and needs stronger destination research first. The goal is to compare places honestly, surface tradeoffs early, and identify the best fit before handing off into `travel-planning` or `travel-itinerary`.

## Use When

- The user wants to compare destinations, regions, or trip styles
- A trip idea is still in the research phase and the right destination is not settled
- The user needs deeper analysis of climate, seasonality, training value, crowds, budget, or travel friction
- The best next step is to narrow choices before building a day by day plan

## Do Not Use When

- The destination is already chosen and the user needs a full itinerary
- The request is mainly about booking specific flights, hotels, or transport
- The user wants a finished travel budget and execution plan more than research
- The question is a quick one off logistics check that does not need structured comparison

## Research Priorities

Always judge options against Mick's actual travel preferences:

- solo travel by default
- private rooms only
- BNA as the home airport unless otherwise stated
- value optimized, not backpacker cheap and not luxury
- preference for active trips, endurance anchors, and good photo worthy experiences

Focus on what materially separates one option from another:

- total trip cost and daily spend
- weather and season fit
- event or activity alignment
- transit complexity
- crowd pressure
- safety and scam friction
- visa or border hassle
- how well the destination fits the stated trip goal

## Workflow

1. Identify the trip goal first.
2. Determine the comparison set:
   - user supplied destinations
   - a region shortlist
   - best fit suggestions if the user only gives goals and constraints
3. Build a direct scorecard for each option.
4. Explain the tradeoffs in plain language, not tourism fluff.
5. Call out strong and weak fit areas:
   - budget fit
   - climate fit
   - activity fit
   - logistics fit
   - pace fit
   - value for the stated season
6. Recommend the best option and at least one fallback.
7. State the next practical move:
   - deeper research
   - move into `travel-planning`
   - move into `travel-itinerary`

## Comparison Framework

For each destination, check:

- best travel window for the stated goal
- worst travel window and why
- likely flight friction from BNA
- local transport simplicity
- private room lodging value
- food cost and quality
- training or adventure opportunities
- scenic or content capture value
- overtourism pressure
- common traveler mistakes

When relevant, also compare:

- event calendars
- altitude or terrain
- rental car need
- ferry or rail usefulness
- remote work practicality
- carry only practicality

## Output Format

Use this structure for substantial comparison requests:

```text
TRIP GOAL:
[What the user is trying to optimize for]

OPTIONS:
- [Destination A]
- [Destination B]

SCORECARD:
| Destination | Budget | Climate | Activity | Logistics | Value | Overall |
|---|---:|---:|---:|---:|---:|---:|

DESTINATION NOTES:
[Destination A]
- Best for:
- Watch for:
- Best season:
- Poor season:
- Estimated daily spend:

[Destination B]
- Best for:
- Watch for:
- Best season:
- Poor season:
- Estimated daily spend:

RECOMMENDATION:
[Best choice and why]

RUNNER UP:
[Fallback and why]

NEXT STEP:
[Move into travel-planning or request deeper research on one option]
```

## Constraints

- Do not give generic top ten destination lists
- Make comparisons explicit and decision oriented
- Prefer practical travel friction over postcard descriptions
- If the user gives weak input, propose a short relevant comparison set instead of pretending certainty
- Hand off to `travel-planning` once a destination is chosen

## References

- `shared/skill-standard.md`
- `claude/skills/travel-planning/SKILL.md`
- `claude/skills/travel-itinerary/SKILL.md`

## Help And Examples

Use this skill when the user needs to decide where to go before planning the trip in detail.

Minimum useful input:

- a destination shortlist or a trip goal
- rough date window
- budget or style constraints if known

Example prompts:

```text
Use travel-research to compare Madeira, Girona, and Mallorca for a spring cycling trip from BNA.
```

```text
Research the best October solo trip options for hiking, good weather, and strong USD value.
```

```text
Compare Japan and Portugal for a two week active trip with good food, easy logistics, and private room lodging.
```

## Validation Checklist

- The comparison focuses on real tradeoffs instead of generic destination blurbs
- The output reflects Mick's travel constraints and preferences
- The recommendation is clear and justified
- The next step points to planning or itinerary work, not more vague brainstorming
