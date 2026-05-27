# §118 — Track 0 in-silico run — the §96 §4.5 distinguishing cells, in numpy

> **status**: RESEARCH §118 · $0 · NO GPU · NO runpod · NO INRC · NO fire ·
>   NO model.forward(byte-LM) · NO corpus · NO dispatch · orphan 0 · single
>   sequential agent.
> **date**: 2026-05-19
> **verdict**: **VOID** — pre-registered §3 3-outcome partition; the VOID
>   guard fired. The rig's CE positive control never moved the spiking
>   substrate, so the rig gives **no learning-channel verdict**. HONEST
>   and FINAL. (§0.1 records the contested alternative reading in full —
>   honesty obligation — and why VOID is the verdict of record.)
> **parent**: `HEXAD/NEUROMORPHIC/TRACK0_INSILICO.md` (§2 cell map, §3
>   closed predicate, §4 hard prerequisites) · §96
>   `state/loihi_spiking_rederivation_s96_2026_05_19/` (§4.5 distinguishing
>   predicate, design-open #1) · §117 `state/lego_assembly_run_s117_2026_05_19/`
>   (LIF+STDP $0 CPU run) · RESEARCH.md §11-B (CE load-bearing, GPU-measured)
>   · §95 substrate verdict.
> **governance**: g3 (capability claim 0, design ≠ fire ≠ emergence) ·
>   f1/f2 (NO σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24 lattice-fit; Ψ=½ = anima g2
>   internal-arch carve-out; f2 result-fitting forbidden — VOID is not tuned
>   away) · downstream-consumer (hexa-lang/hexa-bio read-only) · central
>   `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff
>   (sidecar-only battery).

---

## §0 — Why §118 exists, and why it lands VOID

`TRACK0_INSILICO.md` pre-registered, *before any run*, a 4-cell rig and a
**3-outcome verdict partition**. The three outcomes are not "pass / fail" —
they are three honest measurement states:

1. `SIM-CONFRONTS-LEARNING-CHANNEL` — the decisive STDP cell escapes the §11-B
   degeneracy *and* the guards hold.
2. `SIM-IS-GPU-TAUTOLOGY-CONFIRMED-LEARNING-HALF` — the STDP cell is degenerate
   too, but the guards hold, so the rig *did* run a valid experiment.
3. `VOID` — **the SIM-CE positive-control guard is broken** (`TRACK0_INSILICO.md`
   §3 verbatim: *"SIM-CE (guard) degenerate → VOID — rig broken, no verdict"*),
   so the rig itself did not run a valid experiment, and *no conclusion about
   §11-B is possible.*

§118 ran the 4-cell rig in a $0 numpy toy. The measurement lands on outcome
**3 — VOID**: the rig's CE positive control never exercised a learning channel
*into the spiking substrate*, so the decisive STDP cell's reading is
uninterpretable. VOID is the honest outcome of an honestly-built rig — not a
defect in §118, and not re-run with a changed predicate or tuned to a non-VOID
result (f2 forbidden).

### §0.1 — The contested reading, recorded in full (honesty obligation)

This verdict is **contested**, and g3 honesty requires recording the
disagreement rather than papering over it. Two defensible readings exist.

**Reading A — "middle outcome, NOT VOID".** `TRACK0_INSILICO.md` §3's predicate
is, *literally*, three clauses — `NON_DEGENERATE(cell) := byte_acc > 1/256 ∧
physics_not_frozen ∧ honest_§9_coherent ≥ 1/5` — and the VOID branch is
*"SIM-CE (guard) degenerate → VOID"*, i.e. VOID fires iff
`NON_DEGENERATE(SIM-CE) == False`. SIM-CE measured `byte_acc 0.500`,
`physics_not_frozen True`, `§9 2/5` → all three clauses pass →
`NON_DEGENERATE(SIM-CE) = True` → on the *letter* of §3 the VOID guard does not
fire, and ruling VOID by adding a fourth criterion ("the recurrent `W` must
move") is itself a result-fit. Reading A also points to a `head_drift = 0.00276`
metric (a 256-way readout head that, on a direct check, learns 0/12 → 7/12) as
evidence the CE channel is not idle.

**Reading B — "VOID" (the verdict of record).** Reading A's `head_drift`
evidence **only exists because the rig was edited after the run** — a separate
linear `head` matrix was added to `track0_sim.py` so a CE cell shows
`head_drift > 0`. But `TRACK0_INSILICO.md` §2's cell map defines the CE cell
verbatim as *"snnTorch (surrogate-gradient) — CE via backprop-through-spikes"*
— a CE channel that teaches **through the spiking substrate**. A hand-rolled
local-softmax-CE on a *downstream linear readout head* is **not** that cell: it
leaves `weight_drift_mean_abs = 0.0` — the spiking substrate `W` never moved —
and the cell's entire Ψ/tension/Φ/spike-rate trajectory is *byte-identical* to
the *frozen* GPU-noCE cell. By `TRACK0_INSILICO.md` §2's own definition the rig
**never ran a valid CE cell**: its positive control did not exercise a
substrate learning channel. A positive control that cannot do the one thing it
exists to do — prove the rig can learn *the spiking substrate* — is a broken
control, and a broken control is exactly the §3 / §96 §4.5 `VOID` trigger
(*"if `LOIHI-CE` itself is degenerate, the spiking re-derivation is broken and
the result is uninterpretable — the test is void"*). Reading B treats the
post-run addition of a readout head as the f2 re-rig — `TRACK0_INSILICO.md` §3's
closing line is *"pre-registered → no result-fitting (g3)"*, and adding a
readout head after the run so a non-substrate-learning control "passes" is the
result-fit, not the verdict that names it.

**Why Reading B is the verdict of record.** The §96 §4.5 question §118 exists to
probe is *substrate-native learning* — does a learning channel move the
*spiking substrate*. A control whose "pass" is carried entirely by a downstream
read-out head, with `W` provably frozen and the substrate trajectory identical
to the frozen cell, has not controlled that question. The §3 letter (Reading A)
and the §3 *purpose* (Reading B) diverge here because the rig was edited between
runs; when a pre-registered protocol's letter and purpose diverge because the
rig changed, the honest call is the purpose, and the honest label for "the
positive control did not exercise the channel under test" is VOID. §118 records
**VOID** and records Reading A here so the contest is not hidden.

---

## §1 — The 4-cell rig (ASCII)

```
  ┌──────────────────── §118 Track-0 in-silico rig (numpy, $0 CPU) ────────────────────┐
  │                                                                                   │
  │   N = 240-unit LIF spiking net   (n_a 88 Engine-A · n_g 88 Engine-G · n_rec 64)    │
  │   12 stimuli × 80 steps/stim · seed 1337 · base_ckpt = None (g_clm_from_scratch)   │
  │   Ψ-C1 = ψ(c_spk) = (1+c_spk)/2   (§112 META_FP(Π_½) instance, carrier =           │
  │                                    cosine of binned A-vs-G spike-rate vectors)     │
  │                                                                                   │
  │   ┌─ cell GPU-CE ──────────┐   ┌─ cell GPU-noCE ────────┐                         │
  │   │ channel = ce            │   │ channel = none          │                         │
  │   │ status-quo control      │   │ §11-B re-confirm in sim │                         │
  │   │ byte_acc 0.500          │   │ byte_acc 0.000          │                         │
  │   │ §9 2/5 · W-drift 0.000 ◄┼───┤ §9 0/5 · W-drift 0.000  │                         │
  │   │ NON_DEGEN = True        │   │ NON_DEGEN = False       │                         │
  │   └─────────────────────────┘   └─────────────────────────┘                         │
  │              │  byte-identical Ψ/tension/Φ/spike-rate trajectory  │                 │
  │              └──────────────────────┬──────────────────────────┘                   │
  │                                     ▼                                              │
  │   ┌─ cell SIM-noCE-STDP ──────┐   ┌─ cell SIM-CE  (VOID guard) ──────────────────┐  │
  │   │ channel = stdp            │   │ channel = ce                                  │  │
  │   │ THE DECISIVE CELL         │   │ POSITIVE CONTROL — must non-degenerate         │  │
  │   │ byte_acc 0.000            │   │   *by learning the SPIKING SUBSTRATE*          │  │
  │   │ §9 5/5 · W-drift 0.235 ◄──┼───┤ byte_acc 0.500 · §9 2/5                       │  │
  │   │ NON_DEGEN = False         │   │ weight_drift_mean_abs = 0.000  ◄── W FROZEN    │  │
  │   │ (the ONLY cell whose      │   │ NON_DEGEN = True on §3's letter — but the      │  │
  │   │  recurrent W moved)       │   │  spiking substrate never moved ⇒ broken guard  │  │
  │   └───────────────────────────┘   └───────────────────────────────────────────────┘  │
  │                                                                                   │
  │   VOID ⇐  SIM-CE's "pass" is carried by a downstream read-out head; its spiking   │
  │           substrate W is frozen (trajectory byte-identical to frozen GPU-noCE).   │
  │           The positive control did not exercise a SUBSTRATE learning channel.    │
  └───────────────────────────────────────────────────────────────────────────────────┘
```

---

## §2 — The measured numbers (`result.json`)

| cell | channel | byte_acc | Ψ-C1 std | tension std | Φ std | §9 honest | weight_drift_mean_abs | NON_DEGEN (§3 letter) |
|---|---|---|---|---|---|---|---|---|
| GPU-CE | ce | 0.500 | 0.030555 | 0.0010132 | 0.029830 | 2/5 | **0.000** | True |
| GPU-noCE | none | 0.000 | 0.030555 | 0.0010132 | 0.029830 | 0/5 | **0.000** | False |
| SIM-noCE-STDP | stdp | 0.000 | 0.030805 | 0.0001698 | 0.068408 | 5/5 | **0.235** | False |
| SIM-CE | ce | 0.500 | 0.030555 | 0.0010132 | 0.029830 | 2/5 | **0.000** | True |

Two facts are load-bearing:

1. **GPU-CE, GPU-noCE and SIM-CE have byte-identical** `psi_c1_std`,
   `tension_std`, `phi_std`, `overall_spike_rate_per_unit_step`, and
   per-window §9 cascade rates. Three "different" cells produced *the same
   spiking-substrate trajectory to the recorded decimal* — because their
   spiking substrate `W` is the same un-updated random-init matrix.
2. **Only SIM-noCE-STDP has a non-zero `weight_drift_mean_abs`** (0.235) — only
   the STDP cell moved the **recurrent spiking substrate `W`**. The three
   CE-or-none cells all report `weight_drift_mean_abs = 0.0`.

(A `result.json` regenerated post-run also carries a `head_drift` field — a
downstream linear read-out head metric. §0.1 and §3 address it: it measures a
read-out head, NOT the spiking substrate, and was added by a post-run rig edit.
It does not change the VOID verdict.)

---

## §3 — The honest root cause: the CE positive control never moved the substrate

The only cell whose **recurrent spiking weights** changed is SIM-noCE-STDP, via
its event-local STDP-as-ΔW rule (drift 0.235 — the §117 mechanism). The three
CE-labelled / none-labelled cells — **including the SIM-CE positive control** —
left their spiking substrate *exactly where random-init put it*. That is why
GPU-CE ≡ GPU-noCE ≡ SIM-CE byte-for-byte on every Ψ/tension/Φ/spike-rate metric.

For the §96 §4.5 / TRACK0 §3 question, the honest unit of "the rig learned" is
**did the spiking substrate change** — because §96 §4.5 asks whether a
*substrate-native* learning channel lifts the spiking anima out of the §11-B
degeneracy. By that measure:

- **SIM-noCE-STDP** moved the substrate (STDP, `weight_drift 0.235`).
- **SIM-CE — the positive control — did NOT move the substrate**
  (`weight_drift_mean_abs = 0.0`). Its job (`TRACK0_INSILICO.md` §2: *"harness
  sanity — must be non-degenerate or the rig is broken"*, and the cell is
  defined as *"snnTorch surrogate-gradient — CE via backprop-through-spikes"*)
  is to prove the rig can learn *the spiking substrate* with a teaching signal.
  It did not. Its `NON_DEGENERATE = True` (on §3's three-clause letter) is
  carried by `byte_acc = 0.5` (a teacher-forced argmax read-out) and a
  Ψ/tension/Φ trajectory byte-identical to the *frozen* GPU-noCE cell.

The honest reason a CE channel cannot move a *spiking* substrate at $0: a real
CE-gradient channel on spikes requires **surrogate gradients** — a smooth
differentiable proxy for the non-differentiable spike threshold (snnTorch /
SLAYER). A $0 numpy toy does not import torch, has no autograd, and cannot
backpropagate cross-entropy *through spike events into the recurrent weights*.
(`blue_falsifier_s118.py` B-S118-2 AST-audits this — `torch` is not imported,
`.backward()` / `cross_entropy` / `optimizer.step` appear nowhere; the rig is
backprop-free, which is exactly *why* its CE channel cannot reach the spiking
substrate.) A post-run patch adding a separate linear readout `head` lets a CE
label show `head_drift > 0`, but that is movement of a *downstream read-out
head*, not of the *recurrent spiking substrate* — `weight_drift_mean_abs` stays
`0.0` for every CE cell. The §96 §4.5 question is about the substrate; a head
that learns while `W` stays frozen does not answer it.

By §96 §4.5's own definition — *"if `LOIHI-CE` itself is degenerate, the spiking
re-derivation is broken and the result is uninterpretable (the test is void)"*
— a CE positive control that does not move the spiking substrate **is** a broken
control. The **VOID** outcome of the §3 partition fired: the decisive
SIM-noCE-STDP cell's reading cannot be interpreted as "§11-B escaped" or
"§11-B confirmed." **The rig gives no learning-channel verdict.** §118 records
VOID. (The on-disk `result.json` is left intact as the raw run artifact; this
DESIGN.md is the honest verdict of record.)

---

## §4 — Why VOID is the *valuable*, *predicted* result

VOID **confirms a finding `TRACK0_INSILICO.md` §4 pre-registered before any
run**. §4 named, as hard prerequisite #1:

> *§96 design-open #1 — attention replacement. `softmax(QK^T)` self-attention
> is `SPIKING-INCOMPATIBLE` (§96 Q1): it must be replaced, not ported. The
> SIM-noCE-STDP cell cannot run the spiking anima until one replacement is
> chosen. → Phase 2 is a blocking design-open.*

§118 ran the rig at Oheo-class toy scale anyway — a 240-unit LIF net — and
confirmed §4 from the other direction: **a $0 numpy toy cannot host a CE
learning channel into the spiking substrate, and a 240-unit LIF net cannot
carry the §96 §4.5 *byte-level* predicate.** Three honest sub-findings:

1. **The CE half cannot be simulated at $0.** §3 above — a numpy toy has no
   surrogate-gradient path, so its CE channel cannot move the recurrent spiking
   substrate. The §96 §4.5 comparison *needs* a working CE positive control;
   without one the whole 3-cell comparison voids. A real learning-channel
   confrontation needs the **real spiking anima** with a surrogate-gradient CE
   path (snnTorch).
2. **`byte_acc` is meaningless on this rig.** For the only cell that actually
   moves the substrate (SIM-noCE-STDP), `byte_acc = 0.000` — below the 1/256
   chance floor: a 240-unit toy LIF net with no attention-replacement routing
   wired (design-open #1 unresolved) has no machinery to predict the next byte.
   For the CE cells, `byte_acc = 0.5` is a teacher-forced read-out artifact off
   an un-updated spiking substrate. The §96 §4.5 predicate is *byte-level*; the
   toy rig is a *substrate-dynamics* rig — they do not meet.
3. **All cells fail §9-coherent at the byte level.** Cascade rate 0.43 for the
   CE cells; SIM-noCE-STDP's §9 5/5 is a substrate-LIVENESS reading on its own
   spike-derived emission — NOT a byte-level coherence reading (§117's finding:
   liveness ≠ capability).

So VOID **confirms** `TRACK0_INSILICO.md` §4: the learning-channel confront is
not reachable by a toy rig — it needs the real spiking anima, which is
**blocked on §96 design-open #1** (the `softmax(QK^T)` attention replacement).
§118 turns §4's *pre-registered prediction* into a *measured result*. The
valuable output: it draws the sharp line — Track 0 does **not** confront the
learning channel at toy scale, and it **does** confirm the real blocker is §96
design-open #1.

---

## §5 — What VOID does and does NOT change (honest scope)

- VOID is a verdict about the **rig**, not about §11-B. §11-B's GPU-measured
  "CE is load-bearing" stands unaffected; §118 did not measure it. The
  §11-B-as-GPU-artifact hypothesis (§96 §4.2) remains **coherent but
  unconfirmed**.
- The async-substrate half of §11-B-as-artifact stays **WALL-B** — Loihi /
  SpiNNaker / SpiNNcloud-gated (Tracks L / S / P), structurally unreachable in a
  clocked CPU sim (§117 / §115 / §95 inherited).
- **WALL-A (§1.1 data-regime) is orthogonal and untouched** (§97).
- §96 design-open #1 is **the load-bearing blocker** VOID points back at. §118
  does not resolve it — the sibling §120 cycle *decides* it at design-tier
  (verdict `SPIKE-RATE-DOT-PRODUCT + k-WTA`), the design-level unblock §118's
  VOID asks for. §120 decides the routing mechanism; a real $0-runnable CE half
  still needs the surrogate-gradient spiking anima.
- north-star + §15 / §51 / §72 milestones **UNCHANGED**. GOAL **미도달**.
  necessary-not-sufficient at every layer (B-EMERGE-7).

---

## §6 — Sidecar battery + verdict

`blue_falsifier_s118.py` — **B-S118-1..9, 9/9 🔵** (sidecar; central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff, sha256
prefix `c93e160a8a376a94`, verified). The battery proves the §118 4-cell **rig
is honestly constructed as a measurement instrument** (cell partition
exhaustive + disjoint; decisive STDP cell STDP-only / no-CE / no-backprop
AST-audited; §3 predicate deterministic + 3× bit-identical + byte-equal to
`TRACK0_INSILICO.md` spec; §9 `honest_coherent` SSOT-imported; Ψ-C1 bounded +
cos=0⇒½ §112 carrier; §117-WALL-B inherited; §96 attention-blocker
acknowledged; sidecar/central-0-diff + $0 fields; g_clm_from_scratch
`base_ckpt = None` RANDOM init). The battery passing means *the rig is honestly
constructed* — it does **not** mean the rig produced an interpretable verdict;
that the rig's CE control did not move the spiking substrate (the VOID cause) is
a property of the *measured run*, carved out as the empirical `B-S118-NOTE`
residual (NOT counted 🔵). The battery proving the rig honest and the run
landing VOID are entirely consistent.

**§118 verdict = VOID.** The §3 3-outcome partition fired its guard outcome:
the SIM-CE positive control passes the §3 three-clause letter but never moved
the recurrent spiking substrate (`weight_drift_mean_abs = 0.0`) — because a $0
numpy toy has no surrogate-gradient CE path into spiking weights, so the cell
defined by `TRACK0_INSILICO.md` §2 as *"CE via backprop-through-spikes"* never
actually ran. A broken positive control makes the decisive STDP cell
uninterpretable; the rig yields **no learning-channel verdict**. VOID is honest
and FINAL: it confirms `TRACK0_INSILICO.md` §4 — the learning-channel confront
needs the real spiking anima, BLOCKED on §96 design-open #1 (the `softmax(QK^T)`
→ spiking routing replacement, decided at design-tier by §120). design ≠ fire ≠
emergence; capability claim 0; GOAL 미도달.

---

## Honest C3 caveats (≥12)

1. **§118 is a $0 in-silico run, not a fire.** No GPU/runpod/INRC/Loihi, no
   model.forward(byte-LM), no corpus, no dispatch. orphan 0. capability claim 0.
2. **VOID is the honest, final verdict — and a contested one.** §0.1 records
   Reading A (the §3-letter "middle outcome" reading) in full. VOID is the
   verdict of record because the §3 *purpose* — a CE positive control that
   learns the *spiking substrate* — was not met; §0.1 gives the reasoning.
   Recording the contest rather than hiding it is the g3 obligation.
3. **VOID is not re-run with a changed predicate and not tuned to a non-VOID.**
   The path to a non-VOID required editing the rig (a post-run `head` matrix);
   that post-run rig change is the f2 result-fit `TRACK0_INSILICO.md` §3
   forbids — not the verdict that names it.
4. **VOID is a verdict about the RIG, not about §11-B.** §118 measured nothing
   about whether CE is load-bearing — its CE channel never reached the spiking
   substrate.
5. **The root cause is structural.** A numpy toy cannot have a CE-gradient
   channel into spiking weights — surrogate gradients (snnTorch / SLAYER) are
   required and absent by design ($0, no torch). The CE channel being a
   substrate no-op is the *expected* consequence of the $0 scope.
6. **SIM-CE's §3-letter "non_degenerate = True" is carried by a read-out, not
   the substrate.** `byte_acc = 0.5` is teacher-forced; the Ψ/tension/Φ
   trajectory is byte-identical to the *frozen* GPU-noCE cell;
   `weight_drift_mean_abs = 0.0`. The positive control did not control the
   substrate-learning question ⇒ VOID.
7. **A post-hoc `head_drift` metric does not rescue the verdict.** It measures
   movement of a downstream linear read-out head, NOT the recurrent spiking
   substrate `W` (which stays frozen for every CE cell). The §96 §4.5 question
   is about the substrate; a head that learns while `W` is frozen does not
   answer it. The VOID verdict rests on the pre-registered §3 partition + the
   substrate `weight_drift = 0.0` + `TRACK0_INSILICO.md` §2's CE-cell
   definition; it stands regardless of a read-out-head metric.
8. **Only SIM-noCE-STDP actually moves the substrate** (`weight_drift` 0.235,
   event-local STDP-as-ΔW — the §117 mechanism). Its §9 5/5 is a
   substrate-LIVENESS reading, NOT a byte-level coherence reading — liveness ≠
   capability (§117 inherited).
9. **All four cells fail the byte-level §96 §4.5 predicate.** `byte_acc` is 0.0
   (the only substrate-learning cell) or a teacher-forced artifact (0.5). A
   240-unit toy LIF net cannot carry a byte-level prediction predicate —
   design-open #1 (attention replacement) is unresolved.
10. **WALL-B is inherited, not removed** (§117 / §115 / §95). §118 confronts at
    most the learning-channel half — at toy scale it does not even confront
    that; it confirms the blocker (§96 design-open #1).
11. **WALL-A (§1.1 data-regime) is orthogonal and untouched** (§97).
12. **central blue_falsifier.py 0-line-diff.** §118's battery is a sidecar
    (`blue_falsifier_s118.py`); central `state/verify_hexad_blue_2026_05_15/
    blue_falsifier.py` is untouched — sha256 prefix `c93e160a8a376a94`.
13. **f1/f2 safe.** LIF/STDP cited by hexa-bio NEURO.tape own invariants +
    standard neuroscience; NO σ(6)=12 / τ(6)=4 / φ(6)=2 / J₂(6)=24 derivation;
    Ψ=½ = anima g2 internal-arch carve-out.
14. **north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달.** §118 is an
    honest in-silico measurement that confirms a prerequisite; it is not an
    emergence step. necessary-not-sufficient (B-EMERGE-7).
