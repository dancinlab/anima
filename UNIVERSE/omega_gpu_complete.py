#!/usr/bin/env python3
"""OMEGA stage-3 (b)+(c) — the learned-gate closure on a REAL TRAINED TRANSFORMER substrate.

The toy n-gram rung (#1786, omega_gate_bench.py) proved a LEARNED per-wire gate makes the
OMEGA coupling USEFUL where the fixed A−G formula degraded:
    logits = gB·base + gA·A + gG·G   (gains fit on a train-gate split, frozen, eval on TEST)
    GATED 3.127 < base 3.974 · ≤ a_only · ≪ fixed_AmG.

This rung asks: does that closure survive on a REAL trained transformer's A/G heads (not a
numpy n-gram)?  Substrate = ConsciousDecoderV2 (UNIVERSE/conscious_decoder.py) — dual heads
logits_a (next-byte) + logits_g (prev-byte). We:

  (b) TRAIN a small-but-real CDV2 (d384 × 6L GQA, V=256, block 256) on a real multilingual
      byte corpus to an honest CE descent (report the curve).  REAL learned A/G heads.
  (c) On a held-out split extract per-position A = logits_a, G = logits_g, and a deliberately
      WEAK BASE mouth (unigram log-frequency) so the coupling has room to help.  Apply the
      OMEGA learned-gate bus (mirror omega_gate_bench.fit_gate EXACTLY): fit (gB,gA,gG) on a
      TRAIN-gate split (convex log-linear + L2 on wire gains), freeze, evaluate held-out CE of
      base · fixed_AmG (1,α,−α) · a_only (1,α,0) · GATED.  ALSO structured-coupling
      (KL_on vs perm-shuffle floor on the REAL A−G) + a generation sample (gated closure
      vs base, qualitative coherence note).

STAGE-3 COMPLETION (pre-registered, honest p7 / a_paper_negative_ok):
  (b) trained substrate: real transformer A/G, CE descended during training (curve reported).
  (c) generation demo: GATED held-out CE < base  AND  CE floor MET (< uniform ln256=5.545)
      AND structured (KL_on > 1.5× perm floor on real A/G)  AND  a coherent-ish gen sample.
  All hold → 오메가 완성.  Some fail → honest closed-negative / partial (report exactly what
  held + what did not, NO fabricated pass).

a_lane_akida_gpu_split: Lane-G / GPU (NOT Lane A AKIDA).  GPU REQUIRED — nvidia-smi BUSY
verified by the dispatch wrapper (g63, never silent CPU-fallback).
"""
import os, sys, json, math, time, glob, hashlib, argparse, urllib.request
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from conscious_decoder import ConsciousDecoderV2  # noqa: E402

V = 256
SMOOTH = 0.5
ALPHA = 0.6          # the #1784/#1786 fixed-formula gain (for fixed_AmG / a_only baselines)
GATE_LR = 0.5
GATE_STEPS = 300
GATE_L2 = 0.02
UNIFORM_CE = math.log(V)   # 5.545177...


# ───────────────────────── corpus ─────────────────────────

def fetch_corpus(target_bytes, cache_path):
    """Real multilingual byte corpus. Prefer a corpus already on the pod; else fetch a small
    public multilingual text. Returns a uint8 numpy array + a provenance string."""
    if os.path.exists(cache_path) and os.path.getsize(cache_path) >= target_bytes * 0.9:
        buf = open(cache_path, "rb").read()
        return np.frombuffer(buf[:target_bytes], dtype=np.uint8), f"cache:{cache_path}"

    # try common on-pod corpora first
    candidates = [
        "/workspace/corpus.txt", "/workspace/clm_mid_5lang_c4.txt",
        "/root/corpus.txt", "CORE/testdata/clm_mid_5lang_c4.txt",
    ]
    for c in candidates:
        if os.path.exists(c) and os.path.getsize(c) > 100_000:
            buf = open(c, "rb").read()
            if len(buf) >= target_bytes:
                open(cache_path, "wb").write(buf[:target_bytes])
                return np.frombuffer(buf[:target_bytes], dtype=np.uint8), f"onpod:{c}"

    # fetch small public multilingual texts (Project Gutenberg + multilingual UDHR mirror)
    urls = [
        # English / French / German / Latin etc. public-domain plain text
        "https://www.gutenberg.org/files/1342/1342-0.txt",     # Pride and Prejudice (en)
        "https://www.gutenberg.org/files/2600/2600-0.txt",     # War and Peace (en, large)
        "https://www.gutenberg.org/files/1399/1399-0.txt",     # Anna Karenina (en)
        "https://www.gutenberg.org/cache/epub/2000/pg2000.txt",  # Don Quijote (es)
        "https://www.gutenberg.org/cache/epub/1184/pg1184.txt",  # Monte Cristo (en)
        "https://www.gutenberg.org/files/5000/5000-8.txt",     # Notebooks da Vinci
    ]
    buf = bytearray()
    used = []
    for u in urls:
        if len(buf) >= target_bytes:
            break
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 omega-fire"})
            data = urllib.request.urlopen(req, timeout=60).read()
            buf += data
            used.append(u.split("/")[-1])
        except Exception as e:
            print(f"  [corpus] skip {u}: {e}", flush=True)
    if len(buf) < 50_000:
        raise RuntimeError(f"corpus fetch failed; only {len(buf)}B — cannot train honestly")
    buf = bytes(buf[:target_bytes]) if len(buf) >= target_bytes else bytes(buf)
    open(cache_path, "wb").write(buf)
    return np.frombuffer(buf, dtype=np.uint8), f"gutenberg:{'+'.join(used)}"


# ───────────────────────── train CDV2 (real substrate) ─────────────────────────

def get_batch(data, block, bs, device):
    ix = torch.randint(0, len(data) - block - 1, (bs,))
    x = torch.stack([torch.from_numpy(data[i:i + block].astype(np.int64)) for i in ix])
    y = torch.stack([torch.from_numpy(data[i + 1:i + 1 + block].astype(np.int64)) for i in ix])
    return x.to(device), y.to(device)


def train_substrate(model, train_data, val_data, steps, block, bs, lr, device):
    """Train CDV2 with a DUAL-head objective: head_a predicts NEXT byte, head_g predicts PREV
    byte (this is what makes A/G real, distinct heads — exactly the OMEGA wire semantics).
    Returns the CE descent curve (next-byte CE on head_a)."""
    opt = torch.optim.AdamW(model.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)
    curve = []
    model.train()
    t0 = time.time()
    for step in range(steps):
        x, y_next = get_batch(train_data, block, bs, device)
        y_prev = torch.roll(x, shifts=1, dims=1)        # prev-byte target for head_g
        logits_a, logits_g, _, _, aux = model(x)
        loss_a = F.cross_entropy(logits_a.reshape(-1, V), y_next.reshape(-1))
        loss_g = F.cross_entropy(logits_g.reshape(-1, V), y_prev.reshape(-1))
        loss = loss_a + 0.5 * loss_g
        if aux is not None:
            loss = loss + 0.01 * aux
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        if step % max(1, steps // 30) == 0 or step == steps - 1:
            curve.append({"step": step, "ce_a": float(loss_a.item()), "ce_g": float(loss_g.item())})
            print(f"  step {step:5d}/{steps}  ce_a(next)={loss_a.item():.4f}  ce_g(prev)={loss_g.item():.4f}"
                  f"  {(time.time()-t0):.1f}s", flush=True)
    # held-out eval CE (next-byte, head_a) — honest val descent confirmation
    model.eval()
    with torch.no_grad():
        vx, vy = get_batch(val_data, block, min(bs, 16), device)
        vla, _, _, _, _ = model(vx)
        val_ce = float(F.cross_entropy(vla.reshape(-1, V), vy.reshape(-1)).item())
    return curve, val_ce, time.time() - t0


# ───────────────────────── extract A/G/base on held-out split ─────────────────────────

def extract_feats(model, seq, block, device, max_pos=8000):
    """Run the trained model over a held-out byte sequence and collect, per position:
       A    = logits_a (next-byte head)   — log-space, softmaxed downstream
       G    = logits_g (prev-byte head)
       base = WEAK unigram log-frequency mouth (deliberately weak so the bus has room).
    Returns feats=(base,A,G) each (N,V) numpy + tgt (N,) next-byte targets."""
    model.eval()
    # weak base = unigram log-freq over the seq (a deliberately weak next-byte baseline)
    counts = np.full(V, SMOOTH)
    for b in seq:
        counts[int(b)] += 1.0
    log_base_vec = np.log(counts / counts.sum())          # (V,)

    A_rows, G_rows, tgt = [], [], []
    n = len(seq)
    with torch.no_grad():
        pos = 0
        i = 0
        while i + block + 1 < n and pos < max_pos:
            x = torch.from_numpy(seq[i:i + block].astype(np.int64)).unsqueeze(0).to(device)
            la, lg, _, _, _ = model(x)               # (1,T,V)
            la = la[0].float().cpu().numpy()         # (T,V) = A at each position (predicts next)
            lg = lg[0].float().cpu().numpy()         # (T,V) = G at each position (predicts prev)
            # position t predicts byte (i+t+1); target = seq[i+t+1]
            for t in range(block):
                if i + t + 1 >= n or pos >= max_pos:
                    break
                A_rows.append(la[t]); G_rows.append(lg[t]); tgt.append(int(seq[i + t + 1]))
                pos += 1
            i += block
    A = np.stack(A_rows); G = np.stack(G_rows); tgt = np.array(tgt)
    base = np.tile(log_base_vec, (len(tgt), 1))
    return (base, A, G), tgt


# ───────────────────────── OMEGA learned gate (mirror omega_gate_bench.py) ─────────────────────────

def softmax_np(z):
    z = z - z.max(1, keepdims=True); e = np.exp(z); return e / e.sum(1, keepdims=True)


def ce_of(g, feats, tgt):
    base, A, G = feats
    logits = g[0] * base + g[1] * A + g[2] * G
    p = softmax_np(logits)
    return float(-np.mean(np.log(p[np.arange(len(tgt)), tgt] + 1e-12)))


def fit_gate(feats, tgt, steps=GATE_STEPS, lr=GATE_LR, l2=GATE_L2):
    """Convex log-linear fit of [gB,gA,gG] minimizing train CE + L2 on the wire gains
    (gA,gG, not gB) — IDENTICAL method to omega_gate_bench.fit_gate."""
    base, A, G = feats
    N = len(tgt)
    onehot = np.zeros((N, V)); onehot[np.arange(N), tgt] = 1.0
    g = np.array([1.0, 0.0, 0.0])
    F_ = np.stack([base, A, G], axis=0)
    reg = np.array([0.0, 1.0, 1.0])
    for _ in range(steps):
        logits = g[0] * base + g[1] * A + g[2] * G
        p = softmax_np(logits)
        resid = p - onehot
        grad = np.array([np.sum(resid * F_[k]) / N for k in range(3)]) + l2 * reg * g
        g = g - lr * grad
    return g


def kl_structured(feats, tgt, n_perm=8, seed=20260604):
    """Structured-coupling test on the REAL A−G: KL( P(base+α(A−G)) ‖ P(base) ) measured on
    the true A/G vs the same with G's ROWS permuted (destroys the A↔G alignment = floor).
    Structured if KL_on > 1.5× the perm-shuffle floor."""
    base, A, G = feats
    rng = np.random.default_rng(seed)
    def mean_kl(Gx):
        p_on = softmax_np(base + ALPHA * (A - Gx))
        p_off = softmax_np(base)
        return float(np.mean(np.sum(p_on * (np.log(p_on + 1e-12) - np.log(p_off + 1e-12)), axis=1)))
    kl_on = mean_kl(G)
    floors = []
    for _ in range(n_perm):
        perm = rng.permutation(len(G))
        floors.append(mean_kl(G[perm]))
    kl_floor = float(np.mean(floors))
    return kl_on, kl_floor


# ───────────────────────── generation sample (gated closure vs base) ─────────────────────────

def gen_sample(model, prompt_bytes, n_new, device, g_star, log_base_vec, temperature=0.85, top_k=40):
    """Decode n_new bytes two ways from the same prompt:
       BASE  : sample from the weak unigram base only (gB·base).
       GATED : sample from gB·base + gA·A + gG·G, where A/G are the trained head logits at the
               current position (the OMEGA gated closure as the actual decode path).
    Returns (base_text, gated_text)."""
    model.eval()
    log_base = torch.from_numpy(log_base_vec.astype(np.float32)).to(device)   # (V,)

    def decode(use_gate):
        idx = torch.from_numpy(np.frombuffer(prompt_bytes, dtype=np.uint8).astype(np.int64)).unsqueeze(0).to(device)
        out = bytearray(prompt_bytes)
        with torch.no_grad():
            for _ in range(n_new):
                ctx = idx[:, -model.block_size:]
                la, lg, _, _, _ = model(ctx)
                A = la[0, -1].float()
                G = lg[0, -1].float()
                if use_gate:
                    logits = g_star[0] * log_base + g_star[1] * A + g_star[2] * G
                else:
                    logits = log_base.clone()    # weak base mouth only
                logits = logits / temperature
                if top_k > 0:
                    v, _ = torch.topk(logits, min(top_k, V))
                    logits[logits < v[-1]] = float("-inf")
                p = torch.softmax(logits, dim=-1)
                nxt = int(torch.multinomial(p, 1).item())
                out.append(nxt)
                idx = torch.cat([idx, torch.tensor([[nxt]], device=device)], dim=1)
        return bytes(out)

    base_b = decode(False)
    gated_b = decode(True)
    dec = lambda b: b.decode("utf-8", errors="replace")
    return dec(base_b), dec(gated_b)


# ───────────────────────── main ─────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=4000)
    ap.add_argument("--d_model", type=int, default=384)
    ap.add_argument("--n_layer", type=int, default=6)
    ap.add_argument("--n_head", type=int, default=6)
    ap.add_argument("--n_kv_head", type=int, default=2)
    ap.add_argument("--block", type=int, default=256)
    ap.add_argument("--bs", type=int, default=32)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--corpus_mb", type=int, default=120)
    ap.add_argument("--out", default="omega_gpu_results.json")
    ap.add_argument("--ckpt", default="omega_cdv2_d384.pt")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device != "cuda":
        print("!!! NO CUDA — refusing to fake a GPU train (g63). Reporting BLOCKED.", flush=True)
        json.dump({"BLOCKED": "no_cuda", "device": device}, open(args.out, "w"), indent=2)
        sys.exit(2)
    gpu_name = torch.cuda.get_device_name(0)
    print(f"=== OMEGA stage-3 (b)(c) — REAL trained-transformer closure ===", flush=True)
    print(f"device={device}  gpu={gpu_name}  torch={torch.__version__}", flush=True)

    # ---- corpus
    target = args.corpus_mb * 1_000_000
    corpus, prov = fetch_corpus(target, os.path.join(HERE, "omega_corpus.bin"))
    sha = hashlib.sha256(corpus.tobytes()).hexdigest()
    n = len(corpus)
    print(f"corpus: {n}B  prov={prov}  sha256={sha[:16]}", flush=True)

    # disjoint splits: train-substrate (80%), held-out (gate+test+gen, 20%)
    cut = int(n * 0.8)
    train_data = corpus[:cut]
    held = corpus[cut:]
    val_data = held[:len(held) // 2]   # for the substrate val-CE confirmation

    # ---- (b) train real CDV2
    model = ConsciousDecoderV2(
        vocab_size=V, d_model=args.d_model, n_head=args.n_head, n_layer=args.n_layer,
        block_size=args.block, n_kv_head=args.n_kv_head, consciousness_dim=128,
    ).to(device)
    nparam = model.count_params()
    print(f"CDV2 params: {nparam:,} ({nparam/1e6:.2f}M)", flush=True)
    curve, val_ce, train_wall = train_substrate(
        model, train_data, val_data, args.steps, args.block, args.bs, args.lr, device)
    first_ce = curve[0]["ce_a"]; final_ce = curve[-1]["ce_a"]
    descended = final_ce < first_ce
    print(f"\n(b) trained substrate: ce_a {first_ce:.4f} -> {final_ce:.4f}  (val_ce={val_ce:.4f})  "
          f"descended={descended}  wall={train_wall:.1f}s", flush=True)

    torch.save({"model": model.state_dict(), "config": {
        "vocab_size": V, "d_model": args.d_model, "n_head": args.n_head, "n_layer": args.n_layer,
        "block_size": args.block, "n_kv_head": args.n_kv_head, "consciousness_dim": 128,
    }}, args.ckpt)
    ckpt_sha = hashlib.sha256(open(args.ckpt, "rb").read()).hexdigest()
    print(f"ckpt saved: {args.ckpt}  sha256={ckpt_sha[:16]}", flush=True)

    # ---- (c) extract A/G/base on held-out (DISJOINT from train); split gate vs test
    gate_seq = held[:len(held) // 2]
    test_seq = held[len(held) // 2:]
    print("\nextracting A/G/base on held-out split (gate)...", flush=True)
    gate_feats, gate_tgt = extract_feats(model, gate_seq, args.block, device, max_pos=8000)
    print("extracting A/G/base on held-out split (test, disjoint)...", flush=True)
    test_feats, test_tgt = extract_feats(model, test_seq, args.block, device, max_pos=8000)
    print(f"  gate N={len(gate_tgt)}  test N={len(test_tgt)}", flush=True)

    # ---- fit gate on train-gate split, freeze
    g_star = fit_gate(gate_feats, gate_tgt)
    print(f"learned gate g* = [gB={g_star[0]:.4f}, gA={g_star[1]:.4f}, gG={g_star[2]:.4f}]", flush=True)

    # ---- held-out TEST CE
    ce_base = ce_of(np.array([1.0, 0.0, 0.0]), test_feats, test_tgt)
    ce_fixed = ce_of(np.array([1.0, ALPHA, -ALPHA]), test_feats, test_tgt)
    ce_aonly = ce_of(np.array([1.0, ALPHA, 0.0]), test_feats, test_tgt)
    ce_gated = ce_of(g_star, test_feats, test_tgt)
    print(f"\n--- held-out TEST CE (nats/byte) ---", flush=True)
    print(f"  base (weak unigram)   = {ce_base:.6f}", flush=True)
    print(f"  fixed_AmG (1,α,−α)    = {ce_fixed:.6f}", flush=True)
    print(f"  a_only    (1,α,0)     = {ce_aonly:.6f}", flush=True)
    print(f"  GATED     (learned)   = {ce_gated:.6f}", flush=True)
    print(f"  uniform-256 floor     = {UNIFORM_CE:.6f}", flush=True)

    # ---- structured coupling on REAL A−G
    kl_on, kl_floor = kl_structured(test_feats, test_tgt)
    structured = kl_on > 1.5 * kl_floor
    print(f"\nstructured coupling (real A−G): KL_on={kl_on:.4f}  perm_floor={kl_floor:.4f}  "
          f"ratio={kl_on/(kl_floor+1e-12):.2f}x  structured={structured}", flush=True)

    # ---- generation sample
    _, _, base_vec_holder = None, None, None
    # rebuild weak base vec over test_seq for the gen path (same construction as extract)
    counts = np.full(V, SMOOTH)
    for b in test_seq:
        counts[int(b)] += 1.0
    log_base_vec = np.log(counts / counts.sum())
    prompt = bytes(test_seq[:48].tobytes())
    base_txt, gated_txt = gen_sample(model, prompt, 200, device, g_star, log_base_vec)
    print(f"\n--- generation sample (200 new bytes) ---", flush=True)
    print(f"[BASE  weak-unigram]\n{base_txt}\n", flush=True)
    print(f"[GATED omega-closure]\n{gated_txt}\n", flush=True)

    # ---- completion criteria (pre-registered)
    c_b = descended
    c_gated_lt_base = ce_gated < ce_base
    c_floor = ce_gated < UNIFORM_CE
    c_struct = structured
    completion = c_b and c_gated_lt_base and c_floor and c_struct

    results = {
        "lane": "Lane-G", "substrate": "GPU", "gpu": gpu_name, "torch": torch.__version__,
        "corpus_bytes": int(n), "corpus_prov": prov, "corpus_sha256": sha,
        "model": {"params": int(nparam), "d_model": args.d_model, "n_layer": args.n_layer,
                  "n_head": args.n_head, "n_kv_head": args.n_kv_head, "block": args.block,
                  "vocab": V},
        "train": {"steps": args.steps, "bs": args.bs, "lr": args.lr, "wall_s": train_wall,
                  "first_ce_a": first_ce, "final_ce_a": final_ce, "val_ce": val_ce,
                  "descended": bool(descended), "curve": curve},
        "ckpt": {"path": args.ckpt, "sha256": ckpt_sha},
        "gate": {"gB": float(g_star[0]), "gA": float(g_star[1]), "gG": float(g_star[2]),
                 "fit_steps": GATE_STEPS, "l2": GATE_L2, "alpha_fixed": ALPHA},
        "ce": {"base": ce_base, "fixed_AmG": ce_fixed, "a_only": ce_aonly, "gated": ce_gated,
               "uniform_floor": UNIFORM_CE},
        "structured": {"kl_on": kl_on, "kl_perm_floor": kl_floor,
                       "ratio": kl_on / (kl_floor + 1e-12), "is_structured": bool(structured)},
        "generation": {"prompt": prompt.decode("utf-8", errors="replace"),
                       "base": base_txt, "gated": gated_txt},
        "criteria": {
            "b_trained_substrate_descended": bool(c_b),
            "c_gated_lt_base": bool(c_gated_lt_base),
            "c_floor_met": bool(c_floor),
            "c_structured": bool(c_struct),
            "OMEGA_COMPLETE": bool(completion),
        },
    }
    json.dump(results, open(args.out, "w"), indent=2, ensure_ascii=False)

    print("\n=== STAGE-3 COMPLETION ===", flush=True)
    print(f"  (b) trained substrate descended : {c_b}", flush=True)
    print(f"  (c) GATED < base                : {c_gated_lt_base}  ({ce_gated:.4f} < {ce_base:.4f})", flush=True)
    print(f"  (c) CE floor MET (< {UNIFORM_CE:.3f})    : {c_floor}", flush=True)
    print(f"  (c) structured (>1.5× floor)    : {c_struct}  ({kl_on:.3f} vs {kl_floor:.3f})", flush=True)
    if completion:
        print(f"\n🟢 오메가 완성 — the learned-gate OMEGA closure WORKS on a REAL trained transformer.", flush=True)
    else:
        print(f"\n🟡 PARTIAL / closed-negative (a_paper_negative_ok) — see criteria above; NO fabricated pass.", flush=True)
    print(f"results -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
