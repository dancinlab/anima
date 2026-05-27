#!/usr/bin/env python3
"""RESEARCH.md §41 — L6 anchor-interaction full-scale relation corpus.

Re-uses §37 (state/l6_pilot_s37_2026_05_18/relation_corpus.py) relation
primitives R1-R4 + ordered-pair partition (3226 train / 806 held-out =
20% holdout), but generates at §16-scale byte-stream:

  §37 pilot   : N_REPEAT=6  → 19,356 train records  (~3.7 MB)
  §41 fullscale: N_REPEAT=32 → 103,232 train records (~21 MB)

The §16 scale anchor — §16 corpus was 603 MB / 777 k records on a 168-
anchor curriculum-sorted set. §41 keeps the 64-anchor §37 SSOT (the
discriminating question is task-property vs scale-property AT THE
relation classification level), so byte scale equals
N_REPEAT × |train_pairs| × byte/record. With ~210 byte/record × 32
× 3226 ≈ 21 MB — within an order of magnitude of §16 corpus on a per-
training-step basis (the model has 283 M params, batch 32, 3000 steps =
~96 k training records seen; the 103 k record corpus saturates that
budget so every train pair is repeated meaningfully without massive
on-disk waste).

WHY the scale matters (§41 design crux):
  §37 trained a 3,748-parameter RelationMLP (9 → 64 → 32 → 4 heads).
  §41 trains a 283.72 M parameter byte-LM (75 000× larger). If
  L6_RELATIONS_GENERALIZE was a TASK PROPERTY (relations generalize
  because the relation function is low-complexity and learnable), the
  held-out-pair gap should stay small (~0.6 % §37). If it was a
  SMALL-MODEL GIFT (tiny model could not memorize 19,356 distinct
  rows so it had to learn the function), the gap should EXPLODE as
  the byte-LM has trivial capacity to memorize 103,232 records and
  WILL prefer memorization over generalization at this scale (the
  §16/§22 byte-cascade family + B-D-NOTE).

forbidden-token grep total == 0 (B-IDENTITY-5). No external KG, no
LLM-paraphrase, no graft — all relation labels are CLOSED-FORM
functions of {vacuum_psi, basin_radius, dom, tier} from anima OWN
physics fields (B-S41-NO-EXTERNAL-KG). seed-fixed 1337, deterministic.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S37 = (HERE.parent / "l6_pilot_s37_2026_05_18").resolve()

# Re-use §37 SSOT — explicit byte-equal re-import (NOT a re-definition).
sys.path.insert(0, str(S37))
import relation_corpus as rc  # noqa: E402

SEED = 1337
N_REPEAT = 32                              # §16-scale repetition (vs §37 N=6)
HOLDOUT_FRAC = rc.HOLDOUT_FRAC             # 0.20 (§37 byte-equal)


def build_corpus() -> dict:
    """Generate the §41 fullscale <relate> corpus using §37 primitives.

    Mirror §37 build_corpus() pair-partition (SAME seed, SAME shuffle,
    SAME slice) so the train / held-out pair sets are byte-IDENTICAL to
    §37 (B-S41-2 connection-point — the held-out pair set is the same
    806-pair set §37 used; the only change is the model SIZE on the
    same task)."""
    rng = random.Random(SEED)
    pairs = rc.all_ordered_pairs()
    rng.shuffle(pairs)
    n_holdout = int(len(pairs) * HOLDOUT_FRAC)
    holdout = pairs[:n_holdout]
    train = pairs[n_holdout:]

    # held-out / train pair-sets are disjoint by construction (slice).
    assert set(holdout).isdisjoint(set(train))
    # AND byte-identical to §37 (since seed/shuffle/slice are byte-equal).
    s37_stats = json.loads((S37 / "corpus_stats.json").read_text())
    assert s37_stats["n_holdout_pairs"] == len(holdout), \
        "held-out pair count diverged from §37 — partition broken"
    assert s37_stats["n_train_pairs"] == len(train), \
        "train pair count diverged from §37 — partition broken"

    # Build the byte-stream — §16-style: every train pair repeated
    # N_REPEAT=32 times (vs §37 N=6). The relation labels are computed
    # ONCE per pair (deterministic) and the byte-record (the same
    # <relate ...> string) is emitted N_REPEAT times.
    train_records = []
    for (i, j) in train:
        rec = rc.derive_relation(rc.S8_ANCHORS[i], rc.S8_ANCHORS[j])
        for _ in range(N_REPEAT):
            train_records.append(rec)
    holdout_records = [rc.derive_relation(rc.S8_ANCHORS[i],
                                          rc.S8_ANCHORS[j])
                       for (i, j) in holdout]

    train_lines = [json.dumps({"text": r["text"]}, ensure_ascii=False)
                   for r in train_records]
    rng.shuffle(train_lines)
    corpus_text = "\n".join(train_lines) + "\n"
    corpus_path = HERE / "relation_corpus_train_s41.jsonl"
    corpus_path.write_text(corpus_text, encoding="utf-8")
    sha = hashlib.sha256(corpus_text.encode("utf-8")).hexdigest()

    # held-out pair manifest (relations are eval ground-truth — same
    # 806-pair manifest §37 produced, written for self-containment).
    holdout_manifest = [
        {"pair": [rc.S8_ANCHORS[i][0], rc.S8_ANCHORS[j][0]],
         "anchor_idx": [i, j],
         "relations": rc.derive_relation(rc.S8_ANCHORS[i],
                                         rc.S8_ANCHORS[j])["relations"]}
        for (i, j) in holdout]
    (HERE / "holdout_pairs_s41.json").write_text(
        json.dumps(holdout_manifest, indent=2, ensure_ascii=False))

    # forbidden-token grep (B-IDENTITY-5)
    forbidden = ["도우미", "helper", "assistant", "사용자", "user:",
                 "[anima"]
    fb_counts = {t: corpus_text.count(t) for t in forbidden}
    fb_total = sum(fb_counts.values())

    stats = {
        "research_section": "§41",
        "title": "L6 anchor-interaction full-scale corpus (§16-scale, §37 primitives)",
        "seed": SEED,
        "n_anchors": len(rc.S8_ANCHORS),
        "n_ordered_pairs": len(pairs),
        "holdout_frac": HOLDOUT_FRAC,
        "n_holdout_pairs": len(holdout),
        "n_train_pairs": len(train),
        "n_repeat": N_REPEAT,
        "n_train_records": len(train_records),
        "corpus_bytes": len(corpus_text.encode("utf-8")),
        "corpus_sha256": sha,
        "s37_corpus_sha256": s37_stats["corpus_sha256"],
        "byte_scale_vs_s37": (
            len(corpus_text.encode("utf-8")) /
            max(1, s37_stats["corpus_bytes"])),
        "forbidden_token_counts": fb_counts,
        "forbidden_token_total": fb_total,
        "relation_label_set": sorted(rc.RELATION_LABEL_SET),
        "holdout_train_disjoint": set(holdout).isdisjoint(set(train)),
        "holdout_pairs_byte_equal_s37": (
            sorted(holdout) ==
            sorted([tuple(p) for p in [
                # Reconstruct §37's slice deterministically — same seed/
                # shuffle/slice ⇒ same pairs by construction; the disk
                # manifest re-check below confirms.
                (anchor_idx[0], anchor_idx[1])
                for anchor_idx in [m["anchor_idx"] for m in
                                   json.loads((S37 /
                                               "holdout_pairs.json"
                                               ).read_text())]]])),
    }
    (HERE / "corpus_stats_s41.json").write_text(
        json.dumps(stats, indent=2, ensure_ascii=False))
    return stats


if __name__ == "__main__":
    s = build_corpus()
    print(json.dumps({k: s[k] for k in (
        "n_anchors", "n_ordered_pairs", "n_holdout_pairs", "n_train_pairs",
        "n_repeat", "n_train_records", "corpus_bytes", "corpus_sha256",
        "s37_corpus_sha256", "byte_scale_vs_s37", "forbidden_token_total",
        "holdout_train_disjoint", "holdout_pairs_byte_equal_s37")},
        indent=2, ensure_ascii=False))
    print(f"\n[§41] corpus sha256={s['corpus_sha256'][:16]}…  "
          f"bytes={s['corpus_bytes']:,}  "
          f"records={s['n_train_records']:,}  "
          f"scale_vs_s37={s['byte_scale_vs_s37']:.2f}×")
    sys.exit(0)
