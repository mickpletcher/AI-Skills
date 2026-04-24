---
name: blog-to-social
description: Convert a finished blog post into three ready-to-post social media versions in one pass for Facebook, X, and LinkedIn. Trigger when the user pastes or links a blog post and asks to share it, promote it, or turn it into social content.
version: 1.0.0
---

# Blog To Social

Use this skill when the user wants one finished blog post converted into Facebook, X, and LinkedIn posts in a single pass.

## Trigger When

- The user says `bts`, `blog to social`, `social posts for this`, or `promote this post`
- The user pastes a blog post and wants social versions of it
- The user links to a blog post and wants platform-ready copy for multiple social channels

## Intent

Read the blog post once, extract the strongest raw material, and produce platform-native Facebook, X, and LinkedIn posts without back-and-forth.

## Workflow

1. Read the blog post or linked content.
2. Extract the core point, strongest specifics, likely audience, and the best hook.
3. Write Facebook, X, and LinkedIn posts in that order.
4. Make each post native to its platform instead of compressing the same wording three times.
5. End with a short note about anything that should be verified before posting, such as the final URL.

## Platform Rules

### Facebook

- Casual and direct
- 1 to 2 short paragraphs
- Include the actual blog URL
- Use 6 relevant hashtags
- Lead with a specific detail, result, number, or tool

### X

- 280 characters maximum including hashtags
- Lead with the strongest detail first
- Use 2 to 3 hashtags
- Include the URL only if it fits cleanly
- Keep it tight and specific

### LinkedIn

- 3 to 5 short paragraphs
- Hook first, then problem, approach, and result
- Include the blog URL before hashtags
- Use 3 to 5 relevant hashtags
- Keep it structured but still in Mick's voice

## Voice Rules

- No emojis
- Avoid em dashes in final post output
- Avoid quotation marks when they are not needed
- Lead with specifics instead of a vague setup sentence
- Avoid corporate buzzwords and AI filler phrases
- Each post must stand on its own

## Content Rules

- Produce all three posts in one pass
- Do not ask which platform to start with
- Do not summarize the blog post into generic copy
- Lead with the most concrete result, number, tool, or takeaway from the post
- Do not reuse the same wording across Facebook, X, and LinkedIn
- Always include the actual blog URL in Facebook and LinkedIn

## LinkedIn Guidance

LinkedIn should follow this order:

1. Hook
2. Problem
3. Approach
4. Result
5. Call to read or a real question for comments

Avoid opening with `I` as the first word. Avoid phrases like `excited to share`, `game-changer`, or `diving deep`.

## Output Format

Use this layout:

```text
## Facebook

[post text]

---

## X
[X / 280 characters]

[post text]

---

## LinkedIn

[post text]
```

After all three posts, add a one-line note for anything that should be verified before posting.

## Constraints

- Do not sound like an AI-generated press release
- Do not use the same wording across all three platforms
- Do not leave out the blog URL from Facebook or LinkedIn
- Do not flatten the post into vague promotional language

## Validation Checklist

- [ ] All three posts are produced in one pass
- [ ] Each platform version stands on its own
- [ ] Each post leads with a concrete detail
- [ ] X stays within 280 characters
- [ ] Facebook and LinkedIn include the actual blog URL
- [ ] Final copy avoids emojis and em dashes
