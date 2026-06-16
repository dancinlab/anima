#!/usr/bin/env python3
"""h1139_7b_balanced_5lang.py — BALANCED-corpus 7B × per-language recombination.

THE ONE UNTESTED RECIPE AXIS H_1138 LEFT OPEN: a balanced-5lang-corpus 7B.
  H_1137: BALANCED 303M (full 1.5GB random-window, val_ce 1.366) → 3/5 (en/zh/ko);
          ru/ja failed even dedicated passes → 303M concept-coverage limit.
  H_1138: broad-WIKI-converged 7B (70/30 wiki/dialogue, val_ce 1.66) → 0/5
          → corpus/training axis DOMINATES capacity.
  H_1139 (THIS): continue-train the SAME 7B base on the PURE balanced 5-lang
          corpus (the H_1137 303M recipe at 20× capacity) → per-language ladder.
          Do ru/ja clear once concept capacity is 20×?

TRAINING (proven pieces only, H_1128 80GB recipe):
  * bf16 MODEL + bf16 AdamW states (plain torch AdamW, NO bitsandbytes)
    + gradient-checkpointing → peak ~72.6GB on one 80GB GPU (H_1128 measured).
  * random-window byte batches over the FULL 1.5GB 5-lang corpus
    (en/zh/ru/ja/ko 300MB each → random windows = balanced sampling,
    the H_1137 sampler VERBATIM), cosine + warmup, continue-train lr 8e-5.
  * eval val_ce every eval_every; per-language ladder at mid-train checkpoints
    (EARLY-SUCCESS: stop + harvest immediately if 5/5 at any checkpoint).

FROZEN FALSIFIER (per language, pre-registered, IDENTICAL to H_1137/H_1138 —
NO goalpost move):
  🟢 for lang L iff some k in {2,3,4,5} has
       composed_distinct(L,k) >= 2 AND > max_single(L) AND in_script_ratio(L,k) >= 0.50.
  Finding = n_emergent/5 (balanced-7B) vs 3/5 (balanced-303M) vs 0/5 (wiki-7B).

Lane-G/torch REFERENCE mouth (a_clm_gen_pipeline) — NOT the CORE substrate
(a_core_engine_map). a_scale_honest_scope: 7B-scale single-rung measurement.
a_lane_akida_gpu_split: substrate = PyTorch-CUDA (Lane-G), NOT AKIDA.
"""
from __future__ import annotations
import argparse, json, math, re as _re, time
import torch, torch.nn as nn, torch.nn.functional as F


# ─────────────────────────────────────────────────────────────────────────────
# EXACT H_1128/H_1138 7B ByteGPT arch (vocab256/d4096/36L/32H/block512 = 7.25B)
# + the H_1137 grad_ckpt training hook. forward() returns (logits, loss) so
# BOTH the H_1137 training loop AND gen() (`logits, _ = m(ctx)`) work VERBATIM.
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
    def __init__(s, vocab=256, d=4096, n_layer=36, n_head=32, block=512, p=0.0, grad_ckpt=False):
        super().__init__()
        s.block = block; s.grad_ckpt = grad_ckpt
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    def forward(s, idx, targets=None):
        B, T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device, dtype=x.dtype), diagonal=1)
        for b in s.blocks:
            if s.grad_ckpt and s.training:
                x = torch.utils.checkpoint.checkpoint(b, x, mask, use_reentrant=False)
            else:
                x = b(x, mask)
        logits = s.head(s.ln_f(x))
        loss = F.cross_entropy(logits.view(-1, 256).float(), targets.view(-1)) if targets is not None else None
        return logits, loss


# ── H_1137 corpus loader + balanced random-window sampler — VERBATIM ────────
def load_bytes(p, cap):
    raw = open(p, "rb").read(cap)
    return torch.frombuffer(bytearray(raw), dtype=torch.uint8)  # keep uint8 (1.5GB RAM); cast per-batch

def batch(d, block, bs, dev):
    ix = torch.randint(0, d.numel()-block-1, (bs,))
    x = torch.stack([d[i:i+block] for i in ix]).to(dev).long()
    y = torch.stack([d[i+1:i+1+block] for i in ix]).to(dev).long()
    return x, y


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


def run_all_ladders(m, dev, block, tag):
    print(f"\n##### LADDER @ {tag} #####", flush=True)
    results = {}
    for lang in LANGS:
        results[lang] = run_ladder_lang(m, dev, block, lang)
    n_emergent = sum(1 for L in LANGS if results[L]["emergent"])
    print(f"##### LADDER @ {tag}: n_emergent = {n_emergent}/5 "
          f"[{' '.join(L for L in LANGS if results[L]['emergent'])}] #####", flush=True)
    return results, n_emergent


# ─────────────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="H_1128 broad 7B base ckpt (.pt)")
    ap.add_argument("--corpus", default="/workspace/corpus.txt")
    ap.add_argument("--cap_mb", type=float, default=1500.0)
    ap.add_argument("--bs", type=int, default=6); ap.add_argument("--accum", type=int, default=4)
    ap.add_argument("--steps", type=int, default=3500); ap.add_argument("--warmup", type=int, default=150)
    ap.add_argument("--lr", type=float, default=8e-5)
    ap.add_argument("--ckpt", default="/workspace/ckpt/h1139_best.pt")
    ap.add_argument("--eval_every", type=int, default=500)
    ap.add_argument("--ladder_every", type=int, default=1000)
    a = ap.parse_args()
    dev = "cuda" if torch.cuda.is_available() else "cpu"; torch.manual_seed(7)
    print(f"[dev] {dev} {torch.cuda.get_device_name(0) if dev=='cuda' else ''}", flush=True)

    data = load_bytes(a.corpus, int(a.cap_mb*1024*1024))
    n = data.numel(); tr = data; va = data  # byte-LM full-corpus windows; val_ce = balanced 5-lang signal
    print(f"[data] {n/1e6:.0f}MB (balanced 5-lang: en/zh/ru/ja/ko ~300MB each)", flush=True)

    ck = torch.load(a.base, map_location="cpu", weights_only=False); cfg = ck["config"]
    m = ByteGPT(cfg["vocab"], cfg["d"], cfg["n_layer"], cfg["n_head"], cfg["block"],
                grad_ckpt=True).to(torch.bfloat16)
    sd = ck["model"] if "model" in ck else ck
    m.load_state_dict(sd, strict=False); m = m.to(dev); block = cfg["block"]
    nparam = sum(p.numel() for p in m.parameters())
    print(f"[base] {a.base} cfg={cfg} val_ce={ck.get('val_ce')} step={ck.get('step')}", flush=True)
    print(f"[model] {nparam:,} params ({nparam/1e9:.2f}B) bf16 + grad-ckpt (H_1128 80GB recipe)", flush=True)
    del ck, sd

    # plain torch AdamW; states inherit bf16 from params (the H_1128 80GB trick)
    opt = torch.optim.AdamW(m.parameters(), lr=a.lr, betas=(0.9, 0.95), weight_decay=0.1)

    def eval_ce(d, iters=40):
        m.eval()
        with torch.no_grad():
            tot = 0.0
            for _ in range(iters):
                x, y = batch(d, block, a.bs, dev)
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16) if dev == "cuda" else torch.no_grad():
                    _, l = m(x, y)
                tot += l.item()
        m.train(); return tot/iters

    def save_ckpt(path, vce, st):
        torch.save({"model": m.state_dict(), "config": cfg,
                    "val_ce": vce, "step": st, "nparam": nparam}, path)

    best = 1e9; t0 = time.time(); m.train()
    curve = []; mid_ladders = {}; early_5of5 = False
    for st in range(a.steps):
        lr_t = a.lr*(st+1)/a.warmup if st < a.warmup else a.lr*0.5*(1+math.cos(math.pi*min(1.0,(st-a.warmup)/max(1,a.steps-a.warmup))))
        for g in opt.param_groups: g["lr"] = lr_t
        opt.zero_grad(set_to_none=True); acc = 0.0
        for _ in range(a.accum):
            x, y = batch(tr, block, a.bs, dev)
            if dev == "cuda":
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16): _, l = m(x, y)
            else: _, l = m(x, y)
            (l/a.accum).backward(); acc += l.item()/a.accum
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % a.eval_every == 0 or st == a.steps-1:
            vce = eval_ce(va)
            curve.append({"step": st, "train_ce": round(acc, 4), "val_ce": round(vce, 4)})
            print(f"  step {st:5d} train_ce={acc:.4f} val_ce={vce:.4f} lr={lr_t:.2e} "
                  f"{(time.time()-t0)/60:.1f}min mem={torch.cuda.max_memory_allocated()/2**30:.1f}GB"
                  if dev == "cuda" else
                  f"  step {st:5d} train_ce={acc:.4f} val_ce={vce:.4f} lr={lr_t:.2e}", flush=True)
            if vce < best:
                best = vce; save_ckpt(a.ckpt, vce, st)
                print(f"  [ckpt] saved best val_ce={vce:.4f} @ step {st}", flush=True)
        if a.ladder_every and st > 0 and st % a.ladder_every == 0:
            _, n_mid = run_all_ladders(m, dev, block, f"step{st}")
            mid_ladders[st] = n_mid; m.train()
            if n_mid == 5:  # EARLY-SUCCESS: 5/5 mid-train → harvest immediately
                print(f"[early-success] 5/5 at step {st} — saving + stopping", flush=True)
                vce = eval_ce(va); save_ckpt(a.ckpt, vce, st); best = min(best, vce)
                early_5of5 = True; break
    print(f"[train] done best_val_ce={best:.4f} ckpt={a.ckpt} "
          f"wall={(time.time()-t0)/60:.1f}min", flush=True)

    # ── FINAL per-language ladder on the best ckpt ──
    ck = torch.load(a.ckpt, map_location="cpu", weights_only=False)
    m.load_state_dict(ck["model"]); m = m.to(dev); m.grad_ckpt = False
    results, n_emergent = run_all_ladders(m, dev, block, "BEST")

    print("\n=== H_1139 BALANCED-7B 5-LANGUAGE RECOMBINATION ===", flush=True)
    for L in LANGS:
        R = results[L]
        bestisr = max((R["ladder"][k]["isr"] for k in (2,3,4,5)), default=0.0)
        print(f"  {L}: emergent={R['emergent']} max_single={R['max_single']} best_isr={bestisr:.2f}", flush=True)
    print(f"\n  LANGUAGES CLEARED (balanced-7B, THIS) = {n_emergent}/5", flush=True)
    print(f"  LANGUAGES CLEARED (balanced-303M)     = 3/5  (H_1137: en/zh/ko)", flush=True)
    print(f"  LANGUAGES CLEARED (wiki-7B)           = 0/5  (H_1138)", flush=True)
    lift = n_emergent - 3
    if n_emergent == 5:
        verdict = "🟢 ALL-5-AT-BALANCED-7B (corpus×capacity conjunction completes 5/5)"
    elif n_emergent > 3:
        verdict = f"🟢 CAPACITY-LIFTS-ON-BALANCED ({n_emergent}/5 > 303M 3/5)"
    elif n_emergent == 3:
        verdict = "🔴 NO-LIFT (balanced-7B == balanced-303M 3/5; capacity ⊥ per-lang bound)"
    else:
        verdict = f"🔴 BELOW-303M ({n_emergent}/5 < 3/5)"
    print(f"  Δ vs balanced-303M = {lift:+d} · Δ vs wiki-7B = {n_emergent:+d}", flush=True)
    print(f"  F-7B-BALANCED-5LANG = {n_emergent} {verdict}", flush=True)
    print(f"  Lane-G torch REFERENCE mouth (a_clm_gen_pipeline); a_scale_honest_scope 7B single-rung.", flush=True)

    out = {"nparam": nparam, "best_val_ce": best, "curve": curve,
           "mid_ladders": mid_ladders, "early_5of5": early_5of5,
           "n_emergent_balanced_7b": n_emergent, "n_emergent_303m_baseline": 3,
           "n_emergent_wiki7b_baseline": 0, "delta_vs_303m": lift, "verdict": verdict,
           "results": {L: {"emergent": results[L]["emergent"], "max_single": results[L]["max_single"],
                           "ladder": results[L]["ladder"]} for L in LANGS}}
    json.dump(out, open("/workspace/h1139_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done] wrote /workspace/h1139_result.json", flush=True)


if __name__ == "__main__": main()
