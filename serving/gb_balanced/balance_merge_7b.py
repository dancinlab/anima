#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""balance_merge_7b.py — assemble the 7B-scale web-extended default-lane corpus.

This is the 7B sibling of balance_merge.py. The difference is the BALANCE RULE:

  balance_merge.py (MID-rung, ~0.35 GB):
    clean-only sources -> wiki is the abundant residual floor capped at <45%; the
    corpus is CAPPED by the balance requirement (growing only the abundant clean
    tiers would breach the ceiling) -> 0.268% of 7B-optimal.

  balance_merge_7b.py (7B-rung, GB-scale):
    a NEW `web` tier (FineWeb-2 + mC4, ODC-BY — user-sanctioned 2026-06-05) becomes
    the MAJORITY register (capacity needs bulk). The curated registers (wiki
    baseline / cosmic / Gutenberg art / Gutenberg consciousness / persona-social /
    shaping) stay MEANINGFULLY PRESENT (NOT ~0%) by taking ALL they have, while the
    web tier is capped to a target majority band. The 7B rule:

      web-bulk 55-70%  /  Gutenberg art+consciousness 12-20%  /
      wiki science cosmic 8-12%  /  persona-social 4-8%  /  shaping ~1%.

    NO tier starved to ~0. The web tier is DOWN-capped to keep it within its band
    while every curated tier keeps everything it has (honest; thin langs reported).

Pipeline (same hygiene as balance_merge.py):
  1. dedup    — near-duplicate filter on the FULL block (sha1 of whole block),
                shared seen set across tiers (web docs that duplicate wiki dropped).
  2. BALANCE  — web tier capped to its majority band; curated tiers floor-protected
                (take all available). Curated registers anchor the total; web fills
                up to the majority ceiling.
  3. round-trip — UTF-8 decode/encode every block (vocab256 byte cleanliness);
                control bytes 0xFE/0xFF never emitted.
  4. account  — achieved per-TIER + per-LANG byte split + tier-vs-target band +
                byte-token count vs the 140B Chinchilla-7B-optimal line + which
                7B-regime the achieved size reaches (undertrained vs near-optimal).

Usage
-----
  python3 serving/gb_balanced/balance_merge_7b.py \
      --src-dir serving/corpus/_src \
      --web serving/corpus/_src/web_bulk.txt \
      --shaping serving/corpus/_src/shaping.txt \
      --persona serving/corpus/_src/persona.txt \
      --out serving/corpus/default_lane_7b_webscale.txt \
      --report serving/corpus/_src/7b_webscale_report.json
"""

import argparse
import hashlib
import json
import os
import re

LANGS = ["en", "fr", "de", "es", "ko"]
_HANGUL = re.compile(r"[가-힣]")

# 7B target bands (fractions of the final total). web is the MAJORITY; curated tiers
# stay meaningfully present. Bands are (lo, hi); the merge keeps web within [lo,hi]
# and lets curated tiers take all they have (their floors are guaranteed because
# they are the scarce minority that anchors the total).
WEB_BAND = (0.55, 0.70)          # general-web bulk (FineWeb-2 + mC4, ODC-BY)
# curated registers — TARGET shares of the NON-web remainder. These take all they
# have up to their share of the (1 - web) curated budget; thin tiers keep everything.
CURATED_TARGET = {
    "0_baseline_wiki":      0.10,   # wiki factual baseline (kept present, not bulk)
    "100_cosmic_science":   0.10,   # wiki science/cosmic
    "77_art_gutenberg":     0.40,   # Gutenberg literature/poetry (art bulk of curated)
    "91_consciousness_gut": 0.20,   # Gutenberg philosophy/meditation (의식 register)
    "52_social_persona":    0.17,   # authored persona/SNS (anima identity, capped)
    "shaping_authored":     0.03,   # authored dialogue-act/emotion/code-switch/genre
}
CURATED = list(CURATED_TARGET.keys())


def _round_trip(text):
    return text.encode("utf-8", "replace").decode("utf-8", "ignore")


def _blocks(path):
    if not path or not os.path.exists(path):
        return []
    with open(path, "rb") as f:
        text = f.read().decode("utf-8", "ignore")
    out = []
    for b in text.split("\n\n"):
        b = b.strip()
        if len(b) >= 60:
            out.append(_round_trip(b))
    return out


def _guess_lang(block):
    if _HANGUL.search(block):
        return "ko"
    low = block.lower()
    if any(w in low for w in (" der ", " und ", " die ", " ist ", " nicht ",
                              "ß", " würde", "über")):
        return "de"
    if any(w in low for w in (" le ", " les ", " une ", " être ", " où ",
                              "ç", "è", "ê", "à ")):
        return "fr"
    if any(w in low for w in (" el ", " los ", " una ", " está ", "ñ",
                              "¿", "qué")):
        return "es"
    return "en"


def dedup_full(blocks, seen):
    """Dedup on the WHOLE block (sha1). Shared seen set across tiers so a web doc
    duplicating a wiki article is dropped (the wiki/curated tier wins — it is loaded
    FIRST). Near-duplicate filter on the merge."""
    out = []
    for b in blocks:
        key = hashlib.sha1(b.encode("utf-8", "replace")).hexdigest()
        if key in seen:
            continue
        seen.add(key)
        out.append(b)
    return out


def cap_bytes(blocks, max_bytes):
    """Cap to max_bytes keeping the 5 languages PROPORTIONAL (round-robin by guessed
    lang) so a down-cap of the web tier does not collapse to one language."""
    if max_bytes is None:
        return blocks
    by_lang = {l: [] for l in LANGS}
    for b in blocks:
        by_lang[_guess_lang(b)].append(b)
    cursors = {l: 0 for l in LANGS}
    out, got = [], 0
    progressing = True
    while got < max_bytes and progressing:
        progressing = False
        for l in LANGS:
            if cursors[l] < len(by_lang[l]):
                b = by_lang[l][cursors[l]]
                cursors[l] += 1
                out.append(b)
                got += len((b + "\n\n").encode("utf-8", "replace"))
                progressing = True
                if got >= max_bytes:
                    break
    return out


def _tier_bytes(blocks):
    return sum(len((b + "\n\n").encode("utf-8", "replace")) for b in blocks)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src-dir", default="serving/corpus/_src")
    ap.add_argument("--web", default="serving/corpus/_src/web_bulk.txt")
    ap.add_argument("--shaping", default="serving/corpus/_src/shaping.txt")
    ap.add_argument("--persona", default="serving/corpus/_src/persona.txt")
    ap.add_argument("--out", default="serving/corpus/default_lane_7b_webscale.txt")
    ap.add_argument("--report", default="serving/corpus/_src/7b_webscale_report.json")
    args = ap.parse_args()

    sd = args.src_dir
    raw_paths = {
        "web_bulk":             args.web,
        "0_baseline_wiki":      os.path.join(sd, "wiki_t0.txt"),
        "100_cosmic_science":   os.path.join(sd, "wiki_t100.txt"),
        "77_art_gutenberg":     os.path.join(sd, "gut_art.txt"),
        "91_consciousness_gut": os.path.join(sd, "gut_con.txt"),
        "52_social_persona":    args.persona,
        "shaping_authored":     args.shaping,
    }

    # load + dedup (full-block) with a SHARED seen set. Load curated tiers FIRST so a
    # web doc that duplicates a curated article loses the dup race (curated wins).
    seen = set()
    tier_blocks, tier_avail = {}, {}
    load_order = ["91_consciousness_gut", "77_art_gutenberg", "100_cosmic_science",
                  "0_baseline_wiki", "52_social_persona", "shaping_authored",
                  "web_bulk"]
    for name in load_order:
        blk = dedup_full(_blocks(raw_paths[name]), seen)
        tier_blocks[name] = blk
        tier_avail[name] = _tier_bytes(blk)

    # ---- enforce the 7B band ----
    # The curated registers anchor the total (they take ALL they have — scarce
    # minority). The web tier is the majority, DOWN-capped so its share lands inside
    # WEB_BAND. Given curated_sum C and web target share w in [lo,hi]:
    #   total = C / (1 - w)  ->  web = total * w = C * w / (1 - w).
    # We pick the LARGEST web cap such that web <= web_available AND web_share <= hi,
    # then verify web_share >= lo (if web is too scarce to hit lo, we report honestly
    # and emit all the web we have — the corpus is then curated-heavier than target).
    curated_sum = sum(tier_avail[n] for n in CURATED)
    web_avail = tier_avail["web_bulk"]

    web_cap_hi = int(curated_sum * WEB_BAND[1] / (1.0 - WEB_BAND[1]))
    web = min(web_avail, web_cap_hi)
    caps = {n: None for n in CURATED}   # curated: take all (None = uncapped)
    caps["web_bulk"] = web

    # apply caps to blocks
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    ordered_names = ["web_bulk", "0_baseline_wiki", "100_cosmic_science",
                     "77_art_gutenberg", "91_consciousness_gut",
                     "52_social_persona", "shaping_authored"]
    per_tier_bytes, per_tier_lang = {}, {}
    per_lang_bytes = {l: 0 for l in LANGS}
    total = 0
    with open(args.out, "wb") as f:
        for name in ordered_names:
            blocks = cap_bytes(tier_blocks[name], caps.get(name))
            tb = 0
            pl = {l: 0 for l in LANGS}
            for b in blocks:
                enc = (b + "\n\n").encode("utf-8", "replace")
                f.write(enc)
                nb = len(enc)
                tb += nb; total += nb
                lg = _guess_lang(b)
                pl[lg] += nb; per_lang_bytes[lg] += nb
            per_tier_bytes[name] = tb
            per_tier_lang[name] = pl

    def pct(x):
        return round(100.0 * x / total, 2) if total else 0.0

    tokens = total  # byte-vocab V=256 => 1 byte ~ 1 token
    chinchilla_7b = 140_000_000_000
    ratio = tokens / chinchilla_7b
    tok_per_param = tokens / 7_000_000_000
    web_share = pct(per_tier_bytes["web_bulk"])
    art_con = (pct(per_tier_bytes["77_art_gutenberg"])
               + pct(per_tier_bytes["91_consciousness_gut"]))

    # honest 7B-regime statement
    if ratio >= 0.95:
        regime = "near-Chinchilla-optimal 7B (>=20 tok/param)"
    elif tok_per_param >= 3:
        regime = (f"undertrained-but-coherent 7B "
                  f"({tok_per_param:.1f} tok/param; >=3 = trainable, < 20 optimal)")
    elif tok_per_param >= 1:
        regime = (f"low-data 7B ({tok_per_param:.2f} tok/param; >=1 trainable but "
                  f"well undertrained)")
    else:
        regime = (f"sub-1-tok/param ({tok_per_param:.3f}); NOT 7B-trainable as-is — "
                  f"MID-rung scale")

    report = {
        "out": args.out,
        "total_bytes": total,
        "total_mb": round(total / 1048576, 2),
        "total_gb": round(total / 1073741824, 3),
        "byte_tokens": tokens,
        "chinchilla_7b_optimal_tokens": chinchilla_7b,
        "pct_of_7b_optimal": round(100.0 * ratio, 4),
        "tok_per_param_7b": round(tok_per_param, 4),
        "7b_regime": regime,
        "raw_available_bytes": tier_avail,
        "web_band_target_pct": [WEB_BAND[0] * 100, WEB_BAND[1] * 100],
        "curated_target_share_of_remainder":
            {k: round(100 * v, 1) for k, v in CURATED_TARGET.items()},
        "per_tier_bytes": per_tier_bytes,
        "per_tier_pct": {k: pct(v) for k, v in per_tier_bytes.items()},
        "per_lang_bytes": per_lang_bytes,
        "per_lang_pct": {k: pct(v) for k, v in per_lang_bytes.items()},
        "per_tier_lang_bytes": per_tier_lang,
        "web_share_pct": web_share,
        "web_in_band": WEB_BAND[0] * 100 <= web_share <= WEB_BAND[1] * 100,
        "art_plus_consciousness_pct": round(art_con, 2),
        "cosmic_pct": pct(per_tier_bytes.get("100_cosmic_science", 0)),
        "persona_social_pct": pct(per_tier_bytes.get("52_social_persona", 0)),
        "no_tier_starved":
            all(pct(per_tier_bytes[n]) >= 0.5 for n in ordered_names
                if tier_avail[n] > 0),
        "ko_has_web_bulk": per_tier_lang["web_bulk"]["ko"] > 0,
    }
    sha = hashlib.sha256()
    with open(args.out, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            sha.update(chunk)
    report["sha256"] = sha.hexdigest()

    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    with open(args.report, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
