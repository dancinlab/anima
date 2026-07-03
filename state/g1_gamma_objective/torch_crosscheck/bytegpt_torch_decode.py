#!/usr/bin/env python3
"""EXP-1 G1 torch CROSS-CHECK decoder (DIRECTIONAL, a_engine_native_learning).

Independent torch forward for the ByteGPT 303M .bin (5xu32 [vocab,d,L,H,block]
header, GPT-2-class: pre-LN, exact-erf GELU, tied-shape head). Reproduces the
numpy reference forward (state/g1_growwindow_remeasure/core/decode.py) with a
DIFFERENT compute stack (torch matmul / F.layer_norm / F.gelu) to test whether
the numpy FALSIFY (garbled, A.novel=0) is a numpy-decode artifact or a genuine
model property.

usage:
  python3 bytegpt_torch_decode.py <ckpt.bin> <jobs.tsv> <out.tsv> [greedy|sampled] [device]
jobs.tsv rows: seed_rng<TAB>tag<TAB>seed_text  (\t/\n free in seed)
out.tsv  rows: tag<TAB>text
"""
import sys, struct
import numpy as np
import torch
import torch.nn.functional as F

GEN, TOPK, TEMP = 40, 40, 0.7


def rd_u32(b, off):
    return struct.unpack_from('<I', b, off)[0]


def load(path, device, dtype=torch.float32):
    rb = open(path, 'rb').read()
    vocab = rd_u32(rb, 0); d = rd_u32(rb, 4); nlay = rd_u32(rb, 8)
    nh = rd_u32(rb, 12); block = rd_u32(rb, 16)
    off = [20]

    def rf(n, *shape):
        a = np.frombuffer(rb, dtype='<f4', count=n, offset=off[0]).astype(np.float32)
        off[0] += n * 4
        t = torch.from_numpy(a.copy()).to(device=device, dtype=dtype)
        return t.reshape(*shape) if shape else t

    W = {"vocab": vocab, "d": d, "nlay": nlay, "nh": nh, "block": block}
    W["tok"] = rf(vocab * d, vocab, d)
    W["pos"] = rf(block * d, block, d)
    for k in ("ln1w", "ln1b", "inW", "inB", "oW", "oB", "ln2w", "ln2b",
              "m0W", "m0B", "m2W", "m2B"):
        W[k] = []
    for _ in range(nlay):
        W["ln1w"].append(rf(d, d));              W["ln1b"].append(rf(d, d))
        W["inW"].append(rf(3 * d * d, 3 * d, d)); W["inB"].append(rf(3 * d, 3 * d))
        W["oW"].append(rf(d * d, d, d));          W["oB"].append(rf(d, d))
        W["ln2w"].append(rf(d, d));               W["ln2b"].append(rf(d, d))
        W["m0W"].append(rf(4 * d * d, 4 * d, d)); W["m0B"].append(rf(4 * d, 4 * d))
        W["m2W"].append(rf(d * 4 * d, d, 4 * d)); W["m2B"].append(rf(d, d))
    W["lnfw"] = rf(d, d); W["lnfb"] = rf(d, d)
    W["head"] = rf(vocab * d, vocab, d)
    assert off[0] == len(rb), "size mismatch %d != %d" % (off[0], len(rb))
    return W


@torch.no_grad()
def forward_last(W, ids):
    d = W["d"]; nlay = W["nlay"]; nh = W["nh"]; hd = d // nh
    T = len(ids)
    idt = torch.tensor(ids, dtype=torch.long, device=W["tok"].device)
    x = W["tok"][idt] + W["pos"][0:T]                                 # [T,d]
    scale = 1.0 / (hd ** 0.5)
    causal = torch.triu(torch.full((T, T), float('-inf'), device=x.device), 1)
    for L in range(nlay):
        nrm = F.layer_norm(x, (d,), W["ln1w"][L], W["ln1b"][L], 1e-5)
        qkv = nrm @ W["inW"][L].t() + W["inB"][L]                     # [T,3d]
        q, k, v = qkv[:, :d], qkv[:, d:2 * d], qkv[:, 2 * d:]
        q = q.view(T, nh, hd).transpose(0, 1)                        # [nh,T,hd]
        k = k.view(T, nh, hd).transpose(0, 1)
        v = v.view(T, nh, hd).transpose(0, 1)
        att = (q @ k.transpose(-2, -1)) * scale + causal            # [nh,T,T]
        att = F.softmax(att, dim=-1)
        ctx = (att @ v).transpose(0, 1).reshape(T, d)               # [T,d]
        x = x + (ctx @ W["oW"][L].t() + W["oB"][L])
        nrm = F.layer_norm(x, (d,), W["ln2w"][L], W["ln2b"][L], 1e-5)
        h4 = F.gelu(nrm @ W["m0W"][L].t() + W["m0B"][L])            # exact erf gelu
        x = x + (h4 @ W["m2W"][L].t() + W["m2B"][L])
    last = F.layer_norm(x[T - 1:T], (d,), W["lnfw"], W["lnfb"], 1e-5)[0]
    return W["head"] @ last                                          # [vocab]


def seed_to_ids(s):
    return list(s.encode('utf-8', 'surrogateescape'))


@torch.no_grad()
def decode(W, seed, gen, mode, seed_rng):
    block = W["block"]; vocab = W["vocab"]
    toks = seed_to_ids(seed)
    gen_t = torch.Generator(device='cpu'); gen_t.manual_seed(int(seed_rng))
    out = []
    for _ in range(gen):
        n = len(toks); start = n - block if n > block else 0
        logits = forward_last(W, toks[start:]).float().cpu()
        if mode == "greedy":
            nb = int(torch.argmax(logits).item())
        else:
            lg = logits / TEMP
            k = min(TOPK, vocab)
            topv, topi = torch.topk(lg, k)
            probs = F.softmax(topv, dim=-1)
            pick = torch.multinomial(probs, 1, generator=gen_t).item()
            nb = int(topi[pick].item())
        toks.append(nb); out.append(nb)
    return bytes(out).decode('utf-8', 'surrogateescape')


def main():
    ckpt, jobs, outp = sys.argv[1], sys.argv[2], sys.argv[3]
    mode = sys.argv[4] if len(sys.argv) > 4 else "sampled"
    dev = sys.argv[5] if len(sys.argv) > 5 else (
        "cuda" if torch.cuda.is_available() else "cpu")
    torch.set_grad_enabled(False)
    print("[torch] device=%s mode=%s ckpt=%s" % (dev, mode, ckpt), flush=True)
    W = load(ckpt, torch.device(dev))
    print("[torch] loaded vocab=%d d=%d L=%d H=%d block=%d" % (
        W["vocab"], W["d"], W["nlay"], W["nh"], W["block"]), flush=True)
    rows = []
    for line in open(jobs):
        line = line.rstrip("\n")
        if not line or line.count("\t") < 2:
            continue
        rng, tag, seed = line.split("\t", 2)
        rows.append((int(rng), tag, seed))
    with open(outp, "w", encoding="utf-8", errors="replace") as f:
        for i, (rng, tag, seed) in enumerate(rows):
            txt = decode(W, seed, GEN, mode, rng)
            f.write("%s\t%s\n" % (tag, txt.replace("\n", " ").replace("\t", " ")))
            f.flush()
            print("[%d/%d] %-11s :: %s" % (i + 1, len(rows), tag, txt[:70]), flush=True)
    print("[torch] wrote %s (%d rows)" % (outp, len(rows)), flush=True)


if __name__ == "__main__":
    main()
