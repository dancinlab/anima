# rail_audit Sidecar + analyze_wrapper Dump Gitignore Policy (2026-05-03)

**Status**: LANDED · Option B
**Owner**: anima-eeg N4 (analyze_wrapper) · gitignore policy review
**Cycle**: cycle 8 (2026-05-03)
**SSOT artifact**: `.gitignore` (lines ~202–217)

## Decision

**Option B**: gitignore future `.npy.rail_audit.json` sidecar emissions; preserve the 3
already-committed sidecars from commit `e2ce92413` in-place. No `git rm --cached` —
history is not rewritten.

## Rationale

1. **Determinism**: rail_audit.json sidecars are 100% reproducible from
   `analyze_wrapper.hexa --input <npy>`. The .npy parents and .npy.meta.json
   sidecars **are** committed (verified — see `git ls-files
   anima-eeg/recordings/sessions/`), so any future audit can be regenerated from
   the SSOT in seconds.
2. **Diff hygiene**: recurring measurement cycles (Berger v6 → vN) would each
   re-emit a sidecar per recording. Without the gitignore, every cycle pollutes
   git diff with non-load-bearing JSON.
3. **Audit-trail preservation**: the 3 sidecars already in `e2ce92413` cover the
   N4 wrapper landing evidence. Removing them would erase that proof-carrying
   marker — Option B keeps them as historical anchor.

### raw#10 honest C3 — counter-argument considered

Option A (keep all sidecars committed forever) was *not* chosen, but its
strongest argument is acknowledged: rail_audit sidecars are evidence-trail
artifacts, and gitignoring them does lose per-recording traceability after
this cycle. The mitigation: `analyze_wrapper.hexa` is deterministic + the
.npy + meta.json parents are SSOT, so the audit can always be re-emitted with
a single command. The lost trace is only the *who/when ran the wrapper*,
which is recoverable from session ledgers and runbooks.

## Patterns added to `.gitignore`

```
# rail_audit sidecars — Option B (2026-05-03)
anima-eeg/recordings/sessions/*.npy.rail_audit.json
anima-eeg/recordings/protocols/**/*.npy.rail_audit.json

# analyze_wrapper helper transient dumps + selftest sidecars
state/.analyze_wrapper_dump.txt
state/.analyze_wrapper_dump_clean.txt
state/.analyze_wrapper_dump_*.txt
state/analyze_wrapper_selftest_*.rail_audit.json

# Hexa pwd probe artifacts (N2 sandbox confirmation)
state/_hexa_pwd_out.txt
state/_hexa_pwd_probe.hexa
```

Total: 9 new pattern lines (1 sessions glob + 1 protocols glob + 4 state
dump/selftest patterns + 2 N2 probe patterns + 1 explicit dump_clean.txt for
clarity).

## Cross-links

- N4 wrapper SSOT: `anima-eeg/protocols/analyze_wrapper.hexa`
- B-track runbook: `anima-eeg/docs/electrode_reseat_b_track_runbook_2026_05_03.md`
- Cycle 8 commit: `e2ce92413` (3 sidecars committed there)
- Tracked sidecars (preserved):
  - `anima-eeg/recordings/sessions/berger_ec_60s_2026_05_03.npy.rail_audit.json`
  - `anima-eeg/recordings/sessions/berger_ec_60s_v6_2026_05_03.npy.rail_audit.json`
  - `anima-eeg/recordings/sessions/berger_eo_60s_v6_2026_05_03.npy.rail_audit.json`

## Revision triggers

Revisit this policy if **any** of the following occurs:

1. `analyze_wrapper.hexa` schema bumps (currently
   `anima-eeg/analyze_wrapper/1`) — new schema may need explicit per-cycle
   commits for migration tracking.
2. Sidecar size grows >5 KB (currently ~800 B) — large evidence may justify
   separate R2 distribution like other large data tiers.
3. A regulatory / external review demands per-recording audit trail in git
   history → reconsider Option A or move to Option C (untrack legacy + R2
   archive).
4. Wrapper becomes non-deterministic (e.g., adds wall-clock-derived fields
   beyond `timestamp_utc`) — sidecars would no longer be re-runnable from
   parent .npy.

## Open question

Should `state/analyze_wrapper_selftest_*.rail_audit.json` instead live under
a tracked `state/_selftest_evidence/` folder with a different schema, so
that selftest passes are committed evidence while live-run sidecars stay
ignored? Defer to next anima-eeg cycle review.
