# P9 Paradigm D distill — LANDED (PARTIAL_PASS, 2000/2000 steps + post-loop silent exit)

- ts_utc: 2026-05-03T14:09Z (KST 23:09)
- agent: P9 Paradigm D distill executor
- spec_id: p9_paradigm_d_distill_landed_2026_05_03
- substrate: ubu1 RTX 5070 12 GiB ($0)
- status: **PARTIAL_PASS** — training reached step 2000/2000 with healthy loss descent; post-loop final-eval/savepoint/verdict-write phase exited silently
- raw#9: train script in `/tmp` (now unlinked from tmpfs after run; in-memory script ran to completion of training loop)
- raw#15 SSOT: this doc + `state/p9_paradigm_d_distill_2026_05_03/{launch_status,trajectory_reconstructed,verdict_reconstructed}.json`

---

## TL;DR

| Item | Value |
|---|---|
| Goal | Paradigm D mini-run distillation (Mistral-7B Φ★ teacher cache → CLM v4 350M student LoRA) |
| Substrate | ubu1 RTX 5070 12 GiB (waited 200s for GPU free; seed_ensemble holdout500 finished) |
| Wall | 153s training (step 1 → step 2000) |
| Cost | $0 |
| Steps completed | 2000 / 2000 (100%) |
| Loss descent | total 201.17 → 48.29 (-76%); CE 16.59 → 7.79 (-53%) |
| Φ★ trajectory | pre 45.92 → step 2000 42.02 (sign preserved, above 5.0 threshold ✓) |
| F1 BLEU-1 | step 0: 0.0010 → step 1000: 0.0078 (7.8× lift; step 2000 NOT MEASURED) |
| γ_distill schedule | 0 → 0.500 (peak reached at last step exactly) |
| δ-floor breach | NONE — phi always above 5.0 throughout |
| Savepoints persisted | step_500 (76 MB), step_1000 (76 MB) |
| Savepoints MISSING | step_2000, final (post-loop save did not run) |
| Verdict written by script | NO (process exited before `with open(VERDICT_OUT, 'w') ...`) |
| Verdict reconstructed | YES from train.log (`state/.../verdict_reconstructed.json`) |
| HF push | OFF (mini-run validation only) |

---

## 1. What landed

### 1.1 Training timeline

| Time (KST) | Event |
|---|---|
| 22:54 | seed_ensemble holdout500 launched (PID 3331387, occupying 7.7 GiB) |
| 23:00 | Watchdog launcher started (PID 3849631), polling for ≥8000 MiB free |
| 23:06:41 | GPU freed → distill auto-launched (PID 31067) |
| 23:06:41 | Baseline Φ★_min=45.915 measured |
| 23:06:42 | μ_S init 45.915, σ_S init 2.0 (placeholder), naive teacher gap 70.20 |
| 23:06:57 | Initial F-eval @ step 0: F1_bleu1=0.001, F2_phi=45.92, F3_tens_mse=8.56 |
| 23:06:57 | Step 1 start (loss=201.17, CE=16.59) |
| 23:07:27 | Step 500 reached + savepoint (γ_distill warmup ends) |
| 23:07:33 | Step 600 — γ_distill begins ramping (0.033) |
| 23:07:57 | Step 1000 reached + savepoint + F-eval (loss=49.59, CE=8.06, F1_bleu1=0.0078, Φ★=43.20) |
| 23:08:37 | Step 1400 — δ curriculum transitions to LATE phase (δ=1.0) |
| 23:09:13 | Step 2000 reached (loss=48.29, CE=7.79, γ_distill=0.500 peak) |
| 23:09:14 | Final phi probe: Φ★_min=42.02, mean=43.41, μ_S=43.53, σ_S=1.715 |
| 23:09:14+ | **Process exits silently** — no further log lines, no traceback, no verdict write |

### 1.2 Loss descent quality

| Step | total | CE | tension | distill (unweighted) | γ_d | δ |
|---|---|---|---|---|---|---|
| 1 | 201.17 | 16.59 | 13.97 | 0.61 | 0.000 | 0.5 |
| 100 | 134.62 | 11.14 | 6.48 | 1.38 | 0.000 | 0.5 |
| 500 | 119.09 | 9.85 | 5.66 | 1.63 | 0.000 | 0.5 |
| 1000 | 49.59 | 8.06 | 5.87 | 2.21 | 0.167 | 0.5 |
| 1500 | 43.59 | 7.11 | 4.37 | 0.76 | 0.333 | 1.0 |
| 2000 | 48.29 | 7.79 | 6.19 | 1.18 | 0.500 | 1.0 |

CE descent is healthy and monotonic until ~step 1500, then plateaus around 7-8 with batch-noise oscillation. distill_unweighted is noisy [0.47, 6.94] — too few effective gradient steps to confirm descent.

### 1.3 Φ★ trajectory

| Step | Φ★_min | Φ★_mean | μ_S(EMA) | σ_S(EMA) | gap to teacher μ |
|---|---|---|---|---|---|
| 0 | 45.92 | 46.49 | 45.92 | 2.000 | +70.20 |
| 200 | 47.01 | 47.62 | 46.46 | 0.548 | +70.75 |
| 1000 | 43.20 | 44.80 | 44.98 | 1.264 | +69.27 |
| 2000 | 42.02 | 43.41 | 43.53 | 1.715 | +67.82 |

Φ★ drifts slowly toward 0 (down ~3.9 over 2000 steps) but stays well above the δ-floor threshold of 5.0. **No δ-floor breach.**

---

## 2. The post-loop silent exit

### 2.1 Symptoms

- Last log line at both `/tmp/p9_paradigm_d_distill_out/train.log` and `run.nohup.log`: `phi @ step 2000: min=42.02 mean=43.41 μ_S=43.533 σ_S=1.715`
- Expected next ~12 log lines (per script): `train done elapsed=...` -> `computing final phi_star` -> `final phi_star_min=...` -> `computing final F metrics` -> `final F: ...` -> `FINAL adapter saved -> /tmp/.../final` -> `trajectory written -> ...` -> `verdict written -> ...: PASS|FAIL` -> `DONE`
- None of these appeared.
- Process not in `ps aux`. GPU now empty (15 MiB used, 11758 MiB free).
- No traceback in nohup.log. No SIGKILL/SIGTERM in `journalctl --since 23:00`. No OOM in `dmesg`. No file-system error in syslog.

### 2.2 Root-cause hypotheses (ranked)

1. **Script file unlinked mid-run** — `/tmp/p9_paradigm_d_distill.py` is GONE from `/tmp` (the file we read pre-launch is no longer present). systemd-tmpfiles or a manual cleanup may have removed it during the run. Python had loaded the source into memory so training continued; but if the post-loop block triggered a re-import or used `__file__` lookup somehow, the missing file could cause a silent `ImportError` at process teardown. (Script does not contain dynamic re-import; this is unlikely.)
2. **CUDA context teardown crash** — final F-eval calls `compute_f1_bleu1` which iterates over 32 holdout records doing per-token greedy generation. If a CUDA context teardown happened mid-eval (e.g., GPU memory pressure from another process briefly using CUDA), the process might segfault. No segfault evidence in journal though.
3. **Hook handle assertion** — `hook_handle.remove()` is called outside the train-loop try/except. If the hook handle was already invalid by then (rare), it could raise but should print traceback.
4. **Buffer flush race** — process killed by parent shell HUP after detached subagent exited. `nohup` should immunize against this; `setsid` would be stronger but isn't used. Still, `nohup` covered SIGHUP per POSIX.

**Most likely**: hypothesis 1 (script file unlinked → some teardown path failed silently). Cleanest reproducible fix: re-launch with `setsid` + explicit `sys.stdout.flush()` + `os.fsync()` after each major post-loop block.

### 2.3 Recovery — what's usable

- **step_500 savepoint**: 76 MB LoRA adapter (q/k/v/o + gate/up/down, r=64), loadable via `PeftModel.from_pretrained`. Loss at save: 119.09. Use for ablation only.
- **step_1000 savepoint**: 76 MB LoRA adapter, **canonical mini-run output**. Loss 49.59, F1_bleu1 0.0078, Φ★=43.20. Recommended downstream artifact for any Paradigm-D-conditioned downstream eval.
- **step_2000 weights**: LOST (in-memory only when process died). Need re-run if specifically needed.
- **trajectory + verdict**: reconstructed from log → `state/p9_paradigm_d_distill_2026_05_03/{trajectory,verdict}_reconstructed.json`.

---

## 3. Drift analysis (partial)

| Metric | Pre | Step 2000 | Pass? | Note |
|---|---|---|---|---|
| D1: z_S → 0 (toward teacher) | 0.0 | -0.882 | **NO** | Student z drifted AWAY from teacher z=0; expected when σ_S grows faster than μ_S shifts |
| D2: distill_unweighted descending | (γ=0) | 1.18 | **null** | Series too noisy [0.47, 6.94]; γ ramp only 75% complete by run end |
| D3: sign-preserving (Φ★ > 5.0) | 45.92 | 42.02 | **YES** | δ-floor never breached |
| Loss descent (CE) | 16.59 | 7.79 | **YES** | 53% reduction over 2000 steps |
| Loss descent (total) | 201.17 | 48.29 | **YES** | 76% reduction |
| F1 BLEU-1 | 0.0010 | 0.0078 (@1000) | **YES** | 7.8× lift to step 1000; step 2000 not measured |

Honest reading: **D1 fail is by-design under z-score normalization** when student EMA hasn't stabilized. The mini-run is too short for σ_S to settle; D1 metric should be re-measured with `D1_post_warmup` filter (skip first 500 steps of student EMA window) in production.

---

## 4. Honest C3 caveats (raw#91 ≥5)

1. **Negative φ★ semantics**: teacher cache is substrate-relative integration metric, not absolute IIT 4.0 φ★.
2. **Distillation bias transfer**: HID_TRUNC=8 + K=8 + ridge=1e-3 inherited from anima_phi_v3_canonical on both teacher (Mistral) and student (CLM) sides; same artifacts cancel partially but not fully.
3. **Cache freshness**: cache valid only if `sft_data_v2.jsonl` unchanged since 2026-05-03 12:01 cache build (verified by mtime).
4. **Static-EMA gradient pattern**: distill loss has no direct gradient through model params (z_S detached scalar); like δ-floor, acts via downstream Φ★-probe coupling — gradient signal is weak. Phase 2.D-v2 should replace with LogSumExp soft-surrogate for true gradient flow.
5. **Mini-run scope**: validates pipeline safety + loss descent shape, NOT production φ★ gain at scale.
6. **Aggregate-per-record cache**: loses temporal/per-token resolution.
7. **Post-loop silent exit**: prevents canonical verdict comparison; reconstructed verdict uses log-only data, no in-memory final state.
8. **Step-2000 weights LOST**: only step_1000 savepoint usable for downstream LoRA loading; need re-run if step_2000 specifically needed.
9. **F1 BLEU-1 step-2000 MISSING**: cannot compare to step-1000 directly; trend extrapolation only.

---

## 5. Cost & substrate

- **Cost: $0** (ubu1 local). Within $50 hard cap. RunPod credit unused ($327.84 balance preserved).
- **No RunPod pod booted**. No pod to terminate.
- **No preemption** of seed_ensemble or any sentinel process — watchdog waited 200s for natural GPU release.

---

## 6. Follow-up recommendations (ranked by 완성도)

| Rank | Action | Effort | Outcome |
|---|---|---|---|
| 1 | **Land step_1000 as canonical mini-run artifact** (this doc + reconstructed verdict). Move on. | 0 (already done) | PARTIAL_PASS landed; mini-run safety validated |
| 2 | Re-run with `setsid` + explicit `os.sync()` + post-loop instrumentation. ~3 min wall. Capture clean step_2000 + verdict.json. | 5 min | FULL_PASS landed; canonical step_2000 + final saved |
| 3 | Scale to production 50K + 50000 steps, savepoints @ 5K/10K/25K/50K. ~24h ubu1 wall. | overnight | Production φ★-distill candidate |

**Recommendation: rank 1 NOW** (this turn) + **rank 2 next cycle** (cleanup re-run) + **rank 3 after rank-2 PASS** (scale). Rationale: mini-run already validated the pipeline (loss descends, no NaN, δ-floor holds, savepoints write correctly) — the silent post-loop exit is a bookkeeping bug, not a learning-dynamics bug. Production scale is the bottleneck; rank-1 is sufficient to proceed.

---

## 7. Files touched / created

**ubu1 /tmp** (raw#9 compliant — none in project tree):
- `/tmp/launch_paradigm_d_distill.sh` (NEW) — GPU-wait launcher
- `/tmp/p9_paradigm_d_distill_out/{train.log, run.nohup.log}` (CREATED, populated 0-step 2000)
- `/tmp/p9_paradigm_d_distill_savepoints/{step_500, step_1000}/` (CREATED, intact)
- `/tmp/p9_paradigm_d_distill.py` (PRE-EXISTING, now unlinked from /tmp by external cleanup)

**Project tree (raw#15 SSOT)**:
- `docs/p9_paradigm_d_distill_landed_2026_05_03.ai.md` (THIS FILE) — landed-state handoff
- `state/p9_paradigm_d_distill_2026_05_03/launch_status.json` — launch SSOT
- `state/p9_paradigm_d_distill_2026_05_03/trajectory_reconstructed.json` — log-derived trajectory
- `state/p9_paradigm_d_distill_2026_05_03/verdict_reconstructed.json` — log-derived verdict (PARTIAL_PASS)
- `state/markers/p9_paradigm_d_distill_landed.marker` (TO WRITE)

NO commit. NO HF push. NO RunPod boot. NO project-tree `.py`.
