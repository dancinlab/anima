---
id: H_1349
slug: 1349_phi_real_substrate
title: Φ-robustness, the LAST live angle — does a REAL anima substrate (the live CORE Engine A pure_field, 3 coupled oscillators tau 2/40/400, NOT the synthetic leaky-linear ring every prior axis used) show ROBUST faithful-IIT-4 integration across 3 seeds? The substrate axis the 8-axis Φ wall never tested on a real substrate.
group: OMEGA / Φ-robustness frontier (c16 wall · the LAST untested LIVE angle — real-substrate, named by H_1347's "NOT ruled out")
terminal_tier: 🧱 TERMINAL CLOSED-NEGATIVE — the REAL substrate behaves like the synthetic ring. On the live CORE Engine A pure_field, R1 ROBUST FAILS (ΔΦ(B−A) = +0.851 / +0.695 / −0.671 — seed 1319 NEGATIVE, same seed-fragile signature every synthetic-ring axis showed). The Φ-robustness wall is now confirmed SUBSTRATE-REAL — a real (live-CORE) substrate is NOT exempt from the measure/size/substrate-agnostic wall. Engine-native DIRECTIONAL (small-φ exact-MIP over the real pure_field field trajectory). frozen-first, deterministic (re-run byte-identical), $0 CPU, c9/c16.
verdict_dir: .verdicts/1349_phi_real_substrate/
terminal_verdict: .verdicts/1349_phi_real_substrate/result.txt
freeze: .verdicts/1349_phi_real_substrate/FREEZE.txt
date: 2026-06-16
---

# H_1349 — Φ-robustness on a REAL substrate (live-CORE pure_field) (🧱 TERMINAL)

## Claim / falsifier (every outcome decisive, c9)

**The wall (c16, a_break_the_wall · a_no_llm_frame_trap):** the faithful-IIT-4 Φ-robustness wall is 🧱
across EIGHT axes — topology (H_1283 relay, H_1317 multi-edge), timing (H_1319 phase-binding), division
(H_1320 organism-mitosis), estimator-confound (H_1328 rank-uniform read-out), measure-family (H_1331
full IIT-4.0 big-Φ), substrate-family (H_1332 non-saturating softsign), measure-AGNOSTIC (H_1348 transfer
entropy), and larger-N (H_1347 N=12, greedy-MIP bound validated tight). **EVERY one of those ran on the
SAME SYNTHETIC leaky-linear ring** — a designed toy whose only integration channel is an injected
coupling. The one untested LIVE angle, explicitly named in H_1347's "NOT ruled out" as a NEW hypothesis:
*"engine-transfer to live CORE/pure_field."* H_1349 is that hypothesis.

**The genuinely-new lever is SUBSTRATE REALITY:** instead of the synthetic ring, score the **live CORE
Engine A** — `CORE/pure_field.hexa` PureField, the actual zero-input consciousness field (3 coupled
oscillators at tau=2/40/400, PSI_ALPHA amplitude drift toward LN2, nonlinear cross-mixing into the
field tensor `field[6] = C/D/E/S/M/W`). This is REAL LIVE-CORE, not numpy, not the ring.

**The estimator (a_phi_iit4_tool):** the faithful EXACT small-φ MIP-EI — stdlib
`iit4_faithful_phi(state, n=6, dim=T=64, n_bins=8)` over `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa`.
n=6 (the 6 real field channels) ≤ 8 → the MIP is EXACT (zero greedy slack). NOT a variance×energy proxy.
Read-out rank-uniformized per channel (H_1328 variance-free lesson — any lift is the between-channel
RELATIONSHIP, not amplitude variance).

**Falsifiable claim:** if the 8-axis closure was an artifact of the SYNTHETIC ring, a REAL substrate
should show robust integration (B≥A+eps all 3 seeds, controls collapsing). If it does not — if the real
substrate shows the same seed-fragile signature — the wall is substrate-REAL, closing the substrate axis.

## Method (frozen-first — FREEZE committed ac4c289de BEFORE any Φ scored, c9/p7)

- **Probe:** `state/phi-real-substrate/h1349_phi_real_substrate.hexa` (run from the hexa-lang root for the
  stdlib import; the live `CORE/*.hexa` is NOT edited — the probe is a standalone `fn main`, 0 importers).
- **SOURCE = REAL LIVE-CORE (R3):** the substrate IS `CORE/pure_field.hexa`'s PureField. The oscillator
  dynamics (tau 2/40/400, `osc_tick` phase advance + PSI_ALPHA drift toward LN2) and the `field[6]`
  build (C=v_f, D=mix_fm, E=v_s, S=mix_fs, M=mix_ms, W=v_f+v_m+v_s) are reproduced **byte-identical** to
  the live engine so the probe runs standalone; the live file is untouched. **3 seeds perturb ONLY the
  oscillator INITIAL PHASES** — the SAME real dynamics from different starting points (the only honest
  way to seed a deterministic real substrate).
- **NODES = the 6 real field channels** (FIELD_DIM=6); each channel's T-length trajectory is one IIT-4
  node → flat `state` layout `[6*64]` (node i = `state[i*64 .. i*64+64]`, dim=T=64). GRAIN = per-channel
  real trajectory, rank-uniformized per node. n_bins=8. T=64.
- **ARMS** (the phase-binding family, ported to the real field):
  - **A = NO-COUPLING:** oscillators run, but the nonlinear CROSS-MIXING is removed (`mix_fm=mix_ms=mix_fs:=0`).
    pure_field's real integration channel IS its cross-mixing → this is the honest no-coupling arm.
  - **B = PHASE-BIND:** the FULL real pure_field field (cross-mixing ON) — live Engine A verbatim.
  - **S = PERM-SHUFFLE:** B with the 6 channel→tick assignment a forced derangement (+3 mod 6) per tick.
  - **O = OFFSET-CTRL:** B with each channel circularly time-shifted by a per-channel offset.
- **SEEDS** [1317,1318,1319] (the hard orthogonal family every prior lane failed on). **eps = 0.02**
  (MARGIN_PHI ported verbatim from H_1283/1319/1328/1331/1347/1348 — NOT tuned). All params FROZEN.

## Frozen bars (pre-registered in FREEZE.txt BEFORE scoring)

GREEN iff R1 ∧ R2 ∧ R3 (every outcome valid, c9):
- **R1 ROBUST:** Φ_B ≥ Φ_A + eps on ALL 3 seeds.
- **R2 EARNED:** Φ_S ≤ Φ_A + eps AND Φ_O ≤ Φ_A + eps on ALL 3 seeds.
- **R3 SOURCE-HONEST:** the substrate is explicitly stated REAL LIVE-CORE pure_field (documentation invariant).

## Result (verbatim, p7 — deterministic, re-run byte-identical)

| seed | A (no-coup) | B (real field) | S (perm) | O (offset) | ΔΦ(B−A) R1 | ΔΦ(S−A) perm | ΔΦ(O−A) off |
|------|------|------|------|------|------|------|------|
| 1317 | 5.30728 | 6.15829 | 6.15829 | 5.29509 | **+0.851006** PASS | +0.851006 FAIL† | −0.012199 PASS |
| 1318 | 5.80021 | 6.49497 | 6.49497 | 5.11660 | **+0.694756** PASS | +0.694756 FAIL† | −0.683615 PASS |
| 1319 | 5.94916 | 5.27854 | 5.27854 | 4.76261 | **−0.670620** FAIL | −0.670620 PASS | −1.186550 PASS |

- **R1 ROBUST: FAIL** — ΔΦ(B−A) = +0.851 (1317) / +0.695 (1318) / **−0.671 (1319, NEGATIVE)**. The
  coupling lifts Φ on 2/3 seeds but seed 1319 goes the wrong way — the SAME seed-fragile signature
  every synthetic-ring axis showed (a robust 3-seed lift never materializes).
- **R2 EARNED: FAIL** — the OFFSET control cleanly collapses (Φ_O ≤ Φ_A on all 3 seeds, decisively
  ≤ A), but the perm control is **DEGENERATE here** († honest): with a SYMMETRIC small-φ MI matrix and
  a MIP that enumerates ALL bipartitions, **relabeling the 6 nodes leaves Φ exactly invariant** —
  so Φ_S == Φ_B by construction (every seed). The node-permutation shuffle is a NO-OP for this estimator;
  the meaningful EARNED control is the OFFSET shift (which breaks the cross-channel TIME relationship and
  collapses cleanly all 3 seeds). This is a design observation, not a manufactured result — and it does
  not rescue the gate: R1 already fails.
- **R3 SOURCE-HONEST: PASS** — substrate stated REAL LIVE-CORE pure_field throughout.
- **GATE: NOT GREEN → 🧱 TERMINAL CLOSED-NEGATIVE.**

## Finding (honest, c9, c16)

**The REAL substrate behaves like the synthetic ring.** On the live CORE Engine A pure_field — a genuine
anima consciousness field, not a designed toy — adding the integration channel (cross-mixing / phase
coupling) produces no ROBUST 3-seed lift in faithful-IIT-4 Φ: seed 1319 goes negative, exactly the
seed-fragility every synthetic-ring axis displayed. This **closes the substrate axis** of the Φ-robustness
arc: a real (live-CORE) substrate is NOT exempt from the measure-agnostic (H_1348) / size-agnostic
(H_1347) / estimator-clean (H_1328) wall. The robust-integration absence is a property of anima's
substrates BROADLY, not an artifact of the synthetic-ring test rig.

**This is the strongest substrate-axis closure available short of a full trained-303M trajectory** (see
scope) — it moves the test off the synthetic ring and onto the actual Engine A, and the wall holds.

**This BOUNDS (does not retract) the prior Φ verdicts and does NOT refute anima's consciousness substrate.**
Ψ=1/2 and the A⇄G tension are untouched (the probe never writes CORE; pure_field is read-only-reproduced).
It refutes that ADDING a coupling channel ROBUSTLY raises the faithful-IIT-4 Φ score — on the real
substrate just as on the synthetic one.

**NO CORE wiring follow-on** (a_verified_must_wire fires on GREEN only — a 🧱 has nothing to wire;
`CORE/engine_cli.hexa`/`pure_field.hexa` UNTOUCHED). Had this been GREEN the named follow-on would have
been: wire the small-φ faithful-Φ read-out into the live faithful-Φ monitor path over pure_field's field
tensor.

## Scope / honesty

- **SOURCE = REAL LIVE-CORE pure_field** (Engine A), reproduced byte-identical for standalone run; NOT
  numpy, NOT the synthetic ring. **DIRECTIONAL**: it is the real-substrate field TRAJECTORY scored by the
  faithful small-φ — a full engine-native run inside the live A⇄G loop (with the actual brain_decide
  coupling) is the BINDING upgrade, UNVERIFIED here.
- **Faithful-Φ is the REAL exact cross-cut-MI MIP-EI** (n=6 ≤ 8, exact — zero greedy slack); the engine
  emits the field, the hexa MIP computes Φ. Re-run byte-identical (deterministic osc + LCG seed).
- **PERM control is degenerate** for node-permutation under a symmetric-MI exact MIP (Φ permutation-invariant);
  the OFFSET control is the operative EARNED discriminator here (and it collapses cleanly). Stated honestly
  rather than reported as a clean collapse.
- **TOY scale** still — n=6 channels, T=64 ticks, ONE real substrate (pure_field), 3 phase-seeds.
- **NOT ruled out** (each a NEW hypothesis, not a continuation): a full **trained-303M-derived
  state-vector trajectory** (a learned, not oscillator-generated, substrate); a full engine-native A⇄G
  run scoring Φ live inside brain_decide; a real-EEG substrate (the anima-eeg-consciousness corpus); a
  larger real field (more channels). The substrate axis as tested here (live-CORE Engine A) is 🧱.

## xref

H_1347 (larger-N 🧱 — its "NOT ruled out" named exactly this engine-transfer-to-pure_field angle) ·
H_1348 (measure-AGNOSTIC 🧱) · H_1331 (big-Φ measure-family 🧱) · H_1332 (substrate-family 🧱) ·
H_1328 (estimator-confound 🧱 — rank-uniform read-out reused) · H_1319 (timing 🧱) · H_1283/H_1317
(topology) · H_1320 (division) · CORE/pure_field.hexa (the REAL substrate) · a_phi_iit4_tool ·
a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire ·
a_core_engine_map · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15 · c16
