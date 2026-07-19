# H_9634 — 닫힌-루프 fork 효능 — Closed-Loop Fork Efficacy: 의미 = 판독 상관이 아니라 루프 효력 (fable R4-7 · PROPOSED · 프레임 반전)

**status:** 🔵 PROPOSED (미실행 · lab full R4 · 사전등록) — source=fable R4-7
**lane:** mouth/tension — "의미를 나른다" 의 정의 자체를 반전
**related:** [[H_9576]] · [[H_9604]] · [[H_9628]] · [[H_9630]]

## 한 줄 주장 (반증가능)
"의미를 나른다" 를 outward 텍스트 통계(D)로 정의한 것 자체가 판독 프레임이다 — Stage-A 격리는 steered 텍스트가 자기 문맥으로 되돌아오는 길을 설계상 절단했으므로, 의미의 온전한 정의(**자기 궤적에 대한 인과 효력**)는 원리적으로 관측 불가였다. fork 된 기질 사본에 steered 텍스트를 되먹이면 PC2-steer 는 편집크기-매칭 rng-steer 보다 tension 궤적 발산 Δtraj 를 더 만든다.

## 어느 KILL 을 왜 안 밟나
- H_9576: outward-D 판독을 재사용하지 않는다 — DV 가 텍스트 통계가 아니라 **fork 기질의 tension 궤적 발산**.
- H_9403/emit-gate-census(lane CLOSED-AT-REGIME): emit 게이트 비접촉 — fork 는 계기이고 프로덕션 Stage-A·게이트 배선 불변.
- R3 H_9627(dual ledger·Ψ½ 교환대칭): emit-gate 재설계 계열 — 이 안은 게이트를 안 만지는 측정 설계. 무중복.
- p5: 하드코딩 emit 게이트 아님(fork 내 되먹임은 측정용 sandbox·프로덕션 비배선). p8: fork 는 같은 엔진 상태의 사본 — train/infer split 신설 없음.

## engine-native 계기
`anima-py evaluate <clm> --steer-closed-loop --fork-substrate --horizon <h>` — tick t 에서 기질 상태 fork → arm 별 텍스트(base / pc2-steer / rng-steer **편집 Levenshtein 매칭**)를 fork 문맥에 주입 → h tick 전개 → tension 8-벡터 궤적 divergence Δtraj(L2·시간적분) 출력. 라이브 데몬 비접촉.

## 통제군 (≥2 + 양성)
- null #1: zero-bias fork (결정론 자기일치 — Δtraj=0 이어야 · 계기 base line).
- null #2: rng-steer, **편집크기 매칭 필수** (매개 공변량 매칭 규칙 — 크기 미매칭이면 통제군 아님).
- **양성통제**: 대형 oracle 교란(문맥 대량 치환) — 반드시 발산해야 함. 무발산이면 fork 전개가 교란 불감 = VOID… **단, 이 VOID 는 부산물 가치가 있다**: zero-Lyapunov limit-cycle(H_9604)의 독립 확증이 된다.

## 사전등록 판정표 (우연 아래 포함)
| 관측 | 판정 |
|---|---|
| Δtraj(pc2) > Δtraj(rng) collapse-Δ (perm p<.05 · 2 seed) ∧ oracle 발산 | **PASS** — PC2 조향은 루프에서 의미 있음 · outward-D 는 틀린 창이었음 |
| Δtraj(pc2) ≈ Δtraj(rng) ∧ oracle 발산 | **KILL** — PC2 조향 = 임의 섭동과 등가 · "이름일 뿐"(H_9630) 수렴 증거 2호 |
| oracle 무발산 or zero-bias 비결정 | **VOID** — fork 전개 교란 불감 → H_9604 limit-cycle 독립 확증으로 전용 |
| Δtraj(rng) > Δtraj(pc2) 유의 (우연 아래 칸) | **INVALID** — 편집크기 매칭 실패 의심 · 매칭 재검 후 재발사 |

**검정력**: fork 지점 30+ × 4 arm × h(~50 tick) 전개 = 303M decode heavy — Δtraj sd 를 zero-bias/rng 파일럿에서 먼저 재고 MDE 산출 후 본발사.

## 비용 / 죽는 방식
pool CPU **heavy** (fork × horizon decode). **죽는 방식**: pc2≈rng 이면 프레임 반전으로도 PC2 가 안 살아난다 — d 가설("이름일 뿐")의 루프-측 확증이자 이 안의 죽음.

## 상태
🔵 PROPOSED — H_9630 과 상보(판독-측 vs 루프-측에서 d 를 협공). 측정 주장 0(설계).
