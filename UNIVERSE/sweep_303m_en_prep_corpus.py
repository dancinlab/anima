#!/usr/bin/env python3
"""sweep_303m_en_prep_corpus.py — ENGLISH-FIRST corpus prep for the 303M-EN recipe sweep.

The 303M-EN sweep (MODEL.md anima-303M-RETRO, ENGLISH-FIRST) needs a clean English-dominant
byte corpus. H_1129's substrate note records its corpus as "ASCII-filtered (>=90% ASCII chars
per line) from the 1.5GB 5-lang wiki -> 295MB diverse English". We reproduce that filter
DETERMINISTICALLY from the 5-lang blend already resident on aiden, so the sweep is fully
self-contained (no network, no HF download).

Input : a UTF-8 byte corpus (the 5-lang wiki+dialogue blend).
Output: <out> = English-dominant lines only (>=THRESH ASCII chars per non-empty line),
        truncated to --max_mb. Deterministic (single linear pass, no randomness).

This is the G0/G1/G2 corpus the sweep's a303m_pass evaluators (kwr / recombination ladder /
novelty, all keyed on English signature words) measure against — script-controlled so the
English concept vocabulary dominates generation (the H_1128/H_1129 lesson: a multilingual
blend pulls generation toward the dominant script and zeroes the English-keyed metric).

Usage: sweep_303m_en_prep_corpus.py <src> <out> [--max_mb 120] [--thresh 0.90]
"""
import argparse, hashlib, os, sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--max_mb", type=float, default=120.0)
    ap.add_argument("--thresh", type=float, default=0.90)
    a = ap.parse_args()

    cap = int(a.max_mb * 1024 * 1024)
    written = 0
    kept_lines = 0
    total_lines = 0
    h = hashlib.sha256()
    with open(a.src, "rb") as fin, open(a.out, "wb") as fout:
        for raw in fin:
            total_lines += 1
            try:
                s = raw.decode("utf-8")
            except UnicodeDecodeError:
                s = raw.decode("utf-8", "ignore")
            t = s.strip()
            if not t:
                continue
            ascii_n = sum(1 for c in s if ord(c) < 128)
            if ascii_n < a.thresh * len(s):
                continue
            fout.write(raw)
            h.update(raw)
            written += len(raw)
            kept_lines += 1
            if written >= cap:
                break
    sha = h.hexdigest()
    card = {
        "out": a.out, "src": a.src, "bytes": written, "kept_lines": kept_lines,
        "scanned_lines": total_lines, "thresh_ascii": a.thresh, "sha256": sha,
        "note": "English-dominant ASCII-filter of the 5-lang blend (H_1129 corpus recipe)",
    }
    import json
    with open(a.out + ".card.json", "w") as f:
        json.dump(card, f, indent=2)
    print(f"[prep] {a.out} bytes={written/1e6:.1f}MB kept_lines={kept_lines} "
          f"scanned={total_lines} sha256={sha}", flush=True)


if __name__ == "__main__":
    main()
