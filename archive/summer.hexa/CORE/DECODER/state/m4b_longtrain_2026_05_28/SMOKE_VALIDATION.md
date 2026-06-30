# M4b longtrain — local smoke validation (2026-05-28)

Pre-fire validation of `train_v3_moe_longtrain.hexa` on Mac (CPU, install runtime,
20-line corpus subset, M4B_EPOCHS auto-scaled). Confirms the trainer is correct
before the cost-bearing GPU fire (a_completeness_over_cheap — no firing a broken pipeline).

## PASS — all 3 unblockers + the leak fix validated

1. **BPE O(1) (hexa-lang #1869)**: `loaded 151387 merges, 151643 vocab in 918.579 ms`
   then `bpe: V=151643 n_toks=9062`. The full Qwen BPE tokenize is now sub-second —
   the old O(N_merges) encoder stalled 5+ min even on a 24-line trim (BPE_TOKENIZE_BOTTLENECK.md).
   FRESH-CHECKOUT stdlib (`HEXA_STDLIB_ROOT=/tmp/hexa-fresh`) at transpile time.
2. **fs_mkdir_p**: replaces `dir_create` (cross-backend codegen gap + install no-op stub).
   Fresh runtime `rt_fs_mkdir_p` is a real recursive mkdir.
3. **Budget auto-scaling**: 20-line corpus (9062 toks) → `epochs=332 n_steps=751648
   token_presentations=3,006,592 = 19× V`. Targets ~3M presentations (≫ V=151643)
   regardless of corpus size — the dec_undertrain lever.
4. **mm-leak fix**: per-step backward buffers (d_zT_last_pre, Q_l..h_act_seq_l) HOISTED
   out of the step loop (compile-verified: 0 per-step t_zeros for these). 3-min smoke ran
   with no OOM. (rev2 re-t_zeros'd them every step → host-RSS leak that OOM-killed #1315.)

## baseline reproduced
`step=1 L_ce=648.526` — exactly matches #1315 pod C step-1 CE (apples-to-apples;
same init, same V, same d=64). Confirms the trainer is the same model as the
ruled-out fires, differing ONLY in the budget lever.

CPU is far too slow for 751648 steps (smoke timed out at step 1 after printing it);
the GPU H100 fire does the full run. Loop logic + budget math + leak fix are sound.
