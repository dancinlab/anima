# HF Token Canonical Baseline — 2026-05-04

**Status**: LANDED
**Scope**: anima/{tool,training} + nexus + qmirror + sim-universe + hexa-bio + honesty-monitor + anima-agent + hexa-lang
**SSOT**: `secret get huggingface.token` (HF official tool naming convention)

## TL;DR

Standardized HF token resolution to a canonical 3-tier order. Removed the legacy `hf.token` secret alias and shrunk a sprawling 5-source fallback chain in `tool/hf_upload_mk2.hexa` (v2.0.2 → v2.1.0) to the spec'd 3-tier order. Audit confirms zero live-code references to `hf.token` outside excluded scopes (worktrees, archives, historical state JSON).

## Canonical 3-Tier Order

```
1) secret get huggingface.token     (canonical SSOT — HF naming)
2) ~/.cache/huggingface/token        (HF CLI cache fallback)
3) HF_TOKEN env                      (explicit override)
```

Removed (no longer consulted):
- `hf.token` (legacy alias)
- `.secrets/hf_token` (committed-adjacent — security risk)
- `~/.huggingface/token` (huggingface_hub <0.17 path)
- `/workspace/.hf_token` (RunPod bootstrap path)
- `HUGGING_FACE_HUB_TOKEN` env (huggingface_hub legacy env name)

## Patch List

| File | Before | After | Notes |
|---|---|---|---|
| `tool/hf_upload_mk2.hexa` | v2.0.2 5-source `_resolve_token` | v2.1.0 3-tier canonical | Help text + error msg refreshed; selftest PASS |

### Files already canonical (no patch needed)

| File | Existing pattern |
|---|---|
| `tool/p9_base_validation_h100_orchestrator.hexa` | `secret get huggingface.token` (line 181) + `secret check huggingface.token` (line 127) |
| `nexus/design/kick/2026-04-27_mk-xii-phase3b-70b-vast-ai-r1-download-first-live-attempt-_omega_cycle.json` | `<secret get huggingface.token>` template (line 32) |

### Files using only `~/.cache/huggingface/token` (canonical-compatible, no patch)

These bash wrappers + the H100 P1 precheck hexa already use `${HOME}/.cache/huggingface/token` exclusively (no `hf.token` references):

- `tool/r6_smoke_axis2_qwen25.bash`
- `tool/r6_smoke_axis2_qwen3_null.bash`
- `tool/h_last_raw_regen_r5.bash`
- `tool/h100_stage2_unified_launch.bash`
- `tool/h100_r7_single_path_retrain.bash`
- `tool/h100_stage2_post_launch_chain.bash`
- `tool/anima_h100_p1_single_pilot_precheck.hexa`

## Secret Store State (2026-05-04)

```
[huggingface]
token = "#"     ← VALUE SCRUBBED (sentinel) — re-set required
```

`hf.token` key does NOT exist in `/Users/ghost/etc/secret/credentials`. No `secret rm` action was needed.

## Migration Path For New Code

```hexa
// hexa
let token = exec("secret get huggingface.token 2>/dev/null").trim()
if token.len() == 0 {
    let cache_path = exec("echo \"$HOME\"").trim() + "/.cache/huggingface/token"
    token = exec("test -f " + cache_path + " && cat " + cache_path).trim()
}
if token.len() == 0 {
    token = exec("echo \"$HF_TOKEN\"").trim()
}
```

```bash
# bash
HF_TOKEN_VAL="$(secret get huggingface.token 2>/dev/null \
    || cat "${HOME}/.cache/huggingface/token" 2>/dev/null \
    || echo "${HF_TOKEN:-}")"
[[ -n "${HF_TOKEN_VAL}" ]] || { echo "ABORT: no HF token"; exit 1; }
```

```python
# py (sister code on ubu1 / RunPod — informational only, raw#9 keeps Mac side .py-free)
import os, subprocess, pathlib
def resolve_hf_token():
    try:
        v = subprocess.check_output(["secret", "get", "huggingface.token"], stderr=subprocess.DEVNULL).decode().strip()
        if v: return v
    except Exception: pass
    p = pathlib.Path.home() / ".cache" / "huggingface" / "token"
    if p.exists():
        v = p.read_text().strip()
        if v: return v
    return os.environ.get("HF_TOKEN", "")
```

## Honest C3 Caveats (raw#10)

1. **Legacy `hf.token` may still be referenced in unaudited locations.** The audit intentionally excluded `.claude/worktrees/*`, `archive*`, `references/*`, `state/* (historical JSON)`, and `ready/anima/data/* (corpus dumps)`. Worktree branches that resurrect prior code paths may still call `secret get hf.token` and fail. Sweep any branch before merge.

2. **`secret rm hf.token` was NOT executed (key already absent).** If a future operator re-creates `hf.token` (muscle memory or doc-driven), no tool will warn about the duplicate; sister tooling will silently prefer `huggingface.token`.

3. **HF_TOKEN env precedence is a BREAKING change.** v2.0.2 of `hf_upload_mk2.hexa` consulted `HF_TOKEN` env FIRST (highest priority); v2.1.0 demotes it to TIER 3 (lowest, fallback only). Operators who set `HF_TOKEN` to override a stale secret store value must now either `secret rm huggingface.token` OR delete `~/.cache/huggingface/token` first. This change aligns with the spec's stated priority but must be flagged for any caller relying on env override.

4. **Fallback chain is shorter than before.** Removed `~/.huggingface/token`, `/workspace/.hf_token`, and `HUGGING_FACE_HUB_TOKEN` env. Pod entrypoints that wrote `/workspace/.hf_token` (some RunPod bootstraps) now need to either (a) write to `~/.cache/huggingface/token` instead, or (b) call `secret set huggingface.token` inside the pod, or (c) export `HF_TOKEN` env. Verify pod templates before next launch.

## USER ACTIONS REMAINING

1. **REVOKE** the token exposed in chat (`hf_OjV...REDACTED...mCAF`) at https://huggingface.co/settings/tokens
2. Generate a fresh write-permission token at the same URL
3. Set canonical: `pbpaste | secret set huggingface.token`
4. Sync to Mac HF cache: `secret get huggingface.token > ~/.cache/huggingface/token && chmod 600 ~/.cache/huggingface/token`
5. Sync to ubu1: `secret get huggingface.token | ssh ubu1 'cat > ~/.cache/huggingface/token && chmod 600 ~/.cache/huggingface/token'`
6. (Optional) Audit excluded scopes if any worktree branches will be merged into main: `grep -rn 'hf\.token' /Users/ghost/core/anima/.claude/worktrees/`

## Verification Sentinel

```
__HF_TOKEN_CANONICAL_BASELINE__ LANDED 2026-05-04
```

## References

- Spec: this doc
- Patched: `/Users/ghost/core/anima/tool/hf_upload_mk2.hexa` (v2.1.0)
- Audit: `/Users/ghost/core/anima/state/hf_token_canonical_baseline_2026_05_04/audit.json`
- Patches log: `/Users/ghost/core/anima/state/hf_token_canonical_baseline_2026_05_04/patches.jsonl`
- Marker: `/Users/ghost/core/anima/state/markers/hf_token_canonical_baseline_landed.marker`
- Related: `docs/clm_v4_tokenizer_restored_2026_05_03.ai.md` § "Token resolution surprise"
- Related: `state/clm_v4_tokenizer_ubu1_cache_status_2026_05_04/post_auth_verified_2026_05_04.md`
