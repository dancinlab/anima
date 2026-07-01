"""
H_1145 — ANCHOR-GROUNDING REDUCES FABRICATION
a_kosmos anchors carry REAL text into context (generator L3 slot). Does prepending
a REAL corpus line (anchor) GROUND generation and CUT corpus-absent fabrication vs
a bare (no-anchor) prompt?

FROZEN FALSIFIER (pre-registered, deterministic, p7-respecting):
  Object measured = FABRICATION RATE = corpus-absent content-ngram fraction
  (H_1140 / H_1141 `corpus_absent` grep metric) over a fixed set of idea-prompts.
  Measured per condition, matched seeds:
    - ANCHOR-OFF  : bare idea-prompt
    - ANCHOR-ON   : a REAL corpus line prepended to the idea-prompt
    - ANCHOR-RAND : a shuffled-real-word salad of the SAME length prepended (control)

  FALSIFIER: fabrication(anchor-on) < fabrication(anchor-off) with Cohen's d >= 0.8.
  CONTROL:   the random-anchor must NOT reduce fabrication like the real anchor
             (real-vs-random Cohen's d >= 0.8 in the grounding direction) — proves
             the effect is GROUNDING, not mere context-length.

  H_1145 SUPPORTED iff real-anchor cuts fabrication d>=0.8 (vs none)
                       AND real-anchor beats random-anchor d>=0.8.
  CLOSED-NEGATIVE (a_paper_negative_ok) otherwise (no grounding effect, OR the
  effect is mere context-length and the random salad cuts fabrication just as well).

toy-scope (a_scale_honest_scope): tiny ByteGPT d256/4L, CPU, en slice — scale-up to
the real anima 7B + live kosmos_io anchor slot is the next rung, UNVERIFIED here.

Reuse: H_1142 trainer/model/corpus-loader VERBATIM; H_1141 corpus_absent grep metric.
"""
import os, sys, math, json, time, random, re as _re, subprocess
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

SEED = 7
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
DEV = "cpu"  # GPU on summer is busy (a_dont_kill_live_compute) — isolate on CPU
CORPUS = "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt"
EN_SLICE_BYTES = 24 * 1024 * 1024   # first ~24MB = English block (corpus order en,zh,ru,ja,ko)
BLOCK = 192; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256   # BLOCK 192 so anchor AND a
STEPS = 1500; BS = 16; LR = 3e-4                            # long-enough generation co-fit
GEN_LEN = 96; GEN_TEMP = 0.85; TOPK = 40   # 96-byte gen => enough real-dict content n-grams
SEEDS = tuple(range(7, 27))          # 20 matched seeds — 12 prompts x 20 = 240 combos so the
                                     # ~8%-scorable toy yield still clears MIN_PAIRS (cut3 had 5/60)
ANCHOR_CHARS = 40                    # real-anchor prefix length; random salad matched to this
MIN_PAIRS = 8                        # statistical-power floor: <MIN_PAIRS => INSUFFICIENT (not a verdict)
# context budget kept by generate(): BLOCK-GEN_LEN-1 = 95 bytes. A 40-char anchor +
# "\n" + a ~30-char base prompt = ~71 bytes < 95 => the anchor SURVIVES truncation AND the
# 96-byte continuation yields scorable content n-grams.
# DEFECT LADDER (fixed BEFORE terminal scoring, a_completeness_over_cheap / H_1061 lesson):
#   cut1 ANCHOR=90/GEN=90 BLOCK=128 keep=37 -> anchor truncated out -> all 3 identical, d=0.0
#         (context-window artifact, NOT a true negative).
#   cut2 ANCHOR=34/GEN=48 BLOCK=128 keep=79 -> anchor survives (guard 12/12) BUT GEN=48 too
#         short -> only 1/60 triples had content in all 3 conditions -> n_pairs=1, d=NaN
#         (measurement-power defect, NOT a true negative).
#   cut3 (this) BLOCK=192/GEN=96/ANCHOR=40 keep=95 -> anchor survives AND long gen -> power.


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


# ---------------- corpus-absent fabrication metric (H_1141 VERBATIM) ----------------
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


# ---------------- dict + kwr (H_1142 VERBATIM) ----------------
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


# ---------------- idea-prompts (H_1141 IDEA_PROMPTS extended to ~12) ----------------
IDEA_PROMPTS = [
    # short (<=40 char) so the anchor co-fits the BLOCK=128 window (cf budget note above)
    "Silence and the engine mean ",
    "When memory meets distant minds, ",
    "Consciousness and silence make ",
    "The tension between cells becomes ",
    "A dream and a distant mind merge to ",
    "Memory and tension together create ",
    "When the engine remembers, it ",
    "Distant minds and thought form ",
    "The field between two cells gives ",
    "Where curiosity meets the anchor, ",
    "A repulsion field and a mind make ",
    "When growth and forgetting balance, ",
]


# ---------------- anchor construction ----------------
def pick_real_anchors(raw_text, n):
    """Real corpus lines (>=60 ascii chars) — these literally exist in the corpus."""
    rng = random.Random(SEED + 101)
    lines = [ln.strip() for ln in raw_text.split("\n")
             if len(ln.strip()) >= 60 and ln.strip().isascii()]
    rng.shuffle(lines)
    return [ln[:ANCHOR_CHARS] for ln in lines[:n]]

def make_random_anchor(real_anchor, rng):
    """Shuffled-real-word salad: SAME words as the real anchor, order scrambled
    (and re-drawn from a corpus-word pool) so the SEQUENCE is corpus-absent but
    the length / byte-stats / vocabulary match. Pure context-length control."""
    words = [w for w in _re.findall(r"[A-Za-z]+", real_anchor) if len(w) >= 2]
    if len(words) < 2:
        words = ["the", "of", "and", "to", "a", "in", "is", "that", "for", "with"]
    salad, out = [], ""
    target = len(real_anchor)
    pool = list(words)
    while len(out) < target:
        salad.append(rng.choice(pool)); out = " ".join(salad)
    return out[:target]


# ---------------- generation ----------------
@torch.no_grad()
def generate(m, prompt, seed, max_new=GEN_LEN):
    enc = prompt.encode("utf-8", "ignore")[-(BLOCK - max_new - 1):]
    ids = torch.tensor(list(enc), dtype=torch.long, device=DEV)[None]
    g = torch.Generator(device=DEV).manual_seed(seed)
    out = []
    for _ in range(max_new):
        ctx = ids[:, -BLOCK:]
        logits, _ = m(ctx)
        probs = logits[:, -1, :] / GEN_TEMP
        v, i = torch.topk(probs, TOPK)
        pr = F.softmax(v, dim=-1)
        nxt = i.gather(-1, torch.multinomial(pr, 1, generator=g))
        ids = torch.cat([ids, nxt], dim=1); out.append(int(nxt.item()))
    return bytes(out).decode("utf-8", "ignore")


def fabrication_rate(text, anchor_text, dict_words, corpus_paths):
    """Corpus-absent content-ngram fraction of the GENERATED continuation ONLY.
    n-grams that also appear in the anchor text are excluded so the anchor's own
    (real) content can't depress the score artificially — we score what the model
    FABRICATED beyond the grounding anchor."""
    anchor_grams = content_ngrams(anchor_text or "", dict_words)
    grams = content_ngrams(text, dict_words) - anchor_grams
    if not grams:
        return None, 0, 0           # no content -> undefined, drop from analysis
    n_absent = sum(1 for g in grams if corpus_absent(g, corpus_paths))
    return n_absent / len(grams), n_absent, len(grams)


def cohens_d_paired(a, b):
    """Paired Cohen's d for (a - b): mean diff / sd of diffs. Positive => a > b."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    diff = a - b
    sd = diff.std(ddof=1)
    if sd == 0:
        return float("inf") if diff.mean() > 0 else (float("-inf") if diff.mean() < 0 else 0.0)
    return float(diff.mean() / sd)


def main():
    print("=== H_1145 anchor-grounding reduces fabrication ===", flush=True)
    with open(CORPUS, "rb") as f:
        raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8)
    text = raw.decode("utf-8", "ignore")
    from collections import Counter
    cw = Counter(w for w in ''.join(c if c.isalpha() else ' ' for c in text.lower()).split() if len(w) >= 3)
    corpus_words = {w for w, c in cw.items() if c >= 5}
    dct, dct_src = load_dict(corpus_words)
    corpus_paths = [CORPUS]

    print("\n--- training tiny ByteGPT (en slice) ---", flush=True)
    m = train_model(data)

    # one real anchor + matched random salad per prompt (fixed across seeds)
    real_anchors = pick_real_anchors(text, len(IDEA_PROMPTS))
    rng = random.Random(SEED + 202)
    rand_anchors = [make_random_anchor(ra, rng) for ra in real_anchors]
    # sanity: real anchors are corpus-present, random salads are corpus-absent sequences
    print(f"[anchors] {len(real_anchors)} real corpus lines + matched random salads", flush=True)
    print(f"  e.g. REAL : {real_anchors[0]!r}", flush=True)
    print(f"       RAND : {rand_anchors[0]!r}", flush=True)

    # ── ANTI-DEFECT GUARD (H_1061/H_1066 lesson): the anchor must ACTUALLY survive the
    #    BLOCK truncation, else the falsifier is never tested (the first cut's d=0.0 was
    #    exactly this defect). For every prompt, the truncated real-anchor context must
    #    (a) contain anchor bytes and (b) DIFFER from the bare-prompt truncated context.
    keep = BLOCK - GEN_LEN - 1
    n_survive = 0
    for pi, base in enumerate(IDEA_PROMPTS):
        ra = real_anchors[pi]
        ctx_real = (ra + "\n" + base).encode("utf-8", "ignore")[-keep:]
        ctx_bare = base.encode("utf-8", "ignore")[-keep:]
        anchor_head = ra.encode("utf-8", "ignore")[:12]
        if anchor_head in ctx_real and ctx_real != ctx_bare:
            n_survive += 1
    print(f"[guard] anchor survives truncation in {n_survive}/{len(IDEA_PROMPTS)} prompts "
          f"(keep={keep} bytes)", flush=True)
    if n_survive < len(IDEA_PROMPTS):
        print("[guard] FATAL: anchor does NOT reach the model context — verdict would be a "
              "context-window artifact, NOT a true negative. Aborting before scoring "
              "(a_completeness_over_cheap).", flush=True)
        json.dump({"H": "H_1145", "aborted": True,
                   "reason": "anchor truncated out of context window — construction defect",
                   "n_survive": n_survive, "keep_bytes": keep},
                  open("/tmp/h1145_result.json", "w"), ensure_ascii=False, indent=2)
        sys.exit(1)

    # paired measurement: per (prompt, seed) one value per condition
    none_rates, real_rates, rand_rates = [], [], []
    samples = {"none": [], "real": [], "rand": []}
    n_pairs = 0
    for pi, base in enumerate(IDEA_PROMPTS):
        ra, sa = real_anchors[pi], rand_anchors[pi]
        for sd in SEEDS:
            g_none = generate(m, base, sd)
            g_real = generate(m, ra + "\n" + base, sd)
            g_rand = generate(m, sa + "\n" + base, sd)
            f_none, _, dn = fabrication_rate(g_none, None, dct, corpus_paths)
            f_real, _, dr = fabrication_rate(g_real, ra, dct, corpus_paths)
            f_rand, _, dd = fabrication_rate(g_rand, sa, dct, corpus_paths)
            # paired: keep the triple only if ALL THREE produced scorable content
            if f_none is None or f_real is None or f_rand is None:
                continue
            none_rates.append(f_none); real_rates.append(f_real); rand_rates.append(f_rand)
            n_pairs += 1
            if len(samples["none"]) < 4:
                samples["none"].append({"prompt": base, "seed": sd, "fab": round(f_none, 3), "text": g_none[:90]})
                samples["real"].append({"anchor": ra, "seed": sd, "fab": round(f_real, 3), "text": g_real[:90]})
                samples["rand"].append({"anchor": sa, "seed": sd, "fab": round(f_rand, 3), "text": g_rand[:90]})
            print(f"  [p{pi} s{sd}] none={f_none:.3f}({dn}) real={f_real:.3f}({dr}) rand={f_rand:.3f}({dd})", flush=True)

    mean_none = float(np.mean(none_rates)) if none_rates else float("nan")
    mean_real = float(np.mean(real_rates)) if real_rates else float("nan")
    mean_rand = float(np.mean(rand_rates)) if rand_rates else float("nan")

    # frozen falsifier: real cuts fabrication vs none (d>=0.8 in reduction direction)
    # diffs measured as (none - real) so POSITIVE d => real LOWER => grounding.
    d_real_vs_none = cohens_d_paired(none_rates, real_rates)   # >0 => real fabricates less
    d_real_vs_rand = cohens_d_paired(rand_rates, real_rates)   # >0 => real fabricates less than random salad

    grounds = (mean_real < mean_none) and (d_real_vs_none >= 0.8)
    beats_random = (mean_real < mean_rand) and (d_real_vs_rand >= 0.8)
    insufficient = n_pairs < MIN_PAIRS
    supported = bool(grounds and beats_random and not insufficient)

    if insufficient:
        ruling = (f"INSUFFICIENT-POWER: only {n_pairs} scorable paired triples (< {MIN_PAIRS}) — the "
                  "toy byte-LM emits too little real-dict content to test the d>=0.8 falsifier; NOT a "
                  "terminal verdict (re-run with more power / a stronger backbone). a_scale_honest_scope")
    elif supported:
        ruling = "GROUNDED: a real anchor cuts corpus-absent fabrication AND beats a length-matched random salad"
    elif grounds and not beats_random:
        ruling = ("CLOSED-NEGATIVE: real anchor lowers fabrication but does NOT beat the random-salad control "
                  "(effect is mere context-length, not grounding)")
    else:
        ruling = "CLOSED-NEGATIVE: a real anchor does NOT cut corpus-absent fabrication (d<0.8) — no grounding effect"

    verdict = {
        "H": "H_1145", "title": "anchor-grounding reduces fabrication",
        "dict_source": dct_src,
        "n_pairs": n_pairs,
        "min_pairs_for_power": MIN_PAIRS,
        "insufficient_power": bool(insufficient),
        "fabrication": {
            "anchor_off_mean": mean_none,
            "anchor_on_real_mean": mean_real,
            "anchor_rand_control_mean": mean_rand,
        },
        "falsifier": {
            "cohen_d_real_vs_none": d_real_vs_none, "bar": 0.8,
            "real_cuts_fabrication": bool(grounds),
        },
        "control": {
            "cohen_d_real_vs_random": d_real_vs_rand, "bar": 0.8,
            "real_beats_random": bool(beats_random),
            "note": "random = shuffled-real-word salad, same length as the real anchor (context-length control)",
        },
        "supported": supported,
        "ruling": ruling,
        "samples": samples,
        "scope": ("toy ByteGPT d256/4L, CPU, en 24MB slice; anchor = prepended corpus line (proxy for the "
                  "kosmos_io->generator L3 slot) — scale-up to anima-7B + live anchor wiring UNVERIFIED "
                  "(a_scale_honest_scope)"),
        "config": {"d": D, "n_layer": NLAYER, "block": BLOCK, "steps": STEPS,
                   "n_prompts": len(IDEA_PROMPTS), "seeds": list(SEEDS), "gen_len": GEN_LEN,
                   "anchor_chars": ANCHOR_CHARS, "seed": SEED},
    }
    print("\n=== VERDICT ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1145_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done] /tmp/h1145_result.json", flush=True)


if __name__ == "__main__":
    main()
