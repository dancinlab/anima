# anima self-monitor cron — W1 Phase 6 trip-wire (2026-05-02)

## 1. Mission

W1 anima-self Φ axis closed Phase 5 (`docs/W1_phase5_window_recheck_results_2026_05_01.md`)
with composite verdict **ARTIFACT_PERMANENT_DOWNGRADE**: the rising slope at
W=20 is a sliding-window estimator artifact at n=15 < W. Phase 5 §7 prescribes
the only $0 path forward — accumulate ≥ 20 cron ticks and re-run the four
phases. This monitor is the trip-wire that fires Phase 6 the instant the
threshold is crossed, so we don't poll H100 cycles or human attention.

## 2. Snapshot at creation

Counted from `state/proposals/meta/cycle_log.jsonl` (unique `cycle_id` with
`name=cycle_done`):

| Metric | Value |
|---|---|
| n_ticks observed | **15** (matches W1 Phase 5 §1 cited n) |
| Threshold (Phase 6 unlock) | 20 |
| Remaining ticks | **5** |
| First tick (UTC) | 2026-04-22T13:12:53Z |
| Last tick (UTC) | 2026-05-02T01:49:32Z |
| Span | 9.53 days |
| Mean inter-tick | 17.6 h (small-sample) |
| Median inter-tick | **12.0 h** |
| ETA to n=20 (median) | **~2.5 days** (≈ 2026-05-04 night) |
| ETA to n=20 (mean) | ~3.7 days (≈ 2026-05-05) |

## 3. Components

| Path | Role |
|---|---|
| `tool/anima_self_monitor.hexa` | HEXA-only monitor (NEW). modes: `--status` / `--check` / `--selftest`. |
| `config/launchd/com.anima.self_monitor.plist` | hourly launchd plist (template, user installs). |
| `state/anima_self_monitor_cron_2026_05_02/spec.json` | frozen spec snapshot. |
| `state/anima_self_monitor_cron_2026_05_02/last_check.json` | most recent poll result. |
| `state/anima_self_monitor_cron_2026_05_02/last_alert.json` | idempotency cookie (prevents double-fire). |
| `state/anima_self_monitor_alert.jsonl` | append-only alert sink (load-bearing for Phase 6 launcher). |

## 4. Monitor functions (HEXA + helper python)

- `count_cron_ticks()` — read `state/proposals/meta/cycle_log.jsonl`, return
  count of unique `cycle_id` with `name=cycle_done`. Robust to mojibake bytes
  via `errors='replace'`.
- `check_threshold_n_20(n)` — `n >= 20`.
- `trigger_w1_phase_6_rerun(n, last_ts)` — emit JSON payload with `rerun_spec`
  `{modulus: 1024, windows: [5, 7, 20], expected_outcomes: ['REAL_SIGNAL', 'ARTIFACT_PERMANENT_DOWNGRADE_CONFIRMED']}`.
- `notify(payload)` — append to `state/anima_self_monitor_alert.jsonl`,
  write `last_alert.json`. Idempotent: never re-fires for the same `n_ticks`.

## 5. launchd install (manual)

```
cp config/launchd/com.anima.self_monitor.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/com.anima.self_monitor.plist
launchctl enable gui/$UID/com.anima.self_monitor
launchctl kickstart -k gui/$UID/com.anima.self_monitor   # first poll now
```

Tear-down:
```
launchctl bootout gui/$UID/com.anima.self_monitor
rm ~/Library/LaunchAgents/com.anima.self_monitor.plist
```

`StartInterval = 3600s` — hourly is overkill (median 12h between ticks) but
the run is idempotent and < 1s wall, so cost is ~0. Each hourly run rewrites
`last_check.json`; alerts only emit on the first run that observes `n >= 20`.

## 6. W1 Phase 6 trigger spec (downstream contract)

When `state/anima_self_monitor_alert.jsonl` gains a record with
`event = "w1_phase_6_trigger"`:

1. Launch `/tmp/W1_phase6/window_recheck.py` (off-repo, $0) — same engine as
   Phase 5 driver but with `modulus = 1024` slot-projection added to the axis
   join, and re-run for W ∈ {5, 7, 20} on the new n ≥ 20 trace.
2. Inputs: rebuild Phase 2 trace (`state/W1_phase6_full_19axis_<DATE>/phi_trace_full.jsonl`)
   from the now-saturated `cycle_log.jsonl`. mod-1024 = `state_hash & 1023`
   used as the per-tick categorical for Φ_proxy state-space cardinality.
3. Cross-validation criterion (frozen):
   - **REAL_SIGNAL** ⇔ at all three W ∈ {5, 7, 20}, observed slope is positive
     AND z > +2 against state-hash shuffle null (N=1000, seed=42+W).
   - **ARTIFACT_PERMANENT_DOWNGRADE_CONFIRMED** ⇔ slope sign still
     W-dependent OR observed below null at any W (i.e., Phase 5 pattern persists).
4. Outcome update path: §30 roadmap W1 axis status flips PENDING → either
   PASS (REAL_SIGNAL) or PERMANENT_DOWNGRADE_CONFIRMED.

## 7. Honest C3

1. **Cron tick is a coarse Φ proxy substrate.** The cycle_log records meta
   propose/refine/score steps, not a clean stochastic process. Even at n=20,
   the `cycle_id` cardinality will still be ≤20 distinct hashes; the W=20
   window saturates exactly once. Phase 6 will tell us whether the slope
   sign is W-stable, not whether the underlying Φ estimator has converged
   in distribution. A truly clean reading needs n ≫ W, e.g. n ≥ 100.
2. **Median inter-tick = 12 h is a small-sample estimate.** With only 13
   intervals the median ETA (3 days) has wide uncertainty; the recent run
   shows tight clustering (the last 5 ticks all landed within ~6 h spans),
   while older intervals span days. Real ETA could be anywhere in [2 d, 7 d].
   The hourly cron is conservative against this.
3. **Idempotency is per-n, not per-event.** `last_alert.json` keys on
   `n_ticks_at_alert`. If a manual cycle backfill drops n below 20 then back
   above, a second alert *would* fire. This is intentional — re-crossing the
   threshold is itself signal — but worth flagging since a downstream Phase 6
   launcher must be safe to invoke twice.

## 8. Artifacts

- `tool/anima_self_monitor.hexa` (NEW)
- `config/launchd/com.anima.self_monitor.plist` (NEW, template)
- `state/anima_self_monitor_cron_2026_05_02/spec.json` (frozen snapshot)
- `state/anima_self_monitor_alert.jsonl` (created on first `--check` after threshold)
- This SSOT.
