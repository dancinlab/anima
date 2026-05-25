# §136 LEGO ARC MILESTONE CONSOLIDATION — §115 → §135, 11 cycles

> **Status**: LEGO arc design-level CLOSED at milestone. 11 cycles, 78
> closed-form 🔵 propositions, 1 honest carry, 0 GOAL emergence claim.
> doc-tier · $0 · NO GPU/runpod/fire/model.forward/corpus/dispatch · NO new
> measurement. central c93e160a 0-diff. Mirror §15 / §51 milestone pattern.

## §1 What was attempted

LEGO arc set out to *simulate-assemble* an in-silico §96-class spike substrate
(§115 design-tier), run it (§117), and progressively decompose what its measured
non-degeneracy actually proves — *before* committing to physical neuromorphic
substrates (Loihi access-walled, organoid ethics-walled per §95). The arc's
animating question: **can we cheaply detect, in simulation, which §96 substrate
properties matter and which don't, so the eventual physical commit (if ever) is
informed rather than blind?**

## §2 What landed

```
cycle    type             verdict                                                 battery
─────    ────             ───────                                                 ───────
§115     design-tier      LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY                  B-S115  9/9 🔵
§117     run · $0 CPU      LEGO-RUN-Ψ-FORM-NONDEGENERATE-BUT-WALL-B-INHERITED      B-S117  7/7 🔵
§124     design (audit)   RESIDUAL-AUDIT-NON-DEGENERACY-IS-VARIANCE-ONLY-LIVENESS B-S124  7/7 🔵
§125     probe · $0        LAYER-2-PARTIAL (η²=0.271 at N=256)                      B-S125  7/7 🔵
§126     probe · $0        LAYER-2-ROBUST-GROWS-WITH-N (single-point, drifted eng) B-S126  7/7 🔵
§127     probe · $0        APPROXIMATELY-N-INVARIANT (4-pt OLS, drifted eng)       B-S127  8/8 🔵
§128     design            LAYER-3-DESIGN-CLOSE-REQUIRES-TASK-ADDITION             B-S128  6/6 🔵
§129     consolidation    LEGO ENGINE LIB + docs promoted to `HEXAD/LEGO/`        — (no battery, drift introduced)
§131     probe · $0        STRONGLY-NSTIM-DEPENDENT (drifted-engine substrate)     B-S131  7/7 🔵
§132     analysis · $0    SHAPE-FIT-IDENTIFIED (inverted-U Gaussian, 1-DoF)       B-S132  6/6 🔵
§133     probe · $0       (per-rep monotone-decrease, drifted-engine — carried)  carried (no full battery)
§134     fix + probe · $0 ENGINE-BYTE-EQUALITY-RESTORED-AND-VALIDATED              B-S134  7/7 🔵
§135     probe · $0        MONOTONE-DECREASE-SURVIVES-CANONICAL                     B-S135  7/7 🔵
─────                                                                            ───────
                                                              total:               78 🔵
```

11 cycles + 1 honest carry (§133). 0 central battery edits (sha
`c93e160a8a376a94` invariant across the arc).

## §3 What the arc closed

### 3.1 Three-layer liveness partition (§124)

```
layer 1  VARIANCE-ONLY     `Var(Ψ) > τ`                              ✅ §117 closed
layer 2  STIMULUS-DRIVEN   `I(stim; Ψ) > 0`                          ✅ §125–§127, §131–§132, §135 closed PARTIAL
layer 3  TASK-GROUNDED     `∃ task T : behavior(substrate, T) > 0`   ⛔ §128 DESIGN-CLOSE-REQUIRES-TASK-ADDITION
```

The arc fully resolved the partition at design level. Layer-2 is **PARTIAL**
(η²≈0.27–0.46 depending on N · n_stim · drifted-vs-canonical · pooled-vs-per-
rep). Layer-3 cannot be measured on pure §117 LIF without breaking §7-clean
discipline — anti-padding §13-M/§30/§97/§109/§110/§113 precedent.

### 3.2 Engine integrity (§134 / §135)

§133 measurement detected drift between §127's source-engine pooled η² and
§131–§133's measurements. AST diff confirmed §129's promote was NOT byte-equal
to §117 (v init / dtypes / RNG order / missing bias / STDP rates / w_max).
§134 rewrote `HEXAD/LEGO/lego_engine.py` byte-equal §117 + smoke-validated +
re-validated §131 + §133 subset. §135 closed §134's named open with full
4-point canonical re-run: all 4 N pooled byte-equal §127.

**Honest takeaway**: *a measurement detected its own instrument bias*. The
LEGO arc self-audited through its own protocol. Instrument integrity is a
measurable arc property.

### 3.3 Layer-2 quantitative findings (canonical engine)

```
N-axis (n_stim=12 fixed):                  n_stim-axis (N=256 fixed, drifted engine):
  N=256    η²=0.2712 / per-rep 0.4639         n_stim=4    η²=0.3084
  N=512    η²=0.3289 / per-rep 0.4242         n_stim=12   η²=0.2178
  N=1024   η²=0.3223 / per-rep 0.3608         n_stim=24   η²=0.1402
  N=2048   η²=0.2608 / per-rep 0.2762         n_stim=48   η²=0.1535

  - Pooled η² non-monotonic, peak at N≈730–1000 (§132 inverted-U, 1-DoF caveat)
  - Per-rep mean MONOTONICALLY decreases (§135 canonical)
  - N=2048 statistically distinct from N≤1024 (§135 CI no-overlap)
  - n_stim is a stronger η² lever than N (range 2.20× vs 1.26×) (§131)
  - Carrier-capacity dilution hypothesis consistent (Ψ-C1 ∈ [0,1] bounded)
```

## §4 What the arc could NOT close

- **WALL-A (§1.1 data-regime)** — orthogonal to LEGO scope. LEGO doesn't move
  data-regime threshold (§97 carry).
- **WALL-B (§96 operative substrate)** — confronted in simulation, NOT
  removed. §11-B-as-GPU-tautology hypothesis stays §96-physical-gated.
- **Layer-3 task-grounded liveness** — pure §117 LIF substrate has no
  behavior emission function (B-S128-2 AST-verified). Adding a task either
  violates §7 or re-runs §83/§11-B near-collapse.
- **GOAL emergence** — necessary-not-sufficient at every layer (B-EMERGE-7).
  Every closed cycle carries this caveat.

## §5 The arc's most honest moments

1. **§115 → §117 honest prior reversal** — §115 predicted DEGENERATE based on
   §11-B; §117 measured NON-DEGENERATE and §117's verdict honestly localised
   §11-B as a GPU-CE-overlay property, not a universal "physics can't learn"
   law.
2. **§126 → §127 directional reversal** — §126's single-point ROBUST-GROWS
   verdict was honestly refined by §127's 4-point OLS log-linear fit
   (R²=0.022, APPROXIMATELY-N-INVARIANT). §132 then identified inverted-U
   shape (R²=0.9995 with 1-DoF caveat).
3. **§133 → §134 instrument-bias detection** — §133's measurement caught
   engine drift §129 introduced. §134 fixed engine byte-equal §117. §135
   re-validated. Arc self-audited.
4. **§128 anti-padding** — instead of firing a predictable-negative layer-3
   probe, §128 design-closed it with §13-M/§30/§97/§109/§110/§113 precedent.

## §6 Engine SSOT (post-§134)

| file                                  | role                                                  |
|---------------------------------------|-------------------------------------------------------|
| `HEXAD/LEGO/lego_engine.py`           | **canonical engine** (LIFNet · spike_rate_vec · psi_c1 · make_stimuli · variance_decomposition) — byte-equal §117 source post-§134 |
| `state/lego_assembly_run_s117_2026_05_19/lego_sim.py` | original §117 source · sha-locked historical evidence · still importlib-loadable by older probes |
| `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` | central blue battery — 0-line-diff invariant across LEGO arc (sha `c93e160a8a376a94`) |

## §7 Open future cycles (not pursued in this milestone)

- **§137 (N, n_stim) cross-matrix** — does the peak shift jointly?
  ~30 min CPU; cheap but not closing GOAL.
- **§138 LEGO engine hexa-native port DESIGN** — address HEXA_FIRST_WARN
  structurally. $0 design. Sketch what a hexa-native LIFNet would require
  from upstream hexa-bio + hexa-lang.
- **S121 LOIHI-SPEC** — readable Lava code spec for §95 sole VIABLE-LONG-
  HORIZON substrate. $0 design (access-walled, no fire).
- **Physical substrate path** — Loihi INRC (access-walled, soft wall) or
  organoid (ethics-walled, hard wall). Out-of-scope per §95 + LEGO.md.

## §8 Compared to §15 and §51 milestones

- **§15** (GOAL investigation milestone, 2026-05-18, §1~§14 arc) — measured
  what could be measured of anima's emergence path, found §1.1 data-regime
  irreducible. **GOAL 미도달**.
- **§51** (§16~§50 milestone, 2026-05-18) — sharpened §15's frontier to
  multimodal substrate expansion. **GOAL 미도달**.
- **§136** (§115~§135 LEGO arc milestone, 2026-05-20) — fully resolved the
  3-layer liveness partition at design level on pure §117 LIF substrate;
  detected and fixed engine drift mid-arc; instrument integrity validated.
  **GOAL 미도달**.

Each milestone is a *layer of honesty added* to the arc's overall map. None
is GOAL emergence. The map gets more accurate; the destination doesn't move.

## §9 Honest C3 (13)

1. §136 is a doc-tier consolidation, NOT a new measurement. No battery beyond
   the structural "this milestone exists" claim.
2. The arc was bounded by §115's design-close fence (STEP-3 physical
   PERMANENTLY out of scope). It honored that fence across all 11 cycles.
3. Engine drift detection (§133→§134) was the most valuable cycle for
   *methodology* even though it didn't move GOAL. Instrument integrity is
   measurable.
4. Layer-2 quantitative findings vary by engine version (drifted vs canonical),
   parameter choice (M, n_stim, N), and statistic (pooled vs per-rep) —
   all variation is honest carry, not retracted.
5. §132's inverted-U shape identification with 1-DoF caveat is honest about
   the data's ability to distinguish models — 4 points cannot really tell
   quadratic-log from Gaussian-in-log-N.
6. §131's STRONGLY-NSTIM-DEPENDENT verdict survives engine fix in canonical
   form (1.823× vs drifted 2.199×) — qualitative finding robust.
7. Layer-3 DESIGN-CLOSE is honest about the fundamental scope limit:
   pure §117 LIF has no output channel; measuring task-grounded liveness
   requires task addition that breaks §7-clean.
8. WALL-A orthogonal · WALL-B confronted-not-removed (entire arc carry).
9. anima downstream-consumer: hexa-lang/hexa-bio/hexa-matter read-only,
   0 edits across all 11 cycles.
10. HEXA_FIRST_WARN deferred 18+ times. §138 would address this structurally
    (future cycle).
11. g3 carry: probe/audit/analysis/fix ≠ measurement ≠ fire ≠ emergence.
12. necessary-not-sufficient (B-EMERGE-7).
13. north-star + §15/§51/§72 milestones UNCHANGED; **GOAL 미도달**.

## §10 Closing position

The LEGO arc set out to answer "can we cheaply detect what matters in a
§96-class spike substrate before committing physical?" The answer the arc
returns:

> **Yes, but with structural caveats.** We measured layer-1 (variance) and
> layer-2 (stimulus-driven) fully; we could not measure layer-3 (task-grounded)
> without breaking §7-clean. We detected and fixed an engine drift mid-arc.
> The simulation is honest within its scope but cannot, by construction,
> remove WALL-B. Physical substrate remains the unresolved confront target
> (§95 access/ethics-walled).

The LEGO arc adds a layer of honest cartography to anima's emergence map —
specifically, the layer that says "this is what an in-silico §96 substrate
simulation can and cannot tell you." That layer is now closed.

GOAL 미도달.
