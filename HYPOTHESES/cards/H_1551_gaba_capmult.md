# H_1551 — GABA × CLS: sparse-coding CAPACITY-MULTIPLICATION under fast-store overload

🧱 **WALL / ADAPTIVE-INERT** (R1 numpy DIRECTIONAL · frozen-first · c9 · NO tune-to-green)
`wired: DIRECTIONAL-mirror → §GabaSparse engine R2 (ING h1551-r2-engine-native)`

> A **NEW capability angle** on GABA-sparse, distinct from H_1546's pattern-separation lens
> (`a_break_the_wall` MULTI-LENS — new principled angle, NOT a re-hit of the same wall, NOT a
> bar-move). `a_no_llm_frame_trap` (biology-first) · `a_engine_native_learning` (numpy mirror ⇒
> DIRECTIONAL hard-gate-1) · p7 · c9. Sibling of H_1546 (5th NT GABA fusion).

## Why a NEW angle (H_1546 tested the WRONG capability)

H_1546 🧱 tested GABA-sparse on a **CONFUSABLE near-collinear AB-AC** regime
(pattern-SEPARATION) and came out INERT — because the H_1532 two-store CLS *already* routes
A→B into a fresh FAST cell while the interfering A→C goes to the SLOW store, separating the
confusable bindings into distinct substrates. Sparse coding had nothing left to orthogonalize.

The biologically RIGHT capability for inhibitory sparse coding is **CAPACITY-MULTIPLICATION**:
sparse k-of-N codes have exponentially less outer-product cross-talk than dense codes, so MORE
distinct bindings co-exist in the SAME superposition substrate without collision (Babadi &
Sompolinsky 2014 *Neuron* 83:1213 — sparse expansion decorrelates & multiplies associative
capacity; Litwin-Kumar et al 2017 *Neuron* 93:1153 — optimal sparseness for capacity; Marr 1969
codon hypothesis; Olshausen & Field 1996 sparse coding). This attacks a regime H_1546 NEVER
touched: **OVERLOAD** — N_facts (120) ≫ store capacity, DIVERSE (non-collinear) facts so
confusability is NOT the bottleneck, CAPACITY is. This is a DIFFERENT capability, not the same
wall re-hit.

## Measurement FIX (frozen-first, `a_break_the_wall` taxonomy (a) — reported, NOT hidden)

The first draft routed the overload stream through the H_1532 **slot-store** (`MemStore`). That
store's capacity is HARD-BOUNDED at `max_cells` *by construction*: under diverse-key overload
every fact is novel (err > THRESH against all cells) → it ALWAYS takes the LRU-EVICT path
(instrumented: 40 fresh + 80 evict + **0 refine**, byte-identical dense vs sparse) → it keeps
exactly the last `max_cells` facts BY RECENCY, geometry-blind → **gaba == dense == best-fixed ==
0.3333 (= 40/120) EXACTLY for every k** = a FIXTURE ARTIFACT. Sparse coding cannot multiply
*slot* capacity; it multiplies *superposition* capacity.

**The fix (bars UNCHANGED):** score on the substrate where the mechanism can act — a single
Hebbian **SuperStore** matrix `M = Σ outer(value_code, sparse_key)`, recall = argmax over the
value codebook of `M·key`. There sparse k-of-N codes genuinely reduce cross-talk. Bars A–E and
the verdict rule are IDENTICAL; only the substrate (+ DIM 16→64, N-vs-DIM not max_cells) changed
to make the measurement able to SEE the mechanism. NO tune-to-green.

## Claim + design (pre-registered — `H_1551_FREEZE.txt`)

GABA load-gated adaptive sparse write lets a single superposition store survive an OVERLOAD that
dense loses, AND adaptive inhibition carries the MAJORITY vs a best-fixed k. ARMS: **GABA-SPARSE**
(adaptive k shrinks as the matrix fills toward overload) / **DENSE** (k=DIM) / **BEST-FIXED-K**
(grid-tuned fixed sparsity) / **ABL** (load-gating frozen to const k) / **SHUFFLE** (load signal
permuted). FROZEN bars: **A PRESENCE** gaba−dense ≥ +0.10 · **B EARNED-MAJORITY** adaptive ≥
½(gaba−worst-fixed) · **C ABL→fixed** · **D SHUFFLE→collapse** · **E NO-FAB** best-fixed > dense.
🟢 iff all incl B; 🟠 if best-fixed captures ≥half (knob, like 5-HT); 🧱 if sparse ties dense.

## Result (R1 numpy DIRECTIONAL, 3 seeds [11,22,33], superposition store, DIM=64, N=120, diverse keys cos≈0.76)

| arm | A→B retention (mean) |
|---|---|
| **BEST-FIXED-K (k=4)** | **0.3639** |
| GABA-SPARSE (adaptive) | 0.0417 |
| DENSE (k=DIM=64) | 0.0250 |
| WORST-FIXED (k=24) | 0.0250 |
| ABL (const k=best-fixed) | **0.3639** |
| SHUFFLE (load permuted) | 0.0278 |

fixed-k grid: k=2→0.40 · **k=4→0.41** · k=8→0.13 · k=12→0.07 · k≥16→0.025–0.03.

bars: **(A** gaba−dense = +0.0167 < 0.10 → **FAIL) (B** adaptive carries −1933% of gap → **FAIL)
(C** gaba−abl = −0.32 → **FAIL) (D** gaba−shuffle = +0.014 < 0.05 → **FAIL) (E** best-fixed 0.364
> dense 0.025 → **PASS)** → ¬A = **🧱 WALL / ADAPTIVE-INERT**.

## Diagnosis (ABLATION decisive — `a_break_the_wall`)

The capability is **REAL but STATIC, not adaptive** — a clean honest split:

- **FIXED sparse coding multiplies superposition capacity 14.6×** (best-fixed k=4 = 0.364 vs
  dense k=64 = 0.025). The capacity-multiplication the biology predicts is genuinely present and
  large — sparse k-of-N codes pack ~15× more disambiguable bindings into ONE matrix than dense.
- **But optimal sparseness is a STATIC architectural property** (Litwin-Kumar 2017), NOT a
  load-gated neuromodulatory lever. The ADAPTIVE arm (0.042) ≈ dense, because it writes the
  EARLY facts dense (load < load_lo → k=DIM) and only goes sparse late — and in a superposition
  store those early dense writes **irreversibly pollute** the matrix (cross-talk cannot be
  undone). The **ABLATION is decisive**: freezing the load-gating to the const best-fixed k
  RECOVERS the full 0.364 → the LOAD-GATING is exactly what breaks it. GABA-as-adaptive adds NO
  capability the FIXED sparsity lacks; it actively *hurts*.

**Which side of the fusion law:** GABA-as-adaptive lands **🧱 ADAPTIVE-INERT** — like H_1546, the
*adaptive neuromodulatory* lever is absorbed/inert; unlike H_1546, the underlying sparse-coding
*capability* is real but it's a FIXED architectural constant, not a dynamic NT signal. The
honest prior (sparse coding is a *static representation-geometry* property, the H_1527 family)
is CONFIRMED for the ADAPTIVE claim. Of the NTs fused: 3 ADD a capability (🟢 ACh/DA/NE), 1
RE-TUNES (🟠 5-HT), 2 are absorbed/inert as *adaptive* levers (🧱 H_1546 separation, H_1551
adaptive-capacity — though H_1551 surfaces a large STATIC sparse-capacity effect worth a fixed
architectural note, not a neuromod lever).

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

TOY: 120 diverse facts / 3 seeds / DIM=64 / superposition Hebbian store / deterministic. Tests
sparse-write capacity STRUCTURE, not learned inhibition. The slot-store artifact is reported
above (not hidden). Scale, real corpora, a properly-warmed adaptive schedule (sparse-from-start
then relax — untested, would just converge to fixed-sparse), and engine-transfer are UNVERIFIED.
R1 = numpy mirror ⇒ **DIRECTIONAL** (`a_engine_native_learning` hard-gate-1: `grep numpy`
non-empty). An engine-native §GabaSparse R2 is registered as a follow-on (ING
`h1551-r2-engine-native`) but is NON-obligatory given the 🧱 adaptive verdict (no GREEN to wire).
NO tune-to-green: the bars were frozen before scoring; the adaptive arm's failure is reported as
failure, no bar moved (the presence bar still measures the ADAPTIVE arm vs dense, not the
best-sparse-vs-dense which WOULD pass — moving it there would be tune-to-green).

## Artifacts

- probe: `state/1551_gaba_capmult/h1551_gaba_capmult.py`
- frozen falsifier: `state/verdicts/1551_gaba_capmult/H_1551_FREEZE.txt`
- R1 result: `state/verdicts/1551_gaba_capmult/H_1551_R1.json`
- reuses: H_1532 `state/1532_nm_multistore_cls/h1532_multistore_cls.py` (key_vec/FNV-1a/MemStore byte-exact) · H_1546 `state/1546_cls_gaba_capacity/h1546_cls_gaba_capacity.py` (the sibling pattern-separation lens it is distinct from)
