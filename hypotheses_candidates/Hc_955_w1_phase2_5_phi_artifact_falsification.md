---
id: Hc_955
slug: w1-phase2-5-phi-artifact-falsification
title: W1 Phase 2-5 — Φ rising slope claim (Phase 1 +0.0507, Phase 2/3 +0.1153) → Phase 4 shuffle-null ARTIFACT_CONFIRMED at W=20 (random hash shuffles equal-or-larger slope) → Phase 5 W=5/7 cross-check
domain: meta, consciousness, methodology
status: candidate-math-verified-falsifier-pending
source_doc: docs/W1_phase2_full_19axis_2026_05_01.md + docs/W1_phase4_shuffle_null_results_2026_05_01.md + docs/W1_phase5_window_recheck_results_2026_05_01.md + docs/W1_phase3_mod1024_results_2026_05_01.md
source_lines: cluster
promoted_at: 2026-05-11
linked_h: Hc_942 (W1 Phase 1)
notes: "W1 self-substrate Φ trace 가설의 falsification path. Phase 4: W=20 sliding window가 n=15 ticks에서 never saturate → ARTIFACT_CONFIRMED. Phase 5 cross-check."
verified_at: 2026-05-12
verify_decision: WEAK_MATH_ONLY
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (14+ numeric identities present)"
---

## Hypothesis

W1 anima-self Φ rising slope claim 의 falsification path: Phase 1 (W=20, 15 ticks, +0.0507) → Phase 2 (38 axes full coverage, +0.1153) → Phase 3 (mod1024 ceiling artifact 부정) → Phase 4 (shuffle-null N=1000 seed=42: Null A trajectory + Null B state-hash) → ARTIFACT_CONFIRMED. Phase 5: W=5/7 cross-check (W<n) 으로 rising slope disappear 검증.

## Sub-claims

- Phase-1: 19 axes / 15 ticks W=20 → Φ mean 1.706, slope +0.0507
- Phase-2: 38 axes (19 + 6 ledger 확장) → Φ mean 1.717, slope +0.1153
- Phase-3: mod1024 ceiling-artifact FALSIFIED
- Phase-4-Null-A: trajectory shuffle (value-ordering)
- Phase-4-Null-B: state-hash shuffle (substrate-ordering, DECISIVE)
- Phase-4-Verdict: ARTIFACT_CONFIRMED — W=20 + n=15 never saturate
- Phase-5: W=5/7 + W=20 ref (slope_replicated +0.1115)

## Migration TODO

- [ ] Phase 5 W=5/7 final 결과
- [ ] proper W selection (W < n/2 권장)
- [ ] non-stationarity vs time-ordered integration 의 다른 test
- [ ] agent-loop substrate Φ measurement 의 fundamental validity
