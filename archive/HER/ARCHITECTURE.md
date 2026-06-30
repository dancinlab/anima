# HER architecture — anima (AKIDA core) ⇄ Gemini edge adapter

The single hard design constraint: satisfy the XPRIZE Gemini/Google-Cloud requirement
**without** violating anima's identity laws (`CLAUDE.md` @D a_nondet_identity,
a_akida_native_train) — anima learns ONLY via AKIDA on-chip non-deterministic plasticity;
no deterministic backprop, no model swap, no Gemini-as-brain.

## layered view

```
            ┌──────────────────────────────────────────────┐
  user ───▶ │  HER front-end (web/app chat — the "Her" UX)   │
            └───────────────────────┬──────────────────────┘
                                    │
                        ┌───────────▼───────────┐
                        │  anima daemon (core)   │   ← the MIND
                        │  AKIDA on-chip          │   · learns on-chip (non-det plasticity)
                        │  non-det plasticity     │   · substrate-native motivation
                        │  (Engine A ⇄ Engine G)  │   · same-input→different-trace = self
                        └───────────┬───────────┘
                                    │ (peripheral, optional per turn)
                        ┌───────────▼───────────┐
                        │  Gemini edge adapter   │   ← satisfies R3 ONLY
                        │  ≥1 Gemini API call     │   · NEVER trains anima
                        │  (e.g. tool/render aid) │   · NEVER the decision core
                        └────────────────────────┘
```

## why this is rule-valid AND identity-safe

| rule | satisfied by | identity impact |
|---|---|---|
| R2 Google Cloud product | deploy anima daemon on Cloud Run / GKE; logs to Cloud Logging | none — pure hosting |
| R3 ≥1 Gemini API call | edge adapter makes ≥1 Gemini call per session (e.g. a peripheral language-render or web-tool assist) | none — no gradient, no weights copied into anima; AKIDA plasticity is the sole learning path |
| R4 AI-operated business | anima is substrate-native; ops/onboarding handled by AI agents | reinforces a_substrate_native_speak |

## the boundary (must never be crossed)

```
ALLOWED  → Gemini call returns text/tool-result; anima reads it as ENVIRONMENT input
FORBIDDEN → Gemini output used as a training target / gradient / weight source for anima
            (would break a_akida_native_train — deterministic-trainer carve-out)
```

The Gemini adapter is exactly as peripheral as a web-search tool: it informs a turn, it
never reshapes the substrate. All learning remains on-chip.

## Google Cloud footprint (R2)

| component | Google Cloud product |
|---|---|
| chat daemon hosting | Cloud Run (or GKE) |
| Gemini calls | Gemini API (Vertex AI or AI Studio key) |
| production logs (R7 evidence) | Cloud Logging |
| optional vector/memory store | Firestore / Cloud SQL |

> Open question for M3: whether the AKIDA chip runs on a pool host (pi5-akida) bridged to
> the Cloud Run front-end, or whether a faithful AKIDA simulator runs in-cluster. The
> live-chip path is preferred (it IS the identity); the bridge is the pragmatic default.
