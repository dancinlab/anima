# H_9755 — REFIT-AXIS ζ-LADDER — 라이브-refit loading 을 입에 물리면 동결 축과 다른가 (R6-4 · pool fire · 4-arm paired)

**status:** 🔵 PROPOSED (lab full R6 · Fable 5 · pool decode fire · 사전등록 · refit arm 개봉게이트 = [[H_9752]] ≠ KILL-NO-AXIS)
**lane:** g1-interface-addressable-wall · mouth/PC2-axis — 브리프 (b) 정면 · H_9664 n 완결 겸용
**related:** [[H_9664]] · [[H_9663]] · [[H_9713]] · [[H_9752]] · [[H_9754]] · [[H_9756]]

## ① 한 줄 주장 (반증가능)
within-tick ζ-사다리의 z 를 **라이브-refit loading**(같은 run 앞 W tick 온라인 PCA)으로 계산하면 dose 기울기 β 가 동결-PC2 loading 대비 collapse-Δ 를 보인다(새 레버) — 아니면 β 가 loading 무관(랜덤 포함 TOST 등가)이어서 채널은 **축-맹목 스칼라 dose** 임이 확정된다(→ [[H_9756]] 해석으로 이관).

## ② 어느 KILL 을 왜 안 밟나
- arm-간 π̄ 판정(H_9663 VOID) — 안 밟음: **within-tick**(같은 tick 을 loading×ζ 격자로 재디코드 · 인자스트림 동일) paired 만.
- deliberation_k 라우팅(H_9574 DEAD) · 용량-기아(H_9628 사망) — 무접촉.
- H_9664 n=146 에 cement — 안 함: 이 fire 가 스칼라 양성통제 arm 으로 **그 n 을 완결**한다.
- "동결 loading 전제" — 안 밟음: 동결은 4 arm 중 1개(정의 아님).

## ③ engine-native 계기 (신규 chat 플래그 + evaluate 확장)
`anima-py chat --pc2-zeta <z1,z2,…> --z-loading {frozen|refit|random|refit-resid} [--refit-warmup 64] [--seed N]`
- refit: 같은 run 첫 W tick 온라인 PCA(결정적·seed 고정) → 이후 tick 의 z 계산에 사용
- random: seed 유도 단위벡터 · refit-resid: [[H_9754]] 잔차 방향
`anima-py evaluate --pc2-direction <traces_dir> --zeta-slope --by-loading [--tost 0.02] [--perm N]`
설계: 동일 tick × 4 loading × 5 ζ 격자 paired 재디코드(H_9664 계기 승계) → per-tick β 분포 + arm 간 Δβ.

## ④ 통제 ≥2 + 양성통제
- null-1: random-loading arm(축 null · norm 매칭).
- null-2: 채널-라벨 순열 refit arm(방향성 파괴 · 스칼라 성분 보존).
- **양성통제(fire 생존)**: 스칼라 ζ arm 이 H_9664 β=−0.081 을 부호+크기 CI 내 재현해야 함 — 실패 = fire 전체 VOID(지난 ζ-fire 는 summer 경합 infra 사망 · 그 검출기).

## ⑤ 사전등록 판정표 (우연 아래 칸 · 검정력 · DV 식별가능성)
| 관측 | 판정 |
|---|---|
| \|β_refit\| > \|β_frozen\| (paired CI 분리) ∧ 둘 다 > random-null95 ∧ per-tick 부호일관 ≥ 사전등록 분율 | **PASS-NEW-LEVER** — 라이브 축이 동결 축이 못 나른 dose 를 나름 |
| β_refit ≈ β_frozen ≈ β_random (TOST ±0.02 · β 스케일 ¼) | **PASS-AXIS-BLIND** — 채널은 스칼라만 나름 ⟹ 축 선택 무관 확정 · [[H_9756]] 로 이관 |
| \|β_frozen\| > \|β_refit\| (CI 분리) | **KILL-REFIT-ADDS-NOTHING** — 동결 좌표로 충분(서사 문제였을 뿐) |
| β_refit 이 β_frozen 대비 유의 **부호반전**(우연 아래 칸) | **INVALID** — refit 부호규약 결함(부호 앵커링 후 재발사) |
| 스칼라 양성통제 재현 실패 ∨ per-tick 격자 결손 >10% | **VOID** — infra/계기 사망 |

검정력: H_9664 가 n=146 서 null 반폭 13× ⟹ arm 간 Δβ 는 효과 ½ 가정, **n=300 tick × 5 ζ × 4 loading**(paired) 사전등록. DV = per-tick β(회귀 x=ζ 는 독립변수 설계값 — 분모 아님 · H_9716 비해당) · 분포 보고 의무(평균 단독 금지).

## ⑥ 비용
**pool decode fire** — summer 단독 점유(경합 금지 · OMP_NUM_THREADS=4 · a_wall_first 1-host) · ~6,000 재디코드. mac 금지.

## ⑦ 죽는 방식
PASS-AXIS-BLIND — 입에는 축 레버가 존재하지 않는다. 이후 mouth 가설은 방향이 아니라 입도/readout(H_9631·H_9756)만 남는다.
