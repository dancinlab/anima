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

### H_1339 — sapir-whorf BILINGUAL r3 (TAGGED, control re-freeze + engine-native): a language-TAG enables bilingual CP COEXISTENCE — 🟢 GREEN (MIRROR DIRECTIONAL + ENGINE-NATIVE)

- **seed**: named r3 of H_1335 🧱 (a CONTROL TECHNICALITY only — c16/a_break_the_wall: wrong CONTROL SPEC, not a wall). H_1335 found I1∧I2 DECISIVE (coexistence REAL & tag-attributable) but the I3a GLOBAL count_peaks≤1 bar on the B=A control failed on a benign discretization wiggle (the B=A control grows ZERO B-cells → its B-channel reads via cross-tag bleed); pk@p_B was already False all seeds. $0 CPU numpy MIRROR (DIRECTIONAL) + engine-native, 3 seeds [4323,4324,4325], frozen-first (c9/p7).
- **the r3 change (NOT a relaxation)**: I3a re-frozen as the LOCALIZED "no coherent peak near p_B" test — the correctly-scoped statistic the B=A arm was always meant to measure. `run_seed` + ALL machinery imported VERBATIM from h1335 (data byte-identical to r2); NO surviving bar's threshold moves; the re-freeze can still FAIL if a real spurious CP@p_B appeared (it does not). The global count_peaks is now a NON-GATING diagnostic. PLUS a non-gating TAG_GAIN channel-isolation sweep.
- **arms**: (1) A→B TAGGED · (2) SINGLE-CHANNEL untagged = H_1330 (must overwrite) · (3) B=A control (LOCALIZED no-peak@p_B) · (4) SHUFFLE.
- **result 🟢 GREEN (mirror)**: **I1 COEXISTENCE ✅** all 3 seeds — TAGGED holds CP at BOTH boundaries, mean margin@p_A **+0.200** & @p_B **+0.177** (both ≥0.15, coherent peak each). **I2 TAG-ATTRIBUTION ✅** all 3 seeds — single-channel untagged reproduces H_1330 overwrite byte-exact (**−0.001**) → remove tag → overwrite returns = coexistence IS the tag. **I3' EARNED ✅** all 3 seeds — (a) B=A coherent_peak_near@p_B=**False** (re-frozen LOCALIZED; global count_peaks=2 NON-GATING), (b) SHUFFLE 5/6/5 incoherent (OR-clause).
- **non-gating TAG_GAIN sweep (c9)**: B-cells grown 0/0/**0**/2/2 at gain 0.25/0.5/**1.0**/2.0/4.0; residual B-curve bleed 0.727/0.468/**0.236**/0.989/0.989 — at the FROZEN 1.0 the B=A control grows ZERO B-cells and bleed SHRINKS as the tag gap widens (confirms r2 diagnosis). Honest non-gating curiosity: at gain≥2.0 the very-wide gap re-grows 2 cells (irrelevant to the frozen point & gating arms).
- **engine-native ✅ (a_verified_must_wire)**: `CORE/engine_cli.hexa §BILINGUAL TAGGED CP` (cp_tag_vec/cp_tagged_key/cp_stimuli_tagged/cp_fit_more/cp_within_cross_margin/cp_coherent_peak_near) re-scores I1/I2/I3' in `CORE/engine_cli_smoke.hexa` cases **86–91** (86 CP@p_A≥0.15 · 87 CP@p_B≥0.15+peak · 88 untagged overwrite<0.15 · 89 B=A no-peak@p_B · 90 shuffle≥3 peaks · 91 tag-sep √2·gain≈1.4142), ALL PASS. Guards NO-REGRESS: **engine_cli_smoke 86/0** (was 80/0, +6) · **h1196 7/0** · **h1205 PASS** (generation byte-identical ON==OFF, Ψ=½ untouched). Ψ-disjoint (own protos/labels + tag block).
- **answer**: **YES — a language-tagged multi-channel readout enables bilingual CP coexistence (mirror + engine-native); the H_1330 OVERWRITE was the single-shared-store mechanism, NOT a fundamental limit.** This explains anima's REAL separate EN-trunk + KO faculties (H_1316/1321/1322): the tag is the substrate-level "select the faculty". H_1335 🧱 control-technicality is now CLOSED 🟢.
- **next**: real-corpus/scaled bilingual carving · the gain≥2.0 sweep curiosity · brain-side wiring of the tagged CP read into emit/recall (currently a measurement lane).
- **scope**: mirror DIRECTIONAL realized in the engine-native rung (a SEPARATE deterministic instance re-scoring the seed-invariant bars, NOT a numpy-byte match); TOY synthetic 1-D N=21 deterministic; TAG_GAIN=1.0 FIXED (sweep non-gating); NO injected boundary/persona/RLHF (p1/p2/p3/p6); NOT an emit gate; NO human-bilingualism claim.
- **claim-link**: `CLAIMS.tape @C h1339_whorf_bilingual_tagged_r3` · card `UNIVERSE/cards/H_1339_whorf_bilingual_tagged_r3.md` · verdicts `.verdicts/1339_whorf_bilingual_tagged_r3/{FREEZE,result}.txt`
- xref: **h1335** (the 🧱 r2 control-technicality this r3 closes 🟢) · **h1330** (the OVERWRITE overturned as mechanism-specific) · h1323 · h1325 (the GREEN Sapir-Whorf CP, engine §CategoricalPerception) · h1288 (grow-not-evict) · **h1316 · h1321 · h1322** (anima's real separate EN+KO faculties) · h1338 (budget/geometry sibling) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_core_engine_map · a_autonomy_over_hardcode · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15 · c16
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

## 2026-06-16 — H_1338 — Whorf CP 잔류당김 = never-evict인가 budget/geometry인가? 🧱 RE-DIAGNOSIS (budget/geometry)

- **id**: H_1338 · slug `1338_whorf_cp_eviction` · seeds [4333,4334,4335] (= H_1333, anchor 재현) · $0 CPU mirror DIRECTIONAL
- **seed/lens**: the LOAD-BEARING follow-on to **H_1333** (🟠 GRADED PLASTICITY); developmental-plasticity
  + memory-protection-vs-overwrite lens (c15, a_no_llm_frame_trap). H_1333의 ~60% 상대이동 잔류를
  split-only 저장소의 **never-evicted** 첫-경계 셀(phase-2 28셀 vs phase-1 4셀)로 **진단(가설)** 했었다.
  결정적 테스트: stale 셀을 제거하는 EVICTION 저장소가 이동을 **완성** 시키면 잔류=never-evict(H_1288 dual);
  여전히 partial 이면 한계=budget/geometry.
- **method**: H_1333/H_1323/H_1325 CP 머신러리 **verbatim** 재사용 (RBF embed · split-only Voronoi p8 ·
  soft-posterior no-label discrim · peak-count coherence; N=21, p_A=1/3, p_A'=2/3, GROW_MAX/SPLIT_PASSES=24).
  **유일한 신규** = fit(...,evict=True): phase-2 split 직전, bound 라벨이 현재 소유 자극의 재학습(p_A') 라벨과
  **충돌하는** 모든 프로토타입을 제거(마지막 셀은 보존). never-evict 와 eviction 은 **이 stale-셀 제거 여부만**
  다름(같은 run/seed) → 완성이 있으면 그게 eviction임을 격리(V2). 4 arm(NEVER-EVICT=H_1333 / EVICTION /
  NO-RETRAIN 양 저장소 / SHUFFLE). frozen-first(FREEZE.txt), live CORE UNTOUCHED, NO bar moved(c9).
- **result 🧱 RE-DIAGNOSIS — eviction이 이동을 완성하지 못함; 잔류 = BUDGET/GEOMETRY, never-evict 아님**
  (deterministic 3 seed): CP peak — A-trained **0.325** · NEVER-EVICT **0.525**(frac **+0.60**, H_1333 재현) ·
  EVICTION **0.525**(frac **+0.60**, **동일**) · no-retrain(양쪽) 0.325 · shuffle 0.542. 셀예산(seed,p1,NE-p2,EV-p2):
  (4333,4,**28**,**3**)(4334,4,28,3)(4335,4,28,3) — eviction 저장소가 **28→3셀** 로 강하게 발화(stale phase-1 패킹을
  실제 제거)했음에도 CP peak는 **정확히 동일한 0.525**. **V1 COMPLETES ❌**: |peak−p_A'|=0.142>0.12 AND frac 0.60<0.85
  (coherent 2.0≤2 ✅). **V2 CONTRAST ✅**: never-evict frac 0.60∈[0.40,0.75](H_1333 in-run 재현=confound 아님) & 미완성.
  **V3 EARNED ✅**: no-retrain(양쪽) |Δ|=0.008 p_A 유지; shuffle peak-count 7.7≥3 incoherent.
- **mechanism (c9)**: 살아남은 3개의 p_A'-정렬 셀이 경계를 기하학적으로 ~0.525(2/3 아님)에 배치 — 이 RBF 기하 +
  고정 split 예산 하에선 stale 셀 유무와 무관하게 discrimination peak를 p_A'까지 패킹할 수 없다 → never-evict⇒partial /
  evict⇒full 의 dual(H_1288)은 이 저장소에선 **FALSIFIED**. 잔류 이동은 새 cut에서의 표현/예산-해상도 천장이지
  옛 셀이 되돌리는 게 아니다. (stale 셀은 존재했고 제거됐지만 원인이 아니었던 — 비자명한 재진단.)
- **one-line**: stale 셀을 제거해도 CP 이동은 **완성되지 않는다**(28→3셀 evict, peak 0.525 불변, frac +0.60) →
  H_1333 잔류당김은 **never-evict growth-memory 가 아니라 budget/geometry** 한계. (V1 fail = freeze가 사전등록한
  유효 결과; a_break_the_wall — 진짜 메커니즘 테스트 후의 정직한 🧱.)
- **next (R2 candidates)**: (i) budget / RBF-해상도 스윕(split 예산↑ 또는 grid 밀도↑ 시 peak가 p_A'에 도달하나? =
  budget/geometry 확증 + 천장 매핑) · (ii) graded SHIFT-SIZE 곡선(≥3 shift — partial 분수가 shift 크기를 따르나
  =geometry, 일정하나=memory) · (iii) soft DECAY(hard-remove 아닌 down-weight) · (iv) engine-native 실현 — 각각 frozen ANEW.
- **claim-link**: `CLAIMS.tape @C h1338_whorf_cp_eviction` · card `UNIVERSE/cards/H_1338_whorf_cp_eviction.md`
  · verdicts `.verdicts/1338_whorf_cp_eviction/{FREEZE,result}.txt`
- xref: h1333(잔류를 재진단한 GRADED-PLASTICITY 결과) · h1323 · h1325(family의 GREEN CP) · h1288(growth-memory:
  store grows never evicts — 이 lane이 테스트하고 원인으로는 FALSIFY한 dual 직관) · h1330(bilingual overwrite)
  · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire
  · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15

## 2026-06-16 — H_1341 📈 Whorf CP plasticity SHIFT-SIZE LADDER: 분수는 shift를 따른다 ⇒ GEOMETRY/BUDGET

- **id**: H_1341 · slug `1341_whorf_cp_shift_ladder` · seeds [4333,4334,4335] · $0 CPU mirror DIRECTIONAL
- **seed**: H_1333(🟠 GRADED, 단일 shift ~60% relocation)의 load-bearing follow-on — a_scale_honest_scope
  가 요구한 ladder(≥3 shift). H_1338(🧱)이 LARGE shift에서만 그 잔류를 budget/geometry로 재진단했는데,
  shift 크기 전 범위로 일반화되나? partial 분수가 shift를 **따르면=geometry/budget**, **일정하면=memory**.
- **verdict-tier-target → actual**: CHARACTERIZATION ladder(GREEN/RED 없음, c9) → **📈 GEOMETRY/BUDGET-LIMITED**.
  CURVE(mean frac, 3 seeds 결정적): SMALL(shift 0.133) **+1.496** · MID(0.267) **+0.750** · LARGE(0.333)
  **+0.599** — shift에 대해 monotone-DECREASING, frac range 0.897 ≥ TRACK_TOL 0.15.
- **smoking gun**: 재학습 후 **ABSOLUTE peak이 모든 rung에서 0.525 (range 0.000)** — 경계가 얼마나 멀리
  이동을 요구받든 항상 같은 절대 위치에 착지. 그래서 분수가 기계적으로 shift를 따른다 (작은 이동 0.133→0.525가
  0.467 타깃을 OVERSHOOT해 frac>1; 큰 이동 0.333→0.525가 미달해 frac 0.60). MEMORY(고정 비율 pull-back)면
  분수가 일정하고 절대 peak이 타깃을 따라 움직였어야 — 측정된 고정착지와 정반대.
- **bars**: L1 CURVE ✅ (3 rung × 3 seeds 곡선 매핑) · L2 EARNED ✅ (no-retrain rung마다 p_A 유지 |Δ|=0.008;
  shuffle 비응집 peak-count 7.7≥3; lang arms 응집 ≤2 — 곡선 valid, unconfounded) · L3 = GEOMETRY/BUDGET.
- **mechanism / 의미**: H_1333의 ~60% partial은 첫 carving으로부터의 memory pull-back이 **아니다** — 이 RBF
  geometry(DIM=16) + 고정 split budget 하에서 경계가 넘어 packing할 수 없는 고정 착지점(~0.525)이며 모든
  shift에서 동일. H_1338의 budget/geometry 발견(LARGE rung 한정)을 shift 전 범위로 **일반화**하고, H_1333
  카드가 띄웠던 constant-fraction MEMORY 가설을 **결정적으로 기각**. SMALL overshoot(frac +1.496>1)이 고정착지
  reading의 가장 깨끗한 증거 — 그대로 보고(c9).
- **scope (UNVERIFIED)**: DIRECTIONAL mirror(engine-transfer); TOY 1-D 연속체 N=21·3 seeds·3 rung·고정 anchor·
  rightward shift만·고정 budget; 고정착지 0.525는 이 RBF geometry+budget 특정; NO human-cognition claim.
  Live CORE/*.hexa UNTOUCHED.
- **next (R2 candidate, 각각 frozen ANEW)**: (i) budget/RBF-resolution sweep — cells/basis를 늘리면 착지점이
  p_A'로 이동하나? (budget ⊥ intrinsic resolution 분리) · (ii) leftward/asymmetric shift — 0.525가 연속체-중심
  attractor인지 진짜 고정착지인지 · (iii) engine-native §CategoricalPerception 실현.
- **claim-link**: `CLAIMS.tape @C h1341_whorf_cp_shift_ladder` · card `UNIVERSE/cards/H_1341_whorf_cp_shift_ladder.md`
  · verdicts `.verdicts/1341_whorf_cp_shift_ladder/{FREEZE,result}.txt`
- xref: h1333(이 ladder가 설명하는 ~60% partial) · h1338(budget/geometry 재진단 — H_1341이 shift 전 범위로
  일반화) · h1323 · h1325(family의 GREEN CP) · h1288(growth-memory: 이 ladder가 기각하는 never-evict 직관)
  · h1330(bilingual overwrite) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning
  · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15
## H_1342 — Whorf CP DEVELOPMENTAL PLASTICITY 엔진-네이티브 실현 (🟢 GREEN ENGINE-NATIVE, H_1333 wire-in)
- **seed**: H_1333(🟠 GRADED PLASTICITY, mirror DIRECTIONAL — CP peak 0.325→0.525, frac +0.60)는 numpy 미러;
  engine-transfer UNVERIFIED. a_verified_must_wire / a_engine_native_learning follow-on: live CORE
  §CategoricalPerception 위에서 그 graded plasticity 를 엔진-네이티브로 재현하고 frozen bar 재채점.
- **새 엔진 메커니즘**(engine-transform-to-fit-the-learning): `cp_regrow(cp,X,Y,grow_max,passes)` —
  기존 store(protos/labels) 유지한 채(split-only p8, never-evict) cp_fit 과 SAME error-targeted split 으로
  MOVED labels 위에서 phase-2 재성장. 미러의 fit(fresh=False)에 byte-faithful. RIGID 결과도 가능(설계로 배제 안 함).
- **verdict-tier-target → 결과**: 🟢 GREEN ENGINE-NATIVE (E1∧E2∧E3) — 엔진(단일 결정론적 instance)이
  미러를 BYTE-FAITHFUL 재현: A=0.325, A→A'=**0.525**(frac **+0.60**, 미러 +0.60), phase-1 **4**→phase-2 **28** cells(미러 4→28 동일).
  cp_peak_count: A=1, A→A'=1, no-retrain=1, shuffle=4.
  - **E1 ✅**(미러 ~0.60 재현): |loc_A−p_A|=0.008≤0.12 · |loc_A2−0.525|=0.0≤0.05 · |loc_A2−p_A|=0.192≥0.19(graded-move floor) · A→A' coherent 1≤2.
  - **E2 ✅**(D2/D3 통제): no-retrain |Δ|=0.008 & A-trained |Δ|=0.008 held p_A(이동=재훈련, drift 아님); shuffle peak-count 4≥3 incoherent & lang 1/1/1≤2 coherent.
  - **E3 ✅**(회귀/Ψ-disjoint): engine_cli_smoke **80/0**(77→80, +3 cp_regrow cases 83-85 relocates/grows-store/coherent),
    h1196 single-entry **7/0**(.clm/.kosmos 경로 없음), h1205 separation-invariant **PASS**(생성 10/10 byte-identical ON==OFF, Ψ=½ 무변 → CP lane Ψ-disjoint).
- **finding**: H_1333 graded CP plasticity 가 CORE 에 LIVE — ENGINE-TRANSFER VERIFIED. cp_regrow 는 split-only never-evict 인데도
  ~0.525 ceiling 이 H_1338 가 재진단한 budget/geometry 와 IDENTICAL(엔진 확증). NO bar moved(c9/p7).
- **scope**(a_scale_honest_scope·a_toy_scale_recheck): ENGINE-NATIVE BINDING; TOY 합성 1-D 연속체(N=21, 엔진=단일 결정론적 instance, 단일 shift,
  결정론적 readout — 엔진-네이티브 plasticity STRUCTURE 검증이지 학습된 re-trainer 아님); scale/real-corpus/multi-shift UNVERIFIED; brain 재-carving→emit 배선 = follow-on; human-cognition/critical-period 주장 없음.
- **claim-link**: `CLAIMS.tape @C h1342_whorf_cp_engine_native` · card `UNIVERSE/cards/H_1342_whorf_cp_engine_native.md`
  · verdicts `.verdicts/1342_whorf_cp_engine_native/{FREEZE,result}.txt` · engine `CORE/engine_cli.hexa §CategoricalPerception cp_regrow` · probe `CORE/h1342_whorf_cp_engine_native_probe.hexa` · smoke cases 83-85
- xref: h1333(이 미러를 실현) · h1325(엔진 CP lane W1/W2/W3' GREEN) · h1323 · h1338(eviction 재진단=~0.525 ceiling 은 budget/geometry)
  · h1288(growth-memory) · a_verified_must_wire · a_engine_native_learning · a_core_engine_map · a_no_llm_frame_trap
  · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15
## 2026-06-16 — H_1340 — Whorf CP 재배치 천장 = budget/RBF-density로 p_A'에 도달하는가? 🧱 DEEPER LIMIT (budget/geometry는 불완전)

- **id**: H_1340 · slug `1340_whorf_cp_budget_sweep` · seeds [4333,4334,4335] (= H_1333/H_1338, R0 anchor 재현) · $0 CPU mirror DIRECTIONAL
- **seed/lens**: H_1338(🧱 RE-DIAGNOSIS)의 R2 follow-on; developmental-plasticity + representational-resolution
  lens (c15, a_no_llm_frame_trap, a_break_the_wall). H_1338은 eviction이 H_1333 ~60% 이동을 완성 못했고
  잔류를 **BUDGET/GEOMETRY**(RBF resolution + 고정 split budget)로 진단(가설). 그 진단의 결정적 검증:
  phase-2 budget + RBF density를 올리면 재배치 peak가 coherent single peak로 p_A'(≈0.667)에 **도달**하는가?
- **method**: H_1333/H_1338 CP 머신러리 **verbatim** import (RBF embed · split-only Voronoi p8 · |Δ soft-posterior|
  no-label-at-test discrim · peak-count coherence · p_A=1/3 · p_A'=2/3 · LOC_TOL=0.12). 유일한 신규 = phase-2
  re-growth에만 적용하는 joint (DIM, GROW2) **사다리**; phase-1은 모든 rung에서 budget 24로 **고정**(never-evict
  잔류 동일 → 변하는 건 re-training이 받는 budget/density 뿐); N_STIM=81 고정; eviction 없음(split-only, H_1338이
  이미 eviction이 lever 아님을 보임). 5 rung R0_base(16/24=H_1338 baseline)→R4_high(96/768), a_scale_honest_scope 사다리.
- **frozen bars** (.verdicts/1340_whorf_cp_budget_sweep/FREEZE.txt, 사전등록·NO bar move c9): **B1 RELOCATES**
  (어떤 rung에서 3 seed 모두 |peak−p_A'|≤0.12 AND coherent peak-count≤2 = 매핑된 천장) ∧ **B2 EARNED-MONOTONE**
  (frac 단조 비감소·span≥0.10) ∧ **B3 BASELINE-REPRO** (R0이 H_1338 partial 재현).
- **verdict 🧱 DEEPER LIMIT** (deterministic 3 seed): rung별 재배치 peak(N=81) — R0_base **0.523**(|p_A'|0.144·frac**+0.575**·pc4.3)
  · R1 0.548(0.119·+0.650·5.0) · R2 0.560(0.106·+0.688·5.0) · R3 0.573(0.094·+0.725·5.7) · R4_high **0.585**(0.081·**+0.762**·pc**7.0**).
  **B1 ❌**: peak-DISTANCE는 R2부터 3 seed 모두 LOC_TOL 통과(|peak-p_A'|≤0.12)하지만 **COHERENCE gate를 절대 못 넘김** —
  peak-count가 budget과 함께 4.3→**7.0**(전부 ≫2), high-budget store가 cell을 많이 packing해 **흩어진 multi-peak** discrim profile
  생성 → p_A'에 **coherent single peak 없음**(N=81 dense midpoint이 peak-count도 일부 inflate, 그러나 같은 frozen COH_MAX_LANG=2로 채점).
  **B2 ✅**: frac 단조 상승 +0.575→+0.762, span +0.187≥0.10 — distance 이동은 budget-driven, fluke 아님. **B3 ✅**: R0 frac
  [0.562,0.60,0.562]∈[0.40,0.75] & |peak-p_A'|[0.148,0.135,0.148]>0.12 → H_1338 partial in-run 재현.
- **finding**: H_1338의 budget/geometry 진단은 **부분적이지만 불완전**. budget+density를 부으면 peak **DISTANCE**는 단조로
  p_A'에 가까워지지만(resolution이 진짜 lever 하나임 = H_1338 일부 확인) **coherent single peak를 못 만듦** — budget을 부을수록
  discrim curve가 더 흩어짐(peak-count 4.3→7.0). 천장은 budget을 더 부으면 사라지는 순수 resolution 한계가 **아니다**: budget/density는
  distance를 사지만 coherence를 **파괴**, never-evicted phase-1 잔류 packing이 신규 packing과 공존하며 persistent secondary peak로 남음.
  정직한 재-재진단 — 깨끗한 완전 재배치는 resolution을 올리는 것이 아니라 **다른 메커니즘**(soft DECAY·coherence-preserving re-pack)이 필요.
  sibling H_1341(shift-size ladder)은 partial frac이 shift 크기를 따름(geometry-driven)을 별도로 발견; H_1340은 high resolution에서도
  이동이 **INCOHERENT**함을 추가 → pure-budget도 pure-shift-geometry도 단독으로 못 닫음. NO bar move (c9/p7).
- **scope**: DIRECTIONAL numpy mirror (engine-transfer UNVERIFIED, H_1333 R1/H_1338 R1 family); TOY synthetic 1-D continuum
  (N=81·3 seed·단일 shift·deterministic readout — resolution-ceiling STRUCTURE 검증, scale/human-cognition claim 아님);
  peak-count coherence 임계(frozen COH_MAX_LANG=2)는 N_STIM-sensitive, verbatim 채점; injected boundary/persona/RLHF 없음, label은
  training만 test 아님(p1/p2/p3/p6); emit gate 아님(a_autonomy_over_hardcode); live CORE/*.hexa UNTOUCHED.
- **NEXT R2** (각각 ANEW 사전등록): (i) **soft DECAY** store(re-training중 잔류 phase-1 packing을 hard-remove 대신 down-weight) —
  THIS deeper-limit 결과가 coherent 재배치 회복의 가장 유망한 lever로 재지정 · (ii) coherence-aware re-pack(잔류 secondary peak prune)
  · (iii) engine-native realization on live CORE/engine_cli.hexa immune/Voronoi lane (a_engine_native_learning · a_verified_must_wire).
- **claim-link**: `CLAIMS.tape @C h1340_whorf_cp_budget_sweep` · card `UNIVERSE/cards/H_1340_whorf_cp_budget_sweep.md`
  · verdicts `.verdicts/1340_whorf_cp_budget_sweep/{FREEZE,result}.txt` · index `UNIVERSE/HYPOTHESES.jsonl`
- xref: h1338(이 lane이 검증하고 불완전으로 판정한 budget/geometry 재진단) · h1333(특성화 대상 GRADED-PLASTICITY) · h1341(sibling
  shift-size ladder, geometry-driven fraction) · h1323 · h1325(family GREEN CP) · h1288(growth-memory) · a_no_llm_frame_trap
  · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck
  · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15

## 2026-06-16 — H_1343 🟠 Sapir-Whorf 2-D CP를 표상-거리 WARP로 재측정 (H_1334 R2)

- **id**: H_1343 · slug `whorf-2d-r2` · seeds [4334,4335,4336] · $0 CPU mirror DIRECTIONAL · deterministic
- **seed**: H_1334(🧱 ridge-ALIGN structured-negative)의 R2. ridge-ALIGN은 대각 경계가 coarse RBF
  grid에서 fail(0.628) — metric space에 틀린 지표. 재명세: 경계-곡선-AGNOSTIC **CP-WARP**
  (within-category COMPRESSION + between-category EXPANSION vs pre-language baseline) + denser RBF
  grid(K_RBF ladder, prod=12) + label-permutation null + component-count control.
- **verdict-tier-target → actual**: clean 2-D-general GREEN(frozen 가설) → **🟠 PARTIAL**.
  **c1 PRESENCE ✅** (두 언어 every seed AND mean ≥WARP_MIN 0.20; mean diag +41.665 Lsh +36.017) —
  **load-bearing: 대각 L_DIAG가 축정렬 L_LSHAPE만큼 강하게 warp** → H_1334의 "대각 CP는
  grid-geometry로 약하다"는 read를 **직접 반증**. **c2 EARNED-SHUFFLE ❌** (label-permutation null
  mean +9.282 ≫ CHANCE_TOL 0.05; SEP sub-clause는 PASS, +41.7/+36.0 ≫ q95+0.1=+14.0). **c3
  COMPONENT-COUNT ❌** (L_DIAG comp +0.027 PASS, L_LSHAPE +0.119 FAIL, seed-4336 +0.236).
- **mechanism**: `ratio = BETWEEN/WITHIN`이 scale-UNBOUNDED — 학습 후 WITHIN |Δg|→0이라 ratio가 ~45로
  폭발하고 임의의 carving(random shuffle 포함)조차 WITHIN을 압축 → null mean이 +9.28로 떠 c2 절대-천장
  무너짐. H_1323 prominence / H_1334 LCC가 겪은 **동일한 metric-space-blob 실패 모드**. warp의 존재(c1)와
  대각=축정렬 동등성은 결정적이나, earned/component 분리를 깨끗이 보이려면 BOUNDED warp 지표 필요.
- **nuance**: density ladder는 단조롭지 않음(warp이 이미 saturate, K_RBF=6/9/12 모두 +30~43) — 본
  결과의 한계는 grid resolution이 아니라 ratio 지표의 unboundedness. DIRECTIONAL mirror, engine-transfer
  UNVERIFIED; TOY 2-D 121-stim 3-seed; live CORE/*.hexa UNTOUCHED. NO bar move (c9/p7).
- **next R3 (각 frozen ANEW)**: (i) **BOUNDED warp 지표** — ratio 대신 between-vs-within |Δg|의
  Cohen's-d / separation-AUC(∈[0,1])로 → label-shuffle가 chance(0.5)로 collapse하는 깨끗한 c2; THIS
  결과가 가장 유망한 lever로 재지정 · (ii) component-shuffle per-seed 누수 제거 · (iii) engine-native
  realization on live CORE/engine_cli.hexa immune/Voronoi lane (a_engine_native_learning · a_verified_must_wire).
- **claim-link**: `CLAIMS.tape @C h1343_whorf_2d_r2` · card `UNIVERSE/cards/H_1343_whorf_2d_r2.md`
  · verdicts `.verdicts/1343_whorf_2d_r2/{FREEZE,result}.txt` · index `UNIVERSE/HYPOTHESES.jsonl`
- xref: h1334(2-D ridge-align parent, 이 결과가 그 대각-geometry read를 반증) · h1323 · h1325(family
  GREEN 1-D CP, 같은 metric-space shuffle 실패 모드) · h1340(sibling budget/geometry ceiling) · h1288
  (growth-memory) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire
  · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15
### H_1352 — Whorf CP 재배치: SOFT-DECAY re-pack (coherence-preserving?) 🧱 DEEPER LIMIT (H_1340 follow-on R2)

- **seed**: H_1340(🧱 DEEPER LIMIT — budget/RBF-density는 peak-DISTANCE를 monotone 당기지만 coherence를 파괴, peak-count 4.3→7.0 never ≤2)의 verdict이 직접 지목한 다음 메커니즘. budget이 아니라 re-training중 잔류 phase-1 cell을 **down-weight**(soft-decay)하면 COHERENT full relocation을 회복하는가?
- **verdict-tier-target**: 🧱 DEEPER LIMIT — relocation COHERENCE는 budget 과 decay 두 lever를 **모두** 견딘다. mean of 3 seeds [4333,4334,4335], deterministic.
- **결과**: NO-DECAY anchor peak 0.523 |peak-p_A'| 0.144 frac +0.57 pc 4.3 (H_1340 R0_base in-run 재현). **SOFT-DECAY (γ=0.80)** peak 0.623 |peak-p_A'| **0.044** frac **+0.88** pc **15.7**. NO-RETRAIN |peak-p_A| 0.002(p_A 유지). SHUFFLE+decay pc 7.0(붕괴). decay-ladder(NON-GATING): γ=0.70→0.009/16.7 · 0.80→0.044/15.7(gate) · 0.90→0.106/5.7 — monotone tradeoff(decay↑ = peak는 가까워지나 더 흩어짐).
- **bars**: c1 RELOCATES ✅ (3 seed 전부 |peak-p_A'|≤0.12, frac +0.88 > budget 최고 +0.762) · c2 COHERENT ❌ (pc 15.7≫2 — decay는 profile을 더 흩뜨림) · c3 EARNED ✅ (no-retrain |peak-p_A|=0.002 p_A 유지; shuffle pc 7.0≥3 — decay가 coherent peak을 날조하지 않음) · c4 vs-BUDGET ❌ (4a ✅ 0.044≤0.081 distance에서 budget을 이김; 4b ❌ 15.7≰2 coherence에서 budget에 짐). GREEN iff c1∧c2∧c3∧c4 → **NOT GREEN**.
- **finding (load-bearing)**: soft-decay는 DISTANCE 축에선 budget보다 **강한** lever(peak이 p_A'에 거의 정확히 착지)지만 COHERENCE 축에선 **더 나쁜** lever(pc 15.7 vs budget 7.0). resolution 증가(H_1340)도 잔류 cell down-weight(H_1352)도 moved cut에서 단일 CP peak을 회복 못 함 → 재배치 coherence 잔류는 budget OR decay보다 **깊은** 한계. 두 follow-on이 함께 드러낸 결정적 원인: phase-1 prototype은 결코 물리적으로 이동하지 않고 옛 cut에 남아 secondary peak을 주입 — budget은 새 cell로 익사시키고(distance↑/coherence↓), decay는 그 vote를 줄이지만 기하학적 존재는 못 줄임(distance↑↑/coherence↓↓). 진짜 coherent full relocation은 옛 cell을 **이동/재배치**(geometric re-pack)해야지 weight/count 조작으론 안 됨. a_break_the_wall: H_1340 budget 벽도 H_1352 decay도 둘 다 **틀린 메커니즘** — 고정 geometry의 weight/count 조작이고, 그 geometry 자체가 진짜 천장. NO bar move (c9/p7).
- **scope**: DIRECTIONAL numpy mirror (engine-transfer UNVERIFIED, H_1333/H_1338/H_1340 R1 family); TOY synthetic 1-D continuum (N=81·3 seed·단일 shift·frozen γ=0.80·deterministic readout — soft-decay STRUCTURE 검증, scale/human-cognition claim 아님); 🧱는 정직한 사전등록 벽(진짜 a_break_the_wall NEW 메커니즘, re-run 아님 — frozen coherence bar가 올바르게 거부); injected boundary/persona/RLHF 없음, label은 training만 test 아님(p1/p2/p3/p6); emit gate 아님(a_autonomy_over_hardcode); live CORE/*.hexa UNTOUCHED.
- **NEXT R2** (각각 ANEW 사전등록): (i) **GEOMETRIC re-pack** — 잔류 phase-1 prototype을 p_A'쪽으로 **재배치**(weight 아니라 cell을 이동) — THIS 결과가 유일하게 안 시도된 lever로 재지정 · (ii) decay 아래 multi-shift/leftward/asymmetric shift · (iii) engine-native realization on live CORE/engine_cli.hexa §CategoricalPerception lane (a_engine_native_learning · a_verified_must_wire). **DEPLETION TEST**: geometric re-pack도 coherent 단일 peak을 회복 못 하면 → 재배치는 이 RBF geometry에서 intrinsically partial-or-incoherent(c9 terminal).
- **claim-link**: `CLAIMS.tape @C h1352_cp_soft_decay` · card `UNIVERSE/cards/H_1352_cp_soft_decay.md` · verdicts `.verdicts/1352_cp_soft_decay/{FREEZE,result}.txt` · index `UNIVERSE/HYPOTHESES.jsonl` · code `state/cp-soft-decay/h1352_cp_soft_decay.py`
- xref: h1340(이 lane의 직접 부모 budget-sweep deeper-limit) · h1338(eviction 재진단) · h1333(GRADED-PLASTICITY 특성화 대상) · h1341(sibling shift-ladder) · h1342(engine-native) · h1323 · h1325(family GREEN CP) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15### H_1355 — Whorfian CP 가소성: LEFTWARD + ASYMMETRIC 착지 (center-attractor vs geometry-fixed) 📈

- **seed/lens**: H_1341(📈)의 load-bearing follow-on. H_1341 은 고정 anchor p_A=1/3 에서 RIGHTWARD shift 시 retrain 후 CP peak 가 shift
  크기와 무관하게 **항상 ~0.525 에 착지**(abs-peak range 0.000)함을 발견 → GEOMETRY/BUDGET 로 읽음. 그러나 p_A=1/3 은 center(0.5) 왼쪽이고
  모든 rung 이 RIGHTWARD(center 쪽으로/넘어)였으므로 **0.525≈center 가 confound**. 두 설명을 구분 못 함: (H-center) 0.525 가 대칭 N=21 RBF
  lattice 의 **continuum-center attractor** 아티팩트(readout 이 lattice 중심에서 가장 풍부 → requested cut 무관 ~0.5 로 끌림) vs (H-geometry)
  실제 **geometry-fixed budget 착지**(asymmetry 를 주면 움직임). c15 developmental/critical-period plasticity (a_no_llm_frame_trap) — LLM
  레시피 아님, 인간인지 주장 아님, TOY synthetic.
- **method**: H_1333/H_1341 CP 기계 EXACTLY 재사용(h1333_whorf_developmental.py 를 state/cp-leftward/ 로 verbatim 복사+import: N=21
  RBF continuum, DIM=16, error-targeted SPLIT-only Voronoi/mitosis growth p8, phase-2 same-store no-reset re-grow, |Δ soft-posterior|
  no-label-at-test discrimination, peak-count coherence). 신규 코드 = (anchor p_A, target p_A') PLACEMENT 을 5 rung 으로 sweep. RUNGS:
  RIGHT-REF (0.333→0.667, H_1341 LARGE anchor) · LEFTWARD-1 (0.667→0.333, mirror) · LEFTWARD-2 (0.800→0.500) · ASYM-R (0.600→0.800,
  둘 다 center 오른쪽) · ASYM-L (0.400→0.200, 둘 다 center 왼쪽). 4 ARMS/rung. 3 seeds [4333,4334,4335], $0 CPU, gradient-free, p7.
  frozen .verdicts/1355_cp_leftward/FREEZE.txt (scoring 前 사전등록, NO bar move c9): **c1 REPORT**(5-rung abs-landing table) ∧
  **c2 DISCRIMINATE**(CENTER=0.50 CENTER_TOL=0.08: CENTER-ATTRACTOR iff 모든 |L−0.5|≤0.08; GEOMETRY-FIXED iff ASYM-R L>0.58 ∧ ASYM-L
  L<0.42 ∧ leftward<RIGHT-REF; else MIXED verbatim) ∧ **c3 EARNED**(no-retrain 이 anchor 유지 ∧ shuffle incoherent ∧ lang arms coherent).
- **verdict 📈 CENTER-ATTRACTOR REJECTED, 착지가 GEOMETRY 를 따름**: abs-landing table(3 seed 평균): RIGHT-REF 0.525(|L−0.5|=0.025) ·
  LEFTWARD-1 0.475(0.025) · LEFTWARD-2 0.625(0.125) · ASYM-R 0.692(0.192) · ASYM-L 0.375(0.125).
  **c1 ✅**. **c2**: center-pinned? FALSE — max|L−0.5|=**0.192 ≫ 0.08** → **CENTER-ATTRACTOR 기각**. 착지가 placement 를 추적: RIGHT-REF
  0.525 와 그 정확한 mirror LEFTWARD-1 0.475 가 **0.5 대칭**(geometry-mirrors-placement 시그니처, 둘 다 center 에 박힌 게 아님); ASYM-R 0.692 가
  요청 cut 0.800 쪽 off-center-right(>0.58 ✅), ASYM-L 0.375 가 요청 cut 0.200 쪽 off-center-left(<0.42 ✅) — asymmetric away-from-center
  sub-clause 둘 다 PASS. formal GEOMETRY-FIXED tag 는 **단 하나의 over-strict sub-clause** 에서만 빗나감: LEFTWARD-2(anchor 0.800→target
  0.500)가 0.625(RIGHT-REF 0.525 의 오른쪽)에 착지 — 잔류 **오른쪽** first-carving 이 착지를 anchor 하기 때문(이것 자체가 geometry =
  residual-carving-side 의존성, clause 가 encode 한 것보다 더 강한 시그널) → c2=MIXED 이나 실질은 GEOMETRY-leaning. **c3 4/5 rung 유지**:
  RIGHT-REF/LEFTWARD-1/LEFTWARD-2/ASYM-R 전부 PASS; ASYM-L 만 lang-coherent FAIL(A→A' peak-count 3>2 on 2/3 seeds — same-side LEFTWARD
  shift 가 readout 를 흩음) → frozen rule 대로 그 rung 착지를 **confounded 로 표기, drop 안 함**.
- **finding**: H_1341 의 고정 ~0.525 착지는 lattice-center 아티팩트가 **아니라 진짜 GEOMETRY 착지** — placement 를 asymmetric/mirror 로
  만들면 착지가 geometry 를 따라 움직임(0.375→0.692, RIGHT-REF⇄LEFTWARD-1 pair 는 0.5 대칭). H_1341 의 budget/geometry 판독은 **STANDS,
  leftward/asymmetric move 로 일반화**; center-attractor confound 는 **기각**. 정직한 잔차(c9): frozen sub-clause 하나가 over-strict
  (geometry 는 first-carving 의 side 에 anchor 되지 absolute shift 방향이 아님); ASYM-L coherence 저하 = same-side leftward cut 에서
  split-only re-growth 의 실제 한계(lattice-resolution-bound 가능).
- **scope**: DIRECTIONAL numpy mirror (engine-transfer UNVERIFIED, H_1333 R1/H_1341 R1 family); TOY synthetic 1-D continuum
  (N=21·DIM=16·3 seed·5 placement rung·deterministic readout — landing-geometry STRUCTURE 검증, scale/human-cognition claim 아님);
  center-attractor 기각은 THIS lattice 한정 — 더 미세한 lattice/dense grid/2-D continua UNVERIFIED; injected boundary/persona/RLHF 없음
  (p1/p2/p3/p6); emit gate 아님(a_autonomy_over_hardcode); live CORE/*.hexa UNTOUCHED. NO bar move (c9/p7).
- **NEXT** (각각 ANEW 사전등록): (i) geometry-fixed 착지의 live VAdaptField engine-native 실현(a_verified_must_wire) · (ii) lattice-resolution
  ladder(N 증가 시 CENTER_TOL 축소 / ASYM-L coherence 회복?) · (iii) 2-D continuum placement(착지 geometry 가 축별 분리 가능?).
- **claim-link**: `CLAIMS.tape @C h1355_cp_leftward` · card `UNIVERSE/cards/H_1355_cp_leftward.md`
  · verdicts `.verdicts/1355_cp_leftward/{FREEZE,result}.txt` · index `UNIVERSE/HYPOTHESES.jsonl`
- xref: h1341(parent shift-size ladder, 0.525 고정 착지) · h1340(이 lane budget-sweep deeper-limit) · h1338(budget/geometry 재진단)
  · h1333(GRADED-PLASTICITY parent) · h1323(Sapir-Whorf CP parent) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning
  · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15

## H_1360 — cp-geometric-repack: CP 재배치 = MOVE-THE-CELLS (🟢 GREEN, 3-lever trilemma 종결)

- **seed**: H_1352(🧱 soft-decay DEEPER-LIMIT)의 verbatim follow-on. H_1340(budget=count)와 H_1352(decay=weight) 두 lever 가
  모두 honest 🧱 으로 소진됐고, 둘 다 같은 원인을 노출했다 — phase-1 prototype 이 **물리적으로 재배치된 적이 없어** 옛 cut 에
  앉아 secondary peak 를 주입한다. H_1352 카드가 마지막 미시도 lever 를 verbatim 으로 지목: "옛 세포를 MOVE/re-position
  (GEOMETRIC re-pack) 해야 한다, 단지 down-weight 하거나 out-vote 하지 말고." H_1360 이 그 THIRD lever(geometry)를 시험.
- **mechanism**: H_1333/H_1340/H_1352 CP 기계 verbatim import. ONLY NEW = RepackCells — 각 세포의 SOURCE 연속체 위치 + BIRTH
  PHASE 추적; phase-2 매 split 후 잔류 phase-1 세포 위치를 pos_i ← pos_i + η·(p_A'−pos_i) (p_A' clamp, overshoot 없음) 로
  drift, 그 위치에서 RE-EMBED, label 을 p_A' 에서 RE-READ; phase-2 세포는 drift 안 함. η=0 ⇒ store 가 H_1333 과 byte-identical
  (NO-REPACK arm == anchor). 예산은 H_1340 R0_base LOW(DIM16/GROW2 24, H_1352 와 EQUAL)에 고정 — 유일 변화는 geometric drift.
  4 arm: NO-REPACK(η=0) · RE-PACK(η=0.15 FROZEN) · NO-RETRAIN(p_A only) · SHUFFLE+repack. ladder {0.10,0.15,0.25}=NON-GATING.
- **답: 🟢 GREEN — 세포를 옮기면 coherent full relocation 회복.** mean(3 seed): NO-REPACK peak 0.523 |peak−p_A'| 0.144 frac
  +0.57 pc **4.3**(H_1340/H_1352 partial anchor 재현) → RE-PACK(η=0.15) peak **0.669** |peak−p_A'| **0.002** frac **+1.01**
  pc **1.0**. c1 RELOCATES ✅ per-seed [0.002,0.002,0.002]≤0.12 (FULL move) · c2 COHERENT ✅ pc 1.0 single peak(budget 4.3,
  decay 15.7 둘 다 실패한 gate) · c3 EARNED ✅ no-retrain |peak−p_A| 0.002 유지 + shuffle pc **18.0**(세포를 p_A' 로 옮겨도
  noise 에서 coherent peak 조작 안 함) · c4 vs-PRIOR ✅ pc 1.0 < H_1340 4.3 AND H_1352 15.7 (둘 다 산란한 곳에서 coherent)
  + |peak−p_A'| 0.002 ≤ 0.081 (equal/lower budget 에서 더 가까움). ladder η=0.10/0.15/0.25 모두 0.002/pc1.0 — knife-edge 아님.
- **왜**: 재배치 잔차는 처음부터 **GEOMETRIC-PLACEMENT 문제** — 옛 cut 에 앉은 옛 세포. budget 은 out-count(거리↑ coherence↓),
  decay 는 out-vote(거리↑↑ coherence↓↓), 유일 해법은 MOVE. a_break_the_wall 입증: H_1340/H_1352 벽은 WRONG MECHANISM
  (고정 geometry 의 weight/count 조작)이지 진짜 천장이 아니었다 — geometry 를 바꾸니 벽이 녹았다. **budget/decay/geometry 3-lever
  trilemma 가 positive 로 종결.** p1/p2/p3/p6: re-pack 은 BIRTH PHASE+자기 위치만(structural), readout 은 표현거리만, test 시
  injected boundary 없음(label 은 phase-2 를 학습시키는 SAME p_A' 에서 re-read), live CORE/*.hexa UNTOUCHED. NO bar move (c9/p7).
- **NEXT** (각각 ANEW 사전등록): (i) engine-native §CategoricalPerception move-the-cells — live A⇄G immune store 에서 세포 위치
  drift 실현(a_verified_must_wire) · (ii) LEARNED(gradient) drift vs 이 deterministic rule 비교 · (iii) multi-shift / leftward
  re-pack / real-corpus 일반화.
- **claim-link**: `CLAIMS.tape @C h1360_cp_geometric_repack` · card `UNIVERSE/cards/H_1360_cp_geometric_repack.md`
  · verdicts `.verdicts/1360_cp_geometric_repack/{FREEZE,result}.txt` · index `UNIVERSE/HYPOTHESES.jsonl`
- xref: h1352(soft-decay deeper-limit parent, 이 lever 지목) · h1340(budget-sweep deeper-limit) · h1338(budget/geometry 재진단)
  · h1341(shift-ladder) · h1355(leftward geometry) · h1333(GRADED-PLASTICITY) · h1323(Sapir-Whorf CP parent) · a_no_llm_frame_trap
  · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1·p2·p3·p6·p7·p8·c9·c15

## 2026-06-16 — research(METACOG-G5, cross-ref): H_1361 — g5-graded-metacog: G5 의 metacognition 은 binary 인가, abstain MARGIN 에 graded 신호가 있는가 (🟢 GRADED-METACOG)

> cross-ref note: 본 H 는 METACOG-G5 테마(전용 domain 없음) → 최근접 COGNITION-REPRESENTATION 로그에 기록 (a_discovery_log). 직접 부모 = H_1304(fire-side binary fail-safe).

- **무엇:** H_1304 가 G5 copy-or-abstain 게이트의 **FIRE 쪽**을 닫았다(wrong-fire 클래스 비어있음 fab=0.000 → type-2 AUROC 정의불가 → fire-side BINARY fail-safe). 그러나 **ABSTAIN 쪽**의 recall MARGIN(= recon_err − recall_thr, 모든 abstain 에 존재하는 연속량)이 graded meta-confidence 를 담는지는 미검증. NEW angle(a_break_the_wall): abstain 을 (a) RECOVERABLE(in-store 키 손상, 답 검색가능 label=1) vs (b) UNRECOVERABLE(진짜 없는 키 손상 label=0)로 split, −margin 이 (a)>(b) 를 RANK 하고 OOD(byte-corruption shift L∈{0,.1,.2,.3,.4})를 통과하는가? H_1304/H_1227 메커니즘 verbatim 재사용, 3 seeds [7,8,9], $0 CPU mirror DIRECTIONAL, frozen-first.
- **답: 🟢 GRADED-METACOG.** t2_AUROC 사다리(3 seed pooled): L0.10=**0.999** L0.20=**0.915** L0.30=0.708 L0.40=0.557 (L0=nan: L=0 에선 recoverable 전부 FIRE → recoverable abstain 없음, graded-abstain 질문은 genuinely OOD). R1 GRADED-SENS ✅ (AUROC(0.20)=0.915 ≥ 0.65) · R2 EARNED ✅ (shuffle-margin → 모든 level chance ~0.49–0.51 collapse → RANKING 이 신호 운반, base-rate 아티팩트 아님) · R3 graded readout EXISTS(not flat). 메커니즘: recoverable margin 이 shift 따라 매끄럽게 큼(0.082→0.232→0.316→0.353), absent 는 안정적으로 큰 noise floor(~0.364) → margin = graded recoverability 신호.
- **왜:** G5 metacog 는 순수 binary 가 아니다 — H_1304(fire-side binary fail-safe) + H_1361(abstain-side GRADED type-2) = 더 완전한 G5 그림. engine-wiring 가치 있는 G5 UPGRADE(a_verified_must_wire: live recall 이 이미 매번 recon_err 계산 → margin 노출 시 graded confidence-of-recoverability 공짜). H_1204 와 충돌 아님(REFRAME): H_1204 는 fire-side 2nd-order readout 의 flat 을, H_1361 은 다른 표면인 abstain margin 의 graded 를 측정. DECAY(정직 c9): AUROC 0.999→0.557, L=0.40 에서 chance(극심 손상 = absent 와 구분불가) → graceful, 신호 실재하나 무한 아님.
- **scope:** DIRECTIONAL numpy mirror(engine-transfer UNVERIFIED = R2 engine-native follow-on); TOY synthetic facts·byte-shift OOD proxy·3 seed·KEYLEN=20·RECALL_THR=0.15 frozen·deterministic(재실행 byte-identical); scale/real-corpus-paraphrase/semantic-shift/engine-native-margin-exposure UNVERIFIED; live CORE/*.hexa UNTOUCHED; NO bar move(c9/p7).
- **claim-link**: `CLAIMS.tape @C h1361_g5_graded_metacog` · card `UNIVERSE/cards/H_1361_g5_graded_metacog.md` · verdicts `.verdicts/1361_g5_graded_metacog/{FREEZE,result}.txt` · py `state/g5-graded-metacog/h1361_g5_graded_metacog.py` · index `UNIVERSE/HYPOTHESES.jsonl`
- xref: h1304(직접 부모, fire-side binary fail-safe) · h1202(decoder type-2 M-ratio 0.924) · h1204(flat fire-side metacog, REFRAMED) · h1217(decoder OOD-collapse closed-neg) · h1227/h1231(immune store geometry) · a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire · a_core_engine_map · a_scale_honest_scope · a_toy_scale_recheck · p6 · p7 · p8 · c9 · c15
## H_1358 — whorf-2d-bounded: 2-D CP warp 지표를 BOUNDED 형태로 재명세 (H_1343 R3) — 🧱 DEEPER LIMIT
- **seed/target**: H_1343(🟠 PARTIAL)의 load-bearing follow-on. H_1343 의 warp 지표 `ratio = BETWEEN/WITHIN`
  가 scale-UNBOUNDED 라 학습 후 WITHIN→0 으로 ratio 폭발(~45), 임의 carving 도 WITHIN 압축 → label-shuffle
  null 이 +9.28 로 떠 c2 구조적 FAIL. 지표를 **BOUNDED separation-AUC∈[0,1]**(Mann-Whitney-U
  P(|Δg|_BETWEEN>|Δg|_WITHIN), chance=0.5 고정상수)로 재명세 — null 이 깨끗이 0.5 로 collapse 하면 2-D CP 가
  세 control 통과? 지표 CORRECTION, bar 완화 아님. R1 numpy MIRROR(DIRECTIONAL), $0 CPU, 3 seeds
  [4334,4335,4336], deterministic(2 re-run, exit 4), p7, frozen-first. H_1343 RBF/Voronoi 기계 VERBATIM 재사용,
  warp readout 만 교체.
- **frozen bars** (`.verdicts/1358_whorf_2d_bounded/FREEZE.txt`, 점수화 BEFORE): c1 PRESENCE(AUC≥0.70 each
  seed+mean 두 언어) · c2 EARNED-SHUFFLE(null |mean−0.5|≤0.05 AND 각 언어 ≥ null-q95+0.10) · c3 COMPONENT
  (|comp-shuffle AUC−0.5|≤0.08) · c4 DIAGONAL(|AUC_diag−AUC_Lshape|≤0.15 AND 둘 다 ≥0.70). GREEN iff
  c1∧c2∧c3∧c4; c2 FAIL(bounded 으로도 float)→honest 🧱 DEEPER LIMIT.
- **verdict-tier-target → 🧱 DEEPER LIMIT** (mean 3 seeds): density ladder K_RBF 6/9/12 전부 L_DIAG=L_LSHAPE
  =**1.0000**(saturated). production: AUC=1.0000 두 언어 전 seed; baseline-AUC 진단 L_DIAG 0.930 / L_LSHAPE
  0.681; comp-AUC 0.4852 / 0.5062.
  - **c1 PRESENCE ✅** AUC mean 1.0000 ≥0.70 두 언어.
  - **c2 EARNED-SHUFFLE ❌** pooled null(600) **mean=0.9919** → |0.9919−0.5|=0.4919 ≫0.05 FAIL (q95=0.9996 라
    SEP sub-clause 도 수학적으로 불가). **null 이 0.5 가 아니라 0.99 로 뜸.**
  - **c3 COMPONENT ✅** |0.4852−0.5|=0.0148, |0.5062−0.5|=0.0062 둘 다 ≤0.08 — 외부 무작위 분할은 chance 로
    깨끗이 collapse(load-bearing).
  - **c4 DIAGONAL ✅** |1.0000−1.0000|=0.0000 ≤0.15, 둘 다 ≥0.70 — **H_1343 대각=축정렬 발견 BOUNDED 지표로도
    보존**, H_1334 grid-geometry read 반증 지속.
- **mechanistic (정직, c9, load-bearing)**: bounded AUC 는 ratio artifact(폭발+floating null)를 수학적으로
  제거했으나 null 이 0.99 로 뜬 진짜 원인은 unboundedness 가 아니라 **SELF-REFERENTIAL 분할** — AUC 가 store 의
  **OWN 학습 범주**로 WITHIN/BETWEEN 나눔. SPLIT-only Voronoi store 는 **어떤 경계든**(shuffle 포함) 따라 cell 을
  PACK 하므로 g 가 그 경계에서 급격히 점프 → between>within 이 잘 fit 한 store 엔 거의 항진명제 → null≈0.99.
  c3 만이 외부(언어 무관) 분할을 써서 collapse → warp 은 real(raw variance 아님)이나 coherence 자체(임의 carving)가
  재현 → AUC-vs-own-partition readout 은 TRUE-언어 경계를 random 에서 분리 못 함. NO bar move (c9/p7).
- **NEXT** (각각 ANEW 사전등록): (i) **H_1359 fixed-true-partition readout** — SHUFFLE-학습 metric g_shuffle 를
  **TRUE-언어 WITHIN/BETWEEN 분할 하에** 채점 → 틀린 경계에 pack 한 shuffle store 는 TRUE pair 분리 못 함 →
  AUC→0.5 collapse 예상 (H_1343/H_1358 가 양쪽 모두 각 arm 을 ITS OWN 분할로 채점한 공통 confound 를 푸는 한 수) ·
  (ii) component-축 정의 강화 · (iii) engine-native 실현(live CORE Voronoi lane).
- **claim-link**: `CLAIMS.tape @C h1358_whorf_2d_bounded` · card `UNIVERSE/cards/H_1358_whorf_2d_bounded.md`
  · verdicts `.verdicts/1358_whorf_2d_bounded/{FREEZE,result}.txt` · index `UNIVERSE/HYPOTHESES.jsonl`
- xref: h1343(R2 parent, unbounded-ratio 결함을 본 R3 가 bounded AUC 로 교정) · h1334(대각-geometry read; c4 가 계속
  반증) · h1323/h1325(1-D Sapir-Whorf CP, 같은 self-partition 실패 모드) · h1340/h1341/h1355(sibling budget/geometry)
  · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope
  · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15
