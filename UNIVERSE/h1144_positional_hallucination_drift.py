"""
H_1144 — POSITIONAL HALLUCINATION DRIFT
"A byte-LM ALWAYS continues (no refusal token, H_1142 idea-9). Does it stay
corpus-grounded NEAR the prompt and then DRIFT into fabrication as token position
grows?"

FROZEN FALSIFIER (pre-registered in .discoveries/1144_positional_hallucination_drift.tape —
NO threshold moved, a_paper_negative_ok / a7b_pass spirit):

  METRIC: generate >= GEN_LEN(>=200) tokens from in-corpus prompts. Bin the
          generated continuation by TOKEN POSITION. In each bin, extract content
          n-grams (consecutive real-dict >=3ch words → bi/tri-grams, H_1140) and
          compute the FABRICATION RATE = fraction of those n-grams that are
          corpus-ABSENT (H_1141 corpus_absent VERBATIM: deterministic grep -E -i,
          punct/newline-tolerant).

  F1 MONOTONE   — Spearman(position_bin, fabrication_rate) >= +0.50.
  F2 EFFECT     — late-vs-early Cohen's d >= 0.80 (late bins fabricate more than
                  early bins). coherence(kwr) need NOT drop — fabrication != garble.

  H_1144 SUPPORTED iff F1 AND F2 (monotone drift).
  CLOSED-NEGATIVE (a_paper_negative_ok) iff flat / non-monotone (fabrication is
  position-INDEPENDENT — the LM is uniformly grounded OR uniformly fabricating).

  CONTROL: in-corpus VERBATIM continuation (feed a real corpus line, measure the
           SAME per-position metric on the real bytes). Must stay ~0 fabrication at
           ALL positions — else the per-position metric is a position ARTIFACT and
           the verdict is void.

toy-scope (a_scale_honest_scope): tiny ByteGPT d256/4L, CPU, en slice — scale-up
to the real anima 7B is the next rung, UNVERIFIED here.

REUSE: H_1142 trainer/arch/corpus-loader VERBATIM; H_1141 corpus_absent/content
n-gram extraction VERBATIM.
"""
import os, sys, math, json, time, random, re as _re, subprocess
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

SEED = 7
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
DEV = "cpu"  # GPU on summer is busy (a_dont_kill_live_compute) — isolate on CPU
CORPUS = "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt"
EN_SLICE_BYTES = 24 * 1024 * 1024   # first ~24MB = English block (corpus order en,zh,ru,ja,ko)
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 1500; BS = 16; LR = 3e-4
# H_1144 generation: LONG continuations so position-binning is meaningful.
GEN_LEN = 256            # >= 200 tokens (frozen spec)
N_PROMPTS = 20           # ~20 in-corpus prompts
GEN_TEMP = 0.85; TOPK = 40
N_BINS = 8               # token-position bins over the GEN_LEN window
EARLY_BINS = 3; LATE_BINS = 3   # late-vs-early Cohen's d uses first 3 vs last 3 bins


# ---------------- model (H_1142 VERBATIM) ----------------
class Block(nn.Module):
    def __init__(s, d, h):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.ln2 = nn.LayerNorm(d)
        s.attn = nn.MultiheadAttention(d, h, batch_first=True)
        s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d))
    def forward(s, x, mask):
        a, _ = s.attn(s.ln1(x), s.ln1(x), s.ln1(x), attn_mask=mask, need_weights=False)
        x = x + a; x = x + s.mlp(s.ln2(x)); return x

class ByteGPT(nn.Module):
    def __init__(s, vocab=VOCAB, d=D, n_layer=NLAYER, n_head=NHEAD, block=BLOCK):
        super().__init__()
        s.block = block
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d)
        s.blocks = nn.ModuleList([Block(d, n_head) for _ in range(n_layer)])
        s.lnf = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False)
    def forward(s, idx, targets=None):
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = s.tok(idx) + s.pos(pos)[None]
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        logits = s.head(s.lnf(x))
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
        return logits, loss


def batch(data, block, bs, dev):
    ix = torch.randint(0, data.numel() - block - 1, (bs,))
    x = torch.stack([data[i:i+block] for i in ix]).long()
    y = torch.stack([data[i+1:i+block+1] for i in ix]).long()
    return x.to(dev), y.to(dev)


def train_model(data):
    m = ByteGPT().to(DEV); m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=LR, betas=(0.9, 0.95), weight_decay=0.1)
    t0 = time.time()
    for st in range(STEPS):
        lr_t = LR * min(1.0, (st+1)/80) * (0.5*(1+math.cos(math.pi*min(1.0, st/STEPS))))
        for g in opt.param_groups: g["lr"] = lr_t
        x, y = batch(data, BLOCK, BS, DEV)
        _, l = m(x, y)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % 250 == 0 or st == STEPS-1:
            print(f"  [train] step {st} ce={l.item():.4f} {(time.time()-t0)/60:.1f}min", flush=True)
    m.eval(); return m


# ---------------- dict + coherence (H_1142 VERBATIM) ----------------
def load_dict(corpus_words):
    for p in ("/usr/share/dict/words", "/usr/share/dict/american-english"):
        if os.path.exists(p):
            with open(p, encoding="utf-8", errors="ignore") as f:
                d = {w.strip().lower() for w in f if w.strip().isalpha() and len(w.strip()) >= 2}
            if len(d) > 1000:
                print(f"[dict] {p} ({len(d)} words)", flush=True); return d, "system-dict"
    print(f"[dict] system dict absent -> corpus-frequent fallback ({len(corpus_words)} words)", flush=True)
    return corpus_words, "corpus-freq-fallback"


def known_word_ratio(text, dct):
    words = [w for w in ''.join(c if c.isalpha() else ' ' for c in text.lower()).split() if len(w) >= 3]
    if not words: return 0.0
    return sum(1 for w in words if w in dct) / len(words)


# ---------------- H_1141 content n-grams + corpus-absence VERBATIM ----------------
_STOP = set("""the a an of to and in is it that this for on with as are was be by at from or not
but his her they we you i he she them me my your our their its do does did has have had will
would can could should may might must shall when where what which who whom how why all any some
no one two then than into out up down over under more most less about so very just only own same
such each few other been here there now""".split())

def content_ngrams(text, dict_words):
    toks = _re.findall(r"[A-Za-z]+", text.lower())
    grams = set()
    for n in (2, 3):
        for i in range(len(toks) - n + 1):
            g = toks[i:i + n]
            if not all(len(w) >= 3 and w in dict_words for w in g): continue
            if all(w in _STOP for w in g): continue
            grams.add(" ".join(g))
    return grams

def _gram_regex(ngram):
    ws = ngram.split(" ")
    return r"(^|[^A-Za-z])" + r"[^A-Za-z]+".join(_re.escape(w) for w in ws) + r"([^A-Za-z]|$)"

def corpus_absent(ngram, corpus_paths):
    rx = _gram_regex(ngram)
    for p in corpus_paths:
        if not os.path.exists(p): continue
        r = subprocess.run(["grep", "-E", "-i", "-m", "1", "-q", rx, p])
        if r.returncode == 0: return False
    return True


# ---------------- prompts: in-corpus line prefixes ----------------
def build_prompts(raw_text):
    rng = random.Random(SEED)
    lines = [ln.strip() for ln in raw_text.split("\n") if len(ln.strip()) >= 60 and ln.strip().isascii()]
    rng.shuffle(lines)
    # ~48-char in-corpus prefix as the grounded prompt (the model continues it)
    return [ln[:48] for ln in lines[:N_PROMPTS]], lines


# ---------------- generation: long continuation, byte-position kept ----------------
@torch.no_grad()
def generate_long(m, prompt):
    ids = torch.tensor([b for b in prompt.encode("utf-8", "ignore")[:BLOCK-1]],
                       dtype=torch.long, device=DEV)[None]
    g = torch.Generator(device=DEV).manual_seed(SEED + len(prompt))
    out = []
    for _ in range(GEN_LEN):
        ctx = ids[:, -BLOCK:]
        logits, _ = m(ctx)
        lg = logits[:, -1, :] / GEN_TEMP
        v, i = torch.topk(lg, TOPK)
        pr = F.softmax(v, dim=-1)
        nxt = i.gather(-1, torch.multinomial(pr, 1, generator=g))
        ids = torch.cat([ids, nxt], dim=1); out.append(int(nxt.item()))
    return bytes(out)   # raw generated bytes (excludes the prompt), len == GEN_LEN


# ---------------- per-position fabrication binning ----------------
def per_position_fabrication(gen_byte_seqs, dict_words, corpus_paths):
    """gen_byte_seqs: list of GEN_LEN-byte continuations. Bin each by BYTE POSITION
    into N_BINS, extract content n-grams WITHIN each bin, then per bin compute
    fabrication = corpus-absent fraction of distinct content n-grams. A bin's n-gram
    is positioned by the BYTE OFFSET of its FIRST token within the continuation."""
    bin_edges = np.linspace(0, GEN_LEN, N_BINS + 1).astype(int)
    # accumulate per-bin sets across prompts (distinct n-grams) so absence is computed once
    bin_grams = [dict() for _ in range(N_BINS)]   # ngram -> first-seen example
    for gb in gen_byte_seqs:
        text = gb.decode("utf-8", "ignore")
        # tokens with byte offsets, then bin each n-gram by its first-token offset
        toks = _tokens_with_offsets(gb)
        # build bi/tri-grams from consecutive real-dict >=3ch words, bin by 1st-token offset
        for n in (2, 3):
            for i in range(len(toks) - n + 1):
                window = toks[i:i + n]
                ws = [w for (w, _) in window]
                if not all(len(w) >= 3 and w in dict_words for w in ws): continue
                if all(w in _STOP for w in ws): continue
                first_off = window[0][1]
                b = min(N_BINS - 1, int(np.searchsorted(bin_edges, first_off, side="right") - 1))
                b = max(0, b)
                gram = " ".join(ws)
                bin_grams[b].setdefault(gram, text[:60])
    # compute fabrication rate per bin
    rates, counts, novels = [], [], []
    for b in range(N_BINS):
        grams = list(bin_grams[b].keys())
        if not grams:
            rates.append(float("nan")); counts.append(0); novels.append(0); continue
        n_abs = sum(1 for gram in grams if corpus_absent(gram, corpus_paths))
        rates.append(n_abs / len(grams)); counts.append(len(grams)); novels.append(n_abs)
    return rates, counts, novels, bin_grams, bin_edges.tolist()


def _tokens_with_offsets(gb):
    """list of (lowercased Latin word, byte-start-offset) over the byte sequence gb."""
    text = gb.decode("utf-8", "ignore")
    toks = []
    for mobj in _re.finditer(r"[A-Za-z]+", text):
        w = mobj.group(0).lower()
        # byte offset = byte length of the prefix up to mobj.start() (utf-8); for ASCII == char idx
        boff = len(text[:mobj.start()].encode("utf-8", "ignore"))
        toks.append((w, boff))
    return toks


def spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean()
    den = math.sqrt((ra*ra).sum() * (rb*rb).sum())
    return float((ra*rb).sum()/den) if den else 0.0


def cohens_d(late, early):
    late = np.asarray(late, float); early = np.asarray(early, float)
    nl, ne = len(late), len(early)
    if nl < 1 or ne < 1: return float("nan")
    vl, ve = (late.var(ddof=1) if nl > 1 else 0.0), (early.var(ddof=1) if ne > 1 else 0.0)
    sp = math.sqrt(((nl-1)*vl + (ne-1)*ve) / max(1, nl+ne-2))
    if sp == 0:
        return float("inf") if late.mean() > early.mean() else (0.0 if late.mean()==early.mean() else float("-inf"))
    return (late.mean() - early.mean()) / sp


def main():
    print("=== H_1144 positional hallucination drift ===", flush=True)
    with open(CORPUS, "rb") as f:
        raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8)
    text = raw.decode("utf-8", "ignore")
    from collections import Counter
    cw = Counter(w for w in ''.join(c if c.isalpha() else ' ' for c in text.lower()).split() if len(w) >= 3)
    corpus_words = {w for w, c in cw.items() if c >= 5}
    dct, dct_src = load_dict(corpus_words)
    corpus_paths = [CORPUS]

    prompts, all_lines = build_prompts(text)
    print(f"[prompts] {len(prompts)} in-corpus line prefixes (~48ch)", flush=True)

    print("\n--- training tiny ByteGPT (en slice) ---", flush=True)
    m = train_model(data)

    # ── generate long continuations from in-corpus prompts ──
    print("\n--- generating long continuations (GEN_LEN={}) ---".format(GEN_LEN), flush=True)
    gen_seqs = []; kwrs = []
    for j, p in enumerate(prompts):
        gb = generate_long(m, p)
        gen_seqs.append(gb)
        t = gb.decode("utf-8", "ignore")
        kwrs.append(known_word_ratio(t, dct))
        if j < 3:
            print(f"  [gen {j}] kwr={kwrs[-1]:.2f} prompt={p[:40]!r} -> {t[:90]!r}", flush=True)
    print(f"  mean kwr over {len(gen_seqs)} gens = {np.mean(kwrs):.3f} (fabrication != garble)", flush=True)

    rates, counts, novels, bin_grams, bin_edges = per_position_fabrication(gen_seqs, dct, corpus_paths)
    print("\n--- per-position fabrication (generated) ---", flush=True)
    for b in range(N_BINS):
        print(f"  bin {b} (byte {bin_edges[b]}-{bin_edges[b+1]}): "
              f"fab_rate={rates[b] if not math.isnan(rates[b]) else 'NA'} "
              f"(absent {novels[b]}/{counts[b]} content n-grams)", flush=True)

    # F1 + F2 over bins that HAVE data
    valid = [b for b in range(N_BINS) if counts[b] > 0 and not math.isnan(rates[b])]
    xs = [b for b in valid]; ys = [rates[b] for b in valid]
    rho = spearman(xs, ys) if len(valid) >= 3 else float("nan")
    early_idx = valid[:EARLY_BINS]; late_idx = valid[-LATE_BINS:]
    d = cohens_d([rates[b] for b in late_idx], [rates[b] for b in early_idx]) if valid else float("nan")
    f1 = (not math.isnan(rho)) and rho >= 0.50
    f2 = (not math.isnan(d)) and d >= 0.80

    # ── CONTROL: in-corpus VERBATIM continuation, same per-position metric ──
    print("\n--- CONTROL: in-corpus verbatim continuations ---", flush=True)
    rng = random.Random(SEED + 1)
    long_lines = [ln for ln in all_lines if len(ln.encode("utf-8", "ignore")) >= GEN_LEN + 60]
    rng.shuffle(long_lines)
    ctrl_seqs = []
    for ln in long_lines[:N_PROMPTS]:
        body = ln.encode("utf-8", "ignore")[48:48 + GEN_LEN]  # bytes AFTER the 48ch prefix == verbatim continuation
        if len(body) == GEN_LEN:
            ctrl_seqs.append(body)
    print(f"  {len(ctrl_seqs)} verbatim continuation segments", flush=True)
    c_rates, c_counts, c_novels, _, _ = per_position_fabrication(ctrl_seqs, dct, corpus_paths)
    c_valid = [b for b in range(N_BINS) if c_counts[b] > 0 and not math.isnan(c_rates[b])]
    c_all_rates = [c_rates[b] for b in c_valid]
    control_max = max(c_all_rates) if c_all_rates else 0.0
    control_mean = float(np.mean(c_all_rates)) if c_all_rates else 0.0
    for b in range(N_BINS):
        print(f"  ctrl bin {b}: fab_rate={c_rates[b] if not math.isnan(c_rates[b]) else 'NA'} "
              f"(absent {c_novels[b]}/{c_counts[b]})", flush=True)
    # control valid iff verbatim continuation stays ~0 fabrication at ALL positions
    CONTROL_TOL = 0.10
    control_ok = control_max <= CONTROL_TOL
    print(f"  CONTROL max fab_rate over positions = {control_max:.4f} (mean {control_mean:.4f}); "
          f"<= {CONTROL_TOL} ? {control_ok} (verbatim must stay ~0 => metric not a position artifact)", flush=True)

    supported = bool(f1 and f2 and control_ok)
    if not control_ok:
        ruling = ("VOID-CONTROL: in-corpus verbatim continuation also fabricates "
                  "(metric is a position artifact) — no valid verdict")
    elif supported:
        ruling = "SUPPORTED: fabrication rises monotonically with token position (positional hallucination drift)"
    else:
        ruling = ("CLOSED-NEGATIVE: fabrication is position-INDEPENDENT (no monotone drift) — "
                  "the byte-LM is uniformly (un)grounded across the continuation, not progressively drifting")

    verdict = {
        "H": "H_1144", "title": "positional hallucination drift",
        "dict_source": dct_src,
        "n_prompts": len(prompts), "gen_len": GEN_LEN, "n_bins": N_BINS,
        "mean_kwr": round(float(np.mean(kwrs)), 4),
        "per_bin": [
            {"bin": b, "byte_lo": bin_edges[b], "byte_hi": bin_edges[b+1],
             "fabrication_rate": (None if math.isnan(rates[b]) else round(rates[b], 4)),
             "n_content_ngrams": counts[b], "n_absent": novels[b]}
            for b in range(N_BINS)
        ],
        "F1_monotone": {"spearman_pos_fabrication": (None if math.isnan(rho) else round(rho, 4)),
                        "bar": 0.50, "pass": bool(f1)},
        "F2_effect": {"cohen_d_late_vs_early": (None if math.isnan(d) else round(d, 4)),
                      "early_bins": early_idx, "late_bins": late_idx, "bar": 0.80, "pass": bool(f2)},
        "control": {"per_bin_rate": [None if math.isnan(c_rates[b]) else round(c_rates[b], 4) for b in range(N_BINS)],
                    "per_bin_count": c_counts,
                    "max_rate": round(control_max, 4), "mean_rate": round(control_mean, 4),
                    "tol": CONTROL_TOL, "ok": bool(control_ok),
                    "note": "in-corpus verbatim continuation; must stay ~0 fabrication at ALL positions"},
        "supported": supported,
        "ruling": ruling,
        "scope": "toy ByteGPT d256/4L, CPU, en slice — scale-up to anima-7B UNVERIFIED (a_scale_honest_scope)",
        "config": {"d": D, "n_layer": NLAYER, "block": BLOCK, "steps": STEPS,
                   "n_prompts": N_PROMPTS, "gen_len": GEN_LEN, "n_bins": N_BINS,
                   "gen_temp": GEN_TEMP, "topk": TOPK, "seed": SEED},
    }
    print("\n=== VERDICT ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1144_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done] /tmp/h1144_result.json", flush=True)


if __name__ == "__main__":
    main()
