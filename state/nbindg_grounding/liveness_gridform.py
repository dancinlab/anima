"""H_9302 fork — is the readout broken, or is it grid->natural transfer that is missing?

probe_liveness.py showed the probe cannot read the polarity of the 20 atoms the model was TAUGHT,
when it reads them off a NATURAL review context. Two very different worlds explain that:

  A  the readout is broken   — a linear probe on __last cannot recover polarity from ANY context,
                               taught or not. Then the instrument is junk and nothing this lane
                               measured means anything.
  B  the TRANSFER is missing — the model was taught in the grid format ("이 영화 <atom> => 긍정.")
                               and answers it (H_9286: SEEN 0.950), but that polarity never rides
                               in the representation of a natural review. Then the instrument is
                               FINE and "taught in format X, not readable in format Y" is a real,
                               reportable finding about the substrate.

The two are told apart by one prompt swap: probe the SAME atoms in the format they were TAUGHT.
Grid-format prompt = the grid line truncated right after the atom (identical treatment to the
natural contexts, so only the carrier format differs).

  readable in grid format   -> B: the readout works; grid->natural transfer is the wall
  unreadable there too      -> A: the readout is dead; every negative in this lane is INVALID
"""

from __future__ import annotations

import json
import math
import os
import subprocess

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

HERE = os.path.dirname(os.path.abspath(__file__))
ANIMA = os.path.expanduser("~/.local/bin/anima-py")
CKPT = os.path.expanduser("~/anima-weights/natem_n2")
ARMS = ["main_s7", "main_s11", "base_only", "shuffle_grid"]
WIN = 24
SEED = 7


def build():
    """Grid lines for the 20 taught atoms, truncated right after the atom — same treatment the
    natural contexts get, so the only thing that changes is the carrier."""
    atoms = [a for a in json.load(open(os.path.join(HERE, "gt_atoms_n92.json")))["atoms"]
             if a["split"] == "train"]
    lines = [l.strip() for l in open(os.path.join(HERE, "n2_main_train.txt")) if "=>" in l]
    items, meta = [], []
    for a in atoms:
        hits = [l for l in lines if a["stem"] in l.split("=>")[0]]
        ids = []
        for j, l in enumerate(hits[:24]):
            body = l.split("=>")[0]
            i = body.find(a["stem"])
            frag = body[: i + len(a["stem"])]
            pid = f"G_{a['stem']}__{j}"
            items.append({"id": pid, "prompt": frag})
            ids.append(pid)
        if ids:
            meta.append({"stem": a["stem"], "pol": a["pol"], "ids": ids})
    json.dump({"items": items}, open(os.path.join(HERE, "grid_prompts.json"), "w"),
              ensure_ascii=False)
    return meta, items


def loo(X, y, atom):
    hit_c, hit_a, n = 0, 0, 0
    for a in np.unique(atom):
        te = atom == a
        s = StandardScaler().fit(X[~te])
        m = LogisticRegression(max_iter=2000, C=0.1).fit(s.transform(X[~te]), y[~te])
        p = m.predict(s.transform(X[te]))
        hit_c += int((p == y[te]).sum()); n += int(te.sum())
        hit_a += int((p.mean() > 0.5) == (y[te][0] > 0.5))
    return hit_c / n, hit_a / len(np.unique(atom))


def main() -> int:
    meta, items = build()
    print(f"H_9302-FORK — the SAME probe, on the format the model was TAUGHT")
    print(f"  {len(meta)} taught atoms · {len(items)} grid-format prompts "
          f"(e.g. “{items[0]['prompt']}”)\n")
    out = {"n_atom": len(meta), "n_prompt": len(items), "arms": {}}
    for arm in ARMS:
        npz_p = os.path.join(HERE, "hid", f"grid_{arm}.npz")
        if not os.path.exists(npz_p):
            subprocess.run([ANIMA, "evaluate", os.path.join(CKPT, f"natem_n2_{arm}.clm"),
                            "--dump-hidden", os.path.join(HERE, "grid_prompts.json"),
                            "--out", npz_p, "--win", str(WIN)], check=True, capture_output=True)
        npz = np.load(npz_p)
        X, y, at = [], [], []
        for ai, a in enumerate(meta):
            for i in a["ids"]:
                if i + "__last" in npz.files:
                    X.append(npz[i + "__last"]); y.append(a["pol"]); at.append(ai)
        X, y, at = np.array(X, np.float64), np.array(y), np.array(at)
        c, p = loo(X, y, at)
        out["arms"][arm] = {"per_context": c, "per_atom": p, "n": int(len(y))}
        kind = "EXPERIMENT" if arm.startswith("main") else "control  "
        print(f"  {kind} {arm:>13} | per-context {c:.3f}  ·  per-atom {p:.3f}   (n={len(y)})")

    m = [out["arms"][a]["per_context"] for a in ("main_s7", "main_s11")]
    c = [out["arms"][a]["per_context"] for a in ("base_only", "shuffle_grid")]
    print()
    if min(m) > max(c) and min(m) > 0.6:
        out["verdict"] = ("B — TRANSFER MISSING. The readout WORKS: it reads the taught polarity in "
                          "the taught format, and the untaught controls cannot. So the instrument is "
                          "sound and the real finding is that grid-taught polarity never rides in "
                          "the representation of a NATURAL review — a format-transfer wall, not an "
                          "extraction-channel wall.")
    else:
        out["verdict"] = ("A — READOUT DEAD. The probe cannot read polarity even in the format the "
                          "model was taught and answers at 0.95. A linear read of __last is simply "
                          "not where this model keeps polarity ⇒ every negative in this lane is "
                          "INVALID and the instrument must be redesigned before any verdict.")
    print("VERDICT:", out["verdict"])
    json.dump(out, open(os.path.join(HERE, "probe_liveness_grid.json"), "w"),
              ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
