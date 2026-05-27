# P9 A vs D Cross-Axis — DEFERRED 2026-05-04 (handoff)

## TL;DR

Cross-axis 4-cell verdict watchdog (PID 43833) **killed** at 2026-05-04T06:50:00Z. Reason: Path D 25K was killed earlier ($21.74 sunk), so no D verdict will arrive within the 24h cross-axis budget. Per spec sec.5, UNDETERMINED (missing axis) → WAIT → re-run after both land. Path A r=16 standalone verdict ships via sister watchdog PID 49397 unaffected.

## Watchdog Status (pre-decision snapshot)

| field | value |
|-------|-------|
| PID | 43833 |
| etime at decision | 01:18:18 |
| iter at decision | 16 |
| last poll | 2026-05-04T06:46:04Z |
| A state | WAIT:fallback_status_TRAINING_IN_PROGRESS_3SEED |
| D state | MISSING |
| max_wait_sec | 86400 (24h budget) |
| poll_sec | 300 |

## Options Ranked by 완성도 Lens

### Rank 1 (CHOSEN): OPTION_3_CANCEL_AND_DEFER
- **Reasoning**: Honors spec sec.5 (UNDETERMINED → WAIT). 4-cell matrix is canonical SSOT (raw#15); single-axis emit fabricates labels not in falsifier set. Cancellation releases poll slot; cross-axis re-armed when D fresh attempt is committed in next cycle.
- **Trade-off**: 4-cell verdict deferred. Acceptable: spec already defines this as the correct terminal for missing-axis.

### Rank 2: OPTION_1_WAIT_FOR_D_RELAUNCH
- **Reasoning**: Extends timeout to 7d. Problem: D re-launch is unscheduled (D 25K killed = sunk cost; no commission decision in this cycle). Watchdog wait without launch commitment = dead-poll.
- **Blocker**: `watchdog_loop.sh` is orphan inode (source file deleted post-launch). Live-patching max_wait would require respawn anyway → equivalent to option 3 + later manual respawn.

### Rank 3: OPTION_2_A_ONLY_EMIT
- **Reasoning**: VIOLATES spec sec.5 4-cell matrix. Cells II/IV both require D verdict (PASS or FAIL_D explicitly). Synthesizing a single-axis verdict by collapsing one axis to NULL fabricates a label not in the spec's falsifier set. Patching cross-axis hexa would corrupt SSOT (raw#15) for all future cycles.

## Action Taken

1. `kill 43833` → PID terminated 2026-05-04T06:50:00Z (verified `ps -p 43833` returned no rows, exit_code=1)
2. Decision artifacts written: `state/p9_a_d_cross_axis_decision_2026_05_04/{decision.json, action_log.jsonl}`
3. Marker landed: `state/markers/p9_a_d_cross_axis_deferred.marker`

## Non-Actions (Explicit)

- **DID NOT** preempt Path A pods (`pvkyhb0lb87ydu`, `0jetjpvlm51zoy`, `nzw0btc8br78yy`) — 3-seed retrain continues per Track B
- **DID NOT** spawn replacement cross-axis watchdog — defer until D re-commission
- **DID NOT** patch cross-axis hexa — preserves SSOT integrity per raw#15

## Sister Watchdogs (UNAFFECTED)

- **PID 49397**: Path A r=16 completion watchdog (`tool/path_a_r16_completion_watchdog.hexa --loop --apply`) → continues; will emit single-seed verdict when `mitigation_comparison.json` lands
- **PID 53327**: D 25K watchdog v2 wrapper → continues but D verdict file is absent and no D pod active; effectively idle until D re-commission
- **3-seed amend retrain**: in-pod training PIDs 220 (s43, s44) + watchdog 91788 (s42) continue per Path A r=16 3-seed verdict (`state/p9_path_a_r16_3seed_2026_05_04/verdict.json`); ETA verdict ~13:26 UTC

## Re-Arm Recipe (next cycle)

When D fresh attempt is commissioned:
1. Verify D verdict file path target (likely `state/p9_paradigm_d_25k_eval_2026_05_03_verdict.json` or refreshed path)
2. Re-derive `watchdog_loop.sh` from landing doc `docs/p9_a_d_cross_axis_completion_watchdog_landed_2026_05_04.ai.md` (orphan inode — source must be regenerated)
3. Spawn: `nohup bash state/p9_a_d_cross_axis_2026_05_04/watchdog_loop.sh > .../watchdog_nohup.log 2>&1 &` with max_wait sized to D ETA + 4h buffer
4. Verify A axis is also still terminal (or re-WAIT if A has rolled over to a new cycle as well)

## raw#10 Caveats (3 explicit)

- **C1** — defer is open-ended. Re-arm requires D re-commission decision which is OUT OF SCOPE for this decision. If operator chooses NOT to re-launch D this cycle, cross-axis 4-cell verdict for current Path A r=16 cohort will never compute. Path A standalone verdict still ships via PID 49397.
- **C2** — `watchdog_loop.sh` is orphan inode (source file deleted post-launch); re-arming requires regenerating the script from landing-doc recipe before next spawn.
- **C3** — Path A r=16 single-seed verdict is already PARTIAL evidence. The 3-seed retrain is in progress to address F-PATHA-MITIGATION-1 caveat #4 (landing band [-0.5, +0.5] needs 3-seed amend). When 3-seed verdict lands (~13:26 UTC), the A axis upgrades from PARTIAL → terminal regardless of D. Cross-axis can then be re-armed against the upgraded A verdict + (eventual) D verdict in a future cycle.

## Spend Impact

**$0** — Mac-side decision + kill + file writes only. No GPU rentals affected.

## Constraints Honored

- **raw#9**: Mac-side hexa-only — no GPU spend, no pod operations, kill is OS-level supervisor action
- **raw#15**: SSOT preserved — cross-axis hexa unchanged, spec sec.5 4-cell matrix unchanged
- **raw#10**: 3 caveats explicit (above)
- **No Path A pod preemption**: Path A 3-seed retrain continues uninterrupted
