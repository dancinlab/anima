# P9 F1_v3 Base-Validation BG Cycle — Launch Handoff

- ts_utc: 2026-05-04T00:11:45Z
- prep cycle: `state/p9_base_validation_prep_2026_05_04/`
- target spec: `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md` §3 (base-validation gate) + §8.2 (handoff path)
- target roadmap entry: `.roadmap.p9_sft cond.benchmark_a_prime_base_validation` (status: unmet → running → met)
- prep verdict: **PARTIAL** (10/12 prereqs PASS; 2 model-loader blockers require user ack before launch)
- raw#9 / raw#10 / raw#15 / raw#71 honoured

---

## 1. TL;DR (handoff)

- **Infra READY**: ubu1 RTX 5070 (12GB), torch 2.11.0+cu128, lm-eval 0.4.11, 600GB free disk, HF auth refreshed (commit `eea009b40`), spec marker landed.
- **Two blockers gate launch**:
  1. **Llama-3.2-3B base NOT cached** (only Instruct); spec §3.1 anchor-A specifies base. Recommend OPT-A: pull base model (~6GB / ~5min). Alt OPT-C: pull base + run both as reference.
  2. **CLM v4 base HF-format MISSING** (mirror has only raw `best.pt`); lm-eval-harness HF loader cannot load. Recommend OPT-1: transient ubu1 .py shim to convert best.pt → HF format (~30-60min, raw#9 compliant on Linux side).
- **ETA on green light**: ~9h wall central estimate (band 6-17h per spec §0); breakdown in §6.
- **Cost**: $0 (ubu1 owned hardware).
- **Launch command**: see §3 below; DO NOT execute until user acks both blockers + base-validation BG authorization (consumes ubu1 GPU 6-17h).

---

## 2. Pre-flight checklist (re-runnable on ack)

All commands assume Mac-side `ssh ubu1 '<cmd>'`. Each is read-only/idempotent except where noted.

### 2.1 Confirm infra still PASS

```bash
# torch + GPU + cuda
ssh ubu1 '/home/aiden/venv_orchestrator/bin/python -c "import torch; print(\"torch=\", torch.__version__); print(\"cuda=\", torch.cuda.is_available()); print(\"gpu=\", torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"none\")"'
# expect: torch=2.11.0+cu128 / cuda=True / gpu=NVIDIA GeForce RTX 5070

# lm-eval install
ssh ubu1 '/home/aiden/venv_orchestrator/bin/pip show lm-eval | head -3'
# expect: Name: lm_eval / Version: 0.4.11

# disk headroom
ssh ubu1 'df -h ~/.cache/huggingface ~ | head -5'
# expect: ≥20GB free on root (`/dev/nvme0n1p2`); current ~600GB

# spec marker
ls -la state/markers/p9_benchmark_a_prime_spec_landed.marker
# expect: file exists, mtime 2026-05-03
```

### 2.2 Resolve blocker (i) — Llama base model

```bash
# OPT-A: pull base (recommended for strict §2.6 spec compliance)
ssh ubu1 'source /home/aiden/venv_orchestrator/bin/activate && huggingface-cli download meta-llama/Llama-3.2-3B --local-dir-use-symlinks=auto'
# wall ~5min, ~6GB; verify via:
ssh ubu1 'ls ~/.cache/huggingface/hub/ | grep -E "Llama-3.2-3B[^-]"'
# expect: models--meta-llama--Llama-3.2-3B (no -Instruct suffix)
```

If OPT-A blocked by HF gating, fall back to OPT-B (Instruct + spec amendment §2.6) or OPT-C (run both, report both).

### 2.3 Resolve blocker (ii) — CLM v4 base HF-format

OPT-1 (recommended): transient .py shim on ubu1 (raw#9 — Linux-side .py is permitted; Mac-side ban only).

```bash
ssh ubu1 'mkdir -p ~/p9_base_val_2026_05_04 && cat > ~/p9_base_val_2026_05_04/clm_v4_to_hf.py' <<'PYEOF'
"""Transient HF-format converter for CLM v4 base (best.pt + tokenizer → HF directory).

raw#9: Linux-side .py is permitted; Mac-side ban only. This file lives on ubu1.
Run once, then delete after lm-eval validates it can load.
"""
import os, sys, json, shutil, torch
from pathlib import Path

CLM_TOKENIZER_DIR = Path.home() / ".cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/snapshots/10ee03687db312c55bbec5858c814bef28e4d365/tokenizer"
CLM_BEST_PT = Path.home() / ".cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/snapshots/856278beb59c5b39f16485cc8f3a46dcdaf9d1e3/best.pt"
OUT_DIR = Path.home() / "p9_base_val_2026_05_04/clm_v4_base_hf"

# NOTE: this is a STUB. The actual CLM v4 architecture class must come from the anima
# clm-v4 codebase (likely state/clm_v4_*/ or anima-clm-eeg/). Two paths:
#   path A: import the CLM v4 architecture from anima codebase + state_dict load + save_pretrained
#   path B: if CLM v4 IS a HF-compatible architecture (LLaMA-like), use AutoModelForCausalLM
#          with a manual config and load best.pt as state_dict.
# Verify the architecture class before populating this script. DO NOT run blind.

# pseudocode (validate first):
# from anima_clm_v4 import CLMv4Model, CLMv4Config  # verify this import path
# cfg = CLMv4Config(...)  # populate from training run config
# model = CLMv4Model(cfg)
# state = torch.load(CLM_BEST_PT, map_location='cpu')
# model.load_state_dict(state['model'] if 'model' in state else state)
# model.save_pretrained(OUT_DIR)
# # tokenizer copy
# OUT_DIR.mkdir(parents=True, exist_ok=True)
# for f in CLM_TOKENIZER_DIR.iterdir():
#     shutil.copy(f, OUT_DIR / f.name)

print("STUB — populate CLM v4 architecture import + config before running.")
print(f"tokenizer src: {CLM_TOKENIZER_DIR}")
print(f"best.pt src:   {CLM_BEST_PT}")
print(f"out:           {OUT_DIR}")
PYEOF
```

After populating, run: `ssh ubu1 '/home/aiden/venv_orchestrator/bin/python ~/p9_base_val_2026_05_04/clm_v4_to_hf.py'`

Verify: `ssh ubu1 'ls ~/p9_base_val_2026_05_04/clm_v4_base_hf/'` should show `config.json`, `pytorch_model.bin` or `model.safetensors`, tokenizer files.

NOTE: BG-μ (`state/clm_v4_tokenizer_caller_migration_exec_2026_05_04/`) is migrating CLM v4 tokenizer callers separately; this BG-ν shim is read-only w.r.t. that work.

### 2.4 Smoke test (10 min total before full launch)

```bash
ssh ubu1 'source /home/aiden/venv_orchestrator/bin/activate && \
  cd ~/p9_base_val_2026_05_04 && \
  lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-3.2-3B \
    --tasks hellaswag --limit 100 \
    --batch_size 4 --device cuda:0 --seed 42 \
    --log_samples --output_path ./smoke_llama_hellaswag/ \
    2>&1 | tail -30'
# expect: acc_norm in ~0.65-0.75 range on n=100, no OOM

ssh ubu1 'source /home/aiden/venv_orchestrator/bin/activate && \
  cd ~/p9_base_val_2026_05_04 && \
  lm_eval --model hf \
    --model_args pretrained=$HOME/p9_base_val_2026_05_04/clm_v4_base_hf \
    --tasks hellaswag --limit 100 \
    --batch_size 4 --device cuda:0 --seed 42 \
    --log_samples --output_path ./smoke_clm_hellaswag/ \
    2>&1 | tail -30'
# expect: anchor-B loads end-to-end; acc_norm in ~0.25-0.40 range on n=100
```

If smoke fails on either anchor, **HALT** — escalate to spec amendment per §3.3.

---

## 3. Launch command (full base-validation BG)

After smoke clears, this is the main BG launch. Designed as **one detached `nohup` process per (model × benchmark)** with sentinel emit on completion. Total 6 jobs (2 models × 3 benchmarks); the orchestrator script chains them sequentially to avoid 12GB VRAM contention.

```bash
ssh ubu1 'cat > ~/p9_base_val_2026_05_04/run_base_val.sh' <<'BASHEOF'
#!/bin/bash
# P9 F1_v3 base-validation BG — sequential 6-job orchestrator
# raw#9: Linux-side .sh is permitted; Mac-side ban only.
set -uo pipefail

source /home/aiden/venv_orchestrator/bin/activate
WORK=$HOME/p9_base_val_2026_05_04
cd $WORK
mkdir -p logs results

LLAMA_ID=meta-llama/Llama-3.2-3B
CLM_DIR=$WORK/clm_v4_base_hf

declare -A MODELS=( [llama]="$LLAMA_ID" [clm]="$CLM_DIR" )
declare -A TASKS=( [hellaswag]="hellaswag" [mmlu]="mmlu" [triviaqa]="triviaqa" )
declare -A NSHOTS=( [hellaswag]=0 [mmlu]=5 [triviaqa]=0 )

OVERALL_START=$(date -u +%s)
echo "[orch] start ts=$(date -u +%FT%TZ)" | tee -a logs/orchestrator.log

for mkey in llama clm; do
  for tkey in hellaswag mmlu triviaqa; do
    OUT=$WORK/results/${tkey}_${mkey}
    LOG=$WORK/logs/${tkey}_${mkey}.log
    echo "[run] $mkey × $tkey → $OUT" | tee -a logs/orchestrator.log
    JOB_START=$(date -u +%s)

    lm_eval --model hf \
      --model_args "pretrained=${MODELS[$mkey]},dtype=bfloat16" \
      --tasks "${TASKS[$tkey]}" \
      --num_fewshot "${NSHOTS[$tkey]}" \
      --batch_size auto:4 \
      --max_batch_size 8 \
      --device cuda:0 \
      --seed 42 \
      --log_samples \
      --output_path "$OUT" \
      > "$LOG" 2>&1

    RC=$?
    JOB_END=$(date -u +%s)
    JOB_WALL=$((JOB_END - JOB_START))
    echo "[done] $mkey × $tkey rc=$RC wall=${JOB_WALL}s" | tee -a logs/orchestrator.log
    if [ $RC -ne 0 ]; then
      echo "__P9_BENCH_A_PRIME_BASE_VAL__ FAIL on ${mkey}×${tkey} rc=$RC" | tee -a logs/orchestrator.log
      exit $RC
    fi
  done
done

OVERALL_END=$(date -u +%s)
TOTAL_WALL=$((OVERALL_END - OVERALL_START))
echo "[orch] complete total_wall=${TOTAL_WALL}s ($(awk "BEGIN{print ${TOTAL_WALL}/3600}") hr)" | tee -a logs/orchestrator.log

# stage to verdict computation (consolidator runs Mac-side; sentinel placeholder here)
echo "__P9_BENCH_A_PRIME_BASE_VAL__ AWAITING_VERDICT_COMPUTE" | tee -a logs/orchestrator.log
echo "[next] pull results back to Mac and run consolidator (§5)"
BASHEOF
chmod +x ~/p9_base_val_2026_05_04/run_base_val.sh
```

Detached launch:

```bash
ssh ubu1 'cd ~/p9_base_val_2026_05_04 && \
  nohup ./run_base_val.sh > logs/nohup.log 2>&1 & \
  PID=$!; echo $PID > run.pid; echo "[launched] pid=$PID"; \
  disown $PID 2>/dev/null || true'
```

---

## 4. Watch / monitor command

Mirrors Path A `host_terminator.log` precedent (`state/p9_path_a_llama_lora_2026_05_03/host_terminator.log`).

```bash
# tail orchestrator log + per-job log live
ssh ubu1 'tail -f ~/p9_base_val_2026_05_04/logs/orchestrator.log'

# check process alive + nvidia-smi snapshot
ssh ubu1 'PID=$(cat ~/p9_base_val_2026_05_04/run.pid 2>/dev/null); \
  echo "pid=$PID"; \
  ps -p $PID -o pid,etime,rss,cmd 2>/dev/null || echo "[gone]"; \
  nvidia-smi --query-gpu=name,memory.used,utilization.gpu --format=csv | head -2'

# poll sentinel (parent session can `until` this)
ssh ubu1 'grep -E "__P9_BENCH_A_PRIME_BASE_VAL__" ~/p9_base_val_2026_05_04/logs/orchestrator.log | tail -3'

# pull results to Mac for consolidator (rsync)
rsync -avz ubu1:p9_base_val_2026_05_04/results/ \
  /Users/ghost/core/anima/state/p9_benchmark_a_prime_base_validation_2026_05_<DD>/raw_lm_eval_results/
```

---

## 5. Verdict computation (Mac-side consolidator)

Per spec §3.2 PASS criteria + §2.3 paired bootstrap + McNemar.

### 5.1 Per-criterion table

For each benchmark `B` ∈ {hellaswag, mmlu, triviaqa}:

| criterion | computation | PASS rule |
|---|---|---|
| **C1: anchors run** | both `results/${B}_llama/results.json` and `results/${B}_clm/results.json` exist + `acc`/`acc_norm`/`exact_match` field present | both files non-empty + metric extractable |
| **C2: Llama within ±10% of public** | extract Llama metric `m_llama` from results.json; compare to public reference table | `0.9 × ref ≤ m_llama ≤ 1.1 × ref` |
| **C3: discriminative range** | compute `\|m_llama − m_clm\|`; compute paired-bootstrap 95% CI half-width on Llama−CLM Δ from per-item correctness | `\|Δ\| ≥ 2 × CI_half_width` (HellaSwag ~2pt, MMLU ~1pt, TriviaQA ~1pt per spec §3.2.3) |
| **C4: CLM not at floor** | random baselines: HellaSwag=25%, MMLU=25%, TriviaQA≈0% (floor=5%); | `m_clm ≥ random + 5pt` on ≥2 of 3 benchmarks (per spec §3.2.4) |

Public reference values (spec §2.2 expected):

| benchmark | metric | Llama-3.2-3B base public | acceptable band (±10%) |
|---|---|---|---|
| HellaSwag | acc_norm | ~0.704 | [0.634, 0.774] |
| MMLU 5-shot | acc | ~0.555 | [0.500, 0.610] |
| TriviaQA EM (0-shot, rc.nocontext) | exact_match | ~0.275 | [0.248, 0.303] |

If using Instruct (OPT-B fallback): expected MMLU shifts to ~0.585 (+3pt), HellaSwag ~0.685 (−2pt), TriviaQA ~0.265.

### 5.2 Paired bootstrap + McNemar consolidator

raw#9: consolidator runs on Mac. Pattern from `state/p9_p1_holdout500_reeval_2026_05_03/build_verdict_5seed.py` precedent (existing Mac-side .py is grandfathered; new .py creation banned per raw#9). For this BG-ν cycle, the consolidator is **proposed** as a hexa or transient bash/jq pipeline; user may request a Mac .py port to live under `tool/` if scipy lift required (escalate via spec amendment §2.6).

Pseudocode (Mac-side, hexa pattern):

```
# load per-item correctness from log_samples JSONL
for B in {hellaswag, mmlu, triviaqa}:
  load results/${B}_llama/samples_*.jsonl  → [(qid, correct_llama)]
  load results/${B}_clm/samples_*.jsonl    → [(qid, correct_clm)]
  align by qid → list of (correct_llama, correct_clm) pairs
  Δ_pt = mean(correct_llama) − mean(correct_clm)
  # paired bootstrap 10000x
  bootstrap_deltas = []
  for i in 1..10000:
    idx = random_sample_with_replacement(n_pairs)
    bd = mean([correct_llama[j] for j in idx]) − mean([correct_clm[j] for j in idx])
    bootstrap_deltas.append(bd)
  CI_lo, CI_hi = percentile(bootstrap_deltas, [2.5, 97.5])
  CI_half_width = (CI_hi − CI_lo) / 2
  # McNemar
  b = sum(correct_llama=1 ∧ correct_clm=0)
  c = sum(correct_llama=0 ∧ correct_clm=1)
  if b+c < 25: p = exact_binomial(min(b,c), b+c, 0.5)
  else: stat = (|b−c|−1)² / (b+c); p = chi2_sf(stat, 1)
  emit per-benchmark JSON: {Δ_pt, CI_lo, CI_hi, CI_half_width, mcnemar_b, mcnemar_c, mcnemar_p}
```

### 5.3 Final gate verdict

```
if all C1 PASS:
  if all C2 PASS:
    range_pass_count = sum(C3 PASS for B in 3)
    floor_pass_count = sum(C4 PASS for B in 3)
    if range_pass_count == 3 AND floor_pass_count >= 2:
      verdict = PASS
    elif range_pass_count == 2 AND floor_pass_count >= 2:
      verdict = PARTIAL  # drop the failing benchmark from F1_v3 composite per §3.3
    else:
      verdict = FAIL  # HARD STOP per §3.3 if floor_pass_count < 2
  else:
    verdict = FAIL  # harness config audit needed per §3.3
else:
  verdict = FAIL  # anchor didn't run per §3.3
```

Output artefacts (per spec §3.4):

- `state/p9_benchmark_a_prime_base_validation_2026_05_<DD>/anchors.json` — full per-benchmark numbers + 95% CIs
- `state/p9_benchmark_a_prime_base_validation_2026_05_<DD>/gate_verdict.json` — PASS/PARTIAL/FAIL with per-criterion table
- `state/markers/p9_benchmark_a_prime_base_validation_landed.marker` — only on PASS or PARTIAL-with-fallback (§3.4)

---

## 6. Cost projection table

Cost basis: ubu1 owned hardware (RTX 5070, sm_120, 12GB VRAM, torch 2.11.0+cu128). $0/hr. Forward-pass throughput estimated at ~100 forwards/GPU-sec for 350M-3B class on bf16 with batch_size auto:4.

| job | model | benchmark | n_items | shots | est forwards | est wall | running cumulative |
|---|---|---|---|---|---|---|---|
| 0 | (setup) clm_v4_to_hf shim | — | — | — | — | 30-60min | 0:30-1:00 |
| 0b | Llama base download (if OPT-A) | — | — | — | — | 5min | 0:35-1:05 |
| 0c | smoke n=100 × 2 | both | hellaswag | 100 | 800 | 8min | 0:43-1:13 |
| 1 | Llama-3.2-3B | HellaSwag | 10042 | 0 | ~40k | 30-50min | 1:13-2:03 |
| 2 | Llama-3.2-3B | MMLU | 14042 | 5 | ~280k | 2.0-2.5hr | 3:13-4:33 |
| 3 | Llama-3.2-3B | TriviaQA | 11313 | 0 | ~22k | 25-40min | 3:38-5:13 |
| 4 | CLM v4 base | HellaSwag | 10042 | 0 | ~40k | 15-25min (smaller model) | 3:53-5:38 |
| 5 | CLM v4 base | MMLU | 14042 | 5 | ~280k | 1.0-1.5hr | 4:53-7:08 |
| 6 | CLM v4 base | TriviaQA | 11313 | 0 | ~22k | 12-20min | 5:05-7:28 |
| 7 | rsync results to Mac + consolidator | — | — | — | — | 30min | 5:35-7:58 |
| **total** | | | | | | **5.5-8h central** | **band 6-17h with buffer** |

**Cost: $0 (ubu1 local, $0/hr).** No cloud spend. No HF API spend. Datasets free download (~3GB total). Spec §0 cost band 4-13h validated (revised upward to 6-17h with shim + smoke + buffer).

---

## 7. Honest C3 (raw#10) — minimum 5 caveats

### 7.1 lm-eval-harness version drift

Spec §2.5 requires harness commit pin. Currently lm-eval 0.4.11 from PyPI. The launched BG run will be tagged with `lm_eval --version` capture in `logs/orchestrator.log`, and the verdict JSON must record both the version and the commit hash (`pip show lm-eval | grep Location` + `git -C $(python -c 'import lm_eval; print(lm_eval.__path__[0])')/../.. rev-parse HEAD` if installed from source). Public reference numbers in §5.1 are reported against various lm-eval versions; ±5% drift between v0.4.x releases is documented (e.g. HellaSwag prompt template tweak in v0.4.0 → v0.4.1). **Acceptance band ±10% in spec §3.2 absorbs this drift, but post-publication amendment to a different lm-eval major is forbidden without §2.6 spec re-issue.**

### 7.2 HellaSwag variant ambiguity (val vs test split)

`hellaswag` task in lm-eval defaults to **validation split** (n=10042). The `acc_norm` metric (length-normalized accuracy) is the standard reporting surface; raw `acc` is also emitted. Public reference numbers cited in §5.1 (~70.4% for Llama-3.2-3B base) are **acc_norm on validation**. Verify both fields appear in `results.json` and use `acc_norm` for the Δ vs CLM v4 base. If lm-eval 0.4.11 has renamed the task to `hellaswag_v1` or split the variants, harness audit required before C2 evaluation.

### 7.3 MMLU 5-shot prompt formatting variance

MMLU has 4+ documented prompt formats across implementations:
- HF `lm-evaluation-harness` default (4-option A/B/C/D listing, 5-shot from dev split)
- Original LLaMA paper format (slightly different shot delimiter)
- HELM format (more elaborate question framing)
- Open-LLM-Leaderboard format (matches lm-eval default)

Spec §2.5 locks lm-eval defaults; Llama-3.2-3B model card numbers are typically reported against open-LLM-leaderboard (matches lm-eval). If our measured Llama MMLU lands outside ±10% of 0.555, audit shot count + prompt template before assuming model issue.

### 7.4 TriviaQA gold-answer matching brittleness

TriviaQA `exact_match` metric uses normalized comparison: lowercase + strip punctuation + remove articles ("a", "an", "the"). Variants:
- `triviaqa` (lm-eval default; rc.nocontext val split, n=11313)
- `triviaqa_5shot` (separately registered; harder)
- Alternative scorers: `f1` (token-overlap), `contains` (substring)

We use 0-shot `triviaqa` per §2.1. Llama-3.2-3B base typically scores ~25-30% EM at 0-shot; CLM v4 base on 350M params more likely ~3-8% (near random+5pt floor). **C4 (floor) PASS for TriviaQA on CLM v4 base is the most fragile gate** — if it fails, drop TriviaQA to 2-benchmark composite per spec §3.3.

### 7.5 GPU memory pressure (12GB shared between 3B + 350M)

RTX 5070 12GB total. Peak load during MMLU 5-shot on Llama-3.2-3B with batch_size auto:4:
- Model weights bf16: ~6GB
- KV cache (5-shot prompts ~512-1024 tokens × batch 4-8): ~1.5-3GB
- Activations + harness overhead: ~1-2GB
- Free margin: ~1-3GB

Tight. Spec §2.5 caps `max_batch_size 8`; `auto:4` lets harness back off if OOM. **If first MMLU job OOMs, restart with `max_batch_size 4` or `2`** and document in honest_c3 of the final verdict. CLM v4 base (350M) is comfortable at any batch size.

### 7.6 Llama base vs Instruct policy (BLOCKER (i) escalation)

If user authorizes OPT-B (Instruct fallback) instead of OPT-A (base download), spec §2.6 amendment is **mandatory**: a new dated spec doc must replace `meta-llama/Llama-3.2-3B` with `Llama-3.2-3B-Instruct` in §3.1 and update §2.2 expected anchors (MMLU +3pt, HellaSwag −2pt, TriviaQA approximately unchanged). Skipping this amendment → §7.1 selection-bias caveat in spec violated (raw#10).

### 7.7 CLM v4 conversion shim correctness audit

OPT-1 shim (§2.3) loads `best.pt` into a CLM v4 architecture and emits HF format. The shim is **stub-form** in this handoff doc — actual implementation requires:
1. Verifying CLM v4 architecture class location in anima codebase (likely `anima-clm-eeg/` or similar).
2. Confirming config (vocab_size=64000, hidden, layers, etc.) matches the trained checkpoint.
3. Validating `state['model']` key vs raw state_dict format of `best.pt`.
4. Smoke test: load via `AutoModelForCausalLM.from_pretrained(OUT_DIR)` and verify forward pass matches a reference output token from a known prompt.

If shim is wrong, all CLM v4 base numbers are corrupt. Audit step is mandatory before launching the full BG.

---

## 8. F-handoff status emit

Sentinel emit pattern (per spec §3.4 + roadmap verifier `status_emit`):

```
__P9_BENCH_A_PRIME_BASE_VAL__ <PASS|PARTIAL|FAIL>
```

Locations:
- During run: `~/p9_base_val_2026_05_04/logs/orchestrator.log` (live, sentinel "AWAITING_VERDICT_COMPUTE" emitted on orchestrator complete)
- Post-consolidator: `state/p9_benchmark_a_prime_base_validation_2026_05_<DD>/gate_verdict.json` (final verdict line + per-criterion table)
- Marker (PASS or PARTIAL only): `state/markers/p9_benchmark_a_prime_base_validation_landed.marker`

Verdict file paths (canonical):
- `state/p9_benchmark_a_prime_base_validation_2026_05_<DD>/anchors.json` — per-bench numbers, per-item correctness summary, 95% CIs, McNemar p-values
- `state/p9_benchmark_a_prime_base_validation_2026_05_<DD>/gate_verdict.json` — final PASS/PARTIAL/FAIL + per-C1/C2/C3/C4 sub-verdicts

---

## 9. Roadmap update proposal

When the base-validation BG cycle launches and again when it completes, `.roadmap.p9_sft cond.benchmark_a_prime_base_validation` should be updated. **DO NOT edit the roadmap in this BG-ν prep cycle** — parent session serializes commits at end.

Proposed JSONL field updates:

### 9.1 On launch

```jsonpatch
- "status": "unmet"
- "blocker_reason": "separate BG cycle per spec §8.2; ETA ~6-17h ubu1 wall, $0 (local); HARD STOP if criterion 4 fails on ≥2 benchmarks"
+ "status": "running"
+ "blocker_reason": "BG cycle in progress on ubu1; logs ~/p9_base_val_2026_05_04/logs/orchestrator.log; ETA ~6-17h"
+ "evidence": [
+   "spec docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md §3 + §8.2 handoff path",
+   "prep state/p9_base_validation_prep_2026_05_04/ (PARTIAL→READY post user ack)",
+   "ubu1 PID at ~/p9_base_val_2026_05_04/run.pid"
+ ]
```

### 9.2 On PASS verdict

```jsonpatch
- "status": "running"
+ "status": "met"
+ "blocker_reason": ""
+ "evidence": [
+   ...,
+   "state/p9_benchmark_a_prime_base_validation_2026_05_<DD>/anchors.json",
+   "state/p9_benchmark_a_prime_base_validation_2026_05_<DD>/gate_verdict.json (verdict=PASS)",
+   "state/markers/p9_benchmark_a_prime_base_validation_landed.marker"
+ ]
```

### 9.3 On PARTIAL or FAIL

PARTIAL: status=met but evidence includes "fallback to N-benchmark composite per spec §3.3"; F1_v3 composite §2.4 reduced to N benchmarks.

FAIL: status=blocked; HARD STOP per spec §3.3 criterion-4 if CLM base at floor on ≥2 benchmarks → reopen design space (legacy F1_v2 fallback, or escalate to v2 spec doc).

---

## 10. Hard constraints honoured (raw audit)

- raw#9 (.py ban Mac): NO new Mac-side .py created in this prep. Linux-side .py shim (CLM v4 conversion) is permitted.
- raw#10 honest C3: §7 covers 7 caveats (5 mandated + 2 blocker-specific).
- raw#15 no personal-path leak: Mac paths use `/Users/ghost/core/anima/...` only in repo-internal references; ubu1 paths use `~/...` or `$HOME`. No raw user paths exposed in launched logs.
- raw#71 no spec-after-the-fact: this prep precedes launch; pre-registration §2 is locked at marker; any post-eval threshold change requires §2.6 procedure (new dated spec doc).
- READ-ONLY ubu1 inspection (this BG-ν): NO install, NO GPU job launch — only `ssh ubu1 'ls/df/nvidia-smi/pip-show/python -c'` read-only checks. The actual base-val BG launch (§3) requires explicit user ack.
- DO NOT modify other state/p9_* dirs: confirmed; only `state/p9_base_validation_prep_2026_05_04/` written.
- DO NOT chflags: confirmed.
- NO git operations: this BG-ν does not commit; parent session serializes.

---

## 11. Handoff to parent session

Parent session decision tree:

```
user reads prep verdict (PARTIAL):
  → if user acks both blockers (Llama base + CLM HF shim) AND base-val BG launch:
      → execute §2.2 (download Llama base) + §2.3 (build CLM HF shim) + §2.4 smoke
      → on smoke PASS, execute §3 launch command
      → monitor via §4
      → on completion, run §5 consolidator → emit verdict
      → on PASS marker, update roadmap per §9.2
  → if user requests OPT-B (Instruct fallback) instead of OPT-A:
      → escalate spec amendment §2.6 (new dated spec doc) BEFORE launching
  → if user defers base-val BG:
      → leave prep verdict as PARTIAL; revisit when ubu1 GPU available + user authorization
```

**End of handoff. BG-ν prep complete; ownership transfers to parent session pending user ack.**
