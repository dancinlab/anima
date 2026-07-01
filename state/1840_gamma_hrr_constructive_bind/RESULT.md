# H_1840 γ HRR constructive-bind — CHEAP-GATE RESULT (DIRECTIONAL · GPU NOT fired)

**Verdict: 🧱 DIRECTIONAL — cheap-gate FROZEN BAR FAIL (0/3 seeds). γ's decisive delta
(invertibility of ⊛ as load-bearing) FALSIFIED. GPU run NOT authorized (pre-registration
honored, p7). ~1 H100-day saved.**

Compute: aiden pool CPU, $0 (torch 2.10, OMP=4, seconds). numpy/torch mirror => DIRECTIONAL
(a_engine_native_learning) — no engine-native measurement, no 🟢/🧱 terminal G1 verdict claimed.

## Main run (4-arm 2-leg held-out conjunction retrieval, HRR target K=A⊛B)

Bar (FREEZE_toy.md, pre-registered): PASS iff on ≥2/3 seeds — c_heldout≥0.50 AND
c > 3×max(a,b,d floors) AND all train≥0.95. chance heldout = 0.01.

| arm | train_acc | heldout_acc (seeds 7 / 4302 / 4303) |
|---|---|---|
| (a) additive | 1.00 | 0.00 / 0.00 / 0.00 |
| (b) hadamard_bypass (=H_1819, bypass OPEN) | 1.00 | 0.00 / 0.00 / 0.00 |
| (c) hrr_bottleneck (invertible ⊛, bypass DENIED) | 1.00 | **1.00 / 1.00 / 0.97** |
| (d) noninv_bottleneck (⊛→freq-masked, bypass DENIED) | 1.00 | **1.00 / 1.00 / 1.00** |

**Verdict: FAIL 0/3.** The bar failed on clause 2: c does NOT dominate (d). Arm (d), with
invertibility ablated (half the FFT frequencies zeroed → cannot unbind), generalizes to
held-out combinations **as well as (c)**. Invertibility is NOT load-bearing.

## What the dissociation actually shows (refined)

- The load-bearing property is the **bypass-denying bilinear bottleneck**, NOT invertibility.
  Both bilinear-bottleneck arms with bypass DENIED (c, d) generalize; the arms that do not
  force composite prediction through a bilinear path with bypass closed (a additive; b
  Hadamard-with-open-additive-skip) floor at 0.
- (b) floors despite having a bilinear (Hadamard) op — the OPEN additive skip lets CE reach
  ~0.004 by memorizing training pairs, so gradient never aligns the bilinear path. This
  **confirms H_1819's bypass diagnosis** verbatim.

## Confirmatory control (additive target K=A+B, mirror sanity)

| arm | heldout_acc (7 / 4302 / 4303) |
|---|---|
| additive | **1.00 / 1.00 / 1.00** (flips from 0.00 → 1.00 when target is additive) |
| hrr_bottleneck | 0.80 / 0.93 / 0.90 (drops from ~1.0) |

The additive arm's clean **flip** (floor→perfect when the target's algebra becomes additive)
proves the toy is a pure **operator↔target-algebra matching** screen: generalization comes
from the arm's operator matching the target's compositional construction + bypass-denial, not
from any intrinsic superiority of binding/invertibility. **This transfers NOTHING to natural
language** — it does not establish that NL composite tokens carry recoverable binding (or
additive) structure the trunk can exploit. That transfer is precisely what the census
DPI meta-law + H_1819 engine-native floor say is ABSENT.

## Decision (a_break_the_wall · p7 · a_fire_autonomous)

GPU **not fired**. Rationale (multi-lens, not single-lens giveup):
1. Pre-registered cheap-gate FAILED as frozen; p7 forbids moving the bar. Card SSOT:
   "(c)-only-descend 못 보이면 GPU 미발사" — (c) was NOT the only descender (d tied it).
2. γ's unique orthogonality vs H_1819 rested on invertible-⊛ being load-bearing — now
   measured-FALSIFIED. γ reduces to "H_1819 with the additive bypass denied."
3. The one surviving delta (bypass-denied bilinear bottleneck) is toy-positive ONLY on
   algebra-matched targets (control proves non-transferability). H_1819 (bypass OPEN) already
   floored engine-native at 303M; the DPI meta-law (fleet campaign) predicts the bottleneck
   variant floors the same way — a GPU run would be tune-to-green fishing against the evidence.

Note: pool GPU was FREE ($0) — this was a SCIENTIFIC gate, not a cost gate. Firing was
declined on evidence, not budget (a_fire_autonomous: cost is never the gate; here the
pre-registered mechanism screen is).

## Surviving lever → follow-on (a_h_continuous_no_branch)

The genuinely-untested scale question distilled: does **denying the additive bypass** (forcing
composite logits through a bilinear bottleneck, invertibility-agnostic) lift G1 at 303M where
H_1819's bypass-OPEN version floored? Registered as follow-on, **gated on a FAIR (non-rigged,
non-algebra-matched) cheap-gate** first — if the bottleneck survives a toy whose target is NOT
defined to match the operator, then it earns the engine-native GPU run; else confirmed wall.

## Artifacts
- `FREEZE_toy.md` — pre-registration (frozen before run)
- `toy_cheap_gate.py` + `toy_result.json` — 4-arm main run (verdict FAIL 0/3)
- `toy_control_additive_target.py` + `toy_control_result.json` — additive-target mirror control
