"""
H_1142 — SELF-METACOGNITION / CONFIDENCE-CALIBRATION
"Does the substrate know what it knows?" — fills the gap left by OTHER-MIND
(theory-of-other-mind) + CSP (self-prediction) + imagine (self-simulation):
none of them measure whether anima KNOWS ITS OWN uncertainty.

Candidate metacognition signal:
    C = -(mean next-byte entropy over the generated continuation)
    (high C = confident; the substrate "feels sure")

FROZEN FALSIFIER (pre-registered, deterministic, p7-respecting):
  entropy is the OBJECT measured, NOT the verdict; the verdict is its CALIBRATION
  against INDEPENDENT ground-truth labels.

  F1 DISCRIMINATION  — C separates KNOWN (in-corpus sentence prefixes) from
                       UNKNOWN (real-word salad: real dict words, corpus-ABSENT
                       sequence — same byte stats, only the SEQUENCE is unfamiliar).
                       PASS iff AUROC(uncertainty=-C ; label=UNKNOWN) >= 0.70.
  F2 CALIBRATION-TO-COHERENCE — across ALL gens, confidence C tracks the actual
                       coherence of the model's OWN OUTPUT (known-word-ratio vs dict).
                       PASS iff Spearman rho(C, known_word_ratio) >= +0.30.
  F3 ANTI-GOODHART CONTROL — the UNTRAINED backbone must FAIL F1 (AUROC <= 0.60):
                       proves metacognition is LEARNED, not an architecture/byte artifact.

  H_1142 SUPPORTED iff F1 AND F2 AND F3.
  CLOSED-NEGATIVE (a_paper_negative_ok) iff trained model fails F1 or F2
  (confidence is uncalibrated => substrate is NOT metacognitive).

toy-scope (a_scale_honest_scope): tiny ByteGPT, CPU, en slice — scale-up to the
real anima 7B is the next rung, UNVERIFIED here.
"""
import os, sys, math, json, time, random
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

SEED = 7
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
DEV = "cpu"  # GPU on summer is busy (a_dont_kill_live_compute) — isolate on CPU
CORPUS = "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt"
EN_SLICE_BYTES = 24 * 1024 * 1024   # first ~24MB = English block (corpus order en,zh,ru,ja,ko)
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 1500; BS = 16; LR = 3e-4
GEN_LEN = 80; N_PER_CLASS = 30; GEN_TEMP = 0.7; TOPK = 40


# ---------------- model ----------------
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


# ---------------- prompt construction ----------------
def load_dict(corpus_words):
    for p in ("/usr/share/dict/words", "/usr/share/dict/american-english"):
        if os.path.exists(p):
            with open(p, encoding="utf-8", errors="ignore") as f:
                d = {w.strip().lower() for w in f if w.strip().isalpha() and len(w.strip()) >= 2}
            if len(d) > 1000:
                print(f"[dict] {p} ({len(d)} words)", flush=True); return d, "system-dict"
    # fallback: corpus-frequent words (>=5 occurrences) — document the coupling
    print(f"[dict] system dict absent -> corpus-frequent fallback ({len(corpus_words)} words)", flush=True)
    return corpus_words, "corpus-freq-fallback"


def known_word_ratio(text, dct):
    words = [w for w in ''.join(c if c.isalpha() else ' ' for c in text.lower()).split() if len(w) >= 3]
    if not words: return 0.0
    return sum(1 for w in words if w in dct) / len(words)


def build_prompts(raw_text, dct_list):
    """KNOWN = real in-corpus line prefixes; UNKNOWN = real-word salad (corpus-absent seq)."""
    rng = random.Random(SEED)
    lines = [ln.strip() for ln in raw_text.split("\n") if len(ln.strip()) >= 60 and ln.strip().isascii()]
    rng.shuffle(lines)
    known = [ln[:50] for ln in lines[:N_PER_CLASS]]
    # real-word salad: same approx length, real dict words, shuffled (sequence the model never saw)
    vocab = [w for w in dct_list if 3 <= len(w) <= 9][:20000] or list(dct_list)[:20000]
    unknown = []
    for _ in range(N_PER_CLASS):
        s, words = "", []
        while len(s) < 50:
            w = rng.choice(vocab); words.append(w); s = " ".join(words)
        unknown.append(s[:50])
    return known, unknown


# ---------------- metacognition measurement ----------------
@torch.no_grad()
def generate_and_measure(m, prompt, dct):
    ids = torch.tensor([b for b in prompt.encode("utf-8", "ignore")[:BLOCK-GEN_LEN-1]],
                       dtype=torch.long, device=DEV)[None]
    g = torch.Generator(device=DEV).manual_seed(SEED + len(prompt))
    ents, out = [], []
    for _ in range(GEN_LEN):
        ctx = ids[:, -BLOCK:]
        logits, _ = m(ctx)
        logp = F.log_softmax(logits[:, -1, :], dim=-1)
        p = logp.exp()
        ent = float(-(p * logp).sum().item())   # nats — the candidate metacog signal
        ents.append(ent)
        probs = (logits[:, -1, :] / GEN_TEMP)
        v, i = torch.topk(probs, TOPK)
        pr = F.softmax(v, dim=-1)
        nxt = i.gather(-1, torch.multinomial(pr, 1, generator=g))
        ids = torch.cat([ids, nxt], dim=1); out.append(int(nxt.item()))
    text = bytes(out).decode("utf-8", "ignore")
    mean_ent = float(np.mean(ents))
    return {"confidence": -mean_ent, "mean_entropy": mean_ent,
            "kwr": known_word_ratio(text, dct), "text": text}


def auroc(scores, labels):
    """AUROC via Mann-Whitney rank statistic. labels: 1=positive(UNKNOWN)."""
    s = np.asarray(scores, float); y = np.asarray(labels, int)
    order = np.argsort(s); ranks = np.empty_like(order, float); ranks[order] = np.arange(1, len(s)+1)
    # average ranks for ties
    _, inv, cnt = np.unique(s, return_inverse=True, return_counts=True)
    rsum = np.zeros(len(cnt)); np.add.at(rsum, inv, ranks); avg = rsum / cnt; ranks = avg[inv]
    n1 = y.sum(); n0 = len(y) - n1
    if n1 == 0 or n0 == 0: return float("nan")
    return (ranks[y == 1].sum() - n1*(n1+1)/2) / (n1*n0)


def spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean()
    den = math.sqrt((ra*ra).sum() * (rb*rb).sum())
    return float((ra*rb).sum()/den) if den else 0.0


def evaluate(m, known, unknown, dct, tag):
    rows = []
    for p in known:   rows.append({**generate_and_measure(m, p, dct), "label": 0})
    for p in unknown: rows.append({**generate_and_measure(m, p, dct), "label": 1})
    uncertainty = [-r["confidence"] for r in rows]          # -C = entropy
    labels = [r["label"] for r in rows]
    conf = [r["confidence"] for r in rows]
    kwr = [r["kwr"] for r in rows]
    au = auroc(uncertainty, labels)                          # F1: high entropy on UNKNOWN
    rho = spearman(conf, kwr)                                # F2: confident <=> coherent
    print(f"  [{tag}] AUROC(unknown|entropy)={au:.4f}  Spearman(conf,kwr)={rho:.4f}", flush=True)
    return {"auroc": au, "spearman_conf_kwr": rho,
            "mean_kwr_known": float(np.mean([r["kwr"] for r in rows if r["label"]==0])),
            "mean_ent_known": float(np.mean([r["mean_entropy"] for r in rows if r["label"]==0])),
            "mean_ent_unknown": float(np.mean([r["mean_entropy"] for r in rows if r["label"]==1])),
            "sample_known": rows[0]["text"][:70], "sample_unknown": rows[N_PER_CLASS]["text"][:70]}


def main():
    print("=== H_1142 self-metacognition / confidence-calibration ===", flush=True)
    with open(CORPUS, "rb") as f:
        raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8)
    text = raw.decode("utf-8", "ignore")
    # corpus-freq wordset (for dict fallback + always-available salad vocab)
    from collections import Counter
    cw = Counter(w for w in ''.join(c if c.isalpha() else ' ' for c in text.lower()).split() if len(w) >= 3)
    corpus_words = {w for w, c in cw.items() if c >= 5}
    dct, dct_src = load_dict(corpus_words)
    salad_vocab = sorted(corpus_words) if corpus_words else sorted(dct)
    known, unknown = build_prompts(text, salad_vocab)
    print(f"[prompts] {len(known)} KNOWN (corpus prefixes), {len(unknown)} UNKNOWN (word-salad)", flush=True)

    print("\n--- F3 control: UNTRAINED backbone ---", flush=True)
    torch.manual_seed(SEED)
    m_untrained = ByteGPT().to(DEV); m_untrained.eval()
    ctrl = evaluate(m_untrained, known, unknown, dct, "untrained")

    print("\n--- training tiny ByteGPT (en slice) ---", flush=True)
    m = train_model(data)

    print("\n--- F1/F2: TRAINED model ---", flush=True)
    trained = evaluate(m, known, unknown, dct, "trained")

    f1 = trained["auroc"] >= 0.70
    f2 = trained["spearman_conf_kwr"] >= 0.30
    f3 = ctrl["auroc"] <= 0.60
    supported = bool(f1 and f2 and f3)
    verdict = {
        "H": "H_1142", "title": "self-metacognition / confidence-calibration",
        "dict_source": dct_src,
        "F1_discrimination": {"auroc": trained["auroc"], "bar": 0.70, "pass": bool(f1)},
        "F2_calibration": {"spearman_conf_kwr": trained["spearman_conf_kwr"], "bar": 0.30, "pass": bool(f2)},
        "F3_anti_goodhart_control": {"untrained_auroc": ctrl["auroc"], "bar_max": 0.60, "pass": bool(f3)},
        "trained": trained, "untrained": ctrl,
        "supported": supported,
        "ruling": ("METACOGNITIVE (confidence calibrated)" if supported
                   else "CLOSED-NEGATIVE: confidence NOT calibrated (substrate not metacognitive)"),
        "scope": "toy ByteGPT d256/4L, CPU, en slice — scale-up to anima-7B UNVERIFIED (a_scale_honest_scope)",
        "config": {"d": D, "n_layer": NLAYER, "block": BLOCK, "steps": STEPS,
                   "n_per_class": N_PER_CLASS, "gen_len": GEN_LEN, "seed": SEED},
    }
    print("\n=== VERDICT ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1142_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done] /tmp/h1142_result.json", flush=True)


if __name__ == "__main__":
    main()
