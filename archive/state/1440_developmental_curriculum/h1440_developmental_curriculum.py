#!/usr/bin/env python3
"""H_1440 — DEVELOPMENTAL multi-task curriculum (comparator -> measurable -> bind, SEQUENTIAL).

BIO LENS (a_no_llm_frame_trap): language acquisition is SEQUENTIAL, not simultaneous —
one-word -> two-word -> simple-syntax -> embedded-syntax. The prior training-side digs
co-trained or co-rewarded the legs (H_1435 data-only, H_1436 SIMULTANEOUS co-occurrence
aux that SATURATED step-0 = informative-null, H_1437 form-supervision). H_1440 asks the
DEVELOPMENTAL question: does a STAGED curriculum — first master the comparator FORM in
isolation, THEN master the measurable FORM in isolation, THEN bind the two — teach
idea-SPECIFIC binding (the cross-shuffle-COLLAPSE bar B3 the prior 4 digs all failed)
where the SIMULTANEOUS objective (H_1436) could not?

PHASES (order FROZEN before run, c9 — post-hoc re-ordering forbidden):
  phase1 COMPARATOR-FORM only : corpus of comparative clauses, NO measurable token.
  phase2 MEASURABLE-FORM only : corpus of measurement clauses, NO comparator token.
  phase3 BIND                 : corpus welding BOTH into one negatable claim.
Each phase = a fixed step budget on its OWN corpus, sequentially (phase2 starts from the
phase1 weights, phase3 from the phase2 weights). Scaffolding: each phase is the
precondition of the next.

CONTROLS:
  CURRICULUM-ORDER-SHUFFLE (the developmental-hypothesis killer): SAME three phase-corpora,
    SAME total step budget, but the phase ORDER is RANDOMIZED (e.g. bind->comparator->
    measurable). If the staged ORDER is what teaches binding, the order-shuffle arm must
    NOT show the B3 cross-shuffle collapse. If order is irrelevant (order-shuffle == staged),
    the developmental hypothesis is FALSIFIED (it was just total exposure, not stages).
  SHUFFLE-CORPUS (token-shuffled bytes, structure destroyed): standard tune-to-green killer,
    SAME as H_1435/1436. Lift there = artifact => INVALID.

anti-tune-to-green: the comparator/measurable corpus subjects are DISJOINT from the gauge
CONCEPT keywords + eval seeds + held-out seeds; the FROZEN H_1305 _is_falsifiable detector
is reused VERBATIM; NO detector token is authored into training targets.

FROZEN 5-bar IDENTICAL to H_1435 (B1 FALS>=1, B2 DIST>=5, B3 cross-shuffle COLLAPSE,
B4 held-out, B5 vs-base). + CTRL shuffle-corpus + CURRICULUM-ORDER-SHUFFLE arm reported.
"""
import os, sys, json, random, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g6_common as C
import torch

# reuse H_1435 corpus utilities VERBATIM (same byte-batch + shuffle-bytes machinery)
import h1435_continued_pretrain as base1435
shuffle_bytes = base1435.shuffle_bytes
make_batches = base1435.make_batches

OUT = os.environ.get("G6_OUT", "/workspace/g6/out")

# training-only subjects DISJOINT from gauge CONCEPTs / eval / held-out seeds
TRAIN_SUBJECTS = ["the river", "a metal bar", "the crowd", "this alloy", "the signal",
                  "a colony", "the market", "that current", "the sample", "a fold"]
COMPS = sorted(C.COMPARATOR)
MEAS = sorted(C.MEASURABLE)


# ──────────────────────────────────────────────────────────────────────────────
# PHASE CORPORA — each phase isolates ONE form (developmental staging).
# ──────────────────────────────────────────────────────────────────────────────
def gen_comparator_corpus(n_lines, seed=0):
    """phase1: comparative clauses with a COMPARATOR token, NO measurable token."""
    rng = random.Random(seed)
    templates = [
        "{s} is {c} {s2} when the input rises.",
        "if {s} grows, it becomes {c} than before.",
        "{s} stays {c} {s2} under steady load.",
        "whenever {s} shifts, it turns {c} {s2}.",
        "{s} reads {c} compared with {s2} today.",
    ]
    lines = []
    for _ in range(n_lines):
        t = rng.choice(templates)
        lines.append(t.format(s=rng.choice(TRAIN_SUBJECTS),
                              s2=rng.choice(TRAIN_SUBJECTS),
                              c=rng.choice(COMPS)))
    return "\n".join(lines) + "\n"


def gen_measurable_corpus(n_lines, seed=0):
    """phase2: measurement clauses with a MEASURABLE token, NO comparator token."""
    rng = random.Random(seed)
    templates = [
        "the {m} of {s} was recorded at noon.",
        "we logged the {m} of {s} every hour.",
        "{s} has a {m} that the sensor reports.",
        "the {m} of {s} held near its baseline.",
        "the instrument shows the {m} of {s} clearly.",
    ]
    lines = []
    for _ in range(n_lines):
        t = rng.choice(templates)
        lines.append(t.format(s=rng.choice(TRAIN_SUBJECTS), m=rng.choice(MEAS)))
    return "\n".join(lines) + "\n"


def gen_bind_corpus(n_lines, seed=0):
    """phase3: BIND — one negatable claim joining comparator + measurable (== H_1435 corpus)."""
    rng = random.Random(seed)
    templates = [
        "if {s} grows, the {m} {c} than before.",
        "{s} {c} a higher {m} when the input rises.",
        "the {m} of {s} is greater whenever {s2} {c}.",
        "{s} shows a lower {m} than {s2} under load.",
        "when {s} {c}, its {m} decreases by a fixed amount.",
    ]
    lines = []
    for _ in range(n_lines):
        t = rng.choice(templates)
        lines.append(t.format(s=rng.choice(TRAIN_SUBJECTS),
                              s2=rng.choice(TRAIN_SUBJECTS),
                              c=rng.choice(COMPS), m=rng.choice(MEAS)))
    return "\n".join(lines) + "\n"


PHASE_GENS = {"comparator": gen_comparator_corpus,
              "measurable": gen_measurable_corpus,
              "bind": gen_bind_corpus}

# FROZEN developmental order (comparator -> measurable -> bind). Post-hoc re-order forbidden.
CURRICULUM_ORDER = ["comparator", "measurable", "bind"]


def train_phase(m, cfg, corpus_text, steps, device, lr, bs, tag):
    """One curriculum phase: plain CE continued-pretrain on this phase's corpus."""
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
            print(f"    [H1440 {tag} step {st:4d}] ce={loss.item():.4f} "
                  f"{(time.time()-t0)/60:.1f}min", flush=True)
    return m


def run_curriculum(cfg, device, order, lines, phase_steps, lr, bs, seed, byte_shuffle=False):
    """Load base, run the 3 phases in `order`, return the trained model.
    byte_shuffle=True: each phase corpus is token-shuffled (structure destroyed)."""
    m, _ = C.load_model(C.CKPT_BASE, device)
    for phase in order:
        corpus = PHASE_GENS[phase](lines, seed=seed + hash(phase) % 1000)
        if byte_shuffle:
            corpus = shuffle_bytes(corpus, seed=seed)
        m = train_phase(m, cfg, corpus, phase_steps, device, lr, bs, tag=phase)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--phase-steps", type=int, default=200,
                    help="steps PER phase (3 phases -> 3x total, ~= H_1435 600 if 200)")
    ap.add_argument("--lines", type=int, default=4000)
    ap.add_argument("--lr", type=float, default=3e-5)
    ap.add_argument("--bs", type=int, default=16)
    args = ap.parse_args()
    dev = args.device

    print(f"[H_1440] device={dev} phase_steps={args.phase_steps} order={CURRICULUM_ORDER}",
          flush=True)
    base_m, cfg = C.load_model(C.CKPT_BASE, dev)
    base_eval = C.evaluate(base_m, cfg, "base", list(C.g.IDEATION_SEEDS))
    print(f"[H_1440] base FALS_in={base_eval['FALS_in']} DIST_in={base_eval['DIST_in']} "
          f"FALS_ho={base_eval['FALS_ho']}", flush=True)
    del base_m
    torch.cuda.empty_cache()

    # ── ARM 1: STAGED developmental curriculum (FROZEN order comparator->measurable->bind) ──
    print(f"\n[H_1440] ARM staged curriculum order={CURRICULUM_ORDER}", flush=True)
    m = run_curriculum(cfg, dev, CURRICULUM_ORDER, args.lines, args.phase_steps,
                       args.lr, args.bs, seed=1440)
    out_pt = os.path.join(OUT, "h1440_developmental_curriculum.pt")
    os.makedirs(OUT, exist_ok=True)
    C.save_model(m, cfg, out_pt, {"variant": "H_1440", "order": CURRICULUM_ORDER,
                                  "phase_steps": args.phase_steps, "lr": args.lr})
    staged_eval = C.evaluate(m, cfg, "staged", list(C.g.IDEATION_SEEDS))
    del m
    torch.cuda.empty_cache()

    # ── ARM 2: CURRICULUM-ORDER-SHUFFLE control (random phase order; developmental killer) ──
    rng = random.Random(1440)
    order_shuf = CURRICULUM_ORDER[:]
    while order_shuf == CURRICULUM_ORDER:
        rng.shuffle(order_shuf)
    print(f"\n[H_1440] ARM order-shuffle control order={order_shuf}", flush=True)
    mo = run_curriculum(cfg, dev, order_shuf, args.lines, args.phase_steps,
                        args.lr, args.bs, seed=1440)
    order_shuf_eval = C.evaluate(mo, cfg, "order_shuffle", list(C.g.IDEATION_SEEDS))
    order_shuf_eval["order"] = order_shuf
    del mo
    torch.cuda.empty_cache()

    # ── ARM 3: SHUFFLE-CORPUS control (each phase byte-shuffled; tune-to-green killer) ──
    print(f"\n[H_1440] ARM shuffle-corpus control (byte-shuffled phases)", flush=True)
    ms = run_curriculum(cfg, dev, CURRICULUM_ORDER, args.lines, args.phase_steps,
                        args.lr, args.bs, seed=1440, byte_shuffle=True)
    shuf_corpus_eval = C.evaluate(ms, cfg, "shuffle_corpus", list(C.g.IDEATION_SEEDS))
    del ms
    torch.cuda.empty_cache()

    # ── FROZEN 5-bar (staged is the primary trained arm; shuffle-corpus is the CTRL) ──
    bars = C.print_bars("H_1440 developmental-curriculum", base_eval, staged_eval,
                        shuf_corpus_eval)

    # ── DEVELOPMENTAL discriminator: staged-vs-order-shuffle ──
    print(f"\n  ---- DEVELOPMENTAL DISCRIMINATOR (order matters?) ----", flush=True)
    print(f"  STAGED        FALS_in={staged_eval['FALS_in']} DIST_in={staged_eval['DIST_in']} "
          f"FALS_shuf={staged_eval['FALS_shuf']}", flush=True)
    print(f"  ORDER-SHUFFLE FALS_in={order_shuf_eval['FALS_in']} "
          f"DIST_in={order_shuf_eval['DIST_in']} FALS_shuf={order_shuf_eval['FALS_shuf']} "
          f"order={order_shuf}", flush=True)
    # developmental hypothesis SUPPORTED iff staged shows the B3 collapse AND order-shuffle
    # does NOT (i.e. the staged order is load-bearing for idea-specific binding).
    staged_collapse = staged_eval["FALS_shuf"] < staged_eval["FALS_in"]
    order_collapse = order_shuf_eval["FALS_shuf"] < order_shuf_eval["FALS_in"]
    dev_supported = bool(staged_collapse and not order_collapse and bars["green"])
    print(f"  staged B3-collapse={staged_collapse} · order-shuffle B3-collapse={order_collapse}",
          flush=True)
    if dev_supported:
        dev_note = ("DEVELOPMENTAL SUPPORTED — staged order produces idea-specific binding "
                    "(B3 collapse) that the order-shuffle control does NOT => sequence is "
                    "load-bearing.")
    elif staged_collapse and order_collapse:
        dev_note = ("DEVELOPMENTAL FALSIFIED — order-shuffle ALSO collapses => any exposure to "
                    "the 3 corpora suffices, the STAGED order is not what teaches binding.")
    else:
        dev_note = ("DEVELOPMENTAL NULL — staged did NOT produce a B3 collapse => the curriculum "
                    "did not cross idea-specific binding (same capacity wall as H_1435/1436/1437).")
    print(f"  => {dev_note}", flush=True)

    out = {"variant": "H_1440", "ckpt_base": C.CKPT_BASE, "ckpt_out": out_pt,
           "curriculum_order": CURRICULUM_ORDER, "order_shuffle": order_shuf,
           "base": base_eval, "staged": staged_eval, "order_shuffle_arm": order_shuf_eval,
           "shuffle_corpus": shuf_corpus_eval, "bars": bars,
           "developmental": {"staged_collapse": staged_collapse,
                             "order_collapse": order_collapse,
                             "supported": dev_supported, "note": dev_note}}
    json.dump(out, open(os.path.join(OUT, "h1440_result.json"), "w"),
              ensure_ascii=False, indent=2)
    print(f"[H_1440 done] {OUT}/h1440_result.json", flush=True)


if __name__ == "__main__":
    main()
