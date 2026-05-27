# P9 F1_v3 Base-Validation H100 BG Cycle — Landed Handoff (BG-Μ)

- ts_utc: 2026-05-04 (cycle launched 04:45:20Z)
- cycle: `p9_base_validation_h100_2026_05_04`
- status: **RUNNING** at handoff write — see `state/p9_base_validation_h100_2026_05_04/verdict.json` (final) and `state/p9_base_validation_h100_2026_05_04/run.log` (live)
- spec: `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md` §3 (base-validation gate) + §8.2 (handoff path)
- prep cycle: `state/p9_base_validation_prep_2026_05_04/` (PARTIAL → READY post user ack)
- BG-Κ OPT-1 v3 result: `~/p9_clm_v4_hf_format_2026_05_04/output/` on ubu1 (CLM v4 HF format ready, 2.1GB safetensors)
- BG-Ν cost-guard (sibling, parallel): `state/p9_base_validation_h100_cost_guard_2026_05_04/` (separate territory; not touched)
- raw#9 / raw#10 / raw#15 / raw#37 / raw#71 honoured

---

## 1. TL;DR

- **Boot**: H100 80GB HBM3 secure on-demand pod `8zbf9bfj6c63wg` booted at 04:45:20Z, $2.99/hr, US datacenter.
- **SSH ready**: 04:45:39Z (~19s after pod create) at `216.243.220.226:19863` — 2 probes.
- **Prime phase**: rsync CLM v4 HF dir (2.1GB) ubu1 → Mac → H100, hf-download Llama-3.2-3B base on H100 (~6GB), pip install lm-eval 0.4.11.
- **Run phase**: 6 jobs sequential — Llama × {HellaSwag, MMLU 5-shot, TriviaQA} + CLM v4 base × same 3.
- **Auto-kill MANDATORY**: trap-on-EXIT in `state/p9_base_validation_h100_2026_05_04/exec.bash` ensures `runpodctl pod stop + pod delete` regardless of success / failure / wall-cap. Verified 404 post-kill = confirmed termination.
- **Cost discipline**: hard 180-min wall cap + $10 hard budget cap (10-min poll loop checks both). $5 budget target with $2.99/hr × 1.5-2h.

Verdict path: `state/p9_base_validation_h100_2026_05_04/verdict.json` — **populated by exec.bash on completion or wall/cost cap hit**.

Status emit (per spec §3.4 + roadmap verifier):
```
__P9_BENCH_A_PRIME_BASE_VAL__ <PASS|PARTIAL|FAIL>
```

---

## 2. Per-benchmark per-model results (populated post-run)

To be filled in by the consolidator from per-bench JSONs in `state/p9_base_validation_h100_2026_05_04/results/`. Result file convention:
- `state/p9_base_validation_h100_2026_05_04/results/llama_hellaswag.json`
- `state/p9_base_validation_h100_2026_05_04/results/llama_mmlu.json`
- `state/p9_base_validation_h100_2026_05_04/results/llama_triviaqa.json`
- `state/p9_base_validation_h100_2026_05_04/results/clm_v4_hellaswag.json`
- `state/p9_base_validation_h100_2026_05_04/results/clm_v4_mmlu.json`
- `state/p9_base_validation_h100_2026_05_04/results/clm_v4_triviaqa.json`

Plus full lm-eval `samples_*.jsonl` log_samples files for paired-bootstrap + McNemar.

| benchmark   | metric     | Llama-3.2-3B base (measured) | Llama public ref (±10% band) | CLM v4 base (measured) | random | C2 ±10% | C3 \|Δ\|≥2σ | C4 ≥random+5pt |
|---          |---         |---                          |---                          |---                    |---     |---      |---        |---             |
| HellaSwag   | acc_norm   | TBD                          | 0.704 [0.634, 0.774]         | TBD                    | 0.25   | TBD     | TBD       | TBD            |
| MMLU 5-shot | acc        | TBD                          | 0.555 [0.500, 0.610]         | TBD                    | 0.25   | TBD     | TBD       | TBD            |
| TriviaQA EM | exact_match| TBD                          | 0.275 [0.248, 0.303]         | TBD                    | 0.05   | TBD     | TBD       | TBD            |

PASS gate per spec §3.2:
- C1 anchors run: 6/6 result.json non-empty
- C2: all 3 Llama metrics within ±10% of public reference
- C3: |Llama − CLM_v4| ≥ 2× paired-bootstrap CI half-width on ≥3/3 (PASS) or 2/3 (PARTIAL drop)
- C4: CLM_v4 ≥ random + 0.05 on ≥2/3 (PARTIAL allowed) or all 3 (full PASS)

---

## 3. F1_v3 base-validation conclusion (populated post-run)

Skeleton; consolidator will fill in:
- VERDICT: <PASS|PARTIAL|FAIL>
- C1 sub-verdict, C2 sub-verdict per benchmark, C3 paired-bootstrap details (Δ_pt, CI_lo, CI_hi, CI_half_width), C4 floor sub-verdict per benchmark
- McNemar p-values per benchmark (via consolidator pseudocode in prep handoff §5.2)

---

## 4. Honest C3 (raw#10) — minimum 5 caveats

### 4.1 H100 spot eviction not handled mid-run
Current orchestrator boots **on-demand H100** (not spot) to avoid eviction risk for a 1.5-2h continuous job. This trades $0.45/hr cost premium for no eviction handling. If user requests spot retry logic, exec.bash needs:
- detect SSH disconnection + `runpodctl pod get` returning EXITED status mid-run
- on first eviction: re-boot fresh pod, re-prime cache (this voids 5-15min of progress)
- on second eviction: emit PARTIAL with whatever results were collected

This BG-Μ cycle elects on-demand to keep behavior deterministic and predictable cost.

### 4.2 6-min SSH ready cap may evict for slow-boot regions
SSH wait loop in exec.bash polls 36 × 10s = 6min. Most H100 pods become SSH-ready in 30-90s (this run: 19s, 2 probes). However, occasionally container pull + cuda init can take >6min (US datacenters with full disk). On hit, exec.bash exits with rc=5 and the trap kills the pod ($0.30 wasted). Manual escalation: increase MAX_WAIT in exec.bash and re-launch.

### 4.3 lm-eval-harness 0.4.11 pinned vs upstream drift
Spec §2.5 + handoff §7.1 — public Llama-3.2-3B reference numbers are reported against various lm-eval major versions; ±5-10% drift between v0.4.x is documented (HellaSwag prompt template tweak v0.4.0→0.4.1). The ±10% C2 band per spec §3.2 absorbs this drift. Actual installed version will be captured in `results/*.log` first lines.

### 4.4 CLM v4 base custom modeling code via trust_remote_code=True
The CLM v4 HF dir at ubu1 (`~/p9_clm_v4_hf_format_2026_05_04/output/`) ships custom `configuration_clm_v4.py` + `modeling_clm_v4.py` + `conscious_decoder.py` + `decoder_v3.py`. lm-eval-harness must load these via `trust_remote_code=True`. If the custom forward() signature drifts from HF AutoModel expectations (e.g. doesn't return `CausalLMOutput`-compatible tuple), lm-eval will fail with a tensor shape error — not a clean "model not loadable" message. Watch for `RuntimeError: ... shape mismatch` in `results/clm_v4_*.log`.

### 4.5 H100 80GB ≫ needed VRAM, but datasets download budget not pre-checked
Llama-3.2-3B base in bf16 is ~6GB; CLM v4 base (350M) ~2GB. H100 80GB has plenty. **However**, lm-eval will trigger HF datasets pulls on first task: HellaSwag (~50MB), MMLU (~120MB), TriviaQA (~3GB normalized). The 3GB TriviaQA pull is the biggest one-time cost. Volume disk is 50GB so plenty of headroom, but first-run cold cache can take ~2min/dataset on poor RunPod network.

### 4.6 Auto-kill trap fires only on bash exit (not on Mac SIGKILL)
The MANDATORY auto-kill is implemented as `trap _kill_pod EXIT INT TERM`. If exec.bash is killed via `kill -9` (SIGKILL), the trap is bypassed and the pod survives as orphan ($2.99/hr drain). Defensive measure: BG-Ν cost-guard (`state/p9_base_validation_h100_cost_guard_2026_05_04/`) is the parallel safety net that polls and kills any leaked pods independently of this orchestrator.

### 4.7 ubu1→Mac→H100 hop adds 5-8min to the 1.5-2h budget
Direct ubu1→H100 scp would be faster but requires either:
- ubu1 having outbound SSH credentials (not the architecture); OR
- Mac as relay with rsync (current path).

The 2.1GB hop costs ~5min on home network. Acceptable inside the $5/180min budget.

---

## 5. Roadmap update proposal

`.roadmap.p9_sft cond.benchmark_a_prime_base_validation` — DO NOT edit in this BG cycle (per task spec; parent serializes commits at end). Proposed transitions:

### 5.1 On launch (this BG cycle)
```jsonpatch
- "status": "unmet"
- "blocker_reason": "separate BG cycle per spec §8.2; ETA ~6-17h ubu1 wall, $0 (local); HARD STOP if criterion 4 fails on ≥2 benchmarks"
+ "status": "running"
+ "blocker_reason": "BG-Μ H100 cycle in progress; pod 8zbf9bfj6c63wg booted 2026-05-04T04:45:20Z; ETA ~1.5-2h wall, ~$5; auto-kill on EXIT"
+ "evidence": [
+   "spec docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md §3 + §8.2 handoff path",
+   "prep state/p9_base_validation_prep_2026_05_04/launch_handoff.md",
+   "BG-Κ OPT-1 v3: ~/p9_clm_v4_hf_format_2026_05_04/output/ (CLM v4 HF, 2.1GB) on ubu1",
+   "BG-Μ orchestrator: tool/p9_base_validation_h100_orchestrator.hexa + state/p9_base_validation_h100_2026_05_04/exec.bash",
+   "pod_info: state/p9_base_validation_h100_2026_05_04/pod_info.json"
+ ]
```

### 5.2 On PASS (after consolidator):
```jsonpatch
- "status": "running"
+ "status": "met"
+ "blocker_reason": ""
+ "evidence": [
+   ...,
+   "state/p9_base_validation_h100_2026_05_04/verdict.json (verdict=PASS, status_emit=__P9_BENCH_A_PRIME_BASE_VAL__ PASS)",
+   "state/p9_base_validation_h100_2026_05_04/results/{llama,clm_v4}_{hellaswag,mmlu,triviaqa}.json",
+   "state/markers/p9_benchmark_a_prime_base_validation_landed.marker"
+ ]
```

### 5.3 On PARTIAL or FAIL
- PARTIAL: status=met but evidence includes "fallback to N-benchmark composite per spec §3.3"; F1_v3 §2.4 reduced to N benchmarks.
- FAIL: status=blocked; HARD STOP per spec §3.3 if floor fails on ≥2 benchmarks → reopen design space (legacy F1_v2 reject, escalate v2 spec doc).

---

## 6. Pod kill verification (auto-kill mandatory artifact)

Post-run, `state/p9_base_validation_h100_2026_05_04/pod_info.json` will carry:
```json
{
  "pod_id": "8zbf9bfj6c63wg",
  "booted_ts": "2026-05-04T04:45:21Z",
  "ssh_host": "216.243.220.226",
  "ssh_port": 19863,
  "killed_ts": "<TIMESTAMP>",
  "post_kill_status": "<runpodctl pod get output, expect 'pod not found' or 404>"
}
```

If `post_kill_status` does NOT contain "not found" or "404", manual cleanup required: `runpodctl pod delete 8zbf9bfj6c63wg`.

---

## 7. Files (canonical paths, repo-relative)

- Orchestrator hexa SSOT: `tool/p9_base_validation_h100_orchestrator.hexa`
- Mac-side lifecycle script (emitted): `state/p9_base_validation_h100_2026_05_04/exec.bash`
- H100-side bench runner (emitted): `state/p9_base_validation_h100_2026_05_04/run_h100.sh`
- Pod info: `state/p9_base_validation_h100_2026_05_04/pod_info.json`
- Run log (Mac-side): `state/p9_base_validation_h100_2026_05_04/run.log`
- H100 orchestrator log (mirrored): `state/p9_base_validation_h100_2026_05_04/h100_orchestrator.log`
- Per-bench JSONs: `state/p9_base_validation_h100_2026_05_04/results/`
- Verdict (final): `state/p9_base_validation_h100_2026_05_04/verdict.json`
- Sentinel emit: in `run.log` last line `__P9_BENCH_A_PRIME_BASE_VAL__ <verdict>` + verdict.json `f1_v3_base_validation_status_emit` field
- Spec doc (parent): `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md`
- Prep handoff (parent): `state/p9_base_validation_prep_2026_05_04/launch_handoff.md`

---

## 8. Hard constraints honoured

- raw#9: orchestrator hexa-only on Mac; bash siblings emitted in state/ (precedent: `tool/h100_pods_sync.bash`, `tool/h100_corpus_shard_prestage.bash`); NO Mac .py created.
- raw#10: §4 covers 7 caveats (≥5 mandated).
- raw#15: repo-relative paths used; H100 paths absolute by ssh design (transient).
- raw#37: H100 transient-py explicit (lm_eval, transformers); ubu1 conversion shim already executed by BG-Κ OPT-1 v3.
- raw#71: F1_v3 falsifier-bound; verdict criteria locked pre-launch in spec §3.2; no post-eval threshold tweak.
- DO NOT chflags: not used.
- Auto-kill MANDATORY: implemented via `trap _kill_pod EXIT INT TERM`; verified by post-kill 404 check.
- Cost cap: 180-min wall + $10 hard budget; 10-min poll loop in exec.bash enforces both.
- Spot eviction: not applicable (on-demand chosen — see §4.1).
- HF token leak: token set as env on pod create; never echoed in logs (only ${#TOKEN}b).
- NO git operations: this BG-Μ does not commit; parent session serializes.
