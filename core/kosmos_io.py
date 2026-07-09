"""core/kosmos_io.py — .kosmos anchor writer/reader for the V3 substrate.

py 2-production twin of core/kosmos_io.hexa (which is itself a torch-free port of the
original kosmos_io.py) — byte-exact mirror of the HEXA (owner directive 2026-07-09
"py 자체구현 · 언어간 상호의존 0"). Persists anima emit / anchor / memory as `.kosmos`
(payload = text + tension 5-ch + coord · lane · radius · tier · a_kosmos). This port
preserves the hexa's `.kosmos` byte format exactly (kosmos/1.1).

PRODUCTION SUBSET — this file ports the live write/read path only:
  map_8factor_to_5channel · tension_5ch_to_embedding (LCG + Box-Muller) ·
  create_anchor · emit_anchor_from_v3 · load_anchors (+ parse helpers).
The DISJOINT research lane (retrieve / kosmos_merge / hippo_* CA3 store) lives in the
numpy 2-production twin core/hippo_lane.py and is intentionally NOT duplicated here.

BYTE-FORMAT PARITY (vs kosmos_io.hexa):
  - coord rendered with 4 decimals (hexa format_float(x, 4) ≡ py f"{x:.4f}").
  - radius rendered with 4 decimals.
  - tension channels rendered with 6 decimals (≡ f"{x:.6f}").
  - escaping order matches _escape_kosmos_string: \\\\ then " then \\n, with \\r stripped.
  - emitted_at = UTC `%Y-%m-%dT%H:%M:%SZ` (wall-clock; masked in parity checks).

CARVE-OUT K1 — tension_5ch_to_embedding uses the hexa's self-contained LCG
(1664525/1013904223) + Box-Muller, NOT Python random.Random (documented cross-language
divergence). The values MATCH the hexa exactly (both use this LCG), and DIFFER from the
original .py MT19937 stream (which the hexa also deliberately abandoned). This fn has no
live write-path caller — general API + self-test surface.

Pure python (no numpy — max structure is 5×embed_dim; plain loops preserve accumulation
order = better for parity). No FFI. hexa Map #{} → python dict.
"""

from math import sqrt, log, cos
from datetime import datetime, timezone
import os


# ── 8-factor → 5-channel mapping (kosmos_io.hexa) ───────────────────────────
# Map an 8-factor anima_participant motivation snapshot to the TENSION-LINK
# 5-channel fingerprint. `factors` is a dict; missing key → 0.0.
def _ki_g(factors, k):
    if k not in factors:
        return 0.0
    return float(factors[k])


def map_8factor_to_5channel(factors):
    return {
        "concept":      (_ki_g(factors, "relevance") + _ki_g(factors, "coherence")) / 2.0,
        "context":      _ki_g(factors, "info_gap"),
        "meaning":      (_ki_g(factors, "curiosity") + _ki_g(factors, "originality")) / 2.0,
        "authenticity": (_ki_g(factors, "pain") + _ki_g(factors, "balance")) / 2.0,
        "sender":       _ki_g(factors, "dynamics"),
    }


# ── tension 5-ch → dense embedding ──────────────────────────────────────────
# LCG (Numerical Recipes constants) + Box-Muller, self-contained (carve-out K1).
def _ki_lcg_next(state):
    # 64-bit LCG; mask to 32 bits for the float draw.
    return (state * 1664525 + 1013904223) & 0xFFFFFFFF


def tension_5ch_to_embedding(tension_5ch, embed_dim, seed):
    inv = 1.0 / sqrt(5.0)
    # Build a 5 x embed_dim gaussian projection matrix via Box-Muller.
    state = seed & 0xFFFFFFFF
    w = []
    k = 0
    while k < 5:
        row = []
        d = 0
        while d < embed_dim:
            # draw two uniforms in (0,1], Box-Muller → one gaussian.
            state = _ki_lcg_next(state)
            u1 = (state + 1.0) / 4294967297.0
            state = _ki_lcg_next(state)
            u2 = state / 4294967296.0
            g = sqrt(0.0 - 2.0 * log(u1)) * cos(6.283185307179586 * u2)
            row.append(g * inv)          # N(0, 1/sqrt(5))
            d = d + 1
        w.append(row)
        k = k + 1
    out = []
    z = 0
    while z < embed_dim:
        out.append(0.0)
        z = z + 1
    kk = 0
    while kk < 5:
        row = w[kk]
        dd = 0
        while dd < embed_dim:
            out[dd] = out[dd] + tension_5ch[kk] * row[dd]
            dd = dd + 1
        kk = kk + 1
    return out


# ── anchor creation ─────────────────────────────────────────────────────────

# _escape_kosmos_string: \\ → \\\\, " → \", \n → \\n, \r stripped.
# Order matters (backslash first so the escapes we add are not re-escaped).
def _escape_kosmos_string(s):
    r = s.replace("\\", "\\\\")
    r = r.replace("\"", "\\\"")
    r = r.replace("\n", "\\n")
    r = r.replace("\r", "")
    return r


# UTC timestamp `%Y-%m-%dT%H:%M:%SZ` (wall-clock UTC instant; masked in parity).
def _ki_utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# create_anchor — write a .kosmos anchor to out_dir/<name>.kosmos.
# Returns the path. cross_link == "" means "no cross_link line" (Py None).
def create_anchor(out_dir, name, title, coord_x, coord_y, lane, radius,
                  tier, category, top_emotion, text, tension_5ch,
                  closed_anchor, cross_link):
    if len(tension_5ch) != 5:
        raise ValueError("tension_5ch must have len=5, got " + str(len(tension_5ch)))
    os.makedirs(out_dir, exist_ok=True)
    path = out_dir + "/" + name + ".kosmos"
    text_esc = _escape_kosmos_string(text)

    lines = []
    lines.append("#!/usr/bin/env kosmos")
    lines.append("# " + name + ".kosmos — V3 substrate-native emission anchor")
    lines.append("# Tier 🛸" + str(tier) + " — " + category + ", top emotion " + top_emotion + ".")
    lines.append("")
    lines.append("@anchor " + name + " := \"" + title + "\" :: kosmos-anchor [tier=" + str(tier) + " active]")
    lines.append("  profile      = \"anima-consciousness-carving\"")
    lines.append("  knuth_tier   = " + str(tier))
    lines.append("  category     = \"" + category + "\"")
    lines.append("  top_emotion  = \"" + top_emotion + "\"")
    lines.append("  coord        = [" + "%.4f" % coord_x + ", " + "%.4f" % coord_y + "]")
    lines.append("  lane         = \"" + lane + "\"")
    lines.append("  radius       = " + "%.4f" % radius)
    lines.append("")
    lines.append("  @payload text    := \"" + text_esc + "\"")
    lines.append("  @payload tension := {")
    lines.append("    concept       = " + "%.6f" % tension_5ch[0] + ",")
    lines.append("    context       = " + "%.6f" % tension_5ch[1] + ",")
    lines.append("    meaning       = " + "%.6f" % tension_5ch[2] + ",")
    lines.append("    authenticity  = " + "%.6f" % tension_5ch[3] + ",")
    lines.append("    sender        = " + "%.6f" % tension_5ch[4] + ",")
    lines.append("  }")
    lines.append("  @payload image   := pending \"V3-emit text+tension only\"")
    lines.append("  @payload audio   := pending \"V3-emit text+tension only\"")
    lines.append("  @payload video   := pending \"V3-emit text+tension only\"")
    lines.append("")
    lines.append("  closed_anchor = \"" + closed_anchor + "\"")
    if len(cross_link) > 0:
        lines.append("  cross_link    = \"" + cross_link + "\"")
    lines.append("  emitted_at    = \"" + _ki_utc_now() + "\"")

    # join with "\n" + trailing "\n" (Py: "\n".join(lines) + "\n").
    body = ""
    i = 0
    while i < len(lines):
        body = body + lines[i]
        if i < len(lines) - 1:
            body = body + "\n"
        i = i + 1
    body = body + "\n"
    with open(path, "w", encoding="utf-8", errors="surrogateescape") as f:
        f.write(body)
    return path


# emit_anchor_from_v3 — high-level emit.
#   coord = [phi, mean(tension_5ch)] as Ψ-space placeholder.
#   lane  = "cell_<mitosis_cell_id>".
def emit_anchor_from_v3(out_dir, name, text, tension_5ch, mitosis_cell_id, tier,
                        category, top_emotion, phi, radius):
    s = 0.0
    i = 0
    while i < len(tension_5ch):
        s = s + tension_5ch[i]
        i = i + 1
    denom = len(tension_5ch)
    mean_t = s / (denom if denom > 1 else 1)
    lane = "cell_" + str(mitosis_cell_id)
    title = "v3-emit " + name + " (tier " + str(tier) + ")"
    return create_anchor(out_dir, name, title, phi, mean_t, lane, radius,
                         tier, category, top_emotion, text, tension_5ch,
                         "V3-emit-auto", "")


# ── anchor loader ───────────────────────────────────────────────────────────

# Parse a placement-field value. Mirrors hexa order:
# string literal → list literal → int → float → raw string.
def _parse_value(v_in):
    v = v_in.strip()
    n = len(v)
    # string literal "..."
    if n >= 2 and v.startswith("\"") and v.endswith("\""):
        return v[1:n - 1]
    # list literal [a, b]
    if n >= 2 and v.startswith("[") and v.endswith("]"):
        inner = v[1:n - 1]
        parts = inner.split(",")
        out = []
        i = 0
        while i < len(parts):
            p = parts[i].strip()
            if _ki_is_number(p):
                out.append(float(p))
            else:
                out.append(p)
            i = i + 1
        return out
    # try int then float (Py int() first, then float()).
    if _ki_is_int(v):
        return int(v)
    if _ki_is_number(v):
        return float(v)
    return v


# Is `s` a parseable int (optional leading -, all digits)?
def _ki_is_int(s):
    n = len(s)
    if n == 0:
        return False
    i = 0
    if ord(s[0]) == 45:                          # leading '-'
        i = 1
    if i >= n:
        return False
    while i < n:
        b = ord(s[i])
        if b < 48 or b > 57:                     # not 0-9
            return False
        i = i + 1
    return True


# Is `s` a parseable number (int or float, allows '.', 'e'/'E', sign)?
def _ki_is_number(s):
    n = len(s)
    if n == 0:
        return False
    i = 0
    seen_digit = False
    seen_dot = False
    seen_e = False
    while i < n:
        b = ord(s[i])
        if b >= 48 and b <= 57:
            seen_digit = True
        elif b == 46:                            # '.'
            if seen_dot or seen_e:
                return False
            seen_dot = True
        elif b == 101 or b == 69:                # 'e' / 'E'
            if seen_e or not seen_digit:
                return False
            seen_e = True
        elif b == 43 or b == 45:                 # '+' / '-'
            # sign only valid at pos 0 or right after e/E.
            if i != 0:
                prev = ord(s[i - 1])
                if prev != 101 and prev != 69:
                    return False
        else:
            return False
        i = i + 1
    return seen_digit


# Strip a trailing comma from a value string (Py .rstrip(',')).
def _ki_rstrip_comma(s):
    r = s
    while len(r) > 0 and ord(r[len(r) - 1]) == 44:
        r = r[0:len(r) - 1]
    return r


# Match a placement-field line `  key = value` → [key, value] or [] if no match.
# Mirrors ANCHOR_FIELD_PATTERN = ^\s*(\w+)\s*=\s*(.+?)\s*$ on the RAW line.
def _ki_field_match(line):
    s = line.strip()
    n = len(s)
    if n == 0:
        return []
    # key = leading word chars [A-Za-z0-9_].
    i = 0
    while i < n:
        b = ord(s[i])
        is_word = (b >= 48 and b <= 57) or (b >= 65 and b <= 90) or (b >= 97 and b <= 122) or b == 95
        if not is_word:
            break
        i = i + 1
    if i == 0:
        return []
    key = s[0:i]
    # skip spaces, require '='.
    while i < n and ord(s[i]) == 32:
        i = i + 1
    if i >= n or ord(s[i]) != 61:                # '='
        return []
    i = i + 1
    while i < n and ord(s[i]) == 32:
        i = i + 1
    if i >= n:
        return []
    val = s[i:n].strip()
    if len(val) == 0:
        return []
    return [key, val]


# Extract a @payload text inline string after := "..." .
# regex .*:=\s*"(.*)"\s*$ — greedy; returns the inner string or "" if none.
def _ki_text_payload(line):
    marker = ":="
    mi = _ki_index_of(line, marker)
    if mi < 0:
        return ""
    after = line[mi + 2:len(line)].strip()
    an = len(after)
    if an >= 2 and after.startswith("\"") and after.endswith("\""):
        return after[1:an - 1]
    return ""


def _ki_index_of(hay, needle):
    hn = len(hay)
    nn = len(needle)
    if nn == 0:
        return 0
    i = 0
    while i + nn <= hn:
        k = 0
        ok = True
        while k < nn:
            if hay[i + k] != needle[k]:
                ok = False
                break
            k = k + 1
        if ok:
            return i
        i = i + 1
    return -1


# load_anchors — load all .kosmos files in dir_path. Returns a list of dicts
# with: path, name, fields (dict), text_payload, tension_5ch ([float] optional).
def load_anchors(dir_path):
    anchors = []
    if not _ki_is_dir(dir_path):
        return anchors
    # sorted listing (Py sorted(os.listdir)).
    files = os.listdir(dir_path)
    files = _ki_sort_strings(files)
    fi = 0
    while fi < len(files):
        fname = files[fi]
        fi = fi + 1
        if not fname.endswith(".kosmos"):
            continue
        path = dir_path + "/" + fname
        with open(path, "r", encoding="utf-8", errors="surrogateescape") as f:
            content = f.read()
        name = fname.replace(".kosmos", "")

        fields = {}
        text_payload = ""
        have_text = False
        tension_buf = {}
        have_tension = False
        in_tension = False

        lines = content.split("\n")
        li = 0
        while li < len(lines):
            line = lines[li]
            li = li + 1
            stripped = line.strip()
            if stripped.startswith("@payload tension"):
                in_tension = _ki_index_of(stripped, "{") >= 0
                continue
            if in_tension:
                if stripped.startswith("}"):
                    in_tension = False
                    continue
                m = _ki_field_match(line)
                if len(m) == 2:
                    kv = _ki_rstrip_comma(m[1])
                    if _ki_is_number(kv):
                        tension_buf[m[0]] = float(kv)
                        have_tension = True
                continue
            if stripped.startswith("@payload text"):
                tp = _ki_text_payload(line)
                if len(tp) > 0:
                    text_payload = tp
                    have_text = True
                continue
            if stripped.startswith("@"):
                continue
            m = _ki_field_match(line)
            if len(m) == 2:
                fields[m[0]] = _parse_value(m[1])

        rec = {
            "path":         path,
            "name":         name,
            "fields":       fields,
            "text_payload": text_payload if have_text else "",
        }
        if have_tension:
            rec["tension_5ch"] = [
                _ki_buf_get(tension_buf, "concept"),
                _ki_buf_get(tension_buf, "context"),
                _ki_buf_get(tension_buf, "meaning"),
                _ki_buf_get(tension_buf, "authenticity"),
                _ki_buf_get(tension_buf, "sender"),
            ]
        anchors.append(rec)
    return anchors


def _ki_buf_get(buf, k):
    if k not in buf:
        return 0.0
    return float(buf[k])


# os.path.isdir equivalent.
def _ki_is_dir(path):
    return os.path.isdir(path)


# simple insertion sort over string list (Py sorted on filenames).
def _ki_sort_strings(xs):
    a = []
    i = 0
    while i < len(xs):
        a.append(xs[i])
        i = i + 1
    j = 1
    while j < len(a):
        key = a[j]
        k = j - 1
        while k >= 0 and _ki_str_gt(a[k], key):
            a[k + 1] = a[k]
            k = k - 1
        a[k + 1] = key
        j = j + 1
    return a


# byte-lexicographic a > b (mirrors hexa byte_at comparison = utf-8 bytes).
def _ki_str_gt(a, b):
    ba = a.encode("utf-8", "surrogateescape")
    bb = b.encode("utf-8", "surrogateescape")
    na = len(ba)
    nb = len(bb)
    i = 0
    while i < na and i < nb:
        ca = ba[i]
        cb = bb[i]
        if ca != cb:
            return ca > cb
        i = i + 1
    return na > nb
