# H_6184 — 🎯 G1 커버리지-밀도 lever = arch-무관 (dilated-conv RF 돌파, 자연어 byte)

**tier:** 🟢 DIRECTIONAL-POSITIVE (NL/byte, attn ∧ dilated-conv, torch $0 summer) — H_6183 자매 확증 + conv RF 벽 돌파로 arch-무관 입증
**verdict:** 🟢 DIRECTIONAL-POSITIVE (torch, NL/byte, summer RTX5070 cuda $0). **fable(claude-fable-5, 자율 full-pipeline $6.26, modelUsage 확증=opus 폴백 아님)이 처음부터 코퍼스 제작·학습·측정을 자율 수행**해 H_6183(내 v3) 을 독립 재현 + **conv RF 벽 돌파**. 설계: 24 attr·60 held pair·400 high-train(60% cov) vs 40 low-train(8%)·shuffle_map, 3000 step, seen-true/held/seen-shuffled 3중 채점. **attn(RF-full):** HIGH held 0.950 ≫ LOW held 0.033(LOW seen=100% properly-trained → 깨끗한 floor) · SHUF true-target 0.0(seen-shuffled 0.75 학습=하네스 유효). **convd(DILATED conv, RF 확장):** HIGH held **0.850** ≫ LOW held 0.0 · SHUF 0.0(seen-shuffled 0.933) → **RF 확장이 conv 의 G1 벽을 깸**(H_6183 plain conv K=5 RF=5 는 seen 0/20 INCONCLUSIVE 였음). 즉 커버리지-밀도 lever 는 attention 과 dilated-conv 둘 다서 상전이 = **arch-무관** 확정, 동시에 G1G6-RF-EXPANSION follow-on(RF 확장이 conv 를 상전이 태움) 실증(fable G6 RF 분석 합류). 함의: G1 재조합벽 = trunk-objective TERMINAL 아니라 (a)데이터-커버리지-밀도 + (b)수용영역 이중 bound → production 처방 = 조합-커버리지 설계 코퍼스 + 충분 RF(depth/dilation). caveat: torch DIRECTIONAL, toy-NL byte, production .clm 임계위치 별도측정(a_toy_scale_recheck).

## 결과
| arch | HIGH held | LOW held | SHUF true | SHUF shuffled-tgt | 판정 |
|------|-----------|----------|-----------|-------------------|------|
| attn (RF-full) | **0.950** | 0.033 | 0.0 | 0.75 (하네스 유효) | LEVER |
| convd (DILATED, RF 확장) | **0.850** | 0.0 | 0.0 | 0.933 | LEVER (RF 벽 돌파) |

전 arm seen-true=1.0(LOW 포함, H_6183 LOW seen 20% 보다 깨끗). dilated-conv 가 H_6183 plain-conv INCONCLUSIVE 를 해소 → 커버리지 lever arch-무관.

## 관련
H_6183 · H_6182 · G1G6-RF-EXPANSION · G1-PROD-CORPUS-DENSITY · [[fable-when-stuck-breakthrough]] · [[workflow-model-fable-override-ignored]] · [[frameshift-substrate-gaps-vs-recombination-wall]]
