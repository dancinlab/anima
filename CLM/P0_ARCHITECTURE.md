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
