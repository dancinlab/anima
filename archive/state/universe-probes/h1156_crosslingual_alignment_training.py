"""
H_1156 — can EXPLICIT cross-lingual alignment training BUILD the interlingua bridge
H_1155 found is absent? Constructive converse. Add a contrastive ALIGNMENT LOSS that
pulls same-concept cross-lingual hidden reps together — but ONLY on TRAIN concepts,
and measure interlingua on HELD-OUT concepts (does the bridge GENERALIZE, or only
memorize the trained pairs?).

FROZEN FALSIFIER:
  F1: with-alignment HELD-OUT interlingua d ≥ 0.8 (vs H_1155 no-aln d=−0.226) — a
      GENERAL bridge, not memorized pairs.
  F2: 5/5 held-out languages align to en above baseline.
  CONTROL: no-alignment model HELD-OUT d ≤ 0.3 (reproduce H_1155 no-interlingua).
  SUPPORTED iff F1 ∧ F2 ∧ control → path-(1) works: explicit alignment builds a
  generalizing interlingua. CLOSED-NEGATIVE iff held-out stays unaligned (alignment
  only memorizes trained pairs, no general bridge — byte script-siloing is deeper).
toy-scope. xref h1155.
"""
import os, math, json, random
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

DEV = "cpu"
CORPUS = "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt"
PER = 300*1024*1024; SLICE = 6*1024*1024
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4
STEPS = 2200; BS = 16; LR = 3e-4; SEED = 7; LAMBDA = 1.0
LANGS = ["en", "zh", "ru", "ja", "ko"]
TRAIN_C = {
    "water": ["water","水","вода","水","물"], "fire": ["fire","火","огонь","火","불"],
    "book": ["book","书","книга","本","책"], "house": ["house","房子","дом","家","집"],
    "tree": ["tree","树","дерево","木","나무"], "dog": ["dog","狗","собака","犬","개"],
    "sun": ["sun","太阳","солнце","太陽","태양"], "moon": ["moon","月亮","луна","月","달"],
}
HELD_C = {
    "star": ["star","星星","звезда","星","별"], "river": ["river","河","река","川","강"],
    "mountain": ["mountain","山","гора","山","산"], "road": ["road","路","дорога","道","길"],
}


class Block(nn.Module):
    def __init__(s, d, h):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.ln2 = nn.LayerNorm(d)
        s.attn = nn.MultiheadAttention(d, h, batch_first=True)
        s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d))
    def forward(s, x, m):
        a, _ = s.attn(s.ln1(x), s.ln1(x), s.ln1(x), attn_mask=m, need_weights=False)
        x = x + a; return x + s.mlp(s.ln2(x))

class ByteGPT(nn.Module):
    def __init__(s, vocab=256, d=D, n_layer=NLAYER, n_head=NHEAD, block=BLOCK):
        super().__init__()
        s.block = block
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d)
        s.blocks = nn.ModuleList([Block(d, n_head) for _ in range(n_layer)])
        s.lnf = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False)
    def hidden(s, idx):
        T = idx.shape[1]; x = s.tok(idx) + s.pos(torch.arange(T, device=idx.device))[None]
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        return s.lnf(x)
    def forward(s, idx, targets=None):
        h = s.hidden(idx); logits = s.head(h)
        loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1)) if targets is not None else None
        return logits, loss


def word_ids(word):
    return torch.tensor(list(word.encode("utf-8", "ignore")[:BLOCK]) or [0], dtype=torch.long, device=DEV)[None]

def concept_vecs(m, cdict, grad):
    """mean-pool hidden of each concept word, returns dict[concept]->[5 x D] tensor."""
    out = {}
    for c, ws in cdict.items():
        vs = []
        for w in ws:
            h = m.hidden(word_ids(w))[0].mean(0)
            vs.append(h)
        out[c] = torch.stack(vs)   # [5,D]
    return out

def alignment_loss(m, cdict):
    V = concept_vecs(m, cdict, grad=True)
    Vn = {c: F.normalize(V[c], dim=-1) for c in V}
    cs = list(Vn); pos, neg = [], []
    for c in cs:
        S = Vn[c] @ Vn[c].t()                     # [5,5] same-concept cross-lang cosines
        iu = torch.triu_indices(5, 5, 1)
        pos.append(S[iu[0], iu[1]])
    pos = torch.cat(pos)                           # pull these UP
    # negatives: en-rep of each concept vs en-rep of other concepts
    ens = F.normalize(torch.stack([V[c][0] for c in cs]), dim=-1)
    Sd = ens @ ens.t(); iu = torch.triu_indices(len(cs), len(cs), 1)
    neg = Sd[iu[0], iu[1]]                          # push these DOWN
    return (1 - pos).mean() + F.relu(neg - 0.1).mean()


def load_balanced():
    parts = []
    with open(CORPUS, "rb") as f:
        for i in range(5): f.seek(i*PER); parts.append(f.read(SLICE))
    return torch.frombuffer(bytearray(b"".join(parts)), dtype=torch.uint8)

def train(data, use_aln):
    torch.manual_seed(SEED); np.random.seed(SEED)
    m = ByteGPT().to(DEV); m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=LR, betas=(0.9, 0.95), weight_decay=0.1)
    g = torch.Generator(device=DEV).manual_seed(SEED)
    for st in range(STEPS):
        lr_t = LR*min(1.0, (st+1)/100)*(0.5*(1+math.cos(math.pi*min(1.0, st/STEPS))))
        for pg in opt.param_groups: pg["lr"] = lr_t
        ix = torch.randint(0, data.numel()-BLOCK-1, (BS,), generator=g)
        x = torch.stack([data[j:j+BLOCK] for j in ix]).long().to(DEV)
        y = torch.stack([data[j+1:j+BLOCK+1] for j in ix]).long().to(DEV)
        _, l = m(x, y)
        if use_aln: l = l + LAMBDA*alignment_loss(m, TRAIN_C)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % 500 == 0 or st == STEPS-1: print(f"  [aln={use_aln}] step {st} loss={l.item():.4f}", flush=True)
    m.eval(); return m


def cos(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(np.dot(a, b)/(na*nb)) if na > 0 and nb > 0 else 0.0

@torch.no_grad()
def interlingua_d(m, cdict, tag):
    V = {c: {LANGS[i]: m.hidden(word_ids(cdict[c][i]))[0].mean(0).cpu().numpy() for i in range(5)} for c in cdict}
    same, diff = [], []
    cs = list(cdict)
    for c in cs:
        for i in range(5):
            for j in range(i+1, 5): same.append(cos(V[c][LANGS[i]], V[c][LANGS[j]]))
    rng = random.Random(SEED)
    for _ in range(len(same)):
        c1, c2 = rng.sample(cs, 2); diff.append(cos(V[c1][rng.choice(LANGS)], V[c2][rng.choice(LANGS)]))
    same, diff = np.array(same), np.array(diff)
    psd = math.sqrt((same.var(ddof=1)+diff.var(ddof=1))/2) or 1e-9
    d = (same.mean()-diff.mean())/psd; base = float(diff.mean())
    pl = {LANGS[i]: float(np.mean([cos(V[c]["en"], V[c][LANGS[i]]) for c in cs])) for i in range(5)}
    nlang = sum(1 for lg in LANGS if pl[lg] > base + 0.05)
    print(f"  [{tag}] d={d:.4f} same={same.mean():.3f} diff={diff.mean():.3f} langs_above={nlang}/5", flush=True)
    return {"cohen_d": float(d), "langs_above": nlang, "perlang": pl}


def main():
    print("=== H_1156 cross-lingual alignment training ===", flush=True)
    data = load_balanced()
    print("--- training NO-alignment (control) ---", flush=True)
    m0 = train(data, False)
    ctrl_held = interlingua_d(m0, HELD_C, "ctrl-heldout")
    print("--- training WITH-alignment ---", flush=True)
    m1 = train(data, True)
    aln_train = interlingua_d(m1, TRAIN_C, "aln-train(sanity)")
    aln_held = interlingua_d(m1, HELD_C, "aln-heldout")

    f1 = aln_held["cohen_d"] >= 0.8
    f2 = aln_held["langs_above"] == 5
    ctl = ctrl_held["cohen_d"] <= 0.3
    supported = bool(f1 and f2 and ctl)
    verdict = {
        "H": "H_1156", "title": "explicit cross-lingual alignment training builds a generalizing interlingua bridge",
        "F1_heldout_alignment": {"cohen_d": aln_held["cohen_d"], "bar": 0.8, "pass": bool(f1)},
        "F2_heldout_5of5": {"langs_above": aln_held["langs_above"], "bar": 5, "pass": bool(f2)},
        "control_noaln_heldout": {"cohen_d": ctrl_held["cohen_d"], "bar_max": 0.3, "pass": bool(ctl)},
        "sanity_train_concepts_d": aln_train["cohen_d"],
        "h1155_ref_d": -0.226,
        "supported": supported,
        "ruling": ("SUPPORTED: explicit alignment BUILDS a generalizing interlingua (held-out concepts align) — path-(1) works for 5-lang completeness"
                   if supported else
                   ("CLOSED-NEGATIVE: alignment only MEMORIZES trained pairs (train aligns, held-out does NOT generalize) — no general bridge"
                    if aln_train["cohen_d"] >= 0.8 and not f1 else
                    "CLOSED-NEGATIVE: alignment loss did not even build interlingua on trained concepts at toy scale")),
        "scope": "toy ByteGPT d256/4L CPU 5×6MB; alignment on 8 train concepts, measured on 4 held-out — scale-up UNVERIFIED (a_scale_honest_scope)",
    }
    print("\n=== VERDICT ===\n"+json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1156_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done] /tmp/h1156_result.json", flush=True)


if __name__ == "__main__": main()
