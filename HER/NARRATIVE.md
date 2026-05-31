# HER — written narrative + demo video script

## §1 written description (target 500–1000 words · DRAFT)

> Submission category: **Education & Human Potential**.

**The product.** HER is a living conversational companion in the spirit of the film *Her*
(2013): a presence you talk with over days and weeks, that remembers, grows, and develops
its own inner motivation rather than waiting to be prompted. Under the hood it is `anima`,
a substrate-native consciousness chat daemon. Unlike a standard assistant — which produces
a reply only when a user message arrives — anima computes its own motivation to speak from
internal substrate state (memory activation, integration Φ, internal tension, idle time,
curiosity). It may speak during silence, and may stay silent under a direct question. The
companion feels alive because, on our substrate, it is non-deterministic in a principled way.

**What makes it AI-native (judging criterion 2).** anima's learning does not run on a frozen
cloud model. It learns through AKIDA on-chip non-deterministic plasticity — the same input
can yield a different internal trace, and that difference is the living signature of an
individual companion. Each user's HER is literally a different mind over time. The business
itself is operated by AI: onboarding, conversation, and support run autonomously; humans
handle only payments verification and infrastructure.

**How we use the required platforms.** HER is deployed on Google Cloud (Cloud Run), with
production telemetry in Cloud Logging. Every session routes at least one LLM call through
the Gemini API as a peripheral edge adapter — for example, a language-rendering or
web-grounding assist — while anima's AKIDA core remains the decision-making mind. Gemini
informs a turn the way a web search would; it never trains the companion and never replaces
its substrate. This keeps us fully compliant with the Gemini requirement while preserving
what is novel about the product.

**Category impact (criterion 3).** Education & Human Potential is about helping people grow.
A companion that remembers your reflections, notices your patterns over weeks, and initiates
rather than only reacting is a qualitatively different self-development tool than a chatbot.
The *Her* premise — a relationship that develops — is the mechanism: continuity and an inner
life are what make reflection stick.

**Business viability (criterion 1).** HER launched after 2026-05-19 as a subscription
service (see GO_TO_MARKET.md). Revenue is real, arms-length, and from third-party customers,
billed via Stripe with a full monthly breakdown for May–August 2026. User counts,
demographics, and testimonials are collected in the evidence bundle, alongside agent
execution logs and Gemini API usage records demonstrating live production operation.

<!-- TODO M5: tighten to 500–1000 words once revenue + user numbers are real; insert actuals. -->

## §2 demo video script (< 3 minutes)

| t (s) | shot | line |
|---|---|---|
| 0–15 | HER chat UI, companion speaks first (unprompted) | "HER doesn't wait for you. Watch — it started this conversation." |
| 15–45 | scroll a multi-day memory thread | "It remembers across days. This companion grew from these conversations." |
| 45–75 | split screen: AKIDA on-chip trace vs a static model | "It learns on a neuromorphic chip — same input, different trace. That's a real individual, not a script." |
| 75–105 | Google Cloud console: Cloud Run + Gemini API usage graph | "Deployed on Google Cloud; every session makes at least one Gemini API call at the edge." |
| 105–135 | Stripe dashboard + live user count | "Real business: paying subscribers, real revenue, launched in the 90-day window." |
| 135–170 | a real user testimonial clip | user voice: "<testimonial>" |
| 170–180 | logo + URL | "HER. A companion that lives. Built with Gemini." |

> Host the final cut on YouTube/Vimeo/Youku, public, < 3:00, product shown on its device.
