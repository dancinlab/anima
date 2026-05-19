# Legacy H100 Tooling Audit — Phase 1 (2026-05-05)

Audit conducted as part of `BG-COST-WATCHDOG-PHASE1-IMPL` per spec
`docs/anima_h100_cost_discipline_operationalization_spec_2026_05_05.md` §3.1.

The Phase 1 deliverable introduces two new hexa scripts
(`tool/h100_cost_watchdog.hexa`, `tool/h100_idle_auto_killer.hexa`) plus two
bash helpers (`tool/h100_alert_emit.bash`, `tool/h100_register.bash`). Per
spec C8 the existing reclaim/cost tooling is overlapping; explicit
**retire / absorb / keep** decisions are required to avoid stale duplicate
logic.

## Files audited

### 1. `tool/h100_idle_guard.bash` (50 LoC, executable, May 30 2026)

- **Purpose**: launchd wrapper that chains `h100_pods_sync.bash` then
  `h100_auto_kill.hexa --apply`. Closes the 3-way gap from the
  2026-04-30 idle-burn incident (stale registry, dry-run-only kill,
  hexa darwin shim env).
- **Decision**: **KEEP (retain as launchd entry point)**.
- **Rationale**: this script is the launchd-supervised front door;
  retiring it would require a launchd plist swap (out of Phase 1 scope).
  The new `h100_cost_watchdog.hexa` is a **separate process** (poll-loop
  daemon, not a launchd one-shot) and its action ladder is alert→pause,
  not the binary STOP that `h100_idle_guard` performs. They occupy
  distinct lanes; both can run.
- **Phase 2/3 followup**: once watchdog has been smoke-tested (Phase 4),
  consider folding `h100_idle_guard.bash` into watchdog's "launchd
  selftest" mode and deprecating the standalone bash. Not this cycle
  (raw#15 additive).

### 2. `tool/h100_auto_kill.hexa` (~700 LoC, May 30 2026)

- **Purpose**: idle-pod reclaim. Probes each pod via SSH (nvidia-smi /
  who / tmux / heartbeat mtime), compares idle minutes to threshold,
  emits a STOP signal (`runpodctl stop pod <id>`) when `--apply` is set.
  Includes graceful SIGUSR2 ckpt-save before STOP.
- **Decision**: **KEEP (independent reclaim path)**.
- **Rationale**: the binary "idle for >N minutes → STOP" semantic is
  orthogonal to watchdog's "cost-overrun ladder" semantic. The auto-kill
  triggers on **inactivity** (training stalled / pod abandoned); the
  watchdog triggers on **cost** (target_usd × 2 / × 3). A pod can be
  active-but-overrunning (auto-kill SKIP, watchdog ALERT) or
  idle-but-cheap (auto-kill STOP, watchdog SKIP). Both are needed.
- **Phase 2/3 followup**: watchdog could subscribe to auto-kill's STOP
  events as an additional "pod went down" trigger (replacing the
  pod_get → 404 poll) but this would add coupling; defer.

### 3. `tool/h100_cost_tracker.hexa` (~800 LoC, Apr 24 2026)

- **Purpose**: per-round cost aggregator. Scans
  `state/h100_stage2_launch_state.json`, `state/convergence/h100_stage2_*.json`,
  computes per-attempt `cost = pods × bid × wall_hours`, emits SSOT to
  `state/h100_cost_tracker_result.json`. **Offline / batch** tool — does
  not call RunPod API.
- **Decision**: **KEEP (offline analysis tool, separate concern)**.
- **Rationale**: this is a post-hoc accounting / reconciliation tool —
  not a live watchdog. It reads launch-state SSOTs that the orchestrators
  already write and produces a round-level summary for cost retrospectives
  (e.g. "round 4 attempt 3 burned $X"). The new watchdog focuses on
  **live** cost stream (every-5-min ledger; cumulative spend per pod).
  These are complementary: tracker = retrospective rollup, watchdog =
  real-time alerting.
- **Phase 2/3 followup**: tracker could read watchdog's
  `state/h100_watchdog/ledger.jsonl` as an additional data source for
  pods that were not booted via clm_v4 / stage2 orchestrators
  (legitimate gap). Out of scope for Phase 1.

## Summary table

| File                         | Decision | LoC  | Reclaim path  | Phase     |
|------------------------------|----------|------|---------------|-----------|
| `tool/h100_idle_guard.bash`  | KEEP     | 50   | launchd one-shot | live   |
| `tool/h100_auto_kill.hexa`   | KEEP     | ~700 | inactivity STOP  | live   |
| `tool/h100_cost_tracker.hexa`| KEEP     | ~800 | offline rollup   | live   |
| `tool/h100_cost_watchdog.hexa` (NEW)     | ADD | ~150 | live poll + alert ladder | Phase 1 |
| `tool/h100_idle_auto_killer.hexa` (NEW)  | ADD | ~80  | overrun action ladder    | Phase 1 |
| `tool/h100_alert_emit.bash` (NEW)        | ADD | ~30  | pure-bash alert sink (avoids recursive Anthropic rate limit) | Phase 1 |
| `tool/h100_register.bash` (NEW)          | ADD | ~20  | orchestrator boot-time wrapper | Phase 1 |

**Net result**: 0 retire, 0 absorb, 4 net-new (additive per raw#15). The
three legacy tools occupy distinct lanes (launchd reclaim, inactivity STOP,
offline rollup) and each remains the authoritative implementation for its
lane. The new watchdog covers the **live cost-overrun + heartbeat-staleness +
BG-dead-pod-alive** lane — a gap not previously addressed.

## Honest C3 (audit-side, raw#10)

1. The decision to keep all three legacy tools is the conservative
   choice; an aggressive refactor could fold `h100_idle_guard.bash`
   into a watchdog `--launchd-mode` and reduce surface area, at the
   cost of cross-test scope blow-up.
2. The "complementary lanes" framing is partly post-hoc; in practice,
   the watchdog's idle-no-steps alert (§2.3) and auto-kill's
   nvidia-smi probe overlap. We accept the dual-coverage as redundancy.
3. The cost_tracker tool was never re-validated against the
   2026-05-04→05 Pβ incident data; if the round-level rollup misses
   the $54.72 idle burn (because the pod kept running past the
   "session_closed" timestamp), tracker output is stale by an
   open-ended margin. Watchdog ledger will provide a second data
   source for cross-check.
4. No legacy tool is currently called from a hot-path orchestrator
   (e.g., `clm_v4_lora_train_orchestrator.hexa`); they are all
   launchd / manual-invoke entry points. Phase 2 orchestrator patches
   add only **new** hooks (watchdog register + heartbeat + 404 poll).
5. The audit was performed by reading head-80 of each file and
   skimming the surrounding signature; we did not exhaustively trace
   every helper. A full call-graph audit could surface latent
   coupling (e.g., shared helper imports). Deferred to Phase 4 review.
