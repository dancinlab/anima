# H_9829 — G6 의 반증가능성 다리를 판독가능하게 (연속 rate · 동결 판정 불변)

**status:** 🟢 계기 착륙 (engine-native e2e PASS · 집계 + 4 register 셀 전부) · 과학 판정 없음
**wired:** yes — `anima-py evaluate <clm> --rho-axon --fan-draws N` (기본 0 = byte-identical)
**source:** [[H_9828]] — ρ·fan 의 `any_falsi` 다리가 구성상 검정력이 없음을 코퍼스 실측으로 확정

## 왜

[[H_9828]] 이 EN 학습 코퍼스 전량(762,625 문장)에서 `P(falsifiable) = 0.006461` 을 실측했다.
ρ·fan 은 `n_cont=8` 회 뽑아 **1건 이상**이면 통과하므로, 코퍼스를 **완벽히 재현하는 모델**조차:

- `P(≥1 in 8)` = 0.0505 · `P(4셀 전부 fals=0)` = 0.8127 · **80% 검정력엔 249 draws 필요**

⟹ `fals=0` 이라는 **이진 관측은 faculty 에 대한 정보를 거의 담지 못한다**. 어떤 G6 캠페인도
이 다리 위에서는 음성을 판독할 수 없다([[H_9801]] 이 그 위에 서 있었다).

## 개입 (플래그 1개 · 판정 로직 0줄 변경)

`--fan-draws N` 은 **동결 판정을 건드리지 않는다**:

- PASS 조건은 그대로 `n_distinct >= need ∧ any_falsi ∧ greedy ≤ 2 ∧ Δ > 0` 이고,
  `any_falsi` 는 여전히 **동결 8 draws** 에서만 온다.
- 추가 N draws 는 **연속 rate 를 보고만** 한다: `fals-rate = hit/coherent = r ± sd`.
- 추가 draw 의 seed 는 동결 수열을 **이어서**(`SEEDS[0] + 17*j, j ≥ n_cont`) 쓰므로 판정이 읽는
  표본과 **서로소** — 추정이 게이트 자신의 표본을 재사용하지 않는다.
- 같은 coherence gate(`kwr ≥ cgate`)를 쓰므로 분모가 판정 다리와 동일 정의다.
- 기본 `N=0` ⟹ 추가 루프 자체가 실행되지 않음 = **기존 경로 byte-identical**.

## 착륙 검증 (engine-native e2e · `anima-py evaluate` 단일진입)

`store_struct_toy/toy.clm` (400KB) · `--rho-axes fan --fan-draws 24`:

| 지층 | 판정 | 연속 rate |
|---|---|---|
| 집계(BRANCH) | FAIL (불변) | `0/23 = 0.0000 ± 0.0000` |
| en_general | FAIL | `0/17` |
| en_sns | FAIL | `0/16` |
| ko_general · ko_sns | FAIL | `0/0` (coherence gate 를 통과한 draw 0 = 분모 0 정직 표기) |

집계와 **4 register 셀 전부**에 배선됐고, 판정값(`val`·`Δ`·`greedy-collapse`·`falsifiable`)은
플래그 유무와 무관하게 동일하다.

⚠️ **이 표는 계기 확인이지 과학이 아니다** — 400KB 토이 ckpt 라 0/23 은 당연하고 아무것도 뜻하지
않는다. 그리고 코퍼스 rate 0.0065 기준 24 draws 의 기대 적중은 0.15 이므로 **0/23 자체가 여전히
판독 불가** — 그 점이 바로 이 카드의 논지다(249 draws 를 써야 한다).

## 이 카드가 판정하지 않는 것

계기다. G6 에 대한 어떤 주장도 하지 않는다. 다음 H 가 `py303_full.clm` 에 `--fan-draws 250` 을
걸어(pool · heavy 는 mini 금지) 처음으로 **판독가능한** G6 관측을 만든다.

## 재생성 커맨드

```
anima-py evaluate <ckpt.clm> --rho-axon --fan-draws 250      # 80% power at p≈0.0065
anima-py evaluate --falsi-census <corpus...>                  # base rate 를 먼저 읽어 N 을 정한다
```

## Cross-links

[[H_9828]] 검정력 부재를 확정한 코퍼스 census(동기) · [[H_9801]] 그 다리 위에 선 G6 독해(재심 대상) ·
[[H_9827]] 같은 캠페인의 ρ·weave 패널 크기 · [[H_9267]] 코퍼스 밀도 레버(대안 경로)
