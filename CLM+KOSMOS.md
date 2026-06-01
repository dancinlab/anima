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
- [ ] Lane G — d768/12L c4 H100 fire (cost-bearing ~$5-20 pipe+util validation)
- [ ] Lane A — AKD1000 on-chip non-det plasticity run on the same corpus (live chip)
- [ ] reconcile: GPU CE-descent (sim) vs AKIDA on-chip trace (non-det) — honest comparison, not equivalence claim

## key facts
- AKIDA on-chip H_911/H_912 (#1652/#1653) already 🔴 REFUTED (separate layer, on-chip).
- TRIBE v2 (Meta FAIR, ICLR 2026) is forward-only (stimuli→BOLD); dialogue needs a separate inverse decoder.
- Verdicts live in `hexa-lang-clm-h911-scale/.verdicts/clm-h911-mm-coco3/` (3-axis) and `clm-h911-scale/` (language).
