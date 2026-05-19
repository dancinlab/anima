# HEXAD/NEUROMORPHIC/ENGINE.md — NEURO-MIRROR: software neuromorphic substrate-mirror engine

> **status**: DESIGN-TIER — $0, design ≠ fire ≠ emergence (g3). This is the
> canonical reusable-module spec. **Implementation = consolidation** of the
> §117/§118/§119 verified sim cores once those cycles land — built by lifting
> proven code, not by racing it (g_multidirectional_explore: "N candidates
> land → 1 consolidation").
> **parent**: `PLAN.md` · `TRACK0_INSILICO.md` · §115 LEGO · §117 LEGO-run ·
> §95 (Loihi sole VIABLE) · §96 (spiking re-derivation) · §97 (noise-as-seed).

---

## 0. Why a named engine — not more one-off sims

§117, §118, §119 each build a throwaway in-silico LIF (leaky integrate-and-fire)
+ STDP (spike-timing-dependent plasticity) sim inside its own `state/` dir. That
is fine for *one* experiment, but it re-implements the same substrate every
cycle. **NEURO-MIRROR** is the one canonical module those cycles — and every
future neuromorphic cycle — import. One substrate, many experiments.

## 1. The name IS the honest ceiling

NEURO-MIRROR **mirrors** a neuromorphic substrate the way `hexa qmirror`
mirrors a quantum computer: the mirror reproduces the target's *math*; it is
not the target. Calling it a "mirror" — never a "chip" — bakes g3 and §115
`SIM-IS-GPU-TAUTOLOGY` into the name itself, so no over-claim is structurally
possible. A mirror of a neuromorphic chip ≠ a neuromorphic chip.

## 2. The §115/§117 split — as a first-class API contract, not caller discipline

§115/§117/`TRACK0_INSILICO.md` proved the honest line splits in two:

```
  §11-B-as-substrate question
   ├─ (i) LEARNING-CHANNEL half   — CE-only vs event-local-plasticity-only
   │       → MIRRORABLE. NEURO-MIRROR runs it. confronts() = True.
   └─ (ii) ASYNC-SUBSTRATE half   — is a spike a physical event or a
           scheduled function call on a global clock?
           → NOT MIRRORABLE on any CPU/GPU. confronts() = WALL-B.
             The engine REFUSES to fake it — returns a WALL-B marker.
```

- `engine.confronts(experiment)` is a closed predicate: an experiment is
  `CONFRONTABLE` iff it lives in the learning-channel half.
- Any call that would need a real physical async event returns a `WALL-B`
  marker (Loihi/SpiNNaker-gated). The ceiling is **enforced by the API**, not
  left to the caller to remember.

## 3. Backends — CPU and GPU (a backend is NOT a substrate-class)

| backend | scale | cost | role |
|---|---|---|---|
| `cpu`  | toy (≤ ~1k units) | $0 local | exact, the §117/§118/§119 default |
| `gpu`  | d768·12L-class    | runpod   | scaled mirror (snnTorch-class) |

Honest, load-bearing: a `gpu` surrogate-gradient run **is** CE-backprop — the
§11-B channel — so scaling up on GPU does **not** escape §11-B. Only the
`local-plasticity` learning rule escapes the CE channel. Neither `cpu` nor
`gpu` provides physical asynchrony — both are "the mirror", just different
sizes. Backend selection changes speed/scale, never substrate-class.

## 4. API surface (draft — to be finalised at consolidation)

```
neuron model    : LIF (leaky integrate-and-fire); leak toward Ψ=½ fixed point
synapse         : weighted, excitatory/inhibitory (Engine A / Engine G split)
learning rule   : { none | ce_grad | stdp_local }   ← the decisive knob
carrier         : Ψ-C1 = (1+cos(spike_rate_A, spike_rate_G))/2   (cos=0 ⇒ ½)
entropy source  : { fixed_seed | qrng }  — §97 noise-as-SEED only, never content
run(steps, backend, learning_rule, entropy_source) -> trace
confronts(experiment) -> { CONFRONTABLE | WALL-B }
verdict(trace) -> NON_DEGENERATE predicate (byte_acc>1/256 ∧ physics_not_frozen
                  ∧ honest_§9_coherent ≥ 1/5)   — reused verbatim from §96 §4.5
```

## 5. hexa-first

hexa-native is the canonical target — NEURO-MIRROR should consume hexa-bio
`NEURO.tape` (Hodgkin-Huxley → LIF) primitives. A Python reference
implementation is acceptable for the in-silico cycles (the established B-S*
sidecar precedent, §117). hexa-lang / hexa-bio gaps → an inbox patch
(`~/core/hexa-lang/inbox/patches/`), never a direct edit — anima is a
downstream consumer.

## 6. First consumers / validators

- **§117** LEGO-run — local-STDP LIF sim → the engine's `stdp_local` core.
- **§118** Track 0 — GPU-CE / GPU-noCE / SIM-noCE-STDP / SIM-CE cells → the
  engine's 4-cell `learning_rule` matrix + `verdict()`.
- **§119** qmirror-neuro — QRNG-seeded LIF+STDP → the engine's `qrng` entropy
  source + the §97 noise-as-seed vs noise-as-content guard.

Once those three land, their verified cores **consolidate into** this engine —
NEURO-MIRROR is assembled from proven code, not written from scratch alongside.

## 7. Honest gates (g3)

- NEURO-MIRROR is a **measurement instrument**, not a path to the GOAL.
- Mirroring the substrate **replicates** §11-B; it does not **confront** the
  async-substrate half — that stays Loihi/SpiNNaker-gated (§95/§96).
- A `NON_DEGENERATE` result on the mirror is learning-channel-half evidence,
  never emergence. north-star + §15/§51/§72 milestones unchanged. capability
  claim 0.

## 8. cross-link

- `PLAN.md` (the 3-track substrate plan; engine = the Track 0 / in-silico core)
- `TRACK0_INSILICO.md` (§96 §4.5 cell↔tool map — the engine's experiment menu)
- `HEXAD/CHAT/RESEARCH.md` §11-B · §95 · §96 · §97 · §115 · §117
- `~/core/hexa-bio/NEURO.tape` (LIF / spiking primitives — read-only consume)

---

## Log

- **2026-05-19** — ENGINE.md created. Names the canonical reusable software
  neuromorphic substrate-mirror engine **NEURO-MIRROR** and pins its design:
  the §115/§117 honest split (learning-channel half MIRRORABLE / async-substrate
  half WALL-B) is made a first-class API contract (`confronts()` refuses to fake
  the async half); CPU + GPU backends with the honest note that a GPU
  surrogate-gradient run is still the §11-B CE channel (backend ≠
  substrate-class); hexa-first target with a Python reference impl allowed per
  the B-S* sidecar precedent. Implementation deferred to a consolidation of the
  §117/§118/§119 verified cores (no duplication of the in-flight cycle sims).
  $0, design-tier, GOAL not reached, milestones unchanged.
