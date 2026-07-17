# H_9694 — R2 ⭐ kill#6 잔해 회수: targeted co-train 의 bind Δ 를 frozen 계기로 재획득

**status:** 🧱 DECISION-KILL · ⚠️ MECHANISM-INCONCLUSIVE (303M engine-native · runpod A100 · frozen --fan-bind · lab full reconcile · 2026-07-17) · 1-seed · wired: 계기 배선완료(#3915·#3983)
**lane:** G6/ρ·fan · 데이터 레버 **related:** [[H_9693]] · [[H_9124]] (데이터축 선례) · [[H_9576]] (n=58 부호반전 전례)

## 물음

convergence `g6-ideation-hexa-1` 은 **"TARGETED 가 FALS 를 위조한다"를 죽였지, "TARGETED 가 bind 를 못 움직인다"를 죽인 게 아니다.** 오히려 정반대를 관측했다 — **Δbind 0.444(TARGETED) vs 0.000(SHUF)**. 즉 **데이터 레버가 BIND 를 움직인다는 관측이 이미 존재하는데, 당시 계기가 비동결·비엔진네이티브라 verdict 자격이 없었을 뿐.** 새 능력 주장 0 = "이미 본 신호를 합법으로 벌기" ⟹ 서열 1위(A0 계기 다음).

## 조작 (engine-native)

`anima-py corpus g6bind --out c.txt --lang en --arm {targeted,shuf} --seed S` (corpus.py 서브커맨드 추가 · **동일 seed 2-arm content-matched** · shuf=주제결합 파괴·동일 바이트) → `anima-py train --corpus … --init base.clm` → `anima-py evaluate out.clm --fan-bind` + 기본 G0-G6 병행.

## 게이트 (사전등록)

- **PRIMARY**: bind Δ(TARGETED) − bind Δ(SHUF-trained) **> 0** ∧ permutation null 95% 밖(n≥96 방출 · [[H_9693]] C 설계).
- **게이트**: G0 kwr **5/5 유지**(CPT 파괴 감시 · [[cpt-destroys-what-corpus-omits]] — CPT 는 코퍼스에 없는 능력을 죽인다).
- **fals 는 secondary·wired 표면으로만 보고** (PRIMARY 로 쓰면 kill#6 위조).
- 아래-우연 칸 포함(Δ<0 = anti-bind · 해석 사전등록).
- **발사 전 검정력 계산 필수**([[power-before-negative-verdict]]).

## kill-list 회피

**#6 정면수용** — 주장이 "fals 통과"가 아니라 "**bind Δ > SHUF-trained**"이고 SHUF-trained 팔이 사전등록 1급 통제군. #1 무관(하네스 없음) · #5 무관(gen=40).

## 최대위험

**0.444 가 hexa 시절 비동결 프로브의 인공물일 가능성** — 당시 n·검정력 미상. [[H_9576]] 이 정확히 이렇게 뒤집혔다(n=58 ρ=+0.110 → n=270 ρ=−0.077 부호반전). ⟹ 검정력 먼저.

## falsify

🟢 CRACK: bind Δ 차이 > null 95% ∧ G0 5/5 유지 ∧ 2-seed. | 🧱 KILL: Δ 차이 TOST 0 등가 = 데이터 레버가 BIND 못 움직임(0.444 는 인공물). | ⚠️ G0 붕괴 = CPT 파괴 = 측정 무효.

## 🧱 verdict — DECISION-KILL · MECHANISM-INCONCLUSIVE (2026-07-17 · runpod A100 · frozen --fan-bind · lab full reconcile)

| arm (6000step co-train · val_CE DESCENT 1/1) | composed J | shuffled J | **bind_delta** | mismatched-null p95 |
|---|---|---|---|---|
| base (BEFORE) | 0.0000 | 0.0000 | 0.0000 | — |
| **targeted** (짝유지 fp=4000) | 0.0208 (2/96) | 0.0104 (1/96) | **0.0104 (1/96)** | 0.0521 (5/96) |
| **shuf** (짝파괴 fp=0) | 0.0521 (5/96) | 0.0521 | **0.0000** | 0.0833 (8/96) |

**사전등록 PRIMARY 미달 = CRACK 아님**: `composed J(targeted) > mismatched-null p95` → 0.0208 < 0.0521 ❌ (절1 targeted−shuf=+0.0104>0 은 통과). 엔진 `--fan-bind` 도 양 arm `🧱 NO-BIND` 판정. **decision-level 🧱**.

**그러나 "0.444 인공물 / 레버 무효"는 미획득 (mechanism-INCONCLUSIVE)** — lab full(Fable∥Sol) 압박검증 수렴:
- **절2(`composed J > marginal null`)는 composition 이 아니라 emission 을 잰다** — 짝 전파괴한 shuf arm 이 composed J **최고값**(0.0521)이다(kill#6 재발: FORM 게이트의 다른 얼굴). composition 을 격리하는 유일 지표는 **bind_delta**(paired 차분): targeted +0.0104(유일)·shuf 0(방출 최고인데도 차분 0) = emission 과 decouple.
- **계기 결함**: `--fan-bind` 의 null 은 composed 방출을 **다른 프레임 짝에 채점한 marginal J** 분포(code 확인 `cli/evaluate.py:eval_fan_bind`). bind_delta(paired 차분)는 **자기 null pedestal 이 없다** ⟹ `chance-level-must-be-derived-per-metric` 위반. 올바른 통계량 = 이중차분 D=(Jc−Js)_tgt−(Jc−Js)_shuf 의 paired 순열 null + CI = **미계산**.
- **검정력**: bind_delta 0.0104 = **1건/96** 차이. "composition-sensitivity 를 심었다"는 근거가 표본 한 건. 사전등록 🧱 은 "0.444 TOST 0등가"를 요구하는데 등가한계·TOST 미계산 ⟹ **"0.444 인공물" 미증명**. default 🧱-attribution = tune-to-negative.
- **positive control 부재**: 0.444(hexa 비동결·다른 스케일)의 non-recovery 는 어느 쪽 증거도 아님. 계기결함 vs 레버무효는 **양성통제(H_9267 XBIND D-acc 1.000 을 fan-bind 로) 없이 미귀속**.

**dissent(Fable, 1줄)**: Fable=⚠️ UNDECIDABLE(KILL 로직이 paired 를 marginal null 로 잰 범주오류) · Sol=🧱 decision-level·inconclusive-mechanism. reconcile: code 확인 결과 절2는 사전등록대로 composed-J-absolute vs marginal-null 이라 **letter 상 CRACK 미달=decision 🧱 채택**, Fable 의 범주오류 지적은 **계기 정렬결함**으로 후속(H_9745)에 반영.

**통제 견고**: 두 arm frame_sha=98c48115ca37·claim_sha=e2ac497aa442 **동일** · targeted fp=4000/shuf fp=0. **측정 유효**: val_CE DESCENT(CPT 파괴 아님·⚠️칸 배제).
**scope**: 1-seed(7)·합성 g6bind·303M py303_full. **재현**: `anima-py corpus g6bind --lang en --arm {targeted,shuf} --n-blocks 4000 --seed 7` → `train --init py303_full.clm --steps 6000 --seed 7` → `evaluate --fan-bind --fan-smp 16`.

**후속 (both models · $0~저비용)**: [[H_9745]] fan-bind 에 bind_delta paired 순열 null + prereg TOST(계기↔주장 정렬·`instrument-claim-alignment-before-reading-a-bar`) · [[H_9746]] XBIND(H_9267) 양성통제를 fan-bind 로 = dynamic-range 확정 → 계기결함/레버무효 귀속.

## source
lab full Fable A1 · 선행 [[H_9693]].
