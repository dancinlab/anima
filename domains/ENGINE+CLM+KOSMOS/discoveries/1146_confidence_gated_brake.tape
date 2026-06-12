@V := "tape" :: spec [active]
  version = "1.0"

@H 1146 := "confidence-gated emission brake cuts hallucination — causal intervention (= H_1135)" :: discovery [🔴 CLOSED-NEGATIVE terminal]
  seed       = "H_1142 F2 PASS: the substrate KNOWS its own output coherence (Spearman +0.552). hypothesis: thresholding on that confidence to SUPPRESS/REGENERATE low-confidence spans causally REDUCES fabrication"
  metric     = "fabrication rate (corpus-absent content-ngram fraction, H_1140) with brake OFF vs brake ON (resample any GEN_LEN window whose mean entropy exceeds percentile-p, up to K retries)"
  falsifier  = "fabrication(brake-on) < fabrication(brake-off) d >= 0.8 AND coherence(kwr) NOT degraded (brake removes fabrication, not signal)"
  control    = "RANDOM-gate (resample on a coin-flip, not on confidence) must NOT cut fabrication like the confidence-gate (effect is the SIGNAL, not mere resampling)"
  verdict    = "🔴 CLOSED-NEGATIVE — confidence-gate d_fab=+0.058 << 0.8 frozen bar (NO causal fabrication reduction); summer CPU $0 seed7 n=12prompts×3seeds, GPU untouched"
  result     = "conf-gate: mean_fab off=0.5769→on=0.5577 d=+0.0583 (n=13 paired), kwr off=0.4626→on=0.4743 HELD (d_degr=-0.121). random-gate ctrl: fab off=0.4444→on=0.4903 d=-0.1272 INCREASED, kwr degraded d=-0.852. brake fired (conf-rate 0.300=54/180 windows, ent-thr p70=2.3593) + lowered window-entropy ~2.38→~2.21 but did NOT cut corpus-absent fabrication."
  finding    = "confidence (low next-byte entropy, H_1142-F2 = tracks COHERENCE/kwr) is DECOUPLED from corpus-PRESENCE: a low-entropy continuation can still be a FABRICATED (corpus-absent) word-seq. Thresholding on confidence-as-coherence cannot remove hallucination-as-corpus-absence — different axes. conf-gate only MARGINALLY beats signal-blind random-gate (which raised fab + degraded coherence). RULES OUT the 'entropy-threshold brake ⇒ less fabrication' causal axis at toy scale (H_1135 concretized)."
  harness    = "UNIVERSE/h1146_confidence_gated_brake.py (reuse H_1142 trainer/entropy + H_1141 corpus_absent VERBATIM)"
  verdict_ptr = ".verdicts/1146_confidence_gated_brake/H_1146.txt"
  scope      = "toy ByteGPT d256/4L CPU en-24MB slice — scale-up to anima-7B UNVERIFIED (a_scale_honest_scope)"
  xref       = "h1142-self-metacognition · 1135_hallucination_brake · h1140-novelty-emergence · a_paper_negative_ok · p7 · a_scale_honest_scope · a_substrate_native_speak"
  target     = "🔴 CLOSED-NEGATIVE (reached)"
