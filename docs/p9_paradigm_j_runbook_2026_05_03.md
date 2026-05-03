# P9 Paradigm J — γ-only Mini-Run Runbook (Phase 2.X entry)

- ts_utc: 2026-05-03
- agent: P9 wave-2 J runbook author (doc + script scaffold; no execution)
- spec_id: p9_paradigm_j_runbook_2026_05_03
- companion / source spec: `docs/p9_paradigm_j_active_inference_2026_05_03.md` (§8 mini-run table)
- substrate base: Phase 1.6 sentinel `/tmp/p9_p1_6_sentinel_train_50k.py` on ubu1 (CLM v4 350M + LoRA r=64)
- training script (deliverable B): `/tmp/p9_paradigm_j_mini.py` on ubu1
- gate: doc + script scaffold only; **EXEC requires explicit user OK** (Phase 1.6 currently holds GPU on ubu1)
- raw#9 compliance: writing `.py` to `/tmp` only (allowed substrate per spec); no project-tree `.py` introduced
- raw#15 SSOT: this file
- raw#91 honest C3: §6 below (3 caveats)

---

## 0. TL;DR

| Item | Value |
|---|---|
| Goal | Empirically verify J-VAE objective on CLM v4 350M base — F-J1 (free energy decreases), F-J2 (latent non-trivial), F-J3 (reconstruction non-trivial), F-J4 (φ★ floor preserved), F-J5 (chat-CE ≤ 1.2× α-only baseline) |
| Base model | CLM v4 350M `ConsciousDecoderV2` (d_model=768, n_layer=16) |
| Adapter | peft LoRA r=64, α=128 on `q_proj/k_proj/v_proj/o_proj/gate_proj/up_proj/down_proj` (matches Phase 1 sentinel; **NOT** Phase 1.6's r=128 — keep base J cheaper) |
| Loss | `L = α·CE + γ_FE · F_J` where `F_J = KL(q_φ(s|e_t) ‖ N(0,I)) − β_FE · log p_θ(e_t|s_t)` |
| Variant | J-VAE (Phase-1) — reparameterization trick; J-PC reserved |
| Encoder `q_φ` | 2-layer MLP `768 → 512 → 2 × K_FE` (μ, log σ²) |
| Decoder `p_θ` | 2-layer MLP `K_FE → 512 → 768` (regress back to `e_t`) |
| Latent dim K_FE | 192 (= d/4 = 768/4) |
| Mid-layer ℓ_FE | block index 8 of 16 (mid-depth) |
| Prior | `N(0, I)` (J-VAE) |
| β_FE | locked 1.0 (Phase-1) |
| γ_FE sweep | LHS over `{0.05, 0.2, 0.8}` — 3 mini-runs |
| α (CE weight) | 6.0 fixed (no Phase 1.5 warmup — this is a 1k-subset pilot, not 50K) |
| δ | 0.0 (γ-only mini; δ-floor measurement post-hoc, not in-loop hinge) |
| Subset | 1k from `/tmp/p9_p1_6_sft_data_50k_v3.jsonl` (deterministic, seed=42) |
| Epochs | 1 (~250 steps at batch=4, accum=1) |
| Wall (1× H100) | ~25 min × 3 runs = ~75 min |
| Wall (1× RTX 5070 ubu1) | ~2.5 h × 3 runs = ~7.5 h (not recommended for sweep; see §3) |
| Cost | $2–4 / run × 3 = **$6–12 total** on RunPod 1× H100 spot |

---

## 1. Architecture deltas vs Phase 1.5/1.6 sentinel

The mini-run is a **forked branch** of `/tmp/p9_p1_6_sentinel_train_50k.py`; key deltas:

1. **Add J-VAE heads** — `q_phi: Linear(768, 512) → ReLU → Linear(512, 2*192)` and
   `p_theta: Linear(192, 512) → ReLU → Linear(512, 768)`. Both bf16 on device, ~1M params each, included in optimizer's parameter list (alongside LoRA params).
2. **Forward hooks**:
   - `tok_emb` → capture `e_t` (input embeddings, post-dropout) — `(B, T, 768)`
   - `blocks[8]` output → capture mid-layer hidden `h_mid` — `(B, T, 768)` (used as the conditioning context for `q_phi(s | e_t, h_mid)` if ever extended; Phase-1 J-VAE uses `e_t` only per spec §1.2)
3. **Loss assembly** (per spec §2.1):
   ```
   μ, log_σ² = q_phi(e_t)         # shape (B, T, 192) each
   s = μ + ε ⊙ exp(0.5 · log_σ²)  # ε ~ N(0, I), reparameterization
   ê_t = p_theta(s)               # shape (B, T, 768)
   L_KL    = 0.5 * Σ_dim (σ² + μ² − 1 − log σ²)        # closed form vs N(0,I)
   L_recon = MSE(ê_t, e_t.detach())                     # accuracy term, e_t target detached
   F_J     = L_KL − β_FE · (− L_recon)  = L_KL + β_FE · L_recon
   L_total = α · CE + γ_FE · F_J        # NO β·tens, NO δ·hinge in γ-only mini
   ```
4. **F metric extension**:
   - Add `F_J_total`, `F_J_kl`, `F_J_recon`, `F_J_post_sigma_mean` to `f_log` per probe (every 50 steps; full traj has ~5 probes for 250 steps).
5. **No HF push, no savepoints** — pilot run, in-tmp adapters only, results captured in `trajectory.json`.
6. **No 50K data** — load only first 1000 records (deterministic shuffle with seed=42 prior to slice).

---

## 2. Falsifier readout (post-run)

After each γ_FE run, derive from `trajectory.json`:

| Falsifier | Computed from | Pass criterion |
|---|---|---|
| F-J1 | EMA of `f_log[*]['F_J_total']` | non-increasing trend across 5 probes |
| F-J2 | mean of `f_log[*]['F_J_post_sigma_mean']` | > 0.05 (no posterior collapse) |
| F-J3 | final `f_log[-1]['F_J_recon']` vs initial | recon improves by ≥ 1.0 nat-equiv (MSE drops ≥ 30%) |
| F-J4 | post-run φ★ probe (separate, on saved adapter) | ≥ 5.0 absolute |
| F-J5 | final `f_log[-1]['loss_ce']` vs α-only baseline | within 1.2× of baseline α-only CE on same 1k subset |

α-only baseline = run script with `ANIMA_GAMMA_FE=0.0` once (acts as control); subsequent γ_FE ∈ {0.05, 0.2, 0.8} runs compare against it.

---

## 3. Recommended launch substrate

**Recommendation: RunPod 1× H100 spot** for the 3-run γ_FE LHS sweep.

| Substrate | Pros | Cons | Verdict |
|---|---|---|---|
| ubu1 RTX 5070 (after Phase 1.6 done) | $0; data already cached at `/tmp` | 4–5× slower than H100; total ~7.5 h vs 75 min; blocks ubu1 for any other GPU work | **Acceptable for 1 calibration run; NOT recommended for full 3-run sweep** |
| RunPod 1× H100 spot | 4–5× faster; parallel-able; ubu1 free for other workloads | $6–12 cost; data + ckpt + tokenizer must be uploaded; HF token export needed | **Recommended for sweep** |

**Hybrid plan (recommended)**:
1. After Phase 1.6 sentinel completes on ubu1 (estimated 55–65 min wall, currently in progress), run **1 calibration mini-run on ubu1 with γ_FE = 0.2** (~2.5 h) to validate the script end-to-end at zero cost.
2. If calibration passes F-J1 + F-J3 + F-J5 directionally, spin up RunPod 1× H100 spot and run the full γ_FE ∈ {0.05, 0.2, 0.8} sweep (~75 min, $6–12).
3. If calibration fails any falsifier, debug locally before paying for cloud.

This is the cheapest path to a defensible 3-point γ_FE curve.

---

## 4. Launch sequence (ubu1 calibration)

Pre-flight (assumes Phase 1.6 sentinel has freed the GPU):

```bash
# On ubu1
nvidia-smi  # confirm GPU free
ls -la /tmp/p9_p1_6_sft_data_50k_v3.jsonl    # data present
ls -la /tmp/tokenizer_64k_multilingual.model # tokenizer present
ls -la /home/aiden/anima/checkpoints/clm_v4_350m/scale_350m/best.pt  # ckpt present
ls -la /tmp/p9_paradigm_j_mini.py            # script present (see §5 deliverable)
```

Single calibration run (γ_FE = 0.2):

```bash
cd /tmp
export ANIMA_N_STEPS=250
export ANIMA_GAMMA_FE=0.2
export ANIMA_BETA_FE=1.0
export ANIMA_K_FE=192
export ANIMA_LAYER_FE=8
export ANIMA_SEED=42
export ANIMA_SUBSET=1000
/home/aiden/venv_orchestrator/bin/python3 /tmp/p9_paradigm_j_mini.py \
    2>&1 | tee /tmp/p9_paradigm_j_mini_g0p2.log
```

α-only baseline (γ_FE = 0):

```bash
export ANIMA_GAMMA_FE=0.0
/home/aiden/venv_orchestrator/bin/python3 /tmp/p9_paradigm_j_mini.py \
    2>&1 | tee /tmp/p9_paradigm_j_mini_g0p0_baseline.log
```

Output dir: `/tmp/p9_paradigm_j_mini_out/{trajectory_g{γ}.json, verdict_g{γ}.json, train_g{γ}.log}`.

---

## 5. Launch sequence (RunPod 1× H100 sweep)

Pre-flight on RunPod pod:

```bash
# Upload required files (from local laptop or via runpodctl):
#   /tmp/p9_p1_6_sft_data_50k_v3.jsonl         → /tmp/
#   /tmp/p9_p1_sft_data_holdout_500_augmented.jsonl → /tmp/
#   /tmp/tokenizer_64k_multilingual.model      → /tmp/
#   /home/aiden/anima/checkpoints/clm_v4_350m/scale_350m/best.pt → ~/anima/checkpoints/...
#   /home/aiden/anima/models/conscious_decoder.py + deps → ~/anima/models/
#   /tmp/p9_paradigm_j_mini.py                 → /tmp/
pip install peft==0.19.1 transformers==5.5.0 sentencepiece huggingface_hub
nvidia-smi  # confirm H100
```

3-run sweep:

```bash
for GAMMA in 0.05 0.2 0.8; do
  export ANIMA_GAMMA_FE=$GAMMA
  export ANIMA_N_STEPS=250
  python3 /tmp/p9_paradigm_j_mini.py 2>&1 | tee /tmp/p9_paradigm_j_mini_g${GAMMA}.log
done
# Plus α-only baseline (above)
```

Estimated wall: ~25 min × 3 = 75 min. Cost: ~$2/h × 1.25 h ≈ $2.50/run × 3 + $0.25/h baseline run ≈ **$8–10**.

---

## 6. Honest C3 caveats (mandatory raw#91, 3 items)

1. **K_FE = 192 on a d=768 model is 4× smaller than the spec's K_FE = 1024 on Mistral-7B d=4096.** Same `d/4` ratio, but absolute capacity is in a regime where posterior collapse risk is *higher* (smaller bottleneck → KL term dominates faster). F-J2 is the gate; if it fails on the 350M base, that does not directly invalidate the 7B story — re-validate at scale before drawing FEP-vs-IIT conclusions.
2. **Mid-layer ℓ_FE = 8 was chosen by `n_layer / 2` heuristic without empirical layer-probe evidence.** A real per-layer probe (linear regression of `s_t` against next-token CE) is needed to confirm layer 8 is the optimal injection point. Phase-2 should sweep ℓ_FE ∈ {4, 8, 12}; this Phase-1 mini-run does not.
3. **Reconstruction target `e_t` is the frozen `tok_emb` lookup, not contextual semantics.** Per spec §9 caveat #5, `p_θ(e_t | s_t)` round-trips static embedding vectors — the "generative world model" interpretation is overstated for J-VAE. The genuine FEP test (sequence-level `p(o_{t+1}|s_t)` predictive coding) waits for J-PC in Phase-2. Treat F-J3 pass as "the bottleneck preserves enough info to reconstruct," not "the model has learned a world model."

---

## 7. SSOT pointers

- This runbook: `docs/p9_paradigm_j_runbook_2026_05_03.md` (HERE)
- Source spec: `docs/p9_paradigm_j_active_inference_2026_05_03.md` §8.1
- Training script: `/tmp/p9_paradigm_j_mini.py` on ubu1 (raw#9-compliant `/tmp` substrate)
- Phase 1 sentinel reference: `/tmp/p9_p1_6_sentinel_train_50k.py` on ubu1
- Base model: `/home/aiden/anima/checkpoints/clm_v4_350m/scale_350m/best.pt`
- 1k pilot subset source: `/tmp/p9_p1_6_sft_data_50k_v3.jsonl` (first 1000 records, seed=42 shuffle)
- Holdout for α-only / γ_FE F1 sanity (optional): `/tmp/p9_p1_sft_data_holdout_500_augmented.jsonl`
- Env verified 2026-05-03: peft=0.19.1, transformers=5.5.0, torch=2.6.0+cu124, CUDA=True, 1× RTX 5070 12 GiB
