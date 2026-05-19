# Path A r=16 3-seed Retrain Progress (2026-05-04 05:52 UTC)

## TL;DR
- All 4 pods RUNNING (3 retrain + 1 base val). Watchdog PID 27807 alive (27 min, loop+apply, 600s poll).
- s42 step **5497/10000 (54.97%)**, s43 step **1644/10000 (16.44%)**, s44 step **1739/10000 (17.39%)**.
- Slowest: s44 at 2.69 s/iter. ETA 3/3 hub-pushed: **2026-05-04T12:08 UTC** (+16 min vs 11:52 prior).
- $0 verify-only run. No preemption. SSH OK on all 3 retrain pods.

## Per-pod health
| seed | step | %    | loss (last) | s/iter | epoch | GPU%  | mem MiB     | temp | ckpts saved          | ETA train done UTC |
|------|------|------|-------------|--------|-------|-------|-------------|------|----------------------|---------------------|
| s42  | 5497 | 54.97| 0.6171      | 2.55   | 3.50  | 82    | 27229/81559 | 47C  | ckpt-2000, ckpt-4000 | 09:04               |
| s43  | 1644 | 16.44| 0.6989      | 2.58   | 1.05  | 91    | 27089/81559 | 40C  | (none yet)           | 11:52               |
| s44  | 1739 | 17.39| 0.7245      | 2.69   | 1.11  | 99    | 27191/81559 | 53C  | (none yet)           | 12:03               |

s42 loss window mean (~30 steps): **0.644** — decreasing-noisy-stable trend.
s43/s44 are still in early phase (epoch ~1.05–1.11), losses comparable around 0.70 — healthy warmup tail.

## Cost burn (3 retrain pods only)
- Rate: $2.99/hr each.
- Spend so far: s42 $11.57 (3.87 h), s43 $3.38 (1.13 h), s44 $3.38 (1.13 h). **Total $18.33**.
- Projected at train done: s42 +$9.54, s43 +$17.91, s44 +$18.46. **Total to all-done $64.24**.
- Base val pod 8zbf9bfj6c63wg cost excluded per scope.

## ETA refinement
- Prior 3/3 ready: 2026-05-04T11:52Z.
- Refined 3/3 hub-pushed: **2026-05-04T12:08Z** (drift +16 min, slightly slower).
- Verdict UTC (assumes 90 min eval/seed):
  - parallel eval (3 pods): **13:38Z** (3h44m ahead of 17:22Z prior).
  - pure serial: **16:38Z** (44 min ahead of 17:22Z prior).
- Watchdog buffer: 16 h max_wait → ~10 h headroom past slowest s44 ETA.

## Watchdog
- PID 27807 alive, mode=loop, apply=true, poll_sec=600.
- Last poll 2026-05-04T05:41:57Z: s42/s43/s44 all MISSING (HF tags not yet pushed — expected since none are at step-10000).
- Log: `state/p9_path_a_r16_3seed_2026_05_04/watchdog_3seed_log.jsonl`.

## Caveats (raw#10)
1. SSH may transiently fail on network jitter; this snapshot succeeded all 3 retrain SSH.
2. Eval pod cost not yet incurred — will start when first seed's HF tag lands and watchdog triggers eval.
3. Watchdog max_wait=57600s gives ~10 h headroom past slowest seed's projected done (s44 12:03Z) — comfortable.

## Outputs
- `state/p9_path_a_r16_3seed_progress_2026_05_04/per_pod_health.json`
- `state/p9_path_a_r16_3seed_progress_2026_05_04/eta_refined.json`
- `state/markers/p9_path_a_r16_3seed_progress_2026_05_04.marker`
