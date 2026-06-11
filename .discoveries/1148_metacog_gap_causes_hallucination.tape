@V := "tape" :: spec [active]
  version = "1.0"

@H 1148 := "metacog-gap CAUSES hallucination — the H_1142 input-familiarity blindness IS the fabrication mechanism (capstone/unifying)" :: discovery [PRE-REGISTERED deferred — depends on 1143+1146]
  seed       = "unify the two axes: H_1142 found input-familiarity metacog FAILS (F1 inverted). hypothesis: confident-fabrication events are EXACTLY the cases where input-familiarity-metacog is blind"
  metric     = "per-generation: (a) confidence C (-mean entropy), (b) fabrication = corpus-absent content-ngram fraction, (c) input-familiarity signal (H_1143 ood OR entropy). test: high-confidence + high-fabrication events concentrate in the LOW input-familiarity-detectability region"
  falsifier  = "confident-fabrication rate is >= 2x higher in the metacog-BLIND tercile than the metacog-AWARE tercile (the gap localizes hallucination); AND H_1143-signal, if it passed, SHRINKS this gap"
  control    = "shuffle the familiarity labels -> the 2x concentration must vanish (effect is the gap, not base rate)"
  verdict    = "SUPPORTED iff fabrication concentrates in the blind region >=2x; CLOSED-NEGATIVE iff fabrication is familiarity-independent (two phenomena are distinct, not one)"
  harness    = "UNIVERSE/h1148_metacog_gap_causes_hallucination.py (synthesizes H_1142+H_1143+H_1140 signals)"
  depends    = "run AFTER H_1143 (need its ood signal) and H_1146 (brake baseline)"
  xref       = "h1142-self-metacognition · 1143_hidden_ood_metacog · 1146_confidence_gated_brake · h1140-novelty-emergence · a_paper_negative_ok"
  target     = "🟢 SUPPORTED-NUMERICAL (unifies metacog+hallucination) or 🔴 CLOSED-NEGATIVE (distinct axes)"
