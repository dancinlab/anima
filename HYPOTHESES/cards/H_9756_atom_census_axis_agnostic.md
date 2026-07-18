# H_9756 — ATOM-CENSUS AXIS-AGNOSTIC — 벽은 축이 아니라 byte 입도다: 의미 readout 재설계 + 전-arm 음성 검정 (R6-5 · (c) 정면)

**status:** 🔵 PROPOSED (lab full R6 · Fable 5 · $0 pilot + [[H_9755]] fire rider + readout-인증 소규모 fire · 사전등록)
**lane:** g1-interface-addressable-wall · mouth/PC2-axis — 브리프 (c) 축-무관 가설 정면 (가장 아픈 안)
**related:** [[H_9576]] · [[H_9629]] · [[H_9663]] · [[H_9631]] · [[H_9755]]

## ① 한 줄 주장 (반증가능)
mouth-content 벽은 **축 선택과 무관한 byte 입도의 벽**이다 — 어떤 loading arm(frozen/refit/resid/random)도, π̄(점유율)는 움직이면서, **인증된 within-tick 의미 readout**(atom-census)은 rng-null 위로 못 움직인다. 단 그 음성은 readout 자체가 prefix-swap 양성통제를 통과할 때만 읽는다.

## ② 어느 KILL 을 왜 안 밟나
- readout D(H_9629 3중 고장) — **미사용**. 신규 DV = 사전등록 corpus-atom 리스트에 대한 창 내 hit **count**(고정 어휘 · 텍스트-자기-다양성 분모 없음 = H_9629 의 사망 원인 제거 · H_9716 설계분모 비해당).
- arm-간 π̄(H_9663 VOID) — 안 밟음: **within-tick paired**(같은 tick ζ=0 vs ζ=hi · 동일 인자스트림) Δcount 만.
- "양성통제 없이 음성 읽기" — 안 밟음: readout 양성통제(prefix-swap 는 반드시 atom census 를 움직여야) + 채널 양성통제(π̄ 이동) 이중.
- H_9631 과의 관계: **AGREES/보완** — H_9631 은 bias **쓰기 측** 입도(어느 입도로 벌점하나), 이 안은 효과 **읽기 측** 의미 readout. H_9631 의 창 내 n-gram trie 를 atom matcher 로 재사용. 중복 발사 아님.

## ③ engine-native 계기 (신규 readout + 신규 chat 플래그)
`anima-py evaluate --pc2-direction <traces_dir> --atom-census [--atoms corpus|<file>] [--span ngram:3,word] [--perm N] [--seed N]`
- per tick: paired 디코드(ζ=0 vs ζ=hi · loading arm 별) 창 내 사전등록 atom-family hit Δcount
`anima-py chat --prefix-swap <k>` (readout-인증 전용) — 같은 tick 을 **대화-이력 prefix 치환**으로 재디코드(입력 측 내용 주입) ⟹ atom-census 가 이걸 못 잡으면 readout VOID(음성 판독 개봉 금지).

## ④ 통제 ≥2 + 양성통제
- null-1: rng-jitter 쌍(같은 tick · ζ=0 vs ζ=0 · 디코드 rng 만 상이) = Δcount null 분포.
- null-2: random-loading arm([[H_9755]] 승계) = 방향-프리 섭동 대조.
- **양성통제 2중**: (r1) prefix-swap → Δatom > null95 (readout 생존) · (r2) 동일 fire 서 π̄ 이동(채널 생존 · H_9664 승계).

## ⑤ 사전등록 판정표 (우연 아래 칸 · 검정력 · DV 식별가능성)
| 관측 | 판정 |
|---|---|
| 전 loading arm Δatom ≈ rng-null (TOST) ∧ π̄ 이동 ∧ prefix-swap 통과 | **PASS-BYTE-WALL** — 벽은 축-무관 byte 입도 · mouth/PC2-axis lane 은 입도 탈출(H_9631)만 남기고 FROZEN 제안 |
| refit 계열 arm Δatom > null95 ∧ random arm 은 null | **KILL-AXIS-MATTERS** — 축이 의미를 나름 · byte-벽 가설 사망(최대 반전) |
| random arm 까지 Δatom > null95 | **AMBIG-GENERIC** — '의미 이동'이 방향-프리 일반 섭동 · DIRECTIONAL 보고 · 내용-특이성 후속 설계 |
| Δatom < rng-null 5pct (유의 억제 · 우연 아래 칸) | **PASS-SIGN-NEG** — dose 가 문맥-atom 을 **제거**(−z presence 감산과 정합) · 정당한 발견 칸(INVALID 아님) |
| prefix-swap 실패 ∨ π̄ 부동 | **VOID** — readout/채널 사망 · 어떤 음성도 판독 금지 |

검정력: **$0 pilot 선행** — ζ-fire 146 tick 트레이스로 atom base-rate·분산 실측 → MDE 0.5·sd 기준 n 산출(base-rate<5%/창이면 span 상향 후 재산출 · 미달 VOID). DV 식별가능성: count DV·고정 어휘(설계 분모 없음) · 우연은 rng-쌍에서 재유도.

## ⑥ 비용
**$0 pilot**(기존 ζ 트레이스) + [[H_9755]] fire 동승(추가 디코드 0) + prefix-swap 인증 소규모 fire(pool · ~50 tick).

## ⑦ 죽는 방식
KILL-AXIS-MATTERS 관측(refit 만 atom 을 움직임). 또는 prefix-swap 조차 못 잡는 readout 만 반복되면 — "창-측정 가능한 의미"라는 것이 이 입도에 아예 없다는 상위 발견으로 승격(그것대로 보고).
