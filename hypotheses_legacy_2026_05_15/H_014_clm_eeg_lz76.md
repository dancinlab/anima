---
id: H_014
slug: clm-eeg-lz76-paradigm
title: CLM-EEG LZ76 complexity — consciousness substrate proxy
domain: substrate
status: pre-register-frozen
exploration_method: E3 (theory Schartner) + E5 (variable-ablation)
verification_method: W1 + W2 + W3 + W6
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-04-26 (estimate, see prereg)
since: 2026-04-26
---

# H_014 — CLM-EEG LZ76 paradigm

## Hypothesis

LZ76 (Lempel-Ziv 1976) complexity가 EEG consciousness substrate proxy — Schartner 2017 정합. 의식 상태 (awake / drowsy / sleep)에서 LZ76 distinguishable.

## Migration Status

- **frozen prereg**: `state/clm_eeg_p1_lz_pre_register.json` + `state/clm_eeg_p1_lz_pre_register_real.json`
- raw_rank:12 frozen execution

## Brief Summary

- **Predictions**: LZ76 (awake) > LZ76 (drowsy) > LZ76 (sleep); threshold human_baseline_lz76_x1000 (operational placeholder, longitudinal H_013에서 empirical mean-2SD로 retract per raw#82)
- **Status**: 본 H는 anima-clm-eeg P1 phase frozen prereg
- **Cross-link**: H_013 longitudinal (5-axis subject) 정합

## Cross-Links

- prereg: `state/clm_eeg_p1_lz_pre_register.json`
- sister: H_013 (longitudinal), H_015 (gamma/theta P3)
- roadmap: `.roadmap.eeg` + `.roadmap.anima_clm_eeg`
- own: own 21
- literature: Schartner et al. (2017) Complexity of multi-dimensional spontaneous EEG

## Honest Limits

- L1: LZ76 single-metric — Φ proxy 약 (Φ = integrated info ≠ LZ76 = compression)
- L2: human_baseline placeholder retracted per raw#82 (longitudinal mean-2SD replacement)
- L3: 본 H는 cross-link entry — anima-clm-eeg domain primary
- L4-L5: prereg JSON frozen, 본 entry는 markdown counterpart
