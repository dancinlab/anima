# secret CLI hardening — landed 2026-05-04

**Sentinel**: `__SECRET_CLI_HARDENING__ LANDED 2026-05-04`
**Cycle scope**: harden the unified credential CLI to prevent token leakage through agent / chat logs (root cause #1 of 5 HF token exposures this session).
**Source patched in place** (raw#9 STRICT compliant): `/Users/ghost/core/secret/bin/secret` (bash + python3 stdlib heredocs; user-owned, writable; not a system binary — no abort).

---

## 1. What changed

### F1 — redact-by-default for `secret get`
- Bare `secret get <key>` now prints `***REDACTED:<section.name>:<sha256-prefix-12>***` to stdout (no trailing newline, mirroring legacy whitespace contract).
- The plaintext value is no longer emitted unless `--raw` is supplied.

### F2 — `secret use <key> -- <command...>`
- Resolves the key, exports `SECRET_<SECTION>_<NAME>` (uppercased; dots/dashes -> underscores) plus a stable `SECRET_VALUE` alias into the environment, then `exec`s the command.
- The token value never touches stdout, stderr, or the child command's argv. Only the *key name* appears in `secret use`'s own argv (visible to `ps` for the wrapper process; not for the child after exec, depending on shell).
- Recommended replacement for `EXPORT TOK=$(secret get K); cmd ... 2>&1 | tee log` patterns.

### F3 — `--raw` opt-in plaintext
- Explicit `--raw` returns the plaintext value (parser is order-tolerant: `secret get --raw K` and `secret get K --raw` both work).
- Unknown flags rejected with exit 2 + diagnostic message.

### Help text
- `secret help` rewritten to document the three new affordances and includes a migration paragraph at the bottom.

### Internal refactor
- Old `_get` split into `_get_raw_value` (internal, returns plaintext) + `_get` (user-facing, applies redaction unless `--raw`).
- `_check` was rerouted to call `_get_raw_value` directly so the existence-probe semantics are unaffected by the redaction layer.

---

## 2. Smoke tests — 11/11 PASS

Synthetic test key `test_hardening_probe` (raw#15 compliant, value `synthetic_test_value_NOT_A_REAL_TOKEN_4f3c8a`) was created, exercised across all three features, and removed. Full transcript in `state/secret_cli_hardening_2026_05_04/smoke_test.json`.

| # | Test | Result |
|---|---|---|
| T1 | default redacted output                                                              | PASS |
| T2 | `--raw` after key returns plaintext                                                  | PASS |
| T3 | `secret use` injects 2 env vars (`SECRET_FLAT_TEST_HARDENING_PROBE`, `SECRET_VALUE`) | PASS |
| T4 | parent env clean after `secret use` exits                                            | PASS |
| T5 | child env value matches synthetic value byte-for-byte (length 44)                    | PASS |
| T6 | `secret use` surfaces exec failure (rc 1, stderr message)                            | PASS |
| T7 | unknown flag rejected (rc 2)                                                         | PASS |
| T8 | `--raw` before key (order-tolerant parser)                                           | PASS |
| T9 | `secret use` loose form (without explicit `--`)                                      | PASS |
| T10 | `secret list` still shows the key                                                   | PASS |
| TC | cleanup: `secret rm` + `secret check` confirms removal                               | PASS |

---

## 3. Caller audit — 13 sites, 8 blocking

Full table: `state/secret_cli_hardening_2026_05_04/callers_audit.jsonl`. Blocking subset (will return redacted hash literals to existing $() captures, breaking downstream auth):

### Code (must add `--raw` or migrate to `secret use`)
1. `/Users/ghost/core/anima/tool/hf_upload_mk2.hexa:303` — `exec("secret get huggingface.token 2>/dev/null").trim()`
2. `/Users/ghost/core/anima/tool/p9_base_validation_h100_orchestrator.hexa:180` — emits `export RUNPOD_API_KEY=$(secret get runpod.api_key 2>/dev/null)`
3. `/Users/ghost/core/anima/tool/p9_base_validation_h100_orchestrator.hexa:181` — emits `export HF_TOKEN_LOCAL=$(secret get huggingface.token 2>/dev/null)`
4. `/Users/ghost/core/anima/state/p9_base_validation_h100_2026_05_04/exec.bash:24-25` — regenerable from #2/#3 above
5. `/Users/ghost/core/papers/bin/papers:136` — `osf_token=$(_secret get osf.token 2>/dev/null)`
6. `/Users/ghost/core/papers/bin/papers:151` — `token=$(_secret get "$tkey" 2>/dev/null)`
7. `/Users/ghost/core/papers/bin/papers:215` — `token=$(_secret get zenodo.token 2>/dev/null)`

### Doc / error-string only (cosmetic — recommend update for consistency)
- `tool/anima_an11_mistral7b_dispatch.hexa:99` — error message guidance string
- `papers/README.md:112` — example recipe
- `papers/bin/papers:595` — help text
- `papers/tool/zenodo_publish.hexa:521` — error eprintln
- `papers/tool/osf_publish.hexa:432` — error eprintln

**Migration was NOT auto-applied per cycle constraint** ("DO NOT auto-migrate callers — require explicit user OK"). User decision required before next live use of the affected pipelines.

### Recommended migration patterns

**Pattern A — minimal `--raw` add** (preserves existing shape):
```bash
# before
export HF_TOKEN_LOCAL=$(secret get huggingface.token 2>/dev/null)
# after
export HF_TOKEN_LOCAL=$(secret get huggingface.token --raw 2>/dev/null)
```

**Pattern B — `secret use` refactor** (preferred when the next step is exec'ing a single command):
```bash
# before
export HF_TOKEN=$(secret get huggingface.token); hf upload my-org/my-repo file.bin
# after
secret use huggingface.token -- hf upload my-org/my-repo file.bin
```

---

## 4. Caveats (raw#10, 4 required)

**C1 — BACKWARDS-COMPAT BREAKAGE**: Every caller using bare `secret get` will now receive a ~50-char redacted hash starting with `***REDACTED:`. HTTP `Authorization: Bearer` headers, file dumps, and env exports built on bare `$()` will silently authenticate-as-garbage and the upstream service will return 401/403. The 8 blocking sites in §3 must be migrated before next live invocation. Recommend a quick `grep -rn "secret get" --include='*.bash' --include='*.hexa' --include='*.sh'` sweep against any branch about to be merged or any worktree about to be re-activated.

**C2 — ENV-VAR LEAKAGE VIA /proc/<pid>/environ ON SHARED HOSTS**: `secret use` exports `SECRET_<KEY>` and `SECRET_VALUE` into the child env. On macOS this is a child-process-only ACL (only same-UID processes can read it via `ps -E`). On shared Linux hosts (ubu1, RunPod), `cat /proc/<child_pid>/environ` is readable by other processes of the same UID for the lifetime of the child. NOT a concern for the local Mac use case that motivated this hardening, IS a concern if the same idiom is ported to ubu1 or any RunPod pod. Mitigation: prefer pipe-to-stdin patterns (`secret get K --raw | child --token-from-stdin`) for shared-host callers, or replace `exec` with a `setenv` shim that scrubs the env before re-exec.

**C3 — DEFAULT CHANGE REQUIRES USER NOTIFICATION**: Any operator (human or agent) muscle-memory using `secret get huggingface.token` to inspect a token will now see the redacted hash and may incorrectly conclude the vault is corrupted. This handoff doc + the marker serve as the announcement; recommend mentioning the change in the next session-start handoff and in `docs/hf_token_canonical_baseline_2026_05_04.md` (which currently shows 5 recipe lines using the bare form — those file-write recipes will produce a redacted-hash file until updated to `--raw`).

**C4 — CALLERS AUDIT MAY MISS DYNAMICALLY-GENERATED COMMANDS**: The grep used standard extension globs (`*.bash *.hexa *.py *.sh *.md *.json *.yml *.toml`). Sites where `secret get` is built up via string concatenation inside a `.hexa` template that emits a runtime command line (e.g. `"... " + key + " ..."`), or appears inside a Makefile / Dockerfile / `.envrc` / unversioned `.local/bin` script, may have been missed. The 13 sites in `callers_audit.jsonl` are the *visible* callers; expect a small number of additional discoveries on the next live run when something fails to authenticate. Suggested follow-up sweep: `ag 'secret get'` against `~/.claude/worktrees/`, sister repos in `~/core/*`, and any active `~/.zshrc`/`~/.config/` shell hooks.

---

## 5. Artifacts

| path | purpose |
|---|---|
| `/Users/ghost/core/secret/bin/secret`                                                      | patched CLI (in-place) |
| `state/secret_cli_hardening_2026_05_04/secret.before.bash`                                 | pre-patch snapshot |
| `state/secret_cli_hardening_2026_05_04/secret.after.bash`                                  | post-patch snapshot |
| `state/secret_cli_hardening_2026_05_04/before_after.diff`                                  | unified diff |
| `state/secret_cli_hardening_2026_05_04/audit.json`                                         | features + caveats + invariants |
| `state/secret_cli_hardening_2026_05_04/smoke_test.json`                                    | 11-test transcript |
| `state/secret_cli_hardening_2026_05_04/callers_audit.jsonl`                                | 13 caller sites with severity + fix |
| `state/markers/secret_cli_hardening_landed.marker`                                         | landed marker |
| `docs/secret_cli_hardening_landed_2026_05_04.ai.md`                                        | this handoff |

---

## 6. Constraints honored

- raw#9 STRICT — Mac source = bash, edited in place; no new `.py` created
- raw#15 — synthetic test key only; no real token in any test artifact (synthetic value `synthetic_test_value_NOT_A_REAL_TOKEN_4f3c8a` is self-labeled)
- raw#10 — 4 caveats above
- $0 — Mac local only
- credentials store untouched (the synthetic test key was added then removed; `git diff credentials` reflects no net change from this cycle)
- callers NOT auto-migrated — user OK required (per cycle constraint)
- source was writable + user-owned -> NO abort

---

## 7. Verdict

`__SECRET_CLI_HARDENING__ LANDED 2026-05-04` — 3 features + 11/11 smoke PASS + 13-site caller audit + 4 caveats. Awaiting user OK on caller migration before next live HF/RunPod/Zenodo/OSF invocation through the patched CLI.
