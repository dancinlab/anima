# mk2 Naming Convention — Paradigm-Letter Stage-Prefix Amendment (LANDED)

- date: 2026-05-03
- status: LANDED (additive amendment)
- scope: `tool/hf_upload_mk2.hexa` validator + `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` spec
- trigger: Paradigm J 5/5 HF push recovery BG (a915bca5) bypassed mk2 wrapper
- raw constraints: raw#9 STRICT (hexa-only on Mac), raw#10 (4 honest C3 caveats), raw#15 (no personal-path leak)
- cost: $0 (mac local, no GPU, no HF API mutation in this cycle)
- destructiveness: 0 (no rename/delete; spec §3.2.1 additive; validator allow-list expanded)
- byte-diff to existing HF artifacts: 0

---

## §1 Why this cycle

The Paradigm J HF recovery BG (a915bca5) attempted to push
`need-singularity/clm-v4-paradigm-j-50k-step-{5k,10k,25k,50k,final}`
via the canonical mk2 wrapper. The wrapper rejected the names with:

```
FAIL: stage must start with one of {sft-stage|dpo|merged|base|preview|dev}
      (got: 'paradigm-j-50k-step-5k')
```

The recovery BG worked around this by bypassing the wrapper (raw `hf upload`
shell-out). The push succeeded, but the bypass leaves a hole in the
audit/validation discipline. This amendment closes that hole.

---

## §2 Root cause

The validator implementation in `tool/hf_upload_mk2.hexa` collapses every
post-version segment of the repo name into a single "stage_join" string and
matches against `_naming_allowed_stage_prefixes()`. The §2.1 EBNF in the
spec already defines `paradigm` as an optional slot *between* `base_version`
and `stage`, but the validator does not parse that distinction — it treats
everything after `<lm>-<vN>-` as the stage chain.

The spec §3.3 already enumerates 7 ratified paradigm letters
(`a`/`a-prime`/`b`/`c`/`d`/`e`/`j`), but the validator never consulted them.

---

## §3 Amendment

### 3.1 Spec change

Added `§3.2.1 stage-prefix amendment — paradigm-{letter} (2026-05-03 additive)`
to `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` immediately after
§3.2 base-version. The new section documents:

- the trigger (BG a915bca5)
- the rationale (paradigm-axis ≠ stage-axis but validator collapses them)
- the validator allow-list change (`paradigm-` prefix added)
- the SSOT split (validator is loose; §3.3 table is strict for ratified letters)
- the smoke test that must now PASS
- the retroactive scope (Paradigm J's bypass-pushed repos NOT auto-compliant)

### 3.2 Validator change

`tool/hf_upload_mk2.hexa` (version 2.0.1 → 2.0.2):

- `_naming_allowed_stage_prefixes()` allow-list: appended `"paradigm-"`
- error message updated to include `paradigm-` in the rejection text
- doc-block before the `_naming_validate` family/stage section updated with
  the amendment rationale + ref to spec §3.2.1

No other validator rule mutated. Family enum, README validator, sha256/walk
helpers, upload pipeline — all untouched.

---

## §4 Smoke test

```
$ hexa run tool/hf_upload_mk2.hexa --validate-naming \
    "need-singularity/clm-v4-paradigm-j-50k-step-5k"
OK
__ANIMA_HF_UPLOAD_MK2__ PASS
```

| repo | expected | actual |
|---|---|---|
| `clm-v4-paradigm-j-50k-step-5k` | PASS | PASS |
| `clm-v4-paradigm-a-prime-step-10k` | PASS | PASS |
| `blm-v1-paradigm-d-distill-50k-final` | PASS | PASS |
| `clm-v4-sft-stage1` (regression check) | PASS | PASS |
| `zzz-v4-bogus-stage` (rejection check) | FAIL family | FAIL family |
| `clm-v4-bogus-stage` (rejection check) | FAIL stage | FAIL stage |

Selftest:

```
$ hexa run tool/hf_upload_mk2.hexa --selftest
[P] readme validator: good=OK, bad=rejected
[P] naming validator: good=OK, bad=rejected
[P] hexa selftest: selftest: PASS
__ANIMA_HF_UPLOAD_MK2__ PASS
```

Full smoke audit at
`state/mk2_naming_paradigm_amendment_2026_05_03/smoke_test.json`.

---

## §5 raw#10 honest C3 caveats (4)

### C1 — paradigm enum may need future additions

The §3.3 spec table currently ratifies 7 letters
(`a`/`a-prime`/`b`/`c`/`d`/`e`/`j`). The validator was deliberately made
*looser* than the §3.3 table (it accepts any `paradigm-<anything>` prefix)
to avoid forcing a second SSOT amendment cycle every time a new paradigm
letter is ratified. Trade-off: a typo or rogue letter (e.g.
`clm-v4-paradigm-zzz-step-5k`) now passes the validator. Mitigation: the
§3.3 table remains the authoritative ratification source — audit cycles
must cross-check published HF repos against §3.3, not against the validator.

### C2 — validator regex may need EBNF re-alignment

The §2.1 EBNF treats `paradigm` and `stage` as *separate* optional slots.
The validator implementation collapses them. This amendment makes the
validator *accept* paradigm-prefixed names, but it does not actually parse
the slots distinctly. A future cycle that wants strict slot parsing (e.g.
to enforce "paradigm slot must come before stage slot, not after") will
need a deeper validator rewrite — this amendment is not that rewrite.

### C3 — retroactive validation not enforced

This amendment is forward-looking. The validator now accepts paradigm-
prefixed names for *future* pushes. It does NOT scan the existing 27
need-singularity repos and re-classify the previously-pushed Paradigm J
repos. A separate audit cycle (cf. spec §15 next-cycle candidates) is
needed to (a) sweep all public repos through the amended validator and
(b) update the §7.2 audit table with the new CANON/EXT/FAIL distribution.

### C4 — Paradigm J HF push doesn't auto-retroactively gain mk2 compliance

The Paradigm J BG (a915bca5) pushed via wrapper bypass. Those repos are
named correctly per the amended validator, but they were not pushed
*through* the wrapper — so the wrapper's audit log
(`state/hf_upload_audit/`) and ledger
(`state/hf_upload_ledger_2026_05.jsonl`) have no record of those uploads.
sha256 manifests, README validation, and per-repo audit JSONL are missing
for the J5/5 pushes. Re-running the push through the wrapper would create
a duplicate commit (LFS sha-stable so no byte change, but a no-op commit
on `main`). Decision: accept the audit-log gap; document it here; require
all Paradigm D/E/J *future* pushes to go through the wrapper. The
state/mk2_naming_paradigm_amendment_2026_05_03/audit.json captures this
provenance for downstream cycles.

---

## §6 Files touched

| file | change |
|---|---|
| `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` | additive §3.2.1 |
| `tool/hf_upload_mk2.hexa` | `_naming_allowed_stage_prefixes` allow-list + version 2.0.2 + error msg + doc block |
| `state/mk2_naming_paradigm_amendment_2026_05_03/audit.json` | NEW |
| `state/mk2_naming_paradigm_amendment_2026_05_03/smoke_test.json` | NEW |
| `state/markers/mk2_naming_paradigm_amendment_landed.marker` | NEW |
| `docs/mk2_naming_paradigm_amendment_landed_2026_05_03.ai.md` | NEW (this handoff) |

---

## §7 Next-cycle candidates (NOT this cycle)

| item | priority | rationale |
|---|---|---|
| Re-run Paradigm J HF recovery via mk2 wrapper (verification dry-run) | MED | Validates the validator amendment against real-world J5/5 repos; produces missing audit log entries |
| Audit sweep: re-classify 27 public repos against amended validator | MED | Updates §7.2 audit table; resolves C3 caveat |
| Strict slot-aware validator rewrite (EBNF parity) | LOW | Resolves C2 caveat; requires deeper hexa parser work |
| §3.3 closure for forward letters (F/G/H/I) | LOW | If/when those paradigms ratify, add table rows |
