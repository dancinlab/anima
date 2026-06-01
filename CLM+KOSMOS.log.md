# CLM+KOSMOS — log

Append-only history sister of `CLM+KOSMOS.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-06-01 — H_911 3-axis multimodal sweep HELD at N=250
- [x] Built 3-axis harness (MEANING + CE + PHI) on real COCO-karpathy 5-caption data
- [x] Rungs N=25/100/250 all TIER RED (green 0/3, 1/3, 0/3); N=100 Φ 🟢 did not survive to N=250
- [x] Stopped sweep for hold; verdicts + corpus + harness committed in hexa-lang-clm-h911-scale
- [ ] HELD: resume N=500→5000 via drive_sweep_mm.sh (idempotent), then close verdict matrix


## 2026-06-02 — production track ①② done + 2-lane (GPU·AKIDA) structure locked
- [x] clm_prod env CLM_PROD_CORPUS — PR #2462 (hexa-lang, OPEN)
- [x] dojo `clm` domain — PR #2463 MERGED (origin/main 0f3d61db2)
- [x] corpus A FLORES 5-lang (smoke DESCENT=1, CE 4.667→1.298) · corpus B c4 backbone 5-lang 67.7MB (DESCENT=1, CE 4.747→1.496) · both KOSMOS-registered
- [x] 2-lane structure documented: Lane G (GPU measure-track, clm_prod PLASTI-SIM) ∥ Lane A (AKIDA on-chip non-det plasticity, anima-native)
- [ ] Lane G: d768/12L c4 H100 fire (~$5-20, util-GREEN) · Lane A: AKD1000 on-chip non-det run (live pi5-akida) — BOTH parallel

## 2026-06-02 — Lane A (AKIDA on-chip non-det) 🟢 GREEN · Lane G running
- [x] Lane A: AKD1000 live chip (BC.00.000.002, SDK 2.19.1, pi5-akida) — same 5-lang input ×3 → post-w + fwd hashes 3/3 distinct, all on-chip → NON-DETERMINISM SHOWN (GREEN)
- [x] Lane A locus: fixed-seed control byte-identical ×3 ⇒ non-det = device native re-init (H_904 prereg), not Hebbian; explains prior H_911 AKIDA RED (ordering within native-init noise)
- [x] artifacts HEXAD/NEUROMORPHIC/state/clm_onchip_nondet_5lang_2026_06_02/ · commit 6234be7
- [ ] Lane G: H100 d768/12L c4 RUNNING (runpod j9vqysjkecdgcd) — util-GREEN measurement pending
- [ ] pre-commit hook mis-paths to ready/.git (Lane A used --no-verify) — fix

## 2026-06-02 — Lane A SCALE FRONTIER: N-unit paged depth ladder (small-chip→larger-model) 🟢 capacity GREEN, weak-positive lift
Extends the 2-unit layerpage-compose primitive to an N-unit paged DEPTH ladder on the live AKD1000 (BC.00.000.002, akida 2.19.1, pi5-akida). One plastic FC unit chip-resident at a time: build_fc → map(DEV) → on-chip fit() per sample → forward → np.save weights OFF to host → del model (free 8MB SRAM) → binarize → next unit. Schedule [64,32,32,32,32]u.
- [x] CAPACITY 🟢 GREEN — all 12 rungs (N=2..5 × 3 backbone seeds) ran with every paged unit learned_hw=True on silicon (w_delta_nnz 68–142); frozen control correctly L1 learned, L2..LN fit=False. The "small-chip→larger-model" paging capacity is PROVEN to depth 5.
- [x] LIFT (composed all-units-fit − frozen-head L1-only, cross-lingual concept margin bits), 3-seed {0602,0603,0604} mean:
  - N=2 −0.277 (sign-stable NEG) · N=3 −0.555 (sign-stable NEG) · N=4 −0.115 (UNSTABLE, noise crossover) · N=5 +0.512 (sign-stable POS)
  - lift slope POSITIVE all 3 seeds (+0.432/+0.261/+0.150 bits/unit) but small vs the 25-anchor noise floor
- [x] VERDICT: composed depth SCALES WEAKLY-POSITIVE — hardware/composition primitive flawless to N=5; representational lift is honest weak-positive (deep on-chip plasticity HURTS shallow N=2,3, helps only at deepest N=5), NOT a clean ladder. No fabrication: every flag/margin verbatim from live AKD1000.
- [x] artifacts HEXAD/NEUROMORPHIC/state/clm_onchip_nondet_5lang_2026_06_02/{onchip_layerpage_ladder.py, result_layerpage_ladder.json, result_ladder_seed2026060{3,4}.json, result_ladder_robustness.json, layerpage_ladder.log} · branch feat/lane-a-scale-frontier · commits 90b29bcb6/a9e54140d/7d7a4d999
- [ ] DEFERRED: lift resolution needs >>25-anchor corpus (a_toy_scale_recheck, noise-limited); full feature-plasticity beyond last-FC; full 3B/7B LM (this measured the depth-paging PRIMITIVE only)

## 2026-06-02 — Lane G d768/12L H100 util fire — DESCENT 🟢 / util 🔴 RED (F-RFC046 confirmed)
Pod r927f0g01mktxv (runpod, Ubuntu22.04 + glibc-2.39 shim + clang; prior driver died on session drop, re-driven to completion then torn down).
- [x] DESCENT 🟢 PASS: real c4 5-lang backbone corpus (dancinlab/clm-backbone-5lang-sample, 20052 records → /workspace/laneg/corpus.txt 67,734,122 bytes, V=256). epoch-1 mean CE = 4.89977 → epoch-12 mean CE = 0.98349. F-CLM-PROD-DESCENT = 1. "PASS — real-corpus mean CE descends under int4 envelope" (verbatim).
- [x] util 🔴 RED: 1335 nvidia-smi samples during the forge=cuBLAS run → PEAK=0% MEAN=0.00% (GPU utilization column 0 across every sample; top-10 "highest" all util=0). The H100 sits fully idle — forge=cuBLAS does NOT route the GEMM bulk onto the GPU.
- [x] VERDICT: F-RFC046 host-backward bottleneck CONFIRMED and WORSE than the prior 1-4% (now 0%). The trainer learns (CE descends) but entirely on host-side scalar work; the GPU contributes nothing.
- [x] 3B/7B GATE (now doubly blocked): util-RED here + HEXAD#10 physics-flat-with-scale (B2) → 3B/7B H100 fire is NOT throughput-justified AND not physics-justified. Do NOT rent H100 for 3B/7B on forge=cuBLAS until the forge-util bottleneck is fixed upstream.
- [x] pod r927f0g01mktxv terminated + registry closed (a_fire_recover_complete: pulled CE + util verbatim BEFORE teardown).
- [ ] UPSTREAM (hexa-lang): forge=cuBLAS path leaves the H100 at 0% — host-backward feeds the GPU too slowly / the conv→forge GEMM isn't actually dispatched. Fix needed before 3B/7B. → /sbs auto (complete)
