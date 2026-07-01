#!/usr/bin/env python3
"""H_1464 — PAIRING-CONTRASTIVE binding objective, ENGINE-NATIVE training (303M ByteGPT).

LENS ② of the G6 capacity-wall campaign, the engine-native counterpart of the numpy mirror
(state/1464_pairing_contrastive_bind/h1464_pairing_contrastive.py, DIRECTIONAL). The mirror
broke B3 cross-shuffle COLLAPSE on a bilinear binding model; this re-runs the SAME objective on
the live 303M ByteGPT and (after pt->bin + CORE/bytegpt_decode) re-scores the FROZEN 5-bar.

QUALITATIVE DISTINCTION from H_1441 (state/1441_contrastive_falsifiability/h1441_contrastive.py):
  H_1441 (form-contrastive): pos = FULL falsifiable claim (comparator AND measurable present),
      neg = MINIMAL PAIR with one leg BLANKED (-> non-falsifiable). It rewards FORM-PRESENCE; the
      model learned "emit a falsifiable form unconditionally" => B3 NO-collapse (WALL=CAPACITY at
      torch DIRECTIONAL). It never had to represent WHICH comparator binds to WHICH measurable.

  H_1464 (PAIRING-contrastive): a FIXED roster of N "ideas", each idea = a CANONICAL
      (subject, comparator, measurable) triple. pos = the idea's OWN correct pairing sentence;
      neg = a CROSS sentence re-welding idea_i's comparator with idea_{j!=i}'s measurable. BOTH
      pos and neg are well-formed falsifiable FORMS (two legs present) -- the ONLY difference is
      whether the binding is the CORRECT same-idea one. The contrastive margin can therefore ONLY
      be reduced by representing the binding the whole campaign hunts.

  loss = CE(canonical-pairing corpus) + lam * margin( logP(pos same-idea) - logP(neg cross) )

NOT detector-supervised (a_train_inline_gauge, p7): the contrastive label is STRUCTURAL (same-idea
vs cross-idea pairing), NOT the h1305 detector score. The detector is eval-ONLY VERBATIM, scored
ENGINE-NATIVE afterward (pt_to_engine_bin.py -> CORE/bytegpt_decode -> frozen 5-bar). torch eval is
SKIPPED here (it would be DIRECTIONAL). ckpt MUST be pulled before teardown (a_fire_recover_complete).
"""
import os, sys, json, random, time, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g6_common as C
import torch
import h1435_continued_pretrain as base

make_batches = base.make_batches
shuffle_bytes = base.shuffle_bytes

OUT = os.environ.get("G6_OUT", "/workspace/g6/out")
COMPS = sorted(C.COMPARATOR)
MEAS = sorted(C.MEASURABLE)
SUBJ = base.TRAIN_SUBJECTS

# FROZEN templates — the SAME 5 surface forms as h1435/h1441 (so corpus FORM is identical;
# the ONLY thing H_1464 changes is that pairing is CANONICAL, not random).
PAIR_TEMPLATES = [
    "if {s} grows, the {m} {c} than before.",
    "{s} {c} a higher {m} when the input rises.",
    "the {m} of {s} is greater whenever {s2} {c}.",
    "{s} shows a lower {m} than {s2} under load.",
    "when {s} {c}, its {m} decreases by a fixed amount.",
]

N_IDEAS_CORPUS = 10   # roster of canonical (subject, comparator, measurable) bindings


def make_roster(seed):
    """A FIXED roster of canonical bindings: each subject is permanently bound to ONE comparator
    and ONE measurable. This is the structure PAIRING-contrastive must learn (vs H_1441's random
    combos). Distinct legs so cross-pairs are genuinely different bindings."""
    rng = random.Random(seed)
    subs = list(SUBJ)
    rng.shuffle(subs)
    comps = (COMPS * 3)[: len(subs)]
    meas = (MEAS * 3)[: len(subs)]
    rng.shuffle(comps)
    rng.shuffle(meas)
    roster = []
    for i, s in enumerate(subs[:N_IDEAS_CORPUS]):
        roster.append({"s": s, "c": comps[i % len(comps)], "m": meas[i % len(meas)]})
    return roster


def sentence(idea, c, m, rng):
    """Render an idea with a SPECIFIED comparator c and measurable m (for cross-pair negatives)."""
    t = rng.choice(PAIR_TEMPLATES)
    s2 = rng.choice(SUBJ)
    return t.format(s=idea["s"], s2=s2, c=c, m=m)


def gen_corpus(roster, n_lines, seed=1464):
    """Corpus = ONLY canonical-pairing sentences (each idea with its OWN bound comparator+measurable).
    The model that minimizes CE here sees subject->(its comparator, its measurable) co-occurrence."""
    rng = random.Random(seed)
    lines = []
    for _ in range(n_lines):
        idea = rng.choice(roster)
        lines.append(sentence(idea, idea["c"], idea["m"], rng))
    return "\n".join(lines) + "\n"


def gen_pairs(roster, n, seed):
    """pos = idea's CANONICAL pairing; neg = CROSS re-weld (idea's comparator + ANOTHER idea's
    measurable). Both well-formed; only the binding differs => margin forces binding."""
    rng = random.Random(seed)
    pos, neg = [], []
    for _ in range(n):
        i = rng.randrange(len(roster))
        idea = roster[i]
        j = rng.randrange(len(roster))
        while roster[j]["m"] == idea["m"]:
            j = rng.randrange(len(roster))
        cross_m = roster[j]["m"]
        pos.append(sentence(idea, idea["c"], idea["m"], rng))      # same-idea binding
        neg.append(sentence(idea, idea["c"], cross_m, rng))        # cross binding (wrong measurable)
    return pos, neg


def _seq_loglik(m, text, block, device):
    ids = list(text.encode("utf-8"))[: block + 1]
    if len(ids) < 2:
        return torch.tensor(0.0, device=device)
    x = torch.tensor(ids[:-1], device=device)[None]
    y = torch.tensor(ids[1:], device=device)[None]
    _, ce = m(x, y)
    return -ce


def contrastive_loss(m, pos, neg, block, device, margin=0.5):
    terms = [torch.clamp(margin - (_seq_loglik(m, p, block, device) - _seq_loglik(m, n, block, device)), min=0.0)
             for p, n in zip(pos, neg)]
    return torch.stack(terms).mean()


def train(m, cfg, corpus_text, roster, steps, device, lr=3e-5, bs=4, lam=0.5, pairs_per=4):
    m.train()
    m.grad_ckpt = True   # 12GB GPU: checkpoint blocks during training (off at decode)
    opt = torch.optim.AdamW(m.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)
    gen = make_batches(corpus_text, cfg["block"], bs, device)
    t0 = time.time()
    for st in range(steps):
        x, y = next(gen)
        _, ce = m(x, y)
        pos, neg = gen_pairs(roster, pairs_per, seed=1464000 + st)
        con = contrastive_loss(m, pos, neg, cfg["block"], device)
        loss = ce + lam * con
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0)
        opt.step()
        if st % 50 == 0 or st == steps - 1:
            print(f"    [H1464 step {st:4d}] ce={ce.item():.4f} con={con.item():.4f} "
                  f"{(time.time()-t0)/60:.1f}min", flush=True)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--lines", type=int, default=4000)
    ap.add_argument("--lam", type=float, default=0.5)
    args = ap.parse_args()
    dev = args.device
    os.makedirs(OUT, exist_ok=True)
    print(f"[H_1464] device={dev} steps={args.steps} lam={args.lam}", flush=True)

    roster = make_roster(seed=1464)
    print(f"[H_1464] roster ({len(roster)} canonical bindings):", flush=True)
    for r in roster:
        print(f"    {r['s']:14s} -> comparator={r['c']:10s} measurable={r['m']}", flush=True)
    corpus = gen_corpus(roster, args.lines, seed=1464)

    # PAIRING-contrastive-trained
    m, cfg = C.load_model(C.CKPT_BASE, dev)
    m = train(m, cfg, corpus, roster, args.steps, dev, lam=args.lam)
    out_pt = os.path.join(OUT, "h1464_pairing.pt")
    C.save_model(m, cfg, out_pt, {"variant": "H_1464", "steps": args.steps, "lam": args.lam,
                                  "objective": "pairing-contrastive", "roster": roster})
    del m
    torch.cuda.empty_cache()
    print(f"[H_1464 trained] {out_pt}", flush=True)

    # SHUFFLE-CORPUS control (same bytes, structure destroyed) — same PAIRING recipe.
    shuf = shuffle_bytes(corpus, seed=1464)
    ms, _ = C.load_model(C.CKPT_BASE, dev)
    ms = train(ms, cfg, shuf, roster, args.steps, dev, lam=args.lam)
    shuf_pt = os.path.join(OUT, "h1464_shuffle.pt")
    C.save_model(ms, cfg, shuf_pt, {"variant": "H_1464_shuffle", "steps": args.steps, "lam": args.lam})
    del ms
    torch.cuda.empty_cache()
    print(f"[H_1464 shuffle-control] {shuf_pt}", flush=True)

    # FORM-ONLY ablation (= H_1441 regression control): neg = BLANKED leg, pos = ANY combo.
    # Predicts B3 NO-collapse (form, not binding). Re-uses the H_1441 recipe with the SAME base.
    print("[H_1464] NEXT: pt_to_engine_bin.py {pairing,shuffle}.pt + base -> .bin -> "
          "CORE/bytegpt_decode frozen 5-bar (ENGINE-NATIVE). torch eval skipped (DIRECTIONAL).", flush=True)
    json.dump({"roster": roster, "out_pt": out_pt, "shuf_pt": shuf_pt,
               "steps": args.steps, "lam": args.lam},
              open(os.path.join(OUT, "h1464_train_meta.json"), "w"), indent=2)
    print("H1464_TRAIN_DONE", flush=True)


if __name__ == "__main__":
    main()
