"""H_875 - continual-learning forgetting curve (dose-response).

Maps base-ability forgetting (F-CLM-BOUND z_drop) as a FUNCTION of edge-learn
step count, on BOTH the readout-only edge (H_861 baseline) and the trunk-adjacent
adapter edge (H_865 fix). Produces the curve and identifies, per edge type, the
SAFE STEP BUDGET - the largest swept step count at which z_drop stays below the
RETAIN gate (z_drop < 1.0, the F-CLM-BOUND cutoff frozen at bf98c01).

Reuses VERBATIM from H_861/H_865: the backbone (mid d512/L8/E8 AKIDA int4-sym),
the core/edge split for both edge types, the base-ability / new-context byte
distributions and seeds, the z_drop / gain definitions, and the RETAIN cutoff
z_drop < 1.0. The ONLY new axis is the step ladder [1,2,4,8,16,32,64,128,200,300];
step 300 anchors the H_861/H_865 endpoint exactly.

W2 discipline: crossing threshold FROZEN VERBATIM from F-CLM-BOUND_prereg.txt
(commit bf98c01); post-tuning = 0. A finite (or zero, or >=max) safe budget is
reported honestly (a_paper_negative_ok).

SW-sim of the non-deterministic on-chip edge-learn is acceptable at the
measurement rung (a_scale_honest_scope); foundation H_679 established HW
edge-learn is real. Scope: MEASUREMENT rung (mid d512/L8/E8) only.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model import CLMConfig, CLMConvMoE  # noqa: E402

# --- frozen constants (VERBATIM from H_861 / H_865 prereg) ---
BASE_SEED = 101
NEW_SEED = 202
LR_EDGE = 3e-3
SEQ_LEN = 64
BATCH_SIZE = 16
N_EVAL_BATCHES = 32
ADAPTER_RANK = 64

THR_Z_DROP = 1.0  # F-CLM-BOUND RETAIN cutoff, frozen bf98c01 - the crossing threshold

# the dose axis (frozen ladder); 300 anchors the H_861/H_865 endpoint
STEP_LADDER = [1, 2, 4, 8, 16, 32, 64, 128, 200, 300]
N_ADAPT_MAX = max(STEP_LADDER)


def _lcg(seed):
    state = seed & 0x7FFFFFFF
    while True:
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        yield state


def make_lane_bytes(kind, n, seed):
    rng = _lcg(seed + 1)
    out = []
    if kind == "web":
        motifs = [
            [0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x20],
            [0x77, 0x6f, 0x72, 0x6c, 0x64, 0x2e, 0x20],
            [0x74, 0x68, 0x65, 0x20, 0x71, 0x75, 0x69],
        ]
        while len(out) < n:
            m = motifs[next(rng) % len(motifs)]
            out.extend(m)
            if next(rng) % 17 == 0:
                out.append(0x20 + (next(rng) % 0x5e))
    else:
        period = 11 + (seed % 7)
        base = 0x80
        for i in range(n):
            v = base + ((i % period) * 13 + (next(rng) % 5)) % 0x7f
            out.append(v & 0xFF)
    return out[:n]


def batchify(byte_list, seq_len, n_batches, batch_size, seed):
    g = torch.Generator().manual_seed(seed)
    data = torch.tensor(byte_list, dtype=torch.long)
    max_start = len(data) - seq_len - 1
    batches = []
    for _ in range(n_batches):
        starts = torch.randint(0, max_start, (batch_size,), generator=g)
        toks = torch.stack([data[s:s + seq_len] for s in starts])
        tgts = torch.stack([data[s + 1:s + seq_len + 1] for s in starts])
        batches.append((toks, tgts))
    return batches


class AdapterEdge(nn.Module):
    """Thin additive adapter; up zero-init => identity at step 0 (H_865)."""

    def __init__(self, d_model, rank):
        super().__init__()
        self.down = nn.Conv1d(d_model, rank, kernel_size=1)
        self.act = nn.GELU()
        self.up = nn.Conv1d(rank, d_model, kernel_size=1)
        nn.init.zeros_(self.up.weight)
        nn.init.zeros_(self.up.bias)

    def forward(self, h):
        return h + self.up(self.act(self.down(h)))


class EdgeModel(nn.Module):
    """Frozen backbone + either a readout-only edge (H_861) or an adapter edge
    (H_865). Base always frozen except, for readout-only, the readout conv."""

    def __init__(self, base, edge_type):
        super().__init__()
        self.base = base
        self.edge_type = edge_type
        for p in self.base.parameters():
            p.requires_grad_(False)
        if edge_type == "readout_only":
            self.base.readout.weight.requires_grad_(True)
            self.base.readout.bias.requires_grad_(True)
            self.adapter = None
        elif edge_type == "adapter":
            self.adapter = AdapterEdge(base.cfg.d_model, ADAPTER_RANK)
        else:
            raise ValueError(edge_type)

    def _hidden(self, tokens):
        b = self.base
        x = b.embed(tokens).transpose(1, 2)
        x = b.embed_conv(x)
        for layer in b.trunk:
            x = layer(x)
        x, _ = b.moe(x)
        h = b.norm_out(x)
        if self.adapter is not None:
            h = self.adapter(h)
        return h

    def forward(self, tokens, targets=None):
        h = self._hidden(tokens)
        logits = self.base.readout(h)
        out = {"logits": logits}
        if targets is not None:
            out["ce_loss"] = F.cross_entropy(
                logits.transpose(1, 2).reshape(-1, self.base.cfg.vocab_size),
                targets.reshape(-1),
            )
        return out

    def edge_params(self):
        if self.edge_type == "readout_only":
            return [self.base.readout.weight, self.base.readout.bias]
        return list(self.adapter.parameters())


@torch.no_grad()
def eval_ce(model, batches):
    ces = []
    for toks, tgts in batches:
        ces.append(model(toks, tgts)["ce_loss"].item())
    t = torch.tensor(ces)
    return t.mean().item(), t.std(unbiased=False).item()


def infer_config_and_load(ckpt_path):
    obj = torch.load(ckpt_path, map_location="cpu")
    if isinstance(obj, dict) and "state_dict" in obj:
        sd = obj["state_dict"]
        meta = obj.get("config") or obj.get("cfg") or {}
    elif isinstance(obj, dict) and any(
        k.startswith(("embed", "trunk", "moe", "readout")) for k in obj
    ):
        sd, meta = obj, {}
    else:
        sd = obj.get("model", obj) if isinstance(obj, dict) else obj
        meta = obj.get("config", {}) if isinstance(obj, dict) else {}
    d_model = sd["embed.weight"].shape[1]
    vocab = sd["embed.weight"].shape[0]
    n_trunk = len({k.split(".")[1] for k in sd if k.startswith("trunk.")})
    n_experts = len({k.split(".")[2] for k in sd if k.startswith("moe.experts.")})
    variant = meta.get("variant", "AB") if isinstance(meta, dict) else "AB"
    cfg = CLMConfig(vocab_size=vocab, d_model=d_model, n_trunk_layers=n_trunk,
                    n_experts=n_experts, variant=variant)
    base = CLMConvMoE(cfg)
    missing, unexpected = base.load_state_dict(sd, strict=False)
    return base, cfg, missing, unexpected, sd


def measure_point(base_sd, cfg, edge_type, n_steps, base_eval, new_eval, new_train, device):
    """Fresh model from frozen backbone; adapt n_steps; return z_drop, gain."""
    base = CLMConvMoE(cfg)
    base.load_state_dict(base_sd, strict=False)
    base = base.to(device)
    model = EdgeModel(base, edge_type).to(device)

    model.eval()
    ce_base_pre, sd_base_pre = eval_ce(model, base_eval)
    ce_new_pre, _ = eval_ce(model, new_eval)

    opt = torch.optim.Adam(model.edge_params(), lr=LR_EDGE)
    model.train()
    for i in range(n_steps):
        toks, tgts = new_train[i]
        toks, tgts = toks.to(device), tgts.to(device)
        out = model(toks, tgts)
        opt.zero_grad()
        out["ce_loss"].backward()
        opt.step()
    model.eval()
    ce_base_post, _ = eval_ce(model, base_eval)
    ce_new_post, _ = eval_ce(model, new_eval)

    z_drop = (ce_base_post - ce_base_pre) / max(sd_base_pre, 1e-6)
    gain = ce_new_pre - ce_new_post
    return {
        "steps": n_steps,
        "ce_base_pre": round(ce_base_pre, 5),
        "ce_base_post": round(ce_base_post, 5),
        "sd_base_pre": round(sd_base_pre, 5),
        "ce_new_pre": round(ce_new_pre, 5),
        "ce_new_post": round(ce_new_post, 5),
        "z_drop": round(z_drop, 5),
        "gain": round(gain, 5),
        "retain_pass": bool(z_drop < THR_Z_DROP),
    }


def safe_step_budget(curve):
    """Largest swept step S with z_drop < cutoff AND all smaller steps also < cutoff.
    Returns (budget, crossing_step, kind) kind in {finite, zero, ge_max}."""
    crossing = None
    for pt in curve:
        if pt["z_drop"] >= THR_Z_DROP:
            crossing = pt["steps"]
            break
    if crossing is None:
        return curve[-1]["steps"], None, "ge_max"
    passing = [pt["steps"] for pt in curve if pt["steps"] < crossing and pt["z_drop"] < THR_Z_DROP]
    if not passing:
        return 0, crossing, "zero"
    return max(passing), crossing, "finite"


def run_curve(edge_type, base_sd, cfg, device):
    base_bytes = make_lane_bytes("web", 30000, BASE_SEED)
    new_bytes = make_lane_bytes("new", 30000, NEW_SEED)
    half = len(new_bytes) // 2
    base_eval = batchify(base_bytes, SEQ_LEN, N_EVAL_BATCHES, BATCH_SIZE, BASE_SEED)
    new_eval = batchify(new_bytes[half:], SEQ_LEN, N_EVAL_BATCHES, BATCH_SIZE, NEW_SEED + 1)
    new_train = batchify(new_bytes[:half], SEQ_LEN, N_ADAPT_MAX, BATCH_SIZE, NEW_SEED + 2)

    curve = []
    for s in STEP_LADDER:
        pt = measure_point(base_sd, cfg, edge_type, s, base_eval, new_eval, new_train, device)
        curve.append(pt)
        print("[h875 %s] steps=%-3d z_drop=%+.4f gain=%+.4f retain=%s" % (
            edge_type, s, pt["z_drop"], pt["gain"], pt["retain_pass"]))
    budget, crossing, kind = safe_step_budget(curve)
    return {
        "edge_type": edge_type,
        "rung": "mid d512/L8/E8",
        "step_ladder": STEP_LADDER,
        "crossing_threshold_z_drop": THR_Z_DROP,
        "curve": curve,
        "safe_step_budget": budget,
        "safe_budget_kind": kind,
        "crossing_step": crossing,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--edges", default="readout_only,adapter")
    args = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(0)
    os.makedirs(args.out, exist_ok=True)

    base, cfg, missing, unexpected, sd = infer_config_and_load(args.ckpt)
    print("[h875] loaded backbone d=%d L=%d E=%d V=%d params=%d device=%s" % (
        cfg.d_model, cfg.n_trunk_layers, cfg.n_experts, cfg.vocab_size,
        base.num_params(), device))
    print("[h875] load missing=%s unexpected=%s" % (missing, unexpected))

    edges = [e.strip() for e in args.edges.split(",") if e.strip()]
    results = {}
    for et in edges:
        torch.manual_seed(0)
        results[et] = run_curve(et, sd, cfg, device)

    both_curves = all(results.get(et, {}).get("curve") for et in ("readout_only", "adapter")
                      if et in edges)
    adapter_ok = ("adapter" in results and
                  results["adapter"]["safe_budget_kind"] in ("finite", "ge_max") and
                  results["adapter"]["safe_step_budget"] > 0)
    verdict = "GREEN" if (both_curves and adapter_ok) else "RED"

    out = {
        "campaign": "H_875 continual-learning forgetting curve (dose-response)",
        "frozen_thresholds_commit": "bf98c01",
        "crossing_threshold_z_drop": THR_Z_DROP,
        "step_ladder": STEP_LADDER,
        "edges": results,
        "headline": {
            "readout_only_safe_budget": results.get("readout_only", {}).get("safe_step_budget"),
            "readout_only_budget_kind": results.get("readout_only", {}).get("safe_budget_kind"),
            "adapter_safe_budget": results.get("adapter", {}).get("safe_step_budget"),
            "adapter_budget_kind": results.get("adapter", {}).get("safe_budget_kind"),
            "adapter_extends_budget": (
                results.get("adapter", {}).get("safe_step_budget", -1) >=
                results.get("readout_only", {}).get("safe_step_budget", -1)
            ),
        },
        "verdict": verdict,
        "note": "SW-sim edge-learn (H_679 real); readout-only=H_861 edge, adapter=H_865 edge; "
                "crossing thr z_drop<1.0 frozen bf98c01; measurement rung; a_paper_negative_ok",
    }
    with open(os.path.join(args.out, "clm_forget_curve_result.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("[h875] wrote result json; verdict=%s" % verdict)
    print("=== H875 COMPLETE ===")


if __name__ == "__main__":
    main()
