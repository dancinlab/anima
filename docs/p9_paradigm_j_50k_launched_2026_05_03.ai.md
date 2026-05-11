# P9 Paradigm J 50K production — LAUNCHED (watchdog queued)

- ts_utc: 2026-05-03T12:43Z
- agent: P9 Paradigm J 50K production launcher (RETRY after prior subagent 503)
- spec_id: p9_paradigm_j_50k_landed_2026_05_03 (deferred — landed marker after EXEC completes)
- substrate: ubu1 RTX 5070 12 GiB
- launch state: **WATCHDOG_QUEUED** (GPU currently occupied by another agent's seed43 sentinel retrain; watchdog polls every 10s for ≥9 GiB free, max 2h)
- raw#9: real train script in `/tmp` (no project-tree `.py` introduced)
- raw#15 SSOT: this doc + `state/p9_paradigm_j_50k_2026_05_03/launch_status.json`
- raw#10: synthetic SFT data path (chat composition, p1.6 v3) noted in launch status

---

## TL;DR

| Item | Value |
|---|---|
| Goal | Paradigm J full 50K production with γ_FE=0.2 (sweet spot from 250-step pilot) on Phase 1.6 substrate |
| Base | CLM v4 350M ConsciousDecoderV2 + LoRA r=128 α=128 (attention + MLP) |
| Loss | `α(t)·CE + β·MSE(tens) + δ(t)·max(0, 5−φ★) + γ_FE·F_J` where `F_J = KL(q_φ ‖ N(0,I)) + β_FE·MSE(p_θ, e_t)` |
| Hyperparams | α curriculum 12→6 (3K-7K), β=0.10, δ curriculum 0.5/0.5/1.0, γ_FE=0.2, β_FE=1.0, K_FE=192, ℓ_FE=8 |
| Steps | 50,000 (effective batch 32 = micro 4 × accum 8) |
| Substrate | ubu1 RTX 5070 12 GiB (after GPU frees from seed43 sentinel ~13:55 UTC) |
| Wall | ~60 min training + ~60 min wait = ~14:45-15:00 UTC ETA |
| Cost | $0 (local) |
| Savepoints | step 5K, 10K, 25K, 50K → HF `dancinlab/clm-v4-paradigm-j-50k-step-{N}k` + `-final` |
| Outputs | `/tmp/p9_paradigm_j_50k_out/{trajectory.json, verdict.json, train.log}` on ubu1 |
| Marker (deferred) | `state/markers/p9_paradigm_j_50k_landed.marker` (write after verdict.json appears) |

---

## 1. What I did this turn

1. **Surveyed substrate**. ubu1 GPU 8.3 GiB used / 3.4 GiB free (occupied by `p9_p1_5_sentinel_seed43_train.py` PID 1726340, at step 3500/50000 ≈ 7%, ~75 min remaining). ubu2 also occupied (8.5/3.2 GiB; seed44 sentinel at step 10K/50K). Neither has 10 GiB headroom needed for J 50K + LoRA r=128 + J-VAE heads.
2. **Forked Phase 1.6 sentinel** `/tmp/p9_p1_6_sentinel_train_50k.py` → `/tmp/p9_paradigm_j_50k_train.py` on ubu1. Forking preserves the production scaffolding (α curriculum, savepoints, HF push, F1 holdout, φ★ probe, F-metrics, verdict logic).
3. **Patched J-VAE FEP loss** into the forked script:
   - Added `GaussianEncoder` (q_φ: d_model→512→2K_FE) and `GaussianDecoder` (p_θ: K_FE→512→d_model) modules at `K_FE=192`.
   - Hooked `real_decoder.drop` (post-tok-emb dropout) to capture `e_t`.
   - Added `kl_normal_unit` + `reparameterize` helpers.
   - Optimizer extended to include `q_phi` + `p_theta` parameters alongside LoRA.
   - Loss assembly: `total = α(t)·CE + β·tens + δ·hinge + γ_FE·(KL + β_FE·MSE)`.
   - Compact log + trajectory schema extended with F_J / F_J_kl / F_J_recon fields.
   - Schema strings updated (`anima/p9_paradigm_j_50k/{trajectory,verdict}/1`).
4. **Validated patched script offline**: AST parse OK; J-VAE class injection verified; tokenizer/data/checkpoint paths confirmed present on ubu1; deps (peft 0.19.1, transformers 5.7.0, torch 2.11.0+cu128) confirmed.
5. **Created watchdog launcher** `/tmp/j50k_launcher.sh` on ubu1: polls `nvidia-smi` every 10s; when ≥9000 MiB free, launches the training in detached `nohup` and exits. Max wait 2h then timeout.
6. **Launched watchdog** detached: PID 2151732 on ubu1. Logs to `/tmp/p9_paradigm_j_50k_launcher.log`. As of 12:43 UTC: alive, polling, GPU still 3.4 GiB free.

---

## 2. Initial loss + ETA

**Initial loss trajectory: NOT YET AVAILABLE.** Training has not started — the watchdog is waiting for GPU. The user was specifically informed: "Run training in detached nohup so subagent can return without waiting full duration. Report initial 1K-step loss trajectory + ETA, return; user can poll later."

Per-task fidelity, returning now without waiting 75+ min for GPU + 10+ min for first 1K steps. **Initial loss + per-step latency will be available ~60-75 min from now** at `/tmp/p9_paradigm_j_50k_out/train.log`.

**ETA breakdown**:
- 12:43 UTC: watchdog launched, polling
- ~13:55 UTC: estimated GPU free (seed43 sentinel finishes step 50K)
- ~13:55 UTC: training auto-launches via watchdog
- ~14:00 UTC: tokenization + ckpt load complete (~5 min based on Phase 1.6 sentinel timing)
- ~14:01 UTC: step 1 begins, baseline φ★ + F0 probe
- ~14:10 UTC: step ~1000 reached (initial loss measurable)
- ~14:55-15:00 UTC: step 50000 + final F probe + HF push complete

**Alternative**: if seed43 finishes faster (e.g. user pre-empts) or another GPU frees, watchdog launches sooner and ETA shifts left correspondingly.

---

## 3. Honest C3 caveats (raw#91)

1. **GPU contention is the binding constraint, not capability.** Watchdog approach was chosen to avoid killing another agent's in-progress training (seed43 sentinel). User could alternatively `kill 1726340` on ubu1 to start J 50K immediately — saves ~75 min wall but destroys ~3K steps of Phase 1.5 reproduction work. Default chose preservation; user can override.

2. **K_FE = 192 on d_model 768 is the same `d/4` ratio as the spec's K_FE=1024 on Mistral-7B (d=4096), but absolute capacity is 4× smaller** — posterior collapse risk per spec §6 caveat 1 still applies. F-J2 (sigma_mean > 0.05) is the in-loop check; will be readable from `f_log` in the trajectory.

3. **J-VAE injection point ℓ_FE=8 is `n_layer/2` heuristic, unverified at 50K scale.** The 250-step pilot was pre-Phase-1.6 substrate (LoRA r=64 not r=128); whether γ=0.2 sweet spot transfers to r=128 + α-curriculum + 50× more steps is the empirical question this run answers. **Sweet spot transfer is NOT proven** — pilot result is suggestive, not predictive.

4. **No baseline α-only run for direct F-J5 comparison was launched in this RETRY.** The Phase 1.6 sentinel itself (already complete: F1=0.0059, φ★=43.28) IS the α-only baseline (γ_FE=0). F-J5 readout = `(J50K final CE) ≤ 1.2 × (Phase 1.6 final CE)` — direct comparison, no extra run needed.

5. **HF push to `dancinlab/clm-v4-paradigm-j-50k-*` repos requires HF_TOKEN.** Launcher tries to load from `/home/aiden/.hf_token` or `.bashrc`. If both fail, savepoints still land on disk at `/tmp/p9_paradigm_j_50k_savepoints/` but HF push errors will appear in the verdict's `hf_push_log` (non-blocking — Phase 1.6 sentinel pattern).

6. **Watchdog 2h timeout means: if seed43 + any subsequent jobs total > 2h, training never starts.** If timeout hits, watchdog logs `TIMEOUT: GPU never freed up after 2h` and exits. User must manually rerun watchdog or escalate.

---

## 4. SSOT pointers

- This doc: `docs/p9_paradigm_j_50k_launched_2026_05_03.ai.md` (HERE — LAUNCH state)
- Landed doc (deferred — write after verdict): `docs/p9_paradigm_j_50k_landed_2026_05_03.ai.md`
- Launch status JSON: `state/p9_paradigm_j_50k_2026_05_03/launch_status.json`
- Marker (deferred): `state/markers/p9_paradigm_j_50k_landed.marker`
- Source spec: `docs/p9_paradigm_j_active_inference_2026_05_03.md` §8.1
- Pilot runbook: `docs/p9_paradigm_j_runbook_2026_05_03.md`
- Substrate (Phase 1.6 sentinel parent): `docs/p9_p1_6_redesign_2026_05_03.md`
- Training script (ubu1): `/tmp/p9_paradigm_j_50k_train.py` (28K → 31K bytes after J-VAE patches)
- Patch script (ubu1, mac copy): `/tmp/j50k_patch.py`
- Watchdog launcher (ubu1): `/tmp/j50k_launcher.sh`
- Outputs (ubu1, populated post-EXEC): `/tmp/p9_paradigm_j_50k_out/{trajectory.json, verdict.json, train.log}`
- Savepoints (ubu1, populated post-EXEC): `/tmp/p9_paradigm_j_50k_savepoints/{step_5000, step_10000, step_25000, step_50000, final}/`

---

## 5. User next-step (poll commands)

```bash
# Status of watchdog wait + training launch
ssh ubu1 'tail -20 /tmp/p9_paradigm_j_50k_launcher.log'

# Training progress (after watchdog launches)
ssh ubu1 'tail -30 /tmp/p9_paradigm_j_50k_out/train.log 2>/dev/null'

# GPU state
ssh ubu1 'nvidia-smi --query-gpu=memory.used,memory.free --format=csv'

# Final verdict (after ~14:55 UTC)
ssh ubu1 'cat /tmp/p9_paradigm_j_50k_out/verdict.json'

# Pull artifacts to laptop (after completion)
scp ubu1:/tmp/p9_paradigm_j_50k_out/{trajectory.json,verdict.json,train.log} \
    /Users/ghost/core/anima/state/p9_paradigm_j_50k_2026_05_03/
```
