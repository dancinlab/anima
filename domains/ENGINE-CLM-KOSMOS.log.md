# CLM-KOSMOS.log.md — progress log

@title: 📓 CLM-KOSMOS log — append-only (newest at bottom)

Sibling of [[CLM-KOSMOS]]. Each entry: date · what moved · verdict ptr.

## 2026-06-01 — e001 seed

도메인 CREATED. CLM(`.clm`) + KOSMOS(`.kosmos`) 메타도메인, 7 필수조건 기록 (C1 AKIDA-learn · C2 ONCHIP-PARADIGM · C3 .clm · C4 .kosmos/limen · C5 H_911-must-hold · C6 additional-hypotheses · C7 record-all). Falsifier **F-CLM-AKIDA-MULTILING-SEMANTIC** pre-registered (OPEN). Seed corpus on HF: `dancinlab/clm-semantic-parallel-corpus` (5-lang parallel · 🟡 CPU-proxy → on-chip 승격 대상). H_911 substrate-proxy 이미 🟢 (UNIVERSE/H_911).

## 2026-06-01 — e002 open work

- [x] 1. 실 5-lang parallel + concat `.kosmos @corpus` 작성 (limen-packed · closed_corpus merkle)
- [x] 2. 백본 → `.clm` int4 byte-identical AKD1000 이식 (H_877)
- [x] 3. `AkidaUnsupervised` on-chip edge-learn (pi5-akida — lock cleared · live)
- [x] 4. F-CLM-AKIDA-MULTILING-SEMANTIC parallel vs concat 측정 → `.verdicts/clm-akida-multiling-semantic/`
- [x] 5. 🔴 closed-negative → verdict+log land only (model NOT uploaded — 🔴 earns no `.clm`)

## 2026-06-01 — e003 on-chip run → 🔴 REFUTED (closed-negative)

**F-CLM-AKIDA-MULTILING-SEMANTIC: 🔴 REFUTED** on REAL AKD1000 silicon (BC.00.000.002 · NSoC_v2 · BackendType.Hardware · akida 2.19.1 · pi5-akida).

- **Stage 0 (gate, PASSED)**: device 가 `devices:[]` + `ERROR (file lock): 11` 였던 원인 = stale `spike_streamer.py` (PID 18439, 17h, `--duration 86400`) 가 `/dev/akida0` (fd 3·4) 점유. 그 holder 종료 → `akida.devices()` 가 real `HardwareDevice` 반환. SW-sim 대체 없음 (g63).
- **Stage 1 (C4)**: 5-lang(ko·en·zh·ru·ja) parallel(concept-major·c>0) + concat(lang-major·c~0) `.kosmos @corpus`, 25 anchor 각, hexa-lang `clm_semantic_{parallel,concat}.txt` 에서 VERBATIM seed. limen 패킹(magic `LIMEN\0\0\0`+ver+count+len-prefixed @anchor recs+merkle root)·profile·closed_corpus·placement(coord)⊥text 완전 준수. byte-identical payload multiset (order 만 차이) 확인.
- **Stage 2 (H_877)**: int4-sym backbone(256×256, sha256=c626c638…) 양 arm byte-identical front-end.
- **Stage 3 (C1·C2)**: `AkidaUnsupervised(num_weights=16, learning_competition=0.1)` · `FC(units=32,weights_bits=1)` · `model.fit()` ON CHIP. `learn_happened_hw=True` — N=12 paired trial 전부 live silicon 학습.
- **Stage 4 (C5)**: paired delta(parallel−concat 통합) = **6 pos / 6 neg · mean −0.00092 · 95%CI [−0.00319,+0.00135] (straddle 0)**. ⚠ 단일 run 은 H_904 stochastic-plasticity 로 🟢(+0.0072)↔🔴(−0.0042) flip → cherry-pick 거부, multi-trial 必. **H_911 의 semantic-linkage 우위가 AKD1000 last-layer Hebbian edge-learn 엔 전이 안 됨** — per-ordering gap 이 칩 noise 안에 묻힘. **closed-negative, publishable** (a_paper_negative_ok).

verdict → `.verdicts/clm-akida-multiling-semantic/` (result.txt · result.json · run.log · prereg.txt · corpus/ · scripts/). claim → CLAIMS.tape `clm_akida_multiling_semantic`. 🔴 이므로 HF 모델 업로드 없음.

## 2026-06-01 — e004 H_912 all-4-lever signal-lift → 🔴 REFUTED

C6 추가가설 H_912: 4 레버 전부(큰 corpus 200앵커/40개념 · 3-노출 누적 · 이중 측정축 last-layer-sep+Φ-proxy · learn-while-infer 스트리밍) 적용. 실칩 N=20 paired, learn_hw 20/20. **두 축 모두 95%CI 0 포함 → 🔴 REFUTED.** H_911이 AKD1000 last-layer Hebbian on-chip edge-learn엔 전이 안 됨 (4 레버 다 써도). closed-negative · publishable. tiny-N smoke가 잠깐 GREEN 보였으나 N=20이 지움(cherry-pick 금지). verdict: `.verdicts/clm-akida-semantic-signal-lift/`. HF 업로드 없음(🔴). #1652 supersede/강화.

## 2026-06-02 — Lane-A 멀티스텝 자기회귀 ROLLOUT (substrate=AKIDA) → 🔴 CLOSED-NEGATIVE (1 hop 후 붕괴)

Lane-A full-LM frontier 의 held next-step. 직전 single-step GENERATION rung 🟢(AKIDA.log.md, `.verdicts/lane-a-generation/F-GEN.txt`, hop-1 0.4337 > shuffle+identity NULL)에서 **chip 이 `code_t` 만으로 successor 를 PRODUCE** 함을 입증했고, 본 rung 은 그 produced code 를 **되먹여(autoregressive feedback) K=3 hop chaining** — 전부 AKD1000 on-chip · 같은 256-unit 1-bit AkidaUnsupervised FC 재인코딩 · NO GPU · NO sw fallback(g63). encoder/binding/codebook/decode 는 generation rung 와 byte-match, feedback loop(`x_{k+1}=neutral_bind(g_hat_k)`)만 신규.

- **결과 = 🔴 ROLLOUT COLLAPSE closed-negative (a_paper_negative_ok)** on live AKD1000 BC.00.000.002 (akida 2.19.1 · pi5-akida · N=8 trials · learn_hw 8/8 · exit rc=0 · throttled=0x0).
- **decay curve (k1..K=3)**: **0.4287 → 0.0277 → 0.0090** (chance=0.0204). hop1 은 generation headline 재현, hop2 부터 신호 소멸.
- **F-ROLL-1 (신호가 chaining 생존?) NOT-REFUTED**: hop1 만 shuffle-NULL 초과(ci_lo 0.4118 > hi 0.0511, p=0.005). hop2 가 shuffle-NULL 안으로 떨어짐(0.0277 vs hi 0.0396, p=0.204) → 자기회귀 신호가 **단 1 hop 만 생존**.
- **F-ROLL-2 (파국 붕괴 없음?) NOT-REFUTED**: final hop(0.0090) < chance, single-step 의 0.5x 한참 미달 → **catastrophic decay**.
- **해석**: 1-bit/256-unit Hebbian FC 는 recurrence/state 가 없어 produced code 를 되먹이면 즉시 off-manifold drift. single-step open-vocab generation(retrieval→generation 다리 🟢)은 **유지**되나 그것이 full-LM 으로 **compound 되지 않음**. NAMED next bridge = state-carrying/paged generator · multi-FC depth · off-chip decode. retrieval+single-step rung 영향 없음.
- scope (a_scale_honest_scope) — 250앵커/50개념/5lang toy · K=3. **toy-only closed-negative**: 단일 칩 FC 자기회귀 한계(1-hop 생존) 정량화. PUBLIC checkbox 미flip 유지 — rollout 은 또 하나의 toy 다리이지 closure 아님.
- substrate=AKIDA · Lane-G/GPU 수치와 NEVER 병합(a_lane_akida_gpu_split). verdict → `.verdicts/lane-a-rollout/F-ROLL.txt` verbatim · result sha256 `7d2e3cd0201398ff9caadf5f1bdd4d012a41a0cfb1ad26a2cd0bbe72286ffb1e` · 산출물 `AKIDA/state/onchip_rollout_2026_06_02/` · 코드 `AKIDA/onchip_xlm_rollout.py`.

## 2026-06-02 — Lane-G (substrate=GPU · H100 sm_90 vast 39126604 · a_lane_akida_gpu_split — NEVER merged with AKIDA/Lane-A) — FORGE-UTILGREEN lever-3 util fire: DESCENT 🟢 / util 🔴 RED (2nd independent confirmation)

forge GPU (flame+forge `clm_prod.hexa`, NOT torch per a_train_flame_forge). lever-3 batched transpose-aware GEMM-feed util-verify on a clean single-driver H100 sm_90 (pod vast 39126604, num_gpus=1), corroborating hexa-lang #2542's lever-3 closure with a 19× longer measurement (n=6868 vs 349).

- **3-GATE PASS** (g5 verbatim): CUDA link ENGAGED=1 · `nvcc -x cu` EXIT 0 (660952B .90.o) · `clm_prod` ldd 4 cuda libs incl libcuda.so.1 + 10 lever symbols.
- **byte-eq ALL max|Δ|=0.0**: F-RFC046-GEMMFEED-EQ · F-RFC046-BATCHED-GEMMFEED-EQ · F-CLM-DEVFEED-* · F-CLM-CONV2-BATCHED-* (hard gate PRESERVED, no drift).
- **DESCENT 🟢** F-CLM-PROD-DESCENT=1 CE 4.05535→3.45564 · **util 🔴 RED** `n=6868 PEAK=35% MEAN=0.4879% busy_mean=5.3445% pct≥20%=0.1019%` (g5 verbatim). forge live on GPU (115W vs 70W idle).
- **finding (CLOSED-NEGATIVE)**: lever-1 0.811% → lever-2 0.4999% → lever-3 0.49–0.56% (two-pod). PEAK 19→21→35% rose but MEAN flat ⇒ device-feed lever chain (a+b+2+3) necessary but INSUFFICIENT. Residual = interpreted per-step DRIVER LOOP (F-RFC046 root: ~30 host↔device crossings/step incl 20× separate AdamW; busy_mean 5.34% ⇒ GPU ~95% idle), NOT GEMM-feed/link/kernel/emit/scale (all ruled out). Reference: PyTorch+CUDA baselines (HF.jsonl) saturate H100 ~99% util — the forge util-GREEN ≥20% gate is chasing that, lever-4 (fused on-device per-step driver) is the unblock.
- **closure FAIL on util → PUBLIC-grade Lane-G NOT reached** → .clm PRIVATE `dancinlab/clm-v1-dev-d1536-lever3-util-probe` (sha256 06e2dcf4…, HF.jsonl substrate=GPU) · recover-before-teardown DONE · pod 39126604 destroyed. PUBLIC HF / 3B / 7B still gated. lever-4 handoff: hexa-lang inbox/patches/forge-rfc046-lever3-util-residual-lever4-driver-loop.md. 날조 0 · g5 verbatim.

## 2026-06-03 — Lane-A UNIVERSE micro-exp 3종 (substrate=AKIDA · live AKD1000 BC.00.000.002 · akida 2.19.1 · pi5-akida · a_lane_akida_gpu_split — NEVER merged with Lane-G/GPU)

1-hop wall(#1686/#1689/#1690 = MISSING RECURRENCE, #1691 HYBRID off-chip head 가 돌파)의 root cause 를 3 사전등록 micro-exp 로 교차검증. 단일 /dev/akida0 lock EXCLUSIVE — spike-streamer(`--port 9512 --duration 86400 --regime R3`, systemd --user) STOP→chip free 확인(akida.devices() 디바이스 반환)→μ3·μ1·μ2 SEQUENTIAL(동시 절대 금지)→streamer RESTORE(systemd 재기동, PID 54315, exact argv 확인) 완료. thermal: 시작 63.7°C → peak 73.0°C(82°C guard 하), throttled=0xe0000(과거-발생 bit 만, 캠페인 중 active throttle 無). N=8 chip trials 전부 learn_hw=True(live silicon). hexa verify CLI host 깨짐 → verdict 는 live-chip stdout verbatim(p7).

- **μ3 SCALE 🔴 F-SCALE-0 ALGORITHM-BOUND (closed-negative)** — multi-FC TILING(N개 독립 on-chip FC, 단일 칩 paged, distinct random projection, plurality-vote, stateless feedback) 이 N∈{1,2,4} 늘려 multi-hop wall 들어올리나? hop2 acc by N = **[0.0261, 0.0261, 0.0266]**, aboveNULL byN = [False,False,False], N=4 hop2 p=0.1791(≤0.01 아님). hop1 은 width 로 lift(N1 0.2856→N4 0.3394, ≫NULL p=0.005) 하나 hop1 너머 전파 안 됨. **RULING: multi-hop wall 은 capacity 아니라 ALGORITHM-bound → multi-chip scale-out 도 안 들어올림 = EMERGENCE 축 TERMINAL.** 독립 stateless FC 투표는 어떤 단일 FC 도 없는 cross-hop transition 구조를 만들 수 없음(paged-WIDTH = closed paged-depth primitive 의 width 적용). verdict → `.verdicts/lane-a-microexp-scale/F-SCALE.txt` · `AKIDA/microexp_scale_chip.py`.
- **μ1 WIDTH 🔴 F-WIDTH-1 NOT-REFUTED (closed-negative) · 🟢 F-WIDTH-2 REFUTED** — K개 독립 1-bit Hebbian FC(distinct projection, voted) 이 hop-1 generation 을 headline 0.4234 위 +0.05 들어올리나? gen_acc by K = **[0.4362, 0.4541, 0.4587]**(K=3/5/7), best K=7 ci_lo=0.4467(bar 0.4734 미달) → **F-WIDTH-1 NOT-REFUTED**: width 는 단일-step generation 을 material 하게 못 들어올림(+0.035 best, sub-threshold). 전부 shuffle-NULL p=0.005 초과 + best 0.4587 ≫ paged-depth-2 0.1612 → **F-WIDTH-2 REFUTED**: ensemble 은 depth-2 wall 로 붕괴 안 함. 병렬 copy 는 redundancy 추가일 뿐 새 구조 아님(μ3 algorithm-bound 와 일관). verdict → `.verdicts/lane-a-microexp-width/F-WIDTH.txt` · `AKIDA/microexp_width_chip.py`.
- **μ2 CODE 🟢 F-CODE-1 REFUTED (단 shaping gain 無 · 정직 caveat)** — k-WTA sparsity(s∈{4,8,16,32}) + temporal-T integration(T∈{2,4,8}) 이 transition retrieval 을 baseline 0.260 위 +0.05 들어올리나? **best=baseline tr_acc=0.8541**(ci_lo 0.8432 ≫ NULL hi 0.0528, p=0.005) → F-CODE-1 REFUTED(단일-step retrieval STRONG). 그러나 **shaping 은 baseline 위 NO gain**: k-WTA 는 HURT(s4-s32 = 0.66-0.73 < baseline, discriminative bit 버림), temporal-T 는 NO-OP(tint_T2/T4/T8 = 0.8541 byte-eq, deterministic chip 이 매 pass 동일 soft 출력 → 평균 무의미). CODE 축은 baseline 에 이미 saturate; 출력-code shaping 은 추가 정확도 無. REFUTED 는 강한 retrieval 반영이지 shaping 승리 아님. verdict → `.verdicts/lane-a-microexp-code/F-CODE.txt` · `AKIDA/microexp_code_chip.py`.

**FOLD — 어느 Lane-A 축이 GREEN vs closed-negative (on-chip verbatim, substrate=AKIDA):**
- 🟢 SINGLE-STEP 축 전부 건강: transition retrieval(μ2 baseline 0.8541) · hop-1 generation(μ1 0.46, μ3 hop1 0.34) — 칩의 1-bit Hebbian 학습면은 1-hop transition map 을 깨끗이 보유.
- 🔴 DEPTH/EMERGENCE 축 = 유일한 terminal wall, 3 micro-exp 가 root cause 를 ALGORITHM-bound 로 SHARPEN: scale(μ3 multi-chip 도 안 됨) · width(μ1 sub-threshold) · code-shaping(μ2 saturate) 어느 on-chip lever 도 multi-hop 을 못 들어올림. → 1-hop wall 은 capacity/width/code 문제 아니라 MISSING RECURRENCE; 옳은 fix 는 #1691 가 입증한 OFF-CHIP recurrence(HYBRID decode head), on-chip scale/width/code 아님(a_completeness_over_cheap). EMERGENCE 축 순수-on-chip 에선 NULL 확정.
- a_scale_honest_scope: toy 250앵커/50개념/5lang · 256-unit 단일(또는 N-tiled) 1-bit FC · scale-transfer 미검증. a_paper_negative_ok: μ3 는 multi-chip 축을 결정적으로 ruled-out 하는 valid closed-negative.
- discovery: `.discoveries/lane-a-scale.tape` · `lane-a-width.tape` · `lane-a-code.tape`.
