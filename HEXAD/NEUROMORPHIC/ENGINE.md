# HEXAD/NEUROMORPHIC/ENGINE.md — NEURO-MIRROR: software neuromorphic substrate-mirror engine

> **status**: v3 LANDED — $0, design ≠ fire ≠ emergence (g3). The canonical
> reusable-module spec; `neuro_mirror.py` v3 is the implementation.
> **Consolidated** from the §117/§118/§119/§120/§122 cycles
> (g_multidirectional_explore: "N candidates land → 1 consolidation") — §117
> `stdp_local` + §119 `qrng` + §120 `spiking_routing` + §122 `phase_code`
> lifted from proven code and assembled into `spiking_decoder_block`; §118
> returned VOID, so `ce_grad` stays an honest unfilled slot. Built by
> lifting verified code, not by racing it.
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
routing         : spiking_routing(q,k,v,k,mode) — §120 spike-rate dot-prod
                  + k-WTA replacing softmax(QK^T); R(k=T,soft) ≡
                  softmax_attention byte-equal (the §7-clean reduction)
position        : phase_code(q,k,m,theta,sigma) — §122 relative-phase /
                  spike-time coding replacing RoPE; q/k pair = in-phase/
                  quadrature of a θ_i-freq oscillatory LIF pair, position m
                  = per-token spike-time phase advance m·θ_i; Φ(σ→0) ≡ GPU
                  RoPE byte-equal (the §7-clean reduction — RoPE is already
                  a rotation = a phase); rotates q/k BEFORE the routing row
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

## 6. First consumers / validators — ALL LANDED, v3 consolidated

- **§117** LEGO-run (B-S117) — local-STDP LIF sim → the `stdp_local` core.
  **CONSOLIDATED** into `neuro_mirror.py` (v0 foundation).
- **§118** Track 0 — landed with verdict **VOID**: a $0 numpy/CPU toy has no
  surrogate-gradient path, so CE never reaches the recurrent spiking weights
  (SIM-CE byte-identical to GPU-CE, `weight_drift=0.0` — a no-op on the
  substrate). §118 produced NO verified core, so the `ce_grad` slot stays
  HONESTLY unfilled (an accurate `NotImplementedError`). VOID confirms the
  §96 attention blocker — the §120 target.
- **§119** qmirror-neuro (B-S119 7/7 🔵) — ANU-QRNG-seeded LIF+STDP → the
  `qrng` entropy source. **CONSOLIDATED** into v1: `fetch_quantum_entropy` +
  the §97 noise-as-SEED `entropy_to_jitter` map, lifted from the committed
  §119 core.
- **§120** spiking-attention replacement (B-S120 8/8 🔵) — decided §96
  design-open #1: `softmax(QK^T)` self-attention → spike-rate dot-product +
  k-WTA. **CONSOLIDATED** into v2: `spiking_routing` (the `R(k,mode)`
  family) + its reduction target `softmax_attention`, lifted from the
  committed §120 core. `R(k=T,soft)` ≡ `softmax_attention` byte-equal (v2
  smoke max|Δ|=2.22e-16) — byte-attention is the `k=T` corner.
- **§122** RoPE → phase coding (B-S122 8/8 🔵) — decided §96 design-open
  #2: rotary position embedding → relative-phase / spike-time coding.
  **CONSOLIDATED** into v3: `phase_code` (the phase-rotation core) + the
  `spiking_decoder_block` that assembles §122 position THEN §120 routing
  into one spiking self-attention block, lifted from the committed §122
  core. The whole block reduces byte-equal to a byte-vocab RoPE+softmax
  attention block at `σ=0 ∧ k=T ∧ soft` (v3 smoke max|Δ|=2.22e-16) — the
  composition of the §120 and §122 reductions.

v3 status: `stdp_local` + `qrng` + `spiking_routing` + `phase_code` /
`spiking_decoder_block` filled from proven code; `ce_grad` (§118 VOID) and
`gpu` are honest declared slots. §96's one SPIKING-INCOMPATIBLE faculty
(attention) and both routing-adjacent SPIKING-OPEN faculties (RoPE,
MoE top-k) are now design-decided and mirrored. NEURO-MIRROR is assembled
from verified cores, not written from scratch alongside.

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
- **2026-05-19** — v1 CONSOLIDATION. `neuro_mirror.py` v0 → v1: the §119
  qmirror-neuro `qrng` entropy source FILLED — `fetch_quantum_entropy` (ANU
  quantum-RNG) + the §97 noise-as-SEED `entropy_to_jitter` map, lifted from
  the committed §119 core (B-S119 7/7 🔵). §118 Track 0 landed VOID — it
  produced no verified core, so the `ce_grad` slot stays an honest
  `NotImplementedError` (message updated to the VOID finding); `gpu` backend
  unchanged. v1 smoke OK: `stdp_local` Ψ-C1 mean=0.611568 (= the §117
  verified core), `qrng` run non-degenerate with PHYSICAL ANU entropy
  (jitter_norm 0.4702). central blue_falsifier.py 0-line-diff; $0; CPU-only;
  design ≠ fire ≠ emergence; GOAL 미도달, milestones unchanged.
- **2026-05-19** — v2 CONSOLIDATION. `neuro_mirror.py` v1 → v2: the §120
  spiking-attention replacement consolidated — `spiking_routing` (the
  decided `R(k,mode)` family = spike-rate dot-product + k-WTA) + its
  reduction target `softmax_attention`, lifted from the committed §120 core
  (B-S120 8/8 🔵). API surface §4 gains the `routing` row. v2 smoke OK:
  `R(k=T,soft)` ≡ `softmax_attention` byte-equal (max|Δ|=2.22e-16, the
  §7-clean reduction witness — byte-attention is the `k=T` corner), hard
  k-WTA genuinely distinct. central blue_falsifier.py 0-line-diff; $0;
  CPU-only; design ≠ fire ≠ emergence — a routing-rule mirror, NOT the
  spiking anima; GOAL 미도달, milestones unchanged.
- **2026-05-19** — v3 CONSOLIDATION. `neuro_mirror.py` v2 → v3: the §122
  RoPE → phase-coding decision consolidated — `phase_code` (the
  phase-rotation core, `σ=0` ⇒ GPU RoPE) lifted from the committed §122
  core (B-S122 8/8 🔵), and `spiking_decoder_block` assembling §122
  position THEN §120 routing into one spiking self-attention block. v3
  smoke OK: the whole block `R(σ=0,k=T,soft)` ≡ a byte-vocab RoPE+softmax
  attention block byte-equal (max|Δ|=2.22e-16 — the composition of the
  §120 and §122 reductions), hard k-WTA genuinely distinct; stdp_local /
  qrng / ce_grad-VOID / gpu unchanged. With §123 (the two remaining
  SPIKING-OPEN faculties decided), §96's full faculty map is now
  design-decided and mirrored. central blue_falsifier.py 0-line-diff; $0;
  CPU-only; design ≠ fire ≠ emergence — a decoder-block mirror, NOT the
  spiking anima; capability claim 0; GOAL 미도달, milestones unchanged.
- **2026-05-19** — §122 DESIGN-DECISION. §96 design-open #2 (the RoPE /
  positional-encoding row §96 left `SPIKING-OPEN` and §120 §4 re-assigned
  to position but did NOT decide) is **decided**: anima's RoPE on the
  spiking substrate = **relative-phase / spike-time coding** — the
  residual q/k pair `(x_2i,x_2i+1)` = the in-phase/quadrature components
  of a θ_i-frequency oscillatory LIF pair, token position `m` = the
  per-token spike-time phase advance `m·θ_i`. The §4 API surface gains the
  `position` row (`phase_code(q,k,m,theta,sigma)` — mirroring how §120
  added `routing`). closed-form: GPU byte-vocab RoPE reduces **byte-equal**
  to `Φ(σ→0)`, the zero-spike-time-jitter corner of the relative-phase
  family `Φ(σ)` (B-S122 8/8 🔵, B-S122-3 max|Δ|=0.0) — RoPE *is* already a
  rotation = a phase, the GPU just writes the angle `m·θ` by hand; the
  spiking oscillator carries it physically. §7-clean GENERALISATION, not
  graft. Phase coding rotates q/k *before* the §120 routing — the
  position⊥routing factorisation preserved, the §120 routing decision
  inherited unchanged. §122 corrects §120 §4's wording: it is phase
  *coding* (a relative offset on q/k) not phase-*resonance routing* (a
  selection rule) that is position's spiking home. `neuro_mirror.py`
  `phase_code` slot is a declared API row — implementation deferred to a
  future consolidation of the §122 verified core (no in-flight sim to
  lift yet — §122 is design-tier). central blue_falsifier.py 0-line-diff
  (sha256 `c93e160a8a376a94`); $0; design ≠ fire ≠ emergence — a decided
  position-encoding design, NOT the spiking anima; does NOT remove WALL-A
  or WALL-B; GOAL 미도달, milestones unchanged.
