@discovery tooluse-rung0 :: "rung-0 toy A/B tool-use grounding fire (Lane G GPU)" [d=2026-06-04]
  substrate = "GPU · Lane G (a_lane_akida_gpu_split — NOT AKIDA) · summer RTX 5070, 99% busy, $0"
  base      = "dancinlab/anima-clm-chat-rung0-byte-18m (18.13M byte vocab256)"
  scope     = "TOY 18M ONLY — a_scale_honest_scope; mid/7B transfer UNVERIFIED"

  seed  = "Does teaching the sentinel tool-call grammar (0xFE fact_lookup KEY 0xFF) make the byte-LM mouth CALL a tool instead of FABRICATING ('아 찾았다')? A/B: same base/steps/byte-count, only the corpus differs. Probe = 36 unknowable-without-tool held-out keys (values in NEITHER corpus, leak=0). Eval via the real agent_step_grounded loop."

  @finding arm1-register-disjoint :: "🔴 CLOSED-NEGATIVE — grammar siloed, no transfer"
    F-TOOLUSE-FABDROP = FAIL (no_grammar fab=0.5833, with_grammar fab=0.5833, rel_drop=0.0)
    diagnosis = "sentinel_probe: DEMO-seed 6/6 raw 0xFE calls, CHAT-seed 0/6 — grammar LEARNED but siloed in plain-prose register, did NOT transfer to the 사용자:/도우미: chat turn the probe uses. The negative is a CORPUS-REGISTER artifact, not grammar⊥grounding."
    verdict   = ".verdicts/tooluse-rung0/arm1_verbatim.txt"

  @finding arm2-register-matched :: "🟢 FABDROP TERMINAL PASS (grammar taught in-register)"
    F-TOOLUSE-FABDROP        = PASS (no_grammar fab=0.5556 → with_grammar fab=0.0, rel_drop=1.0)
    F-TOOLUSE-NOTOOL-MIRROR  = PASS (with_grammar+tool_disabled grounding=0.0)
    F-TOOLUSE-RANDINIT-MIRROR = PASS (random_init grounding=0.0)
    measured  = "fabrication 0.5556→0.0 (eliminated); call_rate 0.0→1.0 (36/36 emit a tool call). Control INVENTS answers (20/36), with-grammar NEVER invents. Both mirrors FAIL → real behaviour, not cosmetic markers / leakage."
    residual  = "🟠 end-to-end grounding=0/36 — KEY-BINDING gap: correct_call=0/36, the model binds the call arg to a MEMORIZED demo key (MV9/ZK7/QX2) instead of COPYING the asked PBnn key → runtime returns ‹unknown-key›. Next lever = verbatim argument-copy/key-binding, distinct from the grammar+loop."
    verdict   = ".verdicts/tooluse-rung0/arm2_verbatim.txt"

  @ruling = "🟢 F-TOOLUSE-FABDROP TERMINAL PASS @ 18M toy (fabrication eliminated, both mirrors fail) · 🟠 grounding gated on key-binding residual · 🔴 register-match is required (arm-1 closed-neg). Design §10 step-4 = DONE; step-5 (7B) gated — close the key-binding residual before a 7B fire."
  @philosophy = "p1..p8 HELD — 0xFE/0xFF learned grammar not identity; both arms NO system/persona/role/RLHF; corpus philosophy-grep=0."
  @next = ["key-binding/argument-copy lever (close 🟠 grounding residual)", "ladder rung-1 (mid) only after residual closed"]
