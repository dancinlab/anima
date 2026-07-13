"""H_9297 — the G-PROBE, re-run with the frame finally powered (held-out n: 29 → 91).

H_9296 showed the NBIND-G probe frame could not answer its own question: at n=29 the frozen 0.65
bar sits 1.62σ above chance, so H_9289's 0.5517 (16/29, one-sided p = 0.356) was NOT-POWERED, not
null — and the frontier's whole next move ("INFO-ABSENT ⇒ the wall is the extraction channel ⇒
design the O/C channel") rests on that first link.

H_9296 concluded the fix needed a bigger corpus. It did not. Re-counting the SAME 450k with every
certification bar untouched gives pos 46 / neg 67; the 29 came from `k = min(len(pos), len(neg),
15)` — a code cap. Lifting it yields 91 held-out atoms and moves the bar to 2.86σ, which is the
difference between a frame that cannot tell "moderate signal" from "no signal" and one that can.

Pre-registered in PREREG_H9297.md and committed before these hiddens were dumped. Everything is
byte-identical to H_9289 except the atom count: same 4 frozen ckpts, same contexts, same bar 0.65.

Two things are deliberately different from H_9296, and both are repairs, not loosenings:
  · primary is P-LIN ALONE. H_9296 already showed probe capacity is not the culprit, so running
    four probes as co-primaries would only inflate the multiple-comparison surface. The rest are
    monitors.
  · the control is a 200-draw label-PERMUTATION null, judged by percentile — not a band. H_9296's
    ±0.08 band was ±0.86σ at n=29, so a chance-level shuffle escaped it 39% of the time BY
    CONSTRUCTION, and the gate tripped on sampling noise rather than memorisation. Not repeating it.
"""

from __future__ import annotations

import json
import math
import os

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
BAR = 0.65                # frozen in H_9289 — not moved
L2 = 1e-3
SEED = 7
N_PERM = 200              # V-PERM: the null distribution, not a band
ARMS = ["main_s7", "main_s11", "base_only", "shuffle_grid"]
REPRO_TARGET, REPRO_TOL = 0.5517, 0.05     # V-REPRO on the ORIGINAL 29-atom subset


def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))


def logreg(Xtr, ytr, Xte, l2=L2, iters=800, lr=0.1):
    """L2 logistic regression — byte-faithful to H_9289's `_logreg_l2`."""
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-8
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    w, b = np.zeros(Xtr.shape[1]), 0.0
    for _ in range(iters):
        p = _sigmoid(Xtr @ w + b)
        w -= lr * (Xtr.T @ (p - ytr) / len(ytr) + l2 * w)
        b -= lr * float((p - ytr).mean())
    return _sigmoid(Xte @ w + b), _sigmoid(Xtr @ w + b)


def mlp(Xtr, ytr, Xte, hidden=32, l2=L2, iters=1500, lr=0.05, seed=SEED):
    rng = np.random.default_rng(seed)
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-8
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    d = Xtr.shape[1]
    W1 = rng.normal(0, 1 / np.sqrt(d), (d, hidden)); b1 = np.zeros(hidden)
    w2 = rng.normal(0, 1 / np.sqrt(hidden), hidden); b2 = 0.0
    n = len(ytr)
    for _ in range(iters):
        h = np.tanh(Xtr @ W1 + b1)
        p = _sigmoid(h @ w2 + b2)
        dz = (p - ytr) / n
        dh = np.outer(dz, w2) * (1 - h ** 2)
        W1 -= lr * (Xtr.T @ dh + l2 * W1); b1 -= lr * dh.sum(0)
        w2 -= lr * (h.T @ dz + l2 * w2); b2 -= lr * float(dz.sum())
    return (_sigmoid(np.tanh(Xte @ W1 + b1) @ w2 + b2),
            _sigmoid(np.tanh(Xtr @ W1 + b1) @ w2 + b2))


WIN = int(os.environ.get("PROBE_WIN", "24"))


def load(arm: str):
    """The hidden dump for this arm at the window under test.

    H_9300: `--win` is a BYTE budget (evaluate.py: "T=24 right-aligned byte encode"), and the
    original G-PROBE ran at 24 bytes ≈ 8 Korean characters — while the oracle it is contrasted
    against read the whole 64-character fragment. The polarity evidence sits in the earlier part of
    the context, which the model's dumped representation never saw. So the window is the one thing
    this file varies; everything else is H_9297 verbatim.
    """
    tag = "gt_n92" if WIN == 24 else f"w{WIN}"
    npz = np.load(os.path.join(HERE, "hid", f"{tag}_{arm}.npz"))
    meta = json.load(open(os.path.join(HERE, "gt_atoms_n92.json")))["atoms"]
    prompts = {i["id"]: i["prompt"]
               for i in json.load(open(os.path.join(HERE, "gt_prompts_n92.json")))["items"]}
    ctx, y, split, stems, occ, blen = [], [], [], [], [], []
    for a in meta:
        ids = [i for i in a["ids"] if (i + "__last") in npz.files]
        if not ids:
            continue
        ctx.append(np.stack([npz[i + "__last"] for i in ids], 0).astype(np.float64))
        blen.append(np.mean([len(prompts[i].encode()) for i in ids if i in prompts]))
        y.append(a["pol"]); split.append(a["split"]); stems.append(a["stem"]); occ.append(a["occ"])
    return ctx, np.array(y), np.array(split), stems, occ, np.array(blen)


def length_only(blen, y, tr, te):
    """V-LENGTH-A — the confound floor: what does the byte LENGTH alone score?

    Held-out prompt byte-length correlates with polarity at r = -0.301, and --win pads short
    prompts with spaces, so length is readable straight off the representation. A one-feature
    length probe run through the real pipeline (fit on train, test on held-out) reads 0.648 —
    at the frozen 0.65 bar. Any arm that does not BEAT this floor has not shown polarity.
    """
    x = blen[:, None]
    pte, _ = logreg(x[tr], y[tr].astype(float), x[te])
    return float(((pte > 0.5) == y[te]).mean())


def residualize(pooled, blen, tr):
    """V-LENGTH-B — regress the length direction OUT of the features, then probe the residual.

    Fit (on TRAIN only, so the held-out labels never touch the fit) hidden ~ a + b*byte_length,
    and keep the residual. Polarity that survives here is not length.
    """
    x = np.c_[np.ones(len(blen)), blen]
    coef, *_ = np.linalg.lstsq(x[tr], pooled[tr], rcond=None)
    return pooled - x @ coef


def loo_cv(pooled, y, tr):
    """V-CV — replaces V-FIT. train n=20 in d=768: train_fit == 1.000 for every arm by
    construction (20 points are always separable), so the fit gate certifies nothing.
    Leave-one-out on the 20 train atoms is a gate that can actually fail."""
    Xtr, ytr = pooled[tr], y[tr].astype(float)
    n = len(ytr)
    hits = 0
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        p, _ = logreg(Xtr[m], ytr[m], Xtr[i:i + 1])
        hits += int((p[0] > 0.5) == (ytr[i] > 0.5))
    return hits / n


def main() -> int:
    out = {"bar": BAR, "n_perm": N_PERM, "arms": {}}
    old29 = set(json.load(open(os.path.join(HERE, "gt_atoms.json")))["atoms"][i]["stem"]
                for i in range(len(json.load(open(os.path.join(HERE, "gt_atoms.json")))["atoms"]))
                if json.load(open(os.path.join(HERE, "gt_atoms.json")))["atoms"][i]["split"]
                == "heldout") if os.path.exists(os.path.join(HERE, "gt_atoms.json")) else set()

    for arm in ARMS:
        ctx, y, split, stems, occ, blen = load(arm)
        tr, te = split == "train", split == "heldout"
        pooled = np.stack([c.mean(0) for c in ctx], 0)
        n_te = int(te.sum())
        sd = math.sqrt(0.25 / n_te)

        # ── primary: P-LIN ────────────────────────────────────────────────
        pte, ptr = logreg(pooled[tr], y[tr].astype(float), pooled[te])
        hits = (pte > 0.5) == y[te]
        acc = float(hits.mean())
        fit = float(((ptr > 0.5) == y[tr]).mean())

        # ── V-LENGTH (prereg amendment II) — the confound floor + the length-free probe ──
        len_floor = length_only(blen, y, tr, te)
        res = residualize(pooled, blen, tr)
        rte, _ = logreg(res[tr], y[tr].astype(float), res[te])
        acc_res = float(((rte > 0.5) == y[te]).mean())
        cv20 = loo_cv(pooled, y, tr)

        # V-PERM: 200-draw label-permutation null (percentile, not a band)
        rng = np.random.default_rng(SEED)
        null = np.array([float(((logreg(pooled[tr], rng.permutation(y[tr]).astype(float),
                                        pooled[te])[0] > 0.5) == y[te]).mean())
                         for _ in range(N_PERM)])
        p95 = float(np.quantile(null, 0.95))
        pval = float((null >= acc).mean())

        # monitors (not primary — H_9296 already cleared probe capacity)
        mte, _ = mlp(pooled[tr], y[tr].astype(float), pooled[te])
        mon_nl = float(((mte > 0.5) == y[te]).mean())

        # the ORIGINAL 29-atom subset, scored inside this same run (V-REPRO anchor)
        sub = np.array([s in old29 for s in stems]) & te
        acc29 = float((((pte > 0.5) == y[te])[np.isin(np.where(te)[0], np.where(sub)[0])]).mean()) \
            if sub.sum() else float("nan")

        out["arms"][arm] = {
            "n_heldout": n_te, "chance_sd": sd, "bar_sigma": (BAR - 0.5) / sd,
            "P_LIN": acc, "train_fit": fit, "perm_null_p95": p95, "perm_p": pval,
            "P_NL_monitor": mon_nl, "acc_on_old29_subset": acc29,
            "exact_p_binom": float(stats.binom.sf(round(acc * n_te) - 1, n_te, 0.5)),
            "LENGTH_ONLY_floor": len_floor, "P_LIN_length_residual": acc_res, "loo_cv_train20": cv20,
        }
        r = out["arms"][arm]
        print(f"{arm:>13} | n={n_te:3d} · sd {sd:.4f} · bar = {r['bar_sigma']:.2f}σ")
        print(f"{'':>13} | P-LIN {acc:.3f} (train {fit:.2f})  vs perm-null p95 {p95:.3f} "
              f"· perm p = {pval:.3f} · exact p = {r['exact_p_binom']:.3f}")
        print(f"{'':>13} | [V-LENGTH] length-only floor {len_floor:.3f} · length-residual "
              f"P-LIN {acc_res:.3f}   [V-CV] LOO(train20) {cv20:.3f}")
        print(f"{'':>13} | [monitor] P-NL {mon_nl:.3f}   [V-REPRO] old-29 subset {acc29:.3f}")

    m7, m11 = out["arms"]["main_s7"], out["arms"]["main_s11"]
    v = {
        "V_REPRO": all(abs(a["acc_on_old29_subset"] - REPRO_TARGET) <= REPRO_TOL
                       for a in (m7, m11)),
        # V_FIT is retired (prereg amendment II): train n=20 in d=768 ⇒ fit == 1.000 for every arm
        # by construction, so it is a gate that cannot fail. LOO on the 20 train atoms can.
        "V_CV": all(out["arms"][a]["loo_cv_train20"] >= 0.60 for a in ("main_s7", "main_s11")),
        "V_BASE": out["arms"]["base_only"]["P_LIN"] < BAR,
    }
    print()
    for k, ok in v.items():
        print(f"{k:>8}: {'PASS' if ok else 'FAIL'}")
    out["v_gates"] = {k: bool(x) for k, x in v.items()}

    detect = all(a["P_LIN"] >= BAR and a["perm_p"] < 0.05 for a in (m7, m11))
    partial = all(a["perm_p"] < 0.05 for a in (m7, m11)) and not detect
    split_seed = (m7["perm_p"] < 0.05) != (m11["perm_p"] < 0.05)

    # V-LENGTH (prereg amendment II) — only bites when the arms actually rise. A rise that does
    # not beat the length-only floor, or that dies once length is regressed out, is length.
    beats_floor = all(a["P_LIN"] > a["LENGTH_ONLY_floor"] for a in (m7, m11))
    survives_res = all(a["P_LIN_length_residual"] >= BAR for a in (m7, m11))
    length_confound = (detect or partial) and not (beats_floor and survives_res)
    print(f"{'V_LENGTH':>8}: {'PASS' if (beats_floor and survives_res) else 'FAIL'} "
          f"(beats length-only floor: {beats_floor} · survives length-residual: {survives_res})")
    out["v_gates"]["V_LENGTH"] = bool(beats_floor and survives_res)

    print()
    if not all(v.values()):
        verdict = "⏳ INVALID — a standing V-gate failed; no tier is reported."
    elif length_confound:
        verdict = ("⏳ LENGTH-CONFOUND — the arms rise, but the rise does not clear the length-only "
                   "floor (0.648, at the bar) or does not survive regressing length out. The probe "
                   "read pad-length, not polarity. No tier; redesign on a length-invariant prompt "
                   "set.")
    elif detect:
        verdict = ("🔓 INFO-PRESENT — INFO-ABSENT RETRACTED. The signal was in the representation; "
                   "H_9289's verdict was a power failure, and the frontier's O/C-channel diagnosis "
                   "needs re-examination.")
    elif split_seed:
        verdict = "⏳ SEED-SPLIT — the two seeds disagree; both reported, no tier."
    elif partial:
        verdict = ("🟡 PARTIAL — above the permutation null but below the frozen 0.65 bar. Partial "
                   "signal is really there; the bar does not move, the effect size is reported.")
    else:
        verdict = (f"🧱 INFO-ABSENT CONFIRMED — now EARNED. At n={m7['n_heldout']} the bar sits "
                   f"{m7['bar_sigma']:.2f}σ above chance and the probe still reads chance "
                   "(perm-null not cleared). The representation really lacks it ⇒ the O/C-channel "
                   "move is the right next step.")
    print(f"VERDICT: {verdict}")
    out["verdict"] = verdict
    json.dump(out, open(os.path.join(HERE, f"probe_power_w{WIN}.json"), "w"), ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
