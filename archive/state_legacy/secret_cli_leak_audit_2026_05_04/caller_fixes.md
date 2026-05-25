# Anima Caller Fixes — Token Leak Hardening (2026-05-04)

**Status**: PROPOSAL ONLY — no patches applied. The leaky `state/p9_base_validation_h100_2026_05_04/exec.bash` is post-redact; future emits are the target. Patches below land on the **emitter** (`tool/p9_base_validation_h100_orchestrator.hexa`), not the emitted artifact.

## Patch P-1 (CRITICAL) — `tool/p9_base_validation_h100_orchestrator.hexa`

**Affected lines** (in the emitted bash, derived from emitter lines ~205-220):

Current (leaky) shape:
```bash
$RUNPODCTL pod create \
    --name "$POD_NAME" \
    ...
    --env "{\"HF_TOKEN\":\"$HF_TOKEN_LOCAL\"}" \
    > "$BOOT_OUT" 2>&1
BOOT_RC=$?
log "boot rc=$BOOT_RC"
cat "$BOOT_OUT" | tee -a "$RUN_LOG"      # <-- LEAK: re-streams BOOT_OUT (which contains the env echo) to RUN_LOG
```

Proposed (redact-on-write):
```bash
# Capture raw pod-create output to a private tmpfile that we delete after parsing.
BOOT_RAW="$(mktemp -t boot_raw_XXXX)"; trap 'rm -f "$BOOT_RAW"' RETURN
$RUNPODCTL pod create \
    --name "$POD_NAME" \
    ...
    --env "{\"HF_TOKEN\":\"$HF_TOKEN_LOCAL\"}" \
    > "$BOOT_RAW" 2>&1
BOOT_RC=$?

# Redact the HF_TOKEN before any disk-write. Use length-aware sed.
HF_RX="$(printf '%s' "$HF_TOKEN_LOCAL" | sed 's/[][\.*^$/&|]/\\&/g')"
sed -E "s|${HF_RX}|<REDACTED:huggingface.token>|g" "$BOOT_RAW" > "$BOOT_OUT"
rm -f "$BOOT_RAW"

log "boot rc=$BOOT_RC"
cat "$BOOT_OUT" | tee -a "$RUN_LOG"      # now safe — BOOT_OUT is pre-redacted
```

**Why this shape**:
1. Raw output goes to a tmpfile (700-mode by `mktemp` default), never to a path the user/process tree expects to read.
2. Redaction happens before *any* persistent write to `$STATE_DIR`.
3. `cat ... | tee` line is unchanged — the redact happens upstream so existing log plumbing keeps working.
4. `RETURN` trap removes the tmpfile even on early exit / signal.

**Alternative using Proposal 1 from `secret_cli_v2_proposals.md`** (cleaner, requires `secret with-env` to land first):
```bash
secret with-env huggingface.token -- bash -c '$RUNPODCTL pod create ... --env "{\"HF_TOKEN\":\"$HF_TOKEN\"}" > "$BOOT_OUT" 2>&1'
# secret with-env automatically pipes both streams through redact filter.
```

## Patch P-2 (LATENT) — `tool/h_last_raw_regen_r5.bash`

**Lines 47, 58, 89**:
```bash
readonly HF_TOKEN_FILE="${HOME}/.cache/huggingface/token"  # P4 file-cache
exec > >(tee -a "${LOG}") 2>&1                             # global tee
HF_TOKEN="$(cat "${HF_TOKEN_FILE}")"                       # value into env (line 89)
```

**Risk**: if any future log line prints `$HF_TOKEN` (e.g. debug `echo "token: $HF_TOKEN"`), the global tee at line 58 writes it to `$LOG`.

**Proposed shape**:
1. Replace `cat "${HF_TOKEN_FILE}"` with `secret get huggingface.token` (canonical source-of-truth, decommissions the disk cache for this caller).
2. Add a defensive trailing redact on the LOG file at end-of-script:
   ```bash
   _scrub_log() {
       [ -n "${HF_TOKEN:-}" ] || return 0
       local rx; rx="$(printf '%s' "$HF_TOKEN" | sed 's/[][\.*^$/&|]/\\&/g')"
       sed -E -i.bak "s|${rx}|<REDACTED:HF_TOKEN>|g" "${LOG}" && rm -f "${LOG}.bak"
   }
   trap _scrub_log EXIT
   ```
3. Even better: feed the entire `exec > >(tee ...)` redirect through a redact filter. Sketch:
   ```bash
   _redact_stream() {
       [ -n "${HF_TOKEN:-}" ] || { cat; return; }
       local rx; rx="$(printf '%s' "$HF_TOKEN" | sed 's/[][\.*^$/&|]/\\&/g')"
       sed -uE "s|${rx}|<REDACTED:HF_TOKEN>|g"   # -u: unbuffered, line-by-line
   }
   exec > >(_redact_stream | tee -a "${LOG}") 2>&1
   ```

## Patch P-3 (LATENT) — `tool/h100_r7_single_path_retrain.bash`

**Lines 43, 74, 192-207**: same shape as P-2 (file-cache + global tee), additionally has `curl -H "Authorization: Bearer ${HF_TOKEN_VAL}"` at line 207. If curl emits the failed-request URL or response on error, the bearer value can land in the log.

**Proposed shape**: same `_redact_stream` pre-tee pattern as P-2, applied once in the script preamble. Single fix covers both `cat HF_TOKEN_FILE` and the curl bearer. The redact filter only knows the value of `$HF_TOKEN_VAL`, so even if curl emits a different format (raw vs Bearer), substring match catches it.

## Patch P-4 (LATENT) — `tool/anima_an11_mistral7b_dispatch.hexa:99`

Currently the source comment acknowledges `secret get vast.ssh_private > file` as a known limitation (multi-line value). This *would* be Pattern P4 if executed.

**Proposed**: do NOT use file dump. Pipe directly to the consumer:
```bash
secret get vast.ssh_private | ssh-add -   # consumer reads stdin
```
Or if a file is required (some tools like `ssh -i` need a path), use `mktemp` + `chmod 600` + EXIT trap to delete:
```bash
KEY_FILE="$(mktemp)"
chmod 600 "$KEY_FILE"
trap 'rm -f "$KEY_FILE"' EXIT
secret get vast.ssh_private > "$KEY_FILE"
ssh -i "$KEY_FILE" ...
```
Lifetime of the file is bounded by process lifetime; trap fires even on SIGTERM.

## Generic shell function template

Drop this in `tool/lib/redact.sh` (NEW file — proposed, NOT created here) for callers to source:

```bash
# tool/lib/redact.sh — generic token-shape redact filter for log streams.
# Source this before any `tee`/`>>log` writes that may contain API responses.
#
# Usage:
#   . tool/lib/redact.sh
#   exec > >(redact_known_tokens | tee -a "${LOG}") 2>&1

redact_known_tokens() {
    # Known token-prefix regex set. Lengths chosen to avoid false positives.
    # NOTE: this is a SHAPE-based filter (catches tokens-shaped strings) and is
    # complementary to value-based filters (which need the exact value).
    sed -uE "
        s/(hf_[A-Za-z0-9_]{30,})/<REDACTED:hf_token>/g;
        s/(ghp_[A-Za-z0-9_]{30,})/<REDACTED:github_pat>/g;
        s/(ghs_[A-Za-z0-9_]{30,})/<REDACTED:github_server_token>/g;
        s/(gho_[A-Za-z0-9_]{30,})/<REDACTED:github_oauth>/g;
        s/(sk-ant-[A-Za-z0-9_-]{30,})/<REDACTED:anthropic_api_key>/g;
        s/(rpod_[A-Za-z0-9_]{30,})/<REDACTED:runpod_api_key>/g;
        s/(AKIA[A-Z0-9]{16})/<REDACTED:aws_access_key>/g;
        s/(AIza[A-Za-z0-9_-]{35})/<REDACTED:gcp_api_key>/g;
        s/(Bearer [A-Za-z0-9_-]{40,})/Bearer <REDACTED:bearer_token>/g;
    "
}

# Value-aware redact: pass the actual values you want hidden.
# Usage:
#   redact_values "$HF_TOKEN" "$RUNPOD_API_KEY" < input.log > output.log
redact_values() {
    local sed_prog=""
    for v in "$@"; do
        [ -n "$v" ] || continue
        # Escape sed metacharacters
        local esc; esc="$(printf '%s' "$v" | sed 's/[][\.*^$/&|]/\\&/g')"
        sed_prog+="s|${esc}|<REDACTED:value>|g;"
    done
    [ -n "$sed_prog" ] || { cat; return; }
    sed -uE "$sed_prog"
}
```

**Caveat**: Do NOT use the dangerous "load all secrets" pattern from the user-prompt's example template (`secret list | xargs ... secret get`). That reads the entire vault into shell memory for every invocation. Prefer the prefix-shape filter (`redact_known_tokens`) for general logs and the value-aware filter (`redact_values "$HF_TOKEN"`) when you know exactly which token you injected.

## Honest C3 caveats (raw#10)

1. **None of these patches are tested**. They are sketches based on reading the source. Concrete sed escape rules need a unit test (e.g., `bats`) to verify edge cases — empty value, value with newline, value containing `|` (used as sed delimiter).

2. **Patch P-1 still has a window**: between `mktemp` and the `sed | rm`, the raw boot log exists at a tmpfile path. If a parallel process inspects `$TMPDIR` during that window, leak. Window is ~ms but non-zero. Mitigation: use a memfd / named-pipe / process substitution instead of a tmpfile (`sed -E '...' < <($RUNPODCTL pod create ... 2>&1) > "$BOOT_OUT"`). Refactor recommended but adds complexity.

3. **Emit-time vs run-time fix**. The patches modify the emitter `.hexa`, but `state/p9_base_validation_h100_2026_05_04/exec.bash` is already on disk and was already used. Re-running it (without re-emitting) reproduces the leak. Action item: add a `git pre-commit` hook that refuses to commit any `state/.../exec.bash` file containing the leaky shape (Deliverable D covers this).

4. **`tool/lib/redact.sh` is a new file** — proposed but NOT created in this audit. Creating it requires a separate cycle with raw#9 review (bash sourcing pattern is grandfathered for `tool/h100_*.bash` siblings; `tool/lib/*.sh` would extend that grandfathering).
