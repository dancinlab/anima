#!/usr/bin/env python3
# ==========================================================================
# core/hippo_lane.py — L5 HIPPOCAMPAL ASSOCIATIVE-STORE lane (numpy 2-production).
#
# H_9129 rung-3.  A DISJOINT store-side lane over the .kosmos anchor store:
# pattern-separated (DG kWTA) sparse coding of anima representations + a CA3
# heteroassociative store that does MULTI-STEP pattern completion (transitive
# chaining). This is a READ-ONLY relatedness READOUT — it never mutates the
# emit-drive lane (Ψ / motivation / recall_thr / generator). Adding/consulting
# it therefore cannot change generation bytes (a_substrate_disjoint: separation
# = preservation). The byte-parity hexa twin lives in core/kosmos_io.hexa
# (hippo_kwta / hippo_build_store / hippo_relatedness).
#
# This module is a pure library (NO __main__ execution of the engine) — the
# rep→code encoding uses the real ByteGPT-303M forward via core/decode.py in the
# py-canonical measurement path (== anima-py evaluate ops, a_eval_py_canonical);
# the store + completion here is arch-independent arithmetic (no FFI, no torch).
# ==========================================================================
import numpy as np


# ── DG de-anisotropy (rung-2 GREEN lens: center_zscore) ─────────────────────
def dg_decorrelate(reps, mode="center_zscore"):
    """Whiten anisotropic anima reps before pattern separation. Raw single-token
    303M reps are near-collinear (a dominant shared direction) which masquerades
    as a substrate wall; center/z-score removes it (rung-2 pre-registered lens)."""
    R = np.asarray(reps, dtype=np.float64)
    if mode == "raw":
        return R
    mu = R.mean(axis=0, keepdims=True)
    Rc = R - mu
    if mode == "center":
        return Rc
    if mode == "center_zscore":
        sd = Rc.std(axis=0, keepdims=True) + 1e-6
        return Rc / sd
    raise ValueError(mode)


# ── DG pattern separation: fixed (untrained) random projection → kWTA sparse code ──
def hippo_kwta(v, k):
    """k-winners-take-all cleanup → sparse binary attractor state (CA3 cleanup)."""
    v = np.asarray(v, dtype=np.float64)
    if k >= v.size:
        return (v > 0).astype(np.float32)
    idx = np.argpartition(v, -k)[-k:]
    out = np.zeros_like(v, dtype=np.float32)
    pos = idx[v[idx] > 0]
    out[pos] = 1.0
    return out


def dg_codes(reps, dim, active, seed):
    """Pattern separation. Fixed seeded random projection (DG expansion) of each
    rep → kWTA sparse binary code. Projection is UNTRAINED (no handed advantage);
    correlated reps → overlapping codes (crosstalk preserved = honest test)."""
    reps = np.asarray(reps, dtype=np.float64)
    n, dm = reps.shape
    rng = np.random.default_rng(seed)
    P = rng.standard_normal((dim, dm)).astype(np.float32) / np.sqrt(dm)
    R = reps / (np.linalg.norm(reps, axis=1, keepdims=True) + 1e-9)
    drive = R @ P.T
    return np.stack([hippo_kwta(drive[i], active) for i in range(n)])


# ── CA3 heteroassociative store + multi-step pattern completion ─────────────
def hippo_build_store(codes, edges, dim):
    """Heteroassociative CA3 store: W = Σ outer(code[nxt], code[cur]) over the
    DIRECTED premise edges only. edges = list of (cur, nxt) index pairs."""
    W = np.zeros((dim, dim), dtype=np.float32)
    codes = np.asarray(codes, dtype=np.float32)
    for cur, nxt in edges:
        W += np.outer(codes[nxt], codes[cur])
    return W


def hippo_relatedness(W, codes, i, j, steps, kwta):
    """READ-OUT (no mouth): seed the lane with code[i], run CA3 completion `steps`
    times, return the max overlap between any visited attractor state and code[j].
    Multi-step ⇒ transitive chaining i→i+1→…→j iff a stored relation path exists."""
    codes = np.asarray(codes, dtype=np.float32)
    x = codes[i].copy().astype(np.float64)
    cj = codes[j].astype(np.float64)
    cjn = np.linalg.norm(cj) + 1e-9
    best = 0.0
    for _ in range(steps):
        x = hippo_kwta(W @ x, kwta).astype(np.float64)
        ov = float(x @ cj) / ((np.linalg.norm(x) + 1e-9) * cjn)
        if ov > best:
            best = ov
    return best


# ── deterministic fixture (byte-parity oracle for the kosmos_io.hexa twin) ──
def fixture_codes(n, dim, active, seed):
    """Deterministic sparse binary codes WITHOUT any float RNG divergence across
    languages: bit b is active for item i iff ((i*step + b*mul) % dim) < active
    band — a pure integer construction so hexa and py agree byte-for-byte."""
    codes = np.zeros((n, dim), dtype=np.float32)
    for i in range(n):
        picked = set()
        b = 0
        h = (i * 2654435761 + seed) & 0xFFFFFFFF
        while len(picked) < active:
            h = (h * 1664525 + 1013904223) & 0xFFFFFFFF
            picked.add(h % dim)
            b += 1
        for idx in picked:
            codes[i, idx] = 1.0
    return codes


def _fixture_report():
    """Print a deterministic small-scale CA3 report for hexa byte-parity.
    8 items in one chain 0→1→…→7; reachable = (0,k) k>=2 chain via completion;
    unreachable = a disconnected item. Also a lesion (remove edge 3→4)."""
    N, DIM, ACTIVE, STEPS, KWTA = 8, 64, 4, 8, 4
    codes = fixture_codes(N, DIM, ACTIVE, 20260705)
    edges = [(p, p + 1) for p in range(N - 1)]           # chain 0→1→...→7
    W = hippo_build_store(codes, edges, DIM)
    # reachable 2-hop (0,2) and 3-hop (0,3); adjacent stored (0,1); self-far (0,7)
    for (i, j, tag) in [(0, 1, "recall_1hop"), (0, 2, "novel_2hop"),
                        (0, 3, "novel_3hop"), (0, 7, "novel_7hop")]:
        r = hippo_relatedness(W, codes, i, j, STEPS, KWTA)
        print("py %s(0,%d)=%.6f" % (tag, j, r))
    # lesion: remove edge 3→4 ; pair (0,5) path crosses it → must collapse
    Wl = hippo_build_store(codes, [(p, p + 1) for p in range(N - 1) if p != 3], DIM)
    print("py lesion_broken(0,5)=%.6f" % hippo_relatedness(Wl, codes, 0, 5, STEPS, KWTA))
    print("py lesion_intact(0,2)=%.6f" % hippo_relatedness(Wl, codes, 0, 2, STEPS, KWTA))


if __name__ == "__main__":
    _fixture_report()
