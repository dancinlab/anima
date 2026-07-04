# H_9129 L5 rung-3 — PRE-REGISTERED frozen bar (before measurement; no post-hoc move · c9/p7)

**Goal:** cement gate-7 for the L5 hippocampal associative-store lane by (a) wiring DG-decorrelate
+ CA3 pattern-completion as a LIVE `core/` op, (b) proving disjointness (byte-exact generation
ON==OFF), and (c) the ★MANDATORY novel-chain-vs-stored-recall discriminator (MLC/H_1835 trap guard).

## Fixed hyperparameters (identical to rung-2 GREEN lens)
`seed=20260705 · preproc=center_zscore · N_CHAINS=8 · CHAIN_LEN=6 · DIM=2048 · ACTIVE=40 · STEPS=6 · KWTA=40`.
Reps = mean-pooled pre-lnf 303M hidden of the word bytes via `core/decode.py` (== `anima evaluate --py` ops).
Corpus concept co-occurrence graph = `archive/data/corpus.txt`; premises stored = adjacent (gap=1) edges ONLY.

## Frozen decision bar (set BEFORE running)
GREEN-cement iff ALL of:
1. **novel-chain lift**: `store_gap = novel_chain − unreach > 0.50`.
2. **shuffle collapse**: `shuf_gap < 0.5 · store_gap` (derangement of wiring, same reps/edges).
3. **lane-off collapse**: empty store W=0 → novel < 0.05.
4. **★ novel-vs-recall discriminator PASS** (all three):
   - RECALL positive control (gap=1 directly-stored edges) completes (> 0.50).
   - NOVEL-CHAIN (gap≥2, NEVER stored) lifts (store_gap > 0.50) — a novel 2-edge+ chain, not a stored pair.
   - **LESION isolation**: knock out one mid-chain edge (pos2→pos3) per chain. Novel pairs whose
     transitive path CROSSES the lesion (`path_broken`) MUST collapse (drop > 0.50, residual < 0.50)
     while pairs on one side (`path_intact`) MUST survive (> 0.50, drop < 0.20). Lesion location can
     only matter if completion walks the actual stored path ⇒ isolates genuine chaining from recall/form.
5. **disjoint / ON==OFF**: the live `core/` lane op is ADDITIVE-ONLY (no mutation of any emit-consumed
   surface) ⇒ generation byte-identical lane-ON == lane-OFF; hexa op byte-parity with the numpy twin.
6. **engine-native**: reps via `core/decode.py` == `anima evaluate --py` (a_eval_py_canonical, TERMINAL-eligible).

FAIL (🧱/🔴) iff the lift collapses on the live op, OR the discriminator is recall-only /
lesion-insensitive (lift present but `path_broken` does not collapse) — then rung-2 GREEN stays
measurement-only and rung-3 does not cement.

## Honesty scope carried in (a_scale_honest_scope)
The store is an EXPLICIT heteroassociative store handed the true corpus edges; its transitive closure
is guaranteed by construction. A PASS cements a genuine DISJOINT associative-completion FACULTY
(anima previously had only flat-cosine `retrieve`), NOT a claim that the 303M trunk/mouth recombines.
That boundary is reported regardless of tier and is not a post-hoc bar move.
