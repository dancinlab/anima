"""
H_1155 — INTERLINGUA: does the model align the SAME concept across 5 languages by
MEANING (hidden cosine), even where the surface keyword metric (H_1137) caps ru/ja?

ONE balanced-5lang toy ByteGPT; measure interlingua cosine + an untrained control.
FROZEN FALSIFIER:
  F1: mean(same-concept cross-lingual cosine) − mean(different-concept cosine) d ≥ 0.8
  F2: each of 5 langs aligns to the English anchor above the unrelated-pair baseline
  CONTROL: untrained backbone shows NO alignment (d ≤ 0.3) — must be LEARNED
toy-scope (a_scale_honest_scope). xref h1137/1138/1139.
"""
import os, math, json, time, random
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

DEV = "cpu"
CORPUS = "/home/summer/anima_chat_smoke/corpus_5lang_1p5gb.txt"
PER_LANG_OFFSET = 300 * 1024 * 1024       # corpus order en,zh,ru,ja,ko
SLICE = 6 * 1024 * 1024                    # 6MB per language
BLOCK = 128; D = 256; NLAYER = 4; NHEAD = 4; VOCAB = 256
STEPS = 2000; BS = 16; LR = 3e-4; SEED = 7
LANGS = ["en", "zh", "ru", "ja", "ko"]

# same concept in 5 languages (real translations)
CONCEPTS = {
    "consciousness": {"en": "consciousness", "zh": "意识", "ru": "сознание", "ja": "意識", "ko": "의식"},
    "tension":       {"en": "tension", "zh": "张力", "ru": "напряжение", "ja": "緊張", "ko": "긴장"},
    "memory":        {"en": "memory", "zh": "记忆", "ru": "память", "ja": "記憶", "ko": "기억"},
    "silence":       {"en": "silence", "zh": "沉默", "ru": "тишина", "ja": "沈黙", "ko": "침묵"},
    "engine":        {"en": "engine", "zh": "引擎", "ru": "двигатель", "ja": "エンジン", "ko": "엔진"},
    "dream":         {"en": "dream", "zh": "梦", "ru": "сон", "ja": "夢", "ko": "꿈"},
    "cell":          {"en": "cell", "zh": "细胞", "ru": "клетка", "ja": "細胞", "ko": "세포"},
    "field":         {"en": "field", "zh": "场", "ru": "поле", "ja": "場", "ko": "장"},
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


def load_balanced():
    parts = []
    with open(CORPUS, "rb") as f:
        for i in range(5):
            f.seek(i*PER_LANG_OFFSET); parts.append(f.read(SLICE))
    raw = b"".join(parts)
    return torch.frombuffer(bytearray(raw), dtype=torch.uint8)

def train(data, do_train=True):
    torch.manual_seed(SEED); m = ByteGPT().to(DEV)
    if not do_train: m.eval(); return m
    m.train(); opt = torch.optim.AdamW(m.parameters(), lr=LR, betas=(0.9, 0.95), weight_decay=0.1)
    g = torch.Generator(device=DEV).manual_seed(SEED)
    for st in range(STEPS):
        lr_t = LR*min(1.0, (st+1)/100)*(0.5*(1+math.cos(math.pi*min(1.0, st/STEPS))))
        for pg in opt.param_groups: pg["lr"] = lr_t
        ix = torch.randint(0, data.numel()-BLOCK-1, (BS,), generator=g)
        x = torch.stack([data[j:j+BLOCK] for j in ix]).long().to(DEV)
        y = torch.stack([data[j+1:j+BLOCK+1] for j in ix]).long().to(DEV)
        _, l = m(x, y)
        opt.zero_grad(set_to_none=True); l.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % 500 == 0 or st == STEPS-1: print(f"  [train] step {st} ce={l.item():.4f}", flush=True)
    m.eval(); return m


@torch.no_grad()
def embed(m, word):
    bs = word.encode("utf-8", "ignore")[:BLOCK]
    ids = torch.tensor(list(bs) or [0], dtype=torch.long, device=DEV)[None]
    h = m.hidden(ids)[0].mean(0).cpu().numpy()
    n = np.linalg.norm(h)
    return h/n if n > 0 else h

def cos(a, b): return float(np.dot(a, b))


def measure(m, tag):
    # vec[concept][lang]
    V = {c: {lg: embed(m, CONCEPTS[c][lg]) for lg in LANGS} for c in CONCEPTS}
    same, diff = [], []
    concepts = list(CONCEPTS)
    # same-concept cross-lingual pairs
    for c in concepts:
        for i in range(len(LANGS)):
            for j in range(i+1, len(LANGS)):
                same.append(cos(V[c][LANGS[i]], V[c][LANGS[j]]))
    # different-concept pairs (any lang), matched count via sampling
    rng = random.Random(SEED)
    for _ in range(len(same)):
        c1, c2 = rng.sample(concepts, 2); l1, l2 = rng.choice(LANGS), rng.choice(LANGS)
        diff.append(cos(V[c1][l1], V[c2][l2]))
    same, diff = np.array(same), np.array(diff)
    pooled_sd = math.sqrt((same.var(ddof=1)+diff.var(ddof=1))/2) or 1e-9
    d = (same.mean()-diff.mean())/pooled_sd
    # per-lang: each non-en lang's concept-word vs its English anchor (same concept) > unrelated baseline
    perlang = {}
    base = float(diff.mean())
    for lg in LANGS:
        al = np.mean([cos(V[c]["en"], V[c][lg]) for c in concepts])
        perlang[lg] = {"align_to_en": float(al), "above_baseline": bool(al > base + 0.05)}
    print(f"  [{tag}] same={same.mean():.4f} diff={diff.mean():.4f} d={d:.4f}", flush=True)
    print(f"  [{tag}] per-lang align_to_en: " +
          " ".join(f"{lg}={perlang[lg]['align_to_en']:.3f}{'+' if perlang[lg]['above_baseline'] else '-'}" for lg in LANGS), flush=True)
    return {"same_mean": float(same.mean()), "diff_mean": float(diff.mean()), "cohen_d": float(d), "perlang": perlang}


def main():
    print("=== H_1155 interlingua semantic alignment ===", flush=True)
    random.seed(SEED); np.random.seed(SEED)
    data = load_balanced()
    print(f"[corpus] balanced 5-lang {data.numel()} bytes", flush=True)
    print("\n--- CONTROL: untrained ---", flush=True)
    ctrl = measure(train(data, do_train=False), "untrained")
    print("\n--- training balanced-5lang ---", flush=True)
    m = train(data)
    print("\n--- TRAINED interlingua ---", flush=True)
    tr = measure(m, "trained")

    f1 = tr["cohen_d"] >= 0.8
    f2_langs = [lg for lg in LANGS if tr["perlang"][lg]["above_baseline"]]
    f2 = len(f2_langs) == 5
    ctl = ctrl["cohen_d"] <= 0.3
    supported = bool(f1 and f2 and ctl)
    ruja = {lg: tr["perlang"][lg]["above_baseline"] for lg in ("ru", "ja")}
    verdict = {
        "H": "H_1155", "title": "interlingua — cross-lingual semantic alignment vs surface keyword ceiling",
        "F1_alignment": {"cohen_d": tr["cohen_d"], "bar": 0.8, "pass": bool(f1)},
        "F2_perlang_5of5": {"aligned_langs": f2_langs, "n": len(f2_langs), "bar": 5, "pass": bool(f2)},
        "control_untrained": {"cohen_d": ctrl["cohen_d"], "bar_max": 0.3, "pass": bool(ctl)},
        "ru_ja_semantic_pass": ruja,
        "trained": tr, "untrained": ctrl,
        "supported": supported,
        "ruling": ("SUPPORTED: interlingua EXISTS — concepts align cross-lingually by meaning; "
                   "the H_1137 surface ceiling (ru/ja 3/5) UNDERSOLD semantic alignment"
                   if supported else
                   "CLOSED-NEGATIVE: no learned cross-lingual semantic alignment at toy scale "
                   "(the 3/5 surface ceiling is NOT just a metric artifact here)"),
        "scope": "toy ByteGPT d256/4L CPU, balanced 5×6MB — scale-up to 303M/7B UNVERIFIED (a_scale_honest_scope)",
    }
    print("\n=== VERDICT ===\n"+json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1155_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done] /tmp/h1155_result.json", flush=True)


if __name__ == "__main__": main()
