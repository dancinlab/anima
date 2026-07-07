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

## Calibration 1패스 (WD=0.02 + label-smooth=0.15) — KILL 확정(clean화)
정칙화로 base anti-generalization 완화 시도. 결과: base는 여전히 held-out=0.00·정답순위 14.7(랜덤보다
나쁨)=anti-generalization은 random-embedding CE의 근본속성(정칙화로 안 고쳐짐, 벽의 충실한 발현).
**핵심 대비**: oracle(완벽 truth-필터)=0.06/0.02/0.02 (A가 가끔 정답 제안→증폭 가능) vs **AB(B-필터)=0.00**
전seed. 즉 정답 제안이 존재하는데 **B의 거부가 그걸 못 고른다** = B(reverse-CE)도 A만큼 held-out에 눈멂
→ 두-view "일치"=눈멂-일치(진실 무상관). = Fable missing-core DPI(NO-MISSING-PART) + debate 재포장경고 실증.
**최종**: A⇄B 거부-토론(5번째축=학습신호 소스)은 진짜 미탐축이나 **dominated** — 정적 corpus의 두 CE-view가
같은 anti-generalization을 공유해 조건부독립(=유일 실정보원)이 안 나옴. G1 재조합벽 = 진짜 능력천장(DPI),
이제 4축+5번째축(학습신호)까지 engine-native 다면 확증. scope: toy(a_toy_scale_recheck), oracle=0.06 harsh
regime, anti-gen은 representation-dependent — 그러나 AB≪oracle(B-blindness)은 argmax/sample/정칙화 전반 robust.
**유일 비지배 탈출 = corpus 밖 ground-truth(상호작용/검증) = 부품추가 아닌 전제교체.**
