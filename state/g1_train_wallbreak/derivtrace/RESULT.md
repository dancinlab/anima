# G1 lever#1 derivation-trace — 🟢 DIRECTIONAL-POSITIVE (최초 engine-native G1 lift)

**Fire:** summer pool (RTX5070 own-GEMM, GPU 99-100%), 2026-07-04. warm-FT h1129 303M ByteGPT(d1024 L24), 2000 step, 2-arm 통제(data-format만 변주). engine-native = `anima evaluate --py` BUILT-IN G0-G6(single-entry, TERMINAL-eligible per a_eval_py_canonical). held-out = concept 쌍 {c0,c1}(g6_ideation cz[]), 학습에 both orderings 전혀 미노출(memorization-free generalization).

## 결과 (frozen gen=40 engine-native)
| arm | G0 | G1 best_distinct/max_single | G2 | CLOSURE |
|-----|----|-----|----|---------|
| **DERIV** (target=derivation trace) | 🟢 5/5 | **🟢 PASS bd=2 > ms=1** | 🔴 novel=0(corpus none) | 🔴 |
| FLAT (target=최종답만, 통제) | 🟢 5/5 | 🔴 FAIL bd=2, ms=3 | 🔴 | 🔴 |

val_ce: DERIV 0.072 · FLAT 0.079(heldout_descent).

## 판정: 🟢 DIRECTIONAL-POSITIVE — 최초 engine-native G1 lift
derivation-trace data-format이 held-out 쌍 {c0,c1}에서 **G1 PASS**(bd=2 composed > ms=1 single-parent), **FLAT 통제는 같은 setup서 FAIL**(bd=2, ms=3) → data-format이 격리된 lever. 20+ decode family(g1-decode-wallbreak)+전 학습 family가 못 뚫은 벽을 처음 들어올림. CE=echo 메타법칙이 target=derivation엔 미적용(echo=derivation 생성=composition) 가설 지지.

## 정직 스코프 (c9 · robustness 미확인)
- **marginal**: bd=2는 threshold 정확값. margin(bd2>ms1)은 DERIV의 max_single이 낮아서(1)이지 bd가 높아서 아님.
- **held-out 1쌍**: {c0,c1} 단일. multi-pair robustness 미확인(a_scale_honest_scope).
- **G2 novelty 미측정**: corpus none으로 로드 안 됨 → composed 키워드 corpus-novelty 미확인. G1 내부 ∉seed logic만 통과.
- **paraphrase-invariance 미측정** · CLOSURE(a7b_pass G0∧G1∧G2) 미달.
- tier=DIRECTIONAL-POSITIVE(--py engine-native지만 marginal+1쌍). **robustness follow-on**: multi held-out 쌍 + G2 corpus + paraphrase 재측정으로 bd=2-threshold artifact 배제.

## artifacts
- deriv_eval.txt · flat_eval.txt · artifacts.txt(corpus gen + train json) · ckpt=~/anima-weights/g1_derivtrace/deriv.bin(pull)
