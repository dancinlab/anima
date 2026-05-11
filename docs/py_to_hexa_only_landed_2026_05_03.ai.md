# py_to_hexa_only landed (raw#9 strict, 2026-05-03)

**Status**: LANDED  
**Marker**: `state/markers/py_to_hexa_only_landed.marker`  
**Audit**: `state/py_to_hexa_audit_2026_05_03/audit.json`  
**Cost**: $0 (Mac-local)

## Directive

Sweep ALL Mac-side `.py` to hexa, including the previously-allowed
`_python_bridge/` escape valve. New rule (memory: `feedback_py_to_hexa_only.md`):

- Mac side = **100% hexa**, NO `.py` anywhere
- SDK-only operations must become:
  - (a) raw HTTP via hexa http stdlib, OR
  - (b) external CLI binary via `proc_run` / `exec`, OR
  - (c) shipped to ubu1/RunPod runtime
- ubu1/RunPod-side `.py` untouched

## Files swept

| Path | LoC | Decision | Conversion |
|------|-----|----------|------------|
| `_python_bridge/hf_upload_runner.py` | 500 | convert | (b) external CLI: `hf` v1.8.0 shell-out |
| `tool/anima_holographic_ib_ksg_validate_prod.py` | 205 | delete | (c) deferred to ubu1 (raw#38 long-term hexa-native KSG) |
| `tool/_all_kick_extract_run.py` | 171 | delete | no replacement (raw#37 transient bypass) |
| `anima-eeg-core/tool/modules/_prng/_pcg32_reference.py` | 145 | delete | golden values already baked into hexa test vectors |

**Total**: 4 files deleted (1 converted in-place, 3 deleted no-replacement), 1021 LoC eliminated, 0 LoC added in `.py`.

**Directories removed**: `_python_bridge/` (now empty after `__pycache__` purge).

## Primary conversion: `tool/hf_upload_mk2.hexa`

The original justification for `_python_bridge/hf_upload_runner.py` was:

> "huggingface_hub is a python-only SDK with no public C ABI and no
> hexa-callable bindings. ... current `hf` CLI v1.8.0 lacks tag creation"

**Verified obsolete**: `hf` CLI v1.8.0 has full coverage —

```
$ hf --version
1.8.0
$ hf repo create --help     # has --exist-ok, --type, --token
$ hf upload --help          # folder upload, --commit-message, --token
$ hf repo tag create --help # full tag support
```

So conversion path (b) — external CLI shell-out — is fully viable and was applied.

### Hexa-side replacement architecture

```
tool/hf_upload_mk2.hexa  (v2.0.0, raw#9 strict)
├─ _hf_cli()              → resolve hf binary (override or PATH lookup)
├─ _hf_cli_check()        → version probe + availability check
├─ _resolve_token()       → HF_TOKEN env or ~/.huggingface/token fallback
├─ _sha256_file()         → exec("shasum -a 256 ...")
├─ _walk_files()          → exec("/usr/bin/find ... -prune dot-dirs")
├─ _file_size()           → exec stat (BSD/GNU dual-prong) + wc fallback
├─ _audit_write()         → JSONL append to state/hf_upload_audit/
├─ _do_selftest()         → no-network: cli + sha256 + walk verification
├─ _do_dry_run()          → walk + sha256 every file, audit log, no network
└─ _do_upload()           → hf repo create + hf upload + hf repo tag create
```

The bridge invocation chain (`_proc_run_with_stdin` → `_proc_json_bridge` → `_bridge_call`)
was removed entirely (~80 LoC). Replaced by direct CLI shell-out.

## Verification

```
$ find /Users/ghost/core/anima -name '*.py' \
  -not -path '*/state/*' -not -path '*/.venv*/*' \
  -not -path '*/.claude/*' -not -path '*/__pycache__/*' \
  -not -path '*/anima-physics/*' -not -path '*/anima-eeg/*' \
  -not -path '*/anima-tribe*/*' -not -path '*/ready/*' \
  -not -path '*/references/*' -not -path '*/__pyphi_cache__/*' \
  -not -path '*/.hxc_bench_a29_v3/*'
(empty)

$ hexa run tool/hf_upload_mk2.hexa --selftest
[hf_upload_mk2] SELFTEST (raw#9 strict — no python bridge)
  hf cli      = /Users/ghost/.local/bin/hf
  hf version  = 1.8.0
  hf available= 1
  [P] readme validator: good=OK, bad=rejected
  [P] naming validator: good=OK, bad=rejected
  [P] hexa selftest: selftest: PASS
__ANIMA_HF_UPLOAD_MK2__ PASS

$ hexa run tool/hf_upload_mk2.hexa --dry-run --repo dancinlab/clm-v4-sft-stage1 \
    --ckpt /tmp/_hfmk2_test_ckpt --readme /tmp/_hfmk2_test_readme.md --tag step-25k
[hf_upload_mk2] DRY-RUN (raw#9 strict — hexa-native walk + sha256)
  [P] naming OK
  [P] readme OK (5 required H2 + Caveats >=3)
  files       = 3
  total_bytes = 79
  audit       = state/hf_upload_audit/20260503T151335Z_dancinlab__clm-v4-sft-stage1.jsonl
__ANIMA_HF_UPLOAD_MK2__ PASS
```

Audit log records sha256 for every file with relative paths preserved.

## raw#10 honest C3 caveats (3, mandatory)

1. **HF rate-limit (HTTP 429) coordination is now external.**
   The legacy bridge had explicit `2^attempt` exponential backoff loop with
   `max_retries=3` inside the python process. The new path delegates 429
   handling entirely to `hf` CLI internals — which DO retry, but not in a
   way that this wrapper can introspect or coordinate. Parallel uploads
   from multiple BG subagents may still collectively exceed quota and
   surface as opaque CLI failures rather than per-attempt JSON records.

2. **Error-handling parity is reduced.**
   Bridge contract previously returned a structured JSON map per attempt
   (`HfHubHTTPError`, `huggingface_hub_unavailable`, `no_token`, etc.) so
   downstream callers could branch on error class. The CLI surface is
   stdout/stderr text + exit code — granular error classes are flattened
   into a single `hf_cli_upload_rcN: <stderr text>` string. Audit log
   captures the full CLI output tail (last 1024 bytes), but programmatic
   error-class branching by callers is degraded.

3. **Debug surface area shrinks.**
   No Python tracebacks — when something goes wrong inside `huggingface_hub`,
   the CLI prints a one-line error and exits. The bridge previously surfaced
   `traceback.format_exc()` in the response. Recovery on edge cases (auth
   token resolution, LFS pointer write, repo permission) is harder to
   diagnose without invoking the CLI manually with `--debug` flags. We do
   NOT pass `--quiet` so default verbose CLI output survives in the audit.

## What changed for callers

`tool/hf_upload_mk2.hexa` external API is **unchanged**:

- `--selftest`, `--dry-run`, `--upload`, `--validate-readme`, `--validate-naming`
- README enforcement (5 H2 + ≥3 Caveats bullets) preserved
- Naming validator preserved (org / family / version / stage convention)
- Audit log path + ledger format unchanged
- Sentinel `__ANIMA_HF_UPLOAD_MK2__ PASS|FAIL` preserved
- `tool/hf_upload_mk2_pre_push_hook.hexa` (git pre-push CI hook) unaffected — only calls `--validate-naming`

New ENV: `ANIMA_HF_CLI` overrides `hf` binary path (replaces deprecated `ANIMA_HF_PY`).

## Deferred (long-term hexa-native track)

| Item | Track | Status |
|------|-------|--------|
| Hexa-native scipy-equivalent KSG MI estimator | raw#38 implement-omega-converge | NOT-STARTED |
| Hexa http stdlib + LFS pointer encoder | raw#9 retirement criterion v2 | NOT-STARTED (CLI shell-out is the practical bridge) |

Per raw#9 strict, the `_python_bridge/` directory is now retired entirely.
Future SDK-only operations must follow the new triage:

1. **Try external CLI binary first** (this conversion's pattern)
2. **Try raw HTTP via hexa http stdlib next** (when hexa stdlib has http client)
3. **Ship to ubu1/RunPod runtime as last resort** (where .py is allowed)

## raw#15

No personal-path leak. All paths constructed via `$HOME` env. The audit
log uses `ANIMA_ROOT` (= `$HOME/core/anima`) for all stored paths.

## Backups

All deleted .py files preserved at:
`state/py_to_hexa_audit_2026_05_03/backup/`

(For 1-cycle rollback if a regression surfaces. After 30 days the backup
may be archived or deleted per state/ retention policy.)
