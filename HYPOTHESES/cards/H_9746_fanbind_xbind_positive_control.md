# H_9746 — R2c fan-bind 양성통제: XBIND(H_9267) 을 계기로 재서 dynamic range 확정

**status:** 🟢 POSITIVE-CONTROL PASS (계기 dynamic-range 정상 · R2 레버무효 최종확정 · A100 pod · 2026-07-17) · 선행 [[H_9693]]·[[H_9694]]
**lane:** G6/ρ·fan · 계기 양성통제 **related:** [[H_9694]] · [[xbind-g1-crack-measure-not-substrate]] · [[positive-control-before-reading-a-negative]]

## 물음
H_9694 의 🧱 은 계기결함(BIND 실재하나 fan-bind 맹점)과 레버무효(짝-유지 co-train 이 composition 미형성)를 **못 가른다** — 양성통제 부재. [[H_9267]] XBIND 합성 코퍼스는 held-out D-acc **1.000**(양 seed · G1 CRACK 확증)로 **bind 가 기지-양성**인 유일 조건. 이걸 `--fan-bind` 로 재면 계기의 **dynamic range** 가 확정된다.

## 조작 (engine-native)
H_9267 XBIND corpus 로 co-train 한 ckpt(또는 그 계열)를 `anima-py evaluate --fan-bind` 로 채점. bind-positive 조건에서 fan-bind bind_delta 가 **높게** 나오는지 확인. bind-negative 대조(XBIND shuffle)도 병행.

## 게이트 (사전등록)
- 양성통제 PASS: XBIND(bind 기지-양성)에서 fan-bind bind_delta 가 [[H_9745]] paired-null p95 를 **명확히** 초과.
- 이후 R2 targeted 귀속: 양성통제 PASS ∧ R2 targeted 충분검정력서 0등가 → **레버무효**. 양성통제 FAIL(XBIND 도 낮음) → **계기결함**(fan-bind 이 실 bind 를 못 봄).

## kill-list 회피
#6 무관(양성통제는 bind 기지-양성). 계기 dynamic-range 측정이지 레버 아님.

## 최대위험
XBIND 는 G1(재조합) 축 합성이라 G6(ideation) fan-bind frame 과 도메인 불일치 가능 — fan-bind frame 에 맞는 bind-positive 합성이 별도 필요할 수 있음(그 경우 H_9267 직접 재사용 대신 fan-bind-호환 XBIND 변형 설계).

## falsify
🟢 XBIND fan-bind bind_delta ≫ paired-null = 계기 dynamic-range 정상 → R2 🧱 은 레버무효로 확정가능. | 🧱 XBIND 도 fan-bind 서 낮음 = 계기결함 = R2 🧱 무효(계기가 bind 를 못 봄).

## 양성통제 결과 (2026-07-17 · A100 pod · bindpos + STEP-0 census)

lab full(Fable 코드검증) 설계 → `corpus g6bind --arm bindpos`(BIND=인접쌍→cA+cB·NULL=거리2쌍→cA-echo·J self-witness) 303M co-train → `--fan-bind --fan-smp 48`:

| arm | composed J | shuffled J | ablated | bind_delta | McNemar p | Tango CI | PAIRED |
|---|---|---|---|---|---|---|---|
| **bindpos**(양성통제) | 0.2083 | 0.0069 | 0.0000 | **+0.2014** | **0.0000** | [+0.164,+0.244] | **🟢 BIND-SENSITIVE** |

**★ 양성통제 PASS 결정적**: bind 기지-양성 모델이 fan-bind 서 bind_delta=0.20·McNemar p<0.0001·powered(m=60) → **계기 dynamic-range 정상**. ablated J=0.0000=완벽한 zero-truth pedestal · shuffled J=0.0069(NULL 클래스 cB 억제 성공=조건부 설계 작동).

**★ STEP-0 census (F2 truncation 검증)**: R2 targeted(seed7) --fan-dump 864 emissions census → composed **A-only 28%·both 5%·neither 36%** = A-only<50% ⟹ **truncation 이 지배적 아님 = R2 BIND-ABSENT 판독가능**(Fable F2 교란 배제). (STEP-0 재현 bind_delta=−0.0035 = seed7 일치.)

**★ R2/[[H_9694]] 귀속 완성**: 양성통제 PASS(계기가 0.20 잡음) ∧ targeted 2-seed BIND-ABSENT(−0.0035·−0.0139) ⟹ **R2 의 BIND-ABSENT 는 계기결함 아니라 레버무효 = 최종 확정.** 데이터-포맷 레버(g6bind targeted co-train)가 composition-sensitivity 를 안 심음 — 있었다면 계기가 잡았을 것. 0.444(hexa 비동결) 인공물 확정. **R2 캠페인 완전 종결.**

## source
H_9694 lab full reconcile · Fable+Sol 둘 다 positive control 을 계기결함/레버무효 판별 유일수단으로 지목.
