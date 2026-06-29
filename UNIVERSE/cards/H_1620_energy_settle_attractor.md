# H_1620 — Energy-settle attractor mouth (Hopfield/predictive-coding relaxation)

- **tier:** 🔴 NOT-SUPPORTED (⏳ EVAL DONE · DIRECTIONAL · py 2-production engine · binder-dropped co-training · 9/9)
- **wired:** DIRECTIONAL-mirror — binder trained but DROPPED at .clm serialize; additive readout = no runtime binding. Terminal = hexa engine-native re-run.
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** DYNAMICS
- **artifacts:** `state/h1620_hopfield_mouth/` (RESULT.md · ckpt/*.clm · ckpt/*.g0g6.txt)
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `energy_settle_attractor`

## Mechanism

Mouth forward is NOT feedforward — it is a fixed-point relaxation on a scalar energy E(z; a, b) with symmetric weights (modern-Hopfield / predictive-coding free-energy). Both legs are injected as CLAMPS (boundary conditions): leg_a (trunk/context state) and leg_b (the second representation to bind, e.g. retrieved register or role token) are held fixed while the hidden state z does gradient descent dz/dt = -∂E/∂z for K steps to an attractor z*, which is read out as the next-byte logits. The two legs combine because the settled minimum is a JOINT attractor — a basin that is deep only when both clamps are simultaneously consistent.

## Why it crosses the binding wall

conv/attention(L24) is a single feedforward sweep: it can only ADD-mix the two legs (weighted superposition), which is provably insufficient for a conjunction (the AND of two features). An energy minimum is a nonlinear constraint-satisfaction over BOTH clamps at once: the network cannot lower E unless z reconciles leg_a AND leg_b, so the readout is forced to be the bound conjunction, not a blend. Ablation logic: set relaxation steps K=1 → the operator collapses to exactly one feedforward layer (= conv/attn baseline) → conjunction accuracy drops to additive-baseline level. The lift between K=1 and K≫1 is attributable ONLY to the settling dynamics, isolating binding to the attractor, not to parameter count.

## Cheap test (frozen-first · $0 · decisive numpy probe)

Frozen-first numpy toy ($0): symmetric 2-layer energy net E(z)=½zᵀWz − zᵀ(U_a a + U_b b), relaxed by K=30 GD steps vs K=1 (ablation). Task = held-out 'dual-leg conjunction': two 8-bit legs, target = AND/parity over a hidden position pair (one index in a, one in b) — additive models provably can't fit. PRE-REGISTERED bar: settled (K=30) held-out acc ≥0.90 AND CE < shuffle-leg control; K=1 ablation ≤0.62 (≈additive baseline). Decisive if (settle − ablation) gap ≥0.25 on UNSEEN leg-pair combos.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

(pre-registration only, cost-gated) Replace the 303M mouth's final-block forward with a weight-tied energy block (symmetric W, K=8 settle steps, leg_a=trunk state, leg_b=WM/register read) keeping param budget ~303M. Train on the 4-cell {ko,en}×{general,sns} corpus, held-out CE per cell + own-GEMM forge GPU. Verdict = engine-native G6 fals-rate + G1 recombination via `anima eval` (frozen bars H_1129/1140/1464). Ablation arm: same ckpt with K=1 at eval. Pre-reg success = G6 fals>0 AND G1 recombine≥303M-conv baseline while K=1 arm stays at FAIL. Est ~1 H100-day; fire only on explicit go.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).


## Measured Result (2026-06-30 · py 2-production engine · DIRECTIONAL)

**Training:** 9 CLMs (binder DROPPED at .clm serialize, additive readout). All 4/4 DESCENT (val_CE < 5.545) per arm/seed.

**G0-G6 results:**

| arm | seed | G0 n/5 | G0? | G1 best_distinct | G1 max_single | G6 dist | G6 fals | a7b? |
|-----|------|--------|-----|-----------------|---------------|---------|---------|------|
| asym | 7 | 2/5 | FAIL | 0 | 0 | 4 | 0 | FAIL |
| asym | 4302 | 2/5 | FAIL | 0 | 1 | 1 | 0 | FAIL |
| asym | 4303 | 2/5 | FAIL | 0 | 0 | 1 | 0 | FAIL |
| k1 | 7 | 2/5 | FAIL | 0 | 0 | 4 | 0 | FAIL |
| k1 | 4302 | 3/5 | FAIL | 0 | 0 | 2 | 0 | FAIL |
| k1 | 4303 | 1/5 | FAIL | 1 | 0 | 4 | 0 | FAIL |
| arm | 7 | 2/5 | FAIL | 0 | 1 | 4 | 0 | FAIL |
| arm | 4302 | 3/5 | FAIL | 0 | 0 | 2 | 0 | FAIL |
| arm | 4303 | 4/5 | PASS | 0 | 0 | 4 | 0 | FAIL |

**Verdict: 🔴 NOT-SUPPORTED** (DIRECTIONAL — py 2-production engine)

G1=0 across all main arms while the trunk CAN cohere (>=1 arm G0 PASS) — binder dropped at .clm serialize => additive readout; co-training insufficient for recombination. Note: main binding arm additionally DEGRADES G0 coherence (G0 PASS only in control arms).

**Scope:** binder dropped at serialize → this is trunk co-training effect only (not runtime binding). Same tier as EXP-3/H_1812/H_1814/H_1816. terminal verdict requires hexa engine-native re-run (a_engine_native_learning).
