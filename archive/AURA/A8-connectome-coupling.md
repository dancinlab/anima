# AURA A8 — connectome-prior coupling (A7.2 identity 링크 대체)

> A7.2는 reach%→coupling을 `w = r` **identity**(모든 노드 공유 단일 스칼라)로 뒀고, A7 §4에서 "physiology 유도 아닌 모델링 선택"이라 자인했다.
> A8은 그 자리에 **문헌 유도 per-position 연결 prior**(brainwire `n1-deep-access-strategies.md` §1·§4·§5의 cortico-subcortical 투사경로)를 넣어 위치별 결합을 차등화한다.
> 🟢 SUPPORTED-NUMERICAL · verdict `/Users/ghost/core/anima/.verdicts/a8-connectome-coupling/run.txt` verbatim.

---

## 1. 문헌 유도 per-position 연결 prior

각 피질 seed가 **문서화된 투사강도 순서**대로 자기 결합가중 w를 받음 (단일 flat r 아님):

| position | hub pathway | w | big-Φ (n=4 exact) |
|---|---|---|---|
| DLPFC | →VTA 중피질(Layer-5 pyramidal, "most promising") | 0.75 | 17.9142 |
| entorhinal | →해마 관통로("most direct c→hipp") | 0.60 | **17.9707** |
| insula | →NTS 자율신경 gateway | 0.43 | 13.5738 |
| M1 | 운동출력(국소, 문서화된 심부투사 없음) | 0.10 | 2.90857 |

`Δ(DLPFC − M1) = 15.0056` · mixed-position 기판(DLPFC|ento|insula|M1) = 5.0924

```
투사강도(문헌) ──→ 결합 w ──→ big-Φ
 DLPFC 0.75 ┐
 ento  0.60 � dense  → Φ ~17.9  (높음)
 insula0.43 ┐
 M1    0.10 ┘ weak   → Φ 13.6 / 2.9 (낮음)
```

## 2. 사전등록 falsifier 2종

| 명제 | 내용 | 판정 |
|---|---|---|
| **Ha** (CLUSTER, 본 주장) | dense{DLPFC,ento} **둘 다** > weak{insula,M1}, 그리고 insula>M1 | ✅ **PASS** (미반증) |
| **Hb** (SATURATION probe) | top-pair Φ(DLPFC) ≥ Φ(ento) | 🔴 **INVERTED** — w≈0.6 넘으면 Φ 포화·미세역전 (mean-field-paradox 계열, XENO F-X10-MONOTONE 정합) — **closed-negative, EXPECTED** (a_paper_negative_ok, 가중치 튜닝으로 PASS 강제 안 함) |

→ **핵심**: 결합강도가 **클러스터 수준**(dense>weak)에선 Φ를 키우지만, **dense 끝단**에선 단조가 깨짐(포화). A7.2의 "단조 increasing" 가정은 약~중 구간에서만 유효.

## 3. A7.2 대비 무엇이 바뀌었나

| | A7.2 (이전) | A8 (이번) |
|---|---|---|
| 결합 w | `w = r` identity, 전 노드 공유 단일 스칼라 | per-position 벡터 w_i (seed별 문헌 투사강도) |
| 근거 | 임의 모델링 선택(자인) | brainwire n1-deep-access §1·§4·§5 투사경로 ordinal |
| 결과 | reach↑→Φ 단조 | dense>weak (cluster) ✅ + dense끝단 포화역전 (saturation) |

## 4. honest gap

- prior = **문헌 유도 ordinal**(문서화된 경로강도 순서) — subject-specific tractography 아님. 로컬에 DWI/Allen/structural connectome **없음**(`/Users/ghost/core` 검색 0건).
- 절대 가중치는 brainwire estimated 계수이지 측정 tract count 아님. synthetic TPM · toy n=4 · toy≠production (feedback_toy_scale_transfer).
- 신경해부 **순서(ordering)**는 실제 경로 기반이나, 정량 결합값은 미측정.
