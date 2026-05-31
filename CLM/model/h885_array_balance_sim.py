"""H_885 — MITOSIS multi-chip array LOAD-BALANCE via capacity-aware re-partition.

VERDICT run for F-CLM-ARRAY-BALANCE (UNIVERSE H_885, the AXIS1 7B scale-out
blocker). Re-approaches H_878 (CLOSED-NEGATIVE) with a better dispatcher.

H_878 showed that a STATIC HASH partition of E sparse experts across N MITOSIS
chips (even contiguous shards, expert e -> fixed chip e // shard_size) leaves the
per-chip token load badly IMBALANCED, because the trained top-k router monopolizes
a few experts. H_885 asks:

    Does a CAPACITY-AWARE re-partition (assign experts to chips by MEASURED
    per-expert usage so each chip's aggregate load is balanced) FIX the imbalance
    WITHOUT hurting aggregate output quality?

SW-sim construction (a_scale_honest_scope, identical scope to H_878):
  * Train a single CLMArray (E experts, the landed sparse skeleton) -- SAME as H_878.
  * The SINGLE forward (all experts in one model) = the REFERENCE.
  * STATIC-HASH arm (S): the H_878 partition -- even contiguous shards.
  * CAPACITY-AWARE arm (C): PROFILE per-expert top-1 dispatch counts on a held-out
    PROFILING split (DISJOINT from the eval split), then greedily assign experts
    (descending profiled load) to the least-loaded chip (LPT bin-pack). The
    assignment NEVER peeks at the eval tokens it is scored on.
  * Both arms partition the SAME experts disjointly and route with the SAME router
    weights, so the gathered aggregate is mathematically the single-model forward
    re-associated by chip -> coherence is preserved EXACTLY for either partition.
    The ONLY thing the partition changes is which chip owns which expert, i.e. the
    per-chip LOAD distribution. That is exactly the H_878 gap H_885 attacks.

LOAD METRIC: per-chip dispatch-count CV = std(chip_counts)/mean(chip_counts)
(population std), the scale-free "per-chip load CV" named in the H_885 row.

NOT measured: chip-to-chip DMA latency, silicon timing, real-chip int4 emit drift
(hardware follow-up). CPU/Mac (or single-GPU) toy harness ($0); toy != scale (H_666).

PRE-REGISTERED, FROZEN BEFORE THE RUN (@L7, no post-hoc tampering):
  .verdicts/clm-array-balance/F-CLM-ARRAY-BALANCE_prereg.txt

Run:  python3 CLM/model/h885_array_balance_sim.py
Set H885_JSON / H885_TXT to persist outputs. H885_DEVICE=cuda to use GPU.
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

# ---- device (move ALL tensors here; H_880/882 bug was eval batches left on cpu)
_DEV = os.environ.get("H885_DEVICE", "cuda" if torch.cuda.is_available() else "cpu")
DEVICE = torch.device(_DEV)
if DEVICE.type == "cuda":
    # torch-nightly cuDNN can error on this conv stack; disable if it does.
    if os.environ.get("H885_CUDNN_OFF", "0") == "1":
        torch.backends.cudnn.enabled = False


def _to_dev(x):
    return x.to(DEVICE)


# ---- FROZEN pre-registered thresholds (@L7) ------------------------------- #
N_CHIPS_AXIS = [2, 4, 8]      # N=1 degenerate omitted (CV gain undefined)
N_EXPERTS = 8                 # fixed; partitioned onto N chips by each arm
SEEDS = [42, 43, 44]
TRAIN_STEPS = 120
EVAL_BATCHES = 16
PROFILE_BATCHES = 16          # DISJOINT split for capacity-aware assignment
SEQ_LEN = 64
BATCH_SIZE = 16
LR = 3e-3

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
    "profile_batches": PROFILE_BATCHES,
    "load_metric": "per-chip dispatch-count CV = std/mean (population std)",
    "coh_logit_atol": COH_LOGIT_ATOL,
    "coh_hamming_max": COH_HAMMING_MAX,
    "coh_ce_atol": COH_CE_ATOL,
    "arms": "S=static-hash (H_878 baseline) ; C=capacity-aware LPT bin-pack on disjoint profile split",
    "falsifier": ("F-CLM-ARRAY-BALANCE: for every N in {2,4,8} -- capacity-aware arm "
                  "no chip starves AND CV(capacity-aware) < CV(static-hash) AND "
                  "max|logit_capaware-logit_ref| <= coh_logit_atol AND argmax-hamming "
                  "<= coh_hamming_max AND |CE_capaware-CE_ref| <= coh_ce_atol"),
    "scope": ("SW-sim of @L2 deploy chip-fit track -- silicon NOT measured "
              "(1 AKD1000 today); a_scale_honest_scope; re-approach of H_878 (router)"),
    "device": str(DEVICE),
}


def _even_partition(n_experts: int, n_chips: int) -> List[List[int]]:
    """STATIC-HASH arm (S): the H_878 partition. Even contiguous shards."""
    base = n_experts // n_chips
    rem = n_experts % n_chips
    shards: List[List[int]] = []
    idx = 0
    for c in range(n_chips):
        size = base + (1 if c < rem else 0)
        shards.append(list(range(idx, idx + size)))
        idx += size
    return shards


def _capacity_aware_partition(expert_loads: List[float], n_chips: int) -> List[List[int]]:
    """CAPACITY-AWARE arm (C): LPT (longest-processing-time) greedy bin-pack.

    Given PROFILED per-expert loads (top-1 dispatch counts on the disjoint profile
    split), assign experts (descending profiled load) to the currently least-loaded
    chip. This balances each chip's expected aggregate load instead of using a
    load-blind static hash. Standard makespan-minimization heuristic; the partition
    is still disjoint (each expert lives on exactly one chip), so coherence holds.
    """
    order = sorted(range(len(expert_loads)), key=lambda e: -expert_loads[e])
    chip_load = [0.0] * n_chips
    shards: List[List[int]] = [[] for _ in range(n_chips)]
    # seed each chip with one expert first (guarantee no chip is left empty when
    # E >= n_chips), then LPT-assign the remainder.
    for c in range(n_chips):
        e = order[c]
        shards[c].append(e)
        chip_load[c] += expert_loads[e]
    for e in order[n_chips:]:
        c = min(range(n_chips), key=lambda c: chip_load[c])
        shards[c].append(e)
        chip_load[c] += expert_loads[e]
    for sh in shards:
        sh.sort()
    return shards


@torch.no_grad()
def _single_model_forward(model, x) -> Dict:
    """REFERENCE: the monolithic CLMArray forward (all experts in one model)."""
    out = model(x)
    return {"logits": out["logits"]}


@torch.no_grad()
def _router_top1(model, x) -> torch.Tensor:
    """Per-token top-1 expert id (B,T). Used for profiling + load counting."""
    moe = model.moe
    h = model.embed(x).transpose(1, 2)
    h = model.embed_conv(h)
    for layer in model.trunk:
        h = layer(h)
    logits_r = moe.router(h)                       # (B, n_e, T)
    probs = F.softmax(logits_r, dim=1)
    return probs.argmax(dim=1)                     # (B, T)


@torch.no_grad()
def _profile_expert_loads(model, batches, n_e: int) -> List[float]:
    """Top-1 dispatch counts per expert over the DISJOINT profiling split."""
    counts = torch.zeros(n_e, device=DEVICE)
    for x, _y in batches:
        x = _to_dev(x)
        top1 = _router_top1(model, x)
        counts += torch.bincount(top1.reshape(-1), minlength=n_e).float()
    return [float(v) for v in counts.tolist()]


@torch.no_grad()
def _chip_array_forward(model, x, shards: List[List[int]]) -> Dict:
    """SW-sim N-chip forward: partition experts onto chips, dispatch, gather.

    Identical math to H_878's _chip_array_forward -- only the `shards` mapping
    differs between arms. Returns gathered logits + per-CHIP top-1 dispatch counts.
    """
    moe = model.moe
    cfg = moe.cfg
    n_e = cfg.n_experts
    k = min(cfg.top_k, n_e)

    h = model.embed(x).transpose(1, 2)
    h = model.embed_conv(h)
    for layer in model.trunk:
        h = layer(h)

    logits_r = moe.router(h)                       # (B, n_e, T)
    probs = F.softmax(logits_r, dim=1)
    topv, topi = probs.topk(k, dim=1)
    gate = topv / (topv.sum(dim=1, keepdim=True) + 1e-9)
    mask = torch.zeros_like(probs).scatter_(1, topi, gate)   # (B, n_e, T)

    expert2chip = torch.empty(n_e, dtype=torch.long, device=DEVICE)
    for c, sh in enumerate(shards):
        for e in sh:
            expert2chip[e] = c
    n_chips = len(shards)

    B, C, T = h.shape
    gathered = torch.zeros(B, C, T, device=DEVICE)
    for c, sh in enumerate(shards):
        chip_emit = torch.zeros(B, C, T, device=DEVICE)
        for e in sh:
            chip_emit = chip_emit + mask[:, e:e + 1, :] * moe.experts[e](h)
        gathered = gathered + chip_emit            # GATHER (sum across chips)

    y = model.norm_out(gathered)
    out_logits = model.readout(y)

    top1 = probs.argmax(dim=1)                     # (B, T)
    expert_counts = torch.bincount(top1.reshape(-1), minlength=n_e).float()
    chip_counts = torch.zeros(n_chips, device=DEVICE)
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
        x, y = _to_dev(x), _to_dev(y)
        opt.zero_grad()
        out = model(x, y)
        out["loss"].backward()
        opt.step()
    return stream


def _cv(counts: List[float]) -> float:
    t = torch.tensor(counts, dtype=torch.float64)
    mean = float(t.mean())
    if mean <= 0:
        return float("inf")
    return float(t.std(unbiased=False) / mean)


def _coherence(model, eval_batches, shards) -> Dict:
    """Aggregate-emit coherence of the partition's gather vs single-model ref."""
    max_logit_diff = 0.0
    n_argmax = 0
    n_argmax_mismatch = 0
    ce_ref_sum = 0.0
    ce_arr_sum = 0.0
    n_ce = 0
    chip_counts_acc = torch.zeros(len(shards), device=DEVICE)
    with torch.no_grad():
        for x, y in eval_batches:
            x, y = _to_dev(x), _to_dev(y)
            ref = _single_model_forward(model, x)
            arr = _chip_array_forward(model, x, shards)

            d = float((arr["logits"] - ref["logits"]).abs().max())
            if d > max_logit_diff:
                max_logit_diff = d

            am_ref = ref["logits"].argmax(dim=1)
            am_arr = arr["logits"].argmax(dim=1)
            n_argmax += am_ref.numel()
            n_argmax_mismatch += int((am_ref != am_arr).sum())

            V = ref["logits"].shape[1]
            ce_ref = float(F.cross_entropy(
                ref["logits"].transpose(1, 2).reshape(-1, V), y.reshape(-1)))
            ce_arr = float(F.cross_entropy(
                arr["logits"].transpose(1, 2).reshape(-1, V), y.reshape(-1)))
            ce_ref_sum += ce_ref
            ce_arr_sum += ce_arr
            n_ce += 1
            chip_counts_acc = chip_counts_acc + arr["chip_counts"]
    return {
        "max_logit_diff": max_logit_diff,
        "hamming": n_argmax_mismatch / max(1, n_argmax),
        "ce_delta": abs((ce_arr_sum - ce_ref_sum) / max(1, n_ce)),
        "chip_counts": [int(v) for v in chip_counts_acc.tolist()],
    }


def _measure(n_chips: int, seed: int) -> Dict:
    torch.manual_seed(seed)
    model = build_array(n_experts=N_EXPERTS).to(DEVICE)
    stream = _train(model, seed)
    model.eval()

    # DISJOINT splits: profile != eval (capacity-aware never peeks at eval tokens)
    profile_batches = make_batches(stream, SEQ_LEN, BATCH_SIZE, PROFILE_BATCHES,
                                   seed=seed + 500)
    eval_batches = list(make_batches(stream, SEQ_LEN, BATCH_SIZE, EVAL_BATCHES,
                                     seed=seed + 999))

    # arm S: static-hash (the H_878 partition)
    shards_static = _even_partition(N_EXPERTS, n_chips)

    # arm C: capacity-aware -- profile per-expert load, then LPT bin-pack
    expert_loads = _profile_expert_loads(model, profile_batches, N_EXPERTS)
    shards_capaware = _capacity_aware_partition(expert_loads, n_chips)

    coh_static = _coherence(model, eval_batches, shards_static)
    coh_capaware = _coherence(model, eval_batches, shards_capaware)

    cv_static = _cv([float(v) for v in coh_static["chip_counts"]])
    cv_capaware = _cv([float(v) for v in coh_capaware["chip_counts"]])
    no_starve_capaware = bool(min(coh_capaware["chip_counts"]) > 0)

    return {
        "n_chips": n_chips, "seed": seed,
        "expert_loads_profiled": [int(v) for v in expert_loads],
        "shards_static": shards_static,
        "shards_capaware": shards_capaware,
        "chip_counts_static": coh_static["chip_counts"],
        "chip_counts_capaware": coh_capaware["chip_counts"],
        "cv_static": round(cv_static, 6) if math.isfinite(cv_static) else None,
        "cv_capaware": round(cv_capaware, 6) if math.isfinite(cv_capaware) else None,
        "no_starve_capaware": no_starve_capaware,
        "max_logit_diff_capaware": round(coh_capaware["max_logit_diff"], 9),
        "hamming_capaware": round(coh_capaware["hamming"], 9),
        "ce_delta_capaware": round(coh_capaware["ce_delta"], 9),
        "expert_params": model.moe.expert_param_count(),
        "chip_fit": model.expert_chip_fit(),
    }


def run() -> Dict:
    per_N: Dict[int, Dict] = {}
    rows: List[Dict] = []
    for N in N_CHIPS_AXIS:
        seed_rows = [_measure(N, s) for s in SEEDS]
        rows.extend(seed_rows)
        cv_s = [r["cv_static"] for r in seed_rows if r["cv_static"] is not None]
        cv_c = [r["cv_capaware"] for r in seed_rows if r["cv_capaware"] is not None]
        per_N[N] = {
            "mean_cv_static": round(sum(cv_s) / len(cv_s), 6) if cv_s else None,
            "mean_cv_capaware": round(sum(cv_c) / len(cv_c), 6) if cv_c else None,
            "all_no_starve_capaware": all(r["no_starve_capaware"] for r in seed_rows),
            "max_logit_diff_capaware": round(
                max(r["max_logit_diff_capaware"] for r in seed_rows), 9),
            "max_hamming_capaware": round(
                max(r["hamming_capaware"] for r in seed_rows), 9),
            "max_ce_delta_capaware": round(
                max(r["ce_delta_capaware"] for r in seed_rows), 9),
            "chip_fit": all(r["chip_fit"] for r in seed_rows),
        }

    # --- frozen falsifier evaluation (NO threshold tampering) -------------- #
    cv_improved = all(
        per_N[N]["mean_cv_capaware"] is not None
        and per_N[N]["mean_cv_static"] is not None
        and per_N[N]["mean_cv_capaware"] < per_N[N]["mean_cv_static"]
        for N in N_CHIPS_AXIS)
    no_starve_ok = all(per_N[N]["all_no_starve_capaware"] for N in N_CHIPS_AXIS)
    coh_logit_ok = all(
        per_N[N]["max_logit_diff_capaware"] <= COH_LOGIT_ATOL for N in N_CHIPS_AXIS)
    coh_hamming_ok = all(
        per_N[N]["max_hamming_capaware"] <= COH_HAMMING_MAX for N in N_CHIPS_AXIS)
    coh_ce_ok = all(
        per_N[N]["max_ce_delta_capaware"] <= COH_CE_ATOL for N in N_CHIPS_AXIS)
    all_chip_fit = all(per_N[N]["chip_fit"] for N in N_CHIPS_AXIS)
    passed = bool(cv_improved and no_starve_ok and coh_logit_ok
                  and coh_hamming_ok and coh_ce_ok)

    return {
        "frozen": FROZEN,
        "per_N": {str(N): per_N[N] for N in N_CHIPS_AXIS},
        "per_run": rows,
        "cv_improved_capaware_lt_static": cv_improved,
        "no_starve_capaware_ok": no_starve_ok,
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
        "device": str(DEVICE),
    }


def _fmt_txt(res: Dict) -> str:
    L = []
    L.append("F-CLM-ARRAY-BALANCE -- capacity-aware re-partition vs static-hash (H_878 re-approach)")
    L.append("=" * 84)
    L.append("FROZEN (pre-run, @L7 no tampering):")
    for k, v in res["frozen"].items():
        L.append(f"  {k} = {v}")
    L.append("")
    L.append(f"{'N':>3} {'CV_static':>11} {'CV_capaware':>12} {'CV_improved':>12} "
             f"{'no_starve_C':>12} {'max_logit_d':>12} {'hamming':>9} {'ce_delta':>11}")
    for N in N_CHIPS_AXIS:
        d = res["per_N"][str(N)]
        cs = d["mean_cv_static"]
        cc = d["mean_cv_capaware"]
        improved = (cc is not None and cs is not None and cc < cs)
        L.append(f"{N:>3} {cs:>11.4f} {cc:>12.4f} {str(improved):>12} "
                 f"{str(d['all_no_starve_capaware']):>12} "
                 f"{d['max_logit_diff_capaware']:>12.2e} "
                 f"{d['max_hamming_capaware']:>9.4f} {d['max_ce_delta_capaware']:>11.2e}")
    L.append("")
    L.append(f"CV improved (capaware < static, all N): {res['cv_improved_capaware_lt_static']}")
    L.append(f"no-starve capacity-aware (all N): {res['no_starve_capaware_ok']}")
    L.append(f"coherence logit OK (atol {COH_LOGIT_ATOL}): {res['coherence_logit_ok']}")
    L.append(f"coherence hamming OK (<= {COH_HAMMING_MAX}): {res['coherence_hamming_ok']}")
    L.append(f"coherence CE OK (atol {COH_CE_ATOL}): {res['coherence_ce_ok']}")
    L.append(f"all chips chip-fit: {res['all_chip_fit']}")
    L.append(f"scale scope       : {res['scale_scope']}")
    L.append(f"device            : {res['device']}")
    L.append("")
    L.append(f"VERDICT: {res['verdict']}  {res['verdict_tier']}")
    return "\n".join(L) + "\n"


def main() -> None:
    res = run()
    txt = _fmt_txt(res)
    print(txt, flush=True)
    tdest = os.environ.get("H885_TXT")
    if tdest:
        with open(tdest, "w") as f:
            f.write(txt)
        print(f"wrote TXT -> {tdest}", flush=True)
    jdest = os.environ.get("H885_JSON")
    if jdest:
        with open(jdest, "w") as f:
            json.dump(res, f, indent=2)
        print(f"wrote JSON -> {jdest}", flush=True)


if __name__ == "__main__":
    main()
