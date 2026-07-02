# G1-BS-N14 activation-patching 진단 — RESULT (2026-07-02, brainstorm 최우선 단일실험) — NO BINDING SUBSPACE

**TIER: 🧱 NO LOCALIZED BINDING SUBSPACE (DIRECTIONAL).** torch toy, aiden GPU $0. H_6177 N14 = "결합-부분공간
존재여부 진단→없으면 trunk-objective-floor 기계적 종결".

## Setup (3종 세트)
소형 byte-GPT(d256 4L, 9000step) structured corpus 학습. held-out 쌍: clean="if A,then B:" vs corrupt="if A',then B:".
A-토큰 residual(embedding) activation 을 clean→corrupt patch → A operand 복구되나. oracle=seen-sanity, 지표=mediation
Δ(A-recall patch−corrupt), control=random-position patch.

## Result
- seen-sanity operand-both = **8/8** (모델이 seen 바인딩 학습 = 진단 유효, undertrain 아님)
- mediation Δ (A-활성 patch):    [0,1,0,1,0] mean **0.40**
- control  Δ (random-pos patch): [0,1,0,0,1] mean **0.40**
→ A 활성을 특정 patch해도 A operand 복구가 random-position patch와 **동일(0.40=0.40)** = A-특이 국소 효과 없음.

## 판독
국소화된 결합-부분공간이 존재하지 않는다 — 처치(regularize)할 바인딩 표현 자체가 없음. = G1 trunk-objective-floor 의
**기계적 종결증거**(H_6177 N14 분기: 부재→종결). ⚠️caveat(verdict-integrity): mediation=control=0.40>0 이라 "patch 무효"가
아니라 "A-특이 효과 = 무작위 효과"; 지표가 A-국소성을 완벽 분리 못하는 한계일 수 있어 DIRECTIONAL. 그래도 A-활성이
특별히 A를 복구하지 않음은 명확 → N1/N11(fast-weight/bilevel) 같은 국소-바인딩 처치의 전제(존재하는 부분공간)가 없음을 시사.

## 함의
frame-break(H_6175, 결합을 mouth 밖 symbolic anchor로) 이 국소-바인딩 부재를 우회하는 유일 경로로 부각 — 국소
부분공간이 없으니 trunk 내부를 고치는 ①②④축보다 ⑤(anchor 외재화)가 정합. follow-on: A-국소성 지표 정제(head-level
patching) 로 caveat 해소 + frame-break 생성경로 대비 재측정(H_6175 follow-on).

## Provenance
n14_actpatch.py, n14_result.json. torch, aiden RTX5070, $0. DIRECTIONAL.
