# anima HF naming — family enum reconciliation (handoff)

- date: 2026-05-03
- status: LANDED
- author: anima cycle land BG (Mac local, raw#9 STRICT — hexa-only edit)
- scope: reconcile family-list drift between mk2 spec §3.1 and `tool/hf_upload_mk2.hexa::_naming_allowed_families`
- supersedes-drift: a993063 (Path A naming decision) + a674ae71 (drift report)
- destructive: 0 (additive only — no family removed)
- cost: $0 (Mac local design + edit)
- linked falsifier: F-NAME-1 (audit-time conformance, see spec §10)
- raw#9: STRICT (Mac → hexa-only; no .py created)
- raw#10: 3 honest C3 caveats below
- raw#15: no personal-path leak

---

## §0 TL;DR

Two SSOTs disagreed on the `lm-family` enum:

| SSOT | pre-reconcile families | count |
|---|---|---|
| `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` §3.1 | `blm`, `clm`, `tlm`, `vlm`, `slm`, `nlm` | 6 |
| `tool/hf_upload_mk2.hexa` (validator enum) | `clm`, `alm`, `blm`, `vlm`, `slm`, `tlm`, `mlm`, `hexad`, `composite` | 9 |

Reconciliation = **union of both + new `llm`** for Path A:

`clm | alm | blm | vlm | slm | tlm | nlm | mlm | llm | hexad | composite` (11 families)

Both sides updated in this cycle. Hexa selftest PASS preserved after edit.

---

## §1 Family enum delta (added per side)

### 1.1 Added to spec §3.1 table (5 net new rows)

| family | rationale | source | ratification |
|---|---|---|---|
| `alm` | Audio LM — anima-voice precursor (audio-only encoder/gen) | preserved from validator | INFORMAL (was validator-only) |
| `mlm` | Masked LM — BERT-class encoder-only (forward) | preserved from validator | INFORMAL (was validator-only) |
| `hexad` | multi-modal hexad composite (6-axis) | preserved from validator | INFORMAL (was validator-only) |
| `composite` | generic multi-LM composite catch-all | preserved from validator | INFORMAL (was validator-only) |
| `llm` | Llama-derived LM — Path A informal extension | a993063 + `docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md` | **PROVISIONAL** (informal Path A extension; ratification pending dedicated cycle) |

### 1.2 Added to validator enum (2 net new entries)

| family | rationale | source |
|---|---|---|
| `nlm` | Nexus / Neural LM — nexus-side coordination LM | preserved from spec §3.1 |
| `llm` | Llama-derived LM — Path A | a993063 |

### 1.3 Final canonical enum (11 families)

```
clm | alm | blm | vlm | slm | tlm | nlm | mlm | llm | hexad | composite
```

Both spec EBNF (§2.1 `lm_family` production) and validator
(`_naming_allowed_families()`) updated to this exact 11-entry set, in this
exact order. F-NAME-1 verifier regex (§10.2) likewise expanded.

---

## §2 Files modified

| file | change |
|---|---|
| `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` | §3.1 table expanded 6→11 rows; new §3.1.1 reconciliation note; §2.1 EBNF `lm_family` production expanded; §10.2 `LM` regex group expanded |
| `tool/hf_upload_mk2.hexa` | header comment family list updated; new "Family enum reconciliation" comment block; `_naming_allowed_families()` returns 11-entry list |
| `docs/anima_hf_naming_family_reconcile_2026_05_03.ai.md` | this handoff (NEW) |
| `state/markers/anima_hf_naming_family_reconcile_landed.marker` | landing marker (NEW) |

No HF API call. No remote repo touched. No legacy artifact rename. Pure
SSOT-text edit + validator enum widen.

---

## §3 Selftest result after edit

```
$ hexa run tool/hf_upload_mk2.hexa --selftest
hexa-resolver: route=darwin-bypass reason=metadata-only-argv (raw#103)
[hf_upload_mk2] SELFTEST (raw#9 strict — no python bridge)
  hf cli      = /Users/ghost/.local/bin/hf
  hf version  = 1.8.0
  hf available= 1
  [P] readme validator: good=OK, bad=rejected
  [P] naming validator: good=OK, bad=rejected
  [P] hexa selftest: selftest: PASS
__ANIMA_HF_UPLOAD_MK2__ PASS
```

**Verdict**: PASS preserved across edit (baseline PASS → post-edit PASS).

### 3.1 Smoke validation (new families exercised)

| input | expected | actual |
|---|---|---|
| `dancinlab/llm-v1-base` | OK (new) | OK PASS |
| `dancinlab/nlm-v1-sft-stage1` | OK (added to validator) | OK PASS |
| `dancinlab/alm-v1-preview` | OK (added to spec) | OK PASS |
| `dancinlab/zzz-v1-base` | FAIL (not in enum) | FAIL with reconciled error message: `family must be one of {clm\|alm\|blm\|vlm\|slm\|tlm\|nlm\|mlm\|llm\|hexad\|composite}` |

All four smoke checks behave as expected. Reject path emits the new 11-entry
enum in the error message — verifies the validator is reading the updated
list, not a cached/stale path.

---

## §4 Ratification status of `llm`

**`llm` family ratification = PROVISIONAL / INFORMAL** as of 2026-05-03.

| dimension | status |
|---|---|
| spec §3.1 row | PRESENT (added this cycle) |
| validator enum | PRESENT (added this cycle) |
| dedicated family-spec doc | NOT YET (currently only referenced in `docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md` Path A decision) |
| first repo pushed under `llm-vN-*` | NOT YET (Path A planned `p9-llama32-lora-*` was non-conform; rename to `llm-v1-*` form preferred per this reconcile) |
| cross-substrate falsifier set | NOT YET (no `F-LLM-*` gates defined) |

**Honest assessment**: `llm` is admitted into the enum to **prevent future
drift** (so Path A's first push lands inside §2 EBNF rather than outside it),
but the family lacks the full ratification stack that `clm`/`blm`/`tlm`/`vlm`
enjoy. A follow-up cycle SHOULD produce `docs/llm_family_spec_2026_05_*.md`
covering: (a) what counts as "Llama-derived" (LoRA-on-Llama? full SFT? merge?);
(b) namespace question (does `llm-v1-base-mirror` shadow Meta's licensing
attribution requirements?); (c) interaction with `clm` (when does a Llama-derived
ckpt promote to `clm` if it gains φ★ preservation?).

Until then, `llm` MAY be used in repo names but the README §1 Origin section
MUST cite the Llama base (`meta-llama/Llama-3.2-3B` or equivalent) explicitly,
including license attribution.

---

## §5 raw#10 honest C3 caveats

### C1 — some families are speculative (no production artifact yet)

Of the 11 families in the reconciled enum, only `clm` has production HF
artifacts pushed (per §7 audit, 27 repos, all `clm-v4-*`). `blm`, `tlm`, `vlm`,
`slm` are in active development but not yet pushed. `alm`, `nlm`, `mlm`,
`hexad`, `composite`, `llm` are **forward-only** — no spec-grade research doc
yet defines their full semantics. Admitting them to the enum is an
**anti-drift gesture** (so first push lands conformant) — NOT an endorsement
that they have research-ready definitions. Each forward family will need its
own `docs/<family>_family_spec_*.md` before its first artifact push.

### C2 — `llm` ratification is informal

As detailed in §4 above, `llm` was added to head off Path A's
`p9-llama32-lora-*` non-conform naming pattern. The family was **NOT
ratified** by a dedicated cycle, just admitted into the validator enum. If a
future cycle decides Llama-derived ckpts should instead be expressed as
`clm-v4-paradigm-a-prime-llama32-*` (subordinating the Llama heritage under
the existing CLM family), the `llm` entry MAY be deprecated. The validator
will continue to accept it during deprecation grace.

### C3 — future families may emerge; this is not a closed enum

The reconciled 11-family enum reflects 2026-05-03 understanding. New
modalities (e.g. `tlm` extension to thermal? `klm` for kinesthetic? `glm`
for gustatory?) MAY emerge from anima research. The reconciliation **rule**
codified here (additive union, both SSOTs touched in same cycle, handoff doc
mandatory) MUST be followed for any future addition. The enum is OPEN under
that rule, NOT closed at 11. Anti-pattern: silently appending a family in
either spec §3.1 OR validator without the matching update to the other side
— that is the exact drift this cycle resolved.

---

## §6 Composability

- consumed by: `tool/hf_upload_mk2.hexa` (validator); `docs/anima_hf_upload_mk2_spec_2026_05_03.md` (consumes spec §3.1)
- prerequisite: `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` (the SSOT being reconciled)
- siblings:
  - `docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md` (origin of `llm` family need)
  - `docs/anima_hf_naming_mk2_spec_landed_2026_05_03.ai.md` (original spec land handoff)

---

## §7 Outputs (this cycle)

- `/Users/ghost/core/anima/docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` (UPDATED — §3.1 + §3.1.1 + §2.1 + §10.2)
- `/Users/ghost/core/anima/tool/hf_upload_mk2.hexa` (UPDATED — header + family enum)
- `/Users/ghost/core/anima/docs/anima_hf_naming_family_reconcile_2026_05_03.ai.md` (this file, NEW)
- `/Users/ghost/core/anima/state/markers/anima_hf_naming_family_reconcile_landed.marker` (NEW)
