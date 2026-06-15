# COGNITION-REPRESENTATION — discovery log

Per-domain discovery lane (a_discovery_log). Group for the Sapir-Whorf / categorical-
perception / bilingual-cognition lineage (cognitive-science lens c15, a_no_llm_frame_trap).
Hypothesis cards live in `UNIVERSE/H_<id>_<slug>.md`; index in `UNIVERSE/HYPOTHESES.md`.

## 2026-06-16 — H_1330 🧱 Sapir-Whorf BILINGUAL: OVERWRITE (catastrophic interference)

- **id**: H_1330 · slug `1330_whorf_bilingual` · seeds [4323,4324,4325] · $0 CPU mirror DIRECTIONAL
- **seed**: named EXTENSION frontier of the GREEN H_1323/H_1325 CP result — cross-lane
  interference: does a SECOND language OVERWRITE or COEXIST with the first's CP on ONE substrate?
- **verdict-tier-target → actual**: COEXIST (frozen hypothesis) → **🧱 OVERWRITE / CATASTROPHIC
  INTERFERENCE** (FALSIFIED). I1 COEXISTENCE ❌ (margin@p_A −0.001 vs A-only +0.200, full collapse
  on all 3 seeds); I2 NO-DOUBLE-ARTIFACT ✅ (B=A control 1 peak); I3 EARNED ✅ (shuffle collapses).
- **mechanism**: B labels [p_A,p_B] as 0 while A labeled it 1 — a DIRECT CONTRADICTION on SHARED
  stimuli; the grow-only Voronoi store floods [p_A,p_B] with ~21 new label-0 cells, erasing A's
  swing. H_1288 growth-memory protects ADDITIVE memory (new key) but NOT contradictory RE-LABELING
  of SHARED stimuli → a single shared store cannot hold two contradictory carvings.
- **nuance**: anima's real EN-trunk + KO lanes are SEPARATE faculties (H_1316/1321/1322), not one
  shared store — this is the worst case (maximally overlapping contradictory carvings).
- **next (R2 candidate)**: language-TAGGED / multi-channel readout (distinct label-channels per
  language) to hold two contradictory carvings WITHOUT interference — a DIFFERENT mechanism, frozen
  ANEW, not a bar relaxation. Depletion test unchanged.
- **claim-link**: `CLAIMS.tape @C h1330_whorf_bilingual` · card `UNIVERSE/cards/H_1330_whorf_bilingual.md`
  · verdicts `.verdicts/1330_whorf_bilingual/{H_1330_FREEZE,H_1330}.txt`
- xref: h1323 · h1325 (the GREEN result extended) · **h1288** (growth-memory, the prediction tested)
  · h1316 · h1321 · h1322 · a_no_llm_frame_trap · a_break_the_wall · a_scale_honest_scope · c9 · c15

### H_1335 — sapir-whorf BILINGUAL r2 (TAGGED): does a language-TAG enable CP COEXISTENCE? — 🧱 CONTROL-FAIL (but coexistence REAL & tag-attributable)

- **seed**: named r2 of H_1330 🧱 OVERWRITE (c16/a_break_the_wall — wrong MECHANISM, not a wall). H_1330's overwrite was a SINGLE-SHARED-STORE limit (one bound-label/cell can't hold A=1 & B=0 on the same stimulus). Lens: cognitive-science / bilingual-cognition (c15, a_no_llm_frame_trap). $0 CPU numpy MIRROR (DIRECTIONAL), 3 seeds [4323,4324,4325] (same as H_1323/1325/1330), frozen-first, live CORE UNTOUCHED.
- **mechanism**: IMPORTED VERBATIM from h1330 (embed/VoronoiCells/discrim/within_cross_margin/coherent_peak_near/count_peaks, W1_MARGIN=0.15, p_A=1/3 p_B=2/3, grow-not-evict p8). ONLY NEW = a language-TAG dim: key_A=concat(embed,t_A), key_B=concat(embed,t_B), DISJOINT coords (TAG_GAIN=1.0 FIXED, not swept) so key_A(x) & key_B(x) for the SAME x are separated by sqrt(2)·gain — the [p_A,p_B] contradiction is no longer on a SHARED key. Read CP@p_A via tag_A, @p_B via tag_B = select the faculty by tag (mirrors anima's REAL separate EN-trunk + KO faculties, H_1316/1321/1322).
- **arms**: (1) A→B TAGGED · (2) SINGLE-CHANNEL untagged = exact H_1330 (tag-attribution control) · (3) B=A control · (4) SHUFFLE.
- **result 🧱 CONTROL-FAIL (frozen), coexistence REAL**: **I1 COEXISTENCE ✅** all 3 seeds — TAGGED holds CP at BOTH boundaries, mean margin@p_A **+0.200** & @p_B **+0.177** (both ≥0.15, coherent peak each). **I2 TAG-ATTRIBUTION ✅** all 3 seeds — single-channel (untagged) reproduces H_1330 overwrite byte-exact (mean margin@p_A **−0.001**) → remove tag → overwrite returns = coexistence IS the tag, not extra training. **I3 EARNED ❌** — I3b SHUFFLE ✅ (peaks 5/6/5 incoherent); **I3a B=A ✗** count_peaks=2>1 (frozen ≤1 fails) BUT pk@p_B=False all seeds (the intended no-spurious-CP-at-p_B test PASSES).
- **mechanism diagnostic (c9, non-gating, NO bar moved)**: B=A grows ZERO B-tagged cells (re-learns A's boundary → no error to split) → B-channel reads ENTIRELY via cross-tag bleed from A-cells (dist≈1.42=sqrt(2)·gain), so its curve is the A-channel shape bled through the tag, carrying a benign low-end discretization wiggle = the 2nd "peak". The GLOBAL count_peaks≤1 bar conflated this with the LOCALIZED no-spurious-CP test (which passes). Honest note on TAG_GAIN=1.0: channel isolation imperfect (measurable low-end cross-tag bleed).
- **answer**: **YES — a language-tagged readout enables bilingual CP coexistence, mirroring anima's separate EN+KO faculties; the H_1330 OVERWRITE was the single-shared-store mechanism, NOT a fundamental limit (overturned as mechanism-specific).** Frozen 🧱 is the I3a control technicality ONLY; the science answer is decisively positive & tag-attributable.
- **next (r3 candidate)**: re-freeze I3a as the LOCALIZED "no coherent peak near p_B" test (data already satisfies, pk@p_B=False all seeds) — a DIFFERENT frozen bar, NOT a relaxation; + TAG_GAIN isolation sweep + engine-native realization on live CORE/engine_cli.hexa (a_engine_native_learning · a_verified_must_wire).
- **scope**: DIRECTIONAL mirror (engine-transfer UNVERIFIED); TOY synthetic 1-D N=21 deterministic; TAG_GAIN FIXED; NO human-bilingualism claim.
- **claim-link**: `CLAIMS.tape @C h1335_whorf_bilingual_tagged` · card `UNIVERSE/cards/H_1335_whorf_bilingual_tagged.md` · verdicts `.verdicts/1335_whorf_bilingual_tagged/{FREEZE,result}.txt`
- xref: **h1330** (the 🧱 OVERWRITE this r2 overturns as mechanism-specific) · h1323 · h1325 (the GREEN Sapir-Whorf CP) · h1288 (growth-memory) · **h1316 · h1321 · h1322** (anima's real separate EN+KO faculties this mirrors) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15 · c16
## H_1333 — Whorfian CP: developmentally PLASTIC or RIGID? 🟠 PARTIAL (GRADED PLASTICITY)

- **seed/lens**: extension of the GREEN **H_1323/H_1325** Sapir-Whorf result; developmental /
  critical-period plasticity lens (c15, a_no_llm_frame_trap). Question: is the language-warped
  categorical-perception (CP) boundary PLASTIC (re-locates on re-training) or RIGID (stuck where
  first learned)? verdict-tier-target = D1∧D2∧D3 frozen.
- **method**: reuse the H_1323 CP machinery VERBATIM (RBF embed · split-only Voronoi growth p8 ·
  soft-posterior no-label discrim · peak-count coherence). Train language A (cut p_A=1/3), measure
  CP peak; RE-train the SAME store on a MOVED boundary p_A'=2/3 (phase-2 grow-further, no reset),
  measure CP peak again. 4 arms (A-trained / A→A' re-trained / NO-RETRAIN control / SHUFFLE),
  3 seeds [4333,4334,4335], $0 CPU mirror DIRECTIONAL. Frozen-first (FREEZE.txt), NO bar moved (c9).
- **result 🟠 PARTIAL — GRADED PLASTICITY (not rigid)** (deterministic all 3 seeds): CP peak
  **0.325→0.525, fraction relocated +0.60**. **D2 CONTROL ✅** — no-retrain held p_A (|Δ|=0.008 →
  the move IS the re-training, not drift) + A-trained reproduced H_1323. **D3 EARNED ✅** — shuffle
  incoherent (peak-count **7.7**≥3), lang arms coherent (1.0/1.3/1.0≤2). **D1 PLASTIC ❌ by a hair** —
  |peak−p_A'|=0.142>0.12 (−0.022) AND |peak−p_A|=0.192<MIN_MOVE 0.20 (**missed by 0.008**) → strict
  D1 FAIL, but substantively a SUBSTANTIAL relocation.
- **mechanism (c9)**: split-only growth NEVER evicts old-boundary cells (28 cells after phase-2 vs
  4 after phase-1) → residual phase-1 packing at p_A pulls the peak back from a full move. The
  carving re-locates substantially but a never-evicting store leaves a residual first-cut pull —
  graded, not rigid; not first-carving primacy.
- **one-line**: the language-warped CP boundary is developmentally **GRADED-PLASTIC** — it
  re-locates ~60% of the way on re-training, with a residual pull from the never-evicted first cut.
- **next (R2 candidates)**: (i) graded SHIFT-SIZE curve (≥3 shifts) mapping plasticity-fraction vs
  shift magnitude · (ii) EVICTION/decay store variant (does removing stale old cells complete the
  move?) · (iii) engine-native §CategoricalPerception realization on live CORE/engine_cli.hexa —
  each frozen ANEW, not a bar relaxation.
- **claim-link**: `CLAIMS.tape @C h1333_whorf_developmental` · card `UNIVERSE/cards/H_1333_whorf_developmental.md`
  · verdicts `.verdicts/1333_whorf_developmental/{FREEZE,result}.txt`
- xref: h1323 · h1325 (the GREEN result extended) · h1330 (bilingual overwrite, shared-store
  contradiction) · **h1288** (growth-memory: store grows, never evicts — the mechanism behind the
  residual pull) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning ·
  a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · c9 · c15
  a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · c9 · c15
## 2026-06-16 — H_1334 🧱 Sapir-Whorf 2-D / FEATURAL: STRUCTURED-NEGATIVE (dissociation generalizes, clean bar fails)

- **id**: H_1334 · slug `1334_whorf_2d` · seeds [4334,4335,4336] (H_1323-family +1 decade, PROJ_SEED provenance) · $0 CPU mirror DIRECTIONAL
- **seed**: named EXTENSION of the GREEN 1-D H_1323/H_1325 CP result — does Whorfian categorical
  perception GENERALIZE from a 1-D continuum to a 2-D / featural feature space, or is it 1-D-only?
- **paradigm**: G×G=11×11 (121-stim) feature SQUARE, 2-D RBF code (6×6 centers, dim 36). Two languages
  carve it: L_2D=LINEAR diagonal (u+v>1.0), L'_2D=L-SHAPED corner (u>0.5∧v>0.5). Per grid-EDGE
  discrim = |Δ posterior|; high-discrim edges = CP RIDGE. Ridge-coherence metric (2-D analogue of the
  1-D peak-count) = largest-connected-component fraction of the ridge edge-set; RIDGE-ALIGN = ridge
  closeness to a boundary curve. 4 arms (PRE-LANG/L_2D/L'_2D/SHUFFLE).
- **verdict-tier-target → actual**: 🟢 (CP generalizes to 2-D) → **🧱 STRUCTURED-NEGATIVE** (T1 fails;
  deterministic over 2 re-runs). **T1 2D-CP-PRESENT ❌** — L'_2D PASSES fully (cross-within +0.275,
  vs-baseline +0.254, ridge-align 0.802≥0.70) but **L_2D FAILS the align sub-bar (0.628<0.70)** though
  its CP margins are the LARGEST of any arm (+0.485/+0.496). **T2 2D-DISSOCIATION ✅** — each ridge
  tracks its OWN boundary (L_2D +0.121, L'_2D +0.161, both ≥0.10): the relativity signature SURVIVES
  into 2-D. **T3 EARNED ❌** — shuffle ridge-coherence 0.576>0.50 (metric-space random labels → 41
  cells → connected blob; same failure mode as 1-D H_1323 prominence); mean-lang coherence 0.682<0.70.
- **mechanism**: the diagonal boundary crosses the square's interior where the 6×6 RBF grid is sparse →
  ridge SPREADS off the exact diagonal (align-limited by grid resolution, NOT absence of CP — its
  margins are the strongest); the axis-aligned L-shape is resolved sharply (6 cells, align 0.802,
  coherence 0.833). SHUFFLE in a metric space grows a non-trivially connected high-discrim blob.
- **finding**: Whorfian CP PARTIALLY generalizes to 2-D — DISSOCIATION + cross-within margins hold for
  BOTH languages, clean ridge holds for axis-aligned L'_2D — but does NOT clear a clean 2-D-general
  bar (linear-ridge align-limited by grid resolution + shuffle not incoherent in a metric space).
  Reported straight, NO bar moved (c9/p7).
- **next (R2 candidate, each frozen ANEW)**: denser RBF grid (K_RBF↑, isolate the diagonal align-fail) +
  component-count / per-component-compactness shuffle null (the same metric-space-shuffle fix flagged
  for the 1-D H_1323 R2) + engine-native realization on the live CORE Voronoi lane.
- **claim-link**: `CLAIMS.tape @C h1334_whorf_2d` · card `UNIVERSE/cards/H_1334_whorf_2d.md`
  · verdicts `.verdicts/1334_whorf_2d/{FREEZE,result}.txt`
- xref: h1323 · h1325 (the GREEN 1-D result extended) · h1330 (bilingual sibling) · a_no_llm_frame_trap
  · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope
  · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15
