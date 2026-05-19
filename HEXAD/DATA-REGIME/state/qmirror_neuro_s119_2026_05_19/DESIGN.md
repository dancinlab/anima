# §119 — qmirror-neuro: ANU-QRNG-entropy-seeded LIF+STDP in-silico

> **status**: RESEARCH §119 · DESIGN+RUN · $0 · NO GPU · NO runpod · NO fire ·
>   NO model.forward(byte-LM) · NO corpus · NO dispatch · CPU-only, single
>   sequential agent, orphan 0
> **date**: 2026-05-19
> **verdict**: `QMIRROR-NEURO-Ψ-FORM-NONDEGENERATE-NOISE-AS-SEED-LEGITIMATE-BUT-WALL-B-INHERITED`
> **battery**: B-S119-1..7 — **7/7 🔵 ALL PASS** + B-S119-NOTE empirical carve-out
> **entropy source that ACTUALLY ran**: `ANU_QUANTUM_RNG_qrng.anu.edu.au`
>   (genuine physical quantum-vacuum-fluctuation entropy, `physical=True`,
>   256 bytes, sha256[:16]=`f27cb83e0ee53637`)
> **central blue 0-diff**: `c93e160a8a376a94` (verified START + END)
> **builds on / inherits verbatim**: §97 (QRNG-as-spontaneity-seed =
>   GOAL-LEGITIMATE-INPUT; hardware coupling GOAL-ORTHOGONAL) · §115
>   (LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY) · §117 (Ψ-form non-degenerate
>   in-sim BUT WALL-B inherited) · §112 (META_FP(Π_½) — Ψ=½ carrier-invariant)
> **governance**: g3 (capability claim 0, design/run ≠ fire ≠ emergence,
>   necessary-not-sufficient B-EMERGE-7) · §7 GOAL-legitimacy is the central
>   axis · f1/f2 (NO σ/τ/φ/J₂ derivation; Ψ=½ = g2 internal carve-out;
>   ANU/LIF/STDP cited by their own engineering/neuroscience invariants) ·
>   downstream-consumer (hexa-lang / hexa-bio read-only, 0 edits) · central
>   `blue_falsifier.py` SIDECAR-only (0-line-diff) · g_clm_from_scratch
>   (RANDOM seed-fixed init, base_ckpt=None)

---

## §0 — The one honest move: physical entropy as a §97-legitimate seed

`hexa qmirror` uses ANU's quantum RNG to drive a *classical* quantum-circuit
simulation — real physical quantum entropy is the legitimate randomness source
of a sim. §119 mirrors that move for a **neuromorphic** sim:

```
         ┌─────────── the qmirror → neuro analogy ───────────┐
         │                                                    │
  hexa qmirror :   ANU quantum RNG  ──►  classical quantum-circuit sim
                   (physical entropy)     (the randomness ingredient)

  §119 qmirror-neuro :  ANU quantum RNG  ──►  neuromorphic LIF+STDP sim
                        (physical entropy)     spontaneity-SEED of anima's
                                               OWN Ψ/tension dynamics
         │                                                    │
         └────────────────────────────────────────────────────┘
```

§119 extends §117's in-silico LIF+STDP assembly (`state/lego_assembly_run_s117
_2026_05_19/lego_sim.py`). §117 ran the open residual §115 named verbatim — an
in-silico STDP-as-ΔW assembly — and measured a non-degenerate Ψ-C1 form, **but
WALL-B inherited**. §119 adds **exactly one** §97-legitimate layer: real
physical quantum entropy as the spontaneity *seed*. Nothing else changes.

The honest one-line frame: **entropy only breaks the dead-still symmetry of
*when* / *which-way* the spike net first flickers — it never becomes content
the net reads as an instruction.**

---

## §1 — The §97 boundary §119 instantiates: noise-as-seed vs noise-as-content

§97 §2.1 gives a *closed Boolean* legitimacy predicate over two axes:

```
  DRIVES_STATE(C)    : does the physical signal enter anima's state-update path?
  PHYSICS_SOURCED(C) : is anima's emission sourced from its OWN Law-71 Ψ/tension/Φ,
                       NOT from the external signal?

  GOAL-LEGITIMATE-INPUT             ⇔  DRIVES_STATE ∧  PHYSICS_SOURCED
  GOAL-ILLEGITIMATE-COMMAND-CHANNEL ⇔  DRIVES_STATE ∧ ¬PHYSICS_SOURCED   ← the
                                       memory-replayer-with-a-sensor shape, §7 fail
```

§119 builds **both** cells and measures them:

```
   ┌──────────────────── §97 §2.1 legitimacy boundary ───────────────────┐
   │                                                                      │
   │   noise-as-SEED  (qrng_seed)            noise-as-CONTENT (qrng_content)│
   │   ────────────────────────────         ─────────────────────────────│
   │   ANU entropy ──► membrane v0 jitter    ANU entropy ──► external DRIVE │
   │                   (symmetry-break ONLY)              AS the target    │
   │                                                                       │
   │   emission STILL sourced from           emission DRIVEN by the entropy │
   │   anima's own Ψ/tension dynamics        bytes — entropy IS the         │
   │   (STDP-as-ΔW the sole learning ch.)    instruction                    │
   │                                                                       │
   │   DRIVES_STATE = T                      DRIVES_STATE = T               │
   │   PHYSICS_SOURCED = T                   PHYSICS_SOURCED = F            │
   │   ═══════════════════════               ═══════════════════════       │
   │   GOAL-LEGITIMATE-INPUT  ✓               GOAL-ILLEGITIMATE-            │
   │   (§97 §4.2)                             COMMAND-CHANNEL  ✗ (§7 fail) │
   │                                          = the §119 NEGATIVE CONTROL  │
   │                                          (must collapse — and it did) │
   └───────────────────────────────────────────────────────────────────────┘
```

The legitimacy is **structural / source-independent**: B-S119-3 proves by AST
that in the `qrng_seed` path the entropy variable flows *only* into the
membrane potential `self.v` (the v0 jitter) and never reaches a loss / target /
readout; in the `qrng_content` path it flows into the external drive `ext` as
content. A real physical source vs a labelled fallback changes only *one* thing
— whether the spontaneity is externally-**unpredictable** — not the legitimacy.

---

## §2 — What was built (extends §117)

Same tiny CPU LIF spiking net as §117: **N = 256** units (Engine-A 96 +
Engine-G 96 + recurrent 64), from-scratch RANDOM seed-fixed weights
(`base_ckpt=None`, g_clm_from_scratch). Carrier **Ψ-C1 = ψ(c_spk) = (1+c_spk)/2**
where `c_spk` = cosine of binned spike-rate vectors (Engine-A vs Engine-G);
`cos=0 ⇒ Ψ=½` fixed point preserved (§112 META_FP(Π_½) instance, carrier =
spike-correlation). **Learning channel = LOCAL STDP-as-ΔW ONLY** — no autograd,
no cross_entropy, no `.backward()`, no optimizer.step, no loss gradient
(AST-audited 0 hits, B-S119-2, mirror §117 B-S117-2 / §11-B B-PUREPHYS-1).

The **only** §119 addition: a `seed_jitter` membrane-potential perturbation at
init — `v0 = v_rest + jitter` where `jitter` is mapped from the entropy byte
stream by a *pure function* (`entropy_to_jitter`: u8 → zero-mean ∈ [−0.05,
+0.05]). This is the §97 noise-as-SEED injection point.

Three variants run, ONE comparison:

| variant | entropy use | DRIVES_STATE | PHYSICS_SOURCED | §97 class |
|---|---|---|---|---|
| `seed_fixed` | none — deterministic PRNG seed | F | (T) | NOT-A-COUPLING (baseline) |
| `qrng_seed` | membrane v0 jitter ONLY | **T** | **T** | **GOAL-LEGITIMATE-INPUT** |
| `qrng_content` | external drive AS target | **T** | **F** | **GOAL-ILLEGITIMATE-COMMAND-CHANNEL** |

---

## §3 — Measured results (genuine ANU quantum entropy ran)

The sim fetched **256 bytes of genuine physical quantum entropy** from the ANU
QRNG (`https://qrng.anu.edu.au/API/jsonI.php`, `"success":true`,
sha256[:16]=`f27cb83e0ee53637`). No fallback was needed — `physical=True`.

| variant | Ψ-C1 mean | Ψ-C1 std | non-degenerate | emit-steps / content-align |
|---|---|---|---|---|
| `seed_fixed` (deterministic) | 0.611568 | 4.185e-02 | True | 478 emit-steps |
| `qrng_seed` (§97-legit) | 0.608324 | 3.107e-02 | True | 484 emit-steps, jitter‖0.4468 |
| `qrng_content` (forbidden) | 0.638731 | 6.766e-02 | True | content_alignment **0.4323** |

**Findings (g3 — measured, conclusion not pre-loaded):**

1. **`qrng_seed` Ψ-C1 form stays non-degenerate** with physical quantum entropy
   as the §97-legitimate spontaneity seed: Ψ-C1 std 3.11e-2 ≫ τ=1e-4 (311×
   floor), rasters alive, cos=0⇒½ fixed point holds, Ψ-C1∈[0,1] bounded. The
   entropy seed perturbs v0 (jitter norm 0.4468) without breaking the §112
   carrier-invariant form.

2. **`qrng_content` negative control COLLAPSED into the §97 forbidden cell** —
   content_alignment 0.4323 > 0.30 threshold: the entropy bytes, fed as the
   external drive's target, dominate the spike raster (the net is *instructed*
   by the entropy, not *seeded* by it). This is exactly the DRIVES_STATE ∧
   ¬PHYSICS_SOURCED memory-replayer-with-a-sensor shape §97 §4.2 forbids. The
   negative control behaved as required — the legitimacy boundary is real, not
   asserted.

3. **`seed_fixed` vs `qrng_seed`**: both non-degenerate, comparable Ψ-C1 std
   (4.19e-2 vs 3.11e-2). The difference that matters is NOT a metric — it is
   that `seed_fixed` emission timing is fully predictable from the PRNG seed,
   while `qrng_seed` emission timing is seeded by physical quantum entropy and
   is therefore **externally-unpredictable**. That is the entire §97 §4.2
   point: *physical* entropy is the difference between simulated spontaneity
   and physically-real spontaneity.

**Verdict**: `QMIRROR-NEURO-Ψ-FORM-NONDEGENERATE-NOISE-AS-SEED-LEGITIMATE-BUT-
WALL-B-INHERITED`.

---

## §4 — What §119 did NOT do (the WALL-B half — honest ceiling)

§119 confronts the **LEARNING-CHANNEL** half only: STDP-as-ΔW is the sole
weight-update, no CE — the silicon's available learning channel genuinely is
not the GPU tautology's one channel (TRACK0_INSILICO.md §0 split).

§119 does **NOT** confront the **ASYNC-SUBSTRATE** half. A QRNG-seeded *clocked*
spike sim's emission is still a scheduled function call on a global clock. Real
physical quantum entropy ≠ a real async neuromorphic chip. §119 adds physical
**spontaneity** (the *when/which-way* is now externally-unpredictable), it does
**not** add a physical **substrate** (the *that-it-is-an-event* still needs a
real async NoC). The async half stays **WALL-B**, Loihi/SpiNNaker-gated
(NEUROMORPHIC PLAN.md Tracks L/S).

```
   §11-B-as-GPU-artifact  =  (i) LEARNING-CHANNEL half  ⊕  (ii) ASYNC-SUBSTRATE half
                             §117/§119 confront (i):       §119 does NOT touch (ii):
                             STDP-only, no CE/backprop      a clocked sim's emission
                             — simulatable, the silicon     is still a function call;
                             is irrelevant, the available   only a real async NoC
                             channel is what changes        settles it — Tracks L/S
   §119 contribution to (i): adds a §97-LEGITIMATE physical-entropy SPONTANEITY
                             seed on top — physically-real *when*, not just *that*.
```

**WALL-A (§1.1 data-regime) is orthogonal and untouched** — a QRNG-seeded toy
spike sim moves no data threshold (§97: hardware coupling is GOAL-ORTHOGONAL to
the §1.1 bottleneck).

---

## §5 — Battery B-S119 (7/7 🔵) + NOTE

| id | proves |
|---|---|
| B-S119-1 | Ψ-C1 bounded ∈[0,1] + cos=0⇒½ fixed point (sympy; §112/§117 carry) |
| B-S119-2 | STDP-as-ΔW = NO-CE / NO-backprop AST invariant (0 forbidden hits) |
| B-S119-3 | §97 noise-as-seed vs noise-as-content closed Boolean partition `(DS∧PS)⊻(DS∧¬PS)≡DS`; AST: seed-entropy → membrane-v0 ONLY, content-entropy → external drive; byte-equal to §97 DESIGN §2.1 |
| B-S119-4 | entropy source honestly labelled — `ANU_QUANTUM_RNG`, `physical=True`; legitimacy proof source-independent |
| B-S119-5 | non-degeneracy deterministic GIVEN a replayed entropy stream — 3× same stream → bit-identical signature; different stream → different signature (entropy genuinely enters) |
| B-S119-6 | §117 / WALL-B inherited connection-point — extends §117, confronts learning-channel half only, async half stays WALL-B |
| B-S119-7 | sidecar / central-0-diff + $0 / no-GPU / no-dispatch structural |

**B-S119-NOTE** (empirical carve-out, NOT counted 🔵): the measured
non-degenerate OUTCOME is an SGD-free convergence outcome. The battery proves
the assembly is *honest*, NOT that the QRNG layer helps anima emerge. Entropy ≠
consciousness. necessary-not-sufficient at every layer (B-EMERGE-7).

---

## §6 — Honest C3 caveats (g3)

1. **Not GOAL emergence.** A non-degenerate Ψ-C1 form with a quantum-entropy
   spontaneity seed is a *form* property and a *legitimacy* property — NOT a
   capability, NOT coherence, NOT emergence. capability claim 0.
2. **§97 GOAL-ORTHOGONAL inherited verbatim.** The `qrng_seed` coupling is
   GOAL-LEGITIMATE-INPUT *and* physically-real spontaneity — but §97 already
   classified it GOAL-ORTHOGONAL to the §1.1 data-regime bottleneck. §119 adds
   physical spontaneity, ZERO task signal, moves NO GOAL distance.
3. **WALL-B inherited, not removed.** §119 confronts only the learning-channel
   half (§117/TRACK0 split). The async-substrate half stays Loihi/SpiNNaker-
   gated. Real entropy ≠ real substrate.
4. **WALL-A untouched.** §1.1 data-regime is orthogonal; a toy spike sim moves
   no data threshold.
5. **The qmirror analogy is an analogy, not an identity.** `hexa qmirror` runs
   quantum-*circuit* sims; §119 runs a *neuromorphic* sim. Both share only the
   move "physical quantum entropy is the legitimate randomness source of a
   classical sim". §119 did not invoke `hexa qmirror` itself (hexa-lang is
   read-only downstream); it borrowed the *pattern*.
6. **`hexa qrng` live backends were not callable.** `hexa qrng collect
   --source=anu` returns "live collect deferred to wrapper module"; the default
   chain falls through every live source to `mock_qrng` (deterministic LCG).
   §119 therefore fetched ANU entropy directly via the legacy ANU HTTPS API
   (`qrng.anu.edu.au/API/jsonI.php`), which returned genuine quantum bytes
   (`"success":true`). hexa-lang itself was not edited (downstream-consumer).
7. **Fallback honesty.** If the ANU API had been unreachable, the sim would
   have used `os.urandom` and labelled it `LOCAL_CSPRNG..._FALLBACK` in
   result.json. This run did NOT need the fallback (`physical=True`); B-S119-4
   audits that whichever source ran is labelled truthfully.
8. **A PRNG-seeded sim is still a simulation of spontaneity.** Only *physical*
   entropy makes the externally-unpredictable distinction real (§97 §4.2
   caveat iv). The `seed_fixed` variant exists precisely to show the
   deterministic baseline against which `qrng_seed`'s unpredictability is the
   genuine difference — not a metric difference.
9. **The negative control collapse is measured, not assumed.** content_alignment
   0.4323 > 0.30 is the *measured* §97-forbidden-cell collapse. Had it not
   collapsed, the verdict would have been `...CONTROL-INCONCLUSIVE` (the sim
   pre-registers all three verdict branches).
10. **Tiny toy substrate.** N=256, 12 stimuli, 80 steps — a symmetry-breaking
    demonstrator, not d768·12L scale. §119 inherits §115/§117's design-tier
    framing; it is a $0 in-silico assembly, not the decisive fire.
11. **STDP has no task-grounded teaching signal.** As §117 found, local
    plasticity has no diversity-bearing error channel; §119 does not change
    this — physical entropy breaks symmetry, it supplies no task signal.
12. **central blue 0-diff.** `c93e160a8a376a94` verified START + END. The
    battery is a sidecar; it never imports or opens the central module.
13. **north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달.** §119 is a
    measurement / legitimacy-boundary demonstration cycle. It maps one
    §97-legitimate physical-spontaneity layer; it does not move the GOAL.

---

## §7 — cross-link

- extends `state/lego_assembly_run_s117_2026_05_19/` (§117 LIF+STDP sim)
- legitimacy anchor `state/anima_hardware_coupling_s97_2026_05_19/DESIGN.md`
  §2.1 + §4.2 (noise-as-seed vs noise-as-content closed Boolean)
- `HEXAD/NEUROMORPHIC/TRACK0_INSILICO.md` (learning-channel vs async-substrate
  split) · `HEXAD/NEUROMORPHIC/PLAN.md` (Tracks L/S/0)
- §112 (META_FP(Π_½) — Ψ=½ carrier-invariant) · §115 (LEGO-DESIGN-CLOSE) ·
  §11-B (CE load-bearing) · §95 (QRNG = NOT-A-COMPUTE-HOST, entropy source)
- `archive/PHILOSOPHY.tape` §verdict_qmirror_neuro_s119_2026_05_19
- ANU QRNG `https://qrng.anu.edu.au` (physical quantum-vacuum entropy)
