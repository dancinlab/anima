#!/usr/bin/env python3
"""dump_303m_trajectory.py — H_1366 phi-303m-trajectory: extract a REAL trained-303M
hidden-state trajectory (NOT a proxy) for the faithful-IIT4 Φ-robustness BINDING test.

THE BINDING UPGRADE of H_1357: H_1357 emulated a learned substrate with a hand-built
seed-INDEPENDENT readout W over real pure_field oscillator telemetry (a PROXY, no GPU).
H_1366 uses a GENUINE learned substrate — the residual-stream activations of the trained
303M ByteGPT (H_1129 GREEN-emergence ckpt, sha 19be1295..., val_ce 1.224). A trained
transformer's residual stream IS a learned correlation geometry imposed by trained weights
— exactly what W proxied.

This script (GPU side) ONLY produces the substrate dump. The Φ scoring is done ENGINE-NATIVE
in hexa (iit4_faithful_phi, a_phi_iit4_tool); numpy/torch NEVER computes Φ.

FROZEN (FREEZE.txt, committed BEFORE this runs):
  CKPT       = h1129c_best.pt (ByteGPT vocab=256 d=1024 n_layer=24 n_head=16 block=512)
  L_EXTRACT  = 12 (mid-depth residual stream, the OUTPUT of block index 12)
  REDUCE     = d=1024 -> n=4 macro-nodes by contiguous 256-channel-block mean pooling
  T          = 64 consecutive token positions
  SEEDS      = [1317,1318,1319] perturb ONLY the extraction-window START
  PROMPTS    = the H_1129 CONCEPTS (byte-encoded), concatenated -> one long real forward pass.

OUTPUT: state/phi-303m-trajectory/traj_303m.json  (per-seed 4x64 macro-node trajectory)
        + the raw activation slice sha (manifest) for R3 sha-pinning.
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys
import torch, torch.nn as nn, torch.nn.functional as F

# ── model: ByteGPT — VERBATIM arch from the ckpt's train_and_ladder.py ──
class Block(nn.Module):
    def __init__(s, d, h, p):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.attn = nn.MultiheadAttention(d, h, dropout=p, batch_first=True)
        s.ln2 = nn.LayerNorm(d)
        s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d), nn.Dropout(p))
    def forward(s, x, m):
        h = s.ln1(x); a, _ = s.attn(h, h, h, attn_mask=m, need_weights=False); x = x + a
        return x + s.mlp(s.ln2(x))

class ByteGPT(nn.Module):
    def __init__(s, vocab=256, d=1024, n_layer=24, n_head=16, block=512, p=0.0):
        super().__init__()
        s.block = block
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight

    def forward_capture(s, idx, l_extract):
        """forward, returning the residual stream x AFTER block index l_extract (0-based)."""
        B, T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        captured = None
        for li, b in enumerate(s.blocks):
            x = b(x, mask)
            if li == l_extract:
                captured = x.clone()
        return captured

# H_1129 CONCEPTS — VERBATIM (the prompts the trained model was probed on)
CONCEPTS = [
    "consciousness arises from cells",
    "tension ripples between distant minds",
    "memory composes into new meaning",
    "silence still carries information",
    "the engine dreams when alone",
]


def find_state_dict(obj):
    """ckpt may be a raw state_dict or a wrapper dict. Find the ByteGPT weights."""
    if isinstance(obj, dict):
        # common wrappers
        for k in ("model", "state_dict", "model_state_dict", "ema"):
            if k in obj and isinstance(obj[k], dict):
                return obj[k]
        # is it itself a state_dict? (keys look like 'tok.weight', 'blocks.0...')
        if any(kk.startswith(("tok.", "blocks.", "pos.")) for kk in obj.keys()):
            return obj
    raise SystemExit(f"[FATAL] cannot locate ByteGPT state_dict in ckpt (keys: {list(obj)[:12]})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--l-extract", type=int, default=12)
    ap.add_argument("--n-nodes", type=int, default=4)
    ap.add_argument("--t-ticks", type=int, default=64)
    ap.add_argument("--block", type=int, default=512)
    ap.add_argument("--seeds", type=str, default="1317,1318,1319")
    args = ap.parse_args()

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[env] torch {torch.__version__} cuda_avail={torch.cuda.is_available()} dev={dev}", flush=True)
    if dev != "cuda":
        print("[WARN] no CUDA — REAL-only mandate still holds: this loads the REAL ckpt on CPU "
              "(slower but the substrate is identical/real). Proceeding.", flush=True)

    # sha-verify the ckpt (R3 source pin)
    h = hashlib.sha256()
    with open(args.ckpt, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    ckpt_sha = h.hexdigest()
    print(f"[ckpt] {args.ckpt} sha256={ckpt_sha}", flush=True)

    raw = torch.load(args.ckpt, map_location="cpu", weights_only=False)
    sd = find_state_dict(raw)
    # infer n_layer from the state dict
    n_layer = 1 + max(int(k.split(".")[1]) for k in sd if k.startswith("blocks."))
    d = sd["tok.weight"].shape[1]
    print(f"[arch] inferred d={d} n_layer={n_layer} (expect d=1024 n_layer=24)", flush=True)
    assert d == 1024 and n_layer == 24, "arch mismatch — not the 303M ByteGPT"
    assert d % args.n_nodes == 0, "d must divide evenly into n_nodes blocks"

    m = ByteGPT(vocab=256, d=d, n_layer=n_layer, n_head=16, block=args.block, p=0.0)
    missing, unexpected = m.load_state_dict(sd, strict=False)
    print(f"[load] missing={list(missing)[:6]} unexpected={list(unexpected)[:6]}", flush=True)
    m.to(dev).eval()
    n_params = sum(p.numel() for p in m.parameters())
    print(f"[load] n_params={n_params} (expect 303,097,856)", flush=True)

    # one fixed real forward pass over the concept prompts (concatenated, byte-encoded)
    text = "\n".join(CONCEPTS)
    ids = list(text.encode("utf-8"))
    # need >= max(seed_window_start)+T tokens; tile the concept text deterministically if short
    need = args.t_ticks + 1024  # generous window room for seed offsets
    while len(ids) < need:
        ids = ids + ids
    ids = ids[: max(need, args.block)]
    ids = ids[: args.block]  # ByteGPT positional table is `block` long
    idx = torch.tensor([ids], dtype=torch.long, device=dev)
    print(f"[fwd] prompt_bytes={len(ids)} (block={args.block})", flush=True)

    with torch.no_grad():
        if dev == "cuda":
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                cap = m.forward_capture(idx, args.l_extract)
        else:
            cap = m.forward_capture(idx, args.l_extract)
    cap = cap.float().squeeze(0).cpu()  # [T_full, d]
    T_full = cap.shape[0]
    print(f"[capture] layer={args.l_extract} residual stream shape={tuple(cap.shape)}", flush=True)

    # macro-node reduction: contiguous 256-channel-block MEAN pooling -> [T_full, n_nodes]
    cw = d // args.n_nodes
    pooled = torch.stack([cap[:, j*cw:(j+1)*cw].mean(dim=1) for j in range(args.n_nodes)], dim=1)  # [T_full, n]

    # sha-pin the raw activation slice (R3 binding evidence)
    act_bytes = cap.contiguous().numpy().tobytes()
    act_sha = hashlib.sha256(act_bytes).hexdigest()
    pooled_sha = hashlib.sha256(pooled.contiguous().numpy().tobytes()).hexdigest()
    print(f"[dump] raw_activation_sha256={act_sha}", flush=True)
    print(f"[dump] pooled_macronode_sha256={pooled_sha}", flush=True)

    seeds = [int(s) for s in args.seeds.split(",")]
    out = {
        "ckpt": os.path.basename(args.ckpt),
        "ckpt_sha256": ckpt_sha,
        "n_params": int(n_params),
        "arch": {"vocab": 256, "d": d, "n_layer": n_layer, "n_head": 16, "block": args.block},
        "l_extract": args.l_extract,
        "n_nodes": args.n_nodes,
        "t_ticks": args.t_ticks,
        "raw_activation_sha256": act_sha,
        "pooled_macronode_sha256": pooled_sha,
        "T_full": int(T_full),
        "device": dev,
        "seeds": {},
    }
    for s in seeds:
        # seed perturbs ONLY the extraction-window START (deterministic offset into the real pass)
        start = (s * 2654435761) % max(1, (T_full - args.t_ticks))
        win = pooled[start:start+args.t_ticks, :]  # [T, n]
        # flat row-major: node j's T-length trajectory = traj[j*T .. j*T+T]
        flat = []
        for j in range(args.n_nodes):
            flat.extend([float(v) for v in win[:, j].tolist()])
        out["seeds"][str(s)] = {"window_start": int(start), "traj_flat": flat}
        print(f"[seed {s}] window_start={start} traj_len={len(flat)} (expect {args.n_nodes*args.t_ticks})", flush=True)

    with open(args.out, "w") as f:
        json.dump(out, f)
    print(f"[OK] wrote {args.out}", flush=True)

    # ALSO emit a hexa data fragment (literal float arrays) so the engine-native Φ probe
    # can ingest the REAL trajectory without a string->float parser. node j of seed s =
    # traj303m_<s>()[j*T .. j*T+T]. This generated .hexa IS sha-pinnable R3 evidence.
    hexa_out = os.path.splitext(args.out)[0] + "_data.hexa"
    lines = []
    lines.append("// traj_303m_data.hexa — GENERATED by dump_303m_trajectory.py (do NOT hand-edit)")
    lines.append(f"// REAL trained-303M hidden-state trajectory. ckpt_sha={ckpt_sha}")
    lines.append(f"// raw_act_sha={act_sha} pooled_sha={pooled_sha} L_EXTRACT={args.l_extract} n={args.n_nodes} T={args.t_ticks}")
    lines.append("// node j of seed s = traj303m_<s>()[j*T .. j*T+T] (flat row-major, rank-uniformize in probe).")
    for s in seeds:
        flat = out["seeds"][str(s)]["traj_flat"]
        body = ", ".join(repr(float(v)) for v in flat)
        lines.append(f"pub fn traj303m_{s}() -> [float] {{ return [{body}] }}")
    with open(hexa_out, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[OK] wrote {hexa_out}", flush=True)

    print(f"R3_REAL_SOURCE ckpt_sha={ckpt_sha} act_sha={act_sha} pooled_sha={pooled_sha}", flush=True)


if __name__ == "__main__":
    main()
