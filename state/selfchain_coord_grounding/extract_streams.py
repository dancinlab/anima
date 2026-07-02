#!/usr/bin/env python3
# extract_streams.py — deterministic HELD-OUT stream extraction for L2-2 coord grounding.
# 3 experience streams (ko-general · en-general · ko-sns), 40 texts each (32 chain + 8 held-out
# for G3'), <=256 bytes each. HELD-OUT = a deterministic slice from a fixed offset DEEP into the
# corpus (line 200000+) so it is NOT the front the mouth was warm-FT'd on; NO RNG (frozen).
# Reads the HF-cached .txt (already pulled). numpy/torch 0 (pure text I/O).
import os, sys

SNAP = {
  "ko_general": "datasets--dancinlab--anima-corpus-ko-general/snapshots/9f03495689d52fb50b5b7d8d673d77e38266afcc/anima-corpus-ko-general.txt",
  "en_general": "datasets--dancinlab--anima-corpus-en-general/snapshots/e1c4ef4f595d72b959d0aa73a5cc5c8ba2a065a0/anima-corpus-en-general.txt",
  "ko_sns":     "datasets--dancinlab--anima-corpus-ko-sns/snapshots/410b0b7bcfb15c78ebd609f3af6cef40aa5a7442/anima-corpus-ko-sns.txt",
}
HUB = os.path.expanduser("~/.cache/huggingface/hub")
OUT = os.path.dirname(os.path.abspath(__file__))
N = 40                 # 32 chain + 8 held-out
MAXB = 256
SKIP_FRAC = 0.70       # frozen held-out offset = deep tail (past the warm-FT front)
MIN_BYTES = 24         # skip near-empty lines (need real content to pool)


def extract(path):
    with open(path, encoding="utf-8") as f:
        total = sum(1 for _ in f)
    skip = int(total * SKIP_FRAC)
    picked = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i < skip:
                continue
            s = line.rstrip("\n")
            b = s.encode("utf-8")
            if len(b) < MIN_BYTES:
                continue
            if len(b) > MAXB:
                # truncate on a UTF-8 char boundary at <=MAXB
                b = b[:MAXB]
                while b:
                    try:
                        s = b.decode("utf-8"); break
                    except UnicodeDecodeError:
                        b = b[:-1]
                else:
                    continue
            else:
                s = b.decode("utf-8")
            picked.append(s)
            if len(picked) >= N:
                break
    return picked


def main():
    for short, rel in SNAP.items():
        p = os.path.join(HUB, rel)
        texts = extract(p)
        assert len(texts) == N, f"{short}: got {len(texts)} < {N}"
        outp = os.path.join(OUT, "streams", f"{short}.txt")
        with open(outp, "w", encoding="utf-8") as w:
            for t in texts:
                w.write(t + "\n")
        blens = [len(t.encode("utf-8")) for t in texts]
        print(f"{short}: {len(texts)} texts, bytes min/mean/max = {min(blens)}/{sum(blens)//len(blens)}/{max(blens)} -> {outp}")


if __name__ == "__main__":
    main()
