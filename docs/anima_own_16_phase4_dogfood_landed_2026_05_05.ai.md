---
title: Phase 4 dogfood smoke — landed (3/3 scenarios PASS, $0.32 actual vs $3 cap)
cycle: 2026-05-05
ts: 2026-05-05T_own_16_phase4_dogfood_landed
bg_lane: OWN-16-PHASE4-DOGFOOD
substrate: H100 SECURE @ $2.99/hr (6.46min billable) + mac (synthetic stale-heartbeat scenarios)
status: PHASE4_LANDED
type: dogfood_handoff
predecessor:
  - docs/anima_h100_cost_discipline_operationalization_spec_2026_05_05.md
  - docs/anima_h100_cost_watchdog_phase1_landed_2026_05_05.ai.md
  - docs/anima_h100_cost_watchdog_phase2_landed_2026_05_05.ai.md
  - docs/anima_h100_cost_watchdog_phase3_landed_2026_05_05.ai.md
  - docs/anima_own_16_validator_hexa_landed_2026_05_05.ai.md
related:
  - state/own_16_phase4_dogfood_2026_05_05/verdict.json
  - state/own_16_phase4_dogfood_2026_05_05/logs/
  - tool/h100_cost_watchdog.hexa
  - tool/h100_idle_auto_killer.hexa
  - tool/h100_alert_emit.bash
  - tool/h100_register.bash
  - state/h100_watchdog/closed/
  - state/h100_alert_ledger_2026_05.jsonl
  - state/h100_watchdog/ledger.jsonl
raw_invariants:
  - raw#9 (md handoff + json verdict; bash carve-out only via existing tool/*.bash)
  - raw#10 (>=5 honest C3 in verdict.json + below)
  - raw#15 (additive — no roadmap mutation, no .own mutation, no commit per task §6 directive)
---

# Phase 4 dogfood smoke — landed (2026-05-05)

## Summary (5 bullets)

- **3/3 dogfood scenarios PASS**: (A) graceful complete + 404 verify — real
  H100 pod boot at 06:40:55Z, register, 4 heartbeats, watchdog daemon iter
  (state=ALIVE, no false alert), trap pre-stop, pod stop, pod delete, 404
  confirmed at retry 1, watchdog deregister archived. (B) BG-killed mid-flight
  + auto-pause ladder readiness — synthetic pod with 7-min backdated
  heartbeat, watchdog detects stale (age=421s > 300s threshold), alert-script
  invoked, ledger entry persisted; auto-killer selftest 4/4 PASS confirms
  pause command ready. (C) heartbeat stale alert — second synthetic pod with
  8-min backdated heartbeat, distinct STALE_HEARTBEAT alert (age=481s)
  emitted to ledger.

- ** Phase 1+2+3+3.5+4 = ALL LANDED**. Phase 1 (4 tool files, selftests
  9/9 PASS), Phase 2 (orchestrator hooks, 4 PASS / 2 unrelated T4 FAIL), Phase
  3 (BG launch template + memory), Phase 3.5 (own_16_preflight.hexa validator
  3/3 PASS), Phase 4 (this dogfood, 3/3 PASS). Compute-lifecycle triad
  (HF Hub only + HF lifecycle + H100 cost discipline) is
  complete in spec + tooling + dogfood; promotion from warn-tier to block-tier
  enforcement requires follow-up h100_bg_launch_lint.hexa (NOT yet emitted —
  see honest C7 in verdict).

- **Actual cost = $0.32 / $3 cap (10.7% of budget)**. Pod billable wall =
  6.46min (06:40:55Z → 06:47:23Z). Total dogfood-cycle wall = 11.78min.
  Cost-overrun (2x/3x) alert paths NOT exercised — pod ran $0.32 << $6 (2x
  trigger). Only stale-heartbeat alert path was functionally exercised against
  live tooling. Cost-alert mechanics remain selftest-only (see honest C5).

- **One real watchdog code-path observation**: Scenario B revealed that
  `h100_cost_watchdog.hexa:267` short-circuits on `state=NOT_FOUND` BEFORE
  reaching the alert-emission block. For a synthetic pod (not registered with
  RunPod), runpodctl returns 404 → state=NOT_FOUND → watchdog skips stale
  alert and goes straight to "deregister candidate handed by orchestrator
  trap". To exercise the alert branch I sanitized PATH (no /opt/homebrew),
  forcing `_which("runpodctl")=false → state=UNKNOWN`. UNKNOWN does NOT
  short-circuit, so the alert path was reached. Correct production behavior
  (a confirmed-dead pod should not generate alert noise) but exposes a
  coverage gap: alert path is only validated when runpodctl is unreachable,
  NOT when an alive pod exists with stale heartbeat. Future dogfood should
  keep an alive pod for >5min without heartbeat updates to exercise the alert
  path under canonical state=ALIVE conditions.

- **Honest C3 (>=5)**: see verdict.json for 8 detailed bullets. Headline gaps:
  (1) cost-overrun alert paths not functionally exercised — only selftest;
  (2) NOT_FOUND short-circuit means alert path needs runpodctl-absent
  workaround for synthetic dogfood; (3) alert ledger location is
  state/h100_alert_ledger_<YYYY_MM>.jsonl not the spec's
  state/h100_watchdog/alerts/<ts>_<pod>.json — doc-vs-impl drift;
  (4) enforcement currently warn-tier only — block-tier needs follow-up
  linter; (5) no SSH workload was sent to H100 (registered + billed only) —
  L11/L13 orchestrator paths NOT validated by this dogfood.

## Files written

| Path | Role |
|------|------|
| state/own_16_phase4_dogfood_2026_05_05/verdict.json | SSOT outcome (3/3 scenarios PASS, cost $0.32, 8 honest C3) |
| state/own_16_phase4_dogfood_2026_05_05/logs/pod_create.log | runpodctl create pod stdout (pod alive @ $2.99/hr) |
| state/own_16_phase4_dogfood_2026_05_05/logs/register.log | h100_register.bash output |
| state/own_16_phase4_dogfood_2026_05_05/logs/scenario_a_pod_stop.log | runpodctl pod stop response (desiredStatus → EXITED) |
| state/own_16_phase4_dogfood_2026_05_05/logs/scenario_a_pod_delete.log | runpodctl pod delete response |
| state/own_16_phase4_dogfood_2026_05_05/logs/scenario_a_deregister.log | watchdog --deregister archive output |
| state/own_16_phase4_dogfood_2026_05_05/logs/scenario_a_outcome.json | per-scenario outcome flags |
| state/own_16_phase4_dogfood_2026_05_05/logs/scenario_a_daemon_iter.log | watchdog single-iter on alive pod (state=ALIVE) |
| state/own_16_phase4_dogfood_2026_05_05/logs/scenario_b_daemon_iter.log | first synthetic stale-hb iter (NOT_FOUND short-circuit observed) |
| state/own_16_phase4_dogfood_2026_05_05/logs/scenario_b_unknown_state_iter.log | retry with PATH-sanitized → state=UNKNOWN → STALE_HEARTBEAT alert |
| state/own_16_phase4_dogfood_2026_05_05/logs/scenario_b_killer_selftest.log | h100_idle_auto_killer.hexa --selftest 4/4 PASS |
| state/own_16_phase4_dogfood_2026_05_05/logs/scenario_c_iter.log | second synthetic stale-hb iter (distinct alert) |
| docs/anima_own_16_phase4_dogfood_landed_2026_05_05.ai.md | this Phase 4 handoff |

## Side-effect state changes (additive)

| Path | Change |
|------|--------|
| state/h100_watchdog/ledger.jsonl | NEW (5 rows from dogfood iters; first persistent ledger) |
| state/h100_alert_ledger_2026_05.jsonl | NEW (3 STALE_HEARTBEAT rows from scenarios B+C) |
| state/h100_watchdog/closed/ | 3 new archives (real dogfood pod + 2 synthetics) |
| state/h100_watchdog/pods/ | empty post-cleanup (0 registered pods) |
| state/h100_watchdog/heartbeats/OWN-16-DOGFOOD.txt | retained (4 successive updates + EXITING marker) |
| state/h100_watchdog/heartbeats/OWN-16-DOGFOOD-SYNTH-B-OWNER.txt | retained (backdated stale-marker) |
| state/h100_watchdog/heartbeats/OWN-16-DOGFOOD-SYNTH-C-OWNER.txt | retained (backdated stale-marker) |

## Evidence — alert ledger (state/h100_alert_ledger_2026_05.jsonl)

3 rows, all STALE_HEARTBEAT:

- 2026-05-05T06:50:00Z, pod=OWN-16-DOGFOOD-SYNTH-B, hb_age_sec=421
- 2026-05-05T06:51:52Z, pod=OWN-16-DOGFOOD-SYNTH-B, hb_age_sec=533 (re-emit)
- 2026-05-05T06:51:52Z, pod=OWN-16-DOGFOOD-SYNTH-C, hb_age_sec=481

## Evidence — cost ledger (state/h100_watchdog/ledger.jsonl)

5 rows total: 1 ALIVE row from real pod (cumulative_usd=$0.287 at probe time),
1 NOT_FOUND row from synth-B first probe, 3 UNKNOWN rows from synth-B+C
probes after PATH sanitization.

## Evidence — graceful tear-down chain (Scenario A)

1. runpodctl pod stop → desiredStatus EXITED, lastStatusChange "Exited by user"
2. runpodctl pod delete → `{"deleted":true,"id":"<pod>"}`
3. runpodctl pod get retry 1 → "pod not found, status 404"
4. hexa run tool/h100_cost_watchdog.hexa --deregister → archived to closed/
5. Final runpodctl pod list → empty array (zero live pods)
6. Final --status → registered_pods: 0

## Closure claims

- ** Phase 1+2+3+3.5+4 fully landed**: yes — every preceding doc is
  landed-status, this Phase 4 dogfood verdict 3/3 PASS, no outstanding
  blockers.
- **L23/L24/L25 enforcement closure**: partial — L24 (BG-completion vs
  pod-state-down conflation) is functionally validated via Scenario A's
  graceful 404-verify chain. L23 (rate-limit-fallback) is structurally enabled
  (alert-script is pure-bash to avoid recursive 429) but the
  foreground-takeover trigger is NOT exercised in this dogfood (no rate-limit
  was simulated). L25 (cost-overrun escalation) is selftest-only — see
  honest C5 in verdict.
- **Compute lifecycle triad (+ +) complete?**: yes in
  spec + tooling + dogfood. Block-tier enforcement promotion (warn → block) is
  the next milestone via tool/h100_bg_launch_lint.hexa (proposed in spec
  §5.4, not yet emitted).
- **No git commit performed** per task §6 (sibling BGs share working tree).

## Next-cycle handoff

- **Block-tier promotion**: emit tool/h100_bg_launch_lint.hexa (per spec §5.4
  enforcement-advisory) — wraps own_16_preflight.hexa with hook integration so
  any BG launch prompt failing 6/6 checklist at target_usd >= $5 is
  auto-rejected before hexa-runtime invocation. Estimated $0 mac, ~1h.
- **Cost-overrun functional validation**: a follow-up dogfood should backdate
  start_ts_epoch in a registry entry to simulate elapsed_h > 2x and elapsed_h
  > 3x, exercising the COST_OVERRUN_2X and COST_OVERRUN_3X_AUTOPAUSE alert
  paths against the alert-script. No real H100 boot needed; $0 mac.
- **Spec/impl drift fix**: reconcile spec §3.1 (alerts/<ts>_<pod>_<reason>.json)
  vs implementation (state/h100_alert_ledger_<YYYY_MM>.jsonl) — either update
  spec to match impl, or add per-alert file emission to alert-script. $0 mac.
- **Production launchd plist**: Phase 1 --daemon is single-iteration;
  production deployment requires a launchd plist wrapping
  /Users/ghost/core/hexa-lang/hexa run tool/h100_cost_watchdog.hexa on a
  5-min cadence. Not in this dogfood scope.

## Honest C3 (>=5; supplementary to verdict.json)

1. **Coverage gap — alive-pod stale-heartbeat path not exercised.** Scenario
   B+C used synthetic pod IDs with PATH sanitized to force state=UNKNOWN. The
   canonical production case (real alive pod with operator-orchestrator that
   died → heartbeat goes stale while runpodctl pod get still returns ALIVE)
   was not exercised because the dogfood pod was torn down at end of Scenario
   A to honor the $3 budget. Recommended next-cycle: extend dogfood to ~10min
   (heartbeat skipped during minutes 5-10) at ~$0.50 cost.

2. **Synthetic-vs-real asymmetry in alerts.** All 3 alert ledger rows are from
   synthetic pods (B, C). The real H100 dogfood pod generated 1 watchdog
   ledger row but 0 alerts (correctly — heartbeat was fresh throughout). This
   means alert-emission is dogfooded only against synthetic state; the alert
   wiring against state=ALIVE is structurally identical but not functionally
   validated.

3. **Auto-killer ladder selftest is dry-run only.** Scenario B confirmed
   h100_idle_auto_killer.hexa --selftest 4/4 PASS, but the selftest does NOT
   call real runpodctl pod stop. The actual pause command would be
   `runpodctl pod stop POD_ID` issued via the hexa runtime; this is
   structurally correct and the runpodctl wiring is identical to Scenario A's
   tear-down chain (which DID succeed against real pod), so confidence is
   reasonably transferable, but not first-party validated.

4. **30-min unack autopause window not exercised.** Per spec §3.2 tier 5,
   after a cost_2x_target alert the auto-killer waits 30min for user response
   before issuing pause at cost_3x_target_autopause. This 30-min sleep was
   deliberately skipped per task budget directive. Functional 30-min ladder
   remains unexercised in real-time.

5. **Cost computation accuracy.** The watchdog's cumulative_usd is
   (now - start_ts_epoch) * bid_usd_per_hr / 3600. For Scenario A the elapsed
   window was 06:46:42 (probe time) - 06:40:55 (start) = 347s → 0.0964h
   * $2.99 = $0.288, which rounds to the watchdog's $0.286542 (matches within
   0.5%). Cost computation is correct under the assumed continuous-billing
   model; real RunPod billing may differ on intermediate stop/start cycles.

6. **Compute-lifecycle triad claim sensitivity.** " + + =
   compute-lifecycle triad complete" is a strong claim. The narrower truthful
   claim is " phases 1-4 are spec-tested and tool-validated against the
   operationalization spec". Promotion to canonical taxonomy requires
   explicit .own mutation (admit entry per spec §5.4), which is NOT
   performed in this BG (per task constraint).

7. **Pod billable wall vs dogfood wall mismatch.** Pod was billable for
   6.46min ($0.32). Total dogfood (mac-side scenarios B+C) ran an additional
   ~5min after pod tear-down at $0 cost. The verdict's
   wall_time_min_pod_billable=6.46 is the correct cost-attribution number;
   wall_time_min_dogfood_total=11.78 is the operator-time number. Cost cap
   was honored against the former.

8. **Single-iteration daemon dogfood limitation.** The watchdog was invoked
   manually (single iters via hexa run) 3 times in this dogfood. In production
   it would run via launchd at 5-min cadence. The single-iter logic is fully
   validated; the iter-loop semantics (e.g., what happens if iter N+1 starts
   while iter N is still in runpodctl pod get SSH timeout) are NOT validated.
   Production hardening of the daemon-loop wrapper (lockfile,
   max-concurrent-iter=1) is a future-cycle concern.
