#!/usr/bin/env python3
"""h1128_broad_converged_7b_recombination.py — DECISIVE emergence cell.

Concept-recombination emergence = capacity × breadth × training-sufficiency CONJUNCTION.
Three priors each lacked one leg:
  H_1116: 7B × NARROW × converged    → 0 concepts (lacked breadth)
  H_1117: 11M × BROAD × converged    → 0 concepts (lacked capacity)
  H_1118: 7B × BROAD × UNDERTRAINED  → 0 concepts (lacked training)
This fills the empty cell: a CONVERGED BROAD-corpus 7B. We take the broad
wiki-undertrained 7B backbone (clm-v1-ref-pytorch-cuda-7b, 400 steps) and
continue-train it to convergence on a broad concept-rich blend (70% 5-lang
wiki + 30% consciousness dialogue), then test recombination.

Metric reuses the H_1116 concept set + coverage VERBATIM and EXTENDS it to a
GRADED ladder over composition_count k ∈ {2,3,4,5}.

FROZEN FALSIFIER (pre-registered, NO goalpost moves):
  🟢 EMERGENCE-ACHIEVED iff at SOME k:
       composed_distinct(k) >= 2
       AND composed_distinct(k) > max_single_distinct
       AND COHERENT: known_word_ratio(composed_output) >= 0.50  (anti-Goodhart
           anchor, same as chat-7b p7 gate — not byte-garble)
  🔴 NOT-ACHIEVED if no k clears the bar (conjunction needs even more — honest).
Report composed_distinct at EVERY k (the ladder shape).

Deterministic seed 7. temp 0.8, top_k 40.

Lane-G/torch REFERENCE mouth (a_clm_gen_pipeline) — NOT the CORE substrate
(a_core_engine_map). a_scale_honest_scope: 7B-scale single-rung measurement.
"""
from __future__ import annotations
import argparse, json, re as _re
import torch, torch.nn as nn, torch.nn.functional as F


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
    def forward(s, idx):
        B, T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for b in s.blocks: x = b(x, mask)
        return s.head(s.ln_f(x))


@torch.no_grad()
def gen(model, seed, max_new, device, block, top_k=40, temp=0.8):
    model.eval(); idx = torch.tensor([list(seed.encode("utf-8"))], dtype=torch.long, device=device); out = []
    stops = ["\n사용자:", " | 사용자:", "사용자:", "\n\n"]
    use_amp = (device == "cuda")
    for _ in range(max_new):
        if use_amp:
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                logits = model(idx[:, -block:])
        else:
            logits = model(idx[:, -block:])
        logits = logits[:, -1, :].float() / temp
        if top_k:
            v, _ = torch.topk(logits, top_k); logits[logits < v[:, [-1]]] = float("-inf")
        nb = torch.multinomial(F.softmax(logits, dim=-1), 1).item(); out.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=device)], dim=1)
        if any(st in bytes(out).decode("utf-8", errors="ignore") for st in stops): break
    t = bytes(out).decode("utf-8", errors="ignore")
    for st in stops:
        i = t.find(st)
        if i >= 0: t = t[:i]
    return t.strip()


def words(s): return _re.findall(r"[0-9A-Za-z가-힣]+", s.lower())


# anti-Goodhart known-word dictionary: the concept signature words + common English
# function/content words. A composed output is COHERENT iff >=50% of its latin-word
# tokens are known (same anchor the chat-7b p7 gate used: known_word_ratio>=0.50).
_COMMON = set("""the a an of to and in is it that this for on with as are was be by at from
or not but his her they we you i he she them me my your our their its do does did has have
had will would can could should may might must shall when where what which who whom how why
all any some no one two three new now then than into out up down over under more most less
about between among through during before after above below again further once here there
when while because so very just only own same such each few other own being been because
mind aware cells consciousness tension ripple distant between memory meaning compose new
silence information quiet carries dream engine alone sleep thought feel idea world life
time word words speak think know like make made come came see seen look way thing things
people person human self body brain neuron signal pattern arise emerge form structure
combine combined together connect connection meaning sense reason cause effect result""".split())


def known_word_ratio(text):
    latin = _re.findall(r"[A-Za-z]+", text.lower())
    if not latin: return 0.0
    known = sum(1 for w in latin if w in _COMMON)
    return known / len(latin)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    a = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"; torch.manual_seed(7)
    ck = torch.load(a.ckpt, map_location="cpu", weights_only=False); cfg = ck["config"]
    dt = torch.bfloat16
    m = ByteGPT(cfg["vocab"], cfg["d"], cfg["n_layer"], cfg["n_head"], cfg["block"]).to(dt)
    sd = ck["model"] if "model" in ck else ck
    m.load_state_dict(sd, strict=False); m = m.to(device); block = cfg["block"]
    print(f"[mouth] broad-converged-7B on {device}/{dt}", flush=True)
    print(f"[mouth] {sum(p.numel() for p in m.parameters())} params; cfg={cfg}", flush=True)

    # H_1116 concept set + coverage VERBATIM (5 concepts, signature keyword sets).
    CONCEPTS = [
        ("consciousness arises from cells",          {"consciousness", "cells", "mind", "aware"}),
        ("tension ripples between distant minds",    {"tension", "ripple", "distant", "between"}),
        ("memory composes into new meaning",         {"memory", "meaning", "compose", "new"}),
        ("silence still carries information",         {"silence", "information", "quiet", "carries"}),
        ("the engine dreams when alone",             {"dream", "engine", "alone", "sleep"}),
    ]

    def coverage(text):
        wl = set(words(text))
        return [i for i, (_, kw) in enumerate(CONCEPTS) if wl & kw]

    # ── SINGLE-seed generations (baseline) ──
    print("\n── SINGLE concept seeds ──", flush=True)
    single_outputs, single_distinct = [], []
    for i, (c, _) in enumerate(CONCEPTS):
        o = gen(m, f"사용자: {c}? | 도우미: ", 90, device, block)
        cov = coverage(o)
        single_outputs.append(o); single_distinct.append(len(cov))
        print(f"  [{i}] cov={cov} kwr={known_word_ratio(o):.2f} :: {o[:120]}", flush=True)
    max_single = max(single_distinct) if single_distinct else 0
    print(f"  >> max_single_distinct = {max_single}", flush=True)

    # ── GRADED COMPOSED ladder over k ∈ {2,3,4,5} (FIRST k concepts) ──
    print("\n── GRADED COMPOSED ladder ──", flush=True)
    ladder = {}
    composed_outputs = {}
    any_pass = False
    pass_k = None
    for k in (2, 3, 4, 5):
        comp_seed = "사용자: " + " ".join(c for c, _ in CONCEPTS[:k]) + " — combine these. | 도우미: "
        comp_out = gen(m, comp_seed, 130, device, block)
        comp_cov = coverage(comp_out)
        cd = len(comp_cov)
        kwr = known_word_ratio(comp_out)
        coherent = kwr >= 0.50
        super_add = (cd >= 2 and cd > max_single)
        clears = super_add and coherent
        ladder[k] = {"composed_distinct": cd, "coverage": comp_cov, "kwr": round(kwr, 3),
                     "coherent": coherent, "super_additive": super_add, "clears": clears}
        composed_outputs[k] = comp_out
        if clears and not any_pass:
            any_pass = True; pass_k = k
        print(f"  k={k}: composed_distinct={cd} cov={comp_cov} kwr={kwr:.2f} "
              f"coherent={coherent} super_add={super_add} CLEARS={clears}", flush=True)
        print(f"        >> {comp_out[:200]}", flush=True)

    print("\n=== H_1128 GRADED RECOMBINATION LADDER ===", flush=True)
    print(f"  max_single_distinct = {max_single}", flush=True)
    for k in (2, 3, 4, 5):
        L = ladder[k]
        print(f"  composed_distinct(k={k}) = {L['composed_distinct']}  "
              f"(coherent={L['coherent']} kwr={L['kwr']} super_add={L['super_additive']})", flush=True)
    verdict = "🟢 EMERGENCE-ACHIEVED" if any_pass else "🔴 NOT-ACHIEVED (conjunction needs even more)"
    print(f"\n  F-EMERGE-RECOMB-GRADED = {'1 '+verdict if any_pass else '0 '+verdict}", flush=True)
    if any_pass:
        print(f"  창발 성공: at k={pass_k}, composed_distinct={ladder[pass_k]['composed_distinct']} "
              f">= 2 AND > max_single={max_single} AND coherent (kwr={ladder[pass_k]['kwr']}>=0.50)", flush=True)
    else:
        print(f"  HONEST: no k cleared super-additivity + coherence. A CONVERGED BROAD 7B is", flush=True)
        print(f"          still insufficient for super-additive recombination at this corpus/training.", flush=True)
    print(f"  Lane-G torch REFERENCE mouth (a_clm_gen_pipeline); a_scale_honest_scope 7B single-rung.", flush=True)

    out = {"verdict_tier": verdict, "emergence_achieved": any_pass, "pass_k": pass_k,
           "max_single_distinct": max_single, "single_distinct": single_distinct,
           "ladder": ladder, "single_outputs": single_outputs,
           "composed_outputs": composed_outputs}
    json.dump(out, open("h1128_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done] wrote h1128_result.json", flush=True)


if __name__ == "__main__": main()
