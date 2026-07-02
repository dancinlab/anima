# H_6187 — 🎯 G1 L8+coverage canonical gen=40 재측정: gen-artifact 확증 + engine-native G1=0 floor (torch 발산 → 엔진조사)

**tier:** 🟢 engine-native --py (numpy byte-parity port of core/clm_decode.hexa, torch-free = session-eval-py-only TERMINAL 자격) — gen40 canonical clean 3-way. gen-artifact 대조 = **CONFIRMED**. L8-cov coverage-transfer = **DISPUTED-pending**(torch DIRECTIONAL 발산, 엔진조사 in-flight).
**verdict:** 🟢 CONFIRMED(gen-artifact) + 🟠 DISPUTED(coverage-transfer). 이전 gen=80 non-canonical 3-way(G0 붕괴로 G1=0 무효)를 **canonical gen=40**으로 clean 재측정 — 전 arm **G0 5/5 PASS 선행**(garbage 아님) 위에서 측정.

## 3-arm gen40 verdict (state/g1_coverage_prod_block/results_gen40/)
`python3 cli/evaluate.py <clm> --corpus x4 --gen 40` (numpy byte-parity, grep import-torch|gauge_lib=NONE, 3 ckpt sha256 mac==aiden 검증, gen-guard "frozen bars" 정상):

| arm | ckpt sha | G0 kwr | G1 bestdistinct/max | G2 novel | G5 fab | G6 dist/fals |
|---|---|---|---|---|---|---|
| **L4_clean** (baseline) | e807672 | 🟢 **5/5** | 🔴 **0/0** | 🟢 40 | 🟢 0.088 | 🔴 5/0 |
| **L8_nocov** (깊이만) | 5777c50 | 🟢 5/5 | 🔴 0/0 | 🟢 69 | 🟢 0.028 | 🔴 6/0 |
| **L8_cov** (깊이+coverage) | 2c565ad | 🟢 5/5 | 🔴 **0/0** | 🟢 **100** | 🟢 0.086 | 🔴 6/0 |

(G3 read continuity=0.999950 impostor=0.0 전 arm · G4 N/A · closure a7b_pass=FAIL 전 arm)

## 판정
### ① gen-artifact 대조 → CONFIRMED (terminal)
L4-clean gen40 **G0 5/5 재현**(이전 확정치 state/clm303_clean_corpus/g0g6_py.txt 일치). ⇒ 이전 gen=80 의 G0 2/5 붕괴는 **순수 gen-param(AR-drift) artifact** = clm byte-LM 이 긴 gen 에서 뒤쪽 byte-garble → G0 kwr 인위 붕괴 → G1/G6 cascade. gen-guard(PR #2821)가 이미 코드로 차단(gen≠40 → NON-CANONICAL/DIRECTIONAL 자동 라벨). **verdict-integrity 완결**: 측정경로(gen param) 의심 → 확인 → clean 재측정.

### ② L8-cov coverage-transfer → engine-native G1=0 floor (torch 발산, 엔진조사 in-flight)
전 arm **G0 5/5 PASS 선행**(gen-guard 교훈 준수, garbage 아님) 위에서:
- **L8-cov G1 best_distinct=0** — RF L=8(RF≈511B) + 조합-커버리지 블록 둘 다 넣어도 engine-native G1 재조합 floor. torch DIRECTIONAL coverage 레버(H_6182~6185: toy/NL byte 상전이 + production 코퍼스 BELOW)와 **발산**.
- **L8-nocov G1=0** — 깊이 단독 안 엶(H_1598 depth FALSIFIED 정합).
- **흥미로운 부분**: L8-cov **G2 novel=100**(전 arm 최고, coverage 블록이 novelty 는 올림) 이나 G1 재조합·G6 fals 는 floor = coverage 가 신규성은 주되 조합-바인딩은 아님.
- ⚠️ **DISPUTED**: torch(coverage 레버 열림) vs engine-native(G1=0)의 발산은 terminal 박제 전 확인 대상(verdict-integrity). 이전 전례(g1g6-wall-engine-innocent-3axis · H_1587): torch≠engine 진범이 forward/weight/detector 아니라 옛 scaffold+best-of-K 하네스(gauge_lib._decode) = torch 부풀림, engine 무죄. 이 L8-cov ckpt 도 동형인지 **엔진조사 in-flight**(forward byte-diff · detector parity · decode-procedure 격리 3축). 조사 결과 = engine 무죄면 engine-native floor terminal 확정, 유죄면 재측정.

## 함의 (조사 pending)
- gen-artifact 확증 = **확정**(gen-guard 정당화 완결).
- coverage torch→engine transfer = **미확정**(발산). 엔진 무죄 예상(전례 강함)이나 이 ckpt 재확인 필요. 무죄면 = **G1 coverage 레버는 torch-side artifact, engine-native 는 trunk-objective floor 유지**(convergence G1_WALL 갱신 대상).

**wired:** engine-native measured (--py byte-parity, torch-free). coverage-transfer verdict 는 엔진조사(forward/detector/decode 3축) 착륙 후 확정.

## 관련
H_6185(coverage BELOW·처방 L8+블록) · H_6186(G6 form-priming) · H_6184 · H_6183 · H_6182 · H_1598(depth FALSIFIED) · H_1587(torch≠engine sampler) · [[g1-coverage-density-nl-bytes-lever]] · [[g1g6-wall-engine-innocent-3axis]] · gen-guard PR#2821(evaluate-hexa-2)
