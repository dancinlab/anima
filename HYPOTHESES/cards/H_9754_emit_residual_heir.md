# H_9754 — EMIT-RESIDUAL HEIR — 'emit-직교 제2 DOF'의 라이브 상속자를 좌표-프리로 구성한다 (R6-3 · $0+rider)

**status:** 🔵 PROPOSED (lab full R6 · Fable 5 · $0 안정성 + [[H_9755]] fire rider arm · 사전등록 · 개봉게이트 = H_9752 ≠ KILL-NO-AXIS)
**lane:** g1-interface-addressable-wall · mouth/PC2-axis — (a)→(b) 다리
**related:** [[H_9741]] · [[H_9713]] · [[H_9752]] · [[H_9755]]

## ① 한 줄 주장 (반증가능)
인증 3속성 중 (iii) emit-직교는 동결 좌표의 우연이었고, **라이브 상속자는 구성 가능**하다 — 라이브-refit 2-D 부분공간 안에서 emit 을 회귀로 제거한 **잔차 방향**이 (i) run 간 안정하고(주각) (ii) held-out tick 서 emit 과 비결합이며 (iii) within-tick ζ dose 를 나른다. 셋 중 하나라도 죽으면 "emit-직교 DOF" 서사엔 라이브 지시체가 없다.

## ② 어느 KILL 을 왜 안 밟나
- "동결 loading 전제" — 안 밟음: 동결 PC2 는 **비교 arm** 일 뿐, 정의는 라이브 refit+잔차화.
- H_9741(라이브 PC2 emit-결합)을 재부정 안 함 — 그 결과를 수용하고 "결합은 좌표 사고"라는 **다음 질문**을 검정.
- tune-to-green — 안 밟음: 잔차 방향은 **split A 에서 적합, split B 에서만 판독**(자기적합 순환 차단).
- H_9716 설계분모 DV — 안 밟음: DV = held-out |r| 과 주각(분모-프리).

## ③ engine-native 계기
$0 부: `anima-py evaluate --pc2-direction <traces_dir> --subspace-stability --emit-residual [--cv split-half] [--seed N]` (H_9752 플래그 확장) — 부분공간 내 emit 회귀(split A) → 잔차 방향의 run 간 주각 + split B held-out |r|.
fire 부: [[H_9755]] 의 `--z-loading refit-resid` arm (동일 fire 동승 · 한계비용 ~0).

## ④ 통제 ≥2 + 양성통제
- null-1: 8-공간 전체에서 emit-회귀벡터에 직교화한 **랜덤 직교 방향**(부분공간 밖) — '부분공간이 특별한가 vs 아무 직교나 되는가' 분리.
- null-2: 동결-PC2 arm (비교 좌표).
- **양성통제(readout 생존)**: emit-**정렬** 방향이 held-out tick 서 H_9741 의 |r|≈0.207 을 재현해야 함(못하면 readout 죽음 = VOID).

## ⑤ 사전등록 판정표 (우연 아래 칸 · 검정력 · DV 식별가능성)
| 관측 | 판정 |
|---|---|
| 잔차 방향 cross-run 주각 < null95 ∧ held-out \|r\|_resid < \|r\|_aligned CI 하한 ∧ (fire) β_resid > random-null95 | **PASS-HEIR** — emit-직교 DOF 는 좌표-프리 불변량으로 생존 · 인증 서사 부활(동결 좌표만 사망) |
| 잔차 방향 불안정 ∨ held-out \|r\|_resid ≈ \|r\|_aligned (TOST) | **KILL-COORDINATE-ARTIFACT** — 라이브에 emit-직교 DOF 지시체 없음 · H_9428 (iii) 최종 사망 |
| 안정+비결합인데 (fire) β_resid ≈ random-null (TOST) | **HEIR-MUTE** — 상속자는 있으나 입엔 안 닿음 ⟹ (c) 축-무관 쪽 증거 |
| held-out r_resid 가 null 넘어 유의 **음**(우연 아래 칸) | **INVALID** — 부호/직교화 결함 |
| 양성통제 \|r\|≈0.207 재현 실패 ∨ H_9752=KILL-NO-AXIS | **VOID** — readout 죽음/대상 부재(개봉 금지) |

검정력: 안정성 부 = 기존 트레이스 pooled n≈450 tick(split-half CV) · |r| MDE 0.1 해상. fire 부 n 은 H_9755 사전등록 승계. DV 식별가능성: 주각·\|r\| 분모-프리 · 우연은 surrogate/순열 재유도.

## ⑥ 비용
**$0**(안정성·결합) + H_9755 pool fire 동승 1 arm.

## ⑦ 죽는 방식
잔차 방향이 run 마다 다른 곳을 가리키거나(주각 null), emit 잔차화가 held-out 에서 안 풀리면 — "제2 DOF" 는 동결 좌표의 픽션이었고 라이브 구조는 emit-결합 단일 밴드 + 노이즈로 축소된다.
