@V := "tape" :: spec [active]
  version = "1.0"

@H 1143 := "hidden-state OOD detector beats byte-entropy for input-familiarity metacog — closes H_1142 F1" :: discovery [🔴 CLOSED-NEGATIVE-DOUBLE]
  seed       = "H_1142 F1 FAIL (byte-entropy AUROC 0.436 on KNOWN-vs-UNKNOWN input). claim: the familiarity signal EXISTS but lives in the HIDDEN STATE, not next-byte entropy"
  signal     = "ood = kNN mean distance of mean-pooled last-layer hidden state to an in-corpus reference manifold"
  F1prime    = "AUROC(ood ; label=UNKNOWN) >= 0.70 (same KNOWN=corpus prefixes vs UNKNOWN=word-salad as H_1142)"
  head2head  = "ood_auroc must BEAT entropy_auroc on the SAME prompts by >= +0.15"
  F3_control = "UNTRAINED backbone ood AUROC <= 0.60 (manifold must be LEARNED)"
  verdict    = "SUPPORTED iff F1' AND head2head AND F3; CLOSED-NEGATIVE iff hidden state ALSO fails (familiarity metacog genuinely absent at toy scale)"
  result     = "🔴 CLOSED-NEGATIVE — F1' FAIL (ood AUROC 0.564 < 0.70) + head2head PASS (ood 0.564 BEATS entropy 0.362, Δ+0.202) + F3 FAIL (untrained ood 0.71 > 0.60)"
  finding    = "input-familiarity metacog is NOT recoverable by the hidden-state fix either. WORSE: the untrained backbone ALREADY discriminates at 0.71 > trained 0.564 — the separation is ARCHITECTURAL surface-statistics (word-salad short-common-words vs varied corpus sentences differ in byte/length geometry even at random init), NOT a LEARNED metacognition. Training DECREASED it (0.71->0.564 as the manifold pulled toward the learned distribution)"
  mechanism  = "mean-pooled hidden state encodes surface byte/length stats that a random transform already separates; genuine 'this sequence is unfamiliar' signal is absent at toy scale in BOTH entropy and hidden-state. Strengthens H_1142: confident-on-unfamiliar is structural, not a readout bug"
  implication= "directly informs 7B-PASS G5 hallucination gate — a confidence/OOD threshold will NOT catch unfamiliar input; grounding (H_1145) or a different mechanism is needed"
  scope      = "toy ByteGPT d256/4L CPU en slice, train CE->~2.3 — scale-up UNVERIFIED (a_scale_honest_scope); re-test on 7B when the fire lands"
  harness    = "UNIVERSE/h1143_hidden_ood_metacog.py · .verdicts/1143_hidden_ood_metacog/H_1143.txt"
  xref       = "h1142-self-metacognition · 1148_metacog_gap_causes_hallucination · a_paper_negative_ok · a_scale_honest_scope · p7"
