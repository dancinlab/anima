# Build with Gemini XPRIZE — rules & compliance matrix

Source of truth: <https://xprize.devpost.com/rules> (fetched 2026-06-01).
This file maps each rule to how the HER submission of `anima` complies.

## key dates

| phase | window |
|---|---|
| submission | 2026-05-19 10:00 PT → 2026-08-17 13:00 PT |
| judging | 2026-08-18 → 09-15 |
| winners announced | ~2026-09-25 |

## prize structure

| placement | award |
|---|---|
| 1st | $500,000 |
| 2nd | $200,000 |
| 3rd–5th | $100,000 each |
| 15 runner-ups | $50,000 each |
| 5 category winners | $50,000 each |

> A project qualifies for at most one prize.

## eligibility

| who can enter | who cannot |
|---|---|
| individuals at legal majority | residents of sanctioned countries (RU, Crimea, CU, IR, KP) |
| teams of eligible individuals | XPRIZE / Devpost / promotion-entity employees |
| orgs with < 25 employees | judges + their employers · conflicts of interest |

## requirement → compliance matrix

| # | rule (verbatim intent) | HER compliance |
|---|---|---|
| R1 | project newly created after 2026-05-19 | "HER" companion product + business entity launched post-cutoff; anima codebase is pre-existing infra, the *business/service* is new |
| R2 | use ≥1 Google Cloud product | deploy the chat daemon on Google Cloud (Cloud Run / GKE) — see ARCHITECTURE.md |
| R3 | LLM functionality → ≥1 Gemini API LLM call | thin Gemini edge adapter makes ≥1 call per session; AKIDA core untouched |
| R4 | business operated by AI agents | anima is substrate-native (computes its own motivation from M/C/W/MITOSIS state); ops agents run onboarding/support |
| R5 | real arms-length third-party revenue (USD, monthly May–Aug) | Stripe subscriptions; monthly breakdown + costs + marketing spend disclosed |
| R6 | real users + demographics + testimonials | acquired during the 90-day window; collected in evidence bundle |
| R7 | production-operation evidence | agent execution logs + Gemini API usage records + dashboard screenshots |

## category (1 of 5)

Chosen: **Education & Human Potential** — a companion that supports emotional growth,
reflection, and self-development over time (the *Her* premise), advancing human potential.

> Alternatives considered: Professional Services (coaching), Small Business Services (N/A).
> Education & Human Potential best fits a personal companion.

## required deliverables checklist

- [ ] source repo (public w/ license, or private shared w/ testing@devpost.com + judging@hacker.fund)
- [ ] demo video < 3 min, public on YouTube/Vimeo/Youku, shows the product on its device
- [ ] written description — how it meets requirements + fits the category + which APIs used
- [ ] revenue evidence — total USD + monthly breakdown (May–Aug) + costs (excl. marketing) + marketing spend + related-party revenue separate
- [ ] user evidence — user count + demographics + testimonials
- [ ] production evidence — agent execution logs · Gemini API usage records · dashboard screenshots
- [ ] org corporate ID (if entering as an organization)

## judging (2 stages)

1. **Stage one (pass/fail):** reasonably fits the theme + reasonably applies the required APIs/SDKs.
2. **Stage two (3 equally weighted criteria):**
   - Business viability — real business launched, real users acquired, real revenue earned.
   - AI-native operations — business actually run through AI in production.
   - Category impact — meaningful advancement / credible scale within the category.
