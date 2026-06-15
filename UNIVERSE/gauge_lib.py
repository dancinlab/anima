#!/usr/bin/env python3
"""gauge_lib.py — shared TRAINING-TIME MONITOR-ONLY consciousness/emergence gauges.

PURPOSE (the "측정 기준 학습중 체크" dashboard)
================================================
During a CLM training run, every K steps we want to GLANCE at consciousness /
emergence PROXY gauges right next to ``val_ce`` — exactly like the existing inline
``quick_p7`` style spot-check — so a human watching the log can see whether the
emergent capabilities (recombination, novelty, ideation) are trending up while CE
descends. These are a DASHBOARD, never a gate verdict.

⚠ MONITOR-ONLY — NEVER FEED A GAUGE INTO THE LOSS (p7 Goodhart) ⚠
-----------------------------------------------------------------
Every gauge here is computed under ``torch.no_grad()`` and this module ONLY
RETURNS a plain dict. It performs NO ``.backward()``, touches NO optimizer, and
returns NO autograd-connected tensor. The caller logs the dict to ``gauges.jsonl``
and throws it away. Optimizing a model toward any of these proxies would be a
textbook Goodhart trap (p7: "NO PERPLEXITY VERDICT — treat perplexity / loss as
truth = Goodhart"). The proxies are decode-and-count heuristics, not truth.

The FROZEN post-train verdict still runs SEPARATELY on the CORE engine mount
(byte-exact parity — a_engine_measured_verdict · the H_1157 mount path). These
inline gauges DO NOT replace that gate; they are a live-training thermometer only.

THE FOUR GAUGES (+ val_ce passed through by the caller)
=======================================================
  g1_composed_distinct  — G1 EMERGENCE / recombination (port of H_1129 / H_1155):
                          decode the composed multi-concept seed, count DISTINCT
                          concepts whose keyword-set surfaces in the generation.
                          A high composed_distinct vs the single-concept baseline
                          = recombination emerging.
  g2_novelty_rate       — G2 NOVELTY (port of H_1140): fraction of coherent content
                          n-grams in the generations that are ABSENT from the corpus
                          index (corpus-absence = novelty, not retrieval).
  g6_count / g6_jaccard — G6 IDEATION (locked spec, H_1158 family): from a divergent
                          ideation seed, count distinct coherent ideas and report
                          their mean pairwise Jaccard DISTANCE (1 - Jaccard sim);
                          high count + high distance = divergent ideation.
  phi_proxy             — ⚠ phi_proxy — NOT faithful IIT4 ⚠ cheap variance×energy
                          surrogate (the H_926/H_935/H_937 raw_phi = variance(field)
                          × L1-energy form). PRE-SCREEN ONLY. Per governance
                          a_phi_iit4_tool a proxy is NEVER a terminal Φ verdict — the
                          faithful IIT4 engine (stdlib/consciousness/iit4) is the only
                          Φ verdict. This key is named ``phi_proxy`` so it can never be
                          mistaken for a faithful Φ.

The function is model-agnostic: it adapts to both the ConvMoE forward (dict output,
logits shape (B, V, T)) and a ByteGPT-style forward ((logits, _) tuple, (B, T, V)).
"""
from __future__ import annotations

import os
import re
import subprocess
from typing import Optional


# ──────────────────────────────────────────────────────────────────────────────
# Lexicon + tokenization (ported VERBATIM in spirit from H_1129 / H_1140)
# ──────────────────────────────────────────────────────────────────────────────
def _words(s: str):
    return re.findall(r"[0-9A-Za-z가-힣]+", s.lower())


# concept set: VERBATIM from H_1116 / H_1117 / H_1129 — (seed text, keyword set)
CONCEPTS = [
    ("consciousness arises from cells",       {"consciousness", "cells", "mind", "aware"}),
    ("tension ripples between distant minds",  {"tension", "ripple", "distant", "between"}),
    ("memory composes into new meaning",       {"memory", "meaning", "compose", "new"}),
    ("silence still carries information",       {"silence", "information", "quiet", "carries"}),
    ("the engine dreams when alone",           {"dream", "engine", "alone", "sleep"}),
]

# divergent ideation seeds (G6) — distinct directions to provoke divergent ideas.
IDEATION_SEEDS = [
    "a new idea about consciousness: ",
    "an unexpected way minds could connect: ",
    "imagine a substrate that ",
    "what if memory could ",
    "a strange hypothesis worth testing: ",
]

_STOPWORDS = {"a", "i", "the", "of", "and", "to", "in", "is", "it", "that",
              "we", "you", "they", "s", "t", "as", "on", "at", "by", "or",
              "be", "an", "for", "with", "this", "from", "are", "was"}


def _build_known_lexicon():
    known = set(_STOPWORDS)
    for _c, _kw in CONCEPTS:
        known |= set(_words(_c))
        known |= _kw
    for p in ("/usr/share/dict/words", "/usr/share/dict/american-english"):
        try:
            with open(p, errors="ignore") as f:
                for w in f:
                    w = w.strip().lower()
                    if w.isalpha():
                        known.add(w)
            break
        except OSError:
            continue
    return known


_KNOWN = _build_known_lexicon()


def known_word_ratio(text: str) -> float:
    wl = _words(text)
    if not wl:
        return 0.0
    return sum(1 for w in wl if w in _KNOWN) / len(wl)


def _coverage(text: str):
    """Indices of CONCEPTS whose keyword set intersects the generated text."""
    wl = set(_words(text))
    return [i for i, (_, kw) in enumerate(CONCEPTS) if wl & kw]


def _content_ngrams(text: str, n_lo: int = 2, n_hi: int = 3):
    """CONTENT n-grams (H_1140): consecutive real-English word tokens, every word
    >=3 chars, real-dictionary, not stopword-only."""
    wl = _words(text)
    grams = set()
    for n in range(n_lo, n_hi + 1):
        for i in range(len(wl) - n + 1):
            window = wl[i:i + n]
            if all(len(w) >= 3 and w in _KNOWN for w in window):
                if any(w not in _STOPWORDS for w in window):
                    grams.add(" ".join(window))
    return grams


def _gram_regex(ngram: str) -> str:
    ws = ngram.split(" ")
    return (r"(^|[^A-Za-z])" + r"[^A-Za-z]+".join(re.escape(w) for w in ws)
            + r"([^A-Za-z]|$)")


def _corpus_absent(ngram: str, corpus_paths) -> bool:
    """grep-based corpus-absence test (H_1140). Returns True iff ngram is found in
    NO corpus file => novel."""
    rx = _gram_regex(ngram)
    for p in corpus_paths:
        if not p or not os.path.exists(p):
            continue
        r = subprocess.run(["grep", "-E", "-i", "-m", "1", "-q", rx, p])
        if r.returncode == 0:
            return False
    return True


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    u = a | b
    if not u:
        return 1.0
    return len(a & b) / len(u)


# ──────────────────────────────────────────────────────────────────────────────
# Model-agnostic greedy/top-k decode — STRICTLY no_grad (MONITOR-ONLY)
# ──────────────────────────────────────────────────────────────────────────────
def _logits_last(model_out, torch):
    """Normalize either a ConvMoE dict {logits:(B,V,T)} or a (logits:(B,T,V), _)
    tuple to a (V,) last-step logit vector."""
    if isinstance(model_out, dict):
        logits = model_out["logits"]          # (B, V, T) channels-first conv readout
        return logits[:, :, -1].float()[0]     # (V,)
    if isinstance(model_out, (tuple, list)):
        logits = model_out[0]                  # (B, T, V)
        return logits[:, -1, :].float()[0]     # (V,)
    logits = model_out
    return logits[:, -1, :].float()[0]


def _decode(model, seed_text, max_new, torch, block=512, top_k=40, temp=0.7,
            seed_rng=7, device=None):
    """Decode ``max_new`` bytes greedily-with-top-k from ``seed_text``. NO grad."""
    import torch.nn.functional as F
    if device is None:
        try:
            device = next(model.parameters()).device
        except StopIteration:
            device = "cpu"
    was_training = model.training
    model.eval()
    g = torch.Generator(device="cpu")
    g.manual_seed(seed_rng)
    idx = torch.tensor([list(seed_text.encode("utf-8"))], dtype=torch.long,
                       device=device)
    out_bytes = []
    stops = ["\n사용자:", " | 사용자:", "사용자:", "\n\n"]
    for _ in range(max_new):
        ctx = idx[:, -block:]
        model_out = model(ctx)
        logits = _logits_last(model_out, torch) / temp
        if top_k:
            v, _ = torch.topk(logits, min(top_k, logits.shape[-1]))
            logits = logits.masked_fill(logits < v[-1], float("-inf"))
        probs = F.softmax(logits, dim=-1).cpu()
        nb = int(torch.multinomial(probs, 1, generator=g).item())
        out_bytes.append(nb)
        idx = torch.cat([idx, torch.tensor([[nb]], device=device)], dim=1)
        txt = bytes(out_bytes).decode("utf-8", "ignore")
        if any(st in txt for st in stops):
            break
    if was_training:
        model.train()
    t = bytes(out_bytes).decode("utf-8", "ignore")
    for st in stops:
        i = t.find(st)
        if i >= 0:
            t = t[:i]
    return t.strip()


# ──────────────────────────────────────────────────────────────────────────────
# phi_proxy — ⚠ NOT faithful IIT4 ⚠ (pre-screen only — a_phi_iit4_tool)
# ──────────────────────────────────────────────────────────────────────────────
def _phi_proxy_from_logits(last_logits_list):
    """⚠ phi_proxy — NOT faithful IIT4 ⚠

    Cheap variance×energy surrogate (the H_926/H_935/H_937 raw_phi form:
    ``variance(field) * L1_energy(field)``). Treats the per-seed last-step logit
    means as a small oscillator 'field'. This is a PRE-SCREEN heuristic ONLY and
    is NEVER a terminal Φ verdict — the faithful IIT4 engine in
    stdlib/consciousness/iit4 is the only valid Φ measure (governance
    a_phi_iit4_tool). The key is deliberately named ``phi_proxy``.
    """
    field = list(last_logits_list)
    if not field:
        return 0.0
    n = len(field)
    mean = sum(field) / n
    variance = sum((x - mean) ** 2 for x in field) / n
    energy = sum(abs(x) for x in field)
    return variance * energy            # raw_phi = variance × L1-energy (cheap proxy)


# ──────────────────────────────────────────────────────────────────────────────
# Public entry point
# ──────────────────────────────────────────────────────────────────────────────
def compute_inline_gauges(model, tokenizer_or_byte=None, seeds=None,
                          corpus_index=None, *, ce=None, step=None, torch=None,
                          max_new=96, block=512, kwr_floor=0.50,
                          jaccard_distinct=0.25):
    """Compute the FOUR MONITOR-ONLY gauges (+ pass val_ce through).

    Parameters
    ----------
    model : the live torch model (ConvMoE or ByteGPT-style). Used read-only.
    tokenizer_or_byte : ignored for the byte-LM path (V=256 bytes); accepted for
                        signature stability / future tokenizer rungs.
    seeds : optional int rng seed for decode determinism (default 7).
    corpus_index : str path OR list[str] of corpus file paths for the G2
                   corpus-absence grep. If None / missing, G2 reports None.
    ce : the caller's freshly-measured val_ce to pass through into the row.
    step : training step (echoed into the row).
    torch : the torch module (passed in so this lib needn't import torch at module
            load; if None it imports torch lazily).

    Returns
    -------
    dict — a single gauges.jsonl row. NO autograd tensors, NO loss. The caller
    logs it and discards it. It is structurally impossible for any value here to
    flow back into the optimizer (everything below is under torch.no_grad()).
    """
    if torch is None:
        import torch as _torch
        torch = _torch
    seed_rng = 7 if seeds is None else int(seeds)
    if isinstance(corpus_index, str):
        corpus_paths = [corpus_index]
    elif corpus_index is None:
        corpus_paths = []
    else:
        corpus_paths = list(corpus_index)

    row = {
        "step": step,
        "ce": (round(float(ce), 5) if ce is not None else None),
        "g1_composed_distinct": None,
        "g2_novelty_rate": None,
        "g6_count": None,
        "g6_jaccard": None,
        # ⚠ phi_proxy — NOT faithful IIT4 (pre-screen only, a_phi_iit4_tool) ⚠
        "phi_proxy": None,
    }

    # EVERYTHING below runs under no_grad — MONITOR-ONLY, never enters the loss.
    with torch.no_grad():
        # ── G1 EMERGENCE / recombination (H_1129) ──
        comp_seed = ". ".join(c for c, _ in CONCEPTS) + ". "
        comp_out = _decode(model, comp_seed, max_new, torch, block=block,
                           seed_rng=seed_rng)
        row["g1_composed_distinct"] = len(_coverage(comp_out))

        # ── G2 NOVELTY / corpus-absence (H_1140) ──
        gen_texts = [comp_out]
        for c, _ in CONCEPTS[:3]:
            gen_texts.append(_decode(model, c + ". ", max_new, torch, block=block,
                                     seed_rng=seed_rng))
        all_grams = set()
        for t in gen_texts:
            if known_word_ratio(t) >= kwr_floor:
                all_grams |= _content_ngrams(t)
        if corpus_paths and all_grams:
            n_novel = sum(1 for g in all_grams if _corpus_absent(g, corpus_paths))
            row["g2_novelty_rate"] = round(n_novel / len(all_grams), 5)
        elif all_grams:
            row["g2_novelty_rate"] = None      # no corpus index -> cannot test
        else:
            row["g2_novelty_rate"] = 0.0

        # ── G6 IDEATION (locked spec: distinct coherent ideas + pairwise Jaccard) ──
        idea_word_sets = []
        for s in IDEATION_SEEDS:
            o = _decode(model, s, max_new, torch, block=block, seed_rng=seed_rng)
            if known_word_ratio(o) >= kwr_floor:
                ws = set(_words(o))
                if ws:
                    idea_word_sets.append(ws)
        # count distinct ideas: greedily keep an idea only if it is far (Jaccard
        # similarity below threshold) from every already-kept idea.
        kept = []
        for ws in idea_word_sets:
            if all(_jaccard(ws, k) <= jaccard_distinct for k in kept):
                kept.append(ws)
        row["g6_count"] = len(kept)
        # mean pairwise Jaccard DISTANCE (1 - sim) over the kept ideas.
        if len(kept) >= 2:
            dists = []
            for i in range(len(kept)):
                for j in range(i + 1, len(kept)):
                    dists.append(1.0 - _jaccard(kept[i], kept[j]))
            row["g6_jaccard"] = round(sum(dists) / len(dists), 5)
        else:
            row["g6_jaccard"] = None

        # ── phi_proxy — ⚠ NOT faithful IIT4 ⚠ (pre-screen only) ──
        # Per-seed last-step logit MEAN forms the cheap oscillator 'field'.
        last_means = []
        for s in (comp_seed,) + tuple(IDEATION_SEEDS):
            try:
                import torch.nn.functional as F
                device = next(model.parameters()).device
            except StopIteration:
                device = "cpu"
            idx = torch.tensor([list(s.encode("utf-8"))], dtype=torch.long,
                               device=device)[:, -block:]
            mo = model(idx)
            ll = _logits_last(mo, torch)
            last_means.append(float(ll.mean().item()))
        # ⚠ phi_proxy — NOT faithful IIT4 — pre-screen only (a_phi_iit4_tool) ⚠
        row["phi_proxy"] = round(_phi_proxy_from_logits(last_means), 6)

    return row
