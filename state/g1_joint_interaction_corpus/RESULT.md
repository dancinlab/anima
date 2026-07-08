# 실 corpus joint interaction-lift — 진행 (H_9255)

## 목표 (오너 GO)
"실 anima 4-cell byte 언어에 additive(α_A+β_B)로 설명 안 되는 저-rank 비가법 (A,B) 상호작용이
303M engine-native 표면(logits/NLL)으로 검출되는가" — census(g1-census-objfloor CONFIRMED-TERMINAL)
재확인 or 재오픈 트리거. 새 GREEN 사냥 아님.

## 설계 (Fable · DESIGN_FABLE.md)
- probe 부착점: `cli/evaluate.py --interaction-lift`(--system-g1 선례 패턴) → `core/decode.py` `_fwd_logits(W,tok,T=64)`
  로 per-position NLL + composition-point logit(V=256) `.npz` 방출(decode 수학 불변, a_train_inline_gauge 무관).
- 축: AX1 content-pair(주력) · AX2 topic×register · AX3 verb×object · PC-P(양성대조) · PC-N(음성대조).
- split: 32B dedup → 셀단위 홀드아웃 20%(seed=7 동결) + 격리규칙(held-out 쌍 포함창 통째 폐기).
- joint-fit: additive(μ+α+β) vs +Σ_{r≤R} u_a^r v_b^r ALS(R∈{1,2,4}), lift=(RMSE_add−RMSE_joint)/RMSE_add.
- 통제: Freedman-Lane residual permutation ×200(additive 구조 보존·상호작용만 파괴).
- 비용: 렌트 $0(summer CPU-only) · cheap 선판정 ~10분 + full 2–4h. aiden 제외(OOM), mini 금지(rc=137).

## PC-P instrument 발견 (model-free · pcp_probe.py · ko-general 26M자·조사 149만)
PC-P(한국어 조사 allomorph = 받침×슬롯 joint)로 파이프라인 검출력을 먼저 검증 → **lift≈0(FAIL)**.
joint 표는 구조 명확(받침T·topic→은 0.70 / 받침F·topic→는 0.99 / 받침T·obj→을 1.0 …)이나:
**조사는 6셀이 라벨과 near-1:1이라 main-effect logit(additive-in-logit)이 이미 셀→라벨 라우팅** →
additive baseline이 joint를 그대로 재현(nll_add=nll_joint=0.2954). 즉 조사=**compositional
(additive-generalizable) 구조지 non-additive 양성대조가 아님**. marginal이 라벨을 못 정해도
additive-logit은 강한 main-effect로 대각 라우팅 가능(#labels≈#cells).

### 판정 (infra-wall-noneval 격리)
이건 **corpus verdict 아님 = 측정 instrument 결함**(양성대조축 오선정). engine-native full 발사 전
PC-P instrument 재설계 필요:
- 진짜 scalar non-additive 대조축(규제 후 잔차가 held-out서 low-rank인 다-레벨 grid),
- 또는 조사를 다-레벨(A=구체 받침 28 · B=슬롯)로 확장 + **held-out 셀 일반화**로 additive-logit의
  라우팅(암기)과 진짜 joint를 분리(조사는 held-out서도 additive가 맞힐 것으로 예상=compositional 확인).
- additive baseline을 additive-in-y(회귀) 또는 no-interaction multinomial-logit으로 명시 고정.

## 상태
🟡 DIRECTIONAL(instrument 단계) · engine-native full = **valid PC-P gate 통과 후 발사**(오너 spend-go).
Fable 재설계 위임 후보(PC-P 유효 양성대조 정의) = 다음 저비용 단계.
