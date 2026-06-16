#!/usr/bin/env python3
"""h1138_7b_5lang_recombination.py — 7B × per-language concept-recombination.

DOES THE 7B (20× the 303M of H_1137) achieve super-additive concept-recombination
in ALL 5 languages (en/zh/ru/ja/ko), where the 303M only got 3/5?

INFERENCE-FIRST, CHEAP. H_1128 already produced a 7.25B ByteGPT continue-trained on
the SAME balanced 5-lang corpus to convergence (val CE 1.66). It was scored 🔴 only
because it used an ENGLISH-keyword metric on script-collapsed output. H_1137 then
proved the right test is PER-LANGUAGE (in-language prompts + in-script coherence +
translated concept keywords). So: load the EXISTING H_1128 7B ckpt and run the H_1137
PER-LANGUAGE ladder on it — NO retraining. Inference-only.

This harness:
  * embeds the EXACT H_1128 7B ByteGPT arch (vocab256/d4096/36L/32H/block512, ~7.25B);
    forward() returns (logits, None) so H_1137's gen()/run_ladder_lang() work VERBATIM.
  * REUSES H_1137's per-language metric VERBATIM: LANGS, CONCEPTS, SCRIPT,
    in_script_ratio, coverage, gen, run_ladder_lang (copied byte-for-byte below).
  * gen() temp 0.7, top_k 40, seed 7 — matches H_1137 for comparability.

FROZEN FALSIFIER (per language, pre-registered, NO goalpost move — identical to H_1137):
  🟢 for lang L iff some k in {2,3,4,5} has
       composed_distinct(L,k) >= 2 AND > max_single(L) AND in_script_ratio(L,k) >= 0.50.
  Finding = n_emergent/5 at 7B vs the 303M's 3/5 (does capacity lift ru/ja?).

Lane-G/torch REFERENCE mouth (a_clm_gen_pipeline) — NOT the CORE substrate
(a_core_engine_map). a_scale_honest_scope: 7B-scale single-rung measurement.
a_lane_akida_gpu_split: substrate = PyTorch-CUDA (Lane-G), NOT AKIDA.
"""
from __future__ import annotations
import argparse, json, re as _re
import torch, torch.nn as nn, torch.nn.functional as F


# ─────────────────────────────────────────────────────────────────────────────
# EXACT H_1128 7B ByteGPT arch (vocab256/d4096/36L/32H/block512 = 7.25B).
# forward() returns (logits, None) — the ONLY adaptation vs h1128, so that
# H_1137's gen() (which does `logits, _ = m(ctx)`) works VERBATIM.
# ─────────────────────────────────────────────────────────────────────────────
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
        s.block = block; s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    def forward(s, idx, targets=None):
        B, T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for b in s.blocks: x = b(x, mask)
        return s.head(s.ln_f(x)), None  # (logits, None) — H_1137 gen() compatible


# ─────────────────────────────────────────────────────────────────────────────
# H_1137 per-language metric — COPIED VERBATIM (model-agnostic; calls gen(m,...)).
# ─────────────────────────────────────────────────────────────────────────────
@torch.no_grad()
def gen(m, seed, mx, dev, block, top_k=40, temp=0.7, seed_rng=7):
    m.eval()
    g = torch.Generator(device=dev); g.manual_seed(seed_rng)
    idx = torch.tensor([list(seed.encode("utf-8"))], dtype=torch.long, device=dev); out = []
    use_amp = (dev == "cuda")
    for _ in range(mx):
        ctx = idx[:, -block:]
        if use_amp:
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                logits, _ = m(ctx)
        else:
            logits, _ = m(ctx)
        logits = logits[:, -1, :].float() / temp
        if top_k:
            v, _ = torch.topk(logits, top_k); logits[logits < v[:, [-1]]] = float("-inf")
        nb = torch.multinomial(F.softmax(logits, -1), 1, generator=g).item(); out.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=dev)], 1)
        if "\n\n" in bytes(out).decode("utf-8", "ignore"): break
    return bytes(out).decode("utf-8", "ignore").strip()


# 5 concepts, translated; coverage = substring match (works for no-space scripts).
LANGS = ["en", "zh", "ru", "ja", "ko"]
CONCEPTS = {
 "en": [("consciousness arises from cells", ["consciousness","cells","mind","aware"]),
        ("tension ripples between distant minds", ["tension","ripple","distant","between"]),
        ("memory composes into new meaning", ["memory","meaning","compose","new"]),
        ("silence still carries information", ["silence","information","quiet","carries"]),
        ("the engine dreams when alone", ["dream","engine","alone","sleep"])],
 "ko": [("의식은 세포에서 일어난다", ["의식","세포","마음","정신"]),
        ("긴장은 먼 마음 사이에 퍼진다", ["긴장","물결","먼","사이"]),
        ("기억은 새로운 의미로 구성된다", ["기억","의미","구성","새로"]),
        ("침묵은 여전히 정보를 전달한다", ["침묵","정보","조용","전달"]),
        ("엔진은 혼자일 때 꿈꾼다", ["꿈","엔진","혼자","잠"])],
 "ja": [("意識は細胞から生じる", ["意識","細胞","心","精神"]),
        ("緊張は遠い心の間に波及する", ["緊張","波","遠","間"]),
        ("記憶は新しい意味を構成する", ["記憶","意味","構成","新"]),
        ("沈黙はなお情報を運ぶ", ["沈黙","情報","静","運"]),
        ("エンジンは一人のとき夢を見る", ["夢","エンジン","一人","眠"])],
 "zh": [("意识源于细胞", ["意识","细胞","心灵","觉"]),
        ("紧张在远方的心灵之间荡漾", ["紧张","波","远","之间"]),
        ("记忆组成新的意义", ["记忆","意义","组成","新"]),
        ("沉默仍然传递信息", ["沉默","信息","静","传"]),
        ("引擎独处时做梦", ["梦","引擎","独","睡"])],
 "ru": [("сознание возникает из клеток", ["сознание","клетк","разум","ум"]),
        ("напряжение распространяется между далёкими умами", ["напряжен","рябь","далёк","между"]),
        ("память складывается в новый смысл", ["память","смысл","состав","новы"]),
        ("тишина всё ещё несёт информацию", ["тишин","информаци","тих","нес"]),
        ("двигатель видит сны когда один", ["сон","двигател","один","спать"])],
}
SCRIPT = {
 "en": _re.compile(r"[A-Za-z]"),
 "ru": _re.compile(r"[Ѐ-ӿ]"),
 "zh": _re.compile(r"[一-鿿]"),
 "ja": _re.compile(r"[぀-ヿ一-鿿]"),
 "ko": _re.compile(r"[가-힣]"),
}

def in_script_ratio(text, lang):
    chars = [c for c in text if not c.isspace()]
    if not chars: return 0.0
    rx = SCRIPT[lang]
    return sum(1 for c in chars if rx.match(c)) / len(chars)

def coverage(text, lang):
    return [i for i, (_, kws) in enumerate(CONCEPTS[lang]) if any(k in text for k in kws)]


def run_ladder_lang(m, dev, block, lang):
    print(f"\n========== LANG = {lang} ==========", flush=True)
    singles = []
    for i, (c, _) in enumerate(CONCEPTS[lang]):
        o = gen(m, c + ". ", 70, dev, block)
        cv = coverage(o, lang); singles.append(len(cv))
        print(f"  [{lang} single {i}] cov={cv} isr={in_script_ratio(o,lang):.2f} :: {o[:70]}", flush=True)
    max_single = max(singles) if singles else 0
    ladder = {}; emergent = False
    for k in (2, 3, 4, 5):
        seed = ". ".join(c for c, _ in CONCEPTS[lang][:k]) + ". "
        o = gen(m, seed, 110, dev, block)
        cv = coverage(o, lang); isr = in_script_ratio(o, lang)
        coherent = isr >= 0.50
        clears = (len(cv) >= 2 and len(cv) > max_single and coherent)
        emergent = emergent or clears
        ladder[k] = {"composed_distinct": len(cv), "coverage": cv, "isr": round(isr, 3),
                     "coherent": coherent, "clears": clears, "text": o}
        print(f"  [{lang} k={k}] composed_distinct={len(cv)} cov={cv} isr={isr:.2f} coherent={coherent} clears={clears}", flush=True)
        print(f"        >> {o[:120]}", flush=True)
    print(f"  [{lang}] max_single={max_single} EMERGENT={emergent}", flush=True)
    return {"max_single": max_single, "ladder": ladder, "emergent": emergent}


# ─────────────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    a = ap.parse_args()
    dev = "cuda" if torch.cuda.is_available() else "cpu"; torch.manual_seed(7)
    print(f"[dev] {dev} {torch.cuda.get_device_name(0) if dev=='cuda' else ''}", flush=True)
    ck = torch.load(a.ckpt, map_location="cpu", weights_only=False); cfg = ck["config"]
    dt = torch.bfloat16
    m = ByteGPT(cfg["vocab"], cfg["d"], cfg["n_layer"], cfg["n_head"], cfg["block"]).to(dt)
    sd = ck["model"] if "model" in ck else ck
    m.load_state_dict(sd, strict=False); m = m.to(dev); block = cfg["block"]
    nparam = sum(p.numel() for p in m.parameters())
    print(f"[mouth] H_1128 broad-converged-7B on {dev}/{dt}", flush=True)
    print(f"[mouth] {nparam:,} params ({nparam/1e9:.2f}B); cfg={cfg}; "
          f"val_ce={ck.get('val_ce')} step={ck.get('step')}", flush=True)

    # ── per-language ladder over all 5 LANGS (H_1137 run_ladder_lang VERBATIM) ──
    results = {}
    for lang in LANGS:
        results[lang] = run_ladder_lang(m, dev, block, lang)
    n_emergent = sum(1 for L in LANGS if results[L]["emergent"])

    print("\n=== H_1138 7B 5-LANGUAGE RECOMBINATION (vs H_1137 303M 3/5) ===", flush=True)
    for L in LANGS:
        R = results[L]
        bestisr = max((R["ladder"][k]["isr"] for k in (2,3,4,5)), default=0.0)
        print(f"  {L}: emergent={R['emergent']} max_single={R['max_single']} "
              f"best_isr={bestisr:.2f}", flush=True)
    print(f"\n  LANGUAGES CLEARED (7B)   = {n_emergent}/5", flush=True)
    print(f"  LANGUAGES CLEARED (303M) = 3/5  (H_1137 baseline)", flush=True)
    lift = n_emergent - 3
    if n_emergent == 5:
        verdict = "🟢 ALL-5-AT-7B (capacity lifts all)"
    elif n_emergent > 3:
        verdict = f"🟢 CAPACITY-LIFTS ({n_emergent}/5 > 303M 3/5)"
    elif n_emergent == 3:
        verdict = "🔴 NO-LIFT (7B == 303M 3/5; not capacity — concept-density bound)"
    else:
        verdict = f"🔴 BELOW-303M ({n_emergent}/5 < 3/5)"
    print(f"  Δ vs 303M = {lift:+d}", flush=True)
    print(f"  F-7B-5LANG = {n_emergent} {verdict}", flush=True)
    print(f"  Lane-G torch REFERENCE mouth (a_clm_gen_pipeline); a_scale_honest_scope 7B single-rung.", flush=True)

    out = {"nparam": nparam, "val_ce": ck.get("val_ce"), "n_emergent_7b": n_emergent,
           "n_emergent_303m_baseline": 3, "delta_vs_303m": lift, "verdict": verdict,
           "results": {L: {"emergent": results[L]["emergent"], "max_single": results[L]["max_single"],
                           "ladder": results[L]["ladder"]} for L in LANGS}}
    json.dump(out, open("/tmp/h1138_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done] wrote /tmp/h1138_result.json", flush=True)


if __name__ == "__main__": main()
