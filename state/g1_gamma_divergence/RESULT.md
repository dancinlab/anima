# γ residual-lift probe — 결과 (H_9225 · 🟡 DIRECTIONAL)

## 배경
Fable 발산(고갈: 19 family → 6 클러스터, `FABLE_DIVERGENCE.md`)의 top-1 저비용 결정 probe.
DPI 메타진단: 죽은 G1 레버 전부 "primary loss가 additive-solvable로 남아 binding aux가
trivial 만족(FORM)". γ = additive를 대조군으로 문자 그대로 세우고, **잔차(residual)** 에
held-out 재조합 신호가 있는지 + shuffle로 THEATER 아님을 증명.

## 셋업 (toy · numpy · $0)
- 생성자: `y = a[A] + b[B] + s·<u[A],v[B]>` (K=12 concept, 참 interaction rank=3).
- held-out = 전체 (A,B) 셀의 30%를 train서 제거 → **셀 lookup 불가, 구조 일반화로만 채점**(=재조합).
- 두 추정량 비교: ① frozen-additive→residual bilinear(Fable #8 문자 그대로) ② additive+bilinear **joint-fit**.
- 판정 = held-out RMSE lift(additive 대비) · shuffle(B 짝 파괴) = 결합-파괴 통제.

## 결과
```
 strength  shuffle  add_rmse  2stage_lift  joint_lift  verdict(joint)
      0.0    False     0.153       -0.022      -0.138  POS-CTRL (~0 ✓)
      0.0     True     1.117        0.019       0.011  THEATER-CTRL (collapse ✓)
      0.5    False     0.828       -0.810       0.664  EARNED BIND
      0.5     True     1.364        0.037       0.040  THEATER-CTRL (collapse ✓)
      1.0    False     1.641       -1.417       1.477  EARNED BIND
      1.0     True     1.817        0.067       0.067  THEATER-CTRL (collapse ✓)
      2.0    False     3.277       -2.652       3.113  EARNED BIND
      2.0     True     2.944        0.079       0.075  THEATER-CTRL (collapse ✓)
```

## 판정 (🟡 DIRECTIONAL)
1. **측정 설계 검증됨**: joint-fit이 참 interaction 세기에 비례(0.66→1.48→3.11) held-out lift를
   내고, 모든 shuffle 행에서 ~0으로 붕괴(THEATER 통제 통과), strength=0서 거짓양성 없음.
   → residual/interaction-lift는 EARNED bind를 additive와 게임불가하게 가르는 유효 probe.
2. **설계 교정(핵심)**: Fable #8을 **문자 그대로(frozen-additive→residual)** 구현하면 held-out에서
   전부 음수(−0.8~−2.7) = **실패**. 원인 = frozen additive baseline이 held-out 셀서 편향(train서
   행/열 효과가 interaction에 오염). **additive와 bilinear는 반드시 JOINT 공동적합**해야 신호 복원.
   → DPI 진단의 강화: additive를 먼저 고정(freeze)하고 binding을 얹는 순간 죽은 레버와 같은 함정.
   γ objective도 **additive escape-hatch를 co-optimization으로 없애야**(freeze-then-bolt 금지).

## 범위 정직 (a_scale_honest_scope)
toy·ground-truth low-rank 생성자. 증명한 것 = (a) 참 interaction이 low-rank면 joint combiner가
held-out서 복원 + shuffle 붕괴(측정 설계 sound), (b) frozen-additive 2단계는 confounded 추정량.
**증명 안 한 것** = 실 303M byte-LM 언어에 복원 가능한 비가법 재조합 구조가 실재하는가.
→ 그게 결정적 실험 = 실코퍼스(anima 4-cell)에서 joint interaction-lift + engine-native decode = GPU-gated NEXT.

## NEXT (GPU-gated · explicit go 대기)
- 실 corpus polysemy-necessity(Fable #5) + joint interaction-lift로 실데이터 방향 판정 → 초록이면
  bilinear-generator(#3)·unbind-crosstalk(#6)로 상승, held-out 잔차 신호 0이면 **γ 포함 재조합 벽
  전체가 303M byte-LM 능력천장으로 종결**(값진 negative).
