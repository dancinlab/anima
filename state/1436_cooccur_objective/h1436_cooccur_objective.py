#!/usr/bin/env python3
"""H_1436 — co-occurrence auxiliary-objective training.

ANGLE: the BIND failure is that comparator and measurable tokens are emitted in
SEPARATE windows, never co-active. H_1436 adds an AUXILIARY LOSS that rewards the
model when, within a sliding window, the predicted distribution puts mass on BOTH a
comparator token AND a measurable token co-occurring. The aux loss is a soft
co-activation reward on the SAME training corpus as H_1435 (falsifiable-claim
templated, eval-disjoint subjects). Standard CE + lambda * cooccur_aux.

The aux is NOT the detector: it operates on the frozen COMPARATOR/MEASURABLE byte-level
token presence in the model's own predicted top-k within a window — it shapes the JOINT
emission, it does not author detector tokens into targets (anti-tune-to-green: the corpus
subjects + eval seeds are disjoint; held-out + shuffle-corpus controls gate the lift).
"""
import os, sys, json, random, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g6_common as C
import torch
import torch.nn.functional as F

OUT = os.environ.get("G6_OUT", "/workspace/g6/out")

# reuse H_1435 corpus generator (same falsifiable-claim distribution)
import h1435_continued_pretrain as base1435
gen_corpus = base1435.gen_corpus
shuffle_bytes = base1435.shuffle_bytes
make_batches = base1435.make_batches

# byte-id sets for comparator / measurable FIRST bytes (cheap co-activation proxy):
# we reward joint mass on the leading bytes of any comparator vs any measurable word.
def _lead_byte_ids(words):
    ids = set()
    for w in words:
        if w:
            ids.add(w.encode("utf-8")[0])
            ids.add((" " + w).encode("utf-8")[0])  # leading space variant
    return sorted(ids)

COMP_BYTES = _lead_byte_ids(sorted(C.COMPARATOR))
MEAS_BYTES = _lead_byte_ids(sorted(C.MEASURABLE))


def cooccur_aux(logits, comp_b, meas_b):
    """logits: (B,T,256). Reward windows where predicted prob mass on a comparator
    lead-byte AND a measurable lead-byte are BOTH high somewhere in the window.
    aux = -mean over batch of (max_t p_comp(t)) * (max_t p_meas(t)) — pushes both up
    jointly within the sequence. Returns a scalar to ADD (we minimize -reward)."""
    p = F.softmax(logits, dim=-1)                  # (B,T,256)
    pc = p[:, :, comp_b].sum(-1)                    # (B,T) mass on comparator leads
    pm = p[:, :, meas_b].sum(-1)                    # (B,T) mass on measurable leads
    # peak co-activation per sequence
    reward = (pc.max(dim=1).values * pm.max(dim=1).values).mean()
    return -reward                                  # minimize -> push joint peak up


def train(m, cfg, corpus_text, steps, device, lr=3e-5, bs=16, lam=0.5):
    m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)
    gen = make_batches(corpus_text, cfg["block"], bs, device)
    comp_b = torch.tensor(COMP_BYTES, device=device)
    meas_b = torch.tensor(MEAS_BYTES, device=device)
    t0 = time.time()
    for st in range(steps):
        x, y = next(gen)
        logits, ce = m(x, y)
        aux = cooccur_aux(logits, comp_b, meas_b)
        loss = ce + lam * aux
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        if st % 50 == 0 or st == steps - 1:
            print(f"    [H1436 step {st:4d}] ce={ce.item():.4f} aux={aux.item():.4f} "
                  f"{(time.time()-t0)/60:.1f}min", flush=True)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:1")
    ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--lines", type=int, default=4000)
    ap.add_argument("--lam", type=float, default=0.5)
    args = ap.parse_args()
    dev = args.device

    print(f"[H_1436] device={dev} steps={args.steps} lam={args.lam}", flush=True)
    base_m, cfg = C.load_model(C.CKPT_BASE, dev)
    base_eval = C.evaluate(base_m, cfg, "base", list(C.g.IDEATION_SEEDS))
    print(f"[H_1436] base FALS_in={base_eval['FALS_in']} FALS_ho={base_eval['FALS_ho']}", flush=True)
    del base_m; torch.cuda.empty_cache()

    corpus = gen_corpus(args.lines, seed=1436)

    m, _ = C.load_model(C.CKPT_BASE, dev)
    m = train(m, cfg, corpus, args.steps, dev, lam=args.lam)
    out_pt = os.path.join(OUT, "h1436_cooccur_objective.pt")
    C.save_model(m, cfg, out_pt, {"variant": "H_1436", "steps": args.steps, "lam": args.lam})
    trained_eval = C.evaluate(m, cfg, "trained", list(C.g.IDEATION_SEEDS))
    del m; torch.cuda.empty_cache()

    shuf_corpus = shuffle_bytes(corpus, seed=1436)
    ms, _ = C.load_model(C.CKPT_BASE, dev)
    ms = train(ms, cfg, shuf_corpus, args.steps, dev, lam=args.lam)
    shuf_eval = C.evaluate(ms, cfg, "shuffle_corpus", list(C.g.IDEATION_SEEDS))
    del ms; torch.cuda.empty_cache()

    bars = C.print_bars("H_1436 cooccur-objective", base_eval, trained_eval, shuf_eval)
    out = {"variant": "H_1436", "ckpt_base": C.CKPT_BASE, "ckpt_out": out_pt,
           "base": base_eval, "trained": trained_eval, "shuffle_corpus": shuf_eval, "bars": bars}
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(os.path.join(OUT, "h1436_result.json"), "w"), ensure_ascii=False, indent=2)
    print(f"[H_1436 done] {OUT}/h1436_result.json", flush=True)


if __name__ == "__main__":
    main()
