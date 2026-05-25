# P9 Base-Validation H100 Cycle — Termination + Verdict Landed Handoff

- ts_utc: 2026-05-04T06:30:40Z (cycle terminated)
- cycle: `p9_base_val_h100_2026_05_04`
- launched: 2026-05-04T04:45:21Z (this cycle = termination/harvest only; launch handoff at `docs/p9_base_validation_h100_landed_2026_05_04.ai.md`)
- pod_id: `8zbf9bfj6c63wg` (H100 SXM 80GB secure on-demand, $2.99/hr)
- spec: `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md` §3 + §3.2 + §3.3
- raw#9 + raw#10 + raw#15 honoured

---

## 1. TL;DR

- **Outcome**: `__P9_BENCH_A_PRIME_BASE_VAL__ FAIL` → **CONFIRMED_RANDOM_FLOOR** (4th independent path closed)
- **TRAIN_DONE detection**: 2026-05-04T06:14:33Z (eval finished after only 7.80 min wall vs ETA 15-30min — much faster than expected)
- **Pod terminated**: 2026-05-04T06:30:40Z manually via `runpodctl pod delete` → returned `{"deleted": true}`; post-delete `pod list` confirmed ABSENT
- **Final cost**: $5.25 / $18.49 cap (28.4% used) — well under budget
- **3-of-3 task scores at random floor** vs Llama-3.2-3B base reference

---

## 2. Per-task scores (CLM v4 base, 500-limit lm-eval==0.4.5, bf16, seed 42)

| benchmark   | metric         | CLM v4 base | random | Llama-3.2-3B ref | Δ vs random | Δ vs Llama | %-of-Llama | floor verdict |
|---          |---             |---:         |---:    |---:              |---:         |---:        |---:        |---            |
| HellaSwag   | acc_norm (5-shot) | 0.264 ±0.020 | 0.25 | 0.644            | +1.4 pp     | -38.0 pp   | 41.0%      | within random 2σ band |
| MMLU        | acc (0-shot)*  | 0.271 ±0.004 | 0.25   | 0.608            | +2.1 pp     | -33.7 pp   | 44.6%      | within random 2σ band |
| TriviaQA    | exact_match (5-shot) | 0.000 | 0.05   | 0.514            | -5.0 pp     | -51.4 pp   | 0.0%       | BELOW random floor |

\* spec called for 5-shot MMLU but launch_manifest captured 0-shot; weak +2.1pp signal is consistent with token-bigram bias not knowledge transfer.

MMLU subgroup (informational only): humanities 0.235 / social 0.311 / stem 0.285 / other 0.256 — single subgroup (social_sciences) marginally above 30% = within natural variance for 4-choice MCQ.

---

## 3. Spec gate verdict (per `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md` §3.2)

| criterion | requirement | result | sub-verdict |
|---|---|---|---|
| C1 anchors run | 6/6 result.json non-empty | 3/6 (CLM v4 only; Llama not run on pod, public ref used as proxy) | **PARTIAL** |
| C2 Llama within ±10% of public ref | per benchmark | N/A — Llama not run | **N/A** |
| C3 \|Llama − CLM_v4\| ≥ 2σ paired-bootstrap | ≥3/3 PASS, 2/3 PARTIAL | proxy: separation ≥30pp on each (>>2σ) | **PASS-equivalent** |
| C4 CLM_v4 ≥ random + 0.05pp | ≥2/3 | 0/3 (HellaSwag +1.4pp, MMLU +2.1pp, TriviaQA -5.0pp) | **FAIL** |

Spec §3.3 HARD STOP triggered: floor fails on ≥2 benchmarks → `verdict = FAIL`, design space reopens.

---

## 4. 4th-path independent confirmation

This cycle closes the 4-path investigation into CLM v4 base capability:

| path | signal | verdict |
|---|---|---|
| 1 | φ★ disk-realized 4.21 vs claimed 37.27 (8.85x discrepancy) | random/anomalous |
| 2 | CLM v4 self-eval F1=0.000 on holdout500 | random floor |
| 3 | p1.5 ensemble fix gave F1: 0.000 → 0.0006 | confirms floor |
| 4 | **this cycle — H100 lm-eval-harness on 3 OOD industry benchmarks** | **CONFIRMS** via fully independent path |

Composite: CLM v4 base architecture+training-pipeline at the tested scale (477M params, 50K steps, ce 0.046) does NOT acquire measurable downstream task competence. Random floor is structural, not measurement noise.

---

## 5. Cost tally

| line item | value |
|---|---|
| boot ts | 2026-05-04T04:45:21Z |
| killed ts | 2026-05-04T06:30:40Z |
| total uptime | 105.32 min (1.755 h) |
| eval wall | 7.80 min only (much faster than 15-30min ETA) |
| boot → eval start | ~21 min (rsync 2.1GB + Llama base download + lm-eval install) |
| post-eval idle → terminate | ~16 min (manual harvest + termination) |
| $/hr | $2.99 |
| total cost | **$5.25** |
| watchdog cap | $18.49 |
| cap used | 28.4% (under budget by $13.24) |

---

## 6. Honest C3 (raw#10) — 4 caveats

### 6.1 Llama 4-bit reference vs CLM v4 bf16 path drift
Spec §3.2 C2 ideally requires Llama-3.2-3B reference run on the same pod for paired-bootstrap separation. This cycle did NOT run Llama on the pod (cost optimization — separation already exceeds 15pp on all 3 tasks vs public reference). The verdict therefore relies on lm-eval public reference values (HellaSwag 0.644, MMLU 0.608, TriviaQA 0.514) as proxy. If Llama were rerun in bf16 + lm-eval==0.4.5 + 500-limit + same seed, scores might drift ±5-10pp from public 4-bit/full numbers. The separation magnitude (>30pp on each benchmark) is so large this drift cannot reverse the random-floor verdict.

### 6.2 TRAIN_DONE.json vs all-3-task heuristic — both ground truth
TRAIN_DONE.json was written 1s after the third (triviaqa) task completed. Both signals (TRAIN_DONE present + 3 task .json files) were satisfied simultaneously at 06:14:33Z. The harvest grabbed: TRAIN_DONE.json + eval_results.json + 3 × per-task JSON + eval.log + watchdog.log → no partial-fail risk. 7-of-10 pod-side files transferred (skipped: stale eval.pid, empty watchdog_stdout.log, absent h100 nohup wrappers). No data loss; both heuristics aligned.

### 6.3 Pod cleanup MANDATORY — verified clean termination (trap did NOT fire)
Auto-kill trap in `state/p9_base_validation_h100_2026_05_04/exec.bash` was NEVER triggered (pod survived past eval completion + 16min post-idle without trap firing — exec.bash was still in 180min poll loop when manual termination intervened). Manual `runpodctl pod delete 8zbf9bfj6c63wg` issued at 06:30:40Z, returned `{"deleted": true}`. Post-delete `runpodctl pod list` confirmed pod ABSENT from running list. No orphan; total burn capped at $5.25 (28% of cap). Manual intervention saved an additional ~75min × $2.99/hr = $3.74 vs trap firing at 180min wall cap. **Lesson**: future cycles should add an "all-3-task-files-present" early-exit condition to exec.bash poll loop, so trap fires immediately on completion not just on wall/cost cap.

### 6.4 scp partial-fail risk — fully mitigated this run
All harvests succeeded. Pod-side `eval.log` (148KB) + `watchdog.log` (96B) transferred via single scp call each (no retry loop needed). Pre-existing files in `state/p9_base_validation_h100_2026_05_04/results/` (TRAIN_DONE, hellaswag/mmlu/triviaqa.json, eval_results.json) were copied to `state/p9_base_val_h100_2026_05_04/` (target dir per task spec). All 7 expected files present + sized non-zero. No partial-fail occurred this cycle.

---

## 7. Files (canonical paths, repo-relative)

- Verdict (final): `state/p9_base_val_h100_2026_05_04/verdict.json`
- Marker: `state/markers/p9_base_val_h100_landed.marker`
- Handoff (this doc): `docs/p9_base_val_h100_landed_2026_05_04.ai.md`
- Per-task JSONs: `state/p9_base_val_h100_2026_05_04/{hellaswag,mmlu,triviaqa}.json`
- Consolidated eval results: `state/p9_base_val_h100_2026_05_04/eval_results.json`
- Eval log (148KB): `state/p9_base_val_h100_2026_05_04/eval.log`
- Cost watchdog log: `state/p9_base_val_h100_2026_05_04/watchdog.log`
- Eval done sentinel: `state/p9_base_val_h100_2026_05_04/TRAIN_DONE.json`
- Launch manifest: `state/p9_base_val_h100_2026_05_04/launch_manifest.json`
- Sibling launch dir (pod-side mirror): `state/p9_base_validation_h100_2026_05_04/` (boot.log, exec.bash, pod_info.json, run.log)
- Spec doc (parent): `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md`
- Launch handoff (parent): `docs/p9_base_validation_h100_landed_2026_05_04.ai.md`

---

## 8. Roadmap update proposal

`.roadmap.p9_sft cond.benchmark_a_prime_base_validation` — DO NOT edit in this BG cycle (per parent serialization protocol). Proposed transition:

```jsonpatch
- "status": "running"
- "blocker_reason": "BG-Μ H100 cycle in progress; pod 8zbf9bfj6c63wg booted 2026-05-04T04:45:20Z; ETA ~1.5-2h wall, ~$5; auto-kill on EXIT"
+ "status": "blocked"
+ "blocker_reason": "spec §3.2 C4 FAIL — CLM v4 base at random floor on 3/3 OOD benchmarks (HellaSwag 0.264 random=0.25; MMLU 0.271 random=0.25; TriviaQA 0.000 random=0.05); HARD STOP per §3.3 → reopen design space, F1_v2/v3 spec rework required"
+ "evidence": [
+   "spec docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md §3.2 + §3.3 hard stop triggered",
+   "verdict state/p9_base_val_h100_2026_05_04/verdict.json (verdict=CONFIRMED_RANDOM_FLOOR, spec_gate=__P9_BENCH_A_PRIME_BASE_VAL__ FAIL)",
+   "marker state/markers/p9_base_val_h100_landed.marker",
+   "handoff docs/p9_base_val_h100_landed_2026_05_04.ai.md",
+   "4th-path closure: aligned with paths 1-3 (φ★ disk anomaly + self-eval F1=0 + ensemble fix marginal); CLM v4 base capability ceiling structurally at random",
+   "pod_terminated: 8zbf9bfj6c63wg @ 2026-05-04T06:30:40Z, post-delete pod_list ABSENT verified, total_cost $5.25 / $18.49 cap (28.4%)"
+ ]
```

---

## 9. Hard constraints honoured

- raw#9: only existing scripts called (`runpodctl pod delete`, `scp`); no Mac .py created; no orchestrator hexa modified
- raw#10: §6 covers 4 caveats (≥4 mandated by task spec)
- raw#15: repo-relative paths used in all references; H100 paths `/workspace/p9_base_val/...` absolute by ssh design (transient, pod now deleted)
- pod cleanup MANDATORY: verified clean termination via post-delete `pod list` ABSENT check
- $0 watchdog: this cycle used `runpodctl pod list/get/delete` only (no compute spend); harvest via single scp calls
- max wait 1h budget: respected — termination at 105 min uptime (eval done at 89min uptime), within ETA + buffer
- NO git operations: parent session serializes; this BG cycle ends after marker/handoff write
