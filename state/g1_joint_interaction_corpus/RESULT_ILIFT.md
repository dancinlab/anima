# 실 corpus engine-native joint interaction-lift — 최종 결과 (H_9255 · TERMINAL-eligible)

## 측정 (engine-native 303M · a_eval_py_canonical)
`anima evaluate --py <ckpt> --interaction-lift`(cli/evaluate.py, read-only NLL surface, #3186/#3188)로
303M anima ckpt(e1_slw_303m, 영어)의 en-general content-pair (A,B) 셀별 continuation NLL을 측정 →
offline joint-fit(`interaction_lift_fit.py`: additive main-effect vs +low-rank bilinear ALS,
held-out 20% 셀, Freedman-Lane residual permutation ×200 null).
- ckpt-corpus 매칭 확인: e1_slw_303m 자연-window NLL = ko 6.66(OOD)·en 2.92(정상) → **영어로 측정**
  (verdict-integrity: ko 측정 시 >uniform garbage였을 것, ckpt 학습언어 매칭 필수 · convergence evaluate-py-1).
- summer CPU $0 · 7578 window · 552 셀(24×24 content-word grid) · ~4h detached.

## 결과 (full · 552 셀)
```
grid 24x24 · 552 observed cells
held-out: additive RMSE=0.290 · joint(+bilinear) RMSE=0.523 · lift=-0.801
Freedman-Lane null: lift95=-0.444 (mean -2.967)
VERDICT: lift=-0.801 < null95=-0.444 → NO non-additive signal (ADDITIVE-EXPLAINED)
```
(200-window preview도 동일 방향: lift 0.004 < null95 0.017 = additive-explained.)

## 판정 (Y1 · 값진 negative)
**303M 모델의 NLL surface는 content-pair (A,B)에 대해 완전히 additive** — 각 단어의 고유 기여
(main effect)의 합으로 설명되고, bilinear (A×B) 상호작용 항은 held-out에서 overfit만(음수 lift가
null보다도 아래 = 실데이터가 shuffle보다 더 overfit = 저-rank 비가법 구조 전무). 즉 **모델이 두
개념을 출력에서 비가법으로 결합(constructive bind)하지 않음** — 출력 표면 자체가 additive floor.

Fable 해석 매트릭스의 **Y1(엔진표면)=비가법 무**. G1 census(g1-census-objfloor CONFIRMED-TERMINAL,
"G1 재조합=303M byte-LM 능력천장/additive floor")를 **독립 데이터-측 engine-native 렌즈로 재확인** —
census가 재조합 task로 본 additive floor가 모델의 실코퍼스 출력 NLL surface에서도 그대로 나타남.

## 범위 정직 (a_scale_honest_scope)
- 측정축 = AX1 content-pair × next-continuation NLL(≤64B 창). "재조합"의 한 engine-native 조작화지
  유일 정의 아님. 이 축·이 ckpt(영어)·이 corpus에서 additive.
- Y3(언어 자체의 비가법 구조 실재 여부)는 model-free로 별도 측정 필요(PC-P2 XOR crossover는 실재
  확인했으나 power-limited). Y1=additive는 census 방향과 일치하나, "언어에 신호가 있는데 모델이 못
  담나(재검토) vs 언어에도 없나(천장 재확인)"의 완전 분해는 Y3 대형코퍼스 인증 후.
- census 재오픈 아님 — CONFIRMED-TERMINAL 유지·데이터측 재확인.

## 산출
`en_ax1_full_nll.json`(NLL surface) · `ilift_fit_result.json`(fit verdict) · `interaction_lift_fit.py`
(분석기) · `en_ax1_manifest_meta.json` · 도구=cli/evaluate.py --interaction-lift(#3186).
