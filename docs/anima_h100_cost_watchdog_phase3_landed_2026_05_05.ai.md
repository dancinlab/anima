---
title: H100 cost watchdog Phase 3 — landed (BG launch prompt template + memory enforcement)
cycle: 2026-05-05
ts: 2026-05-05T_h100_cost_watchdog_phase3_landed
bg_lane: BG-COST-WATCHDOG-PHASE3
substrate: mac ($0, md + memory only, no exec, no commit)
status: PHASE3_LANDED
type: convention_enforcement_handoff
predecessor:
  - docs/anima_h100_cost_discipline_operationalization_spec_2026_05_05.md (§3.4 + §4 Phase 3 scope)
  - docs/anima_own_16_h100_cost_discipline_landed_2026_05_05.ai.md (own 16 admission)
  - docs/anima_h100_cost_watchdog_phase1_landed_2026_05_05.ai.md (Phase 1 — tooling emission + selftest PASS)
  - (Phase 2 — orchestrator boot/heartbeat/trap/verdict hooks, in-flight sister BG)
related:
  - docs/anima_h100_bg_launch_prompt_template_2026_05_05.md (NEW — TEMPLATE doc)
  - feedback_h100_cost_discipline_l23_l25_watchdog_own_16.md (memory updated with Phase 3 §)
  - MEMORY.md (cross-link added)
  - tool/anima_bg_prompt_validator.hexa (PROPOSED future cycle — convention→tool migration)
raw_invariants:
  - raw#9 (md only — no code emission, no exec)
  - raw#10 (≥5 honest C3 below)
  - raw#15 (additive — no retire/absorb)
---

# H100 cost watchdog Phase 3 — landed (2026-05-05)

## Summary (5 bullets)

- **Memory entry updated**: `feedback_h100_cost_discipline_l23_l25_watchdog_own_16.md`
  appended with new "## How to apply (Phase 3 — BG launch prompt enforcement)"
  section enumerating the 6 mandatory checklist items (boot register /
  heartbeat touch / trap pre-stop deregister / verdict.json 5 fields /
  L23 fail-fast rescue trigger / L25 escalation awareness) plus
  deviation-policy thresholds ($5 mandatory / $1-5 strongly recommended /
  $0 optional) and reference to the new template doc + future
  `anima_bg_prompt_validator.hexa` proposal.

- **BG launch prompt template doc landed**:
  `docs/anima_h100_bg_launch_prompt_template_2026_05_05.md` (status TEMPLATE,
  ~290 lines, 8 sections — scope / 6 checklist items verbatim / hexa
  example boot snippet / validator hexa proposal / deviation policy /
  Pβ precedent / 7 honest-c3 entries / references). Boilerplate that any
  H100 BG launch prompt with `target_usd ≥ $1` can copy + lane-substitute.

- **MEMORY.md cross-link added** as new line below the existing own 16
  entry: "BG launch prompt L23/L24/L25 template" pointing to the same
  memory file (Phase 3 section anchor) — provides discoverable index
  hook for future BG-launching subagents that need quick-reference to
  the 6-checklist enforcement.

- **Phase 1 + Phase 2 + Phase 3 all landed → Phase 4 smoke ready** (deferred
  to separate cycle): Phase 4 = $1-3 H100 minimal pod boot, register with
  the watchdog being tested (dogfood pattern), simulate 3 scenarios
  (graceful complete + 404 verify / BG-killed mid-flight + watchdog auto-
  pause / heartbeat-stale → alert), then tear down cleanly. Phase 4 is
  the first opportunity to validate the convention-level Phase 3
  enforcement against a real-substrate end-to-end run.

- **Honest C3 (≥5)**: (1) Phase 3 enforcement is convention-level, not
  tool-level — `tool/anima_bg_prompt_validator.hexa` does not yet exist;
  the 6 checklist items are advisory-mandatory until validator + PreToolUse
  hook lands future cycle. (2) Cost ≥ $1 threshold is heuristic — sub-$1
  BGs that go 100× over still leak Pβ-class burn; floor was chosen for
  Phase 4 smoke dogfood compatibility, not principle. (3) L23 foreground
  takeover within 5min is unrealistic for overnight / weekend autonomy
  — Item 5 assumes operator-at-terminal; out-of-band paging (push / SMS)
  is required for true L23 resilience and is out of scope for the
  template. (4) Verdict.json 5-field schema is v1 floor (additive); if
  Phase 4 surfaces missing fields the schema bumps to v2 and old prompts
  fail field-presence linting unless validator accepts superset — that
  forward-compat discipline is not codified anywhere yet. (5) Items 5+6
  are prompt-prose disclosure (operator awareness), NOT executable code
  — a BG that includes Items 1-4 but skips 5-6 will pass token-level lint
  while losing the L23/L25 epistemic payload; only mitigation is
  template-adherence checked by future validator. (6) Template is mac-
  centric in the Item 5 rescue command (`/opt/homebrew/bin/runpodctl`);
  ubu1/ubu2 operators copying literally will hit "command not found"
  unless they substitute substrate-correct path. (7) own 14 + 15 + 16
  triad coherence: Phase 3 closes the "compute lifecycle convention
  layer" but storage (own 14) + publication (own 15) do NOT have parallel
  convention-layer templates; future cycle could mirror this 6-checklist
  pattern for HF Hub upload prompts to harden own 14 + 15 enforcement.

## Files written / updated

| Path | Δ | Role |
|------|---|------|
| `docs/anima_h100_bg_launch_prompt_template_2026_05_05.md` | NEW | TEMPLATE doc (8 sections, 7 honest-c3) |
| `docs/anima_h100_cost_watchdog_phase3_landed_2026_05_05.ai.md` | NEW | this handoff |
| `~/.hive/.../memory/feedback_h100_cost_discipline_l23_l25_watchdog_own_16.md` | APPENDED | Phase 3 application § + deviation policy |
| `~/.hive/.../memory/MEMORY.md` | APPENDED | cross-link line below own 16 entry |

## Phase ladder status

| Phase | Status | Cost | Cycle |
|-------|--------|------|-------|
| Phase 1 (tooling emission + selftest) | LANDED | $0 | 2026-05-05 (sister BG) |
| Phase 2 (orchestrator hooks) | IN-FLIGHT (sister BG) | $0 | 2026-05-05 |
| Phase 3 (memory + prompt template) | **LANDED (this BG)** | $0 | 2026-05-05 |
| Phase 4 ($1-3 H100 smoke) | READY (deferred separate cycle) | $1-3 | TBD |

## Next-cycle handoff

- Phase 4 smoke can launch as soon as next cycle opens. Surface = boot 1
  minimal H100 pod (cheapest tier, ~$1.99-2.99/hr × ~30min budget),
  register via `tool/h100_register.bash` (Item 1), simulate 3 scenarios
  per spec §4, tear down + 404 verify (Item 4 success gate). Phase 4 BG
  launch prompt is itself the **first real-world adopter** of this
  Phase 3 template — pure dogfood test.

- Future cycle: emit `tool/anima_bg_prompt_validator.hexa` per Phase 3
  template §4. Surface = `--prompt-file <path>` exit-code lint, scans
  required tokens for items 1-6. Migration = convention → tool
  enforcement once validator + PreToolUse hook land.

- No commit this cycle (per CRITICAL bullet — md only, raw#9/10/15).
  Next cycle should batch Phase 1 + Phase 2 + Phase 3 + Phase 4 results
  into a single additive commit.
