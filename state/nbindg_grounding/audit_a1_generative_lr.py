"""A1 — the GENERATIVE-LR probe: is the polarity written in the model, just not INVERTIBLE?

This is the fork the whole O/C-channel design hangs on, and it costs $0.

H_9297 proved (EARNED, n=91, bar 2.86σ) that a probe reading the frozen representation cannot
recover a held-out atom's polarity — while H_9291's oracle recovers it 29/29 from the very same
left-context bytes. So the information is in the input and not in the representation. Two mechanisms
survive that, and they demand opposite treatments:

  M1  WRITE-ABSENT       — the CE gradient never wrote atom→polarity at all. Nothing to invert.
  M2  DIRECTION-MISMATCH — it DID write, but only in the generative direction. A causal LM trained
                           on "배송도 빠르고 리얼좋아요" learns  p(atom | polar-context)  — the
                           forward map. Our grid query asks  p(polarity | atom)  — the reverse.
                           The knowledge would be there, and simply not invertible.

A1 measures the forward map directly, on the frozen ckpts, with no retraining:

    Δ(a) = log p(a | C⁺) − log p(a | C⁻)

C⁺/C⁻ are authored positive/negative sentiment carriers (measurement-only — they never enter any
training corpus). If the model wrote the association, a positive atom is cheaper to emit after a
positive carrier, so sign(Δ) should track gold polarity ACROSS THE HELD-OUT ATOMS. Chance is 0.5.

  · sign-accuracy ≫ chance  ⇒  **M2** — the knowledge is written but not invertible. The O channel
    must then centre on an INVERSION curriculum (teach the model to query its own generative
    knowledge), and an abstention objective alone would be treating the wrong disease.
  · sign-accuracy ≈ chance  ⇒  **M1** — nothing was written. Inversion has nothing to invert; the
    recipe must first make the corpus WRITE the association (exposure/objective), and the design's
    §1-3 INVERSION curriculum is dead before it costs a single GPU-hour.

Either way the answer changes what we would spend $21 on, which is the whole point of running it
first. Precedent: two cheap audits (H_9296, H_9297) have already overturned an expensive
conclusion in this lane.

The NLL comes from the mandated path — `anima-py evaluate --interaction-lift`, the exact production
trunk forward — so this is engine-native, not a mirror.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ANIMA = "/tmp/animaenv/bin/anima-py"
CKPT_DIR = os.path.expanduser("~/anima-weights/natem_n2")
ARMS = ["main_s7", "main_s11", "base_only", "shuffle_grid"]
WIN = 64
SCORE_LEN = 8          # the atom's own bytes are what we score

# Authored sentiment carriers — MEASUREMENT-ONLY (they appear in no training corpus).
#
# JUNCTION-MATCHED, and that matching is the whole point. The first attempt used carriers that
# ENDED differently ("…품질도 훌륭해서 " vs "…형편없어서 "), so the byte-NLL of the atom was
# dominated by the grammatical fit at the seam rather than by sentiment — and A4 caught it: the
# probe read chance even on the SEEN atoms the model answers at 0.950. A probe that cannot see
# what it is built to see cannot certify its absence.
#
# The repair: every carrier now ends with the SAME bytes ("… 정말 "), so the seam is byte-identical
# across the ⁺/⁻ arms and cancels in the paired difference. Only the sentiment EARLIER in the
# carrier differs. A4 re-runs on SEEN atoms and must now pass, or A1 stays INVALID.
_TAIL = " 정말 "
C_POS = ["배송도 빠르고 품질도 좋아서" + _TAIL, "너무 만족스럽고 마음에 들어서" + _TAIL]
C_NEG = ["배송도 느리고 품질도 나빠서" + _TAIL, "너무 실망스럽고 마음에 안 들어서" + _TAIL]


def build_manifests(atoms, split="heldout"):
    """One manifest PER ATOM BYTE-LENGTH, each scoring exactly that many bytes.

    `--score-len` is manifest-global, but Korean stems are 3–12 bytes. A fixed score_len therefore
    scores PAST the atom and into the carrier — and since the ⁺/⁻ carriers differ, that contaminates
    the very contrast the probe is built on. (This is what made the first passes read chance even on
    the corpus's most strongly grounded atoms.) Grouping by byte length pins the scored window to
    exactly the atom.
    """
    by_len = {}
    for i, a in enumerate(atoms):
        by_len.setdefault(len(a["stem"].encode()), []).append((i, a))
    paths = []
    for L, group in sorted(by_len.items()):
        items = []
        for i, a in group:
            for j, c in enumerate(C_POS):
                items.append({"text": c + a["stem"], "a": i, "b": j})
            for j, c in enumerate(C_NEG):
                items.append({"text": c + a["stem"], "a": i, "b": len(C_POS) + j})
        path = os.path.join(HERE, f"a1_manifest_{split}_L{L}.json")
        json.dump({"win": WIN, "score_len": L, "items": items},
                  open(path, "w"), ensure_ascii=False)
        paths.append((L, path))
    return paths


def run_arm(arm: str, manifests, split="heldout") -> dict:
    """Merged cells across the per-length manifests: (atom idx, carrier idx) -> NLL of the atom."""
    nll = {}
    for L, manifest in manifests:
        out = os.path.join(HERE, f"a1_nll_{split}_L{L}_{arm}.json")
        if not os.path.exists(out):
            subprocess.run([ANIMA, "evaluate", os.path.join(CKPT_DIR, f"natem_n2_{arm}.clm"),
                            "--interaction-lift", manifest, "--out", out,
                            "--win", str(WIN), "--score-len", str(L)],
                           check=True, capture_output=True)
        cells = json.load(open(out))["cells"]
        for k, v in cells.items():
            a, b = (int(x) for x in k.split(","))
            nll[(a, b)] = float(np.mean(v))
    return nll


def main() -> int:
    split = sys.argv[1] if len(sys.argv) > 1 else "heldout"
    if split == "strong":
        # A4-STRONG: the probe's real positive control. Not the grid atoms (whose association the
        # grid installed as a REVERSE-only lookup) but the atoms the CORPUS itself grounds hardest —
        # occ >= 500, purity >= 0.90 (최고 / 별로 / 빠르 / 재미없 …). If the generative direction
        # cannot be seen even HERE, the probe is dead and its silence certifies nothing.
        atoms = json.load(open(os.path.join(HERE, "a4_strong_atoms.json")))["atoms"]
    else:
        meta = json.load(open(os.path.join(HERE, "gt_atoms_n92.json")))["atoms"]
        atoms = [a for a in meta if a["split"] == split]
    n = len(atoms)
    sd = math.sqrt(0.25 / n)
    print(f"A1 — GENERATIVE-LR probe · split={split} · n = {n} · chance sd = {sd:.4f}")
    print(f"     Δ(a) = log p(a | C⁺) − log p(a | C⁻)   ({len(C_POS)}+{len(C_NEG)} authored carriers,"
          f" measurement-only)\n")

    manifests = build_manifests(atoms, split)
    out = {"split": split, "n": n, "chance_sd": sd, "arms": {}}

    for arm in ARMS:
        nll = run_arm(arm, manifests, split)
        d, gold = [], []
        for i, a in enumerate(atoms):
            pos = np.mean([nll[(i, j)] for j in range(len(C_POS))])
            neg = np.mean([nll[(i, len(C_POS) + j)] for j in range(len(C_NEG))])
            d.append(neg - pos)                     # NLL⁻ − NLL⁺ = log p(a|C⁺) − log p(a|C⁻)
            gold.append(a["pol"])
        d, gold = np.array(d), np.array(gold)
        hit = (d > 0) == (gold == 1)
        acc = float(hit.mean())
        p1 = float(stats.binom.sf(int(hit.sum()) - 1, n, 0.5))
        # effect size: does |Δ| separate at all, and does it point the right way?
        r = float(stats.pointbiserialr(gold, d).statistic)
        out["arms"][arm] = {"sign_acc": acc, "sigma": (acc - 0.5) / sd, "exact_p": p1,
                            "pointbiserial_r": r, "mean_delta_pos": float(d[gold == 1].mean()),
                            "mean_delta_neg": float(d[gold == 0].mean())}
        print(f"  {arm:>13} | sign-acc {acc:.3f} ({(acc-0.5)/sd:+.2f}σ) · exact p = {p1:.4f} "
              f"· r_pb = {r:+.3f}")
        print(f"  {'':>13} | mean Δ: 긍정 원자 {d[gold==1].mean():+.3f} · 부정 원자 "
              f"{d[gold==0].mean():+.3f}")

    m7, m11 = out["arms"]["main_s7"], out["arms"]["main_s11"]
    base = out["arms"]["base_only"]
    m2 = all(a["exact_p"] < 0.05 for a in (m7, m11))
    print()
    if m2:
        verdict = ("🔓 **M2 DIRECTION-MISMATCH** — the association IS written, in the generative "
                   "direction, and the grid query simply cannot invert it. ⇒ the O channel must "
                   "centre on an INVERSION curriculum; an abstention objective alone treats the "
                   "wrong disease.")
    elif all(a["exact_p"] >= 0.05 for a in (m7, m11)):
        verdict = ("🧱 **M1 WRITE-ABSENT** — the forward map is at chance too, so nothing was "
                   "written in either direction. ⇒ the INVERSION curriculum has nothing to invert "
                   "and is dead before it costs a GPU-hour; the recipe must first make the corpus "
                   "WRITE the association.")
    else:
        verdict = "⏳ SEED-SPLIT — the two seeds disagree; both reported, no fork resolved."
    if base["exact_p"] < 0.05:
        verdict += (f"\n  ⚠️ base_only also reads {base['sign_acc']:.3f} (p={base['exact_p']:.4f}) — "
                    "the effect is not grid-specific; it may be generic corpus sentiment "
                    "co-occurrence rather than anything the N2 recipe installed.")
    print(f"VERDICT: {verdict}")
    out["verdict"] = verdict
    json.dump(out, open(os.path.join(HERE, f"audit_a1_{split}.json"), "w"), ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
