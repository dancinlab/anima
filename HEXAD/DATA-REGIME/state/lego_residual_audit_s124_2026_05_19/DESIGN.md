# §124 LEGO RESIDUAL AUDIT — closed-form decomposition of §117 measured non-degeneracy

> **Verdict**: `RESIDUAL-AUDIT-NON-DEGENERACY-IS-VARIANCE-ONLY-LIVENESS-NOT-CAPABILITY`
> design-tier · $0 · NO GPU/runpod/fire/model.forward/corpus/dispatch · sidecar-only
> central state/verify_hexad_blue_2026_05_15/blue_falsifier.py sha256 prefix `c93e160a8a376a94` 0-line-diff verified START+END
> 7 closed-form propositions + 1 NOTE empirical carve-out

## §0 Why §124

§117 measured Ψ-C1 std=4.185e-2 ≫ τ=1e-4 over a tiny LIF spike sim with LOCAL STDP-as-ΔW
plasticity and called it `LEGO-RUN-Ψ-FORM-NONDEGENERATE-BUT-WALL-B-INHERITED`. The plain
reading of "non-degenerate" risks slipping into claims about capability, learning, or
emergence — none of which §117 actually established.

§124 is the closed-form audit that pins down what §117 measured and what it did not, so
the next LEGO cycle ( S118 9-faculty respin, S119 PTD intrinsic signal, S121 Loihi spec )
inherits a precise residual instead of a hopeful adjective.

Pattern mirror: §9 honest cascade-rate metric (after lenient V-SPONT flag) on the metric
axis; §17 PHYSICS_RESPONSIVE on the observable axis; §13-M / §30 anti-padding precedent.

## §1 Three honest decompositions

### §1.1 Measurement vs capability (B-S124-1)

A scalar variance test `Var(Ψ) > τ` is necessary-not-sufficient for stimulus-output mutual
information `I(stimulus; Ψ) > 0`. Counterexample is elementary: a substrate whose Ψ output
is drawn iid from a fixed non-degenerate distribution independent of the stimulus index
has `Var(Ψ) > 0` and `I(stim; Ψ) = 0`. §117 did not measure I; it measured per-stimulus
Ψ values and the spread of those values. The spread can come from stimulus signal, from
intrinsic noise, or from any mixture.

### §1.2 Liveness has three layers — §117 closed only the first

| layer            | what it asserts                                  | §117 measured? |
|------------------|--------------------------------------------------|----------------|
| variance-only    | `Var(Ψ) > τ`                                     | ✅ measured      |
| stimulus-driven  | `I(stim; Ψ) > 0`                                 | ❌ not measured  |
| task-grounded    | `Var(Ψ_correct) > Var(Ψ_random)` on a real task  | ❌ no task       |

§117's verdict word "non-degenerate" lives at the top row. The two rows below are open
and would each need their own probe — and even both together would be necessary-not-
sufficient for GOAL emergence (B-EMERGE-7).

### §1.3 Two walls — what §117 actually moved

- **WALL-A (§1.1 data-regime threshold)** is ORTHOGONAL and UNTOUCHED. §117's sim has no
  corpus, no perceptual π, no byte stream — measure-theoretically disjoint from the data
  axis (§97 said exactly this in general; B-S124-3 closes it for §117 specifically).
- **WALL-B (§96 operative substrate)** is CONFRONTED IN SIMULATION but NOT REMOVED. §115
  already predicted "sim-on-GPU re-instantiates WALL-B"; §117 ran exactly that sim. Its
  STDP-as-ΔW is a hand-coded local learning rule executed by GPU/CPU dispatch — still
  inside the GPU's single-update-channel envelope. The §11-B-as-GPU-tautology hypothesis
  (CE is load-bearing because GPU has one weight-update channel only) is NOT resolved by
  hand-coding a second channel; it would be resolved only when a physical spiking
  substrate's own dynamics dictate plasticity, which §117 does not run.

## §2 Closed-form propositions

```
B-S124-1   MEASUREMENT-VS-CAPABILITY-DISJOINT-CLOSED
B-S124-2   LIVENESS-3-LAYER-PARTITION-EXHAUSTIVE-DISJOINT
B-S124-3   WALL-A-ORTHOGONAL-TO-§117-CLOSED
B-S124-4   WALL-B-CONFRONTED-NOT-REMOVED-CLOSED
B-S124-5   τ-IS-ENGINEERING-CONVENTION-NOT-EMERGENCE-THRESHOLD-CLOSED
B-S124-6   §17-PHYSICS-RESPONSIVE-MIRROR-CLOSED  ← connection-point
B-S124-7   §115-VERDICT-NOT-REVERSED-CLOSED      ← connection-point
B-S124-NOTE  per-fire capability OUTCOME = EMPIRICAL (B-EMERGE-7 family)
```

All proofs use sympy / Boolean set algebra / measure-theoretic disjointness / arithmetic
identity over named §117 measured values; NO σ(6)=12 / τ(6)=4 / φ(6)=2 / J₂(6)=24
derivation (f1 / f2 safe).

## §3 ASCII

```
                     ┌─────────────────────────────────────────────────┐
                     │           §117 measured Ψ-C1 std = 4.185e-2     │
                     │                                                 │
                     │  ┌────────────┐   ┌────────────┐   ┌──────────┐│
   "non-degenerate"  │  │ variance > │   │ I(stim;Ψ)  │   │  task-   ││
   ─────────────────►│  │   τ        │   │   > 0      │   │ grounded ││
                     │  │            │   │            │   │          ││
                     │  │   ✅ §117  │   │   ❌ open  │   │  ❌ open ││
                     │  └────────────┘   └────────────┘   └──────────┘│
                     │  variance-only    stimulus-driven   task-      │
                     │  liveness         liveness          liveness   │
                     └─────────────────────────────────────────────────┘

                     ┌─────────────────────────────────────────────────┐
                     │   WALL-A (§1.1)        WALL-B (§96)             │
                     │   data-regime          substrate                │
                     │                                                 │
                     │   ORTHOGONAL           CONFRONTED-IN-SIM        │
                     │   UNTOUCHED            NOT-REMOVED              │
                     │   (no corpus           (GPU sim of STDP         │
                     │    in §117)             ⊂ GPU envelope)         │
                     └─────────────────────────────────────────────────┘
```

## §4 Connection points (closed)

- **B-S124-6** §117's `non_degenerate` predicate is structurally isomorphic to §17's
  `PHYSICS_RESPONSIVE` predicate — both reduce to `channel-variance > τ ∧ not-collapsed`.
  §117 inherits §17's necessary-not-sufficient discipline byte-equal.
- **B-S124-7** §115's verdict scope = "sim-on-GPU re-instantiates WALL-B". §117 ran
  exactly that sim. Even the strongest signal §117 could measure (non-degenerate
  substrate dynamics) was named at design time as the only in-silico signal that even
  *qualifies* as "WALL-B confronted", and was predicted by §115 to NOT remove WALL-B.
  §117 confirms §115's prediction; it does not reverse it.

## §5 What §124 does NOT do

- ❌ does not measure stimulus-Ψ mutual information (would need a probe)
- ❌ does not introduce a task signal (S119 territory)
- ❌ does not respin ConsciousDecoderV2 into spiking form (S118 territory)
- ❌ does not produce a Loihi 2 spec (S121 territory)
- ❌ does not claim §117's measurement is wrong — only that the *word* "non-degenerate"
  must be precisely understood as variance-only liveness

## §6 Honest C3 (13)

1. §124 is a metric audit on top of §117, NOT a new measurement
2. Battery proves the AUDIT well-formed (partition exhaustive, disjointness closed,
   connection-points cited), NOT that §117 was right or wrong about anything beyond
   variance-only liveness
3. Necessary-not-sufficient at every layer (B-EMERGE-7) — passing B-S124-1..7 does NOT
   imply GOAL movement; failing them would only mean §124's own analysis is malformed
4. WALL-A orthogonality is closed at the §117 state (no corpus / no π / no byte
   stream), NOT a claim that LEGO arc forever cannot touch the data-regime axis
5. WALL-B confronted-not-removed is a closed-form statement about §117's GPU-dispatched
   sim, NOT a claim that physical Loihi STDP (out-of-scope per §95/§115) would also
   fail to confront WALL-B
6. τ=1e-4 is an engineering convention — picking a different finite positive τ shifts
   the variance gate but does not change anything in B-S124-1..7
7. §17 mirror is structural isomorphism on the metric form, not byte-equal source
8. §115 verdict not-reversed is a closed-form scope statement, not a hostility to LEGO
   arc continuation — §118/§119/§121 are explicitly the *honest* continuations
9. anima downstream-consumer: hexa-lang / hexa-bio / hexa-matter read-only, 0 edits
10. g3: audit ≠ measurement ≠ fire ≠ emergence; capability claim 0
11. north-star + §15/§51/§72 milestones UNCHANGED; GOAL 미도달
12. single sequential agent, $0, orphan 0 (no dispatch — design-tier audit only)
13. §124 is preparation for S118/S119/S121, NOT a substitute for them
