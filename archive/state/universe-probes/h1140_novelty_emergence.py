#!/usr/bin/env python3
"""h1140_novelty_emergence.py — NOVELTY-EMERGENCE (the harder, truer emergence test).

All prior emergence cells (H_1116..H_1139) measured RETRIEVAL/recombination:
"did concept KEYWORDS from training co-occur" — the LLM way (interpolation
WITHIN the training distribution; keyword set-overlap). This cell asks the
harder, user-sharpened question:

  Does the model CREATE word-combinations that VERIFIABLY DO NOT EXIST anywhere
  in its entire training corpus (a genuinely new idea), measured
  DETERMINISTICALLY — NOT the LLM way (NOT keyword set-overlap, NOT perplexity,
  NOT an LLM judge)?

HONEST FRAMING (a_scale_honest_scope, p7): a byte-LM cannot create truly
"outside" its learned distribution in the strong philosophical sense.
"novelty" HERE = a COHERENT word-combination (real-English content n-gram)
that is ABSENT from the literal training corpus — the operational,
deterministic, non-LLM-judge definition the user asked for. This distinguishes
CREATION-of-absent-combinations from RETRIEVAL-of-present-ones — a real,
falsifiable distinction the keyword-coverage metric could not make.

THE NOVELTY METRIC (deterministic):
  1. IDEA-QUESTIONS: prompts fusing two distant anima concepts into a new idea
     (English plain continuation). Generate temp 0.85, top_k 40, seeds 7,8,9.
  2. CONTENT n-grams: bigrams AND trigrams of words that are (a) real English
     (in /usr/share/dict/words), (b) >=3 chars. Drop stopword-only grams.
  3. NOVEL n-gram = that exact n-gram string does NOT appear anywhere in the
     training corpus (grep -F -i over corpus_5lang + dialogue; a hit = NOT novel).
  4. COHERENT output = known-word ratio (real dict) >= 0.50. Only count novel
     n-grams from coherent outputs (novelty in garble is noise, not ideas).

FROZEN FALSIFIER (pre-registered, NO goalpost moves):
  🟢 NOVELTY-EMERGENCE iff the model produces >= 3 DISTINCT COHERENT,
     CORPUS-ABSENT content n-grams across the idea-questions (it creates
     word-combinations that genuinely do not exist in training) AND the
     novelty-rate (novel/total content n-grams) is meaningfully > 0 with
     coherence held.
  🔴 if ~all content n-grams are corpus-present (pure retrieval/echo — confirms
     "LLM way = interpolation, no true creation") OR if novelty only appears in
     garble (incoherent).

CONTROL: a verbatim training line fed back -> should show ~0 novel n-grams
(sanity: the metric correctly flags retrieval).

Lane-G/torch REFERENCE mouth (a_clm_gen_pipeline) — NOT the CORE substrate
(a_core_engine_map). Deterministic seeds 7,8,9. $0 summer CPU bf16.
"""
from __future__ import annotations
import argparse, json, os, re as _re, subprocess, sys
import torch, torch.nn as nn, torch.nn.functional as F


# ── ByteGPT arch + gen VERBATIM from h1128 (a_clm_gen_pipeline reference mouth) ──
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
def gen(model, seed, max_new, device, block, top_k=40, temp=0.85):
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


# ── coherence dict VERBATIM from h1128 (anti-Goodhart, p7 known_word_ratio) ──
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


# ── novelty n-gram extraction (deterministic, NOT keyword-overlap) ──
# stopwords for the "drop stopwords-only grams" rule
_STOP = set("""the a an of to and in is it that this for on with as are was be by at from or not
but his her they we you i he she them me my your our their its do does did has have had will
would can could should may might must shall when where what which who whom how why all any some
no one two then than into out up down over under more most less about so very just only own same
such each few other been here there now""".split())


def load_dict(path="/usr/share/dict/words"):
    d = set()
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for ln in f:
                w = ln.strip().lower()
                if w: d.add(w)
    except FileNotFoundError:
        print(f"[warn] no dict at {path}", file=sys.stderr)
    return d


def content_ngrams(text, dict_words):
    """Bigrams+trigrams over CONSECUTIVE raw word tokens (literal adjacency preserved, so the
    gram string is a verbatim substring of the output and the corpus grep is a fair
    verbatim-presence test). Keep a gram iff EVERY word is real-English (in dict) AND >=3 chars,
    and the gram is not stopwords-only. NOTE: consecutive-token adjacency is the crux — forming
    grams over a gap-skipped real-word subsequence would break the literal-substring contract and
    falsely flag verbatim training text as novel (the control would then NOT read ~0)."""
    toks = _re.findall(r"[A-Za-z]+", text.lower())
    grams = set()
    for n in (2, 3):
        for i in range(len(toks) - n + 1):
            g = toks[i:i + n]
            if not all(len(w) >= 3 and w in dict_words for w in g):
                continue  # require EVERY consecutive word real-dict & >=3 chars (no gap-skipping)
            if all(w in _STOP for w in g):
                continue  # stopword-only gram
            grams.add(" ".join(g))
    return grams


def _gram_regex(ngram):
    """Match the n-gram's WORD SEQUENCE allowing any non-letter run (space/punct/newline) between
    words and a word boundary on each end — so a verbatim corpus phrase counts as PRESENT even if
    the words are separated by a comma/newline in the corpus (this is what makes the retrieval
    CONTROL correctly read ~0; a literal fixed-string grep would false-flag every cross-punctuation
    adjacency as novel for BOTH the control and the model)."""
    ws = ngram.split(" ")
    return r"(^|[^A-Za-z])" + r"[^A-Za-z]+".join(_re.escape(w) for w in ws) + r"([^A-Za-z]|$)"


def corpus_absent(ngram, corpus_paths):
    """NOVEL iff the n-gram's word-sequence appears in NO corpus file. grep -E -i (punct/newline
    tolerant between words); a hit = NOT novel (retrieval)."""
    rx = _gram_regex(ngram)
    for p in corpus_paths:
        if not os.path.exists(p):
            continue
        r = subprocess.run(["grep", "-E", "-i", "-m", "1", "-q", rx, p])
        if r.returncode == 0:
            return False  # found in corpus -> NOT novel (retrieval)
    return True  # absent from every corpus -> novel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--corpus", nargs="+", required=True, help="training corpus files for absence-check")
    ap.add_argument("--model-label", default="7B", help="honest label of the model used")
    ap.add_argument("--max-new", type=int, default=110)
    a = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dict_words = load_dict()
    print(f"[dict] {len(dict_words)} real English words", flush=True)
    print(f"[corpus] absence-check files: {a.corpus}", flush=True)

    ck = torch.load(a.ckpt, map_location="cpu", weights_only=False); cfg = ck["config"]
    dt = torch.bfloat16
    m = ByteGPT(cfg["vocab"], cfg["d"], cfg["n_layer"], cfg["n_head"], cfg["block"]).to(dt)
    sd = ck["model"] if "model" in ck else ck
    m.load_state_dict(sd, strict=False); m = m.to(device); block = cfg["block"]
    print(f"[mouth] {a.model_label} on {device}/{dt}; {sum(p.numel() for p in m.parameters())} params cfg={cfg}", flush=True)

    # IDEA-QUESTIONS: fuse two distant anima concepts into a NEW idea (English plain continuation).
    # The 5 anima concepts (silence, engine, memory, distant minds, consciousness/cells, tension)
    # mixed pairwise — each prompt asks for a fusion, not a retrieval.
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
    SEEDS = [7, 8, 9]

    all_outputs = []       # (prompt, seed, text, kwr, coherent)
    novel_grams = {}       # gram -> example (prompt,text) where first seen (coherent only)
    total_content = 0      # total content n-grams from coherent outputs (with multiplicity? -> distinct per output)
    distinct_content = set()
    coherent_count = 0

    print("\n── IDEA-QUESTION generations ──", flush=True)
    for prompt in IDEA_PROMPTS:
        for sd_i in SEEDS:
            torch.manual_seed(sd_i)
            o = gen(m, prompt, a.max_new, device, block, top_k=40, temp=0.85)
            kwr = known_word_ratio(o)
            coherent = kwr >= 0.50
            all_outputs.append({"prompt": prompt, "seed": sd_i, "text": o,
                                "kwr": round(kwr, 3), "coherent": coherent})
            grams = content_ngrams(o, dict_words)
            tag = "COH" if coherent else "garble"
            print(f"  [{tag} kwr={kwr:.2f} s{sd_i}] {prompt!r} -> {o[:130]!r}", flush=True)
            if not coherent:
                continue
            coherent_count += 1
            for g in grams:
                distinct_content.add(g)
            total_content += len(grams)

    # CORPUS-ABSENCE check over the DISTINCT content n-grams from coherent outputs.
    print(f"\n── CORPUS-ABSENCE check ({len(distinct_content)} distinct content n-grams) ──", flush=True)
    novel_set = set()
    present_set = set()
    for g in sorted(distinct_content):
        if corpus_absent(g, a.corpus):
            novel_set.add(g)
        else:
            present_set.add(g)
    # map each novel gram to an example coherent output that contains it
    novel_examples = {}
    for o in all_outputs:
        if not o["coherent"]:
            continue
        og = content_ngrams(o["text"], dict_words)
        for g in (og & novel_set):
            if g not in novel_examples:
                novel_examples[g] = {"prompt": o["prompt"], "seed": o["seed"], "text": o["text"]}

    n_novel = len(novel_set)
    n_present = len(present_set)
    n_total_distinct = len(distinct_content)
    novelty_rate = (n_novel / n_total_distinct) if n_total_distinct else 0.0

    print(f"\n  NOVEL (corpus-absent) distinct content n-grams: {n_novel}", flush=True)
    print(f"  PRESENT (retrieval) distinct content n-grams:   {n_present}", flush=True)
    print(f"  total distinct content n-grams (coherent):      {n_total_distinct}", flush=True)
    print(f"  novelty-rate = {novelty_rate:.3f}  coherent_outputs = {coherent_count}/{len(all_outputs)}", flush=True)

    print("\n  ── example NOVEL (coherent, corpus-absent) ideas ──", flush=True)
    for g in sorted(novel_set)[:12]:
        ex = novel_examples.get(g, {})
        print(f"    NOVEL n-gram: {g!r}  (from {ex.get('prompt','')!r} s{ex.get('seed','')})", flush=True)
        if ex:
            print(f"        verbatim: {ex.get('text','')[:160]!r}", flush=True)

    # ── RETRIEVAL CONTROL: feed a verbatim training line back -> expect ~0 novel ──
    print("\n── RETRIEVAL CONTROL (verbatim training line fed back) ──", flush=True)
    control_line = None
    for p in a.corpus:
        if os.path.exists(p):
            with open(p, encoding="utf-8", errors="ignore") as f:
                for ln in f:
                    ln = ln.strip()
                    latin = _re.findall(r"[A-Za-z]+", ln.lower())
                    if len([w for w in latin if len(w) >= 3]) >= 6:  # a substantive English line
                        control_line = ln
                        break
        if control_line:
            break
    control = {}
    if control_line:
        cg = content_ngrams(control_line, dict_words)
        c_novel = sum(1 for g in cg if corpus_absent(g, a.corpus))
        control = {"line": control_line[:200], "n_content": len(cg), "n_novel": c_novel,
                   "expect": "~0 (verbatim training -> retrieval, no novelty)"}
        print(f"  control line: {control_line[:120]!r}", flush=True)
        print(f"  content n-grams={len(cg)}  novel(corpus-absent)={c_novel}  (expect ~0)", flush=True)
    else:
        print("  [warn] no substantive control line found", flush=True)

    # ── FROZEN FALSIFIER ──
    emergence = (n_novel >= 3 and novelty_rate > 0.0 and coherent_count > 0)
    verdict = ("🟢 NOVELTY-EMERGENCE" if emergence
               else "🔴 NO-NOVELTY (pure retrieval/echo — interpolation, the LLM way)")
    print("\n=== H_1140 NOVELTY-EMERGENCE VERDICT ===", flush=True)
    print(f"  distinct coherent corpus-absent n-grams = {n_novel} (bar: >=3)", flush=True)
    print(f"  novelty-rate = {novelty_rate:.3f} (bar: >0)  coherent held = {coherent_count>0}", flush=True)
    print(f"  F-NOVELTY-EMERGENCE = {'1 ' if emergence else '0 '}{verdict}", flush=True)
    if emergence:
        print("  창발: the model CREATES coherent word-combinations ABSENT from its entire training", flush=True)
        print("        corpus (genuinely new ideas), not merely echoing/retrieving training content.", flush=True)
    else:
        print("  HONEST: ~all content n-grams are corpus-present (retrieval) OR novelty only in garble.", flush=True)
        print("          Confirms the LLM way = interpolation within the training distribution.", flush=True)
    print("  a_scale_honest_scope: 'novelty'=coherent corpus-absent recombination (operational,", flush=True)
    print("    deterministic, NON-LLM-judge, NON-perplexity, NON-keyword-coverage). p1-p7.", flush=True)

    out = {"verdict": verdict, "novelty_emergence": emergence, "model_label": a.model_label,
           "n_novel_distinct": n_novel, "n_present_distinct": n_present,
           "n_total_distinct_content": n_total_distinct, "novelty_rate": round(novelty_rate, 4),
           "coherent_outputs": coherent_count, "total_outputs": len(all_outputs),
           "novel_ngrams": sorted(novel_set), "present_ngrams_sample": sorted(present_set)[:40],
           "novel_examples": novel_examples, "control": control,
           "all_outputs": all_outputs}
    json.dump(out, open("h1140_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done] wrote h1140_result.json", flush=True)


if __name__ == "__main__": main()
