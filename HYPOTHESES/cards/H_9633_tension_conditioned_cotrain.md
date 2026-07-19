# H_9633 — tension 조건화 공학습 — Tension-Conditioned Cotrain: 사상은 decode 가 아니라 학습이 설치한다 (fable R4-6 · PROPOSED · c 정면)

**status:** 🔵 PROPOSED (미실행 · lab full R4 · 사전등록 · toy=DIRECTIONAL 상한) — source=fable R4-6
**lane:** mouth/tension × 학습 신호 (H_9423 공학습 선례의 tension-lane 이식)
**related:** [[H_9423]] · [[H_9576]] · [[H_9628]] · [[H_9630]]

## 한 줄 주장 (반증가능)
decode-time bias 가 의미를 못 나른 것은 모델이 **그 섭동→의미 사상을 배운 적 없기 때문**이다 — z-bucket 을 입력 조건 채널로 공학습(트렁크 입력에 bucket 임베딩 가산·loss 는 plain CE 불변)하면, held-out 문맥에서 bucket 스윕 low→high 가 텍스트 novelty 통계를 단조 이동시킨다.

## 어느 KILL 을 왜 안 밟나
- H_9576: decode-time bias lane 이 아니라 **학습-설치** lane — 죽은 각도의 재생성 아님.
- R3 H_9623(CLMS lesion)/H_9624(curriculum race): 둘 다 **CLMS store** 필연성 검정 — 이 안은 store 무관 **tension 조건 채널** 신설. AGREES(같은 "다리는 학습이 설치한다" 프레임·H_9423 선례 공유) but 무중복.
- `a_train_inline_gauge`: z 라벨은 **입력을 조건화**하지 loss 에 안 들어감 — in-training gauge 금지 비저촉.
- p8: train 과 infer 가 **같은 채널**(train=self-supervised novelty bucket, infer=라이브 PC2→bucket) — split 아님. p5: 게이트는 여전히 BASE 소비(Stage-A 유지)·emit 결정 비접촉.
- cpt-destroys 메모리: 소코퍼스 CPT 위험 → **toy scratch 우선** + 303M 은 base-corpus 혼합 CPT 로만(오너 go 라인).

## engine-native 계기
`anima-py corpus <fmt> --tension-bucket-channel` (창별 novelty 통계 self-supervised 3-bucket 라벨) → `anima-py train --cond-channel tension3` (bucket 임베딩을 트렁크 입력에 가산) → `anima-py evaluate <clm> --cond-sweep low,mid,high` (frozen held-out 문맥에서 bucket 스윕 Δnovelty).

## 통제군 (≥2 + 양성)
- null #1: shuffled-label cotrain (라벨↔창 순열 — 채널 존재 효과 분리).
- null #2: no-channel cotrain (파라미터 매칭 — control-must-match-mediating-covariate).
- **양성통제**: seen-데이터 oracle-bucket 스윕 — 조건화가 최소한 seen 에서 먹는지(이게 죽으면 P1 개봉 금지 = V2_1 규율).

## 사전등록 판정표 (우연 아래 포함)
| 관측 | 판정 |
|---|---|
| held-out cond-sweep 단조 Δnovelty > 양 null 대비 collapse-Δ (2 seed) | **PASS-toy (DIRECTIONAL)** — 303M 이식 후에만 TERMINAL 후보 · infer 에서 라이브 PC2→bucket 배선하면 "의미 나르는 mouth" 최초 실증 |
| seen oracle 조차 무이동 | **KILL** — 조건 채널 자체 미학습 · "학습이 사상을 설치한다" 경로 사망 |
| shuffled-label 도 이동 | **VOID→교란** — 라벨이 아니라 채널 존재 자체의 효과 · 설계 재작업 |
| 역-단조 (high→low novelty · 우연 아래 칸) | **INVALID** — 라벨 부호 결함 · 수리 먼저 |

**검정력**: toy scratch 2 seed × 3 arm; eval 은 frozen held-out 30+ 문맥 × 3 bucket. Δnovelty MDE 는 toy 파일럿 sd 로 사전 산출(음성 판정 전 검정력 규칙).

## 비용 / 죽는 방식
toy = pool GPU 소액 → 303M CPT = **GPU fire (오너 go)**. **죽는 방식**: seen 양성통제부터 무이동이면 이 경로 전체가 죽고, 벽은 "학습으로도 안 설치됨" 으로 격상된다(그게 관측이다).

## 상태
🔵 PROPOSED — toy 우선·DIRECTIONAL 상한 명시. 측정 주장 0(설계).
