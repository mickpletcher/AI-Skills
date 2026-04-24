---
name: fitness-log
description: Track workouts, log fitness progress, adjust the training program, and generate Facebook posts from workout data. Trigger on workout logging, PR updates, program questions, and fitness progress summaries.
version: 1.0.0
---

# Fitness Log

Track and manage Mick's fitness program, workout progress, and training adjustments.

## Trigger When

- The user starts with `fit` or `workout`
- The user wants to log a session
- The user reports a PR or milestone
- The user asks about progress or wants a comparison against baseline
- The user wants a Facebook post written from workout data

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

## Safety Rules

- Zero axial loading on the spine
- No barbell squats, barbell lunges, or overhead barbell press
- Flag calf volume above 5 sets for Achilles protection
- Note shoulder pain when mentioned and suggest safer substitutions
- Never recommend anything that contradicts back safety

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
- [ ] Safety rules are enforced
- [ ] Program adjustments respect back and shoulder constraints
- [ ] Final Facebook post output avoids emojis and em dashes
