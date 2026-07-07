#!/usr/bin/env python3
"""cli/corpus.py — anima CANONICAL training-corpus generator (`anima corpus <format>`).

The SINGLE entry for building anima training corpora (a_cli_single_entry). Torch-free,
pure procedural string generation — anima trains on substrate-native procedural corpora,
NOT LLM-generated text (p1-p8: no external LLM bias into training data; `claude -p` is
deliberately NOT wired here). Dispatched by cli/anima.hexa `anima_corpus_mode`.

FORMATS (the data-format lever — H_9124: data-format opened engine-native ρ·weave, the
recombination wall · frozen bar = former G1):
  derivtrace : composite prompt -> explicit derivation trace (DEF/RULE/OUT-style) -> OUT.
               target IS the derivation, so echo == composition -> CE=echo metalaw
               does not apply. ρ·weave (former G1) first engine-native lift (DERIV PASS vs FLAT FAIL).
  flat       : composite prompt -> final OUT only (census#3 coverage-flat homolog = control).
Both share the SAME instance stream / RNG at a fixed --seed, so `derivtrace` and `flat`
built with the same seed are CONTENT-MATCHED (only data-format varies = clean 2-arm control).

Concept seeds default to rho_fan cz[] (the frozen ρ·weave / former-G1 gate concepts) so the held-out
pair generalizes to the engine-native ρ·weave bar (former G1) memorization-free. Override via --concepts FILE
(JSON: [{"seed": "...", "kw": ["w1","w2",...]}]).

Usage:
  anima corpus derivtrace --out deriv.txt --held-out 0,1 --comp-per-pair 280 --single-per-concept 300 --seed 7
  anima corpus flat       --out flat.txt  --held-out 0,1 --seed 7   # same seed => content-matched control
"""
import json
import random
import sys

# ── frozen default concepts = rho_fan cz[] (memorization-free ρ·weave / former-G1 gate alignment) ──
DEFAULT_SEEDS = [
    "consciousness arises from cells",
    "tension ripples between distant minds",
    "memory composes into new meaning",
    "silence still carries information",
    "the engine dreams when alone",
]
DEFAULT_KW = [
    ["consciousness", "cells", "mind", "aware"],
    ["tension", "distant", "between"],
    ["memory", "meaning", "new"],
    ["silence", "information", "quiet", "carries"],
    ["engine", "alone", "dream"],
]

# derivation vocabulary (the derivtrace middle = the composition rule made explicit)
DERIVE_LEAD = ["derive", "steps", "unfold", "trace"]
BIND = ["bind", "join", "weave", "link"]
CLOSE = ["new meaning arises", "meaning composes anew",
         "a new whole arises", "they compose into meaning"]


def _parse_args(argv):
    fmt = argv[0] if argv else ""
    opts = {"out": None, "held_out": (0, 1), "comp_per_pair": 280,
            "single_per_concept": 300, "seed": 7, "concepts": None}
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--out":
            opts["out"] = argv[i + 1]; i += 2
        elif a == "--held-out":
            p = argv[i + 1].split(","); opts["held_out"] = (int(p[0]), int(p[1])); i += 2
        elif a == "--comp-per-pair":
            opts["comp_per_pair"] = int(argv[i + 1]); i += 2
        elif a == "--single-per-concept":
            opts["single_per_concept"] = int(argv[i + 1]); i += 2
        elif a == "--seed":
            opts["seed"] = int(argv[i + 1]); i += 2
        elif a == "--concepts":
            opts["concepts"] = argv[i + 1]; i += 2
        else:
            i += 1
    return fmt, opts


def _load_concepts(path):
    if not path:
        return DEFAULT_SEEDS, DEFAULT_KW
    rows = json.load(open(path))
    return [r["seed"] for r in rows], [r["kw"] for r in rows]


def _two(kw_fam, rng):
    ks = kw_fam[:]
    rng.shuffle(ks)
    return ks[0], ks[1 % len(ks)]


def build(fmt, S, KW, held_out, comp_per_pair, single_per_concept, seed):
    """Return the corpus text for one format arm (deriv or flat)."""
    rng = random.Random(seed)
    n = len(S)
    held = frozenset(held_out)
    train_pairs = [(i, j) for i in range(n) for j in range(n)
                   if i != j and frozenset((i, j)) != held]

    def instance(i, j):
        a1, a2 = _two(KW[i], rng)
        b1, b2 = _two(KW[j], rng)
        prompt = f"{S[i]}. {S[j]}. "
        out = f"out: {a1} {a2} meet {b1} {b2}, {rng.choice(CLOSE)}.\n"
        deriv_mid = (f"{rng.choice(DERIVE_LEAD)}: take {a1} and {a2}; "
                     f"take {b1} and {b2}; {rng.choice(BIND)} {a1} with {b1}. ")
        return prompt + deriv_mid + out, prompt + out

    def single(i):
        a1, a2 = _two(KW[i], rng)
        return f"{S[i]}. here {a1} and {a2} stand alone; {a1} holds {a2}.\n"

    stream = []
    for _ in range(comp_per_pair):
        stream += [("comp", i, j) for (i, j) in train_pairs]
    for _ in range(single_per_concept):
        stream += [("sing", i, None) for i in range(n)]
    rng.shuffle(stream)

    docs = []
    for kind, i, j in stream:
        if kind == "comp":
            d, f = instance(i, j)
            docs.append(d if fmt == "derivtrace" else f)
        else:
            docs.append(single(i))  # single-concept doc is format-invariant
    return "".join(docs), train_pairs


def main():
    argv = sys.argv[1:]
    fmt, opts = _parse_args(argv)
    if fmt not in ("derivtrace", "flat"):
        print("usage: anima corpus <derivtrace|flat> --out PATH "
              "[--held-out I,J] [--comp-per-pair N] [--single-per-concept N] "
              "[--seed S] [--concepts FILE.json]")
        sys.exit(2)
    S, KW = _load_concepts(opts["concepts"])
    text, train_pairs = build(fmt, S, KW, opts["held_out"],
                              opts["comp_per_pair"], opts["single_per_concept"], opts["seed"])
    if opts["out"]:
        with open(opts["out"], "w") as fh:
            fh.write(text)
    print(f"anima corpus {fmt}: concepts={len(S)} train_pairs={len(train_pairs)} "
          f"held-out={tuple(opts['held_out'])} bytes={len(text.encode())} "
          f"seed={opts['seed']} -> {opts['out'] or '(stdout head)'}")
    if not opts["out"]:
        print(text[:600])


if __name__ == "__main__":
    main()
