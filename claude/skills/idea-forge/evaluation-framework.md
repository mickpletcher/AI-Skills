# IdeaForge Evaluation Framework

Reference for Stages 2 and 3. Defines how to interpret, classify, and expand an idea consistently.

---

## Idea Classification

Classify the idea into one primary type before expanding. Use the first type that fits. When an idea spans multiple types, note all that apply and pick the one that drives the core value.

| Type | Description | Examples |
| --- | --- | --- |
| Product | A discrete thing someone installs, buys, or subscribes to | Consumer app, hardware device, SaaS tool, browser extension |
| Automation | A workflow, job, or event-driven process that runs unattended | n8n flow, scheduled PS script, Home Assistant automation, cron job |
| Infrastructure | A system that hosts, connects, or manages other systems | Homelab config, Proxmox setup, self-hosted stack, network topology |
| Platform | A layer other things are built on top of | API, SDK, marketplace, developer tool, plugin ecosystem |
| Research | A hypothesis, experiment, or data analysis | Market study, ML experiment, academic question, A/B test design |
| Business model | A strategy for capturing value rather than creating a new product | Licensing approach, freemium design, service bundling, pricing structure |
| Integration | Connecting two existing systems | API bridge, webhook handler, sync service, protocol adapter |
| Process | A redesigned way of doing something operational | Hiring workflow, content pipeline, deployment process, review cadence |
| Creative | A content system, generative format, or media concept | Newsletter format, video series structure, AI-generated content pipeline |

---

## Feasibility Indicators

Use these signals when assessing Technical Feasibility in Stage 2.

**Positive signals (raise the score):**
- Core technology is proven and available as open source or a commercial API
- A working prototype could use existing libraries without novel algorithms
- The idea is essentially a combination or configuration of known components
- Clear precedent exists in an adjacent domain (same tech applied to a different problem)

**Negative signals (lower the score):**
- Requires real-time processing at a scale that current hardware cannot support economically
- Depends on an API, dataset, or model that does not exist yet
- Core mechanism has not been demonstrated in any published research or product
- Requires specialized hardware (sensors, ASICs, robotics) that is not commercially available

**Questions to answer:**
1. What is the hardest technical problem to solve?
2. What existing library, API, or platform is the closest starting point?
3. What is the failure mode if the hardest problem turns out to be harder than expected?

---

## Commercial Viability Indicators

**Painkiller vs. vitamin test:**
A painkiller solves a problem people are already paying to solve or living with significant cost. A vitamin is a nice-to-have that people say they want but do not urgently need. Painkillers score higher.

**Buyer identification test:**
Can you name a specific type of person or company that would pay for this next week? If the buyer is everyone, the buyer is no one.

**Positive signals:**
- People currently pay for an inferior version of this
- The problem causes quantifiable loss (time, money, risk, friction)
- A clear B2B buyer exists with a defined budget category (IT ops, security, dev tools, etc.)
- The idea maps to a known procurement category

**Negative signals:**
- The value is real but distributed — no single buyer captures enough benefit to justify paying
- The market requires changing established behavior without a strong forcing function
- The closest existing solution is free and widely adopted
- The buyer and the user are different people with misaligned incentives

---

## Patent Potential Assessment

Run this check before asserting patent potential.

**Step 1: Identify the novel claim**
A patent claim must describe a specific mechanism, process, or composition that is new. "An AI system that does X" is not a claim. "A method for scoring resume content using weighted multi-principle evaluation against a curated recruiter-sourced library" is closer.

**Step 2: Check for prior art indicators**
- Is this a known technique applied in a new domain? (Prior art likely exists in the source domain)
- Is this a combination of two known methods? (May be obvious — hard to patent)
- Does this describe a fundamentally new mechanism? (Stronger claim)

**Step 3: Assess protection value**
A patent is only valuable if enforcement is practical. Consider:
- Would a competitor clearly be infringing if they built a similar product?
- Is the core mechanism visible in the product (testable externally) or hidden in implementation?
- Is the market large enough that patent protection matters?

**Verdict options:**
- Strong patent potential: novel mechanism, specific process, defensible claim
- Narrow patent potential: novel angle exists but prior art is heavy
- No clear patent angle: combination of known methods or too abstract to claim
- Defer to a patent attorney: sufficient novelty to warrant a professional search

---

## Expansion Checklist

Use in Stage 3. Work through each category and generate content for any that produce meaningful output. Skip those that do not apply.

### Features and Capabilities
- [ ] What is the minimal version that still delivers real value?
- [ ] What would make version 2 significantly better than version 1?
- [ ] What edge cases does the current framing break on?
- [ ] What would a power user want that a typical user would not?

### Integration Opportunities
- [ ] What existing platforms would this plug into naturally? (Slack, GitHub, Home Assistant, Obsidian, n8n, Intune, etc.)
- [ ] What webhook or event-driven trigger could automate input into this?
- [ ] What output format or API would let other tools consume this?

### AI Enhancement
- [ ] Where does a language model add value? (Classification, generation, summarization, extraction)
- [ ] Where do embeddings and semantic search add value? (Similarity, deduplication, retrieval)
- [ ] Where does a local LLM make sense over a cloud API? (Privacy, cost, latency)
- [ ] What agent or tool-use pattern fits? (Single-shot, multi-step, memory-backed)

### Automation Paths
- [ ] What triggers this? (Schedule, event, webhook, sensor, user action)
- [ ] What runs after the trigger without human input?
- [ ] What conditions require a human decision?
- [ ] What is the failure mode and how does the system recover?

### Business Models (apply all that fit)
- [ ] SaaS subscription — what tier structure makes sense?
- [ ] One-time purchase — what is the natural price point?
- [ ] Usage-based — what is the billable unit?
- [ ] Open source + hosted — what does the paid tier add?
- [ ] White-label licensing — who would re-brand this?
- [ ] API access — who builds on top of this?
- [ ] Consulting or services — who needs help implementing this?

### Local-First Alternative
- [ ] What would a version running fully on local hardware look like?
- [ ] What cloud dependencies could be replaced with open-source equivalents?
- [ ] What is lost in a local-first version versus a cloud version?

### Privacy and Security
- [ ] What personal data does this handle?
- [ ] What credentials or API keys does this require?
- [ ] What is the blast radius if this system is compromised?
- [ ] What regulations might apply? (GDPR, HIPAA, SOC 2, CCPA)

---

## Idea Relationship Signals

When processing multiple ideas over time, flag these patterns:

- **Complements**: Idea A and Idea B solve different parts of the same problem and would work better together.
- **Prerequisite**: Idea B is only viable if Idea A exists first.
- **Monetizes**: Idea C provides a revenue path for Idea D which currently lacks one.
- **Conflicts**: Idea E and Idea F target the same market with incompatible assumptions — pick one or reconcile the difference.
- **Supersedes**: A newer idea makes an older one redundant or obsolete.

Note: Full relationship mapping across an idea library is a future upgrade. For now, flag obvious relationships in the output when the user references multiple ideas in the same session.
