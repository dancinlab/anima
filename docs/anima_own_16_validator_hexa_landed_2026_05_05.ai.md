---
title: anima own 16 validator hexa LANDED — convention → mechanical enforcement
cycle: 2026-05-05
ts: 2026-05-05T_own_16_validator_hexa_landed
bg_lane: BG-OWN-16-VALIDATOR-HEXA
substrate: mac ($0, ~35min, hexa codegen + selftest only, no commit)
status: LANDED
type: tooling_landed_handoff
predecessor:
  - docs/anima_h100_cost_discipline_operationalization_spec_2026_05_05.md (§3.4 — 6-item checklist authority)
  - docs/anima_h100_bg_launch_prompt_template_2026_05_05.md (Phase 3 boilerplate)
  - tool/h100_cost_watchdog.hexa (Phase 1 watchdog — register/deregister API)
  - feedback_h100_cost_discipline_l23_l25_watchdog_own_16.md (memory SSOT)
artifacts:
  - tool/own_16_preflight.hexa (NEW, 389 LoC, raw#9 hexa-only)
  - state/own_16_preflight_test_2026_05_05/scenario_full_pass.txt
  - state/own_16_preflight_test_2026_05_05/scenario_partial_fail.txt
  - state/own_16_preflight_test_2026_05_05/scenario_zero_cost_optional.txt
  - state/own_16_preflight_test_2026_05_05/test_runner.bash
  - state/own_16_preflight_test_2026_05_05/test_runner_results.json
  - state/own_16_preflight_2026_05_05/verdict.json
  - feedback_h100_cost_discipline_l23_l25_watchdog_own_16.md (PATCH — mechanical-enforcement section appended)
raw_invariants:
  - raw#9 (hexa + bash carve-out OK; selftest only — no pod exec)
  - raw#10 (≥5 honest C3 in §5; verdict.json honest_c3 has 7 entries)
  - raw#15 (additive only — no roadmap mutation, no .own mutation, no commit, no exec)
---

# anima own 16 validator hexa LANDED (2026-05-05)

## §1 What landed

`tool/own_16_preflight.hexa` (389 LoC) — heuristic substring-match validator
that scans an H100 BG launch prompt for the 6 mandatory own 16 checklist
items defined in `docs/anima_h100_cost_discipline_operationalization_spec_2026_05_05.md` §3.4
and `docs/anima_h100_bg_launch_prompt_template_2026_05_05.md` §2.

The validator emits a canonical STDOUT marker line:

```
__OWN_16_PREFLIGHT__ <PASS|WARN|FAIL> score=N/6 missing=[item-list] target_usd=<float>
```

This line is the contract that downstream tooling (test_runner.bash,
future PreToolUse hook) parses for verdict assertion. The hexa runner on
this mac substrate does not reliably propagate `main()` return values as
POSIX exit codes (honest_c3 C4) — same convention as
`tool/h100_cost_watchdog.hexa` selftest reads ledger row presence rather
than relying on exit code.

## §2 6 checklist signals detected

| Item | Name              | Tokens (substring-match heuristic)                                      |
|------|-------------------|--------------------------------------------------------------------------|
| 1    | boot_register     | `h100_register.bash` OR (`h100_cost_watchdog.hexa` AND `--register`)     |
| 2    | heartbeat_hook    | `state/h100_watchdog/heartbeats` OR (`heartbeat` AND `5min`/`5 min`)     |
| 3    | trap_deregister   | `--deregister` OR `watchdog_deregistered`                                |
| 4    | verdict_schema    | `pod_kill_verified_404` AND `watchdog_deregistered`                      |
| 5    | l23_failfast      | `L23` OR `rate-limit-fallback` OR `foreground takeover` OR `rate-limit fallback` |
| 6    | l25_escalation    | `L25` OR `cost-overrun escalation` OR `auto-pause` OR `auto-PAUSE`       |

## §3 Deviation policy

| Cost band                       | Required score   | Verdict           |
|---------------------------------|------------------|-------------------|
| `target_usd ≥ $5` (mandatory)   | 6/6              | 6 → PASS, else FAIL |
| `$1 ≤ target_usd < $5`          | 5+/6             | ≥5 PASS, 4 WARN, <4 FAIL |
| `target_usd = $0` (optional)    | n/a              | always PASS       |

Target_usd is extracted by regex-light scan (priority: `--target-usd N`
override > `target_usd:` key > `$N target/H100/budget` near-miss); explicit
override via `--target-usd N` flag bypasses extraction.

## §4 Selftest evidence

3-scenario harness validated by `state/own_16_preflight_test_2026_05_05/test_runner.bash`:

```
[S1_full_pass]          PASS — verdict=PASS  score=6/6  (full 6-item prompt at $5)
[S2_partial_fail_at_5]  PASS — verdict=FAIL  score=4/6  (items 5+6 missing at $5 mandatory)
[S3_zero_cost_optional] PASS — verdict=PASS  score=0/6  ($0 optional, all items absent)
```

Runner exit 0; results JSON at
`state/own_16_preflight_test_2026_05_05/test_runner_results.json`.

## §5 Honest C3 (raw#10)

1. **Heuristic substring-match** — semantic equivalence is not guaranteed.
   Future BG prompts using different phrasing for the same intent (e.g.,
   "register-pod" instead of `--register`) may produce false-FAIL.
   Mitigation = additive token-list expansion in subsequent cycles.

2. **Deviation thresholds heuristic** — $5 / $1 / $0 bands chosen against
   current Phase 4 smoke target band. After production data refinement
   may shift; the validator is NOT a substitute for cost-band review.

3. **Target_usd extraction is regex-light + first-match-wins** — multi-
   budget prompts (e.g., `$1 smoke + $5 production` in same launch) will
   pick the lower band incorrectly. Workaround = explicit
   `--target-usd N` override flag.

4. **Hexa runner does not propagate POSIX exit code on mac substrate** —
   STDOUT marker line is the contract; test_runner.bash + future hook
   integrations must assert on the marker, not on `$?`. Same convention
   as `tool/h100_cost_watchdog.hexa` selftest.

5. **PASS only confirms prompt-level intent** — does NOT verify runtime
   watchdog registration actually succeeded. Runtime verification
   requires Phase 4 dogfood smoke ($1-3 H100, user ACK).

6. **L23/L25 detection by token presence** — prose-disclosure DEPTH (does
   the prompt actually internalize the lesson, or just name-drop the L-
   tag?) is not measured. A prompt that says "L23 is acknowledged" with
   no rescue command body still passes Item 5.

7. **Validator is opt-in** — no PreToolUse hook auto-runs it yet. Operator
   or orchestrator-author must explicitly invoke before BG launch.
   Convention→mechanical migration is partial; full PreToolUse-hook
   integration deferred to follow-up cycle.

## §6 own 16 phase promotion

| Aspect                  | Pre-2026-05-05            | Post-2026-05-05 (this BG)        |
|-------------------------|---------------------------|----------------------------------|
| Enforcement layer       | convention-only           | mechanical lint available         |
| Tool surface            | none (advisory in memory) | `tool/own_16_preflight.hexa`     |
| Verdict marker          | n/a                       | `__OWN_16_PREFLIGHT__ ...`       |
| Selftest                | n/a                       | 3 scenarios PASS, runner exit 0  |
| Auto-trigger            | n/a                       | manual (PreToolUse hook deferred) |
| Phase 4 dogfood blocker | tooling absent            | tooling ready (user ACK required) |

## §7 Phase 4 readiness

Phase 4 H100 dogfood smoke ($1-3 H100, user ACK) preconditions:

| Precondition                                          | Status   |
|-------------------------------------------------------|----------|
| Phase 1 watchdog hexa landed                          | LANDED   |
| Phase 1 alert sink (`h100_alert_emit.bash`) landed    | LANDED   |
| Phase 1 register wrapper (`h100_register.bash`) landed| LANDED   |
| Phase 3 mechanical validator landed (this BG)         | LANDED   |
| Memory SSOT updated with mechanical-enforcement section | LANDED |
| User ACK on dogfood smoke target_usd 1-3 + scenarios  | PENDING  |

**Recommended Phase 4 dogfood scenarios** (next-cycle):

1. **graceful-complete + 404 verify** — boot $1 smoke pod, register,
   complete training, deregister, verify 404 + verdict.json schema.
2. **BG-killed mid-flight + watchdog auto-pause** — boot $1 smoke pod,
   simulate BG agent death (kill PID), confirm watchdog detects stale
   heartbeat, auto-pause fires at 3× threshold.
3. **heartbeat-stale alert** — boot $1 smoke pod, halt heartbeat updates,
   confirm alert at 5min stale threshold.

All three scenarios MUST run the launch prompt through
`hexa run tool/own_16_preflight.hexa --validate-prompt <prompt>` before
boot; PASS required to proceed (mandatory-band $5 OR strongly-recommended
band $1-3).

## §8 References

- spec: `docs/anima_h100_cost_discipline_operationalization_spec_2026_05_05.md`
- template: `docs/anima_h100_bg_launch_prompt_template_2026_05_05.md`
- Phase 1 watchdog: `tool/h100_cost_watchdog.hexa`
- memory SSOT: `feedback_h100_cost_discipline_l23_l25_watchdog_own_16.md`
- verdict: `state/own_16_preflight_2026_05_05/verdict.json`
- test scenarios: `state/own_16_preflight_test_2026_05_05/`
- Pβ rescue precedent: `state/p9_pbeta_paradigm_d_50k_rescue_kill_2026_05_05/verdict.json`
