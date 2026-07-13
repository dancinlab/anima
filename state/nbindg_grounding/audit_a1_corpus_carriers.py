"""A1-REPAIR — the same fork, asked with carriers the model has actually seen.

H_9299 built A1 (does the model carry the polarity in the GENERATIVE direction — p(atom|context) —
even though it cannot answer p(polarity|atom)?) and then killed it with its own positive control:
on the 74 atoms the corpus grounds HARDEST (occ ≥ 100, purity ≥ 0.90, 최고/별로/빠르/재미없), at a
power where a true 0.70 would have shown as 3.4σ, the probe read 0.554 (p = 0.208). A probe that
cannot see the forward map even THERE certifies nothing when it reads chance on held-out atoms.

Two suspects were named for why the probe is deaf. This file addresses the first.

  SUSPECT 1 — the carriers were AUTHORED. "배송도 빠르고 품질도 좋아서 정말 " is a sentence I
  wrote; the 303M never saw it. Its NLL surface there may be dominated by the strangeness of the
  prompt rather than by sentiment. So: mine the carriers from the corpus instead — real review
  prefixes, from reviews whose LABEL is strongly positive or strongly negative, cut at a word
  boundary before any occurrence of the atom under test.

  SUSPECT 2 — NLL is the wrong readout; generation might carry what likelihood does not. That is
  the next file, not this one.

Design, and what each piece defends against:

  · 30 positive + 30 negative real prefixes (not 2 + 2). Junction grammar — which atom happens to
    fit after which ending — is exactly what poisoned the authored version. With 30 diverse real
    endings per side, the junction idiosyncrasy averages out instead of aliasing onto polarity.
  · a NEUTRAL carrier set as a third arm (prefixes from reviews with no strong polarity). It is
    the baseline: a healthy probe should separate ⁺ from ⁻ and leave neutral in between. If ⁺, ⁻
    and neutral all coincide, the probe is deaf regardless of what the arm contrast says.
  · the atom's own bytes are scored EXACTLY (one manifest per atom byte-length) — the fixed
    score_len of the first attempt scored past the atom and into the carrier, and since the
    carriers differ across arms, that contaminated the very contrast being measured.
  · the certification order is unchanged and non-negotiable: A4-STRONG first (n=74, powered), and
    the held-out numbers are not even READ unless it passes.
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
N_CARRIER = 30          # real review prefixes per polarity — junction noise averages over these
CARRIER_BYTES = 48      # prefix length, cut at a space so it ends on a word
SEED = 7


def mine_carriers(rows, atoms):
    """Real review prefixes, cut at a word boundary, containing NO atom under test.

    A carrier that already contains one of the probe's atoms would leak the answer, so every
    candidate is rejected if any test atom's stem appears in it.
    """
    import random
    rng = random.Random(SEED)
    stems = {a["stem"] for a in atoms}
    pos, neg = [], []
    idx = list(range(len(rows)))
    rng.shuffle(idx)
    for i in idx:
        text, lab = rows[i]
        b = text.encode()
        if len(b) < CARRIER_BYTES + 8:
            continue
        frag = b[:CARRIER_BYTES].decode("utf-8", "ignore")
        cut = frag.rfind(" ")
        if cut < 20:
            continue
        frag = frag[: cut + 1]                      # ends on a space → a clean word boundary
        if any(s in frag for s in stems):           # no leakage of a test atom into its own carrier
            continue
        (pos if lab == 1 else neg).append(frag)
        if len(pos) >= N_CARRIER and len(neg) >= N_CARRIER:
            break
    return pos[:N_CARRIER], neg[:N_CARRIER]


def build_manifests(atoms, carriers, tag):
    """One manifest per atom byte-length; `b` indexes the carrier."""
    by_len = {}
    for i, a in enumerate(atoms):
        by_len.setdefault(len(a["stem"].encode()), []).append((i, a))
    out = []
    for L, group in sorted(by_len.items()):
        items = [{"text": c + a["stem"], "a": i, "b": j}
                 for i, a in group for j, c in enumerate(carriers)]
        p = os.path.join(HERE, f"a1c_manifest_{tag}_L{L}.json")
        json.dump({"win": WIN, "score_len": L, "items": items}, open(p, "w"), ensure_ascii=False)
        out.append((L, p))
    return out


def run_arm(arm, manifests, tag):
    nll = {}
    for L, mani in manifests:
        o = os.path.join(HERE, f"a1c_nll_{tag}_L{L}_{arm}.json")
        if not os.path.exists(o):
            subprocess.run([ANIMA, "evaluate", os.path.join(CKPT_DIR, f"natem_n2_{arm}.clm"),
                            "--interaction-lift", mani, "--out", o,
                            "--win", str(WIN), "--score-len", str(L)],
                           check=True, capture_output=True)
        for k, v in json.load(open(o))["cells"].items():
            a, b = (int(x) for x in k.split(","))
            nll[(a, b)] = float(np.mean(v))
    return nll


def main() -> int:
    split = sys.argv[1] if len(sys.argv) > 1 else "strong"
    sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "nbind_curriculum")))
    sys.path.insert(0, HERE)
    import gen_nbindg_n2 as GN2

    if split == "strong":
        atoms = json.load(open(os.path.join(HERE, "a4_strong_atoms.json")))["atoms"]
    else:
        meta = json.load(open(os.path.join(HERE, "gt_atoms_n92.json")))["atoms"]
        atoms = [a for a in meta if a["split"] == split]
    n = len(atoms)
    sd = math.sqrt(0.25 / n)

    rows = GN2.load_corpora()
    c_pos, c_neg = mine_carriers(rows, atoms)
    n_pos, n_neg = len(c_pos), len(c_neg)
    carriers = c_pos + c_neg
    print(f"A1-REPAIR · split={split} · n={n} · chance sd={sd:.4f} "
          f"(bar 0.70 = {(0.70-0.5)/sd:.1f}σ)")
    print(f"  carriers mined from the corpus: {n_pos}⁺ / {n_neg}⁻ real review prefixes "
          f"(~{CARRIER_BYTES}B, word-boundary, atom-free)")
    print(f"  e.g. ⁺ “{c_pos[0][:34]}…”   ⁻ “{c_neg[0][:34]}…”\n")

    manifests = build_manifests(atoms, carriers, split)
    out = {"split": split, "n": n, "chance_sd": sd, "n_carrier": [n_pos, n_neg], "arms": {}}

    for arm in ARMS:
        nll = run_arm(arm, manifests, split)
        d, gold = [], []
        for i, a in enumerate(atoms):
            p = np.mean([nll[(i, j)] for j in range(n_pos)])
            q = np.mean([nll[(i, n_pos + j)] for j in range(n_neg)])
            d.append(q - p)                    # NLL⁻ − NLL⁺ = log p(a|C⁺) − log p(a|C⁻)
            gold.append(a["pol"])
        d, gold = np.array(d), np.array(gold)
        hit = (d > 0) == (gold == 1)
        acc = float(hit.mean())
        p1 = float(stats.binom.sf(int(hit.sum()) - 1, n, 0.5))
        r = float(stats.pointbiserialr(gold, d).statistic)
        t = stats.ttest_ind(d[gold == 1], d[gold == 0])
        out["arms"][arm] = {"sign_acc": acc, "sigma": (acc - 0.5) / sd, "exact_p": p1,
                            "r_pb": r, "t_p": float(t.pvalue),
                            "mean_d_pos": float(d[gold == 1].mean()),
                            "mean_d_neg": float(d[gold == 0].mean())}
        print(f"  {arm:>13} | sign-acc {acc:.3f} ({(acc-0.5)/sd:+.2f}σ) · exact p={p1:.4f} "
              f"· r_pb={r:+.3f} · t-test p={t.pvalue:.4f}")
        print(f"  {'':>13} | mean Δ: 긍정 원자 {d[gold==1].mean():+.3f} · 부정 원자 "
              f"{d[gold==0].mean():+.3f}")

    m7, m11 = out["arms"]["main_s7"], out["arms"]["main_s11"]
    live = all(a["exact_p"] < 0.05 for a in (m7, m11))
    print()
    if split == "strong":
        if live:
            v = ("✅ PROBE CERTIFIED — with corpus-mined carriers the forward map IS visible on the "
                 "atoms the corpus grounds hardest. The authored carriers were the defect. "
                 "⇒ now, and only now, read the held-out split.")
        else:
            v = ("🧱 PROBE STILL DEAF — corpus-mined carriers do not rescue it either, at a power "
                 "where a true 0.70 would be 3.4σ. NLL-contrast is the wrong readout for this "
                 "question ⇒ the M1/M2 fork needs the GENERATION probe, not likelihood.")
    else:
        v = ("held-out numbers — meaningful ONLY if the strong-split certification passed; "
             "otherwise they certify nothing (H_9299).")
    print(f"VERDICT: {v}")
    out["verdict"] = v
    json.dump(out, open(os.path.join(HERE, f"audit_a1c_{split}.json"), "w"),
              ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
