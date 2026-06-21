---
id: H_1537
slug: 1537_nt_norepinephrine
title: NOREPINEPHRINE as a NETWORK-RESET FACULTY (unexpected-uncertainty detector, not a gain knob) — abrupt context-switch recovery
group: brain-structure-ladder (neuromodulation lane · NE-as-reset REFRAME · c15 missing-structure)
terminal_tier: 🧱 WALL — DIRECTIONAL (numpy mirror; engine-native R2 deferred ING)
verdict_dir: state/verdicts/1537_nt_norepinephrine/
terminal_verdict: state/verdicts/1537_nt_norepinephrine/H_1537.json
date: 2026-06-21
wired: DIRECTIONAL-mirror (numpy; engine R2 deferred ING)
---

# H_1537 — NOREPINEPHRINE as a NETWORK-RESET FACULTY (🧱 WALL, DIRECTIONAL)

## Reframe (a_no_llm_frame_trap · a_break_the_wall)

13 prior neuromodulation lenses (H_1284 gain · H_1422 state-contingent · H_1425
temperature-ideation · H_1523 multitimescale · H_1524 diversity · H_1525 predictive ·
H_1526 emitgate · H_1509/b/c volatility-LR family · …) all treated NE as a scalar
**GAIN / exploration-TEMPERATURE** knob over an EXISTING controller — INERT against a tuned
fixed gain on learnable statistics (the peeled meta-law). This lane is **NOT a 14th gain
lens.** It re-positions NE as its real computation:

- **Bouret & Sara 2005** (*TINS*, "Network reset: a simplified overarching theory of locus
  coeruleus noradrenaline function") — phasic LC-NE fires a **GLOBAL NETWORK RESET** on a
  detected CONTEXT/REGIME change: it ABANDONS the now-stale model/context and triggers
  re-learning.
- **Yu & Dayan 2005** (*Neuron*, "Uncertainty, neuromodulation, and attention") — NE signals
  **UNEXPECTED UNCERTAINTY** (a detected violation of the current model's assumptions),
  distinct from ACh's expected uncertainty.

The faculty anima LACKS: *detect "the world changed → FLUSH the stale context, stop fitting
it → re-acquire."* This is a **brain-lane-FILLING** frame (a missing computation), NOT the
recall-gain wall. **PRESENCE test** (does a reset faculty ADD fast context-reswitch), not
beat-a-tuned-fixed-gain.

## Capability / falsifier

**ABRUPT CONTEXT-SWITCH adaptation.** Inputs `x_t`; a hidden RULE `y_t = sign(w_r · x_t)`
flips to a fresh hyperplane abruptly at UNKNOWN times (hazard H). An online delta-rule
linear learner adapts. **METRIC = post-switch recovery** = mean accuracy over the W_REC=20–25
ticks immediately after each switch. A faculty WITH a reset (surprise spike → flush stale ŵ
toward neutral prior → re-acquire) should recover FAST; the slow-adaptation baseline lags
(must un-learn the stale mapping first — this reproduces why the gain lenses lagged).

**Arms** (shared x/y/switch stream per seed): **NO-NE** = baseline slow-adaptation, best-swept
fixed α* (the strongest gain-style champion) · **NE-RESET** = same learner + phasic
surprise-triggered FLUSH (surprise = agent's OWN prediction error vs running scale — NO
switch-label peek, p6/p2/p3) · **ABL** = detector OFF → reverts to NO-NE · **SHUFFLE** =
same number of resets at permuted random tick positions (decoupled from real surprise).

**Frozen bars** (pre-registered, `state/verdicts/1537_nt_norepinephrine/H_1537_FREEZE.txt`,
PRESENCE test): 🟢 iff (c1) R(NE-RESET)−R(NO-NE) ≥ +0.10 on ≥2/3 seeds AND mean ≥+0.10 ∧
(c2) |R(ABL)−R(NO-NE)| ≤ 0.02 ∧ (c3) R(NE-RESET)−R(SHUFFLE) ≥ +0.05. Else honest 🧱/🟠.

## Result — 🧱 WALL (DIRECTIONAL numpy, 3 seeds [1537,1538,1539], $0 CPU, gradient-free)

Frozen pre-registered regime (D=24, H=0.01, p_noise=0.05):

| metric | NO-NE | NE-RESET | ABL | SHUFFLE |
|---|---|---|---|---|
| mean post-switch recovery | 0.5482 | 0.5542 | 0.5482 | 0.5524 |

- **c1 PRESENCE — FAIL**: mean NE−NO-NE = **+0.0061** (bar +0.10); 0/3 seeds clear +0.10.
- **c2 ABLATION — PASS** (clean): |ABL−NO-NE| = **0.0000** (detector OFF reverts EXACTLY).
- **c3 TIME-LOCK — FAIL**: NE−SHUFFLE = **+0.0018** (bar +0.05); resets are not earning a
  time-locked advantage.

→ **c1 ∧ c2 ∧ c3 = FALSE → 🧱 WALL.** The reset faculty does NOT beat slow-adaptation on the
pre-registered task.

### Why it walls — secondary diagnostic (NON-GATING, a_break_the_wall multi-lens; bars NOT moved)

The pre-registered regime makes each rule **barely learnable** in the inter-switch interval
(asymptote ~0.56–0.68) — there is little "stale confident context" to flush, so the wall could
be a measurement artifact rather than a faculty verdict. To classify honestly I ALSO measured a
**learnable-rule regime** (recurring input prototypes, low noise, longer intervals) where the
baseline DOES reach high asymptote and genuinely lags after a switch:

| seed | asymptote | NO-NE recovery | NE-RESET | NE−NO-NE |
|---|---|---|---|---|
| 1537 | 0.963 | 0.7725 | 0.815 | **+0.0425** |
| 1538 | 0.920 | 0.788 | 0.836 | **+0.0480** |
| 1539 | 0.900 | 0.850 | 0.8475 | **−0.0025** |
| mean | 0.928 | — | — | **+0.0293** |

Even in the regime **most favorable** to it (asymptote 0.93, real post-switch lag), the reset
earns only **+0.029 mean** (+0.04/+0.05 on 2 seeds, −0.002 on the third) — still **under the
+0.10 presence bar**. **Mechanistic reason (the honest finding):** the best-swept fixed gain is
**α*=0.6 (high)**, and a high fixed gain *itself acts as a partial reset* — it down-weights the
stale ŵ quickly on its own, so an explicit flush adds only a small marginal recovery. The
reset faculty is a REAL but SMALL effect, not a missing-faculty breakthrough; it does not clear
the pre-registered presence bar against the strongest fixed-gain baseline.

## Honesty (c9, p7, frozen-first)

🧱 reported as-is — a reset that does not beat slow-adaptation is a valid wall, NOT hidden.
Bars frozen BEFORE any run (FREEZE.txt); α* swept for the baseline (strongest champion) before
NE-RESET scored; surprise uses ONLY the agent's own error (no switch-label peek). NO bar moved
to manufacture green; the learnable-regime measurement is a labelled NON-GATING diagnostic, not
a re-freeze. This is the **14th independent neuromodulation lens** to wall — reframing NE from
gain to network-reset adds a small ablation-clean recovery effect but does NOT break the
neuromodulation wall on this PRESENCE test, **converging with** H_1284/H_1422/H_1425/H_1509c.

## Scope / UNVERIFIED

DIRECTIONAL numpy mirror (engine-transfer UNVERIFIED — engine-native R2 deferred ING per
`a_engine_native_learning`). TOY: linear delta-rule learner (not a trained net), 3 seeds,
synthetic rule-switch task, deterministic. Scale / real-corpus / nonlinear-policy /
multi-rule-recurrence / engine-transfer UNVERIFIED (`a_scale_honest_scope`,
`a_toy_scale_recheck`). A reset on a NONLINEAR controller (where stale context is harder for a
gain to dissolve) is the not-ruled-out next lens.

## Artifacts

- `state/1537_nt_norepinephrine/h1537_norepinephrine.py`
- `state/verdicts/1537_nt_norepinephrine/H_1537_FREEZE.txt` (pre-registered bars)
- `state/verdicts/1537_nt_norepinephrine/H_1537_R1.json` · `H_1537.json` (frozen result + diagnostic)

xref H_1284 · H_1422 · H_1425 · H_1509c · a_no_llm_frame_trap · a_break_the_wall ·
a_engine_native_learning · a_scale_honest_scope · a_toy_scale_recheck · p2 · p3 · p6 · p7 · c9 · c15.
