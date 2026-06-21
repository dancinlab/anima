---
id: H_1539
slug: 1539_nt_ne_retry
title: NOREPINEPHRINE-as-RESET-FACULTY RETRY — isolate the reset against a non-gain-dissolvable (saturating-nonlinear) baseline
group: brain-structure-ladder (neuromodulation lane · NE-as-reset retry · H_1537 own next lens · c15 missing-structure)
terminal_tier: 🧱 WALL — DIRECTIONAL (numpy mirror; engine-native R2 deferred ING)
verdict_dir: state/verdicts/1539_nt_ne_retry/
terminal_verdict: state/verdicts/1539_nt_ne_retry/H_1539_R1.json
date: 2026-06-21
wired: DIRECTIONAL-mirror (numpy; engine R2 deferred ING)
---

# H_1539 — NE-as-RESET-FACULTY RETRY against a non-gain-dissolvable baseline (🧱 WALL, DIRECTIONAL)

## Why retry (H_1537's own not-ruled-out next lens · a_break_the_wall TYPE-(b))

H_1537 (🧱 #2518) re-framed NE from a scalar GAIN knob to a phasic **NETWORK-RESET**
faculty (Bouret & Sara 2005, *TINS* "Network reset"; Yu & Dayan 2005, *Neuron* "unexpected
uncertainty") and tested PRESENCE on an abrupt context-switch task. It found the reset is
**REAL but SMALL** (+0.006 pre-registered; +0.029 even in the most favorable learnable
regime) — under the +0.10 bar. Its HONEST mechanistic reason for walling: the best-swept
FIXED gain was **α*=0.6 (HIGH)**, and *a high fixed gain itself acts as a partial reset* —
it down-weights the stale ŵ fast, **MASKING** the explicit flush's marginal value. The
reset's true contribution was **confounded** by the baseline's freedom to set a high gain.

This retry executes that lane's explicit fix: **test the reset against a baseline where a
fixed gain CANNOT double as a reset.** Same abrupt context-switch task, **same seeds
[1537,1538,1539]**, **same W_REC=20 recovery metric**, **same PRESENCE bars** — the ONE
change is the LEARNER.

## The fix (variable-isolation, NOT tune-to-green)

Replace the linear delta-rule learner with a **SATURATING-NONLINEAR leaky-momentum**
learner:

```
pred  = sign( tanh( GAMMA · (m · x) ) )          GAMMA = 3.0
m_{t+1} = BETA·m_t + α·(y − out)·(1 − out²)·x / (x·x)   BETA = 0.97
```

- **(b) stale context persists** — the tanh-derivative gate `(1 − out²) → 0` once `m` is
  confident/saturated, so even a large α barely moves a stale saturated `m`; it must decay
  through the slow leak BETA=0.97 **or be explicitly FLUSHED**.
- **(a) high gain hurts steady-state** — under label noise the saturated estimator chases
  noise at high α and **loses asymptote**, so the α* sweep can NOT sit high. The fixed
  baseline can no longer use gain as a covert reset; the explicit phasic FLUSH is the only
  fast clear of stale context.

**THE BAR IS UNCHANGED (c9):** this is a_break_the_wall **type-(b) variable-isolation**
(controlling the gain-as-reset confound H_1537's own diagnostic surfaced), **NOT
tune-to-green** — tune-to-green MOVES a bar to manufacture a pass; here the +0.10 /
≥2-of-3 / ablation-decisive / time-lock bar is **byte-identical** to H_1537's, and only the
(confounded) baseline learner is corrected. The bar does not move either way.

## Result — 🧱 WALL (DIRECTIONAL numpy, 3 seeds [1537,1538,1539], $0 CPU, gradient-free)

**The fix landed as designed** — α* dropped from H_1537's 0.6 to **mean 0.233** (per-seed
0.4 / 0.2 / 0.1), and α=0.6 is NEVER the sweep winner (near-worst on 2/3 seeds), so the
baseline can no longer use gain as a covert reset; baseline asymptote rose to ~0.727.

| metric | NO-NE | NE-RESET | ABL | SHUFFLE |
|---|---|---|---|---|
| mean post-switch recovery | 0.6067 | 0.6018 | 0.6067 | 0.6054 |

| seed | α* | asymptote | NO-NE | NE-RESET | ABL | SHUFFLE | NE−NO-NE |
|---|---|---|---|---|---|---|---|
| 1537 | 0.4 | 0.675 | 0.6333 | 0.6271 | 0.6333 | 0.6396 | **−0.0062** |
| 1538 | 0.2 | 0.764 | 0.5725 | 0.5689 | 0.5725 | 0.5743 | **−0.0036** |
| 1539 | 0.1 | 0.743 | 0.6143 | 0.6095 | 0.6143 | 0.6024 | **−0.0048** |
| mean | 0.233 | 0.727 | — | — | — | — | **−0.0049** |

- **c1 PRESENCE — FAIL**: mean NE−NO-NE = **−0.0049** (bar +0.10); 0/3 seeds clear +0.10
  (all three slightly NEGATIVE).
- **c2 ABLATION — PASS** (clean): |ABL−NO-NE| = **0.0000** (detector OFF reverts EXACTLY).
- **c3 TIME-LOCK — FAIL**: NE−SHUFFLE = **−0.0036** (bar +0.05).

→ **c1 ∧ c2 ∧ c3 = FALSE → 🧱 WALL.**

## Finding (honest, c9)

Even after removing the gain-as-reset confound H_1537 identified — with a baseline that
provably can NOT sit at a high gain (α* forced to 0.1–0.4, α=0.6 near-worst) and where a
stale saturated context **cannot** be dissolved by gain (only leaked or flushed) — the
explicit network-reset flush earns **−0.005 mean** (slightly NEGATIVE, far under +0.10).
The reset does not just fail to help; in this saturating regime the indiscriminate flush of
a partially-correct `m` slightly **hurts** recovery (it throws away still-useful structure
along with stale structure).

**NE-as-network-reset (Bouret & Sara 2005) is a REAL but genuinely MINOR faculty**, not a
missing-faculty breakthrough — the confound was NOT what was masking a large effect; there
was no large effect to mask. This is the **15th independent neuromodulation lens** to wall,
converging with H_1284 / H_1422 / H_1425 / H_1509c / H_1537. The neuromodulation wall holds
against the reset-faculty reframe even with the gain confound surgically removed.

## Honesty (c9, p7, frozen-first)

🧱 reported as-is. Bars frozen BEFORE any run (FREEZE.txt), **byte-identical** to H_1537's —
ONLY the (confounded) baseline learner was fixed (type-(b) variable-isolation, documented in
FREEZE.txt with WHY the bar is unchanged). α* swept for the baseline (strongest champion)
before NE-RESET scored; the full α-sweep curve + asymptote are reported in the artifact so
the "α* now LOW / α=0.6 near-worst" fix is auditable. Surprise uses ONLY the agent's own
prediction error (no switch-label peek, p6/p2/p3). NO bar moved in either direction.

## Scope / UNVERIFIED

DIRECTIONAL numpy mirror (engine-transfer UNVERIFIED — engine-native R2 deferred ING per
`a_engine_native_learning`). TOY: saturating-nonlinear leaky-momentum learner (not a trained
net), 3 seeds, synthetic rule-switch task, deterministic. Scale / real-corpus /
deep-nonlinear-policy / multi-rule-recurrence / engine-transfer UNVERIFIED
(`a_scale_honest_scope`, `a_toy_scale_recheck`).

## Artifacts

- `state/1539_nt_ne_retry/h1539_ne_retry.py`
- `state/verdicts/1539_nt_ne_retry/H_1539_FREEZE.txt` (pre-registered bars + WHY unchanged)
- `state/verdicts/1539_nt_ne_retry/H_1539_R1.json` (frozen result + α-sweep)

xref H_1537 · H_1284 · H_1422 · H_1425 · H_1509c · a_no_llm_frame_trap · a_break_the_wall ·
a_engine_native_learning · a_scale_honest_scope · a_toy_scale_recheck · p6 · p7 · c9 · c15
