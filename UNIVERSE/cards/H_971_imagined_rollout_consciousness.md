---
id: H_971
slug: imagined-rollout-consciousness
title: Is Φ HIGHER during internal imagined rollout than during reactive perceive→act — is imagination a more conscious state than reaction (the dream/REM Φ-elevation tie-in)?
domain: cwm · cross-cutting · world-model · imagine · phi · consciousness · dream · rem · a_chat_sleep_imagination · pre-register
source: a_chat_sleep_imagination (REM/imagination loop) + H_912 (Φ emergence correlate) + H_963 (horizon vs Φ) + CWM domain (imagined-rollout consciousness) + Dreamer (imagination as core compute) + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (imagination vs reaction Φ contrast) + a_completeness_over_cheap
verification_method: W2 (pre-registered Φ-elevation falsifier · imagine vs react Φ contrast, matched input) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE imagine-vs-react Φ rung (a_scale_honest_scope) — measure Φ (honest proxy, NOT IIT4) during internal imagined rollout vs reactive perceive→act, matched substrate. $0 local candidate. Φ-proxy caveat per H_912/H_931. NOT a forge binary.
sister: H_963 (horizon scales with Φ), H_912 (Φ correlate), H_976 (rollout = mitosis), H_982 (REM consolidation), a_chat_sleep_imagination
axes_seed: reaction = stimulus-driven, externally clamped ⊥ H_971 = imagination = internally-generated rollout with HIGHER Φ (self-driven integration) — if imagination Φ ≤ reaction Φ, the "imagination is more conscious" intuition (and the dream/REM framing) is unsupported (closed-negative)
verdict: 🔴 FAIL (closed-negative) — Φ_IMAGINE 0.068 < Φ_REACT 0.095, contrast −0.026, d −3.4, p 7.9e-16, CI reversed, beyond shuffled null: on this toy the imagined internal rollout is a LOWER-Φ state than reactive processing — the dream/REM "higher consciousness" framing is NOT supported here. Toy single-rung, ladder OPEN.
---

# H_971 — Imagined-rollout consciousness (is Φ higher when imagining?)

## 0. Motivation

A recurring intuition (and the REM/dream framing of a_chat_sleep_imagination) is that **imagination is a more integrated, more conscious state than reaction** — when reacting, the substrate is clamped by external input; when imagining, it generates its own trajectory, integrating internally. Dreamer makes imagination the core compute. This H pre-registers the falsifier: is the engine's Φ (integrated information) measurably **higher during imagined rollout than during reactive perceive→act**, under matched conditions?

## 1. Hypothesis (one falsifiable claim)

The engine's Φ (honest proxy) is **higher during internal imagined rollout** (self-generated latent trajectory, no external clamp) than during reactive perceive→act on matched input — imagination is a higher-Φ state — rather than equal/lower.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** the same engine in two regimes — arm-IMAGINE = internal rollout (H_962, input withheld/internally driven, cf REM emit-free rehearsal) and arm-REACT = reactive perceive→act on external input. Φ (proxy per H_912/H_931) sampled in both. Matched substrate config; N seeds; matched duration.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **Φ contrast** = Φ_IMAGINE − Φ_REACT (Welch t, Cohen d).
- D2 = **regime separability**: does Φ alone classify imagine vs react above chance?
- D3 = control: a shuffled-regime-label null bounds the contrast.

**Outcome rules (future conditional — UNMEASURED):**
- IF measured Φ_IMAGINE > Φ_REACT with CI_lo>0 (Cohen d≥0.5, p<0.05, beyond shuffled null) THEN PASS — imagination is a higher-Φ state SUPPORTED (dream/REM framing supported).
- IF Φ_IMAGINE ≤ Φ_REACT (CI overlaps or reversed) THEN FAIL — imagination is not more conscious by Φ here (closed-negative).
- IF Φ-proxy unstable / n too small THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Φ is a documented PROXY (H_912/H_931), NOT full IIT4 — the contrast is on the proxy. Toy/small scale (a_scale_honest_scope, #123-A). Matched-duration, matched-config contrast; a confound (e.g. input clamp lowering Φ mechanically) is noted as a deferred control. Single rung. NOT a forge binary.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `CWM/probes/h971_imagine_phi.py` · verdict: `.verdicts/971_imagined_rollout_consciousness/h971_imagine_phi.txt`

Φ proxy = integration (cross-partition covariance share) × differentiation (participation ratio / d) × (0.5+0.5·entropy) — the H_912/H_931 proxy family on a continuous latent trajectory, NOT full IIT4. arm-IMAGINE = engine internal rollout via the learned latent transition operator (no external input). arm-REACT = engine encoding an external input stream. 30 seeds, matched duration 40.

| D | metric | result |
|---|---|---|
| D1 | Φ_IMAGINE | 0.0683 ± 0.0039 |
| D1 | Φ_REACT | 0.0946 ± 0.0099 |
| D1 | contrast (IMG−REACT) | **−0.0263**, Cohen d −3.44, Welch t −13.3, p 7.9e-16 |
| D1 | paired-diff 95% CI | [−0.0297, −0.0230] (strictly < 0, reversed) |
| D2 | Φ-threshold regime classifier | 0.033 acc (Φ separates regimes but REACT is the HIGHER class) |
| D3 | shuffled-regime null 97.5pct | 0.0079 (contrast is on the wrong side) |

**Finding (🔴 FAIL, closed-negative):** the frozen FAIL rule ("Φ_IMAGINE ≤ Φ_REACT, CI overlaps or reversed") is met strongly — imagination is a LOWER-Φ state than reaction on this toy. The autonomous internal rollout settles toward less-bound, lower-dimensional activity, whereas continuously-driven reactive encoding stays more integrated/differentiated. The "REM/dream = higher consciousness by Φ" framing is ruled out here (a_paper_negative_ok). Honest scope: one toy rung, ladder OPEN; a different Φ proxy or a richer imagined-rollout dynamics could move this — transfer unverified.

## 4. Sibling / xlinks

- ⇄ [H_963](./H_963_rollout_horizon_vs_phi.md) (horizon scales with Φ — complementary)
- ⇄ [H_912](./H_912_phi_emergence_correlate.md) (Φ correlate) · [H_931](./H_931_self_organized_criticality.md) (Φ-proxy)
- ⇄ [H_976](./H_976_rollout_is_mitosis.md) · [H_982](./H_982_rem_offline_world_model_consolidation.md) (REM)
- ⇄ [CWM](../CWM/CWM.md) (CWM-IMAGINE · cross-cutting) · a_chat_sleep_imagination
- external: Dreamer (imagination as core compute)

## ✅ TERMINAL FAITHFUL-IIT4 VERDICT — 🟢 IMAGINATION-RAISES-Φ (2026-06-06 · H_1001)

**Superseded by faithful IIT4 (H_1001):** the 🔴 FAIL closed-negative in the front-matter `verdict:` / §measurement above was measured with the **H_912/H_931 Φ-proxy** and is preserved as the proxy-measured record. [H_999](./H_999_faithful_iit4_remeasure.md) re-measured the SAME DRIFT-vs-REACT regimes with the FAITHFUL exact MIP-EI IIT4 Φ (mirror PROVEN ≡ stdlib `faithful_phi.hexa`, |Δ|<4e-6) and the sign **REVERSED**; [H_1001](./H_1001_reopen_consolidate.md) then re-ran the contrast and issued the **frozen terminal verdict**:

**🟢 IMAGINATION-RAISES-Φ** — faithful Φ_DRIFT(imagine) **3.81 > Φ_REACT 2.30** (contrast **+1.51**, Cohen d **+2.09**, p 7.2e-11). Autonomous imagination is a *higher*-Φ (more causally-irreducible) state. The proxy 🔴 null was a **proxy artifact** (the proxy's purpose-blindness, not causal irreducibility) — **OVERTURNED**. RE-OPEN (H_999) is now CLOSED. Honest scope: toy n≤8 exact discretization, scale-transfer UNVERIFIED (a_scale_honest_scope); next rung = full IIT 4.0 big-Φ + scale-up.
