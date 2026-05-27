---
id: H_013
slug: longitudinal-eeg-5axis
title: longitudinal EEG 5-axis (caffeine + circadian + postmeal + postexercise + sleep) — N=170 within-subject
domain: physics
status: pre-register-frozen
exploration_method: E5 (variable-ablation) + E7 (user subject)
verification_method: W1 (raw#12 frozen) + W2 (5+ falsifier) + W3 (deterministic) + W6 (ledger jsonl)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-04-28
since: 2026-04-28
---

# H_013 — longitudinal EEG 5-axis within-subject

## Hypothesis

within-subject N=1 longitudinal EEG study (subject search5599@proton.me, 170 sessions over ~14d) 5-axis × 17-level design — caffeine effect + circadian peak + postmeal dip + postexercise recovery + sleep inertia.

## Migration Status

- **frozen prereg**: `state/longitudinal_pre_register.json` (raw_rank:12, frozen_at:2026-04-28)
- 본 H는 raw#12 strict execution lane — JSON spec frozen

## Brief Summary

- **H1 caffeine**: engagement (beta/alpha) at +30/+60min > pre-09:00 baseline (paired t, alpha=0.0025 Bonferroni)
- **H2 circadian**: LZ76 at 15:00 ≥ 09:00 (Marzano 2010 afternoon peak)
- **H3 postmeal**: engagement at +0min < +2h (postprandial dip)
- **H4 postexercise**: gamma/theta at +0min > +30min recovery
- **H5 sleep**: drowsy_idx wake-immediate > +60min (sleep inertia)

- **Variables**: 5 axis × 17 level × N=10 = 170 sessions
- **Falsifiers**: F1 (synthetic stream uniform LZ76) + F2 (between/within variance) + F3 (ledger row missing field) + F4 (session_id collision) + F5 (post-hoc edit raw#12 violation)
- **Verdict rule**: TRANSITION_READY = (N≥170) AND (per_axis_min_N≥10) AND (gap_count≤10%)

## Cross-Links

- prereg JSON: `state/longitudinal_pre_register.json`
- sister: clm_eeg p1/p2/p3 prereg (`state/clm_eeg_p*_pre_register.json`)
- roadmap: `.roadmap.eeg` longitudinal entry
- own:
- literature: Marzano (2010), Schartner (2017) LZ76 criteria

## Honest Limits

- L1: N=1 within-subject — generalization X (사용자 본인 한정)
- L2: prereg JSON frozen 2026-04-28 — post-hoc edit 시 raw#12 violation
- L3: 170 session goal vs 현재 progress 별도 cycle audit
- L4: anima-clm-eeg domain primary — 본 H는 cross-link entry
- L5: raw#82 retraction protocol 정합 (criteria_provenance 명시)
