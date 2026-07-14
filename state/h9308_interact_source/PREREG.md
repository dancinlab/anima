# PREREG — INTERACT-SOURCE 스크리너 (개입 분포에 bits 가 있는가)

도시에: `state/fable_killshots/w6_메타DPI.out.md` 카드 2 (축소판 킬샷).
가설: 자기 실행 궤적의 (상태, 행동)→후속결과 결합은 정적 코퍼스에 없는 EARNED 정보를 담는다.

## 프리징 (데이터의 *효과* 를 보기 전에 고정)

- **DV (헤드라인)**: `Î(A_t ; Y_t | S_t)` — nats, plugin + Miller–Madow 편향보정.
  - `A_t` = 행동 = emit ∈ {0,1} (EMIT=1 · ACTIVE_VETO=0). 궤적의 유일한 행동 변수
    (gtext 내용은 궤적당 sha 2종 = {고정 발화, 빈 문자열} ⇒ 행동의 *내용* 엔트로피 0).
  - `Y_t` = 후속-문맥-변화 = `1[ ΔC_t ≥ median(ΔC) ]`,
    `ΔC_t = ||C_{t+1} − C_t||_1`, `C = (nov_ctx, rel_ctx, cur_ctx, gap_ctx, allo_ctx, agloop_ctx, scn_ctx)`.
    (행동 자체를 DV 에 담지 않는다 — 장부형 DV 금지.)
  - `S_t` = 상태 = `stage` ∈ {0..4} (PRIMARY). 데몬이 로그하는 상태변수이며 emit 의 드라이버.
  - 조건부라서 "행동은 상태의 함수"라는 동어반복이 제거됨 — 이것이 카드 2 의 설계 취지.
- **등가마진 (TOST)**: ±0.02 nats. **PASS** = TOST(±0.02) FAIL **AND** 95% CI 하한 > 0.
- **arms**: ① REAL ② ACTION-SHUFFLE (S-층 내 A 순열 — 주변분포 보존·결합만 파괴)
  ③ STATE-ONLY (`Î(S;Y)` — Y 채널 liveness) ④ PEDESTAL (참값 0: A 를 p̂(A|S) 에서 독립 재추출 ⇒ Y 로의 인과경로 0)
  ⑤ ALIVE 양성대조 (합성: A 에 잔여 엔트로피 주입 + Y=f(A,S) 로 **참값 기지**).
  난수 = numpy PCG64 (arm 별 독립 스트림 · LCG 금지).
- **추론**: block bootstrap(L=50, B=2000) 90%/95% CI · within-stratum permutation null(B=2000) p값 ·
  블록(100 tick) paired-t 로 REAL−PEDESTAL. **max(controls) 순서통계량 금지.**
- **V-게이트 (하나라도 실패 → INVALID 또는 NOT-POWERED, PASS/FAIL 아님)**:
  - **V-CEILING**: `H(A|S) > 등가마진(0.02 nats)`. 실패 ⇒ DV 의 정보천장이 마진보다 낮음 ⇒ **NOT-POWERED**
    (어떤 n 으로도 PASS 불가). MI ≤ H(A|S) 는 항등부등식이므로 이 게이트가 검정력의 1차 관문이다.
  - **V-ALIVE**: 양성대조가 기지 참값을 ±25% 내로 회수.
  - **V-PEDESTAL**: 참값 0 arm 이 |MI| ≤ 3×bootstrap sd.
- **N_REQ**: ALIVE 생성기로 참값 = 0.02 nats(마진) 인 합성궤적을 만들어 n 그리드에서 검정력 80% 되는 최소 n 을
  시뮬레이션으로 산출 (데이터 효과를 보기 전에).

## 사전 계측 (데이터 구조 — 효과 아님)

n(tracked, worktree) = 900×3 (h9269 pod_harvest B/C/D · `stage_cycle:true`) + 608 + 97 (h1058) = **2,705 tick**.
`(stage, emit)` 교차표가 **결정적**: stage∈{0,1,4}→EMIT 전부, stage∈{2,3}→ACTIVE_VETO 전부 (900/900, 3 궤적 모두;
h1058 도 동일 규칙). ⇒ `H(A|S=stage) = 0` 이 예상되며, 그렇다면 V-CEILING 실패 ⇒ 판정은 NOT-POWERED.
이 사실은 **효과 추정 전** 에 확정하며, 사후에 조건집합에서 stage 를 빼서 MI 를 만들어내는 것은 tune-to-green 이므로 금지한다.
(S-lite = tercile(idle) 조건부는 **SECONDARY DIAGNOSTIC** 로만 보고 — stage 매개 교란이라 PASS 경로가 될 수 없다.)
