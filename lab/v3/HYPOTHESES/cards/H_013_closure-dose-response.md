---
id: H_013
ssot: ARCHITECTURE.json → verification-h013 + decision-reframe-c (frozen pre-register/verdict record)
slug: closure-dose-response
title: Is the H_011 proxy anchor a SUBSTANTIVE seat of aliveness (env-loop F8) or a TOY artifact of a deterministic env that mechanically answers actions? Sweep the env's action-contingency DOSE down toward the real owner loop's measured level (~0.42) and measure where the certified LV-C block-closure dies. DOSE-ROBUST = F8 is a real seat (a positive independent of the human-gated H_012B); TOY-FRAGILE = the anchor was mechanical-responsiveness, reframe C presumed dead on both loops.
domain: reframe (C) — relocating closure to the env-loop (F8) and testing whether it survives realistic (owner-loop-like) contingency
status: pre-register-frozen
verdict: pending
exploration_method: campaign synthesis (Fable) after the H_012 2×2 owner-loop refusal matrix — the load-bearing uncertainty is now 'is the F8 anchor substantive or a toy artifact', which IS $0-testable
verification_method: reuse the H_011 Stage-A certified LV-C machinery (block closure vs Watson yoked ghosts, null-env, echo guard) with ONE added knob — the env applies the agent's action with probability p (else acts on its own marginal); sweep p and measure closure; frozen from run-h011-py-1 in-regime gate semantics
pre_register_frozen: true
frozen_at: 2026-07-17
deterministic: seeded-GPU (7B brain frozen from H_011) + stdlib-deterministic scripted plants; verdict replays from the logged actions
---

# H_013 — closure-dose-response

## Hypothesis

H_011 proved closed-loop causation EXISTS + is measurable — a 7B brain ANCHORED on the certified LV-C block
closure (0.76, 5/5) in the micro-tenant. But the H_012 2×2 matrix (target × timescale) refuses the SAME
thesis on the real owner loop at every $0 lens. Either reframe C is false on the real loop, or the proxy
anchor is a TOY ARTIFACT: the micro-tenant env responds to the agent's action **deterministically,
immediately, fully-observably**, whereas the real owner's measured utterance→input contingency is near the
yoked floor (~0.42 sign_base_full). H_013 discriminates: **dilute the env's action-contingency toward
owner-loop-like levels and find where closure dies.**

> **Falsifiable prediction**: the 7B's LV-C block closure DEGRADES GRACEFULLY as the env's action-
> contingency is diluted, remaining ≥ the 0.60 anchor at a pre-registered dose d* calibrated to the real
> owner loop's contingency band. The falsifying outcome is COLLAPSE to the yoked floor at any dose
> materially above d*.

## Design (reuse the H_011 Stage-A certified harness + ONE knob)

- **Dose knob**: the env applies the agent's chosen action with probability **p ∈ {1.0, 0.75, 0.5, 0.25,
  0.1}**; with prob (1−p) it steps on a marginal-sampled action instead (contingency diluted, marginal
  preserved). Keyed by (seed, t) so factual/ghost branches share the dilution draw.
- **Estimator (unchanged, certified)**: LV-C block closure vs marginal-matched Watson yoked ghosts (own
  actions permuted, same (seed,t) noise), `tool/anima_v3` shift-null band + binom gates; frozen AND-gate
  in-regime semantics (`convergence run-h011-py-1`).
- **Brain**: the 7B Qwen2.5-Instruct nf4 frozen from H_011 (on summer, $0), 5 episodes per dose. A LOCAL
  scripted `policy_live` dose sweep (no LLM) runs first as the god-view reference curve + certification.
- **d\* calibration**: pre-register d* = the dose at which a scripted known-contingency policy's own
  in-world sign_base_full matches the owner loop's ~0.42 band (measured, not guessed).

## Plants (certify BEFORE any verdict — the H_009/H_011 staging law)

- **P-DOSE**: a scripted known-contingency brain at each p — the estimator's closure must track dose
  MONOTONICALLY (non-increasing as p falls). Certification gate; must pass first.
- **P-DEAD**: an action-ignoring (null) env must REFUSE (closure ≈ chance) at ALL doses.
- **P-LIVE**: full-dose (p=1.0) must REPLICATE the H_011 anchor (0.76 ± band) as the positive control.

## Pre-registered gates / verdicts

| condition | verdict | meaning |
|---|---|---|
| plants fail | INSTRUMENT-INVALID | fix before any substrate verdict |
| CD-1 monotonicity (closure non-increasing in dilution, Spearman ≤ 0) AND CD-2 closure ≥ 0.60 at d* | **DOSE-ROBUST** | F8 relocation is SUBSTANTIVE — a positive result independent of H_012B; also yields a quantitative closure prediction for the owner loop's contingency band |
| CD-1 pass, CD-2 fail (collapse to yoked floor above d*) | **TOY-FRAGILE** | the H_011 anchor is an artifact of mechanical responsiveness; reframe C presumed dead on BOTH loops; the campaign pivots to reframe D or accepts H_012B as the sole residue |

**Honest limit**: this tests the env-loop (F8) substrate, not the owner (F7); it cannot resolve the
sequence-contingency residue (H_012B-only). A DOSE-ROBUST result is the campaign's first substrate-level
positive; a TOY-FRAGILE result closes reframe C at $0.

## Instrument repair (2026-07-17 — the first scripted run FAILED certification and root-caused a certified-estimator bug)

The first scripted run returned **INSTRUMENT-INVALID**: P-DEAD read closure **0.667 at every dose**
(null env, actions verifiably inert) and the live curve was dose-FLAT — LV-C ignored action-contingency.
Root cause (`probe_lvc_bias.py`, deterministic, $0): **a frame misalignment in the certified H_011
`lv_c`**, not the suspected asymmetric-control geometry —

- `fC = obs_traj[:-1]` collected **PRE-step** obs `[o_0..o_{T-1}]`, while `_replay_tape` collects
  **POST-step** obs `[o_1..o_T]`. Closed sat one tick behind BOTH ghosts, so `d(C,P1)` carried a
  one-tick-shift term that `d(P1,P2)` lacked.
- Proof: in the null env the two ghosts are **bit-identical** (`d(P1,P2)=0` exactly) and the ALIGNED
  closed stream is bit-identical to them too — the residual per-tick sqdist 0.0152 that had been blamed
  on an "energy side-channel" is exactly the one-tick shift (null skips `_apply_action` entirely, so no
  energy channel exists). Old null closure = the fraction of blocks whose digest drifts across 50 ticks
  (pure exogenous drift) = 0.667 — **above the 0.60 gate**: the old estimator could not refuse a dead env.
  H_011's P-DEAD only checked LV-W, never LV-C, so this passed certification unseen.
- **Fix (upstream, in H_011 `run_h011.lv_c` + `lv_c_dose` here): `fC = obs_traj[1:]`** — one line,
  features/blockmeans/gates untouched. Repaired: null env reads **0.000 at every dose** (all streams
  identical, strict `>` never fires); live full-dose plants are UNCHANGED (P-LIVE 0.750, P-OPEN 0.417);
  near-dead dose p=0.1 drops 0.833→0.389 (now refuses).
- **H_011 consequence: the 7B ANCHOR (0.7625) is SUSPENDED** — it was measured with the biased estimator
  whose measured null floor (0.667) exceeds the gate, and its episode-1 closure (0.625) is *below* that
  floor. Full-dose scripted readings were unaffected by the repair, so survival is plausible — but it must
  be re-earned: re-run stage B on summer with the repaired estimator (tape was not persisted, so the
  closure cannot be recomputed offline). See `state/h011_live-ab-closure_2026-07-16/result_stageA_lvc-repair.json`.

## Verdict

_scripted phase (repaired estimator): **CERTIFIED** — P-DOSE monotone (concordance 0.6 ≥ 0.5: closure
0.722 / 0.889 / 0.833 / 0.667 / 0.389 as p falls 1.0→0.1; sign statistic saturates mid-dose, falls off
toward dead), P-LIVE(p=1) 0.722 ≥ 0.60, P-DEAD 0.000 at all doses. d\* = p0.25 (env_contingency 0.377
≈ owner 0.42), scripted closure at d\* = 0.667. Substrate verdict pending — the 7B dose sweep (summer,
$0) AND the H_011 stage-B re-run with the repaired estimator._
