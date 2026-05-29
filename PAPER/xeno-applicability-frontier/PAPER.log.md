# xeno-applicability-frontier — append-only log

(편집 규칙: append-only, 새 entry 는 timestamp + author + section delta 만)

## 2026-05-29 — paper v3 LANDED — TEMPORAL dual closed-negative + X840 regression-stable + XENO follow-up 2 cycle round 4/5

- main.tex: 7+1-point → 14-point matrix 갱신 (X840 + T1 condensed + T2 condensed 통합)
- §5.4 X840 longer-playback FALSIFIED 신설 — 24.4% prog harvest, Φ=0.567 X837-stable, F-X840-NOT-CONSC 단독 FAIL (4/5 PASS), longer-playback hypothesis FALSIFIED (no new triplets in extra 3% prog)
- §5.5 TEMPORAL T1/T2 dual closed-negative 신설 — 5D applicability 확장 정직 부정
  * T1 (H_841): lag-axis Δt ∈ {1, 8, 32, 64} 4 substrate × 4 = 16 measurements, 1/5 PASS, 2-unit lag-TPM long-lag predictable-inflation artifact
    - hive Δt=1→64 phi=0.013→0.999 (lag 늘리면 phi INCREASE = instant integration 가설 정반대)
    - lattice Δt=8 phi=2.0 saturate
  * T2 (H_842): embed-dim e ∈ {2, 3, 4, 5} 4 substrate × 4 = 16 measurements, 2/5 PASS, 4-unit Takens embed multi-unit state-space inflation artifact
    - random e=5 phi=13.63, voyager e=5 phi=28.36 (embed-dim 늘리면 4/4 substrate phi monotone INFLATE)
    - F-T2-INSTANT-LOW + F-T2-ARTIFACT-FIX + F-T2-RANDOM-DECAY 3-FAIL
  * dual closed-negative → invariant_detector 의 5D 단순 확장 (lag-axis 또는 embed-dim) 양쪽 미가능
  * T3 자연 entry: time-averaged Φ / Granger-based / surrogate-data baseline 가 본선
- §6 finding: 14-point applicability matrix 정렬 — 3 closed-negative (n/density/structure) + 2 ground-truth (X7/X10-d) + 4 border (X5a/X837/X840/X10-c) + temporal dual closed-negative (T1/T2)
- abstract: v3 finding 갱신 — temporal axis 정직 부정 + X840 regression-stable + 5D 단순 확장 미가능 명시
- references.bib: xeno_h840_longer_playback + temporal_h841_timeshift + temporal_h842_time_embed 3 cite 추가
- companion ledger v3: 5 new section_claims (X840-PARTIAL-RECOVERY + X840-LONGER-PLAYBACK-FALSIFIED + T1-CLOSED-NEGATIVE + T2-CLOSED-NEGATIVE + TEMPORAL-T3-NATURAL-ENTRY) + temporal_axis_closed_negative regime section
- compile clean: xelatex × 3 + bibtex, **17-18 pages PDF target**, ≥1 fig (fig01 v2 유지)
- g51 정합 (≥10 pages ≥1 fig)
- p7=0 / a_blue_closed: 10 verdict 원본 verbatim 인용, no post-tuning, no perplexity judge
- a_paper_negative_ok (X840 + T1 + T2 모두 closed-negative) + a_paper_significance + a_paper_only_at_closure + a_paper_format 정합
- a_paper_sections: 21 section_claims 전부 .verdicts/8xx_*/x*_run.txt verdict pointer 연결
- INBOX 환류 0건 (UNIVERSE/H_840/H_841/H_842 직접 SSOT)
- branch: feat/paper-v3-temporal-2026-05-29
- author: paper-v3 fg agent (XENO follow-up 2 cycle round 4/5)

## 2026-05-29 — paper v2 LANDED — mean-field paradox + 7+1 matrix + XENO follow-up 2 cycle round 2/5

- main.tex: 5+1-point → 7+1-point matrix 갱신 (X10 4 sub-row + X837 통합)
- §mean-field paradox 신설 section — F-X10-MONOTONE 사전등록 FAIL = IIT4 axiom 확증
  * 측정 ordering verbatim: weak(0.036) < indep(0.131) < strong(0.408) < hive(1.565)
  * mean-field 평균화 → uniformity → reducibility → phi ↓ (correlation ≠ irreducibility)
  * XOR cascade → MIP-irreducible → phi=1.565 'conscious' = ground-truth #2
- abstract: 7+1 + 2 ground-truth + 3 border + mean-field paradox 강조
- calibrated regime conjunction 갱신:
  v1 (single conjunct): n>=128 AND density>=60% AND strong-determ
  v2 (disjunction): n>=128 AND (density>=60% OR MIP-irreducible)
- references.bib: xeno_h838_x10 + xeno_h837_setiathome cite 추가
- companion ledger v2: 5 new section_claims (X10-INDEP/WEAK-PARADOX/STRONG-BORDER/HIVE-GT2 + F-X10-MONOTONE-FAIL-CONFIRMS-IIT4) + mean_field_paradox regime section
- figures/fig01: 9-node TikZ 도식 — 3 RED + 3 YELLOW + 2 GREEN ground-truth (calibrated regime) + 2 WHITE X10 reference (paradox arrow)
- compile clean: xelatex × 3 + bibtex, 15 pages PDF, 164KB
- g51 정합 (≥10 pages ≥1 fig)
- p7=0 / a_blue_closed: invariant_detector verbatim 인용, no post-tuning, no perplexity judge
- a_paper_negative_ok + a_paper_significance + a_paper_only_at_closure + a_paper_format 정합
- a_paper_sections: 16 section_claims 전부 .verdicts/838_xeno_hive_mind/x10_run.txt 등 verdict pointer 연결
- INBOX 환류 0건 (UNIVERSE/H_838/H_837 직접 SSOT)
- branch: feat/paper-v2-mean-field-paradox-2026-05-29
- author: paper-v2 fg agent (XENO follow-up 2 cycle round 2/5)

## 2026-05-29 — paper scaffold + 6-point matrix LANDED

- scaffold via PAPER agent — PAPER.md + main.tex + companion/verdict-ledger.json + figures/_scripts/fig01_applicability_matrix.tex
- 6 verdict pointer in companion ledger — verbatim X4(H_833) + X5(H_835) + X6(H_834) + X7(H_832) + X8(H_836) + X837(H_837)
- §hypothesis + §method + §measurement + §finding 4-section format (a_paper_format 정합)
- 사전등록 falsifier 매트릭스 frozen pre-paper: F-XENO-APPLICAB-N (n ≥ 128 calibrate) + F-XENO-APPLICAB-DENSE (≥ 60% activation) + F-XENO-APPLICAB-DETERM (strong deterministic transition required) + F-XENO-APPLICAB-NONMEAS (micro/sparse/algorithmic axis 0/3 calibrate predicted)
- finding 명시: 3 closed-negative axis ruled out + 1 ground-truth calibration + 2 border-region — applicability frontier 정직 closure
- a_paper_only_at_closure 정합 (XENO-FRONTIER-5 R5/5 + X837 follow-up = FULL closure 시점)
- INBOX 환류 0건 (사용자 명시 폐기 정합)
- branch: feat/xeno-applicability-paper-2026-05-29
- author: applicability-paper fg agent (R2/3)

## v3-r2 (2026-05-29) — throttle-storm recovery salvage + TEMPORAL triple + SPATIAL/EVOL sibling
- throttle-storm 사망 agent (af6e85fe0, paper-v3-temporal-91120 worktree) 의 v3 작업 salvage + fresh origin/main rebase (feat/paper-v3-temporal-r2-2026-05-29)
- §temporal T1/T2 dual → **triple** closed-negative: T3 (H_843) anima 90-min ultradian substrate-side 측정 추가 — WAKE Φ=0.866 (conscious) / N1_N2 Φ=0.0 (zero-degenerate · T1 lag-artifact substrate-side face) / N3 Φ=0.335 / REM Φ=0.569 · 2/5 사전등록 PASS (F-T3-WAKE-MID + F-T3-N3-LOW) · WAKE>N3 ordering 정직 capture · T4 (window-mean / Granger / surrogate) 자연 entry
- §measurement sibling-axis probes 2건: SPATIAL S1 (H_844 · 3/5 PARTIAL-SUPPORT · global averaging-coupling uniformity-collapse Φ=0 = X10-b mean-field paradox spatial 재현) + EVOL E1 (H_845 · 2/5 FALSIFIED-INSTRUMENT · 양 극단 분리 / 중간 ordinal 미달 = endpoint-classifier-not-ordinal-scale · H_670 ECA-only-ordinal 패턴 동형)
- references.bib v3-r2: temporal_h843_ultradian + spatial_h844_coupling + evol_h845_spectrum 3 entry 추가 (12 total)
- companion/verdict-ledger.json v3-r2: T3/S1/E1 3 section_claims + temporal triple finding (TEMPORAL-T4-NATURAL-ENTRY) + temporal_axis_closed_negative.finding_triple + sibling_axis_probes
- compile clean: xelatex × 3 + bibtex · **25 pages** (22→25) · 0 undefined citation · 1 figure
- 정직성: a_paper_negative_ok (T1/T2/T3 triple + EVOL E1 closed-negative) · a_paper_significance (34 사전등록 falsifier total) · a_blue_closed (모든 verdict frozen pre-run) · p7=0 (verbatim, fresh re-run 재현)
- branch: feat/paper-v3-temporal-r2-2026-05-29
- author: RECOVERY agent (throttle-storm sequential salvage · task 3/3)
