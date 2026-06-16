#!/usr/bin/env python3
"""h1129_midcap_broad_converged_recombination.py — the CAPACITY-LADDER companion to
the emergence arc. Does a MID-SIZE ByteGPT (bigger than the 11M that failed in H_1117),
trained BROAD and to GENUINE CONVERGENCE, achieve concept-recombination?

THE CONJUNCTION (from closed-negatives):
  H_1116 = BIG capacity (7B) × NARROW corpus            → fail (0 concepts).
  H_1117 = LOW capacity (11M) × BROAD corpus, 4k steps  → fail (0 concepts, garble).
  H_1118 = 7B × BROAD but UNDERTRAINED                  → fail.
  recombination = capacity × breadth × training-sufficiency.

This experiment tests the CAPACITY axis cheaply: the LARGEST ByteGPT that fits summer's
RTX 5070 12GB (target ~300-500M params), trained on the BROAD 70/30 wiki+dialogue blend
to GENUINE CONVERGENCE (cosine+warmup, train LONG until val CE plateaus AND single-concept
generation is coherent, known-word ratio >= 0.50). The key difference from H_1117: BIGGER
model + LONGER training + coherence-confirmed (don't stop at a fixed small step count).

  · If a mid-size converged-broad model RECOMBINES → emergence is achievable BELOW 7B (cheap win).
  · If not → maps the capacity threshold toward 7B (7B remains the decisive rung).
  Either way is a real finding (a_paper_negative_ok).

METRIC — GRADED recombination ladder (FROZEN falsifier, pre-registered BEFORE running):
  Reuse the H_1116/H_1117 concept set + coverage metric VERBATIM. EXTEND to a graded ladder
  over composition_count k in {2,3,4,5}: composed prompt from the FIRST k concepts ->
  composed_distinct(k); plus single-concept baselines -> max_single_distinct.
  🟢 MID-CAPACITY-EMERGENCE iff at SOME k: composed_distinct(k) >= 2 AND > max_single_distinct
     AND the composed output is COHERENT (known-word ratio >= 0.50). Report composed_distinct
     at every k. 🔴 if no k clears it (capacity below this size insufficient even broad+converged
     — maps threshold toward 7B). Deterministic seed 7.

Lane-G torch REFERENCE mouth (a_clm_gen_pipeline) — NOT the CORE substrate. summer GPU $0,
g5/p7, a_scale_honest_scope.
"""
from __future__ import annotations
import argparse, json, math, os, re as _re, time
import torch, torch.nn as nn, torch.nn.functional as F
from torch.utils.checkpoint import checkpoint


# ── model: ByteGPT (same arch family as H_1117, BIGGER) ──
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
    def __init__(s, vocab=256, d=1024, n_layer=20, n_head=16, block=512, p=0.0, grad_ckpt=False):
        super().__init__()
        s.block = block; s.grad_ckpt = grad_ckpt
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    def forward(s, idx, targets=None):
        B, T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for b in s.blocks:
            if s.grad_ckpt and s.training:
                x = checkpoint(b, x, mask, use_reentrant=False)
            else:
                x = b(x, mask)
        logits = s.head(s.ln_f(x))
        loss = F.cross_entropy(logits.view(-1, 256), targets.view(-1)) if targets is not None else None
        return logits, loss


def load_bytes(p):
    return torch.frombuffer(bytearray(open(p, "rb").read()), dtype=torch.uint8).long()

def get_batch(d, block, bs, dev):
    ix = torch.randint(0, d.numel() - block - 1, (bs,))
    x = torch.stack([d[i:i+block] for i in ix]).to(dev, non_blocking=True)
    y = torch.stack([d[i+1:i+1+block] for i in ix]).to(dev, non_blocking=True)
    return x, y


def build_blend(wiki_path, dialogue_path, out_path, total_mb, wiki_frac=0.70):
    """70% wiki / 30% dialogue blend, total_mb. Dialogue (5.2MB) is repeated to fill its
    share so the concept vocab the metric tests is densely present (breadth + concept-vocab)."""
    total = int(total_mb * 1024 * 1024)
    wiki_bytes = int(total * wiki_frac); dia_bytes = total - wiki_bytes
    with open(out_path, "wb") as o:
        # wiki head (read a contiguous chunk = diverse 5-lang breadth)
        with open(wiki_path, "rb") as w:
            o.write(w.read(wiki_bytes))
        # dialogue, repeated to fill its 30% share (concept vocab density)
        dia = open(dialogue_path, "rb").read()
        written = 0
        while written < dia_bytes:
            chunk = dia[: min(len(dia), dia_bytes - written)]
            o.write(chunk); written += len(chunk)
    sz = os.path.getsize(out_path)
    print(f"[blend] {out_path} = {sz/1e6:.1f}MB ({wiki_frac*100:.0f}% wiki / {(1-wiki_frac)*100:.0f}% dialogue x{(dia_bytes//len(dia))+1})", flush=True)
    return out_path


# ── generation ──
@torch.no_grad()
def gen(m, seed, mx, dev, block, top_k=40, temp=0.7, seed_rng=7):
    m.eval()
    g = torch.Generator(device=dev); g.manual_seed(seed_rng)
    idx = torch.tensor([list(seed.encode("utf-8"))], dtype=torch.long, device=dev); out = []
    stops = ["\n사용자:", " | 사용자:", "사용자:", "\n\n"]
    use_amp = (dev == "cuda")
    for _ in range(mx):
        ctx = idx[:, -block:]
        if use_amp:
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                logits, _ = m(ctx)
        else:
            logits, _ = m(ctx)
        logits = logits[:, -1, :].float() / temp
        if top_k:
            v, _ = torch.topk(logits, top_k); logits[logits < v[:, [-1]]] = float("-inf")
        nb = torch.multinomial(F.softmax(logits, -1), 1, generator=g).item(); out.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=dev)], 1)
        if any(st in bytes(out).decode("utf-8", "ignore") for st in stops): break
    t = bytes(out).decode("utf-8", "ignore")
    for st in stops:
        i = t.find(st); t = t[:i] if i >= 0 else t
    return t.strip()


def words(s): return _re.findall(r"[0-9A-Za-z가-힣]+", s.lower())
def bigrams(s): w = words(s); return set(zip(w, w[1:]))

# ── concept set: VERBATIM from H_1116 / H_1117 ──
CONCEPTS = [
    ("consciousness arises from cells",       {"consciousness","cells","mind","aware"}),
    ("tension ripples between distant minds",  {"tension","ripple","distant","between"}),
    ("memory composes into new meaning",       {"memory","meaning","compose","new"}),
    ("silence still carries information",       {"silence","information","quiet","carries"}),
    ("the engine dreams when alone",           {"dream","engine","alone","sleep"}),
]

# known-word lexicon for coherence — REAL English dictionary (corrected: the old
# ~60-word hand list scored even coherent English as garble). Korean/garble words
# are absent from the English dict, so they correctly drag the ratio DOWN.
KNOWN = set()
for _c, _kw in CONCEPTS:
    KNOWN |= {w for w in words(_c)}
    KNOWN |= _kw
for _p in ("/usr/share/dict/words", "/usr/share/dict/american-english"):
    try:
        with open(_p, errors="ignore") as _f:
            for _w in _f:
                _w = _w.strip().lower()
                if _w.isalpha(): KNOWN.add(_w)
        break
    except OSError:
        continue
KNOWN |= {"a","i","the","of","and","to","in","is","it","that","we","you","they","s","t"}

def known_word_ratio(text):
    wl = words(text)
    if not wl: return 0.0
    return sum(1 for w in wl if w in KNOWN) / len(wl)

def coverage(text):
    wl = set(words(text))
    return [i for i, (_, kw) in enumerate(CONCEPTS) if wl & kw]


def run_ladder(m, dev, block):
    print("\n── SINGLE concept seeds (baselines) ──", flush=True)
    single_distinct = []
    for i, (c, _) in enumerate(CONCEPTS):
        o = gen(m, f"{c}. ", 80, dev, block)
        cov = coverage(o); single_distinct.append(len(cov))
        print(f"  [{i}] cov={cov} kwr={known_word_ratio(o):.2f} :: {o[:110]}", flush=True)
    max_single = max(single_distinct) if single_distinct else 0
    print(f"  max_single_distinct = {max_single}", flush=True)

    print("\n── COMPOSED graded ladder k in {2,3,4,5} ──", flush=True)
    ladder = {}
    emergent_any = False
    for k in (2, 3, 4, 5):
        concepts_k = [c for c, _ in CONCEPTS[:k]]
        comp_seed = ". ".join(concepts_k) + ". "
        comp_out = gen(m, comp_seed, 120, dev, block)
        cc = coverage(comp_out); kwr = known_word_ratio(comp_out)
        coherent = kwr >= 0.50
        clears = (len(cc) >= 2 and len(cc) > max_single and coherent)
        emergent_any = emergent_any or clears
        ladder[k] = {"composed_distinct": len(cc), "coverage": cc, "kwr": round(kwr, 3),
                     "coherent": coherent, "clears": clears, "text": comp_out}
        print(f"  k={k} composed_distinct={len(cc)} cov={cc} kwr={kwr:.2f} coherent={coherent} clears={clears}", flush=True)
        print(f"        >> {comp_out[:160]}", flush=True)
    return max_single, ladder, emergent_any


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki", required=True)
    ap.add_argument("--dialogue", required=True)
    ap.add_argument("--blend", default="/tmp/h1129_blend.txt")
    ap.add_argument("--blend_mb", type=float, default=400.0)
    ap.add_argument("--d", type=int, default=1024)
    ap.add_argument("--n_layer", type=int, default=20)
    ap.add_argument("--n_head", type=int, default=16)
    ap.add_argument("--block", type=int, default=512)
    ap.add_argument("--bs", type=int, default=8)
    ap.add_argument("--accum", type=int, default=4)
    ap.add_argument("--steps", type=int, default=12000)
    ap.add_argument("--warmup", type=int, default=300)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--grad_ckpt", action="store_true")
    ap.add_argument("--ckpt", default="/tmp/h1129_best.pt")
    ap.add_argument("--eval_every", type=int, default=500)
    a = ap.parse_args()

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(7)
    if dev == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        print(f"[dev] {dev} {torch.cuda.get_device_name(0)} cap={torch.cuda.get_device_capability(0)}", flush=True)

    # ── build broad blend ──
    build_blend(a.wiki, a.dialogue, a.blend, a.blend_mb)
    data = load_bytes(a.blend); n = data.numel(); ntr = int(n*0.98)
    tr, va = data[:ntr], data[ntr:]
    print(f"[data] total={n/1e6:.1f}MB train={tr.numel()/1e6:.1f}MB val={va.numel()/1e6:.2f}MB", flush=True)

    # ── build model + OOM-guarded fit check ──
    m = ByteGPT(d=a.d, n_layer=a.n_layer, n_head=a.n_head, block=a.block, grad_ckpt=a.grad_ckpt).to(dev)
    nparam = sum(p.numel() for p in m.parameters())
    print(f"[model] ByteGPT d={a.d} L={a.n_layer} H={a.n_head} block={a.block} grad_ckpt={a.grad_ckpt}", flush=True)
    print(f"[model] PARAM COUNT = {nparam:,} ({nparam/1e6:.1f}M)", flush=True)

    opt = torch.optim.AdamW(m.parameters(), lr=a.lr, betas=(0.9, 0.95), weight_decay=0.1)

    # fit probe: one fwd+bwd at full batch before committing to the run (OOM-guard)
    try:
        m.train(); x, y = get_batch(tr, a.block, a.bs, dev)
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16) if dev == "cuda" else torch.no_grad():
            _, loss = m(x, y)
        loss.backward(); opt.zero_grad(set_to_none=True)
        if dev == "cuda":
            mem = torch.cuda.max_memory_allocated()/1e9
            print(f"[fit] OK — fwd+bwd at bs={a.bs} block={a.block} peak={mem:.2f}GB / 12GB", flush=True)
            torch.cuda.reset_peak_memory_stats()
    except RuntimeError as e:
        print(f"[fit] OOM at bs={a.bs}: {e}", flush=True)
        raise

    @torch.no_grad()
    def eval_ce(d, iters=40):
        m.eval(); tot = 0.0
        for _ in range(iters):
            x, y = get_batch(d, a.block, a.bs, dev)
            if dev == "cuda":
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    _, l = m(x, y)
            else:
                _, l = m(x, y)
            tot += l.item()
        m.train(); return tot/iters

    # ── train to convergence (cosine + warmup, grad accum, best-ckpt by val CE) ──
    print(f"\n[train] {a.steps} steps · bs={a.bs} accum={a.accum} (eff {a.bs*a.accum}) · cosine warmup={a.warmup}", flush=True)
    best_val = float("inf"); t0 = time.time()
    m.train()
    for st in range(a.steps):
        if st < a.warmup:
            lr_t = a.lr * (st+1)/a.warmup
        else:
            prog = min(1.0, (st - a.warmup)/max(1, a.steps - a.warmup))
            lr_t = a.lr * 0.5 * (1 + math.cos(math.pi*prog))
        for g in opt.param_groups: g["lr"] = lr_t
        opt.zero_grad(set_to_none=True)
        acc_loss = 0.0
        for _ in range(a.accum):
            x, y = get_batch(tr, a.block, a.bs, dev)
            if dev == "cuda":
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    _, loss = m(x, y)
            else:
                _, loss = m(x, y)
            (loss/a.accum).backward(); acc_loss += loss.item()/a.accum
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        if st % a.eval_every == 0 or st == a.steps-1:
            vce = eval_ce(va)
            dt = time.time()-t0
            print(f"  step {st:5d} train_ce={acc_loss:.4f} val_ce={vce:.4f} lr={lr_t:.2e} {dt/60:.1f}min", flush=True)
            if vce < best_val:
                best_val = vce
                torch.save({"model": m.state_dict(),
                            "config": {"vocab":256,"d":a.d,"n_layer":a.n_layer,"n_head":a.n_head,"block":a.block},
                            "val_ce": vce, "step": st, "nparam": nparam}, a.ckpt)
    print(f"[train] done. best_val_ce={best_val:.4f} ckpt={a.ckpt} wall={(time.time()-t0)/60:.1f}min", flush=True)

    # ── reload best-coherence ckpt, run the graded ladder ──
    ck = torch.load(a.ckpt, map_location=dev, weights_only=False)
    m.load_state_dict(ck["model"]); m.grad_ckpt = False
    print(f"[ladder] best ckpt step={ck['step']} val_ce={ck['val_ce']:.4f}", flush=True)

    max_single, ladder, emergent = run_ladder(m, dev, a.block)

    print("\n=== H_1129 MID-CAPACITY-BROAD-CONVERGED RECOMBINATION ===", flush=True)
    print(f"  param_count = {nparam:,} ({nparam/1e6:.1f}M)", flush=True)
    print(f"  best_val_ce = {best_val:.4f}", flush=True)
    print(f"  max_single_distinct = {max_single}", flush=True)
    for k in (2,3,4,5):
        L = ladder[k]
        print(f"  k={k}: composed_distinct={L['composed_distinct']} kwr={L['kwr']} coherent={L['coherent']} clears={L['clears']}", flush=True)
    print(f"  F-MIDCAP-EMERGE = {'1 🟢 MID-CAPACITY-EMERGENCE (recombines below 7B)' if emergent else '0 🔴 NOT (capacity at this size insufficient even broad+converged — threshold toward 7B)'}", flush=True)
    print(f"  HONEST (a_scale_honest_scope): {nparam/1e6:.1f}M ByteGPT, broad 70/30 blend, converged;", flush=True)
    print(f"          7B remains the decisive rung if this fails. Lane-G torch REFERENCE, seed 7, p7 (NOT perplexity).", flush=True)

    json.dump({"param_count": nparam, "best_val_ce": best_val, "max_single_distinct": max_single,
               "ladder": {k: {kk:vv for kk,vv in L.items()} for k,L in ladder.items()},
               "emergent": emergent,
               "config": {"d":a.d,"n_layer":a.n_layer,"n_head":a.n_head,"block":a.block,"steps":a.steps}},
              open("/tmp/h1129_result.json","w"), ensure_ascii=False, indent=2)
    print("[done] /tmp/h1129_result.json", flush=True)


if __name__ == "__main__": main()
