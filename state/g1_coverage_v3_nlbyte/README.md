# G1 조합-커버리지 밀도 — 자연어 byte 스케일 확정 (H_6183)

H_6182(toy 20 color×20 shape 커버리지 상전이)의 **자연어 byte 스케일 확정**.
torch DIRECTIONAL (aiden/summer RTX5070 pool, $0). engine-native 아님.

## 설계
- 30 concepts, 각 고유 ATTR 단어(azure/amber/cobalt…) 부여.
- 템플릿: `the {A} and the {B} yield {ATTR[a]} and {ATTR[b]}.`
- metric `recomb()`: held pair generation 이 **ATTR[a] AND ATTR[b] 둘 다** 포함해야 HIT
  = 두 학습된 속성의 **새 조합** 강제 (pair-특이, v1/v2 측정함정 회피).
- arms: HIGH(237 pairs ~60% coverage) vs LOW(31 pairs ~8%, matched ~1.2MB) + SHUF(속성 shuffle control).
- INCONCLUSIVE gate: seen-sanity<10 이면 학습부족.

## 파일
- `bt_v3.py` — pair-특이 실험 스크립트 (HIGH/LOW/SHUF arms, seen-sanity + pair-특이 metric + shuffle control)
- `corpus/high_v3.txt` `low_v3.txt` `shuf_v3.txt` — v3 생성 코퍼스
- `corpus/high_coverage.txt` `low_coverage.txt` — 이전 coverage 코퍼스(PR #2795 계열)
- `newcorpus_v3_attn.json` — attn arm 수치
- `v3_attn.log` — raw stdout

## 결과 (verdict = state/verdicts/6183_g1_density_nlbyte/H_6183.txt)
attn: HIGH held 95% ≫ LOW 25%, SHUF 0% → COVERAGE LEVER (pair-specific).
conv: HIGH seen 0/20 → INCONCLUSIVE (RF=5byte 벽, fable G6 RF 합류).

## follow-on
- conv RF 확장(dilated/wide-K ConvMoE, param-matched) → conv 도 상전이 타는지 (G1G6-RF-EXPANSION).
- production .clm 코퍼스가 target 개념쌍 커버리지 임계(~20%) 위/아래인지 측정 → 아래면 조합-커버리지 설계 코퍼스로 재학습 (G1-PROD-CORPUS-DENSITY).
