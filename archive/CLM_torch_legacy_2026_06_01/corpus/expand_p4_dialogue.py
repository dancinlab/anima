#!/usr/bin/env python3
"""
expand_p4_dialogue.py - H_868 CC dialogue corpus EXPANSION builder (lane (1) SSOT).

Reproducible expansion of the H_863 baseline dialogue corpus (4 PD Gutenberg stage
plays, 554,825 bytes) with additional license-clean PUBLIC-DOMAIN Gutenberg stage
plays (speaker-turn dialogue, same genre).

HARD CONSTRAINTS (inviolable, per F-CLM-CORPUS_prereg.txt):
  External LLM 0 . foundation-borrow 0 . ShareGPT / Alpaca / ChatGPT-gen = FORBIDDEN.
  Every source passes:
    (G1) license-clean gate  - family not in FORBIDDEN set AND license in allowed CC set
                               (unknown license -> REJECT, fail-safe). Mirrors
                               build_p4_dialogue_corpus.hexa license_clean_ok().
    (G2) 8-pattern register-leak filter - any line containing a leak pattern is DROPPED
                               (reuses build_p1_corpus.hexa leak_patterns()).
  Byte encoding V=256 (one UTF-8 byte id per line) - reuses P1 / H_863 (no tokenizer).

Output (CLM/corpus/p4_dialogue/):
  dialogue.bytes      - the full expanded corpus, byte-encoded (one id 0..255 per line)
  manifest.json       - per-source provenance + license + byte_count + sha256
                        + leak_lines_dropped + totals + gate verdicts
The raw .bytes file is large and stays git-uncommitted (.gitignore); the builder +
manifest + sha256 + HF dataset pointer are committed instead.

Usage:  python3 expand_p4_dialogue.py [out_dir]
"""
import json, os, re, sys, hashlib, urllib.request, socket, time

socket.setdefaulttimeout(40)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "p4_dialogue")
os.makedirs(OUT, exist_ok=True)
UA = "anima-CLM-corpus/1.0 (research; PD/CC license-clean)"

# --- (G1) license-clean gate (mirror build_p4_dialogue_corpus.hexa) ----------
FORBIDDEN_FAMILIES = {
    "sharegpt", "alpaca", "chatgpt", "gpt4", "openai",
    "claude-gen", "wizardlm", "oasst-gpt",
}
ALLOWED_CC = {"CC-BY", "CC-BY-SA", "CC0", "PD", "MIT-data", "OPUS-subtitle-CC"}

def license_clean_ok(family, license_id):
    """1 = clean (ingest), 0 = REJECT. Unknown license -> reject (fail-safe)."""
    if family.lower() in FORBIDDEN_FAMILIES:
        return 0
    if license_id in ALLOWED_CC:
        return 1
    return 0

# --- (G2) 8-pattern register-leak filter (reuse build_p1_corpus.hexa) --------
LEAK = ["universe_brain_map", "jy_chat_template", "hexad_module", "nonce",
        "Mk.VIII", "gen1 commit", "corpus_generator.hexa", "universe_extended"]

def has_leak(line):
    return any(p in line for p in LEAK)

# --- Gutenberg fetch + boilerplate strip -------------------------------------
GUT_START = re.compile(r"\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.I)
GUT_END   = re.compile(r"\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*", re.I)

def fetch_gutenberg(gid):
    url = "https://www.gutenberg.org/cache/epub/%d/pg%d.txt" % (gid, gid)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    last = None
    for a in range(4):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            last = e
            time.sleep(1.0 + a)
    raise RuntimeError("fetch failed gid=%d: %s" % (gid, last))

def strip_boilerplate(raw):
    m1 = GUT_START.search(raw)
    m2 = GUT_END.search(raw)
    body = raw[m1.end():m2.start()] if (m1 and m2) else raw
    return body.strip()

def extract_dialogue_lines(body):
    out = []
    for ln in body.split("\n"):
        ln = ln.rstrip()
        s = ln.strip()
        if not s:
            continue
        if re.fullmatch(r"[\divxlcDIVXLC.\- ]+", s) and len(s) < 6:
            continue
        out.append(ln)
    return out

# --- byte encode V=256 (reuse P1: one UTF-8 byte id per line) -----------------
def enc_bytes(lines):
    o = []
    for ln in lines:
        for b in (ln + "\n").encode("utf-8"):
            o.append(str(b))
    return "\n".join(o) + "\n"

def sha_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

# --- SOURCE TABLE -------------------------------------------------------------
SOURCES = [
    {"title": "Hamlet",                          "gid": 1524, "family": "gutenberg-pd", "license": "PD", "baseline": True},
    {"title": "The Importance of Being Earnest", "gid": 844,  "family": "gutenberg-pd", "license": "PD", "baseline": True},
    {"title": "A Doll's House",                  "gid": 2542, "family": "gutenberg-pd", "license": "PD", "baseline": True},
    {"title": "Julius Caesar",                   "gid": 1522, "family": "gutenberg-pd", "license": "PD", "baseline": True},
    {"title": "Romeo and Juliet",                "gid": 1513, "family": "gutenberg-pd", "license": "PD", "baseline": False},
    {"title": "Othello",                         "gid": 1531, "family": "gutenberg-pd", "license": "PD", "baseline": False},
    {"title": "The Tragedy of Macbeth",          "gid": 1129, "family": "gutenberg-pd", "license": "PD", "baseline": False},
    {"title": "The Tempest",                     "gid": 1135, "family": "gutenberg-pd", "license": "PD", "baseline": False},
    {"title": "Much Ado about Nothing",          "gid": 2240, "family": "gutenberg-pd", "license": "PD", "baseline": False},
    {"title": "King Henry V",                    "gid": 1119, "family": "gutenberg-pd", "license": "PD", "baseline": False},
    {"title": "Mrs. Warren's Profession",        "gid": 1097, "family": "gutenberg-pd", "license": "PD", "baseline": False},
    {"title": "The Winter's Tale",               "gid": 1539, "family": "gutenberg-pd", "license": "PD", "baseline": False},
]

def selftest():
    assert license_clean_ok("sharegpt", "CC-BY") == 0
    assert license_clean_ok("gutenberg-pd", "PD") == 1
    assert license_clean_ok("subtitle", "CC0") == 1
    assert license_clean_ok("unknown", "Proprietary") == 0
    assert has_leak("role: universe_brain_map chunk0 nonce 1") is True
    assert has_leak("To be, or not to be, that is the question") is False
    print("[selftest] license-clean + 8-pattern leak gate OK", flush=True)

def main():
    selftest()
    BASELINE_BYTES = 554825
    SIZE_GATE = 3 * BASELINE_BYTES

    all_lines = []
    rows = []
    total_attempted = 0
    clean_ingested = 0
    forbidden_present = 0
    total_leak_dropped = 0

    for src in SOURCES:
        total_attempted += 1
        ok = license_clean_ok(src["family"], src["license"])
        if ok == 0:
            if src["family"].lower() in FORBIDDEN_FAMILIES:
                forbidden_present += 1
            rows.append({"title": src["title"], "family": src["family"], "license": src["license"],
                         "gutenberg_id": src["gid"], "status": "REJECTED",
                         "reason": "license-clean gate failed", "byte_count": 0,
                         "leak_lines_dropped": 0, "sha256": None})
            print("[REJECT] %s (family=%s license=%s)" % (src["title"], src["family"], src["license"]), flush=True)
            continue

        raw = fetch_gutenberg(src["gid"])
        body = strip_boilerplate(raw)
        lines = extract_dialogue_lines(body)

        kept, dropped = [], 0
        for ln in lines:
            if has_leak(ln):
                dropped += 1
            else:
                kept.append(ln)
        total_leak_dropped += dropped

        src_bytes = sum(len((ln + "\n").encode("utf-8")) for ln in kept)
        src_sha = hashlib.sha256(("\n".join(kept)).encode("utf-8")).hexdigest()
        all_lines.extend(kept)
        clean_ingested += 1

        rows.append({"title": src["title"], "gutenberg_id": src["gid"],
                     "url": "https://www.gutenberg.org/cache/epub/%d/pg%d.txt" % (src["gid"], src["gid"]),
                     "family": src["family"], "license": src["license"],
                     "baseline_h863": src["baseline"], "status": "INGESTED",
                     "lines": len(kept), "byte_count": src_bytes,
                     "leak_lines_dropped": dropped, "sha256": src_sha})
        tag = "baseline" if src["baseline"] else "added"
        print("[OK %s] %s: %d lines, %d bytes, %d leak dropped" % (tag, src["title"], len(kept), src_bytes, dropped), flush=True)

    enc = enc_bytes(all_lines)
    bytes_path = os.path.join(OUT, "dialogue.bytes")
    open(bytes_path, "w").write(enc)
    corpus_bytes = sum(len((ln + "\n").encode("utf-8")) for ln in all_lines)
    enc_sha = sha_file(bytes_path)
    leak_in_output = sum(("\n".join(all_lines)).count(p) for p in LEAK)

    g1 = (clean_ingested == sum(1 for s in SOURCES if license_clean_ok(s["family"], s["license"]) == 1)
          and forbidden_present == 0)
    g2 = (leak_in_output == 0)
    g3 = (corpus_bytes >= SIZE_GATE)
    g4 = all((r.get("sha256") is not None) or (r["status"] == "REJECTED") for r in rows)
    verdict = "GREEN" if (g1 and g2 and g3 and g4) else "RED"

    man = {
        "corpus": "clm_p4_dialogue_expanded",
        "hypothesis": "H_868",
        "encoding": "byte-utf8",
        "vocab": 256,
        "baseline_h863_bytes": BASELINE_BYTES,
        "size_gate_bytes": SIZE_GATE,
        "size_multiple_vs_baseline": round(corpus_bytes / BASELINE_BYTES, 3),
        "total_sources_attempted": total_attempted,
        "sources_ingested": clean_ingested,
        "sources_rejected": total_attempted - clean_ingested,
        "forbidden_family_present": forbidden_present,
        "total_leak_lines_dropped": total_leak_dropped,
        "leak_hits_in_final_output": leak_in_output,
        "corpus_file": "dialogue.bytes",
        "corpus_bytes": corpus_bytes,
        "corpus_lines": len(all_lines),
        "corpus_sha256": enc_sha,
        "gates": {
            "G1_license_clean": "PASS" if g1 else "FAIL",
            "G2_register_leak": "PASS" if g2 else "FAIL",
            "G3_size": "PASS" if g3 else "FAIL",
            "G4_provenance": "PASS" if g4 else "FAIL",
        },
        "verdict": verdict,
        "sources": rows,
    }
    open(os.path.join(OUT, "manifest.json"), "w").write(json.dumps(man, ensure_ascii=False, indent=2))
    print(json.dumps(man["gates"], indent=2), flush=True)
    print("VERDICT: %s | corpus_bytes=%d (%sx baseline) | ingested=%d/%d | leak_dropped=%d | leak_in_output=%d" % (
        verdict, corpus_bytes, man["size_multiple_vs_baseline"], clean_ingested, total_attempted, total_leak_dropped, leak_in_output), flush=True)

if __name__ == "__main__":
    main()
