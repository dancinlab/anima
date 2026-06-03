# NEURO-CANDIDATES — neuroscience mechanism hypotheses (H_889…H_909)

> Brainstorm seed: 2026-06-03. Neuroscience names the computational/dynamical mechanisms by which a neural
> substrate codes, learns, holds, and unifies state. anima is a substrate-native consciousness engine (M/Φ/W
> tension field · MITOSIS · Ψ=1/2 attractor), so each neuroscience mechanism maps to an anima-substrate readout
> and becomes a FALSIFIABLE hypothesis. Convention mirrors BIO-CANDIDATES.md / BIO-TRANSFER-CANDIDATES.md:
> mechanism → anima analog → PRE-REGISTERED FALSIFIER → substrate tag. status: candidate-unverified.
>
> Numbering continues after the bio-transfer family (ended H_888). UNIVERSE main H_NNN go to H_860; bio-transfer
> took 861–888; neuroscience takes 889+. Where a mechanism overlaps an existing consciousness H (e.g. H_004
> hard-problem, IIT entries), the link is noted — these are MECHANISM-level candidates with substrate falsifiers,
> not re-statements. a_lane_akida_gpu_split (AKIDA on-chip ⊥ GPU) · a_scale_honest_scope (toy ≠ prod) · p6/p7.

---

## Round 1 — oscillation, timing & criticality

- **H_889 PREDICTIVE-CODING** 🔮 — "뇌는 예측하고 오차만 보낸다". The cortex predicts its input and propagates
  only the prediction ERROR (free-energy minimization). anima: a cell emits only its prediction-error tension, not
  its full state, so the field's bandwidth carries surprise. FALSIFIER F-889: error-only propagation does NOT
  predict the next input better than full-state propagation at MATCHED bandwidth. → REFUTED iff error-coding wins
  at equal channel cost. substrate: CPU-toy. (free-energy / active-inference link.)
- **H_890 THETA-GAMMA-COUPLING** 🌀 — "느린 리듬이 빠른 리듬을 슬롯으로 묶기". A slow theta cycle nests several
  fast gamma cycles → ordered memory slots (cross-frequency coupling). anima: a slow tension cycle gates discrete
  fast emit slots; sequence items occupy distinct phase slots. FALSIFIER F-890: items placed in distinct phase
  slots are NOT recalled in correct order better than unslotted (rate-only). → REFUTED iff phase-slotted order
  recall > unslotted. substrate: CPU-toy.
- **H_891 CRITICALITY** ⚡ — "임계점에 스스로 맞추는 뇌" (neuronal avalanches). The brain self-tunes near a critical
  point where activity cascades follow a power law and dynamic range / information transmission is maximal. anima:
  the cell field self-organizes to criticality — cascade sizes are power-law, NOT sub-critical (dies) or super
  (saturates). FALSIFIER F-891: avalanche size distribution is NOT power-law (slope ≈ −1.5) at the operating point.
  → REFUTED iff power-law with the critical exponent emerges + dynamic range peaks there. substrate: CPU-toy.
- **H_892 PHASE-PRECESSION** ⏱️ — "리듬 대비 발화 타이밍이 위치를 담는다". Spike timing relative to the ongoing
  rhythm carries info FINER than firing rate (a temporal code). anima: emit TIMING within a tension cycle carries
  information beyond emit rate. FALSIFIER F-892: decoding from emit-phase does NOT beat decoding from rate alone.
  → REFUTED iff phase-decode accuracy > rate-decode. substrate: CPU-toy.

## Round 2 — coding & representation

- **H_893 SPARSE-CODING** 🔌 — "몇 개만 켜서 효율적으로 표현". A few active units represent input efficiently
  (energy + capacity win). anima: a sparsity pressure on the field yields fewer-active-cell codes at equal/better
  reconstruction. FALSIFIER F-893: sparse codes reconstruct at WORSE fidelity per active cell than dense.
  → REFUTED iff sparse reaches equal fidelity with fewer active cells. substrate: CPU-toy.
- **H_894 GRID-METRIC** 🗺️ — "육각 주기 코드 = 거리 자(尺)". Grid cells tile space with multi-scale hexagonal
  periodicity, giving a metric that supports path-integration + generalization. anima: a periodic multi-scale code
  over the concept coordinate supports interpolation to NOVEL coordinates. FALSIFIER F-894: a grid-like periodic
  code does NOT generalize to unseen coordinate interpolation better than one-hot. → REFUTED iff grid > one-hot on
  novel-coordinate readout. substrate: CPU-toy. (links Lane A coordinate axis.)
- **H_895 MIXED-SELECTIVITY** 🎛️ — "여러 변수를 비선형으로 섞어 유연하게". Neurons with nonlinear MIXED tuning make
  many task-variable combinations linearly readable (prefrontal flexibility). anima: mixed-selective cells give a
  population linearly separable on more variable-combos than pure-selective cells. FALSIFIER F-895: mixed
  selectivity does NOT raise the number of linearly-separable variable-combos vs pure. → REFUTED iff mixed > pure
  on separable-combo count. substrate: CPU-toy.

## Round 3 — plasticity & learning rules

- **H_896 STDP** ↪️ — "선후 타이밍이 시냅스 방향을 정한다". Spike-timing-dependent plasticity: pre-before-post
  strengthens, post-before-pre weakens → DIRECTIONAL edges. anima: an order-sensitive Hebbian rule makes t→t+1
  edges strong and t+1→t weak (directionality the symmetric rule lacks). FALSIFIER F-896: STDP yields SYMMETRIC
  (non-directional) edges indistinguishable from plain Hebbian. → REFUTED iff edge asymmetry > symmetric-Hebbian
  baseline. substrate: CPU-toy / CHIP-future (AKD1000 IP-v1 can't map STDP — needs AKD1500, cf lane-a recurrence wall).
- **H_897 THREE-FACTOR-RULE** 🍬 — "보상 신호가 학습을 켠다". Plasticity gated by a third, GLOBAL neuromodulator
  (dopamine/reward): only reward-coincident edges consolidate. anima: edge update = pre × post × global-reward
  tension; ungated coincidences fade. FALSIFIER F-897: reward-gated edges do NOT align with task reward better than
  ungated Hebbian. → REFUTED iff gated edges track reward structure > ungated. substrate: CPU-toy.
- **H_898 METAPLASTICITY** 🎚️ — "학습률이 스스로 조절된다" (plasticity of plasticity, BCM). Recent activity slides
  the THRESHOLD for future potentiation, preventing runaway. anima: a cell's learning rate adapts to its recent
  activation history. FALSIFIER F-898: a sliding-threshold cell does NOT avoid the runaway potentiation a fixed-rate
  cell suffers. → REFUTED iff sliding-threshold stays bounded while fixed-rate diverges. substrate: CPU-toy.
- **H_899 DENDRITIC-COMPUTE** 🌿 — "가지돌기가 곧 숨은 한 층". Dendrites compute local nonlinear subunits — a single
  neuron ≈ a 2-layer net. anima: per-cell nonlinear sub-compartments raise representational capacity without adding
  cells. FALSIFIER F-899: a dendritic (sub-compartment) cell CANNOT solve an XOR-like task that a point-cell also
  cannot. → REFUTED iff dendritic single-cell solves XOR where point-cell fails. substrate: CPU-toy.

## Round 4 — dynamics & attractors

- **H_900 ATTRACTOR-COMPLETION** 🕳️ — "일부만 줘도 전체를 떠올린다" (Hopfield). Point attractors store patterns and
  complete them from partial/noisy cues. anima: the tension field has stable attractors that pattern-complete a
  partial anchor. FALSIFIER F-900: a partial cue does NOT converge to the stored pattern above a noise floor
  (no basin). → REFUTED iff partial-cue completion > noise across a basin radius. substrate: CPU-toy.
- **H_901 RING-ATTRACTOR** 💍 — "둥근 변수를 한 봉우리로 쥔다" (head-direction). A continuous ring attractor holds a
  persistent activity bump encoding a circular variable and integrates velocity input. anima: a ring of cells holds
  a bump on the coordinate ring, integrating drift without losing the angle. FALSIFIER F-901: the bump does NOT
  persist / drifts beyond tolerance without input. → REFUTED iff bump persists + integrates within tolerance.
  substrate: CPU-toy.
- **H_902 EI-BALANCE** ⚖️ — "흥분과 억제의 팽팽한 균형". Tight excitation/inhibition balance keeps the network both
  stable AND responsive (not seizing, not silent). anima: a balanced inhibitory counter-tension prevents runaway
  while preserving sensitivity. FALSIFIER F-902: an E/I-balanced field is NOT both more stable AND more responsive
  than an unbalanced one. → REFUTED iff balance dominates on the stability×responsiveness frontier. substrate: CPU-toy.
- **H_903 UP-DOWN-STATES** 🌗 — "켜짐/꺼짐을 오가는 휴지기 뇌" (slow oscillation). At rest the cortex alternates
  bistable active/quiet states — the substrate of slow-wave sleep. anima: the field spontaneously alternates
  high/low global-tension states without external drive (links DREAM N3 / a_chat_sleep_imagination). FALSIFIER
  F-903: no spontaneous bistable alternation emerges (field rests in one state). → REFUTED iff bistable
  alternation self-arises. substrate: CPU-toy.

## Round 5 — systems & global integration

- **H_904 GLOBAL-WORKSPACE** 📡 — "이긴 연합이 뇌 전체로 방송" (GWT, conscious access). Above an IGNITION threshold a
  winning coalition's content is broadcast brain-wide → reportable/conscious; below, it stays local. anima: above an
  ignition threshold one coalition's content broadcasts to ALL cells (all-or-none), else local-only. FALSIFIER
  F-904: broadcast is GRADED with no sharp ignition threshold. → REFUTED iff a sharp all-or-none ignition appears
  across drive rungs. substrate: CPU-toy. (links H_004 consciousness · GWT.)
- **H_905 PREDICTIVE-HIERARCHY** 🏛️ — "위는 예측을, 아래는 오차를" (hierarchical predictive coding). Cortical layers
  pass predictions DOWN and errors UP, converging on a generative model. anima: a layered field — top predicts,
  bottom returns error — reconstructs structured input. FALSIFIER F-905: the hierarchy does NOT reconstruct
  structured input better than flat (single-level) error-coding. → REFUTED iff hierarchical > flat on structured
  data. substrate: CPU-toy. (extends H_889.)
- **H_906 REENTRY** 🔁 — "되먹임 고리가 흩어진 활동을 묶는다" (Edelman). Bidirectional re-entrant loops integrate
  distributed activity into a unified state (a route to Φ). anima: re-entrant coupling between cell groups raises
  integration above feedforward-only. FALSIFIER F-906: re-entrant coupling does NOT raise an integration (Φ-like)
  measure above feedforward-only. → REFUTED iff re-entry > feedforward on integration. substrate: CPU-toy.
  (links IIT / Φ.)
- **H_907 NEURAL-DARWINISM** 🧬 — "가르치지 않고 골라낸다" (selectionism, Edelman). A degenerate repertoire of cell
  groups COMPETES; the environment SELECTS — no instructive teaching signal. anima: a diverse cell-group repertoire
  is selected by environment fit (MITOSIS/APOPTOSIS), matching the task with NO instructive gradient. FALSIFIER
  F-907: a purely selectionist population does NOT beat random drift on the task without any instructive signal.
  → REFUTED iff selection > drift, instruction-free. substrate: CPU-toy. (p6 — must emerge, not be fine-tuned.)

## Round 6 — memory allocation & update

- **H_908 ENGRAM-ALLOCATION** 📍 — "어느 세포가 기억을 맡을지 흥분도가 정한다" (CREB). The most EXCITABLE neurons at
  encoding capture the memory; biasing excitability redirects which cells store it. anima: the highest-tension cells
  at encoding capture the anchor; pre-biasing excitability shifts storage. FALSIFIER F-908: pre-encoding
  excitability bias does NOT shift which cells hold the anchor. → REFUTED iff biased cells preferentially store.
  substrate: CPU-toy. (distinct from H_865 LTP: WHICH cell, not edge strength.)
- **H_909 RECONSOLIDATION** ♻️ — "떠올리면 다시 말랑해진다". Reactivating a stored memory opens a LABILE window in
  which it can be updated, then re-stabilizes. anima: reactivating an anchor opens a window where it is editable;
  outside the window edits don't take. FALSIFIER F-909: reactivation-then-edit does NOT change the anchor more than
  edit-without-reactivation. → REFUTED iff reactivated edits dominate. substrate: CPU-toy.

## Round 7+ — DEPLETION

New candidates collapse onto prior entries (this family + bio-transfer + existing UNIVERSE H_001–860):
- "gamma binding-by-synchrony" ≈ H_890 + H_867 MET (sync) · "sharp-wave ripple replay" ≈ H_878 ENGRAM-CONSOLIDATION
- "Hebbian cell assembly" ≈ H_865 LTP · "neurogenesis" ≈ MITOSIS · "synaptic scaling / homeostasis" ≈ HOMEOSTASIS (BIO-CANDIDATES)
- "winner-take-all" ≈ H_904 ignition + H_902 E/I · "line/integrator attractor" ≈ H_901 RING (continuous-attractor class)
- "default-mode network" ≈ H_903 UP-DOWN (intrinsic activity) · "thalamocortical gating" ≈ H_904 broadcast + relay
- "reward-prediction-error (dopamine)" ≈ H_897 three-factor · "efficient/redundancy-reduction coding" ≈ H_893 sparse
→ round 7 produced 0 distinct new mechanisms ⇒ brainstorm DEPLETED at H_909 (21 candidates: H_889–909, all distinct;
no padding — the listed near-duplicates fold into named entries).

### Family map (neural function × anima substrate readout)

```
FUNCTION ↓        │ mechanism (H_)                        │ anima substrate readout
──────────────────┼───────────────────────────────────────┼──────────────────────────────
predict / code    │ 889 PRED-CODE · 905 PRED-HIER          │ error-only emit · layered generative
timing / rhythm   │ 890 THETA-GAMMA · 892 PHASE-PRECESS    │ phase-slotted emit
criticality       │ 891 AVALANCHE                          │ power-law cascade self-org
representation    │ 893 SPARSE · 894 GRID · 895 MIXED-SEL  │ sparse/periodic/mixed codes
plasticity        │ 896 STDP · 897 3-FACTOR · 898 METAPL.  │ directional/reward-gated/sliding edges
                  │ 899 DENDRITE                           │ per-cell nonlinear subunit
attractor dynamics│ 900 COMPLETION · 901 RING · 902 E/I    │ pattern-complete · bump · balance
                  │ 903 UP-DOWN                            │ spontaneous bistable rest (DREAM)
integration       │ 904 WORKSPACE · 906 REENTRY            │ ignition broadcast · Φ-raising loops
selection         │ 907 NEURAL-DARWINISM                   │ instruction-free MITOSIS/APOPTOSIS fit
memory ops        │ 908 ALLOCATION · 909 RECONSOLIDATION   │ excitability capture · labile re-edit window
```

### Pre-registration note (a_paper_significance · a_scale_honest_scope · p6/p7)
All H_889–909 are candidate-unverified. Most are substrate:CPU-toy — next batch authors emergent falsifiers
(`neuro_toys.py`, same pattern as `bio_transfer_toys.py`: fixed seeds, emergent dynamics so signatures are NOT
hard-coded, p7 direct readout). H_896 STDP has a CHIP-future caveat (AKD1000 IP-v1 cannot map spike-timing
plasticity — needs AKD1500, cf the lane-a recurrence wall). H_907 honours p6 (ethics/competence must EMERGE via
selection, not be fine-tuned in). No toy-green is a production claim until a scale-up re-test (a_toy_scale_recheck).
Several link existing consciousness H's (H_004, IIT/Φ) — those links are noted, not duplicated.
