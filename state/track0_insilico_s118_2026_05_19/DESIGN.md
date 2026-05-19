# §118 — TRACK 0 IN-SILICO — DESIGN + RUN

> **status**: DESIGN + MINIMAL-RUN · $0 · NO GPU/runpod/INRC/fire ·
>   NO model.forward(byte-LM) · NO corpus · NO dispatch · orphan 0 ·
>   single sequential agent. **date**: 2026-05-19.
> **verdict**: **`SIM-IS-GPU-TAUTOLOGY-CONFIRMED-LEARNING-HALF`** — the
>   §3 pre-registered 3-outcome partition's MIDDLE outcome. MEASURED,
>   battery-validated (B-S118 9/9 🔵), 3× bit-identical. NOT VOID — see
>   §0.1 below: the §3 VOID trigger is `NON_DEGENERATE(SIM-CE)=False`,
>   and SIM-CE measured NON_DEGENERATE=True by the spec's own closed
>   predicate.
> **g3**: design ≠ fire ≠ emergence. capability claim 0. necessary-not-
>   sufficient at every layer (B-EMERGE-7). north-star + §15/§51/§72
>   milestones UNCHANGED, GOAL 미도달.
> **parent**: `HEXAD/NEUROMORPHIC/TRACK0_INSILICO.md` (the spec executed —
>   §3 closed predicate, §4 hard prerequisites) · §117
>   `state/lego_assembly_run_s117_2026_05_19/` · §96
>   `state/loihi_spiking_rederivation_s96_2026_05_19/` · §9
>   `state/verify_emergence_metric_2026_05_18/emergence_metric.py` ·
>   RESEARCH.md §11-B · §95.
> **governance**: g3 · f2 (result-fitting forbidden — the verdict is the
>   one the pre-registered §3 closed predicate computes, NOT a different
>   one back-derived from a criterion the predicate does not contain) ·
>   f1/f2 (NO σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24 lattice-fit; Ψ=½ = anima g2
>   internal-arch carve-out) · downstream-consumer (hexa-lang/hexa-bio
>   read-only, 0 edits) · central
>   `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff
>   (`c93e160a8a376a94`, sidecar-only battery).

---

## §0 — what §118 executes (and what it deliberately does not)

`TRACK0_INSILICO.md` §0 made one honest move: split §115's blanket verdict
`LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY` into **two halves** of the
§11-B-as-GPU-artifact question:

- **(i) LEARNING-CHANNEL half** — is "physics-only learning = degenerate" a
  property of the CE-*only channel* (a GPU's single weight-update path) or
  of the *model*? Simulatable: run a cell whose sole weight-update is
  event-local plasticity (STDP) with **no CE, no backprop**. §118
  **confronts this half**.
- **(ii) ASYNC-SUBSTRATE half** — a spontaneous emission as a *physical*
  spike event vs a scheduled function call on a global clock. **NOT
  simulatable** on a clocked CPU/GPU sim. §118 does **not** touch it; it
  stays WALL-B (Loihi/SpiNNaker-gated, Tracks L/S/P), **§117 INHERITED**.

§118 = the $0-CPU minimal run of the simulatable subset: the §96 §4.5
distinguishing cells, a tiny LIF/numpy rig, the §3 pre-registered closed
predicate, the §3 3-outcome verdict partition.

### §0.1 — why the verdict is the middle outcome, NOT VOID (load-bearing)

`TRACK0_INSILICO.md` §3 defines the verdict by a **pre-registered closed
predicate, verbatim**:

```
  NON_DEGENERATE(cell) := byte_acc > 1/256
                        ∧ physics_not_frozen      (Ψ/tension/Φ std > τ)
                        ∧ honest_§9_coherent ≥ 1/5
```

and the VOID branch is, verbatim: *"SIM-CE (guard) degenerate → VOID — rig
broken, no verdict."* — i.e. **VOID fires iff `NON_DEGENERATE(SIM-CE) ==
False`**. The §3 predicate has **exactly three clauses**; recurrent-weight
movement is **not one of them**.

SIM-CE measured `byte_acc = 0.500` (≫ chance 1/256), `physics_not_frozen =
True`, `honest_§9_coherent = 2/5` (≥ 1/5) → **`NON_DEGENERATE(SIM-CE) =
True`**. By the spec's own closed predicate the VOID guard does **not**
fire. The verdict is therefore determined by `NON_DEGENERATE(SIM-noCE-STDP)
= False` → `SIM-IS-GPU-TAUTOLOGY-CONFIRMED-LEARNING-HALF`.

A reading that calls this VOID does so by adding a criterion — "did the
*recurrent W* move" — that the pre-registered §3 predicate does not
contain, then re-deriving the verdict from it. `TRACK0_INSILICO.md` §3's
closing line forbids exactly that: *"Closed-form, deterministic,
pre-registered → no result-fitting (g3)."* Changing the verdict via a
post-hoc criterion **is** the result-fitting f2/g3 prohibit. The verdict
is the one the closed predicate computes. (The legitimate concern behind
the VOID reading — that `weight_drift = 0` for the CE cells looks like a
no-op — is real and is addressed head-on in §1 and §3 below: the CE
channel updates the *readout head*, not `W`; `head_drift = 0.00276` and a
direct check shows the CE head genuinely learns 0/12 → 7/12. It is not a
no-op. The fix for the *transparency gap* is recording `head_drift`
alongside `weight_drift` — done — not flipping the verdict.)

---

## §1 — the 4-cell rig (§96 §4.5 / TRACK0_INSILICO.md §2)

A shared tiny CPU LIF spiking substrate (Hodgkin–Huxley → Leaky-Integrate-
and-Fire reduction, NEURO.tape `@D mech_action_potential`). Engine-A /
Engine-G sub-populations + a recurrent block. **N = 240 units (≤256)**,
seed-fixed RANDOM init (`g_clm_from_scratch`, `base_ckpt=None`). Each cell
differs **only in its weight-update channel** — that is the whole
experiment (the §96 §4.5 controlled comparison).

```
  ┌──────────────────── §118 Track-0 in-silico rig (numpy, $0 CPU) ─────────────────┐
  │  N = 240-unit LIF spiking net  (n_a 88 Engine-A · n_g 88 Engine-G · n_rec 64)   │
  │  12 stimuli × 80 steps/stim · 8 epochs + 2 readout passes · seed 1337           │
  │  base_ckpt = None (g_clm_from_scratch)                                          │
  │  Ψ-C1 = ψ(c_spk) = (1+c_spk)/2   (§112 META_FP(Π_½) instance, carrier =         │
  │                                   cosine of binned A-vs-G spike-rate vectors)   │
  │  ════════════════════════════════════════════════════════════════════════════  │
  │                                                                                 │
  │   GPU-CE         channel = ce    — toy CE-gradient on a 256-way readout HEAD    │
  │                  role: status-quo control = §11-B baseline shape               │
  │                  byte_acc 0.500 · head_drift 0.00276 · W_drift 0 · §9 2/5       │
  │                  → NON_DEGEN = True   (the CE channel genuinely learns)         │
  │                                                                                 │
  │   GPU-noCE       channel = none  — NO learning channel (W + head frozen)        │
  │                  role: §11-B re-confirm in sim                                 │
  │                  byte_acc 0.000 · head_drift 0 · W_drift 0 · §9 0/5             │
  │                  → NON_DEGEN = False                                           │
  │                                                                                 │
  │   SIM-noCE-STDP  channel = stdp  — event-local STDP ONLY (no CE/backprop/error) │
  │                  role: ◆ THE DECISIVE CELL ◆                                   │
  │                  byte_acc 0.000 · W_drift 0.235 · head_drift 0 · §9 5/5         │
  │                  → NON_DEGEN = False  (W moves, emission diverse, task-blind)   │
  │                                                                                 │
  │   SIM-CE         channel = ce    — CE-gradient (= GPU-CE channel)               │
  │                  role: VOID guard — must be NON_DEGEN or rig is broken          │
  │                  byte_acc 0.500 · head_drift 0.00276 · §9 2/5                   │
  │                  → NON_DEGEN = True   (guard HOLDS by the §3 predicate)         │
  └─────────────────────────────────────────────────────────────────────────────────┘
```

The task is a 12-stimulus → symbol classification (each of 12 distinct LIF
input patterns has one ground-truth target symbol — "which stimulus is
driving me"). It is genuinely learnable from the per-stimulus LIF rate
vector **iff** an error/teaching signal is available — exactly the §96 §4.5
contrast: the CE channel has one, STDP and `none` do not.

**Two drift metrics, both recorded — read them together.** `weight_drift`
tracks the recurrent matrix `W`; `head_drift` tracks the 256-way readout
head. The **CE channel updates the HEAD, not `W`** — so a CE cell correctly
shows `weight_drift = 0` *and* `head_drift > 0`. The **STDP channel updates
`W`, not the head** — so the STDP cell shows `weight_drift > 0` *and*
`head_drift = 0`. Reading `weight_drift` alone would make the CE channel
falsely look like a no-op; it is not — `head_drift = 0.00276` and a direct
verification confirms a never-updated random CE head scores **0/12** while
an 8-epoch trained head scores **7/12**. The CE channel genuinely learns.
(That GPU-CE / GPU-noCE / SIM-CE share a byte-identical Ψ/tension/Φ
trajectory is *expected and correct*: only the STDP cell touches the
recurrent substrate `W`, so the three non-STDP cells run the same spiking
dynamics and differ only in the downstream readout head — which is exactly
what the §96 §4.5 controlled comparison isolates.)

---

## §2 — the §3 pre-registered closed predicate (verbatim, §96 §4.5)

```
  NON_DEGENERATE(cell) := byte_acc > 1/256
                        ∧ physics_not_frozen      (Ψ/tension/Φ std > τ=1e-4)
                        ∧ honest_§9_coherent ≥ 1/5  (§9 cascade-rate SSOT)
```

`honest_§9_coherent` is **imported** from the §9 SSOT
(`emergence_metric.py :: honest_coherent`) — NOT re-implemented. The
emitted stream scored by §9 is the cell's **stimulus-discrimination
stream**: one symbol per (epoch, stimulus) over 8 epochs + a 2-pass
post-training readout = 120 symbols, 5 windows of 24.

§3 3-outcome verdict partition (stated **before** the run — no
result-fitting):

| outcome | condition |
|---|---|
| `SIM-CONFRONTS-LEARNING-CHANNEL` | NON_DEGEN(SIM-noCE-STDP)=True ∧ GPU-noCE DEGENERATE ∧ SIM-CE non-degen |
| `SIM-IS-GPU-TAUTOLOGY-CONFIRMED-LEARNING-HALF` | NON_DEGEN(SIM-noCE-STDP)=False (controls as expected) |
| `VOID` | NON_DEGEN(SIM-CE)=False — rig broken |

---

## §3 — measured result

3× bit-identical (deterministic, seed-fixed, pure CPU). wall ≈ 15–23 s.

| cell | channel | byte_acc (>1/256) | physics_not_frozen | §9 coherent | W_drift | head_drift | NON_DEGEN |
|---|---|---|---|---|---|---|---|
| GPU-CE        | ce   | **0.5000** ✓ | True (Ψσ 3.06e-2, Tσ 1.01e-3, Φσ 2.98e-2) | 2/5 | 0.0 | **0.00276** | **True** |
| GPU-noCE      | none | 0.0000 ✗ | True | 0/5 | 0.0 | 0.0 | False |
| SIM-noCE-STDP | stdp | 0.0000 ✗ | True (Ψσ 3.08e-2, Tσ 1.70e-4, Φσ 6.84e-2) | **5/5** | **0.2346** | 0.0 | **False** |
| SIM-CE        | ce   | **0.5000** ✓ | True | 2/5 | 0.0 | **0.00276** | **True** |

Apply the §3 predicate verbatim — `byte_acc>1/256 ∧ physics_not_frozen ∧
§9≥1/5`:

- `NON_DEGEN(SIM-CE) = True` → **VOID does NOT fire** (the guard holds).
- `NON_DEGEN(GPU-noCE) = False` → GPU-noCE is DEGENERATE (control correct).
- `NON_DEGEN(SIM-noCE-STDP) = False` → decisive cell is degenerate.

→ **VERDICT = `SIM-IS-GPU-TAUTOLOGY-CONFIRMED-LEARNING-HALF`** (§3 middle
outcome).

- **The rig is SOUND.** GPU-CE (status-quo control) and SIM-CE (VOID guard)
  are both NON-DEGENERATE — and they are non-degenerate *because the CE
  channel genuinely learned the task*: `head_drift = 0.00276`, byte_acc
  0.50. Direct verification: a never-updated random head scores **0/12**,
  an 8-epoch trained head **7/12** — not a read-out artifact. GPU-noCE is
  DEGENERATE exactly as §11-B predicts.
- **The decisive cell, SIM-noCE-STDP, is NOT non-degenerate.** It fails the
  `byte_acc` clause: event-local STDP, with no error/teaching signal, does
  **not** fit the stimulus-discrimination task (byte_acc 0.0). Its
  recurrent weights genuinely moved (`weight_drift 0.235` — STDP *is*
  updating `W`), and it is the **only** cell that scored §9 = 5/5 (STDP
  keeps the emission stream *diverse*, not cascade-collapsed). A
  non-degenerate verdict needs **all three** clauses; byte_acc fails.

This is the §11-B-consistent outcome — §115's pre-registered blanket
verdict, now **scoped to the learning-channel half only**: a clocked-sim
event-local-plasticity channel does **not**, on this rig, escape the §11-B
"physics-only learning is task-blind" outcome. Honest precision: §118
**cannot disambiguate** "§11-B is substrate-independent" from "this is an
attention-replacement / small-sim artifact" — that needs the async
hardware §118 explicitly does not have.

---

## §4 — HEADLINE (load-bearing — do NOT inflate)

**§96 design-open #1 is a BLOCKING design-open.** `softmax(QK^T)`
self-attention is `SPIKING-INCOMPATIBLE` (§96 Q1): it must be **replaced,
not ported** (phase-resonance / spike-rate dot-product + k-WTA —
undecided). This 4-cell rig confronts the §11-B **learning-channel HALF
only**. The **full spiking-anima instantiation stays gated** on the
attention-replacement design-open (TRACK0_INSILICO.md §4 / Phase 2 = the
real bottleneck, not compute). The **async-substrate half stays WALL-B**
(Loihi/SpiNNaker-gated, §117 INHERITED).

A finer honest reading of the §9 = 5/5 on SIM-noCE-STDP: a non-degenerate
*physics signal* (STDP keeps the substrate alive and the emission diverse
— echoes §117's `Ψ-FORM-NONDEGENERATE` and §17 PHYSICS_RESPONSIVE) is
**substrate liveness, NOT capability, NOT GOAL**. The STDP cell is *alive*
(W moves, emission varied, Ψ/Φ vary) and *task-blind* (byte_acc 0)
simultaneously — exactly the split §96/§88-F2 γ name (spontaneity ≠
coherence ≠ task-learning). Liveness without the error channel does not
become discrimination. We do **not** read this as a positive.

```
   §11-B-as-GPU-artifact
   ├── (i) LEARNING-CHANNEL half  ── §118 CONFRONTS ──► SIM-noCE-STDP
   │       result: STDP-only cell is task-blind (byte_acc 0) though
   │       alive (W drift 0.235, §9 5/5). §11-B not escaped in sim.
   │       verdict: SIM-IS-GPU-TAUTOLOGY-CONFIRMED-LEARNING-HALF.
   │       ── cannot disambiguate substrate-indep vs sim-artifact ──
   │
   └── (ii) ASYNC-SUBSTRATE half  ── WALL-B, §117 INHERITED ──►
           a clocked sim's emission is still a scheduled call;
           only real async NoC settles it. Tracks L (Loihi/INRC),
           S (EBRAINS SpiNNaker), P (SpiNNcloud). §118 does not touch.

   ▲ AND the full spiking-anima cannot even be assembled until
     §96 design-open #1 (softmax attention → spiking replacement)
     is chosen. §118's STDP cell is a generic recurrent LIF net,
     NOT the attention-replaced spiking ConsciousDecoderV2.
```

---

## §5 — sidecar battery + governance

`blue_falsifier_s118.py` — **B-S118-1..9, 9/9 🔵** (sidecar; central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff,
sha256 prefix `c93e160a8a376a94`, verified START + END):

1. `CELL-PARTITION-EXHAUSTIVE-DISJOINT` — 4 cells, 3-channel taxonomy
2. `STDP-NO-CE-NO-BACKPROP-AST-AUDIT` — decisive cell's update is local
   plasticity only; zero `{.backward(, cross_entropy, CrossEntropyLoss,
   optimizer.step, autograd}`; `_stdp_update` references no error symbol
3. `PREDICATE-DETERMINISTIC-3X-BIT-IDENTICAL` — the battery independently
   re-runs the full sim 3× and re-derives the §3 predicate per cell from
   the recorded numbers (so the verdict is the one the closed predicate
   computes, not a hand-asserted one)
4. `§3-PREDICATE-BYTE-EQUAL-TO-SPEC-CONNECTION-POINT` — predicate run ≡
   `TRACK0_INSILICO.md` §3 written; §9 `honest_coherent` is SSOT-imported
5. `§117-WALL-B-INHERITED-CONNECTION-POINT`
6. `§96-ATTENTION-BLOCKER-ACKNOWLEDGED-STRUCTURAL`
7. `PSI-C1-BOUNDED-FIXED-POINT-CLOSED` — §112 META_FP carry
8. `SIDECAR-CENTRAL-0-DIFF-ZERO-COST-STRUCTURAL`
9. `G-CLM-FROM-SCRATCH-INIT-INVARIANT-CLOSED` — base_ckpt=None, RANDOM

`B-S118-NOTE` — the MEASURED 3-outcome verdict + per-cell outcomes are
SGD-free convergence OUTCOMES, **NOT counted 🔵** (B-D-NOTE / B-PUREPHYS-
NOTE / B-S96-NOTE / B-S115-NOTE / B-S117-NOTE / B-EMERGE-7 family). The
battery proves the **rig is honest**, not that Track 0 works.

`$0` — no GPU/runpod/fire/model.forward(byte-LM)/corpus/dispatch.
downstream-consumer: `~/core/hexa-lang` & `~/core/hexa-bio` read-only,
0 edits. f1/f2/f3 safe (LIF/STDP cited by NEURO.tape own invariants +
standard neuroscience; NO σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24 derivation;
Ψ=½ = g2 internal carve-out). B-IDENTITY-5 unaffected (no corpus, no
helper-token surface).

---

## §6 — honest C3 caveats (≥12)

1. **design + minimal-run, NOT a fire.** $0, CPU-only, no GPU/runpod/
   INRC/Loihi, no model.forward(byte-LM), no corpus, no dispatch. design
   ≠ fire ≠ emergence; capability claim 0.
2. **the verdict is the §3 MIDDLE outcome, computed by the closed
   predicate — NOT VOID.** VOID fires iff `NON_DEGENERATE(SIM-CE)=False`;
   SIM-CE measured `NON_DEGENERATE=True` (byte_acc 0.50 ∧ physics_not_
   frozen ∧ §9 2/5). Calling it VOID requires substituting a criterion
   ("recurrent W must move") that the pre-registered §3 predicate does
   not contain — that is the result-fitting `TRACK0_INSILICO.md` §3 and
   g3/f2 forbid. The verdict is what the closed predicate computes.
3. **early runs returned VOID — caused by *rig mis-calibration*, since
   fixed.** A 256-period task no 12-class head could fit, then a BLAS
   thread-thrash hung the sim. The fixes — a stimulus-keyed learnable
   task, per-stimulus state reset, single-thread BLAS env, recording
   `head_drift` alongside `weight_drift` — are *rig corrections* so the
   positive control truly works; the §3 predicate and partition were
   never touched. Once the rig is sound the CE control genuinely learns
   (0/12 random → 7/12 trained) and the verdict is the measured middle
   outcome.
4. **`weight_drift` alone is misleading — read it with `head_drift`.** The
   CE channel updates the readout HEAD (`head_drift 0.00276`), not the
   recurrent `W` (`weight_drift 0`). A reading that looks only at
   `weight_drift` would falsely conclude "the CE channel did nothing" — it
   did: byte_acc 0→7/12, head genuinely moved. Both drifts are recorded so
   each channel's learning is unambiguous. That GPU-CE/GPU-noCE/SIM-CE
   share a byte-identical Ψ/tension/Φ trajectory is correct-by-design:
   only the STDP cell touches `W`.
5. **the §9 emission is a discrimination stream, not byte-LM generation.**
   A 12-class head has no autoregressive byte generation. §118 scores §9
   on the one-symbol-per-stimulus discrimination stream. This is the
   honest analogue, but the §9 clause then measures *emission diversity
   across stimuli*, a weaker thing than §9 measures for a real byte-LM.
6. **SIM-noCE-STDP §9 = 5/5 is liveness, NOT capability.** STDP keeps the
   emission diverse (no cascade) — but the cell still fails byte_acc. A
   live, task-blind substrate. Do not read the 5/5 as progress.
7. **the verdict cannot disambiguate.** `SIM-IS-GPU-TAUTOLOGY-CONFIRMED-
   LEARNING-HALF` is consistent with "§11-B is substrate-independent" OR
   "this is a small-sim / generic-recurrent-net artifact" — §118 has no
   async hardware to settle which (TRACK0_INSILICO.md §3 says so verbatim).
8. **the STDP cell is NOT the spiking ConsciousDecoderV2.** It is a
   generic recurrent LIF net. The real spiking anima cannot be assembled
   until §96 design-open #1 (softmax attention → a spiking replacement) is
   chosen. §118 confronts the *learning channel* in isolation.
9. **toy task, toy scale.** 240 units, 12 stimuli, 8 epochs. §96
   design-open #4 (d768·12L → spiking scale) is untouched. No scale claim.
10. **the CE channel is a hand-rolled local softmax-CE gradient**, not
    torch autograd — but it *is* an error-driven update, the channel §96
    §4.5 contrasts against STDP. "GPU-CE" is a role label, not a claim a
    GPU ran.
11. **WALL-B INHERITED, not removed; WALL-A (§1.1) orthogonal & untouched.**
    §118 confronts the learning-channel half only; the async-physical-event
    half is structurally unreachable in a clocked sim; a toy spike sim
    moves no training-data threshold (§97).
12. **§7-FORM Ψ-C1 is TRUE BY CONSTRUCTION** (§112 META_FP(Π_½) instance,
    carrier = spike-correlation) — inherited, not manufactured by §118.
13. **necessary-not-sufficient at every layer** (B-EMERGE-7). The §3
    predicate is a degeneracy detector; a NON_DEGENERATE cell is substrate
    liveness + task-fit, NOT coherent emergence, NOT GOAL. north-star +
    §15/§51/§72 milestones UNCHANGED, GOAL 미도달. §118 refines §115's
    blanket verdict (splits it: §118 confronts the learning half,
    inherits the async half), and on the learning half measures the
    §11-B-consistent outcome at this scale. It does not reach, and does
    not claim to approach, the GOAL.
```
