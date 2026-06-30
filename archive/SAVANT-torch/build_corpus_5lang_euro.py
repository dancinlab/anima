#!/usr/bin/env python
"""SAVANT torch-cuda lane — 5-language (en·fr·de·es·ru) clean-license corpus builder.

Builds a real multilingual pretrain byte stream for the SAVANT 5-lang 7B
torch-cuda reference rung. Clean-license: wikimedia/wikipedia (CC-BY-SA / ODC-BY
sample) per language, balanced bytes, deduped, UTF-8 flattened to a single
byte stream. This mirrors the OMEGA en/fr/de/es/ru corpus axis (the OMEGA 400MB
gutenberg+wiki probe established this exact language set) but is rebuilt here
under the torch-cuda lane so the artifact + sha are self-contained.

Honest scope (a_scale_honest_scope): corpus SIZE is a parameter (--mb-per-lang).
rung0 uses a small slice (fast validation); the 7B rung scales it up. The card
records the actual built size + sha — no inflated claim.

Languages: en fr de es ru   (European 5-lang SAVANT set, per the task spec)
License: wikimedia/wikipedia text = CC-BY-SA 4.0 (clean, attributable).

USAGE
    python build_corpus_5lang_euro.py --out /workspace/savant/corpus_5lang.txt \
        --mb-per-lang 80 --date 20231101
"""
import argparse, hashlib, os, sys, time

LANGS = ["en", "fr", "de", "es", "ru"]


def fetch_lang(lang, target_bytes, date):
    """Stream wikimedia/wikipedia <date>.<lang> until target_bytes of text."""
    from datasets import load_dataset
    ds = load_dataset("wikimedia/wikipedia", f"{date}.{lang}", split="train",
                      streaming=True)
    buf = []
    got = 0
    seen = set()
    for row in ds:
        t = (row.get("text") or "").strip()
        if not t or len(t) < 200:
            continue
        h = hash(t[:256])
        if h in seen:
            continue
        seen.add(h)
        buf.append(t)
        got += len(t.encode("utf-8", "replace"))
        if got >= target_bytes:
            break
    blob = ("\n\n".join(buf)).encode("utf-8", "replace")
    return blob[:target_bytes]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--mb-per-lang", type=float, default=80.0)
    ap.add_argument("--date", default="20231101")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    target = int(args.mb_per_lang * 1024 * 1024)
    parts = []
    per_lang_sizes = {}
    t0 = time.time()
    for lang in LANGS:
        print(f"[corpus] fetching {lang} target={target} bytes ...", flush=True)
        blob = fetch_lang(lang, target, args.date)
        per_lang_sizes[lang] = len(blob)
        parts.append(blob)
        print(f"[corpus] {lang}: {len(blob)} bytes ({len(blob)/1024/1024:.1f} MB) "
              f"elapsed={time.time()-t0:.0f}s", flush=True)

    data = b"\n\n".join(parts)
    with open(args.out, "wb") as f:
        f.write(data)
    sha = hashlib.sha256(data).hexdigest()
    print(f"=== CORPUS_BYTES={len(data)} ({len(data)/1024/1024:.1f} MB) ===", flush=True)
    print(f"=== CORPUS_SHA256={sha} ===", flush=True)
    print(f"=== PER_LANG={per_lang_sizes} ===", flush=True)
    print(f"=== CORPUS_PATH={args.out} ===", flush=True)
    # persist a tiny card next to the corpus
    card = os.path.join(os.path.dirname(args.out), "corpus_card.txt")
    with open(card, "w") as f:
        f.write(f"languages={','.join(LANGS)}\n")
        f.write(f"source=wikimedia/wikipedia {args.date}\n")
        f.write(f"license=CC-BY-SA-4.0\n")
        f.write(f"bytes={len(data)}\n")
        f.write(f"sha256={sha}\n")
        f.write(f"per_lang={per_lang_sizes}\n")
    print(f"=== CARD={card} ===", flush=True)


if __name__ == "__main__":
    main()
