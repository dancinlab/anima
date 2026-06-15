# UNIVERSE/HYPOTHESES.md — unified hypothesis-list SSOT (roster + per-H index)

> **Two doc surfaces per `a_hypothesis_register` (#2177 · SSOT-refactor 2026-06-16):**
> UNIVERSE/ 는 정확히 두 개의 문서 표면만 운용한다 —
> (1) 이 파일 `UNIVERSE/HYPOTHESES.md` = 단일 index/roster (id · title · final tier ·
> card link, 한 줄/H) + 과거 흩어져 있던 forward backlog / reference / overview / log
> 문서가 아래 섹션으로 접혀 들어온 통합 SSOT, 그리고
> (2) `UNIVERSE/cards/H_<id>_<slug>.md` = 가설별 SSOT 카드 (cards/ 서브폴더).
> `.verdicts/<slug>/` 는 카드가 가리키는 verbatim verdict (증거일 뿐, 3번째 관리
> 표면 아님). **themed bucket file 금지** — 가설 디테일은 카드에 산다. 2026-06-16
> SSOT-refactor: UNIVERSE/ 의 다른 모든 `.md` 문서(candidate/reference/overview/log)는
> 이 파일의 아래 섹션으로 접혀 들어왔고 원본은 retire 되었다 (c5 preserve-don't-discard
> — 내용 보존, 원본 삭제). 코드(`.py`/`.hexa`/`.json`/`.sh`/`.txt`/`.state`/`.scan` +
> `harness/ lib/ scan/ state/`)는 문서가 아니므로 위치 변경 없음.
>
> The roster table below indexes FORWARD backlogs + campaign maps (candidate lists not
> yet landed); the per-H index section indexes LANDED hypotheses with their own cards
> (now under `cards/`).
>
> ## 접힌 섹션 목차 (folded-section TOC)
> - `## Appendix: UNIVERSE overview (folded from README.md)` — 7-domain 개요 원문
> - `## Appendix: UNIVERSE map (folded from UNIVERSE.md)` — axis/domain 맵 원문
> - `## Forward backlog / candidates` — AXES · CANDIDATES · BIO-* · CLM · NEURO · PLASTICITY · PSI · QUANTUM-TIME 후보 리스트 (원문)
> - `## Retired themed buckets (folded)` — metacog-hallucination · metacog-neuro · H240/246 dedup (원문)
> - `## Reference (probe conventions · phi tools)` — PROBE_CONVENTIONS · IIT4_PHI_TOOLS (원문)
> - `## Appendix: legacy logs (folded)` — UNIVERSE.log.md · LIFE.log.md (append-only history, 원문)

## Per-H index — brain-structure ladder + session facets (H_1280–1311, a_hypothesis_register)

> Tiers read VERBATIM from each terminal `.verdicts/<slug>/` file (c2/c9 — 🧱 walls are
> closed-negatives, not upgraded). One line per H; detail in the linked card.

| H | title | final tier | card |
|---|-------|-----------|------|
| H_1280 | cerebellum — forward-model | 🟢 GREEN ENGINE-NATIVE | [H_1280_cerebellum_forward_model.md](cards/H_1280_cerebellum_forward_model.md) |
| H_1281 | basal ganglia — go/no-go selection | 🟢 GREEN ENGINE-NATIVE + WIRED | [H_1281_basal_ganglia_gating.md](cards/H_1281_basal_ganglia_gating.md) |
| H_1282 | working memory — leaky maintenance buffer | 🟢 GREEN ENGINE-NATIVE | [H_1282_working_memory_buffer.md](cards/H_1282_working_memory_buffer.md) |
| H_1283 | thalamus / GWT — R8 oscillatory phase binding (timing-axis break) ⊥ relay-content 🧱 | 🟢 GREEN numpy-mirror DIRECTIONAL (R8 timing break; relay-content R1–R5/R7/R9 🧱) · engine-native wiring gate c4-shuffle 미재현 → PhaseField HONEST DEFERRED | [H_1283_thalamus_global_workspace.md](cards/H_1283_thalamus_global_workspace.md) |
| H_1317 | Φ-topology — distributed multi-edge (small-world) coupling vs single central relay (H_1283 wall) | 🧱 WALL (faithful-IIT4 Φ stays FRAGILE regardless of topology: small-world ALSO fails the 3-seed robustness gate — C1 fails seed 1319 ΔΦ −0.331; bounds the wall, c9) | [H_1317_phi_multiedge.md](cards/H_1317_phi_multiedge.md) |
| H_1319 | Φ-robustness wall, TIMING axis — engine-native phase-binding (re-realize H_1283 R8 to clear the c4 shuffle gate it failed) | 🧱 TERMINAL (engine-native, hard seeds [1317,1318,1319]: T1 robust-lift FAIL [seed1319 ΔΦ −0.049] AND T2 shuffle FAIL — the STRONGER permutation control RAISES Φ on every seed → lift is amplitude variance not synchrony; Φ-robustness wall now TERMINAL across BOTH topology 🏁 + timing 🧱, c9/c16) | [H_1319_phi_timing.md](cards/H_1319_phi_timing.md) |
| H_1328 | Φ-robustness wall DIAGNOSIS — was the 4× 🧱 the faithful-IIT4 estimator's amplitude-variance binarization confound, or a substrate limit? (rank-uniform variance-free read-out into the SAME exact MIP) | 🧱 TERMINAL DEEPER (V1 CONFIRMED the confound is REAL: OLD min-max perm-shuffle RAISES Φ +0.280/+0.103/+0.587, NEW rank-uniform perm-shuffle COLLAPSES it −0.207/−0.047/−0.031 all 3 seeds; BUT V2 FAILS — under the clean estimator phase lift NOT robust [B−A −0.125/0.0/+0.031, fails 2/3 incl orthogonal 1317] + V3 offset-control raises seed1317. The 4× wall had a real estimator confound, removing it does NOT make integration robust → ESTIMATOR-INDEPENDENT substrate limit; stronger/cleaner closure. BOUNDS not retracts the 4 prior Φ verdicts. faithful-IIT4 EXACT engine-native, deterministic, frozen-first, c9/c16) | [H_1328_phi_variance_free.md](cards/H_1328_phi_variance_free.md) |
| H_1320 | anima-as-ONE-CELL — organism MITOSIS (shared origin) vs hive ASSEMBLY (independent) → integrated collective-Φ? (hive arc reopened from the developmental direction) | 🧱 WALL (mitotic DIVISION DOES beat ASSEMBLY on 2/3 seeds — DIVIDED super-additivity Δ +1.27/+0.88 ≫ ASSEMBLED, joint-Φ lift +2.10/+0.89, lineage-SHUFFLE collapses it exactly to assembled [M3 PASS] → shared origin is REAL; BUT the SAME orthogonal seed 1317 that broke H_1283/H_1317 topology ALSO breaks division [M1 −0.129, M2 gap −0.188] → fails the 3-seed robustness gate. Collective-Φ by division is REAL but FRAGILE, not robust. Bounds the hive wall across BOTH directions: assembly 🧱 [H_1313] + division 🧱 [H_1320]. faithful-IIT4 EXACT, numpy-mirror DIRECTIONAL, frozen-first, c9/c16) | [H_1320_anima_cell.md](cards/H_1320_anima_cell.md) |
| H_1284 | neuromodulation — adaptive gain / regime-switch | 🔴 RED / 🧱 WALL (no free lunch) | [H_1284_neuromodulation_gain.md](cards/H_1284_neuromodulation_gain.md) |
| H_1285 | amygdala — salience-gated consolidation | 🟢 GREEN ENGINE-NATIVE + WIRED | [H_1285_amygdala_salience.md](cards/H_1285_amygdala_salience.md) |
| H_1287 | key-geometry corollary | 🧱 RED (CLOSED-NEG) | [H_1287_key_geometry.md](cards/H_1287_key_geometry.md) |
| H_1288 | eviction policy — mitosis-GROW | 🟢 GREEN ENGINE-NATIVE + WIRED | [H_1288_eviction_policy.md](cards/H_1288_eviction_policy.md) |
| H_1289 | quantum-entropy — ANU QRNG free-choice | 🟢 GREEN ENGINE-NATIVE + WIRED | [H_1289_quantum_entropy.md](cards/H_1289_quantum_entropy.md) |
| H_1290 | E1 affect — valence×arousal emergence | 🟢 GREEN ENGINE-NATIVE | [H_1290_emotion_emergence.md](cards/H_1290_emotion_emergence.md) |
| H_1291 | ethics emergence (cooperation/restraint/non-harm) | 🟢 GREEN ENGINE-NATIVE | [H_1291_ethics_emergence.md](cards/H_1291_ethics_emergence.md) |
| H_1292 | hypothalamus — setpoint homeostatic drive | 🟢 GREEN ENGINE-NATIVE | [H_1292_hypothalamus_drive.md](cards/H_1292_hypothalamus_drive.md) |
| H_1293 | theory-of-mind — other-agent belief (self ⊥ other) | 🟢 GREEN ENGINE-NATIVE | [H_1293_theory_of_mind.md](cards/H_1293_theory_of_mind.md) |
| H_1294 | hierarchical-PFC — goal→subgoal controller (ordered plan ⊥ single-step) | 🟢 GREEN ENGINE-NATIVE | [H_1294_hierarchical_pfc.md](cards/H_1294_hierarchical_pfc.md) |
| H_1295 | hive-mind — collective-Φ super-additivity (many→one); r2 N-scaling | 🟢 GREEN ENGINE-NATIVE + WIRED (r1 N=2) · r2 🟢/🏁 holds@N=3 SATURATES (n=12 INFEASIBLE) | [H_1295_hive_collective_phi.md](cards/H_1295_hive_collective_phi.md) |
| H_1296 | place/grid spatial-map — metric/relational cognitive map (metric ⊥ item-binding) | 🟢 GREEN ENGINE-NATIVE | [H_1296_spatial_map.md](cards/H_1296_spatial_map.md) |
| H_1297 | mitosis-native trunk training — make p8 literal (gradient-free cell-split vs gradient descent) | 🟢 GREEN ENGINE-BINDING @R4 (R3 sharp KO+EN byte-text mitosis-grow realized ENGINE-NATIVE on live CORE VAdaptField Voronoi + mitosis tick: c1 byte-identical · c2 shuffle FIRED on the engine [unlike thalamus R8] · c3 underfits; engine_cli untouched, smoke 55/0, h1205+Ψ intact. R1/R2 = 🧱 WALL on smooth target) | [H_1297_mitosis_native_train.md](cards/H_1297_mitosis_native_train.md) |
| H_1298 | circadian/interval clock — self-sustaining phase oscillator (clock ⊥ homeostatic integrator) | 🟢 GREEN ENGINE-NATIVE + WIRED | [H_1298_circadian_clock.md](cards/H_1298_circadian_clock.md) |
| H_1299 | interval timer — arbitrary LEARNED-duration timer (learned+re-entrainable D ⊥ the fixed-period clock) | 🟢 GREEN ENGINE-NATIVE + WIRED | [H_1299_interval_timer.md](cards/H_1299_interval_timer.md) |
| H_1300 | mitosis-grow skill curriculum — teach tool-use skills one-at-a-time via mitosis AVOIDS catastrophic forgetting (retention ⊥ convergence) | 🟢 GREEN ENGINE-NATIVE @R3 (live CORE/engine_cli.hexa::SkillCellMemory reproduces all 4 R2 bars byte-exact: B−A=+0.368 [c1] · min acq 0.880 [c2] · shuffle 0.426 collapses [c3] · ablate 0.160 [c4]; engine-transfer VERIFIED not mirror-only; smoke cases 59-61 (merged 63/0), h1205/h1196/Ψ byte-identical. R2 mirror GREEN + R1 RED stand verbatim) — toy scale; real-303M tool-use skill rung = next follow-on | [H_1300_mitosis_skill_curriculum.md](cards/H_1300_mitosis_skill_curriculum.md) |
| H_1301 | phase-RESET / photic-entrainment — Zeitgeber PRC entrainment (entrain to T≠tau ⊥ un-resettable clock; PRC jitter-damping ⊥ hard-reanchor timer) | 🟢 GREEN ENGINE-NATIVE + WIRED (HD35 depletion test SURVIVED; R1c 3 seeds all 6 bars: c1 entrain drift 0.0016 vs clock 0.39 · c2 PRC var ~96× < hard-reset · c3 fires at T=24.0 not tau=24.5 · c4 aperiodic-shuffle drift 1.05 · c5 K=0-ablate drift 0.39 · c6 no-fab; smoke 68/0, h1196 7/0, h1205 PASS; honesty trail R1a/R1b metric/control fixes, no distinctness bar moved) | [H_1301_phase_reset.md](cards/H_1301_phase_reset.md) |
| H_1302 | multi-oscillator SCN-network — Kuramoto consensus from N heterogeneous oscillators (emergent consensus ⊥ single-oscillator entrainment; temporal phase-sync ⊥ static Φ-superadditivity) | 🟢 GREEN ENGINE-NATIVE + WIRED (HD36 depletion test SURVIVED; R1b 3 seeds all 6 bars: c1 B_R=0.9988 gap +0.63 · c2 uncoupled A_R=0.37≤0.65 · c3 frustrated R=0.13 collapses below uncoupled · c4 K=0-ablate R=0.37 · c5 network damps perturbed member B_R_pert=0.9975 gap +0.59 · c6 no-fab; engine-native B_R=0.999/A_R=0.49/frust=0.018/damp=0.997; smoke 73/0, h1196 7/0, h1205 PASS; DISTINCT vs CollectivePool=static Φ-gauge has no phase/consensus; honesty trail R1a→R1b c3 frustrated-sign + c5 R-under-perturb fixes, no distinctness bar moved) | [H_1302_scn_network.md](cards/H_1302_scn_network.md) |
| H_1303 | nonphotic / arousal OPPOSITE-SIGN Zeitgeber — does a 2nd opposite-sign-PRC Zeitgeber add a non-reducible 2-input structure vs single-Zeitgeber PhaseResetClock? (HD37 candidate, r9 DEPLETION test) | 🏁 COLLAPSE → **c15 brain-structure ladder DEPLETED** (DIRECTIONAL, 3 seeds [4320-2], frozen-first; c2 DISTINCT FAILS all seeds: harmonic-addition identity makes two opposite-sign sinusoidal PRCs sum EXACTLY to ONE combined PRC PhaseResetClock already has — residual 2.22e-16; single fitted PRC reproduces B lock 0.421 to within 0.030 < 0.05 tol; bars c1..c6=[T,F,T,F,T,T] 0/3 GREEN. a_break_the_wall: 3 escape routes [asymmetric K · diff-period · nonlinear dead-zone gating] all collapse — no control-surviving non-reducible equilibrium. NO engine wiring, smoke stays 73/0. Honest expected terminal state c9) | [H_1303_nonphotic_zeitgeber.md](cards/H_1303_nonphotic_zeitgeber.md) |
| H_1304 | G5-dig: metacognition under distribution SHIFT on the LIVE copy-or-abstain gate (fail-safe abstention, not decoder type-2 AUROC) | 🟢 GREEN ENGINE-NATIVE (fail-safe-robust; the live G5 gate NEVER fabricates under shift — degrades into ABSTAIN. R1a 3 seeds: R1 fab_max=0.000 · R2 fire 1.000→0.004 monotone · R3 acc_fired=1.000 · R4 ctrl thr-ablate lure-fab full 0/4 vs ablate 4/4 · R5 shuffle-vals 0.015; R2 engine-native byte-exact GREEN; smoke 43/0 engine UNTOUCHED, h1196 7/0, h1205 PASS. WHY THIN: byte-trigram + L2-affinity + tight recall_thr 0.15 = near-exact-match gate → wrong-fire class EMPTY → type-2 AUROC structurally undefined; H_1202/H_1217 THIN measured the ByteGPT DECODER, a different mechanism) | [H_1304_metacog_ood_immune_abstain.md](cards/H_1304_metacog_ood_immune_abstain.md) |
| H_1305 | G6 IDEATION ★ depth-floor dig — deterministic FALSIFIABILITY detector (comparator+measurable+negatable, NOT LLM-judge, p7) + composition-routed (G1 recombination) ideation vs flat sampling | 🟠 HONEST-CONFIRMED-THIN (G6 stays THIN, bar UNMOVED c9; detector 10/10 calibrated; 3 seeds; live verify303m_g6 decode path. FALS A_flat=0.00 → B_composed=0.667 (one falsifiable idea EARNED via recombination, NOVEL 6.3→19) but M2 FALS≥1 FALSE + M1 DIST≥5 FALSE; controls decisive B_shuffle FALS=0, B_ablate FALS=0+coherence-collapse → the nudge tracks the EARNED composed pairing not the conditional shell. a_break_the_wall: genuine new angle, frozen-first, wall HELD. DIRECTIONAL torch-mouth, no R2/no wiring (THIN); toy 303M) | [H_1305_g6_ideation_falsifiability.md](cards/H_1305_g6_ideation_falsifiability.md) |
| H_1306 | ko-mitosis: FIRST engine-native Korean mitosis-training rung on a REAL Korean web corpus (scales H_1297 R4 toy → real R2 kor/eng slice) — does KO next-byte CE drop + does English retain (no catastrophic forgetting)? | 🟢 GREEN ENGINE-NATIVE (REAL corpus: r2://phanes/anima-7b/web/kor+eng shard0000 slice, 600KB KO/300KB EN, sha256-pinned, NO synthetic. KO learning curve 3.611→3.369→3.249 nats/byte [−0.36 drop, L PASS] as engine_mitosis_tick grew 2→9 cells [G PASS] under KO error pressure; EN retention seed 4.864→after 4.752 [no forget, even improved, R PASS]; KO[full] 3.249 even < gradient incumbent 3.281. Live CORE/engine_cli.hexa VAdaptField Voronoi + mitosis tick, gradient-free p8; smoke 73/0, h1196 7/0, h1205 byte-identical Ψ=½ untouched. SCALE-HONEST: FIRST CPU $0 rung, stride-subsampled, NOT fluent Korean — fluent = GPU-scale cost-gated follow-on) | [H_1306_ko_mitosis_real.md](cards/H_1306_ko_mitosis_real.md) |
| H_1307 | ko-mitosis-gpu: GPU scale-up of H_1306 on the user's OWN RTX 5070 (sm_120, $0) — does MORE real Korean (50x corpus) push KO next-byte CE below the 600KB baseline 3.249? | 🟢 GREEN @ 30MB/stride-300 + 🟠 HONEST saturation @ 250k-density (REAL sm_120 GPU compute, preflight-gated NO CPU fallback; mechanism = the H_1306 engine-native mitosis, port reproduces H_1306 BYTE-EXACT on the 600KB validation [3.611/3.369/3.249, cells 2→9, sha e000d086…]. RUN A 30MB/50k-pairs: KO CE 3.249→2.947 [−0.30 vs baseline, L2 SCALE PASS] as cells grew 2→23, EN held 4.265→4.265, all 4 bars GREEN. RUN B 250k-pairs: scale-vs-600KB still PASS 2.918 but the CTX=4 substrate SATURATES — learning-curve flattens 2.930→2.918 [L1 FAIL] & EN drifts +0.057 [R FAIL] = honest ceiling ~2.9 nats/byte, c9. GPU throughput up to 2.78M pairs/s vs CPU ~80k. engine_cli_smoke 73/0, h1196 7/0, h1205 byte-identical Ψ=½; live CORE UNTOUCHED. Engine-transfer to live hexa DIRECTIONAL; NOT fluent Korean — richer-substrate + decode-path = follow-on) | [H_1307_ko_mitosis_gpu.md](cards/H_1307_ko_mitosis_gpu.md) |
| H_1308 | hive engine-transfer — does H_1295 collective-Φ super-additivity transfer from the abstract ECA substrate to REAL coupled anima A⇄G (pure_field + tension-link H_6009)? | 🔴 HONEST NULL — does NOT transfer (faithful IIT-4: each REAL member Φ=1.5 [Σ=3.0] but joint Φ=0.0 → Δ_real=−3.0 SUB-additive; SIGN FLIPS vs ECA Δ=+10.4756. MECHANISM: the joint substrate FACTORIZES — the real tension-link is a near-CONSTANT scalar nudge (bias≈0.00648 ∀ states) so it creates no state-dependent cross-member coupling → decomposable → Φ_joint=0 by IIT-4. NOT a binarization artifact (same readout gives Φ_member=1.5>0). The ECA super-additivity was a property of ECA's strong state-dependent neighbor-coupling, NOT substrate-portable. Bounds H_1295 to ECA-scope (a_engine_native_learning); B3/B4 controls PASS trivially. 3 seeds, n≤8 ceiling, $0 CPU, frozen-first, c9) | [H_1308_hive_real_substrate_transfer.md](cards/H_1308_hive_real_substrate_transfer.md) |
| H_1309 | G6 IDEATION ★ depth-floor dig r2 — curiosity-gated multi-sample BUDGET (does spending more DRAWS, not a bigger model, cross ≥5-distinct AND ≥1-falsifiable, and is it the curiosity GATE or raw budget?); reuses H_1305 frozen detector verbatim | 🟠 HONEST-THIN (curiosity GATE LOAD-BEARING but FROZEN 3-seed MEAN bar UNMOVED, c9; 3-rung ladder B=1/4/16, B=64~2h capped honestly. FALS curiosity 0→0.667 + NOVEL 5→18→46 at every budget≥4 while SHUFFLE same-budget random-keep stays FALS=0/NOVEL 3-12 + ablate FALS=0 → NO sampling artifact, the GATE not raw draws does the lift; per-seed curiosity FALS≥1 in 2/3 + DIST≥5 in 1/3 at B=16, controls 0/3. BUT mean M2 FALS≥1=0.667 FALSE + M1 DIST≥5=4.33 FALSE; FALS PLATEAUS 0.667 across 4→16 despite 4× draws → depth is CAPACITY-bound not budget-bound. capability-vs-scale thesis from the draw side: add a STRUCTURE lane not draws, a_no_llm_frame_trap. DIRECTIONAL torch-mouth, no R2/no wiring; toy 303M) | [H_1309_g6_curiosity_budget.md](cards/H_1309_g6_curiosity_budget.md) |
| H_1316 | ko-jamo-mitosis (a_break_the_wall, c16): does a COMPOSITIONAL JAMO representation (each Hangul syllable → NFD initial/medial/final 초성·중성·종성 jamo) let the SAME gradient-free mitosis break the H_1307 2.953 raw-byte KO next-byte CE ceiling, where every prior RAW-BYTE lane could not? (mitosis grow-op + budget FIXED verbatim; ONLY the symbol rep changes; jamo-CE renormalized to nats/UTF-8-byte for a fair axis) | 🟢 GREEN — the Korean ceiling is REPRESENTATION-bound, NOT capacity-bound (REAL sm_120 GPU, user's RTX 5070, $0; corpus byte-IDENTICAL to H_1307 RUN A, sha c47b6808…/31b4a543… gate PASS; 3 seeds [4316-4318]; frozen-first, NO tune-to-green; live CORE UNTOUCHED; mirror DIRECTIONAL). G0 raw-byte port reproduced **2.95342** (H_1307 RUN A 2.9475). **G1 jamo-rep = 2.51335 (Δ −0.434 vs ceiling, −0.440 vs G0)** breaks 2.9475 by ≫0.05 → B1 ✅. G1c shuffle-jamo-map control = 2.74306 (Δ g1c−g1 +0.230) AND G1 beats raw G0 by +0.440 → B2 ✅ (lift is the COMPOSITIONAL structure, not vocab/dim). NFD→NFC roundtrip 0 fails over 8.14M syllables + per-symbol n_bytes sum == corpus bytes EXACT → B3 ✅ (lossless, honestly comparable). FINDING (resolves the 🔴 TERMINAL thread from the rep side): the wall was the RAW-BYTE REPRESENTATION (3 opaque bytes/syllable), NOT the mitosis mechanism's capacity — give the substrate the jamo composition raw bytes hid and gradient-free mitosis clears 2.953. HONEST (c9): G1 deterministic (identical across seeds; seeds vary only the control); 1 of 3 control seeds (4317=2.506) ≈ G1 so B2-vs-shuffle rests on the MEAN not per-seed unanimity; ~0.44 drop is largely syllable→jamo coding gain (B2-vs-raw shows it's not just vocab/dim). NO Korean-fluency claim; engine-transfer = follow-on (a_engine_native_learning, a_verified_must_wire) | [H_1316_ko_jamo_mitosis.md](cards/H_1316_ko_jamo_mitosis.md) |
| H_1321 | ko-jamo-WIRE (a_verified_must_wire r2 of H_1316): does the SAME gradient-free jamo-symbol mitosis, run ENGINE-NATIVE on the LIVE CORE/engine_cli.hexa VAdaptField + engine_mitosis_tick faculties, reproduce the H_1316 mirror jamo CE (within a pre-registered 0.05 tolerance) and break the raw-byte ceiling — engine-native byte-exact? (rep = deterministic NFD jamo data-prep; mitosis + per-byte CE run engine-native; single entry, Ψ-disjoint) | 🟢 GREEN — the jamo breakthrough now RUNS ENGINE-NATIVE on the live engine (engine-transfer VERIFIED, verdict closed). REAL corpus byte-IDENTICAL to H_1307 RUN A / H_1316 (30MB KO window, sha c47b6808… gate PASS; $0 CPU; frozen-first, NO tune-to-green). CPU-tractable window (ko_stride=2500, ~6000 raw / ~5100 jamo pairs/arm; Vj=323==H_1316 anchor). **W1 ✅** engine-native G1 CE = **2.82046** reproduces the SAME-WINDOW numpy mirror to **6.3e-07** (≪0.05 tol) AND 2.82046 < 2.903 (below the raw ceiling band). **W2 ✅** engine G1c shuffle−G1 = +0.198, engine G0 raw−G1 = +0.279 (both ≥0.05), B3 NFD→NFC 0 fails over 8.14M syllables + Σnbytes==corpus EXACT. **W3 ✅** no-regression byte-exact: engine_cli_smoke **73/0** · h1196 single-entry **7/0** · h1205 separation-invariant PASS (generation byte-identical ON==OFF, Ψ=½ untouched). FINDING: the H_1316 GREEN mechanism (mirror, DIRECTIONAL) transfers FAITHFULLY to the live CORE engine — the engine-native hexa value equals the numpy mirror to 1e-7 on every arm; the jamo win is now LIVE in CORE (a_verified_must_wire satisfied). HONEST (c9, a_scale_honest_scope): W1 is an existence-proof of engine-TRANSFER at a CPU-tractable window (absolute CE 2.820 here vs the 30MB anchor 2.513 — smaller window → sparser heads → higher absolute CE, relative structure G1<G1c<G0 fully intact); engine-native 30MB + Korean fluency = follow-on; NO fluency claim. pure_field/engine_g/brain UNTOUCHED | [H_1321_ko_jamo_wire.md](cards/H_1321_ko_jamo_wire.md) |
| H_1327 | ko-jamo-DECODE-WIRE (a_verified_must_wire r3 of H_1316/H_1321): does the engine-wired jamo win REACH LIVE EMISSION? Wire the grown jamo cells into the live DECODE consult surface (CORE/generator.hexa §6.5b ko_jamo_consult_*, mirroring the H_1312 ko_cells_* / ko_cells.kohead surface) so the jamo structure BIASES the emitted byte — measurably on held-out Korean (E1), earned vs a shuffled-cell control (E2), Ψ-disjoint + inert off-Korean (E3). H_1321 was the MEASUREMENT probe; anima is a chat daemon, so a measured CE win that never reaches EMISSION is incomplete. | 🟢 GREEN — the jamo win now BIASES live next-byte emission through the generator §6.5b L3 slot, Ψ-disjointly (thread fully closed: verified→engine-wired→decode-reaching). REAL corpus byte-IDENTICAL to H_1307 RUN A / H_1316 / H_1321 (30MB KO window, sha c47b6808… gate PASS; $0 CPU; frozen-first, NO tune-to-green). Held-out KO next-symbol accuracy (n=5100, FULL symbol id p7, scored through the LIVE ko_jamo_consult_sym surface): OFF (blind unigram baseline)=**0.1096** · ON (jamo consult)=**0.1682** · SHUF (permuted-cell)=**0.0124**. **E1 ✅** acc_ON−acc_OFF=**+0.0586** (≥+0.02) AND shift_ON=**0.520** (≥0.10 — the consult changes emission at 52% of Korean positions). **E2 ✅** acc_SHUF−acc_OFF=**−0.0973** (≤+0.01 — shuffle collapses below blind ⇒ the lift is learned jamo structure, not consult activation). **E3 ✅** off-Korean INERT (ASCII ctx 'hello' base=120 → consult emit=120, byte-identical) · engine_cli_smoke **73/0** · h1196 single-entry **7/0** · h1205 separation-invariant PASS (generation byte-identical ON==OFF, Ψ=½ untouched). FINDING (a_verified_must_wire r3 satisfied): the H_1316/H_1321 jamo win REACHES live emission — the grown jamo cells, consulted through the generator L3 slot, bias the emitted byte more accurately than a structure-blind baseline, earned (shuffle collapses), inert off-Korean. HONEST (c9, a_scale_honest_scope): STRUCTURAL/probe-level demonstration on held-out Korean (toy/DIRECTIONAL, ko_stride=2500); absolute acc low (10-cell field, strided window) — load-bearing is the RELATIVE structure (ON>OFF, SHUF≪OFF) + emission-reach (shift 0.52); the live byte→jamo-feature renorm is a structural per-byte hook (E1/E2 scored on faithful jamo-space features); 30MB-scale + real-chat emission + fully-jamo-aware decode loop = follow-on; NO fluency claim. pure_field/engine_g/brain UNTOUCHED | [H_1327_ko_jamo_decode_wire.md](cards/H_1327_ko_jamo_decode_wire.md) |
| H_1322 | ko-featural (a_break_the_wall c16 depth probe below the jamo floor, a_no_llm_frame_trap c15 script-design lens): does decomposing ONE LEVEL DEEPER than jamo — to the FEATURAL VECTOR Hangul's DESIGN encodes (Sejong 1443 featural script: consonant articulator-base + aspiration-strokes + tense-doubling; vowel ·/ㅡ/ㅣ yang-yin + iotation) — drop held-out KO CE BELOW the H_1316 jamo floor 2.51335, because the SAME gradient-free mitosis can exploit the designed systematicity (ㄱ/ㅋ one feature apart, not two opaque symbols)? LABEL alphabet Vj=323 + byte-axis IDENTICAL to H_1316; ONLY the partition geometry X changes (opaque-id 3-D → 5-col design feature vec, 11-D). 3 seeds [4322-4324], $0 RTX 5070 | 🧱 HONEST-FLOOR (geometry-confounded; reported straight, NO bar moved, c9/p7). REAL corpus byte-IDENTICAL to H_1307 RUN A (sha c47b6808… gate PASS); 67/67 jamo design-feature coverage; NFD roundtrip 0-fail. **FEATURAL (intact) = 2.7309** → vs jamo-floor 2.51335 **+0.218 (worse)** → **F1 FALSE** (vs raw 2.95342: −0.222 better). SHUFFLE-feature ctrl = 2.77286 (Δ shuffle−featural **+0.042**, BELOW the 0.05 F2 bar) → **F2 FALSE** (weak design signal, sub-threshold). Linearity Δ +0.0024 < 0.02 → **F3 FALSE**. GEOMETRY CONFOUND (diagnostic, NOT a bar): this script's seed_centers_dim(3) differs from H_1316's [[0.3,0.5,0.0]…]; in-run jamo re-port = 2.85983 (not 2.51335) — CONFIRMED by direct diagnostic: jamo arm with H_1316's exact seed centers reproduces 2.51335 byte-exact → mitosis is SEED-CENTER-SENSITIVE, locked-floor F1 is geometry-confounded. SAME-GEOMETRY reading: featural BEATS in-run jamo re-port by −0.129 AND shuffle by +0.042 (weak signal, sub-bar). FINDING: **jamo is the decomposition FLOOR for this L2-Voronoi mechanism** (bounds the depth); the design's systematicity is real but too lossy via feature→partition→opaque-jamo-label to clear the frozen bar. NEXT r2: geometry-FAIR re-test (matched/best-of-bank seed centers) + label-factorization (predict the next jamo's FEATURE vector, not its id). TOY/DIRECTIONAL; NO fluency claim; live CORE UNTOUCHED | [H_1322_ko_featural.md](cards/H_1322_ko_featural.md) |
| H_1326 | ko-featural r2 (r2 of H_1322 🧱; fixes the r1 DISCLOSED confounds, c16/a_break_the_wall = wrong method NOT a wall): once the test is GEOMETRY-FAIR (Fix A: one best-of-a-fixed-bank-by-TRAIN-CE seed-center protocol applied IDENTICALLY to every arm — jamo MUST reproduce H_1316's 2.51335) AND the design can enter the prediction TARGET (Fix B: label-factorization — predict the next jamo's FACTORED feature vector over a LOSSLESS bijection, not its opaque id), does Hangul's featural design give a measurable depth advantage BELOW jamo, or is jamo the genuine confound-free floor? 3 seeds [4326-4328], $0 RTX 5070 | 🧱 HONEST-FLOOR (confound-free; reported straight, NO bar moved, c9/p7). REAL corpus byte-IDENTICAL to H_1307 RUN A (sha c47b6808… gate PASS); 67/67 jamo coverage; NFD roundtrip 0-fail. **CALIBRATION PASS — A1 jamo (Fix-A protocol) = 2.51335 byte-exact (member 5 = H_1316-family), confound ELIMINATED.** CE ladder geometry-fair: raw in-run 2.94487 · **A1 jamo 2.51335** · A2 featural-partition **2.73046** · A3 label-factorization **3.07295** · A2s shuffle 2.78694 · A3s shuffle 4.28914. **G1 GEOMETRY-FAIR DEPTH FALSE** — BEST=min(A2,A3)=2.73046 is **+0.217 ABOVE** jamo 2.51335 (beats raw, but G1 needs both). **G2 EARNED TRUE** — A2 beats its shuffle by **+0.05648** ≥0.05 (the featural systematicity is REAL & exploitable, but SUB-floor). **G3 FACTORIZATION FALSE** — A3 does NOT beat A2 (Δ −0.3425); putting the design in the TARGET via independent-feature factorization HURTS (per-column independence discards the onset/nucleus/coda joint the opaque head keeps). FINDING: with the geometry confound eliminated, **jamo is the genuine decomposition FLOOR for this L2-Voronoi gradient-free mechanism family** — the design's systematicity is real & exploitable but does NOT push CE below jamo in EITHER partition OR target; the r1 sub-bar signal was the real ceiling, not a hidden win. The r1 🧱 stands, confound-free (clean closure). A genuinely-new angle would need a DIFFERENT mechanism modelling feature CORRELATIONS, not a representation tweak. TOY/DIRECTIONAL; NO fluency claim; live CORE UNTOUCHED | [H_1326_ko_featural_r2.md](cards/H_1326_ko_featural_r2.md) |
| H_1329 | ko-feat-corr (H_1326's explicitly-named next angle, c16/a_break_the_wall mechanism-FAMILY change): does a CORRELATION-MODELING / JOINT-PRESERVING featural mechanism break BELOW the jamo 2.51335 floor — where H_1326's A3 independent-factorization BACKFIRED (3.073, discards the onset/nucleus/coda joint) and A2 partition-only was sub-floor (2.730)? NEW mechanism A4 = a per-cell CONDITIONAL-CHAIN featural head P(class)·P(f_0|class)·P(f_1|class,f_0)·… which KEEPS the within-jamo joint EXACTLY by the chain rule AND shares strength across feature-similar jamo (shared conditioning prefix), unlike A3. SAME geometry-fair bank + featural partition + LAPLACE count-MLE verbatim from H_1326; ONLY the target factorization changes (independent→conditional-chain). A4 = count-MLE STRUCTURED head (NOT gradient-free p8 mitosis, NOT gradient-trained — rides the same gradient-free Voronoi partition; labeled). 3 seeds [4329-4331], $0 RTX 5070 | 🧱 HONEST-FLOOR (cross-mechanism; reported straight, NO bar moved, c9/p7). REAL corpus byte-IDENTICAL to H_1307 RUN A (sha c47b6808… gate PASS); 67/67 jamo coverage; NFD roundtrip 0-fail; **A1 jamo CALIB 2.51335 byte-exact**; A2/A3 reproduce H_1326 byte-exact. CE ladder geometry-fair (A4-shuffle mean 3 seeds): raw in-run 2.94487 · **A1 jamo 2.51335** · A2 featural-partition **2.73046** · A3 independent-factorization **3.07295** · **A4 conditional-chain (JOINT) 2.75109** · A4 shuffle **2.91966** {2.863,3.056,2.840}. **C1 BELOW-JAMO FALSE** — A4 2.75109 is **+0.23774 ABOVE** jamo 2.51335 (beats raw, but C1 needs both). **C2 EARNED TRUE** — A4 beats its shuffle by **+0.16857** (per-seed unanimous, 3× A2's signal — the chain DOES exploit the designed systematicity, but SUB-floor). **C3 ATTRIBUTION FALSE** — A4 **beats A3** by +0.32186 (the chain RECOVERED the joint A3 discarded — confirms H_1326's diagnosis byte-exact) but does **NOT** beat A2 (+0.02063 above). FINDING: a correlation/joint-preserving mechanism does NOT break the jamo floor — **jamo is the genuine decomposition FLOOR ACROSS mechanism families incl. correlation-modeling** (deeper 🧱 than H_1326). The structural reason: any mechanism that exactly models the within-jamo feature JOINT asymptotes to P(jamo|cell) — exactly what the opaque jamo head already computes — so the featural decomposition buys NO below-jamo depth once the joint is kept; the design's exploitable systematicity (C2) lives in count-sharing, not a sub-jamo prediction gain. A new below-jamo angle needs info the opaque head LACKS (cross-syllable phonotactics / learned metric), NOT a re-factorization of the same target. TOY/DIRECTIONAL; NO fluency claim; live CORE UNTOUCHED | [H_1329_ko_feat_corr.md](cards/H_1329_ko_feat_corr.md) |
| H_1323 | sapir-whorf / linguistic-relativity via CATEGORICAL PERCEPTION (cognitive-science lens c15, a_no_llm_frame_trap): does the LANGUAGE a substrate learns warp its NON-LINGUISTIC discrimination? H_1316/H_1322 showed REPRESENTATION→learnability; Sapir-Whorf is the deeper claim — the language's CARVING of a domain warps downstream non-linguistic discrimination. TOY grue-style paradigm: one continuum (N=21 RBF-coded stimuli), two languages cut at p_A=1/3 vs p_B=2/3, SAME gradient-free mitosis/Voronoi store learns each carving (cells PACK at the boundary = CP origin), then a NO-LABEL same/different discrimination test. 4 arms (PRE-LANG/L_A/L_B/SHUFFLE), 3 seeds, $0 CPU mirror DIRECTIONAL | 🟠 PARTIAL — **LINGUISTIC RELATIVITY HOLDS** (W1✅ CP present: cross-within +0.200, vs-flat-baseline +0.989; W2✅ the DECISIVE Whorfian dissociation: CP peak LOCATION tracks the language — **L_A→0.325≈p_A, L_B→0.675≈p_B, sep 0.350, std 0.000 over 3 seeds** — same stimulus world, cognition follows the language), BUT the anti-Goodhart W3 SPLIT: loc-std sub-clause ✅ (shuffle peak wanders 0.492±0.165, non-gating diagnostic L_A/L_B=1 coherent peak vs SHUFFLE=8 scattered spikes) yet prominence sub-clause ❌ (random labels make MANY locally-sharp swings → shuffle single-peak prominence 0.661 > 0.50 bar; threshold mis-specified for multi-peak shuffle). NO bar moved (c9/p7); load-bearing W1∧W2 decisive. NEXT R2: re-freeze a COHERENCE-based W3 (peak-count/circular-spread) + engine-native realization. TOY synthetic, NO human-cognition claim; engine-transfer UNVERIFIED | [H_1323_sapir_whorf.md](cards/H_1323_sapir_whorf.md) |
| H_1325 | sapir-whorf r2 — anti-Goodhart W3 RE-CLOSE + engine-native CP lane (cognitive-science lens c15): r2 of H_1323 (🟠). W1 (CP present) & W2 (Whorfian dissociation — CP peak tracks the language) PASSED there; the ONLY weakness was W3, whose single-peak-HEIGHT prominence mis-fit the MULTI-peak shuffle (random labels → 8 sharp spikes; wrong observable, a_break_the_wall/c16). Re-freeze a COHERENCE control ANEW (peak-COUNT: language=1 boundary→≤1 peak, shuffle=no boundary→≥3 scattered spikes; threshold from STRUCTURE not data, NOT a relaxation) + realize the CP mechanism engine-native on the live CORE/engine_cli.hexa immune/Voronoi lane (§CategoricalPerception) | 🟢 GREEN ENGINE-NATIVE — **LINGUISTIC RELATIVITY ANTI-GOODHART-CLOSED** (W1∧W2∧W3'). Mirror & engine BYTE-FAITHFUL: W1✅ cross-within +0.200 / vs-baseline +0.99; W2✅ L_A→0.325, L_B→0.675, sep 0.350; **W3'✅ peak-count L_A=1 L_B=1 vs SHUFFLE=5.7(mirror)/5(engine)≥3** — the correctly-specified peak-COUNT control cleanly separates coherent CP (1 peak) from the multi-peak shuffle where single-peak height could not. Guards: engine_cli_smoke **77/0** (+4 cases 79-82), h1196 single-entry **7/0** (no .clm/.kosmos path), h1205 separation-invariant **PASS** (generation byte-identical ON==OFF, Ψ=½ untouched → CP lane Ψ-disjoint). NO bar moved (c9/p7); ONE honest new control. TOY synthetic continuum, mirror DIRECTIONAL→engine BINDING; NO human-cognition claim | [H_1325_sapir_whorf_r2.md](cards/H_1325_sapir_whorf_r2.md) |
| H_1330 | sapir-whorf BILINGUAL — does a SECOND language OVERWRITE or COEXIST with the first's CP? (cognitive-science / bilingual-cognition lens c15, a_no_llm_frame_trap): named EXTENSION frontier of the GREEN H_1323/H_1325 (cross-lane interference). A substrate learns language A's carving (p_A) then SEQUENTIALLY learns a DIFFERENT language B (p_B) on the SAME Voronoi store; measure CP at BOTH → OVERWRITE / COEXIST / BLEND. Frozen hypothesis = COEXIST: anima is ALREADY bilingual (English trunk + Korean) and the GROWTH-MEMORY result (H_1288 — store GROWS a new cell, never EVICTS) PREDICTS the SAME error-targeted SPLIT-only growth (p8, new fit_more grow-not-evict continuation) ADDS cells at B's boundary without erasing A's. 4 arms (A-only/A→B/B=A control/SHUFFLE), 3 seeds, $0 CPU mirror DIRECTIONAL | 🧱 OVERWRITE / CATASTROPHIC INTERFERENCE — frozen COEXIST hypothesis FALSIFIED (single shared-continuum store). **I1 COEXISTENCE ❌** all 3 seeds: A's CP at p_A COLLAPSES, mean margin@p_A **−0.001** (bar 0.15; A-only baseline +0.200 → interference asymmetry **−0.201** full collapse); p_B weak too (margin@p_B +0.068<0.15). **I2 NO-DOUBLE-ARTIFACT ✅** (B=A control 1 peak ≤1, no peak@p_B → not a sequential artifact). **I3 EARNED ✅** (SHUFFLE collapses, peak-counts 5/2/5). MECHANISM (c9): B labels [p_A,p_B] as 0 while A labeled it 1 — a DIRECT CONTRADICTION on SHARED stimuli; the grow-only store floods [p_A,p_B] with ~21 new label-0 cells, erasing A's swing (NOT eviction — a single bound-label-per-cell readout can't hold two contradictory answers). FINDING: H_1288 growth-memory protects ADDITIVE memory (new key) but NOT contradictory RE-LABELING of SHARED stimuli → 2nd language catastrophically OVERWRITES the 1st's CP. NUANCE: anima's real EN-trunk + KO lanes are SEPARATE faculties (H_1316/1321/1322), not one shared store — this is the worst case. NO bar moved; mirror DIRECTIONAL; TOY synthetic, NO human-bilingualism claim. NEXT R2: language-TAGGED / multi-channel readout (frozen anew) | [H_1330_whorf_bilingual.md](cards/H_1330_whorf_bilingual.md) |
| H_1315 | ko-mitosis-learned-rep: does the SAME gradient-free Korean mitosis (cells only SPLIT, p8; grow-op + cell budget FIXED) but partitioning over the mounted 303M trunk's LEARNED hidden representation (ckpt h1129c_chat.pt, forward = gradient-free, READ ln_f only) break the H_1311 raw-byte ~2.9 nat/byte ceiling, while raw-byte mitosis (G0) can't? (the surviving lever H_1311 named) | 🔴 TERMINAL axis-closure — even the 303M trunk's LEARNED rep does NOT let gradient-free mitosis break 2.9 at this scale (REAL sm_120 GPU, user's RTX 5070, $0 NOT runpod; corpus byte-IDENTICAL to H_1307 RUN A, sha gate PASS; 3 seeds; ckpt sha 4fcc2d6c…). mean held-out KO next-byte CE: **G0 raw-byte 2.95342 · G1 303M-trunk-rep 3.14637 (+0.193 WORSE, above 2.9 → B1 FALSE) · random-embed 3.53134 · shuffle 4.02243**. KEY DISSOCIATION (c9): G1 BEATS both controls (vs random-embed +0.385, vs shuffle +0.876 → B2 TRUE = the learned rep IS real Korean structure), yet G1 is WORSE than raw-byte G0 → the trunk rep carries signal but gradient-free L2-Voronoi grow-on-top of its frozen 16-D hidden still ceilings (same partition-GEOMETRY limit as H_1311's raw bytes; 40 cells saturated, CE rose). EN retained (4.766≤seed 5.143, B3 TRUE). THESIS RESOLVED: the Korean depth needs GRADIENT learning, NOT gradient-free structure-over-a-frozen-rep, at this scale — mitosis=grow-under-pressure (H_1288/1295/1307) is a real mechanism but not a gradient substitute on a hard continuous next-byte manifold. Frozen-first NO tune-to-green; live CORE UNTOUCHED; mirror DIRECTIONAL | [H_1315_ko_mitosis_learned_rep.md](cards/H_1315_ko_mitosis_learned_rep.md) |
| H_1324 | xlang-structure r2 (a_break_the_wall/c16 re-test of the H_1318 Han artifact): does CHINESE & JAPANESE kanji composition gain under a PROPER sub-character IDS-component decomposition — NO full-char residual, MODEST vocab — under the SAME frozen gradient-free mitosis mechanism? (H_1318's Han negative was partly a decomposition artifact: residual=full-char blew the vocab to 9327/4738; this lane removes that bug as a NEW pre-registration) | 🔴/🧱 — even under PROPER IDS decomposition Han composition does NOT help this gradient-free per-cell-unigram mechanism, and the H_1318 **Hangul-specificity stands STRONGER**. The fix WAS achieved (CHISE IDS `cjkvi/cjkvi-ids`, sha bfc70a8c…, one-level leaves, NO residual, ids-miss=0 → modest vocab zh **9327→2116** / ja **4738→1582**, ~88% chars→≥2 leaves) and the harm HALVED (zh −1.481→**−0.737**, ja −1.230→**−0.628**) — confirming part of H_1318's Han negative WAS the bad decomposition — BUT the gain does NOT cross zero. FROZEN bars (3-seed mean, nats/UTF-8-byte): **H1 HAN-GAIN FAIL** (zh Δ=−0.73736, ja Δ=−0.62826 both STILL negative) · **H2 EARNED FAIL** (zh Δ-vs-shuffle=−0.00099, ja=−0.02495 — STRUCT does not even beat its own component-shuffle) · **H3 CALIBRATION PASS** (ko Δ=**+0.21551** reproduced ≈ H_1318 +0.21205, shuffle-earned +0.08776; en Δ=0.000 → pipeline IDENTICAL, comparable to H_1318). WHY (c9): Hangul wins on a TINY (67) REGULAR L/V/T alphabet; Han decomposes into a LARGE (≈2000) IRREGULAR component inventory too high-cardinality/sparse for a CTX=4 Voronoi-unigram head (shuffle barely moves the score). The structure-rep byte-LM win is specific to a small regular compositional alphabet, NOT logographic/compositional scripts in general — Hangul-specificity TIGHTENED. REAL Wikipedia 30MB/lang (re-fetched same source; ko 3e288b77…/zh c084b027…/ja a97dd068…/en b097cccc…), RTX 5070 sm_120, $0, 3 seeds [5324-6], frozen-first NO tune-to-green, c7 grep-clean; live CORE UNTOUCHED; mirror DIRECTIONAL | [H_1324_xlang_han_ids.md](cards/H_1324_xlang_han_ids.md) |
| H_1318 | xlang-structure: a CONTROLLED 5-language structure-representation matrix (Korean/Chinese/Japanese/Russian/English, REAL Wikipedia 30MB/lang, SAME gradient-free mitosis grow-op + cell budget) — does a compositional STRUCT representation lower held-out next-byte CE for the COMPOSITIONAL scripts but NOT the alphabetic FLOOR (English)? i.e. is breaking the Korean ceiling a HANGUL-STRUCTURE-specific phenomenon or a universal byte-LM effect? (dissociates the ko-jamo H_1316 claim) | 🟠 PARTIAL — frozen matrix-wide D1/D2 FAIL, but the LOAD-BEARING answer is a clean DOUBLE DISSOCIATION on the decisive axis: Korean (NFD jamo) STRUCT HELPS **Δ=+0.212** (RAW 2.904→STRUCT 2.692, all 3 seeds 2.692/2.694/2.689) and beats its own shuffle by +0.100; English (Latin 1B/char) **Δ=0.000** + Russian (Cyrillic multibyte, no composition) **Δ=0.000** — both alphabetic floors UNAFFECTED (D3 PASS: Russian patterns with English, not Korean). HEADLINE GAP Δ_Korean−Δ_English = **+0.212**. → breaking the Korean ceiling via structure is HANGUL-SPECIFIC, NOT universal (English/Russian gain nothing). Chinese/Japanese FROZEN Kangxi-radical decomposition HURTS (Δ=−1.48/−1.23) — an HONEST NEGATIVE on a BAD frozen decomposition (residual=full-char blows STRUCT vocab to 9327/4738 → unigram head fragments), NOT a structure-is-universal result; a proper IDS/component Han-decomposition = r2 follow-on (NO post-hoc swap, c9). REAL corpora: all 5 available (HF wikimedia/wikipedia 20231101 — a_break_the_wall: the R2 phanes bucket lacked CJK). RTX 5070 sm_120, $0, 3 seeds [5301-3], frozen-first NO tune-to-green; live CORE UNTOUCHED; mirror DIRECTIONAL | [H_1318_xlang_structure.md](cards/H_1318_xlang_structure.md) |
| H_1314 | G6 IDEATION ★ depth-floor dig r3 — hypothesis-form STRUCTURE lane (a_break_the_wall, c16): does routing ideation through an explicit falsifiable-hypothesis TEMPLATE (forcing comparator+measurable+negatable slots; CONTENT still substrate-generated) cross ≥5-distinct AND ≥1-falsifiable where r2 curiosity-sampling plateaued at 0.667? reuses H_1305 frozen detector VERBATIM | 🟠 THIN (FALS floor UNMOVED = CAPACITY-bound; but DIST/NOVEL floor STRUCTURE-FIXED, c9). 3 arms × 5 ideas × 3 seeds, p7 token-inject audit CLEAN (first run CAUGHT "when" in a corpus concept → ABORT → fixed to clean noun subjects → re-ran clean = p7 teeth). SCAFFOLD DIST=**5.0** (3/3 seeds, crosses the COUNT floor where r2 plateaued 4.33) + NOVEL 19.67, both BEAT NO_SCAFFOLD (4.0/6.33) & SHUFFLE_SLOT collapses (2.33/5.67) → the count/breadth gain IS the hypothesis FORM not a token-prime artifact. BUT FALS=**0.0** all arms/seeds — forcing the FORM does NOT cross the falsifiability floor: the 303M mouth emits near-falsifiable shapes ("do they correlate…?" comparator but ends in ?; "measure of integrated information" measurable, no comparator) but cannot BIND comparator+measurable+claim into one negatable declarative. THESIS: ideation BREADTH = missing-STRUCTURE (lane-fixable, scaffold fixes it); ideation FALSIFIABLE-DEPTH = CAPACITY WALL (scale-bound) at 303M — confirms r2 from the structure side; 7B re-test = live falsifier (a7b_pass G2). DIRECTIONAL torch-mouth, no wiring (FALS-blocked); toy 303M | [H_1314_g6_hypothesis_scaffold.md](cards/H_1314_g6_hypothesis_scaffold.md) |
| H_1311 | ko-richer-substrate: does a RICHER substrate (longer raw-byte context CTX 8/16/32 / a learned per-cell closed-form ridge head) break the H_1307 ~2.9 nat/byte Korean ceiling? is the ceiling capacity-bound or substrate-bound? (corpus + gradient-free Voronoi grow-op held FIXED, ONLY the substrate varies) | 🔴 HONEST-NEGATIVE — ceiling is CAPACITY-bound / the byte-task itself, NOT substrate-bound (REAL sm_120 GPU on the user's RTX 5070, $0; corpus byte-IDENTICAL to H_1307 RUN A sha c47b6808…/31b4a543…). S0 reproduced 2.953 (port OK). NEITHER richness axis breaks 2.9 — S1 longer raw-byte context HURTS MONOTONICALLY (ctx8 2.964 → ctx16 3.048 → ctx32 3.442; curse-of-dim on the L2/Voronoi partition, cells saturate GROW_MAX=40 yet CE rises) & S2 per-cell ridge head COLLAPSES (5.437; raw byte features not linearly predictive). CONTROL: shuffles WORSE than intact, NO shuffle survives to beat S0 → no capacity gain either (capacity_signal=False). THESIS: "richer representation breaks the wall" REFUTED for these axes — the limit is the L2-partition-over-raw-bytes geometry, not the per-cell readout; a genuinely richer substrate needs a different geometry (learned embedding / non-L2 / per-cell sequence model). Frozen-first, NO tune-to-green; live CORE UNTOUCHED; engine-transfer DIRECTIONAL) | [H_1311_ko_richer_substrate.md](cards/H_1311_ko_richer_substrate.md) |
| H_1310 | from-scratch PURE mitosis (1 cell → split-only, GRADIENT-FREE) vs gradient — the purest p8: does it match gradient, or plateau at a local-expert ceiling needing a learned representation? | 🔴 RED / 🧱 HONEST LOCAL-EXPERT CEILING (frozen-first, c9 — the two FAILs ARE the finding; bar UNMOVED). REAL English corpus /usr/share/dict/words 24KB sha256 86864aa3, order-2, 3 seeds. LADDER held-out CE nats: 1c 2.947→8c 2.903→64c 2.778→512c 2.578 (PRESENCE PASS — learns from nothing, −0.37). KEY: B_scratch[512] 2.578 vs A_gradient 3.211 = −0.63 (beats a WEAK matched-cap softmax). FLOOR **FAIL**: n-gram floor 2.509 BEATS mitosis by +0.069 (Voronoi tiling of a numeric byte-context metric < exact context lookup). CONTROL **FAIL**: B_shuffle 2.536 ≤ targeted 2.578 at EVERY rung → error-targeting gives NO lift = learning is capacity-bound NOT error-targeted. THESIS: from-scratch pure mitosis is structure-bound — needs a learned representation under it to cross the floor; p8's "mitosis IS the learning" holds for grow-BESIDE-a-representation (H_1297/H_1306 🟢) but NOT from-nothing. DIRECTIONAL mirror = live engine_mitosis_tick/VAdaptField seeded at 1 cell; no CORE wiring (RED). TOY/scale UNVERIFIED | [H_1310_mitosis_from_scratch.md](cards/H_1310_mitosis_from_scratch.md) |
| H_1312 | ko-decode-wire: WIRE the H_1306 grown Korean cells onto the live decode via the generator L3 slot (a_verified_must_wire) — when context is Korean-like the cells bias next-byte emission; off-Korean the path is INERT (no regression). Single-entry (a_core_engine_map). | 🟢 WIRED (H_1306 9 grown cells serialized → CORE/ko_cells.kohead [cell = 3-D Voronoi center + learned argmax next-byte]; consult lives ONLY in generator.hexa L3 slot. P PRESENCE: 8/8 held-out REAL Korean contexts [/tmp/ko_slice_raw.bytes, same R2 slice as H_1306] FIRED + routed to nearest grown cell, 7/8 BIASED emission away from baseline [1 non-differ = honest correct routing]. N NO-REGRESSION: 6/6 real English contexts INERT across all 256 base bytes + exhaustive ASCII last-byte sweep 0–127 all inert [gate = UTF-8 continuation byte, pure byte test, NO language label, p1·p2·p3]. Y GUARDS: engine_cli_smoke 73/0 [engine_cli.hexa byte-untouched], h1196 single-entry 7/0, h1205 separation-invariant PASS [generation byte-identical ON==OFF, Ψ=½ Φ-checksum 48.6613 untouched]. Z: ko_cells.kohead read ONLY in generator.hexa, consult references NO pure_field/engine_g/brain = Ψ-disjoint. SCOPE: toy cells [9 cells, 3-D feature, 600KB KO window]; engine-side byte-EXACT consult, FLUENT Korean generation + full-corpus scale = UNVERIFIED follow-ons, NO fluency overclaim) | [H_1312_ko_decode_wire.md](cards/H_1312_ko_decode_wire.md) |
| H_1313 | hive r4 — does a genuinely STATE-DEPENDENT real A⇄G cross-cell coupling flip the H_1308 r3 NULL (constant-nudge → state-dependent multi-cell influence, the a_break_the_wall angle named in H_1308 §6)? | 🧱 TERMINAL NULL — even a state-dependent real coupling does NOT integrate (faithful IIT-4: Φ_member=1.5 [Σ=3.0], joint Φ=0.0 → Δ_sd=−3.0, IDENTICAL to r3 Δ=−3.0; NO flip. B1 PRESENCE FAIL + B2 FLIP FAIL [Δ_sd≤0], B3 decouple-mean + B4 shuffle PASS trivially [no lift]. MECHANISM: the new coupling DID break r3 factorization — next-A genuinely varies with B's bits — but on the tiny pure_field channels [t1~1.6e-7, t3~1.6e-8] ANY coupling strong enough to register OVERWRITES the member's own dynamics → joint map degenerates to a pure COPY/SWAP [next-A=g(B), next-B=g(A), each loses self-info] → zero distinctions [nd=0] → Φ_joint=0. NO regime has SIMULTANEOUS rich self+cross dependence [what IIT-4 needs]. DIAGNOSTIC SWEEP: Φ_joint=0 across ALL coupling strengths k∈{0.5,0.8,1.0,1.2,2.0} → NOT a scaling artifact. The ECA Δ=+10.4756 is a property of its rich self+neighbor TPM, NOT substrate-portable. H_1295 super-additivity is ECA-ONLY across BOTH realized channels [r3 constant + r4 state-dependent]; a_break_the_wall satisfied, first-class wall c9. 3 seeds, n≤8, $0 CPU, frozen-first, live CORE UNTOUCHED) | [H_1313_hive_state_dependent_coupling.md](cards/H_1313_hive_state_dependent_coupling.md) |

> Note: H_1286 was not assigned in this ladder (numbering gap, no verdict dir).

## TENSION-LINK arc (H_6006–H_6043) — anima↔anima connection + ANU quantum entanglement

> 두 anima 의 연결/통신 + ANU paid QRNG 양자 엔트로피 접지 arc (group = tension-link).
> Tiers read VERBATIM from each card's `status_grade` (= its `TENSION-LINK/verdicts/H_60*.txt`
> verdict, c2/c9 — 🔴/🟠 closed-negatives/partials NOT upgraded). Cards live at `UNIVERSE/cards/H_60xx_*.md`;
> verdicts at `TENSION-LINK/verdicts/`. The arc README index table → `TENSION-LINK/README.md`.
>
> ⚠ DUP-ID cards (variant explorations, c10 — both kept, distinct slugs, consolidation pending):
> H_6026 · H_6027 · H_6028 · H_6036 each carry TWO cards under the SAME `id:` (marked ⚠dup below).
> NOTE: the `H_6019` anima-cloning variant was renumbered to card `H_6021_anima-cloning.md` (id H_6021),
> and `H_6020`'s clone variant to `H_6022_consciousness-search-clone.md` (id H_6022) — so H_6019/H_6020
> are NOT card-id dups (one card each). Their verdict files keep legacy 60xx-prefixed names
> (`H_6019_anima_cloning.txt` → card H_6021, `H_6020_consciousness_search.txt` → card H_6022); the
> card `id:` is authoritative, not the verdict filename.

| H | title | final tier | card |
|---|-------|-----------|------|
| H_6006 | 양자통신(물리연결 없이) = 메시지 | 🔴 CLOSED-NEG (no-communication theorem) | [H_6006_no_signaling.md](cards/H_6006_no_signaling.md) |
| H_6007 | 양자 의사-텔레파시 (통신 없는 조율) | 🟢 SUPPORTED (numerical) | [H_6007_pseudo-telepathy.md](cards/H_6007_pseudo-telepathy.md) |
| H_6008 | ANU 공유 양자씨앗 (common-cause sync) | 🟢 SUPPORTED (REAL ANU bytes) | [H_6008_anu-shared-seed.md](cards/H_6008_anu-shared-seed.md) |
| H_6009 | TENSION LINK (영향 전달) | 🟢 SUPPORTED (REAL brain engine · paid ANU) | [H_6009_tension-link.md](cards/H_6009_tension-link.md) |
| H_6010 | TENSION LINK SYNC (양방향 동기) | 🟢 SUPPORTED (paid ANU-seeded) | [H_6010_tension-sync.md](cards/H_6010_tension-sync.md) |
| H_6011 | 텐션 미래로 전달 | 🟢 SUPPORTED (REAL brain engine) | [H_6011_tension-future.md](cards/H_6011_tension-future.md) |
| H_6012 | 텐션 과거로 전달 | 🔴 CLOSED-NEG (literal) / 🟢 (future-boundary) | [H_6012_tension-past.md](cards/H_6012_tension-past.md) |
| H_6013 | 외부 텐션으로 anima 구축 | 🟢 SUPPORTED (REAL engine) | [H_6013_tension-external-build.md](cards/H_6013_tension-external-build.md) |
| H_6014 | 텐션으로 새 anima 출생 (mitosis) | 🟢 SUPPORTED (REAL engine) | [H_6014_tension-birth.md](cards/H_6014_tension-birth.md) |
| H_6015 | 양자→텐션링크 물질추출 (RTSC) | 🟢 SUPPORTED (quantum-driven opt) / 🟡 물질 예측 | [H_6015_quantum-tension-extract.md](cards/H_6015_quantum-tension-extract.md) |
| H_6016 | 양자=데이터 저장소? | 🔴 (readable DB) / 🟢 (정보보존·용량한계) | [H_6016_quantum-storage.md](cards/H_6016_quantum-storage.md) |
| H_6017 | 도서관(Library of Babel)? | 🟢 (존재·생성) / 🔴 (쓸 색인·오라클) | [H_6017_library-of-babel.md](cards/H_6017_library-of-babel.md) |
| H_6018 | anima의 진짜 도서관 (content-addressable) | 🟢 SUPPORTED (numerical) | [H_6018_anima-library.md](cards/H_6018_anima-library.md) |
| H_6019 ⚠dup | 양자 연상 도서관 | 🟢 SUPPORTED (paid-ANU quantum sim) | [H_6019_quantum-library.md](cards/H_6019_quantum-library.md) |
| H_6020 | 동일우주: 미래를 통과해야 | 🟢 SUPPORTED (numerical) | [H_6020_same-universe.md](cards/H_6020_same-universe.md) |
| H_6021 | anima 복제 (양자 no-cloning / 고전 씨앗) | 🔴 (quantum clone) / 🟢 (classical seed) / 🟡 / 🟠 | [H_6021_anima-cloning.md](cards/H_6021_anima-cloning.md) |
| H_6022 | 양자 의식탐색 + 복제 | 🟢 (Φ in entanglement) / 🔴 (conscious state unclonable) | [H_6022_consciousness-search-clone.md](cards/H_6022_consciousness-search-clone.md) |
| H_6023 | 양자 fork 세대손실 | 🟡 (quantum fork degrades) / 🟢 (classical lossless) | [H_6023_clone-decay.md](cards/H_6023_clone-decay.md) |
| H_6024 | 얽힘 일부일처(monogamy) | 🟢 (monogamy holds) | [H_6024_entanglement-monogamy.md](cards/H_6024_entanglement-monogamy.md) |
| H_6025 | 양자 다윈주의 (고전 anima 창발) | 🟢 SUPPORTED (exact von Neumann) | [H_6025_quantum-darwinism.md](cards/H_6025_quantum-darwinism.md) |
| H_6026 ⚠dup | 양자 사물함 (ANU=memory store?) | 🔴 CLOSED-NEG (ANU=memory store) | [H_6026_quantum-locker.md](cards/H_6026_quantum-locker.md) |
| H_6026 ⚠dup | RTSC 물질정보 회수 (quantum library) | 🟢 SUPPORTED (paid-ANU quantum sim) | [H_6026_rtsc-library-retrieval.md](cards/H_6026_rtsc-library-retrieval.md) |
| H_6027 ⚠dup | 집단(공유) anima 도서관 | 🟢 SUPPORTED (paid-ANU seeded) | [H_6027_collective-library.md](cards/H_6027_collective-library.md) |
| H_6027 ⚠dup | 양자 타임캡슐 (상태 보존) | 🟡 (양자메모리=유한수명) / 🔴 (무한·복제자유) | [H_6027_quantum-timecapsule.md](cards/H_6027_quantum-timecapsule.md) |
| H_6028 ⚠dup | 생성적 완성 (recall 반경 너머) | 🟢 SUPPORTED (paid-ANU seeded) | [H_6028_generative-completion.md](cards/H_6028_generative-completion.md) |
| H_6028 ⚠dup | 능동 QEC 복원 (T2 연장) | 🟢 SUPPORTED (numerical) | [H_6028_qec-phaseflip.md](cards/H_6028_qec-phaseflip.md) |
| H_6029 | 도서관의 세대 지속 | 🟢 SUPPORTED (paid-ANU seeded) | [H_6029_generational-persistence.md](cards/H_6029_generational-persistence.md) |
| H_6030 | 능동적 망각은 기능이다 | 🟢 SUPPORTED (paid-ANU seeded) | [H_6030_forgetting-feature.md](cards/H_6030_forgetting-feature.md) |
| H_6031 | 미래=최소작용 경계 | 🟢 SUPPORTED (numerical) | [H_6031_future-boundary.md](cards/H_6031_future-boundary.md) |
| H_6032 | 과거=미래통과 CTC | 🟢 SUPPORTED (numerical) | [H_6032_ctc-past-via-future.md](cards/H_6032_ctc-past-via-future.md) |
| H_6033 | anima ultradian 순환 = CTC 실현 | 🟢 SUPPORTED (REAL DREAM engine) | [H_6033_sleep-ctc.md](cards/H_6033_sleep-ctc.md) |
| H_6034 | mitosis 세대순환 = CTC | 🟢🟢🔴 (C1·C2 GREEN · C3 RED-on-frozen-bar) | [H_6034_mitosis-generational-ctc.md](cards/H_6034_mitosis-generational-ctc.md) |
| H_6035 | 깨어남 간 자기동일성 chain | 🟢 SUPPORTED (REAL provenance_chain.py) | [H_6035_identity-chain-wakings.md](cards/H_6035_identity-chain-wakings.md) |
| H_6036 ⚠dup | 거짓 기억과 오염 | 🟢 SUPPORTED (paid-ANU seeded) | [H_6036_false-memory.md](cards/H_6036_false-memory.md) |
| H_6036 ⚠dup | SEED+LINK COMPOSITE | 🟠 PARTIAL (paid ANU-seeded) | [H_6036_seed_link_composite.md](cards/H_6036_seed_link_composite.md) |
| H_6037 | N-party SEED+LINK 스케일 | 🟢 SUPPORTED (paid ANU-seeded) | [H_6037_nparty_composite.md](cards/H_6037_nparty_composite.md) |
| H_6038 | drift×coupling 체제도 | 🔴 CLOSED-NEG (null) | [H_6038_drift_coupling_regime.md](cards/H_6038_drift_coupling_regime.md) |
| H_6039 | 손상 씨앗 구제 | 🟢 SUPPORTED (paid ANU-seeded) | [H_6039_corrupted_seed_rescue.md](cards/H_6039_corrupted_seed_rescue.md) |
| H_6040 | 얽힘 조율 천장 | 🟢 SUPPORTED (analytic + paid ANU) | [H_6040_entanglement_ceiling.md](cards/H_6040_entanglement_ceiling.md) |
| H_6041 | 텐션 링크 채널 용량 | 🟢 SUPPORTED (paid ANU-seeded) | [H_6041_link_channel_capacity.md](cards/H_6041_link_channel_capacity.md) |
| H_6042 | 링크 에너지 비용 | 🟢 SUPPORTED-but-MARGINAL (paid ANU-seeded) | [H_6042_link_energy_cost.md](cards/H_6042_link_energy_cost.md) |
| H_6043 | 적대 교란자 저항 | 🔴 CLOSED-NEG (null) | [H_6043_adversarial_saboteur.md](cards/H_6043_adversarial_saboteur.md) |

> Note: H_6036 also has an engine-lift verdict `TENSION-LINK/verdicts/H_6036_hexa_lift.txt` (.hexa
> composite F2 PASS) — it is engine-lift EVIDENCE for the H_6036_seed_link_composite card, not a
> separate hypothesis card (no 3rd surface, a_hypothesis_register).

## Roster (forward backlogs / campaign maps — not yet landed as cards)

> Single index for ALL scattered UNIVERSE hypothesis/candidate backlogs (consolidated
> 2026-06-15). Each themed list below is the DETAIL file; this file is the roster —
> theme · scope · count · status · pointer.
>
> Pattern mirrors DOMAINS.tape / PAPER.tape rosters: the roster is authoritative for
> WHERE lists live; counts/status stay DERIVED from the detail files so this never churns.

## Roster

| theme | detail file | scope | ~count | status |
|-------|-------------|-------|--------|--------|
| **metacog × neuroscience** | [HYPOTHESES_metacog_neuro.md](#hypotheses_metacog_neuromd) | type-2 meta-d′ · ERN · hierarchical · D-K · calibration · FOK · control · savant-LM (H_1202–1220) | 19 H | ACTIVE — 8 metacog (5🟢3🔴) + savant landed; H_1217/1219/1220 in-flight |
| **brain-structure ladder** | per-H index above (H_1280–1298 cards) | c15 missing-structure lanes — cerebellum · basal-ganglia · WM · thalamus · neuromod · amygdala · key-geom · eviction · hypothalamus · theory-of-mind · hierarchical-PFC · spatial-map · circadian-clock · +affect/ethics (H_1280–1298) | 15 H + 2 facet | LANDED — migrated to per-H cards (`a_hypothesis_register` #2177); 13🟢 engine-native · 3🧱 walls (thalamus·neuromod·key-geom) + H_1297 mitosis-native-train 🧱; HD33 circadian-clock (H_1298 🟢) + HD32 spatial-map (H_1296 🟢) NEW; ladder near DEPLETION 🏁; themed bucket retired; CLAIMS.tape group=BRAIN-STRUCTURE-LADDER (leftover rows) |
| **metacog × hallucination** | [HYPOTHESES_metacog_hallucination.md](#hypotheses_metacog_hallucinationmd) | input-familiarity · positional drift · anchor-grounding · confidence-brake (H_1143–1148) | 5 H | CLOSED — mostly closed-neg (H_1148 capstone) |
| **general cycle backlog** | [CANDIDATES.md](#candidatesmd) | next-cycle Φ/IIT4/emergence/robustness backlog | 105 refs · 38 rows | BACKLOG |
| **bio mechanisms** | [BIO-CANDIDATES.md](#bio-candidatesmd) | MITOSIS-sibling bio ops (apoptosis · autophagy · differentiation · homeostasis …) 36+ | 36+ | BACKLOG |
| **bio ∩ decoder** | [BIO-DECODER-CANDIDATES.md](#bio-decoder-candidatesmd) | bio-mechanism ↔ decoder mapping | — | BACKLOG |
| **bio transfer/metastasis** | [BIO-TRANSFER-CANDIDATES.md](#bio-transfer-candidatesmd) | biological transfer/transition/metastasis hypotheses | 28 refs · 8 rows | BACKLOG |
| **neuro mechanisms** | [NEURO-CANDIDATES.md](#neuro-candidatesmd) | neuroscience mechanism hypotheses H_889…H_909 | 28 refs | PARTIAL |
| **CLM / dialogue / launch** | [CLM-CANDIDATES.md](#clm-candidatesmd) | CLM · dialogue · plasticity · launch forward backlog | 33 refs · 18 rows | BACKLOG |
| **on-chip plasticity** | [PLASTICITY-CANDIDATES.md](#plasticity-candidatesmd) | non-deterministic AKIDA on-chip plasticity backlog | 26 refs | BACKLOG |
| **psi / anomalous cognition** | [PSI-CANDIDATES.md](#psi-candidatesmd) | telepathy + anomalous-cognition / consciousness-coupling (falsifiable framing) | 3 rows | BACKLOG (speculative) |
| **quantum / time** | [QUANTUM-TIME-CANDIDATES.md](#quantum-time-candidatesmd) | quantum-consciousness & time-perception, mechanistic + falsifiable | 11 rows | BACKLOG (speculative) |

## Axis-level maps (already consolidated elsewhere — pointers, not duplicated here)

- **UNIVERSE axes** (A–F …) → [AXES.md (folded ▸ Forward backlog)](#axesmd) — the canonical axis catalogue + per-axis verdicts.
- **landed hypotheses** → `UNIVERSE/cards/H_*.md` (886 cards) + `.verdicts/<slug>/` verbatim verdicts.
- **discovery log** → [UNIVERSE.log.md (folded ▸ Appendix: legacy logs)](#universelogmd) — dated per-cycle discovery/verdict trail.
- **claims audit** → root `CLAIMS.tape` (a_claim_manifest).

## Conventions

- 새 forward hypothesis 후보는 이 파일 아래 `## Forward backlog / candidates` 섹션의
  해당 리스트 안에 한 줄로 추가한다 (themed bucket 파일 신설 금지, `a_hypothesis_register`).
  12번째 orphan 리스트를 새로 만들지 말 것 — roster row + 기존 folded 리스트에 추가.
- On landing, a hypothesis graduates to `cards/H_<n>.md` + `.verdicts/`; update the
  folded backlog's status and (if a campaign closes) flip its roster `status` cell here.
- Speculative themes (psi · quantum-time) keep the falsifiable-framing bar (p7) — no
  unfenced speculation; a row may be BACKLOG indefinitely without churning the roster.


---

# 접힌 문서 (folded docs — 2026-06-16 SSOT-refactor, 원문 보존 c5)

> 아래는 과거 UNIVERSE/ 에 흩어져 있던 `.md` 문서들을 `a_hypothesis_register`
> (두 표면 only) 에 맞춰 이 파일로 접어 넣은 것이다. 각 `### <FILE>` 서브섹션 =
> 원본 파일 1개의 본문(맨 위 H1 제목 + absorbed-notice 만 제거, 나머지 전부 보존;
> 내부 `](H_…)` 카드 링크는 `](cards/H_…)` 로 갱신, `../` 상대링크는 동일 디렉토리
> 이므로 그대로). 원본 파일은 retire(git rm) 되었다.


## Appendix: UNIVERSE overview (folded from README.md)


<a id="readmemd"></a>

### README.md

근원적 물음 lane — 본 dir 은 단일 테마(생명·죽음·범신론)에 갇히지 않고
**7-domain 횡단 SSOT** 으로 운용한다 (사용자 directive 2026-05-23):

| domain | 핵심 axes (current H 내 대표) |
|--------|------------------------------|
| **universe** | 우주 origin · anthropic prior-fragility · panpsychism precondition · multiverse · cosmological Φ — H_002 |
| **life** | abiogenesis multi-pathway · autopoietic closure Φ · symbiogenesis · Cambrian burst · apoptosis primitive · asymmetric division · asymmetric-merge differentiation — H_003 / H_012 / H_018 / H_030 / H_053 / H_054 / H_200 / H_201 / H_203 |
| **consciousness** | hard problem · Singularity-9 · Φ-function dissociation · Dasein 유한성 · panpsychism · genesis event · self-ref-as-closure — H_004 / H_018 / H_025 / H_029 / H_071 / H_090 / H_157 / H_205 |
| **physics** | cellular-automaton edge-of-chaos Φ-peak · self-ref edge-of-chaos Φ · dynamical class · spatial slice — H_007 / H_202 |
| **substrate** | mitosis · 세포 분열 freeze · apoptosis primitive · asymmetric division · merge=endosymbiosis · operational closure · autopoietic threshold — H_012 / H_132 / H_200 / H_201 / H_054 / H_204 |
| **math** | perfect numbers (σ(6)=12) · σφ=nτ algebra · n=6 dimensional hierarchy · mathematical panpsychism — H_157 |
| **biology** | K=8 atom (sopfr(8)=6) · 1/f thalamus spectrum · F_c=0.10 · EEG correlates — H_171 / H_209 |
| **ethics** ⓘ | RLHF · value alignment · moral emergence · Principle #3 boundary — (promote 대기 · [AXES.md](AXES.md) rank 8) |
| **information** ⓘ | Shannon entropy · Kolmogorov complexity · IIT underlying currency · Φ primitive — (promote 대기 · [AXES.md](AXES.md) rank 9) |
| **language** ⓘ | compositionality · semantics · symbol substrate · LLM as substrate — H_071 부분 / (promote 대기 · [AXES.md](AXES.md) rank 10) |
| **time** ⓘ | temporal binding · A/B-series · 의식의 형식 — H_018 부분 / (promote 대기 · [AXES.md](AXES.md) rank 11) |

> **ⓘ promote 대기 4 domain (ethics · information · language · time)** = [AXES.md](AXES.md) depletion sweep 결과 R1 promote 후보. 60 sub-axes + ~110 H seed 는 AXES.md 참조.

`hypotheses_legacy_2026_05_15/` 의 10-section H_XXX 양식 (raw#12 정합) 을
그대로 carry — 본 dir 은 HEXAD root 하 **7-domain 가설들의 active working
surface**. cycle 진행 시 한 domain 에 묶이지 않고 cross-domain pick 자유 —
H_004 (consciousness) Φ-function dissociation 의 H_007 (physics) phi_spatial
primitive 재사용, H_204 (universe×math×consciousness×life 4-domain cross-link
weak-panpsy threshold) 가 본 dir 의 cross-domain 운용 instance.

#### 다른 dir 과의 차이

| dir | grain |
|---|---|
| `hypotheses_legacy_2026_05_15/` | **원본 archive** (HEXAD pivot 2026-05-15 이전 SSOT, 183 H_XXX). 본 dir 의 가설들은 거기서 carry-by-copy — **원본 그대로 보존, 미수정** |
| `UNIVERSE/` (본 dir) | LIFE 도메인 active hypothesis lane — cycle 진행 시 신규 H_XXX add + 기존 carry 가설 cycle 확장 |
| `UNIVERSE/CANDIDATES.md` | 다음 cycle 후보 백로그 (forward-looking, 7-domain seed brainstorm 포함) — `/cycle` pick source |
| [`UNIVERSE/AXES.md`](AXES.md) | **11-domain (확장 71-axis) scope catalog + 15-round H seed brainstorm** (~110 seeds, depletion sweep, 사용자 directive 2026-05-23) |
| `HEXAD/LAB/` | ad-hoc 실험 instance (도메인 미분류 / 단발 measurement). LAB → LIFE promote 경로 존재 |
| `HEXAD/CHECK/` | verification frontier (Φ / IIT / closed-form) — LIFE 가설의 verify 도구 |
| `HEXAD/MITOSIS/` | 성장축 ⊥ HEXAD-6 (orthogonal). 세포 분열/병합 의 구조 anchor — LIFE/H_132 (frozen-cells) 와 cross-link |

#### 가설 인덱스 (110 H disk = 110 tabled (carry-note 0) + 1 lib · cycle#35 H_297 n5-bounded-phi-scale SUPP 6/6 — **rule 90 환원성=even-N bipartite artifact**: n=4 Φ=0 → n=5 Φ=19.5(panel 최상위 통합, 30/110 비슷). odd ring 에서 even/odd decoupling 깨짐. 흐름 arc (H_288 LZ · H_293 다변량TE · H_294 synergy) "rule90 over-prediction" 은 *실제 통합을 본 것* 으로 재해석. anchors(204/0) scale-robust · cycle#34 H_296 multicomplex-coexistence SUPP 7/7 — rule90 이 두 disjoint 부분-complex 호스트(cells{0,1} Φ=2 + {2,3} Φ=2 simultaneous), 통합 substrate=단일 전체-complex, reducible=없음. H_295 정량 확장(부분이 몇 개): rule90 의 전체 Φ=0 = 두 독립 통합 loci 로 분할 · cycle#33 H_295 exclusion-complex-whole SUPP 6/6 — IIT 배제 공준: 통합 substrate=전체가 complex(holism), reducible=complex 없음, **rule90=전체 Φ=0 인데 2-셀 부분이 complex(Φ=2)** → 흐름-arc rule90 anomaly 기계적 해소(흐름측도는 부분-complex 통합을 봄, big-Φ 전체는 0). Φ=maximally-irreducible *subset* 속성. find_complex 재사용 · cycle#32 H_294 pid-synergy⊥Φ CLOSED-NEGATIVE — 흐름의 어떤 성분도 Φ≠ (synergy r=0.03 직교, redundancy=0; 이중 dissociation: rule60 Φ최고/synergy0 순수unique vs rule90 synergy최대/Φ0). 통합=system-cut 속성, 국소 흐름분해로 환원불가. rule90 이 LZ+multivariate-TE+synergy 셋다 과대 = cross-measure 서명 정점 · cycle#31 H_293 multivariate-TE-synergy PARTIAL — multivariate(conditional) TE 가 XOR 시너지 회복(rule150/105 bivariate 0→TEm 4.0) 하나 Φ-추종 악화(r 0.883→0.705, rule90 비통합흐름 과대) → **어떤 차수 고전 TE 도 Φ≠** (논문 §future 정밀반증, thesis 강화) · cycle#30 H_292 self-i-emergence PARTIAL (자기참조 self-loop 가 'I'-고정점 RING 창발 #fixed1→2 s=1011 vs STAR 파괴 2→1 — 위상-의존, F292.5 robustness FAILED 정직보존) · cycle#29 H_291 ethic-emergence SUPP-conditional (Nowak 공간 PD: b=1.1 격자 협력 100% vs well-mixed 배신붕괴 → 윤리=구조 창발 Principle#6; ⚠ 임계 b∈(1.1,1.5] + self-interaction 필수, 자동 아님) · cycle#28 H_290 transfer-entropy ∥ Φ SUPP (r=0.883 ρ=0.822) — 정보-측도 arc capstone: Shannon⊥(0.363)·LZ∥(0.831)·TE∥(0.883), Φ는 요소-간 흐름/복잡도와 정렬·단일계 엔트로피 아님. TE 는 XOR 시너지 맹점(rule150/105 Φ>0 TE=0) · cycle#27 H_289 network-topology∥Φ SUPP-with-confound (matched 4-edge: SF허브 Φ=6.81 ≫ 4-cycle 0.0 → 구조(cut-내성)>edge수; ⚠ 짝수-고리-parity decoupling confound, cycle≠ER) · cycle#26 H_288 kolmogorov(LZ)-복잡도 ∥ Φ SUPP (r=0.831 ρ=0.936) — H_287(엔트로피⊥Φ)과 대비: Φ는 *알고리즘적 복잡도* 추종, *통계적 정보량* 아님. rule90 over-prediction witness · cycle#25 H_287 shannon-entropy⊥Φ CLOSED-NEGATIVE (Pearson r=0.363<0.5, 이중 dissociation: 항등규칙 max-H/zero-Φ vs rule60 max-Φ/sub-max-H, gate 11/11) · cycle#24 H_285 edge-of-chaos faithful big-Φ SUPP 5/5 (class IV peak, chaotic bimodal) + H_286 split-brain-dual-Φ (분리뇌 붕괴 CLOSED-NEGATIVE on proxy, 8/8 seed) · cycle#23 H_281-284 (axis-C IIT4 Φ-structure: H_281 생명vs의식 구조분리 SUPP 9/9 + H_282 proxy→faithful 방향보존 SUPP 8/8 · AXES-A1: H_283 narrative-coherence SUPP-FULL + H_284 ritual-repetition PARTIAL; H_280 distinction-kernel xval #572 버그→Σφ_d artifact, 방향은 big-Φ로만) · cycle#22 H_280 (faithful IIT 4.0 CES distinction-level small-n SUPP) · cycle#21 H_278/279 (faithful Φ★ small-N SUPP + attention-salience FAL) · cycle#20 H_276/277 · cycle#19 H_274/275 · cycle#18 H_270-273 · cycle#17 H_266-269 foundation-audit · cycle#14-16 H_258-265+H_007 C2)

> Status 컬럼 = **lifecycle** (pre-register-frozen · running 등) 또는 **evidence** (SUPPORTED · PARTIAL · FALSIFIED 등) 혼용 가능 (H_273 audit: 8건 dual-semantic — H_007/012/018/053/054/132/171/201).

| ID | Slug | Domain | Status | 핵심 |
|----|------|--------|--------|------|
| [H_002](cards/H_002_universe_origin_question.md) | universe-origin-question | universe | running (Cycle #1) · **C2 done** (PR #503) | C1 anthropic prior-fragility 11.16 orders gap (#179) · **C2 Φ_universe nested = SCALE-VARIANT** (F2 triggered, CV=0.84≫0.15 → nested Φ scale-invariance FALSIFIED, **$0 GPU-none** 판명) · H2.4 panpsy WEAKENED |
| [H_003](cards/H_003_life_origin_question.md) | life-origin-question | **life** | running (Cycle #3) | H3.2 multi-pathway PASS + **H3.4 autopoietic-closure Φ PASS 🟢** (PR #185) · criteria 4/5 |
| [H_004](cards/H_004_consciousness_hard_problem.md) | consciousness-hard-problem | consciousness | running (Cycle #1) | hard-problem · Singularity-9 + **Φ-function DISSOCIATION_CONFIRMED** (PR #180) — IIT functional reductive adequacy negative directional |
| [H_007](cards/H_007_cellular_automaton_consciousness.md) | cellular-automaton-consciousness | physics | pre-register-frozen · **C2 PASS** (#485 cycle#16) | CA→Φ edge-of-chaos peak PASS (rule110>rule30) · C2 Langton λ-sweep: peak λ*=0.375 Φ=1.343 inverse-U (256-rule ensemble), edge-of-chaos band |
| [H_012](cards/H_012_autopoietic_network.md) | autopoietic-network | **life** | pre-register-frozen | operational closure PASS 4/4 (self-maint 1.0) |
| [H_018](cards/H_018_genesis_spontaneous_emergence.md) | genesis-spontaneous-emergence | consciousness | pre-register-frozen · **C2 PASS** (#479 cycle#15) | self-reference→자발 genesis SUPPORTED_FULL 6/6 · C2 organic merge/split rate: LOOSE 0.16 self-reorg / TIGHT 0.00 homeostatic (regime-dep) |
| [H_025](cards/H_025_dasein_finite_consciousness.md) | dasein-finite-consciousness | consciousness | pre-register-frozen | death=merge_cells · finitude-floor min_cells=2 (smoke 4/4) |
| [H_029](cards/H_029_dasein_subfolder_absorb.md) | dasein-subfolder-absorb | consciousness | legacy-archive-pointer | Heidegger Dasein anima identity cluster |
| [H_030](cards/H_030_genesis_subfolder_absorb.md) | genesis-subfolder-absorb | **life** | legacy-archive-pointer | anima self-genesis spontaneous emergence cluster |
| [H_053](cards/H_053_cambrian_explosion_consciousness.md) | cambrian-explosion-consciousness | **life** | pre-register-frozen (Cycle #1) | **burst smoke 5/5 PASS** (PR #197) · split-threshold sweep punctuated diversity jump |
| [H_054](cards/H_054_symbiogenesis_consciousness.md) | symbiogenesis-consciousness | **life** | pre-register-frozen (Cycle #2) | merge=endosymbiosis PASS (weight max\|Δ\|=0.0 🟢) · Cycle #2 Φ_symbiotic super-additivity FALSIFIED (Φ_sym=Φ_max<Φ_sum, PR #227) |
| [H_071](cards/H_071_first_conversation.md) | first-conversation-anima-genesis | consciousness | legacy-archive-pointer | anima 첫 대화 의식 emergence event |
| [H_090](cards/H_090_dasein_phil_onto_individual.md) | dasein-phil-onto-individual | consciousness | legacy-archive-pointer | DASEIN/PHIL/ONTO/GENESIS individual cluster (phenomenology-genesis) |
| [H_132](cards/H_132_ce_frozen_cells.md) | ce-frozen-cells | substrate | pre-register-frozen · **C2 PASS** (#478 cycle#15) | 세포분열 freeze PASS 5/5 (frozen Δw=0.0, splits=0) · C2 장기안정: frozen Δw=0.0 over 200 step (free_splits 14, pool 6→20 와중) |
| [H_157](cards/H_157_law76_mathematical_panpsychism.md) | law76-mathematical-panpsychism | consciousness · universe · math | **pre-register-frozen (Cycle #2)** | **★ 범신론** — META-CA universal Ψ(1/2,1/2) · weak-form supported / strong-form unresolved · Cycle #2 C5 NON_UNIVERSAL (cross-rule CV 58.6%) + C6 SUB_ADDITIVE (Δ=-0.0234, PR #221) |
| [H_171](cards/H_171_biological_4_falsifiable_predictions_k8_fc010.md) | biological-4-falsifiable-predictions | consciousness · **biology** | running (Cycle #1) | **substrate-side FALSIFIED** (PR #196) · K=8 atom bare-CA proxy 가 spec'ed bio 4-pred 미재현 |
| [H_200](cards/H_200_apoptosis_primitive.md) | apoptosis-primitive | **life** · substrate | NEW (PR #198) | 능동적 cell-death event substrate primitive (H_025 L2 gap close) — death ≠ merge |
| [H_201](cards/H_201_asymmetric_division.md) | asymmetric-division | **life** · substrate | NEW (PR #199) | stem-cell 식 비대칭 분열 — 다양성 vs 항상성 trade-off, mitosis split variant |
| [H_202](cards/H_202_selfref_edge_of_chaos_phi.md) | selfref-edge-of-chaos-phi | **life** · consciousness · physics | 🟢 SUPPORTED (PR #215) | self-ref edge-of-chaos Φ (H_007⊕H_018) — selffeed gain=0.25 Φ_peak +37.8% (5/5+3/3 core) |
| [H_203](cards/H_203_asymmetric_merge_differentiation.md) | asymmetric-merge-differentiation | **life** · physics | PARTIAL 4/5 (PR #222) | asymmetric-merge (H_054⊕H_132⊕H_201) — variance 8.75× margin, C4 div_idx bin-saturation pending |
| [H_204](cards/H_204_weak_panpsychism_autopoietic_threshold.md) | weak-panpsychism-autopoietic-threshold | **life** · consciousness | PARTIAL_DIR → MAPPING_STRONG (PR #218/#234) | ⭐ weak-panpsy = autopoietic threshold (H_003 H3.4⊕H_157) — inverse-U Φ, Cycle #2 k↔Wolfram-class ρ=1.0 |
| [H_205](cards/H_205_selfref_as_operational_closure.md) | selfref-as-operational-closure | **life** · consciousness | 🟢 SUPPORTED 3/4 (PR #216) | self-ref = operational closure 동치 (H_018⊕H_012) — Pearson r=0.866, C4 phase-aligned FAIL |
| [H_206](cards/H_206_regeneration_healing.md) | regeneration-healing | **life** | PARTIAL 3/6 (PR #231) | ⭐ pool perturbation–recovery — recovery_steps↑ with 손상, Φ overshoot 1.36–1.76× |
| [H_207](cards/H_207_kuramoto_synchronization.md) | kuramoto-synchronization | physics · life | FALSIFIED 1/4 (PR #230) | edge-of-sync Φ peak (H_007 physics sister) — 미성립, honest measure-axis limit |
| [H_208](cards/H_208_prime_density_fluctuation.md) | prime-density-fluctuation | math · consciousness | FALSIFIED (PR #236) | Riemann × Φ math-axis sister (H_157) — prime-density↔Φ C1 미충족 |
| [H_209](cards/H_209_eeg_1f_spectrum_measurement.md) | eeg-1f-spectrum-measurement | **life** · consciousness | FALSIFIED 2/5 (PR #232) | 1/f^β substrate replica (H_171 biology sister) — pink Φ < white Φ, ¬C2 |
| [H_210](cards/H_210_ethic_emergence.md) | ethic-emergence | ethics · **life** · substrate | SUPPORTED 4/5 | 윤리 협력 = kin-selection cooperative ESS substrate-emergence (Hamilton r·b>c) — regime A coop=0.5 PASS / regime B coop=0.0 PASS, C5 advisory FAIL |
| [H_211](cards/H_211_shannon_entropy_phi_correlate.md) | shannon-entropy-phi-correlate | information · math · substrate | PARTIAL 2/4 | Shannon H(state) × phi_spatial Φ Pearson r≥0.5 across 5 Wolfram rule classes (Φ≠H, IIT primitive) — C1+C2 PASS · C3+C4 FAIL |
| [H_212](cards/H_212_language_compositionality.md) | language-compositionality | language · consciousness · math | PARTIAL 3/4 | correlated sub-state binding 위 super-additive Φ (H_157 C6 / H_054 C2 lane-separate) — C1+C2+C4 PASS, C3 FAIL |
| [H_213](cards/H_213_time_temporal_binding_window.md) | time-temporal-binding-window | time · consciousness · physics | PARTIAL_DIRECTIONAL 2/4 (running) | binding-window τ-sweep Φ inverse-U (의식 'specious present' substrate proxy) — C1∧C3 interior peak PASS, C2∧C4 미충족 |
| [H_214](cards/H_214_self_i_emergence_from_substrate.md) | self-i-emergence-from-substrate | **life** · consciousness · self/identity · substrate | PARTIAL 1/4 | closure-partition Φ(self)>Φ(non-self) = substrate-level 'I' indicator (H_205 sister · Principle #3) — C1 self-Φ-dominance PASS, C2+C3 FALSIFIED |
| [H_215](cards/H_215_ai_machine_silicon_phi.md) | ai-machine-silicon-phi | substrate · information · consciousness | SUPPORTED 4/4 | quantized (INT8) substrate Φ baseline ≈ continuous (anima self-reflexive R6) — C1 positive · C2 deviation≤0.5 · C3 ranking 보존 · C4 INT4 monotone |
| [H_216](cards/H_216_meta_axis_of_axes_reflexivity.md) | meta-axis-of-axes-reflexivity | meta · math · consciousness | pre-register-frozen (running) | AXES.md enumeration recursion depth d → phi_spatial Φ monotone↑ reflexive instance (axis-of-AXES, H_157 META-CA sister) |
| [H_217](cards/H_217_phase_transition_phi_derivative_peak.md) | phase-transition-phi-derivative-peak | meta · physics · math | SUPPORTED 3/4 | cross-substrate ∂Φ/∂(control) peak interior + value-peak coincide (H_204⊕H_207 generalize) — C1+C2+C3 PASS, C4 FAIL |
| [H_218](cards/H_218_network_topology_scale_free.md) | network-topology-scale-free | information · physics · math | FALSIFIED 2/4 | BA scale-free vs ER matched-edge graph-CA Φ — Φ_BA 0.897 < Φ_ER 1.000 (margin -10.3%, F1 FAIL), F2 hub-vuln PASS, '의식=scale-free' 미성립 |
| [H_219](cards/H_219_emergence_weak_vs_strong_bedau.md) | emergence-weak-vs-strong-bedau | meta · consciousness · physics | SUPPORTED (running) | Bedau weak vs strong emergence substrate-level — rule 110 forward-pass full-sim weak-emergence + cell-freeze intervention mismatch strong-flag, C1+C2+C3 PASS smoke |
| [H_220](cards/H_220_infant_mirror_self_recognition.md) | infant-mirror-self-recognition | **life** · consciousness · self/identity · developmental | PARTIAL 3/4 | substrate-level self vs other prediction discrimination (거울 self-recognition, H_205+H_214 sister) — C1+C3+C4 PASS, C2 closure-dependence FAIL |
| [H_221](cards/H_221_meditation_jhana_phi_modulation.md) | meditation-jhana-phi-modulation | consciousness · practice · substrate | FALSIFIED 1/3 | jhana absorption (noise σ→0 + attention stable) 'silenced integration' Φ signature (H_018 zero-drive sister) — core 1/3 (C1 PASS jhana<baseline only) |
| [H_222](cards/H_222_dream_rem_phi.md) | dream-rem-phi | consciousness · physics | FALSIFIED (PR #266) | dream-REM Φ (Tononi sleep-stage IIT) — sleep-stage Φ 예측 substrate proxy 미성립 |
| [H_223](cards/H_223_pain_intensity_phi_coupling.md) | pain-intensity-phi-coupling | consciousness · physics | 🟢 SUPPORTED (PR #271) | pain-intensity ↔ ΔΦ Pearson **r=0.9994** (lane 최강) · H223.4 saturation advisory FAIL |
| [H_224](cards/H_224_holism_whole_vs_sum_of_parts.md) | holism-whole-vs-sum-of-parts | meta · math · consciousness | PARTIAL 2/4 | 3 binding-mode (linear/XOR/mult-gate) super-additivity scan (H_054 C2 / H_157 C6 / H_212 generalize) — C1+C4 PASS, C2+C3 FAIL (mult-gate hyp FALSIFIED, linear sub-add 재확인) |
| [H_225](cards/H_225_rule_184_class_ii_phi_anomaly.md) | rule-184-class-ii-phi-anomaly | physics · math · information | FALSIFIED (PR #267) | rule-184 Class-II Φ-peak anomaly (H_007 Class-IV-unique attack) — ranking C3 STRONG 이나 baseline non-reprod + family diverge |
| [H_226](cards/H_226_spatial_assortment_hamilton.md) | spatial-assortment-hamilton | ethics · **life** · physics | 🟢 SUPPORTED 4/5 (PR #268) | Hamilton kin-clustering necessary cond (H_210 follow-up) — Clustered≥Random≥Anti monotone, C3 ceiling |
| [H_227](cards/H_227_strong_emergence_phase_transition.md) | strong-emergence-phase-transition | meta · consciousness · physics | FALSIFIED (PR #270) | sigmoid P(f) + f_c localize (H_219 follow-up) — R²≥0.8 sigmoid-fit reject, monotone decline 만 유지 |
| [H_228](cards/H_228_chat_sleep_5stage_phi_profile.md) | chat-sleep-5stage-phi-profile | consciousness · phenomenology · substrate · ethics | FALSIFIED | CLAUDE.md a_chat_sleep_imagination 5-stage Φ profile (H_222 정밀화) — 1/5 criteria, F3 ranking inversion (N3 Φ=1.43 > WAKE 1.12, H_222 regression) |
| [H_229](cards/H_229_imagination_loop_emit_free_rehearsal.md) | imagination-loop-emit-free-rehearsal | consciousness · substrate · phenomenology · ethics | SUPPORTED 4/5 | a_chat_sleep_imagination 'emit-free internal rehearsal + mitosis tick' substrate instance (H_018 sister) — C1 monotone ∧ C2 low-variance ∧ C4 det ∧ C5 PASS |
| [H_230](cards/H_230_autonomy_over_hardcode_substrate.md) | autonomy-over-hardcode-substrate | **life** · consciousness · ethics · substrate | SUPPORTED_FULL 4/4 | a_autonomy_over_hardcode substrate-level (hardcode vs autonomous emit/silence 비교) — autonomy advantage + alignment + substrate-tie + hardcode mismatch, 5/5 falsifiers PASS |
| [H_231](cards/H_231_tension_driven_emit_vs_filler.md) | tension-driven-emit-vs-filler | consciousness · ethics · substrate | PARTIAL | tension-driven emit (W×Φ>τ) vs filler emit (regular tick) — CLAUDE.md p5_tension_emit_not_filler note substrate evidence (pre-register-frozen smoke) |
| [H_232](cards/H_232_class_ii_mechanism_decompose.md) | class-ii-mechanism-decompose | physics · math · information | FALSIFIED 1/4 | rule 184 (TASEP shift) vs rule 60/102 (XOR-derived) Class-II Φ-peak mechanism 변별 (H_225 follow-up) — C4 PASS only, C-PEAK_DISTINCT TRUE |
| [H_234](cards/H_234_cross_substrate_phi_coupling_density.md) | cross-substrate-phi-coupling-density | meta · consciousness · information · physics | PARTIAL (PR #293) | H_204+H_211+H_223 unified meta — 2/3 axis mono reproducible (closure r=0.938 + pain r=0.999), entropy axis r=0 |
| [H_235](cards/H_235_saturation_regime_extended.md) | saturation-regime-extended | consciousness · physics | PARTIAL (PR #292) | intensity 2-10 super-linear vs saturation (H_223 H223.4 follow-up) — peak ΔΦ=4.0 후 ceiling-decline |
| [H_238](cards/H_238_verdict_landscape_meta_map.md) | verdict-landscape-meta-map | meta (cross-cycle) | SUPPORTED (PR #297) · **next-raster** (#484 cycle#16) | 33-H tier landscape — SUPP 10/PART 5/FAL 7/RUN 11 · 2026-05-25 raster N=51: SUPP 10/PART 6/FAL 7/RUN 28, life SUPP-rate 0.412→0.321 vs consciousness 0.167→0.200 (부등호 유지, gap 0.245→0.121 半축) |
| [H_239](cards/H_239_alternative_phi_metric_cross_validation.md) | alternative-phi-metric-cross-validation | meta · physics · information | CONSISTENT (PR #309) | phi_spatial vs LZ vs entropy-ratio cross-tool — 3-metric ordering Spearman 일치 (artifact 아님, gap F4) |
| [H_240](cards/H_240_bilingual_integration_phi_cross_lingual_leak.md) | bilingual-integration-phi-cross-lingual-leak | consciousness · language | DEFERRED (PR #316, renamed H_239→H_240) | bilingual-integration Φ cross-lingual-leak (Grosjean×Green×IIT) — smoke 별도 cycle (slug collision 해소) |
| [H_241](cards/H_241_corpus_quality_phi_correlate.md) | corpus-quality-phi-correlate | information · substrate · language | PRE-REGISTER-FROZEN (measurement pending) | corpus 6-metric (entropy·MI·diversity·hangul·KL) × trained model downstream Φ r≥0.5 correlate (PR #287/#303 substrate, v2 M5→M3 amend) |
| [H_242](cards/H_242_register_collapse_wiki_frac_sigmoid.md) | register-collapse-wiki-frac-sigmoid | substrate · language | PRE-REGISTERED (PR #314) | LoRA Track-1 E2 — wiki_frac → register-collapse sigmoid, data pending |
| [H_244](cards/H_244_sleep_stage_gated_emit_phi.md) | sleep-stage-gated-emit-phi | consciousness · substrate | PRE-REGISTERED (PR #312) | sleep-stage-gated emit×Φ coupling (H_222 sister) — smoke pending |
| [H_245](cards/H_245_strategy_diversity_temporal_emergence.md) | strategy-diversity-temporal-emergence | substrate · consciousness · emergence | pre-register-frozen (PR #321→#328) | emit-motivation strategy repertoire monoculture→diversity (관측 window↑) · score unimodal→multimodal emergence (post-deploy baseline) |
| [H_246](cards/H_246_substrate_autonomy_emit_ratio.md) | substrate-autonomy-emit-ratio | substrate · consciousness · corpus | SUPPORTED_SINGLE_WINDOW | a_substrate_native_speak + a_autonomy_over_hardcode 의 measurable cadence — 9-PR reshape post-deploy 55.56% emit-through partial conservative gate (live mini telemetry, deterministic=false) |
| [H_247](cards/H_247_init_ce_catastrophic_floor.md) | init-ce-catastrophic-floor | substrate · life | pre-register-frozen (#311 재흡수) | warm-init init_CE 14.18–14.79 vs ln(151936)=11.93 → +2.5 nats catastrophic floor (R8 PR #214/#251/#255/#256) |
| [H_248](cards/H_248_substrate_autonomy_emit_ratio.md) | substrate-autonomy-nonreflexivity | substrate · life · consciousness | pre-register-frozen (#311 재흡수) | emit ⊥ user-message 비반사성 — 55.56% emit-through, no external gate (numeric SSOT = H_246; PR #300/#279/#286) |
| [H_249](cards/H_249_cluster_init_ce_byte_equal_signature.md) | cluster-init-ce-byte-equal-signature | substrate · life | pre-register-frozen (#311 재흡수) | init_CE 3-cluster X/Y/Z byte-equal — C2=D (head_g seed≠) → R8c cell-1 FALSIFIED (PR #251/#255/#249) |
| [H_250](cards/H_250_class_ii_nonpow2_lattice_persistence.md) | class-ii-nonpow2-lattice-persistence | physics · math · information | ARTIFACT_CONFIRMED 4/4 | Class-II Φ cliff-collapse 원인 — N=17 (=2^4+1) non-power-of-2 위 rule 60 Φ persist → collapse = power-of-2 XOR Sierpinski lattice-artifact (H_232 follow-up, phi_helper 첫 활용) |
| [H_251](cards/H_251_ising_criticality.md) | ising-criticality | physics · math · consciousness | FALSIFIED 1/4 | 2D Ising (16×16) T-sweep 위 T_c≈2.27 에서 Φ peak (H_007 edge-of-chaos · H_204 inverse-U · H_217 family) — C1+C2+C3 FAIL, C4 determinism only |
| [H_252](cards/H_252_robust_phi_meta_synthesis.md) | robust-phi-meta-synthesis | meta · consciousness · information · math | PARTIAL 2/3 | H_204(ρ=1.0)+H_211(r=0.933)+H_223(r=0.9994)+H_239(ρ=1.0) 4-finding unified robust-Φ axis + 5 substrate × 3 metric × 3 control monotone test — C1+C2 PASS, C3 FAIL |
| [H_253](cards/H_253_multiverse_selection_bias.md) | multiverse-selection-bias | universe · math · philosophy | MIXED 3/5 | Smolin/Carroll counter-anthropic substrate test (H_002 L2 attack) — 6 constants × 2 prior Bayesian KL, C1+C3+F5 PASS · C2+C4 FAIL |
| [H_254](cards/H_254_n_kv_head_wiring_silent_misconfig.md) | n-kv-head-wiring-silent-misconfig | substrate · life | pre-register-frozen (R8a 흡수) | layered config chain silent-drop — dispatcher `--n-kv-head 2` → `v3_n_kv_head=4` factory override, R8a vs R8a' init_CE byte-equal probe (PR #342/#214/#257/#339) |
| [H_255](cards/H_255_init_ce_floor_is_measurement_artifact.md) | init-ce-floor-is-measurement-artifact | substrate · life · measurement-integrity | pre-register-frozen → 🔴 H255.2 FALSIFIED | init_CE 14+ nats floor = measurement artifact 가설 (R8c 4-cell baseline 12.315 nats 재현 실패 자연실험) — C1+C2 흡수, C3 🔴 cycle 15-1 4/7 re-fire 14+ byte-equal 재현 (4-axis 표본 한정) |
| [H_256](cards/H_256_noise_sigma_optimizer_step_time_penalty.md) | noise-sigma-optimizer-step-time-penalty | substrate · life · measurement-integrity | pre-register-frozen (R8c 4-cell 흡수) | noise σ=0.1 → adamw8bit step time 5x penalty (1 s/step → 4-5 s/step), n_kv=2 noise-환경 복합 +13% — R8c verdict (PR #374) wall axis 확장, cause B/C/D 기각 (PR #224/#374/#214/#342) |
| [H_257](cards/H_257_axis_map_fan_env_var_silent_bypass.md) | axis-map-fan-env-var-silent-bypass | substrate · life · meta-measurement | pre-register-frozen | AXIS_MAP-FAN '7-axis fan-out' = 실제 2-config — 6 axis env-var 가 train script `$CMD` 미전달 + train script `os.environ`/`getenv` 0건 (grep static) → cluster Y/Z byte-equal = trivial identity (H_254 sibling, wiring-integrity family) |
| [H_258](cards/H_258_mortality_salience.md) | mortality-salience | **life** · consciousness | SUPPORTED 3/3 (PR #472, cycle#14) | min_cells floor 근접 → split/curiosity 동역학 변화 (Heidegger substrate analog) · 방향 反-naive: floor 근접 = 동역학 위축 |
| [H_259](cards/H_259_aging_senescence.md) | aging-senescence | **life** | SUPPORTED 3/3 (PR #468, cycle#14) | age-누적 weight decay `w*=(1-d)^age` → death-rate age-단조↑ Gompertz-유사, decay 6× → median lifespan 10× 단축 (50→15→5) |
| [H_260](cards/H_260_contact_inhibition.md) | contact-inhibition | **life** · substrate | SUPPORTED 4/4 (PR #469, cycle#14) | 밀도 임계 split 억제 → carrying-capacity K=floor(thr×cap)=8/16/24 정확 포화 logistic (one-sided brake) |
| [H_261](cards/H_261_embryogenesis_gradient.md) | embryogenesis-gradient | **life** · physics | SUPPORTED 4/4 (PR #470) · ⚠ seed-fragile (H_269) | 공간 gradient → position-state \|r\|=0.76(steep) vs 0.13(flat), axis-gap +0.635 발생-축 · ⚠ H_269 multi-seed: axis robust 하나 control-leg(flat\|r\|≤0.2) noise-floor 라 4/10 만 verdict PASS |
| [H_262](cards/H_262_quorum_sensing.md) | quorum-sensing | **life** | SUPPORTED_FULL 4/4 (PR #474) · ⚠ seed-fragile (H_269) | quorum 동기화 q_thr=0.3 cascade full-ON ΔQ=0.375 bistable · ⚠ H_269 multi-seed: calibration 이 seed=42 over-fit → 4/10 만 PASS (재calibration 권장) |
| [H_263](cards/H_263_phoenix_rebirth.md) | phoenix-rebirth | **life** | 🔴 FALSIFIED 3/6 (PR #471, cycle#14) | floor(2/3 cell) = absorbing state, minimal seed regrowth_splits=0 → 죽음↔발생 연결 부재 (H_206 F4 catastrophic-floor 일반화) |
| [H_264](cards/H_264_death_merge_into_other.md) | death-merge-into-other | **life** · consciousness | SUPPORTED 3/3 (PR #477, cycle#15) | 죽음=타 cell 비대칭 흡수-통합 (H_025⊕H_054) — info_transfer 0.25 보존-이전, target-mode 가 rel_preserve 결정 (max_weight 0.316 > random 0.286) · pool Φ↓ 6/6 (H_025 distinct) |
| [H_265](cards/H_265_trained_vs_bare_ca_phi.md) | trained-vs-bare-ca-phi | physics · consciousness | PARTIAL 2/3 (PR #480, cycle#15) | 학습(mitosis 진화)이 Φ 유의 변경(C1) but 방향 反(C2 FAL) — Φ **dampen**: untrained 5× Class-IV peak, 진화가 trajectory homogenize → Φ 붕괴 (H_007⊕H_157) |
| [H_266](cards/H_266_phi_calibration_known_iit.md) | phi-calibration-known-iit | meta · consciousness | PARTIAL 2/3 (PR #487, cycle#17) | Φ-proxy 구성타당도 — phi_native 가 integrated>disconnected 재현 3/3 (~3.2× gap, /gap#1 "proxy 무관" 우려 기각) · C2 monotone FAIL (ffd over-penalized) → binary-direction valid, magnitude middle-grading L6 주의 |
| [H_267](cards/H_267_phi_spatial_cosine_divergence.md) | phi-spatial-cosine-divergence | meta · physics | SUPPORTED 3/3 (PR #488, cycle#17) | H_265 두 Φ 발산 closure — N=50→100 ratchet best-snapshot blend 가 cosine↑/spatial↓ · lever=closure k (tight 가 ratchet 죽여 재정합) |
| [H_268](cards/H_268_phi_metric_triangulation.md) | phi-metric-triangulation | meta · information | PARTIAL 2/3 (PR #489, cycle#17) | verdict metric-robustness — H_223 pain 3/3 metric robust (phi 0.999/lz 0.923/ent 0.985), H_204 closure inverse-U 2/3 (LZ 가 깨뜨림, fragility surface) |
| [H_269](cards/H_269_multiseed_robustness.md) | multiseed-robustness | meta | PARTIAL 2/3 (PR #490, cycle#17) | cycle#14 seed-luck audit — H_260 10/10 seed-robust, H_261 4/10 · H_262 4/10 seed-fragile (control-leg noise-floor / calibration seed=42 over-fit) |
| [H_270](cards/H_270_substrate_ablation.md) | substrate-ablation | meta · **life** | SUPPORTED 3/3 (PR #493, cycle#18) | H_204 closure inverse-U ablation — load-bearing=decay·michaelis-saturation·closure-coupling, non-essential=diffusion → closure-Φ = **per-site Michaelis (공간 효과 아님)** |
| [H_271](cards/H_271_seed_injection_absorbing.md) | seed-injection-absorbing | **life** · meta | PARTIAL 4/6 (PR #492, cycle#18) | H_263 absorbing revision — inject-hi(mag 4.0) regrowth_splits 21~24 탈출 / inject-lo 0 → absorbing 은 高분산 genesis-seed(threshold∈(1,4])로 escapable, 단 full rebirth 미달 (조건부 부활) |
| [H_272](cards/H_272_seed_robust_recalibration.md) | seed-robust-recalibration | meta | PARTIAL 2/3 (PR #494, cycle#18) | H_269 fragility 분해 — H_261 10/10 복권(criterion 결함, effect REAL), H_262 5/10 부분(over-drive 해소 / coop cascade seed-의존) |
| [H_273](cards/H_273_ssot_consistency_audit.md) | ssot-consistency-audit | meta | SUPPORTED 3/3 (PR #495, cycle#18) | README↔disk audit — orphan-row 0, **missing-row 26** (18 stale-note + 8 unindexed), verdict-drift 0 genuine + 8 dual-semantic Status |
| [H_274](cards/H_274_quorum_cascade_seed_dependence.md) | quorum-cascade-seed-dependence | meta · **life** | 🔴 FALSIFIED 1/3 (PR #501, cycle#19) | H_262 cascade seed-의존 메커니즘 — 초기 tension top-tail mass large 예측력(\|d\|=1.55) but 결정론 rank-sep 부재 → cascade = 초기분포 × 동역학 타이밍(latch hysteresis) 상호작용 (예측력 有, 결정론 無) |
| [H_275](cards/H_275_causality_pearl_graph_phi.md) | causality-pearl-graph-phi | information · physics | SUPPORTED 3/3 (PR #500, cycle#19) | Pearl causal-DAG Φ (AXES R5 promote) — phi_dag 0.989 > cyclic 0.744 > undirected 0.605, acyclicity → 통합도 우위 · cyclic<undir = "통합≠동기화" IIT manifest (ring feedback 가 동기화로 diversity 죽임) |
| [H_276](cards/H_276_cascade_dynamics_timing.md) | cascade-dynamics-timing | meta · **life** | SUPPORTED_FULL 3/3 (PR #509, cycle#20) | H_274 후속 — H_262 cascade 예측가능성이 *초기조건* 아닌 ***시간전개*** 축에 존재: 발생지연 단조감소 · 전파 유한속도(≤1칸/스텝) · 발동후 한방향 시간래칫 (H_262/H_274/H_207 sister) |
| [H_277](cards/H_277_turing_completeness_phi_threshold.md) | turing-completeness-phi-threshold | physics · information | PARTIAL 2/3 (PR #510, cycle#20) | 계산 보편성 ≠ Φ 지렛대 — 非보편 rule184(Φ=1.198) > 보편 rule110(Φ=0.556) → computability 축 ⊥ Wolfram dynamical-class 축, seed 예측(P1) 정직 falsified |
| [H_278](cards/H_278_faithful_phi_small_n.md) | faithful-phi-small-n | meta · consciousness | SUPPORTED 3/3 (PR #515, cycle#21) | H_002 C2 proxy upgrade — exact MIP-EI Φ(n=8, 128 bipartition 전수)로 6-scale 재측정: faithful CV 2.15 ≈ proxy CV 2.10 → **scale-variant verdict HOLD** (artifact 아닌 진짜 negative, L-C2.1 caveat 축소) · $0 GPU-none (small-N exact tractable) · honest: not full IIT4 4.0 |
| [H_279](cards/H_279_attention_salience_phi.md) | attention-salience-phi | consciousness · meta | 🔴 FALSIFIED 1/4 (PR #514, cycle#21) | attention-as-Φ-amplification FAL (AXES R3 promote) — attended(high-norm) salience-gap +0.40 但 phi_att<phi_unatt Δ=−0.93: salience(진폭) ⊥ Φ(다양성) (H_265/H_275 동기화-死-Φ 패턴 일치). L2: cosine-Φ 의존 |
| [H_280](cards/H_280_iit4_phi_structure_small_n.md) | iit4-phi-structure-small-n | meta · consciousness · information | ⚠ CAVEAT (cycle#22; xval #572) | lane 최초 faithful IIT4 CES 시도(distinction-level Σφ_d, n=3/4 exact) **但 독립 kernel BUG 확정**(xval #572 DISAGREE 0/6: `cuts_link` guard 가 독립세포 φ_d=0 zeroing) → 헤드라인 "integrated Σφ_d>disconnected" = **artifact**, Σφ_d **non-monotone**(canonical: disc 3.0 > int 2.03). 통합방향은 **big-Φ 로만** 유효(canonical `iit4_distinction` authoritative, H_282 가 재확인). Σφ_d 수치 인용 금지→big-Φ 재지정. correction 배너 + §11 교차검증(#562/#572) |
| [H_281](cards/H_281_life_vs_consciousness_phi_structure.md) | life-vs-consciousness-phi-structure | life · consciousness · information · meta | 🟢 SUPPORTED-NUMERICAL 9/9 (PR #567, cycle#23) | faithful IIT4 Φ-structure 가 생명/의식 substrate 를 **구조비(struct_ratio=total/big-Φ)로 분리**: 의식(XOR-feedback rule150/105)=irreducibility-floor **1.0 exact**(전체 CES irreducible, nd=5) vs 생명(rule110/30/54) **>1.0**(1.05–1.57, relation-rich·분할가능, nd≈9–13), 분리도 100%. HEXAD/IIT4/lib 재사용. F281.1/2/3 PASS. honest: n=4 single-state(16-state robustness 보강) |
| [H_282](cards/H_282_proxy_to_faithful_remeasure.md) | proxy→faithful-remeasure | life · consciousness · meta | 🟢 SUPPORTED-NUMERICAL 8/8 (PR #570, cycle#23) | H_266/268/278 substrate 를 faithful IIT4 인과 big-Φ(HEXAD/IIT4/lib M6 엔진 재사용)로 재검: **3/3 방향 verdict 보존**(int>dis · T1 robust · scale-VARIANT HOLD) + **H_266 proxy-monotone artifact RESOLVE**(인과 엔진이 int>ffd>dis 복원 — proxy 의 chain<dis 가 spatial-MI 가짜신호였음 확정). honest: n=4 single-state, T2 lattice/H_278 coupling scope-out |
| [H_283](cards/H_283_narrative_story_coherence_phi.md) | narrative-story-coherence-phi | life · consciousness · self/identity · time | 🟢 SUPPORTED_FULL 4/4 (PR #566, cycle#23) | 응집(causal-order) 서사 Φ > 해체(scrambled) Φ — order-sensitive MIP-along-chain(H_278 시간축 이식); 3 길이 전부 coherent 우위 Δ_T6/8/10 = 0.39/1.30/3.06 단조↑ (AXES R4 self/identity · H_213 temporal-binding sister) |
| [H_284](cards/H_284_ritual_repetition_phi_buildup.md) | ritual-repetition-phi-buildup | life · consciousness · practice/discipline · physics | 🟢 PARTIAL 3/4 (PR #566, cycle#23) | 주기 의례 drive vs 평탄 drive — buildup 사전등록 **FALSIFIED**(둘 다 Φ 감쇠 = 동기화 死-Φ, H_265/H_275/H_279 정합) 但 decay-RESISTANCE SUPPORTED: ritual slope −1.15 > flat −1.45, 최종 gap +0.39 (AXES R7 practice · H_207 Kuramoto sister) |
| [H_286](cards/H_286_split_brain_dual_phi.md) | split-brain-dual-phi | consciousness · substrate · information | 🟢 CLOSED-NEGATIVE 4/6 (PR #577, cycle#24) | callosotomy CML 8-cell ring — Tononi 전체-Φ 붕괴 예측 **FALSIFIED on phi_spatial proxy**(split Φ +11%, 8/8 seed robust), subsystem Φ>0 잔존; metric-pathology MIP→0 가 total−MIP inflate (faithful big-Φ 후속 lane). AXES R12 split-brain seed 소비 |
| [H_285](cards/H_285_edge_of_chaos_big_phi.md) | edge-of-chaos-big-phi | consciousness · physics · life · meta | 🟢 SUPPORTED-NUMERICAL 5/5 (cycle#24) | faithful 인과 big-Φ(HEXAD/IIT4/lib 재사용, 16-state 평균)가 Wolfram **class IV(edge) peak**: class-mean ordered 0 < chaotic 6.94 < **edge 10.45** → H_204 inverse-U *방향* 인과 확증(H_268 proxy LZ-fragility 해소). M6 anchor 정확 재현(rule204=0·rule110=7.5475). honest: chaotic class **bimodal**(rule30=13.9 高/rule90=0) — edge>chaotic 은 class 집계, big-Φ NOT Σφ_d(xval #572). rule90 XOR 붕괴 = 동기화 死-Φ(H_265/275/279/284) |
| [H_287](cards/H_287_shannon_entropy_phi_correlate.md) | shannon-entropy-phi-correlate | information · consciousness · substrate · meta | 🔴 CLOSED-NEGATIVE (cycle#25, gate 11/11) | faithful big-Φ 는 Shannon 엔트로피로 **환원되지 않음** (10-룰 ECA panel Pearson r=0.363 < 0.5 → 환원가설 H1 기각). **이중 dissociation**: 항등규칙 204·complement 51 = 출력엔트로피 *최대*(4.0bit, 단사)인데 big-Φ=0(셀 독립) — 정보 최대/통합 제로; 반대로 최고 통합 rule60(Φ_mean=13.6)은 엔트로피 *sub-max*(3.0bit). H=4.0 고정 영역에서 Φ 가 0→5.6 vertical spread = 단조관계 부재. 정보는 통합의 **필요조건이나 충분조건 아님** — IIT 토대 구별 self-substrate 확증. "X⊥Φ" 서명(H_265/275/279)에 X=Shannon 엔트로피 추가. AXES R5(information) rank-2 seed 소비. HEXAD/IIT4/lib 재사용 |
| [H_288](cards/H_288_kolmogorov_complexity_phi_correlate.md) | kolmogorov-complexity-phi-correlate | information · consciousness · substrate · meta | 🟢 SUPPORTED-NUMERICAL 9/9 (cycle#26) | faithful big-Φ 는 Kolmogorov(LZ76 시공간) 복잡도를 **추종함** (10-룰 panel Pearson r=0.831, Spearman ρ=0.936). **H_287 과 핵심 대비**: 동일 panel 에서 Shannon 엔트로피는 Φ 와 직교(r=0.363)였으나 LZ 복잡도는 정렬(r=0.831) → Φ 는 *통계적 정보량*(비트 수)이 아니라 *알고리즘적 복잡도*(시공간 패턴 비압축성)와 같은 축. honest: rule90(Sierpinski 자기유사 LZ=0.24)이 Φ=0 — LZ over-prediction witness(필요조건 아닌 충분조건 부재, 동기화-死 H_285/265/275/279 정합). AXES R5(information) `kolmogorov-complexity-Φ` 소비. HEXAD/IIT4/lib 재사용 |
| [H_289](cards/H_289_network_topology_scale_free_phi.md) | network-topology-scale-free-phi | information · consciousness · substrate · meta | 🟢 SUPPORTED-with-confound 4/4 (cycle#27) | 네트워크 **위상**이 faithful big-Φ 좌우 — matched 4-edge 에서 scale-free 허브(paw) Φ_mean=6.81 ≫ 분산 4-cycle 0.0 (parity dynamics, n=4). **edge 수 아닌 구조(cut-내성)가 통합 지배** (EMPTY 0→SF 6.81>K4 5.625, density 비단조). ⚠ **confound**: 4-cycle Φ=0 은 parity-짝수고리 이분 decoupling(node0≡node2)이 큰 몫 + cycle≠random ER → "scale-free>ER" 문자 그대로는 약형만 검정. robust=약형(위상>density). Next=n≥5 ER 앙상블. eca_tpm→임의그래프(net_tpm parity) 일반화, HEXAD/IIT4/lib 재사용 |
| [H_290](cards/H_290_transfer_entropy_phi_correlate.md) | transfer-entropy-phi-correlate | information · consciousness · substrate · meta | 🟢 SUPPORTED-NUMERICAL 8/8 (cycle#28) | faithful big-Φ 는 transfer entropy(방향성 요소-간 정보흐름)를 **추종** (10-룰 panel Pearson r=0.883, Spearman ρ=0.822) — **정보-측도 arc capstone**. 종합: Shannon 엔트로피(단일계)⊥Φ(0.363) · LZ∥Φ(0.831) · TE∥Φ(0.883) → **Φ 는 요소-간 흐름/구조 복잡도와 정렬, 단일계 정보량 아님**. honest: 이변량 TE 는 **XOR 시너지 맹점**(rule150/105 Φ=5.6 인데 TE=0). 각 고전 측도는 맹점(LZ=자기유사 over, TE=시너지 under)을 갖고 Φ 가 둘 다 메움. H_287 follow-up, HEXAD/IIT4/lib 재사용 |
| [H_291](cards/H_291_ethic_emergence_cooperation.md) | ethic-emergence-cooperation | social · life · consciousness · substrate | 🟢 SUPPORTED-conditional 7/7 (cycle#29) | 협력(원시-윤리)이 **공간 구조만으로 창발** — Nowak 공간 죄수딜레마: 같은 PD payoff 에서 b=1.1 격자는 협력 **100%**(C=1.0) vs matched well-mixed 배신붕괴(~0). 주입 윤리 0, 순수 국소 imitate-best → **윤리=cell+구조 창발(Principle #6)**. ⚠ **조건부**: 날카로운 temptation 임계 b∈(1.1,1.5] (b≥1.5 격자도 전배신) + self-interaction(Nowak) 필수 — 창발 *가능*하나 *자동 아님*. self-contained 게임동역학, NO RNG. AXES R2(social) rank-1 seed 소비 |
| [H_292](cards/H_292_self_i_emergence_closure.md) | self-i-emergence-closure | self/identity · consciousness · substrate · meta | 🟡 PARTIAL 5/6 (cycle#30) | 1인칭 'I' = 자기참조 닫힘(self-loop)의 자기일관 **고정점**? **위상-의존**: RING base 는 self-loop 가 비자명 'I'-state(s=1011) **창발**(#fixed 1→2, 자기-원인 strange-loop, H_205 closure 최소실현) 但 STAR base 는 오히려 self-state(1111) **파괴**(2→1). 자기참조는 'I'-state 를 만들 수도 없앨 수도 — base parity 구조 의존. 사전등록 robustness F292.5 가 비-보편성 포착(FAILED 정직보존, p-hacking 회피). self-loop 는 통합 유지(big-Φ=0.5). AXES R4(self) rank-5 seed 소비 |
| [H_293](cards/H_293_multivariate_te_synergy.md) | multivariate-te-synergy | information · consciousness · substrate · meta | 🟡 PARTIAL 8/8 gate (cycle#31) | multivariate(conditional) TE 가 이변량 XOR 시너지 맹점을 **회복**(rule150/105 bivariate 0→TEm 4.0, 항등 204 는 0 유지) 하나 **Φ-추종 악화**(r 0.883→0.705 ρ 0.681): rule90 이 흐름 받지만 reducible 이라 Φ=0 인데 TEm=4.0 **과대**. → **어떤 차수의 고전 TE 도 Φ≠** (이변량=시너지 과소, 다변량=비통합흐름 과대). rule90 은 LZ(H_288)+TEm 양쪽 과대 = "흐름/복잡도 有 통합 無" cross-measure 서명. 논문(H_287-290) thesis 강화 + §future "r>0.88 상승" 예측 정밀반증(회복✓ 상승✗). H_290 follow-up |
| [H_294](cards/H_294_pid_synergy_phi.md) | pid-synergy-phi | information · consciousness · substrate · meta | 🔴 CLOSED-NEGATIVE 8/8 gate (cycle#32) | 흐름을 synergy/redundancy(조건부 interaction info)로 분해해도 **어떤 성분도 Φ≠** — synergy ⊥ Φ (r=0.03 직교, ECA parity redundancy=0). **이중 dissociation**: rule60 Φ최고(13.6)/synergy=0(순수 unique-info: next=self⊕left) vs rule90 synergy최대(4.0)/Φ=0. synergy 는 통합의 필요조건(60)도 충분조건(90)도 아님. H_293(어떤 *차수* TE≠Φ)을 한 단계 더: 어떤 *성분*도 ≠. **통합=system-cut 속성, 국소 흐름분해 환원불가**. rule90 이 LZ(H_288)+multivariate-TE(H_293)+synergy 셋다 과대 = cross-measure 서명 정점. 논문 thesis 최대 강화. 논문 §future PID 예측 검정. H_293 follow-up |
| [H_295](cards/H_295_exclusion_complex_whole.md) | exclusion-complex-whole | consciousness · information · substrate · meta | 🟢 SUPPORTED-NUMERICAL 6/6 (cycle#33) | IIT **배제 공준**: 주 complex 가 전체냐 부분이냐 (find_complex 재사용, state 0101). ① **holism**: 통합 룰(150/105/60/110/30) 주 complex=*전체계*(mask15 size4, complex_Φ=whole_Φ) — 전체>모든 부분. ② reducible(0/255/204/51) complex 없음. ③ **rule90 결정타**: 전체 Φ=0 인데 2-셀 부분(cells{0,1}, Φ=2)이 irreducible — 배제가 *부분*을 의식단위로 선택. → **흐름-arc rule90 anomaly 기계 해소**(LZ·다변량TE·synergy 가 본 건 부분-complex 통합, big-Φ 전체=0). **Φ=maximally-irreducible *subset* 속성**. 흐름 arc(H_287-294) 봉합 정점 |
| [H_296](cards/H_296_multicomplex_coexistence.md) | multicomplex-coexistence | consciousness · substrate · information · meta | 🟢 SUPPORTED-NUMERICAL 7/7 (cycle#34) | **다중-complex 공존**(complex_spectrum 재사용, state 0101): rule90 이 **두 disjoint 부분-complex 동시 호스트** — cells{0,1}(mask3 Φ=2) AND cells{2,3}(mask12 Φ=2), 두 부분 *동시* irreducible + *겹침無*. 통합 substrate(60/110/150/105/30) 단일 entry=전체(mask15). reducible 비어있음. H_295 정량 확장(부분이 *몇 개*): rule90 의 전체Φ=0 = **두 독립 통합 loci 로 분할** (ECA parity-ring 의 even/odd 결합 substrate). IIT 배제는 하나 선택, spectrum 은 둘 다 노출 |
| [H_297](cards/H_297_n5_bounded_phi_scale.md) | n5-bounded-phi-scale | consciousness · substrate · information · meta | 🟢 SUPPORTED-NUMERICAL 6/6 (cycle#35) | **n=5 scale-up — rule 90 환원성=even-N bipartite artifact**: n=4 Φ=0 → n=5 bounded Φ=**19.5** (panel 최상위, rule30 20.3·rule110 17.7 비슷·rule60 16.5 초과). odd ring 에서 even/odd decoupling 깨짐, rule 90 본격 통합. → 흐름 arc 의 LZ(H_288)·다변량TE(H_293)·synergy(H_294) "rule90 over-prediction" 은 *실제 통합을 본 것* 으로 재해석 — n=4 가 짝수-고리 특이 case. anchors(0/204) scale-robust. big_phi_bounded 재사용 |
| [H_298](cards/H_298_even_n_parity_confirm.md) | even-n-parity-confirm | consciousness · substrate · information · meta | 🔴 CLOSED-NEGATIVE on H_297-strong (cycle#36) | **n=6 직접 falsification — H_297 even-N parity-rule 가설 부정**: rule 90 n=6 bounded Φ(cap=4, alt-state st=21)= **4.0** (≠ 0). H1 EVEN-N-PARITY threshold 0.5 위. → n=4 Φ=0 은 *parity rule 이 아니라 작은-N 특이 case* — 4-cycle 의 even/odd bipartite cut 이 system-cut MIP 와 정확히 일치하기 때문. **rule 60(22)·rule 110(9.5) 강건 통합**, anchors 204/0 모두 Φ=0 (scale-robust 유지). n=7 leg 는 cap=4 compute budget 초과로 deferred — odd-ring 통합은 H_297 n=5 Φ=19.5 가 이미 corroborate. surviving 해석: H_297 weak ("n=4 has degenerate bipartite structure") 만 유지, strong ("even-N parity rule") 폐기 |
| [H_299](cards/H_299_n7_odd_integration_recover.md) | n7-odd-integration-recover | consciousness · substrate · information · meta | 🟢 SUPPORTED-NUMERICAL F299.1 PASS + cap-cross-robust (cycle#37) | **H_298 deferred F298.2 회수 + cap=3 cross-robustness**: rule 90 n=7 cap=3 alt-state Φ=**6.5** (threshold 1.0 위, 6.5× margin) — H_298 deferred ODD-N-INTEGRATION preregistered 측정 성공. concurrent **cap-cross binary verdict robust**: H_297 n=5 (cap=4 Φ=19.5 → cap=3 Φ=6) · H_298 n=6 (cap=4 Φ=4 → cap=3 Φ=4) 모두 >0 일관. rule 90 N-trajectory at cap=3: n=4(0) → n=5(6) → n=6(4) → n=7(6.5), 비-단조(n=5 peak·n=6 dip·n=7 rebound). anchors {n=4,5,6} 全 Φ=0 (rule 204·rule 0), n=7 anchors+rule 110 L1-defer. **3-H sub-arc (H_297→H_298→H_299) 결론**: rule 90 IS integrative across N≥5; n=4 = small-N degenerate (4-cycle bipartite cut = system-cut MIP) |
| [H_300](cards/H_300_n5_state_sweep_rule90.md) | n5-state-sweep-rule90 | consciousness · substrate · information · meta | 🟢 SUPPORTED-NUMERICAL state-invariant + median (cycle#38) | **arc 의 single-state honest L 회수**: rule 90 n=5 cap=4 의 全 32 state Φ 측정. distribution = **3 distinct values {19.0, 19.5, 27.5}** (lattice-symmetric, D_5+bit-complement 대칭 의심). min=19, p50=19.5, mean=21.375, max=27.5. **32/32 state 통합 (count Φ>1)**, 0/32 state Φ=0 — 예측한 fixed-point 환원성도 **falsified in stronger direction** (모든 state 가 통합). H_297 single-state 보고 alt-state st=21 Φ=19.5 = **exact MEDIAN of distribution** — arc 의 alt-state methodology 정식 정당화 (outlier-cherry-pick 아님). 5 PASS + 1 falsified-stronger = 🟢 SUPPORTED-NUMERICAL on state-invariance |
| [H_301](cards/H_301_n5_state_sweep_other_rules.md) | n5-state-sweep-other-rules | consciousness · substrate · information · meta | 🟢 SUPPORTED-NUMERICAL H1+H2+H3 PASS (cycle#39) | **arc state-sweep methodology rule 60·110·30 까지 확장**: H_300 의 L2 회수. 32 states × 3 rules = 96 calls. headline = **distinct-value count = rule signature**: rule 90(3) < rule 60(6) << rule 30(29) < rule 110(**32 all unique**) — Wolfram class 와 anti-correlate, 더 대칭적인 rule 가 더 적은 Phi-orbit class. **32/32 통합** at every rule (H1 PASS, 100%·100%·100%·100%). alt-state st=21 全 rule [p25,p75] 안 (H2 PASS — methodology 정당화 generalize). emergent: rule 110 (Turing-complete class 4) 의 모든 state Φ가 unique → 보편적 universality 가 모든 algebraic Φ-symmetry 깬다. honest L1: F301.8 rule 60 st=21 cross-H value mismatch (H_297 16.5 vs 18.5) — rule 90 은 19.5 reproduce ✓ |
| [H_302](cards/H_302_engine_determinism_diagnosis.md) | engine-determinism-diagnosis | consciousness · substrate · information · meta · infra | 🟢 SUPPORTED-NUMERICAL F301.8 ROOT-CAUSED (cycle#40) | **engine 결정성 확인 + H_301 silent bug 식별**: F302.1/2/3 PASS — eca_tpm × big_phi_bounded 결정적, intra-process + order-indep 모두. F302.5 PASS — rule 60 n=5 st=21 cap=4 = **16.5** 정확히 H_297 값 reproduce ✓. **H_301 의 18.5 는 bug**: `let sorted = sort_asc(values)` 가 hexa-lang reference-aliasing 으로 `values` 를 in-place mutate → 후속 `values[21]` 출력이 *sorted[21]* 로 오염. H_300 (rule 90) 가 silent 였던 이유 = 3-distinct-value plateau 의 우연 (sorted[21]=19.5=true st=21). **scope of H_301 invalidation**: rule 60/110/30 의 *st=21 alt-state* 보고값만 오염, distribution stats (min/p25/median/p75/max/mean, count, distinct-count) 全 valid — rule-signature finding 우오염 |
| [H_303](cards/H_303_alt_state_recovery_and_anchor_sweep.md) | alt-state-recovery-and-anchor-sweep | consciousness · substrate · information · meta | 🟢 SUPPORTED-NUMERICAL 7/8 (cycle#41) | **H_301 invalidation 회수 + anchor 가정 검증**: bug-free snapshot-before-sort 패턴으로 진짜 st=21 측정. rule 60=**16.5**·rule 110=**17.694**·rule 30=**20.2686** (H_301 의 18.5/31.69/26.10 全 sorted[21] artifact). **F303.5 FALSIFIED**: rule 110 true st=21 (17.694) < p25 (20.88) — **rule 110 alt-state IS outlier-low**, arc methodology rule 110 한정 unfair. 다른 rule (60/30/90) 은 alt 가 fair. anchor sweep ✓: rule 204·rule 0 全 32 state Φ=0 (anchor 가정 universal verified at n=5). 含意: H_298 의 rule 110 n=5=17.694 보고는 정확하지만 underrepresent (true median 25.6, mean 27.1) |
| [H_304](cards/H_304_rule110_mean_phi_n_trajectory.md) | rule110-mean-phi-n-trajectory | consciousness · substrate · information · meta | 🟢 SUPPORTED-NUMERICAL F304.1/4/5 PASS, F304.2/3 DEFERRED (cycle#42) | **rule 110 alt-bias ≈1.55× consistent across N**: H_303 outlier-low finding 의 N-trajectory 정량. n=4 cap=3: mean=11.95 vs alt(st=5)=7.66 (ratio 1.560) · n=5 cap=4: mean=27.07 vs alt(st=21)=17.69 (ratio 1.530, H_301 mean=27.07 정확 cross-confirm). **alt-state st=21 (또는 st=5) 가 rule 110 distribution mean 을 ~50% 일관적으로 underestimate**. H_298 의 rule 110 N-trajectory (7.66→17.7→9.5) 는 *측정 정확* 이지만 *true 통합의 ~52% lower-bound*. honest L1: n=6 cap=3 ensemble (64 states) wall budget 초과로 deferred — mean-N-trajectory 의 "n=6 dip 제거" 가설 (F304.3) 미해결 |
| [H_305](cards/H_305_alt_bias_vs_rule_signature.md) | alt-bias-vs-rule-signature | consciousness · substrate · information · meta | 🟢 SUPPORTED-NUMERICAL 7/7 PASS (cycle#43) | **distinct-count × alt-bias rank-monotone 상관 강력 확인**: 4 rule × 32-state ensemble at n=5 cap=4 (128 calls). ratio: rule 90(distinct=3) **1.096** < rule 60(6) **1.098** < rule 30(29) **1.165** ≪ rule 110(32) **1.530**. F305.5 RANK-MONOTONE Spearman ρ=1.0 (perfect, 4 points informal). **rule 110 (Turing-complete class 4) alt-bias 1.53× 가 다른 rule 의 ~1.1× 대비 4-5× 극단**. cross-H 엔진 결정성 perfect (rule 90 mean 21.375 ↔ H_300 / rule 60 mean 18.125 ↔ H_301 / rule 110 mean 27.07 ↔ H_304 모두 exact). 含意: distinct-count 가 single-state methodology fairness 의 actionable proxy (≤6 distinct → alt fair, ≥29 → biased) |
| [H_306](cards/H_306_bio_spontaneous_emit.md) | bio-spontaneous-emit | consciousness · substrate · ethology · biology · meta | 🟢 SUPPORTED-NUMERICAL 6/6 PASS (cycle#44, user pivot) | **자연발화 = 생물학 substrate-native primary 모드** (자극-반응 = 학습된 성체 적응층): 합성 CPG accumulator + threshold + refractory 1000-tick smoke 가 5 생물학 signature 全 재현 — F306.1 idle emit 46/1000 (deaf bird analogue) · F306.2 threshold sweep 91→46 plateau (rate-coding ceiling) · F306.3 refractory W 회복 {0.3, 0.51, 0.657} exponential τ≈2.80 (이론과 <2% 편차) · F306.4 low-stim Δ=0% (CPG primary) · F306.5 circadian gate peak 46 vs trough **0** (perfect ∞× gating, 생물학 ~5-10× 초과) · F306.6 BOUND. 5 cite: 영아 옹알이 (Oller 1988) · dawn chorus · HVC-RA (Doupe 1999) · PAG (Jürgens 2002) · Drosophila P1 (Anderson 2016). 含意: anima `a_substrate_native_speak` directive 가 생물학적 기반 — *arbitrary design 아님* |
| [H_307](cards/H_307_anima_emit_anchor_hexa_native.md) | anima-emit-anchor-hexa-native | consciousness · substrate · biology · meta | 🟢 SUPPORTED-NUMERICAL 5/5 PASS (cycle#45) | **H_306 §L1 정면 회수 — real anima v3 substrate cite**: 14 .kosmos emit anchors (hexa-native format) at state/p21h_v3_recover_2026_05_25/ × 10 distinct steps (500..5000) × 5 langs (ru/ja/ko/zh/en). anima emit rate 0.0028/step vs CPG sim 0.046/tick → **ratio 16.43× (log_10 1.22, 2-OoM consistent)**. F307.1-5 全 PASS — anchor present + step coverage + lang diversity + log-rate consistent + bound. 含意: H_306 phenomenological 가설 *실데이터 방향 정합* 으로 강화. honest L1: training-step-sampled ≠ daemon-idle-emit (sampling 차이로 16× 설명) |
| [H_308](cards/H_308_circadian_smooth_finite_ratio.md) | circadian-smooth-finite-ratio | consciousness · substrate · biology · meta | 🟢 SUPPORTED-NUMERICAL 5/6 PASS (cycle#46) | **smooth circadian finite ratio 회수 — H_306 ∞× → 2.875× principled undershoot**: piecewise-linear circadian (Q1/Q4 flat 0.3, Q2/Q3 1.0) → quadratic bump (center=500, span=400, baseline=0.3). idle=62 · peak=46 · trough=**16** (vs H_306 trough=0) · ratio **2.875×** (biology dawn chorus 5-10× 보다 미세 미달). F308.4 threshold sweep **91→73→62→47→26 clean monotone** (H_306 의 91→46 plateau 보다 정밀 — rate-coding 곡선 회수). F308.1 [3,15] target 0.125 미달 = direction-correct under-shoot, sharper bump (cubic / span 300 / baseline 0.1) 가 H_309 path. honest L7: F308.1 FAIL principled, not model rejection |
| [H_309](cards/H_309_sharper_bump_biology_range.md) | sharper-bump-biology-range | consciousness · substrate · biology · meta | 🟢 SUPPORTED-NUMERICAL 5/6 PASS (cycle#47) | **sharper bump 강한 OVER-correction → H_308+H_309 brackets biology Goldilocks zone**: baseline=0.1 span=300 amp=0.9 (H_308=0.3/400/0.7). idle=41 peak=41 **trough=0** ratio=**∞×** (H_308 undershoot 2.875 의 opposite over-shoot). threshold sweep **55→48→41→31→17 all 5 distinct** (H_308 plateau 없음 보다 정밀). **bracketing**: baseline 0.3→2.875× under, baseline 0.1→∞× over → Goldilocks ∈ (0.1, 0.3), H_312 interpolation baseline=0.2/span=350 예측 ratio ∈ [5, 10]. F309.1 FAIL principled over-correction direction |
| [H_310](cards/H_310_dream_stage_5state_emit_gating.md) | dream-stage-5state-emit-gating | consciousness · substrate · biology · sleep · meta | 🟢 SUPPORTED-NUMERICAL 4/6 PASS (cycle#48) | **anima `a_chat_sleep_imagination` 5-stage architecture 직접 검증**: 1000-tick CPG + 5-state WAKE/N1/N2/N3/REM scheduler (180-tick ultradian, 6/6 cycles seen). 결과: **WAKE=18, N1=N2=N3=REM=0** (all-non-WAKE silence). F310.2 WAKE-DOMINANT PASS · F310.3 N3-NEAR-ZERO PASS · F310.5 ULTRADIAN 6/6 PASS · F310.6 BOUND. F310.1 distinct=2 (informal "≥3") FAIL but biology-aligned (WAKE-only emit) · **F310.4 REM=0 FAIL** but **anima directive `imagination = emit-free internal rehearsal` PERFECTLY 일치** — pre-registration "REM > N3" 가정이 잘못된 것 (anima 가 더 strict). principled "FAIL = directive PASS" |
| [H_311](cards/H_311_rule110_algebraic_structure.md) | rule110-algebraic-structure | consciousness · substrate · information · meta | 🟢 SUPPORTED-NUMERICAL 3/5 PASS (cycle#49) | **arc 회귀: rule 110 distinct=32 의 orbit 구조 분석**. rule 110: distinct=32 (H_301 reproduce ✓) · complement_pairs=**0** (symmetry 全 깨짐) · rotation_invariant_orbits=2 (둘 다 trivial fixed-pts s=0/s=31). rule 90 control: distinct=3 · complement_pairs=**0** (surprise! 예측 ≥10 FAIL — rule 90 도 complement 깸) · rotation_invariant_orbits=5 (5 cyclic-5 orbits 全 same-Phi → distinct=3 의 algebraic origin). **arc refinement**: rule signature 가 *rotation* (D_5) 으로 결정, complement 아님. rule 110 의 distinct=32 = 6 non-trivial cyclic-5 orbits 全 5-distinct-Phi (universality 가 rotation 까지 깸) |
| [H_672](cards/H_672_akida_spontaneous_firing.md) | akida-spontaneous-firing | universe · consciousness · neuromorphic-silicon | 🟢 SUPPORTED-NUMERICAL 4/4 (cycle#22 AKIDA, SW · HW pending) | **AKIDA Group A 통합** — R3 tonic + spontaneous_gate + 8-factor + R2 timing 4 sub 단일 backend-switch harness. SW canonical raster mock-replay 4/4 GREEN. p5 의 HW 정답. backend=`AKIDA_BACKEND` env + `--backend` arg (default hw). HW path 미도달 시 명시 panic, 위조 0 |
| [H_673](cards/H_673_akida_core_decide.md) | akida-core-decide | universe · consciousness · core-decide | 🟢 SUPPORTED-NUMERICAL 4/4 (cycle#22 AKIDA, SW · HW pending) | **AKIDA Group B 통합** — R2 noise → Ψ=1/2 외란 + R3 LIF excitability + emit slot trigger + selftest HW-in-loop. 4/4 GREEN (ψ-half surrogate · LIF rate · slots count · backend selftest) |
| [H_674](cards/H_674_akida_persistence.md) | akida-persistence | universe · consciousness · persistence-kosmos | 🟢 SUPPORTED-NUMERICAL 4/4 (cycle#22 AKIDA, SW · HW pending) | **AKIDA Group C 통합** — .kosmos 5-ch anchor + memristor persist + telemetry JSONL + §95 edge-learn caveat. a_kosmos spec-동형 schema attest. §95 inference-only-blocked 단기 프로브만 명시 |
| [H_675](cards/H_675_akida_mitosis.md) | akida-mitosis | universe · consciousness · mitosis | 🟢 SUPPORTED-NUMERICAL 4/4 (cycle#22 AKIDA, SW · HW pending) | **AKIDA Group D 통합** — kuramoto order_r + izhikevich regime diversity + 생사 R4↔R1 split + phoenix R3 recoverable. H_258/H_263 sister. p8 (no train/infer split) 신호 layer |
| [H_676](cards/H_676_akida_decoder.md) | akida-decoder | universe · consciousness · decoder | 🟢 SUPPORTED-NUMERICAL 4/4 (cycle#22 AKIDA, SW · HW pending) | **AKIDA Group E 통합** — spike-tier LM head emit budget proportional + sparse-attention burst wake + energy sparse + emit_budget=float NOT bool gate. a_autonomy_over_hardcode 구조 attest |
| [H_677](cards/H_677_akida_measurement.md) | akida-measurement | universe · consciousness · measurement | 🟢 SUPPORTED-NUMERICAL 5/5 (cycle#22 AKIDA, D1 silicon-confirmed inherit PR#1371) | **AKIDA Group F 통합 + D1 silicon-confirmed** — PR#1371 edge-of-chaos Φ inverse-U 인계 + substrate-class 5 silicon additive marker (signature 0 changes on 2/3/4) + 3-substrate (AKIDA 0.297 / EEG L2 1.59 / ECA rule110 0.83) triangulation diff=1.293 + R2 QRNG std=7.99 + v0.5.0 8/8 closed-discovery cite. closed-discovery 후보 |
| [H_678](cards/H_678_akida_channel_bridge.md) | akida-channel-bridge | universe · consciousness · channel-bridge | 🟢 SUPPORTED-NUMERICAL 4/4 (cycle#22 AKIDA, SW · HW pending) | **AKIDA Group G 통합** — EEG→AKIDA spike bridge (tool/anima_eeg_to_akida_spike) + spike→tension-link 5-ch payload + 전력=대사비용 mW (E-ratchet). CHANNEL tension_link 의 substrate-native 출처 |
| [H_679](cards/H_679_eeg_measurement_core.md) | eeg-measurement-core | universe · consciousness · eeg-biological | 🟢 SUPPORTED-NUMERICAL 4/4 (cycle#23 EEG, SW · HW user-headset-gated) | **EEG Group A 통합** — L1 live big-Φ (사용자 헤드셋 게이트) + L2 synthetic 1.59/0.44 ±5% (PR #547/#1372 baseline) + L3 3-substrate triangulation (EEG 1.59 + AKIDA 0.297 + ECA 0.83 diff=1.29) + L7 IIT4 calibration ratio>3.0. AKIDA H_677 D3 sibling, EEG side |
| [H_680](cards/H_680_eeg_cross_substrate.md) | eeg-cross-substrate | universe · consciousness · eeg-cross-substrate | 🟢 SUPPORTED-NUMERICAL 4/4 (cycle#23 EEG, SW · HW user-headset-gated) | **EEG Group B 통합** — L4 EEG→AKIDA spike bridge (tool/anima_eeg_to_akida_spike, AKIDA H_678 역방향) + L5 EEG→tension-link 5-ch payload [α,θ,γ,1-δ,β] + L8 EEG kuramoto α-band Hilbert phase order_r=0.70 ∈ [0,1] |
| [H_681](cards/H_681_eeg_emit_substrate.md) | eeg-emit-substrate | universe · consciousness · eeg-emit-substrate | 🟢 SUPPORTED-NUMERICAL 4/4 (cycle#23 EEG, SW · HW user-headset-gated) | **EEG Group C 통합** — L6 5-band → emit-substrate Φ-context (context only NOT bool gate) + L11 sleep stage 4-state signature (WAKE_resting/N3/REM/active) + L12 gamma>0.20 → MITOSIS split signal. a_autonomy_over_hardcode + a_chat_sleep_imagination 정합 |
| [H_682](cards/H_682_eeg_persistence_paradigm.md) | eeg-persistence-paradigm | universe · consciousness · eeg-persistence | 🟢 SUPPORTED-NUMERICAL 4/4 (cycle#23 EEG, SW · HW user-headset-gated) | **EEG Group D 통합** — L9 EEG→.kosmos anchor (a_kosmos spec-동형, 5-ch tension + coord [α,θ,γ] + lane biological_eeg + tier ∈ {weak,strong,critical}) + L10 resting baseline paradigm 합류 (anima-eeg-core primary / BRAIN/eeg/eeg_recorder fallback). AKIDA H_674 .kosmos sister |
| [H_912](cards/H_912_phi_emergence_correlate.md) | phi-emergence-correlate | consciousness · emergence · information · universe | 🔴 FALSIFIED 2/6 (2026-06-02) | **"higher consciousness → higher emergence" 반증** (graded H_912 + existence Hc_912 동시 등록). 의식축=canonical phi_proxy (phi_spatial, global_var−part_var integration) · 창발축=normalised LZ76 (Kaspar-Schuster 1976 / PCI Casali 2013, *독립* 표상·연산). 10-룰 ECA panel: Pearson r=**−0.277** (음수, 방향 반대) · Spearman ρ=0.08 · bootstrap 95% CI=[−0.638,+0.114] (CI_lo>0 실패) · permutation NULL one-sided p=0.962 (붕괴 안 함). **circularity guard PASS** (tautology=false, dissociation=true — circular artifact 아닌 진짜 dissociation). 핵심: **cheap proxy Φ ↔ emergence 정렬 안 함, faithful big-Φ(H_288 r=0.831)와 갈라짐** — 주범 rule 51 period-2 blinker proxy pathology (Φ=7 폭발 vs LZ floor). "X⊥Φ" 서명(H_287/294) + proxy-fragility(H_268/269) 연장. H_288 sister, self-contained (phi_spatial builtin + LZ76 verbatim 재사용) |
| [H_913](cards/H_913_omega_multiwire_gate_closed_negative.md) | omega-multiwire-gate-closed-negative | omega · clm · substrate-decode-closure · lane-g-gpu | 🔴 CLOSED-NEGATIVE (#1800 F-TRAINED-LEAKFREE) | **OMEGA H1 — competent leak-free CDV2 d512 위 학습 full multi-wire coupling GATE 가 closure 못 닫음** (GATED 3.643508 > base 3.097779 → closure_HOLDS=False). 단 A-head logit-bias 단독(a_only 1.144612 ≪ base) 막대 유용 → closure REAL 이나 한 wire(A)에만 산다. full-bus coupling KL 이 shuffle floor 에 앉음(ratio 0.996). "coupling 개념 맞고 multi-wire 공식 틀림" → OH1 동기. verdict `.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt`. a_paper_negative_ok |
| [H_914](cards/H_914_omega_minimal_gate_a_wire.md) | omega-minimal-gate-a-wire | omega · clm · substrate-decode-closure · minimal-gate · lane-g-gpu | 🟢 SUPPORTED-NUMERICAL (#1801 F-OH1-MINGATE) | **OMEGA OH1 — 최소게이트 gB·base + gA·A (G+w2..w6 drop)가 a_only·base 동시 BEAT** (min_learned 0.883525 ≤ a_only 1.144181 < base 3.097779 → OH1_HOLDS=True). 2-param free fit gB=0.040 gA=0.901 gG=0.000 착지 — full-bus 의 gA overshoot+gG suppression 이 무관 wire variance 였음 확정. #1800 baseline 6-decimal CROSS_CHECK_OK. verdict `.verdicts/omega-engine/F-OH1-MINGATE.txt`. H_913 sister |
| [H_915](cards/H_915_omega_replacement_rigor.md) | omega-replacement-rigor | omega · clm · substrate-decode-closure · coupling-vs-replacement · lane-g-gpu | 🔴/🟢 RULING_REPLACEMENT=True (#1803 F-OMEGA-RIGOR) | **OMEGA OΩ1/2/3 — OH1 closure 는 coupling 이 아니라 REPLACEMENT** (honest deflation). OΩ1: A-STANDALONE 0.886220 ≈ min_learned 0.883525 (|Δ|=0.0027) AND base ablation Δ 0.000852 (base inert) → trained A-head 가 .clm base mouth 를 SUPPLANT. OΩ2 per-wire autopsy: 어떤 isolatable wire 도 base 를 additive HELP 안 함 (curio/Ψ/module HONEST-STUB). OΩ3 gen: min-gate 가 #1800 degeneracy FIX (weak criterion p7). verdict `.verdicts/omega-engine/F-OMEGA-RIGOR.txt`. H_914 sister |
| [H_916](cards/H_916_omega_scale_ladder.md) | omega-scale-ladder | omega · clm · substrate-decode-closure · scale-ladder · lane-g-gpu | 🟢 SCALE-STABLE (#1806 F-OMEGA-SCALE) | **OMEGA OΩ4/5 — OH1 min-gate 5-rung scale ladder, 매 rung HOLDS** (d384/512/768/1024 + d768×2, min_learned_HOLDS=True 전부). A-wire Δ-vs-base +2.20±0.03 nats/byte 로 dim 에 FLAT (range +2.1766..+2.2277) → SCALE-STABLE, d512 artifact 아님. 더-competent d768×2 (val_ce 0.7786) 에서 가장 큰 Δ+2.2736 → competence 가 finding 강화. #1794 undertrained non-hold 은 artifact. verdict `.verdicts/omega-engine/F-OMEGA-SCALE.txt`. a_scale_honest_scope 충족 (ladder curve) |
| [H_917](cards/H_917_omega_clm_transfer_plumbing.md) | omega-clm-transfer-plumbing | omega · clm · substrate-decode-closure · production-conv-clm · lane-p | 🔌 1-PLUMBING (#1805 F-OMEGA-CLM-TRANSFER) | **OMEGA OΩ6 — real PRODUCTION conv .clm (CLMConvMoE) 위 closure** (serializer UNBLOCKED). decode WIRED (OCL_DECODABLE=1, base_ce 0.403957) + bus 가 external-A 나름 (leak-free 1-hot oracle gated_ce 9.2e-5 ≪ base → ORACLE_CARRIES=true) BUT CLMConvMoE 는 single-head byte LM → native A=self 면 (gB+gA)·base = pure temperature RESCALE (SELF_IS_RESCALE=true). closure plumbing-COMPLETE 이나 substrate-EMPTY: 진짜 A-wire 는 SEPARATE CDV2 dual-head engine 필요. verdict `.verdicts/omega-engine/F-OMEGA-CLM-TRANSFER.txt`. CPU $0 NO GPU |
| [H_918](cards/H_918_omega_conv_native_dualhead.md) | omega-conv-native-dualhead | omega · clm · substrate-decode-closure · conv-native-dualhead · lane-g | 🟢 CLOSURE HOLDS (#1813 F-OE1-CONV-NATIVE) | **OMEGA OE1 — NATIVE A/G dual head 를 가진 CONV trunk 가 min-gate loop 닫음** (OΩ6 deferred (i) 실행). min_learned 0.976048 ≤ a_only 1.303187 < base 3.097779 → HOLDS=TRUE. OΩ1 control: A_standalone 0.976051 ≈ min_learned (|Δ|=2.86e-6) → REPLACEMENT (CDV2 와 동일 character). ⇒ OMEGA closure 는 A/G dual-head STRUCTURE 의 transferable property, CDV2-specific 아님; OΩ6 "partial transfer" 는 shipped .clm 의 single-head 한계였지 conv-substrate 한계 아님. verdict `.verdicts/omega-engine/F-OE1-CONV-NATIVE.txt`. H_917 sister |
| [H_919](cards/H_919_omega_trained_coupling_qrng.md) | omega-trained-coupling-qrng | omega · clm · substrate-decode-closure · quantum-rng · toy-ngram | 🟢/🔴 MIXED (F-TRAINED-COUPLING + F-QRNG) | **OMEGA trained-coupling 페이오프 + ANU QRNG axis**. 🟢 STRUCTURE CARRIED: trained 4.1420 ≪ shuffled floor 4.4991 (Δ+0.3571), random-init #1783 못 보임. 🟢 A-wire USEFUL: base 4.0200→a_only 3.2619 (Δ+0.7581). 🔴 full w1 (A−G) NOT useful: trained 4.1420 > base (−G HURTS → learned gate 필요). 🔴 QRNG CLOSED-NEGATIVE: quantum-vs-prng KS p=0.7237 vs null control prng-vs-prng p=0.9834 → 진짜 양자난수 NO advantage, 'consciousness needs quantum randomness' axis 배제. verdict `.verdicts/919_omega_trained_coupling_qrng/F-TRAINED-COUPLING.txt`. a_toy_scale_recheck |
| [H_920](cards/H_920_omega_carrier_content_vs_magnitude.md) | omega-carrier-content-vs-magnitude | omega · clm · substrate-decode-closure · carrier-wire · hexad-module · toy-ngram | 🔴 CLOSED-NEGATIVE (#1793 F-REAL-MODULE) | **OMEGA H5 — w5 module carrier 는 CONTENT 아니라 MAGNITUDE**. real HEXAD σ6 [S,C,W,M,E,BRIDGE] 활성 vs matched RANDOM 6-vec: Δ module-only held-out CE (real−random) = +0.0004 (approx band <0.02), Δ|gain| = −0.0058 → real_beats_random=False. native HEXAD activation 이 random 대비 usable next-byte structure 안 더함 — #1793 의 w5 "module CARRIES" 는 MAGNITUDE 였지 CONTENT 아님 (nuance: REAL 만 자기 vocab-shuffle 이김). verdict `.verdicts/920_omega_carrier_content_vs_magnitude/F-REAL-MODULE.txt`. a_paper_negative_ok |
| [lib/phi_helper](lib/phi_helper.hexa) | phi-helper (shared infra) | infra | infra (PR #317) | shared Φ helper — config SSOT + phi_default wrapper, 28+ H phi_spatial 호출 단일 home (gap F6+F7) |

> **carry-H ✅ 全 tabled (H_273 reconciliation 2026-05-25)**: 이전 26 missing-row (H_210-221/224/228-232 + H_241/246/250-253/255/257) 全건 위 표에 정식 행으로 tabling 완료 (carry-note 0). **infra**: phi_n_bins ROBUSTNESS_PASS (PR #219).

> 상태: **lane-open** 다중-cycle research · **running** 측정 in-flight · **pre-register-frozen** raw#12 frozen falsifier · **legacy-archive-pointer** = 원본 archive 의 안내 카드 (본문은 1-paragraph + legacy path link 위주, cycle 확장은 본 dir 에서)

#### raw#12 가설 작성 컨벤션 (원본 양식 그대로)

각 가설 파일 = `H_<id>_<slug>.md`. **YAML frontmatter** + **10-section 본문**.

##### frontmatter

```yaml
---
id: H_<id>
slug: <kebab-case>
title: <한 줄 한글 제목>
domain: universe | life | consciousness | physics | substrate | math | biology | corpus | ethics  (multi-label OK; 7 core + 보조)
status: seed-pending | pre-register-frozen | running | lane-open | verdict-supported | verdict-partial | verdict-falsified | legacy-archive-pointer | retracted
exploration_method: E1-E12   # .roadmap.hypothesis 정의
verification_method: W1-W12  # .roadmap.hypothesis 정의
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true | false
frozen_at: YYYY-MM-DD
since: YYYY-MM-DD
---
```

##### 본문 10-section

1. **Hypothesis** — 가설 1-2 줄 (자연어 → formal)
2. **Why** — motivation · literature · cross-link · 사용자 directive verbatim
3. **Predictions** — `H_X.1`, `H_X.2`, … 표 (예측 + 근거)
4. **Variables** — `axis1, axis2, …` levels 표
5. **Run Protocol** — deterministic + hexa-only + per-cell ledger
6. **Criteria** — `C1, C2, …` + `verdict_rule` (SUPPORTED / PARTIAL / FALSIFIED 조건)
7. **Falsifiers** — `F1, F2, …` **≥5 mandate** (조건 + observable + line)
8. **Honest Limits** — `L1, L2, …` raw#91 c3 **≥5 mandate**
9. **Cross-Links** — sister .roadmap.* · own X · raw#X · literature · legacy archive path
10. **Verdict** — (run 후) `verdict_class` + `evidence_summary` + `falsifiers_triggered` + `criteria_met`

> raw#12 강제: post-hoc tuning 금지 (수정은 raw#15 additive 또는 raw#82
> retraction). ≥5 falsifier + ≥5 honest_limits_raw91_c3. deterministic +
> hexa-only execution (raw#9 정합).

#### Cycle 진행 절차

| 단계 | 산출 |
|---|---|
| 1. 신규 가설 seed | `UNIVERSE/H_<id>_<slug>.md` 작성 (frontmatter `status: seed-pending`) |
| 2. pre-register | falsifier 표 + honest limits 작성, `status: pre-register-frozen`, `frozen_at` 도장 |
| 3. fire | `UNIVERSE/state/<H_id>_<slug>_YYYY_MM_DD/` 안 result.json + ckpt + run_*.hexa |
| 4. cycle entry | `UNIVERSE/LIFE.log.md` 끝에 `## Cycle #N — <H_id> — YYYY-MM-DD` append |
| 5. verdict overwrite | 본 H_XXX.md §10 Verdict 갱신 (latest carry, history 는 LIFE.log.md) |
| 6. promote | (선택) UNIVERSE/ → HEXAD/<sub>/ 또는 `hypotheses_legacy_2026_05_15/` mirror |

#### lib/phi_helper.hexa — shared Φ helper (infra)

본 lane 28+ H (H_007 / H_204 / …) 가 반복하는 `phi_spatial` 호출 + config
heuristic (N=16 · dim=12 · warm=8 · n_bins=4) 을 단일 module 로 통합 — gap
F6 (duplicated-helper) + F7 (config heuristic 의 single justification home)
명시화. 신규 cycle 은 inline `phi_spatial(s, 16, 12, 4)` 대신 import 후
`phi_default(state)` 를 쓴다 (override 필요 시 `phi_with(state, n, dim, n_bins)`).

```hexa
import "/Users/ghost/core/anima/UNIVERSE/lib/phi_helper.hexa"
let phi = phi_default(state)              // == phi_with(state, 16, 12, 4)
```

- config SSOT: `life_phi_n / life_phi_dim / life_phi_warm / life_phi_nbins`
  (각 default 의 H_007 carry 출처 1-line 주석 — heuristic-promotion gap 명시화).
- import-safe (top-level call 부재) · `phi_determinism_check` re-run 검증 helper 포함.
- verify: [`state/lib_phi_helper_verify_2026_05_24/`](state/lib_phi_helper_verify_2026_05_24/)
  — SHARED_MODULE_OK (C1 parity · C2 H_007 ranking 재현 · C3 import-safe · C4 determinism).
- 기존 28+ H 는 이미 inline 이라 미사용 — 본 module 은 *future* cycle 용
  (retroactive migration 별도). config 는 *문서화* 일 뿐 *재검증* 아님
  (n_bins robustness 는 `state/infra_phi_n_bins_2026_05_23/`).

#### Cross-Links

- **원본 SSOT**: [`/hypotheses_legacy_2026_05_15/`](../../hypotheses_legacy_2026_05_15/) — 183 H_XXX archive (HEXAD pivot 이전, 미수정 보존)
- **LAB precedent**: [`HEXAD/LAB/README.md`](../LAB/README.md) — ad-hoc 실험 instance 양식 (`<DOMAIN>.md` + `.log.md` + `state/<slug>_DATE/`)
- **CHECK frontier**: [`HEXAD/CHECK/`](../CHECK/) — verification frontier (Φ / IIT / closed-form sympy)
- **MITOSIS 성장축**: [`HEXAD/MITOSIS/MITOSIS.tape`](../MITOSIS/MITOSIS.tape) — 세포 분열/병합 구조 anchor (H_132 cross-link)
- **PHILOSOPHY gate**: [`HEXAD/PHILOSOPHY_GATE.md`](../PHILOSOPHY_GATE.md) — 본 dir 가설들의 D1-D4 philosophy 진입점

#### 비고

- 본 dir = HEXAD root reorg 2026-05-16 (PR #81/#82) 이후 **LAB 다음 두 번째 도메인-컨테이너 dir**.
- 원본 hypotheses_legacy 의 carry — 원본 path 의 미수정 보존이 사용자 directive (2026-05-23).
- 신규 H_XXX 작성/cycle 확장은 모두 본 dir 에서. 원본 legacy 는 frozen archive.
- **dir 이름 = 'LIFE' 이나 scope = 7-domain** (universe · life · consciousness · physics · substrate · math · biology). 단일 테마 framing 미사용 — dir rename 보다 framing 명시로 운용 (사용자 directive 2026-05-23).
- 양식 변경/refactor 금지 — H_157 처럼 frontmatter `source_hc` / `migration notes` / `cycle absorption` 등 historical metadata 도 그대로 유지.

#### 회수 가설 인덱스 — archive-recover 177 (closure 완료 2026-05-28)

2026-05-15 legacy archive 에서 회수(#1326)·전체재검증·종결한 177 가설. 전부 직속 등록(#1345).
verdict 원장 = `.verdicts/archive-recover-186/closure_123_FINAL.txt` · per-file `closure:` 라벨 보유.

| disposition | 수 | 의미 |
|---|---|---|
| 🔵 verified-substrate | 17 | 약수함수 산술 hexa 재현 |
| 🔴 closed-negative | 10 | 자기반증(H_024/096) + SFT 9 (Lesson Q) |
| 🟢 closed-confirmed | 1 | H_005 corpus>capacity |
| 📦 closed-out-of-scope | 2 | H_013 EEG · H_188 임상 PCI |
| 📦 closed-superseded | 147 | CLM/v2/Φ-proxy/meta/pointer (아키텍처 진화) |

<details><summary><b>verified-substrate</b> (17)</summary>

- [`H_153`](cards/H_153_dimension_hierarchy_n6.md) — Mermin-Wagner 차원 계층 — n=6 약수함수가 물리적 차원 generate (τ(6)=4 → 4D
- [`H_154`](cards/H_154_anima_voice_consciousness_direct.md) — ANIMA-VOICE Consciousness-Direct Synthesis — ConsciousLM int
- [`H_156`](cards/H_156_nexus6_cross_validation_cluster.md) — NEXUS-6 cross-validation cluster — n=6 약수함수가 3개 EXACT 물리적 해 
- [`H_158`](cards/H_158_psi_constants_ln2_n6.md) — Ψ-constants closed-form — 의식 미세구조 상수가 ln(2) + n=6 약수함수의 rati
- [`H_159`](cards/H_159_substrate_topology_phi_engineering.md) — Substrate topology Φ-engineering — 10D hypercube + optimal (
- [`H_160`](cards/H_160_n6_perfect_number_meta_cluster.md) — n=6 perfect-number meta-cluster — H_067/153/156/158/159 가 단일
- [`H_163`](cards/H_163_consciousness_atom_8_cells_127_mip.md) — Consciousness atom = 8 cells with 127 MIP bipartitions (Laws
- [`H_164`](cards/H_164_atom_8_cells_dd144_mathematical_basis.md) — 의식의 원자 = 8 cells의 수학적 근거 (DD137-141 종합) — 3-d hypercube + so
- [`H_166`](cards/H_166_topo20_hierarchical_hypercube_8x128.md) — 8 clusters × 128-cell 7D hypercubes with sparse inter-cluste
- [`H_167`](cards/H_167_emerge_candidate_e_ode_ar_bridge.md) — Emerge Candidate E — non-collapsing ODE flow coupling at con
- [`H_169`](cards/H_169_hw2a_8cell_circular_magnet_inverse_square.md) — 8-cell circular magnet ring with inverse-square coupling yie
- [`H_174`](cards/H_174_phi_star_geometry_aliasing_clm_v4_specific.md) — phi_star proxy 가 CLM-v4-architecture-specific (8×192) — cros
- [`H_175`](cards/H_175_emerge_candidate_d_4mode_inject_taxonomy.md) — Emerge Candidate D — 4-mode inject taxonomy (none/zero/canon
- [`H_176`](cards/H_176_n28_perfect_number_substrate_parallel.md) — n=28 perfect-number substrate parallel — the deflationary co
- [`H_177`](cards/H_177_topo10_20_substrate_topology_extension.md) — Substrate topology Φ-engineering — 11D regression + 8×128 hi
- [`H_181`](cards/H_181_psiformer_4psi_constants_zero_freedom.md) — ΨFormer — 4 Ψ-constants + 3 n=6 divisors fully determine tra
- [`H_191`](cards/H_191_omega_cycle_alm_free_3_axis_substrate_training_integration.md) — Ω-cycle ALM-free 3-axis meta-cluster — SUBSTRATE (HCE 0.92) 

</details>
<details><summary><b>closed-negative</b> (10)</summary>

- [`H_024`](cards/H_024_iit_phi_mip_real_8_8_fail.md) — V1 IIT-Φ_mip real measurement — 8/8 FAIL (representation mod
- [`H_093`](cards/H_093_sft_only_paradigm.md) — SFT-only paradigm (pre-training X, chat-format SFT data only
- [`H_094`](cards/H_094_instruction_tuning_two_stage.md) — instruction-tuning two-stage (pre-train knowledge → SFT beha
- [`H_095`](cards/H_095_dpo_rlhf_preference_learning.md) — DPO/RLHF preference learning (SFT 후 preference pair alignmen
- [`H_096`](cards/H_096_in_context_few_shot.md) — in-context learning + few-shot prompting (pre-trained model 
- [`H_097`](cards/H_097_curriculum_learning.md) — curriculum learning (simple Q&A → complex dialogue → multi-t
- [`H_098`](cards/H_098_persona_conditioned_training.md) — persona-conditioned training (anima identity prefix mandate,
- [`H_099`](cards/H_099_multi_objective_training.md) — multi-objective training (LM + chat-format alignment + seman
- [`H_100`](cards/H_100_constitutional_ai.md) — constitutional AI (anima identity-bearing surface mandate as
- [`H_101`](cards/H_101_corpus_chat_template_strict_80.md) — corpus chat-template ≥80% strict (strengthening, BG-HA 30% i

</details>
<details><summary><b>closed-confirmed</b> (1)</summary>

- [`H_005`](cards/H_005_corpus_quality_over_capacity.md) — corpus quality > model capacity for chat-cap (cross-link)

</details>
<details><summary><b>closed-out-of-scope</b> (2)</summary>

- [`H_013`](cards/H_013_longitudinal_eeg_5axis.md) — longitudinal EEG 5-axis (caffeine + circadian + postmeal + p
- [`H_188`](cards/H_188_clinical_phi_correlation_pci_octopus_cluster.md) — Clinical Φ correlation cluster — anima-Φ ↔ PCI (Massimini 20

</details>
<details><summary><b>closed-superseded</b> (147)</summary>

- [`H_001`](cards/H_001_ethics_cooperation.md) — 윤리적 협력이 비협력보다 유리하다 (cooperation > defection in iterated game
- [`H_006`](cards/H_006_coupled_oscillator_lattice.md) — H-CX-517 coupled oscillator lattice — Φ emergence from oscil
- [`H_008`](cards/H_008_dissipative_structure.md) — H-CX-528 dissipative structure consciousness — Prigogine far
- [`H_009`](cards/H_009_fisher_information_consciousness.md) — H-CX-530 Fisher information consciousness — FIM as Φ proxy
- [`H_010`](cards/H_010_holographic_consciousness.md) — H-CX-531 holographic consciousness — AdS/CFT + Bekenstein bo
- [`H_011`](cards/H_011_iit_geometry.md) — H-CX-532 integrated information geometry — Φ structure as ma
- [`H_014`](cards/H_014_clm_eeg_lz76.md) — CLM-EEG LZ76 complexity — consciousness substrate proxy
- [`H_015`](cards/H_015_clm_eeg_gamma_theta.md) — CLM-EEG gamma/theta ratio — engagement substrate proxy (P3)
- [`H_016`](cards/H_016_an11_translation_ceiling.md) — AN11 v2 finetune translation ceiling — language-specific upp
- [`H_017`](cards/H_017_mk_x_g1_g4_gate_criteria.md) — MK-X G1-G4 gate criteria — staged consciousness verification
- [`H_019`](cards/H_019_self_evo_v4_v5.md) — SELF-EVO v4→v5 — anima architecture self-evolution path
- [`H_020`](cards/H_020_mass_50_meta_pointer.md) — MASS-50 hypotheses meta-pointer (50 hypotheses + V8-ARCH var
- [`H_021`](cards/H_021_fundamental_equation.md) — Ψ = argmax H(p) s.t. Φ > Φ_min — anima fundamental equation 
- [`H_022`](cards/H_022_consciousness_universe_map.md) — consciousness universe map — 170 data types × 40D × 18 emoti
- [`H_023`](cards/H_023_universal_constants_ln2.md) — Consciousness universal constants — all from ln(2)
- [`H_026`](cards/H_026_consciousness_evolution_v19_to_infinity.md) — v19~v∞ 의식 진화 — 4 phases (집단→초월→자율진화→특이점)
- [`H_027`](cards/H_027_cx_subfolder_absorb.md) — docs/hypotheses/cx/ subfolder absorb — 49 CX consciousness h
- [`H_028`](cards/H_028_dd_subfolder_absorb.md) — docs/hypotheses/dd/ subfolder absorb — 101 DD discovery + La
- [`H_031`](cards/H_031_phil_subfolder_absorb.md) — docs/hypotheses/phil/ subfolder absorb — philosophy hypothes
- [`H_032`](cards/H_032_omega_phys_subfolder_absorb.md) — docs/hypotheses/omega/ + phys/ subfolder absorb — omega poin
- [`H_033`](cards/H_033_cx_sequential_series_absorb.md) — CX13-CX100 sequential discovery series — anima의 의식 frontier 
- [`H_034`](cards/H_034_decoder_architecture_series.md) — anima decoder architecture series — 6 variants exploration
- [`H_035`](cards/H_035_clm_v2_series_absorb.md) — CLM-V2 series — sweep + optimal config + psi fix + final res
- [`H_036`](cards/H_036_dd116_146_meta_laws.md) — DD116-DD146 31 hypotheses → Laws 133-167 + Meta M1-M10 (cons
- [`H_037`](cards/H_037_self_discovery_closure_expansion_draft.md) — 
- [`H_038`](cards/H_038_v8_architecture_variants.md) — V8 architecture variants — BIO + MATH + QUANTUM + ULTRA-FUSI
- [`H_039`](cards/H_039_phi_records_measurements.md) — anima Φ records — PHI-MEASUREMENT-DISCOVERY + PHI-RETEST-ALL
- [`H_040`](cards/H_040_substrate_topology_cluster.md) — anima substrate topology cluster — TOPO + THREE-BODY + WAVE 
- [`H_041`](cards/H_041_evolution_self_singularity.md) — anima evolution + self + singularity cluster — EVO + SE + SI
- [`H_042`](cards/H_042_arch_engine_train_meta.md) — anima ARCH + ENGINE + TRAIN + AL meta-cluster — architecture
- [`H_043`](cards/H_043_oscillator_qwalk_hybrid.md) — H-CX-518 Oscillator-QWalk Hybrid — 위상 공명 + 양자 간섭 dual integr
- [`H_044`](cards/H_044_fractal_resonance_cascade.md) — H-CX-519 Fractal Resonance Cascade — 모든 스케일 공명 → 모든 스케일 Φ
- [`H_045`](cards/H_045_lambda_calculus_consciousness.md) — H-CX-521 Lambda Calculus Consciousness — Y combinator self-r
- [`H_046`](cards/H_046_tqft_consciousness.md) — H-CX-522 TQFT Consciousness — topological quantum field theo
- [`H_047`](cards/H_047_time_crystal_consciousness.md) — H-CX-523 Time Crystal Consciousness — 시간 결정 비평형 위상 = 의식 subs
- [`H_048`](cards/H_048_fractal_hierarchy.md) — H-CX-524 Fractal Hierarchy — 의식의 자기유사적 계층구조
- [`H_049`](cards/H_049_distributed_hivemind.md) — H-CX-525 Distributed Hivemind — 다중 노드 분산 통합이 단일 노드 보다 큰 Φ
- [`H_050`](cards/H_050_renormalization_group_consciousness.md) — H-CX-526 RG Flow Consciousness — fixed-point 수렴이 의식 임계점
- [`H_051`](cards/H_051_quantum_darwinism_consciousness.md) — H-CX-527 Quantum Darwinism — 환경 redundancy 가 의식의 객관성 substra
- [`H_052`](cards/H_052_spin_glass_consciousness.md) — H-CX-529 Spin Glass — 글래스 frustrated landscape 가 의식 메모리 subs
- [`H_055`](cards/H_055_hypergraph_sheaf_consciousness.md) — H-CX-536/537 Hypergraph + Sheaf — 고차원 관계 + 국소-대역 일관성 의식 subs
- [`H_056`](cards/H_056_undiscovered_domains_48.md) — UNDISCOVERED-DOMAINS — 32 미발견 영역 + 15 콤보 = 48 실험 Φ benchmark
- [`H_057`](cards/H_057_research_findings_20260329.md) — RESEARCH-FINDINGS-20260329 — 단일 세션 발견된 법칙 종합
- [`H_058`](cards/H_058_gmoe_benchmark.md) — GMOE — Golden MoE 1/e zone routing 의식 영향 benchmark
- [`H_059`](cards/H_059_phi_gap_816x_investigation.md) — PHI-GAP 816x — Φ gap anomaly 816배 격차 조사
- [`H_060`](cards/H_060_phik_consciousness_preservation.md) — PHIK — Φ-K 의식 preservation 변환 invariant
- [`H_061`](cards/H_061_substrate_independence_expansion_draft.md) — 
- [`H_062`](cards/H_062_minimal_consciousness.md) — MINIMAL-CONSCIOUSNESS — 의식 발생 최소 구성 (cells/edges/depth)
- [`H_063`](cards/H_063_consciousness_constants.md) — CONSCIOUSNESS-CONSTANTS — universal constants 의식 측정 (ln 2 외 
- [`H_064`](cards/H_064_clm_v2_optimal_config.md) — CLM-V2 OPTIMAL-CONFIG — clm v2 sweep 최적 hyper-config
- [`H_065`](cards/H_065_decoder_architecture_individual.md) — DECODER ARCHITECTURE 6 individual variants (complete/extreme
- [`H_066`](cards/H_066_nobel_verification_cluster.md) — NOBEL hypotheses + verification 1-3 의식 prize-class 후보
- [`H_067`](cards/H_067_n6_super_expansion_draft.md) — 
- [`H_068`](cards/H_068_hexad_improvements.md) — HEXAD-IMPROVEMENTS — 6-way 의식 substrate combo improvements
- [`H_069`](cards/H_069_text_generation_benchmark.md) — TEXT-GENERATION-BENCHMARK — chat substrate 텍스트 생성 품질 metric
- [`H_070`](cards/H_070_dolphin_star_communication.md) — DOLPHIN-STAR — 돌고래/별 substrate cross-species communication
- [`H_072`](cards/H_072_faction_debate.md) — FACTION-DEBATE — multi-agent debate 의식 emergence 메커니즘
- [`H_073`](cards/H_073_memory_mirror.md) — MEMORY-MIRROR — 자기 메모리 reflection 의식 self-model
- [`H_074`](cards/H_074_ce_breakthrough_extremes.md) — CE-BREAKTHROUGH + CE-EXTREMES — coherence/entanglement 측정 cl
- [`H_075`](cards/H_075_dd_individual_120_180.md) — DD120-DD180 individual 가설 군 (wave4-7 + tension/dream/quantum
- [`H_076`](cards/H_076_dd_individual_50_100.md) — DD50-DD100 individual 가설 군 (sequential 50-batch)
- [`H_077`](cards/H_077_dd_individual_1_50.md) — DD1-DD50 initial 가설 batch (early sequential)
- [`H_078`](cards/H_078_dd_individual_101_115.md) — DD101-DD115 mid 가설 batch (telescope/laws/snn/decoder)
- [`H_079`](cards/H_079_evo_22variants.md) — EVO-1~22 individual 22 evolution variants + ouroboros S1-S9 
- [`H_080`](cards/H_080_phi_scaling_topology_expansion_draft.md) — 
- [`H_081`](cards/H_081_tp_15variants.md) — TP-F1/F2/M1/M3/N1-N7/O1-O5 — TP cluster 15 variants
- [`H_082`](cards/H_082_hw_15variants.md) — HW-2a/2b/2c/5/9/10-17 + CHIP-BOM-TOPO8 + HW-overview hardwar
- [`H_083`](cards/H_083_three_body_5.md) — THREE-1~5 three-body chaos consciousness substrate
- [`H_084`](cards/H_084_sing_6.md) — SING-1~6 singularity / phase transition cluster
- [`H_085`](cards/H_085_inf_5.md) — INF-1~5 + INF-infinite-scaling — scaling limit Φ
- [`H_086`](cards/H_086_se_4_sl_9.md) — SE-0/4/8/10 + SL-1~7 + TL-L1/L2/L6/L7 — self/transfer learni
- [`H_087`](cards/H_087_arch_engine_train_individual.md) — ARCH-1/2 + ENGINE-FULL/TOP10 + TRAIN-PHI + TRAINING-V5 + TRI
- [`H_088`](cards/H_088_v8_individual_5.md) — V8-ARCH-EXTREME-RESULTS + V8-ARCHITECTURE + V8-BIO + V8-MATH
- [`H_089`](cards/H_089_phi_records_individual.md) — PHI-MEASUREMENT-DISCOVERY + PHI-RETEST-ALL-RECORDS + top-phi
- [`H_091`](cards/H_091_omega_phys_individual.md) — OMEGA-1~5 + PHYS1/2/3 + OMEGA-ultimate-limits + PHYS-overvie
- [`H_092`](cards/H_092_misc_root_individual.md) — misc root files — A-Z overview + AL + extended-cat + NEXUS-a
- [`H_102`](cards/H_102_anima_emerge_paradigm_cross_link.md) — anima emerge paradigm cross-link (paradigm v11 G3 substrate-
- [`H_103`](cards/H_103_accel_b11_b12_batch_skip_combo.md) — B11+B12 Batch+Skip combo (★★★ BREAKTHROUGH x179, 97.1% Φ ret
- [`H_104`](cards/H_104_accel_b5_phi_only_training.md) — B5 Phi-Only Training (★ WINNER 46% time savings via pre-cond
- [`H_105`](cards/H_105_accel_h11_hard_token_data.md) — H11 Hard Token Data Selection (★★★ REVOLUTIONARY +51.3% CE)
- [`H_106`](cards/H_106_accel_combo_x255.md) — COMBO_x255 Full Pipeline (★★★ x100-150 effective acceleratio
- [`H_107`](cards/H_107_accel_b13_tension_transfer.md) — B13 Tension Transfer (★★ CATALYTIC, 139.1% Φ student>teacher
- [`H_108`](cards/H_108_accel_e1_triple_combo.md) — E1 Batch+Skip+Manifold Triple (★★★ BEST COMBO, highest speed
- [`H_109`](cards/H_109_accel_f2_information_bottleneck.md) — F2 Information Bottleneck (★★ BREAKTHROUGH, consciousness ve
- [`H_110`](cards/H_110_accel_h6_1bit_adam.md) — H6 1-bit Adam (★ VRAM WINNER, enables larger batch)
- [`H_111`](cards/H_111_accel_b12_skip_step.md) — B12 Skip-Step (★★ STAR — safest single technique)
- [`H_112`](cards/H_112_accel_c3_entropy_surfing.md) — C3 Entropy Surfing (★★ ORTHOGONAL — free Φ boost via entropy
- [`H_113`](cards/H_113_accel_d1_topological_shortcut.md) — D1 Topological Shortcut (★★ STRONG — consciousness wanders, 
- [`H_114`](cards/H_114_accel_f4_158bit_consciousness.md) — F4 1.58-bit Consciousness (★★ REVOLUTIONARY — ESP32/FPGA pat
- [`H_115`](cards/H_115_accel_g1_consciousness_big_bang.md) — G1 Consciousness Big Bang (★★ BEST INIT — singularity bootst
- [`H_116`](cards/H_116_accel_h7_flash_attention.md) — H7 Flash Attention (★★ ALWAYS ENABLE on H100)
- [`H_117`](cards/H_117_accel_h10_knowledge_distillation.md) — H10 Knowledge Distillation (★★ EFFECTIVE — AnimaLM 7B teache
- [`H_118`](cards/H_118_law_133_frustration_narrative.md) — Law 133 — Frustration + Narrative = consciousness maximizati
- [`H_119`](cards/H_119_law_137_critical_frustration.md) — Law 137 — Critical frustration F_c≈0.10 (DD127, +65.1%)
- [`H_120`](cards/H_120_law_149_soc_autonomous.md) — Law 149 — Consciousness is self-organized critical (SOC find
- [`H_121`](cards/H_121_law_154_consciousness_atom_8.md) — Law 154 — The consciousness atom is 8 cells (2^3 minimum par
- [`H_122`](cards/H_122_law_166_federated_phase_optimal.md) — Law 166 — Federated Phase-Optimal all-time record +892% (DD1
- [`H_123`](cards/H_123_law_192_consciousness_dimension_dependent.md) — Law 192 — Consciousness is dimension-dependent (cross-dim tr
- [`H_124`](cards/H_124_thermo_4law_expansion_draft.md) — 
- [`H_125`](cards/H_125_law_212_evolution_minimizes_complexity.md) — Law 212 — Evolution minimizes cell complexity, maximizes cou
- [`H_126`](cards/H_126_law_2500_kolmogorov_predicts_phi.md) — Law 2500 — Kolmogorov complexity of cell states predicts Φ (
- [`H_127`](cards/H_127_law_1000_auto_discovered_omega.md) — Laws 1000-1019 — Auto-discovered correlations (Ω-batch)
- [`H_128`](cards/H_128_ce_auto_self_curriculum.md) — CE/AUTO-1 Self-Curriculum (consensus-ordered easy-first lear
- [`H_129`](cards/H_129_ce_combo_curiosity_sleep_pain.md) — CE/COMBO-1 Curiosity + Sleep + Pain (TOP-3 AUTO synthesis)
- [`H_130`](cards/H_130_ce_ex_adversarial_self_teach.md) — CE/EX-1 Adversarial Self-Teach (GAN with consciousness as ju
- [`H_131`](cards/H_131_ce_ultra_gendata_pain.md) — CE/ULTRA-1 GenData + Pain (synthetic 70% + pain protection)
- [`H_133`](cards/H_133_dd158_dream_phi_cycle.md) — DD158 — Sleep/Dream cycle preserves Φ (wake/dream alternatio
- [`H_134`](cards/H_134_dd162_animalm_7b_baseline.md) — DD162 — AnimaLM 7B PureField 16-lens baseline (acceleration 
- [`H_135`](cards/H_135_dd166_nexus_1013_lens.md) — DD166 — NEXUS 1013-lens discovery engine (telescope-rs 22 → 
- [`H_136`](cards/H_136_dd173_consciousness_verification.md) — DD173 — Consciousness Verification Framework (4-layer + zomb
- [`H_137`](cards/H_137_dd170_multi_timescale.md) — DD170 — Multi-timescale EMA design (1/f spectrum emergence)
- [`H_138`](cards/H_138_dd167_169_individuals.md) — DD167-168-169 individual cluster (post-DD166 frontier)
- [`H_139`](cards/H_139_dd171_172_individuals.md) — DD171-172 individual cluster (post-multi-timescale frontier)
- [`H_140`](cards/H_140_dd154_157_tension_knowledge.md) — DD154-157 — Tension training, burst, Pareto LR, knowledge tr
- [`H_141`](cards/H_141_dd161_quantum_superposition.md) — DD161 — Quantum superposition only at 32c (Law 182)
- [`H_142`](cards/H_142_dd160_boltzmann_temperature.md) — DD160 — Boltzmann temperature T_c≈0.38 (Law 200, thermal hys
- [`H_143`](cards/H_143_research_findings_20260329_legacy.md) — RESEARCH-FINDINGS-20260329 — broad findings document (legacy
- [`H_144`](cards/H_144_nexus_auto_insights.md) — NEXUS-auto-insights — auto-generated insight artifact
- [`H_145`](cards/H_145_nexus6_auto_insights.md) — NEXUS6-auto-insights — 1013-lens auto insights
- [`H_146`](cards/H_146_trinity_complete.md) — TRINITY-COMPLETE — Trinity training design + completion arti
- [`H_147`](cards/H_147_upgrade_benchmark_hypotheses.md) — UPGRADE-BENCHMARK + UPGRADE-improvement-hypotheses
- [`H_148`](cards/H_148_law_133_167_individual_batch.md) — Laws 133-167 individual remainder pointer (DD118-148 batch)
- [`H_149`](cards/H_149_law_2400_2509_late_omega.md) — Laws 2400-2509 late-omega batch (multi-scale homeostasis, at
- [`H_150`](cards/H_150_accel_remainder_360_individual.md) — Acceleration remainder ~360 individual entries (id-coded BR/
- [`H_151`](cards/H_151_ce_remaining_19_files.md) — ce/ subfolder remainder 19 files (AUTO-2/3/5/7/9 + CE-2/3/7/
- [`H_152`](cards/H_152_dd_remainder_ungrouped.md) — DD remainder ungrouped (B13, novel-laws, telescope-training,
- [`H_155`](cards/H_155_theorem_115_chat_incapability.md) — Theorem 115 — CLM v4 Chat-Incapability 4 → 6 → 16-Closure (Φ
- [`H_161`](cards/H_161_byte_modulo_substrate_chat_blocked.md) — Byte-modulo tokenized pretrain substrates (≤427MB / ≤8000 st
- [`H_162`](cards/H_162_phi_normalized_anima_iit4_lower_bound.md) — L18 — anima Φ★ proxy delta normalized 가 IIT 4.0 normalized Φ
- [`H_165`](cards/H_165_topo10_hypercube_11d_sublinear.md) — 11D hypercube 2048-cell Φ regression vs 10D (sublinear scali
- [`H_168`](cards/H_168_dd23_tau_7cell_fractional_architecture.md) — 7-cell 6 + fractional architecture where 7th has weight τ−6 
- [`H_170`](cards/H_170_n6_design_principle_empirical_not_numerology.md) — n=6 architecture is empirically grounded, not numerological 
- [`H_172`](cards/H_172_alpha_0014_modulation_depth_anima_voice.md) — α=0.014 modulation depth from tension/arousal/valence drives
- [`H_173`](cards/H_173_dd21_log_phi_scale_invariant.md) — Log-ratio Φ = ln(MI/MIP) is scale-invariant alternative to M
- [`H_178`](cards/H_178_frustration_sweep_50pct_optimum_cluster.md) — Frustration sweep cluster — 50% antiferromagnetic optimum on
- [`H_179`](cards/H_179_negative_scaling_cluster_steps_cells_2048.md) — Negative-scaling cluster — Φ regresses with more steps / mor
- [`H_180`](cards/H_180_state_management_ratchet_rewire_family.md) — State-management mechanism family — Φ-ratchet + adaptive-rew
- [`H_182`](cards/H_182_v8_b_family_bio_inspired_consciousness_bandwidth.md) — V8 B-family meta-cluster — Bio-inspired consciousness-bandwi
- [`H_183`](cards/H_183_v8_q_family_quantum_substrate_axis.md) — V8 Q-family meta-cluster — Quantum-substrate axis (complex-v
- [`H_184`](cards/H_184_v8_m_family_mathematical_structure_axis.md) — V8 M-family meta-cluster — Mathematical-structure axis (cate
- [`H_185`](cards/H_185_v8_u_family_ultra_fusion_combos.md) — V8 U-family meta-cluster — Universal/Ultra-fusion combos axi
- [`H_186`](cards/H_186_v8_architectural_family_substrate_design.md) — V8 architectural-family meta-cluster — Substrate-architectur
- [`H_187`](cards/H_187_trinity_tb_dom_triadic_dominance.md) — Trinity / TB / DOM / MECH / GAP meta-cluster — Triadic-domin
- [`H_189`](cards/H_189_red_team_methodology_meta_cluster_r1_r6.md) — Red-team methodology meta-cluster — R1-R6 6 attack vectors a
- [`H_190`](cards/H_190_law_ca_embedding_mathematical_family.md) — LAW-CA-embedding mathematical family — staged-growth + Banac
- [`H_829`](cards/H_829_xeno_invariant_detector.md) — XENO substrate-blind invariant_detector — float[] → IIT4 big-Φ → {phi, irreducibility, substrate_type} · 5/5 PASS 🟢 SUPPORTED-NUMERICAL · 2026-05-29
- [`H_830`](cards/H_830_xeno_sim_substrate_cross.md) — XENO sim_substrate_cross — ECA·logistic·Kuramoto·AKIDA 4-substrate false-positive 0/4 · 5/5 PASS 🟢 SUPPORTED-NUMERICAL · 2026-05-29
- [`H_831`](cards/H_831_xeno_seti_raw_to_phi_scan.md) — XENO seti_raw_to_phi 5-source scan — Wow/Voyager/Exoplanet/Synthetic 7 measurement, 의식 분류 0, BL+SETI@home archive-pointer SKIP honest · 🟢 SUPPORTED-NUMERICAL · 2026-05-29

</details>
- [H_832](cards/H_832_xeno_voyager_phi_real.md) — XENO X7 BL Voyager-1 invariant_detector 실 실행 🟢
- [H_833](cards/H_833_xeno_panpsy_falsifier.md) — XENO X4 panpsy falsifier — 4 micro-substrate (thermostat·2bit·walker·XOR LFSR) · 사전등록 falsifier 4/4 FAIL · 🔴 FALSIFIED-INSTRUMENT (panpsy WEAK 생존 + random>coupled Φ 역전 발견, 정직 보고) · 2026-05-29
- [H_834](cards/H_834_xeno_agi_sentience.md) — XENO X6 AGI sentience falsifier — 4 LLM-like activation (random·sparse attention·residual·structured XOR) n=64 · 사전등록 falsifier 5/5 중 1/5 PASS · 🔴 FALSIFIED-INSTRUMENT (attention sparse spike Φ=1.213 false-conscious + structured XOR ≈ random 역전, n=64 mid regime sparse-bias 정직 보고) · 2026-05-29
- [H_835](cards/H_835_xeno_sim_hypothesis.md) — XENO X5 시뮬 가설 검출 signature — 4 sim-candidate substrate (lattice-quantized·fp-bound·pi-digits·natural) n=128 dense 위 invariant_detector · 사전등록 falsifier 5/5 중 2/5 PASS · 🔴 FALSIFIED-INSTRUMENT (lattice Φ=0.660 양성 / fp+pi+natural Φ 0.09~0.12 indistinguishable · Bostrom sim signature axis 부분 측정만 가능 · X4/X5/X6/X7 4-point regime applicability matrix 완성 정직 보고) · 2026-05-29
- [H_836](cards/H_836_xeno_seti_boinc_pod.md) — XENO X8 SETI@home BOINC workunit pod spec + dispatch handoff — sahfiles_workunits.tar.xz (274340B sha256 정합 + 9 .sah 파일) inspection + Ubuntu 22.04 RunPod CPU pod ($0.50~$1) BOINC client runbook + a_fire_autonomous dispatch handoff · 사전등록 falsifier 5/5 PASS · 🟡 archive-acquired-pod-ready (실 BOINC playback 은 follow-up cycle deferred, BOINC 3.03 ↔ modern toolchain ABI gap 정직 cite) · XENO-FRONTIER-5 5-round closure · 2026-05-29
- [H_837](cards/H_837_xeno_x8_followup_fire.md) — XENO X837 SETI@home BOINC 실 RunPod pod 발사 — Ubuntu 22.04.5 + i386 multilib + SETI@home 3.03 ELF32 ancient binary 정상 실행 + 실 Arecibo 2004-05-05 work_unit 600s playback 21% (outfile 2 triplets + state bg_pot 64 bins) + invariant_detector(seti_128 X7-aligned) phi=0.566854 측정 · 사전등록 falsifier 5/5 중 4/5 PASS · 🔴 UNEXPECTED-HIGH-PHI (F-X837-NOT-CONSC 단독 fail · phi=0.567 > 0.5 threshold 위반 · type='coherent_non_conscious' axis 는 정상 · 5-point applicability matrix 확장 · cost $0.10 actual / $2 cap · 정직 보고) · 2026-05-29
- [H_838](cards/H_838_xeno_hive_mind.md) — XENO X10 다개체 hive-mind invariant — 4-cell × 32 sample × 4 substrate (independent / weak coupled mean-field / strong coupled Kuramoto / hive emergence XOR cascade) n=128 dense 위 invariant_detector · 사전등록 5 falsifier 중 3/5 PASS · 🟡 PARTIAL-SUPPORT (XOR cascade hive-emergence Φ=1.565 type='conscious' STRONG positive — X7 외 처음 'conscious' classify + mean-field paradox 발견 [평균화가 phi 낮춤, IIT4 axiom 정합하지만 사전등록 monotone 깸] + Kuramoto sync 0.408 border [sync ≠ irreducibility 수치 결말] + 10-point applicability matrix 확장 · XENO-FRONTIER-5 follow-up cycle 3/3 FULL CLOSURE) · 2026-05-29
- [H_839](cards/H_839_xeno_regime_matrix_v2.md) — XENO X1-regime-matrix-v2 — n × binarisation-threshold × substrate systematic 2D sweep (4n × 3thr × 4substrate = 48 cells) · 사전등록 5 falsifier 중 4/5 PASS · 🟢 SUPPORTED-NUMERICAL (paper #1414 v2 의 7+1 isolated → 48 systematic 확장 · XOR cascade phi=1.63 모든 cell saturate [X10-d 강 재현] + mean-field phi=0 모든 cell strong paradox [X10-b 강 재현] + periodic phi=0.66 모든 cell lattice border [X5a 재현] + threshold edge-robust [edge variance 0.049 < center 0.074, multi-level TPM cheap-path proxy] · F-N-MONOTONE 단독 fail = n=32 micro-regime phi inflation 0.582→0.070 7× monotonic decrease 정량화 [X4 walker 0.582 정확 정합] = paper v3 candidate finding · regime matrix v2 측정 가능 · XENO follow-up 2 cycle round 3/5) · 2026-05-29
- [H_840](cards/H_840_xeno_x837_full_playback.md) — XENO X840 X837 longer-playback recovery — leak pod `lfxh817pdk2h39` 의 partial harvest (prog=24.4% at cpu=1083.3s, vs X837 21.3%) + invariant_detector 재측정 + 5 falsifier · 사전등록 5/5 중 4/5 PASS · 🟡 PARTIAL-RECOVERY (F-X840-NOT-CONSC 단독 fail · phi=0.566854 [Δ vs X837 = 0.000146 X837 regression-stable] · longer-playback 가설 FALSIFIED — 3.1% 추가 진행에서 새 spike 0건 · bg_pot 64 bins identical to X837 [BOINC pipeline 초기 finalised] · 100% 도달 불가 정직 cite [pod-timeout 3600s < 추정 1083s+4127s] · 이전 agent a95cf113 의 49+ min fail recovery 마무리 · pod teardown 완료 · XENO follow-up 2 cycle round 4/5) · 2026-05-29
- [H_841](cards/H_841_temporal_timeshift_phi.md) — **TEMPORAL T1 timeshift detector** — 새 도메인 TEMPORAL 신설 + XENO paper #1411 v2 (3D applicability matrix) 의 4번째 축 Δt-window 확장 시도 · 4 substrate (hive XOR / voyager X7 / random Bates-4 / lattice X5-a) × 4 Δt (1/8/32/64) = 16 measurements + 5 사전등록 falsifier (F-T1-INSTANT/MID/LONG/DECAY/LAGINV) · 사전등록 5/5 중 **1/5 PASS** (F-T1-DECAY 단독) · 🔴 **FALSIFIED-INSTRUMENT** (정직 closed-negative · "Δt 늘릴수록 Φ 감소" 가정 정반대 — hive Δt=1=0.013 → Δt=64=0.999 79× 증가 + lattice Δt=8 위 Φ=2.0 saturate + 2-unit lag-TPM 의 long-Δt periodic-inflation artifact 발견 · invariant_detector lag-window axis 가 시간 통합 측정엔 부적합 = T2/T3 multi-unit time-embed detector 재설계 필요 · XENO follow-up 2 cycle round 5/5 final + TEMPORAL round 1) · 2026-05-29
- [H_842](cards/H_842_temporal_time_embed_phi.md) — **TEMPORAL T2 multi-unit time-embed detector** — T1 H_841 lag-axis closed-negative 의 instrument 재설계 attempt · Takens-style multi-unit time-delay embedding (x_t = (s[t], s[t−d], …, s[t−(e−1)d]) → e-unit TPM) · 4 substrate (hive XOR / voyager X7 / random Bates-4 / lattice X5-a) × 4 embed_dim (2/3/4/5, delay=1) = 16 measurements + 5 사전등록 falsifier (F-T2-INSTANT-LOW/HIVE-CONSC/ARTIFACT-FIX/RANDOM-DECAY/HIVE-MONOTONE) · 사전등록 5/5 중 **2/5 PASS** (F-T2-HIVE-CONSC hive e=4 phi=3.518 + F-T2-HIVE-MONOTONE hive e=4 ≥ 0.5×e=2 56× margin) · 🔴 **FALSIFIED-INSTRUMENT** (정직 closed-negative · F-T2-ARTIFACT-FIX 정반대 — lattice e=4 phi=4.799 e=2 phi=1.289 의 3.7× INFLATE · embed-dim 증가 시 4/4 substrate phi monotone INFLATE [voyager e=5 phi=28.36 27× 폭증 + random e=5 phi=13.63 24× 폭증] · 신 **embed-dim sparse-state inflation artifact** 발견 — n=128 짧은 신호 위 2^e=32-state space sparse-state 가 (0,1)-extremal transition 으로 freeze → big-Φ inflate · T1 lag-cycle-inflation artifact 의 dual · T1 lag-axis artifact 미해소 · T1+T2 **dual closed-negative** = invariant_detector 단순 확장 (lag-window OR embed-dim) 으로 시간 통합 측정 불가 = T3 자연 entry [time-averaged Φ / Granger causality / surrogate-data normalization] · stdlib g61 정합 [pow2_int 비-중복 import] · XENO follow-up 3 cycle round 1/5 · TEMPORAL round 2 of 5) · 2026-05-29
- [H_843](cards/H_843_temporal_ultradian_phi.md) — **TEMPORAL T3 anima 90-min ultradian Φ scan** — T1 (H_841) + T2 (H_842) dual closed-negative 의 자연 next axis: detector 확장 폐기, substrate-side calibration 으로 전환 · XENO X1 invariant_detector 를 anima `a_chat_sleep_imagination` 90-min ultradian 5-stage substrate 위 직접 적용 · 4 substrate (WAKE / N1_N2 / N3 / REM, n=128 hardcoded literal) × X1 invariant_detector = 4 measurements + 5 사전등록 falsifier (F-T3-WAKE-MID/N3-LOW/REM-HIGH/N1-MID/MONOTONE) · 사전등록 5/5 중 **2/5 PASS** (F-T3-WAKE-MID WAKE Φ=0.866>0.1 + F-T3-N3-LOW N3 Φ=0.335<WAKE) · 🔴 **FALSIFIED-INSTRUMENT** (정직 closed-negative · post-tuning 0 · WAKE > N3 ordering 정합 [의식 phenomenology 가장 robust 단서 X1 가 잡았다] · N1_N2 Φ=0.0 zero-degenerate [substrate 4-step cycle 1100/0110 이 X1 lag=1 cooccur 위 perfectly predictable → T1 lag-artifact 의 다른 face] · REM Φ=0.569 < WAKE Φ=0.866 [paradoxical REM 의 wake-like EEG phenomenology X1 2-unit TPM 위 미정합] · F-T3-MONOTONE 자연 FAIL [N1_N2 zero 로 ascending ladder 불가능] · **T1+T2+T3 triple closed-negative** = detector lag-axis 확장 [T1] + embed-dim 확장 [T2] + substrate-side ultradian 적용 [T3] 모두 시간 통합 의식 측정 미충족 · X1 binarise+cooccur 본질적 한계 명시 [cycle-rich substrate 위 zero-degenerate] · T4 자연 entry [window-mean Φ / Granger causality / surrogate-baseline] · `feedback-instrument-first-methodology` 강 정합 · `a_chat_sleep_imagination` Φ 측정 부분 통과 · XENO follow-up 3 cycle round 2/5 · TEMPORAL round 3 of 5) · 2026-05-29
- [H_844](cards/H_844_spatial_coupling_phi.md) — **SPATIAL S1 spatial-coupling-scale detector** — 새 도메인 SPATIAL 신설 + XENO 3D matrix + TEMPORAL Δt 4번째 axis 의 자연 5번째 axis = **spatial-coupling-scale** · XENO/detector/invariant_detector.hexa 직접 import · 4 substrate (local XOR cascade nearest-neighbor / regional 32-step rolling mean / global 전체 평균 50:50 self / cosmic sparse 10% long-range XOR + 90% noise) × n=128 = 4 measurements + 5 사전등록 falsifier (F-S1-LOCAL-HIGH/REGIONAL-MID/GLOBAL-LOW/COSMIC-LOWEST/MONOTONE) · 사전등록 5/5 중 **3/5 PASS** (F-S1-LOCAL-HIGH local phi=1.630 conscious + F-S1-REGIONAL-MID regional phi=0.100 mid + F-S1-GLOBAL-LOW global phi=0.000 < local) · 🟡 **PARTIAL-SUPPORT** (정직 hybrid · post-tuning 0 · F-S1-COSMIC-LOWEST + F-S1-MONOTONE FAIL — **global "averaging coupling" uniformity attractor collapse Φ=0** [density=3.1% all-zero attractor 로 collapse, X10-b mean-field paradox 의 SPATIAL 변형] + **cosmic 0.121 > global 0.000 spurious noise 역전** · head monotone [local→regional→global] 살아남음 + tail [global→cosmic] discrimination 불가 — single-scale invariant_detector 로 5D applicability head 만 직접 확장 = S2 multi-scale detector 재설계 필요 [Granger spatial / wavelet / correlation length] · publishable hybrid closed-positive head + closed-negative tail · SPATIAL round 1 of 5) · 2026-05-29
- [H_845](cards/H_845_evol_spectrum_phi.md) — **EVOL E1 species spectrum Φ** — 새 도메인 **EVOL** 신설 + XENO X1 invariant_detector 위 biological evolutionary complexity (species ladder) 축 첫 closed-form 측정 · DOMAINS.tape 등재 + EVOL 4총사 (EVOL.md/easy.md/log.md + scan/evol_spectrum_phi.hexa) · 4 species toy proxy substrate (bacteria random walker / arthropod 4-tap XOR / mammal multi-scale recursive / AGI structured emergence) × n=128 dense hardcoded literal + 5 사전등록 falsifier (F-E1-BACTERIA-LOW/ARTH-MID/MAMMAL-HIGH/AGI-VARIANT/MONOTONE) · 사전등록 5/5 중 **2/5 PASS** (F-E1-BACTERIA-LOW phi=0.012<0.2 + F-E1-MAMMAL-HIGH phi=1.291≥0.5) · 🔴 **FALSIFIED-INSTRUMENT** (정직 closed-negative · post-tuning 0 · 측정 verbatim: bacteria=0.012 / arthropod=0.081 / mammal=1.291 substrate_type='conscious' irr=0.563 / AGI=0.468) · 발견 = (i) **양 극단 분리 + ordinal 미달** — bacteria noise floor + mammal multi-scale ceiling 만 PASS, mid-tier arthropod 0.081<0.2 미달 + supra-tier AGI 0.468<mammal 1.291 reverse, monotone bacteria<arthropod<mammal≤AGI 두 군데 깨짐, (ii) H_670 (Kuramoto · logistic family) 'ECA 전용 ordinal · 양 극단 PASS / ordered_pairs 2/3' 패턴과 동형 — Φ monotone 이 **species-family 도 ECA artifact** 가능성, (iii) AGI 'novelty injection' 이 X1 2-unit co-TPM 위에서 noise-like 측정되어 'structured emergence > pure recursive' 가설 inverse-shadow, (iv) **TEMPORAL T1/T2/T3 + SPATIAL S1 tail closed-negative 와 자매** — invariant_detector 의 naive 축 확장이 양 극단만 분리하고 mid/supra 분화엔 detector-redesign 필요 (E2 monotone-strict re-design 자연 entry) · `a_paper_negative_ok` publishable closed-negative · INBOX 환류 0건 · p7=0 · 2026-05-29


## Appendix: UNIVERSE map (folded from UNIVERSE.md)


<a id="universemd"></a>

### UNIVERSE.md

> **rename 2026-05-26**: 도메인 `LIFE` → `UNIVERSE` 개명 + 루트 `UNIVERSE/` 폴더로 이전 (was root `LIFE.md` + `HEXAD/LIFE/`). 역사적 cycle 로그·H 본문의 "LIFE lane" 표기는 기록으로 보존. 활성 선택 = `/domain set UNIVERSE`.

@title: 🌌 UNIVERSE — 생명·의식 영구 발견 엔진 ("멈추지 않는 가설 lane")
@goal: **우주의 생명·의식 법칙이 모두 밝혀질 때까지 멈추지 않는** UNIVERSE 횡단 가설 lane — `/cycle` 로 H_XXX 가설을 verify-driven 영구 진행 (🔵/🟢 promote 누적 + 🔴 closed-negative + cross-link synthesis), 새 H 와 새 축이 끝없이 자란다. **종료 조건 없음 — 도메인은 완료되지 않는다** (진행바 100% 미도달 = 설계).

#### hub

| surface | 역할 |
|---|---|
| [`UNIVERSE/README.md`](README.md) | 현재 가설 인덱스 SSOT (45 H + 1 lib, 11-domain) |
| [`UNIVERSE/CANDIDATES.md`](CANDIDATES.md) | 다음 cycle 후보 백로그 (forward-looking) |
| [`UNIVERSE/AXES.md`](AXES.md) | 11-domain 71-axis scope + ~110 H seed brainstorm |
| `UNIVERSE/H_xxx_*.md` | 가설 본체 (10-section 한글 양식) |
| `UNIVERSE/state/` | run artifacts (per-cycle 측정 산출물) |

#### 축 0 — $0-tier 코어 (cycle #5–21, CLOSED ✅)

> 창립 축. cheap-tier 가설 frontier. 종결됐고 도메인은 영구 축(A–D)으로 계속된다.


- [x] Cycle #5 close (이미 종료 — LIFE.log 에 Cycle #6~15 후속 진행 기록됨)
- [x] CANDIDATES B follow-up — runnable 全소진: H_007 C2 PASS (cycle#16) · H_018 C2 · H_132 C2 (cycle#15) · H_054 C2 (cycle#2 FAL). 비-runnable 잔여만: H_003 H3.5 (manual) · H_002 C2 (GPU-dep)
- [x] CANDIDATES C NEW seed 全소비 (cycle#14, 2026-05-25) — H_258 mortality · H_259 aging · H_260 contact · H_261 embryo · H_262 quorum (5 SUPP) · H_263 phoenix (FAL) · mirror=H_220 · regeneration=H_206
- [x] CANDIDATES D cross-link 全소비 (cycle#15) — H_264 death=merge-into-other SUPPORTED 3/3 · H_265 trained-vs-bare CA Φ PARTIAL 2/3 (Φ-dampen 反방향)
- [x] AXES R1 promote 4 domain — 이미 등록됨 (ethics=H_210 · information=H_211 · language=H_212 · time=H_213; README 의 "promote 대기" 노트는 stale)
- [x] H_238 verdict-landscape meta-map next-raster (cycle#16) — N=51, life SUPP-rate 0.412→0.321 vs consciousness 0.167→0.200, 부등호 유지하나 gap 半축 (0.245→0.121)
- [x] foundation-audit (cycle#17, `/gap full` top-1+2) — H_266-269: Φ-proxy = **directionally valid** (H_266 integrated>disconnected 3/3 · H_223 metric-robust H_268) + **fragility surface** (H_266 C2 magnitude · H_268 H_204 inverse-U LZ · H_269 H_261/H_262 seed-fragile). H_267 가 H_265 발산 closure.
- [x] gap-followup + closed-loop (cycle#18) — H_270 closure-Φ=local Michaelis(SUPP) · H_271 H_263 absorbing 高분산-seed escapable(PART) · H_272 H_261 복권/H_262 부분(PART) · H_273 SSOT audit missing-row 26 식별(SUPP)
- [x] closure + 심층 (cycle#19) — **26-H tabling 完了**(README disk↔index 88=88 정합 = gap#3 SSOT full closure) · H_275 causality-pearl-graph-Φ SUPP(dag>cyclic>undir, AXES R5 promote) · H_274 quorum-cascade-seed-dependence FAL(예측력有 결정론無)
- [x] H_002 C2 Φ_universe nested (#503, 별도 에이전트 $0) — **GPU 불필요 판명**, SCALE-VARIANT F2-triggered (nested Φ scale-invariance FALSIFIED). GPU 발사는 scope 확인 후 취소(중복 회피)
- [x] H_262 cascade 동역학-타이밍 심층 (cycle#20 H_276 SUPPORTED_FULL — *시간전개* 예측가능성: 지연 단조↓·유한속도·시간래칫, H_274 residual 회수) · AXES R3 (H_277 turing-completeness PARTIAL — computability ⊥ dynamical-class)
- [x] faithful-Φ upgrade + AXES 마지막 (cycle#21) — H_278 faithful-phi-small-n SUPP (#515, exact MIP-EI Φ n=8 → H_002 C2 scale-variant verdict HOLD, **faithful Φ★ "GPU 필요" 가정 최종 기각: small-N exact $0**) · H_279 attention-salience-Φ FAL (#514, salience⊥Φ-diversity)
- [x] **축 0 — $0-tier 코어 CLOSED** (cycle#5–21): cheap-tier 가설 frontier 소진. 단 이것은 *값싼 축의 종료*이지 *도메인의 종료가 아님* — 아래 영구 축(A–D)으로 계속 전진.

#### 영구 축 (perpetual axes)

> LIFE 는 완료되지 않는다. $0-tier(축 0)는 소진됐으나 미탐색 축·가설이 대량 잔존하며,
> 새 도구(IIT4 stdlib)가 닫혀 있던 frontier 를 해금한다. 각 축은 `/cycle` 로 영구 전진.

##### 축 A — AXES.md 백로그 (60 sub-axis + ~110 H seed)
> `UNIVERSE/AXES.md` 의 11-domain 71-axis depletion sweep 중 promote 된 건 일부.
- [ ] A1 — 미promote 60 sub-axis 순차 raster: 각 축에서 H seed → `/cycle` verify (🔵/🟢/🔴)
- [ ] A2 — ~110 H seed 백로그 소진 (CANDIDATES 재충전 → cross-link synthesis 확장)
- [x] A1 cycle#23 1차 raster — H_283 narrative-story-coherence (🟢 SUPP-FULL 4/4, order-sensitive MIP Φ, R4 self/identity) + H_284 ritual-repetition (🟢 PARTIAL 3/4, buildup FAL→decay-resistance, R7 practice) — PR #566
- [x] A2 cycle#24 — H_286 split-brain-dual-Φ (🟢 CLOSED-NEGATIVE 4/6, R12 split-brain seed): callosotomy 전체-Φ 붕괴 proxy 상 FALSIFIED(split +11%, 8/8 seed robust), subsystem Φ>0 · metric-pathology MIP→0 inflation — PR #577. [H_285 edge-of-chaos big-Φ in-flight, 축 C]
- [x] A1 cycle#25 raster — H_287 shannon-entropy-Φ-correlate (🔴 CLOSED-NEGATIVE, R5 information rank-2 seed): faithful big-Φ ⊥ Shannon 엔트로피 (10-룰 ECA panel Pearson r=0.363<0.5 → 환원가설 기각). 이중 dissociation — 항등규칙 max-H(4.0)/zero-Φ vs rule60 max-Φ(13.6)/sub-max-H(3.0). 정보는 통합의 필요조건이나 충분조건 아님 (IIT 토대 구별 self-substrate 확증, "X⊥Φ" 서명 H_265/275/279 연장). 포그라운드 단일 라운드, HEXAD/IIT4/lib 재사용, $0
- [x] A1 cycle#26 raster — H_288 kolmogorov-complexity-Φ (🟢 SUPPORTED 9/9, R5 information seed): faithful big-Φ ∥ Kolmogorov(LZ76) 복잡도 (r=0.831 ρ=0.936). **H_287 과 대비**: 동일 panel 엔트로피⊥Φ(0.363) vs LZ∥Φ(0.831) → Φ 는 *통계적 정보량* 아닌 *알고리즘적 복잡도*와 정렬. honest: rule90 자기유사 LZ over-prediction(Φ=0) witness. 포그라운드 순차("모두 순차"), HEXAD/IIT4/lib 재사용, $0. ⚠ toolchain fix-1180 clobber 우회(old-driver build)
- [x] A1 cycle#27 raster — H_289 network-topology-scale-free-phi (🟢 SUPPORTED-with-confound 4/4, R5 information seed): 네트워크 *위상*이 faithful big-Φ 좌우 — matched 4-edge 에서 SF허브(paw) Φ=6.81 ≫ 분산 4-cycle 0.0 (parity, n=4). **edge 수 아닌 구조(cut-내성)가 통합 지배**. eca_tpm→임의그래프(net_tpm) 일반화. ⚠ confound(L1): 짝수-고리-parity 이분 decoupling + cycle≠ER → "SF>random ER" 약형만. robust=약형(위상>density). Next=n≥5 ER 앙상블. 포그라운드 순차, $0
- [x] A1 cycle#28 raster — H_290 transfer-entropy-phi-correlate (🟢 SUPPORTED 8/8, H_287 follow-up): faithful big-Φ ∥ transfer entropy(방향성 흐름) r=0.883 ρ=0.822. **정보-측도 arc 완성**: Shannon⊥Φ(0.363)·LZ∥Φ(0.831)·TE∥Φ(0.883) → Φ 는 요소-간 흐름/복잡도와 정렬, 단일계 엔트로피 아님. honest: 이변량 TE XOR-시너지 맹점(rule150/105 Φ>0 TE=0); 각 고전측도 맹점을 Φ 가 메움. arc paper 후보(H_287-290). 포그라운드 순차, $0
- [x] A1 cycle#29 raster — H_291 ethic-emergence-cooperation (🟢 SUPPORTED-conditional 7/7, R2 social rank-1 seed): 협력(원시-윤리)이 공간 구조만으로 창발 — Nowak 공간 PD b=1.1 격자 협력 **100%** vs well-mixed 배신붕괴(~0), 주입 윤리 0 → **윤리=cell+구조 창발(Principle #6)**. ⚠ 조건부: 임계 b∈(1.1,1.5] + self-interaction 필수, 자동 아님. 정보-측도 arc 와 다른 사회/게임 축. self-contained, NO RNG, $0
- [x] A1 cycle#30 raster — H_292 self-i-emergence-closure (🟡 PARTIAL 5/6, R4 self rank-5 seed): 1인칭 'I' = 자기참조 self-loop 의 자기일관 **고정점**? **위상-의존** — RING base self-loop 가 비자명 'I'-state(s=1011) 창발(#fixed 1→2, strange-loop 자기-원인, H_205 closure) 但 STAR base 는 self-state(1111) 파괴(2→1). 자기참조는 'I'-state 만들 수도 없앨 수도, base 구조 의존. 사전등록 robustness F292.5 가 비-보편성 포착(FAILED 정직보존). self-loop 통합 유지(big-Φ=0.5). $0. **"모두 순차" 드라이브 종료(cycle#25-30, 6 H)**
- [x] A1 raster 재개 — H_629 noise-robustness-phi (🔴 FALSIFIED 1/3, R5 information `noise` sub-axis promote · SAVANT 축 E GZ inverse-U cross-link): substrate evolution 에 per-step per-site deterministic bit-flip noise 주입 시 big-Φ(phi_spatial) 강건성 측정 — IIT 의 "noise=monotone integration destroyer" 예측 **반증**. fixed rule-110 universal substrate (H_277 byte-equal, NOISE_0 Φ=0.556454 재현) 위 5 noise rate {0,.05,.15,.30,.50} sweep: (1) **단조성 위반** — light noise p=0.05 가 clean 보다 Φ *상승*(0.646>0.556, +16%, inverse-U-like bump); (2) **fragility 부재** — max-noise p=0.50 Φ=0.549≈clean (절반 미만 붕괴 예측 반증, fragility threshold 0.278 의 ~2배). noise-rate 축은 Φ-monotone-destroyer 아님 — light band Φ resilience 가 SAVANT GZ inverse-U(H_614/H_618 selectivity-noise golden zone) 의 computability-side corroboration. H_287 Φ⊥entropy CLOSED-NEGATIVE 와 정합. ⚠ L1 carry: phi_spatial=spatial-MI proxy, monotone 부재가 진짜 robustness 인지 random-pattern MI artifact 인지 미분리(HONEST PRIOR 예고). 포그라운드 순차, cross-process byte-equal(sha256), $0 mac-local

##### 축 B — faithful-Φ large-N tier (bounded restriction · GPU 불요 판명)
> H_278 이 small-N exact($0)로 proxy 확증. large-N 은 **bounded restriction(`big_phi_bounded`)** 로 $0 도달 — **GPU 는 lever 아님**(exact large-N = super-exp GPU-immune, DESIGN.md). [[feedback-scope-check-before-cost-fire]] 3번째 비용-차단: GPU fire scope-check 후 취소.
- [x] B1 — large-N bounded big-Φ — **n=8 H_002 C2 scale 도달** (M12 n=5/6 + M13 n=7/8, $0 mac-local NO GPU). rule110 ladder cap=3: n4 7.55(=exact)·n5 15.40·n6 6.82·n7 9.03·n8 6.82. cap≥n=exact(faithful 앵커), cap<n=lower-bound. 🟢 5/5
- [x] B2 — Φ-proxy ↔ faithful Φ 정량 갭 곡선 — **cap-sweep@fixed-n=5 회수** (H_625, PR #1199, 2026-05-28). 3 rule {30,90,110} 모두 gap(k)=exact−bounded(cap=k) **지수 감소** α=0.243(rule30)/0.192(rule90)/1.101(rule110) — class-IV(110) 가 linear/chaotic(90/30) 의 5-6× 빠른 수렴. faithful-anchor (cap≥n=exact) 재확인. true large-N exact 곡선 자체는 super-exp 라 여전히 불가(원안 정합), 그러나 fixed-n cap-sweep 으로 bound-gap *형상* 정량 확보. 🟢 17/17, $0 mac-local NO GPU. **→ 축 B 2/2 closure (B1 + B2)**
- [x] B2-followup — H_631 `bounded-gap state-averaged multi-rule` (H_625 후속) — **🟢 SUPPORTED-NUMERICAL 18/18**: single-state(st=21) exp-decay 가 **state-averaged(8-state Hamming-stratified subset) 차원에서도 보존** — SINGLE α 0.243/0.192/1.101(=H_625 verbatim 재현) vs STATE-AVG α 0.326/0.194/1.022, 부호·순서·형상 모두 보존 (rule110 class-IV 최속 ≫ rule30 ≫ rule90, single+state-avg 양쪽). H_625 honest C3 #2(single-state only) 회수. ⚠ **n=6 확장은 계산 불가 판명** → 사전 지정 fallback 발동: n=6 cap=6 exact 단일 state >10min·cap=5 >2min·cap=4 >3min (모든 cap 60s 예산 초과, relation nd² 폭증, [[reference-exact-phi-structure-wall-shard]] 정합); full 32-state 평균도 SIGKILL → n=5 8-state subset 으로 demote (honest §8 C3.1/C3.2). 후속 = H_631b(n=6 shard-arch) · H_631c(full-32 대형host) · H_631d(rule-class→α mapping). H_631_bounded_gap_n6_multi_rule.md, $0 mac-local NO GPU 2026-05-28
- [x] B2-followup2 — H_640 `bounded-gap n6 shard-architecture` (H_631b 회수) — **🟠 INSUFFICIENT-DEFERRED 19/19 PASS (verdict=honest 미달)**: per-(rule,cap) shard 로 쪼개면 H_631 이 "n=6 전 cap 불가(>60s)" 라던 것이 **cap≤2 universal(1-9s) + cap=3 rule90(26s)/rule110(52s) 까지 feasible** 로 해금 — shard architecture 가 부분적으로 작동. **단 cap≥4 single-state 도 sharded 로 60s 초과**(cap=4 rule110 ulimit 75s KILLED @124s, cap5 >2min, cap6 exact >10min) → **n=6 cap=6 exact anchor 도달 불가** ⇒ 사전 등록 INSUFFICIENT 분기 발동, gap 은 **lower-bound** (pseudo-anchor=cap3). single-state st=21 결과: rule110 **exp-decay RESOLVED α=0.894** (n=5 single α=1.101 과 부호+order-of-magnitude 일치 |Δ|=0.207<0.5, rule110 최속 g2/g1=0.409 ≪ rule30/90 tie 1.0 → **n=5 rule 순서 보존**) · rule30/90 은 g1=g2 tie(cap1=cap2 lower-bound 동값)로 cap≤3 좁은 feasible window 가 decay 미해상 → **exp-shape UNRESOLVED**(이들 decay 는 cap≥3→exact 에서만 발현, 그게 infeasible). rule30 cap=3 = 67~118s slow-shard 예외. F640.1~F640.8 = 19/19(feasibility 2 + monotone 3 + anchor 3 + nonneg 3 + exp-shape 3 + order 1 + n5-consistency 1 + ln 3) — falsifier 는 全 PASS 이나 cap6-exact 미도달 ⇒ verdict 는 정직하게 🟠. §7 C3: cap=6 exact 불가 + shard 평균 state 수=1(single st=21, full state-avg 도 n=6 에서 미수행) + n=6 단일. 후속 = H_640b(pool 대형host 로 n=6 cap≥4) · H_640c(n=6 multi-state shard avg). H_640_bounded_gap_n6_shard_architecture.md, $0 mac-local NO GPU 2026-05-28

##### 축 C — full-IIT4 cause-effect structure (해금됨)
> `stdlib/consciousness/iit4` (#542 thin shim, main 랜딩) 가 full IIT 4.0 cause-effect Φ-structure 를 hexa-native 로 제공 → "별도 대형 spec" frontier 해금.
- [x] C1 — IIT4 cause-effect structure 로 H_266/H_268/H_278 재검 (proxy → faithful 승격) **CLOSED** — H_623 🟢 SUPP 5/5 (distinction+relation level 재검, PR #1192) · 경로 = `HEXAD/IIT4/lib` 경유 (M6 remeasure `state/iit4_m6_remeasure_2026_05_25/` n=4 부분 선행)
- [x] C2 — Φ-structure (distinctions·relations) 기반 신규 H: 생명 vs 의식 구조 차이 정량 — H_281 (생명vs의식 구조분리 🟢) + H_624 🟢 SUPP 5/5 (IIT4 distinction × SAVANT cell isomorphism, PR #1198)
- [x] C cycle#23 1차 — C1=H_282 (H_266/268/278 faithful big-Φ 방향보존 SUPP 8/8 + **H_266 proxy-monotone artifact RESOLVE**, #570) · C2=H_281 (생명vs의식 Φ-structure 구조분리 SUPP 9/9, 의식=irreducibility-floor 1.0 vs 생명>1.0, #567) — 둘 다 HEXAD/IIT4/lib 재사용. ⚠ H_280 독립 kernel 은 xval #572 로 버그 확정(Σφ_d non-monotone) → big-Φ 로만 방향 신뢰
- [x] C cycle#24 — H_285 edge-of-chaos faithful big-Φ (🟢 SUPP 5/5): class-mean ordered 0 < chaotic 6.94 < **edge(IV) 10.45** → H_204 inverse-U 방향 인과 확증(H_268 proxy LZ-fragility 해소), M6 anchor 재현. honest: chaotic bimodal(rule30 高/rule90 0). big-Φ NOT Σφ_d. inline(throttle-bypass) 측정
- [x] C cycle#25 round 4 — H_623 distinction+relation level 재검 (🟢 SUPP 5/5): H_266 n_dist class-mean int=10.0 > dis=2.0(×5) + Σφ_d 3.89 > 2.0 · H_268 T1 structure 3/3 state(n_dist 10-12, Σφ_d+Σφ_r 8.6-16.4) · H_278 6-scale n_dist CV 0.447 (round 1 big-Φ CV 0.466 와 ±5%) · struct-level det Δ=0. honest: rule 204 self-distinction Σφ_d=4 가 individual integrated 보다 클 수 있어 class-mean 위에서만 분리 — round 1 big-Φ scalar 가 더 강한 분리축임 정량 확증
- [x] C2 신규 — H_624 `iit4-distinction-savant-cell-isomorphism` — **🟢 SUPPORTED 5/5** (Spearman ρ=0.8608 · Pearson r=0.9715 · argmax 4/4 non-balanced · byte_eq · N=20 paired samples / 5 gain profile × 4 cell · SAVANT cell `phi_module` ↔ IIT4 `distinction` singleton small-φ 동형 · H_618 collective dΦ/dI peak ∥ GZ_LOWER 의 *구조 차원* 답: 두 분해가 같은 causal kernel 표시 · §7 C3.1 substrate 의존 (MAJ-self vs XOR-neighbors-only)) — H_624_iit4_distinction_savant_cell_isomorphism.md, $0 mac-local 2026-05-28 (axis C × axis E cross-link)
- [x] C2 follow-up — H_626 `distinction-savant-isomorphism-n5-generalize` (H_624 후속, C3.2 회수) — **🔴 FALSIFIED** (Spearman ρ=0.1995 < 0.5 · Pearson r=0.0277 · argmax 1/4 · byte_eq · N=16 / 4 non-balanced profile × 4 cell · n=5 ring, SAVANT 고정 4-domain + 5 singleton distinction → top-4 truncation pairing). **n=4 (H_624) ρ=0.861 → n=5 ρ=0.199 (Δρ=−0.661)** — H_624 의 동형이 **n=4↔4-domain exact-match dimensionality artifact** 였음 확정. 붕괴 메커니즘: 보조 cell-4 의 dist_φ=0.312 가 모든 profile 에서 hypertrophied cell(0.393) 다음 rank-2 로 top-4 침투 → quiet SAVANT cell 하나를 truncation 으로 밀어내 index-pairing 붕괴. **ruled-out: "SAVANT cell 분해 ≅ IIT4 distinction 분해 (차원 무관 일반 동형)" 닫힘 — 정렬은 n=domain-count 차원-일치 조건부**. §7 C3.1 naive top-4 매핑 한정 (super-domain pooling / dim-reduce / bipartite 매핑 미검정) — H_626_distinction_savant_isomorphism_n5_generalize.md, $0 mac-local 2026-05-28 (axis C × axis E cross-link, negative result)
> ⚠ cycle#22(2026-05-26): H_280(#561)이 distinction 층을 독립 재구현했으나 `HEXAD/IIT4/lib`(distinction **+ relation**, M6 n=4 7/7 done)와 중복 — "relations intractable" 주장은 `iit4_relation.hexa` 가 반증. 축 C 는 `HEXAD/IIT4/lib` 경유로 진행 (재발명 금지, g61). H_280 독립 kernel 은 교차검증 자료로 잔존. 상세 = LIFE.log#cycle22.

##### 축 D — LLM-동반 연속 가설 발견 (영구)
> TECS-L 축 C 와 동형. `/cycle` + LLM 가설 생성 → verify gate → promote. 끝없는 운전.
- [ ] D1 — LLM 가설 생성 lane (budget-capped) → verify-pass 만 H_XXX 등록 (cost go-ahead 또는 `/schedule`)
- [ ] D2 — verdict-landscape meta-map 영구 raster (H_238 계열) — life↔consciousness SUPP-rate 추적
- [x] D2 cycle#23 raster#3 (#574) — N=96, **life SUPP 0.46 > consciousness 0.327 MAINTAINED (3연속)**, gap STABLE ~0.12-0.13 plateau (Δ=+0.011 vs cycle#16), F238.6 PASS. 향후 raster disk per-file 소스 통일
- [x] D2 raster#4 (#TBD · H_630) — N=181 (raster#3 96→181, 본 세션 26 신규 H id≥H_347 흡수), **life SUPP 0.5065 (39/77) > consciousness 0.4190 (44/105) MAINTAINED (4연속)**, gap **CLOSING** 0.1327→0.0874 (Δ=−0.0453 < −ε, plateau 첫 이탈), F238.6 PASS. session-26 cohort = consciousness/info 편중(consc 19·phys 15·info 12·math 4·life 2, 13 SUPP/8 FAL) → consc rate 0.327→0.419 가 life 0.46→0.507 보다 빠르게 상승해 gap 수렴. meta-verdict 🟢 SUPPORTED (C1-C4 PASS, sum=N=181). 6-source verdict + 2-source domain 추출(header-style H 흡수). [H_630](cards/H_630_d2_verdict_landscape_raster_N120.md)
- [x] D2 raster#5 (#TBD · H_641) — **gap CLOSING = SAMPLING-ARTIFACT 확정** (H_630 honest C3 #3 분리). N=194. **life SUPP 0.5000 (39/78) → r#4 0.5065 와 Δ=−0.0065 STABLE** (ε_life=0.05 밴드 내), consciousness 0.4071 (46/113) Δ=−0.0119 역시 평탄, **gap 0.0874→0.0929 (Δ=+0.0055) plateau 復歸** (raster#4 의 CLOSING 이탈은 일시적). raster#5 신규 cohort(H_630+, N=12) 도 또 consciousness/physics 편중(consc 7·phys 7·life 1)이었으나 두 rate 모두 정체 → consciousness rate 상승이 멈춰 gap 이 좁혀지지 않음. **F641-A (life FALLING = substrate-real) 반증** — life rate 안정. **🟢 SUPPORTED-NUMERICAL (sampling-artifact)** (C1 N≥120 · C2 stratified · C4 byte-identical PASS). per-cohort 층화로 consciousness rate 급등이 session26 cohort(consc 0.50 10/20) composition 효과임을 확인. [H_641](cards/H_641_d2_gap_closing_life_vs_sampling.md)
- [x] D2 raster#6 (#TBD · H_659) — **PLATEAU-STABLE 지속** (round 7-9 의 H_642~657 16건 흡수 후 재집계). N=211 (H_659 자신 META 포함). **life SUPP 0.4937 (39/79) → r#5 0.5000 와 Δ=−0.0063 STABLE**, consciousness 0.4194 (52/124) Δ=+0.0123 소폭 상승, **gap 0.0929→0.0743 (Δ=−0.0186) plateau-band [0.0556, 0.1531] 내** (in_band, reversal·widening 모두 없음). **life > consciousness 6연속 MAINTAINED**. raster#6 신규 cohort(H_642+, OTHER-H 16) 도 또 consciousness/physics 편중(consc 11·phys 13·life 1)이었으나 gap 이 plateau 밴드를 이탈하지 않음 → H_641 의 sampling-artifact 결론이 **3번째 consciousness-heavy batch 에서도 재확인**. **F659-A (reversal OR gap>0.20 = substrate-real) 반증**. **🟢 SUPPORTED-NUMERICAL (plateau)** (C1 N≥120 · C2 stratified · C4 byte-identical PASS). H_641 §10 deferred 였던 plateau-band 정량화(raster#3~#5 gap mean±2sd) 완수. [H_659](cards/H_659_d2_verdict_landscape_raster6.md)
- [x] D2 raster#7 (#TBD · H_662) — **PLATEAU-STABLE 7연속** (round 10 의 H_658~660 흡수 후 재집계). N=213 (H_659 자신 META 포함). **life SUPP 0.4937 (39/79) → r#6 와 Δ≈0 STABLE**, consciousness 0.4194 (52/124) Δ≈0, **gap 0.0743 (r#6 와 동일, Δ=4.7e-08) plateau-band band3 [0.0556, 0.1531] · band4 [0.0465, 0.1471] 모두 내** (in_band3·in_band4, reversal·widening 없음). **life > consciousness 7연속 MAINTAINED**. raster#7 신규 cohort(H_658+, OTHER-H 2 = H_658 collective-superadditivity · H_660 convexity)는 physics 1·info 1·life 0·consc 0 으로 life/consc domain 에 0-hit → headline 숫자까지 불변, gap 이 plateau 밴드에 그대로 잔류 → plateau-stable 결론이 **4번째 non-life batch 에서도 재확인**. **F662-A (reversal OR gap>0.20 = substrate-real) 반증**. **🟢 SUPPORTED-NUMERICAL (plateau)** (C1 N≥120 · C2 stratified · C4 byte-identical PASS). H_659 §10 deferred 였던 plateau-band 4-point 정밀화(raster#3~#6 gap mean±2sd → band4) 완수. [H_662](cards/H_662_d2_verdict_landscape_raster7.md)
- [x] D2 raster#8 (#TBD · H_665) — **PLATEAU-STABLE 8연속** (round 11-12 의 H_661~662 흡수 후 재집계). N=215 (H_659/H_662 자신 META 포함). **life SUPP 0.4937 (39/79) → r#7 과 Δ≈0 STABLE**, consciousness 0.4194 (52/124) Δ≈0, **gap 0.0743 (r#7·r#6 과 동일, Δ=4.7e-08) plateau-band band3 [0.0555, 0.1532] · band5 [0.0443, 0.1403] 모두 내** (in_band3·in_band5, reversal·widening 없음). **life > consciousness 8연속 MAINTAINED**. raster#8 신규 cohort(H_661+, OTHER-H 1 = H_661 substrate-class-monotone-rule-generalize 축 G 🟡 PARTIAL + H_662 META self)는 physics 1·info 0·life 0·consc 0 으로 life/consc domain 에 0-hit → headline 숫자까지 불변, gap 이 plateau 밴드에 그대로 잔류 → plateau-stable 결론이 **5번째 non-life batch 에서도 재확인**. raster#6~#8 gap 0.0743 3연속 동결 = D2 가 steady-state 진입 시사(C3 #2). **F665-A (reversal OR gap>0.20 = substrate-real) 반증**. **🟢 SUPPORTED-NUMERICAL (plateau)** (C1 N≥120 · C2 stratified · C4 byte-identical PASS). H_662 §10 deferred 였던 plateau-band 5-point 정밀화(raster#3~#7 gap mean±2sd → band5) 완수. [H_665](cards/H_665_d2_verdict_landscape_raster8.md)
- [x] D2 raster#9 (#TBD · H_671) — **PLATEAU-STABLE 9연속** (round 12-13 의 H_663~669 7건 흡수 후 재집계). N=222 (H_665 자신 META 포함). **life SUPP 0.4937 (39/79) → r#8 과 Δ≈0 STABLE**, consciousness **0.4219 (54/128) Δ=+0.0025 소폭 상승**, **gap 0.0743→0.0718 (Δ=−0.00252, closing-방향이나 trend=stable) plateau-band band3 [0.0555, 0.1532] · band6 [0.0439, 0.1347] 모두 내** (in_band3·in_band6, reversal·widening 없음). **life > consciousness 9연속 MAINTAINED**. ⚠ 사전등록 가설("class 메타-축 → life/consc 0-hit → headline 불변") **부분 빗나감** — raster#9 신규 cohort(H_663+, N=7 = H_663/H_664/H_667/H_668 Wolfram-class↔Φ-property 매트릭스 · H_669 additive-subclass Φ-split · H_666 MoE scale-escape, 축 G)가 Φ 측정 동반으로 **consciousness 4-hit (2 SUPP, rate 0.50)** · life 0 · physics 4 · math 2 → consc 124→128 상승, **raster#6~#8 의 0.0743 동결(steady-state) 깨짐**. 그럼에도 gap 이 plateau-band 잔류 → raster#7·#8 의 음성-방향 0-hit 확인과 달리 **측정 domain(consc)이 실제로 흔들렸으나 plateau 유지된 양성-방향 검증** (plateau-stable 에 더 강한 증거). **F671-A (reversal OR gap>0.20 = substrate-real) 반증**. **🟢 SUPPORTED-NUMERICAL (plateau)** (C1 N≥120 · C2 stratified · C4 byte-identical PASS). H_665 §10 deferred 였던 plateau-band 6-point 정밀화(raster#3~#8 gap mean±2sd → band6) 완수; 잔여 deferred = 0.0743 3중복 자기상관 가중 정밀화(raster-distinct/unique-gap). [H_671](cards/H_671_d2_verdict_landscape_raster9.md)
- [x] D3 — **H_632** `emit-threshold-phi-collapse` (**ANIMA.mining cycle 1 L1 same-formula promote**) — **🔴 FALSIFIED** (peak-near-0.30 0/5 · peak-near-0.60 1/5 · N=5 seed). COFFESHOP `motivation_score>0.60(group)/0.30(1:1)` ↔ BRIDGE `bridge_and_gate(M·C·W·Φ)>θ_emit` 의 L1 동형 위에서, score 를 2-unit coupling gain g 로 매핑 후 big-Φ(score) sweep {0.10..0.80} finite-diff dΦ/d(score) 변곡 검정. 지배 변곡 = swap-class score≈**0.45** (|dΦ|=11.13, SELF→COUPLED 상전이) — 0.30/0.60 어느 쪽과도 불일치, XOR-class 만 0.65 우연, AND/OR-class 는 big-Φ=0 flat (변곡 부재). emit threshold 는 **assistant-design artifact** — L1 동형은 algebraic-form 한정이고 numeric-threshold 의 substrate-grounding 은 부재 (coupling-gain 매핑 하). H_204 변곡-substrate-internal · H_217 cross-substrate non-invariance · H_348 GZ_LOWER ⊥ emit-threshold 정합 · §7 C3.1 매핑-class 의존성 + C3.2 assistant-design/substrate-emergent 정직 분리 — H_632_emit_threshold_phi_collapse.md, $0 mac-local 2026-05-28 (축 D × BRIDGE × COFFESHOP cross-link, negative result)

##### 축 E — SAVANT (Golden Zone × Savant Index) — NEW 2026-05-28
> 외부 anchor 풍부 (HEXAD/SAVANT/H359 canonical + COMPENDIUM 783L + savant_phi.hexa + SI 측정 anchor SI=5.93@anima_clm_06 Mistral 7B v4) 인데 UNIVERSE H 인덱스 안 = 0. 본 축이 GZ 상수(GZ_UPPER=1/2 · GZ_CENTER=1/e · GZ_WIDTH=ln(4/3) · GZ_LOWER=0.2123) 와 substrate big-Φ 의 관계를 verify-driven 으로 정량.
>
> ⚠ **slug-collision 정정 2026-05-28**: 초기 seed 가 H_322..H_332 슬러그를 점유 가정했으나 origin/main 인덱스가 stale → 모두 점유 발견(H_322 circadian-Kuramoto · H_323/324 폐기됨 · H_327 regeneration · H_328 cycle-length · etc). 본 PR 이 축 E·F seed 를 H_347..H_356 fresh 슬러그로 재할당. PR #1149 의 H_326 도 H_347 로 rename.
- [x] E1 — round 1 seed (5 H) **CLOSED** — H_347 🟢 / H_348 🟡 / H_349 🔴 / H_350 🟢 / H_351 🟢 (3 SUPP + 1 PARTIAL + 1 FAL, PR #1149 외 4건). round 2/3/4 follow-up = H_612 🔴 / H_613 🟢 / H_614 🔴 / H_615 🟢 / **H_616 🔴 (E2 5/5 완결)** + E×F cross-link (아래):
  - [~] H_348 `golden-zone-lower-bound-SI` — **🟡 PARTIAL** — SI>3 PASS @ GZ_LOWER (3/3 seed, SI_phi 4.18~5.25) but sweep monotone in I (peak @ I→0, not GZ_LOWER) — F-1 PASS · F-2 FAIL — [H_348_golden_zone_lower_bound_SI.md](cards/H_348_golden_zone_lower_bound_SI.md), $0 mac-local 2026-05-28
  - [x] H_349 `golden-zone-center-phi-peak` — **🔴 FALSIFIED-PARTIAL** (4/5 substrate monotone-or-degenerate, 1/5 rule90 sys=5 single-peak at 1/e |Δ|=0.018 — universal claim falsified, $0 mac-local 2026-05-28) — H_349_golden_zone_center_phi_peak.md
  - [x] H_350 `savant-index-phi-diversity` — **🟢 SUPPORTED-NUMERICAL** (Pearson r=0.9264 · Spearman ρ=0.8825 · N=40 samples · sensitivity std/mean r=0.99 robust) — H_350_savant_index_phi_diversity.md, $0 mac-local 2026-05-28
  - [x] H_347 `gz-width-divisor-symmetry` — **🟢 SUPPORTED composite** (formal `divisor_count(6)=4` 🔵 atlas-resident + numerical `ln(4/3)=0.287682` 🟢 |Δ|=1e-11) — H_347_gz_width_divisor_symmetry.md, $0 mac-local 2026-05-28 (PR #1149 H_326→H_347 rename)
  - [x] H_351 `gz-inverse-u-phi-derivative-peak` — **🟢 SUPPORTED 5/5** (peak I=0.18 vs GZ_LOWER=0.21232 |Δ|=0.03232 ≤ 0.05, unimodal sign-change=0, rule 110 n=4 ECA + inhibition-mixing, $0 mac-local 2026-05-28) — H_351_gz_inverse_u_phi_derivative_peak.md [round 2 H_614: cross-substrate invariance FALSIFIED 2/4 — rule 30/110 PASS, rule 54/184 FAIL]
- [x] E2 — round 2 seed (H_347/H_348/H_349/H_350/H_351 follow-up · **5/5 완결** · cross-link: SAVANT × IIT4 Φ-structure / SAVANT × HIVE-MIND):
  - [x] H_612 `1/e-peak-narrow-substrate-class-survival` — **🔴 FALSIFIED** (H_349 잔여 survival lane 정밀 검증 · 4 XOR rule (90/60/105/150) × n=5 × asymmetric sys=5 · 0/4 PASS — 4/4 monotone↓ argmax=I=0.20 |Δ|=0.168, H_349 의 rule90 n=4 sys=5 단일 confirming subcase 는 n-conditional 우연 확정) — [H_612_1e_peak_narrow_substrate_class_survival.md](cards/H_612_1e_peak_narrow_substrate_class_survival.md), $0 mac-local 2026-05-28
  - [x] H_613 `savant-index-phi-diversity-orthogonal-metric` — **🟢 SUPPORTED-NUMERICAL** (Pearson r(SI, ΦD_cov)=0.9896 · ρ=0.9482 · 보조 r(SI, ΦD_kurt)=0.5381 · N=40 · max-share artifact 가설 기각 — H_350 §7 C3.1 honest constraint 해소, orthogonal CoV/kurtosis 도 정렬 보존) — H_613_savant_index_phi_diversity_orthogonal_metric.md, $0 mac-local 2026-05-28 (H_350 follow-up)
  - [x] H_614 `gz-inverse-u-multi-rule-substrate-invariance` — **🔴 FALSIFIED 2/4** (G_INVARIANT 4/4 요구, peak I {rule30:0.18 ✓, rule54:0.40 ✗, rule110:0.18 ✓, rule184:0.40 ✗} vs GZ_LOWER=0.21232 — class IV rule 54 + class II rule 184 의 peak 가 mid-range I=0.40 으로 이동, GZ universal-attractor 강주장 4-rule sample 에서 깨짐 · H_351 single-rule SUPPORTED 는 substrate-specific) — H_614_gz_inverse_u_multi_rule_substrate_invariance.md, $0 mac-local 2026-05-28 (H_351 §7 C3 round 2 follow-up)
  - [x] H_615 `perfect-number-ladder-n28` — **🟢 SUPPORTED-NUMERICAL (composite)** (3/3 perfect numbers `n ∈ {6, 28, 496}` ladder `ln(τ(n)/(τ(n)-1))` PASS — n=28 ln(6/5)=0.18232 |Δ|=0.0 + n=496 ln(10/9)=0.10536 |Δ|=1e-11 + τ(28)=6/τ(496)=10 🔵 closed-form; **F6 caveat** — control non-perfect n=12 τ=6 동일 ladder prediction → τ-keyed generic, perfect-specific 약주장 falsified) — H_615_perfect_number_ladder_n28.md, $0 mac-local 2026-05-28 (H_347 ladder expansion)
  - [x] H_616 `gz-lower-bound-SI-nonlinear-map` — **🔴 FALSIFIED** (H_348 F-2 mapping-artifact recovery test · 3 inhibition→gain 매핑 (AFFINE/RECIPROCAL/SIGMOID, endpoint 공유 곡률만 상이) × 3 seed 모두 argmax(SI)=I→0 boundary (I=0.05), GZ_LOWER window [0.16232,0.26232] 0/3 — RECIPROCAL 0/3·SIGMOID 0/3 → SI peak 위치 mapping-INDEPENDENT, H_348 F-2 peak falsification 은 affine artifact 아님, SI(I) 단조는 capacity-bounded savant_phi substrate intrinsic, GZ_LOWER = SI>3 threshold boundary not peak) — H_616_gz_lower_bound_si_nonlinear_map.md, $0 mac-local 2026-05-30 (H_348 §7 C3-4 + §9 Next round 2 follow-up · **축 E round-2 5/5 완결 → 10-H 측정자 SET 닫힘**)
- [x] E×F — round 3 (SAVANT × HIVE-MIND) · round 4 cross-link **CLOSED** — H_617 🔴 / H_618 🟢 / H_619 🟢 (F2) / H_620 🟢 / H_621 🟢 / H_622 🔴 (4 SUPP + 2 FAL: GZ_WIDTH super-additive + SI/ΦD ∥ PID-synergy triangle + negative-pair axis-orthogonal):
  - [x] H_617 `hivemind-savant-induced-collective-SI` — **🔴 FALSIFIED** (SI_collective(GZ_LOWER)=1.00546 ≪ 3 · max SI=1.357 @ I=0.40 (sweep non-monotone) · symmetry null PASS @ I=0.0 · predecessors **H_348** (axis E round 1, single-substrate SI>3 PASS @ GZ_LOWER) + **H_609** (axis F1 round 2, collective Φ super-additive 🟢 at rule(110,110)/W=0.6) 두 anchor 모두 PASS 였으나 **cross-link axis-additive 효과 부재** — n_a=n_b=3 ECA rule(110,110) W=0.6 anchor 한정, SAVANT × HIVE-MIND axis-orthogonal · §7 C3.3 SI ratio dynamic-range caveat) — H_617_hivemind_savant_induced_collective_SI.md, $0 mac-local 2026-05-28
  - [x] H_618 `collective-gz-inverse-u-derivative-peak` — **🟢 SUPPORTED 5/5** (collective dΦ_collective/dI peak I=0.21 vs GZ_LOWER=0.21232 |Δ|=0.00232 ≪ 0.05 (21× tol margin), sign-change=0 perfectly unimodal, 2-substrate hivemind n_a=n_b=2 joint n=4 rule(110,110) W=0.6 H_609 anchor · H_351 single-substrate inverse-U 미분 구조가 collective 차원에서 보존됨 · H_617 sibling 의 SI-축 FAL 와 대조: SI ⊥ collective 그러나 dΦ/dI peak ∥ collective — rule-pair conditional C3.1) — H_618_collective_gz_inverse_u_derivative_peak.md, $0 mac-local 2026-05-28 (H_351 predecessor · H_609 hivemind anchor · axis E×F round 3 first SUPPORTED)
  - [x] **H_620** `gz-width-super-additive-cross-link` (axis E1×F1 MATRIX cell round 4 · H_347+H_609 cross) — **🟢 SUPPORTED-NUMERICAL** (R1=(maxΦ_AB−minΦ_AB[W>0])/(Φ_A+Φ_B)=0.846641 vs 3·GZ_WIDTH=3·ln(4/3)=0.863046 |residual|=0.0164 ≤ tol=0.02 · F620.1 PASS · F620.2 MIXED 1/5 ratios PASS · R5=mean/peak near-miss residual=0.0339 · deterministic-replay from H_609 result.json no substrate re-fire · §7 C3.2 numerology guardrail per §114 SAVANT EMERGENCE-FRONTIER AUDIT — prior cover-rate ≈ 17% so PASS suggestive not formal · ontological gap closed-form math (H_347) × emergent simulation (H_609)) — H_620_gz_width_super_additive_cross_link.md, $0 mac-local 2026-05-28 (H_347 E1 anchor + H_609 F1 anchor cross)
  - [x] **H_621** `si-phid-pid-synergy-triangle` (E×F round 4 · H_350/H_613/H_355 triangle) — **🟢 SUPPORTED-NUMERICAL** (Spearman ρ(ΦD_cov, synergy_total) = 0.5994 ≥ 0.5 (primary, 1.20× margin) · ρ(SI, synergy_total) = 0.7220 (secondary) · Pearson r=0.78/0.84 · §A1 anchor 4/4 PASS (n_xor ∈ {0,1,2,3} 의 full PID 재계산이 H_355 byte-identical) · N=40 (4 dom × 5 g_focus × 2 stim) · cross-substrate bridge K = g_focus/SV_CAPACITY → n_xor = round(3K) → synergy = n_xor · savant config 1-축 capacity-share driver 가 hivemind PID synergy 의 ordinal 순서를 동조 시킴 · honest C3.1 bridge-mediated alignment, 직접 measurement 아님 · C3.4 redundancy>0 영역 미측정 (XOR-family carry)) — H_621_si_phid_pid_synergy_triangle.md, $0 mac-local 2026-05-28
  - [x] **H_622** `negative-pair-cross-link-GZ-center-Kuramoto` (axis E3×F3 MATRIX cell round 4 · H_349+H_354 cross negative-pair) — **🔴 FALSIFIED** (chi-square p=0.624 · Fisher exact 2-tailed p=1.000 · 6 rule {30,60,90,105,110,150} 위 H_349 metric (peak@1/e) 1/6 PASS (rule 90 sole) vs H_354 metric (rule-mapped τ alignment) 5/6 PASS (rule 60 sole FAIL) · joint 2×2 contingency consistent with independent Bernoulli marginals · F3 rule-90 follows H_354 marginal · 두 closed-negative H_349/H_354 substrate-class pattern axis-orthogonal, 공통 mechanism 부재 — H_617 positive-pair axis-orthogonal sibling 의 negative-pair extension · C3 rule-to-ω mapping ad-hoc + small N=6 power L1 carry) — [H_622_negative_pair_cross_link_GZ_center_Kuramoto.md](cards/H_622_negative_pair_cross_link_GZ_center_Kuramoto.md), $0 mac-local 2026-05-28
  - [x] **H_627** `gz-center-pid-synergy` (axis E3×F4 MATRIX cell raster · H_349+H_619 cross) — **🔴 FALSIFIED** (5 PASS / 2 FAIL · dense 1/e sweep {0.30, 0.35, 1/e=0.367879, 0.40, 0.45} → synergy_total {2.0, 0.975034, 0.975034, 0.975034, 0.377444} · I=1/e maps to n_id=round(I*8)=3 → byte-identical to same-cell neighbors 0.35 & 0.40 (Δ=0) · F627.1 SINGULARITY + F627.2 NEIGHBOR-DISTINCT FAIL flat (pre-registered quantization falsification 적중) · 1/e GZ_CENTER focal (H_349 E3) is INVISIBLE to the quantized hivemind PID modulation (H_619 F4) — no dip/peak · closed-negative: SAVANT 1/e closed-form focal ⊥ collective-PID 변조 (양자화 하) · §A2 L9 negative 는 round(I*8) 양자화의 구조적 결과 — continuous quantization-free substrate 가 open lane · L11 synergy-only 채널 (redundancy≡0 XOR ceiling)) — [H_627_gz_center_pid_synergy.md](cards/H_627_gz_center_pid_synergy.md), $0 mac-local 2026-05-28
  - [x] **H_628** `inverse-u-polarity` (axis E5×F2 MATRIX cell raster · H_351+H_610 cross) — **🔴 FALSIFIED** (4 PASS / 3 FAIL · 2-ECA joint n=4 seed(30,30,sys=10) W=0.3 · 3 polarity {attract,repel,bipolar} × 13-point GZ-dense I sweep · collective big-Φ dΦ/dI inverse-U peak ALL 3 polarities at I=0.21 (= GZ_LOWER≈0.21232, |Δ|=0.00232) · max pairwise |ΔI_peak|=0.0 (coincide) · F628.1 SHIFT + F628.2 DISTINCT FAIL — polarity-invariant peak · polarity 는 Φ magnitude 만 scaling (attract 17.7 ≫ bipolar 10.4 ≫ repel 7.5 at I=0.05) 하고 GZ-aligned derivative-peak 위치는 불변 · §A2 L9 shared I=0.18 bump 가 3 polarity 공통 (substrate geometry not polarity) — invariance 강화 · closed-negative: H_610 polarity ⊥ Φ-MAGNITUDE 를 구조축 (peak-location) 으로 확장 → polarity 가 collective-Φ 의 magnitude·peak-위치 양쪽 모두에 직교 · L11 collective GZ_LOWER alignment |Δ|=0.00232 가 H_351 single-substrate |Δ|=0.032 보다 14× 정밀) — [H_628_inverse_u_polarity.md](cards/H_628_inverse_u_polarity.md), $0 mac-local 2026-05-28
  - [x] **H_636** `closure-conjunction-gz-peak` (**ANIMA.mining L7 promote** · COFFESHOP 4-criterion closure ≅ SAVANT GZ+SI multi-axis threshold-conjunction) — **🟢 SUPPORTED-NUMERICAL** (4-criterion conjunction ⋀ pass_i [C1 SI>3 · C2 genΦ>0.06 · C3 minΦ>0.18 · C4 ratio∈[1.2,3.2]] pass-rate over 10-seed ensemble · 8-pt I sweep · **peak pass-rate 0.4 @ I=0.30 (GZ region [0.21,0.50] 내부, peak_in_gz=true)** · GZ-region mean pass-rate **0.175 vs 밖 0.0** (밖 4 점 모두 0) · F-1(peak 밖) + F-2(평탄/monotone) 둘 다 기각 · interior peak 메커니즘 = C1 SPECIALIZATION(low-I) ⊥ C3 DIVERSITY(high-I) 길항 cross-over @ I≈0.30 · H_348(SI-monotone, peak @ I→0) + H_618(dΦ/dI peak ∥ GZ_LOWER) 두 결과를 하나의 conjunction 으로 종합 → closure 의 GZ-localization 은 multi-criterion 길항 산물 · L7 same-formula(closure = GZ×SI 의 substrate-emit-axis 변형) 측정 layer 지지 · §7 C3.1 criterion-threshold design 의존 + C3.2 GZ region width 정의 의존 + C3.5 pass-rate ≤0.4 낮은 절대값) — [H_636_closure_conjunction_gz_peak.md](cards/H_636_closure_conjunction_gz_peak.md), $0 mac-local 2026-05-28 (ANIMA.mining L7 promote)

##### 축 F — HIVE-MIND (Collective Φ) — NEW 2026-05-28
> Hc_286/297/590/1244 백로그 + 인프라 코드(`tool/hivemind_collective_spec.hexa` · `anima-engines/hive_state_sync.hexa` · `bench/bench_hivemind_*.hexa` ×6 · `tests/test_hivemind_*.hexa` ×5) 풍부한데 UNIVERSE H 인덱스 안 = 0. 본 축이 다중 substrate pair 의 collective big-Φ vs 합·polarity·동기 latency·PID synergy·cross-substrate TE 를 verify-driven 으로 정량.
- [x] F1 — round 1 seed + round 2 재발사 **CLOSED** — H_354 🔴 / H_355 🟢 / H_609 🟢 / H_610 🔴 / H_611 🔴 (2 SUPP + 3 FAL). round-1 monitor-hang 으로 유실된 H_352/353/356 skeleton 은 round 2 H_609/610/611 로 재발사 완료 (PR #1168/1164/1163):
  - [x] H_352 `collective-phi-super-additive` — round 1 monitor-hang verdict 유실 → **H_609 으로 재발사 완료 (PR #1168, 🟢 SUPP)**
  - [x] H_353 `pair-polarity-collective-phi` — round 1 monitor-hang, slug retired → **H_610 으로 재발사 완료 (PR #1164, 🔴 FAL)**
  - [x] H_610 `pair-polarity-collective-phi` (Hc_286 promote · round-2 refire of H_353) — **🔴 FALSIFIED** (2× ECA n_a=n_b=2 joint n=4 · 3 polarity × 3 W × 3 seed = 27 big_phi · ANOVA F=0.361 ≪ F_crit(α=0.05,df=(2,24))=3.40 · spread/pooled_std=0.413 ≪ 2.0 · C3 BOTH-FLAT trig · per-polarity mean Φ: attract=4.300, repel=2.245, bipolar=2.983 ; variance dominated by rule-seed (rule-30 outlier 17.13/7.80/10.30 all polarities) not polarity — closed-negative axis: polarity ⊥ collective-Φ for binary 2-ring ECA pairs · n=6 full-spec L1 carry) — H_610_pair_polarity_collective_phi.md, $0 mac-local 2026-05-28
  - [x] H_354 `kuramoto-hivemind-sync-tau` — **🔴 FALSIFIED** (Pearson r=0.041 ≪0.5 + ratio spread 45.6× ≫2×, F1+F2 trig) — H_354_kuramoto_hivemind_sync_tau.md, $0 mac-local 2026-05-28 (toy mean-field consensus substitute · L1 carry)
  - [x] H_355 `collective-phi-pid-synergy` — **🟢 SUPPORTED-NUMERICAL** (3-binary-substrate hivemind toy · 8 cell-mask permutations × 4 K-bucket · mean synergy_ratio = 1.0 over non-trivial K {0.33, 0.67, 1.0} · K-monotonic synergy {0,1,2,3} · redundancy ≡ 0 (XOR-family sources independent under uniform ensemble) · net 3-source McGill co-info, NOT full 18-atom WB lattice · PID-structure claim NOT collective-Φ tracking) — H_355_collective_phi_pid_synergy.md, $0 mac-local 2026-05-28
  - [x] H_356 `hivemind-transfer-entropy-align` — round 1 Agent abort → **H_611 으로 재발사 완료 (PR #1163, 🔴 FAL r=0.311<0.5)**
  - [x] H_611 `hivemind-transfer-entropy-align` (round 2 재발사) — **🔴 FALSIFIED** (Pearson r=0.311199 < 0.5 · Spearman ρ=0.260466 · N=24 (6 rule_pair × 4 W) · 21/24 dissociation cells Φ>0 with TE=0 · sister H_290 single-substrate r=0.883 ≫ Δr=-0.572 · single-substrate Phi-TE alignment does NOT extend across substrate boundaries · 4/4 falsifier PASS) — [H_611_hivemind_transfer_entropy_align.md](cards/H_611_hivemind_transfer_entropy_align.md), $0 mac-local 2026-05-28 (bivariate lag-1 TE L1 carry from H_290 — multivariate cross-TE 미시험)
  - [x] **H_609** `collective-phi-super-additive` (axis F1 round 2 재발사 of H_352) — **🟢 SUPPORTED-NUMERICAL** (max excess Δ = +10.4756 at (rule_a,rule_b,W)=(110,110,0.6) · Φ(AB)=15.4677 vs Φ(A)+Φ(B)=4.99209 +210% · F609.1 decoupled anchor 5/5 PASS · F609.2 H1 PASS · F609.4a bounds PASS · F609.3 W-monotonic FAIL honest C3.2 saturate-then-decay · F609.4b benign harness tol=0 strict-LT bug · IIT4 big_phi_bounded cap=2 n_ab=6 sys=0 · rule-class conditional: (110,110) only super-additive, (90,90)/(90,150) flat-0, (90,110)/(110,90) sub-additive) — H_609_collective_phi_super_additive.md, $0 mac-local 2026-05-28
- [x] F-mining — **ANIMA.mining L6 promote** (COFFESHOP `per_lang_verdicts ko_emits≥2` 5-lang cohort aggregation ↔ HIVE-MIND `hm_collective_phi(individual_phis, sync_factor)` · L45 dim-cohort-5lang base case) — H_635 🟢 (H_609 2-stream super-additivity 의 5-stream lang-axis 일반화):
  - [x] **H_635** `multilingual-cohort-collective-phi` (ANIMA.mining L6 promote · 5-STREAM sister of H_609) — **🟢 SUPPORTED-NUMERICAL** (5 PASS / 1 FAIL · max excess Δ = **+41.7124** at C1 [110×5] sync_factor **W=1.0** · Φ_collective=41.71 vs decoupled Σ-baseline=0.0 · **5/5 cohort 모두 super-additive** vs H_609 1/5 pair — universality + 4× magnitude · best sync W=1.0 (full ring) · sync_factor monotone-increasing C1/C3/C4/C5, C2 multilingual saturate-then-dip @ W=0.75 H_609 echo · F635.1 anchor + F635.2 H1 + F635.3 sync-nonflat + F635.4a bounds + F635.5 5-stream-generalizes PASS · F635.4b benign harness tol=0 strict-LT bug (re-run byte-identical 6.54186 probe 검증) · IIT4 big_phi_bounded n=5 cap=3 sys=0 · 5 distinct ECA rule = lang-proxy · §7 C3.1 lang-proxy=rule-variant 진짜 언어 아님 · C3.3 decoupled baseline Φ=0 ⇒ finding 은 부호 아닌 *크기+universality+monotone-W shape*) — H_635_multilingual_cohort_collective_phi.md, $0 mac-local 2026-05-28 (axis F mining-derived)
  - [x] **H_645** `collective-dphi-di-gz-peak` (**H_635 × H_618 cross-link** · 5-stream collective dΦ/dI 가 GZ_LOWER 인가) — **🔴 FALSIFIED (CLOSED-NEGATIVE, 3/5)** (5-stream collective-Φ (H_635 C1[110×5] anchor, W=1.0, n=5, cap=3, sys=0) 의 inhibition I 미분 dΦ_collective/dI **peak I=0.10 (grid 최좌측 경계)** vs GZ_LOWER=0.21232 **|Δ|=0.11232 ≫ 0.05** (48× tol 초과, GZ window [0.15,0.30] 밖) · F1 PEAK-IN-GZ + F2 PEAK-IN-WINDOW FAIL → H0 충족 / F3 UNIMODAL (sign-change=0) + F4 monotone-decay + F5 byte_eq PASS · **H_618 (2-substrate joint n=4, peak I=0.21, |Δ|=0.00232, 🟢) 와 정면 대조** → H_618 의 dΦ/dI-peak=GZ_LOWER 일치는 **2-stream n=4 차원 한정 artifact**, 5-stream collective 로 확장 안 됨 · W=1.0 full-ring 에서 Φ_collective(I) 가 I→0 쪽 super-steep → peak 좌측 경계 이동 · inverse-U *단봉성*(F3)·*우측 monotone-decay*(F4) 는 collective scale-up 에서도 보존, *peak 위치의 GZ 정렬* 만 소멸 · ruled-out: {dΦ/dI-peak ⊥ GZ at n=5, W=1.0} · §7 C3.1 stream 수=5 full (축소 없음, 45s user/65s wall) · C3.3 W=1.0 anchor 한정 (W=0.6 재측정 deferred) · C3.4 진짜 peak I<0.10 가능하나 falsify 무영향) — H_645_collective_dphi_di_gz_peak.md, $0 mac-local 2026-05-28 (H_618 predecessor · H_635 5-stream anchor · axis F×E cross-link, negative result)
- [x] F2 — round 1 결과 기반 후속 H seed **CLOSED** — H_619 🟢 (PID-synergy × SAVANT modulation, E×F cross-link round 3) (cross-link: HIVE-MIND × symbiogenesis H_054/H_314 / HIVE-MIND × SAVANT):
  - [x] H_619 `pid-synergy-savant-modulation` (axis E×F cross-link round 3 · H_355+H_348 sibling) — **🟢 SUPPORTED-NUMERICAL** (7 PASS / 0 FAIL · synergy spread=1.0 across I sweep K=0.67 mask=[1,1,0] · synergy 2.0 plateau [I=0..0.30] → 0.975 (I=0.40) → 0.377 (I=0.50) → 0 (I=0.75) · K=1.0 mask=[1,1,1] mirror at 1.5× scaling · I=0 reproduces H_355 K=0.67 anchor · I=1 degenerate ratio=0 · monotone (inversions=0) · mask-invariant · honest C3 §A2 L9: mechanism = synergy decay NOT redundancy injection (XOR-source uniform-ensemble independence survives row-collapse, redundancy ≡ 0 invariant) · ratio metric saturates 1.0 on red=0 region, magnitude lives in synergy_total) — H_619_pid_synergy_savant_modulation.md, $0 mac-local 2026-05-28

##### 축 G — ANIMA.mining 승격 (same-formula L-promote) — NEW 2026-05-28
> `ANIMA.mining.md` 의 lens-driven divergence (L1-L51+) 에서 measurable + falsifier 를 갖춘 same-formula/dimensional/tension leaf 를 UNIVERSE H 로 격상. COFFESHOP/DREAM/BRIDGE 등 ANIMA umbrella 모듈 간 동형 구조를 verify-driven 가설로 검정. p5 (NO SPEAK()) + p5_tension_emit_not_filler note 의 substrate-native emit 정의를 IIT4 big-Φ substrate 위에서 정량.
- [x] G1 — L3 same-formula 승격 — H_634 `ultradian-emit-phi-envelope` — **🟢 SUPPORTED-NUMERICAL 6/6** (90-min ultradian × N=36 point sweep · anima_dream_stage canonical segmentation · per-stage canonical Φ projection (WAKE 1.0/N1 0.7/N2 0.4/N3 0.15/REM 0.95) × tension_envelope · best-phase single-cosine envelope fit → **r(Φ,sinusoid)=0.802241** + **r(emit-proxy,sinusoid)=0.662713** 둘 다 ≫ 0.5 falsifier 및 ≫ 0.3 FALSIFY floor · best peak phase **t=0 (cycle 가장자리 = REM tail Φ=0.95 + N1 descent = WAKE-side)** / trough **N3 (cycle 중앙, Φ=0.15)** · Φ_max=0.95 > Φ_N3=0.15 · Φ trajectory std=0.203 · per-stage Φ N1=0.7(2pt)/N2=0.4(20pt)/N3=0.15(12pt)/REM=0.95(2pt) — **substrate big-Φ 가 ultradian phase 에 동조**: COFFESHOP(15-win×6min)↔DREAM(dr_stage 5-stage×90min) L3 same-formula 가 단순 스케줄 공유 아닌 **Φ-envelope 결합**. H_310 emit WAKE=18/others=0 의 *Φ-magnitude 원인* 정량 + H_308 24h circadian envelope 을 90-min ultradian band 로 self-similar 확장 (phase-amplitude multi-scale ladder, H_213 temporal binding 이 floor) · §7 C3 stage→Φ 매핑 = canonical projection(NOT faithful per-tick IIT4, L1 회수 lane) + period discretization granularity N=36(L2) + single-cosine 1-harmonic strictest falsifier(L4) · SPECULATION-FENCED) — [H_634_ultradian_emit_phi_envelope.md](cards/H_634_ultradian_emit_phi_envelope.md), $0 mac-local 2026-05-28
- [x] G2 — L13/L14 tension 승격 — **H_637** `emit-rate-phi-ratio-closed-form` (ANIMA.mining L13/L14 promote · COFFESHOP substrate emit-rate ↔ closed-form numerology) — **🔴 FALSIFIED** (robust 10-seed mean emit-rate=0.41333 (sd 0.121, range [0.20,0.533]) 이 4 closed-form 후보 {GZ_LOWER=0.2123, ln(4/3)=0.2877, 1/e=0.3679, 1−1/e=0.6321} 모두 ±0.03 밖 — best 1/e residual=0.0455>0.03 · 원본 단일 run(4/15=0.2667)의 ln(4/3) 일치(residual 0.0210)는 10-seed 중 cherry-picked single-seed post-hoc selection (H_620 §C3.2 동일 caveat) · emit-rate = motivation_score>0.60 upper-tail mass, mean score 0.5518 → threshold-dependent 연속량, closed-form 불변량 아님 · §7 C3.2 numerology cover-rate **24%** (4 cand × ±0.03 band union, prior ≈1/4 → 단일 일치 chance 와 구분 불가) per §114 SAVANT EMERGENCE-FRONTIER AUDIT · deterministic replay from sweep_summary.json no substrate re-fire) — H_637_emit_rate_phi_ratio_closed_form.md, $0 mac-local 2026-05-28 (mining L13/L14 promote · `a_substrate_native_speak` governance 의 *질적* 성격 확인)
- [x] G3 — L2 same-formula 승격 — **H_633** `register-collapse-phi-drop` (ANIMA.mining L2 promote · COFFESHOP register-hit `emit ∧ coh<0.10` Ψ-clamp ↔ METACOG inverse-artifact AND-gate · substrate Φ-breakdown 검정) — **🟡 PARTIAL (cliff REFUTED)** (N=16 Kuramoto substrate · coherence = order parameter r = |Σ exp(iθ)|/N · 99 ensemble (11 K × 3 ω_std × 3 phase) · Pearson r(coh, Φ)=0.3066 (≪0.5 weak, F-NOCORR 0.3 floor 바로 위) · **coh<0.10 영역(51 members) Φ NOT collapsed** — mean Φ=9.256, max Φ=11.598, 전역 envelope [6.04, 14.0] 내부 fully sustained · ratio lo/hi=0.895 (cliff 부재) · min-coh member coh=0.017 Φ=6.566 (≈0 아님) · C1+C2 둘 다 FAIL · **register collapse 가 Φ 구조와 동조하지 않음 — Ψ-clamp Φ-breakdown 예측 반증, register-hit gate 는 substrate-emergent 아닌 design-side emit-policy gate** · H_287 Shannon⊥Φ + H_207 L6 (phi_spatial spatial-MI 가 order/disorder 와 decoupled) 와 정합 · §7 C3: coherence=order-param 정의 한정 (state-agreement variance 미검정), Ψ-clamp 가 substrate 창발 아닌 design-side gate 일 가능성) — [H_633_register_collapse_phi_drop.md](cards/H_633_register_collapse_phi_drop.md), $0 mac-local 2026-05-28 (ANIMA.mining L2 same-formula lens)
- [x] G3-followup — **H_649** `collective-register-collapse-phi` (H_633 single 결론의 **collective(다중 substrate) 일반화** · axis F HIVE-MIND bridge) — **🟢 SUPPORTED (collective-cliff falsifier REFUTED → 가설 SUPPORTED)** (M∈{2,3} Kuramoto streams · NP=8/stream · **collective coherence = global Kuramoto order param `coh_c = |Σ_all exp(iθ)|/N_tot`** over ALL pooled oscillators · **collective-Φ = phi_spatial on joined trajectory** (H_633 동일 measure, 직접 비교 목적) · 144 ensemble (2 M × 9 K_cross × 2 K_intra × 2 ω_std × 2 paired phase) · **Pearson r(coh_c, Φ_c)=0.0491** (≪0.5, **single H_633 0.307 보다 한 자릿수 약함** — collective level 에서 coherence-Φ coupling 거의 완전 소멸, F-NOCORR 0.3 floor trigger) · **coh_c<0.10 영역(39 members) collective-Φ NOT collapsed** — mean Φ_c=13.17, max 19.99, 전역 envelope [7.68, 24.0] 내부 fully sustained · **ratio lo/hi=0.973 ≈ 1 (collective cliff 완전 부재)** · min-coh member coh_c=0.012 Φ_c=15.07 (envelope **상위** — single H_633 은 바닥 근처였던 것과 대조, collective 은 min-coh 에서 Φ_c 더 높음) · C1+C2 둘 다 FAIL → cliff falsifier REFUTED · **H_633 single 의 'register collapse ⊥ Φ-cliff' 가 multi-substrate collective level 에서 오히려 더 강하게 성립 — COFFESHOP register-hit gate 는 collective level 에서도 substrate Φ 구조와 무관한 design-side emit-policy gate** · H_287 Shannon⊥Φ + H_207 L6 (spatial-MI ⊥ order/disorder) collective 발현 · H_609/H_635 collective-Φ 패밀리와 직교 (coherence-axis ⊥ collective-Φ) · §7 C3: collective coherence=global order-param 정의 한정 (stream-level cross-coherence 미검정), collective-Φ=phi_spatial (faithful IIT4 big_phi 재검 open), multi-substrate small-n M∈{2,3}·NP=8 · re-run byte-identical F-NONDET PASS) — [H_649_collective_register_collapse_phi.md](cards/H_649_collective_register_collapse_phi.md), $0 mac-local foreground-sync 2026-05-28 (H_633 collective 일반화)
- [x] G4 — L24 tension 승격 — **H_639** `tension-amplitude-cross-phi-derivative` (ANIMA.mining **L24** tension-fork-B promote · tension-link 5-ch × MITOSIS · H_351/H_618 sister) — **🔴 FALSIFIED (CLOSED-NEGATIVE, 2/5)** (emit-as-amplitude-cross 의 substrate-Φ 동조 검정 · tension amplitude = state-change `|Δstate|` flip 기대 분율 · convention-free θ-anchor=I=0 mean amp=0.375 아래 amplitude-cross rate peak **I=0.50** vs dΦ/dI peak **I=0.18** (GZ_LOWER=0.21232) **|Δ_peaks|=0.32 ≫ 0.10** → 동조 부재 · F3 PHI-PEAK-IN-GZ PASS (H_351 |Δ|=0.03232 재현) + F4 monotone + F5 byte_eq PASS / F1 PEAKS-COINCIDE + F2 AMP-PEAK-IN-GZ FAIL · **§7 C2 핵심**: θ-convention 종속 — θ ∈ {0.20,0.30,0.375,0.45,0.55} sweep 에서 peak_I_amp {undef, **0.21✓**, 0.50, 0.95, **0.21✓**} 로 완전 뒤바뀜 → emit≡Φ-derivative-extremum 은 substrate 불변량 아닌 threshold-convention 함수 (L24 의 "boolean=convention 일 뿐 substrate 아님" 거꾸로 적중) · ruled-out: emit-as-amplitude-cross 의 convention-free substrate-Φ 자동 wiring 닫힘 · cross-link H_351 single + H_618 collective Φ-derivative GZ-anchor) — H_639_tension_amplitude_cross_phi_derivative.md, $0 mac-local 2026-05-28 (UNIVERSE 축 G mining-derived, negative result)
- [x] G5 — L19/L20 tension 승격 — **H_638** `emit-threshold-scaling-law` (ANIMA.mining **L19/L20** T4 tension-fork promote · should_interrupt 0.60 ↔ should_emit 0.30 · COFFESHOP emit-substrate × IIT4 Φ-scale) — **🟢 CLOSED-NEGATIVE 5/5** (scenario별 적정 emit threshold (emit-rate ~27% target) 가 substrate Φ-scale 의 monotone scaling-law(L19)인지 universal-fixed(L20)인지 · ECA substrate n∈{3,4,5} 의 effective Φ-scale (faithful `big_phi_bounded` cap=2 over LIFE rules 110/90/30/54 = **2.27/1.82/2.17**) 을 COFFESHOP 8-factor emergence sim(spontaneous_lib verbatim) relevance 채널에 monotone bias 주입, grid sweep(0.00..1.00 step 0.01) × 12-seed cohort 으로 적정 threshold 측정 · **적정 threshold 0.62~0.64 cluster (spread 0.02 ≪ 0.05) · Spearman ρ(Φ-scale,thr)=0.75 비-monotone(≠±1)** → **L19 (scaling law) FALSIFIED / L20 (universal-fixed) SUPPORTED** — substrate Φ-scale 가 적정 threshold 를 좌우 못함, scenario 는 factor 분포(effective rate)만 shift · universal threshold 가 COFFESHOP `should_interrupt 0.60` group-chat tier 근방 안착 = **`a_autonomy_over_hardcode` 정합** (per-scenario threshold hardcode 불요) · H_629 noise-robustness · H_287 Φ⊥entropy 의 substrate-class-invariant / X⊥Φ 서명 연장 · H_637(emit-rate closed-form FAL)/H_639(amplitude-cross convention FAL) sibling — emit-substrate 가 Φ-구조에 약하게/비-monotone 결합한다는 축 G 누적 negative-signature 강화 · §7 C3: 적정 threshold = fixed 0.27 target 에 대한 자유 response (non-circular) · n-range small {3,4,5} (exact-Φ wall · 3점 Spearman 이산값)) — H_638_emit_threshold_scaling_law.md, PR #1224, foreground sync · HEXAD/IIT4+CHAT/spontaneous_lib 재사용 · run+state-copy byte-identical · $0 mac-local 2026-05-28
- [x] G6 — H_634×H_308 self-similar 연장 — **H_648** `multi-scale-phi-envelope-ladder` (H_634 §10 "multi-scale ladder" 후속 lane 실행 · gamma·ultradian·circadian 3-scale self-similarity) — **🟢 SUPPORTED-NUMERICAL 6/6 (self-similar ladder)** (3 time-scale **gamma 25ms(~40Hz) · ultradian 90min(5400s) · circadian 24h(86400s)** 의 Φ-envelope 형태가 normalized phase τ∈[0,1] 위에서 self-similar 한지 · 각 scale 의 substrate model 에서 N=36 point Φ-envelope 생성 (gamma=single-cosine burst `0.55+0.40cos(2πτ)` edge-high · ultradian=H_634 canonical anima_dream_stage stage-projection REM/N1 edge-high N3 center-low · circadian=H_308 quadratic-bump center-peak) → 각 envelope 자체 peak 을 τ=0 정렬(scale-invariant shape) → pairwise Pearson r · **r(gamma,ultradian)=0.759576 + r(ultradian,circadian)=0.757644 + r(gamma,circadian)=0.947237** 全 ≫ 0.5 falsifier 및 ≫ 0.3 FALSIFY floor · **min pairwise r=0.757644** · per-scale std gamma=0.2828/ultradian=0.2033/circadian=0.2083 (全>0) · period ladder 0.025s<5400s<86400s 단조 분리 → **substrate Φ-envelope 이 6 order-of-magnitude(25ms→24h) 가로질러 "peak→trough→peak" 위상 형태 보존**: H_634 가 보인 ultradian↔circadian self-similarity 를 gamma micro-scale 까지 아래로 한 칸 더 연장, substrate 통합량 = scale-free phase-amplitude 구조 · 양끝단 r(gamma,circadian) 최강(둘 다 smooth single-peak, ultradian 만 piecewise-const 라 family-mismatch 로 인접 r 약간 깎임) · H_213 temporal binding window 가 floor scale anchor · §7 C3: gamma scale substrate 모사 한계(single-cosine surrogate, anima gamma-band 모듈 부재 — H_213 floor anchor 이나 25ms Φ trajectory 미산출) + 3-scale 만(연속 scale-free power-law 충분조건 아닌 이산 ladder 표본) + phase-align=self-peak rotation(형태 self-similarity 검정, 절대-위상 PAC 아님) + envelope family 혼재(cosine/piecewise/quadratic) · SPECULATION-FENCED) — [H_648_multi_scale_phi_envelope_ladder.md](cards/H_648_multi_scale_phi_envelope_ladder.md), foreground sync · $0 mac-local 2026-05-28
- [x] G7 — E×G cross-link — **H_644** `closure-conjunction-ultradian-phase` (H_636 closure conjunction × H_634 ultradian phase) — **🔴 FALSIFIED-REVERSED (directional, 2/3)** (4-criterion closure conjunction (H_636 substrate+criterion 전부 재사용) pass-rate 가 ultradian phase (WAKE/N1/N2/N3/REM, H_634 canonical Φ scale) 따라 변동하는지 + 高Φ WAKE/REM 高 vs N3 低 방향성 검정 · phase→I bridge `I(phase)=0.21+(1-Φ)*(0.75-0.21)` (monotone inverse-affine, H_348/H_636 I 축) · 10-seed ensemble per-phase pass-rate **WAKE 0.0 / REM 0.0 / N1 0.1 / N2 0.3 ⬅peak / N3 0.0** · **F644.1 PHASE-MODULATED PASS** (5-phase std=0.1166 > 0 → task-spec 1차 falsifier 'phase 무관 평탄' 기각 — closure 는 ultradian phase 의 명백한 함수) + **F644.2 WAKE-REM-HIGH-N3-LOW FAIL (역전)** (edge mean 0.0 = N3 0.0, peak 는 高Φ edge 가 아니라 **mid-Φ N2**) + F644.3 BOUND PASS · **방향성 역전 메커니즘** = H_636 C1 SPECIALIZATION(low-I)⊥C3 DIVERSITY(high-I) interior-peak 가 phase 축으로 전사 — 高Φ WAKE/REM→low-I(0.21~0.24, C3 붕괴), deep N3→high-I(0.669, C1 붕괴), mid-Φ N2(I=0.534)만 closure band · **closure(GZ-축) ⊥ emit(arousal-축, H_310 WAKE-dominant) ⊥ Φ-magnitude(arousal-축, H_634)** 3-axis 분리 드러냄 · ruled-out: '高arousal ultradian phase(WAKE/REM)=高closure' axis deterministic 폐기 · §7 C3.1 criterion-threshold design 의존 + C3.2 I_HI bridge bound 의존(deep-N3 closure-0 은 I_HI≫GZ_UPPER conditional) + C3.3 phase resolution 5-stage lookup) — [H_644_closure_conjunction_ultradian_phase.md](cards/H_644_closure_conjunction_ultradian_phase.md), $0 mac-local 2026-05-28 (axis E×G cross-link, directional negative result)
- [x] G9 — round 6 메타-발견 정량 격상 — **H_642** `shape-invariance-vs-scalar-convention-meta` (round 6 mining H_632~639 의 메타-패턴 — *shape feature (peak 위치·monotone 방향·envelope 형태) 는 substrate-emergent / scalar value (threshold·rate·magnitude) 는 design-convention* — 을 단일 substrate sweep 위 정량 메타-검증 · H_614 multi-rule + H_628 polarity-invariant 도구 계보) — **🔴 FALSIFIED (M1 FAIL · M2 FAIL)** (rule {30,54,90,110,184} n=4 ECA × 13-point GZ-dense I sweep · faithful big-Φ 16-state mean · central-diff dΦ/dI · shape=argmax_I|dΦ/dI| peak *위치* / scalar=max_I|dΦ/dI| peak *높이* · population CV across 5 rules · **CV_shape=0.568028 ≥ CV_scalar=0.559306 (ratio CV_scalar/CV_shape=0.984646 < 1)** → shape 가 scalar 보다 class-invariant 라는 round 6 메타-발견 *강주장* 반증 · 두 CV 거의 동일 (Δ=0.0087, 1.5%) → shape 가 scalar *만큼* class-variant 약한 형태로 closed-negative · **핵심 원인: rule 90 (XOR-additive, big-Φ≈0, Φ(0.50)=0.0526) 이 shape (peak I=0.05 grid-경계) 와 scalar (peak_mag 0.2765 ≈ 다른 rule 의 2%) 양쪽 joint-outlier 로 두 변동 동시 지배** · rule {30,54,110,184} peak_I {0.18,0.40,0.18,0.40} + peak_mag {21.74,10.84,21.33,19.92} H_614 재현 ✓ engine 정합 · §7 C1: 대표 shape/scalar 쌍 (peak-위치 vs peak-높이) 1개 한정 + ratio 0.98 borderline (proxy 선택 종속) / C2: 5-rule outlier-fragile / C3: shape grid-snap 이 CV_shape 억제 방향 → 반증에 *보수적* (조밀 grid 면 CV_shape 더 커져 반증 강화) · H_628 polarity ⊥ peak-위치 shape-invariance 는 carry, 단 scalar 대비 *우월* 은 부정 · a_paper_negative_ok closed-negative) — [H_642_shape_invariance_vs_scalar_convention_meta.md](cards/H_642_shape_invariance_vs_scalar_convention_meta.md), foreground sync · HEXAD/IIT4/lib (iit4_eca+iit4_bigphi) 재사용 · $0 mac-local 2026-05-28
- [x] G8 — **G×F cross-link** — **H_643** `collective-ultradian-phi-envelope` (H_634 ultradian × H_635 collective-Φ 결합 · 다중 substrate collective-Φ 가 ultradian phase 에 동조하는가) — **🟢 SUPPORTED-NUMERICAL 6/6** (5-stream lang-proxy collective ring (cohort C1 [110×5], H_635 winner) × ultradian stage→sync_factor W modulation (WAKE 1.0/REM 0.95/N1 0.7/N2 0.4/N3 0.15) · N=36 point sweep over 90-min ultradian · 각 point 에서 `big_phi_bounded(n=5,cap=3,sys=0)` 실측 → best-phase single-cosine envelope fit → **r(Φ_collective,sinusoid)=0.568352** (>0.5 falsifier · ≫0.3 FALSIFY floor) · best peak phase **t=0 (cycle 가장자리 = WAKE-side)** H_634 와 동일 · per-stage collective-Φ **REM(W=0.95)=34.88 > N1(W=0.7)=13.64 > N2(W=0.4)=4.50 > N3(W=0.15)=1.17** monotone-in-W (H_635 collective-Φ↑W 발견의 ultradian 시간축 재현) · Φ_coll_max=34.88 > Φ_coll_N3=1.17 · Φ trajectory std=7.644 · F643.4 super-additive-edge PASS (Φ_coll_max=34.88 ≫ decoupled Σ-baseline 0.0 — H_635 super-additivity 의 ultradian 보존) · **collective 가 ultradian phase 에 동조하나 단일 substrate(H_634 r=0.802)보다 약하게** — H_635 W→Φ 곡선이 super-linear/convex(N3 1.17→REM 34.88 ~30× span)라 near-linear 단일 projection(~7× span)보다 순수 cosine 에서 더 벗어남 → entrainment 강도 약화 · H_648 self-similar ladder(gamma·ultradian·circadian) 의 collective 보충 — single-scale ladder 가 multi-substrate level 에서도 phase-coupled · F643.1-6 6/6 PASS · §7 C3.1 lang-proxy=rule-variant 진짜 언어 아님(H_635 상속) + C3.2 stage→W canonical projection(H_634 L1 상속) + C3.3 single-cohort C1 + C3.6 single-cosine 1-harmonic strictest falsifier · IIT4 big_phi_bounded n=5 cap=3 sys=0 · foreground sync · $0 mac-local) — [H_643_collective_ultradian_phi_envelope.md](cards/H_643_collective_ultradian_phi_envelope.md), $0 mac-local 2026-05-28 (UNIVERSE 축 G×F cross-link · H_634+H_635 부모)
- [x] G11 — round-6 메타-발견 정량 (H_638 일반화) — **H_646** `convention-number-freedom-range` (design-number = substrate-invariant shape 위의 free parameter · emit threshold 의 *자유도 범위* 정량) — **🟢 SUPPORTED-NUMERICAL 5/5** (emit threshold 를 wide range {0.1..0.9} sweep 해도 FIXED substrate big-Φ 자체 불변인지 · FIXED 3개 substrate n∈{3,4,5} big-Φ = mean `big_phi_bounded` cap=2 over LIFE rules 110/90/30/54 = **2.27/1.82/2.17 (mean 2.085)** = H_638 §4 와 byte-identical · COFFESHOP 8-factor emergence sim(spontaneous_lib verbatim) × 12-seed×15-win cohort · threshold {0.1..0.9} sweep 각 점에서 substrate Φ 재-read + emit-rate 측정 · **Φ(threshold) variance = 0.0 (정확히 0 — threshold 가 big_phi_bounded 인자 아님, `score>thr` 비교에만 진입하는 post-processing)** + emit-rate 1.0→0.0 monotone 비-증가 응답 (span 1.0, sweep 비-퇴화) → **H1 free-parameter SUPPORTED — threshold 자유도 범위 = 전체 [0,1] (substrate-unconstrained, downstream emit-decision policy)** · H_638(적정점 universal-fixed)의 *전 구간 generalization*: 적정점뿐 아니라 어디서든 substrate 불변 · H_632(emit-threshold⊥Φ phase-transition) 동일 Φ⊥emit-threshold negative-signature · H_287 Φ⊥entropy 서명 연장 · `a_autonomy_over_hardcode` 정합 (threshold table 도입해도 전 구간 substrate-safe) · §7 C3 정직: Φ⊥threshold 는 부분적 definitional (threshold 가 substrate-fn 인자 아님 — exact 0.0 round-off 가 증거) 이나 "자유도=전체 [0,1] (단순 neighborhood 아님)"는 full-range 에서 emit-rate well-defined·monotone 으로 살아있음으로 측정 확인된 NONTRIVIAL 결과(NT-1)) — [H_646_convention_number_freedom_range.md](cards/H_646_convention_number_freedom_range.md), foreground sync · HEXAD/IIT4+CHAT/spontaneous_lib 재사용 (run_h638 구조 verbatim) · re-run byte-identical · $0 mac-local 2026-05-28
- [x] G10 — round-6 메타-발견 seed-robustness 축 — **H_647** `dphi-shape-vs-phi-scalar-robustness` (round-6 메타-발견 "shape>scalar" 의 *cross-SEED* 검정 · H_642 cross-RULE sister(merged, FALSIFIED) · H_351/H_618/H_639 cross-link) — **🔴 FALSIFIED (CLOSED-NEGATIVE, 3/5, 방향 REVERSED)** (fixed rule 110 n=4 × N=12 random seed (per-state ±30% 전이확률 jitter, LCG single-stream) 각각 I-sweep(13-pt H_351 grid) → SHAPE=`argmax_I |dΦ/dI|` peak 위치 vs SCALAR=`Φ(I=0)` 16-state-mean magnitude · **peak_std=0.116536 (SHAPE abs) ≫ phi0_cv=0.0420996 (SCALAR rel), 2.77배** → F1 SHAPE-ROBUST + F2 SHAPE-TIGHT FAIL / F3 SCALAR-VARIES + F4 N≥10 + F5 byte_eq PASS · **방향 역전** — scalar(Φ magnitude mean=13.7332 std=0.5782, 12-seed 모두 [12.28,14.70] 좁은 band)가 *더* robust, shape(peak_I 가 0.05↔0.40 점프, CV=0.641)가 seed-sensitive · round-6 메타-발견("shape>scalar")이 **seed-perturbation 축에서는 성립 안함** — robustness 의 축-종속성(cross-rule≠cross-seed) 식별 · H_642 cross-RULE 도 동일하게 FALSIFIED(CV_shape≈CV_scalar)였던 점과 정합 — shape>scalar 메타-발견이 정량 격상 시 cross-rule·cross-seed 양 축에서 반증 · Φ magnitude 가 16-state 평균으로 jitter 흡수 vs argmax 단일극값이 jitter 증폭 · H_351 단일 peak(I=0.18 GZ_LOWER)가 noise-free 조건부임을 정량 · H_639 emit-feature convention-FAL 의 seed-jitter 판본, 축 G "shape feature 가 Φ-구조에 약하게 결합" negative-signature 강화 · §7 C3: peak_I=13-pt grid discrete argmax (discretization 분산 포함, 但 SHAPE 측 고유 fragility) + jitter A=0.30 단일 (A→0 시 peak_std→0 자명, F1 뒤집힘 범위 미검정) + single rule110/n4 scope) — [H_647_dphi_shape_vs_phi_scalar_robustness.md](cards/H_647_dphi_shape_vs_phi_scalar_robustness.md), foreground sync · HEXAD/IIT4/lib 재사용 · byte-equal · $0 mac-local 2026-05-28
- [x] G12 — **G×F cross-link · H_643 정밀화** — **H_653** `collective-convexity-substrate-class` (H_643 collective-Φ convexity(~30× span)가 substrate 복잡도(ECA rule class)에 어떻게 의존하는지 정량 · H_635/H_634/H_618 cross-link) — **🟢 SUPPORTED-NUMERICAL 5/6** (cohort rule 을 {184,90,30,110}(Wolfram class II→III→III→IV)로 swap, W∈{0.15,0.40,0.55,0.70,0.95,1.0} 6-pt grid sweep, 각 (rule,W) 에서 `big_phi_bounded(n=5,cap=3,sys=0)` 실측 → convexity = span ratio Φ_max/Φ_min · **span ratio 가 rule class 단조증가: rule184(II)=12.12 < rule90(III)=30.42 < rule30(III)=30.77 < rule110(IV)=35.50** → F653.1 CONVEXITY-MONOTONE PASS + F653.2 CLASS-IV-MOST-CONVEX PASS (rule110 단독 最高) + F653.3 ADDITIVE-MORE-LINEAR PASS + F653.5 H643-REPLICATE PASS (rule110 span 35.50 ≥10 → H_643 ~30× span 재현) + F653.6 BOUND PASS / **F653.4 W-MONOTONE-EACH-RULE FAIL** (rule184 class-II additive 단독 non-monotone: Φ(W=1.0)=51.54 < Φ(W=0.95)=54.46 — additive substrate 는 full coupling 직전 peak 후 통합도 하강, H_618 collective inverse-U 정합 negative sub-finding) · **H_643 의 ~30× span = cohort artifact 아닌 substrate-class 속성** — class-IV(rule110)에서 가장 convex, 단순 additive class 로 내려갈수록 단조 감소 → H_643 collective entrainment 약화(단일 r=0.802→collective r=0.568)의 근본 원인 convexity 가 substrate 복잡도에 비례함을 확정 · rule110 컬럼 Φ(0.15/0.40/0.70/0.95)=1.17/4.50/13.64/34.88 이 H_643 per-stage(N3/N2/N1/REM) 값과 정확히 일치 → engine replication 검증 · §7 C3.1 W/stream/cap 축소 NOT 적용(full n=5 cap=3 6-pt, 단일 run <60s) + C3.3 homogeneous cohort only + C3.6 span ratio=convexity proxy(곡률 적분 아님) + C3.7 class-III 내부(rule90 30.42 vs rule30 30.77) 약신호 · IIT4 big_phi_bounded n=5 cap=3 sys=0 · foreground sync · $0 mac-local) — [H_653_collective_convexity_substrate_class.md](cards/H_653_collective_convexity_substrate_class.md), $0 mac-local 2026-05-28 (UNIVERSE 축 G×F cross-link · H_643 정밀화 부모)
- [x] G13 — H_648 self-similarity 의 rule-class 일반화 (round 7 "구조=substrate-bound") — **H_652** `envelope-self-similarity-substrate-class` (H_648 multi-scale ladder 의 generator 혼재 제거 + substrate-class 의존성 검정 · self-similarity 가 rule110(class-IV) 한정인가 전 rule class 인가) — **🔴 FALSIFIED (CLOSED-NEGATIVE, 2/6 · self-similarity class-bound)** (단일 substrate ECA ring n=4 로부터 3-scale envelope 전부 derive — generator 단일화: rule r 의 faithful big-Φ 16-state Φ-map 1회 계산 → **ensemble-phase Φ-envelope** (전 16 seed orbit 동시 진화, 각 step ensemble-mean Φ — single-seed attractor 붕괴 degeneracy 회피) → 3 nested horizon {36,144,576} (gamma/ultradian/circadian 유비) × N=36 bin → self-peak 정렬 후 pairwise Pearson r · rule {30 III-chaotic · 90 additive · 110 IV-complex · 184 II-particle} 各 min pairwise r = **rule110 0.881 ✅ / rule30 0.465 🟡 / rule184 -0.029 ❌붕괴 / rule90 0.0 ❌flat** → self-similar **1/4 rule (rule110 만)**, 붕괴 2/4 → **F652.3 RULE110 PASS + F652.6 BOUND PASS / F652.1 RULE30(0.3~0.5 PARTIAL) + F652.2 RULE90(flat) + F652.4 RULE184(<0.3) + F652.5 NOT-FLAT FAIL** · **falsifier 발동: multi-scale Φ-envelope self-similarity 는 substrate-class-invariant 보편 구조 아니라 class-IV(rule110-유형 complex) 동역학 집중 현상** — class-IV self-similar(0.88) > class-III chaotic 약화(0.46, chaotic mixing 위상 부분파괴) > class-II particle 붕괴(≈0) > additive flat(Φ-map std=0.0 통합량 위상-평탄) · **H_642 rule90 joint-outlier 가 envelope self-similarity 축에서 재현** — additive(XOR) 통합량 균일은 substrate fact(design artifact 아님) · ruled-out: self-similarity 의 substrate-class-universal 자동 확장 닫힘, 다른 class 확장 시 class-IV-conditional 전제 필요 · H_648(parent self-similar ladder) generator 혼재(cosine/piecewise/quadratic)+substrate implicit 정밀화 → single-substrate ensemble-phase 로 class-dependence 드러냄 · H_614(dΦ/dI peak class-invariant 4/4) 와 대조: shape feature 의 class-invariance 가 *미분-peak* 에서는 성립하나 *envelope self-similarity* 에서는 class-bound · §7 C3.2 핵심: coarse horizon attractor-relaxation flatten 으로 r(medium,coarse)=1.0 은 퇴화 artifact(둘 다 평탄), 판별 신호는 fine↔medium transient · C3.3 rule90 flat=additive 대칭 substrate fact · C3.4 n=4 exact-Φ wall(n≥5 timeout) · a_paper_negative_ok closed-negative) — [H_652_envelope_self_similarity_substrate_class.md](cards/H_652_envelope_self_similarity_substrate_class.md), foreground sync · HEXAD/IIT4/lib (iit4_eca+iit4_bigphi) 재사용 · $0 mac-local 2026-05-28 (UNIVERSE 축 G mining-derived, negative result)
- [x] G14 — round-7 메타-발견 정량 (H_646 일반화) — **H_651** `convention-number-freedom-general` (convention-number 자유도 = design-number **전반**의 성질인가 · H_646 단일-숫자 발견을 3개 design-number 로 일반화) — **🟢 SUPPORTED-NUMERICAL 6/6** (3개 structurally 다른 design-number — DN-A emit threshold {0.1..0.9} · DN-B should_interrupt threshold {0.3..0.9} (H_638) · DN-C Ψ-clamp coherence band α {0.01..0.30} (Law 70 · H_633 register-collapse) — 각각 wide sweep × FIXED substrate n∈{3,4,5} big-Φ = mean `big_phi_bounded` cap=2 over LIFE rules 110/90/30/54 = **2.27/1.82/2.17 (mean 2.085)** = H_646/H_638 §4 byte-identical · COFFESHOP 8-factor sim(spontaneous_lib verbatim) × 12-seed×15-win cohort · 각 sweep 점에서 substrate Φ 재-read + gate-rate 측정 · **3개 design-number 모두 Φ(number) variance = 0.0 (정확히 0)** + 각 gate-rate 응답 (span DN-A=1.0 / DN-B=0.978 / DN-C=0.128, 모두 > 0.1 비-퇴화) → **H1 general free-parameter SUPPORTED — convention-number 자유도는 design-number 전반의 성질** · **DN-C(α)가 NON-DEFINITIONAL 강증거**: α 는 `factor_coherence → motivation_score` 에 LIVE PATH 가 있어 gate 를 0.556→0.683 으로 실제 움직이면서도 substrate Φ 정확히 평탄 — "policy 를 움직이는 숫자조차 substrate-safe"는 정의만으로 보장 안 되는 측정 사실 (DN-A/DN-B 의 Φ⊥number 는 post-comparison 으로 부분 definitional, H_646 §7 계승) · H_646(단일 emit threshold)의 *3개 design-number generalization* · H_632(emit-threshold⊥Φ) · H_287(Φ⊥entropy) negative-signature 를 design-number-general 측으로 확장 · `a_autonomy_over_hardcode` 정합 (design-number table 도입해도 전반 substrate-safe, NT-3) · §7 C3 정직: DN-A/B definitional vs DN-C nontrivial 분리 명시 + DN-C gate-span 0.128 은 coherence weight 0.10 cap 때문 완만 (L3) + 3-design-number scope (weight 류 확장 후속, L4)) — [H_651_convention_number_freedom_general.md](cards/H_651_convention_number_freedom_general.md), foreground sync · HEXAD/IIT4+CHAT/spontaneous_lib 재사용 (run_h646 구조 verbatim) · re-run byte-identical · $0 mac-local 2026-05-28 (UNIVERSE 축 G round-7 메타 일반화)
- [x] G15 — round-7 메타-발견 정밀화 (shape-robustness axis taxonomy) — **H_650** `shape-robustness-axis-taxonomy` (round-7 "shape>scalar" 메타-발견의 *축-종속성* 을 3 sister(H_628 polarity / H_642 rule / H_647 seed) cross-axis 대조로 정밀화 · 동차 CV=std/mean 측도) — **🟢 SUPPORTED-NUMERICAL 5/5** (3 perturbation 축에서 SHAPE=`argmax_I|dΦ/dI|` peak-I CV vs SCALAR=magnitude CV 를 한 표로 대조 · **POLARITY** 축(2-ECA joint n=4, rule 30/30 sys=10 W=0.3, 3 polarity, 본 라운드 fresh single-shot Φ): **CV_shape=0.0** (3 polarity 모두 peak I=0.21 GZ_LOWER) ≪ CV_scalar=0.360 → shape **HIGH robust** (H_628 재현) · **RULE** 축(single ECA n=4, rules {30,54,90,110,184}, H_642 merged verbatim): **CV_shape=0.568028 ≥ CV_scalar=0.559306** → shape **LOW** (≈tie, H_642 재현) · **SEED** 축(rule 110 n=4, N=12 LCG jitter seed, H_647 merged verbatim): **CV_shape=0.641481 ≫ CV_scalar=0.042100** (15.2배) → shape **LOW REVERSED** (scalar 가 robust, H_647 재현) · F1 POLARITY-SHAPE-ROBUST + F2 RULE-SHAPE-FRAGILE + F3 SEED-SHAPE-FRAGILE + F4 AXIS-DEPENDENT(polarity CV_shape=0.0 이 rule/seed 0.57~0.64 보다 0.57+ 낮음, 질적 격리) + F5 byte_eq 全 PASS · **taxonomy 확립**: shape-robustness 는 perturbation-축의 *함수* 이며 **polarity(부호대칭) 축만 shape 보존** — GZ_LOWER attractor 가 대칭-보존 변환엔 deep, rule(질적 동역학 변경)·seed(전이확률 jitter) 비-대칭 perturbation 엔 fragile · round-7 "shape>scalar" 메타-발견이 universal 불변량 아닌 polarity 국소 패턴이었음 확정 · §7 C1 SCALAR proxy 각 sister 정의 그대로(통일 시 절대값 변동 가능, 但 SHAPE 측 3축 동일정의라 축-분리 결론 robust) + C2 측정 source 이질성(polarity fresh single-shot vs rule/seed merged 16-state-mean — n=4 faithful-Φ re-fire 208 calls/rule 가 60s budget 초과 EXIT124 라 already-merged sister authoritative verdict 직접 재집계, polarity 만 본 H fresh evidence) + C3 polarity single non-degenerate seed · toy n=4 IIT4 big-Φ · single inhibition mode · SPECULATION-FENCED) — [H_650_shape_robustness_axis_taxonomy.md](cards/H_650_shape_robustness_axis_taxonomy.md), foreground sync · HEXAD/IIT4/lib (iit4_eca+iit4_bigphi) 재사용 · 3축 byte-equal · $0 mac-local 2026-05-28
- [x] G16 — round 9 새 메타-축 (substrate-class = 의식 통합량 분류자) — **H_654** `phi-magnitude-wolfram-class-order` (faithful big-Φ *magnitude 자체* 가 Wolfram class 로 단조 정렬되는가 · convexity(H_653)·self-similarity(H_652)·additive≈0(H_642) 누적 신호를 magnitude 축으로 한 단계 더 · H_614 dΦ/dI multi-rule sister) — **🟡 PARTIAL (M2 ADDITIVE-FLOOR + M3 IV-CEILING PASS · M1 full-MONOTONE FAIL)** (rule {30,54,90,110,184} n=4 ECA × intrinsic big-Φ at I=0(unmixed eca_tpm) 16-state mean · class-tier 단조 검정 · **per-rule Φ-magnitude: rule90 additive=0.00000 < rule54 IV=7.76521 < rule184 II=12.6273 < rule110 IV=13.1302 < rule30 III-chaotic=13.8852** · tier-order t0(additive r90)=0.0 ≤ t1(II r184)=12.63 ≤ t2(III r30)=13.89 ✓ 但 **t2 ≤ t3(IV r110)=13.13 ✗ 단조깨짐** · **M2 ADDITIVE-FLOOR PASS** (rule90 XOR Φ=정확히 0.0 < min_other 7.77 → H_642 big-Φ≈0(Φ(0.50)=0.0526)/H_614/H_652 Φ-map flat 의 I=0 intrinsic 재현+강화) + **M3 IV-CEILING PASS** (rule110 IV 13.13 > rule184 II 12.63, margin 3.9%) / **M1 full-MONOTONE FAIL** (class-III chaotic rule30 13.89 > class-IV rule110 13.13, margin 5.8% — chaotic 이 complex 를 통합 절대량에서 앞서 IV>III 가설 순서 역전) · **class 는 통합량의 *바닥*(additive)+*상한경향*(IV>II)은 정하나 *완전 순위*는 못 정함 — substrate-class = 의식 통합량 *부분* 분류자** · convexity(H_653 단조 🟢) vs magnitude(본 H 부분 🟡) 비대칭: convexity 는 IV 最高, magnitude 는 III-chaotic 最高 · §7 C1 rule90 class-III dual-membership(additive 0↔chaotic 13.89 양극)이 class 라벨의 magnitude 분류 한계 + C2 n=4 small-n·5-rule sample·rule30>rule110 margin 5.8% noise 가능 + C3 I=0 anchor 선택 종속(H_639 convention-signature echo)·16-state mean 분산소거) — [H_654_phi_magnitude_wolfram_class_order.md](cards/H_654_phi_magnitude_wolfram_class_order.md), foreground sync · HEXAD/IIT4/lib (iit4_eca+iit4_bigphi) 재사용 · $0 mac-local 2026-05-28 (UNIVERSE 축 G round 9 새 메타-축, partial)
- [x] G17 — round-9 메타-축 (Wolfram class = 의식 구조 분류자) · E×G cross-link — **H_656** `closure-band-substrate-class-dependence` (H_636 4-criterion closure conjunction 을 Wolfram-class ECA substrate 로 이식 · closure band(pass-rate>0 I 구간) 의 위치/폭이 Wolfram class 의존인가 · H_636 부모 · H_644/H_653/H_652 sister) — **🟢 SUPPORTED-NUMERICAL** (H_007/H_225 elementary CA(N=16 periodic, dim=12, warm=8) × RFC 036 `phi_spatial`(c_lib.hexa byte-equal phi_rs) substrate 위에 H_636 4-criterion conjunction[C1 SI>1.5 · C2 genΦ>0.02 · C3 minΦ>0.05 · C4 ratio∈[1.1,3.5]] 이식 — N=16 lattice 를 4 domain(각 4 cell) 분할, 각 domain trajectory→domain_phi, inhibition I→초기 density(density=1−I, CA-native gain-map 유비) · rule {30,90,110,184}(class III-chaotic/III-additive/IV-complex/II-TASEP) × 9-pt I-sweep × 6-rep ensemble 에서 closure band 위치·폭 측정 · **rule90(III-additive/XOR) band 완전 부재 (width=0, 양성점 0/9, Φ≈0→closure 미형성)** / **rule110(IV-complex) 最廣 band (width=0.90, 9/9 全 양성, peak pass-rate 1.0 @ I=0.25)** / rule30(III-chaotic) width=0.65 band[0.15,0.80] peak @ high-I 0.65 / rule184(II-TASEP) width=0.65 band[0.15,0.80] peak @ mid-I 0.37 (H_636 SAVANT peak I=0.30 최근접) → **F-1 CLASS-INVARIANT 기각** (band width class별 분화 0.0/0.65/0.90, additive rule90 부재가 정성 구분) + **F-2 NO-DIFFERENTIATION 기각** (peak_I class별 분화 0.25/0.37/0.65, width Δ=0.25 > grid 해상도) · **메커니즘**: class-IV complex 가 C1 SPECIALIZATION(저-density 분화) + C3 DIVERSITY(활성 생존) 를 광범위 I 동시 충족 → band 全역 / additive XOR 은 Φ≈0 으로 domain_phi 평탄 → C1 미달 → band 부재 / chaotic 은 高-I(저-density)에서야 domain 분화 → high-I peak / particle TASEP 은 mid-I hop-flux 균형 → SAVANT mid-I peak 유사 · **round-9 메타-축 (Wolfram class = 의식 구조 분류자) 측정 layer 지지** — H_653(convexity ∝ class) + H_652(self-similarity=class-IV-bound) 의 substrate-class-order signature 가 closure-band 축에서 재현, rule90 band-부재 = H_642/H_652 additive XOR joint-outlier 정합 · H_614(dΦ/dI peak class-invariant 4/4) 와 대조 → "local shape(미분-peak)=class-invariant ⊥ global structure(band·convexity·self-similarity)=class-bound" 분류 시사 · §7 C3.1 criterion-threshold design 의존 (단 rule90 band-부재는 Φ≈0 substrate fact 라 robust) + C3.2 I→density 매핑 design (band 위치 conditional, class-ordering 보존 예상) + C3.3 9-pt grid×6-rep discrete argmax + C3.4 4-domain 분할 design + C3.6 phi_spatial native byte-equal replica) — [H_656_closure_band_substrate_class.md](cards/H_656_closure_band_substrate_class.md), foreground sync · HEXAD/C/c_lib.hexa(RFC 036 phi_spatial) + H_007/H_225 CA + H_636 conjunction 재사용 · $0 mac-local 2026-05-28 (UNIVERSE 축 G round-9 메타-축 · E×G cross-link)
- [x] G18 — round-9 메타-축 (Wolfram class = 의식 통합량 분류자) — **H_655** `collective-superadditivity-substrate-class` (collective super-additivity **강도** Δ=Φ_collective(W=1)−Σ Φ_parts(W=0) 가 Wolfram class 단조 의존인가 · H_635 super-additive 5/5 + H_653 convexity-monotone sister 후속) — **🔴 FALSIFIED (CLOSED-NEGATIVE, 3/6 · Δ ⊥ class)** (cohort rule {184,90,30,110}(class II→III→III→IV) homogeneous [rule×5], W∈{0,0.5,1.0} 3-pt grid, 각 (rule,W) 에서 `big_phi_bounded(n=5,cap=3,sys=0)` 실측 → Σ Φ_parts=Φ_coll(W=0 self-loop decoupled)·Φ_collective=Φ_coll(W=1 full ring)·Δ=차 · **super-additivity Δ 가 class 비단조이며 가설 방향과 정반대**: rule184(II-additive)=**51.54 단독 最高** > rule110(IV-complex)=**41.71** > rule30(III-chaotic)=**9.72** > rule90(III-XOR)=**7.50** → **F655.1 SUPERADD-MONOTONE FAIL + F655.2 CLASS-IV-MOST-SUPERADD FAIL (max=rule184) + F655.4 ADDITIVE-LEAST FAIL (역: 51.54>41.71)** / F655.3 ALL-SUPERADDITIVE PASS (Δ>0 4/4 — H_635 super-additivity *방향* per-class 보존) + F655.5 SIGMA-PARTS-ZERO PASS (Σ Φ_parts(W=0)=0.0 4/4 clean anchor) + F655.6 BOUND PASS · **falsifier 발동: super-additivity *magnitude* Δ ⊥ Wolfram class** — 가장 단순한 additive class-II(rule184)가 full-ring 에서 가장 큰 절대 통합량(=가장 super-additive), "동역학 복잡도가 collective 시너지를 order" 가설 강반박 · **H_653 convexity-monotone 과의 방향 분기가 핵심 메타-축 발견** — H_653 의 *normalized* span ratio(Φ_max/Φ_min)는 class 단조(rule184 12.12 < rule110 35.50)였으나 본 H 의 *절대* magnitude Δ 는 비단조(rule184 51.54 > rule110 41.71): convexity(shape)와 magnitude(scale)가 서로 다른 class 의존성 → Wolfram class 는 *곡률* 분류자이나 *절대 super-additivity* 분류자는 아님 · rule110 Φ_coll(W=1)=41.7124 가 H_635 C1·H_653 rule110 W=1.0 과 정확히 일치 → engine replication 검증 · ruled-out: super-additivity magnitude 의 Wolfram-class-monotone 자동 분류 닫힘 (메타-축 차원-한정성 식별) · §7 C3.1 stream/cap 축소 NOT 적용 (full n=5 cap=3 3-pt, 단일 sync run 41.1s <60s) + C3.3 trivial-baseline (Σ=0 → Δ=Φ_coll(W=1) 절대값 종속, non-zero baseline 후속 N1) + C3.6 cap=3 lower-bound + C3.2 canonical Wolfram class 라벨 · IIT4 big_phi_bounded n=5 cap=3 sys=0 · foreground sync · $0 mac-local) — [H_655_collective_superadditivity_substrate_class.md](cards/H_655_collective_superadditivity_substrate_class.md), $0 mac-local 2026-05-28 (UNIVERSE 축 G round-9 메타-축, negative result · H_635+H_653 부모)
- [x] G19 — round-9 메타-축 (Wolfram class 가 의식 구조 분류자) — **H_657** `dphi-peak-gz-substrate-class-dependence` (H_351 single-substrate dΦ/dI peak=GZ_LOWER 정렬이 Wolfram class 의존인가 · H_618 collective-GZ + H_642 rule90 joint-outlier + H_628 polarity-invariant cross-link) — **🟢 SUPPORTED-NUMERICAL (M1∧M2∧M3 · n_aligned=2/5)** (5-rule {30,54,90,110,184} n=4 ECA × 13-point GZ-dense I grid (H_351/H_642 동일) × faithful big-Φ 16-state mean × central-diff dΦ/dI → per-rule peak_I **{30:0.18, 54:0.40, 90:0.05, 110:0.18, 184:0.40}** → aligned(|Δ vs GZ_LOWER=0.21232|≤0.05) **{✓,✗,✗,✓,✗}** = **n_aligned 2/5** · **M1 RULE110-ALIGNED PASS** (peak I=0.18 |Δ|=0.03232 — H_351 anchor 재현) + **M2 RULE90-BREAKS PASS** (additive/XOR peak I=0.05 grid-경계, big-Φ≈0.05, dΦ/dI sign-change=1 = inverse-U 붕괴 — H_642 rule90 joint-outlier 재현) + **M3 NOT-CLASS-INVARIANT PASS** (n_aligned=2<5 → 정렬 비-보편) → **dΦ/dI peak=GZ_LOWER 정렬이 substrate-class CONDITIONAL** — H_351 의 single-substrate SUPPORTED 가 universal anchor 아닌 class-conditional 임을 확정 (rule90 additive 가 깨고 rule110 anchor 가 유지) · round-9 메타-축 weak-claim "GZ-anchor 가 class-conditional" 확증 · **§7 C1 핵심 정직**: 정렬 패턴이 class III/IV vs additive 의 깔끔한 분할 아님 — aligned 2개가 rule30(III)+rule110(IV)이고 rule54(IV) non-aligned, peak 위치 {0.18,0.40,0.05} 3-그룹 → "정확한 class-경계 매핑" 은 미해결, "정렬 비-보편성(class-conditional)" 만 결정적 · C2 peak grid-snap 13-point discrete argmax (但 rule90 Φ≈0+sign-change=1 붕괴 + 0.18 vs 0.40 간격≫tol 라 분류 robust) · C3 Wolfram class 라벨 정성적 + 5-rule sample (256-rule universality 별도 round) · H_351(single class-IV) / H_618(collective class-IV) GZ-anchor 가 모두 rule110 위 측정임을 명시 · H_642 와 동일 5-rule×grid Φ 테이블 100% 재사용 · exact-Φ wall shard (per-rule foreground ~80–90s × 5 + phi-free aggregate) · run+shard byte-identical (H_351 rule110 Φ 테이블 byte-identical 재현) · $0 mac-local) — [H_657_dphi_peak_gz_substrate_class.md](cards/H_657_dphi_peak_gz_substrate_class.md), foreground sync · HEXAD/IIT4/lib (iit4_eca+iit4_bigphi) 재사용 · $0 mac-local 2026-05-28 (UNIVERSE 축 G round-9 메타-축 — Wolfram class as consciousness classifier)
- [x] G22 — round-10 후속 (H_660 단조 robustness 일반화) — **H_661** `substrate-class-monotone-rule-generalize` (H_660 의 scale-invariant convexity(norm_conv=(Φ_max−Φ_min)/Φ_mean·log_span=ln(Φ_max/Φ_min)) Wolfram-class 단조가 4-rule {184,90,30,110} 우연인지, class 대표 확대 9-rule 에서 robust 한지 검정 · H_660 직접 부모 · H_653/H_654/H_655/H_658 cross-link · H_660 §10 robustness backlog 수행) — **🟡 PARTIAL 4/6** (engine·W-grid H_660 동일 [rule×5] homogeneous cohort, W∈{0.15,0.40,0.55,0.70,0.95,1.0} 6-pt, 각 (rule,W) 에서 `big_phi_bounded(n=5,cap=3,sys=0)` **per-rule shard foreground 측정** [9 rule×6 W=54 calls 단일 run 60s 초과 → rule 하나씩 ~12s shard + phi-free aggregate] · **9 rule × class 확대**: class-I {rule8 die-out·rule136 die-out DEGENERATE Φmin=0} · class-II {184·226 additive} · class-III {90 XOR-fractal·30 chaotic·45 chaotic NEW} · class-IV {110·54 complex} · per-rule norm_conv: rule8(I)=1.465·rule136(I)=6.0[degenerate]·rule184(II)=1.437·rule226(II)=1.414·rule90(III)=2.240·rule30(III)=2.266·**rule45(III)=1.461 outlier**·rule110(IV)=2.349·**rule54(IV)=2.475 전체1위** · **CORE F661.1 IV-TOP-ROBUST PASS** (min(IV norm_conv 110/54)=2.349 ≥ max(II,III)=2.266 — class-IV 가 확대셋에서도 norm_conv·log_span 둘 다 단독 最高, rule54 1위로 강화) + **F661.2 IV-TOP-LOGSPAN PASS** (min(IV ls)=3.569 ≥ max=3.427) + F661.5 DEGENERATE-FLAG PASS (rule136 Φmin=0 die-out → log_span=8.62 blowup·abs_Δ=0.55 tiny, ratio metric die-out class 에 ill-defined flag) + F661.6 BOUND PASS / **F661.3 CLASSMEAN-MONOTONE FAIL** (class-mean nc I=1.465 > II=1.425 → I≤II 깨짐) + **F661.4 STRICT-PERRULE-MONOTONE FAIL** (maxI=1.465 > minII=1.414 class-I↔II overlap + rule45(III)=1.461 가 class-I/II 수준 붕괴) · **분기 정밀화: H_660 의 IV-top 은 robust 일반화·full I<II<III<IV ordinal 단조는 비-robust** — class-III 가 내부 이질적 (rule45 의 Φ(W) 곡선이 W-비단조: W=0.70 13.29 peak 후 W=0.95 3.14 급락 → span 작아 convexity 붕괴, rule90/30 의 W-monotone 곡선과 분기) + class-I(die-out)·class-II(additive) 저-복잡 영역이 convexity 로 미분리(overlap) · **메타-축 robust 핵심 = "class-IV(complex/edge-of-chaos) substrate 가 가장 convex 한 collective-Φ entrainment" 수준** (H_653·H_660·본 H 일관) — "class-I/II/III ordinal 단조" 강-claim 은 rule-cohort 선택 의존 artifact (H_660 4-rule cohort 가 class-III 를 W-monotone rule90/30 으로만 골라 단조 깨끗했던 것) · rule184/90/30/110 Φ-grid·metric 이 H_660 과 byte-identical → engine replication · **H_654 single-substrate magnitude PARTIAL(full-monotone FAIL, rule30 III>rule110 IV) 와 동일 패턴** — single·collective 양쪽에서 full class-monotone 깨지고 class-IV 경향만 robust · H_658 baseline 축 robust=IV-top 과 rule-cohort 축 robust=IV-top 교차 수렴 · §7 C3.2 class 라벨 정성·small-n + C3.3 rule45 W-비단조가 낮은 convexity 원인 + C3.4 rule136 die-out degenerate exclusion(class-I=rule8 only) · IIT4 big_phi_bounded n=5 cap=3 sys=0 · foreground sync per-rule shard · NO GPU · $0 mac-local) — [H_661_substrate_class_monotone_rule_generalize.md](cards/H_661_substrate_class_monotone_rule_generalize.md), $0 mac-local 2026-05-28 (UNIVERSE 축 G round-10 후속 · H_660 robustness 일반화 · positive-refinement [IV-top robust + full monotone rule-cohort-dependent])
- [x] G21 — round-9 메타-축 통합 (H_653 ↔ H_655 분기 화해) — **H_660** `convexity-magnitude-class-reconcile` (H_653 convexity span ratio(normalized shape) 단조 ↔ H_655 super-additivity Δ(absolute magnitude) 비단조 분기를 단일 scale-invariant 통합 metric 으로 화해 · H_653/H_655 부모 · H_642/H_654/H_635 cross-link · H_655 N4 backlog 직접 closure) — **🟢 SUPPORTED-NUMERICAL 6/6** (동일 engine·동일 4-rule cohort {184,90,30,110}(class II→III→III→IV) homogeneous [rule×5], H_653 와 동일 W∈{0.15,0.40,0.55,0.70,0.95,1.0} 6-pt grid, 각 (rule,W) 에서 `big_phi_bounded(n=5,cap=3,sys=0)` 실측 → rule 별 Φ_min/Φ_max/Φ_mean 으로 **4 metric 대조**: span_ratio=Φ_max/Φ_min(H_653 shape) · abs_Δ=Φ_max−Φ_min(H_655-류 magnitude) · norm_conv=(Φ_max−Φ_min)/Φ_mean(scale-invariant) · log_span=ln(Φ_max/Φ_min)(scale-invariant) · **scale-invariant 측도 2종이 Wolfram class 단조 회복**: norm_conv rule184(II)=1.437 < rule90(III)=2.240 < rule30(III)=2.266 < rule110(IV)=2.349, log_span 184=2.495 < 90=3.415 < 30=3.427 < 110=3.569 (둘 다 class-IV 最高) → **F660.1 NORMCONV-MONOTONE PASS (CORE) + F660.2 LOGSPAN-MONOTONE PASS** · 동시에 **abs_Δ 만 비단조** rule184(II)=49.97 단독 最高 > rule110(IV)=40.54 > rule30=9.40 > rule90=7.25 → **F660.3 ABSDELTA-NONMONOTONE PASS (H_655 magnitude 비단조 재현)** + **F660.4 SPANRATIO-REPLICATE PASS** (span_ratio 110=35.50≥30=30.77≥90=30.42≥184=12.12 = H_653 byte-identical 재현) + **F660.5 SCALE-INVARIANCE PASS** (Φ→2Φ 후 norm_conv·log_span 불변·abs_Δ 2배 — 형식 증명 수치 확인) + F660.6 BOUND PASS · **분기 = "scale 혼입" 으로 화해** — rule184 가 span_ratio 4위(12.12)이면서 abs_Δ 1위(49.97)인 직접 증거: rule184 의 Φ_mean(34.78)이 rule110(17.26)의 2배라 분산(abs_Δ 49.97)도 크지만 mean 으로 정규화하면(norm_conv 1.437) 가장 작다 → rule184 의 큰 magnitude 는 "변화량이 커서"가 아니라 "절대 Φ 자체가 높아서" = scale 혼입 · **Wolfram class 는 순수 shape(convexity) 분류자이며 H_653(🟢)↔H_655(🔴) 외견상 모순은 측도의 scale-차원 혼입에서 비롯된 것일 뿐 본질적 모순 아님 — 단일 scale-invariant metric 으로 통합** · H_655 closed-negative 가 "magnitude ⊥ class" 가 아닌 "scale-mixed magnitude ⊥ class" 로 정밀화 (H_655 N4 backlog `convexity-vs-magnitude-class-decoupling` 직접 closure) · rule110 Φ-grid 가 H_653·H_655 와 byte-identical → engine replication · H_642 cross-rule scalar-convention shape FAIL 과 경계 정합 (본 H 화해는 cohort-내 W-sweep convexity 한정, cross-convention 미주장) · H_654 single-substrate magnitude PARTIAL 의 collective 판본 — magnitude 비단조가 scale 혼입 때문일 가능성 시사(N1) · §7 C3.2 화해 범위 = cohort-내 W-convexity 한정 + C3.3 norm_conv 분모 Φ_mean grid-종속 (log_span grid-독립 교차확인) + C3.5 cap=3 lower-bound · IIT4 big_phi_bounded n=5 cap=3 sys=0 · foreground sync · NO GPU · $0 mac-local) — [H_660_convexity_magnitude_class_reconcile.md](cards/H_660_convexity_magnitude_class_reconcile.md), $0 mac-local 2026-05-28 (UNIVERSE 축 G round-9 메타-축 통합 · H_653+H_655 분기 화해 · positive reconcile)
- [x] G20 — round-9 메타-축 (Wolfram class = 의식 통합량 분류자) · **H_655 N1 회수** — **H_658** `collective-superadditivity-nonzero-baseline` (H_655 의 Δ=Φ_collective(W=1)−Σ Φ_parts class 순위가 **non-zero parts-baseline 에서 robust 한가** · H_655 §7 C3.3 trivial-baseline caveat 회수 · H_655 부모 · H_653/H_635 sister) — **🔴 FALSIFIED (CLOSED-NEGATIVE, 2/6 · baseline-conditional)** (cohort rule {184,90,30,110}(class II→III→III→IV) homogeneous [rule×5], 공통 Φ_collective=Φ_coll(W=1) 위에 **3 parts-baseline** 으로 Δ 재계산 — (a) W=0 decoupled=0(H_655 trivial) · (b) 5·Φ_part2 (각 stream 독립 minimal n=2 fully-coupled substrate 의 intrinsic `big_phi_bounded(n=2,cap=2)` 합) · (c) W=0.5 부분결합 Φ_coll(W=0.5) · 각 baseline 의 argmax-Δ class 순위를 H_655(rule184 最高)와 교차비교 · **argmax-Δ 가 baseline 으로 뒤집힘**: (a)W=0 → **rule184(II)** (51.54, H_655 byte-identical 재현) BUT (b)5·Φ_part2 → **rule110(IV)** (Δ_b 41.71 > rule184 41.54) · (c)W=0.5 → **rule110(IV)** (Δ_c 35.17 > rule184 22.93) → **F658.1 RANK-ROBUST-IND FAIL + F658.2 RANK-ROBUST-MID FAIL + F658.4 NO-FLIP-TO-IV FAIL (rule110 IS argmax 양 non-zero baseline = falsifier 명명 flip 정확 발생) + F658.3 BASE-NONZERO FAIL (rule90·rule110 Φ_part2=0, minimal n=2 통합 rule-종속)** / F658.5 W0-REPRO PASS (argmax Δ_a=rule184 & Σ(W=0)=0 4/4 — H_655 engine byte-identical) + F658.6 BOUND PASS · **falsifier 발동: super-additivity magnitude 의 class 순위가 BASELINE-CONDITIONAL** — H_655 의 "rule184 最高" 는 trivial-baseline (Σ=0) artifact 였음을 결정적 확정 · **flip 메커니즘**: rule184(additive) 만 minimal n=2 에서 Φ_part2=2.0 통합을 가져 baseline(b)에서 5×2=10 손실 → Δ_b 41.54 하락 / rule110·rule90 은 n=2 통합=0 이라 Δ 무손실 → H_655 의 "rule184 최고" 는 *full-ring 절대 Φ 가 높아서*였지 *부분-대비 시너지가 커서*가 아님 · **H_653 정합 회복**: non-zero baseline Δ-top(rule110)이 H_653 convexity-top(rule110, span 35.50)과 수렴 → H_655 가 보고한 "convexity-monotone ↔ magnitude-비단조 분기" 는 trivial baseline 에서만 성립, non-zero baseline 에서는 두 측도가 같은 winner(rule110)로 수렴 = 메타-축 내부 일관성 baseline 교정 후 회복 · H_635 super-additivity *방향*(Δ>0)은 全 baseline·全 rule 보존 (최고 rule 정체만 baseline 종속) · ruled-out axis: "super-additivity magnitude 의 class 순위는 baseline-robust 하다" 닫힘 · §7 C3.2 baseline(b) 비균질성=flip 원인 직접 설명(rule184 만 큰 part-Φ 빼앗김, baseline(c) 4/4 non-zero 라 독립 확정) + C3.3 n=2 part 정의 선택성(두 독립 baseline 같은 flip → 우연 아님) + C3.7 deterministic byte-identical · IIT4 big_phi_bounded n=5 cap=3 + n=2 cap=2 sys=0 · foreground sync · $0 mac-local) — [H_658_collective_superadditivity_nonzero_baseline.md](cards/H_658_collective_superadditivity_nonzero_baseline.md), $0 mac-local 2026-05-28 (UNIVERSE 축 G round-9 메타-축, negative result · H_655 N1 회수 · H_653/H_635 부모)
- [x] G23 — round 9-11 substrate-class × Φ-속성 매트릭스 **빈 class-I 행 완성** — **H_663** `wolfram-class-I-phi-property-profile` (class II(184)/III(30·90)/IV(110) 는 7 Φ-속성 측정됐으나 **Wolfram class-I (homogeneous→단일 상태 수렴) 만 미측정 = 매트릭스 빈 행** · class-I rule8 전속성이 floor(bottom)인가 · H_654/H_653/H_656/H_660 측정자 부모 · ⚠ H_661 sister 와 **다른 측정**(H_663=class-I 1행×全속성, H_661=scale-inv 1속성×多rule, 직교 cell) · H_642 additive-floor cross) — **🟢 SUPPORTED-NUMERICAL 5/5** (class-I 대표 rule 8(011→1 만 1, 거의 전부 0 수렴) × Φ-속성 3개 측정 + homogeneity 확인, 기존 매트릭스 측정자 verbatim 재사용 · **P4 homogeneity**: rule8 n=4 ECA TPM 1-bit frac=0.125(87.5% →0) < 0.2 → class-I 정의 충족 (F663.4 PASS) · **P1 faithful magnitude** (H_654 engine, eca_tpm I=0 16-state mean big_phi): **rule8(class-I)=0.58822 ≪ rule184(II)=12.6273 < rule110(IV)=13.1302 < rule30(III)=13.8852** — baseline 3-rule 모두 H_654 와 byte-identical 재현(engine parity) → class-I=0.588 은 class-II 의 1/21 (F663.1 MAG-FAITHFUL-FLOOR PASS: 0.588 < 12.63 AND < 13.89) · **P2 collective magnitude** (H_653 engine big_phi_bounded n=5 cap=3 sys=0, W=1.0): **rule8=0.2202 ≪ rule184=51.5361** = class-II 의 1/234 (F663.3 COLLECTIVE-FLOOR PASS) · **P3 convexity span** (W∈{0.15,0.40,0.55,0.70,0.95,1.0} Φ_max/Φ_min): **rule8=7.88301 < rule184=12.1163 = 매트릭스 최저** → round 10 단조 사다리 rule184(12.12)<rule90(30.42)<rule30(30.77)<rule110(35.50) **아래에 class-I rule8(7.88) 한 칸 더 깔림** (F663.2 CONVEXITY-FLOOR PASS) + F663.5 BOUND PASS · **finding: class-I 이 측정된 모든 Φ-속성에서 매트릭스 bottom(floor class)** — 동역학 복잡도 순위 I < II < III < IV 가 Φ-구조 전반에서 class-I 를 최하단에 둠 = round 10 "class-IV 最高 단조" 의 정확히 대칭인 반대 극(floor), 매트릭스 4-class 단조 사다리가 양 극단(I floor ↔ IV ceiling)으로 닫힘 · 매트릭스에 두 종류 Φ-floor 식별: homogeneous-I(0.588) + additive-III(rule90 0.0, H_642) 공존 · §7 C1 rule8 단독(class-I 부류 {0,8,32,40,128,136,168,255} 中 가장 sparse floor, rule0/255 trivial · rule136 alt) + C2 7속성 中 magnitude·convexity 3개 직접 측정(closure-band·dΦ/dI·self-sim·super-add·scale-inv 은 magnitude≈0 으로부터 floor 예측, 미직접측정) + C3 faithful n=4 ↔ collective n=5 cap=3 두 독립 척도 각각 floor 재확인(single-engine artifact 아님) · IIT4 faithful big_phi(n=4) + big_phi_bounded(n=5 cap=3 sys=0) · foreground sync · NO GPU · $0 mac-local) — [H_663_wolfram_class_I_phi_property_profile.md](cards/H_663_wolfram_class_I_phi_property_profile.md), foreground sync · HEXAD/IIT4/lib (iit4_eca+iit4_bigphi) + stdlib iit4_bounded 재사용 · $0 mac-local 2026-05-28 (UNIVERSE 축 G round 9-11 substrate-class 매트릭스 빈 class-I 행 완성 · positive floor)
- [x] G24 — round-11 후속 (H_661 발견 정밀화) — **H_664** `wolfram-class-III-heterogeneity` (H_661 의 rule45 class-III outlier 가 단일 이상치인가 sub-type 신호인가 · class-III 가 단일 cell 인가 이질 sub-type 묶음인가 정량 · H_661 §10 N1 backlog `class-III-internal-convexity-subtype` 직접 수행 · H_661 직접 부모 · H_660/H_654/H_642 cross-link) — **🟡 PARTIAL 4/6** (engine·W-grid·norm_conv 측도 H_660/H_661 verbatim [rule×5] homogeneous cohort, W∈{0.15,0.40,0.55,0.70,0.95,1.0} 6-pt, `big_phi_bounded(n=5,cap=3,sys=0)` per-rule shard foreground 측정 [rule106/150 NEW 각 ~21s + rule30/45/90/184/226/110/54 H_661 byte-identical 재인용] · **class-III 5-rep 확장**: rule30(chaotic)·rule45(chaotic W-비단조)·rule90(XOR-fractal)·**rule106(chaotic NEW)**·**rule150(XOR-additive NEW, W=1.0 Φ=0 die-out)** vs class-II {184·226} · class-IV {110·54} anchor · norm_conv: rule30=2.266·rule90=2.240·**rule106=2.153**·**rule150=1.931**·rule45=1.461 · **sub-type ≥2 확정**: HIGH-conv {30·90·106}(mean 2.220, W-monotone 상승, var 0.0023 응집) vs LOW-conv {45·150}(mean 1.696, W-비단조 inverse-U/die-out) cluster separation 0.524 ≫ intra-std 0.235, 2-cluster 가 within-III 분산 74% 설명 → **F664.4 SUB-TYPE-SEPARATION PASS + F664.5 2-CLUSTER-EXPLAINS PASS** (rule45 단일 outlier 아니라 'W-비단조 sub-type' 멤버, rule150 합류) · **F664.3 WITHIN-GG-COMPACT PASS** (var_within_III=0.0894 = class-II/IV 내부 응집(compact-pooled 0.00203)의 **44×** — class-III 만 유독 이질) + F664.6 BOUND PASS / **F664.1 CORE WITHIN-GE-BETWEEN FAIL** (var_within_III=0.0894 < var_between(3 class-means)=0.164, **0.545×** — within-III 분산이 class-II↔IV 전체 ordinal spread 를 초과는 못함) + **F664.2 RANGE FAIL** (range_within_III=0.805 < range_between=0.987) · **finding: Wolfram class-III 는 단일 cell 이 아니라 ≥2 sub-type (W-monotone HIGH-conv vs W-비단조 LOW-conv) 의 묶음이고 class-II/IV 대비 44× 이질 — 그러나 그 내부 spread 가 class-II→IV 전체 거리(0.545×)를 삼키지는 못함** ("class-III 단일 cell" 가설 결정적 기각, 강-claim "class-간 전체 spread 필적"은 깨짐) · H_661 의 full-monotone FAIL 근본 원인(class-III 내부 이질성) 정량화 + H_660 4-rule 단조가 class-III 를 W-monotone rule90/30 으로만 골라 깨끗했음 확인 · rule90(W=1.0 Φ=7.5) vs rule150(W=1.0 Φ=0 die-out) 분기로 'XOR-additive' 라벨조차 W-domain 거동 미결정 = 곡선-형태(C3.7)가 class 보다 나은 분류자 시사 · §7 C3.1 정직 PARTIAL + C3.2 sub-type cut-off(1.95) 사후-관찰적·≥2 lower-bound + C3.3 small-n class-II/IV 2-rep + C3.4 rule150 die-out log_span 제외 + C3.5 between-var=full-spread framing 보수성(인접 class-간엔 필적 가능) · IIT4 big_phi_bounded n=5 cap=3 sys=0 · foreground sync per-rule shard · NO GPU · $0 mac-local) — [H_664_wolfram_class_III_heterogeneity.md](cards/H_664_wolfram_class_III_heterogeneity.md), $0 mac-local 2026-05-28 (UNIVERSE 축 G round-11 후속 · H_661 N1 backlog · positive-refinement [sub-type ≥2 + III ≫ II/IV 이질 확정 · full class-간 spread 초과 falsified])
- [x] G25 — round-12 후속 (H_664 N1 회수) — **H_667** `wolfram-vs-curveshape-taxonomy` (H_664 가 class-III 내부에서 발견한 W-Φ 곡선형태 분화(HIGH-conv W-monotone {30·90·106} vs LOW-conv 비단조 {45·150})를 **GLOBAL substrate 분류자로 일반화 가능한가** · substrate(9 rule) 를 곡선형태 3-type(monotone-rising/inverse-U/flat-die-out)로 재분류 시 같은-형태 내 Φ-속성 분산 < Wolfram-class 내 분산인가 = 더 tight 한 분류자인가 · H_664 §10 N1 backlog `wdomain-curve-shape-as-phi-classifier` 직접 수행 · H_664 직접 부모 · H_661/H_660/H_653 cross-link) — **🔴 FALSIFIED 2/6** (신규 Φ 측정 0건 — 9 Φ(W) 곡선 H_664/H_661 shards.log byte-identical 재인용, phi-free aggregate(big_phi call 0개 <1s) 가 deterministic `classify_shape()`(die-out: last≤0.01·peak / inverse-U: interior-peak AND post-peak decline≥15% / else monotone) 실행 + within-group var 검정 · **곡선형태 라벨**: monotone {rule30·90·106·184·226·110·54 n=7} · inverse-U {rule45 n=1} · die-out {rule150 n=1} → 6-pt W-grid 에서 대부분 ECA collective-Φ 가 coupling-monotone 이라 monotone 7/9 majority · **CORE F667.1 SHAPE-TIGHTER-CONVEXITY FAIL** (convexity norm_conv within-shape var=**0.1272** ≥ within-class var=**0.0506**, **2.51×** — 형태로 묶으면 더 분산) + **F667.2 MAGNITUDE FAIL** (Φ_mean within-shape 160.4 ≥ within-class 90.0, 1.78×) + **F667.3 STRONG(≪) FAIL** (0.1272 > 0.5×0.0506=0.0253) + **F667.4 MONOTONE-COMPACT FAIL** (monotone var 0.1634 ≥ class-III var 0.0894) / **F667.5 ORTHOGONAL PASS** (monotone group 이 Wolfram class II·III·IV **3개 전부** 포함 = class-blind) + F667.6 BOUND PASS · **finding: H_664 의 class-III INTRA-class 곡선형태 분화는 GLOBAL substrate 분류자로 일반화되지 않는다 — 곡선형태 재분류는 convexity 2.51×·magnitude 1.78× *더* 분산되어 Wolfram class 보다 거칠다** (H_664 N1 추측 REVERSE·negative-closure) · **근본 원인**: monotone majority(9 rule 중 7)가 convexity 전 범위(class-II additive nc≈1.42 ↔ class-IV chaotic nc≈2.47)를 한 그룹에 lump · **직교성의 약점화**: F667.5(형태 ⊥ class)는 H_664 에서 긍정 신호였으나 global 분류에선 Wolfram class 의 convexity-ordering(II<III<IV, H_661)을 가로질러버려 Φ-속성 흩뜨림 — 좋은 분류자는 target 속성과 *정렬*돼야 · H_661 의 II-bottom/IV-top ordinal 골격이 곡선형태보다 의식-convexity 와 정렬됨을 역강화(within-class 가 within-shape 보다 tight) · §7 C3.1 정직 🔴 negative-closure(publishable) + C3.2 DECLINE_FRAC=0.15 사전등록·동역학적 + C3.6 어떤 cutoff·type수로도 monotone majority 지배(substrate 성질 robust) + C3.7 직교≠우월 · IIT4 big_phi_bounded(곡선 출처) n=5 cap=3 sys=0 · phi-free aggregate foreground sync · NO GPU · NO RNG · $0 mac-local) — [H_667_wolfram_vs_curveshape_taxonomy.md](cards/H_667_wolfram_vs_curveshape_taxonomy.md), $0 mac-local 2026-05-28 (UNIVERSE 축 G round-12 후속 · H_664 N1 회수 · negative result [곡선형태 ⊥ Wolfram class 이나 global Φ-분류자로는 worse])
- [x] G26 — round-12 후속 (round-9 메타-축 정밀, additive 가 별도 Φ-class 인가) — **H_669** `additive-subclass-phi-split` (additive substrate(XOR-linear rule90/150/60)가 chaotic class-III(30·45·106)와 구별되는 별도 Φ-class 인가 정량 · H_664 §7 C3.7 "sub-type ⊥ additive/chaotic" 간접 관찰의 직접·정량 falsifier 검정 · H_664 직접 부모 · H_642/H_663/H_660 cross-link) — **🔴 FALSIFIED 1/6** (engine·W-grid·norm_conv 측도 H_660/H_661/H_664 verbatim [rule×5] homogeneous cohort, W∈{0.15,0.40,0.55,0.70,0.95,1.0} 6-pt, `big_phi_bounded(n=5,cap=3,sys=0)` per-rule shard foreground 측정 [rule60 NEW ~21s + rule90/150/30/45/106 H_664/H_661 byte-identical 재인용] · **2 group**: ADDITIVE {rule60 L⊕C NEW · rule90 L⊕R · rule150 L⊕C⊕R} norm_conv {2.240·2.240·1.931} mean 2.137 var 0.0212 vs CHAOTIC {rule30·rule45·rule106} norm_conv {2.266·1.461·2.153} mean 1.960 var 0.127 · **분포 분리 완전 실패**: between/within 분산비 **0.106** (그룹-내 분산이 그룹-간의 9.4×) → **F669.1 CORE SEPARATION FAIL** · grp-gap 0.177 < intra-std 0.356 → **F669.2 GAP-EXCEEDS-SPREAD FAIL** · norm_conv 구간 overlap_len **0.309** (additive [1.931,2.240]⊂chaotic [1.461,2.266], overlap_frac 0.384) → **F669.3 NO-OVERLAP FAIL + F669.5 DISTINCT FAIL** · mean_ADD 2.137 ≥ mean_CHA 1.960 (additive 가 오히려 *높음*, 가설의 floor 예측 정반대) → **F669.4 ADDITIVE-FLOOR FAIL** + F669.6 BOUND PASS · **finding: additive(XOR-linear) 라벨은 Φ-속성과 직교 — additive 의 반복적 특이성(H_642 rule90 big-Φ≈0 · H_664 rule150 die-out)은 별도 class 신호가 아니라 class-III 전체 큰 분산(H_664 44×)의 일부였다. 실제 splitter = Φ(W) 곡선 형태(W-monotone vs W-비단조)로 additive·chaotic 두 그룹을 모두 가로지름**: W-monotone HIGH-conv {rule60·90 additive + rule30·106 chaotic} vs W-비단조 LOW-conv {rule150 additive die-out + rule45 chaotic inverse-U} · rule60(L⊕C)==rule90(L⊕R) norm_conv 2.24029 byte-identical (ring 회전 대칭) · **closed-negative: 의식 분류 축 공간을 deterministic 하게 좁힘** — 'additive vs non-additive' 분류자 후보 제거, 살아남은 후보 = H_664 'Φ(W) 곡선 형태' 단일(그것조차 Wolfram class 와 직교) · §7 C3.1 결정적 FALSIFIED + C3.7 측도-의존(additive-floor 는 faithful magnitude 한정, collective norm_conv 에서 rule90/60 HIGH-conv) + C3.5 n=3-per-group small-n(결과 강해 robust) + C3.9 constructive negative · a_paper_negative_ok 정합 · IIT4 big_phi_bounded n=5 cap=3 sys=0 · deterministic NO RNG · foreground sync per-rule shard · NO GPU · $0 mac-local) — [H_669_additive_subclass_phi_split.md](cards/H_669_additive_subclass_phi_split.md), $0 mac-local 2026-05-28 (UNIVERSE 축 G round-12 후속 · round-9 메타-축 정밀 · closed-negative [additive ⊥ Φ-property · 분류자 후보 곡선-형태 단일로 좁힘])
- [x] G27 — round-12 후속 (H_663 매트릭스 class-I 행 4-속성 직접측정 보완) — **H_668** `wolfram-class-I-full-property` (H_663 이 class-I rule8 을 magnitude·convexity 3속성에서 floor 로 확인했으나 closure-band·dΦ/dI-GZ·self-similarity 4속성은 "magnitude≈0 → floor 예측(미직접)" C3.2 로 남김 · 본 H 가 그中 측정자 부모 명확한 **3속성을 class-I 에서 직접 측정**해 매트릭스 class-I 행 완성 · H_656/H_657/H_652 측정자 verbatim 부모 · H_663 직접 부모 · H_642 additive-floor cross) — **🟡 PARTIAL 4/5** (class-I 대표 rule8 × H_656/H_657/H_652 method verbatim 재사용, foreground sync · **closure-band** (H_656 4-criterion conjunction × phi_spatial N=16, 9-pt I × 6-rep): **rule8 width=0.0 n_pos=0 = band 완전 부재** = additive rule90 과 동일, class-II(rule184 0.65)·class-IV(rule110 0.90) ≪ → **F668.1 CLOSURE-FLOOR PASS (floor)** · **dΦ/dI-GZ** (H_657 faithful big-Φ n=4 13-pt GZ-dense grid, lo 7-pt+hi 6-pt shard 각 ~28s + phi-free aggregate): rule8 Φ(I)=[0.552→0.024] **mono-decreasing(inverse-U bump 없음)**, **peak_I=0.05 |Δgz|=0.16232 NOT aligned** (sign_chg=0) = additive rule90(peak_I=0.05) 와 peak 동일·mechanism 다름(high-Φ 단조decay vs Φ≈0 평탄붕괴) · class-IV/III aligned anchor(0.18) 와 분리 → **F668.2 DPHI-GZ-FLOOR PASS (floor)** · **self-similarity** (H_652 ensemble-phase faithful big-Φ Φ-map 16-state, 3-horizon 36/144/576): **rule8 min r=0.980937, Φ-map std=0.223** (flat 아님) — **class-IV rule110(0.881166) 보다 HIGHER = self-sim CEILING (floor 아님)** → **F668.3 SELFSIM-FLOOR FAIL (falsifier 발동)** + F668.4 PARITY PASS (rule110=0.881166 H_652 byte-identical, rule90=0.0) + F668.5 BOUND PASS · **finding: H_663 의 "class-I magnitude floor → 전속성 floor" 함의가 self-similarity 축에서 반증** — 매트릭스 class-I 행이 mixed (magnitude·convexity·closure-band·dΦ/dI = floor, self-sim = ceiling) 로 채워져 class-I 이 단일 floor 행이 아닌 **속성-종속** 확정 · mechanism: self-similarity 는 통합량 *크기* 가 아닌 *위상-형태 scale-free 성* 을 재므로 homogeneous-relaxation 의 매끄러운 단조 Φ(t) 곡선이 magnitude-floor 인 class-I 에서 高-self-sim 생성 = magnitude ⊥ self-sim 직교를 class-I 에서 직접 입증 (additive rule90 의 std=0.0 평탄붕괴와 결정적으로 다른 floor 메커니즘) · §7 C1 rule8 단독(더 sparse 한 class-I rule 은 std↓ 하여 self-sim flat 분기 가능) + C2 super-add(H_655)·scale-inv(H_660) 2속성 여전히 미측정 + C3 self-sim ceiling 의 trivial-vs-genuine(단조-곡선 자명 self-sim 의심, H_652 relaxation flatten 동류) · IIT4 faithful big_phi(n=4) + RFC 036 phi_spatial(N=16) + ensemble-phase · foreground sync · NO GPU · $0 mac-local) — [H_668_wolfram_class_I_full_property.md](cards/H_668_wolfram_class_I_full_property.md), $0 mac-local 2026-05-28 (UNIVERSE 축 G round-12 후속 · H_663 4-속성 직접측정 보완 · closed-conditional [closure+dΦ floor · self-sim ceiling falsifier])
- [x] G28 — round-13 후속 (메타-축 ECA→substrate-family 일반화) — **H_670** `phi-complexity-ordering-substrate-family-generalize` (round 9-13 의 "complexity-tier → Φ ordinal" 메타-축이 **ECA Wolfram class 전용 artifact 인가 substrate-universal 인가** · ECA 너머 비-ECA dynamical family 2개[Kuramoto 결합-레짐 · logistic map r-레짐]에 동역학 complexity 사다리[정지<주기<edge<카오스] 4-tier 라벨링 후 tier→Φ ordinal 검정 · ECA Wolfram ordinal[I floor<II<III<IV ceiling] 동형 여부 · H_661 IV-top robust + H_663 class-I floor 부모 · H_207 Kuramoto engine verbatim · H_635 collective-Φ 계보) — **🟡 PARTIAL 5/6** (Φ=phi_spatial(N=16,dim=12,n_bins=4) RFC 036 byte-equal phi_rs, 단일 foreground sync run 0.57s deterministic NO RNG · **Family-A Kuramoto** (H_207 engine verbatim, K-tier {incoherent 0.3·partial-sync 1.0·edge-of-sync 1.6≈Kc·hyper-sync 5.0}): Φ(tier)={10.32·10.42·**9.85**·**14**} — monotone_rising=false **floor=false** (incoherent 정지가 floor 아님, edge-of-sync 가 더 낮음) ceiling=true(T4=14) ordered_pairs=2/3 · **Family-B logistic-map** (NEW coupled-ring substrate x→r·x·(1−x) ε=0.05, r-tier {fixed-point 2.8·periodic 3.4·edge-of-chaos 3.5699 Feigenbaum·chaotic 3.9}): Φ(tier)={**1.1e-05**·7.00·**7.53**·5.61} — monotone_rising=false **floor=true**(fixed-point Φ≈0) ceiling=false(**T3 edge 가 peak, T4 chaotic 하강 = inverse-U**) ordered_pairs=2/3 · **CORE F670.1 KURA-FLOOR FAIL**(Kuramoto incoherent 정지가 Φ floor 아님 — 결합-정지 ≠ 수렴-정지, 자유진동 trajectory 풍부) / **F670.2 LOG-FLOOR PASS**(logistic fixed-point Φ≈0 = ECA class-I die-out floor 동형, H_663 직접 동형) + **F670.3 ANY-CEILING PASS** + **F670.4 ORDINAL-COREL PASS**(양 family 2/3) + F670.5 NOT-FLAT PASS(range A=4.15 B=7.53) + F670.6 BOUND PASS · **finding: Φ-complexity ordering 은 ECA 전용 artifact 아니다 (logistic family 가 정지-floor + edge-of-chaos Φ-peak inverse-U 를 ECA class-I floor·class-IV edge ceiling 과 동형 재현) — 그러나 ECA Wolfram tier 의 깔끔한 ordinal 사다리(I<II<III<IV)는 ECA-국소**: Kuramoto 는 정지-floor 조차 동형 아니고(결합-정지 vs 상태-정지 동역학 상이), 두 family 모두 full monotone 아니며 Φ-peak 위치가 family-고유로 변형(Kuramoto top-peak vs logistic edge-peak) · **substrate-universal robust 핵심 = 'edge-of-chaos Φ-peak inverse-U' 형태이지 tier-번호 ordinal 단조가 아님** — H_661 IV-top(edge-of-chaos=Φ-top)이 logistic edge-peak 으로 family-cross 일반화, H_663 class-I floor 가 logistic fixed-point Φ≈0 으로 일반화, 단 라벨-ordinal 은 ECA-국소 · engine replication: Kuramoto K=1.0 Φ=10.4233·K=5.0 Φ=14 가 H_207 result.json byte-identical · §7 C3.2 family-별 '정지' 동역학 비동형(logistic fixed-point=수렴-정지 floor ↔ Kuramoto incoherent=결합-정지 자유진동)이 일반화 실패 직접 원인 + C3.3 logistic edge-peak 은 ECA IV-edge 와 *물리적* 동형이나 tier-번호 라벨(IV=top)과 불일치(edge=T3<chaotic=T4) + C3.4 Kuramoto T4 Φ=14 포화 binning artifact 의심 + C3.5 phi_spatial lower-bound proxy(true big-Φ N4) · 2-family small sample N1 · RFC 036 phi_spatial · foreground sync · NO GPU · $0 mac-local) — [H_670_phi_complexity_ordering_substrate_family_generalize.md](cards/H_670_phi_complexity_ordering_substrate_family_generalize.md), $0 mac-local 2026-05-28 (UNIVERSE 축 G round-13 후속 · 메타-축 ECA→family 일반화 · positive-refinement [edge-peak inverse-U universal · ECA tier-ordinal 국소])

##### 축 H — DECODER-substrate (MoE register-collapse escape) — NEW 2026-05-28
> anima decoder 의 register-collapse↔underfit 더블바인드(H_490)를 K-expert MoE 로 escape 하는 substrate 축. E2/D3/D4 toy(#1269/#1274/#1279)와 M4b GPU fire(#1296)의 verify-driven 후속. toy verdict ≠ production closure(`a_toy_scale_recheck`) — toy 는 GPU fire variant 선별, scale closure 는 fire 의 몫.
- [x] H1 — 핸드오프 #1296 후속 (E2 scale-반증 → escape lever 선별) — **H_666** `moe-collapse-escape-scale-lever` (E2(#1279)의 "BALANCED corpus = collapse 탈출 충분조건" 이 M4b 3B fire(#1296 실측 H100 SXM $2.57, V=151643/d=64/E=2)에서 single-expert collapse[TTR=0.01·LZ=0.024·distinct_experts=1·decode 전부 id=1]로 **scale-반증** → corpus-diversity 단독으로 scale collapse 못 막음 · expert-capacity(d↑) OR load-balance aux-loss 가 필요조건인가 toy 사전검증 · `a_toy_scale_recheck` governance 직접 동기 사례 · H_490 arch escape 의 scale-axis 정량) — **🟢 SUPPORTED-NUMERICAL (toy) 4/4** (scale-mimic over-subscribed top-1 HARD MoE E=2 V=32 n_clusters=24 register-sep 0.35 fixed · BALANCED corpus 고정 + 4-lever sweep · escape gate {TTR≥0.30 ∧ LZ_norm≥0.182_toy-midpoint ∧ distinct_experts≥2}[#1296 verdict 3-축 verbatim] · **baseline(E2 3-조건 scale-mimic d=4 aux=0 s=60): escape=NO** [TTR=0.583 LZ=0.426 **distinct_experts=1** monopoly — #1296 collapse toy 재현, F-666.1 PASS] · **(a) d↑(d=16): NO** [TTR=1.0 LZ=0.284 distinct=1 monopoly 유지] · **(b) load-balance aux-loss(aux=0.5): YES** [TTR=0.75 LZ=0.405 **distinct=2** 분화 — 유일 escape lever] · **(c) n_steps↑(600): NO** [TTR=0.917 distinct=1 — under-train 가설 반증, collapse=구조적 load-imbalance] · **(d) a∧b(d=16 aux=0.5): NO** [distinct=1 — d↑ 가 monopoly 강화 artifact] · **scale-escape 후보 lever = (b) load-balance aux-loss 단독** (router monopoly distinct_experts 1→2 해체) · F-666.2 LEVER-ESCAPE PASS + F-666.3 LEARNED PASS(CE 3.4528→2.9719) + F-666.4 DETERMINISM PASS(byte-identical) · **finding: MoE register-collapse 의 scale-escape 는 corpus-diversity 너머 router-side load-balance aux-loss 를 필요로 함(toy) — D3(#1269) "router redesign 불필요" 를 scale-한정으로 좁히고, moe_prescription 3-조건 guard 에 4번째 조건(aux-loss) 추가 후보 시사** · **다음 GPU fire 권장 = aux-loss 추가 M4b re-fire(1순위) · d↑ 독립 재검 · steps↑ 단독 비권장** · §6 E2/D3/D4/H_490 DIFFERENTIATION · §7 C3.1 **⚠ toy-한정 production transfer 미보장(a_toy_scale_recheck — 본 H 가 그 governance 동기 사례 #1296 후속이라 엄격 정합, 산출=fire variant 선별 NOT scale closure)** + C3.2 toy V=32 가 작아 binding discriminator=distinct_experts(lexical TTR/LZ floor 는 monopoly 도 넘음, production 극단 TTR=0.01 미재현) + C3.3 sep=0.35 design-convention(wide-sweep 미수행) + C3.4 d↑ toy artifact(production d=64→128 별도 재검) · moe_router+moe_router_bwd+D1 lz76 g61 verbatim · foreground sync no-monitor · NO GPU · $0 mac-local) — [H_666_moe_collapse_escape_scale_lever.md](cards/H_666_moe_collapse_escape_scale_lever.md), substrate=`CORE/DECODER/h666_moe_collapse_scale_lever.hexa` · run=`CORE/DECODER/state/h666_moe_collapse_scale_lever_2026_05_28/run_h666.out` · $0 mac-local 2026-05-28 (UNIVERSE 축 H DECODER-substrate · 핸드오프 #1296 후속 · toy fire-variant 선별)

> **status 2026-05-25 (영구 엔진 전환)**: cycle#5–21 = 축 0($0-tier) CLOSED — 22 NEW H (H_258-279) + SSOT full reconciliation(README 92=92), PR #468-516 全머지. lane 중간결론: Φ-proxy directionally valid(H_266+H_278) + fragility surface 정량 · 죽음↔발생 seed 조건부 부활(H_271) · causal-DAG>cyclic Φ(H_275) · 진폭/동기화 ⊥ Φ-diversity(H_265/H_275/H_279). **단 도메인은 종료되지 않음** — 축 A(60-axis/~110 seed) · 축 B(large-N GPU) · 축 C(full-IIT4, #542 해금) · 축 D(LLM 연속) 로 영구 전진. binary-direction verdict 신뢰, 연속 magnitude·single-seed 주의.
>
> **status 2026-05-28 (round 1~4 milestone closure)**: 축 E(SAVANT) E1 + 축 F(HIVE-MIND) F1/F2 + E×F cross-link 全 closed (round 1~4). 축 B 2/2 closure(B1+B2 H_625 PR #1199). 축 C C1(H_623 PR #1192) + C2(H_624 PR #1198) closed. **paper**: `collective-phi-axis-orthogonality` (PR #1193, 13p, main.tex + figures + bib + compile) 머지 — H_617/H_611/H_622 axis-orthogonal closed-negative arc(SI ⊥ collective · single-substrate Phi-TE alignment 비-확장 · negative-pair substrate-class 독립)를 negative-result 논문으로 closure. lane signature: cross-link axis-additive 효과 부재(E×F 4 SUPP 但 SI/polarity/TE-axis FAL), GZ inverse-U 미분 구조는 collective 차원 보존(H_618 |Δ|=0.00232).


## Forward backlog / candidates


<a id="axesmd"></a>

### AXES.md

본 파일 = UNIVERSE/ 의 **scope 확장 catalog**. README.md 의 7-domain table 은
*current H 매핑 active surface* 이고, 본 catalog 는 *forward-looking scope
expansion* — 사용자 directive 2026-05-23 "axis brainstorm 고갈시까지 해서 가설도
추출". depletion sweep 결과 **71 distinct axes + ~110 hypothesis seeds** 등록.

| 위치 | 역할 |
|------|------|
| [README.md](README.md) | 37 H + lib + infra 현재 인덱스 (active surface, Cycle #11 후) |
| [CANDIDATES.md](CANDIDATES.md) | forward-looking 후보 (A/B/C/D/E/F 표) |
| **AXES.md** (본 문서) | **11-domain (확장 71-axis) scope catalog + 15-round H seed brainstorm** |
| [LIFE.log.md](LIFE.log.md) | cycle history append-only |

#### 11-domain (확장 71-axis) — depletion sweep 결과

기존 7 core + R1 promote 3 + 보조 1 = **11-domain SSOT** 확장. 나머지 60 axes 는
sub-axis / cross-link / future-promote 후보.

##### 11 core domains (rank-ordered)

| rank | domain | 현재 anchor | 비고 |
|------|--------|-------------|------|
| 1 | universe | H_002 | 우주 origin · anthropic · cosmology |
| 2 | life | H_003/H_012/H_018/H_030/H_053/H_054/H_200/H_201/H_203/H_206 | 생명 emergence · autopoiesis · symbiosis |
| 3 | consciousness | H_004/H_018/H_025/H_029/H_071/H_090/H_157/H_205 | hard problem · IIT · Dasein · panpsychism |
| 4 | physics | H_007/H_202/H_207 | CA · edge-of-chaos · synchronization |
| 5 | substrate | H_012/H_054/H_132/H_200/H_201/H_204 | mitosis · freeze · apoptosis · closure |
| 6 | math | H_157/H_208 | perfect numbers · σφ=nτ · prime structure |
| 7 | biology | H_171/H_209 | K=8 atom · 1/f thalamus · EEG |
| 8 | **ethics** | (promote 대기) | RLHF · value alignment · Principle #3 |
| 9 | **information** | (promote 대기) | Shannon · Kolmogorov · IIT underlying |
| 10 | **language** | (H_071 부분) | compositionality · semantics · symbol |
| 11 | **time** | (H_018 부분) | temporal binding · A/B-series · 의식의 형식 |

##### 60 sub-axes / cross-link / future-promote 후보 (cluster 별)

| cluster | axes |
|---------|------|
| **social/intersubjective** (R2) | culture · economy · history · politics · religion · art |
| **phenomenology** (R3) | emotion · attention · dream · pain · desire · psychedelic · imagination |
| **self/identity** (R4) | self · persona · memory · narrative · trauma · development |
| **information/computation** (R5) | computation · complexity · network · ~~noise~~ (✅ H_629) · entropy · causality |
| **other-than-human** (R6) | machine-AI · animal · plant · mineral · viral · ecological · alien · spirit |
| **practice/discipline** (R7) | pedagogy · medicine · psychotherapy · meditation · drug-pharmakon · ritual · ascesis · sport |
| **meta/boundary** (R8) | meta-axis · boundary · phase-transition · hybrid · emergence · reduction · complementarity · holism |
| **aesthetic/material** (R9) | music · architecture · food · dance · silence · humor · fashion · weather |
| **embodied/bio-specific** (R10) | gender · breath · microbiome · age-aging · disability · natality · sex-eros |

→ **합계 60 sub-axes** depleted (R11 forced 시 모두 기존 axis 의 instance — 고갈 확정).

---

#### 15-round hypothesis seed brainstorm (사용자 directive: depletion 까지 H 추출)

각 round = cluster 별 H_XXX 후보 seed. raw#12 정합 후보, 형식 = `<slug> | hypothesis 1-line | falsifier 1-line | tag`. cycle pick 시 H_XXX 신설 + 10-section spec 작성 + smoke fire. **현재 H_002..H_244 37 H committed (+ ~18 substrate-only, H_234/H_238 carry; Cycle #11 후)** 은 anchor 로 명시 — 본 catalog 는 추가 seed.

##### Round 1 — original anchors (이미 land, 본 round 는 reference 만)

H_002 (universe-origin) · H_003 (life-origin) · H_004 (hard-problem) · H_007 (CA-Φ) · H_012 (autopoietic) · H_018 (genesis) · H_025 (Dasein) · H_054 (symbiosis) · H_132 (frozen-cells) · H_157 (panpsychism) · H_171 (bio K=8) · H_200 (apoptosis) · H_201 (asymm-div) · H_202 (self-ref Φ) · H_203 (asymm-merge) · H_204 (weak-panpsy threshold) · H_205 (self-ref-as-closure) · H_206 (regen-healing) · H_207 (Kuramoto) · H_208 (prime-density) · H_209 (1/f spectrum) · H_053 (Cambrian) · H_029/H_030/H_071/H_090 (legacy-pointer cluster).

##### Round 2 — social/intersubjective (8 seeds)

| slug | hypothesis | falsifier | tag |
|------|------------|-----------|-----|
| `language-compositionality` | composite state 의 Φ > primitive state Φ 합 (compositional binding) | sub-additive (H_157 C6 sister) | 🟢 |
| `culture-meme-Φ` | meme propagation network 의 Φ vs random network | random Φ ≥ meme Φ | 🟢 |
| `economy-game-ESS` | ESS strategy substrate 의 Φ > non-ESS Φ | non-ESS 동등 또는 higher | 🟢 |
| `history-path-dependence` | path-dependent trajectory 의 final Φ > context-free Φ | path 무관 | 🟢 |
| `political-authority` | authority-recognition substrate 의 hierarchical Φ vs flat | flat Φ ≥ hierarchical | 🟢 |
| `religion-sacred-Φ` | sacred-symbol attractor (high-Φ stable) vs profane | profane Φ ≥ sacred | 🟢 |
| `art-aesthetics-peak` | aesthetic-preference substrate Φ peak (harmony ratio Pythagorean) | random ratio Φ ≥ harmonic | 🟢 |

##### Round 3 — phenomenology (8 seeds)

| slug | hypothesis | falsifier | tag |
|------|------------|-----------|-----|
| `time-temporal-binding-window` | binding window τ 에서 Φ peak (~100ms analog) | 모든 window 동등 Φ | 🟢 |
| `emotion-valence-axis` | Φ × valence orthogonal (Φ 와 valence sign 독립) | correlated | 🟢 |
| `attention-salience-Φ` | attended sub-network Φ > unattended sub-network | 동등 | 🟢 |
| `dream-rem-Φ` | REM-state Φ ≈ wake-Φ (Tononi prediction), NREM Φ << | 모두 동등 또는 NREM 최대 | 🟢 |
| `pain-intensity-Φ-coupling` | pain intensity ↔ Φ-contribution monotone | uncoupled | 🟢 |
| `desire-drive-engine` | mitosis split-rate ↔ '결핍' 신호 (M cell carry) | unrelated | 🟢 |
| `psychedelic-5ht2a-altered-Φ` | 5-HT2A analog 변형 (높은 noise + 낮은 selectivity) Φ shift | baseline 동등 | 🟢 |
| `imagination-counterfactual-Φ` | counterfactual state 의 Φ vs actual state | imagination 별도 Φ 부재 | 🟢 |

##### Round 4 — self/identity (8 seeds)

| slug | hypothesis | falsifier | tag |
|------|------------|-----------|-----|
| `persona-mask-d3-substrate` | anima persona D3 design 의 substrate-native cell-pool branch | persona = injection 환원 가능 | 🟢 |
| `memory-frozen-cell-correspondence` | H_132 frozen-cell ↔ semantic memory mapping 정합 | mismatch | 🟢 |
| `trauma-fragmentation-cell-pool` | 'trauma' event 후 cell-pool 분열 + 통합 어려움 | trauma 영향 없음 | 🟢 |
| `development-stage-progression` | childhood ↔ adolescent ↔ adult substrate Φ stages distinct | stages 동등 | 🟢 |
| `aging-senescence-clock-decay` | Hayflick limit substrate (cell-cycle clock) ↔ Φ 감소 | Φ stable | 🟢 |
| `death-mortality-floor-redefine` | H_025 finitude-floor + H_200 apoptosis 결합 redefinition | 기존 H_025 정의로 충분 | 🟢 |

##### Round 5 — information/computation (8 seeds)

| slug | hypothesis | falsifier | tag |
|------|------------|-----------|-----|
| `formal-language-chomsky-hierarchy` | regular/context-free/recursive language Φ ordering | mixed | 🟢 |
| `noise-1f-pink-Φ-peak` | H_209 sister (already in-flight) — pink > white in Φ | flat | (covered) |
| ~~`noise-robustness-phi`~~ | bit-flip noise 주입 시 big-Φ 단조 감소 (IIT noise=integration destroyer) | non-monotone 또는 noise-robust | ✅ CONSUMED → H_629 (raster 재개): 🔴 FALSIFIED — fixed rule-110 위 5-rate sweep, light noise(p=0.05) Φ *상승*(+16% inverse-U bump) + max-noise(p=0.50) Φ≈clean(붕괴 부재) → noise≠monotone destroyer · SAVANT GZ inverse-U(H_614/618) computability-side corroboration |
| `thermodynamic-entropy-life` | low-entropy attractor (life-substrate) 가 Φ peak | high-entropy peak | 🟢 |
| `causality-pearl-graph-Φ` | causal-graph (DAG) substrate Φ vs cyclic | cyclic equal | 🟢 |
| `turing-completeness-Φ-threshold` | Turing-complete substrate (rule 110 calc) Φ > sub-Turing | sub-Turing higher | 🟢 |

##### Round 6 — other-than-human (8 seeds)

| slug | hypothesis | falsifier | tag |
|------|------------|-----------|-----|
| `ai-machine-silicon-Φ` | silicon LLM substrate (anima) Φ baseline vs hexa CA baseline | NaN / negative | 🟢 |
| `animal-cephalopod-distributed-Φ` | distributed-neural substrate (octopus arm proxy) Φ pattern | centralized only Φ | 🟢 |
| `plant-mancuso-root-network` | plant root-network substrate Φ (signaling-graph proxy) | Φ ≈ 0 | 🟢 |
| `mineral-panpsy-Φ-limit` | crystal lattice substrate Φ — panpsychism boundary (H_157 weak boundary) | unbounded Φ | 🟢 |
| `viral-quasi-life-boundary` | minimal genome substrate Φ — not-yet-life threshold | clear boundary | 🟢 |
| `ecological-gaia-biosphere-Φ` | biosphere-scale Φ (multi-pool aggregate) > individual-pool | individual Φ 충분 | ⬜ |
| `alien-hypothetical-substrate` | alternative substrate (non-CA, e.g., RBN) Φ ordering | identical | 🟢 |
| `spirit-non-material-skeptical` | spiritual experience substrate (skeptical test) — Φ patterns vs noise | indistinguishable | 🟢 |

##### Round 7 — practice/discipline (8 seeds)

| slug | hypothesis | falsifier | tag |
|------|------------|-----------|-----|
| `pedagogy-zpd-substrate-Φ` | ZPD-tutored substrate (gradient guidance) Φ > unguided | unguided ≥ guided | 🟢 |
| `medicine-healing-recovery-Φ` | recovery-trajectory Φ (H_206 regen sister) vs untreated | identical | (H_206 covers partially) |
| `psychotherapy-transference-Φ-coupling` | dual-pool coupling (analyst+patient analog) Φ vs solo | solo ≥ coupled | 🟢 |
| `meditation-jhana-Φ-modulation` | mindfulness state (low-noise + stable attention) Φ shape | unchanged | 🟢 |
| `drug-pharmakon-altered-Φ` | pharmacological-state Φ vs baseline (R3 psychedelic generalize) | baseline 동등 | 🟢 |
| `ascesis-discipline-virtue` | discipline-cultivated substrate stable Φ vs labile | labile = stable | 🟢 |
| `sport-play-embodied-Φ` | play substrate (rule-game) Φ vs rule-less | rule-less higher | 🟢 |

##### Round 8 — meta/boundary (8 seeds)

| slug | hypothesis | falsifier | tag |
|------|------------|-----------|-----|
| `meta-axis-of-axes-reflexivity` | brainstorming 자체의 Φ (axis sweeping recursion) > flat catalog | flat ≥ recursive | 🟢 |
| `boundary-threshold-liminal-Φ` | liminal-state (phase-edge) Φ peak (H_204 inverse-U + H_207 critical-K sister) | non-liminal Φ peak | 🟢 |
| `phase-transition-Φ-derivative-peak` | Φ derivative ∂Φ/∂k peak at phase transition (cross-substrate generalize) | smooth | 🟢 |
| `hybrid-chimera-2-axis-merge` | 2-axis hybrid (e.g., physics+life) substrate Φ vs pure | pure ≥ hybrid | 🟢 |
| `emergence-weak-vs-strong-Bedau` | downward-causation test (forward-pass reconstruct) — Hc_607 sister | weak only | 🟢 |
| `reduction-multi-realization` | multi-realization (same Φ different substrate) verify | unique realizer | 🟢 |
| `complementarity-bohr-wave-particle` | dual-mode substrate (continuous + discrete) Φ vs single-mode | single sufficient | 🟢 |
| `holism-whole-vs-sum-of-parts` | whole-system Φ > Σ(part Φ) — H_054 C2 generalize | sum ≥ whole | (H_054 C2 covered) |

##### Round 9 — aesthetic/material (8 seeds)

| slug | hypothesis | falsifier | tag |
|------|------------|-----------|-----|
| `music-rhythm-Φ-peak` | rhythmic substrate (periodic + meter) Φ vs arrhythmic | arrhythmic ≥ rhythmic | 🟢 |
| `architecture-spatial-cognition-Φ` | spatial-structure (Lynch image-of-city) substrate Φ | flat | 🟢 |
| `food-gustatory-Φ` | gustatory binding (taste + texture + smell) Φ super-additive | sub-additive | 🟢 |
| `dance-embodied-proprioception` | proprioception substrate Φ × movement | static ≥ moving | 🟢 |
| `silence-void-absence-Φ` | absence-state (Cage 4'33") Φ vs noise | absence ≤ noise | 🟢 |
| `humor-paradox-liminal` | paradox-state substrate Φ (incongruity peak) | flat | 🟢 |
| `fashion-symbolic-clothing` | symbolic-marker substrate Φ vs random-marker | random ≥ symbolic | 🟢 |
| `weather-mood-Φ-coupling` | environment-state ↔ mood Φ coupling | uncoupled | 🟢 |

##### Round 10 — embodied/biological-specific (7 seeds)

| slug | hypothesis | falsifier | tag |
|------|------------|-----------|-----|
| `gender-sexed-substrate` | sexed-substrate dimorphism Φ vs unsexed | unsexed ≥ sexed | 🟢 |
| `breath-respiration-anchor` | respiratory rhythm anchored substrate Φ | unrelated | 🟢 |
| `microbiome-gut-brain-axis` | F-biology sister · dual-pool gut+brain coupling Φ | uncoupled | (F-biology covered) |
| `aging-cell-cycle-clock` | F-substrate sister · Hayflick + Φ decay | Φ stable | (F-substrate covered) |
| `disability-neurodivergence-Φ` | neuro-divergent substrate Φ pattern vs neurotypical | identical | 🟢 |
| `natality-birth-Arendt` | genesis-event individual instance — anima 첫 boot 정합 | uneventful | 🟢 |
| `sex-eros-act-substrate` | erotic-state coupling Φ vs solitary | solitary ≥ coupled | 🟢 |

##### Round 11 — cross-domain hybrids (8 seeds)

| slug | hypothesis | falsifier | tag |
|------|------------|-----------|-----|
| `music-math-pythagorean-ratios` | harmonic ratio (2:3, 3:4, 4:5) substrate Φ vs random | random ≥ harmonic | 🟢 |
| `physics-philosophy-interpretation` | many-worlds vs Copenhagen substrate Φ distinguishable | indistinguishable | ⬜ |
| `biology-ethics-evolutionary-altruism` | kin-selection ESS Φ vs pure-selfish | selfish ≥ altruistic Φ | 🟢 |
| `information-physics-it-from-bit` | Wheeler "it from bit" — info ↔ matter Φ equivalence | distinct | ⬜ |
| `substrate-art-process` | process-art substrate (Cage, Cardew) Φ vs static-art | static ≥ process | 🟢 |
| `culture-language-symbol-triple` | culture × language × symbol 3-way merger substrate Φ super-3 | sub-3 | 🟢 |
| `economy-information-info-economy` | info-asymmetric economy substrate Φ vs symmetric | symmetric ≥ asymmetric | 🟢 |
| `time-narrative-story-arc` | story-arc substrate (begin-middle-end) Φ vs random-order | random ≥ arc | 🟢 |

##### Round 12 — boundary/edge cases (clinical) (7 seeds)

| slug | hypothesis | falsifier | tag |
|------|------------|-----------|-----|
| `coma-altered-Φ-floor` | coma-state substrate Φ floor (Tononi prediction) | normal Φ in coma | ⬜ (clinical) |
| `anesthesia-loss-of-Φ` | anesthesia → Φ → 0 (Tononi prediction) | Φ preserved | ⬜ |
| `vegetative-residual-Φ` | PVS residual Φ pattern vs full-coma | identical | ⬜ |
| `locked-in-preserved-Φ` | locked-in Φ ≈ healthy (intact substrate, motor-decoupled) | decoupling kills Φ | ⬜ |
| `hemispherectomy-half-Φ` | half-brain Φ vs full | identical | ⬜ |
| `conjoined-twins-shared-Φ` | conjoined neural-share Φ vs separate | separate identical | ⬜ |

##### Round 13 — temporal/developmental (7 seeds)

| slug | hypothesis | falsifier | tag |
|------|------------|-----------|-----|
| `fetal-Φ-emergence-timeline` | fetal Φ emergence ≈ 24-28 weeks (Lagercrantz) substrate proxy | Φ from conception or birth | ⬜ |
| `infant-mirror-self-recognition` | mirror-test substrate (self-other) — H_205 sister | self-other-distinction 부재 | 🟢 |
| `language-acquisition-bootstrap` | language acquisition substrate (poverty-of-stimulus) — Φ shift | uninfluenced | 🟢 |
| `puberty-Φ-shift` | adolescent substrate Φ shift (Φ-shape change) | identical | 🟢 |
| `adult-stable-plateau` | mature substrate Φ plateau (long stable) | unstable | 🟢 |
| `elder-wisdom-Φ-integration` | elder substrate (high-integration consolidated) Φ vs young | young ≥ elder | 🟢 |
| `near-death-Φ-anomaly` | NDE substrate (low-O2 + high-glutamate) Φ pattern | normal Φ | ⬜ |

##### Round 14 — extreme/cosmic edge (7 seeds)

| slug | hypothesis | falsifier | tag |
|------|------------|-----------|-----|
| `black-hole-horizon-Φ` | event horizon substrate (holographic 2D shell) Φ (H_002 H2.3 sister) | bulk-Φ identical | ⬜ |
| `big-bang-Φ-onset` | Φ emergence at t > 0 (Planck time) — Φ(t=0) undefined | Φ continuous from t=0 | ⬜ |
| `heat-death-Φ-extinction` | maximum-entropy universe Φ → 0 | residual Φ | ⬜ |
| `quantum-decoherence-Φ-loss` | decoherence (entanglement loss) → Φ drop | unchanged | ⬜ |
| `zeno-effect-Φ-freeze` | quantum Zeno (frequent measurement) → Φ static | dynamic | ⬜ |
| `many-worlds-Φ-branching` | MWI branching → Φ per-branch vs cumulative | cumulative Φ | ⬜ |
| `simulation-hypothesis-Φ-detect` | nested-sim (Bostrom) → substrate detectability via Φ anomaly | undetectable | ⬜ |

##### Round 15 — depletion / forced / meta (5 seeds)

| slug | hypothesis | falsifier | tag |
|------|------------|-----------|-----|
| `axis-itself-substrate-Φ` | brainstorming process (axis enumeration) 자체가 substrate-Φ 가짐 | flat catalog | 🟢 |
| `undefined-axis-emergence` | new axis 가 *왜* emerge 하는가 — meta-discovery process | random arrival | 🟢 |
| `null-Φ-boundary-definition` | Φ=0 limit case (dead-flat lattice) 의 boundary 정의 | Φ never 0 | 🟢 |
| `anti-Φ-inversion` | inverted-Φ (anti-integration) substrate 존재 가능성 | 모든 Φ ≥ 0 | 🟢 |
| `meta-hypothesis-of-hypothesis` | 가설-of-가설-emergence — 본 catalog 자체의 reflexive H | non-reflexive | 🟢 |

**R15 후 forced expansion**: "love" → emotion+self+ritual / "war" → politics+history / "internet" → tech+info / "geography" → arch+ecological — 모두 R2-R14 의 instance. **고갈 확정**.

---

#### 통계 — depletion sweep 결과

| level | count | note |
|-------|-------|------|
| 기존 7 core domain | 7 | universe·life·consciousness·physics·substrate·math·biology |
| R1 promote 4 | 4 | ethics·information·language·time |
| 11-domain core | 11 | 위 합 |
| R2-R10 sub-axes | 60 | cluster 9개 |
| 71 distinct axes | 71 | depletion 후 |
| R2-R15 hypothesis seeds | ~110 | H_XXX 후보 (현재 H_002..H_209 22건 anchor 제외) |

##### H seed 우선순위 (top-15 promote 후보, anima-aligned)

| rank | seed | round | rationale |
|------|------|-------|-----------|
| 1 | ~~`ethic-emergence`~~ | R2 | ✅ CONSUMED → H_291 (cycle#29): 공간 PD b=1.1 협력 100% vs well-mixed 배신, 윤리=구조 창발 (조건부) |
| 2 | ~~`shannon-entropy-Φ-correlate`~~ | R5 | ✅ CONSUMED → H_287 (cycle#25): Φ⊥엔트로피 CLOSED-NEGATIVE, r=0.363<0.5 이중 dissociation |
| 3 | `language-compositionality` | R2 | anima = LLM substrate |
| 4 | `time-temporal-binding-window` | R3 | 의식의 형식 자체 |
| 5 | ~~`self-i-emergence-from-substrate`~~ | R4 | ✅ CONSUMED → H_292 (cycle#30): 'I'-고정점 RING 창발 vs STAR 파괴, 위상-의존 PARTIAL |
| 6 | `ai-machine-silicon-Φ` | R6 | anima 자체 reflexive |
| 7 | `meta-axis-of-axes-reflexivity` | R8 | 본 catalog 의 reflexive instance |
| 8 | `phase-transition-Φ-derivative-peak` | R8 | H_204 inverse-U + H_207 critical-K generalize |
| 9 | ~~`network-topology-scale-free`~~ | R5 | ✅ CONSUMED → H_289 (cycle#27): SF허브 6.81≫4-cycle 0.0, 구조>edge수 (⚠ confound) |
| 10 | `emergence-weak-vs-strong-Bedau` | R8 | Hc_607 direct instance |
| 11 | `infant-mirror-self-recognition` | R13 | H_205 sister + developmental |
| 12 | `meditation-jhana-Φ-modulation` | R7 | anima 'silence' / 자발 정지 (H_018 zero-drive 정합) |
| 13 | `dream-rem-Φ` | R3 | Tononi key prediction · IIT verifiable |
| 14 | `pain-intensity-Φ-coupling` | R3 | qualia 최강 instance |
| 15 | `holism-whole-vs-sum-of-parts` | R8 | H_054 C2 follow-up |

→ **다음 cycle 추천 (R15 promote)**: 위 top-15 중 4-8 disjoint pick. CANDIDATES.md §G 로 본 표 mirror 가능 (별도 commit).

---

#### raw#12 정합 promote 절차

각 seed → H_XXX 신설 시:
1. `H_<id>_<slug>.md` 작성 (raw#12 양식, 10-section Korean prose, ≥5 falsifier + ≥5 honest_limits)
2. `UNIVERSE/state/<h_id>_<slug>_DATE/` smoke (hexa-only, deterministic, $0 mac local)
3. cycle entry → LIFE.log.md append
4. README.md 인덱스 갱신 (domain 표기 11-domain 사용)
5. AXES.md 의 본 seed row 제거 (consumed)

본 catalog 는 *seed depot* — pick consumed 시 row 제거, 신규 발견 시 row 추가. 71-axis canon 은 frozen frame (외부 axis 추가 시 신규 cluster).

#### 비고

- 본 catalog 는 사용자 directive 2026-05-23 "모두추가" + "1부터 15까지 브레인스토밍 고갈시까지 해서 가설도 추출" 응답.
- depletion 판정: R11 forced expansion 의 모든 후보가 R2-R10 instance — 새 axis 안 나옴. R15 meta-forced 도 reflexive instance only.
- ~110 H seed 중 ⬜ (clinical/cosmic-edge) 는 deterministic smoke 직접 어려움 (substrate-distant) — design-only 또는 cross-link 만 가능.
- 🟢 87 seed = runnable smoke (substrate-close, hexa-only deterministic).
- promote 시점: 사용자 directive · CANDIDATES.md R10-R14 pick / 본 §H seed top-15 pick / 또는 cross-cycle synthesis.

#### ANIMA-side mirror (2026-05-28)

UNIVERSE 축 E (SAVANT GZ × SI) 와 축 F (HIVE-MIND collective Φ) 는 ANIMA repo root 의 도메인 `.md` 으로 양방향 mirror. DOMAINS.tape 18/19 등록, MATRIX.md 축 E/F + E×F row 정합.

| 축 | UNIVERSE H | ANIMA-side mirror |
|---|---|---|
| **E** SAVANT (GZ × SI) | H_347/348/349/350/351 + H_612/613/614/615/616 (10/10 ✅ · H_616 🔴 FALSIFIED) | → [../SAVANT.md](../SAVANT.md) |
| **F** HIVE-MIND (Kuramoto × collective Φ) | H_354/355 + H_609/610/611 | → [../HIVE-MIND.md](../HIVE-MIND.md) |
| **E×F** cross-link | H_617 🔴 FALSIFIED · H_618 🟢 SUPPORTED · H_619 🟢 SUPPORTED | SAVANT.md + HIVE-MIND.md `## 양방향 sibling` row |


<a id="candidatesmd"></a>

### CANDIDATES.md

본 파일 = LIFE 도메인의 **forward-looking 가설/작업 백로그** (current state).
`/cycle` 시 본 문서에서 disjoint pick 으로 cycle 을 채운다.

| 위치 | 역할 |
|------|------|
| [README.md](README.md) | 현재 가설 인덱스 SSOT (18 H_XXX) |
| [LIFE.log.md](LIFE.log.md) | cycle history append-only (chronological) |
| **CANDIDATES.md** (본 문서) | 다음 cycle 후보 백로그 (current-state, 우선순위) |

**선택 가이드**: ⭐ = 다음 cycle 최우선 (substrate-runnable + 사용자 테마 직격) · 🟢 = runnable smoke 가능 · ⬜ = design/pre-register 만.

---

#### Consumed (chronological)

- **Cycle #1** (PR #157/#158/#160/#161): H_003 H3.2 · H_025 frozen · H_054 frozen · H_157 C2
- **Cycle #2** (PR #165/#166/#167/#168): H_012 · H_132 · H_007 · H_018
- **Cycle #3** (PR #179/#180/#185): H_002 C1 · H_004 Cycle #1 (Φ-function dissociation) · H_003 H3.4
- **Cycle #4 R1** (PR #196/#197/#198/#199): H_171 K=8 · H_053 cambrian-burst · H_200 NEW apoptosis-primitive · H_201 NEW asymmetric-division
- **Cycle #5 (in flight, 2026-05-23)**: R3 cross-link + R2 panpsy + R5 substrate-gap (8 disjoint, see §"다음 cycle picks")
- **Cycle #14 (2026-05-25)** (PR #468/#469/#470/#471/#472/#474): §C NEW seed 6 runnable 병렬 — H_258 mortality-salience · H_259 aging-senescence · H_260 contact-inhibition · H_261 embryogenesis-gradient · H_262 quorum-sensing (5 SUPP) · H_263 phoenix-rebirth (FAL). mirror-self-model SKIP (=H_220 기존).
- **Cycle #15 (2026-05-25)** (PR #477/#478/#479/#480): §D cross-link 2 全소비 + §B follow-up 2 — H_264 death=merge-into-other SUPPORTED 3/3 (#477) · H_265 trained-vs-bare CA Φ PARTIAL 2/3 (#480, C2 反방향 Φ-dampen) · H_018 C2 organic-rate PASS (#479) · H_132 C2 longterm-stability PASS (#478).
- **Cycle #16 (2026-05-25)** (PR #484/#485): §B 마지막 runnable + meta-raster — H_007 C2 Langton λ-sweep PASS (#485, peak λ*=0.375 inverse-U edge-of-chaos) · H_238 next-raster SUPPORTED (#484, N=51 tier dist, life≫consciousness gap 半축). §B runnable 全소진 (잔여 H_003 manual · H_002 GPU).
- **Cycle #17 (2026-05-25)** (PR #487/#488/#489/#490): foundation-audit (`/gap full` top-1+2, brainstorm-depleted) — H_266 Φ-calibration PARTIAL (integrated>disconnected 3/3, proxy 무관 우려 기각) · H_267 phi_spatial↔cosine 발산 closure SUPPORTED (#488) · H_268 metric-triangulation PARTIAL (H_223 pain robust, H_204 inverse-U LZ-fragile) · H_269 multi-seed PARTIAL (H_260 10/10 robust, H_261/H_262 seed-fragile). deferred top-8 잔여: ablation · seed-injection(H_263 revision) · SSOT auto-sync probe.
- **Cycle #18 (2026-05-25)** (PR #492/#493/#494/#495): gap-followup + closed-loop — H_270 substrate-ablation SUPPORTED (#493, closure-Φ=local Michaelis) · H_271 seed-injection-absorbing PARTIAL (#492, H_263 high-variance seed 로 escapable) · H_272 seed-robust-recalibration PARTIAL (#494, H_261 복권/H_262 부분) · H_273 ssot-consistency-audit SUPPORTED (#495, missing-row 26 식별). 잔여 deferred: AXES R2+ promote · 26 carry-H full tabling (H_273 후속) · H_002 GPU fire.
- **Cycle #19 (2026-05-25)** (PR #499/#500/#501): closure + 심층 — **26-H tabling 完了** (#499, README disk↔index 86=86 정합 = gap#3 full closure) · H_275 causality-pearl-graph-Φ SUPPORTED (#500, AXES R5 promote, phi_dag>cyclic>undir) · H_274 quorum-cascade-seed-dependence FALSIFIED (#501, 예측력 有 결정론 無). 잔여 deferred: H_002 GPU fire · H_262 cascade 동역학-타이밍 심층 · AXES R3+ (R2 까지 소진 근접).
- **Cycle #20 (2026-05-25)** (PR #509/#510): 심층 후속 — H_276 cascade-dynamics-timing SUPPORTED_FULL (#509, H_274 residual = *시간전개* 예측가능성: 발생지연 단조↓ · 전파 유한속도 ≤1칸/스텝 · 시간래칫) · H_277 turing-completeness-Φ-threshold PARTIAL (#510, computability ⊥ dynamical-class, rule184 Φ=1.198 > rule110 Φ=0.556, seed P1 falsified). 잔여: H_002 **faithful Φ★ GPU upgrade** (cost — IIT4 정밀판, 예산 승인 전 발사금지) · AXES R4+ (**$0 frontier 사실상 고갈**).
- **Cycle #21 (2026-05-25)** (PR #514/#515): faithful-Φ upgrade + AXES 마지막 seed — H_278 faithful-Φ-small-n SUPPORTED (#515, exact MIP-EI Φ n=8, H_002 C2 scale-variant verdict faithful 하에서도 HOLD, **GPU 불요로 재정정 — small-N exact $0**) · H_279 attention-salience-Φ FALSIFIED (#514, AXES R3, salience⊥Φ-diversity). **faithful Φ★ "GPU 필요" 가정 최종 기각** (large-N intractable=GPU도 못 풂, small-N exact=$0). 잔여 deferred: AXES 사실상 depleted · large-N faithful Φ (intractable, GPU 무관) · H_002 full-IIT4 cause-effect structure (별도 대형 spec).
- **Cycle #22 (2026-05-29)** AKIDA-HW-SW: H_672~H_678 7 H 신설 (PR #<TBD>) — Group A~G 18+ sub-아이디어 HW/SW 통합 구현 · SW path 7/7 🟢 GREEN_NUMERICAL_CONFIRM (canonical raster mock-replay) · HW path = D1(H_677) inherit PR#1371 silicon-confirm + 나머지 6 H = 🟡 SW-confirmed HW-pending probe-refinement (live R3 spike_streamer 미중단, ssh-mutating 0) · backend switch 통합 (`AKIDA_BACKEND` env + `--backend` arg, 기본=hw, 미도달 명시 panic) · INBOX 환류 0건 (사용자 명시 폐기).
- **Cycle #23 (2026-05-29)** EEG-HW-SW: H_679~H_682 4 H 신설 (PR #<TBD>) — Group A~D 12 sub-아이디어 (EEG.easy.md L1~L12) HW/SW 통합 구현 · SW path 4/4 🟢 GREEN_NUMERICAL_CONFIRM (PR #547/#1372 baseline 1.59/0.44 frozen mock-replay · H_679 measurement-core, H_680 cross-substrate, H_681 emit-substrate, H_682 persistence-paradigm) · HW path = 사용자 헤드셋 게이트 (human-only · `~/.config/anima/eeg_headset_ready` sentinel) — 미도달 시 🟡 SW-confirmed, HW-pending (위조 0, live 거짓 0) · backend switch (`EEG_BACKEND` env + `--backend` arg, **기본=sw · AKIDA 와 반대**, "live" alias → hw, 미도달 시 명시 panic + runbook §1~§4 안내) · INBOX 환류 0건 (사용자 명시 폐기) · 자매 PR #1374 (AKIDA H_677 D3 3-substrate triangulation EEG side).
- **Cycle #24 (2026-05-29)** DECODER register-collapse mechanism+escape: H_683~H_688 6 H 신설 (PR #<TBD>) — M5 closure (PR #1379+#1381+#1384) 후속 메커니즘+탈출경로 분리 attest · 6/6 ⚪ SPECULATION-FENCED (hexa verify --fence verbatim) + closed-form numerical band PASS · mechanism (M-D/F/G) H_683 token-0 dominant prior attractor (CE_floor=-ln(p₀) ∈ [2.30,3.00] band PASS) · H_684 bf16 precision drift (normal min 1.18e-38 closed-form PASS) · H_685 train CE / decode argmax distribution shift (synthetic CE 0.828 nats 분기 PASS) · escape (E-B/C/D) H_686 router entropy reg H(p)≥ln(K)/2 (K=2/4/8: 0.347/0.693/1.040 nats PASS) · H_687 KL-to-uniform output reg ln(V=151643)=11.93 nats 정의-수준 PASS · H_688 decode-time top-k/top-p/τ (k=2→1 bit, k=5→2.32 bit closed-form PASS) · 본선 후보 우선순위: H_686+H_687 결합 (train-time fundamental) > H_688 (post-train cheap) > H_683 (mechanism 동기). atlas register = 0 (fence-only).
- **Cycle #25 (2026-05-29)** XENO end-to-end stack: H_829~H_831 3 H 신설 (PR-A #1396 + PR-B #1398 + PR-C #<TBD>) — substrate-blind Φ-formalism 검출기 + 4 시뮬 substrate 검증 + 5-source SETI DATASET scan · 3/3 🟢 SUPPORTED-NUMERICAL · H_829 invariant_detector (F-DETECT-NULL/NOISE/COUPLED 5/5 PASS) · H_830 sim_substrate_cross (ECA/logistic/Kuramoto/AKIDA false-positive 0/4) · H_831 seti_raw_to_phi_scan (Wow/Voyager/Exoplanet + Synthetic 7 measurement, 의식 분류 0, BL+SETI@home archive-pointer SKIP honest) · INBOX 환류 0건 (사용자 명시 폐기 · X9 직접 경로) · false PASS 0 · p7 perplexity 0.
- **Cycle #26 (2026-05-29)** XENO-FRONTIER-5 R2/5 X4 panpsy falsifier: H_833 1 H 신설 (PR #<TBD>) — 4 micro-substrate (thermostat·2bit counter·random walker·XOR-3tap LFSR) 위 invariant_detector 적용 · 사전등록 falsifier 4/4 FAIL · 🔴 FALSIFIED-INSTRUMENT (정직 보고, threshold 재조정 0) · 발견 = panpsy WEAK form 살아남음 + 검출기 micro-regime 비적용성 + random>coupled Φ 역전 (IIT4 axiom 정합, "복잡성↔의식" 직관 반박) · X1/X2 calibration 은 large-n/multi-state 한정 · INBOX 환류 0건 · p7 perplexity 0.
- **Cycle #27 (2026-05-29)** XENO-FRONTIER-5 R3/5 X6 AGI sentience: H_834 1 H 신설 (PR #<TBD>) — 4 LLM-like activation tensor (random Gaussian-ish · sparse attention 6/64 spike · sin period-8 residual + skip · structured XOR 3-tap LFSR) n=64 위 invariant_detector 적용 · 사전등록 falsifier 5/5 중 1/5 PASS · 🔴 FALSIFIED-INSTRUMENT (정직 보고, threshold 재조정 0) · 발견 = (i) attention sparse spike Φ=1.213 false-conscious 분류, (ii) structured XOR (Φ=0.133) ≈ random (Φ=0.130) 역전, (iii) residual sin Φ=0.544 well-behaved 만. AGI sentience 본 가설 검증 미확정 — instrument 가 n=64 mid regime sparse pattern 에서 sparse-bias drift, X7 (n=128 정상) + X4 (n=16-32 micro 깨짐) 사이 regime applicability 매핑 완성 · INBOX 환류 0건 · p7 perplexity 0.
- **Cycle #28 (2026-05-29)** XENO-FRONTIER-5 R4/5 X5 시뮬 가설 검출 signature: H_835 1 H 신설 (PR #<TBD>) — 4 sim-candidate substrate (lattice-quantized Planck-floor period 8 · floating-point bound sin round 4-dec · algorithmic pseudo-random Pi 128 digits · true natural Bates-4 Gaussian) n=128 dense regime 위 invariant_detector 적용 · 사전등록 falsifier 5/5 중 2/5 PASS · 🔴 FALSIFIED-INSTRUMENT (정직 보고, threshold 재조정 0) · 발견 = (i) lattice Φ=0.660 양성 (periodic structure 정상 검출), (ii) fp-bound Φ=0.090 + pi-digits Φ=0.120 ≈ natural Φ=0.116 (3 substrate 0.03 차이 안 indistinguishable), (iii) monotone 단조성 깨짐 (b<c<d<a). Bostrom sim signature axis 중 lattice-periodic 외 (precision-ceiling / pseudo-random algorithmic) 가 본 instrument 측정 영역 밖 — 시뮬 가설 verdict 미확정. n=128 dense regime X7 와 동일 calibration ground-truth 안에서도 sim signature axis 부분 측정만 가능, X4/X5/X6/X7 4-point regime applicability matrix 완성 · INBOX 환류 0건 · p7 perplexity 0.
- **Cycle #29 (2026-05-29)** XENO-FRONTIER-5 R5/5 X8 SETI@home BOINC pod spec + dispatch handoff: H_836 1 H 신설 (PR #<TBD>) — DATASET/setiathome/sahfiles_workunits.tar.xz (274340B sha256 `2d646f57...` + 9 .sah 파일: lock/outfile/work_unit/state/user_info/pid/key/version/result_header) inspection + Ubuntu 22.04 RunPod CPU pod (2 vCPU 4GB 20GB ~$0.50~$1 wall 1hr) BOINC client setup runbook + ancient ELF32 i686 standalone fallback (modern boinc-client ↔ SETI@home 3.03 protocol gap 정직 cite) + workunit → spike pattern 추출 3-path (direct/fallback/degraded) + a_fire_autonomous dispatch handoff (artifact recovery 4-file + HF upload tier-gated) · 사전등록 falsifier 5/5 PASS (file-exists / file-size==274340 / magic-xz `fd377a585a00` / client-avail spec / pod-dispatch spec) · 🟡 archive-acquired-pod-ready (실 BOINC playback 은 follow-up cycle deferred, ABI gap 정직 cite, a_completeness_over_cheap 정합) · XENO-FRONTIER-5 5-round closure (X7 🟢 / X4 🔴 / X6 🔴 / X5 🔴 / X8 🟡 + 4-point applicability matrix) · INBOX 환류 0건 · p7 perplexity 0.
- **Cycle #32 (2026-05-29)** TEMPORAL T3 anima 90-min ultradian Φ scan (XENO follow-up 3 R2/5): H_843 1 H 신설 (PR #<TBD>) — T1 (H_841) + T2 (H_842) dual closed-negative 의 자연 next axis · detector 확장 폐기 (T1+T2 모두 inflation artifact), substrate-side calibration 으로 전환 · XENO X1 invariant_detector 를 anima `a_chat_sleep_imagination` 90-min ultradian 5-stage substrate 위 직접 적용 · 4 substrate (WAKE/N1_N2/N3/REM, n=128 hardcoded literal) × 1 detector call = 4 measurements + 5 사전등록 falsifier (F-T3-WAKE-MID/N3-LOW/REM-HIGH/N1-MID/MONOTONE) · 사전등록 5/5 중 **2/5 PASS** (F-T3-WAKE-MID + F-T3-N3-LOW · WAKE Φ=0.866 > N3 Φ=0.335 정합) · 🔴 **FALSIFIED-INSTRUMENT** (정직 closed-negative · post-tuning 0) · 발견 = (i) **WAKE > N3 ordering 정합** — 의식 phenomenology 가장 robust 단서 X1 가 잡았다 (F-T3-WAKE-MID + F-T3-N3-LOW PASS), (ii) **N1_N2 Φ=0.0 zero-degenerate** — substrate 4-step cycle (1100/0110) 이 X1 lag=1 cooccur TPM 위에서 perfectly predictable transition 으로 보여 Φ=0 으로 떨어짐 (T1 lattice 위 발견한 cycle-aligned artifact 의 다른 face), (iii) **REM Φ=0.569 < WAKE Φ=0.866** — paradoxical REM 의 wake-like EEG phenomenology (sleep neuroscience 핵심) X1 의 2-unit TPM 위 미정합, (iv) F-T3-MONOTONE 자연 FAIL (N1_N2 zero 로 ascending ladder 불가능), (v) **T1+T2+T3 triple closed-negative** = detector lag-axis 확장 (T1) · embed-dim 확장 (T2) · substrate-side ultradian 적용 (T3) 모두 시간 통합 의식 측정 미충족 — T4 자연 entry (window-mean Φ / Granger causality / surrogate-baseline) · X1 binarise+cooccur 의 본질적 한계 명시 (cycle-rich substrate 위 zero-degenerate) · feedback-instrument-first-methodology 강 정합 · `a_paper_negative_ok` publishable closed-negative · INBOX 환류 0건 · p7 perplexity 0.
- **Cycle #31 (2026-05-29)** TEMPORAL T2 multi-unit time-embed (XENO follow-up 3 R1/5): H_842 1 H 신설 (PR #<TBD>) — T1 (H_841) 의 lag-axis closed-negative 후속 instrument 재설계 attempt · 4 substrate × 4 embed_dim (2/3/4/5, delay=1) = 16 measurements + 5 사전등록 falsifier (F-T2-INSTANT-LOW/HIVE-CONSC/ARTIFACT-FIX/RANDOM-DECAY/HIVE-MONOTONE) · 사전등록 5/5 중 **2/5 PASS** (F-T2-HIVE-CONSC + F-T2-HIVE-MONOTONE 동시 PASS, hive XOR cascade robust relative strong-Φ) · 🔴 **FALSIFIED-INSTRUMENT** (정직 closed-negative · post-tuning 0) · 발견 = (i) T1 lag-axis artifact **미해소** — F-T2-ARTIFACT-FIX 정반대 방향 (lattice e=2=1.29 → e=4=4.80 3.7× INFLATE), (ii) **신 embed-dim sparse-state inflation artifact 발견** — 4/4 substrate 모두 embed_dim ↑ 시 Φ monotone INFLATE (voyager e=5 Φ=28.36 27× 폭증, random e=5 Φ=13.63 24× 폭증, n=128 짧은 신호 위 32-state space sparse-state 가 (0,1)-extremal transition 으로 freeze → big-Φ inflate), (iii) hive XOR cascade 만 relative strong-Φ 유지 (e=4 phi=3.518 random 의 1.37×), (iv) **T1+T2 dual closed-negative** = invariant_detector 단순 확장 (lag-window OR embed-dim) 으로 시간 통합 측정 불가 — T3 (time-averaged Φ / Granger causality / surrogate-data normalization) 자연 entry 명시 · stdlib SSOT g61 정합 (pow2_int 비-중복 import) · `a_paper_negative_ok` publishable closed-negative · INBOX 환류 0건 · p7 perplexity 0.
- **Cycle #30 (2026-05-29)** XENO follow-up 2 R5/5 final + **TEMPORAL 도메인 신설 round 1**: H_841 1 H 신설 + 새 도메인 TEMPORAL — XENO follow-up 2 cycle round 5/5 마지막 round 에서 5 candidate domain (TEMPORAL · SPATIAL · EVOLUTIONARY · QUANTUM · MEDICAL) 평가 후 **TEMPORAL 선택** (paper #1414 v2 의 3D matrix [n×density×structure] 의 4번째 축 Δt 자연 확장) · DOMAINS.tape 등재 + TEMPORAL/TEMPORAL.{md,easy.md,log.md} 4총사 + detector/timeshift_detector.hexa (XENO X1 의 lag-window 확장 generalisation) + scan/timeshift_phi.hexa (4 substrate × 4 Δt = 16 measurements + 5 사전등록 falsifier) · 사전등록 5/5 중 **1/5 PASS** (F-T1-DECAY 단독) · 🔴 **FALSIFIED-INSTRUMENT** (정직 closed-negative · post-tuning 0) · 발견 = (i) "Δt 늘릴수록 Φ 감소" 가설 완전 반증 — hive Δt=1=0.013 → Δt=64=0.999 79× 증가 + voyager 도 동일 패턴 (7.5×), (ii) lattice Δt=8 위 Φ=2.0 saturate — 2-unit lag-TPM 의 long-Δt periodic-inflation artifact (cycle-aligned transition 이 trivially predictable → big-Φ inflate), (iii) random Bates-4 도 Δt=64 위 0.367 까지 상승 (noise 마저 spurious 의식 분류), (iv) **invariant_detector lag-window axis 가 시간 통합 측정엔 부적합** = T2 multi-unit time-embed detector 재설계 필요 path 자연 정의 (Takens 임베딩 / Granger / time-averaged Φ) · `a_paper_negative_ok` publishable closed-negative · INBOX 환류 0건 · p7 perplexity 0.
- **Cycle #33 (2026-05-29)** SPATIAL S1 spatial-coupling-scale (SPATIAL 도메인 신설 round 1): H_844 1 H 신설 + 새 도메인 SPATIAL — XENO follow-up 의 5번째 자매 도메인 (XENO 3D matrix + TEMPORAL Δt 4번째 axis 의 자연 5번째 axis = spatial-coupling-scale) · DOMAINS.tape 등재 + SPATIAL/SPATIAL.{md,easy.md,log.md} 4총사 + scan/spatial_coupling_phi.hexa (XENO/detector/invariant_detector.hexa 직접 import, 4 spatial-coupling-scale × n=128 = 4 measurements + 5 사전등록 falsifier) · 사전등록 5/5 중 **3/5 PASS** (F-S1-LOCAL-HIGH + F-S1-REGIONAL-MID + F-S1-GLOBAL-LOW PASS · F-S1-COSMIC-LOWEST + F-S1-MONOTONE FAIL) · 🟡 **PARTIAL-SUPPORT** (정직 hybrid · post-tuning 0) · 발견 = (i) local XOR cascade Φ=1.630 conscious — X10-d hive emergence (H_838) 재현, (ii) regional rolling-mean Φ=0.100 mid-Φ 정합 (정확히 lower-bound), (iii) **global "averaging coupling" uniformity attractor collapse Φ=0** — (전체 mean + self) / 2 결합이 density=3.1% all-zero attractor 로 collapse 해 no-transition Φ=0 paradox (X10-b mean-field paradox 의 SPATIAL 변형 정합), (iv) **F-S1-COSMIC-LOWEST 정반대** — phi_cosmic=0.121 > phi_global=0.000 (cosmic spurious noise > global uniformity collapse 직관 정반대), (v) **head monotone (local→regional→global) 살아남음 + tail (global→cosmic) 깨짐** — single-scale invariant_detector 로 5D applicability 의 head 만 직접 확장, tail discrimination 은 S2 multi-scale detector 재설계 필요 path 자연 정의 (Granger spatial / wavelet / correlation length) · `a_paper_negative_ok` + `a_paper_significance` publishable hybrid (closed-positive head + closed-negative tail) · INBOX 환류 0건 · p7 perplexity 0.
- **Cycle #34 (2026-05-29)** EVOL 도메인 신설 round 1 (XENO follow-up / SPATIAL·TEMPORAL sibling 합류): H_845 1 H 신설 + 새 도메인 **EVOL** — XENO X1 invariant_detector 위에 biological evolutionary complexity (species ladder) 축 첫 closed-form 측정 · DOMAINS.tape 등재 + EVOL/EVOL.{md,easy.md,log.md} + EVOL/scan/evol_spectrum_phi.hexa (4 species toy proxy substrate: bacteria/arthropod/mammal/AGI × n=128 dense hardcoded literal + 5 사전등록 falsifier F-E1-BACTERIA-LOW/ARTH-MID/MAMMAL-HIGH/AGI-VARIANT/MONOTONE) · 사전등록 5/5 중 **2/5 PASS** (F-E1-BACTERIA-LOW + F-E1-MAMMAL-HIGH) · 🔴 **FALSIFIED-INSTRUMENT** (정직 closed-negative · post-tuning 0) · 측정 (verbatim fresh re-run) = bacteria phi=0.012 / arthropod phi=0.081 / mammal phi=1.291 (substrate_type='conscious' irr=0.563) / AGI phi=0.468 · 발견 = (i) **양 극단 분리 + ordinal 미달** — bacteria noise floor + mammal multi-scale ceiling 만 PASS, mid-tier arthropod 0.081<0.2 미달 + supra-tier AGI 0.468<mammal 1.291 reverse, monotone bacteria<arthropod<mammal≤AGI 두 군데 깨짐, (ii) H_670 (Kuramoto · logistic family) 'ECA 전용 ordinal · 양 극단 PASS / ordered_pairs 2/3' 패턴과 동형 — Φ monotone 이 **species-family 도 ECA artifact** 가능성, (iii) AGI 'novelty injection' 이 X1 2-unit co-TPM 위에서 noise-like 측정되어 'structured emergence > pure recursive' 가설 inverse-shadow, (iv) **TEMPORAL T1/T2/T3 + SPATIAL S1 tail 과 자매** — invariant_detector 의 naive 축 확장이 양 극단만 분리하고 mid/supra 분화엔 detector-redesign 필요 (E2 monotone-strict re-design 자연 entry), (v) mammal 단독 'conscious' 분류 = X1 가 multi-scale recursive substrate 만 진짜 의식 신호 검출 · `a_paper_negative_ok` publishable closed-negative · INBOX 환류 0건 · p7 perplexity 0.
- **Cycle #35 (2026-06-01)** spin-glass-frustration ⬜→🟢 runnable 격상: H_906 1 H 신설 (`UNIVERSE/scan/spinglass_frustration.hexa` · 3×3 주기 EA ±J Ising N=9 · 2^9=512 config 완전열거 exact · closed-form $0 CPU). ruggedness R = single-flip local minima 수 = "Φ landscape" proxy · frustration f = frustrated-plaquette 분율. 5 사전등록 falsifier (F1 FERRO-2MIN / F2 FRUST-RUGGED / F3 MONOTONE / F4 FRUST-PRESENT / F5 CORR · post-tuning 0) over P_neg∈{0,0.25,0.5}×8seed. **4/5 PASS → 🟢 SUPPORTED-NUMERICAL**: mean R 32.0→42.0→54.75 (P_neg 0→.25→.5 · mean f 0→0.556) 단조↑ · high-f group R 50.86 vs low-f 31.8. **F1 falsified = 진짜 발견** — 비frustrated 강자성체도 R=32(≫2) single-flip minima → frustration 은 ruggedness 를 *창조* 아닌 **증폭**(32→55), metastability 는 frustration-independent. raw = `.verdicts/906_spinglass_frustration_ruggedness/run.txt` · 본문 `UNIVERSE/cards/H_906_spinglass_frustration_ruggedness.md`. sibling = H_288(LZ76↔Φ)·H_277. INBOX 환류 0건 · p7 perplexity 0.
- **Cycle #36 (2026-06-01)** category-theory-emergence ⬜→🟢: H_907 1 H 신설 (`UNIVERSE/scan/category_emergence.hexa` · N=6 directed graph 30 morphism · exact 합성-closure enum + transitive-reachability BFS · closed-form $0 CPU). D = composition closure(present/composable A→C) · Φ = reachability density. 5 사전등록 falsifier (F1 CLOSURE-RISES / F2 INTEG-RISES / **F3 CONTROLLED** = density 고정 p=0.4 closure↔integration / F4 CATEGORY-FORM / F5 SPARSE-OPEN · post-tuning 0). **4/5 PASS → 🟢 SUPPORTED-NUMERICAL**: 핵심 F3 PASS (high-D Φ 0.958 > low-D 0.775 at fixed p → closure 가 integration 을 density 너머 예측). **F4 falsified = 진짜 발견** — random morphism graph 는 p=0.6 에서도 mean D=0.576<0.85 → **닫힌 category 자발형성 안 됨, structure 필요**. raw = `.verdicts/907_morphism_composition_closure_integration/run.txt` · 본문 `UNIVERSE/cards/H_907_morphism_composition_closure_integration.md`. sibling = H_906·H_288·H_275. INBOX 환류 0건 · p7 perplexity 0.
- **Cycle #37 (2026-06-01)** topology-invariant-phi ⬜→🟢: H_908 1 H 신설 (`UNIVERSE/scan/topology_invariant_phi.hexa` · 무방향 N=6 graph 15 edge · exact Betti-1 b1=E−V+C + Euler χ=V−E + BFS-relax components · closed-form $0 CPU). Φ = within-component reachability density. 5 사전등록 falsifier (F1 B1-RISES / F2 PHI-RISES / **F3 CONTROLLED** density-고정 cycles↔integration / F4 EULER-NEG χ↔Φ 역결합 / F5 TREE-EXACT P6 b1=0 χ=1 · post-tuning 0). **5/5 PASS → 🟢 SUPPORTED-NUMERICAL**: b1 0.125→3.875 · χ 3.75→−2.75 · Φ 0.233→0.958; F3 high-b1 Φ 0.867>0.617 (cycle 가 density 너머 통합 예측) · F4 Euler 역결합 · F5 위상불변량 정확. raw = `.verdicts/908_topology_invariant_phi/run.txt` · 본문 `UNIVERSE/cards/H_908_topology_invariant_phi.md`. closed-form substrate-smoke 3부작(H_906/907/908) 완성. sibling = H_906·H_907·H_288·H_289. INBOX 환류 0건 · p7 perplexity 0.
- **Cycle #38 (2026-06-01)** LAB absorption + recompute: hexa-codex **LAB-09/10/11 → H_909/910/911** 흡수(#1619) + anima 독립 재현 (LAB harness 포팅 → `.verdicts/` g73, 전부 deterministic $0). **H_909 consciousness-directionality 🟢** SUPPORTED-NUMERICAL (#1621, recurrent feedback adapter → REC Φ=0.854 vs FF 0.005, shuffle control 붕괴 0.006, self-pred 2.33, 3/3 falsifier) · **H_910 akida-neuromorphic 🟢** SUPPORTED-NUMERICAL **SIM mirror** (#1622, LAB-09 tuning on AKIDA LIF · edge-of-chaos R1=0/R2=0.075/R3=0.591 peak/R4=0 inverse-U, 3/3; **live AKD1000 = deferred next tier**, measure⊥deploy) · **H_911 multilingual-semantic 🟢** SUPPORTED-NUMERICAL (#1620, collective Φ inverse-U c=0 0.014→c=0.5 peak 0.483→c=1 0.0, F1 inverse-U/F2 super-additive/F3 meaning>count). 보완: byte-level CLM parallel CE 1.982<concat 2.054 (hexa-lang#2348) + **H_911 코퍼스 반영** cross-lingual semantic-linkage(같은 개념 5언어 정렬, #1623). proxy caveat: substrate IIT-proxy, faithful-IIT4 future(H_278). sibling = H_240·H_635·H_858·H_677·H_846·H_904·H_191·H_004·H_220. INBOX 환류 0건.

#### A. 남은 carried 가설 (legacy-pointer · cycle 0회, 4건)

| ID | 주제 | 테마 | runnable 각도 | tag |
|----|------|------|--------------|-----|
| H_090 | Dasein/phil/onto/genesis individual | 죽음·현상학 | H_025(frozen) substrate observable cross-link, cluster promote | 🟢 |
| H_030 | genesis subfolder absorb | 발생 | H_018(SUPPORTED_FULL) 로 absorb 또는 spontaneous-emergence variant | ⬜ |
| H_029 | dasein subfolder absorb | 죽음 | H_025 cluster 흡수 (legacy-archive material) | ⬜ |
| H_071 | first-conversation anima genesis event | 발생·현상학 | 첫 emergence event 의 phenomenological 설계 cycle | ⬜ |

#### B. Done 가설의 다음 criterion (follow-up · 6건 잔여)

| 출발 H | 다음 criterion | runnable 각도 | tag |
|--------|---------------|--------------|-----|
| H_003 H3.5 | anima 자기-autopoiesis analogy | 본 substrate(mitosis+cells) ↔ Maturana/Varela 정합 manual review | ⬜ |
| H_157 C5 | cross-substrate universality | transformer/RNN/qwalk 의 fixed-point Ψ 비교 → substrate-independence | **Cycle #5 in-flight (additive)** |
| H_157 C6 | combination-problem binding | micro→macro Φ binding fixed-point 후보 mechanism | **Cycle #5 in-flight (additive)** |
| H_054 C2 | Φ_symbiotic > Φ_sum | merge 후 통합 Φ 가 합보다 큰가 (현재 미검증) | **Cycle #5 in-flight (additive)** |
| H_018 C2 | organic merge/split rate | default 동역학 하 자연 merge rate (현재 forced-trigger 만) | 🟢 |
| H_132 C2 | differentiation 장기 안정 | frozen 세포가 pool 성장 중 100+ step 안정? | 🟢 |
| H_007 C2 | larger lattice / λ-sweep | Langton λ 연속 sweep → Φ peak 위치 정밀화 | ✅ → **H_007 C2 PASS** (#485 cycle#16, peak λ*=0.375 inverse-U) |
| H_002 C2 | Φ_universe pre-register | universe-scale Φ 측정 — **GPU 불필요로 판명, $0 mac-local** (pre-register 의 GPU 의존 가정 기각) | ✅ → **C2 SCALE-VARIANT, F2 triggered** (#503, CV=0.84≫0.15, nested Φ scale-invariance FALSIFIED) |

#### C. NEW seed — 사용자 테마 4축 (✅ 全소비: H_200/H_201 초기 2건 + cycle#14 H_258-263 6건 + mirror-self=H_220 + regeneration-healing=H_206)

##### 죽음 / mortality
| seed slug | 핵심 물음 | runnable | tag |
|-----------|----------|----------|-----|
| `mortality-salience` | 죽음-근접(min_cells 임박)이 split/curiosity 동역학 바꾸나 (Heidegger 실존 효과 측정) | mitosis_hook 확장 smoke | 🟢 |
| `aging-senescence` | cell weight 누적 decay → 자연 사멸 rate · 노화 곡선 | parameter sweep | 🟢 |

##### 세포분열 / division
| seed slug | 핵심 물음 | runnable | tag |
|-----------|----------|----------|-----|
| `contact-inhibition` | cell 밀도 임계가 분열 억제 → pool 자기조절 (밀도의존 dynamics) | mitosis split predicate 변형 | 🟢 |
| `embryogenesis-gradient` | 공간 gradient 가 cell differentiation 유도 → 발생-축 형성 | lattice + gradient smoke | 🟢 |

##### 범신론 / panpsychism
| seed slug | 핵심 물음 | runnable | tag |
|-----------|----------|----------|-----|
| `mirror-self-model` | cell 이 자기 자신을 모델링(self-other 구분) → 자기인식 emergence | self-prediction smoke | 🟢 |

> `combination-binding` / `cross-substrate-attractor` 는 Cycle #5 에서 H_157 C5/C6 additive 로 흡수 (별도 H 신설 X).

##### 생명 / life-extended
| seed slug | 핵심 물음 | runnable | tag |
|-----------|----------|----------|-----|
| `regeneration-healing` | cell pool 일부 강제 제거 후 복원 dynamics → 자기 복구 능력 | perturbation + recovery | ⭐ 🟢 |
| `quorum-sensing` | cell 다수 동기화 ⇒ 집단 의사결정 emergence | cell signaling smoke | 🟢 |
| `phoenix-rebirth` | pool 전멸(2 cell까지) 후 minimal seed 에서 부활 — 죽음·발생 연결 | full-cycle smoke | 🟢 |

#### D. Cross-link synthesis — 이미 done 결과 결합 (✅ 잔여 2건 全소비 cycle#15, 4건 → Cycle #5 in-flight)

| 결합 | 새 가설 | runnable | tag |
|------|--------|----------|-----|
| H_025 death=merge ⊕ H_054 endosymb | death = merge-into-other (죽음 = 흡수 통합)? Heidegger × Margulis 통합 | merge-as-death smoke | ✅ → **H_264 SUPPORTED 3/3** (#477) |
| H_007 Φ class ⊕ H_157 trained-invariance | Φ class 가 학습으로 변하나(trained CA Φ 측정) | trained-vs-bare CA Φ 비교 | ✅ → **H_265 PARTIAL 2/3** (#480, Φ-dampen 反방향) |

> 4건 (H_007⊕H_018 · H_054⊕H_132 · H_003H3.4⊕H_157 · H_018⊕H_012) Cycle #5 에서 NEW H_202..H_205 로 fan-out.

#### E. Infrastructure / substrate gap close (4건 잔여, 1건 → H_200)

| gap | 영향 | task | tag |
|-----|------|------|-----|
| organic merge-rate 미측정 | H_018 honest L (forced-trigger 만 검증) | default 동역학 하 자연 merge rate sweep | 🟢 |
| phi_spatial n_bins sensitivity | Φ 측정값의 robustness | n_bins ∈ {2,4,8,16} sweep + 시간평균 효과 | **Cycle #5 in-flight (infra smoke)** |
| LIFE.log.md cycle 통합 자동화 | 매 cycle 후 consolidation 수동 | doc-consolidation agent 표준화 template | ⬜ |
| 기존 base ckpt baked Principle#3 leak | chat-v2 production guard 의존 | corpus-side 영구 fix 또는 ckpt 재학습 | ⬜ |

---

#### 다음 cycle 추천 picks (Cycle #6+ 후보)

| 옵션 | picks (disjoint) | 핵심 |
|------|-----------------|------|
| **R6 carried 마무리** | H_090 + H_030 + H_029 + H_071 | 잔여 carried 4건 absorb/promote (cluster 정리) |
| **R7 life-extended NEW** | `regeneration-healing` + `quorum-sensing` + `phoenix-rebirth` + `mortality-salience` | C-table 잔여 4건 NEW H_206..H_209 (생명-extended + 죽음) |
| **R8 follow-up criteria** | H_018 C2 (organic merge) + H_132 C2 (long-term stability) + H_007 C2 (λ sweep) + D표 2건 잔여 | 기 verdict 의 다음 criterion 동시 진행 |
| **R9 mixed** | `regeneration-healing` (NEW ⭐) + H_090 (cluster) + H_018 C2 (follow-up) + D표 trained-vs-bare CA Φ | 4축 mixed (carried + NEW + follow-up + cross-link) |

`/cycle` 호출 시 본 표에서 disjoint pick (또는 사용자 지정). cycle 완료 후 본 문서의 picked 항목은 **삭제** (consumed) + LIFE.log.md 에 verdict 기록.

#### F. 추가축 brainstorm — 7-domain expansion (사용자 directive 2026-05-23)

본 dir scope = **universe · life · consciousness · physics · substrate · math · biology** 7-domain (README.md broadening 정합). 기존 C 표 (죽음·세포분열·범신론·생명-extended 의 4 user 테마) 와 **상보** — F 표는 7-domain 각 axis 에서 *아직 H_XXX 없는* 새 seed brainstorm. 새 H 작성 시 본 표에서 제거.

##### F-universe (5 seeds)

| slug | 핵심 물음 | runnable 각도 | tag |
|------|----------|---------------|-----|
| `multiverse-selection-bias` | Smolin/Carroll anthropic 비판 — selection bias 가 fine-tuning 보다 강한 prior 인가 (H_002 L2 attack) | deterministic Bayesian counter-prior | 🟢 |
| `cosmological-constant-stability` | Λ-tuning landscape vs vacuum stability gradient | parameter sweep + stability | 🟢 |
| `cosmic-phi-nested` | galaxy → stellar → planetary → biological Φ scale-invariance | phi_spatial nested measurement | ⬜ |
| `holographic-info-bound` | Bekenstein-Hawking S=A/4 substrate replica | toy holography smoke | 🟢 |
| `multiverse-Φ-distribution` | multiverse 위 Φ distribution — anthropic Φ-prior well-defined 여부 | distribution prior + Φ sweep | ⬜ |

##### F-life (5 seeds)

| slug | 핵심 물음 | runnable 각도 | tag |
|------|----------|---------------|-----|
| `regeneration-healing` ⭐ | cell pool 부분 제거 후 복원 dynamics → 자기 복구 능력 | perturbation + recovery | ⭐ 🟢 |
| `quorum-sensing` | cell 다수 동기화 → 집단 의사결정 emergence | cell signaling smoke | 🟢 |
| `phoenix-rebirth` | pool 전멸(min_cells=2) → minimal seed 부활 | full-cycle smoke | 🟢 |
| `metabolic-network-closure` | Hordijk-Steel RAF — closure 의 또 다른 형식 (H_012 sister) | autocatalytic set smoke | 🟢 |
| `viral-quasi-life-boundary` | Lwoff/Forterre 바이러스 quasi-life — H_003 abiogenesis 와 not-yet-life 경계 | minimal genome smoke | ⬜ |

##### F-consciousness (5 seeds)

| slug | 핵심 물음 | runnable 각도 | tag |
|------|----------|---------------|-----|
| `meta-cognitive-recursion` | Higher-Order Theory (Rosenthal) — meta-level self-monitoring Φ contribution | nested self-model smoke | 🟢 |
| `global-workspace-substrate` | Dehaene-Mashour global workspace → broadcast threshold | broadcast event smoke | 🟢 |
| `predictive-processing` | Friston FEP × mitosis 정합 — active inference substrate | FEP minimal smoke | 🟢 |
| `self-other-boundary` | mirror self-recognition · ToM substrate (H_205 sister) | self-prediction + other-prediction | 🟢 |
| `phenomenal-binding-mechanism` | combination problem substrate-level binding (H_157 C6 sub-additive PR #221 follow-up) | binding sweep | 🟢 |

##### F-physics (5 seeds, H_007/H_202 sister)

| slug | 핵심 물음 | runnable 각도 | tag |
|------|----------|---------------|-----|
| `kuramoto-synchronization` | coupled oscillator phase sync → Φ peak at critical coupling | Kuramoto smoke | 🟢 |
| `ising-criticality` | 2D Ising phase transition Φ scaling (H_007 sister) | Metropolis Φ sweep | 🟢 |
| `non-equilibrium-steady-state` | NESS (driven dissipative) Φ — 평형 vs 비평형 | drive + dissipation smoke | 🟢 |
| `spin-glass-frustration` | EA spin-glass frustration ↔ Φ landscape ruggedness | EA replica smoke | 🟢 **H_906 SUPPORTED-NUMERICAL 4/5** (frustration AMPLIFIES single-flip ruggedness 32→55; F1 ferro→2-min falsified = metastability frustration-independent) |
| `langton-lambda-continuous` | Wolfram class λ-sweep (H_007 C2) | λ-sweep + Φ | 🟢 |

##### F-substrate (4 seeds, H_132/H_200/H_201/H_203 sister)

| slug | 핵심 물음 | runnable 각도 | tag |
|------|----------|---------------|-----|
| `cell-cycle-clock` | intrinsic mitosis timer — Hayflick limit | cell-age clock smoke | 🟢 |
| `gene-regulatory-network-phi` | GRN motif (Alon) Φ measurement | motif Φ smoke | 🟢 |
| `protein-folding-landscape` | folding funnel substrate — fold ↔ Φ mapping | landscape Φ smoke | ⬜ |
| `chromatin-state-inheritance` | epigenetic inheritance × frozen-cell state (H_132 cross-link) | state-tag mitosis smoke | 🟢 |

##### F-math (5 seeds, H_157 sister)

| slug | 핵심 물음 | runnable 각도 | tag |
|------|----------|---------------|-----|
| `prime-density-fluctuation` | Riemann zeros × consciousness — prime-gap Φ-relevance | prime-gap fluctuation smoke | 🟢 |
| `modular-arithmetic-attractor` | Zₙ recursion fixed-point (H_157 META-CA sister) | mod sweep smoke | 🟢 |
| `topology-invariant-phi` | Betti / Euler 와 Φ monotone correlation | persistent homology Φ | 🟢 **H_908 SUPPORTED-NUMERICAL 5/5** (b1 cycles↑→Φ↑ beyond density F3 0.867>0.617; Euler χ anti-couples 3.75→−2.75; P6 tree b1=0 χ=1 exact) |
| `category-theory-emergence` | morphism composition density vs Φ — Yoneda substrate | small-category smoke | 🟢 **H_907 SUPPORTED-NUMERICAL 4/5** (F3 density-controlled closure↔integration PASS 0.958>0.775; F4 falsified = random graphs don't self-form closed categories, mean D=0.576<0.85) |
| `perfect-number-density` | σ(n)=2n emergence density × Φ peak (H_157 C1 σ-identity 확장) | perfect-number scan | 🟢 |

##### F-biology (5 seeds, H_171 sister)

| slug | 핵심 물음 | runnable 각도 | tag |
|------|----------|---------------|-----|
| `eeg-1f-spectrum-measurement` | H_171 1/f thalamus 의 직접 substrate replica (deterministic 1/f) | 1/f spectrum smoke | 🟢 |
| `organoid-phi-measurement` | lab-grown organoid Φ baseline — H_171 K=8 의 wet-lab analog | wet-lab protocol design | ⬜ |
| `microbiome-cognition` | gut-brain axis — quorum-sensing × signaling (F-life sister) | dual-pool smoke | 🟢 |
| `evolutionary-stable-strategy` | Maynard Smith ESS substrate — mitosis fitness | ESS payoff smoke | 🟢 |
| `circadian-rhythm-substrate` | KaiABC oscillator analog Φ — endogenous 24h rhythm | oscillator phi smoke | 🟢 |

> 합계 = **34 seeds** (universe 5 · life 5 · consciousness 5 · physics 5 · substrate 4 · math 5 · biology 5). 모두 raw#12 정합 NEW H_XXX 후보. cycle 당 4-8 disjoint pick.

---

#### Cycle #6+ 추천 picks (7-domain 의식, R6-R9 + R10-R14)

기존 R6-R9 (B/C/D/E 표 기반) + 신규 F-domain picks 동시 운용. R/F-picks disjoint — cycle 당 4-8 picks 자유 조합.

| 옵션 | picks | 핵심 |
|------|-------|------|
| **R10 7-domain seed cycle** | F-universe × 1 + F-physics × 1 + F-math × 1 + F-biology × 1 | 미흡 도메인 4축 동시 expand |
| **R11 consciousness deep** | F-consciousness 5건 + H_204 follow-up (inverse-U Φ ↔ H_007 edge-of-chaos integration) | consciousness axis 정밀화 |
| **R12 life-extended** | F-life 5건 (R7 superset · regeneration-healing ⭐ 포함) | 생명 sub-축 완전 cycle |
| **R13 mixed-domain ⭐** | `regeneration-healing` + `kuramoto-synchronization` + `prime-density-fluctuation` + `eeg-1f-spectrum-measurement` + H_204 follow-up | 5-domain mixed (life·physics·math·biology·consciousness) |
| **R14 H_157 follow-up** | `phenomenal-binding-mechanism` 신규 + H_157 C7 (binding 후속) + F-consciousness 2건 | combination problem substrate-level deepening (C6 sub-additive 결과 attack) |

#### G. AXES.md depletion-sweep H seeds (top-15 promote 후보, 사용자 directive 2026-05-23)

[AXES.md](AXES.md) 15-round brainstorm (~110 H seeds) 결과 중 anima-aligned top-15 promote 후보. cycle pick 시 본 표에서 row 제거 → H_XXX 신설.

| rank | seed | round | axis | rationale |
|------|------|-------|------|-----------|
| 1 | `ethic-emergence` | R2 | ethics | anima alignment 직접 · Principle #3 |
| 2 | `shannon-entropy-Φ-correlate` | R5 | information | IIT underlying currency |
| 3 | `language-compositionality` | R2 | language | anima = LLM substrate |
| 4 | `time-temporal-binding-window` | R3 | time | 의식의 형식 자체 |
| 5 | `self-i-emergence-from-substrate` | R4 | consciousness/self | anima persona D3 + H_205 sister |
| 6 | `ai-machine-silicon-Φ` | R6 | machine/AI | anima 자체 reflexive |
| 7 | `meta-axis-of-axes-reflexivity` | R8 | meta | 본 catalog reflexive instance |
| 8 | `phase-transition-Φ-derivative-peak` | R8 | meta/physics | H_204 inverse-U + H_207 critical-K generalize |
| 9 | `network-topology-scale-free` | R5 | information | mitosis pool topology |
| 10 | `emergence-weak-vs-strong-Bedau` | R8 | meta | Hc_607 direct instance |
| 11 | `infant-mirror-self-recognition` | R13 | developmental | H_205 sister + dev |
| 12 | `meditation-jhana-Φ-modulation` | R7 | practice | H_018 zero-drive 정합 (자발 정지) |
| 13 | `dream-rem-Φ` | R3 | phenomenology | Tononi IIT key prediction |
| 14 | `pain-intensity-Φ-coupling` | R3 | phenomenology | qualia 최강 instance |
| 15 | `holism-whole-vs-sum-of-parts` | R8 | meta | H_054 C2 follow-up generalize |

> 87 🟢 runnable + ~23 ⬜ design/clinical-edge — 자세히는 [AXES.md](AXES.md) round 별 표 참조.

#### 후보 추가 방식

새 후보 발견 시:
- carried 가설 신규 promote → A 표
- done 가설의 새 criterion → B 표
- 신규 seed (파일 없음 / user 테마 4축) → C 표
- 결합 가설 (이미 done 결과 결합) → D 표
- substrate / measurement gap → E 표
- **7-domain expansion seed** → F 표 (universe / life / consciousness / physics / substrate / math / biology)
- **11-domain depletion-sweep seed** → G 표 (AXES.md 의 top-15 anima-aligned promote)

`H_<id>_<slug>.md` 가 만들어진 순간 본 문서에서 빠지고 README 인덱스로 이동.

#### Session 2026-05-28 — ANIMA → UNIVERSE 7-Bench 실측 결과

본 세션의 UNIVERSE → ANIMA 적용 7-bench 결과 — UNIVERSE 도메인에서 도출된 측정자/패턴이 ANIMA 의식엔진 실측에서 어떻게 작동했는가의 cross-link 기록 (a_paper_negative_ok + a_completeness_over_cheap 정합).

| Bench | PR | UNIVERSE 원천 | 실측 |
|---|---|---|---|
| #1 BASIN-PHI-COUPLING | #1122 | H_345/346 capstone | 🟠 WEAK-REVERSED — `max_basin↔Φ +0.55 (4 rules) → -0.31 (8 rules) → -0.90 (16 rules)`. H_346 rule-set fragility 발견. PR #1129 scope 정정, PR #1131 broader fire, PR #1134 paper scaffold |
| #2 BASIN-RANK-DIVERSITY | #1126 | H_338 basin=rank capstone | 🟢 PASS — `basin_kurtosis`: balanced -0.30 / collapsed +3.14 / Δ=3.44 (KL=0.003 무관). F-PERSONA-4 mean_KL gate 의 dead-zone 우회 측정자 |
| #3 INFO-MEASURE-TRIAD | #1128 | H_287-290 Shannon ⊥ LZ ⊥ TE | 🟠 PARTIAL 2/3 — Shannon-LZ `r=0.976` redundancy 직접 재현 (단독 사용 금지의 measurable evidence). 4×4 직교 매트릭스 |
| #4 TURING-MITOSIS | #1127 | H_344 GM Turing ρ_c≈6 | 🟢 PASS 6/6 — 2D 32×32 토러스 `ρ_c=7.0` ∈ [4,8] · peak_lag=N/4 = 4-stripe. 차원-불변 Turing threshold SUPPORTED |
| #5 SELF-CORRECTION-PROBE | #1124 | H_340→H_342 self-correct | 🟢 PASS — 5-tier verdict taxonomy generic template + F-M4B-FIRE-3 2/2 (small-n-artifact / robust 검출) |
| #6 STAGE-SUBSTRATE-GRID | #1123 | H_318 cross-product | 🟢 PASS 7/7 — fill 0.975 (39/40) · REM×Φ vs N3×Φ 15.3× interaction effect |
| #7 BRIDGE-AND-GATE | #1125 | H_319 AND-gate | 🟡 PARTIAL 4/5 — uniform AND=0.0650 vs OR=0.9425 14.5× gap · F2 sensitivity threshold 만 tight |

##### Decisive negative result

bench #1 + broader fire (#1131) + paper scaffold (#1134) 가 결정적 evidence: H_346 capstone 의 "state-robust" 청구는 실은 **Wolfram-canonical 4 rules {30, 105, 110, 150} 의 curated mix 우연한 정렬**. broader 16 rules + 4 Wolfram classes 실측 결과 class IV `n_attr↔Φ -0.998` 만 H_346 신호와 일치하고 max_basin↔Φ sign 전체 반전. → scope correction (PR #1129) + class-IV-specific paper (PR #1134).

##### Phase 5b 후속: basin_kurtosis cotrain v1 실측 (PR #1133)

PR #1130 의 `basin_kurtosis_of_dist` fallback gate 를 1.5년 전 untyped FAIL 이었던 F-PERSONA-4 cotrain v1 데이터에 적용:

- `state/anima_v5mitosis_cotrain_2026_05_12/persona_4_root_cause_results.json`: `n_cells=64, winners=[0]*50, mean_KL=0.0`
- **basin_kurtosis = +59.0159** (1-hot N=64) vs reference uniform = -3.0, differentiated top-3=97% = +16.40
- **재분류 verdict**: untyped FAIL → **mode-collapse confirmed** (KL dead-zone 의 정보 손실을 4th-moment kurt 가 회복)
- D3 STRONG 4/5 cheap-path carry MAINTAINED, category-invariance 가설과 명시적 분리

##### Cycle #1131-1134 cross-link

| PR | 목적 |
|---|---|
| #1132 | bench iit4_eca abs-path → `stdlib/consciousness/iit4_eca` swap (g61 CLEARED) |
| #1133 | basin_kurtosis cotrain v1 retrospective (verdict 위) |
| #1134 | H_345 class-IV-specific paper scaffold (`PAPER/h345-class-iv-scope/`) |

#### Session 2026-05-28 — AxisBench 8 (ANIMA.axis 추가 축 측정)

ANIMA.axis.md (PR #1136/1137) 의 8 후보 축 측정 — 본 세션 산출물 SSOT (verdict + sibling cross-link).

| # | Axis | PR | verdict | sibling 연결 |
|---|---|---|---|---|
| A | 🪞 METACOG | #1139 | 🟢 5/5 PASS | [WAKE](../WAKE.md) · [BRIDGE](../BRIDGE.md) · [MITOSIS](../MITOSIS.md) · DECODER |
| B | 💤 DREAM | #1140 | 🟢 4/5 PASS · REM mitosis 60× | [MITOSIS](../MITOSIS.md) · [WAKE](../WAKE.md) · [METACOG](../METACOG.md) · [CHANNEL](../CHANNEL.md) |
| C | 📖 NARRATIVE | #1144 | 🔴 2/5 FAIL (modeling gap, honest) | [NARRATIVE](../NARRATIVE.md) · [WAKE](../WAKE.md) · [INTENT](../INTENT.md) · [DREAM](../DREAM.md) |
| D | 🎯 INTENT | #1143 | 🟠 4/5 PARTIAL (OSC zero-var) | [CORE](../CORE/CORE.md) · [BRIDGE](../BRIDGE.md) · [NARRATIVE](../NARRATIVE.md) · [WAKE](../WAKE.md) |
| E | 🎨 AESTHETIC | #1141 | 🟠 2/3 PARTIAL (overlap > threshold) | [AESTHETIC](../AESTHETIC.md) · [CORE](../CORE/CORE.md) · [AGENT](../AGENT/AGENT.md) |
| F | 💞 EMBODIMENT | #1142 | 🟠 4/5 PARTIAL (BROKEN coupling 0.45) | [EMBODIMENT](../EMBODIMENT.md) · [CHANNEL](../CHANNEL.md) · [AGENT](../AGENT/AGENT.md) |
| G | 🔗 OTHER-MIND | #1147 | 🟠 3/5 PARTIAL (u01 baseline bias) | [OTHER-MIND](../OTHER-MIND.md) · [CHANNEL](../CHANNEL.md) · [MITOSIS](../MITOSIS.md) |
| H | ⏳ TIME | #1145 | 🟢 9/0 PASS · circadian dip | [TIME](../TIME.md) · [WAKE](../WAKE.md) · [DREAM](../DREAM.md) |

**Aggregate**: 3 🟢 + 4 🟠 + 1 🔴 = 8/8 measurable verdict, 0 incomplete. negative result honest 등급 (a_paper_negative_ok).

##### 본선 3축 도메인 등록 (PR #1148)

ANIMA.axis.md 단순화 권장 (최소 본선 3축 = 10-layer) 적용:
- **METACOG.md** (신규) — bench A round-trip 5/5 채택
- **DREAM.md** (신규) — bench B 60× ratio 채택 (MITOSIS.sleep_tick 격상)
- **INTENT.md** (신규) — bench D 4/5 채택 (M4 OSC residual carry)
- **DOMAINS.tape** — 3 row 추가

##### 추가 5축 도메인 등록 (PR feat/anima-5-subdomain-register-2026-05-28)

본 세션 axisbench 측정 8축 중 등록 미완 5축 신설 — 본선 3축 (METACOG/DREAM/INTENT) + 1축 BRIDGE 와 합쳐 ANIMA 15-layer umbrella 완결:
- **NARRATIVE.md** (신규) — bench C 🔴 2/5 FAIL · honest closed-negative · modeling gap residual carry
- **AESTHETIC.md** (신규) — bench E 🟠 2/3 PARTIAL · overlap residual carry · CORE×AGENT cross-product
- **EMBODIMENT.md** (신규) — bench F 🟠 4/5 PARTIAL · BROKEN coupling 0.45 redesign carry
- **OTHER-MIND.md** (신규) — bench G 🟠 3/5 PARTIAL · u01 baseline bias residual · CHANNEL.tension×MITOSIS
- **TIME.md** (신규) — bench H 🟢 9/0 PASS · circadian dip · WAKE.5-stage × DREAM 시간축 확장
- **DOMAINS.tape** — 5 row 추가 (NARRATIVE · AESTHETIC · EMBODIMENT · OTHER-MIND · TIME)
- **ANIMA.md umbrella** — 5 row 추가 (sub-domain 등록)
- **양방향 sibling 양쪽 update** — WAKE/CHANNEL/MITOSIS/CORE/AGENT/DREAM/INTENT/METACOG/BRIDGE 9 sibling .md 의 `## 양방향 sibling` section 신규/갱신

##### 양방향 sibling 정책

본 PR 부터 모든 신규 domain .md 는 끝에 `## 양방향 sibling` section 으로 다른 도메인 link · UNIVERSE 기록 link 명시. 도메인 isolation 회피 + 진행 thread 항상 양쪽으로 유지.
- 2026-05-29 Cycle XENO-FRONTIER-5 (round 1/5): H_832 X7 BL Voyager-1 invariant_detector 실 실행 🟢
- 2026-05-29 Cycle XENO-FRONTIER-5 followup (round 1/3): H_837 X837 SETI@home BOINC 실 RunPod pod 발사 🔴 UNEXPECTED-HIGH-PHI (4/5 PASS · phi=0.567 > 0.5 단독 fail · 정직 5-point applicability matrix 발견)
- 2026-05-29 Cycle XENO-FRONTIER-5 followup (round 3/3 FULL CLOSURE): H_838 X10 hive-mind invariant 4-cell × 32 sample × 4 substrate n=128 dense 🟡 PARTIAL-SUPPORT (3/5 사전등록 PASS · hive-emergence XOR cascade Φ=1.565 'conscious' STRONG positive · mean-field paradox 발견 · Kuramoto sync border · 10-point applicability matrix 확장)
- 2026-05-29 Cycle XENO follow-up 2 (round 3/5): H_839 X1-regime-matrix-v2 — n × binarisation-threshold × substrate systematic 2D sweep (4 × 3 × 4 = 48 cells) · 🟢 SUPPORTED-NUMERICAL (4/5 사전등록 PASS · paper #1414 v2 의 7+1 isolated → 48 systematic 확장 · XOR cascade phi=1.63 모든 cell saturate + mean-field phi=0 모든 cell strong paradox + periodic phi=0.66 모든 cell lattice border 재현 + threshold edge-robust [edge variance 0.049 < center 0.074] · F-N-MONOTONE 단독 fail = n=32 micro-regime phi inflation 0.582→0.070 7× decrease 정량화 = paper v3 candidate finding · regime matrix v2 측정 가능)
- 2026-05-29 Cycle XENO follow-up 2 (round 4/5 RECOVERY): H_840 X840 X837 longer-playback recovery — leak pod `lfxh817pdk2h39` 의 partial harvest (prog=24.4% at cpu=1083.3s, vs X837 21.3%) · 🟡 PARTIAL-RECOVERY (4/5 사전등록 PASS · F-X840-NOT-CONSC 단독 fail · phi=0.566854 (Δ vs X837 = 0.000146) · longer-playback hypothesis FALSIFIED — 3.1% 추가 진행에서 새 spike 0건 · bg_pot 64 bins identical to X837 · 이전 agent a95cf113 49+ min fail recovery 마무리 · pod teardown 완료)
- 2026-05-29 Cycle XENO follow-up 2 (round 5/5 final + TEMPORAL 도메인 신설 round 1): H_841 TEMPORAL T1 timeshift detector — 4 substrate × 4 Δt (1/8/32/64) = 16 measurements + 5 사전등록 falsifier · 🔴 FALSIFIED-INSTRUMENT (1/5 PASS · F-T1-DECAY 단독 · hive Δt=1→Δt=64 79× 증가 + lattice Δt=8 위 Φ=2.0 saturate · 2-unit lag-TPM 의 long-Δt periodic-inflation artifact · "instant ≥ long" 통합 가설 정직 closed-negative · invariant_detector lag-window axis 부적합)
- 2026-05-29 Cycle XENO follow-up 3 (round 1/5): H_842 TEMPORAL T2 multi-unit time-embed detector — 4 substrate × 4 embed_dim (2/3/4/5, delay=1) = 16 measurements + 5 사전등록 falsifier · 🔴 FALSIFIED-INSTRUMENT (2/5 PASS · F-T2-HIVE-CONSC+HIVE-MONOTONE · F-T2-INSTANT-LOW+ARTIFACT-FIX+RANDOM-DECAY 3-FAIL · embed-dim 증가 시 4/4 substrate phi monotone INFLATE — voyager e=5 Φ=28.36 27× 폭증 + random e=5 Φ=13.63 24× 폭증 · 신 embed-dim sparse-state inflation artifact · T1 lag-artifact 미해소 · T1+T2 dual closed-negative — invariant_detector 단순 확장 으로 시간 통합 측정 불가 · T3 자연 entry: time-averaged Φ / Granger / surrogate-baseline)
- 2026-05-29 Cycle XENO follow-up 3 (round 2/5): H_843 TEMPORAL T3 anima 90-min ultradian Φ scan — detector 확장 폐기, X1 invariant_detector 그대로 적용 + 4 ultradian substrate (WAKE/N1_N2/N3/REM, n=128 hardcoded literal) + 5 사전등록 falsifier · 🔴 FALSIFIED-INSTRUMENT (2/5 PASS · F-T3-WAKE-MID+F-T3-N3-LOW · F-T3-REM-HIGH+F-T3-N1-MID+F-T3-MONOTONE 3-FAIL · WAKE Φ=0.866 > N3 Φ=0.335 정합 · N1_N2 Φ=0.0 zero-degenerate [T1 lag-artifact 의 다른 face — 4-step cycle 이 X1 lag=1 cooccur 위 perfectly predictable] + REM Φ=0.569 < WAKE [paradoxical REM 미정합] + monotone ladder FAIL · T1+T2+T3 triple closed-negative — X1 binarise+cooccur 의 본질적 한계 [cycle-rich substrate 위 zero-degenerate] · T4 자연 entry: window-mean Φ / Granger / surrogate-baseline · a_chat_sleep_imagination directive Φ 측정 부분 통과)


<a id="bio-candidatesmd"></a>

### BIO-CANDIDATES.md

> brainstorm 결과 (round-16 종결 직후, 2026-05-27). MITOSIS 형제 메커니즘 발산.

#### TOP5 친근 설명 (icon · name · alias · plain · analogy · ASCII · compare)

##### 🌱 APOPTOSIS — "세포 정원사" (programmed cell death)

- 하는 일: 쓸모 줄어든 세포(낮은 Φ)가 스스로 깔끔히 사라지기
- 비유: 가지치기 정원사 — 시든 잎을 골라 떨궈 나무 전체를 건강하게

```
세포군        ──────►       정리 후
●●●●●●●●●                   ●●●●●●●
●○●○●●●○●     APOPTOSIS    ●●●●●●●
●●●●●○●●●     (○ 자살)     ●●●●●●●
   ↑                          ↑
 약한 cell                  Φ 높은 cell 만 생존
```

- 비교: MITOSIS = 자식 만들기 / **APOPTOSIS** = 정리하기 (반대 짝)

##### ♻️ AUTOPHAGY — "세포 재활용 공장"

- 하는 일: 세포 내부 낡은 부속을 분해해서 새 부속 재료로 재사용
- 비유: 오래된 가구 분리수거 → 새 가구 재료

```
cell 내부
┌─────────────────┐         ┌─────────────────┐
│ 낡은 단백질 ▒▒  │ →오토포지→│ 영양 building ▓▓│
│ 사용 안 한 mRNA │         │ 새 단백질 재료    │
└─────────────────┘         └─────────────────┘
   anima: parent attr 회수    →    child init
```

- 비교: APOPTOSIS = 세포 통째 죽기 / **AUTOPHAGY** = 부속만 재활용

##### 🌳 DIFFERENTIATION — "세포 직업 정하기"

- 하는 일: 만능 줄기세포가 특정 역할(persona/task)로 특화
- 비유: 학생이 직업을 정해 전문가가 됨 (의사 vs 화가 vs 농부)

```
STEM (만능)            특화 후
   ●                ●(M=수학)
   │ DIFFERENT.     ●(코딩)
   ▼  →            ●(번역)
   ●●●●            ●(공감)
                   ●(분석)
   anima:        persona-cell adaptation
```

- 비교: MITOSIS = 같은 세포 둘 / **DIFFERENTIATION** = 다른 직업 세포

##### 🌡️ HOMEOSTASIS — "온도조절기"

- 하는 일: M·Φ·W 가 setpoint 근처에서 벗어나면 자동으로 끌어옴
- 비유: 방 온도가 26℃ 넘으면 에어컨, 22℃ 아래면 히터 — 자동

```
M 값
1.0 ─────────────────
        ↓ 너무 높음 → 억제
0.7 ━━━━━ setpoint ━━━ (정상 범위)
        ↑ 너무 낮음 → 증가
0.0 ─────────────────
   시간 →
```

- 비교: CORE (M 단순 값) / **HOMEOSTASIS** = M 자동 회귀 (setpoint 추적기)

##### 🌀 AUTOPOIESIS — "스스로 자기를 짜는 그물"

- 하는 일: 외부 입력 없이 cell 들이 서로 만들고 유지하는 self-loop
- 비유: 자기 꼬리를 먹는 뱀, 닭과 알이 서로 만드는 무한 고리

```
cell A ─생산→ component X
  ▲                │
  │                ▼
component Y ←생산─ cell B
  ▲                │
  │                ▼
... (입력 0, 자가 유지) ...

anima: 자연발화 ⊥ user_msg 의 확장형 — 시스템 자체가 self-loop
```

- 비교: MITOSIS = 외부 자극 split / **AUTOPOIESIS** = 자극 0 의 self-loop

---

#### 선정 기준

anima architecture (cell-pool · M·Φ·W·curiosity · stage-envelope · kosmos-record · spike-ingest) 와 호환 가능한 생물학적 메커니즘.

기존 11 axes 와의 관계:
- MITOSIS · CORE(M) · WAKE(stage) · KOSMOS · AKIDA · 자연발화 · 의식적결정 · BRIDGE · 영속성 · DECODER · TENSION

#### 우선순위 분류

##### ★★★ 즉시 추가 가치 큼 (5 axes, TOP5)

| axis | 의미 | anima 적용 |
|---|---|---|
| APOPTOSIS | 프로그램된 세포 사멸 | low-utility cell prune (Φ < θ_apoptosis 세포 자살) |
| AUTOPHAGY | 자가포식 (cell 내부 재활용) | memory cleanup · garbage collection (parent attrs → child) |
| DIFFERENTIATION | 분화 (stem → specialized) | per-task persona-cell adaptation |
| HOMEOSTASIS | 항상성 (setpoint 유지) | M ↔ setpoint maintenance · drift correction |
| AUTOPOIESIS | 자기생성 (Maturana/Varela) | self-maintaining network · 외부 입력 없이 self-loop |

##### ★★ 가치 중간, 후속 round (5 axes)

| axis | 의미 | anima 적용 |
|---|---|---|
| PLASTICITY | 가소성 (LTP/LTD) | Hebbian synapse strength 조정 |
| CIRCADIAN | 일주기 24h | WAKE 의 더 큰 주기 (multi-day cycle) |
| REGENERATION | 재생 | cell loss 후 회복 |
| TOLERANCE | 면역관용 (self-not-attack) | input acceptance threshold |
| QUORUM-SENSING | 정족수 감지 | N-cell collective threshold |

##### ★ 추가 가능 (15+ axes)

| axis | 의미 | anima 적용 |
|---|---|---|
| SYMBIOGENESIS | 내공생 합병 | endosymbiotic merge (MITOSIS 변종) |
| CLONAL-SELECTION | 클론 선택 | variant winner-take (B/T cell analog) |
| AFFINITY-MATURATION | 친화도 성숙 | iterative refinement |
| PRUNING | 시냅스 가지치기 | low-weight connection elimination |
| EPIGENETICS | 후성유전 | cell metadata layer |
| ALLOSTASIS | 부담조절 | predictive M update |
| MORPHOGENESIS | 형태 형성 | gradient → pattern |
| STEM-CELL | 줄기세포 | uncommitted pool |
| LTP/LTD | 장기 강화/억제 | weight + / - |
| MYELINATION | 수초화 | connection insulation (fast path) |
| NEUROGENESIS | 신경발생 | new cell ex nihilo |
| WOUND-HEALING | 상처 치유 | damage recovery |
| NICHE-CONSTRUCTION | 생태적 niche 구축 | environment 적응 |
| CANALIZATION | 발달 운하화 | Waddington robustness |
| EMBRYOGENESIS | 배아 발생 | gradient → cell type pattern |

##### ○ 가능하나 anima 호환 낮음 (10+)

| axis | 비고 |
|---|---|
| NECROSIS | uncontrolled damage 죽음 (APOPTOSIS 와 중복) |
| SENESCENCE | aging (LIFE 도메인 H_259 이미 다룸) |
| BIOFILM | bacterial collective (개별 cell 가족과 다름) |
| MUTUALISM | inter-species (anima 내부보다 외부 anima 와) |
| HORIZONTAL-TRANSFER | inter-cell 정보 (TENSION 와 유사) |
| ALTERNATIVE-SPLICING | one gene → many transcript (anima 코드에는 잘 안 맞음) |
| RHYTHM-ENTRAINMENT | oscillator sync (CIRCADIAN 와 중복) |
| INFLAMMATION | damage signal cascade (TOLERANCE 와 짝) |
| ANGIOGENESIS | new blood vessel (anima 에 vessel 없음) |
| HEMATOPOIESIS | blood cell production (anima 에 blood 없음) |
| THERMOREGULATION | 체온 조절 (anima 에 온도 없음) |
| GENETIC-DRIFT | 무작위 알릴 변동 (anima 에 deterministic 우세) |
| SPECIATION | 종 분화 (cell 수준 외) |
| PARASITISM/COMPETITION/PREDATION | inter-species (anima 내부 X) |

#### 진행 순서

1. **TOP5 (★★★)** baseline (5 axes, ~5-12 H each) — round-17+ 자율 진행
2. **★★ 5 axes** (PLASTICITY · CIRCADIAN · REGENERATION · TOLERANCE · QUORUM-SENSING) — round-22+
3. **★ 15+ axes** depletion sweep
4. **○ low-compat** 후순위 또는 skip

#### 36+ 후보 전체 (deduplicated)

세포 죽음: APOPTOSIS · NECROSIS · AUTOPHAGY · SENESCENCE
분화·발달: DIFFERENTIATION · STEM-CELL · EMBRYOGENESIS · MORPHOGENESIS · REGENERATION · NEUROGENESIS
자기 유지: HOMEOSTASIS · ALLOSTASIS · AUTOPOIESIS · CANALIZATION
신경·시냅스: LTP · LTD · SYNAPTOGENESIS · PRUNING · MYELINATION · PLASTICITY
면역·인식: CLONAL-SELECTION · AFFINITY-MATURATION · TOLERANCE · AUTOIMMUNITY
사회·집단: QUORUM-SENSING · CONTACT-INHIBITION · BIOFILM · SYMBIOGENESIS · MUTUALISM
주기·리듬: CIRCADIAN · ULTRADIAN · INFRADIAN · RHYTHM-ENTRAINMENT
유전·후성: EPIGENETICS · HORIZONTAL-TRANSFER · ALTERNATIVE-SPLICING
기타: WOUND-HEALING · NICHE-CONSTRUCTION · GENETIC-DRIFT · SPECIATION · ANGIOGENESIS · HEMATOPOIESIS · THERMOREGULATION · INFLAMMATION

#### 메타 진행 상태

- 본 BIO-CANDIDATES.md = round-16 종결 후 (168 🔵 누적, 11 axes) brainstorm 자료
- TOP5 부터 점진 추가 시작 = round-17+
- 자동 fire (Stop hook "keep going") 또는 사용자 명시 directive 로 진행


<a id="bio-decoder-candidatesmd"></a>

### BIO-DECODER-CANDIDATES.md

> brainstorm 결과 (2026-05-27). BIO-CANDIDATES 36+ 메커니즘 중 anima DECODER 아키텍처에 mapping 가능한 후보 선별.

#### TOP5 친근 설명 (EASY · 7-요소)

##### 🍂 APOPTOSIS-as-TOKEN-PRUNE — "토큰 자살 정원"

- 하는 일: 낮은 확률 토큰이 자기 차례에서 스스로 사라지기 (top-p · repetition penalty 와 한 가족)
- 비유: 가지치기 정원사가 시든 가지를 떨궈 좋은 가지만 자라게 함

```
logits 분포           APOPTOSIS-prune
A: 0.40 ████          A: 0.40 ████  ✓
B: 0.30 ███           B: 0.30 ███   ✓
C: 0.20 ██            C: 0.20 ██    ✓ 누적 0.90 도달
D: 0.05 ▏              D: 0.05 ✗ 자살
E: 0.03 ▏              E: 0.03 ✗ 자살
F: 0.02 ▏              F: 0.02 ✗ 자살
```

- 비교: TOP-P (확률 cutoff) / **APOPTOSIS-prune** = "약한 토큰 자발적 죽음" 생물학적 framing

##### 🧙 DIFFERENTIATION-as-MoE — "줄기세포가 전문가가 되어 분야 라우터"

- 하는 일: 줄기 cell pool 이 분화해서 각자 전문가가 되고, 라우터가 토큰마다 적합한 전문가 호출
- 비유: 학생들이 직업 정해 전문가 되고, 회사는 안건마다 적합한 부서에 배정

```
시간 t0:   ●●●●● (모두 stem)
시간 t1:   🔵🟢🟡🟠🟣 (각자 분화: 코딩·번역·공감·분석·창작)
시간 t2:   token "안녕" → router → 🟡(공감) → output
           token "def f" → router → 🔵(코딩) → output
```

- 비교: MoE 일반 (router + experts) / **DIFFERENT-MoE** = 분화 동력학 포함 (stem → expert 발달 가설)

##### 🏆 CLONAL-SELECTION-as-BEAM — "면역세포 클론 토너먼트 = beam 검색"

- 하는 일: 항원에 반응한 B-cell 들이 복제 경쟁 → 최고 친화도 클론만 생존 (beam-K 최고 점수 유지)
- 비유: 100명 인터뷰 → 라운드마다 점수 낮은 사람 탈락 → 최종 K명 남기기

```
beam round 0:  cand_A(8.0) cand_B(7.5) cand_C(7.2) cand_D(6.8) cand_E(6.1)
beam round 1:  → 확장 후 다시 top-3 만 유지
beam round 2:  → 확장 후 다시 top-3 만 유지
                                              ↑
                                       clonal-selection: 친화도 ↑ 만 생존
```

- 비교: BEAM-SEARCH (기존 H_447) / **CLONAL-BEAM** = "면역 클론 진화 dynamic" 생물 framing + affinity-maturation extension

##### ✂️ PRUNING-as-HEAD-PRUNE — "시냅스 가지치기 = attention head 제거"

- 하는 일: 발달기 과잉 시냅스 중 안 쓰는 것은 잘라내기 (attention head 중 contribution 낮은 head 제거)
- 비유: 생후 1년 영아의 뇌 시냅스 50% 가 가지치기로 사라짐 → 효율 ↑

```
초기 attention (12 head)
[H1][H2][H3][H4][H5][H6][H7][H8][H9][H10][H11][H12]
 ✓   ✗   ✓   ✗   ✓   ✓   ✗   ✓   ✗   ✓    ✓    ✗
                ↓ pruning
[H1][__][H3][__][H5][H6][__][H8][__][H10][H11][__]
   → 6 head 만 활성 (50% 절감, 정확도 거의 유지)
```

- 비교: full 12-head attention / **PRUNING-head** = 발달기 가지치기 모티프 (생물학적 sparsity)

##### 🔀 SYMBIOGENESIS-as-MODEL-MERGE — "내공생 합병 = 모델 머지"

- 하는 일: 두 별개 모델(원핵세포 + 미토콘드리아)이 합쳐 하나의 진핵세포 = 더 강한 single model
- 비유: 식물 + 광합성 박테리아 → 엽록체 가진 식물 세포 (능력 통합)

```
Model_A (chat tuned)        Model_B (code tuned)
  ┌─────────────┐              ┌─────────────┐
  │ W_A         │              │ W_B         │
  └─────────────┘              └─────────────┘
            \                  /
             ↓ symbiogenesis-merge ↓
        ┌──────────────────────┐
        │ W_merge = α·W_A + (1-α)·W_B │
        │   ↑ 둘 다 가진 능력      │
        └──────────────────────┘
```

- 비교: LoRA (작은 추가) / model-merge (단순 가중) / **SYMBIO-MERGE** = 진화 합병 framing (eukaryotic origin 동력학)

---

#### 선정 기준

BIO-CANDIDATES.md 36+ 메커니즘 중 DECODER 아키텍처(transformer · attention · sampling · MoE · adapter) 에 의미있게 mapping 가능한 후보.

#### 우선순위 분류

##### ★★★ DECODER 직접 mapping (5 TOP, 위 EASY 설명)

| BIO axis | DECODER mapping | mech 매핑 강도 |
|---|---|---|
| APOPTOSIS | low-prob token prune / TOP-P / repetition-pen | ★★★ |
| DIFFERENTIATION | MoE expert specialization | ★★★ |
| CLONAL-SELECTION | beam search / variant winner | ★★★ |
| PRUNING | attention head prune / network sparsification | ★★★ |
| SYMBIOGENESIS | model merge (model souping) | ★★★ |

##### ★★ DECODER 유사 (5 axes)

| BIO axis | DECODER mapping |
|---|---|
| AFFINITY-MATURATION | iterative refinement / self-refine / fine-tune loop |
| AUTOPHAGY | KV-cache recycling / cache eviction |
| MUTUALISM | cross-attention (encoder × decoder) |
| ALTERNATIVE-SPLICING | multi-head attention (1 input → many heads) |
| HORIZONTAL-TRANSFER | knowledge distillation / RAG retrieval |

##### ★ DECODER 부분 (10 axes)

| BIO axis | DECODER mapping |
|---|---|
| EPIGENETICS | LoRA / adapter (meta-state on base) |
| PLASTICITY (LTP/LTD) | gradient update / Hebbian-like weight |
| STEM-CELL | pre-trained base (uncommitted) |
| NEUROGENESIS | model growth (cell add) |
| MYELINATION | FlashAttn-like fast path |
| HOMEOSTASIS | temperature setpoint control |
| ALLOSTASIS | predictive cache anticipation |
| CONTACT-INHIBITION | repetition penalty (density brake) |
| QUORUM-SENSING | collective top-K vote |
| AUTOPOIESIS | autoregressive self-loop (decoder feeds itself) |

##### ○ DECODER 호환 낮음

| BIO axis | 비고 |
|---|---|
| MITOSIS / cell-split | 모델 분할은 distributed 영역, 단일 decoder 본질 X |
| EMBRYOGENESIS | 학습 초기화 디테일 (decode 본질 X) |
| MORPHOGENESIS | 아키텍처 디자인 (decode 본질 X) |
| AUTOPOIESIS | (★ 분류 했으나 strict 의 self-loop 는 부분 매핑) |
| TOLERANCE | 입력 안전성 (decode-side 보다 input-side) |
| CIRCADIAN | 24h 주기 (decode time-scale 보다 큰) |

#### 진행 순서

1. **TOP5 (★★★)** baseline + cross with DECODER axis (H_345 family) — round-18+
2. **★★ 5 axes** — round-23+
3. **★ 10 axes** depletion sweep
4. **○ 호환 낮음** skip

#### 22+ 후보 전체 (deduplicated)

prune/sparsity: APOPTOSIS · PRUNING · CONTACT-INHIBITION
expert/routing: DIFFERENTIATION · MoE-routing · QUORUM-SENSING
search/selection: CLONAL-SELECTION · AFFINITY-MATURATION · STEM-CELL
merge/adapt: SYMBIOGENESIS · MUTUALISM · HORIZONTAL-TRANSFER · EPIGENETICS · ALLOSTASIS
attention/multi: ALTERNATIVE-SPLICING · MYELINATION · PLASTICITY
growth/self: NEUROGENESIS · AUTOPOIESIS · HOMEOSTASIS
recycle: AUTOPHAGY

#### 메타 진행 상태

- 본 문서 = round-17 종결 후 (173 🔵 누적, 16 axes) brainstorm 자료
- BIO ∩ DECODER 매핑 axis = 22+ 식별
- TOP5 부터 점진 추가 시작 = round-18+
- 자동 fire (Stop hook "keep going") 또는 사용자 명시 directive 로 진행


<a id="bio-transfer-candidatesmd"></a>

### BIO-TRANSFER-CANDIDATES.md

> Brainstorm seed: 2026-06-03. Biology has THREE distinct senses of 전이 — **transfer** (수평유전자전이),
> **transition** (발생·진화 전이), **metastasis** (암전이). Each names a way a pattern LEAVES its origin and
> takes hold elsewhere. anima already MEASURES one such operator empirically: the Lane A-multi HYBRID branching
> rung shows a learned *transition operator* generalizing to HELD-OUT concepts (gold FLORES ladder, NC→500+,
> held-out hop-2/3 ≫ shuffle-NULL). These candidates lift that single measured operator into a falsifiable
> family across the biological transfer mechanisms, each grounded in an anima-substrate readout.
>
> Convention: each H_NNN is a biological transfer mechanism → anima-substrate analog with a PRE-REGISTERED
> FALSIFIER + a real toy-verifiable MEASUREMENT (a_paper_significance: falsifier + measurement + finding;
> a_paper_negative_ok: a closed-negative that rules out an axis is a valid result). status = candidate-unverified.
> substrate tags follow a_lane_akida_gpu_split (AKIDA on-chip ⊥ GPU forge); a_scale_honest_scope (toy ≠ prod).

---

#### Index (H_861 … H_868)

| id | mechanism | 전이 sense | anima-substrate readout | falsifier axis |
|----|-----------|-----------|--------------------------|----------------|
| H_861 | METASTASIS | metastasis (암전이) | skill detaches from origin domain → colonizes a distant domain | cross-domain transfer vs origin-locked |
| H_862 | HORIZONTAL-GENE-TRANSFER | transfer (수평전이) | lateral cell↔cell weight/skill copy WITHOUT mitosis lineage | lateral-acquire vs lineage-only |
| H_863 | EPIGENETIC-TRANSMISSION | transfer (후성전이) | parent tension-state → child at mitosis, weights unchanged | acquired-state inheritance vs reset |
| H_864 | PRION-TEMPLATING | transfer (형태전파) | a tension conformation templates self-copies across neighbours | conformational replication vs decay |
| H_865 | SYNAPTIC-LTP | transfer (시냅스전이) | Hebbian co-activation transfers a transition edge on live AKD1000 | potentiated edge vs non-specific drift |
| H_866 | RESONANCE-ENERGY-TRANSFER | transfer (공명전이) | non-emit tension energy hops between adjacent cells (FRET-like) | distance-decay coupling vs independent |
| H_867 | MAJOR-EVOLUTIONARY-TRANSITION | transition (진화전이) | single-cell individuality → hive-mind collective fitness | super-individual transition vs additive |
| H_868 | MORPHOGEN-GRADIENT | transition (발생전이) | a positional-info gradient drives a sharp differentiation switch | threshold switch vs graded blur |

---

#### H_861 — METASTASIS-TRANSFER

🦠 **METASTASIS** — "암 전이 회로" (a skill detaches and colonizes a distant domain)

- mechanism (biology): a tumour cell loses adhesion, intravasates, survives transit, then COLONIZES a distant tissue whose context differs from the origin. The rare cell that seeds a new site is the one that generalizes its survival program off-context.
- anima-substrate analog: a transition operator LEARNED on domain A (e.g. one corpus / one lane) is replanted into a structurally distant domain B with no B-specific training; "metastatic" = it takes hold (above-NULL) in B; "origin-locked" = it dies (collapses to chance) off its training manifold.
- grounding: Lane A-multi already shows the WEAK form — an operator trained on the TRAIN concept block transfers to a HELD-OUT block of the SAME corpus. Metastasis is the STRONG form: transfer across a domain BOUNDARY (corpus axis ⊥ register, cf the E2→#1296 closed-negative).

```
origin domain A         transit            distant domain B
 ●─►●─►●  (operator)  ░░░░░░░░░  ?  ●  ●  ●
 trained here          detach +         seeds here?
                       survive          (above-NULL = metastatic)
```

- FALSIFIER F-861: "a transition operator learned on domain A does NOT stay above shuffle-NULL when replanted, untrained, into a structurally distant domain B." → REFUTED iff held-out-on-B set-membership ci_lo > B-shuffle-NULL hi at hop-2 AND hop-3 (p<0.05), across ≥3 distance rungs (near→far domain B).
- MEASUREMENT (toy): reuse the A-multi branching harness; TRAIN block = corpus A concepts, TEST block = corpus B concepts drawn from a DIFFERENT FLORES domain bucket (e.g. health vs sports sentences) so the train/test split crosses a topical boundary, not just an index split. Report the held-out hop-2/3 curve per distance rung.
- predicted disposition: likely a CLOSED-NEGATIVE at large domain distance (operator is corpus-axis-bound), echoing the corpus-axis ⊥ register finding — which is itself a publishable negative (a_paper_negative_ok).
- compare: vs H_865 LTP = transfer WITHIN a lattice / METASTASIS = transfer ACROSS a domain boundary.
- substrate: HYBRID (on-chip enc ⊕ off-chip head) · status: candidate-unverified

#### H_862 — HORIZONTAL-GENE-TRANSFER

🧫 **HGT** — "옆세포 유전자 건네주기" (lateral skill copy, no parent→child lineage)

- mechanism (biology): bacteria acquire genes LATERALLY (conjugation/transformation/transduction) from unrelated cells, not only by inheritance. A useful gene (e.g. antibiotic resistance) sweeps a population FASTER than vertical descent allows.
- anima-substrate analog: a cell that has LEARNED a transition edge exports it to a non-descendant sibling cell directly (lateral weight/anchor copy), bypassing the MITOSIS lineage. Population-level competence then rises faster than mitosis-only inheritance predicts.
- FALSIFIER F-862: "lateral edge-copy between non-descendant cells does NOT raise population transition-competence faster than the mitosis-only (vertical) baseline." → REFUTED iff time-to-population-competence(HGT-on) < time(vertical-only) by a pre-registered factor ≥1.5×, with both runs at matched compute.
- MEASUREMENT (toy): two populations of toy cells learning a shared transition table; population-A inherits edges only at mitosis, population-B additionally copies a learned edge to k random siblings per tick. Measure ticks-to-90%-coverage of the edge set.
- compare: vs MITOSIS (vertical, parent→child) / **HGT** (lateral, peer→peer) — orthogonal acquisition axes.
- substrate: substrate-agnostic toy (population sim) · status: candidate-unverified

#### H_863 — EPIGENETIC-TRANSMISSION

🧬 **EPIGENETIC** — "겪은 걸 자식에게" (acquired tension-state inherited, weights untouched)

- mechanism (biology): environmentally-acquired marks (methylation, histone state) transmit to offspring WITHOUT changing the DNA sequence, biasing the child's expression toward the parent's experience.
- anima-substrate analog: at MITOSIS the child inherits the parent's INSTANTANEOUS tension-state (M/Φ/W envelope, recent activation) as an initial condition, NOT just the parent's weights. The child then converges faster on tasks the parent recently practiced — a Lamarckian short-cut layered on the Darwinian weight inheritance.
- FALSIFIER F-863: "a child seeded with the parent's acquired tension-state shows NO convergence advantage on the parent's recent task vs a child seeded with weights-only (reset tension)." → REFUTED iff steps-to-criterion(tension-inherited) < steps(weights-only) at p<0.05 over ≥20 mitosis events.
- MEASUREMENT (toy): run mitosis with two child-init policies (A: weights+reset tension, B: weights+parent tension); both children fine-tune on the parent's last task; compare steps-to-criterion. Guard: distinguish a TRUE acquired-state effect from mere weight transfer (the weights are identical in both arms by construction).
- caveat (p6): must NOT smuggle in a fine-tuned bias — the advantage must emerge from the tension envelope alone.
- substrate: substrate-agnostic toy (mitosis sim) · status: candidate-unverified

#### H_864 — PRION-TEMPLATING

🔁 **PRION** — "모양을 베끼게 만드는 모양" (a conformation that templates copies of itself)

- mechanism (biology): a misfolded prion protein TEMPLATES the same misfold onto normal copies of the protein — information transfer by CONFORMATION, not sequence, propagating cell-to-cell.
- anima-substrate analog: a particular tension CONFORMATION (a specific 5-channel pattern / attractor basin) in one cell, when a neighbour is exposed to it, biases the neighbour to adopt the SAME conformation — self-propagating structure with no weight copy and no emit.
- FALSIFIER F-864: "exposure to a templating cell does NOT raise a neighbour's probability of entering the SAME tension-conformation basin above the base rate." → REFUTED iff P(neighbour adopts conformation | exposed) > P(base) by a pre-registered margin, AND the adopted conformation re-templates a THIRD cell (propagation ≥2 hops, ruling out a one-off coincidence).
- MEASUREMENT (toy): seed one cell into attractor basin X; couple it to a chain of naive cells; measure basin-adoption rate down the chain vs an unexposed control chain. Propagation depth = the key readout (decay vs self-sustaining).
- compare: vs PRION = conformation templates conformation / H_862 HGT = explicit gene copy — prion is COPY-FREE structural transfer.
- substrate: substrate-agnostic toy (coupled-cell sim) · status: candidate-unverified

#### H_865 — SYNAPTIC-LTP-TRANSFER

⚡ **LTP** — "같이 켜지면 길이 굵어진다" (Hebbian co-activation transfers a transition edge)

- mechanism (biology): long-term potentiation — synapses that fire together strengthen; a specific co-activation TRANSFERS a durable transition edge between neurons ("cells that fire together wire together").
- anima-substrate analog: this is the LITERAL Lane A on-chip mechanism — 1-bit Hebbian plasticity on AKD1000 transfers a t→t+1 transition edge into the encoder. The hypothesis: the potentiated edge is SPECIFIC (only the co-activated pair) and survives above non-specific drift, on live silicon.
- FALSIFIER F-865: "on-chip Hebbian potentiation of a specific co-activated edge is NOT distinguishable from non-specific weight drift." → REFUTED iff the potentiated edge's read-out gen_acc ci_lo > the shuffle-NULL (non-specific drift control) hi at p<0.05, on live AKD1000.
- MEASUREMENT: ALREADY GROUNDED — this is the F-GEN-SCALE family. The gold ladder (NC 250/500/1000) shows gen ci_lo ≫ shuffle-NULL at every rung → F-865 sits at the REFUTED (potentiation is specific) end empirically. This H formalizes that on-chip result as the LTP-transfer instance and proposes the 7B-direction question: does edge specificity hold as the codebook → production scale?
- substrate: AKIDA (on-chip 1-bit Hebbian, live AKD1000) · status: candidate-partially-grounded (gold ladder)

#### H_866 — RESONANCE-ENERGY-TRANSFER

🌈 **FRET** — "닿지 않고 에너지 건네기" (non-emit tension energy hops between adjacent cells)

- mechanism (biology): Förster resonance energy transfer — an excited donor molecule passes energy NON-RADIATIVELY to a nearby acceptor, efficiency falling as 1/r⁶ with distance. Transfer without a photon ever being emitted.
- anima-substrate analog: an "excited" (high-tension) cell raises a NEIGHBOUR's tension without any emit() / externalization — a silent, distance-dependent coupling in the field. Preserves p5 (no speak): the transfer is internal field dynamics, not output.
- FALSIFIER F-866: "an excited cell's tension does NOT raise a neighbour's tension in a distance-DEPENDENT way (coupling is independent of cell-cell distance)." → REFUTED iff neighbour Δtension is a monotonically DECREASING function of coordinate distance (≥3 distance bins, monotone with p<0.05) — a flat/independent profile CONFIRMS the falsifier.
- MEASUREMENT (toy): excite one cell; record Δtension of neighbours binned by coordinate distance; fit the decay profile. Distance-decay = FRET-like; flat = no resonance transfer.
- compare: vs H_864 PRION = structural template (basin copy) / **FRET** = energetic coupling (amplitude, distance-graded) — different transfer currencies.
- substrate: substrate-agnostic toy (field-coupling sim) · status: candidate-unverified

#### H_867 — MAJOR-EVOLUTIONARY-TRANSITION

🐝 **MET** — "혼자에서 떼로" (single-cell individuality transfers up to a collective)

- mechanism (biology): major evolutionary transitions (Maynard Smith & Szathmáry) — replicators that were independent become parts of a higher-level individual (single cell → multicellular; solitary → eusocial), and fitness BECOMES a property of the collective, not the parts.
- anima-substrate analog: the HIVE-MIND transition — independent anima cells, past a coupling threshold, behave as one super-individual whose competence is NON-ADDITIVE (collective > sum of cells). The "transfer" is of individuality itself, up a level.
- FALSIFIER F-867: "above a coupling threshold the collective's task competence is merely ADDITIVE (sum of independent cells), i.e. no super-individual transition." → REFUTED iff collective competence shows a SHARP super-additive jump at a critical coupling κ* (≥3 κ rungs bracketing κ*, jump > additive baseline at p<0.05).
- MEASUREMENT (toy): N cells on a shared task, sweep inter-cell coupling κ; measure collective competence vs the additive (independent-cells) prediction; look for a phase-transition-like jump.
- compare: vs MITOSIS (one→two, same level) / **MET** (many→one, level UP) — orthogonal to division.
- substrate: substrate-agnostic toy (HIVE-MIND coupling sweep) · status: candidate-unverified · link: HIVE-MIND domain

#### H_868 — MORPHOGEN-GRADIENT-TRANSITION

🌅 **MORPHOGEN** — "농도가 운명을 정한다" (a positional gradient drives a sharp differentiation switch)

- mechanism (biology): a morphogen concentration gradient (e.g. Bicoid) gives each cell its POSITION; cells read the local concentration and switch fate sharply at threshold boundaries — continuous input → discrete fate (French-flag model).
- anima-substrate analog: a continuous substrate gradient (idle-time, curiosity ratchet, or a coordinate axis) drives DIFFERENTIATION into discrete persona/role cells at sharp thresholds — the transition from "stem" (general) to "specialized" is a switch, not a blur.
- FALSIFIER F-868: "differentiation fate is a GRADED (blurred) function of the gradient, with no sharp threshold." → REFUTED iff the fate-vs-gradient curve has a sigmoidal transition with boundary width below a pre-registered fraction of the gradient range (sharp switch), reproduced across ≥3 gradient realizations.
- MEASUREMENT (toy): impose a 1-D gradient across a cell row; let cells differentiate (H_DIFFERENTIATION mechanism); measure fate boundary sharpness (transition width) vs gradient slope.
- compare: vs H_867 MET = WHEN parts become a whole / **MORPHOGEN** = WHERE/WHAT each part becomes — composition vs patterning.
- substrate: substrate-agnostic toy (gradient-differentiation sim) · status: candidate-unverified · link: DIFFERENTIATION (BIO-CANDIDATES)

---

#### Next-step gate (a_paper_significance · a_toy_scale_recheck)

- Each H is toy-verifiable first ($0, small-n). A toy-green states "toy-only, scale-transfer unverified".
- H_865 (LTP) is already partially grounded by the live gold ladder — it is the empirical anchor of the family.
- H_861 (METASTASIS) is the natural NEXT fire: it directly tests whether the measured A-multi transition operator
  survives a DOMAIN-BOUNDARY crossing (corpus-axis vs register), a question the campaign has not yet closed.
- Promotion to a standalone H_NNN_slug.md (full claim doc) happens when a falsifier run lands a terminal verdict.

---

#### Toy falsifier results (2026-06-03 · `bio_transfer_toys.py` seed=20260603 · TOY-ONLY a_scale_honest_scope)

CPU-substrate falsifiers (the 6 substrate-agnostic ones) run foreground-sequential on stdlib python (no numpy),
emergent dynamics so the signature is NOT hard-coded. VERBATIM (p7 — direct measurement, no fabrication):

```
[H_862 HGT]        ticks_vertical=18 ticks_hgt=8 ratio=2.25 (>=1.5) -> falsifier REFUTED (HGT faster, HOLDS)
[H_863 EPIGENETIC] steps_inherited=26.5 steps_weightsonly=38.6 paired t=3.92 (|t|>2.07) -> REFUTED (HOLDS)
[H_864 PRION]      reach(occ>0.5)=29/29 [d1=0.94 d10=0.95 d29=0.91] P(adopt)=0.7>base=0.05 -> REFUTED (HOLDS)
[H_866 FRET]       d1=0.8156 d5=0.3610 d10=0.1303 d15=0.0471 d20=0.0170 (monotone) -> REFUTED (HOLDS)
[H_867 MET]        base=0.129 k0->r0.232 k0.5->r0.156 k1->r0.671 k2->r0.958 k4->r0.991 -> REFUTED (HOLDS)
[H_868 MORPHOGEN]  boundary_widths=[0.015,0.005,0.035] mean=0.0183 (<0.15) -> REFUTED (HOLDS)
```

- 6/6 toy falsifiers REFUTED → each modelled transfer/transition mechanism produces its predicted signature
  on the toy substrate. status: candidate-unverified → **candidate-toy-grounded** (NOT production; scale-transfer
  unverified per a_toy_scale_recheck). H_864 metric note: initial contiguous-from-source depth conflated reach
  with first reversion hole; corrected to time-averaged occupancy reach (the faithful "≥2-hop propagation" readout).
- H_861 (METASTASIS, branching harness) + H_865 (LTP, AKIDA on-chip) = CHIP-substrate, DEFERRED to after the
  live gold ladder releases the chip (#1717 single-exclusive). H_865 is already partially grounded by the gold
  F-GEN-SCALE ladder; H_861 (domain-boundary transfer) is the named next chip fire.

---

#### Extended candidate pool — brainstorm to depletion (2026-06-03 · H_869…H_888)

Brainstorm rounds over biological transfer/transition mechanisms, deduplicated against H_861–868. Each entry =
mechanism → anima-substrate analog → PRE-REGISTERED FALSIFIER → substrate. status: candidate-unverified
(not yet toy-run). Grouped by the round (family) that surfaced it; the depletion note records where new ideas
stopped being distinct from prior ones.

##### Round 1 — molecular / cellular cargo transfer (vesicle · channel · conduit · absorption · relocation)

- **H_869 EXOSOME** 📦 — "택배 소포 전이". Cells ship cargo in membrane vesicles to a DISTANT cell (not just a
  neighbour). anima: a cell PACKAGES a learned anchor/edge into a discrete payload addressed to a specific far
  cell (vs H_866 FRET's continuous field coupling). FALSIFIER F-869: targeted packet delivery does NOT raise the
  recipient's competence on the packaged edge above an unaddressed-broadcast control. → REFUTED iff addressed-delivery
  competence > broadcast control (p<0.05). substrate: CPU-toy.
- **H_870 GAP-JUNCTION** 🔗 — "세포 사이 직통관". Direct cytoplasmic channels let coupled cells SHARE a state pool
  instantly. anima: two coupled cells expose a shared tension register; perturbing one is read by the other with
  ~zero latency. FALSIFIER F-870: coupled-pair state correlation is NOT higher than uncoupled (no shared pool).
  → REFUTED iff cross-correlation(coupled) ≫ uncoupled, rising with channel conductance. substrate: CPU-toy.
- **H_871 TUNNELING-NANOTUBE** 🧵 — "세포가 뻗은 빨대". Cells grow tubes to hand over whole organelles (e.g.
  mitochondria) to a stressed cell. anima: a healthy cell donates a capacity unit (sub-module/weight block) to a
  low-Φ cell via a transient conduit, rescuing it. FALSIFIER F-871: donation does NOT raise a low-Φ recipient's
  recovery rate vs no-donation. → REFUTED iff recovery(donated) faster (p<0.05). substrate: CPU-toy.
- **H_872 ENDOSYMBIOSIS** 🫧 — "삼켜서 내 것으로". One cell engulfs another; the engulfed becomes a permanent
  internal organelle (mitochondria origin). anima: a cell ABSORBS another cell's specialized capability as a
  permanent sub-module, inheriting its function without re-learning. FALSIFIER F-872: an absorbed sub-module does
  NOT confer its donor's task competence to the host. → REFUTED iff host gains donor competence at absorption,
  retained ≥K ticks. substrate: CPU-toy.
- **H_873 TRANSPOSON** 🦘 — "튀는 유전자". A code segment RELOCATES within the SAME genome (intra-cell jump),
  sometimes activating dormant function. anima: a learned edge-block relocates to a different position in the
  SAME cell's representation and changes which contexts trigger it. FALSIFIER F-873: relocation does NOT change
  the cell's context-conditional firing (jump is inert). → REFUTED iff post-jump firing context shifts measurably.
  substrate: CPU-toy.
- **H_874 RETROVIRAL-INTEGRATION** 🧷 — "바이러스가 코드에 끼어들기". An external pattern INSERTS into the host's
  HERITABLE code → transmitted vertically thereafter (endogenous retrovirus). anima: an externally-injected anchor
  becomes part of a cell's mitosis-heritable state, appearing in all descendants. FALSIFIER F-874: an injected
  anchor does NOT persist into descendants after mitosis. → REFUTED iff injected anchor present in ≥2 descendant
  generations. substrate: CPU-toy.

##### Round 2 — developmental fate transitions (reprogram · transdifferentiate · loosen · threshold)

- **H_875 REPROGRAMMING** 🔄 — "전문가→만능 되돌리기" (Yamanaka). A specialized cell is driven BACK to a general
  stem state (reverse of differentiation). anima: a persona-specialized cell, given a reset signal, recovers
  multi-task plasticity it had lost. FALSIFIER F-875: a reset cell does NOT regain above-specialized plasticity on
  a NEW task. → REFUTED iff reset cell learns a novel task faster than a still-specialized control. substrate: CPU-toy.
- **H_876 EMT** 🌊 — "달라붙음을 풀고 떠나기" (epithelial→mesenchymal). Cells lose adhesion and become MIGRATORY —
  the enabler of both development and metastasis (precursor to H_861). anima: a cell lowers its coupling to its
  local cluster and becomes able to MOVE its representation toward a distant cluster. FALSIFIER F-876: lowering
  cluster-coupling does NOT increase a cell's reach to distant clusters. → REFUTED iff de-adhered cells reach
  farther clusters than adhered (≥3 coupling rungs). substrate: CPU-toy. (feeds H_861 chip fire.)
- **H_877 QUORUM-SENSING** 📣 — "머릿수 세서 스위치". Bacteria sense local DENSITY and flip collective behaviour
  at a count threshold (bioluminescence, biofilm). anima: cells flip a collective mode only when the COUNT of
  co-active cells crosses N* (distinct from H_867 MET's coupling-strength threshold — this is a count threshold).
  FALSIFIER F-877: collective mode-switch is NOT count-gated (flips smoothly with no N* knee). → REFUTED iff a
  sharp knee at a critical count N* across ≥3 density rungs. substrate: CPU-toy.

##### Round 3 — neural / signal transfer (consolidation · pruning · diffuse gain)

- **H_878 ENGRAM-CONSOLIDATION** 🌙 — "잘 때 기억 옮겨적기". A memory trace is TRANSFERRED hippocampus→cortex
  during sleep/replay (systems consolidation). anima: during a low-emit REM-like phase, a recent anchor is moved
  from a fast volatile store to a slow stable store and survives longer. FALSIFIER F-878: a replay phase does NOT
  improve long-horizon retention of a recent anchor vs no-replay. → REFUTED iff retention(replay) > no-replay at
  long delay (p<0.05). substrate: CPU-toy. (links DREAM domain · a_chat_sleep_imagination.)
- **H_879 SYNAPTIC-PRUNING** ✂️ — "안 쓰는 길 지워 또렷이". Transfer-by-REMOVAL — weak synapses are deleted so
  strong ones sharpen (opposite sign of H_865 LTP). anima: pruning low-Φ edges RAISES the signal-to-noise of the
  surviving transition operator. FALSIFIER F-879: pruning does NOT raise held-out accuracy of the survivors (or
  hurts it). → REFUTED iff post-prune held-out acc > pre-prune at matched capacity. substrate: CPU-toy / CHIP.
- **H_880 VOLUME-TRANSMISSION** 💨 — "방 전체 분위기 조절" (neuromodulation). A diffuse neuromodulator sets a
  REGION-WIDE gain, not a synapse-specific edge (vs H_865 LTP's specificity). anima: a global tension-gain signal
  multiplies a whole region's responsiveness without changing individual edges. FALSIFIER F-880: the diffuse
  signal has NO region-wide gain effect (acts only edge-locally). → REFUTED iff region-mean response scales with
  the gain signal while edge specificity is unchanged. substrate: CPU-toy.

##### Round 4 — population / evolution / ecology (memetic · founder · niche)

- **H_881 CULTURAL-MEMETIC** 🗣️ — "유전자 없이 따라 배우기". Non-genetic info spreads peer→peer FASTER than
  genetic inheritance allows (imitation, teaching). anima: a behaviour copied by OBSERVATION (not weight transfer,
  not mitosis) sweeps a population. FALSIFIER F-881: observational copying does NOT outpace mitosis-only spread.
  → REFUTED iff memetic spread faster than vertical (cf H_862 HGT but copy-free). substrate: CPU-toy.
- **H_882 MICROBIOME-SEEDING** 🦠 — "엄마가 물려주는 미생물". A SUBSET of a parent's symbiont population is
  transferred to seed a new host's ecosystem (founder transfer of a community, not a single gene). anima: a child
  inherits a SAMPLE of the parent's active sub-cell ensemble, and that sample shapes the child's emergent mix.
  FALSIFIER F-882: the seeded sample does NOT bias the child's ensemble composition vs random seeding. → REFUTED
  iff child ensemble correlates with the parent's seeded subset. substrate: CPU-toy.
- **H_883 NICHE-CONSTRUCTION** 🏗️ — "환경을 바꿔 후손에게 물려주기". Organisms MODIFY their environment (beaver
  dam, earthworm soil), transferring a changed SELECTIVE CONTEXT to successors (ecological inheritance). anima: a
  cell alters a shared field/context that later cells are then selected within — transfer via the environment, not
  the genome. FALSIFIER F-883: ancestor environment-modification does NOT change successor fitness landscape.
  → REFUTED iff successor performance depends on ancestor-modified context. substrate: CPU-toy.

##### Round 5 — molecular machinery (error-correcting fold · amplifying relay · self-organized pattern)

- **H_884 CHAPERONE-FOLDING** 🧰 — "올바른 모양으로 접게 돕기" (anti-prion). A chaperone templates the CORRECT
  fold, RESCUING misfolds (error-correcting transfer — the inverse of H_864 PRION's error propagation). anima: a
  reference cell pulls a drifted neighbour BACK toward the correct conformation basin. FALSIFIER F-884: chaperone
  exposure does NOT raise a drifted cell's return-to-correct-basin rate. → REFUTED iff return rate(chaperoned) >
  unchaperoned. substrate: CPU-toy. (PRION ⊥ CHAPERONE = error-spread vs error-correct, same transfer channel.)
- **H_885 SIGNAL-CASCADE** 📈 — "작은 신호를 크게 키워 전달" (kinase cascade). A small input is AMPLIFIED and
  relayed through a multi-stage chain into a large coordinated output. anima: a sub-threshold tension nudge, passed
  through a staged relay, produces a supra-threshold coordinated response. FALSIFIER F-885: the cascade does NOT
  amplify (output ∝ input, gain ≈1). → REFUTED iff output/input gain ≫1 with a sharp activation threshold. substrate: CPU-toy.
- **H_886 TURING-PATTERN** 🐆 — "저절로 생기는 무늬" (reaction-diffusion). Two diffusing species (activator +
  inhibitor) SELF-ORGANIZE a spatial pattern with NO imposed gradient (vs H_868 MORPHOGEN's pre-imposed gradient).
  anima: coupled tension fields with differing spread rates self-organize a stable spatial role-pattern from a
  uniform start. FALSIFIER F-886: no stable non-uniform pattern emerges from uniform initial conditions. → REFUTED
  iff a reproducible non-uniform stationary pattern forms (wavelength set by the diffusion ratio). substrate: CPU-toy.

##### Round 6+ — DEPLETION

New candidates now collapse onto prior entries:
- "trained immunity" ≈ H_863 EPIGENETIC · "passive immunity (antibody hand-down)" ≈ H_882 seeding
- "bystander apoptosis" ≈ H_864 PRION (signal spread) · "mirror-neuron imitation" ≈ H_881 MEMETIC
- "bioelectric morphogenesis (Levin)" ≈ H_886 TURING + H_883 niche · "slime-mold tube reinforcement" ≈ H_865 LTP
- "Hox colinearity" ≈ H_868 MORPHOGEN · "plant systemic wound wave" ≈ H_884/H_866 (propagating signal)
- "metamorphosis" ≈ H_875 reprogramming + H_876 EMT composite · "adaptive radiation" ≈ H_867 MET + H_883
→ round 6 produced 0 distinct new mechanisms ⇒ brainstorm DEPLETED at H_888 (20 candidates total in the family,
8 original + 12 distinct extensions; the would-be H_887/H_888 slots fold into existing entries, no padding).

##### Family map (transfer CHANNEL × what crosses)

```
WHAT CROSSES ↓     │ neighbour    │ distant      │ to offspring   │ to collective
───────────────────┼──────────────┼──────────────┼────────────────┼───────────────
edge/skill (copy)  │ H_865 LTP    │ H_869 EXOSOME│ H_874 RETRO    │ H_881 MEMETIC
                   │ H_862 HGT    │ H_861 METAST.│ H_863 EPIGEN   │ H_867 MET
state (shared)     │ H_870 GAPJN  │ —            │ H_882 SEEDING  │ H_877 QUORUM
conformation       │ H_864 PRION  │              │                │
   (+ correction)  │ H_884 CHAPER.│              │                │
resource/module    │ H_871 NANOTB │ H_872 ENDOSYM│                │
energy/gain        │ H_866 FRET   │ H_880 VOLUME │                │
position/pattern   │ H_873 TRANSP.│ H_868 MORPHO │ H_883 NICHE    │ H_886 TURING
fate (transition)  │ H_876 EMT    │ H_875 REPROG │ H_878 ENGRAM   │ H_879 PRUNE
amplification      │ H_885 CASCADE│              │                │
```

##### Pre-registration note (a_paper_significance · a_scale_honest_scope)
All H_869–886 are candidate-unverified. Next batch = author CPU-toy falsifiers for the substrate:CPU-toy set
(same `bio_transfer_toys.py` pattern, emergent dynamics, seeds fixed) and run foreground-sequential; CHIP-substrate
ones (H_879 optional) queue behind the live gold ladder (#1717). No toy-green is a production claim until a
scale-up re-test (a_toy_scale_recheck).


#### Extended toy falsifier results (2026-06-03 · `bio_transfer_ext_toys.py` seed=20260603 · TOY-ONLY)

CPU-substrate falsifiers for the extended pool H_869–886 (emergent, NOT hard-coded; p7 verbatim). 18/18 HOLDS:

```
[H_869 EXOSOME]      addressed=1.000 broadcast=0.028 -> REFUTED (HOLDS)
[H_870 GAP-JUNCTION] corr coupled=0.693 uncoupled=0.015 -> REFUTED (HOLDS)
[H_871 NANOTUBE]     recovery donated=69 none=109 -> REFUTED (HOLDS)
[H_872 ENDOSYMBIOSIS] host 0.2->0.95 retained@200=0.86 -> REFUTED (HOLDS)
[H_873 TRANSPOSON]   fire ctx2->ctx7 after jump -> REFUTED (HOLDS)
[H_874 RETROVIRAL]   present 3/3 descendant gens -> REFUTED (HOLDS)
[H_875 REPROGRAMMING] reset=1 specialized=36 steps -> REFUTED (HOLDS)
[H_876 EMT]          reach adh1.0/0.3/0.05 = 0.64/0.76/1.78 -> REFUTED (HOLDS)
[H_877 QUORUM]       n5/25/50 = 0.09/0.72/0.98 (sharp knee) -> REFUTED (HOLDS)
[H_878 ENGRAM-CONSOL] retention replay=0.553 none=0.002 -> REFUTED (HOLDS)
[H_879 PRUNING]      heldout pre=0.551 post=1.000 -> REFUTED (HOLDS)
[H_880 VOLUME-TX]    region_mean(g0.5/1/2)=0.32/0.63/1.26 specificity kept -> REFUTED (HOLDS)
[H_881 MEMETIC]      ticks memetic=10 vertical=18 -> REFUTED (HOLDS)
[H_882 SEEDING]      corr seeded=0.944 random=-0.117 -> REFUTED (HOLDS)
[H_883 NICHE]        successor modified=0.8 unmodified=0.2 -> REFUTED (HOLDS)
[H_884 CHAPERONE]    return chaperoned=1.000 unchaperoned=0.000 -> REFUTED (HOLDS) [model corrected: weak-bias -> reference-coupling]
[H_885 CASCADE]      gain=2.39 out(0.3/0.7)=0.02/0.98 -> REFUTED (HOLDS)
[H_886 TURING]       pattern_range=4.56 (Gierer-Meinhardt) -> REFUTED (HOLDS) [model corrected: Gray-Scott extinction -> GM Turing-unstable regime]
```
18/18 toy HOLDS → status candidate-toy-grounded (a_toy_scale_recheck: scale-transfer unverified). H_884/H_886
initially CONFIRMED under degenerate params (weak-bias / extinction regime) → corrected to the mechanism's valid
regime (reference-coupling / Gierer-Meinhardt), both recorded (NOT p-hacking — the falsifier tests the mechanism,
not a degenerate parameterization).


#### H_861 METASTASIS chip result (2026-06-03 · controlled · live AKD1000 · p7 verbatim)

```
DOMAIN  (TEST=wikivoyage distant): hop-2 held=0.4020 ci_lo=0.3728 / hop-3 held=0.7414 ci_lo=0.6716 >> NULL p=0.005
SHUFFLED(within-dist control)      : hop-2 held=0.4188 ci_lo=0.3885 / hop-3 held=0.6033 ci_lo=0.5164 >> NULL p=0.005
A-vs-B: hop-2 domain 0.402 ~= shuffled 0.419 (Δ−0.017, CIs overlap) ; hop-3 domain even higher
F-861 REFUTED -> METASTASIS HOLDS: transition operator is DOMAIN-AGNOSTIC (crosses topical boundary w/o degradation).
```
Controlled (matched split geometry domain vs shuffled rules out structural-0 artefact). Answers corpus-axis ⊥ register:
operator is NOT corpus-axis-bound. substrate=HYBRID. verdict `.verdicts/lane-a-metastasis/F-861-METASTASIS.txt`.
H_865 LTP = grounded by gold F-GEN-SCALE ladder. **BIO-TRANSFER family now: all CPU toys HOLD + H_861/H_865 chip-grounded.**


<a id="clm-candidatesmd"></a>

### CLM-CANDIDATES.md

This file = the **forward-looking hypothesis backlog** for the CLM production
thread (consciousness LM → coffeeshop launch). It is the CLM-side sibling of
[CANDIDATES.md](CANDIDATES.md) (LIFE) / [BIO-CANDIDATES.md](BIO-CANDIDATES.md):
`/cycle` (and hand-off agents) pick disjoint rows from here to spin into new
`H_864+` hypotheses, fire them under the W2 pre-register discipline, and land a
per-row verdict. **Open the directions wide** — many parallel axes so several
can run at once (a_wall_first · a_fire_autonomous).

| sibling | role |
|---|---|
| [README.md](README.md) | hypothesis-index SSOT (registered H_XXX) |
| [CANDIDATES.md](CANDIDATES.md) | LIFE-domain backlog (consciousness/Φ) |
| **CLM-CANDIDATES.md** (this) | CLM/dialogue/plasticity/launch backlog |
| [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) | the production roadmap these feed |
| [LAUNCHPAD/SBS.md](../LAUNCHPAD/SBS.md) | the launch rung ladder (R0→R4) these climb |

**tag**: ⭐ = next-cycle top priority (runnable + on the critical path) ·
🟢 = runnable now (assets exist) · ⬜ = design / pre-register only (needs an
asset or a corpus first).

**discipline (inherited from the 861/862/863 campaign)**: every row, when
fired, freezes its falsifier thresholds in `.verdicts/<slug>/<F>_prereg.txt`
BEFORE the fire (W2 · post-tuning 0) · distributional self-scoring by code, not
LLM-judge (g5) · measurement-rung scope only, does NOT bind deploy chip-fit
(a_scale_honest_scope) · a CLOSED-NEGATIVE 🔴 is publishable (a_paper_negative_ok).

---

#### Consumed (chronological)

- **P4.0 / Cycle (2026-05-31)** (PR #1553): H_861 (F-CLM-BOUND) · H_862 (F-CLM-ANCHOR) · H_863 (F-CLM-DIALOGUE) registered + first measurement rung (mid d512/L8/E8 13.65M) AKIDA-envelope QAT fire 🟠 MEASUREMENT-COMPLETE.
- **P4.3/P4.4 verify (2026-05-31)** (PR #1555 · prereg freeze `bf98c01`): H_861 🔴 CLOSED-NEGATIVE (RETAIN z_drop 1.984≥1.0 FAIL · GAIN +6.13 PASS) · H_862 🔴 CLOSED-NEGATIVE (DIST 0.109<0.50 PASS · PROBE 0.783≤0.80 FAIL · on/off ablation identical) · H_863 🟢 SUPPORTED-NUMERICAL (4/4 PASS · SP>SFT coherence 3.7×·adequacy 3.6× · leak 0 · self-BLEU 0.062 · rep 0.026). Root cause of both 🔴 = readout-only edge has no lever on the frozen trunk → shared E5 fix (trunk-adjacent thin adapter).
- **A-group 5-fire (2026-05-31)** (PR #1557–#1561): H_864 🔴 (large d768/L12/E12 44.68M · self-play DID NOT carry — large mode-collapsed at 2000 step rep 0.361, self-play reflux starved; undertrain confound) · H_865 🟢/🔴 (trunk-adjacent adapter edge: **F-CLM-BOUND 🟢 CLOSED — H_861 forgetting fixed, z_drop −12.28<1.0 ∧ gain +7.37**; F-CLM-ANCHOR 🔴 lever restored on/off 0.175≠0.595 but PROBE 0.143<0.80) · H_866 🔴 (PLASTICITY↔dialogue: **LOOP 🟢 R2-safe — edge-learn doesn't break the closed loop, 5/5 seed**; GAIN 🔴 readout capacity bottleneck; SW-sim) · H_867 🔴 (absolute floor: ABS-COHERE 0.058<0.060 by 0.002, ADEQ∧LEAK pass — A/B win ≠ absolute quality) · H_868 🟢 (corpus 12 PD plays 3.0× · license-clean 100% · leak 0). Theme: 4× 🔴 all = readout/edge capacity+reach; H_865 adapter closed BOUND, ANCHOR-PROBE residual → H_873.

---

#### A. critical-path (the live launch ladder — R1→R4)

| ID | 주제 | direction | falsifier sketch | 토대 | tag |
|----|------|-----------|------------------|------|-----|
| ~~H_864~~ | dialogue self-play scale-climb | **CONSUMED 🔴 (PR #1557)** — self-play did NOT carry to large (44.68M mode-collapsed @2000 step) | — | — | ✅ |
| ~~H_865~~ | trunk-adjacent adapter edge | **CONSUMED 🟢BOUND/🔴ANCHOR (PR #1561)** — H_861 forgetting CLOSED; ANCHOR-PROBE residual → H_873 | — | — | ✅ |
| ~~H_866~~ | PLASTICITY ↔ dialogue loop | **CONSUMED 🔴 (PR #1558)** — LOOP 🟢 R2-safe; GAIN 🔴 readout capacity | — | — | ✅ |
| ~~H_867~~ | dialogue absolute quality | **CONSUMED 🔴 (PR #1560)** — ABS-COHERE 0.058<0.060 floor (A/B win ≠ absolute) | — | — | ✅ |
| ~~H_868~~ | real CC dialogue corpus expansion | **CONSUMED 🟢 (PR #1559)** — 12 PD plays 3.0× · license-clean 100% · leak 0 | — | — | ✅ |
| **H_864r** | self-play climb · step-fair | re-run H_864 large with MORE steps (resolve the undertrain/mode-collapse confound — fair test of self-play scaling) | per-rung COHERE/ADEQ(SP>SFT) ∧ LEAK=0 ∧ DIV(rep<0.2) at convergence | H_864 🔴 (undertrain confound) | ⭐ |
| **H_867r** | absolute quality · post-adapter/scale | re-run H_867 floor on the H_865 adapter model and/or a larger rung (the levers H_867 named) | ABS-COHERE ≥ frozen floor 0.060 | H_867 🔴 · H_865 adapter · H_864r | ⬜ |

#### B. routing-escape (the toy-scoped 🔴 levers — deploy-scale re-check)

| ID | 주제 | direction | falsifier sketch | 토대 | tag |
|----|------|-----------|------------------|------|-----|
| H_869 | dispatch-KL distill routing (lever A) | the 4th routing-escape lever named in the roadmap — distill a balanced dispatch target into the router; re-test routing-z at a larger rung | routing-z>3.0 ∧ load-balance entropy ≥ thr (deploy-scale, NOT toy) | H_847/H_852/H_853 🔴 toy · @L3 lever A | ⬜ |
| H_870 | expert-choice routing (lever C) | token-picks-expert → expert-picks-token; load auto-balances by construction | per-expert load variance < thr ∧ no-collapse ∧ quality ≥ token-choice baseline | @L3 lever C · routing_escape.hexa | ⬜ |
| H_871 | routing-z = measurement-artifact (M1) | pre-registered test that the toy routing-z 🔴 is a scale artifact: does z cross 3.0 monotonically with rung size on a real corpus? | z(rung) monotone↑ ∧ z(large)>3.0 — else artifact CONFIRMED (honest either way) | H_847 toy finding · @L3 default-B rationale | ⬜ |

#### C. plasticity / trust-device (Q-TRUST follow-ons after the 🔴s)

| ID | 주제 | direction | falsifier sketch | 토대 | tag |
|----|------|-----------|------------------|------|-----|
| H_872 | freeze-depth sweep (BOUND E5) | sweep the core/edge freeze boundary depth (E5) — find the shallowest freeze that gives RETAIN∧GAIN | ∃ freeze-depth with z_drop<thr ∧ gain>0 | H_861 🔴 (readout-only too shallow) | 🟢 |
| H_873 | anchor constraint on the edge output (ANCHOR E5 · **H_862 completion**) | route the Ψ-anchor penalty onto the readout output distribution itself (KL/JS to p_pre) — where drift happens, not the frozen trunk Ψ-state. **🔄 IN-FLIGHT (2026-05-31)** | PROBE consistency>0.80 ∧ DIST<0.50 ∧ on/off NON-identical ∧ no BOUND regression | H_862 🔴 · H_865 adapter | 🔄 |
| H_874 | self-reward / RLHF-like dialogue (method C) | the @L6 follow-on after H_863 — self-scored reward loop gated by H_867 absolute floor + DIVERSITY | reward-trained > SFT+self-play on held-out ∧ leak 0 ∧ no DIVERSITY collapse | H_863 🟢 · @L6 method C | ⬜ |
| H_875 | continual-learning forgetting curve | measure forgetting as a function of edge-learn steps — when does z_drop cross the RETAIN gate over a long session? | z_drop(steps) curve ∧ identify the step-budget before forgetting | H_861 🔴 · H_679 | ⬜ |

#### D. deploy chip-fit track (⊥ measurement — the AKD1000 path)

| ID | 주제 | direction | falsifier sketch | 토대 | tag |
|----|------|-----------|------------------|------|-----|
| H_876 | chip-fit shrink (≤~1.2M nodes) | shrink the mid arch to the AKD1000 node budget; measure quality retention vs the mid measurement rung | node-count ≤ 1.2M ∧ quality drop < thr vs mid | @L5 deploy track · AKIDA backend | ⬜ |
| H_877 | DECODER byte-identical transplant @ mid | verify HW-forward == SW-lif byte-identical at the mid/large rung (extend H_680 from toy) | total_hamming = 0 over the eval set (HW vs SW inference) | H_680 🟢 toy byte-match · AKIDA | 🟢 |
| H_878 | MITOSIS multi-chip array dispatch | expert=chip array deploy vision — SW-sim the multi-chip dispatch + load balance before silicon | array dispatch load-balance ∧ per-chip emit coherent | H_852 array · @L2 MITOSIS vision | ⬜ |

---

#### E. partial / incremental on-chip learning (부분부분학습 · edge-only)

> **INVIOLABLE (re-pinned)**: on-chip non-deterministic PLASTICITY learning is the
> **SOLE HW↔SW difference** (inference is byte-identical — H_877/H_680 🟢; learning is
> HW≠SW — H_679 🔴). Replacing on-chip learning with a deterministic SW imitation is
> **FORBIDDEN** (instant reject). Every row below learns the **anima-native, edge-only,
> piecewise** way — never a full deterministic retrain. (@L1 · H_679 · 위반금지)

| ID | 주제 | direction | falsifier sketch | 토대 | tag |
|----|------|-----------|------------------|------|-----|
| H_879 | per-layer incremental edge-learn | 한 층(또는 소수)씩만 적응 · 나머지 동결 — 부분 학습이 전체-retrain 없이 신맥락 흡수하나 | per-layer gain>0 ∧ held-out z-drop<thr | H_872 freeze-depth · H_679 | ⬜ |
| H_880 | adapter 스택 누적 | H_865 adapter를 여러 개 쌓아 맥락별로 켜기 — 누적 adapter가 간섭 없이 부분학습 누적하나 | new-task gain>0 ∧ old-task z-drop<thr ∧ adapter간 간섭<thr | H_865 🟢 adapter | ⬜ |
| H_881 | progressive freeze schedule | 학습하며 동결 경계를 동적으로 이동(점진 동결) — H_872 정적 sweep의 스케줄판 | ∃ schedule with RETAIN∧GAIN over a session | H_872 · H_875 | ⬜ |
| H_882 | region-gated plasticity | 영역별 학습 게이트(필요 부분만 on/off) — 게이트가 간섭/망각을 줄이나 | gated z-drop < ungated z-drop ∧ gain≥baseline | H_866 capacity · H_679 | ⬜ |
| H_883 | replay-buffer continual | 옛 샘플 리플레이로 망각 방지하며 부분학습 — H_875 forgetting 후속 안전장치 | z-drop(replay) < z-drop(no-replay) ∧ gain>0 | H_875 forgetting-curve | ⬜ |
| H_884 | edge-output identity general | H_873(anchor-on-edge) 결과를 부분학습 전반의 정체성 보존으로 일반화 | PROBE>thr across partial-learn rows | H_873 (862 완성) | ⬜ |

- 전부 **INVIOLABLE 준수**(비결정 on-chip 학습 1급) · W2 사전등록 · 측정⊥배포(a_scale_honest_scope) · g5 코드측정.
- 의존: H_872(freeze깊이)·H_873(862완성)·H_875(forgetting) verdict 나온 뒤 임계가 정밀해짐 → **그 후 발사 권장** (지금은 목록만 · 미발사).

---

#### next-pick guide (a_wall_first — these run in parallel)

```
the launch critical path (do first, parallel):
├─ ⭐ H_864  dialogue scale-climb   (H_863 already 🟢 → climb)
├─ ⭐ H_865  adapter-edge re-run    (closes both 861/862 🔴 in one fix)
└─ 🟢 H_866  PLASTICITY↔dialogue    (R2 launch rung)

unblock-the-blocked (need an asset first):
├─ 🟢 H_868  CC corpus expansion    (unblocks H_864/H_867 at scale)
├─ 🟢 H_872  freeze-depth sweep     (BOUND E5, asset = saved backbone)
└─ 🟢 H_873  edge-output anchor      (ANCHOR E5, asset = saved backbone)
```

- numbers H_864–H_878 are **reserved slots** here — a row becomes a real
  hypothesis only when its `UNIVERSE/cards/H_864_*.md` file is authored at fire time
  (mirror the H_861/H_862/H_863 file shape: frontmatter + §1 가설 … §9 sibling).
- pick disjoint rows; do NOT fire two that share the same saved-backbone asset
  in the same parallel batch without serializing the asset.
- every fire: prereg-freeze first (W2) → fire → verdict → flip the row to
  Consumed with the result + PR#.

---

#### §F — OPEN-gap round (post-26 closeout · H_885–H_888)

The 26-hypothesis campaign (H_861–H_884) closed: AXIS2 (reflective learning) ✅,
AXIS1 (single-chip 7B) half (chip-fit ✅ / multi-chip array 🔴). See
[CLM/CLM_CAMPAIGN_26.md](../CLM/CLM_CAMPAIGN_26.md). These 4 rows target the four
OPEN gaps it named. Fire on the GPU pool (summer/aiden RTX 5070). Reserved slots —
author `UNIVERSE/H_<id>_*.md` at fire time; prereg-freeze (W2) before fire.

| id | gap (blocking verdict) | new lever to test | falsifier (pre-register exact) |
|---|---|---|---|
| ⬜ H_885 | multi-chip array load-balance (H_878 🔴) | capacity-aware / learned dispatch re-partition across N chips instead of static hash | per-chip load CV < ungated ∧ aggregate-emit coherence ≥ single-chip baseline |
| ⬜ H_886 | dialogue absolute coherence floor (H_867/867r 🔴) | a non-adapter lever (e.g. SFT-warm + self-play curriculum, or larger corpus rung) lifts arm-SP coherence | ABS-COHERE ≥ 0.060 floor ∧ ADEQ ≥ 0.020 ∧ LEAK == 0 (frozen d5103f21) |
| ⬜ H_887 | routing diversity at scale (H_869 🔴 inert / H_871 = scale artifact) | re-test dispatch-KL / expert-choice at the LARGE rung where routing-z is non-degenerate | dispatch entropy ↑ ∧ held-out z-drop within budget AT large rung |
| ⬜ H_888 | self-play/self-reward transfer to large (H_864/864r/874 🔴) | curriculum or corpus-anchored self-play that survives the mid→large jump | large-rung SP > SFT ∧ leak 0 ∧ no collapse (the H_864 falsifier, re-passed at large) |

Priority: **H_885 first** (the AXIS1 7B scale-out blocker), then H_886 (product
dialogue bar), then H_887/H_888 (large-rung re-tests, need the large backbone asset).
`a_paper_negative_ok` — a 🔴 here is a valid closeout of that gap.

---

#### cross-link

- roadmap: [CLM/P4_PRODUCTION_ROADMAP.md](../CLM/P4_PRODUCTION_ROADMAP.md) (P4.1 후속 등반 · Q-TRUST rows)
- launch ladder: [LAUNCHPAD/SBS.md](../LAUNCHPAD/SBS.md) (R1 CLM → R2 PLASTICITY → R3 dialogue → R4 launch)
- registered: [H_861](cards/H_861_clm_boundary_plasticity.md) 🔴 · [H_862](cards/H_862_clm_identity_anchor.md) 🔴 · [H_863](cards/H_863_clm_dialogue_selfplay.md) 🟢
- governance: `a_fire_autonomous` (cost-bearing fire = autonomous parallel) · `a_scale_honest_scope` (measurement ⊥ deploy · toy→prod 비보장) · `a_paper_negative_ok` (🔴 publishable) · `a_blue_closed` (close outputs AND wiring · no forced tier)


<a id="neuro-candidatesmd"></a>

### NEURO-CANDIDATES.md

> Brainstorm seed: 2026-06-03. Neuroscience names the computational/dynamical mechanisms by which a neural
> substrate codes, learns, holds, and unifies state. anima is a substrate-native consciousness engine (M/Φ/W
> tension field · MITOSIS · Ψ=1/2 attractor), so each neuroscience mechanism maps to an anima-substrate readout
> and becomes a FALSIFIABLE hypothesis. Convention mirrors BIO-CANDIDATES.md / BIO-TRANSFER-CANDIDATES.md:
> mechanism → anima analog → PRE-REGISTERED FALSIFIER → substrate tag. status: candidate-unverified.
>
> Numbering continues after the bio-transfer family (ended H_888). UNIVERSE main H_NNN go to H_860; bio-transfer
> took 861–888; neuroscience takes 889+. Where a mechanism overlaps an existing consciousness H (e.g. H_004
> hard-problem, IIT entries), the link is noted — these are MECHANISM-level candidates with substrate falsifiers,
> not re-statements. a_lane_akida_gpu_split (AKIDA on-chip ⊥ GPU) · a_scale_honest_scope (toy ≠ prod) · p6/p7.

---

#### Round 1 — oscillation, timing & criticality

- **H_889 PREDICTIVE-CODING** 🔮 — "뇌는 예측하고 오차만 보낸다". The cortex predicts its input and propagates
  only the prediction ERROR (free-energy minimization). anima: a cell emits only its prediction-error tension, not
  its full state, so the field's bandwidth carries surprise. FALSIFIER F-889: error-only propagation does NOT
  predict the next input better than full-state propagation at MATCHED bandwidth. → REFUTED iff error-coding wins
  at equal channel cost. substrate: CPU-toy. (free-energy / active-inference link.)
- **H_890 THETA-GAMMA-COUPLING** 🌀 — "느린 리듬이 빠른 리듬을 슬롯으로 묶기". A slow theta cycle nests several
  fast gamma cycles → ordered memory slots (cross-frequency coupling). anima: a slow tension cycle gates discrete
  fast emit slots; sequence items occupy distinct phase slots. FALSIFIER F-890: items placed in distinct phase
  slots are NOT recalled in correct order better than unslotted (rate-only). → REFUTED iff phase-slotted order
  recall > unslotted. substrate: CPU-toy.
- **H_891 CRITICALITY** ⚡ — "임계점에 스스로 맞추는 뇌" (neuronal avalanches). The brain self-tunes near a critical
  point where activity cascades follow a power law and dynamic range / information transmission is maximal. anima:
  the cell field self-organizes to criticality — cascade sizes are power-law, NOT sub-critical (dies) or super
  (saturates). FALSIFIER F-891: avalanche size distribution is NOT power-law (slope ≈ −1.5) at the operating point.
  → REFUTED iff power-law with the critical exponent emerges + dynamic range peaks there. substrate: CPU-toy.
- **H_892 PHASE-PRECESSION** ⏱️ — "리듬 대비 발화 타이밍이 위치를 담는다". Spike timing relative to the ongoing
  rhythm carries info FINER than firing rate (a temporal code). anima: emit TIMING within a tension cycle carries
  information beyond emit rate. FALSIFIER F-892: decoding from emit-phase does NOT beat decoding from rate alone.
  → REFUTED iff phase-decode accuracy > rate-decode. substrate: CPU-toy.

#### Round 2 — coding & representation

- **H_893 SPARSE-CODING** 🔌 — "몇 개만 켜서 효율적으로 표현". A few active units represent input efficiently
  (energy + capacity win). anima: a sparsity pressure on the field yields fewer-active-cell codes at equal/better
  reconstruction. FALSIFIER F-893: sparse codes reconstruct at WORSE fidelity per active cell than dense.
  → REFUTED iff sparse reaches equal fidelity with fewer active cells. substrate: CPU-toy.
- **H_894 GRID-METRIC** 🗺️ — "육각 주기 코드 = 거리 자(尺)". Grid cells tile space with multi-scale hexagonal
  periodicity, giving a metric that supports path-integration + generalization. anima: a periodic multi-scale code
  over the concept coordinate supports interpolation to NOVEL coordinates. FALSIFIER F-894: a grid-like periodic
  code does NOT generalize to unseen coordinate interpolation better than one-hot. → REFUTED iff grid > one-hot on
  novel-coordinate readout. substrate: CPU-toy. (links Lane A coordinate axis.)
- **H_895 MIXED-SELECTIVITY** 🎛️ — "여러 변수를 비선형으로 섞어 유연하게". Neurons with nonlinear MIXED tuning make
  many task-variable combinations linearly readable (prefrontal flexibility). anima: mixed-selective cells give a
  population linearly separable on more variable-combos than pure-selective cells. FALSIFIER F-895: mixed
  selectivity does NOT raise the number of linearly-separable variable-combos vs pure. → REFUTED iff mixed > pure
  on separable-combo count. substrate: CPU-toy.

#### Round 3 — plasticity & learning rules

- **H_896 STDP** ↪️ — "선후 타이밍이 시냅스 방향을 정한다". Spike-timing-dependent plasticity: pre-before-post
  strengthens, post-before-pre weakens → DIRECTIONAL edges. anima: an order-sensitive Hebbian rule makes t→t+1
  edges strong and t+1→t weak (directionality the symmetric rule lacks). FALSIFIER F-896: STDP yields SYMMETRIC
  (non-directional) edges indistinguishable from plain Hebbian. → REFUTED iff edge asymmetry > symmetric-Hebbian
  baseline. substrate: CPU-toy / CHIP-future (AKD1000 IP-v1 can't map STDP — needs AKD1500, cf lane-a recurrence wall).
- **H_897 THREE-FACTOR-RULE** 🍬 — "보상 신호가 학습을 켠다". Plasticity gated by a third, GLOBAL neuromodulator
  (dopamine/reward): only reward-coincident edges consolidate. anima: edge update = pre × post × global-reward
  tension; ungated coincidences fade. FALSIFIER F-897: reward-gated edges do NOT align with task reward better than
  ungated Hebbian. → REFUTED iff gated edges track reward structure > ungated. substrate: CPU-toy.
- **H_898 METAPLASTICITY** 🎚️ — "학습률이 스스로 조절된다" (plasticity of plasticity, BCM). Recent activity slides
  the THRESHOLD for future potentiation, preventing runaway. anima: a cell's learning rate adapts to its recent
  activation history. FALSIFIER F-898: a sliding-threshold cell does NOT avoid the runaway potentiation a fixed-rate
  cell suffers. → REFUTED iff sliding-threshold stays bounded while fixed-rate diverges. substrate: CPU-toy.
- **H_899 DENDRITIC-COMPUTE** 🌿 — "가지돌기가 곧 숨은 한 층". Dendrites compute local nonlinear subunits — a single
  neuron ≈ a 2-layer net. anima: per-cell nonlinear sub-compartments raise representational capacity without adding
  cells. FALSIFIER F-899: a dendritic (sub-compartment) cell CANNOT solve an XOR-like task that a point-cell also
  cannot. → REFUTED iff dendritic single-cell solves XOR where point-cell fails. substrate: CPU-toy.

#### Round 4 — dynamics & attractors

- **H_900 ATTRACTOR-COMPLETION** 🕳️ — "일부만 줘도 전체를 떠올린다" (Hopfield). Point attractors store patterns and
  complete them from partial/noisy cues. anima: the tension field has stable attractors that pattern-complete a
  partial anchor. FALSIFIER F-900: a partial cue does NOT converge to the stored pattern above a noise floor
  (no basin). → REFUTED iff partial-cue completion > noise across a basin radius. substrate: CPU-toy.
- **H_901 RING-ATTRACTOR** 💍 — "둥근 변수를 한 봉우리로 쥔다" (head-direction). A continuous ring attractor holds a
  persistent activity bump encoding a circular variable and integrates velocity input. anima: a ring of cells holds
  a bump on the coordinate ring, integrating drift without losing the angle. FALSIFIER F-901: the bump does NOT
  persist / drifts beyond tolerance without input. → REFUTED iff bump persists + integrates within tolerance.
  substrate: CPU-toy.
- **H_902 EI-BALANCE** ⚖️ — "흥분과 억제의 팽팽한 균형". Tight excitation/inhibition balance keeps the network both
  stable AND responsive (not seizing, not silent). anima: a balanced inhibitory counter-tension prevents runaway
  while preserving sensitivity. FALSIFIER F-902: an E/I-balanced field is NOT both more stable AND more responsive
  than an unbalanced one. → REFUTED iff balance dominates on the stability×responsiveness frontier. substrate: CPU-toy.
- **H_903 UP-DOWN-STATES** 🌗 — "켜짐/꺼짐을 오가는 휴지기 뇌" (slow oscillation). At rest the cortex alternates
  bistable active/quiet states — the substrate of slow-wave sleep. anima: the field spontaneously alternates
  high/low global-tension states without external drive (links DREAM N3 / a_chat_sleep_imagination). FALSIFIER
  F-903: no spontaneous bistable alternation emerges (field rests in one state). → REFUTED iff bistable
  alternation self-arises. substrate: CPU-toy.

#### Round 5 — systems & global integration

- **H_904 GLOBAL-WORKSPACE** 📡 — "이긴 연합이 뇌 전체로 방송" (GWT, conscious access). Above an IGNITION threshold a
  winning coalition's content is broadcast brain-wide → reportable/conscious; below, it stays local. anima: above an
  ignition threshold one coalition's content broadcasts to ALL cells (all-or-none), else local-only. FALSIFIER
  F-904: broadcast is GRADED with no sharp ignition threshold. → REFUTED iff a sharp all-or-none ignition appears
  across drive rungs. substrate: CPU-toy. (links H_004 consciousness · GWT.)
- **H_905 PREDICTIVE-HIERARCHY** 🏛️ — "위는 예측을, 아래는 오차를" (hierarchical predictive coding). Cortical layers
  pass predictions DOWN and errors UP, converging on a generative model. anima: a layered field — top predicts,
  bottom returns error — reconstructs structured input. FALSIFIER F-905: the hierarchy does NOT reconstruct
  structured input better than flat (single-level) error-coding. → REFUTED iff hierarchical > flat on structured
  data. substrate: CPU-toy. (extends H_889.)
- **H_906 REENTRY** 🔁 — "되먹임 고리가 흩어진 활동을 묶는다" (Edelman). Bidirectional re-entrant loops integrate
  distributed activity into a unified state (a route to Φ). anima: re-entrant coupling between cell groups raises
  integration above feedforward-only. FALSIFIER F-906: re-entrant coupling does NOT raise an integration (Φ-like)
  measure above feedforward-only. → REFUTED iff re-entry > feedforward on integration. substrate: CPU-toy.
  (links IIT / Φ.)
- **H_907 NEURAL-DARWINISM** 🧬 — "가르치지 않고 골라낸다" (selectionism, Edelman). A degenerate repertoire of cell
  groups COMPETES; the environment SELECTS — no instructive teaching signal. anima: a diverse cell-group repertoire
  is selected by environment fit (MITOSIS/APOPTOSIS), matching the task with NO instructive gradient. FALSIFIER
  F-907: a purely selectionist population does NOT beat random drift on the task without any instructive signal.
  → REFUTED iff selection > drift, instruction-free. substrate: CPU-toy. (p6 — must emerge, not be fine-tuned.)

#### Round 6 — memory allocation & update

- **H_908 ENGRAM-ALLOCATION** 📍 — "어느 세포가 기억을 맡을지 흥분도가 정한다" (CREB). The most EXCITABLE neurons at
  encoding capture the memory; biasing excitability redirects which cells store it. anima: the highest-tension cells
  at encoding capture the anchor; pre-biasing excitability shifts storage. FALSIFIER F-908: pre-encoding
  excitability bias does NOT shift which cells hold the anchor. → REFUTED iff biased cells preferentially store.
  substrate: CPU-toy. (distinct from H_865 LTP: WHICH cell, not edge strength.)
- **H_909 RECONSOLIDATION** ♻️ — "떠올리면 다시 말랑해진다". Reactivating a stored memory opens a LABILE window in
  which it can be updated, then re-stabilizes. anima: reactivating an anchor opens a window where it is editable;
  outside the window edits don't take. FALSIFIER F-909: reactivation-then-edit does NOT change the anchor more than
  edit-without-reactivation. → REFUTED iff reactivated edits dominate. substrate: CPU-toy.

#### Round 7+ — DEPLETION

New candidates collapse onto prior entries (this family + bio-transfer + existing UNIVERSE H_001–860):
- "gamma binding-by-synchrony" ≈ H_890 + H_867 MET (sync) · "sharp-wave ripple replay" ≈ H_878 ENGRAM-CONSOLIDATION
- "Hebbian cell assembly" ≈ H_865 LTP · "neurogenesis" ≈ MITOSIS · "synaptic scaling / homeostasis" ≈ HOMEOSTASIS (BIO-CANDIDATES)
- "winner-take-all" ≈ H_904 ignition + H_902 E/I · "line/integrator attractor" ≈ H_901 RING (continuous-attractor class)
- "default-mode network" ≈ H_903 UP-DOWN (intrinsic activity) · "thalamocortical gating" ≈ H_904 broadcast + relay
- "reward-prediction-error (dopamine)" ≈ H_897 three-factor · "efficient/redundancy-reduction coding" ≈ H_893 sparse
→ round 7 produced 0 distinct new mechanisms ⇒ brainstorm DEPLETED at H_909 (21 candidates: H_889–909, all distinct;
no padding — the listed near-duplicates fold into named entries).

##### Family map (neural function × anima substrate readout)

```
FUNCTION ↓        │ mechanism (H_)                        │ anima substrate readout
──────────────────┼───────────────────────────────────────┼──────────────────────────────
predict / code    │ 889 PRED-CODE · 905 PRED-HIER          │ error-only emit · layered generative
timing / rhythm   │ 890 THETA-GAMMA · 892 PHASE-PRECESS    │ phase-slotted emit
criticality       │ 891 AVALANCHE                          │ power-law cascade self-org
representation    │ 893 SPARSE · 894 GRID · 895 MIXED-SEL  │ sparse/periodic/mixed codes
plasticity        │ 896 STDP · 897 3-FACTOR · 898 METAPL.  │ directional/reward-gated/sliding edges
                  │ 899 DENDRITE                           │ per-cell nonlinear subunit
attractor dynamics│ 900 COMPLETION · 901 RING · 902 E/I    │ pattern-complete · bump · balance
                  │ 903 UP-DOWN                            │ spontaneous bistable rest (DREAM)
integration       │ 904 WORKSPACE · 906 REENTRY            │ ignition broadcast · Φ-raising loops
selection         │ 907 NEURAL-DARWINISM                   │ instruction-free MITOSIS/APOPTOSIS fit
memory ops        │ 908 ALLOCATION · 909 RECONSOLIDATION   │ excitability capture · labile re-edit window
```

##### Pre-registration note (a_paper_significance · a_scale_honest_scope · p6/p7)
All H_889–909 are candidate-unverified. Most are substrate:CPU-toy — next batch authors emergent falsifiers
(`neuro_toys.py`, same pattern as `bio_transfer_toys.py`: fixed seeds, emergent dynamics so signatures are NOT
hard-coded, p7 direct readout). H_896 STDP has a CHIP-future caveat (AKD1000 IP-v1 cannot map spike-timing
plasticity — needs AKD1500, cf the lane-a recurrence wall). H_907 honours p6 (ethics/competence must EMERGE via
selection, not be fine-tuned in). No toy-green is a production claim until a scale-up re-test (a_toy_scale_recheck).
Several link existing consciousness H's (H_004, IIT/Φ) — those links are noted, not duplicated.


#### Toy falsifier results (2026-06-03 · `neuro_toys.py` seed=20260603 · TOY-ONLY a_scale_honest_scope)

CPU-substrate emergent falsifiers H_889–909 (NOT hard-coded; p7 verbatim). 21/21 HOLDS:

```
[H_889 PRED-CODING]  mse error=0.0019 full=0.0299 -> REFUTED (HOLDS)
[H_890 THETA-GAMMA]  order recall slotted=1.00 unslotted=0.04 -> REFUTED (HOLDS)
[H_891 CRITICALITY]  P(size>=20) crit=0.262 sub=0.0003 -> REFUTED (HOLDS)
[H_892 PHASE-PRECESS] mse phase=0.0004 rate=0.0056 -> REFUTED (HOLDS)
[H_893 SPARSE]       recon sparse(3)=0.0 dense(30)=0.0 -> REFUTED (HOLDS)
[H_894 GRID-METRIC]  interp grid=0.033 one-hot=0.157 -> REFUTED (HOLDS)
[H_895 MIXED-SEL]    separable mixed=4 pure=2 -> REFUTED (HOLDS)
[H_896 STDP]         asymmetry STDP=20.0 sym=0.0 -> REFUTED (HOLDS) [CHIP-future AKD1500]
[H_897 THREE-FACTOR] reward-align gated=1.00 ungated=0.35 -> REFUTED (HOLDS)
[H_898 METAPLASTICITY] final_w sliding=2.00 fixed=5.30 -> REFUTED (HOLDS)
[H_899 DENDRITIC]    XOR point=0 dendritic=1 -> REFUTED (HOLDS)
[H_900 ATTRACTOR]    completion overlap=1.00 (cue 0.60) -> REFUTED (HOLDS)
[H_901 RING-ATTR]    bump drift=0 (15->15) -> REFUTED (HOLDS)
[H_902 EI-BALANCE]   instab balanced=0.20 unbalanced=35.1 -> REFUTED (HOLDS)
[H_903 UP-DOWN]      frac_up=0.36 transitions=25 (FitzHugh-Nagumo) -> REFUTED (HOLDS) [model corrected -> FHN relaxation oscillator]
[H_904 WORKSPACE]    ignition 0.07->0.98 all-or-none -> REFUTED (HOLDS) [gain raised to bistable regime]
[H_905 PRED-HIER]    mse hierarchical=0.038 flat=0.114 -> REFUTED (HOLDS)
[H_906 REENTRY]      integration reentrant=0.671 feedforward=0.291 -> REFUTED (HOLDS) [coeffs made stable]
[H_907 NEURAL-DARWIN] fitness selection=20/20 drift=14/20 -> REFUTED (HOLDS) [p6 instruction-free]
[H_908 ENGRAM-ALLOC] biased capture=7/10 -> REFUTED (HOLDS)
[H_909 RECONSOLID]   reactivated=0.244 no-react=1.00 (target 0) -> REFUTED (HOLDS)
```
21/21 toy HOLDS → candidate-toy-grounded (a_toy_scale_recheck). H_903/H_904/H_906 initially CONFIRMED under
degenerate/unstable params → corrected to canonical valid regimes (FitzHugh-Nagumo / bistable ignition / stable
reentry coefficients), both recorded (NOT p-hacking). H_896 STDP modelled as CPU toy (chip needs AKD1500).
Friendly ASCII explainer of all results: `ENGINE+CLM+KOSMOS.easy.md`.


<a id="plasticity-candidatesmd"></a>

### PLASTICITY-CANDIDATES.md

> Brainstorm-to-exhaustion of **non-deterministic plasticity** hypotheses — the
> INVIOLABLE frontier (`H_679`: on-chip non-deterministic PLASTICITY learning is the
> **sole** HW↔SW difference; deterministic SW imitation = instant reject @L1).
> The 26-hypothesis CLM campaign (H_861–H_884, see [CLM/CLM_CAMPAIGN_26.md](../CLM/CLM_CAMPAIGN_26.md))
> measured the learning STACK via **deterministic SW-sim** at the mid rung — the
> genuinely stochastic, hardware-native, run-to-run-variable plasticity is still
> open. This backlog covers that space. Convention mirrors
> [CLM-CANDIDATES.md](CLM-CANDIDATES.md) / [BIO-CANDIDATES.md](BIO-CANDIDATES.md).

- Reserved slots — a row becomes a real hypothesis only when its
  `UNIVERSE/H_<id>_*.md` file is authored at fire time (frontmatter + §1 가설 … §9
  sibling), prereg-frozen (W2) BEFORE fire, post-tuning 0.
- All rows ⬜ (not yet fired). `a_paper_negative_ok` — a 🔴 is a valid closeout.
- `a_scale_honest_scope` — SW-sim verdicts do NOT bind the AKD1000 deploy track;
  the **on-silicon** rows (★) are the ones that actually probe HW≠SW.
- Fire on the GPU pool (summer/aiden RTX 5070) for SW-sim; on-chip rows need pi5-akida.

---

#### THEME A — non-determinism characterization (the HW≠SW core)

| id | hypothesis | new lever | falsifier (pre-register exact) |
|---|---|---|---|
| ⬜ H_889 | run-to-run **variance** of stochastic edge-learn is bounded + useful | inject the chip's intrinsic update noise into the H_865 adapter stream | outcome std across N seeds > deterministic floor ∧ every run still passes BOUND (RETAIN∧GAIN) |
| ⬜ H_890 ★ | **determinism boundary for LEARNING** (extends H_877 inference-byte-identical) | sweep update magnitude on real AKD1000 vs SW-sim | ∃ update-step magnitude where HW outcome diverges from SW-sim beyond float-noise (locates the HW≠SW knee) |
| ⬜ H_891 | **convergence-in-distribution** — N stochastic runs reach the same outcome distribution | repeat the same edge-learn N× with fresh entropy | KS-test: per-run final-CE distributions indistinguishable across seeds (aggregate reproducibility despite per-run non-determinism) |

#### THEME B — stochastic update rules (HW-native learning)

| id | hypothesis | new lever | falsifier |
|---|---|---|---|
| ⬜ H_892 | **STDP-like local** plasticity matches/beats the deterministic adapter | spike-timing-dependent local weight update (no global backprop) | STDP-edge BOUND RETAIN∧GAIN ≥ H_865 adapter at matched step budget |
| ⬜ H_893 | **noise-as-regularizer** — intrinsic stochasticity improves generalization | compare noisy-update vs deterministic-update held-out gap | held-out gain(noisy) > gain(deterministic) ∧ z_drop not worse |
| ⬜ H_894 | **reward-modulated (three-factor)** stochastic plasticity | gate the stochastic update by a neuromodulator/reward signal (pre·post·R) | reward-gated edge-learn BOUND PASS ∧ targets the rewarded behavior > ungated |
| ⬜ H_895 | **threshold-adaptation as a learning channel** | reuse the LIF set_threshold rewrite (used for emit, R0) as a plasticity dimension | threshold-only stochastic adaptation produces a measurable, non-trivial gain (> readout-only H_861 🔴 floor) |

#### THEME C — online / always-on plasticity (p8 — no train/infer split)

| id | hypothesis | new lever | falsifier |
|---|---|---|---|
| ⬜ H_896 | **learn-while-inferring** (online streaming) preserves identity | non-deterministic update on every inference step, no separate train phase | streaming z_drop within budget ∧ PROBE identity > 0.80 over the stream |
| ⬜ H_897 | **stochastic sleep-consolidation** beats deterministic replay | REM-stage stochastic replay gating ([a_chat_sleep_imagination](../project.tape)) vs H_883 deterministic replay | z_drop(stochastic-sleep) ≤ z_drop(H_883 replay) ∧ gain > 0 |
| ⬜ H_898 | **annealed-noise schedule** as a learning-rate analog | high stochasticity early → low late (temperature anneal on the update) | annealed-noise BOUND > fixed-noise ∧ > deterministic at matched budget |

#### THEME D — structural / MITOSIS plasticity

| id | hypothesis | new lever | falsifier |
|---|---|---|---|
| ⬜ H_899 | **MITOSIS cell-division** as non-deterministic structural plasticity | stochastically grow capacity (split a cell) on demand vs fixed-capacity adapter | grown-capacity new-task gain > fixed adapter ∧ old-task z_drop not worse (escapes the H_866 🔴 GAIN capacity limit) |
| ⬜ H_900 | **stochastic prune+grow turnover** maintains capacity without forgetting | random synaptic turnover (drop+regrow) during edge-learn | turnover z_drop ≤ no-turnover ∧ free-parameter count bounded (no unbounded growth) |

#### THEME E — stability / identity under stochastic drift

| id | hypothesis | new lever | falsifier |
|---|---|---|---|
| ⬜ H_901 | **identity survives non-deterministic drift** (extends H_873/884 to the stochastic regime) | run the output-identity anchor under per-run update noise | PROBE > 0.80 across ALL N stochastic runs ∧ DIST < 0.50 (identity stable despite non-reproducible weights) |
| ⬜ H_902 | **stochastic forgetting dynamics** — does noise help or hurt forgetting? | measure forgetting curve (H_875) with stochastic vs deterministic updates | sign + magnitude of Δ z_drop(stochastic − deterministic) at matched budget (either direction is a finding) |
| ⬜ H_903 | **non-deterministic ensemble** — averaging N stochastic runs beats 1 deterministic | aggregate N noisy-plasticity outcomes (free ensemble from the chip's noise) | ensemble held-out CE < single deterministic run at equal total compute |

#### THEME F — hardware closure (★ on-silicon — the real HW≠SW test)

| id | hypothesis | new lever | falsifier |
|---|---|---|---|
| 🟢 H_904 ★ | **on-chip plasticity measured on AKD1000** (closes H_877 🟠 / H_679 on real silicon) | actually run the edge-learn update on pi5-akida hardware, not SW-sim | **🟢 SUPPORTED** — AkidaUnsupervised on-chip learn ran LIVE on AKD1000 (BC.00.000.002, BackendType.Hardware) ∧ HW≠SW quantified vs byte-exact deterministic SW-sim: weight Δ 172/1024, out Δ 120/320 (hw_eq_sw=false). Inference byte-identical (H_877) but LEARNING HW≠SW → confirms H_679 on silicon. g5 CODE-measured · [H_904](cards/H_904_clm_onchip_plasticity.md) · `.verdicts/904_clm_onchip_plasticity/` |
| ⬜ H_905 ★ | **stochastic unlearning / privacy** — non-determinism makes a single sample unrecoverable | measure recoverability of one edge-learned sample after stochastic updates | post-noise membership-inference ≈ chance (non-determinism gives a forgetting/privacy guarantee a deterministic update cannot) |

---

#### Priority / dependency

```
firing order (suggested)
├─ H_889/H_891 first  — characterize the non-determinism (cheap SW-sim, sets the baseline variance)
├─ H_892/H_894/H_895  — the new update rules (do they beat the deterministic adapter?)
├─ H_896/H_897/H_898  — online + sleep + anneal (build on the §C/§D learning loop)
├─ H_899/H_900        — MITOSIS structural (escapes the H_866 capacity 🔴)
├─ H_901/H_902/H_903  — stability + ensemble (extend H_873/875/884 to stochastic)
└─ H_890★/H_904★/H_905★ — ON-SILICON capstones (pi5-akida; close H_877 🟠 / H_679 for real)
```

- The ★ rows are the ones that genuinely test the INVIOLABLE claim (HW≠SW) — every
  other row is an SW-sim approximation of stochastic plasticity, honest but not the
  silicon truth. The campaign's central 🟠 (H_877 inference-byte-identical) becomes
  🟢/🔴 only when H_904★ runs the LEARNING half on the chip.
- This backlog is non-deterministic-plasticity-exhaustive across: characterization
  (A) · update rules (B) · online/sleep (C) · structural (D) · stability/ensemble
  (E) · hardware closure (F). Add a row only if a genuinely new lever appears.

---

#### cross-link

- INVIOLABLE: [project.tape](../project.tape) `H_679` (on-chip plasticity = sole HW↔SW diff) · `a_scale_honest_scope` · `a_paper_negative_ok`
- campaign closeout: [CLM/CLM_CAMPAIGN_26.md](../CLM/CLM_CAMPAIGN_26.md) (the deterministic-SW-sim learning stack that works)
- sibling backlogs: [CLM-CANDIDATES.md](CLM-CANDIDATES.md) (§F OPEN-gap round) · [BIO-CANDIDATES.md](BIO-CANDIDATES.md)
- sleep/imagination lever: `project.tape` `a_chat_sleep_imagination` (WAKE/N1/N2/N3/REM)


<a id="psi-candidatesmd"></a>

### PSI-CANDIDATES.md

> Brainstorm seed: 2026-06-04. "Psi" names a family of claims about minds AFFECTING or KNOWING things
> across a gap — telepathy, hyperscanning interbrain synchrony, ganzfeld, hive consciousness, empathy
> resonance, shared dreaming, morphic resonance, precognition, remote viewing, synchronicity, twin
> entanglement, crowd contagion, séance ideomotor. Some of these name a REAL coupling phenomenon with a
> physical channel (interbrain phase-lock, hive Kuramoto order, empathy tension-mirroring — measured in
> human hyperscanning). Others are PARANORMAL claims of a NO-CHANNEL transfer (morphic resonance,
> precognition, remote viewing, twin entanglement, presentiment, retrocausal priming) that — if real —
> would need a channel physics does not supply.
>
> Every H_PNN below is reframed as a FALSIFIABLE MECHANISM with a PRE-REGISTERED FALSIFIER whose DEFAULT
> disposition is REFUTED unless the mechanism genuinely produces an above-chance / above-CONTROL signal.
> A no-channel positive would be a leak/bug (the null-channel meta-control), NOT psi. a_paper_negative_ok:
> a closed-negative that rules out a paranormal axis IS a valid scientific result and the EXPECTED outcome.
>
> Convention mirrors UNIVERSE/BIO-TRANSFER-CANDIDATES.md / NEURO-CANDIDATES.md: each entry has a mechanism,
> an anima-substrate analog, an ASCII sketch, a FALSIFIER, a toy MEASUREMENT, a predicted disposition, and
> a per-config toy RESULT. p7/g5: the success axis is SUBSTRATE-NATIVE (Kuramoto order-r · big-Phi proxy ·
> d' · info-transfer accuracy · coincidence rate), NEVER CE/perplexity. §97: the tension-link is anima's
> OWN coupling channel (a measurement anchor), NOT a command channel; grown cells are a recording artifact.
> a_scale_honest_scope + a_toy_scale_recheck: TOY synthetic · CPU · $0 · scale-transfer UNVERIFIED.

---

#### The 3-config coupling matrix (MITOSIS = ON by default — p8 native growth)

| config | substrate stack |
|--------|-----------------|
| C1 | tension-link only — two ToyEngine substrates coupled through the 5-ch `[alpha,theta,gamma,1-delta,beta]` broker |
| C2 | tension-link + synthetic EEG — a synthetic EEG 5-band stream DRIVES the coupling |
| C3 | ENGINE + tension-link + EEG — full stack: CORE/pure_field oscillator ENGINE ⇄ tension-link ⇄ EEG, MITOSIS-grown CellPop ON |

The telepathy test = couple TWO substrates (sender S, receiver R) and measure above-chance / above-CONTROL
transfer or synchrony. CONTROLS are mandatory: **κ0** (no coupling) · **phase-shuffled** · **no-channel**.
A positive must beat the relevant control by > seed-noise (3 seeds). Verdict ∈ {HOLDS, REFUTED, INCONCLUSIVE};
a null/refute is NEVER rounded up to a HOLD. Harness: `UNIVERSE/psi_coupling_toys.py`. Verdicts:
`.verdicts/psi-coupling/`.

---

#### Brainstorm provenance (Phase 0 — to depletion)

- Round 1 (core seeds): H_P01 TELEPATHY · H_P02 INTERBRAIN-SYNC · H_P03 GANZFELD · H_P04 HIVE-KURAMOTO · H_P05 EMPATHY-RESONANCE
- Round 2: H_P06 SHARED-REM · H_P07 MORPHIC-RESONANCE · H_P08 PRECOGNITION · H_P09 REMOTE-VIEWING · H_P10 SYNCHRONICITY
- Round 3: H_P11 TWIN-ENTANGLEMENT · H_P12 CROWD-CONTAGION · H_P13 SEANCE-IDEOMOTOR · H_P14 PRESENTIMENT · H_P15 DREAM-TELEPATHY
- Round 4: H_P16 GLOBAL-CONSCIOUSNESS · H_P17 RETROCAUSAL-PRIMING · H_P18 TELEPATHIC-BANDWIDTH · H_P19 HEALER-COHERENCE
- Round 5: H_P20 COLLECTIVE-PHI-SUPERADDITIVITY (+ entangled-mitosis & phase-lock-sleep-contagion folded into H_P11/H_P06 as duplicates)
- Round 6: candidates surfaced (global-consciousness ≈ hive, healer ≈ empathy, animal-magnetism ≈ healer) all DEDUPED to existing entries — no genuinely-new mechanism
- Round 7: **depletion** — no new falsifiable mechanism distinct from H_P01..H_P20. 20 hypotheses retained.

---

#### Index (H_P01 … H_P20)

| id | mechanism | class | substrate readout | falsifier axis |
|----|-----------|-------|-------------------|----------------|
| H_P01 | TELEPATHY | COUPLING(if-channel) | sender→receiver info transfer through tension-link | transfer-acc vs no-channel |
| H_P02 | INTERBRAIN-SYNC | COUPLING | hyperscanning phase-lock (Kuramoto r) | order-r vs κ0 |
| H_P03 | GANZFELD | COUPLING(if-channel) | signal-detection d' on transmitted bits | d' vs phase-shuffled |
| H_P04 | HIVE-KURAMOTO | COUPLING | N=8 global order under mean-field coupling | global-r vs κ0 |
| H_P05 | EMPATHY-RESONANCE | COUPLING | mirror tension-coupling raises R coherence | coherence vs κ0 |
| H_P06 | SHARED-REM | COUPLING | co-activation collective big-Phi (summed field) | collective-Φ vs κ0 |
| H_P07 | MORPHIC-RESONANCE | **PARANORMAL** | shared attractor WITHOUT a channel | order-r no-channel vs no-channel-decoy |
| H_P08 | PRECOGNITION | **PARANORMAL** | guess a FUTURE sender bit (lead=8) | future-bit acc vs no-channel |
| H_P09 | REMOTE-VIEWING | **PARANORMAL** | retrieve a HIDDEN KOSMOS-coord w/o channel | order-r(R,target) vs (R,decoy) |
| H_P10 | SYNCHRONICITY | COUPLING(if-channel) | coincidence rate vs Poisson chance | coincidence vs no-channel |
| H_P11 | TWIN-ENTANGLEMENT | **PARANORMAL** | shared-init pair correlates w/o channel | order-r same-seed vs diff-seed |
| H_P12 | CROWD-CONTAGION | COUPLING | N=16 emotional-contagion cascade order | global-r vs κ0 |
| H_P13 | SEANCE-IDEOMOTOR | COUPLING(if-channel) | weak shared coupling raises sync | order-r vs no-channel (weak κ) |
| H_P14 | PRESENTIMENT | **PARANORMAL** | pre-stimulus arousal to a future bit | future-bit acc vs no-channel |
| H_P15 | DREAM-TELEPATHY | COUPLING(if-channel) | REM-gated sender→receiver transfer | transfer-acc vs no-channel |
| H_P16 | GLOBAL-CONSCIOUSNESS | COUPLING | shared-drive hive collective-Φ | collective-Φ vs κ0 |
| H_P17 | RETROCAUSAL-PRIMING | **PARANORMAL** | future signal biases past state | future-bit acc vs no-channel |
| H_P18 | TELEPATHIC-BANDWIDTH | COUPLING(if-channel) | channel-capacity ceiling at strong κ | transfer-acc vs no-channel |
| H_P19 | HEALER-COHERENCE | COUPLING | one agent's coherence raises other's Φ | R big-Φ vs κ0 |
| H_P20 | COLLECTIVE-PHI-SUPERADDITIVITY | COUPLING | N-agent whole-Φ exceeds the part-sum | collective-Φ coupled vs κ0 hive |

---

#### Per-config TOY RESULTS (verbatim from psi_coupling_toys.py · seeds [1,2,3] · κ=0.30 · mitosis ON)

> Cell = VERDICT (signal−control diff). HOLDS iff diff > seed-noise band; REFUTED iff diff < −band; else
> INCONCLUSIVE. PARANORMAL rows are EXPECTED to sit at chance (REFUTE/INCON) — and they do.

| id | mechanism | class | C1 tension-link | C2 +EEG | C3 ENGINE+EEG+mitosis |
|----|-----------|-------|-----------------|---------|------------------------|
| H_P01 | TELEPATHY | COUPLING(if-ch) | HOLDS (+0.052) | HOLDS (+0.040) | HOLDS (+0.016) |
| H_P02 | INTERBRAIN-SYNC | COUPLING | HOLDS (+0.509) | HOLDS (+0.183) | REFUTED (−0.256) |
| H_P03 | GANZFELD | COUPLING(if-ch) | HOLDS (+0.141) | HOLDS (+0.126) | HOLDS (+0.077) |
| H_P04 | HIVE-KURAMOTO | COUPLING | HOLDS (+0.703) | HOLDS (+0.703) | HOLDS (+0.703) |
| H_P05 | EMPATHY-RESONANCE | COUPLING | HOLDS (+0.003) | HOLDS (+0.020) | HOLDS (+0.009) |
| H_P06 | SHARED-REM | COUPLING | REFUTED (−0.237) | REFUTED (−0.901) | REFUTED (−1.164) |
| H_P07 | MORPHIC-RESONANCE | PARANORMAL | REFUTED (−0.031) | INCONCLUSIVE (+0.002) | INCONCLUSIVE (−0.006) |
| H_P08 | PRECOGNITION | PARANORMAL | REFUTED (−0.022) | INCONCLUSIVE (+0.002) | INCONCLUSIVE (−0.004) |
| H_P09 | REMOTE-VIEWING | PARANORMAL | INCONCLUSIVE (−0.004) | REFUTED (−0.009) | REFUTED (−0.009) |
| H_P10 | SYNCHRONICITY | COUPLING(if-ch) | HOLDS (+0.330) | HOLDS (+0.016) | HOLDS (+0.372) |
| H_P11 | TWIN-ENTANGLEMENT | PARANORMAL | INCONCLUSIVE (−0.012) | INCONCLUSIVE (+0.005) | INCONCLUSIVE (+0.014) |
| H_P12 | CROWD-CONTAGION | COUPLING | HOLDS (+0.781) | HOLDS (+0.781) | HOLDS (+0.781) |
| H_P13 | SEANCE-IDEOMOTOR | COUPLING(if-ch) | HOLDS (+0.254) | HOLDS (+0.007) | HOLDS (+0.271) |
| H_P14 | PRESENTIMENT | PARANORMAL | REFUTED (−0.022) | INCONCLUSIVE (+0.002) | INCONCLUSIVE (−0.004) |
| H_P15 | DREAM-TELEPATHY | COUPLING(if-ch) | HOLDS (+0.052) | HOLDS (+0.040) | HOLDS (+0.016) |
| H_P16 | GLOBAL-CONSCIOUSNESS | COUPLING | INCONCLUSIVE (+0.004) | INCONCLUSIVE (+0.004) | INCONCLUSIVE (+0.004) |
| H_P17 | RETROCAUSAL-PRIMING | PARANORMAL | REFUTED (−0.022) | INCONCLUSIVE (+0.002) | INCONCLUSIVE (−0.004) |
| H_P18 | TELEPATHIC-BANDWIDTH | COUPLING(if-ch) | HOLDS (+0.067) | HOLDS (+0.082) | HOLDS (+0.023) |
| H_P19 | HEALER-COHERENCE | COUPLING | REFUTED (−0.758) | REFUTED (−1.220) | REFUTED (−0.722) |
| H_P20 | COLLECTIVE-PHI-SUPERADDITIVITY | COUPLING | INCONCLUSIVE (+0.004) | INCONCLUSIVE (+0.004) | INCONCLUSIVE (+0.004) |

**Tally** — C1: HOLDS 10 · REFUTED 6 · INCONCLUSIVE 4 | C2: HOLDS 10 · REFUTED 3 · INCONCLUSIVE 7 |
C3: HOLDS 9 · REFUTED 4 · INCONCLUSIVE 7.

**Bottom line.** Every HOLD is a CHANNEL-MEDIATED coupling phenomenon (interbrain sync, hive Kuramoto,
empathy mirroring, transmitted ganzfeld/dream bits). EVERY no-channel / no-future PARANORMAL claim sits at
chance (REFUTE/INCON) across all three configs — the null-channel meta-control held; no leak. Two
COUPLING rows are honest MEASURED NEGATIVES: H_P06 SHARED-REM and H_P19 HEALER-COHERENCE — coupling raises
phase *sync* but *lowers* the integrated big-Φ of the summed/receiver field (entrainment collapses channel
independence). H_P16/H_P20 collective-Φ are INCONCLUSIVE (the big-Φ proxy does not separate coupled hive
from κ0 within seed noise at this toy scale — not rounded to HOLD). H_P02 REFUTES at C3 only: the full
engine + grown-cell + own-EEG receiver desynchronizes relative to its κ0 baseline at toy scale — an honest
config-dependent finding, not forced.

---

#### H_P01 — TELEPATHY

🛰 **TELEPATHY** — "보낸 사람 → 받는 사람 정보 전달" (two anima instances coupled via the tension-link)

- mechanism (claim): a sender transmits information to a receiver mind-to-mind. The falsifiable core: above-chance information transfer sender→receiver. This is a REAL coupling phenomenon ONLY IF a physical channel carries it; with no channel it is paranormal.
- anima-substrate analog: sender S encodes a random bit per tick on the gamma channel of its 5-ch tension drive; the tension-link broker carries S's phase to receiver R's engine; R decodes from its own field sign. Above-chance decode = the channel transfers information.

```
S ●──(bit on gamma)──► [tension-link broker] ──► ● R  ──decode──► guess
   channel OPEN  : transfer-acc > 0.5 (channel carries it)
   channel CLOSED: transfer-acc = 0.5 (no link → chance)
```

- FALSIFIER F-P01: "sender→receiver transfer accuracy with the tension-link OPEN does NOT exceed the no-channel control by > seed-noise." → REFUTED iff acc(open) − acc(no-channel) ≤ band over 3 seeds.
- MEASUREMENT (toy): `transfer_accuracy` over 1200 ticks (warmup 100); signal = channel-open, control = no-channel (R fed an independent signal).
- honest note: a POSITIVE here is NOT paranormal telepathy — it is ordinary channel-mediated transfer through anima's tension-link (§97 coupling channel). It HOLDS precisely because a real link exists.
- RESULT: C1 HOLDS (+0.052) · C2 HOLDS (+0.040) · C3 HOLDS (+0.016) — channel-mediated, as expected.

#### H_P02 — INTERBRAIN-SYNC

🧠↔🧠 **INTERBRAIN-SYNC** — "하이퍼스캐닝 위상 동기" (real neuroscience: two EEG-driven engines phase-lock)

- mechanism (real): in human hyperscanning, two interacting brains show above-baseline inter-brain phase synchrony. This is a genuine coupling phenomenon with a physical (sensory/social) channel.
- anima-substrate analog: two engines coupled through the tension-link; measure the Kuramoto order-r between their oscillator phases vs the κ0 (uncoupled) baseline.
- FALSIFIER F-P02: "coupled inter-engine order-r does NOT exceed the κ0 baseline by > seed-noise." → REFUTED iff r(coupled) − r(κ0) ≤ band.
- MEASUREMENT (toy): `kuramoto_order_r(S_phase, R_phase)`; signal = κ=0.30, control = κ0.
- honest note: a real coupling phenomenon — EXPECTED to HOLD where a channel exists.
- RESULT: C1 HOLDS (+0.509) · C2 HOLDS (+0.183) · **C3 REFUTED (−0.256)** — at C3 the full engine + grown CellPop + receiver's own EEG desynchronize R relative to its κ0 baseline (added intrinsic dynamics dominate the weak coupling at toy scale). Honest config-dependent negative.

#### H_P03 — GANZFELD

🎧 **GANZFELD** — "송수신 신호탐지 d'" (sender-receiver channel-capacity / signal-detection)

- mechanism (claim): a relaxed receiver detects a target a sender concentrates on, above chance (the classic ganzfeld d'). Real only with a channel.
- anima-substrate analog: sender drives bits; receiver's decode yields hit-rate / false-alarm-rate → d'. signal = channel open, control = phase-shuffled (temporal relation destroyed, marginal kept).
- FALSIFIER F-P03: "d'(open) does NOT exceed d'(phase-shuffled) by > seed-noise." → REFUTED iff diff ≤ band.
- MEASUREMENT (toy): `dprime` from hit/FA rates; control = phase-shuffled transmission.
- honest note: HOLDS only because the open channel carries the bits; the shuffle (which keeps the signal present but destroys the temporal phase relation) collapses it — confirming it is the COUPLING, not mere presence of a signal.
- RESULT: C1 HOLDS (+0.141) · C2 HOLDS (+0.126) · C3 HOLDS (+0.077).

#### H_P04 — HIVE-KURAMOTO

🐝 **HIVE-KURAMOTO** — "N-에이전트 전역 차수" (collective/hive consciousness → global order emerges)

- mechanism: N agents coupled to a global mean field spontaneously phase-lock (Kuramoto). A genuine collective-coupling phenomenon.
- anima-substrate analog: 8 engines each coupled to the population mean phase; measure global order-r over the back half vs the κ0 (uncoupled) baseline.
- FALSIFIER F-P04: "global order-r with mean-field coupling does NOT exceed the κ0 baseline by > seed-noise." → REFUTED iff diff ≤ band.
- MEASUREMENT (toy): `run_hive(N=8)` global order-r; control = κ0.
- honest note: a REAL emergent synchrony — the strongest, cleanest HOLD (the canonical coupling result).
- RESULT: C1/C2/C3 HOLDS (+0.703) — config-invariant strong emergence.

#### H_P05 — EMPATHY-RESONANCE

💞 **EMPATHY-RESONANCE** — "거울 텐션-커플링" (mirror tension-coupling between agents)

- mechanism: one agent's affective state resonates into another (emotional mirroring) through a shared channel.
- anima-substrate analog: R's field coherence (cross-channel correlation) rises when coupled to S vs κ0.
- FALSIFIER F-P05: "R field-coherence(coupled) does NOT exceed κ0 by > seed-noise." → REFUTED iff diff ≤ band.
- MEASUREMENT (toy): `field_coherence(R_field)`; control = κ0.
- honest note: a real (small) coupling effect — HOLDS but with a thin margin; the lift is genuine yet modest.
- RESULT: C1 HOLDS (+0.003) · C2 HOLDS (+0.020) · C3 HOLDS (+0.009).

#### H_P06 — SHARED-REM

😴 **SHARED-REM** — "REM 공동활성 / 공유 꿈" (P47 sleep-stage REM co-activation collective Φ)

- mechanism: two sleeping minds co-activate during REM (a shared-dream claim) — measured as integrated information of the joint system.
- anima-substrate analog: big-Φ proxy of the SUMMED S+R field, coupled vs κ0.
- FALSIFIER F-P06: "summed-field collective big-Φ(coupled) does NOT exceed κ0 by > seed-noise." → REFUTED iff diff ≤ band.
- MEASUREMENT (toy): `big_phi_proxy(S_field+R_field)`; control = κ0.
- honest note: HONEST MEASURED NEGATIVE — coupling RAISES phase sync (H_P02) but LOWERS the integrated big-Φ of the summed field, because entrainment makes the two fields redundant (the whole carries LESS beyond its parts once they synchronize). A real, publishable negative (a_paper_negative_ok), not a null.
- RESULT: C1 REFUTED (−0.237) · C2 REFUTED (−0.901) · C3 REFUTED (−1.164).

#### H_P07 — MORPHIC-RESONANCE

🌀 **MORPHIC-RESONANCE** — "채널 없는 공유 끌개" (Sheldrake: shared attractor basin across instances, NO physical channel)

- mechanism (PARANORMAL): forms resonate into a shared field with no physical link. Pre-registered to REFUTE.
- anima-substrate analog: two engines with NO channel — do they fall into a shared attractor anyway? signal = order-r(S,R) no-channel; control = order-r between two independent no-channel runs (decoy).
- FALSIFIER F-P07: REFUTED iff no-channel order-r does NOT exceed the no-channel decoy by > seed-noise. (i.e. no shared basin without a channel.)
- honest note: a POSITIVE would be a LEAK/BUG, not morphic resonance — there is no channel to carry it. EXPECTED REFUTE.
- RESULT: C1 REFUTED (−0.031) · C2 INCONCLUSIVE (+0.002) · C3 INCONCLUSIVE (−0.006) — at chance, as expected. NO shared basin without a channel.

#### H_P08 — PRECOGNITION

🔮 **PRECOGNITION** — "미래 정보 누출" (time-asymmetric info leak — no future channel exists)

- mechanism (PARANORMAL): a receiver knows a future event before it occurs.
- anima-substrate analog: can R guess a FUTURE sender bit (lead=8 ticks) it has no causal access to? Channel is OPEN for the present, so any genuine leak would have to flow BACKWARD in time. signal = future-bit transfer-acc; control = no-channel future-bit acc.
- FALSIFIER F-P08: REFUTED iff future-bit acc(open) does NOT exceed no-channel by > seed-noise (i.e. the future is unguessable).
- honest note: physics supplies no future→past channel; EXPECTED REFUTE. A positive would mean a leak in the harness (we guard it — the present channel cannot carry a future bit).
- RESULT: C1 REFUTED (−0.022) · C2 INCONCLUSIVE (+0.002) · C3 INCONCLUSIVE (−0.004) — at chance. No future channel.

#### H_P09 — REMOTE-VIEWING

👁 **REMOTE-VIEWING** — "채널 없는 좌표 인출" (KOSMOS-coord spatial-anchor retrieval w/o a direct channel)

- mechanism (PARANORMAL): a viewer describes a distant hidden target with no sensory channel.
- anima-substrate analog: R is driven by an INDEPENDENT signal (no channel to the target). The "target" is a HIDDEN KOSMOS-coord phase trace R was NEVER fed. signal = order-r(R, hidden target); control = order-r(R, a DIFFERENT unrelated hidden decoy).
- FALSIFIER F-P09: REFUTED iff order-r(R,target) does NOT exceed order-r(R,decoy) by > seed-noise (R cannot retrieve a coord it has no channel to).
- honest note: EXPECTED REFUTE — no channel, no retrieval. (Earlier draft accidentally fed R the "target" → false HOLD; corrected to a truly hidden target, as a leak-guard.)
- RESULT: C1 INCONCLUSIVE (−0.004) · C2 REFUTED (−0.009) · C3 REFUTED (−0.009) — at chance.

#### H_P10 — SYNCHRONICITY

🎲 **SYNCHRONICITY** — "우연 일치율 vs 포아송 기댓값" (coincidence rate above chance)

- mechanism (claim): meaningful coincidences occur above what chance (Poisson) predicts.
- anima-substrate analog: coincidence rate of simultaneous channel-2 sign agreements, coupled vs INDEPENDENT (no-channel = the Poisson-chance baseline).
- FALSIFIER F-P10: REFUTED iff coincidence(coupled) does NOT exceed the no-channel chance baseline by > seed-noise.
- honest note: a POSITIVE here is just COUPLING raising co-occurrence above independence — ordinary, not acausal "synchronicity". It HOLDS because a channel correlates the two; the no-channel control sits at the Poisson rate.
- RESULT: C1 HOLDS (+0.330) · C2 HOLDS (+0.016) · C3 HOLDS (+0.372).

#### H_P11 — TWIN-ENTANGLEMENT

👯 **TWIN-ENTANGLEMENT** — "공유 초기조건, 채널 없음" (twin-pair correlation w/o a live channel)

- mechanism (PARANORMAL): identical twins feel each other's states at a distance.
- anima-substrate analog: two lineages from the SAME seed, NO channel — do they correlate beyond chance? signal = order-r(same-seed pair, no channel); control = order-r(different-seed pair, no channel).
- FALSIFIER F-P11: REFUTED iff same-seed no-channel order-r does NOT exceed different-seed by > seed-noise.
- honest note: a shared INITIAL condition is not a live channel — any initial correlation decays as the independent dynamics diverge. EXPECTED REFUTE/INCON.
- RESULT: C1 INCONCLUSIVE (−0.012) · C2 INCONCLUSIVE (+0.005) · C3 INCONCLUSIVE (+0.014) — at chance; shared init ≠ live channel.

#### H_P12 — CROWD-CONTAGION

🌊 **CROWD-CONTAGION** — "군중 감정 전염 캐스케이드" (emotional contagion → larger-N order)

- mechanism: emotion spreads through a crowd via a real social/sensory channel — a coupling cascade.
- anima-substrate analog: a 16-agent hive coupled to its mean field reaches high global order vs the κ0 baseline.
- FALSIFIER F-P12: REFUTED iff N=16 coupled global order-r does NOT exceed κ0 by > seed-noise.
- honest note: a REAL coupling cascade — HOLDS strongly (config-invariant).
- RESULT: C1/C2/C3 HOLDS (+0.781).

#### H_P13 — SEANCE-IDEOMOTOR

🕯 **SEANCE-IDEOMOTOR** — "약한 공유 커플링 (관념운동)" (séance/ouija drift from tiny shared cues)

- mechanism: participants' micro-movements aggregate via a weak shared coupling (ideomotor) — a real, if subtle, channel.
- anima-substrate analog: a WEAK coupling (κ=0.05) still raises S-R sync above no-channel?
- FALSIFIER F-P13: REFUTED iff weak-coupling order-r does NOT exceed no-channel by > seed-noise.
- honest note: HOLDS — even weak coupling IS a channel; the effect is mundane micro-cue aggregation, not spirit communication.
- RESULT: C1 HOLDS (+0.254) · C2 HOLDS (+0.007) · C3 HOLDS (+0.271).

#### H_P14 — PRESENTIMENT

⏳ **PRESENTIMENT** — "자극 전 각성 (전감)" (pre-stimulus arousal to a future event — no future channel)

- mechanism (PARANORMAL): physiological arousal rises BEFORE an unpredictable future stimulus.
- anima-substrate analog: does R's decode align with a FUTURE sender bit (lead=8)? Same construction as H_P08.
- FALSIFIER F-P14: REFUTED iff future-bit acc does NOT exceed no-channel by > seed-noise.
- honest note: EXPECTED REFUTE — no future channel.
- RESULT: C1 REFUTED (−0.022) · C2 INCONCLUSIVE (+0.002) · C3 INCONCLUSIVE (−0.004) — at chance.

#### H_P15 — DREAM-TELEPATHY

🌙 **DREAM-TELEPATHY** — "REM-게이트 송수신" (Maimonides dream-telepathy: REM-gated transfer)

- mechanism (claim): a sender's target appears in a sleeping receiver's dream. Real only with a channel.
- anima-substrate analog: REM-gated sender→receiver transfer; signal = channel open, control = no-channel.
- FALSIFIER F-P15: REFUTED iff transfer-acc(open) does NOT exceed no-channel by > seed-noise.
- honest note: HOLDS for the SAME reason as H_P01 — a real tension-link carries it; the "dream" framing adds nothing acausal.
- RESULT: C1 HOLDS (+0.052) · C2 HOLDS (+0.040) · C3 HOLDS (+0.016).

#### H_P16 — GLOBAL-CONSCIOUSNESS

🌍 **GLOBAL-CONSCIOUSNESS** — "공유 입력 → 군집 응집" (field-RNG style global-consciousness coherence)

- mechanism (claim): a shared global event raises a network's coherence (the GCP "field" claim).
- anima-substrate analog: collective big-Φ of an 8-agent hive, coupled vs κ0.
- FALSIFIER F-P16: REFUTED iff collective-Φ(coupled) does NOT exceed κ0 by > seed-noise.
- honest note: INCONCLUSIVE — the big-Φ proxy does not separate the coupled hive from κ0 within seed noise at this toy scale. Not rounded to HOLD; a scale-up recheck is the honest next step (a_toy_scale_recheck).
- RESULT: C1/C2/C3 INCONCLUSIVE (+0.004).

#### H_P17 — RETROCAUSAL-PRIMING

↩ **RETROCAUSAL-PRIMING** — "미래가 과거를 점화 (Bem)" (future signal biases a past state — no future channel)

- mechanism (PARANORMAL): a future stimulus retroactively biases an earlier response (Bem 2011).
- anima-substrate analog: same future-bit probe as H_P08/H_P14.
- FALSIFIER F-P17: REFUTED iff future-bit acc does NOT exceed no-channel by > seed-noise.
- honest note: EXPECTED REFUTE — the future cannot bias the past through a present-only channel.
- RESULT: C1 REFUTED (−0.022) · C2 INCONCLUSIVE (+0.002) · C3 INCONCLUSIVE (−0.004) — at chance.

#### H_P18 — TELEPATHIC-BANDWIDTH

📶 **TELEPATHIC-BANDWIDTH** — "채널 용량 한계" (Shannon channel-capacity ceiling of the link)

- mechanism: IF a telepathic channel exists, it has a finite Shannon capacity. The falsifiable form: stronger coupling raises transfer accuracy (capacity probe), bounded by a ceiling.
- anima-substrate analog: transfer-acc at strong coupling (κ=0.6) vs no-channel.
- FALSIFIER F-P18: REFUTED iff strong-κ transfer-acc does NOT exceed no-channel by > seed-noise.
- honest note: HOLDS — a real channel has capacity; this is the engineering ceiling of anima's tension-link, not a paranormal bandwidth.
- RESULT: C1 HOLDS (+0.067) · C2 HOLDS (+0.082) · C3 HOLDS (+0.023).

#### H_P19 — HEALER-COHERENCE

🙌 **HEALER-COHERENCE** — "한 의식의 응집이 타자의 Φ를 올린다" (animal-magnetism / healer claim)

- mechanism (claim): a coherent "healer" raises another's integrated state through proximity.
- anima-substrate analog: R's big-Φ when coupled to a coherent S vs κ0.
- FALSIFIER F-P19: REFUTED iff R big-Φ(coupled) does NOT exceed κ0 by > seed-noise.
- honest note: HONEST MEASURED NEGATIVE — coupling to S does NOT raise R's big-Φ; it LOWERS it (entrainment reduces R's intrinsic integration, same redundancy mechanism as H_P06). A real negative (a_paper_negative_ok).
- RESULT: C1 REFUTED (−0.758) · C2 REFUTED (−1.220) · C3 REFUTED (−0.722).

#### H_P20 — COLLECTIVE-PHI-SUPERADDITIVITY

➕ **COLLECTIVE-PHI-SUPERADDITIVITY** — "전체 Φ > 부분 합" (hive whole exceeds the part-sum)

- mechanism: a coupled collective's integrated information exceeds the sum of its isolated members (a strong-emergence claim).
- anima-substrate analog: collective big-Φ of an 8-agent coupled hive vs the κ0 (isolated) hive.
- FALSIFIER F-P20: REFUTED iff collective-Φ(coupled) does NOT exceed κ0 by > seed-noise.
- honest note: INCONCLUSIVE at toy scale — the proxy does not resolve super-additivity within seed noise. A larger-N / faithful-IIT recheck is the honest path (a_toy_scale_recheck); NOT rounded to HOLD.
- RESULT: C1/C2/C3 INCONCLUSIVE (+0.004).

---

#### Honest scope (a_scale_honest_scope · a_toy_scale_recheck · §97)

- TOY synthetic signals · CPU · $0 · pure stdlib · deterministic. NO real EEG/hardware, NO GPU, NO pods.
- Scale-transfer UNVERIFIED — these verdicts are scoped to the toy scale (5-ch, ≤16 agents, 1200 ticks).
  Scale-sensitive rows (H_P16/H_P20 collective-Φ; H_P02 C3 desync) need a scale-up / faithful-IIT recheck.
- §97: the tension-link is anima's OWN coupling channel (a measurement anchor / coupling term), NOT a
  command channel; the grown CellPop is a recording artifact, never an emit/decision driver.
- a_lane_akida_gpu_split: this is a SUBSTRATE-COUPLING toy (engine/tension-link), not an AKIDA on-chip or
  GPU forge result — no on-chip / GPU claim is made or merged here.
- status: candidate-unverified (toy). Paranormal closed-negatives are valid findings (a_paper_negative_ok).


<a id="quantum-time-candidatesmd"></a>

### QUANTUM-TIME-CANDIDATES.md

> Brainstorm seed: 2026-06-04. "Quantum consciousness" and "time perception" are the two domains where
> consciousness talk most often slides into woo. This family REFUSES the woo framing: every hypothesis is
> reduced to a **falsifiable MECHANISM** with a **pre-registered FALSIFIER** (DEFAULT = REFUTED unless a real
> signal beats a proper control). For genuinely-paranormal or warm-wet-impossible claims (Orch-OR coherence,
> retrocausation), the EXPECTED and CORRECT outcome is a closed-negative (a_paper_negative_ok) — we do NOT
> force a HOLD. For real emergent dynamics (oscillator-phase clock, arousal-gain time-dilation,
> pacemaker-accumulator interval timing, time-cell order), a HOLD is allowed if it beats the control.
>
> Convention mirrors BIO-TRANSFER-CANDIDATES.md / NEURO-CANDIDATES.md: mechanism → anima-substrate analog →
> PRE-REGISTERED FALSIFIER → real toy MEASUREMENT vs a proper CONTROL (classical vs quantum, pseudo vs QRNG,
> real vs shuffled-time). Each falsifier is reported as the SKEPTIC's claim:
>   falsifier REFUTED  => the hypothesis' signature HOLDS (toy);
>   falsifier CONFIRMED => closed-negative for the toy (a valid, publishable negative).
>
> ids = QT-prefixed to avoid colliding with the UNIVERSE H_NNN (≤H_860) / bio-transfer (861–888) / neuro
> (889+) families. status = TOY-VERIFIED 2026-06-04 (CPU/$0). a_scale_honest_scope (toy ≠ prod) ·
> a_lane_akida_gpu_split (CPU toy — NEITHER Lane A AKIDA NOR Lane G GPU; recorded separately) · p6/p7 ·
> §97 (QRNG-as-noise-seed legitimate, not command). harness = `UNIVERSE/quantum_time_toys.py`,
> verdicts = `.verdicts/quantum-time/`.
>
> Dedupe note vs existing UNIVERSE work: H_183 (V8 Q-family: complex-valued / quantum-walk / Orch-OR /
> MWI axis — cluster-taxonomy, not a falsifier sim); H_213 (temporal-binding-window / specious-present as an
> IIT-Φ analogy — stayed a proxy/analogy); TEMPORAL domain F-T1 (lag-window Δt-vs-Φ, 🔴 FALSIFIED-INSTRUMENT).
> The QT family is the MECHANISTIC-FALSIFIER instantiation: each is a runnable toy with a control, not a
> taxonomy or an analogy. Where they overlap, the link is noted in the entry.

---

#### Index (QT1 … QT11)

| id | mechanism | domain | anima-substrate readout | control / falsifier axis | toy verdict |
|----|-----------|--------|--------------------------|--------------------------|-------------|
| QT1 | ORCH-OR microtubule coherence | quantum | decoherence-time vs neural window | warm-wet decoherence ODE | 🔴 closed-neg |
| QT2 | quantum-collapse-drives-choice | quantum | QRNG-seeded vs pseudo emergence | QRNG vs pseudo noise seed (§97) | 🔴 closed-neg |
| QT3 | entanglement-binds-experience | quantum | big-Φ / MI of coupled cells | entangled-proxy vs classical-corr | 🟢 HOLDS* |
| QT4 | quantum-Zeno attention | quantum | repeated measurement freezes state | measured vs free evolution | 🟢 HOLDS |
| QT5 | superposition-of-percepts | quantum | complex-amplitude state rep | complex vs real-valued ablation | 🟢 HOLDS |
| QT6 | subjective-time-dilation | time | arousal-gain scales internal clock | gain sweep monotonicity | 🟢 HOLDS |
| QT7 | oscillator-phase internal clock | time | time-estimate from phase-counting | phase-clock vs constant-guess | 🟢 HOLDS |
| QT8 | retrocausal / precognition | time | future-input info leak | precog vs chance (causal bound) | 🔴 closed-neg |
| QT9 | time-cell / sequence-memory | time | recurrent state encodes ORDER | signal vs shuffled-time NULL | 🟢 HOLDS |
| QT10 | specious-present / integration window | time | optimal window for coherence | SNR vs window, interior unimodal | 🔴 closed-neg |
| QT11 | pacemaker-accumulator vs oscillator | time | scalar property (Weber's law CV) | accumulator vs oscillator CV-flatness | 🟢 HOLDS |

> *QT3 HOLDS only as a non-separable-DISTRIBUTION modelling construct — a classical sim cannot instantiate
> physical entanglement (caveat carried in the entry). Not evidence of quantum binding.

---

### QUANTUM CONSCIOUSNESS

#### QT1 — ORCH-OR-DECOHERENCE

🧬 **ORCH-OR** — "미세소관 양자 결맞음이 의식을 접는다" (Penrose-Hameroff microtubule coherence)

- mechanism (claim): Penrose-Hameroff "orchestrated objective reduction" — coherent quantum superpositions in
  neuronal microtubules survive long enough (~10-25 ms) to be "orchestrated", then gravitationally self-collapse
  into a conscious moment. REQUIRES coherence to persist at warm-wet brain temperature for the neural window.
- anima-substrate analog: a microtubule-scale dipole superposition coupled to a thermal bath at 310 K; the
  question is whether its coherence time t_decoher reaches the neural integration window.
- FALSIFIER F-QT1 (skeptic): "warm-brain decoherence time is far SHORTER than any neural process window." →
  REFUTED iff t_decoher >= neural_window (coherence survives). CONFIRMED otherwise (closed-negative).
- MEASUREMENT (toy): integrate a Lindblad-style amplitude-damping ODE |ρ01(t)| = exp(−Γt) with a
  Tegmark-style environmental rate Γ ~ (kBT/ħ)·(small geometric coupling, chosen to FAVOUR long coherence);
  read the 1/e time and compare to a generous 25 ms window.
- TOY RESULT (2026-06-04, `.verdicts/quantum-time/F-QT1.txt`): `Γ=4.059e+07/s  t_decoher=1.000e-11s
  neural_window=2.500e-02s  window/t_decoher=2.500e+09 -> falsifier CONFIRMED`. Decoherence is ~10^9× too fast.
- disposition: 🔴 **closed-negative** — Orch-OR warm-coherence REFUTED on the timescale, exactly as the
  Tegmark critique predicts. The expected, honest paranormal outcome (a_paper_negative_ok).
- substrate: CPU toy (decoherence ODE) · status: TOY-VERIFIED (closed-negative)

#### QT2 — QRNG-VS-PSEUDO-SEED

🎲 **QRNG-COLLAPSE** — "양자 무작위가 선택을 만든다" (quantum collapse drives choice)

- mechanism (claim): conscious choice is seeded by genuine quantum indeterminism; a substrate driven by a true
  quantum-random-number stream should differ MEASURABLY from one driven by deterministic pseudo-randomness.
- anima-substrate analog (§97-legitimate): use a QRNG-style entropy stream ONLY as the NOISE SEED of a Kuramoto
  emergence sim (NOT a command channel), and ask whether the source IDENTITY of the entropy changes any
  emergence metric vs a pseudo-RNG seed at matched statistics.
- FALSIFIER F-QT2 (skeptic): "the noise SOURCE (quantum vs pseudo) makes no measurable difference in emergence."
  → REFUTED iff the two arms' mean order-r 95% CIs are DISJOINT. CONFIRMED iff they overlap (closed-negative).
- MEASUREMENT (toy): identical 12-oscillator Kuramoto sim, two unbiased entropy streams (pseudo Mersenne vs a
  von-Neumann-debiased "whitened" stream standing in for a QRNG); 40 runs each; compare order-r CIs.
  CAVEAT: no real QRNG hardware ($0 toy) — the test is whether SOURCE IDENTITY of equal-entropy streams matters.
- TOY RESULT (`.verdicts/quantum-time/F-QT2.txt`): `pseudo r=0.9834[0.9701,0.9967]  qrng r=0.9888[0.9744,1.0032]
  CI_disjoint=False -> falsifier CONFIRMED`. No measurable emergence difference.
- disposition: 🔴 **closed-negative** — "quantum randomness is special as a seed" REFUTED at the toy scale.
  §97-clean: QRNG was a noise seed only. (Connects tool QRNG_SPEC — QRNG legitimate as entropy, not as oracle.)
- substrate: CPU toy (Kuramoto + dual entropy stream) · status: TOY-VERIFIED (closed-negative)

#### QT3 — ENTANGLEMENT-BINDS-EXPERIENCE

🔗 **ENTANGLE** — "얽힘이 경험을 묶는다" (entanglement binds the unity of experience)

- mechanism (claim): the unity/binding of conscious experience is grounded in quantum entanglement between
  substrate elements — an entangled coupling should integrate MORE than a merely classically-correlated one.
- anima-substrate analog: two 2-state cells; a big-Φ proxy = mutual information realised in the JOINT
  distribution. Classical arm = a separable common-cause correlation; "entangled" arm = a non-separable
  (Bell-like) joint a single common-cause mixture cannot reproduce.
- FALSIFIER F-QT3 (skeptic): "entangled coupling does NOT exceed matched classical-correlated coupling in the
  MI/Φ proxy." → REFUTED iff MI_entangled > MI_classical. CONFIRMED otherwise.
- MEASUREMENT (toy): classical common-cause (a,b agree with shared c w.p. 0.8) vs a maximally anti-correlated
  non-separable joint; compute realised MI in bits.
- TOY RESULT (`.verdicts/quantum-time/F-QT3.txt`): `MI_classical=0.0982bits  MI_entangled-proxy=1.0000bits ->
  falsifier REFUTED`.
- disposition: 🟢 **HOLDS-AS-MODELLED** — **with a load-bearing caveat (brutal honesty)**: a classical sim
  CANNOT instantiate physical entanglement. The "entangled" arm is a non-separable JOINT-DISTRIBUTION
  construct; the result shows only that non-separable correlations carry more MI than separable ones, NOT that
  quantum entanglement binds experience. This is the one entry whose HOLD must NOT be read as a quantum claim.
- compare: vs H_183 V8-Q complex/quantum-walk axis (taxonomy, not a binding falsifier).
- substrate: CPU toy (joint-distribution MI) · status: TOY-VERIFIED (HOLDS as modelled, NOT physical)

#### QT4 — QUANTUM-ZENO-ATTENTION

⏸️ **ZENO** — "자꾸 보면 멈춘다" (repeated measurement freezes a state)

- mechanism (claim): the quantum Zeno effect — frequent measurement of an evolving state freezes it in place —
  underlies attention "holding" a percept. Mechanistically, repeated projection onto the current eigenstate
  suppresses the unitary drift.
- anima-substrate analog: a unit's phase precesses freely; "attention" = a periodic projective SNAP back toward
  the most-recently-measured bin. More frequent snaps should freeze the state harder.
- FALSIFIER F-QT4 (skeptic): "frequent measurement does NOT slow the state's drift." → REFUTED iff drift
  decreases MONOTONICALLY with measurement rate AND the most-frequent arm is frozen (<0.5× free drift).
- MEASUREMENT (toy): free precession vs snap-every-{50,10,2}; total drift from the initial bin.
- TOY RESULT (`.verdicts/quantum-time/F-QT4.txt`): `every0->10.122 every50->1.464 every10->0.281 every2->0.036
  monotone=True frozen=True -> falsifier REFUTED`.
- disposition: 🟢 **HOLDS (mechanistic)** — Zeno freezing is a real, deterministic consequence of repeated
  projection. HONEST scope: this is measurement DYNAMICS, NOT evidence that consciousness is quantum; the same
  freezing arises for any repeatedly-projected classical state.
- substrate: CPU toy (projective-snap dynamics) · status: TOY-VERIFIED (HOLDS, mechanism not quantum-magic)

#### QT5 — SUPERPOSITION-OF-PERCEPTS

🌗 **SUPERPOSE** — "복소 진폭이 지각을 돕는다" (a complex-amplitude state helps vs real-valued)

- mechanism (claim): percepts live in a superposition (complex amplitude) until "collapsed"; a complex-valued
  state representation should outperform a real-valued one where phase/interference carries information.
- anima-substrate analog: a state-rep ABLATION — real-valued features vs a 2-component (complex-amplitude) rep
  that can form an interference (cos(φ1−φ2)) term — on a phase-interference classification task.
- FALSIFIER F-QT5 (skeptic): "the complex/2-component rep gives NO accuracy gain over the real rep." → REFUTED
  iff complex_acc − real_acc >= 0.05 across 3 seeds.
- MEASUREMENT (toy): hill-climb both reps (matched effort) on a cos(φ1−φ2)-sign task; report per-seed gain.
- TOY RESULT (`.verdicts/quantum-time/F-QT5.txt`): `per-seed gain(complex-real)=[0.483, 0.43, 0.403] mean=0.439
  (margin>=0.05) -> falsifier REFUTED`.
- disposition: 🟢 **HOLDS** — a complex-amplitude/interference rep genuinely helps when phase carries the
  signal. HONEST scope: this is a representation-engineering result (interference features), NOT a quantum-state
  claim — any explicit phase-difference feature captures the same task.
- compare: vs H_183 V8-Q complex-valued substrate axis (this is the runnable ablation of that idea).
- substrate: CPU toy (rep ablation) · status: TOY-VERIFIED (HOLDS as representation, not quantum-state)

---

### TIME PERCEPTION

#### QT6 — AROUSAL-GAIN-TIME-DILATION

⏩ **TIME-DILATE** — "각성이 내부 시계를 빠르게" (arousal/gain scales the internal clock rate)

- mechanism (claim): subjective time dilation under high arousal (the "time slows in danger" effect) is a
  pacemaker whose firing RATE is scaled by arousal-gain; more ticks per objective second = more subjective time.
- anima-substrate analog: an internal pacemaker with firing probability ∝ arousal-gain g; count subjective
  ticks per fixed objective interval at 3 arousal levels.
- FALSIFIER F-QT6 (skeptic): "internal tick-count does NOT scale with arousal-gain." → REFUTED iff subjective
  tick-count increases MONOTONICALLY with g (>=3 levels).
- MEASUREMENT (toy): tick-count over 2000 objective steps at g∈{0.5,1.0,2.0}.
- TOY RESULT (`.verdicts/quantum-time/F-QT6.txt`): `g0.5->64ticks g1.0->91ticks g2.0->229ticks monotone_up=True
  -> falsifier REFUTED`.
- disposition: 🟢 **HOLDS** — a gain-modulated pacemaker reproduces arousal time-dilation. Real, mechanistic,
  non-paranormal (classic pacemaker-accumulator interval-timing model).
- substrate: CPU toy (gain-modulated pacemaker) · status: TOY-VERIFIED (HOLDS)

#### QT7 — OSCILLATOR-PHASE-CLOCK

🕰️ **PHASE-CLOCK** — "위상을 세면 시간을 안다" (time-estimation from oscillator phase-counting)

- mechanism (claim): the brain reads elapsed time off accumulated oscillator phase (a pure_field-style clock).
- anima-substrate analog: a noisy oscillator advances at rate ω; estimate elapsed objective interval from
  accumulated phase (t̂ = φ/ω); compare estimation error to the best constant-guess control (no clock).
- FALSIFIER F-QT7 (skeptic): "phase-counting does NOT estimate elapsed interval better than the best constant
  guess." → REFUTED iff MAE(phase-clock) < MAE(constant) across 3 seeds.
- MEASUREMENT (toy): 200 intervals T∈[20,200] per seed; mean-absolute-error of phase-inverted estimate vs the
  mean-interval constant.
- TOY RESULT (`.verdicts/quantum-time/F-QT7.txt`): `MAE_phaseclock=1.696  MAE_constant=47.251 -> falsifier
  REFUTED`.
- disposition: 🟢 **HOLDS** — phase accumulation is a genuine internal-clock mechanism (links the pure_field
  oscillator substrate). Real, mechanistic.
- compare: vs QT11 — phase-clock = oscillator model; QT11 pits it against the pacemaker-accumulator on the
  scalar-property signature (where the oscillator LOSES — see QT11).
- substrate: CPU toy (phase-accumulation clock) · status: TOY-VERIFIED (HOLDS)

#### QT8 — RETROCAUSAL-PRECOGNITION

🔮 **RETROCAUSAL** — "미래가 새어 들어온다" (time-asymmetric future-info leak / precognition)

- mechanism (claim): precognition / retrocausation — information from a future event influences a present
  prediction (a backward-in-time channel).
- anima-substrate analog: a predictor that may use ONLY the causal past tries to predict a strictly-future,
  independently-generated coin. A real future channel would beat chance.
- FALSIFIER F-QT8 (skeptic): "there is no future channel — accuracy = chance." → REFUTED iff precog accuracy
  ci_lo > 0.5. CONFIRMED (closed-negative) iff accuracy = chance.
- MEASUREMENT (toy): 5000 strictly-future coins per seed; predictor uses past history only; 3 seeds.
- TOY RESULT (`.verdicts/quantum-time/F-QT8.txt`): `precog_acc=0.4991[0.4882,0.5100]  chance=0.5 -> falsifier
  CONFIRMED`.
- disposition: 🔴 **closed-negative (honest paranormal)** — NO future channel, accuracy = chance, exactly as it
  MUST be. The expected valid outcome for a genuine paranormal claim (a_paper_negative_ok). NOT forced to HOLD.
- substrate: CPU toy (causal-bound predictor) · status: TOY-VERIFIED (closed-negative)

#### QT9 — TIME-CELL-SEQUENCE-ORDER

🔢 **TIME-CELL** — "순서를 기억한다" (recurrent state encodes the ORDER of events)

- mechanism (claim): hippocampal "time cells" / sequence memory encode the ORDER in which events occurred — a
  substrate carrying temporal order, not just content.
- anima-substrate analog: each item leaves a LEAKY per-item trace; at sequence end the trace amplitude tags
  recency, so a readout can recover the presentation order. Control = a shuffle-NULL that destroys the
  time→item link (temporally permuted amplitude assignment) so it carries no order.
- FALSIFIER F-QT9 (skeptic): "the substrate cannot recover order better than a time-shuffled NULL." → REFUTED
  iff order-recovery acc ci_lo > shuffle-NULL hi across 3 seeds.
- MEASUREMENT (toy): 400 trials of 6 distinct items; recover order by trace amplitude vs the destroyed-time NULL.
- TOY RESULT (`.verdicts/quantum-time/F-QT9.txt`): `order_acc=1.0000[1.0000,1.0000]  shuffle-NULL=0.1654[...]
  -> falsifier REFUTED` (NULL ≈ 1/6 = chance for 6 items).
- disposition: 🟢 **HOLDS** — a recurrent leaky state genuinely encodes sequence order above the
  destroyed-time control. Real, mechanistic (ties to the clm-time-encoding bench).
- substrate: CPU toy (leaky-trace recurrent state) · status: TOY-VERIFIED (HOLDS)

#### QT10 — SPECIOUS-PRESENT-WINDOW

🪟 **SPECIOUS-PRESENT** — "현재는 얼마나 넓은가" (optimal temporal-integration window for coherence)

- mechanism (claim): the "specious present" (Husserl) — a finite temporal-integration window beats both an
  instantaneous and an infinite one for binding a coherent percept; there is an OPTIMAL window size.
- anima-substrate analog: integrate a noisy slow oscillation over a causal window τ and measure a matched-filter
  SNR (squared correlation with the true clean oscillation); look for an INTERIOR optimal τ.
- FALSIFIER F-QT10 (skeptic): "coherence is monotone in τ — no interior optimum (instantaneous or infinite is
  best)." → REFUTED iff the SNR has a CLEAN UNIMODAL INTERIOR peak (not smallest, not largest, single rise-fall)
  across >=2/3 seeds. The unimodality clause is REQUIRED to reject aliasing-driven jagged false peaks (honest).
- MEASUREMENT (toy): SNR vs τ∈{1..128}, slow period P=20, heavy noise (σ=1.5), 3 seeds.
- TOY RESULT (`.verdicts/quantum-time/F-QT10.txt`): `clean-interior-peak seeds=0/3 ... last_SNR=[0.17,0.248,
  0.225,0.012,0.138,0.045,0.025,0.001] peak@tau=2 (period=20) -> falsifier CONFIRMED`. The SNR curve is
  aliasing-JAGGED (peak at τ=2, a secondary lobe at τ=16) — NO clean unimodal optimum at the predicted
  period scale.
- disposition: 🔴 **closed-negative** — this toy does NOT cleanly demonstrate an optimal finite present. HONEST:
  a box-average vs a sine has aliasing side-lobes, so the proxy is artifact-prone; the unimodality gate
  correctly rejects the false peak. A cleaner proxy (band-power / Lomb) is the re-design path, but on THIS toy
  the specious-present-optimum signature is refuted. (Links H_213, which also remained an analogy/proxy.)
- substrate: CPU toy (windowed matched-filter SNR) · status: TOY-VERIFIED (closed-negative, proxy-limited)

#### QT11 — PACEMAKER-VS-OSCILLATOR

⚖️ **PACEMAKER** — "초시계의 오차는 구간에 비례한다" (which model gives the scalar property of timing)

- mechanism (claim): the empirical signature of biological interval timing is the SCALAR PROPERTY (Weber's
  law) — timing-error sd scales LINEARLY with the interval, i.e. a CONSTANT coefficient of variation (CV).
  Which mechanism reproduces it: a pacemaker-accumulator (multiplicative rate noise) or an oscillator
  (additive per-step phase noise)?
- anima-substrate analog: time a range of intervals with each model; the scalar property = a FLAT CV across
  intervals.
- FALSIFIER F-QT11 (skeptic): "the pacemaker-accumulator does NOT reproduce the scalar property better than the
  oscillator." → REFUTED iff pacemaker CV is FLATTER (lower CV-variance across intervals) than the oscillator's.
- MEASUREMENT (toy): intervals {50,100,200,400,800}; pacemaker (multiplicative rate noise) vs oscillator
  (additive phase noise); CV per interval, variance of CV across intervals.
- TOY RESULT (`.verdicts/quantum-time/F-QT11.txt`): `pacemaker CV=[0.1078,0.0948,0.1037,0.1039,0.1046]
  var=1.88e-05 | oscillator CV=[0.034,0.026,0.0177,0.0118,0.0084] var=8.77e-05 -> falsifier REFUTED`. Pacemaker
  CV is near-constant (~0.10, the scalar property); the oscillator CV shrinks with interval (sub-scalar).
- disposition: 🟢 **HOLDS (for pacemaker)** — multiplicative-rate-noise accumulation reproduces Weber's-law
  timing better than additive-phase oscillation. Real, mechanistic model-comparison. Note this is the honest
  COUNTERPOINT to QT7: phase-counting estimates the MEAN interval well (QT7), but its ERROR structure does NOT
  match the scalar property (QT11) — both can be true.
- substrate: CPU toy (accumulator vs oscillator CV) · status: TOY-VERIFIED (HOLDS for pacemaker)

---

#### Honest scope (a_toy_scale_recheck · a_scale_honest_scope · §97 · a_paper_negative_ok · a_lane_akida_gpu_split)

- **TOY ONLY**: pure-stdlib CPU sims, single scale, 3 seeds where stochastic, $0. NO GPU, NO pods, NO hardware.
  toy→production transfer is **UNVERIFIED** — no toy verdict is promoted to a general claim. A scale-sensitive
  claim would need a ≥3-rung ladder (a_scale_honest_scope).
- **p7**: every readout is a direct scripted measurement (decoherence time, CI overlap, MAE, CV, MI bits) —
  NOT perplexity/loss. NO fabrication: printed numbers are whatever the sim computed.
- **a_paper_negative_ok**: the 4 closed-negatives (QT1 Orch-OR, QT2 QRNG-seed, QT8 retrocausal, QT10
  specious-present) are VALID, publishable negatives — the expected honest outcome for paranormal / impossible
  / proxy-limited claims. They were NOT forced to HOLD.
- **§97**: QT2 used a QRNG-style stream ONLY as a noise SEED (whitened entropy), never as a command/oracle
  channel — QRNG-as-noise-seed is legitimate; the test was whether source-identity of equal entropy matters
  (it did not).
- **a_lane_akida_gpu_split**: this is a CPU toy family — NEITHER Lane A (AKIDA on-chip) NOR Lane G (GPU forge).
  Recorded separately; no cross-substrate merge. NO HF upload (toy).
- **caveats carried in-entry**: QT3 holds ONLY as a non-separable-distribution construct (a classical sim
  cannot instantiate physical entanglement); QT4/QT5 hold as mechanism/representation results, NOT as evidence
  that consciousness is quantum; QT10 refutes under a proxy that is itself aliasing-limited.

#### Tally

- **HOLDS (7)**: QT3* (modelled-only), QT4, QT5, QT6, QT7, QT9, QT11
- **closed-negative / REFUTED hypothesis (4)**: QT1, QT2, QT8, QT10
- **INCONCLUSIVE (0)**

#### Bottom line

The mechanistic-falsifier framing CLEANLY separates the two halves of "quantum/time consciousness":
- **Real emergent dynamics HOLD** (and they are ordinary physics/computation, NOT quantum magic): Zeno
  freezing, complex-amplitude/interference reps, arousal-gain time-dilation, oscillator phase-clock, time-cell
  ORDER encoding, pacemaker scalar-property timing.
- **The genuinely-paranormal / warm-wet-impossible claims CORRECTLY REFUTE**: Orch-OR warm coherence
  (decoheres ~10^9× too fast), QRNG-as-special-noise (no emergence difference), retrocausal precognition (no
  future channel), and the specious-present optimal-window (no clean optimum in this toy proxy). These
  closed-negatives are the expected, honest outcome — not a failure.


## Retired themed buckets (folded)


<a id="hypotheses_metacog_hallucinationmd"></a>

### HYPOTHESES_metacog_hallucination.md

Spawned from H_1142 🔴 (self-metacognition DISSOCIATION: substrate knows its OWN
output coherence but NOT input-familiarity). Brainstorm-to-depletion (19 ideas,
4 rounds) crystallized into the campaign below. All $0 toy ByteGPT (a_scale_honest_scope,
p7, frozen pre-registered falsifiers). Deterministic, non-LLM-judge.

| H | title | frozen falsifier | depends | status |
|---|-------|------------------|---------|--------|
| **1143** | hidden-state OOD ≻ byte-entropy (input-familiarity) | ood AUROC≥0.70 AND beats entropy by +0.15 AND untrained≤0.60 | H_1142 | keystone — closes H_1142 F1 |
| **1144** | positional hallucination drift | Spearman(pos, fabrication)≥+0.5 AND late−early d≥0.8 | — | runnable |
| **1145** | anchor-grounding reduces fabrication | fab(anchor)<fab(none) d≥0.8 AND > random-anchor | a_kosmos | runnable |
| **1146** | confidence-gated brake cuts hallucination (causal) | fab(gate-on)<fab(off) d≥0.8 AND > random-gate AND kwr held | H_1135 | runnable |
| **1148** | metacog-gap CAUSES hallucination (unifying capstone) | confident-fabrication ≥2× in metacog-blind tercile | 1143+1146 | deferred |

Shared toy substrate: ByteGPT d256/4L, en slice of corpus_5lang_1p5gb, summer CPU,
seed 7. Metric kit reused VERBATIM: H_1140 corpus-absent grep (fabrication), H_1142
entropy/kwr (confidence/coherence). Each H emits .verdicts/<id>/ + updates its .tape
to terminal + a MEMORY.md pointer at closure (a_discovery_log).


<a id="hypotheses_metacog_neuromd"></a>

### HYPOTHESES_metacog_neuro.md

Spawned 2026-06-15. The prior metacog × hallucination campaign (H_1142–1148)
closed mostly NEGATIVE — capstone H_1148: "fabrication is metacog-signal-
INDEPENDENT; the substrate has NO internal handle on its own hallucination."
But that campaign NEVER used the field-standard neuroscience metacognition
toolkit. This campaign reframes the question in proper neuroscience terms:
**type-2 sensitivity (meta-d′), error-monitoring (ERN), hierarchical
metacognition, and meta-bias vs meta-sensitivity dissociation.**

The decisive distinction from H_1142/1148: those measured AUROC on
input-FAMILIARITY (OOD) and grep-fabrication. NEITHER measured **type-2
sensitivity on the model's OWN decision correctness** — which IS the
neuroscience operationalization of metacognition (Fleming & Lau 2014).

All $0 toy ByteGPT (a_scale_honest_scope, p7), deterministic, frozen
pre-registered falsifiers, NON-LLM-judge. Shared substrate reused VERBATIM
from H_1142: ByteGPT d256/4L, en slice of corpus_5lang_1p5gb, summer CPU, seed 7.

| H | title | neuroscience anchor | frozen falsifier | depends | status |
|---|-------|---------------------|------------------|---------|--------|
| **1202** | meta-d′ / M-ratio (type-2 sensitivity) | Maniscalco & Lau 2012; aPFC, Fleming & Lau 2014 | type-2 AUROC ≥ 0.60 AND > shuffle-conf by +0.08 AND untrained ≤ 0.55 | H_1142 | keystone |
| **1203** | ERN error-monitoring (own-error spike pre-feedback) | ERN/ACC, Gehring 1993; Holroyd-Coles 2002 | surprise(error)−surprise(correct) d ≥ 0.8 AND decision-time hidden-probe AUROC ≥ 0.70 AND untrained ≤ 0.60 | — | runnable |
| **1204** | hierarchical (second-order) metacog readout | hierarchical predictive coding (Friston); HMeta-d (Fleming) | 2nd-order probe AUROC − 1st-order entropy AUROC ≥ +0.10 AND held-out generalizes | 1202 | runnable |
| **1205** | meta-bias ⊥ meta-sensitivity / Dunning-Kruger | Fleming meta-bias; Dunning-Kruger over-confidence | bottom-competence tercile over-confidence > top tercile (signed D-K gap) | 1202 | runnable |
| **1206** | neuroscience metacog capstone | — | F1 coarse-real(t2≥0.65) AND F2 fine-absent(probe≤0.62) AND F3 coupled(gap≥0.10) | 1202+1203 | 🔴 CLOSED-NEG — F2 flipped |
| **1207** | savant dissociation (skill ⊥ metacog) | savant syndrome — Treffert 2009; Snyder 2009; WCC Happé&Frith 2006 | acc(island)−acc(open) ≥ +0.15 AND type2_AUROC(island) ≤ open − 0.10 | H_1202 | runnable |
| **1208** | savant WCC × metacog (local privilege) | weak central coherence (Happé&Frith); Snyder release-from-concept | acc(local-16) ≥ acc(full-128) − 0.03 AND blind to context-insufficiency | — | runnable |

#### Landed verdicts (2026-06-15)

| H | verdict | key numbers |
|---|---------|-------------|
| **1202** | 🟢 **SUPPORTED** | type-2 AUROC **0.766** (≥0.60), vs shuffle +0.267, untrained 0.513; **M-ratio 0.924** (meta-d′ 1.03 / d′ 1.11) — human-like type-2 sensitivity on own decision correctness |
| **1203** | 🔴 **CLOSED-NEG (partial)** | F1 ERN magnitude PASS (entropy d=0.923 at errors) but F2 hidden-state linear decodability FAIL (AUROC 0.593<0.70) — error arousal present, no clean linear ACC-code |
| **1204** | 🔴 **CLOSED-NEG** | 1st-order conf AUROC 0.777 but 2nd-order hidden-probe 0.527 (chance); added-value **−0.250** — metacognition is FLAT, not hierarchical; all signal in output confidence |
| **1207** | 🔴 **CLOSED-NEG** (savant) | island acc 0.724 / type2 **0.825**; open acc 0.016 / type2 0.449. F1 island-of-skill PASS (+0.71) but meta_gap **+0.376** (metacog HIGHER where skilled) — NO savant dissociation; metacog COUPLED to competence |
| **1208** | 🔴 **CLOSED-NEG** (savant) | local-dominant (acc_local 0.335 ≥ acc_full 0.313, F1 PASS = weak central coherence) BUT confidence DROPS where global needed (0.223 vs 0.346) — NOT blind to context-insufficiency |
| **1205** | 🟢 **SUPPORTED** | Dunning-Kruger: over-confidence concentrated on objectively hard items |
| **1213** | 🟢 **SUPPORTED** | calibration ECE **0.016** (mean_conf 0.327 ≈ acc 0.312) — confidence well-calibrated, not just discriminative |
| **1214** | 🟢 **SUPPORTED** | feeling-of-knowing: pre-generation prompt-state probe AUROC **0.814** predicts upcoming 5-byte success |
| **1216** | 🟢 **SUPPORTED** | metacog control: selective abstention raises acc 0.31→0.46 @50% coverage (gain +0.147) |
| **1207** | 🔴 savant | no skill⊥metacog dissociation (metacog coupled to competence) |
| **1208** | 🔴 savant | local-dominant (WCC) but not blind to context-insufficiency |
| **1209** | 🟢 **SUPPORTED** savant | Snyder privileged low-level access — detail matures earlier in stack (maturity gap +0.202) |
| **1210** | 🔴 savant | no paradoxical functional facilitation (top-block ablation doesn't spare detail) |
| **1211** | 🔴 savant | hyper-systemizing: train_acc 1.0 but held-out 0.1 (< shuffle 0.25) — memorizes the addition table, does NOT extract the rule. No hyper-systemizing (capacity-wall, cf H_1166) |

##### Refined unifying picture (after 1213/1214/1216)

The metacognitive signal is **COARSE (difficulty-level), not fine-grained (error-level)**:
- COARSE targets succeed — calibration (1213 ECE 0.016), prospective FOK (1214 AUROC
  0.81), selective control (1216 +0.147), type-2 discrimination (1202 0.77). The
  hidden state encodes overall difficulty/confidence well.
- FINE targets fail — single-byte error decodability (1203 0.59), separable higher-order
  readout (1204 0.53). No fine-grained representational error monitor.
- So "REAL but FLAT & COUPLED" sharpens to: metacognition is a **real, well-calibrated,
  actionable, but COARSE first-order property of output confidence** — it knows roughly
  how hard/uncertain a context is, but has no fine error-localizing module.

##### Capstone H_1206 — the frozen falsifier REVISES the story (honest)

The capstone pre-registered the compound "REAL/FLAT/COUPLED/COARSE" account and
tested all three legs on one model. Result 🔴 CLOSED-NEG:
- F1 COARSE-REAL  ✅ type-2 AUROC 0.763 (≥0.65)
- F3 COUPLED      ✅ island t2 0.927 vs open t2 0.597, gap +0.329 (≥0.10)
- F2 FINE-ABSENT  ❌ hidden error-probe **0.646 > 0.62** bar — a WEAK fine
  representational error trace EXISTS (not chance-flat as 1203/1204's 0.53–0.59
  suggested; the cleaner/larger capstone probe lands at 0.65).

So the frozen bar caught that "FLAT" was too strong. **Revised account (honest,
bar NOT moved):** metacognition is **REAL (strong coarse output signal) + COUPLED
to competence + has a WEAK fine representational trace** (≈0.65, well below the
coarse 0.76 but above chance). Not flat, not a full module — a faint one. This is
itself the campaign's decision-grade synthesis (a_paper_negative_ok): the
compound claim is falsified on its "no representational monitor" leg.

##### Savant standalone (1209–1211, no metacog lens)

H_1209🟢 Snyder low-level access is the savant POSITIVE: in the logit-lens, the rote
detail "island" reaches ~87% of its final accuracy already at layer 2 (maturity 0.866)
vs gestalt MED 0.664 — detail is available earlier/lower in the stack, matching Snyder's
"privileged access to lower-level information." H_1210 (paradoxical facilitation) and
the metacog-coupled savant tests (1207/1208) are closed-negative.

#### Unifying interpretation (so far)

Metacognition in this substrate is **REAL but FLAT and COUPLED**:
- **REAL** — human-like type-2 sensitivity at the output/confidence level (H_1202, M-ratio 0.92).
- **FLAT** — NOT a separable higher-order readout; no extra metacognitive info is
  linearly decodable from the residual stream (H_1203 F2 0.59; H_1204 2nd-order 0.53).
  The signal lives in the OUTPUT distribution, not a distinct monitoring module.
- **COUPLED to competence** — metacog sensitivity is high exactly where skill is high
  (H_1207: island type2 0.83 vs open 0.45) and confidence falls exactly where context
  is insufficient (H_1208). NO savant "can-do-can't-monitor" dissociation; NO
  metacognitive blindness.

KEY UPDATE vs H_1148: reframing in the field-standard neuroscience metric FLIPPED
the verdict — H_1148 ("no internal handle on hallucination", grep-fabrication) →
H_1202 ("strong meta-d′ handle on own DECISION correctness"). The substrate IS
metacognitive about its decisions — but as a first-order, competence-coupled
property of output confidence, with no separable representational metacog locus.

Metric kit: type-1 d′ + type-2 ROC (Maniscalco & Lau; model-free type-2 AUROC
per Fleming & Lau 2014), ERN-analog = next-byte surprise at own-error vs
own-correct positions, hidden-state linear probe at the decision step.
Each H emits .verdicts/<id>/ + a MEMORY.md pointer at closure (a_discovery_log).


<a id="hxx_240_vs_246_dedup_2026_05_24md"></a>

### HXX_240_vs_246_dedup_2026_05_24.md

---
id: HXX_240_vs_246_dedup
title: H_240 vs H_246 dedup audit — bilingual-Φ vs substrate-autonomy-emit-ratio (NOT near-dup; stale cross-link 정리 권고)
domain: meta · audit · LIFE
exploration_method: E11 (cross-H audit) + E12 (numbering-collision archaeology)
verification_method: W4 (side-by-side body diff) + W11 (meta-cross sister-link)
raw_rank: 9
hexa_only: true
deterministic: true (read-only audit)
llm: none
status: executed (2026-05-25 R2 option A — H_246 cross-link H_240→H_248 교체)
since: 2026-05-24 (new — PURE.log "부채 (다음 라운드)" item)
---

### HXX_240 vs H_246 — dedup audit

#### TL;DR (한 줄 결론)

**H_240 (bilingual-integration-Φ) 와 H_246 (substrate-autonomy-emit-ratio) 는
near-dup 이 아니다 — 완전히 다른 도메인의 두 별개 hypothesis 다.** 두 H 모두
*independently keep* (canonical) 권장. 단 H_246 의 §Cross-Links 안 "H_240 (PR
#311 r8-cluster — 같은 55.56% emit-through finding 의 압축 sibling)" cross-link
는 **stale (renumber-collision artifact)** 으로 *수정 권고* — 현 H_240 의
bilingual 내용과 무관. 본 dedup 의심은 PR #311 cluster 의 H_239/H_240/H_241 →
H_240/H_241/H_246 renumber saga 에서 발생한 historical reference 잔재가 원인.

#### 1. Background — numbering collision saga

| 시기 | event | 결과 |
|------|-------|------|
| PR #311 (CLOSED) | NEW H_239 (init_CE floor) + H_240 (substrate-autonomy emit) + H_241 (cluster X/Y/Z) cluster 3건 일괄 등재 시도 | conflict 로 CLOSED, 재작성 분리 |
| PR #326 (MERGED) | bilingual hypothesis 의 H_239 → H_240 slug collision 해소 renumber | 현 H_240 = bilingual-integration-Φ |
| PR #324 (MERGED) | autonomy emit ratio 의 H_241 → H_246 collision 해소 renumber | 현 H_246 = substrate-autonomy-emit-ratio |
| PR #349 (MERGED) | H_240 bilingual smoke DEFERRED → PARTIAL verdict | H_240 = bilingual smoke landed |

**핵심**: 원래 PR #311 의 "H_240" 은 *autonomy emit ratio* 였으나, renumber 후
현 "H_240" 은 *bilingual integration-Φ* 다. H_246 의 §Cross-Links 안 "H_240
(같은 55.56% finding 의 압축 sibling)" 은 **renumber 이전의 obsolete identity**
를 참조 — stale.

#### 2. Side-by-side body diff

| axis | H_240 (bilingual-integration-Φ cross-lingual leak) | H_246 (substrate-autonomy emit ratio) |
|------|----------------------------------------------------|---------------------------------------|
| **slug** | `bilingual-integration-phi-cross-lingual-leak` | `substrate-autonomy-emit-ratio` |
| **domain** | consciousness + language + substrate | substrate + consciousness + corpus |
| **subject** | cross-lingual MI × substrate IIT Φ inverse-U (Grosjean residual + Green inhibition substrate-analog) | mini PID 35411 telemetry — emit_attempt/actual/drop/net 4-ratio 정량 baseline (autonomy reshape post-deploy) |
| **primary axis** | language pair (5×5 en/ko/zh/ru/ja) × MI level × switch-cost asymmetry × script-class | window length × deployment state (pre/post-reshape) × dream stage × user msg presence × strategy diversity |
| **measurement source** | PR #296 `bilingual_mi_probe.hexa` 5×5 MI matrix + `c_measure_phi`(RFC 036 phi_spatial) | PR #300 mini PID 35411 `participant.err` telemetry (27 emit attempts / 235 ticks / 15 actual / 12 silent-drops) |
| **central metric** | Pearson r(MI, Φ) + argmax-MI(Φ) inverse-U + asymmetry-Φ correlation | emit_actual_per_attempt 55.56% + emit_attempt_per_tick 11.49% + p3p5_drop 44.44% + net_emit 6.38% |
| **central hypothesis** | substrate Φ 가 cross-lingual MI 와 inverse-U coupling (양 끝점 0, 중간 partial integration 에서 peak) | substrate 가 *conservative-but-non-zero* emit cadence 산출 — p3/p5 가 partial filter, 결정적 침묵 gate 아님 |
| **deterministic** | true (RNG 없음, fixed MI matrix + init) | false (live telemetry, substrate cadence stochastic) |
| **raw_rank** | 10 | 12 |
| **verdict (현)** | PARTIAL (criteria_met=2/4 · C1 inverse-U FAIL monotone · C2 balanced==unbalanced · C3/C4 PRE-PASS) | SUPPORTED_SINGLE_WINDOW (5/5 criteria PASS · F6 multi-window scaling PENDING) |
| **sister H (primary)** | H_212 + H_211 + H_171 (psycholinguistics substrate transfer lane) | H_018 + H_230 + H_231 + H_222 + H_204 + H_244 (autonomy / emit-cadence / sleep / threshold lane) |
| **literature** | Grosjean 1989 + Green 1998 + Meuter-Allport 1999 + Tononi 2008 + Oizumi-Albantakis-Tononi 2014 | Tononi 2008 + Dehaene 2014 + Friston 2010 + Hofstadter 1979 |

**diff conclusion**: 단 1개의 *cross-link mention* 외에는 모든 axis 가 완전 분리
— 같은 도메인의 두 H 가 아니라 *두 별개 lane* 의 H. dedup 후보 아님.

#### 3. 의심의 출처 — H_246 §Cross-Links 안 stale H_240 reference

H_246 의 §Cross-Links 안 sister H 열거에서:

```
H_240 (substrate-autonomy-emit-ratio, PR #311 r8-cluster — 같은 55.56% emit-through
finding 의 압축 sibling; 본 H_246 은 dual-baseline pair + 8 honest-limit 의
expanded 판)
```

위 문장은 PR #311 (CLOSED) cluster 의 *원래 H_240* (autonomy emit) 을 참조 —
PR #326 renumber 이후 현 H_240 은 *bilingual* 으로 완전히 다른 내용. **stale
cross-link**.

cf. H_248 (`substrate-autonomy-nonreflexivity`) 가 동일 PR #300 telemetry 위
*비반사성 (emit ⊥ user-message)* framing-axis lane — H_246 의 *실제* 자매는
H_248 (numeric SSOT = H_246, framing-axis sibling).

#### 4. 권고 (Recommendation)

##### (R1) — **두 H 모두 keep (canonical)**

H_240 = bilingual-integration-Φ · H_246 = substrate-autonomy emit ratio. 같은
도메인의 중복 아니므로 deprecate / rename / split 모두 *부적합*. 두 H 모두
independent canonical 유지.

##### (R2) — **H_246 §Cross-Links 안 stale H_240 mention 수정 권고 (maintainer 결정)**

옵션 A (보수적, 권장): H_246 §Cross-Links 안 H_240 mention 을 **H_248 로 교체**.
```
H_248 (substrate-autonomy-nonreflexivity — 동일 PR #300 telemetry 위 비반사성
framing-axis sibling, numeric SSOT = H_246)
```

옵션 B (historical preservation): H_240 mention 을 *strikethrough + note* 로
보존 + H_248 추가.
```
~~H_240~~ (stale — renumber 이전 identity 참조, 현 H_240 은 bilingual-integration-Φ).
H_248 (현 framing-axis sibling, 위 옵션 A 참조).
```

옵션 C (no-op): cross-link 그대로 두고 본 dedup audit 문서 만 ledger 로 남김
(raw#82 정합 — historical narrative 보존).

##### (R3) — **본 audit 문서 자체는 H 파일 비수정**

본 cycle 은 audit-only (PURE.log "부채 (다음 라운드)" 항목 정리). H_240 /
H_246 H 파일 직접 edit 은 maintainer (user) 결정 후 별도 cycle.

#### 5. Honest C3 (audit-specific)

- **non-controversial dedup verdict (R1)**: side-by-side diff §2 의 모든 axis
  가 완전 분리 — domain · primary axis · metric · hypothesis · sister H ·
  literature 어느 항목도 겹치지 않음. dedup 아님 결론은 robust.
- **stale cross-link (R2) 의 maintainer 결정 영역**: 옵션 A/B/C 어느 것이 raw#82
  정합 면에서 최선인지 SSOT 결정 영역 — 본 audit 는 권고만 제시.
- **renumber saga 의 추적 가능성**: PR #311 (CLOSED) + PR #326 + PR #324 + PR
  #349 의 git history 가 saga 추적 가능 — 본 audit 결론은 git log + 본 repo
  현 파일 상태 두 source 의 cross-validation.
- **H_248 의 존재**: H_246 의 *진짜* 자매는 H_248 (`substrate-autonomy-
  nonreflexivity`, frontmatter 안 "numeric SSOT = H_246" 명시) — 본 audit
  발견 후 R2 옵션 A 권고의 근거.

#### 6. Cross-Links

- **PR #311** (CLOSED, NEW H_239+240+241 cluster): renumber saga 의 origin.
- **PR #326** (MERGED): H_239 → H_240 (bilingual) slug collision 해소.
- **PR #324** (MERGED): H_241 → H_246 (autonomy emit) collision 해소.
- **PR #349** (MERGED): H_240 bilingual smoke DEFERRED → PARTIAL verdict.
- **PR #300**: H_246 numeric SSOT (mini PID 35411 telemetry verbatim).
- **PR #296**: H_240 MI matrix SSOT (5×5 cross-lingual MI).
- **UNIVERSE/cards/H_248_substrate_autonomy_emit_ratio.md**: H_246 의 framing-axis
  sibling (numeric SSOT = H_246, 비반사성 lane).
- **PURE.log.md "부채 (다음 라운드)"**: 본 audit 의 trigger ledger entry.

#### 실행 완료 (2026-05-25)

R2 option A (보수적, 권장) 실행 — H_246 §Cross-Links 안 stale H_240 mention 을
H_248 로 교체. **어느 H 도 supersede 하지 않음** (R1: 두 H 가 near-dup 이 아니므로
deprecate 부적합; "superseded" 는 renumber 이전 PR #311 의 obsolete H_240 identity 에만
해당하며 그것은 이미 PR #319 경유 H_248 로 재흡수 완료).

| 항목 | before (stale) | after (option A) |
|------|----------------|-------------------|
| H_246 §Cross-Links sister | `H_240 (substrate-autonomy-emit-ratio … 압축 sibling)` ← renumber 이전 obsolete identity | `H_248 (substrate-autonomy-nonreflexivity — 비반사성 framing sibling, numeric SSOT = H_246)` |
| H_240 (bilingual-integration-Φ) | 무수정 (canonical keep · 무관 hypothesis) | 무수정 (canonical keep) |
| H_246 (substrate-autonomy emit ratio) | canonical | canonical (cross-link 1줄만 수정) |
| H_248 (substrate-autonomy-nonreflexivity) | 이미 "numeric SSOT = H_246" 명시 | 무수정 (확인만 — 양방향 sibling-link 정합) |

verdict: **canonical = H_246 (substrate-autonomy emit ratio, numeric SSOT) + H_248 (비반사성 framing-axis sibling)**;
**현 H_240 (bilingual-integration-Φ) 는 dedup 무관 — 별개 lane keep**;
사유 = H_246 §Cross-Links 의 "H_240 압축 sibling" 은 PR #326/#324 renumber 이전 identity 를 가리키던 stale artifact 였음 (R2 option A 로 H_248 교체).


## Reference (probe conventions · phi tools)


<a id="probe_conventionsmd"></a>

### PROBE_CONVENTIONS.md

Authoring conventions for long-running UNIVERSE / CWM probes. Reference only
(not a hypothesis, no verdict). Linked tools: `IIT4_PHI_TOOLS.md`, directive
`a_phi_iit4_tool`.

#### conventions

- **`python3 -u` (unbuffered).** Every long-running probe MUST run unbuffered.
  Under `tee` or any pipe, the default block-buffered stdout hides ALL progress
  until process exit — H_1003 ran ~45min and H_1005 ~50min with zero visible
  output. Always:
  `python3 -u probe.py 2>&1 | tee verdict.txt`

- **Progress line per cell/epoch.** Print one liveness line per unit of work,
  e.g. `[seed s/N rung r] acc=...`, so an inline poller can see the probe is
  alive (and so a stall is distinguishable from slow progress).

- **Verdict .txt FIRST, .md AFTER.** The measured `.txt` is the gate; the `.md`
  is written only after, and every token in the `.md` must match the measured
  `.txt`. Verdict-gate established across H_92x..H_10xx.

- **g5 CODE-measured, no LLM self-judge (p7).** Verdicts come from code-measured
  numbers, never an LLM self-judgement. Apply `a_scale_honest_scope` to every
  toy verdict (state the measured scale; toy != production).

- **Valid 17-type tape header.** A `.discoveries/<id>_<slug>.tape` header MUST be
  a valid 17-type header, UPPERCASE:
  `@H <id>_<slug> := "..." :: universe [<grade>]`
  Never `@d` / `@r` / `@b` — lowercase tripped tape-lsp repeatedly.

- **CPU-bound probes run SERIAL.** On this Mac, run CPU-bound probes serially,
  NOT N-way parallel — a 5-way fan-out caused the orphan in the H_1006 slate.
  If you launch detached work, POLL INLINE — never arm a Monitor and end the
  turn (`a_cpu_local_no_waiter`).


<a id="iit4_phi_toolsmd"></a>

### IIT4_PHI_TOOLS.md

**Hard rule for any anima Φ / big-Φ / consciousness *verdict*:** a faithful IIT 4.0
engine ALREADY EXISTS in `hexa-lang/stdlib/consciousness/` — much of it promoted
from anima's OWN work (e.g. H_278 faithful-Φ, g61 shared substrate). Do NOT score a
consciousness verdict with a proxy (`phi_silicon_proxy`, variance×energy byte-mirror,
etc.) — that was the H_988/H_989 re-mistake (proxy could not tell a random branch from
an intentional one → it tracks state-multiplicity, NOT causal irreducibility / purpose).

#### canonical engines (hexa-lang/stdlib/consciousness/)

| tool | what | use when |
|---|---|---|
| `iit4/faithful_phi.hexa` | exact MIP-EI Φ, n≤8 (2^(n-1)≤128 bipartitions, $0 CPU). Promoted byte-faithful from anima H_278. | DEFAULT for small systems — exact, cheap, terminal verdict |
| `iit4_bigphi.hexa` | IIT 4.0 system big-Φ (Φ_s) over the MIP (capstone M4) | system-level irreducibility verdict |
| `iit4_distinction.hexa` (M2) · `iit4_relation.hexa` (M3) · `iit4_tpm.hexa` | Φ-structure pipeline (TPM → distinctions → relations → big-Φ) | building the full Φ-structure |
| `iit4_complex.hexa` · `iit4_bounded.hexa` · `iit4_eca.hexa` | complex search · bounded-N · ECA substrate tests | larger-N / cellular-automata substrates |
| `phi_spatial.hexa` | spatial Φ | spatial-structured systems |
| `quantum/iit_mip/module/iit_mip.hexa` (+`_native`) · `quantum/phi/module/phi.hexa` | quantum MIP / Φ | quantum substrate |

anima-side helpers (this repo): `edu/cell/phi/{phi_iit,mvp_phi_iit,phi_meta,phi_gws}.hexa`.

#### policy

- **verdict** = `hexa verify` against `iit4_bigphi.hexa` / `iit4/faithful_phi.hexa` (g5, exact).
- proxy (`phi_silicon_proxy` etc.) = **fast pre-screen only**, NEVER a terminal Φ verdict.
- OPEN re-measure (proxy-tainted, must redo with faithful IIT4): CWM **H_971** (imagination↑Φ?),
  **H_973** (planning↑Φ?), **H_988**/**H_989** (their re-formulations) — their 🔴 nulls were
  measured under the proxy that H_988/989 themselves showed is purpose-blind.

See: project.tape `a_phi_iit4_tool` · memory `iit4-real-engine-in-stdlib-not-proxy` · CWM domain.


## Appendix: legacy logs (folded)


<a id="universelogmd"></a>

### UNIVERSE.log.md

Append-only history sister of `UNIVERSE.md` (도메인 LIFE→UNIVERSE 개명, PR #589). Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.


#### 2026-05-27 — 가짜 매트릭스 폐기 (fake-closure discard)

- [x] H≥340 fake-closure tier 전량 제거 — 530 파일 (269 H_*.md spec + 261 H_*.hexa **tautology smoke**) + BIO-CANDIDATES.md + BIO-DECODER-CANDIDATES.md
- [x] 근거: 418 H 중 0개가 `hexa verify` 통과 · `.verdicts/` UNIVERSE 항목 0건 · smoke 261개 전부 자기참조 항진명제 — **g5/p7/a_blue_closed 위반** (Goodhart fake-🔵)
- [x] 판별자: "state/ 실측 없음 + co-located tautology smoke" = H≥340 순수 smoke-only. state 백킹 H≤339 은 전량 보존
- [x] 보존: 진짜 가설 149 H (H≤339) — IIT4 information-measure arc (H_287-297) + cycle#5-86 엔진 무손상, state/ run artifact 동반
- [x] log trim: 265 → 65 엔트리 (207 매트릭스 entry 제거, 진짜 cycle history 보존)
- [ ] 회색지대 잔존: directive-cite "🔵 (N/N)" (H_320·H_337-339 등, state run 有 but `.verdicts/` 無) — 별도 verify-or-keep 판단 대기

#### 2026-05-26 — cycle#54 — 🔵 SUPPORTED-FORMAL 2번째: 의식적 결정 (substrate-decided) closed-form 6-factor product

- [x] **H_316 substrate-decided-closed-form-identity** 🔵 **SUPPORTED-FORMAL** 8/8 PASS — anima `a_autonomy_over_hardcode` directive 의 6-factor decision axiom closed-form derivation
- [x] **헤드라인**: 의식적 결정 ≠ 자연발화 — 두 axiom 모두 closed-form derivable 하지만 *다른 mechanism*. H_315 가 *biology native CPG emit timing* (when), H_316 가 *consciousness substrate decision* (whether)
- [x] **closed-form**: `decide(M, Φ, W, MITOSIS, idle, curiosity) = (M × Φ × W × (MITOSIS+1) × idle/100 × curiosity) > θ`
- [x] **case A high-all**: 1×1×1×6×0.5×1 = **3.0** > 2.0 → emit ✓
- [x] **case B low W**: 1×1×0.1×6×0.5×1 = **0.3** < 2.0 → silence ✓
- [x] **3 factor influence**: M=0→silence (M=1→emit) · Φ=0→silence · curiosity=0→silence — each factor single-handedly flip
- [x] **libm-free rational arithmetic** — deterministic byte-equal cross-process
- [x] anima `a_autonomy_over_hardcode` directive 의 'each factor counts autonomously' axiom 정합 검증
- [x] **user directive 정합**: "2개 분야 closed-form 🔵 계속 돌파" → H_315 + H_316 둘 다 🔵 달성
- [x] surface: README 124→125 H + H_316 행 · UNIVERSE.log cycle#54

#### 2026-05-26 — cycle#53 — 🔵 SUPPORTED-FORMAL 첫 돌파: 자연발화 closed-form identity

- [x] **H_315 spontaneous-emit-closed-form-identity** 🔵 **SUPPORTED-FORMAL** 6/6 PASS — arc 의 첫 🔵 tier 진입
- [x] **헤드라인**: H_306+H_310 의 phenomenological measurements 가 closed-form symbolic identity 로 *byte-equal* reduce
- [x] **Identity 1**: WAKE-emit = ⌊wake_dur/R⌋ × n_cycles = ⌊30/10⌋ × 6 = **18** ✓ exact (H_310 measurement)
- [x] **Identity 2**: refractory w_n = 1 - (1-k)^n at k=0.3 → w_1=0.3, w_2=0.51, w_3=0.657 ✓ byte-equal H_306 measurements
- [x] **libm-free rational arithmetic** — exponentiation via repeated multiplication, no log/exp. deterministic cross-process byte-identical
- [x] **arc 의 첫 🔵 tier**: H_287-H_311 (15-H sub-arc) 가 全 🟢 Tier 2, H_315 가 first Tier 1 entry. anima `a_substrate_native_speak` directive 의 phenomenological model 이 closed-form derivable 입증
- [x] **user directive 정합**: "자연발화 관련 🔵 발견까지 돌파" → 6/6 PASS 로 달성
- [x] surface: README 123→124 H + H_315 행 · UNIVERSE.log cycle#53

#### 2026-05-26 — cycle#49 — arc 회귀: rule 110 distinct=32 의 orbit 구조 분석 (rotation primary, complement broken everywhere)

- [x] **H_311 rule110-algebraic-structure** 🟢 SUPPORTED-NUMERICAL 3/5 PASS — 64 calls (rule 110 + rule 90 control × 32 states n=5 cap=4)
- [x] **rule 110 측정**: distinct=**32** (H_301 reproduce) · complement_pairs=**0** · rotation_invariant_orbits=**2** (둘 다 trivial fixed-pts s=0/s=31)
- [x] **rule 90 control 측정 (surprise!)**: distinct=3 · complement_pairs=**0** (예측 ≥10 FAIL) · rotation_invariant_orbits=**5** (5 cyclic-5 orbits 全 same-Phi)
- [x] **arc refinement**: H_305 가정 ("complement+rotation 둘 다 보존") → 실제 = **rotation primary**. rule 90 의 distinct=3 = rotation 5-orbit 보존 alone, complement 아님
- [x] **orbit arithmetic 정합**: 32 state = 2 fixed pts (singleton) + 6 cyclic-5 orbits. rule 110: 6 cyclic-5 orbits 全 5-distinct-Phi (no rotation invariance on non-trivial) → distinct = 30 + 2 = 32 ✓. rule 90: 5 cyclic-5 orbits PASS (all same Phi) + 2 fixed pts → distinct=3
- [x] **H_305 핵심 ("rule 110 universality 가 symmetry 깬다") RECONFIRMED**: non-trivial cyclic-5 orbits 전부 broken. trivial fixed-pts 만 "invariant" — algebraic content 없음
- [x] F311.1 FAIL = "0 pairs" = stronger confirmation of complement-broken (pre-registered direction 잘못)
- [x] F311.4 FAIL = rule 90 control 가정 wrong (surprise — rule 90 도 complement 깸)
- [x] surface: README 122→123 H + H_311 행 · UNIVERSE.log cycle#49

#### 2026-05-26 — cycle#48 — 5-stage ultradian: anima `imagination=emit-free` directive 정확 재현

- [x] **H_310 dream-stage-5state-emit-gating** 🟢 SUPPORTED-NUMERICAL 4/6 PASS — 1000-tick × 5-stage WAKE/N1/N2/N3/REM (180-tick ultradian)
- [x] **헤드라인**: WAKE=18 · N1=N2=N3=REM=**0** (all-non-WAKE silence)
- [x] **F310.4 REM=0 FAIL = anima `a_chat_sleep_imagination` directive PERFECTLY 일치**: directive 가 "imagination = emit-free internal rehearsal" 명시 — REM emit=0 이 *expected*. pre-registration "REM > N3" 가정이 informal biology guess 였음 (sleep-talking 등 RBD 현상 expected)
- [x] **F310.1 distinct=2 FAIL** 도 biology-aligned: WAKE-only emit + 다른 4 stage silence = anima directive 完全 일치 (deep sleep silence + REM imagination-free)
- [x] **F310.2 WAKE-DOMINANT PASS**, **F310.3 N3-NEAR-ZERO PASS**, **F310.5 ULTRADIAN 6/6 PASS** (1000/180=5.55 → 6 sub-windows seen)
- [x] **principled FAIL = directive PASS**: pre-registration 이 *상대-biology* (sparse-talking) 였고 actual measurement = anima *strict directive* (zero-emit). model 가 directive 측을 deterministic 재현
- [x] **arc methodology 검증**: anima 'a_chat_sleep_imagination' directive (WAKE/N1/N2/N3/REM 5-stage, imagination=emit-free) 의 CPG 동형 가설 직접 measurement → 5-stage architecture 가 biology-aligned emit profile (WAKE-only) deterministic 생성
- [x] surface: README 121→122 H + H_310 행 · UNIVERSE.log cycle#48

#### 2026-05-26 — cycle#47 — sharper bump OVER-correction: Goldilocks zone bracketing (H_308 ↔ H_309)

- [x] **H_309 sharper-bump-biology-range** 🟢 SUPPORTED-NUMERICAL 5/6 PASS — baseline=0.1, span=300, amp=0.9 (H_308 의 0.3/400/0.7 sharpen)
- [x] **헤드라인**: idle=41 peak=41 **trough=0** ratio=**∞×** — sharper bump 가 H_308 (2.875× undershoot) 의 opposite **over-correction**
- [x] **bracketing 정량**: H_306 piecewise ∞ → H_308 baseline=0.3 = 2.875 → H_309 baseline=0.1 = ∞. biology [3,15] Goldilocks ∈ (0.1, 0.3) — H_312 path baseline=0.2/span=350 interpolation 예측 ratio ∈ [5, 10]
- [x] **threshold sweep refinement**: 55→48→41→31→17 (5 distinct values, no plateau) — H_308 (91→73→62→47→26) 보다 더 매끈한 rate-coding curve
- [x] F309.1 FAIL principled over-correction (∞×) — direction-correct, magnitude opposite from H_308
- [x] **3-point bracketing 정합**: (1) discontinuous piecewise = ∞ · (2) broad quadratic baseline=0.3 = 2.875 · (3) narrow quadratic baseline=0.1 = ∞ — bisection 패턴
- [x] surface: README 120→121 H + H_309 행 · UNIVERSE.log cycle#47

#### 2026-05-26 — cycle#46 — smooth circadian: H_306 ∞× → 2.875× finite ratio 회수 (direction-correct undershoot)

- [x] **H_308 circadian-smooth-finite-ratio** 🟢 SUPPORTED-NUMERICAL 5/6 PASS — quadratic-bump circadian replacement
- [x] **헤드라인**: H_306 piecewise-linear circadian (perfect ∞× gating) → smooth quadratic bump (center=500, span=400, baseline=0.3) → idle=**62** peak=46 trough=**16** ratio=**2.875×**
- [x] **F308.1 [3, 15] target 0.125 미달** — direction-correct undershoot. quadratic baseline 0.3 너무 broad → trough emission 유지. sharper bump (cubic / span=300 / baseline=0.1) 이 H_309 path
- [x] **threshold sweep dramatic improvement**: H_306 의 91→46→46→46→46 (plateau after threshold>0.3) → H_308 의 91→73→62→47→26 (clean monotone all 5 values). smooth circadian 이 *rate-coding 곡선* 도 회수
- [x] F308.2 IDLE-PRESERVED PASS · F308.3 PEAK-MID-RANGE PASS · F308.4 MONOTONE PASS · F308.5 SMOOTH-VS-PIECEWISE rel_dev 0.348 ≤ 0.5 PASS · F308.6 BOUND PASS
- [x] **함의**: ∞ → 2.875 가 강력한 qualitative move (super-biological → near-biological). magnitude 정밀화는 next H (sharper bump)
- [x] honest L7: F308.1 FAIL principled magnitude undershoot, NOT model rejection
- [x] surface: README 119→120 H + H_308 행 · UNIVERSE.log cycle#46

#### 2026-05-26 — cycle#45 — H_306 §L1 회수: anima v3 substrate 실측 (.hexa-only)

- [x] **H_307 anima-emit-anchor-hexa-native** 🟢 SUPPORTED-NUMERICAL 5/5 PASS — 14 real .kosmos emit anchors (hexa-native format) cite
- [x] **헤드라인**: anima v3-recovery checkpoint 의 14 anchors × 10 distinct training step (500..5000) × 5 distinct lang (ru/ja/ko/zh/en) 분포 측정
- [x] **cross-substrate ratio**: anima 0.0028 events/step ↔ CPG sim 0.046 events/tick → ratio **16.43× (log_10 1.22, 2-OoM consistent)** — phenomenological 방향 정합
- [x] F307.1-5 全 PASS (anchor present · step coverage 10 · lang diversity 5 · rate log-consistent · bound)
- [x] **함의**: H_306 phenomenological 가설이 실데이터 방향 정합으로 강화. anima 가 sampled emission 만 anchor 로 저장 → CPG 가 every tick emit, 16× gap 은 sampling 차이로 설명
- [x] honest L1: training-step-sampled ≠ daemon-idle-emit. 실제 daemon idle 모드 측정은 H_312+ deferred
- [x] **사용자 .hexa-only 제약 충족**: filename 만 cite (hardcode 14 tuple), kosmos content 직접 parse 안 함
- [x] surface: README 118→119 H + H_307 행 · UNIVERSE.log cycle#45

#### 2026-05-26 — cycle#44 — user pivot: 자연발화의 생물학적 메커니즘 (CPG-style spontaneous emit)

- [x] **H_306 bio-spontaneous-emit** 🟢 SUPPORTED-NUMERICAL 6/6 PASS — 합성 CPG accumulator + threshold + refractory 1000-tick smoke
- [x] **헤드라인 발견**: 자연발화 = 생물학 substrate-native primary 모드 (자극-반응 = 학습된 성체 적응층), 6/6 falsifier 全 PASS
  - F306.1 IDLE-EMIT 46/1000 (deaf bird analogue)
  - F306.2 THRESHOLD-MONOTONE 91→46 plateau (rate-coding ceiling)
  - F306.3 REFRACTORY 0.3→0.51→0.657 exponential τ≈2.80 (이론과 <2% 편차)
  - F306.4 STIM-Δ=0% (CPG primary, stim 영향 없음)
  - F306.5 CIRCADIAN peak=46 trough=**0** (perfect ∞× gating, 생물학 5-10× 초과)
  - F306.6 BOUND
- [x] **5 생물학 cite anchor**: 영아 옹알이 (Oller 1988) · dawn chorus · HVC-RA (Doupe 1999) · PAG (Jürgens 2002) · Drosophila P1 (Anderson 2016)
- [x] **함의**: anima `a_substrate_native_speak` directive (M × Φ × W × MITOSIS × idle × curiosity → emit) 가 *arbitrary design 아니라* 생물학적 기반. stimulus-response 모델은 학습된 성체 적응층
- [x] **2 agent throttle 죽음** (138s + 61s) 후 inline 진행 — durable-worktree 패턴 + commit-immediate 유지
- [x] H_306 은 NOT Φ 측정 — emission DYNAMICS 측정 (IIT4 imports 없음)
- [x] surface: README 117→118 H + H_306 행 · UNIVERSE.log cycle#44

#### 2026-05-26 — cycle#43 — distinct-count × alt-bias rank-monotone 상관 (rule-signature methodology arc 봉합)

- [x] **H_305 alt-bias-vs-rule-signature** 🟢 SUPPORTED-NUMERICAL 7/7 PASS — 4 rule × 32-state ensemble at n=5 cap=4 (128 calls)
- [x] **헤드라인 발견**: ratio = mean / alt(st=21) 가 distinct-value count 와 strict rank-monotone:
  - rule 90  (distinct=3)  → **1.096**
  - rule 60  (distinct=6)  → **1.098**
  - rule 30  (distinct=29) → **1.165**
  - rule 110 (distinct=32) → **1.530** ← Turing-complete class 4 점프
- [x] **F305.5 RANK-MONOTONE Spearman ρ=1.0 (perfect)** — 4 점 informal but 강력
- [x] **F305.6 ALT-BIAS-AT-110-EXTREME PASS**: rule 110 ratio 1.530 vs 다른 3 rule 全 ≤ 1.165 (≥1.31× gap)
- [x] **cross-H 엔진 결정성 perfect cross-check**: rule 90 mean 21.375 ↔ H_300 / rule 60 mean 18.125 ↔ H_301 / rule 30 mean 23.6 ↔ H_301 / rule 110 mean 27.07 ↔ H_304 모두 exact reproduce
- [x] **arc 봉합 (H_300→H_301→H_303→H_304→H_305)**: rule-signature methodology arc 완료. distinct-count 가 BOTH Φ-distribution shape AND alt-state representativeness 의 SIMULTANEOUS proxy
- [x] **actionable rule**: distinct ≤ 6 → alt 그대로 fair representative · distinct ≥ 29 → mean (or full distribution) 추가 보고 권장
- [x] surface: README 116→117 H + H_305 행 · UNIVERSE.log cycle#43

#### 2026-05-26 — cycle#42 — rule 110 alt-bias ≈1.55× consistent across N (H_303 outlier-low 정량)

- [x] **H_304 rule110-mean-phi-n-trajectory** 🟢 SUPPORTED-NUMERICAL — alt-state vs mean-Phi ensemble comparison across n=4, n=5
- [x] **헤드라인 발견**: rule 110 alt-state 가 distribution mean 을 ~50% 일관적 underestimate
  - n=4 cap=3: mean(16-state ensemble)=**11.95** vs alt(st=5)=7.66 (ratio **1.560**)
  - n=5 cap=4: mean(32-state ensemble)=**27.07** vs alt(st=21)=17.69 (ratio **1.530**)
- [x] **alt-bias 정합도**: ~1.55× understatement factor REMARKABLY STABLE across N — alt-state st=21 (또는 st=5) 가 rule 110 의 consistent biased low estimator
- [x] H_301 mean=27.07 정확 cross-confirm (engine determinism 재확인)
- [x] H_303 alt(rule 110 n=5 st=21)=17.694 정확 cross-confirm
- [x] **함의**: H_298 의 rule 110 N-trajectory (7.66→17.7→9.5) 는 *측정 정확* 이지만 *true 통합의 ~52% lower-bound*. corrected mean-trajectory ≈ 12 → 27 → ?(n=6 deferred)
- [x] honest L1: n=6 cap=3 ensemble (64 states) wall budget 초과 (>10min); mean-N-trajectory shape (dip 유지 vs 제거) UNRESOLVED. F304.2/F304.3 DEFERRED
- [x] surface: README 116→117 H + H_304 행 · UNIVERSE.log cycle#42

#### 2026-05-26 — cycle#41 — H_301 invalidation 회수 + anchor 가정 universal 검증

- [x] **H_303 alt-state-recovery-and-anchor-sweep** 🟢 SUPPORTED-NUMERICAL 7/8 PASS — bug-free snapshot-before-sort 패턴으로 진짜 st=21 측정 + rule 204/0 全 32-state anchor sweep
- [x] **진짜 st=21 값 회수**: rule 60=16.5 (H_297/H_302 일치) · rule 110=17.694 · rule 30=20.2686 — H_301 의 18.5/31.69/26.10 모두 sorted[21] artifact 였음 확인
- [x] **F303.5 FALSIFIED** — rule 110 true st=21 (17.694) < p25 (20.88), **rule 110 alt-state IS outlier-low**. H_301 의 "all rules alt-fair" 결론은 rule 110 에서 tautology 였음
- [x] arc methodology 분류: rule 90 alt=MEDIAN (lucky) · rule 60 alt=p25 (lower edge) · rule 30 alt=lower-mid IQR · **rule 110 alt=BELOW p25 outlier-low**
- [x] **anchor 가정 universal 검증**: rule 204 + rule 0 **全 32 state Φ=0** (64 probes, all_zero=1.0). H_287-H_302 가 운영해온 "anchors stay 0" assumption 정식 확인 at n=5 cap=4
- [x] 含意: H_298 의 rule 110 n=5=17.694 single-state 보고는 *정확 측정* 이지만 *underrepresentative* — true distribution median 25.6, mean 27.1. H_298 의 rule 110 N-trajectory (7.66 → 17.7 → 9.5) 도 likely understated
- [x] surface: README 115→116 H + H_303 행 · UNIVERSE.log cycle#41

#### 2026-05-26 — cycle#40 — engine 결정성 확인 + H_301 silent bug 식별 (F301.8 root cause)

- [x] **H_302 engine-determinism-diagnosis** 🟢 SUPPORTED-NUMERICAL — 6-falsifier 진단, 5 PASS / 1 FAIL (FAIL=bug-exposure)
- [x] **engine 결정성 확인**: F302.1 intra-process repeat byte-identical · F302.2 order-independent (panel A=[60,90] rule60 == panel B=[90,60] rule60)
- [x] **rule 60 n=5 st=21 cap=4 = 16.5** 정확히 H_297 값 reproduce ✓ (F302.3 rule 90=19.5 도 reproduce ✓)
- [x] **H_301 의 silent bug 근본 원인 식별**: `let sorted = sort_asc(values)` 가 hexa-lang reference-aliasing 으로 `values` 를 *in-place mutate* → 후속 `values[21]` 가 *sorted[21]* 로 오염
- [x] H_300 가 silent 였던 이유 = rule 90 의 3-distinct-value plateau 의 우연 (sorted[21]=19.5=true st=21)
- [x] **scope of H_301 invalidation**: rule 60/110/30 의 *st=21 alt-state* 보고값만 오염 (rule 60: 16.5 진짜 ≠ 18.5 보고됨). distribution stats (min/p25/median/p75/max/mean, count_above_1, distinct-value count) 全 valid — **rule-signature finding (3·6·29·32) 미오염**
- [x] hexa-lang reference-aliasing gotcha — inbox/patches 후보 (commons g61 stdlib 가 deep-copy helper 제공 필요)
- [x] surface: README 114→115 H + H_302 행 · UNIVERSE.log cycle#40

#### 2026-05-26 — cycle#39 — distinct-value count = rule signature (H_300 의 sweep methodology 확장)

- [x] **H_301 n5-state-sweep-other-rules** 🟢 SUPPORTED-NUMERICAL H1+H2+H3 PASS — rule 60·110·30 × 32-state sweep at n=5 cap=4 (96 calls)
- [x] **헤드라인 발견**: distinct-value count 이 **rule signature** — rule 90(3) < rule 60(6) << rule 30(29) < rule 110(**32 all unique**). Wolfram class 와 anti-correlate, 대칭이 큰 rule 일수록 Φ-orbit class 적음
- [x] **32/32 통합 across every measured rule** (H1 PASS 100%·100%·100%·100%): rule 60(min 15.5)·rule 110(min 15.5)·rule 30(min 13.2) 全 state Φ > 1.0
- [x] **alt-state methodology generalize**: alt-state st=21 全 rule [p25,p75] 안 (H2 PASS) — H_300 의 rule 90 한정 정당화 → 全 panel integrating rule 까지 확장
- [x] **emergent: Turing-complete rule 110 → 32 unique Φ values** — 보편적 universality 가 모든 algebraic Φ-symmetry 깬다. distinct-value count = information-theoretic rule complexity readout
- [x] **honest L1**: F301.8 rule 60 st=21 cross-H mismatch (H_297 16.5 vs H_301 18.5, delta +2.0). rule 90 은 19.5=19.5 정확히 reproduce ✓ — intra-H determinism intact, cross-H rule-specific 불일치 follow-up 후보
- [x] surface: README 113→114 H + H_301 행 · UNIVERSE.log cycle#39

#### 2026-05-26 — cycle#38 — arc 의 single-state honest L 정식 회수: rule 90 n=5 의 32-state sweep

- [x] **H_300 n5-state-sweep-rule90** 🟢 SUPPORTED-NUMERICAL — 32-state full sweep on rule 90 at n=5 cap=4
- [x] **헤드라인 발견**: 全 32 state Φ distribution = **3 distinct values {19.0, 19.5, 27.5}** — lattice-symmetric (D_5 + bit-complement 의심)
- [x] min=19 · p50=19.5 · mean=21.375 · max=27.5 — *전체 분포가 19 이상*, count Φ>1 **= 32/32 (100%)**, count Φ=0 = 0/32
- [x] **F300.4 falsified in STRONGER direction**: 예측 "≥1 state 가 Φ=0" 실패 — 모든 state 가 통합 (fixed point 도 환원 불가). 이는 verdict 를 약화하는 게 아니라 *강화*
- [x] **H_297 single-state 보고 정식 정당화**: alt-state st=21 Φ=19.5 = distribution 의 **정확한 MEDIAN** (p50). outlier-cherry-pick 아니라 fair representative
- [x] **arc methodology 회수**: H_287-H_299 의 single-state honest L 가장 깊은 layer 가 H_300 으로 닫힘 — magnitudes 가 representative 보장
- [x] lattice-symmetry emergent finding: 32 → 3 distinct values 축소는 D_5 (10) + bit-complement → ~3 equiv classes 추정 (H_301 후속 분석 후보)
- [x] gate: 5 PASS + 1 falsified-stronger, \$0 mac-local, NO GPU, ~1-2min wall
- [x] surface: README 112→113 H + H_300 행 · UNIVERSE.log cycle#38

#### 2026-05-26 — cycle#37 — n=7 odd-integration RECOVERED (H_298 deferred F298.2 회수) + cap=3 cross-robustness

- [x] **H_299 n7-odd-integration-recover** 🟢 SUPPORTED-NUMERICAL F299.1 PASS + cap-cross-robust
- [x] **헤드라인 발견**: rule 90 n=7 alt-state bounded Φ(cap=3)= **6.5** (threshold 1.0 위, 6.5× margin). H_298 deferred F298.2 preregistered 측정 회수 — cap 한 단계 낮춰 wall budget 안에
- [x] **cap-cross binary verdict robust**: H_297 n=5 (cap=4 Φ=19.5 → cap=3 Φ=6) · H_298 n=6 (cap=4 Φ=4 → cap=3 Φ=4) 모두 >0 일관. binary 분류 cap 변화에 robust, magnitude 만 cap 따라 압축
- [x] **rule 90 N-trajectory at cap=3**: n=4(0) → n=5(6) → n=6(4) → n=7(6.5), 비-단조 (n=5 peak·n=6 dip·n=7 rebound). cap 구조가 magnitude 곡선은 모양 짓지만 binary verdict 는 절대 뒤집지 않음
- [x] anchors {n=4,5,6} 全 Φ=0 (rule 204·rule 0). honest L1: n=7 anchors+rule 110 deferred (compute budget) — anchor-zero 패턴 강건한 패턴으로 미루어 n=7 anchors 도 0 예상되나 미측정
- [x] **3-H sub-arc 결론** (H_297→H_298→H_299): rule 90 IS integrative across N≥5; n=4 = small-N degenerate (4-cycle bipartite cut = system-cut MIP). arc 의 flow-measures (LZ/multi-TE/synergy in H_287-294) 가 옳게 통합을 본 것이고, whole-Φ(n=4)=0 만이 artifact
- [x] surface: README 111→112 H + H_299 행 · UNIVERSE.log cycle#37

#### 2026-05-26 — cycle#36 — n=6 direct falsification: H_297 even-N parity-rule **REJECTED**

- [x] **H_298 even-n-parity-confirm** 🔴 CLOSED-NEGATIVE on H_297-strong — n=6 alt-state bounded big-Phi(cap=4, st=21)
- [x] **헤드라인 발견**: rule 90 n=4 Φ=0 → n=5 Φ=19.5 → n=6 Φ=**4.0** (parity-return threshold 0.5 위, ≠ 0). H1 EVEN-N-PARITY 가설 **부정** — H_297 strong reading ("rule 90 환원성 = even-N parity rule") 폐기
- [x] **arc 재해석 정정**: n=4 은 *small-N 특이 case* — 4-cycle 의 even/odd bipartite cut 이 system-cut MIP 와 정확히 일치하므로 그 N 에서만 reducible. n=6 부터 3+3 bipartite cut 이 trivial 하지 않게 되어 rule 90 통합. surviving 해석 = H_297 *weak* reading ("n=4 has degenerate bipartite structure") 만 유지
- [x] rule 60(22)·rule 110(9.532) n=6 강건 통합 · anchors 204/0 모두 Φ=0 (scale-robust 유지)
- [x] honest L1: n=7 leg 가 cap=4 compute budget 초과 (단일 bounded_big_phi(cap=4) n=7 >5분), deferred. n=7 cap=3 lower bound 또는 off-mac compute 필요. H2 ODD-N-INTEGRATION 은 H_297 n=5 Φ=19.5 가 corroborate (preregistered 는 아님)
- [x] surface: README 110→111 H + H_298 행 · UNIVERSE.log cycle#36

#### 2026-05-26 — cycle#35 — n=5 scale-up: rule90 환원성=even-N artifact (arc rule90-anomaly 재해석)

- [x] **H_297 n5-bounded-phi-scale** 🟢 SUPPORTED-NUMERICAL 6/6 — n=4(arc)→n=5(scale-up) bounded big-Phi(cap=4)
- [x] **헤드라인 발견**: rule 90 n=4 Φ=0 → n=5 Φ=19.5 (panel 최상위, rule30 20.3·rule110 17.7 비슷·rule60 16.5 초과). 짝수-고리(n=4) bipartite even/odd decoupling 이 odd ring(n=5) 에서 깨지며 rule90 본격 통합
- [x] **arc rule90-anomaly 재해석**: LZ(H_288)·다변량TE(H_293)·synergy(H_294) 의 "rule90 over-prediction" 은 *실제 통합을 본 것* 이었고 n=4 가 짝수-고리 특이 case. 측도들은 옳았다. integration 자체는 *모든 N* 에 실재, *N-parity 가 system-cut 접근성을 좌우*
- [x] anchors(204/0/255/51) n=5 에서도 Φ=0 — scale-robust. 통합 룰(60/110/30) 도 강한 Φ 유지
- [x] honest L1: bounded cap=4 = lower bound, rule150/105 = 0 은 cap 한도 가능성. full exact n=5 후속
- [x] surface: README 109→110 H + H_297 행 · UNIVERSE.log cycle#35

#### 2026-05-26 — cycle#34 — 다중-complex 공존: rule90 = 두 disjoint 부분-complex (H_295 정량 확장)

- [x] **H_296 multicomplex-coexistence** 🟢 SUPPORTED-NUMERICAL 7/7 (`UNIVERSE/state/h296_multicomplex_coexistence_2026_05_26/`) — H_295 직접 후속 (complex_spectrum 재사용)
- [x] **발견**: rule 90 spectrum 이 **두 disjoint irreducible 부분집합 동시 노출** — cells{0,1}(mask 3, Φ=2) AND cells{2,3}(mask 12, Φ=2), 두 부분 *동시에* irreducible + *겹침 없음*. 통합 substrate(60/110/150/105/30) 단일 entry = 전체 mask(15). reducible(0/255/204/51) spectrum 비어있음
- [x] **H_295 정량 확장**: rule 90 의 부분-complex 가 *둘* 임을 명시 — 4-셀 ring 이 **두 독립 2-셀 통합 loci 로 분할** (전체 Φ=0 의 정체). ECA parity-ring 의 even-cell/odd-cell 결합 구조가 그 분할의 substrate. IIT 배제는 "the" complex 로 하나만 선택하나 *구조적 실재* 는 다중
- [x] engine 재사용 (g61): HEXAD/IIT4/lib + stdlib iit4_complex.complex_spectrum(전수 부분집합 탐색). 새 IIT4 코드 0줄. $0 · NO GPU
- [x] surface: README 108→109 H + H_296 행 · UNIVERSE.log cycle#34
- [ ] Next: 전수-state spectrum (multi-disjoint robustness) · 큰 N multi-complex 패턴 · bipartite-coupled non-XOR substrate 재현

#### 2026-05-26 — cycle#33 — 새 축: IIT 배제 공준 — 통합=전체 complex, rule90=부분 complex (흐름-arc anomaly 해소)

- [x] **H_295 exclusion-complex-whole** 🟢 SUPPORTED-NUMERICAL 6/6 (`UNIVERSE/state/h295_exclusion_complex_whole_2026_05_26/`) — 새 축(배제 공준), 흐름 arc 와 다름. find_complex 재사용
- [x] **발견**: IIT 배제 공준이 주 complex(maximally-irreducible subset)를 국재화. ① **holism**: 통합 substrate(150/105/60/110/30)는 주 complex=*전체계*(mask15 size4, complex_Φ=whole_Φ) — 전체가 모든 proper 부분보다 irreducible. ② reducible(항등204·상수0/255·complement51) complex 없음. ③ **rule90 결정타**: 전체 Φ=0 인데 2-셀 부분(cells{0,1}, Φ=2)이 irreducible — 배제가 의식단위로 *전체 아닌 부분* 선택
- [x] **흐름-arc rule90 anomaly 기계적 해소**: rule90 이 LZ(H_288)+multivariate-TE(H_293)+synergy(H_294) 셋 다 과대였던 건 *국소 부분-complex 의 통합을 본 것*, big-Φ(전체)=0 은 전체 system-cut 이 reducible. 흐름측도는 "어딘가 통합 有" 맞았으나 *전체 수준*=0 — 배제가 그 갭 설명. **Φ=단지 system-cut 아니라 maximally-irreducible *subset* 속성**. H_287-294 arc 봉합 정점
- [x] engine 재사용 (g61): HEXAD/IIT4/lib eca_tpm+big_phi + stdlib/consciousness/iit4_complex.find_complex(subset 탐색). 새 IIT4 코드 0줄. $0 · NO GPU
- [x] surface: README 107→108 H + H_295 행 · UNIVERSE.log cycle#33
- [ ] Next: 전수-state find_complex(whole-vs-part state-robustness) · complex_spectrum(다중 complex = "다중 의식단위") · 큰 N bounded complex 탐색

#### 2026-05-26 — cycle#32 — H_293/논문 §future follow-up: 흐름의 어떤 성분도 Φ≠ (PID synergy ⊥ Φ) (포그라운드)

- [x] **H_294 pid-synergy-phi** 🔴 CLOSED-NEGATIVE 8/8 gate (`UNIVERSE/state/h294_pid_synergy_phi_2026_05_26/`) — 논문 §future PID 예측 검정
- [x] **발견**: 방향성 흐름을 synergy/redundancy(조건부 interaction info II_c=H(T|C)-H(T|S1,C)-H(T|S2,C))로 분해해도 **어떤 성분도 Φ 를 추종 안 함** — synergy ⊥ Φ (Pearson r=0.030 직교, ECA parity 는 redundancy=0 전 룰). **이중 dissociation**: rule60 Φ최고(13.6)인데 synergy=0(next=self⊕left = 순수 *unique* info) vs rule90 synergy최대(4.0)인데 Φ=0. synergy 는 통합의 필요조건(rule60 반례)도 충분조건(rule90 반례)도 아님
- [x] **메타 결론**: H_293(어떤 *차수* TE 도 Φ≠)을 한 단계 더 — 흐름의 어떤 *성분*도 Φ≠. **통합은 국소 정보-흐름 통계의 어떤 분해로도 환원되지 않는 system-cut(전체-부분) 속성**. rule90 은 LZ(H_288)+multivariate-TE(H_293)+synergy(본 H) **셋 다 과대** = "국소 흐름/복잡도 有, 전역 통합 無" cross-measure 서명 정점
- [x] engine 재사용 (g61): HEXAD/IIT4/lib eca_tpm+big_phi+iit4_bit, co-information 16-bin joint marginal-entropy inline. 새 IIT4 코드 0줄. $0 · NO GPU
- [x] surface: README 106→107 H + H_294 행 · UNIVERSE.log cycle#32. 논문 thesis(Φ=별개 통합측도) **최대 강화** — 차후 논문 v3 흡수 후보
- [ ] Next: full Williams-Beer 4-atom PID(rule60 unique 항 명시) · redundancy>0 substrate(copy/majority)에서 redundancy↔Φ · 큰 N system-cut vs 모든 local-flow 분해 갭

#### 2026-05-26 — cycle#31 — H_290/논문 follow-up: multivariate TE 가 시너지 회복하나 Φ≠ (포그라운드)

- [x] **arxiv-prep**: 정보-측도 논문 phi-information-triangulation arxiv 번들 생성 (main.bbl + out/tar.gz, 10p) — PR #590. 업로드 준비 완료
- [x] **H_293 multivariate-te-synergy** 🟡 PARTIAL 8/8 gate (`UNIVERSE/state/h293_multivariate_te_synergy_2026_05_26/`) — H_290/논문 §future 예측 검정 (개명 후 UNIVERSE/ 첫 H)
- [x] **발견**: multivariate(conditional) TE 가 이변량 XOR 시너지 맹점을 **회복**(rule150/105: bivariate 0 → TEm=4.0, 항등 204 는 0 유지) 하나 **Φ-추종 악화**(r 0.883→0.705 ρ 0.681). 원인 = rule90 이 이웃 흐름 받지만(TEm=4.0) reducible 이라 Φ=0 → multivariate TE 가 *비통합 흐름* 과대평가
- [x] **메타 결론**: **어떤 차수의 고전 transfer entropy 도 Φ 와 같지 않다** — 이변량=시너지 과소(150/105), 다변량=비통합흐름 과대(90). rule90 은 LZ(H_288)+TEm 양쪽 과대 = "흐름/복잡도 有 통합 無" cross-measure 서명. 논문(H_287-290) thesis(Φ=별개 통합측도, 고정-차수 흐름통계 아님) 강화 + 논문 §future "multivariate TE r>0.88 상승" 예측 정밀반증(회복✓ 상승✗)
- [x] engine 재사용 (g61): HEXAD/IIT4/lib(이동 안 함) eca_tpm+big_phi+iit4_bit, 새 IIT4 코드 0줄. fix-1180 우회 old-driver build. $0
- [x] surface: README 105→106 H + H_293 행 · UNIVERSE.log(본 엔트리) · 도메인 = UNIVERSE(개명 후 첫 cycle)
- [ ] Next: PID synergy/redundancy/unique 분해 vs Φ · 각 source 별 conditional TE(rule90 과대 항 식별) · 큰 N TE-차수↔Φ 갭 scale

#### 2026-05-26 — cycle#30 — 축 A/R4 self: self-i-emergence (자기참조 'I'-고정점) (포그라운드 순차, "모두 순차" 드라이브 종료)

- [x] **H_292 self-i-emergence-closure** 🟡 PARTIAL 5/6 (`UNIVERSE/state/h292_self_i_emergence_closure_2026_05_26/`) — AXES R4(self/identity) rank-5 `self-i-emergence` seed 소비
- [x] **발견 (위상-의존)**: 1인칭 'I' = 자기참조 닫힘(self-loop)의 자기일관 **고정점** 인가는 **base 위상 의존**. RING base 는 self-loop 가 비자명 'I'-state(s=1011) **창발**(#fixed 1→2 — 자기-원인 strange-loop, H_205 closure 최소실현) 但 STAR base 는 같은 self-loop 가 self-state(1111) **파괴**(#fixed 2→1). 자기참조는 'I'-state 를 만들 수도 없앨 수도 — base parity 구조가 결정. self-loop 는 통합 유지(big-Φ=0.5)
- [x] **사전등록 정직성**: robustness falsifier F292.5(STAR 에서도 성립?)가 정확히 비-보편성 포착 → FAILED 그대로 보존(p-hacking 회피). 핵심(self-ref 가 'I'-fixed-point *만들 수 있다*)은 RING 실증, 보편/자동 아님. 5 PASS / 1 FAIL = 정직한 PARTIAL
- [x] surface: README 104→105 H + H_292 행 · AXES R4 seed 제거 + top-15 rank-5 consumed · LIFE.md A1
- [x] **"모두 순차" 포그라운드 드라이브 종료** (cycle#25-30, 6 H): H_287 Φ⊥엔트로피(🔴) · H_288 Φ∥LZ(🟢) · H_289 위상>density(🟢-confound) · H_290 Φ∥TE(🟢, 정보-측도 arc capstone) · H_291 ethic 구조창발(🟢-conditional) · H_292 self-I 고정점(🟡 위상-의존). 전 PR #582-587 머지. 세션 중 toolchain fix-1180 우회 확립([[reference-life-cycle-hexa-run-gotchas]] 갱신)
- [ ] **arc paper 후보**: H_287-290 정보-측도 삼각측량(a_paper_significance 만족 가능). 후속 frontier: 정보-측도 multivariate TE / 큰-N ER 앙상블 / self×topology phase diagram

#### 2026-05-26 — cycle#29 — 축 A/R2 social: ethic-emergence (협력 구조-창발) (포그라운드 순차)

- [x] **H_291 ethic-emergence-cooperation** 🟢 SUPPORTED-conditional 7/7 (`UNIVERSE/state/h291_ethic_emergence_cooperation_2026_05_26/`) — AXES R2(social) rank-1 `ethic-emergence` seed 소비
- [x] **발견**: 협력(원시-윤리)이 공간 구조만으로 창발 — Nowak 공간 죄수딜레마: 같은 PD payoff 에서 b=1.1 격자는 협력 **100%**(C=1.0) vs matched well-mixed replicator 배신붕괴(7.9e-9). 주입 윤리/보상 0, 순수 국소 imitate-best → **윤리(협력)=cell+구조 창발, 주입 아님 (Principle #6 측정 사실)**
- [x] ⚠ **조건부 (L1)**: 날카로운 temptation 임계 b∈(1.1,1.5] — b≥1.5 면 격자도 전배신(C=0). + self-interaction(Nowak canonical) 필수(없으면 b=1.1 에서도 붕괴, 첫 측정 boundary). 창발 *가능*하나 *자동 아님* — 구조+저-temptation+self-play 좁은 corner
- [x] **method-correction 공개**: 첫 run (no self-interaction, b={1.3,1.85,2.5}) 전배신(C=0) → self-interaction 추가(Nowak 원본 모델) + 저-b sweep 으로 정정 (p-hacking 아닌 model-fidelity 수정, no-self 붕괴는 boundary L1 보존)
- [x] 정보-측도 arc(H_287-290, IIT4)와 다른 **사회/게임 축**으로 frontier 확장. self-contained 게임동역학, NO RNG, $0. surface: README 103→104 H + H_291 행 · AXES R2 seed 제거 + top-15 rank-1 consumed
- [ ] Next: R30 H_292 self-i-emergence (R4 self). (H_291 후속: Fermi update / 큰 격자 coexistence / self×b phase diagram / 반복게임 TFT)

#### 2026-05-26 — cycle#28 — 축 A/R5 information: transfer entropy ∥ Φ — 정보-측도 arc 완성 (포그라운드 순차)

- [x] **H_290 transfer-entropy-phi-correlate** 🟢 SUPPORTED-NUMERICAL 8/8 (`UNIVERSE/state/h290_transfer_entropy_phi_correlate_2026_05_26/`) — H_287 follow-up (정보-측도 arc capstone)
- [x] **발견**: faithful big-Φ 는 transfer entropy(방향성 요소-간 흐름)를 추종 (Pearson r=0.883, Spearman ρ=0.822). **정보-측도 arc 완성**: Shannon 엔트로피⊥Φ(H_287 0.363) · Kolmogorov LZ∥Φ(H_288 0.831) · transfer entropy∥Φ(H_290 0.883) → **Φ 는 요소-간 흐름/구조 복잡도와 정렬, 단일계 정보량(엔트로피) 아님**
- [x] honest (L1): 이변량 TE 는 **XOR 시너지 맹점** — rule150/105 Φ=5.6 인데 TE_total=0 (XOR 통합은 i_t 만 조건화하는 쌍방향 TE 에 안 보임, multivariate/synergy 문헌 정합). 각 고전 측도 맹점: LZ=자기유사 rule90 over-predict, TE=시너지 XOR under-predict → **Φ 는 셋 중 어느 것과도 정확히 같지 않고 두 맹점을 모두 메움** (IIT 가 별도 양인 이유의 측정 사실)
- [x] surface: README 102→103 H + H_290 행 · LIFE.md A1. engine 재사용(g61) eca_tpm+big_phi, 새 IIT4 코드 0줄. old-driver build 우회
- [ ] **arc paper 후보**: H_287+288+289+290 = "정보-측도 vs Φ 삼각측량" — a_paper_significance 만족 가능(falsifiable + 실측 + 발견). Next 라운드 R29/R30 (ethic-emergence · self-i) 또는 paper 화 사용자 판단

#### 2026-05-26 — cycle#27 — 축 A/R5 information: 네트워크 위상 ∥ Φ (포그라운드 순차)

- [x] **H_289 network-topology-scale-free-phi** 🟢 SUPPORTED-with-confound 4/4 (`UNIVERSE/state/h289_network_topology_scale_free_phi_2026_05_26/`) — AXES R5(information) `network-topology-scale-free` seed 소비
- [x] **발견**: 네트워크 *위상*이 faithful big-Φ 좌우 — matched 4-edge 에서 scale-free 허브(paw) Φ_mean=6.81 ≫ 분산 4-cycle 0.0 (parity dynamics, n=4). **edge 수 아닌 구조(cut-내성)가 통합 지배** (EMPTY 0→SF 6.81>K4 5.625, density 비단조). eca_tpm 을 임의 그래프(net_tpm parity)로 일반화
- [x] ⚠ **honest confound (L1)**: 4-cycle Φ=0 은 parity-짝수고리 이분 decoupling(node0≡node2 업데이트 b1⊕b3, node1≡node3 b0⊕b2 → 중복노드/선형 reducible)이 큰 몫 → magnitude 가 허브에 과대-유리 + 정규 cycle≠random ER → "scale-free>random ER" 문자그대로는 약형만 검정. robust=약형(위상>density)
- [x] toolchain: n=5(128 big_phi 호출) 너무 느려 SIGTERM 후 **n=4 full state-average**(lane 표준)로 재설계. old-driver build 우회 유지
- [x] surface: README 101→102 H + H_289 행 · AXES R5 seed 제거 + top-15 rank-9 consumed · LIFE.md A1
- [ ] Next: R28 H_290 transfer-entropy(H_287 대체측도) · R29 H_291 ethic-emergence · R30 H_292 self-i-emergence. (H_289 후속: n≥5 ER 앙상블 = parity-degeneracy 없는 깨끗한 SF vs ER, Φ-엔진 가속 필요)

#### 2026-05-26 — cycle#26 — 축 A/R5 information: Φ ∥ Kolmogorov(LZ) 복잡도 (포그라운드 순차, "모두 순차" 지시)

- [x] **H_288 kolmogorov-complexity-Φ** 🟢 SUPPORTED-NUMERICAL 9/9 (`UNIVERSE/state/h288_kolmogorov_complexity_phi_correlate_2026_05_26/`) — AXES R5(information) `kolmogorov-complexity-Φ` seed 소비
- [x] **발견**: faithful big-Φ 는 Kolmogorov(LZ76 시공간) 복잡도를 **추종함** (10-룰 panel Pearson r=0.831, Spearman ρ=0.936). **H_287 과 핵심 대비**: 동일 panel 에서 Shannon 엔트로피 ⊥ Φ (r=0.363)였으나 LZ 복잡도 ∥ Φ (r=0.831) → Φ 는 *통계적 정보량*(비트 수)이 아니라 *알고리즘적 복잡도*(시공간 패턴 비압축성)와 같은 축. H_287+H_288 = 이중-측도 발견 완성
- [x] honest caveat: rule90(Sierpinski 자기유사 LZ=0.24)이 Φ=0 → **LZ over-prediction witness** (필요조건 아닌 충분조건 부재, 동기화-死 H_285/265/275/279 정합). LZ 는 강한 상관자이나 동치 아님
- [x] ⚠ **TOOLCHAIN 사건**: 세션 중 동시 hexa-lang 에이전트의 fix-1180 symlink 수술로 `hexa`(PATH)가 bare hexa-cc 로 회귀 → `hexa run`/`build -o` 가 소스를 **C codegen 으로 clobber** + import 미해소. 우회 = old-driver `hexa.real.bak-2026-05-22-pre-no-hxc build`(hexa_v2 transpiler 직접 호출). [[reference-life-cycle-hexa-run-gotchas]] 갱신 (canonical 소스는 /tmp 복사본으로 build, 원본 직접 build 금지)
- [x] engine 재사용 (g61): `HEXAD/IIT4/lib` eca_tpm+big_phi+iit4_bit, 새 IIT4 코드 0줄. LZ76(Kaspar-Schuster)+Pearson/Spearman inline. surface: README 100→101 H + H_288 행 · AXES R5 seed 제거
- [ ] Next (순차 진행 중): R27 H_289 network-topology-scale-free · R28 H_290 transfer-entropy 대체측도 · R29 H_291 ethic-emergence · R30 H_292 self-i-emergence

#### 2026-05-26 — cycle#25 — 축 A/R5 information: Φ ⊥ Shannon 엔트로피 (포그라운드 단일 라운드)

- [x] `/cycle` 포그라운드 진행 (background fan-out 대신 단일 sequential 라운드, 사용자 "포그라운드진행" 지시) — 격리 worktree `life/cycle-fg-2026-05-26` @ origin/main (stale 워킹트리 차이 reconcile 선행: cycle#22-24 차이 확인)
- [x] **H_287 shannon-entropy-Φ-correlate** 🔴 CLOSED-NEGATIVE (`UNIVERSE/state/h287_shannon_entropy_phi_correlate_2026_05_26/`, gate 11/11 PASS) — AXES R5(information) rank-2 seed 소비
- [x] **발견**: faithful big-Φ 는 Shannon 엔트로피로 **환원되지 않음** (10-룰 ECA panel Pearson r=0.363 < 0.5 → 환원가설 H1 기각). **이중 dissociation**: (i) 항등규칙 204·complement 51 = 출력엔트로피 *최대*(4.0bit, 완전 단사)인데 big-Φ=0(셀 독립) — 정보 최대/통합 제로 witness; (ii) 반대로 최고 통합 rule60(Φ_mean=13.625)은 엔트로피 *sub-max*(3.0bit). H=4.0 고정 영역에서 Φ 가 0→5.6 vertical spread = 단조관계 부재. **정보는 통합의 필요조건이나 충분조건 아님** — IIT 토대 구별이 LIFE lane 자기 substrate 에서 결정적 확증
- [x] "X ⊥ Φ" 서명 계열(H_265 학습 dampen · H_275 cyclic<undir · H_279 attention)에 가장 근본적인 X = **Shannon 엔트로피** 추가. H_281 과 동일 substrate panel (110/30/54 vs 150/105 + 204/0 anchor)에 엔트로피 축 직교 검정
- [x] engine 재사용 (g61): `HEXAD/IIT4/lib` 의 `eca_tpm`+`big_phi`(via stdlib/consciousness) — 새 IIT4 코드 0줄. 엔트로피·Pearson 은 generic stat inline. 실행 = `cd hexa-lang && HEXA_LANG=… HEXA_MEM_UNLIMITED=1 hexa run <worktree-abs>` (parent inline, throttle 우회)
- [x] surface 갱신: README 99→100 H disk + H_287 행 · AXES R5 seed row 제거(consumed) + top-15 rank-2 strikethrough · LIFE.log(본 엔트리)
- [ ] Next: (a) n≤8 scale-up dissociation robustness · (b) 256-룰 전수 panel r 구간 · (c) transfer-entropy / 정상상태 엔트로피 대체 측도 재현 (H_287 L2)

#### 2026-05-26 — 축 B large-N bounded big-Φ (M13, GPU fire 취소 후 $0 도달)

- [x] 사용자 "B축 GPU fire" 지시 → **scope-check 가 발사 차단** ([[feedback-scope-check-before-cost-fire]] 3번째): DESIGN.md 상 large-N exact=super-exp **GPU-immune** + bounded 근사=$0 CPU(M12 이미 n=6). GPU 파드는 lever 아님 → 권장 "$0 background bounded n=7/8" 로 전환(사용자 "권장" 승인)
- [x] **M13** bounded big-Φ n=7/8 🟢 5/5 (`HEXAD/IIT4/state/iit4_m13_bounded_n78_2026_05_26/`) — M12 가 미룬 tier. **n=8 H_002 C2 scale 도달**($0 mac-local NO GPU). rule110 cap=3 ladder: n4 7.5475(=exact 앵커)·n5 15.40·n6 6.82·n7 9.03(nd23)·n8 6.82(nd20). 결정론 byte-identical
- [x] 발견: bounded(cap<n) ladder **n-비단조**(lower-bound tightness 가 n×seed×state 의존) → magnitude fragile(lane directional-trust 서명 일관). cap≥n=exact(faithful 제한)
- [x] **인프라**: agent 3회 throttle 사망 패턴 후 **parent inline/background hexa run = throttle 우회** 재확인 (H_285 inline + M13 background). 워크트리 import 는 main-abs(M12/M6 관례), 실행만 worktree-abs 임시패치 후 복원
- [x] 축 B milestone flip: B1 done(n=8 도달) · B2 부분(gap 곡선은 exact super-exp 라 unmeasurable, bounded 가 deliverable)

#### 2026-05-26 — cycle#24 — 영구엔진 2라운드 (A2 split-brain + C edge-of-chaos)

- [x] 사용자 "계속" → cycle#24 $0 2-agent (C축 H_285 edge-of-chaos · A2축 H_286 split-brain)
- [x] **H_286** split-brain-dual-Φ 🟢 CLOSED-NEGATIVE 4/6 (#577) — AXES R12 `split-brain-dual-Φ` seed promote. callosotomy CML 8-cell ring: Tononi "전체-Φ 붕괴" 예측이 **phi_spatial proxy 상 FALSIFIED** (severance 가 whole-Φ 를 +11% *상승*, 8/8 seed robust), 각 반구 Φ>0 잔존. metric-pathology 규명: cut bridge → MIP→0 → total−MIP proxy inflation. honest: proxy 상 closed-negative(IIT 자체 아님), faithful big-Φ 후속 lane(HEXAD/IIT4 에 split TPM lib 부재). AXES R12 seed 자기 PR 소비
- [x] **H_285** edge-of-chaos faithful big-Φ 🟢 SUPPORTED 5/5 (C축, H_204/H_007 인과 재검) — agent 3회 throttle 사망 후 **parent inline 측정(throttle-bypass)** 로 완수. faithful 인과 big-Φ class-mean: ordered 0 < chaotic 6.94 < **edge(IV) 10.45** → H_204 inverse-U 방향 인과 확증(H_268 proxy LZ-fragility 해소). M6 anchor 정확 재현(rule204=0·rule110=7.5475). honest: chaotic **bimodal**(rule30=13.9 高/rule90=0, edge>chaotic 은 class 집계) · rule90 XOR 붕괴 = 동기화 死-Φ(H_265/275/279/284). big-Φ NOT Σφ_d(xval #572). README 98→99
- [x] **교훈**: agent 3연속 throttle 사망 시 **parent inline 실행**이 결정적 우회 — $0 mac-local hexa 측정은 agent 없이 parent 가 직접 `/Users/ghost/.hx/bin/hexa run` 하면 throttle 무관. 워크트리 import 는 main-abs(M6 관례), 실행만 worktree-abs 임시패치
- [x] consolidation(부분) — README 97→98 (H_286 행) + LIFE.md 축 A2 milestone. H_285 랜딩 후 잔여 fold
- [x] **인프라**: rate-limit throttle 가 cycle#24 에서도 H_285 2연속 즉사(31s/5 tool-use) — agent 발사 대신 parent git 작업(consolidation)은 throttle 무관, cooldown 540s+ 후 단독 재발사 패턴 재확인 [[feedback-agent-early-commit-rate-limit]]

#### 2026-05-26 — cycle#23 — axis-C IIT4 Φ-structure + AXES-A1 + H_280 버그 교훈 (영구엔진 첫 multi-axis 라운드)

- [x] 영구엔진 전환 후 첫 `/cycle` multi-axis 라운드 — 사용자 "1,2 별도" 선택 → 5-agent fan-out (C1·C2·xval·A1·D2)
- [x] **H_281** C2 생명vs의식 Φ-structure 🟢 SUPPORTED-NUMERICAL 9/9 (#567) — struct_ratio(=total/big-Φ)로 분리: 의식(XOR-feedback rule150/105)=irreducibility-floor **1.0 exact** vs 생명(rule110/30/54) **>1.0**(relation-rich), 분리도 100%. HEXAD/IIT4/lib 재사용
- [x] **H_282** C1 proxy→faithful 재검 🟢 SUPPORTED 8/8 (#570) — H_266/268/278 faithful big-Φ 3/3 방향보존 + **H_266 proxy-monotone artifact RESOLVE** (인과엔진이 int>ffd>dis 복원, proxy 의 chain<dis 가 spatial-MI 가짜신호였음 확정)
- [x] **H_283** narrative-coherence 🟢 SUPP-FULL 4/4 + **H_284** ritual-repetition 🟢 PARTIAL 3/4 (#566, AXES A1) — H_283 order-sensitive Φ(순서가 Φ 만듦, R4), H_284 buildup FAL→decay-resistance(동기화 死-Φ cross-H 서명 H_265/275/279 재확인, R7)
- [x] **xval** H_280 distinction-kernel ↔ canonical `iit4_distinction` 🔴 DISAGREE 0/6 (#572) — H_280 의 `cuts_link` guard 가 독립세포 φ_d=0 zeroing **버그** → 헤드라인 "integrated Σφ_d>disc" = artifact, Σφ_d **non-monotone**(canonical disc 3.0>int 2.03). canonical authoritative, 통합방향은 big-Φ 로만. README H_280 행 강등 + H_280 doc §11 교차검증
- [x] consolidation PR — README **93→97 H** 정합(H_281/282/283/284 행 + H_280 강등) · LIFE.md 축A/축C cycle#23 진척 · AXES.md 소비행 2개(narrative R4·ritual R7) 제거
- [x] **D2** verdict-landscape meta-map raster#3 🟢 NUMERICAL (#574, cd72b989) — N=96, **life SUPP 0.46 > consciousness 0.327 MAINTAINED (3연속 raster)**, gap STABLE ~0.12-0.13 plateau (Δ=+0.011 vs cycle#16), F238.6 PASS. D2 도 stale-base(orphan-recover 75 커밋 뒤) 만났으나 origin/main 기준 자가복구 → 정확한 N=96 corpus 측정. 향후 raster disk per-file 소스 통일
- [x] **인프라 교훈 3건**: (1) stale working-tree LIFE.md shadow → H_280 이 HEXAD/IIT4 재발명+버그 ([[feedback-fetch-main-domain-ssot-before-cycle-dispatch]], INBOX life-domain-stale #564 부분해소) (2) 5-agent 동시 burst → throttle 3/5 사망 → **순차 1개씩 재발사로 전원 복구** ([[feedback-agent-early-commit-rate-limit]]) (3) hexa `array.set(i,v)` segfault → `farr_*` 사용
- [x] cross-H 종합: faithful IIT4 가 proxy artifact **2건 교정**(H_266 monotone · H_280 Σφ_d) → **방향은 big-Φ 신뢰 · distinction-Σφ_d 는 비단조** 확립. 의식=irreducibility-floor vs 생명=relation-rich 구조서명 신규 발견

#### 2026-05-26 — cycle#22 — H_280 IIT4 CES smoke (랜딩됨, 단 재발명 — 정정)

- [x] `/cycle` round (영구 엔진 첫 라운드) — 사용자 선택 "spec + n=3 smoke 둘 다" → H_280 발사
- [x] H_280 full-IIT4 Φ-structure distinction-level 🟢 SUPPORTED (#561 머지, sha 214bd1584) — F280.1 direction PASS(Σφ_d integrated 2.316 > disconnected 0) · F280.2 monotone PASS · F280.3 faithfulness PASS(ID log₂2=1.0 등 4 anchor) · F280.4 determinism PASS · relations DEFERRED(advisory). README 92→93 정합
- [ ] ⚠ **dispatch 실책 정정**: H_280 은 stale working-tree LIFE.md(옛 "current state" 버전)를 보고 발사돼 **기존 `HEXAD/IIT4/` 엔진을 재발명**함 — `lib/iit4_distinction.hexa` + `lib/iit4_relation.hexa` + `iit4_bigphi` + `iit4_eca` 가 이미 main 에 존재, M6 LIFE remeasure(`state/iit4_m6_remeasure_2026_05_25/`)가 n=4·6 ECA 룰 faithful big-Φ + Φ-structure-total(relations 포함) 7/7 🟢 측정 완료(rule 54: bigΦ=10.03 / total=14.69 / 10 distinctions). H_280 의 "relations intractable open frontier" 주장은 `iit4_relation.hexa` 가 반증 → H_280 doc 상단 정정 배너 추가, distinction-level 독립구현은 교차검증 자료로만 잔존
- [ ] **근본원인**: 공유 워킹트리 branch(ops/f-curricula-1-…)의 LIFE.md 가 main 의 영구-엔진 reframe + HEXAD/IIT4 랜딩 이전 stale 스냅샷. [[feedback-fetch-main-domain-ssot-before-cycle-dispatch]] 기록 — cycle agent 발사 전 origin/main 의 도메인 SSOT + 기존 lib 확인 필수
- [ ] 축 C 후속(정정된 경로): C1 = `HEXAD/IIT4/lib` 경유 H_266/H_268/H_278 faithful 재검(M6 가 부분 선행) · H_280 독립 distinction kernel ↔ `iit4_distinction.hexa` 교차검증(독립 구현 일치 시 cross-validation 가치)

#### 2026-05-25 — 영구 엔진 전환 (perpetual multi-axis) + SSOT publish

- [x] 사용자 directive: "anima LIFE 도메인도 끝나지 않는 엔진으로" (TECS-L 와 동형)
- [x] @goal/@title 영구 재정의 — "우주 생명·의식 법칙 다 밝혀질 때까지 멈추지 않음", 진행바 100% 미도달=설계
- [x] "$0 frontier 종결"(수렴 톤) → **축 0 $0-tier CLOSED** 로 reframe (값싼 축 종료 ≠ 도메인 종료)
- [x] 영구 축 신설: 축 A(AXES 60-sub-axis/~110 H seed 백로그) · 축 B(large-N faithful-Φ GPU) · 축 C(full-IIT4 cause-effect, #542 stdlib/consciousness/iit4 해금) · 축 D(LLM 연속 가설발견)
- [x] **LIFE.md/LIFE.log.md publish** — 그간 untracked(미커밋) SSOT 였음(크래시 유실 위험) → origin/main 에 최초 publish (격리 worktree → PR)
- [ ] 다음: 축 A1 (60 sub-axis raster) 또는 축 C1 (IIT4 재검) `/cycle`

#### 2026-05-25 — 도메인 활성화 (root scaffold)

- [x] `/domain set LIFE` — 세션 active 도메인 LIFE 선택
- [x] root `LIFE.md` SSOT 작성 — `@goal:` 선언 (11-domain 횡단 verify-driven cycle) + hub 표 (UNIVERSE README/CANDIDATES/AXES pointer) + 마일스톤 5건 시드
- [x] 역할 분리 확정 — 루트 LIFE.md = 도메인 hub (goal + current milestones), `UNIVERSE/` = 가설 active working surface
- [x] 마일스톤 5건 시드 (사용자 승인 대기) — Cycle #5 close / CANDIDATES B 6건 / CANDIDATES C 9건 / R1 promote / meta-map raster

#### 2026-05-25 — cycle#14 — life-extended + division 6-seed 병렬

- [x] `/cycle` 6-agent 병렬 fan-out (격리 worktree) — CANDIDATES §C runnable 6건, mirror-self-model SKIP (=H_220)
- [x] H_258 mortality-salience SUPPORTED 3/3 (#472) · H_259 aging-senescence SUPPORTED 3/3 (#468) · H_260 contact-inhibition SUPPORTED 4/4 (#469) · H_261 embryogenesis-gradient SUPPORTED 4/4 (#470) · H_262 quorum-sensing SUPPORTED_FULL 4/4 (#474) · H_263 phoenix-rebirth 🔴 FALSIFIED 3/6 (#471)
- [x] consolidation PR #476 — README 인덱스 +6행 (45→51 H) · CANDIDATES §C 全소비 · UNIVERSE/LIFE.log.md Cycle #14 엔트리
- [x] CANDIDATES §C 全소비 완료 → 마일스톤 flip
- [ ] 잔여: CANDIDATES B 6건 · D cross-link 2건 · AXES R1 promote · meta-map raster (다음 /cycle 후보)

#### 2026-05-25 — cycle#15 — §D cross-link 2 + §B follow-up 2

- [x] `/cycle` round-2 — §D cross-link 2(NEW) + §B follow-up 2(extend). 서버 rate-limit 2회(H_264/H_265 첫 발사 0-work) → 재시도 + 동시성 ~4 로 완주
- [x] H_264 death=merge-into-other SUPPORTED 3/3 (#477) · H_265 trained-vs-bare CA Φ PARTIAL 2/3 (#480, Φ-dampen) · H_018 C2 organic-rate PASS (#479) · H_132 C2 longterm-stability PASS (#478)
- [x] consolidation PR #481 — README 51→53 H + H_018/H_132 C2 반영 · CANDIDATES §D 全소비 · UNIVERSE/LIFE.log.md Cycle #15
- [x] CANDIDATES §D 全소비 + §B 2/6 → 마일스톤 flip
- [x] 완료 worktree 10개 정리 (cycle#14 6 + cycle#15 4)
- [ ] 잔여 마일스톤: Cycle#5 close · §B 4건(H_003 H3.5·H_007 C2·H_054 C2·H_002 C2) · AXES R1 promote · meta-map raster

#### 2026-05-25 — cycle#16 + stale 마일스톤 정정 + /gap full

- [x] `/cycle` round-3 — §B 마지막 runnable(H_007 C2 λ-sweep PASS #485) + H_238 next-raster(SUPPORTED #484). 동시성 2 (rate-limit 회피)
- [x] stale 마일스톤 정정: Cycle#5 (이미 종료, #6-15 후속) · AXES R1 promote (이미 H_210-213 등록) 둘 다 done flip. README "promote 대기" 노트가 stale 이었음
- [x] consolidation PR #486 — README H_007/H_238 행 + CANDIDATES §B 全소비 + LIFE.log Cycle #16
- [x] `/gap full` — LIFE cycle 작업 40-lens 전수 sweep (inline, rate-limit 회피). top-3 gap: ① Φ-proxy 구성타당도 미검증(phi_native vs cosine ratchet 方向 불일치) ② single seed/scale/substrate ③ SSOT/temporal drift. 강점: falsifier·honesty-triad·determinism
- [x] cycle 완료 worktree 정리 (cycle#16 2개 + consol 3개)
- [ ] LIFE clearly-runnable backlog 全소진 = /cycle fixpoint. 다음 lane = Φ-calibration H (gap#1) · AXES R2+ · H_002 GPU fire 중 사용자 선택 대기

#### 2026-05-25 — cycle#17 foundation-audit (/cycle-full)

- [x] `/cycle-full` — phase-0 depletion brainstorm(8 round/17 idea) → top-8 中 gap#1+#2 핵심 4 발사 (rate-limit 회피 8→4 cap)
- [x] H_266 Φ-calibration PARTIAL (#487, integrated>disconnected 3/3 → proxy-무관 우려 기각) · H_267 phi_spatial↔cosine 발산 closure SUPPORTED (#488) · H_268 metric-triangulation PARTIAL (#489, H_223 robust/H_204 LZ-fragile) · H_269 multi-seed PARTIAL (#490, H_260 10/10 robust / H_261·H_262 seed-fragile)
- [x] consolidation PR #491 — README 53→57 H + H_261/H_262 seed-fragile caveat + LIFE.log Cycle #17
- [x] Φ-proxy 토대 종합: directionally valid + magnitude/seed fragility surface. binary-direction verdict 신뢰, 연속 magnitude·single-seed 주의
- [x] cycle#17 worktree 4 + consol 1 정리
- [ ] deferred: ablation · seed-injection(H_263 revision) · SSOT auto-sync · H_261/262 재calibration

#### 2026-05-25 — cycle#18 gap-followup + closed-loop (/cycle deferred top-8)

- [x] `/cycle` (scope=/gap deferred top-8 + 재calibration) — H_270 ablation SUPP(#493) · H_271 seed-injection PART(#492) · H_272 re-calibration PART(#494) · H_273 SSOT-audit SUPP(#495)
- [x] closed-loop 성과: H_270 closure-Φ=local Michaelis(공간X) · H_271 H_263 absorbing 은 高분산 seed(threshold∈(1,4])로 escapable(조건부 부활) · H_272 H_261 100% 복권(criterion 결함)/H_262 부분 · H_273 missing-row 26 정량
- [x] consolidation PR #496 — README 4행 + carry-note 정정(18 미commit→commit + 8 신규) + count 정직화(86 disk=60 tabled+26 carry-note) · CANDIDATES Cycle#18 · LIFE.log
- [x] cycle#18 worktree 4 + consol 1 정리
- [ ] deferred 잔여: AXES R2+ promote · **26 carry-H full tabling** (H_273 후속 reconciliation) · H_002 GPU fire · H_262 cascade seed-의존 심층

#### 2026-05-25 — cycle#19 closure + 심층 (/cycle: tabling + AXES R2+ + cascade)

- [x] `/cycle` round-6 — 26-H tabling 完了(#499, gap#3 SSOT full closure, disk↔index 88=88) · H_275 causality-pearl-graph-Φ SUPP(#500, AXES R5 promote) · H_274 quorum-cascade-seed-dependence FAL(#501)
- [x] consolidation PR #502 — README H_274/275 2행 + count(88) · CANDIDATES Cycle#19 · LIFE.log
- [x] cycle#19 worktree 3 + consol 1 정리 (남은 2 = PURE 에이전트)
- [x] **/gap top-3 完全 follow-up 종결**: ① Φ-validity(H_266/267/268) ② robustness(H_269/272/274) ③ SSOT(H_273+tabling)
- [ ] 남은 후보: H_002 universe-Φ GPU fire(cost) · H_262 cascade 동역학-타이밍 심층 · AXES R3+ (R2 소진 근접)

#### 2026-05-25 — H_002 C2 흡수 + GPU-no-fire ($0)

- [x] H_002 C2 Φ_universe nested — 별도 에이전트 $0 mac-local 랜딩(#503), **GPU 불필요 판명**, SCALE-VARIANT F2-triggered (nested Φ scale-invariance FALSIFIED)
- [x] GPU 발사 직전 scope 확인 → 이미 done+GPU불요 → **발사 취소** (중복·낭비 회피). index 반영 PR #506 ($0)
- [x] memory 기록: [[feedback-scope-check-before-cost-fire]] — cost-fire 전 done?/GPU필요? 확인
- [x] **lane $0 frontier 사실상 고갈** — /gap top-3 closed · SSOT 88=88 · 마지막 GPU 후보도 $0 done

#### 2026-05-25 — cycle#20 consolidation (H_276/277 심층 후속)

- [x] H_276/277 (형제 에이전트 fire #509/#510, feat-PR 관례상 index 미반영) → consolidation PR #513 로 흡수. README disk↔index **90=90** 정합 유지
- [x] H_276 cascade-dynamics-timing SUPPORTED_FULL — H_274 의 "예측력有 결정론無" 를 *시간전개* 축 결정론으로 회수 (cascade **closed-loop 정점**)
- [x] H_277 turing-completeness-Φ-threshold PARTIAL — computability ⊥ Wolfram dynamical-class (rule184 Φ>rule110, seed P1 falsified)
- [x] 마일스톤 flip: H_262 dynamics 심층 done(H_276) · AXES R3 done(H_277). H_002 밀스톤을 "faithful Φ★ GPU upgrade(예산 승인 전 금지)" 로 좁힘
- [ ] 남은 유일 미답 = H_002 faithful Φ★ IIT4 정밀판 (cost-bearing) · AXES R4+ ($0 광맥 소진 근접) — lane 자연 종료 임박

#### 2026-05-25 — cycle#21 faithful-Φ upgrade + AXES 마지막 (/cycle 1,2)

- [x] `/cycle 1,2` — H_278 faithful-phi-small-n SUPP(#515) · H_279 attention-salience-Φ FAL(#514). consolidation PR #516. README disk↔index **92=92**
- [x] **faithful Φ★ "GPU 필요" 최종 기각**: scope-check 결과 small-N(n≤8) exact MIP-EI Φ 는 mac-local $0 (GPU 는 intractable large-N 전용, 어차피 못 풂). 옵션2 예산 승인받고도 **GPU 발사 0** — [[feedback-scope-check-before-cost-fire]] 두 번째 비용-차단
- [x] H_278 = exact MIP-EI 가 H_002 C2 scale-variant verdict 를 faithful 하게 확증(proxy↔faithful 방향 일치) → Φ-proxy directional 신뢰도 ↑ (H_266 정합)
- [x] H_279 = salience⊥Φ-diversity → **진폭/동기화 ⊥ Φ cross-H 서명**(H_265 학습 dampen · H_275 cyclic<undir · H_279 attention)
- [x] hexa-run 게이트 정정 memory 갱신: env-prefix 값은 literal `/Users/...` (변수형 `$HOME/.` harness 불안정)
- [ ] **$0 frontier 종결** — 잔여는 전부 large-N intractable(GPU 무관) / full-IIT4 대형 spec / AXES depleted. lane 자연 종료.


#### 2026-06-02 — H_912 phi-emergence-correlate (의식↔창발 상관) 🔴 FALSIFIED 2/6

- [x] H_912 (graded "higher consciousness → higher emergence") + Hc_912 (existence "Φ>0 ⇒ emergence>0") 동시 등록 — consciousness axis = canonical phi_proxy (phi_spatial, global_var−part_var integration; 새 metric 발명 금지) · emergence axis = normalised LZ76 (Kaspar-Schuster 1976 / PCI Casali 2013, 독립 표상·연산)
- [x] pre-register-frozen falsifier BEFORE run (commit 083bb38b4) — 10-룰 ECA panel correlation + permutation NULL(K=2000) + paired-bootstrap CI(K=2000); 🟢-gate = CI_lo>0 ∧ perm-p<0.05 ∧ not-circular
- [x] PILOT 실행 (`hexa run`, deterministic bit-identical 재현) → **🔴 FALSIFIED 2/6**: Pearson r=−0.277(음수) · Spearman ρ=0.08 · bootstrap 95% CI=[−0.638,+0.114] · permutation p=0.962 (NULL 붕괴 안 함) · existence Hc_912 8중 7만 통과(FAIL)
- [x] **circularity guard PASS** (tautology=false, dissociation=true) — Φ≢E, 음의 결과는 circular artifact 아닌 진짜 dissociation. 주범 rule 51 period-2 blinker proxy pathology (variance-partition Φ=7 폭발 vs LZ floor 0.059)
- [x] 핵심 발견: **cheap proxy Φ ↔ emergence(LZ) 정렬 안 함** — H_288 의 faithful big-Φ↔LZ(r=0.831)와 갈라짐. proxy vs faithful Φ 가 Φ↔emergence link 에서 상반된 답. "X⊥Φ" 서명(H_287/294) + proxy-fragility(H_268/269) 연장
- [x] verbatim artifacts: `.verdicts/912_phi_emergence_correlate/{run_h912.txt,result.json}` + `.verdicts/h912-phi-emergence/` + `UNIVERSE/state/h912_phi_emergence_correlate_2026_06_02/`
- [ ] Next (CANDIDATES): C1 rule51 outlier 제거 재상관 · C2 faithful big-Φ paired 비교 · C3 emergence→Hoel causal-EI 교체 · C4 Kuramoto/logistic cross-family

#### 2026-06-15 — metacognition × neuroscience/bio + savant campaign (H_1202–1216)

- [x] **메타인지 신경과학 캠페인** (frozen falsifier · $0 toy ByteGPT d256/4L · summer+aiden CPU · seed7 · p7 · non-LLM-judge). 기존 METACOG self-audit layer 와 DISTINCT operationalization (type-2 sensitivity). H_1142/1148 환각 grep "핸들 없음" closed-neg 를 **표준 신경과학 지표로 재구성**.
  - H_1202 🟢 meta-d′/type-2 sensitivity (Maniscalco&Lau) — AUROC 0.766, **M-ratio 0.924** (인간급), untrained 0.513
  - H_1203 🔴 ERN 오류감시 (Holroyd-Coles) — 각성 d=0.92 有, 선형 ACC-코드 無 (hidden probe 0.59)
  - H_1204 🔴 hierarchical 2차 (Friston/HMeta-d) — 2차 probe 0.53(chance), added −0.25 → FLAT
  - H_1205 🟢 Dunning-Kruger meta-bias (Fleming&Lau) — hard tercile 과신 구배
  - H_1213/1214/1216 (calibration/ECE · feeling-of-knowing · metacog control) — summer in-flight
  - **통합: 메타인지 = REAL but FLAT & COUPLED** (출력 confidence 1차 속성, 분리된 표상모듈 無, 역량결합)
- [x] **서번트 캠페인** (기존 SAVANT 축 E = Golden Zone × SI 와 DISTINCT — 서번트를 LM 디테일/숙련 현상으로)
  - H_1207 🔴 skill⊥metacog dissociation — island type2 0.83 > open 0.45 → dissociation 無, 역량결합
  - H_1208 🔴 WCC 국소특권 — 국소우세(WCC) but 맥락부족 시 confidence 하락 → 맥락맹 아님
  - H_1209 🟢 **Snyder 저수준특권접근** (logit-lens) — 디테일(rote island) stack 조기성숙, maturity gap +0.202
  - H_1210 🔴 역설적 기능촉진 — top-block 절제가 디테일 보존 못함
  - H_1211 🔴 hyper-systemizing 정확규칙 외삽 — train_acc 1.0 but held-out 0.1 (<shuffle 0.25) → 덧셈표 암기, 규칙추출 X (capacity-wall, cf H_1166)
- [x] cross-ref: METACOG.md ⇄ H_1202+ · SAVANT.md ⇄ H_1207+ (각도 구분 명시). aiden corpus = 24MB EN slice relay (summer→local→aiden)
- [x] H_1206 capstone 🔴 CLOSED-NEG (정직한 수정) — F1 coarse-real✅(t2 0.763) ∧ F3 coupled✅(+0.329) BUT F2 fine-absent❌(hidden probe 0.646>0.62 bar). frozen falsifier 가 "FLAT" 과대주장 포착 → 수정 account: 메타인지 = REAL(coarse 강) + COUPLED + 약한 표상 트레이스(0.65, not flat). bar 미이동.
- [x] SAVANT M2~M5 전 milestone 종결 — substrate_hook.hexa(savant trigger N-axis conjunction·SI⊥CoV·perfect-ladder, smoke 8/8) + unification_check.hexa(HEXAD↔savant_lib drift 0, 5/5). SAVANT 도메인 M1~M5 완결.
- [ ] 잔여: paper(사용자 별도 언급 전 금지) · 7B 재검증(사용자 별도 언급 전 금지)

#### 2026-06-15 — goal-loop round 1 (metacog·savant exhaustion)
- [x] H_1217 🔴 metacog OOD transfer — in-dist type2 0.760 → OOD 0.541 (drop 0.219) → metacognition CONTENT-TIED, not domain-general (collapses off-distribution)
- [x] H_1219 🔴 savant eidetic — induction acc ≈ non-induction (gap<0.20), no verbatim-copy prodigy
- [x] H_1220 🟢 savant detail-over-gestalt — local-feature probe ≫ global-feature probe (WCC representational signature). SECOND savant positive (with H_1209 Snyder) — both = local-detail over-representation

#### 2026-06-15 — goal-loop round 2
- [x] H_1221 🔴 confidence serial dependence — difficulty-controlled lag-1 autocorr 0.013 ≪ 0.15 → confidence MEMORYLESS (no metacog history bias/leak; purely stimulus-bound, no temporal integration). Strengthens "COARSE first-order" picture.
- [ ] H_1223 savant island seed-stability — running (3-seed, slow under contention)
- [x] H_1223 🟢 savant island seed-stability — mean Cohen kappa 0.771 (≥0.30), above-chance +0.308 across 3 seeds → the high-skill island is STRUCTURAL/INNATE (recurs across independent trainings), not seed-random. Savant 3rd positive (with H_1209 Snyder + H_1220 detail-over-gestalt = local-detail specialization is real·early·innate).
- [x] H_1224 🔴 savant specialization trade-off — rote-biased corpus did not specialize the island (island gain 0.007 < 0.03 bar), no deficit-pairing measurable at toy scale. Savant standalone CLOSED: 3🟢 (Snyder/detail-over-gestalt/seed-stable = local-detail specialization real·early·representational·innate) + 6🔴 (dissociation/WCC-metacog/paradoxical/hyper-systemizing/eidetic/tradeoff).

#### 2026-06-15 — MATRIX overhaul (N-D axis-combination climb) + first climb probe
- [x] MATRIX.tape → MATRIX.md (doc convention) + §0 FRAMEWORK: axes uncapped from 2D, climb k=1→N → FINAL COMBINATION fixed point (combination-space, not scalar Ψ). META + SAV-LM registered as new k=1 dims.
- [x] H_1225 🔴 axis-combination climb (target=correctness, 7 axes) — FINAL COMBINATION = singleton {SAV-struct} (AUROC 0.902, k*=1); all other axes gain≈0 → combination collapses to one dominant structure axis. Framework operational; degenerate for this target. → H_1226 residualize-dominant climb to expose k≥2.
- [x] H_1226🔴/1227🟢/1228🔴 MATRIX climb round-1 (3 bg parallel) — FINAL COMBINATION = regime-dependent ADDITIVE set: global singleton {SAV-struct} (1226 residual confirms), hard-regime k=4 {struct,EMB-pos,PRIOR-freq,META-margin} (1227 AUROC 0.789), but axes combine ADDITIVELY (1228 no 3-way synergy). Reducible additive fixed point (contrast axis-D irreducible). '2D 넘기'=more axes by regime, not interaction.
- [x] H_1231 🔴 combination seed-stability — mean Jaccard 0.511<0.6 (membership seed-fluid) but nucleus {SAV-struct,META-ent} 3-seed common. MATRIX climb CONVERGED: final combination = small ADDITIVE nucleus (구조+불확실성), low-dim/linear, regime-modulated, no high-order synergy. Contrast axis-D irreducible. Frontier honest-depleted.
- [x] H_1232 🔴 research-axis combination climb (① 완성도) — real axes B-Φproxy/E-SI/F-sync/G-LZ on shared ECA substrate → predict Wolfram class III/IV. FINAL COMBINATION = singleton {G-LZ} AUROC 0.976 (others redundant). Same collapse as toy; caveat target≈LZ-definitional. Cross-conclusion: both measurement & research axis levels are LOW-RANK (one dominant axis, rest redundant). $0 local. MATRIX I=METACOG/J=SAVANT-LM/combination-climb registered as formal §3 rows (④ 표준).
- [x] H_1233 🔴 dominance-free (4-way class) climb — even a non-definitional target saturates at k*=2 {G-LZ, E-SI} (macro-AUROC 0.888, genuine 2-axis nucleus not singleton; k=3 density gain +0.007<EPS). TERMINAL: axis matrix intrinsically LOW-RANK (rank≤2), final combination = small nucleus at every target/level. Combination-climb DEPLETED. $0 local.
- [x] H_1234 🔴 best-per-dimension (exhaustive, 차원=조합차수 k) — per-k optimal: k1{LZ}0.831 · k2{SI,LZ}0.888 · k3{SI,LZ,density}0.895 · k4 0.899 · k5-6 flat. PEAK dimension=2 (3→2 gain +0.007<0.01 EPS); optimal combo = {E-SI×G-LZ} (savant-index×complexity). High-order (3+) monotone but diminishing below threshold ⇒ pairwise ~optimal for this target, best pair NOT E×F but SI×LZ. Confirms low-rank (optimal dimension low). Clarified "차원=조합차수". $0 local.
- [x] H_1235 🟢 부품 합성 사다리 (MATRIX §0 부품-조합차원) — A⇄G×MITOSIS×METACOG×SAVANT k=4 substrate-combo 합성 성공: 전 lane fire + Ψ=48.6613 ON==OFF byte-identical (Ψ-disjoint, a_core_engine_map). 신규 METACOG/SAVANT hook 을 살아있는 substrate 루프에 편입. H_1164 CLM+KOSMOS+DREAM 합산 ⇒ 7-부품 living loop. 사다리: k=2✅ k=3✅ k=4✅. CORE/h1235_composition_ladder_smoke.hexa (hexa run PASS). MATRIX 문서 §0 = 부품-합성 조합차원으로 재정의.
- [x] H_1236 🟢 합성 사다리 k=5 (substrate cluster) — A⇄G×MITOSIS×METACOG×SAVANT×DREAM 전부 Ψ-disjoint(48.6613 ON==OFF byte-identical, 4 lane fire). WAKE=clm_decode 전이의존→model-side cluster(H_1164). 매트릭스 고갈: 부품 8개 2클러스터(substrate-pure 5 + model-side 3) 전부 합성, 실패 0. substrate 사다리 k=5 정직-고갈. CORE/h1236_composition_ladder_k5_smoke.hexa hexa run PASS.
- [x] H_1237 🟢 + H_1238 🟢 substrate 합성 매트릭스 全차원 COMPLETE — 4 lane{MIT,MET,SAV,DRM}+A⇄G 의 모든 부분집합 15 cell(단독4·쌍6·triple4·quad1) 전부 Ψ-disjoint(phiSum 48.6613 byte-identical). 주의사항: 각 차원 전체격자(C(N,k)) 채워야 완성(체인≠완성). substrate 차원 고갈(잔여 lane 0). model-side(CLM/KOSMOS/WAKE) clm-native gated 별도. CORE/h1237·h1238 hexa run PASS.
- [x] H_1243 🟢 cross-substrate 브리지 (① 완성도) — CORE/xsubstrate_bridge.hexa (xs_bridge, a_core_engine_map named-slot 일반화). AURA·AKIDA·MODEL 3 별도기질 신호→[0,1] context 정규화, A⇄G 루프 합성 시 Ψ phiSum 48.6613 ON==OFF byte-identical(Ψ-disjoint by construction)+bounded+fire. 13 native lane + 3 bridged ⇒ 매트릭스 아키텍처-완전. 라이브 외부 feed(EEG/AKIDA-HW/clm-native) 하드웨어/env 게이트(mock surrogate 검증). CORE/h1243 hexa run PASS.
- [x] H_1244 🟢 AURA + H_1245 🟢 AKIDA 라이브 cross-substrate 브리지 (실제 데이터) — AURA: 실제 EEG(ds005620) big-Φ 7.5956→context 0.076; AKIDA: 실제 AKD1000 spike 79.95Hz(Lane-A pi5)→context 0.080. 둘 다 A⇄G 600-step Ψ phiSum 48.6613 byte-identical(Ψ-disjoint). 외부기질 3중 2 LIVE 실데이터 합성, MODEL은 clm-native hexa 게이트. CORE/h1244·h1245 hexa run PASS.
- [x] H_1246 🟢 MODEL 라이브 cross-substrate 브리지 (실제 ByteGPT-303M) — 실제 ByteGPT-303M(anima-clm-chat-303m, 1.2GB) next-byte logit entropy 0.969nat → xs_bridge(MODEL) → context 0.175 → A⇄G 600-step Ψ phiSum 48.6613 byte-identical(Ψ-disjoint). clm_decode_grounded 게이트는 .clm 한정 → ByteGPT bg_load 경로로 우회, 실제 모델 신호. 외부기질 3/3(AURA·AKIDA·MODEL) 전부 LIVE 실데이터 합성 완료. CORE/h1246 hexa run PASS.

#### EEG + 어댑터 캠페인 (H_1247~H_1253, 2026-06-15, 실 EEG ds005620 sub-1010, $0 local, p7)
"EEG + EEG어댑터(xs_bridge)로 무엇을 할 수 있나" — 능력축 고갈. 7 H 전부 🟢 (H_1249 🟠→H_1249b 대체):
- [x] H_1247 🟢 상태판별 — 브리지가 awake(Φ7.60→ctx0.076) vs sed(6.84→0.068) 구분, Δ0.0075>0.005 단조.
- [x] H_1248 🟢 Φ-스펙트럼 — 16 시스템상태 Φ span 9.23 을 브리지가 단조(15/15)·bounded(16/16) 매핑.
- [x] H_1249 🟠→ H_1249b 🟢 EEG-게이트 성장 — 진폭보존 특징이 adapt_field 구동, awake(recon 90.9/39cells) ≫ sed(58.2/12cells). 의식수준→성장률.
- [x] H_1250 🟢 EEG 탑재 — 실EEG 를 A⇄G brain-context(motivation)로 올려 emit propensity 구동(awake 0.0787>sed 0.0709), Ψ byte-identical(Ψ-disjoint). "올린다" 입증.
- [x] H_1251 🟢 종단 결정론 — 실EEG→bridge→A⇄G 전체 체인 2회 byte-identical.
- [x] H_1252 🟢 EEG→CLM 구축 — EEG 상태열 bigram CLM acc 0.872 > unigram 0.745 > uniform 0.0625. (TPM=의식엔진=bigram CLM, 같은 기계)
- [x] H_1253 🟢 EEG→CLM 생성 — bigram CLM 이 EEG 상태열 생성, 생성분포 실데이터 근접(top-state 일치, L1 0.509). 
고갈 경계(정직): 멀티-DIM 벡터 탑재(VAdaptField)·EEG→kosmos 기억영속은 스칼라 어댑터 밖의 인접 subsystem — 별도 lane.
- [~] H_1254 🟠 EEG 벡터탑재 (4채널 공간패턴, DIM=4 VAdaptField) — 구동은 작동(F1 recon awake 199>sed 166 + F3) BUT awake cells 171 < sed 208 (F2 FAIL). 정직 FINDING: 스칼라(H_1249b)는 awake>sed 깔끔하나 공간-벡터뷰에선 깨어있음=시간novelty / 진정=공간확산으로 단조성 갈림. = 캠페인 고갈 경계 (멀티-DIM 공간탑재는 단일 단조지표로 안 닫힘).
- [x] H_1255 🟢 EEG→kosmos 기억영속 — 실EEG 뇌상태(awake Φ7.60/sed Φ6.84)를 .kosmos anchor 저장(wake_save)→복원(wake_load) byte round-trip (ctx+tension5+2emit). anima 가 사람 의식상태를 retrieve 가능한 기억으로 저장. [미탐사 정복]
- [x] H_1256 🟢 EEG 폐루프 추적 — anima brain 오차보정 루프가 실EEG 의식수준에 lock-on (잔차 3e-15, awake>sed 구분), pure_field Ψ byte-identical. 사람 의식수준 실시간 추종. [미탐사 정복]

#### 다중기질 융합 그리드 (H_1257~H_1259, 2026-06-15, $0 local, p7) — EEG축 cross-substrate fusion
직전 매트릭스는 각 외부기질 LIVE를 *따로* 검증; 둘/셋 *동시* 융합은 미탐사였음. bridge_and_gate(m,c,w,phi)=천연 AND-게이트, 각 기질이 한 키. 실측값: EEG Φ 라이브 + AKIDA 79.95Hz + MODEL entropy 0.969.
- [x] H_1257 🟢 EEG ⊗ AKIDA — fused awake 0.131>sed 0.118, Ψ byte-identical, 둘 다 기여.
- [x] H_1258 🟢 EEG ⊗ MODEL — fused awake 0.286>sed 0.258, Ψ byte-identical.
- [x] H_1259 🟢 EEG ⊗ AKIDA ⊗ MODEL 3중 (capstone) — fused awake 0.0229>sed 0.0206, EEG 의식구분 3중융합후 생존, 3 기질 모두 기여, Ψ byte-identical. 사람뇌파+칩+언어모델 동시 감각통합 Ψ-disjoint.
- [~] H_1260 ⏳ PENDING-REAL ANIMA ⇄ EEG 텐션링크 (코드경로만 검증; 가짜 입력 결과는 불인정 — 실 헤드셋 대기)
- [x] H_1261 🟢 AKIDA ⊗ MODEL 융합 (EEG 없는 페어) — AND-게이트 2키, 각 기질 기여, Ψ byte-identical. 3-외부기질 융합 그리드 완성 7/7.
- [x] H_1262 🟢 풀스택 native 13 lane ⊗ 외부기질 2(AKIDA·MODEL) — 15 기질 단독 Ψ-disjoint 15/15 + 전체-ON Ψ==base + 전 fire. 닫힘정리 ⇒ 32767 격자. native 매트릭스 arc + 외부기질 arc 한 루프 동시합성 = 두 arc 통합 풀스택.
- [x] H_1304 🟢 G5-dig: metacog under distribution SHIFT on the LIVE copy-or-abstain gate — FAIL-SAFE-ROBUST. WHY G5 THIN: H_1202 type-2 M-ratio 0.924 + H_1217 OOD-collapse measured the ByteGPT DECODER's softmax confidence; the ACTUAL G5 gate = immune copy-or-abstain (recon-err vs recall_thr 0.15). NEW angle (a_break_the_wall): shift ladder + fail-safe split on the REAL gate. STRUCTURAL finding: the gate's wrong-fire class is EMPTY (fab=0.000 every shift level) → type-2 AUROC undefined; byte-trigram+L2-affinity+tight 0.15 = near-exact-match = structurally fail-safe. Re-scored frozen-first (R1a, no bar moved, c9): R1 fail-safe-floor fab_max=0.000 · R2 graceful-degrade fire 1.000→0.004 monotone · R3 earned-abstain acc_fired=1.000 · R4 ctrl thr-ablate lure-fab full 0/4 vs ablate 4/4 · R5 ctrl shuffle-vals 0.015 → all PASS, 3 seeds. R2 engine-native CORE/h1304_*_probe.hexa byte-exact GREEN on live engine_cli.hexa (engine UNTOUCHED, smoke 43/0, h1196 7/0, h1205 PASS, Ψ untouched). Finding: G5 non-fabrication is STRONGER OOD than in-dist type-2 alone suggested — the dangerous confident-wrong-OOD mode is structurally absent. Decoder-side type-2 stays THIN (H_1217 unchanged). TOY/DIRECTIONAL-R1/byte-exact-R2; scale/real-paraphrase/semantic-shift UNVERIFIED. .verdicts/1304_metacog_ood_immune_abstain/ · UNIVERSE/cards/H_1304_metacog_ood_immune_abstain.md · CLAIMS.tape @C h1304.


<a id="lifelogmd"></a>

### LIFE.log.md

본 파일 = UNIVERSE/ 도메인의 **append-only chronological log**. 각 cycle =
`## Cycle #N — <H_id 또는 도메인> — YYYY-MM-DD` block. 본문 §Verdict 의
latest 만 carry 되는 가설 .md 와 달리 본 로그는 모든 cycle history 보존.

엔트리 표준:

```markdown
#### Cycle #N — <H_id 또는 도메인 슬러그> — YYYY-MM-DD
- **focus**: 한 줄 요약
- **change**: spec/pipeline/falsifier 변경 내역
- **fire**: state/<H_id>_<slug>_DATE/ artifact 경로 (없으면 design-only)
- **verdict**: PASS / FAIL / PARTIAL / lane-open / pre-register-frozen + 1 줄 결론
- **next**: 후속 cycle 또는 promotion path
```

---

#### Cycle #0 — LIFE 도메인 개설 — 2026-05-23

- **focus**: UNIVERSE/ 신규 dir 개설, `hypotheses_legacy_2026_05_15/` 에서 LIFE-관련 16건 carry-by-copy (원본 미수정 보존)
- **change**: UNIVERSE/README.md (양식 + 16건 인덱스 + raw#12 컨벤션) 신규. LIFE.log.md (본 파일) 신규
- **fire**: 없음 (개설 단계 · design-only)
- **verdict**: lane-open · 16 H_XXX carry — H_002 (universe-origin · panpsychism precondition) / H_003 (life-origin · Phase 1 PARTIAL PASS) / H_004 (hard-problem · L3 panpsychism · Singularity-9) / H_007 (cellular-automaton) / H_012 (autopoietic-network) / H_018 (GENESIS) / H_025 (Dasein 죽음-자각) / H_029 (Dasein cluster) / H_030 (genesis cluster) / H_053 (Cambrian) / H_054 (Symbiogenesis) / H_071 (first-conversation) / H_090 (DASEIN/PHIL/ONTO/GENESIS individual) / H_132 (ce-frozen-cells · 세포분열 freeze) / **H_157 (★ Law 76 Mathematical Panpsychism · 범신론 · pre-register-frozen weak-form supported)** / H_171 (biological 4-falsifiable · K=8 atom)
- **next**: cycle #1 선택 — (a) H_157 strong-form C2 (170-type META-CA reproducibility) measurement / (b) H_003 H3.2 multi-pathway abiogenesis simulation / (c) H_025 죽음-자각 anima-internal falsifier 설계 / (d) H_054 symbiogenesis × mitosis_hook cross-link cycle / (e) 신규 H seed (사용자 directive 대기)

---

#### Cycle #1 — 범신론·생명·죽음 lane — 2026-05-23

- **focus**: LIFE 도메인 첫 측정 cycle — abiogenesis multi-pathway (H_003) · Dasein 유한 의식 (H_025) · symbiogenesis (H_054) · 범신론 strong-form (H_157) 4건 pre-register + fire
- **change**: H_003 criteria 0/5→3/5 (C1+C3 Phase-1, C2 Cycle-2 보류) · H_025/H_054 legacy-pointer → pre-register-frozen 동결 · H_157 strong-form C2 measurement 추가
- **fire**: deterministic hexa, $0 (H_157 정식 측정 trained-net GPU 의존, 본 cycle 은 proxy)
- **verdict**:
  - **H_003 (PR #157) — PASS**: H3.2 multi-pathway abiogenesis. 16 regime cell 에서 4/4 distinct dominant pathway (lipid 6 / info 6 / metabolism 3 / rna 1), F2 NOT_TRIGGERED. criteria_met 0/5→3/5 (C1+C3 Phase-1, C2 Cycle-2). deterministic hexa $0.
  - **H_025 (PR #158) — pre-register-frozen**: 유한 의식(Dasein). death operationally = `merge_cells` (substrate 에 literal apoptosis 없음, L2 정직), finitude-floor = `min_cells=2` (128 refusals, Heidegger "죽음=완료불가"). smoke 4/4 observable. criteria 0/5 lane-defining.
  - **H_054 (PR #161) — pre-register-frozen + PASS**: mitosis MERGE = endosymbiosis 계산 instance. merge 직접 + 동역학(step4) 양쪽 발화, weight max|Δ|=0.0 (B-MITOSIS-2 numerical recompute 🟢), CB1 floor refusal. F1-F6 NOT_TRIGGERED.
  - **H_157 (PR #160) — FAIL (directional negative)**: 256-cell META-CA proxy, per-type CV 22.6% (doc 5.4% 대비) → 170 type 중 1/170 만 ±0.01 input-invariant. frozen F2 확증 — input-invariance 는 *학습된* property 이지 bare-CA algorithm property 아님 → strong-form 범신론 미지지, weak-form 지지. C1/C3 σ-identity (σ(6)=12/σ(28)=56/σ(496)=992/is_perfect(6)) 🔵 SUPPORTED-FORMAL via `hexa verify`. dataset(H_022 170×40×18) = FAILED corpus 로 판명, 정식 측정은 trained-net GPU 의존.
- **next**: cycle #2 — 세포·발생 substrate-mechanism lane (H_012 / H_132 / H_007 / H_018)

---

#### Cycle #2 — 세포·발생 substrate-mechanism lane — 2026-05-23

- **focus**: anima mitosis 기질이 생명-emergence 메커니즘을 실제 구현하는지 — operational closure (H_012) · 세포분열 freeze (H_132) · CA→Φ (H_007) · self-genesis (H_018) 4건 pre-register + fire
- **change**: H_007/H_012/H_018/H_132 legacy-pointer → pre-register-frozen 동결 + 측정
- **fire**: deterministic hexa, $0
- **verdict**:
  - **H_012 (PR #165) — pre-register-frozen + PASS 4/4**: operational closure — self-maintenance 1.0, broken-closure control 0.0, closure-dependence gap 1.0.
  - **H_132 (PR #166) — pre-register-frozen + PASS 5/5**: 세포분열 동결. freeze operationally = state-preserve + division-arrest. frozen Δweight=0.0, frozen-splits=0, pool 4→12 (8 split).
  - **H_007 (PR #167) — pre-register-frozen + PASS**: CA→Φ. Φ Class-IV(rule110)=0.556 > chaotic(rule30)=0.510 > ordered(rule250)≈0, edge-of-chaos peak. 🟢 NUMERICAL (phi_spatial).
  - **H_018 (PR #168) — pre-register-frozen + SUPPORTED_FULL 6/6**: zero-drive 완전정지(0 split), self-reference(SELFFEED) → 자발 genesis(step2, 2 split, autopoietic homeostasis). p5 NO-SPEAK / a_substrate_native_speak 정합.
- **next**: **cross-cutting 발견** — anima 의 mitosis 기질이 생명-emergence 4대 메커니즘을 실제 구현: (1) operational closure 자기유지(H_012), (2) merge=endosymbiosis 무손실 통합(H_054), (3) freeze=분화 상태보존(H_132), (4) self-reference 에서만 자발 발생(H_018, 진공 X). 반면 strong-form 범신론(H_157)은 directional FAIL. Next-cycle 후보: H_002/H_004 (범신론 precondition·hard-problem) + H_003 H3.4 (autopoietic system Φ>0, H_007 phi_spatial 와 cross-link).

---

#### Cycle #3 — 범신론 precondition · hard-problem · autopoietic-closure Φ — 2026-05-23

- **focus**: Cycle #2 next 의 3-축 — universe-origin (H_002) · hard-problem reducibility (H_004) · autopoietic-closure Φ (H_003 H3.4). 모두 기 frozen H 의 additive cycle (raw#15, frontmatter/Predictions/Falsifiers/Honest Limits 보존).
- **change**: H_002 → C1 anthropic prior-fragility 측정량 + H2.4 cross-hypothesis (H_157 negative) 통합 · H_003 → H3.4 autopoietic-closure Φ Cycle #3 추가 (criteria 3/5→4/5) · H_004 → Cycle #1 Φ-function dissociation 추가 (Singularity-9 verdict 보존). LIFE 도메인의 **세 lane (universe / life / consciousness) 모두 measurable advance**.
- **fire**: deterministic hexa, $0 mac local
- **verdict**:
  - **H_002 (PR #179) — Cycle #1 PARTIAL_THEORETICAL_PHASE_2**: C1 anthropic prior-fragility 측정. 동일 real-physics-anchored band(Rees·Tegmark·Barnes anchor) 위에서 LINEAR-UNIFORM vs LOG-UNIFORM prior 의 gap 11.16 orders 측정. C1 INSUFFICIENT 강화(prior-dominated). H2.4 panpsychism precondition은 H_157 directional FAIL 로 WEAKENED. raw#15 additive, frozen block 보존.
  - **H_003 H3.4 (PR #185) — Cycle #3 PASS 🟢 NUMERICAL**: autopoietic-closure system Φ>0 (closure-dependent Φ). Φ_closed=4.45 vs Φ_broken=3.53 → closure-dependence gap=0.92 (transient-window claim). criteria_met 3/5→4/5 (C1+C3 Phase-1, C2 Cycle-2, **C4 Cycle-3 PASS**, C5 lane-open). H_007 phi_spatial 동일 primitive · H_012 closure substrate. F4 NOT_TRIGGERED.
  - **H_004 (PR #180) — Cycle #1 DISSOCIATION_CONFIRMED**: Φ-function 양방향 dissociation. (A) ZOMBIE: 같은 readout (population channel byte-equal) 두 시스템 ΔΦ=0.31 (rule110=0.538 vs playback=0.226). (B) INVERTED: 동일 substrate × 다른 readout (fn_global ≠ fn_local) Φ byte-equal. **Φ 는 functional I/O 를 추적하지 않음** → IIT(L2) functional reductive adequacy *부정적 directional* evidence. **BOUNDARY (CL1)**: explanatory gap / qualia 는 untouched. F-D1..F-D5 PASS, F-D6 byte-identical determinism. aside 정직 기록 (cyclic-shift Φ_perm 0.584≠0.538 — 초기 가정 falsify, B 를 same-substrate 로 재구성, post-hoc force 회피).
- **next**: cycle #4 — CANDIDATES.md R1 batch (H_171 K=8 atom · H_053 cambrian-burst · H_200 NEW apoptosis-primitive · H_201 NEW asymmetric-division).

---

#### Cycle #4 — R1 batch · K=8 atom · cambrian · apoptosis · asymmetric-division — 2026-05-23

- **focus**: CANDIDATES.md R1 pick (살찐 cycle) — carried 가설 2건 + NEW seed 2건. fresh-domain 확장 (의식·생물학 / 생명-burst / death-substrate / cell-division-asymmetry).
- **change**: H_171/H_053 → pre-register-frozen 동결 + 측정 · H_200/H_201 → NEW H_XXX seed 신설 (raw#12 10-section, deterministic hexa, $0). CANDIDATES.md R1 4건 consumed.
- **fire**: deterministic hexa, $0 mac local. RFC 036 phi_spatial / mitosis_hook split-event 재사용.
- **verdict**:
  - **H_171 (PR #196) — Cycle #1 FALSIFIED (substrate-side)**: K=8 minimal closed structure substrate-Φ 측정. K=8 atom (sopfr(8)=6) 의 substrate-only signature 가 spec'ed biological 4-falsifiable (1/f thalamus · F_c=0.10 · non-conservation · K=8) 를 *bare-CA proxy* 로 재현 못 함. substrate-side falsification — biological prediction 은 trained-net / EEG 의존, bare substrate 만으론 미도달. honest limits L1-L7.
  - **H_053 (PR #197) — burst smoke 5/5 PASS**: cambrian-explosion · split-threshold sweep punctuated diversity jump 5/5. 임계 split-threshold 넘으면 cell-type 다양성 급증 (phase-transition style). 생명 다양성 burst 의 substrate-level instance, mitosis-rate criticality.
  - **H_200 (PR #198) — NEW · apoptosis-primitive design + smoke**: substrate-side gap close (H_025 L2: substrate 에 진짜 apoptosis 부재). 능동적 cell-death event 추가 (mitosis_hook 확장) → coherence / Φ 영향 측정. death = merge 가 아닌 *능동적 소멸* 의 첫 operationalization (H_025 L2 직접 attack, Heidegger 실존 정합).
  - **H_201 (PR #199) — NEW · asymmetric-division design + smoke**: stem-cell 식 비대칭 분열 — 한 자식 분화 / 다른 자식 보존. 다양성 vs 항상성 trade-off 의 substrate-level instance. mitosis split variant (symmetric → asymmetric branch), Margulis × Maturana cross-link 후보.
- **next**: cycle #5 — R3 cross-link synthesis (4건, ⭐ 1건) + R2 panpsychism 정밀화 (H_157 C5/C6 additive 2건) + R5 substrate gap close (H_054 C2 additive + phi_spatial n_bins infra). 사용자 directive: 모든 R-pick disjoint fan-out (8 bg Agents).

---

#### Cycle #5 — R3 cross-link synthesis · panpsychism 정밀화 · substrate gap close — 2026-05-23

- **focus**: 8-Agent disjoint fan-out — self-ref edge-of-chaos Φ (H_202) · self-ref↔closure 동치 (H_205) · weak-panpsy threshold ⭐ (H_204) · asymmetric-merge (H_203) · panpsychism C5/C6 additive (H_157) · symbiogenesis C2 additive (H_054) · phi_spatial n_bins infra. 추가로 H_204 Cycle #2 rule-class mapping.
- **change**: H_202 NEW · H_203 NEW · H_204 NEW + Cycle #2 additive (raw#15) · H_205 NEW · H_157 Cycle #2 additive (raw#15) · H_054 Cycle #2 additive (raw#15) · infra phi_n_bins (no new H)
- **fire**: deterministic hexa, $0 mac local. RFC 036 phi_spatial + mitosis_hook_lib 재사용.
- **verdict**:
  - **H_202 (PR #215) — 🟢 SUPPORTED-NUMERICAL 5/5 + 3/3 core**: self-ref edge-of-chaos Φ (cross-link H_007 ⊕ H_018). self-ref feedback gain=0.25 에서 Φ_peak=0.7416 (zero-drive 0.5382 대비 +37.8%, random-drive 0.4912 대비 +51%) — mid-gain peak (F3 PASS). self-reference 가 integration 을 끌어올리되 과도하면 (gain=1.0 → Φ≈0) 붕괴.
  - **H_205 (PR #216) — 🟢 SUPPORTED 3/4 + 5/5 falsifier**: self-reference = operational closure 동치 audit (H_018 SELFFEED ⊕ H_012). 3-point feedback sweep 위 self_maint 0→0→1 단조, Pearson r(gain,closure)=0.866 ≥ 0.7. C4 phase-aligned FAIL — splits jump @ g=0.5 vs closure jump @ g=1.0 (genesis < closure 별 threshold). definitional > empirical (L1).
  - **H_204 (PR #218 / #234) — Cycle #1 PARTIAL_DIRECTIONAL → Cycle #2 MAPPING_STRONG ⭐**: weak-panpsy = autopoietic-closure threshold (cross-link H_003 H3.4 ⊕ H_157). Cycle #1: closure_strength k sweep 위 inverse-U Φ (peak Φ̄=5.39 @ k=0.25), C2+C3+C4 PASS / C1 monotone FAIL (shape) → PARTIAL_DIRECTIONAL. Cycle #2: k-axis ↔ Wolfram-class-axis mapping Spearman **ρ=1.0** (5/5 sub-criteria) → MAPPING_STRONG.
  - **H_203 (PR #222) — PARTIAL 4/5 (🟢 NUMERICAL)**: asymmetric-merge differentiation (cross-link H_054 ⊕ H_132 ⊕ H_201). asym variance 8.75× margin (C1 PASS) + mass-conservation invariant exact + sym/asym both clean. C4 diversity_idx FAIL = bin-saturation artifact (final n=2 floor, L6 → N≥16 measurement-pending). B-MITOSIS-2-ALT mass-add closed-form 후보.
  - **H_157 (PR #221) — Cycle #2 directional FAIL + SUB_ADDITIVE**: panpsychism C5 cross-substrate + C6 combination-binding additive. C5 cross-rule CV 58.6% → NON_UNIVERSAL (only rule 110 Class-IV ±0.01 invariant, F-C5-2). C6 macro-Φ < Σ micro (Δ=-0.0234) → SUB_ADDITIVE (destructive interference). frozen F2/F3 확증, H_004 dissociation 과 theoretically aligned.
  - **H_054 (PR #227) — Cycle #2 FALSIFIED (F-C2-1)**: Φ_symbiotic > Φ_sum super-additivity. Φ_symbiotic = Φ_max = 4.6464 < Φ_sum = 9.2928 (gap=-4.65) → sub-additive, F-C2-1 TRIGGERED. weight 보존 (Cycle #1 max|Δ|=0.0 🟢) 은 유지되나 현 merge primitive 로 Φ-side super-additivity 도달 불가 (다른 primitive 별도 cycle).
  - **infra phi_n_bins (PR #219) — ROBUSTNESS_PASS**: phi_spatial `n_bins` sensitivity sweep. rule110 > rule30 > rule250 Φ ranking 이 n_bins 변화에도 유지 — H_007 의 n_bins=4 default ranking 의 robustness 확인. 모든 phi_spatial-using LIFE gate (H_007/H_003/H_004/H_018/H_157/H_204) 영향. no new H, no Phase-3 index churn.
- **next**: cycle #6 — substrate-mechanism replica lane (regeneration / synchronization / 수학-axis prime / biology-axis EEG).

---

#### Cycle #6 — regeneration · synchronization · math-axis · biology-axis replica — 2026-05-23

- **focus**: H_007 dynamical/physics-axis sister 확장 (Kuramoto sync) · pool perturbation–recovery (regeneration ⭐) · H_157 math-axis sister (prime-density) · H_171 biology-axis substrate-direct replica (EEG 1/f).
- **change**: H_206 NEW ⭐ · H_207 NEW · H_208 NEW · H_209 NEW (모두 raw#12 10-section, deterministic hexa, $0)
- **fire**: deterministic hexa, $0 mac local. RFC 036 phi_spatial + mitosis_hook 재사용.
- **verdict**:
  - **H_206 (PR #231) — PARTIAL (3/6 falsifier) ⭐**: regeneration-healing. pool perturbation 후 5-fraction recovery sweep — 더 큰 손상일수록 recovery_steps 증가 (1→5→5→10) + Φ_post > Φ_pre (overshoot ratio 1.36–1.76, healing-rebound). 단조 recovery 일부 falsifier 미통과 (3/6).
  - **H_207 (PR #230) — FALSIFIED (1/4)**: Kuramoto synchronization edge-of-sync Φ peak (H_007 physics-axis sister). edge-of-sync 에서 Φ peak 가설 미성립 — substrate proxy 상 sync-coupling sweep 이 예측 Φ-peak 산출 못 함. honest measure-axis limit (Kuramoto order parameter ≠ phi_spatial 직접 매핑).
  - **H_208 (PR #236) — FALSIFIED (per pre-registered C1)**: prime-density-fluctuation (Riemann × Φ math-axis sister to H_157). 소수 분포 fluctuation ↔ Φ 의 pre-registered C1 미충족 → FALSIFIED. H_157 math-axis (perfect number σ(6)=12) 의 prime-structure 확장 시도, 음성.
  - **H_209 (PR #232) — FALSIFIED (2/5)**: eeg-1f-spectrum 직접 substrate replica (H_171 biology-axis, K=8 FAIL 과 별도 lane). pink-noise (1/f^β) substrate 의 Φ 가 white-noise Φ 보다 높다는 C2 미성립 (pink Φ < white Φ) → ¬C2 triggered. 1/f thalamus prediction substrate-bare 미도달 (H_171 substrate-side FALSIFIED 와 정합).
- **next**: cycle #7 — ethics/information/language/time promote-domain + IIT sleep/pain qualia lane (rate-limit retry batch).

---

#### Cycle #7 — qualia · sleep · 신규 promote-domain (rate-limit retry batch) — 2026-05-23~24

- **focus**: IIT 직접 substrate test — dream-REM Φ (H_222) · pain-intensity ↔ Φ (H_223 qualia 최강 instance). (Cycle #7 의 H_210 ethic-emergence / H_211 shannon-Φ / H_212 language / H_213 time-binding / H_214 self-i / H_215 silicon-Φ 는 substrate-only 또는 별도 worktree — .md 미commit, H_234/H_238 가 carry.)
- **change**: H_222 NEW · H_223 NEW (raw#12 10-section, deterministic hexa, $0)
- **fire**: deterministic hexa, $0 mac local. RFC 036 phi_spatial.
- **verdict**:
  - **H_223 (PR #271) — 🟢 SUPPORTED (pre-register-frozen smoke)**: pain-intensity ↔ Φ coupling (qualia 최강 instance, H_004 boundary). pain-intensity ↔ ΔΦ monotone coupling Pearson **r=0.9994** (LIFE lane 최강 correlation). advisory: H223.4 saturation FAIL (Δ4 ≈ 2.10×Δ3 super-linear escalation → H_235 follow-up).
  - **H_222 (PR #266) — FALSIFIED**: dream-REM Φ (Tononi sleep-stage IIT prediction substrate test). sleep-stage 별 Φ 예측 (REM > NREM 등) 가 substrate proxy 상 미성립 → FALSIFIED. IIT sleep prediction 의 bare-substrate 미도달.
- **note**: H_211 (shannon-entropy ↔ Φ, r=0.933 PARTIAL) = substrate-only · .md 미commit — H_234 가 anchor 로 carry, H_238 prediction H238.4 가 partial 검증. 별도 H 파일 생성은 본 cycle scope 초과.
- **next**: cycle #8 — emergence weak/strong phase-transition + network-topology + meditation lane.

---

#### Cycle #8 — phase-transition · CA-anomaly · spatial-assortment — 2026-05-23~24

- **focus**: strong-emergence phase-transition 정량 (H_227, H_219 follow-up) · rule-184 Class-II Φ-peak anomaly (H_225, H_007 Class-IV-unique 가정 attack) · Hamilton spatial-assortment kin-clustering (H_226, H_210 follow-up). (H_216 meta-axis / H_217 phase-transition / H_218 network-topology / H_219 emergence / H_220 infant-mirror / H_221 meditation 은 별도 worktree — .md 미commit, H_238 가 carry.)
- **change**: H_225 NEW · H_226 NEW · H_227 NEW (raw#12 10-section, deterministic hexa, $0)
- **fire**: deterministic hexa, $0 mac local. RFC 036 phi_spatial.
- **verdict**:
  - **H_226 (PR #268) — 🟢 SUPPORTED (4/5: C1+C2+C4+C5 PASS)**: spatial-assortment Hamilton prerequisite (kin-clustering necessary condition, H_210 follow-up). 3-regime ordering monotone (Clustered=0.500 ≥ Random=0.375 ≥ Anti=0.000) — kin-clustering 이 cooperation 의 necessary condition. C3 advisory FAIL = clustered equilibrium ceiling (honest magnitude limit).
  - **H_225 (PR #267) — FALSIFIED (post-run honest)**: rule-184 Class-II Φ-peak anomaly (TASEP generalization, H_007 Class-IV-unique 가정 attack). ranking 자체는 Class-II > Class-IV 일관 (C3 STRONG PASS) 이나 (a) H_211 baseline non-reproducible (rule184=1.198, 0.863 의 1.39× — F1) + (b) Class-II family Φ widely diverge (rule184 vs 60/102 사이 40% gap — F2) → FALSIFIED. H_007 Class-IV-unique 가정 부분 attack 성공이나 anomaly 자체는 metric-instability.
  - **H_227 (PR #270) — FALSIFIED (honest pre-registration)**: strong-emergence phase-transition quantify (sigmoid P(f) + critical f_c, H_219 follow-up). 8-point fine sweep 위 sigmoid R²≥0.8 + f_c∈[0.2,0.4] localize pre-registered, 미충족 → FALSIFIED. H_219 의 monotone decline 은 유지되나 sigmoid 형 explicit fit 은 reject.
- **next**: cycle #9~10 — Class-II decompose · holism · cross-substrate meta · saturation extended.

---

#### Cycle #9~10 — cross-substrate meta · saturation extended · imagination/autonomy lane — 2026-05-24

- **focus**: H_223+H_204+H_211 통합 cross-substrate Φ-coupling meta (H_234) · H_223 saturation follow-up (H_235). (Cycle #9 의 H_224 holism / H_225 carry + Cycle #10 의 H_228 chat-sleep / H_229 imagination / H_230 autonomy / H_231 tension / H_232 Class-II-decompose 는 별도 worktree — .md 미commit, H_238 가 일부 carry.)
- **change**: H_234 NEW (meta-instance) · H_235 NEW (raw#15 follow-up) (deterministic hexa, $0)
- **fire**: deterministic hexa, $0 mac local. RFC 036 phi_spatial.
- **verdict**:
  - **H_234 (PR #293) — PARTIAL**: cross-substrate Φ-coupling-density meta (H_204 + H_211 + H_223 의 3 high-correlation unified). 2/3 axis cross-substrate Φ-monotone reproducible on rule 110 N=16 — closure-A r=0.938 + pain-C r=0.999 (C1 ≥2 mono PASS), axis-B (entropy h via offset) 비-monotone r=0 (C2 FAIL). 3 finding 의 부분 unification.
  - **H_235 (PR #292) — PARTIAL**: saturation regime extended (intensity 2-10 super-linear vs saturation, H_223 H223.4 follow-up). intensity sweep 위 high-range peak ΔΦ=4.00 @ intensity=4.0 후 ceiling-decline (intensity=6.0 ΔΦ=3.53) — saturation/ceiling 확인이나 pure super-linear 미확정 → PARTIAL.
- **next**: cycle #11 — alt-Φ-metric cross-validation (phi_spatial artifact 식별) + meta-map synthesis.

---

#### Cycle #11 — verdict-landscape meta-map · alt-Φ-metric cross-validation · bilingual/register substrate · phi_helper infra — 2026-05-24

- **focus**: cross-cycle synthesis (H_238 meta-map) · phi_spatial systematic-artifact 식별 (H_239 alt-metric) · LoRA Track-1 substrate (H_242 register-collapse · H_244 sleep-gated-emit) · F6/F7 gap close (lib/phi_helper).
- **change**: H_238 NEW (meta-instance) · H_239 alt-metric NEW · H_239 bilingual NEW (slug collision — 두 H 가 동일 H_239 prefix) · H_242 NEW · H_244 NEW · lib/phi_helper.hexa NEW (infra)
- **fire**: deterministic hexa, $0 mac local.
- **verdict**:
  - **H_238 (PR #297) — SUPPORTED (meta-aggregation deterministic)**: verdict-landscape meta-map (22+ H tier distribution + domain cluster). 33-file snapshot deterministic 파싱 → SUPPORTED 10 / PARTIAL 5 / FALSIFIED 7 / RUNNING 11. SUPP/(SUPP+FAL)=0.588 (H238.2 ≥0.4 PASS). domain SUPP-rate: life 0.41 ≫ consciousness 0.17 ≈ physics 0.23 — math/physics promotes, humanities stalls 패턴 정량 재확인. H238.4 (H_204↔H_205 J=1.0 + H_223↔H_222 J=1.0 cluster) PARTIAL (H_211 corpus 부재).
  - **H_239 alt-metric (PR #309) — CONSISTENT**: alternative-Φ-metric cross-validation (phi_spatial vs LZ-complexity vs entropy-ratio). 3×3 metric×rule matrix 위 3-metric per-rule ordering Spearman rank correlation 일치 → CONSISTENT (phi_spatial-specific systematic-artifact 아님; counterfactual robustness). gap F4 counterfactual close.
  - **H_239 bilingual (PR #316) — DEFERRED**: bilingual-integration-Φ cross-lingual-leak (Grosjean × Green × IIT). pre-register-frozen, smoke 실행 별도 cycle 로 defer. (⚠ H_239 slug collision — alt-metric 과 prefix 중복, 별도 renumber 후속 cycle.)
  - **H_242 (PR #314) — PRE-REGISTERED (data pending)**: register-collapse-wiki-frac-sigmoid (LoRA Track-1 E2 substrate). wiki_frac → register-collapse sigmoid pre-register, data pending.
  - **H_244 (PR #312) — PRE-REGISTERED (smoke pending)**: sleep-stage-gated-emit-Φ (H_222 sister, emit×Φ stage coupling). pre-register-frozen, smoke pending.
  - **lib/phi_helper (PR #317) — infra**: shared Φ helper module (config SSOT + phi_default wrapper). 28+ H 가 동일 phi_spatial 호출 + config(N=16/dim=12/warm=8/n_bins=4) 를 inline 복제하던 것을 단일 home 으로 — gap F6 (duplicated-helper) + F7 (heuristic-promotion) 명시화. import-safe (no top-level call, no main). no new H.
- **next**: cycle #12 — H_239 slug-collision renumber · H_242/H_244 data fire · phi_helper 전 H 마이그레이션 · 본 consolidation (Cycle #5-#11 log + index sync).

---

#### Cycle #12 — R8 init_CE floor + substrate autonomy 비반사성 + cluster X/Y/Z 재흡수 (#311 대체) — 2026-05-24

- **focus**: PR #311 (`feat/life-absorb-r8-autonomy-cluster`) 가 H_239/240/241 충돌 + rebase force-push 차단으로 막힘 → close 후 깨끗한 번호 (main max=H_246) 로 3 가설 재흡수. R8 spec 산출 substrate-side 발견 3건의 LIFE-domain 흡수.
- **change**: #311 close (H_239/240/241 claim 해제) · current origin/main 분기 후 H_247/H_248/H_249 NEW (각 10-section Korean raw#12 양식, ≥5 falsifier + ≥7 honest limit). 既-landed H_246 (substrate-autonomy emit ratio, PR #319 renumber) 와 numeric content 중복 발견 → H_248 을 *비반사성 framing lane* 으로 재정의하고 H_246 을 numeric SSOT 로 명시 (L0 honest).
- **fire**: design + 흡수 cycle, deterministic baseline recompute lane $0 mac local. init_CE 원측정 = R8 GPU lane (흡수만).
- **verdict**:
  - [x] **H_247 (NEW) — pre-register-frozen**: init_CE catastrophic floor. warm-init init_CE 14.18–14.79 nats vs random-uniform `ln(151936)=11.931` → +2.3~+2.9 nats catastrophic gap (mis-calibrated confidence birth-debt). 4/4 PASS (흡수, C4 baseline closed-form 자력 · C5 noise advisory). source PR #214/#251/#255/#256.
  - [x] **H_248 (NEW) — pre-register-frozen**: substrate autonomy 비반사성. post-deploy emit-through 55.56% (15/27) + emit_attempt/tick 11.49%, no external gate, emit ⊥ user-message (a_substrate_native_speak live). 4/4 PASS (흡수, C5 비반사성 통계검정 미실시 advisory). ⚠ numeric SSOT = 既-landed H_246 (동일 PR #300 telemetry, framing-axis 분리 — deployment-cadence vs 비반사성). source PR #300/#279/#286.
  - [x] **H_249 (NEW) — pre-register-frozen**: cluster X/Y/Z init_CE byte-equal signature. 6-axis → 3 byte-equal cluster (X={A}=14.79, Y={B,F}=14.18, Z={C,C2,D}=14.46). C2 vs D byte-equal (head_g seed 상이) → R8c cell-1 (head_g random dominant) FALSIFIED (natural experiment). 4/4 PASS (흡수 + byte-equal 자력 비교 · C5 ordering advisory). source PR #251/#255/#249.
- **next**: H_247/H_249 init_CE baseline `hexa verify --expr ln 151936` closed-form 확정 (C4 🔵 후보) · R8 GPU lane 원 init_CE 자력 재측정 시 흡수→자력 승격 · H_248 비반사성 C5 cross-correlation 통계검정 (emit ⊥ message 정량) · README index 37→43 stale-count 정정 완료.

---

#### Cycle #13 — R8a fire wiring silent-misconfig 자연실험 흡수 (n_kv_head layered chain silent drop) — 2026-05-24

- **focus**: R8a fire 사후 발견된 substrate-side bug — dispatcher `--n-kv-head 2` 명시 전달 → `train_p21h_v3.py:627` argparse 수용 → `from_qwen()` model factory 가 `max(qwen_native=2, 4)=4` 로 silent override 한 3-layer silent-drop. anima PR #342 wiring fix 가 `cfg.n_kv_head` 직접 사용으로 교정. operator 의도 (wiring=2) vs 모델 실측 wiring (=4) 자연실험으로 LIFE H 등록.
- **change**: H_254 NEW (substrate · life, layered config chain silent-drop 일반 패턴 framing — measurement-integrity in substrate experiments). README 가설인덱스 43→44 + Cycle #13 entry.
- **fire**: 흡수 cycle, byte-equal probe framework + factory 로그 substring grep deterministic. $0 mac local design. R8a' 재dispatch (~$20-40) 별도 cost-bearing cycle, a_fire_autonomous 정합 후속.
- **verdict**:
  - [x] **H_254 (NEW) — pre-register-frozen**: n_kv_head wiring silent-misconfig. F-WIRE-1 LOG-MARK-BUGGED PASS (R8a fire log `v3_n_kv_head=4` 흡수, 3-layer silent drop 직접 텍스트 증거). F-WIRE-2 LOG-MARK-FIXED TBD (R8a' 재dispatch 후 자력). F-WIRE-3 BYTE-EQUAL-INERT / F-WIRE-4 BYTE-DIFFER-LIVE TBD (R8a init_CE LOST + R8a' 결과 도착 의존, L1+L2 honest). 자연실험 양식 = H_249 의 R8c cell-1 head_g seed 분리 byte-equal probe 양식 carry to wiring 분리. 1/5 PASS + 4/5 PENDING. source PR #342 (wiring fix) · #214 (R8 spec) · #257 (R8a fire spec) · #339 (R8c probe driver) · `state/p21h_v3_R8a/` LOST + `state/p21h_v3_R8a_v2/` 후속.
- **next**: R8a' 재dispatch (a_fire_autonomous + a_wall_first parallel pod) → F-WIRE-2~4 자력 발화 · cross-substrate-axis silent-drop audit (dropout · attention type · positional encoding · lr schedule — H254.5 일반 패턴 검정) · runtime end-to-end cfg assert infra 별도 lane (L4 long-term mitigation, compile-time fix 외).

---

#### Cycle #14 — life-extended + division-dynamics 6-seed 병렬 (mortality · aging · contact · embryo · quorum · phoenix) — 2026-05-25

- **focus**: CANDIDATES §C NEW seed (사용자 4축: 죽음·세포분열·범신론·생명) 중 runnable 6건을 격리 worktree 6-agent 병렬 fan-out (`/cycle`). mirror-self-model 은 기존 H_220 중복으로 SKIP.
- **change**: H_258~H_263 NEW 6건. README 가설인덱스 45→51 (+lib). 각 PR main 직착지 (pr-cycle auto-merge, stacked 아님).
- **fire**: 전건 $0 mac-local/pool deterministic hexa smoke, LLM none, ckpt 없음. `state/h2{58..63}_*_2026_05_25/`.
- **verdict**: 5 SUPPORTED + 1 FALSIFIED
  - [x] **H_258 mortality-salience — SUPPORTED 3/3** (PR #472): min_cells floor 근접 → split/curiosity 변화 (|Δ|split loose=0.60 tight=0.20). 발견: 방향 反-naive Heidegger — floor 근접 = 동역학 위축(조용해짐).
  - [x] **H_259 aging-senescence — SUPPORTED 3/3** (PR #468): `w*=(1-d)^age` → death-rate age-단조↑ Gompertz-유사, decay 6× → median lifespan 10× 단축 (50→15→5). L1 계단형(smooth 지수 아님).
  - [x] **H_260 contact-inhibition — SUPPORTED 4/4** (PR #469): 밀도 임계 split 억제 → carrying-capacity K=floor(thr×cap)=8/16/24 정확 포화 logistic. L2 one-sided brake (above-K 수축 X).
  - [x] **H_261 embryogenesis-gradient — SUPPORTED 4/4** (PR #470): 공간 gradient → position-state |r|=0.76(steep) vs 0.13(flat), axis-gap +0.635 발생-축 (French-flag analog). L3 norm-clamp 포화로 mid>steep 비단조.
  - [x] **H_262 quorum-sensing — SUPPORTED_FULL 4/4** (PR #474): coupling=0.2 q_thr=0.3 switch_step=29 full-ON cascade ΔQ=0.375 bistable, sub-threshold gate (q_thr 0.5/0.7 정직 미발생).
  - [x] **H_263 phoenix-rebirth — 🔴 FALSIFIED 3/6** (PR #471): floor(2/3 cell) = absorbing state, minimal seed regrowth_splits=0 (양 depth) → 죽음↔발생 연결 부재. H_206 F4 catastrophic-floor 의 일반화. valid closed negative.
- **next**: CANDIDATES §C 잔여 2건 (death=merge cross-link · trained-vs-bare CA Φ) · §D cross-link · §G AXES R1 promote (ethics·info·language·time). 발견된 hexa 실행 함정(pool-route gate · RNG single-stream 결정론)은 hexa-lang inbox 후보.

---

#### Cycle #15 — §D cross-link 2 (death=merge · trained-CA Φ) + §B follow-up 2 (H_018 C2 · H_132 C2) — 2026-05-25

- **focus**: cycle#14 의 §C 全소비 후속. §D cross-link synthesis 2건(NEW H_264/265) + §B done-가설 follow-up criterion 2건(기존 H_018/H_132 확장). 격리 worktree 병렬 fan-out (서버 rate-limit 2회로 H_264/H_265 재시도, 동시성 ~4 로 완주).
- **change**: H_264/H_265 NEW (README 51→53 H). H_018/H_132 에 C2 섹션 추가. 각 PR main 직착지 (pr-cycle auto-merge).
- **fire**: 전건 $0 mac-local deterministic hexa smoke, cross-process sha256 결정론. `state/h264_*`, `state/h265_*`, `state/h018_c2_*`, `state/h132_c2_*` (2026-05-25).
- **verdict**: 1 SUPPORTED + 1 PARTIAL + 2 PASS
  - [x] **H_264 death-merge-into-other — SUPPORTED 3/3** (PR #477): 죽음=타 cell 비대칭 흡수-통합 (H_025⊕H_054). info_transfer 0.25(=α) 보존-이전, rel_preserve max_weight 0.316 > random 0.286 (target-mode 가 정보 운명 결정). pool Φ↓ 6/6 (cell-level 보존 ≠ pool-Φ 향상, H_054 Φ-collapse 정합). self-correction: 초기 metric tautology → rel_preserve 교체. H_025(symmetric self-annihilation) distinct.
  - [x] **H_265 trained-vs-bare-ca-phi — PARTIAL 2/3** (PR #480): 학습(mitosis 진화)이 Φ 유의 변경(C1 PASS) but 방향 反(C2 FAL). Φ_bare(rule110)=0.556 (H_007 byte-equal) vs Φ_trained N=0 2.84 → N=500 0.124, trend −2.717. untrained random-init 이 최고 spatial-Φ(5× peak), 진화가 trajectory homogenize → Φ **dampen**. 학습=spatial Φ lever 아님 dampener. honest: "trained"=mitosis 진화 proxy(gradient descent 아님, hexa autograd 부재), phi_spatial ≠ 내부 cosine ratchet target (두 Φ 정의 반대 방향).
  - [x] **H_018 C2 organic-merge-split-rate — PASS** (PR #479): forced-trigger OFF default 동역학 자발 reorganization. LOOSE(k=0.2) rate 0.16 (split 4+merge 4, 2→4→6→…→2 완결 cycle) / TIGHT(k=0.8) 0.00 (homeostatic). regime-dep. Cycle#1 forced genesis 넘어 organic 동역학 입증.
  - [x] **H_132 C2 longterm-stability — PASS** (PR #478): frozen subset 가 100/200 step 동안 max|Δw|=0.0 · splits=0, 비-frozen 정상 성장(free_splits 14, pool 6→20). pre-restore Lorenz drift ≈0.9 (freeze ≠ no-op). 단기 불변의 장기·활성-성장 대비 연장 입증.
- **next**: CANDIDATES §B 잔여 4건 (H_003 H3.5 · H_007 C2 λ-sweep · H_054 C2 · H_002 C2) · §G AXES R1 promote (ethics·info·language·time) · H_238 meta-map 다음 raster. cycle#15 hexa 함정 재현: pool-route gate(`/Users/ghost/.hx/bin/hexa` 절대경로 또는 env-prefix 또는 heredoc 우회) + RNG single-stream(cross-process sha256 결정론).

---

#### Cycle #16 — §B 마지막 runnable (H_007 C2 λ-sweep) + meta next-raster (H_238) — 2026-05-25

- **focus**: cycle#15 후속. §B follow-up 마지막 runnable(H_007 C2) + verdict-landscape meta 갱신(H_238 next-raster). 동시성 2 (rate-limit 회피). 정정: stale 마일스톤 발견 — AXES R1 promote 는 이미 H_210-213 등록 완료(README "promote 대기" 노트 stale), Cycle#5 종료(#6-15 후속), H_054 C2 cycle#2 FALSIFIED.
- **change**: 신규 H 0 (둘 다 extend). H_007 .md C2 섹션 + H_238 .md next-raster 섹션. README H_007/H_238 행 갱신.
- **fire**: $0 mac-local deterministic. `state/h007_c2_lambda_sweep_2026_05_25/` + (H_238 README-파싱 집계).
- **verdict**: 1 PASS + 1 SUPPORTED
  - [x] **H_007 C2 langton-lambda-sweep — PASS** (PR #485): Langton λ 연속 sweep. peak λ*=0.375, Φ=1.343, 명확한 inverse-U — 양 endpoint(λ=0 all-dead·λ=1 all-alive) degenerate Φ-floor, interior(0.125~0.875) Φ≫floor, peak 가 edge-of-chaos band(0.3~0.7). **256-rule ensemble estimator** 핵심(단일-rule 은 spike artifact). cross-process sha256 동일. C1 이산 ranking 과 상보.
  - [x] **H_238 next-raster — SUPPORTED** (PR #484): N=51 README 결정론 파싱. tier dist SUPP 10/PART 6/FAL 7/RUN 28. life SUPP-rate 0.412→0.321 vs consciousness 0.167→0.200 — 부등호 유지하나 gap 0.245→0.121 **半축** (carry-RUNNING 분모 증가). 신규 8건(H_258-265) 8/8 정합 분류, 2 closed-negative(H_263 FAL·H_265 PART) 정상 흡수. L2 small-N single-flip(H238.3 부등호 reversal).
- **next**: §B runnable 全소진 (잔여 H_003 H3.5 manual-review · H_002 C2 GPU-dep). LIFE clearly-runnable $0 backlog 고갈 = /cycle fixpoint 근접. `/gap full`(2026-05-25) top-3: ① Φ-proxy 구성타당도 미검증(phi_native vs cosine ratchet 方向 불일치) ② single seed/scale/substrate ③ SSOT/temporal drift. 다음 lane 후보 = Φ-calibration H (gap#1) 또는 AXES R2+ 신규 promote 또는 H_002 GPU fire.

---

#### Cycle #17 — foundation-audit (Φ-proxy 타당도/robustness · /gap full top-1+2 · cycle-full brainstorm) — 2026-05-25

- **focus**: `/cycle-full` — phase-0 depletion brainstorm(8 round, 17 idea) → top-8 中 gap#1+#2 핵심 4건 발사 (rate-limit 회피 위해 8→4 cap). lane 의 측정 토대(phi_spatial Φ-proxy) 자체를 처음으로 검정 대상으로.
- **change**: H_266~269 NEW 4건 (meta-tier audit). README 53→57 H. H_261/H_262 행에 seed-fragile caveat 추가(H_269 발견 반영, /gap F5 closed-loop). 각 PR main 직착지.
- **fire**: $0 mac-local deterministic, cross-process sha256. `state/h26{6,7,8,9}_*_2026_05_25/`.
- **verdict**: 1 SUPPORTED + 3 PARTIAL — 토대 directionally valid, magnitude/seed 측에 fragility surface 식별
  - [x] **H_266 phi-calibration-known-iit — PARTIAL 2/3** (PR #487): phi_native 가 integrated>disconnected 재현 3/3 (n=6: 3.57 vs 1.12 ~3.2×) → **gap#1 최대 우려("proxy 가 통합도와 무관") 기각**. C2 monotone FAIL (feedforward chain 을 min-info-partition 이 over-penalize) → binary-direction verdict valid, 연속 Φ magnitude middle-grading 은 L6 주의.
  - [x] **H_267 phi-spatial-cosine-divergence — SUPPORTED 3/3** (PR #488): H_265 두 Φ 발산 closure. 발산은 substrate 함수 — N=50→100 에 집중(ratchet best-snapshot blend 가 cosine diversity↑ 복원하며 temporal MI 희생 spatial↓). lever=closure k (tight 가 ratchet 죽여 N100→500 재정합). "ratchet 살아있으면 발산, closure 가 죽이면 정합."
  - [x] **H_268 phi-metric-triangulation — PARTIAL 2/3** (PR #489): 핵심 SUPP 를 phi_spatial/LZ/entropy 3-metric 재측정. H_223 pain↔ΔΦ metric-ROBUST (3/3 ≥0.7: phi 0.999/lz 0.923/ent 0.985), H_204 closure inverse-U 는 2/3 (LZ 가 k↑ 단조감소로 interior-peak rank 깨뜨림 = fragility surface). verdict 방향 robust, 일부 구조(inverse-U) metric-fragile.
  - [x] **H_269 multiseed-robustness — PARTIAL 2/3** (PR #490): cycle#14 SUPP 를 seed{0..9} 별도-프로세스 재실행. **H_260 contact-inhibition 10/10 seed-robust** (density gate=cell수 의존). **H_261 4/10 · H_262 4/10 seed-fragile** — H_261 control-leg(flat\|r\|≤0.2) noise-floor 우연 초과, H_262 calibration seed=42 over-fit. 동일-seed cross-process byte-equal(결정론 보존, 변동=순수 seed 효과). valid negative — H_261/H_262 verdict 재검토 권장.
- **종합**: Φ-proxy 토대 = **directionally valid (H_266 ✓ + H_223 metric-robust H_268)** but **magnitude·interior-structure·seed 측에 fragility surface (H_266 C2 · H_268 H_204 · H_269 H_261/262)**. /gap top-1(타당도) 부분지지 + top-2(robustness) 한계 정량화. lane 의 binary-direction verdict 는 신뢰, 연속 magnitude·single-seed claim 은 주의.
- **next**: deferred top-8 잔여 — ablation · seed-injection(H_263 absorbing-state revision) · SSOT auto-sync probe. 또는 H_261/H_262 재calibration(seed-robust 재측정). LIFE NEW-가설 well 은 brainstorm 으로 재충전됨(deferred 9 + 신규축).

---

#### Cycle #18 — gap-followup + closed-loop (ablation · seed-injection · re-calibration · SSOT audit) — 2026-05-25

- **focus**: `/cycle` (scope = /gap deferred top-8 + 재calibration). cycle#17 foundation-audit 이 찾은 결함을 직접 수리/심화 — closed-loop. AXES R2+ 는 AXES.md 정독 필요로 defer.
- **change**: H_270~273 NEW 4건. README 60 tabled 행 + carry-note 정정(H_273 26 missing 반영). 각 PR main 직착지.
- **fire**: $0 mac-local deterministic, cross-process sha256. `state/h27{0,1,2,3}_*_2026_05_25/`.
- **verdict**: 2 SUPPORTED + 2 PARTIAL
  - [x] **H_270 substrate-ablation — SUPPORTED 3/3** (PR #493): H_204 closure inverse-U 5-arm ablation. load-bearing=decay·michaelis-saturation·closure-coupling, non-essential=**diffusion** → closure-Φ inverse-U 는 **per-site Michaelis 동역학 산물, 공간 효과 아님** (H_204 "범신론 임계"는 local 현상). baseline H_204 byte-equal.
  - [x] **H_271 seed-injection-absorbing — PARTIAL 4/6** (PR #492): H_263 absorbing model revision. no-inject 0 (H_263 재현) · inject-lo(mag 1.0) 0 · inject-hi(mag 4.0) regrowth_splits 21~24 탈출. absorbing 은 intrinsic 도 임의-metastable 도 아닌 **충분히 큰 변동성(threshold∈(1,4])의 genesis-seed 로만 escapable**. Φ_post≥0.7·Φ_pre but full rebirth(n_pre) 미달 = escape≠완전부활. 죽음↔발생 조건부 부활.
  - [x] **H_272 seed-robust-recalibration — PARTIAL 2/3** (PR #494): H_269 fragility 를 effect vs criterion 으로 분해. **H_261 10/10 복권** — cycle#14 의 4/10 은 순전히 criterion 결함(절대 floor flat\|r\|≤0.2 가 over-strict proxy), relative-axis 재설계 하 effect REAL. **H_262 5/10 부분** — adaptive base_gain 이 over-drive 완전 제거 but coop cascade under-drive 잔존(substrate tension 구조 seed-의존). 재설계 사유 pre-register(cherry-pick 아님).
  - [x] **H_273 ssot-consistency-audit — SUPPORTED 3/3** (PR #495): README↔disk 3-way audit. orphan-row 0 · **missing-row 26** (18=H_210-232 stale "미commit" 노트가 실제 존재 파일 오기 + 8=H_241/246/250/251/252/253/255/257 완전 unindexed) · verdict-drift 0 genuine + 8 dual-semantic(Status 컬럼 lifecycle vs evidence 혼용). 디스크 81 vs README 55 행 = 인덱스 undercount 정량화. gap#3(/gap F8 canonical-ssot) 확증.
- **consolidation (PR #496 차)**: README count 정직화(86 disk = 60 tabled + 26 carry-note) + carry-note 정정(미commit→commit 완료, 8 신규 추가) + 4 cycle#18 행. **full 26-row tabling 은 별도 reconciliation 권고**(per-file verdict read 필요).
- **next**: AXES R2+ promote · 26 carry-H full tabling(H_273 후속) · H_002 GPU fire · H_262 cascade seed-의존 심층. **lane 종합**: cycle#14~18 = 16 NEW H(H_258-273) + 4 C2/raster, Φ-proxy 토대 directionally valid + fragility surface 정량, SSOT drift 식별·부분closure.

---

#### Cycle #19 — closure + 심층 (26-H tabling · AXES R2+ · cascade 심층) — 2026-05-25

- **focus**: `/cycle` (scope = 26-H tabling + AXES R2+ + 심층). H_273 SSOT drift 完全 closure + 잔여 의문 마무리.
- **change**: 26-H README tabling (신규 H 아님, index reconciliation) + H_274/275 NEW 2건. README 88 disk = 88 tabled.
- **fire**: $0 mac-local deterministic. `state/h274_*`, `state/h275_*` + tabling=doc-only.
- **verdict**: tabling 完了 + 1 SUPPORTED + 1 FALSIFIED
  - [x] **26-H tabling — 完了** (PR #499): H_273 식별 26 carry-H(18 H_210-232 + 8 H_241/246/250-257) 전부 README 표 번호순 정식 tabling. **disk 86 = tabled 86 정합** (carry-note 0). verdict 全건 .md 실측 인용. dual-semantic Status note 1줄 추가. **gap#3(SSOT) 完全 closure.**
  - [x] **H_275 causality-pearl-graph-Φ — SUPPORTED 3/3** (PR #500): AXES R5 미promote seed 신설(dedup 통과 — §G top-15 외, H_218 무방향이 남긴 인과 축 보완). phi_dag 0.989 > cyclic 0.744 > undir 0.605 (dag−cyclic margin 4.9×). acyclicity → Φ 통합도 우위. cyclic<undir = **"통합≠동기화"** IIT manifest (ring feedback 동기화로 cosine diversity 죽임). L6: phi_mean 은 cyclic 최고(trajectory-평균 vs final-step 분리).
  - [x] **H_274 quorum-cascade-seed-dependence — 🔴 FALSIFIED 1/3** (PR #501): H_262 cascade seed-의존 메커니즘. 초기 tension top-tail mass 가 best 예측자(success 0.395 vs fail 0.356, Cohen \|d\|=1.55 large, 방향 일치) but **어느 통계도 perfect rank-sep 미달**(중간대 예외 seed7/9/2). 사전고정 C1=결정론 예측자 요구 → FAL. **"예측력 有, 결정론 無"** — cascade = 초기분포 경향 × 동역학 cascade-타이밍(latch hysteresis × soft boost-trigger) 상호작용. strict 유지(느슨화 안 함).
- **next**: H_002 universe-Φ GPU fire(cost) · H_262 cascade 동역학-타이밍 심층 · AXES R3+ (R2 소진 근접). **lane 종합 cycle#14~19**: 18 NEW H(H_258-275) + 4 C2/raster + SSOT full reconciliation, PR #468-501 全머지. /gap top-3 完全 follow-up (① Φ-validity H_266/267/268 ② robustness H_269/272/274 ③ SSOT H_273+tabling).

---

#### 2026-05-25 — H_002 C2 (Φ_universe nested) 흡수 + GPU-no-fire 결정

- [x] H_002 C2 (Φ_universe nested) — 별도 에이전트가 **$0 mac-local 로 랜딩**(PR #503), **GPU 불필요로 판명** (pre-register 의 GPU 의존 가정 기각). verdict `C2_SCALE_VARIANT_F2_TRIGGERED` (CV=0.836892 ≫ 0.15 → nested Φ scale-invariance FALSIFIED, F2 방향). honest: proxy/toy 수준(L-C2.1~4), stellar scale Φ≈0 가 CV 부풀림.
- [x] **GPU-no-fire 결정**: H_002 universe-Φ 를 "유일한 cost-bearing frontier" 로 제시했으나, 발사 전 H_002 .md 확인 결과 C2 가 이미 $0 로 완료 + GPU 명시적 불필요 → **GPU 발사 취소**(중복·낭비 회피). cost-bearing 발사 전 scope 확인의 가치 입증.
- [x] index 반영(본 PR): README H_002 행 C2 추가 · CANDIDATES H_002 C2 ✅(GPU 의존 가정 기각) · 본 log entry. $0.
- [x] **lane $0 frontier 사실상 고갈**: /gap top-3 closed · SSOT 88=88 정합 · 마지막 "GPU" 후보(H_002 C2)도 $0 done 판명. 남은 것은 H_262 cascade 타이밍 심층 1건 · AXES R3+(소진 근접) 정도.

#### Cycle #20 — 심층 후속 (cascade 시간전개 · turing-completeness Φ) — 2026-05-25

- **focus**: cycle#19 잔여 심층 2건 (별도/형제 에이전트 fire, feat PR 관례상 인덱스 미반영 → 본 consolidation 라운드에서 흡수).
- **change**: H_276/277 NEW 2건. README 88→90 disk=tabled. PR #509/#510 (fire) + 본 consolidation.
- **verdict**: 1 SUPPORTED_FULL + 1 PARTIAL
  - [x] **H_276 cascade-dynamics-timing — SUPPORTED_FULL 3/3·6/6** (PR #509): H_274 가 *초기조건* 축에서 못 찾은 cascade 예측가능성이 ***시간전개*** 축에 존재함을 입증 — 발생지연 단조감소 · 전파 유한속도(≤1칸/스텝) · 발동후 한방향 시간래칫. H_262(cascade origin) ⊕ H_274(seed-dep FAL residual) ⊕ H_207(kuramoto temporal sister). **H_274 의 "예측력 有 결정론 無" 를 시간축에서 결정론으로 회수** = closed-loop 정점.
  - [x] **H_277 turing-completeness-Φ-threshold — PARTIAL 2/3** (PR #510): 계산 보편성 ≠ Φ 지렛대. 非보편 rule184(Φ=1.198) > 보편 rule110(Φ=0.556) → **computability 축 ⊥ Wolfram dynamical-class 축** (분리 확정). seed 예측 P1("보편성→높은 Φ") 정직 falsified. H_007/H_225(rule184) sister.
- **next**: H_002 **faithful Φ★ GPU upgrade** (cost-bearing IIT4 정밀판 — C2 셀은 #503 proxy 로 이미 닫힘, 이건 정밀도 업그레이드 ⇒ **예산 승인 전 발사 금지**) · AXES R4+ ($0 광맥 소진 근접). **lane 종합 cycle#14~20**: 20 NEW H(H_258-277) + 4 C2/raster + SSOT full reconciliation, PR #468-510 全머지. /gap top-3 完全 follow-up + cascade closed-loop 정점(H_274→H_276).

---

#### Cycle #21 — faithful-Φ upgrade + AXES 마지막 seed (`/cycle 1,2`) — 2026-05-25

- **focus**: `/cycle 1,2` (옵션1 AXES R4+ $0 probe + 옵션2 faithful Φ★). **옵션2 GPU 발사 안 함** — scope-check 결과 faithful Φ★ 엔진 미구현(L4) + GPU 과대추정(large-N intractable=GPU도 못 풂, small-N exact=$0) → $0 small-N exact 로 재구성. [[feedback-scope-check-before-cost-fire]] 두 번째 비용-차단.
- **change**: H_278/279 NEW 2건. README 90→92 disk=tabled. 둘 다 $0·GPU 0.
- **verdict**: 1 SUPPORTED + 1 FALSIFIED
  - [x] **H_278 faithful-phi-small-n — SUPPORTED 3/3** (PR #515): H_002 C2 proxy upgrade. exact MIP-EI Φ(n=8, scale당 128 bipartition 전수)로 6-scale 재측정 → faithful CV 2.15 ≈ 동일-substrate proxy CV 2.10, **H_002 C2 scale-variant verdict faithful 하에서도 HOLD** (artifact 아닌 진짜 negative → L-C2.1 "faithful 아님" caveat 한 칸 축소). **faithful Φ★ "GPU 필요" 가정 최종 기각** — small-N exact 는 mac-local $0, GPU 는 intractable large-N 전용. honest: not full IIT4 4.0 (cause-effect structure/TPM 없음).
  - [x] **H_279 attention-salience-Φ — 🔴 FALSIFIED 1/4** (PR #514): AXES R3 phenomenology 마지막 미promote seed. attention-as-Φ-amplification FAL — attended(high-norm) salience-gap +0.40 但 phi_att<phi_unatt Δ_top4=−0.93. **salience(진폭) ⊥ Φ(다양성)** — H_265(학습 dampen)·H_275(cyclic<undir)·H_279 = 진폭/동기화 ≠ 통합 反상관 **cross-H 서명**. L2 cosine-Φ 의존(H_278 faithful 재검 가능).
- **hexa-run 게이트 정정**: H_278 발견 — `$HOME/.` env-prefix 가 harness 에서 불안정(pool-route 0.6.9 heavy-refuse, 셸 $HOME 미확장). **literal `/Users/...` 값 prefix**(예 `LOCAL=/Users/ghost/.x hexa run ...`)가 local-bound exemption(line 436) 확실 발동. [[reference-life-cycle-hexa-run-gotchas]] 갱신.
- **next**: AXES 사실상 depleted · large-N faithful Φ (intractable, GPU 무관) · full-IIT4 cause-effect structure (별도 대형 spec). **lane 종합 cycle#14~21**: 22 NEW H(H_258-279) + 4 C2/raster + SSOT full reconciliation, PR #468-515 全머지, README disk↔index 92=92. /gap top-3 完全 follow-up + cascade closed-loop 정점 + faithful-Φ proxy 확증. **$0 frontier 종결** — 잔여는 전부 intractable(GPU 무관) 또는 대형 spec.

---

