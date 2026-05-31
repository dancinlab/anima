"""H_878 — MITOSIS multi-chip array dispatch SW-simulation.

This is the VERDICT run for F-CLM-MITOSIS-ARRAY (CLM/P4_PRODUCTION_ROADMAP.md
@L2 MITOSIS, UNIVERSE H_878). It is a pure SW-SIMULATION of the deploy chip-fit
track: there is exactly ONE physical AKD1000 today (the rest is pi5/1-chip), so
the N-chip array is simulated in software.

The deploy vision (@L2) is `expert = chip`: a MITOSIS array of N AKD1000 chips,
where the MoE router dispatches each token to a chip and each chip emits
independently. H_852 already showed the *expert-count* scale axis; H_878 asks the
DEPLOY question instead:

    When the E sparse experts are PARTITIONED onto N disjoint chips and each chip
    emits independently, does the dispatch (1) LOAD-BALANCE across chips (no chip
    starves / saturates) and (2) does the gathered N-chip aggregate output stay
    COHERENT with the single-model reference (within tolerance)?

SW-sim construction (a_scale_honest_scope):
  * Train a single CLMArray (E experts, the landed sparse skeleton).
  * The SINGLE forward (all experts in one model) = the REFERENCE.
  * The N-CHIP forward partitions the E experts into N disjoint shards (chip c
    owns experts[shards[c]]). Each token is routed by the SAME router; its top-1
    expert determines its chip. Each chip runs ONLY its own experts, emits its
    own contribution, and a GATHER sums the per-chip emits back into one output.
  * Because the expert<->chip mapping is a disjoint partition of the SAME experts
    and the SAME router weights, the gathered aggregate is mathematically the
    single-model forward re-associated by chip. Coherence therefore tests the
    SW dispatch + gather contract (partition/scatter/gather correctness), and
    load-balance tests how the trained router spreads tokens across chips.

NOT measured: chip-to-chip DMA latency, silicon timing, real-chip int4 emit drift
(hardware follow-up). This is a CPU/Mac toy harness ($0); toy != scale (H_666).

PRE-REGISTERED, FROZEN BEFORE THE RUN (@L7, no post-hoc tampering):
  .verdicts/clm-mitosis-array-sim/F-CLM-MITOSIS-ARRAY_prereg.txt

Run:  python3 CLM/model/h878_chip_array_sim.py
Set H878_JSON / H878_TXT to persist outputs.
"""

from __future__ import annotations

import json
import math
import os
import sys
from typing import Dict, List

import torch
import torch.nn.functional as F

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from array_moe import build_array, AKD1000_NODE_BUDGET            # noqa: E402
from data import make_synthetic_corpus, make_batches, lane_tagged_stream  # noqa: E402

# ---- FROZEN pre-registered thresholds (@L7) ------------------------------- #
N_CHIPS_AXIS = [1, 2, 4, 8]   # 1 = single-chip degenerate baseline
N_EXPERTS = 8                 # fixed; partitioned evenly onto N chips
SEEDS = [42, 43, 44]
TRAIN_STEPS = 120
EVAL_BATCHES = 16
SEQ_LEN = 64
BATCH_SIZE = 16
LR = 3e-3

LOADBAL_RATIO_MAX = 4.0       # max/min per-chip dispatch ratio bound (N>=2)
COH_LOGIT_ATOL = 1e-4         # max abs logit diff array-vs-reference
COH_HAMMING_MAX = 0.0         # fraction of next-byte argmax mismatches (exact)
COH_CE_ATOL = 1e-4            # abs cross-entropy delta array-vs-reference

FROZEN = {
    "axis_n_chips": N_CHIPS_AXIS,
    "n_experts": N_EXPERTS,
    "d_model/L": "d64/L2 (toy)",
    "top_k": 2,
    "seeds": SEEDS,
    "train_steps": TRAIN_STEPS,
    "eval_batches": EVAL_BATCHES,
    "loadbal_ratio_max": LOADBAL_RATIO_MAX,
    "coh_logit_atol": COH_LOGIT_ATOL,
    "coh_hamming_max": COH_HAMMING_MAX,
    "coh_ce_atol": COH_CE_ATOL,
    "falsifier": ("F-CLM-MITOSIS-ARRAY: for every N in {2,4,8} -- no chip starves "
                  "AND max/min per-chip dispatch ratio <= loadbal_ratio_max AND "
                  "max|logit_array-logit_ref| <= coh_logit_atol AND argmax-hamming "
                  "<= coh_hamming_max AND |CE_array-CE_ref| <= coh_ce_atol"),
    "scope": ("SW-sim of @L2 deploy chip-fit track -- silicon NOT measured "
              "(1 AKD1000 today); a_scale_honest_scope"),
}


def _even_partition(n_experts: int, n_chips: int) -> List[List[int]]:
    """Partition expert indices [0..E) into n_chips disjoint contiguous shards.

    Each shard = the experts that physically live on one AKD1000 chip. As even
    as possible (first (E mod N) chips get one extra expert).
    """
    base = n_experts // n_chips
    rem = n_experts % n_chips
    shards: List[List[int]] = []
    idx = 0
    for c in range(n_chips):
        size = base + (1 if c < rem else 0)
        shards.append(list(range(idx, idx + size)))
        idx += size
    return shards


@torch.no_grad()
def _single_model_forward(model, x) -> Dict:
    """REFERENCE: the monolithic CLMArray forward (all experts in one model)."""
    out = model(x)
    return {"logits": out["logits"], "dispatch_counts": out["dispatch_counts"]}


@torch.no_grad()
def _chip_array_forward(model, x, shards: List[List[int]]) -> Dict:
    """SW-sim N-chip forward: partition experts onto chips, dispatch, gather.

    Replays the SparseMoEArray math (array_moe.SparseMoEArray.forward) but routes
    each token's contribution through the CHIP that owns its expert, accumulates
    per-chip emits, then GATHERS (sums) them. The gathered MoE output is fed
    through the SAME trunk/norm/readout as the reference, so any divergence is
    purely the partition/scatter/gather contract.

    Returns gathered logits + per-CHIP top-1 dispatch counts (load-balance).
    """
    moe = model.moe
    cfg = moe.cfg
    n_e = cfg.n_experts
    k = min(cfg.top_k, n_e)

    # shared front-end (identical to CLMArray.forward up to the MoE layer)
    h = model.embed(x).transpose(1, 2)
    h = model.embed_conv(h)
    for layer in model.trunk:
        h = layer(h)

    # router (shared weights) -> gate mask, exactly as SparseMoEArray.forward
    logits_r = moe.router(h)                       # (B, n_e, T)
    probs = F.softmax(logits_r, dim=1)
    topv, topi = probs.topk(k, dim=1)
    gate = topv / (topv.sum(dim=1, keepdim=True) + 1e-9)
    mask = torch.zeros_like(probs).scatter_(1, topi, gate)   # (B, n_e, T)

    # expert -> chip lookup
    expert2chip = torch.empty(n_e, dtype=torch.long)
    for c, sh in enumerate(shards):
        for e in sh:
            expert2chip[e] = c
    n_chips = len(shards)

    # per-CHIP emit: each chip runs ONLY its own experts, emits its masked sum.
    B, C, T = h.shape
    gathered = torch.zeros(B, C, T)
    for c, sh in enumerate(shards):
        chip_emit = torch.zeros(B, C, T)
        for e in sh:
            chip_emit = chip_emit + mask[:, e:e + 1, :] * moe.experts[e](h)
        gathered = gathered + chip_emit            # GATHER (sum across chips)

    # finish with the SAME tail as CLMArray.forward
    y = model.norm_out(gathered)
    out_logits = model.readout(y)

    # per-CHIP top-1 dispatch counts (load-balance) = sum of expert counts on chip
    top1 = probs.argmax(dim=1)                     # (B, T)
    expert_counts = torch.bincount(top1.reshape(-1), minlength=n_e).float()
    chip_counts = torch.zeros(n_chips)
    for e in range(n_e):
        chip_counts[int(expert2chip[e])] += expert_counts[e]
    return {"logits": out_logits, "chip_counts": chip_counts}


def _train(model, seed: int):
    torch.manual_seed(seed)
    web, reg = make_synthetic_corpus(n_bytes_per_lane=8192, seed=seed)
    stream, _lane = lane_tagged_stream(web, reg, block=64)
    batches = make_batches(stream, SEQ_LEN, BATCH_SIZE, TRAIN_STEPS, seed=seed)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    model.train()
    for x, y in batches:
        opt.zero_grad()
        out = model(x, y)
        out["loss"].backward()
        opt.step()
    return stream


def _measure(n_chips: int, seed: int) -> Dict:
    torch.manual_seed(seed)
    model = build_array(n_experts=N_EXPERTS)
    stream = _train(model, seed)
    model.eval()
    shards = _even_partition(N_EXPERTS, n_chips)

    eval_batches = make_batches(stream, SEQ_LEN, BATCH_SIZE, EVAL_BATCHES,
                                seed=seed + 999)

    chip_counts_acc = torch.zeros(n_chips)
    max_logit_diff = 0.0
    n_argmax = 0
    n_argmax_mismatch = 0
    ce_ref_sum = 0.0
    ce_arr_sum = 0.0
    n_ce = 0
    with torch.no_grad():
        for x, y in eval_batches:
            ref = _single_model_forward(model, x)
            arr = _chip_array_forward(model, x, shards)

            # (B) coherence: logit abs diff
            d = float((arr["logits"] - ref["logits"]).abs().max())
            if d > max_logit_diff:
                max_logit_diff = d

            # (B) coherence: next-byte argmax (hard emit) hamming
            am_ref = ref["logits"].argmax(dim=1)    # (B, T)
            am_arr = arr["logits"].argmax(dim=1)
            n_argmax += am_ref.numel()
            n_argmax_mismatch += int((am_ref != am_arr).sum())

            # (B) coherence: cross-entropy delta
            V = ref["logits"].shape[1]
            ce_ref = float(F.cross_entropy(
                ref["logits"].transpose(1, 2).reshape(-1, V), y.reshape(-1)))
            ce_arr = float(F.cross_entropy(
                arr["logits"].transpose(1, 2).reshape(-1, V), y.reshape(-1)))
            ce_ref_sum += ce_ref
            ce_arr_sum += ce_arr
            n_ce += 1

            # (A) load-balance: per-chip dispatch counts
            chip_counts_acc = chip_counts_acc + arr["chip_counts"]

    cc = chip_counts_acc
    min_c = float(cc.min())
    max_c = float(cc.max())
    no_starve = bool(min_c > 0)
    ratio = (max_c / min_c) if min_c > 0 else float("inf")
    hamming = n_argmax_mismatch / max(1, n_argmax)
    ce_delta = abs((ce_arr_sum - ce_ref_sum) / max(1, n_ce))

    return {
        "n_chips": n_chips, "seed": seed,
        "shards": shards,
        "chip_counts": [int(v) for v in cc.tolist()],
        "no_starve": no_starve,
        "loadbal_ratio": round(ratio, 5) if math.isfinite(ratio) else None,
        "max_logit_diff": round(max_logit_diff, 9),
        "hamming_mismatch": round(hamming, 9),
        "ce_delta": round(ce_delta, 9),
        "expert_params": model.moe.expert_param_count(),
        "chip_fit": model.expert_chip_fit(),
    }


def run() -> Dict:
    per_N: Dict[int, Dict] = {}
    rows: List[Dict] = []
    for N in N_CHIPS_AXIS:
        seed_rows = [_measure(N, s) for s in SEEDS]
        rows.extend(seed_rows)
        ratios = [r["loadbal_ratio"] for r in seed_rows
                  if r["loadbal_ratio"] is not None]
        per_N[N] = {
            "mean_loadbal_ratio": (round(sum(ratios) / len(ratios), 5)
                                   if ratios else None),
            "max_loadbal_ratio": (round(max(ratios), 5) if ratios else None),
            "all_no_starve": all(r["no_starve"] for r in seed_rows),
            "max_logit_diff": round(max(r["max_logit_diff"] for r in seed_rows), 9),
            "max_hamming": round(max(r["hamming_mismatch"] for r in seed_rows), 9),
            "max_ce_delta": round(max(r["ce_delta"] for r in seed_rows), 9),
            "chip_fit": all(r["chip_fit"] for r in seed_rows),
        }

    # --- frozen falsifier evaluation (NO threshold tampering) -------------- #
    # gate over multi-chip configs N in {2,4,8}; N=1 is the degenerate baseline.
    multi = [N for N in N_CHIPS_AXIS if N >= 2]
    loadbal_ok = all(
        per_N[N]["all_no_starve"]
        and per_N[N]["max_loadbal_ratio"] is not None
        and per_N[N]["max_loadbal_ratio"] <= LOADBAL_RATIO_MAX
        for N in multi)
    coh_logit_ok = all(per_N[N]["max_logit_diff"] <= COH_LOGIT_ATOL for N in multi)
    coh_hamming_ok = all(per_N[N]["max_hamming"] <= COH_HAMMING_MAX for N in multi)
    coh_ce_ok = all(per_N[N]["max_ce_delta"] <= COH_CE_ATOL for N in multi)
    all_chip_fit = all(per_N[N]["chip_fit"] for N in N_CHIPS_AXIS)
    passed = bool(loadbal_ok and coh_logit_ok and coh_hamming_ok and coh_ce_ok)

    return {
        "frozen": FROZEN,
        "per_N": {str(N): per_N[N] for N in N_CHIPS_AXIS},
        "per_run": rows,
        "loadbal_ok": loadbal_ok,
        "coherence_logit_ok": coh_logit_ok,
        "coherence_hamming_ok": coh_hamming_ok,
        "coherence_ce_ok": coh_ce_ok,
        "all_chip_fit": all_chip_fit,
        "verdict": "PASS" if passed else "FAIL",
        "verdict_tier": ("\U0001f7e2 SUPPORTED-NUMERICAL" if passed
                         else "\U0001f534 CLOSED-NEGATIVE"),
        "akd1000_budget": AKD1000_NODE_BUDGET,
        "scale_scope": FROZEN["scope"],
        "torch": torch.__version__,
    }


def _fmt_txt(res: Dict) -> str:
    L = []
    L.append("F-CLM-MITOSIS-ARRAY -- N-chip array dispatch SW-simulation")
    L.append("=" * 68)
    L.append("FROZEN (pre-run, @L7 no tampering):")
    for k, v in res["frozen"].items():
        L.append(f"  {k} = {v}")
    L.append("")
    L.append(f"{'N':>3} {'loadbal_ratio':>14} {'no_starve':>10} "
             f"{'max_logit_d':>13} {'hamming':>10} {'ce_delta':>12} {'chip_fit':>9}")
    for N in N_CHIPS_AXIS:
        d = res["per_N"][str(N)]
        lr = d["max_loadbal_ratio"]
        lr_s = f"{lr:.4f}" if lr is not None else "n/a(N=1)"
        L.append(f"{N:>3} {lr_s:>14} {str(d['all_no_starve']):>10} "
                 f"{d['max_logit_diff']:>13.2e} {d['max_hamming']:>10.4f} "
                 f"{d['max_ce_delta']:>12.2e} {str(d['chip_fit']):>9}")
    L.append("")
    L.append(f"load-balance OK (N>=2, ratio<= {LOADBAL_RATIO_MAX}, no starve): "
             f"{res['loadbal_ok']}")
    L.append(f"coherence logit OK (atol {COH_LOGIT_ATOL}): {res['coherence_logit_ok']}")
    L.append(f"coherence hamming OK (<= {COH_HAMMING_MAX}): {res['coherence_hamming_ok']}")
    L.append(f"coherence CE OK (atol {COH_CE_ATOL}): {res['coherence_ce_ok']}")
    L.append(f"all chips chip-fit: {res['all_chip_fit']}")
    L.append(f"scale scope       : {res['scale_scope']}")
    L.append("")
    L.append(f"VERDICT: {res['verdict']}  {res['verdict_tier']}")
    return "\n".join(L) + "\n"


def main() -> None:
    res = run()
    txt = _fmt_txt(res)
    print(txt, flush=True)
    tdest = os.environ.get("H878_TXT")
    if tdest:
        with open(tdest, "w") as f:
            f.write(txt)
        print(f"wrote TXT -> {tdest}", flush=True)
    jdest = os.environ.get("H878_JSON")
    if jdest:
        with open(jdest, "w") as f:
            json.dump(res, f, indent=2)
        print(f"wrote JSON -> {jdest}", flush=True)


if __name__ == "__main__":
    main()
