# P9 Phase 2 Entry Runbook — 8 LHS Combo DDP Launch on RunPod 8×H100

- ts_utc: 2026-05-03
- agent: G5 (runbook only — no execution, no .py creation, no commit)
- spec_id: `p9_phase2_entry_runbook_2026_05_03`
- substrate: P9 Phase 1.6 sentinel SOFT gate clearance (F1 ≥ 0.05) IN FLIGHT on ubu1; this runbook prepares execution-ready scaffolding for the moment Phase 1.6 verdict lands GREEN
- gate: doc-only deliverable; Phase 2 EXEC requires explicit user OK AND Phase 1.6 SOFT PASS verification
- substrate spec: `state/p9_sft_spec_2026_05_02/{hyperparameter_grid,falsifiers_preregistered,cost_estimate,decision_matrix,risk_strategy,architecture,loss_design}.json`
- predecessor docs: `docs/p9_p1_6_redesign_2026_05_03.md`, `docs/p9_sft_data_alpha_redesign_2026_05_03.md`

---

## 0. TL;DR

| Item | Value |
|---|---|
| Phase | P9 Phase 2 (S3 strategy: 8-of-9 LHS sweep over LoRA-only S1) |
| Combos | 8 of 9 LHS samples; **lhs2 dropped** (rationale §3.0) |
| Topology | **Recommendation: 8-pod parallel** (1×H100 80GB each), NOT single 8-GPU DDP pod (rationale §4) |
| Cost target | **$288 spot / $516 secure** (24hr wall, 8 pods × $1.50/hr spot OR × $2.69/hr on-demand) |
| Per-combo wall | 8–12hr (50K examples × 3 epochs × LoRA bf16 on H100) |
| Pre-launch checklist | **9 items** (§1) — ALL must PASS before pod launch |
| Pareto selection | argmax `M_chat = (BLEU1 + φ★/41.86) / 2` s.t. F2 PASS — script spec §6 |
| Decision matrix | SUCCESS / PARTIAL / FAIL — §8 |
| Phase 1.6 dependency | F1 ≥ 0.05 (SOFT gate) MUST be observed BEFORE this runbook fires |

**Headline.** Phase 2 fires only after Phase 1.6 SOFT-gates F1 ≥ 0.05 (~50% probability per Phase 1.6 redesign §5.1). Once cleared, this runbook sweeps 8 LHS hyperparameter combos in parallel pods, each running 50K-step LoRA SFT on the v3 data composition with combo-specific (α, β, γ, δ). Winner is the combo maximizing chat capability `M_chat` subject to F2 φ★ preservation. Expected cost band: $288–$516, expected wall: 24hr (parallel) vs ~96hr (sequential).

---

## 1. Pre-launch checklist

ALL items must be confirmed PASS before any RunPod pod is provisioned. Failure of any single item = NO-GO.

| # | Item | Verification | Owner | Pass criterion |
|---:|---|---|---|---|
| 1 | Phase 1.6 sentinel verdict | Read `/tmp/p9_p1_6_sentinel_out/verdict.json` on ubu1 | ubu1 agent | F1 BLEU-1 ≥ 0.05 (SOFT gate) AND F2 φ★ ≥ 5.0 |
| 2 | Phase 1.6 φ★ delta | Same verdict.json + `phi_star_baseline_2026_05_02.json` | ubu1 agent | φ★ delta ≥ −10.0 from baseline 41.86 |
| 3 | v3 data manifest available | `/tmp/p9_p1_6_sft_data_50k_v3.jsonl` exists, 50K records, chat coverage = 100% | ubu1 agent | line count = 50000, chat fraction = 1.0 |
| 4 | Holdout-500 reused | `/tmp/sft_data_holdout_500.jsonl` checksum matches Phase 1, 1.5, 1.6 | ubu1 agent | sha256 match (avoids contamination across phases) |
| 5 | Base CLM HF mirror reachable | `huggingface-cli download anima-research/clm-v4-350m-base --include best.pt --revision main` test pull from a fresh RunPod pod template | RunPod test | download succeeds in < 5 min, sha256 matches ubu1 local |
| 6 | Phase 1.6 v3 data HF mirror | `huggingface-cli upload anima-research/p9-sft-data-v3 /tmp/p9_p1_6_sft_data_50k_v3.jsonl` from ubu1 first | ubu1 agent | upload succeeds; HF dataset card includes composition table from Phase 1.6 §3.1 |
| 7 | Savepoint storage plan | RunPod network volume OR HF Hub repo `anima-research/clm-v4-sft-2-c{0..7}` provisioned | user + ubu1 | 8 repos created OR 100GB network volume mounted (~12GB per combo × 8 = 96GB) |
| 8 | RunPod credit balance | `runpodctl get balance` (or web UI) | user | ≥ $600 (covers $516 secure worst case + 16% margin) |
| 9 | F2 ABORT mechanism armed | per-pod cron job polls every 5K steps; reads `phi_star_ema` from training log; if EMA < 10.0 → kill pod via `runpodctl pod stop <id>` | per-pod startup script | dry-run on Phase 1.6 sentinel log validates polling logic |

**If any item fails**: STOP. Do not provision pods. Diagnose root cause and re-run check. Particularly:
- Item 1 failure (Phase 1.6 SOFT gate miss): trigger Phase 1.7 redesign per `p9_p1_6_redesign_2026_05_03.md` §6 decision matrix. Phase 2 NO-GO until SOFT gate clears.
- Item 5 failure (HF mirror unreachable): check `huggingface_hub` token, repo visibility (public vs private), revision hash. Cold-HF download + 25min per fresh model is the canonical RunPod pattern (raw#19 memory note).
- Item 9 failure (ABORT polling broken): the F2 ABORT is the primary safety net. NO pod launches without verified ABORT logic.

---

## 2. RunPod 8×H100 SXM 80GB pod spec

### 2.1 Recommended pod template (per-pod, 8 pods total)

| Field | Value |
|---|---|
| GPU | 1 × H100 SXM 80GB |
| Provider | RunPod Community Cloud (spot priority) |
| Spot pricing target | $1.50/hr (community spot avg 2026-05) |
| On-demand fallback | $2.69/hr (RunPod secure cloud H100 SXM 80GB on-demand) |
| Container | `runpod/pytorch:2.4.0-py3.11-cuda12.4-devel-ubuntu22.04` |
| Disk | 100GB container volume (base CLM ~2GB + LoRA savepoints ~12GB + intermediate logs ~10GB + scratch ~76GB) |
| Network volume | OPTIONAL: 100GB shared volume mount at `/workspace/savepoints` for cross-pod savepoint persistence (cost +$0.07/GB-month ≈ $7/mo) |
| Region | US-East-1 priority (lowest community spot pricing); fallback EU-West-1 |
| Env | `HF_TOKEN`, `WANDB_API_KEY` (optional), `COMBO_ID` (lhs1/lhs3/...), `ALPHA`, `BETA`, `GAMMA`, `DELTA`, `BASE_MODEL_REPO`, `DATA_REPO` |
| Startup script | per-combo training script (§3) wrapped in resilience loop (`while true; do python train.py || sleep 60; done` for spot eviction recovery) |

### 2.2 Spot vs On-demand decision

- **Default: spot (community cloud)**. Cost $288 for 8 pods × 24hr × $1.50/hr.
- **Spot eviction risk**: RunPod community spot eviction rate ~5–15% per 24hr in US-East. Per-combo savepoint at step 5K, 13K, 25K, 50K (matches Phase 1.6 cadence) bounds re-work to ≤ 5K steps (~1hr) on eviction.
- **Fallback to on-demand**: if 3+ pods are evicted within first 6hr (signaling region-wide capacity pressure), switch remaining combos to secure cloud on-demand. Cost: $516 worst case if all 8 pods migrate.
- **No-go condition**: H100 SXM 80GB unavailable in both spot AND on-demand for > 72hr → defer Phase 2 OR migrate to A100 80GB (40% slower, ~$0.99/hr spot, would need wall budget revision to ~36hr).

### 2.3 Pod provisioning script (template)

```bash
# pseudocode — actual EXEC done from ubu1 or runpodctl wrapper
for combo_id in lhs1 lhs3 lhs4 lhs5 lhs6 lhs7 lhs8 lhs9; do
  read alpha beta gamma delta < <(jq -r ".lhs_samples_explicit[] | select(.id==\"$combo_id\") | \"\(.alpha) \(.beta) \(.gamma) \(.delta)\"" \
    state/p9_sft_spec_2026_05_02/hyperparameter_grid.json)
  runpodctl pod create \
    --gpu-type "H100 SXM 80GB" \
    --image "runpod/pytorch:2.4.0-py3.11-cuda12.4-devel-ubuntu22.04" \
    --disk-size 100 \
    --community-spot \
    --env HF_TOKEN="$HF_TOKEN" \
    --env COMBO_ID="$combo_id" \
    --env ALPHA="$alpha" --env BETA="$beta" --env GAMMA="$gamma" --env DELTA="$delta" \
    --env BASE_MODEL_REPO="anima-research/clm-v4-350m-base" \
    --env DATA_REPO="anima-research/p9-sft-data-v3" \
    --startup-cmd "/workspace/p9_phase2_train.sh"
done
```

---

## 3. Per-combo training script template

### 3.0 8-combo selection — drop lhs2 rationale

The 9 LHS samples are listed in `hyperparameter_grid.json:lhs_samples_explicit`. Phase 2 runs 8; the dropped combo is **lhs2** (α=2.0, β=0.1, γ=0.5, δ=0.5).

Drop rationale (in priority order):
1. **γ=0.5 is highest in the grid**, but γ (BOLD MSE) is **forced to 0** in Phase 1.6 v3 (BOLD target blocked per Phase 1.6 §0 — measured BOLD bottleneck). With γ effectively masked, lhs2's only distinguishing axis vs lhs9 (α=1.0, β=0.1, γ=0.3, δ=0.5) is α=2.0 vs 1.0 — a 1-axis perturbation already covered by lhs5 (α=2.0, β=0.5) and lhs7 (α=2.0, β=0.3).
2. **δ=0.5 is the lowest φ★ floor in the grid**. With Phase 1.5 measuring φ★ delta = −6.6 and Phase 1.6 expected to widen toward −9.0, lhs2 provides the weakest φ★ protection — and a high-α + low-δ combo is the worst case for F2 ABORT risk. Removing it preserves combo budget for safer α/δ pairs.
3. **lhs9 already covers β=0.1, δ=0.5 region** with α=1.0 (safer middle-α). lhs2 is redundant under the γ-masking constraint.

The 8 combos retained for Phase 2:

| pod | combo | α | β | γ (masked → 0) | δ | role |
|---:|---|---:|---:|---:|---:|---|
| 0 | lhs1 | 0.5 | 0.5 | 0.3 → 0 | 1.0 | low-α + high-β + mid-δ; tension-fit emphasis |
| 1 | lhs3 | 1.0 | 0.3 | 0.1 → 0 | 2.0 | mid-α + high-δ; max φ★ floor |
| 2 | lhs4 | 0.5 | 0.1 | 0.1 → 0 | 1.0 | low-α + low-β + mid-δ; chat-capacity floor |
| 3 | lhs5 | 2.0 | 0.5 | 0.1 → 0 | 2.0 | high-α + high-β + high-δ; max-pressure cell |
| 4 | lhs6 | 1.0 | 0.5 | 0.5 → 0 | 0.5 | mid-α + high-β + low-δ; tension+φ★ tradeoff |
| 5 | lhs7 | 2.0 | 0.3 | 0.3 → 0 | 1.0 | high-α + mid-β + mid-δ; chat-priority candidate |
| 6 | lhs8 | 0.5 | 0.3 | 0.5 → 0 | 2.0 | low-α + mid-β + high-δ; safety-emphasis |
| 7 | lhs9 | 1.0 | 0.1 | 0.3 → 0 | 0.5 | mid-α + low-β + low-δ; minimal-regularization baseline |

### 3.1 Training script (template extension of Phase 1.5 sentinel)

Base script: `/tmp/p9_p1_5_sentinel_train_50k.py` on ubu1 (Phase 1.5 sentinel). Phase 2 extension changes:

| Field | Phase 1.5 sentinel | **Phase 2 per-combo** |
|---|---|---|
| Base model | local `~/anima/checkpoints/clm_v4_350m/scale_350m/best.pt` | HF pull `anima-research/clm-v4-350m-base@best.pt` (cold-cache, ~25min one-time per pod) |
| Data | local `/tmp/p9_p1_5_sft_data_50k_v2.jsonl` | HF pull `anima-research/p9-sft-data-v3` (50K, ~5min) |
| Holdout | local `/tmp/sft_data_holdout_500.jsonl` | HF pull `anima-research/p9-sft-holdout-500@v1` |
| α | hard-coded warmup schedule (12.0 → 6.0) | env `$ALPHA` × {12, 6}-shaped warmup multiplier (Phase 1.6 §3.2: 0–3K=12α, 3K–7K=12α→6α lin, 7K–50K=6α). Note: combo α is the **steady-state multiplier** baseline, so e.g. lhs1 α=0.5 → warmup peak = 6.0, steady = 3.0 |
| β | 0.10 (Phase 1.6) | env `$BETA` (NOT the Phase 1.6 0.10) — combo β is THE β |
| γ | 0 (BOLD blocked) | hard-coded 0 (γ env ignored — γ axis masked) |
| δ | curriculum 0.5/0.5/1.0 (Phase 1.6) | env `$DELTA` × curriculum {1.0, 1.0, 2.0}-multiplier — so e.g. lhs1 δ=1.0 → curriculum 1.0/1.0/2.0; lhs5 δ=2.0 → 2.0/2.0/4.0 |
| LoRA r | 128 (Phase 1.6) | **128** (carry forward from Phase 1.6 — capacity scale-up validated) |
| LoRA α | 128 (ratio 1.0) | **128** (Phase 1.6 §4.4 stability bet preserved) |
| LoRA target_modules | q_proj, k_proj, v_proj, o_proj | **same** (attention-only, attention scope unchanged from Phase 1.6) |
| Steps | 50K | 50K × 3 epochs = **150K** (S3 spec from `cost_estimate.json`, 3 epochs gives the sweep more signal than Phase 1.6's 1-epoch sentinel) |
| Effective batch | 32 (4 × 8) | **32 (4 × 8)** unchanged; H100 80GB easily fits full batch with bf16 + LoRA |
| Optimizer | AdamW (b1=0.9, b2=0.95, wd=0.01) | unchanged |
| LR | 1e-4 cosine warmup 500 | unchanged |
| Save points | 5K, 13K, 25K, 50K | **5K, 13K, 25K, 50K, 100K, 150K** (6 savepoints across 3 epochs; HF push at each) |
| Holdout eval | end-of-training only | **every 25K steps** (6 mid-train F1 measurements per combo for ABORT sensitivity) |
| φ★ EMA poll | every 100 steps, EMA-smoothed | every 100 steps; **F2 ABORT trigger at EMA φ★ < 10.0** (per `risk_strategy.json` L5) |

### 3.2 Pseudocode skeleton (NOT a .py file — illustrative only per raw#9)

```
# /workspace/p9_phase2_train.sh on each RunPod pod
#!/bin/bash
set -e
huggingface-cli download $BASE_MODEL_REPO --include best.pt -d /workspace/base
huggingface-cli download $DATA_REPO -d /workspace/data
huggingface-cli download anima-research/p9-sft-holdout-500 -d /workspace/holdout

python -c "
from anima.training.p9_phase2 import run_combo
run_combo(
    combo_id=os.environ['COMBO_ID'],
    alpha=float(os.environ['ALPHA']),
    beta=float(os.environ['BETA']),
    gamma=0.0,  # masked
    delta=float(os.environ['DELTA']),
    base_ckpt='/workspace/base/best.pt',
    data_path='/workspace/data',
    holdout_path='/workspace/holdout',
    output_dir='/workspace/savepoints',
    hf_repo=f'anima-research/clm-v4-sft-2-{os.environ[\"COMBO_ID\"]}',
    epochs=3,
    save_steps=[5000, 13000, 25000, 50000, 100000, 150000],
    eval_steps=25000,
    f2_abort_phi_ema_threshold=10.0,
)
"
```

The `anima.training.p9_phase2.run_combo` function is to be authored on ubu1 (raw#9: no .py on Mac; new module lands on ubu1 first, then HF-mirrored or rsynced into the RunPod pod via the training repo install).

---

## 4. DDP single-pod vs 8-pod parallel — recommendation

### 4.1 Two topology options

| Option | Pods | GPUs/pod | Topology | Inter-combo coupling |
|---|---:|---:|---|---|
| **A: 8-pod parallel (RECOMMENDED)** | 8 | 1 | independent processes, no DDP | none (combos 100% isolated) |
| B: 1-pod 8-GPU DDP | 1 | 8 | 8 combos as 8 separate DDP groups within one pod (each combo uses 1 GPU; no actual DDP — just GPU partitioning) | none functionally; shared NVLink + host RAM + container disk |

Note: a TRUE 8-GPU DDP within combo (i.e. 1 combo × 8 GPUs DDP-trained) is rejected — LoRA on a 350M base does not benefit from 8-way DDP (per-GPU compute is tiny relative to all-reduce overhead; LoRA params ~38M reduce trivially). DDP would only help if doing full SFT on a much larger base.

### 4.2 8-pod parallel — pros & cons

**Pros:**
1. **True isolation**: spot eviction of one pod kills only that combo, not all 8. Critical for spot pricing where 5–15% per-24hr eviction is expected.
2. **Granular cost control**: kill failed combos early without disturbing winners. Per-pod F2 ABORT logic is straightforward.
3. **Region diversity hedge**: pods can spawn across US-East-1, US-West-2, EU-West-1 — capacity pressure in one region doesn't block all 8.
4. **No GPU contention**: each combo gets full H100 80GB bandwidth + memory. Phase 1.5 ubu1 RTX 5070 was 12GB-tight; H100 80GB has ample headroom (~10–15 GB used per LoRA combo, leaving room for larger eval batch sizes mid-train).
5. **Simpler logging**: per-combo stdout/stderr trivially separable; no DDP rank-aware logging needed.

**Cons:**
1. **Cold-HF download per pod**: 8× $1.50 + 8× 25min wallclock (200 GPU-min wasted on download). Mitigation: pre-warm an HF cache via shared network volume mounted read-only across pods (saves 7/8 of the cost ≈ $10).
2. **8 separate billing meters**: minor accounting overhead.
3. **No shared evaluation cache**: each combo re-encodes the holdout-500 prompts (small cost, ~2min per combo).

### 4.3 1-pod 8-GPU DDP — pros & cons

**Pros:**
1. **Single billing meter**, single SSH endpoint, simpler logging.
2. **Shared HF cache**: base CLM downloaded once, read by all 8 processes (saves 7× $1.50 + 7× 25min).
3. **Network volume not needed**: container disk shared across all 8 procs.

**Cons:**
1. **Single point of failure**: pod eviction kills ALL 8 combos. Spot eviction probability over 24hr ≈ 10% per pod → 1-pod spot has 10% chance of full-Phase-2 wipe (acceptable for $288 worst case but bad UX).
2. **8× H100 SXM 80GB pods are scarcer than 1× H100**: queue time can be hours in community spot, potentially days in some regions. Mitigation: use H100 PCIe 80GB instead, but PCIe is ~15% slower than SXM.
3. **Inter-process contention**: 8 processes share host RAM (typically 1024GB on 8×H100 nodes, plenty), shared NVMe (a hot bottleneck if savepoint writes overlap; mitigation: stagger savepoint cadence by combo_id).
4. **Cost: 8×H100 SXM 80GB on-demand ≈ $25–28/hr** (RunPod secure cloud); spot ≈ $14–16/hr. 24hr wall = $336–672. Comparable to 8-pod parallel $288–516 but with worse failure mode.
5. **F2 ABORT complexity**: killing one combo's process while keeping the pod alive for others requires per-process supervision (systemd or supervisord); operationally fragile.

### 4.4 Recommendation: **8-pod parallel**

Decision: **Option A (8-pod parallel)**. Primary drivers:
- Fault isolation under spot eviction is worth the $10 cold-HF download premium.
- 1×H100 pods are widely available; 8×H100 pods can have multi-hour queue waits.
- Per-combo F2 ABORT is operationally clean (1 pod = 1 combo = 1 abort signal).
- Cost difference is < 5% in the realistic case (1-pod actually slightly higher due to 8×H100 spot premium per-GPU-hr).

**Reversal trigger**: if community spot prices for 1×H100 SXM 80GB rise > $2.00/hr at launch time (rare but possible during AI conference season), reconsider 1-pod 8-GPU on-demand at $25/hr if it provisions immediately.

---

## 5. Per-combo savepoint + HF push

### 5.1 Savepoint cadence

Per combo, 6 savepoints across 150K steps (3 epochs × 50K):
- step 5,000 (early CE descent inflection — Phase 1.5 anchor)
- step 13,000 (Phase 1.5 CE plateau probe)
- step 25,000 (mid-epoch-1)
- step 50,000 (epoch-1 end; matches Phase 1, 1.5, 1.6 final-step for direct comparison)
- step 100,000 (epoch-2 end)
- step 150,000 (epoch-3 end; final)

Each savepoint contains: LoRA adapter weights, optimizer state, RNG state, `phi_star_ema` value at savepoint, `loss_log_compact` (tail 5K steps), `holdout_eval` (if eval step coincides).

### 5.2 HF push naming

HF org: `anima-research` (per `p9_sft_p0_hf_org_setup_landed_2026_05_03.ai.md`).

Per-combo repo: `anima-research/clm-v4-sft-2-c{0..7}` (c0=lhs1, c1=lhs3, c2=lhs4, c3=lhs5, c4=lhs6, c5=lhs7, c6=lhs8, c7=lhs9).

Per-savepoint revision tags:
- `step-5k`, `step-13k`, `step-25k`, `step-50k`, `step-100k`, `step-150k`
- `stage2` alias → final step for the combo (typically `step-150k`, but if F2 ABORT triggers at e.g. step-87k, the last clean savepoint becomes `stage2`)

Aggregate winner repo (post-Pareto): `anima-research/clm-v4-sft-2-stage2-winner` with `combo_id` field in repo card pointing to source combo.

### 5.3 Push timing

To minimize HF rate-limit and bandwidth cost:
- Push savepoints 5K, 13K, 25K immediately (~50–80MB LoRA + optim state; small).
- Push savepoints 50K, 100K, 150K with optim state stripped (LoRA-only; ~20MB) to reduce upload volume; full optim state archived to RunPod network volume as fallback resume point.
- Async push: training continues during upload (background `huggingface-cli upload` process).

---

## 6. Pareto selection script spec

Script lives at `state/p9_sft_spec_2026_05_02/pareto_select_spec.json` (data spec; the script implementation is .py and lands on ubu1 per raw#9, NOT in this Mac docs run).

### 6.1 Spec

```
schema: anima/state/p9_sft_spec/pareto_select/1
inputs:
  - per-combo verdict file: state/p9_phase2_2026_05_XX/c{0..7}_verdict.json
    fields: combo_id, alpha, beta, gamma, delta, F1_BLEU1, F2_phi_star, F3_tens_mse, F4_bold_pearson, training_steps_completed, abort_reason
selection_criteria_primary: M_chat = (F1_BLEU1 + F2_phi_star / 41.86) / 2
constraint: F2_phi_star >= 5.0  (else combo excluded)
tie_break:
  1. F1_BLEU1 descending
  2. φ★ delta ascending (smaller drop = better)
  3. F3_tens_mse ascending (lower = better, soft signal)
  4. combo_id ascending (deterministic)
output:
  - winner: combo_id of argmax M_chat among F2-PASS combos
  - runners_up: top-3 by M_chat
  - excluded: list of combos with F2 FAIL or training abort
  - score_table: full sorted M_chat table
verdict_file: state/p9_phase2_2026_05_XX/winner_verdict.json
```

### 6.2 Worked example

Hypothetical post-Phase-2 verdict (illustrative):

| combo | F1 BLEU1 | F2 φ★ | F2 PASS? | F1+φ★/41.86 | M_chat | Status |
|---|---:|---:|---:|---:|---:|---|
| c0 (lhs1) | 0.082 | 38.1 | YES | 0.082+0.910 | 0.496 | OK |
| c1 (lhs3) | 0.061 | 41.0 | YES | 0.061+0.980 | 0.520 | OK |
| c2 (lhs4) | 0.045 | 39.5 | YES | 0.045+0.943 | 0.494 | OK |
| c3 (lhs5) | 0.094 | 4.2 | **NO** | excluded | excluded | F2_FAIL |
| c4 (lhs6) | 0.071 | 36.8 | YES | 0.071+0.879 | 0.475 | OK |
| c5 (lhs7) | **0.118** | 32.4 | YES | 0.118+0.774 | **0.446** | OK |
| c6 (lhs8) | 0.058 | 40.5 | YES | 0.058+0.967 | 0.513 | OK |
| c7 (lhs9) | 0.067 | 39.2 | YES | 0.067+0.936 | 0.502 | OK |

**Winner: c1 (lhs3)** with M_chat = 0.520 (despite c5 having highest F1, its φ★ erosion drags M_chat below). c5 + c0 + c7 are runners-up with within-5% M_chat.

This worked example highlights the Pareto tradeoff: **chat-capability (F1) and φ★-preservation (F2) trade off**; M_chat aggregates them with equal weight. If user later prefers raw chat dominance, the score function is easily reweighted (e.g. M_chat_2 = 0.7·BLEU1 + 0.3·φ★/41.86).

---

## 7. Cost monitoring per-combo

### 7.1 Per-pod cost tracking

Per-pod billing logged to `state/p9_phase2_2026_05_XX/cost_log.jsonl` (append-only). Each entry:
```
{ts_utc, pod_id, combo_id, gpu_hours_consumed, hourly_rate, cumulative_usd, status}
```

Polling: every 1hr via `runpodctl get pod $POD_ID --format json | jq '.gpu_hours, .runtime_status'`. Cumulative cost computed client-side from gpu_hours × hourly_rate.

### 7.2 Per-combo cost ceiling

| Combo | Wall ceiling | Cost ceiling spot ($1.50/hr) | Cost ceiling on-demand ($2.69/hr) |
|---|---:|---:|---:|
| c0–c7 (each) | 24 hr | $36.00 | $64.56 |
| **Total Phase 2** | 24 hr (parallel) | **$288.00** | **$516.48** |

If a combo's cumulative cost exceeds $40 (spot) or $70 (on-demand) without producing a savepoint at step 150K, F2 ABORT (§9) AND cost ceiling triggers cascade kill of that pod.

### 7.3 Bonus accounting

- Cold-HF base CLM download: $1.50 × 8 pods = $12 (one-time)
- HF Hub bandwidth (savepoint pushes): 6 savepoints × ~50MB × 8 combos = 2.4GB upload, free per HF Hub tier
- HF Hub storage: 8 repos × 6 revisions × ~50MB ≈ 2.4GB persistent, free per HF tier
- RunPod network volume (optional shared HF cache): 100GB × $0.07/GB-month ≈ $0.50 for 24hr usage

**Grand total cost band: $288 + $13 = $301 spot / $516 + $13 = $529 on-demand.**

---

## 8. Result aggregation spec

### 8.1 Combo result table

After all 8 combos complete (or abort), aggregate `c{0..7}_verdict.json` into single `phase2_results.json`:

```
schema: anima/state/p9_phase2/results/1
phase2_run_id: p9_phase2_2026_05_XX
ts_utc_start: ...
ts_utc_end: ...
total_cost_usd: ...
total_wall_hours: ...
combos: [
  {combo_id, alpha, beta, gamma, delta, status, F1_BLEU1, F2_phi_star, F3_tens_mse, F4_bold_pearson,
   savepoints_pushed, hf_repo, training_steps_completed, abort_reason_if_any, M_chat, rank}
]
winner: { combo_id, M_chat, hf_repo, savepoint_revision }
runners_up: [...]
excluded: [...]
```

### 8.2 Phase 2 decision matrix (SUCCESS / PARTIAL / FAIL)

| Verdict | Trigger | Action |
|---|---|---|
| **SUCCESS** | Winner M_chat ≥ 0.55 AND F1 ≥ 0.132 (HARD gate) AND F2 ≥ 5.0 AND ≥ 6 of 8 combos completed (≥ 75% yield) | Declare P9 SUCCESS. Promote winner to `clm-v4-sft-2-stage2-winner`. Begin Phase 3 (deployment + downstream eval). |
| **PARTIAL** | Winner F1 ∈ [0.05, 0.132) (SOFT but not HARD) AND F2 ≥ 5.0 AND ≥ 4 of 8 combos completed | Declare P9 PARTIAL. Two paths: (a) ship winner as Phase 2 best-effort + plan Phase 1.7 (S2 full SFT) for HARD gate; (b) extend Phase 2 with 4 additional combos at higher α (variant grid) without restarting infra. |
| **FAIL_PHI** | ≥ 4 of 8 combos F2 FAIL (φ★ collapse) | Declare P9_FAIL_PHI. Per `falsifiers_preregistered.json:verdict_logic`, full retrain required. Revisit base CLM checkpoint OR reduce LoRA r back to 64. |
| **FAIL_CHAT** | All F2 PASS but no winner crosses F1 SOFT gate 0.05 | Declare P9_FAIL_CHAT. Escalate to S2 (full SFT) per `risk_strategy.json` strategies[1]. Cost step-up: $800–2000 for one S2 run. |
| **INFRA_FAIL** | ≥ 4 of 8 combos failed to complete training due to spot eviction / OOM / network errors (NOT F2 ABORT) | Re-run failed combos with on-demand pricing. Cost step-up: ~$100/combo additional. |

### 8.3 Reporting artifacts

After verdict declared:
- `state/p9_phase2_2026_05_XX/phase2_results.json`
- `state/p9_phase2_2026_05_XX/winner_verdict.json`
- `state/p9_phase2_2026_05_XX/cost_log.jsonl`
- `docs/p9_phase2_landed_2026_05_XX.ai.md` (closure doc with verdict + artifacts + honest c3)
- `state/markers/p9_phase2_landed.marker`

---

## 9. F2 ABORT mechanism per combo

### 9.1 Abort logic

Per pod, a sidecar process polls every 100 training steps:
1. Read latest `phi_star_ema` from training log file (`/workspace/savepoints/$COMBO_ID/loss_log_compact.jsonl` tail).
2. If `phi_star_ema < 10.0` (= 2× safety margin above F2 threshold 5.0, per `risk_strategy.json` L5):
   - Fire ABORT signal: `runpodctl pod stop $POD_ID`
   - Push last clean savepoint to HF with revision tag `aborted-step-$STEP_NUM`
   - Write `c{N}_verdict.json` with `status: F2_ABORT`, `abort_step: $STEP_NUM`, `abort_phi_ema: $VALUE`
3. If `phi_star_ema < 5.0` (HARD F2 floor): same as above but also tag savepoint `aborted-phi-collapse` for forensic review.

### 9.2 Recovery path on ABORT

- Single combo abort (1 of 8): no Phase 2-wide impact. Combo excluded from Pareto selection. Other 7 continue.
- Multi-combo abort (≥ 4 of 8): triggers Phase 2 verdict FAIL_PHI (§8.2). Full halt and diagnostic ablation.
- Per-combo retry: NOT performed automatically. Operator decision after Phase 2 verdict to retry specific combos with adjusted hyperparameters (e.g. raise δ or lower α for chronic F2-fail combos).

### 9.3 ABORT testing pre-launch

Before Phase 2 fires, dry-run the ABORT polling logic on Phase 1.6 sentinel's `loss_log_compact.jsonl`:
1. Spoof a synthetic log entry with `phi_star_ema: 8.5`.
2. Verify polling script detects, fires `runpodctl pod stop` (against a test pod), and writes verdict file.
3. Cleanup test pod.

This is checklist item #9 (§1).

---

## 10. Honest C3 (raw#91) — what is hypothetical

1. **Phase 1.6 SOFT gate clearance is unverified.** This runbook assumes Phase 1.6 sentinel (currently in flight on ubu1) clears F1 ≥ 0.05. Per Phase 1.6 §5.1, the probability is ~50%. If it misses, ALL Phase 2 cost ($288–516) is deferred until Phase 1.7 lands a higher F1.
2. **Per-combo wall estimate 8–12hr is extrapolated.** `cost_estimate.json` says 10.7hr for 50K examples × 3 epochs at H100 bf16 LoRA, throughput 8000 tok/s. Real H100 throughput on a 350M base + LoRA r=128 has not been measured by this project; first pod's first 1K steps must be monitored to validate. If actual throughput is 0.5× expected, wall doubles → cost doubles → re-evaluate.
3. **Spot eviction rate 5–15%/24hr is a regional + temporal estimate.** RunPod community spot eviction varies by region, GPU type, and global demand. AI conference seasons can spike to 30%+. Real eviction stats for 2026-05 in US-East-1 require Phase 2 launch to measure.
4. **8-pod vs 1-pod recommendation assumes spot pricing parity.** If 1×H100 spot rises to $2.20/hr but 8×H100 spot stays at $14/hr (= $1.75/hr per GPU), 1-pod becomes cost-favorable. Decision should be re-validated at launch time with live RunPod pricing.
5. **HF Hub free tier limits.** Phase 2 will create 8 model repos × 6 revisions = 48 model artifacts. HF free tier has model repo soft limits (~30 free private repos per user). May need HF Pro ($9/mo) for the duration. Not included in $288 cost target.
6. **γ=0 forced masking is not in the original 9-LHS spec.** `hyperparameter_grid.json` LHS samples have γ ∈ {0.1, 0.3, 0.5}. Phase 1.6 redesign forces γ=0 (BOLD blocked). This means the 8 surviving combos collapse from 4-D LHS to effective 3-D LHS sweep over (α, β, δ). The selection-coverage of the original 4-D space is partial; if measured BOLD becomes available later, a γ-only follow-up sweep would be needed to complete the design.
7. **lhs2 drop is reasoned, not measured.** §3.0 rationale is structural (γ-mask + δ=0.5 weakest φ★). No prior Phase 1.x evidence directly excludes lhs2. Alternative drop: lhs5 (high-α + high-β + high-δ = max-pressure cell) which might yield F2_FAIL anyway. Dropping lhs5 instead would preserve more α=2.0 coverage but lose the max-stress probe. Choice of lhs2 is operator judgment per the principles in `risk_strategy.json` (LOW phi_risk priority).
8. **Pareto M_chat = (BLEU1 + φ★/41.86) / 2 weights both axes equally.** The selection_criteria in `hyperparameter_grid.json:37` uses this exact formula, so this runbook adheres. But the formula is itself a design choice — a real chat product might prefer 0.7 weight on BLEU1; a safety-first deployment might prefer 0.3 weight on BLEU1. The `pareto_select_spec.json` script is parameterizable.
9. **F2 ABORT polling at every 100 steps assumes φ★ EMA computation cost is bounded.** `loss_design.json:phi_star_compute_cost` says ~30s per microbatch, evaluated every 100 steps. On H100 this should be ~3–5s per evaluation; if it slips to 30s+ (e.g. due to TRIBE forward overhead), ABORT polling latency grows and worst-case φ★-collapse-to-detection lag widens.
10. **No execution performed.** This runbook is doc-only. All cost / wall / verdict values become measured only after explicit user EXEC OK + Phase 1.6 SOFT PASS verification. Pre-launch checklist (§1) must complete with all 9 items GREEN before pod provisioning.

---

## 11. References

- Spec dir: `$ANIMA/state/p9_sft_spec_2026_05_02/{architecture,sft_data_format,loss_design,hyperparameter_grid,falsifiers_preregistered,cost_estimate,decision_matrix,risk_strategy}.json`
- Phase 1.6 redesign: `$ANIMA/docs/p9_p1_6_redesign_2026_05_03.md`
- Phase 1.5 sentinel script (script base): `/tmp/p9_p1_5_sentinel_train_50k.py` on ubu1
- Phase 1.5 sentinel verdict: `/tmp/p9_p1_5_sentinel_out/verdict.json` on ubu1
- Phase 1, 1.5, 1.6 holdout (reused unchanged): `/tmp/sft_data_holdout_500.jsonl` on ubu1
- HF org setup: `$ANIMA/docs/p9_sft_p0_hf_org_setup_landed_2026_05_03.ai.md`
- Phase 2 marker target (post-EXEC): `$ANIMA/state/markers/p9_phase2_landed.marker`
- Falsifiers preregistered (F1 HARD = 0.132, F2 ≥ 5.0 floor): `$ANIMA/state/p9_sft_spec_2026_05_02/falsifiers_preregistered.json`

---

**End of P9 Phase 2 entry runbook. EXEC requires:**
1. Explicit user OK
2. Phase 1.6 SOFT gate (F1 ≥ 0.05) verified PASS
3. All 9 pre-launch checklist items (§1) GREEN
