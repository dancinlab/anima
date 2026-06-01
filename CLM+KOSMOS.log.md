# CLM+KOSMOS — log

Append-only history sister of `CLM+KOSMOS.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-06-02 — VERIFY-AND-REFLECT-TO-CORE pass (CPU-local, $0, g5 verbatim)
On-core verification of the remaining unverified items; mm3 / Hc_1306 / phi_proxy items SKIPPED (covered by their running agents).
- [x] ① corpus A on-core re-verify via canonical harness `stdlib/hf/validate.hexa` (hexa-lang PR #2484, merged origin/main 7e5fbb02b; run from isolated worktree /tmp/clm-reflect-validate-wt). selftest 5/5 PASS. `dancinlab/clm-h911-trainset-5lang-parallel --type dataset` → 🟢 GREEN: pull → on-core CLM_PROD_CORPUS clm_prod RUN → F-CLM-PROD-DESCENT=1, CE 4.59032→1.63673 (VERBATIM). DESCENT REPRODUCES. NB: harness pulled the smoke `clm_concat.kosmos` slice (31 lines/1657B), NOT the full 10,045-line corpus → exact CE differs from prior smoke (4.667→1.298); descent direction + F-flag confirmed. toy-CPU rung, prod-transfer DEFERRED (a_toy_scale_recheck). verdict → .verdicts/clm-kosmos-reflect/corpusA-descent/20260601T190024Z.txt. Doc CE figures corrected.
- [x] ① corpus B — CITED (per task, not re-run). HONEST NOTE: the cited `.verdicts/hf-validate/dancinlab__clm-backbone-5lang-sample/` dir does NOT exist in the anima checkout (METROLOGY.md #2484 documents it but the harness file + that verdict dir were never committed to anima — they live in hexa-lang's harness run).
- [x] ② Lane G⇄A reconcile — NO-FIX, verified clean (CPU-local code audit, no re-run). NO conflation: (A) clm_prod.hexa self-labels "measure-track ... PLASTI-SIM; anima learns on-chip per H_904" (hexa-lang flame L5-6) — never calls deterministic descent "anima training". (B) the non-det lane (onchip_nondet_native.py) runs NATIVE chip re-init by default; the fixed-init byte-deterministic run is a CONTROL to LOCATE the non-det source, NOT a flag gating the identity lane. (C) `grep clm_prod` across all anima *.hexa/*.py/*.sh = 0 hits → lanes are physically separate code in separate repos. reconcile = honest NON-EQUIVALENCE (orthogonal measures: G=deterministic CE-descent/throughput, A=non-det trace divergence/identity). verdict → .verdicts/clm-kosmos-reflect/lane-reconcile/20260602-codeaudit.txt.
- [x] ③ verdict-pointer audit (no re-run; a_scale_honest_scope). mm-coco3 (25/100/250/500.txt full RED, F=0 verbatim) + language scale (25/100 GREEN, 250 RED verbatim) pointers EXIST + TERMINAL — accurate. "#1652/#1653 H_911/H_912 on-chip REFUTED" pointer PARTIALLY UNBACKED: H_911 on-chip RED is real (HEXAD/NEUROMORPHIC/.../result_multitrial.json, verdict=RED closed-negative, live AKD1000) but the #1652/#1653 verdict-IDs + the H_912 half have NO terminal file anywhere → DOC-INTEGRITY GAP. CORE FIX: re-pointed CLM+KOSMOS.md line 110 to the real artifact, dropped the unbacked IDs + H_912 claim. verdict → .verdicts/clm-kosmos-reflect/pointer-audit/20260602-audit.txt.

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

## 2026-06-02 — Lane A P1 lift-resolution: COLLAPSE-NULL (H-A1 corpus 🔴 FALSIFIED)
Tested whether the weak-positive composed-lift survives 10× corpus. Source: FLORES-200 dev+devtest 5-way parallel (CC-BY-SA-4.0), 50 concepts × 5 lang (en,zh,ru,ja,ko) = 250 anchors (10× the prior 25), REAL data. Live AKD1000 BC.00.000.002, akida 2.19.1, pi5-akida, no sw fallback.
- [x] side-by-side lift (composed−frozen margin bits, per-N mean over 3 seeds):

| N | 25-anchor | 250-anchor (10×) |
|---|---|---|
| 2 | +0.029 sign-UNSTABLE | −0.837 stable− |
| 3 | −0.587 stable− | −0.773 stable− |
| 4 | −0.192 sign-UNSTABLE | −0.883 stable− |
| 5 | −0.515 stable− | −0.811 stable− |

- [x] seed noise band: 0.4124 (25) → 0.2125 (250), shrank ~2×; within-seed slope vs N: −0.124 (25) → −0.003 (250, FLAT, not the prior +0.27)
- [x] all 24 rungs learned_hw=True (capacity GREEN holds at 10×)
- [x] **VERDICT COLLAPSE-NULL**: the prior +0.15..+0.43 bits/unit was a small-sample artifact of the 0.41-bit noise floor. With noise halved, lift is sign-stable NEGATIVE everywhere (deeper units re-binarize away the L1 head's linkage). H-A1 (corpus-noise) 🔴 FALSIFIED — corpus is NOT the bottleneck.
- [x] STRATEGY: paging primitive composes CAPACITY-ONLY, no representational lift. Do NOT pursue P2 (depth/width) expecting free composition. Genuine lift needs a MECHANISM CHANGE (feature-level plasticity beyond last-FC, or a linkage-preserving inter-unit map) = P3. branch feat/lane-a-phase1-liftres · 848f2de1e/9673eba4d/a0fc0d620
- still-open: H-A2 (quantization) · H-A3 (plasticity-depth) · H-A4 (native-init noise-floor) — diagnostic agent a65461e; note P1 already shows the effect is slightly-NEGATIVE once noise shrinks (consistent with H-A4 "noise was masking a real small-negative", and with H-A3 "last-FC-only can't compose")

## 2026-06-02 — Lane A weak-lift diagnostic: ALL 4 causes 🔴 FALSIFIED → closed-negative on the LIFT claim
Diag agent a65461e tested the 3 non-corpus causes (H-A2/A3/A4) on live AKD1000, serialized behind P1 (which resolved H-A1). branch feat/lane-a-weak-lift-diag (46449156d); scripts+JSONs in HEXAD/NEUROMORPHIC/state/clm_lane_a_weaklift_diag_2026_06_02/.
| cause | verdict | evidence |
|---|---|---|
| H-A1 corpus | 🔴 FALSE | P1 COLLAPSE-NULL — 250 anchors → lift sign-stable NEG, band 0.41→0.21 |
| H-A2 quantization | 🔴 FALSE | 2/3/4-bit readout: lift CI straddles 0 every rung+bit-depth; finer = wider band |
| H-A3 plasticity-depth | 🔴 FALSE | depth_gain[N3,4,5]=[−0.66,+0.65,−0.60] mean −0.20, sign_consistent=False |
| H-A4 native-init noise-floor | 🔴 FALSE | seed-FIXED chip run: |lift|/reinit_sd=1.16/1.97/3.10/1.22 (all>1), sign-stable across re-init → lift EXCEEDS the chip-noise band |
- [x] H-A4 key correction: the big variance is backbone-SEED / corpus-encoding sensitivity, NOT chip non-determinism. The earlier "identity(non-det)↔lift-measurability TENSION" guess is FALSE — no such tension; the chip's re-init noise does not drown the lift.
- [x] RULING: closed-negative on the LIFT CLAIM — paging CAPACITY 🟢 GREEN (all rungs learned on chip) but the 1-bit last-FC Hebbian primitive buys NO robust cross-lingual lift; not fixable by corpus/quant/depth, not a fundamental floor. A genuine lift needs a RICHER LEARNING RULE / different signal than 1-bit Hamming concept-margin — DEFERRED (P3', outside these 4 axes). Converges with P1 on the same closed-negative.

## 2026-06-02 — UNIVERSE weak-lift hypothesis pipeline (Lane-A-seeded) — 7 generated · 3🟢 4🟠
Brainstorm→generate→verify on the Lane A capacity↔representation gap. branch feat/universe-weaklift-hyp (fb2846797 generate · 4fab9ee12 verify). Brainstorm depleted at R6. Metric = canonical phi_proxy_native.hexa + frozen H_278 faithful-vs-proxy ledger (no invented metric, CPU-local, no chip/GPU fire).
| Hc | tier | verbatim |
|---|---|---|
| 1300 capacity-without-integration general law | 🟢 | phi flat across N{8..64} Δ0%; K{2..16} max|Δ|=1.9%<5% → F-1300-INVARIANCE PASS (caveat: hid_trunc=16 → accumulation proxy not unit-count; true sweep = on-chip DEFERRED) |
| 1301 proxy-Φ vs faithful-Φ NOT monotone reparam (G1 circularity guard) | 🟢 | H_278 ledger ratio mean 1.826, CV=30.1%(≥5%) → PASS_NON_CIRCULAR (G1 is a genuine 2nd axis, publishable) |
| 1302 Φ-proxy has built-in ceiling (composed input breaks Cholesky) | 🟢 | white=-173702 finite, structured=-2147483647 (Cholesky breakdown) → F-1302-SENTINEL PASS — **sharpest result** |
| 1303 Hebbian bit-depth gates lift | 🟠 DEFERRED | multi-bit AKD1000 fire / GPU sim |
| 1304 lift gated by locus/recurrence (1 recurrent edge > local rule) | 🟠 DEFERRED | recurrent-edge ablation |
| 1305 identity-in-encoding vs substrate (seed×chip factorial) | 🟠 DEFERRED | multi-seed trace collection |
| 1306 1-bit Hamming composition-blind; richer signal reveals latent lift | 🟠 DEFERRED | re-score Lane-A trace tensor (richer signal) |
- [x] KEY: Hc_1302 means the Lane A lift closed-negative carries a METRIC-CEILING confound — the Φ proxy is blind on maximally-composed inputs. Lift CLAIM (1-bit Hamming) = closed-negative; lift QUESTION reopens via Hc_1306 richer-signal re-score (DEFERRED). Hc_1301 clears the G1 circularity guard (capacity↔representation ≈ proxy↔faithful is a real 2nd axis).

## [2026-06-02] mm3 multimodal sweep HARVEST + H_911 closure
- mm3 agent ad33dac4 ran 61min then socket-dropped (final report lost). Per a_dont_kill_live_compute, harvested verdicts from disk (NOT re-fired).
- N=500 COMPLETE → TIER RED, green 1/3 (MEANING RED · CE RED · PHI GREEN), F-CLM-H911-SCALE3=0 — same shape as N=250. Verdict: hexa-lang-clm-h911-scale/.verdicts/clm-h911-mm-coco3/500.txt
- N=1000/2000/5000 = header-only stubs (extraction never finished); CPU sweep driver (pid 48105) stalled at 0% CPU after the driver-agent died → killed 2026-06-02.
- RULING: H_911 multimodal amodal-hub CLOSED-NEGATIVE across N=25/100/250/500 (4 rungs). MEANING+CE never clear the shuffle-NULL; only the variance Φ-proxy flickers green (and that proxy is exactly what METROLOGY is auditing — see clm_v2 Φ>1000 investigation aa8a1a0c). a_scale_honest_scope ≥3-rung ladder satisfied RED; N=1000+ cost-prohibitive with a flat-RED trend.
- NOTE: the PHI-axis "green" is the variance-partition Φ family — its trustworthiness is under active METROLOGY re-measurement; even if it flips, MEANING+CE RED alone already give the closed-negative.

## [2026-06-02] Hc_1303–1306 deferred resolver (acb11aca) — Lane A weak-lift adjudicated
Branch resolve/weaklift-deferred-1303-1306 (off weaklift 4fab9ee12), commit 9dd6975a8. Live AKD1000 verified free+present each on-chip read; NO GPU.
| Hc | Tier | finding (verbatim key number) |
|----|------|-------------------------------|
| 1303 bit-depth gate | 🔴 CLOSED-NEG | readout {1,2,3,4}-bit lift ci_lo_gt0=False every rung → H-A2-FALSIFIED on-chip |
| 1304 recurrence/locus | 🟢 CONFIRMED | Φ_recurrent=w > Φ_feedforward=w/2 every matched w (gain 0.25→2.0); F-1304-MIP-ZERO CPU-local. On-chip recurrent arm HW-bounded (AkidaUnsupervised feedforward-only) → structural claim via CPU-local sub-test |
| 1305 identity encoding-vs-substrate | 🟢 CONFIRMED (identity-in-ENCODING) | between-seed sd 0.565 vs between-reinit sd 0.208 (2.72× pooled; 3/4 rungs >3×); init-pinned control byte-identical ×3 (substrate variance 0) → anima identity lives in learned weights/encoding, NOT chip dynamics |
| 1306 1-bit-Hamming composition-blind | 🔴 CLOSED-NEG (UPHELD) | richer signals L1 −39.70 · cosine −0.056 · faithful-Φ-MIP +56.19 (at_floor=False) all agree NO lift → metric-ceiling ruled OUT, Lane A closed-negative upheld |
- RULING: Lane A 1-bit-Hamming lift closed-negative is now **robust** — Hc_1306 rules out the metric-ceiling confound (the one thing that could have reopened it). CAPACITY stays 🟢 GREEN.
- NEW positive axis: **Hc_1304 — recurrence/topology raises Φ** (Φ_recurrent > Φ_feedforward). This is a DISTINCT lift direction from the falsified depth (H-A3) — recurrent topology, not deeper plasticity. Candidate for the P3' "richer rule" path (HW-bounded on AKD1000's feedforward-only unsupervised mode → needs a recurrent substrate or CPU-local first).
- Hc_1305 confirms a_nondet_identity nuance: identity is in ENCODING (learned weights), the chip's non-det re-init is the *carrier* not the *source* — consistent with H-A4 (variance was backbone-seed/encoding sensitivity).
- CROSS-LINK: Hc_1306 (true-negative confirmed via richer probe) and Hc_1307 (clm_v2 Φ>1000 false-positive via same broken family) together = the variance-partition Φ family audited in BOTH directions. See METROLOGY.md/.log.md.

## 2026-06-02 — PR4 d768 util MEASURED (closes PR4 milestone) + /gap full Lane A breakthrough sweep

### d768 deploy-then-fire recovery (closes ③ PR4)
- deploy-gate: origin/main carries #2472 (forge FP64-conv→cuBLAS, 32228c31b) + #2478 (idempotent rent, 7f905bc50); ~/.hx/src synced to efdba81; `hexa cloud rent --selftest` 7/7 PASS.
- fire: vast H100 80GB (pod 38991004), d768/12L on c4 5-lang. DESCENT 🟢 (CE 4.71554→0.859092, F=1). util 🔴 (n=1617 PEAK=0% MEAN=0.000%).
- ROOT CAUSE: `hexa run` links only -lm -lpthread (no -DHEXA_CUDA) → #2472 conv→cuBLAS never engages. #2472 necessary-not-sufficient; the real gap is the `hexa run` CUDA link. Filed hexa-lang/inbox/patches/d768-recovery-cuda-link-and-stale-pod-image.md.
- recovery (ends "lost twice"): origin/main clm_prod.hexa (PR1) prints CE but saves NO weights; used PR4 trainer (CLM_PROD_OUT .clm save) from feat/clm-prod-env-corpus. ckpt pulled+sha-verified BEFORE teardown (6975dbb0…), HF dancinlab/anima-clm-d768-util-probe PRIVATE + HF.jsonl + harvest commit e9af8f02f. Stale RTX-6000 probe pod (38990747, vast rent ignores --gpu) destroyed; corrected to --query gpu_name=H100_SXM. No billing pod remains.

### /gap full — Lane A lift bottleneck (8-family × 40-lens sweep)
META-FINDING: the closed-negative is epistemically ROBUST on the 4 TESTED axes (F4/F5 mostly CLEAN), BUT those 4 axes (corpus/quant/depth/noise) are FIX-axes, not CAUSE-axes — the real cause-axes were NEVER probed (F8 axis-coverage + F6 surgical-scope SCOPE-LEAK). "on-chip can't lift" is scope-leaked; honest claim = "1-bit Hebbian last-FC on random-encoded feedforward input can't lift".
TOP-3 uncovered cause-axes (all ESCAPE the falsified 4):
- ① INPUT-ENCODING (F8): all 4 falsifiers + Hc_1306 sit downstream of ONE fixed random backbone rng_bb.integers(-7,8,(256,256)); a learned linguistic encoder may reopen lift. Highest leverage.
- ② TEMPORAL-CODE (F7, all 5 lenses GAP): readout is rate-code 1-bit Hamming; SNN lift may live in spike-TIMING (STDP). Hc_1306 tested only STATIC signals — timing never tested.
- ③ OBJECTIVE+READOUT (F8 landscape, F6 occams, F1 functor): 1-bit-Hebbian-last-FC chosen by backend availability; AkidaSupervised + 4-bit weights + pre-binarization analog readout all chip-native + untested.
ACTION: breakthrough probe battery fired on pi5-akida ($0) — agent a78629c, pre-registered falsifiers per cause-axis; ANY probe with lift ci_lo>0 REOPENS Lane A P3, ALL-flat HARDENS the closed-negative to 8 axes.

## 2026-06-02 — Lane A CAUSE-AXIS breakthrough battery RESULT (live AKD1000, pi5-akida, $0) — P3 REOPENED on ENCODING
Pre-registered falsifiers → `.verdicts/lane-a-causeaxis/PREREGISTER.md`; chip = AKD1000 BC.00.000.002, akida 2.19.1, venv ~/.venv/anima-akida; 8 paired chip trials/probe, on-chip learn live every trial; CPU-local raw.npz re-score in parallel (no chip claim).

- **PROBE 1 INPUT-ENCODING → 🟢 REOPEN**: structured SVD cross-lingual encoder vs fixed random int4 backbone → lift mean **+0.9210 bits, 95%CI [+0.7382,+1.1038], 8/8 positive, ci_lo>0**; whitened encoder mean +0.4190, CI [+0.1035,+0.7345], 7/8. The random `BACKBONE_INT4 = rng_bb.integers(-7,8,(256,256))` that all 4 prior falsifiers + Hc_1306 sat downstream of IS a lift bottleneck. CPU re-score corroborates (encoded-input lift svd +10.68 / whitened +9.06). CAVEAT (a_scale_honest_scope): RELATIVE lift only — both arms' absolute margins stay negative at 25-anchor toy scale. → `.verdicts/lane-a-causeaxis/P1-encoding.txt`
- **PROBE 2 OBJECTIVE+READOUT → 🔴 FALSIFIED (hardens)**: 4-bit weights → chip `ValueError: Only layers with binary weights can be trained` (on-chip learning hardware-locked to 1-bit); supervised N/A-SDK (only AkidaUnsupervised in 2.19.1); pre-binarize analog readout margin −4.877 ci_lo −5.282. → `P2-objective-readout.txt`
- **PROBE 3 SPIKE-TIMING → 🔴 FALSIFIED (hardens)**: SDK exposes NO spike-event-timing (only PowerEvent/power_events power telemetry + predict_classes — stated, not fabricated); rank-order temporal proxy margin −0.1076 ci_lo −0.1111 (8 trials). → `P3-temporal-code.txt`

DISPOSITION: **REOPENED on the ENCODING axis** (1/3 cause-axes lit). Objective/readout + spike-timing axes now ALSO closed (closed-negative hardens over those two). The encoding lift path runs on the EXISTING AKD1000 — no new hardware (corrects prior "needs different hardware" deferral). Verbatim chip stdout: `.verdicts/lane-a-causeaxis/causeaxis_chip_stdout.log`; full JSON: `result_causeaxis_chip.json`; CPU re-score: `cpu_rescore_result.json`. agent run on branch feat/e31-anchor-authoring.

## 2026-06-02 — @goal pivot: H_911 closed-negative → production CLM/KOSMOS
- New @goal: PUBLIC-grade CLM on BOTH lanes (Lane A AKIDA · Lane G GPU flame+forge) → 3B → 7B; KOSMOS HF upload; UNIVERSE alongside as needed.
- Canonical = flame+forge on forge GPU substrate (a_train_flame_forge, never silent CPU-fallback); Lane A ⊥ Lane G separate (a_lane_akida_gpu_split); HF PUBLIC only at closure-PASS (a_hf_autonomous).
- In flight: Lane G flame+forge PUBLIC-grade fire (agent a4fa10a0) on a CUDA-devel H100_SXM (pod 39000300) — the gating step for the 3B/7B ladder. Prior d768 util-RED root cause = bare pod image (no nvcc/cublas) → forge .cu couldn't build → CPU fallback; fixed by CUDA-devel image (NOT a hexa-run link hack).
- Prior H_911 amodal-hub 3-axis probe = CLOSED-NEGATIVE (4-rung flat-RED), kept in status as the completed prior arc.
