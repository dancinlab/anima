# anima-eeg exec() silent-fail audit — 2026-04-28

## Scope
9 anima-eeg helper files (.hexa). Audit only — no fixes applied.

## Verified hexa runtime exec API (code-level, not hypothesis)

Source: `<repo-root>/../hexa-lang/self/rt/proc.hexa`

| API | Signature | Returns |
|---|---|---|
| `exec(cmd: string)` | `hexa_exec(cmd: string) -> string` | captured stdout only (exit code DISCARDED) |
| `exec_with_status(cmd: string)` | `hexa_exec_with_status(cmd: string) -> [any]` | `[stdout: string, exit_code: int]` |
| `exec_stream(cmd, on_line)` | builtin, registered in codegen_c2.hexa:3417 + build_c.hexa:2383 | streams lines to callback, returns int (treated as exit) |
| `safe_exec(cmd)` (stdlib/law_io.hexa) | `pub fn safe_exec(cmd: string) -> int` | wraps exec(), tries cmd, returns 0/1 (NOT real exit code) |

KEY FINDING: `exec()` returns string. Comparing it to int (== 0, != 0) is a silent type mismatch — hexa runtime does not error; comparison is always false in C-codegen path.

`exec_status()` from the original hypothesis does NOT exist as a top-level binding — only `exec_with_status()` is the real API. RFC-006 ground truth: use `exec_with_status()` or `exec_stream()`.

## Counts

- Total exec/exec_*() callsites scanned: 14
- BUG (string→int silent fail): 9
- OK_CAPTURE (string in, string out): 1
- OK_PROPER_API (exec_with_status correctly): 3
- OK_ALLOWED (annotated): 0

## Per-file breakdown

| File | line | call | classification | severity |
|---|---|---|---|---|
| board_health_check.hexa | 497 | `let rc = exec(cmd)` then `if rc==0/4/5/6/7` + `exit(rc)` | BUG | critical |
| calibrate.hexa | 340 | `let r = exec_with_status(cmd)` | OK_PROPER_API | none |
| eeg_recorder.hexa | 367 | `let r = exec_with_status(cmd)` | OK_PROPER_API | none |
| experiment.hexa | 416 | `let r = exec_with_status(cmd)` | OK_PROPER_API | none |
| electrode_adjustment_helper.hexa | 807 | `let _c = exec("clear")` (discarded) | VIOLATION | low |
| electrode_adjustment_helper.hexa | 1148 | `let _rc = exec(cmd)` then `return _rc` | BUG | high |
| electrode_adjustment_helper.hexa | 1282 | `let rc = exec(cmd); exit(rc)` | BUG | high |
| impedance_check.hexa | 62 | `return exec("date -u ...").trim()` | OK_CAPTURE | none |
| impedance_check.hexa | 571 | `let _rc = exec(cmd)` then `return _rc` ... `exit(rc)` | BUG | high |
| full_helmet_view.hexa | 701 | `let test_venv = exec("test -x ...")` then `if test_venv != 0` | BUG | critical |
| full_helmet_view.hexa | 708 | `let rc = exec(cmd); exit(rc)` | BUG | high |
| full_helmet_view.hexa | 738 | `let rc = exec(cmd); exit(rc)` | BUG | high |
| headplot_helper.hexa | 418 | `let rc = exec(cmd)` then `return rc` ... `exit(rc)` | BUG | high |
| electrode_helper_rich.hexa | 711 | `let rc = exec(cmd); exit(rc)` | BUG | high |

## Critical top-3 (highest functional risk)

1. **full_helmet_view.hexa:701-702** — `let test_venv = exec("test -x ...")` followed by `if test_venv != 0`. The exec captures empty stdout (`test` writes nothing), so `test_venv` is `""` — comparing string to int 0 is undefined-by-design. The intended venv vs `/usr/bin/python3` fallback is broken. This is the canonical silent-fail pattern from the discovery.

2. **board_health_check.hexa:497-523** — `let rc = exec(cmd); if rc == 0 ...; exit(rc)`. SCHEMA emits `exit_code: <string>` (looks fine in printout). Verdict branches all check `rc == 0/4/5/6/7` against a string — every comparison is false. Always falls through to `verdict: UNKNOWN exit_code=...` and the final `exit(rc)` passes a string to `exit()`. Helper exit codes (4/5/6/7 = NOT_DETECTED / SHORTED / 8CH_ONLY / PARTIAL_DEAD) are completely lost.

3. **electrode_adjustment_helper.hexa:1148 + impedance_check.hexa:571 + headplot_helper.hexa:418** — same antipattern: `_rc/rc` named like int, holds string, returned up the stack, eventually fed to `exit(rc)`. Multi-file silent-exit propagation. Treat as one cluster.

## Recommended fixes (NOT applied — this audit only)

- For exit-code intent: `let r = exec_with_status(cmd); let rc = to_int(r[1])`. Then `if rc == 0 ...` works.
- For string capture intent (impedance_check:62 already correct): keep `exec()` and add comment `// captures stdout`.

## raw compliance notes


## Files

- JSONL audit: `/tmp/anima_eeg_exec_audit_2026_04_28.jsonl`
- Summary: `/tmp/anima_eeg_exec_audit_summary.md`
