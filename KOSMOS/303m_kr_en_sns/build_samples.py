#!/usr/bin/env python3
# build_samples.py — curated, balanced, PII-clean anchor-sample builder for the
# 303M KOSMOS set (3 register components: 🇰🇷 Korean · 🇬🇧 English · 📱 SNS).
#
# This is a $0 CPU data-assembly script (no GPU, no model). It curates a
# SAMPLE-SCALE grounding/carving anchor set from material anima already has —
# NOT the full webscale corpus (a_scale_honest_scope). byte V256, byte-level.
#
# Sources:
#   ko  : serving/corpus/anima_7b_webscale.ko.head.txt  (FineWeb-2 ko head, ODC-BY)
#   en  : serving/corpus/anima_7b_webscale.en.head.txt  (FineWeb en head, ODC-BY)
#   sns : serving/corpus/persona_sns_corpus.sample.txt  (anima authored persona×SNS register, generated)
#         + serving/persona_instagram_samples.md         (authored persona×Instagram DM samples)
#
# PII: strip emails/phones -> [EMAIL]/[PHONE] (matches the corpus-card convention;
#      the ko/en heads already use [EMAIL]). Determinism: fixed slicing, no RNG.

import hashlib
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / "samples"
OUT.mkdir(parents=True, exist_ok=True)

# Per-component byte budget for a curated grounding ANCHOR set (sample-scale,
# not webscale). Hundreds-thousands of anchor lines per component.
TARGET_BYTES = 120 * 1024  # ~120 KiB per text component (curated sample, balanced)

EMAIL_RE = re.compile(rb"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(rb"(?<!\d)(?:\+?\d[\d\-\s().]{8,}\d)(?!\d)")


def pii_clean(b: bytes) -> bytes:
    b = EMAIL_RE.sub(b"[EMAIL]", b)

    def _ph(m):
        s = m.group(0)
        if any(c in s for c in b"-() ") and sum(c in b"0123456789" for c in s) >= 9:
            return b"[PHONE]"
        return s

    b = PHONE_RE.sub(_ph, b)
    return b


def take_lines(raw: bytes, budget: int) -> bytes:
    out, seen, total = [], set(), 0
    for line in raw.split(b"\n"):
        line = line.rstrip(b"\r")
        if not line.strip():
            continue
        key = line[:80]
        if key in seen:
            continue
        seen.add(key)
        if total + len(line) + 1 > budget:
            break
        out.append(line)
        total += len(line) + 1
    return b"\n".join(out) + b"\n"


def build_text_component(src: Path, budget: int) -> bytes:
    return take_lines(pii_clean(src.read_bytes()), budget)


def build_sns_component(budget: int) -> bytes:
    """SNS register = anima authored persona×SNS dialogue. Two sources:
    (1) the generated persona_sns_corpus sample (turn-per-line: '<speaker>: ...')
    (2) the instagram-DM samples md (blockquoted '> <speaker>: ...' turns).
    Keep persona-voice register turns; drop markdown scaffolding."""
    lines = []
    # (1) generated SNS corpus sample — already turn-per-line
    gen = pii_clean((REPO / "serving/corpus/persona_sns_corpus.sample.txt").read_bytes())
    for line in gen.split(b"\n"):
        s = line.strip()
        if s and b":" in s:
            lines.append(s)
    # (2) instagram DM samples md — blockquoted turns
    ig = pii_clean((REPO / "serving/persona_instagram_samples.md").read_bytes())
    for line in ig.split(b"\n"):
        s = line.strip()
        if s.startswith(b">") and b":" in s:
            body = s[1:].strip()
            if body and not body.startswith(b"**") and not body.startswith(b"`"):
                lines.append(body)
    return take_lines(b"\n".join(lines), budget)


def manifest(path: Path):
    b = path.read_bytes()
    return {"bytes": len(b), "lines": b.count(b"\n"), "sha256": hashlib.sha256(b).hexdigest()}


def main():
    comps = {
        "ko": build_text_component(REPO / "serving/corpus/anima_7b_webscale.ko.head.txt", TARGET_BYTES),
        "en": build_text_component(REPO / "serving/corpus/anima_7b_webscale.en.head.txt", TARGET_BYTES),
        "sns": build_sns_component(TARGET_BYTES),
    }
    report = {}
    for name, data in comps.items():
        p = OUT / f"{name}.sample.txt"
        p.write_bytes(data)
        report[name] = manifest(p)
    for name in ("ko", "en", "sns"):
        m = report[name]
        print(f"{name}\tbytes={m['bytes']}\tlines={m['lines']}\tsha256={m['sha256']}")
    blob = b"".join(comps.values())
    assert not EMAIL_RE.search(blob), "RAW EMAIL LEAK"
    print("PII_CLEAN=ok")


if __name__ == "__main__":
    main()
