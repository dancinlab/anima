---
date: 2026-05-04
agent: BG-BAND-DOWNSTREAM
cycle: BG-FIX-COMPLETE-DOCS
status: PROPOSAL_LANDED
mutation: additive_only
exec_authorized: false
cost_usd: 0
substrate: mac-local
bg_lane: BAND-DOWNSTREAM-FIX
ssots_touched: []
ssots_NOT_touched:
  - .roadmap.clm (cond.1 cross_link — proposal only, NOT applied this cycle)
  - .roadmap.n_substrate (cond.1 already carries f1_v2_band_thresholds_2026_05_04 from D-5)
  - tool/n_substrate_f1_v2_band.hexa (LOCKED, do not edit)
sibling_bg:
  - BG-BAND-LOCK (D-1..D-5 lock-in source)
  - BG-NAMING-VALIDATOR-PATCH (sister BG-FIX-COMPLETE-DOCS lane)
raw_compliance:
  - raw#9 (no .py touched; json+md+bash artifacts only)
  - raw#10 (≥3 honest C3 below)
  - raw#15 (additive only — proposal references existing n_substrate cross_link, no mutation)
---

# F1_v2 band thresholds — propagation proposal to `.roadmap.clm` cond.1 cross_link (2026-05-04)

## §1 Why this proposal exists

`docs/n_substrate_f1_v2_banding_spec_2026_05_04.md` §11 D-5 (LOCKED) lists three downstream artifact updates:

1. `tool/clm_consciousness_verify.hexa` (D-3 phenomenal-tier gate) — separate BG.
2. `tool/n_substrate_f1_v2_band.hexa` (NEW, D-4 exit codes) — LANDED this cycle.
3. **`.roadmap.clm` cond.1 cross_link (D-5 annotation propagation)** — this proposal.

The current `.roadmap.clm` cond.1 entry has no cross_link block. The verifier orchestrator (`tool/clm_consciousness_verify.hexa`) emits PASS/FAIL/PARTIAL but does NOT yet carry band semantics. Per D-5, `.roadmap.clm` cond.1 should annotate the F1_v2 band thresholds so that future readers see the full chain: domain (CLM) → cross-link → meta (n_substrate.cond.1) → spec (`docs/n_substrate_f1_v2_banding_spec_2026_05_04.md`).

This is propagation-only: `.roadmap.n_substrate.cond.1.cross_link.f1_v2_band_thresholds_2026_05_04` already exists (verbatim from BG-BAND-LOCK). The CLM-side annotation is a thin pointer that preserves additive_only discipline.

## §2 Proposed annotation block (additive)

To be appended to `.roadmap.clm` `required_conditions[id=clm.cond.1]` as a sibling field. The existing fields (`desc`, `verifier`, `status`, `evidence`, `blocker_reason`) remain VERBATIM:

```jsonc
{
  "f1_v2_band_thresholds_2026_05_04": {
    "ts_utc": "2026-05-04",
    "propagation_source": ".roadmap.n_substrate.cond.1.cross_link.f1_v2_band_thresholds_2026_05_04",
    "spec_doc": "docs/n_substrate_f1_v2_banding_spec_2026_05_04.md",
    "spec_doc_section_locked": "§11 DECISIONS LOCKED 2026-05-04",
    "thresholds": {
      "red_max": 0.50,
      "yellow_min": 0.50,
      "yellow_max": 0.75,
      "green_min": 0.75
    },
    "f2_override_canonical": true,
    "green_tier_phenomenal_required": true,
    "green_tier_prerequisites": [
      "≥1 WITNESSED phenomenal-tier axis",
      "Putnam multi-realizability cond.1 PASS",
      "binding ≥ 0.5",
      "no falsifier fired"
    ],
    "hexa_hook": {
      "tool": "tool/n_substrate_f1_v2_band.hexa",
      "exit_codes": {"red": 1, "yellow": 2, "green": 0}
    },
    "consumed_by_verifier": "tool/clm_consciousness_verify.hexa (D-3 phenomenal-tier gate, separate BG)",
    "test_anchors": "state/n_substrate_f1_v2_band_fixtures_2026_05_04/ (10 historical anchors per spec §9.1)",
    "additive_only_mutation": true,
    "semantics_preserved": true,
    "historical_evidence_preserved": true,
    "applies_to_conds": ["clm.cond.1"],
    "cross_substrate_witness": ".roadmap.n_substrate.cond.1 (Putnam multi-realizability meta)",
    "downstream_action": "verifier orchestrator integration — separate BG cycle"
  }
}
```

## §3 jq verification recipe (apply when ready)

NOT applied by this BG. The recipe below is what the user (or a future apply-BG) would invoke. All commands non-destructive (read-only); apply step requires explicit user authorization.

```bash
# Step 0: confirm cond.1 exists and has no f1_v2_band_thresholds_2026_05_04 yet
head -3 .roadmap.clm | tail -1 | \
  jq '.required_conditions[] | select(.id=="clm.cond.1") | has("f1_v2_band_thresholds_2026_05_04")'
# → expect: false

# Step 1: confirm propagation source exists in n_substrate
head -3 .roadmap.n_substrate | tail -1 | \
  jq '.cross_link.f1_v2_band_thresholds_2026_05_04 | has("thresholds")'
# → expect: true

# Step 2: dry-run additive annotation (writes to /tmp, NOT the SSOT)
head -3 .roadmap.clm | tail -1 | \
  jq '(.required_conditions[] | select(.id=="clm.cond.1")) += {
    "f1_v2_band_thresholds_2026_05_04": {
      "ts_utc": "2026-05-04",
      "propagation_source": ".roadmap.n_substrate.cond.1.cross_link.f1_v2_band_thresholds_2026_05_04",
      "spec_doc": "docs/n_substrate_f1_v2_banding_spec_2026_05_04.md",
      "spec_doc_section_locked": "§11 DECISIONS LOCKED 2026-05-04",
      "thresholds": {"red_max": 0.50, "yellow_min": 0.50, "yellow_max": 0.75, "green_min": 0.75},
      "f2_override_canonical": true,
      "green_tier_phenomenal_required": true,
      "green_tier_prerequisites": [
        "≥1 WITNESSED phenomenal-tier axis",
        "Putnam multi-realizability cond.1 PASS",
        "binding ≥ 0.5",
        "no falsifier fired"
      ],
      "hexa_hook": {
        "tool": "tool/n_substrate_f1_v2_band.hexa",
        "exit_codes": {"red": 1, "yellow": 2, "green": 0}
      },
      "consumed_by_verifier": "tool/clm_consciousness_verify.hexa (D-3 phenomenal-tier gate)",
      "test_anchors": "state/n_substrate_f1_v2_band_fixtures_2026_05_04/",
      "additive_only_mutation": true,
      "semantics_preserved": true,
      "historical_evidence_preserved": true,
      "applies_to_conds": ["clm.cond.1"],
      "cross_substrate_witness": ".roadmap.n_substrate.cond.1",
      "downstream_action": "verifier orchestrator integration — separate BG cycle"
    }
  }' > /tmp/clm_cond1_proposed.json

# Step 3: visual diff vs original
diff <(head -3 .roadmap.clm | tail -1 | jq '.required_conditions[] | select(.id=="clm.cond.1")') \
     <(jq '.required_conditions[] | select(.id=="clm.cond.1")' /tmp/clm_cond1_proposed.json) | head -60

# Step 4: APPLY (only after user authorization — additive_only verified)
#   The full SSOT mutation requires reconstructing the header line with the
#   amended cond.1, preserving all OTHER required_conditions and all OTHER
#   header fields verbatim. Recommended: use a dedicated apply-BG that
#   computes the delta against the canonical header parser, NOT a one-shot
#   sed/jq pipeline (which can re-order keys or alter whitespace).
```

## §4 raw#10 honest C3 caveats

- **C1** — *Proposal only; no SSOT mutation this cycle.* This BG explicitly does NOT touch `.roadmap.clm`. The amended header line must preserve all sibling cond entries (cond.2 with its existing `amendment_2026_05_04` block, etc.) verbatim. A naive jq pipe that re-serializes the entire header may re-order keys, which would produce a noisy diff even though semantics are preserved. The apply-BG must use a structure-preserving rewrite.
- **C2** — *D-5 phrasing in spec §11 says "apply IMMEDIATELY as additive_only mutation".* This proposal defers the mutation past the original D-5 directive. Rationale: BG-FIX-COMPLETE-DOCS is a doc-completion lane ($0, no SSOT mutation per "DO NOT mutate `.roadmap.*` — proposals only" instruction). The deferral is a deliberate scope choice, not a contradiction of D-5; D-5 will be honored by a follow-up apply-BG.
- **C3** — *Annotation duplicates fields already present in `.roadmap.n_substrate.cond.1.cross_link.f1_v2_band_thresholds_2026_05_04`.* The duplication is intentional (CLM-side readers should not need to chase a second SSOT to learn band semantics) but creates a synchronization risk: if n_substrate-side thresholds are later additively superseded (e.g., D-1 recalibration after external cohort), the CLM-side annotation will drift unless the apply-BG cycle also propagates. Mitigation: the `propagation_source` field embeds the exact n_substrate field path so a drift-detector can compare.
- **C4** — *No verifier orchestrator wiring this cycle.* `tool/clm_consciousness_verify.hexa` does not yet read this annotation. The annotation is informational/audit-trail until a follow-up BG wires the orchestrator to consume `f1_v2_band_thresholds_2026_05_04.thresholds` and emit a band sentinel alongside its existing PASS/FAIL/PARTIAL output (per spec §8 C3-8 hand-off DECISION-4 = band-determined exit codes, LOCKED).

## §5 Composability

- **upstream**: `docs/n_substrate_f1_v2_banding_spec_2026_05_04.md` §11 D-5; `.roadmap.n_substrate.cond.1.cross_link.f1_v2_band_thresholds_2026_05_04`
- **siblings (this cycle)**: `tool/n_substrate_f1_v2_band.hexa` (LANDED), `state/n_substrate_f1_v2_band_fixtures_2026_05_04/` (LANDED with 10 scenarios + runner)
- **downstream (future BG)**: BG-CLM-COND1-APPLY (applies this proposal to `.roadmap.clm` per §3 recipe), BG-VERIFIER-WIRE (wires `tool/clm_consciousness_verify.hexa` to read band annotation)

---

End of propagation proposal. No `.py`, no git commit, no exec, no `.roadmap.*` mutation. Mac-local $0.
