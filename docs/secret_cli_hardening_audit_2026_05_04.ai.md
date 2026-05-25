# Secret CLI Hardening Audit — AI-Native Handoff (2026-05-04)

**Cycle**: secret CLI leak-prevention spec + impl + caller audit
**Trigger**: HF token plaintext leak in `state/p9_base_validation_h100_2026_05_04/{boot.log, run.log, exec.nohup.log}` during P9 F1_v3 base-validation H100 boot.
**Status**: AUDIT COMPLETE; proposals + caller-fix designs landed; CLI patches PENDING (separate `/Users/ghost/core/secret/` repo); pre-commit hook install PENDING.
**Repo**: `/Users/ghost/core/anima/`
**Outputs**: 4 deliverables under `state/secret_cli_leak_audit_2026_05_04/` + this handoff doc.

## What landed

### Deliverable A — `state/secret_cli_leak_audit_2026_05_04/audit.md`
- Leak chronology: `secret get` → env var (safe) → `runpodctl pod create --env "HF_TOKEN=$HF_TOKEN_LOCAL" > boot.log 2>&1` (LEAK: RunPod API echoes env back) → `cat boot.log | tee -a run.log` (PROPAGATION).
- 5-pattern caller taxonomy (P1 safe / P2 pipe / **P3 env+log = THE LEAK** / P4 file dump / P5 print).
- Inventory: 1 active P3 (the H100 orchestrator); 3 latent P4 (h_last_raw_regen_r5, h100_r7_single_path_retrain, anima_an11_mistral7b_dispatch).
- 4 falsifier checks (3 currently PASS, 1 FAIL — F-LEAK-AUDIT-3 fails on the orchestrator).

### Deliverable B — `state/secret_cli_leak_audit_2026_05_04/secret_cli_v2_proposals.md`
- 5 ranked proposals for `/Users/ghost/core/secret/bin/secret`:
  1. `secret with-env K -- cmd...` exec wrapper (pipes child stdout/stderr through redact filter) — **HIGHEST LEVERAGE**, ~25 LoC bash sketch.
  2. `secret redact [--keys K1,...]` stdin filter — for retrofitting existing pipelines.
  3. `secret leak-check <file...>` audit — for pre-commit hook + post-incident sweeps.
  4. `secret rotate <key>` semi-automated rotation flow with revocation-URL table.
  5. `secret env-mask` (LOW PRIORITY; subsumed by 1+2).
- Each proposal has impl sketch, test cases, rollout plan, caveats.

### Deliverable C — `state/secret_cli_leak_audit_2026_05_04/caller_fixes.md`
- 4 patches (P-1 critical for the H100 orchestrator emitter; P-2/P-3/P-4 latent).
- Generic `tool/lib/redact.sh` template with 2 functions: `redact_known_tokens` (shape-based) and `redact_values` (value-aware).
- Critical fix-surface clarification: emitter `.hexa`, not the emitted `exec.bash`.

### Deliverable D — `state/secret_cli_leak_audit_2026_05_04/precommit_hook_proposal.md`
- 9-pattern regex set covering hf_, ghp_, ghs_, gho_, github_pat_, sk-ant-, rpod_, AKIA, AIza.
- ~60 LoC bash sketch with allowlist support + optional value-based pass when `secret leak-check` is available.
- Install via `ln -sf` symlink; bootstrap via `tool/dev_setup.bash`.
- 4 falsifier tests + 5 honest C3 caveats.

## What's pending

### Block 1 — secret CLI v2 (separate repo `/Users/ghost/core/secret/`)
- Apply Proposal 1 (`with-env`) — biggest single security win.
- Apply Proposal 2 (`redact`).
- Apply Proposal 3 (`leak-check`) — needed for value-based pre-commit pass.
- Update `/Users/ghost/core/secret/bin/secret` `_help` block.
- Owner: separate cycle, separate commit. Out of scope of anima merge.

### Block 2 — anima emitter patch (`tool/p9_base_validation_h100_orchestrator.hexa`)
- Inject the `mktemp + sed redact + rm` shape into the emit_body string at the runpodctl-create stage (lines ~205-220 of emitter).
- Re-emit `state/p9_base_validation_h100_2026_05_04/exec.bash` (overwrites the on-disk redacted file with a non-leaky-shape new emit).
- Re-test: re-run with a TEST token (not the production one), confirm no plaintext in any log.
- Owner: anima-side cycle.

### Block 3 — latent caller patches
- `tool/h_last_raw_regen_r5.bash`: replace `cat $HF_TOKEN_FILE` with `secret get`, add `_redact_stream` to global tee redirect.
- `tool/h100_r7_single_path_retrain.bash`: same pattern.
- `tool/anima_an11_mistral7b_dispatch.hexa`: switch from file-dump intent to mktemp+trap.

### Block 4 — pre-commit hook install
- Create `tool/git_hooks/pre_commit_token_scan.bash` (chmod +x) per Deliverable D sketch.
- Create empty `tool/git_hooks/leak_allowlist.txt`.
- Add `tool/dev_setup.bash` symlink-installer.
- Document in repo's CONTRIBUTING / README.

### Block 5 — token rotation
- User-side action: rotate the leaked HF token at `https://huggingface.co/settings/tokens`.
- Update local store: `secret set huggingface.token` (interactive `read -s` form, NOT argv form).
- Verify pod boot still works with new token (re-run smoke test on a 5-minute spot pod).

### Block 6 — leak-trace history scrub (OPTIONAL, USER DECIDES)
- The leaked token bytes still exist in the working tree's *redacted* logs (the old commit history doesn't have them since these state files are uncommitted). If the user wants to be paranoid: `git filter-repo` is unnecessary (no commits affected), but **rotate the token** — value is now considered burned.

## Recommended next-cycle action

**Single highest-impact action**: rotate the HF token (Block 5) + apply Block 2 emitter patch in the same cycle. Without rotation, even after fixing the emitter, the leaked value is still live and exploitable until the user revokes it on HF's side.

Suggested order:
1. **NOW** (user-side, ~2 min): rotate token at HF settings + `secret set huggingface.token` (stdin form).
2. **THIS CYCLE** (anima): apply Block 2 emitter patch + commit. Re-emit + re-test the orchestrator with the new token on a 5-min spot pod.
3. **NEXT CYCLE** (anima): apply Block 3 latent caller patches + Block 4 pre-commit hook.
4. **WHEN AVAILABLE** (secret repo): apply Block 1 CLI v2 in isolation, then anima callers can opt into `secret with-env`.

## Cross-references

- Origin: `state/p9_base_validation_h100_2026_05_04/{exec.bash, boot.log, exec.nohup.log, run.log}`
- Emitter: `tool/p9_base_validation_h100_orchestrator.hexa` (lines 158+)
- Secret CLI source: `/Users/ghost/core/secret/bin/secret` (separate repo)
- Audit deliverables: `state/secret_cli_leak_audit_2026_05_04/{audit,secret_cli_v2_proposals,caller_fixes,precommit_hook_proposal}.md`

## Honest C3 caveats (raw#10)

1. **No execution validation in this audit cycle**. All sketches are read-only design. Sed escape rules, line-number arithmetic in the pre-commit hook, and PIPESTATUS handling all need actual `bats` tests before the patches are deployed. Treat the LoC counts as estimates.

2. **`secret with-env` design assumes Mac-side bash 4+** for `mapfile` and named-array indexing. macOS ships bash 3.2 by default; the secret repo currently uses `#!/usr/bin/env bash` which on macOS without homebrew bash will use 3.2. Either pin to `/opt/homebrew/bin/bash` or rewrite without `mapfile`. Decision to be made in secret-repo cycle.

3. **The leaked HF token's blast radius is limited to HF resources** (not GitHub, not RunPod) — but if it's a write-scoped token, public model creation/deletion is possible until rotated. The audit assumes a read-scoped token; if it was write-scoped, the urgency is higher.

4. **Worktree mirrors not separately audited**. ~85 `.claude/worktrees/.../setup_secrets.hexa` files were skipped (assumed to be stale snapshots that will refresh on next agent worktree sync). If any worktree has an actively-running orchestrator, it could re-trigger the leak. Mitigation: rotate the token (Block 5) renders all stale worktrees benign.

5. **No coverage for non-RunPod cloud APIs**. The audit focused on RunPod's GraphQL env-echo behavior. Other cloud APIs (Vast.ai, Lambda Labs, Modal, AWS) may have similar response-echo patterns. Recommend a follow-up sweep when non-RunPod callers are added.
