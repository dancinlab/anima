# H_1552 — GABA × CLS: adaptive sparseness under NON-STATIONARY load

🧱 **WALL / STATIC-ARCHITECTURE** (R1 numpy DIRECTIONAL · frozen-first · c9 · NO tune-to-green)
`wired: DIRECTIONAL-mirror → §GabaSparse engine R2 (ING h1552-r2-engine-native)`

> The **3rd decisive GABA lens** — `a_break_the_wall` MULTI-LENS class-(d). The one regime where
> adaptive sparseness *could* have honestly beaten fixed (the fusion-law **shifting-optimum**
> condition), tested and **falsified**. `a_no_llm_frame_trap` (biology-first) ·
> `a_engine_native_learning` (numpy mirror ⇒ DIRECTIONAL hard-gate-1) · p7 · c9.

## Why this is the legitimate LAST GABA lens (not fishing)

GABA-as-adaptive walled TWICE on **STATIONARY** regimes — H_1546 🧱 (pattern-SEPARATION,
absorbed by the CLS fast/slow architecture) and H_1551 🧱 (capacity-MULTIPLICATION under
STATIONARY overload, ADAPTIVE-INERT — a single best-fixed k=4 captures the whole 14.6× capacity
gain). The **fusion law** proven across the 6 fused NTs (ACh/DA/NE/orexin/5-HT 🟢/🟠 vs the GABA
walls): an adaptive NT lever beats a grid-tuned FIXED setting **only where the optimal operating
point SHIFTS over time**. orexin (H_1550 🟢) and 5-HT (H_1549 🟢) earned their honest green
*because the optimum shifted*; H_1551's stationary overload had ONE optimal k everywhere → adaptive
correctly inert.

The untested regime — the **only** one where adaptive sparseness could earn its keep — is
**NON-STATIONARY load**: the binding-arrival RATE alternates between LIGHT phases (few writes →
low cross-talk → dense/large-k best for fidelity) and HEAVY phases (many writes → high cross-talk
→ sparse/small-k needed to avoid collision). Premise: under non-stationary load no single fixed-k
is optimal (light-optimal large k overflows in heavy; heavy-optimal small k wastes fidelity in
light), so GABA-gated adaptive-k tracking the *current local* load should beat the best fixed-k.
The **same shifting-optimum principle** that gave orexin/5-HT their green, applied to GABA —
a principled distinct lens, NOT a bar move (Litwin-Kumar 2017: optimal sparseness depends on load).

## Claim + design (pre-registered — `H_1552_FREEZE.txt`)

Stream = 8 alternating segments (4 LIGHT rate=6 + 4 HEAVY rate=24 = 120 facts, matching H_1551's
load but **non-stationarily distributed**) into ONE Hebbian SuperStore (H_1551 substrate, VERBATIM).
ARMS: **GABA-ADAPTIVE-K** (k=K_SPARSE=8 in heavy phases, k=K_LIGHT=DIM=64 in light phases —
the shifting-optimum hypothesis) / **BEST-FIXED-K** (grid-tuned single k over the whole stream,
disjoint tune seed) / **DENSE** / **ABL** (k const = best-fixed) / **SHUFFLE** (load-phase signal
permuted). FROZEN bars: **A PRESENCE** gaba − **best-fixed** ≥ +0.10 (stricter than H_1551's
vs-dense — adaptive must beat the best FIXED k, since non-stationarity is what's supposed to break
fixed-k) · **B EARNED-MAJORITY** · **C ABL→best-fixed** · **D SHUFFLE→collapse** · **E NO-FAB**.
🟢 iff A∧B∧C∧D∧E; 🟠 if A∧E∧¬B; 🧱 if ¬A.

## Result (R1 numpy DIRECTIONAL, 3 seeds [11,22,33], SuperStore, DIM=64, 120 facts non-stationary, diverse keys cos≈0.76)

| arm | binding retention (mean) |
|---|---|
| **BEST-FIXED-K (k=4)** | **0.3639** |
| GABA-ADAPTIVE-K (k_light=64 / k_sparse=8) | 0.1333 |
| ABL (const k = best-fixed) | **0.3639** |
| SHUFFLE (load-phase permuted) | 0.1167 |
| DENSE (k=64) | 0.0250 |
| WORST-FIXED (k=24) | 0.0250 |

fixed-k grid: **k=2→0.400 · k=4→0.408 · k=8→0.133** · k=12→0.067 · k=16→0.033 · k≥24→0.025.

per-seed gaba − best-fixed: seed11 −0.250 · seed22 −0.217 · seed33 −0.225 (0/3 wins).

bars: **(A** gaba−best-fixed = −0.231 < +0.10 → **FAIL) (B** adaptive carries −213% of gap →
**FAIL) (C** gaba−abl = −0.231 → **FAIL) (D** gaba−shuffle = +0.017 < 0.05 → **FAIL) (E**
best-fixed 0.364 > dense 0.025 → **PASS)** → ¬A = **🧱 WALL / STATIC-ARCHITECTURE**.

## Diagnosis — the shifting-optimum premise is FALSE in a SHARED superposition matrix (ABLATION decisive)

The non-stationary regime did **NOT** make adaptive the lever, and the reason is mechanistically
clean and load-bearing:

- **There is no phase-LOCAL optimum, because all phases share ONE global matrix.** The hypothesis
  assumed light-phase facts could be written DENSE (k=DIM) for fidelity without harm. But in a
  single shared superposition store the dense light-phase codes' outer-product cross-talk **pollutes
  the SAME matrix** that holds the heavy-phase bindings — irreversibly (cross-talk cannot be undone,
  exactly the H_1551 mechanism). So K_LIGHT=DIM (the shifting-optimum arm) collapses to 0.133, far
  *below* the globally-sparse best-fixed k=4 (0.364). The optimum is **global**, not phase-local.
- **A confirmatory full (k_light × k_sparse) sweep** (8×4 grid, not part of the frozen verdict)
  finds the best *adaptive* pair is (k_light=4, k_sparse=2)=0.428 — but that is **not phase-tracking**,
  it is "sparse-everywhere" (sparse in BOTH phases); the moment k_light goes large (the genuine
  shifting-optimum hypothesis) the arm loses. So even the *generous* reading gives no faculty: there
  is no honest non-stationary lever, only a re-discovery that **global sparsity is optimal regardless
  of local arrival rate**.
- **The ABLATION is decisive:** freezing the load-gating to the const best-fixed k RECOVERS the full
  0.364 → the load-gating is exactly what breaks it (identical to H_1551). SHUFFLE barely moves
  (gaba 0.133 vs shuffle 0.117) precisely because the gate adds no value to permute away.

**Which side of the fusion law:** GABA lands **🧱 STATIC-ARCHITECTURE** for the 3rd time. Unlike
orexin/5-HT (where the optimum genuinely shifts over time → adaptive wins), the optimal sparseness
in a shared associative substrate does **NOT** shift with local load — it is a **global static
architectural constant** (Litwin-Kumar 2017 optimal-sparseness, here *per-substrate* not
*per-phase*). This is the **3rd decisive lens** (after H_1546 separation, H_1551 stationary-capacity)
and the one that was *specifically designed to give adaptive its best chance* (the shifting-optimum
condition that worked for every other NT) — its failure **confirms a class-(d) no-free-lunch ceiling**
for GABA-as-NT: **GABA is a static architectural parameter, not an adaptive faculty.** Of the NTs
fused: ACh/DA/NE/orexin/5-HT add capability or re-tune (🟢/🟠 — shifting optimum); GABA is absorbed/
static across separation, stationary-capacity, AND non-stationary load (🧱×3).

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

TOY: 120 facts non-stationarily distributed / 3 seeds / DIM=64 / single Hebbian superposition store
/ deterministic / binary phase (light↔heavy). Tests adaptive-sparse write under alternating load
STRUCTURE, not a learned controller. The shifting-optimum premise is honestly falsified *for a
shared-matrix substrate*; a substrate with **phase-LOCAL stores** (separate matrix per phase) could
restore a phase-local optimum — but that is a NEW architecture (multi-store), not a GABA-NT lever,
and would be the CLS multi-store family (H_1532), not this hypothesis. Scale, real corpora, and
engine-transfer are UNVERIFIED. R1 = numpy mirror ⇒ **DIRECTIONAL** (`a_engine_native_learning`
hard-gate-1: `grep numpy` non-empty). An engine-native §GabaSparse R2 is registered as a follow-on
(ING `h1552-r2-engine-native`) but is NON-obligatory given the 🧱 verdict (no GREEN to wire). NO
tune-to-green: bars were frozen before scoring; the adaptive arm's failure is reported as failure,
no bar moved (the presence bar measures the ADAPTIVE arm vs the best-FIXED-k; the generous full
k-sweep is reported above as a NON-gating diagnostic, NOT folded into the verdict).

## Artifacts

- probe: `state/1552_gaba_nonstat/h1552_gaba_nonstat.py`
- frozen falsifier: `state/verdicts/1552_gaba_nonstat/H_1552_FREEZE.txt`
- R1 result: `state/verdicts/1552_gaba_nonstat/H_1552_R1.json`
- reuses: H_1551 `state/1551_gaba_capmult/h1551_gaba_capmult.py` (SuperStore / sparse_code /
  key_vec / FNV-1a byte-exact) · H_1546 `state/1546_cls_gaba_capacity/h1546_cls_gaba_capacity.py`
  (the 1st GABA lens) — the 3rd GABA lens completing the class-(d) ceiling.
