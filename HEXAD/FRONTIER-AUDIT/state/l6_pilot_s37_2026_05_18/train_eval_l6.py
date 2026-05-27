#!/usr/bin/env python3
"""RESEARCH.md §37 — L6 held-out-pair pilot: trainer + held-out eval.

The discriminating measurement DESIGN_L6.md §6.1 / §7.2 specified: a
fraction of anchor PAIRS is held out of training; the pilot measures
whether the model predicts the HELD-OUT pairs' relations correctly.

  held-out-pair accuracy >> chance  ⇒  relations GENERALIZE
                                        (L6 fire-worthy at scale)
  held-out-pair accuracy ~ chance   ⇒  memorization-at-relation-
                                        granularity (the §16.6-C defect
                                        lifted one level) ⇒ L6
                                        design-close per §13-M/§13-L
                                        anti-padding.

────────────────────────────────────────────────────────────────────────
SUBSTRATE — honest statement (g3)
────────────────────────────────────────────────────────────────────────
This pilot trains a SMALL from-scratch model ($0 Mac CPU, NO GPU) — a
relation classifier: input = the anchor-PAIR physics feature vector
{vacuum_psi_i, vacuum_psi_j, basin_radius_i, basin_radius_j, tier_i,
tier_j, dom_i==dom_j}, output = the four relation labels R1-R4.

Why a feature classifier and not a byte-LM generation probe:
  - the §33 design's discriminating signal is "held-out-pair relation
    ACCURACY" — a per-pair correct/incorrect count. A classifier
    measures exactly that, deterministically and cheaply.
  - a byte-LM evaluated by free generation would conflate the relation-
    function-learning signal with byte-cascade decoding artefacts (the
    §16/§22 B-ATTRACTOR family). The classifier isolates the inter-
    anchor-reasoning question: did the model learn the FUNCTION
    (physics fields → relation), or memorize the 3226 trained rows?
  - this keeps the pilot honest and $0: a 64-anchor relation task is
    tiny; a from-scratch MLP on CPU answers it in seconds.

The classifier IS a genuine held-out-pair generalization probe: the
3226 train pairs and the 806 held-out pairs are a DISJOINT partition of
the 4032 ordered pairs (B-S37-1 connection point). The model never sees
a held-out pair during training. If held-out accuracy ~ chance, the
model memorized the train rows; if >> chance, it learned the relation
geometry. from-scratch RANDOM seed-fixed 1337 (g_clm_from_scratch).

NO GPU. NO pre-trained weights. Deterministic (seed-fixed).
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import torch
import torch.nn as nn

HERE = Path(__file__).resolve().parent
SEED = 1337

# import the anchor SSOT + relation primitives under test
sys.path.insert(0, str(HERE))
import relation_corpus as rc                         # noqa: E402

# the four relations and their label codomains (B-S37-3 bounds these)
RELATIONS = {
    "R1": ["near", "mid", "far"],
    "R2": ["i_contains_j", "j_contains_i", "overlap", "disjoint"],
    "R3": ["same_domain", "different_domain"],
    "R4": ["i_shallower", "i_deeper", "i_eq_j"],
}


def pair_features(a, b) -> list:
    """Anchor-pair physics feature vector — anima's OWN fields ONLY.

    {vacuum_psi_i (2), vacuum_psi_j (2), basin_radius_i, basin_radius_j,
     tier_i_norm, tier_j_norm, dom_same} = 9-dim. tier normalised by /303
     (the §16 curriculum tier_w normaliser). NO external feature."""
    pi, pj = a[5], b[5]
    return [
        pi[0], pi[1], pj[0], pj[1],
        a[6], b[6],
        a[0] / 303.0, b[0] / 303.0,
        1.0 if a[2] == b[2] else 0.0,
    ]


class RelationMLP(nn.Module):
    """Tiny from-scratch relation classifier. 9 -> 64 -> 32 -> 4 heads.

    Four output heads (one per relation R1-R4), each a small softmax
    classifier over that relation's label codomain."""

    def __init__(self):
        super().__init__()
        self.trunk = nn.Sequential(
            nn.Linear(9, 64), nn.GELU(),
            nn.Linear(64, 32), nn.GELU(),
        )
        self.heads = nn.ModuleDict({
            rk: nn.Linear(32, len(labels))
            for rk, labels in RELATIONS.items()
        })

    def forward(self, x):
        h = self.trunk(x)
        return {rk: self.heads[rk](h) for rk in RELATIONS}


def build_split():
    """Reproduce the relation_corpus.py held-out / train pair partition
    EXACTLY (same seed, same shuffle, same slice) — so the pilot's
    held-out set is byte-equal to the corpus's held-out manifest."""
    import random
    rng = random.Random(SEED)
    pairs = rc.all_ordered_pairs()
    rng.shuffle(pairs)
    n_holdout = int(len(pairs) * rc.HOLDOUT_FRAC)
    return pairs[:n_holdout], pairs[n_holdout:]    # (holdout, train)


def make_xy(pairs):
    X, Y = [], {rk: [] for rk in RELATIONS}
    for (i, j) in pairs:
        a, b = rc.S8_ANCHORS[i], rc.S8_ANCHORS[j]
        X.append(pair_features(a, b))
        rels = rc.derive_relation(a, b)["relations"]
        for rk, labels in RELATIONS.items():
            Y[rk].append(labels.index(rels[rk]))
    Xt = torch.tensor(X, dtype=torch.float32)
    Yt = {rk: torch.tensor(v, dtype=torch.long) for rk, v in Y.items()}
    return Xt, Yt


def chance_baseline(holdout):
    """Majority-class chance per relation: the accuracy a model gets by
    always predicting the most frequent label on the held-out set. This
    is the honest 'chance' the held-out accuracy is compared against."""
    out = {}
    for rk, labels in RELATIONS.items():
        counts = [0] * len(labels)
        for (i, j) in holdout:
            rels = rc.derive_relation(rc.S8_ANCHORS[i],
                                      rc.S8_ANCHORS[j])["relations"]
            counts[labels.index(rels[rk])] += 1
        out[rk] = max(counts) / max(1, sum(counts))
    # uniform-random chance too (1/|labels|)
    out_uniform = {rk: 1.0 / len(labels)
                   for rk, labels in RELATIONS.items()}
    return out, out_uniform


def main() -> int:
    torch.manual_seed(SEED)

    holdout, train = build_split()
    assert set(holdout).isdisjoint(set(train)), "held-out leakage!"

    Xtr, Ytr = make_xy(train)
    Xho, Yho = make_xy(holdout)

    # normalise features by train-set mean/std (held-out uses train stats
    # — no held-out leakage into the normaliser)
    mu = Xtr.mean(0, keepdim=True)
    sd = Xtr.std(0, keepdim=True).clamp_min(1e-6)
    Xtr_n = (Xtr - mu) / sd
    Xho_n = (Xho - mu) / sd

    model = RelationMLP()
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3, weight_decay=1e-4)
    ce = nn.CrossEntropyLoss()

    n_epoch = 400
    bs = 256
    n = Xtr_n.shape[0]
    train_log = []
    for ep in range(n_epoch):
        perm = torch.randperm(n)
        model.train()
        ep_loss = 0.0
        for k in range(0, n, bs):
            idx = perm[k:k + bs]
            xb = Xtr_n[idx]
            opt.zero_grad()
            logits = model(xb)
            loss = sum(ce(logits[rk], Ytr[rk][idx]) for rk in RELATIONS)
            loss.backward()
            opt.step()
            ep_loss += float(loss) * len(idx)
        if ep % 50 == 0 or ep == n_epoch - 1:
            train_log.append({"epoch": ep, "loss": ep_loss / n})

    # ── evaluation ─────────────────────────────────────────────────────
    model.eval()
    with torch.no_grad():
        tr_logits = model(Xtr_n)
        ho_logits = model(Xho_n)

    def acc(logits, Y):
        out = {}
        for rk in RELATIONS:
            pred = logits[rk].argmax(-1)
            out[rk] = float((pred == Y[rk]).float().mean())
        # joint: ALL FOUR relations correct for the pair
        all_correct = torch.ones(len(Y["R1"]), dtype=torch.bool)
        for rk in RELATIONS:
            all_correct &= (logits[rk].argmax(-1) == Y[rk])
        out["JOINT_all4"] = float(all_correct.float().mean())
        return out

    train_acc = acc(tr_logits, Ytr)
    holdout_acc = acc(ho_logits, Yho)
    chance_majority, chance_uniform = chance_baseline(holdout)

    # ── verdict ────────────────────────────────────────────────────────
    # per-relation lift over majority-class chance
    lift = {rk: holdout_acc[rk] - chance_majority[rk] for rk in RELATIONS}
    # mean held-out per-relation accuracy vs mean majority chance
    mean_ho = sum(holdout_acc[rk] for rk in RELATIONS) / 4.0
    mean_chance = sum(chance_majority[rk] for rk in RELATIONS) / 4.0
    # decision: held-out accuracy >> chance ?  use a margin of 0.15 over
    # majority chance on the mean per-relation accuracy AND every single
    # relation strictly above its own majority chance.
    MARGIN = 0.15
    every_rel_above_chance = all(
        holdout_acc[rk] > chance_majority[rk] for rk in RELATIONS)
    mean_above_margin = (mean_ho - mean_chance) > MARGIN
    generalizes = every_rel_above_chance and mean_above_margin

    verdict = ("L6_RELATIONS_GENERALIZE" if generalizes
               else "L6_DESIGN_CLOSE")
    decision = (
        "GENERALIZE — held-out-pair relation accuracy >> chance; the "
        "model learned the relation FUNCTION, not the trained rows. L6 "
        "is fire-worthy at scale (DESIGN_L6.md §7.2)."
        if generalizes else
        "MEMORIZE / FLAT — held-out-pair relation accuracy ~ chance; the "
        "§16.6-C memorization defect is reproduced at relation-"
        "granularity. L6 design-close per §13-M/§13-L anti-padding "
        "(DESIGN_L6.md §7.1).")

    result = {
        "research_section": "§37",
        "title": "L6 anchor-interaction held-out-pair pilot",
        "substrate": "small from-scratch RelationMLP (9->64->32->4heads), "
                     "$0 Mac CPU, NO GPU — honest per FINDINGS.md §2",
        "seed": SEED,
        "n_train_pairs": len(train),
        "n_holdout_pairs": len(holdout),
        "holdout_train_disjoint": set(holdout).isdisjoint(set(train)),
        "n_epoch": n_epoch,
        "train_log": train_log,
        "train_accuracy": train_acc,
        "holdout_accuracy": holdout_acc,
        "chance_majority_class": chance_majority,
        "chance_uniform": chance_uniform,
        "holdout_lift_over_majority": lift,
        "mean_holdout_acc": mean_ho,
        "mean_majority_chance": mean_chance,
        "margin_threshold": MARGIN,
        "every_relation_above_chance": every_rel_above_chance,
        "mean_above_margin": mean_above_margin,
        "generalizes": generalizes,
        "verdict": verdict,
        "decision": decision,
    }
    (HERE / "result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False))
    print(json.dumps({k: result[k] for k in (
        "verdict", "holdout_accuracy", "train_accuracy",
        "chance_majority_class", "holdout_lift_over_majority",
        "mean_holdout_acc", "mean_majority_chance", "generalizes")},
        indent=2, ensure_ascii=False))
    print(f"\n[§37] verdict={verdict}  generalizes={generalizes}")
    print(f"[§37] mean held-out acc {mean_ho:.4f} vs majority chance "
          f"{mean_chance:.4f}  (JOINT all-4 held-out "
          f"{holdout_acc['JOINT_all4']:.4f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
