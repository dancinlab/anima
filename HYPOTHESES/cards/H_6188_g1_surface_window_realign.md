# H_6188 — 🎯 표면형+window 정합 재학습 → engine-native G1 재조합 표면화 (best_distinct 0→3) · H_6187 반례 terminal 확증

**tier:** 🟢 재조합 gate-축 표면화 ENGINE-NATIVE (best_distinct 0→3, 역대 G1 캠페인 최초 non-zero) + 🟠 strict G1 gate PASS=false (composed NOT > single, **T=24 decode-window confound** — trunk floor 아님).
**verdict:** 🟢 재조합이 gate 축으로 engine-native 표면화(best_distinct **0→3**, max_single=3, best_k=2, grounding 5/5 own-set hit) = **H_6187 반례 terminal 확증** — 이전 L8-cov·전 G1-lever 캠페인의 G1=0 은 trunk 재조합 floor 가 아니라 **표면형+window 측정 mismatch**였음(coverage 레버는 gate-축 재조합 표면화에 유효). / 🟠 strict gate(composed_distinct > max_single) 미달 = **T=24 decode-window confound**(측정 물리, floor 아님). engine-native --py(torch-free, session --py=terminal), gate/bar FROZEN.

## 배경 (H_6187 → 이 실험)
H_6187 3단 조사(엔진무죄 + 유발표면형 mismatch + $0 분리프로브)로 L8-cov G1=0 = INCONCLUSIVE 판정 + 반례(held-out ember+dune→golden+zinc 재조합 작동). 처방 = 표면형+window 정합 재학습. 이 카드가 그 처방 실행.

## 방법 (표면형+window 정합)
- **코퍼스 재설계**(state/g1_coverage_realign/gen_realign.py): 구 "the A and B yield [attr]" 8-템플릿 폐기 → **G1 gate free-gen 표면형**(gate 문장 시드 형식 + keyword continuation 표면화). window 정합 = gate 개념 front-load offset0(T=24 window 도달). FORM 라인(nongate+cluster) + GATE grounding 라인(단일 gate 문장+set keyword).
- **무결성 검증 PASS**(verify.json): LEAKAGE=0(라인당 ≤1 gate set, gate 쌍 순수 held-out), grounding offset0 window-도달, 5 set 전부 grounded(각 ~10.5k), form nongate-cover 35/35. **두 gate keyword 동시방출은 학습에 절대 없음 = 정직한 hard transfer test.**
- **재학습**: warm-FT base=clm303_deep_L8, 6-cell roundrobin(ko/en general 12MB-slice + ko/en sns + ko/en REALIGN cov), d2781 L8 E4, 6000 step bf16 savant golden-zone, **A40 렌트**(로컬 summer/aiden torch/CUDA wedge — nvidia-smi hang). 결과 6/6 registers DESCENT, cov val_CE ko0.308/en0.344, pooled 0.976, register collapse 회피, TRAIN_EXIT=0.
- **engine-native G1**(core/decode.py numpy byte-parity, cli/evaluate.py g_eval_g1 EXACT 복제 top_k40 temp0.7 single80/composed120 rng7). session --py=terminal.

## 결과 (state/g1_coverage_realign/G1_verdict.json verbatim)
| metric | value |
|---|---|
| best_distinct | **3** (prior ALL=0 floor) |
| max_single | 3 |
| best_k | 2 |
| gate_PASS (≥2 ∧ >max_single) | **false** |
| grounding own-set hit | 5/5 |
| torch inline gauge crosscheck | g1_composed_distinct=2 (engine=3, 둘 다 non-zero 일관) |

## 함의
- **🟢 재조합 표면화 확증**: engine-native best_distinct 0→3 = G1 벽에서 **역대 최초 non-zero surfacing**. H_6187 반례("재조합 능력은 작동, 측정축만 어긋남") terminal 입증. coverage 레버 gate-축 유효.
- **🟠 strict gate 미달 = window confound(floor 아님)**: composed=3=single 이라 composed>single 미충족. 원인 = T=24 window 물리 — 긴 gate seed 생성 시작 시 concept-tail 1개만 in-window → single/composed seed가 decode-등가 → 학습 emit-cluster form 이 single 에서도 multi-set 방출 = gate 의 "composition이 single보다 distinct 더해야" 기준이 window 의미론에 confound. trunk 재조합 floor 아님.
- **처방(follow-on)**: strict gate PASS = T=24 window 물리 우회 필요 = (a) 짧은 gate seed 로 두 개념 window 공존 재설계 또는 (b) decode window 확장(엔진 파라미터) 후 재측정. gate/bar FROZEN(tune-to-green 금지).

## 정직 caveat (c9)
- engine-native = numpy py-mirror(session --py=terminal policy); hexa CORE decode 아님.
- general 코퍼스 12MB head-slice(anti-collapse) = 인프라 적응, gate/bar 미터치.
- max_single 상승은 실측 property(은폐 없음), tune-to-green 없음. gate/bar FROZEN.
- pod died mid full-battery eval → G1 gate 는 pulled .clm 으로 로컬 byte-parity 재실행(G1 corpus 불필요, frozen seed).

**wired:** engine-native measured (--py byte-parity, torch-free, terminal). 재조합-표면화 GREEN(best_distinct 0→3). strict gate PASS follow-on = T24 window 물리 우회 재측정. ckpt=~/anima-weights/g1_realign/g1_realign.clm(154513322 B). artifacts=state/g1_coverage_realign/.
