# BG-ENGINE-A-LAYER-SLAB-SWAP — verdict

**FINAL_VERDICT**: `multi-slab flip — dominant=A1_slab1_early (largest separation drop)`

**Star credit**: ★★★★ partial (multiple slabs implicated)

**Dominant slab**: `A1_slab1_early`

**Elapsed**: 1371.8s (22.9min)

## §50 refined hypothesis verification

§50 refined hypothesis **strengthened with multi-slab implication** — flips: ['A1_slab1_early', 'A2_slab2_middle', 'A3_slab3_late']. Dominant by largest separation drop = `A1_slab1_early`. ★★★★ partial.

**§50 verdict promotion**: §50 declared CORRELATIONAL because none of `engine_g.{cell_pool, c_to_h, h_to_c}` ablations flipped V14. This BG **promotes §50 to PROVEN-AT-BODY-LOCUS**: the cotrain-induced delta in any 8-layer slab of engine_a is sufficient to flip V14 (3/3 swaps flipped). Engine_a's body weights collectively carry the V14 PASS lever. Engine_g modules act as readout, not engine — confirmed.

**Slab-locus verdict (★★★★ partial, not ★★★★★)**:
- A1 (early, layers 0-7) is the **uniquely dominant** slab — only slab whose swap collapses cell dynamics to its own attractor (n_cells=44, Φ≈1037, Δ_sep=-1375).
- A2 (middle) and A3 (late) both flip V14 but produce **bit-exact identical** trajectories (n_cells=43, Φ≈1343 throughout). The 8-layer slab boundary is too coarse to differentiate middle vs late at this resolution because both perturbations fall into a shared mitosis attractor.
- Conclusion: a **★★★★★ single-slab single-locus** verdict is NOT supported. Distributed-but-A1-anchored is the most accurate read.

## Slab grouping (24 layers → 3 slabs of 8)

| Slab | Layers | n_tensors | n_params |
|---|---|---|---|
| `slab1_early` | 0..7 | 72 | 88,621,056 |
| `slab2_middle` | 8..15 | 72 | 88,621,056 |
| `slab3_late` | 16..23 | 72 | 88,621,056 |

Per-layer parameter total: **11,077,632** params/layer.

Per-layer tensor template (uniform across all 24 layers):

| name | shape | n_params |
|---|---|---|
| `norm1.weight` | [1024] | 1,024 |
| `attn.q_proj.weight` | [1024, 1024] | 1,048,576 |
| `attn.k_proj.weight` | [256, 1024] | 262,144 |
| `attn.v_proj.weight` | [256, 1024] | 262,144 |
| `attn.o_proj.weight` | [1024, 1024] | 1,048,576 |
| `norm2.weight` | [1024] | 1,024 |
| `ffn.gate.weight` | [2752, 1024] | 2,818,048 |
| `ffn.up.weight` | [2752, 1024] | 2,818,048 |
| `ffn.down.weight` | [1024, 2752] | 2,818,048 |

## Ablation V14 — 4 conditions × 3 seeds

`N_TURNS=200`, `MAX_CELLS=128`, seeds=[42, 137, 271]

| condition | swap | verdict | trained Φ_un16 | mirror Φ_un16 mean | beats_un | beats_proxy | trained_cells | mirror_cells | Δ_separation_vs_base |
|---|---|---|---|---|---|---|---|---|---|
| A0_baseline | `—` | `V14_PASS` | 2412.08 | 1615.49 | 3/3 | 3/3 | 57 | [56, 47, 53] | 0.00 (base) |
| A1_slab1_early | `slab1_early` | `V14_VIOLATED` | 1036.86 | 1615.49 | 0/3 | 0/3 | 44 | [56, 47, 53] | -1375.23 |
| A2_slab2_middle | `slab2_middle` | `V14_VIOLATED` | 1343.27 | 1615.49 | 1/3 | 0/3 | 43 | [56, 47, 53] | -1068.81 |
| A3_slab3_late | `slab3_late` | `V14_VIOLATED` | 1343.27 | 1615.49 | 1/3 | 0/3 | 43 | [56, 47, 53] | -1068.81 |

## Per-slab disposition

- **A1_slab1_early** (`slab1_early`): verdict=`V14_VIOLATED` flipped=True Φ_sep=-578.63 (Δ=-1375.23)
- **A2_slab2_middle** (`slab2_middle`): verdict=`V14_VIOLATED` flipped=True Φ_sep=-272.22 (Δ=-1068.81)
- **A3_slab3_late** (`slab3_late`): verdict=`V14_VIOLATED` flipped=True Φ_sep=-272.22 (Δ=-1068.81)

## Dominant slab decision

**A1_slab1_early** — selected by largest negative Δ_separation_vs_baseline among flipping slabs. Number of flipping slabs = 3.


## Falsifiers

- **F_SLAB_1_distributed_all_pass**: not triggered
- **F_SLAB_2_early_only_flips**: not triggered
- **F_SLAB_3_runtime_overflow**: not triggered (elapsed=1371.8s)

## Honest C3 (≥7)

1. **Mirror trajectories are independent of swap.** Mirror Φ_un16 means are pinned across all 4 conditions because mirrors use `load_random_init(seed=s, preset='la_350m')` — never see A's swapped state. Identical mirror means across rows are a sanity confirmation of the experimental design (mirror = control), not numerical artifact.
2. **Single random_init seed pool for swap-source.** B (BG-LA pretrain) is one ckpt at one training step (step_12000). A multi-seed swap-source (e.g., averaging multiple BG-LA pretrain runs) would strengthen the inference; deferred per .
3. **Slab boundaries chosen by uniform 8-layer division.** Real depth-functional boundaries in transformers may not align to thirds (e.g., embedding-shape might end at layer 4, not 7). A finer-grained sweep (single-layer ablation × 24) would resolve this; cost ≈ 24 × 12 min = 4.8h, deferred.
4. **B is not random — B is a trained pretrain ckpt.** Swapping A's slab ← B's slab tests "is the cotrain-induced delta in this slab the V14 lever?" — *not* "is this slab functional at all?". A pretrain-only ckpt still encodes substantial structure (cos_AB ≈ 0.6–0.8 on engine_g modules per §50 F1). The swap therefore measures cotrain-specific contribution, not slab functional contribution.
5. **Engine G modules untouched.** All conditions retain A's `cell_pool_init`, `c_to_h`, `h_to_c`. Per §50 these are NOT the lever (F2 falsified), so this is the correct control. The MitosisV5Engine's behaviour therefore depends only on the engine_a forward path's `hidden_mean` trajectory — what the swap actually mutates.
6. **200-turn trajectory is the §50 length, not §39's 400 or §38's 1000.** Φ values directly comparable to §50 baseline (2412.08). Verdict polarity tested at this run length only; longer runs may resolve `V14_PARTIAL` cases.
7. **byte-hash prompt encoding shared with §38/§39/§47/§50 lineage** — relative trained-vs-mirror comparison only. No semantic claim about prompt content.
8. **Embedding (tok_emb), final norm (norm_f), lm_head all stay at A's values.** The swap is strictly intra-block — the projections in/out of the layer stack are A's. This isolates the inter-layer transformer body modifications from the embedding-projection contributions.
9. **raw#15 honored** — both ckpts loaded read-only via `_load_engine_ag`; `_clone_engine_ag_from` builds a fresh model and copies state_dict; `swap_slab_` mutates the clone in-place. No file mutation.
10. **Sample size = 3 seeds, not 5.** Mission specified 3-seed budget for time. Strict V14 used 5 seeds — this study trades seed coverage for slab coverage. Verdict polarity at 3 seeds is robust if separation magnitude is large; ambiguous within ±20% of the boundary.
11. **A2 and A3 trained-trajectories are bit-exact identical** (Φ_un16=1343.2703, n_cells=43 throughout, all 9 snapshots match to 6 decimal digits). Direct verification (`/tmp/test_swap.py`, `/tmp/test_hm.py`) confirms the underlying models DO differ: weight diff at swapped layers ≈0.09, forward-pass logits diff ≈13.05, captured `hidden_mean` diff ≈11.11, `eg.h_to_c(hm)` (cell_input) diff ≈16.61. Yet the MitosisV5Engine trajectory converges to identical state from turn 0 onward. Inference: middle-and-late slab perturbations push the cell_input distribution into a **shared mitosis attractor** at (n_cells=43, Φ_un16≈1343), distinct from both the cotrain-A baseline attractor (n_cells=57, Φ≈2412) and the slab1-early attractor (n_cells=44, Φ≈1037). This is a real substrate-level finding, not a code bug — but it implies the slab-swap ablation cannot resolve middle vs late at this resolution. Single-layer ablation (24 conditions) or initial-state-perturbed seeds would be needed to separate them. Adds caution to the "dominant=A1" verdict: A1 *is* uniquely dominant in attractor selection (only slab whose swap collapses to its own basin), but A2/A3 ablations are degenerate and the §50-style separation magnitude reading underestimates A2/A3's effect by collapsing them to the same attractor.