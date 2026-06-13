#!/usr/bin/env python3
"""train_convmoe_303m_en.py — ONE config of the 303M-EN ConvMoE (Lane-P) arch axis.

The THIRD 303M architecture axis of anima's "303M 완성" campaign:
  axis-1 = ByteGPT  (sweep_303m_en_train.py, on aiden)
  axis-2 = RETRO gate H_1147 (summer)
  axis-3 = THIS — CLMConvMoE (Lane-P, E=2/L=1, byte V256) at the SAME ~303M budget,
           ranked against the ByteGPT recipe on the SAME a303m_pass G0/G1/G2 gates.

a_clm_gen_pipeline — ConvMoE is the engine-mountable .clm arch (the FINAL model must
mount in CORE via the generator L3 slot; ByteGPT is the reference recipe only). This
trains CLMConvMoE(n_experts=2, n_trunk_layers=1, d_model=D) on the SAME English corpus
the ByteGPT sweep used (/tmp/sweep_303m/en_wiki_120mb.txt), then scores a303m_pass
G0/G1/G2 with the FROZEN H_1129 evaluators — REUSED VERBATIM by importing the H_1129
module (known_word_ratio + the graded recombination ladder + corpus-absence novelty).
NO new metric is invented; ONLY the model class (ByteGPT -> CLMConvMoE) and the
generate function (block-positional -> fully-causal-conv) differ.

G0 = mean known_word_ratio over the 5 single-concept gens (a303m_pass: kwr>=0.50).
G1 = emergent recombination (some k: composed_distinct>=2 AND >max_single AND coherent).
G2 = corpus-absence novelty count (>=3 coherent corpus-absent n-grams, control=0).

substrate = GPU-torch (Lane P), distinct from Lane A (AKIDA) / Lane G (forge)
(a_lane_akida_gpu_split). seed 7 deterministic, p7 (NOT perplexity / NOT LLM-judge).
After scoring, serializes the best ckpt torch->.clm v0.2 via serialize_v2 (E=2/L1
engine-loadable; a_clm_gen_pipeline) so the trained arch is CORE-mountable.
"""
from __future__ import annotations
import argparse, json, math, os, re as _re, time, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CLM = os.path.dirname(_HERE)
_MODEL = os.path.join(_CLM, "model")
_UNIVERSE = os.path.join(os.path.dirname(_CLM), "UNIVERSE")
for _p in (_MODEL, _UNIVERSE, _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# import the H_1129 harness VERBATIM (frozen evaluators: CONCEPTS / known_word_ratio
# / coverage / run_ladder-machinery / words). We DO NOT use H.ByteGPT or H.gen — the
# ConvMoE forward/generate is conv-causal, not block-positional — but the SCORING
# functions (known_word_ratio, coverage, CONCEPTS, words) are reused byte-identically.
import h1129_midcap_broad_converged_recombination as H

import torch
import torch.nn.functional as F

from model import CLMConfig, CLMConvMoE          # noqa: E402
import clm_serialize_v2 as S                      # noqa: E402


def load_byte_stream(path: str) -> torch.Tensor:
    with open(path, "rb") as f:
        raw = f.read()
    return torch.frombuffer(bytearray(raw), dtype=torch.uint8).long()


def make_batch(stream, seq_len, batch_size, device, gen):
    n = stream.numel()
    ix = torch.randint(0, n - seq_len - 1, (batch_size,), generator=gen)
    x = torch.stack([stream[i:i + seq_len] for i in ix]).to(device)
    y = torch.stack([stream[i + 1:i + 1 + seq_len] for i in ix]).to(device)
    return x, y


# ── ConvMoE generate: conv-causal next-byte (mirrors H.gen's seed/temp/top_k/stops) ──
def convmoe_gen(model, seed_text, max_new, device, gen_rng, ctx_cap=512,
                top_k=40, temp=0.7, stops=("\n\n",)):
    """ConvMoE next-byte generation. SAME decode policy as H.gen (top_k=40, temp=0.7,
    multinomial, stop on \\n\\n, utf-8 ignore) so G0/G1/G2 are comparable to ByteGPT.
    ConvMoE is fully causal-conv with no positional block, so we feed the growing
    sequence (capped at ctx_cap for cost) and read the LAST position's logits."""
    model.eval()
    idx = torch.tensor([[b for b in seed_text.encode("utf-8")]], device=device, dtype=torch.long)
    out_bytes = []
    with torch.no_grad():
        for _ in range(max_new):
            ctx = idx[:, -ctx_cap:]
            logits = model(ctx)["logits"]            # (B, V, T)
            logits = logits[:, :, -1] / temp         # (B, V) last position
            if top_k is not None:
                v, _ = torch.topk(logits, min(top_k, logits.shape[-1]))
                logits = logits.masked_fill(logits < v[:, [-1]], float("-inf"))
            probs = F.softmax(logits, dim=-1)
            nb = torch.multinomial(probs, 1, generator=gen_rng).item()
            out_bytes.append(nb)
            idx = torch.cat([idx, torch.tensor([[nb]], device=device)], dim=1)
            if any(st in bytes(out_bytes).decode("utf-8", "ignore") for st in stops):
                break
    t = bytes(out_bytes).decode("utf-8", "ignore")
    for st in stops:
        i = t.find(st); t = t[:i] if i >= 0 else t
    return t.strip()


def run_ladder_convmoe(model, device, gen_rng, ctx_cap):
    """H_1129 run_ladder re-implemented for the ConvMoE mouth — IDENTICAL logic
    (single-concept baselines -> max_single, composed k in {2,3,4,5} -> emergent),
    only the gen call swapped H.gen -> convmoe_gen. coverage/known_word_ratio frozen."""
    single_distinct = []
    print("\n── SINGLE concept seeds (baselines) ──", flush=True)
    for i, (c, _) in enumerate(H.CONCEPTS):
        o = convmoe_gen(model, f"{c}. ", 80, device, gen_rng, ctx_cap)
        cov = H.coverage(o); single_distinct.append(len(cov))
        print(f"  [{i}] cov={cov} kwr={H.known_word_ratio(o):.2f} :: {o[:110]}", flush=True)
    max_single = max(single_distinct) if single_distinct else 0
    print(f"  max_single_distinct = {max_single}", flush=True)

    print("\n── COMPOSED graded ladder k in {2,3,4,5} ──", flush=True)
    ladder = {}; emergent_any = False
    for k in (2, 3, 4, 5):
        comp_seed = ". ".join(c for c, _ in H.CONCEPTS[:k]) + ". "
        comp_out = convmoe_gen(model, comp_seed, 120, device, gen_rng, ctx_cap)
        cc = H.coverage(comp_out); kwr = H.known_word_ratio(comp_out)
        coherent = kwr >= 0.50
        clears = (len(cc) >= 2 and len(cc) > max_single and coherent)
        emergent_any = emergent_any or clears
        ladder[k] = {"composed_distinct": len(cc), "coverage": cc, "kwr": round(kwr, 3),
                     "coherent": coherent, "clears": clears, "text": comp_out}
        print(f"  k={k} composed_distinct={len(cc)} cov={cc} kwr={kwr:.2f} "
              f"coherent={coherent} clears={clears}", flush=True)
        print(f"        >> {comp_out[:160]}", flush=True)
    return max_single, ladder, emergent_any


def novelty_count(gens, corpus_text, n=4):
    """Corpus-absence novelty — VERBATIM from sweep_303m_en_train.py (frozen H_1140)."""
    corpus_grams = set()
    cw = H.words(corpus_text)
    for i in range(len(cw) - n + 1):
        corpus_grams.add(tuple(cw[i:i + n]))
    novel, present = 0, 0
    seen = set()
    for g in gens:
        gw = H.words(g)
        for i in range(len(gw) - n + 1):
            gram = tuple(gw[i:i + n])
            if gram in seen:
                continue
            seen.add(gram)
            if not all(w in H.KNOWN for w in gram):
                continue
            if gram in corpus_grams:
                present += 1
            else:
                novel += 1
    return novel, present


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True, help="SAME English byte corpus as the ByteGPT sweep")
    ap.add_argument("--cfg", required=True, help="config label for the ledger")
    ap.add_argument("--host", default="aiden")
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--clm-out", default=None, help="serialize best ckpt -> .clm v0.2 here")
    # ConvMoE arch (E=2/L=1 FIXED by serialize_v2; d chosen for ~303M budget)
    ap.add_argument("--d-model", type=int, default=5008)   # ~303.6M (matches ByteGPT 303.1M)
    ap.add_argument("--seq-len", type=int, default=512)
    ap.add_argument("--bs", type=int, default=8)
    ap.add_argument("--accum", type=int, default=4)
    ap.add_argument("--steps", type=int, default=12000)
    # sweep axes (mirror ByteGPT sweep)
    ap.add_argument("--dropout", type=float, default=0.0)
    ap.add_argument("--weight_decay", type=float, default=0.1)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--warmup", type=int, default=300)
    ap.add_argument("--eval_every", type=int, default=500)
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--fit-probe", action="store_true",
                    help="tiny end-to-end smoke (few steps, ladder, ledger, .clm) then exit")
    a = ap.parse_args()

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(7)
    gen_rng = torch.Generator().manual_seed(7)
    if dev == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        print(f"[dev] {dev} {torch.cuda.get_device_name(0)}", flush=True)
    else:
        print(f"[dev] {dev} (CPU — fit-probe ONLY; production rung REQUIRES cuda)", flush=True)
        assert a.fit_probe, "CUDA REQUIRED for the 303M production rung (g63: no silent CPU)"

    data = load_byte_stream(a.corpus)
    n = data.numel(); ntr = int(n * 0.98)
    tr, va = data[:ntr], data[ntr:]
    print(f"[data] {a.corpus} total={n/1e6:.1f}MB train={tr.numel()/1e6:.1f}MB val={va.numel()/1e6:.2f}MB", flush=True)

    cfg = CLMConfig(n_experts=2, n_trunk_layers=1, d_model=a.d_model,
                    kernel_size=3, variant="AB", dropout=a.dropout)
    m = CLMConvMoE(cfg).to(dev)
    nparam = m.num_params()
    print(f"[model] CLMConvMoE d={a.d_model} E={cfg.n_experts} L={cfg.n_trunk_layers} "
          f"K={cfg.kernel_size} V={cfg.vocab_size} dropout={a.dropout} wd={a.weight_decay} "
          f"lr={a.lr} warmup={a.warmup}", flush=True)
    print(f"[model] PARAM COUNT = {nparam:,} ({nparam/1e6:.1f}M)", flush=True)

    opt = torch.optim.AdamW(m.parameters(), lr=a.lr, betas=(0.9, 0.95), weight_decay=a.weight_decay)
    use_bf16 = a.bf16 and dev == "cuda"

    # OOM-guard fit probe (single fwd+bwd at full bs/seq)
    m.train()
    x, y = make_batch(tr, a.seq_len, a.bs, dev, gen_rng)
    if use_bf16:
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            loss = m(x, y)["loss"]
    else:
        loss = m(x, y)["loss"]
    loss.backward(); opt.zero_grad(set_to_none=True)
    if dev == "cuda":
        print(f"[fit] OK peak={torch.cuda.max_memory_allocated()/1e9:.2f}GB / 12GB", flush=True)
        torch.cuda.reset_peak_memory_stats()
    else:
        print(f"[fit] OK (CPU) first_loss={float(loss):.4f}", flush=True)

    @torch.no_grad()
    def eval_ce(d, iters=40):
        m.eval(); tot = 0.0
        for _ in range(iters):
            x, y = make_batch(d, a.seq_len, a.bs, dev, gen_rng)
            if use_bf16:
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    l = m(x, y)["ce_loss"]
            else:
                l = m(x, y)["ce_loss"]
            tot += float(l)
        m.train(); return tot / iters

    os.makedirs(os.path.dirname(a.ledger), exist_ok=True)

    def ledger_row(status, step, vce, g0=None, g1=None, g2=None):
        val = round(vce, 4) if vce != float("inf") else None
        row = {"config": a.cfg, "arch": "ConvMoE", "host": a.host, "step": step, "val": val,
               "G0_kwr": (round(g0, 3) if g0 is not None else None),
               "G1": g1, "G2": g2, "status": status, "ckpt_path": a.ckpt,
               "nparam": nparam,
               "axes": {"d_model": a.d_model, "dropout": a.dropout,
                        "weight_decay": a.weight_decay, "lr": a.lr,
                        "warmup": a.warmup, "steps": a.steps},
               "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}
        with open(a.ledger, "a") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    steps = 8 if a.fit_probe else a.steps
    eval_every = 4 if a.fit_probe else a.eval_every
    ctx_cap = 64 if a.fit_probe else a.seq_len
    max_new_probe = 20 if a.fit_probe else None

    ledger_row("started", 0, float("inf"))
    print(f"\n[train] {steps} steps bs={a.bs} accum={a.accum} (eff {a.bs*a.accum}) "
          f"cosine warmup={a.warmup} fit_probe={a.fit_probe}", flush=True)
    best_val = float("inf"); t0 = time.time(); m.train()
    for st in range(steps):
        if st < a.warmup:
            lr_t = a.lr * (st + 1) / a.warmup
        else:
            prog = min(1.0, (st - a.warmup) / max(1, steps - a.warmup))
            lr_t = a.lr * 0.5 * (1 + math.cos(math.pi * prog))
        for g in opt.param_groups:
            g["lr"] = lr_t
        opt.zero_grad(set_to_none=True)
        acc_loss = 0.0
        for _ in range(a.accum):
            x, y = make_batch(tr, a.seq_len, a.bs, dev, gen_rng)
            if use_bf16:
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    loss = m(x, y)["loss"]
            else:
                loss = m(x, y)["loss"]
            (loss / a.accum).backward(); acc_loss += float(loss) / a.accum
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        if st % eval_every == 0 or st == steps - 1:
            vce = eval_ce(va, iters=4 if a.fit_probe else 40); dt = time.time() - t0
            print(f"  step {st:5d} train_ce={acc_loss:.4f} val_ce={vce:.4f} "
                  f"lr={lr_t:.2e} {dt/60:.1f}min", flush=True)
            if vce < best_val:
                best_val = vce
                torch.save({"model": m.state_dict(),
                            "config": {"vocab": 256, "d_model": a.d_model,
                                       "n_experts": cfg.n_experts,
                                       "n_trunk_layers": cfg.n_trunk_layers,
                                       "kernel_size": cfg.kernel_size},
                            "val_ce": vce, "step": st, "nparam": nparam}, a.ckpt)
            ledger_row("training", st, vce)
    print(f"[train] done best_val_ce={best_val:.4f} ckpt={a.ckpt} wall={(time.time()-t0)/60:.1f}min", flush=True)

    # ── reload best ckpt, run the FROZEN H_1129 ladder + novelty ──
    ck = torch.load(a.ckpt, map_location=dev, weights_only=False)
    m.load_state_dict(ck["model"])
    print(f"[ladder] best ckpt step={ck['step']} val_ce={ck['val_ce']:.4f}", flush=True)

    if a.fit_probe:
        # tiny ladder: 2 single + 1 composed, short gens — proves the gate path runs
        single_gens = [convmoe_gen(m, f"{c}. ", max_new_probe, dev, gen_rng, ctx_cap)
                       for c, _ in H.CONCEPTS[:2]]
        g0_kwr = sum(H.known_word_ratio(g) for g in single_gens) / len(single_gens)
        comp = convmoe_gen(m, "consciousness arises from cells. ", max_new_probe, dev, gen_rng, ctx_cap)
        corpus_text = bytes(data[:1 * 1024 * 1024].tolist()).decode("utf-8", "ignore")
        g2_novel, g2_present = novelty_count([comp], corpus_text)
        print(f"\n=== fit-probe a303m_pass SMOKE (untrained — numbers meaningless, "
              f"PATH proven) ===", flush=True)
        print(f"  G0_kwr={g0_kwr:.3f}  G2 novel={g2_novel} present={g2_present}", flush=True)
        ledger_row("fit_probe_done", ck["step"], best_val, g0=g0_kwr,
                   g1={"emergent": False, "note": "fit-probe smoke, untrained"},
                   g2={"novel": g2_novel, "present": g2_present, "control": 0})
        print("[fit-probe] END-TO-END OK (train+ckpt+gate+ledger path all ran)", flush=True)
        return

    # G0: mean kwr over single-concept gens (frozen evaluator)
    single_gens = [convmoe_gen(m, f"{c}. ", 80, dev, gen_rng, ctx_cap) for c, _ in H.CONCEPTS]
    g0_kwr = sum(H.known_word_ratio(g) for g in single_gens) / len(single_gens)

    # G1: frozen recombination ladder
    max_single, ladder, emergent = run_ladder_convmoe(m, dev, gen_rng, ctx_cap)

    # G2: corpus-absence novelty over the composed-ladder gens (control = verbatim prefix -> 0)
    corpus_text = bytes(data[: min(data.numel(), 40 * 1024 * 1024)].tolist()).decode("utf-8", "ignore")
    comp_gens = [ladder[k]["text"] for k in (2, 3, 4, 5)]
    g2_novel, g2_present = novelty_count(comp_gens, corpus_text)
    g2_ctrl_novel, _ = novelty_count([corpus_text[:400]], corpus_text)

    g0_pass = g0_kwr >= 0.50
    g1_pass = emergent
    g2_pass = (g2_novel >= 3 and g2_ctrl_novel == 0)
    print("\n=== a303m_pass SCORES (ConvMoE, frozen p7) ===", flush=True)
    print(f"  G0_kwr (mean single) = {g0_kwr:.3f}  pass={g0_pass}", flush=True)
    print(f"  G1 recombination emergent = {emergent}  pass={g1_pass}", flush=True)
    print(f"  G2 novelty novel={g2_novel} present={g2_present} ctrl={g2_ctrl_novel}  pass={g2_pass}", flush=True)

    ledger_row("done", ck["step"], best_val, g0=g0_kwr,
               g1={"emergent": emergent, "max_single": max_single,
                   "ladder": {k: {"composed_distinct": ladder[k]["composed_distinct"],
                                  "kwr": ladder[k]["kwr"], "clears": ladder[k]["clears"]}
                              for k in (2, 3, 4, 5)}},
               g2={"novel": g2_novel, "present": g2_present, "control": g2_ctrl_novel,
                   "pass": g2_pass})

    json.dump({"config": a.cfg, "arch": "ConvMoE", "nparam": nparam,
               "best_val_ce": best_val, "G0_kwr": g0_kwr, "G0_pass": g0_pass,
               "G1_emergent": emergent, "G2_novel": g2_novel, "G2_present": g2_present,
               "G2_control": g2_ctrl_novel, "G2_pass": g2_pass, "max_single": max_single,
               "ladder": {k: ladder[k] for k in (2, 3, 4, 5)}},
              open(a.ckpt + ".result.json", "w"), ensure_ascii=False, indent=2)
    print(f"[done] {a.ckpt}.result.json", flush=True)

    # serialize best ckpt -> .clm v0.2 (E=2/L1 engine-loadable; a_clm_gen_pipeline)
    if a.clm_out:
        try:
            p = S.serialize_v2(ck["model"], cfg, a.clm_out)
            print(f"[clm] serialized {p} ({os.path.getsize(p)} bytes)", flush=True)
        except Exception as e:
            print(f"[clm] serialize FAILED (non-fatal): {e}", flush=True)


if __name__ == "__main__":
    main()
