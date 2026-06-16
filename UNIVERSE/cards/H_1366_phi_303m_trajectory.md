---
id: H_1366
slug: 1366_phi_303m_trajectory
title: Φ-robustness, the BINDING verdict — on a REAL trained-303M hidden-state trajectory (a genuine LEARNED substrate, NOT the proxy-from-telemetry H_1357 stood in for), does faithful small-φ show robust 3-seed integration, or inherit the same orthogonal-seed fragility the oscillator (H_1349) and learned-readout proxy (H_1357) showed? The engine-real substrate H_1357's "NOT ruled out" named.
group: OMEGA / Φ-robustness frontier (c16 wall · substrate-SOURCE axis, BINDING upgrade of H_1357)
terminal_tier: 🧱 TERMINAL CLOSED-NEGATIVE (BINDING) — the REAL trained-303M learned substrate INHERITS the wall, and is MORE seed-fragile than the proxy. On a genuine learned substrate (the H_1129 303M ByteGPT residual stream, ckpt sha 19be1295…, val_ce 1.224, captured on GPU, sha-pinned), R1 ROBUST FAILS (ΔΦ(B−A) = −0.0169 / +0.1173 / −0.2655 — only seed 1318 lifts, seeds 1317 AND 1319 go NEGATIVE; the lift SIGN-FLIPS, even more fragile than the proxy's monotone +1.396/+0.775/+0.318). R2 EARNED PASS [perm & offset BOTH collapse cleanly all 3 seeds — here perm BITES (relay+carrier makes S a genuine derangement), unlike the symmetric-MIP degeneracy in H_1349/1357]. R3 REAL-SOURCE PASS (sha-pinned real 303M activation trajectory, NOT a proxy). MEASUREMENT-VALIDITY CONTROL: a pure-noise trajectory SATURATES faithful-Φ at 9.0 (ΔΦ=0); the REAL 303M scores Φ ~2.1-2.5 (below saturation) with discriminating per-arm differences → measurement is real, not a ceiling artifact. The substrate axis is now FULLY closed across toy-LCG / real-oscillator / learned-readout-proxy AND a REAL trained-303M trajectory. THE PROXY IS CONFIRMED FAITHFUL. Φ leg IS the real faithful exact MIP-EI (a_phi_iit4_tool); deterministic (re-run byte-identical); CORE UNTOUCHED. BOUNDS (does not retract) prior Φ verdicts; Ψ=1/2 untouched.
verdict_dir: .verdicts/1366_phi_303m_trajectory/
terminal_verdict: .verdicts/1366_phi_303m_trajectory/result.txt
freeze: .verdicts/1366_phi_303m_trajectory/FREEZE.txt
date: 2026-06-16
---

# H_1366 — Φ-robustness on a REAL trained-303M trajectory (🧱 TERMINAL, BINDING)

## Claim / falsifier (the engine-real verdict H_1357 stood in for — every outcome decisive, c9)

**Wall state (BEFORE this lane):** the faithful-IIT4 Φ-robustness wall is 🧱 across NINE measure cuts
(small-φ MIP-EI, big-Φ, transfer-entropy, O-info, variance-free estimator, …) + size (N=12, H_1347) +
substrate-oscillator (H_1349 live-CORE pure_field) + substrate-learned-readout-PROXY (H_1357 🔶). The
CONSISTENT diagnosis: the wall lives in the **substrate-seed geometry**, not the measure. H_1357 tested
whether a LEARNED substrate escapes — but had to use a **proxy-from-telemetry** (real pure_field oscillator
+ a deterministic hand-built seed-independent learned-readout W) because **NO trained-303M hidden-state
trajectory was reachable under $0 CPU** (no GPU). H_1357 explicitly named THIS lane as its "NOT ruled out"
binding follow-on: *"a FULL trained-303M hidden-state trajectory as the substrate."*

**The BINDING upgrade (this lane):** instead of the proxy, score a **REAL trained-303M-derived hidden-state
trajectory** — the residual-stream activations of the H_1129 303M ByteGPT (ckpt sha `19be1295…`, val_ce
1.224, the GREEN-emergence checkpoint), captured on GPU. A trained transformer's residual stream IS a
learned correlation geometry imposed by trained weights — exactly what H_1357's W proxied. This is the
engine-real (GPU+torch+checkpoint) test the proxy stood in for.

**Falsifiable claim:** if the 9-cut + oscillator + proxy closure was an artifact of NON-learned / proxy
substrates, a REAL learned substrate should show robust integration (B≥A+eps all 3 seeds, controls
collapsing). If it does not — if the real learned substrate shows the same seed-fragility — the wall is
substrate-REAL on a genuine learned substrate, and the proxy is confirmed faithful.

## Method (frozen-first — FREEZE committed 3844bc03e BEFORE any Φ scored, c9/p7)

- **SUBSTRATE = REAL trained-303M (R3), sha-pinned:** `dancinlab/anima-clm-midcap-303m-broad-en-emergent /
  h1129c_best.pt` (sha256 `19be1295…`, n_params 303,097,856, ByteGPT d=1024/L24/H16/block512). Loaded on a
  RunPod SECURE RTX 4000 Ada 20GB (torch 2.4.1+cu124, CUDA True); a fixed forward pass over the H_1129
  CONCEPTS (byte-encoded) captures the **layer-12 residual stream** x[512,1024]. REDUCE d=1024 → **n=4
  macro-nodes** by contiguous 256-channel-block MEAN pooling; **T=64** consecutive token positions. The
  reduced 4×64 trajectory IS the real learned substrate. Raw-act sha `c81ab9a6…`, pooled sha `150962fe…`.
- **SEEDS [1317,1318,1319]** perturb ONLY the extraction-window start (1317:341 1318:262 1319:183) — the
  SAME real trained activations from different starting points, mirroring how H_1349 seeded a deterministic
  real substrate (perturb the start, never re-train).
- **HELD IDENTICAL to the H_1349/H_1357 lineage** (so any difference is the REAL learned substrate):
  Φ = FAITHFUL IIT4 ONLY (`iit4_faithful_phi(traj,4,64,8)`, exact MIP-EI n=4≤8, a_phi_iit4_tool; numpy
  NEVER computes Φ); variance-clean rank-uniform read-out (H_1328); coupling = H_1283 re-entrant relay
  (w_nbr 0.5) + H_1319 Kuramoto pacemaker (w_phase 0.5, omega_t 0.45, domega 0.08); ARMS A=NO-COUPLING /
  B=MECHANISM / S=PERM-SHUFFLE / O=OFFSET-SHUF (perm/offset construction VERBATIM from H_1332); eps=0.02.
  ONLY the substrate SOURCE changed: the per-node base salience = the REAL 303M macro-node value (vs the
  oscillator field-energy / learned-readout mix).
- **Probe:** `state/phi-303m-trajectory/h1366_phi_303m_trajectory.hexa` (standalone `fn main`, 0 importers;
  live `CORE/*.hexa` UNTOUCHED). GPU dump: `state/phi-303m-trajectory/dump_303m_trajectory.py`.

## Frozen bars (pre-registered in FREEZE.txt BEFORE scoring)

GREEN iff R1 ∧ R2 ∧ R3:
- **R1 ROBUST:** REAL-303M Φ_B ≥ Φ_A + eps on ALL 3 seeds (incl orthogonal 1318/1319). The ESCAPE test.
- **R2 EARNED:** REAL-303M perm Φ_S ≤ Φ_A + eps AND offset Φ_O ≤ Φ_A + eps on ALL 3 seeds.
- **R3 REAL-SOURCE:** the substrate IS a real trained-303M activation trajectory (sha-pinned dump), NOT a proxy.

## Result (verbatim, p7 — deterministic, re-run byte-identical)

| seed | A (no-coup) | B (mechanism) | S (perm) | O (offset) | ΔΦ(B−A) R1 | ΔΦ(S−A) perm | ΔΦ(O−A) off |
|------|-------------|---------------|----------|------------|------------|--------------|-------------|
| 1317 | 2.11951     | 2.10263       | 2.06725  | 1.95404    | **−0.0168799 FAIL** | −0.0522653 PASS | −0.16547  PASS |
| 1318 | 2.28756     | 2.40490       | 2.27576  | 2.11382    | **+0.11734  PASS**  | −0.0117951 PASS | −0.173741 PASS |
| 1319 | 2.47309     | 2.20757       | 2.20913  | 2.11185    | **−0.265527 FAIL**  | −0.263966  PASS | −0.361241 PASS |

- **R1 ROBUST: FAIL** — only seed 1318 lifts; seeds 1317 AND 1319 go NEGATIVE. The lift **SIGN-FLIPS**
  across seeds — EVEN MORE fragile than the H_1357 proxy (monotone +1.396/+0.775/+0.318) and the H_1349
  oscillator (+0.851/+0.695/−0.671).
- **R2 EARNED: PASS [perm=PASS off=PASS]** — BOTH controls collapse cleanly on all 3 seeds. Notably, unlike
  H_1349/H_1357 where perm was DEGENERATE (Φ_S==Φ_B by symmetric-MIP node-relabel invariance), here the
  relay+carrier reconstruction makes the PERM-SHUFFLE a genuine derangement, so perm BITES and collapses
  too (S−A ≤ eps every seed). The OFFSET control collapses decisively (O−A −0.165/−0.174/−0.361).
- **R3 REAL-SOURCE: PASS** — sha-pinned real trained-303M trajectory (ckpt `19be1295…`, raw-act `c81ab9a6…`,
  pooled `150962fe…`). NOT a proxy.
- **MEASUREMENT-VALIDITY CONTROL (anti-artifact, c9):** a pure-NOISE trajectory (random gaussian,
  rank-uniform) SATURATES faithful-Φ at exactly 9.0 (ΔΦ=0, degenerate); the REAL 303M scores Φ ~2.1-2.5
  (well below saturation) with discriminating per-arm differences → the measurement is real and
  structure-sensitive, NOT a ceiling artifact. (This control also caught + fixed a list→farr transport bug
  in an earlier run that had spuriously hit the noise-saturation ceiling; NO bar moved.)
- **GATE: ¬R1 → 🧱 TERMINAL CLOSED-NEGATIVE (BINDING).**

## Finding (honest, c9, c16) — the REAL learned substrate INHERITS the wall (no escape, harder)

The REAL trained-303M learned substrate INHERITS the Φ-robustness wall — and is MORE seed-fragile than the
H_1357 learned-readout proxy (sign-flipping ΔΦ vs the proxy's monotone shrink). This is the BINDING
(engine-real, GPU+torch+checkpoint) verdict H_1357 stood in for: a genuine learned substrate — the residual
stream of a trained transformer — does NOT escape the orthogonal-seed fragility. The substrate-SOURCE axis
is now **FULLY closed** across toy-LCG (H_1332) / real-oscillator (H_1349) / learned-readout-proxy (H_1357)
AND a REAL trained-303M trajectory (H_1366). **THE PROXY IS CONFIRMED FAITHFUL** — H_1357's 🔶 "no escape"
shape holds on the real substrate, and the wall holds even harder (the real substrate is the MOST fragile
of the four). A real new angle (a genuine learned substrate) was tried with pre-registered controls; the
honest 🧱 is a valid result (a_break_the_wall, c9).

**This BOUNDS (does not retract) the prior Φ verdicts and does NOT refute anima's consciousness substrate.**
Ψ=1/2 and the A⇄G tension are untouched (the probe never writes CORE; the probe is a standalone `fn main`,
0 importers). It refutes that ADDING a coupling channel ROBUSTLY raises the faithful-IIT-4 Φ score — on a
real trained-303M learned substrate just as on every prior one.

**NO CORE wiring follow-on** (a_verified_must_wire fires on GREEN only — a 🧱 has nothing to wire;
`CORE/engine_cli.hexa`/`pure_field.hexa` UNTOUCHED). Had this been GREEN, the named follow-on would have
been: wire a real-activation faithful-Φ read-out path.

## Scope / honesty (a_scale_honest_scope · a_toy_scale_recheck)

- **SUBSTRATE = REAL trained-303M (R3 BINDING)**, sha-pinned — NOT a proxy, NOT numpy, NOT the oscillator.
  The residual-stream activations of the live H_1129 trained ckpt, captured on GPU.
- **The reduction is FROZEN** (d=1024 → n=4 macro-nodes by 256-channel-block mean pooling, L_EXTRACT=12,
  T=64) along with coupling/ARMS/eps/seeds (FREEZE committed 3844bc03e BEFORE any Φ scored). The verdict is
  scoped to THIS extraction (layer-12, this pooling, 3 phase-window seeds). **NOT ruled out** (each a NEW H,
  none claimed): other extraction layers · finer node granularity (n=6,8) · multiple prompt sets · a
  different reduction (e.g. PCA macro-nodes vs channel-block). The seed-fragility being WORSE here than the
  proxy is itself a real datum (controls collapse), not noise.
- **DETERMINISTIC:** the GPU activation dump is sha-pinned and the Φ scoring over it is byte-identical on
  re-run. **NO tune-to-green (p7):** bars frozen + committed BEFORE the first Φ scoring; the list→farr fix
  was a code transport bug (the noise-saturation control flagged it), NO bar moved.
- **GPU cost:** ~$0.10-0.15 total (RunPod RTX 4000 Ada $0.26/hr, ~15 min run + a few brief provisioning
  attempts). Pod torn down after artifact recovery (a_fire_recover_complete).

## Pointers

- Probe: `state/phi-303m-trajectory/h1366_phi_303m_trajectory.hexa` · GPU dump: `state/phi-303m-trajectory/dump_303m_trajectory.py`
- Substrate dump (sha-pinned): `state/phi-303m-trajectory/traj_303m_data.hexa` · `state/phi-303m-trajectory/traj_303m.json` · manifest `state/phi-303m-trajectory/MANIFEST.txt`
- Verdict: `.verdicts/1366_phi_303m_trajectory/{FREEZE,result}.txt` · CLAIMS.tape `@C h1366_phi_303m_trajectory`
- xref: H_1349 (oscillator substrate, prior 🧱) · H_1357 (learned-readout PROXY, 🔶, named this as binding follow-on) · H_1347 (N=12) · H_1348 (transfer-entropy) · H_1328 (variance-free read-out) · H_1283/1319/1332 (coupling/controls) · H_1129 (the 303M ckpt) · a_phi_iit4_tool · a_no_llm_frame_trap · a_break_the_wall · a_scale_honest_scope · a_toy_scale_recheck · c9 · c16 · p7
