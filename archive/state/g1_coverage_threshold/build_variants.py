#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════════════
#  H_1824 — compositional-data-coverage variant builder (orthogonal family #1).
#
#  From the 4 clean register cells {gen,sns}x{ko,en}.txt build 3 density variants
#  LOW / MID / HIGH per cell, keeping the 4-cell register split. The ONLY varied
#  axis is compositional density (compound/derived-word frequency per line).
#
#  COMPOUND/DERIVED detector (closed-class heuristic, deterministic p7):
#    en: a token is "compound/derived" if it (a) contains a hyphen joining two
#        alpha stems (nation-state, left-wing), OR (b) ends in a productive
#        derivational affix on a >=5-char stem (-ness -ment -tion -ity -able
#        -ful -less -ship -hood -ward -wise -ization), OR (c) is a known closed
#        compound (sunlight, rainbow, airport, bookshelf, notebook, keyboard,
#        ...), OR (d) is a long (>=9) all-alpha token that splits into two known
#        sub-stems (crude productive-compound proxy).
#    ko: a token (whitespace) is "compound/derived" if it (a) contains a known
#        productive suffix block (-주의 -화 -적 -성 -들 -하다 -되다 -스럽 -답-),
#        OR (b) is a >=4-syllable Hangul run whose first 2 + last 2 syllables are
#        each a frequent standalone block (compound proxy), OR (c) contains a
#        latin-in-hangul gloss "(Peanut Farmer)" style compound annotation.
#
#  DENSITY(line) = compound_tokens / max(1, total_tokens).  Per-cell density =
#  mean over lines (weighted by line length when reported per-1k-tokens).
#
#  VARIANTS per cell (line-level binning, byte-preserving sentences):
#    LOW  : keep lines with density <= q33  (compositionally sparse)
#    MID  : keep ALL lines (as-is baseline)
#    HIGH : keep lines with density >= q67, then OVERSAMPLE the top-decile-dense
#           lines so the cell HIGH byte-size ~matches MID (density ceiling).
#  We size LOW/HIGH cells to ~the MID cell byte count (±) by sampling-with-repeat
#  on the dense side / truncation on the sparse side, so train BUDGET is equal
#  across variants and only DENSITY differs (controls corpus-size confound).
#
#  FAIL-LOUD (a_chat_registers): prints per-variant per-cell compounds/1k-tokens.
#  If the per-cell mean density is NOT monotone LOW < MID < HIGH the build is
#  INVALID -> exit 3 (no silent skip).
# ════════════════════════════════════════════════════════════════════════════
from __future__ import annotations
import os
import sys
import random
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "clm303_clean_corpus"))
OUT = os.path.join(HERE, "variants")

CELLS = [("gen_ko", "ko"), ("gen_en", "en"), ("sns_ko", "ko"), ("sns_en", "en")]

# ── EN compound/derived detection ────────────────────────────────────────────
EN_AFFIX = ("ness", "ment", "tion", "sion", "ity", "able", "ible", "ful",
            "less", "ship", "hood", "ward", "wise", "ization", "isation",
            "ologist", "ology", "ically")
EN_KNOWN_COMPOUND = {
    "sunlight", "rainbow", "airport", "bookshelf", "notebook", "keyboard",
    "moonlight", "daylight", "newspaper", "waterfall", "firefly", "football",
    "basketball", "weekend", "birthday", "background", "foreground",
    "everyone", "everything", "everywhere", "something", "somewhere",
    "anyone", "anything", "nowhere", "without", "within", "throughout",
    "lifetime", "worldwide", "framework", "network", "database", "software",
    "hardware", "feedback", "outcome", "income", "upstream", "downstream",
    "overflow", "underflow", "afterward", "henceforth", "nonetheless",
    "spacecraft", "spaceship", "battlefield", "countryside", "grassland",
    "homeland", "mainland", "wasteland", "stronghold", "household",
    "stateless", "wingspan", "lighthouse", "greenhouse", "warehouse",
    "blackboard", "cardboard", "keyhole", "loophole", "pinpoint",
}
EN_STEMS = {
    "sun", "moon", "day", "night", "light", "rain", "snow", "water", "fire",
    "land", "house", "home", "work", "book", "key", "board", "net", "way",
    "side", "ground", "back", "fore", "out", "over", "under", "up", "down",
    "head", "hand", "foot", "eye", "ear", "air", "sea", "wind", "wood",
    "stone", "iron", "gold", "star", "world", "life", "time", "war", "space",
    "ship", "craft", "field", "stream", "flow", "fall", "yard", "wide",
    "stand", "hold", "point", "mark", "place", "room", "wall", "door",
}
EN_TOK = re.compile(r"[A-Za-z][A-Za-z\-']*")


def en_is_compound(tok: str) -> bool:
    t = tok.lower().strip("'")
    if "-" in t:
        parts = [p for p in t.split("-") if p]
        if len(parts) >= 2 and all(len(p) >= 2 and p.isalpha() for p in parts):
            return True
    if t in EN_KNOWN_COMPOUND:
        return True
    if len(t) >= 8:
        for af in EN_AFFIX:
            if t.endswith(af) and len(t) - len(af) >= 4:
                return True
    if len(t) >= 9 and t.isalpha():
        # crude productive-compound proxy: known stem prefix + known stem suffix
        for s1 in EN_STEMS:
            if t.startswith(s1) and len(t) - len(s1) >= 3:
                rest = t[len(s1):]
                if rest in EN_STEMS or any(rest.startswith(s2) for s2 in EN_STEMS):
                    return True
    return False


# ── KO compound/derived detection ────────────────────────────────────────────
KO_SUFFIX = ("주의", "화", "적", "성", "들", "하다", "되다", "스럽", "답게",
             "롭게", "스러운", "하는", "되는", "시키", "당하", "이라는",
             "에서의", "으로의", "로서의", "처럼", "마저", "조차")
HANGUL = re.compile(r"[가-힣]+")
KO_TOK = re.compile(r"[가-힣]+")
LATIN_IN_PAREN = re.compile(r"\([A-Za-z][A-Za-z ]+\)")


def ko_is_compound(tok: str, freq_blocks: set | None = None) -> bool:
    for sf in KO_SUFFIX:
        if tok.endswith(sf) and len(tok) - len(sf) >= 1:
            return True
    if len(tok) >= 4 and freq_blocks is not None:
        head = tok[:2]
        tail = tok[-2:]
        if head in freq_blocks and tail in freq_blocks and head != tail:
            return True
    return False


def line_density(line: str, lang: str, ko_freq: set | None) -> tuple[int, int]:
    """Return (compound_tokens, total_tokens) for a line."""
    if lang == "en":
        toks = EN_TOK.findall(line)
        if not toks:
            return 0, 0
        comp = sum(1 for t in toks if en_is_compound(t))
        # paren-gloss compounds count as 1 extra compound signal
        comp += len(LATIN_IN_PAREN.findall(line))
        return comp, len(toks)
    else:
        toks = KO_TOK.findall(line)
        if not toks:
            return 0, 0
        comp = sum(1 for t in toks if ko_is_compound(t, ko_freq))
        comp += len(LATIN_IN_PAREN.findall(line))
        return comp, len(toks)


def build_ko_freq(lines: list[str]) -> set:
    """Frequent 2-syllable Hangul blocks (for compound-proxy head/tail test)."""
    from collections import Counter
    c = Counter()
    for ln in lines:
        for run in HANGUL.findall(ln):
            for i in range(len(run) - 1):
                c[run[i:i + 2]] += 1
    # top blocks that appear often enough to be "standalone-ish"
    return {b for b, n in c.items() if n >= 20}


def process_cell(name: str, lang: str, rng: random.Random) -> dict:
    path = os.path.join(SRC, name + ".txt")
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = [ln.rstrip("\n") for ln in f if ln.strip()]
    ko_freq = build_ko_freq(lines) if lang == "ko" else None

    scored = []  # (density, comp, tot, line)
    for ln in lines:
        comp, tot = line_density(ln, lang, ko_freq)
        dens = (comp / tot) if tot else 0.0
        scored.append((dens, comp, tot, ln))

    dens_vals = sorted(s[0] for s in scored)
    n = len(dens_vals)
    q33 = dens_vals[int(0.33 * n)]
    q67 = dens_vals[int(0.67 * n)]
    q90 = dens_vals[int(0.90 * n)]

    low = [s for s in scored if s[0] <= q33]
    mid = scored[:]                       # as-is baseline
    high_pool = [s for s in scored if s[0] >= q67]
    top_pool = [s for s in scored if s[0] >= q90] or high_pool

    mid_bytes = sum(len(s[3].encode("utf-8")) + 1 for s in mid)

    # size LOW to ~mid_bytes by repeating its (sparse) lines
    def grow_to(pool, target_bytes):
        out = []
        sz = 0
        idx = 0
        pl = pool[:]
        rng.shuffle(pl)
        if not pl:
            return out
        while sz < target_bytes:
            s = pl[idx % len(pl)]
            out.append(s)
            sz += len(s[3].encode("utf-8")) + 1
            idx += 1
        return out

    low_sized = grow_to(low, mid_bytes)
    # HIGH = high_pool, but oversample top-decile-dense lines to reach mid_bytes
    high_base = high_pool[:]
    high_sized = high_base[:]
    cur = sum(len(s[3].encode("utf-8")) + 1 for s in high_sized)
    extra = grow_to(top_pool, max(0, mid_bytes - cur))
    high_sized = high_sized + extra

    def cell_density_per1k(rows):
        comp = sum(r[1] for r in rows)
        tot = sum(r[2] for r in rows)
        return (1000.0 * comp / tot) if tot else 0.0, tot, comp

    variants = {"LOW": low_sized, "MID": mid, "HIGH": high_sized}
    rep = {}
    for v, rows in variants.items():
        d1k, tot, comp = cell_density_per1k(rows)
        nbytes = sum(len(s[3].encode("utf-8")) + 1 for s in rows)
        rep[v] = {"dens_per1k": d1k, "lines": len(rows), "tokens": tot,
                  "compounds": comp, "bytes": nbytes}
        # write the variant cell file
        vdir = os.path.join(OUT, v)
        os.makedirs(vdir, exist_ok=True)
        with open(os.path.join(vdir, name + ".txt"), "w", encoding="utf-8") as f:
            for s in rows:
                f.write(s[3] + "\n")
    return {"q33": q33, "q67": q67, "q90": q90, "rep": rep}


def main():
    rng = random.Random(20260630)
    os.makedirs(OUT, exist_ok=True)
    print("=== H_1824 compositional-density variant build ===")
    print(f"  src: {SRC}")
    print(f"  out: {OUT}")
    print("")
    all_rep = {}
    for name, lang in CELLS:
        info = process_cell(name, lang, rng)
        all_rep[name] = info["rep"]
        print(f"  cell {name:<8s} ({lang})  q33={info['q33']:.4f} "
              f"q67={info['q67']:.4f} q90={info['q90']:.4f}")
        for v in ("LOW", "MID", "HIGH"):
            r = info["rep"][v]
            print(f"     {v:<5s} dens={r['dens_per1k']:7.3f}/1k  "
                  f"lines={r['lines']:6d} tokens={r['tokens']:8d} "
                  f"compounds={r['compounds']:7d} bytes={r['bytes']:9d}")

    # ── fail-loud monotonicity check (per cell + pooled) ─────────────────────
    print("")
    print("=== MONOTONICITY GATE (LOW < MID < HIGH compounds/1k) ===")
    all_ok = True
    for name, _ in CELLS:
        r = all_rep[name]
        lo, mi, hi = r["LOW"]["dens_per1k"], r["MID"]["dens_per1k"], r["HIGH"]["dens_per1k"]
        ok = lo < mi < hi
        all_ok = all_ok and ok
        print(f"  {name:<8s} LOW={lo:.3f} < MID={mi:.3f} < HIGH={hi:.3f}  "
              f"-> {'OK' if ok else 'NON-MONOTONE'}")
    # pooled
    def pooled(v):
        comp = sum(all_rep[n][v]["compounds"] for n, _ in CELLS)
        tot = sum(all_rep[n][v]["tokens"] for n, _ in CELLS)
        return 1000.0 * comp / tot if tot else 0.0
    plo, pmi, phi = pooled("LOW"), pooled("MID"), pooled("HIGH")
    pok = plo < pmi < phi
    print(f"  {'POOLED':<8s} LOW={plo:.3f} < MID={pmi:.3f} < HIGH={phi:.3f}  "
          f"-> {'OK' if pok else 'NON-MONOTONE'}")
    print("")
    if all_ok and pok:
        print("PASS — compositional density is MONOTONE LOW<MID<HIGH across all "
              "4 cells + pooled. Variants are valid for the threshold test.")
        sys.exit(0)
    print("FAIL — density NOT monotone (build INVALID, a_chat_registers fail-loud). "
          "Adjust detector/quantiles before training.")
    sys.exit(3)


if __name__ == "__main__":
    main()
