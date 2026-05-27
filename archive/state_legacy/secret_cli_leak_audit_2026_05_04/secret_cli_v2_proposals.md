# Secret CLI v2 — Hardening Proposals (DESIGN ONLY)

**Target repo**: `/Users/ghost/core/secret/` (separate repo; absolute paths used per raw#15 disclaimer).
**Status**: DESIGN ONLY. Do NOT modify `/Users/ghost/core/secret/bin/secret` source from this audit. Proposals to be reviewed and applied in the secret repo's own commit cycle.
**Current CLI**: `/Users/ghost/core/secret/bin/secret` (298 LoC, bash + python3 stdlib heredocs, INI-style `credentials` file at repo root, `chmod 600`).

## Ranked proposals (by impact ÷ implementation cost)

### Proposal 1 (HIGHEST LEVERAGE) — `secret with-env K1 [K2...] -- cmd...`

**Signature**: `secret with-env <key> [<key2> ...] -- <command> [args...]`

**Semantics**:
1. Resolve each key via existing `_resolve_key` + `_get`.
2. Map dotted key → uppercase env var name: `huggingface.token` → `HF_TOKEN` (configurable map; default rule: `<section>.<name>` → `<SECTION>_<NAME>` uppercase). Add `--as VAR` flag for explicit naming.
3. `exec` the command with the env vars set, AND wire stdout+stderr through an in-process redact filter that replaces the resolved values with `<REDACTED:keyname>` before they reach the parent's stdout/stderr.
4. The redact filter only knows the *specific values* loaded for this invocation — minimal memory exposure.

**Bash impl sketch** (~25 LoC; sketch only, raw#9 ban does not apply since target is the secret repo, not anima):
```bash
_with_env() {
    local -a keys=() cmd_argv=()
    local saw_dashdash=0
    for arg in "$@"; do
        if [ $saw_dashdash -eq 1 ]; then cmd_argv+=("$arg"); continue; fi
        if [ "$arg" = "--" ]; then saw_dashdash=1; continue; fi
        keys+=("$arg")
    done
    [ ${#cmd_argv[@]} -ge 1 ] || _die "with-env requires '-- <command>'"
    [ ${#keys[@]} -ge 1 ] || _die "with-env requires at least one key"

    local -a env_kvs=() values=()
    for k in "${keys[@]}"; do
        local v; v="$(_get "$k")"
        local var_name; var_name="$(printf '%s' "${k%.*}_${k#*.}" | tr '[:lower:]' '[:upper:]')"
        env_kvs+=("$var_name=$v")
        values+=("$v")
    done
    # Build sed redact program from values (escape regex metachars)
    local sed_prog=""
    local i=0
    for k in "${keys[@]}"; do
        local esc; esc="$(printf '%s' "${values[$i]}" | sed 's/[][\.*^$/&]/\\&/g')"
        sed_prog+="s|${esc}|<REDACTED:${k}>|g;"
        i=$((i+1))
    done
    # exec command with env, pipe both streams through sed
    env "${env_kvs[@]}" "${cmd_argv[@]}" 2>&1 \
        | sed -E "$sed_prog"
}
```

**Test cases**:
- `secret with-env huggingface.token -- echo "token=$HF_TOKEN"` → outputs `token=<REDACTED:huggingface.token>`.
- `secret with-env runpod.api_key huggingface.token -- runpodctl pod create --env "{\"HF_TOKEN\":\"$HF_TOKEN\"}"` → response JSON has `<REDACTED:huggingface.token>` instead of plaintext.
- Exit code: must propagate command's exit code (use `${PIPESTATUS[0]}`).
- Empty value: error out before exec (don't run command with empty token).

**Rollout plan**:
1. Land in `secret/bin/secret` behind `secret with-env` subcommand (additive, no breaking change).
2. Update `_help` block.
3. Anima callers can opt in by replacing `export HF_TOKEN=$(secret get huggingface.token); cmd ... 2>&1 | tee log` → `secret with-env huggingface.token -- cmd ... 2>&1 | tee log`.

**Caveats**: (a) `sed` regex escaping must handle all 7 special chars including `/` (used as delimiter) — sketch above uses `|` to reduce conflicts but a value containing `|` will still break. (b) PIPESTATUS handling differs between bash and zsh. (c) Multi-line tokens (rare but possible for multi-line PEM-style secrets) won't be redacted by line-based sed — would need pcre2grep or python.

### Proposal 2 (HIGH LEVERAGE) — `secret redact` stdin filter

**Signature**: `<cmd> | secret redact [--keys K1,K2,...]`

**Semantics**: read stdin, replace any value matching a known secret with `<REDACTED:keyname>`, emit on stdout. With no `--keys`, redact ALL secrets in store (loads all values to memory — heavy; see caveats). With `--keys`, redact only the listed keys.

**Impl sketch**:
```bash
_redact() {
    local -a keys=()
    if [ "${1:-}" = "--keys" ]; then
        shift; IFS=',' read -ra keys <<< "${1:-}"; shift
    else
        mapfile -t keys < <(_list)
    fi
    local sed_prog=""
    for k in "${keys[@]}"; do
        local v; v="$(_get "$k" 2>/dev/null)" || continue
        [ -n "$v" ] || continue
        local esc; esc="$(printf '%s' "$v" | sed 's/[][\.*^$/&|]/\\&/g')"
        sed_prog+="s|${esc}|<REDACTED:${k}>|g;"
    done
    [ -n "$sed_prog" ] || { cat; return; }
    sed -E "$sed_prog"
}
```

**Test cases**:
- `echo "abc hf_FAKE123 def" | secret redact --keys huggingface.token` (assuming stored value `hf_FAKE123`) → `abc <REDACTED:huggingface.token> def`.
- Empty stdin → empty stdout.
- Token absent from stdin → passes through untouched.

**Caveats**: (a) Reads all secret values to memory if no `--keys` — strongly discourage default form. (b) Streaming through sed is line-buffered; for very long lines or binary payloads, behavior degrades. (c) If two secrets share a substring (e.g. `gh_AAA` and `gh_AAABBB`), order of substitution matters; sort keys by value length descending. (d) Cannot redact secrets shorter than ~10 bytes safely (false positives on common strings).

### Proposal 3 — `secret leak-check <file...>`

**Signature**: `secret leak-check [--keys K1,...] <file> [<file>...]`

**Semantics**: scan files for substring matches against known secret values; emit `file:line:keyname` for every hit, exit 1 if any match found, exit 0 if clean. Useful for pre-commit hooks and post-incident sweeps.

**Impl sketch**:
```bash
_leak_check() {
    local -a keys=() files=()
    if [ "${1:-}" = "--keys" ]; then shift; IFS=',' read -ra keys <<< "$1"; shift; else mapfile -t keys < <(_list); fi
    files=("$@")
    local found=0
    for f in "${files[@]}"; do
        [ -f "$f" ] || continue
        for k in "${keys[@]}"; do
            local v; v="$(_get "$k" 2>/dev/null)" || continue
            [ -n "$v" ] || continue
            if grep -nF "$v" "$f" >/dev/null 2>&1; then
                grep -nF "$v" "$f" | while IFS=: read -r ln rest; do
                    echo "$f:$ln: leak of '$k' detected" >&2
                done
                found=1
            fi
        done
    done
    return $found
}
```

**Test cases**:
- Clean file → exit 0, no output.
- File containing one stored token value → exit 1, `path:42: leak of 'huggingface.token' detected` on stderr.
- Glob expansion: `secret leak-check state/**/*.log` (caller's shell does the glob).

**Caveats**: (a) Same memory exposure as `redact` if no `--keys`. (b) `grep -F` is fast but won't catch base64-encoded variants of the token. (c) Won't catch tokens that have been rotated (the new value isn't in the store yet during the check). (d) Cannot detect tokens in compressed or binary blobs (zip, tar, sqlite).

### Proposal 4 — `secret rotate <key>`

**Signature**: `secret rotate <key>`

**Semantics**: human-assisted rotation. (a) Print the current value's last 4 chars + revocation URL (per-section table). (b) Prompt user to paste new value via `read -s`. (c) Atomic swap: old value backed up to `${CREDS}.bak.$(date +%s)`, new value written. (d) Optional: emit a `state/secret_rotations/<ts>_<key>.json` audit record (no value, just timestamp + key).

**Section→URL table** (hardcoded in `_rotate`):
- `huggingface.token` → `https://huggingface.co/settings/tokens`
- `github.token` → `https://github.com/settings/tokens`
- `runpod.api_key` → `https://www.runpod.io/console/user/settings`
- `anthropic.api_key` → `https://console.anthropic.com/settings/keys`

**Impl sketch**:
```bash
_rotate() {
    local key; key="$(_resolve_key "$1")"
    local section="${key%.*}"
    local cur; cur="$(_get "$key" 2>/dev/null)" || _die "key '$key' not found"
    local cur_tail="${cur: -4}"
    local urls; urls="$(_rotation_url_for "$section")"
    echo "secret: rotating $key (current ends in ...$cur_tail)" >&2
    [ -n "$urls" ] && echo "secret: revoke at: $urls" >&2
    echo -n "secret: paste new value (input hidden): " >&2
    local new; IFS= read -rs new </dev/tty
    echo >&2
    [ -n "$new" ] || _die "empty new value"
    [ "$new" = "$cur" ] && _die "new == old; aborting"
    cp "$CREDS" "${CREDS}.bak.$(date +%s)"
    chmod 600 "${CREDS}.bak."*
    echo "$new" | _set "$key"
    echo "ok: rotated $key (backup: ${CREDS}.bak.<ts>)" >&2
}
```

**Caveats**: (a) Doesn't actually invoke the revocation API — manual step required. (b) `cur ends in ...XYZ` partial-disclosure aids visual verification but is itself a small information leak (4 chars). Acceptable tradeoff. (c) Backup file accumulates (`.bak.<ts>` files). Add a `secret rotate-gc` housekeeping subcommand.

### Proposal 5 (LOW PRIORITY) — `secret env-mask`

**Signature**: `eval "$(secret env-mask --keys K1,K2)"`

**Semantics**: emit a sed program string to stdout that, when evaluated by the caller, produces a function `mask_known_tokens` redacting the listed keys. Useful when caller wants the filter as a reusable function rather than a per-command pipe.

**Impl sketch**: ~10 LoC. Output:
```sh
mask_known_tokens() { sed -E 's|VALUE1|<REDACTED:K1>|g; s|VALUE2|<REDACTED:K2>|g'; }
```

**Caveats**: (a) Caller's shell process now has the values inside a function definition in shell memory — wider exposure than Proposal 1's exec-and-pipe. (b) `eval` of CLI output is a security smell. (c) Largely subsumed by Proposal 1 + 2.

## Honest C3 caveats (raw#10)

1. **All proposals load secret values into shell process memory** at invocation. The current CLI's `_get` already does this, so no regression — but the `redact` and `leak-check` modes that load *all* secrets at once expand the exposure window from ~ms to seconds. A compromised shell during that window can read the whole vault.

2. **sed-based redaction has fundamental edge cases**: tokens that contain regex metacharacters are escaped (sketch shows `[][\.*^$/&|]`), but sufficiently weird tokens (NUL bytes, multi-line values) bypass line-based sed entirely. Recommend a python heredoc fallback for `_redact` if `sed` reports no match but stdin is non-empty (canary check).

3. **Symbol propagation through subshells**: `secret with-env K -- cmd` works for the direct child, but if `cmd` spawns its own subprocesses that re-emit the secret to *their* stdout/stderr, the redact filter still catches them (via the parent's pipe). However, if `cmd` writes to a side-channel file directly (`tool --log-file=/tmp/x`), the redact filter never sees those bytes. Documentation must warn callers not to give subprocess explicit file-output flags for token-bearing data.

4. **No protection against accidental `set -x`**. If a caller has `set -x` (xtrace) enabled, the shell prints every expanded command including `--env "K=actualvalue"` to stderr *before* `with-env` ever runs. Counter-measure: detect xtrace at startup of `with-env` and refuse with a clear error (`[ -o xtrace ] && _die "xtrace enabled — refuses to expose secrets"`).

5. **The CLI's existing `set` form still has the shell-history leak**: `secret set K $TOKEN` writes `$TOKEN` to bash/zsh history file. The current `_help` text already warns about this (line 276 of bin/secret). No regression but worth re-emphasizing in any v2 doc. A `--no-argv` flag rejecting argv form entirely could be added (forces stdin or tty).

6. **Backwards compatibility**: all 5 proposals are additive (new subcommands). No changes to existing `get`/`set`/`rm`/`list`/`check` behavior. Roll-forward only; no migration needed.
