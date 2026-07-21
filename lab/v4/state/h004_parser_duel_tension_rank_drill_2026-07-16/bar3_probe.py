#!/usr/bin/env python3
"""bar3 discriminator — does C-perm's drill-true-gold 0.64 REACH the held-out f2″ harness gate?

fit-check bar3 measured C-perm on the DRILL surface (training-dist, memorizable) = 0.6432 > 0.60.
The FROZEN harness gate measures C-perm on HELD-OUT f2″ (lexeme-disjoint from drill; run-1 = 0.45/0.5).
This probe retrains C-perm at fit-check scale (d=64/L2, CPT 200 + drill 1500, the fixed objective) and
reports BOTH surfaces, plus A-duel f2″ as a live reference:
  • C-perm drill-true-gold high AND f2″ ≈ 0.5  ⇒ benign drill-memorization; bar3 gates the wrong surface.
  • C-perm f2″ > 0.6                             ⇒ genuine surface-leak reaches held-out ⇒ panel defect.
$0-ish (~5 min MPS). Reuses train_h004's train_arm/_load/dacc_panel verbatim (one-variable intact).
"""
from __future__ import annotations
import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import train_h004 as T


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true",
                    help="d=384/L4 at the full-run config (CPT 8000 + drill 4000) — decisive size confound")
    a = ap.parse_args()
    import torch
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    torch_, M, cfg, Struct = T._load(smoke=not a.full)           # d=64/L2  or  d=384/L4
    drill = json.load(open(os.path.join(_HERE, "drill_grid_multi.json"), encoding="utf-8"))
    f2 = json.load(open(os.path.join(_HERE, "panel_f2doubleprime.json"), encoding="utf-8"))
    f1 = json.load(open(os.path.join(_HERE, "panel_f1prime.json"), encoding="utf-8"))
    n_cpt, seqlen, steps = (120000, 512, (8000, 4000)) if a.full else (2000, 128, (200, 1500))
    cpt_win = T._cpt_windows(T._nsmc_lines(n_cpt), seqlen, torch_)
    print(f"bar3-probe: d={cfg.d_model}/L{cfg.n_trunk_layers} on {device}, "
          f"CPT {steps[0]} + drill {steps[1]} (fixed objective) …", flush=True)
    out = {"device": device, "d_model": cfg.d_model, "arms": {}}
    for arm in ("C-perm", "A-duel"):
        model, ce_ans = T.train_arm(arm, 0, (torch_, M, cfg, Struct), {"f2": f2, "f1": f1},
                                    drill, cpt_win, steps, device, tag=None)
        rec = {
            "drill_true_gold": round(T.dacc_panel(model, torch_, drill[:64], arm, 0, device), 4),
            "f2doubleprime_heldout": round(T.dacc_panel(model, torch_, f2, arm, 1, device), 4),
            "ce_ans_final": round(ce_ans, 4),
        }
        out["arms"][arm] = rec
        print(f"    {arm}: drill(true)={rec['drill_true_gold']}  "
              f"f2''(held-out)={rec['f2doubleprime_heldout']}  ce_ans={rec['ce_ans_final']}", flush=True)
    cperm_f2 = out["arms"]["C-perm"]["f2doubleprime_heldout"]
    out["cperm_f2_in_harness_band"] = 0.45 <= cperm_f2 <= 0.55
    out["reading"] = ("benign drill-memorization — bar3 gates the wrong surface (C-perm clean on held-out)"
                      if cperm_f2 <= 0.55 else
                      "GENUINE LEAK — C-perm beats chance on held-out f2''; panel/objective defect")
    fn = f"bar3_probe_result_d{cfg.d_model}.json"
    with open(os.path.join(_HERE, fn), "w") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    print(f"\nC-perm held-out f2'' = {cperm_f2} (harness band [0.45,0.55]: "
          f"{'IN' if out['cperm_f2_in_harness_band'] else 'OUT'})")
    print("READING:", out["reading"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
