# xeno-applicability-frontier — append-only log

(편집 규칙: append-only, 새 entry 는 timestamp + author + section delta 만)

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
