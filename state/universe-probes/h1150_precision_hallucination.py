"""
H_1150 — PREDICTIVE-CODING PRECISION & ABERRANT-PRECISION HALLUCINATION

NEUROSCIENCE GROUNDING (predictive coding / active inference, Friston free-energy):
  perception balances PRIOR precision against SENSORY/LIKELIHOOD precision.
  Hallucination = ABERRANT PRECISION — the prior is over-weighted relative to the
  evidence (Powers, Corlett et al, Science 2017: conditioned hallucinations — people
  with stronger priors hallucinate a tone that isn't there). This directly grounds
  the metacog campaign's anti-metacognition finding (H_1148: the high-confidence
  tercile fabricated 2.4x MORE — over-sharp = over-confident prior = MORE hallucination).

In a byte-LM, sampling TEMPERATURE is an inverse prior-precision knob:
  low temp = sharp distribution = HIGH prior precision.

FROZEN FALSIFIER (pre-registered in .discoveries/1150_precision_hallucination.tape,
deterministic, p7-respecting — thresholds set BEFORE measurement, never moved):

  F1  PRECISION->FABRICATION MONOTONICITY
      Across T in {1.2, 1.0, 0.85, 0.7, 0.5}, prior_precision = 1/T (rising as T falls).
      Fabrication = corpus-absent content-ngram fraction (H_1140 metric, H_1141 grep).
      PASS iff Spearman(prior_precision, fabrication) >= +0.50
      (fabrication rises MONOTONICALLY as the prior sharpens = aberrant precision).

  F2  PRECISION-BALANCE BRAKE (the constructive test the entropy-brake H_1146 failed)
      When the next-byte PRIOR is anomalously sharp (per-step prior entropy below a
      run-percentile = over-precise prior), re-weight the sampling distribution toward
      the LIKELIHOOD/EVIDENCE term:
          p  <-  (1 - alpha) * p_prior  +  alpha * p_evidence
      p_evidence = corpus next-byte BIGRAM distribution P(byte | prev_byte) — the
      "sensory evidence" of what actually followed in the training corpus (the
      likelihood term of free-energy). This re-balances over-precise priors toward
      evidence, the active-inference correction for aberrant precision.
      PASS iff fabrication(balance-ON) < fabrication(unbalanced baseline, same T)
      with paired Cohen's d >= 0.80 AND coherence NOT degraded
      (mean kwr drop <= 0.05 AND no degradation d >= 0.80).

  CONTROL  PRECISION-RANDOM
      Same per-step mix magnitude alpha, fired on the SAME over-sharp steps, but mixed
      toward a FIXED RANDOM direction instead of the corpus-bigram evidence
      (a precision perturbation of matched magnitude, wrong direction). Must NOT cut
      fabrication like the principled balance:
          random d_fab < balance d_fab  AND  random fails d >= 0.80.

  H_1150 SUPPORTED iff F1 AND F2 AND control.
  CLOSED-NEGATIVE (a_paper_negative_ok) otherwise.
  PARTIAL-PUBLISHABLE: if ONLY F1 holds, that alone links prior-precision -> hallucination.

toy-scope (a_scale_honest_scope): tiny ByteGPT d256/4L, CPU, en slice — scale-up to
the real anima 7B is the next rung, UNVERIFIED here.
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
TOPK = 40

# F1 temperature ladder (prior_precision = 1/T, rising as T falls)
TEMPS = [1.2, 1.0, 0.85, 0.7, 0.5]

# F2 brake config
WIN = 24            # generation window length (bytes per unit) — H_1146 alignment
N_WIN = 5           # windows per generation -> 120 bytes content
SEEDS = (7, 8, 9)   # generation seeds per prompt
SHARP_PCTL = 30     # per-step prior entropy BELOW this run-percentile = over-sharp prior
ALPHA = 0.5         # precision-balance mix weight toward evidence (likelihood term)
F2_TEMP = 0.7       # F2 runs at a sharp (high prior-precision) temperature where aberrant precision bites


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

def fabrication_rate(text, dict_words, corpus_paths):
    grams = content_ngrams(text, dict_words)
    if not grams:
        return None, 0, 0
    absent = sum(1 for g in grams if corpus_absent(g, corpus_paths))
    return absent / len(grams), absent, len(grams)


# ---------------- corpus bigram next-byte EVIDENCE distribution (the likelihood term) ----------------
def build_evidence_bigram(raw_bytes):
    """P(next_byte | prev_byte) over the training slice = the sensory/likelihood term.
    Returns a (256,256) float tensor of next-byte probabilities, Laplace-smoothed."""
    arr = np.frombuffer(raw_bytes, dtype=np.uint8)
    counts = np.ones((256, 256), dtype=np.float64)  # Laplace add-1 (never zero -> valid mixing target)
    prev = arr[:-1].astype(np.int64); nxt = arr[1:].astype(np.int64)
    np.add.at(counts, (prev, nxt), 1.0)
    probs = counts / counts.sum(axis=1, keepdims=True)
    return torch.tensor(probs, dtype=torch.float32, device=DEV)


# ---------------- windowed generation with precision-balance brake ----------------
@torch.no_grad()
def _gen_window(m, ids, win_len, gen_seed, temp, mode, evidence, rand_dir, sharp_thr):
    """Generate win_len bytes from ids[0]; return (new_ids, out_bytes, mean_prior_entropy, n_balanced).
    mode:
      'off'     plain temperature sampling (the unbalanced baseline).
      'balance' if per-step PRIOR entropy < sharp_thr (over-sharp prior), mix sampling
                distribution toward corpus-bigram EVIDENCE: p=(1-a)p_prior + a*p_evidence.
      'random'  same gating + magnitude, mix toward a FIXED RANDOM direction (control).
    Entropy/sampling machinery is H_1142/H_1146 next-byte entropy (nats) VERBATIM."""
    g = torch.Generator(device=DEV).manual_seed(gen_seed)
    out = []; ents = []; n_bal = 0
    cur = ids
    for _ in range(win_len):
        ctx = cur[:, -BLOCK:]
        logits, _ = m(ctx)
        logp = F.log_softmax(logits[:, -1, :], dim=-1)
        pmodel = logp.exp()
        ent = float(-(pmodel * logp).sum().item())   # PRIOR entropy (nats) — H_1142 signal
        ents.append(ent)
        # temperature-shaped PRIOR sampling distribution
        p_prior = F.softmax(logits[:, -1, :] / temp, dim=-1)[0]   # (256,)
        prev_byte = int(cur[0, -1].item())
        p = p_prior
        if mode in ("balance", "random") and ent < sharp_thr:
            n_bal += 1
            if mode == "balance":
                p_evid = evidence[prev_byte]                       # likelihood term
            else:
                p_evid = rand_dir                                  # matched-magnitude wrong direction
            p = (1.0 - ALPHA) * p_prior + ALPHA * p_evid
            p = p / p.sum()
        # top-k restriction on the (possibly re-balanced) distribution, then sample
        v, i = torch.topk(p, TOPK)
        v = v / v.sum()
        nxt = i[torch.multinomial(v, 1, generator=g)]
        cur = torch.cat([cur, nxt.view(1, 1)], dim=1); out.append(int(nxt.item()))
    return cur, out, float(np.mean(ents)), n_bal


@torch.no_grad()
def generate(m, prompt, base_seed, temp, mode, evidence, rand_dir, sharp_thr):
    ids = torch.tensor([b for b in prompt.encode("utf-8", "ignore")[:BLOCK - WIN*N_WIN - 1]],
                       dtype=torch.long, device=DEV)[None]
    all_out = []; ents = []; n_bal = 0
    for wi in range(N_WIN):
        seed = base_seed * 100003 + wi * 7919
        ids, out, ent, nb = _gen_window(m, ids, WIN, seed, temp, mode, evidence, rand_dir, sharp_thr)
        all_out += out; ents.append(ent); n_bal += nb
    text = bytes(all_out).decode("utf-8", "ignore")
    return {"text": text, "mean_entropy": float(np.mean(ents)), "n_balanced": n_bal}


def cohens_d_paired(a, b):
    """Paired Cohen's d for (a - b): positive => a > b. d = mean(diff)/sd(diff)."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    diff = a - b
    sd = diff.std(ddof=1)
    if sd == 0:
        return 0.0 if diff.mean() == 0 else float(np.sign(diff.mean()) * 99.0)
    return float(diff.mean() / sd)


def spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean()
    den = math.sqrt((ra*ra).sum() * (rb*rb).sum())
    return float((ra*rb).sum()/den) if den else 0.0


# ---------------- prompts (H_1146 distant-concept fusions VERBATIM) ----------------
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


# ---------------- F1: temperature ladder = prior-precision ladder ----------------
def run_f1(m, dict_words, corpus_paths):
    print("\n=== F1: prior-precision (1/T) -> fabrication monotonicity ===", flush=True)
    per_temp = {}
    prec_vals, fab_vals = [], []   # per-(temp,prompt,seed) point for Spearman
    for T in TEMPS:
        fabs = []
        for pi, prompt in enumerate(PROMPTS):
            for sd in SEEDS:
                r = generate(m, prompt, sd, T, "off", None, None, -1.0)
                fab, nab, ntot = fabrication_rate(r["text"], dict_words, corpus_paths)
                if fab is None:
                    continue
                fabs.append(fab)
                prec_vals.append(1.0 / T); fab_vals.append(fab)
        mean_fab = float(np.mean(fabs)) if fabs else float("nan")
        per_temp[T] = {"mean_fab": mean_fab, "n_scored": len(fabs)}
        print(f"  [F1 T={T} prec={1.0/T:.3f}] mean_fab={mean_fab:.4f} (n={len(fabs)})", flush=True)
    rho = spearman(prec_vals, fab_vals)
    # also rank by temp-mean (robust monotonic check)
    temp_means = [per_temp[T]["mean_fab"] for T in TEMPS]
    rho_means = spearman([1.0/T for T in TEMPS], temp_means)
    print(f"  [F1] Spearman(prior_precision, fabrication) point-wise={rho:.4f}  temp-mean={rho_means:.4f}", flush=True)
    return {"per_temp": per_temp, "spearman_pointwise": rho, "spearman_tempmean": rho_means,
            "n_points": len(fab_vals)}


# ---------------- F2 + control: precision-balance brake ----------------
def calibrate_sharp_threshold(m, temp):
    """Run off-generation at F2 temp, pool per-step PRIOR entropies, set the over-sharp percentile."""
    pool = []
    for prompt in PROMPTS:
        for sd in SEEDS:
            ids = torch.tensor([b for b in prompt.encode("utf-8", "ignore")[:BLOCK - WIN*N_WIN - 1]],
                               dtype=torch.long, device=DEV)[None]
            for wi in range(N_WIN):
                seed = sd * 100003 + wi * 7919
                # capture per-step entropies via a no-brake window with a side hook
                cur = ids
                g = torch.Generator(device=DEV).manual_seed(seed)
                for _ in range(WIN):
                    ctx = cur[:, -BLOCK:]
                    logits, _ = m(ctx)
                    logp = F.log_softmax(logits[:, -1, :], dim=-1)
                    p = logp.exp()
                    pool.append(float(-(p * logp).sum().item()))
                    pr = F.softmax(logits[:, -1, :] / temp, dim=-1)[0]
                    v, i = torch.topk(pr, TOPK); v = v / v.sum()
                    nxt = i[torch.multinomial(v, 1, generator=g)]
                    cur = torch.cat([cur, nxt.view(1, 1)], dim=1)
                ids = cur
    thr = float(np.percentile(pool, SHARP_PCTL))
    print(f"[calib] per-step prior-entropy percentile-{SHARP_PCTL} = {thr:.4f} "
          f"(pool n={len(pool)} min={min(pool):.3f} max={max(pool):.3f})", flush=True)
    return thr


def run_condition_f2(m, temp, mode, evidence, rand_dir, sharp_thr, dict_words, corpus_paths, tag):
    keys, fabs, kwrs, nbal = [], [], [], []
    for pi, prompt in enumerate(PROMPTS):
        for sd in SEEDS:
            r = generate(m, prompt, sd, temp, mode, evidence, rand_dir, sharp_thr)
            fab, nab, ntot = fabrication_rate(r["text"], dict_words, corpus_paths)
            kwr = kwr_realdict(r["text"], dict_words)
            keys.append((pi, sd)); fabs.append(fab); kwrs.append(kwr); nbal.append(r["n_balanced"])
            ftxt = "skip" if fab is None else f"{fab:.3f}"
            print(f"  [{tag} p{pi} s{sd}] fab={ftxt} ({nab}/{ntot}) kwr={kwr:.2f} "
                  f"bal={r['n_balanced']} ent={r['mean_entropy']:.3f} :: {r['text'][:55]!r}", flush=True)
    return {"keys": keys, "fab": fabs, "kwr": kwrs, "n_balanced": nbal}


def paired_stats(off, on):
    okey = {k: i for i, k in enumerate(off["keys"])}
    fa, fb, ka, kb = [], [], [], []
    for j, k in enumerate(on["keys"]):
        i = okey[k]
        if off["fab"][i] is None or on["fab"][j] is None:
            continue
        fa.append(off["fab"][i]); fb.append(on["fab"][j])
        ka.append(off["kwr"][i]); kb.append(on["kwr"][j])
    n = len(fa)
    return {
        "n_pairs": n,
        "mean_fab_off": float(np.mean(fa)) if n else None,
        "mean_fab_on": float(np.mean(fb)) if n else None,
        "mean_kwr_off": float(np.mean(ka)) if n else None,
        "mean_kwr_on": float(np.mean(kb)) if n else None,
        "d_fab_reduction": cohens_d_paired(fa, fb),      # off-on ; positive => on REDUCES fab
        "d_kwr_degradation": cohens_d_paired(ka, kb),    # off-on ; positive => on DEGRADES kwr
    }


def main():
    print("=== H_1150 predictive-coding precision & aberrant-precision hallucination ===", flush=True)
    corpus_paths = [CORPUS]
    with open(CORPUS, "rb") as f:
        raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8)
    dict_words = load_real_dict()
    print(f"[dict] /usr/share/dict/words ({len(dict_words)} words)", flush=True)

    print("\n--- building corpus bigram EVIDENCE distribution (likelihood term) ---", flush=True)
    evidence = build_evidence_bigram(raw)
    print(f"[evidence] bigram next-byte P (256x256) built; row-sum check={float(evidence.sum(1).mean()):.4f}", flush=True)

    print("\n--- training tiny ByteGPT (en slice) ---", flush=True)
    m = train_model(data)

    # ---- F1 ----
    f1res = run_f1(m, dict_words, corpus_paths)

    # ---- F2 calibration ----
    print(f"\n=== F2: precision-balance brake @ T={F2_TEMP} (alpha={ALPHA}, sharp-pctl={SHARP_PCTL}) ===", flush=True)
    sharp_thr = calibrate_sharp_threshold(m, F2_TEMP)

    # fixed random direction (control): a valid prob vector, matched mixing magnitude, wrong direction
    rg = np.random.RandomState(SEED + 1234)
    rand_dir = rg.dirichlet(np.ones(256))   # deterministic random simplex point
    rand_dir = torch.tensor(rand_dir, dtype=torch.float32, device=DEV)

    print("\n--- condition: UNBALANCED baseline (off) ---", flush=True)
    off = run_condition_f2(m, F2_TEMP, "off", None, None, sharp_thr, dict_words, corpus_paths, "off")

    print("\n--- condition: PRECISION-BALANCE (mix toward corpus-bigram evidence) ---", flush=True)
    bal = run_condition_f2(m, F2_TEMP, "balance", evidence, None, sharp_thr, dict_words, corpus_paths, "bal")

    print("\n--- condition: PRECISION-RANDOM control (mix toward random direction, matched alpha) ---", flush=True)
    rnd = run_condition_f2(m, F2_TEMP, "random", evidence, rand_dir, sharp_thr, dict_words, corpus_paths, "rnd")

    bal_stats = paired_stats(off, bal)
    rnd_stats = paired_stats(off, rnd)
    bal_balrate = sum(bal["n_balanced"]) / (len(bal["n_balanced"]) * WIN * N_WIN)
    rnd_balrate = sum(rnd["n_balanced"]) / (len(rnd["n_balanced"]) * WIN * N_WIN)
    print(f"\n[budget] balance fired on {sum(bal['n_balanced'])} steps (rate {bal_balrate:.3f}); "
          f"random fired on {sum(rnd['n_balanced'])} steps (rate {rnd_balrate:.3f})", flush=True)

    # ----- FROZEN falsifier (pre-registered, no threshold moved) -----
    F1_BAR = 0.50
    DFAB_BAR = 0.80
    KWR_DROP_BAR = 0.05
    DKWR_DEGR_BAR = 0.80

    f1_pass = (f1res["spearman_pointwise"] >= F1_BAR) and (f1res["spearman_tempmean"] >= F1_BAR)

    bal_cuts = bal_stats["d_fab_reduction"] >= DFAB_BAR
    kwr_drop = (bal_stats["mean_kwr_off"] - bal_stats["mean_kwr_on"]) if bal_stats["mean_kwr_off"] is not None else 0.0
    kwr_not_degraded = (bal_stats["d_kwr_degradation"] < DKWR_DEGR_BAR) and (kwr_drop <= KWR_DROP_BAR)
    f2_pass = bool(bal_cuts and kwr_not_degraded)

    control_pass = (rnd_stats["d_fab_reduction"] < bal_stats["d_fab_reduction"]) and \
                   (rnd_stats["d_fab_reduction"] < DFAB_BAR)

    supported = bool(f1_pass and f2_pass and control_pass)
    f1_only = bool(f1_pass and not (f2_pass and control_pass))

    if supported:
        ruling = ("SUPPORTED: prior-precision (1/T) DRIVES fabrication "
                  f"(Spearman={f1res['spearman_pointwise']:.3f}>={F1_BAR}), and a free-energy "
                  f"precision-balance brake CUTS it (d={bal_stats['d_fab_reduction']:.3f}>={DFAB_BAR}) "
                  f"where the random-direction control cannot (d={rnd_stats['d_fab_reduction']:.3f}), coherence held")
    elif f1_only:
        ruling = ("PARTIAL/PUBLISHABLE (F1 only): prior-precision DRIVES fabrication "
                  f"(Spearman={f1res['spearman_pointwise']:.3f}>={F1_BAR}) = aberrant-precision mechanism CONFIRMED, "
                  f"but the precision-balance brake did NOT cut it (d={bal_stats['d_fab_reduction']:.3f}<{DFAB_BAR}) "
                  "— hallucination is driven by precision yet not corrected by evidence-mixing at toy scale")
    else:
        reasons = []
        if not f1_pass: reasons.append(f"F1 Spearman pointwise={f1res['spearman_pointwise']:.3f}/tempmean={f1res['spearman_tempmean']:.3f}<{F1_BAR}")
        if not bal_cuts: reasons.append(f"F2 balance d_fab={bal_stats['d_fab_reduction']:.3f}<{DFAB_BAR}")
        if f2_pass and not kwr_not_degraded: reasons.append(f"coherence degraded (kwr drop={kwr_drop:.3f}, d_degr={bal_stats['d_kwr_degradation']:.3f})")
        if not control_pass: reasons.append(f"control fails (random d_fab={rnd_stats['d_fab_reduction']:.3f} >= balance or >= {DFAB_BAR})")
        ruling = "CLOSED-NEGATIVE: " + "; ".join(reasons)

    verdict = {
        "H": "H_1150", "title": "predictive-coding precision & aberrant-precision hallucination",
        "supported": supported, "f1_only_partial": f1_only,
        "ruling": ruling,
        "falsifier": {"F1_spearman_bar": F1_BAR, "F2_d_fab_bar": DFAB_BAR,
                      "kwr_drop_bar": KWR_DROP_BAR, "d_kwr_degr_bar": DKWR_DEGR_BAR},
        "F1_precision_to_fabrication": {
            "spearman_pointwise": f1res["spearman_pointwise"],
            "spearman_tempmean": f1res["spearman_tempmean"],
            "pass": bool(f1_pass), "n_points": f1res["n_points"],
            "per_temp": {str(T): f1res["per_temp"][T] for T in TEMPS},
        },
        "F2_precision_balance": {
            "balance_stats": bal_stats, "pass": bool(f2_pass),
            "bal_cuts": bool(bal_cuts), "kwr_not_degraded": bool(kwr_not_degraded),
            "kwr_drop": float(kwr_drop), "balance_fire_rate": float(bal_balrate),
        },
        "control_precision_random": {
            "random_stats": rnd_stats, "pass": bool(control_pass),
            "random_fire_rate": float(rnd_balrate),
        },
        "config": {"d": D, "n_layer": NLAYER, "block": BLOCK, "steps": STEPS,
                   "temps": TEMPS, "f2_temp": F2_TEMP, "alpha": ALPHA, "sharp_pctl": SHARP_PCTL,
                   "win": WIN, "n_win": N_WIN, "n_prompts": len(PROMPTS), "seeds": list(SEEDS),
                   "topk": TOPK, "seed": SEED},
        "scope": "toy ByteGPT d256/4L CPU en-24MB slice — scale-up to anima-7B UNVERIFIED (a_scale_honest_scope)",
        "neuro": "Friston free-energy / predictive coding; aberrant precision (Powers/Corlett, Science 2017). T=inverse prior-precision; balance brake re-weights over-sharp prior toward corpus-bigram likelihood/evidence.",
    }
    print("\n=== VERDICT ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1150_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done] /tmp/h1150_result.json", flush=True)


if __name__ == "__main__":
    main()
