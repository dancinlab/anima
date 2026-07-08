# H_9255 · g1_joint_interaction_corpus

🟡 DIRECTIONAL (instrument 단계) — 실 corpus joint interaction-lift (engine-native 303M · 오너 GO)

## 주장
실 anima 4-cell byte 언어에 additive(α_A+β_B)로 설명 안 되는 저-rank 비가법 (A,B) 상호작용이
303M engine-native 표면(logits/NLL)으로 검출되는가. residual-lift(H_9225)의 실데이터 판. census
(g1-census-objfloor CONFIRMED-TERMINAL) 재확인 or 재오픈 트리거 — 새 GREEN 사냥 아님.

## 방법 (Fable 설계 · state/g1_joint_interaction_corpus/DESIGN_FABLE.md)
probe=`cli/evaluate.py --interaction-lift`(--system-g1 선례)→`core/decode.py _fwd_logits(T=64)` per-pos NLL+logit.
축 AX1 content-pair·AX2 topic×register·AX3 verb-object + PC-P/PC-N 대조. 셀단위 홀드아웃20%(seed=7)+격리.
joint-fit additive vs +bilinear ALS, lift=(RMSE_add−RMSE_joint)/RMSE_add, Freedman-Lane 200perm 통제.
비용=$0 summer CPU(cheap 10분+full 2–4h), aiden 제외(OOM)·mini 금지(rc=137).

## PC-P instrument 발견 (model-free · pcp_probe.py)
한국어 조사 allomorph(받침×슬롯)로 검출력 검증 → lift≈0(FAIL). 구조는 실재(joint 표 명확)하나
6셀 near-1:1이라 main-effect logit이 이미 라우팅 → 조사=compositional(additive-generalizable)지
non-additive 양성대조 아님. **corpus verdict 아님=측정 instrument 결함**(infra-wall-noneval 격리).
⟹ PC-P 재설계 필요(진짜 scalar non-additive 대조·다-레벨 held-out·additive-in-y baseline 고정).

## 상태
engine-native full = valid PC-P gate 통과 후 발사(오너 spend-go). 부모=gate-g1-recomb-gamma-divergence ·
형제 H_9225(residual-lift). 지배원리=additive를 primary서 necessitate(offer 아님).

## engine-native FULL verdict (TERMINAL-eligible · a_eval_py_canonical)
303M en-general 552 content-pair 셀(cli/evaluate.py --interaction-lift #3186, summer $0):
held-out additive RMSE 0.290 vs joint(+bilinear) 0.523, **lift=-0.801 < Freedman-Lane null95 -0.444
= NO non-additive signal (ADDITIVE-EXPLAINED)**. 모델 NLL surface가 content-pair에 완전 additive
(main-effect 합, bilinear=overfit) = 출력에서 비가법 결합 안 함 = additive floor. Fable Y1=비가법 무 →
g1-census-objfloor(재조합 능력천장) 데이터측 engine-native 재확인(값진 negative). ckpt-corpus 언어매칭
필수(convergence evaluate-py-1). 산출=state/g1_joint_interaction_corpus/RESULT_ILIFT.md. census 재오픈 아님.
