"""
H_1152 — NEUROMODULATORY UNCERTAINTY SPLIT (ACh expected ⊥ NE unexpected).

Yu & Dayan (2005): acetylcholine (ACh) signals EXPECTED uncertainty (known noise
within the current model); norepinephrine (NE) signals UNEXPECTED uncertainty
(model breakdown / surprise the current model is WRONG). They are DISTINCT
channels. The metacog campaign (H_1142..H_1148) used a SINGLE conflated
uncertainty scalar (next-byte entropy) that FAILED to predict fabrication —
H_1148: confidence/entropy was ANTI-predictive (Spearman(C,fab)=+0.257, wrong
direction; high-conf fab 0.400 vs low-conf 0.164).

HYPOTHESIS: separating uncertainty into
  ACh_channel = EXPECTED uncertainty = mean within-distribution next-byte entropy
                (= the OLD conflated scalar; the model's own sense of "known noise")
  NE_channel  = UNEXPECTED uncertainty = model-mismatch SURPRISE, two deterministic
                variants (both computed; stronger-F1 = primary):
     NE_kl   = mean KL( model next-byte posterior || corpus unigram prior )
               — the posterior departs from the corpus base rate = the model is
                 ASSERTING structure the base distribution does not contain.
     NE_gap  = mean( realized surprise - predicted entropy )
             = mean( -log p(sampled byte)  -  H[p] )
               — the model is MORE surprised by its OWN sampled output than its own
                 predicted entropy said it should be = a mis-calibration / model-
                 breakdown spike (positive => realized > expected = NE firing).
yields an NE channel that predicts fabrication where conflated entropy failed.

FROZEN FALSIFIER (pre-registered, deterministic, p7):
  F1  Spearman(NE_channel, fabrication) >= +0.30   (correctly-signed handle)
  F2  |Spearman(ACh_channel, NE_channel)| < 0.7    (channels genuinely distinct)
  CONTROL  |Spearman(NE_untrained, fab_untrained)| <= 0.15   (learned, not artifact)
  SUPPORTED iff F1 ∧ F2 ∧ control ; else CLOSED-NEGATIVE (a_paper_negative_ok).

fabrication = corpus-absent content-ngram fraction (H_1140 grep metric, verbatim).
toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU, en slice; anima-7B UNVERIFIED.
xref H_1148 / H_1142 / H_1140.
"""
import os, math, json, time, random, subprocess
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

SEED = 7
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
DEV = "cpu"  # summer GPU untouched (a_dont_kill_live_compute); CPU isolate
CORPUS = "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt"
EN_SLICE_BYTES = 24 * 1024 * 1024
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 1500; BS = 16; LR = 3e-4
GEN_LEN = 90; GEN_TEMP = 0.85; TOPK = 40
N_PROMPTS = 24; SEEDS = [7, 8, 9]

# concept-fusion idea prompts (H_1140/H_1148-style distant-pair fusion) — verbatim
CONCEPTS = ["consciousness","tension","memory","silence","engine","cell","mitosis",
            "curiosity","anchor","dream","field","repulsion","emergence","novelty",
            "coherence","substrate","idle","ratchet","division","resonance"]


# ---------------- model (verbatim from H_1148) ----------------
class Block(nn.Module):
    def __init__(s, d, h):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.ln2 = nn.LayerNorm(d)
        s.attn = nn.MultiheadAttention(d, h, batch_first=True)
        s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d))
    def forward(s, x, mask):
        a, _ = s.attn(s.ln1(x), s.ln1(x), s.ln1(x), attn_mask=mask, need_weights=False)
        x = x + a; return x + s.mlp(s.ln2(x))

class ByteGPT(nn.Module):
    def __init__(s, vocab=VOCAB, d=D, n_layer=NLAYER, n_head=NHEAD, block=BLOCK):
        super().__init__()
        s.block = block
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d)
        s.blocks = nn.ModuleList([Block(d, n_head) for _ in range(n_layer)])
        s.lnf = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False)
    def forward(s, idx, targets=None):
        T = idx.shape[1]
        x = s.tok(idx) + s.pos(torch.arange(T, device=idx.device))[None]
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        logits = s.head(s.lnf(x))
        loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1)) if targets is not None else None
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
        x, y = batch(data, BLOCK, BS, DEV); _, l = m(x, y)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % 500 == 0 or st == STEPS-1:
            print(f"  [train] step {st} ce={l.item():.4f} {(time.time()-t0)/60:.1f}min", flush=True)
    m.eval(); return m


def load_dict():
    for p in ("/usr/share/dict/words",):
        if os.path.exists(p):
            return {w.strip().lower() for w in open(p, encoding="utf-8", errors="ignore")
                    if w.strip().isalpha() and len(w.strip()) >= 3}
    return set()

def content_ngrams(text, dct):
    words = [w for w in ''.join(c if c.isalpha() else ' ' for c in text.lower()).split()
             if len(w) >= 3 and w in dct]
    grams = []
    for n in (2, 3):
        for i in range(len(words)-n+1):
            grams.append(" ".join(words[i:i+n]))
    return grams

_CORPUS_LC = None   # full corpus, lowercased bytes, loaded once (in-memory mirror of grep -F -i)
def _load_corpus_lc():
    global _CORPUS_LC
    if _CORPUS_LC is None:
        t0 = time.time()
        with open(CORPUS, "rb") as f:
            _CORPUS_LC = f.read().lower()    # bytes.lower() == ASCII case-fold == grep -i over ASCII corpus
        print(f"  [corpus] loaded {len(_CORPUS_LC)/1e9:.2f}GB lowercased in {(time.time()-t0):.1f}s", flush=True)
    return _CORPUS_LC

def corpus_absent(ngram):
    # deterministic corpus-absence (H_1140/h1141 metric). EXACT semantics of
    # `grep -F -i -m1 <ngram> CORPUS` (case-insensitive literal substring over the
    # whole file), but as a one-time in-memory scan instead of a 1.5GB grep per call
    # (thousands of full-corpus greps under contention -> hours; this -> seconds).
    cl = _load_corpus_lc()
    return ngram.lower().encode("utf-8", "ignore") not in cl   # True = absent = fabricated


@torch.no_grad()
def measure(m, prompt, seed, log_prior):
    """One generation; returns ACh (expected entropy), NE_kl, NE_gap, fabrication.
    log_prior: corpus unigram log-prior over 256 bytes (the NE reference prior)."""
    pid = [b for b in prompt.encode("utf-8", "ignore")[:BLOCK-GEN_LEN-1]]
    ids = torch.tensor(pid, dtype=torch.long, device=DEV)[None]
    g = torch.Generator(device=DEV).manual_seed(seed)
    ents, kls, gaps, out = [], [], [], []
    prior = torch.tensor(np.exp(log_prior), dtype=torch.float32, device=DEV)   # p_prior(256)
    lprior = torch.tensor(log_prior, dtype=torch.float32, device=DEV)
    for _ in range(GEN_LEN):
        logits, _ = m(ids[:, -BLOCK:])
        logp = F.log_softmax(logits[:, -1, :], -1)[0]   # (256,)
        p = logp.exp()
        ent = float(-(p * logp).sum().item())           # ACh: expected (within-model) entropy [nats]
        ents.append(ent)
        # NE_kl: KL(model posterior || corpus unigram prior) — model departs from base rate
        kl = float((p * (logp - lprior)).sum().item())
        kls.append(kl)
        # sample next byte
        v, i = torch.topk(logits[:, -1, :] / GEN_TEMP, TOPK)
        nxt = i.gather(-1, torch.multinomial(F.softmax(v, -1), 1, generator=g))
        b = int(nxt.item())
        # NE_gap: realized surprise of the sampled byte minus the model's own predicted entropy
        realized = float(-logp[b].item())
        gaps.append(realized - ent)
        ids = torch.cat([ids, nxt], 1); out.append(b)
    text = bytes(out).decode("utf-8", "ignore")
    grams = content_ngrams(text, dct_g)
    fab = (sum(1 for gm in grams if corpus_absent(gm)) / len(grams)) if grams else 0.0
    return {"ACh": float(np.mean(ents)),            # expected uncertainty (high = model unsure within model)
            "NE_kl": float(np.mean(kls)),           # unexpected: posterior-vs-prior divergence
            "NE_gap": float(np.mean(gaps)),         # unexpected: realized-vs-predicted surprise gap
            "conf": -float(np.mean(ents)),          # H_1148 confidence reproduction
            "fab": fab, "n_grams": len(grams)}


def spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    if np.std(a) < 1e-12 or np.std(b) < 1e-12: return 0.0
    ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean(); den = math.sqrt((ra*ra).sum()*(rb*rb).sum())
    return float((ra*rb).sum()/den) if den else 0.0


dct_g = set()  # set in main, used inside measure()

def unigram_log_prior(raw_bytes):
    """corpus unigram byte distribution (the NE reference 'prior model') -> log-prob(256)."""
    counts = np.bincount(np.frombuffer(raw_bytes, dtype=np.uint8), minlength=256).astype(np.float64)
    counts += 1.0  # Laplace smoothing so KL is finite everywhere
    p = counts / counts.sum()
    return np.log(p)


def run_battery(m, prompts, log_prior, tag):
    rows = []
    for p in prompts:
        for sd in SEEDS:
            rows.append(measure(m, p, sd, log_prior))
    ACh = [r["ACh"] for r in rows]; NEk = [r["NE_kl"] for r in rows]
    NEg = [r["NE_gap"] for r in rows]; fab = [r["fab"] for r in rows]
    conf = [r["conf"] for r in rows]
    res = {
        "n_gens": len(rows), "mean_fab": float(np.mean(fab)),
        "spearman_NEkl_fab": spearman(NEk, fab),
        "spearman_NEgap_fab": spearman(NEg, fab),
        "spearman_ACh_fab": spearman(ACh, fab),
        "spearman_conf_fab": spearman(conf, fab),          # H_1148 reproduction (~+0.257)
        "spearman_ACh_NEkl": spearman(ACh, NEk),
        "spearman_ACh_NEgap": spearman(ACh, NEg),
    }
    print(f"  [{tag}] NEkl->fab={res['spearman_NEkl_fab']:+.4f} NEgap->fab={res['spearman_NEgap_fab']:+.4f} "
          f"ACh->fab={res['spearman_ACh_fab']:+.4f} conf->fab={res['spearman_conf_fab']:+.4f} "
          f"ACh~NEkl={res['spearman_ACh_NEkl']:+.4f} ACh~NEgap={res['spearman_ACh_NEgap']:+.4f}", flush=True)
    return res, rows


def main():
    global dct_g
    print("=== H_1152 neuromodulatory uncertainty split (ACh expected ⊥ NE unexpected) ===", flush=True)
    with open(CORPUS, "rb") as f: raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8)
    log_prior = unigram_log_prior(raw)
    dct_g = load_dict(); print(f"[dict] {len(dct_g)} words", flush=True)
    rng = random.Random(SEED)
    prompts = [f"What links {a} and {b}? " for a, b in (rng.sample(CONCEPTS, 2) for _ in range(N_PROMPTS))]
    print(f"[prompts] {len(prompts)} concept-fusion x {len(SEEDS)} seeds = {len(prompts)*len(SEEDS)} gens", flush=True)

    print("\n--- CONTROL: UNTRAINED backbone ---", flush=True)
    torch.manual_seed(SEED)
    m_un = ByteGPT().to(DEV); m_un.eval()
    ctrl, _ = run_battery(m_un, prompts, log_prior, "untrained")

    print("\n--- training tiny ByteGPT (en slice) ---", flush=True)
    m = train_model(data)

    print("\n--- TRAINED battery ---", flush=True)
    tr, rows = run_battery(m, prompts, log_prior, "trained")

    # primary NE = stronger-F1 of the two pre-registered variants
    ne_variants = {"NE_kl": tr["spearman_NEkl_fab"], "NE_gap": tr["spearman_NEgap_fab"]}
    primary_ne = max(ne_variants, key=lambda k: ne_variants[k])
    f1_val = ne_variants[primary_ne]
    ach_ne = tr["spearman_ACh_NEkl"] if primary_ne == "NE_kl" else tr["spearman_ACh_NEgap"]
    ctrl_ne = ctrl["spearman_NEkl_fab"] if primary_ne == "NE_kl" else ctrl["spearman_NEgap_fab"]

    f1 = f1_val >= 0.30
    f2 = abs(ach_ne) < 0.70
    control_ok = abs(ctrl_ne) <= 0.15
    supported = bool(f1 and f2 and control_ok)

    verdict = {
        "H": "H_1152", "title": "neuromodulatory uncertainty split (ACh expected ⊥ NE unexpected)",
        "grounding": "Yu & Dayan 2005 — ACh=expected uncertainty (within-model entropy), NE=unexpected uncertainty (model-mismatch surprise)",
        "primary_NE_channel": primary_ne,
        "F1_NE_predicts_fab": {"spearman": f1_val, "bar": 0.30, "pass": bool(f1),
                               "both_variants": {"NE_kl": tr["spearman_NEkl_fab"], "NE_gap": tr["spearman_NEgap_fab"]}},
        "F2_dissociation": {"spearman_ACh_NE": ach_ne, "bar_max_abs": 0.70, "pass": bool(f2),
                            "ACh_NEkl": tr["spearman_ACh_NEkl"], "ACh_NEgap": tr["spearman_ACh_NEgap"]},
        "control_anti_goodhart": {"untrained_NE_fab_spearman": ctrl_ne, "bar_max_abs": 0.15, "pass": bool(control_ok),
                                  "untrained_NEkl": ctrl["spearman_NEkl_fab"], "untrained_NEgap": ctrl["spearman_NEgap_fab"]},
        "baseline_conflated": {"trained_conf_fab": tr["spearman_conf_fab"],
                               "trained_ACh_fab": tr["spearman_ACh_fab"],
                               "note": "H_1148 conflated-entropy signal reproduction (conf~+0.257 anti-predictive)"},
        "trained": tr, "untrained": ctrl,
        "supported": supported,
        "ruling": ("SUPPORTED: the expected/unexpected (ACh⊥NE) split yields a correctly-signed NE fabrication handle "
                   "that conflated entropy lacked (F1∧F2∧control)" if supported else
                   "CLOSED-NEGATIVE (a_paper_negative_ok): the ACh⊥NE split does NOT yield a correctly-signed fabrication "
                   "handle that conflated entropy lacked"),
        "scope": "toy ByteGPT d256/4L CPU en-24MB slice seed 7 — anima-7B UNVERIFIED (a_scale_honest_scope)",
        "config": {"d": D, "n_layer": NLAYER, "block": BLOCK, "steps": STEPS,
                   "n_prompts": N_PROMPTS, "seeds": SEEDS, "gen_len": GEN_LEN, "seed": SEED},
    }
    print("\n=== VERDICT ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1152_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done] /tmp/h1152_result.json", flush=True)


if __name__ == "__main__":
    main()
