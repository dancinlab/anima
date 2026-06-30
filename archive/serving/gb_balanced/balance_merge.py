#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""balance_merge.py — assemble the KOSMOS-tier-BALANCED GB-scale default-lane corpus.

Takes the per-tier source slices (wiki t0/t100 + Gutenberg art/consciousness) plus
the authored register-shaping + capped persona/SNS slices, then ENFORCES the KOSMOS
ladder rather than merely concatenating:

  1. dedup    — near-duplicate filter on the FULL block (sha1 of the whole block),
                NOT a short prefix — templated authored slices share long prefixes,
                so a prefix-hash would wrongly collapse them.
  2. LADDER   — cap each tier to its target share of the total so NO single tier
                exceeds ~45% and consciousness / art stay meaningfully present.
                The dominant wiki-baseline tier is DOWN-capped to its target; thin
                tiers (consciousness, es/ko) keep everything they have (honest).
  3. round-trip — UTF-8 decode/encode every block (vocab256 byte cleanliness).
  4. account  — emit achieved per-TIER and per-LANG byte split + tier vs ideal
                ladder + byte-token count vs the 140B Chinchilla-7B-optimal line.

The target ladder (fractions of the final total). Tiers that cannot reach their
target (consciousness, es/ko Gutenberg) take ALL they have — honest, never padded;
the freed share is absorbed by the wiki baseline cap which is computed LAST so the
total stays coherent and no tier exceeds the 45% ceiling.

Usage
-----
  python3 serving/gb_balanced/balance_merge.py \
      --src-dir serving/corpus/_src \
      --shaping serving/corpus/_src/shaping.txt \
      --persona serving/corpus/_src/persona.txt \
      --out serving/corpus/default_lane_gb_balanced.txt \
      --report serving/corpus/_src/gb_balanced_report.json
"""

import argparse
import hashlib
import json
import os
import re

LANGS = ["en", "fr", "de", "es", "ko"]
_HANGUL = re.compile(r"[가-힣]")

# target tier shares (sum ~1.0). wiki baseline is the residual floor (computed last).
TARGET = {
    "0_baseline_wiki":      0.40,   # the broad factual floor (kept clear of 45% ceiling)
    "100_cosmic_science":   0.10,
    "77_art_gutenberg":     0.20,
    "91_consciousness_gut": 0.10,
    "52_social_persona":    0.12,
    "shaping_authored":     0.10,
}
MAX_TIER = 0.44  # internal ceiling — keeps the REPORTED tier pct strictly under 45%
# per-tier soft headroom above its TARGET share — keeps any one register (e.g. art,
# which scales abundantly) from ballooning and crowding the others. art is capped at
# TARGET+HEADROOM of the total so the ladder stays even.
TIER_HEADROOM = 0.10


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
    """Dedup on the WHOLE block (not a prefix) so templated authored slices that
    share long prefixes are NOT wrongly collapsed."""
    out = []
    for b in blocks:
        key = hashlib.sha1(b.encode("utf-8", "replace")).hexdigest()
        if key in seen:
            continue
        seen.add(key)
        out.append(b)
    return out


def cap_bytes(blocks, max_bytes):
    """Cap to max_bytes while keeping the 5 languages PROPORTIONAL — round-robin by
    guessed language so a down-cap of a dominant tier (e.g. wiki) does not collapse
    to whichever language happens to come first in the file."""
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
                nb = len(b.encode("utf-8", "replace")) + 2
                if got + nb > max_bytes:
                    continue
                out.append(b)
                got += nb
                progressing = True
                if got >= max_bytes:
                    break
    return out


def _tier_bytes(blocks):
    return sum(len(b.encode("utf-8", "replace")) + 2 for b in blocks)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src-dir", default="serving/corpus/_src")
    ap.add_argument("--shaping", default="serving/corpus/_src/shaping.txt")
    ap.add_argument("--persona", default="serving/corpus/_src/persona.txt")
    ap.add_argument("--out", default="serving/corpus/default_lane_gb_balanced.txt")
    ap.add_argument("--report", default="serving/corpus/_src/gb_balanced_report.json")
    args = ap.parse_args()

    sd = args.src_dir
    raw_paths = {
        "0_baseline_wiki":      os.path.join(sd, "wiki_t0.txt"),
        "100_cosmic_science":   os.path.join(sd, "wiki_t100.txt"),
        "77_art_gutenberg":     os.path.join(sd, "gut_art.txt"),
        "91_consciousness_gut": os.path.join(sd, "gut_con.txt"),
        "52_social_persona":    args.persona,
        "shaping_authored":     args.shaping,
    }

    # load + dedup (full-block) with a SHARED seen set so cross-tier dups are removed
    seen = set()
    tier_blocks, tier_avail = {}, {}
    for name in ["91_consciousness_gut", "77_art_gutenberg", "100_cosmic_science",
                 "52_social_persona", "shaping_authored", "0_baseline_wiki"]:
        # consciousness first so its (scarce) blocks win any cross-tier dup race
        blk = dedup_full(_blocks(raw_paths[name]), seen)
        tier_blocks[name] = blk
        tier_avail[name] = _tier_bytes(blk)

    # ---- enforce the ladder ----
    # Pick a TOTAL T anchored on the SCARCEST tier that we want meaningfully present
    # (consciousness): give it all it has at its target share, which sizes T; then every
    # other tier takes min(available, target_share * T). Tiers short of target keep all
    # they have (honest). Finally clamp any tier to the MAX_TIER ceiling. This keeps art
    # from dominating and keeps consciousness/art comparable as KOSMOS registers.
    # Sweep a range of totals T and pick the LARGEST T that still yields a valid ladder
    # (no tier over MAX_TIER) given what each tier actually HAS. For a given T each tier
    # takes min(available, target*T); tiers short of target inflate the others' relative
    # share, so beyond a point wiki (the only abundant tier) would exceed MAX_TIER — the
    # sweep stops just before that. This maximizes corpus size subject to the ladder.
    # The NON-wiki tiers (art / science / consciousness / persona / shaping) supply
    # everything they have UP TO their target share of a sweep total; the abundant wiki
    # baseline then fills the rest up to EXACTLY the MAX_TIER ceiling. Because the scarce
    # tiers (consciousness, shaping, persona, es/ko) fall short of their targets, tying
    # wiki to a fixed 40% would force a tiny corpus; instead wiki = the largest value
    # that keeps wiki_share <= MAX_TIER given the real non-wiki bytes. This maximizes the
    # corpus subject to the ladder while consuming the non-wiki real text fully.
    NONWIKI = [n for n in TARGET if n != "0_baseline_wiki"]
    # sweep a total T for the NON-wiki tiers; each takes min(avail, target*T_eff) where
    # T_eff scales the non-wiki targets to sum to 1 among themselves.
    nonwiki_target_sum = sum(TARGET[n] for n in NONWIKI)
    best, best_total = None, -1
    T_hi = sum(tier_avail[n] for n in NONWIKI) / min(TARGET[n] for n in NONWIKI)
    for i in range(1, 4001):
        T = T_hi * i / 4000
        nw = {n: min(tier_avail[n], int(TARGET[n] * T)) for n in NONWIKI}
        nw_sum = sum(nw.values())
        if nw_sum <= 0:
            continue
        # wiki fills up to the MAX_TIER ceiling: wiki/(wiki+nw_sum) <= MAX_TIER
        wiki_max_by_ceiling = int(MAX_TIER / (1.0 - MAX_TIER) * nw_sum)
        wiki = min(tier_avail["0_baseline_wiki"], wiki_max_by_ceiling)
        caps = dict(nw); caps["0_baseline_wiki"] = wiki
        tot = sum(caps.values())
        # validity: no tier over MAX_TIER, AND each non-wiki tier within TARGET+headroom
        # so a scalable register (art) cannot crowd out the others.
        ok = all(v <= MAX_TIER * tot + 1 for v in caps.values())
        ok = ok and all(
            caps[n] <= (TARGET[n] + TIER_HEADROOM) * tot + 1 for n in NONWIKI)
        if ok and tot > best_total:
            best, best_total = caps, tot
    caps = best if best else {n: min(tier_avail[n], int(TARGET[n] * 0)) for n in TARGET}

    # apply caps to blocks
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    ordered_names = ["0_baseline_wiki", "100_cosmic_science", "77_art_gutenberg",
                     "91_consciousness_gut", "52_social_persona", "shaping_authored"]
    per_tier_bytes, per_tier_lang = {}, {}
    per_lang_bytes = {l: 0 for l in LANGS}
    total = 0
    with open(args.out, "wb") as f:
        for name in ordered_names:
            blocks = cap_bytes(tier_blocks[name], caps[name])
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
    report = {
        "out": args.out,
        "total_bytes": total,
        "total_mb": round(total / 1048576, 2),
        "total_gb": round(total / 1073741824, 3),
        "byte_tokens": tokens,
        "chinchilla_7b_optimal_tokens": chinchilla_7b,
        "pct_of_7b_optimal": round(100.0 * tokens / chinchilla_7b, 4),
        "raw_available_bytes": tier_avail,
        "target_tier_pct": {k: round(100 * v, 1) for k, v in TARGET.items()},
        "per_tier_bytes": per_tier_bytes,
        "per_tier_pct": {k: pct(v) for k, v in per_tier_bytes.items()},
        "per_lang_bytes": per_lang_bytes,
        "per_lang_pct": {k: pct(v) for k, v in per_lang_bytes.items()},
        "per_tier_lang_bytes": per_tier_lang,
        "max_tier_pct": max(pct(v) for v in per_tier_bytes.values()) if per_tier_bytes else 0,
        "ladder_ok_no_tier_over_45": all(pct(v) <= 45.0 for v in per_tier_bytes.values()),
        "consciousness_present": pct(per_tier_bytes.get("91_consciousness_gut", 0)) >= 1.0,
        "art_present": pct(per_tier_bytes.get("77_art_gutenberg", 0)) >= 1.0,
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
