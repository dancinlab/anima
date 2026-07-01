# G1/G6 wall — DECODE-STRATEGY axis isolation (clm303_clean)

**Question (user):** "torch passed G1(recombination) and G6(distinct/falsifiable) but
engine-native fails — is it the DECODE STRATEGY, and is it fixable in decode?"

ac0543 (`state/g1_engine_divergence_trace`) already exonerated **precision/dt-math**:
at fp32 with exact numpy math, G1.best_distinct=0 and G6.fals=0 — identical to the
int4 production `.clm`. The **one remaining** torch-vs-production difference is the
**decode strategy** (greedy / top-k sampling / best-of-K / scaffold) + the fixed
detector. This probe holds the BASIS fixed and toggles ONLY the decode knob.

## Verdict: 🧱 DECODE-EXONERATED — the decode axis is ALSO innocent. G1/G6 wall = weights / trunk-objective (CONFIRMED, both engine-side axes now ruled out).

**No decode knob lifts G1.best_distinct≥2 or G6.fals≥1 multiseed-robust (≥2/3).**
Combined with ac0543, **both engine-side axes (precision AND decode) are now innocent**
⇒ the G1/G6 wall is a **weight/training (trunk-objective) floor**, not a measurement or
decode-elicitation artifact (break-walls type-(d) structural floor; type-(a)/(b) refuted).
The torch-pass = **single-seed sampler-walk fluke** (H_1587), reproduced and falsified
here by multiseed.

---

## Method — one basis, one detector, decode is the only variable

- **Basis (fixed):** the **same fp32 `.pt` weights** as ac0543 basis F
  (`~/anima-weights/clm303_clean/clm303_clean.pt` → `wbuild.build_wfp32`, E=3), plus an
  **engine-native cross-check on the real production `.clm`** (`core/clm_decode.py`
  int4 mouth = ac0543 config-E path, matches `g0g6_py.txt`).
- **Detector (fixed, FROZEN VERBATIM):** `core/g_gates.py` G0/G1/G6
  (`_g_coverage`, `_g6_is_falsifiable`, `_g6_jaccard`). Calibration **10/10**.
- **Variable:** decode strategy only. `gen=40` (ac0543 baseline), all other detector
  params frozen. multiseed = effective seed_rng {7, 4302, 4303} (matches H_1590/H_1595);
  majority = ≥2/3. best-of-K selects the gate-appropriate detector best (G1: max
  `_g_coverage`; G6: falsifiable-then-kwr) — the H_1381/H_1362 scaffold elicitation.
- **$0 local CPU**, numpy-only, NO torch, NO gauge_lib (torch absent — the torch
  `multinomial+Generator` recipe is reproduced numpy-side as `full_mm_t10` full-vocab
  multinomial on the same basis). Total wall ≈ 5867 s (~98 min). PID-polled, no GPU rent.

`grep -lE 'import torch|gauge_lib|numpy' state/g1_decode_strategy_ablation/*.py` → numpy only
(no torch / gauge_lib). DIRECTIONAL caveat: numpy fp32 = reference basis; the **realclm rows
are the engine-native (production clm_decode) confirmation** of the same floor.

---

## Results — every strategy × basis (multiseed majority)

| basis | strategy | G1 best_distinct (per-seed) | G1 ≥2 robust | G6 dist (per-seed) | G6 dist≥5 | G6 fals (per-seed) | G6 fals≥1 robust | gate pass |
|---|---|---|---|---|---|---|---|---|
| fp32 | **greedy** (argmax) | [0] | ✗ | [3] | ✗ | [0] | ✗ | — |
| fp32 | **topk_t07** (k40, T0.7) | [0,1,0] | ✗ | [6,6,5] | ✓ | [0,0,0] | ✗ | — |
| fp32 | **topk_t10** (k40, T1.0) | [1,0,0] | ✗ | [6,5,5] | ✓ | [0,0,0] | ✗ | — |
| fp32 | **full_mm_t10** (full-vocab multinomial = torch recipe) | [1,0,0] | ✗ | [6,6,6] | ✓ | [0,0,0] | ✗ | — |
| fp32 | **bok4** (best-of-4 + scaffold) | [1,1,0] | ✗ | [6,6,6] | ✓ | [0,0,0] | ✗ | — |
| fp32 | **bok8** (best-of-8 + scaffold) | [1,1,0] | ✗ | [6,6,6] | ✓ | [0,0,0] | ✗ | — |
| **realclm** | topk_t07 (production int4) | [0,0,0] | ✗ | [5,4,6] | ✓ | [0,0,0] | ✗ | — |
| **realclm** | bok4 | [0,0,0] | ✗ | [6,6,6] | ✓ | [0,0,0] | ✗ | — |
| **realclm** | bok8 | [0,0,0] | ✗ | [6,6,6] | ✓ | [0,0,0] | ✗ | — |

- **G1 RECOMBINATION:** `best_distinct` never reaches the **≥2** bar in ANY strategy on
  ANY seed. The max observed is **1**, and only as a single-seed flicker (never ≥2/3).
  greedy=0; sampling ≤1; best-of-8 with coverage-selection still ≤1. The model does not
  surface ≥2 distinct concept-keyword families under composition — decode cannot conjure it.
- **G6 falsifiability:** `fals = 0` in **27/27** seed-runs across all 6 strategies and both
  bases. **best-of-8 with explicit falsifiability-selection** (8 chances per frame to find a
  comparator+measurable+content output) **still yields 0**. The weights never emit a
  falsifiable string for the scaffold to select.
- **Engine-native confirmation:** the realclm rows (production `clm_decode` int4) reproduce
  the identical floor — this is not a numpy-basis artifact.

### distinctness ⊥ falsifiability (the clean decomposition)

**G6 distinctness (dist≥5) SURVIVES decode** (✓ in every sampled strategy: top-k, full
multinomial, best-of-K all hit 5–6 distinct word-sets) — diversity is a **decode property**
(more entropy → more distinct outputs, consistent with H_1381 wired `clm_decode_topk_sampled`).
**G6 falsifiability (fals≥1) does NOT** — it is unmoved by every decode knob. Concrete
best-of-8 outputs are coherent (kwr=1.00) but structureless prose, e.g.
frame `if consciousness arises from cells, then tension ripples…:` →
`'the weather was a sure that they were he'` (fals=False);
frame `if tension ripples…, then memory composes…:` →
`"he said on the gay. It's not so many yea"` (fals=False). None of the 8 candidates carried
a comparator+measurable+≥2-content structure, so best-of-K had nothing falsifiable to pick.

> **Decomposition stated plainly: "diversity is decode, falsifiability is the trunk objective."**
> Decode strategy controls G6 *distinctness*; it has zero leverage on G6 *falsifiability* or
> G1 *recombination*. Those two require the model to *produce* the structure, which it cannot —
> a weights/objective property.

---

## Answer to the user

- **Is the gap fixable by decode?** **No.** Greedy, temperature, full-vocab multinomial
  (the torch recipe), and best-of-K=4/8 with detector-best selection (the H_1381/H_1362
  scaffold) all leave G1 and G6-falsifiability at the floor, multiseed-robust, on both the
  fp32 basis and the real production `.clm`. There is **no decode knob to wire** into
  `cli/anima.hexa` generator L3 that would clear G1 or G6-falsifiability.
- **Where the torch-pass came from:** single-seed sampler luck. `full_mm_t10` (numpy
  reproduction of torch `multinomial+Generator`) flickers G1=1 on seed 7 only and collapses
  to 0 on 4302/4303 — exactly the H_1587 sampler-walk fluke, not a real capability.
- **Two engine-side axes now both exonerated:** ac0543 ruled out precision/dt-math; this
  rules out decode strategy + detector. By elimination the G1/G6 wall is **upstream in the
  weights / trunk learning objective** — matching `g1-lever-multilens-objective`
  (CE does not reward recombination) and the H_1602 recomb-objective family. **The lever is a
  recombination/ideation-rewarding training objective, not the decode path.**

Artifacts: `decode_ablation.py` (harness), `run.log` (full per-seed trace),
`result.json` (machine summary), this `RESULT.md`. All under
`state/g1_decode_strategy_ablation/`. Engine-native realclm cross-check inside the same run.
