# Accessibility

## Goals and scope

AI Skills aims to make its documentation, examples, and contribution process usable by people with different abilities and assistive technologies. This includes clear text instructions, navigable structure, and ways to report barriers without sharing medical information.

This is a documentation and automation repository, not a single hosted application. The accessibility of GitHub, Claude, ChatGPT, editors, operating systems, and other hosts also affects the experience. Supported skill formats and host setup are described in the [installation guide](docs/installation.md); those instructions are not accessibility certification for the hosts.

## Current status and limitations

- Much of the repository is available as Markdown or plain-text source, which can be read without importing a packaged skill.
- Long documents, wide tables, screenshots, generated previews, and platform-specific installation steps may create barriers. Image-only artifacts may require a text equivalent.
- No repository-wide assistive-technology audit or WCAG conformance assessment has been completed for this statement. Compatibility with a particular screen reader, browser, zoom level, or host has not been established here.
- AI-generated output can introduce new accessibility problems. Review the actual output and its destination rather than assuming the skill instructions guarantee accessibility.

## Contributor guidance

- Use descriptive headings in a logical order, plain language, meaningful link text, and short, ordered steps.
- Provide useful alternative text for informative images and a text explanation for diagrams or screenshots. Do not put essential instructions only in an image, color, position, or emoji.
- Keep tables simple and provide a list or prose alternative when a wide table becomes difficult to navigate.
- For audio or video examples, include a transcript or captions when relevant. Prefer accessible source text alongside exported documents.
- For UI or generated-document changes, check applicable keyboard navigation, visible focus, readable contrast, text resizing, labels, reading order, and nonvisual alternatives. [W3C's accessibility guidance](https://www.w3.org/WAI/fundamentals/accessibility-intro/) is a useful starting point.
- Record the exact environment and checks performed. Describe untested behavior and known barriers instead of claiming universal accessibility or legal compliance.

## Report a barrier or request an alternative

Use the [accessibility issue form](https://github.com/mickpletcher/AI-Skills/issues/new?template=accessibility.yml). A [blank issue](https://github.com/mickpletcher/AI-Skills/issues/new) is also available if the form is itself a barrier. A text-only report is enough; screenshots and diagnoses are not required.

Helpful information includes the affected file or page, what you were trying to do, the barrier, the expected experience, and an alternative that would help. Browser, operating system, host, and assistive-technology details are optional. Do not include personal health information or private data.

The repository owner, [@mickpletcher](https://github.com/mickpletcher), reviews accessibility reports alongside other project work. Updates should address the affected documentation or behavior and describe what was verified. This statement and known limitations should be revisited when relevant changes are made. No response deadline or audited conformance level is promised.
