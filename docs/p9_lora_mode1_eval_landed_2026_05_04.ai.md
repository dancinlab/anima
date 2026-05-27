# P9 LoRA Mode 1 Eval — Landed Handoff (2026-05-04)

**Cycle**: `p9_lora_mode1_eval_2026_05_04`
**Spec ref**: BG-Ξ amendment `f6eb6517` (F1_v3 V2 c3+c4 thresholds), BG-ξ verify_report (step-8k anchor), BG-Ο `93bef8c8` (Llama base anchors)
**BG sibling**: BG-Ρ (this) — parallel with BG-Σ (`opt_1_v4_exec_*`) and BG-Τ (`triviaqa_filter_audit`)
**Verdict**: **PASS** (with `INFRASTRUCTURE_PASS / SCIENCE_FAIL` caveat — see §3)
**Wall**: 22 min · **Cost**: $1.10 (single attempt-2 pod) / $1.20 cumulative (both attempts)

---

## TL;DR

- **F1_v3 V2 = SUCCESS** (all 4 criteria PASS): c1 anchors_run, c2 llama±10%, c3 lora-base 2σ, c4 lora≥random+5pp.
- **But** the c3 deltas are uniformly **negative** — Path A step-8k LoRA degrades Llama-3.2-3B base on all 3 academic benchmarks:
  - HellaSwag acc_norm: 0.654 → 0.642 (Δ −1.2pp, within noise)
  - MMLU 5-shot: 0.5796 → 0.5301 (Δ −4.95pp, **statistically significant**)
  - TriviaQA EM: 0.396 → 0.302 (Δ −9.4pp, **statistically significant**)
- This validates the **falsifier framework** (we can detect a non-zero LoRA-vs-base separation) but **not** the LoRA itself as a beneficial adaptation. Direction is consistent with the **catastrophic-forgetting hypothesis** flagged in BG-Ξ omnibus commit `11331fe4` hint.

---

## 1. Per-benchmark numbers (LoRA vs Llama-3.2-3B base, BG-Ο anchors)

| Benchmark | Metric | LoRA | Llama base | Δ (pp) | 2σ threshold (pp) | c3 | c4 |
|---|---|---:|---:|---:|---:|---|---|
| HellaSwag | acc_norm 0-shot | 0.642 | 0.654 | −1.2 | 4.29 | FAIL (within noise) | PASS |
| MMLU | acc 5-shot | 0.5301 | 0.5796 | −4.95 | 0.87 | **PASS** (sig.) | PASS |
| TriviaQA | EM 0-shot remove_whitespace | 0.302 | 0.396 | −9.4 | 4.38 | **PASS** (sig.) | PASS |

c3 PASS count = 2/3 → c3 verdict = PASS (≥2/3 rule).
c4 PASS count = 3/3 → c4 verdict = PASS.
Both PASS → **F1_v3 V2 = SUCCESS**.

---

## 2. F1_v3 V2 cumulative status

| Criterion | Source BG | Verdict |
|---|---|---|
| c1 anchors_run | BG-Ο 93bef8c8 | PASS |
| c2 llama±10% | BG-Ο 93bef8c8 | PASS (2/3) |
| c3 lora−base 2σ | THIS BG | PASS (2/3) |
| c4 lora≥random+5pp | THIS BG | PASS (3/3) |
| **F1_v3 V2 overall** | — | **SUCCESS** (all 4 criteria PASS) |

---

## 3. Infrastructure-pass / science-fail caveat

The c3 and c4 criteria measure **separation** and **non-collapse**, respectively. Both are PASS. But:

- **c3 detects degradation as readily as improvement** — it's a magnitude-of-effect test, not a direction test.
- All 3 benchmarks show LoRA *worse* than Llama base. Two of those degradations are statistically significant.

Reading this honestly:

- **Infrastructure**: ✅ PASS — pipeline works, anchors hold, LoRA correctly composed onto base, results files materialize, falsifier framework distinguishes signal from noise.
- **Science**: ❌ FAIL — the trained adapter is a regression on these academic benchmarks. It is NOT a viable F1_v3 verdict-delta improver in its current state.

**Likely cause** (per BG-Ξ omnibus hint): SFT corpus distribution mismatch. The Path A training corpus (`sft_data_full_50k_augmented.jsonl`, axis-conditioned anima recipes) targets behaviors orthogonal to academic-benchmark factual recall + commonsense MC. 5 epochs of SFT with high learning-rate LoRA (r=64, lr=1e-4) likely overwrote some of the base model's pretrained factual representations — classic catastrophic forgetting on out-of-distribution evaluation.

---

## 4. Adapter-base composition caveat

The HF adapter_config.json declares `base_model_name_or_path = meta-llama/Llama-3.2-3B-Instruct`, but BG-Ο anchored on **non-Instruct** `meta-llama/Llama-3.2-3B`. We composed the LoRA onto non-Instruct base to maintain Δ-comparability with the BG-Ο anchor. This may amplify apparent degradation due to template-mismatch artifacts.

Future cleaner re-eval options:
1. Re-run BG-Ο anchors on `Llama-3.2-3B-Instruct` and compose LoRA onto Instruct — proper Δ would be `Instruct+LoRA − Instruct`.
2. Retrain Path A LoRA with `base = Llama-3.2-3B` (non-Instruct, matching BG-Ο anchor).

Both options are out-of-scope for this BG.

---

## 5. Step-8k anchor caveat (BG-ξ inheritance)

LoRA evaluated = HF commit `5a9b4584` ("Training in progress, step 8000"), not the pre-registered step-10000 ckpt. Per BG-ξ verify_report, the final 2000 steps + `final/` save never reached the HF mirror (lost during pod-termination push race). The reported degradations may differ ±5-10% from what a true step-10k LoRA would show. Cannot disambiguate without retraining or recovering the lost ckpt.

---

## 6. Lessons learned

### L-attempt1: lm-eval `revision=` flag scope confusion

Initial attempt passed `revision=5a9b4584` to lm-eval `--model_args`, expecting it to pin the LoRA adapter at step-8k. **It does not** — `revision=` applies to the base `pretrained` model. Result: 404 against `meta-llama/Llama-3.2-3B@5a9b4584`.

**Fix**: Pre-download LoRA at pinned revision via `hf download <repo> --revision <sha> --local-dir <path>`, then pass `peft=<local_path>`. No `revision=` in lm-eval args.

Cost of this lesson: $0.10 (attempt1 pod, 2 min wall, killed within 90s of sentinel-on-error).

### L-attempt2: ssh-detach hang on launch

The launch ssh command (`nohup bash run_h100.bash > orchestrator.log 2>&1 & disown ...`) hung the local exec.bash for ~5 min because the remote backgrounded process kept the ssh channel open even with `disown`. Standard fix: add `</dev/null` to redirect stdin away from ssh channel.

In this BG, manual `kill <ssh-pid>` from a sibling Bash call unblocked the exec.bash and the run_h100.bash on pod continued unaffected (since it was backgrounded with stdin/stderr already redirected).

**Future**: emitted launch line should be `nohup bash run_h100.bash </dev/null > orchestrator.log 2>&1 & disown`.

### L-verdict: awk quote-escaping bug

The c3_check awk function had unescaped `"PASS|"`/`"FAIL|"` literals inside the outer `awk "BEGIN{...}"` double-quoted string, causing bash to terminate the awk string prematurely → empty awk output → empty c3 verdict → c3 reported FAIL 0/3 in auto-emitted verdict.json.

**Fix applied (post-hoc)**: Recomputed c3 manually using `awk -v` flag (passes values as awk variables, not via shell interpolation into awk string), wrote corrected verdict.json. The c3 LOGIC is correct; only the bash emit had the escaping bug.

**Future**: orchestrator hexa template should use `awk -v key=value` pattern uniformly.

---

## 7. Deliverables

- `state/p9_lora_mode1_eval_2026_05_04/verdict.json` (corrected, schema=anima/p9_lora_mode1_eval/verdict/1)
- `state/p9_lora_mode1_eval_2026_05_04/results/lora_hellaswag.json`
- `state/p9_lora_mode1_eval_2026_05_04/results/lora_mmlu.json`
- `state/p9_lora_mode1_eval_2026_05_04/results/lora_triviaqa.json`
- `state/p9_lora_mode1_eval_2026_05_04/results/lora_*_dir/` (log_samples per-prompt, ~155MB total)
- `state/p9_lora_mode1_eval_2026_05_04/results/COMPLETE.sentinel`
- `state/p9_lora_mode1_eval_2026_05_04/run.log` (redacted)
- `state/p9_lora_mode1_eval_2026_05_04/exec.bash` (emitted)
- `state/p9_lora_mode1_eval_2026_05_04/run_h100.bash` (emitted)
- `state/p9_lora_mode1_eval_2026_05_04/h100_orchestrator.log`
- `tool/p9_lora_mode1_eval_h100_orchestrator.hexa` (orchestrator template, NEW)
- Attempt1 aside: `state/p9_lora_mode1_eval_2026_05_04/{results_attempt1/,run.attempt1.log,verdict.attempt1.json,h100_orchestrator.attempt1.log,pod_info.attempt1.json,boot.attempt1.log,heartbeat.attempt1.txt,exec.nohup.attempt1.log}`

---

## 8. Roadmap proposals (parent serializes)

```jsonl
{"id":"p9_sft.cond.f1_v3_v2_c3_lora_base_2_sigma","status":"PENDING → PASS","ts":"2026-05-04T09:05:00Z","cycle_ref":"p9_lora_mode1_eval_2026_05_04","reason":"LoRA(step-8k)−Llama-base 2σ separation PASS on 2/3 benchmarks (mmlu+triviaqa) per BG-Ξ amendment f6eb6517 ≥2/3 rule"}
{"id":"p9_sft.cond.f1_v3_v2_c4_lora_above_random_5pt","status":"PENDING → PASS","ts":"2026-05-04T09:05:00Z","cycle_ref":"p9_lora_mode1_eval_2026_05_04","reason":"LoRA acc ≥ random+5pp on 3/3 benchmarks (0.642/0.530/0.302 vs thresholds 0.30/0.30/0.05)"}
{"id":"p9_sft.cond.f1_v3_v2_overall","status":"PENDING → SUCCESS_WITH_CAVEAT","ts":"2026-05-04T09:05:00Z","cycle_ref":"p9_lora_mode1_eval_2026_05_04","reason":"All 4 criteria PASS but direction of c3 deltas is uniformly negative (LoRA degrades base); INFRASTRUCTURE_PASS / SCIENCE_FAIL hybrid; falsifier framework validates but trained adapter is a regression on these benchmarks"}
{"id":"p9_sft.cond.path_a_lora_step8k_quality","status":"UNKNOWN → REGRESSION_VS_BASE","ts":"2026-05-04T09:05:00Z","reason":"step-8k LoRA causes 4.95pp MMLU drop and 9.4pp TriviaQA EM drop relative to Llama-3.2-3B base; consistent with catastrophic-forgetting hypothesis from BG-Ξ omnibus 11331fe4"}
```

---

## 9. Honest C3 (raw#10)

See verdict.json `honest_c3_caveats` for 7 caveats. Top 3:

1. **Step-8k anchor not step-10k** — eval target is the partial adapter (80% of pre-registered training); cannot rule out that step-10k would have shown improvement (though the trajectory in train.log already showed loss converged at 0.27 by step-8k, so additional improvement unlikely).
2. **Adapter-base mismatch** — adapter trained on Llama-3.2-3B-Instruct, evaluated on non-Instruct base. Re-eval on Instruct base may shift Δ by 2-5pp.
3. **Single-seed (42) limit=500** — multi-seed bootstrap or full-dataset eval needed to confirm degradation magnitude is robust.

---

## 10. Constraint compliance

- raw#9: hexa-only Mac (orchestrator hexa + emitted bash sibling); zero new .py on Mac
- raw#10: 7 honest C3 caveats in verdict.json
- raw#15: paths repo-relative on Mac, /workspace/* on H100 (transient)
- raw#37: H100 transient python (lm_eval+peft+transformers) permitted; ubu1 not used
- raw#71: c3+c4 thresholds frozen pre-launch (BG-Ξ amendment); only fix was awk quote-escape (no threshold tweak)
- HF token never written raw to long-lived files; sed redact pre-tee on boot.log + post-hoc on pod_info.json
- Pod 8umghrgn5v3zct killed and 404 verified
- No git operations in this cycle (parent serializes)
- No external r=16 retrain pods (`nzw0btc8br78yy`, `0jetjpvlm51zoy`) touched
- No BG-Σ / BG-Τ files touched

---

## 11. Next actions (out-of-scope here)

- **Re-eval on Instruct base** — would clarify whether degradation is real or template-mismatch artifact (~1.5h, $4.50)
- **Recover or retrain step-10k** — confirm whether last 2k steps shifted direction (long: ~12h, $36)
- **Distribution-aware retraining** — train Path A LoRA with mixed corpus (anima axes + academic benchmark held-in) to test whether catastrophic forgetting is recoverable
- **Mode 2 eval** — CLM v4 base on same 3 benchmarks, for cross-substrate comparison

---

**End of handoff.**
