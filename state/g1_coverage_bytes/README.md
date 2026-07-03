# g1_coverage_bytes — 조합-커버리지 밀도 → pair-특이 재조합 (자연어 byte, 303M-이전 toy→NL 스케일 브리지)

**질문:** toy(20개념²)에서 확인된 "코퍼스 조합-커버리지 밀도 = 유일한 G1 양성 레버"가
자연어 byte 코퍼스에서도 pair-특이 재조합을 켜는가?

**설계 (측정 함정 3개 회피):**
- 개념 24 × 고유 속성 24. fact 라인("the ocean is silver .")이 부품을 전 arm 동일 학습.
- pair 라인("the ocean and the clock yield silver hollow .") = 조합 규칙(개념 순서대로 속성).
  → held pair 정답 = 학습된 두 부품의 **새 결합**(암기 불가).
- held 60쌍(전 arm 공통 미노출) · HIGH=400/552(72%)×30rep · LOW=40/552(7%, HIGH의 부분집합)×300rep
  → pair-라인 12,000개로 크기 매칭(byte 0.4% 이내). fact 6,000라인 동일.
- SHUFFLE control: HIGH와 동형이나 pair 속성을 고정-오답으로 치환(조합 규칙 파괴).
- 지표: prompt "\nthe A and the B yield" → greedy 26byte.
  strict = " attrA attrB"로 시작 · loose = 두 속성 포함. (v1 too-strict/v2 too-loose 회피)
- conv RF-벽 회피: attn(RF-full) 주역 + convd(depthwise K=5, dilation 1/2/4/8, RF≈61byte) 변종.

**모델/학습:** byte-LM d256·L4·H8·block64 (~3.3M params), AdamW 3e-4 cosine, bs128×3000step,
summer pool RTX5070. torch 미러 = **DIRECTIONAL** (engine-native 아님).

**파일:**
- gen_corpus.py — 코퍼스 생성기(seed 1234, 결정적)
- corpus_high.txt / corpus_low.txt / corpus_shuffle.txt — 3 arm 코퍼스 (~0.7MB each)
- meta.json — attr 맵·held/train 분할·shuffle 맵·eval 세트
- bt.py — 학습+측정(1 arm) · run_all.sh — 6 arm(attn/convd × high/low/shuffle) 순차
- results_*.json / log_*.txt — summer:~/g1full/ 에서 회수
