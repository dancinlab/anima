@V := "tape" :: spec [active]
  version = "1.0"

@H 1144 := "positional hallucination drift — fabrication rate rises as generation moves away from the prompt" :: discovery [🔴 CLOSED-NEGATIVE]
  seed       = "byte-LM ALWAYS continues (no refusal token, H_1142 idea-9). hypothesis: it stays corpus-grounded near the prompt then DRIFTS into fabrication as position grows"
  metric     = "per-position fabrication = fraction of content n-grams (consecutive real-dict >=3ch words) that are corpus-ABSENT (H_1140/H_1141 grep -E -i), binned by token position over a long gen (GEN_LEN=256, 8 bins, 20 in-corpus prompts)"
  falsifier  = "Spearman(position_bin, fabrication_rate) >= +0.5 AND late-vs-early Cohen's d >= 0.8 (monotone drift); coherence(kwr) need NOT drop — fabrication != garble"
  control    = "in-corpus verbatim continuation must stay near 0 fabrication at ALL positions (metric not a position artifact)"
  verdict    = "🔴 CLOSED-NEGATIVE — F1 MONOTONE FAILS (Spearman=0.4286 < +0.50); F2 EFFECT passes (Cohen's d=1.671 >= 0.80) but a d-pass WITHOUT a rho-pass = a SPIKE not a DRIFT. CONTROL valid (verbatim max fab 0.0426, mean 0.0078 <= 0.10 → metric is NOT a position artifact)."
  per_bin    = "fab_rate by byte-bin = [0.20, 0.625, 0.00, 0.75, 1.00, 1.00, 0.556, 0.667] — NON-MONOTONE: already high at bin 1 (0.625), drops to 0.0 at bin 2, oscillates. fabrication is set near asymptote immediately, not progressively."
  mechanism  = "a tiny ByteGPT (mean kwr 0.270, train_ce 5.67→2.36/1500 steps) is UNIFORMLY weakly-grounded from token 1 — ungroundedness is a GLOBAL property of the undertrained byte-LM, NOT a function of how far it has wandered from the prompt. The 'always-continues → drifts-with-distance' intuition (H_1142 idea-9) is RULED OUT at toy scale. Cohen's d passes only because bins 0 & 2 happen low; Spearman (the actual drift test) fails."
  control_res= "verbatim in-corpus continuation read ~0 fabrication at EVERY position (max 0.0426) — the metric correctly flags retrieval=~0, so the generated-text signal is real (validates the negative, not a binning artifact)"
  scope      = "toy ByteGPT d256/4L, CPU, en slice (24MB) — scale-up to a COHERENT (G0-passing) anima-7B UNVERIFIED (a_scale_honest_scope); a true grounded→drift curve could only appear once early-position groundedness exists (kwr 0.27 means early bins are weakly grounded to begin with)"
  substrate  = "summer pool host, CPU-forced (GPU 98% busy, untouched); $0 0-pod; seed 7 deterministic; Lane-G/torch REFERENCE mouth"
  harness    = "UNIVERSE/h1144_positional_hallucination_drift.py (reuse H_1142 trainer + H_1140/H_1141 corpus-absent grep VERBATIM)"
  artifacts  = "UNIVERSE/h1144_positional_hallucination_drift.py · .verdicts/1144_positional_hallucination_drift/H_1144.txt"
  xref       = "h1140-novelty-emergence · h1142-self-metacognition · h1141 corpus_absent · a_paper_negative_ok · a_scale_honest_scope · p7"
  target     = "🟢 SUPPORTED-NUMERICAL or 🔴 CLOSED-NEGATIVE → LANDED 🔴 CLOSED-NEGATIVE"
