---
id: H_1015
slug: human-bar-placement-control
title: On a genuinely world-model-REQUIRING control task (hidden-velocity station-keeping), does anima's closed-loop WM policy land WITHIN-or-ABOVE the pre-registered human band while a reactive baseline lands BELOW — the first falsifiable placement of the CWM north star (not just the instrument)?
domain: cwm · cross-cutting · world-model · human-level · north-star · behavior-eval · placement · control · pre-register
source: CWM milestone M8 (behavior eval vs human baseline — instrument authored H_972, "anima placement downstream" explicitly DEFERRED) + H_964 (world-model-as-policy on hidden-velocity control) + H_970 (WM>LM separator) + a_paper_significance (falsifiable hypothesis + real measurement) + a_scale_honest_scope + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (human-reference task + metric) — reuse the H_972 bar machinery on the H_964 CONTROL task (where reaction provably fails) instead of the saturating delayed-cue task; do the DEFERRED placement step + a_completeness_over_cheap
verification_method: W2 (pre-registered placement falsifier — anima closed-loop WM policy vs a near-optimal-with-lapse human-proxy band on a WM-requiring control task) + g5 CODE-measured (no LLM self-judge, p7)
deterministic: true
cross_process_byte_identical: false
llm: none
hexa_only: false
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: measured
scope: ONE placement rung (a_scale_honest_scope · a_toy_scale_recheck). TOY $0 CPU-local numpy. Task = the H_964 partial-observability control env (agent sees POSITION only, optimal action needs HIDDEN velocity). Human-proxy = a near-optimal oracle policy (knows velocity) with a documented ~7% human attention-lapse rate — the SAME human-proxy construction as the H_972 instrument, transplanted onto the control task. Metric M = mean episode return (0 = optimal station-keeping, more negative = worse). NO live human study. This H does the DEFERRED placement (H_972 authored the instrument, deferred WHERE anima lands); the contribution is the FIRST falsifiable north-star placement on a task that REQUIRES the world model. Single rung; scale-transfer UNVERIFIED. NOT a forge binary; no GPU. No Φ/IIT4 claim here (behavior metric only), so a_phi_iit4_tool is n/a.
sister: H_972 (the bar instrument — delayed-cue, saturates), H_964 (the control task + WAM/reactive/random arms), H_970 (WM>LM), H_990 (closed loop), CWM M8
verdict: 🟢 PASS — north star is a TRUE falsifiable placement on a WM-REQUIRING task. On the H_964 hidden-velocity station-keeping env (position-only obs, optimal action needs hidden velocity), with metric M = mean episode return (0=optimal): human-proxy band [25th,75th pct] = [-1.1633, -1.0633]; random M=-6.1249, REACTIVE (single-frame obs->action) M=-1.9237, anima (WM latent->action) M=-0.6426. D1 band VALID — random CI_hi -5.9883 AND reactive CI_hi -1.8834 BOTH below band_lo -1.1633 (a single-frame reactive policy CANNOT reach the band, so the task genuinely REQUIRES the world model; the placement is non-vacuous). D2 the human-proxy discriminates from random (Welch p 2.2e-45, Cohen d 15.67). D3 anima CI [-0.6575, -0.6282] lands ABOVE the human band (human+). PASS = band valid AND discriminating AND anima WITHIN-or-ABOVE band; here anima is human-level-or-beyond. The reason anima beats the human-proxy: the proxy carries the documented ~7% attention lapse while anima's deterministic WM policy does not lapse — a faithful "above-human-because-no-lapse" reading, NOT a general human-superiority claim. This is the DEFERRED H_972 placement, now done on a hard task. TOY single rung, $0 CPU-local; scale-transfer to richer / embodied environments UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck). g5 CODE-measured (no LLM self-judge, p7). a_phi_iit4_tool n/a (behavior return, no Φ claim).
---

# H_1015 — human-bar PLACEMENT on a world-model-requiring control task

## 0. motivation
CWM milestone M8's instrument (H_972 🟢) proved a falsifiable human-level bar EXISTS and works, but
it explicitly DEFERRED the actual placement of anima ("PASS = the instrument works, NOT a general
'anima is human-level' claim ... anima placement downstream"). Worse, the H_972 instrument used the
delayed-cue MEMORY task where the world model saturates near 1.0 and the band is trivially clean —
so it does not yet TEST the north star on a hard task. The CWM north star is "anima acts in a world
like a human, or beyond." The honest next step (M8) is to do the deferred PLACEMENT on a task that
genuinely REQUIRES the world model — H_964's partial-observability control env, where the agent sees
only POSITION and the optimal action depends on the HIDDEN velocity, so a single-frame reactive
policy provably cannot succeed. This is the first falsifiable measurement of where anima's behavior
lands relative to a human reference on a WM-requiring task.

## 1. hypothesis (one falsifiable claim)
On the H_964 hidden-velocity station-keeping control task, with the metric M = mean episode return
and a pre-registered human band = [25th, 75th pct] of a near-optimal-with-lapse human-proxy, anima's
closed-loop world-model policy (latent -> action) lands WITHIN or ABOVE the human band, while a
single-frame REACTIVE baseline lands BELOW the band and a RANDOM agent is below both — i.e. the north
star "human-level-or-beyond" is, on this WM-requiring task, a TRUE and falsifiable placement (not a
vibe, and not a saturated triviality).

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-07)
**Setup:** H_964 control env (ODIM=2 position-only obs, NACT=4 thrusts, hidden velocity, DRAG=1.0,
reward = -||pos||, horizon T). Train a WM action head (delay-embedding latent -> action, imitation of
the oracle) and a REACTIVE action head (single position -> action, imitation of the oracle), exactly
as H_964. Human-proxy = the ORACLE optimal_action (which knows velocity) executed with a ~7% per-step
attention-lapse (lapse -> random thrust), the SAME lapse construction as the H_972 instrument. N runs
per agent, each run = a batch of episodes; metric M = mean episode return (higher/less-negative is
better; 0 = optimal). Multi-seed, python3 -u, serial, $0 CPU.

Pre-register: human band = [human-proxy 25th pct, 75th pct]. above band = human+; within = human-level;
below = sub-human.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = band validity: REACTIVE and RANDOM agents must land BELOW band_lo (CI_hi < band_lo). If a
  single-frame reactive policy were inside the human band, the task would NOT require a world model
  and the placement would be vacuous.
- D2 = discriminability: the human-proxy must separate from RANDOM (Welch p<0.05, Cohen |d|>=0.8).
- D3 = anima placement: anima (WM) closed-loop policy return CI vs the human band (below/within/above).

**Outcome rules (frozen BEFORE the run):**
- IF the band is valid (D1: reactive AND random below band) AND the human-proxy discriminates from
  random (D2) AND anima's CI lands WITHIN or ABOVE the human band (D3)
  THEN PASS / GREEN = the north star is a TRUE falsifiable placement on a WM-requiring task — anima is
  human-level-or-beyond HERE (toy, single rung; this is the deferred H_972 placement, now done).
- IF the band is valid + discriminating BUT anima lands BELOW the human band (D3 below)
  THEN RED = CLOSED-NEGATIVE (a_paper_negative_ok) — on a genuinely WM-requiring control task anima's
  policy is SUB-human; the north star is falsified HERE and the gap is the quantified finding.
- IF the band is NOT valid (reactive lands inside the band, so the task does not require a WM) OR the
  human-proxy does not discriminate from random THEN FAIL/INCOMPLETE — the placement is vacuous on
  this task (honest, a_scale_honest_scope · C3); re-pick a harder task.

## 3. honest scope
Toy, small scale (a_scale_honest_scope · a_toy_scale_recheck, #123-A n/a — behavior metric, not
entropy-quality). Human reference = a documented near-optimal-with-lapse proxy, NOT a live IRB human
study; the ~7% lapse is the H_972 construction transplanted. The control env is the H_964 toy; the bar
is one defensible operationalization. Single rung; scale-transfer to richer environments / real
embodiment UNVERIFIED. No Φ/IIT4 claim here (a_phi_iit4_tool n/a — behavior return only). NOT a forge
binary; $0 CPU-local, no GPU.

## 4. measurement + finding (2026-06-07 · 🟢 PASS · g5 CODE-measured · substrate=CPU-mirror numpy · $0)
Probe: `CWM/probes/h1015_human_bar_placement.py` · verdict: `.verdicts/1015_human_bar_placement_control/H_1015.txt`

Task = H_964 hidden-velocity station-keeping (position-only obs); metric M = mean episode return
(0 = optimal). 40 runs × 60 episodes per agent; human-proxy lapse = 0.07 (same as H_972).

| agent | M (mean ± std) |
|---|---|
| human-proxy (reference) | -1.1098 ± 0.0899 → band [-1.1633, -1.0633] |
| random | -6.1249 ± 0.4377 |
| reactive (single-frame obs→action) | -1.9237 ± 0.1320 |
| anima (WM latent→action) | **-0.6426 ± 0.0463** |

- **D1 band validity ✓** — random CI_hi -5.9883 AND reactive CI_hi -1.8834 BOTH below band_lo -1.1633.
  Crucially the REACTIVE single-frame policy cannot reach the band: the task genuinely REQUIRES the
  world model (hidden velocity is unrecoverable from one frame), so the placement is NON-vacuous —
  exactly the gap H_972's saturating delayed-cue task could not exercise.
- **D2 discriminability ✓** — human-proxy vs random Welch t 70.1, p 2.2e-45, Cohen d 15.67.
- **D3 anima placement ✓** — anima CI [-0.6575, -0.6282] lands ABOVE the human band (human+).

**Finding (🟢 PASS):** the CWM north star "human-level-or-beyond" is, for the first time, a TRUE and
falsifiable PLACEMENT on a task that genuinely requires the world model — not just an instrument
(H_972) and not a saturated triviality. anima's closed-loop WM policy lands ABOVE the human band while
the reactive baseline lands BELOW it, proving (a) the task needs the world model and (b) anima clears
the human bar HERE. Honest mechanism: anima beats the human-proxy because the proxy carries the
documented ~7% attention lapse while anima's deterministic WM policy does not — an "above-human-
because-no-lapse" reading, NOT a general claim that anima exceeds humans. This completes the DEFERRED
H_972 placement step of CWM M8. TOY single rung, $0 CPU-local; scale-transfer to richer / embodied
environments UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck). Ladder OPEN.

## 5. sibling / xlinks
- ⇄ [H_972](./H_972_human_level_or_beyond_bar.md) (the bar instrument — saturating delayed-cue task)
- ⇄ [H_964](./H_964_latent_to_action_policy.md) (the WM-requiring control task + WAM/reactive/random)
- ⇄ [H_970](./H_970_world_model_vs_language_model_decisive_test.md) (WM>LM separator)
- ⇄ [CWM](../CWM/CWM.md) (CWM-VERIFY · north star · M8)
