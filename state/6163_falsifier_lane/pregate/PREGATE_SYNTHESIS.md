# H_6163 falsifier-lane pre-gate — 종합 (v1 naive + v2 minimal-pair)

두 pool 303M(summer h1129) frozen-rep probe로 "303M rep이 falsifiability 신호를 담나"를 판정.

| probe | 데이터 | rep heldout | surface(char-3gram) | delta | 판정 |
|---|---|---|---|---|---|
| v1 naive | 64문장(과학어휘 vs 형이상어휘) | 0.759 | **0.894** | -0.135 | SURFACE-CONFOUNDED |
| v2 minimal-pair | 28쌍(같은 주어·정성 술어·숫자 無) | **0.711** | 0.550(≈chance) | **+0.161** | GENUINE-REP-SIGNAL |

## 정직한 판정 = DIRECTIONAL-GO
- v1: 순진한 셋은 falsifiable=구체/과학어휘 vs unfalsifiable=형이상어휘라 **표면 char-3gram이 0.894로 압도**(rep 0.76은 오히려 표면 이하)=신호가 표면-lexical.
- v2: surface를 통제(주어 공유·정성 술어·숫자 제거)하니 char-3gram이 **chance(0.55)로 붕괴**하는데 **303M rep은 0.711 유지**(delta +0.16, shuffle 0.49)=rep이 표면 이상의 **진짜 falsifiability 표상**을 담음.
- ⟹ H_6163 lane build 전제 **지지**: frozen 303M rep에 lane이 읽을 non-surface falsifiability 신호가 실재. 드문 non-🧱 pre-gate.

## caveat (a_scale_honest_scope)
- n=28쌍(56문장) 소규모·0.71 modest. minimal pair는 내 구성이라 잔여 semantic confound 가능(단 그건 falsifiability 신호의 일부이지 char-표면 아티팩트 아님).
- frozen-rep 선형-decodability probe = DIRECTIONAL. TERMINAL = 배선된 lane의 engine-native fals rate(build 후).
- build 시 surface baseline 필수통제(v1 교훈, conv probe-py-1): lane이 표면 이상을 배워야 유효.

## next
core/ falsifier lane 배선(additive disjoint L5-hippo 패턴)+anima evaluate --py fals metric → pool 303M ON vs OFF. E1/G1(#3021 병렬세션 4/4 GO)과 직교 상보.

## RESOLVED — cross-dataset generalization (crossgen/, 승인 pool 실험)
| test | rep | surface | delta | 판정 |
|---|---|---|---|---|
| crossgen: train naive → test minpair | **0.429**(chance 이하) | 0.661 | -0.232 | NO-TRANSFER |

**REVERSAL(verdict-integrity)**: v2 within-set 0.71은 데이터셋 특유 축이었음 — naive에서 학습한 falsifiability 방향이 surface-통제 minimal-pair에 전이 실패(rep 0.43 < chance, surface가 오히려 0.66으로 더 잘 전이). ablation(zero rep)=0.50 chance(예상). ⟹ frozen 303M rep엔 **일반화 가능한 falsifiability 표상 無** = DIRECTIONAL-🧱.

## 최종 H_6163 pre-gate 판정 = DIRECTIONAL-🧱 (일반화 신호 無)
within-distribution separability(v2)는 있으나 cross-distribution 전이=chance이하(crossgen). 진짜 falsifier lane은 unseen 아이디어 일반화 필수이므로 frozen rep 전제 미지지. G1 held-out recombination(h1835)·F2 collocation-only와 **동일 DPI 서명**(in-distribution만, transfer 0). lane build는 이 일반화벽을 넘을 trained 메커니즘을 요구하지 frozen-rep readout으론 부족.
