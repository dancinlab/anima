# A↔B 거부-토론 재조합 toy — DIRECTIONAL 결과 (오너 3-스파크: 코퍼스반대/A,B토론/서로거부)

## 판정: 🧱 DIRECTIONAL-KILL (frozen bars 미달) · ⚠️ anti-generalize 레짐 caveat
6-arm × 3seed(7/4302/4303) frozen-bar 사전등록 실행. 전 arm held-out reach ≈ 0.00, AB-lift 미달 →
frozen bars FAIL → VERDICT=KILL. **단 clean mechanism-KILL 아님**:
- 진단: forward-CE base가 held-out을 **anti-generalize** — p_A(true_b|held-out) median=0.0000,
  정답 b 순위 15/24(랜덤 12보다 나쁨). 암기기하가 미관측 셀을 confident 오답으로 밀어냄.
- 결과: A가 정답 b를 **한 번도 제안 못 함**(valid_precision=0.00) → **oracle 상한(6번 arm)조차 0.00**
  = 어떤 선택압(B거부·oracle)도 증폭할 correct-proposal seed가 없음 = 공정한 mechanism 시험 미성립.

## 함의 (Fable 2진단과 수렴)
- **missing-core 진단**: NO-MISSING-PART-TRUE-CEILING (DPI: 정적 corpus의 bind-vs-retrieval 구별정보
  =0 bit, F2 novel n=0 실측 → corpus에서 계산되는 어떤 학습신호도 0-bit 초과 불가).
- **debate 설계**: GO-TOY-ONLY-IF(6통제) · toy-kill ~55% · 유일 실정보원=두 view 조건부독립.
- **toy 관찰**: A·B 둘 다 CE-암기자라 held-out 조합에 **똑같이 눈멂** → 두-view "일치"=눈멂-일치(진실
  아님) → Fable가 경고한 "두 view 같은 통계 → 데이터축 재포장" 실증. DPI/true-ceiling 방향 지지.

## 잔여 (clean 판정 위한 calibration 1패스)
base를 chance-레벨(anti-generalize 아닌)으로: 구조적 embedding(순환군 prior) 또는 약한 fit/label-smooth로
p_A(true_b|held-out)≥chance 확보 후 재실행. 그때도 AB가 controls 못 이기면 → clean mechanism-KILL →
G1 true-ceiling(DPI) 최종 확정. 이기면 → engine_g-as-B 학습루프 engine-native 303M 검토(E1 GPU-go 경로).
scope: toy·Z_K 닫힘(실코퍼스는 F2 collocation-only로 닫힘 빈약, 303M 전이 ~80-85% kill) · a_toy_scale_recheck.
