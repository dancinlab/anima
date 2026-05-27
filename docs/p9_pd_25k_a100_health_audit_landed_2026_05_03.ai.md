# P9 Paradigm D 25K A100 — Health Audit (LANDED)

**ts_utc**: 2026-05-03T21:50:00Z
**pod_id**: `7ubgzj4s8spb4p`
**verdict**: POD_ALIVE_BUT_NOT_TRAINING

## TL;DR

Pod alive (RUNNING, 5.98h since create), but training **never started**. Container restart at ~21:30 UTC (5h 39m after pod create) wiped /workspace; rsync re-transfer in progress (52.7% of best.pt at 1.37 MB/s, ETA ~40 min). GPU idle (0% util). No savepoints exist (resume scaffolding unexercised). Current spend $4.72 — projected total $19+ exceeds $14.50 watchdog and $17 hard cap.

## Key findings

| Metric | Value |
|---|---|
| Pod status | RUNNING |
| Pod uptime since create | 5.98h |
| Container age (since restart) | 19.4 min |
| Training process alive | **NO** |
| Watchdog alive | **NO** |
| GPU utilization | **0%** |
| GPU memory used | 0 MiB / 81920 MiB |
| Current step | n/a (not started) |
| Loss trajectory | n/a |
| Bundle transfer | 52.7% (best.pt 2829/5366 MB) |
| Recent rsync rate | 1.37 MB/s (slow) |
| Bundle ETA | ~40 min |
| Savepoints | 0 |
| Resume scaffolding exercised | **NO** |
| HF token on pod | **NO** |
| Current spend | **$4.72** |
| Projected total (if no further preempt) | **$19.47** → exceeds caps |

## Container restart evidence

- `/proc/1` jiffies (1108449867) vs host uptime (11085665s) → container started 21:30:25 UTC
- Pod created 15:51:30 UTC → 5h 39m gap = container restart, not original boot
- `/workspace` contents: only `.best.pt.6lK6Q0` (rsync temp) + `launch_a100_distill.sh` (created 21:37 post-restart)
- Missing: `p9_paradigm_d_distill_v2.py`, `distill_watchdog.sh`, all training data, `models/conscious_decoder.py`, savepoints, logs
- `/dev/md1` mounted xfs at /workspace (100GB persistent) — but volume effectively reset

This is consistent with **community spot preempt** behavior. Volume was nominally persistent but contents lost.

## Cost projection (3 options, ranked by 완성도)

### A. WAIT — let bundle finish + A100 train to 25K
- Bundle ETA: 40 min ($0.53)
- Training ETA: 18h ($14.22)
- **Total: $19.47** → overruns watchdog by $4.97 → **watchdog will kill at $14.50** before completion
- 완성도: LOW — guaranteed mid-training kill

### B. ABORT NOW — terminate pod, re-launch on H100 PCIe when stock
- Save remaining $0.79/hr immediately
- Sunk cost: $4.72
- Re-launch on H100 PCIe ($1.59/hr) × 10h = $15.90
- **Total: $20.62** (vs A's $14.50 partial) — but A produces incomplete model
- 완성도: HIGH — achieves 25K completion; H100 less preempt-prone in secure tier
- **Caveat C3**: H100 PCIe community supply likely also constrained; secure tier $2.49/hr

### C. RAISE CAP — bump watchdog to $20, hard cap $22, let A100 complete
- Same projected total $19.47, but no premature kill
- 완성도: MEDIUM — completes if no further preempt; second preempt would cascade
- **Caveat C3**: 1 preempt in 6h suggests ~16% hourly preempt rate → 18h × 16% = high probability of further preempts wasting more cost

### Recommendation (완성도 lens): **B → ABORT and re-launch on H100 secure**
H100 secure $2.49/hr × 10h = $24.90 — exceeds caps but **deterministic completion**. If $17 cap is hard, fall back to A100 with raised cap (option C) and accept ~30% probability of further preempt.

## Resume status

- Scaffolding present in script (per v2 1071 LoC)
- Not exercised: 0 savepoints exist
- First savepoint planned at step 1000 (per resume granularity spec)
- HF token absent → first savepoint cannot push to HF

## Three honest C3 caveats (raw#10)

1. **Preempt unpredictable on community spot** — observed 1 preempt in 6h on this pod; A100 community supply varies hour-to-hour; further preempts would compound waste.
2. **Resume scaffolding not yet exercised** — script has resume code but never tested with actual savepoint; first real test would be next preempt after step 1000.
3. **A100 1.5-2× slower than H100** — wall_max 18h set for A100, but at $0.79/hr × 18h = $14.22 train cost alone exceeds $14.50 watchdog after the $4.72 sunk cost. Math doesn't close even on first attempt.

## Artifacts

- `state/p9_pd_25k_a100_health_audit_2026_05_03/health.json`
- `state/p9_pd_25k_a100_health_audit_2026_05_03/cost_projection.json`
- `state/p9_pd_25k_a100_health_audit_2026_05_03/resume_status.json`
- `state/markers/p9_pd_25k_a100_health_audit_landed.marker`

## Decision required

User must choose between (A) wait + accept watchdog kill, (B) abort + re-launch H100, or (C) raise cap + accept preempt risk. Per constraint, NO action taken — pure monitoring. Cost is currently $4.72 and growing at $0.79/hr.
