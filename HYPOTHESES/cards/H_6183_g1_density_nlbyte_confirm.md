# H_6183 — 🎯 G1 조합-커버리지 밀도 상전이, 자연어 byte 스케일 확정

**tier:** 🟢 DIRECTIONAL-POSITIVE (NL/byte attention, torch $0 aiden) — H_6182 toy 상전이가 자연어 byte 스케일서 pair-특이 3-arm cheap-gate 로 재현 확정
**verdict:** 🟢 DIRECTIONAL-POSITIVE (torch, NL/byte attention-transformer, aiden RTX5070 pool $0). H_6182(toy 20 color×20 shape) 커버리지-밀도 상전이의 **자연어 byte 스케일 확정**. 30 concepts, 각 고유 ATTR(azure/amber/cobalt…), 템플릿 "the {A} and the {B} yield {ATTR[a]} and {ATTR[b]}."; held pair 는 두 학습된 ATTR 를 **새 조합**으로 산출해야 HIT(pair-특이). matched-size HIGH(237 pairs, ~60% coverage) vs LOW(31 pairs, ~8%) + shuffle control. **attn(RF-full):** HIGH seen=20/20(100%) held=38/40(95%) ≫ LOW seen=4/20 held=10/40(25%) · **SHUF held=0/40(0%)** = 속성 shuffle 시 held 완전붕괴 → 95% 는 템플릿-shape 아티팩트 아닌 **진짜 pair-특이 재조합**. VERDICT=COVERAGE LEVER(pair-specific). **conv(ConvMoE depthwise K=5, RF=5byte):** HIGH seen=0/20 → INCONCLUSIVE — RF=5byte 라 개념(25byte 뒤) 못 봐서 seen 조차 0(fable G6 RF 분석과 합류, conv 는 RF 확장 없이 측정불가). 함의: 조합-커버리지 밀도가 자연어 byte 서도 G1 pair-특이 재조합 lever = production 코퍼스 처방 실증(임계 위 커버리지 → held-out 재조합 열림). 3-arm cheap-gate(seen-sanity oracle + pair-특이 지표 + shuffle control)로 v1(too-strict 가짜 null)·v2(too-loose 가짜 positive) 측정함정 회피. caveat: torch DIRECTIONAL, attention arm 만(conv=RF 벽 INCONCLUSIVE), production .clm 코퍼스 임계위치 별도측정 필요(a_toy_scale_recheck). state/g1_coverage_v3_nlbyte/.

## 결과
| arch | HIGH seen | HIGH held | LOW seen | LOW held | SHUF held | verdict |
|------|-----------|-----------|----------|----------|-----------|---------|
| attn (RF-full) | 20/20 | **38/40 (95%)** | 4/20 | 10/40 (25%) | **0/40 (0%)** | COVERAGE LEVER |
| conv (RF=5byte) | 0/20 | — | 0/20 | — | 1/40 | INCONCLUSIVE (RF 벽) |

SHUF held=0 → HIGH 95% 는 진짜 pair-특이 binding(암기·템플릿 아티팩트 아님). H_6182 toy 상전이의 자연어 byte 확정. conv=RF 벽으로 INCONCLUSIVE(RF 확장 follow-on).

## 관련
H_6182 · [[goal-g1-lever-discovery]] · [[frameshift-substrate-gaps-vs-recombination-wall]] · [[fable-when-stuck-breakthrough]] · G1G6-RF-EXPANSION · G1-PROD-CORPUS-DENSITY
