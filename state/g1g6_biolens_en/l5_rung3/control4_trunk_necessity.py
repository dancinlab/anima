#!/usr/bin/env python3
"""H_9129 L5 rung(3) — CONTROL 4: TRUNK-NECESSITY (the missing crux control).

The rung-3 discriminator (l5_discriminator.py) proved novel-chain != stored-recall
(FORM / SHUFFLE / LANE-OFF / LESION all pass, store_gap +0.8631, 7.31x). But that
does NOT separate two mechanisms:
  (G1) trunk recombination — the 303M reps themselves carry the compositional
       structure and the store merely reads it out, OR
  (G2) explicit-store — the heteroassociative store + near-orthogonal DG codes
       chain premises by transitive closure REGARDLESS of what the reps are.

This control (Fable rung-3 design, deliverable 4/6) rebuilds the store with RANDOM
near-orthogonal codes of the same dim/sparsity replacing the 303M reps — everything
else (random projection seed, center_zscore, DG k-WTA, outer-product store, k-WTA
completion, the SAME chains/edges/novel-pairs) held identical. Only `reps` differ.

  cement-as-G1 (trunk necessity)  iff  store_gap_real >= 2 * store_gap_random
  else                             ->  the chaining is a property of the store, not
                                       the trunk  =>  G2 explicit-store, WALL for G1.

$0, no best-of-K; the random arm needs no model. Reuses l5_discriminator.py verbatim
(import, not copy) so the pipeline is byte-1:1 with the GREEN rung-3 measurement.
Frozen bar pre-registered here BEFORE running (a_break_the_wall, no tune-to-green)."""
import os
import sys
import time
import json
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "core"))   # decode.py (== anima evaluate --py ops)
sys.path.insert(0, _HERE)                          # l5_discriminator.py
import l5_discriminator as L5                       # reuse EXACT rung-3 pipeline (import, not copy)

# ── frozen bar (pre-registered) ──────────────────────────────────────────────
G1_RATIO_BAR = 2.0        # store_gap_real must be >= 2x store_gap_random to claim trunk-G1
SEED = L5.SEED
CL   = L5.CHAIN_LEN
NC   = L5.N_CHAINS


def build_pairs(items):
    """Reconstruct edges / novel_pairs / unreach EXACTLY as l5_discriminator.main()."""
    N = len(items)
    def chain_of(k): return k // CL
    full_edges = []
    for c in range(NC):
        base = c * CL
        for p in range(CL - 1):
            full_edges.append((base + p, base + p + 1))
    recall_pairs, novel_pairs = [], []
    for c in range(NC):
        base = c * CL
        for a in range(CL):
            if a + 1 < CL:
                recall_pairs.append((base + a, base + a + 1))
            for b in range(a + 2, CL):
                novel_pairs.append((base + a, base + b))
    rng = np.random.default_rng(SEED)   # main() module-level rng, unconsumed before unreach
    unreach, seen = [], set()
    while len(unreach) < len(novel_pairs):
        i = int(rng.integers(N)); j = int(rng.integers(N))
        if chain_of(i) == chain_of(j):
            continue
        k = (min(i, j), max(i, j))
        if k in seen:
            continue
        seen.add(k); unreach.append((i, j))
    return full_edges, recall_pairs, novel_pairs, unreach


def measure(reps, full_edges, novel_pairs, unreach):
    """Identical dg->store->relatedness pipeline; returns (novel_mean, unreach_mean, gap, overlap)."""
    R = L5.preprocess(reps, L5.PREPROC)
    codes = L5.dg_codes(R, np.random.default_rng(SEED))   # same projection seed both arms
    Wfull = L5.build_store(codes, full_edges)
    nc = np.array([L5.relatedness(Wfull, codes, i, j) for i, j in novel_pairs])
    ur = np.array([L5.relatedness(Wfull, codes, i, j) for i, j in unreach])
    avg_overlap = float(np.mean([float(codes[a] @ codes[b]) / L5.ACTIVE
                                 for a in range(len(reps)) for b in range(a + 1, len(reps))]))
    return float(nc.mean()), float(ur.mean()), float(nc.mean() - ur.mean()), avg_overlap


def main():
    t0 = time.time()
    print("[1/4] rebuild identical corpus chains (l5_discriminator verbatim) ...", flush=True)
    lines = L5.load_lines()
    vocab, freq, co = L5.build_graph(lines)
    chains = L5.greedy_chains(vocab, freq, co)
    assert len(chains) == NC, f"chains={len(chains)} != {NC}"
    items = [w for ch in chains for w in ch]
    full_edges, recall_pairs, novel_pairs, unreach = build_pairs(items)
    print(f"      items={len(items)} edges={len(full_edges)} novel={len(novel_pairs)} "
          f"unreach={len(unreach)}", flush=True)

    print("[2/4] REAL arm — 303M h1129 reps (fidelity check vs frozen 0.8631) ...", flush=True)
    W = L5.d.bg_load(L5.CKPT)
    assert L5.d.bg_is_bytegpt(L5.CKPT), "not bytegpt"
    reps_real = np.zeros((len(items), W["d"]), dtype=np.float64)
    for k, w in enumerate(items):
        reps_real[k] = L5.rep303(W, w)
    nc_r, ur_r, gap_r, ov_r = measure(reps_real, full_edges, novel_pairs, unreach)
    print(f"      REAL  novel={nc_r:.4f} unreach={ur_r:.4f} store_gap={gap_r:+.4f} "
          f"dg_overlap={ov_r:.4f}  ({time.time()-t0:.1f}s)", flush=True)

    print("[3/4] RANDOM arm — trunk-necessity control (iid gaussian near-orth reps) ...",
          flush=True)
    rep_rng = np.random.default_rng(SEED + 1)          # separate stream; reps only diff
    reps_rand = rep_rng.standard_normal((len(items), W["d"])).astype(np.float64)
    nc_x, ur_x, gap_x, ov_x = measure(reps_rand, full_edges, novel_pairs, unreach)
    print(f"      RAND  novel={nc_x:.4f} unreach={ur_x:.4f} store_gap={gap_x:+.4f} "
          f"dg_overlap={ov_x:.4f}", flush=True)

    print("[4/4] verdict ...", flush=True)
    ratio = gap_r / gap_x if gap_x > 1e-9 else float("inf")
    trunk_necessary = gap_r >= G1_RATIO_BAR * gap_x
    verdict = "G1-TRUNK (GREEN-eligible)" if trunk_necessary else "G2-EXPLICIT-STORE (WALL for G1)"

    L = []
    L.append("# H_9129 L5 rung(3) — CONTROL 4: TRUNK-NECESSITY (crux — real reps vs random codes)")
    L.append(f"ckpt={L5.CKPT}")
    L.append(f"engine: real ByteGPT-303M h1129 d={W['d']} nlay={W['nlay']} nh={W['nh']} "
             f"(core/decode.py == anima evaluate --py ops)")
    L.append(f"seed={SEED} preproc={L5.PREPROC} DIM={L5.DIM} ACTIVE={L5.ACTIVE} "
             f"STEPS={L5.STEPS} KWTA={L5.KWTA}  · pipeline imported 1:1 from l5_discriminator.py")
    L.append(f"frozen bar (pre-registered): trunk-G1 iff store_gap_real >= {G1_RATIO_BAR}x store_gap_random")
    L.append("")
    L.append("## REAL 303M reps  (fidelity: should reproduce discriminator store_gap +0.8631)")
    L.append(f"  novel_chain mean = {nc_r:.4f}   unreach mean = {ur_r:.4f}   "
             f"store_gap = {gap_r:+.4f}   dg_overlap = {ov_r:.4f}")
    L.append("")
    L.append("## RANDOM near-orthogonal codes  (trunk removed; store + DG identical)")
    L.append(f"  novel_chain mean = {nc_x:.4f}   unreach mean = {ur_x:.4f}   "
             f"store_gap = {gap_x:+.4f}   dg_overlap = {ov_x:.4f}")
    L.append("")
    L.append("## VERDICT")
    L.append(f"  store_gap_real / store_gap_random = {ratio:.2f}x   (bar = {G1_RATIO_BAR:.1f}x)")
    L.append(f"  trunk_necessary (real >= 2x random) = {trunk_necessary}")
    L.append(f"  >>> {verdict}")
    if not trunk_necessary:
        L.append("  interpretation: random near-orthogonal codes chain the SAME novel held-out")
        L.append("  pairs about as well as the 303M reps => the transitive closure is done by the")
        L.append("  explicit heteroassociative store, INDEPENDENT of the trunk. The novel-chain")
        L.append("  lift is a G2 explicit-store capability, NOT G1 trunk recombination. The wire")
        L.append("  can still cement as a live grounded-recall FACULTY, but the G1-recombination")
        L.append("  claim is WALL. Only gamma trained-constructive-bind can move trunk G1.")
    out = "\n".join(L) + "\n"
    print("\n" + out)
    with open(os.path.join(_HERE, "result_control4_trunk_necessity.txt"), "w") as f:
        f.write(out)
    with open(os.path.join(_HERE, "result_control4_trunk_necessity.json"), "w") as f:
        json.dump({"store_gap_real": gap_r, "store_gap_random": gap_x, "ratio": ratio,
                   "novel_real": nc_r, "novel_random": nc_x, "unreach_real": ur_r,
                   "unreach_random": ur_x, "dg_overlap_real": ov_r, "dg_overlap_random": ov_x,
                   "trunk_necessary": bool(trunk_necessary), "bar_ratio": G1_RATIO_BAR,
                   "verdict": verdict}, f, indent=2)
    print(f"[done] {time.time()-t0:.1f}s  -> result_control4_trunk_necessity.{{txt,json}}")


if __name__ == "__main__":
    main()
