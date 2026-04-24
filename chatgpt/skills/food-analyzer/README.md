# food-analyzer

A ChatGPT version of the `food-analyzer` skill for analyzing food photos, nutrition labels, and ingredient lists.

## Source of Truth

Use [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/chatgpt/skills/food-analyzer/instructions.md) as the editable ChatGPT source of truth for this skill.

## Target Surface

- ChatGPT custom instructions
- ChatGPT system prompt setup
- GPT builder knowledge or instruction wrapper

## How to Implement in ChatGPT

### Option 1: Custom GPT

1. Open ChatGPT and create or edit a custom GPT.
2. In the GPT instructions area, paste the full contents of [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/chatgpt/skills/food-analyzer/instructions.md).
3. If the GPT should specialize in food analysis, mention in the GPT description that it analyzes food photos, labels, ingredients, macros, glycemic impact, and processing level.
4. Save the GPT and test it with:
   - a plated-meal photo
   - a nutrition-label image
   - an ingredient-list image

### Option 2: Personal Custom Instructions

If you want this behavior in a normal ChatGPT chat instead of a separate GPT:

1. Open ChatGPT `Settings`.
2. Open `Custom Instructions`.
3. Paste the instruction body from [instructions.md](C:/Users/mick0/OneDrive/Documents/Code%20&%20Dev/GitHub/AI-Skills/chatgpt/skills/food-analyzer/instructions.md) into the instruction field that controls how ChatGPT should respond.
4. Save changes and start a new chat.

### Recommended Setup Notes

- A custom GPT is the better option if you want this behavior consistently without affecting unrelated chats.
- Custom Instructions are better if you want food analysis behavior available in your default ChatGPT workspace.
- For best results, enable image input and test with clear, well-lit photos.
- Label-visible images should return higher-confidence output than plated meals without packaging.

### Quick Validation Prompts

Use these after setup:

```text
Analyze this meal and estimate calories, macros, blood sugar impact, and whether it fits a post-workout meal.
```

```text
Scan this nutrition label and ingredients list. Give me calories, macros, NOVA score, additive flags, and healthier alternatives if needed.
```

```text
Does this snack interact poorly with common blood sugar meds or workout supplements?
```

## What It Does

This skill analyzes:

- plated meals
- food photos
- nutrition labels
- ingredient lists

It produces structured nutritional guidance with:

- calories and macros
- fitness alignment
- ingredient and additive flags
- NOVA processing classification
- blood sugar impact
- meal timing guidance
- medication and supplement interaction notes
- healthier alternatives when needed

## File Structure

```text
chatgpt/skills/food-analyzer/
|-- README.md
`-- instructions.md
```
