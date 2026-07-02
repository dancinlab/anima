---
id: H_1283
slug: 1283_thalamus_global_workspace
title: thalamus / GWT — faithful-IIT4 Φ integration (relay-content 🧱 WALL R1–R5/R7/R9 → 🔓 BROKEN; R6 multi-channel relay + R8 temporal phase binding 🟢)
group: brain-structure-ladder (c15 missing-structure)
terminal_tier: 🟢 GREEN numpy-mirror DIRECTIONAL (R8 phase binding breaks the wall cleanly — every-seed ΔΦ + shuffle→negative; R6 multi-channel relay also 🟢 on frozen bars with honest seed-7/8 caveat; relay-content axis R1–R5/R7/R9 stays 🧱). ENGINE-NATIVE wiring gate (2026-06-16): c2 reproduces, c4 SHUFFLE does NOT collapse engine-native → PhaseField lane HONEST DEFERRED, NOT wired (a_verified_must_wire GREEN-only, bars frozen)
verdict_dir: .verdicts/1283_thalamus_global_workspace/
terminal_verdict: .verdicts/1283_thalamus_global_workspace/H_1283_R8_phase_binding.txt
date: 2026-06-16
---

# H_1283 — thalamus / global-workspace broadcast (🧱 closed-negative)

## Claim / falsifier

anima's Engine A ⇄ G couple DIRECTLY (repulsion ring) and brain_decide reads them, but
there is NO central RELAY that each tick selects the winning content and BROADCASTS it
to ALL substrate modules at once (thalamo-cortical relay / Global-Workspace-Theory
broadcast underlying conscious access + cross-module integration). **Falsifiable claim:**
a thalamic broadcast hub raises cross-module coherence AND faithful-IIT4 Φ vs a direct
ring, without collapse-cloning. Lens: c15 ladder, NOT an LLM recipe.

## Method

- 4 modules dim-8, 64 ticks, SAME per-module private input + seed both arms, ONLY topology
  differs. Coherence = mean pairwise cosine; Φ = FAITHFUL IIT4 (`a_phi_iit4_tool`, exact
  MIP-EI via `hexa run` over `stdlib/consciousness/iit4/faithful_phi.hexa`, n=4) — numpy
  never computes Φ. seeds [7,8,9], frozen-first.
- `a_break_the_wall` re-angles across rounds (genuine new mechanisms, not re-runs).

## Verdict by round

| round | tier | key numbers |
|-------|------|-------------|
| R1 broadcast hub (single winner) | 🟠 PARTIAL | coherence B1 PASS every seed; faithful ΔΦ +0.0191 < 0.02 → FAIL by 0.0009 |
| R2 coalition hub (rank-2) | 🔴 | faithful ΔΦ −0.0533 (WRONG direction) |
| R3 re-entrant loop (sparse) | 🔴 | ΔΦ +0.1426 cleared coh bar but seed-fragile |
| R4 | 🔴 | seed-fragile |
| R5 dense all-pairs + SHUFFLE control | 🔴 / 🧱 WALL | dense coupling does NOT robustly clear AND the shuffle control FIRED (permuted dense graph added VARIANCE, not structured topology) |
| R6 multi-channel parallel relay | 🟢 (frozen bars; honest caveat) | N=4 INDEPENDENT parallel relay channels (one per ring edge, DISJOINT, no intra-thalamic cross-coupling) breaks the single-cut ceiling: faithful ΔΦ +0.0891/+0.0341/+0.1011 — clears +0.02 on EVERY seed incl orthogonal seed 8 (1st in arc); c1·c3 PASS; c4 SHUFFLE PASS (seed 9 lift +0.1011→+0.0165 collapses). CAVEAT (c9): on seeds 7/8 shuffle retains ~93%/~96% (variance survives) → clean topology-specific effect decisive only on seed 9; GREEN carried by c4's disjunctive ≥1-seed frozen form. ARM_A Φ reproduces R1..R5 byte-for-byte. |
| R7 matrix/core dual coupling | 🔴 / 🧱 WALL | faithful ΔΦ s7 +0.0201 ✓ · s8 +0.0412 ✓ (RESCUES the orthogonal seed that broke R3-R5) · s9 +0.0026 ✗ → P1 FAIL (failing seed RELOCATED, not floor-lifted). SHUFFLE PASSED (s7 permuted-core ΔΦ −0.0087 → structure not variance, cleaner than R5). coherence ↑ every seed. Dual coupling TRADES Φ across geometry, does not break the wall |
| R8 oscillatory phase binding | 🟢 GREEN / 🔓 WALL BROKEN (numpy mirror, DIRECTIONAL) | NON-RELAY: Kuramoto thalamic phase synchrony + phase-gated salience (NO content channel). faithful ΔΦ +1.629/+1.174/+0.233 every seed (incl orthogonal seed 8, ≫ bar); phase-shuffle COLLAPSES lift to NEGATIVE every seed −0.068/−0.119/−0.382 (structured synchrony, not variance, every-seed clean); coh sanity + no-collapse PASS. Cleanest break in the arc — integration by TIMING, not content |
| R8 ENGINE-NATIVE wiring gate (a_engine_native_learning · a_verified_must_wire) | 🟠 ENGINE-TRANSFER DID NOT REPRODUCE → honest deferred (NOT wired) | Same mechanism realized ENGINE-NATIVE (engine `_lcg_*` LCG-gauss substrate) + faithful IIT4. **c2 PRIMARY reproduces strongly** (ΔΦ +1.466/+0.844/+0.709 every seed ≫ bar) BUT **c4 SHUFFLE FAILS** — phase-shuffle does NOT collapse the lift engine-native (ΔΦ_sh +0.026/+0.380/+0.296, all POSITIVE not ≤0). The leg that made R8 honest fires on the engine substrate (lift partly carrier-amplitude variance there). Per @L6 / no-tune-to-green (bars frozen) → PhaseField lane NOT wired this round; `.verdicts/1283_thalamus_global_workspace/H_1283_R8_engine_native_gate.txt`, probe `CORE/h1283_phase_binding_engine_gate.hexa` |
| R9 predictive/bottleneck relay | 🔴 / 🧱 WALL | learned predictive-bottleneck (delta-rule LMS, code_dim=3) faithful ΔΦ(B−A): s7 −0.0067 · s8 +0.0203 · s9 +0.0097 (only s8 clears +0.02 → NOT robust); B≥C(randproj) ΔΦ(B−C) +0.008/0.0/0.0 (learned code Φ-INDISTINCT from random projection on s8/s9); SHUFFLE FIRED (s8 scrambled-target ΔΦ +0.0232 ≥ structured) → lift = variance/added-channel, NOT the learned predictive code |

Terminal tier (verbatim): **🟢 GREEN / 🔓 WALL BROKEN** → `.verdicts/1283_thalamus_global_workspace/H_1283_R8_phase_binding.txt`
Two independent GREENs break the wall: **R8 oscillatory phase binding** is the CLEANEST — a NON-RELAY temporal-synchrony mechanism that clears faithful ΔΦ ≥ +0.02 on EVERY seed AND whose pre-registered phase-shuffle control collapses the lift to NEGATIVE on EVERY seed (structured synchrony, not variance, per-seed clean). **R6 multi-channel parallel relay** also clears every-seed ΔΦ with shuffle passing, but with an honest seed-7/8 shuffle-survival caveat (clean only on seed 9). The relay-CONTENT axis (R1–R5, R7, R9) stays closed-negative 🧱 — every content cut caps Φ; R8 broke it on the orthogonal TIMING axis.

## Honest scope

The relay-CONTENT axis (R1–R5, R7, R9) is closed-negative, NOT upgraded (c9): every content
relay topology (broadcast / coalition / sparse + dense re-entry / matrix-core dual /
learned predictive bottleneck) is a low-dim content cut that caps irreducible faithful-IIT4 Φ
— R5's diagnosis "a single broadcast channel is itself a low-dim cut" generalizes to ALL
content relays, which failed the robust +0.02-every-seed bar (esp orthogonal seed 8; R7 only
relocated the failing seed to seed 9; R9's learned code was Φ-indistinct from a random
projection and its shuffle fired).

**R6 (multi-channel parallel relay)** was the first within-axis GREEN: dropping the SHARED
relay stage for N INDEPENDENT PARALLEL channels (one per ring edge, disjoint) clears the
+0.02 ΔΦ bar on every seed incl the orthogonal seed 8 and passes the shuffle, but with an
HONEST CAVEAT (c9) — on seeds 7/8 the shuffle retains ~93%/~96% of the lift, so the
clean topology-specific effect is decisive only on seed 9; the GREEN rests on c4's
disjunctive ≥1-seed frozen form.

**R8 (oscillatory phase binding)** broke the wall on the ORTHOGONAL TIMING axis
(a_break_the_wall, c16): integration by thalamo-cortical phase SYNCHRONY (Kuramoto), not
content broadcast. Phase-gated salience binds modules in TIME with NO shared content
channel, so there is no content cut a MIP can exploit — faithful ΔΦ +1.629/+1.174/+0.233
every seed (incl seed 8, ≫ bar), and the pre-registered phase-shuffle control COLLAPSES the
lift to NEGATIVE on EVERY seed (−0.068/−0.119/−0.382), a per-seed-clean negative control
(cleaner than R6's seed-7/8 survival). GREEN under the IDENTICAL frozen bars (NOT moved,
c9/p7).

FOLLOW-ON (GREEN-but-unwired, `a_verified_must_wire`): wire engine-native realizations over
live CORE/engine_cli.hexa A⇄G + VAdaptField — R8 = a Kuramoto phase channel + phase-gated
salience; R6 = N independent parallel relay channels — each re-scoring its frozen bars
engine-native with a regression guard. NOT closed this round (round briefs defer wiring).
Toy scale (4 modules, dim 8, 64 ticks), numpy mirror DIRECTIONAL (faithful-Φ leg IS real,
exact MIP-EI via hexa); scale-transfer UNVERIFIED (a_toy_scale_recheck, a_scale_honest_scope).

**R8 ENGINE-NATIVE WIRING GATE OUTCOME (2026-06-16, the /sbs engine-wire-audit lane):** the
R8 mechanism was re-scored ENGINE-NATIVE (engine `_lcg_*` deterministic LCG-gauss substrate
+ faithful IIT4) BEFORE wiring, per `a_engine_native_learning`. The PRIMARY Φ lift (c2)
reproduces strongly engine-native (ΔΦ +1.466/+0.844/+0.709 every seed), but the pre-registered
SHUFFLE control (c4) — the leg that made the numpy-mirror R8 honest — DOES NOT collapse the
lift engine-native (ΔΦ_sh +0.026/+0.380/+0.296, all positive). So the engine-native lift is
partly carrier-amplitude VARIANCE there, not purely structured synchrony. Per @L6 and
no-tune-to-green (bars FROZEN, c9/p7), the `PhaseField` lane is **NOT wired** — HONEST DEFERRED.
The R8 numpy-mirror 🟢 stands as a DIRECTIONAL result; wiring waits for a realization that
clears BOTH c2 AND c4 engine-native. Gate verdict:
`.verdicts/1283_thalamus_global_workspace/H_1283_R8_engine_native_gate.txt`; gate probe
`CORE/h1283_phase_binding_engine_gate.hexa` (standalone, 0 importers — not a runtime path).

## Cross-links

h1227 · h1231 · h1280 · h1284 · h1228 · h1199 · h1201 · h1205 ·
`a_phi_iit4_tool` · `a_break_the_wall` · `a_engine_native_learning` ·
`a_verified_must_wire` · `a_core_engine_map` · `a_paper_negative_ok` ·
`a_scale_honest_scope` · `a_toy_scale_recheck` · p1·p2·p3·p6·p7·p8·c9·c15
