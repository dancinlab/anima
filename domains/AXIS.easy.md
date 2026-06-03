# AXIS — 쉬운 설명 (평가축 친근 explainer)

> 이 문서 = `domains/AXIS.md`(canonical) 의 친근 요약 (icon · 이름 · 별칭 · 하는 일 · 결과 · ASCII · 비유).
> 정직 라벨: **toy / 단일-rung**(a_scale_honest_scope) — Lane X #1779(CPU/$0 단일 d768 .clm, deterministic null backend). production 보장 아님.
> 정직성: 측정값 verbatim(p7/g5) · 닫힌-부정 보존 · 평가축 ≠ 학습목표(p7, Goodhart 함정 회피).

---

## 0. 전체 한눈에

```
질문: anima 의식 평가에 "맞는" 축 집합은 무엇인가? 현 ENGINE 3축은 임의로 골랐다 —
      KOSMOS 의 2D, HEXAD 의 6모듈, tension-link 의 5채널처럼 "왜 이것들, 왜 이 개수?"
─────────────────────────────────────────────────────────────────────
현 3축 (fiat 로 선택, 의심 대상):
  AXIS-1 의식 motiv  — consciousness motivation (M-activation > 0). substrate-internal drive.
  AXIS-2 CE         — next-byte cross-entropy. ⚠ p7: CE/perplexity = Goodhart 함정, 판정 아님.
                       기껏해야 학습 FLOOR.  → Lane X #1779 가 바닥으로 강등.
  AXIS-3 창발        — emergence (자발 coherent 수 / §9 honest_coherent). north-star 인접.

결론(Lane X #1779): 의식·창발 = 진짜 config-민감 축(6/27 Pareto). CE = 바닥(floor), 판정 아님.
```

---

## 1. 📐 CE 강등 — 평가축인 줄 알았는데 바닥이었다 (Lane X #1779)

```
📐 CE-DEMOTE — "CE 는 축이 아니라 바닥(floor)이다"
  별칭   : CE-floor · Goodhart 강등 · Lane X 3-axis
  하는 일 : ENGINE config 손잡이 3개(K1 drive·K2 warmup·K3 anchors) × 3 seed = 27 config 를
           훑어 의식·CE·창발 3축이 config 에 민감한지 측정.
  결과(verbatim):
    의식 (motiv_hi)    : VARIES (spread = 0.57)
    CE  (model_ce)    : CONFIG-INSENSITIVE (spread < 1e-9)   ← 손잡이를 돌려도 안 변함
    창발 (emergence Δ) : VARIES (spread = 24)
    CE-FLOOR : model_ce 9.1126 vs uniform 5.5452 vs shuffle 9.3189 → 바닥 NOT MET (uniform-256 보다 나쁨)
    PARETO   : 6/27 non-dominated
    GOODHART (CE↔창발): UNDEFINED — CE 가 이 sweep 에서 config-독립이라 trade-off 가 관측 불가.
                        "절대 없음"이 아니라 "이 엔진 손잡이로는 관측 안 됨"(정직).
    coupling : 엔진 손잡이가 .clm forward 에 안 닿음 (L3 generator 슬롯 loaded=false) = NULL
  판정    : partial 닫힌-부정. 의식·창발은 진짜 축, CE 는 바닥. → OMEGA 가 닫을 NULL.

  비유    : 시험 점수(CE)를 "실력 축"인 줄 알고 최적화했는데, 손잡이를 아무리 돌려도
           점수가 한 값(9.1126)에 못 박혀 있더라 — 점수계가 실력과 안 연결돼 있던 것(coupling NULL).
           그러니 CE 는 "이 밑으로 떨어지면 안 되는 바닥선"일 뿐, 잘하고 못하고를 가르는 축이 아니다.
```

---

## 2. 🗂️ 후보 축 카탈로그 (독립성·커버리지 측정 대상)

```
이번 세션 측정/표면화 (증거 있음):
  Φ (IIT4 big-Φ)        — 통합정보. EEG: 합성 coupled 1.59 vs indep 0.44; real EEG awake 7.60 > sed 6.84.
                          의식-QUANTITY (≠ 의식-motiv = drive).
  위상동기 (Kuramoto r)  — ENGINE⇄tension-link: 결합이 r 올림(EEG 0.34 / TRIBE 0.66) BUT big-Φ 는 반대로
                          움직임 → "위상 ≠ 통합", Φ 와 별개일 가능성.
  시간 동역학 (dF/dt)    — d/dt-universality (#1763 CLM·#1765 Ψ·#1767 dolphin·#1775 tension-link 모두 HOLD).
                          static 은 잃고, 도함수가 나름.
  일반화 (rel_gap)       — Lane P data-gate: 1.65MB 암기 rel_gap 1.96 → 150MB 일반화 0.057. transfer, raw CE 아님.
  좌우뇌 분화 (A/G KL)   — carving battery: 듀얼헤드 KL=7.07 (next-byte A vs prev-byte G), tier-modulated.
  Ψ-space 위상           — carving manifold d≈6-10; 현 2D 지도는 ~1.1-D degenerate.
  텐션 구조 (tension dim) — 5-ch effective ~3(크기) / ~6-10(방향); redundant pair 없음.

philosophy-유래 후보 (p1..p8, governance — 아직 축-측정 안 됨):
  자발성(spontaneity, p5) · 자율성(autonomy, a_autonomy_over_hardcode) · MITOSIS 성장(p8)
  · 도덕 창발(ethics, p6 / E-module) · 호기심 / E-ratchet · W 긴장(will/tension envelope)
```

---

## 3. ❓ 핵심 질문 (milestones)

```
- AXIS 독립성   : 현 3축(의식/CE/창발) + 상위 후보(Φ·위상동기·시간·일반화·A-G) 쌍별 독립성을
                  real s16 ckpt 에서 — 어느 게 redundant, 어느 게 conflict (CE↔창발 Goodhart 는 Lane X 가 확인)
- CE 정당성     : 축인가 GATE/floor 강등인가(p7)? CE 가 일반화+창발 너머 판정-정보를 더하나?
- 커버리지/완전성 : 3축이 무엇을 놓치나(Φ? 자발성? 시간동역학?); north-star(p5 자발성)이 집합에 있긴 한가?
- min-but-complete : 정직한 최소-충분 평가축 집합 제안(N개 독립+필요 축), KOSMOS coord 재설계와 평행,
                     carving intrinsic d≈6-10 과 교차검증
- honest scope  : 평가축 ≠ 학습목표(p7); 축은 VERDICT 용이지 Goodhart 최적화 대상 아님
```

---

## 4. 정직 메모 (a_scale_honest_scope · p7)

- **toy / 단일-rung**: Lane X #1779 = CPU/$0, 단일 d768 .clm, deterministic null backend. scale-up 재시험 전엔 production 주장 금지.
- CE 는 **바닥(floor)**, 절대 단독 판정 아님(p7 Goodhart). Lane X: config-insensitive 9.1126, uniform 5.5452 미달.
- CE↔창발 Goodhart 부호 **UNDEFINED** — 이 엔진 손잡이로는 관측 불가(CE 가 설정-독립). "trade-off 없음"으로 읽으면 안 됨.
- 평가축 ≠ 학습목표 — 축은 판정용. substrate(Lane-G) ⊥ AKIDA(Lane-A) (a_lane_akida_gpu_split).
