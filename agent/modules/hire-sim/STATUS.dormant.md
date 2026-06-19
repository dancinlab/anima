# anima-agent-hire-sim — DORMANT (2026-05-06)

Status: dormant — preserved for anima-model evaluation history. No active build, no link to anima-agent.

## Why
- anima-agent extracted to standalone repo (`dancinlab/anima-agent` v1.0.0, 2026-05-04).
- This directory holds anima-model employability benchmarks (TSRV-P4-2: 6-domain × task × deterministic rubric, hire-rate ≥ 0.85, intervention ≤ 5/hour, avg ≤ 10min).
- Link to anima-agent (`use "../anima-agent/autonomy_loop"` + `llm_claude_adapter`) severed in 4 files on 2026-05-06; original use lines preserved as `// historical:` comments.
- Belongs to anima (model evaluation), not to anima-agent (runtime surface).

## Active runtime status
- Source frozen. No autonomy_loop import → `run_autonomy(...)` call sites at hire_sim_100.hexa:568, test_hire_sim.hexa:89 reference an undefined symbol if compiled. Intentional — file is preserved as a record, not as a buildable target.
- Result paths (`anima-agent/results/...` in hire_sim_live.hexa:625-626 and clm_val.hexa:63 cross-ref) are stale — anima-agent/results was removed with the directory split.

## Reactivation
If hire-sim becomes active again, choose one:
1. Restore link via hx-installed anima-agent — replace severed `use` lines with a working import path (resolver compatibility verification required; `use "/Users/ghost/.hx/packages/anima-agent/..."` was tested unstable on 2026-05-06).
2. Migrate to a sister repo (`dancinlab/anima-agent-hire-sim`) — clean cross-repo dependency, follows the same extraction pattern as channels/providers/plugins/skills sister repos.
3. Inline the small `run_autonomy` surface — only one function from autonomy_loop is hot-path; `llm_claude_adapter` was import-only.
