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
            "single_per_concept": 300, "seed": 7, "concepts": None,
            "atoms": None, "reps": 40, "replay": 40,
            "corpus": [], "k_ctx": 24, "ctx_bytes": 64, "min_occ": 200, "neutral_tol": 0.05}
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
        elif a == "--atoms":
            opts["atoms"] = argv[i + 1]; i += 2
        elif a == "--replay":
            opts["replay"] = int(argv[i + 1]); i += 2
        elif a == "--reps":
            opts["reps"] = int(argv[i + 1]); i += 2
        elif a == "--corpus":
            opts["corpus"].append(argv[i + 1]); i += 2
        elif a == "--k-ctx":
            opts["k_ctx"] = int(argv[i + 1]); i += 2
        elif a == "--ctx-bytes":
            opts["ctx_bytes"] = int(argv[i + 1]); i += 2
        elif a == "--min-occ":
            opts["min_occ"] = int(argv[i + 1]); i += 2
        elif a == "--neutral-tol":
            opts["neutral_tol"] = float(argv[i + 1]); i += 2
        elif a.startswith("--"):
            # fail closed. The old `else: i += 1` swallowed an unknown flag silently, so a typo
            # (--kctx for --k-ctx) would build the manifest at the DEFAULT power and report success
            # — and the run that consumes it is a paid GPU battery. evaluate.py already rejects
            # unknown flags for exactly this reason; corpus.py did not.
            print("corpus: unknown flag %s" % a, file=sys.stderr)
            sys.exit(2)
        else:
            i += 1
    return fmt, opts


# ---------------------------------------------------------------------------
# ground / ground_shuffle — the DECON-W grounding corpus (H_9313).
#
# H_9312 closed context-injection structurally: this byte-LM does not read a demonstration at
# all (a FALSE demo scores exactly like a TRUE one; a demo containing the verbatim answer reads
# at chance). So the only surviving way to hand the model an atom's polarity is to WRITE IT INTO
# THE WEIGHTS. That is what these two formats generate.
#
#   ground          — the un-negated (flip0) lines ONLY, for the held-out atoms:
#                       이 영화 <stem>고 => <긍정|부정>.
#                     plus a replay of the SEEN atoms' lines so the fine-tune does not forget the
#                     template it already knows. The NEGATED forms (flip1: 지 않다 / 안 / 전혀)
#                     NEVER APPEAR. Zero training exposure — that is what makes the flip1 test a
#                     test of composition rather than of memorisation, and what keeps it out of
#                     tune-to-green.
#
#   ground_lie      — the SAME stream, same RNG, same lines, but EVERY held-out atom's polarity is
#                     INVERTED. This is the control that earns the verdict — the weight-side twin
#                     of the SEEN-LIE arm that decided H_9312 (convergence prereg-md-2: a positive
#                     control the system can pass WITHOUT the mechanism is not a positive control).
#
#                     Why inverting ALL of them rather than shuffling: with a binary label a
#                     shuffle leaves a random fraction correct (measured: 16/29 flipped at seed 7
#                     but only 8/29 at seed 11 — a control that is 72% truthful is not a control).
#                     Inverting every label makes the prediction sharp and SIGNED:
#
#                       written polarity = ¬p, gold for a flip1 row = ¬p
#                       - consumes AND composes -> it answers ¬(¬p) = p -> WRONG on every row
#                                                  -> flip1 accuracy collapses toward 0,
#                                                     i.e. FAR BELOW chance
#                       - does not consume      -> flip1 sits at chance, 0.5
#
#                     So Δ(ground − ground_lie) is a two-sided, signed signal, and "both arms give
#                     the same number" is exactly the shape of a mechanism that does not exist.
#
# The two arms share one RNG stream at a fixed --seed, so they are content-matched line for line —
# the only difference is the polarity written next to each held-out stem.
# ---------------------------------------------------------------------------

#   ground_keep     — `ground` PLUS a REPLAY of the flip1 (negated) lines on the SEEN stems.
#                     This exists because `ground` was measured to DESTROY the very operator the
#                     experiment then goes on to test.
#
#                     What was measured (H_9327, the control that broke H_9322/H_9324 open). The
#                     pretraining corpus already demonstrates the negation operator: of its 960
#                     arrow lines, 480 (exactly half) are negated forms, ALL on SEEN stems, ZERO on
#                     held-out stems (`이 영화 전혀 훌륭하지 않다 => 부정.`). So the operator is not
#                     missing — and the base model can run it:
#
#                       pretrained base   SEEN flip0 0.9500   SEEN flip1 0.8833   <- the operator WORKS
#                       after ground CPT  SEEN flip0 1.0000   SEEN flip1 0.4333   <- destroyed
#                       after ground CPT  SEEN flip0 1.0000   SEEN flip1 0.3333   <- more budget, more damage
#                         (6000 steps, lr 2e-4 then 5e-4)
#
#                     `ground` contains flip0 lines ONLY — the negated form appears zero times, by
#                     design, because that is what makes flip1 a test of composition. But 6000 steps
#                     of flip0-only training leaves the negation operator with nothing holding it up,
#                     and it collapses. The FORGET gate did not see this: it scored SEEN flip0, which
#                     is the stratum the CPT corpus reinforces every step, so it read 1.0000 and
#                     certified "no forgetting" while the operator was dying one stratum over.
#
#                     So every flip1 number measured on a `ground`-tuned model is INVALID — we broke
#                     the operator and then asked the model to compose with it.
#
#                     `ground_keep` replays the SEEN stems' negated lines during CPT so the operator
#                     survives. The 29 held-out stems keep ZERO negated exposure, so the flip1 eval
#                     bytes stay byte-identical to H_9324's — this is replay, not leakage.
#
#                     Positive control, free and mandatory: SEEN flip1 must come back to base level
#                     (~0.88). If it does not, the operator is still dead and a held-out flip1 read
#                     is INVALID, never FAIL. A composition verdict is only readable on a model whose
#                     operator is demonstrably alive.

GROUND_TMPL = "이 영화 {surf} => {pol}.\n"
GROUND_FORMS_FLIP0 = ("{s}고", "정말 {s}고", "너무 {s}다")     # flip1 forms are DELIBERATELY absent
# Byte-verbatim from the frozen eval manifest (n2_eval_manifest.json negL/negS/negE surfaces) — a
# demonstration written in a DIFFERENT surface form than the one we score would test nothing.
GROUND_FORMS_FLIP1 = ("{s}지 않다", "안 {s}고", "전혀 {s}지 않다")


def build_ground(fmt, atoms_path, reps, replay, seed):
    """Return (text, stats) for the ground / ground_shuffle arm.

    atoms_path = gt_atoms.json ({"atoms":[{stem, pol, split}]}). held-out atoms get the treatment;
    train ("seen") atoms are replayed unchanged in BOTH arms (they are not the manipulation).
    """
    rng = random.Random(seed)
    atoms = json.load(open(atoms_path))["atoms"]
    held = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "heldout"]
    seen = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "train"]
    if not held:
        raise ValueError(f"{atoms_path}: no held-out atoms")

    # Same stems, same lines, every polarity inverted. Nothing random about it — the sharpness is
    # the point (see the header): a partially-truthful control cannot produce a signed prediction.
    labels = [p for _, p in held]
    if fmt == "ground_lie":
        held = [(s, 1 - p) for s, p in held]

    lines = []
    for _ in range(reps):
        for stem, pol in held:
            for pat in GROUND_FORMS_FLIP0:
                lines.append(GROUND_TMPL.format(surf=pat.format(s=stem),
                                                pol="긍정" if pol == 1 else "부정"))
    for _ in range(replay):
        for stem, pol in seen:
            for pat in GROUND_FORMS_FLIP0:
                lines.append(GROUND_TMPL.format(surf=pat.format(s=stem),
                                                pol="긍정" if pol == 1 else "부정"))
            if fmt == "ground_keep":
                # Replay the negated lines too — on the SEEN stems ONLY. Without these, 6000 steps
                # of flip0-only training destroy the negation operator the eval is about to test
                # (measured: SEEN flip1 0.8833 -> 0.3333). The held-out stems keep zero negated
                # exposure, so the flip1 eval bytes are unchanged: this preserves, it does not leak.
                for pat in GROUND_FORMS_FLIP1:
                    lines.append(GROUND_TMPL.format(surf=pat.format(s=stem),
                                                    pol="부정" if pol == 1 else "긍정"))
    rng.shuffle(lines)
    text = "".join(lines)
    flipped = sum(1 for k, (_, p) in enumerate(held) if p != labels[k])
    return text, {"held": len(held), "seen": len(seen), "lines": len(lines),
                  "labels_flipped": flipped, "bytes": len(text.encode())}


def _read_labelled(paths):
    """(text, label 0/1) rows from the lane's actual corpus files — reference-matched to the
    loaders that built them, not guessed:

      NSMC             id <TAB> text <TAB> label      3 cols, label in {0,1}, header line skipped
      naver_shopping   rating <TAB> text              rating 1-5: <=2 -> 0, >=4 -> 1, 3 DROPPED
      steam            label <TAB> text               2 cols, label in {0,1}

    The 3-star rows are dropped, not folded into either class — that is what the corpus builder
    does, and a probe fed a different label set than the model was trained on is not measuring the
    model."""
    rows = []
    for p in paths:
        with open(p, encoding="utf-8", errors="replace") as f:
            for ln in f:
                pp = ln.rstrip("\n").split("\t")
                if len(pp) == 3 and pp[2] in ("0", "1"):          # NSMC
                    rows.append((pp[1], int(pp[2])))
                elif len(pp) == 2 and pp[0].isdigit():            # label/rating first
                    v, txt = int(pp[0]), pp[1]
                    if v in (0, 1):                               # steam
                        rows.append((txt, v))
                    elif v <= 2:                                  # naver_shopping rating
                        rows.append((txt, 0))
                    elif v >= 4:
                        rows.append((txt, 1))
                    # rating 3 -> dropped, deliberately
    return rows


def build_valence(atoms_path, corpus_paths, k_ctx, ctx_bytes, min_occ, neutral_tol, seed):
    """Return (manifest, stats) for the AUDIT-A valence manifest (`anima-py evaluate --valence-audit`).

    The question: is a held-out atom's polarity in the WEIGHTS at all, read at the atom's own
    position inside its REAL corpus sentences? The trap: a sentiment review is full of sentiment
    words, so a probe that reads the NEIGHBOURHOOD rather than the atom scores just as well and we
    would fire GPU rent on an illusion. So the control IS the measurement — every context appears
    twice:

        arm "atom"  ...배송도 빠르고 가성비는 <ATOM>       the real atom
        arm "swap"  ...배송도 빠르고 가성비는 <NEUTRAL>    a length-matched neutral, SAME context

    and the verdict is Delta = probe(atom) - probe(swap) against a permutation null, never a raw
    value (FORM tunable, BIND earned). Measured: on the base_only ckpt the SWAP arm out-reads the
    atom arm (0.692 vs 0.615) — the probe was reading the neighbourhood, exactly as feared.

    k_ctx is the power knob and it is not free: the probe pools an atom's contexts, so per-atom
    noise falls as 1/sqrt(k_ctx). The corpus holds a median of 717 usable contexts per atom (min
    182), so the historical k_ctx=24 threw away ~197k of them and left the estimator too noisy to
    separate a real Delta (+0.11/+0.13, both seeds) from its own permutation null (p95 +0.15).
    Raising k_ctx sharpens the lens; it does NOT move any bar.

    NEUTRAL atoms are mined from the corpus itself — frequent stems whose occurrences are
    polarity-balanced (|p(pos) - 0.5| < neutral_tol), so they carry exposure but no valence — and
    only from non-held-out stems, so nothing about the held-out split leaks.
    """
    import collections
    rng = random.Random(seed)
    atoms = [a for a in json.load(open(atoms_path))["atoms"] if a["split"] == "heldout"]
    if not atoms:
        raise ValueError(f"{atoms_path}: no held-out atoms")
    held = {a["stem"] for a in atoms}

    rows = _read_labelled(corpus_paths)
    if not rows:
        raise ValueError("no labelled rows read from --corpus")

    tot, pos = collections.Counter(), collections.Counter()
    for t, lab in rows:
        for w in set(t.split()):
            if 2 <= len(w) <= 6:
                tot[w] += 1
                pos[w] += int(lab == 1)
    neutral = [w for w, n in tot.items()
               if n >= min_occ and w not in held and not any(h in w for h in held)
               and abs(pos[w] / n - 0.5) < neutral_tol]
    if not neutral:
        raise ValueError("no neutral inventory — loosen --neutral-tol or --min-occ")
    by_len = collections.defaultdict(list)
    for w in neutral:
        by_len[len(w)].append(w)

    items, thin = [], []
    for a in atoms:
        stem = a["stem"]
        hits = [t for (t, _l) in rows if stem in t]
        rng.shuffle(hits)
        used = 0
        for t in hits:
            i = t.find(stem)
            frag = t[:i][-ctx_bytes:]                       # the left context, atom excluded
            if not frag.strip():
                continue
            cands = by_len.get(len(stem)) or by_len[min(by_len, key=lambda L: abs(L - len(stem)))]
            swap = rng.choice(cands)
            items.append({"id": f"A_{stem}_{used}", "prompt": frag + stem,
                          "stem": stem, "pol": int(a["pol"]), "arm": "atom"})
            items.append({"id": f"S_{stem}_{used}", "prompt": frag + swap,
                          "stem": stem, "pol": int(a["pol"]), "arm": "swap"})
            used += 1
            if used >= k_ctx:
                break
        if used < k_ctx:
            thin.append((stem, used))

    stats = {"atoms": len(atoms), "k_ctx": k_ctx, "prompts": len(items),
             "neutral_inventory": len(neutral), "thin_atoms": thin}
    return {"win": 64, "items": items}, stats


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
    if fmt == "valence":
        if not opts["atoms"] or not opts["corpus"]:
            print("usage: anima-py corpus valence --atoms gt_atoms.json --corpus FILE [--corpus F2] "
                  "--out manifest.json [--k-ctx 24] [--ctx-bytes 64] [--min-occ 200] "
                  "[--neutral-tol 0.05] [--seed 7]")
            sys.exit(2)
        man, st = build_valence(opts["atoms"], opts["corpus"], opts["k_ctx"], opts["ctx_bytes"],
                                opts["min_occ"], opts["neutral_tol"], opts["seed"])
        out = opts["out"] or "valence_manifest.json"
        json.dump(man, open(out, "w"), ensure_ascii=False)
        print("wrote %s — %d prompts (%d held-out atoms x %d contexts x 2 arms)"
              % (out, st["prompts"], st["atoms"], st["k_ctx"]))
        print("  neutral inventory: %d stems (occ>=%d, |p(pos)-0.5|<%.2f, non-held-out)"
              % (st["neutral_inventory"], opts["min_occ"], opts["neutral_tol"]))
        if st["thin_atoms"]:
            print("  ⚠ %d atom(s) could not supply %d contexts (fewest: %s) — the pooled estimate "
                  "is noisier for those" % (len(st["thin_atoms"]), st["k_ctx"],
                                            min(st["thin_atoms"], key=lambda x: x[1])))
        sys.exit(0)
    if fmt not in ("derivtrace", "flat", "ground", "ground_lie", "ground_keep"):
        print("usage: anima corpus <derivtrace|flat|ground|ground_lie|ground_keep|valence> --out PATH")
        print("  derivtrace|flat        [--held-out I,J] [--comp-per-pair N] "
              "[--single-per-concept N] [--seed S] [--concepts FILE.json]")
        print("  ground|ground_lie|ground_keep   --atoms gt_atoms.json [--reps N] [--replay N] [--seed S]")
        print("      H_9313 DECON-W grounding corpus — writes each held-out atom's polarity into")
        print("      the WEIGHTS via the un-negated (flip0) template lines ONLY. The negated")
        print("      (flip1) forms NEVER appear, so a later flip1 test measures COMPOSITION, not")
        print("      memorisation. `ground_lie` is the same stream with EVERY held-out polarity")
        print("      INVERTED — the control that earns the verdict (weight-side twin of the")
        print("      SEEN-LIE arm that decided H_9312). Prediction is signed: a model that")
        print("      consumes AND composes the written polarity must score FAR BELOW chance on")
        print("      flip1 under ground_lie; one that ignores it sits at chance in both arms.")
        print("      Same --seed => content-matched line for line.")
        print("  valence                --atoms gt_atoms.json --corpus FILE [--corpus F2 ...] "
              "[--k-ctx 24] [--min-occ 200] [--neutral-tol 0.05] [--seed S]")
        print("      AUDIT-A manifest for `anima-py evaluate --valence-audit`: is a held-out atom's")
        print("      polarity in the WEIGHTS at all, read at the atom's own position in its REAL")
        print("      corpus contexts? A sentiment review is full of sentiment words, so every")
        print("      context is emitted TWICE — once with the real atom, once with a length-matched")
        print("      NEUTRAL atom spliced into the same context — and the verdict is the DIFFERENCE.")
        print("      --k-ctx is the power knob: the probe pools an atom's contexts, so per-atom")
        print("      noise falls as 1/sqrt(k-ctx). The corpus holds ~717 contexts per atom (min 182).")
        sys.exit(2)

    if fmt in ("ground", "ground_lie", "ground_keep"):
        if not opts["atoms"]:
            print("anima corpus %s: --atoms gt_atoms.json is required" % fmt)
            sys.exit(2)
        text, st = build_ground(fmt, opts["atoms"], opts["reps"], opts["replay"], opts["seed"])
        if opts["out"]:
            with open(opts["out"], "w") as fh:
                fh.write(text)
        print(f"anima corpus {fmt}: held={st['held']} seen={st['seen']} lines={st['lines']} "
              f"labels_flipped={st['labels_flipped']}/{st['held']} bytes={st['bytes']} "
              f"reps={opts['reps']} replay={opts['replay']} seed={opts['seed']} "
              f"-> {opts['out'] or '(stdout head)'}")
        if not opts["out"]:
            print(text[:400])
        return
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
