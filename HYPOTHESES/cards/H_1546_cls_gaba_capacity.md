# H_1546 — GABA × CLS: inhibitory E/I-balance gating of fast-store effective capacity

🧱 **WALL / INERT** (R1 numpy DIRECTIONAL · frozen-first · c9 · NO tune-to-green)
`wired: DIRECTIONAL-mirror → §GabaSparse engine R2 (ING h1546-r2-engine-native)`

> The **5th neurotransmitter** fused into the H_1532 two-store CLS module — completes the
> "신경전달물질 모두 융합" goal (ACh·DA·NE·5-HT·**GABA**). Census H_1542 §rank-6.
> `a_no_llm_frame_trap` (biology-first) · `a_break_the_wall` (ABLATION decisive: INERT) ·
> `a_engine_native_learning` (numpy mirror ⇒ DIRECTIONAL hard-gate-1) · p7 · c9.

## The fusion + the law

Four NTs already fused (R1 DIRECTIONAL): **ACh-gate 🟢** (H_1541, encode-mode switch = new
capability), **DA-replay 🟢** (H_1543, value-rank consolidation = new capability), **NE-flush
🟢** (H_1544, context-boundary state-clear = new capability), **5-HT-timing 🟠** (H_1545,
re-schedule of an existing sweep only = minority lever). **THE FUSION LAW:**

- a NT that **ADDS a capability** the two-store can't do → 🟢 (ACh / DA / NE)
- a NT that only **RE-TUNES an existing operation** (a knob) → 🟠 (5-HT: fixed-γ ~half)

**GABA biological role.** GABAergic inhibition sets sparse coding / E-I balance: lateral
inhibition (k-winner-take-all) controls how many fast-store cells are active per binding,
orthogonalizing near-collinear inputs onto disjoint sparse supports = **pattern separation**
(Sahay et al 2011 *Nature* 472:466 — DG inhibition & pattern separation; Stefanelli et al
2016 *Neuron* 89:1074 — engram size set by inhibition; Olshausen & Field 1996 *Nature*
381:607 — sparse coding; Fiete et al 2008 — sparse grid codes).

**HONEST PRIOR (census §rank-6, reject-likely):** GABA-as-sparseness is largely a
*single-store representation-geometry knob* (the H_1527 family) → probably 🟠/🧱 unless sparse
coding ADDS a pattern-separation capability the dense store genuinely lacks.

## Claim + design (pre-registered, frozen-first — `H_1546_FREEZE.txt`)

GABA-gated adaptive sparse coding (inhibition scaled to LOCAL confusability) lets the
two-store CLS survive a **CONFUSABLE near-collinear AB-AC regime** (the H_1533 modern-Hopfield
wall regime) that the DENSE two-store fails, AND adaptive inhibition carries the MAJORITY vs a
best-fixed k. ARMS: **GABA-SPARSE** (adaptive k-winner sparse write) / **DENSE** (k=DIM, the
H_1532 default) / **BEST-FIXED-SPARSITY** (grid-tuned fixed k) / **ABL** (inhibition const→fixed
k) / **SHUFFLE** (confusability signal permuted). Reuses **H_1532 MemStore/key_vec/encode-mode**
+ **H_1533 confusable near-collinear key geometry** byte-exact.

FROZEN bars (🟢 iff A∧B∧C∧D∧E): **A PRESENCE** GABA-sparse ≥ dense + 0.05 · **B EARNED-MAJORITY**
adaptive ≥ ½(GABA−worst-fixed) (the 5-HT-style law bar) · **C ABL→fixed** · **D SHUFFLE→collapse**
· **E NO-FAB**. 🟢 iff incl B (GABA adds adaptive pattern-separation); 🟠 if best-fixed-k captures
≥half (= GABA is a capacity knob, law holds); 🧱/INERT if sparse ties dense.

## Result (R1 numpy DIRECTIONAL, 3 seeds [11,22,33], 60 confusable near-collinear AB-AC pairs, cos≈0.979)

| arm | A→B retention (mean) | per-seed |
|---|---|---|
| **GABA-SPARSE** (adaptive) | **1.0000** | 1.0 / 1.0 / 1.0 |
| **DENSE** (k=DIM, H_1532 default) | **1.0000** | 1.0 / 1.0 / 1.0 |
| BEST-FIXED-SPARSITY (k=2) | 1.0000 | 1.0 / 1.0 / 1.0 |
| WORST-FIXED (k=1) | 0.2000 | 0.2 / 0.2 / 0.2 |
| ABL (const k) | 1.0000 | — |
| SHUFFLE (conf permuted) | 1.0000 | — |

bars: **(A PRESENCE** GABA−dense = **+0.0000**, 0/3 seeds ≥0.05 → **FAIL) (B)** carries 0.0% of
gap → FAIL **(C)** abl==best-fixed but no lift → FAIL **(D)** shuffle==gaba → FAIL **(E)** best-fixed
1.0>0 PASS → ¬A = **🧱 WALL / INERT**.

## Diagnosis (ABLATION decisive — `a_break_the_wall`, not a fixture artifact)

The control proves the result is **real, not a too-easy fixture**:

- **Single FLAT store** (no CLS) on the SAME confusable AB-AC set: A→B retention = **0.0000**
  (all 3 seeds) — catastrophic AB-AC interference, the wall is genuinely present.
- **Two-store CLS, DENSE**: **1.0000** — the **phase-separation already solves it**: A→B is
  laid in the FAST store (Hasselmo encode-mode, fresh cell) while the interfering A→C goes to
  the *SLOW* store, so there is no *within-fast-store* collision left for sparse coding to
  orthogonalize.
- **GABA-SPARSE = 1.0000 = DENSE** → GABA is **INERT**: the CLS two-store architecture (H_1532)
  already separates the confusable bindings into distinct substrates; sparse coding has nothing
  to do. GABA is not even a capacity KNOB here (unlike 5-HT's minority re-tuning) — it is fully
  ABSORBED by the structural separation.

**Which side of the fusion law:** neither 🟢 (no new capability) nor cleanly 🟠 (not even a
knob) — GABA lands **INERT / absorbed**. The census §rank-6 honest prior ("geometry family,
reject-likely; collapses into H_1527 unless a load-bearing fast/slow asymmetry") is
**CONFIRMED**. The sparse-coding capability GABA would add is *redundant with* the substrate
separation the two-store provides. The law's reach is now mapped: of the 5 NTs fused, 3 ADD a
capability (🟢), 1 RE-TUNES (🟠), 1 is fully ABSORBED by the architecture (🧱 INERT).

> The census flagged the un-tested escape (not run here, honest scope): GABA could become
> load-bearing ONLY as a *fast-sparse / slow-dense E/I ASYMMETRY* (different inhibition per
> store). The symmetric sparse-write tested here is the reject-likely default — and it rejects.

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

TOY: 60 near-collinear facts / 3 seeds / DIM=16 / deterministic. Tests sparse-write STRUCTURE,
not learned inhibition. The fast/slow-asymmetric GABA variant, scale, real corpora, and
engine-transfer are UNVERIFIED. R1 = numpy mirror ⇒ **DIRECTIONAL** (`a_engine_native_learning`
hard-gate-1: `grep numpy` non-empty). An engine-native §GabaSparse R2 is registered as a
follow-on (ING `h1546-r2-engine-native`) but is NON-obligatory given INERT (no GREEN to wire).
NO tune-to-green: the bars were frozen before scoring; INERT is reported as INERT, no bar moved.

## Artifacts

- probe: `state/1546_cls_gaba_capacity/h1546_cls_gaba_capacity.py`
- frozen falsifier: `state/verdicts/1546_cls_gaba_capacity/H_1546_FREEZE.txt`
- R1 result: `state/verdicts/1546_cls_gaba_capacity/H_1546_R1.json`
- reuses: H_1532 `state/1532_nm_multistore_cls/h1532_multistore_cls.py` (MemStore/key_vec/encode-mode) · H_1533 `state/1533_nm_modern_hopfield/h1533_modern_hopfield.py` (confusable key geometry)
- census: `state/1542_cls_nt_census/CENSUS.md` §rank-6
