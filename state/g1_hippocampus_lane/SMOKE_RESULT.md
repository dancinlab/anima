# hippo_retrieve_smoke.hexa — engine-native TOY harness run
# date: 2026-07-03 · hexa v0.574.1 · host: mini (mini-safe, no decode) · exit 0
# reproduce: hexa run core/hippo_retrieve_smoke.hexa
# SCOPE: harness-validation (anti-artifact controls fire). NOT a 303M verdict.

==============================================================================
HIPPOCAMPAL HETERO-ASSOCIATIVE retrieve-into-context — ENGINE-NATIVE smoke
  slug g1_hippocampus_lane · TOY harness-validation (NOT frozen 303M bar)
  live ops: core/hippo_retrieve.hexa (conjunction-key recall, kosmos cosine)
==============================================================================
(A) cue (ocean, engine) -> hetero recall:
      recalled associate D = 'harvest'   (GOLD = 'harvest')
      D is OFF-SEED (not ocean/engine) AND off-midpoint (arbitrary bind).
      key = per-channel CONJUNCTION sqrt(a*b)  (NOT the arithmetic mean = kosmos_merge).
      recall via kosmos_io retrieve cosine — NOT immune_memory_recall (recall_thr untouched).

(B) echo-guard NOVEL-ONLY discriminator (composed_novel > max_single=0):
  ARM-BIND         novel_only=4/4 leak=0 (bar>=2) => PASS
  ARM-ECHO         novel_only=0/4 leak=0 (bar>=2) => FAIL
  SINGLE-PARENT    novel_only=0/4 leak=0 (bar>=2) => FAIL
  SCRAMBLE         novel_only=0/4 leak=0 (bar>=2) => FAIL
------------------------------------------------------------------------------
  HARNESS-VALID (bind PASS ∧ echo FAIL ∧ scramble FAIL ∧ leak=0): true
  VERDICT: ENGINE-NATIVE (live hippo_retrieve ops) — GREEN still needs the real
           303M mouth on pool: does it BIND injected D vs echo the seed?
           (anima evaluate --py <clm>; mini=OOM, decode banned here.)
==============================================================================
