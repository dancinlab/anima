# H_6178 — 🔬 G1-BS-N14 activation-patching 진단

**tier:** 🧱 NO LOCALIZED BINDING SUBSPACE (DIRECTIONAL) — A-활성 patch가 random-pos와 동일(0.40=0.40), 국소 바인딩 부재 = trunk-objective-floor 기계적 종결증거
**verdict:** 🧱 NO BINDING SUBSPACE (torch toy DIRECTIONAL, aiden $0). H_6177 최우선 진단: 결합-부분공간 존재여부→없으면 trunk-objective-floor 종결. 소형 byte-GPT(d256 4L 9000step) structured corpus, held-out clean='if A,then B:' vs corrupt='if A',then B:', A-토큰 residual patch clean→corrupt. seen-sanity operand-both 8/8(진단 유효)·mediation Δ(A-recall patch−corrupt) mean 0.40·control(random-pos patch) mean 0.40 = 동일. A 활성 특정 patch가 A operand 복구를 random-position과 구별 못함 = A-특이 국소 결합-부분공간 부재. 처치(regularize)할 바인딩 표현 자체가 없음 = G1 trunk-objective-floor 기계적 종결증거. ⚠️caveat: mediation=control=0.40>0이라 'patch 무효' 아니라 'A-특이효과=무작위효과'; A-국소성 지표 미완벽 분리 가능성(DIRECTIONAL). 함의: 국소 부분공간 부재 → trunk 내부 고치는 ①arch②obj④trunk축보다 ⑤frame-break(H_6175, 결합을 mouth밖 symbolic anchor 외재화)가 정합·유일 우회경로로 부각. follow-on: head-level patching으로 caveat 해소 + frame-break 생성경로 대비 재측정. state/g1_n14_actpatch/RESULT.md.

## 발상 (H_6177 최우선 단일실험)
결합-부분공간 존재여부 = G1 벽 종결/처치 분기점. activation-patching mediation vs random-control.

## 결과
seen 8/8 유효 · mediation 0.40 = control 0.40 = 국소 바인딩 부재 → trunk-objective-floor 종결증거. caveat: 지표 A-국소성 미완벽분리(DIRECTIONAL).

## 함의
국소 부분공간 없음 → ⑤frame-break(anchor 외재화)가 유일 우회. follow-on=head-level patching + frame-break 생성경로 대비.

## 관련
[[goal-g1-lever-discovery]] · H_6177 · H_6175 · H_6174 · H_6169
