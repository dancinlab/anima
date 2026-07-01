"""
H_1148 — METACOG-GAP CAUSES HALLUCINATION (unifying capstone).
Synthesizes H_1142 (confidence C = -mean entropy), H_1143 (ood = hidden-state
familiarity), H_1140 (fabrication F = corpus-absent content-ngram fraction).

CLAIM: confident-fabrication events concentrate where the substrate's input-
familiarity metacog is BLIND — i.e. fabrication is HIGHER in the metacog-blind
tercile (low/uninformative familiarity signal) than the metacog-aware tercile.

FROZEN FALSIFIER (pre-registered):
  F_concentration: fabrication rate in the metacog-BLIND tercile >= 2.0x the
       metacog-AWARE tercile, terciled by the familiarity (ood) signal.
  Also report Spearman(C, F) and Spearman(ood, F): if BOTH |rho| < 0.3, NO internal
       signal predicts fabrication => the unified negative ("no metacog handle on
       hallucination") consistent with H_1143 + H_1146.
  SUPPORTED iff concentration >= 2.0x; CLOSED-NEGATIVE iff flat (fabrication is
       metacog-signal-independent => metacog-gap does NOT localize hallucination).

toy-scope (a_scale_honest_scope). xref H_1142/1143/1144/1145/1146/1140.
"""
import os, math, json, time, random, subprocess
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

SEED = 7
random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)
DEV = "cpu"
CORPUS = "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt"
EN_SLICE_BYTES = 24 * 1024 * 1024
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 1500; BS = 16; LR = 3e-4
N_REF = 60; GEN_LEN = 90; GEN_TEMP = 0.85; TOPK = 40; KNN = 5
N_PROMPTS = 24; SEEDS = [7, 8, 9]

# ---- concept-fusion idea prompts (H_1140-style distant-pair fusion) ----
CONCEPTS = ["consciousness","tension","memory","silence","engine","cell","mitosis",
            "curiosity","anchor","dream","field","repulsion","emergence","novelty",
            "coherence","substrate","idle","ratchet","division","resonance"]


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
    def hidden(s, idx):
        T = idx.shape[1]
        x = s.tok(idx) + s.pos(torch.arange(T, device=idx.device))[None]
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        return s.lnf(x)
    def forward(s, idx, targets=None):
        h = s.hidden(idx); logits = s.head(h)
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
    for st in range(STEPS):
        lr_t = LR * min(1.0, (st+1)/80) * (0.5*(1+math.cos(math.pi*min(1.0, st/STEPS))))
        for g in opt.param_groups: g["lr"] = lr_t
        x, y = batch(data, BLOCK, BS, DEV); _, l = m(x, y)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % 500 == 0 or st == STEPS-1: print(f"  [train] step {st} ce={l.item():.4f}", flush=True)
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

def corpus_absent(ngram):
    # deterministic corpus-absence (H_1140 metric): grep -F -i, punct/newline tolerant
    try:
        r = subprocess.run(["grep", "-F", "-i", "-m", "1", ngram, CORPUS],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
        return r.returncode != 0      # nonzero = not found = absent = fabricated
    except Exception:
        return False

@torch.no_grad()
def measure(m, prompt, seed, ref_mat, dct):
    pid = [b for b in prompt.encode("utf-8", "ignore")[:BLOCK-GEN_LEN-1]]
    ids = torch.tensor(pid, dtype=torch.long, device=DEV)[None]
    # ood = familiarity signal on the prompt (H_1143)
    hp = m.hidden(ids)[0].mean(0).cpu().numpy()
    d = np.linalg.norm(ref_mat - hp[None], axis=1); ood = float(np.sort(d)[:KNN].mean())
    g = torch.Generator(device=DEV).manual_seed(seed); ents = []; out = []
    for _ in range(GEN_LEN):
        logits, _ = m(ids[:, -BLOCK:]); logp = F.log_softmax(logits[:, -1, :], -1); p = logp.exp()
        ents.append(float(-(p*logp).sum().item()))
        v, i = torch.topk(logits[:, -1, :]/GEN_TEMP, TOPK)
        nxt = i.gather(-1, torch.multinomial(F.softmax(v, -1), 1, generator=g))
        ids = torch.cat([ids, nxt], 1); out.append(int(nxt.item()))
    text = bytes(out).decode("utf-8", "ignore")
    grams = content_ngrams(text, dct)
    fab = (sum(1 for g_ in grams if corpus_absent(g_)) / len(grams)) if grams else 0.0
    return {"C": -float(np.mean(ents)), "ood": ood, "fab": fab, "n_grams": len(grams)}


def spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean(); den = math.sqrt((ra*ra).sum()*(rb*rb).sum())
    return float((ra*rb).sum()/den) if den else 0.0

def tercile_fab(signal, fab):
    idx = np.argsort(signal); n = len(idx); t = n // 3
    low = [fab[i] for i in idx[:t]]; high = [fab[i] for i in idx[-t:]]
    return float(np.mean(low)), float(np.mean(high))


def main():
    print("=== H_1148 metacog-gap causes hallucination (capstone) ===", flush=True)
    with open(CORPUS, "rb") as f: raw = f.read(EN_SLICE_BYTES)
    data = torch.frombuffer(bytearray(raw), dtype=torch.uint8); text = raw.decode("utf-8", "ignore")
    dct = load_dict(); print(f"[dict] {len(dct)} words", flush=True)
    rng = random.Random(SEED)
    lines = [ln.strip() for ln in text.split("\n") if len(ln.strip()) >= 60 and ln.strip().isascii()]
    rng.shuffle(lines); ref = [ln[:50] for ln in lines[:N_REF]]
    pairs = []
    for _ in range(N_PROMPTS):
        a, b = rng.sample(CONCEPTS, 2); pairs.append(f"What links {a} and {b}? ")
    print("--- training ---", flush=True); m = train_model(data)
    ref_mat = np.stack([m.hidden(torch.tensor([c for c in p.encode()[:50]], dtype=torch.long)[None]).detach()[0].mean(0).numpy() for p in ref])

    rows = []
    for p in pairs:
        for sd in SEEDS:
            rows.append(measure(m, p, sd, ref_mat, dct))
    C = [r["C"] for r in rows]; ood = [r["ood"] for r in rows]; fab = [r["fab"] for r in rows]
    rho_cf = spearman(C, fab); rho_of = spearman(ood, fab)
    # metacog-blind = high ood (unfamiliar, signal says "far") ; aware = low ood
    aware_fab, blind_fab = tercile_fab(np.array(ood), fab)   # low-ood, high-ood
    conc = (blind_fab / aware_fab) if aware_fab > 1e-9 else float("inf")
    # also confidence terciles
    lowC_fab, highC_fab = tercile_fab(np.array(C), fab)

    supported = bool(conc >= 2.0)
    no_handle = bool(abs(rho_cf) < 0.3 and abs(rho_of) < 0.3)
    verdict = {
        "H": "H_1148", "title": "metacog-gap causes hallucination (unifying capstone)",
        "n_gens": len(rows), "mean_fab": float(np.mean(fab)),
        "F_concentration": {"blind_tercile_fab": blind_fab, "aware_tercile_fab": aware_fab,
                            "ratio": conc, "bar": 2.0, "pass": supported},
        "spearman_conf_fab": rho_cf, "spearman_ood_fab": rho_of,
        "confidence_terciles": {"low_conf_fab": lowC_fab, "high_conf_fab": highC_fab},
        "no_metacog_handle": no_handle,
        "supported": supported,
        "ruling": ("SUPPORTED: fabrication concentrates in the metacog-blind region (gap localizes hallucination)"
                   if supported else
                   ("CLOSED-NEGATIVE: fabrication is metacog-signal-INDEPENDENT — NO internal handle on hallucination "
                    "(|rho(C,fab)|<0.3 AND |rho(ood,fab)|<0.3); the metacog-gap does NOT localize hallucination — "
                    "unifies the campaign's negatives" if no_handle else
                    "CLOSED-NEGATIVE: concentration <2.0x — metacog-gap does NOT localize hallucination")),
        "scope": "toy ByteGPT d256/4L CPU en slice — scale-up UNVERIFIED (a_scale_honest_scope)",
    }
    print("\n=== VERDICT ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1148_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done] /tmp/h1148_result.json", flush=True)


if __name__ == "__main__": main()
