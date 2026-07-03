#!/usr/bin/env python3
"""A11 CE-DELETED TPR-forward-slot trainer — the single UNBUILT G1-escape cell.

WIRE_SPEC v0.3 realization (state/g1_objfloor_escape/A11_engine_native/WIRE_SPEC.md):
  1) CE is DELETED (not added-to). The trunk is warm-FT'd end-to-end by a
     contrastive-replace InfoNCE (echo-A / echo-B / wrong-D hard negatives), the
     autoregressive byte-mouth analog of a11_natural.py::train_eval. NO full-vocab
     F.cross_entropy anywhere. Distinct from H_9120 (=ce + lambda*aux additive
     family, already FALSIFIED-CEILING).
  2) The readout is replaced by a multiplicative TPR role-filler binding slot:
     R=2 FIXED orthonormal roles (a balanced disjoint partition of d = the
     canonical orthonormal R=2 TPR slot), c_r = yn (Hadamard) roles[r],
     out[t] = sum_r S_r . (yn[t] (Hadamard) roles[r]). Warm-init reconstructs the
     base linear readout EXACTLY at step 0 (G0 preserved, no undertrain confound).
  3) Serialize to a v0.3 CLMT-trailer .clm (S_0 in the roW slot, roles + S_1 in a
     new "CLMT" ext-block; old golden .clm lack the tag => non-TPR path).

Warm base = clm303_clean (G0-green CLMConvMoE 303M: d3784/L4/E3/K3/V256).
Score = anima evaluate --py (torch-free numpy) G1.
"""
from __future__ import annotations
import argparse, json, os, sys, time, struct
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

_MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clmmodel")
sys.path.insert(0, _MODEL)
from model import CLMConfig, CLMConvMoE
import clm_serialize_v2 as SER


class TPRReadout(nn.Module):
    """out[v,t] = sum_r S_r[v,:] . (yn[:,t] (Hadamard) roles[r,:]).

    roles = R=2 FIXED orthonormal roles: a balanced disjoint partition of the d
    channels (role 0 owns half the dims scaled by sqrt(2), role 1 the other half).
    Disjoint support == orthonormal at R=2 (the a11 roles=eye(2) analog for a single
    autoregressive hidden). S_0,S_1 are the two learned signature projections."""
    def __init__(self, d, V, base_W, base_b, seed=0):
        super().__init__()
        self.d, self.V = d, V
        g = torch.Generator().manual_seed(seed)
        perm = torch.randperm(d, generator=g)
        half = d // 2
        m0 = torch.zeros(d); m1 = torch.zeros(d)
        s2 = float(np.sqrt(2.0))
        m0[perm[:half]] = s2
        m1[perm[half:]] = s2
        self.register_buffer("roles", torch.stack([m0, m1], 0))
        W = base_W.reshape(V, d).float().cpu()
        base_b = base_b.reshape(V).float().cpu()
        S0 = torch.zeros(V, d); S1 = torch.zeros(V, d)
        e = (m0 > 0); o = (m1 > 0)
        S0[:, e] = W[:, e] / s2
        S1[:, o] = W[:, o] / s2
        self.S0 = nn.Parameter(S0)
        self.S1 = nn.Parameter(S1)
        self.b0 = nn.Parameter(base_b.clone())
        self.b1 = nn.Parameter(torch.zeros(V))

    def forward(self, x):
        B, d, T = x.shape
        r0 = self.roles[0].view(1, d, 1); r1 = self.roles[1].view(1, d, 1)
        c0 = x * r0; c1 = x * r1
        out = torch.einsum('vd,bdt->bvt', self.S0, c0) + torch.einsum('vd,bdt->bvt', self.S1, c1)
        out = out + self.b0.view(1, self.V, 1) + self.b1.view(1, self.V, 1)
        return out


def torch_sd_from_clm(clm_path, core_dir):
    """Dequantize a serialized .clm (the DEPLOYED G0-green artifact) into a torch
    CLMConvMoE state_dict + (d,L,E,K). Warming from the .clm (not a mismatched .pt)
    guarantees the G0-green base (no undertrain confound). Conv weight inverse of
    clm_serialize_v2._conv_w_to_2d = plain reshape(cout,in,K)."""
    sys.path.insert(0, core_dir)
    import decode as D
    W = D.clm_load_weights(clm_path)
    d, E, V, K, L = W["d"], W["E"], W["V"], W["K"], W["L"]
    t = lambda a: torch.tensor(np.asarray(a), dtype=torch.float32)
    sd = {}
    sd["embed.weight"] = t(W["embed"])                                    # (V,d)
    sd["embed_conv.conv.weight"] = t(W["ecWt"].T).reshape(d, d, K)
    sd["embed_conv.conv.bias"] = t(W["ecB"])
    for l in range(L):
        sd[f"trunk.{l}.conv.conv.weight"] = t(W["tcWt"][l].T).reshape(d, d, K)
        sd[f"trunk.{l}.conv.conv.bias"] = t(W["tcB"][l])
        sd[f"trunk.{l}.norm.weight"] = t(W["tgG"][l])
        sd[f"trunk.{l}.norm.bias"] = t(W["tgB"][l])
    for e in range(E):
        sd[f"moe.experts.{e}.conv.conv.weight"] = t(W["eWt"][e].T).reshape(d, d, K)
        sd[f"moe.experts.{e}.conv.conv.bias"] = t(W["eB"][e])
    sd["moe.router.weight"] = t(W["rWt"].T).reshape(E, d, 1)
    sd["moe.router.bias"] = t(W["rB"])
    sd["norm_out.weight"] = t(W["noG"])
    sd["norm_out.bias"] = t(W["noB"])
    sd["readout.weight"] = t(W["roWt"].T).reshape(V, d, 1)
    sd["readout.bias"] = t(W["roB"])
    return sd, dict(d=d, L=L, E=E, K=K, V=V)


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
    """CE-DELETED contrastive-replace InfoNCE (echo-A/echo-B/wrong-D negatives).
    logits (B,V,T); pos=y[t]; negA=x[t] (echo current), negB=x[t-1] (echo prev),
    negD=random byte != pos. 4-way softmax, target col 0. NO full-vocab CE."""
    B, V, T = logits.shape
    lg = logits.permute(0, 2, 1).reshape(B*T, V)
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


def serialize_tpr(model, tpr, L, E, out_path):
    """v0.3 CLMT trailer: MAIN body = serialize_v3 with readout <- S_0; then append
    'CLMT' + R:u8 + roles ext (R*d f32) + S_1 conv block + S_1 bias ext."""
    d, V = tpr.d, tpr.V
    sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    sd["readout.weight"] = tpr.S0.detach().cpu().reshape(V, d, 1)
    sd["readout.bias"] = tpr.b0.detach().cpu()
    blob = SER._pack_main_blob(SER._resolve_state_dict(sd, None), L, E)
    CLMT = bytes([67, 76, 77, 84])
    blob += CLMT
    blob += struct.pack("<B", 2)
    roles = tpr.roles.detach().cpu().numpy().astype("<f4")
    blob += SER._pack_ext(roles)
    S1 = tpr.S1.detach().cpu().numpy().reshape(V, d)
    blob += SER._pack_conv_block(S1)
    blob += SER._pack_ext(tpr.b1.detach().cpu().numpy())
    with open(out_path, "wb") as f:
        f.write(blob)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-pt", default=None)
    ap.add_argument("--base-clm", default=None)
    ap.add_argument("--core-dir", default="/root/anima/core")
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--clm-out", required=True)
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
    print(f"=== A11 CE-DELETED TPR-slot train | device={device} torch={torch.__version__} ===", flush=True)

    if a.base_clm:
        sd, mc = torch_sd_from_clm(a.base_clm, a.core_dir)
        # variant="A" => SOFT expert mixture, byte-matching decode.py nn_moe_router_fwd
        # (the deployed scorer). variant AB's hard top-k would diverge train<->score.
        cfg = CLMConfig(d_model=mc["d"], n_trunk_layers=mc["L"], n_experts=mc["E"],
                        kernel_size=mc["K"], vocab_size=mc["V"], variant="A", grad_checkpoint=True)
        print(f"warm base from .clm {a.base_clm} cfg={mc}", flush=True)
    else:
        cfg = CLMConfig(d_model=3784, n_trunk_layers=4, n_experts=4, kernel_size=3,
                        vocab_size=256, variant="AB", grad_checkpoint=True)
        sd = torch.load(a.base_pt, map_location="cpu")
        if isinstance(sd, dict) and "model" in sd and "readout.weight" not in sd:
            sd = sd["model"]
    model = CLMConvMoE(cfg).to(device)
    missing, unexpected = model.load_state_dict(sd, strict=False)
    print(f"loaded base: missing={len(missing)} unexpected={len(unexpected)}", flush=True)
    L, E = cfg.n_trunk_layers, cfg.n_experts
    base_W = model.readout.weight.data.clone()
    base_b = model.readout.bias.data.clone()
    tpr = TPRReadout(cfg.d_model, cfg.vocab_size, base_W, base_b, seed=a.seed).to(device)
    model.readout = tpr

    stream = load_stream(a.corpus)
    n = stream.numel()
    train_stream = stream[: n - a.val_tail]
    val_stream = stream[n - a.val_tail:]
    print(f"corpus bytes={n} train={train_stream.numel()} val_tail={val_stream.numel()}", flush=True)

    model.eval()
    with torch.no_grad():
        xb, yb = make_batch(train_stream, 64, 2, device, torch.Generator().manual_seed(1))
        xe = model.embed(xb).transpose(1, 2); xe = model.embed_conv(xe)
        for layer in model.trunk: xe = layer(xe)
        xe, _ = model.moe(xe); xe = model.norm_out(xe)
        tpr_lg = tpr(xe)
        base_lg = F.conv1d(xe, base_W, base_b)
        recon = float((tpr_lg - base_lg).abs().max())
    print(f"[warm-init parity] max|TPR - base linear readout| = {recon:.3e} (expect ~0)", flush=True)

    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, betas=(0.9, 0.95), weight_decay=0.01)
    gen = torch.Generator().manual_seed(a.seed)
    dgen = torch.Generator(device=device).manual_seed(a.seed + 1)
    model.train()
    t0 = time.time(); losses = []
    for step in range(a.steps):
        xb, yb = make_batch(train_stream, a.seq_len, a.batch_size, device, gen)
        out = model(xb)
        logits = out["logits"]
        nce = infonce_loss(logits, xb, yb, dgen)
        aux = out.get("aux_loss", torch.zeros((), device=device))
        loss = nce + aux
        opt.zero_grad(set_to_none=True); loss.backward(); opt.step()
        if step % max(1, a.steps // 20) == 0 or step == a.steps - 1:
            losses.append((step, float(nce), float(aux)))
            print(f"  step {step:5d} infoNCE={float(nce):.4f} aux={float(aux):.4f} "
                  f"({(time.time()-t0):.0f}s)", flush=True)

    model.eval()
    with torch.no_grad():
        vnce = []
        vg = torch.Generator().manual_seed(999)
        vdg = torch.Generator(device=device).manual_seed(999)
        for _ in range(10):
            xb, yb = make_batch(val_stream, a.seq_len, a.batch_size, device, vg)
            out = model(xb); vnce.append(float(infonce_loss(out["logits"], xb, yb, vdg)))
        val_nce = float(np.mean(vnce))
    print(f"[held-out] mean InfoNCE = {val_nce:.4f}", flush=True)

    serialize_tpr(model, tpr, L, E, a.clm_out)
    print(f"[serialize] wrote {a.clm_out} ({os.path.getsize(a.clm_out)} bytes)", flush=True)

    if a.json_out:
        json.dump(dict(steps=a.steps, lr=a.lr, batch=a.batch_size, seq_len=a.seq_len,
                       warm_recon=recon, val_infonce=val_nce, losses=losses,
                       clm=a.clm_out, base=a.base_pt, corpus=a.corpus,
                       objective="CE-DELETED-InfoNCE(echoA/echoB/wrongD)+MoE-aux",
                       readout="TPR R=2 orthonormal-partition role-filler bind"),
                  open(a.json_out, "w"), indent=2)
    print("TRAIN_DONE", flush=True)


if __name__ == "__main__":
    main()
