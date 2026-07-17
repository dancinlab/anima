# H_9746 — R2c fan-bind 양성통제: XBIND(H_9267) 을 계기로 재서 dynamic range 확정

**status:** 🔵 PROPOSED (H_9694 reconcile 후속 · lab full Fable+Sol 수렴 · 양성통제) · not-terminal · 선행 [[H_9693]]·[[H_9694]]
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

## source
H_9694 lab full reconcile · Fable+Sol 둘 다 positive control 을 계기결함/레버무효 판별 유일수단으로 지목.
