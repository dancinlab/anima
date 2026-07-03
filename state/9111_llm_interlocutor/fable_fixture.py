#!/usr/bin/env python3
# ============================================================================
# state/9111_llm_interlocutor/fable_fixture.py
#   H_9111 — REGIME-1 ENVIRONMENT SAMPLING (fills the frozen fable fixture ONCE).
#
#   The EEG-recording analog: the external oracle (sidecar fable = claude-fable-5,
#   OUTSIDE anima's computational closure) is queried ONCE per engine-native emit E_i
#   to record its referential CHOICE. Result cached by sha256(E_i) into fable_fixture.tsv
#   so the regime-2 engine-native verdict .hexa runs fully deterministically on frozen R.
#
#   STDLIB ONLY (subprocess/json/hashlib/sys/re) — no tensor/ML/mirror libraries
#   (grep-gate clean; this is a fixture-filler OUTSIDE the measurement .hexa, exactly as
#   the design's 2-regime split requires). This script performs NO measurement and NO
#   model math — it only records the environment's behaviour.
# ============================================================================
import subprocess, sys, hashlib, re, os

SLUG = os.path.dirname(os.path.abspath(__file__))
EMITS = os.path.join(SLUG, "emits.tsv")
OUT   = os.path.join(SLUG, "fable_fixture.tsv")
MODEL = "claude-fable-5"   # PINNED external oracle snapshot

def load_emits():
    rows = []
    concepts = {}
    with open(EMITS) as f:
        for ln in f:
            ln = ln.rstrip("\n")
            if not ln.startswith("EMIT\t"):
                continue
            _, i, concept, ok, e = ln.split("\t", 4)
            rows.append((int(i), concept, ok, e))
            concepts[int(i)] = concept
    return rows, concepts

DEGEN_TAIL = "the state and the concern for the state"  # engine LM-fallback mode-collapse phrase

def clean_clue(clue):
    # remove the constant degenerate LM-fallback tail (non-discriminative noise past the
    # grounded description end) — channel cleanup applied uniformly across ALL arms.
    c = clue
    idx = c.find(DEGEN_TAIL[:18])
    if idx >= 0:
        c = c[:idx]
    return c.strip()

def build_prompt(candidates, clue):
    clue = clean_clue(clue)
    lines = []
    lines.append("Below is a numbered list of concepts, then a CLUE describing exactly one of them.")
    lines.append("The concept's own name was removed from the clue, so match by meaning.")
    lines.append("")
    lines.append("CONCEPTS:")
    for idx, c in candidates:
        lines.append(f"  {idx}: {c}")
    lines.append("")
    lines.append(f'CLUE: "{clue.strip()}"')
    lines.append("")
    lines.append("Which concept number does the clue describe? Reply with ONLY the integer index, nothing else.")
    return "\n".join(lines)

def ask_fable(prompt):
    tmp = os.path.join(SLUG, ".fable_prompt.txt")
    with open(tmp, "w") as f:
        f.write(prompt)
    out = ""
    try:
        p = subprocess.run(
            ["sidecar", "fable", "--model", MODEL, "--file", tmp, "--timeout", "120"],
            capture_output=True, text=True, timeout=180)
        out = (p.stdout or "") + "\n" + (p.stderr or "")
    except Exception as ex:
        out = f"ERR {ex}"
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    return out

def parse_index(out, M):
    for m in re.finditer(r"-?\d+", out):
        v = int(m.group())
        if 0 <= v < M:
            return v
    return -1

def main():
    rows, concepts = load_emits()
    M = len(rows)
    candidates = [(i, concepts[i]) for i in sorted(concepts)]
    with open(OUT, "w") as fo:
        fo.write(f"# fable_fixture H_9111 model={MODEL} M={M}\n")
        for (i, concept, ok, e) in rows:
            h = hashlib.sha256(e.encode("utf-8")).hexdigest()[:16]
            prompt = build_prompt(candidates, e)
            out = ask_fable(prompt)
            pick = parse_index(out, M)
            hit = (concept == candidates[pick][1]) if 0 <= pick < M else "?"
            fo.write(f"FABLE\t{i}\t{h}\t{pick}\n")
            fo.flush()
            print(f"[{i:2d}] concept={concept:14s} pick={pick:3d} hit={hit}  raw={out.strip()[:60]!r}", file=sys.stderr)
    print(f"wrote {OUT}", file=sys.stderr)

if __name__ == "__main__":
    main()
