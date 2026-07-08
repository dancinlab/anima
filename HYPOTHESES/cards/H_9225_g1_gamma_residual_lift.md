# H_9225 · g1_gamma_residual_lift

🟡 DIRECTIONAL — γ residual-lift 측정 설계 검증 + Fable #8 freeze-then-bolt 함정 교정

## 주장
G1 재조합 벽의 유일 잔여 레버 γ(trained-constructive-bind)를 additive-대조군 잔차의 held-out
interaction-lift로 측정한다. EARNED bind = additive baseline 대비 held-out RMSE lift가 참
결합세기에 비례하고 shuffle(결합-파괴)서 붕괴하는 margin.

## 방법
toy numpy ($0): `y=a[A]+b[B]+s·<u[A],v[B]>` (K=12, rank=3), held-out=30% (A,B)셀 제거(셀 lookup
불가=재조합만). 두 추정량: ① frozen-additive→residual bilinear(Fable #8 문자) ② additive+bilinear
joint-fit. 통제: shuffle B 짝 파괴 = combination-destruction control.
산출 = `state/g1_gamma_divergence/residual_lift_probe.py` · `RESULT.md`.

## 결과 / 판정
- joint-fit: strength=0 lift~0(거짓양성 없음) · strength>0 lift 0.66→1.48→3.11(세기비례=EARNED) ·
  모든 shuffle 행 붕괴~0(THEATER 통제 통과). → **측정 설계 유효**.
- **교정**: Fable #8 문자 그대로(frozen-additive→residual)는 held-out 전부 음수(실패) = confounded
  추정량. additive를 freeze하고 binding 얹으면 죽은 레버와 동일 함정. **joint 공동적합 필수** →
  DPI 진단 강화(γ objective도 additive escape-hatch를 co-opt로 제거해야, freeze-then-bolt 금지).

## 범위 (a_scale_honest_scope)
toy ground-truth 생성자 — 측정 설계 sound + frozen-2단계 confound 증명. 실 303M byte-LM 언어에
비가법 재조합 구조 실재 여부는 미증명 = 결정적 실험(실코퍼스 joint interaction-lift +
engine-native decode) GPU-gated NEXT.

## 계보
부모 = 재조합 벽 프로그램(goal-biolens · substrate-framebreak-g1). Fable 발산 top-1(#8 residual-lift).
관련 = measurement-metalaw(FORM tunable·BIND earned·Δ 신호) · h1816-predcoding-binding(additive서 붕괴).
