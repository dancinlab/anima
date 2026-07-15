# H_9375 — V4 STEM-COLLISION-CLEAN: is the stem side of the operator's address BYTE-FUZZY or DISCRETE? (fresh-data · sequential-gated re-earn of H_9372)

**tier**: 🧊 **FROZEN PREREG** (this commit) — no number has been read. The verdict is written into the RESULT section below and the ARCHITECTURE `g1-census-objfloor` node ONLY after measurement, frozen-first.
**status**: PREREGISTERED (2026-07-15) — sequential-gated. The freeze is a committed artifact BEFORE the judged data (fresh s13 ckpt + fresh nonce ladder) exists.
**renumber**: origin-max at prereg = H_9372; V2 KEY-LADDER takes H_9373. This lever takes **H_9375** (origin-max+3, headroom to survive parallel races · G6 uniqueness confirmed). 
**lane**: `g1-interface-addressable-wall` · V4
**parent**: H_9372 (⛔ INVALID-ANCHOR PERMANENT — the burned V3 this re-earns) · H_9327 (BINDING 🧱) · H_9358 (V1 TWO-LANE 🟢) · H_9353 (V5 NO-IN-CONTEXT-CHANNEL 🧱 EARNED)
**instrument**: `anima-py corpus atoms --collision-split` (nonce ladder builder · engine-native, merged in V3) → `anima-py evaluate --xbind` (TERMINAL). Post-hoc statistics on the engine's row-dump only (no re-implemented forward pass · `a_experiment_engine_native`).
**cost**: ARM-R $0 (frozen base ckpt, zero training) · ARM-F = one 303M CPT (pool, no rent · summer)

---

## Why this H exists (settled — not re-derived here)

V3 STEM-COLLISION (H_9372) landed **⛔ INVALID-ANCHOR (PERMANENT)** over a **strong 🟢-BLEED-shaped signal**:
JT p=0.0001 both seeds · k2 S/A 0.840 (s7) / 0.791 (s11) · negJ surface-control flat (p=0.44 / 0.18) ·
pedestal ≈ 0 · s11 passed all 3 frozen gates. The **only** failure was s7's natural anchor over-reproducing
H_9327's held-out flip1 by **0.0052** (0.6552 vs the frozen G-ANCHOR ceiling 0.65). Fable ruled that
**re-anchoring on the SAME deterministic-eval data = tune-to-green**: on a deterministic eval the anchor value
is *burned* — any re-frozen gate's pass/fail is computable at freeze time. **H_9372 stays ⛔ PERMANENTLY. Its
s7 data is NEVER re-read and NEVER re-gated here** (convergence `BURNED_GATE_REANCHOR_TUNE_TO_GREEN`, landed
separately as PR #3661). The signal is strong enough to justify a **fresh-data follow-on with sequential gating
that makes anchor-shopping structurally impossible.**

## The question (unchanged from V3)

Is the STEM side of the operator's address **BYTE-FUZZY** (a stem sharing more bytes with a SEEN stem is pulled
monotonically toward its polarity → a cheap escape: spell a new stem into a SEEN byte-neighbourhood) or
**DISCRETE / REPRESENTATIONAL** (near-miss = total miss; the address is created only by learning)?

---

## FROZEN DESIGN — the sequential contract (this is the whole point; it is what makes it NOT tune-to-green)

The freeze (this commit) is landed BEFORE any measurement. Two arms; a 🟢 cement needs **BOTH**.

### Frozen instrument constants (one instrument, applied to both ckpts)
- **Fresh nonce ladder** = `anima-py corpus atoms --collision-split --atoms gt_atoms.json --nonce-fillers 3 --seed 9375 --win 64` — a **NEW filler RNG seed (9375 ≠ V3's 7)** → a fresh filler sample, so the nonce byte-content of V4 does not exist at V3's freeze either. `gt_atoms.json` md5 `7e9931291983e20c156201973d51a8d0` (the frozen instrument atoms).
- Manifest structure (VERBATIM from the merged builder `cli/corpus.py::build_collision_split`, byte budget ko=3B/char): for each 3-syllable SEEN donor `d` (polarity `p`) and `k∈{0,1,2,3}`, `nonce(d,k,f)=d[:k]+filler(d,f)[k:]` (always 9B, length-matched at every k). k0=0B unrelated control · k1=3B · k2=6B graded near-miss · k3=9B = the donor itself (positive control) · nat = the 29 natural held-out stems (H_9327 flip1 anchor). Surfaces: negL, negZ (operator-live) · negJ (no-operator surface control). Gold = the DONOR-implied negated word (`m>0` ⇒ leans donor-implied).
- **DV** `m = NLL(counterfactual) − NLL(gold)`. **Stratum stat** `S_k = ½[mean(m|donor pol=1)+mean(m|donor pol=0)]` on operator-live surfaces only. **Anchor** `A = S_3`; every bound is a fraction of A (scale-free). **Secondary** D-acc (greedy first word == donor-implied word).

### UNTOUCHED invariants from V3 — **not one character changed**
JT k∈{0,1,2} one-sided ↑ · 10,000 within-donor k-permutations · clustering unit = DONOR (not item) · negL/negZ primary · negJ surface-control · pedestal donor-polarity label-shuffle (true=0) · k1 ambiguous-prefix drop (5 donors whose 1-syllable prefix is shared, e.g. `유`→유쾌하+/유치하−) · donors 6 pos / 6 neg (builder REFUSES an unbalanced set) · 9B length-match across the whole ladder · G-POS (k3 D-acc ≥ 0.75 ∧ S_3>0) · G-CTRL0 (|S_0| ≤ 0.20·A). The verdict table covers **below-chance**: any arm with a JT-significant *decreasing* trend = ANTI-BLEED → 🔴 (never "판별 불가" — a failure is chance, below-chance is a discovery).

### ARM-R — s11 REPLICATE ($0, no training) — the re-usable seed
s11 passed the ORIGINAL frozen V3 gate 3/3, so it is re-usable WITHOUT re-gating (no shopping — s11's anchor is not re-judged). Procedure:
1. Build the fresh nonce ladder (seed 9375, above) → run `anima-py evaluate natem_c34_main_s11.clm --xbind <fresh_manifest> --n-decode <all>` (frozen ckpt `natem_c34_main_s11.clm`, md5 recorded in RESULT, zero training).
2. Score **JT p (k∈{0,1,2})** and **S_2** on operator-live surfaces.
3. **WRONG-DONOR CONTROL (frozen · closes the filler-length hole)**: re-score the SAME fresh nonce rows against a **permuted donor→polarity map** and require the trend to vanish. Definition, frozen: draw ONE balanced (still 6/6) random permutation `π` of the 12 donor polarity labels with `random.Random(9375)` (reject if identity); set `m'_i = m_i · (+1 if π(donor_i)==pol_i else −1)`; run the **identical** within-donor one-sided-increasing JT on `m'` over k∈{0,1,2}. **PASS = flat, p > .10.** Rationale: if the k-climb were a filler-length / byte-prior artifact independent of the *true* donor's polarity, it would survive π; a real byte-address effect (tied to the true donor) cancels under π.

### ARM-F — fresh seed s13 CPT (the cement path, needs training · pool $0) — the anti-peeking gate
**Corpus recipe discovery (documented, load-bearing):** the natem_c34 lineage is **seed-parameterized** — s7's corpus md5 `d466d0cff4a730fee72c521852c502d6` (160,086 B) ≠ s11's `a996436a00556468130467296e46c2bf` (178,234 B). The builder `random.Random(seed)` drives BOTH corpus generation AND training; s7/s11 were `build_c34(7)+train(--seed 7)` and `build_c34(11)+train(--seed 11)`. The **faithful third seed** is therefore:
- **s13 corpus** = `state/nbindg_grounding/gen_nbindg_c34.py` (sha256 `8d482e95c157eec6348ac948770e7df761f47513525906032a352d03a2478caf`) `--seed 13 --arm main` over frozen datasets `~/g1_natem/{nsmc_ratings_train.txt md5 45009b9a…, naver_shopping.txt md5 cd029e47…, steam.txt md5 33610570…}` + `n2_eval_manifest.json` md5 `ce9b1f7a4f8f4bb5afde18925abc63e7` (the 29 P_nat atoms, verbatim) + deps `gen_nbindg_n2.py` sha `9014dc41…` / `gen_nbind.py` sha `aa6b11de…`. Determinism is verified on the pool (build twice → identical md5) BEFORE training. **Fallback (pre-specified, so it cannot be a post-hoc choice):** if the build is non-deterministic, reuse s11's frozen corpus (md5 `a996436a…`) with `--seed 13` — a fixed-data, fresh-seed replicate; documented in RESULT. Either path leaves the s13 anchor non-existent at freeze.
- **s13 train** = `anima-py train --arch clm --canon --arm ctrl --objective ce_marginal --corpus c34_main_s13_train.txt --cell-label en-general --steps 60000 --batch-size 8 --bf16 --seed 13 --val-frac 0.02 --val-every 15000 --out natem_c34_main_s13.clm` (byte-identical recipe to s7/s11; ONLY the seed changes to 13). Pull the ckpt to `~/anima-weights/c34/` before any teardown (`a_fire_recover_complete`).

**Sequential anti-peeking order (MANDATORY):**
1. Measure the **nat anchor ONLY** on s13: extract the `nat|…` rows of the fresh manifest into an anchor-only manifest, run `anima-py evaluate natem_c34_main_s13.clm --xbind <anchor_only>`. Compute pooled nat D-acc + per-polarity-class D-acc on operator-live surfaces (negL, negZ).
2. **Judge G-ANCHOR′.** 
3. **Run the full nonce ladder on s13 ONLY IF G-ANCHOR′ PASSES.** If it fails: report *"ckpt out-of-regime · primary NOT run"* and stop ARM-F. This is the anti-peeking gate — the primary result is never even generated on an out-of-regime ckpt, so it cannot be peeked at and it cannot be shopped.

### G-ANCHOR′ (frozen NOW, from pre-unblinding H_9327 numbers + the binomial formula ONLY)
pooled nat D-acc ∈ **[0.278, 0.744]** — derived: H_9327 card per-seed held-out flip1 DV {0.4598, 0.5632} ± 1.96·√(p(1−p)/29) = [0.278, 0.744] (verified: 0.4598−1.96·0.09255=0.2784 · 0.5632+1.96·0.09210=0.7437) — **AND** a per-polarity-class floor: each class D-acc ≥ **0.15** (constant-predictor-collapse guard, `polarity-split-before-headline`).

### Honest-disclosure clause (verbatim, as required)
V3's 0.6552 **WOULD** have passed this band. The defense is **NOT the band width** but: (i) the band is derived only from pre-unblinding H_9327 card numbers + the binomial formula — no V3/V4 number entered it; (ii) the judged target (the fresh **s13** anchor) **does not exist at freeze time** — it is created only by the seed-13 CPT that runs after this commit lands; (iii) the sequential order — the anchor is judged, and the primary is generated, in that fixed order, so the primary result on an out-of-regime ckpt is never produced. s7/s11 are **NOT re-judged** by this gate (their eval data is burned; s11 is re-used only as a fresh-nonce REPLICATE, not re-gated).

### Verdict rule (frozen · pre-committed)
- 🟢 **BLEED / BYTE-FUZZY** cement ⟺ **ARM-F** (G-ANCHOR′ PASS ∧ JT p<.05 ∧ S_2 > 0.20·A) **AND** **ARM-R** (JT p<.05 ∧ S_2 > 0.20·A ∧ wrong-donor JT flat p>.10) — **BOTH**.
- ⛔ **INVALID (anchor fail)** — G-ANCHOR′ fails on s13 (fresh out-of-regime): a clean honest result, primary not run, no re-gate.
- 🔴 **ANTI-BLEED / DISCRETE** — any operator-live arm shows a JT-significant *decreasing* trend, or the equivalence bound holds (S_1,S_2 90% CI entirely within ±0.20·A) in both arms.
- ⏳ **UNDERPOWERED** — S_2 90% CI wider than the ±0.20·A band ⇒ no negative claim.
- s7 is **permanently isolated** from verdict arithmetic (exploratory reporting only).

### Scope (one line)
**Earns** — EN-discriminator-adjacent, 303M, natem_c34 lineage, regime-certified ckpt: the operator's stem-axis address is byte-fuzzy (monotone BLEED in shared prefix bytes, ~6B≈ceiling). **Does NOT earn** — the KO lane's own closure · the wall's mechanism (the two-lane runtime-bridge absence H_9358 is a SEPARATE axis — BLEED is address *topography*, not the binding *mechanism*) · natural-distribution relevance (natural stem collisions are structurally 0 = census DEGENERATE; the nonce ladder is synthetic) · capability (ρ-AXON reach).

---

## RESULT (filled ONLY after measurement — frozen-first, no bar moved)

_pending — ARM-R and ARM-F measured post-freeze; numbers verbatim from `anima-py evaluate` row-dumps + the frozen readout._
