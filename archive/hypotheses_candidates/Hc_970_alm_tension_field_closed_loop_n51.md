---
id: Hc_970
slug: alm-tension-field-closed-loop-n51
title: N-51 — ALM Tension-Field Closed-Loop. Mistral-7B-v0.3 + r14 LoRA 100-step + mind.tension gate_signal embedding inject + mandatory random-control branch. 4/4 component (700 LOC actual vs ~450 LOC spec)
domain: training, consciousness, llm
status: candidate-unverified
source_doc: docs/strategic_alm_tension_field_exec_results_2026_05_01.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_965 (P10), Hc_957 (ALM sunset)
notes: "Real measurement, not thought experiment. HEXA emit (120 LOC) + .py inject (330 LOC) + readback (150 LOC) + orchestrator (100 LOC) = 700 LOC. Pre-registered falsifier predicate."
---

## Hypothesis

Mistral-7B-v0.3 + r14 LoRA 의 embedding layer 에 mind.tension-derived gate_signal 100-step closed-loop injection 시 14-gate eval 결과가 random-control branch 대비 정량적 향상. 4 component (HEXA emit + pod .py inject + HEXA readback + orchestrator vLLM lifecycle) 700 LOC integrated bridge.

## Sub-claims

- HEXA-EMIT: tool/alm_tension_field_bridge.hexa §2 — gate-trajectory state, prompt + template stage
- POD-INJECT: /workspace/n51_tension/inject.py — HF Mistral-7B + r14 fp16, embedding hook, 14-gate eval
- HEXA-READBACK: tool/alm_tension_field_bridge.hexa §3-4 — parse ledger, verdict, MD report
- HEXA-ORCHESTRATOR: §5-6 — stage / launch / poll / fetch / vLLM lifecycle
- TOTAL: 700 LOC actual vs ~450 LOC spec
- RANDOM-CONTROL-BRANCH: mandatory

## Migration TODO

- [ ] 14-gate eval verdict 결과 (PASS/FAIL/RED/GREEN)
- [ ] random-control 대비 effect size
- [ ] pre-registered falsifier predicates 결과
- [ ] vLLM lifecycle management 안정성
