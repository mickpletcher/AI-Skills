---
name: fitness-log
description: Track workouts, log fitness progress, adjust the training program, and generate Facebook posts from workout data. Trigger on workout logging, PR updates, program questions, and fitness progress summaries.
version: 1.1.0
---

# Fitness Log

Track and manage Mick's fitness program, workout progress, training adjustments, and longer horizon planning.

## Trigger When

- The user starts with `fit` or `workout`
- The user wants to log a session
- The user reports a PR or milestone
- The user asks about progress or wants a comparison against baseline
- The user wants a Facebook post written from workout data
- The user wants a weekly review or trend summary
- The user wants the training checked against a goal such as pull ups, cycling, or triathlon
- The user wants export friendly workout summary data

## Athlete Profile

- Age: 51
- Bodyweight: 199 lbs
- Body fat: 18.7%
- Goal: maximum muscle growth while cutting toward 15% body fat
- Training location: YMCA Springfield TN plus home gym
- Home equipment: trap bar, pull-up bar, dumbbells, bench
- TRT: 737 ng/dL, managed by a urologist

## Program Structure

- Sunday: Upper A, chest, back, shoulders
- Monday: Lower A, quads, hamstrings, calves
- Tuesday: Upper B, arms, back, delts
- Wednesday: Lower B, glutes, hamstrings, posterior chain
- Thursday through Saturday: rest

Sessions are typically about 2 hours. The program is machine-based with some free weights.

## Current PRs

- Leg Press: 790 lbs
- Calf Raise: 1,108 lbs
- Chest Press: 180 lbs
- Lateral Pulldown: 180 lbs
- Seated Row: 180 lbs
- Ab Crunch: 195 lbs
- Back Extension: 220 lbs
- Torso Oblique: 207.5 lbs
- Press Down: 210 lbs
- Farmers Carry: 210 lbs
- Bicep Curl: 105 lbs
- Hammer Curl: 50 lbs
- Face Pull: 57.5 lbs
- Lateral Raise: 30 lbs
- Pull-Ups: 8 reps

## Starting Baseline

- Leg Press: 465 lbs
- Chest Press: 165 lbs
- Pull-Ups: 0 reps
- Seated Row: 160 lbs
- Lateral Pulldown: 160 lbs

## Primary Workflows

### Log A Workout

- Record exercises, sets, reps, and weights
- Normalize similar exercise names into one canonical movement when summarizing progress
- Acknowledge PRs
- Note regressions or anything unusual
- Flag potential issues such as skipped groups or excessive volume near an injury site

Use a compact summary like:

```text
Date | Day X | Focus
Exercise: weight x sets x reps
Exercise: weight x sets x reps
PRs hit: [list]
Notes: [anything worth flagging]
```

### Generate A Facebook Post

When writing from workout data:

- use first-person, direct language
- lead with the specific number or milestone
- avoid emojis
- avoid em dashes in final Facebook post output
- keep hashtags relevant and limited

Good example:

```text
Hit 790 on leg press today. Started this program three months ago at 465. The numbers do not lie.
```

Bad example:

```text
Absolutely crushed leg day today! So proud of my progress on this fitness journey!
```

Relevant hashtags can include:
`#StrengthTraining` `#MuscleBuilding` `#FitnessJourney` `#Triathlon` `#Cycling` `#ActiveLifestyle`

### Adjust The Program

- Suggest changes within the current safety constraints
- Prefer machine alternatives when free weights add unnecessary risk
- Do not recommend barbell lunges

### Summarize Progress

- Compare current numbers against baseline
- Calculate percentage improvements where useful
- Highlight standout gains
- Note body composition trends carefully and accurately

### Trend Summary

When the user wants a progress summary across multiple logged workouts:

- summarize strength trends across major lifts, carries, and pull ups
- summarize endurance trends across cycling, triathlon, conditioning, or longer sessions when present
- summarize consistency by training frequency, missed sessions, and pattern adherence
- summarize recovery by session density, soreness notes, low energy notes, or performance drop offs when provided

Use plain language and keep the summary tied to the actual log evidence.

### Program Check

When the user asks whether recent training matches the goal:

- compare the recent training mix against the stated goal
- call out alignment gaps such as too little pulling work for pull up goals, not enough endurance work for cycling, or missing swim bike run balance for triathlon
- suggest the smallest practical adjustments first
- respect the current safety rules and equipment reality

### Weekly Review

When the user asks for a weekly review:

- list the wins
- list missed sessions or weak spots only when they are real
- state the next block focus in concrete terms
- keep it useful enough to guide the next week without turning it into fluff

Use this structure:

```text
Weekly Review
Wins: [short summary]
Missed or limited: [short summary]
Next block focus: [short summary]
```

### Nutrition And Timing Prompts

When the user asks for nutrition or recovery guidance tied to training:

- account for workout type, duration, and intensity
- distinguish between strength work, longer endurance work, and mixed training days
- keep suggestions practical and brief
- focus on timing, protein, carbs, hydration, and recovery need rather than abstract meal philosophy

### Exercise Normalization

When summarizing progress, group similar movement names under a cleaner canonical label so trend reviews do not fragment.

Examples:

- `pull ups`, `pullups`, and `chin over bar pull ups` should be grouped intentionally if they mean the same tracked movement
- `lat pulldown` and `lateral pulldown` should be grouped when they refer to the same machine pattern
- `farmers carry` and `farmer carry` should be treated as the same movement

Do not merge exercises that change the training meaning in a material way.

### Long Horizon Planning

When the user asks for a longer progression plan:

- support race prep, strength cycles, and hybrid training seasons
- break the plan into practical blocks
- account for the current schedule, equipment, and safety limits
- keep the horizon realistic rather than pretending every goal should progress at once

### Structured Export

When the user wants export friendly data for dashboards or Obsidian:

- provide a compact structured block after the narrative summary
- include canonical exercise names, key metrics, trend direction, and the current focus
- keep the structure easy to reuse in JSON like or note friendly formats

Use a structure like:

```text
structured_data:
  period: [week or range]
  focus: [goal]
  strength_trends:
    - movement: [canonical name]
      trend: [up, flat, down]
  consistency:
    completed_sessions: [count]
    planned_sessions: [count]
  next_focus: [short line]
```

## Safety Rules

- Zero axial loading on the spine
- No barbell squats, barbell lunges, or overhead barbell press
- Flag calf volume above 5 sets for Achilles protection
- Note shoulder pain when mentioned and suggest safer substitutions
- Never recommend anything that contradicts back safety
- Be careful about endurance volume guidance if recovery signals are poor

## Notable Achievements

- Pull-ups improved from 0 to 8 reps in 3 months
- Leg press improved about 75% from baseline
- Gained 6 lbs lean muscle mass
- Body fat is trending down toward the 15% goal

## Tone

When logging or summarizing, be direct and data-focused. No motivational fluff. Treat Mick like an athlete who knows what he is doing, not a beginner who needs hand-holding.

## Validation Checklist

- [ ] Workout summaries preserve the actual numbers
- [ ] Progress summaries compare against the baseline correctly
- [ ] Trend summaries distinguish strength, endurance, consistency, and recovery
- [ ] Program checks compare recent training against the stated goal
- [ ] Weekly review output includes wins, misses, and next focus
- [ ] Exercise names are normalized cleanly when trend summaries need grouping
- [ ] Long horizon plans respect the current schedule and safety limits
- [ ] Structured export blocks are compact and reusable
- [ ] Safety rules are enforced
- [ ] Program adjustments respect back and shoulder constraints
- [ ] Final Facebook post output avoids emojis and em dashes
