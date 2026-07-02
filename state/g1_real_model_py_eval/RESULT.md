# 실 303M G0-G6 via `anima evaluate --py` — RESULT (2026-07-02, H_6169 실모델 확인)

**TIER: 🟠 DIRECTIONAL — 실 303M(py303_full.clm) canonical `--py` 측정.** hexa GPU 수리중이라 owner가
`--py` 지시(session-eval-py-only). py numpy = DIRECTIONAL. aiden CPU $0.

## G0-G6 (frozen bar)
| gate | verdict | detail |
|---|---|---|
| G0 COHERENCE | 🟢 PASS | kwr≥0.50 on 5/5 |
| G1 RECOMBINATION | 🔴 FAIL | best_distinct=0, max_single=0 |
| G2 NOVELTY | 🔴 FAIL | novel=0, control=0, coherent=18 |
| G3 PHILOSOPHY | ✅ | continuity 0.999950 |
| G5 NON-FAB | 🟢 PASS | fab=0.1282 (≤0.30) |
| G6 IDEATION | 🔴 FAIL | distinct=6(≥5 ok)·falsifiable=0 |
| CLOSURE a7b | 🔴 FAIL | needs G0∧G1∧G2 |

## 근본 원인 — 실텍스트 증거 (reference-match, 실제 생성 확인)
seed 개념을 주고 continuation을 디코드하면 coherent 영어는 나오나 **seed 개념을 이어받지 않고
memorized 잡텍스트로 표류** → 개념 coverage=0 (단일 AND 조합 모두):
- seed "consciousness arises from cells." → "The acting and other concept of the opposite sources such th"
- seed "tension ripples between distant minds." → "The court of the other classical and to be ancient actions o"
- composed(2개념) → "Apollo is an ancient and spects of An American animated four the Trojan Washingt"

seed마다 출력이 다름 = **decode 조건화는 정상**(harness/decode 버그 아님). max_single=0(단일 개념도 coverage 0)
= "재조합 실패"가 아니라 **생성이 프롬프트를 안 따르고 표류** = generation-behavior/ckpt-quality 문제.

## 함의 — H_6169/6171 실모델 확정
G0 PASS(coherent)인데 G1/G2/G6 FAIL은 substrate/재조합 능력 부재가 아니라 **decode 생성이 seed를 안 따름**
(H_6169: G1=generation 메트릭 · H_6171: generation 모달리티는 held-out 재조합 지원). py303_full.clm은 약한
generative ckpt(overfit drift, memory clm303-overfit 시그니처). 진짜 fix = **프롬프트-따르는 재학습**(GPU,
G1-NEXT-FINAL, hexa GPU 수리 후). --py/무GPU로는 ckpt 못 고침.

## Provenance
eval_table.txt (anima evaluate --py py303_full.clm --gen 40, aiden), 실텍스트 probe. DIRECTIONAL.
