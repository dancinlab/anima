# P9 Path A r=16 3-seed Progress Poll #2 — 2026-05-04 06:38 UTC

## TL;DR

3/3 pods RUNNING and progressing. Watchdog PID 27807 alive. ETA ready_3of3 = **11:56 UTC** (ahead of progress1 by 11min). Verdict ETA **13:26-16:26 UTC** (within prior 13:38-16:38 window).

**raw#9/15/$0 honored**: observe-only, no preempt, no kill, no spend beyond running pods.

## Per-Pod Snapshot

| Seed | Step | % | Loss(mean) | sec/it | GPU% | Temp | Ckpts | Train ETA | Hub ETA |
|------|------|---|-----------|--------|------|------|-------|-----------|---------|
| s42  | 6557/10000 | 65.6 | 0.615 | 2.65 | 83 | 51C | 2k/4k/6k | 09:10 UTC | 09:15 UTC |
| s43  | 2770/10000 | 27.7 | 0.743 | 2.60 | 100 | 40C | 2k | 11:51 UTC | 11:56 UTC |
| s44  | 2929/10000 | 29.3 | 0.660 | 2.20 | 100 | 51C | 2k | 10:57 UTC | 11:02 UTC |

**Slowest = s43** → ready_3of3 = 11:56 UTC

## Loss Trends (vs progress1 poll @ 05:52 UTC)

- s42: 0.6440 → 0.6150 (↓ 0.029) — healthy, late-mid training stable-noisy
- s43: 0.6989 → 0.7432 (↑ 0.044) — early-epoch noise (expected; only 1 datapoint in prev poll)
- s44: 0.7245 → 0.6600 (↓ 0.065) — healthiest trajectory; fastest sec/iter (2.20)

## Throughput Delta (45.85 min elapsed since progress1)

- s42: +1060 steps (23.1 steps/min)
- s43: +1126 steps (24.6 steps/min)
- s44: +1190 steps (26.0 steps/min) ← fastest

## Cost Burn

- Spent so far: **$25.11** (+$6.78 vs progress1)
- Burn rate: **$8.97/hr** (3 pods × $2.99/hr)
- Projected cumulative to train_done (slowest = s43): **$61.22**
- Base val pod excluded from this scope

## ETA Refined

- ready_3of3: **11:56 UTC** (slowest = s43)
- Verdict UTC (parallel eval, 90min): **13:26 UTC**
- Verdict UTC (serial eval, 270min): **16:26 UTC**
- Both within user's prior window (13:38-16:38 UTC); parallel-path ahead by 11min vs progress1

## Watchdog Status

- PID 27807 alive, etime 01:14:30, mode=loop apply=true
- Last poll: 06:32:06 UTC (10min cadence)
- ready_count_latest: 0/3 (expected — no seed at step-10000 yet)
- max_wait: 57600s (16h from 05:21 UTC start = 21:21 UTC) → 9h25m headroom past ready_3of3 ETA

## Constraints Honored

- raw#9/15/$0: observe-only ✓
- raw#10 caveats acknowledged:
  1. SSH transient jitter — all 3 succeeded on 2nd attempt
  2. log path = `<output-dir>/train.log` (not `/workspace/train.log`) — corrected
  3. watchdog ready_count=0 expected at this stage

## Next Poll Recommendation

Suggest next poll at **08:30-09:00 UTC** to catch s42 train_done (~09:10 UTC) and verify push_to_hub success on s42 hub repo.

## Files

- per_pod_health.json — full snapshot data
- eta_refined.json — refined ETA + cost projections
- marker (state/markers/) — completion marker
