---
date: 2026-05-04
agent: BG-NAMING-AMEND
status: landed
mutation: additive_only
exec_authorized: false
cost_usd: 0
substrate: mac-local
ssots_touched:
  - .roadmap.clm (cond.2 — additive amendment_2026_05_04 block)
ssots_NOT_touched:
  - docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md (no §3.1 EBNF change required — clm-v4 already in enum)
  - tool/hf_upload_mk2.hexa (no hardcoded anima- prefix; validator already conforms)
sibling_bg:
  - BG-HF-Release-Audit (gap #1 source)
  - BG-MODULES-CLM-MD (downstream README sync source author)
  - BG-MODEL-CARD (downstream README content draft)
  - BG-MANIFEST (downstream manifest.json author)
raw_compliance:
  - raw#9 (no .py touched)
  - raw#10 (3+ honest C3 caveats below)
  - raw#15 (additive only — original desc + hf_release_planned strings preserved verbatim)
---

# anima/HF naming — CLM cond.2 canonical-name amendment landed (2026-05-04)

## §1 What was renamed

- **Old canonical** (cond.2 desc + cross_link.hf_release_planned): `dancinlab/anima-clm-mk2-v1`
- **New canonical** (amendment_2026_05_04.new_canonical): `dancinlab/clm-v4-mk2-v1`
- **Mutation site**: `.roadmap.clm` line 3 header → `required_conditions[1]` (id=`clm.cond.2`) → new sibling field `amendment_2026_05_04`
- **Original strings**: NOT modified. Both the `desc` field literal and `cross_link.hf_release_planned` literal remain readable for full audit trail (additive_only_mutation=true, historical_evidence_preserved=true).

## §2 Why (EBNF compliance)

Per `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` §3.1, the `lm_family` enum admits only:
`blm | clm | tlm | vlm | slm | nlm | alm | mlm | llm | hexad | composite` (11 families).

The token `anima-` does NOT appear in this enum. `anima-clm-mk2-v1` parses ambiguously as either lm-family=`anima-clm` (banned per §6 anti-pattern "repeated lm-family / non-enum prefix") OR base-version=`mk2` (banned per §3.2 — `mk2` is not a valid `v\d+` form).

The new canonical `clm-v4-mk2-v1` parses cleanly as: `lm_family=clm` + `base_version=v4` + variant slot `mk2-v1` (legacy `\d+-\d+` form per §3.7, grace-period acceptable). Cleaner alternative future re-base would be `clm-v4` (size suffix omitted per §3.5 "obvious from base-version") — the amendment preserves `mk2-v1` as variant for traceability with the original cond.2 intent.

## §3 Downstream artifacts requiring update

Listed in amendment block field `downstream_artifact_updates_required`:

1. `docs/modules/clm.md` — README sync source (currently nonexistent per audit doc §1.2; sibling BG-MODULES-CLM-MD authors from scratch)
2. README draft (sibling BG-MODEL-CARD) — must use new canonical name in title + Origin section
3. `manifest.json` (sibling BG-MANIFEST) — record new repo name + sha256s under new key
4. `tool/hf_upload_mk2.hexa` (next BG cycle config) — when push runs, `--repo` flag must use `clm-v4-mk2-v1`, not `anima-clm-mk2-v1`

Additionally (not listed in amendment but discovered by grep): 4 landed docs cite the old name (`docs/clm_v4_release_path_decision_2026_05_04.md`, `docs/clm_v4_release_path_landed_2026_05_04.ai.md`, `docs/anima_clm_hf_release_v1_plan_2026_05_04.md`, `docs/anima_clm_hf_release_v1_landed_2026_05_04.ai.md`). These are landed `ai.md` and discussion-doc artifacts; per anima additive discipline they are NOT mutated retroactively. Future ai-md cycles should cite this amendment doc to resolve naming references forward.

## §4 Historical evidence preserved

The amendment is purely additive. Verification commands:

```bash
# Original desc string — unchanged:
head -3 .roadmap.clm | tail -1 | \
  jq -r '.required_conditions[] | select(.id=="clm.cond.2") | .desc'
# → "HF release v1 — public weight + model card published as dancinlab/anima-clm-mk2-v1 ..."

# Original cross_link.hf_release_planned — unchanged:
head -3 .roadmap.clm | tail -1 | jq -r '.cross_link.hf_release_planned'
# → "dancinlab/anima-clm-mk2-v1"

# New canonical via amendment block:
head -3 .roadmap.clm | tail -1 | \
  jq -r '.required_conditions[] | select(.id=="clm.cond.2") | .amendment_2026_05_04.new_canonical'
# → "dancinlab/clm-v4-mk2-v1"
```

Future readers can reconstruct the full naming-decision history by inspecting both the superseded literals and the amendment block in a single jq expression.

## §5 raw#10 honest C3 caveats

- **C1** — *Amendment is additive, original `hf_release_planned` field is still readable for audit trail.* This is intentional (additive discipline) but means downstream tooling that naively reads `cross_link.hf_release_planned` will still get the old (non-conformant) name. Tooling MUST be amendment-aware: prefer `required_conditions[id=clm.cond.2].amendment_2026_05_04.new_canonical` when present, fallback to `cross_link.hf_release_planned` otherwise. The `tool/hf_upload_mk2.hexa --repo <flag>` consumer will need a config update in the BG-CONFIG cycle (NOT this cycle).
- **C2** — *The new canonical `clm-v4-mk2-v1` uses the legacy `\d+-\d+` variant form (§3.7), which is grace-period-deprecated until 2026-06-02 per spec §8.1.* Strict §10.4 PASS criteria require either CANON regex OR EXT regex with README banner. The new name is EXT-conformant via the legacy variant fallback. A cleaner future migration would drop `-mk2-v1` entirely (to `clm-v4` or `clm-v4-base-mirror-promoted`) but that loses the cond.2 textual intent of "mk2 era v1 release". Honest acknowledgment: amendment trades naming-purity for cross_link-textual-fidelity.
- **C3** — *No spec §3.1 EBNF amendment was needed, but the `anima-clm-mk2-v1` literal still appears in 4+ landed `ai.md` docs (per §3 above) that are NOT updated by this BG.* Anima additive discipline forbids retroactive ai-md mutation, so the docs/ corpus retains a "naming drift footprint" until the next cycle that intentionally amends those specific docs (likely the model-card cycle). Search `grep -rn "anima-clm-mk2-v1" docs/` will continue to surface the old name; readers must consult this amendment doc to resolve.
- **C4** — *Validator hexa (`tool/hf_upload_mk2.hexa`) was inspected and contains no hardcoded `anima-clm` references; the family enum already admits `clm`, and `clm-v4-mk2-v1` parses via the EXT regex with legacy variant.* Therefore no hexa amendment is needed in this cycle. However, this conclusion assumes the validator's variant-slot regex matches `\d+-\d+` form anywhere after the version slot — verified by reading §10.2 spec; not directly smoke-tested in this BG (out of scope per "no exec" constraint). Smoke-test under sibling BG-CONFIG when first push is staged.

## §6 Composability

- **upstream**: `docs/anima_clm_hf_release_v1_audit_2026_05_04.md` §1 (Q1 = Option A user authorization)
- **siblings (concurrent BG cycle)**: BG-MODULES-CLM-MD, BG-MODEL-CARD, BG-MANIFEST (each consumes the new canonical)
- **downstream (future BG)**: BG-CONFIG (updates `tool/hf_upload_mk2.hexa --repo` invocation defaults), BG-PUSH-V1 (executes the actual HF push under new name)

---

End of amendment landed doc. No `.py` written. No git commit. No exec. Mac-local $0.
