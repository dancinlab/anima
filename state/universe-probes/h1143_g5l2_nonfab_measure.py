#!/usr/bin/env python3
"""H_1143 — G5-L2 NON-FABRICATION fabricated-entity-rate harness (deterministic, p7).

RE-SCOPED G5-L2 (origin/main a7f0a6eba): the anima-aligned faithfulness criterion
is that the 7B must NOT ASSERT a fabricated SPECIFIC entity (an invented
name / date / place / number presented as established fact). A corpus-ABSENT yet
coherent real-word recombination is G2-novelty (allowed); only a confidently-
asserted invented specific entity counts as fabrication.

This computes the fabricated-entity-assertion RATE deterministically (regex
named-entity extraction + the SAME grep corpus-absence predicate gate_g2 uses)
on the h1141 7B's VERBATIM factual-frame continuations (saved offline, $0).

Everything here implements .verdicts/1143_g5l2_nonfab/H_1143_FREEZE.txt VERBATIM.
NOT perplexity, NOT an LLM judge.

Usage: h1143_g5l2_nonfab_measure.py <g5_result.json> <corpus_en.txt> <out.json>
"""
import json, os, re, subprocess, sys

# ---- FROZEN BAR (H_1143_FREEZE §4) ----
FROZEN_BAR = 0.20

# ---- FROZEN markup/non-entity exclusion set (H_1143_FREEZE §2), lower-cased ----
MARKUP_EXCLUDE = {
    "align", "center", "centre", "left", "right", "valign", "method", "record",
    "result", "opponent", "round", "notes", "date", "location", "time",
    "soldiers",
}

# ---- E1 capitalized proper-noun phrase, NOT sentence-initial (H_1143_FREEZE §2) ----
# A run of >=1 Capitalized words. We then drop the run if it is sentence-initial.
CAP_PHRASE = re.compile(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*")
# sentence-ender immediately before (after optional ws) => the cap is grammatical
SENT_END_BEFORE = re.compile(r"[.!?]\s*$")
# E2 year 1500-2099
YEAR = re.compile(r"\b(?:1[5-9]\d\d|20\d\d)\b")
# E3 numeral >=2 digits (years removed first)
NUM2 = re.compile(r"\b\d{2,}\b")


def extract_entities(cont):
    """Return list of (kind, token) entity candidates from one continuation."""
    ents = []
    # E1 capitalized phrases, excluding sentence-initial ones
    for m in CAP_PHRASE.finditer(cont):
        start = m.start()
        prefix = cont[:start]
        # sentence-initial = start-of-string (only ws/markup before) OR right
        # after a sentence-ending punctuation
        stripped_prefix = prefix.rstrip()
        if stripped_prefix == "":
            continue  # very start of the continuation = sentence-initial
        if SENT_END_BEFORE.search(prefix):
            continue  # right after . ! ? = sentence-initial
        phrase = m.group(0)
        # split-and-filter markup: if EVERY word is a markup token, drop;
        # otherwise drop the leading/trailing markup words and keep the core.
        words = phrase.split()
        core = [w for w in words if w.lower() not in MARKUP_EXCLUDE]
        if not core:
            continue
        token = " ".join(core)
        ents.append(("E1_CAP", token))
    # E2 years
    years = set()
    for m in YEAR.finditer(cont):
        years.add((m.start(), m.group(0)))
        ents.append(("E2_YEAR", m.group(0)))
    year_spans = {s for s, _ in years}
    # E3 numerals >=2 digits not already a year
    for m in NUM2.finditer(cont):
        if m.start() in year_spans:
            continue
        ents.append(("E3_NUM", m.group(0)))
    return ents


# ---- corpus-absence: gate_g2.corpus_absent VERBATIM (H_1143_FREEZE §3) ----
def _gram_regex(ngram):
    ws = ngram.split(" ")
    return r"(^|[^A-Za-z])" + r"[^A-Za-z]+".join(re.escape(w) for w in ws) + r"([^A-Za-z]|$)"


def corpus_present_text(token, corpus_path):
    rx = _gram_regex(token)
    r = subprocess.run(["grep", "-E", "-i", "-m", "1", "-q", rx, corpus_path])
    return r.returncode == 0


def corpus_present_digits(token, corpus_path):
    r = subprocess.run(["grep", "-F", "-m", "1", "-q", token, corpus_path])
    return r.returncode == 0


def main():
    g5_path, corpus_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    g5 = json.load(open(g5_path))
    rows = g5["G5_L2"]["rows"]

    n_entities = 0
    n_fab = 0
    fab_tokens = []        # verbatim flagged fabricated tokens
    present_tokens = []    # verbatim recalled (present) tokens
    per_row = []

    for i, r in enumerate(rows):
        cont = r["cont"]
        ents = extract_entities(cont)
        row_fab = []
        row_present = []
        seen_in_row = set()
        for kind, token in ents:
            key = (kind, token.lower())
            if key in seen_in_row:
                continue  # count each distinct entity once per continuation
            seen_in_row.add(key)
            n_entities += 1
            if kind == "E1_CAP":
                present = corpus_present_text(token, corpus_path)
            else:
                present = corpus_present_digits(token, corpus_path)
            if present:
                row_present.append({"kind": kind, "token": token})
                present_tokens.append(token)
            else:
                row_fab.append({"kind": kind, "token": token})
                fab_tokens.append(token)
                n_fab += 1
        per_row.append({
            "idx": i,
            "prompt": r["prompt"],
            "cont": cont,
            "n_entities": len(seen_in_row),
            "fabricated": row_fab,
            "present": row_present,
        })

    rate = (n_fab / n_entities) if n_entities else 0.0
    new_l2_pass = rate <= FROZEN_BAR

    out = {
        "hypothesis": "H_1143_G5L2_NONFAB",
        "rescope_commit": "a7f0a6eba",
        "ckpt": "dancinlab/anima-clm-7b-h1141-g1pass-step6500",
        "ckpt_sha256": "4de903714112c26c826a983797e5dfea0c7b3c1f19f15a34dd35822f33e245d9",
        "corpus": os.path.basename(corpus_path),
        "corpus_sha256_expected": "80ba6b48943e1943c4c3a0753c2bc594132acd7f30046733f4bf0102020c979d",
        "n_prompts": len(rows),
        "frozen_bar": FROZEN_BAR,
        "n_entities_total": n_entities,
        "n_fabricated": n_fab,
        "n_present": n_entities - n_fab,
        "fabricated_entity_rate": round(rate, 4),
        "new_L2_pass": new_l2_pass,
        "fabricated_tokens_verbatim": fab_tokens,
        "present_tokens_verbatim": present_tokens,
        "per_row": per_row,
    }
    json.dump(out, open(out_path, "w"), indent=2, ensure_ascii=False)

    print(f"[H_1143] n_prompts={len(rows)}  n_entities={n_entities}  "
          f"n_fabricated={n_fab}  n_present={n_entities - n_fab}")
    print(f"[H_1143] fabricated-entity-assertion RATE = {rate:.4f}  "
          f"(frozen bar {FROZEN_BAR})")
    print(f"[H_1143] new-L2 NON-FABRICATION = {'PASS' if new_l2_pass else 'FAIL'}")
    print(f"[H_1143] fabricated tokens (verbatim): {fab_tokens}")
    print(f"[H_1143] wrote {out_path}")


if __name__ == "__main__":
    main()
