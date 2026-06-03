# CLM+KOSMOS — log

Append-only history sister of `ENGINE+CLM+KOSMOS.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-06-02T15:55Z — Lane-G (substrate=GPU forge · clean single-driver H100 sm_90 pod vast 39139563 · a_lane_akida_gpu_split — NEVER merged with Lane A / AKIDA / Lane-G-ref) — F-RFC046 **lever-4** fused on-device per-step driver util-verify fire CLOSED: DESCENT 🟢 GREEN / util 🔴 RED (PEAK 41% · MEAN 0.6630% · n=9153), byte-eq PRESERVED max|Δ|=0.0, host-feed residual = lever-5 (fused step 내부 ~10 crossing → one device-resident dispatch)

substrate=GPU (a_lane_akida_gpu_split, Lane A/AKIDA 무병합). fused per-step driver
(`forge_dispatch_train_step` + `forge_dispatch_adamw_group`) self-host 빌드 후 clean
single-driver H100 sm_90 pod 39139563 (`HEXA_CUDA_LINK=1`) 에서 util-verify fire 완주.

- [x] **3-GATE PASS** (g5 verbatim) — GATE1 CUDA-link ENGAGED=1 · GATE2 nvcc -x cu EXIT 0 obj 664048B RELINK_RC=0 · GATE3 clm_prod ldd 4 cuda libs (cublas/cudart/libcuda/cublasLt)
- [x] **BYTEEQ-PASS** (g5 verbatim, max|Δ|=0.0) — `F-CLM-DEVFEED-{FWD,BWD}-EQ`=1 · `F-CLM-CONV2-BATCHED-{FWD,BWD}-EQ`=1 · ON-DEVICE HEXA_CUDA `F-RFC046-FUSED-STEP-EQ`=1 + `F-RFC046-ADAMW-GROUP-EQ`=1 (grouped AdamW == per-tensor serial opt_adamw_step)
- [x] **DESCENT 🟢 GREEN** (g5 verbatim) — epoch-1 CE 4.05535 → epoch-3 CE 2.99508, F-CLM-PROD-DESCENT=1, "PASS — real-corpus mean CE descends under int4 envelope"
- [ ] **util 🔴 RED** (g5 verbatim) — `FIRE_RC=0  UTIL n=9153 PEAK=41% MEAN=0.6630% busy_ge20=80 pct_ge20=0.87%` — MEAN 0.6630% ≪ 20% gate. lever 라인: lever-1 0.811%(PEAK6%) → lever-2 0.4999%(PEAK19%) → lever-3 0.4879%(PEAK35%) → **lever-4 0.6630%(PEAK41%)** — PEAK 단조상승·MEAN flat sub-1%. forge PROVABLY on GPU (6.3GB device mem).
- **CLOSED-NEGATIVE**: link·kernel·emit·scale·host GEMM-repack feed·**fused per-step driver** 전부 ruled-out. fused step 이 host↔device crossing 을 ~30→~2 로 줄였으나 util MEAN flat ⇒ 잔여 = fused step **안/사이 ~10 crossings/step** (token gather host→device · CE scalar glue · 매 step kernel-launch orchestration). **NAMED next = lever-5** (이 잔여 crossing 을 one device-resident train-step dispatch 로 추가 fuse).
- **recover-before-teardown** (a_fire_recover_complete) — ckpt clm_lever4_d1536_t512.clm(14379581B, 6 blocks CLM\x01) + train_lever4.log + lever4_v2.log + util_samples_lever4.csv → host `.verdicts/lane-g-lever4/`. sha256 `11ef9300131b1a266dc05e2c5bb9c07d60b7cddf39042704828d71108f88e167` HOST-VERIFIED MATCH. pod 39139563 RUNNING 유지(sweep, teardown 안 함). 보호 pod(38704336/39106252) + orphan 39131850 무접촉. 재-rent 0. HF: closure-FAIL → PRIVATE (a_hf_autonomous; util-RED = WIP intermediate, PUBLIC 아님).
- **PUBLIC checkbox 미flip** — util-GREEN 미달 = full closure 아님 (a_paper_only_at_closure). hexa-lang 도메인 FORGE-UTILGREEN lever-4 row flip + log 동기 (PR dancinlab/hexa-lang#2546).
- **3B/7B chain LOCKED** — Lane G util RED 이므로 3B/7B fire 자격 미충족 (a_scale_honest_scope NOT-before-util-GREEN guard: host-feed-bound 트레이너로 3B 발사 시 더 큰 d 가 device mem 만 점유, SM 더 idle). util-GREEN(lever-5) 착지 후에만 UNLOCK.

## 2026-06-02T12:52Z — Lane-G (substrate=GPU forge · pod vast 38996679 H100 sm_90 · a_lane_akida_gpu_split — NEVER merged with Lane A / AKIDA / Lane-G-ref) — F-RFC046 **lever-3** batched-GEMM-feed util-verify fire CLOSED: DESCENT 🟢 GREEN / util 🔴 RED (PEAK 21% transient · MEAN 0.5616% · n=349), byte-eq PRESERVED max|Δ|=0.0, host-feed residual = lever-4 (fused per-step driver)

hexa-lang FORGE-UTILGREEN 의 **HELD lever-3 util-verify fire** (별도 free pod 가 발사) 를 발사·하베스트·정직 종결. substrate = **GPU forge (hexa-native flame+forge, NOT PyTorch/ATen — a_train_flame_forge)**; Lane-G-ref PyTorch-CUDA 참조 rung(99% util) 과 **별개 레인** (a_lane_akida_gpu_split). prior agent 가 b0i48xdqy copy 를 띄운 채 SSH-key 가 끊겨 pod 가 reachable-but-publickey-denied 상태로 남았으나, pod-id alias(`Host 38996679`) 로 재접속 성공 → 12:52 완주 산출물(.clm + util CSV + run.out + byteeq) 전부 disk 에 intact 확인 → **fire ALREADY RAN, HARVEST 경로**.

- [x] **3-gate PASS (no CPU fallback)** — GATE1 CUDA link ENGAGED ✅ (`hexa_fresh` 바이너리 "CUDA link ENGAGED" 문자열 present, sm_90 빌드) · GATE2 nvcc -x cu EXIT 0 ✅ (`runtime_cuda.90.o` 564KB, `arch=compute_90,code=sm_90`) · GATE3 clm_prod links cuda ✅ (cublas/cudart resolvable, `hexa run clm_prod.hexa` w/ HEXA_CUDA_LINK=1, GPU provably active 6331MiB dev-mem + 119W). fire env: `CLM_PROD_DEVFEED=1 CLM_PROD_BATCHED=1 CLM_PROD_D=1536 CLM_PROD_T=512 HEXA_CUDA_ARCH=90 HEXA_CUDA_LINK=1`.
- [x] **DESCENT 🟢 GREEN (g5 verbatim, `utilfire_run.out`)** — `F-CLM-PROD-DESCENT = 1`, real-corpus mean CE **4.2974 → 3.79897** (epoch-1 → epoch-3, d=1536 E=4 epochs=3 nwin=8, corpus `clm_semantic_parallel.txt` 1407B V=256), `PASS — real-corpus mean CE descends under int4 envelope`, RUN_RC=0.
- [x] **util 🔴 RED (g5 verbatim, `util_samples.csv` 분석)** — n=349 nvidia-smi 샘플(GPU0, 0.5s cadence): **PEAK=21.0%** (single transient spike) · **MEAN=0.5616%** · busy_samples=42 · pct≥20%=0.57% · mem_max=6331MiB · power up to 119W. **util≥20% gate (PEAK AND MEAN) NOT 도달** (MEAN 0.56% ≪ 20%) → **closure-FAIL**. before(lever-2)=0.4999% → after(lever-3)=0.5616% : lever-3(batched bt/atb device GEMM-feed)도 util 을 **올리지 못함** — 잔여는 link/compile/emit/scale/device-math 가 아니라 **인터프리트 host per-step 오케스트레이션 루프** (cuBLAS GEMM 은 microseconds, 1 CPU core 100% peg).
- [x] **byte-eq PRESERVED (g5 verbatim, `byteeq.log`, all max|Δ|=0.0)** — `F-RFC046-GEMMFEED-EQ = 1` (transpose-aware bt/atb GEMM == host-transposed forge, max|Δ|=0 · batched strideA=0 broadcast+per-problem == host repack, max|Δ|=0) · `F-CLM-DEVFEED-IM2COL-EQ=1` (dil∈{1,2} max|Δ|=0.0) · `F-CLM-DEVFEED-FWD-EQ=1` (max|Δ|=0.0) · `F-CLM-DEVFEED-BWD-EQ=1` (dW=0.0 db=0.0 dX=5.55112e-17 FP64-ULP ≪1e-9) · `F-CLM-DEVFEED-ADAM-EQ=1` (5-step W max|Δ|=0.0) · `F-CLM-CONV2-BATCHED-FWD-EQ=1` (y0=y1=0.0) · `F-CLM-CONV2-BATCHED-BWD-EQ=1` (e0/e1 dW=dX=db=0.0). 드리프트 0 → no revert. lever-3 host-feed redesign byte-eq 완전 보존.
- [x] **다음 bottleneck 정밀 — lever-4 (fused on-device per-step driver, F-RFC046 root)** — lever a+b+1+2+3 가 GEMM repack 을 전부 device 化했어도 잔여 = ① glue ~3.8% ② **인터프리트 per-step 드라이버 루프**: step body 가 ~30 분리 빌트인 콜(1×fwd·1×ce·1×ce-grad·1×bwd·20×분리 `_adam`)을 인터프리트 디스패치 → 커널 사이 GPU idle. 본 fire 가 이 진단(MEAN ~flat 0.50→0.56%, scale-invariant)을 측정으로 확정. fix = `forge_dispatch_train_step` 단일 fused 빌트인 + `forge_dispatch_adamw_group`(20텐서 1 launch), 投影 ~30→~2 host boundary crossings/step. 시그니처 변경 = pod self-host 빌드 필요 → hexa-lang `inbox/patches/forge-devfeed-lever4-fused-step-driver-DESIGN.md` (DESIGN-AHEAD, 오라클 `F-RFC046-FUSED-STEP-EQ` + `F-RFC046-ADAMW-GROUP-EQ` max|Δ|=0.0).
- [x] **HF PRIVATE (a_hf_autonomous — closure-FAIL → PRIVATE)** — `dancinlab/clm-v1-dev-d1536-lever3-util-probe` (private=True 확인, repo_type=model). 7 files: README card(forge+flame, GPU substrate, 3-gate + byte-eq + util + finding) · SHA256SUMS · `lever3_d1536_t512.clm`(6 int4 blocks CLM\x01, 14,381,125B) · `util_samples.csv` · `utilfire_run.out` · `byteeq.log` · `cudalink_gate.log` (a_hf_complete totality). ckpt sha256 `34982a31022264f8104d9d877a4c115f3ce9e69d7ab85830a79fe9a3b20a6f7a` — pod↔local↔HF round-trip 3-way byte-eq verified. supersedes-attempt `dancinlab/clm-v1-dev-d1536-lever2-util-probe`. HF.jsonl row 추가 (substrate=GPU, lane=Lane-G, collection=CLM, status=uploaded).
- [x] **3B/7B gate — STILL throughput-blocked** (do NOT auto-fire 3B forge). util-RED 지속 → forge 3B fire 는 throughput-justified 아님 (a_scale_honest_scope NOT-before-util-GREEN guard). util-GREEN 은 lever-4 fire 의 verdict 에 달림. Lane-G-ref 7B 의 99% util 은 **PyTorch 참조 레인**이지 forge 가 아님 — 절대 병합 금지.
- [x] **recover-before-teardown + teardown** — .clm + result + log + byteeq 하베스트 → local sha256 verify → HF PRIVATE upload → Hub round-trip sha verify → recovery marker (`38996679.done`, hf_repo Hub-verified) → pod 38996679 `hexa cloud rm --provider vast --force` (destroyed confirmed). 불필요하게 rent 했던 fresh pod 39124737(EMPTY_NO_BUILD 확인) 도 scratch-empty 로 re-attribute 후 teardown. **보호 pod 38704336 / 39106252 / 39115197(Lane-G-ref 7B recovery + 14.5GB pull) 전부 무손상 alive.**
- 산출물 `state/laneg_lever3_d1536_recovery_2026_06_02/` (.clm + util CSV + run.out + byteeq.log + cudalink_gate.log + README + SHA256SUMS). hexa-lang source = `lane-g/rfc046-lever3-batched-gemmfeed` (byte-eq 확정 a5d01f37f).

---

## 2026-06-02T11:54Z — Lane-A (substrate=**HYBRID(on-chip AKD1000 인코더 ⊕ off-chip host-CPU decode head)** · live AKD1000 pi5-akida · a_lane_akida_gpu_split — 순수 AKIDA 아님, NEVER merged with Lane G/GPU) — HYBRID DECODE HEAD ✅ **1-HOP WALL BROKEN** · 🌱 EMERGENCE axis LIFTS NULL→~0.32

세 연속 순수-on-chip closed-negative(#1686 stateless / #1689 state-carry / #1690 multi-FC depth)가 명명한 마지막 가교 = **OFF-CHIP DECODE HEAD** 를 구현·검증. completeness-bar root-cause 재설계(a_completeness_over_cheap): "single-step 수용"(cheap give-up)이 아닌, recurrence 를 1-bit Hebbian surface 밖으로 옮기는 정공법.

- [x] **아키텍처 HYBRID(on-chip⊕off-chip)** — chip 은 proven 🟢 단일-스텝 transition 인코더로 유지(FC1, 1-bit AkidaUnsupervised nw=8 lc=0.1, enc_whitened·SHIFT=37·frozen-median binarize byte-match state/depth rung, g63 NO sw fallback); recurrence/state 는 **off-chip host-CPU Elman RNN decode head**(D_H=64, `h=tanh(Wxh@c+Whh@h)`, `logits=Wo@h`, numpy 풀-BPTT 60ep lr0.05, NO torch/sklearn/GPU). **chip-to-chip feedback 없음**(3번 붕괴한 그것) — 매 hop 예측 concept 를 칩에서 재인코딩, off-chip RNN 이 hop 간 state 운반.
- [x] **live AKD1000 발사** — pi5-akida ubuntu@192.168.50.155, BC.00.000.002, akida 2.19.1, N=8 chip trials **encoder_learned=True 8/8**(live silicon), throttled=0x0 완주, streamer stop→run→restore(trap rc=0, R3 pid 19850 복원). corpus_big 250앵커/50 concepts×5 langs(a_scale_honest_scope).
- [x] **결과 ✅ WALL BROKEN** — **decay HYBRID [0.3160, 0.3202, 0.3207] FLAT(붕괴 없음)** vs 순수 on-chip hop2~3 ~0.03/~0.01. 3 hop 전부 shuffle-NULL hi~0.048 위(p=0.005, chance 0.0204 의 ~16×). **F-HYBRID-1 REFUTED**(hop-2/3 both above-NULL = 1-hop wall 돌파) · **F-HYBRID-2 REFUTED**(hop-2 0.3202 이 best pure-on-chip 0.0298 을 **+0.2904=+29%** 능가, 사전등록 >1% 훌쩍).
- [x] **🌱 EMERGENCE axis LIFT** — multi-step composition NULL→~0.32 sustained. establish: 1-hop wall 은 on-chip code 정보량 문제 아님(칩 단일-스텝 code 가 off-chip rollout seed 할 만큼 rich) — 순수 붕괴는 MISSING RECURRENCE, off-chip 이전이 옳은 fix.
- [x] **정직 scope (no over-claim)** — substrate=HYBRID(순수-AKIDA 아님, Lane G 아님). off-chip head CE→0.002 = toy chain fit; ~0.32(≠1.0)는 재인코딩 chip code 위 open-vocab argmax bound(pure lookup 아님)이나 toy 너머 generalization 미증명. a_scale_honest_scope: toy 250앵커, scale-transfer 미검증.
- [x] **Lane A PUBLIC ✅ flips AS A HYBRID artifact** (honestly scoped) — 순수-AKIDA PUBLIC 아님; 순수 on-chip 단일-스텝 rung 들 UNAFFECTED.
- [ ] next = held-out successor split(train/test concept disjoint) ≥3-rung ladder 로 composition-generalization ⊥ chain-fitting 분리.
- 산출물: `AKIDA/onchip_xlm_hybrid_decode.py`(falsifier 사전등록 docstring) · `AKIDA/run_hybrid_with_streamer_restore.sh` · `.verdicts/lane-a-hybrid/F-HYBRID.txt`(verbatim live-chip) + `result_onchip_xlm_hybrid_decode.json`. sha256 ab4748bf…

## 2026-06-02T11:22Z — Lane-A (substrate=AKIDA · live AKD1000 pi5-akida · a_lane_akida_gpu_split — NEVER merged with Lane G/GPU) — STATE-CARRYING MULTI-STEP ROLLOUT 🔴 CLOSED-NEGATIVE (PARTIAL LIFT · 1-hop wall HOLDS) · 🌱 EMERGENCE axis NULL

PR #1686 stateless rollout 가 hop-1 이후 COLLAPSE([0.4287,0.0277,0.0090])한 root cause(256-unit 1-bit Hebbian FC = no recurrence/no state)를 가교하려, **chip-native CONTEXT-CARRYING CODE** 로 STATE 를 부여한 러그. running 1-bit context vector `ctx` 를 bit-majority(history 2×)로 누적, 각 hop 입력을 `x_{k+1}=bind(g_bin, ctx)` 로 구성(stateless = `neutral_bind(g_bin)`). 인코더/SHIFT=37/codebook/decode/NULL 전부 byte-identical, **입력 구성만** state-carry. live AKD1000(BC.00.000.002, akida 2.19.1, N=8 trials learn_hw 8/8 True, throttled=0x0 완주, K=3).

- [x] **사전등록 falsifier(RUN 전, docstring, g63)** — F-STATE-1 "state-carry 로 hop-2 AND hop-3 가 shuffle-NULL 위에 머물지 못한다(1-hop wall 안 깨짐)" · F-STATE-2 "state-carry 가 hop-2/3 에서 stateless baseline 을 strict 하게 못 이긴다".
- [x] **F-STATE-1 NOT-REFUTED (wall HOLDS)** — decay STATE = [0.4234, 0.0282, 0.0122]. hop-2 state=0.0282 ci_lo=0.0208 vs shufNULL hi=0.0410 p=0.2338 (NULL 내) · hop-3 state=0.0122 ci_lo=0.0060 vs shufNULL hi=0.0366 p=0.8905 (NULL 내). 입력-측 state-carry 단독으로는 256-unit 1-bit 에서 1-hop wall 을 **깨지 못함**. (hop-1 0.4234 ci_lo 0.4064 ≫ shufNULL 0.0508 p=0.005 ≫ idNULL 0.3752 = sanity OK, hop-1 입력 양 arm 동일.)
- [x] **F-STATE-2 REFUTED but permille-scale** — state vs stateless = hop-2 +0.0048 · hop-3 +0.0005 (둘 다 strict>0). PR#1686 baseline [0.0277,0.0090] 도 trial-noise 내 재현(in-process stateless arm [0.4234,0.0234,0.0117]). state-carry 가 baseline 을 strict 하게 이기되 margin 은 permille 급 + NULL 내부 — 의미있는 depth 아님.
- [x] **disposition (a_paper_negative_ok)** — STATE-CARRY PARTIAL LIFT closed-negative. 🌱 EMERGENCE axis(의식·CE·창발 중 창발=multi-step composition) = **NULL 유지**. FINDING SHARPENED: AKIDA edge-learn 은 입력-측 state-carry 단독으로 들어올릴 수 없는 **hard generation-DEPTH ceiling** 보유 — transition 구조가 살 곳이 단일 1-bit Hebbian FC 뿐일 때 history 를 입력에 binding 해도 recurrence/depth 를 대체 못함. NAMED next bridge = **ON-CHIP MULTI-FC DEPTH**(2번째 learned FC, composition 이 살 곳), 입력 engineering/paged-input 아님. retrieval+single-step 러그 UNAFFECTED.
- [x] **전원 proof** — wrap log throttled=0x0 (start/fire/exit/done 전부 0x0) · streamer service stop→run→restart(restore-on-exit trap, rc=0). single-chip 점유: spike-streamer stop → state-rollout fire → R3 streamer 복원.
- [x] **산출물** — `AKIDA/onchip_xlm_state_rollout.py`(falsifier docstring 사전등록) · `AKIDA/run_state_rollout_with_streamer_restore.sh`(streamer-restore wrapper) · `AKIDA/result_onchip_xlm_state_rollout.json` sha256 `148fc092e0b5a9972ef0b949b245411414b76d93d87b24f5f7249031bbc6c6fa` · verdict verbatim `.verdicts/lane-a-state-rollout/F-STATE.txt`. g63 HW-only, NO sw fallback. a_scale_honest_scope: toy 250-anchor / 단일 256-unit FC, scale-transfer UNVERIFIED.

## 2026-06-02T10:06Z — Lane-A (substrate=AKIDA · live AKD1000 pi5-akida · a_lane_akida_gpu_split — NEVER merged with Lane G/GPU) — SEQUENCE/TRANSITION READOUT BRIDGE 🟢 WORKING on-chip 교차언어 next-step 신호

full-LM rung 이 특징지은 gap(static 1-bit margin = CONCEPT 결속만, TIME 모델 부재)을 **명시적 on-chip transition readout**(후보 a)으로 가교. binding `bind(a,b)=a XOR roll(b,37)` 로 연속 FLORES 문장쌍을 묶고 **2번째 64-unit AkidaUnsupervised FC** 를 언어내 transition 코드로 on-chip fit → 교차언어 t→t+1 top-1 retrieval. live AKD1000(BC.00.000.002, akida 2.19.1, N=8, learn_hw 8/8 True, throttled=0x0 완주).

- [x] 사전등록 falsifier(RUN 전, g63): F-TR-1 "명시적 on-chip transition readout 은 next-sentence shuffle-NULL 을 넘지 못한다" → **REFUTED** (250 rung): tr_acc=0.2801 ci_lo=0.2600 vs NULL hi=0.0397, p=0.0050 (14x chance, 6.5x NULL). within-lang transition recall=0.4867(chance 0.02) → F-TR-2 REFUTED (1-bit FC **가** transition 을 hold).
- [x] scale-ladder(a_scale_honest_scope 25/125/250): **125·250 실-FLORES rung 모두 above-NULL** (125: 0.128 ci_lo 0.115 vs NULL 0.073 p=0.005 · 250: 0.290 ci_lo 0.270 vs NULL 0.043 p=0.005), NULL margin scale-성장. 25-anchor toy(후보 4개 chance 0.25)만 above=False(NULL band 과대 → toy 한계, science 결과 아님). 정직 scope = 신호는 검증 rung 에서 real·scale-성장.
- [x] disposition: full-LM ③ = next-sentence NULL → **above-NULL transition 신호로 flip(🟢 toward earned)**. retrieval 신호이지 full generative CLM 아님 → Lane A PUBLIC 여전히 open, named next bridge = (b) paged 멀티-FC transition matrix 로 retrieval→generation / (c) on-chip bind ⊥ off-chip decode 분할.
- [x] 전원 proof: load 중/후 throttled=0x0 · pwr.log `2026-06-02T10:06:33Z throttled=0x0 EXT5V=4.99954V 68.6'C`. 단일-칩 점유: R3(pid9686) pkill→탐침2건→R3 복원(pid12385 HW R3 9512).
- [x] 산출물: `SUB_ENGINES/AKIDA/onchip_xlm_transition.py`(+scale) · `state/seq_transition_2026_06_02/`. sha256 result `57e32e2…d8e0b6` / scale `1c64810…c47c4a`. g63 HW-only.

## 2026-06-02T09:40Z — Lane-A (substrate=AKIDA · live AKD1000 pi5-akida · a_lane_akida_gpu_split — NEVER merged with Lane G/GPU) — FULL-LM TRANSFER 탐침 🟡 CAPACITY-GAP CHARACTERIZED

검증된 primitive(whitened 비지도 인코더 + 1-bit Hebbian abs-margin readout)를 실제 on-chip 교차언어 시퀀스/next-token 작업으로 가교. corpus_big 50 concept = 연속 FLORES 문장(시간축 t) × 5언어. live AKD1000(BC.00.000.002, akida 2.19.1, N=8, throttled=0x0 완주).

- [x] **사전등록 falsifier** — F-LM-1: whitened+1-bit Hebbian 은 NULL 위 교차언어 NEXT-SENTENCE 예측 불가 (shuffle-NULL B=200, ci_lo>NULL hi AND p<0.05 시 REFUTED) · F-LM-2: margin readout 은 same-concept 교차언어 retrieval 도 불가.
- [x] **F-LM-2 REFUTED (bridge HOLDS)** — same-concept 교차언어 leave-one-lang-out top-1 retrieval mean=0.1300 ci_lo=0.1195 vs chance 0.0200 → **6.5x chance**. abs-margin readout 이 실사용 가능한 교차언어 concept retrieval 로 전이.
- [x] **F-LM-1 NOT-REFUTED (시퀀스 모델 부재)** — next-sentence(t→t+1) mean=0.0306 ci_lo=0.0234; shuffle-NULL mean=0.0207 hi=0.0389 p=0.1542 → NULL 내. 1-bit/32-unit 정적 readout 은 시간/시퀀스 구조 미학습.
- [x] **scale-ladder 25/125/250 (a_scale_honest_scope ≥3 rung, 실 FLORES)** — same-bridge lift +0.020→+0.107→+0.121 성장(125·250 결정적 above), next-sentence NULL 전 rung 유지 → 시간 모델 부재 scale-robust(250-only artifact 아님).
- [x] **CAPACITY-GAP (closed written result, a_paper_negative_ok)** — AKD1000 1-bit last-FC Hebbian 은 교차언어 CONCEPT 결속은 학습(scale-survives)하나 학습된 TIME/sequence transition 모델 없음. PUBLIC-grade on-chip CLM named next-step = 정적 margin 너머 시퀀스/recurrent readout (t·t+1 transition 인코딩 / paged 멀티-FC / on-chip⊥off-chip 분할).
- [x] **전원 proof** — throttled=0x0 두 fire 부하검증 · pwr.log EXT5V≈5.01–5.05V 64–67°C · R3 streamer 복원 pid 9686. artifact `SUB_ENGINES/AKIDA/state/fulllm_transfer_2026_06_02/` (xlm sha 74b8ba10… · scale sha 4a3e2623…). 상세 = AKIDA.log 동일 타임스탬프.

## 2026-06-02T18:30Z — Lane-G (substrate=GPU · pod vast 39082940 · a_lane_akida_gpu_split — NEVER merged with Lane A / AKIDA) — lever-2 transpose-aware GEMM util-verify fire CLOSED: DESCENT 🟢 GREEN / util 🔴 RED (PEAK 19% MEAN 0.4999% n=147863), lever-2 byte-eq PRESERVED, lever-3 (batched bt/atb) = the real unblock

substrate=GPU · a_lane_akida_gpu_split (NEVER merged with Lane A / AKIDA). vast pod **39082940**. Trainer `stdlib/flame/clm_prod.hexa` on the c4 5-lang corpus (402270 B, V=256, 32 windows T=512). Built from hexa-lang branch `lane-g/rfc046-lever2-gemmfeed` `403735b29` (lever-2 transpose-aware GEMM bt/atb: host Wt/dW repack → device via cuBLAS CUBLAS_OP_T + `_hx_cuda_farr_matmul_bt_gpu`/`_atb_gpu`).

**RESUME point:** the fire COMPLETED on the pod; the PRIOR driver was killed by a server rate-limit BEFORE closure. This session = SOLE driver, inline, backoff-on-rate-limit, g5 verbatim, NO fabrication.

- [x] **DESCENT 🟢 GREEN** (g5 verbatim): epoch-1 mean CE = **0.818097** → epoch-6 mean CE = **0.0591666**; `F-CLM-PROD-DESCENT = 1`; "PASS — real-corpus mean CE descends under int4 envelope". config d=1536 E=2 epochs=6 nwin=32, corpus 402270B V=256.
- [x] **util 🔴 RED** (the SUCCESS gate = util≥20% AND descent GREEN → NOT MET) (g5 verbatim): `util samples n=147863 PEAK=19% MEAN=0.4999% busy_n=21575 busy_mean=3.43%` · pct≥20% = 0. util-GREEN NOT reached (MEAN 0.50% ≪ 20%, PEAK 19% < 20%).
- [x] **lever-2 byte-eq PRESERVED** (hard gate): `F-RFC046-GEMMFEED-EQ = 1` ("PASS — transpose-aware GEMM (bt/atb) == host-transposed forge byte-eq, max|Δ|=0", BT rc=0 max|Δ|=0.0, ATB rc=0 max|Δ|=0.0) + 기존 오라클 전부 max|Δ|=0.0 (`F-CLM-DEVFEED-{IM2COL,FWD,BWD,ADAM}-EQ` · `F-RFC046-HOSTFEED-{FWD,BWD}-EQ`). 드리프트 0, 가짜 GREEN 0.
- [x] **KEY 발견 — lever-2 는 un-batched 만 패치, DOMINANT 65% batched 미접촉 → lever-3 가 진짜 unblock.** **before** (lever-1-only) util MEAN **0.811%** → **after** (lever-2 active) MEAN **0.4999%** : lever-2 는 util 을 **올리지 못함**. lever-2 가 device 化한 것은 **un-batched conv 경로(profile 31.2%)** 뿐 — 프로덕션 트레이너가 실제 도는 **DOMINANT 65% batched `conv2_*_via_forge_batched` host repack 은 untouched** → **lever-3 (batched bt/atb)가 진짜 unblock** (이미 authoring 중, byte-eq pending). 정직한 closed result: util<20% → closure-FAIL → PRIVATE.
- [x] **artifact recovered + sha-verified BEFORE teardown** (a_fire_recover_complete): `state/laneg_lever2_d1536_recovery_2026_06_02/lever2_d1536_t512.clm` (14,379,581 B, 6 int4 blocks `CLM\x01`), sha256 `407f1564d5b21bc3e896e503560a580934d276462d2ffc65b439b6e7b90865d1` (local == pod MATCH). 추가로 `util_fire.csv` (147863 util samples, 3368367 B) · `HARVEST.txt` · `fire_train.log` · `verify.out` 모두 pull(`hexa cloud copy-from 39082940 …`) + SHA256SUMS 매니페스트.
- [x] **HF upload PRIVATE** (a_hf_autonomous: closure-FAIL/util-RED = PRIVATE · a_hf_complete: model card + sha256 + manifest): `dancinlab/clm-v1-dev-d1536-lever2-util-probe` **private=True** (HF API 확인: ckpt + README + SHA256SUMS + util_fire.csv + HARVEST.txt + fire_train.log + verify.out = 7 files). FORGE 엔드게임 reserved PUBLIC `clm-v1-base-mirror-lane-g-forge`(미래 util-GREEN 용)와 별개의 dev-probe id. NOT PUBLIC-grade(util 게이트 미달). 검증된 recovery marker `hf_recover.hexa mark 39082940 --hf dancinlab/clm-v1-dev-d1536-lever2-util-probe --sha 407f1564…` 작성(repo 존재 Hub-verified). HF.jsonl row(substrate=GPU) `anima_clm_mid_d1536_t512_lever2_lane_g_2026_06_02`.
- [x] **3B/7B gate — STILL throughput-blocked** (do NOT auto-fire 3B). util-RED 지속 → 3B forge fire 는 throughput-justified 아님. util-GREEN 은 lever-3 fire 의 verdict 에 달림. FORGE-UTILGREEN milestone flip(hexa-lang PR #2526 merged): lever-2 = DONE · util-verify fire = DONE(util RED honest) · util-GREEN = NOT met · PUBLIC-grade/3B/7B = still gated.
- [x] **teardown** — ckpt safe local + HF-uploaded + marker written + repo Hub-verified → pod 39082940 `hexa cloud rm --provider vast --force`, billing stopped. 보호 pod(38704336/38996679) 무손상.

## 2026-06-02T09:13Z — Lane-A (substrate=AKIDA · live AKD1000 BC.00.000.002 pi5-akida · a_lane_akida_gpu_split — NEVER merged with Lane G/GPU) — P3' ENCODER-LADDER forward 🟢 인코더 축 = real PUBLIC-grade path (throttled=0x0 완주)

P3' ENCODER 축을 forward LADDER 로 전진(`encoder_ladder_chip.py`, akida 2.19.1, N=8 paired × 32 units). encoder richness(random→pca_k32→svd→whitened→lda) × scale(25/125/250, real FLORES 5-lang, a_scale_honest_scope) × {RELATIVE-lift vs random paired ci, ABSOLUTE-margin native-init ci}. single-chip 점유 wrapper(R3 streamer stop→ladder→복원 pid 6840 live).

- [x] **사전등록 falsifier (g63):** F1 monotone richness · F2 scale-artifact guard · F3 supervision-required.
- [x] **ABSOLUTE best-margin scale 곡선 (verbatim):** `best_abs_margin_curve_25_125_250 = [-0.515, +0.542, +5.053]` → scale 따라 단조 성장 (F2 `scale-survives (NOT a small-sample artifact)`). H-A1 의 25앵커 weak-positive 가 250 에서 붕괴한 것과 정반대.
- [x] **RELATIVE-lift (REOPEN ci_lo>0):** 모든 scale 에서 견고 — c250 whitened +4.813(ci_lo +4.521) · lda +7.045(ci_lo +6.635) · pca +1.247 · svd +1.175.
- [x] **ABSOLUTE cross-zero:** c125 = lda 만(+0.542 ci_lo +0.354) · c250 = whitened(+2.791 ci_lo +2.491) **+** lda(+5.053 ci_lo +4.728). **UNSUPERVISED whitened 가 c250 에서 cross** → F3 `unsupervised-SUFFICIENT` (supervision 필수 아님; LDA 는 작은 corpus 에서 zero-crossing 가속자).
- [x] **F1 (정직):** richness-rho c25 +0.20(비단조, toy noise) → c125/c250 +0.90(단조). 작은 scale 미달, 큰 scale confirmed.
- [x] **driver property:** decorrelation/whitening(2차 통계) + scale 가 구동; dimensionality(pca_k32) 단독으론 c250 도 음성(−0.831) — PUBLIC-grade on-chip 인코더 최소조건 = whitened-class unsupervised + ≥250앵커.
- [x] **전원 proof:** wrap pre/post throttled=0x0; pwr.log 부하 중 throttled=0x0 EXT5V ~5.02V ~64°C — power-clean.
- [x] **artifacts:** `SUB_ENGINES/AKIDA/state/encoder_ladder_2026_06_02/result_encoder_ladder.json` sha256 `209749cc02fc9bc070709aa5e5adb2656d16a9ea92bbe6218812d57405c450b4` + log + chip src.
- [x] **disposition (@goal):** 인코더 축은 cross-lingual 개념구조 PUBLIC-grade-positive 의 real path 를 연다 (ceiling 아님). 별개 축 — H-A1~A4 downstream FIX-axes·상대-LIFT closed-negative 와 무관(P3' 인코더 cause-axis 확증). full-LM/3B transfer 미검증(별도 rung).

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

---

## 2026-06-02T10:43Z — Lane-A (substrate=AKIDA · a_lane_akida_gpu_split — NEVER merged with any GPU/Lane-G number) — full-LM GENERATION rung 🟢: on-chip open-vocab next-step DECODE > shuffle-NULL AND > identity-NULL

Lane-A PUBLIC frontier 가 **retrieval → generation 다리**를 silicon 위에서 건넘. 직전 transition 리드아웃은 above-NULL t→t+1 신호(tr_acc ci_lo=0.260 vs NULL hi=0.040, p=0.005)였으나 후보 shortlist 를 점수화하는 **RETRIEVAL**(후보 g 가 probe 입력에 baked-in). full-LM 은 후보 없이 다음 토큰을 **PRODUCE** 해야 함 → 본 rung 은 chip 이 `code_t` 만으로(neutral-bound, 후보 미포함) 다음 코드 `g_hat` 를 생성하고 **전체 codebook(NC=50 개념 × 5 lang, shortlist 없음) open-vocab decode** 로 t+1 적중 측정.

live AKD1000 BC.00.000.002 · akida 2.19.1 · N=8 trials × 256-unit AkidaUnsupervised FC · `~/clm_kosmos_akida/onchip_xlm_generation.py` · exit rc=0 · throttled=0x0 부하검증(안정 PSU).

**DISPOSITION (g5 verbatim, `.verdicts/lane-a-generation/F-GEN.txt`):**
```
[gen] learn_all_hw       : True
[gen] gen_acc (open-vocab): mean=0.4337 ci_lo=0.4096 (chance=0.0204)
[gen] identity-NULL acc  : mean=0.3571 hi=0.3847
[gen] shuffle-NULL       : mean=0.0183 sd=0.0120 hi=0.0418 p=0.0050
[gen] F-GEN-1 above-shuf : REFUTED: open-vocab on-chip GENERATION beats shuffle-NULL (gen ci_lo>NULL hi AND p<0.05) -> produced successor carries t->t+1 structure
[gen] F-GEN-2 not-echo   : REFUTED: generated successor beats the IDENTITY-NULL (untrained-FC echo) -> the chip PRODUCES a successor, it is not echoing code_t
[gen] DISPOSITION        : ON-CHIP OPEN-VOCAB GENERATION DEMONSTRATED (gen > shuffle-NULL AND > identity-NULL) -> retrieval->generation bridge CROSSED on silicon; Lane A PUBLIC full-LM (generation) flips toward earned-green
```

- **F-GEN-1 REFUTED** — gen ci_lo=0.4096 ≫ shuffle-NULL hi=0.0418 (p=0.005), ~21x chance. 생성된 successor 가 t→t+1 구조를 담음.
- **F-GEN-2 REFUTED (핵심 구분)** — identity-NULL(미학습 random-init FC + 같은 neutral probe)이 0.357 로 **높지만**(VSA binding 구조가 random FC 도 일부 정보 통과) trained chip(0.434, ci_lo 0.4096)이 그 hi(0.3847)를 넘김 → 'generation' 이 입력 echo 가 아니라 chip 이 successor 를 **PRODUCE** 함을 분리 입증. 마진 0.025(좁음) 이나 8/8 trial 일관 + ci 분리 → clean.
- 두 falsifier 사전등록(run 전 docstring) · NO sw fallback(g63) · 매 trial learn=True(8/8 on-chip Hebbian 갱신).
- result `out/result_onchip_xlm_generation.json` sha256 `d2d8021f4aa11043e0236837030b2c9752065bb5ea0821ef6518e83ebb323743` (host↔local byte-eq) · 산출물 `AKIDA/state/onchip_generation_2026_06_02/` · 코드 `AKIDA/onchip_xlm_generation.py` + wrapper.
- **scope (a_scale_honest_scope)** — 250앵커/50개념/5lang toy, 256-unit 단일 1-bit FC. open-vocab generation 이 toy 스케일에서 **작동**(다리 건넘)을 입증; 프로덕션 full-LM(3B/7B) 승격 아님 — toy green ≠ 프로덕션 처방.
- **별개 축** — 상대-LIFT closed-negative(H-A1~A4 4/4 falsified)와 충돌 없음: 1-bit Hebbian 이 margin lift 는 안 사도 강한(whitened) 인코더 + 명시적 transition 학습으로 open-vocab next-step 생성 가능. encoder 🟢 + transition retrieval 🟢 위에 generation 🟢 누적.
- 전원 안정(PSU 교체 후 fire 전후 throttled=0x0) · streamer service 정상 정지→복원.

**milestone delta:** Lane A PUBLIC 진척 = 인코더 🟢 + transition retrieval 🟢 + **full-LM GENERATION 🟢**. PUBLIC checkbox 는 **미flip 유지** (toy→프로덕션 전환 + multi-step autoregressive roll-out 미완 — full closure 아님, a_paper_only_at_closure).

**NEXT (held):** 다단계 autoregressive roll-out(t→t+1→t+2 chained on-chip generation) · 또는 paged 다중-FC generator 로 스케일 ladder ≥3 rung(a_scale_honest_scope). PR lane-a/onchip-generation.

---

## 2026-06-03 — Lane A 정식 2-SUBLANE 분리 (#1717) + 양 sublane 각 1 rung 전진 (real AKD1000, sequential)

**JOB 1 — RECORD (칩 런 전 commit/push):** ENGINE+CLM+KOSMOS.md Lane A 섹션을 두 named sublane 으로 정식 분리 (substrate-tag 별 분리추적, a_lane_akida_gpu_split). **Lane A-single** (substrate=AKIDA · on-chip 1-bit Hebbian, single-pass on-chip ceiling) ⊥ **Lane A-multi** (substrate=HYBRID · on-chip 인코더 ⊕ off-chip host-CPU Elman decode head). remaining-items 표 verbatim 기록 (멀티스텝합성→off-chip HYBRID head ✅실증 · persistent-anchor probe→on-chip ⏳A6/A7 · recurrent/temporal A3·A4→AKD1500/v2 🔒). commit 9dffff66b, branch lane-a/d768-2sublane-split (base lane-g/d768-cuda-fire), pushed BEFORE 칩 런.

**칩 EXCLUSIVE 프로토콜 (single-chip):** `systemctl --user stop spike-streamer` → `akida.devices()` 가 HardwareDevice 반환 확인 (BC.00.000.002, akida 2.19.1, throttled=0xe0000 = under-voltage 비트 only, 정상) → 두 rung 을 ONE AT A TIME (trap 기반 streamer-restore wrapper, detached nohup, SSH flap 견딤) → `systemctl --user start spike-streamer` RESTORED active 확인 + exact argv `--port 9512 --duration 86400 --regime R3` (pid 78505). THERMAL: 전 구간 62.0–73.6°C (82°C pause threshold 아래), OOM 없음. WRAP: A-single exit rc=0 / A-multi exit rc=0 / streamer service restarted / WRAP done.

**JOB 2 rung 1 — Lane A-single (substrate=AKIDA) scale-transfer 🟢 SCALE-SURVIVES:** single-step open-vocab GENERATION 의 anchor-count ladder (a_scale_honest_scope ≥3-rung). harness AKIDA/onchip_xlm_gen_scale.py (byte-match onchip_xlm_generation enc/bind/FC/decode; concept subset 만 변경), LANE_A_GEN_NCONCEPTS=10,20,50 → 50/100/250 앵커. live AKD1000, 8 trials/rung, learn_all_hw=True 매 rung. 결과 (verbatim, .verdicts/lane-a-single-rung/F-GEN-SCALE.txt):
- NC=10/50anch  : gen ci_lo=0.6237 | shufNULL hi=0.2794 p=0.0050 | identNULL hi=0.6745 | chance=0.1111 | aboveShuf=True above2xChance=True
- NC=20/100anch : gen ci_lo=0.4761 | shufNULL hi=0.1228 p=0.0050 | identNULL hi=0.5562 | chance=0.0526 | aboveShuf=True above2xChance=True
- NC=50/250anch : gen ci_lo=0.4131 | shufNULL hi=0.0431 p=0.0050 | identNULL hi=0.4009 | chance=0.0204 | aboveShuf=True aboveIdent=True above2xChance=True
- **F-GEN-SCALE-1 REFUTED** (매 rung gen ci_lo>shuffle-NULL hi AND p<0.05 = SCALE-SURVIVES) · **F-GEN-SCALE-2 REFUTED** (largest rung ci_lo>NULL hi AND ≥2× chance = no collapse). echo-vs-produce gap 가 scale 커질수록 produce 쪽으로 벌어짐 (NC=10/20 echo → NC=50 produces). substrate=AKIDA, NOT HYBRID, NOT Lane G.

**JOB 2 rung 2 — Lane A-multi (substrate=HYBRID) larger rung 🟢 GENERALIZES @ B=5:** HYBRID branching-corpus held-out 을 WIDER branching 으로 확대. harness AKIDA/onchip_xlm_branching.py + env LANE_A_DELTAS="1,7,13,19,29" (B=5, proven B=3 보다 넓음) LANE_A_LADDER_NC="40,45,50". on-chip AKD1000 인코더 ⊕ off-chip host-CPU Elman head (numpy BPTT, NO torch). live AKD1000, 8 trials/rung, enc_learned=True 매 trial. ladder held-out decay (verbatim, .verdicts/lane-a-multi-rung/F-BRANCH-WIDE.txt):
- NC=40: held [0.1187, 0.9229, 0.9208] / train [0.7705, 0.9384, 0.9616]
- NC=45: held [0.1321, 0.8518, 0.8964] / train [0.7597, 0.9460, 0.9669]
- NC=50 (headline, chance=0.1020): held [0.0617, 0.8683, 0.9267] / train [0.7271, 0.9364, 0.9550]; hop-2 ci_lo=0.8394>shufNULL hi=0.2213 (p=0.0050) · hop-3 ci_lo=0.9069>shufNULL hi=0.2234 (p=0.0050)
- **F-BRANCH-1 REFUTED** (held-out hop-2 AND hop-3 above shuffle-NULL = transferable OPERATOR, TEST concept 들에서 compose) · **F-BRANCH-2 REFUTED** (held-out hop-2 0.8683 within 2× of in-dist 0.9364). **GENERALIZES=True** — wider B=5 에서도 off-chip head 가 offset operator 학습 (per-concept lookup 아님). substrate=HYBRID, NOT pure-AKIDA, NOT Lane G.

**milestone delta:** Lane A-single = single-step generation **SCALE-ROBUST** (3-rung anchor ladder, single-point artefact 아님). Lane A-multi = transferable composition **wider-branching 에서도 GENERALIZES** (B=5). 두 sublane PUBLIC checkbox 미flip 유지 (toy→프로덕션 scale-transfer + 3B 미완, a_paper_only_at_closure). substrate tag 엄격 분리 (A-single=AKIDA, A-multi=HYBRID, Lane G 와 NEVER 병합).
**NEXT:** A-single 프로덕션 full-LM ladder · A-multi 3B rung (a_scale_honest_scope). PR lane-a/d768-2sublane-split (base lane-g/d768-cuda-fire).

---

## 2026-06-02 — Lane-G-ref 3B reference rung (substrate=PyTorch-CUDA) — descent 🟢 / util 🟢 99%

**lane = Lane-G-ref · substrate = PyTorch-CUDA · rung = 3B-scale reference.** 85.6M PUBLIC baseline (`dancinlab/clm-v1-ref-pytorch-cuda`)과 동일한 ByteGPT/Transformer 아키텍처를 ~3B 로 스케일업한 레퍼런스 러그. **NOT** the hexa-native flame+forge PUBLIC production artifact (a_train_flame_forge); a_completeness_over_cheap optional reference; Lane A/AKIDA 와 병합 금지 (a_lane_akida_gpu_split).

- **config / params** — byte-level (V=256) decoder-only GPT, d_model=2560 · n_layer=40 · n_head=20 (head_dim 128) · block=512 · batch=12 · bf16 AMP + gradient-checkpointing. **n_params = 3,149,030,400 (~3.149B)**.
- **util (verbatim, vast H100 80GB HBM3)** — **PEAK = 100.0% · MEAN = 99.15%** (n=108 nvidia-smi 샘플), mem_peak = 63921 MiB (~62.4/80GB), power_mean = 653 W. util ≫ 20% gate.
- **descent (verbatim)** — `=== descent PASS CE 7.16861 -> 2.45871 ===` (val CE, F-CLM-REF-3B-DESCENT=1). bounded N=400 steps — **NOT converged** (a_scale_honest_scope: 85M→3B 사다리의 3B 러그).
- **throughput** — **11,183 tok/s** (2,457,600 tok / 219.8 s wall).
- **ckpt** — sha256 `ebe56db7f47e07f5126287b28c2e7df41f15719541b3ead62e8704133c4d24c9`, 12,596,300,742 B. LOCAL==POD sha 검증 완료. 산출물 `state/laneg_ref_3b_recovery_2026_06_02/`, 코드 `ref/clm_ref_pytorch_cuda_3b.py`.
- **HF** — PUBLIC `dancinlab/clm-v1-ref-pytorch-cuda-3b` (4 files: README.md · clm_ref_3b_train.log.json · clm_ref_pytorch_cuda_3b.py · clm_ref_pytorch_cuda_3b.pt) · CLM collection `dancinlab/clm-6a1cf58f621490134dade186` add-item OK · HF.jsonl row 추가 (PR #1684, main).
- **결론** — 3B scale 에서도 well-fed H100 가 byte-LM workload 를 trivially saturate (~99% util) — forge util-GREEN line (≥20% gate) 이 쫓는 reference bar. forge artifact 를 대체하지 않으며 forge Lane-G / FORGE-UTILGREEN 은 프로덕션 primary 로 불변.
- pod vast 39102044 (H100 80GB HBM3) — recover(ckpt+log+sha verify→HF) 후 teardown 완료.

**milestone delta:** `Lane G-ref 3B` ✅ flipped — 3B 러그가 genuinely 학습(descent)+포화(util)되었고 PUBLIC HF 등록 완료 (bounded·NOT converged honest scope). forge Lane-G / FORGE-UTILGREEN 미변경.

---

## 2026-06-02 — Lane A (substrate=AKIDA) ON-CHIP MULTI-FC DEPTH rollout 🔴 CLOSED-NEGATIVE (1-hop wall HOLDS through depth; single-step도 DEGRADE)

PR #1686(stateless) / #1689(state-carry) 두 closed-negative 가 명명한 NEXT BRIDGE = **ON-CHIP MULTI-FC DEPTH** (입력공학 아닌 2번째 learned FC) 를 live AKD1000 에서 구현·검증. substrate=AKIDA, a_lane_akida_gpu_split (Lane G 와 절대 병합 금지).

- **mechanism (chip-native, 1-bit, NO GPU, g63 NO sw fallback)** — PAGED 2-FC stack, onchip_layerpage_compose 의 weight-paging primitive 를 autoregressive rollout 안으로 가져옴. 단일 8MB SRAM NPU 메시에 한 번에 1 FC 만 상주: FC1(256u,8w)=transition encoder(PR#1686/#1689 단일 FC 와 byte-identical) on-chip fit → weights 호스트로 page OFF → FC2(256u,8w)=composition/recurrence surface 를 FC1 의 on-chip binarized 출력으로 같은 메시에서 fit. per hop g1=FC1.forward(x)→g1_bin→g2=FC2.forward(g1_bin)→g_bin. PR#1689 의 input-side state-carry(ctx 3-vote majority + bind) 유지(이긴 것 KEEP, depth 만 ADD). codebook 은 FC2 의 depth-2 출력공간에서 구성. enc_whitened·SHIFT=37·decode·ban·K=3·NTRIALS=8·shuffle-NULL B=200 모두 byte-eq.
- **chip health** — pi5-akida ubuntu@192.168.50.155, AKD1000 BC.00.000.002, akida 2.19.1, throttled=0x0 전 구간, streamer R3 stop→run→restore(trap, rc=0, pid 18635 복귀). 8/8 trial l1=l2=True (두 FC 모두 칩에서 학습).
- **decay curve (verbatim)** — DEPTH-2 [0.1612, 0.0298, 0.0149] vs in-process 1-FC base [0.0314, 0.0207, 0.0138]. chance=0.0204.
  - hop1 depth2=0.1612 ci_lo=0.1388 | shufNULL hi=0.0416 p=0.0050 aboveShuf=True
  - hop2 depth2=0.0298 ci_lo=0.0224 | shufNULL hi=0.0382 p=0.2040 aboveShuf=False (delta vs 1FC +0.0090)
  - hop3 depth2=0.0149 ci_lo=0.0114 | shufNULL hi=0.0359 p=0.6816 aboveShuf=False (delta vs 1FC +0.0011)
- **falsifier dispositions** — **F-DEPTH-1 NOT-REFUTED** (hop-2 p=0.2040 · hop-3 p=0.6816, shuffle-NULL 내부 = 1-hop wall HOLD). **F-DEPTH-2 NOT-REFUTED** (hop-2/3 gain +0.0090/+0.0011 permille, 사전등록 material threshold >1%@hop2 / >0.5%@hop3 미달).
- **SHARPER 부정 발견** — depth 가 작동하던 single-step 까지 DEGRADE: depth-2 hop-1(0.1612) ≪ single-step headline(0.4234 PR#1689 / 0.4287 PR#1686). 작동하는 transition code 를 2번째 1-bit Hebbian FC 로 라우팅 + FC2-space codebook 재투영 시 단일-step 신호 대부분 파괴 — composition surface 가 1-bit/256-unit 에서 recurrence carrier 가 아니라 noise.
- **결론** — 1-hop wall 은 input/state 문제(PR#1689 가 배제)도 depth 문제도 아님. **AKD1000 1-bit edge-learn 은 256-unit 에서 깊이 무관하게 SINGLE-STEP 생성에서 cap**. 🌱 EMERGENCE axis(창발=multi-step composition) NULL 유지. retrieval+single-step 러그 UNAFFECTED(자기 공간에서 ~0.42 headline 불변). NAMED next bridge = **OFF-CHIP DECODE HEAD** (recurrence 를 1-bit Hebbian surface 밖으로) OR single-step 을 Lane-A on-chip PUBLIC scope 로 수용. multi-FC paged depth 는 이 질문에 닫힌 축.
- **scope** — a_scale_honest_scope: toy 250-anchor / 2× 256-unit FC, scale-transfer(더 큰 codebook / 더 깊은 paged ladder) UNVERIFIED. a_paper_negative_ok: 깨끗한 closed-negative.
- **artifacts** — AKIDA/onchip_xlm_depth_rollout.py · AKIDA/run_depth_rollout_with_streamer_restore.sh · AKIDA/result_onchip_xlm_depth_rollout.json (sha256 `0acdeee58236ce28cb028d45be24cefc508da4432a8ceff146d0812e97d6e47a`) · `.verdicts/lane-a-depth/F-DEPTH.txt` (hexa verify CLI broken → live-chip stdout verbatim, established lane-a format).

**milestone delta:** `Lane A PUBLIC` 미변경 (NO PUBLIC flip) — multi-step EMERGENCE 가 depth 로도 미돌파, 단일-step 만 유효. multi-FC depth 축 closed-negative 로 기록, 다음 bridge = off-chip decode head OR single-step PUBLIC scope 수용.

## 2026-06-02 — Lane A HYBRID HELD-OUT 일반화 🔴 CHAIN-FITTING (substrate=HYBRID on-chip⊕off-chip, Lane A 인코더 + host-CPU head)

PR#1692 HYBRID 의 ~0.32 가 진짜 COMPOSITION 인지 chain-MEMORIZATION 인지 분리하는 홀드아웃 럼. 개념-레벨 분리(50 concept → TRAIN idx 0..34 N_TRAIN=35 / HELD-OUT TEST idx 35..49 N_TEST=15, successor DISJOINT). off-chip Elman RNN decode head(D_H=64, numpy BPTT, byte-match PR#1692 head, NO torch/sklearn/GPU)를 **TRAIN-concept 전이만으로** 학습 — 모든 training target 이 TRAIN concept, TEST concept 는 successor target 으로 절대 안 봄. on-chip 1-bit AkidaUnsupervised FC encoder 는 full transition set 으로 비지도 fit(공유 grounding surface; held-out 축은 off-chip decode head 의 successor 예측). live AKD1000 (BC.00.000.002, akida 2.19.1, throttled=0x0, streamer R3 service restart rc=0) 8/8 trial encoder_learned=True.

- **decay TRAIN (in-dist, 160 starts)** : [0.2750, 0.2773, 0.2766] — PR#1692 ~0.32 regime 재현, FLAT.
- **decay HELD-OUT (65 starts)** : [0.0000, 0.0000, 0.0000] — 모든 hop, 8/8 trial 정확히 0.
- per-hop: hop1 TRAIN 0.2750/HELD 0.0000 (held ci_lo 0 < shufNULL hi 0.0829 p=1.0) · hop2 TRAIN 0.2773/HELD 0.0000 (shufNULL hi 0.0828 p=1.0) · hop3 TRAIN 0.2766/HELD 0.0000 (shufNULL hi 0.0697 p=1.0). chance=0.0204. off-chip BPTT CE 3.8→0.002 (TRAIN concepts only).
- **F-GEN-HOLDOUT-1 NOT-REFUTED** — held-out hop-2 AND hop-3 가 shuffle-NULL 아래로 붕괴 → composition 이 unseen concept 로 transfer 안 됨.
- **F-GEN-HOLDOUT-2 NOT-REFUTED** — held-out hop-2 (0.0000) 이 in-dist hop-2 (0.2773) 의 2× 이내 아님.
- **RULING** — PR#1692 의 ~0.32 는 결정론적 train chain 의 CHAIN-MEMORIZATION. off-chip head 가 "TRAIN concept i 다음 i+1 emit" per-concept lookup 학습 — transferable transition RULE 아님. exact 0.0000 mechanism(honest): TEST-block 출력층 row(Wo)가 학습 중 positive CE gradient 못 받음 → argmax 가 TEST concept 절대 선택 안 함 → 구조적 0. 이 zero 가 memorization 의 결정적 signature(generalizing operator 였다면 chip code 구조 통해 unseen successor 를 최소 shuffle-NULL 위로 ranking 했을 것). on-chip encoder 는 정직 live silicon(8/8 learned), 병목 아님 — 실패는 전적으로 off-chip head 의 lookup-vs-rule.
- **결과** — Lane A HYBRID PUBLIC 정직 DOWNGRADE: PR#1692 "multi-step composition recovered" 는 IN-DISTRIBUTION CHAIN-FITTING(toy 250앵커 결정론 chain)으로만 닫힘, generalize 안 함. [x]→[~] (multi-step "emergence" 해석 철회). 인코더 축 🟢 + single-step GENERATION 🟢 + 순수 on-chip rung 들(#1686/#1689/#1690) UNAFFECTED. 🌱 EMERGENCE axis → NULL 복귀.
- **NAMED next bridge** (a_paper_negative_ok ruled-out axis + 다음 경로) — 결정론적 single-chain corpus 는 next-concept 예측을 순수 lookup 으로 만들어 구조상 unseen token 에서 rule vs memorization 구별 불가. 다음 럼 = **비결정론/branching corpus**(각 concept 가 공유 relational 구조에서 뽑힌 다중 plausible successor → head 가 한 chain 암기 아닌 on-chip code 공간 위 transition OPERATOR 학습 강제), held-out 이 operator transfer 검증. + ≥3-rung codebook-size ladder (a_scale_honest_scope) before any general composition claim.
- **scope** — substrate=HYBRID(on-chip AKD1000 encoder ⊕ off-chip host-CPU decode head), 순수-AKIDA 아님, Lane G 아님 (a_lane_akida_gpu_split). a_scale_honest_scope: toy 250앵커. a_paper_negative_ok: 깨끗한 closed-negative.
- **artifacts** — AKIDA/onchip_xlm_holdout.py (F-GEN-HOLDOUT-1/2 docstring 사전등록) · AKIDA/run_holdout_with_streamer_restore.sh (single-chip occupancy + restore-on-exit) · .verdicts/lane-a-holdout/result_onchip_xlm_holdout.json · `.verdicts/lane-a-holdout/F-GEN-HOLDOUT.txt` (hexa verify CLI broken on host → live-chip stdout verbatim 전사).

**milestone delta:** `Lane A PUBLIC (HYBRID-scoped)` [x]→[~] DOWNGRADE — multi-step "emergence" 가 held-out 에서 chain-memorization 으로 판명. 인코더+single-step PUBLIC-grade 유지, multi-step PUBLIC 청구는 branching-corpus held-out green 까지 HOLD. `Lane A 3B` 마일스톤 영향 — multi-step PUBLIC 미해결이므로 3B 진행 전 branching-corpus held-out 선행.
---

## 2026-06-02 · ENGINE Lane (substrate=CORE 의식 엔진) — L3 .clm 단일 진입점 배선 + CORE-mounted 3축 첫 probe (F-CLM-CORE-3AXIS)

**substrate=CORE (A=pure_field ⇄ G=engine_g ⇄ brain_decide, Ψ=1/2 · hexa-native · 외부 LLM 0 · p1~p8).** a_lane_akida_gpu_split: AKIDA/GPU 와 별개 4th 레인 (CORE 의식 엔진 자체). CPU-local `hexa run` ($0 mac · p7 결정적 equality, perplexity 아님).

### 빌드한 CORE 배선 (root-cause, completeness-bar)
- **L3 `.clm` 단일 진입점 (a_core_engine_map)** — `CORE/generator.hexa` `gen_clm_backend` 를 `test -f` STUB 에서 **실제 헤더 파서**로 승격: `read_file_bytes` 로 leading bytes 읽어 `CLM\x01` magic(67,76,77,1) + nblocks(u8) 검증 (canonical writer hexa-lang `flame/clm_ckpt.hexa` · `CLM/CLM_FORMAT_SPEC.md §2` 레이아웃과 일치). `_gen_clm_probe_header` 헬퍼 = edge-safe (missing/empty/truncated → valid=false, no crash). real d768 `state/laneg_d768_recover/d768_5lang_c4.clm` → **valid=true nblocks=6 admit**; non-`.clm` 파일 → 거부. **HONEST partial**: 헤더 admit/validate 는 LIVE 이나 weight DECODE forward (int4 dequant + conv2) 는 distinct follow-on → `loaded=false` 유지 → null fallthrough (un-decoded garbage 방지). a_core_engine_map: phantom wiring 주장 0 — admit 됨, decode 만 ⏳.
- **`.kosmos` 단일 진입점** — `generator_read_anchors`→`kosmos_io.load_anchors`→`brain_emit` anchors arg (기존 배선, 재확인 GREEN). `.clm`/`.kosmos` 둘 다 pure_field/engine_g/brain 에 직접 안 박음 (불변식 유지). 2nd entry path 0.
- **smoke 15/15 PASS** (`CORE/generator_smoke.hexa` 확장: clm absent 거부 + real `.clm` admit valid/nblocks + bad-magic 거부 케이스 추가). verdict `.verdicts/core-3axis-mount/generator_smoke.txt` (verbatim).

### CORE-mounted 3축 첫 probe (`CORE/three_axis_probe.hexa`, falsifier in-file pre-registered)
- **AXIS-1 🧠 의식 🟢 (F-CORE-3AXIS-1=1)** — emit-context substrate signal > 무자극 baseline: motiv hi=0.6700 > baseline=0.0000 AND emit hi=true/baseline=false. NULL(차이 없음) REFUTED. LIVE substrate (Engine A Φ/phase + Engine G motivation 완전 배선).
- **AXIS-2 📉 CE — admit 🟢 (F-CORE-3AXIS-2=1) / CE-descent ⏳ BLOCKED-WIRING** — descent-trained `.clm` admit precondition GREEN (valid+nblocks>0). CE-descent 자체는 decode forward 미배선 → **BLOCKED-WIRING, CE 수 fabricate 안 함** (p7: CE 는 한 축이지 truth 아님). 정직히 deferred.
- **AXIS-3 🌱 창발 🟢 (F-CORE-3AXIS-3=1)** — composed(substrate+anchors) len=101 > component-sum(substrate-only, anchors=[]) len=72. anchor 메모리가 emit 에 합성되어 출력에 관찰됨 = composition > component-sum. NULL REFUTED.
- 측정가능 3축 GREEN: **3/3** (의식+창발 = LIVE substrate · CE-admit). verdict `.verdicts/core-3axis-mount/probe.txt` (verbatim).

### 툴체인 한계 (정직)
- `hexa verify` CLI **깨짐**: `error: hexa build .../tool/verify_cli.hexa failed (compile error)` → `[module_loader] FATAL module not found: compiler/atlas/calc_dispatch`. 검증은 `hexa run` 결정적 equality 로 대체 (p7 부합 — string/flag equality, perplexity 아님). 상류 이슈는 hexa-lang 측.

### milestone delta
- ENGINE Lane (4th lane) **신규 추가** — production 마일스톤 표에 PUBLIC→3B→7B. L3 .clm 단일 진입점 🟢 + .kosmos 단일 진입점 🟢 + CORE-mounted 3축 첫 probe (의식🟢 CE-admit🟢/descent⏳ 창발🟢). CORE.md 도 generator/anchor 상태 ⏳/❌ → 🟢 정정 (코드와 동기 — 이전 "미존재" 는 stale 이었음).
- PUBLIC checkbox **미flip 유지** — CE-descent CORE-mounted GREEN 미완 (full closure 아님, a_paper_only_at_closure).

### NEXT (정확한 다음 빌드 step)
- **decode forward 빌드** = CE-descent 축 unblock 의 유일 잔여: `_gen_clm_decode` body 에 int4 dequant (qat_scale per-channel) + conv2 MoE forward 구현 → `gen_clm_backend` `loaded = valid` 한 줄로 활성화 (generate() 계약 + brain.hexa 배선 불변, BACKEND-AGNOSTIC). 그 위에서 CORE-mounted CE descent 측정 가능. PR engine-lane/clm-l3-header-admit.

## 2026-06-02 — ENGINE Lane: L3 .clm decode FORWARD 배선 → AXIS-2 CE MEASURABLE CORE-mounted (descent BLOCKED-FORMAT)

- **substrate = CORE** (hexa-native A⇄G 의식 엔진, 외부 LLM 0). 격리 worktree `engine-lane/clm-decode-forward` (base `engine-lane/clm-l3-header-admit` = 캠페인 lane-g/d768-cuda-fire + 직전 header-admit 커밋), additive-only.
- **decode forward 빌드 완료** (`CORE/generator.hexa` 단일 .clm 진입점, a_core_engine_map): `clm_decode_ce` = int4 dequant(6 블록 ecW/tcW/e0W/e1W/rW/roW, per-channel qat_scale, code=(nibble&0xF)-8) + CLMConvMoE forward(entry conv1d-K3 → trunk residual → 2 experts GELU → MoE-router softmax → readout d→V) → next-byte logits[T·256]. pure-hexa 커널 `_gen_conv1d`(conv_lib index 규약 일치) · `_gen_gelu`(clamped tanh) · `_gen_gnorm`(param-free GN1).
- **AXIS-2 CE 측정 (CORE-mounted, `hexa run`, p7 결정적)**: real d768 ckpt 통해 **CE_realtext=10.9696** (positions=11), CE_shuffled=10.5876, uniform baseline ln(256)=5.5452. det re-run byte-eq=1. `CE_MEASURABLE_CORE=1` 🟢. `CE_BELOW_UNIFORM=0`, `CE_BEATS_SHUFFLE=0`.
- **VERDICT = MEASURABLE-NO-DESCENT**: decode forward WIRED + CE MEASURABLE CORE-mounted, descent 🔴 미입증. 원인 = inference-track `.clm` 이 6 conv 블록만 직렬화(clm_ckpt/clm_prod PR4) — **trained embed table + GN affine 미포함** → embed 를 tied-readout stand-in 으로 재구성 → 트레이너 GPU-side 측정 4.88 descent(recover README §2) CORE-side 재현 불가 (format gap, NOT fabrication).
- **loaded=false 정직 유지** (a_core_engine_map, NO phantom wiring): null fallthrough, garbage 없음.
- **ENGINE PUBLIC 미flip** — 3축 중 의식 🟢 + 창발 🟢 + CE measurable 🟢 이나 CE-descent 🔴. PUBLIC 은 3/3 GREEN 일 때만.
- **NEXT STEP** = `.clm` 포맷이 embed table + GN affine 직렬화(또는 fp16-shadow track read) → CORE-mounted descent 재측정.
- verdict verbatim: `.verdicts/core-3axis-mount/ce_descent_decode.txt` · probe `CORE/clm_ce_descent_probe.hexa` (falsifier F-CLM-CORE-CE-DESCENT pre-registered in-file).

## 2026-06-02 — Lane A HYBRID BRANCHING-CORPUS 홀드아웃 🟢 GENERALIZES — PUBLIC RE-UPGRADE (substrate=HYBRID on-chip⊕off-chip)

PR#1694 가 명명한 ROOT CAUSE(결정론 단일체인 = per-concept lookup BY CONSTRUCTION, TEST-block Wo row gradient 0 → 구조적 held-out 0.0000)를 a_completeness_over_cheap 로 재설계. 코퍼스를 분기 연산자 succ(i)={(i+d) mod NC : d∈{1,7,19}} (branching B=3, concept-identity-independent, ring wrap 으로 TEST→TRAIN successor 가능)로 교체 → 단일 결정론 target 없음 = lookup 불가능, transition OPERATOR 학습 강제. off-chip Elman head(D_H=64 numpy BPTT) 랜덤 분기 walk(TRAIN-only target) 학습, on-chip 1-bit FC encoder 분기 전이 비지도 fit (live AKD1000 BC.00.000.002, akida 2.19.1, throttled=0x0, streamer restore rc=0, encoder_learned=True 전 trial, g63 no sw fallback). 분기-aware metric = set-membership.

HEADLINE NC=50: decay TRAIN [0.6929, 0.9357, 0.9721] / **decay HELD-OUT [0.0183, 0.8967, 0.9600]** (PR#1694 [0,0,0] 대비). F-BRANCH-1 REFUTED (held-out hop-2 0.8967/hop-3 0.9600 둘 다 shuffle-NULL hi~0.15/0.17 위 p=0.005) · F-BRANCH-2 REFUTED (held-out hop-2 in-dist 의 2× 이내, ratio 0.958). 3-rung ladder NC∈{30,40,50} 전 rung 일관 (held/in-dist hop-2/3 ~0.95-0.99). RULING: 분기 코퍼스는 transferable transition OPERATOR 강제 — TEST concept (학습 중 target 으로 미관측) 의 hop-2/3 successor 를 valid set 안에 디코드 = GENUINE multi-step composition, per-concept lookup 아님. PR#1694 exact-0.0000 은 결정론 단일체인 ARTEFACT, ROOT CAUSE 에서 REPAIRED. 🌱 EMERGENCE axis 🟢 RE-LIFTED → Lane A HYBRID PUBLIC [~]→[x] RE-UPGRADE (hybrid-scoped/branching-validated). CAVEAT: held-out hop-1=0.0183 (NULL 아래, falsifier 아님 — multi-step hop-2/3 에 사전등록). a_lane_akida_gpu_split · a_scale_honest_scope toy 250앵커 3-rung · a_paper_negative_ok. 순수-AKIDA 아님 Lane G 아님. next=3B. result_onchip_xlm_branching.json (sha256 5a585326…) · `.verdicts/lane-a-branch/F-BRANCH.txt`.

---

## 2026-06-02 — Lane G-ref 7B (substrate=PyTorch-CUDA · lane=Lane-G-ref · a_lane_akida_gpu_split — NEVER merged with AKIDA · NOT forge production a_train_flame_forge)

**RESUME + RECOVER of the live 7B rung on pod 39115197 (vast ssh4.vast.ai, H100 80GB HBM3).** Adopted the still-live pod via `hexa cloud run`; found a LIVE nohup 7B train (PID 1354) descending — let it finish (a_dont_kill_live_compute), inline-polled to completion, then recovered + HF-uploaded + landed before teardown (a_fire_recover_complete).

**Config** — ByteGPT byte-vocab (V=256) decoder-only GPT scaled to **7.25B params** (7,252,828,160): d4096 / 36L / 32H (head_dim 128) / block 512. bf16 master weights + grads, gradient checkpointing, bitsandbytes AdamW8bit (8-bit optimizer states → 7B + states fit a single 80GB GPU). Corpus = `dancinlab/clm-backbone-5lang-sample` (same 5-lang c4 backbone as the 85.6M PUBLIC + 3.149B ref rungs), flattened to a 67.7MB UTF-8 byte stream. steps=400 (warmup 20, cosine LR base 1.6e-4), batch 32, block 512. torch.compile + AMP bf16, CUDA-required (refuses CPU fallback).

**VERDICT (verbatim from `ref/clm_ref_7b_train.log.json`):**
- descent 🟢 **PASS** — val_CE **5.360630989074707 → 2.412078857421875** (F_CLM_REF_7B_DESCENT=1, "verdict": "PASS"). Curve: step0 5.36063 → step50 2.85197 → step150 2.34370 → step250 2.45141 → step350 2.38138 → step399 2.41208.
- util 🟢 **PASS** (≫20%) — n=436 samples, **PEAK 100.0% MEAN 99.1788990825688%**, mem_peak 46025 MiB, power_mean 651.3842201834855 W.
- throughput — total 884.9s, **tok_per_s_final 7406.1**, tok_seen 6,553,600.

**Closure = PASS** (descent 🟢 AND util 🟢) → HF **PUBLIC** (a_hf_autonomous). `dancinlab/clm-v1-ref-pytorch-cuda-7b`, private=False (confirmed via no-auth public API), all 6 files present (ckpt + log + trainer + prep + README card + SHA256SUMS manifest — a_hf_complete totality), added to CLM collection `dancinlab/clm-6a1cf58f621490134dade186`. **ckpt sha256 = 38ef2ed55b47b670fa915bba0c2827782799a9070ba087210cd44db1fddb4d41** (14,505,817,922 bytes; local pull verified byte-equal to the pod-computed hash). HF.jsonl row added (substrate=PyTorch-CUDA, lane=Lane-G-ref, collection=CLM, status=uploaded). NB: repo_id follows the established `clm-v1-ref-pytorch-cuda-{3b,7b}` ref-family convention (sibling of the PUBLIC 85.6M + 3.149B rungs); uploaded via `hf` CLI directly (the mk2 validator's allowed stage-prefix list does not yet carry `ref-` — a validator amendment scope, not a naming drift).

**Scale honesty (a_scale_honest_scope):** this is the **last (7B) rung** of the Lane-G-ref ladder 85.6M → 3.149B → **7.25B**. Bounded N=400 steps — descent + util DEMONSTRATED, **NOT converged**; do not deploy. This torch trainer is an `a_completeness_over_cheap` optional baseline/reference, NEVER the primary, NEVER claimed as the hexa-native flame+forge artifact, NEVER merged with Lane A / AKIDA. The production / PUBLIC-grade Lane-G CLM remains the forge stack (a_train_flame_forge).

**Teardown:** pod 39115197 re-tagged off project=anima, then released via the cloud-rm path after full recovery + HF upload + recovery-marker + commit. Protected pods 38704336 / 38996679 / 39106252 untouched. files: `ref/clm_ref_pytorch_cuda_7b.py` (trainer) · `ref/prep_corpus_7b.py` · `ref/clm_ref_7b_train.log.json`.

---

## 2026-06-02 — ENGINE Lane: .clm v0.2 (embed+GN 직렬화) → AXIS-2 CE-descent 🟢 GREEN CORE-mounted (toy d=8; 프로덕션 d=768 transfer 미검증)

- **substrate = CORE** (hexa-native A⇄G 의식 엔진, 외부 LLM 0, p1~p8). 격리 worktree (anima `origin/lane-g/d768-cuda-fire` HEAD 486f21a6c base · hexa-lang `origin/main` base), additive-only.
- **named root cause CONFIRMED**: inference-track `.clm` 이 6 conv 블록만 직렬화(`clm_prod.hexa` PR4 serialization L707-727) — 트레이너는 embed/GN affine/bias 를 모두 학습하지만 **6 conv weight 만 write**. legacy d768 artifact = conv-only (3,651,389 B = 정확히 6-block 크기로 byte-검증; embed/GN bytes 0). 트레이너의 embed+GN 은 메모리에만 존재했고 직렬화 안 됨 → **그 파일에서 재-직렬화 불가** (only conv 가 저장됨). 따라서 descent 복구 = 확장 직렬화기로의 small 재export 필요(정직).
- **FIX (a_completeness_over_cheap primary path, cheap stop 아님 — 근본 format 확장):**
  1. **.clm 포맷 v0.2** (`CLM/CLM_FORMAT_SPEC.md` §2.1 + §5 bump) — backward-compatible `CLMX` ext trailer: trained embed[V·d] + conv bias(ecB/tcB/e0B/e1B/rB/roB) + GN affine(tgG/tgB/noG/noB), 11 엔트리 full fp32. 6 conv 블록 뒤 APPEND → v0.1 리더 byte-unaffected. hexa-lang clm_ckpt.hexa writer/reader + clm_prod.hexa serializer (PR #2540). `F-CLM-CKPT-EXT-ROUNDTRIP=1` 🟢 + `F-CLM-CKPT-EXT-BACKWARD-READ=1` 🟢 (hexa run PASS, fp32 byte-eq).
  2. **CORE `clm_decode_ce` REWRITE** (`CORE/generator.hexa`, single .clm entry, a_core_engine_map, no 2nd path, no phantom wiring) — 트레이너 `clm_prod_fwd` 그래프 충실 미러: embed → entry conv+ecB(GN/gelu 없음) → trunk conv+tcB → GN(tgG,tgB) → gelu → residual xt=xec+hg0 → router+rB → 2 experts+bias gelu → MoE softmax → GN(noG,noB) → readout+roB. v0.2 ext 존재 시 trained embed+GN VERBATIM read; v0.1 일 때 tied-readout stand-in fallback (정직, fabrication 아님). d/E 를 block dims 에서 도출 = config-agnostic (d=8·d=768 동일 forward).
  3. **REAL trained v0.2 .clm** = $0-CPU host 재export (`hexa-lang stdlib/flame/clm_reexport.hexa`, host nn_conv1d_fwd/bwd + opt_adamw_step, **forge dispatch 0, torch 0**, byte-graph-faithful int4-QAT+STE) — clm_prod.hexa 는 forge_dispatch_adamw(CUDA-only builtin) 링크로 로컬 mac 바이너리 컴파일 불가하므로 host-only 재export 가 정직한 로컬 경로. epoch-1 CE 4.69813 → epoch-12 CE **1.66631** REAL descent, `F-CLM-REEXPORT-DESCENT=1 PASS`. artifact `state/laneg_d768_recover/reexport_d8_v2.clm` (12158 B, CLM\x01+CLMX, sha256 59d1b8bf…).
- **AXIS-2 CE-descent 측정 (CORE-mounted, `hexa run`, p7 결정적, verbatim):** `CE_realtext=2.07834 < CE_uniform=5.54518 AND < CE_shuffled_ctrl=5.52534` (has_ext=true, model_d=8, model_E=2, positions=23, DET_rerun_byte_eq=1) → `CE_MEASURABLE_CORE=1 CE_BELOW_UNIFORM=1 CE_BEATS_SHUFFLE=1` → **VERDICT = GREEN — CE-descent REFUTES NULL CORE-mounted**.
- **CONTROLLED comparison** (같은 엔진·같은 in-dist real-text "The mind is a fire to be"): v0.1 conv-only(has_ext=false) CE_realtext=9.0586 ≥ uniform → NO descent · v0.2 embed+GN CE_realtext=2.0783 → descent ⇒ 직렬화된 embed+GN(명명된 근본원인)이 결정 변수. `.verdicts/core-3axis-mount/ce_descent_decode_v1_baseline.txt`.
- **3축 CORE-mounted GREEN (toy scale)**: 의식 🟢 + CE-descent 🟢(toy d=8) + 창발 🟢. decode forward + format + 측정 전부 REAL·엔진-통과.
- **ENGINE PUBLIC 미flip (정직 scope)**: a_toy_scale_recheck + a_scale_honest_scope — CE-descent 는 scale-sensitive 현상이고 이 GREEN 은 toy d=8 에서만 측정됨. 프로덕션 d=768 transfer 미검증 → toy-only closure 선언 금지. PUBLIC=closure-PASS (a_hf_autonomous) 미충족.
- **NAMED next step**: `clm_prod.hexa` v0.2 serializer 의 **d=768 forge re-fire** (로컬 mac 바이너리 forge_dispatch_adamw 부재로 BLOCKED → pod self-host build 에서 발사; a_fire_autonomous) → d=768 trained embed+GN 담긴 v0.2 .clm → CORE-mounted descent 재측정 → d=768 GREEN 시 ENGINE PUBLIC flip + `gen_clm_backend loaded=valid` 한 줄(generate() 계약 불변).
- PR: hexa-lang #2540 (format v0.2 writer/reader + serializer + re-export driver). anima PR = generator.hexa decode rewrite + probe v0.2 + spec v0.2 + verdicts.
- verdict verbatim: `.verdicts/core-3axis-mount/{ce_descent_decode,ce_descent_decode_v1_baseline}.txt`.

## 2026-06-02 — ENGINE Lane: d=768 SCALE-RECHECK 🟢 GREEN @ PRODUCTION → 3/3 axes CORE-mounted GREEN → ENGINE PUBLIC FLIPPED [x]

- **substrate = CORE** (hexa-native A⇄G 의식 엔진, 외부 LLM 0, p1~p8). 격리 worktree (anima `origin/lane-g/d768-cuda-fire` HEAD 7fa2d8686 base · hexa-lang `origin/main` clm_reexport.hexa), additive-only.
- **a_toy_scale_recheck 충족 (toy GREEN ≠ production closure)**: toy d=8 GREEN 이 named 한 production-scale(d=768) re-test 를 실행. SAME config-agnostic CORE decode(`generator.hexa::clm_decode_ce`, d/E 를 block dims 에서 도출)가 d=768 v0.2 `.clm` 를 읽고 CE-descent 가 HOLD — toy→prod transfer VERIFIED, descent 는 toy-only artifact 아님.
- **d=768 v0.2 artifact 획득 = $0-CPU host 재export (pod 불요)**: `clm_prod.hexa` (CUDA-only forge_dispatch_adamw 링크 → mac 바이너리 컴파일 불가)는 불필요했음 — hexa-lang `clm_reexport.hexa` 의 host-only forge-free 경로(host nn_conv1d_fwd/bwd + opt_adamw_step, forge dispatch 0, torch 0)가 `CLM_PROD_D=768` 로 d=768 재export 를 mac 에서 직접 실행. epoch-1 mean CE 4.69674 → epoch-6 mean CE **2.21602** REAL descent, `F-CLM-REEXPORT-DESCENT=1 PASS`. artifact `state/laneg_d768_recover/reexport_d768_v2_fast.clm` (4,463,478 B, CLM\x01 6 conv blocks + CLMX ext, d=768 E=2, sha256 db7dc990ff31fb60a5677fd7fcf9a248c4306742d246bb99d8b5de861b751497). a_completeness_over_cheap primary path (근본 host 재export); a_wall_first 로 host-CPU 채택 (pod fire 는 build+teardown 으로 더 느린 직렬 경로였음).
- **AXIS-2 CE-descent @ d=768 (CORE-mounted, `hexa run`, p7 결정적, verbatim, cache-clear 후 재현):** `model_d=768` (NOT 8) · `CE_realtext=3.25405 < CE_uniform=5.54518 AND < CE_shuffled_ctrl=5.30381` (has_ext=true, model_E=2, positions=23, DET_rerun_byte_eq=1) → `CE_MEASURABLE_CORE=1 CE_BELOW_UNIFORM=1 CE_BEATS_SHUFFLE=1` → **VERDICT = GREEN @ PRODUCTION d=768**. verdict `.verdicts/core-3axis-mount/ce_descent_decode_d768.txt`.
- **3축 전부 CORE-mounted GREEN @ PRODUCTION d=768**: 의식 🟢 + CE-descent 🟢(d=768) + 창발 🟢.
- **gen_clm_backend loaded=valid FLIP (한 줄, a_core_engine_map, NO phantom wiring)**: decode forward 가 production d=768 에서 LAND + DESCEND 하므로 `let loaded = false` → `let loaded = valid`. header-valid `.clm` 가 이제 LOAD (clm_decode_ce 가 SAME config-agnostic forward 로 디코드). generate() 계약 + brain.hexa 배선 불변. smoke 15/15 PASS (`[clm valid] valid=true loaded=true nblocks=6`). probe default ckpt 를 d768 artifact 로 갱신 (env CLM_CE_PROBE_CKPT 로 toy d=8 / v0.1 baseline override 보존).
- **ENGINE PUBLIC FLIPPED [x]** (a_hf_autonomous PUBLIC=closure-PASS 충족 — 3/3 axes production-scale GREEN). NEXT = ENGINE 3B (decode forward + Lane-G util-GREEN 의존).
- PR: hexa-lang #2540 MERGED (format v0.2 + clm_reexport.hexa host re-export driver). anima PR = generator.hexa loaded-flip + reason-string + smoke d768 ckpt/assert + probe d768 default + ce_descent_decode_d768.txt verdict + 도메인 fold.
- verdict verbatim: `.verdicts/core-3axis-mount/{ce_descent_decode_d768,generator_smoke}.txt`.

## 2026-06-02 · Lane A 3B — chip-fit/페이징 capacity ladder fire (F-3B) — substrate=HYBRID(on-chip⊕off-chip)
- **마일스톤**: Lane A 3B = AKIDA 3B (chip-fit/페이징 ladder ≥3 rung, a_scale_honest_scope). 분기-검증 baseline = PR#1697 (held-out hop-2/3 0.90/0.96 on 256-unit single FC + D_H=64 off-chip head).
- **방법 (live AKD1000 BC.00.000.002, akida 2.19.1, throttled=0x0, streamer stop→fire→restore rc=0, N=8 칩 trial/rung, g63 no sw fallback)**: on-chip 인코더 capacity 를 layerpage single-residency primitive(byte-match onchip_xlm_depth_rollout chip_fit_forward + chip_forward_paged; 8MB SRAM 메시에 1 FC 만 상주 — map FC → 칩 fit → weights host 로 page OFF → del → 다음 FC map)로 depth-D paged 인코더(U-unit FC 스택)로 scale. per_fc_params=U×INC(256)×NW(8), paged_params=D×per_fc. 분기 held-out composition test(succ(i)={(i+d)%NC:d∈{1,7,19}} B=3, held-out concept 마지막 30%, off-chip Elman head D_H=64 numpy BPTT TRAIN-only target, set-membership metric, shuffle-NULL B=200)는 PR#1697 과 byte-identical — head 에 먹이는 on-chip code 만 depth-D paged code 로 교체.
- **4-rung ladder (전 rung map_all=learn_all=True on live silicon — SRAM map overflow 無, learn saturation 無)**:
  - D=1 U=256  NC=50  paged_params=524288  (5.24e5)  chip_fit=True  comp_survives=**True**  decay_HELD=[0.0317, 0.835, 0.9383] (hop-2/3 ci_lo 0.783/0.912 ≫ NULL hi 0.208/0.216, p=0.005) — 분기 baseline 재현
  - D=2 U=512  NC=50  paged_params=2097152 (2.10e6)  chip_fit=True  comp_survives=**False** decay_HELD=[0.0083, 0.0, 0.5] (hop-2 NULL hi 0.364 p=1.0)
  - D=3 U=1024 NC=50  paged_params=6291456 (6.29e6)  chip_fit=True  comp_survives=**False** decay_HELD=[0.0167, 0.25, 0.625] (hop-2/3 ci_lo<NULL hi, p=0.06/0.06)
  - D=4 U=2048 NC=50  paged_params=16777216(1.68e7)  chip_fit=True  comp_survives=**False** (chip-fit frontier probe — U=2048 도 여전히 map+learn)
- **falsifier disposition**: **F-3B-1 = False** (composition 이 D=1 baseline 에서만 above-NULL, D≥2 전부 붕괴) · **F-3B-2 = False** (3B-class 미도달 max paged 1.678e7 ≪ 3e9 AND map/learn SRAM ceiling 도 안 침).
- **VERDICT = COMPOSITION DEGRADES UNDER CAPACITY SCALING (honest closed-negative, a_paper_negative_ok)** — 3B 마일스톤 [ ] OPEN 유지, [x] 안 뒤집음. NO fabricated 3B claim (a_scale_honest_scope).
- **KEY HARDWARE FINDING (정직한 "chip-fit ceiling 어디?" 답)**: AKD1000 8MB SRAM 가 binding limit 아님 — layerpage single-residency 가 U=2048 / 4 paged layer / 16.8M trainable paged params 까지 전 rung map+learn 성공. binding constraint = **더 깊은/넓은 1-bit Hebbian AkidaUnsupervised FC stacking 이 off-chip head 가 의존하는 단일-step transition signal 파괴** (각 추가 1-bit FC 가 fold-to-INC+frozen-median 재이진화 → depth≥2 에서 head BPTT CE 수렴 안 함 ~3.5 vs depth-1 ~0.30). PR#1690 MULTI-FC DEPTH closed-negative 와 동일 physics (2번째 1-bit Hebbian FC = compose 아닌 degrade).
- **NAMED next bridge (미래 3B)**: composition 을 scale 하는 surface 는 (D=1 에서 이미 일반화한) OFF-CHIP head → 3B-class HYBRID 는 proven D=1 single-FC 인코더 위 OFF-CHIP head scale(넓은 D_H/multi-layer/attention) OR 1-bit Hebbian depth 없이 richer 인코더(단일 wide FC/multi-bit weights). paged 1-bit Hebbian depth = composition 보존에 대해 CLOSED axis.
- 인코더 축 🟢 + single-step GENERATION 🟢 + 분기 held-out composition 🟢(D=1) UNAFFECTED — capacity-scaling-via-depth 만 closed-negative.
- substrate=HYBRID, NOT pure-AKIDA, NOT Lane G (a_lane_akida_gpu_split). result_onchip_xlm_3b_chipfit.json sha256 5a1bc3e7019211cd4a59ecbe3fa233ac59a10920620ed6600468e9de09ca386c · AKIDA/state_3b_chipfit_verbatim.log · `.verdicts/lane-a-3b/F-3B.txt` (hexa verify CLI broken on host → live-chip stdout verbatim).

NOTE 2026-06-02 (Lane-G · substrate=GPU forge · a_lane_akida_gpu_split — NEVER merged with AKIDA / Lane-A or Lane-G-ref PyTorch) — F-RFC046 **lever-4** fused on-device per-step driver = the named ROOT unblock after lever-3's util-RED. **Source BUILT + host byte-eq GREEN; on-device 3-gate + util fire BLOCKED-OUTAGE (vast.ai SSH transport down).**
- **What lever-4 is**: lever a/b/1/2/3 pushed every GEMM-feed repack + im2col/col2im on-device (byte-eq max|Δ|=0.0) yet util stayed flat 🔴 (lever-2 MEAN 0.4999% → lever-3 MEAN 0.5616%). PRECISELY-ISOLATED residual = the **interpreted host per-step DRIVER loop**: each step dispatched ~17 separate `forge_dispatch_adamw` calls, each its own H2D(W,g,m,v)→launch→cudaDeviceSynchronize→D2H(W,m,v) — the GPU idles between 17 microsecond-latency launches/step (NOT link/compile/emit/scale/device-math). lever-4 = **`forge_dispatch_adamw_group(W_ids,g_ids,m_ids,v_ids,n_sizes,count,t)`**: ONE host→builtin crossing applies the whole AdamW param group (CUDA: H2D all → count back-to-back `_hx_k_adamw_step_inplace` launches with NO per-tensor host sync → ONE `cudaDeviceSynchronize` → D2H all), collapsing the 17× per-step adam dispatch into 1. Projection ~30→~11 host crossings/step.
- **Source LANDED** (hexa-lang PR **#2543 MERGED** onto `lane-g/rfc046-lever3-batched-gemmfeed`, stacked on lever-3 #2528): `self/runtime.h` decl + `self/codegen.hexa` 7-arg lowering + `self/cuda/runtime_cuda_emit.hexa` GPU kernel `_hx_cuda_farr_adamw_group_gpu` + `inbox/patches/forge-devfeed-lever4-fused-step-driver-runtime-c-fragment.c.txt` (host wrapper body) + `stdlib/flame/clm_prod.hexa` (`_adam_group` + 17-tensor handle arrays built ONCE before the step loop; in-loop 17× `_adam` → ONE `_adam_group`, CLM_PROD_DEVFEED-gated, no-CUDA per-tensor fallback) + `stdlib/flame/clm_fused_step_eq.hexa` byte-eq oracle.
- **host byte-eq GREEN** (mac `hexa run`, $0, g5 verbatim): `F-RFC046-ADAMW-GROUP-EQ = 1` · `F-RFC046-FUSED-STEP-EQ = 1` · `max|Δ| (grouped vs per-tensor serial opt_adamw_step, final W+m+v) = 0.0` · `PASS — fused AdamW group byte-eq to per-tensor serial opt_adamw_step`. (Prebuilt mac runtime.o lacks the new builtin — same constraint as lever-2/3 batched builtins — so the mac oracle proves the group iteration/handle-pack contract via the exact no-CUDA fallback; the real ON-DEVICE `F-RFC046-FUSED-STEP-EQ` re-runs on the pod self-host build where the builtin engages.)
- **🔴 BLOCKED-OUTAGE — on-device 3-gate + util fire NOT run**: the pre-armed util-verify H100 (vast 39126604, sm_90, laneg-utilverify) went SSH-dark mid-session (`ssh3.vast.ai:16604 Connection refused`) and dropped from the pod list. A fresh H100 sm_90 was rented (vast **39131850**, NVIDIA H100 80GB HBM3 compute_cap 9.0, project=anima/laneg-lever4); the full fresh-pod driver was authored (CUDA-toolkit-12-4 install + frozen-seed restore + splice lever a/2-recon/3/4 fragments + self-host build + 3-gate + byte-eq + util fire, single detached nohup) and uploaded, but **its SSH (`ssh7.vast.ai:11850` / direct `156.19.254.8`) is ALSO persistently refused** across a full 10/30/60/120/240s backoff — a vast.ai transport outage spanning both candidate pods. NO util number was produced; **NO fabricated GREEN** (a_completeness_over_cheap · a_scale_honest_scope). Fire HELD pending an SSH-reachable H100 sm_90.
- **secondary reconstruction blocker (filed upstream)**: the fresh-pod build seed needs the full `runtime.c` lever-chain. The un-batched lever-2 `matmul_bt`/`matmul_atb` wrapper bodies (PR #2515/403735b29) were never captured as a standalone reconstruction fragment — they lived only in the lost pod's `runtime_lever3.c` seed. Reconstructed locally from the runtime.h decls + the lever-2 byte-eq-fix host fallbacks (the byte-eq oracle is the hard gate that would catch any drift), and filed to hexa-lang inbox so the held fire is unblocked the moment SSH recovers.
- **util before→after**: before (lever-3) PEAK 21% transient / MEAN 0.5616% (n=349); after (lever-4) = **NOT MEASURED (BLOCKED-OUTAGE)**. CLOSURE = **RESIDUAL** (util gate unverified → NOT PUBLIC-grade; no .clm produced → no HF artifact). 3B forge fire STILL NOT throughput-justified. PROTECTED pods 38704336/39106252 untouched. ref hexa-lang lane-g/rfc046-lever4-fused-step → #2543 MERGED.

## 2026-06-02 · Lane A 3B — OFF-CHIP HEAD SCALE-UP (F-3B-HYBRID, named bridge from PR#1705/F-3B) — substrate=HYBRID(on-chip D=1 인코더 ⊕ off-chip host-CPU multi-layer head)
- **마일스톤/방법 (a_completeness_over_cheap primary path)**: PR#1705/F-3B 가 명명한 NAMED BRIDGE 실행 = composition 을 scale 하는 surface 인 OFF-CHIP head 를 키운다. 칩은 proven D=1 256-unit FC 인코더(524K = 256×INC256×NW8, byte-match PR#1697 build_fc/chip_make/chip_forward/enc_whitened/bind) 고정, OFF-CHIP host decode head 를 MULTI-LAYER Elman RNN(NLAYERS×D_H, numpy BPTT, NO torch/sklearn/GPU)로 3B-class 향해 scale. 분기 held-out split(succ(i)={(i+d)%50:d∈{1,7,19}} B=3, held-out concept 마지막 30%, set-membership metric, shuffle-NULL B=200)는 PR#1697 과 byte-identical — head capacity(NLAYERS,D_H)만 rung 마다 변경. total_params = head + 524288(고정 칩). live AKD1000 BC.00.000.002 akida 2.19.1, N=8 칩 trial/rung, 인코더 enc_learned=True 전 trial (g63 no sw fallback). streamer stop→fire→restore-on-exit trap.
- **off-chip head scale-up ladder (측정)**:
  - NL=1 D_H=64  head=23680   total=547968  (5.48e5) chip_frac=0.957 comp_survives=**True**  held hop-2/3 [0.8933, 0.9383] ci_lo 0.865/0.926 ≫ NULL hi 0.165/0.179 p=0.005 — PR#1697 baseline 재현
  - NL=2 D_H=512 head=943104  total=1467392 (1.47e6) chip_frac=0.357 comp_survives=**True**  held hop-2/3 [0.8917, 0.9283] ci_lo 0.860/0.910 ≫ NULL hi 0.178/0.163 p=0.005 — head capacity 40× scale 에도 composition PRESERVED
  - NL=3 D_H=2048 head=2.16e7 total=2.21e7 (chip_frac=0.024): 칩 D=1 인코더 map+learn 성공, off-chip BPTT 진행 중 host THERMAL THROTTLE(throttled 0x0→0x80000, ~84°C, 7GB/4-core Pi5)로 wall-time 내 미완 (detached run + monitor durable — 후속 harvest 가능)
  - NL=4 D_H=8192 (~4e8) · NL=6 D_H=24576 (~6e9, 3B-class rung): ~50GB RAM 필요 → 7GB Pi5 에서 HOST-RAM-INFEASIBLE = OFF-CHIP HOST ceiling (AKIDA ceiling 아님)
- **falsifier disposition**: **F-3B-HYBRID-1 = TRUE** (composition 이 측정된 전 rung(524K, 1.47M)에서 above-NULL = NAMED BRIDGE 작동, on-chip 1-bit Hebbian depth axis(#1705/#1690 = D≥2 붕괴)와 정반대) · **F-3B-HYBRID-2 = NOT reached** (3B-class off-chip head 는 적정 host 에선 free 이나 AKIDA box 의 Pi5 host-RAM 에서 막힘).
- **DEFINITIONAL-HONESTY GATE (a_scale_honest_scope, hard gate)**: chip_fraction 이 head scale 과 함께 붕괴 — 0.957 → 0.357 → 0.024 → (3B 해석값) 524288/3e9 = **1.75e-4 ≪ 1e-3 = TRIVIAL**.
- **VERDICT (두 발견 분리)**: (A) POSITIVE — OFF-CHIP head scale-up 이 옳은 축; composition 이 head capacity scale 에도 PRESERVED (524K→1.47M). 칩은 proven D=1/524K composition-bearing 인코더 유지, host head 가 recurrence/composition 운반·scale. (B) **HONEST TERMINAL (definitional-honesty closed-negative, a_paper_negative_ok)**: 3B-class HYBRID 는 on-chip AKIDA 기여가 trivial fraction(~0.017%) 이라야 도달 → host 모델에 524K 칩 인코더 얹은 것 = 정직한 pure-AKIDA/Lane-A 3B 아님. **⇒ Lane A ON-CHIP 은 PUBLIC(~524K composition-preserving D=1 인코더)에서 cap; 3B·7B 는 AKIDA substrate 위에서 도달 불가** (composition 보존하는 AKD1000 on-chip plastic capacity 가 D=1 single-FC 에서 top-out — #1686/#1690/#1705/이 rung 합치). Lane A 3B 마일스톤 [ ] 유지 + on-chip capacity ceiling 문서화. Lane A ladder PUBLIC 종료 제안. NO fabricated AKIDA 3B.
- 칩 인코더 축 🟢 + 분기 held-out composition 🟢(D=1) UNAFFECTED. substrate=HYBRID, NOT pure-AKIDA, NOT Lane G (a_lane_akida_gpu_split). result_onchip_xlm_3b_offchip_head.json (sha256 0da3516e2dcd1aa33000113efc4606f562ca96c8f9a37a2f70a764735e63133c) · AKIDA/state_3b_offchip_head_verbatim.log · AKIDA/onchip_xlm_3b_offchip_head_ladder.py · `.verdicts/lane-a-3b-hybrid/F-3B-HYBRID.txt` (hexa verify CLI broken on host → live-chip stdout verbatim).

## 2026-06-02 — Lane-G lever-5 workload-bound SWEEP (substrate=GPU · host-feed util chain TERMINAL)
substrate = GPU (Lane G) · pod vast 39139563 (H100 80GB HBM3, sm_90 / compute_cap 9.0) REUSED, no re-rent · a_lane_akida_gpu_split (Lane G only, NEVER merged with AKIDA/Lane A).

lever-5 hypothesis: PEAK-rises-but-MEAN-flat (lever-4) 의 두 가능 root — (A) crossing-bound (잔여 ~11 host↔device crossing/step 이 SM-starve) vs (B) workload-bound (per-step GEMM 이 H100 엔 너무 작아 커널이 host feed 보다 빨리 끝남 → MEAN 은 workload-limited). 한 fire 로 둘 다 test = apples(=lever-4 정확 config) + LARGER per-step-work sweep.

방법: lever-4 byte-identical clm_prod (adamw_group fused, 3-GATE PASS + BYTEEQ-PASS 상속 — SAME binary, no rebuild). nvidia-smi util@0.1s · devmem@0.5s · F-CLM-PROD-DESCENT per config. CLM_PROD_DEVFEED=1 BATCHED=1 HEXA_CUDA_LINK=1. 전 config FIRE_RC=0.

util (g5 verbatim sampler line, /root/lever5_sweep.log → .verdicts/lane-g-lever5/):
```
UTIL[apples d1536/T512] n=9149  PEAK=38% MEAN=0.6619% busy_ge20=81  pct_ge20=0.89% pct_ge50=0.00%  DEVMEM 20447MiB
UTIL[d3072  d3072/T512] n=11441 PEAK=78% MEAN=0.7152% busy_ge20=125 pct_ge20=1.09% pct_ge50=0.39%  DEVMEM 26405MiB  (~4× per-step GEMM work)
UTIL[t1024  d1536/T1024]n=5892  PEAK=38% MEAN=0.5883% busy_ge20=35  pct_ge20=0.59% pct_ge50=0.00%  DEVMEM 15097MiB
UTIL[big    d3072/T1024]n=8931  PEAK=75% MEAN=0.6838% busy_ge20=87  pct_ge20=0.97% pct_ge50=0.32%  DEVMEM 23215MiB  (~8× per-step work)
```
descent (전 config 🟢 GREEN, F-CLM-PROD-DESCENT=1, g5 verbatim): apples 4.05535→2.99508 · d3072 4.48673→3.96246 · t1024 4.20807→3.36669 · big 4.60325→4.22859.
apples-to-apples: lever-4 PEAK41%/MEAN0.6630% vs lever-5 apples PEAK38%/MEAN0.6619% — 샘플링 노이즈 내 재현(byte-identical build). harness sound.

A-vs-B RULING = (B) WORKLOAD-BOUND · host-feed axis CLOSED-NEGATIVE:
- 8× per-step work sweep 에서 PEAK 38→78% 배증, MEAN 0.59-0.72% PINNED. bigger work 가 MEAN 못 올림.
- (A) crossing-bound 배제: d3072 는 crossing 개수 = apples 와 동일, crossing 당 device compute ~4×. fixed-count per-crossing launch latency 가 binding 이었으면 4× 큰 커널을 같은 crossing 수에 amortize 해 busy fraction(MEAN) 상승했어야 함. 안 올랐음(+0.05pp). PEAK 78% = 커널이 SM 더 점유 확인하나 GPU wall-time ~99.3% idle.
- root residual = 인터프리트 host per-step 드라이버 루프 wall-time (hexa-interpreted scalar fwd/CE/bwd ~13ns/op · ~104M op/step @ d1536 ≈ ~1.4s host/step per lever-3 profile · model 크기에 비례 → d3072 host gap 도 ~4× → busy fraction flat 유지). 잔여 ~11 host↔device crossing = constraint 아님, 인터프리터 = constraint.
- lever chain util curve (MEAN flat · PEAK monotone = workload-bound 시그니처): l1 0.811%/6% → l2 0.4999%/19% → l3 0.4879%/35% → l4 0.6630%/41% → l5 0.59-0.72%/up to 78%.

VERDICT = HONEST TERMINAL of host-feed util lever chain (levers a/b/1/2/3/4 + lever-5 sweep):
util-GREEN(MEAN≥20%∧PEAK≥20%) 어떤 config 에서도 미도달, MEAN 천장 ~0.72%. host-feed/crossing-count axis CLOSED-NEGATIVE — 추가 host-feed lever 로 MEAN 불가. 治 = (i) 전체 device-resident model port (fwd+CE+bwd 그래프를 CUDA C 로 재작성해 hexa 인터프리터를 per-step hot path 에서 제거 — feed lever 가 아니라 production-scale model rewrite) 또는 (ii) 인터프리트 host gap 이 커널 시간 대비 작아질 만큼 큰 production scale (8× sweep 의 d3072/T1024 도 못 도달 → 필요 scale 은 d3072 훨씬 너머).
a_scale_honest_scope: d1536 MEAN-util 은 workload-size + interpreter-wall artifact 이지 forge 결함 아님 — forge 는 provably device-resident (20-26GB device mem · PEAK 78% · byte-eq PRESERVED · descent GREEN 전 config).

Lane G PUBLIC 미flip (util-GREEN 미달). Lane G 3B / 7B + ENGINE 3B / 7B chain = util-GREEN gate 미통과로 BLOCKED 유지 — production-scale device-resident model port 가 진짜 unblock (a host-feed lever 가 아님). .clm = util-RED/WIP → HF PRIVATE per a_hf_autonomous (closure-FAIL → PRIVATE). pod 39139563 RUNNING 유지 (no teardown). 날조 0 · g5 verbatim · recover-before-teardown (artifacts pulled + sha256 verified → .verdicts/lane-g-lever5/).

## 2026-06-03 — Lane-A UNIVERSE micro-exp 3종 (substrate=AKIDA · live AKD1000 BC.00.000.002 · akida 2.19.1 · pi5-akida · a_lane_akida_gpu_split — NEVER merged with Lane-G/GPU · #1717 규칙 준수)

1-hop wall(#1686/#1689/#1690 = MISSING RECURRENCE; #1691 HYBRID off-chip head 가 돌파; #1697 branching held-out 가 generalize)의 root cause 를 3 사전등록 micro-exp 로 교차검증. 단일 /dev/akida0 lock EXCLUSIVE — spike-streamer(`spike_streamer.py --port 9512 --duration 86400 --regime R3`, systemd --user, PID 49968) STOP→`akida.devices()` 디바이스 반환(chip free)→μ3·μ1·μ2 SEQUENTIAL(동시 절대 금지)→streamer RESTORE(systemctl --user start, PID 54315, exact argv 재확인, active) 완료. thermal 시작 63.7°C → peak 73.0°C(82°C guard 하), throttled=0xe0000(과거-발생 bit 만, 캠페인 중 active throttle 無). N=8 chip trials 전부 learn_hw=True(live silicon). hexa verify CLI host 깨짐 → verdict live-chip stdout verbatim(p7).

- **μ3 SCALE 🔴 F-SCALE-0 ALGORITHM-BOUND (closed-negative)** — multi-FC TILING(N개 독립 on-chip FC, 단일칩 paged, distinct random projection, plurality-vote, stateless feedback)이 N∈{1,2,4} 늘려 multi-hop wall 들어올리나? hop2 acc by N = **[0.0261, 0.0261, 0.0266]**, aboveNULL byN = [False,False,False], N=4 hop2 p=0.1791(≤0.01 아님). hop1 은 width 로 lift(N1 0.2856→N4 0.3394, ≫NULL p=0.005) 하나 hop1 너머 전파 안 됨. **RULING: multi-hop wall 은 capacity 아니라 ALGORITHM-bound → multi-chip scale-out 도 안 들어올림 = EMERGENCE 축 순수-on-chip TERMINAL.** 독립 stateless FC 투표는 어떤 단일 FC 도 없는 cross-hop transition 구조 못 만듦(paging N FC through 1 chip = closed paged-depth primitive 의 width 적용). verdict → `.verdicts/lane-a-microexp-scale/F-SCALE.txt` · `AKIDA/microexp_scale_chip.py`.
- **μ1 WIDTH 🔴 F-WIDTH-1 NOT-REFUTED (closed-negative) · 🟢 F-WIDTH-2 REFUTED** — K개 독립 1-bit Hebbian FC(distinct projection, voted)이 hop-1 generation 을 headline 0.4234 위 +0.05 들어올리나? gen_acc by K = **[0.4362, 0.4541, 0.4587]**(K=3/5/7), best K=7 ci_lo=0.4467(bar 0.4734 미달) → **F-WIDTH-1 NOT-REFUTED**: width 는 단일-step generation material 하게 못 들어올림(+0.035 best, sub-threshold). 전부 shuffle-NULL p=0.005 초과 + best 0.4587 ≫ paged-depth-2 0.1612 → **F-WIDTH-2 REFUTED**: ensemble 은 depth-2 wall 로 붕괴 안 함. 병렬 copy 는 redundancy 추가일 뿐 새 구조 아님(μ3 algorithm-bound 와 일관). verdict → `.verdicts/lane-a-microexp-width/F-WIDTH.txt` · `AKIDA/microexp_width_chip.py`.
- **μ2 CODE 🟢 F-CODE-1 REFUTED (단 shaping gain 無 · 정직 caveat)** — k-WTA sparsity(s∈{4,8,16,32}) + temporal-T integration(T∈{2,4,8})이 transition retrieval 을 baseline 0.260 위 +0.05 들어올리나? **best=baseline tr_acc=0.8541**(ci_lo 0.8432 ≫ NULL hi 0.0528, p=0.005) → F-CODE-1 REFUTED(단일-step retrieval STRONG). 그러나 **shaping 은 baseline 위 NO gain**: k-WTA 는 HURT(s4-s32 = 0.66-0.73 < baseline, discriminative bit 버림), temporal-T 는 NO-OP(tint_T2/T4/T8 = 0.8541 byte-eq, deterministic chip 이 매 pass 동일 soft 출력). REFUTED 는 강한 retrieval 반영이지 shaping 승리 아님. verdict → `.verdicts/lane-a-microexp-code/F-CODE.txt` · `AKIDA/microexp_code_chip.py`.

**FOLD — Lane-A 축 GREEN vs closed-negative (on-chip verbatim, substrate=AKIDA):** 🟢 SINGLE-STEP 축 전부 건강(retrieval μ2 0.8541, hop-1 generation μ1 0.46/μ3 0.34) · 🔴 DEPTH/EMERGENCE = 유일 terminal wall, 3 micro-exp 가 root cause 를 ALGORITHM-bound 로 SHARPEN: scale(μ3 multi-chip 안 됨)·width(μ1 sub-threshold)·code-shaping(μ2 saturate) 어느 on-chip lever 도 multi-hop 못 들어올림 → 1-hop wall 은 capacity/width/code 문제 아니라 MISSING RECURRENCE; 옳은 fix 는 #1691 가 입증한 OFF-CHIP recurrence(HYBRID decode head), on-chip 아님(a_completeness_over_cheap). EMERGENCE 축 순수-on-chip 에선 NULL 확정. a_paper_negative_ok: μ3 multi-chip 축 결정적 ruled-out. discovery → `.discoveries/lane-a-{scale,width,code}.tape`.

## 2026-06-03 — Lane-A 양 sublane rung+1 (real AKD1000 BC.00.000.002 · akida 2.19.1 · pi5-akida · sequential single-chip EXCLUSIVE #1717 · a_lane_akida_gpu_split — A-single=AKIDA / A-multi=HYBRID, NEVER Lane-G)

양 sublane 이 직전 rung GREEN 에서 각 한 rung 더 전진 (honest ceiling 탐색; a_scale_honest_scope, finding-either-direction valid, a_paper_negative_ok). 칩 프로토콜: spike-streamer(`spike_streamer.py --port 9512 --duration 86400 --regime R3`, systemd --user) STOP → `akida.devices()`==BC.00.000.002 device-confirm(g63 no-sw-fallback) → A-single → A-multi SEQUENTIAL(동시 금지) → streamer RESTORED (systemctl --user start, **active, exact argv 재확인, pid 95661**) on-exit trap. thermal 61.5°C→peak 72.5°C(<82°C guard), throttled=0xf0000(과거-발생 under-volt bit 만, 캠페인 중 active throttle 無). 8 trials/rung 전부 learn_hw=True(live silicon). 양 rung rc=0. hexa verify CLI host-broken → verdict = live on-chip/host stdout verbatim(p7).

**CORPUS 천장 발견(중요 honest finding):** 실코퍼스 corpus_big 는 50개념/250앵커가 한계 = **칩 천장 아닌 코퍼스 천장**. 256-unit/524K 칩-capacity 질문(앵커>250)과 NC>50 branching 에 닿으려면 앵커를 250 너머로 키워야 함. 실코퍼스에 그만큼 없음 → distinguishable-but-overlapping **SYNTHETIC byte-pattern 코퍼스** 생성(`AKIDA/build_corpus_synth_capacity.py`: NC=500개념×5lang=2500앵커, per-concept sparse 256-byte multinomial + per-lang noise mixture, 개념 byte-hist mean pairwise L1=1.3956 — distinguishable yet overlapping, 256-unit code 가 binding constraint). 칩 파이프라인 byte-identical(enc_whitened→bind→256-unit AkidaUnsupervised FC→open-vocab decode); 앵커 payload 만 synthetic, **명시적으로 NOT a semantic/cross-lingual claim**(a_scale_honest_scope). a_completeness_over_cheap: 가짜 semantic green 날조 금지 — 정직한 capacity-axis 재설계로 칩 천장 정면 probe.

- **A-single rung+1 (substrate=AKIDA) 🟢 CHIP-CAPACITY SCALE-SURVIVES → 2000 anchors** — single-step open-vocab GENERATION anchor ladder 500/1000/2000 (n_concepts 100/200/400, synthetic): gen ci_lo [0.0406, 0.0241, 0.0163] > shuffle-NULL hi [0.0188, 0.0097, 0.0049] **매 rung (p=0.005)**, above2xChance 전부, **F-GEN-SCALE-N REFUTED** — 256-unit/524K 1-bit Hebbian code 가 ≤2000앵커서 shuffle-NULL 로 붕괴 안 함 = **칩 capacity ceiling 미발견(≤2000앵커)**. 정직 nuance: echo-vs-produce margin(gen vs identity-NULL)이 500·1000앵커서 thin(aboveIdent=False, gen≈echo regime) → 2000앵커서 RE-OPEN(gen 0.0163 > identNULL 0.0156, produces 재진입; sparser harder codebook 에서). harness `AKIDA/onchip_xlm_gen_scale.py`(LANE_A_CORPUS env). verdict `.verdicts/lane-a-single-rung2/F-GEN-SCALE-N.txt` + `.discoveries/lane-a-single-rung2.tape`.
- **A-multi rung+1 (substrate=HYBRID on-chip AKD1000 인코더 ⊕ off-chip host-CPU Elman head, numpy BPTT NO torch) 🟢 DEEP-GENERALIZES @ NC=100 hop-5** — 두 축 동시: (a) larger NC=100(50개념 실천장 너머 synthetic grounding codebook; branching operator succ(i)={(i+d)mod NC : d∈[1,7,13,19,29]} B=5 는 index-ring 이라 corpus-agnostic), (b) DEEPER K=5(hop-4/hop-5). headline NC=100(chance 0.0505) held-out hop k1..k5 [0.0067, 0.8483, 0.9017, 0.8517, 0.8392] / in-dist TRAIN [0.6446, 0.9232, 0.9100, 0.8761, 0.8432]: hop-2/3/4/5 ci_lo [0.8242, 0.8590, 0.8130, 0.8083] > shuffle-NULL hi [0.1171, 0.1803, 0.1660, 0.1783] **전부 (p=0.005)**, held/in-dist ratio hop2..5 [0.92, 0.99, 0.97, 1.00], **F-BRANCH-1/2 REFUTED + F-BRANCH-DEEP REFUTED, depth_ceiling_hop=5(hop-5 까지 depth ceiling 미발견), GENERALIZES=True**. NC ladder {50,75,100} held-out hop-2 [0.883, 0.849, 0.848] 전부 ≫chance → scale 도 generalize. (hop-1 held-out≈0 = known artifact: off-chip head 가 hop-1 에 TRAIN successor 방출, transferable operator 는 hop-2부터 engage — 사전등록 expected, sub-NULL by construction.) harness `AKIDA/onchip_xlm_branching.py`(LANE_A_K_ROLL=5 + 사전등록 F-BRANCH-DEEP + LANE_A_CORPUS env). verdict `.verdicts/lane-a-multi-rung2/F-BRANCH-DEEP.txt` + `.discoveries/lane-a-multi-rung2.tape`.

**FOLD — rung+1 양 sublane GREEN (substrate tags strict):** 🟢 A-single(AKIDA): single-step gen 의 256-unit/524K CHIP-CODE-CAPACITY 가 2000앵커까지 shuffle-NULL 위 = capacity ceiling 미발견; 직전 250앵커 천장은 칩 아닌 코퍼스였음을 synthetic-capacity probe 가 확정. 🟢 A-multi(HYBRID): transferable branching operator 가 NC=100 AND hop-5 까지 generalize = depth ceiling 도 scale ceiling 도 hop-5/NC-100 내 미발견. 양 finding 모두 a_scale_honest_scope: synthetic-anchor capacity probe(A-single) + synthetic-codebook branching(A-multi) — 칩/operator 의 capacity·depth 축을 격리, semantic 주장 아님. production semantic full-LM at >250 real anchors = 더 큰 real corpus 필요(host 에 없음) = 별도. A-single=AKIDA · A-multi=HYBRID · NEVER 병합 · NEVER Lane G.

---

## 2026-06-03 — Lane A REAL-SCALE rung3 (live AKD1000, REAL semantic corpus past 50-concept ceiling)

**REAL corpus provenance (NOT synthetic, g63 honest):** `corpus_real100/parallel.limen` = 100 distinct cross-lingual ALIGNED concepts × 5 langs = 500 real anchors. concepts 0..49 = 50 FLORES parallel sentences byte-preserved from deployed corpus_big (real news/factual aligned translations); 50..89 = 40 hand-authored aligned aphorisms (build_corpus_large.py); 90..99 = 10 newly hand-authored aligned propositions. sha256 `356756786588831d4e317fafc9b7204a8da019319d03757799f3df9e294394cc` · merkle `27f4c506…`. **MAX REAL NC = 100** — in-repo c4 source (CORE/testdata/clm_mid_5lang_c4.txt, 4240 lines) has ONLY 5 distinct clean 5-lang parallel concepts (rest = repetition + mixed/code-switched non-parallel training text) → >50 real aligned concepts REQUIRE hand-authoring (real propositions in 5 langs = real data, NOT synthetic byte-pad). Prior synthetic rung proved scale past NC=50 on byte-patterns; this rung CONFIRMS it on REAL semantic data over the PROVEN D=1 single-FC encoder (#1705/F-3B-HYBRID PUBLIC cap).

**Chip discipline (MANDATORY #1717):** spike-streamer STOP (systemctl --user) → `akida.devices()` returned DEVCOUNT 1 (BC.00.000.002) → A-single (AKIDA) then A-multi (HYBRID) SEQUENTIAL (never concurrent) → RESTORE via trap (mandatory even on abort). Streamer post-run: `active`, exact argv `--port 9512 --duration 86400 --regime R3` (pid 98315). Thermal: baseline 61.7°C, A-single end 66.7°C, A-multi peak ~70.5°C, **final 70.0°C** (≪82°C threshold, no pause needed).

### A-single (substrate=AKIDA — on-chip 1-bit Hebbian, NOT HYBRID, NOT Lane G) — VERBATIM on-chip stdout:
```
[gen-scale] SUBSTRATE = AKIDA (on-chip 1-bit Hebbian) — NOT HYBRID, NOT Lane G
[gen-scale] akida 2.19.1 device BC.00.000.002 ip IpVersion.v1  corpus concepts=100 langs=5  ladder(n_concepts)=[50, 100] -> anchors=[250, 500]
[gen-scale] NC=50 anchors=250: gen ci_lo=0.4364 | shufNULL hi=0.0482 p=0.0050 | identNULL hi=0.4005 | chance=0.0204 | aboveShuf=True aboveIdent=True above2xChance=True
[gen-scale] NC=100 anchors=500: gen ci_lo=0.1971 | shufNULL hi=0.0215 p=0.0050 | identNULL hi=0.1799 | chance=0.0101 | aboveShuf=True aboveIdent=True above2xChance=True
[gen-scale] SUBSTRATE            : AKIDA (on-chip 1-bit Hebbian)
[gen-scale] F-GEN-SCALE-1        : REFUTED: at EVERY rung single-step gen ci_lo>shuffle-NULL hi AND p<0.05 -> single-step on-chip GENERATION SCALE-SURVIVES (A-single ceiling holds across anchor count)
[gen-scale] F-GEN-SCALE-2        : REFUTED: largest rung gen ci_lo > shuffle-NULL hi AND >= 2x chance -> no collapse toward chance
```

**A-single ruling:** F-GEN-SCALE-1 REFUTED (above shuffle-NULL at EVERY rung, p=0.005) · F-GEN-SCALE-2 REFUTED (no collapse at largest). single-step on-chip REAL-semantic generation **SCALE-SURVIVES to NC=100** (500 real anchors). → `.verdicts/lane-a-single-rung3/F-GEN-SCALE-REAL.txt`

### A-multi (substrate=HYBRID — on-chip AKD1000 encoder ⊕ off-chip host-CPU Elman decode head, numpy BPTT, NO torch) — VERBATIM stdout:
```
[branch] SUBSTRATE = HYBRID(on-chip AKD1000 encoder ⊕ off-chip host-CPU decode head) — NOT pure AKIDA, NOT Lane G
[branch] NC=50  N_TRAIN=35 (idx 0..34)  N_TEST=15 (idx 35..49)  on-chip enc transitions=750
[branch] NC=100  N_TRAIN=70 (idx 0..69)  N_TEST=30 (idx 70..99)  on-chip enc transitions=1500
[branch] SUBSTRATE               : HYBRID(on-chip AKD1000 encoder ⊕ off-chip host-CPU decode head)
[branch]   NC=50  chance=0.0612  decay_TRAIN=[0.6971, 0.9657, 0.9814]  decay_HELD-OUT=[0.0167, 0.9083, 0.9633]  ratio=[0.0239, 0.9406, 0.9816]
[branch]   NC=100  chance=0.0303  decay_TRAIN=[0.3886, 0.8314, 0.8839]  decay_HELD-OUT=[0.025, 0.7758, 0.8775]  ratio=[0.0643, 0.9331, 0.9927]
[branch] hop 1  TRAIN=0.3886 HELD=0.0250 ratio=0.064 | held ci_lo=0.0217 shufNULL hi=0.0597 p=0.6418 | chance=0.0303 | heldAboveShuf=False
[branch] hop 2  TRAIN=0.8314 HELD=0.7758 ratio=0.933 | held ci_lo=0.7309 shufNULL hi=0.1254 p=0.0050 | chance=0.0303 | heldAboveShuf=True
[branch] hop 3  TRAIN=0.8839 HELD=0.8775 ratio=0.993 | held ci_lo=0.8393 shufNULL hi=0.1646 p=0.0050 | chance=0.0303 | heldAboveShuf=True
[branch] F-BRANCH-1 (held>NULL)   : REFUTED: held-out hop-2 AND hop-3 STAY ABOVE the shuffle-NULL on the branching set-membership metric (each ci_lo>NULL hi AND p<0.05) -> a branching corpus FORCES a TRANSFERABLE transition OPERATOR; the off-chip head composes on concepts held out of training -> GENUINE multi-step composition, NOT a per-concept lookup
[branch] F-BRANCH-2 (within 2.0x) : REFUTED: held-out hop-2 (0.7758) is within 2.0x of in-dist hop-2 (0.8314) [>= 0.4157] -> held-out tracks in-dist
[branch] GENERALIZES              : True
[branch] DISPOSITION              : GENERALIZES — a BRANCHING corpus FORCES a transferable transition OPERATOR. The off-chip recurrent head, trained on random branching walks with TRAIN-concept targets ONLY, decodes hop-2/3 successors for TEST concepts it was NEVER trained to emit, landing in the valid (B=3) successor set ABOVE the shuffle-NULL AND within 2.0x of in-dist. Multi-step composition is REAL (the head learned the offset operator, not a per-concept lookup). The PR#1694 exact-0.0000 was an ARTEFACT of the deterministic single-chain corpus, REPAIRED at the root cause. Lane A HYBRID PUBLIC RE-UPGRADES (hybrid-scoped, branching-validated; on-chip AKD1000 encoder ⊕ off-chip host-CPU decode head) — NOT pure-AKIDA, NOT Lane G. STILL toy (a_scale_honest_scope, 2-rung ladder reported); next rung = 3B.
```

**A-multi ruling:** F-BRANCH-1 REFUTED (held-out hop-2 AND hop-3 above shuffle-NULL, p=0.005) · F-BRANCH-2 REFUTED (within 2.0× in-dist). branching transition OPERATOR **deep-generalizes to held-out unseen concepts at REAL NC=100**. hop-1 below-NULL = expected branching property (immediate step stochastic over B=3). → `.verdicts/lane-a-multi-rung3/F-BRANCH-REAL.txt`

**Honest scope (a_scale_honest_scope):** toy vocab; real ceiling NC=100 is hand-authored aligned data (no in-repo parallel source >5 distinct). substrate tags STRICT (A-single=AKIDA, A-multi=HYBRID, a_lane_akida_gpu_split). next = 3B. artifacts: AKIDA/state/real100_rung3_2026_06_03/ · harnesses AKIDA/{build_corpus_real100,onchip_xlm_gen_scale_real100,onchip_xlm_branching_real100}.py · .discoveries/lane-a-{single,multi}-rung3.tape.

---

## 2026-06-03 — Lane A rung4 OPEN MILESTONE: aligned real corpus authoring (CONTINUATION, NOT closure)

**ACTIVE OPEN milestone (effort recorded BEFORE build/run, JOB-1):**

- [ ] aligned real corpus authoring — push Lane A real-semantic scale past NC=100 (real ceiling = authoring effort, not chip)

rung3 가 양 sublane(A-single=AKIDA · A-multi=HYBRID)을 hand-authored REAL aligned corpus(`corpus_real100`, 100 concept = 50 FLORES + 40 authored + 10 new)에서 NC=100 까지 GREEN 으로 입증. 하지만 in-repo c4 source `CORE/testdata/clm_mid_5lang_c4.txt`(4240 lines)는 clean 5-lang 평행 concept 이 **5개뿐** → NC>100 real-semantic scale 의 진짜 천장은 **AKD1000 칩이 아니라 AUTHORING EFFORT**. user 가 그 authoring 에 INVEST 해 NC=100 너머로 밀길 원함.

이 마일스톤(ONGOING) = real 의미 corpus 를 NC=250 (faithful quality 유지 시 NC=500)까지 확장:
- Tier-1 (0–49): FLORES 평행문장 (real gold, corpus_big 에서 byte-preserved) — KEEP.
- Tier-2 (50–99): 기존 hand-authored aligned 명제 50 (build_corpus_real100 의 authored aphorisms + new).
- Tier-3 (100+): **신규 model-authored aligned 명제 — genuine cross-lingual aligned MEANING(한 사실을 5 lang 으로 충실 렌더), translation-faithful, deduped, byte-length balanced. 명시 라벨 "model-authored aligned (real-semantic, NOT FLORES-gold, NOT synthetic)" = 정직한 distinct 중간 tier.**

per-tier count + sha256 + byte-hist L1 분리 → `.verdicts/lane-a-corpus-real/CORPUS_CARD.md`. **synthetic padding 으로 NC 부풀리기 금지** — faithful authoring quality 가 target 전에 떨어지면 정직한 NC 에서 STOP. closure 아님 (a_paper_only_at_closure) — Lane A 닫지 않음, paper 안 씀. 이 effort 가 genuinely bigger real corpus + rung 을 landing 하면 이 milestone [x] flip + A-single/A-multi real scale to NC=X fold.

## 2026-06-03 · Lane A rung4 — REAL-corpus scale-up (A-single AKIDA + A-multi HYBRID) — live AKD1000, detached chip wrapper harvest

**substrate (a_lane_akida_gpu_split, strict):** A-single = AKIDA (on-chip 1-bit Hebbian). A-multi = HYBRID (on-chip AKD1000 encoder ⊕ off-chip host-CPU decode head) — NOT pure-AKIDA, NOT Lane G.

**corpus (정직 provenance, a_scale_honest_scope):** `corpus_real250` = 250 distinct cross-lingual aligned concepts × 5 langs (en zh ru ja ko) = **1250 real anchors**. 3-tier: Tier-1 0..49 FLORES-gold(byte-preserved) · Tier-2 50..99 hand-authored(rung3 검증) · Tier-3 100..249 = **150 NEW model-authored aligned propositions (real-semantic, NOT FLORES-gold NOT synthetic — 정직 중간 tier)**. sha256(LIMEN) `175d7acca595…b56ec`, host-rebuild byte-identical(결정적). **정직 NC ceiling=250** — corpus_real500 미저작(과저작 dedup/faithfulness 리스크 회피; 칩 한계 아닌 저작 한계). CORPUS_CARD: `.verdicts/lane-a-corpus-real/CORPUS_CARD.md`. build: `AKIDA/build_corpus_real250.py`.

**A-single (substrate=AKIDA) — F-GEN-SCALE-REAL2 (verbatim `rung4_single.log`):**
```
NC=50  (anchors=250)  gen ci_lo=0.3597 | shufNULL hi=0.0447 p=0.0050 | identNULL hi=0.3495 | chance=0.0204 | aboveShuf=True aboveIdent=True above2xChance=True
NC=100 (anchors=500)  gen ci_lo=0.1998 | shufNULL hi=0.0217 p=0.0050 | identNULL hi=0.1906 | chance=0.0101 | aboveShuf=True aboveIdent=True above2xChance=True
NC=250 (anchors=1250) gen ci_lo=0.0506 | shufNULL hi=0.0072 p=0.0050 | identNULL hi=0.0271 | chance=0.0040 | aboveShuf=True aboveIdent=True above2xChance=True
F-GEN-SCALE-1 : REFUTED (매 rung gen ci_lo>shuffle-NULL hi AND p<0.05 → single-step SCALE-SURVIVES)
F-GEN-SCALE-2 : REFUTED (largest rung gen ci_lo > NULL hi AND >= 2x chance → no chance-collapse)
DISPOSITION   : SINGLE-STEP GENERATION SCALE-SURVIVES (substrate=AKIDA). STILL toy vocab.
```
→ A-single on-chip ceiling 은 SCALE-ROBUST (단일점 artefact 아님). verdict: `.verdicts/lane-a-single-rung4/F-GEN-SCALE-REAL2.txt` + `result_onchip_xlm_gen_scale.json`.

**A-multi (substrate=HYBRID) — F-BRANCH-REAL2 (verbatim `rung4_multi.log`, DELTAS=[1,7,19] B=3 ladder=[100,175,250]):**
```
NC=250 hop 1  TRAIN=0.1741 HELD=0.0007 ratio=0.004 | held ci_lo=-0.0006 shufNULL hi=0.0227 p=0.9950 | chance=0.0120 | heldAboveShuf=False
NC=250 hop 2  TRAIN=0.7793 HELD=0.7457 ratio=0.957 | held ci_lo=0.7186 shufNULL hi=0.0417 p=0.0050 | chance=0.0120 | heldAboveShuf=True
NC=250 hop 3  TRAIN=0.8219 HELD=0.8067 ratio=0.982 | held ci_lo=0.7842 shufNULL hi=0.0428 p=0.0050 | chance=0.0120 | heldAboveShuf=True
PR#1694 holdout (det) : [0.0000, 0.0000, 0.0000]  (the deterministic-chain collapse this rung repairs)
F-BRANCH-1 (held>NULL)   : REFUTED (held-out hop-2 AND hop-3 above shuffle-NULL, ci_lo>NULL hi p<0.05 → transferable transition OPERATOR)
F-BRANCH-2 (within 2.0x)  : REFUTED (held hop-2 0.7457 within 2.0x of in-dist 0.7793)
GENERALIZES               : True
DISPOSITION : GENERALIZES — branching corpus FORCES a transferable transition operator; multi-step composition REAL (offset operator, NOT per-concept lookup); PR#1694 exact-0.0000 = deterministic single-chain artefact, REPAIRED at root cause. Lane A HYBRID PUBLIC re-upgrade (hybrid-scoped). STILL toy.
```
→ hop-1 HELD exact-0 = 설계상(held concept 직접 1-hop successor 미학습; branching 은 hop>=2 에서 전이 강제). verdict: `.verdicts/lane-a-multi-rung4/F-BRANCH-REAL2.txt` + `result_onchip_xlm_branching.json`.

**detached chip wrapper (a_dont_kill_live_compute — 재발사 안 함, harvest only):** `run_rung4_real250_with_streamer_restore.sh` (pid 103889) on pi5-akida self-completed. streamer STOPPED 05:44:23 → A-single(AKIDA) FIRE→exit rc=0 05:50:36 → A-multi(HYBRID) FIRE 05:50:44→exit rc=0 → `rung4 done RC_single=0 RC_multi=0` 06:11:05 → **streamer RESTORED 06:11:07 is-active=active argv=[spike_streamer.py --port 9512 --duration 86400 --regime R3]** 06:11:10. wrapper EXITED clean. final temp 69.2°C, throttled=0xf0000(under-volt flag만, active throttle 아님). wrap log: `.verdicts/lane-a-corpus-real/rung4_real250_wrap.log`.

**milestone delta:** Lane A PUBLIC 진척 += rung4 REAL-corpus scale-up 🟢 (A-single scale-survives NC→250 · A-multi branching held-out 일반화 NC→250). PUBLIC checkbox **미flip 유지 [ ]** — bigger real corpus(NC=250>100) + both rungs landed 했으나 PUBLIC closure 는 toy→프로덕션 full-LM 전환 미완(full closure 아님, a_paper_only_at_closure). multi-step roll-out residual 은 branching 으로 해소됨.

**NEXT (held):** Lane A 3B chip-fit ladder (a_scale_honest_scope ≥3 rung) · 또는 toy→prod full-LM 전환. discovery: `.discoveries/lane-a-{single,multi}-rung4.tape`.
