# H_6174 — 🏋️ G1 training-recipe toy 3-실험 (TRUE GAP)

**tier:** 🧱 toy training-recipe = 암기(seen 8/8) BUT held-out 재조합 0~1/5 = TRUE GAP; corpus/copy-skill/data-scale 다 바인딩 설치 실패
**title:** 🏋️ G1 training-recipe toy 3-실험(structured corpus·copy-skill aug·coverage ladder) — 소형 byte-GPT이 seen 쌍 8/8 마스터하나 held-out 재조합 0~1/5 = undertraining 아닌 TRUE 재조합 갭, corpus/objective/data-scale toy 처방은 변수바인딩 못 심음
**verdict:** 🧱 TRUE RECOMBINATION GAP at toy scale (torch DIRECTIONAL, aiden/summer $0, 소형 byte-GPT d256 4L). G1-NEXT-FINAL toy. 3 실험 3종세트(seen-sanity oracle+pair특정지표+shuffle control): v3 pairspec(structured corpus) REAL pair_hit 0/5·shuffle 1/5 NO BREAK · copyskill(copy-skill 라인 aug) seen 8/8 마스터·held 1/5 NO TRANSFER · coverage ladder(seen 4→16쌍) held mean 2.0 flat NO data-scale lever. 모델은 seen 완벽 마스터(8/8)=undertraining 아님, held-out 0~1/5=암기만·일반화X=TRUE 재조합 갭. structured corpus·copy-skill·data-scale 어느 것도 toy 스케일서 변수 바인딩 설치 못함. ★지표교훈: v1 ANY-coverage는 템플릿 echo로 shuffle도 만점(non-discriminating)→pair특정 지표 필수(fair-cheap-gate-design-1). 함의: G1=변수바인딩 결핍 재확인(H_6169~6173). 남은 미검 축=arch(copy/induction-head)·trunk(TPR)·frame-break(neurosymbolic kosmos)[ING G1-BS-1~4], 실 303M 재학습(scale 증폭 가설)도 미검. state/g1_training_recipe_toy/RESULT.md.

## 발상 (G1-NEXT-FINAL toy, owner training go)
structured corpus + copy-skill aug + data-coverage ladder가 held-out 재조합을 여는지 소형 byte-GPT로 시험.

## 결과
seen 8/8 마스터 BUT held-out 0~1/5 = undertraining 아닌 TRUE 재조합 갭. 3 처방 전부 바인딩 설치 실패. v1 ANY-coverage 지표결함→pair특정 재채점.

## 함의
G1=변수바인딩 결핍(H_6169~6173). 남은 미검=arch/trunk/frame-break(ING G1-BS-1~4) + 실303M 재학습 scale.

## 관련
[[goal-g1-lever-discovery]] · H_6169 · H_6171 · H_6172 · H_6173 · [[fair-cheap-gate-design]]
