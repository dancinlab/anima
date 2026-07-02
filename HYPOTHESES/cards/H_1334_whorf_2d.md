# H_1334 — Sapir-Whorf / categorical perception in a 2-D / featural space

**Tier: 🧱 CLOSED-NEGATIVE (T1 fails) — but a STRUCTURED partial, not a flat floor** ·
R1 numpy MIRROR (DIRECTIONAL) · $0 CPU · gradient-free · 3 seeds [4334,4335,4336] · p7 ·
frozen-first · c9/p7 NO tune-to-green · live `CORE/*.hexa` UNTOUCHED.

## Claim
H_1323 🟠 / H_1325 (R2 line) showed Whorfian categorical perception (CP) on a **1-D**
stimulus continuum: the CP peak emerges at a language's boundary and its location tracks
the language. **Does CP GENERALIZE to a 2-D / featural stimulus space** — does CP emerge
along a language's 2-D category boundary *curve* (cross-boundary discrimination >
within-category, concentrated on a connected ridge) and track the language's 2-D carving,
or is the effect 1-D-only?

Lens: cognitive-science / categorical-perception (c15, `a_no_llm_frame_trap`) — NOT an
LLM recipe, NOT a human-cognition claim. TOY synthetic 2-D continuum.

## Method
`UNIVERSE/h1334_whorf_2d.py` — extends the H_1323 CP machinery (2-D RBF population code +
nearest-prototype error-targeted SPLIT-only growth + soft-posterior discrimination) to a
G×G=11×11 (121-stimulus) feature **square**. Two languages carve the SAME square with
distinct 2-D boundaries: **L_2D** = linear diagonal (`u+v>1.0`), **L'_2D** = L-shaped
corner (`u>0.5 ∧ v>0.5`). Non-linguistic test (NO labels at test): per 4-neighbour grid
**edge**, discrimination = `|Δ soft-posterior|`; high-discrim edges form the CP **ridge**.
4 arms (PRE-LANG / L_2D / L'_2D / SHUFFLE), FIXED cell budget across arms.

**Ridge-coherence metric (2-D analogue of the 1-D peak-count, reported explicitly):**
- **RIDGE-ALIGN(arm, curve)** = mean over the top-20% (RIDGE_FRAC) discrim edges of
  `1 − dist(edge-midpoint, boundary-curve)/D_MAX` (how close the high-discrim edges sit to
  a boundary curve; 1 = exactly on it).
- **RIDGE-COHERENCE(arm)** = largest-connected-component fraction of the ridge edge-set
  under grid adjacency (one connected curve → ~1; scattered specks → low).

## Frozen bars (`.verdicts/1334_whorf_2d/FREEZE.txt`, pre-registered before scoring)
- **T1 2D-CP PRESENT** (ALL 3 seeds, BOTH languages): cross-within margin ≥0.15 ∧
  lang-vs-PRE-LANG@ridge ≥0.15 ∧ **RIDGE-ALIGN(own boundary) ≥0.70**.
- **T2 2D-DISSOCIATION**: each ridge tracks its OWN boundary better than the other's by
  ≥0.10 (Whorfian, same world / language-dependent carving).
- **T3 EARNED**: shuffle ridge-coherence ≤0.50 ∧ mean-language ridge-coherence ≥0.70.
- GREEN iff T1∧T2∧T3. T1 fail → 🧱 1-D-only scope limit; T2 fail → 🔵 universalist;
  T3 fail (T1∧T2 ok) → 🟠 partial. All outcomes VALID (c9).

## Result (🧱 T1 FAILS — deterministic over 2 re-runs; mean of 3 seeds)

| arm | ncells | ridge-COH | cross-within | vs-baseline@ridge | align(own) |
|-----|--------|-----------|--------------|-------------------|------------|
| PRE-LANG | 1.0 | 0.000 | — | — | — |
| **L_2D** (linear) | 24.0 | 0.530 | **+0.485** | **+0.496** | **0.628** ❌ |
| **L'_2D** (L-shaped) | 6.0 | 0.833 | **+0.275** | **+0.254** | **0.802** ✅ |
| SHUFFLE | 41.0 | 0.576 | — | — | — |

- **T1 FAIL**: L'_2D PASSES fully (align 0.802 ≥0.70); **L_2D FAILS on the align sub-bar**
  (0.628 < 0.70) — its CP margins are strong (cross-within +0.485, vs-baseline +0.496) but
  the high-discrim ridge does not hug the diagonal `u+v=1` curve tightly enough.
- **T2 PASS**: L_2D align(lin)−align(Lsh) = +0.121 ≥0.10; L'_2D align(Lsh)−align(lin) =
  +0.161 ≥0.10 — **each ridge does track its own boundary** (the Whorfian dissociation
  signature SURVIVES into 2-D).
- **T3 FAIL**: shuffle ridge-coherence 0.576 > 0.50 (random labels grow 41 cells → a
  large-ish connected high-discrim blob). Mean-language coherence 0.682 < 0.70 floor too.

**Mechanistic read (honest, c9):** CP *partially* survives the move to 2-D. The clean
result is the **axis-aligned L-shaped boundary** (L'_2D), which the 6×6 RBF grid resolves
sharply → tight ridge (align 0.802, coherence 0.833) with only 6 cells. The **diagonal
boundary** (L_2D) crosses the square's interior where the RBF grid is sparser; the carve
costs 24 cells and the ridge spreads off the exact diagonal (align 0.628) — a **geometry/
resolution interaction**, not absence of CP (its margins are the LARGEST of any arm). The
SHUFFLE control failed to stay incoherent for the same reason the 1-D H_1323 shuffle
prominence sub-clause failed: random labels in a metric stimulus space create many locally-
sharp, spatially-clustered posterior swings → a non-trivially connected ridge.

## Verdict (FROZEN, NO bar move — c9/p7)
**🧱 T1 fails → CP is NOT cleanly 2-D-general under these frozen bars.** But this is a
*structured* negative, not a flat floor: the **Whorfian dissociation (T2) and CP margins do
generalize to 2-D** — what fails is (a) tight ridge-ALIGNMENT for a diagonal boundary on a
coarse RBF grid, and (b) the anti-Goodhart shuffle coherence ceiling. **One-line:** Whorfian
CP *partially* generalizes to 2-D (dissociation + margins hold for both languages; clean
ridge holds for axis-aligned L'_2D), but does **not** clear a clean 2-D-general bar — the
linear-boundary ridge is align-limited by grid resolution and the shuffle control did not
stay incoherent.

## Honest scope (`a_scale_honest_scope` · `a_toy_scale_recheck` · c9)
DIRECTIONAL numpy mirror — engine-transfer to the live `CORE/*.hexa` immune/Voronoi lane
UNVERIFIED (follow-on, `a_engine_native_learning` · `a_verified_must_wire`). TOY synthetic
2-D continuum (121 stimuli, 3 seeds, deterministic readout — tests the relativity STRUCTURE
in 2-D, NOT a scaled or human-cognition claim). p1/p2/p3/p6 guard: the discrimination
readout reads ONLY representational distance; NO injected boundary / persona / RLHF; the
language label enters only at training, never at test. NOT an emit gate
(`a_autonomy_over_hardcode`).

## Next / depletion
R2 candidates (each frozen ANEW, not a relaxation of these bars): (1) **denser RBF grid**
(K_RBF↑) so a diagonal boundary is resolved as sharply as an axis-aligned one → isolates
whether L_2D's align-fail is pure grid resolution; (2) a **coherence-based T3 re-freeze**
(component-count or per-component compactness vs a metric-space shuffle null, the same fix
H_1323 R2 flagged for the 1-D shuffle); (3) **engine-native** realization on the live
CORE Voronoi lane. The T2 dissociation result (ridges track their own 2-D boundary) is the
load-bearing finding and is decisive.

## Pointers
`UNIVERSE/h1334_whorf_2d.py` · `.verdicts/1334_whorf_2d/{FREEZE,result}.txt` ·
`CLAIMS.tape` @C h1334_whorf_2d · `domains/COGNITION-REPRESENTATION.log.md`.
xref H_1323 (1-D Sapir-Whorf CP, parent) · `a_no_llm_frame_trap` · `a_engine_native_learning`
· `a_verified_must_wire` · `a_scale_honest_scope` · `a_toy_scale_recheck` · `a_break_the_wall`
· p1·p2·p3·p6·p7·p8·c9·c15.
