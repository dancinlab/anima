# anima CLI mk2 — Phase 1 sub-cycle: args/exec fix (LANDED 2026-05-06)

Companion verdict: state/anima_cli_mk2_2026_05_06/phase_1_sub_args_fix_verdict.json

## Scope
bin/anima.hexa Phase 1 dispatcher sub-cycle:
1. argv parsing fix — args[0]='void' regression closed
2. exec syscall integration — print stub replaced with real exec()
3. raw#9 hexa-only / raw#10 honest C3 / raw#15 additive / freeze 정합 유지

## Discoveries

### A. args() convention
args() returns [interp_real_path, script_path, ...user_args] in both interp
and codegen run paths. Existing _user_argv() in tool/anima_cli/_common.hexa
filters by /.hexa-cache/ substring which does NOT strip the first 2 entries
on a real interp run.

All 26 tool/anima_cli/*.hexa scripts that use let sub = _str(argv[0]) (compute
audit doctor etc) currently treat the interp binary path as the subcommand.
Reason it didn't surface earlier: _arg_present(argv, "--help") flag scans
matches regardless of position.

### B. Canonical strip pattern (browser-harness)
/Users/ghost/.hx/packages/browser-harness/wrappers/browser_harness.hexa lines
92-106 provides the canonical robust pattern: scan for a trailing .hexa suffix
(= the script path itself) then take everything after. Adopted in our fix.

### C. hexa-strict auto-invoke
fn main() (no params) is auto-invoked by hexa-strict. A trailing main() call
triggers a hard error: auto-invoke conflict. All 26 scripts in tool/anima_cli/
end with main() and are therefore currently broken when invoked directly via
hexa run. This is the downstream blocker exposed by our fix.

### D. exec / RC capture
hexa stdlib exec(cmd) returns buffered stdout (no live streaming, no RC).
We wrap child invocation with printf __ANIMA_CHILD_RC=N sentinel and parse
the trailing line back. C2 caveat: long-running interactive REPL needs real
fork/exec syscall — Phase 2 lane.

## Fix applied — bin/anima.hexa

- fn main(args) -> fn main() + auto-invoke (no trailing call) — hexa-strict 정합
- _user_argv() helper added — browser-harness pattern .hexa suffix scan
- _hexa_bin() / _shq() / _exec_hexa() helpers — safe shell escape + RC forward
- print stub x4 sites replaced with real _exec_hexa(path, rest) and exit(rc)

LoC 161 -> 232.

## Test results (mac local 0 USD)

| Surface | Status | RC |
|---------|--------|----|
| anima --help | PASS — emits surface | 0 |
| anima --version | PASS — anima 0.2.0-mk2 | 0 |
| anima -h | PASS — same as --help | 0 |
| anima ops (no topic) | PASS — Usage line | 2 |
| anima ops doctor | PARTIAL — reaches doctor.hexa downstream auto-invoke fails | 1 |
| anima audit (legacy compat) | PARTIAL — deprecation hint + forwards same downstream bug | 1 |
| anima connect (T3 stub) | PASS — wire-up pending v2.0 | 0 |
| anima nonexistent | PASS — unknown line | 2 |

Dispatcher itself: all paths green.
Downstream blocker: 26 anima_cli scripts need trailing main() removal.

## Honest C3 (raw#10)

- C1 spec yaml dispatch table 직접 read X — hexa stdlib yaml 미land
- C2 exec() buffered not streamed — Phase 2 fork/exec lane for actual REPL
- C3 T1 chat REPL은 dialogue.hexa wired but actual REPL loop 미구현
- C4 T2 26 topics .hexa 존재 verified ALL 26 auto-invoke conflict
- C5 _user_argv() last .hexa suffix 가정 — partial truncation edge case
- C6 __ANIMA_CHILD_RC sentinel false-match edge case if child prints same literal

## Next sub-cycle (ranked by 완성도)

1. anima_cli sweep (0 USD ~30min 1 BG) — 26 files trailing main() removal +0.10 lift
2. Phase 1 stable land — dispatcher PASS, separable from sweep lane
3. spec yaml direct read — hexa-cc upstream 의존 비실행

## Verdict

PASS_DISPATCHER_FIXED_BLOCKED_BY_DOWNSTREAM_AUTO_INVOKE_SWEEP
