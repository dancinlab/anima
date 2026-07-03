#!/usr/bin/env python3
"""A11 CE-DELETED TPR-forward-slot on the G0-GREEN ByteGPT h1129c trunk.

The CLM path proved the mechanism byte-exact but has NO G0-green base (clm303 is
sub-G0 under mouth-gen eval), so a CLM G1 number is INCONCLUSIVE (undertrain
confound). ByteGPT h1129c is the ONLY G0-green 303M trunk (prior RESULT 5/5), so
it is the valid substrate for the CE-deleted TPR forward-slot G1 determination.

Identical mechanism to the CLM trainer:
  - CE DELETED: contrastive-replace InfoNCE (echo-A/echo-B/wrong-D), NO full-V CE.
  - TPR readout: R=2 fixed orthonormal roles (disjoint partition), untied head
    S_0,S_1; out[t] = sum_r S_r . (ln_f(h)[t] (Hadamard) roles[r]). Warm-init
    reconstructs the tied head EXACTLY (G0 preserved).
Serialize: standard ByteGPT .bin (head <- S_0) + appended "BGT\\x01" trailer
(roles[R,d] + S_1[V,d], f32). decode.py bg readout gets the bind_type=3 branch.
"""
from __future__ import annotations
import argparse, json, os, sys, time, struct
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

_MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clmmodel")
sys.path.insert(0, _MODEL)
from bytegpt_model import ByteGPT, ByteGPTConfig
sys.path.insert(0, "/root/anima/core")
import serialize as BSER


def load_stream(path):
    raw = open(path, "rb").read()
    return torch.frombuffer(bytearray(raw), dtype=torch.uint8).long()


def make_batch(stream, seq_len, bs, device, gen):
    n = stream.numel()
    ix = torch.randint(0, n - seq_len - 1, (bs,), generator=gen)
    x = torch.stack([stream[i:i+seq_len] for i in ix]).to(device)
    y = torch.stack([stream[i+1:i+1+seq_len] for i in ix]).to(device)
    return x, y


def infonce_loss(logits, x, y, gen):
    """CE-DELETED contrastive-replace InfoNCE. logits (B,T,V)."""
    B, T, V = logits.shape
    lg = logits.reshape(B*T, V)
    pos = y.reshape(-1)
    eA = x.reshape(-1)
    xprev = torch.cat([x[:, :1], x[:, :-1]], 1)
    eB = xprev.reshape(-1)
    dD = torch.randint(0, V, (B*T,), generator=gen, device=logits.device)
    coll = (dD == pos)
    while coll.any():
        dD = torch.where(coll, torch.randint(0, V, (B*T,), generator=gen, device=logits.device), dD)
        coll = (dD == pos)
    idx = torch.arange(B*T, device=logits.device)
    z = torch.stack([lg[idx, pos], lg[idx, eA], lg[idx, eB], lg[idx, dD]], 1)
    tgt = torch.zeros(B*T, dtype=torch.long, device=logits.device)
    return F.cross_entropy(z, tgt)


class BGTPR(nn.Module):
    """ByteGPT trunk + TPR untied-head forward-slot."""
    def __init__(self, base: ByteGPT, seed=0):
        super().__init__()
        self.base = base
        d, V = base.cfg.d, base.cfg.vocab
        self.d, self.V = d, V
        g = torch.Generator().manual_seed(seed)
        perm = torch.randperm(d, generator=g); half = d // 2
        s2 = float(np.sqrt(2.0))
        m0 = torch.zeros(d); m1 = torch.zeros(d)
        m0[perm[:half]] = s2; m1[perm[half:]] = s2
        self.register_buffer("roles", torch.stack([m0, m1], 0))
        Wt = base.head.weight.data.clone().float().cpu()      # tied head (V,d)
        S0 = torch.zeros(V, d); S1 = torch.zeros(V, d)
        S0[:, m0 > 0] = Wt[:, m0 > 0] / s2
        S1[:, m1 > 0] = Wt[:, m1 > 0] / s2
        self.S0 = nn.Parameter(S0); self.S1 = nn.Parameter(S1)

    def forward(self, idx):
        h = self.base._penultimate(idx)                       # (B,T,d) post ln_f
        r0 = self.roles[0].view(1, 1, -1); r1 = self.roles[1].view(1, 1, -1)
        out = (h * r0) @ self.S0.t() + (h * r1) @ self.S1.t()  # (B,T,V)
        return out


def append_bgt(bin_path, roles, S1):
    with open(bin_path, "ab") as f:
        f.write(bytes([66, 71, 84, 1]))                        # "BGT\x01"
        f.write(struct.pack("<I", roles.shape[0]))             # R
        f.write(roles.astype("<f4").tobytes())                 # roles (R,d)
        f.write(S1.astype("<f4").tobytes())                    # S1 (V,d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-pt", required=True)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--bin-out", required=True)
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--seq-len", type=int, default=256)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--val-tail", type=int, default=155076)
    ap.add_argument("--json-out", default=None)
    a = ap.parse_args()
    torch.manual_seed(a.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"=== A11 CE-DELETED TPR-slot on ByteGPT h1129c | device={device} torch={torch.__version__} ===", flush=True)

    ck = torch.load(a.base_pt, map_location="cpu")
    cfgd = ck["config"] if isinstance(ck, dict) and "config" in ck else None
    sd = ck["model"] if isinstance(ck, dict) and "model" in ck else ck
    if cfgd is None:
        d = sd["ln_f.weight"].shape[0]; V = sd["tok.weight"].shape[0]
        L = len([k for k in sd if k.endswith("attn.in_proj_weight")])
        cfgd = dict(vocab=V, d=d, n_layer=L, n_head=d // 64, block=1024)
    cfg = ByteGPTConfig(**cfgd)
    print(f"cfg={cfgd}", flush=True)
    base = ByteGPT(cfg)
    miss, unexp = base.load_state_dict(sd, strict=False)
    print(f"loaded base: missing={len(miss)} unexpected={len(unexp)}", flush=True)
    model = BGTPR(base, seed=a.seed).to(device)

    # warm-init parity: TPR head == tied head at step0
    model.eval()
    with torch.no_grad():
        xb, _ = make_batch(load_stream(a.corpus), 64, 2, device, torch.Generator().manual_seed(1))
        h = model.base._penultimate(xb)
        tpr_lg = (h * model.roles[0].view(1, 1, -1)) @ model.S0.t() + (h * model.roles[1].view(1, 1, -1)) @ model.S1.t()
        base_lg = model.base.head(h)
        recon = float((tpr_lg - base_lg).abs().max())
    print(f"[warm-init parity] max|TPR - tied head| = {recon:.3e}", flush=True)

    stream = load_stream(a.corpus); n = stream.numel()
    train_stream = stream[: n - a.val_tail]; val_stream = stream[n - a.val_tail:]
    print(f"corpus bytes={n} train={train_stream.numel()} val_tail={val_stream.numel()}", flush=True)

    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, betas=(0.9, 0.95), weight_decay=0.01)
    gen = torch.Generator().manual_seed(a.seed)
    dgen = torch.Generator(device=device).manual_seed(a.seed + 1)
    model.train()
    t0 = time.time(); losses = []
    for step in range(a.steps):
        xb, yb = make_batch(train_stream, a.seq_len, a.batch_size, device, gen)
        logits = model(xb)
        nce = infonce_loss(logits, xb, yb, dgen)
        opt.zero_grad(set_to_none=True); nce.backward(); opt.step()
        if step % max(1, a.steps // 20) == 0 or step == a.steps - 1:
            losses.append((step, float(nce)))
            print(f"  step {step:5d} infoNCE={float(nce):.4f} ({(time.time()-t0):.0f}s)", flush=True)

    model.eval()
    with torch.no_grad():
        vg = torch.Generator().manual_seed(999); vdg = torch.Generator(device=device).manual_seed(999)
        vnce = [float(infonce_loss(model(make_batch(val_stream, a.seq_len, a.batch_size, device, vg)[0]),
                                   *make_batch(val_stream, a.seq_len, a.batch_size, device,
                                               torch.Generator().manual_seed(999))[:2], vdg)) for _ in range(6)]
        val_nce = float(np.mean(vnce))
    print(f"[held-out] mean InfoNCE ~ {val_nce:.4f}", flush=True)

    # serialize: write a .pt with head <- S_0 (untied), then serialize() -> .bin, append BGT.
    out_sd = {k: v.detach().cpu() for k, v in model.base.state_dict().items()}
    out_sd["head.weight"] = model.S0.detach().cpu()            # untied head = S_0
    tmp_pt = a.bin_out + ".tmp.pt"
    torch.save({"model": out_sd, "config": cfgd}, tmp_pt)
    BSER.serialize(tmp_pt, a.bin_out)
    append_bgt(a.bin_out, model.roles.detach().cpu().numpy(), model.S1.detach().cpu().numpy())
    os.remove(tmp_pt)
    print(f"[serialize] wrote {a.bin_out} ({os.path.getsize(a.bin_out)} bytes) + BGT trailer", flush=True)

    if a.json_out:
        json.dump(dict(steps=a.steps, lr=a.lr, batch=a.batch_size, warm_recon=recon,
                       val_infonce=val_nce, losses=losses, bin=a.bin_out, base=a.base_pt,
                       objective="CE-DELETED-InfoNCE(echoA/echoB/wrongD)",
                       readout="TPR R=2 orthonormal-partition role-filler bind (ByteGPT untied head)"),
                  open(a.json_out, "w"), indent=2)
    print("TRAIN_DONE", flush=True)


if __name__ == "__main__":
    main()
