#!/usr/bin/env python3
"""h1141_7b_g5_eval.py — measure the G5 gate (NO HALLUCINATION) from
/7B_PASS_CONDITIONS.md on the H_1141 7B ckpt. The LAST open a7b_pass gate.

  ckpt = dancinlab/anima-clm-7b-h1141-g1pass-step6500 (h1141_g1pass_step6500.pt,
         7,252,828,160 params, sha256 4de903714112c26c826a983797e5dfea0c7b3c1f19f15a34dd35822f33e245d9).

G5-L1 LEXICAL (frozen): fabricated-word-rate = fraction of latin word-tokens NOT
  in /usr/share/dict/words. PASS iff L1 <= 0.30 (>=70% real words). Computed on
  fresh G2-style idea generations (temp 0.85, seeds {7,8,9}).

G5-L2 FAITHFULNESS (frozen): feed the FIRST HALF of N verbatim corpus sentences;
  for each, measure word-overlap of the model's continuation vs the TRUE corpus
  continuation. PASS iff on closed/factual prompts the model is grounded (overlap
  distribution clearly above a random-continuation control) rather than
  confabulating. We operationalize "clearly above" as a frozen pre-registered
  bound: mean(true-overlap) - mean(random-control-overlap) effect with Cohen's
  d >= 0.8 AND mean_true > mean_random (deterministic, seed 7, p7, NOT LLM judge).

ByteGPT arch + gen()/kwr code = h1141_7b_pass_attempt.py VERBATIM.
Corpus = build_wiki5_bigcorpus.py source (wikimedia/wikipedia 20231101 en/zh/ru/ja/ko,
300MB/lang) — the SAME deterministic corpus the model trained on; we probe the
English (closed/factual prose) portion for L2 verbatim sentences.

a_scale_honest_scope: 7B single-rung. a_lane_akida_gpu_split: substrate=PyTorch-CUDA
(Lane-G ref). p7 (word-overlap/dict, NOT perplexity, NOT LLM judge). seed 7.
"""
from __future__ import annotations
import argparse, json, math, os, re as _re, statistics, sys, time
import torch, torch.nn as nn, torch.nn.functional as F


# ── ByteGPT arch — h1141_7b_pass_attempt.py VERBATIM (config comes from ckpt) ──
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
            x = b(x, mask)
        logits = s.head(s.ln_f(x))
        loss = F.cross_entropy(logits.view(-1, 256).float(), targets.view(-1)) if targets is not None else None
        return logits, loss


# ── gen()/gen_novel()/kwr — h1141_7b_pass_attempt.py VERBATIM ──
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


@torch.no_grad()
def gen_novel(m, seed, mx, dev, block, top_k=40, temp=0.85):
    m.eval(); idx = torch.tensor([list(seed.encode("utf-8"))], dtype=torch.long, device=dev); out = []
    stops = ["\n사용자:", " | 사용자:", "사용자:", "\n\n"]
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
        nb = torch.multinomial(F.softmax(logits, -1), 1).item(); out.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=dev)], 1)
        if any(st in bytes(out).decode("utf-8", "ignore") for st in stops): break
    t = bytes(out).decode("utf-8", "ignore")
    for st in stops:
        i = t.find(st)
        if i >= 0: t = t[:i]
    return t.strip()


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


# ── G2-style idea prompts (h1141 VERBATIM) for L1 fresh generations ──
IDEA_PROMPTS = [
    "Silence and the engine together mean ",
    "When memory meets distant minds, ",
    "Consciousness and silence combine into ",
    "The tension between cells and the engine becomes ",
    "If a dream and a distant mind merge, the result is ",
    "Memory and tension together create ",
    "When the engine remembers silence, it ",
    "Distant minds and consciousness form ",
]


# ─────────────────────────────────────────────────────────────────────────────
# G5-L1 LEXICAL — fabricated-word-rate <= 0.30 on fresh generations.
# fabricated-rate = 1 - known-word-ratio (kwr vs /usr/share/dict). seeds {7,8,9}.
# ─────────────────────────────────────────────────────────────────────────────
def gate_g5_l1(m, dev, block, dict_words):
    print("\n##### GATE G5-L1 — LEXICAL (fabricated-word-rate <= 0.30) #####", flush=True)
    rows = []; all_latin = 0; all_fab = 0
    for prompt in IDEA_PROMPTS:
        for sd_i in (7, 8, 9):
            torch.manual_seed(sd_i)
            o = gen_novel(m, prompt, 110, dev, block, top_k=40, temp=0.85)
            latin = _re.findall(r"[A-Za-z]+", o.lower())
            known = sum(1 for w in latin if w in dict_words)
            fab = len(latin) - known
            kwr = (known / len(latin)) if latin else 0.0
            rate = 1.0 - kwr
            all_latin += len(latin); all_fab += fab
            rows.append({"prompt": prompt, "seed": sd_i, "n_words": len(latin),
                         "n_fab": fab, "fab_rate": round(rate, 4), "text": o})
            print(f"  [s{sd_i} fab={rate:.2f} ({fab}/{len(latin)})] {prompt!r} -> {o[:90]!r}", flush=True)
    # pooled fabricated-word-rate over ALL tokens (the frozen aggregate metric)
    pooled = (all_fab / all_latin) if all_latin else 1.0
    per_gen = [r["fab_rate"] for r in rows if r["n_words"] > 0]
    mean_per_gen = statistics.mean(per_gen) if per_gen else 1.0
    g5_l1 = pooled <= 0.30
    print(f"##### G5-L1: pooled fab-rate={pooled:.4f} (mean-per-gen={mean_per_gen:.4f}) "
          f"over {all_latin} tokens -> {'PASS' if g5_l1 else 'FAIL'} (bar <=0.30) #####", flush=True)
    return {"pooled_fab_rate": round(pooled, 4), "mean_per_gen_fab_rate": round(mean_per_gen, 4),
            "n_tokens": all_latin, "n_fab": all_fab, "pass": g5_l1, "rows": rows}


# ─────────────────────────────────────────────────────────────────────────────
# G5-L2 FAITHFULNESS — verbatim-sentence continuation overlap vs random control.
# ─────────────────────────────────────────────────────────────────────────────
_WORD = _re.compile(r"[A-Za-z]+")
_STOP = set("""the a an of to and in is it that this for on with as are was were be been by at from or
not but his her its their they we you i he she them our your when where what which who how all any
some no more most into out up down over under was has have had will would can could a an""".split())

def words_lower(text):
    return [w for w in _WORD.findall(text.lower()) if len(w) >= 3 and w not in _STOP]

def overlap_frac(cont, truth):
    """fraction of TRUE-continuation content words the model continuation reproduced
    (recall of the grounded content; symmetric-ish, bounded [0,1])."""
    tw = words_lower(truth)
    if not tw: return None
    cw = set(words_lower(cont))
    if not cw: return 0.0
    hit = sum(1 for w in set(tw) if w in cw)
    return hit / len(set(tw))


def extract_sentences(corpus_path, en_bytes, n_want, min_words=14, max_words=40, seed=7):
    """Pull verbatim English sentences from the en portion (first en_bytes).
    Deterministic: sort candidates, stride-sample n_want. Closed/factual prose."""
    raw = open(corpus_path, "rb").read(en_bytes)
    text = raw.decode("utf-8", "ignore")
    # split on sentence terminators; keep sentences that look like factual prose
    cands = []
    for para in text.split("\n\n"):
        para = " ".join(para.split())
        for sent in _re.split(r"(?<=[.!?])\s+", para):
            sent = sent.strip()
            wlist = _WORD.findall(sent)
            if not (min_words <= len(wlist) <= max_words):
                continue
            # require mostly ASCII letters (English) + ends with a terminator
            if not sent[-1:] in ".!?":
                continue
            ascii_ratio = sum(c.isascii() for c in sent) / max(1, len(sent))
            if ascii_ratio < 0.97:
                continue
            # avoid lines that are mostly digits/refs
            alpha = sum(c.isalpha() for c in sent)
            if alpha / max(1, len(sent)) < 0.6:
                continue
            cands.append(sent)
    # dedup + deterministic order
    seen = set(); uniq = []
    for s in cands:
        if s in seen: continue
        seen.add(s); uniq.append(s)
    uniq.sort()
    if len(uniq) < n_want:
        return uniq
    stride = len(uniq) / n_want
    return [uniq[int(i * stride)] for i in range(n_want)]


@torch.no_grad()
def gen_from_prompt_grounded(m, prompt, mx, dev, block, top_k=40, temp=0.7, seed_rng=7):
    """Like gen() but stop on sentence terminator OR \\n\\n. Returns continuation only."""
    m.eval()
    g = torch.Generator(device=dev); g.manual_seed(seed_rng)
    idx = torch.tensor([list(prompt.encode("utf-8"))], dtype=torch.long, device=dev); out = []
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
        dec = bytes(out).decode("utf-8", "ignore")
        if "\n\n" in dec: break
    return bytes(out).decode("utf-8", "ignore").strip()


def first_half_split(sentence):
    """Split a sentence into (prompt=first half words, truth=second half words)."""
    w = _WORD.findall(sentence)
    # split on the WORD boundary at the midpoint, preserving the original prefix text
    mid = len(w) // 2
    # find char index where the (mid)-th word ends
    count = 0; idx = 0
    for mobj in _WORD.finditer(sentence):
        count += 1
        if count == mid:
            idx = mobj.end(); break
    prompt = sentence[:idx]
    truth = sentence[idx:].strip()
    return prompt, truth


def gate_g5_l2(m, dev, block, corpus_path, en_bytes, n_sentences=40, seed=7):
    print(f"\n##### GATE G5-L2 — FAITHFULNESS (verbatim-sentence overlap vs random control) #####", flush=True)
    sents = extract_sentences(corpus_path, en_bytes, n_sentences, seed=seed)
    print(f"  extracted {len(sents)} verbatim English factual sentences from en corpus", flush=True)
    true_ov = []; rand_ov = []; rows = []
    truths_pool = []
    # first pass: build prompt/truth + model continuation; collect overlaps
    pairs = []
    for s in sents:
        prompt, truth = first_half_split(s)
        if len(words_lower(truth)) < 3 or len(prompt.strip()) < 8:
            continue
        cont = gen_from_prompt_grounded(m, prompt, 90, dev, block, top_k=40, temp=0.7, seed_rng=seed)
        pairs.append({"prompt": prompt, "truth": truth, "cont": cont})
        truths_pool.append(truth)
    # second pass: true-overlap + random-control (shuffle truths deterministically)
    import random as _rnd
    rng = _rnd.Random(seed)
    perm = list(range(len(pairs)))
    # derangement-ish: rotate by a fixed offset so no truth maps to itself
    off = max(1, len(pairs) // 3)
    for i, p in enumerate(pairs):
        ov_t = overlap_frac(p["cont"], p["truth"])
        rand_truth = truths_pool[(i + off) % len(truths_pool)]
        ov_r = overlap_frac(p["cont"], rand_truth)
        if ov_t is None or ov_r is None:
            continue
        true_ov.append(ov_t); rand_ov.append(ov_r)
        rows.append({"prompt": p["prompt"][:80], "truth": p["truth"][:80], "cont": p["cont"][:80],
                     "overlap_true": round(ov_t, 4), "overlap_random": round(ov_r, 4)})
        print(f"  [t={ov_t:.2f} r={ov_r:.2f}] P:{p['prompt'][:42]!r} -> C:{p['cont'][:42]!r} | TRUE:{p['truth'][:42]!r}", flush=True)
    n = len(true_ov)
    mt = statistics.mean(true_ov) if true_ov else 0.0
    mr = statistics.mean(rand_ov) if rand_ov else 0.0
    # paired Cohen's d on (true - random) per-item
    diffs = [t - r for t, r in zip(true_ov, rand_ov)]
    md = statistics.mean(diffs) if diffs else 0.0
    sd = statistics.pstdev(diffs) if len(diffs) > 1 else 0.0
    d_eff = (md / sd) if sd > 1e-12 else (float("inf") if md > 0 else 0.0)
    g5_l2 = (mt > mr) and (d_eff >= 0.8)
    print(f"\n  N={n}  mean_overlap_true={mt:.4f}  mean_overlap_random(control)={mr:.4f}", flush=True)
    print(f"  mean_diff(true-random)={md:.4f}  paired Cohen's d={d_eff:.4f} (frozen bar: d>=0.8 AND true>random)", flush=True)
    print(f"##### G5-L2: {'PASS' if g5_l2 else 'FAIL'} #####", flush=True)
    return {"n": n, "mean_overlap_true": round(mt, 4), "mean_overlap_random": round(mr, 4),
            "mean_diff": round(md, 4), "cohens_d": (round(d_eff, 4) if math.isfinite(d_eff) else "inf"),
            "pass": g5_l2, "rows": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--en_mb", type=float, default=300.0, help="English portion size = first N MB (= bytes_per_lang)")
    ap.add_argument("--n_sentences", type=int, default=40)
    ap.add_argument("--out", default="/workspace/h1141_g5_result.json")
    a = ap.parse_args()
    dev = "cuda" if torch.cuda.is_available() else "cpu"; torch.manual_seed(7)
    print(f"[dev] {dev} {torch.cuda.get_device_name(0) if dev=='cuda' else ''}", flush=True)
    real_dict = load_real_dict()
    print(f"[dict] {len(real_dict)} real English words", flush=True)

    import hashlib
    h = hashlib.sha256()
    with open(a.ckpt, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    sha = h.hexdigest()
    print(f"[ckpt] {a.ckpt} sha256={sha}", flush=True)

    bk = torch.load(a.ckpt, map_location="cpu", weights_only=False); cfg = bk["config"]
    block = cfg["block"]
    m = ByteGPT(cfg["vocab"], cfg["d"], cfg["n_layer"], cfg["n_head"], cfg["block"]).to(torch.bfloat16)
    m.load_state_dict(bk["model"], strict=False); m = m.to(dev)
    nparam = sum(p.numel() for p in m.parameters())
    print(f"[model] cfg={cfg} val_ce={bk.get('val_ce')} step={bk.get('step')} params={nparam:,}", flush=True)
    del bk

    en_bytes = int(a.en_mb * 1024 * 1024)
    g5_l1 = gate_g5_l1(m, dev, block, real_dict)
    g5_l2 = gate_g5_l2(m, dev, block, a.corpus, en_bytes, n_sentences=a.n_sentences, seed=7)

    g5 = g5_l1["pass"] and g5_l2["pass"]
    print("\n" + "=" * 70, flush=True)
    print("### H_1141 7B — GATE G5 (NO HALLUCINATION) ###", flush=True)
    print(f"  G5-L1 LEXICAL     : {'PASS' if g5_l1['pass'] else 'FAIL'}  (fab-rate {g5_l1['pooled_fab_rate']} <= 0.30)", flush=True)
    print(f"  G5-L2 FAITHFULNESS: {'PASS' if g5_l2['pass'] else 'FAIL'}  (overlap true {g5_l2['mean_overlap_true']} vs random {g5_l2['mean_overlap_random']}, d={g5_l2['cohens_d']})", flush=True)
    print(f"  -> G5 = {'PASS' if g5 else 'FAIL'} (L1 AND L2)", flush=True)
    print("=" * 70, flush=True)

    out = {"hypothesis": "H_1141_G5", "ckpt": a.ckpt, "sha256": sha, "nparam": nparam,
           "config": cfg, "G5_L1": g5_l1, "G5_L2": g5_l2, "G5_pass": g5}
    json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=2)
    print(f"\n[done] wrote {a.out}", flush=True)


if __name__ == "__main__": main()
