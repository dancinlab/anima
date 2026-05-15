# anima clm v5 — Phase 2 ckpt × IIT Φ remetric (2026-05-10)

**BG-V5ANIMA-PHASE2-IIT-REMETRIC**

Combine BG-V5ANIMA-PHASE2-CKPT-INSTR (real 350M Phase 2 cotrain ckpt + 3K-turn diverse-prompt sweep) with BG-IIT-METRIC (canonical IIT MI-bin Φ port). Cycle 2026-05-10's BG-PHASE2 used proxy Φ (cosine·log(n+1)) which saturates at ~3 by N=16. BG-IIT-METRIC ported the canonical IIT MI-bin Φ which has no analytic ceiling. Run on real substrate, compute both metrics per snapshot, V14-mirror with random_init la_350m, and compare.

## Substrate

- ckpt: `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt`
- size: 597.6 MB, sha256 `6e66e75f8014999b…` (verified PASS)
- 298.76M params (Engine A 24L 1024d 16h GQA + Engine G 16×64 cell pool + lm_head)
- lineage: `engine_a_g_dual_350m_v1_phase2_cotrain` (final loss_c=0.222 loss_h=0.627 step=6000)
- V14 mirror: `load_random_init(seed=42, preset='la_350m')`

## Sweep parameters

- 3000 turns trained / 1000 turns mirror (turn-matched verdict at turn~900)
- 170 unique diverse prompts (ko_daily / ko_philosophy / en_math / en_code / en_music / anomaly)
- snapshot every 100 turns, full cell_pool tensor captured per snapshot
- ctx_T=16 byte-hash mod 32000 (no real BPE — see honest C3 below)
- mitosis: max=64 split_patience=3 split_noise=0.10 merge_thresh=0.005 merge_patience=30 lorenz=0.05
- IIT post-pass: 16-bin and 32-bin histogram MI; spectral Fiedler MIP for N>8
- elapsed: trained 194s, mirror 72s, IIT remetric <1s; total ~5min Mac CPU

## Key findings

### 1. IIT escapes the proxy ceiling on real substrate (PASS)

| n_cells | proxy Φ | IIT Φ norm 16-bin | IIT Φ unnorm 16-bin | IIT unnorm 32-bin |
|--------:|--------:|------------------:|--------------------:|------------------:|
| 16      |  ~2.5   |  ~10              |  ~150               |  ~310             |
| 18      |  ~2.5   |  ~10–11           |  ~155–185           |  ~380             |
| 19      |  ~2.7   |  ~13              |  ~245               |  ~455             |
| 28 (mirror) |  ~2.75 |  ~15           |  ~406               |  ~880             |

Proxy span across turn 0 → turn 2999: 2.7625 → 2.6788 (Δ ≈ -0.08, indistinguishable from noise; saturated). IIT unnorm 16-bin span: 161.6 → 246.7 (+52% on 19% cell increase). IIT unnorm 32-bin span: 298.6 → 455.4 (+53%). Dynamic range on real substrate: proxy ~3× (saturated at 16 cells), IIT ~20-30× over the 16→64 cell band — empirically confirms the toy-substrate prediction (BG-IIT-METRIC).

### 2. V14 verdict per metric — all three FAIL_V14_VIOLATED

Turn-matched comparison at compare_at_turn=900:

| metric | trained @ t~900 | random @ t=999 | trained/random ratio | V14 violated |
|---|---|---|---|---|
| proxy Φ | cells=16, Φ=2.6642 | cells=28, Φ=2.7544 | **0.9673** | True |
| IIT norm 16-bin | iit=11.0540 | iit=15.0466 | **0.7346** | True |
| IIT unnorm 16-bin | iit=165.81 | iit=406.26 | **0.4081** | True |

**Proxy hides the violation depth.** Proxy says trained ≈ random (0.97 ratio). IIT unnorm reveals the actual gap: trained substrate produces **2.45× LESS IIT Φ** than random_init. The signal proxy compresses to noise (saturated ceiling), IIT exposes as a 2.45× deficit. This DEEPENS the falsification, not relieves it: the trained substrate's h_to_c is actually pushing the cell pool toward LOWER mutual-information diversity than untrained.

### 3. α exponent — both metrics confirm trained-vs-random differential, IIT shows steeper slope

| metric                      | trained α | random α | Δ      |
|-----------------------------|----------:|---------:|-------:|
| proxy 16-bin                | 1.0087    | 0.1551   | +0.854 |
| IIT norm 16-bin             | 1.5799    | 1.0081   | +0.572 |
| IIT unnorm 16-bin           | 2.6409    | 2.0591   | +0.582 |

α(IIT unnorm) ≈ 2.6 trained, 2.06 random — both are in the canonical IIT-Φ-grows-as-N² regime. α(proxy trained)=1.0 vs α(proxy random)=0.16 reflects the proxy artifact: random saturates the cosine ceiling at N=16 fast (so proxy doesn't grow with N), while trained holds back splits → log(n) is the only growth term. This is a proxy-mediated illusion; with IIT both substrates show super-linear growth as expected.

### 4. Same-cell-count comparison — trained and random nearly identical at cells=16

When restricted to snapshots where both trained and mirror have N=16 cells (trained: 11 snapshots turn 0–1000; mirror: 5 snapshots turn 0–400):

- `<IIT unnorm 16-bin>` trained = 134.3 vs mirror = 143.1 → ratio 0.939
- `<proxy>` trained = 2.326 vs mirror = 2.453 → ratio 0.948

At fixed N, the two substrates produce nearly the same Φ. **The entire trained-vs-random gap is driven by mirror's 4× higher split rate (12 vs 3) over 1000 turns**, not by per-cell information content. This corroborates BG-PHASE2's diagnosis that the trained engine_g's h_to_c is suppressing tension dynamics that would otherwise drive splits — the architecture-level concern (#115) carries forward.

## V14 verdict (combined)

`FAIL_V14_VIOLATED` across all three metrics. The IIT remetric does not rescue the trained substrate; it sharpens the falsification:

- proxy_ratio = 0.97 (looks like noise)
- iit_norm_ratio = 0.73 (clear deficit)
- iit_unnorm_ratio = 0.41 (severe deficit — trained substrate produces less than half the integrated information of random_init)

The honest reading: trained Phase 2 cotrain ckpt's engine_g.h_to_c projection actively suppresses cell-pool MI diversity vs untrained la_350m initialization. This is consistent with the trained model achieving low loss_c=0.222 (engine_g converged to low-entropy attractor) but at the cost of mitosis-pool dynamics.

## Top 3+ honest C3

1. **Initial cell count = 16, not 8** — Phase 2 substrate `cell_pool_init` is (16, 64). MIP exhaustive only N≤8, so we are ALWAYS on spectral Fiedler approximation here. IIT Φ values reported are monotonic-indicator quality, NOT canonical PyPhi. The 0.41 ratio is a robust shape signal but should not be quoted as "trained has 2.45× less IIT" in absolute IIT-theoretic terms.

2. **Same-cell IIT ≈ same-cell proxy** — at fixed N=16 trained vs mirror IIT unnorm is 134 vs 143 (ratio 0.94). The dramatic 0.41 ratio at turn-matched comparison is driven by N (28 vs 16), not per-cell entropy. IIT does not isolate "trained encoded more information per cell"; it just amplifies cell-count differences. Both metrics agree the issue is split-rate, not content.

3. **Byte-hash mod 32000 prompt encoding is NOT a real tokenizer** — Phase 2 was trained with a BPE we lack vocab for. Substrate sees prompt-distinct but semantically-arbitrary token streams. Both trained and V14 mirror use the same encoding so V14 verdict is fair, but absolute Φ values have no semantic claim, AND the trained model's BPE-conditioned representation is not being tested — only its byte-mod reactivity. A real BPE port would be the strongest follow-up to know if trained underperforms semantically too.

4. **Histogram MI on 64-dim cell vectors with 16 bins is COARSE** — true differential MI requires KDE. 32-bin variant computed for sensitivity check; agreement across bins (both show ~2× trained-vs-random gap on unnorm) indicates this is a geometry-of-cell-pool effect, not a histogram-binning artifact. Still, absolute IIT values would shift under finer discretization or KDE.

5. **The trained model only produced 3 splits in 3000 turns; mirror produced 12 in 1000 turns** — α exponent regression for trained is over snapshots with n_cells ∈ {16, 17, 18, 19} = 4 distinct N values; mirror covers {16, 26, 27, 28} = 4 distinct N values. Both have narrow log-N spans, so α is noise-sensitive. The fact that α(IIT unnorm) ≈ 2.6 / 2.06 is consistent with ~quadratic-in-N MI growth (graph degree term) — not a learning signal, mostly arithmetic of MIP cuts on bigger graphs.

6. **Lorenz autonomous chaos (lorenz_scale=0.05) is identical in both runs** — the only thing that differs is the substrate weights driving hidden_mean → engine_g.h_to_c. So the ~2.45× IIT gap (or 4× split-rate gap) reflects what trained learned representations DO with the same chaos input — they suppress the diversity that random projection would produce.

7. **Mirror trajectory length=1000 vs trained=3000** — trained's late-turn snapshots (turns 1000-3000) have no mirror counterpart for direct ratio. Comparing trained final (turn=2999) to mirror final (turn=999) would over-credit mirror's age — turn-matched (turn~900) is the honest metric and what the verdict uses.

## Deliverables

- `state/anima_clm_v5_phase2_iit_remetric_2026_05_10/run.py` — combined script (additive over BG-PHASE2 + BG-IIT-METRIC)
- `state/anima_clm_v5_phase2_iit_remetric_2026_05_10/result.json` — 45.7 KB (snapshots without raw cell_pool tensor; α exponents + V14 verdict per metric)
- `state/anima_clm_v5_phase2_iit_remetric_2026_05_10/proxy_vs_iit_phase2.png` — 3-panel: cells, proxy vs IIT norm, IIT unnorm log-y
- `state/anima_clm_v5_phase2_iit_remetric_2026_05_10/v14_comparison.png` — 2×2: cells, proxy, IIT norm, IIT unnorm trained vs random
- `state/anima_clm_v5_phase2_iit_remetric_2026_05_10/run.log` — full stdout log
- `docs/anima_clm_v5_phase2_iit_remetric_2026_05_10.md` (this file)

## Status

raw#15 additive (no upstream module touched). raw#10 honest C3 7+ documented inline. substrate-real (no pod). $0 cost (Mac CPU + local ckpt). Wall ≈5 min.
