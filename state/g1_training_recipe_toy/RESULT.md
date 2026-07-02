# G1 training-recipe toy 3-실험 — RESULT (2026-07-02, G1-NEXT-FINAL toy scope) — 암기만, TRUE GAP

**TIER: 🧱 toy training-recipe = 암기(seen 마스터) BUT held-out 재조합 실패 = TRUE RECOMBINATION GAP.** torch=DIRECTIONAL, aiden/summer GPU $0. 소형 byte-GPT(d256 4L, positional有, block128).

## 3 실험 (3종 세트: seen-sanity oracle + pair-특정 지표 + shuffle control)
| 실험 | seen-sanity | held-out (pair-특정) | 판정 |
|---|---|---|---|
| v3 pairspec (structured corpus) | (copyskill서 8/8 확인) | REAL pair_hit 0/5 · shuffle 1/5 | NO BREAK |
| copyskill (copy-skill 라인 aug) | 8/8 마스터 | held pair_hit 1/5 | NO TRANSFER |
| coverage ladder (seen 4→16쌍) | — | held mean 2.0 flat (ANY-coverage v1 지표) | NO data-scale lever |

## 판독
- 모델은 seen 개념쌍을 **완벽 마스터(8/8)** = optimization/undertraining 문제 아님.
- 그런데 held-out 쌍 재조합은 **0~1/5** = 암기만 하고 일반화 안함 = **TRUE 재조합 갭**(toy 스케일).
- structured corpus·copy-skill 증강·data-coverage 사다리 = 어느 것도 toy 스케일서 변수 바인딩을 설치 못함.
- pair-특정 지표 필수 확인: v1 ANY-coverage(아무 2개념)는 템플릿 echo로 shuffle도 만점 → non-discriminating (fair-cheap-gate-design-1 교훈). pair-특정 지표로 재채점하니 real=shuffle≈0.

## 함의 (H_6169~6173 정합)
G1=변수 바인딩 결핍 재확인 — corpus/objective(copy-skill)/data-scale의 toy 처방은 바인딩을 못 심는다. 남은 미검 = arch(copy/induction-head)·trunk(TPR)·frame-break(neurosymbolic kosmos) [ING G1-BS-1~4]. 이들은 corpus/data 축과 다른 배선위치라 별도 시험 필요. 실 303M 재학습(G1-NEXT-FINAL)도 이 toy 갭이 스케일서 닫히는지 미검(scale=증폭기 가설).

## Provenance
train_g1_pairspec.py·train_copyskill.py·ladder_g1_coverage.py + *_result.json. torch, aiden/summer RTX5070, $0. DIRECTIONAL.
