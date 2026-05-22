# engine — historical log

> Spec at [./ENGINE.md](./ENGINE.md).

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
