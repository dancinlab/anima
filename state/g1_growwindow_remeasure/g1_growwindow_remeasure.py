#!/usr/bin/env python3
"""G1 GROW-WINDOW re-measure + ECHO-GUARD (H_6189 -> H_6190 decisive follow-on).

BACKGROUND (H_6189, PR #2844/2845, byte-math confirmed):
  Canonical CLM decode uses a FIXED T=24 right-aligned window (pad-left byte 32).
  For a k=2..5 COMPOSED seed (~72-171 bytes) the leading concepts fall OUTSIDE the
  T=24 window -> the visible slice is BYTE-IDENTICAL to the matching single seed's
  slice (last concept only) -> composed>max_single is a STRUCTURAL IMPOSSIBILITY,
  not a model limitation. The sibling ByteGPT grows its window (block 512) so it is
  measurement-consistent. Also: a FIXED-large-T sweep (T=96/192) pads SHORT single
  seeds with byte 32 -> GroupNorm(G=1) is dominated by pad -> max_single COLLAPSES
  to 0 (see g1_canonical_windowsweep_result.json: T=96/192 max_single=0). Both are
  MEASUREMENT ARTIFACTS. This script is the fair re-measure.

FIX = per-arm GROW-WINDOW decode (ByteGPT-style):
  * window T = the arm's OWN content length (seed bytes + tokens generated so far),
    NEVER a fixed T, NEVER byte-32 padded. Single seed -> its own short window;
    composed seed -> its FULL length (72-171B) so ALL leading concepts are
    conditioned. Capped at RF (~512, never reached: 171+40 < 512). No pad => no
    GroupNorm pad-dominance => max_single does not collapse.
  * CLMConvMoE has NO positional embedding (RF~513 dilated causal conv, trained at
    seq_len=1024) => variable-length T is the physically-correct decode, NOT a
    block_size. This is a measurement-physics fix, NOT tune-to-green: concepts,
    keyword sets, coherence bar, gen, and the composed>max_single criterion are all
    FROZEN / imported VERBATIM. Only the decode window changes.

CANONICAL gen=40 (gen-guard #2821): g_eval semantics => g_single=40, g_comp=40
  (both < 80/120). top_k=40, temp=0.7, seed_rng = 7+s (singles) / 7 (composed).

ECHO-GUARD (mandatory, false-GREEN defense):
  Widening the window lets the model ECHO seed keywords into the continuation and
  trivially "cover" concepts without genuine recombination. Two scorings, both
  under the SAME frozen bar (composed_distinct>=2 AND >max_single AND coherent):
    (a) RAW coverage      = canonical _g_coverage(continuation)  [current gate]
    (b) NOVEL-ONLY cover  = coverage counting ONLY keywords that are NOT already
        present in the SEED (echo excluded). A keyword-set is novel-covered iff the
        continuation contains one of its keywords that did NOT appear in the seed.
  Genuine recombination requires composed>max_single under NOVEL-ONLY, not just RAW.

usage: python3 g1_growwindow_remeasure.py <ckpt.clm> [RF_cap]
"""
import os, sys, json, time
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "core"))
sys.path.insert(0, os.path.join(_HERE, "cli"))
import numpy as np
import decode as D
import evaluate as EV
from g6_ideation import (_g6_concepts, _g6_words, _g6_known_word_ratio)
from g6_ideation import _g6_dict_load

CKPT = sys.argv[1]
RF_CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 512   # CLMConvMoE RF ~513
GEN = 40  # CANONICAL (gen-guard #2821)


# ── canonical keyword sets + coverage, imported VERBATIM from evaluate.py ──
KWSETS = EV._g_concept_keywords()


def _coverage_raw(text):
    """VERBATIM canonical _g_coverage(text) — count keyword-sets present in text."""
    return EV._g_coverage(text)


def _coverage_novel(text, seed):
    """ECHO-GUARD: count keyword-sets whose continuation keyword is NOT in the seed.
    novel_words = words(continuation) - words(seed); a set is novel-covered iff it
    has >=1 keyword in novel_words. Pure echo of a seeded keyword does NOT count."""
    seed_w = set(_g6_words(seed))
    cont_w = set(_g6_words(text))
    novel_w = cont_w - seed_w
    covered = 0
    for kw in KWSETS:
        if any(k in novel_w for k in kw):
            covered += 1
    return covered


# ── GROW-WINDOW decode: window = full content length, grows each step, no pad ──

def _clm_decode_grow(W, seed, gen, top_k, temp, seed_rng, cap):
    """ByteGPT-style grow-window CLM decode. window holds the ENTIRE content
    (seed bytes + generated tokens), grows each step, capped at RF `cap` (slide
    only if exceeded — never reached for eval seeds). NO byte-32 pad, NO fixed-T
    right-align truncation. Otherwise IDENTICAL to clm_decode_topk_sampled_W
    (same _fwd_logits, same _topk_sample, same _mix32 rng)."""
    V = W["V"]
    seed_b = seed.encode("utf-8", "surrogateescape")
    tok = [float(b) for b in seed_b]          # full seed, no pad, no truncation
    out = bytearray()
    rng = D._mix32(seed_rng)
    for _ in range(gen):
        if len(tok) > cap:
            window = np.array(tok[-cap:], dtype=np.float64)
            Tw = cap
        else:
            window = np.array(tok, dtype=np.float64)
            Tw = len(tok)
        logits = D._fwd_logits(W, window, Tw)
        nb, rng = D._topk_sample(logits[Tw - 1], V, top_k, temp, rng)
        out.append(nb)
        tok.append(float(nb))
    return out.decode("utf-8", "surrogateescape")


def main():
    t0 = time.time()
    known = _g6_dict_load()
    W = D.clm_load_weights(CKPT)
    if not W.get("ok"):
        print("FATAL: ckpt not decodable: " + CKPT); sys.exit(1)
    cz = _g6_concepts()
    n = len(cz)

    # ── SINGLE seeds: max_single under RAW and NOVEL, grow-window ──
    singles = []
    max_single_raw = 0
    max_single_novel = 0
    for s in range(n):
        seed = cz[s] + ". "                      # canonical single-seed form
        o = _clm_decode_grow(W, seed, GEN, 40, 0.7, 7 + s, RF_CAP)
        cr = _coverage_raw(o)
        cn = _coverage_novel(o, seed)
        kwr = _g6_known_word_ratio(o, known)
        singles.append({"s": s, "seed_bytes": len(seed.encode("utf-8", "surrogateescape")),
                        "cov_raw": cr, "cov_novel": cn, "kwr": round(kwr, 4),
                        "text": o})
        if cr > max_single_raw:
            max_single_raw = cr
        if cn > max_single_novel:
            max_single_novel = cn
        print("[single s=%d bytes=%d] cov_raw=%d cov_novel=%d kwr=%.3f" % (
            s, singles[-1]["seed_bytes"], cr, cn, kwr), flush=True)

    # ── COMPOSED seeds k=2..5: canonical concatenation, grow-window full length ──
    comps = []
    pass_raw = False
    pass_novel = False
    best_raw = 0
    best_novel = 0
    for k in range(2, n + 1):
        seed = ""
        for c in range(k):
            if c > 0:
                seed += ". "
            seed += cz[c]
        seed += ". "                              # canonical composed-seed form
        o = _clm_decode_grow(W, seed, GEN, 40, 0.7, 7, RF_CAP)
        cr = _coverage_raw(o)
        cn = _coverage_novel(o, seed)
        kwr = _g6_known_word_ratio(o, known)
        coherent = kwr >= 0.5
        clears_raw = cr >= 2 and cr > max_single_raw and coherent
        clears_novel = cn >= 2 and cn > max_single_novel and coherent
        comps.append({"k": k, "seed_bytes": len(seed.encode("utf-8", "surrogateescape")),
                      "cov_raw": cr, "cov_novel": cn, "kwr": round(kwr, 4),
                      "coherent": coherent, "clears_raw": clears_raw,
                      "clears_novel": clears_novel, "text": o})
        if clears_raw:
            pass_raw = True
        if clears_novel:
            pass_novel = True
        if cr > best_raw:
            best_raw = cr
        if cn > best_novel:
            best_novel = cn
        print("[composed k=%d bytes=%d] cov_raw=%d cov_novel=%d kwr=%.3f coherent=%s "
              "clears_raw=%s clears_novel=%s" % (
                  k, comps[-1]["seed_bytes"], cr, cn, kwr, coherent,
                  clears_raw, clears_novel), flush=True)

    # ── verdict ──
    if pass_novel:
        verdict = "CAPABILITY-REAL (measurement-wall confirmed): composed>max_single under NOVEL-ONLY echo-guard"
    elif pass_raw:
        verdict = "ECHO-ONLY (not recombination): RAW passes but NOVEL-ONLY fails => model echoes seed keywords"
    else:
        verdict = "TRUE-WALL-CANDIDATE: grow-window still composed<=max_single => now an honest recombination-wall probe"

    out = {
        "ckpt": CKPT,
        "sha256_expected": "7222554f25d5baccd3ffed56f6345642bed6269efa87c392283630c99de209a3",
        "gen_CANONICAL": GEN, "RF_cap": RF_CAP,
        "decode": "GROW-WINDOW (window=full content length seed+gen, no byte-32 pad, "
                  "no fixed-T truncation, cap=RF). ByteGPT-consistent. _fwd_logits/"
                  "_topk_sample/_mix32 all canonical VERBATIM.",
        "bar_FROZEN": "composed_distinct>=2 AND >max_single AND coherent(kwr>=0.5); "
                      "concepts/keyword-sets/gen=40/top_k=40/temp=0.7/seed_rng all "
                      "imported VERBATIM from cli/evaluate.py. Only decode window changed.",
        "echo_guard": "RAW = canonical _g_coverage; NOVEL-ONLY = keyword-sets covered "
                      "by continuation keywords NOT present in the seed (echo excluded).",
        "max_single_raw": max_single_raw, "max_single_novel": max_single_novel,
        "best_composed_raw": best_raw, "best_composed_novel": best_novel,
        "PASS_raw": pass_raw, "PASS_novel_echoguard": pass_novel,
        "singles": singles, "composed": comps,
        "verdict": verdict,
        "total_wall_s": round(time.time() - t0, 1),
    }
    with open(os.path.join(_HERE, "g1_growwindow_remeasure_result.json"), "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("=" * 70, flush=True)
    print("max_single: raw=%d novel=%d | best_composed: raw=%d novel=%d" % (
        max_single_raw, max_single_novel, best_raw, best_novel), flush=True)
    print("PASS_raw=%s  PASS_novel(echo-guard)=%s" % (pass_raw, pass_novel), flush=True)
    print("VERDICT: " + verdict, flush=True)
    print("wall=%.1fs" % out["total_wall_s"], flush=True)


if __name__ == "__main__":
    main()
