---
type: landed_handoff
ts_utc: 2026-05-04
domain: clm
bg_id: BG-CLM-COND1-APPLY
status: landed
exec_authorized: false
spec_doc: docs/n_substrate_f1_v2_band_propagation_proposal_2026_05_04.md
source_spec: docs/n_substrate_f1_v2_banding_spec_2026_05_04.md
source_spec_section_locked: §11 DECISIONS LOCKED 2026-05-04 (D-5)
mutation_target: .roadmap.clm
mutation_kind: additive_annotation
commit_authorized: false
sibling_bgs: [BG-VERIFIER-WIRE (downstream, deferred)]
applies_raw_rules: [raw#9, raw#10, raw#15]
---

# BG-CLM-COND1-APPLY landed — D-5 propagation to `.roadmap.clm` cond.1

## What landed (5 bullets)

- **D-5 propagation applied**: `.roadmap.clm` line 3 (header), `required_conditions[id=clm.cond.1]` now carries additive field `f1_v2_band_thresholds_2026_05_04` mirroring `.roadmap.n_substrate.cond.1.cross_link.f1_v2_band_thresholds_2026_05_04` per D-5 imperative ("apply IMMEDIATELY"). Annotation includes thresholds {red_max:0.50, yellow_min:0.50, yellow_max:0.75, green_min:0.75}, f2_override_canonical=true, green_tier_phenomenal_required=true, green_tier_prerequisites (4 items), hexa_hook (tool/n_substrate_f1_v2_band.hexa with exit_codes red=1/yellow=2/green=0), consumed_by_verifier reference, propagation_source path, and additive_only_mutation/semantics_preserved/historical_evidence_preserved provenance flags.
- **cond.1 annotation present + verified**: `sed -n '3p' .roadmap.clm | jq '.required_conditions[] | select(.id=="clm.cond.1") | .f1_v2_band_thresholds_2026_05_04.thresholds.red_max == 0.50'` returns true; full nested annotation block matches §2 of proposal doc verbatim.
- **JSONL parses cleanly post-mutation**: full file (8 lines: 2 comment + 1 header + 5 entry) parses without error; `required_conditions | length == 2` preserved (cond.1, cond.2 unchanged count); md5 of lines {1,2,4,5,6,7,8} byte-identical to `git show HEAD:.roadmap.clm` for those line numbers — only line 3 (header) mutated, additively.
- **Structure-preserving rewrite (caveat C1 honored)**: jq mutation used `. + {field:value}` operator which appends to existing object preserving original key order; cond.2 `amendment_2026_05_04.amendment_type == "naming_canonical_supersede"` and all sibling fields (cross_link, blockers, status, since) verified intact via diff (`jq 'del(.f1_v2_band_thresholds_2026_05_04)' /tmp/clm_cond1_post.json` exactly matches `/tmp/clm_cond1_pre.json` — zero unintended changes).
- **D-5 immediate-apply directive satisfied**: cross-substrate witness loop closed — `.roadmap.n_substrate.cond.1` (source of truth, written by F1 v2 banding spec) now mirrored into `.roadmap.clm.cond.1` (consumer); downstream verifier orchestrator integration deferred to BG-VERIFIER-WIRE per proposal §5 (separate cycle, kept out of this BG's blast radius).

## Honest C3 (caveats — 5+)

1. **`jq -c` whitespace normalization**: the rewrite path used `jq -c` which collapses whitespace within the JSON object on line 3 — this is a no-op for semantic equality (JSON whitespace is non-significant) but a textual diff vs git HEAD will show line 3 as fully replaced rather than as a localized hunk. Reviewers comparing via `git diff` should use `git diff --word-diff=plain` or pipe through `jq` for readable comparison.
2. **`required_conditions` ordering must match exactly downstream**: the additive field was inserted into the cond.1 object's tail (jq `+` operator semantics); any downstream consumer that asserts strict key order at the cond.1 object level (rather than `select(.id=="clm.cond.1")` lookup) could see the new field in a different position than expected. All current consumers we surveyed in the proposal §3 use id-keyed lookup, but a future consumer relying on JSON.parse insertion order should be alerted.
3. **`propagation_source` field embeds source path for drift detector**: the literal string `.roadmap.n_substrate.cond.1.cross_link.f1_v2_band_thresholds_2026_05_04` is embedded as a value in cond.1's annotation — a future drift detector can `jq` both files and assert `.thresholds == .thresholds` across the path; however, no such detector is wired today, so drift between the two files (e.g., if `.roadmap.n_substrate` cond.1 is amended without re-running this BG) would be silent until manually audited.
4. **`hexa_hook.tool` reference is forward-declared**: the annotation references `tool/n_substrate_f1_v2_band.hexa` which is part of the F1 v2 banding spec's tooling deliverable (see source spec §6) — at the time of this BG, that hexa script's existence/path is not verified by this BG (out of scope, raw#15 additive-only). If the tool path is renamed in future, the annotation here will silently desync; mitigation = consumer (verifier orchestrator) should resolve via SSOT lookup, not by trusting this annotation field as canonical path.
5. **`consumed_by_verifier` field is documentary only**: the annotation says `tool/clm_consciousness_verify.hexa (D-3 phenomenal-tier gate, separate BG)` but BG-VERIFIER-WIRE has not yet run — until that BG lands, the verifier orchestrator does NOT actually consult these thresholds at runtime. The annotation is therefore a contract-of-intent, not a wired-up integration. The D-5 imperative is satisfied at the SSOT layer; the runtime layer is one BG removed.
6. **No git commit performed**: per BG instructions, this is a $0 SSOT mutation with no commit; the working tree now diverges from HEAD on `.roadmap.clm`. A future commit BG must batch this with the companion landed handoff for atomic provenance. Until then, `git status` will show `.roadmap.clm` modified (this is expected, not an error).
7. **Pre-flight relied on `head -3 | tail -1` shorthand which happened to land on line 3 (the header)** — this worked because lines 1-2 are `#` comments and line 3 is the JSONL header, but if a future editor adds another comment line, the pre-flight one-liner would silently hit a comment line. The actual mutation used `sed -n '3p'` after explicitly verifying line 3 = header, so the mutation itself is line-number-robust to its own assumption. Future BGs touching this file should re-verify the header line number rather than assuming line 3.

## Verification commands (re-runnable)

```bash
cd /Users/ghost/core/anima

# 1. JSONL integrity
LINE_NUM=0
while IFS= read -r line; do
  LINE_NUM=$((LINE_NUM+1))
  [[ "$line" =~ ^# ]] && continue
  [[ -z "$line" ]] && continue
  echo "$line" | jq -e . > /dev/null || echo "FAIL line $LINE_NUM"
done < .roadmap.clm
# expect: no FAIL output

# 2. Annotation present
sed -n '3p' .roadmap.clm | \
  jq -e '.required_conditions[] | select(.id=="clm.cond.1") | .f1_v2_band_thresholds_2026_05_04.thresholds.red_max == 0.50'
# expect: true

# 3. cond.2 amendment preserved
sed -n '3p' .roadmap.clm | \
  jq -e '.required_conditions[] | select(.id=="clm.cond.2") | .amendment_2026_05_04.amendment_type == "naming_canonical_supersede"'
# expect: true

# 4. required_conditions length unchanged
sed -n '3p' .roadmap.clm | jq '.required_conditions | length'
# expect: 2
```

## Downstream

- **BG-VERIFIER-WIRE** (separate cycle): wire `tool/clm_consciousness_verify.hexa` to consult these thresholds at runtime; emit RED/YELLOW/GREEN exit codes per `hexa_hook.exit_codes`.
- **Drift detector** (future, not blocking): periodic `jq` cross-file equality check between `.roadmap.n_substrate.cond.1.cross_link.f1_v2_band_thresholds_2026_05_04` and `.roadmap.clm.cond.1.f1_v2_band_thresholds_2026_05_04` to catch silent desync.
- **Commit batch** (next cycle): commit `.roadmap.clm` + this landed handoff together for atomic provenance.
