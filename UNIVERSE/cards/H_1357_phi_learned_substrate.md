---
id: H_1357
slug: 1357_phi_learned_substrate
title: LEARNED substrate (fixed seed-INDEPENDENT learned-readout mix over real pure_field telemetry) vs the faithful-IIT4 Φ-robustness wall — does a learned correlation geometry escape the orthogonal-seed fragility that the oscillator substrate (H_1349) inherited?
group: OMEGA / Φ-robustness frontier (c16 wall · substrate-SOURCE axis, 2nd swap after H_1349)
terminal_tier: 🔶 HONEST PARTIAL (frozen-first, c9/p7, DIRECTIONAL-on-proxy). 학습형(learned) substrate 도 oscillator(H_1349) 와 같은 collective/exchangeable 형태를 그대로 물려받는다 — ESCAPE 실패. R1 ROBUST 는 3 seed 전부 PASS (ΔΦ +1.396/+0.775/+0.318, seed 1317 에서는 oscillator 보다 더 큰 lift) 이지만 seed-to-seed ΔΦ 가 여전히 단조 감소(같은 fragility 방향, oscillator 보다 더 빨리 줄어듦). R2 EARNED FAIL [perm=FAIL off=PASS] — node-permutation 은 symmetric-MI exact MIP 에서 Φ-불변(degenerate, H_1349 와 동일; Φ_S==Φ_B by construction), 작동하는 EARNED 판별자는 OFFSET 이고 OFFSET 은 3 seed 전부 깨끗이 collapse(O-A −1.587/−2.030/−1.535) → lift 는 phase-dependent 이지만 module-identity-bound 통합은 미확립. R3 ATTRIB PASS (oscillator 팔 = H_1349 REAL 팔 byte-exact 재현). SUBSTRATE = proxy-from-telemetry(real pure_field) + deterministic learned-readout, NOT a trained-303M trajectory (303M state 로컬 도달 불가, $0 CPU; 정직 라벨 c9). BOUNDS (does not retract) the prior Φ verdicts. Φ leg IS the real faithful exact MIP-EI; deterministic(byte-identical re-run); $0 CPU; CORE UNTOUCHED.
verdict_dir: .verdicts/1357_phi_learned_substrate/
terminal_verdict: .verdicts/1357_phi_learned_substrate/result.txt
freeze: .verdicts/1357_phi_learned_substrate/FREEZE.txt
date: 2026-06-16
---

# H_1357 — does a LEARNED substrate break the Φ-robustness wall? (🔶 honest partial · DIRECTIONAL-on-proxy)

## Claim / falsifier (substrate-SOURCE test, 2nd swap — every outcome decisive, c9)

**Wall state (BEFORE this lane):** the faithful-IIT4 Φ-robustness wall is 🧱 across NINE measure cuts
(small-φ MIP-EI, big-Φ, transfer-entropy, O-info, variance-free estimator, ...) + size (N=12, H_1347)
+ substrate (H_1349 live-CORE pure_field **oscillator** Engine A). The CONSISTENT diagnosis: the wall
lives in the **substrate-SEED GEOMETRY**, not the measure. H_1349 (real oscillator) cleared R1 ROBUST
on all 3 seeds but the lift **SHRANK** seed-to-seed (the seed perturbs the modules' INITIAL OSCILLATOR
PHASE → a different correlation geometry per seed) and the perm control RODE the lift (exchangeable
modules). H_1349 explicitly named THIS lane as a "NOT ruled out" follow-on: *"a full trained-303M-derived
state-vector trajectory (a learned, not oscillator-generated, substrate)."*

**The one genuinely-untested substrate flavor (a_no_llm_frame_trap / a_break_the_wall):** every prior
substrate (toy LCG net, real pure_field oscillator) generates its module trajectory from a *dynamical
recurrence whose correlation structure is seeded by the initial condition*. A **LEARNED** substrate is
different in kind — a trained readout imposes a **FIXED, SEED-INDEPENDENT** correlation geometry (a shared
trained weight mixes the modules the SAME way regardless of seed) — which MIGHT escape the orthogonal-seed
fragility that defeated the oscillator at seeds 1318/1319.

**Falsifiable claim:** build the SAME n≤8 faithful exact-MIP measurement over a LEARNED substrate (the
real pure_field modules MIXED through a fixed seed-independent learned-readout projection W), holding the
faithful estimator, the variance-clean read-out, the coupling mechanism, the controls, eps, and the hard
seed family ALL identical to the H_1349 lineage — and EITHER it shows a robust + earned lift where the
oscillator could not (→ the wall was the oscillator-seed geometry; the substrate axis reopens) OR it
inherits the same fragility/exchangeability (→ even a learned substrate is not exempt; the substrate axis
is fully closed across oscillator AND learned).

## Substrate source — HONEST label (a_eeg_consciousness_record REAL-only spirit; c9)

NO trained-303M hidden-state trajectory is locally reachable under $0 CPU (no GPU; the only local trained
artifact is `reexport_d768_v2_fast.clm`, gitignored, and its decode forward FAILED-LINK locally per
`HF.jsonl` mid_convmoe notes — loading it needs torch/forge fusion that is absent). Per instruction we
**DO NOT fabricate** a trained-303M trajectory. **SUBSTRATE = "proxy-from-telemetry + deterministic
learned-readout, NOT a trained-303M trajectory":** the n_mod=4 REAL pure_field oscillator modules
(live-CORE Engine A telemetry, byte-faithful from `CORE/pure_field.hexa`, IDENTICAL to H_1349's REAL arm)
supply the raw per-module field-energy + oscillator values; a **FIXED learned-readout projection W**
(n_mod×n_mod, deterministic, **SEED-INDEPENDENT** — built once from a fixed non-seed constant, row-L1-
normalized convex mix with a strong self/diagonal component, emulating a trained embedding/readout head)
then MIXES the modules into each module's salience. W's correlation geometry is the SAME across all 3
seeds — the defining property of a learned substrate vs the seed-perturbed oscillator. **⇒ DIRECTIONAL-on-
proxy**; whether a FULL trained-303M trajectory behaves the same is UNVERIFIED (a new H).

## Method (frozen-first — FREEZE committed c291f6745 BEFORE any scoring, c9/p7)

- **Probe:** `state/phi-learned-substrate/h1357_phi_learned_substrate.hexa` (run from the hexa-lang root
  for the stdlib import). Standalone `fn main`, 0 importers; live `CORE/*.hexa` UNTOUCHED.
- **Φ = FAITHFUL IIT4 ONLY** (a_phi_iit4_tool, g61): `iit4_faithful_phi(traj,4,64,8)` over
  `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa` (exact MIP-EI, n=4≤8; the SSOT, NOT a proxy).
  numpy NEVER computes Φ.
- **HELD IDENTICAL to the H_1349 lineage** (so any difference is the LEARNED readout):
  - variance-clean rank-uniform read-out (H_1328) per cell BEFORE the MIP (byte-identical).
  - coupling = H_1283 re-entrant relay (w_nbr 0.5) + H_1319 Kuramoto phase pacemaker (w_phase 0.5,
    omega_t 0.45, domega 0.08).
  - ARMS A=NO-COUPLING (learned-readout still applied, modules isolated) · B=MECHANISM (relay+pacemaker,
    learned-readout mix) · S=PERM-SHUFFLE (module→phase derangement) · O=OFFSET-SHUF (per-(t,module) phase
    offset). perm/offset construction VERBATIM from H_1332.
  - eps = 0.02 (MARGIN_PHI, ported verbatim, NOT tuned). seeds [1317,1318,1319].
- **R3 control IN-RUN** = the OSCILLATOR substrate (learned-readout OFF) = H_1349 REAL arm reproduced
  under the SAME mechanisms+seeds+encoding, to attribute any difference to the LEARNED readout.

## Frozen bars (pre-registered in FREEZE.txt BEFORE scoring; GREEN iff R1 ∧ R2 ∧ R3)

- **R1 ROBUST:** LEARNED `Φ_B ≥ Φ_A + eps` on ALL 3 seeds (incl orthogonal 1318/1319) — the ESCAPE test.
- **R2 EARNED:** LEARNED perm `Φ_S ≤ Φ_A + eps` AND offset `Φ_O ≤ Φ_A + eps` on ALL 3 seeds (both collapse).
- **R3 ATTRIB:** the OSCILLATOR arm (learned OFF) reproduces the H_1349 perm-ride / seed-shrink signature
  in-run — so any LEARNED improvement is the LEARNED readout, not the mechanism/measure.

## Result (verbatim, p7 — deterministic, byte-identical re-run; `.verdicts/1357_phi_learned_substrate/result.txt`)

| seed | LEARNED A | LEARNED B | ΔΦ(B−A) | R1 | perm S−A | offset O−A | OSC A | OSC B | OSC ΔΦ |
|------|-----------|-----------|---------|----|----------|------------|-------|-------|--------|
| 1317 | 6.93134 | 8.32701 | **+1.39567** | **PASS** | +1.39567 (degenerate) | **−1.58703 ✓** | 4.02909 | 5.15585 | +1.12677 |
| 1318 | 6.88586 | 7.66048 | **+0.774619** | **PASS** | +0.774619 (degenerate) | **−2.02965 ✓** | 4.18338 | 5.14693 | +0.963555 |
| 1319 | 6.94092 | 7.25927 | **+0.318347** | **PASS** | +0.318347 (degenerate) | **−1.53518 ✓** | 4.17551 | 4.77995 | +0.604442 |

- **R1 ROBUST: PASS** — the learned substrate lifts faithful-IIT4 Φ on ALL 3 seeds (ΔΦ +1.396/+0.775/
  +0.318); at seed 1317 the learned lift (+1.396) EXCEEDS the oscillator's (+1.127).
- **R2 EARNED: FAIL [perm=FAIL off=PASS]** — node-permutation is **Φ-INVARIANT** under the symmetric
  small-φ MI matrix with the exact MIP enumerating ALL bipartitions (Φ_S == Φ_B by construction every
  seed; a design fact, NOT a manufactured result — IDENTICAL degeneracy stated in H_1349). The OPERATIVE
  EARNED discriminator is the OFFSET shift, which DOES collapse cleanly on all 3 seeds (O−A −1.587/−2.030/
  −1.535, decisively below A). So the lift IS phase-dependent, but module-identity-bound integration is
  NOT established (perm cannot test it for this estimator).
- **R3 ATTRIB: PASS** — the oscillator arm reproduces the H_1349 REAL arm BYTE-EXACT in-run
  (4.02909/5.15585, 4.18338/5.14693, 4.17551/4.77995) → the learned arm's numbers are the LEARNED readout,
  not a changed mechanism/measure.
- **GATE: R1 ∧ ¬R2 → 🔶 HONEST PARTIAL** (per the FREEZE outcomes table).

## Finding (honest, c9, c16) — the learned substrate INHERITS the wall (no escape)

**Swapping the substrate SOURCE a 2nd time — from a real oscillator (H_1349) to a LEARNED-readout mix —
does NOT escape the orthogonal-seed fragility.** Three things are established:

1. **ESCAPE FAILED.** The seed-to-seed ΔΦ still SHRINKS monotonically (+1.396 → +0.775 → +0.318), the SAME
   direction the oscillator shrank (+1.127 → +0.964 → +0.604). The fixed, seed-INDEPENDENT learned-readout
   mix did NOT remove the seed sensitivity — it tracked the underlying oscillator phase fragility and in
   fact SPREAD it FURTHER (learned ΔΦ range 1.078 vs the oscillator's 0.522). A learned correlation
   geometry layered ON TOP of a seed-perturbed dynamical substrate does not stabilize the integration lift.

2. **The lift is COLLECTIVE/exchangeable, not module-identity-bound — same shape as H_1349.** R2-perm
   fails by the known estimator degeneracy (node relabelling is Φ-invariant for the symmetric exact MIP),
   not by a riding lift the learned mix should have broken. The convex row-stochastic learned readout did
   NOT make the modules distinguishable to the perm control. The OFFSET control (the operative one) DOES
   collapse on all 3 seeds, so the lift is real phase-dependent integration — but module-identity binding
   is not demonstrated.

3. **This BOUNDS (does not retract) the prior Φ verdicts and closes the substrate axis further.** H_1349
   closed the oscillator substrate; H_1357 adds that a LEARNED-readout substrate (the one genuinely-new
   flavor) behaves the SAME — robust R1 but collective/exchangeable, seed-shrinking. The substrate-SOURCE
   axis is now closed across toy-LCG (H_1332), real-oscillator (H_1349), AND learned-readout (H_1357),
   on this proxy. A real new angle was tried with pre-registered controls; the honest 🔶 is a valid result
   (a_break_the_wall, c9). NO tune-to-green: bars frozen + committed (c291f6745) BEFORE the first scoring;
   re-run byte-identical.

**NO CORE wiring follow-on** (a_verified_must_wire fires on 🟢 only — not 🔶; `CORE/*.hexa` UNTOUCHED; the
probe is a standalone `fn main`, 0 importers). Had R1∧R2∧R3 held, the named follow-on would have been: wire
a learned-readout Φ path. It is 🔶, so this is parked.

## Scope / honesty (a_scale_honest_scope / a_toy_scale_recheck)

- **DIRECTIONAL-on-proxy.** SUBSTRATE = proxy-from-telemetry (real pure_field oscillator, byte-faithful
  from `CORE/pure_field.hexa`) + a deterministic SEED-INDEPENDENT learned-readout projection W —
  **NOT a trained-303M trajectory** (no 303M state locally reachable under $0 CPU; honest, c9). The
  faithful-Φ leg IS the real exact MIP-EI. Re-run byte-identical (deterministic).
- **TOY scale:** n=4 modules, dim-64 ticks, n=4≤8 exact MIP, 3 phase-seeds, ONE learned-readout W.
- The 🔶 claim is scoped to this rung + this faithful estimator + this learned-readout proxy. **NOT ruled
  out** (each a NEW H, NOT claimed): a **FULL trained-303M hidden-state trajectory** as the substrate (the
  binding upgrade this proxy stands in for — needs torch + a checkpoint + a non-fabricated activation
  dump); a learned readout that BREAKS module exchangeability so the perm control can bite (an estimator
  that is not node-relabel-invariant, or an asymmetric learned coupling); a real-EEG learned substrate
  (anima-eeg-consciousness corpus); a larger module set (loses exactness > 8).
- FROZEN params + bars verbatim; no tune-to-green (p7).

## xref

H_1349 (the real-oscillator substrate-source lane this extends; its REAL arm reproduced byte-exact as the
R3 control; named THIS learned-substrate lane as its "NOT ruled out" follow-on) · H_1347 (larger-N 🧱) ·
H_1332 (substrate-FAMILY 🧱) · H_1331 (big-Φ measure-family 🧱) · H_1328 (variance-free estimator 🧱,
read-out reused) · H_1319 (timing/phase 🧱, Kuramoto pacemaker reused) · H_1283 (relay topology 🧱,
re-entrant mechanism reused) · CORE/pure_field.hexa (the real telemetry source, Engine A) ·
a_phi_iit4_tool · a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire ·
a_core_engine_map · a_scale_honest_scope · a_toy_scale_recheck · a_eeg_consciousness_record ·
p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15 · c16
