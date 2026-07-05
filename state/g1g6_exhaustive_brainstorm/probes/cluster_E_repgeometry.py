#!/usr/bin/env python3
"""CLUSTER E (표현·아키텍처) — FROZEN-REP GEOMETRY falsifier.  $0, mini, ONE 303M load.

QUESTION (brainstorm §0 piece 2 — 표현 벽):
  role·relation·direction 이 frozen 303M latent 에 분리되어 있는가? (factorized basis?)
  For the G1 RECOMBINATION wall: is the frozen trunk rep of a concept PAIR additive
  (superposition / DPI floor) with NO factorized role subspace, or does it carry
  non-additive interaction + orthogonal role subspaces an E1..E12 op could exploit?

TWO TESTS, ONE LOAD:
  T1 ADDITIVE-INTERACTION (DPI floor at geometry): 2-way ANOVA interaction variance
     fraction R = ||h(a,b)-mean-U[a]-V[b]||² / ||h(a,b)-mean||².  R≈0 -> pure
     superposition (DPI floor). R large -> real compositional interaction present.
  T2 FACTORIZED-BASIS (orthogonal role subspaces — the literal 'factorized basis'):
     principal angles between span(U=slot-1) and span(V=slot-2). max_overlap_cos≈1
     -> roles SHARE one direction (no factorization, additive bag). ≈0 -> roles are
     in orthogonal subspaces (factorized — an E3/E4/E6/E11 op could read them apart).

PREREG FROZEN BARS (set BEFORE running; a_break_the_wall, no tune-to-green):
  REP-WALL-AT-GEOMETRY  iff  R <= 0.10  AND  max_overlap_cos >= 0.90
     (>=90% additive AND the two role slots collapse to one shared direction: no
      factorized basis, no bindable structure in frozen rep. E3/E5/E8/E9/E11 on the
      frozen rep = rethread of additive floor (H_1816/H_1822/exp3); only trunk-
      internal E1/E4/E6/E10 — all GPU-gated — can inject factorization.)
  REP-WALL-NOT-HERE     iff  R >= 0.25  OR   max_overlap_cos <= 0.30
     (real interaction OR genuinely orthogonal role subspaces: the frozen rep DOES
      have exploitable factorized structure; the wall is downstream — readout/mouth/
      search — and cluster-E trunk arch changes are unnecessary.)
  else INCONCLUSIVE.
  Secondary (last-token confounded): rev_asym = ||h(a,b)-h(b,a)|| / ||h(a,b)-h(a,b')||.

ENGINE-NATIVE: core/decode.py bg_load + bg_forward_last_hidden = the py 2-production
numpy path the canonical G1 --py measurement uses (H_6190). Single forward per seed;
h1129.bin loaded ONCE. No training, no decode loop, no tune-to-green.

usage: OMP_NUM_THREADS=4 python3 cluster_E_repgeometry.py [ckpt.bin]
"""
import os, sys, json, time
import numpy as np
sys.path.insert(0, "/Users/mini/dancinlab/anima/core")
import decode as D

CKPT = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
    "~/anima-weights/bytegpt303_h1129/h1129.bin")
CONCEPTS = ["ocean", "forest", "engine", "music", "market", "medicine",
            "desert", "galaxy", "kitchen", "law", "glacier", "circuit"]

def fwd_hidden(W, s):
    ids = list(s.encode("utf-8", "surrogateescape"))
    return D.bg_forward_last_hidden(W, ids, len(ids))

def main():
    t0 = time.time()
    print(f"[load] {CKPT}", flush=True)
    W = D.bg_load(CKPT)
    d = W["d"]; nlay = W["nlay"]; nh = W["nh"]; vocab = W["vocab"]
    print(f"[load] d={d} nlay={nlay} nh={nh} vocab={vocab} bind={bool(W.get('bind'))}", flush=True)
    n = len(CONCEPTS)
    H = np.zeros((n, n, d), dtype=np.float64)
    for a in range(n):
        for b in range(n):
            H[a, b] = fwd_hidden(W, f"{CONCEPTS[a]}. {CONCEPTS[b]}.")
            if ((a*n+b+1) % 24 == 0):
                print(f"[fwd] {a*n+b+1}/{n*n}  ({time.time()-t0:.1f}s)", flush=True)
    print(f"[fwd] done ({time.time()-t0:.1f}s)", flush=True)

    # T1: 2-way ANOVA additive-interaction
    mean_all = H.mean(axis=(0, 1))
    U = H.mean(axis=1) - mean_all    # slot-1 (first concept)  [n,d]
    V = H.mean(axis=0) - mean_all    # slot-2 (last concept)   [n,d]
    fit = mean_all + U[:, None, :] + V[None, :, :]
    inter = H - fit
    R = float(np.sum(inter**2) / max(np.sum((H - mean_all)**2), 1e-300))
    U_share = float(np.linalg.norm(U) / max(np.linalg.norm(H - mean_all), 1e-300))
    V_share = float(np.linalg.norm(V) / max(np.linalg.norm(H - mean_all), 1e-300))

    # T2: factorized basis — principal angles between span(U) and span(V)
    Qu, _ = np.linalg.qr(U.T)   # d x n
    Qv, _ = np.linalg.qr(V.T)
    s = np.linalg.svd(Qu.T @ Qv, compute_uv=False)  # cosines of principal angles
    max_overlap = float(s[0])
    mean_overlap = float(np.mean(s[:min(len(s), 11)]))

    # secondary: reversal asymmetry (last-token confounded)
    rev_d = []; swap_d = []
    for a in range(n):
        for b in range(n):
            if a == b: continue
            rev_d.append(np.linalg.norm(H[a, b] - H[b, a]))
            bp = (b + 1) % n
            if bp == a: bp = (b + 2) % n
            swap_d.append(np.linalg.norm(H[a, b] - H[a, bp]))
    rev_asym = float(np.mean(rev_d) / max(np.mean(swap_d), 1e-300))

    if R <= 0.10 and max_overlap >= 0.90:
        verdict = "REP-WALL-AT-GEOMETRY"
    elif R >= 0.25 or max_overlap <= 0.30:
        verdict = "REP-WALL-NOT-HERE"
    else:
        verdict = "INCONCLUSIVE"

    out = {
        "ckpt": CKPT, "d": int(d), "nlay": int(nlay), "n_concepts": n,
        "T1_interaction_R": R, "T1_additive_share": 1.0 - R,
        "T1_slot1_firstconcept_signal_share": U_share,
        "T1_slot2_lastconcept_signal_share": V_share,
        "T2_max_overlap_cos": max_overlap, "T2_mean_overlap_cos": mean_overlap,
        "T2_principal_angle_cos_top5": [float(x) for x in s[:5]],
        "secondary_reversal_asym": rev_asym,
        "prereg_bar": {"R_low": 0.10, "R_high": 0.25, "overlap_high": 0.90, "overlap_low": 0.30},
        "verdict": verdict, "elapsed_s": round(time.time() - t0, 1),
    }
    print("\n=== CLUSTER E FROZEN-REP GEOMETRY VERDICT ===")
    print(json.dumps(out, indent=2))
    print("\n--- read ---")
    print(f"first-concept(slot1) carries {U_share*100:.1f}% of pair-rep variance; "
          f"last-concept(slot2) {V_share*100:.1f}%; interaction {R*100:.1f}%.")
    print(f"role-subspace max-overlap cos={max_overlap:.3f} "
          f"({'shared/no-factorization' if max_overlap>=0.9 else 'orthogonal/factorized' if max_overlap<=0.3 else 'partial'}).")
    if verdict == "REP-WALL-AT-GEOMETRY":
        print("-> E3/E5/E8/E9/E11 on frozen rep = rethread (H_1816/H_1822/exp3 floor).")
        print("-> Only E1/E4/E6/E10 (trunk-internal, GPU-gated) can inject factorization.")
    elif verdict == "REP-WALL-NOT-HERE":
        print("-> Frozen rep HAS exploitable factorized structure; wall is downstream (B).")
    else:
        print("-> Ambiguous: mostly additive, weak/partial role separation.")

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "cluster_E_repgeometry_result.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n[saved] cluster_E_repgeometry_result.json ({out['elapsed_s']}s)")

if __name__ == "__main__":
    main()
