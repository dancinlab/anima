---
id: H_1023
slug: phi-split-substrate-generality
title: Does the redundancy-driven faithful-up / big-Phi-down split generalize beyond the planning-control substrate to a DIFFERENT generative substrate (a trained CLMConvMoE latent, or an unrelated task TPM)?
domain: universe · cwm · consciousness · iit4 · big-phi · faithful-phi · measure-disagreement · substrate-generality · pre-register
source: H_1017 (redundancy explains the split) + H_1020 (mechanism predictor robust n=5) — both measured ONLY on the planning depth-ladder control substrate; cross-substrate generality is untested
exploration_method: E2 (re-run the two-engine + PID protocol on a NEW substrate) + E14 (substrate-native IIT4) + a_scale_honest_scope
verification_method: W2 (pre-registered cross-substrate falsifier · both stdlib engines + WB I_min PID · mirror equivalence-proof) + g5 CODE-measured (no LLM self-judge, p7) + a_phi_iit4_tool
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: measured
measured_at: 2026-06-07
verdict: 🔴 SPLIT-TASK-LOCAL (closed-negative, a_paper_negative_ok)
---

# H_1023 — is the redundancy-split substrate-general?

## 0. motivation
The split + redundancy mechanism (H_1012/1017/1020) were all measured on ONE substrate: the latent
transition structure of the planning-control toy. If the split is a genuine property of the two Phi
measures (not of that one task), an intervention that floods a DIFFERENT substrate with redundant
shared information should also produce faithful-up / big-Phi-down — and the redundancy-margin should
again predict it. Tests whether the finding is about the measures or about the task.

## 1. hypothesis
On a different generative substrate (e.g. the discretized latent of a trained CLMConvMoE, or an
unrelated structured TPM), a redundancy-injecting intervention reproduces the sign-split and the
redundancy-margin again separates split from no-split — the split is substrate-general.

## 2. pre-registered falsifier (frozen 2026-06-07)
Build >=1 NEW substrate (not the planning-control env). Apply a redundancy-raising vs a
synergy-raising intervention; score faithful_phi + big-Phi (matched discretization, mirror-proven)
and the WB I_min redundancy-margin, at $n=4$ (and $n=5$ if tractable).
- PASS = SPLIT-SUBSTRATE-GENERAL : the redundancy-raising intervention reproduces faithful-up /
  big-Phi-down on the new substrate AND the redundancy-margin separates it from the synergy control.
- FAIL = SPLIT-TASK-LOCAL : the split does NOT reproduce off the planning substrate (closed-negative,
  a_paper_negative_ok) — would BOUND the paper to the control task.

## 3. honest scope
Toy $n=4$ (n=5 if tractable), $0 CPU; real IIT4 engines, no proxy (a_phi_iit4_tool). The PID is the
explanatory variable, not a Phi proxy. Substrate choice + intervention construction must be stated
and pre-frozen. Scale-transfer UNVERIFIED (a_scale_honest_scope).

## 4. sibling / xlinks
to [H_1017](./H_1017_split_redundancy_mechanism.md) · [H_1020](./H_1020_redundancy_predictor_robustness.md) · [H_1012](./H_1012_bigphi_faithful_larger_n.md) · PAPER/phi-measure-dependence-planning · a_phi_iit4_tool

## 5. measurement + finding (measured 2026-06-07)

Verdict: **🔴 SPLIT-TASK-LOCAL** (closed-negative, a_paper_negative_ok).
Verbatim raw stdout: [`.verdicts/1023_phi_split_substrate_generality/H_1023.txt`](../.verdicts/1023_phi_split_substrate_generality/H_1023.txt).
Script: [`UNIVERSE/h1023_phi_split_substrate_generality.py`](./h1023_phi_split_substrate_generality.py).

### substrate used (frozen before scoring)
A NEW generative substrate distinct from the planning-control env: a structured
**TPM-driven n=4 binary Markov chain** — no `LatentWorldModel`, no planning rollout.
Bits are produced directly from explicit frozen channel rules, then fed to the SAME
matched binary discretization that drives both engines. Two interventions, each scored
vs the SAME independent-noisy-bits baseline (30 seeds each, matching H_1017):
- **redundancy-raising** = coupled-copy channel (units 1,2,3 = noisy copies of unit 0);
- **synergy-raising** = XOR/parity channel (each unit's next bit = parity of the other three).

Engines re-proven == stdlib at **n=4 AND n=5** (H_1012 `prove_mirrors_at_n`) before scoring;
the Williams-Beer I_min PID re-validated on canonical COPY (red=1.000, syn=0.000) / XOR
(red=0.000, syn=1.000). PID = explanatory variable, not a Phi proxy (a_phi_iit4_tool).

### per-intervention result (30 seeds, matched n=4)
| intervention | faithful_phi Δ (sign) | big-Phi Δ (sign) | SPLIT? | Δredundancy | Δsynergy | margin Δred−Δsyn |
|---|---|---|---|---|---|---|
| redundancy (coupled-copy) | +1.1220 d=+9.65 → RAISES | +0.2606 d=+0.35 p=0.18 → RAISES (NULL) | **False** | +4.4174 | +0.7520 | **+3.6654** |
| synergy (XOR/parity) | +0.0128 → RAISES | +3.2668 d=+3.12 → RAISES | False | +0.0622 | +0.1194 | −0.0572 |

### finding (the ruled-out axis)
The pre-registered split **did NOT reproduce** off the planning substrate. The
redundancy-raising intervention raised faithful_phi strongly (as expected) but big-Phi
did **NOT go down** — it was statistically null/slightly up (+0.26, d=+0.35, p=0.18), so the
required faithful-UP / **big-Phi-DOWN** sign-split is absent. The WB redundancy-margin still
behaves as the H_1017 theory predicts (redundancy arm margin +3.67 ≫ synergy control −0.057,
strict separation), confirming the PID correctly reads the injected redundancy on this
substrate — but the PASS gate requires BOTH the correct split signs AND margin separation,
and the **sign condition fails**. Conversely, the synergy XOR channel *raised* big-Phi
sharply (+3.27), the opposite direction from a redundancy-driven big-Phi drop.

Closed-negative: the faithful-UP / big-Phi-DOWN sign-split is **bounded to the
planning-control task**; it does not transfer to a structured-TPM Markov substrate even
when the WB redundancy-margin is reproduced. This **rules out the substrate-general axis**:
the H_1012..H_1020 sign-split is a joint property of (the two Phi measures × the planning
task's specific structure), NOT of the measures alone. The redundancy-margin (PID) is
substrate-general; the big-Phi-DOWN half of the split is not. BOUNDS
PAPER/phi-measure-dependence-planning to its control substrate.

### honest scope
TOY n=4 (n=5 cross-check on the equivalence proof only); both engines exact; PID exact +
deterministic. Scale-transfer UNVERIFIED (a_scale_honest_scope). g5 CODE-measured
(no LLM self-judge, p7), a_phi_iit4_tool. NOT a forge binary; $0 CPU-local, no GPU.
