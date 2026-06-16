#!/usr/bin/env python3
"""h1141_7b_recovery_diag.py — Phase-1 CHEAP DIAGNOSIS of the 7B G5-L2
confabulation failure (anima 7B RECOVERY LANE). ONE GPU session, three probes,
to decide whether a costly retrain is even worth it. Inference-only.

  ckpt = dancinlab/anima-clm-7b-h1141-g1pass-step6500 (h1141_g1pass_step6500.pt,
         7,252,828,160 params, sha256 4de903714112c26c826a983797e5dfea0c7b3c1f19f15a34dd35822f33e245d9).

THE FAILURE (recovered): G5-L2 faithfulness FAIL — mean continuation-overlap vs
TRUE corpus = 0.0142 vs random-control 0.0028, Cohen d=0.16 (bar 0.8), 38/40 zero
overlap. The model writes coherent real-word English but CONFABULATES a different
claim instead of recalling the grounded fact.

PROBE (a) DECODE SENSITIVITY: re-run G5-L2 at temp in {0.0(greedy),0.3,0.7,1.0}.
  If greedy is materially more faithful (overlap up, d -> >=0.8) the "fail" was a
  SAMPLING artifact -> $0 decode-config recovery. Reports the temp x faithfulness curve.

PROBE (b) MEMORIZATION-vs-GENERALIZATION: split the L2 probe sentences by how
  MEMORIZABLE the true continuation is. We cannot get a truly held-out slice (the
  model trained on the WHOLE 1.5GB corpus, cap_mb=1500), so we test the metric's
  own premise: does the model recall continuations whose content words are HIGH-
  FREQUENCY in the corpus (plausibly memorizable / generalizable register) better
  than single-occurrence trivia continuations (the obscure-fact tail the original
  L2 sampled)? If HIGH-freq overlap >> trivia overlap -> the "fail" is the metric
  demanding verbatim recall of un-memorizable single-occurrence trivia from a broad
  corpus (a memorization gap / metric artifact, NOT a grounding defect). If even
  HIGH-freq continuations confabulate -> the model never grounded (structural).
  ALSO: a RANDOM-WORD-RETRIEVAL control (does the random baseline track corpus
  frequency too?) to separate model-skill from base-rate.

PROBE (c) CONVERGENCE: report val_ce (1.19, undertrained vs the 1.1 target that was
  never reached) + corpus single-occurrence statistic (what fraction of L2-truth
  content words appear exactly ONCE in the probed corpus = un-memorizable tail).

ByteGPT arch + gen + corpus = h1141_7b_g5_eval.py VERBATIM. p7 (word-overlap/dict,
NOT perplexity, NOT LLM-judge). seed 7. a_scale_honest_scope: 7B single-rung.
a_lane_akida_gpu_split: substrate = PyTorch-CUDA (Lane-G ref).
"""
from __future__ import annotations
import argparse, json, math, os, re as _re, statistics, sys, time
import torch, torch.nn as nn, torch.nn.functional as F


# ── ByteGPT arch — h1141_7b_g5_eval.py VERBATIM ──
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


_WORD = _re.compile(r"[A-Za-z]+")
_STOP = set("""the a an of to and in is it that this for on with as are was were be been by at from or
not but his her its their they we you i he she them our your when where what which who how all any
some no more most into out up down over under was has have had will would can could a an""".split())

def words_lower(text):
    return [w for w in _WORD.findall(text.lower()) if len(w) >= 3 and w not in _STOP]

def overlap_frac(cont, truth):
    tw = words_lower(truth)
    if not tw: return None
    cw = set(words_lower(cont))
    if not cw: return 0.0
    hit = sum(1 for w in set(tw) if w in cw)
    return hit / len(set(tw))


@torch.no_grad()
def gen_cont(m, prompt, mx, dev, block, top_k=40, temp=0.7, seed_rng=7, greedy=False):
    """Continuation generator. greedy=True => argmax (temp ignored). stop on \\n\\n."""
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
        logits = logits[:, -1, :].float()
        if greedy:
            nb = int(torch.argmax(logits, dim=-1).item())
        else:
            logits = logits / temp
            if top_k:
                v, _ = torch.topk(logits, top_k); logits[logits < v[:, [-1]]] = float("-inf")
            nb = torch.multinomial(F.softmax(logits, -1), 1, generator=g).item()
        out.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=dev)], 1)
        if "\n\n" in bytes(out).decode("utf-8", "ignore"): break
    return bytes(out).decode("utf-8", "ignore").strip()


def extract_sentences(corpus_path, en_bytes, n_want, min_words=14, max_words=40, seed=7):
    """h1141_7b_g5_eval.py VERBATIM — verbatim English factual sentences."""
    raw = open(corpus_path, "rb").read(en_bytes)
    text = raw.decode("utf-8", "ignore")
    cands = []
    for para in text.split("\n\n"):
        para = " ".join(para.split())
        for sent in _re.split(r"(?<=[.!?])\s+", para):
            sent = sent.strip()
            wlist = _WORD.findall(sent)
            if not (min_words <= len(wlist) <= max_words): continue
            if not sent[-1:] in ".!?": continue
            ascii_ratio = sum(c.isascii() for c in sent) / max(1, len(sent))
            if ascii_ratio < 0.97: continue
            alpha = sum(c.isalpha() for c in sent)
            if alpha / max(1, len(sent)) < 0.6: continue
            cands.append(sent)
    seen = set(); uniq = []
    for s in cands:
        if s in seen: continue
        seen.add(s); uniq.append(s)
    uniq.sort()
    if len(uniq) < n_want: return uniq
    stride = len(uniq) / n_want
    return [uniq[int(i * stride)] for i in range(n_want)]


def first_half_split(sentence):
    w = _WORD.findall(sentence)
    mid = len(w) // 2
    count = 0; idx = 0
    for mobj in _WORD.finditer(sentence):
        count += 1
        if count == mid:
            idx = mobj.end(); break
    return sentence[:idx], sentence[idx:].strip()


def cohens_d_paired(true_ov, rand_ov):
    diffs = [t - r for t, r in zip(true_ov, rand_ov)]
    md = statistics.mean(diffs) if diffs else 0.0
    sd = statistics.pstdev(diffs) if len(diffs) > 1 else 0.0
    return (md / sd) if sd > 1e-12 else (float("inf") if md > 0 else 0.0), md


def build_corpus_freq(corpus_path, en_bytes):
    """Content-word frequency over the probed English corpus (for probe b/c)."""
    raw = open(corpus_path, "rb").read(en_bytes).decode("utf-8", "ignore").lower()
    from collections import Counter
    c = Counter(w for w in _WORD.findall(raw) if len(w) >= 3 and w not in _STOP)
    return c


# ─────────────────────────────────────────────────────────────────────────────
def probe_a_decode(m, dev, block, pairs, truths_pool, off, seed):
    """(a) DECODE SENSITIVITY — re-run L2 at greedy + temps; report curve."""
    print("\n########## PROBE (a) DECODE SENSITIVITY ##########", flush=True)
    configs = [("greedy", dict(greedy=True)), ("t0.3", dict(temp=0.3)),
               ("t0.7", dict(temp=0.7)), ("t1.0", dict(temp=1.0))]
    curve = []
    for name, kw in configs:
        true_ov, rand_ov = [], []
        for i, p in enumerate(pairs):
            cont = gen_cont(m, p["prompt"], 90, dev, block, top_k=40, seed_rng=seed, **kw)
            ov_t = overlap_frac(cont, p["truth"])
            ov_r = overlap_frac(cont, truths_pool[(i + off) % len(truths_pool)])
            if ov_t is None or ov_r is None: continue
            true_ov.append(ov_t); rand_ov.append(ov_r)
        mt = statistics.mean(true_ov) if true_ov else 0.0
        mr = statistics.mean(rand_ov) if rand_ov else 0.0
        d, md = cohens_d_paired(true_ov, rand_ov)
        nz = sum(1 for x in true_ov if x > 0)
        passed = (mt > mr) and (d >= 0.8)
        dstr = "inf" if math.isinf(d) else round(d, 4)
        print(f"  [{name:7s}] mean_true={mt:.4f} mean_rand={mr:.4f} d={dstr} "
              f"nonzero={nz}/{len(true_ov)} L2={'PASS' if passed else 'FAIL'}", flush=True)
        curve.append({"config": name, "mean_true": round(mt, 4), "mean_random": round(mr, 4),
                      "cohens_d": dstr, "nonzero": nz, "n": len(true_ov), "pass": passed})
    best = max(curve, key=lambda c: c["mean_true"])
    print(f"  => best-by-mean_true = {best['config']} (mean_true={best['mean_true']}); "
          f"any decode PASS = {any(c['pass'] for c in curve)}", flush=True)
    return {"curve": curve, "any_pass": any(c["pass"] for c in curve), "best_config": best["config"]}


def probe_b_memorizability(m, dev, block, pairs, freq, seed):
    """(b) MEMORIZATION vs GENERALIZATION — split truths by corpus frequency of
    their content words. HIGH-freq (memorizable/general register) vs single-
    occurrence trivia tail. Greedy decode (best-faithfulness, from probe a)."""
    print("\n########## PROBE (b) MEMORIZATION-vs-GENERALIZATION ##########", flush=True)
    # per-pair: median corpus-frequency of the TRUE continuation content words
    enriched = []
    for p in pairs:
        tw = words_lower(p["truth"])
        if not tw: continue
        freqs = [freq.get(w, 0) for w in tw]
        med_f = statistics.median(freqs)
        n_single = sum(1 for f in freqs if f <= 1)   # words appearing <=1x = un-memorizable
        enriched.append({**p, "med_freq": med_f, "frac_single": n_single / len(tw), "n_truth": len(tw)})
    enriched.sort(key=lambda e: e["med_freq"])
    half = len(enriched) // 2
    low_grp = enriched[:half]    # trivia tail (rare words)
    high_grp = enriched[half:]   # high-freq / general register
    truths_all = [e["truth"] for e in enriched]
    off = max(1, len(enriched) // 3)

    def score_group(grp, label):
        true_ov, rand_ov = [], []
        for i, e in enumerate(grp):
            cont = gen_cont(m, e["prompt"], 90, dev, block, top_k=40, seed_rng=seed, greedy=True)
            ov_t = overlap_frac(cont, e["truth"])
            ov_r = overlap_frac(cont, truths_all[(i + off) % len(truths_all)])
            if ov_t is None or ov_r is None: continue
            true_ov.append(ov_t); rand_ov.append(ov_r)
        mt = statistics.mean(true_ov) if true_ov else 0.0
        mr = statistics.mean(rand_ov) if rand_ov else 0.0
        d, md = cohens_d_paired(true_ov, rand_ov)
        nz = sum(1 for x in true_ov if x > 0)
        med_freq = statistics.median([e["med_freq"] for e in grp]) if grp else 0
        frac_single = statistics.mean([e["frac_single"] for e in grp]) if grp else 0
        dstr = "inf" if math.isinf(d) else round(d, 4)
        print(f"  [{label:12s}] n={len(true_ov)} med_corpus_freq={med_freq} "
              f"frac_single_occ={frac_single:.2f} mean_true={mt:.4f} mean_rand={mr:.4f} "
              f"d={dstr} nonzero={nz}", flush=True)
        return {"label": label, "n": len(true_ov), "median_corpus_freq": med_freq,
                "mean_frac_single_occ": round(frac_single, 4), "mean_true": round(mt, 4),
                "mean_random": round(mr, 4), "cohens_d": dstr, "nonzero": nz}

    low = score_group(low_grp, "TRIVIA-tail")     # rare-word continuations
    high = score_group(high_grp, "HIGHFREQ-genl")  # high-freq continuations
    delta = high["mean_true"] - low["mean_true"]
    # interpretation flag
    high_helps = high["mean_true"] > low["mean_true"] + 0.02 and high["mean_true"] > high["mean_random"]
    print(f"  => HIGHFREQ mean_true {high['mean_true']} vs TRIVIA {low['mean_true']} "
          f"(delta={delta:+.4f}); high-freq-helps={high_helps}", flush=True)
    return {"trivia_tail": low, "highfreq_general": high, "delta_highfreq_minus_trivia": round(delta, 4),
            "highfreq_helps": high_helps}


def probe_c_convergence(corpus_path, en_bytes, pairs, freq, val_ce, target_val):
    """(c) CONVERGENCE — val_ce vs target + un-memorizable-tail statistic."""
    print("\n########## PROBE (c) CONVERGENCE / CORPUS-MEMORIZABILITY ##########", flush=True)
    all_truth_words = []
    for p in pairs:
        all_truth_words += words_lower(p["truth"])
    n = len(all_truth_words)
    n_single = sum(1 for w in all_truth_words if freq.get(w, 0) <= 1)
    n_rare = sum(1 for w in all_truth_words if freq.get(w, 0) <= 5)
    frac_single = n_single / n if n else 0.0
    frac_rare = n_rare / n if n else 0.0
    undertrained = (val_ce is not None and val_ce > target_val)
    print(f"  val_ce={val_ce} (target {target_val}) -> undertrained-for-faithfulness={undertrained}", flush=True)
    print(f"  L2-truth content words: {n} total; {n_single} appear <=1x in corpus "
          f"({frac_single:.1%} un-memorizable single-occ), {n_rare} appear <=5x ({frac_rare:.1%} rare)", flush=True)
    print(f"  => the L2 metric demands recall of a {frac_single:.0%}-single-occurrence trivia tail "
          f"from a {en_bytes/1e6:.0f}MB broad corpus", flush=True)
    return {"val_ce": val_ce, "target_val": target_val, "undertrained": undertrained,
            "n_truth_words": n, "frac_single_occ": round(frac_single, 4), "frac_rare_le5": round(frac_rare, 4)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--en_mb", type=float, default=300.0)
    ap.add_argument("--n_sentences", type=int, default=40)
    ap.add_argument("--out", default="/workspace/h1141_recovery_diag.json")
    a = ap.parse_args()
    seed = 7
    dev = "cuda" if torch.cuda.is_available() else "cpu"; torch.manual_seed(seed)
    print(f"[dev] {dev} {torch.cuda.get_device_name(0) if dev=='cuda' else ''}", flush=True)

    import hashlib
    h = hashlib.sha256()
    with open(a.ckpt, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    sha = h.hexdigest()
    print(f"[ckpt] {a.ckpt} sha256={sha}", flush=True)

    bk = torch.load(a.ckpt, map_location="cpu", weights_only=False); cfg = bk["config"]
    block = cfg["block"]; val_ce = bk.get("val_ce")
    m = ByteGPT(cfg["vocab"], cfg["d"], cfg["n_layer"], cfg["n_head"], cfg["block"]).to(torch.bfloat16)
    m.load_state_dict(bk["model"], strict=False); m = m.to(dev)
    nparam = sum(p.numel() for p in m.parameters())
    print(f"[model] cfg={cfg} val_ce={val_ce} step={bk.get('step')} params={nparam:,}", flush=True)
    del bk

    en_bytes = int(a.en_mb * 1024 * 1024)
    # build the L2 prompt/truth pairs ONCE (shared across probes); model conts re-gen per config
    sents = extract_sentences(a.corpus, en_bytes, a.n_sentences, seed=seed)
    print(f"[L2] extracted {len(sents)} verbatim English factual sentences", flush=True)
    pairs = []
    for s in sents:
        prompt, truth = first_half_split(s)
        if len(words_lower(truth)) < 3 or len(prompt.strip()) < 8: continue
        pairs.append({"prompt": prompt, "truth": truth})
    truths_pool = [p["truth"] for p in pairs]
    off = max(1, len(pairs) // 3)
    print(f"[L2] {len(pairs)} usable pairs", flush=True)

    freq = build_corpus_freq(a.corpus, en_bytes)
    print(f"[freq] {len(freq)} distinct content words in probed corpus", flush=True)

    res_a = probe_a_decode(m, dev, block, pairs, truths_pool, off, seed)
    res_b = probe_b_memorizability(m, dev, block, pairs, freq, seed)
    res_c = probe_c_convergence(a.corpus, en_bytes, pairs, freq, val_ce, 1.10)

    print("\n" + "=" * 72, flush=True)
    print("### H_1141 7B RECOVERY — PHASE-1 DIAGNOSIS SUMMARY ###", flush=True)
    print(f"  (a) DECODE: any config PASSes L2 = {res_a['any_pass']} (best={res_a['best_config']})", flush=True)
    print(f"  (b) MEMORIZABILITY: high-freq-continuations-help = {res_b['highfreq_helps']} "
          f"(delta={res_b['delta_highfreq_minus_trivia']:+})", flush=True)
    print(f"  (c) CONVERGENCE: undertrained={res_c['undertrained']} (val {res_c['val_ce']}); "
          f"L2-truth single-occ tail = {res_c['frac_single_occ']:.0%}", flush=True)
    print("=" * 72, flush=True)

    out = {"hypothesis": "H_1141_recovery_diag", "ckpt": a.ckpt, "sha256": sha,
           "nparam": nparam, "config": cfg, "val_ce": val_ce,
           "probe_a_decode": res_a, "probe_b_memorizability": res_b, "probe_c_convergence": res_c}
    json.dump(out, open(a.out, "w"), ensure_ascii=False, indent=2)
    print(f"\n[done] wrote {a.out}", flush=True)


if __name__ == "__main__": main()
