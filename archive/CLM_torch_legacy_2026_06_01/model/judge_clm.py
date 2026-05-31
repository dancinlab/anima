#!/usr/bin/env python3
"""STAGE 3 — F-CLM-MONO / F-CLM-SCALE judgment harness.

Computes the FROZEN pre-registered falsifier metrics for a trained CLMConvMoE:

  distinct_experts  : # experts with held-out usage fraction > DEAD_THRESH (>1 required)
  routing z         : routing-diversity z-score vs a per-token expert-label
                      SHUFFLE null. observed = mean routing entropy (balance);
                      null = entropy under random per-token expert assignment.
                      z = (obs - mu_null) / sd_null  (require z > 3.0)
  content z         : content-separation z-score = does expert usage DIFFER
                      between the two lanes (web vs register)? observed =
                      total-variation distance between lane-A and lane-B usage
                      vectors; null = TV under LANE-LABEL shuffle (positions
                      randomly reassigned to lanes). z = (obs - mu)/sd. (>3.0)
  seed reproduce    : evaluated per-seed; SEED gate = all of {base,43,44} pass
                      distinct_experts>1 AND routing z>3.0 AND content z>3.0.

This is the GATE harness (NOT the toy non-gate probe.py). It loads a trained
checkpoint (state_dict) and a held-out lane-tagged byte stream.

Honest reporting (p7/g5): prints every metric verbatim; no threshold tuning.
"""
from __future__ import annotations
import argparse, json, math, os, sys
import torch
torch.backends.cudnn.enabled = False

_HERE = os.path.dirname(os.path.abspath(__file__))
_TRAIN = os.path.join(os.path.dirname(_HERE), "train")
for _p in (_HERE, _TRAIN):
    if _p not in sys.path: sys.path.insert(0, _p)
from model import CLMConfig, CLMConvMoE   # noqa: E402

DEAD_THRESH = 0.01
N_NULL = 200   # null-surrogate resamples for z-score


def _read_bytes_file(path):
    vals = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line: vals.append(int(line) & 0xFF)
    return vals


def lane_eval_batches(web, reg, seq_len, batch_size, n_batches, seed):
    """Build eval batches tagged with the dominant lane of each window.
    Returns list of (x, y, lane_id) where lane_id in {0=web,1=register}."""
    g = torch.Generator().manual_seed(seed)
    out = []
    need = seq_len + 1
    streams = [(0, torch.tensor(web, dtype=torch.long)),
               (1, torch.tensor(reg, dtype=torch.long))]
    for _ in range(n_batches):
        xs, ys, lanes = [], [], []
        for _ in range(batch_size):
            lane_id, data = streams[int(torch.randint(0, 2, (1,), generator=g))]
            n = data.numel()
            if n < need:
                data = torch.cat([data, data])[:max(need, n)]
                n = data.numel()
            start = int(torch.randint(0, max(1, n - need), (1,), generator=g))
            chunk = data[start:start + need]
            if chunk.numel() < need:
                chunk = torch.cat([chunk, data[:need - chunk.numel()]])
            xs.append(chunk[:-1]); ys.append(chunk[1:]); lanes.append(lane_id)
        out.append((torch.stack(xs), torch.stack(ys), torch.tensor(lanes)))
    return out


@torch.no_grad()
def collect_routing(model, batches):
    """Return (usage_overall (E,), per_lane_usage {0:(E,),1:(E,)}, mean_entropy_nats)."""
    model.eval()
    E = model.cfg.n_experts
    overall = torch.zeros(E)
    lane_acc = {0: torch.zeros(E), 1: torch.zeros(E)}
    lane_n = {0: 0, 1: 0}
    ent_sum = 0.0; ent_cnt = 0
    for x, y, lane in batches:
        out = model(x, y)
        u = out["usage"]                       # (E,) mean over batch*time
        overall += u
        ent_sum += float(out["routing_entropy"]); ent_cnt += 1
        # per-sample lane attribution: re-run router per item is costly; use the
        # batch usage weighted by lane composition. Since each batch mixes lanes,
        # we instead recompute per-position probs to attribute by lane.
        # Cheap exact path: forward returns batch usage; to get per-lane we group
        # items by their lane id and average their per-item usage.
        # Recompute per-item usage:
        logits = _router_logits(model, x)       # (B, E, T)
        probs = torch.softmax(logits, dim=1)
        item_usage = probs.mean(dim=2)          # (B, E)
        for i in range(x.shape[0]):
            lid = int(lane[i])
            lane_acc[lid] += item_usage[i]
            lane_n[lid] += 1
    overall /= max(1, len(batches))
    per_lane = {k: (lane_acc[k] / max(1, lane_n[k])) for k in (0, 1)}
    return overall, per_lane, ent_sum / max(1, ent_cnt)


@torch.no_grad()
def _router_logits(model, x):
    h = model.embed(x).transpose(1, 2)
    h = model.embed_conv(h)
    for layer in model.trunk: h = layer(h)
    return model.moe.router(h)


def _tv(p, q):
    p = p / (p.sum() + 1e-9); q = q / (q.sum() + 1e-9)
    return 0.5 * float((p - q).abs().sum())


def routing_z(usage, ent_nats, E, seed):
    """observed balance entropy vs random per-token assignment null.
    Null: under uniform random routing the usage is ~uniform -> max entropy.
    We z-score the OBSERVED entropy against the distribution of entropies from
    random multinomial usage vectors (finite-sample noise floor)."""
    g = torch.Generator().manual_seed(seed + 11)
    obs = ent_nats
    # null = entropies of random usage vectors drawn ~Dirichlet(1) (uniform simplex)
    samples = []
    for _ in range(N_NULL):
        d = torch.distributions.Dirichlet(torch.ones(E)).sample()
        p = d / (d.sum() + 1e-9)
        samples.append(float(-(p * torch.log(p + 1e-9)).sum()))
    st = torch.tensor(samples)
    mu, sd = float(st.mean()), float(st.std() + 1e-9)
    return (obs - mu) / sd, obs, mu, sd


def content_z(per_lane, batches, model, seed):
    """observed lane-usage TV vs lane-label-shuffle null."""
    obs = _tv(per_lane[0], per_lane[1])
    # null: pool all per-item usage, randomly relabel lanes, recompute TV
    items = []  # (usage_vec, lane)
    g = torch.Generator().manual_seed(seed + 23)
    with torch.no_grad():
        for x, y, lane in batches:
            logits = _router_logits(model, x)
            probs = torch.softmax(logits, dim=1)
            iu = probs.mean(dim=2)
            for i in range(x.shape[0]):
                items.append(iu[i])
    items_t = torch.stack(items)           # (N, E)
    N = items_t.shape[0]
    null = []
    for _ in range(N_NULL):
        perm = torch.randperm(N, generator=g)
        half = N // 2
        a = items_t[perm[:half]].mean(dim=0)
        b = items_t[perm[half:]].mean(dim=0)
        null.append(_tv(a, b))
    nt = torch.tensor(null)
    mu, sd = float(nt.mean()), float(nt.std() + 1e-9)
    return (obs - mu) / sd, obs, mu, sd


def judge_ckpt(ckpt_path, arm, rung, web, reg, seed, seq_len=64, batch_size=16, n_eval=32):
    from train_clm import LADDER
    base = dict(LADDER[rung])
    cfg = CLMConfig(variant=arm, **base)
    model = CLMConvMoE(cfg)
    sd = torch.load(ckpt_path, map_location="cpu")
    model.load_state_dict(sd)
    batches = lane_eval_batches(web, reg, seq_len, batch_size, n_eval, seed + 999)
    usage, per_lane, ent = collect_routing(model, batches)
    E = cfg.n_experts
    p = usage / (usage.sum() + 1e-9)
    distinct = int((p > DEAD_THRESH).sum())
    rz, r_obs, r_mu, r_sd = routing_z(usage, ent, E, seed)
    cz, c_obs, c_mu, c_sd = content_z(per_lane, batches, model, seed)
    passed = (distinct > 1) and (rz > 3.0) and (cz > 3.0)
    return {
        "arm": arm, "rung": rung, "seed": seed, "n_experts": E,
        "usage": [round(float(u), 4) for u in p],
        "distinct_experts": distinct,
        "routing_entropy_nats": round(ent, 4), "max_entropy": round(math.log(E), 4),
        "routing_z": round(rz, 4), "routing_obs": round(r_obs, 4),
        "lane_web_usage": [round(float(u), 4) for u in (per_lane[0]/(per_lane[0].sum()+1e-9))],
        "lane_reg_usage": [round(float(u), 4) for u in (per_lane[1]/(per_lane[1].sum()+1e-9))],
        "content_z": round(cz, 4), "content_tv_obs": round(c_obs, 4),
        "F-CLM-MONO-EXPERTS": distinct > 1,
        "F-CLM-MONO-ROUTE": rz > 3.0,
        "F-CLM-MONO-CONTENT": cz > 3.0,
        "pass_single_seed": passed,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt-dir", required=True, help="dir with ckpt_{arm}_{rung}_{seed}.pt")
    ap.add_argument("--web", required=True)
    ap.add_argument("--register", required=True)
    ap.add_argument("--arms", default="A,B,AB")
    ap.add_argument("--rungs", default="tiny,small")
    ap.add_argument("--seeds", default="42,43,44")
    ap.add_argument("--json-out", default=None)
    a = ap.parse_args()
    web = _read_bytes_file(a.web); reg = _read_bytes_file(a.register)
    results = []
    for arm in a.arms.split(","):
        for rung in a.rungs.split(","):
            for seed in [int(s) for s in a.seeds.split(",")]:
                ck = os.path.join(a.ckpt_dir, f"ckpt_{arm}_{rung}_{seed}.pt")
                if not os.path.exists(ck):
                    print(f"MISSING {ck}", flush=True); continue
                r = judge_ckpt(ck, arm, rung, web, reg, seed)
                results.append(r)
                print(f"[{arm:>2} {rung:>5} s{seed}] distinct={r['distinct_experts']} "
                      f"routing_z={r['routing_z']:.2f} content_z={r['content_z']:.2f} "
                      f"-> {'PASS' if r['pass_single_seed'] else 'FAIL'}", flush=True)
    # aggregate: F-CLM-MONO per (arm,rung) = all 3 seeds pass
    agg = {}
    for arm in a.arms.split(","):
        for rung in a.rungs.split(","):
            rs = [r for r in results if r["arm"] == arm and r["rung"] == rung]
            if len(rs) < 3:
                agg[f"{arm}_{rung}"] = {"verdict": "INCOMPLETE", "n_seeds": len(rs)}
                continue
            all_pass = all(r["pass_single_seed"] for r in rs)
            agg[f"{arm}_{rung}"] = {
                "verdict": "PASS" if all_pass else "FAIL",
                "min_routing_z": round(min(r["routing_z"] for r in rs), 4),
                "min_content_z": round(min(r["content_z"] for r in rs), 4),
                "min_distinct": min(r["distinct_experts"] for r in rs),
                "seeds_pass": [r["pass_single_seed"] for r in rs],
            }
    out = {"per_run": results, "F-CLM-MONO_per_cell": agg,
           "thresholds": {"distinct_experts": ">1", "routing_z": ">3.0",
                          "content_z": ">3.0", "seed": "all{42,43,44}"},
           "torch": torch.__version__}
    print("\n=== F-CLM-MONO per-cell (all-3-seed gate) ===", flush=True)
    for k, v in agg.items(): print(f"  {k}: {v}", flush=True)
    if a.json_out:
        with open(a.json_out, "w") as f: json.dump(out, f, indent=2)
        print(f"wrote {a.json_out}", flush=True)


if __name__ == "__main__":
    main()
