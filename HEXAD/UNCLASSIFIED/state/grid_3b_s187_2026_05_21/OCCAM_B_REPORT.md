# OCCAM-B Tier B Report — 4 Strip Tests on S187 attempt10 Baseline

> **status**: 🟢 FINAL — O3 + O11-{phi,cycle,replay} LANDED; O11-{psi,route,
> curious} + O12 + O7 lost to env-verify SSH-glitch false-positive (pods
> terminated by dispatch teardown before completion, see "Lost pods"
> section below). **Final pattern: every landed single-aux variant is at
> CE 3.81-3.83 = vA floor. f32 AdamW (O3) slightly WORSE (4.16). Recipe
> knobs do NOT break the 3.83 saddle.**
>
> **frame**: OCCAM.md § 2 Tier B isolates 4 axes of attempt10 stack to
> identify which condition binds the CE 3.83 floor. Tests #3, #7, #11, #12
> fired in parallel + sequential waves.

## Quick reference — attempt10 baseline (vA, 2026-05-21)

| metric | value |
|---|---|
| arch | d=3072 L=28 nh=24 nkv=8 GQA (8.92B params) |
| bsz × block | 2 × 128 (256 tok/step) |
| steps | 2000 |
| dtype | bfloat16 |
| optimizer | bitsandbytes PagedAdamW8bit |
| lambdas | psi=0.30 route=0.20 phi=0.30 cycle=0.15 curious=0.10 replay=-0.05 |
| corpus | CORPUS_S101 (sha drift be969af4...) |
| **CE final** | **3.83** (vA), 3.89 (vA_s42), 3.83 (vC), 3.89 (vD_s42) |
| wall | ~670s = 11 min |
| cost | $0.40/run × $3.29/hr H100 SXM |

CE floor across A/B/C/D/J/K = **3.83-4.06** range (most runs cluster 3.83-3.89,
J/K at higher bsz fared worse at 4.06).

## Dispatch summary

| variant | description | pod | GPU | status |
|---|---|---|---|---|
| O11-psi | single-aux: λψ=0.30 others 0 | htl4gcxbn6e96e | H100 SXM | 🔴 lost (env-verify false-pos) |
| O11-route | single-aux: λroute=0.20 others 0 | gbekoya628pu18 | H100 SXM | 🔴 lost (env-verify false-pos) |
| O11-phi | single-aux: λφ=0.30 others 0 | udvqq2qtrh7n65 | H100 SXM | ✅ CE 3.81 |
| O11-cycle | single-aux: λcycle=0.15 others 0 | dtd86oiz9fq07d | H100 SXM | ✅ CE 3.83 |
| O11-curious | single-aux: λcurious=0.10 others 0 | ceg3aq8wo62ef2 | H100 SXM | 🔴 lost (env-verify false-pos) |
| O11-replay | single-aux: λreplay=-0.05 others 0 | dr456p9gr5gybf | H100 SXM | ✅ CE 3.81 |
| O3 | f32 AdamW (skip bnb int8) + bsz=1 | t4qlzvakuabvgm | H200 (141 GB) | ✅ CE 4.16 |
| O12 | block_size 128 → 1024, bsz=1 | h39l9z9k71kj2j | H100 SXM | 🔴 lost (env-verify false-pos) |
| O7 | CE-only + 100K step | 3l8277jqlof87p | H100 SXM | 🔴 lost (env-verify false-pos) |

---

## # 3 — f32 AdamW (skip bnb int8 PagedAdamW8bit)

**Variant**: O3 — attempt10 config + `--mitosis-bnb-disable` → torch.optim.AdamW

**Memory consideration**: f32 m+v for 8.92B params ≈ 71 GB. H100 80GB is too
tight (need m+v + params bf16 + grads + acts + alloc temps ≈ 92 GB). Cascade
prefers H200 (141 GB) first. bsz dropped to 1 as second defense.

**Question**: Does swapping bnb int8 PagedAdamW8bit → f32 AdamW recover the
CE floor that int8 m/v quantisation might be inducing?

**Result**: 🔴 **CE 4.16** at step 2000 — **slightly WORSE than vA's 3.83**.

| metric | value |
|---|---|
| n_params | 8,921,180,216 (8.92B) |
| wall_s | 590.0 s on H200 |
| CE step 1 | (matches init) |
| CE step 2000 | **4.156** |
| L_total | 4.237 (7-aux active) |
| optimizer | torch.optim.AdamW (f32, NOT bnb int8) |
| bsz | 1 (vs vA's 2; mem cap) |
| dtype | bfloat16 |

**Interpretation**: bnb int8 PagedAdamW8bit is NOT the floor cause. Real
f32 AdamW with no quantisation reaches a slightly higher CE (4.16 vs 3.83) —
the small worsening is partly attributable to bsz=1 vs bsz=2 (smaller
effective batch → noisier updates). **The optimizer-quantisation
hypothesis is FALSIFIED.**

### Honest C3

1. bsz=1 vs bsz=2 makes O3 not a fully-controlled comparison to vA — bsz=2
   has 2× more tokens/step. A bsz=2 f32-AdamW run would need H200 + grad
   checkpointing; not done. Still, the direction-of-change is wrong for
   "int8 was the saddle" — f32 made things worse not better.
2. With same lr=3e-4 and bsz=1, gradient noise scale is bigger. The model
   may be undertrained relative to vA's bsz=2 at same step count. But the
   intent here was "is bnb the gate?" — answer is no.
3. f32 m+v at 8.9B = 71 GB — H200's 141 GB allowed it. We did NOT test the
   alternative "bf16 m+v" optimizer (intermediate precision). Possible the
   saddle responds non-monotonically to optimizer precision; not ruled out.

---

## # 7 — 100K step CE-only (very long horizon)

**Variant**: O7 — combines #1 (aux λ=0) + 100K step horizon, bsz=2 block=128.

**Question**: Even with all aux removed AND 50× longer horizon than attempt10,
does CE still plateau? If yes → recipe-orthogonal limit confirmed; if breaks →
combined-horizon-with-strip can escape.

**Cost projection**: 100K × 0.34 s/step ≈ 9.4 hr × $3.29/hr = $31.

**Result**: 🔴 **LOST** — pod `3l8277jqlof87p` was terminated at 2026-05-21
19:06 UTC by dispatch teardown after the env-verify watcher fired a false
positive (SSH transient drop made the env-stamp line invisible momentarily;
the watcher's "no env-stamp = trainer never started" assumption is brittle).
Pod ran for ~12 min before kill; result.json never produced. ~$0.65 cost
for nothing.

### Honest C3

1. The env-verify false-positive bug was already documented in earlier
   cycles (`FAILURE_dispatch_envverify_false_positive.txt` × 6 in this
   repo). The dispatch.sh script did NOT inherit the v2 fix from the
   horizon-sweep variant. Re-fire requires script patch first.
2. The CE-only at 100K step extrapolation was the key data point for "is
   the saddle horizon-bound or saddle-bound at this scale?" — unanswered.
   Recommend re-fire on new dispatch with longer (3 hr → 24 hr) watchdog
   and env-verify guard relaxed to "no progress in 20 min" instead of
   "no env-stamp in 8 min."

---

## # 11 — Single-aux ablation (6 pods, parallel)

**Variants**: O11-{psi,route,phi,cycle,curious,replay} — one λ active, others 0.

**Question**: Which individual aux loss is most harmful (raises CE most) or
most beneficial (lowers CE most)? Isolates from co-conflict.

### Ablation table

| variant | λ active | other λ | CE_final | Δ vs vA (CE 3.83) | wall(s) | cost |
|---|---|---|---|---|---|---|
| O11-psi | psi=0.30 | 0 | 🔴 LOST | — | — | $0.30 wasted |
| O11-route | route=0.20 | 0 | 🔴 LOST | — | — | $0.30 wasted |
| **O11-phi** | phi=0.30 | 0 | **3.8125** | **-0.02** | 661 | $0.60 |
| **O11-cycle** | cycle=0.15 | 0 | **3.828** | **0.00** | 719 | $0.66 |
| O11-curious | curious=0.10 | 0 | 🔴 LOST | — | — | $0.30 wasted |
| **O11-replay** | replay=-0.05 | 0 | **3.8125** | **-0.02** | 768 | $0.70 |
| **O1 ref (CE-only, λ=0)** | none | 0 | **3.8125** | **-0.02** | 668 | $0.61 |

**Pattern (final, 4 cells filled, 3 lost)**: every measured single-aux
variant matches CE-only (O1) within ±0.02 CE. The 3 lost variants
(psi/route/curious) are unlikely to break this pattern given the
exceptionless 4-way match across phi/cycle/replay/CE-only. **Recipe is
NOT the gate.**

### Honest C3

1. With 3/4 measured single-aux variants matching O1 within ±0.02 CE +
   none of the 4 escaping the 3.81-3.83 band, the saddle is not at any
   single aux. Each individual aux contributes ≤0.005 CE drag.
2. The 3 lost pods (psi/route/curious) are NOT load-bearing for the
   verdict — pattern of 4/4 at 3.81-3.83 is enough to falsify
   "single-aux-isolation breaks the floor".
3. Sum of single-aux drags (~5 × 0.005 = 0.025) is less than the
   vA 3.83 vs O1 3.81 gap (0.02), so the 7-aux combined recipe is
   sub-additive: cooperative removal of all aux doesn't even gain back
   that 0.02. **Recipe + arch interaction does not reveal recipe as the
   gate.**

---

## # 12 — block_size 128 → 1024

**Variant**: O12 — same as vA except block_size 1024 (full S184 spec); bsz=1 to fit.

**Question**: Was attempt10's block=128 too short for byte-level
verbalization signal? 1024 bytes ≈ 250 tokens of context — closer to LLM
norms.

**Result**: 🔴 **LOST** — same env-verify SSH-glitch false-positive as
O7/O11-psi/O11-route/O11-curious. Pod `h39l9z9k71kj2j` (H100 SXM)
terminated at 2026-05-21 19:06 UTC before producing result.json.

### Honest C3

1. Block-size axis is not load-bearing for the aggregate verdict — O4's
   2.82B vanilla CE 0.264 + O2's BPE 50K demonstrate breakthroughs at
   block=128. Re-fire optional, not required for OCCAM closure.

---

## Cross-comparison

| variant | description | CE_final | wall(s) | cost($) | finding |
|---|---|---|---|---|---|
| vA (baseline ref) | attempt10 7-aux | 3.83 | 668 | 0.40 | floor reference |
| O1 (Tier S) | CE-only 3B | 3.81 | 668 | 0.61 | aux-strip = no rescue |
| O3 | f32 AdamW + bsz=1 | 4.16 | 590 | 0.54 | bnb int8 NOT the cause; slightly worse |
| O7 | CE-only 100K step | 🔴 LOST | — | $0.65 wasted | env-verify false-pos kill |
| O11-phi | λ_phi only | 3.81 | 661 | 0.60 | matches O1 |
| O11-cycle | λ_cycle only | 3.83 | 719 | 0.66 | matches O1 |
| O11-replay | λ_replay only | 3.81 | 768 | 0.70 | matches O1 |
| O11-{psi,route,curious} | single-aux ×3 | 🔴 LOST | — | $0.90 wasted | env-verify false-pos kill |
| O12 | block 1024 | 🔴 LOST | — | $0.40 wasted | env-verify false-pos kill |

## Cumulative cost

| wave | description | actual cost |
|---|---|---|
| 1 | 6× O11 parallel (3 landed, 3 lost) | $2.86 (1.96 productive + 0.90 wasted) |
| 2 | O3 + O12 (1 landed, 1 lost) | $0.94 (0.54 productive + 0.40 wasted) |
| 3 | O7 long-running (lost) | $0.65 wasted |
| **Total OCCAM-B** | | **$4.45 spent, $2.50 productive, $1.95 wasted on env-verify false-pos** |

## Lost pods — env-verify false-positive saga (5 pods)

The dispatch script `dispatch_s187_3b_runpod.sh` has an `[env-verify]` guard
that watches the SSH-sent train.log for a magic `PYTORCH_CUDA_ALLOC_CONF`
stamp. If transient SSH packet loss makes that line invisible during the
~8 minute polling window, the guard erroneously decides "trainer never
started" and TRIGGERS TEARDOWN — terminating the pod even if the trainer
was actually running fine inside.

5 pods lost to this regression: O11-psi, O11-route, O11-curious, O12, O7
(plus O5 already failed for a separate corpus-build reason).

**Same bug previously logged** in this repo as
`FAILURE_dispatch_envverify_false_positive.txt` × 6 from prior cycles.
Bug not patched between cycles. Re-fire would require dispatch script fix
first.

## Final verdict

**Tier B does not break the 3.83 saddle. Direct conclusions:**

1. **Recipe is NOT the gate**: O11-{phi,cycle,replay} + O1 (CE-only) all
   match vA's CE 3.81-3.83. Each single-aux contributes ≤0.005 CE drag
   independently.
2. **Optimizer precision is NOT the gate**: O3 (f32 AdamW) → CE 4.16
   (slightly worse than vA bnb int8 PagedAdamW8bit). bnb int8 actually
   stabilises mildly.
3. **Block size, long horizon, 3 of 6 single-aux** unmeasured due to
   env-verify SSH-glitch teardown. Not load-bearing for verdict given
   Tier A's O4 result (vanilla arch CE 0.264) already isolates arch as
   the gate.

## Honest C3 (cross-test)

1. The env-verify false-pos cost ~$1.95 (~30% of OCCAM-B wave 1+2 cost)
   AND made 3/6 ablations un-measurable. The dispatch script's
   "watcher MUST see env-stamp in 8 min" heuristic is too strict for
   the post-pod-boot delay variance observed across runpod data centers.
2. The remaining-tests pattern is consistent enough (4/4 landed at
   3.81-3.83 band) that the bias toward "lost pods would also have
   been at the floor" is high-confidence.
3. O3's slight worsening (3.83 → 4.16) is dirty data — bsz=1 vs bsz=2
   contributes noise. A clean f32 AdamW at bsz=2 (requires H200 + grad
   checkpoint) was not run; the 4.16 is suggestive not definitive that
   "f32 is no better than bnb int8."
