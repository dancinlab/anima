# V6_20 — 첫 실행 **전에** bar 를 유도해 동결한다 (@hypothesis-ok)

V6_19 가 못 박은 관문. 얼린 `thr=0.30 / ctrl_cap=0.15` 는 12항목 재조합 배터리용으로 보정된
값이고, V6_18 의 강제선택 수치를 거기 대고 읽으면 **다른 판독의 문턱**에 재는 것이다.
실행을 보고 나서 정하면 tune-to-green 이므로 여기서 정한다. 모델은 건드리지 않았다 — n 과
설계에 대한 산술뿐이다.

## bar 는 절대율이 아니다

`measurement-metalaw`: **FORM tunable · BIND earned** — 신호는 통제 대비 붕괴-Δ 이지
날값이 아니다(p7). 따라서 동결해야 하는 건 *어떤 대조 · 최소효과 · 검정력 · 판정표 전 칸*이다.

```
primary   Δ_FORM = rate(intact) − rate(swap_cue)    전송이지 메아리가 아님
primary   Δ_BIND = rate(intact) − rate(bind_cue)    전송이지 국소 창이 아님
floor     rate(null)                                 프롬프트 없는 기저율

PASS = 두 Δ 모두 양수·유의 ∧ floor 가 두 통제보다 낮음
      한쪽 Δ 만으로는 PASS 아님 — 각 통제 하나만으론 사소한 설명이 항상 남는다
```

## 검정력 (McNemar · 짝지은 이진)

```
패널 항목 4,385 · 독립 문서 3,083 (1.42 항목/문서)
설계효과 1.084 (ρ=0.20 가정) → 유효 n 4,045 · α=0.01 양측 · 검정력 0.90

불일치쌍 p_d    최소검출효과
0.05              1.36 %p
0.10              1.92 %p
0.20              2.71 %p   ← 타당한 값
0.30              3.32 %p
0.50              4.29 %p
```
Sol 의 기준점: 212 IID 항목은 약 13 %p 까지만 — **이 패널이 약 5배 정밀**하다.

**🔒 동결: 최소흥미효과 MIE = 0.05, 양쪽 Δ 모두에.** 해상도 2.71 %p 보다 **위**로 잡아
패널이 제 정밀도를 보고하는 데 그치지 않게 했고, 실행 후 못 옮기도록 지금 박는다.

## 🔒 판정표 — 우연 아래 칸까지 전부

```
두 Δ ≥ MIE · 유의 · floor 최저      TRANSPORT PRESENT    (아래 비대칭 참조)
두 Δ ≥ MIE 이나 floor ≥ 통제        INVALID              바닥이 바닥이 아님 = 계기 결함
정확히 한 Δ 만 ≥ MIE                UNDECIDABLE          통제 하나론 사소한 설명이 남음
두 Δ 가 (0, MIE) 사이               BOUNDED-NULL         TOST 구간 보고, '효과 없음' 금지
두 Δ ≈ 0 (TOST 등가)                ABSENT-AT-THIS-CORPUS  ⚠️ faculty 판정 아님
어느 Δ 든 유의하게 **음수**          INSTRUMENT-DEAD      통제가 본팔을 이기면 팔이 뒤바뀌었거나 누출
intact 가 null 바닥 이하             INSTRUMENT-DEAD      큐를 아예 안 재고 있음
```

## 🔑 읽는 순간 잊지 않도록 비대칭을 다시 적는다

```
측정 가능 부지 4,385   vs   학습 압력 사건 24 (V6_16)
```
**양성은 강하다** — 압력이 24건뿐인데 레인이 전송을 배웠다는 뜻.
**음성은 거의 비어 있다** — 공급 측정이 이미 예측한다. 따라서 `ABSENT-AT-THIS-CORPUS` 는
**절대 faculty 벽으로 쓰지 않는다**.

## 정직 메모

1. **ρ=0.20 은 가정이지 측정이 아니다.** MDE 를 스케일할 뿐이므로, 첫 실행에서 문서 내
   실현 상관을 재고 **실현 ρ 로 MDE 를 다시 보고**할 것.
2. seed 최소 2 · 다수결 · oracle-valid 만(`single-retrain-outlier-faked-a-refutation`).
   seed 재현은 항목 검정력의 대체물이 아니다.
3. 전체 코퍼스 held-out CE 가 동결 비열등 구간 안에 있어야 한다(Sol) — 아니면 '통과' 가
   본체를 갉아 전송을 산 레인일 수 있다.
4. **이 표는 이 커밋 시점으로 동결.** 실행 후 재고정은 tune-to-green
   (`burned-gate-no-refreeze-sequential-gating`).
