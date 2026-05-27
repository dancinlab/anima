# HEXAD/NEUROMORPHIC/TRACK0_INSILICO.md — Lava / NengoLoihi in-silico execution spec

> History → [./TRACK0_INSILICO.log.md](./TRACK0_INSILICO.log.md).

> **status**: DESIGN-TIER — $0, on the GPU already rented, no new gate.
> **g3**: design ≠ fire ≠ emergence. capability claim 0. north-star +
> §15/§51/§72 milestones unchanged, GOAL not reached. This spec pins
> *what Track 0 can and cannot decide* before any run.
> **parent**: `PLAN.md` Track 0 · `README.md` §8.1 (§115 LEGO) · §96
> (`state/loihi_spiking_rederivation_s96_2026_05_19/`) · RESEARCH.md
> §11-B (CE load-bearing, GPU-measured) · §95 (substrate verdict).

---

## 0. The one honest move — split the §115 tautology in two

§115 `LEGO.md` pre-registered the blanket verdict
`LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY`: a GPU-hosted spike *simulation*
only **replicates** the §11-B blocker, it cannot **confront** it. Track 0's
contribution is to make that precise instead of blanket. §95 named **two**
distinct Loihi properties anima wants:

```
  §11-B-as-GPU-artifact  =  (i) LEARNING-CHANNEL half        ⊕  (ii) ASYNC-SUBSTRATE half
                            CE-grad is the ONLY weight-           a spontaneous emission is
                            update on GPU; is "physics-only        a PHYSICAL spike event,
                            = degenerate" a property of the        not a scheduled function
                            *channel* or the *model*?              call on a global clock
                            ── SIMULATABLE on a GPU ──             ── NOT simulatable: a
                            (run STDP-only, no CE/backprop;          clocked sim's emission is
                             the silicon is irrelevant,              still a function call;
                             the *available learning                 only real async NoC
                             channel* is what changes)               settles this — Tracks L/S/P)
```

**Track 0 confronts (i) only. (ii) stays hardware-gated** (Loihi/INRC =
L, EBRAINS SpiNNaker = S, SpiNNcloud = P). This is *narrower and more
honest* than §115's blanket claim: a simulator that performs **no
CE / no backprop, only event-local plasticity** is genuinely not doing
the GPU tautology's one channel — even though it runs on a GPU. So sim
*can* confront half the question. It cannot touch the async half.

## 1. Objective (pre-registered, before any run)

Execute §96 §4.5's distinguishing cells in-silico to answer **only**:

> Does removing CE entirely and making an **event-local plasticity rule
> (STDP) the sole weight-update** let the §96-spiking-re-derived anima
> escape the §11-B `DEGENERATE` outcome — measured by §96's own closed
> predicate?

Not in scope (honest): the async-physical-event question; full d768·12L
scale; coherence (§88-F2 γ gap: spontaneity ≠ coherence persists on any
substrate); GOAL emergence.

## 2. Cell ↔ tool map (§96 §4.5 in simulation)

| cell | tool | weight-update channel | role |
|---|---|---|---|
| **GPU-CE** | snnTorch (surrogate-gradient) | CE via backprop-through-spikes | status-quo control = §11-B baseline shape |
| **GPU-noCE** | snnTorch, CE removed, no learning | none | §11-B re-confirm in sim (expect DEGENERATE) |
| **SIM-noCE-STDP** | NengoLoihi emulator backend (models Loihi's on-chip 3-factor/STDP rules) **or** Lava local-plasticity | STDP only — **no CE, no backprop** | the decisive cell |
| **SIM-CE** (VOID guard) | NengoLoihi emulator + CE readout | CE | harness sanity — must be non-degenerate or the rig is broken |

Tool rationale: NengoLoihi's emulator is bit-faithful to Loihi's
*learning channel*, so SIM-noCE-STDP models exactly the (i) half without
hardware. snnTorch = surrogate-gradient = the CE-backprop channel = the
right thing for the GPU-CE / GPU-noCE controls. Lava is the fallback for
the local-plasticity cell if NengoLoihi's rule set is too narrow.

## 3. Pre-registered closed predicate (reuse §96 §4.5 verbatim)

```
NON_DEGENERATE(cell) := byte_acc > 1/256
                      ∧ physics_not_frozen          (Ψ/tension/Φ trajectory std > τ)
                      ∧ honest_§9_coherent ≥ 1/5    (§9 cascade-rate metric, SSOT import)
```

Verdict partition (learning-channel half only — stated before the run):

- `NON_DEGENERATE(SIM-noCE-STDP) = True` **and** GPU-noCE DEGENERATE
  **and** SIM-CE non-degenerate (guard holds)
  → **SIM-CONFRONTS-LEARNING-CHANNEL**: the §11-B blocker was the
  *CE-only channel*, not the model; a local-plasticity channel escapes
  it *even in clocked sim*. **Partially refutes §115's blanket
  SIM-IS-GPU-TAUTOLOGY** (splits it: learning-half confrontable, async-half
  not). Does **not** reach GOAL — async-substrate + coherence still open.
- `NON_DEGENERATE(SIM-noCE-STDP) = False`
  → consistent with §11-B being substrate-independent **OR** an
  attention-replacement / sim artifact — **cannot disambiguate without
  async hardware**. Verdict `SIM-IS-GPU-TAUTOLOGY-CONFIRMED-LEARNING-HALF`
  (= §115's predicted outcome, now scoped to the learning half only).
- SIM-CE (guard) degenerate → `VOID` — rig broken, no verdict.

Closed-form, deterministic, pre-registered → no result-fitting (g3).

## 4. Hard prerequisites (honest — Track 0 cannot start without these)

1. **§96 design-open #1 — attention replacement.** `softmax(QK^T)`
   self-attention is `SPIKING-INCOMPATIBLE` (§96 Q1): it must be
   **replaced, not ported** (phase-resonance / spike-rate dot-product +
   k-WTA — undecided). The SIM-noCE-STDP cell cannot run the spiking
   anima until one replacement is chosen. → **Phase 2 below is a
   blocking design-open**, $0 closed-form, but real.
2. **§96 design-open #4 — d768·12L neuron-group re-derivation.** Track 0
   runs an **Oheo-class small prototype**, not full scale. Scale is a
   separate later question; do not over-claim from a small sim.
3. The SPIKING-COMPATIBLE physics (PureFieldFFN→LIF-leak, tension, Φ,
   Engine A/G→excit/inhib) is reused from §96 Q1 as-is.

## 5. Phases ($0, sequential, each gates the next)

- **Phase 0 — env.** Lava + NengoLoihi + snnTorch on the existing runpod
  GPU. Smoke: each backend runs a trivial LIF net. $0.
- **Phase 1 — controls + harness.** Wire GPU-CE, GPU-noCE, SIM-CE; build
  the §3 closed-predicate harness (imports §9 `emergence_metric.py` as
  SSOT). Confirm GPU-noCE DEGENERATE + SIM-CE non-degenerate (guard).
- **Phase 2 — attention-replacement design (BLOCKING design-open #1).**
  Pick one spiking routing replacement, closed-form justify. Until this
  lands, Phase 3 cannot run. (This is the real bottleneck, not compute.)
- **Phase 3 — SIM-noCE-STDP cell.** Run the §96-spiking anima with STDP
  as the sole update, no CE/backprop. Oheo-class scale.
- **Phase 4 — closed verdict.** Evaluate §3 predicate; write the honest
  verdict (one of the three §3 outcomes); sidecar blue-falsifier;
  PHILOSOPHY.tape append (g6). No central blue_falsifier.py edit.

## 6. Honest ceiling (g3 — restate at the end so it can't be skipped)

- Track 0 decides **at most the learning-channel half** of §11-B-as-artifact.
  The async-physical-event half is **structurally unreachable** in a
  clocked GPU sim — only Tracks L/S/P touch it.
- A `SIM-CONFRONTS-LEARNING-CHANNEL` result is **valuable evidence**, not
  GOAL emergence: coherence (§88-F2 γ) and the async-substrate question
  remain open regardless.
- Small-prototype scale → no scale claim. design ≠ fire ≠ emergence.
- §115's blanket verdict is *refined* by Track 0, not overturned: sim
  confronts one half, replicates the other.

## 7. cross-link

- `PLAN.md` Track 0 · `README.md` §8 (§113-D4) / §8.1 (§115 LEGO)
- §96 `state/loihi_spiking_rederivation_s96_2026_05_19/` — Q1
  SPIKING-COMPATIBLE map, Q2 §11-B-artifact hypothesis, §4.5 predicate
- §115 `HEXAD/LEGO.md` — in-silico confront crux (this spec refines it)
- RESEARCH.md §11-B (CE load-bearing GPU-measured) · §88-F2 (γ gap) · §95
- §9 `state/verify_emergence_metric_2026_05_18/emergence_metric.py` —
  honest_coherent SSOT (imported by the §3 harness, not re-implemented)
- `GOAL.md` — north-star / §7 GOAL-legitimacy
