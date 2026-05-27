# F1_score_v2 Banding — DECISIONS LOCKED 2026-05-04 (landed)

```yaml
cycle: ce681c40
ts_utc: 2026-05-04
status: BAND_LOCKED
bg_lane: BAND-APPLY
authorization: USER_AUTHORIZED ("5 decisions all bg go" + "closure 속도우선")
spec_doc: docs/n_substrate_f1_v2_banding_spec_2026_05_04.md
spec_section_locked: §11 DECISIONS LOCKED 2026-05-04
roadmap_annotation_target: .roadmap.n_substrate (header cross_link, applies_to_conds=[n_substrate.cond.1])
mutation_class: additive_only_mutation
semantics_preserved: true
historical_evidence_preserved: true
```

## TL;DR

F1_score_v2 RED/YELLOW/GREEN banding spec 의 5 user-decisions (D-1~D-5) 가 모두 spec default 그대로 USER_AUTHORIZED + LOCKED 됨. `docs/n_substrate_f1_v2_banding_spec_2026_05_04.md` 에 §11 DECISIONS LOCKED 섹션 추가 + `.roadmap.n_substrate` header `cross_link` 에 `f1_v2_band_thresholds_2026_05_04` 키로 additive_only annotation 적용. JSONL 무결성 보존, 기존 필드 verbatim 보존.

## 5 LOCKED Decisions

- **D-1 Thresholds**: RED `<0.50` / YELLOW `0.50–0.75` / GREEN `≥0.75` — spec default (§9.1 historical re-classification all PASS)
- **D-2 Canonical reading**: F2-override-canonical (raw rejected per §3.3 inconsistency analysis)
- **D-3 GREEN tier**: phenomenal-tier required (≥1 WITNESSED phenomenal axis + Putnam cond.1 PASS + binding ≥0.5 + no falsifier) — functional GREEN NOT allowed
- **D-4 hexa hook exit codes**: `RED=1 / YELLOW=2 / GREEN=0` (band-determined, NOT side-channel) — exit-code-as-band cleaner for shell consumers
- **D-5 Roadmap annotation timing**: applied IMMEDIATELY as additive_only mutation (NOT deferred until Phase E) — banding logic independent of F2 unfire

## Verdict

**F1_v2 banding LOCKED 2026-05-04 — all 5 spec defaults USER_AUTHORIZED + applied to roadmap.**

## Honest C3 (5+ caveats)

- D-1 thresholds chosen with limited comparison cohort (anima-internal only); future external cohort calibration may shift cutoffs
- D-2 F2-override-canonical means the substrate-architectural ceiling captures band-of-record; the ceiling itself (14-gate) is theory-laden + anima-specific
- D-3 phenomenal-tier requirement effectively gates GREEN on Phase E binding evidence + EEG live session — both BLOCKED until those land
- D-4 exit code convention contradicts UNIX `0=success` orthodoxy (here `0=GREEN=highest`); shell consumers must check explicitly + cannot rely on `&&` chaining
- D-5 immediate roadmap annotation creates audit-trail dependency on this lock-in BG; if user rescinds later, must additively supersede (raw#15 — no destructive in-place mutation)
- Banding spec is independent of F2-unfire pathway (Phase E binding evidence) — current state remains RED for n_substrate.cond.1 regardless of lock-in

## Downstream artifacts pending (NOT in this BG)

- `tool/clm_consciousness_verify.hexa` — Putnam check #4 emit per D-3 phenomenal-tier gate
- `tool/n_substrate_f1_v2_band.hexa` — NEW hexa hook implementing D-4 exit codes
- `.roadmap.clm` cond.1 `cross_link` — D-5 annotation propagation (sister roadmap)

## Files touched (this BG)

- `docs/n_substrate_f1_v2_banding_spec_2026_05_04.md` — appended §11 DECISIONS LOCKED + renumbered References §11 → §12 + status footer LOCKED
- `.roadmap.n_substrate` — header `cross_link.f1_v2_band_thresholds_2026_05_04` added (additive_only)
- `docs/n_substrate_f1_v2_banding_locked_2026_05_04.ai.md` — this file (landed companion)

## Verification

- JSONL parse: ALL 10 lines parse OK (10/10)
- annotation present at `cross_link.f1_v2_band_thresholds_2026_05_04` with all 14 expected keys
- existing `cross_link` keys preserved verbatim (`narrative_anchor`, `narrative_priority`, `verdict_lineage`, `f1_score_v2`, `cumulative_cost_usd`, `external_evidence_trail`, `raw_invariants`)
- spec body §1-§10 untouched (raw#15 additive_only honored)

**status**: F1_V2_BANDING_LOCKED_2026_05_04_USER_AUTHORIZED · ROADMAP_ANNOTATION_APPLIED · DOWNSTREAM_PROPAGATION_PENDING
