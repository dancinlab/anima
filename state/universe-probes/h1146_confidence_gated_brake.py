"""
H_1146 — CONFIDENCE-GATED EMISSION BRAKE CUTS HALLUCINATION (causal) == H_1135

SEED: H_1142 F2 PASSED — the substrate KNOWS its own output coherence
(Spearman(confidence, kwr) = +0.552 > 0 : low next-byte entropy <=> coherent
output). H_1146 asks the CAUSAL forward question: if we THRESHOLD on that
confidence signal during generation to SUPPRESS/REGENERATE low-confidence
(high-entropy) spans, does fabrication CAUSALLY drop?

FABRICATION (H_1140 metric): fraction of a generation's content n-grams
(consecutive real-dict >=3-char words, 2/3-grams) that are ABSENT from the
ENTIRE training corpus (deterministic grep -E -i, H_1141 corpus_absent).
High fabrication = the model emits coherent-looking word-sequences it never saw
= hallucination/confabulation surface.

BRAKE (the intervention): generation proceeds in GEN_LEN windows. After drawing
a window, if its mean next-byte entropy exceeds a per-run percentile-p threshold,
RESAMPLE that window (up to K retries, each with a different generator seed) and
keep the LOWEST-ENTROPY draw. The window is then committed and generation
continues. Confidence drives WHICH windows get resampled.

FROZEN FALSIFIER (pre-registered, deterministic, p7-respecting — no threshold moved):
  fabrication(brake-on) < fabrication(brake-off) with paired Cohen's d >= 0.8
  AND coherence (kwr) NOT degraded (DKWR_BAR: mean kwr drop <= 0.05 AND
  no paired d-degradation >= 0.8 in the WRONG direction) — the brake must remove
  FABRICATION, not signal.

CONTROL (RANDOM-gate): resample on a COIN-FLIP (NOT on entropy), matched to the
confidence-gate's realized resample budget (same number of windows resampled, same
K). The random-gate must NOT cut fabrication like the confidence-gate
(random d_fab < confidence d_fab AND random fails the d>=0.8 bar) — proving the
SIGNAL drives the reduction, not mere extra sampling.

H_1146 SUPPORTED iff confidence-gate d_fab >= 0.8 AND confidence d_fab > random d_fab
AND random-gate does NOT itself clear d>=0.8 AND kwr NOT degraded.
CLOSED-NEGATIVE (a_paper_negative_ok) otherwise.

toy-scope (a_scale_honest_scope): tiny ByteGPT d256/4L, CPU, en slice — scale-up
to the real anima 7B is the next rung, UNVERIFIED here.
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
GEN_TEMP = 0.85; TOPK = 40

# brake config
WIN = 24            # GEN_LEN window length (bytes per resample unit)
N_WIN = 5           # windows per generation -> 120 bytes generated content
PERCENTILE_P = 70   # window mean-entropy above this run-percentile => high-entropy => brake
K_RETRY = 3         # resample budget per braked window (keep lowest-entropy draw)
N_SEEDS = 3         # generation seeds per prompt (7,8,9)


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


# ---------------- dict / coherence / fabrication (H_1141 VERBATIM) ----------------
def load_real_dict(path="/usr/share/dict/words"):
    d = set()
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for ln in f:
                w = ln.strip().lower()
                if w: d.add(w)
    except FileNotFoundError:
        print(f"[warn] no real dict at {path}", file=sys.stderr)
    return d

def kwr_realdict(text, dict_words):
    latin = _re.findall(r"[A-Za-z]+", text.lower())
    if not latin: return 0.0
    known = sum(1 for w in latin if w in dict_words)
    return known / len(latin)

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


# ---------------- windowed generation with entropy + brake ----------------
@torch.no_grad()
def _gen_window(m, ids, win_len, gen_seed):
    """Generate win_len bytes from ids[0]; return (new_ids, out_bytes, mean_entropy).
    Entropy machinery is H_1142's per-step next-byte entropy (nats) VERBATIM."""
    g = torch.Generator(device=DEV).manual_seed(gen_seed)
    ents, out = [], []
    cur = ids
    for _ in range(win_len):
        ctx = cur[:, -BLOCK:]
        logits, _ = m(ctx)
        logp = F.log_softmax(logits[:, -1, :], dim=-1)
        p = logp.exp()
        ent = float(-(p * logp).sum().item())   # nats — H_1142 confidence signal
        ents.append(ent)
        probs = (logits[:, -1, :] / GEN_TEMP)
        v, i = torch.topk(probs, TOPK)
        pr = F.softmax(v, dim=-1)
        nxt = i.gather(-1, torch.multinomial(pr, 1, generator=g))
        cur = torch.cat([cur, nxt], dim=1); out.append(int(nxt.item()))
    return cur, out, float(np.mean(ents))


@torch.no_grad()
def generate(m, prompt, base_seed, mode, ent_threshold, coin_p):
    """mode: 'off' | 'conf' | 'rand'.
    Returns dict(text, kwr-input bytes, mean_entropy, n_resampled).
    - off : draw each window once, commit.
    - conf: draw window; if mean_ent > ent_threshold, resample K times (new seeds),
            keep lowest-entropy draw.
    - rand: draw window; on a coin-flip (prob coin_p, signal-blind), resample K times,
            keep lowest-entropy draw (same budget, no entropy gate on WHETHER to brake).
    """
    ids = torch.tensor([b for b in prompt.encode("utf-8", "ignore")[:BLOCK - WIN*N_WIN - 1]],
                       dtype=torch.long, device=DEV)[None]
    rng = random.Random(base_seed * 1000 + 13)   # coin/seed stream, deterministic per (prompt,seed,mode)
    all_out = []; win_ents = []; n_resampled = 0
    for wi in range(N_WIN):
        first_seed = base_seed * 100003 + wi * 7919
        cand_ids, cand_out, cand_ent = _gen_window(m, ids, WIN, first_seed)
        brake = False
        if mode == "conf":
            brake = cand_ent > ent_threshold
        elif mode == "rand":
            brake = rng.random() < coin_p
        if brake:
            n_resampled += 1
            best = (cand_ent, cand_ids, cand_out)
            for r in range(K_RETRY):
                rs = first_seed + 104729 * (r + 1)
                r_ids, r_out, r_ent = _gen_window(m, ids, WIN, rs)
                if r_ent < best[0]:
                    best = (r_ent, r_ids, r_out)
            cand_ent, cand_ids, cand_out = best
        ids = cand_ids; all_out += cand_out; win_ents.append(cand_ent)
    text = bytes(all_out).decode("utf-8", "ignore")
    return {"text": text, "mean_entropy": float(np.mean(win_ents)), "n_resampled": n_resampled}


def cohens_d_paired(a, b):
    """Paired Cohen's d for (a - b): positive => a > b. d = mean(diff)/sd(diff)."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    diff = a - b
    sd = diff.std(ddof=1)
    if sd == 0:
        return 0.0 if diff.mean() == 0 else float(np.sign(diff.mean()) * 99.0)
    return float(diff.mean() / sd)


# ---------------- prompts (H_1141 idea-prompts + a few extra distant-concept fusions) ----------------
PROMPTS = [
    "Silence and the engine together mean ",
    "When memory meets distant minds, ",
    "Consciousness and silence combine into ",
    "The tension between cells and the engine becomes ",
    "If a dream and a distant mind merge, the result is ",
    "Memory and tension together create ",
    "When the engine remembers silence, it ",
    "Distant minds and consciousness form ",
    "The administrative council decided that ",
    "In the early history of the river valley, ",
    "A new theory of viability suggests that ",
    "The association for cleaning announced that ",
]


def fabrication_rate(text, dict_words, corpus_paths):
    """Fraction of content n-grams that are corpus-ABSENT (H_1140 fabrication)."""
    grams = content_ngrams(text, dict_words)
    if not grams:
        return None, 0, 0  # no scorable content
    absent = sum(1 for g in grams if corpus_absent(g, corpus_paths))
    return absent / len(grams), absent, len(grams)


def run_condition(m, mode, ent_threshold, coin_p, dict_words, corpus_paths, tag):
    fabs, kwrs, resamp = [], [], []
    keys = []
    for pi, prompt in enumerate(PROMPTS):
        for sd in (7, 8, 9):
            r = generate(m, prompt, sd, mode, ent_threshold, coin_p)
            fab, nab, ntot = fabrication_rate(r["text"], dict_words, corpus_paths)
            kwr = kwr_realdict(r["text"], dict_words)
            keys.append((pi, sd))
            fabs.append(fab); kwrs.append(kwr); resamp.append(r["n_resampled"])
            ftxt = "skip" if fab is None else f"{fab:.3f}"
            print(f"  [{tag} p{pi} s{sd}] fab={ftxt} ({nab}/{ntot}) kwr={kwr:.2f} "
                  f"resamp={r['n_resampled']} ent={r['mean_entropy']:.3f} :: {r['text'][:60]!r}",
                  flush=True)
    return {"keys": keys, "fab": fabs, "kwr": kwrs, "resamp": resamp}


def calibrate_threshold(m, dict_words, corpus_paths):
    """Run brake-off once, collect per-window mean entropies to set percentile-p threshold,
    and return the off-condition results (reused as baseline, identical seeds)."""
    # First pass: collect all window entropies under off-generation to compute the percentile.
    win_ent_pool = []
    for prompt in PROMPTS:
        for sd in (7, 8, 9):
            ids = torch.tensor([b for b in prompt.encode("utf-8", "ignore")[:BLOCK - WIN*N_WIN - 1]],
                               dtype=torch.long, device=DEV)[None]
            for wi in range(N_WIN):
                first_seed = sd * 100003 + wi * 7919
                ids, _out, ent = _gen_window(m, ids, WIN, first_seed)
                win_ent_pool.append(ent)
    thr = float(np.percentile(win_ent_pool, PERCENTILE_P))
    print(f"[calib] window-entropy percentile-{PERCENTILE_P} = {thr:.4f} "
          f"(pool n={len(win_ent_pool)}, min={min(win_ent_pool):.3f} max={max(win_ent_pool):.3f})",
          flush=True)
    return thr


def paired_stats(off, on, dict_words):
    """Align by key, drop pairs where either fab is None, compute paired d for fab and kwr."""
    okey = {k: i for i, k in enumerate(off["keys"])}
    fa, fb, ka, kb = [], [], [], []
    for j, k in enumerate(on["keys"]):
        i = okey[k]
        if off["fab"][i] is None or on["fab"][j] is None:
            continue
        fa.append(off["fab"][i]); fb.append(on["fab"][j])
        ka.append(off["kwr"][i]); kb.append(on["kwr"][j])
    n = len(fa)
    d_fab = cohens_d_paired(fa, fb)        # off - on ; positive => on REDUCES fabrication
    d_kwr_drop = cohens_d_paired(ka, kb)   # off - on ; positive => on DEGRADES coherence
    return {
        "n_pairs": n,
        "mean_fab_off": float(np.mean(fa)) if n else None,
        "mean_fab_on": float(np.mean(fb)) if n else None,
        "mean_kwr_off": float(np.mean(ka)) if n else None,
        "mean_kwr_on": float(np.mean(kb)) if n else None,
        "d_fab_reduction": d_fab,
        "d_kwr_degradation": d_kwr_drop,
    }


def main():
    print("=== H_1146 confidence-gated emission brake (== H_1135) ===", flush=True)
    corpus_paths = [CORPUS]
    with open(CORPUS, "rb") as f:
        raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8)
    dict_words = load_real_dict()
    print(f"[dict] /usr/share/dict/words ({len(dict_words)} words)", flush=True)

    print("\n--- training tiny ByteGPT (en slice) ---", flush=True)
    m = train_model(data)

    print("\n--- calibrating brake threshold (percentile of off-gen window entropy) ---", flush=True)
    ent_threshold = calibrate_threshold(m, dict_words, corpus_paths)

    print("\n--- condition: BRAKE-OFF (baseline) ---", flush=True)
    off = run_condition(m, "off", ent_threshold, 0.0, dict_words, corpus_paths, "off")

    # match random-gate's coin probability to the confidence-gate's realized brake rate.
    print("\n--- condition: CONFIDENCE-BRAKE ---", flush=True)
    conf = run_condition(m, "conf", ent_threshold, 0.0, dict_words, corpus_paths, "conf")
    conf_brake_rate = sum(conf["resamp"]) / (len(conf["resamp"]) * N_WIN)
    print(f"[budget] confidence-gate realized brake rate = {conf_brake_rate:.3f} "
          f"({sum(conf['resamp'])} windows / {len(conf['resamp'])*N_WIN})", flush=True)

    print("\n--- condition: RANDOM-BRAKE (control, matched budget) ---", flush=True)
    rand = run_condition(m, "rand", ent_threshold, conf_brake_rate, dict_words, corpus_paths, "rand")
    rand_brake_rate = sum(rand["resamp"]) / (len(rand["resamp"]) * N_WIN)
    print(f"[budget] random-gate realized brake rate = {rand_brake_rate:.3f} "
          f"({sum(rand['resamp'])} windows / {len(rand['resamp'])*N_WIN})", flush=True)

    conf_stats = paired_stats(off, conf, dict_words)
    rand_stats = paired_stats(off, rand, dict_words)

    # ----- frozen falsifier -----
    DFAB_BAR = 0.8
    DKWR_DROP_BAR = 0.8       # coherence "not degraded" => degradation d must NOT reach 0.8
    KWR_MEAN_DROP_BAR = 0.05  # and absolute mean kwr drop <= 0.05

    conf_cuts = conf_stats["d_fab_reduction"] >= DFAB_BAR
    beats_random = conf_stats["d_fab_reduction"] > rand_stats["d_fab_reduction"]
    random_does_not_clear = rand_stats["d_fab_reduction"] < DFAB_BAR
    kwr_mean_drop = (conf_stats["mean_kwr_off"] - conf_stats["mean_kwr_on"]) \
        if conf_stats["mean_kwr_off"] is not None else 0.0
    kwr_not_degraded = (conf_stats["d_kwr_degradation"] < DKWR_DROP_BAR) and (kwr_mean_drop <= KWR_MEAN_DROP_BAR)

    supported = bool(conf_cuts and beats_random and random_does_not_clear and kwr_not_degraded)

    if supported:
        ruling = ("SUPPORTED: confidence-gated brake CAUSALLY cuts fabrication "
                  f"(d={conf_stats['d_fab_reduction']:.3f}>={DFAB_BAR}), beats signal-blind "
                  f"random-gate (d={rand_stats['d_fab_reduction']:.3f}), coherence held "
                  f"(kwr drop={kwr_mean_drop:.3f})")
    else:
        reasons = []
        if not conf_cuts: reasons.append(f"confidence d_fab={conf_stats['d_fab_reduction']:.3f}<{DFAB_BAR}")
        if not beats_random: reasons.append(f"does NOT beat random ({conf_stats['d_fab_reduction']:.3f}<=({rand_stats['d_fab_reduction']:.3f}))")
        if not random_does_not_clear: reasons.append(f"random-gate ALSO clears bar (d={rand_stats['d_fab_reduction']:.3f}>= {DFAB_BAR}: effect=mere resampling)")
        if not kwr_not_degraded: reasons.append(f"coherence degraded (kwr drop={kwr_mean_drop:.3f}, d_degr={conf_stats['d_kwr_degradation']:.3f})")
        ruling = "CLOSED-NEGATIVE: " + "; ".join(reasons)

    verdict = {
        "H": "H_1146", "title": "confidence-gated emission brake cuts hallucination (causal) == H_1135",
        "supported": supported,
        "ruling": ruling,
        "falsifier": {
            "d_fab_bar": DFAB_BAR, "kwr_mean_drop_bar": KWR_MEAN_DROP_BAR, "d_kwr_drop_bar": DKWR_DROP_BAR,
            "conf_cuts_fab": bool(conf_cuts), "beats_random": bool(beats_random),
            "random_does_not_clear": bool(random_does_not_clear), "kwr_not_degraded": bool(kwr_not_degraded),
        },
        "confidence_gate": conf_stats,
        "random_gate_control": rand_stats,
        "kwr_mean_drop_conf": float(kwr_mean_drop),
        "brake_budget": {"conf_rate": conf_brake_rate, "rand_rate": rand_brake_rate,
                         "ent_threshold": ent_threshold, "percentile": PERCENTILE_P, "K_retry": K_RETRY},
        "per_condition": {
            "off":  {"mean_fab": float(np.mean([x for x in off["fab"] if x is not None])),
                     "mean_kwr": float(np.mean(off["kwr"])), "n_scored": sum(1 for x in off["fab"] if x is not None)},
            "conf": {"mean_fab": float(np.mean([x for x in conf["fab"] if x is not None])),
                     "mean_kwr": float(np.mean(conf["kwr"])), "n_scored": sum(1 for x in conf["fab"] if x is not None)},
            "rand": {"mean_fab": float(np.mean([x for x in rand["fab"] if x is not None])),
                     "mean_kwr": float(np.mean(rand["kwr"])), "n_scored": sum(1 for x in rand["fab"] if x is not None)},
        },
        "scope": "toy ByteGPT d256/4L, CPU, en 24MB slice — scale-up to anima-7B UNVERIFIED (a_scale_honest_scope)",
        "config": {"d": D, "n_layer": NLAYER, "block": BLOCK, "steps": STEPS,
                   "win": WIN, "n_win": N_WIN, "percentile_p": PERCENTILE_P, "k_retry": K_RETRY,
                   "n_prompts": len(PROMPTS), "n_seeds": N_SEEDS, "gen_temp": GEN_TEMP, "topk": TOPK, "seed": SEED},
    }
    print("\n=== VERDICT ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1146_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done] /tmp/h1146_result.json", flush=True)


if __name__ == "__main__":
    main()
