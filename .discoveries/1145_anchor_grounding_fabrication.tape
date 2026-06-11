@V := "tape" :: spec [active]
  version = "1.0"

@H 1145 := "anchor-grounding reduces fabrication — a real in-context anchor lowers the hallucination rate" :: discovery [🔴 CLOSED-NEGATIVE]
  seed       = "a_kosmos anchors carry real text into context (generator L3 slot). hypothesis: prepending a real corpus anchor GROUNDS generation, cutting corpus-absent fabrication vs no-anchor"
  metric     = "fabrication rate = corpus-absent content-ngram fraction (H_1140) over idea-questions, measured ANCHOR-ON (real corpus line prepended) vs ANCHOR-OFF (bare prompt), matched seeds"
  falsifier  = "fabrication(anchor-on) < fabrication(anchor-off) with Cohen's d >= 0.8 (grounding effect)"
  control    = "RANDOM-anchor (shuffled-word salad prepended) must NOT reduce fabrication like a real anchor (effect is grounding, not mere context-length)"
  verdict    = "SUPPORTED iff real-anchor cuts fabrication d>=0.8 AND > random-anchor; CLOSED-NEGATIVE iff no grounding effect"
  result     = "🔴 CLOSED-NEGATIVE — a real corpus anchor does NOT cut corpus-absent fabrication (Cohen's d real-vs-none = 0.0) and does not beat the random-anchor control (d = 0.0). NO grounding effect"
  finding    = "prepending a real corpus line (proxy for the kosmos_io->generator L3 anchor slot) does NOT ground generation at toy scale — the byte-LM ignores in-context anchor semantics for fabrication purposes; anchor-as-grounding is unverified here (would need a real anchor-conditioned trainer, not just prefix injection)"
  harness    = "UNIVERSE/h1145_anchor_grounding_fabrication.py · .verdicts/1145_anchor_grounding_fabrication/H_1145.txt"
  xref       = "a_kosmos · a_core_engine_map · h1140-novelty-emergence · 1148_metacog_gap_causes_hallucination · a_paper_negative_ok · p7"
