# H_6187 — 🎯 G1 L8+coverage gen=40 재측정: gen-artifact 확증 + L8-cov G1=0 = INCONCLUSIVE(측정 2중 mismatch) + ⭐재조합 능력 작동 반례

**tier:** 🟢 CONFIRMED(gen-artifact, engine-native --py TERMINAL) + 🟠 INCONCLUSIVE(coverage-transfer, 측정-무결성 mismatch — terminal 아님) + ⭐긍정발견(held-out 재조합 능력 작동).
**verdict:** 🟢 CONFIRMED(gen-artifact) + 🟠 **INCONCLUSIVE**(coverage-transfer, terminal 철회). 초기 "engine-native G1=0 floor TERMINAL" 판정은 **과판정 → RETRACTED**. 엔진조사(엔진 무죄, torch·engine 둘 다 303M G1=0)에 이어 mismatch 조사 + $0 분리 프로브로 **G1=0 의 진짜 원인 = 측정-무결성 2중 mismatch(유발 표면형 + T=24 decode-window)** 확정 — trunk-objective 와 무관. 게다가 **재조합 능력은 이미 작동**(held-out unseen 쌍 ember+dune→golden+zinc 정확 재조합) = "재조합 벽 = trunk floor" 메타법칙 반례. 이전 gen=80(G0 붕괴 무효)를 canonical gen=40 clean 재측정 — 전 arm **G0 5/5 PASS 선행**.

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
### ③ 3단 조사 → G1=0 = 측정 mismatch (INCONCLUSIVE, terminal 철회)
초기 "engine-native floor terminal"을 3단으로 파고들어 **철회**:
- **엔진조사**(state/g1_engine_investigate/): 엔진 무죄. torch·engine 둘 다 303M G1=0(L8-cov 학습로그 torch fp32 probe 도 g1_distinct=0) = "발산" 아닌 category error. forward argmax 일치, detector 둘 다 0. torch coverage 신호(H_6182~6185)는 TOY held-out 정확도 축(생성 아님).
- **mismatch 조사**(state/g1_coverage_mismatch_probe/REPORT.md): coverage 블록은 "the A and the B yield [attr]" 8 고정 템플릿으로 조합 학습했는데 G1 gate 는 gate 문장 시드 자유생성 측정 → **유발 표면형 mismatch**. gate 시드 내용어가 블록에 0회 = 학습된 combiner 미트리거. toy v3 GREEN 도 학습 템플릿 접두사 프롬프트로 쟀음(자유형 transfer 미검증).
- **$0 분리 프로브**(state/g1_coverage_mismatch_probe/separation/, engine-native --py greedy): ①매핑 못배움 REFUTED(SEEN both 6/12, ocean+stone→azure+russet)·③진짜 floor **REFUTED**(held-out unseen ember+dune→golden+zinc 정확 재조합)·②**표면형/window-잠금 확정**. 추가 물리 병목: ckpt decode window **T=24 bytes** 라 "the consciousness and the tension yield"(40B+)에서 첫 gate 개념이 window 밖으로 밀려나 물리적 공동조건화 불가.

## 함의 (확정)
- gen-artifact 확증 = **확정**(gen-guard 정당화 완결).
- **L8-cov G1=0 = INCONCLUSIVE**(terminal 철회) — trunk-objective floor 증거가 **아님**. 진짜 원인 = 측정-무결성 2중 mismatch(①유발 표면형: gate 프롬프트가 학습 형식 밖 ②decode-window T=24: 긴 gate 개념 공동조건화 물리 차단), 둘 다 trunk objective 무관.
- **⭐ 반례 발견**: held-out(코퍼스 미노출) 조합 재조합 능력이 이미 **작동**(ember+dune→golden+zinc, window 안일 때) = "G1 재조합 벽 = trunk objective floor" 메타법칙에 대한 반례(이 템플릿 과제·window 안). combiner 는 작동하고 G1 gate 로 표면화만 안 됨.
- **처방(재학습 필요, terminal 아님)**: ①표면형 정합 코퍼스(gate free-gen 형식으로 조합 학습, non-gate 개념·gate 쌍 held-out 유지) + ②window/배치 정합(긴 gate 개념이 T=24 window 공존하게 짧게 배치). gate/bar frozen 유지(tune-to-green 금지).

**wired:** engine-native measured (--py byte-parity, torch-free). gen-artifact 부분 terminal 확정. coverage-transfer = INCONCLUSIVE(표면형+window 정합 재학습 follow-on 후 재판정).

## 관련
H_6185(coverage BELOW·처방 L8+블록) · H_6186(G6 form-priming) · H_6184 · H_6183 · H_6182 · H_1598(depth FALSIFIED) · H_1587(torch≠engine sampler) · [[g1-coverage-density-nl-bytes-lever]] · [[g1g6-wall-engine-innocent-3axis]] · gen-guard PR#2821(evaluate-hexa-2)
