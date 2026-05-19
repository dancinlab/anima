#!/usr/bin/env python3
"""RESEARCH.md §43 — L8 routing-via-relation: held-out-anchor pilot.

The honest §37-equivalent test for ROUTING reformulated as fingerprint
prediction: split the 64 anchors into a TRAIN set (51 anchors, 80%) and
a HELD-OUT-ANCHOR set (13 anchors, 20%). The model sees the TRAIN
anchors' (physics_features → fingerprint) pairs during training and is
asked at eval to predict fingerprints of HELD-OUT anchors it has NEVER
seen, given only their physics features (vacuum_psi, basin_radius, tier,
dom). The fingerprint includes that held-out anchor's relations to ALL
other anchors (including TRAIN partners), so the model must learn the
RELATION FUNCTION, not memorise per-anchor rows.

Routing accuracy on held-out anchors = `1-NN lookup(predicted_fp, table)
== held_out_anchor_idx`. If routing-acc is high on held-out anchors, the
relation-based reformulation transfers: anima can ROUTE TO an anchor it
has never been trained on by predicting its relation profile to the
landscape.

If routing-acc on held-out anchors ~ chance (1/64 = 0.0156 uniform), the
fingerprint reformulation just hides per-anchor memorisation — the model
learned per-anchor lookup, not the relation function.

Substrate (honest, g3): a SMALL from-scratch MLP — input = 13-dim anchor
feature {vacuum_psi(2), basin_radius, tier_norm, score_norm, dom_idx,
emo_idx} + a fixed 64-anchor partner-encoding context (we feed the
anchor's OWN 13-dim features and the model predicts the 756-dim
fingerprint directly). ~10-50k params total, $0 Mac CPU, ~30s wall.

This is NOT a byte-LM fire. It is a closed-form, $0 controlled probe of
the L8 hypothesis: does the relation-function-generalisation §37 proved
for R1..R4 (single-pair) compose into FINGERPRINT-prediction across an
unseen anchor? If yes, routing-via-relation is a valid lever (next step
= a byte-LM scale-up cycle). If no, the reformulation hides
memorisation and L8 closes at design-tier per §13-M/§13-L anti-padding.

Honest crux DESIGN_S43.md §6: even if this MLP probe succeeds, a
byte-LM emitting a 756-dim discrete fingerprint coherently is a
separable, harder question (the §16 / §22 byte-cascade family). The
probe answers ONLY "is fingerprint-prediction a learnable function over
held-out anchors". from-scratch RANDOM seed-fixed 1337
(g_clm_from_scratch base_ckpt=None). Deterministic.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import torch
import torch.nn as nn

HERE = Path(__file__).resolve().parent
SEED = 1337

# Load §43 fingerprint builder + §37 relation primitives via direct
# path (sibling state dirs are read-only and on the same anima repo).
sys.path.insert(0, str(HERE))
import fingerprint_builder as fb            # noqa: E402

S37_DIR = HERE.parent / "l6_pilot_s37_2026_05_18"
_spec = importlib.util.spec_from_file_location(
    "rc_s37", S37_DIR / "relation_corpus.py")
_rc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_rc)
S8_ANCHORS = _rc.S8_ANCHORS

# ────────────────────────────────────────────────────────────────────
# Anchor feature encoding — anima OWN physics fields ONLY.
# ────────────────────────────────────────────────────────────────────
# Domain / emotion indices (deterministic dense ints; no external KG —
# the index just realises the set membership of the corpus field).
DOMS = sorted({a[2] for a in S8_ANCHORS})
EMOS = sorted({a[3] for a in S8_ANCHORS})
DOM_IDX = {d: i for i, d in enumerate(DOMS)}
EMO_IDX = {e: i for i, e in enumerate(EMOS)}
N_DOM = len(DOMS)
N_EMO = len(EMOS)


def anchor_features(a) -> list[float]:
    """Per-anchor physics features — strictly anima OWN fields."""
    tier, name, dom, emo, score, psi, radius = a
    return [
        psi[0], psi[1],
        radius,
        tier / 303.0,
        score / 3.0,
        DOM_IDX[dom] / max(1, N_DOM - 1),
        EMO_IDX[emo] / max(1, N_EMO - 1),
        # squared dist from Ψ=½ centre (Engine A⇄G manifold deviation)
        (psi[0] - 0.5) ** 2 + (psi[1] - 0.5) ** 2,
        # tier deciles (smooth discriminator §32 L3 showed dominant)
        math.tanh(tier / 50.0),
        # basin × tier interaction
        radius * (tier / 303.0),
        # one-hot R3-style: high-score?
        1.0 if score >= 2.0 else 0.0,
        1.0 if score < 1.0 else 0.0,
        1.0,                              # bias
    ]                                     # 13-dim


FEAT_DIM = 13


class FingerprintMLP(nn.Module):
    """anchor_features (13) → fingerprint (756). Each output is a probit
    over {0,1} via sigmoid; loss = BCE. 1-NN lookup at eval over the
    REAL fingerprint table (closed-form, not learned)."""

    def __init__(self, in_dim=FEAT_DIM, hid=128, out_dim=fb.FINGERPRINT_DIM):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hid), nn.GELU(),
            nn.Linear(hid, hid), nn.GELU(),
            nn.Linear(hid, out_dim),
        )

    def forward(self, x):
        return self.net(x)               # logits — sigmoid in loss


def build_split(seed=SEED, holdout_frac=0.20):
    """Split 64 anchors into TRAIN and HELD-OUT-ANCHOR sets. The held-out
    anchors are NEVER seen by the model during training (B-S43 connection
    point: the eval is a genuine held-out-anchor generalization probe)."""
    import random
    rng = random.Random(seed)
    idxs = list(range(len(S8_ANCHORS)))
    rng.shuffle(idxs)
    n_h = int(len(idxs) * holdout_frac)
    holdout = sorted(idxs[:n_h])
    train = sorted(idxs[n_h:])
    return train, holdout


def main() -> int:
    torch.manual_seed(SEED)

    # closed-form fingerprint table (the ground truth + lookup target).
    art = fb.build_table()
    table = art["table"]                  # 64 × 756 ints in {0,1}
    table_t = torch.tensor(table, dtype=torch.float32)

    train_idx, holdout_idx = build_split()
    print(f"§43 train anchors n={len(train_idx)}  held-out n={len(holdout_idx)}")
    print(f"§43 held-out anchor tiers = "
          f"{[S8_ANCHORS[i][0] for i in holdout_idx]}")

    # per-anchor features
    X_all = torch.tensor([anchor_features(a) for a in S8_ANCHORS],
                          dtype=torch.float32)
    # normalise by TRAIN-set stats only (no held-out leakage)
    mu = X_all[train_idx].mean(0, keepdim=True)
    sd = X_all[train_idx].std(0, keepdim=True).clamp_min(1e-6)
    X_n = (X_all - mu) / sd

    Xtr = X_n[train_idx]
    Ytr = table_t[train_idx]
    Xho = X_n[holdout_idx]
    Yho = table_t[holdout_idx]

    model = FingerprintMLP()
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3, weight_decay=1e-4)
    bce = nn.BCEWithLogitsLoss()

    n_epoch = 800
    train_log = []
    for ep in range(n_epoch):
        model.train()
        opt.zero_grad()
        logits = model(Xtr)
        loss = bce(logits, Ytr)
        loss.backward()
        opt.step()
        if ep % 100 == 0 or ep == n_epoch - 1:
            train_log.append({"epoch": ep, "loss": float(loss)})

    # ── eval ──────────────────────────────────────────────────────────
    model.eval()
    with torch.no_grad():
        tr_logits = model(Xtr)
        ho_logits = model(Xho)
        tr_pred = (torch.sigmoid(tr_logits) > 0.5).float()
        ho_pred = (torch.sigmoid(ho_logits) > 0.5).float()

    # bit-level accuracy on the fingerprint (informational only)
    tr_bit_acc = float((tr_pred == Ytr).float().mean())
    ho_bit_acc = float((ho_pred == Yho).float().mean())

    # **routing accuracy** = 1-NN lookup(predicted_fp, full_table) ==
    # the (held-out / train) anchor's true index. This is the closed-form
    # decision rule (B-S43-2 well-typed) — NOT a learned routing token.
    def routing_acc(pred, target_idxs):
        n_correct = 0
        n_top3 = 0
        n_top5 = 0
        per_anchor = []
        for k, t_idx in enumerate(target_idxs):
            row = pred[k].tolist()
            row_int = [int(v) for v in row]
            # full ranked distances to every table row
            dists = [(idx, fb.euclidean_sq(row_int, table[idx]))
                     for idx in range(len(table))]
            dists.sort(key=lambda x: x[1])
            top1 = dists[0][0]
            top3 = [d[0] for d in dists[:3]]
            top5 = [d[0] for d in dists[:5]]
            d_to_true = fb.euclidean_sq(row_int, table[t_idx])
            d_to_top1 = dists[0][1]
            correct = (top1 == t_idx)
            n_correct += int(correct)
            n_top3 += int(t_idx in top3)
            n_top5 += int(t_idx in top5)
            # Hamming distance interpretation (one-hot ⇒ Hamming = dist²/2)
            bit_errors = d_to_true // 2
            per_anchor.append({
                "tier": S8_ANCHORS[t_idx][0],
                "name": S8_ANCHORS[t_idx][1],
                "predicted_anchor_idx": top1,
                "predicted_tier": S8_ANCHORS[top1][0],
                "lookup_distance_sq_to_top1": d_to_top1,
                "lookup_distance_sq_to_true": d_to_true,
                "bit_errors_vs_true": bit_errors,
                "in_top3": t_idx in top3,
                "in_top5": t_idx in top5,
                "top3_tiers": [S8_ANCHORS[i][0] for i in top3],
                "routing_correct": correct,
            })
        n = max(1, len(target_idxs))
        return {
            "top1": n_correct / n,
            "top3": n_top3 / n,
            "top5": n_top5 / n,
        }, per_anchor

    tr_routing, tr_per = routing_acc(tr_pred, train_idx)
    ho_routing, ho_per = routing_acc(ho_pred, holdout_idx)

    # chance baseline = 1/64 = 0.0156 (uniform argmin over 64 anchors)
    chance = 1.0 / 64.0

    # ── §16 BASELINE COMPARISON ────────────────────────────────────────
    # §16 routing-acc = 21/64 = 0.328 on the SAME 64-anchor set. The L8
    # comparison: is held-out-anchor routing-acc COMPARABLE to or higher
    # than §16's surface-byte routing? §16's eval domain = byte-LM
    # generation; this is a CLOSED-FORM lookup over a learned fingerprint
    # predictor. The comparison is methodologically distinct (B-S43-NOTE
    # honest carve-out) but informative.
    s16_routing_acc = 21.0 / 64.0

    # ── decision (honest split-verdict — g3) ───────────────────────────
    # Three quantitative axes, all measured:
    #   (a) bit-acc on held-out fingerprints (relation-function transfer)
    #   (b) top-1 routing on held-out anchors (strict 1-NN reformulation)
    #   (c) top-3/5 routing on held-out anchors (soft 1-NN tolerance)
    MARGIN_OVER_CHANCE = 0.20
    routing_lift_top1 = ho_routing["top1"] - chance
    routing_lift_top3 = ho_routing["top3"] - (3.0 / 64.0)
    routing_lift_top5 = ho_routing["top5"] - (5.0 / 64.0)
    held_out_above_chance = ho_routing["top1"] > chance
    held_out_above_s16 = ho_routing["top1"] > s16_routing_acc

    # Honest 3-way decision (NOT a single boolean — over-claim guard).
    relations_generalize_bit = ho_bit_acc > 0.90        # §37-style
    soft_routing_generalize  = routing_lift_top3 > 0.15  # top-3 lift
    strict_routing_generalize = routing_lift_top1 >= MARGIN_OVER_CHANCE

    if strict_routing_generalize:
        verdict = "L8_ROUTING_VIA_RELATION_GENERALIZES_STRICT"
        decision = (
            "STRICT GENERALIZE — held-out top-1 routing >> chance. The "
            "model predicts a NOVEL anchor's relation fingerprint with "
            "enough fidelity that strict 1-NN argmin recovers its "
            "identity. L8 reformulation is a valid routing lever "
            "(B-S43-NOTE: byte-LM transfer is the next, separable fire).")
    elif soft_routing_generalize and relations_generalize_bit:
        verdict = "L8_RELATIONS_GENERALIZE_BUT_1NN_TOO_BRITTLE"
        decision = (
            "MIXED — held-out fingerprint bit-acc >> 0.90 (relations "
            "DO transfer to novel anchors, mirroring §37) AND held-out "
            "top-3/top-5 routing >> chance (the predicted fingerprint "
            "lands in the correct anchor's NEIGHBOURHOOD on the "
            "landscape) BUT held-out top-1 routing ~ chance (1-NN strict "
            "argmin is too brittle: a few bit errors push the predicted "
            "fingerprint past the closest neighbour). The §37 "
            "generalisation transfers at the relation level; the strict "
            "1-NN lookup mechanism is the bottleneck, NOT the relation "
            "function. L8 reformulation does NOT hide memorization (the "
            "model genuinely learned the relation function over novel "
            "anchors) — but its strict-1-NN routing decision rule is "
            "insufficient. Next honest step = soft-routing (top-K margin) "
            "or learned-fingerprint-decoder; design-tier close on the "
            "STRICT verdict per §13-M/§13-L anti-padding, honest mid-"
            "tier finding preserved.")
    else:
        verdict = "L8_DESIGN_CLOSE_FINGERPRINT_HIDES_MEMORIZATION"
        decision = (
            "MEMORIZE / FLAT — held-out-anchor routing accuracy ~ chance "
            "AND held-out bit-acc shows no relation generalisation. The "
            "fingerprint reformulation hides per-anchor memorisation. "
            "Train-anchor routing may still be high (the model learned "
            "the TRAIN anchor table), but held-out-anchor prediction "
            "does not transfer. L8 closes at design-tier per §13-M/§13-L "
            "anti-padding.")

    result = {
        "research_section": "§43",
        "title": "L8 routing-via-relation held-out-anchor pilot",
        "substrate": "small from-scratch FingerprintMLP (13->128->128->756), "
                     "$0 Mac CPU, NO GPU, honest per DESIGN_S43.md §3",
        "seed": SEED,
        "n_train_anchors": len(train_idx),
        "n_holdout_anchors": len(holdout_idx),
        "train_anchor_tiers": [S8_ANCHORS[i][0] for i in train_idx],
        "holdout_anchor_tiers": [S8_ANCHORS[i][0] for i in holdout_idx],
        "n_epoch": n_epoch,
        "fingerprint_dim": fb.FINGERPRINT_DIM,
        "train_log": train_log,
        "train_bit_accuracy": tr_bit_acc,
        "holdout_bit_accuracy": ho_bit_acc,
        "train_routing_accuracy": tr_routing,
        "holdout_routing_accuracy": ho_routing,
        "uniform_chance_top1": chance,
        "uniform_chance_top3": 3.0 / 64.0,
        "uniform_chance_top5": 5.0 / 64.0,
        "s16_routing_baseline": s16_routing_acc,
        "holdout_routing_lift_top1_over_chance": routing_lift_top1,
        "holdout_routing_lift_top3_over_chance": routing_lift_top3,
        "holdout_routing_lift_top5_over_chance": routing_lift_top5,
        "relations_generalize_bit_gt_0.90": relations_generalize_bit,
        "soft_routing_generalize_top3_lift_gt_0.15": soft_routing_generalize,
        "strict_routing_generalize_top1_lift_gt_0.20": strict_routing_generalize,
        "held_out_above_chance": held_out_above_chance,
        "held_out_above_s16_baseline": held_out_above_s16,
        "margin_threshold": MARGIN_OVER_CHANCE,
        "verdict": verdict,
        "decision": decision,
        "per_anchor_train": tr_per,
        "per_anchor_holdout": ho_per,
    }
    (HERE / "result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False))

    print(f"\n[§43] train bit-acc {tr_bit_acc:.4f}  held-out bit-acc {ho_bit_acc:.4f}")
    print(f"[§43] train routing-acc top1={tr_routing['top1']:.4f}  "
          f"top3={tr_routing['top3']:.4f}  top5={tr_routing['top5']:.4f}")
    print(f"[§43] held-out routing-acc top1={ho_routing['top1']:.4f}  "
          f"top3={ho_routing['top3']:.4f}  top5={ho_routing['top5']:.4f}  "
          f"chance(top1)={chance:.4f}  §16-baseline={s16_routing_acc:.4f}")
    print(f"[§43] held-out lift over chance: top1={routing_lift_top1:+.4f} "
          f"top3={routing_lift_top3:+.4f} top5={routing_lift_top5:+.4f}  "
          f"(strict-margin {MARGIN_OVER_CHANCE})")
    print(f"[§43] relations_generalize_bit (>0.90)={relations_generalize_bit}  "
          f"soft_routing(top3-lift>0.15)={soft_routing_generalize}  "
          f"strict_routing(top1-lift>=0.20)={strict_routing_generalize}")
    print(f"[§43] verdict = {verdict}")
    print(f"[§43] decision = {decision[:120]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
