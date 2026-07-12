#!/usr/bin/env python3
"""H_9289 GT-TRANSFER STEP-0 — G-PROBE triage ($0 · frozen N2 ckpt).

Distinguishes INFO-PRESENT (held-out atom polarity IS linearly readable from the frozen N2
representation, sign just needs anchoring) vs INFO-ABSENT (polarity not in the repr at all).

Pipeline (two phases):
  build : mine natural-context prompts per atom (P_grid train + P_nat held-out) -> gt_prompts.json
          + gt_atoms.json (atom->pol, split).  Reuses gen_nbindg / gen_nbindg_n2 VERBATIM so the
          atom sets are byte-identical to what N2 trained/eval'd (reference-match, no cherry-pick).
  probe : load per-ckpt --dump-hidden npz -> mean-pool each atom's contexts -> L2-logreg probe
          trained on P_grid polarity, tested on held-out P_nat.  Controls: shuffle-label (capacity
          floor) + base_only ckpt (learned-content floor).  Verdict per the frozen H_9289 branch.

Frozen branch (H_9289): held-out probe-acc >= 0.65 BOTH main seeds AND base_only <= shuffle+0.05
  -> INFO-PRESENT (MAIN=C2).  else INFO-ABSENT (MAIN=C3+C4 hybrid corpus).
No tune-to-green: bars fixed here, pre-registered in the card before any measurement.
"""
import os, sys, json, random
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

SEED = 7
K_CTX = 24                        # natural-context prompts sampled per atom
WIN = 24                         # dump-hidden right-align window (matches --win)
POS_BAR = 0.65                   # frozen INFO-PRESENT bar (held-out probe-acc, both seeds)
L2 = 5.0                         # strong L2 (n_train ~20 << d ~768 -> heavy reg mandatory)


def _atom_sets(seed=SEED):
    """P_grid (train, model learned polarity) + P_nat viable (held-out) — byte-identical to N2.
    gen modules imported lazily here so the `probe` phase (npz-only) needs no corpus/module deps."""
    sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "nbind_curriculum")))
    sys.path.insert(0, HERE)
    import gen_nbind as GN             # H_9272 module: load_nsmc/build/pol/plist
    import gen_nbindg_n2 as GN2        # load_corpora + audit_pnat + V-F filter (imports gen_nbind)
    rows = GN2.load_corpora()
    nsmc_rows = list(GN.load_nsmc(None))
    B = GN.build(nsmc_rows, seed)
    grid_stems = list(B["plist"]); grid_pol = B["pol"]
    viable, cand, audit = GN2.audit_pnat(rows, set(grid_stems), seed)
    authored = "\n".join(B["main_lines"] + B["ctrl_lines"])
    viable = [p for p in viable if p not in authored]
    grid = [{"stem": s, "pol": int(grid_pol[s]), "split": "train"} for s in grid_stems]
    nat = [{"stem": p, "pol": int(cand[p]["pol"]), "split": "heldout"} for p in viable]
    return grid + nat, rows, audit


def _contexts(stem, rows, rng, k=K_CTX):
    """k natural reviews containing the stem, TRUNCATED right after the stem so the atom lands
    at the end of the right-aligned window (its contextualized hidden = __last)."""
    hits = [t for (t, _l) in rows if stem in t]
    rng.shuffle(hits)
    out = []
    for t in hits:
        i = t.find(stem)
        frag = t[: i + len(stem)]
        frag = frag[-64:]
        if frag.strip():
            out.append(frag)
        if len(out) >= k:
            break
    return out


def cmd_build():
    atoms, rows, audit = _atom_sets()
    rng = random.Random(SEED)
    items, atom_meta = [], []
    for a in atoms:
        ctx = _contexts(a["stem"], rows, rng)
        if len(ctx) < 6:
            continue
        ids = []
        for j, frag in enumerate(ctx):
            pid = "%s__%d" % (a["stem"], j)
            items.append({"id": pid, "prompt": frag})
            ids.append(pid)
        atom_meta.append({"stem": a["stem"], "pol": a["pol"], "split": a["split"], "ids": ids})
    json.dump({"items": items}, open(os.path.join(HERE, "gt_prompts.json"), "w"),
              ensure_ascii=False)
    json.dump({"atoms": atom_meta, "n_prompts": len(items),
               "n_train": sum(1 for a in atom_meta if a["split"] == "train"),
               "n_heldout": sum(1 for a in atom_meta if a["split"] == "heldout")},
              open(os.path.join(HERE, "gt_atoms.json"), "w"), ensure_ascii=False, indent=1)
    print("BUILD: %d prompts · %d train atoms · %d heldout atoms" %
          (len(items), sum(1 for a in atom_meta if a["split"] == "train"),
           sum(1 for a in atom_meta if a["split"] == "heldout")))


def _atom_reps(npz, atom_meta, key="__last"):
    X, y, split, stems = [], [], [], []
    for a in atom_meta:
        vs = [npz[i + key] for i in a["ids"] if (i + key) in npz.files]
        if not vs:
            continue
        X.append(np.mean(np.stack(vs, 0), 0))
        y.append(a["pol"]); split.append(a["split"]); stems.append(a["stem"])
    return np.stack(X, 0).astype(np.float64), np.array(y), np.array(split), stems


def _logreg_l2(Xtr, ytr, Xte, l2=L2, iters=800, lr=0.1):
    """Tiny standardized L2 logistic regression (numpy). Heavy reg for n<<d."""
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6
    Xtr = (Xtr - mu) / sd; Xte = (Xte - mu) / sd
    n, d = Xtr.shape
    w = np.zeros(d); b = 0.0
    yb = ytr.astype(np.float64)
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-(Xtr @ w + b)))
        gw = Xtr.T @ (p - yb) / n + l2 * w / n
        gb = float(np.mean(p - yb))
        w -= lr * gw; b -= lr * gb
    pte = 1.0 / (1.0 + np.exp(-(Xte @ w + b)))
    return pte


def cmd_probe(npz_paths):
    atom_meta = json.load(open(os.path.join(HERE, "gt_atoms.json")))["atoms"]
    out = {"bar_pos": POS_BAR, "K_ctx": K_CTX, "L2": L2, "per_ckpt": {}}
    for label, path in npz_paths.items():
        if not os.path.exists(path):
            out["per_ckpt"][label] = {"error": "npz missing"}
            continue
        npz = np.load(path)
        X, y, split, stems = _atom_reps(npz, atom_meta)
        tr = split == "train"; te = split == "heldout"
        if tr.sum() < 4 or te.sum() < 4:
            out["per_ckpt"][label] = {"error": "too few atoms",
                                      "n_tr": int(tr.sum()), "n_te": int(te.sum())}
            continue
        pte = _logreg_l2(X[tr], y[tr], X[te])
        acc = float(np.mean((pte >= 0.5).astype(int) == y[te]))
        rng = np.random.RandomState(SEED)
        accs_sh = []
        for _ in range(20):
            ysh = rng.permutation(y[tr])
            psh = _logreg_l2(X[tr], ysh, X[te])
            accs_sh.append(float(np.mean((psh >= 0.5).astype(int) == y[te])))
        sh = float(np.mean(accs_sh))
        per_atom = sorted([(stems[i], int(y[te][k]), float(pte[k]))
                           for k, i in enumerate(np.where(te)[0])], key=lambda z: z[2])
        out["per_ckpt"][label] = {
            "heldout_probe_acc": round(acc, 4), "shuffle_acc": round(sh, 4),
            "delta_vs_shuffle": round(acc - sh, 4),
            "n_train_atoms": int(tr.sum()), "n_heldout_atoms": int(te.sum()),
            "per_atom_prob": [[s, p, round(pr, 3)] for s, p, pr in per_atom],
        }
    s7 = out["per_ckpt"].get("main_s7", {}); s11 = out["per_ckpt"].get("main_s11", {})
    base = out["per_ckpt"].get("base_only", {})
    a7 = s7.get("heldout_probe_acc", 0); a11 = s11.get("heldout_probe_acc", 0)
    shref = max(s7.get("shuffle_acc", 0.5), s11.get("shuffle_acc", 0.5))
    ab = base.get("heldout_probe_acc", 1.0)
    info_present = (a7 >= POS_BAR and a11 >= POS_BAR and ab <= shref + 0.05)
    out["verdict"] = {
        "main_s7_acc": a7, "main_s11_acc": a11, "base_only_acc": ab, "shuffle_ref": shref,
        "INFO_PRESENT": bool(info_present),
        "call": ("INFO-PRESENT -> MAIN=C2(GT-curriculum)" if info_present
                 else "INFO-ABSENT -> MAIN=C3+C4 hybrid corpus"),
    }
    json.dump(out, open(os.path.join(HERE, "gt_step0_result.json"), "w"),
              ensure_ascii=False, indent=1)
    print(json.dumps(out["verdict"], ensure_ascii=False))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    if cmd == "build":
        cmd_build()
    elif cmd == "probe":
        base = sys.argv[2] if len(sys.argv) > 2 else HERE
        cmd_probe({
            "main_s7": os.path.join(base, "gt_hidden_main_s7.npz"),
            "main_s11": os.path.join(base, "gt_hidden_main_s11.npz"),
            "base_only": os.path.join(base, "gt_hidden_base_only.npz"),
            "shuffle_grid": os.path.join(base, "gt_hidden_shuffle_grid.npz"),
        })
    else:
        print("usage: gt_step0_gprobe.py build|probe [npz_dir]")
