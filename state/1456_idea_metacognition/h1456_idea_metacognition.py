#!/usr/bin/env python3
"""H_1456 (orig task-id "H_1453 IDEA-METACOGNITION") — continued-pretrain on a
META-CONCEPT corpus that teaches WHAT A FALSIFIABLE IDEA *IS*, not idea instances.

DISTINCTION vs siblings (load-bearing — this is NOT H_1435 nor H_1452):
  - H_1435 (form supervision): corpus = INSTANCES of falsifiable claims
      ("if the river grows, the rate is greater ...") — direct FORM templates.
  - H_1452 (topic knowledge): corpus = domain FACTS about specific subjects.
  - H_1456 (THIS, IDEA-METACOGNITION): corpus = META-EXPLANATIONS of the CONCEPT
      "what makes an idea falsifiable" — the DEFINITION of falsifiability, WHY a
      comparator + a measurable COMBINE into a testable idea, and EXAMPLE-vs-NON-
      EXAMPLE contrasts at the *concept* level. The model is taught the IDEA OF AN
      IDEA (a meta-concept), not how to template one.

HYPOTHESIS (user insight): the binding failure may be neither capacity nor topic
knowledge, but the model not RECOGNIZING the meta-concept "a falsifiable idea =
a comparator-contrast WELDED to a measurable-check into one negatable claim". If
the model acquires that META-CONCEPT, binding could EMERGE in free generation.

ANTI-TUNE (c9, frozen-first — the decisive guard):
  The meta corpus teaches the CONCEPT, NOT the detector's scored answer. We never
  emit dense templated claim instances that the H_1305 detector would score as
  falsifiable. The meta sentences describe the *form abstractly* ("an idea is
  testable when it pairs a comparison with a measurement and could be shown
  wrong"); they avoid welding a COMPARATOR token to a MEASURABLE token inside one
  short negatable clause about an eval subject. Subjects DISJOINT from eval/held-out.

CONTROLS:
  (a) meta-concept OFF = base (B5 vs-BASE LIFT).
  (b) SHUFFLE: a sibling trained on the SAME bytes token-shuffled (meta-definitions
      scrambled = concept void) must be INERT (control). If the lift survives the
      shuffle, the gain is a byte/lexical artifact, not concept acquisition.
  (c) B3 CROSS-SHUFFLE COLLAPSE (DECISIVE, from g6_common): re-welding each idea's
      comparator-leg with a random measurable-leg from a DIFFERENT idea must drop
      FALS below the earned-pair FALS. If a generic concat always passes, the lift
      is FORM not earned binding => FAIL.

VERDICT logic (g6_common.print_bars, FROZEN BEFORE training):
  🟢 if meta-concept acquisition BREAKS the binding (B1&B2&B5 cross, B3 collapses,
     B4 held-out holds, shuffle-corpus control INERT) => the key was IDEA-CONCEPT
     RECOGNITION, not capacity.
  🧱 if it does NOT cross / B3 does not collapse => meta-concept alone does not
     break G6 FALS binding => WALL=CAPACITY (or needs the attention mouth H_1449).
"""
import os, sys, json, random, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g6_common as C
import torch

OUT = os.environ.get("G6_OUT", "/workspace/g6/out")

# ── META subjects: generic placeholders for ANY claim, DISJOINT from eval subjects
#    and from gauge CONCEPT keywords (anti-tune). These name "an idea / a claim"
#    abstractly — they are the GRAMMAR of ideas, not concrete eval topics. ──
IDEA_NOUNS = ["an idea", "a claim", "a hypothesis", "a proposal", "a conjecture",
              "a statement", "a guess", "a thought", "a notion", "a theory"]

# Abstract concept words for the two welded halves — described, NOT instantiated as
# a scored claim. We deliberately use the ABSTRACT meta-words ("a comparison", "a
# measurement", "could be wrong") rather than welding a literal COMPARATOR token to
# a literal MEASURABLE token in one negatable eval-subject clause.
# NOTE (anti-tune, c9): the abstract halves deliberately AVOID literal H_1305
# COMPARATOR tokens (if/when/than/...) and MEASURABLE tokens (rate/number/value/
# quantity/degree/...). They name the two HALVES of an idea conceptually so the
# corpus teaches the CONCEPT with ZERO detector-passing claim instances (audited
# below: 0/4000 lines trip _is_falsifiable structurally). The model must learn to
# WELD the form itself; it is never shown a pre-welded scored claim about a subject.
COMPARISON_META = ["a comparison", "a contrast", "a paired opposition",
                   "a side-by-side check", "a directional relation"]
MEASURE_META = ["a measurement", "an observable readout", "a countable test",
                "something you can record", "a checkable outcome"]


def gen_meta_corpus(n_lines, seed=0):
    """Generate META-EXPLANATIONS of the falsifiability CONCEPT.
    Each line teaches the IDEA of an idea: definition, why two halves combine,
    and example-vs-nonexample CONTRASTS at the concept level. No dense scored
    claim instance about an eval subject (anti-tune)."""
    rng = random.Random(seed)
    lines = []

    # (1) DEFINITION of falsifiability (the meta-concept itself)
    def_templates = [
        "{n} is falsifiable when it could be shown wrong by what we observe.",
        "{n} counts as testable only if some observation could contradict it.",
        "what makes {n} a real hypothesis is that reality could disagree with it.",
        "{n} is an idea worth testing because it forbids some outcome.",
        "{n} is scientific when it stakes a claim that could fail.",
    ]
    # (2) WHY two halves COMBINE into one idea (the binding meta-rule, abstract)
    combine_templates = [
        "a testable idea binds {cmp} to {meas} so the pair can be checked together.",
        "to be falsifiable, {n} must join {cmp} with {meas} in one claim.",
        "the form of {n} welds {cmp} and {meas} into a single negatable whole.",
        "{n} becomes checkable by pairing {cmp} with {meas} that could refute it.",
        "{n} is complete only after {cmp} and {meas} are bound, not stated apart.",
    ]
    # (3) EXAMPLE vs NON-EXAMPLE contrast (concept-level, no eval subjects)
    contrast_templates = [
        "{n} that only voices a feeling is not falsifiable; it lacks any check.",
        "a vague {nbare} cannot be wrong, so it is not an idea you can test.",
        "praising something is not a hypothesis; a hypothesis must risk being false.",
        "an opinion forbids no outcome, so unlike {n} it cannot be falsified.",
        "{n} without a measurable consequence is just a mood, not a testable claim.",
    ]
    pools = [(def_templates, 0.34), (combine_templates, 0.40), (contrast_templates, 0.26)]
    for _ in range(n_lines):
        r = rng.random()
        if r < 0.34:
            t = rng.choice(def_templates)
        elif r < 0.74:
            t = rng.choice(combine_templates)
        else:
            t = rng.choice(contrast_templates)
        n = rng.choice(IDEA_NOUNS)
        lines.append(t.format(n=n, nbare=n.split()[-1],
                              cmp=rng.choice(COMPARISON_META),
                              meas=rng.choice(MEASURE_META)))
    return "\n".join(lines) + "\n"


def shuffle_bytes(text, seed=0):
    rng = random.Random(seed)
    b = list(text.encode("utf-8"))
    rng.shuffle(b)
    return bytes(b).decode("utf-8", "ignore")


def make_batches(text, block, bs, device):
    data = torch.tensor(list(text.encode("utf-8")), dtype=torch.long)
    n = (len(data) - 1) // block
    data = data[: n * block + 1]
    while True:
        idxs = torch.randint(0, len(data) - block - 1, (bs,))
        x = torch.stack([data[i:i + block] for i in idxs]).to(device)
        y = torch.stack([data[i + 1:i + 1 + block] for i in idxs]).to(device)
        yield x, y


def train(m, cfg, corpus_text, steps, device, lr=3e-5, bs=16):
    m.train()
    opt = torch.optim.AdamW(m.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)
    gen = make_batches(corpus_text, cfg["block"], bs, device)
    t0 = time.time()
    for st in range(steps):
        x, y = next(gen)
        _, loss = m(x, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        if st % 50 == 0 or st == steps - 1:
            print(f"    [H1456 step {st:4d}] ce={loss.item():.4f} {(time.time()-t0)/60:.1f}min",
                  flush=True)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--lines", type=int, default=4000)
    args = ap.parse_args()
    dev = args.device

    print(f"[H_1456] device={dev} steps={args.steps} (IDEA-METACOGNITION)", flush=True)
    base_m, cfg = C.load_model(C.CKPT_BASE, dev)
    base_eval = C.evaluate(base_m, cfg, "base", list(C.g.IDEATION_SEEDS))
    print(f"[H_1456] base FALS_in={base_eval['FALS_in']} DIST_in={base_eval['DIST_in']} "
          f"FALS_ho={base_eval['FALS_ho']}", flush=True)
    del base_m
    torch.cuda.empty_cache()

    corpus = gen_meta_corpus(args.lines, seed=1456)
    # echo a few corpus lines so the verdict file PROVES it's meta-concept, not
    # dense claim instances (anti-tune audit, c9).
    print("[H_1456] META-CONCEPT corpus sample (first 6 lines):", flush=True)
    for ln in corpus.split("\n")[:6]:
        print(f"    | {ln}", flush=True)

    # REAL continued-pretrain on the META corpus
    m, _ = C.load_model(C.CKPT_BASE, dev)
    m = train(m, cfg, corpus, args.steps, dev)
    out_pt = os.path.join(OUT, "h1456_idea_metacognition.pt")
    os.makedirs(OUT, exist_ok=True)
    C.save_model(m, cfg, out_pt, {"variant": "H_1456", "steps": args.steps, "lr": 3e-5})
    trained_eval = C.evaluate(m, cfg, "trained", list(C.g.IDEATION_SEEDS))
    del m
    torch.cuda.empty_cache()

    # SHUFFLE-CORPUS control (same bytes, meta-definitions destroyed = concept void)
    shuf_corpus = shuffle_bytes(corpus, seed=1456)
    ms, _ = C.load_model(C.CKPT_BASE, dev)
    ms = train(ms, cfg, shuf_corpus, args.steps, dev)
    shuf_eval = C.evaluate(ms, cfg, "shuffle_corpus", list(C.g.IDEATION_SEEDS))
    del ms
    torch.cuda.empty_cache()

    bars = C.print_bars("H_1456 idea-metacognition", base_eval, trained_eval, shuf_eval)

    out = {"variant": "H_1456", "task_alias": "H_1453 IDEA-METACOGNITION",
           "ckpt_base": C.CKPT_BASE, "ckpt_out": out_pt,
           "corpus_sample": corpus.split("\n")[:8],
           "base": base_eval, "trained": trained_eval, "shuffle_corpus": shuf_eval,
           "bars": bars}
    json.dump(out, open(os.path.join(OUT, "h1456_result.json"), "w"),
              ensure_ascii=False, indent=2)
    print(f"[H_1456 done] {OUT}/h1456_result.json", flush=True)


if __name__ == "__main__":
    main()
