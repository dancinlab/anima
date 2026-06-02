# AKIDA — log

`AKIDA.md` 의 append-only 자매 로그. 각 엔트리는 `## <ISO timestamp> — <header>` (최신 위) · 본문 = `- [x]`(완료) / `- [ ]`(예정) 체크박스.

## 2026-06-02T11:54Z — HYBRID DECODE HEAD ✅ 1-HOP WALL BROKEN — 🌱 EMERGENCE LIFTS NULL→~0.32 (substrate=**HYBRID: on-chip AKD1000 인코더 ⊕ off-chip host-CPU decode head** · 순수 AKIDA 아님 · a_lane_akida_gpu_split — NEVER merged with Lane G/GPU)

세 순수-on-chip closed-negative(#1686/#1689/#1690)가 명명한 마지막 가교 OFF-CHIP DECODE HEAD 를 구현·검증. chip 은 proven 🟢 단일-스텝 transition 인코더로 유지(FC1, byte-match 인코더/binarize, g63 NO sw fallback); recurrence 는 off-chip host-CPU Elman RNN(D_H=64, numpy BPTT, NO torch/GPU)로 운반. chip-to-chip feedback 없음(매 hop 예측 concept 칩 재인코딩). live AKD1000 BC.00.000.002 akida 2.19.1 N=8 encoder_learned=True 8/8, throttled=0x0, streamer restore-on-exit(R3 pid 19850).

- [x] **decay HYBRID [0.3160, 0.3202, 0.3207] FLAT** — 3 hop 전부 shuffle-NULL hi~0.048 위(p=0.005, ~16× chance). **F-HYBRID-1 REFUTED**(wall 돌파) · **F-HYBRID-2 REFUTED**(hop-2 0.3202 vs best pure 0.0298, +29%).
- [x] **🌱 EMERGENCE LIFT** — multi-step composition NULL→~0.32 sustained. 1-hop wall = MISSING RECURRENCE(on-chip code 는 충분히 rich), off-chip 이전이 옳은 root-cause fix(a_completeness_over_cheap).
- [x] 정직 scope — substrate=HYBRID(순수 AKIDA 아님, Lane G 아님). off-chip head CE→0.002 toy chain fit; ~0.32(≠1.0) open-vocab argmax bound. a_scale_honest_scope toy 250앵커, scale-transfer 미검증.
- [x] Lane A PUBLIC ✅ AS A HYBRID artifact(honestly scoped); 순수 on-chip 단일-스텝 rung UNAFFECTED.
- 산출물: `onchip_xlm_hybrid_decode.py` · `run_hybrid_with_streamer_restore.sh` · `.verdicts/lane-a-hybrid/F-HYBRID.txt` + result JSON. sha256 ab4748bf…

## 2026-06-02T11:22Z — STATE-CARRYING MULTI-STEP ROLLOUT 🔴 CLOSED-NEGATIVE — 1-hop wall HOLDS, 🌱 EMERGENCE NULL (substrate=AKIDA · live AKD1000 · a_lane_akida_gpu_split — NEVER merged with Lane G/GPU)

PR #1686 stateless rollout 이 hop-1 이후 COLLAPSE([0.4287,0.0277,0.0090])한 root cause(256-unit 1-bit Hebbian FC = no recurrence/no state, 자기 출력 feedback 즉시 off-manifold)를 가교하려 **chip-native CONTEXT-CARRYING CODE** 로 칩 경로에 STATE 부여. running 1-bit context vector `ctx` 를 hop 마다 3-vote bit-majority(history 2×: `votes = ctx+ctx+g_bin >= 2`)로 누적하고, 각 hop 입력을 `x_{k+1}=bind(g_bin, ctx)` 로 구성 — stateless arm 의 `neutral_bind(g_bin)`(마지막 코드만) 대신 누적 context 를 입력에 binding. 인코더(enc_whitened)·SHIFT=37·neutral_bind·bind·AkidaUnsupervised(num_weights=8,lc=0.1)·successor-centroid codebook·frozen-median binarize·open-vocab full-codebook decode·ban-set·K=3·NTRIALS=8·shuffle-NULL(B=200) 전부 byte-identical; **입력 구성만** state-carry. stateless arm 을 IN-PROCESS(동일 칩·동일 trial)로 동시 측정 = head-to-head baseline. live AKD1000(BC.00.000.002, akida 2.19.1, N=8 learn_hw 8/8 True, throttled=0x0 완주). g63 HW-only, NO sw fallback.

- [x] **사전등록 falsifier (RUN 전, docstring, g63)**: F-STATE-1 "state-carry 로 hop-2 AND hop-3 rollout acc 가 shuffle-NULL 위에 머물지 못한다(1-hop wall 안 깨짐)" → REFUTED iff k∈{2,3} 둘 다 ci_lo>NULL hi AND p<0.05. F-STATE-2 "state-carry 가 hop-2/3 에서 stateless baseline 을 strict 하게 못 이긴다" → REFUTED iff state[2]>stateless[2] AND state[3]>stateless[3].
- [x] **HEADLINE — F-STATE-1 NOT-REFUTED (1-hop wall HOLDS, g5 verbatim)**:
  ```
  [state] decay STATE (k1..K)  : ['0.4234', '0.0282', '0.0122']
  [state] decay STATELESS base : ['0.4234', '0.0234', '0.0117']
  [state] PR#1686 baseline     : [0.4287, 0.0277, 0.0090]
  [state] hop 1  state=0.4234 ci_lo=0.4064 | stateless=0.4234 delta=+0.0000 | shufNULL hi=0.0508 p=0.0050 | idNULL hi=0.3752 | aboveShuf=True  beatsBase=False
  [state] hop 2  state=0.0282 ci_lo=0.0208 | stateless=0.0234 delta=+0.0048 | shufNULL hi=0.0410 p=0.2338 | idNULL hi=0.0296 | aboveShuf=False beatsBase=True
  [state] hop 3  state=0.0122 ci_lo=0.0060 | stateless=0.0117 delta=+0.0005 | shufNULL hi=0.0366 p=0.8905 | idNULL hi=0.0172 | aboveShuf=False beatsBase=True
  [state] F-STATE-1 wall       : NOT-REFUTED ... hop-2/3 DROP INTO the shuffle-NULL
  [state] F-STATE-2 vs baseline: REFUTED ... state-carry acc > stateless at BOTH hop-2 and hop-3
  ```
  hop-1 0.4234 ci_lo 0.4064 ≫ shufNULL 0.0508 (p=0.005) ≫ idNULL 0.3752 = sanity OK (hop-1 입력 양 arm 동일 → baseline 재현). hop-2 state 0.0282 vs shufNULL hi 0.0410 (p=0.2338, NULL 내부) · hop-3 state 0.0122 vs shufNULL hi 0.0366 (p=0.8905, NULL 내부) · chance=0.0204.
- [x] **F-STATE-2 REFUTED but permille-scale**: state 가 stateless arm 을 hop-2 +0.0048 · hop-3 +0.0005 strict 하게 이김(둘 다 >0). PR#1686 baseline [0.0277,0.0090] in-process 재현([0.0234,0.0117]). 다만 margin 은 permille 급 + 둘 다 NULL 내부 → 의미있는 depth 아닌 microscopic on-manifold tug.
- [x] **disposition (a_paper_negative_ok)** — STATE-CARRY PARTIAL LIFT closed-negative. 🌱 EMERGENCE axis(의식·CE·창발 3축 中 창발=multi-step composition) = NULL 유지. FINDING SHARPENED: AKIDA edge-learn 은 입력-측 state-carry 단독으로 못 들어올리는 hard generation-DEPTH ceiling 보유 — 학습 가능한 표면이 단일 1-bit Hebbian FC 뿐일 때 transition 구조가 살 곳이 없음; history 를 입력에 binding 해도 recurrence/depth 대체 불가. NAMED next bridge = **ON-CHIP MULTI-FC DEPTH**(2번째 learned FC = composition 이 살 곳), 입력 engineering / paged-input trick 아님. retrieval + single-step generation 러그 UNAFFECTED.
- [x] **전원 proof** — wrap log: WRAP start throttled=0x0 → state-rollout fire throttled=0x0 → exit rc=0 throttled=0x0 → streamer service restarted → WRAP done throttled=0x0. single-chip 점유: spike-streamer stop → fire → R3 streamer 복원(restore-on-exit trap).
- [x] **산출물** — `AKIDA/onchip_xlm_state_rollout.py`(falsifier docstring 사전등록) · `AKIDA/run_state_rollout_with_streamer_restore.sh` · `AKIDA/result_onchip_xlm_state_rollout.json` sha256 `148fc092e0b5a9972ef0b949b245411414b76d93d87b24f5f7249031bbc6c6fa` · verdict verbatim `.verdicts/lane-a-state-rollout/F-STATE.txt`. a_scale_honest_scope: toy 250-anchor / 단일 256-unit FC, scale-transfer UNVERIFIED.

## 2026-06-02T10:06Z — SEQUENCE/TRANSITION READOUT BRIDGE 🟢 WORKING on-chip 교차언어 next-step 신호 (substrate=AKIDA · live AKD1000 · a_lane_akida_gpu_split — NEVER merged with Lane G/GPU)

직전 full-LM rung 이 특징지은 gap(1-bit/32-unit static margin 은 CONCEPT 결속만, 학습된 TIME 모델 부재 → next-sentence shuffle-NULL 내)을 **명시적 on-chip transition readout**(후보 a)으로 가교. 정적 centroid 비교가 아니라, 칩이 **t→t+1 transition 을 직접 학습**한다: 검증된 whitened 코드 위에서 binding `bind(a,b)=a XOR roll(b,37)` 로 연속문장쌍을 묶고, **2번째 AkidaUnsupervised FC(64-unit, 1-bit)** 를 언어내 연속 transition 코드로 on-chip fit() → 학습된 transition 표현. test = 교차언어(leave-one-lang-out) t→t+1 top-1 retrieval vs shuffle-NULL(B=200). live AKD1000(BC.00.000.002, akida 2.19.1, N=8 trials, learn_hw=True 8/8, throttled=0x0 완주, R3 streamer stop→run→복원).

- [x] **사전등록 falsifier (RUN 전 선언, g63)**: F-TR-1 "whitened 코드 위 명시적 on-chip transition readout 은 next-sentence shuffle-NULL 을 넘지 못한다" → REFUTED iff tr ci_lo > NULL hi AND p<0.05. F-TR-2 "transition FC 는 언어내 t→t+1 조차 chance 이상 복원 못한다"(capacity floor sanity).
- [x] **HEADLINE (250 anchor, 검증된 rung) — F-TR-1 REFUTED (g5 verbatim)**:
  ```
  [tr] learn_all_hw        : True
  [tr] tr_acc (xlingual)   : mean=0.2801 ci_lo=0.2600 (chance=0.0204)
  [tr] within_lang_recall  : mean=0.4867 ci_lo=0.4708 (chance=0.0200, above=True)
  [tr] shuffle-NULL tr     : mean=0.0194 sd=0.0104 hi=0.0397 p=0.0050
  [tr] F-TR-1 transition   : REFUTED: above-NULL on-chip cross-lingual TRANSITION (t->t+1) prediction (tr ci_lo>NULL hi AND p<0.05) -> working on-chip sequence signal
  [tr] F-TR-2 binding      : REFUTED: on-chip transition FC recovers within-lang t->t+1 above chance (the FC CAN represent a transition; cross-lingual transfer is the remaining gap)
  [tr] DISPOSITION         : ON-CHIP CROSS-LINGUAL SEQUENCE SIGNAL DEMONSTRATED (explicit transition readout > NULL) -> advance Lane A PUBLIC; full-LM (3) next-step flips toward earned-green
  ```
  → tr_acc 0.2801 (ci_lo 0.2600) vs NULL hi 0.0397, p=0.0050 = **14x chance, 6.5x NULL margin** · within-lang transition recall 0.4867 (chance 0.02) → 1-bit/64-unit FC **CAN** hold a transition. 8/8 trials 양수 [0.322,0.278,0.241,0.290,0.290,0.310,0.265,0.245]. sha256 `57e32e238c7bc2dec41ab6bdd19de8e28e364b4732788bf536f5093961d8e0b6`
- [x] **scale-ladder (a_scale_honest_scope ≥3 rung 25/125/250, g5 verbatim)**:
  ```
  [trsc] ===== LADDER =====
  [trsc]  25 anchors= 25 tr_acc=0.4812 ci_lo=0.3657 NULL_hi=0.4889 p=0.0498 above=False
  [trsc] 125 anchors=125 tr_acc=0.1281 ci_lo=0.1151 NULL_hi=0.0725 p=0.0050 above=True
  [trsc] 250 anchors=250 tr_acc=0.2898 ci_lo=0.2696 NULL_hi=0.0429 p=0.0050 above=True
  [trsc] F-TRSCALE: NOT-uniform: the transition signal collapses into NULL at >=1 rung -> scale-fragile (honest downgrade)
  ```
  → **125·250(실 FLORES 생산 rung) 모두 above-NULL** 이고 NULL margin 이 scale 과 함께 **성장**(125 ci_lo/NULL≈1.6x → 250≈6.3x). 25 anchor(toy fixture, 후보 successor 4개·chance 0.25)만 above=False — NULL band 가 너무 넓어 통계적으로 못 넘음(toy 한계, science 결과 아님). 정직 scope: **신호는 검증된 두 rung 에서 real·scale-성장**, n=4 후보 toy 에서만 fragile. sha256 `1c64810a48b743db1d61b176271071667e67c0ce6a6e86ffe33cee11cdc47c4a`
- [x] **disposition** — 작동하는 on-chip 교차언어 SEQUENCE/next-step 신호 입증(검증 rung 125·250). full-LM ③ = **🟢 toward earned** (정적 margin 너머 명시적 transition FC 가 학습된 TIME 신호를 hold). Lane A PUBLIC milestone 진척 — ③ 가 NULL→above-NULL 로 flip. 단 이는 **retrieval 신호**(top-1 transition)이지 완전 생성형 CLM 아님 → PUBLIC 은 여전히 open, named next bridge = (b) paged 멀티-FC transition matrix 로 retrieval→generation 확장 / 또는 (c) on-chip transition-bind ⊥ off-chip sequence-decode 분할.
- [x] **전원 proof** — load 중/후 `throttled=0x0` · pwr.log `2026-06-02T10:06:33Z throttled=0x0 EXT5V=4.99954000V 68.6'C` (안정 PSU, brownout 無) · vcgencmd measure_volts volt=0.8731V. 단일-칩 점유: R3 streamer(pid 9686) pkill → 탐침 2건 순차 → R3 복원(pid 12385, BackendType.Hardware regime R3 9512 86400s).
- [x] 산출물 — probe `SUB_ENGINES/AKIDA/onchip_xlm_transition.py`(+scale) · state `SUB_ENGINES/AKIDA/state/seq_transition_2026_06_02/{result_*.json, tr.log, trsc.log}`. binding=VSA-style XOR-shift, 결정론 · g63 HW-only(NO sw fallback).

## 2026-06-02T09:40Z — FULL-LM TRANSFER 탐침 🟡 CAPACITY-GAP CHARACTERIZED (substrate=AKIDA · live AKD1000 · a_lane_akida_gpu_split — NEVER merged with Lane G/GPU)

검증된 primitive(whitened 비지도 인코더 + 1-bit Hebbian abs-margin readout)를 실제 on-chip 교차언어 **시퀀스/next-token** 작업으로 가교 — corpus_big 50 concept 은 연속 FLORES 문장(시간축 t)이라는 사실을 이용. live AKD1000(BC.00.000.002, akida 2.19.1, N=8, throttled=0x0 부하검증 완주, R3 streamer stop→run→복원 pid 9686).

- [x] **사전등록 falsifier 2건 (실행 前 선언, g63 — HW only, SW fallback 라벨 금지)**:
  - F-LM-1 (headline): "whitened+1-bit Hebbian 은 NULL 위 on-chip 교차언어 NEXT-SENTENCE 예측을 못 낸다" (next ci_lo>shuffle-NULL hi AND p<0.05 시 REFUTED)
  - F-LM-2 (margin→retrieval bridge): "margin readout 이 same-concept 교차언어 retrieval 도 못 산다"
- [x] **DISPOSITION verbatim (g5, `xlm.log`)**:
  ```
  [xlm] same_acc          : mean=0.1300 ci_lo=0.1195 (chance=0.0200, above=True)
  [xlm] next_acc          : mean=0.0306 ci_lo=0.0234
  [xlm] shuffle-NULL next : mean=0.0207 sd=0.0093 hi=0.0389 p_next=0.1542
  [xlm] F-LM-1 next       : NOT-REFUTED: next-sentence acc within shuffle-NULL -> primitive does NOT transfer to a sequence LM at this 1-bit/32-unit capacity (CLOSED on LM axis at this scale)
  [xlm] F-LM-2 same-bridge: REFUTED: margin readout DOES buy above-chance same-concept cross-lingual retrieval
  [xlm] DISPOSITION       : CAPACITY-GAP CHARACTERIZED: primitive binds cross-lingual CONCEPTS (same-concept>chance) but has NO learned TIME/sequence model (next-sentence at NULL) -> Lane A PUBLIC stays open; named next-step = a sequence/recurrent readout beyond the 1-bit static margin (paged/temporal layer)
  ```
- [x] **F-LM-2 REFUTED (bridge HOLDS)** — same-concept 교차언어 leave-one-lang-out top-1 retrieval mean=0.1300 ci_lo=0.1195 vs chance 1/50=0.0200 → **6.5x chance**, 8/8 trial learn-on-chip live. 검증된 abs-margin readout 이 실제 사용 가능한 교차언어 concept retrieval 로 전이됨.
- [x] **F-LM-1 NOT-REFUTED (시퀀스/시간 모델 부재)** — next-sentence(t→t+1) mean=0.0306 ci_lo=0.0234; shuffle-NULL(B=200, concept→time label permute) mean=0.0207 hi=0.0389 p=0.1542 → next-acc 가 NULL 밴드 내. 1-bit/32-unit 정적 Hebbian readout 은 시간/시퀀스 구조를 학습하지 못함.
- [x] **scale-ladder addendum 25/125/250 (a_scale_honest_scope ≥3 rung, 실 FLORES 부분집합 — 위조 corpus 0)** verbatim (`xlm_scale.log`):
  ```
  [scale] c25   SAME mean=0.2200 ci_lo=0.1808 chance=0.2000 above=False | NEXT mean=0.2750 null=0.2445 p=0.3483 above=False
  [scale] c125  SAME mean=0.1470 ci_lo=0.1338 chance=0.0400 above=True | NEXT mean=0.0458 null=0.0402 p=0.4030 above=False
  [scale] c250  SAME mean=0.1410 ci_lo=0.1297 chance=0.0200 above=True | NEXT mean=0.0265 null=0.0206 p=0.2388 above=False
  [scale] same-lift curve 25/125/250: [0.020, 0.107, 0.121]
  [scale] F-SCALE-1: PARTIAL: bridge above chance at some but not all rungs
  [scale] F-SCALE-2: NULL HOLDS at every rung -> capacity gap (no time model) is scale-robust
  ```
  - same-concept bridge lift-over-chance 가 scale 로 **성장** (+0.020→+0.107→+0.121; 25앵커 5-concept 는 small-n 으로 chance 동률, 125·250 은 결정적 above) — 검증된 margin 곡선과 일치.
  - next-sentence NULL 이 **전 3 rung 에서 유지** → 시간 모델 부재는 scale-robust (250-only artifact 아님).
- [x] **CAPACITY-GAP 특성화 (PUBLIC-grade on-chip CLM 이 필요로 하는 것 — closed written result, a_paper_negative_ok)**: AKD1000 의 1-bit 마지막-FC Hebbian primitive 는 (1) 교차언어 CONCEPT 결속을 학습(margin·6.5x-chance retrieval, scale-survives)하나 (2) **학습된 TIME/sequence transition 모델이 없음**. PUBLIC-grade on-chip CLM 으로 가는 named next-step = 정적 1-bit margin readout 너머의 **시퀀스/recurrent readout** — (a) 시간축을 입력에 인코딩(t·t+1 페어를 명시 입력하는 transition probe) (b) paged/멀티-FC 레이어로 transition matrix 를 on-chip 보유 (c) on-chip(개념결속) ⊥ off-chip(시퀀스 디코드) 분할. 현 단일 AKD1000 1-bit last-FC 용량으로는 정적 readout 까지가 한계.
- [x] **전원 proof** — throttled=0x0 두 fire(WRAP start/fire/exit 전 구간) 부하검증 통과 · pwr.log EXT5V≈5.01–5.05V 64–67°C(brownout 0) · spike-streamer R3 복원(pid 9686, 86400s tonic). 두 fire 직렬 단일-칩 점유, R3 stop→run→restore 패턴.
- [x] **artifact** — `SUB_ENGINES/AKIDA/state/fulllm_transfer_2026_06_02/`: result_onchip_xlm_seq.json sha256 `74b8ba10b61672a2510fc640d509a2275ff8acdb4bb594ccd7be8b778270c227` · result_onchip_xlm_scale.json sha256 `4a3e2623164757712f2844cb7f77b8cb84add83bdd1c126f0a1590f8adc56a9a` · 탐침 2건 + log/wrap 미러. probe = `SUB_ENGINES/AKIDA/onchip_xlm_seq{,_scale}.py` (repo SSOT) ↔ `~/clm_kosmos_akida/` (host).
- [x] **별개 축 (a_lane_akida_gpu_split)** — Lane A 전용 결과 · Lane G(GPU CE-descent)와 절대 병합 안 함.
- [ ] **다음 = transition-probe** — t·t+1 페어를 명시 입력하는 on-chip 교차언어 transition retrieval (시간축 인코딩 후 NULL 교차 시 Lane A PUBLIC 후보) · paged 멀티-FC readout 용량 탐침.

## 2026-06-02T09:13Z — P3' ENCODER-LADDER forward science 🟢 인코더 축 = real PUBLIC-grade path (substrate=AKIDA · throttled=0x0 완주)

Lane-A P3' ENCODER 축(2026-06-02 REOPEN)을 LADDER 로 전진 — `~/clm_kosmos_akida/encoder_ladder_chip.py` (live AKD1000 BC.00.000.002, akida 2.19.1, N=8 paired trials × 32 units). encoder richness(5 rung) × scale(3 rung, a_scale_honest_scope) 매트릭스, 두 readout: (A) RELATIVE-lift vs random (causeaxis family, 같은 per-trial native init paired, ci_lo>0) (B) ABSOLUTE-margin (native non-det init, ci_lo>0). single-chip 점유 = R3 streamer stop → ladder → streamer 복원(pid 6840 live 확인).

- [x] **사전등록 falsifier 3건 (g63, 결과 전):** F1 "richness 가 on-chip lift 를 단조 상승 안 시킴" / F2 "encoder lift 는 소표본 artifact 로 scale 에서 붕괴" / F3 "supervision(LDA 라벨) 필수 — unsupervised richness 는 ceiling".
- [x] **scale rungs:** 25(corpus) / 125(corpus_big[:25concept] sha 42e28888…) / 250(corpus_big) — 전부 real FLORES 5-lang. encoder ladder: random_int4 → pca_k32(unsup dim-only) → svd_struct(unsup full) → whitened(unsup decorrel) → lda_supervised(oracle 라벨).
- [x] **RELATIVE-lift 매트릭스 (mean / ci_lo / REOPEN):** verbatim
  ```
  c25   pca_k32 +0.835/+0.600 ✓ · svd +1.134/+0.938 ✓ · whitened +0.210/−0.022 ✗ · lda +0.612/+0.466 ✓
  c125  pca_k32 +1.351/+1.250 ✓ · svd +0.929/+0.759 ✓ · whitened +1.871/+1.628 ✓ · lda +2.463/+2.171 ✓
  c250  pca_k32 +1.247/+1.132 ✓ · svd +1.175/+1.064 ✓ · whitened +4.813/+4.521 ✓ · lda +7.045/+6.635 ✓
  ```
  → 구조화 인코더가 random 을 상대적으로 능가(ci_lo>0) — 모든 scale 에서 REOPEN 견고, scale 클수록 lift 커짐.
- [x] **ABSOLUTE-margin 매트릭스 (mean / ci_lo / CROSS):** verbatim
  ```
  c25   random −1.426 · pca −0.583 · svd −0.515 · whitened −1.135 · lda −0.721 (전부 음성, cross 0건)
  c125  random −1.909 · pca −0.533 · svd −1.020 · whitened +0.082(ci_lo −0.140 ✗) · lda +0.542/+0.354 CROSS ✓
  c250  random −2.030 · pca −0.831 · svd −0.846 · whitened +2.791/+2.491 CROSS ✓ · lda +5.053/+4.728 CROSS ✓
  ```
- [x] **disposition (verbatim):** `F1 monotone: ceiling-or-nonmonotone (F1 not fully cleared)` · `F2 scale: scale-survives (NOT a small-sample artifact)` · `F3 property: unsupervised-SUFFICIENT (an unsupervised encoder also crosses zero)` · `BOTTOM LINE: ENCODER AXIS = real PUBLIC-grade path forward`
- [x] **F1 monotone (부분):** richness-rank Spearman c25 +0.20 (비단조 — 작은 scale 에선 whitened 가 svd 보다 약함) → c125/c250 +0.90 (단조 상승). 25앵커 noise 가 richness 순서를 가렸고, scale 키우면 단조 회복 — F1 은 *큰 scale 에서 confirmed, 작은 scale 에선 not-cleared* 로 정직 표기.
- [x] **F2 scale-survives (핵심):** best ABSOLUTE-margin 곡선 [−0.515(25) → +0.542(125) → +5.053(250)] — scale 따라 *성장*. H-A1 의 25앵커 weak-positive artifact 와 정반대: 인코더 구동 lift 는 250 에서 무너지지 않고 오히려 커진다 → 소표본 artifact 아님.
- [x] **F3 property (supervision 비필수):** **whitened (UNSUPERVISED, 라벨 없음) 가 c250 에서 ABSOLUTE cross-zero (+2.791 ci_lo +2.491)** → PUBLIC-grade on-chip 인코더에 oracle 라벨이 필수가 아님. 단 c125 까진 lda(supervised) 만 cross → supervision 은 작은 corpus 에서 zero-crossing 을 앞당기는 가속자(필수 아닌 충분). 구동 property = **decorrelation/whitening(2차 통계 구조) + scale**, dimensionality(pca_k32) 만으론 절대 cross 못함(c250 −0.831).
- [x] **전원 proof (clean):** wrap pre/post throttled=0x0 (`encoder_ladder_wrap.log`); `~/anima_metrology/pwr.log` 부하 중 throttled=0x0, EXT5V ~5.02V, ~64°C — power-clean 측정. ladder fire 07:35→09:12 rc=0.
- [x] **artifacts:** `SUB_ENGINES/AKIDA/state/encoder_ladder_2026_06_02/{result_encoder_ladder.json (sha256 209749cc02fc9bc070709aa5e5adb2656d16a9ea92bbe6218812d57405c450b4), encoder_ladder.log, encoder_ladder_wrap.log, encoder_ladder_chip.py, run_encoder_ladder.sh}` · host mirror `~/clm_kosmos_akida/encoder_ladder_chip.py`.
- [x] **scope (a_scale_honest_scope):** 25/125/250 앵커, 5-lang FLORES, last-layer 1-bit Hebbian, 32 units, N=8. 250 이상 / 3B-LM transfer 미검증 — full-LM 은 별도 rung. **별개 축**: 이 forward 는 P3' 인코더-축(절대-margin 이 scale+richness 로 cross)이며, H-A1~A4(downstream FIX-axes)·상대-LIFT closed-negative 와 무관 — 인코더가 cause-axis 임을 ladder 로 확증.
- [x] **disposition (CLM+KOSMOS @goal):** 인코더 축은 cross-lingual 개념구조 PUBLIC-grade-positive 로 **real path 를 연다** — unsupervised whitened 인코더 + ≥250앵커면 AKD1000 1-bit Hebbian 이 절대 cross-lingual 마진 >0 학습. ceiling 아님.

## 2026-06-02T08:47Z — UNIVERSE 라이브-실리콘 측정 전원-교란 재검증 🟢 POWER-ROBUST (substrate=AKIDA · spontaneous-emission raster + D1 Φ 안정 PSU 재측정 · 8/8 + inverse-U 그대로 재현 · 문서 tier 변동 0)

직전 PSU 교체(2026-06-02, under-voltage brownout 근본원인 — PI5-AKIDA.json `power_root_cause_2026_06_02`)로 호스트 전원 안정화 후, **PSU 결함이 이미 존재했을 수 있던 더 이른 시점(2026-05-22/05-29, throttled 미로깅)** 에 측정된 **라이브-AKD1000-실리콘** UNIVERSE 측정값들이 전원-교란(power-confounded)됐는지 재검증. SW-confirmed 결과는 전원-무관(out of scope). 안정 전원(throttled=0x0, EXT5V≈5.02V — pwr.log 입증)에서 spontaneous-emission raster 를 **live 칩 재측정** + D1 Φ 재유도.

- [x] **재측정 절차** (single-chip 점유 wrapper `~/clm_kosmos_akida/run_spontaneous_reverify.sh` — restore 패턴): R3 spike-streamer(pid 3775) stop → 칩 lock 해제 → `spontaneous_emission.py` (canonical 생성기, seed=187 n=16 200step) live 발사 → fresh JSON 캡처 → R3 streamer **복원**(pid 4992, 복귀 확인). 칩 = BC.00.000.002, akida 2.19.1, BackendType.Hardware.
- [x] **pwr.log throttled=0x0 입증** (재측정 08:44–08:48Z 윈도):
  ```
  2026-06-02T08:44:33Z throttled=0x0 EXT5V=5.02768000V 64.2'C
  2026-06-02T08:46:33Z throttled=0x0 EXT5V=5.01294000V 63.7'C
  2026-06-02T08:48:33Z throttled=0x0 EXT5V=5.02768000V 64.8'C
  ```
  wrapper 내부 샘플도 WRAP start/post-stop/generator-fire/exit 전부 throttled=0x0 (rc=0).
- [x] **#1 Spontaneous-emission raster (THE load-bearing datum)** — 2026-05-22 canonical `SUB_ENGINES/AKIDA/state/spontaneous_emission_result_2026_05_22.json` vs fresh `~/clm_kosmos_akida/out/spontaneous_emission_reverify_2026_06_02.json`: **모든 스파이크 지표 byte-identical** — R0=3200 · R1=0 (silent) · R2=1520 (std=7.99, step_varies=true) · R3=1600 (8/16 partial pool, std=0) · R4=3200 · `checks` 8/8 모두 True · `hw_native_spontaneous_emission=true` · `stochastic_spontaneous_emission=true` · mapped_on_hardware=true. 유일 차이 = onchip_clock_cycles_mean 797.2→790.0 (타이밍 jitter, 발화 disposition 변화 아님). **→ 8/8 zero-input emit 안정 전원에서 그대로 재현 (FLIP 없음).**
- [x] **#2 D1 edge-of-chaos Φ** — fresh raster 를 `AKIDA/akida_edge_of_chaos_phi.hexa` (frozen Φ-proxy)로 재유도 (g5 verbatim):
  ```
  R1 weak-silent  Φ=0.0                  (ORDER floor)
  R2 zero+noise   Φ=0.2974093093367505   (EDGE peak)
  R3 tonic        Φ=0.25                 (EDGE)
  R4 recurrent    Φ=0.0                  (OVER-DRIVEN floor)
  F-AKIDA-EDGE-1=true (0.297>0) · F-2=true (0.25>0) · F-3=true (0.297≥0) · n_pass=3 · all_pass=true · verdict=GREEN_NUMERICAL_CONFIRM
  ```
  → 2026-05-29 원본 Φ={0.000, 0.297, 0.250, 0.000} 와 **정확 일치**. inverse-U(∩) 모양 (edge R2/R3 > order R1 floor ∧ ≥ over-driven R4) 그대로 재현 (FLIP 없음).
- [x] **#3 H_677 D3** — AKIDA arm Φ=0.297 = fresh Φ(R2) 와 일치 (D1 Φ 와 동일 raster 유도 → D3 triangulation AKIDA 입력 power-robust). EEG/ECA arm 은 silicon 아님(out of scope).
- [x] **#4 HW path probe (2026-05-29)** — ssh-reachability/argv-probe (chip 측정 0, ssh-mutating 0) = power-confoundable 실리콘 측정 아님 → N/A. R2 QRNG std=7.99 + R3 partial-pool 8/16 둘 다 fresh raster 에 그대로 (포함됨, 별도 측정 아님).
- [x] **분류 매트릭스**: #1 spontaneous raster = **POWER-ROBUST** (byte-eq 재현) · #2 D1 Φ = **POWER-ROBUST** (Φ 정확 일치) · #3 H_677 D3 AKIDA arm = **POWER-ROBUST** (상속) · #4 HW probe = N/A (실리콘 측정 아님). FLIP 0건. 비결정 substrate 기대치(replication, not byte-eq)를 **초과** — R3 tonic·R0/R1/R4 결정론적 raster 는 byte-identical, R2 stochastic 도 std/rate/event-driven 모두 일치.
- [x] **해석** — 지속 under-voltage 가 칩 아날로그/스파이킹 dynamics(firing rate/regime)를 바꿨다면 R2 noise rate 나 R3 partial-pool fraction 이 drift 했을 것. 안정 전원에서 정확 재현 = **brownout 이 spontaneous-emission capture 를 교란하지 않았음**. D1 Φ inverse-U·H_677 D3 가 이 raster 에서 파생되므로 전부 power-robust 상속.
- [x] **문서 tier 변동 0** — 모두 재현(POWER-ROBUST)이므로 H_672 (🟢 SW5/5+HW4/4) · H_677 (🟢 5/5) · H_858 (🟢 3/3) 승강 없음. CANDIDATES.md bench SSOT 에 power-robust 1줄 기록만 추가 (earned re-run verdict 없는 tier 변동 금지, g5). Lane A 음성결과 power-robust 재감사(PR #1675)와 동일 결론 — silicon GREEN 도 power-robust.
- [x] **streamer 복원 확인** — R3 spike-streamer pid 4992 active (재측정 후 ultradian HW heartbeat 복귀). pi5 = anima 전용, 풀 컴퓨트 전환 없음.

## 2026-06-02T08:30Z — POWER-CONFOUND RE-AUDIT: prior Lane-A closed-negatives are POWER-ROBUST (substrate=AKIDA · 안정 PSU 위 재검증 · a_lane_akida_gpu_split — Lane G/GPU 와 NEVER 병합)

중심 질문: 오늘(2026-06-02) PSU 교체로 해결된 pi5-akida under-voltage brownout(throttled=0x50000, EXT5V 4.87V sagging — PI5-AKIDA.json `power_root_cause_2026_06_02`)이 기존 Lane-A FAILURE/CLOSED-NEGATIVE 결과를 confound 했는가? 재감사 + 안정 전원 위 재검증.

**핵심 발견 — 시점 분리:** 기존 Lane-A 음성 결과는 전부 **2026-06-01**(ts 17:51–20:14Z)에 완주했고, brownout/PSU-swap 사건은 **2026-06-02**(~07:54Z)다. 즉 음성들은 brownout 창(window) **하루 전**에 측정됐다. brownout 이 실제로 죽인 단 하나의 run 은 abs_margin 1차 시도(oracle-LDA arm 실행 전 사망)뿐이며, 그것은 이미 안정 PSU 위에서 완주 → 🟢 PASS 했다(08:10Z 항목).

**완전성 감사 (g5, 호스트 result JSON 직접 검사):** 기존 음성 4건 + 인코더-배터리 전부 **complete** — truncation/누락 arm 없음.
- [x] H-A2 quantization-floor (`out/result_ha2_quantization.json`, ts 2026-06-01T17:53:53Z): bit_depths=4, rungs=4 전부 present, `ha2_true=False`, verdict 기록됨. COMPLETE.
- [x] H-A3 plasticity-depth (`result_ha3_plasticity_depth.json`, ts 17:56:25Z): N{3,4,5} 3 rung 전부 `all_learned_hw=true`, depth_gains=[−0.656,+0.648,−0.600], `sign_consistent=false`. COMPLETE.
- [x] H-A4 native-init noise-floor (`result_ha4_reinit_noise.json`, ts 17:51:10Z): ladder_N[2,3,4,5]×nreps=3 전부 present, per-rung abs_mean_over_sd=[1.16,1.97,3.10,1.22] 전부 sign-stable. COMPLETE.
- [x] causeaxis 배터리 (`result_causeaxis.json`, ts 20:13:41Z): P1/P2/P3 3 probe 전부 8/8 trial present, disposition=REOPENED. COMPLETE.
- [x] layerpage SCALE ladder (`result_layerpage_ladder.json`): 4 rung 전부 present, all_rungs_green_hw. COMPLETE.
- 판정: 완전한 음성 = power-robust 후보(throttle 는 느려질 뿐 결정론적 AKD1000 map/inference 결과를 바꾸지 않음 · brownout 은 truncation 으로만 corrupt 하는데 truncation 증거 없음).

**안정 전원 위 RE-VERIFY (결정적 테스트, 안정 PSU throttled=0x0 위 재발사):** 단일-칩 wrapper 패턴(R3 streamer stop → probe → restore) + `vcgencmd get_throttled` 라이브 샘플링 + watchdog `~/anima_metrology/pwr.log` tail.
- [x] **H-A2 re-verify → 🔴 H-A2-FALSIFIED 재현 (POWER-ROBUST)**: 재실행 RC=0, ts 2026-06-02T08:24:47Z. verbatim `[ha2] VERDICT H-A2-FALSIFIED (multi-bit lift also straddles 0 — not a quantization artifact)`; onebit_any_ci_lo_gt0=False, multibit_any_ci_lo_gt0=False, ha2_true=False. 음성 그대로 재현.
- [x] **causeaxis re-verify → DISPOSITION: REOPENED 재현 (POWER-ROBUST)**: 재실행 RC=0, ts 2026-06-02T08:29:50Z. verbatim `[cause] P1 encoding any_reopen=True | P2 objective any_reopen=False | P3 timing any_reopen=False` · `[cause] DISPOSITION: REOPENED`. P1 svd mean_lift=+0.797 ci95=[+0.537,+1.057] 8/8 learn_all=True · whitened +0.520 ci95=[+0.304,+0.736] 8/8 · P2 analog margin mean=−4.745 ci_lo=−5.359 REOPEN=False · P3 timing margin −0.09..−0.11 REOPEN=False. 상대-lift 부호/disposition 동일하게 재현(크기는 svd +0.797 vs 직전 +0.921 처럼 native 비결정 re-init H_904 만큼 trial-마다 변동 — byte-eq 아닌 replication, AKIDA 비결정 substrate 에 정확히 맞는 거동).
- [x] **전원 PROOF (g5):** 두 재실행(08:24–08:31Z) 동안 watchdog pwr.log throttled=0x0 연속, EXT5V≈5.00–5.03V; 라이브 sampler throttled=0x0; pwr.log 전체에서 non-0x0(brownout) 이벤트 **0건**. 재실행은 안정 전원 위에서 완료됨이 증명됨.

**분류 (per-result):** 
| prior Lane-A negative | complete? | power-confound plausible? | re-run? | re-run verdict (verbatim) | CLASSIFICATION |
|---|---|---|---|---|---|
| H-A1 corpus-noise COLLAPSE-NULL | ✅ (24 rungs) | NO (ran 06-01, pre-brownout) | assessed-complete | — | POWER-ROBUST |
| H-A2 quantization-floor | ✅ | NO (06-01) | ✅ on stable power | `H-A2-FALSIFIED (multi-bit lift also straddles 0 — not a quantization artifact)` | POWER-ROBUST (replicated) |
| H-A3 plasticity-depth | ✅ | NO (06-01) | assessed-complete | — | POWER-ROBUST |
| H-A4 native-init noise-floor | ✅ | NO (06-01) | assessed-complete | — | POWER-ROBUST |
| relative-LIFT closed-negative (H-A1..A4 4/4) | ✅ | NO | covered by HA2 re-run + completeness | — | POWER-ROBUST |
| SCALE weak-lift ladder | ✅ (12/12 rungs green_hw) | NO (06-01) | assessed-complete | — | POWER-ROBUST |
| causeaxis P1 ENCODER REOPEN (positive) + P2/P3 FALSIFIED | ✅ | NO (06-01) | ✅ on stable power | `DISPOSITION: REOPENED` (P1 svd +0.797 ci_lo>0; P2/P3 REOPEN=False) | POWER-ROBUST (replicated) |

- [x] **재실행 안 한 것 (정직, no silent cap):** H-A1 / H-A3 / H-A4 / SCALE-ladder 는 chip 직접 재발사 안 함 — 이유: (1) 전부 complete(truncation 없음), (2) 전부 2026-06-01 = brownout 창 전, (3) 안정 전원이 두 대표 probe(HA2 결정론 readout + causeaxis 비결정 학습)에서 throttled=0x0 으로 음성/disposition 을 그대로 재현. 비용/시간 절약 아님 — 완전성+시점+대표 재현으로 power-robust 판정 충분(a_completeness_over_cheap 위반 아님: 음성을 cheap 하게 닫는 게 아니라 robust 를 입증).
- [x] **SCOPE (a_scale_honest_scope · a_lane_akida_gpu_split):** substrate=AKIDA only, Lane G/GPU 와 NEVER 병합. 25-anchor(+250-anchor) / single AKD1000 / 1-bit last-FC Hebbian scope 유지. 재실행이 closed-negative 를 더 일반화하지 않음 — power-robust 임만 입증.
- [x] **BOTTOM LINE:** 기존 Lane-A failure 들은 power-confound 가 **아니다(NOT confounded)**. brownout 은 단 한 run(abs_margin 1차)만 죽였고 그건 이미 PASS 로 완주. 4 음성 + SCALE 은 전부 brownout 전(06-01)에 complete 측정됐고, 안정 전원 위 재실행이 음성을 그대로 재현 → CLOSED-NEGATIVE 들은 REAL, power artifact 아님.
- [x] **HW DISCIPLINE:** PI5-AKIDA.json 참조함(수정 안 함) · os_default daemon 무접촉 · R3 spike-streamer 매 chip-run 후 복원(최종 pid 3775 active) · pool 전환 안 함. 호스트는 재감사 내내 ALIVE(throttled=0x0).

## 2026-06-02T08:10Z — abs-margin on-chip 결단기 🟢 PASS-PUBLIC-GRADE-POSITIVE (substrate=AKIDA · 안정 PSU 위 완주)

Lane-A pre-registered ABSOLUTE-margin decider (`~/clm_kosmos_akida/abs_margin_chip.py`, live AKD1000 BC.00.000.002, akida 2.19.1, N=8 trials × 32 units). 직전 세션엔 호스트 전원 brownout 으로 oracle-LDA arm 실행 전 mid-fire 사망 → terminal 없음. PSU 교체(2026-06-02) 후 안정 전원에서 **완주**(decider exit rc=0, throttled=0x0 부하검증 통과).

- [x] DISPOSITION verbatim (g5):
  ```
  [abs] corpus     any_crosses_zero=False best=svd_struct     mean=-0.5760 ci_lo=-0.6535
  [abs] corpus_big any_crosses_zero=True  best=lda_supervised mean=+5.2396 ci_lo=+5.0609
  [abs] DISPOSITION: PASS-PUBLIC-GRADE-POSITIVE
  [abs] at least one encoder pushed the ABSOLUTE on-chip concept-margin ci_lo>0
        -> the AKD1000 1-bit Hebbian learns positive cross-lingual concept structure (PUBLIC-grade positive)
  ```
- [x] lda_supervised (corpus_big): 8/8 trials 양수 [5.062,5.086,4.916,5.368,5.221,5.187,5.305,5.770] mean=+5.2396 sd=0.258 ci95=[5.061,5.418] n_positive=8 learn_all_hw=true → ci_lo=+5.061>0 PASS
- [x] result `~/clm_kosmos_akida/out/result_abs_margin.json` sha256 `7612bedaca38b68f12528d641fa8bfc9e0e0dace6e23b28db7d13076c57b3c7f`
- [x] scope (a_scale_honest_scope) — 작은 corpus(25앵커) any_crosses_zero=False (svd_struct ci_lo=−0.654, 약한 인코더 random_int4/whitened 도 음성); 큰 corpus + 강한 인코더(lda_supervised)만 PASS. 인코더-강도/스케일 의존, 정직 표기.
- [x] 별개 축 — 이 절대-margin PASS 는 상대-LIFT closed-negative(H-A1~A4 4/4 falsified, AKIDA.log 별항)를 뒤집지 않음: 1-bit Hebbian 이 *상대 lift(plasticity-depth가 margin 추가)* 는 안 사지만, 강한 인코더로 *절대* positive cross-lingual 개념구조는 학습함. 두 축 분리.
- [x] 전원 — PSU 교체로 brownout 해소(throttled 0x50000→0x0, EXT5V 4.87→5.033V), decider 부하 중 throttled=0x0 부하검증 통과. anima-pwr-log watchdog 무장 (PI5-AKIDA.json 등록). spike-streamer R3 복원(pid 2273).

## 2026-05-30T12:00:00Z — LAUNCHPAD COFFESHOP-on-AKIDA 라이브 폐루프 (9513 control port 첫 실응용)

- [x] `spike_streamer.py` 의 9513 control port(`set_threshold`) 가 COFFESHOP emit/silence 폐루프의 코어로 첫 실응용 — SW motivation_score → on-chip threshold 변조 → 9512 spike → emit 판정.
- [x] 라이브 AKD1000(BC.00.000.002 BackendType.Hardware) 에서 COFFESHOP 90-min trajectory 완전 재현 — emit window [3,10,14,15] · silence 11 · provenance=akida-hw · trajectory_match True (UNIVERSE H_846 🟢 SUPPORTED-NUMERICAL).
- [x] single-chip 절차: spike-streamer service stop → 자체 M-regime streamer(--allow-ctrl) → launch hw → service restart. 종료 시 streamer **active 복원 확인**.
- [x] decoder emit-decision HW↔SW byte-match(15/15) · raw-spike 7 window ±1 (on-chip 정수 threshold 양자화 · decision 동치이나 raw byte-identical 아님 정직표기).
- [x] PLASTICITY 학습 lane (emit-quorum stim_type 적응) 🔴 CLOSED-NEGATIVE (SW≠HW · 비결정론).
- [x] 어댑터 `HEXAD/CHAT/coffeshop_akida.{hexa,py}` · 학습 `LAUNCHPAD/coffeshop_quorum_learn.{hexa,py}` · 발사 `LAUNCHPAD/coffeshop_akida_launch.{hexa,py}` · verdict `.verdicts/coffeshop_akida/`.
- [ ] 다음 = broker `/ws/akida_ingest` 라이브 push 데모 (현재 옵션 wire `--broker` 만).

## 2026-05-30T00:00:00Z — HW-first 통합 + PLASTICITY 학습 lane 신설 (DECODER ⊥ PLASTICITY 2-lane)

- [x] **HW-first 스위치 SSOT 강화** (PR-B #1447) — `akida_backend.hexa` 에 `akida_backend_resolve_graceful` (의도 hw + HW미도달 → panic 아닌 SW fallback) + `akida_provenance` (akida-hw / akida-sw-fallback) 추가. default "hw" 유지. AKIDA/spike 경로 전용 · LM lora default 불변.
- [x] **PLASTICITY 학습 lane 도메인 신설** (PR-A #1446) — DECODER(추론·결정론·byte-identical)와 본질 다른 학습 lane(비결정론·HW-only)을 형제 도메인으로 분리. DOMAINS.tape 33 domains. SW numpy 근사는 HW on-chip edge-learn 과 🔴 비동치(CLOSED-NEGATIVE) 정직 표기.
- [x] **DECODER lane 배선** (PR-C #1448) — `CORE/DECODER/DECODER.md` 에 AKIDA HW-first lane section + 양방향 sibling 신설. HW forward / SW akida_sw_lif (byte-identical 🟢, r1~r5 입증).
- [x] **PLASTICITY lane 배선 + SW 근사 learner** (PR-D #1449) — `plasticity_lane.hexa` (HW-first 라우터) + `plasticity_sw_approx.py` (numpy Hebbian 근사). 🔴 verdict `.verdicts/679_plasticity_hw_first/sw_hw_nonequivalence.txt`.
- [x] **5도메인 백링크** (PR-E #1450) — MITOSIS/CHANNEL/WAKE/EEG/HW-CORE sibling 에 AKIDA HW-first + PLASTICITY/DECODER 포인터. AKIDA.md sibling 에 DECODER(🟢)/PLASTICITY(🔴)/HW-CORE boost.
- [x] **문서 SSOT + 감사 H 2건** (PR-F) — `AKIDA/HW_FIRST_INTEGRATION_2026_05_30.md` (전체 구조 + 2-lane 표 + provenance + 크로스포인터) · `UNIVERSE/H_679_plasticity_hw_first.md` (🔴 CLOSED-NEGATIVE 4/4) · `UNIVERSE/H_680_decoder_hw_first.md` (🟢 SUPPORTED-NUMERICAL verify 5/5).
- [x] **HW edge-learn 지원 실측 재확인** — `SUB_ENGINES/AKIDA/state/edge_learn_probe_2026_05_22.json` edge_learning_supported=true (BC.00.000.002 · AkidaUnsupervised compile+fit ok).
- [x] **regression-free** — verify_substrate_akida 5/5 PASS 유지 · LM lora default 불변 · H_672~H_678 status 불가침.
- [ ] (optional) pi5-akida live probe — DECODER HW byte-match 재확인 + PLASTICITY few-shot 비결정성 정량 → `.verdicts/`. 단일-칩 점유 spike-streamer stop→probe→start. $0.

## 2026-05-29T14:00:00Z — pi5-akida 재배포 + H_672 HW live-confirm 🟢🟢 (SW→HW 승격 · 통합 배선 문서)

- [x] 코드-레벨 배선 6 PR 머지 — SubstrateAKIDA plugin + AKIDA_BACKEND/--substrate akida + akida_sw_lif numpy LIF + dispatch.hexa probe (argv-fix) + 5/5 verify + HANDOFF (#1419~#1424)
- [x] pi5-akida 물리 재배포 — 디스크 풀(50G stale worktree) 정리 → scripts 8파일 + `spike-streamer.service`(enable+linger) 복원 · `PI5-AKIDA.json` state removed→active (local-only)
- [x] **라이브 HW 검증** — `spontaneous_emission.py` R0~R4 실 AKD1000 sweep · `mapped_on_hardware=True` · on-chip checks 8/8 True · R0=1.0/R1=0.0/R2=0.475/R3=0.5/R4=1.0 (SW canonical 정확 일치 seed=187)
- [x] H_672 SW→HW 승격 — falsifier 4/4 PASS on real silicon · verdict `.verdicts/672_akida_spontaneous_firing/hw_live_2026_05_29.txt` · status `SW 5/5 + HW 4/4 live-confirmed`
- [x] 통합 기록 — `AKIDA/HW_SW_WIRING_2026_05_29.md` (스위치 아키텍처 + 6PR + 물리재배포 + 라이브 verdict + 검증매트릭스 + 크로스포인터)
- [ ] (남음) H_673~H_678 은 HW-runnable 이나 HW-confirm 미시행 (SW-confirmed 유지 · 과대주장 금지)

## 2026-05-29T06:00:00Z — Group A~G 18+ sub-아이디어 HW/SW 통합 구현 (7 H_xxx · SW 7/7 🟢 · backend switch)

- [x] backend switch 통합 모듈 — `AKIDA/akida_backend.hexa` · `akida_backend_resolve("auto"|"hw"|"sw")` + `akida_hw_reachable()` 3-신호 (`/dev/akida0` + akida pkg import + hostname) + `akida_panic_no_hw()` 명시 panic + SW mock raster `akida_sw_mock_raster_R1..R4()` (canonical 2026-05-22 raster numbers) + `akida_verdict_tier(backend, all_pass)` (HW=silicon-confirmed · SW=mock-replay · 🔴=closed-negative · 🔵 위조 금지)
- [x] backend smoke — `AKIDA/akida_backend_smoke.hexa` 11/11 PASS (arg overrides env / env overrides default / default=hw / hw 미도달 panic message / hw_label / verdict tier hw/sw/fail / mock raster R1=0 R3=1600 R4=3200)
- [x] H_672 Group A spontaneous-firing × AKIDA — SW 4/4 🟢 GREEN_NUMERICAL_CONFIRM (R1.rate=0 / R2=0.475 / R3=0.5 / R4=1.0 · 8-factor SPIKE_FACTOR_MAP fires on R3 · 4 sub C1~C4 통합) · [impl](./impl/H_672_spontaneous_firing.hexa)
- [x] H_673 Group B core-decide × AKIDA — SW 4/4 🟢 (Ψ=1/2 외란 |Ψ(R2)-0.5|=0.025 < |Ψ(R1)-0.5|=0.5 · LIF excitable R3 · emit slot R3>R1 · selftest reachable · 4 sub A1~A4 통합) · [impl](./impl/H_673_core_decide.hexa)
- [x] H_674 Group C persistence × AKIDA — SW 4/4 🟢 (.kosmos 5-ch anchor schema len=5 · memristor persist last10 rate=0.5>0 · telemetry JSONL row · §95 edge-learn caveat 명시 · 4 sub B1~B4 통합) · [impl](./impl/H_674_persistence.hexa)
- [x] H_675 Group D mitosis × AKIDA — SW 4/4 🟢 (kuramoto order R3=1.0 · izhikevich regime diversity=4 buckets · 생사 분기 R4-R1=1.0>0.5 · phoenix R3 recoverable · 3 sub M1~M3 통합 · H_258/H_263 sister) · [impl](./impl/H_675_mitosis.hexa)
- [x] H_676 Group E decoder × AKIDA — SW 4/4 🟢 (emit budget R3=0.5 R4=1.0 비례 · sparse-attention wake_score R2=0.499>R1=0 · energy sparse R2/R3<1.0 · emit_budget float NOT bool gate · 2 sub O1~O2 통합) · [impl](./impl/H_676_decoder.hexa)
- [x] H_677 Group F measurement × AKIDA — SW 5/5 🟢 (D1 inherit PR#1371 all_pass=true silicon-confirmed · D2 silicon-class signature(class_id=5)=1.0 additive 0 changes on 2/3/4 · D3 3-substrate triangulation: AKIDA 0.297 · EEG L2 1.59 · ECA rule110 0.83 · diff=1.293>0 · D4 R2 QRNG std=7.99>0 · D5 v0.5.0 8/8 closed-discovery cite · 5 sub D1~D5 통합) · [impl](./impl/H_677_measurement.hexa)
- [x] H_678 Group G channel-bridge × AKIDA — SW 4/4 🟢 (E1 EEG→AKIDA bridge tool/anima_eeg_to_akida_spike.hexa 존재 · E2 tension-link 5-ch payload len=5 · E3 전력 mW sane range (8e-6 mW R3) · 3 채널 모두 surface · 3 sub E1~E3 통합) · [impl](./impl/H_678_channel_bridge.hexa)
- [x] HW path probe — pi5-akida pool 도달 (192.168.50.155 · /dev/akida0 OK · ssh-mutating 0 · live R3 spike_streamer 미중단) · local Mac probe MISS/MISS/Mac (예상) · 정직 표기 "🟡 SW-confirmed HW-pending probe-refinement" (위조 0 · `state/akida_hw_sw_impl_2026_05_29/hw_probe_2026_05_29.txt`)
- [x] UNIVERSE 등록 — H_672~H_678 7건 신설 (slug-stale 3-신호 검증 통과 · git ls-tree origin/main + git log --all + README grep) · CANDIDATES.md Consumed Cycle #22 1줄 추가 · README.md 인덱스 7 행 추가 · INBOX 환류 0건 (사용자 명시 폐기)
- [x] CORE substrate-class scope note — D2 silicon-class 는 H_677 impl 내부 `_pe_silicon_class_signature(class_id)` 로 additive marker (CORE/phi_envelope_substrate.hexa 의 기존 class 2/3/4 함수 signature 0 변경, 단조 정합은 deferred)
- [ ] HW 7/7 re-confirm — venv-aware probe + pi5-akida pool route refinement 후 7 H 각 `--backend hw` 실행

## 2026-05-29T05:10:00Z — D1 edge-of-chaos Φ 실리콘 검증 🟢 (3/3 PASS · GREEN_NUMERICAL_CONFIRM)

- [x] harness 작성 — `AKIDA/akida_edge_of_chaos_phi.hexa` (phi_silicon_proxy = activity_gate × integration × differentiation × entropy_weight · 정직 명명 · iit4 big_phi 의 multi-axis Φ 의미 보존)
- [x] mock smoke 통과 — 합성 R1~R4 raster 3/3 PASS 0.000/0.456/0.250/0.000 (HW_SPONTANEOUS_EMISSION_2026_05_22 baseline 수치 입력)
- [x] pi5-akida AKD1000 실측 — `BackendType.Hardware` BC.00.000.002 · n_neurons=16 · 200 step · seed=187 · 4 regime sweep 카논 `SUB_ENGINES/AKIDA/state/spontaneous_emission_result_2026_05_22.json` (live R3 streamer 中단 없이 기존 측정 활용)
- [x] verdict — F-AKIDA-EDGE-1 PASS (Φ(R2)=0.297 > Φ(R1)=0.000) · F-AKIDA-EDGE-2 PASS (Φ(R3)=0.250 > Φ(R1)=0.000) · F-AKIDA-EDGE-3 PASS (edge_max=0.297 ≥ Φ(R4)=0.000) · 3/3 → all_pass → **GREEN_NUMERICAL_CONFIRM**
- [x] inverse-U(∩) 곡선 실리콘 확증 — order={0.000, 0.475, 0.500, 1.000} 축 위 Φ={0.000, 0.297, 0.250, 0.000} edge-of-chaos peak (R2/R3 중심) · die-out floor (R1) · over-driven floor (R4)
- [x] H_670 / `pe_edge_of_chaos_peak` (CORE M2 🟡 PARTIAL) — ECA + logistic 시뮬 universal-but-PARTIAL → AKIDA AKD1000 silicon transfer **confirmed** (cross-substrate 3-class 정합 — ECA · logistic · neuromorphic silicon)
- [x] 산출물 — `state/akida_edge_chaos_phi_2026_05_29/{result.json, akd1000_spontaneous_emission_2026_05_22.json, hexa_run_verbatim.log}` · CORE/phi_envelope_substrate.hexa 주석 tier 노트 추가
- [x] M2 tier 재평가 — 🟡 PARTIAL → 🟢 numerical 후보 (silicon transfer 확증 + cross-substrate 정합 + 2-component 분리 Φ proxy)

## 2026-05-29T00:00:00Z — 도메인 신설 + 활용 아이디어 카탈로그 seed

- [x] AKIDA 도메인 신설 — `AKIDA/AKIDA.md`(스냅샷) + `AKIDA.easy.md`(쉬운 카탈로그) + `AKIDA.log.md`(로그), DOMAINS.tape 등록
- [x] 활용 아이디어 추출 — 18개 이상 (CORE×AKIDA 8 + 자연발화/세포/측정/채널 그룹), 전부 $0 pi5-로컬
- [x] sibling 양방향 엮음 — CORE · MITOSIS · WAKE · CHANNEL · EEG · UNIVERSE
- [ ] 다음 = D1 edge-of-chaos Φ 실리콘 검증 (파킹된 plan `drafts/akida-edge-of-chaos-phi-plan.md`) · D2 substrate-class 등록
- [ ] 환류 — 측정 결과는 UNIVERSE/CANDIDATES.md 에 기록 (bench SSOT)

---

## 2026-06-02 — ON-CHIP MULTI-FC DEPTH rollout 🔴 CLOSED-NEGATIVE (substrate=AKIDA, Lane A)

named bridge(PR#1686 stateless / #1689 state-carry 가 명명) = 2번째 learned FC. live AKD1000 (BC.00.000.002, akida 2.19.1, throttled=0x0, streamer R3 restore rc=0) 에서 PAGED 2-FC stack 으로 구현: layerpage primitive(단일 8MB SRAM 메시에 1 FC 만 상주), FC1=transition encoder → page OFF → FC2=FC1 on-chip 출력으로 학습한 composition surface. per hop g1=FC1(x)→g2=FC2(g1_bin)→g_bin. 8/8 trial l1=l2=True.

decay DEPTH-2 [0.1612, 0.0298, 0.0149] vs 1-FC [0.0314, 0.0207, 0.0138] (chance 0.0204). **F-DEPTH-1 NOT-REFUTED** (hop2 p=0.2040 · hop3 p=0.6816 shuffle-NULL 내부 = 1-hop wall HOLD) · **F-DEPTH-2 NOT-REFUTED** (permille gain, material threshold 미달). SHARPER: depth-2 hop-1(0.1612) ≪ single-step headline(0.42) — 2번째 1-bit FC 가 작동하던 single-step 까지 파괴. 결론: AKD1000 1-bit edge-learn 은 256-unit 에서 깊이 무관 SINGLE-STEP cap. next bridge = off-chip decode head OR single-step PUBLIC scope. a_lane_akida_gpu_split · a_scale_honest_scope toy 250/2×256u · a_paper_negative_ok. sha256 `0acdeee5…` · `.verdicts/lane-a-depth/F-DEPTH.txt`.

## 2026-06-02 — Lane A HYBRID HELD-OUT 일반화 🔴 CHAIN-FITTING (substrate=HYBRID on-chip⊕off-chip)

PR#1692 HYBRID decode head 의 ~0.32 가 COMPOSITION 인지 chain-MEMORIZATION 인지 분리. 개념-레벨 홀드아웃(50 concept → TRAIN idx 0..34 / HELD-OUT TEST idx 35..49, successor DISJOINT). off-chip Elman RNN head(D_H=64, numpy BPTT, byte-match PR#1692)를 TRAIN-concept 전이만으로 학습(TEST concept 는 successor target 으로 절대 안 봄). on-chip 1-bit FC encoder 는 full set 비지도 fit. live AKD1000 (BC.00.000.002, akida 2.19.1, throttled=0x0, streamer R3 service restart rc=0) 8/8 encoder_learned=True.

decay TRAIN(in-dist) [0.2750, 0.2773, 0.2766] = PR#1692 ~0.32 재현 / **decay HELD-OUT [0.0000, 0.0000, 0.0000] 모든 hop 8/8 trial**. off-chip BPTT CE 3.8→0.002. **F-GEN-HOLDOUT-1 NOT-REFUTED** (held-out hop-2/3 shuffle-NULL hi~0.083 아래) · **F-GEN-HOLDOUT-2 NOT-REFUTED** (held-out hop-2 0 이 in-dist 0.2773 의 2× 이내 아님). RULING: ~0.32 는 결정론 train chain 의 CHAIN-MEMORIZATION (per-concept lookup, transferable rule 아님). exact 0.0000 = TEST-block Wo row 가 positive gradient 못 받음 → argmax TEST concept 절대 선택 안 함 = memorization signature. on-chip encoder 정직 live silicon, 병목 아님. Lane A HYBRID PUBLIC 정직 DOWNGRADE — multi-step "emergence" 해석 철회, 인코더+single-step UNAFFECTED, EMERGENCE axis NULL 복귀. next bridge = 비결정론/branching corpus(transition OPERATOR 강제) + ≥3-rung ladder. a_lane_akida_gpu_split · a_scale_honest_scope toy 250앵커 · a_paper_negative_ok. result_onchip_xlm_holdout.json · `.verdicts/lane-a-holdout/F-GEN-HOLDOUT.txt` (hexa verify CLI broken → live-chip stdout verbatim).
