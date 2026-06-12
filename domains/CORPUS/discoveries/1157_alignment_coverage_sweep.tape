@V := "tape" :: spec [active]
  version = "1.0"

@H 1157 := "does MORE parallel coverage build a GENERALIZING interlingua bridge in a byte-LM (coverage sweep of the H_1156 alignment loss)?" :: discovery [🔴 CLOSED-NEGATIVE-COVERAGE-INDEPENDENT]
  seed       = "H_1156 🔴: 8-pair alignment MEMORIZES (train d=24.5) but held-out d=−0.06 (no bridge). user-picked path-(1) full-parallel realized as a $0 COVERAGE SWEEP: does held-out interlingua climb as K (aligned concepts) grows 0->8->27, or stay flat (coverage-independent siloing)?"
  F1         = "held-out interlingua d at K=27 >= 0.8 (coverage builds a general bridge)"
  F2         = "monotone climb d(K=27) - d(K=8) >= 0.5 (coverage HELPS)"
  control    = "K=0 no-alignment held-out d <= 0.3 (reproduce H_1155/1156)"
  verdict    = "SUPPORTED iff F1 & control (recipe = enough aligned pairs); CLOSED-NEG iff held-out ~0 at K=27 (coverage-independent — path-1 needs ~FULL translation coverage, not partial pairs)"
  honest     = "hand-curated 35-concept 5-lang lexicon (minor translation noise possible, e.g. ko homographs); toy d256/4L; sweep 0/8/27 only (a_scale_honest_scope)"
  result     = "🔴 CLOSED-NEGATIVE — FLAT curve: held-out d = K0 −0.194 / K8 −0.079 / K27 −0.116 (F1 fail, F2 climb −0.037 fail, control pass). 3.4x more aligned pairs gave ZERO held-out generalization"
  finding    = "byte-LM script-siloing is COVERAGE-INDEPENDENT at toy scale — partial pairwise alignment NEVER generalizes (8 or 27 pairs alike memorize-only, cf H_1156 train d=24.5 vs held-out ~0). path-(1) requires ~FULL translation coverage (= building a translation model), not partial pairs. INTERLINGUA ARC FULLY CLOSED: blend(H_1155) · capacity(H_1139) · surface/anisotropy(H_1155b/c) · pairwise-alignment(H_1156) · coverage(H_1157) ALL negative — 5/5 needs full-translation training OR per-language measurement (H_1129 recipe)"
  harness    = "UNIVERSE/h1157_alignment_coverage_sweep.py · .verdicts/1157_alignment_coverage_sweep/H_1157.txt"
  xref       = "h1156 (8-pair memorize) · h1155 (interlingua absent) · h1137/1139 (ru/ja ceiling) · h1129 · a_clm_gen_pipeline · a_scale_honest_scope · a_paper_negative_ok · p7"
  target     = "🟢 SUPPORTED-NUMERICAL (coverage builds bridge; recipe) or 🔴 CLOSED-NEGATIVE (coverage-independent siloing)"
