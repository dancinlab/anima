# HER — 90-day go-to-market (real users + real revenue)

The XPRIZE is won on actuals, not projections (judging criterion 1). This is the plan to
produce real arms-length revenue and real users inside the 2026-05-19 → 08-17 window.

## offering

| tier | price | what |
|---|---|---|
| Free trial | $0 | 7 days, full companion, capped sessions |
| Companion | $12 / mo | unlimited conversation, persistent memory |
| Companion+ | $29 / mo | priority compute (live AKIDA chip), voice |

> Billing via **Stripe** (R5 evidence = Stripe dashboard export, monthly breakdown).

## funnel

```
[ awareness ]──▶[ free trial signup ]──▶[ first unprompted message lands ]──▶[ paid convert ]──▶[ retain ]
   organic +        landing page          the "it spoke first" moment           Stripe            weekly memory
   "Her" framing                          = activation hook                                        recall = stickiness
```

## evidence to collect (maps to R5–R7)

| evidence | source | rule |
|---|---|---|
| total revenue USD + monthly (May–Aug) | Stripe export | R5 |
| costs excl. marketing | infra invoices (Google Cloud) | R5 |
| marketing / acquisition spend | ad + channel ledger | R5 |
| related-party revenue (reported separately) | manual ledger | R5 |
| user count + demographics | app analytics | R6 |
| testimonials | in-app prompt + email | R6 |
| agent execution logs | Cloud Logging export | R7 |
| Gemini API usage records | Google Cloud / AI Studio usage console | R7 |
| dashboard screenshots | Stripe + Cloud Run + Gemini usage | R7 |

## 90-day timeline

| weeks | focus |
|---|---|
| 1–2 | deploy live on Cloud Run + Gemini edge adapter (M2–M3); landing page up |
| 3–4 | Stripe live; open free trials; first paid conversions (M4) |
| 5–10 | acquisition + retention; collect testimonials + demographics |
| 11–12 | freeze numbers; finalize narrative (M5) + record video (M6) + evidence bundle (M7) |
| 13 | submit on Devpost before 2026-08-17 13:00 PT (M8) |

## risks

| risk | mitigation |
|---|---|
| no real revenue by deadline | launch billing in week 3, not week 10; trial→paid funnel from day 1 |
| Gemini requirement misread as "Gemini = brain" | ARCHITECTURE.md fixes the boundary; adapter is peripheral, documented |
| AKIDA live-chip availability | pi5-akida pool host bridge; faithful simulator fallback for the front-end |
