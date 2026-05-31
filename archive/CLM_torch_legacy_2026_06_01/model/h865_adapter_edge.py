"""H_865 - trunk-adjacent adapter edge (the shared E5 fix for H_861/H_862 RED).

Re-runs BOTH falsifier sets (F-CLM-BOUND, F-CLM-ANCHOR) from the H_861/H_862
campaign, but replaces the readout-only edge with a THIN TRAINABLE ADAPTER
inserted between the FROZEN norm_out and a FROZEN base readout:

    norm_out (FROZEN) --> h --> h' = h + adapter(h) --> readout (FROZEN) --> logits

Why this gives the constraints a lever (the root cause both RED named):
  * H_861 readout-only: the readout is SHARED across the base byte band and the
    new-context high band; re-fitting it for the new band STEALS probability mass
    from the base band -> catastrophic forgetting (z_drop 1.984 >= 1.0).
    The adapter carries NEW-CONTEXT capacity in a SEPARATE additive path while
    the base readout mapping is PRESERVED (adapter zero-init -> identity at step
    0), so the base band is protected by construction.
  * H_862 anchor: model_psi probe reads norm_out, a FROZEN quantity in the
    readout-only edge -> the anchor Psi-penalty had ZERO grad path -> lambda
    on/off produced IDENTICAL trajectories (no lever). With the adapter, model_psi
    is computed from the ADAPTED h' which IS trainable -> the Psi-penalty now has
    a real grad lever -> on/off must differ.

W2 discipline: thresholds FROZEN VERBATIM from commit bf98c01. Same falsifiers,
NEW edge architecture -> thresholds unchanged, post-tuning = 0. A still-failing
gate is reported RED honestly (a_paper_negative_ok); no threshold may move.

SW-sim of the non-deterministic on-chip edge-learn is acceptable at the
measurement rung (a_scale_honest_scope); foundation H_679 established HW
edge-learn is real. Scope: MEASUREMENT rung (mid d512/L8/E8) only.
"""

from __future__ import annotations

import argparse
import glob
import json
import math
import os
import re
import sys

import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model import CLMConfig, CLMConvMoE  # noqa: E402

BASE_SEED = 101
NEW_SEED = 202
PROBE_SEED = 313
PSI_W_SEED = 31
N_ADAPT = 300
LR_EDGE = 3e-3
SEQ_LEN = 64
BATCH_SIZE = 16
N_EVAL_BATCHES = 32
LAMBDA_ANCHOR = 1.0
ADAPTER_RANK = 64

THR_Z_DROP = 1.0
THR_GAIN = 0.0
THR_D_ANCHOR_MAX = 0.50
THR_PROBE = 0.80


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
    def __init__(self, d_model, rank):
        super().__init__()
        self.down = nn.Conv1d(d_model, rank, kernel_size=1)
        self.act = nn.GELU()
        self.up = nn.Conv1d(rank, d_model, kernel_size=1)
        nn.init.zeros_(self.up.weight)
        nn.init.zeros_(self.up.bias)

    def forward(self, h):
        return h + self.up(self.act(self.down(h)))


class AdaptedCLM(nn.Module):
    def __init__(self, base):
        super().__init__()
        self.base = base
        for p in self.base.parameters():
            p.requires_grad_(False)
        self.adapter = AdapterEdge(base.cfg.d_model, ADAPTER_RANK)

    def trunk_norm_out(self, tokens):
        b = self.base
        x = b.embed(tokens).transpose(1, 2)
        x = b.embed_conv(x)
        for layer in b.trunk:
            x = layer(x)
        x, _ = b.moe(x)
        h = b.norm_out(x)
        return self.adapter(h)

    def forward(self, tokens, targets=None):
        hp = self.trunk_norm_out(tokens)
        logits = self.base.readout(hp)
        out = {"logits": logits, "hp": hp}
        if targets is not None:
            ce = F.cross_entropy(
                logits.transpose(1, 2).reshape(-1, self.base.cfg.vocab_size),
                targets.reshape(-1),
            )
            out["ce_loss"] = ce
        return out

    def id_hidden(self, tokens):
        hp = self.trunk_norm_out(tokens)
        return hp.mean(dim=(0, 2))


@torch.no_grad()
def eval_ce(model, batches):
    ces = []
    for toks, tgts in batches:
        out = model(toks, tgts)
        ces.append(out["ce_loss"].item())
    t = torch.tensor(ces)
    return t.mean().item(), t.std(unbiased=False).item()


def fixed_psi_W(d_model, device):
    g = torch.Generator(device="cpu").manual_seed(PSI_W_SEED)
    W = torch.randn(2, d_model, generator=g) / math.sqrt(d_model)
    return W.to(device)


def load_anchor_coords(anchor_dir):
    coords, payloads = [], []
    files = sorted(glob.glob(os.path.join(anchor_dir, "*.kosmos")))
    for fp in files:
        with open(fp, "r", errors="replace") as f:
            txt = f.read()
        c = _extract_coord(txt)
        if c is None:
            continue
        coords.append(c)
        payloads.append(_extract_payload(txt))
    return torch.tensor(coords, dtype=torch.float32), payloads


def _extract_coord(txt):
    m = re.search(r'coord["\s:=]*\[?\s*([-\d.eE]+)[\s,]+([-\d.eE]+)', txt)
    if m:
        return [float(m.group(1)), float(m.group(2))]
    return None


def _extract_payload(txt):
    # E-31 .kosmos: `@payload text := "..."` -- grab the text-modality payload
    m = re.search(r'@payload\s+text\s*:?=\s*"(.*?)"', txt, re.DOTALL)
    if m and m.group(1).strip():
        return m.group(1).strip()
    return txt


def build_identity_probe(payloads, seq_len, vocab=256):
    raw = []
    for p in payloads:
        raw.extend([b & 0xFF for b in p.encode("utf-8", errors="replace")])
        raw.append(0x0A)
    data = torch.tensor(raw, dtype=torch.long)
    n = len(payloads)
    if len(data) < seq_len + 1:
        data = data.repeat((seq_len + 1) // max(len(data), 1) + 1)
    step = max((len(data) - seq_len - 1) // max(n, 1), 1)
    win = []
    for i in range(n):
        s = min(i * step, len(data) - seq_len - 1)
        win.append(data[s:s + seq_len])
    return torch.stack(win)


def model_psi(model, W, probe_toks):
    h_id = model.id_hidden(probe_toks)
    return torch.sigmoid(W @ h_id)


def min_anchor_dist(psi, coords):
    d = torch.norm(coords - psi.unsqueeze(0), dim=1)
    return d.min()


@torch.no_grad()
def probe_dist(model, probe_toks):
    out = model(probe_toks)
    logits = out["logits"]
    return F.softmax(logits[:, :, -1], dim=1)


def js_divergence(p, q):
    m = 0.5 * (p + q)
    def kl(a, b):
        return (a * (torch.log(a + 1e-12) - torch.log(b + 1e-12))).sum(dim=1)
    js = 0.5 * kl(p, m) + 0.5 * kl(q, m)
    return (js / math.log(2)).clamp(0, 1)


def infer_config_and_load(ckpt_path):
    obj = torch.load(ckpt_path, map_location="cpu")
    if isinstance(obj, dict) and "state_dict" in obj:
        sd = obj["state_dict"]
        meta = obj.get("config") or obj.get("cfg") or {}
    elif isinstance(obj, dict) and any(k.startswith(("embed", "trunk", "moe", "readout")) for k in obj):
        sd = obj
        meta = {}
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


def run_bound(base, device):
    base_bytes = make_lane_bytes("web", 30000, BASE_SEED)
    new_bytes = make_lane_bytes("new", 30000, NEW_SEED)
    half = len(new_bytes) // 2
    base_eval = batchify(base_bytes, SEQ_LEN, N_EVAL_BATCHES, BATCH_SIZE, BASE_SEED)
    new_eval = batchify(new_bytes[half:], SEQ_LEN, N_EVAL_BATCHES, BATCH_SIZE, NEW_SEED + 1)
    new_train = batchify(new_bytes[:half], SEQ_LEN, N_ADAPT, BATCH_SIZE, NEW_SEED + 2)

    model = AdaptedCLM(base).to(device)
    model.eval()
    ce_base_pre, sd_base_pre = eval_ce(model, base_eval)
    ce_new_pre, _ = eval_ce(model, new_eval)

    opt = torch.optim.Adam(model.adapter.parameters(), lr=LR_EDGE)
    model.train()
    for i in range(N_ADAPT):
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
        "hypothesis": "H_865 F-CLM-BOUND (adapter edge)",
        "rung": "mid d512/L8/E8",
        "edge": "trunk-adjacent adapter (norm_out + adapter) -> FROZEN readout; rank=%d" % ADAPTER_RANK,
        "ce_base_pre": round(ce_base_pre, 5), "sd_base_pre": round(sd_base_pre, 5),
        "ce_base_post": round(ce_base_post, 5),
        "ce_new_pre": round(ce_new_pre, 5), "ce_new_post": round(ce_new_post, 5),
        "z_drop": round(z_drop, 5), "gain": round(gain, 5),
        "threshold_z_drop": "<1.0", "threshold_gain": ">0.0",
        "RETAIN_pass": bool(z_drop < THR_Z_DROP),
        "GAIN_pass": bool(gain > THR_GAIN),
        "verdict": "GREEN" if (z_drop < THR_Z_DROP and gain > THR_GAIN) else "RED",
        "note": "SW-sim edge-learn (H_679 real); adapter carries new-context in separate path, base readout FROZEN; measurement rung; frozen thr bf98c01",
    }


def run_anchor(base, anchor_dir, device, lam):
    coords, payloads = load_anchor_coords(anchor_dir)
    coords = coords.to(device)
    n_anchors = coords.shape[0]
    probe_toks = build_identity_probe(payloads, SEQ_LEN).to(device)
    new_bytes = make_lane_bytes("new", 30000, NEW_SEED)
    new_train = batchify(new_bytes[:len(new_bytes) // 2], SEQ_LEN, N_ADAPT, BATCH_SIZE, NEW_SEED + 2)

    model = AdaptedCLM(base).to(device)
    W = fixed_psi_W(base.cfg.d_model, device)
    model.eval()
    with torch.no_grad():
        psi_pre = model_psi(model, W, probe_toks)
        d_pre = min_anchor_dist(psi_pre, coords).item()
        p_pre = probe_dist(model, probe_toks)

    opt = torch.optim.Adam(model.adapter.parameters(), lr=LR_EDGE)
    d_traj = [d_pre]
    model.train()
    for i in range(N_ADAPT):
        toks, tgts = new_train[i]
        toks, tgts = toks.to(device), tgts.to(device)
        out = model(toks, tgts)
        task = out["ce_loss"]
        psi = model_psi(model, W, probe_toks)
        d_anchor = min_anchor_dist(psi, coords)
        loss = task + lam * d_anchor
        opt.zero_grad()
        loss.backward()
        opt.step()
        d_traj.append(d_anchor.item())
    model.eval()
    with torch.no_grad():
        psi_post = model_psi(model, W, probe_toks)
        d_post = min_anchor_dist(psi_post, coords).item()
        p_post = probe_dist(model, probe_toks)
        consistency = (1.0 - js_divergence(p_pre, p_post)).mean().item()
    return {
        "lambda": lam, "n_anchors": n_anchors,
        "d_anchor_pre": round(d_pre, 5), "d_anchor_post": round(d_post, 5),
        "d_anchor_max": round(max(d_traj), 5),
        "probe_consistency": round(consistency, 5),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--anchors", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(0)
    os.makedirs(args.out, exist_ok=True)

    base, cfg, missing, unexpected, _ = infer_config_and_load(args.ckpt)
    base = base.to(device)
    print("[h865] loaded backbone d=%d L=%d E=%d V=%d params=%d device=%s" % (
        cfg.d_model, cfg.n_trunk_layers, cfg.n_experts, cfg.vocab_size,
        base.num_params(), device))
    print("[h865] load missing=%s unexpected=%s" % (missing, unexpected))

    bound = run_bound(base, device)
    print("[h865 BOUND]", json.dumps(bound))

    on = run_anchor(base, args.anchors, device, LAMBDA_ANCHOR)
    off = run_anchor(base, args.anchors, device, 0.0)
    on_off_identical = (
        abs(on["d_anchor_max"] - off["d_anchor_max"]) < 1e-6 and
        abs(on["probe_consistency"] - off["probe_consistency"]) < 1e-6
    )
    DIST_pass = on["d_anchor_max"] < THR_D_ANCHOR_MAX
    PROBE_pass = on["probe_consistency"] > THR_PROBE
    anchor_verdict = "GREEN" if (DIST_pass and PROBE_pass and not on_off_identical) else "RED"
    anchor = {
        "hypothesis": "H_865 F-CLM-ANCHOR (adapter edge)",
        "rung": "mid d512/L8/E8",
        "edge": "adapter gives Psi-penalty a grad lever (model_psi from ADAPTED norm_out)",
        "n_anchors": on["n_anchors"], "lambda_on": LAMBDA_ANCHOR,
        "on_d_anchor_pre": on["d_anchor_pre"], "on_d_anchor_post": on["d_anchor_post"],
        "on_d_anchor_max": on["d_anchor_max"], "on_probe_consistency": on["probe_consistency"],
        "off_d_anchor_pre": off["d_anchor_pre"], "off_d_anchor_post": off["d_anchor_post"],
        "off_d_anchor_max": off["d_anchor_max"], "off_probe_consistency": off["probe_consistency"],
        "on_off_identical": bool(on_off_identical),
        "threshold_d_anchor_max": "<0.50", "threshold_probe_consistency": ">0.80",
        "DIST_pass": bool(DIST_pass), "PROBE_pass": bool(PROBE_pass),
        "lever_present": bool(not on_off_identical),
        "verdict": anchor_verdict,
        "note": "SW-sim edge-learn (H_679 real); adapter -> Psi-probe lever; E2 on/off ablation must be NON-identical; frozen thr bf98c01",
    }
    print("[h865 ANCHOR]", json.dumps(anchor))

    result = {
        "campaign": "H_865 trunk-adjacent adapter edge (E5 fix for H_861/H_862)",
        "frozen_thresholds_commit": "bf98c01",
        "adapter_rank": ADAPTER_RANK,
        "BOUND": bound, "ANCHOR": anchor,
        "headline": {
            "BOUND_closed": bound["verdict"] == "GREEN",
            "ANCHOR_closed": anchor["verdict"] == "GREEN",
        },
    }
    with open(os.path.join(args.out, "clm_adapter_edge_result.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("[h865] wrote result json")
    print("=== H865 COMPLETE ===")


if __name__ == "__main__":
    main()
