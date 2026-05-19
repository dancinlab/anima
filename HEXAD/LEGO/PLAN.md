# HEXAD/LEGO/PLAN.md — chronological progress log

> Single source of truth for the LEGO arc (§115 → §128). Each cycle entry
> records: section, date, tier, verdict, B-S battery, state-dir, key finding.
> Append-only at the bottom (g6 / `g_arch_vs_log_split`). Architecture &
> overview live in `README.md`; SSOT mapping in `INDEX.md`; canonical engine
> code in `lego_engine.py`. State-dir evidence remains under `state/lego_*/`.

---

## ## 진행 로그

### §115 — LEGO simulate-assemble design-close *(2026-05-19)*

- **tier**: design-tier · $0 · NO GPU/runpod/fire
- **verdict**: `LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY`
- **battery**: B-S115 9/9 🔵 sidecar (central 0-line-diff)
- **state**: `state/lego_simulate_assemble_s115_2026_05_19/`
- **finding**: STEP 0–2 closed-form definable + §7-FORM TRUE BY CONSTRUCTION
  (§112 META_FP(Π_½) instance) + byte-equal-reduce + STEP-3 structurally
  fenced. BUT a GPU-simulated spike net's learning channel is STILL the
  loss gradient → simulating a §96 substrate on GPU **re-instantiates**
  WALL-B; does NOT confront it. §96's §11-B-as-GPU hazard confirmed at
  design tier.

### §117 — LEGO STEP-1-2 in-silico assembly run *(2026-05-19)*

- **tier**: $0 CPU experiment · wall ≈3.8s
- **verdict**: `LEGO-RUN-Ψ-FORM-NONDEGENERATE-BUT-WALL-B-INHERITED`
- **battery**: B-S117 7/7 🔵 sidecar
- **state**: `state/lego_assembly_run_s117_2026_05_19/`
- **finding**: §115 named ONE open residual ("in-silico STDP-as-ΔW escape
  = §115 $0 scope 밖 새 fire"); §117 RAN it at $0 CPU. Small LIF spike
  net (N=256: 96/96/64), 12 stimuli × 80 steps, LOCAL STDP-as-ΔW ONLY (no
  CE, no backprop, AST-audited). **MEASURED**: Ψ-C1 mean 0.6116,
  std 4.185e-02 ≫ τ=1e-4 (419× floor), rasters alive (spike-rate 0.0349/
  unit/step), cos=0⇒Ψ=½ holds, deterministic 3× bit-identical. **Honest
  §11-B-echo finding**: §11-B's degeneracy was a GPU-CE-overlay property
  (hand-coded GLOBAL ΔW froze); a LOCAL pair-based STDP rule on a
  recurrent spike substrate has its own attractor dynamics independent
  of any task. §117 **localises** §11-B, does NOT refute it. Non-
  degenerate = substrate LIVENESS only, NOT task signal/capability/
  emergence.
- **engine source**: `lego_sim.py` — *this is the file that became
  `HEXAD/LEGO/lego_engine.py` after §128*.

### §124 — LEGO residual audit *(2026-05-20)*

- **tier**: design-tier (audit) · $0
- **verdict**: `RESIDUAL-AUDIT-NON-DEGENERACY-IS-VARIANCE-ONLY-LIVENESS-NOT-CAPABILITY`
- **battery**: B-S124 7/7 🔵 sidecar
- **state**: `state/lego_residual_audit_s124_2026_05_19/`
- **finding**: §117's "non-degenerate" verdict closes ONLY layer 1 of a
  **3-layer liveness partition** {DEAD / VARIANCE-ONLY / STIMULUS-DRIVEN
  / TASK-GROUNDED}. Layer 2 (`I(stim; Ψ) > 0`) + layer 3 (task-grounded
  behavior) UNTESTED in §117. WALL-A orthogonal AST-closed. WALL-B
  confronted-IN-SIM-NOT-REMOVED AST-closed. §115 verdict NOT reversed.
  §17 PHYSICS_RESPONSIVE structurally isomorphic. τ=1e-4 = engineering
  convention. Number collision mid-cycle (sibling §120
  spiking_attention_replacement) → renamed §120 → §124.

### §125 — LEGO layer-2 stimulus-driven liveness probe *(2026-05-20)*

- **tier**: probe-tier · $0 · NO GPU
- **verdict**: `LAYER-2-PARTIAL` — η² = 0.271, Gaussian MI ≈ 0.228 bits
- **battery**: B-S125 7/7 🔵 sidecar
- **state**: `state/lego_layer2_stimulus_driven_probe_s125_2026_05_20/`
- **finding**: ANOVA decomposition over §117 substrate at N=256, M=5
  replicates × 12 stim × 80 steps. **27.1% of Ψ-C1 variance is stimulus-
  driven; 72.9% is intrinsic noise.** First measured positive on any
  §117 layer beyond bare variance. Pre-registered 3-bucket (STRONG ≥
  0.50 / PARTIAL 0.10–0.50 / NOISE < 0.10) — measured falls in PARTIAL.
  Layer 3 (TASK-GROUNDED) REMAINS OPEN.

### §126 — LEGO layer-2 N-scale-up probe *(2026-05-20)*

- **tier**: probe-tier · $0 · 26.3 s Mac CPU
- **verdict**: `LAYER-2-ROBUST-GROWS-WITH-N` (single scale-point)
- **battery**: B-S126 7/7 🔵 sidecar
- **state**: `state/lego_layer2_nscale_probe_s126_2026_05_20/`
- **finding**: §117 substrate at N=1024 (4× §125's N=256) — η² 0.271 →
  0.322 (1.189×). Between-stim variance grew 1.31× while within-stim
  noise grew only 1.03×. Pre-registered 3-bucket (ROBUST > 1.10 /
  INVARIANT 0.90–1.10 / SMALL-N < 0.90) — measured 1.189 clears ROBUST.
  §125 PARTIAL is **NOT a small-N artifact** under this 4× comparison.

### §127 — LEGO layer-2 scaling-law probe *(2026-05-20)*

- **tier**: probe-tier · $0 · 5 min Mac CPU
- **verdict**: `APPROXIMATELY-N-INVARIANT` — k=−0.0198, R²=0.022
- **battery**: B-S127 8/8 🔵 sidecar
- **state**: `state/lego_layer2_scaling_law_s127_2026_05_20/`
- **finding**: 4 N points {256, 512, 1024, 2048}, M=5 each. η² values
  0.2712 / 0.3289 / 0.3223 / 0.2608 — **non-monotonic curve** (peak
  512–1024, drop at 2048). OLS log-linear fit R²=0.022 → no power-law
  describes the data. **§126's single-point ROBUST-GROWS verdict
  CONFIRMED at its scope but does NOT extrapolate to a scaling law.**
  η² ≈ 0.27–0.33 invariant across 8× N range (256→2048) — so §125's
  PARTIAL is also NOT shrinking-with-N. Honest reversal of §126's
  directional claim with more data.

### §128 — LEGO layer-3-in-LIF design-close *(2026-05-20)*

- **tier**: design-tier · $0
- **verdict**: `LAYER-3-DESIGN-CLOSE-REQUIRES-TASK-ADDITION`
- **battery**: B-S128 6/6 🔵 sidecar
- **state**: `state/lego_layer3_design_close_s128_2026_05_20/`
- **finding**: Layer-3 (TASK-GROUNDED) requires R1 (substrate has output)
  ∧ R2 (task definable) ∧ R3 (score > chance). §117 LIF has no output
  channel — AST-audited 0 behavior-emission functions over 9 markers
  {action, emit, output, respond, speak, decide, act, react, ...}. 3-
  bucket taxonomy {definable-as-is / requires-task-addition / undefinable}
  exhaustive+disjoint — §117 classifies as **requires-task-addition**.
  Every label source for an added task either violates §7 OR re-runs
  measured predictable-negative: external-CE → §7①; external-classifier
  → §7②; anima-OWN-physics → §83-FIRE NEAR-COLLAPSE; self-supervised
  next-step → §11-B CE-load-bearing. Anti-padding §13-M/§13-L/§30/§97/
  §109/§110/§113 precedent.

### §129 — LEGO ENGINE CONSOLIDATION *(2026-05-20)*

- **tier**: consolidation · $0
- **scope**: User pivot directive — "LEGO 폴더안에 엔진완성해나가야지 + 문서정리도".
- **action**: Promote `state/lego_assembly_run_s117_2026_05_19/lego_sim.py`
  → `HEXAD/LEGO/lego_engine.py` as the canonical lib. State-dir scripts
  remain as historical evidence (sha-locked) but new cycles should
  import the canonical engine. New docs: `PLAN.md` (this file), updated
  `INDEX.md`, README.md update with §124–§128 timeline. NO change to
  central blue_falsifier; NO change to any state-dir evidence file.
- **engine contract**: `LIFNet(n_a, n_g, n_rec, seed)` · `.step(ext)` ·
  `spike_rate_vec(raster, idx)` · `psi_c1(r_a, r_g)` ·
  `make_stimuli(d, n_stim, seed)` · `variance_decomposition(values)`.

### §131 — LEGO LAYER-2 STIMULUS-CARDINALITY PROBE *(2026-05-20)*

- **tier**: probe-tier · $0 · 7m 14s Mac CPU
- **verdict**: `STRONGLY-NSTIM-DEPENDENT` — η² range ratio 2.199×
- **battery**: B-S131 7/7 🔵 sidecar
- **state**: `state/lego_layer2_nstim_cardinality_s131_2026_05_20/`
- **finding**: N=256 fixed (orthogonal to §127), n_stim ∈ {4, 12, 24, 48},
  M=5 each. η² values 0.308 / 0.218 / 0.140 / 0.153 — **peak at lowest
  n_stim=4**, mostly monotone decrease 4→24, slight rise 24→48. Range
  ratio 2.199× > 1.50 → STRONGLY. **n_stim is a stronger η² lever than
  N** (n_stim range 2.20× vs N range 1.26× from §127). §125's n_stim=12
  was mid-range mediocre — arc would have measured stronger PARTIAL at
  n_stim=4. Carrier-capacity dilution hypothesis consistent (Ψ-C1 ∈ [0,1]
  bounded). **First LEGO probe written against post-§129 canonical engine
  SSOT** `HEXAD/LEGO/lego_engine.py` (B-S131-4 AST verified).

---

## LEGO arc — summary verdict ladder

```
§115 DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY
  ↓
§117 RUN: Ψ-form NON-DEGENERATE (LOCAL STDP), layer-1 variance-only liveness closed
  ↓
§124 AUDIT: "non-degenerate" = ONLY variance-only liveness (layer 1 of 3)
  ↓
§125 LAYER-2 PROBE: η²=0.271 PARTIAL at N=256
  ↓
§126 LAYER-2 N-SCALE-UP: η²=0.322 (4×N, 1.189×) — ROBUST at one point
  ↓
§127 SCALING-LAW: 4 N points → APPROXIMATELY-N-INVARIANT (k=−0.02, R²=0.022)
                  §126 single-point CONFIRMED, power-law extrapolation REFUTED
  ↓
§128 LAYER-3 DESIGN-CLOSE: requires task addition; pure §117 LIF cannot measure
                            layer-3 (anti-padding §13-M / §30 / §97 / §109 /
                            §110 / §113 precedent)
  ↓
§129 ENGINE CONSOLIDATION: lego_sim.py → HEXAD/LEGO/lego_engine.py
                            PLAN/INDEX/README documentation cleanup
```

g3 carry across every cycle: probe ≠ fire ≠ emergence; necessary-not-
sufficient at every layer (B-EMERGE-7); WALL-A (§1.1 data-regime)
orthogonal; WALL-B (§96 substrate) confronted-in-sim-NOT-removed;
north-star + §15/§51/§72 milestones UNCHANGED; **GOAL 미도달**.

### §132 — LEGO LAYER-2 NON-MONOTONIC SHAPE FIT *(2026-05-20)*

- **tier**: analysis-tier · $0 instant (re-fit of §127 data, NO new measurement)
- **verdict**: `SHAPE-FIT-IDENTIFIED` — inverted-U Gaussian-in-log-N R²=0.9995
- **battery**: B-S132 6/6 🔵 sidecar
- **state**: `state/lego_layer2_shape_fit_s132_2026_05_20/`
- **finding**: Re-fit §127's 4 (N, η²) points with 4 candidate models — A
  log-linear (§127 baseline) R²=0.0225 · B quadratic-log R²=0.9995 · C
  saturating Hill R²=0.0082 · D inverted-U Gaussian-in-log-N R²=0.9995.
  **Peak models (B + D) agree, monotone models (A + C) reject** —
  load-bearing closed-form (B-S132-5). Peak N* ≈ 730–1000. §127's
  non-monotonic shape is an inverted-U peak structure, NOT noise. **1-DoF
  caveat**: 4 points + 3 free params; perfect R² structural, load-bearing
  signal is peak-vs-monotone *agreement* not R² magnitude. Refines §127
  verdict without overturning it.
