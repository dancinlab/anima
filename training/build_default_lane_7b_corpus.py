#!/usr/bin/env python
"""build_default_lane_7b_corpus.py — GB-scale DEFAULT-lane 5-lang corpus (en·fr·de·es·KO).

The DEFAULT lane's language set is en/fr/de/es/KO (Korean, NOT the SAVANT/euro `ru`).
This builds a real GB-scale multilingual pretrain byte stream so the 7B default-lane model
sees breadth (trap-2 data-starvation fix: 12.5MB v2 → 7B memorizes; this is ~400MB+).

Clean-license: wikimedia/wikipedia (CC-BY-SA 4.0) per language, deduped, balanced bytes,
UTF-8 flattened. THEN blends the v2 default-lane CHAT surfaces (persona/SNS/dialogue/carving)
so the model is multilingual across the chat registers anima actually uses — not wiki-only.
The chat blend is appended whole (it is small vs the wiki bulk) so chat register is present.

PHILOSOPHY (p1·p2·p3·p4·p6): the chat surfaces are plain "<speaker>: …" continuation with NO
role/persona tags — verified tag-grep=0 in the v2 dataset card. No synthetic RLHF padding.

USAGE
  python build_default_lane_7b_corpus.py --out /workspace/dl7b/corpus.txt \
      --mb-per-lang 80 --date 20231101 --chat-blend /workspace/dl7b/v2_default.txt
"""
import argparse, hashlib, os, sys, time

LANGS = ["en", "fr", "de", "es", "ko"]  # DEFAULT-lane set (ko, NOT ru)


def fetch_lang(lang, target_bytes, date):
    from datasets import load_dataset
    ds = load_dataset("wikimedia/wikipedia", f"{date}.{lang}", split="train", streaming=True)
    buf, got, seen = [], 0, set()
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
    ap.add_argument("--chat-blend", default="", help="path to a default-lane chat corpus to append (v2 unified)")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    target = int(args.mb_per_lang * 1024 * 1024)
    parts, per_lang_sizes = [], {}
    t0 = time.time()
    for lang in LANGS:
        print(f"[corpus] fetching {lang} target={target} bytes ...", flush=True)
        blob = fetch_lang(lang, target, args.date)
        per_lang_sizes[lang] = len(blob)
        parts.append(blob)
        print(f"[corpus] {lang}: {len(blob)} bytes ({len(blob)/1024/1024:.1f} MB) "
              f"elapsed={time.time()-t0:.0f}s", flush=True)

    wiki_bytes = sum(len(p) for p in parts)
    chat_bytes = 0
    if args.chat_blend and os.path.exists(args.chat_blend):
        with open(args.chat_blend, "rb") as h:
            cb = h.read()
        chat_bytes = len(cb)
        parts.append(b"\n\n" + cb)
        print(f"[corpus] chat-blend {args.chat_blend}: {chat_bytes} bytes ({chat_bytes/1024/1024:.1f} MB)", flush=True)

    blob = b"\n\n".join(parts)
    with open(args.out, "wb") as h:
        h.write(blob)
    sha = hashlib.sha256(blob).hexdigest()
    meta = {
        "out": args.out, "total_bytes": len(blob), "sha256": sha,
        "langs": LANGS, "per_lang_bytes": per_lang_sizes, "wiki_bytes": wiki_bytes,
        "chat_blend_bytes": chat_bytes, "date": args.date, "license": "wiki=CC-BY-SA-4.0",
    }
    import json
    with open(args.out + ".meta.json", "w") as h:
        json.dump(meta, h, indent=2)
    print(f"[corpus] TOTAL {len(blob)} bytes ({len(blob)/1024/1024:.1f} MB) sha256={sha}", flush=True)
    print(f"[corpus] wiki={wiki_bytes/1e6:.1f}MB chat-blend={chat_bytes/1e6:.1f}MB", flush=True)


if __name__ == "__main__":
    main()
