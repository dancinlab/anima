# P9 Paradigm J 50K production — LANDED (FAIL_J: CUDA OOM at step 0)

- ts_utc: 2026-05-03T23:15Z
- agent: P9 Paradigm J 50K harvest subagent (post-launch verdict synthesis)
- spec_id: p9_paradigm_j_50k_landed_2026_05_03
- substrate: ubu1 RTX 5070 12 GiB
- verdict: **FAIL_J** (reason: `CUDA_OOM_AT_STEP_0_NO_TRAINING_OCCURRED`)
- raw#9: training script lives at `/tmp/p9_paradigm_j_50k_train.py` on ubu1; no `.py` added to project tree
- raw#15 SSOT: this doc + verdict.json + trajectory.json + comparison_matrix.json + marker
- raw#10: synthetic SFT data path was p1.6 v3 chat composition; irrelevant since training never read data
- cost: $0 (local)

---

## TL;DR

| Item | Value |
|---|---|
| Goal | Paradigm J full 50K production with γ_FE=0.2 (sweet spot from 250-step pilot) on Phase 1.6 substrate |
| Outcome | **FAIL_J — zero training steps executed** |
| Crash | torch.OutOfMemoryError at line 178 (`torch.load(CLM_CKPT)`) at 13:53:08 UTC, 4 seconds after watchdog launched training |
| Watchdog | Waited 70 min (300+ poll attempts), saw 11758 MiB free, launched, exited per design (single-shot, no respawn) |
| Interfering process | PID 3100322 holding 5.9 GiB on the GPU at crash time; identity now unknown (process gone, no tag captured) |
| Savepoints | 0/5 (none written) |
| HF repos pushed | 0/5 (HF API confirms `dancinlab/clm-v4-paradigm-j-50k-*` does not exist) |
| Falsifier outcomes | F1/F2/F3/F-J/F-J2 all VACUOUS_FAIL (no data); F4 NOT_APPLICABLE (γ_BOLD=0 by design) |
| Empirical question answered | None — sweet-spot transfer (r=64→r=128, 250→50K) remains untested |
| Sentinel-50k retraining? | NO (per task constraint "NO retraining") |
| Savepoints deleted? | NO (per task constraint "Do NOT delete savepoints"); zero existed, zero deleted |

---

## 1. What I did this turn

1. **SSH'd ubu1, verified training PID 3100347 is dead** (`nvidia-smi` shows 15 MiB used, no compute apps running; no watchdog; no respawn process).
2. **Pulled `train.log` (740 bytes) and `launch.log` (3429 bytes)** from `/tmp/p9_paradigm_j_50k_out/` to `/Users/ghost/core/anima/state/p9_paradigm_j_50k_2026_05_03/`.
3. **Read both logs** — confirmed torch.OutOfMemoryError at `torch.load(CLM_CKPT, ...)` (training script line 178) at 13:53:08 UTC, exactly 4 seconds after watchdog launched training at 13:53:04 UTC.
4. **Read watchdog launcher log** `/tmp/p9_paradigm_j_50k_launcher.log` — confirmed clean exit per design ("watchdog END (training will run ~2-4h in background)") with no respawn logic.
5. **Verified HF mirror is empty** via `curl 'https://huggingface.co/api/models?author=dancinlab&search=paradigm-j'` → `[]`. No savepoints pushed.
6. **Verified savepoint dir is empty** — `/tmp/p9_paradigm_j_50k_savepoints/` exists with zero files. Constraint "Do NOT delete savepoints" honored vacuously (nothing to delete).
7. **Verified Phase 1.6 baseline + pilot context** by reading `docs/p9_paradigm_j_50k_launched_2026_05_03.ai.md` §3 caveats: Phase 1.6 baseline F1=0.0059, φ★=43.28; pilot sweet spot γ_FE=0.2 was on r=64 substrate (transfer to r=128 + 50K steps was the empirical question this run was supposed to answer).
8. **Synthesized verdict.json + trajectory.json (empty) + comparison_matrix.json** at `state/p9_paradigm_j_50k_2026_05_03/`. Training script never produced these because it crashed at step 0; harvester wrote them per task spec.
9. **Wrote marker** `state/markers/p9_paradigm_j_50k_landed.marker`.
10. **Wrote this handoff** `docs/p9_paradigm_j_50k_landed_2026_05_03.ai.md`.

---

## 2. Crash forensics

### 2.1 Timeline

| ts_utc | event |
|---|---|
| 2026-05-03T12:43:00Z | Launch agent created watchdog `/tmp/j50k_launcher.sh` PID 2151732 on ubu1; GPU then 8367 MiB used by seed43 sentinel (PID 1726340) |
| 2026-05-03T13:32:51Z | Watchdog poll attempt 300 — GPU 3406 MiB free (seed43 partially released memory) |
| 2026-05-03T13:53:04Z | Watchdog poll observes 11758 MiB free; launches `python /tmp/p9_paradigm_j_50k_train.py` PID 3100347 in detached nohup; watchdog exits cleanly |
| 2026-05-03T13:53:05Z | Training: torch=2.11.0+cu128 imports OK, GPU detected, tokenizer loaded vocab=64000 |
| 2026-05-03T13:53:08Z | Training: decoder built (params=477,648,512). Then `torch.load(CLM_CKPT, map_location=device, weights_only=False)` raises `torch.OutOfMemoryError: Tried to allocate 20.00 MiB. GPU 0 has a total capacity of 11.50 GiB of which 18.19 MiB is free. Process 3100322 has 5.90 GiB memory in use.` |
| 2026-05-03T13:53:08Z | Process 3100347 dies with stack trace; no further training attempted (no respawn logic) |
| 2026-05-03T23:10:00Z | Harvester observes GPU now 11758 MiB free again (15 MiB used), no compute apps, watchdog gone |

### 2.2 Why crashed despite seeing 11758 MiB free at launch?

Within 1-3 seconds of watchdog observing 11758 MiB free, **another process (PID 3100322)** allocated 5.9 GiB on the GPU. By the time the J 50K training script reached the checkpoint load step (decoder construction + base CLM 350M load = ~5-6 GiB headroom needed), only 18 MiB remained free.

**Identity of PID 3100322 unknown at harvest** — process was already gone when harvester arrived, and no tagging mechanism (e.g. process name capture in launcher) was in place. **Possibilities** (ranked by prior likelihood, no direct evidence for any):
1. Another agent's launched job that won the GPU race (most likely given the active session has multiple subagents)
2. A leftover Python kernel from the seed43 sentinel that finished but didn't fully release CUDA context
3. A user-initiated script run between watchdog observation and our launch

### 2.3 Why watchdog didn't retry

The watchdog `/tmp/j50k_launcher.sh` was designed as **single-shot** per `state/p9_paradigm_j_50k_2026_05_03/launch_status.json` line 9: `"After watchdog launches training, the watchdog itself exits cleanly. Training runs in detached nohup."` There is no retry/respawn loop. Once `train.pid` is written and `nohup python ...` is launched, the watchdog assumed success and exited. The training crash happened post-watchdog-exit — no monitor was watching.

This is a **design gap**, not a bug — the original design explicitly traded restart-on-crash for simplicity (single launcher process, clean exit).

---

## 3. Falsifier outcomes (per F-hierarchy spec)

| Falsifier | Threshold (SUCCESS_J) | Measured | Outcome |
|---|---|---|---|
| F1 BLEU-1 holdout-500 | ≥ 0.0059 (Phase 1.6) | null | VACUOUS_FAIL |
| F2 φ★ trajectory final | ≥ 5.0 | null | VACUOUS_FAIL |
| F3 tension MSE final | < 0.1 | null | VACUOUS_FAIL |
| F4 BOLD r | (γ_BOLD=0 by design) | N/A | NOT_APPLICABLE |
| F-J KL final | non-divergent | null | VACUOUS_FAIL |
| F-J recon final | non-divergent | null | VACUOUS_FAIL |
| F-J2 σ_q mean (anti-collapse) | > 0.05 | null | VACUOUS_FAIL |

**Verdict label per spec hierarchy**:
- SUCCESS_J = F1 ≥ baseline AND F2 ≥ 5.0 AND F3 < 0.1 AND F-J converged → 0/4 met → not SUCCESS_J
- PARTIAL_J = 1-2 falsifiers PASS → 0 falsifiers PASS → not PARTIAL_J
- **FAIL_J = all falsifiers fail OR F-J diverged → 6 vacuous fails → FAIL_J**

The label is unambiguous despite the unusual cause (no training rather than bad training): zero passes ≤ FAIL_J's "all falsifiers fail" threshold.

---

## 4. Comparison vs pilot + Phase 1.6 baseline

| Metric | Paradigm J 50K (this run) | Paradigm J pilot 250-step | Phase 1.6 sentinel (γ_FE=0 baseline) |
|---|---|---|---|
| F1 BLEU-1 holdout-500 | null | not recorded (BLEU was 50K-only diagnostic) | 0.0059 |
| φ★ final | null | not meaningful @ 250 steps | 43.28 |
| F-J KL final | null | qualitatively converged at γ_FE=0.2 sweet spot | N/A (no J-VAE) |
| F-J recon final | null | qualitatively good accuracy at γ_FE=0.2 | N/A |
| Substrate | (intended: r=128 + Phase 1.6) | r=64, pre-Phase-1.6 | r=128, Phase 1.6 |
| Steps | 0 / 50000 | 250 | 50000 |
| γ_FE sweet spot transfer (r=64→128, 250→50K) | **UNANSWERED** | (the question this run was meant to answer) | N/A |

The single most important comparison — **does γ_FE=0.2 sweet spot survive the substrate jump from r=64 pilot to r=128 production at 200× more training steps?** — remains open.

---

## 5. Honest C3 caveats (raw#91)

1. **OOM root cause is unknown.** PID 3100322 held 5.9 GiB on the GPU at the crash moment, but the process was gone before harvester arrived. No process name was captured by the watchdog (which only logs `nvidia-smi --query-gpu` totals, not per-process tagging via `--query-compute-apps`). Without identifying the interfering process, we cannot prevent recurrence on retry — the next launch could lose the same race. **Mitigation for next attempt**: extend watchdog to log `nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv` every poll, plus add a 30s post-launch `if ! kill -0 $TRAIN_PID; then ...` watchdog-respawn block.

2. **Watchdog single-shot design has no retry-on-crash logic.** This is the second-order failure mode — even if root cause #1 is fixed, transient OOM/network/HF-push failures during a 50K run would still crash the whole job with no automatic recovery. **Mitigation for next attempt**: wrap the training launch in a 3-attempt retry loop in the launcher script (with exponential backoff and ≥9 GiB GPU re-check between attempts), and consider `flock` on a `/tmp/p9_paradigm_j_50k.lock` to prevent concurrent attempts.

3. **The empirical question — does γ_FE=0.2 sweet spot transfer from pilot (r=64, 250 steps) to production (r=128, 50K steps)? — remains unanswered.** Pilot evidence is qualitative ("γ_FE=0.2 was best of {0.05, 0.2, 0.8}" per `docs/p9_paradigm_j_active_inference_2026_05_03.md` §3.3) and substrate-mismatched. Until a successful 50K run completes, we have **zero data on whether Paradigm J as a paradigm beats Phase 1.6 baseline at full scale**. The comparison_matrix.json scaffolding is preserved precisely so the next run's outputs can drop in mechanically.

---

## 6. SSOT pointers

- **This handoff**: `docs/p9_paradigm_j_50k_landed_2026_05_03.ai.md` (HERE — LANDED state)
- **Launch handoff**: `docs/p9_paradigm_j_50k_launched_2026_05_03.ai.md` (predecessor)
- **Verdict JSON**: `state/p9_paradigm_j_50k_2026_05_03/verdict.json`
- **Trajectory JSON (empty)**: `state/p9_paradigm_j_50k_2026_05_03/trajectory.json`
- **Comparison matrix**: `state/p9_paradigm_j_50k_2026_05_03/comparison_matrix.json`
- **Marker**: `state/markers/p9_paradigm_j_50k_landed.marker`
- **Crash logs (mac-side copies)**: `state/p9_paradigm_j_50k_2026_05_03/{train.log, launch.log}`
- **Crash logs (ubu1 originals, preserved)**: `/tmp/p9_paradigm_j_50k_out/{train.log, launch.log, train.pid}`
- **Training script (ubu1, preserved)**: `/tmp/p9_paradigm_j_50k_train.py`
- **Watchdog log (ubu1, preserved)**: `/tmp/p9_paradigm_j_50k_launcher.log`
- **Empty savepoint dir (ubu1, preserved per constraint)**: `/tmp/p9_paradigm_j_50k_savepoints/` (0 files)
- **Source spec**: `docs/p9_paradigm_j_active_inference_2026_05_03.md`
- **Pilot runbook**: `docs/p9_paradigm_j_runbook_2026_05_03.md`
- **Phase 1.6 substrate**: `docs/p9_p1_6_redesign_2026_05_03.md`

---

## 7. User next-step (decision points)

This is a **harvest task only** per the task brief — NO retraining attempted, NO savepoints deleted. The user has three forward paths (presented for completeness, NOT executed):

| Option | Cost | Wall | Completeness | Recommendation |
|---|---|---|---|---|
| (A) Retry on ubu1 with hardened watchdog (per-process tagging + 3-attempt retry + flock) | $0 | ~75 min wait + ~60 min train + retry budget | HIGH — answers the empirical question, addresses both root causes | **Rank 1** if user wants Paradigm J answer cheaply |
| (B) Move to RunPod H100 (per Paradigm D 50K cost analysis: $17.50 at half-scope, $27.50 at full 50K on H100 PCIe spot) | $17.50–$30 | ~14–22 h wall | HIGHEST — eliminates GPU-contention risk entirely | Rank 2 — better completeness but breaks $0 cap |
| (C) Defer Paradigm J indefinitely; lean on remaining paradigms (A/A'/B/C/D/E + Phase 1.6 baseline) | $0 | 0 | LOW — leaves theoretical-pluralism FEP hedge unvalidated | Rank 3 — only if budget/queue priorities preempt |

**Per "completion-quality recommendation" memory rule**: Rank 1 = Option A (hardened-retry on ubu1) — highest completeness within $0 cap, directly addresses both identified failure modes, preserves the sweet-spot-transfer question as the immediate next deliverable.

__END HANDOFF__
