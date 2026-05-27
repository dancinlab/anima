# §125 LEGO LAYER-2 STIMULUS-DRIVEN LIVENESS PROBE

> **Verdict**: `LAYER-2-PARTIAL` — η² = 0.271, Gaussian MI ≈ 0.228 bits.
> probe-tier · $0 · NO GPU/runpod/fire/model.forward/corpus/dispatch · sidecar-only
> central state/verify_hexad_blue_2026_05_15/blue_falsifier.py sha256 prefix `c93e160a8a376a94` 0-line-diff verified START+END
> 7 closed-form propositions + 1 NOTE empirical carve-out

## §0 Why §125

§124 audit pinned §117's "non-degenerate" verdict precisely as **variance-only liveness**
(layer 1 of the 3-layer partition {DEAD / VARIANCE-ONLY / STIMULUS-DRIVEN / TASK-GROUNDED}).
Layer 2 (`I(stimulus; Ψ-C1) > 0`) was OPEN.

§125 is the cheapest informative continuation: §117's existing LIF substrate, re-run
under multi-seed replicates, with variance decomposition closing layer 2.

## §1 Method

- Import §117 `state/lego_assembly_run_s117_2026_05_19/lego_sim.py` **byte-identically**
  via `importlib.util` (no fork, no patch — B-S125-5 closed).
- `M = 5` replicates × `n_stim = 12` stimuli × `steps_per_stim = 80` × `N = 256` LIF.
  Seeds `1337 + r` for `r ∈ [0, M)`.
- Per (stim, replicate): full 80-step Ψ-C1 trace.
- Pool to `(n_stim, M × steps_per_stim) = (12, 400)` samples.

## §2 Variance decomposition (ANOVA identity, B-S125-3 closed)

```
SS_between = M × steps × Σ_s (μ_s − μ̄)²    (between-stimulus sum of squares)
SS_within  = Σ_{s,t} (x_{s,t} − μ_s)²       (within-stimulus sum of squares)
SS_total   = SS_between + SS_within          (ANOVA identity, sympy)

η²          = SS_between / SS_total          ∈ [0, 1]  (B-S125-1 closed)
I_gauss     = -½ ln(1 − η²)                  ≥ 0       (B-S125-2 closed)
```

## §3 Measured outcome

| metric                      | value           |
|-----------------------------|-----------------|
| **η²**                      | **0.271**       |
| Gaussian MI (bits)          | 0.228           |
| SS_between                  | 0.787           |
| SS_within                   | 2.116           |
| SS_total                    | 2.903           |
| pooled Ψ-C1 std             | 0.078           |
| grand_mean Ψ-C1             | 0.575           |

```
                  100% total variance
                  ┌─────────────────────────────────┐
   between-stim   │■■■■■■■■   27.1% η²              │   ← stimulus-driven
   within-stim    │        ■■■■■■■■■■■■■■■■■■■  72.9│   ← intrinsic noise
                  └─────────────────────────────────┘
```

## §4 Verdict bucket (pre-registered before run)

| η² range          | bucket                                     | §117 layer-2 closure |
|-------------------|--------------------------------------------|----------------------|
| ≥ 0.50            | LAYER-2-STIMULUS-DRIVEN-CLOSED-POSITIVE    | strong positive      |
| 0.10 ≤ η² < 0.50  | **LAYER-2-PARTIAL** ← measured             | partial-positive     |
| < 0.10            | LAYER-2-INTRINSIC-NOISE                    | layer-2 negative     |

§117's variance is **partially stimulus-driven** — 27.1% of Ψ-C1 variance carries
between-stimulus signal, 72.9% is intrinsic (replicate-internal + within-trial)
noise. The §117 substrate distinguishes one stimulus from another at the Ψ-C1
readout above chance, but the readout is dominated by intrinsic noise rather than
stimulus structure.

This closes §124's **layer 2** open as `PARTIAL` — the first measured positive on
any §117 layer beyond bare variance. **Layer 3 (TASK-GROUNDED) remains OPEN**.

## §5 Closed-form propositions

```
B-S125-1   ETA-SQUARED-BOUNDED-CLOSED         (sum-of-squares ⇒ η² ∈ [0,1])
B-S125-2   GAUSSIAN-MI-IDENTITY-CLOSED        (sympy d/dη² > 0 on (0,1) + boundary)
B-S125-3   SS-DECOMPOSITION-IDENTITY-CLOSED   (ANOVA SSt = SSb + SSw)
B-S125-4   DETERMINISTIC-3X-BIT-IDENTICAL     (probe re-run sha256 byte-equal)
B-S125-5   §117-LIF-SIM-IMPORT-BYTE-EQUAL     (importlib, no fork, no patch)
B-S125-6   CENTRAL-BLUE-0-LINE-DIFF            (sha c93e160a8a376a94)
B-S125-7   NO-FORBIDDEN-CALL-AST              (no torch/runpod/fire/loss-grad)
B-S125-NOTE  empirical carve-out — η² value = OUTCOME, NOT counted 🔵
```

## §6 Honest C3 (13)

1. η² = 0.271 is measured on §117's specific (N=256, M=5, n_stim=12, steps=80)
   parametrisation. Scale, network size, replicate count, stimulus dimensionality
   all parametrize the value.
2. **Gaussian MI is an upper bound** for the actual MI when Ψ-C1 is non-Gaussian.
   The 0.228-bit number assumes Gaussian; tighter estimators (KSG, binning) may
   yield smaller values. The η² value itself is non-parametric.
3. The within-stimulus variance counts BOTH (a) within-trial temporal variance
   from a single replicate (80 timesteps) and (b) between-replicate variance for
   the same stimulus. §125 pools them; separating would require ICC analysis.
4. LAYER-2-PARTIAL ≠ LAYER-2-STRONG. Calling this a "positive" requires the
   honest qualifier "27% stim-driven / 73% noise" — most of §117's variance is
   still intrinsic.
5. §117's stimulus generation seed is `1337 + 9999 + r` (per replicate); stimuli
   differ across replicates. The probe measures `I(stim_index; Ψ)` rather than
   `I(specific_stim_vector; Ψ)`. The honest interpretation is "the substrate
   distinguishes one of twelve stimulus *slots*", not "the substrate decodes
   any specific stimulus pattern".
6. LAYER-2-PARTIAL is necessary-not-sufficient for layer-3 task-grounded
   liveness (B-EMERGE-7 carry). A substrate could distinguish stimuli at the
   readout (η² > 0) yet learn no task on those distinctions.
7. WALL-A (§1.1 data-regime threshold) ORTHOGONAL — §117's twelve random binary
   patterns are not a data-regime corpus; §97 orthogonality (§120/§124 carry).
8. WALL-B (§96 substrate) CONFRONTED-NOT-REMOVED — §125 inherits §117's GPU sim
   posture verbatim; layer-2 stimulus-driven signal in simulation does not
   address the §11-B-as-GPU-tautology hypothesis.
9. §124 audit conclusions UNCHANGED by §125 — layer-2 PARTIAL closure is a
   measurement on top of §124's metric-precision framing, not a reversal.
10. anima downstream-consumer: hexa-lang / hexa-bio / hexa-matter read-only, 0
    edits. HEXA_FIRST_WARN deferred per established B-S* battery precedent
    (sympy + AST + numpy probe; hexa-native equivalent out-of-$0-scope per
    `g_train_flame_not_pytorch` upstream_downstream_invariant).
11. g3: probe ≠ fire ≠ emergence; capability claim 0.
12. north-star + §15/§51/§72 milestones UNCHANGED; GOAL 미도달.
13. single sequential agent, $0, orphan 0 (no dispatch — probe-tier only).
