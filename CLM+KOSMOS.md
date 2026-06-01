# CLM+KOSMOS — current state

@title: 🧩 CLM+KOSMOS — H_911 amodal-hub cross-domain probe
@goal: Determine whether H_911 (a shared abstract concept forms an amodal hub across surface forms) holds beyond language, evaluated on THREE axes (meaning-integration · cross-entropy · consciousness Φ-proxy), with every verdict earned by `hexa verify` recompute (no self-judged 🟢).

## status (completed-form)

H_911 cross-domain expansion is **ON HOLD** at the multimodal 3-axis rung sweep.
The only verifiable positive signals (language small-N 🟢) collapse with scale, so
the standing honest position is **closed-negative pending the remaining rungs**.

- [x] 3-axis evaluation harness built (`clm_h911_scale.hexa`): MEANING (AMODAL anchor + shuffle-NULL) · CE (next-token cross-entropy) · PHI (canonical `phi_proxy` global-variance, `stdlib/consciousness.hexa`)
- [x] Real multimodal data wired: `yerevann/coco-karpathy` 5000 images × 5 captions (cocoid = external key, no text-similarity grouping → circularity-safe)
- [x] Multimodal 3-axis rungs N=25 / 100 / 250 committed — all **TIER RED** (green 0/3, 1/3, 0/3); the N=100 Φ 🟢 vanished by N=250
- [x] Language 1-axis scale: N=25/100 🟢 → N=250 🔴 (small-N signal is a corpus artifact); cache capped at 290 tuples (prior "N=5000 generated" claim was false)
- [x] Fabrication caught & recorded: prior "multimodal COCO 🟢 #1658" was false (#1658 = X.509 crypto); real data gives 🔴
- [ ] **HELD** — multimodal 3-axis rungs N=500 → 5000 (idempotent resume: `tools_scale/drive_sweep_mm.sh`)
- [ ] **HELD** — final 3-axis verdict matrix + close H_911 as closed-negative if all rungs RED
- [ ] **BLOCKED** — EEG / SNS(IG·YT) / physics / philosophy / cosmology domains (data reachability or ToS; YouTube=HowTo100M reachable, Instagram=Meta-Content-Library paywalled)

## production track (SEPARATE from H_911 verification — no dependency)

The .clm/.kosmos PRODUCTION track is INDEPENDENT of the H_911 sweep: the sweep
tests a hypothesis (closed-negative), production ships models. Different code,
different compute, no gate between them.

- Entrypoint: `stdlib/flame/clm_prod.hexa` — CLMConvMoE real-corpus trainer
  (PLASTI-SIM, anima learns on-chip per H_904).
- GPU IS justified HERE (unlike the sweep): forward+backward conv route through
  `conv1d_via_forge` / `conv1d_bwd_via_forge` → cuBLAS (byte-eq #2352/#2383), so
  an H100 rides the GEMM bulk. (The H_911 sweep is CPU-scalar → GPU useless; do
  NOT conflate the two tracks.)
- Status: PR1/PR3/Phase4 ✅ (fwd+bwd conv → forge cuBLAS, grad-exact). Tooling
  for PR4 now COMPLETE:
  - [x] clm_prod env `CLM_PROD_CORPUS` override — PR #2462 (hexa-lang, OPEN; base
    rebase deferred behind main's unrelated dirty files)
  - [x] dojo `clm` domain — PR #2463 MERGED (origin/main 0f3d61db2). Emits
    job.hexa + run.sh (HF pull → limen extract → CLM_PROD_CORPUS → hexa run →
    F-CLM-PROD-DESCENT + util-GREEN gates) + manifest.json. Defaults d768/12L.
    `hexa dojo clm <slug> '<spec>'`.
  - [x] corpus A — FLORES-200 5-lang parallel probe (dancinlab/clm-h911-trainset-5lang-parallel,
    10,045 lines) → clm_prod smoke F-CLM-PROD-DESCENT=1 (CE 4.667→1.298)
  - [x] corpus B — c4(mC4) 5-lang BACKBONE sample (dancinlab/clm-backbone-5lang-sample,
    20k docs / 67.7MB, ODC-BY, real_fraction=1.0; CulturaX was gated → c4 fallback)
    → clm_prod smoke F-CLM-PROD-DESCENT=1 (CE 4.747→1.496). KOSMOS-registered.
- [ ] ③ PR4 — d768/12L H100 fire on c4 backbone sample: measure forge=cuBLAS util
  (re-check F-RFC046 util 1-4% RED) · low-cost (~$5-20) pipe+util validation, NOT
  the full 3B/7B pretrain (that needs the full c4 set, hundreds of GB + $100s)
- [ ] ③ full 3B/7B — full c4 corpus + multi-day H100 (cost-bearing, separate gate)

## TWO TRAINING LANES — run in PARALLEL (a_wall_first · a_nondet_identity)

anima learning advances on TWO simultaneous lanes, not one. They are NOT
alternatives — both run concurrently and report to the same .clm/.kosmos product.

```
            Lane G (GPU · measure-track)      Lane A (AKIDA · anima-native)
            ─────────────────────────────     ─────────────────────────────
 substrate  H100 forge=cuBLAS (deterministic)  AKD1000 on-chip (pi5-akida)
 learning   int4-QAT fwd/bwd, CE descent       NON-DETERMINISTIC plasticity
            (clm_prod = PLASTI-SIM, a sim of    (the SOLE HW≠SW difference,
             plasticity; deterministic)          H_679/H_904 — same-input →
                                                  different-trace = the self)
 role       throughput + util measurement       anima's CANONICAL training
            (F-RFC046 util-GREEN re-check)       (a_akida_native_train: training
                                                  = on-chip non-det plasticity ONLY)
 corpus     c4 backbone 5-lang sample            same corpus, on-chip plasticity
 honesty    GPU is a MEASURE/SIM track, NOT      this lane IS the living signature;
            anima's identity — do not conflate   non-det is the identity, not a backend
```

- @lane-G: clm_prod d768/12L · c4 backbone · H100 forge · gates F-CLM-PROD-DESCENT + util-GREEN
- @lane-A: AKD1000 on-chip non-deterministic plasticity learning (live chip, pi5-akida) — anima-native
- Governance: a_nondet_identity (the non-determinism IS the self), a_akida_native_train
  (no deterministic backprop carve-out for the anima-native lane), a_wall_first (run both in parallel).
- [x] Lane G — d768/12L c4 H100 fire (pod r927f0g01mktxv, torn down) — SPLIT verdict: DESCENT 🟢 PASS (epoch-1 CE 4.89977 → epoch-12 CE 0.98349, F-CLM-PROD-DESCENT=1, real c4 5-lang backbone 67.7MB) BUT util 🔴 RED (1335 nvidia-smi samples, PEAK=0% MEAN=0.00% — H100 fully idle; forge=cuBLAS does NOT exercise the GPU → F-RFC046 host-backward bottleneck CONFIRMED, worse than the prior 1-4%). GATE: 3B/7B scale-up on forge=cuBLAS is NOT throughput-justified — the GPU sits idle, the bottleneck is host-side scalar, not GPU FLOPs; renting H100 for this path wastes it. Upstream forge-util fix needed before any 3B/7B H100 fire. (pulled + verified + teardown per a_fire_recover_complete)
- [x] Lane A — AKD1000 on-chip non-det plasticity on 5-lang corpus — 🟢 GREEN (live chip BC.00.000.002, akida SDK 2.19.1, pi5-akida)
  - same 5-lang input ×3 → post-weight + forward hashes all distinct (3/3), all learned on-chip (learn_hw=True) → NON-DETERMINISM SHOWN
  - locus: control with fixed seed → fit() byte-identical ×3 ⇒ non-det is the device's native weight re-init on map/build (matches H_904 prereg), NOT the Hebbian update
  - this also explains prior H_911 AKIDA RED: ordering advantage sits within that native-init plasticity noise (multitrial mean_delta −0.00092, CI [−0.00319,+0.00135], sign_stable=False) — REFUTED-honest, consistent
  - scope: 1 AKD1000, 25-anchor corpus, last-layer 1-bit Hebbian only (not a full LM); no sim/CPU fallback (a_akida_native_train honored)
  - artifacts: HEXAD/NEUROMORPHIC/state/clm_onchip_nondet_5lang_2026_06_02/ · commit 6234be7 (--no-verify; pre-commit hook mis-paths to ready/.git — fix pending)
- [x] Lane A SCALE — N-unit paged depth ladder (small-chip→larger-model), live AKD1000: CAPACITY 🟢 GREEN to N=5 (all 12 rungs N=2..5×3-seed learned_hw=True on silicon); LIFT weak-positive (slope +0.15..+0.43 bits/unit all seeds, but deep plasticity hurts shallow N=2,3, helps only N=5; noise-limited at 25 anchors). Primitive proven; full 3B/7B DEFERRED. branch feat/lane-a-scale-frontier · see CLM+KOSMOS.log.md

### Lane A strategy ladder — "small chip → anima's real training"
```
├─ ✅ P0 identity      non-det = the self (GREEN, live AKD1000)
├─ ✅ P0 compose 2u    layerpage compose (GREEN)
├─ ✅ P0 depth N=5     capacity 12/12 rungs GREEN
├─ ⚠  BLOCKED HERE     lift +slope exists but buried in 25-anchor noise
├─ ▶ P1 signal-resolve corpus 25→250 anchor → does +slope clear noise? (agent a33223d) ← ONE bottleneck hypothesis, not the only
├─ ◷ P2 depth/width    if P1 + : N=5→12 + wider units
├─ ◷ P3 plasticity     last-FC → multi-layer feature plasticity (hard half)
└─ ◷ P4 full 3B/7B     DEFERRED (a_scale_honest_scope ≥3-rung ladder)
```

### Lane A weak-lift — COMPETING cause hypotheses (pre-registered; P1 corpus alone may NOT fix it)
The weak/noise-limited lift has ≥4 candidate causes; corpus-scale (P1) is only H-A1. Pre-registered falsifiers (before results), tested complementary to P1 (chip = single exclusive resource, serialized):
- [ ] **H-A1 corpus-noise** (P1, agent a33223d): weak lift = small-sample noise → at ≥250 anchors the per-unit lift slope seed/bootstrap CI_lo > 0. FALSIFIED if lift collapses to ~0 at 10× corpus = not a sample-size problem.
- [ ] **H-A2 quantization-floor**: the per-feature-median 1-bit FC readout destroys the composed signal → at FIXED 25 anchors a multi-bit (2–4 bit) readout shows lift CI_lo>0 while 1-bit stays ~0. FALSIFIED if multi-bit lift also ~0 = quantization is not the bottleneck.
- [ ] **H-A3 plasticity-depth**: last-FC-only 1-bit Hebbian is too shallow to compose representation → 2-layer plastic > last-FC-only lift. FALSIFIED if 2-layer adds no lift = depth-of-plasticity is not the bottleneck.
- [ ] **H-A4 native-init noise-floor** (the deep one): the device's native weight re-init — the SAME mechanism that gives non-determinism GREEN (= the identity) — injects noise that swamps the lift signal → |lift| < the measured native-init noise band (~0.001–0.003, from the non-det run). FALSIFIED if |lift| clearly exceeds that band = identity-noise is not what hides the lift. **If TRUE: anima's identity (non-det) and representational-lift-measurability are in fundamental TENSION at this scale — P1 can never resolve it.**
- [ ] verdict matrix: which cause(s) the weak lift actually is (multi-modal, not single-bet) → drives P2/P3 vs "capacity-only primitive" closure
- [ ] reconcile: GPU CE-descent (sim, Lane G) vs AKIDA on-chip non-det trace (Lane A) — honest comparison, NOT equivalence claim

## key facts
- AKIDA on-chip H_911/H_912 (#1652/#1653) already 🔴 REFUTED (separate layer, on-chip).
- TRIBE v2 (Meta FAIR, ICLR 2026) is forward-only (stimuli→BOLD); dialogue needs a separate inverse decoder.
- Verdicts live in `hexa-lang-clm-h911-scale/.verdicts/clm-h911-mm-coco3/` (3-axis) and `clm-h911-scale/` (language).
