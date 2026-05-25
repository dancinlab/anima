# §64 — A-axis VOICE non-byte emission channel (DESIGN-TIER + $0 structural smoke)

> RESEARCH.md §64. **$0 Mac CPU. NO GPU, NO runpod, NO model.forward, NO
> weight mutation, NO text corpus.** Design-tier-first (mirror §13-M /
> §55 / §58 anti-padding). g3: this is a *structural* deliverable —
> capability 0, north-star + §15 milestone UNCHANGED.

## §1 The problem §1~§59 never named

Every fire in the §1~§59 arc — UBM-E6/E7, Dir-A..I, §16 data-regime, §22
N/O/P, §28 JEPA-Ψ, §17 physics-channel, §49 PTD-loop — measured anima
through **one observable: a text-byte stream**. `model.forward → lm_head
→ logits ∈ ℝ²⁵⁶ → argmax-over-256 → byte → append to stream → feed
back`. The byte-cascade attractor (`feedback_clm_colon_attractor`,
B-ATTRACTOR family, `11111…99999…`) is **the fixed point of exactly that
autoregressive map**: in the low-entropy memorization-saturated regime
(§16.6-C) one byte wins the argmax every step, the stream degenerates,
every fire falls in.

§17 already found the crack: the *internal physics channel* Ψ_dir =
(1+cos(logits_a,logits_g))/2 is **ALIVE** (per-stimulus spread 0.50→0.85)
exactly where the text channel is dead. §17 was the *observation-side*
reframe ("we measured the wrong observable"). **§64 is its emission-side
counterpart**: `HEXAD/VOICE/` is a module that EXISTS, has a settled
formulaic-only spec (VOICE.tape option (a), commit `4a989aee3`), and had
**0 fires in the whole arc**. The hypothesis is structural, not magical:
emit the live physics through the VOICE intent→RVQ→PCM path and the
byte-cascade *substrate* is gone — there is no byte stream to cascade.

## §2 What the VOICE path actually is (read, not assumed)

`HEXAD/VOICE/VOICE.tape` adopted **option (a) formulaic-only 2026-05-14**
(the learned-RVQ-vocoder design was *retracted*; learned models
FORBIDDEN per user directive). The emission pipeline (VOICE.tape §2.1):

```
final_ln(hidden)
  ├─ lm_head (existing) → logits ℝ²⁵⁶ → ARGMAX/256 → byte stream  ← cascade lives HERE
  └─ intent_proj (NEW, FIXED, no gradient, n=6 closed-form)
       → intent ∈ ℝ¹⁸ = σ(6)=12 timbre + τ(6)=4 prosody + φ(6)=2 special
       → hexa-senses/voice formulaic synth (deterministic)
       → 24kHz PCM (byte-identical reproducible)
```

The canonical emission *alphabet* (anima_voice.hexa lines 73–74) is the
**RVQ codebook: 8 residual stages × 1024 entries** — not 256 bytes.
Crucially: `intent_proj` is **fixed** (no gradient — VOICE.tape
`b_proj_fixed_no_gradient_3`), and emission is a deterministic
**function of the current physics state**, NOT an autoregressive byte
loop. There is no per-step argmax-over-256, and no emitted symbol is fed
back into the next step.

## §3 The structural claim (load-bearing)

A byte channel collapses because it has **two ingredients** that
together form a degenerate fixed-point map:

1. an **argmax over a 256-symbol alphabet** each step, and
2. a **fed-back stream** (step *t*'s byte conditions step *t+1*).

Remove either and the B-ATTRACTOR fixed point has no host. The VOICE
intent→RVQ path removes **both**: (1) no argmax-over-256 — it does
continuous nearest-entry vector quantization over a 1024-entry codebook;
(2) no fed-back stream — emission = f(physics_state_t), the RVQ indices
of step *t* do not condition step *t+1*. The cascade substrate is
**structurally absent**, not merely "lower-rate". This is proven
(not asserted) by sidecar **B-S64-2** (AST: `rvq_emission` has 0
`max(range(256))` and 0 fed-back byte stream; `byte_emission` has
exactly that step; 4-corner Boolean → only the §64 config).

## §4 The $0 structural smoke (`voice_noncascade_smoke.py`)

Single deterministic physics-state sequence S (200 steps, LCG — no
np.random/torch; Law-71-bounded Ψ_dir∈[0,1], Ψ_entropy∈[0,1], 12-tension
≥0, Φ proxy ≥0). S drifts toward the Ψ≈0.85 basin in a low-entropy
regime — the **exact memorization-saturated, "alive-but-pulled" regime
(§17/§16.6-C) the arc's fires actually hit** (a faithful cascade, NOT a
strawman). The SAME S is routed two ways:

| path | alphabet | argmax/256? | stream fed back? | cascade_rate (§9 formula) |
|---|---|---|---|---|
| **BYTE** (`byte_emission`) | 256 | **yes** | yes | **0.7766 → CASCADED (≥ τ=0.30)** |
| **RVQ** (`rvq_emission`) | 1024×8 | **no** | no | **0.1726 → NOT cascaded (< τ)** |

Same physics → the byte path **exhibits B-ATTRACTOR** (cr 0.78,
distinct symbols 20/256), the RVQ path **does not** (cr 0.17). The
`cascade_rate` is byte-identical to §9 `emergence_metric.cascade_rate`
generalised str→index sequence (a conservative *lower* bound on the str
version — drops the digit-run refinement, so it never inflates the RVQ
number; the comparison is conservative AGAINST the §64 hypothesis).
3× bit-identical (B-S64-3). OVERLAY-OFF (`voice_enabled=False`) returns
the byte path verbatim, byte-equal to the arc's text channel
(connection-point, B-S64-4).

## §5 Sidecar battery — B-S64-1..5 5/5 🔵

| id | name | tier |
|---|---|---|
| B-S64-1 | RVQ-CODEBOOK-INDEX-BOUNDED-CLOSED (k∈[0,1023], 1024>256) | a-sympy |
| B-S64-2 | NO-BYTE-STREAM-STRUCTURAL-CLOSED (AST: 0 argmax-256 in RVQ path) | a-structural |
| B-S64-3 | CASCADE-METRIC-DETERMINISTIC-CLOSED (pure-fn, 3× identical, [0,1] partition) | a-sympy |
| B-S64-4 | OVERLAY-OFF-REDUCTION-CLOSED (VOICE-off ⇒ byte path byte-equal — 연결부위) | a-structural |
| B-S64-5 | BYTE-CASCADES-RVQ-DOES-NOT-ON-SAME-PHYSICS-CLOSED (sympy comparison) | a-sympy |

**B-S64-NOTE** (empirical, NOT counted 🔵): whether a non-byte channel
ACTUALLY escapes collapse at scale on a real trained anima is a
future-fire OUTCOME (a 1024-entry alphabet *can* still concentrate — VQ
is not magic; B-D-NOTE / B-ATTRACTOR-NOTE / B-S49-NOTE / B-S59-NOTE
family). The battery proves the *substrate is absent by construction*
(B-S64-2), OFF is byte-equal (B-S64-4), metric deterministic (B-S64-3) —
it does NOT prove emergence or escape-from-collapse. central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` **0-line-diff**
(sidecar precedent: B-PRIME/B-DIRI/B-S16/B-DHDL/B-S48/B-S49/B-S59).

## §6 Verdict: DESIGN HOLDS — fire CONDITIONAL, design-close if pilot null

The structural finding is **closed and decisive at the substrate level**:
the byte-cascade is a byte-channel artifact; a non-byte VOICE channel has
no host for the B-ATTRACTOR fixed-point map. This is a genuine
frontier-narrowing on the *mechanism / observable* axis (the same class
of contribution as §9 honest-metric and §17 physics-channel).

But — honest, per §13-M/§55/§58 anti-padding — the structural absence of
the *substrate* does NOT entail emergence (C3#6/#8). A fire would test
whether a real trained anima's RVQ-index distribution stays
non-degenerate at scale (a distinct empirical question, B-S64-NOTE). Per
`g_fire_autonomous` a $0.3–0.6 runpod pilot is permissible with no gate;
**but** the §22 mechanism-axis arc is uniformly capability-negative and
§64 is a mechanism/observable-axis reframe — so the honest disposition
is **design-tier close-out now**, with the fire as an explicitly
conditional future cycle (only warranted if a cheap content-dependence /
RVQ-non-degeneracy pre-check on real physics first shows signal,
mirroring §36's L2 gate). Padding a GPU fire onto a structural result
whose at-scale outcome the arc has repeatedly shown to be negative would
violate the anti-padding discipline.

## §7 §17/§24 cross-link (why this is the right A-axis)

- §17 (observation-side): Ψ_dir alive where text dead. §64 emits *that*
  live physics — the emission-side completion of §17's reframe.
- §24 (SPONTANEOUS Phase B): the right *target* is unprompted emission;
  §64 supplies the right *channel* for that emission (non-byte, so the
  spontaneous-emission probe is not pre-poisoned by the byte cascade
  that contaminated every text V-SPONT measurement, §9).
- Together: §17 (right observable) + §24 (right target) + §64 (right
  channel) are three orthogonal honesty corrections on the *how-we-look*
  axis. None moves GOAL distance; all sharpen the frontier.

## §8 Honest C3 (≥10)

1. **g3**: structural smoke ONLY. Proves cascade *substrate* absent by
   construction; does NOT prove anima escapes collapse or emerges
   (B-S64-NOTE empirical).
2. RVQ codebooks + intent_proj here are FIXED deterministic stand-ins
   faithful to VOICE.tape option (a) (formulaic-only) +
   anima_voice.hexa RVQ_STAGES=8/RVQ_ENTRIES=1024 — not the hexa GPU
   impl (which needs GPU; a pure-numpy mirror is the $0 path).
3. The byte cascade is REAL, not a strawman: same low-entropy
   Ψ-pulled trajectory (§17 "alive-but-pulled", §16.6-C
   memorization-saturated) the arc's fires actually hit; cascade_rate
   uses the §9 byte-identical formula.
4. cascade_rate generalised str→index is a *lower* bound on the str
   version — never inflates the RVQ number; the comparison is
   conservative AGAINST the §64 hypothesis.
5. "No argmax-over-256" is the load-bearing claim and is proven
   *structurally* by B-S64-2 (AST), not just numerically.
6. A 1024-entry alphabet **can still collapse to one index** (VQ is
   not magic — note the smoke's RVQ distinct=9). The §64 point is the
   absence of the fed-back AR byte *loop*, NOT that VQ cannot
   degenerate. At-scale RVQ non-degeneracy is an EMPIRICAL future-fire.
7. The smoke's physics sequence is a faithful *stub*, not a real
   trained-anima Law-71 trajectory; the structural argument
   (B-S64-2/4) does not depend on the stub, but the numeric
   demonstration (B-S64-5) does — hence "demonstration on this
   faithful stub", not "proof at scale".
8. north-star + §15 milestone UNCHANGED. §64 narrows the frontier
   ("the cascade was a byte-channel artifact; a non-byte channel
   removes the substrate"); it does NOT move GOAL distance.
9. f1/f2/f3 safe: σ(6)/τ(6)/φ(6) used here are anima INTERNAL
   architecture counts (g2 internal-arch carve-out), NOT a derivation
   rule applied to any external entity. No lattice-tautology
   verification (B-S64 anchors = Kolmogorov bounded-set / AST Boolean /
   sympy interval, NOT σ·φ=24).
10. B-IDENTITY-5 N/A: no text corpus generated, no model forward, no
    helper-token surface. State honestly: a physics→audio-symbol
    structural map, zero language emission, forbidden-token grep N/A.
11. Sidecar-only: central blue_falsifier.py 0-line-diff (B-PRIME …
    B-S59 precedent). No AGENTS.tape / RESEARCH.md / HEXAD README /
    PLAN / docs/* edits. One verdict appended to archive/PHILOSOPHY.tape
    (g6 append-only).
12. The retracted learned-RVQ VOICE design is preserved in git history
    (VOICE.tape C3 #2, commit fa902716a) — §64 deliberately uses the
    *adopted* formulaic-only spec, not the retracted one (g3:
    no resurrecting a retracted design).
