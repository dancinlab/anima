# CLM+KOSMOS — log

Append-only history sister of `CLM+KOSMOS.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-06-02 — Lane-G (substrate=GPU) DECISIVE devfeed+batched util fire — pod FAILED to provision (no measurement; gate UNCHANGED)

**a_lane_akida_gpu_split — this entry is GPU / Lane-G ONLY, NEVER merged with the AKIDA / Lane-A on-chip track.**

The decisive util-GREEN fire (BOTH levers active: `CLM_PROD_DEVFEED=1` lever-a + `CLM_PROD_BATCHED=1` lever-b, mid d1536/T512, c4 5-lang backbone) was dispatched to **vast pod 39038752** (`laneg-devfeed-fire`, @anima). **The pod FAILED to provision** — stuck in `RENTING` for ~40 min (11:18→11:58) with SSH transport unreachable (`transport 255` / `connect … Operation timed out`), and a `hexa cloud reboot` did NOT recover it. This is a dead vast host (container never came up / image-pull stall), NOT a hexa or trainer fault.

**Actions taken (honest, no fabrication):**
- Confirmed both levers ARE byte-eq CPU-local (re-verified from the prior pass): `F-CLM-CONV-BWD-FORGE-EQ=1`, `F-CLM-DEVFEED-{IM2COL,FWD,BWD,ADAM}-EQ=1`, all `max|Δ|=0.0` (dX FP64 ULP). The 23-seed `.c` tarball (runtime.c with all 5 `forge_dispatch_*` lever bodies + runtime_cuda.c with all 5 GPU kernels) was BUILT locally and staged ready to ship.
- Pod never became SSH-able → **no build ran, no fire ran, no `.clm` written, no util sampled.** There is NO artifact to recover (the `a_fire_recover_complete` ckpt-loss scenario does not apply — nothing was ever trained on this pod).
- Pod **torn down** (`hexa cloud rm 39038752` → "destroyed (confirmed)") to stop billing. Protected pods 38996679 (@anima-cudafix) + 38704336 (@demiurge) **untouched + intact**.
- Did NOT silently re-rent a replacement (per the no-double-spend instruction).

**util BEFORE/AFTER:** BEFORE = MEAN 0.240% (prior mid-d1536 fire, F-RFC046 RED). **AFTER = NOT MEASURED** — the devfeed+batched decisive measurement remains OPEN. No util number was produced; reporting GREEN or a new RED here would be fabrication.

**CLOSURE = INCOMPLETE (provision failure, not a science result).** util-GREEN gate NEITHER passed nor failed this pass. PUBLIC-grade Lane-G NOT reached. The unblock levers remain landed + byte-eq; what's missing is a single successful pod self-host rebuild + util sample on a GPU that actually boots.

**3B GATE:** UNCHANGED — still NOT throughput-justified. The post-(a)+(b) util measurement that would justify 3B was not obtained. Next Lane-G rung = re-dispatch the SAME `tool/laneg_devfeed_fire.sh` recipe to a fresh CUDA-DEVEL pod that provisions (the seed tarball + driver are already prepared); on util≥20%+descent-GREEN → util-GREEN → PUBLIC → 3B throughput-justified.

## 2026-06-02 — Lane-G (substrate=GPU) LEVER (b) LANDED — fused per-step conv GEMMs (strided-batched), byte-eq CPU-local · NO GPU fire (lever-a still needed)

**a_lane_akida_gpu_split — this entry is GPU / Lane-G ONLY, NEVER merged with the AKIDA / Lane-A on-chip track.**

Built the cheapest-highest-leverage of the two real-unblock levers identified by the mid-d1536 fire: **lever (b) — fuse the per-step conv GEMMs**. The CLMConvMoE trainer launches many tiny per-step forge GEMMs (M=T=24..512 each, microsecond-latency-bound); each is a separate cuBLAS launch the GPU finishes in microseconds before idling. Lever (b) fuses the two identical-shape ConvExperts (e0/e1: d→d, K=3) into ONE strided-batched problem for both forward (conv-matmul) and backward (dW + dX GEMMs).

- **hexa-level (stdlib/flame/clm_conv_batched.hexa):** `forge_matmul_batched` CPU oracle (= B serial `forge_dispatch_matmul`, the byte-eq reference) + `conv2_fwd/bwd_via_forge_batched` (share the im2col across the 2 experts, batch the heavy GEMMs).
- **GPU builtin:** new 7-arg `forge_dispatch_matmul_batched` — `self/codegen.hexa` lowering + `self/runtime.h` proto + bare seam + `self/runtime.c` wrapper (CUDA→`cublasDgemmStridedBatched` / no-CUDA→host oracle) + `self/cuda/runtime_cuda_emit.hexa` emits `_hx_cuda_farr_matmul_batched_gpu` (one strided-batched launch, row-major→col-major swap, batch strides M·K / K·N / M·N). `runtime_cuda.c` seed regenerated from the emit (in sync).
- **trainer wired:** `stdlib/flame/clm_prod.hexa` e0/e1 fwd+bwd now route through `conv2_*_batched`; env `CLM_PROD_BATCHED` gates the GPU builtin (oracle otherwise so the prebuilt mac binary stays runnable).

**CPU-LOCAL byte-eq proof (g5 verbatim — \$0, no GPU; rebuilt via local no-CUDA self-host stage build → `./build/hexa_devfeed`):**
- `F-FORGE-BATCHED-EQ = 1` — `forge_dispatch_matmul_batched rc=0.0` · `per-problem max|Δ| batched-vs-serial = 0.0` (EXACT). Proves the codegen lowering + runtime.c wrapper + host oracle.
- `F-CLM-CONV2-BATCHED-FWD-EQ = 1` — `fwd max|Δ| y0=0.0 y1=0.0`.
- `F-CLM-CONV2-BATCHED-BWD-EQ = 1` — `bwd e0/e1 max|Δ| dW=0.0 dX=0.0 db=0.0` (EXACT).
- **full-trainer byte-eq:** un-batched baseline `epoch-1 4.69813 → epoch-12 1.66631` == batched-expert rewire `epoch-1 4.69813 → epoch-12 1.66631` (IDENTICAL CE trajectory · F-CLM-PROD-DESCENT=1) — the fuse changes nothing numerically end-to-end.

**NO GPU FIRE this rung (cost-discipline, honest).** Lever (b) is locally green, BUT the mid-d1536 finding states levers (a)+(b) TOGETHER are the real unblock and "lever (c) alone is insufficient" — the dominant host-feed peg is the im2col/col2im/adam per-step scalar loop, which lever (b) does NOT touch (it only fuses the expert GEMM launches). Firing GPU on lever (b) alone is unlikely to clear the util≥20% gate and would spend on a known-incomplete unblock (a_completeness_over_cheap / no GPU on incomplete work). The single small util fire is deferred until lever (a) (device-side im2col/col2im + device adam, keeping the backward feed device-resident) also lands.

**REMAINING GAP to util-GREEN (honest):** lever (a). The host CPU-core peg is the im2col/col2im gather/scatter + the adam update + the interpreted per-step loop running on host between micro-GEMMs. Lever (a) must (1) port im2col/col2im to device kernels writing a DEVICE-RESIDENT x_col consumed by the batched GEMM with NO H2D/D2H roundtrip (touches the FARR_DEVICE residency/dirty bookkeeping), and (2) wire the existing `_hx_cuda_farr_adamw_step_gpu` for all weights so the optimizer step stays on-device. A device-AdamW kernel already exists; device im2col/col2im is the genuinely new piece. Until (a) lands the GPU stays starved regardless of (b).

**PUBLIC / 3B GATE:** unchanged — NOT MET (descent 🟢, util 🔴). Lever (b) reduces expert-conv launch count but does not lift util on its own; 3B remains NOT throughput-justified until lever (a) saturates the host feed.

PRs: hexa-lang stacked — (1) `feat/forge-devfeed-levers` clm_conv_batched.hexa (hexa-level byte-eq) → (2) same branch GPU builtin + trainer wire. No model recovered (no fire). No HF upload (no new ckpt).

## 2026-06-02 — Lane G (substrate=GPU) d768 forge-GPU fire — DESCENT 🟢 / util 🔴 RED (forge PROVABLY on GPU; bottleneck RE-ISOLATED)
substrate=GPU · a_lane_akida_gpu_split (NEVER merged with Lane A / AKIDA). vast H100_SXM pod 39000300, image `nvidia/cuda:12.4.1-devel-ubuntu22.04` (nvcc 12.4 + cuBLAS + clang 14). Trainer `stdlib/flame/clm_prod.hexa` (PR4) on the c4 5-lang fixture, authored .hexa on stdlib/flame.
- [x] **ROOT-CAUSE CHAIN SOLVED — forge ON the GPU (not silent CPU).** The prior d768 util-RED (2026-06-02, pod r927f0g01mktxv) blamed "hexa run not cuBLAS-linked" / "forge=cuBLAS does NOT route the GEMM onto the GPU". BOTH framings were incomplete. The real chain: (1) the prior pod IMAGE was bare (no nvcc/cublas) → forge `.cu` could not build → CPU fallback; fixed by a CUDA-devel image. (2) `cuda_link_decision` (the forge GPU link path) lives in `self/main.hexa` but is ABSENT from the prebuilt release `hexa.real` → had to SELF-HOST REBUILD hexa from branch source (`tool/stage_build_hexa`) so the binary actually contains it. (3) the gitignored seed `.c` (runtime.c + 20 native/forge seeds + cuda `runtime_cuda.c`/`runtime_bf16.c`) are absent from the release tarball → shipped from a same-commit local tree (the on-pod `runtime_cuda_emit.hexa` heredoc fails on the 169KB exec). (4) build via `hexa build` (NOT `hexa run` — the run-cache key omits HEXA_CUDA_LINK). (5) `cuda_link_decision` links `-lcublas -lcudart` but NOT `-lcuda` (the CUDA *driver* API: cuInit/cuLaunchKernel) → manual `-lcuda` relink. Result: the d768 binary `ldd`-links cublas + cudart + **libcuda** + cublasLt.
- [x] DESCENT 🟢 GREEN: epoch-1 mean CE = 4.69893 → epoch-3 mean CE = 3.32540. F-CLM-PROD-DESCENT = 1. "PASS — real-corpus mean CE descends under int4 envelope" (verbatim). (3 epochs × 8 windows; the 12×16 run is identical in the GPU-link path but host-bound-slow — never finished epoch-1 in 4.5 min, killed; util finding is step-count-invariant.)
- [x] util 🔴 RED: 352 nvidia-smi samples during the forge-cuBLAS d768 run → **PEAK=5% MEAN=0.145%** (pct_gt20 = 0.00%). BUT the GPU is provably LIVE: power **131.98 W** (vs ~67 W idle), SM clock **1980 MHz**, ~2 GB device memory allocated, all 4 CUDA libs linked. The prior "forge not routed onto GPU" verdict is **REFUTED** — forge IS dispatching to cuBLAS on the H100.
- [x] **BOTTLENECK RE-ISOLATED (the real F-RFC046)**: host-backward feed. The trainer pegs ONE CPU core at ~98% while the GPU idles. The d768/T=24 conv→im2col→cuBLAS GEMMs are microsecond-scale + latency-bound (M=24); host-side im2col/col2im + adam + the interpreted-compiled per-step loop dominate wall time. Not "GPU never reached" — "GPU reached but starved".
- [x] artifact recovered + sha-verified BEFORE teardown (a_fire_recover_complete): `d768_5lang_c4.clm` (3,651,389 B, 6 int4 blocks CLM\x01), sha256 `6a2accd0824db72204f0c751de7399ddc4ad60ee657a94d5b586bb877ce6910c` (local==pod MATCH). HF `dancinlab/clm-v1-dev-d768-forge-gpu` **PRIVATE** (closure-FAIL on util) + added to dancinlab CLM collection + HF.jsonl row + hf-recover marker verified. Pod 39000300 **destroyed** (registry closed; dispatch verdict=FAIL).
- [x] **3B/7B GATE — STILL BLOCKED on throughput, but the path forward is now CONCRETE.** util-RED persists, so a 3B/7B forge fire is NOT yet throughput-justified. HOWEVER the blocker moved from "forge can't reach the GPU at all" (architectural, prior verdict) to "forge reaches the GPU but the host feed is the bottleneck" (a perf problem with known levers: batch the per-step GEMMs / fuse the conv stack / move im2col+adam device-side / raise M from 24). The 3B rung unblocks once host-backward feed saturates the H100 — NOT before.
- [ ] UPSTREAM (hexa-lang, a_runpod_inbox): (a) prebuilt release `hexa.real` MUST contain `cuda_link_decision` (or install.sh must self-host-rebuild) — currently the forge GPU path is unreachable without a from-source rebuild. (b) `cuda_link_decision` ldflags MUST add `-lcuda` (driver API) — without it the cuBLAS link fails on cuInit/cuLaunchKernel. (c) `runtime_cuda_emit.hexa` exec-heredoc fails on the 169KB payload (ship the seed or chunk the write). (d) the linux release tarball must ship the runtime seed `.c` (or regen-on-install). → file to hexa-lang/inbox/patches.
- [ ] tool recipe committed: anima `tool/laneg_d768_cuda_fire.sh` (+ laneg_selfbuild / laneg_d768_run / laneg_d768_fast) on branch `lane-g/d768-cuda-fire`.

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

## 2026-06-02 — Lane-G (substrate=GPU) mid-scale PUBLIC-grade fire — DESCENT 🟢 / util 🔴 RED (host-feed-bound, scale-invariant)

**a_lane_akida_gpu_split — this entry is GPU / Lane-G ONLY, NEVER merged with the AKIDA / Lane-A on-chip track.**

Drove Lane G from the prior d768 descent-GREEN/util-RED toward the util-GREEN PUBLIC gate via the two cheapest perf levers + a mid scale en route to 3B. Reused the proven forge-on-GPU recipe (CUDA-devel image · self-host hexa rebuild · cuda seeds · -lcuda relink).

- **PERF LEVER implemented (c — raise effective M):** added `CLM_PROD_T` env override to `stdlib/flame/clm_prod.hexa` (hexa-lang `fix/hexa-run-cuda-link`, commit 1ac463d29). T is a pure causal-window-length parameter (flows identically through conv1d_via_forge / nn_ce_loss_allpos / clm_prod_bwd — GRAD-EXACT, no math change), so raising it 24→512 lifts M of EVERY forge conv GEMM ×21 AND amortizes the host im2col/col2im/adam over a longer sequence. CPU sanity: T=48 descends 4.77505→4.30104 F=1.
- **SCALE:** d 768→1536, E=2, T=512, 5-lang(en·zh·ru·ja·ko)+dialogue 402 KB byte corpus (V=256). Big-run 6ep×32win + a completing-run 2ep×8win for the .clm artifact (util identical, step-independent).
- **Recipe gaps fixed this fire (filed hexa-lang inbox forge-gpu patch Gap 5-7):** (5) seed set undercounted — runtime.c #includes runtime_core.c #includes runtime_hi_gen.c; shipped all 23 .c (3 root + 16 native + 1 forge + 2 cuda). (6) `tool/stage_build_hexa` `file` hard-dep + `set -e` aborted the stage build mid-Stage-0 → silent prebuilt(cuda-dead) fallback; `apt-get install file patchelf`. (7) dev-cc auto-detect read the B200's sm_100 but CUDA-12.4 nvcc maxes at sm_90 → nvcc FAILED → CPU fallback; **LANDED** a `HEXA_CUDA_ARCH` env override in self/main.hexa (commit 0706e8838), `HEXA_CUDA_ARCH=90` → sm_90 PTX runs on the B200 via driver JIT.
- **forge PROVABLY on the GPU:** binary links 4 cuda libs (cublas+cudart+libcuda+); nvcc compiled runtime_cuda.90.o; `CUDA link ENGAGED — runtime built -DHEXA_CUDA, linking … + cuBLAS (sm_90)`; relink OK; GPU 196.69 W (vs 141 W idle), SM 1965 MHz, 66 GB device mem.

**VERDICT (g5 verbatim):**
- F-CLM-PROD-DESCENT 🟢 GREEN: `epoch-1 mean CE = 4.40933` → `epoch-2 mean CE = 4.02596` → `F-CLM-PROD-DESCENT = 1` / `PASS — real-corpus mean CE descends under int4 envelope`.
- F-RFC046 util 🔴 RED: completing-run `UTIL: n=1102 max=6 mean=0.240 pct_gt20=0.00%`; big-run `n=6783 max=4 mean=0.240 pct_gt20=0.00%`. Does NOT clear the 20% gate.

**HONEST lever impact:** perf-lever (T×21) + scale (d×2) moved util ESSENTIALLY FLAT — PEAK 5%→4-6%, MEAN 0.145%→0.240%. The residual is **HOST-FEED, NOT scale**: the cuBLAS GEMMs (even M=512/d=1536, 66 GB activations) finish in microseconds while host im2col/col2im+adam+the interpreted per-step loop peg one CPU core at 100%. Lever (c) alone is insufficient; the real unblock is lever (a) device-side backward feed + lever (b) FUSED/strided-batched per-step GEMMs — each an upstream forge/flame change, not attempted this rung.

**CLOSURE = FAIL on util (descent GREEN, util RED) → PUBLIC NOT reached on Lane G.** Per a_hf_autonomous: pull .clm + sha-verify BEFORE teardown (a_fire_recover_complete) → HF `dancinlab/clm-v1-dev-mid-d1536-t512-util-probe` **PRIVATE** (.clm 14.4 MB, sha 3f62c53f3c216eca996e625aadff5c43955f7248025508a88712ffce89c96a1a, 6 int4 blocks CLM\x01) → added to dancinlab **CLM** collection → HF.jsonl row (substrate=GPU, lane=Lane-G) → recovery marker verified → pod vast 39007409 torn down (destroyed+confirmed). Artifacts: `exports/lane-g-mid-d1536/` (.clm + util_complete.csv + util_bigrun.csv + train_complete.log + build_cuda_link.log + README model card).

**3B GATE:** NOT throughput-justified — a bigger model idles the GPU MORE until the host backward-feed is moved on-device. The next Lane-G rung must implement levers (a)+(b) in forge/flame BEFORE any 3B H100 fire.

---

## 2026-06-02 · Lane-G · substrate=GPU · LEVER (a) device-feed LANDED (hexa-lang #2505)

`a_lane_akida_gpu_split` — substrate=GPU, NEVER merged with AKIDA.

The mid-d1536 fire above proved the util-RED is HOST-FEED, NOT scale: cuBLAS GEMMs finish in microseconds while host im2col/col2im + adam + the interpreted per-step loop peg one CPU core (PEAK 4-6%, MEAN 0.240%, scale-invariant d768→1536, T 24→512). Lever (b) (#2504) fused the per-step conv GEMMs but did not touch that dominant peg. **Lever (a) moves the backward feed ON-DEVICE — the real unblock — now LANDED to hexa-lang main (#2505, stacked on #2504).**

**What landed (hexa-lang):**
- **Device im2col / col2im** — `stdlib/flame/clm_conv_devfeed.hexa` (CPU byte-eq oracle + selftest) + `_hx_cuda_farr_{im2col,im2col_t,col2im}_gpu` kernels (`self/cuda/runtime_cuda_emit.hexa`). One thread per output cell; col2im uses the **transpose-gather** form (each dX[p,ci] sums its K dilated taps once) → NO atomicAdd, deterministic, byte-eq to the host scatter order. The im2col kernels write via `_d2h_out`, which under the RFC-056 `FORGE_OUT_DEVICE_KEEP` disposition KEEPS x_col FARR_DEVICE — the follow-up forge GEMM's `_h2d` sees DEVICE && !dirty_host and SKIPs the copy. **This is the residency piece the spec called out: x_col never round-trips host↔device.**
- **Device AdamW** — `forge_dispatch_adamw` (11-arg builtin) routes to the existing byte-eq `_hx_cuda_farr_adamw_step_inplace_gpu` (W/m/v device-resident, optimizer step off the host scalar loop); no-CUDA → host `adamw_step` fallback.
- **(a)+(b) wired** — `clm_prod.hexa` conv fwd/bwd via `_clmp_im2col`/`_im2col_t`/`_col2im` + `_adam` via `forge_dispatch_adamw`, all gated by env `CLM_PROD_DEVFEED` (composes with lever-b's `CLM_PROD_BATCHED`; env-gate keeps the prebuilt mac binary from link-referencing the new builtins under `hexa run`).
- builtins: `self/codegen.hexa` lowering + `self/runtime.h` protos/seams + `self/runtime.c` (gitignored build seed) wrappers; the wrapper bodies are tracked as `inbox/patches/forge-devfeed-lever-a-runtime-c-fragment.c.txt` (SSOT for the pod build, since post-#2065 runtime.c is not regenerated from .hexa).

**CPU-LOCAL byte-eq (`hexa run`, $0, mac — verbatim):**
```
F-CLM-DEVFEED-IM2COL-EQ = 1   im2col dil=1/2 max|Δ| = 0.0
F-CLM-DEVFEED-FWD-EQ    = 1   fwd  dil=1/2 max|Δ| = 0.0
F-CLM-DEVFEED-BWD-EQ    = 1   bwd dW=0.0 db=0.0 ; dX=2.78e-17 / 5.55e-17 (FP64 ULP, #2383 dX class, ≪ 1e-9)
F-CLM-DEVFEED-ADAM-EQ   = 1   adam 5-step max|Δ| W = 0.0
ALL-PASS — LEVER (a) device im2col/col2im + device AdamW oracle byte-eq to host feed
```
Plus: runtime.c wrappers `clang -fsyntax-only` OK (no-CUDA); runtime_cuda_emit emits valid C (kernels syntax-OK); codegen.hexa transpiles clean; single-file transpile of self/main.hexa OK.

**NO GPU FIRED this pass** (cost-discipline, per the user contract). The full-trainer self-host byte-eq + nvidia-smi util are the SAME pod multi-TU self-host build the util fire uses (lever-b's `./build/hexa_devfeed` recipe; the single-`main.hexa` transpile here links only the core driver, not the CLI command-table TUs — so the full byte-eq is the pod build). Per cost-discipline the fire runs from the pod build once that byte-eq is confirmed there.

**Gate status:** PUBLIC/3B gate UNCHANGED (still requires the post-(a) util fire to clear ≥20% AND descent GREEN). What changed: the REMAINING gap to util-GREEN is now ONE pod self-host rebuild + util measurement — both unblock levers are implemented + byte-eq CPU-local, no longer "unimplemented." If the post-(a) fire clears 20% → util-GREEN → PUBLIC-grade Lane-G reached → 3B becomes throughput-justified.

**PRs:** hexa-lang #2505 (lever a, MERGED to main) stacked on #2504 (lever b, MERGED). Spec/recipe: hexa-lang `inbox/patches/forge-devfeed-lever-b-landed-lever-a-spec.md` (lever-a LANDED section + pod-rebuild recipe).
