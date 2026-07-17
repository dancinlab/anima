# H_9694 — R2 ⭐ kill#6 잔해 회수: targeted co-train 의 bind Δ 를 frozen 계기로 재획득

**status:** 🔵 PRE-REG (lab full · Fable A1 = 최고 성공확률 각도) · not-terminal · wired: 미배선 (선행 [[H_9693]] 필수)
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

## source
lab full Fable A1 · 선행 [[H_9693]].
