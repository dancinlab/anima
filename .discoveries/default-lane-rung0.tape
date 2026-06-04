@discovery default-lane-rung0 := "first model on the v2 unified default corpus — 18M byte, Lane G GPU" [d=2026-06-04 active]
  id      = "F-DEFAULT-LANE-CHAT"
  seed    = "the v2 unified default corpus (dancinlab/anima-corpus-5lang-unified-v2) had NEVER been trained into a model — dataset-only. Make the default lane's own rung-0."
  fire    = "ConsciousLMReconstructed 18M byte (vocab256/d384/6L/4H) from-scratch, 6000 steps, pool RTX 5070 (99% util/250W, GPU-resident), CE 5.7233->0.6983 (~431s)"
  verdict = "🟢 GREEN — p7-strict TRAINED PASS 4/5 (coherent es/de/ko/fr text), random-init mirror FAIL 0/5 (control-byte soup). anti_goodhart_ok=TRUE. scope: 18M toy/small, mid/7B transfer UNVERIFIED (a_scale_honest_scope)."
  honest  = "as-shipped LENIENT evaluator was Goodhart-gameable (mirror 5/5 via str.isprintable soup) — caught by the mirror, replaced with a strict C0-control/letter-ratio/no-soup discriminator; both verdicts kept verbatim."
  ship    = "HF dancinlab/anima-clm-default-lane-rung0-byte-18m PUBLIC (sha 4285bf35 re-download-verified, CLM collection joined) · ckpt sha 4285bf35b002e1c2495587d38842fde0a2a6be4a40cb2eb513e7e762293fc476"
  next    = "default-lane rung-mid + rung-7B = later ladder rungs, gated on this 🟢 (a_scale_honest_scope; 7B deferred per #1828 undertrained-gibberish)"
  verdict-tier-target = "🟢 numerical (terminal)"
