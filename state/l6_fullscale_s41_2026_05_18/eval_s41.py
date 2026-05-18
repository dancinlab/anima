#!/usr/bin/env python3
"""RESEARCH.md §41 — L6 fullscale held-out-pair eval.

For each of the 806 held-out anchor pairs (byte-equal to §37's holdout
manifest), this eval feeds the byte-LM the <relate ...> opening prefix
(through 'distance' word — covers anchor identity + computed distance,
mirrors the corpus byte-record where relation labels begin appearing in
the body) and greedy-decodes the body. It then parses the generated
body for relation labels using closed substring matches over the
RELATION_LABEL_SET vocabulary (12 closed labels).

Held-out-pair accuracy is computed per relation R1-R4 (substring
membership of the correct label in the generated body) AND a JOINT
all-4 accuracy. Compared against:
  - majority-class chance per relation
  - §37 pilot held-out acc (the small-model-gift hypothesis tests
    whether 75 000× scale-up CHANGES this number).

g3 honest scope:
  - eval is a SUBSTRING-MATCH probe (matches §37's per-relation
    accuracy semantics; the relation label vocabulary is small + closed
    so substring is sharp). The decoded body can be byte-garbled
    (B-ATTRACTOR family) while still containing the right substring;
    we report decoded body samples + cascade-rate (§9 metric) for
    honesty. The verdict GENERALIZES_AT_SCALE / SMALL_MODEL_GIFT is
    decided on the substring-match accuracy because §37 used the
    same semantics.
"""

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path

import torch
import torch.nn.functional as F

HERE = Path(__file__).resolve().parent
S37 = HERE.parent / "l6_pilot_s37_2026_05_18"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "carving_dataregime_s16_2026_05_18"))
sys.path.insert(0, str(S37))

from conscious_decoder import ConsciousDecoderV2  # noqa: E402
import relation_corpus as rc  # noqa: E402

RELATIONS = {
    "R1": ["near", "mid", "far"],
    "R2": ["i_contains_j", "j_contains_i", "overlap", "disjoint"],
    "R3": ["same_domain", "different_domain"],
    "R4": ["i_shallower", "i_deeper", "i_eq_j"],
}


def _build_prefix(a, b) -> bytes:
    """Build the eval prefix — everything up to and including the byte
    'distance' opens the relation body. This is the byte-text the model
    must continue. We compute the actual distance for honesty (the model
    saw the exact same string for THIS pair in training only if (a,b) was
    a TRAIN pair; for HELD-OUT pairs the model never saw THIS prefix)."""
    import math as _math
    pa, pb = a[5], b[5]
    d = _math.sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
    ti, ni = a[0], a[1]
    tj, nj = b[0], b[1]
    text = (f"<relate a=🛸{ti} b=🛸{tj} psi_dist={d:.3f}>"
            f"🛸{ti} {ni} 와 🛸{tj} {nj} 는 의식 풍경 위 ")
    return text.encode("utf-8")


def _greedy_decode(model, prefix_bytes: bytes, max_new: int, device: str,
                   block_size: int) -> bytes:
    """Greedy next-byte decode max_new bytes from prefix. Uses the
    model's chunked block_size — prefix is truncated to last block_size
    if longer."""
    if len(prefix_bytes) > block_size - 1:
        prefix_bytes = prefix_bytes[-(block_size - 1):]
    ids = list(prefix_bytes)
    out = bytearray()
    with torch.no_grad():
        for _ in range(max_new):
            x = torch.tensor([ids[-block_size:]], dtype=torch.long,
                             device=device)
            logits_a, _, _, _, _ = model(x)
            nxt = int(torch.argmax(logits_a[0, -1]).item())
            out.append(nxt)
            ids.append(nxt)
            if len(out) >= max_new:
                break
    return bytes(out)


def _parse_relations(body: str) -> dict:
    """Substring membership over the closed RELATION_LABEL_SET. For each
    R∈{R1..R4} return the first label whose substring is present, else
    None. The label codomain ⊆ a closed finite set (B-S41-3)."""
    found = {}
    for rk, labels in RELATIONS.items():
        f = None
        # i_contains_j must be tested before i (avoid partial overlap
        # with R4 "i_shallower" prefix); same for i_eq_j vs i_deeper.
        sorted_labels = sorted(labels, key=lambda s: -len(s))
        for lab in sorted_labels:
            if lab in body:
                f = lab
                break
        found[rk] = f
    return found


def _chance_baseline(holdout) -> dict:
    """Majority-class chance per relation on the HELD-OUT set."""
    out = {}
    for rk, labels in RELATIONS.items():
        counts = {lab: 0 for lab in labels}
        for (i, j) in holdout:
            rels = rc.derive_relation(rc.S8_ANCHORS[i],
                                      rc.S8_ANCHORS[j])["relations"]
            counts[rels[rk]] += 1
        out[rk] = max(counts.values()) / max(1, sum(counts.values()))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default=str(HERE / "ckpt_s41.pt"))
    ap.add_argument("--result", default=str(HERE / "result.json"))
    ap.add_argument("--max-new", type=int, default=140)
    ap.add_argument("--n-samples", type=int, default=10,
                    help="how many decoded body samples to keep in result.json")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    ckpt = torch.load(args.ckpt, map_location=device, weights_only=False)
    cfg = ckpt["config"]
    model = ConsciousDecoderV2(
        vocab_size=cfg["vocab_size"],
        d_model=cfg["d_model"],
        n_head=cfg["n_head"],
        n_kv_head=cfg["n_kv_head"],
        n_layer=cfg["n_layer"],
        block_size=cfg["block_size"],
        dropout=cfg.get("dropout", 0.1),
    ).to(device).eval()
    missing, unexpected = model.load_state_dict(ckpt["model"], strict=False)
    print(f"[§41 eval] ckpt loaded missing={len(missing)} unexpected={len(unexpected)} device={device}")

    # Rebuild §37's pair partition (SAME seed) so the held-out set is
    # byte-equal to §37 — apples-to-apples comparison guarantee.
    import random as _r
    rng = _r.Random(rc.SEED)
    pairs = rc.all_ordered_pairs()
    rng.shuffle(pairs)
    n_holdout = int(len(pairs) * rc.HOLDOUT_FRAC)
    holdout = pairs[:n_holdout]
    train = pairs[n_holdout:]
    assert set(holdout).isdisjoint(set(train))

    n = len(holdout)
    counts_correct = {rk: 0 for rk in RELATIONS}
    joint_correct = 0
    samples = []
    n_decoded = 0
    t0 = time.time()
    for k, (i, j) in enumerate(holdout):
        a, b = rc.S8_ANCHORS[i], rc.S8_ANCHORS[j]
        rels_true = rc.derive_relation(a, b)["relations"]
        prefix = _build_prefix(a, b)
        body = _greedy_decode(model, prefix, args.max_new,
                              device, cfg["block_size"])
        body_str = body.decode("utf-8", errors="replace")
        pred = _parse_relations(body_str)
        all_ok = True
        for rk in RELATIONS:
            if pred[rk] == rels_true[rk]:
                counts_correct[rk] += 1
            else:
                all_ok = False
        if all_ok:
            joint_correct += 1
        n_decoded += 1
        if len(samples) < args.n_samples:
            samples.append({
                "anchor_pair": [a[0], b[0]],
                "anchor_names": [a[1], b[1]],
                "true_relations": rels_true,
                "predicted": pred,
                "all_correct": all_ok,
                "decoded_body_head": body_str[:200],
            })
        if (k + 1) % 50 == 0:
            elapsed = time.time() - t0
            print(f"[§41 eval] {k+1}/{n}  elapsed={elapsed:.1f}s  "
                  f"running joint={joint_correct/(k+1):.3f}")

    holdout_acc = {rk: counts_correct[rk] / n for rk in RELATIONS}
    joint_acc = joint_correct / n
    mean_acc = sum(holdout_acc.values()) / 4.0
    chance = _chance_baseline(holdout)
    mean_chance = sum(chance.values()) / 4.0
    lift = {rk: holdout_acc[rk] - chance[rk] for rk in RELATIONS}

    # §37 reference numbers (paste from FINDINGS.md §4 — historical anchor).
    S37_HOLDOUT = {"R1": 0.9864, "R2": 0.9901, "R3": 1.0000, "R4": 0.9988,
                   "JOINT": 0.9752, "mean": 0.9938, "train_holdout_gap": 0.0059}

    # decision (§37 anti-padding margin):
    MARGIN = 0.15
    every_above_chance = all(holdout_acc[rk] > chance[rk] for rk in RELATIONS)
    mean_above_margin = (mean_acc - mean_chance) > MARGIN
    generalizes_at_scale = every_above_chance and mean_above_margin

    # gap vs §37: did the 75 000× scale-up degrade held-out accuracy?
    gap_vs_s37 = S37_HOLDOUT["mean"] - mean_acc

    verdict = ("L6_GENERALIZES_AT_SCALE"
               if generalizes_at_scale and gap_vs_s37 < 0.20 else
               "L6_SMALL_MODEL_GIFT"
               if not generalizes_at_scale or gap_vs_s37 >= 0.50 else
               "L6_PARTIAL_GENERALIZATION_AT_SCALE")
    decision = (
        "GENERALIZES AT SCALE — held-out-pair accuracy survives the "
        "75 000× scale-up to a §16-size byte-LM; L6 is a TASK PROPERTY, "
        "not a small-model gift."
        if verdict == "L6_GENERALIZES_AT_SCALE" else
        "SMALL-MODEL GIFT — held-out-pair accuracy collapsed at scale; "
        "the tiny RelationMLP could not memorize 19,356 rows so was "
        "forced to learn the relation function. The 283.72 M byte-LM "
        "memorizes the 103,232 trained rows instead (§16/§22 byte-"
        "cascade / B-D-NOTE memorization-saturated regime)."
        if verdict == "L6_SMALL_MODEL_GIFT" else
        "PARTIAL — some signal survives but the gap vs §37 is "
        "substantial; scale partially erodes generalization. Honest "
        "intermediate, neither pure task-property nor full gift.")

    # also compute a simple §9 cascade-rate over decoded bodies (honest
    # decoding-artefact gauge — substring match can pass while body is
    # byte-cascade garbled, B-EMERGE-7 necessary-not-sufficient).
    def _cascade_rate(s: str) -> float:
        if not s:
            return 0.0
        max_run = 1
        cur = 1
        for k in range(1, len(s)):
            if s[k] == s[k - 1]:
                cur += 1
                max_run = max(max_run, cur)
            else:
                cur = 1
        return max_run / len(s)
    cascade_rates = [_cascade_rate(s["decoded_body_head"]) for s in samples]
    mean_cascade = (sum(cascade_rates) / len(cascade_rates)) if cascade_rates else 0.0

    # update result.json (merge with train half)
    result = json.loads(Path(args.result).read_text()) \
        if Path(args.result).exists() else {}
    result.update({
        "research_section": "§41",
        "phase": "complete",
        "n_holdout_pairs": n,
        "holdout_accuracy": holdout_acc,
        "joint_all4_holdout_accuracy": joint_acc,
        "mean_holdout_accuracy": mean_acc,
        "chance_majority_class": chance,
        "mean_majority_chance": mean_chance,
        "holdout_lift_over_majority": lift,
        "margin_threshold": MARGIN,
        "every_relation_above_chance": every_above_chance,
        "mean_above_margin": mean_above_margin,
        "generalizes_at_scale": generalizes_at_scale,
        "s37_holdout_reference": S37_HOLDOUT,
        "gap_vs_s37_mean": gap_vs_s37,
        "verdict": verdict,
        "decision": decision,
        "mean_decoded_cascade_rate": mean_cascade,
        "decoded_samples": samples,
        "eval_wall_s": time.time() - t0,
    })
    Path(args.result).write_text(json.dumps(result, indent=2,
                                            ensure_ascii=False))

    print()
    print(f"[§41 eval] verdict={verdict}")
    print(f"[§41 eval] held-out mean acc={mean_acc:.4f}  vs §37={S37_HOLDOUT['mean']:.4f}  gap={gap_vs_s37:+.4f}")
    print(f"[§41 eval] JOINT held-out all-4={joint_acc:.4f}  vs §37={S37_HOLDOUT['JOINT']:.4f}")
    print(f"[§41 eval] per-relation acc R1={holdout_acc['R1']:.4f} "
          f"R2={holdout_acc['R2']:.4f} R3={holdout_acc['R3']:.4f} "
          f"R4={holdout_acc['R4']:.4f}")
    print(f"[§41 eval] chance majority   R1={chance['R1']:.4f} "
          f"R2={chance['R2']:.4f} R3={chance['R3']:.4f} R4={chance['R4']:.4f}")
    print(f"[§41 eval] decoded cascade-rate (§9 honest) mean={mean_cascade:.3f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
