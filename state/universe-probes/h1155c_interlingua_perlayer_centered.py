"""
H_1155c — interlingua on the real 5lang 7B, DEBIASED: per-LAYER + CENTERED cosine.
H_1155b found d≈0 but reps were ANISOTROPIC (all ~0.90 cosine). This removes the
dominant common direction (centering) and scans ALL 36 layers — does a MIDDLE layer
or a centered metric reveal cross-lingual semantic alignment the final-layer raw
cosine masked? CPU-only, GPU untouched.
"""
import os, math, json
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

os.environ["CUDA_VISIBLE_DEVICES"] = ""
DEV = "cpu"; CKPT = "/workspace/ckpt/h1141_best.pt"; SEED = 7
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


class Block(nn.Module):
    def __init__(s, d, h, p):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.attn = nn.MultiheadAttention(d, h, dropout=p, batch_first=True)
        s.ln2 = nn.LayerNorm(d); s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d), nn.Dropout(p))
    def forward(s, x, m):
        h = s.ln1(x); a, _ = s.attn(h, h, h, attn_mask=m, need_weights=False); x = x + a
        return x + s.mlp(s.ln2(x))

class ByteGPT(nn.Module):
    def __init__(s, vocab=256, d=4096, n_layer=36, n_head=32, block=512, p=0.0):
        super().__init__()
        s.block = block
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    @torch.no_grad()
    def layer_means(s, idx):
        T = idx.shape[1]
        x = s.tok(idx) + s.pos(torch.arange(T, device=idx.device))[None]
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), 1)
        outs = []
        for b in s.blocks:
            x = b(x, mask); outs.append(x[0].mean(0).float().cpu().numpy())   # per-layer mean-pool
        outs.append(s.ln_f(x)[0].mean(0).float().cpu().numpy())               # final ln_f
        return outs   # length n_layer+1


def cohen_d_interlingua(vecs_by_concept):  # vecs_by_concept[c][lang] = np vector (already used as-is)
    same, diff = [], []
    cs = list(vecs_by_concept)
    def cos(a, b):
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        return float(np.dot(a, b)/(na*nb)) if na > 0 and nb > 0 else 0.0
    for c in cs:
        for i in range(len(LANGS)):
            for j in range(i+1, len(LANGS)):
                same.append(cos(vecs_by_concept[c][LANGS[i]], vecs_by_concept[c][LANGS[j]]))
    import random
    rng = random.Random(SEED)
    for _ in range(len(same)):
        c1, c2 = rng.sample(cs, 2)
        diff.append(cos(vecs_by_concept[c1][rng.choice(LANGS)], vecs_by_concept[c2][rng.choice(LANGS)]))
    same, diff = np.array(same), np.array(diff)
    psd = math.sqrt((same.var(ddof=1)+diff.var(ddof=1))/2) or 1e-9
    return (same.mean()-diff.mean())/psd, float(same.mean()), float(diff.mean())


def main():
    print("=== H_1155c per-layer + centered interlingua (7B) ===", flush=True)
    ck = torch.load(CKPT, map_location="cpu", weights_only=False); cfg = ck["config"]
    m = ByteGPT(vocab=cfg["vocab"], d=cfg["d"], n_layer=cfg["n_layer"], n_head=cfg["n_head"], block=cfg["block"])
    m.load_state_dict(ck["model"]); m.float(); m.eval()
    print(f"[model] loaded 7B val_ce={ck.get('val_ce')} layers={cfg['n_layer']}", flush=True)
    # reps[layer][concept][lang]
    nL = cfg["n_layer"] + 1
    reps = [{c: {} for c in CONCEPTS} for _ in range(nL)]
    for c in CONCEPTS:
        for lg in LANGS:
            bs = CONCEPTS[c][lg].encode("utf-8", "ignore")[:cfg["block"]]
            ids = torch.tensor(list(bs) or [0], dtype=torch.long)[None]
            lm = m.layer_means(ids)
            for L in range(nL): reps[L][c][lg] = lm[L]
    results = []
    for L in range(nL):
        # RAW
        d_raw, s_raw, f_raw = cohen_d_interlingua(reps[L])
        # CENTERED: subtract global mean across all word-reps at this layer
        allv = np.stack([reps[L][c][lg] for c in CONCEPTS for lg in LANGS])
        mu = allv.mean(0)
        cen = {c: {lg: reps[L][c][lg]-mu for lg in LANGS} for c in CONCEPTS}
        d_cen, s_cen, f_cen = cohen_d_interlingua(cen)
        results.append({"layer": L, "raw_d": d_raw, "centered_d": d_cen,
                        "raw_same": s_raw, "raw_diff": f_raw, "cen_same": s_cen, "cen_diff": f_cen})
        if L % 6 == 0 or L == nL-1:
            print(f"  layer {L:2d}: raw_d={d_raw:+.3f} centered_d={d_cen:+.3f}", flush=True)
    best_raw = max(results, key=lambda r: r["raw_d"])
    best_cen = max(results, key=lambda r: r["centered_d"])
    supported = bool(best_cen["centered_d"] >= 0.8 or best_raw["raw_d"] >= 0.8)
    verdict = {
        "H": "H_1155c", "title": "per-layer + centered interlingua on the real 5lang 7B (debias H_1155b anisotropy)",
        "ckpt_val_ce": ck.get("val_ce"),
        "best_raw_layer": best_raw["layer"], "best_raw_d": best_raw["raw_d"],
        "best_centered_layer": best_cen["layer"], "best_centered_d": best_cen["centered_d"],
        "bar": 0.8, "supported": supported,
        "h1155b_final_raw_d": -0.038,
        "all_layers": results,
        "ruling": ("SUPPORTED: a debiased/per-layer metric DOES reveal cross-lingual interlingua the final-layer raw cosine masked (anisotropy was hiding it)"
                   if supported else
                   "CLOSED-NEGATIVE: no interlingua at ANY layer even after centering — the 7B genuinely lacks cross-lingual semantic alignment (ru/ja ceiling is real, not a metric/anisotropy artifact)"),
        "scope": "real 7.25B 5lang ckpt val_ce~1.43; per-layer mean-pool, centered cosine; Lane-G",
    }
    print("\n=== VERDICT ===\n"+json.dumps({k: v for k, v in verdict.items() if k != "all_layers"}, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/workspace/h1155c_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done] /workspace/h1155c_result.json", flush=True)


if __name__ == "__main__": main()
