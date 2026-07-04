# H_9129 L5 hippocampal associative-store — 303M ENGINE-NATIVE rung(2) PRE-REGISTRATION

> Frozen bar written BEFORE running (p7 · c9 · a_no_tune_to_green). Item representations
> come from the REAL anima ByteGPT-303M h1129 (`~/anima-weights/bytegpt303_h1129/h1129.bin`)
> via the byte-exact `core/decode.py` engine forward (== `anima evaluate --py` engine ops,
> a_eval_py_canonical). The lane read-out (DG pattern-separation + CA3 heteroassociative
> pattern-completion) is a numpy SUBSTRATE operator laid ON TOP of engine representations —
> this is rung(2) "measure on real 303M representations", NOT yet rung(3) live `core/*.hexa`.

## What escalates vs STEP-0 (DIRECTIONAL)
STEP-0 used TOY iid-random sparse orthogonal codes → reach=1.0000 exact (handed advantage:
orthogonal codes make chaining trivial). Rung(2) replaces item codes with REAL 303M h1129
hidden representations of real corpus concept words. The DG sparse code is now a fixed
seeded random projection OF the 303M representation (kWTA) → semantically-related concepts
produce OVERLAPPING sparse codes → CA3 crosstalk is preserved. The open question: does the
dense/correlated 303M representation geometry DESTROY the transitive chaining (WALL) or does
reachable still lift >> unreachable with shuffle-collapse (BIND survives on real substrate)?

## Real corpus concept relation graph (held-out transitive inference, Dušek–Eichenbaum)
- Corpus = `archive/data/corpus.txt` (real anima dialogue corpus; English content lines).
- Nodes = top frequent English content words (stopword-filtered, alpha, len>=4).
- Edges = real line-level co-occurrence counts between content words (PMI-ranked).
- Chains = greedy disjoint walks on the co-occurrence graph → each ADJACENT link = a real
  strong corpus co-occurrence (the stored "premise"). Node sets are DISJOINT across chains.
- reachable pairs = WITHIN-chain NON-adjacent (gap>=2) → 2-hop+ transitive, never a stored
  premise edge, HELD-OUT.
- unreachable pairs = CROSS-chain, frequency/count-matched, no stored path, HELD-OUT.
- Both classes share the SAME surface form (real corpus words drawn from one freq band).

## Conditions
- FORM baseline = raw 303M-rep cosine (reports the representation-geometry confound directly).
- STORE = CA3 completion relatedness on the real relation graph.
- SHUFFLE ablation = permute the successor wiring (derangement), SAME nodes / SAME reps /
  SAME #edges → isolates RELATION lift beyond any form/geometry. **decisive BIND control.**
- LANE-OFF ablation = empty store (W=0) → relatedness must collapse to ~0 (causal check).

## FROZEN BAR (pre-registered — no post-hoc tuning)
- **GREEN** (BIND survives on real 303M substrate): store_gap = reach_mean − unreach_mean
  **> 0.50** AND shuffle_collapsed (shuf_gap < 0.5·store_gap) AND lane_off_collapsed
  (loff_gap < 0.05) AND representations are real-303M-engine.
- **WALL**: reps are real-303M but store_gap < 0.50 OR reach/unreach ratio < 1.5 — i.e. the
  lane COLLAPSES on the real substrate although the toy STEP-0 gave 7.88×. (a_break_the_wall)
- **RED**: floor (max store signal < 0.02, retrieves nothing) OR infra failure to extract reps.
- **fooled_by_form** = NOT shuffle_collapsed (lift persists under shuffle ⇒ it was
  form/geometry, not relation). handed-advantage flag: if reach_mean == 1.0000 exact ⇒
  suspect by-construction and report.

## Fixed hyperparameters (locked before run)
SEED=20260705 · N_CHAINS=8 · CHAIN_LEN=6 (N_ITEMS=48) · DIM=2048 · ACTIVE=40 · STEPS=6 ·
KWTA=40 · rep = mean-pooled pre-lnf final-layer 303M hidden (d=1024) of the word bytes.
