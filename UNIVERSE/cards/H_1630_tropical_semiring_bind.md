# H_1630 — Tropical (max-plus) semiring binding mouth

- **tier:** 🔴 NOT-SUPPORTED (⏳ EVAL DONE · DIRECTIONAL · py 2-production engine · binder-dropped co-training · 9/9)
- **wired:** DIRECTIONAL-mirror — binder trained but DROPPED at .clm serialize; additive readout = no runtime binding. Terminal = hexa engine-native re-run.
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** semiring algebra — tropical (max,+) replaces the (+,×) ring; idempotent selective binding (Viterbi-style), no superposition crosstalk
- **artifacts:** `state/h1630_tropical_mouth/` (RESULT.md · ckpt/*.clm · ckpt/*.g0g6.txt)
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `tropical_semiring_bind`

## Mechanism

Replace the ring (+,×) that conv and attention live in with the tropical semiring (max,+). Each forward step forms a role-filler score matrix S[r,f] = role_proj + filler_proj (additive = multiplicative in log space), and the bound representation per role is a tropical matvec b[r] = max_f (S[r,f] + value[f]), with the argmax routing exactly one filler to each role. Both legs combine in one pass via max-plus contraction = a hard, temperature-annealable (softmax T→0) winner-take-one assignment.

## Why it crosses the binding wall

Ring-based binders (outer product, circular conv, attention) SUPERPOSE fillers — every role gets a weighted blend, and across L24 depth the blends crosstalk until distinct role-filler pairs become inseparable (the observed fals=0). Max-plus is idempotent (max(x,x)=x) and selective: it forces a discrete one-filler-per-role assignment that survives depth without smearing — the exact reason Viterbi/DP uses the tropical semiring. Recombination crosses because a novel pair is simply a new argmax in the same score matrix; no learned weight for that specific pair exists or is needed. Ablation is a single continuous knob: anneal the semiring temperature from tropical (T→0) back to log-sum-exp/softmax (T=1, = ordinary attention). If the G1/G6 lift vanishes monotonically as T→1, max-plus selectivity is proven load-bearing rather than incidental.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, $0, frozen-first. Synthetic 4 roles × 8 fillers with random projections. Pre-registered bar: tropical bind separates held-out role-filler pairs (linear-probe acc ≥0.90) while the T=1 softmax control stays <0.60, AND tropical decode is invariant to injected distractor fillers (no crosstalk) whereas softmax degrades with each distractor. Decision: if tropical ≤ softmax or crosstalk-invariance fails, FALSIFIED.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Cost-gated 303M, pre-register only. Swap attention's softmax-weighted value sum for a temperature-annealed max-plus head (start T=1 for trainability, schedule toward T→0; straight-through argmax for the hard limit) in K trunk layers. 4-cell corpus, held-out DESCENT, CORE-mount G1/G6. Pre-register the annealing schedule and bar; ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).


## Measured Result (2026-06-30 · py 2-production engine · DIRECTIONAL)

**Training:** 9 CLMs (binder DROPPED at .clm serialize, additive readout). All 4/4 DESCENT (val_CE < 5.545) per arm/seed.

**G0-G6 results:**

| arm | seed | G0 n/5 | G0? | G1 best_distinct | G1 max_single | G6 dist | G6 fals | a7b? |
|-----|------|--------|-----|-----------------|---------------|---------|---------|------|
| soft | 7 | 1/5 | FAIL | 0 | 0 | 3 | 0 | FAIL |
| soft | 4302 | 3/5 | FAIL | 0 | 0 | 5 | 0 | FAIL |
| soft | 4303 | 2/5 | FAIL | 1 | 0 | 4 | 0 | FAIL |
| mid | 7 | 3/5 | FAIL | 0 | 1 | 2 | 0 | FAIL |
| mid | 4302 | 3/5 | FAIL | 0 | 0 | 3 | 0 | FAIL |
| mid | 4303 | 3/5 | FAIL | 0 | 0 | 3 | 0 | FAIL |
| arm | 7 | 3/5 | FAIL | 0 | 0 | 3 | 0 | FAIL |
| arm | 4302 | 4/5 | PASS | 0 | 0 | 5 | 0 | FAIL |
| arm | 4303 | 2/5 | FAIL | 1 | 0 | 1 | 0 | FAIL |

**Verdict: 🔴 NOT-SUPPORTED** (DIRECTIONAL — py 2-production engine)

G1 floors at the bar across all main arms while the trunk CAN cohere (>=1 arm G0 PASS) (sporadic best_distinct max=1<2 not above control max=1) — binder dropped at .clm serialize => additive readout; co-training insufficient for recombination. Note: main binding arm additionally DEGRADES G0 coherence (G0 PASS only in control arms).

**Scope:** binder dropped at serialize → this is trunk co-training effect only (not runtime binding). Same tier as EXP-3/H_1812/H_1814/H_1816. terminal verdict requires hexa engine-native re-run (a_engine_native_learning).
