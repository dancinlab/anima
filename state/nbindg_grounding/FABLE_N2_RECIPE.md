Design complete. I read `gen_nbindg_n2.py`, `gen_nbind.py`, and `STAGE1_dilution_verdict.json` on origin/main. Headline first, then the frozen recipe.

# FROZEN RECIPE — NBIND-G N2 exposure-matched training

## 0. The headline hazard: the CURRENT default reproduces STAGE-1 almost exactly

`NSMC_FILLER_MULT = 8` is a **line-count** knob, but exposure is a **byte** phenomenon. Grid geometry (from `gen_nbind.py`): 20 predicates × 4 train cells × REP 12 = **960 grid lines ≈ 48 KB** (~50 B/line). MULT=8 → 7,680 filler reviews ≈ **768 KB** (natural reviews ≈ 100 B, ~2× a grid line). So the real grid byte-fraction is

  f_grid = 48 / (48+768) ≈ **0.059** — not the 1/9 ≈ 0.11 the line ratio suggests.

At the H_9272 budget of 20k steps, effective grid exposure = 0.059 × 20k ≈ **1.2k steps ≪ E\* = 12k**. That is *worse* than STAGE-1's worst clean rung (f=0.3 → 6k) and would produce a guaranteed chance-level INVALID dressed as a grounding negative. Exposure-matching the default instead (T = 12k/0.059 ≈ 204k steps) is R3-class spend. **Both directions are wrong; the fix is: shrink + bias the filler, and denominate the knob in bytes.**

## 1. Filler density — FROZEN: byte-ratio knob, biased fill

Replace `NSMC_FILLER_MULT = 8` (lines) with **`FILLER_BYTE_RATIO = 3.0`** (filler bytes = 3× grid bytes → **f_grid = 0.25** by construction, ≈144 KB ≈ ~1,400 reviews).

**Fill order (biased — yes, keep the `filler_grounding`-first bias, and go further):**
1. Per-atom round-robin over P_nat-bearing reviews, **cap 60 reviews/atom**, dedup, until byte target or caps hit.
2. Top up remaining bytes with general (non-P_nat) reviews.
3. **Frozen per-atom corpus floor: ≥ 30 occurrences of each viable atom in the final train text** (count in the built corpus, not the 450k pool). Atoms under the floor are dropped from the viable set *pre-fire*; if survivors × 6 < 120 eval items → INVALID pre-fire (existing gate, re-checked post-build).

**Why biased is correct here, not a confound:** (a) all three corpora share the identical `nat_filler`, so any selection bias subtracts out of both Δs — bias is validity-neutral by construction; (b) grounding signal per byte is what buys down T: representative filler wastes bytes on atom-free reviews, which lowers f_grid and inflates T linearly (the STAGE-1 lesson run in reverse); (c) the grounding channel is unlabeled co-occurrence *inside* P_nat-bearing reviews — general reviews contribute ~nothing to it.

**Grounding-sufficiency rationale (the N):** epochs are invariant under exposure-matching — epochs ≈ E\* × (bytes/step) / grid_bytes ≈ 15–19 regardless of filler volume (T scales with corpus size; STAGE-1's own "12k steps ≈ 15 epochs" on the ~48 KB base corpus pins the constant). So a P_nat atom with ≥30–50 corpus occurrences gets ≈ 550–950 raw exposures — the same order as a P_grid predicate's 48 stamped lines × ~15 epochs ≈ 720, compensating for the weaker (unlabeled, purity 0.85) per-exposure signal with parity in raw count. ~1,400 biased reviews / 30 atoms ≈ 45–50 occ/atom nominal, floor 30 enforced.

## 2. Steps per arm — FROZEN: T = ⌈margin × E\*/f_grid⌉ = 60,000

Formula: **T = ⌈1.25 × E\*/f_grid⌉** with E\* = 12,000 (STAGE-1 measured knee), f_grid = actual grid-byte fraction of the *built* main corpus (target 0.25).

  T = 1.25 × 12,000 / 0.25 = **60,000 steps**, giving effective grid exposure T×f = 15k ≥ 1.25 E\*. The 1.25 margin covers (i) the sharp knee (8k = 0.475 → 12k = 1.0 leaves no measured slack below 12k) and (ii) possible mild interference slowdown from mixed-corpus training that pure-grid E\* didn't see.

**All 4 arms: identical T = 60k, identical corpus size — confirm, with one correction.** As currently coded, `base_only = corpus([])` is ~48 KB smaller than main, so at fixed T it gets more epochs on the filler. That bias *favors* base_only (conservative for the claim), but it's free to remove: **pad base_only with extra general reviews (never more P_nat-bearing ones) to byte-match main within ±2%**, so epochs-per-P_nat-occurrence are equal across arms. shuffle_grid already byte-matches main (same grid line count).

`--audit` must emit `f_grid_bytes` and `T_required` into `N2_PREFIRE_AUDIT.json`; the fire script reads T from there, never hardcodes it.

## 3. Arms — confirm the 4-run set

| run | corpus | seed | isolates |
|---|---|---|---|
| main-s7 | grid + filler | 7 | the claim: operator × natural grounding |
| main-s11 | grid + filler | 11 | seed robustness (V5) |
| base_only | filler (+pad) | 7 | crux: what nature alone installs (generic negation handling, free sentiment mapping) — predicted weak |
| shuffle_grid | coin-grid + filler | 7 | format-without-operator: grid taught "`=> 긍정/부정` answer format", not XOR |

Single seed on controls is adequate: the Δ bar (0.20) dwarfs observed control seed noise (XBIND control 0.515), and both controls sit under the same eval.

## 4. Frozen validity gates (pre-verdict, any fail → INVALID, never MODEL-🧱)

- **(a) Grid-reproduction gate:** each main arm's **seen D-acc on P_grid cells ≥ 0.85** (H_9272 reference 0.92). Below bar = grid under-exposed = STAGE-1-class INVALID. Evaluate with the existing H_9272 seen manifest — costs nothing extra.
- **(a′) Control-liveness twin:** shuffle_grid seen acc on its *coin* labels ≥ 0.85. If the shuffle arm can't even memorize its cells, its control value is VOID (dead control makes Δ vs shuffle meaningless).
- **(b) Exposure arithmetic gate (pre-fire, $0):** assert T × f_grid_bytes ≥ 1.25 × 12,000 from the built corpus's actual bytes before any pool dispatch — this is the mechanical guard against a silent re-widening of the filler.
- **(c) V-F leak (already coded):** no P_nat stem in any authored line, no eval seed verbatim in train — keep, plus the new per-atom corpus-occurrence floor from §1.
- **(d) Seed gate (V5):** the two main seeds must land the same side of every bar; a straddle → 🟡 DIRECTIONAL, no bar adjustment, no third-seed fishing.

## 5. Frozen verdict grid (bars decided now)

Eval: held-out P_nat × 6 D-acc (n = survivors×6 ≥ 120), `anima-py evaluate --xbind`. **Δ-inflation guard (H_9272 out-of-band lesson): every Δ is computed against max(control_acc, 0.50)** — a control that lands below chance never inflates Δ.

- **NAT-CRACK 🟢 (grounded):** BOTH main seeds: Δ(main − max(base_only, .50)) ≥ 0.20 AND Δ(main − max(shuffle, .50)) ≥ 0.20; gates (a)(a′)(b)(c) pass; base_only in predicted-weak band [0.40, 0.65]. If base_only > 0.65 (nature installs more than predicted), the Δ bars still apply but tier caps at 🟢-dir with an explicit "strong natural baseline" note — not INVALID.
- **FORMAT-🧱:** Δ vs base_only ≥ 0.20 but Δ vs shuffle_grid < 0.20 → the lift is answer-format teaching, not the operator. (N1 already argues against this; N2 must still be able to return it.)
- **MODEL-🧱:** gates all pass (grid installed at ≥0.85 seen — this is what makes it a *result* and not an exposure artifact) but main Δ < 0.20 vs both controls. **Frozen sub-split, report-mandatory:** decompose main held-out by flip class — flip0 items' gold = pol(p) directly, so **flip0 acc = grounding liveness, flip1 acc = operator application**. flip0 low → GROUNDING-🧱 (polarity never installed from natural usage — a data/frame result, echoes NATEM DATA-🧱); flip0 high + flip1 low → true operator-transfer MODEL-🧱. These are different follow-ons; don't let them collapse into one tier.
- **INVALID:** any §4 gate fail. Ckpt still PULLED before teardown (a_fire_recover_complete) — an INVALID run's checkpoint is reusable for continued-training exposure top-up.

## 6. Cost / wall — pool-first, 1-line estimate

4 × 60k steps @ 303M = each run is 3.0× an H_9272 20k run on the same trainer; on summer+aiden (2 × RTX5070 sm_120, 2 sequential runs per host, one heavy job per host — summer wedge caveat) ≈ **2 × (3× H_9272 wall) per host ≈ overnight $0 if a 20k run is ≲3h**. Frozen decision rule instead of a guess: log steps/s at step 500; if projected single-run wall > 10h (host total > 20h), rent 2 pods and go 4-way parallel (~9h wall, ~$1–2, a_wall_first — autonomous with the 1-line estimate at dispatch).

## Param diff summary for the parent (freeze into `gen_nbindg_n2.py`)

1. `NSMC_FILLER_MULT=8` → **`FILLER_BYTE_RATIO=3.0`** (bytes, not lines; target f_grid=0.25).
2. Biased fill: per-atom round-robin, cap 60/atom, then general top-up; **per-atom corpus-occurrence floor 30**, drop-then-recheck n_eval ≥ 120.
3. base_only padded with general reviews to byte-match main ±2%.
4. Audit emits `f_grid_bytes`, `T_required = ceil(1.25*12000/f_grid_bytes)`; fire script consumes it. **T = 60,000, all 4 arms.**
5. Gates: main seen ≥ 0.85 AND shuffle seen(coin) ≥ 0.85 pre-verdict; Δs vs max(control, 0.50); bars Δ ≥ 0.20 both controls, both seeds.

The single highest-value line: **f_grid must be measured in bytes and T derived from it (60k @ f=0.25) — the shipped default (MULT=8 lines @ 20k steps) is f≈0.059/exposure≈1.2k, i.e. a pre-built STAGE-1 INVALID.**

(Housekeeping note for the owner: claude.ai Gmail/Calendar/Drive MCP connectors need re-auth via claude.ai connector settings; unavailable this session — unrelated to this design task.)
