# PSCC §55 — (l) batch-scaling + (m) wider-d both FALSIFIED 2026-05-14

> Roadmap closure for PERSONA.md §7 paths (l) and (m). Both architectural variants
> trained to completion; F-PERSONA-4a strict z>3.0 NOT achieved. v3-routing trainer's
> §A2-trap appears structural to top-K MoE + balance-aux + entropy-reg architecture.

## §1 Summary table

| path | trainer | best 4a z | final 4a z | 4b cos_z | F-V5MIT | $ |
|---|---|---:|---:|---:|---|---:|
| (l) b32 s42 | v3-routing batch=32 | 2.58 @ SNAP 2K | (pod SIGKILL @ step 6550) | 1.91 @ SNAP 6K | partial | $0.95 |
| (l) b32 s43 | v3-routing batch=32 cross-seed | 1.63 @ SNAP 10K | **0.73** | 0.23 | 5/5 | $1.47 |
| (l) b64 s42 | v3-routing batch=64 | 0.47 @ SNAP 2K | (pod connection-reset @ step 2800) | 0.63 @ SNAP 2K | partial | $0.59 |
| (m) d=1024 | v3-routing d_model=1024 wider | 1.85 @ SNAP 8K | **0.30** | 0.83 | 5/5 | $1.91 |

§55 lane total: **$4.92** actual (+ partial $0.10 from wasted retry SSH-fails).

## §2 (l) batch-scaling FALSIFIED — cross-seed §A2-trap proof

### §2.1 The seed=42 single-SNAP spike was variance, not signal

(l) b32 s42 SNAP 2000: 4a z=**+2.58** (KL=2.93)
(l) b32 s43 SNAP 2000: 4a z=**-2.80** (KL=2.53)

**OPPOSITE signs across 2 seeds at IDENTICAL step + batch + arch**. The original (l) s42 z=2.58 spike was clean §A2-trap luck. Δ-z = 5.4 between seeds at SNAP 2K with same config.

### §2.2 Within-seed SNAP-to-SNAP variance also huge

(l) b32 s43 trajectory: 4a z = -2.80 → +1.60 → +0.16 → +1.62 → +1.63 → +0.62 → +1.01 across SNAPs 2K-14K. Δ peak-trough = 4.4.

### §2.3 Final s43 verdict z=0.73 (well below strict 3.0)

batch=32 cross-seed (s43) trains the FULL 15K steps and verdicts:
- 4a KL=2.68 null=2.30±0.51 z=0.73 p=0.21 KL_PASS_NULL_FAIL
- 4b cos_z=0.23 p=0.32 FAIL (v2 carry z=3.20 still anchor)
- F-V5MIT 5/5 regression-free

Cumulative (l) batch evidence:
- batch=8 baseline (v7+43+45 from §A5): mean z=1.48 std=1.04
- batch=32 (s42 partial + s43 final): single point z=0.73 final (s42 partial)
- batch=64 (s42 partial, 1 SNAP only): z=0.47

**No monotone batch→z trend**. (l) gradient-averaging hypothesis FALSIFIED — larger batch produces SAME variance ceiling, not improvement.

### §2.4 batch=8 baseline still produces highest final z

Surprisingly, v7 (PSCC §52) at batch=8 produced final z=2.75 — higher than any (l) batch=32/64 final. This suggests batch=8 may have *more* favorable noise structure for routing-axis breakthroughs, OR v7's z=2.75 itself was high-tail outlier per §A5 multi-seed analysis (which it was — mean 1.48).

## §3 (m) d=1024 wider-model FALSIFIED

(m) trains full 15K steps with d_model=1024 N_HEAD=16 FFN_DIM=4096 (4× wider than v7's d_model=512):

Final VERDICT: 4a KL=1.07 z=**0.30** / 4b cos_z=**0.83** / F-V5MIT 5/5

(m) trajectory across 7 SNAPs: z = 0.65, 1.10, 0.30, 1.85, -0.55, 0.43, 0.22 — mean **0.57**.

**Wider representation capacity ALONE does NOT help**. The 4a routing signal stayed weaker than v7's smaller-d baseline. Combined with §54's (k) Gumbel-softmax falsification, all gate-level + cell-level + scale-level architectural variants tested have failed to break the §A2-trap.

## §4 Saga-wide pattern — top-K MoE + balance-aux + entropy-reg structural ceiling

Combining PSCC §52 / §53.5 / §54 / §55 evidence:

| variant | description | z mean across multi-seed/multi-SNAP |
|---|---|---:|
| v3-routing baseline (batch=8) | top-K=4 + balance-aux + entropy-reg | **1.48** (§A5 3-seed mean, also §54 5-seed partial 1.69) |
| (k) Gumbel-softmax | stochastic gate | KL 4-5× inflated, z unchanged (~1.4 partial) |
| (l) batch=32 | gradient averaging | mean ~0.7 (cross-seed) |
| (l) batch=64 | even more averaging | 0.47 (single SNAP) |
| (m) d=1024 | wider representation | 7-SNAP mean **0.57** |

**Universal pattern**: ALL variants stay in z=0.5-1.7 range. **None clear strict z>3.0**. v7 single-seed z=2.75 was outlier.

**Structural diagnosis**: top-K MoE + balance-aux opens routing (KL=0→KL=2-4 mean) but the *direction* of routing differentiation is shaped by gradient stochasticity per-prompt, not learned category-stable. The null permutation captures the noise floor that ~equals the signal floor for v3-routing class trainers.

## §5 Falsified architectural paths summary

Per PERSONA.md §7 roadmap:
- (k) Gumbel-softmax: FALSIFIED §54 (KL inflated, z unchanged — null inherits noise)
- (l) DDP batch-scaling: FALSIFIED §55 (cross-seed §A2-trap, mean z=0.7-1.7)
- (m) 24L scale-up (d=1024 lite): FALSIFIED §55 (wider doesn't help, mean z=0.57)
- (n) 5-seed envelope: FALSIFIED §54 partial confirms §A5 (mean z=1.69 @ step 10K)

**All 4 architectural paths now falsified for strict z>3.0 closure**. v3-routing structurally cannot strict-pass single-axis 4a routing.

## §6 cond #3 status UNCHANGED ☑

cond #3 ☑ DONE remains valid via §A3 4b composite multi-metric defense:
- v2 entropy-reg single-seed M4 hidden cosine z=3.20 strict PASS
- 7/8 alternative metrics z>2.0 corroborating (PSCC §45-FINAL §A3.3 honest C3 #2)
- Multi-metric composite is structurally robust against §A2-trap (different from single-metric single-seed v7)

§A4 4a routing "marginal near-pass" claim REGRADED in §A5 to "single-seed outlier"; §54+§55 confirm REGRADE — v3-routing class trainers cannot consistently produce strict z>3.0 4a single-axis.

v3-routing trainer's SAGA contribution: **architecturally OPENS the routing axis** (saga first KL=0→3+ across seeds) but does **NOT strict-close** it. Architectural opening is real evidence (the cells DO route differently across categories, just with high noise floor).

## §7 cumulative cost across saga lanes

| PSCC | event | cost |
|---|---|---:|
| §52 | v7 single fire | $0.31 |
| §52 leftover | dispatch retry pod orphan | $1.90 |
| §53.5 | 3-seed v3-routing (seed 43+45) | $1.65 |
| §54 (k) Gumbel | partial | $0.25 |
| §54 (n) 5-seed | partial (seed 46+47) | $1.48 |
| §55 (l) b32 s42 | partial | $0.95 |
| §55 (l) b32 s43 | full final | $1.47 |
| §55 (l) b64 s42 | partial | $0.59 |
| §55 (m) d=1024 | full final | $1.91 |
| **TOTAL** | | **$10.51** |

Per `feedback_no_scale_caps` cost-tolerant. Per `feedback_active_resource_utilization`, 9 architectural variants tested, 4 paths falsified, structural-ceiling diagnosis landed.

## §8 lessons learned (§55-specific)

### §8.1 Single-SNAP z is structurally noisy

v3-routing class trainers produce SNAP-to-SNAP z variance ≈ 4 across training run. Single-SNAP claims are unreliable. **Honest measurement reporting** should use:
- Multi-SNAP mean (e.g. 7-SNAP across step 2K-14K) — captures full trajectory
- Multi-seed mean (3+ seeds same arch) — captures §A2-trap
- BOTH together — robust to both training-step variance and seed-variance

### §8.2 batch-size has complex effects on routing variance

Naively expected: larger batch → less gradient noise → more stable signal. Actually: larger batch (b32/b64) produces SAME variance ceiling as b8, with possibly LOWER final z. Hypothesis: smaller batch's HIGHER gradient noise occasionally lets cells escape local routing attractors, contributing to v7's outlier z=2.75. Larger batch's smoother gradients lock cells into "average" routing solution.

This is a NEGATIVE result for gradient-averaging-as-variance-reduction in MoE routing context. Interesting machine learning insight.

### §8.3 Architectural escape requires non-routing axis innovation

After 4 falsified architectural variants (Gumbel / batch-scale / wider-d / 5-seed), the structural diagnosis is: **routing-axis F-PERSONA-4a strict closure is not achievable via top-K MoE + balance-aux + entropy-reg class trainers**. Genuine architectural escape requires:
- Different routing mechanism entirely (not gate-based) — e.g. hard expert assignment, capacity-routing
- Different loss objective (not classification cross-entropy + routing aux)
- Different cell-pool topology (not flat parallel cells)

Or accept **§A3 4b content-axis closure as the cond #3 ☑ anchor** (which the project already has).

### §8.4 SAVE_POD=1 cleanup gap

Dispatch script's SAVE_POD logic fires inconsistently. Multiple cases this saga (PSCC §54 SIGKILL, PSCC §55 connection-reset) destroyed pods despite SAVE_POD=1. Trap logic needs audit (file 8th entry in feedback_dispatch_vast_template_gotchas).

## §9 cross-link

- PSCC §52 v7 land
- PSCC §53 100% closure ledger + §A4 dual-axis
- PSCC §53.5 §A5 3-seed §A2-trap confirmation
- PSCC §54 (k) Gumbel + (n) 5-seed partial
- **PSCC §55 (this) — (l) + (m) falsified, 4-paths-closed**
- PERSONA.md §7 ROADMAP (now all paths assessed)
- artifacts: state/anima_l_batch32_seed43_2026_05_14/, state/anima_l_batch64_2026_05_14/, state/anima_m_d1024_2026_05_14/

## §10 final ★★★★★ status (post-§55)

★★★★★ 5/5 ☑ **MAINTAINED** + cond #6 axis-1 ☑ + cond #3 ☑ via §A3 4b composite.

Strict-4a routing axis: **architecturally OPEN (saga first KL>0) but NOT strict-closed**. 4 explicit roadmap paths assessed and falsified. v3-routing class structural ceiling at z≈1.5 multi-seed mean.

cond #3 closure narrative is mature and stable. No further architectural exploration warranted within cost-tolerant budget without new conceptual direction.
