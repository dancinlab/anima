# VLM Stage1 Progress Monitoring — Landed 2026-05-04

## Cycle
Sister BG launched VLM stage1 (ubu1 RTX 5070, PID 31960, 50k steps, ETA 5.4-5.6h).
This cycle: health check + tail-watchdog setup + first HF mid-train backup.

## Health Snapshot (2026-05-04T14:18 KST)
- PID 31960 alive, elapsed 46m, CPU 12.6%, MEM 9.5%
- Step 7450 / 50000 (14.9%)
- Loss 8.55 (decreasing from 8.78 at step 5k)
- sps 2.66 (steadily climbing from 2.61)
- ETA refined: 4.4h remaining, 5.0h total (vs initial 5.4-5.6h)
- GPU: 883/12227 MiB (7.2%), util 17%, 51°C — ample headroom

## Watchdog (caveat #3 mitigation)
- Script: `/tmp/vlm_stage1_tail_watchdog.sh` (raw#9: ubu .sh permitted)
- PID 3436596, interval 30s
- Patterns: Traceback | Killed | OOM | CUDA out of memory | RuntimeError | Segmentation
- Alert log: `/tmp/vlm_stage1_watchdog_alert.log`
- Exits with code 1 (PID gone) or 2 (pattern hit), logs latest savepoint path

## First HF Push (step-5k)
- Local: `/tmp/vlm_stage1_savepoints/step-5k/` (332KB: adapter_config + adapter_model + README)
- LoRA r=8 alpha=16 dropout=0.05 on [wq, wk, wv, wo, intent_proj] confirmed
- HF repo: `dancinlab/vlm-anima-voice-paradigm-stage1-step-5k` (HTTP 200, paradigm prefix per mk2 amendment)
- Commit: "VLM stage1 step-5k LoRA savepoint (loss=8.78, sps=2.61)"

## Next Savepoint Schedule
- step-10k: ETA ~35 min
- step-15k: ETA ~70 min
- step-25k: ETA ~140 min
- step-50k (final): ETA ~270 min (~4.5h)

## 4 Caveats (raw#10)
1. **Tail-watchdog blind spots**: SIGSEGV / OOM-killer / torchcodec C-level crashes may exit without stderr write — watchdog catches PID disappearance fallback only after train process gone
2. **HF push timing race**: if savepoint write + HF push overlap with next train step's checkpoint write, atomicity not guaranteed (mitigation: push from frozen step-Nk dir, never in-flight)
3. **RTX 5070 12GB OOM future risk**: currently 7.2% util, but if loss-aware grad-norm spikes or seq-len adapts upward, could approach ceiling — watchdog catches `CUDA out of memory` pattern
4. **5k savepoint maturity**: loss=8.78 may be borderline for downstream eval; recommend waiting for step-15k or step-25k for first usable adapter — step-5k pushed for resumption insurance, not deployment

## Outputs
- `state/vlm_stage1_progress_2026_05_04/health.json`
- `state/vlm_stage1_progress_2026_05_04/savepoint_backup.json`
- `state/markers/vlm_stage1_progress_monitoring_2026_05_04.marker`
- `/tmp/vlm_stage1_tail_watchdog.sh` (ubu1)
- HF: `dancinlab/vlm-anima-voice-paradigm-stage1-step-5k`

## Constraints Honored
- raw#9 STRICT: Mac → no .sh; ubu1 .sh permitted (watchdog written on ubu1 only)
- raw#15: no preemption (training continues uninterrupted, monitoring read-only)
- raw#10: 4 caveats explicit
- $0: HF push uses existing token, watchdog is shell-only
- DO NOT preempt: confirmed PID 31960 elapsed time still climbing post-cycle
