#!/usr/bin/env python3
"""OMEGA decisive follow-up — does the substrate->decode closure SURVIVE on a WELL-TRAINED,
LEAK-FREE substrate?  (the #1794 follow-up)

#1794 (OMEGA-A) added causal_ca=True to ConsciousDecoderV2, REMOVING the CA-neighbor
lookahead leak (leak self-test 0.000). It revealed #1791's headline absolute-CE win
(GATED 0.345 << base) was LEAK-DRIVEN: on the leak-free substrate GATED 3.594 > base 3.015
AND val_ce ~= uniform 5.43 — the substrate GENERALIZED WEAKLY (it was UNDERTRAINED: d384/d768,
only ~2500-6000 steps, small corpus). The leak-INVARIANT relative structure (A-wire +0.158 >>
shuffle -0.509) held, but the absolute closure win did not.

THE OPEN QUESTION THIS RUNG SETTLES: train a leak-free (causal_ca=True) CDV2 to ADEQUATE
generalization — enough steps/data that held-out val_ce drops CLEARLY BELOW uniform
(ln256 = 5.545; target val_ce <= ~4.0 or as low as budget allows). THEN on this well-trained
leak-free substrate run the learned-gate closure eval (mirror #1794/#1786): held-out CE for
base / a_only / fixed_AmG / GATED, PLUS the leak-invariant structured-coupling (A-wire real vs
shuffle).

PRE-REGISTERED FALSIFIER:
  "the closure helps a TRAINED substrate" HOLDS  iff
      (GATED < base  AND  GATED <= a_only)
  on the leak-free, WELL-GENERALIZING substrate (val_ce clearly < uniform).
  If it still fails (GATED >= base) even when val_ce is well below uniform -> honest
  CLOSED-NEGATIVE: the gated bus does NOT improve a COMPETENT substrate's prediction (the
  closure carries structure but not predictive usefulness once the mouth is good).
Either result is the decisive answer — reported exactly, NO fabrication.

a_lane_akida_gpu_split: Lane-G / GPU (NOT Lane A AKIDA). GPU REQUIRED (g63, no silent CPU).
"""
import os, sys, json, math, time, hashlib, argparse
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from conscious_decoder import ConsciousDecoderV2  # noqa: E402
from omega_gpu_complete import (  # noqa: E402
    fetch_corpus, get_batch, extract_feats,
    softmax_np, ce_of, fit_gate, kl_structured,
    V, SMOOTH, ALPHA, UNIFORM_CE, GATE_STEPS, GATE_L2,
)

# generation byte-stats reused from the #1794 driver
from omega_gen_cluster import byte_stats, gen_sample  # noqa: E402


# ───────────────────── robust multi-batch held-out val_ce ─────────────────────

def eval_val_ce(model, val_data, block, bs, device, n_batches=40, seed=20260604):
    """Honest held-out next-byte CE on head_a, averaged over MANY disjoint-ish val batches
    (not a single 16-row batch like the toy train loop). This is the generalization metric
    the falsifier pre-registers against uniform = ln256 = 5.545."""
    model.eval()
    g = torch.Generator().manual_seed(seed)
    tot, ntok = 0.0, 0
    with torch.no_grad():
        for _ in range(n_batches):
            ix = torch.randint(0, len(val_data) - block - 1, (bs,), generator=g)
            x = torch.stack([torch.from_numpy(val_data[int(i):int(i) + block].astype(np.int64)) for i in ix]).to(device)
            y = torch.stack([torch.from_numpy(val_data[int(i) + 1:int(i) + 1 + block].astype(np.int64)) for i in ix]).to(device)
            la, _, _, _, _ = model(x)
            ce = F.cross_entropy(la.reshape(-1, V), y.reshape(-1), reduction="sum")
            tot += float(ce.item()); ntok += y.numel()
    return tot / max(1, ntok)


# ───────────────────── train the leak-free substrate to ADEQUATE generalization ─────────

def train_to_competence(model, train_data, val_data, steps, block, bs, lr, device,
                        warmup=200, val_every=500):
    """Train CDV2 (dual-head: head_a next-byte, head_g prev-byte) with cosine-decay LR + warmup
    for MANY more steps than #1794, tracking a robust multi-batch val_ce curve so we can SEE the
    held-out next-byte head descend below uniform. Same objective as omega_gpu_complete (byte-eq
    method); the ONLY change vs #1794 is more steps + a real val curve + LR schedule."""
    opt = torch.optim.AdamW(model.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)

    def lr_at(step):
        if step < warmup:
            return lr * (step + 1) / warmup
        prog = (step - warmup) / max(1, steps - warmup)
        return lr * (0.1 + 0.9 * 0.5 * (1.0 + math.cos(math.pi * prog)))

    train_curve = []   # train ce_a / ce_g
    val_curve = []     # robust held-out val_ce
    model.train()
    t0 = time.time()
    for step in range(steps):
        for pg in opt.param_groups:
            pg["lr"] = lr_at(step)
        x, y_next = get_batch(train_data, block, bs, device)
        y_prev = torch.roll(x, shifts=1, dims=1)
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
        if step % max(1, steps // 40) == 0 or step == steps - 1:
            train_curve.append({"step": step, "ce_a": float(loss_a.item()), "ce_g": float(loss_g.item())})
            print(f"  step {step:6d}/{steps}  ce_a(next)={loss_a.item():.4f}  ce_g(prev)={loss_g.item():.4f}"
                  f"  lr={lr_at(step):.2e}  {(time.time()-t0):.1f}s", flush=True)
        if step % val_every == 0 or step == steps - 1:
            vce = eval_val_ce(model, val_data, block, bs, device)
            val_curve.append({"step": step, "val_ce": vce})
            print(f"    [val] step {step:6d}  val_ce(head_a, multi-batch)={vce:.4f}  "
                  f"(uniform={UNIFORM_CE:.4f}, below_uniform={vce < UNIFORM_CE})", flush=True)
            model.train()
    final_val = eval_val_ce(model, val_data, block, bs, device, n_batches=80)
    return train_curve, val_curve, final_val, time.time() - t0


# ───────────────────── the closure eval on the well-trained substrate ─────────────────────

def closure_eval(model, held, block, device, label, do_gen=True):
    """Mirror #1794/#1786 exactly: extract base/A/G on disjoint held-out gate+test splits,
    fit the learned gate on the gate split, then report held-out TEST CE for
    base / fixed_AmG / a_only / GATED + the leak-invariant structured-coupling (real vs shuffle).
    PRE-REGISTERED falsifier: closure HOLDS iff GATED < base AND GATED <= a_only."""
    gate_seq = held[:len(held) // 2]
    test_seq = held[len(held) // 2:]
    gate_feats, gate_tgt = extract_feats(model, gate_seq, block, device, max_pos=12000)
    test_feats, test_tgt = extract_feats(model, test_seq, block, device, max_pos=12000)
    test_feats_shuf, _ = extract_feats(model, test_seq, block, device, max_pos=12000, shuffle_ctx=True)

    g_star = fit_gate(gate_feats, gate_tgt, steps=GATE_STEPS, l2=GATE_L2)
    print(f"learned gate g* = [gB={g_star[0]:.4f}, gA={g_star[1]:.4f}, gG={g_star[2]:.4f}]", flush=True)

    ce_base = ce_of(np.array([1.0, 0.0, 0.0]), test_feats, test_tgt)
    ce_fixed = ce_of(np.array([1.0, ALPHA, -ALPHA]), test_feats, test_tgt)
    ce_aonly = ce_of(np.array([1.0, ALPHA, 0.0]), test_feats, test_tgt)
    ce_gated = ce_of(g_star, test_feats, test_tgt)
    print(f"--- held-out TEST CE (LEAK-FREE, well-trained, nats/byte) ---", flush=True)
    print(f"  base {ce_base:.6f} | fixed_AmG {ce_fixed:.6f} | a_only {ce_aonly:.6f} | "
          f"GATED {ce_gated:.6f} | uniform {UNIFORM_CE:.6f}", flush=True)

    st = kl_structured(test_feats, test_feats_shuf, test_tgt)
    print(f"structured: A-wire gain real {st['gain_real']:.4f} vs shuf {st['gain_shuf']:.4f} "
          f"-> structured(>1.5x)={st['structured_ce']}", flush=True)

    # PRE-REGISTERED falsifier
    gated_lt_base = ce_gated < ce_base
    gated_le_aonly = ce_gated <= ce_aonly
    closure_holds = bool(gated_lt_base and gated_le_aonly)
    print(f"\n  >>> CLOSURE FALSIFIER: GATED<base={gated_lt_base}  AND  GATED<=a_only={gated_le_aonly}"
          f"  -> closure_HOLDS={closure_holds}", flush=True)

    gen = None
    if do_gen:
        counts = np.full(V, SMOOTH)
        for b in test_seq:
            counts[int(b)] += 1.0
        log_base_vec = np.log(counts / counts.sum())
        prompt = bytes(test_seq[:48].tobytes())
        base_txt, gated_txt, base_b, gated_b = gen_sample(model, prompt, 300, device, g_star, log_base_vec)
        gated_stats = byte_stats(gated_b[len(prompt):])
        base_stats = byte_stats(base_b[len(prompt):])
        coherent = (gated_stats["entropy"] > 1.5 and gated_stats["distinct_frac"] > 0.10
                    and gated_stats["ws_frac"] < 0.80)
        print(f"\n  gen: gated entropy={gated_stats['entropy']:.3f} distinct={gated_stats['distinct_frac']:.3f}"
              f" ws={gated_stats['ws_frac']:.3f} coherent={coherent}", flush=True)
        print(f"  [GATED] {gated_txt[len(prompt):][:160]!r}", flush=True)
        gen = {"coherent": bool(coherent), "base_stats": base_stats, "gated_stats": gated_stats,
               "gated_sample": gated_txt[len(prompt.decode('utf-8', errors='replace')):][:300],
               "base_sample": base_txt[len(prompt.decode('utf-8', errors='replace')):][:300]}

    return {
        "gate": {"gB": float(g_star[0]), "gA": float(g_star[1]), "gG": float(g_star[2])},
        "ce": {"base": ce_base, "fixed_AmG": ce_fixed, "a_only": ce_aonly, "gated": ce_gated,
               "uniform_floor": UNIFORM_CE},
        "structured": st,
        "closure": {"gated_lt_base": gated_lt_base, "gated_le_aonly": gated_le_aonly,
                    "HOLDS": closure_holds},
        "gen": gen,
    }


def run_rung(d_model, n_layer, n_head, n_kv_head, block, bs, lr, steps, device,
             train_data, val_data, held, label, ckpt_path=None):
    print(f"\n{'='*26} TRAINED-LEAKFREE RUNG {label} (d_model={d_model}, causal_ca=True) {'='*26}", flush=True)
    model = ConsciousDecoderV2(
        vocab_size=V, d_model=d_model, n_head=n_head, n_layer=n_layer,
        block_size=block, n_kv_head=n_kv_head, consciousness_dim=128,
        causal_ca=True,   # ← strictly-causal CA — no lookahead leak (the #1794 fix)
    ).to(device)
    nparam = model.count_params()
    print(f"CDV2 params: {nparam:,} ({nparam/1e6:.2f}M)  causal_ca={model.causal_ca}", flush=True)

    # leak self-test (untrained): flip ONLY last byte -> head_a at earlier positions must NOT move
    model.eval()
    with torch.no_grad():
        xt = torch.randint(0, V, (1, min(32, block)), device=device)
        la1, _, _, _, _ = model(xt)
        xt2 = xt.clone(); xt2[0, -1] = (int(xt[0, -1]) + 7) % V
        la2, _, _, _, _ = model(xt2)
        leak = float((la1[0, :-1] - la2[0, :-1]).abs().max().item())
    print(f"leak self-test (flip last byte -> max change in head_a earlier pos): {leak:.3e}  (want ~0)", flush=True)
    leak_free = leak < 1e-4

    train_curve, val_curve, final_val, train_wall = train_to_competence(
        model, train_data, val_data, steps, block, bs, lr, device)
    first_ce = train_curve[0]["ce_a"]; final_ce = train_curve[-1]["ce_a"]
    below_uniform = final_val < UNIFORM_CE
    competent = final_val <= 4.0   # the pre-registered "adequate generalization" bar
    print(f"\n(b) trained leak-free: ce_a {first_ce:.4f} -> {final_ce:.4f}  FINAL val_ce={final_val:.4f}  "
          f"below_uniform={below_uniform}  competent(<=4.0)={competent}  wall={train_wall:.1f}s", flush=True)

    if ckpt_path:
        cfg = {"vocab_size": V, "d_model": d_model, "n_head": n_head, "n_layer": n_layer,
               "block_size": block, "n_kv_head": n_kv_head, "consciousness_dim": 128, "causal_ca": True}
        torch.save({"model": model.state_dict(), "config": cfg}, ckpt_path)
        ckpt_sha = hashlib.sha256(open(ckpt_path, "rb").read()).hexdigest()
        print(f"ckpt saved: {ckpt_path}  sha256={ckpt_sha[:16]}", flush=True)
    else:
        ckpt_sha = None

    cl = closure_eval(model, held, block, device, label)

    return {
        "label": label, "leak_self_test": leak, "leak_free": bool(leak_free),
        "params": int(nparam), "d_model": d_model, "n_layer": n_layer, "steps": steps,
        "train": {"first_ce_a": first_ce, "final_ce_a": final_ce, "final_val_ce": final_val,
                  "below_uniform": bool(below_uniform), "competent": bool(competent),
                  "wall_s": train_wall, "train_curve": train_curve, "val_curve": val_curve},
        "ckpt_sha256": ckpt_sha,
        **cl,
        "config": {"vocab_size": V, "d_model": d_model, "n_head": n_head, "n_layer": n_layer,
                   "block_size": block, "n_kv_head": n_kv_head, "consciousness_dim": 128, "causal_ca": True},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=20000)
    ap.add_argument("--block", type=int, default=256)
    ap.add_argument("--bs", type=int, default=48)
    ap.add_argument("--lr", type=float, default=6e-4)
    ap.add_argument("--corpus_mb", type=int, default=400)
    ap.add_argument("--d_model", type=int, default=512)
    ap.add_argument("--n_layer", type=int, default=8)
    ap.add_argument("--n_head", type=int, default=8)
    ap.add_argument("--n_kv_head", type=int, default=4)
    ap.add_argument("--out", default="omega_trained_leakfree_results.json")
    ap.add_argument("--ckpt", default="omega_cdv2_trained_leakfree.pt")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device != "cuda":
        print("!!! NO CUDA — refusing to fake a GPU train (g63). Reporting BLOCKED.", flush=True)
        json.dump({"BLOCKED": "no_cuda", "device": device}, open(args.out, "w"), indent=2)
        sys.exit(2)
    gpu_name = torch.cuda.get_device_name(0)
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    print(f"=== OMEGA trained-leakfree — WELL-TRAINED causal-CA substrate + closure eval ===", flush=True)
    print(f"device={device}  gpu={gpu_name}  torch={torch.__version__}", flush=True)

    target = args.corpus_mb * 1_000_000
    corpus, prov = fetch_corpus(target, os.path.join(HERE, "omega_corpus_big.bin"))
    sha = hashlib.sha256(corpus.tobytes()).hexdigest()
    n = len(corpus)
    print(f"corpus: {n}B ({n/1e6:.1f}MB)  prov={prov}  sha256={sha[:16]}", flush=True)

    cut = int(n * 0.9)
    train_data = corpus[:cut]
    held = corpus[cut:]
    val_data = held[:len(held) // 2]

    t_start = time.time()
    r = run_rung(args.d_model, args.n_layer, args.n_head, args.n_kv_head, args.block,
                 args.bs, args.lr, args.steps, device, train_data, val_data, held,
                 f"d{args.d_model}-trained-leakfree", ckpt_path=args.ckpt)

    results = {
        "lane": "Lane-G", "substrate": "GPU", "gpu": gpu_name, "torch": torch.__version__,
        "corpus_bytes": int(n), "corpus_mb": n / 1e6, "corpus_prov": prov, "corpus_sha256": sha,
        "fix": "causal_ca=True — strictly-causal CA (no lookahead leak), trained to competence",
        "question": "does the substrate->decode closure SURVIVE on a well-trained leak-free substrate?",
        "falsifier": "closure HOLDS iff GATED < base AND GATED <= a_only on a val_ce<uniform substrate",
        "ckpt": {"path": args.ckpt, "sha256": r.get("ckpt_sha256")},
        "rung": r,
        "total_wall_s": time.time() - t_start,
    }
    json.dump(results, open(args.out, "w"), indent=2, ensure_ascii=False)

    print("\n=== TRAINED-LEAKFREE SUMMARY ===", flush=True)
    print(f"  leak self-test: {r['leak_self_test']:.3e} (leak_free={r['leak_free']})", flush=True)
    print(f"  final val_ce: {r['train']['final_val_ce']:.4f}  below_uniform={r['train']['below_uniform']}"
          f"  competent(<=4.0)={r['train']['competent']}", flush=True)
    ce = r["ce"]
    print(f"  CE: base {ce['base']:.4f} | a_only {ce['a_only']:.4f} | fixed_AmG {ce['fixed_AmG']:.4f}"
          f" | GATED {ce['gated']:.4f} | uniform {ce['uniform_floor']:.4f}", flush=True)
    print(f"  structured: real {r['structured']['gain_real']:.4f} vs shuf {r['structured']['gain_shuf']:.4f}"
          f" -> {r['structured']['structured_ce']}", flush=True)
    print(f"  >>> CLOSURE on a COMPETENT substrate HOLDS = {r['closure']['HOLDS']}"
          f"  (GATED<base={r['closure']['gated_lt_base']}, GATED<=a_only={r['closure']['gated_le_aonly']})", flush=True)
    print(f"results -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
