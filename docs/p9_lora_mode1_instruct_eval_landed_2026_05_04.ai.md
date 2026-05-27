# P9 BG-Psi: Mode 1 LoRA Re-eval with Llama-3.2-3B-Instruct Anchor — LANDED 2026-05-04

**Cycle**: `p9_lora_mode1_instruct_eval_2026_05_04`
**Verdict**: `FORGETTING_INDEPENDENT` (F1_v3 V2 = SUCCESS_WITH_CAVEAT)
**Wall**: 31 min  **Cost**: $1.54  **Pod kill verified**: true (404)

## Why this BG existed

Per BG-Rho honest C3 #2 (commit `fa7db7bc`):
> Adapter base mismatch: HF adapter_config.json declares base = meta-llama/Llama-3.2-3B-Instruct,
> but we composed onto meta-llama/Llama-3.2-3B (non-Instruct, BG-Omicron anchor). LoRA weights were
> trained against Instruct's chat-templated representations; applying them to base may amplify the
> apparent degradation due to template-mismatch artifacts.

BG-Psi tests this hypothesis by re-evaluating Mode 1 with **Llama-3.2-3B-Instruct as base + LoRA**, plus re-measuring Llama-3.2-3B-Instruct baseline anchors on the same 3 benchmarks (HellaSwag 0-shot acc_norm, MMLU 5-shot, TriviaQA 0-shot EM, limit=500, seed=42, bf16).

If degradation magnitude shrinks substantially (>=50% on >=2/3 benches), template-mismatch is confirmed; if it persists, catastrophic forgetting is confirmed independent of base choice.

## Raw numbers

### Instruct base anchors (this BG)

| bench       | metric            | base (Instruct) | LoRA (Instruct+adapter) | Delta_pp | 2sigma_thr_pp | c3   | c4   |
|-------------|-------------------|-----------------|-------------------------|----------|---------------|------|------|
| HellaSwag   | acc_norm          | 0.632           | 0.636                   | +0.4     | 4.31          | FAIL | PASS |
| MMLU        | acc (5-shot)      | 0.6179          | 0.5860                  | -3.19    | 0.86          | PASS | PASS |
| TriviaQA    | EM (rm_ws)        | 0.480           | 0.398                   | -8.2     | 4.47          | PASS | PASS |

### Cross-anchor comparison

| bench     | Delta_BG-Rho (non-Instruct) | Delta_BG-Psi (Instruct) | Delta_diff | shrink_ratio | classification |
|-----------|-----------------------------|-------------------------|------------|--------------|----------------|
| HellaSwag | -1.2 pp                     | +0.4 pp                 | +1.6 pp    | 0.667        | SHRUNK         |
| MMLU      | -4.95 pp                    | -3.19 pp                | +1.76 pp   | 0.356        | PERSISTED      |
| TriviaQA  | -9.4 pp                     | -8.2 pp                 | +1.2 pp    | 0.128        | PERSISTED      |

**Decision rule**: >=2/3 SHRUNK -> TEMPLATE_MISMATCH_CONFIRMED; >=2/3 PERSISTED -> FORGETTING_INDEPENDENT; any INCREASED -> UNEXPECTED.

**Result**: 2/3 PERSISTED, 1/3 SHRUNK -> **FORGETTING_INDEPENDENT**.

### Instruct vs non-Instruct base ceiling

Switching from non-Instruct (BG-Omicron 93bef8c8) to Instruct base on the eval anchor:

- HellaSwag acc_norm: 0.654 -> 0.632 (-2.2pp; within 1 stderr noise)
- MMLU acc: 0.5796 -> 0.6179 (+3.83pp; typical IFT lift)
- TriviaQA EM: 0.396 -> 0.480 (+8.4pp; large IFT lift on factual recall)

So Instruct base has higher ceiling on MMLU+TriviaQA. The LoRA composed onto Instruct gets close to the non-Instruct base ceiling on these tasks (LoRA-Instruct MMLU 0.586 vs non-Instruct base MMLU 0.580 — basically equal), suggesting the LoRA "burns off" the IFT bonus.

## Hypothesis verdict

**Template-mismatch hypothesis: PARTIALLY supported but NOT primary driver**

- Switching to matching Instruct anchor reduces |Delta| by 1.2-1.8pp uniformly.
- On a 8-9pp degradation magnitude (TriviaQA), 1.2pp reduction = ~13% — small.
- On a 5pp magnitude (MMLU), 1.76pp reduction = ~36% — moderate.
- HellaSwag goes from -1.2pp (within noise) to +0.4pp (within noise) — qualitatively unchanged.

**Catastrophic forgetting hypothesis: CONFIRMED**

- 2/3 benchmarks (MMLU, TriviaQA) show statistically significant degradation under matching anchor.
- 64-88% of observed degradation is base-independent.
- Adapter directly degrades factual recall + multitask MC accuracy regardless of which sibling base it composes onto.

## F1_v3 V2 verdict with Instruct anchor

| criterion | result      | count |
|-----------|-------------|-------|
| c3 LoRA-base 2sigma | PASS | 2/3 (mmlu+triviaqa) |
| c4 LoRA >= rand+5pp | PASS | 3/3 |
| F1_v3 V2 overall    | SUCCESS | infrastructure pass / science fail (degradation direction) |

Same hybrid as BG-Rho: pipeline works, falsifier framework detects the LoRA-base separation, but separation is in the wrong direction (down).

## Pod lifecycle

- pod_id: `w7b46czo3ekxof`
- gpu: 1x H100 80GB HBM3 SECURE on-demand @ $2.99/hr
- ssh ready: 18s after boot (2 probes)
- benchmark wall: ~27min (sentinel detected at elapsed=27min)
- final scp: ~200s window
- post-kill: 404 verified
- total wall: 31min, cost $1.54 (well within $3.50 hard cap, $2.50 target)

## Lessons learned (new)

1. **L7 — runpodctl pod get -o json env-field leaks tokens**: trap-time `_kill_pod()` calls `runpodctl pod get` which dumps full pod env including `HF_TOKEN` literal. Lesson L5 (sed redact at boot) only covered boot.log; trap output goes to run.log + nohup directly. Post-hoc redaction was applied across all 6 log files (run.log, exec.nohup.log, h100_orchestrator.log, boot.log, pod_info.json, heartbeat.txt). **Future cycles must pipe ALL runpodctl output through `redact_hf` filter, including in trap functions.**

2. **L8 — jq -n with non-ASCII string literals is brittle**: emitting verdict.json via inline `jq -n --arg ... '{...honest_c3: ["..."]}'` with the Greek letter Rho (U+03A1) inside a string literal caused a jq compile error (the bash interpolated `BG-Rho` string in the awk command also had escaping issues with the Greek Rho rendered as `Ρ`). **Future emit pattern should use jq --rawfile for honest_c3 array, or restrict to ASCII-only string set.** (Worked around post-hoc by reconstructing verdict.json directly from result JSONs + run.log values.)

3. **L9 — Result JSONs survive even when verdict computation fails**: because run_h100.bash wrote per-bench JSONs first and emitted the sentinel, all 6 numeric metrics + log_samples + eval_results.json were intact even though the Mac-side jq emit failed. This validated the data-first design (lesson L6). Verdict reconstruction was straightforward.

## Next steps (recommended)

1. **Update F1_v3 V2 with two-anchor evidence**: BG-Rho + BG-Psi together establish that catastrophic forgetting is the dominant signature (~64-88% of effect) and template-mismatch is a real but minor (~12-36%) contributor. Update the F-1_v3 spec to require multi-anchor reporting going forward.
2. **Path A retrain v2 (BG-Phi territory)**: must use lower learning rate or KL-distillation to base to mitigate catastrophic forgetting. The Instruct base eval here gives a clear quantitative target: LoRA must reach Instruct base parity (0.617 MMLU, 0.480 TriviaQA, 0.632 HellaSwag) without dropping >=2 stderr.
3. **Optional follow-up BG**: re-eval with apply_chat_template=true to test if proper Instruct chat framing further reduces |Delta| (would distinguish "raw-prompt-on-Instruct" vs "chat-template-on-Instruct" ceilings).

## Deliverables (all paths absolute)

- `/Users/ghost/core/anima/state/p9_lora_mode1_instruct_eval_2026_05_04/verdict.json`
- `/Users/ghost/core/anima/state/p9_lora_mode1_instruct_eval_2026_05_04/results/` (6 JSONs + 6 log_sample dirs + sentinel + eval_results.json)
- `/Users/ghost/core/anima/state/p9_lora_mode1_instruct_eval_2026_05_04/exec.bash`
- `/Users/ghost/core/anima/state/p9_lora_mode1_instruct_eval_2026_05_04/run_h100.bash`
- `/Users/ghost/core/anima/state/p9_lora_mode1_instruct_eval_2026_05_04/run.log`
- `/Users/ghost/core/anima/state/p9_lora_mode1_instruct_eval_2026_05_04/h100_orchestrator.log`
- `/Users/ghost/core/anima/tool/p9_lora_mode1_instruct_eval_h100_orchestrator.hexa`
- `/Users/ghost/core/anima/docs/p9_lora_mode1_instruct_eval_landed_2026_05_04.ai.md` (this file)

## Compliance summary

- **raw#9**: Mac-side bash sibling pattern; zero new Mac .py
- **raw#10**: 7 honest C3 caveats in verdict.json
- **raw#15**: all paths absolute Mac or /workspace/* H100 transient
- **raw#37**: H100 SECURE on-demand; no ubu1
- **raw#71**: thresholds (c3 2sigma, c4 rand+5pp, shrink 0.5/0.25) fixed pre-launch
- **git ops**: NONE in this cycle (parent serializes)
- **HF token redaction**: post-hoc applied across all 6 log files; verified 0 token literals remain
