# check_bounces.hexa — hexa-native re-implementation (raw#107)

**Date:** 2026-05-02
**Branch:** main (race-isolated under `state/check_bounces_hexa_native_2026_05_02/`)
**Issue:** raw#107 — Gmail bounce checker was a python-shim wrapper; HEXA-FIRST policy bans `.py` in `anima` repo. Re-implement in pure hexa, mirroring the `send.hexa` raw#9 pattern.

## Files
- `/Users/ghost/core/contact/scripts/check_bounces.hexa` — 537 LOC (was 23 LOC python wrapper)
- `/Users/ghost/core/anima/state/check_bounces_hexa_native_2026_05_02/runs.jsonl` — append-only audit ledger
- `/Users/ghost/core/anima/state/check_bounces_hexa_native_2026_05_02/run_<UTCSTAMP>_<mode>.json` — per-run JSON report

## Pattern reuse from `scripts/send.hexa`
- `shell_escape_single` — verbatim
- `json_escape` — verbatim
- `read_file_safe` — verbatim
- `load_token_map` — verbatim (token at `/Users/ghost/etc/secret/gmail_token.json`)
- `refresh_access_token` — verbatim (POST `oauth2.googleapis.com/token`, persists refreshed access token preserving `refresh_token` + `gmail.send` + `gmail.readonly` scopes)
- CLI dispatch shape (av-walk with `--flag` + value pickup) — same idiom

New, bounce-specific:
- `build_query(hours_back)` — `from:postmaster OR from:mailer-daemon` plus `after:<unix>` window, `expr $(date +%s) - secs` for BusyBox compatibility
- `url_encode` — awk-based percent-encoder (no jq/python in docker hexa runtime)
- `gmail_list_messages` / `gmail_get_message` — `GET /users/me/messages?q=...` then per-id `GET /users/me/messages/{id}?format=full`
- `header_lookup` — accepts both `list` and `array` `type_of` results (hexa runtime quirk — `[]`-literals report `array`)
- `extract_reason_from_snippet` — heuristic search for `550 5.x`, `552 5.`, `554 5.`, `Address not found`, `does not exist`, etc.
- `parse_bounce_message` — distill `{id, from, subject, date, snippet, reason}` from full Gmail msg
- `format_report_text` / `format_report_json` — dual-format output
- `append_audit` — write per-run JSON + jsonl ledger line
- `run_selftest` — fully offline mock (two synthetic bounces) exercises parse + format + audit; assertions on count, id, subject, reason, JSON serialization

## CLI
```
hexa scripts/check_bounces.hexa                # last 24h (default)
hexa scripts/check_bounces.hexa --hours 48
hexa scripts/check_bounces.hexa --all          # no after: clause
hexa scripts/check_bounces.hexa --json         # JSON instead of text
hexa scripts/check_bounces.hexa --selftest     # offline mock, no Gmail call
```

## Verification

### Selftest — PASS
```
=== check_bounces.hexa --selftest (offline mock) ===
count: 2 (mock_msg_a + mock_msg_b)
SELFTEST PASS (mock parse + report)
```
Assertions checked: list length, first id, first subject, reason non-empty (550 hit), JSON serializer count.

### Live D+1 Levin bounce check — 0 bounces
```
hexa scripts/check_bounces.hexa --hours 24
query: from:postmaster OR from:mailer-daemon after:1777637919
count: 0
(no bounces found)
```
The Levin send (2026-05-01) is **clean** at D+1 — no postmaster/mailer-daemon DSN within the 24h window.

### Sanity — 30-day window returns 9 historical bounces
Confirms Gmail REST integration is genuinely live (not silently empty); historical April bounces (math.jussieu.fr, math.ucla.edu, math.nus.edu.sg, etc.) parsed correctly with subject `Delivery Status Notification (Failure)`.

## Audit ledger snapshot
```
{"ts":"2026-05-02T12:14:09Z","mode":"selftest","window_hours":24,"count":2,...}
{"ts":"2026-05-02T12:18:40Z","mode":"live","window_hours":24,"count":0,...}
{"ts":"2026-05-02T12:19:20Z","mode":"live","window_hours":720,"count":9,...}
```

## Constraints honored
- HEXA-only (no `.py` added/edited in `anima` repo); existing python wrapper logic obsoleted by self-contained hexa flow.
- $0 spend (local docker hexa runtime, free Gmail REST quota).
- Race isolation: bounded to `contact/scripts/check_bounces.hexa` + `state/check_bounces_hexa_native_2026_05_02/*` + this doc.
- OAuth token never logged (only `<redacted, len=N>`).
- Wall time: ~12 min from start of session to live PASS.
