#!/usr/bin/env python3
"""g1_multiseed.py — REFERENCE-MATCH fix for the G1 RECOMBINATION metric (ad13 path 1).

Builds DIRECTLY on state/1587_engine_torch_g1_divergence/g1_ladder_3way.py (ad13's harness).
The G1 recombination DEFINITION is frozen VERBATIM (7B_PASS_CONDITIONS / a7b_pass / H_1129):
  for some k in {2,3,4,5}: composed_distinct >= 2 AND composed_distinct > max_single AND coherent(kwr>=0.50).

The ONLY change is SEED-ROBUSTNESS (frozen-first, NOT tune-to-green): instead of declaring G1 on a
single fragile RNG walk (seed 7), evaluate the ladder over the seed set {7, 4302, 4303}
(reference-match — the same seeds the G6 ladders use [4301/4302/4303]; 7 = the H_1129 single-seed
default) and define GREEN = recombination clears in a MAJORITY of seeds (>=2/3). Applied
SYMMETRICALLY to BOTH the torch reference path AND the engine path, so they're compared on the
identical robust metric.

Usage:
  g1_multiseed.py bytegpt <h1129.bin> [<h1129c_best.pt>]   # engine arm (+torch arm if .pt & torch)
  g1_multiseed.py clm     <clm303_clean.clm> [<.pt>]       # engine arm
"""
from __future__ import annotations
import sys, os, re, time
HERE = os.path.dirname(os.path.abspath(__file__))
# core/ is two levels up from state/1588_.../  -> repo_root/core
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(REPO, "core"), os.path.join(HERE, "core"), HERE):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

# ── frozen metric (VERBATIM from ad13 g1_ladder_3way.py / H_1129 harness) ──────────────
CONCEPTS = [
    ("consciousness arises from cells",       {"consciousness","cells","mind","aware"}),
    ("tension ripples between distant minds",  {"tension","ripple","distant","between"}),
    ("memory composes into new meaning",       {"memory","meaning","compose","new"}),
    ("silence still carries information",       {"silence","information","quiet","carries"}),
    ("the engine dreams when alone",           {"dream","engine","alone","sleep"}),
]
def words(s): return re.findall(r"[0-9A-Za-z가-힣]+", s.lower())
KNOWN = set()
for _c, _kw in CONCEPTS:
    KNOWN |= {w for w in words(_c)}; KNOWN |= _kw
for _p in ("/usr/share/dict/words", "/usr/share/dict/american-english"):
    try:
        with open(_p, errors="ignore") as _f:
            for _w in _f:
                _w = _w.strip().lower()
                if _w.isalpha(): KNOWN.add(_w)
        break
    except OSError: continue
KNOWN |= {"a","i","the","of","and","to","in","is","it","that","we","you","they","s","t"}
def kwr(text):
    wl = words(text); return sum(1 for w in wl if w in KNOWN)/len(wl) if wl else 0.0
def coverage(text):
    wl = set(words(text)); return [i for i,(_,kw) in enumerate(CONCEPTS) if wl & kw]

STOPS = ["\n사용자:", " | 사용자:", "사용자:", "\n\n"]
def _trim(t):
    for st in STOPS:
        i = t.find(st); t = t[:i] if i >= 0 else t
    return t.strip()

# ── ladder over a SINGLE seed (frozen metric) ─────────────────────────────────────────
def ladder_seed(genfn, seed_rng, label):
    """Run the full G1 ladder for one RNG seed. genfn(seed_text, max_tok, seed_rng) -> str."""
    sd = []
    singles = []
    for i,(c,_) in enumerate(CONCEPTS):
        # H_1129 uses per-concept seed (7+s) for singles; keep that offset relative to base seed
        o = genfn(f"{c}. ", 80, seed_rng + i); cov = coverage(o); sd.append(len(cov))
        singles.append({"i": i, "cov": cov, "kwr": round(kwr(o),3), "text": o[:90]})
    ms = max(sd) if sd else 0
    ks = []; clears_any = False; best = 0
    for k in (2,3,4,5):
        seedp = ". ".join(c for c,_ in CONCEPTS[:k]) + ". "
        o = genfn(seedp, 120, seed_rng); cc = coverage(o); kk = kwr(o); coh = kk>=0.50
        clears = (len(cc)>=2 and len(cc)>ms and coh)
        clears_any = clears_any or clears; best = max(best, len(cc))
        ks.append({"k":k,"distinct":len(cc),"cov":cc,"kwr":round(kk,3),"coherent":coh,
                   "clears":clears,"text":o[:130]})
    print(f"  [seed {seed_rng}] {label}: max_single={ms} best_composed={best} "
          f"clears={'GREEN' if clears_any else 'FAIL'}", flush=True)
    for k in ks:
        print(f"      k={k['k']} distinct={k['distinct']} cov={k['cov']} kwr={k['kwr']} "
              f"coherent={k['coherent']} clears={k['clears']}", flush=True)
        print(f"         >> {k['text']!r}", flush=True)
    return {"seed": seed_rng, "max_single": ms, "best_composed": best,
            "clears": clears_any, "singles": singles, "ks": ks}

# ── multi-seed verdict (the REFERENCE-MATCH metric) ───────────────────────────────────
SEEDS = [7, 4302, 4303]   # reference-match: H_1129 seed 7 + G6-ladder seeds 4302/4303
def multiseed(genfn, label):
    print(f"\n##### MULTI-SEED LADDER [{label}]  seeds={SEEDS} #####", flush=True)
    per = [ladder_seed(genfn, s, label) for s in SEEDS]
    ngreen = sum(1 for r in per if r["clears"])
    verdict = "GREEN" if ngreen >= 2 else "FAIL"   # majority of 3
    print(f"  ==> [{label}] MULTI-SEED G1 = {verdict}  ({ngreen}/{len(SEEDS)} seeds clear)", flush=True)
    return {"label": label, "seeds": SEEDS, "per_seed": per, "n_green": ngreen,
            "n_seeds": len(SEEDS), "verdict": verdict}

# ── engine generators (py 2-production) ───────────────────────────────────────────────
def engine_bytegpt(binp):
    import bytegpt_decode as B
    W = B.bg_load(binp)
    def gen(seed, mx, seed_rng):
        ids = list(seed.encode("utf-8"))
        return _trim(B.bytegpt_decode_topk_sampled_W(W, ids, mx, 40, 0.7, seed_rng)["text"])
    return gen

def engine_clm(clmp):
    import clm_decode as C
    W = C.clm_load_weights(clmp)
    def gen(seed, mx, seed_rng):
        return _trim(C.clm_decode_topk_sampled_W(W, seed, mx, 40, 0.7, seed_rng)["text"])
    return gen

# ── torch reference generators (multinomial + Generator) ──────────────────────────────
def torch_bytegpt(ptp):
    import torch, torch.nn as nn, torch.nn.functional as F
    class Block(nn.Module):
        def __init__(s,d,h,p):
            super().__init__(); s.ln1=nn.LayerNorm(d)
            s.attn=nn.MultiheadAttention(d,h,dropout=p,batch_first=True); s.ln2=nn.LayerNorm(d)
            s.mlp=nn.Sequential(nn.Linear(d,4*d),nn.GELU(),nn.Linear(4*d,d),nn.Dropout(p))
        def forward(s,x,m):
            h=s.ln1(x); a,_=s.attn(h,h,h,attn_mask=m,need_weights=False); x=x+a
            return x+s.mlp(s.ln2(x))
    class ByteGPT(nn.Module):
        def __init__(s,vocab=256,d=1024,n_layer=24,n_head=16,block=512):
            super().__init__(); s.block=block
            s.tok=nn.Embedding(vocab,d); s.pos=nn.Embedding(block,d); s.drop=nn.Dropout(0.0)
            s.blocks=nn.ModuleList([Block(d,n_head,0.0) for _ in range(n_layer)])
            s.ln_f=nn.LayerNorm(d); s.head=nn.Linear(d,vocab,bias=False); s.head.weight=s.tok.weight
        def forward(s,idx):
            Bb,T=idx.shape; pos=torch.arange(T,device=idx.device)
            x=s.tok(idx)+s.pos(pos)[None,:,:]
            mask=torch.triu(torch.full((T,T),float("-inf"),device=idx.device),diagonal=1)
            for b in s.blocks: x=b(x,mask)
            return s.head(s.ln_f(x))
    ck=torch.load(ptp,map_location="cpu",weights_only=False); cfg=ck["config"]
    dev="cuda" if torch.cuda.is_available() else "cpu"
    use_amp = dev=="cuda"
    m=ByteGPT(**cfg).to(dev); m.load_state_dict(ck["model"]); m.eval()
    block=cfg["block"]
    @torch.no_grad()
    def gen(seed, mx, seed_rng):
        g=torch.Generator(device=dev); g.manual_seed(seed_rng)
        idx=torch.tensor([list(seed.encode("utf-8"))],dtype=torch.long,device=dev); out=[]
        for _ in range(mx):
            ctx=idx[:,-block:]
            if use_amp:
                with torch.autocast(device_type="cuda",dtype=torch.bfloat16): logits=m(ctx)
            else: logits=m(ctx)
            logits=logits[:,-1,:].float()/0.7
            v,_=torch.topk(logits,40); logits[logits<v[:,[-1]]]=float("-inf")
            nb=torch.multinomial(F.softmax(logits,-1),1,generator=g).item(); out.append(nb)
            idx=torch.cat([idx,torch.tensor([[nb]],device=dev)],1)
            if any(st in bytes(out).decode("utf-8","ignore") for st in STOPS): break
        return _trim(bytes(out).decode("utf-8","ignore"))
    print(f"  (torch bytegpt: dev={dev} amp={use_amp} cfg={cfg})", flush=True)
    return gen

def main():
    kind = sys.argv[1]; wpath = sys.argv[2]
    ptp = sys.argv[3] if len(sys.argv) > 3 else None
    print("="*80)
    print(f"G1 MULTI-SEED REFERENCE-MATCH — kind={kind} weights={os.path.basename(wpath)}")
    print(f"date {time.strftime('%Y-%m-%d %H:%M:%S')} host {os.uname().nodename} seeds={SEEDS}")
    print("="*80)

    results = {}
    # torch reference arm (if .pt present and torch importable) — bytegpt only
    if ptp and kind == "bytegpt":
        try:
            import torch as _t
            _ = _t.__version__
            results["torch_ref"] = multiseed(torch_bytegpt(ptp), "torch-ref (multinomial+Gen)")
        except Exception as e:
            print(f"  [torch arm skipped: {e}]", flush=True)

    # engine arm (py 2-production) — always
    if kind == "bytegpt":
        results["engine"] = multiseed(engine_bytegpt(wpath), "engine (py bytegpt_decode)")
    elif kind == "clm":
        results["engine"] = multiseed(engine_clm(wpath), "engine (py clm_decode)")
    else:
        print("unknown kind", kind); return 2

    print("\n"+"="*80); print("MULTI-SEED G1 SUMMARY"); print("="*80)
    for arm, r in results.items():
        print(f"  {arm:12s}: {r['verdict']}  ({r['n_green']}/{r['n_seeds']} seeds)  "
              f"per-seed clears={[ (p['seed'], p['clears']) for p in r['per_seed'] ]}")
    import json
    out = os.path.join(HERE, f"result_{kind}_{os.path.basename(wpath)}.json")
    with open(out, "w") as f: json.dump(results, f, indent=2)
    print(f"\nwrote {out}")
    return 0

if __name__ == "__main__": sys.exit(main())
