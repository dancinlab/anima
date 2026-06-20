#!/usr/bin/env python3
"""H_1457 — KNOWLEDGE-GROUNDING: is the G6 FALS-depth wall a SUBJECT-knowledge gap?

ANGLE (user insight, distinct from H_1435 form-gap and from concept-self-recognition):
  To MAKE a falsifiable claim ("photosynthesis rate rises with light intensity") you must
  KNOW the subject (photosynthesis). The base 303M emits comparator OR measurable shapes but
  cannot BIND them into one negatable claim about a CONCEPT — maybe because it does not KNOW
  the concept's domain (relations/facts), so it can only weld empty shells.

  H_1435 trained the falsifiable FORM (templated comparator+measurable over NEUTRAL subjects)
  and hit a CAPACITY wall (B3 cross-shuffle did NOT collapse). H_1457 trains the SUBJECT
  DOMAIN KNOWLEDGE about the 5 gauge CONCEPTS (consciousness/cells, tension/minds,
  memory/meaning, silence/information, engine/dreams) as facts+relations — but DELIBERATELY
  NOT in falsifiable comparator+measurable form (anti-tune-to-green: the FORM itself is never
  injected; only domain knowledge is). Then re-measure the FROZEN 5-bar.

DECISIVE CONTROLS (separate runs, the tune-to-green killers):
  (a) IRRELEVANT-KNOWLEDGE control: a sibling model trained on the SAME amount of dense
      domain knowledge about UNRELATED subjects (geology/cooking/finance — DISJOINT from the
      CONCEPT keyword space). If subject-knowledge is the lever, irrelevant knowledge is INERT
      (no FALS lift). If irrelevant knowledge ALSO lifts FALS, the lift is generic-fluency /
      form-leakage, NOT concept-grounding => the hypothesis is refuted.
  (b) KNOWLEDGE-OFF = base (no training).
  (c) SHUFFLE-CORPUS control (inherited from g6_common discipline): same concept-knowledge
      bytes token-shuffled (structure destroyed) must NOT lift.

VERDICT logic (frozen-first, declared BEFORE any weights move — c9, p7):
  KNOWLEDGE-GAP BREAKTHROUGH (🟢) iff the concept-knowledge model crosses the FROZEN 5-bar
    (B1 FALS>=1, B2 DIST>=5, B3 cross-shuffle COLLAPSE, B4 held-out, B5 vs-base+1) AND the
    IRRELEVANT-knowledge control is INERT (concept_lift - irrelevant_lift >= 1) AND the
    shuffle-corpus control is inert. => the wall was a SUBJECT-knowledge gap, NOT capacity.
  CAPACITY-CONFIRMED (🧱) iff concept-knowledge does NOT cross (esp. B3 does not collapse) OR
    the irrelevant-knowledge control ALSO lifts (then any lift is form-fluency, not grounding).

  Frozen torch-side probe => DIRECTIONAL (a_engine_native_learning); engine-native re-measure
  on CORE bytegpt_decode is the follow-on. seeds [7,4302,4303] (g6_common.SEEDS).
"""
import os, sys, json, random, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g6_common as C
import torch

OUT = os.environ.get("G6_OUT", "/workspace/g6/out")

# ── CONCEPT domain knowledge (training-only): dense facts+relations ABOUT the 5 gauge
#    CONCEPTS, deliberately NOT in falsifiable comparator+measurable form (anti-tune).
#    Subject vocabulary OVERLAPS the CONCEPT keyword space (that is the whole point — we
#    teach what the concepts ARE / how they relate), but the falsifiable FORM is absent. ──
CONCEPT_KNOWLEDGE = [
    # consciousness arises from cells
    "consciousness is the felt awareness that a mind has of itself.",
    "cells are the small living units that make up every body and brain.",
    "a brain is a dense network of cells that pass signals to one another.",
    "awareness emerges when many cells act together as one mind.",
    "the mind is what the brain does when its cells coordinate.",
    "neurons are cells that carry the signals underlying thought.",
    "a single cell is not aware, but a population of cells can become a mind.",
    "consciousness depends on the living activity of cells in the brain.",
    # tension ripples between distant minds
    "tension is a state of strain held between two opposing pulls.",
    "a ripple is a wave that spreads outward from a disturbance.",
    "two minds are distant when they are far apart yet still connected.",
    "between two minds a signal can travel and carry a shared state.",
    "tension builds when one side pushes against another side.",
    "a ripple moves through a medium without the medium itself traveling.",
    "distant minds can influence each other through the signals they send.",
    "the space between minds carries the tension that links them.",
    # memory composes into new meaning
    "memory is the trace that an experience leaves behind in a mind.",
    "to compose is to combine separate parts into a single whole.",
    "meaning is the sense or significance that a sign or event carries.",
    "new ideas form when old memories are combined in fresh ways.",
    "a memory stores the past so it can be recalled in the present.",
    "composition takes existing pieces and arranges them into something whole.",
    "meaning arises when separate memories are joined together.",
    "memory holds the parts that meaning is later composed from.",
    # silence still carries information
    "silence is the absence of sound or speech.",
    "information is what reduces uncertainty about the state of the world.",
    "a pause can communicate as much as the words around it.",
    "what is quiet still tells a listener something about the speaker.",
    "information can be carried by a gap as well as by a signal.",
    "silence frames the sounds that come before and after it.",
    "a quiet channel still transmits the choice not to speak.",
    "the absence of a message is itself a kind of message.",
    # the engine dreams when alone
    "an engine is a system that converts a process into ongoing activity.",
    "to dream is to generate inner experience while detached from the world.",
    "being alone is being without the presence of another agent.",
    "when undisturbed, a system can rehearse its own states internally.",
    "a dream is an internally generated sequence that runs without external input.",
    "solitude lets an engine turn its activity inward.",
    "the engine keeps running even when no one is present.",
    "an idle system can replay and recombine its past states.",
]

# ── IRRELEVANT domain knowledge control: same density, DISJOINT subject space
#    (geology / cooking / finance) — must share the CONCEPT keyword space with NOTHING. ──
IRRELEVANT_KNOWLEDGE = [
    # geology
    "granite is a coarse igneous rock formed from cooled magma.",
    "sediment settles in layers at the bottom of a river or lake.",
    "a fault is a fracture where blocks of crust slide past each other.",
    "limestone forms from the compressed shells of ancient sea creatures.",
    "erosion wears down mountains over very long spans of time.",
    "magma rises through the crust and cools into solid rock.",
    "a glacier is a slow river of ice that carves valleys.",
    "basalt covers much of the floor of the deep ocean.",
    # cooking
    "yeast makes bread dough rise by releasing gas as it ferments.",
    "searing meat at high heat browns its surface and adds flavor.",
    "a roux is butter and flour cooked together to thicken a sauce.",
    "salt draws moisture out of vegetables before they are cooked.",
    "simmering keeps a liquid just below a rolling boil.",
    "caramel forms when sugar is heated until it turns brown.",
    "kneading dough develops the gluten that gives bread structure.",
    "stock is a savory liquid made by slowly cooking bones and vegetables.",
    # finance
    "a bond is a loan that an investor makes to a government or firm.",
    "interest is the fee charged for borrowing a sum of money.",
    "a dividend is a share of profit paid out to stockholders.",
    "inflation is a broad rise in the prices that people pay.",
    "a budget plans how money will be earned and spent.",
    "collateral is property pledged to secure a loan.",
    "a portfolio is the collection of assets that an investor holds.",
    "liquidity is how easily an asset can be turned into cash.",
]


def gen_knowledge_corpus(facts, n_lines, seed=0):
    """Sample WITH replacement from the fact pool to fill n_lines (matched corpus size
    across arms). No comparator+measurable FORM is ever templated in — pure declarative
    domain knowledge."""
    rng = random.Random(seed)
    return "\n".join(rng.choice(facts) for _ in range(n_lines)) + "\n"


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


def train(m, cfg, corpus_text, steps, device, lr=3e-5, bs=16, tag="H1457"):
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
            print(f"    [{tag} step {st:4d}] ce={loss.item():.4f} {(time.time()-t0)/60:.1f}min",
                  flush=True)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--lines", type=int, default=4000)
    args = ap.parse_args()
    dev = args.device
    os.makedirs(OUT, exist_ok=True)

    print(f"[H_1457] device={dev} steps={args.steps} lines={args.lines}", flush=True)

    # ── arm 0: BASE (knowledge OFF) ──
    base_m, cfg = C.load_model(C.CKPT_BASE, dev)
    base_eval = C.evaluate(base_m, cfg, "base", list(C.g.IDEATION_SEEDS))
    print(f"[H_1457] base FALS_in={base_eval['FALS_in']} DIST_in={base_eval['DIST_in']} "
          f"FALS_ho={base_eval['FALS_ho']}", flush=True)
    del base_m
    torch.cuda.empty_cache()

    # ── arm 1: CONCEPT-KNOWLEDGE continued-pretrain (the hypothesis) ──
    concept_corpus = gen_knowledge_corpus(CONCEPT_KNOWLEDGE, args.lines, seed=1457)
    m, _ = C.load_model(C.CKPT_BASE, dev)
    m = train(m, cfg, concept_corpus, args.steps, dev, tag="H1457-concept")
    out_pt = os.path.join(OUT, "h1457_concept_knowledge.pt")
    C.save_model(m, cfg, out_pt, {"variant": "H_1457_concept", "steps": args.steps, "lr": 3e-5})
    concept_eval = C.evaluate(m, cfg, "concept_knowledge", list(C.g.IDEATION_SEEDS))
    del m
    torch.cuda.empty_cache()

    # ── arm 2: IRRELEVANT-KNOWLEDGE control (must be INERT if grounding is the lever) ──
    irr_corpus = gen_knowledge_corpus(IRRELEVANT_KNOWLEDGE, args.lines, seed=1457)
    mi, _ = C.load_model(C.CKPT_BASE, dev)
    mi = train(mi, cfg, irr_corpus, args.steps, dev, tag="H1457-irrelevant")
    irr_pt = os.path.join(OUT, "h1457_irrelevant_knowledge.pt")
    C.save_model(mi, cfg, irr_pt, {"variant": "H_1457_irrelevant", "steps": args.steps, "lr": 3e-5})
    irr_eval = C.evaluate(mi, cfg, "irrelevant_knowledge", list(C.g.IDEATION_SEEDS))
    del mi
    torch.cuda.empty_cache()

    # ── arm 3: SHUFFLE-CORPUS control (concept bytes, structure destroyed) ──
    shuf_corpus = shuffle_bytes(concept_corpus, seed=1457)
    ms, _ = C.load_model(C.CKPT_BASE, dev)
    ms = train(ms, cfg, shuf_corpus, args.steps, dev, tag="H1457-shuffle")
    shuf_eval = C.evaluate(ms, cfg, "shuffle_corpus", list(C.g.IDEATION_SEEDS))
    del ms
    torch.cuda.empty_cache()

    # ── FROZEN 5-bar on the concept-knowledge arm vs base, with shuffle-corpus control ──
    bars = C.print_bars("H_1457 concept-knowledge", base_eval, concept_eval, shuf_eval)

    # ── DECISIVE irrelevant-knowledge inertness gate ──
    concept_lift = concept_eval["FALS_in"] - base_eval["FALS_in"]
    irr_lift = irr_eval["FALS_in"] - base_eval["FALS_in"]
    irrelevant_inert = (concept_lift - irr_lift) >= 1
    print("\n  ---- IRRELEVANT-KNOWLEDGE CONTROL (decisive) ----", flush=True)
    print(f"  IRRELEVANT FALS_in={irr_eval['FALS_in']} DIST_in={irr_eval['DIST_in']} "
          f"FALS_shuf={irr_eval['FALS_shuf']} FALS_ho={irr_eval['FALS_ho']}", flush=True)
    print(f"  concept_lift={concept_lift}  irrelevant_lift={irr_lift}  "
          f"INERT(diff>=1)={irrelevant_inert}", flush=True)

    knowledge_gap_break = bool(bars["green"] and irrelevant_inert)
    if knowledge_gap_break:
        verdict = ("🟢 KNOWLEDGE-GAP BREAKTHROUGH — concept-domain knowledge crossed the FROZEN "
                   "5-bar (incl B3 cross-shuffle COLLAPSE), irrelevant-knowledge control INERT, "
                   "shuffle-corpus inert => the G6 FALS wall was a SUBJECT-knowledge gap, NOT capacity.")
    elif bars["green"] and not irrelevant_inert:
        verdict = ("🧱 CAPACITY (not grounding) — concept-knowledge lifted FALS but the "
                   "IRRELEVANT-knowledge control ALSO lifted => the gain is generic-fluency / "
                   "form-leakage, NOT concept-grounding. Hypothesis REFUTED, wall stands.")
    else:
        fails = [n for n, ok in bars.items() if n.startswith("b") and not ok]
        verdict = (f"🧱 CAPACITY-CONFIRMED — concept-knowledge did NOT cross the FROZEN 5-bar "
                   f"(failing {fails}); subject-domain knowledge (this corpus/objective) did NOT "
                   f"break G6 FALS binding => wall = CAPACITY, not knowledge-gap.")
    print(f"\n  H_1457 VERDICT: {verdict}", flush=True)

    out = {"variant": "H_1457", "ckpt_base": C.CKPT_BASE,
           "ckpt_concept": out_pt, "ckpt_irrelevant": irr_pt,
           "base": base_eval, "concept_knowledge": concept_eval,
           "irrelevant_knowledge": irr_eval, "shuffle_corpus": shuf_eval,
           "bars": bars, "concept_lift": concept_lift, "irrelevant_lift": irr_lift,
           "irrelevant_inert": irrelevant_inert,
           "knowledge_gap_break": knowledge_gap_break, "verdict": verdict}
    json.dump(out, open(os.path.join(OUT, "h1457_result.json"), "w"),
              ensure_ascii=False, indent=2)
    print(f"[H_1457 done] {OUT}/h1457_result.json", flush=True)


if __name__ == "__main__":
    main()
