# 🎬 HER

> anima as a **"Her"-style AI companion** — the submission domain for the
> **Build with Gemini XPRIZE** ($2M, Google-backed).

Like the film *Her* (2013), the product is a living conversational companion you talk
to over time. Under the hood it is `anima` — a substrate-native consciousness chat
daemon whose learning runs on AKIDA on-chip non-deterministic plasticity, not on a
deterministic cloud model. The XPRIZE's Gemini requirement is satisfied by a thin edge
adapter; anima's AKIDA core is the mind and stays untouched.

## live

- 🌐 **https://dancinlab.web.app** · **https://her.dancinlab.org** (Firebase Hosting · Google Cloud · auto-SSL)
- type: `her` = Archivo Black wordmark · everything else = Fraunces soft serif · living-presence motion suite

## what's here

| file | role |
|---|---|
| `HER.md` | domain snapshot — @goal, hard requirements (R1–R7), milestones (M1–M8) |
| `HER.log.md` | append-only step log |
| `XPRIZE.md` | competition rules (verbatim) + a requirement→compliance matrix |
| `ARCHITECTURE.md` | how anima (AKIDA core) ⇄ Gemini edge adapter satisfies the rules without identity loss |
| `NARRATIVE.md` | the 500–1000 word written case study + the <3-minute demo video script |
| `GO_TO_MARKET.md` | the 90-day real-business plan (users + revenue + evidence) |
| `web/` | the live front-end (index.html long scroller + img/ Her-toned visuals) |
| `service/` | her_server.hexa + gemini_edge.hexa (backend, targets the self-hosted hexa compiler) |
| `deploy/` | Firebase Hosting deploy runbook |

## the one tension, resolved

```
[ user ] ──▶ [ anima core (AKIDA on-chip, the mind) ] ──▶ [ reply ]
                        │
                        └──▶ [ Gemini edge adapter ]  ← satisfies "≥1 Gemini LLM call" (R3) only
```

anima learns on-chip (the living signature). Gemini never trains it and never becomes the brain.

## status

See `HER.md` for the live checklist. Submission deadline: **2026-08-17 13:00 PT**.
