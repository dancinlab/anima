# commit_msg_diff_alignment_lint — Design (2026-04-28)

## raw#85 strengthening (escalation-audit-trail-witness)

Prior audit (`a8e5c7a2` lineage) discovered:

- commit `50002d89` subject = `fix(an11-fire18): Mode H fix #4 — cuda_max_good>=12.8 ...`
- diff top-1 (by LoC change) = `anima-clm-eeg/tool/clm_eeg_lz76_real.hexa  +568 LoC`
- ⇒ subject scope tag (`an11-fire18`) does NOT appear in any of the top files.
- ⇒ silent attribution drift / commit message acts as cover for unrelated work.

Lint goal: catch this class of drift at landing time (audit-only, no hook
enforcement — raw#13 hooks ban respected).

---

## Algorithm

1. **Parse subject** — `git log -1 --format=%s <sha>`, take first line, ≤70 chars.
2. **Extract scope tag** — regex `<type>\(<scope>\):` →
   `type ∈ {feat, fix, docs, refactor, test, chore, witness, omega-cycle,
   release, math-limit, fire, strengthen}`; `scope` is the inside of `()`.
3. **Tokenize scope** — split scope on `[-_/]` → keyword set `K`.
   Drop stopwords `{a, an, v1, v2, v3, fix, the}`.
4. **Diff top files** — `git show --numstat <sha>` →
   sort by `added + deleted` desc → take top-3 file paths.
5. **Alignment check** — for each keyword `k ∈ K`:
   - PASS-strict: `k` substring-matches any path in **top-1** (case-insensitive).
   - PASS-warn:  `k` substring-matches any path in **top-3** but not top-1.
   - FAIL:       `k` matches none of top-3.
6. **Verdict** — strictest keyword wins (one FAIL ⇒ FAIL_MISMATCH;
   else any WARN ⇒ WARN_LOOSE; else PASS).

### Special cases

- **doc-only commits** (`docs(...)`): top file under `docs/` or `*.md` ⇒ auto-PASS.
- **multi-scope** (`omega-cycle(C1+manifest)`): both scopes treated as
  alternatives — one match suffices.
- **session/closure commits** (no scope or scope == repo name) ⇒ exempt (NO_SCOPE).
- **release commits** ⇒ exempt (release scope is intentionally repo-wide).

### Severity

- `FAIL_MISMATCH` — scope keyword absent from top-3. Block = false (audit-only).
- `WARN_LOOSE`   — scope present in top-3 but not top-1.
- `PASS`         — scope present in top-1.
- `NO_SCOPE`     — could not parse scope tag (exempt).
- `EXEMPT`       — release / docs / merge.

---

## Implementation

- `anima-eeg/tool/commit_msg_diff_alignment_lint.hexa` — pure-hexa wrapper
  (raw#9), emits a `/tmp` python helper (raw#37 transient) that runs `git`.
- ~80 LoC hexa + ~120 LoC python helper.

### Modes

| Flag                 | Behavior                                              |
|----------------------|-------------------------------------------------------|
| `--selftest`         | 4-mode synthetic fixture suite                        |
| `--audit-sha <sha>`  | Audit single commit                                   |
| `--audit-recent N`   | Audit recent N commits, write summary                 |
| (no flag)            | usage                                                 |

### Frozen criteria (raw#12)

- Top-N = 3 (top-1 strict, top-3 warn cushion).
- Subject truncation = 70 chars (Conventional Commits standard).
- Stopwords frozen at landing.
- Verdict labels frozen: `PASS / WARN_LOOSE / FAIL_MISMATCH / NO_SCOPE / EXEMPT`.

---

## Falsifiers (raw#71, ≥5)

- F1 (true positive — honest C3 nuance): commit `50002d89` MUST yield
  `FAIL_MISMATCH` OR `WARN_LOOSE`.  Empirical run produces `WARN_LOOSE`:
  the scope token `an11` IS present in top-3 (`state/an11_fire_*/boot.log`)
  but NOT in top-1 (`anima-clm-eeg/tool/clm_eeg_lz76_real.hexa  +568 LoC`).
  Lint correctly flags the drift — the dominant LoC change is unrelated to
  the declared scope.  Either `FAIL_MISMATCH` (strict) or `WARN_LOOSE`
  (top-3 cushion) constitutes a successful detection per the spec.
- F2 (true negative): commit `7ea7453fa`
  (`feat(eeg-daily-life)`, top file `eeg_daily_life_verifier.hexa`)
  MUST yield `PASS`.
- F3 (synthetic mismatch): subject `fix(scope-foo): ...` + diff top
  `bar/qux.hexa` MUST yield `FAIL_MISMATCH`.
- F4 (synthetic exempt): subject `release(...): ...` MUST yield `EXEMPT`.
- F5 (synthetic warn): scope keyword in top-3 but not top-1 MUST yield
  `WARN_LOOSE`.
- F6 (no-scope): subject `merge: ...` (no `()`) MUST yield `NO_SCOPE`.

---

## Integration

- Lint is **audit-only**, NOT a git hook (raw#13 hooks ban respected).
- Recommended invocation: daily cron via hive-init or manual:
  ```
  hexa run anima-eeg/tool/commit_msg_diff_alignment_lint.hexa --audit-recent 100
  ```
- Output → `/tmp/anima_commit_msg_drift_audit.md` (raw#37 transient by default).

---

## hexa-lang upstream RFC (raw#159 candidate)

Cross-repo applicable: hexa-lang, airgenome, anima all share commit-msg
discipline. RFC-009 candidate: lift to `$HEXA_LANG/tool/` if mismatch rate
≥ 5% across 3 repos and lint stable for ≥ 7 days. **DEFERRED** to a separate
cycle per task instructions; this lands in anima first.

---

## Compliance

- raw#9   pure-hexa wrapper, .py helper /tmp-only
- raw#10  honest C3 (audit-only, no enforcement; selftest disclosures kept honest)
- raw#12  frozen criteria (top-N, stopwords, verdict labels)
- raw#13  hooks ban respected (NOT installed as git hook)
- raw#37  transient .py helper to /tmp
- raw#65  idempotent (deterministic stopwords, git read-only)
- raw#71  ≥6 falsifiers
- raw#85  escalation-audit-trail-witness — commit landing now audited
- raw#159 hexa-lang upstream RFC candidate (deferred cycle)
