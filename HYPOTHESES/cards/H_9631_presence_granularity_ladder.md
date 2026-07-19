# H_9631 — 현존-입도 사다리 — Presence-Granularity Ladder: coverage-포화 기전과 byte→span 회복 (fable R4-4 · PROPOSED · b 정면)

**status:** 🔵 PROPOSED (미실행 · lab full R4 · 사전등록 · H_9628 INSTRUMENT-PASS 후 개봉) — source=fable R4-4
**lane:** mouth/tension — byte 입도 병목의 기전 특정 + 탈출 입도
**related:** [[H_9576]] · [[H_9628]] · [[H_9630]]

## 한 줄 주장 (반증가능)
byte 입도 실패의 기전은 **coverage 포화**다 — T=24 byte 창의 "문맥 현존" 집합은 고빈도 철자 byte(공백·모음·자주 쓰는 자음)를 거의 전부 포함하므로 −z bias 는 의미-맹목 빈도 섭동으로 퇴화한다(텍스트는 바뀌나 의미는 안 실림 = H_9576 관측 그대로). 현존 판정을 n-gram/단어 span 으로 올려 **문맥 내용의 재등장이 완성되는 후보만** 벌점하면 방향성 ρ 가 부호+로 회복된다.

## 어느 KILL 을 왜 안 밟나
가장 가까운 KILL = H_9576 (byte 입도 bias 방향성 — n=270 KILL). 이 안은 byte 입도를 재검정하지 않는다(byte arm 은 **알려진-null 음성통제**로만 씀) — 죽음의 기전 가설(포화)을 세우고 **다른 입도**를 검정한다. p5 안전성: Stage-A 격리 그대로(게이트는 BASE 후보만 청취·steered 는 emit 확정 후 outward 2차 decode 만) — 오너가 이미 승인한 배선의 현존-판정 함수만 교체.

## engine-native 계기
`anima-py evaluate <clm> --pc2-direction --presence-granularity {byte|ngram:3|ngram:5|word}` — bias 대상 후보 byte = 해당 입도에서 창 내 매칭이 **완성되는** byte 만(창 내 n-gram trie). $0 선행: 기존 H_9576 trace 로 입도별 coverage 율(후보 중 bias 피격 비율) 산출해 byte≈포화 예측을 먼저 확인 — 단 cement 는 플래그 산출 수치로만(H_9303/9307).

## 통제군 (≥2 + 양성)
- 음성통제(알려진 null): byte arm = H_9576 재현.
- null: rng-z arm (각 입도).
- **양성통제**: dose 사다리 (각 입도 — H_9628 승계 · 입도별 계기 생존 확인).

## 사전등록 판정표 (우연 아래 포함)
| 관측 | 판정 |
|---|---|
| 입도↑ 에 따라 ρ 단조 회복 ∧ ngram:5/word 에서 ρ > null95 부호+ (2 seed) | **PASS** — 입도가 병목이었음 · 의미 전달의 최소 입도 특정 |
| 전 입도 null ∧ 각 입도 dose 생존 | **KILL** — 입도는 병목 아님 → z 축 사망 쪽(H_9630 합류) |
| 해당 입도 dose 사망 | **VOID** — 그 입도 계기 무효(coverage 희소로 bias 무접촉 가능 — word 입도서 예상 리스크) |
| span ρ 유의 음(−) (우연 아래 칸) | **INVALID** — bias 부호 역설계 결함 · 수리 먼저 |

**검정력**: 입도 4 × 270 tick × 2 seed ≈ 2200 tick. |ρ|≥0.12/입도 해상(H_9576 동급).

## 비용 / 죽는 방식
pool CPU. **죽는 방식**: word 입도에서도 null(그 입도 dose 생존 하)이면 "입도 병목" 기전은 사망 — 벽은 입도가 아니라 z 또는 프레임(H_9630/9634)으로 좁혀진다.

## 상태
🔵 PROPOSED — 개봉 조건 = H_9628 INSTRUMENT-PASS. 측정 주장 0(설계).
