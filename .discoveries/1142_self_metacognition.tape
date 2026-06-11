@V := "tape" :: spec [active]
  version = "1.0"

@H 1142 := "self-metacognition / confidence-calibration — does the substrate know what it knows?" :: discovery [🔴 CLOSED-NEGATIVE-DISSOCIATION]
  seed       = "fills the gap: OTHER-MIND=theory-of-OTHER-mind, CSP=self-prediction, imagine=self-simulation — NONE measure whether anima knows its OWN uncertainty"
  signal     = "C = -(mean next-byte entropy over generated continuation); high C = confident"
  p7_guard   = "entropy is the OBJECT measured, NOT the verdict; verdict = its calibration vs INDEPENDENT ground-truth (corpus-membership + dict-coherence)"
  F1_disc    = "AUROC(uncertainty=-C ; label=UNKNOWN) >= 0.70 — KNOWN=in-corpus prefixes vs UNKNOWN=real-word salad (corpus-absent sequence, same byte stats)"
  F2_calib   = "Spearman(C, known_word_ratio of own output) >= +0.30 — confident <=> coherent"
  F3_control = "UNTRAINED backbone AUROC <= 0.60 — metacognition must be LEARNED not architectural (anti-Goodhart)"
  verdict    = "SUPPORTED iff F1 AND F2 AND F3; CLOSED-NEGATIVE (a_paper_negative_ok) iff trained fails F1 or F2"
  result     = "🔴 CLOSED-NEGATIVE — F1 FAIL (AUROC 0.436, BELOW chance, INVERTED) + F2 PASS (Spearman +0.552) + F3 PASS (untrained AUROC 0.522, rho 0.126)"
  finding    = "DISSOCIATION: toy substrate HAS output-coherence metacognition (F2 learned — knows when its OWN output is garble) but LACKS input-familiarity metacognition (F1 inverted — feels MORE confident on common-word salad than real corpus). mean_ent: known 2.227 > unknown 2.192"
  mechanism  = "next-byte entropy tracks LOCAL token-predictability (frequent dict words = low entropy = false confidence), NOT global sequence-novelty — so 'knows-what-it-knows' on INPUT fails while output-monitoring succeeds"
  scope      = "toy ByteGPT d256/4L, CPU, en slice, train CE 5.71->2.33, 2.2min — scale-up to anima-7B UNVERIFIED (a_scale_honest_scope)"
  harness    = "UNIVERSE/h1142_self_metacognition.py · .verdicts/1142_self_metacognition/H_1142.txt"
  xref       = "other-mind · csp-h1064-h1065 · imagine-h1021-1041 · a_paper_negative_ok · a_scale_honest_scope · p7 · 7b-pass-G5-hallucination"
