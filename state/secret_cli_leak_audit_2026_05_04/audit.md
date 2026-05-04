# Secret CLI Leak Pattern Audit — 2026-05-04

**Cycle**: `state/secret_cli_leak_audit_2026_05_04/`
**Trigger**: HF token leak (plaintext) in `state/p9_base_validation_h100_2026_05_04/{boot.log, exec.nohup.log, run.log}` during P9 F1_v3 base-validation H100 boot at `2026-05-04T04:45:20Z`.
**Status**: tokens redacted in working tree, NOT YET COMMITTED. User to rotate HF token externally (`secret set huggingface.token`).

## 1. Leak chronology — root cause

| Step | Component | Evidence | Risk |
|---|---|---|---|
| 1 | `secret get huggingface.token 2>/dev/null` (`state/p9_base_validation_h100_2026_05_04/exec.bash:25`) | exec.bash line 25 | SAFE — value lives in shell var only |
| 2 | `export HF_TOKEN_LOCAL=$(secret get huggingface.token)` | exec.bash line 25 | SAFE — env var, no disk write |
| 3 | `runpodctl pod create --env "{\"HF_TOKEN\":\"$HF_TOKEN_LOCAL\"}" > "$BOOT_OUT" 2>&1` (line 36-48) | exec.bash line 47-48; emits to `boot.log` | HIGH — RunPod GraphQL response contains the env vars echoed back |
| 4 | `cat "$BOOT_OUT" \| tee -a "$RUN_LOG"` (line 51) | exec.bash line 51 | LEAK PROPAGATION — both `boot.log` AND `run.log` now contain plaintext token |
| 5 | `nohup ... > exec.nohup.log 2>&1` outer wrapper | n/a (process-level redirect) | LEAK PROPAGATION 2nd hop |

**Redacted evidence shape** (boot.log lines 5-8 post-redact):
```
"env": [
  "HF_TOKEN=<HF_TOKEN_REDACTED>",
  "PUBLIC_KEY=ssh-ed25519 ..."
],
```

The leak is **not** in `secret get` itself. The leak is in the caller's failure to filter `runpodctl pod create`'s JSON response, which by design echoes back every `--env` key/value as confirmation. `runpodctl` cannot omit them — its API contract is that the pod descriptor (which includes env) is the boot return payload. **The orchestrator must filter.**

## 2. Caller pattern taxonomy

| Pattern | Shape | Risk | Disk-leak? | Fix |
|---|---|---|---|---|
| **P1 — safe fetch** | `T=$(secret get K) && tool --token "$T"` | LOW | No (in-memory shell var) | none needed |
| **P2 — pipe consumer** | `secret get K \| tool --stdin-token` | LOW-MED | depends on `tool` | audit `tool` for log-of-stdin |
| **P3 — env+log (THE LEAK)** | `tool --env "K=$(secret get X)" 2>&1 \| tee log` (or `> log 2>&1`) — when `tool` echoes back the env in its API response | **HIGH** | YES — plaintext to disk | filter `tool` output through `secret redact` |
| **P4 — file dump** | `secret get K > /tmp/token` or `cat ~/.cache/huggingface/token` | **HIGH** | YES | replace with in-memory env or use `with-env` wrapper |
| **P5 — print** | `secret get K` (interactive, terminal only) | LOW | No (TTY only) | none if no piped logger |

The P9 base-validation orchestrator hit **Pattern P3** at `exec.bash:47-51`. Pattern P4 is also live in the codebase (`tool/h_last_raw_regen_r5.bash:89` reads `~/.cache/huggingface/token` after a global `exec > >(tee -a LOG)` redirect — risky if the token is later printed).

## 3. anima caller inventory

Sources scanned: `--include='*.hexa' --include='*.bash' --include='*.sh'`, excluding worktree mirrors (`.claude/worktrees/`).

| File | Line | Pattern | Status |
|---|---|---|---|
| `state/p9_base_validation_h100_2026_05_04/exec.bash` | 24-25, 47-51 | **P3 LEAK** | Redacted post-hoc; emitter still emits the leaky shape |
| `tool/p9_base_validation_h100_orchestrator.hexa` | 126-127 | P5 (`secret check`) | safe (no value retrieval) |
| `tool/p9_base_validation_h100_orchestrator.hexa` | 180-181, 205 | **P3 LEAK source** (emits exec.bash) | needs filter injection at emit time |
| `tool/h_last_raw_regen_r5.bash` | 47, 58, 89 | P4 (file dump) + global tee | risky if future token print added |
| `tool/h100_r7_single_path_retrain.bash` | 43, 74, 192-207 | P4 (file dump) + curl with `Authorization: Bearer` + global tee | LEAK candidate if curl errors echo header |
| `tool/anima_an11_mistral7b_dispatch.hexa` | 99 | P4 (intent: `secret get vast.ssh_private > file`) | flagged in source comment as limitation |
| `anima-core/runtime/setup_secrets.hexa` | 1+ | P1/P2 (init only) | safe — values stay in env |

**Counts (excluding worktree mirrors which are stale snapshots, ~85 of them):**
- P1: ~3
- P2: ~1
- **P3: 1 active (`exec.bash` + emitter)**
- **P4: 3 latent (h_last_raw, h100_r7, an11_mistral)**
- P5: 2

The P3 case is the confirmed-historical-leak path. The P4 cases are not currently leaking but are 1 logger-line away from leaking.

## 4. Falsifier set

- **F-LEAK-AUDIT-1**: zero `secret get K \| tee` patterns in tracked source.
  - Verify: `grep -rE "secret get [a-z._]+ ?\| ?tee" --include='*.bash' --include='*.hexa' --include='*.sh' anima` exits non-zero.
  - **CURRENT**: PASS (no direct pipe-to-tee found).
- **F-LEAK-AUDIT-2**: zero `secret get K > <persistent_path>` patterns.
  - Verify: `grep -rE "secret get [a-z._]+ ?> ?[^/dev/null]" --include='*.bash' --include='*.hexa' anima` exits non-zero.
  - **CURRENT**: PASS for direct shape; latent risk via P4 (file caches).
- **F-LEAK-AUDIT-3**: every API caller that injects `$HF_TOKEN`/`$RUNPOD_API_KEY`/etc. into a subprocess `--env` flag wraps the subprocess output through a redact filter before logging.
  - Verify: for each match of `runpodctl.*--env.*\$[A-Z_]+`, the same line/block must include `\| secret redact` or equivalent sed filter.
  - **CURRENT**: FAIL — `state/p9_base_validation_h100_2026_05_04/exec.bash` line 36-51 has no redact filter.
- **F-LEAK-AUDIT-4**: no caller writes secret values to a file path under repo working tree (excluding `.gitignore`'d caches).
  - **CURRENT**: PASS in repo proper; `~/.cache/huggingface/token` is outside repo.

## 5. Honest C3 (raw#10 caveats)

1. **Post-redact-only inference**. The exact byte-form of the original leak in `boot.log`/`run.log`/`exec.nohup.log` cannot be re-verified — those files are already redacted in the working tree (no commit yet). The leak shape is reconstructed from the surviving JSON skeleton + emitter source. If the emitter source has been edited between leak and now, the reconstruction may understate or overstate scope.

2. **Worktree mirror noise**. The grep returned ~85 hits from `.claude/worktrees/.../setup_secrets.hexa` (stale agent worktree mirrors). Active fix scope is the canonical `anima-core/runtime/setup_secrets.hexa` only; worktree copies will refresh on next sync. Did NOT separately audit each — assumed identical.

3. **`exec.bash` is emitted, not authored**. The fix surface is the `.hexa` emitter (`tool/p9_base_validation_h100_orchestrator.hexa` lines 158+), NOT the on-disk `exec.bash`. Patching `exec.bash` directly is overwritten next emit. Caller-fix doc (Deliverable C) will reflect this.

4. **No memory-side scrub**. Even with redact-on-output, the token still passes through Mac shell process memory (`HF_TOKEN_LOCAL` env var) and potentially through `runpodctl` process memory. A memory-resident attacker (other Mac process with `ptrace`/`vmread`) can still extract. Scope of this audit is disk-leak prevention only, not memory hardening.

5. **`secret get` exit-code masking**. The orchestrator uses `secret get K 2>/dev/null` which suppresses stderr from a missing key. Combined with `set -uo pipefail` (no `-e`), a missing key gives empty `HF_TOKEN_LOCAL` which is then injected as `--env "{\"HF_TOKEN\":\"\"}"` — RunPod accepts this and the pod boots without auth. Not a leak per se, but a silent-fail risk that could mask config drift. Fix: keep `secret check` precondition (lines 126-127 in emitter) which we already have.

6. **Redact filter assumes known-prefix tokens**. HF (`hf_*`), GitHub (`ghp_*`/`ghs_*`/`gho_*`), Anthropic (`sk-ant-*`), AWS (`AKIA*`), GCP (`AIza*`) — all have stable prefixes. RunPod API keys (`rpod_*` per their 2024+ format) and bare bearer tokens (`Bearer xxx` without prefix) are weaker. A naive regex-based redact filter will miss prefixless secrets. Mitigation: also pass through the *known set* from `secret list` for value-substring redaction, but that requires reading every secret into memory (security trade-off).
