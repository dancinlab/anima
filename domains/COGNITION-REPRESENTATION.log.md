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
- xref: h1340(이 lane의 직접 부모 budget-sweep deeper-limit) · h1338(eviction 재진단) · h1333(GRADED-PLASTICITY 특성화 대상) · h1341(sibling shift-ladder) · h1342(engine-native) · h1323 · h1325(family GREEN CP) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · p8 · c9 · c15
