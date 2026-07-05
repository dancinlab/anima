#!/usr/bin/env python3
"""Cluster B - B7 anti-copy / G6 attention copy-bias probe (NOT-RUN this turn).

STATUS: NOT-RUN on mini. h1129.bin = 1.2GB ByteGPT303; loading on mini risks swap-OOM
(rc=137, memory: heavy-anima-eval-pool-not-mini). Single numpy MHA forward at seq~70
is feasible on a RAM-safe host (aiden/summer/pod). Script left for GPU/pool execution.

PREREG BAR (frozen, declared before any run):
  Load h1129.bin ONCE (ByteGPT303, G6 BASE ckpt). For one composed 2-concept ideation
  seed, run _bg_forward_build (captures per-layer K,V) and reconstruct the LAST-position
  attention weights per head over seed-token positions. Compute:
    - attention_mass on concept-A keyword span vs concept-B keyword span vs filler
    - copy-bias ratio = max(span_A, span_B) / (span_A + span_B + filler_nonseed)
  VERDICT:
    - if copy-bias ratio > 0.66 (one concept dominates) => trunk collapses to one
      concept => B6 (contrastive) / B7 (anti-copy) HIGHER-EV than B1 (set selection
      cannot recover what the trunk never bound).
    - if attention balanced across BOTH concept spans (each >= 0.2 of mass) => genuine
      trunk-level bind => B1 (set selection over K-pool) is the right lever, B7 is THIN.
  DEPENDS-ON: candidate ideation-seed texts (concept strings for spans a,b) - must be
  re-emitted from g6_ideation.hexa g6_build_frames (not in the stored .out files, which
  hold only scores). So this probe ALSO requires a re-decode of >=1 frame to recover the
  seed text -> effectively GPU-gated, not pure-$0.

MECHANISM vs H_6190:
  H_6190 already showed behaviorally (G1 CLM, grow-window) that novel-only = ECHO-ONLY
  (removing seed-keyword echo leaves cov_novel=1 = max_single, no genuine signal).
  B7 (decode-time anti-copy mask) on G1 is therefore RETREAD-adjacent to H_6190 echo-guard.
  This G6 attention probe is the mechanism-confirmation analog for G6 (ByteGPT, real MHA),
  where no attention-equivalent has been measured. SHUF control (fb 0.33 vs TARGETED 5.67)
  already proves topic-bind at SCORE level; attention would only localize it.
"""
# Implementation sketch (run on RAM-safe host):
#   import sys; sys.path.insert(0,'/Users/mini/dancinlab/anima/core')
#   import decode as D, numpy as np
#   W = D.bg_load('/Users/mini/anima-weights/bytegpt303_h1129/h1129.bin')
#   seed_ids = [b for b in seed_text.encode('utf-8','surrogateescape')]
#   logits, cache = D._bg_forward_build(W, seed_ids, len(seed_ids))  # K,V per layer
#   # reconstruct Q[last] from ln1(x[last]) @ inW -> attend against cache K -> softmax
#   # (re-use _bg_mha math for one head at a time, record weights instead of @V)
#   # => attention[last, :] per (layer, head); aggregate mass on span offsets.
print(__doc__)
