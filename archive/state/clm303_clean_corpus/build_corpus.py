#!/usr/bin/env python3
"""build_corpus.py — reproducible builder for the anima clean 4-cell register
corpus ({ko·en}x{general·SNS}, a_chat_registers). Single SSOT for HOW the
datasets were made (anti-"대충 4칸" — every cell is language-verified clean).

Cells (canonical names):
  anima-corpus-ko-general : FineWeb2 ko (HF anima-corpus-ko-fineweb2-broad), capped
  anima-corpus-en-general : FineWeb-en (HF HuggingFaceFW/fineweb), capped + en-verified
  anima-corpus-ko-sns     : persona ko + 5lang-split ko + MIT/apache ko-chat augmentation
  anima-corpus-en-sns      : 5lang-split en-SNS (clean en lines only)

Every line is language-classified (clean_split.classify) so a cell only contains
its target language (de/es/fr/ja/zh dropped, dedup). The prior failure was
5lang-contaminated "en" cells + a single-cell pod stage — this script makes the
composition explicit and verifiable (re-run langaudit.py on the outputs).

Usage:
  python build_corpus.py --out-dir OUT --cap-mb 60 [--ko-sns-aug] [--no-hf]
"""
import argparse
import hashlib
import importlib.util
import os
import sys

# shared torch-free classifier from the sibling clean_split.py
_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "clean_split", os.path.join(_here, "clean_split.py"))
_cs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cs)
classify = _cs.classify


def stream_hf_text(repo, target_lang, cap_bytes, en_min_words=3):
    """Stream an HF dataset's text column, keep only `target_lang` lines, until
    cap_bytes of kept text. Returns a list of clean lines (deduped)."""
    from datasets import load_dataset
    ds = load_dataset(repo, split="train", streaming=True)
    seen, kept, nbytes = set(), [], 0
    text_col = None
    for row in ds:
        if text_col is None:
            for c in ("text", "content", "body", "caption"):
                if c in row:
                    text_col = c
                    break
            if text_col is None:
                text_col = next(iter(row))
        for line in str(row[text_col]).split("\n"):
            s = line.strip()
            if len(s) < 4:
                continue
            if classify(s, en_min_words) != target_lang:
                continue
            h = hash(s)
            if h in seen:
                continue
            seen.add(h)
            kept.append(s)
            nbytes += len(s.encode()) + 1
        if nbytes >= cap_bytes:
            break
    return kept


def range_read_hf_txt(repo, filename, target_lang, cap_bytes, raw_cap_bytes,
                      en_min_words=3):
    """Range-read the first raw_cap_bytes of a raw .txt file in an HF dataset
    (for repos that store one big .txt, not a parquet/text-column dataset that
    load_dataset can stream), keep only target_lang lines until cap_bytes."""
    import urllib.request
    from huggingface_hub import hf_hub_url
    url = hf_hub_url(repo, filename, repo_type="dataset")
    req = urllib.request.Request(url, headers={"Range": f"bytes=0-{raw_cap_bytes}"})
    blob = urllib.request.urlopen(req, timeout=180).read()
    seen, kept, nbytes = set(), [], 0
    for line in blob.decode("utf-8", "replace").split("\n"):
        s = line.strip()
        if len(s) < 4:
            continue
        if classify(s, en_min_words) != target_lang:
            continue
        h = hash(s)
        if h in seen:
            continue
        seen.add(h)
        kept.append(s)
        nbytes += len(s.encode()) + 1
        if nbytes >= cap_bytes:
            break
    return kept


def split_local(paths, target_lang, en_min_words=3, cap_bytes=0):
    """Keep only target_lang lines from local files (deduped); optional cap."""
    seen, kept, nbytes = set(), [], 0
    for p in paths:
        if not os.path.exists(p):
            print(f"  WARN local source missing: {p}")
            continue
        for raw in open(p, "rb"):
            s = raw.decode("utf-8", "replace").strip()
            if len(s) < 4:
                continue
            if classify(s, en_min_words) != target_lang:
                continue
            h = hash(s)
            if h in seen:
                continue
            seen.add(h)
            kept.append(s)
            nbytes += len(raw)
            if cap_bytes and nbytes >= cap_bytes:
                return kept
    return kept


def write_cell(lines, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + ("\n" if lines else ""))
    return os.path.getsize(path)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--cap-mb", type=float, default=60.0,
                    help="per-general-cell cap in MB (SNS cells use all clean lines)")
    ap.add_argument("--trainset", default="",
                    help="local trainset dir with the 5lang/persona source files")
    ap.add_argument("--ko-sns-aug", action="store_true",
                    help="also pull MIT/apache ko-chat HF datasets into ko-sns")
    ap.add_argument("--no-hf", action="store_true",
                    help="skip HF streaming (local-only smoke build)")
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    cap = int(a.cap_mb * 1e6)
    TS = a.trainset
    out = {}

    # general cells (HF webscale, capped + language-verified)
    if not a.no_hf:
        print("ko-general <- HF anima-corpus-ko-fineweb2-broad raw .txt (range-read, ko-verified)")
        # this repo stores ONE big .txt (not a parquet text-column dataset), so
        # range-read a raw prefix (~3x cap to survive non-ko/dup drops) and keep ko.
        out["anima-corpus-ko-general"] = range_read_hf_txt(
            "dancinlab/anima-corpus-ko-fineweb2-broad", "ko_fineweb2_broad.txt",
            "ko", cap, raw_cap_bytes=int(cap * 3))
        print("en-general <- HF HuggingFaceFW/fineweb (cap, en-verified)")
        out["anima-corpus-en-general"] = stream_hf_text(
            "HuggingFaceFW/fineweb", "en", cap)

    # ko-sns — persona ko + 5lang-split ko (+ optional MIT/apache aug)
    print("ko-sns <- persona ko + 5lang-split ko" + (" + HF aug" if a.ko_sns_aug else ""))
    ko_sns_src = [os.path.join(TS, f) for f in
                  ("persona_sns_corpus.txt", "persona_sns_corpus_5lang_v2.txt")] if TS else []
    ko_sns = split_local(ko_sns_src, "ko")
    if a.ko_sns_aug and not a.no_hf:
        for repo in ("NLPBada/korean-persona-chat-dataset",
                     "JaeJiMin/korean_chat_friendly",
                     "jojo0217/korean_safe_conversation"):
            try:
                ko_sns += stream_hf_text(repo, "ko", cap)
            except Exception as e:
                print(f"  WARN ko-sns aug {repo}: {type(e).__name__}")
    out["anima-corpus-ko-sns"] = list(dict.fromkeys(ko_sns))  # dedup, keep order

    # en-sns — 5lang-split en-SNS (clean en only)
    print("en-sns <- 5lang-split en-SNS")
    en_sns_src = [os.path.join(TS, f) for f in
                  ("persona_sns_corpus_5lang_v2.txt",)] if TS else []
    out["anima-corpus-en-sns"] = split_local(en_sns_src, "en")

    # write + manifest
    print("\n-- manifest --")
    man = []
    for name, lines in out.items():
        p = os.path.join(a.out_dir, name + ".txt")
        sz = write_cell(lines, p)
        sh = sha256(p)
        man.append((name, len(lines), sz, sh))
        print(f"  {name:<26s} {len(lines):>8d} lines  {sz/1e6:>7.2f}MB  {sh[:16]}")
    with open(os.path.join(a.out_dir, "MANIFEST.sha256"), "w") as f:
        for name, n, sz, sh in man:
            f.write(f"{sh}  {name}.txt  ({n} lines, {sz} bytes)\n")
    print(f"\nwrote {len(man)} cells + MANIFEST.sha256 to {a.out_dir}")


if __name__ == "__main__":
    main()
