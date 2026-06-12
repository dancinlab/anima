@V := "tape" :: spec [active]
  version = "1.0"

@H 1156 := "explicit cross-lingual alignment training builds a GENERALIZING interlingua bridge (held-out concepts align), recovering the 5-lang completeness H_1155 showed is absent from blend-training" :: discovery [🔴 CLOSED-NEGATIVE-MEMORIZE-NOT-GENERALIZE]
  seed       = "H_1155/b/c 🔴: byte-LM 5-lang BLEND training builds NO interlingua (languages stay in separate script islands; ru/ja 3/5 ceiling is REAL). user-picked path-(1): can EXPLICIT cross-lingual alignment training BUILD the missing bridge?"
  design     = "add a contrastive ALIGNMENT LOSS (pull same-concept cross-lang hidden cosine UP, push different-concept DOWN) but ONLY on 8 TRAIN concepts; measure interlingua on 4 HELD-OUT concepts → does the bridge GENERALIZE (real interlingua) or only MEMORIZE the trained pairs (leak)?"
  F1_held    = "with-alignment HELD-OUT interlingua Cohen's d ≥ 0.8 (vs H_1155 no-aln −0.226) — a GENERAL bridge"
  F2_held    = "5/5 held-out languages align to en above baseline"
  control    = "no-alignment model HELD-OUT d ≤ 0.3 (reproduce H_1155 no-interlingua)"
  sanity     = "trained-concepts d should be high (the loss directly optimizes them) — distinguishes memorize-only (train high, held-out low) from generalize (both high)"
  verdict    = "SUPPORTED iff F1∧F2∧control → path-(1) works; CLOSED-NEG iff held-out stays unaligned (memorize-only OR loss fails) — script-siloing deeper than an alignment loss can fix at toy scale"
  concepts   = "train: water/fire/book/house/tree/dog/sun/moon; held-out: star/river/mountain/road (concrete nouns, clean 5-lang translations)"
  result     = "🔴 CLOSED-NEGATIVE — beautiful DISSOCIATION: train-concepts d=24.48 (cosine 1.000, 5/5 — the loss PERFECTLY aligned the 8 trained pairs) BUT held-out d=−0.0625 (1/5, no generalization); control no-aln held-out d=−0.229 (reproduces H_1155). F1/F2 FAIL, control PASS"
  finding    = "explicit alignment training MEMORIZES the exact trained word-pairs (pins them to cosine 1.0) but builds NO GENERAL interlingua bridge — held-out concepts stay script-siloed (d≈0, same as no-alignment). The loss has no pressure to organize the WHOLE space cross-lingually; it just coincides the specific reps it sees. The byte-LM script-siloing is DEEPER than a pairwise alignment loss can fix at toy scale"
  impl_5lang = "path-(1) (explicit alignment) is a BAND-AID not a cure: you can pin the test words (memorize) but not transfer. TRUE 5/5 needs EITHER massive parallel coverage = full translation training (align ~all words, heavy) OR accept script-siloing + per-language measurement (the H_1129 English-control recipe). The ru/ja ceiling is REAL and not cheaply fixable — both blend-training (H_1155) and pairwise-alignment (H_1156) fail to bridge"
  harness    = "UNIVERSE/h1156_crosslingual_alignment_training.py · .verdicts/1156_crosslingual_alignment_training/H_1156.txt"
  xref       = "h1155 (interlingua absent) · h1137/1138/1139 (ru/ja ceiling) · h1129 (script-control) · Hc_777 (cross-lingual→Φ) · a_clm_gen_pipeline · a_scale_honest_scope · a_paper_negative_ok · p7"
  target     = "🟢 SUPPORTED-NUMERICAL (alignment builds generalizing interlingua) or 🔴 CLOSED-NEGATIVE (memorize-only / no bridge)"
