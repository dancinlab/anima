#!/usr/bin/env python3
"""
H_9129 rung-2 — REAL 303M engine representation extractor (h1129 ByteGPT).

Escalates the STEP-0 integrated PFC-BG-hippo lane (state/g1_combolane_step0/
integrated/combolane.py) from TOY random hypervectors to REAL 303M engine
representations. The atomic concept vectors that the HRR bind/gate/completion
pipeline operates on are pulled from the ACTUAL h1129.bin forward pass, using the
EXACT engine ops imported from core/decode.py (byte-parity with cli/evaluate.hexa)
— not an arbitrary numpy embedding.

Representation = residual-stream hidden state at the FINAL layer (pre-ln_f), the
richest engine summary of a concept byte-string (the vector the tied head reads).
Two pre-registered pooling forms are cached (chosen BEFORE seeing lane results):
  - mean-pool over the concept's byte positions   (primary symbol — stable)
  - last-token residual                            (causal sequence summary)

WHY engine-native (honest scope): the vectors ARE the real 303M engine's forward
output (core/decode.py bg_load + the exact _bg_mha/_bg_layernorm_rows/_bg_gelu
ops). This is NOT the `anima evaluate --py` decode-scoring path (the lane is not
wired into core/ yet — that is rung-3), so the overall verdict stays DIRECTIONAL
per a_engine_native_learning; but the REPRESENTATIONS are engine-grounded, the
decisive upgrade over STEP-0's ideal random vectors.
"""
import os, sys, json
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "core"))

import decode as D  # exact engine ops (byte-parity with cli/evaluate.hexa)

CKPT = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")


def residual_reps(W, s):
    """Run the EXACT h1129 forward (core/decode ops) and return the FINAL-layer
    residual stream x:[T,d] (pre-ln_f). This mirrors bg_forward_last_W's loop
    verbatim but keeps the full [T,d] residual instead of only last-pos logits."""
    d = W["d"]; nlay = W["nlay"]; nh = W["nh"]
    ids = D._seed_to_ids(s)
    T = len(ids)
    ids = np.asarray(ids, dtype=np.int64)
    x = W["tok"][ids] + W["pos"][0:T]                      # [T, d]
    for Lr in range(nlay):
        nrm = D._bg_layernorm_rows(x, W["ln1w"][Lr], W["ln1b"][Lr], T, d)
        aout = D._bg_mha(nrm, W["inW"][Lr], W["inB"][Lr],
                         W["oW"][Lr], W["oB"][Lr], T, d, nh)
        x = x + aout
        nrm = D._bg_layernorm_rows(x, W["ln2w"][Lr], W["ln2b"][Lr], T, d)
        h4 = D._bg_gelu(nrm @ W["m0W"][Lr].T + W["m0B"][Lr])
        mlpo = h4 @ W["m2W"][Lr].T + W["m2B"][Lr]
        x = x + mlpo
    return x                                               # [T, d] float64 residual


# ── 3 concept pools (role-filler symbols) = REAL common English nouns in the
#    model's ko/en byte distribution. 24 per pool, all distinct, dict words. ──
POOL_A = ["ocean","forest","engine","music","market","medicine","desert","galaxy",
          "kitchen","river","mountain","garden","factory","harbor","meadow","volcano",
          "library","bridge","tunnel","glacier","circuit","reactor","furnace","canyon"]
POOL_B = ["salt","moss","fuel","chord","price","fever","dune","comet",
          "flour","stone","pine","seed","steel","rope","grass","ash",
          "paper","cable","brick","frost","wire","atom","coal","clay"]
POOL_C = ["deep","green","hot","loud","cheap","sick","dry","bright",
          "warm","hard","soft","cold","sharp","dark","fresh","heavy",
          "light","rough","smooth","frozen","thin","dense","wide","narrow"]


def main():
    print("[extract] loading h1129 303M (float64, ~2.4GB) …", flush=True)
    W = D.bg_load(CKPT)
    print("[extract] loaded. d=%d nlay=%d nh=%d vocab=%d"
          % (W["d"], W["nlay"], W["nh"], W["vocab"]), flush=True)
    pools = {"A": POOL_A, "B": POOL_B, "C": POOL_C}
    out = {}
    for pk, words in pools.items():
        mean_rows = []; last_rows = []
        for i, w in enumerate(words):
            x = residual_reps(W, w)                        # [T,d]
            mean_rows.append(x.mean(axis=0))
            last_rows.append(x[-1])
            print("  [%s %2d/%d] %-10s T=%d |mean|=%.2f"
                  % (pk, i + 1, len(words), w, x.shape[0],
                     float(np.linalg.norm(x.mean(axis=0)))), flush=True)
        out["%s_mean" % pk] = np.array(mean_rows)
        out["%s_last" % pk] = np.array(last_rows)
    np.savez(os.path.join(_HERE, "reps_h1129.npz"), **out)
    # honest diagnostics: how non-orthogonal / non-uniform are REAL 303M reps?
    diag = {}
    for form in ("mean", "last"):
        allv = np.concatenate([out["%s_%s" % (pk, form)] for pk in pools])
        norms = np.linalg.norm(allv, axis=1)
        vn = allv / (norms[:, None] + 1e-9)
        G = vn @ vn.T
        off = G[~np.eye(len(G), dtype=bool)]
        diag[form] = {
            "n": int(len(allv)),
            "norm_min": float(norms.min()), "norm_max": float(norms.max()),
            "norm_ratio": float(norms.max() / norms.min()),
            "offdiag_cos_mean": float(off.mean()),
            "offdiag_cos_abs_mean": float(np.abs(off).mean()),
            "offdiag_cos_max": float(off.max()),
        }
    with open(os.path.join(_HERE, "reps_diag.json"), "w") as f:
        json.dump(diag, f, indent=2)
    print("\n[extract] DIAGNOSTICS (real 303M reps vs ideal random):", flush=True)
    for form, dd in diag.items():
        print("  %-4s norm_ratio=%.1f  offdiag|cos|_mean=%.3f  cos_max=%.3f"
              % (form, dd["norm_ratio"], dd["offdiag_cos_abs_mean"],
                 dd["offdiag_cos_max"]), flush=True)
    print("  (ideal random hypervectors: norm_ratio~1.0, |cos|_mean~1/sqrt(d)=%.3f)"
          % (1.0 / np.sqrt(W["d"])), flush=True)


if __name__ == "__main__":
    main()
