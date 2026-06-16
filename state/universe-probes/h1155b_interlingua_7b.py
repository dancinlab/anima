"""
H_1155b — interlingua probe on the REAL balanced-5lang 7B (h1141_best.pt, the live
H_1141 fire ckpt). Decisive scale-up of H_1155 (toy byte showed NO interlingua;
does the 7B that gives 3/5 carry cross-lingual SEMANTIC alignment the surface
metric missed?). CPU-only (CUDA_VISIBLE_DEVICES='') so training on GPU is untouched.
"""
import os, math, json
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

os.environ["CUDA_VISIBLE_DEVICES"] = ""
DEV = "cpu"
CKPT = "/workspace/ckpt/h1141_best.pt"
LANGS = ["en", "zh", "ru", "ja", "ko"]
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
SEED = 7


class Block(nn.Module):
    def __init__(s, d, h, p):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.attn = nn.MultiheadAttention(d, h, dropout=p, batch_first=True)
        s.ln2 = nn.LayerNorm(d); s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d), nn.Dropout(p))
    def forward(s, x, m):
        h = s.ln1(x); a, _ = s.attn(h, h, h, attn_mask=m, need_weights=False); x = x + a
        return x + s.mlp(s.ln2(x))

class ByteGPT(nn.Module):
    def __init__(s, vocab=256, d=4096, n_layer=36, n_head=32, block=512, p=0.0, grad_ckpt=False):
        super().__init__()
        s.block = block; s.grad_ckpt = grad_ckpt
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    def hidden(s, idx):
        T = idx.shape[1]
        x = s.drop(s.tok(idx) + s.pos(torch.arange(T, device=idx.device))[None])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), 1)
        for b in s.blocks: x = b(x, mask)
        return s.ln_f(x)


def auroc_cos(a, b): return float(np.dot(a, b))

@torch.no_grad()
def embed(m, word):
    bs = word.encode("utf-8", "ignore")[:m.block]
    ids = torch.tensor(list(bs) or [0], dtype=torch.long, device=DEV)[None]
    h = m.hidden(ids)[0].mean(0).float().cpu().numpy()
    n = np.linalg.norm(h); return h/n if n > 0 else h


def measure(m, tag):
    import random
    V = {c: {lg: embed(m, CONCEPTS[c][lg]) for lg in LANGS} for c in CONCEPTS}
    same, diff = [], []
    cs = list(CONCEPTS)
    for c in cs:
        for i in range(len(LANGS)):
            for j in range(i+1, len(LANGS)):
                same.append(auroc_cos(V[c][LANGS[i]], V[c][LANGS[j]]))
    rng = random.Random(SEED)
    for _ in range(len(same)):
        c1, c2 = rng.sample(cs, 2); same_count = auroc_cos(V[c1][rng.choice(LANGS)], V[c2][rng.choice(LANGS)])
        diff.append(same_count)
    same, diff = np.array(same), np.array(diff)
    psd = math.sqrt((same.var(ddof=1)+diff.var(ddof=1))/2) or 1e-9
    d = (same.mean()-diff.mean())/psd
    base = float(diff.mean()); perlang = {}
    for lg in LANGS:
        al = float(np.mean([auroc_cos(V[c]["en"], V[c][lg]) for c in cs]))
        perlang[lg] = {"align_to_en": al, "above_baseline": bool(al > base + 0.05)}
    print(f"  [{tag}] same={same.mean():.4f} diff={diff.mean():.4f} d={d:.4f}", flush=True)
    print("  [{}] per-lang: {}".format(tag, " ".join(f"{lg}={perlang[lg]['align_to_en']:.3f}{'+' if perlang[lg]['above_baseline'] else '-'}" for lg in LANGS)), flush=True)
    return {"same_mean": float(same.mean()), "diff_mean": float(diff.mean()), "cohen_d": float(d), "perlang": perlang}


def main():
    print("=== H_1155b interlingua on REAL 5lang 7B (h1141_best.pt) ===", flush=True)
    ck = torch.load(CKPT, map_location="cpu", weights_only=False)
    cfg = ck.get("config", {"vocab": 256, "d": 4096, "n_layer": 36, "n_head": 32, "block": 512})
    print(f"[ckpt] config={cfg} val_ce={ck.get('val_ce')} step={ck.get('step')}", flush=True)
    m = ByteGPT(vocab=cfg["vocab"], d=cfg["d"], n_layer=cfg["n_layer"], n_head=cfg["n_head"], block=cfg["block"])
    m.load_state_dict(ck["model"]); m.float(); m.eval()
    print("[model] loaded 7B to CPU fp32", flush=True)
    tr = measure(m, "7B-trained")
    f1 = tr["cohen_d"] >= 0.8
    f2_langs = [lg for lg in LANGS if tr["perlang"][lg]["above_baseline"]]
    verdict = {
        "H": "H_1155b", "title": "interlingua on the real balanced-5lang 7B (h1141 fire ckpt)",
        "ckpt_val_ce": ck.get("val_ce"), "ckpt_step": ck.get("step"),
        "F1_alignment": {"cohen_d": tr["cohen_d"], "bar": 0.8, "pass": bool(f1)},
        "F2_perlang": {"aligned_langs": f2_langs, "n": len(f2_langs), "bar": 5, "pass": bool(len(f2_langs) == 5)},
        "ru_ja_semantic_pass": {lg: tr["perlang"][lg]["above_baseline"] for lg in ("ru", "ja")},
        "trained": tr,
        "vs_toy": "H_1155 toy d=−0.226 (no interlingua); does the 7B differ?",
        "ruling": ("SUPPORTED: the 7B DOES carry cross-lingual interlingua the toy lacked — the ru/ja 3/5 ceiling was a surface-metric artifact"
                   if (f1 and len(f2_langs) == 5) else
                   "CLOSED-NEGATIVE: even the real 5lang 7B shows no cross-lingual semantic alignment — the ceiling is real, not just a metric artifact"),
        "scope": "real 7.25B balanced-5lang ckpt (val_ce ~1.43, mid-train best); Lane-G reference; mean-pool hidden",
    }
    print("\n=== VERDICT ===\n"+json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/workspace/h1155b_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done] /workspace/h1155b_result.json", flush=True)


if __name__ == "__main__": main()
