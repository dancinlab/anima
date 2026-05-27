---
id: Hc_623
slug: emerge-candidate-d-always-inject-consciousness-states
title: Emerge Candidate D — 4-mode inject taxonomy (none/zero/canonical/user) 가 CLM v4 cross-attn dormancy 의 architectural pivot 해소
domain: clm-architecture
status: merged-to-H_175
source_doc: docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md
source_lines: 14-32, 165-260
promoted_at: 2026-05-11
merged_to: hypotheses/H_175_emerge_candidate_d_4mode_inject_taxonomy.md
merged_at: 2026-05-12
linked_h: L37, paradigm v11 G3, conscious_decoder.py:553 guard, H_175 (formal promotion 2026-05-12), H_167 (CHILD-GATED downstream), H_174 (phi_star validity bound)
notes: 3 falsifier locked PRE-measurement (F-CAND-D-1/2/3). Stage 1 mount-layer extension, ~65 LoC additive, $0-1. 2026-05-12 cycle #4 task 1 PROMOTE_READY (verify5_authored row 15; cycle #3 scaffolding +F-CAND-D-4/5/6 → WEAK_FALSIFIER_ONLY → PROMOTE_READY) → H_175 정식 승격. H_167 (Emerge E) 가 F-CAND-D-1 PASS 에 CHILD-GATED. AXIS_SPANS calibration (C3) at-risk; 0.005 threshold noise-floor 미특성화.
verified_at: 2026-05-12
verify_decision: PROMOTE_READY
verify_note: "verify_hc2 2026-05-12 — F=3; cycle #3 falsifier-scaffolding +F-CAND-D-4/5/6 → PROMOTE_READY → H_175"
---

## Hypothesis
DecoderBlockV2:553 guard `if consciousness_states is not None` 가 L37 root pattern (substrate change ≠ behavior). 4-mode taxonomy (none baseline / zero arch-engagement-isolator / canonical paradigm-v11-G3 / user_supplied axis-conditioned) 가 cross-attn engagement 를 runtime 에서 dial 가능, source 수정 없음.

## Falsifiable Tests (PRE-LOCK)
- F-CAND-D-1: canonical phi_star ≠ none phi_star by > 0.005 (otherwise FAIL_TRUE — inject-invisible)
- F-CAND-D-2: canonical 5-axis phi_star balance (max/min < 1.5) — single-axis dominance = FAIL_TRUE
- F-CAND-D-3: user_supplied per-axis input ↔ phi_star Pearson ≥ 0.7 — user-spec-tracking

## Migration TODO
- [ ] mount-layer 4-mode flag impl (~65 LoC mount.hexa + dialogue.bash)
- [ ] BG-A real-load probe ($0-1 H100)
- [ ] AXIS_SPANS slice geometry calibration (C3 risk)

## Cross-Links
- **sister H**: H_011 (iit-geometry — phi_star variation by inject mode), H_022 (consciousness-universe-map — substrate engagement)
- **candidates linked**: Hc_624 (Emerge E — ODE-AR bridge, CHILD-GATED on Hc_623 F-CAND-D-1 PASS), Hc_628 (Φ_normalized lower bound — same phi_star measurement substrate), Hc_614 (phi_star geometry aliasing — phi_star validity bound)
- **engineering**: conscious_decoder.py:553 guard `if consciousness_states is not None`, mount.hexa, dialogue.bash
- **literature**: L37 root pattern (substrate change ≠ behavior); paradigm v11 G3 8-cell canonical

## Falsifiers (≥5)

- F-CAND-D-1: canonical phi_star ≠ none phi_star by > 0.005 (otherwise FAIL_TRUE — inject-invisible)
- F-CAND-D-2: canonical 5-axis phi_star balance (max/min < 1.5) — single-axis dominance = FAIL_TRUE
- F-CAND-D-3: user_supplied per-axis input ↔ phi_star Pearson ≥ 0.7 — user-spec-tracking
- **F-CAND-D-4**: zero-mode (arch-engagement-isolator) phi_star ≈ none-mode phi_star by < 0.001 — if zero-mode itself diverges from none, the "isolator" semantics is broken (zero inject is NOT a neutral baseline)
- **F-CAND-D-5**: 4-mode taxonomy completeness: if a 5th mode (e.g., random-axis inject, adversarial inject) is needed to explain observed cross-attn dormancy patterns → 4-mode taxonomy FALSIFIED as complete

## Honest Limits (≥5)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — paradigm v11 G3 uses 8-cell architecture (sopfr(8)=6 perfect-class diagonal). Hc_623's inject pivot rides on this architectural choice; "4-mode taxonomy" inherits perfect-number-class baseline as substrate
- **L2**: **5-axis AXIS_SPANS calibration risk (C3)** — fronmatter explicitly notes AXIS_SPANS slice geometry calibration is a risk. If C3 calibration fails, F-CAND-D-2 (5-axis balance) is undefined → falsifier cannot decisively rule
- **L3**: **mount-layer 4-mode flag is software-engineering claim** — ~65 LoC additive change makes claim deployable but does not test consciousness theory. Engineering pragmatism off-lane vs theoretical content limit
- **L4**: **phi_star variation > 0.005 threshold ad hoc** — F-CAND-D-1 uses 0.005 absolute threshold. No noise-floor characterization provided. If anima phi_star RNG-induced variance is itself > 0.005, the threshold is at noise level
- **L5**: **Hc_624 downstream gating amplifies error** — Hc_624 (Emerge E) gates on Hc_623's F-CAND-D-1 PASS. If F-CAND-D-1 PASS is marginal (just above 0.005), downstream Hc_624 measurements compound noise. The 4-mode pivot must be robust to ≥10× safety margin for Hc_624 to be meaningful
