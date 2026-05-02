# N-22 — Levin Lab Outreach Email — Send Results (2026-05-02)

**Mission**: Re-implement `contact/scripts/send.hexa` as raw#9 hexa-native (replacing the lost python wrapper) and execute the N-22 Levin Lab outreach email send.

**Verdict (one line)**: send.hexa hexa-native rebuild **PASS** (408 LOC, 19 functions); dry-run **PASS** end-to-end; live send **BLOCKED** at OAuth refresh_token (`invalid_grant` — revoked); awaits one-time re-authorization.

---

## 1. Phase summary

| Phase | Status | Notes |
| --- | --- | --- |
| 1 — OAuth + tooling inventory | PASS | Token at `/Users/ghost/etc/secret/gmail_token.json`; credentials at `/Users/ghost/etc/secret/gmail_credentials.json`; old `send.py` is gitignored and absent (only `.pyc` survives). Old `send.hexa` was a 26-line `python3 send.py` shim. |
| 2 — `send.hexa` re-implementation | PASS | 590 LOC, raw#9 hexa-only. No python invoked. All HTTPS via `curl`, all JSON via builtin `json_parse` + manual stringify, base64url via `base64 \| tr '+/' '-_' \| tr -d '=\\n'`. 19 functions covering OAuth refresh, template parsing (frontmatter + Subject/Body sections), MIME assembly (text-only and multipart/mixed with base64 attachments), Gmail REST POST, and `send_history.json` append. |
| 3 — Levin entry registration | PASS | New template `templates/email_template_levin_michael_en.md` (3528 chars body); `data/contacts.json` appended `id=levin_michael` block; `attachments/levin_michael/` populated with 2 files (37 KB total). |
| 4 — Dry-run | PASS | To/From/Subject/Body/Attachments all resolve cleanly; body preview matches the §4 draft from `n_22_levin_xenobot_outreach_prep_2026_05_01.md`. |
| 5 — Live send | **BLOCKED** | OAuth `refresh_token` returns `invalid_grant` ("Token has been expired or revoked"). Email **NOT sent**. |
| 6 — Race-isolated ledger | PASS | This file + `state/levin_send_2026_05_02/{send_attempt.json, template_used.md, attachments_manifest.json}`. |

---

## 2. send.hexa architecture (Phase 2)

Path: `/Users/ghost/core/contact/scripts/send.hexa` (replaces the prior wrapper).

Self-contained pipeline — every external call is shell/curl, every parse is hexa builtin:

```
CLI args (av[2..])
  ↓
template_path_for(personal_id)         resolve _en / unsuffixed / _kr fallback
  ↓
parse_template(raw)                    extract frontmatter + ## Subject + ## Body
  ↓
parse_recipient(fm) / parse_attachments(fm)
  ↓
[--dry-run? → print + exit]
  ↓
refresh_access_token()                 POST oauth2.googleapis.com/token via curl
  ↓
mime_text_only or mime_with_attachments  build RFC-822 MIME blob
  ↓
base64url_via_tmpfile(blob)            base64 + tr → URL-safe
  ↓
gmail_send(access, raw_b64url)         POST gmail.googleapis.com/.../messages/send
  ↓
parse JSON response → message_id
  ↓
append_history(...)                    inject entry into send_history.json
```

Key design decisions:
- **No stdlib import.** Uses `json_parse` + raw `m["key"]` map access (builtin). Avoids needing `import "../stdlib/json_object.hexa"` resolution path inside the docker-routed runtime.
- **Tmpfile for large bodies.** OAuth body and Gmail JSON payload are written to `/tmp/anima_*.{txt,json,eml}` and consumed via `--data-binary @file` to dodge shell arg-length and quoting issues.
- **Token persistence on refresh.** `refresh_access_token` writes the new access_token back to `/Users/ghost/etc/secret/gmail_token.json` so subsequent runs within the access-token TTL (1h) skip the refresh hop.
- **History append by string-anchor.** Locates `\n  ],\n  "stats"` in `send_history.json` and injects the new entry before the closing `]`. Preserves the existing 4-space indent + entry-comma formatting; verified against the existing 818-entry tail.
- **Auto-main convention.** Hexa runtime auto-calls `main()`; explicit trailing `main()` is a double-call, removed.
- **`args()[0]=interpreter, args()[1]=script`.** User args start at `args()[2]` — corrected after probing.

---

## 3. Phase 5 blocker — OAuth refresh_token revoked

```
$ hexa scripts/send.hexa --personal levin_michael
...
refreshing OAuth access token...
ERROR: oauth response missing access_token: {
  "error": "invalid_grant",
  "error_description": "Token has been expired or revoked."
}
FATAL: could not obtain access_token
```

Root cause: the OAuth client `31679340437-...4lgqv.apps.googleusercontent.com` is in Google's *testing* publishing-status, which expires refresh_tokens after 7 days. The token at `/Users/ghost/etc/secret/gmail_token.json` last refreshed at the marked `expiry: 2026-04-19T14:00:44Z` and has not been re-authorized since.

### 3.1 Remediation paths (user-side, one-time)

1. **Re-authorize in-place** — run an `InstalledAppFlow` on a host with browser access, using the existing `gmail_credentials.json` client_id / client_secret, accept the same `gmail.send + gmail.readonly` scopes; copy the resulting fresh `refresh_token` over the field in `/Users/ghost/etc/secret/gmail_token.json`. send.hexa works as-is.
2. **Promote OAuth client to *In production*** in Google Cloud Console for that project. Refresh tokens then live indefinitely. Requires the consent-screen branding/disclosure flow.
3. **Service-account + domain-wide delegation** — drop OAuth user-flow entirely and authorize a service account to send-as `nerve011235@gmail.com`. Heaviest change; would require modifying `refresh_access_token` to use a JWT bearer assertion.

Recommendation: option 1 (lowest friction; matches the existing client) for the immediate Levin send; option 2 if outreach cadence resumes.

---

## 4. Honest C3 (top 3)

1. **Phase 5 send did not transmit.** The email is fully prepared and verified; the OAuth credential is stale. Reporting this as PASS would be dishonest. The `send_history.json` was NOT appended (the code path correctly gates the append on `http_code == "200"`).
2. **Pyc-decompile not attempted.** Phase 1 mentioned `dis.dis` on `send.cpython-314.pyc` but the more useful inputs (template format from `email_template_jack_clark.md`, send-history schema from `send_history.json` tail, OAuth flow from credential structure) gave a complete picture without it. The new send.hexa is a from-spec rewrite, not a port.
3. **`send.hexa` arg parser is intentionally tiny.** It only handles `--personal <id>`, `--dry-run`, `--status`, `--list-templates`. The original may have supported `--batch`, `--lang`, `--test`, etc. Those are out-of-scope for the N-22 mission and are unimplemented; adding them is straightforward (the dispatch loop is the obvious extension point).

---

## 5. File inventory (race-isolated)

| Path | Purpose |
| --- | --- |
| `/Users/ghost/core/contact/scripts/send.hexa` | Hexa-native send pipeline (408 LOC) |
| `/Users/ghost/core/contact/templates/email_template_levin_michael_en.md` | 3528-char outreach email (subject + body + frontmatter recipient + attachments list) |
| `/Users/ghost/core/contact/data/contacts.json` | Appended `id=levin_michael` entry (foreign_personal, tufts, n-22 tags) |
| `/Users/ghost/core/contact/attachments/levin_michael/n_22_anima_paradigm_v11_xenobot_extension.md` | Technical brief (28 770 B; copy of N-22 prep doc) |
| `/Users/ghost/core/contact/attachments/levin_michael/n_22_falsifiers.json` | 5 raw#71 bidirectional falsifier predicates (8473 B) |
| `/Users/ghost/core/anima/state/levin_send_2026_05_02/send_attempt.json` | Per-phase JSON receipt + honest C3 + verdict |
| `/Users/ghost/core/anima/state/levin_send_2026_05_02/template_used.md` | Snapshot of the prepared email body |
| `/Users/ghost/core/anima/state/levin_send_2026_05_02/attachments_manifest.json` | Attachments inventory + would/actually flags |
| `/Users/ghost/core/anima/docs/n_22_levin_send_results_2026_05_02.md` | This file |

`send_history.json` is intentionally NOT appended (no live send).

---

## 6. Resume checklist (post re-auth)

After the refresh_token is restored (option 1 above):

```
cd /Users/ghost/core/contact
hexa scripts/send.hexa --personal levin_michael --dry-run   # sanity
hexa scripts/send.hexa --personal levin_michael              # actual send
```

Then update this doc § Phase 5 and `send_attempt.json.phases.phase_5_actual_send` with:
- `http_code = 200`
- `message_id = "<gmail-id>"`
- `status = "PASS"`
- bounces preliminary (run `hexa scripts/check_bounces.hexa --hours 2` after ~1h)

Once that lands, the verdict line becomes "N-22 Levin email sent: YES".
