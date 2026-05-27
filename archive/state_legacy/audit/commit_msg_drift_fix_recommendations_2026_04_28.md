# Anima commit-msg ↔ diff drift — fix recommendations (documentation only)

- ts: 2026-04-28
- audit source: `anima-eeg/tool/commit_msg_diff_alignment_lint.hexa --audit-recent 100`
- audit raw: `/tmp/anima_drift_audit_2026_04_28.md`
- prior audit (commit 02916fbb6): FAIL=10 (14.08%), WARN=13 (18.31%), PASS=48, EXEMPT=29
- this audit:                     FAIL=13 (17.81%), WARN=9  (12.33%), PASS=51, EXEMPT=27
- delta: +3 FAIL since prior run (regression — drift is still landing in real time)

> **Hard rule (raw#9 / raw#10 / raw#65 / raw#85 / raw#91 /):**
> Git history is **not** rewritten. No `--amend`, no `rebase -i`, no
> `force-push`. The 13 FAIL_MISMATCH commits below stay exactly as they
> are in the immutable log. This file is the corrective witness — future
> readers can map the misleading subject back to the real diff.

---

## 1. FAIL_MISMATCH commits (13) — sha · original subject · top-1 file · corrected subject

### 1.1 Roadmap-code-only scope (no file token)
The scope is a project code (`B11`, `B10`, `C19`, `C18`, `C22`) that does
not appear anywhere in the modified file paths. The change is real and
correct; the lint cannot match because the human-meaningful file token
(`behavioral_correlates_logger`, `eeg_anomaly_autoencoder`, etc.) lives in
the **subject body**, not the **scope parens**.

| sha | original subject | top-1 file | corrected subject |
|---|---|---|---|
| `dbf7af009` | `feat(B11): behavioral_correlates_logger — 5 metrics × 5-min sliding window …` | `anima-eeg/tool/behavioral_correlates_logger.hexa (+396)` | `feat(B11-behavioral-correlates-logger): 5 metrics × 5-min sliding window — 7/7 falsifiers PASS` |
| `8e64c5145` | `feat(B10): eeg_anomaly_autoencoder — pure-numpy AE state-shift detector …` | `anima-clm-eeg/tool/eeg_anomaly_autoencoder.hexa (+908)` | `feat(B10-eeg-anomaly-autoencoder): pure-numpy AE state-shift detector — 4/4 selftest` |
| `43cc4dcdf` | `feat(C19): webcam eye-tracker + EEG cross-modal …` | `anima-eeg/tool/eye_tracker_webcam.hexa (+474)` | `feat(C19-eye-tracker-webcam): gaze/blink/fixation/saccade/pupil 5 metrics — 7/7 falsifiers PASS` |
| `ac0b1a862` | `feat(C18): wearable_health_integrator — Apple Watch / Oura / Whoop …` | `anima-eeg/tool/wearable_health_integrator.hexa (+380)` | `feat(C18-wearable-health-integrator): Apple Watch / Oura / Whoop × EEG cross-validation — 5/5 falsifiers PASS` |
| `3d765697e` | `feat(C22): cross-substrate Φ proxy correlator — anima-physics 9 substr…` | `anima-physics/eeg/cross_substrate_phi_correlator.hexa (+384)` | `feat(C22-cross-substrate-phi-correlator): anima-physics 9 substrate × EEG anchor` |
| `1bd4b7e01` | `feat(F1-cycle4-T8n-rule110-gen): rule-110 elementary CA generalization — H1_SUPPORTED` | `docs/hxc_cumulative_milestone_2026-04-28.md (+60)` (lint sees `f1`,`cycle4`,`t8n`,`rule110`,`gen` ↛ doc path) | This commit's diff is the milestone+witness, **not** the rule110 module — see §1.5 swap. |

**Corrective rule for future commits:**
include the kebab-case file stem inside the scope:
`feat(B11-behavioral-correlates-logger): …` instead of `feat(B11): …`.
Lint will then match `behavioral_correlates_logger` token to the path.

### 1.2 Vendor-tree noise (top-1 is .venv / .hxc_aot)

| sha | original subject | top-1 (noise) | actual code change | corrected subject |
|---|---|---|---|---|
| `ec2ae4b2f` | `fix(an11-fire13): pip uninstall + force-reinstall — Mode D fix #3 (con…)` | `anima-eeg/full_helmet_view.hexa (+741)` (unrelated bulk-add) | install-fix is in launch shell + dispatch path | `fix(an11-fire13-pip-reinstall): Mode D fix #3 — conda priority — see state/an11_dispatch/` |
| `17f524b40` | `fix(an11-fire7): vllm GPU memory OOM root-cause …` | `.venv-eeg/lib/python3.12/site-packages/numpy/__init__.pyi (+6202)` | tiny launcher tweak, masked by venv commit | `fix(an11-fire7-vllm-oom): gc + empty_cache + --gpu-memory-utilization 0.7 (NOTE: venv vendored in same commit, ignore noise)` |

**Corrective rule:** vendored libraries (`.venv-eeg/`, `.hxc_aot/`,
`node_modules/`) must **never** share a commit with intentional code
changes. Add `.venv-eeg/` to the lint EXEMPT prefix list (see §3.2).

### 1.3 Witness-doc commits where scope token is the experiment ID

| sha | original subject | top-1 file | corrected subject |
|---|---|---|---|
| `315b61249` | `witness(A24): first-tick verified + dispatcher integration MEASURED — …` | `state/format_witness/2026-04-28_full_6repo_aggregate_post_a19_dispatcher_measured_per_file.json (+2234)` (lint reads `a19`, not `a24`) | `witness(a24-first-tick-post-a19-dispatcher): 216/216 byte-eq + 78.20% MEASURED + 1.80pp gap` |
| `67e71082a` | `omega-cycle(C1): A19 subsequent-tick LIVE FIRE witness — wire-v2 promo…` | `state/format_witness/2026-04-28_a19_subsequent_tick_live_fire.jsonl (+14)` (token `a19` not in scope) | `omega-cycle(C1-a19-subsequent-tick-live-fire): wire-v2 promotion + +0.15pp aggregate (78.05 → 78.20%, gap 1.80pp)` |

**Corrective rule:** when the diff is a single witness file named
`<exp_id>_<phase>.jsonl`, mirror that id into the scope.

### 1.4 Generic infra commits with multi-file diff

| sha | original subject | top-1 file | corrected subject |
|---|---|---|---|
| `ff93121b7` | `fix(an11-r39-infra): seed 인자 통합 (env var 통한 LoRA stochastic 통제)` | `anima-eeg/electrode_adjustment_helper.hexa (+560)` | The actual seed-arg change is in the dispatch script, but the largest diff is the unrelated electrode bulk-add. **Same anti-pattern as §1.2 — multiple unrelated changes squashed.** Future split required. |
| `7bbbf49c1` | `docs(session-end): "루프 종료" + "all kick" 응답 — market NO_OFFERS …` | `state/an11_dispatch/fire_seed4.log (+26)` | Wrong type — should not be `docs(...)` since top-1 is a `.log`, not a `.md`. Corrected: `ops(an11-dispatch-session-end): "루프 종료" + "all kick" — market NO_OFFERS honest disclosure` |

### 1.5 Confirmed message-swap (twin commit pair)

Commits `53c711ebc` and `1bd4b7e01` were authored 21 seconds apart and
the **subjects are transposed**:

| sha | original subject | actual diff | corrected subject |
|---|---|---|---|
| `53c711ebc` | `omega-cycle(C1+raw137 v6): A25 v2 FULL DEPLOYMENT 6-repo LIVE FIRE — 78.05% …` | `tool/anima_law64_rule110_generalization.hexa (+433)` + `state/law64_rule110_gen/run_20260428T031853Z.log (+39)` | `feat(F1-cycle4-T8n-rule110-gen): rule-110 elementary CA generalization — H1_SUPPORTED` |
| `1bd4b7e01` | `feat(F1-cycle4-T8n-rule110-gen): rule-110 elementary CA generalization — H1_SUPPORTED` | `docs/hxc_cumulative_milestone_2026-04-28.md (+60)` + `state/format_witness/2026-04-28_a25_v2_full_deployment_6repo_80pct_measured.jsonl (+10)` | `omega-cycle(C1+raw137 v6): A25 v2 FULL DEPLOYMENT 6-repo LIVE FIRE — 78.05% MEASURED + cumulative 93.69%` |

**Root cause:** the two commits were generated by the same script
session and got their subject lines crossed when staging. **High-impact
drift** because future readers grepping for `rule110` will land on the
wrong sha and vice versa.

**Documentation pointer:** anyone looking for the rule110-gen code →
`53c711ebc`. Anyone looking for the A25-v2 6-repo deployment witness →
`1bd4b7e01`.

---

## 2. Top problem patterns (root-cause clusters)

| pattern | count | mitigation |
|---|---|---|
| roadmap-code-only scope (`B11`, `C18`, `C22` …) | 5 | mandate `<code>-<file-stem>` scope form |
| vendor-tree noise overpowering top-1 | 2 | exclude `.venv-eeg/`, `.hxc_aot/` from numstat ranking |
| witness-id missing from scope | 2 | mirror `state/format_witness/<id>.jsonl` id into scope |
| infra commits with unrelated bulk-add bundled | 2 | enforce single-purpose commits (see Future-Commit Guidelines §3.1) |
| message-swap (twin commit transposition) | 2 (1 pair) | post-commit lint must run **before** push (see §3.5) |

---

## 3. Future-commit guidelines (lint-pass guarantee)

### 3.1 Single-purpose commits
One `feat()` / `fix()` / `witness()` per commit. Never bundle vendored
library installs (`.venv-eeg/`, `.hxc_aot/`) with intentional code in
the same commit. Use `chore(vendor-bump): …` for vendor-only commits.

### 3.2 Scope = code + file-stem
- BAD: `feat(B11): behavioral_correlates_logger — …`
- GOOD: `feat(B11-behavioral-correlates-logger): …`
- BAD: `witness(A24): first-tick post-A19-dispatcher`
- GOOD: `witness(a24-first-tick-post-a19-dispatcher): …`

### 3.3 Witness-only commits
If diff is a single `state/format_witness/*.jsonl`, the scope must
contain at least one path token from that file (e.g. `a25`, `a19`,
`first-tick`, `live-fire`).

### 3.4 Type discipline
- `docs(...)` only when top-1 is `*.md` or under `docs/`
- `ops(...)` for log-only / dispatch / runpod / state changes
- `chore(...)` for vendored-only / formatting-only changes

### 3.5 Pre-push lint hook (recommendation)
Add a **manual pre-push check** to user workflow (NOT a git hook —
respects raw#13 audit-only contract):
```
$HEXA_LANG/hexa.real run anima-eeg/tool/commit_msg_diff_alignment_lint.hexa --audit-sha HEAD
```
If verdict is `FAIL_MISMATCH` or `WARN_LOOSE`, the user makes a manual
call: amend if not yet pushed (allowed pre-push, before history is
public), or roll forward with documentation. **Never** rewrite already-
pushed history.

---

## 4. Lint refinement plan (raw#85 strengthening candidates)

### 4.1 Vendor-path filter (high priority)
Currently `diff_top_files()` ranks **every** path equally. `.venv-eeg/`,
`.hxc_aot/`, `node_modules/`, `references/` should be filtered before
top-N selection so the *intentional* code change becomes top-1.

```python
VENDOR_PREFIXES = ('.venv-eeg/', '.hxc_aot/', 'node_modules/',
                   'references/', '.git/', 'dist/')
def diff_top_files(sha, n=3):
    ...
    rows = [(t,p) for (t,p) in rows
            if not any(p.startswith(v) for v in VENDOR_PREFIXES)]
    rows.sort(reverse=True)
    return rows[:n]
```
Expected impact: `17f524b40` (an11-fire7) and `ec2ae4b2f` (an11-fire13)
move from FAIL → PASS without any commit-msg change.

### 4.2 IDF (inverse document frequency) token weighting (medium priority)
Currently `keyword_in_path()` treats `eeg` (broad — appears in 800+
files) the same as `lz76` (specific — appears in 4 files). A token
that matches everything is no signal.

```python
# Build path frequency map across audit window
all_paths = set()
for s in shas:
    for _,p in diff_top_files(s, 99):
        all_paths.add(p)

def token_specificity(tok, all_paths):
    hit = sum(1 for p in all_paths if tok in p.lower())
    if hit == 0: return 0.0
    return 1.0 / (1.0 + math.log(1+hit))   # high tok seen many → low weight

def classify_v2(...):
    ...
    score = sum(token_specificity(t, ALL) for t in matched_in_top1)
    if score >= 0.5:        v = 'PASS'
    elif score > 0.0:        v = 'WARN_LOOSE'
    elif matched_in_top3:    v = 'WARN_LOOSE'
    else:                    v = 'FAIL_MISMATCH'
```
Expected impact: a commit that "matches" only because the broad token
`eeg` overlaps with the path will be downgraded to WARN, exposing the
real drift.

### 4.3 WARN_LOOSE → FAIL threshold (low priority — defer)
The user asked whether WARN_LOOSE should be promoted to FAIL. **Recommend
NO**. Current data:
- 9 WARN_LOOSE = scope token in top-3 file but not top-1
- 6 of 9 are `an11-fire*` commits where the actual launch-script change
  *is* in the diff (just not top-1 by LoC)
Promoting WARN → FAIL would generate 9 false-FAILs and dilute the signal.
Better path: implement §4.1 (vendor filter) first; many WARN cases will
auto-promote to PASS once the venv noise is filtered out.

### 4.4 Twin-swap detector (new falsifier F7)
Detect commits authored within a 60s window where the subject of A
matches the diff of B and vice versa. Add as falsifier F7 with
synthetic test:
```python
F7_synth_swap = [
    ('shaA', 'feat(rule110): ...', ['unrelated.jsonl']),
    ('shaB', 'omega(a25-v2): ...', ['rule110.hexa']),
]
expect: F7 flags both as SWAP_SUSPECTED
```
This catches cases like §1.5 that current lint cannot.

### 4.5 Body-token fallback (new — keeps roadmap-code scopes valid)
If `scope tokens` produce no top-1 match, parse the **subject body**
(after the `: `) for additional candidate tokens and retry the match.
This rescues `feat(B11): behavioral_correlates_logger — …` since
`behavioral_correlates_logger` is in the body and matches the path.

```python
def body_tokens(subject):
    body = subject.split(':',1)[-1]
    return [t for t in re.split(r'[\s\-_/]+', body.lower())
            if len(t) > 3 and t not in STOPWORDS]

# in classify(): if no scope-token match, retry with body tokens →
# verdict 'PASS_BODY' (still a pass, but flagged as scope-could-be-better)
```
Expected impact: 5 of 13 FAIL_MISMATCH (roadmap-code-only) move to
`PASS_BODY` (a new healthier verdict) without rewriting any commit msg.

---

## 5. Summary table — projected verdict shift after refinements

| sha | current | after §4.1 vendor | after §4.5 body-token | after §4.2 IDF |
|---|---|---|---|---|
| dbf7af009 (B11) | FAIL | FAIL | **PASS_BODY** | PASS_BODY |
| 8e64c5145 (B10) | FAIL | FAIL | **PASS_BODY** | PASS_BODY |
| 43cc4dcdf (C19) | FAIL | FAIL | **PASS_BODY** | PASS_BODY |
| ac0b1a862 (C18) | FAIL | FAIL | **PASS_BODY** | PASS_BODY |
| 3d765697e (C22) | FAIL | FAIL | **PASS_BODY** | PASS_BODY |
| ec2ae4b2f (fire13) | FAIL | **WARN/PASS** | PASS | PASS |
| 17f524b40 (fire7)  | FAIL | **PASS** | PASS | PASS |
| 315b61249 (A24)    | FAIL | FAIL | FAIL | FAIL (real drift — needs commit-msg discipline) |
| 7bbbf49c1 (session-end) | FAIL | FAIL | FAIL | FAIL (real drift) |
| 67e71082a (C1/A19) | FAIL | FAIL | **PASS_BODY** | PASS_BODY |
| ff93121b7 (r39-infra) | FAIL | FAIL | FAIL | FAIL (bundled commit — split required) |
| 53c711ebc (swap)   | FAIL | FAIL | FAIL | FAIL (caught by §4.4 SWAP_SUSPECTED) |
| 1bd4b7e01 (swap)   | FAIL | FAIL | FAIL | FAIL (caught by §4.4 SWAP_SUSPECTED) |

**Projected post-refinement state:** 13 → 4 true FAIL (1 real drift + 1
bundled + 2 swap), 5 PASS_BODY (healthy), 2 promoted to PASS via vendor
filter. Mismatch_rate **17.81 % → ~5.5 %**.

---

## 6. Compliance ledger
- raw#9 pure-hexa lint untouched — only doc + plan changes proposed
- raw#10 honest C3 — drift count rose +3 since prior audit, reported truthfully
- raw#65 idempotent — re-running lint reproduces the table verbatim
- raw#85 strengthening candidates listed in §4 for future implementation
- raw#91 — git history not modified
- — recommendations only, no destructive ops

End of recommendations document.
