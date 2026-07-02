# H_6169 — 🔎 G1 메트릭 정체 (generation-diversity, not recombination)

**tier:** 🟠 ANALYSIS — anima G1(composed_distinct)=generation-diversity 메트릭이지 held-out 재조합 측정 아님; G1=0=생성 floor(하류)
**title:** 🔎 G1 메트릭 정체 — anima G1(composed_distinct)은 5 고정 개념-문장 'if cA,then cB:' GENERATION 다양성 측정이지 held-out 인수-재조합 아님 → 실텍스트 G1=0은 substrate 재조합벽 아니라 generation-side floor
**verdict:** 🟠 ANALYSIS(코드 정독, $0). core/g6_ideation.py g6_build_frames/_g6_concepts: G1/재조합 메트릭 = 5개 고정 완전문장을 'if cA, then cB: ' 프롬프트로 주고 생성 continuation의 composed_distinct(다양성) 측정 + shuffled/ablated 대조. held-out train/test 분할 없음. ⇒ G1=0 = 303M decode가 composed 프레임서 distinct·coherent 생성 못함 = generation-diversity floor(G0 하류), 'substrate 재조합 불능' 측정 아님. H_6168(개념 feature distinct id 0.917)과 정합: 재료 有, generation-side가 병목. 옛 clm303 G1=0(H_1218) 재조합벽 해석은 실은 generation floor. #2(G1-NEXT-2) 재프레임: 기존 메트릭 재실행=무의미(생성측정), 진짜 재조합 terminal=held-out 조합분할 NEW generation 메트릭 설계 필요(owner-scope). state/g1_metric_is_generation_diversity/RESULT.md.

## 발상 (G1-NEXT-3, all-go)
실텍스트 G1=0이 진짜 재조합벽인지 확인하려 anima G1 메트릭 구성을 코드 정독.

## 발견
G1=5개 고정 개념-문장 'if cA,then cB:' 생성 다양성(composed_distinct) 측정, held-out 분할 없음 → G1=0=generation floor(하류), 재조합능력 측정 아님. H_6168과 정합.

## #2 재프레임
기존 메트릭 재실행 무의미(생성측정). 진짜 재조합 terminal=held-out 조합분할 NEW generation 메트릭(owner-scope).

## 관련
[[goal-g1-lever-discovery]] · H_6166 · H_6167 · H_6168 · H_1218 · [[substrate-framebreak-g1-combination-operator]]
