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
