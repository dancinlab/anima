<!-- [Hc_922 n22-levin-xenobot-anthrobot-bioelectric — moved to hypotheses_candidates/Hc_922_n22_levin_xenobot_anthrobot_bioelectric.md on 2026-05-11] -->

# N-22 Levin response monitor + bounce check infra schedule

**Date authored**: 2026-05-02
**Send anchor**: Gmail msg_id `19de825e26e98b82`, HTTP 200, `michael.levin@tufts.edu`, sender `nerve011235@gmail.com`
**Send record (immutable)**: `/Users/ghost/core/anima/state/levin_send_2026_05_02/`
**Monitor state (this task)**: `/Users/ghost/core/anima/state/n_22_levin_monitor_2026_05_02/`

## 1. Schedule (D+1 / D+7 / D+14 / D+28)

| Label | Date       | Purpose                              | Action if silent                                          |
|-------|------------|--------------------------------------|-----------------------------------------------------------|
| D+1   | 2026-05-03 | Bounce check                         | User manual Gmail check (top-3 below) -> mark CLEAN/BOUNCED |
| D+7   | 2026-05-09 | First response checkpoint            | Stay silent, no nag — proceed to D+14                     |
| D+14  | 2026-05-16 | Follow-up decision (one-time only)   | Send `follow_up_template.md` (~150 EN words)              |
| D+28  | 2026-05-30 | Final status                         | Archive, optional re-prompt 3-6mo later (lighter cadence) |

## 2. Follow-up rule

- **Trigger**: no response by D+14 (2026-05-16)
- **Quantity**: exactly one follow-up; no further nags after that
- **Etiquette basis**: academic norm — single gentle follow-up acceptable, second = pestering
- **Template**: `state/n_22_levin_monitor_2026_05_02/follow_up_template.md`
- **Subject**: `Re: anima CP2 framework × xenobot bioelectric Φ — gentle follow-up`
- **Softer ask**: "even a brief reply on whether this aligns with your current bandwidth would be valuable"

## 3. Response handling (any time D+0+)

| Reply type                 | Action                                                                              |
|----------------------------|-------------------------------------------------------------------------------------|
| POSITIVE                   | Present 3 partnership options per #89: consultation / pilot data / joint paper      |
| NEGATIVE / decline         | Thank, gracious one-liner, archive                                                  |
| PARTIAL (interested-busy)  | Thank, mark interested, re-prompt 3-6mo later (lighter cadence)                      |
| REDIRECT to grad student   | Forward + brief intro, accept redirect, treat grad as new primary                   |

## 4. User manual check (D+1) — top-3

1. **Inbox** — search `from:postmaster OR from:mailer-daemon OR from:noreply newer_than:2d`. Clean = zero results.
2. **Spam folder** — same query (Gmail occasionally misclassifies bounces).
3. **Sent folder** — verify `19de825e26e98b82` present with both attachments (`n_22_anima_paradigm_v11_xenobot_extension.md` 28770B + `n_22_falsifiers.json` 8473B).

(Bonus rank-4: scan inbound from `@tufts.edu` — in the unlikely D+1 reply event, short-circuit to response handling.)

## 5. Honest C3

- Academic cold-email response rate: **10-30%** typical baseline.
- Levin lab adjustment (high-profile, large inbound): **5-15%** estimated.
- Partnership decision dependencies: Levin himself + lab bandwidth + user's own partnership criteria.
- ETA from response received -> partnership active: **+4-12 weeks**.
- Total ETA outreach -> active partnership: **5-16 weeks** if PASS, **~28 days** to no-response close if silent.

## 6. `check_bounces.hexa` hexa-native re-implementation (deferred)

- Current file is a **26-line .py wrapper** (`scripts/check_bounces.hexa` -> `python3 check_bounces.py`); the `.py` was deleted under HEXA-FIRST policy.
- **LOC estimate**: ~150 (vs send.hexa 590; bounce check is read-only, smaller surface).
- Pattern: reuse `load_token_map()` + `refresh_access_token()` from `send.hexa`; single Gmail REST call:
  `GET https://gmail.googleapis.com/gmail/v1/users/me/messages?q=from:postmaster%20OR%20from:mailer-daemon&maxResults=10`
- **Recommendation**: separate task launch. Manual D+1 check is sufficient bridge.

## 7. send_history.json checkpoint append schema

Per #89 §5 — append target documented at `state/n_22_levin_monitor_2026_05_02/send_history_checkpoint_append.json`. Race-isolated: this monitor task does NOT modify `/Users/ghost/core/contact/data/send_history.json`. Enrichment append occurs when a checkpoint transitions (PENDING -> CLEAN/BOUNCED, false -> received, null -> sent, etc.) and is performed by the corresponding day's monitor invocation.

## 8. Race isolation

Writes confined to:
- `state/n_22_levin_monitor_2026_05_02/schedule.json`
- `state/n_22_levin_monitor_2026_05_02/send_history_checkpoint_append.json`
- `state/n_22_levin_monitor_2026_05_02/follow_up_template.md`
- `state/n_22_levin_monitor_2026_05_02/manual_check_checklist.json`
- `docs/n_22_levin_monitor_schedule_2026_05_02.md` (this file)

No edits to `state/levin_send_2026_05_02/*` (immutable send record) or `/Users/ghost/core/contact/data/send_history.json` (existing entry preserved).
