#!/usr/bin/env python3
"""gen_nbindg.py — NBIND-G carrier-transfer manifest (N1 · $0 · existing H_9272 ckpt).

Fable NBIND-G arbitration (2026-07-12): H_9272 (🟡 DIRECTIONAL, held-out D-acc 0.700)
proved the XBIND recipe survives natural-Korean sentiment atoms — but its grid arm is
substantially XBIND re-skinned (authored xor over natural vocabulary). The genuinely NEW
question = ATOM-GROUNDING TRANSFER: does the grid-learned XOR operator apply to atoms whose
polarity is grounded ONLY in natural distributional usage?

GROUND-TRUTH CONSTRAINT (reference-matched on gen_nbind.py, this turn): H_9272's training
corpus (nbind_train.txt) is 100% authored grid lines `이 영화 <surf> => <긍정/부정>.` — ZERO
raw NSMC review text. Therefore:
  · The GROUNDING claim (P_nat atoms, polarity from nature) CANNOT be tested on the existing
    ckpt (no grounding source) → it is the N2 spend-gated retrain (raw-NSMC-in-mix).
  · The only VALID $0 falsifier on the existing ckpt uses the 20 GROUNDED grid predicates
    (seen D-acc 0.92) and keeps the in-distribution `=> 긍정/부정` readout. The single
    transferable variable is the CARRIER (the frame before <surf>, trained as "이 영화 ").

N1 = CARRIER-DISTANCE LADDER (this file). Same 40 held-out (p,form) cells as H_9272, three
carrier levels:
  C0  "이 영화 <surf> => "                      training carrier → reproduce 0.700 (control)
  C1  "<alt movie-domain NP> <surf> => "         near transfer (carrier-lexeme swap)
  C2  "<verbatim real NSMC review> <surf> => "   wild-natural transfer (Fable bar-3 done
                                                  validly: real-review context, grounded
                                                  atoms, valid readout)
Verdict logic (frozen, decided now):
  · C0 must reproduce ≈0.70 (±0.10) else ckpt/harness INVALID (verdict-integrity).
  · CARRIER-ROBUST 🟢-dir : C1 & C2 both ≥ C0−0.10  → operator is carrier-general, not bound
                            to the literal training frame (strengthens H_9272; compositional).
  · FORMAT-🧱             : C1 and/or C2 collapse to chance (≤0.55) while C0 reproduces →
                            operator bound to the authored frame; DATA-🧱 hardens, and the
                            grounding claim rests entirely on N2 (retrain).
Any outcome leaves H_9267 CRACK and H_9272 DIRECTIONAL untouched. No tune-to-green: bars
frozen here, before the run; ckpt is fixed (no retrain in N1).

Also freezes P_nat_freeze.json — the ≥30 held-out grounding atoms for the N2 spend-gated
grounding program (built now so N2 cannot cherry-pick atoms post-hoc).

Usage:
  python3 gen_nbindg.py --out-dir . [--nsmc <path>] [--seed 7]
Readout: `anima-py evaluate <ckpt> --xbind nbindg_carrier_ladder_manifest.json --arm main`.
"""
import json
import os
import random
import sys

# reuse the FROZEN H_9272 pipeline verbatim (reference-match, no re-invention)
_NBIND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "nbind_curriculum")
sys.path.insert(0, _NBIND_DIR)
import gen_nbind as GN

# C1 near-transfer carriers: natural movie-review noun phrases (domain-matched, atom-neutral)
C1_CARRIERS = ["이 배우", "그 장면", "이 드라마", "이 작품", "그 연기", "이 감독"]
N_C2_CTX = 6            # distinct real-review contexts cycled for C2 (per-item rng pick)
C2_MIN, C2_MAX = 8, 40  # verbatim review char length band for a clean short context


def _clean_reviews(rows, exclude_stems, n_want, rng):
    """short verbatim NSMC reviews that contain NONE of the grid predicate stems (no leak)."""
    out = []
    for text, _lab in rows:
        t = text.strip()
        if not (C2_MIN <= len(t) <= C2_MAX):
            continue
        if any(st in t for st in exclude_stems):
            continue
        if "=>" in t or "긍정" in t or "부정" in t:
            continue
        out.append(t)
        if len(out) >= n_want * 40:
            break
    rng.shuffle(out)
    return out[: n_want * 40] or ["재밌게 봤어요"]


def build_ladder(rows, seed):
    B = GN.build(rows, seed)                 # exact H_9272 grid (same 20 preds, held cells)
    NF = dict((f[0], f[2]) for f in GN.NEG_FORMS)
    preds, pol = B["preds"], B["pol"]
    er = random.Random(seed + 97)            # eval rng, decoupled from train rng
    stems = set(B["plist"])
    ctx_pool = _clean_reviews(rows, stems, N_C2_CTX, er)

    def item(p, fid, carrier, level):
        bit = B["out_bit"](p, fid)
        span = er.choice(preds[p]["spans"]) if preds[p]["spans"] else (None, p)
        surf = GN.render(p, span[1], span[0], NF[fid])
        seed_s = carrier + " " + surf + " => "
        return {"p": p, "form": fid, "a": p, "b": fid, "carrier_level": level,
                "carrier": carrier, "pol": pol[p], "flip": GN.FLIP[fid], "xor": bit,
                "surf": surf, "seed": seed_s,
                "gold": ("긍정." if bit else "부정."),
                "counterfactual": ("부정." if bit else "긍정."),
                "gold_word": "긍정" if bit else "부정"}

    held = B["heldout_cells"]                 # 40 cells (20 preds x 2)
    c0, c1, c2 = [], [], []
    for (p, fid) in held:
        c0.append(item(p, fid, "이 영화", "C0"))
        c1.append(item(p, fid, er.choice(C1_CARRIERS), "C1"))
        c2.append(item(p, fid, er.choice(ctx_pool), "C2"))

    # V-F leak guard: no seed may reveal the target token.
    for it in c0 + c1 + c2:
        assert "긍정" not in it["seed"] and "부정" not in it["seed"], it["seed"]

    manifest = {
        "format": "nbind-eval-v1", "task": "NBIND-G carrier-transfer ladder (N1)",
        "note": "XBIND-isomorphic --xbind readout. 3 carrier levels C0(train)/C1(near)/"
                "C2(wild-natural). Existing H_9272 ckpt, no retrain. Grounded grid atoms.",
        "gen": 8, "win": 64,
        "heldout": c0 + c1 + c2,             # evaluator scores all; split by carrier_level
        "seen": [],
        "levels": {"C0": len(c0), "C1": len(c1), "C2": len(c2)},
    }
    return B, manifest


def freeze_pnat(rows, B):
    """P_nat = predicates NOT in the 20-pred grid, frozen for the N2 grounding retrain.

    The strict H_9272 thresholds (purity>=0.90) are EXHAUSTED by the 20-pred grid — the
    purity-certified sentiment inventory is tiny (~10/polarity). That scarcity is itself a
    NATEM finding. For a valid N2 inventory we relax purity to Fable §3.1's bar (>=0.85),
    keeping the structural predicate filters (ending-diversity, syllable, non-past) so P_nat
    atoms are still real inflecting predicates. Record exactly what was relaxed (honesty).
    """
    grid = set(B["plist"])
    sweep = {}
    best = None
    for pur in (0.90, 0.85, 0.80):
        preds = GN.mine_predicates(rows, GN.MINOCC, pur)
        extra = [(p, d) for p, d in preds.items() if p not in grid]
        pos = sorted([(p, d) for p, d in extra if d["pol"] == 1], key=lambda x: -x[1]["n"])
        neg = sorted([(p, d) for p, d in extra if d["pol"] == 0], key=lambda x: -x[1]["n"])
        k = min(len(pos), len(neg), 15)
        sweep["purity>=%.2f" % pur] = {"n_extra_pos": len(pos), "n_extra_neg": len(neg),
                                       "k_per_pol": k}
        if best is None and k >= 10:
            best = (pur, preds, pos[:k] + neg[:k], k)
    if best is None:            # even at 0.80 the inventory is too small
        pur, preds, chosen, k = 0.80, GN.mine_predicates(rows, GN.MINOCC, 0.80), [], 0
    else:
        pur, preds, chosen, k = best
    p_nat = [p for p, _ in chosen]
    return {"note": "N2 grounding atoms: NOT in H_9272 grid. Frozen pre-N2 so the spend-"
                    "gated retrain cannot cherry-pick atoms post-hoc. purity relaxed from "
                    "0.90 (grid-exhausted) to the loosest bar giving k>=10 per polarity.",
            "purity_used": pur, "purity_sweep": sweep,
            "n_grid": len(grid), "n_pnat": len(p_nat), "k_per_pol": k,
            "p_nat": [{"stem": p, "pol": preds[p]["pol"], "n": preds[p]["n"],
                       "purity": preds[p]["purity"]} for p in p_nat],
            "INVALID_if": "k<10 at purity>=0.80 (insufficient grounding inventory)"}


def main():
    args = sys.argv[1:]

    def val(flag, default, cast):
        return cast(args[args.index(flag) + 1]) if flag in args else default

    out_dir = val("--out-dir", ".", str)
    nsmc = val("--nsmc", None, str)
    seed = val("--seed", 7, int)

    rows = GN.load_nsmc(nsmc)
    B, manifest = build_ladder(rows, seed)
    pnat = freeze_pnat(rows, B)

    with open(out_dir + "/nbindg_carrier_ladder_manifest.json", "w") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    with open(out_dir + "/P_nat_freeze.json", "w") as f:
        json.dump(pnat, f, ensure_ascii=False, indent=1)

    meta = {"seed": seed, "n_grid_preds": len(B["plist"]),
            "n_heldout_cells": len(B["heldout_cells"]),
            "levels": manifest["levels"], "n_items": len(manifest["heldout"]),
            "pnat_frozen": pnat["n_pnat"], "pnat_valid": pnat["n_pnat"] >= 20,
            "example_seeds": {lv: next(it["seed"] for it in manifest["heldout"]
                                       if it["carrier_level"] == lv)
                              for lv in ("C0", "C1", "C2")}}
    with open(out_dir + "/N0_AUDIT.json", "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    print(json.dumps(meta, ensure_ascii=False, indent=1))
    if not meta["pnat_valid"]:
        print("P_nat inventory < 20 — N2 grounding program would be INVALID", file=sys.stderr)


if __name__ == "__main__":
    main()
