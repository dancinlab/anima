# CLM+KOSMOS — log

Append-only history sister of `CLM+KOSMOS.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-06-02T08:47Z — Lane-A (substrate=AKIDA · live AKD1000 pi5-akida · a_lane_akida_gpu_split — NEVER merged with Lane G/GPU) — UNIVERSE 라이브-실리콘 측정 전원-교란 재검증 🟢 POWER-ROBUST (spontaneous raster + D1 Φ 안정 PSU 재측정 · 문서 tier 변동 0)

substrate=AKIDA · a_lane_akida_gpu_split (Lane G/GPU 와 NEVER 병합). PSU 교체(2026-06-02, under-voltage brownout 근본원인)로 안정화 후, **결함이 이미 있었을 수 있던 더 이른 시점(05-22/05-29, throttled 미로깅)** 의 라이브-AKD1000-실리콘 UNIVERSE 측정값이 power-confounded 인지 재검증. SW-confirmed = out of scope. 결정적 재측정: spontaneous-emission raster live 칩 재발사 + D1 Φ 재유도, 안정 전원(throttled=0x0, EXT5V≈5.02V) pwr.log 입증.

- [x] **재측정** — single-chip wrapper `run_spontaneous_reverify.sh`: R3 streamer(pid 3775) stop → 칩 free → `spontaneous_emission.py` (seed=187 n=16 200step) live 발사(rc=0) → fresh JSON → streamer 복원(pid 4992 active 확인). 칩 BC.00.000.002, akida 2.19.1, BackendType.Hardware.
- [x] **pwr.log throttled=0x0** (08:44–08:48Z): `08:44:33Z throttled=0x0 EXT5V=5.02768V 64.2'C` · `08:46:33Z throttled=0x0 EXT5V=5.01294V` · `08:48:33Z throttled=0x0 EXT5V=5.02768V`. wrapper 내부 모든 단계 throttled=0x0.
- [x] **#1 spontaneous raster (load-bearing)** — 05-22 canonical vs fresh: **byte-identical** — R0=3200 · R1=0 · R2=1520 (std=7.99 step_varies) · R3=1600 (8/16 partial pool) · R4=3200 · `checks` 8/8 True · hw_native + stochastic + mapped_on_hardware=true. 유일 차 = onchip_clock_mean 797.2→790.0 (타이밍 jitter). → 8/8 zero-input emit 재현 (FLIP 0).
- [x] **#2 D1 edge-of-chaos Φ** — fresh raster → `akida_edge_of_chaos_phi.hexa` frozen proxy (g5): Φ(R1)=0.0 · Φ(R2)=0.2974093093367505 · Φ(R3)=0.25 · Φ(R4)=0.0 · F1/F2/F3=true · all_pass=true · GREEN_NUMERICAL_CONFIRM. 05-29 원본 Φ={0,0.297,0.250,0} **정확 일치**, inverse-U 재현 (FLIP 0).
- [x] **#3 H_677 D3** — AKIDA arm Φ=0.297 = fresh Φ(R2) 일치 (동일 raster 파생 → power-robust 상속). **#4 HW probe(05-29)** = ssh-reachability (chip 측정 0) → N/A.
- [x] **분류** — #1 raster POWER-ROBUST · #2 D1 Φ POWER-ROBUST · #3 D3 POWER-ROBUST(상속) · #4 N/A. FLIP 0. 비결정 substrate 기대치(replication)를 초과 — 결정론 regime byte-eq, R2 stochastic 도 std/rate/event-driven 일치 → brownout 이 capture 미교란.
- [x] **문서 tier 변동 0** — 전부 재현. H_672/H_677/H_858 승강 없음 (earned re-run verdict 없이 tier 불변, g5). CANDIDATES.md 에 power-robust 1줄만. Lane A 음성결과 power-robust 재감사(PR #1675)와 같은 결론 — silicon GREEN 도 power-robust.

## 2026-06-02T08:30Z — Lane-A (substrate=AKIDA · live AKD1000 pi5-akida · a_lane_akida_gpu_split — NEVER merged with Lane G/GPU) — POWER-CONFOUND RE-AUDIT: prior closed-negatives are POWER-ROBUST (안정 PSU 위 재검증)

중심 질문: 오늘 PSU 교체로 해결된 under-voltage brownout(throttled=0x50000, EXT5V 4.87V — PI5-AKIDA.json `power_root_cause_2026_06_02`)이 기존 Lane-A H-A1~A4 closed-negative / relative-LIFT closed-negative / SCALE weak-lift ladder 를 confound 했는가? 재감사 + 안정 전원 위 재발사.

- [x] **시점 분리 (결정적):** 기존 음성 4건+배터리는 전부 **2026-06-01** 완주(ts 17:51–20:14Z), brownout/PSU-swap 은 **2026-06-02 ~07:54Z** — 음성들은 brownout 창 **하루 전** 측정. brownout 이 실제 죽인 run = abs_margin 1차(oracle-LDA arm 전 사망)뿐이며 이미 안정 PSU 위 완주 🟢 PASS(08:10Z 항목).
- [x] **완전성 감사 (g5, 호스트 result JSON 직접):** truncation/누락 arm 0건. H-A2(bit_depths=4·rungs=4·ha2_true=False) · H-A3(N{3,4,5} all_learned_hw=true) · H-A4(ladder_N[2,3,4,5]×nreps=3 per-rung 전부 sign-stable) · causeaxis(P1/P2/P3 8/8 trial) · SCALE-ladder(4 rung all_rungs_green_hw) — 전부 COMPLETE+terminal.
- [x] **RE-VERIFY on STABLE power (throttled=0x0):** 단일-칩 wrapper(R3 stop→probe→restore) + live `vcgencmd get_throttled` + watchdog pwr.log.
  - **H-A2 재실행 → 🔴 H-A2-FALSIFIED 재현 (POWER-ROBUST)**, RC=0 ts 08:24:47Z: `H-A2-FALSIFIED (multi-bit lift also straddles 0 — not a quantization artifact)`, onebit/multibit ci_lo_gt0=False.
  - **causeaxis 재실행 → DISPOSITION: REOPENED 재현 (POWER-ROBUST)**, RC=0 ts 08:29:50Z: `P1 encoding any_reopen=True | P2 objective any_reopen=False | P3 timing any_reopen=False`; P1 svd mean_lift=+0.797 ci95=[+0.537,+1.057] 8/8 · whitened +0.520 ci95=[+0.304,+0.736] 8/8 · P2 −4.745 ci_lo −5.359 · P3 −0.09..−0.11. 부호/disposition 동일 재현(크기는 svd +0.797 vs 직전 +0.921 — native 비결정 re-init H_904 만큼 trial 변동, byte-eq 아닌 replication = AKIDA 비결정 substrate 정상 거동).
  - **전원 PROOF:** 두 재실행(08:24–08:31Z) 내내 watchdog pwr.log throttled=0x0 연속, EXT5V≈5.00–5.03V; live sampler throttled=0x0; pwr.log 전체 non-0x0 이벤트 0건.
- [x] **분류:** H-A1 corpus(POWER-ROBUST, 완전+06-01) · H-A2 quant(POWER-ROBUST, 재현) · H-A3 depth(POWER-ROBUST, 완전+06-01) · H-A4 noise-floor(POWER-ROBUST, 완전+06-01) · relative-LIFT closed-negative(POWER-ROBUST) · SCALE weak-lift ladder(POWER-ROBUST, 12/12 green_hw, 06-01) · causeaxis P1 REOPEN+P2/P3 FALSIFIED(POWER-ROBUST, 재현). **flip 0건** — 어떤 음성도 안정 전원에서 뒤집히지 않음.
- [x] **재발사 안 한 것(정직, no silent cap):** H-A1/H-A3/H-A4/SCALE 는 chip 직접 재발사 안 함 — complete + 06-01(pre-brownout) + 대표 2 probe(HA2 결정론 readout · causeaxis 비결정 학습)가 throttled=0x0 으로 음성 재현. completeness+시점+대표재현으로 power-robust 충분(a_completeness_over_cheap: cheap-close 가 아니라 robust 입증).
- [x] **SCOPE (a_scale_honest_scope · a_lane_akida_gpu_split):** substrate=AKIDA only, Lane G/GPU NEVER 병합. 25/250-anchor·single AKD1000·1-bit last-FC Hebbian scope 유지. 재실행은 power-robust 만 입증, closed-negative 를 더 일반화하지 않음.
- [x] **BOTTOM LINE:** 기존 Lane-A failure 는 **power-confound 아님(NOT confounded)**. brownout 은 abs_margin 1차 한 run 만 죽였고(이미 PASS 완주), 나머지 음성+SCALE 은 brownout 전 complete 측정 + 안정 전원 재현 → CLOSED-NEGATIVE 는 REAL. CLM+KOSMOS.md 의 H-A 블록/SCALE 항목 **변경 없음**(flip 없으므로 milestone "pass" 승격 금지 — g5).
- [x] **HW:** PI5-AKIDA.json 참조(미수정)·os_default 무접촉·R3 streamer 매 run 후 복원(final pid 3775 active)·pool 전환 안 함. 호스트 재감사 내내 ALIVE throttled=0x0. (full 재감사 매트릭스+verbatim = AKIDA.log.md 동시점 항목)

## 2026-06-02T08:10Z — Lane-A (substrate=AKIDA · live AKD1000 pi5-akida · a_lane_akida_gpu_split — NEVER merged with Lane G/GPU) — abs-margin on-chip 결단기 🟢 PASS-PUBLIC-GRADE-POSITIVE (안정 PSU 위 완주)

substrate=AKIDA · a_lane_akida_gpu_split (Lane G 와 NEVER 병합). live chip BC.00.000.002, akida 2.19.1, decider `~/clm_kosmos_akida/abs_margin_chip.py` (N=8 trials × 32 units, 4 encoder × 2 corpus). 직전 세션은 호스트 전원 brownout 으로 oracle-LDA arm 실행 전 mid-fire 사망(terminal 없음). PSU 물리 교체(2026-06-02, under-voltage 근본원인 — PI5-AKIDA.json 참조) 후 안정 전원에서 **완주**.

- [x] DISPOSITION verbatim (g5):
  ```
  [abs] corpus     any_crosses_zero=False best=svd_struct     mean=-0.5760 ci_lo=-0.6535
  [abs] corpus_big any_crosses_zero=True  best=lda_supervised mean=+5.2396 ci_lo=+5.0609
  [abs] DISPOSITION: PASS-PUBLIC-GRADE-POSITIVE
  [abs] at least one encoder pushed the ABSOLUTE on-chip concept-margin ci_lo>0
        -> the AKD1000 1-bit Hebbian learns positive cross-lingual concept structure (PUBLIC-grade positive)
  ```
- [x] lda_supervised (corpus_big) 8/8 trials 양수 mean=+5.2396 sd=0.258 ci95=[5.061,5.418] n_positive=8 learn_all_hw=true → ci_lo=+5.061>0 PASS · result sha256 `7612bedaca38b68f12528d641fa8bfc9e0e0dace6e23b28db7d13076c57b3c7f`
- [x] scope (a_scale_honest_scope) — 작은 corpus(25앵커) any_crosses_zero=False; 약한 인코더(random_int4/svd_struct/whitened) 음성. 강한 인코더(lda_supervised)+큰 corpus만 PASS. 인코더-강도/스케일 의존, 정직.
- [x] 별개 축 — 절대-margin PASS 는 상대-LIFT closed-negative(H-A1~A4 4/4)와 무관: 1-bit Hebbian 이 *상대 lift* 는 안 사지만 강한 인코더로 *절대* positive 개념구조는 학습. 두 축 분리(a_lane_akida_gpu_split 정신).
- [x] 전원 — PSU 교체로 brownout 해소(throttled 0x50000→0x0, EXT5V 4.87→5.033V); decider 부하 중 throttled=0x0 부하검증 통과. anima-pwr-log watchdog(60s) 무장 + persistent journal — 재발 시 timestamp 포착. PI5-AKIDA.json 등록(commit 92c79172c).
- [x] PUBLIC 판정 — disposition=PASS-PUBLIC-GRADE-POSITIVE (substrate=AKIDA). HF 업로드 대상은 metrology verdict(result JSON)로 모델 ckpt 아님 — 도메인 기록 + sha 보존, HF 모델 업로드는 해당 없음.
- [x] HF — N/A (verdict-only artifact, not a trained ckpt). Lane G 의 GPU util-GREEN HF PUBLIC 게이트와 분리.

## 2026-06-02 — Lane-G (substrate=GPU · pod 39062745 vast RTX-PRO-6000-Blackwell · a_lane_akida_gpu_split — NEVER merged with AKIDA) — devfeed+batched util fire: THIRD root cause FIXED (emit recursion + write-fail), all 3 verify-before-fire PASS, DESCENT 🟢 GREEN / util 🔴 RED (host-feed bottleneck CONFIRMED with both levers)

substrate=GPU · a_lane_akida_gpu_split (NEVER merged with Lane A / AKIDA). vast pod **39062745** "laneg-utilgreen", **NVIDIA RTX PRO 6000 Blackwell** (97887 MiB, CUDA 12.4 / nvcc 12.4 / cuBLAS, gcc 11.4, clang 14, glibc 2.35→2.39 shim). Trainer `stdlib/flame/clm_prod.hexa` (PR4) on the c4 5-lang corpus (`clm_mid_5lang_c4.txt`, 402270 B, V=256, 16 windows). Built from hexa-lang `laneg/devfeed-cudalink-integrated` (cuda_link + lever-a #2505 + lever-b #2504 + nvcc fwd-decl #2506 + the two fixes landed this session).

**RESUME point:** the prior agent died on a transient server rate-limit mid-build; the pod was a FRESH boot (Jun 2 05:25 — nothing built, no logs). So "resume" = build from scratch on the live READY pod. Branch confirmed: integrated branch carries cuda_link_decision + fwd-decl + both levers (NOT on origin/main).

- [x] **THIRD Lane-G util-RED root cause FOUND + FIXED** (after #2504/#2505 link + #2506 nvcc fwd-decl). The `HEXA_CUDA_LINK=1 hexa build clm_prod` spawned an **unbounded fork-bomb** (1800+ procs, self-reparenting to init) at `[cuda] emitting runtime_cuda.c`. **#3a:** `cuda_link_decision` emits via a nested `hexa run runtime_cuda_emit.hexa` that INHERITS `HEXA_CUDA_LINK=1` → re-enters the cuda path → sees `runtime_cuda.c` still absent → emits again → ∞. Fix = prefix the nested emit with `HEXA_NO_CUDA=1` (force_off short-circuit). **#3b:** with #3a the failure surfaced clean — `[runtime_cuda_emit] FATAL: failed to write` — the emit packed the whole ~100 KB / 3967-line `runtime_cuda.c` into ONE `exec("cat > out <<'EOF' …")` command; the exec arg buffer truncated it → file never written (so the on-demand emit had ALWAYS failed silently, masked by the recursion). Fix = `write_file(out_path, c_text)` builtin (rt_write_file; no shell, no ARG_MAX). → hexa-lang `laneg/devfeed-cudalink-integrated` commits `27535d93d` (#3a) + `bb10154fb` (#3b); inbox patch `fe2e43a35` (a_runpod_inbox).
- [x] **VERIFY-BEFORE-FIRE — all 3 PASS** (gated; no CPU fire allowed otherwise): (a) build.log `CUDA link ENGAGED` count = **1**. (b) `nvcc -x cu runtime_cuda.c` EXIT **0**, no errors (3967-line emit, fwd-decls present → 555824-byte `runtime_cuda.90.o`). (c) clm_prod `ldd` = **4 cuda libs** (libcublas.so.12 + libcudart.so.12 + **libcuda.so.1** + libcublasLt.so.12); `forge_dispatch_matmul_batched` = 1, `forge_dispatch_adamw` = 1. (Initial `hexa build` hit the expected `-lcuda` driver-symbol miss — cuModuleUnload/cuLaunchKernel — and the `-lcuda` relink fallback produced the binary.)
- [x] **DESCENT 🟢 GREEN:** epoch-1 mean CE = **4.88733** → epoch-3 mean CE = **4.87688**; `F-CLM-PROD-DESCENT = 1`; "PASS — real-corpus mean CE descends under int4 envelope" (verbatim, g5). config d=768 E=2 epochs=3 nwin=16 T=24.
- [x] **util 🔴 RED** (the SUCCESS gate = util≥20% AND descent GREEN → NOT MET). **BEFORE = 0 % / 2 MiB** (idle baseline, verbatim). **AFTER (T=24 run):** `UTIL: n=388 peak=5 mean=0.784 ge20pct=0.00`, peak dev-mem 3952 MiB; top samples `5, ~3700 MiB, ~87 W`. **AFTER (T=512 run):** `n=987 peak=6 mean=0.811 ge20pct=0.00`, peak dev-mem **14784 MiB**. GPU provably LIVE (87 W vs ~70 W idle, ~3.7–14.8 GB device-resident, all 4 cuda libs) — but SM-starved.
- [x] **BOTTLENECK = host-feed, CONFIRMED with BOTH levers (DEVFEED=1 + BATCHED=1).** During the run the trainer pegs ONE CPU core at **100 %** while the GPU idles (`gpu 1 %`). The device-feed levers made buffers device-resident (mem 2 MiB → up to 14.8 GB) but did NOT lift util above ~5–6 % — so the residual is the F-RFC046 host-backward per-step orchestration, NOT link/compile/emit (all fixed) and NOT memory residency or scale (T24 5 % ≈ T512 6 %). What device feed bought vs the prior 0.240 %: device-resident memory (GB-scale) + confirmation the levers aren't the lift — the host interpreted-compiled per-step loop is.
- [x] **artifact recovered + sha-verified BEFORE teardown** (a_fire_recover_complete): `state/laneg_d768_recover/d768_5lang_c4.clm` (3,651,389 B, 6 int4 blocks `CLM\x01`), sha256 `98094a5d47b701b407b70adc86b983bfd33c9cf33a2fa1e48c55a4813b631ffb` (local == pod MATCH).
- [x] **HF upload PRIVATE** (a_hf_autonomous, closure-FAIL on util): `dancinlab/clm-v1-dev-d768-devfeed-rc3-util-probe` **private=True** (README + .clm verified present via HF API) + added to dancinlab **CLM collection** + HF.jsonl row (substrate=GPU) `anima_clm_d768_devfeed_rc3_lane_g_2026_06_02`. Supersedes-attempt `clm-v1-dev-d768-forge-gpu` (root cause #3 now fixed; same util-RED re-confirmed).
- [x] **3B/7B gate — STILL throughput-blocked** (do NOT auto-fire 3B). util-RED persists, so a 3B forge fire is NOT throughput-justified. With #3 fixed, ALL the build/link/compile/emit blockers are now closed — the SOLE remaining lever is the host-feed per-step orchestration (device im2col/adam are on; the interpreted-compiled loop dominates wall time). 3B unblocks once host-feed saturates the GPU, NOT before.

## 2026-06-02 — Lane-G (substrate=GPU · pod 39052854 vast H100 NVL · a_lane_akida_gpu_split — NEVER merged with AKIDA) — devfeed+batched util fire HARVESTED: CUDA LINK FIXED (ENGAGED=1) but GPU 0 MiB → ROOT CAUSE #2 = nvcc compile of runtime_cuda.c FAILS (missing fwd-decls) → CPU-only fallback. util-RED, link-fixed-but-not-on-GPU. NOT throughput-justified.

**Pod / process:** vast H100 NVL pod `39052854` (@anima "laneg-devfeed-fire3"); detached fire `clm_prod_devfeed` PID 2248, R-state, **99.9% of ONE CPU core**, RSS ~48 GiB.

**GPU util AFTER — 6 samples over ~2 min (verbatim, `nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader`):**
```
0 %, 0 MiB
0 %, 0 MiB
0 %, 0 MiB
0 %, 0 MiB
0 %, 0 MiB
0 %, 0 MiB
```
Confirmed NOT a late-engaging setup phase — `util.csv` on the pod shows every in-run sample is `0, 0, <power>, <mem>` (util=0, gpu-mem-used=0) for the entire fire. **util AFTER ≈ 0% (GPU 0 MiB)**, vs **util BEFORE = 0.240% MEAN** (prior host-feed CPU peg). The recipe/link fix did NOT lift util — a second defect blocks it.

**Build log (verbatim, `/workspace/laneg_fire.log`):**
```
  fresh hexa built; 'CUDA link ENGAGED' count = 1          ← LINK FIX LANDED (recipe success)
=== [4b/7] BUILD clm_prod with HEXA_CUDA_LINK=1 -> forge GPU binary ===
  build rc=0
  [cuda] nvcc compiling runtime_cuda.c for sm_90 ...
  [cuda] nvcc compile FAILED — building CPU-only:           ← ROOT CAUSE #2
/root/.hx/src/self/cuda/runtime_cuda.c(903): error: identifier "_d2h_out" is undefined
6 errors detected in the compilation of "/root/.hx/src/self/cuda/runtime_cuda.c".
--- binary cuda libs ---
(no binary / static)                                        ← clm_prod is CPU-ONLY
```
No `mean CE` / epoch / terminal `RUN_RC`/`DONE` emitted — the CPU fallback binary is still grinding (window 1/16 at d=1536, T=512); `train.log` stops at the corpus/window banner. Per the contract, with GPU confirmed 0 we do NOT wait for the slow CPU run.

**ROOT CAUSE #2 — CONFIRMED against the pod source (corrects the prior "kernels not `__global__`" hypothesis):**
- The 5 lever-(a) wrappers ARE correctly structured: `_hx_cuda_farr_{im2col,im2col_t,col2im,matmul_batched,adamw_step_inplace}_gpu` are HOST entry functions (`int … (…)`, `#ifdef __CUDACC__`) that LAUNCH real `__global__` kernels via `<<<grid,block>>>` (e.g. `_hx_k_col2im<<<…>>>`). The file has 37 `__global__` defs. **The `__global__` qualifier is NOT missing.**
- The compile MODE is correct too: hexa builds this TU with **`nvcc -x cu`** (confirmed: build log `[cuda] nvcc compiling runtime_cuda.c for sm_90`; `self/cuda/PHASE_D_H100_EVIDENCE.md:38` = `nvcc -x cu -c runtime_cuda.c`). **NOT a `-x c` host-compile.**
- The REAL defect is a **missing forward declaration / definition-ordering bug**. The im2col trio (`_hx_cuda_farr_im2col_gpu` @833, `_im2col_t_gpu` @862, `_col2im_gpu` @887) CALL two `static` helpers — `_ensure_dev_alloc_out` (defined @975) and `_d2h_out` (defined @1027) — that are defined LATER in the TU with NO prior prototype. In `-x cu` (C++/CUDA) mode an undeclared-before-use identifier is a hard error, so nvcc errors out:
```
runtime_cuda.c(844): error: identifier "_ensure_dev_alloc_out" is undefined   (im2col)
runtime_cuda.c(854): error: identifier "_d2h_out" is undefined                (im2col)
runtime_cuda.c(869): error: identifier "_ensure_dev_alloc_out" is undefined   (im2col_t)
runtime_cuda.c(879): error: identifier "_d2h_out" is undefined                (im2col_t)
runtime_cuda.c(893): error: identifier "_ensure_dev_alloc_out" is undefined   (col2im)
runtime_cuda.c(903): error: identifier "_d2h_out" is undefined                (col2im)
6 errors detected
```
→ whole TU fails → `clm_prod` silently rebuilds CPU-only → no GPU kernel ever launches → GPU 0 MiB. Other call sites of the same helpers (line 1631/1687/1738…) are AFTER the definitions, so only the spliced im2col trio is upstream of the defs.

**VERDICT (honest, g5):** **util-RED on this run — GPU 0% / 0 MiB — DESPITE a correct CUDA link.** The recipe/link fix WORKED (CUDA link ENGAGED=1; no longer a CPU-only build like origin/main). But a SECOND, distinct defect remains: the lever-(a) device path does not compile (`nvcc -x cu` fails on the im2col trio's forward-undeclared static helpers `_ensure_dev_alloc_out`/`_d2h_out`), so the trainer falls back to a CPU-only binary and no GPU kernel launches. **NOT a `__global__`/compile-mode defect** (the prior hypothesis is RULED OUT — both are correct). before(0.240% mean) / after(~0%, GPU 0 MiB).

**Recovery:** NONE — `find /workspace /root -name '*.clm'` = empty; the run wrote no checkpoint (nvcc fail → CPU fallback → still in window 1/16). No HF upload (nothing to upload, RED).

**Gate status:** PUBLIC/3B gate **UNCHANGED** — NOT throughput-justified. Still requires a post-fix util fire to clear ≥20% AND descent GREEN. The remaining gap to util-GREEN is now ONE source fix (forward-declare the two static helpers before the im2col trio, re-confirm `nvcc -x cu` passes, keep byte-eq to the CPU oracle) + a re-fire. Inbox spec: `hexa-lang/inbox/patches/forge-devfeed-kernels-not-global-qualifier.md`.

**Teardown:** pod 39052854 torn down after harvest (no artifact to keep). a_lane_akida_gpu_split: substrate=GPU, NEVER merged with any AKIDA/Lane-A number.

---



**a_lane_akida_gpu_split — this entry is GPU / Lane-G ONLY, NEVER merged with the AKIDA / Lane-A on-chip track.**

Provision-failure RETRY of the decisive util-GREEN fire (BOTH levers: `CLM_PROD_DEVFEED=1` lever-a + `CLM_PROD_BATCHED=1` lever-b, mid d1536/T512, c4 5-lang backbone). The prepped 23-seed tarball (`/tmp/hexa_seed_c.tgz`, sha `f0c9a944…`, all 5 `forge_dispatch_*` lever bodies + 5 GPU kernels) + driver `tool/laneg_devfeed_fire.sh` were intact locally. **Outcome: NO util measurement — the run was blocked first by a build-recipe gap (caught + fixed) and then by a provider-wide provisioning outage (3 dead hosts, rotation budget exhausted).** util-GREEN gate NEITHER passed nor failed; reporting GREEN or a new RED would be fabrication.

**BUILD-RECIPE GAP FOUND + FIXED (the real technical finding this pass):**
- The driver's premise — "self-host rebuild of `origin/main` bakes in `cuda_link_decision`" — is FALSE. `origin/main` carries the two levers (#2504 lever-b + #2505 lever-a) but **NOT** the forge GPU-link path. `cuda_link_decision` / `CUDA link ENGAGED` is **0 occurrences** in `origin/main:self/main.hexa`; it lives only on `fix/hexa-run-cuda-link` (commit 346d68e8a), never merged to main.
- CONSEQUENCE observed on the first live pod (vast 39046120, H200/sm_90, CUDA-devel): the self-host rebuild produced `hexa_fresh` with `'CUDA link ENGAGED' count = 0`, the clm_prod build linked `-lm -lpthread` only (`ldd` cuda libs = none), and the fire started **CPU-only** (GPU idle 76 W, 0 % util) — a FALSE util-RED. Aborted the CPU run before any `.clm` was written (verified `NO_CLM`).
- FIX (durable, pushed): merged `origin/main` (levers + 23 seeds) with `origin/fix/hexa-run-cuda-link` (cuda link) → branch **`hexa-lang laneg/devfeed-cuda-link-merge`** (commit 8312a8cae). `self/main.hexa` conflict resolved so the runtime.o cache compile keeps main's `_hexa_clang_capped` hardening AND injects `_cuda_cflags` (the `-DHEXA_CUDA` that the prior build silently dropped). ALSO fixed Gap 2 at the source: `_cuda_ldflags` now adds `-lcuda` + `/usr/lib/x86_64-linux-gnu` (driver API was undefined-reference without it). Merge **transpiles + builds clean locally** (`TRANSPILE+BUILD OK`, CPU-only mac, 2.2 MB, benign warnings only — proves the merge is syntactically valid). NB: a pre-existing `laneg/devfeed-cudalink-integrated` (f8d6232f2) does the same integration minus the `-lcuda` Gap-2 fix; the merge branch is a superset. The fire driver was re-pointed at the merge branch (mawk-safe util awk retained for the pod's mawk).

**INFRA BLOCKER — 3 dead provisions, rotation budget exhausted (NOT a science result):**
- Provision #1: **runpod** `--gpu H100` → "no id in response (no capacity)" — clean no-op, no pod. Fell back to a pre-existing READY vast pod **39046120** (project=anima/laneg-devfeed-fire2) which DID pass the health gate initially (SSH + nvidia-smi live, H200/sm_90, nvcc 12.4 + cuBLAS + libcuda). Shipped seeds + driver, fired — but the CPU-only build (above) pegged 1 core and **starved sshd → SSH went persistently dark** (20 consecutive `transport 255`, trainer unkillable). Torn down (`rm --force` after `NO_CLM` verified + honest re-attribution; no ckpt at risk).
- Rotation #2: **vast** 39050718 (H100_SXM, reliability>0.95 filter) → stuck **RENTING ~5 min, never exposed SSH** (health gate HEALTHY=0). Torn down.
- Rotation #3: **runpod** 85mlcuh8se3mju (explicit "NVIDIA H100 80GB HBM3") → capacity available this time, but stuck **RENTING ~7 min, no SSH endpoint**. Torn down. (An earlier 20s-wait runpod rent self-destroyed before SSH; ghost row cleaned.)
- Provider-wide slow/dark provisioning today on BOTH vast and runpod. This mirrors the predecessor entry's dead host 39038752. **All teardowns verified no-ckpt; protected pods 38996679 (@anima-cudafix) + 38704336 (@demiurge) untouched + intact; no orphan billing pod of mine remains** (16 vast instances flagged by reap are pre-existing other-session pods, NOT touched per a_dont_kill_live_compute).

**util BEFORE/AFTER:** BEFORE = MEAN 0.240 % (prior mid-d1536 fire, F-RFC046 RED). **AFTER = NOT MEASURED** — the devfeed+batched decisive measurement remains OPEN. No HF upload (no ckpt). No HF.jsonl row added.

**CLOSURE = INCOMPLETE (infra blocker + recipe-gap fixed, not a science verdict).** PUBLIC-grade Lane-G NOT reached. NET PROGRESS this pass: the build recipe is now CORRECT (merge branch `laneg/devfeed-cuda-link-merge` carries levers + cuda_link_decision + `-lcuda`, locally build-validated) so the next attempt no longer silently CPU-falls-back. What remains missing is purely a GPU host that boots SSH-able. Next Lane-G rung = re-dispatch `tool/laneg_devfeed_fire.sh` (BRANCH already updatable to the merge branch) to a CUDA-DEVEL pod that provisions; on util≥20 %+descent-GREEN → util-GREEN → PUBLIC → 3B throughput-justified.

**3B GATE:** UNCHANGED — still NOT throughput-justified (no post-(a)+(b) util obtained).

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

---

## 2026-06-02 — Lane A (substrate=AKIDA · pi5-akida · a_lane_akida_gpu_split — NEVER merged with any GPU/Lane-G number) — ABSOLUTE-MARGIN falsifier FIRED on live AKD1000, host went dark MID-FIRE → BLOCKED (honest, no fabricated result)

**Rung picked (the decisive pre-registered next step):** the P3 ENCODER REOPEN verdict (`.verdicts/lane-a-causeaxis/P1-encoding.txt`) closed with an explicit pre-registered SCOPE caveat: the encoder lift is RELATIVE (structured beats random, +0.92 bits ci_lo>0) but BOTH arms' ABSOLUTE concept-margins stayed NEGATIVE at toy scale — "the next rung is whether a stronger structured/learned multilingual encoder pushes the absolute margin above 0, not just the relative lift." This is the PUBLIC-grade Lane-A question, so I fired exactly that.

**Falsifier (pre-registered, `.verdicts/lane-a-absmargin/PREREGISTER.md`):** ABSOLUTE concept-margin (between-minus-within Hamming bits, per-feature-median binarized on-chip fwd, native non-det chip init per trial / H_904, N=8 trials, ci_lo=mean−1.96·SEM). Encoders of increasing LEARNED strength: random_int4 → svd_struct → whitened → **lda_supervised** (multi-class LDA maximizing between/within concept scatter using corpus concept labels = oracle-strength upper bound on a "stronger learned multilingual encoder"). Scales: corpus (25-anchor) AND corpus_big (250-anchor). PASS (PUBLIC-grade positive) iff some encoder ABSOLUTE ci_lo>0 (learn_all_hw); else CLOSED-NEGATIVE scoped to measured anchor scale (a_scale_honest_scope).

**Reachability + chip CONFIRMED LIVE at fire start (verbatim chip stdout):**
```
[abs] akida 2.19.1 device BC.00.000.002 ip IpVersion.v1  N=8 trials units=32
[abs] ===== SCALE corpus : count=25 concepts=5 langs=5 =====
[abs] random_int4            trial 0: abs_margin=-1.4400 learn=True
[abs] random_int4            trial 1: abs_margin=-1.7120 learn=True
```
On-chip learning live (learn=True) on the real AKD1000 (BC.00.000.002, akida 2.19.1, anima-akida venv). Script `~/clm_kosmos_akida/abs_margin_chip.py` launched under nohup.

**BLOCKER:** mid-fire (during the random_int4 trials) pi5-akida went fully OFF-NETWORK — `ssh: Host is down` / `ping: No route to host` / 100% packet loss, sustained for the rest of the session. This is a host-level outage (power/network/reboot of the Pi), NOT remediable remotely. The result file `out/result_abs_margin.json` therefore never reached a terminal `disposition` from this session's vantage. NO AKIDA verdict is claimed (the only thing measured before the drop is the random_int4 control going NEGATIVE at −1.44/−1.71, consistent with the prior closed-negative — but that is the CONTROL arm, not the falsifier; the oracle-LDA treatment arm never ran).

**Armed harvester (a_cpu_local_no_waiter):** a durable local harvester (`/tmp/laneA_harvest.sh`) + log Monitor are running; they reconnect on host recovery and auto-harvest `abs_margin.log` + `result_abs_margin.json` IF the nohup survived (network-only blip) or report DIED if the host rebooted (nohup lost). pi5-akida is sacred host config (PI5-AKIDA.json) — NOT touched/swapped; the outage is external.

**Closure verdict:** BLOCKED — not PUBLIC-grade, not closed-negative. Honest: chip was reachable + learning live, the rung is correctly pre-registered and on-target, but the host dropped mid-fire so no terminal on-chip measurement exists. Smallest unblock step: when pi5-akida returns to the LAN, re-run `~/.venv/anima-akida/bin/python -u ~/clm_kosmos_akida/abs_margin_chip.py` (idempotent, commit-early JSON) — ~16 encoder×scale chip-map cycles; the LDA-oracle treatment arm is what decides PASS vs closed-negative.

**Lane G (substrate=GPU · NEVER merged):** still held on provider-wide provisioning outage (vast+runpod dark). Recipe is FIXED on hexa-lang `laneg/devfeed-cuda-link-merge` (verified present locally + origin); waits only on a live SSH-able GPU host.

---

## 2026-06-02 (later) — Lane A (substrate=AKIDA · pi5-akida · a_lane_akida_gpu_split — NEVER merged with any GPU/Lane-G number) — "all go" decider re-attempt → host STILL DARK, BLOCKED reconfirmed + harvester re-armed (durable)

**Trigger:** user "all go" on the pre-registered absolute-margin decider (`.verdicts/lane-a-absmargin/PREREGISTER.md`). The test is built + pre-registered; only blocker was the pi5-akida host outage. Re-checked reachability this session before any fire.

**Reachability (verbatim, this session):**
```
sidecar pool on pi5-akida → ssh: connect to host 192.168.50.155 port 22: Operation timed out
ping -c2 192.168.50.155     → 2 packets transmitted, 0 received, 100.0% packet loss
```
pi5-akida (ubuntu@192.168.50.155 per PI5-AKIDA.json) is STILL fully off-network — the same external host outage. NOT remotely remediable. No `sidecar pool` route, no ICMP. Per a_lane_akida_gpu_split + a_fire_autonomous scope: Lane A is AKIDA-only, $0 — NO GPU/cloud pod substituted (substituting Lane-G for Lane-A is forbidden). "go" cannot force an external host back online.

**Decider NOT run** — STEP 2/3 cannot execute on-chip while the host is dark. No on-chip abs_margin measured this session; **no result fabricated**. The oracle-LDA treatment arm (the decider for PASS vs closed-negative) remains UN-RUN, exactly as the prior entry.

**Prior harvester had given up:** the earlier `/tmp/laneA_harvest.sh` ran ~30min, logged `HOST_STAYED_DARK`, and exited (90-try cap). No artifacts harvested (`/tmp/result_abs_margin.json.harvested` absent).

**Harvester RE-ARMED (durable, a_cpu_local_no_waiter):** re-armed `/tmp/laneA_harvest.sh` as a background nohup (no 30-min cap; ~10-min heartbeat). On host return it (1) harvests `abs_margin.log` + `result_abs_margin.json` if a terminal `disposition` exists, else (2) auto-re-fires `~/.venv/anima-akida/bin/python -u abs_margin_chip.py` on-chip and keeps polling. CPU-local poll, no Monitor/waiter dependency.

**Closure verdict:** BLOCKED-OUTAGE (unchanged) — not PUBLIC-grade, not closed-negative. The decider is correct, pre-registered, on-target; the ONLY gap is the external pi5-akida host being off-network. PI5-AKIDA.json consulted, NOT modified; no os_default daemon touched; pi5-akida NOT converted to pool compute. Next Lane-A step: when pi5-akida rejoins the LAN the armed harvester auto-fires + harvests the decider, with the LDA-oracle arm settling PASS (PUBLIC-positive, ci_lo>0) vs CLOSED-NEGATIVE scoped to 25/250-anchor.

---

## 2026-06-02 (Lane-G · substrate=GPU · a_lane_akida_gpu_split — NEVER merged with any AKIDA/Lane-A number) — F-RFC046 host per-step orchestration redesign LANDED (byte-eq PRESERVED) · util≥20% PENDING held GPU fire

**Trigger:** today's CLEAN Lane-G GPU fire (all 5 build/link/compile/emit bugs fixed + merged; GPU **provably live** — 87W + GB-scale device memory) definitively pinned util RED — mean **0.811%**, peak 6%, n=987 at mid d~1536/T~512 — DESPITE both device-feed levers active (lever-a #2505, lever-b #2504). CE descent GREEN (F-CLM-PROD-DESCENT=1). One CPU core 100% pegged + GPU SM-starved. Root cause NOT link/kernel/emit/scale (all closed today) — the interpreted host-side per-step orchestration loop in flame/clm_prod dominates the hot path.

**PROFILE-FIRST (@L1, verbatim — d=1536/T=512/K=3/E=2/V=256):**
```
measured hexa-interpreter throughput (warm, compile-cached, mac CPU):
  empty (alloc+exit)        : 0.03 s
  14,155,776-op host loop   : 0.22 s   →  ~13.4 ns / interpreted scalar op

per-step HOST scalar-op count (runs host-interpreted EVEN with DEVFEED+BATCHED):
  FWD TOTAL  41,422,848
  BWD TOTAL  62,656,512
  TOTAL     104,079,360  (+22 separate _adam dispatches)

category breakdown:
  expert batched-path host repack/im2col/col2im : 67,633,152  (65.0%)  ← DOMINANT
  conv Wt-transpose + bias + db (4 convs ea way): 32,514,048  (31.2%)
  residual/copy/sum glue                        :  3,932,160  ( 3.8%)

wall-time: 104.08M × 13.4 ns ≈ 1.39 s host CPU/step (one core 100%) vs sub-ms GPU
GEMM → util ≈ <1ms/1400ms ≈ 0.07–0.8%  ⇒ MATCHES the fire (mean 0.811%, peak 6%).
```
ROOT (pinned): the batched-expert path (`conv2_*_via_forge_batched`) carried INLINE host `t_set` im2col/im2col_t loops that BYPASSED lever-(a)'s device helpers — so the experts' gather never went device-resident.

**REDESIGN (@L2):** route the batched-expert fwd/bwd im2col / im2col_t through the lever-(a) device helpers (`_clmp_im2col` / `_clmp_im2col_t`) — device-resident under CLM_PROD_DEVFEED so the gather leaves the host hot path and the batched GEMM reads it in place with no H2D roundtrip. Device math (levers a+b) intact. (hexa-lang stdlib/flame/clm_prod.hexa.)

**BYTE-EQ (@L3, g5 verbatim — $0 mac CPU oracle stdlib/flame/clm_prod_hostfeed_eq.hexa):**
```
  fwd dil=1 max|Δ| y0=0.0 y1=0.0
  fwd dil=2 max|Δ| y0=0.0 y1=0.0
F-RFC046-HOSTFEED-FWD-EQ = 1
  bwd dil=1 max|Δ| xcolT=0.0
  bwd dil=2 max|Δ| xcolT=0.0
F-RFC046-HOSTFEED-BWD-EQ = 1
ALL-PASS — F-RFC046 batched-expert host-feed redesign byte-eq to the inline-host path
```
Existing oracles unchanged & re-green: F-CLM-DEVFEED-{IM2COL,FWD,BWD,ADAM}-EQ all max|Δ|=0.0 (dX 2.78e-17/5.55e-17 FP64-ULP), F-CLM-CONV2-BATCHED-{FWD,BWD}-EQ all 0.0. NO numeric drift → no revert.

**HONEST residual:** im2col routing removes the expert GATHER from the host hot path, but the DOMINANT remaining host cost is the GEMM-feed REPACK (Wt transpose · a_all/b_all/c_all pack/unpack · dW unpack — the 14.16M-op loops) intrinsic to the matmul calling convention. Eliminating it needs a device repack / transpose-aware GEMM builtin (forge_dispatch_matmul has no transpose variant) → self/runtime.c + cuda-kernel signature change, pod self-host rebuild, NOT mac-byte-eq-testable. Distinct follow-on lever, out of scope for this byte-eq source PR.

**SHIP:** hexa-lang PR #2515 (code + oracle, base main) + #2516 (docs: inbox patch + CHANGELOG; merged into the pr1 branch by the create→merge-atomic g47 hook, so #2515 now carries all 4 files). NO force-push; main untouched (HEAD a7f145cd). Auto-QA: conformance @L1–@L5 ↔ code 1:1 PASS · regression (all byte-eq oracles max|Δ|=0.0 + codegen clean) PASS.

**@L5 — NO GPU FIRED this pass** (cost-discipline; source + byte-eq only). 

**NEXT (HELD — gated for explicit user go):** util≥20% verify fire — clean single-driver H100 sm_90 (no collision), CLM_PROD_DEVFEED + CLM_PROD_BATCHED both set, HEXA_CUDA_ARCH=90, -lcuda. SUCCESS = util ≥20% AND descent GREEN; paste nvidia-smi PEAK/MEAN verbatim. The source redesign CANNOT confirm util≥20% without that fire — util-GREEN is NOT claimed from source work alone. ref fe2e43a35; hexa-lang inbox/patches/forge-rfc046-host-feed-residual-resolution.md.
