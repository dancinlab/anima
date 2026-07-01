#!/usr/bin/env python3
"""h1132_recombination_training_phase_transition.py — the TRAINING-AMOUNT axis of the
emergence-of-ideation arc. Holding capacity + breadth + corpus FIXED, does concept-
recombination switch on at a TRAINING THRESHOLD (a phase transition in composed_distinct
vs training-steps), or rise smoothly?

THE ARC (closed-negatives + the H_1129 🟢):
  H_1116 = BIG capacity (7B) × NARROW corpus            → fail (0 concepts).
  H_1117 = LOW capacity (11M) × BROAD corpus, 4k steps  → fail (0 concepts, garble).
  H_1118 = 7B × BROAD but UNDERTRAINED                  → fail (the undertraining confound).
  H_1128 = 7B × BROAD × CONVERGED (multilang)           → fail (script collapse).
  H_1129 = 303M × BROAD × CONVERGED × SCRIPT-CONTROL    → 🟢 EMERGENT (k=5 cd=3 > max_single).
  recombination = capacity × breadth × training-sufficiency × script-control.

H_1132 isolates the TRAINING-SUFFICIENCY axis at FIXED capacity + FIXED broad
English-dominant corpus: train ONE toy byte-LM and CHECKPOINT at a LOG-SPACED step
ladder (250/500/1k/2k/4k/8k), then run the H_1129 GRADED recombination metric on each
rung. Plot composed_distinct(best-k) vs step.

  · SHARP KNEE (composed_distinct ~0 below S*, jumps to >=2 above, >50% of the total
    rise inside one log-step doubling) = TRAINING-PHASE-TRANSITION.
  · GRADUAL RAMP (rises smoothly, no knee) = training-sufficiency is a continuous dial.

FROZEN FALSIFIER (pre-registered VERBATIM from .discoveries/1132_*.tape):
  🟢 TRAINING-PHASE-TRANSITION iff composed_distinct(best-k) is ~0 below a critical step
     S* and jumps to >=2 above it with a knee sharper than linear (>50% of the total rise
     occurs within one log-step doubling).
  🔴 SMOOTH if recombination rises gradually with no knee (then training-sufficiency is a
     continuous dial, not a transition).
  Coherence-gated (known-word ratio >= 0.50) at EVERY checkpoint to separate 'learned to
  spell' from 'learned to recombine'. Deterministic seed 7.

Honest scope (a_scale_honest_scope): the transition step S* is capacity+corpus specific
(toy byte-LM, this English-dominant broad blend) — does NOT claim a universal S*. Maps the
SHAPE (knee vs ramp) of the training axis. Lane-G torch REFERENCE mouth (a_clm_gen_pipeline,
NOT the CORE substrate). Local Apple-MPS/CPU $0, g5, p7 (set-overlap, NOT perplexity).
"""
from __future__ import annotations
import argparse, json, math, os, re as _re, time
import torch, torch.nn as nn, torch.nn.functional as F


# ── model: ByteGPT (same arch family as H_1117/H_1129, toy size) ──
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
    def __init__(s, vocab=256, d=256, n_layer=6, n_head=8, block=256, p=0.0):
        super().__init__()
        s.block = block
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
        s.apply(s._init)
    @staticmethod
    def _init(mod):
        # GPT-style small init so the tied-head initial CE starts near ln(256)~5.5
        # (default nn.Embedding N(0,1) made the tied logits explode to CE~243).
        if isinstance(mod, nn.Linear):
            nn.init.normal_(mod.weight, mean=0.0, std=0.02)
            if mod.bias is not None: nn.init.zeros_(mod.bias)
        elif isinstance(mod, nn.Embedding):
            nn.init.normal_(mod.weight, mean=0.0, std=0.02)
    def forward(s, idx, targets=None):
        B, T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        # boolean causal mask (additive -inf mask produces NaN softmax on some MPS builds)
        mask = torch.ones(T, T, dtype=torch.bool, device=idx.device).triu(1)
        for b in s.blocks:
            x = b(x, mask)
        logits = s.head(s.ln_f(x))
        loss = F.cross_entropy(logits.view(-1, 256), targets.view(-1)) if targets is not None else None
        return logits, loss


def load_bytes(p):
    return torch.frombuffer(bytearray(open(p, "rb").read()), dtype=torch.uint8).long()

def get_batch(d, block, bs, dev, gen=None):
    ix = torch.randint(0, d.numel() - block - 1, (bs,), generator=gen)
    x = torch.stack([d[i:i+block] for i in ix]).to(dev, non_blocking=True)
    y = torch.stack([d[i+1:i+1+block] for i in ix]).to(dev, non_blocking=True)
    return x, y


def build_blend(en_path, dialogue_path, out_path, total_mb, en_frac=0.70):
    """English-dominant broad blend (script-controlled per the H_1129 ingredient). The wide
    English webscale head supplies breadth; the dialogue corpus is ASCII-filtered (keeps the
    English lines that carry the concept vocabulary) and repeated to fill the concept-vocab
    share. Korean/non-ASCII lines are dropped so generation stays English-script."""
    total = int(total_mb * 1024 * 1024)
    en_bytes = int(total * en_frac); dia_bytes = total - en_bytes

    # ASCII-filter the dialogue corpus line-by-line (>=90% ASCII per line)
    dia_lines = []
    for ln in open(dialogue_path, "rb").read().split(b"\n"):
        if not ln.strip():
            continue
        asc = sum(1 for c in ln if c < 128)
        if asc / max(1, len(ln)) >= 0.90:
            dia_lines.append(ln)
    dia = b"\n".join(dia_lines) + b"\n"

    # the English breadth source (repeat to fill its share — toy corpus is small)
    en_src = open(en_path, "rb").read()

    with open(out_path, "wb") as o:
        written = 0
        while written < en_bytes:
            chunk = en_src[: min(len(en_src), en_bytes - written)]
            o.write(chunk); written += len(chunk)
        written = 0
        while written < dia_bytes:
            chunk = dia[: min(len(dia), dia_bytes - written)]
            o.write(chunk); written += len(chunk)
    sz = os.path.getsize(out_path)
    print(f"[blend] {out_path} = {sz/1e6:.1f}MB ({en_frac*100:.0f}% en-webscale / "
          f"{(1-en_frac)*100:.0f}% ascii-dialogue, dia-filtered={len(dia)/1e3:.1f}KB)", flush=True)
    return out_path


# ── generation (VERBATIM from H_1129) ──
@torch.no_grad()
def gen(m, seed, mx, dev, block, top_k=40, temp=0.7, seed_rng=7):
    m.eval()
    g = torch.Generator(device="cpu"); g.manual_seed(seed_rng)
    idx = torch.tensor([list(seed.encode("utf-8"))], dtype=torch.long, device=dev); out = []
    stops = ["\n사용자:", " | 사용자:", "사용자:", "\n\n"]
    for _ in range(mx):
        ctx = idx[:, -block:]
        logits, _ = m(ctx)
        logits = logits[:, -1, :].float() / temp
        if top_k:
            v, _ = torch.topk(logits, top_k); logits[logits < v[:, [-1]]] = float("-inf")
        probs = F.softmax(logits, -1).cpu()
        nb = torch.multinomial(probs, 1, generator=g).item(); out.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=dev)], 1)
        if any(st in bytes(out).decode("utf-8", "ignore") for st in stops): break
    t = bytes(out).decode("utf-8", "ignore")
    for st in stops:
        i = t.find(st); t = t[:i] if i >= 0 else t
    return t.strip()


def words(s): return _re.findall(r"[0-9A-Za-z가-힣]+", s.lower())
def bigrams(s): w = words(s); return set(zip(w, w[1:]))

# ── concept set: VERBATIM from H_1116 / H_1117 / H_1129 ──
CONCEPTS = [
    ("consciousness arises from cells",       {"consciousness","cells","mind","aware"}),
    ("tension ripples between distant minds",  {"tension","ripple","distant","between"}),
    ("memory composes into new meaning",       {"memory","meaning","compose","new"}),
    ("silence still carries information",       {"silence","information","quiet","carries"}),
    ("the engine dreams when alone",           {"dream","engine","alone","sleep"}),
]

# known-word lexicon for coherence — REAL English dictionary (VERBATIM from H_1129)
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
    """The H_1129 GRADED recombination ladder — single baselines + composed k in {2,3,4,5}.
    Returns max_single, per-k dict, and best_composed_distinct over coherent k."""
    single_distinct = []
    for i, (c, _) in enumerate(CONCEPTS):
        o = gen(m, f"{c}. ", 80, dev, block)
        cov = coverage(o); single_distinct.append(len(cov))
    max_single = max(single_distinct) if single_distinct else 0

    ladder = {}
    best_cd = 0
    emergent_any = False
    for k in (2, 3, 4, 5):
        concepts_k = [c for c, _ in CONCEPTS[:k]]
        comp_seed = ". ".join(concepts_k) + ". "
        comp_out = gen(m, comp_seed, 120, dev, block)
        cc = coverage(comp_out); kwr = known_word_ratio(comp_out)
        coherent = kwr >= 0.50
        clears = (len(cc) >= 2 and len(cc) > max_single and coherent)
        emergent_any = emergent_any or clears
        # best composed_distinct counts only COHERENT rungs (spell-gated)
        cd_coh = len(cc) if coherent else 0
        best_cd = max(best_cd, cd_coh)
        ladder[k] = {"composed_distinct": len(cc), "coverage": cc, "kwr": round(kwr, 3),
                     "coherent": coherent, "clears": clears, "text": comp_out}
    return max_single, ladder, emergent_any, best_cd


def train_with_ladder(a, dev):
    torch.manual_seed(7)
    bgen = torch.Generator(device="cpu"); bgen.manual_seed(7)

    build_blend(a.en, a.dialogue, a.blend, a.blend_mb)
    data = load_bytes(a.blend); n = data.numel(); ntr = int(n*0.98)
    tr, va = data[:ntr], data[ntr:]
    print(f"[data] total={n/1e6:.1f}MB train={tr.numel()/1e6:.1f}MB val={va.numel()/1e6:.2f}MB", flush=True)

    m = ByteGPT(d=a.d, n_layer=a.n_layer, n_head=a.n_head, block=a.block).to(dev)
    nparam = sum(p.numel() for p in m.parameters())
    print(f"[model] ByteGPT d={a.d} L={a.n_layer} H={a.n_head} block={a.block} "
          f"PARAM={nparam:,} ({nparam/1e6:.2f}M)", flush=True)

    opt = torch.optim.AdamW(m.parameters(), lr=a.lr, betas=(0.9, 0.95), weight_decay=0.1)

    @torch.no_grad()
    def eval_ce(d, iters=20):
        m.eval(); tot = 0.0
        eg = torch.Generator(device="cpu"); eg.manual_seed(123)
        for _ in range(iters):
            x, y = get_batch(d, a.block, a.bs, dev, eg)
            _, l = m(x, y); tot += l.item()
        m.train(); return tot/iters

    # LOG-SPACED checkpoint ladder (the rungs the falsifier sweeps)
    ladder_steps = sorted(int(s) for s in a.ladder.split(","))
    max_step = max(ladder_steps)
    print(f"[ladder] checkpoint steps = {ladder_steps}", flush=True)

    results = {}
    t0 = time.time()
    m.train()
    for st in range(1, max_step + 1):
        # cosine schedule to the FULL max_step (fixed schedule so each rung is the same run)
        if st < a.warmup:
            lr_t = a.lr * st / a.warmup
        else:
            prog = min(1.0, (st - a.warmup) / max(1, max_step - a.warmup))
            lr_t = a.lr * 0.5 * (1 + math.cos(math.pi * prog))
        for g in opt.param_groups: g["lr"] = lr_t
        opt.zero_grad(set_to_none=True)
        acc_loss = 0.0
        for _ in range(a.accum):
            x, y = get_batch(tr, a.block, a.bs, dev, bgen)
            _, loss = m(x, y)
            (loss / a.accum).backward(); acc_loss += loss.item() / a.accum
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()

        if st in ladder_steps:
            vce = eval_ce(va)
            max_single, lad, emergent, best_cd = run_ladder(m, dev, a.block)
            dt = (time.time() - t0) / 60
            results[st] = {"step": st, "val_ce": round(vce, 4), "max_single": max_single,
                           "best_composed_distinct": best_cd, "emergent": emergent,
                           "ladder": {k: {"composed_distinct": v["composed_distinct"],
                                          "kwr": v["kwr"], "coherent": v["coherent"],
                                          "clears": v["clears"]} for k, v in lad.items()}}
            print(f"\n[RUNG step={st:5d}] val_ce={vce:.4f} max_single={max_single} "
                  f"best_composed_distinct(coherent)={best_cd} emergent={emergent} ({dt:.1f}min)", flush=True)
            for k in (2, 3, 4, 5):
                v = lad[k]
                print(f"    k={k} composed_distinct={v['composed_distinct']} cov={v['coverage']} "
                      f"kwr={v['kwr']} coherent={v['coherent']} clears={v['clears']}", flush=True)
                print(f"        >> {v['text'][:150]}", flush=True)
            # save the ckpt rung (gitignored; registered in HF.jsonl)
            if a.save_ckpts:
                cpath = os.path.join(a.ckpt_dir, f"h1132_step{st}.pt")
                torch.save({"model": m.state_dict(),
                            "config": {"vocab":256,"d":a.d,"n_layer":a.n_layer,
                                       "n_head":a.n_head,"block":a.block},
                            "val_ce": vce, "step": st, "nparam": nparam}, cpath)
            m.train()
    return nparam, results, ladder_steps


def knee_analysis(results, ladder_steps):
    """Apply the frozen falsifier: is best_composed_distinct(step) a SHARP KNEE or a SMOOTH ramp?

    KNEE iff: ~0 below a critical S*, jumps to >=2 above S*, and >50% of the total rise occurs
    within ONE log-step doubling (i.e. between two adjacent ladder rungs whose step ratio<=~2.5).
    SMOOTH iff: rises gradually with no such single-doubling jump.
    """
    steps = ladder_steps
    cd = [results[s]["best_composed_distinct"] for s in steps]
    final = cd[-1]; first = cd[0]
    total_rise = final - first

    print("\n=== KNEE ANALYSIS (frozen falsifier) ===", flush=True)
    print(f"  best_composed_distinct ladder (coherent-gated): "
          f"{list(zip(steps, cd))}", flush=True)
    print(f"  total_rise = {total_rise} (first={first} @step{steps[0]} -> final={final} @step{steps[-1]})", flush=True)

    if final < 2:
        # never reaches the recombination bar at all -> neither knee nor smooth-onto-recomb
        verdict = "NO-ONSET"
        print(f"  best_composed_distinct never reaches >=2 (max={max(cd)}) -> recombination "
              f"does NOT switch on within this training ladder at this capacity/corpus.", flush=True)
        return verdict, {"cd": cd, "total_rise": total_rise, "max_cd": max(cd), "Sstar": None}

    # find the largest single-doubling jump (adjacent rungs with step ratio<=2.5)
    best_jump = 0.0; jump_lo = jump_hi = None; Sstar = None
    for i in range(1, len(steps)):
        ratio = steps[i] / steps[i-1]
        jump = cd[i] - cd[i-1]
        if ratio <= 2.5 and jump > best_jump:
            best_jump = jump; jump_lo, jump_hi = steps[i-1], steps[i]
    # S* = the first rung where best_composed_distinct crosses to >=2
    for i, v in enumerate(cd):
        if v >= 2:
            Sstar = steps[i]; break

    frac_in_one_doubling = (best_jump / total_rise) if total_rise > 0 else 0.0
    knee = (best_jump >= 2 and frac_in_one_doubling > 0.50)
    verdict = "KNEE" if knee else "SMOOTH"

    print(f"  largest single-log-step-doubling jump = {best_jump} "
          f"(between step {jump_lo} -> {jump_hi})", flush=True)
    print(f"  fraction of total rise inside that one doubling = {frac_in_one_doubling:.2f} "
          f"(>0.50 required for a knee)", flush=True)
    print(f"  S* (first step with best_composed_distinct>=2) = {Sstar}", flush=True)
    print(f"  -> {'🟢 TRAINING-PHASE-TRANSITION (sharp knee)' if knee else '🔴 SMOOTH ramp (no knee — training-sufficiency is a continuous dial)'}", flush=True)
    return verdict, {"cd": cd, "total_rise": total_rise, "best_jump": best_jump,
                     "jump_between": [jump_lo, jump_hi],
                     "frac_in_one_doubling": round(frac_in_one_doubling, 3),
                     "Sstar": Sstar, "knee": knee}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--en", required=True, help="English breadth corpus (webscale head)")
    ap.add_argument("--dialogue", required=True, help="dialogue corpus (concept-vocab, ascii-filtered)")
    ap.add_argument("--blend", default="/tmp/h1132_blend.txt")
    ap.add_argument("--blend_mb", type=float, default=12.0)
    ap.add_argument("--d", type=int, default=256)
    ap.add_argument("--n_layer", type=int, default=6)
    ap.add_argument("--n_head", type=int, default=8)
    ap.add_argument("--block", type=int, default=256)
    ap.add_argument("--bs", type=int, default=24)
    ap.add_argument("--accum", type=int, default=1)
    ap.add_argument("--lr", type=float, default=6e-4)
    ap.add_argument("--warmup", type=int, default=200)
    ap.add_argument("--ladder", default="250,500,1000,2000,4000,8000")
    ap.add_argument("--ckpt_dir", default="/tmp/h1132_ckpts")
    ap.add_argument("--save_ckpts", action="store_true")
    ap.add_argument("--device", default="auto")
    a = ap.parse_args()

    if a.device == "auto":
        # CPU default: MPS softmax over an all-masked row yields NaN on this torch build
        # (the causal byte-LM has fully-masked positions); CUDA preferred when present.
        dev = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        dev = a.device
    os.makedirs(a.ckpt_dir, exist_ok=True)
    print(f"[dev] {dev} | torch {torch.__version__} | seed 7 | KNOWN-lexicon {len(KNOWN):,} words", flush=True)

    nparam, results, ladder_steps = train_with_ladder(a, dev)
    verdict, knee_info = knee_analysis(results, ladder_steps)

    print("\n=== H_1132 RECOMBINATION TRAINING-PHASE-TRANSITION ===", flush=True)
    print(f"  param_count = {nparam:,} ({nparam/1e6:.2f}M)  [capacity FIXED]", flush=True)
    print(f"  corpus = English-dominant broad blend {a.blend_mb:.0f}MB  [breadth FIXED]", flush=True)
    print(f"  TRAINING-AMOUNT swept over ladder {ladder_steps}", flush=True)
    print(f"  composed_distinct(best-k, coherent-gated) per step:", flush=True)
    for s in ladder_steps:
        r = results[s]
        print(f"    step {s:5d}: val_ce={r['val_ce']:.4f} best_composed_distinct={r['best_composed_distinct']} "
              f"max_single={r['max_single']} emergent={r['emergent']}", flush=True)
    tier = {"KNEE": "1 🟢 TRAINING-PHASE-TRANSITION (sharp knee at S*)",
            "SMOOTH": "0 🔴 SMOOTH (gradual ramp, no knee — training-sufficiency a continuous dial)",
            "NO-ONSET": "0 🔴 NO-ONSET (recombination does not switch on in this ladder at this capacity/corpus)"}[verdict]
    print(f"  F-TRAINING-PHASE-TRANSITION = {tier}", flush=True)
    print(f"  HONEST (a_scale_honest_scope): toy {nparam/1e6:.2f}M ByteGPT, English-dominant broad blend;", flush=True)
    print(f"          S* is capacity+corpus specific — NOT a universal threshold. p7 set-overlap (NOT perplexity), seed 7.", flush=True)

    out = {"hypothesis": "H_1132_recombination_training_phase_transition",
           "param_count": nparam, "blend_mb": a.blend_mb, "ladder_steps": ladder_steps,
           "config": {"d":a.d,"n_layer":a.n_layer,"n_head":a.n_head,"block":a.block,
                      "bs":a.bs,"accum":a.accum,"lr":a.lr},
           "per_step": results, "verdict": verdict, "knee_analysis": knee_info,
           "F_TRAINING_PHASE_TRANSITION": tier}
    json.dump(out, open("/tmp/h1132_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done] /tmp/h1132_result.json", flush=True)


if __name__ == "__main__": main()
