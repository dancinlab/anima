# BG-COMPONENT-MLP-EMBED-V14 — spec

**Date**: 2026-05-10
**Lineage**: §50 → §57 (slab-locus) → §58 (correlation/h_to_c) → §62 (component-locus weight-space) → THIS BG (component-axis V14 verification).
**Predecessor verdict**: §57 PROMOTED §50 to PROVEN-AT-BODY-LOCUS — engine_a's 24-layer transformer body collectively carries the V14 PASS lever; A1/A2/A3 swaps all flip V14_PASS → V14_VIOLATED, with A1_slab1_early dominant in attractor selection. §62 found chat dual-loss localizes weight-drift to `attn.q_proj` (cos_AB=0.6468) but with U-shaped layer profile (slab2_middle most-drifted) — drift magnitude DECOUPLED from V14 causal effect (F-DUAL-LOSS-3 partial trigger).

**Mission**: Functional (V14) verification of §62 prediction 3 + finding 7 follow-up.

## Predictions tested

§62 listed 4 ablation predictions; this BG fires 1 of them functionally:

- **Prediction 3** (CONFIRM/FALSIFY): MLP-gate-only swap perturbs V14 less than full slab swap (§57: full slab → V14_VIOLATED, separation_change ≈ −1068 to −1375) but more than v_proj swap (deferred).
- **Bonus 4** (BEYOND §57 SURFACE): tok_emb / lm_head swap probe — these are tied at runtime per `EngineAGModel(cfg.tie_lm_head=True)` so `tok_emb.weight = lm_head.weight`. §62 found `tok_emb.weight` cos_AB = 0.7464 — non-trivial drift. §57's swap surface was layers-only; tok_emb / lm_head / norm_f stayed at A's values. This BG opens that surface.

## Substrates

Identical to §57 / §62.

| Substrate | path | params | training |
|---|---|---|---|
| A | `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt` | 350M bf16 | BG-LB pretrain → Phase 2 chat-template cotrain (curriculum w=0.3→0.5) |
| B | `~/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt` | 350M bf16 | BG-LA persona-only pretrain (no chat dual loss) |

## Method — 30 V14 trajectory trials

Each trial = 1 V14 short trajectory: 1 trained pass at `N_TURNS=128`, `MAX_CELLS=128`. The mirror baseline distribution is computed once (3 mirror seeds) as a shared reference.

### Conditions and trial counts

| condition | swap surface | trials | seeds |
|---|---|---|---|
| C0 baseline | (none — pristine A) | 1 | 42 |
| C1 gate × slab1 | `layers.0..7.ffn.gate.weight` ← B | 3 | 42, 137, 271 |
| C2 gate × slab2 | `layers.8..15.ffn.gate.weight` ← B | 3 | 42, 137, 271 |
| C3 gate × slab3 | `layers.16..23.ffn.gate.weight` ← B | 3 | 42, 137, 271 |
| C4 up × slab1 | `layers.0..7.ffn.up.weight` ← B | 3 | 42, 137, 271 |
| C5 down × slab1 | `layers.0..7.ffn.down.weight` ← B | 3 | 42, 137, 271 |
| C6 tok_emb only | `tok_emb.weight` ← B (lm_head retains A via untying) | 5 | 42, 137, 271, 311, 521 |
| C7 lm_head only | `lm_head.weight` ← B (tok_emb retains A via untying) | 5 | 42, 137, 271, 311, 521 |
| C8 tok_emb + lm_head | both ← B (kept tied) | 5 | 42, 137, 271, 311, 521 |
| **Σ** | | **30** | |

Plus mirror baseline (3 random_init mirrors at seeds 42, 137, 271) once.

### Tying handling for C6 / C7

`EngineAGModel.__init__` sets `self.lm_head.weight = self.tok_emb.weight` when `cfg.tie_lm_head=True` (true for both substrates). Direct in-place mutation of `tok_emb.weight` automatically mutates `lm_head.weight`.

For **C6 tok_emb only** and **C7 lm_head only**, we untie pre-swap by replacing the `lm_head.weight` `nn.Parameter` with a fresh independent clone, perform the targeted swap, then run V14. Diagnostic asserts confirm post-swap that the non-target tensor still equals A.

For **C8 tok_emb + lm_head pair**, tying is preserved; one in-place swap on `tok_emb.weight` propagates to `lm_head.weight`.

### V14 short trajectory definition (mirrors §57 / §50)

- `compute_iit_phi(cell_pool, n_bins=16)` per-snapshot
- `MitosisV5Engine` with split_patience=3, split_noise=0.10, merge_threshold=0.005, merge_patience=30, min_cells=2, lorenz_scale=0.05
- byte-hash prompt encoding via `_v14_5seed_run.encode_prompt_to_ids` (`T=16`)
- `MAX_CELLS=128`, `N_TURNS=128`, `SNAPSHOT_EVERY=16`

### Per-trial outputs

- `final_iit_un16` — terminal Φ_un16
- `final_proxy_phi` — terminal proxy phi
- `final_n_cells`
- `n_splits`, `n_merges`, `cap_bound_turns`
- 8-snapshot trajectory

### Per-condition aggregation

mean / std / min / max of `final_iit_un16` and `final_n_cells` across the condition's trials. Compared against:
- baseline trained Φ_un16 (C0 single value)
- mirror Φ_un16 distribution (mean over 3 random_init seeds)

### V14 verdict per condition

For each trial: `beats_mirror = trained_un16 > mean(mirror_un16) AND trained_proxy > mean(mirror_proxy)`.

Condition verdict:
- `V14_PASS_ROBUST` — all trials beat both metrics
- `V14_PASS_PARTIAL` — majority of trials beat
- `V14_VIOLATED` — minority/none of trials beat

## Falsifiers

- **F-COMP-1** (Prediction 3 confirmed): `gate × slab1` produces verdict between baseline (PASS) and full-slab (VIOLATED). Quantified: `mean(separation) ∈ (slab1_full_separation, baseline_separation)` strictly (i.e., gate-only-slab1 partially perturbs). ★★★ supportive evidence.
- **F-COMP-2** (Prediction 3 falsified — gate dominant): gate × slab1 fully reproduces slab1 V14_VIOLATED. Implies MLP-gate is the slab1 lever. Cross-link with §62 (which found `q_proj` more drifted than `gate`) → drift-vs-causality decoupling extended to component axis.
- **F-COMP-3** (Prediction 3 falsified — gate negligible): gate × slab1 preserves V14_PASS at baseline level. Implies attention components carry slab1's V14 effect (q/k/o), consistent with §62's q_proj primacy.
- **F-COMP-4** (tok_emb causally dominant): tok_emb-only swap flips V14. Implies §57's slab study missed a major lever — embedding map matters beyond layer body.
- **F-COMP-5** (lm_head causally null when untied): lm_head-only swap leaves V14 unchanged. Confirms that the engine_g `hidden_mean` capture (which is read AFTER `norm_f` but BEFORE `lm_head`, via `HiddenMeanCapture`) is decoupled from `lm_head` — a sanity check (lm_head is downstream of hidden_mean capture, so it physically cannot affect the mitosis trajectory).

Note on F-COMP-5: `HiddenMeanCapture` (per `_v14_5seed_run.py`) hooks `model.engine_g`, which receives `hidden.mean` BEFORE `lm_head`. Therefore lm_head perturbation CANNOT affect engine_g cell dynamics; F-COMP-5 should trivially pass. If it does not, there is an instrumentation bug.

## Constraints (own/raw)

- **raw#9** — `training/*.py` local-only; this script lives under `state/` (gitignored).
- **raw#15 additive** — A and B ckpts loaded read-only via `torch.load`; all tensor ops are out-of-place (per-condition fresh model build from snapshotted A state_dict); no file mutation.
- **own 16** — $0 local Mac CPU; wall-clock target ≤60 min.
- **own 22** — every trial's metrics emit; verdict.md SSOT; **REBORN.md NOT appended** by this run (parent dispatcher §63 handles that).
- **own 38** — artefacts under `state/anima_component_mlp_embed_v14_2026_05_10/`.

## Time budget

- 30 trials × ~30s = ~15 min (target)
- Plus baseline + 3 mirrors ≈ 2 min
- Plus model-load overhead (B once + A snapshot once) ≈ 1 min
- **Total target**: ≤20 min, hard ceiling 60 min.

## Output deliverables

| file | content |
|---|---|
| `spec.md` (this) | hypothesis + method + falsifier table |
| `run.py` | the executable (raw#9, state-local, gitignored) |
| `run.log` | timestamped run-log with per-trial flip events |
| `trial_results.json` | all 30 trial scalars + 8 snapshots each |
| `summary.json` | per-condition aggregate stats + falsifier dispositions |
| `verdict.md` | Prediction 3 + tok_emb/lm_head decision + C3 ≥7 |
