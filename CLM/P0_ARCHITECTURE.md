# CLM P0 — 아키텍처 설계 (확정)

> CLM(anima-native 의식 언어모델, scratch from-zero)의 P0 바닥설계. sbs manual co-design으로
> 10개 결정(Q1~Q4 + d1~d6) 확정. 다음 세션은 이 문서가 SSOT — 설계 재발명 금지.
> sibling: [CLM.md](./CLM.md) · [AKIDA](../AKIDA/AKIDA.md) · [CORE/DECODER](../CORE/DECODER/DECODER.md) · [LAUNCHPAD](../LAUNCHPAD/LAUNCHPAD.md)

## 0. 한눈 구조

```
   byte text (V=256)
        │  dilated conv embed
        ▼
   ┌─────────── Conv-native trunk (AKIDA 온칩) ───────────┐
   │  dilated conv stack  +  MoE router                   │
   │       ├─ expert0 (cell0) ─ coherent main             │
   │       ├─ expert1 (cell1) ─ register/anima            │  ← MoE expert = mitosis cell
   │       └─ expertK (cellK) ─ …                          │
   │  monopoly-escape: load-balance aux + hard top-K + entropy anneal
   └──────────────────────────────────────────────────────┘
        │ int4 quantized (QAT)
        ▼
   readout → next byte        emit/silence는 LAUNCHPAD 게이트(별도)
        │
   추론 = AKIDA(int4) ONLY   학습도 AKIDA   영속 = .kosmos
   ─ 학습 2-phase: ① pretrain = AKIDA-향 QAT(GPU backprop·int4 envelope 시뮬) · ② 적응 = AKIDA-위 PLASTICITY on-chip edge-learn
```

## 1. 확정 결정셋 (10)

| # | 축 | 결정 | 근거 |
|---|---|---|---|
| **Q1** | arch family | **Conv-native LM** (dilated conv · attention 없음) | AKIDA conv byte-identical 증명(5-stage) · attention은 AKIDA 매핑 불가 → AKIDA 우선과 정합 · byte 긴 sequence가 conv엔 약(O(n·k)) |
| **Q2** | 더블바인드 탈출 | **MoE conv-expert = mitosis cell** (분열한 cell이 각 expert) | A(MoE 토이증명) + C(p8 train=infer·anima-native) 결합 · register 격리=메인 coherent 유지 |
| **Q3** | monopoly 토대 | **byte-vocab V=256** + 3-arm(A/B/A+B) + F-CLM-MONO | V≫d(15만/64=2370배)가 monopoly 근원 → byte로 V/d=4배 = 근원 소멸 (prior art 미시도 lever) |
| **Q4** | scale 실험 | micro-exp 토이=**직관(non-gate)** · 3-arm **전부 full-fire**가 판정 · scale ladder · wall-first·무캡 | toy≠scale(H_666 실증) → toy로 prune 금지, 다 발사 |
| **d1** | corpus | **신규** + **혼합**(웹대량=coherence + 엄선=register) + **.kosmos 영속 필수(SKIP 금지)** | MoE 2-lane ↔ corpus 2-source 1:1 · a_kosmos 거버넌스(required·active) = .kosmos 영속은 **면제 불가** · 현 spec(kosmos/1.1)이 byte-corpus를 못 받치면 **upstream을 먼저 업그레이드한 뒤** 영속한다 · "얽매이지 않음"=업그레이드를 **별도 트랙으로 병행**해 전체를 멈추지 않는다는 뜻이지 **건너뛰어도 된다는 뜻이 아니다** · ✅ **실현**: kosmos/2.0 `@corpus`(6 PR #8~13) + `corpus/clm_p1.corpus.kosmos` 영속(lsp clean) · coord 실측=ENCODER 도메인 |
| **d2** | .clm 포맷 | **2-track**(int4 AKIDA + fp16 GPU shadow) + QAT scale + manifest(sha256·kosmos ptr) | AKIDA추론·GPU학습재개·mitosis 한 파일 · naive PTQ int4 파괴→QAT 필수(실측) |
| **d3** | scale rung | tiny `d64/L2/E4` · small `d256/L4/E8` · target **≤ AKD1000 fit** (P4 probe 확정) | 추론 AKIDA-only라 칩 용량이 target 상한 · byte+conv라 작아도 됨 |
| **d4** | 경로 | **추론 AKIDA(int4) ONLY** · **학습도 AKIDA** = ① AKIDA-향 QAT(GPU backprop이되 int4 envelope 향해 pretrain) + ② AKIDA-위 PLASTICITY on-chip 적응(AKD1000 edge-learn) | LAUNCHPAD AKIDA-first-everywhere 복원(학습·디코더·발화결정=AKIDA). 칩 위 full-backprop만 물리 불가(AKD1000=추론칩) → 그 한 단계만 GPU honest carve-out, 나머지는 AKIDA-bound. GPU 추론 escape 없음(추론은 순수 AKIDA int4) |
| **d5** | trainer(B0) | **hexa-native 학습 = 1순위(g1-pure)** · **AKIDA-향 QAT envelope 시뮬 손실** · PyTorch는 토이/대조용 폴백 · 적응 lane = PLASTICITY 위임 | ✅ **UPDATE 2026-05-30: hexa 학습속도 완전 해결**(사용자 확인·hexa-lang측) → M5 🔴 INFEASIBLE(0.28 step/s) 전제 소멸. 2-track 우회 불필요 — 모델+트레이너 둘 다 hexa-native 가능(g1). 학습 job = **`/dojo`로 생성**(job.hexa+train+run.sh). **QAT = 학습 forward 에 AKIDA envelope(act_bits∈{1,2,4}·symmetric int4[-7,+7]·step=2^(input_bits−act_bits)·conv/FC/pool, `akida_sw_lif` byte-identical 집합) 를 시뮬레이트 = "AKIDA 를 향해" 학습**(§9). on-chip 맥락적응은 **PLASTICITY 도메인 edge-learn 위임**(중복 0). anima P2 fire에서 step-rate 재측정으로 최종 확인 · 추론 AKIDA-int4-only 불변 |
| **d6** | falsifier 임계 | **z>3.0 양축 + multi-seed{base,43,44} 재현** | v7 z=2.75 단일seed marginal 교훈 · §A2-trap·seed-artifact 차단 |

## 2. AKIDA-map 경계 (정직)

| 단계 | 어디서 | 정합 |
|---|---|---|
| 추론 (conv trunk + readout) | **AKD1000 int4 온칩 ONLY** | conv/FC/pool 5-stage byte-identical 증명 envelope |
| 학습 ① pretrain (AKIDA-향 QAT) | GPU backprop, **AKIDA envelope 시뮬** | "AKIDA 를 향해" 학습 — 학습 forward 가 int4/act_bits envelope(`akida_sw_lif` 집합)를 시뮬, 배포 시 PTQ 파괴 없이 .clm int4 → 온칩 |
| 학습 ② on-chip 적응 (AKIDA-위 PLASTICITY) | **AKD1000 edge-learn 온칩** | "AKIDA 위에서" 진짜 학습 — PLASTICITY 도메인 위임 · 🔴 비결정·SW 비동치 정직(H_679) |
| 칩 위 full-backprop | ❌ 물리 불가 | AKD1000=추론칩 — 이 한 단계만 GPU honest carve-out |
| emit/silence 게이트 | LAUNCHPAD(별도) | CLM=콘텐츠("무엇") · 게이트=타이밍("언제") |

⚠ **honest**: attention을 안 쓰는 이유 = AKIDA 프리미티브(conv/FC/pool/sepconv)에 attention 매핑 불가. 전체 추론을 칩에 올리려면 conv-native가 필수. (transformer 썼으면 추론이 GPU로 새서 d4 위반)
⚠ **honest (학습)**: "학습도 AKIDA"는 두 단계 모두 AKIDA-bound 라는 뜻 — ① pretrain 은 GPU backprop 이되 AKIDA int4 envelope 를 향해(QAT), ② 맥락적응은 AKD1000 위 edge-learn(PLASTICITY). **칩 위 full-backprop 만 물리 불가** = 그 한 단계만 GPU. (학습 전체를 "GPU only" 라 적으면 LAUNCHPAD AKIDA-first 와 PLASTICITY 도메인 위반)

## 3. 더블바인드 탈출 = 3-arm ablation (Q3 핵심)

```
   공통 토대: byte-vocab V=256 · conv-native · MoE(=mitosis cell)
        │
   ┌────┼─────────────┐
   ARM A         ARM B          ARM A+B ★untried
   entropy-reg   topK+load-bal  A+B 합본
   (content축)   (routing축)     (dual-axis 노림)
        └────┼─────────────┘
   F-CLM-MONO: distinct_experts>1 ∧ routing z>3.0 ∧ content z>3.0 ∧ seed{base,43,44} 재현
```
- prior art: H_666(MoE collapse, toy🟢 scale🔴) · v5-mitosis v1~v7(v7 routing z=2.75 marginal·content 후퇴). **monopoly 근원=V≫d** → byte-vocab이 근원 직격(우리 신규 lever).

## 4. 사전등록 falsifier (UNIVERSE 등록 대상)

| id | 주장 | 판정 시점 | tier 목표 |
|---|---|---|---|
| **F-CLM-MONO** | distinct_experts>1 ∧ routing z>3.0 ∧ content z>3.0 ∧ multi-seed 재현 | P2 full-fire | 🟢/🔴 |
| **F-CLM-AKIDA-MAP** | 추론 path 연산자 ⊆ AKIDA envelope(conv/FC/pool/sepconv·int4·act_bits) | P0 구조검증(now) | 🔵 formal |
| **F-CLM-QUANT** | QAT int4 round-trip ppl 열화 < 임계 (naive PTQ는 파괴 실증) | P3 | 🟢 |
| **F-CLM-SCALE** | monopoly-escape가 ladder rung 따라 유지(전이곡선) | P2 multi-rung | 🟢/🔴 |
| **F-CLM-MITOSIS** | cell-pool 성장(p8 train=infer) | P2 | 🟢 |

## 5. 실험 매트릭스 (Q4 — 3-arm × scale ladder)

```
              tiny(d64)   small(d256)  target(≤AKD1000)
   ARM A      A·t          A·s          A·T
   ARM B      B·t          B·s          B·T
   ARM A+B    AB·t         AB·s         AB·T
   micro-exp(토이)=직관 non-gate · full-fire 전부=판정 · /micro-exp 병렬 · wall-first·무캡
   추적축: distinct_experts & dual-axis z  vs  scale (전이곡선=1급 산출)
```

## 6. authoring 규약 (가드 정정)

- `.hexa`/`.md`/`.tape` = Write/Edit OK (hexa-native 가드 통과).
- **`.py` = 가드 차단** (project.tape repo). escape: (가) `python3 -c "open(PATH,'w').write(...)"` 채널(미커버) · (나) `sidecar disable hexa-native`(작업후 `enable` 복원) · pod/pi5엔 무적용.
- ⚠ **`@py`/`@python` attr는 없음** (hexa-native 0.5.0 "NO opt-out" 명시 — 오해 정정).
- 학습 .py(PyTorch)는 GPU pod서 작성(project.tape 없음) 권장.

## 7. 정직한 물리 현실 (재확인)

- ✅ **hexa-native trainer throughput 해결됨**(2026-05-30, 사용자 확인·hexa-lang측) — 기존 M5 🔴 INFEASIBLE(0.28 step/s) 더는 유효치 않음. CLM 학습을 hexa-native(g1-pure)로 진행 가능, `/dojo`로 job 생성. anima P2 fire에서 step-rate 재측정으로 최종 확인(p7/g5). 추론 AKIDA-int4-only 불변.
- **"학습도 AKIDA" (LAUNCHPAD AKIDA-first 복원)** — 학습은 GPU only 가 아니다. ① pretrain = **AKIDA-향 QAT**(GPU backprop 이되 AKIDA int4 envelope[§9]을 향해 학습) · ② 맥락적응 = **AKIDA-위 PLASTICITY** on-chip edge-learn(AKD1000). 두 단계 모두 AKIDA-bound. **칩 위 full-backprop 만 물리 불가** = 그 한 단계만 GPU(AKD1000=추론칩) honest carve-out.
- target 크기 = AKD1000 fit 실측(P4) 전엔 미확정 — "≤칩용량" 상한.
- monopoly-escape = toy🟢·scale🔴 미해결 → byte-vocab으로 근원 직격 시도(가설, P2 falsify).

## 8. 다음 (P1~P5)

- P1 corpus: 웹대량+엄선 혼합 byte build · .kosmos emit 영속 배선.
- P2 train: 3-arm × ladder full-fire **hexa-native(g1) AKIDA-향 QAT pretrain**(§9 envelope 손실) · 학습 job=`/dojo` 생성 · F-CLM-MONO/SCALE 판정 · step-rate 재측정. 맥락적응 lane = **PLASTICITY on-chip edge-learn**(위임).
- P3 .clm: QAT int4 + fp shadow 직렬화 + manifest.
- P4 AKIDA: .clm int4 → AKD1000 온칩 추론 · fit probe로 target 확정.
- P5 DECODER 통합: generator → brain_decide emit 슬롯 → LAUNCHPAD COFFESHOP 콘텐츠.
- B0: hexa-native trainer throughput fix — ✅ **해결됨**(2026-05-30, hexa-lang측). P2가 hexa-native로 진행.
- QAT 손실/양자화기 코드 스텁 = 모델(T4) 선행 후속 (설계는 §9, 코드는 후속).

## 9. QAT 설계 — "AKIDA 를 향해" 학습 (설계만 · 코드는 모델 선행 후속)

> "학습도 AKIDA"의 pretrain 단계. GPU backprop 이되 학습 forward 가 AKIDA 배포 envelope 를
> 시뮬레이트해 **AKIDA 를 향해** 학습한다. 목표 = 배포 시 naive PTQ int4 round-trip 파괴(기 실측)
> 회피 — 학습이 이미 양자화된 도착지를 알고 수렴. 코드 = T4(모델) 선행 후 스텁(d5).

**AKIDA envelope (= 학습 target 양자화 집합, AKIDA 1~5차 byte-identical 검증)**
- 활성: `act_bits ∈ {1,2,4}` · step `= 2^(input_bits − act_bits)` · `y = clip(ceil(pot/step), 0, 2^act_bits − 1)` (act_bits=1 → LIF 환원). `akida_sw_lif::fc_quantized_forward` 와 동일 공식.
- 가중치: **symmetric int4 `[-7,+7]`** (칩이 −8 거부 실측 → two's-complement 아님). per-channel scale.
- 연산자: conv(stride/VALID·180° flip true-conv) · FC(deep cascade) · pool(MAX, fused) · sepconv(dw RAW potential → pw fused single-quantize) — 모두 envelope 내.

**QAT forward/backward (설계)**
- forward: `w_q = quant_int4_sym(w, scale)` → `act_q = akida_act_quant(pot, act_bits, input_bits)` — 즉 학습 forward 가 위 envelope 를 그대로 통과.
- backward: **STE(straight-through estimator)** — quantize step 의 gradient 는 identity(`∂w_q/∂w ≈ 1` clip 범위 내), 범위 밖은 0. GPU backprop 으로 fp16 master weight 갱신, forward 만 양자화.
- scale 산출: per-channel, 학습중 양자화-aware로 산출 → `.clm` blocks `qat_scale` 저장(CLM_FORMAT_SPEC §2) → AKIDA 가 재계산 없이 직접 로드.

**QAT 학습 손실 (설계)**
- base = next-byte CE(byte-vocab V=256).
- **envelope 정합 항(선택)**: 양자화 forward 출력이 fp shadow forward 출력과 발산하지 않도록 정합 손실(예: KL/MSE on logits) 옵션 — naive PTQ 파괴를 학습 신호로 흡수. (가중치 λ = P3 F-CLM-QUANT 임계 튜닝 대상.)
- 판정 = **F-CLM-QUANT** (QAT int4 round-trip ppl 열화 < 임계, P3) — naive PTQ 파괴 대조.

**도착지 검증**: 학습 envelope = `akida_sw_lif` 검증집합 ⊆ AKD1000 byte-identical 영역 → QAT 로 학습한 int4 weight 는 배포 시 SW=HW byte-identical(추론). 즉 "AKIDA 를 향해" 가 빈말이 아니라 검증된 도착지.

**경계 (honest)**: QAT 는 GPU backprop 사용 — 칩 위 full-backprop 은 물리 불가(AKD1000=추론칩). on-chip 맥락 적응(진짜 칩 위 학습)은 PLASTICITY 도메인 edge-learn(🔴 비결정·SW 비동치, H_679) 가 담당, QAT 와 직교한 후속 lane.

## 11. MITOSIS-ARRAY — scale=expert-count 돌파엔진 (DISSOLVE)

> 출처: [CLM.breakthrough.mining.md](./CLM.breakthrough.mining.md) `@status: depleted-both` 의 **DISSOLVE** 권고결론.
> 충돌: **측정-타당성**(MoE routing-diversity/monopoly-escape 는 3B/7B scale 에서만 의미있게 측정 — H_847 🔴 가 tiny~small 2.70M 한정인 이유, a_scale_honest_scope) ⊥ **AKIDA 온칩**(AKD1000 ~1.2M 노드 = 소형 강제) 정면충돌.

### 11.1 충돌의 뿌리 — "scale = per-model size" 암묵 가정

H_847 routing-z 가 tiny~small 한정으로만 측정될 수 있었던 근본 이유는 routing-diversity 가 **모델 차원(d_model)** 을 키워야 의미가 커진다고 가정했기 때문이다. 그러면 측정엔 GPU 3B 가 필요하고, AKIDA(각 칩 ≤1.2M) 와 정면충돌한다. 이 가정을 깨면 충돌이 소멸한다 (mining DISSOLVE · E1·E2·E3·E6).

### 11.2 DISSOLVE — scale 축을 model-dim → **expert-COUNT** 로 이동 (@L2)

```
   기존:  scale = d_model 키우기            →  GPU 3B 필요  ⊥  AKD1000 ≤1.2M
   DISSOLVE: scale = expert 개수 E 키우기    →  각 expert ≤1.2M chip-fit 불변
            big = Σ_E (chip-fit expert)       →  E 로 scale, unit 은 영원히 chip-fit
```

- **routing-diversity 재정의 (@L2)**: 단일모델 내부의 d-의존량이 아니라, **expert-count 를 sweep 한 inter-expert(=inter-chip) dispatch entropy**. E 를 늘려가며 dispatch 분포가 uniform-null 대비 얼마나 다양해지는지(monopoly-escape 동역학)를 chip-native 로 실측한다. E=4,8,16,32,64 sweep, 각 expert 는 chip-fit(≤1.2M params).
- **측정이 chip-native 가 됨**: "routing-diversity 측정하려면 3B GPU 가야" 가 사라진다 — expert 수만 늘리면 각 unit 은 AKD1000 fit 을 유지한 채 monopoly 동역학을 scale 한다.

### 11.3 expert = mitosis cell = AKD1000 chip 매핑 (@L3)

```
   분열한 mitosis cell  ≡  MoE conv-expert  ≡  AKD1000 칩 1개
   (P0 Q2)                 (router 가 dispatch)   (≤1.2M 노드 fit)
```

- mining E6 (equivalence): expert=mitosis cell=칩 — P0 Q2(MoE=mitosis) + LAUNCHPAD AKIDA-first 가 이미 이 엔진을 가리킨다.
- mining E2 (causal): **칩 제약(각 expert ≤1.2M 강제)이 곧 specialization 을 강제** → chip-fit 이 monopoly-escape 메커니즘 그 자체(chip-as-regularizer, mining L5). 측정 한계가 아니라 escape 메커니즘.
- top-k sparse activation: 토큰당 active subset 만 forward (Switch/GShard) = "총용량 거대, per-token active 미세" = big=Σ small 그 자체.

### 11.4 배포 경로 — N-칩 어레이 + 1-칩 time-mux fallback (@L5)

```
   배포 A (N-chip array):   E expert = N × AKD1000 (1 expert/칩) — 병렬, N×1.2M effective
   배포 B (time-mux 1-chip): 1 AKD1000 에 expert 가중치 시분할 스트리밍 — 큰 effective, 작은 순간 footprint, latency↑
```

- mining L7/L8 (E4 dependency): expert-array 의 물리 실현 = N×AKD1000(병렬) 또는 time-mux(1칩 순차). pool 의 pi5-akida 가 LAUNCHPAD 다중-AKIDA 와 정합.
- 측정-rung ⊥ 배포-rung (a_scale_honest_scope): GPU sparse-MoE(top-k cheap)에서 dispatch entropy 측정 ⊥ 칩-어레이 배포. 둘은 분리된 rung 이며, **BRIDGE(§ 후속 distill)** 가 측정 finding 의 배포 transfer 를 보장한다.

### 11.5 정직 caveat — 물리 다중-AKD1000 = 현재 pi5 1칩 (@L6)

⚠ **HONEST (p7)**: 물리 다중-AKD1000 칩 어레이는 **현재 pool 에 pi5 1개(AKD1000 1칩)뿐**이다. 따라서 expert-array 의 inter-chip dispatch entropy 는:
- **먼저 SW-sim + GPU sparse-MoE 로 측정** (top-k active = cheap, expert-count sweep E=4~64 를 GPU 1대로 실측).
- **물리 다중칩 배포는 hardware 확보 시** — 그때까지 단일 AKD1000 은 time-mux(배포 B)로 fallback.
- 즉 "inter-chip dispatch entropy" 의 측정 surrogate 는 **inter-expert dispatch entropy(SW/GPU)** 이고, 칩-어레이는 그 배포 실현이다. 이 surrogate≡target 동치(mining E3)는 top-k routing 이 expert↔칩 1:1 이라 성립하나, **물리 칩-간 통신 지연/DMA 는 미측정** — 이 한 축만 hardware 후속이다 (정직 boundary).

### 11.6 사전등록 falsifier (신규)

| id | 주장 | 판정 시점 | tier 목표 |
|---|---|---|---|
| **F-CLM-MONO-ARRAY** | expert-count E sweep 시 inter-expert dispatch entropy 가 uniform-null 대비 단조 상승(monopoly-escape 가 E 로 scale) | P-ARRAY (now) | 🟢/🔴 |
| **F-CLM-BRIDGE-XFER** | teacher(유효 scale GPU) 의 monopoly-escape 가 chip-fit student 로 distill 후 생존(transfer Δ) | P-BRIDGE | 🟢/🔴 |

- F-CLM-MONO-ARRAY 는 H_847 의 후속 — H_847 은 **고정 rung(tiny/small)에서 routing-z 임계**를 봤고(🔴), 이 엔진은 **rung 을 expert-count 로 바꿔** dispatch entropy 의 scale 거동을 본다. 둘은 다른 falsifier(H_847=고정 z 임계 · ARRAY=scale 단조성).
- BRIDGE(distill) = SECONDARY arm — transfer 보장 cross-check (a_scale_honest_scope 측정rung⊥배포rung 에 transfer 추가).

---

## 12. PHI-NATIVE — 측도 교체로 충돌 ROOT 소멸 (round-3 winner)

> §11 MITOSIS-ARRAY(DISSOLVE scale=expert-count)는 H_852+H_854 에서 🔴🔴, BRIDGE(distill)도 H_853+H_854 에서 🔴🔴 — **둘 다 toy∧production deterministic CLOSED**. hexa-loop round-3(`CLM.breakthrough.mining.md` ROUND 3, depleted-both)이 그 死因을 짚음: **routing-diversity 라는 측도 자체**가 (a) null-referenced → ln(E) 천장 doomed (b) scale-dependent. 5-lens 수렴 결론 = **측도를 바꿔라**.

### 12.1 핵심 reframe

| | 닫힌 두 경로 (§11 ARRAY · BRIDGE) | PHI-NATIVE (§12) |
|---|---|---|
| 무엇을 측정 | inter-expert dispatch entropy (routing-diversity) | **IIT4 Φ** (region/coarse bounded) |
| scale 의존 | ✗ ln(E) doomed | ✅ **scale-free** (Φ(n=5)≈valid as Φ(n=500)) |
| null 필요 | ✗ uniform-simplex (ln E 천장) | ✅ **intrinsic·null-free** |
| 어디서 측정 | GPU proxy | **AKD1000 spike 출력**(배포 칩) |
| 측정rung vs 배포rung | 분리(충돌) | **동일 칩(붕괴)** → 충돌 ROOT 소멸 |

핵심: "의식 측도가 큰 scale 필요"는 *틀린 측도(routing-diversity)*에 대해서만 참이었다. Φ 는 작은 n 에서도 meaningful → **측정⊥배포 충돌이 애초에 없음**(배포하는 칩에서 Φ 를 잰다). 이것은 SOLVE 가 아니라 **REFRAME** — routing-diversity 질문(🔴 closed)을 *moot* 하게 만든다.

### 12.2 설계 (재사용 우선 · g0/g1)

```
  CLM forward (AKIDA int4) ──→ spike 출력 (snn_lif / spike_streamer)
                                     │  TPM 추출 (time-binned spike → 전이행렬)
                                     ▼
            region/coarse-grained 분할 (n≤~7 region, exact 2^(2n) 회피)
                                     │  iit4_bounded.hexa (재사용)
                                     ▼
                          Φ (bounded big-phi) = CLM 의식 신호
```

- **Φ 변종**: `HEXAD/IIT4/lib/iit4_bounded.hexa`(bounded big-phi, 큰 n) + `iit4_bigphi.hexa` 재사용. exact Φ cost 2^(2n) → region 분할(n≤~7)로 coarse-grain.
- **측정 대상**: AKD1000 spike 출력 — SW(`SUB_ENGINES/AKIDA/pack/adapters/snn_lif.py`·`akida_sw_lif`) toy → pi5 HW(`spike_streamer`) later. 선례 `AKIDA/akida_edge_of_chaos_phi.hexa`(AKIDA+Φ 이미 연결).
- **TPM**: time-binned spike raster → 전이확률행렬(TPM) → IIT4 Φ 입력 (anima IIT4 표준 경로).
- **시간축 옵션**(r3-c3): spike train 시간동역학의 temporal Φ — AKIDA=spiking 칩의 native 신호. v1=공간 region-Φ, v2=temporal.

### 12.3 toy 검증 질문 (sbs auto → 별도 구현)

Φ-on-chip 이 *좋은 CLM 의식 신호*인지 실측(검증 없이 채택 금지):
- **F-CLM-PHI-MEANINGFUL** (사전등록): region-Φ 가 ① 작은 n 에서도 non-trivial(Φ>0 변별) ② monopoly-collapse spike(저 Φ) vs rich spike(고 Φ) 변별 ③ size-robust(n 바꿔도 신호 보존, ln E 류 artifact 無).
- 검증 = ubu-1 GPU only(Mac 0 · NULL 류 ≤16) · verbatim `.verdicts/` + UNIVERSE H + CLAIMS. 🟢(Φ meaningful → 측도교체 성립) / 🔴(Φ도 부적합 → 더 깊은 reframe) 둘 다 정직 보고.

### 12.4 정직 경계

- PHI-NATIVE 는 routing-diversity 🔴(§11)를 *해결*하지 않고 *우회*한다 — 두 measure 는 orthogonal. §11 falsifier 는 닫힌 채 유지.
- exact Φ 불가(2^(2n)) → region/coarse 근사만 주장. 1.2M 노드 전체 Φ 는 미주장.
- v1 SW spike(akida_sw_lif) 측정 → HW(pi5 AKD1000) 측정은 후속. byte-identical SW↔HW(H_680)라 SW v1 이 HW 대리로 정당하나, 실 HW Φ 는 별도.
