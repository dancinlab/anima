"""H_9297 — rebuild the G-PROBE prompt set with the code cap lifted (held-out n: 29/30 → 92).

H_9296 established that the whole NBIND-G G-PROBE frame sits on n=29 held-out atoms, where the
frozen 0.65 bar is only 1.62σ above chance — so H_9289's "INFO-ABSENT" (0.5517 = 16/29, one-sided
p = 0.356) is NOT-POWERED, not null. Its own NEXT said the fix needs a bigger or different corpus.

That was wrong, and this script is the receipt. Re-counting the SAME 450k corpus with every
certification bar untouched (purity ≥ 0.85, occ ≥ 100, syll ≤ 3, non-grid, non-past) yields
pos 46 / neg 67. The 29 came from a line in gen_nbindg_n2.py:

    k = min(len(pos), len(neg), 15)          <- a self-imposed CODE cap, not a data limit

Lift it and held-out n becomes 92, which moves the bar from 1.62σ to 2.88σ — the difference
between a frame that cannot distinguish "moderate signal" from "no signal" and one that can.

Everything else is byte-identical to H_9289: same 4 frozen ckpts, same K_CTX=24 / WIN=24 window,
same left-context truncation, same split, same bar. Only the atom count moves.

    python3 gt_power_build.py            # → gt_prompts_n92.json + gt_atoms_n92.json
"""

from __future__ import annotations

import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 7
# H_9301 — K_CTX is the THIRD code cap in this lane (after k_cap=15 and WIN=24). The corpus holds
# a median of 717 usable contexts per atom (min 182, max 24,899), and this cap binds on 111/111
# atoms, discarding 197,169 of them. The probe MEAN-POOLS an atom's contexts, so the cap is a
# sqrt(K_hi/24) noise penalty paid for nothing. Env-driven so H_9289/H_9297 stay byte-reproducible
# at the default; H_9301 fires at K_CTX=182 (the minimum every atom can supply, so no atom is
# pooled over fewer contexts than any other).
K_CTX = int(os.environ.get("K_CTX", "24"))
K_CAP = 10 ** 9     # THE ONE CHANGE: no ceiling on atoms per polarity
MIN_CTX = 6         # an atom needs at least this many usable contexts (H_9289 verbatim)
OCC_FLOOR = 30      # pre-registered exposure floor — an atom the model barely saw proves nothing


def _contexts(stem, rows, rng, k=None):
    """k natural reviews containing the stem, TRUNCATED right after it so the atom lands at the
    end of the right-aligned window (its contextualised hidden = __last). H_9289 verbatim."""
    k = K_CTX if k is None else k
    hits = [t for (t, _l) in rows if stem in t]
    rng.shuffle(hits)
    out = []
    for t in hits:
        i = t.find(stem)
        frag = t[: i + len(stem)][-64:]
        if frag.strip():
            out.append(frag)
        if len(out) >= k:
            break
    return out


def main() -> int:
    sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "nbind_curriculum")))
    sys.path.insert(0, HERE)
    import gen_nbind as GN
    import gen_nbindg_n2 as GN2

    rows = GN2.load_corpora()
    nsmc_rows = list(GN.load_nsmc(None))
    B = GN.build(nsmc_rows, SEED)
    grid_stems = list(B["plist"])
    grid_pol = B["pol"]

    viable, cand, audit = GN2.audit_pnat(rows, set(grid_stems), SEED, k_cap=K_CAP)
    authored = "\n".join(B["main_lines"] + B["ctrl_lines"])
    collide = [p for p in viable if p in authored]          # V-F: stem nested in an authored line
    viable = [p for p in viable if p not in collide]

    thin = [p for p in viable if cand[p]["n"] < OCC_FLOOR]  # V-EXPOSURE
    viable = [p for p in viable if cand[p]["n"] >= OCC_FLOOR]

    atoms = ([{"stem": s, "pol": int(grid_pol[s]), "split": "train"} for s in grid_stems]
             + [{"stem": p, "pol": int(cand[p]["pol"]), "split": "heldout"} for p in viable])

    rng = random.Random(SEED)
    items, meta = [], []
    for a in atoms:
        ctx = _contexts(a["stem"], rows, rng)
        if len(ctx) < MIN_CTX:
            continue
        ids = []
        for j, frag in enumerate(ctx):
            pid = f"{a['stem']}__{j}"
            items.append({"id": pid, "prompt": frag})
            ids.append(pid)
        meta.append({"stem": a["stem"], "pol": a["pol"], "split": a["split"],
                     "occ": int(cand[a["stem"]]["n"]) if a["split"] == "heldout" else None,
                     "ids": ids})

    n_tr = sum(1 for a in meta if a["split"] == "train")
    n_te = sum(1 for a in meta if a["split"] == "heldout")
    tag = "n92" if K_CTX == 24 else f"k{K_CTX}"
    json.dump({"items": items}, open(os.path.join(HERE, f"gt_prompts_{tag}.json"), "w"),
              ensure_ascii=False)
    json.dump({"atoms": meta, "n_prompts": len(items), "n_train": n_tr, "n_heldout": n_te,
               "k_cap": "lifted", "v_f_collision_dropped": collide,
               "v_exposure_thin_dropped": thin, "occ_floor": OCC_FLOOR,
               "cand_pos": audit["n_cand_pos"], "cand_neg": audit["n_cand_neg"],
               "k_ctx": K_CTX},
              open(os.path.join(HERE, f"gt_atoms_{tag}.json"), "w"), ensure_ascii=False, indent=1)

    import math
    sd = math.sqrt(0.25 / n_te)
    print(f"certified candidates: pos {audit['n_cand_pos']} · neg {audit['n_cand_neg']}  "
          f"(bars untouched: purity ≥ {GN2.PURITY_NAT} · occ ≥ {GN2.MINOCC_NAT})")
    print(f"V-F authored-collision dropped: {len(collide)}   V-EXPOSURE thin dropped: {len(thin)}")
    print(f"BUILD: {len(items)} prompts · {n_tr} train atoms · **{n_te} held-out atoms** "
          f"(was 29 under the k=15 cap)")
    print(f"power: chance sd = {sd:.4f}  ⇒  the frozen 0.65 bar now sits {(0.65 - 0.5) / sd:.2f}σ "
          f"above chance (was 1.62σ)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
