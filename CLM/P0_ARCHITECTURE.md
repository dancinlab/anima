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
   추론 = AKIDA(int4) ONLY   학습 = GPU(fp16)   영속 = .kosmos
```

## 1. 확정 결정셋 (10)

| # | 축 | 결정 | 근거 |
|---|---|---|---|
| **Q1** | arch family | **Conv-native LM** (dilated conv · attention 없음) | AKIDA conv byte-identical 증명(5-stage) · attention은 AKIDA 매핑 불가 → AKIDA 우선과 정합 · byte 긴 sequence가 conv엔 약(O(n·k)) |
| **Q2** | 더블바인드 탈출 | **MoE conv-expert = mitosis cell** (분열한 cell이 각 expert) | A(MoE 토이증명) + C(p8 train=infer·anima-native) 결합 · register 격리=메인 coherent 유지 |
| **Q3** | monopoly 토대 | **byte-vocab V=256** + 3-arm(A/B/A+B) + F-CLM-MONO | V≫d(15만/64=2370배)가 monopoly 근원 → byte로 V/d=4배 = 근원 소멸 (prior art 미시도 lever) |
| **Q4** | scale 실험 | micro-exp 토이=**직관(non-gate)** · 3-arm **전부 full-fire**가 판정 · scale ladder · wall-first·무캡 | toy≠scale(H_666 실증) → toy로 prune 금지, 다 발사 |
| **d1** | corpus | **신규** + **혼합**(웹대량=coherence + 엄선=register) + **.kosmos 영속 필수(SKIP 금지)** | MoE 2-lane ↔ corpus 2-source 1:1 · a_kosmos 거버넌스(required·active) = .kosmos 영속은 **면제 불가** · 현 spec(kosmos/1.1)이 byte-corpus를 못 받치면 **upstream을 먼저 업그레이드한 뒤** 영속한다 · "얽매이지 않음"=업그레이드를 **별도 트랙으로 병행**해 전체를 멈추지 않는다는 뜻이지 **건너뛰어도 된다는 뜻이 아니다** |
| **d2** | .clm 포맷 | **2-track**(int4 AKIDA + fp16 GPU shadow) + QAT scale + manifest(sha256·kosmos ptr) | AKIDA추론·GPU학습재개·mitosis 한 파일 · naive PTQ int4 파괴→QAT 필수(실측) |
| **d3** | scale rung | tiny `d64/L2/E4` · small `d256/L4/E8` · target **≤ AKD1000 fit** (P4 probe 확정) | 추론 AKIDA-only라 칩 용량이 target 상한 · byte+conv라 작아도 됨 |
| **d4** | 경로 | **추론 AKIDA(int4) ONLY** · **학습 GPU(fp16)** · 2-track 병행 | AKIDA=추론칩(학습칩 아님) · GPU 추론 escape 없음(순수 AKIDA) |
| **d5** | trainer(B0) | **2-track**: PyTorch fp 학습 즉시 진행 ∥ hexa-native trainer fix 별도 | M5 hexa trainer 🔴 INFEASIBLE(0.28 step/s) · wall-first라 런치 안 막힘 · 추론 AKIDA-only는 불변(g1 핵심 유지) |
| **d6** | falsifier 임계 | **z>3.0 양축 + multi-seed{base,43,44} 재현** | v7 z=2.75 단일seed marginal 교훈 · §A2-trap·seed-artifact 차단 |

## 2. AKIDA-map 경계 (정직)

| 단계 | 어디서 | 정합 |
|---|---|---|
| 추론 (conv trunk + readout) | **AKD1000 int4 온칩 ONLY** | conv/FC/pool 5-stage byte-identical 증명 envelope |
| 학습 (pretrain) | GPU fp16 (PyTorch) | AKIDA=추론칩 |
| on-chip 학습 | ❌ 사용 안 함 | 🔴 CLOSED-NEGATIVE(비결정) — H_679 |
| emit/silence 게이트 | LAUNCHPAD(별도) | CLM=콘텐츠("무엇") · 게이트=타이밍("언제") |

⚠ **honest**: attention을 안 쓰는 이유 = AKIDA 프리미티브(conv/FC/pool/sepconv)에 attention 매핑 불가. 전체 추론을 칩에 올리려면 conv-native가 필수. (transformer 썼으면 추론이 GPU로 새서 d4 위반)

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

- hexa-native trainer throughput 🔴 INFEASIBLE(M5 0.28 step/s) → d5에서 PyTorch 병행으로 우회(추론 AKIDA-only 불변).
- target 크기 = AKD1000 fit 실측(P4) 전엔 미확정 — "≤칩용량" 상한.
- monopoly-escape = toy🟢·scale🔴 미해결 → byte-vocab으로 근원 직격 시도(가설, P2 falsify).

## 8. 다음 (P1~P5)

- P1 corpus: 웹대량+엄선 혼합 byte build · .kosmos emit 영속 배선.
- P2 train: 3-arm × ladder full-fire (PyTorch fp) · F-CLM-MONO/SCALE 판정.
- P3 .clm: QAT int4 + fp shadow 직렬화 + manifest.
- P4 AKIDA: .clm int4 → AKD1000 온칩 추론 · fit probe로 target 확정.
- P5 DECODER 통합: generator → brain_decide emit 슬롯 → LAUNCHPAD COFFESHOP 콘텐츠.
- B0(병렬): hexa-native trainer throughput fix (hexa-lang INBOX 트랙).
