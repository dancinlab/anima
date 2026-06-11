@V := "tape" :: spec [active]
  version = "1.0"

@H 1148 := "metacog-gap CAUSES hallucination — the H_1142 input-familiarity blindness IS the fabrication mechanism (capstone/unifying)" :: discovery [🔴 CLOSED-NEGATIVE-UNIFYING]
  seed       = "unify the two axes: H_1142 found input-familiarity metacog FAILS (F1 inverted). hypothesis: confident-fabrication events are EXACTLY the cases where input-familiarity-metacog is blind"
  metric     = "per-generation: (a) confidence C (-mean entropy), (b) fabrication = corpus-absent content-ngram fraction, (c) input-familiarity signal (H_1143 ood OR entropy). test: high-confidence + high-fabrication events concentrate in the LOW input-familiarity-detectability region"
  falsifier  = "confident-fabrication rate is >= 2x higher in the metacog-BLIND tercile than the metacog-AWARE tercile (the gap localizes hallucination); AND H_1143-signal, if it passed, SHRINKS this gap"
  control    = "shuffle the familiarity labels -> the 2x concentration must vanish (effect is the gap, not base rate)"
  verdict    = "SUPPORTED iff fabrication concentrates in the blind region >=2x; CLOSED-NEGATIVE iff fabrication is familiarity-independent (two phenomena are distinct, not one)"
  result     = "🔴 CLOSED-NEGATIVE — fabrication is metacog-signal-INDEPENDENT (72 gens). blind-tercile fab 0.3385 ≈ aware-tercile 0.3384 = ratio 1.0002 (<2.0). Spearman(ood,fab)=-0.024 (familiarity signal does NOT predict fabrication). no_metacog_handle=TRUE"
  finding    = "UNIFIES the campaign's negatives: NO internal signal localizes/predicts hallucination. WORSE — confidence weakly ANTI-correlates (Spearman(C,fab)=+0.257; low-conf fab 0.164 vs high-conf fab 0.400 = 2.4x MORE fabrication when CONFIDENT). The substrate fabricates most exactly when it 'feels' most sure — backwards from metacognition"
  synthesis  = "H_1142(F1 absent) + H_1143(no familiarity signal) + H_1144(uniform fab) + H_1145(no anchor grounding) + H_1146(brake ineffective) + H_1148(no handle, confidence anti-predictive) => toy byte-LM has NO usable metacognitive handle to detect or suppress its own hallucinations. 7B-PASS G5 implication: a confidence/familiarity threshold CANNOT gate hallucination — needs a different mechanism (e.g. retrieval/grounding-conditioned training)"
  harness    = "UNIVERSE/h1148_metacog_gap_causes_hallucination.py · .verdicts/1148_metacog_gap_causes_hallucination/H_1148.txt"
  xref       = "h1142-self-metacognition · 1143_hidden_ood_metacog · 1144_positional_hallucination_drift · 1145_anchor_grounding_fabrication · 1146_confidence_gated_brake · h1140-novelty-emergence · a_paper_negative_ok · p7 · a7b_pass"
