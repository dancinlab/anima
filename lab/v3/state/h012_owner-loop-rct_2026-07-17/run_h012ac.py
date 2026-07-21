"""H_012A-c — block-OUTCOME target: are the real-loop refusals at the WRONG TIMESCALE? ($0, stdlib).

H_010/H_012A/H_012A-b all test ONE-STEP (U_t -> R_{t+1}). The proxy's 7B ANCHORED at the BLOCK level (LV-C)
and FAILED one-step (LV-W), so the real-loop refusals may be at the wrong timescale. The block level FACTORS:
the sequence-contingency half (yoked permuted-sequence ghost) is interventional -> H_012B-only; the block-
OUTCOME half is identified under the SAME per-step ignorability H_012A accepted.

Test: treatment = a SINGLE utterance U_t (decode-stochastic within context-matched strata, M=60), outcome =
blockmean(features(R_{t+1..t+k})), primary k=5. sign(err_BASE > err_FULL) + within-session shift-null band +
disjoint replication. Distinct from one-step via INTEGRATION (per-lag effects below the one-step floor sum
over k) and DELAY (lag>1 influence with no lag-1 trace). Still semi-interventional (cannot anchor); tests
single-utterance->window, NOT sequence-contingency (that residue is H_012B-only).

Reuses the certified estimator (features/_distmat/echo_strip from run_h010, _matched_cand from run_h012a).
Privacy: no owner content to the repo, only aggregate scalars.
Run: python3 state/h012_owner-loop-rct_2026-07-17/run_h012ac.py
"""

from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))
sys.path.insert(0, os.path.join(_ROOT, "state", "h010_loop-granger-gate_2026-07-16"))
sys.path.insert(0, _HERE)

import run_h010 as H
import run_h012a as A

K = 5                          # primary window (k=3,8 sensitivity only)
N_CAP = A.N_CAP
M_CAP = A.M_CAP
M_FRAC = A.M_FRAC
_PMF = 0.10                    # plant m_frac (plant n=700 -> M=60, the real-data regime)


# ---- block-mean-target estimator (vector target, sqdist; sign null band) -----
def analyze_block(rows, m_frac=M_FRAC, m_cap=M_CAP):
    """rows = [(sess, sidx, feat_Rt, feat_U, block_target_vec)]."""
    n = len(rows)
    sess = [r[0] for r in rows]; sidx = [r[1] for r in rows]
    fRt = [r[2] for r in rows]; fU = [r[3] for r in rows]; tgt = [r[4] for r in rows]
    distRt = H._distmat(fRt); distU = H._distmat(fU)
    M = min(m_cap, max(H.KNN + 2, int(m_frac * n)))
    cand = A._matched_cand(distRt, sess, sidx, n, M)
    row_base = lambda i: distRt[i]
    row_full = lambda i: [distRt[i][j] + distU[i][j] for j in range(n)]
    eb = H._knn_err(tgt, cand, row_base)
    ef = H._knn_err(tgt, cand, row_full)
    sign_bf = sum(1 for a, b in zip(eb, ef) if a > b) / n

    sess_members = {}
    for i in range(n):
        sess_members.setdefault(sess[i], []).append(i)
    for s in sess_members:
        sess_members[s].sort(key=lambda i: sidx[i])
    null_signs = []
    for d in range(1, H.SHIFTS + 1):
        umap = list(range(n))
        for mem in sess_members.values():
            L = len(mem)
            if L < 3:
                continue
            for pos, i in enumerate(mem):
                umap[i] = mem[(pos + d) % L]
        ef_sh = H._knn_err(tgt, cand, lambda i, um=umap: [distRt[i][j] + distU[um[i]][j] for j in range(n)])
        null_signs.append(sum(1 for a, b in zip(eb, ef_sh) if a > b) / n)
    null_signs.sort()
    p95 = null_signs[int(0.95 * (len(null_signs) - 1))] if null_signs else 0.5
    return {"n": n, "M": M, "sign_base_full": round(sign_bf, 4), "null_p95": round(p95, 4),
            "beats_null": bool(sign_bf > p95 and sign_bf >= H.SIGN_PAIR)}


# ---- block-mean row builder (owner subsequent-window statistics) -------------
def _blockrows(triples, k=K):
    """[(sess, sidx, Rt, U, Rt1)] -> [(sess, sidx, feat_Rt, feat_U, blockmean feat over next-k owner replies)].
    Block target = mean over the window of features(echo_strip(Rt1_{idx+j}, U_query)); drops pairs with < k
    following pairs in the session."""
    by = {}
    for t in triples:
        by.setdefault(t[0], []).append(t)
    rows = []
    for sid, seq in by.items():
        seq.sort(key=lambda t: t[1])
        for idx in range(len(seq) - k + 1):
            _, sx, rt, u, _ = seq[idx]
            win = seq[idx:idx + k]
            fs = [H.features(H.echo_strip(w[4], u)) for w in win]     # strip each reply vs the QUERY utterance
            dim = len(fs[0])
            blk = [sum(f[d] for f in fs) / k for d in range(dim)]
            rows.append((sid, sx, H.features(rt), H.features(u), blk))
    return rows


# ---- block-structured plants ------------------------------------------------
def _cip(t):
    return bytes([150 + (t % 90)])


def _plant_blockpos(n_sess=40, per=20, ktypes=10, w=14, seed=711):
    """P-BLOCKPOS (integration): shared context; each U carries a type; U_p leaves a per-lag cipher of its
    type in EACH of the next K owner replies. Per-lag strength (w bytes) is small vs the single-reply noise
    so one-step is weak; the k=5 block-mean averages K consistent copies -> clears (reproduces LV-W-fail/
    LV-C-pass integration). Calibrated: one-step below block."""
    rng = H._LCG(seed)
    ctx = H._rand_text(rng, 200); base = H._rand_text(rng, 40)
    trip = []
    for s in range(n_sess):
        types = [int(rng.u() * ktypes) % ktypes for _ in range(per)]
        us = [bytes([65 + a]) * 200 + H._rand_text(rng, 20) for a in types]
        for p in range(per):
            # owner reply after U_p carries a per-lag cipher of U_p, U_{p-1}, ... plus per-reply noise that
            # dilutes any SINGLE reply (one-step weak) but averages out across the K-window (block strong).
            seg = b""
            for lag in range(K):
                src = p - lag
                seg += (_cip(types[src]) * w) if src >= 0 else (H._rand_text(rng, w))
            rt1 = base + seg + H._rand_text(rng, 200)                 # heavy per-reply noise
            rt = ctx + H._rand_text(rng, 20)
            trip.append((f"BP{s}", p, rt[-H.RB:], us[p][-H.UB:], rt1[:H.RB]))
    return trip


def _plant_delay(n_sess=40, per=20, ktypes=10, seed=822):
    """P-DELAY: U_p influences ONLY the lag-3 owner reply (Rt1_{p+2}), nothing at lag 1. One-step blind;
    the k=5 block-mean (which includes lag 3) must detect it."""
    rng = H._LCG(seed)
    ctx = H._rand_text(rng, 200); base = H._rand_text(rng, 120)
    trip = []
    for s in range(n_sess):
        types = [int(rng.u() * ktypes) % ktypes for _ in range(per)]
        us = [bytes([65 + a]) * 200 + H._rand_text(rng, 20) for a in types]
        for p in range(per):
            src = p - 2                                               # lag-3 reply carries U_{p-2}'s cipher
            seg = _cip(types[src]) * 120 if src >= 0 else b""
            rt1 = base + seg + H._rand_text(rng, 40)
            rt = ctx + H._rand_text(rng, 20)
            trip.append((f"BD{s}", p, rt[-H.RB:], us[p][-H.UB:], rt1[:H.RB]))
    return trip


def _plant_blocknull(n_sess=40, per=20, seed=933):
    """P-BLOCKNULL: shared context, random utterance, owner window independent -> must refuse."""
    rng = H._LCG(seed)
    ctx = H._rand_text(rng, 200); base = H._rand_text(rng, 120)
    trip = []
    for s in range(n_sess):
        for p in range(per):
            u = H._rand_text(rng, 200)
            rt1 = base + H._rand_text(rng, 200)
            rt = ctx + H._rand_text(rng, 20)
            trip.append((f"BN{s}", p, rt[-H.RB:], u[-H.UB:], rt1[:H.RB]))
    return trip


def _plant_blockconf(n_sess=40, per=24, seed=1044):
    """P-BLOCKCONF (critical): a slow-drift latent z drives BOTH the utterance AND the owner window with NO
    U->R edge. z is encoded into the CONTEXT too (the owner replies to z). Window aggregation amplifies the
    slow-drift confound; the estimator must still REFUSE (FULL must not beat context, and shift-null of a
    slow signal stays high)."""
    rng = H._LCG(seed)
    trip = []
    for s in range(n_sess):
        z = int(rng.u() * 8)
        for p in range(per):
            if rng.u() < 0.25:
                z = (z + (1 if rng.u() < 0.5 else -1)) % 8            # slow random walk
            u = bytes([65 + z]) * 200 + H._rand_text(rng, 20)         # U encodes z
            rt = bytes([40 + z]) * 180 + H._rand_text(rng, 20)        # CONTEXT encodes z (owner responds to z)
            rt1 = bytes([200 + z]) * 140 + H._rand_text(rng, 60)      # owner window encodes z, NO U edge
            trip.append((f"BC{s}", p, rt[-H.RB:], u[-H.UB:], rt1[:H.RB]))
    return trip


def certify():
    bp = analyze_block(_blockrows(_plant_blockpos()), m_frac=_PMF)
    # one-step reference for the SAME positive plant (k=1) -> must be BELOW the block signal (integration)
    bp1 = analyze_block(_blockrows(_plant_blockpos(), k=1), m_frac=_PMF)
    dl = analyze_block(_blockrows(_plant_delay()), m_frac=_PMF)
    dl1 = analyze_block(_blockrows(_plant_delay(), k=1), m_frac=_PMF)
    nu = analyze_block(_blockrows(_plant_blocknull()), m_frac=_PMF)
    cf = analyze_block(_blockrows(_plant_blockconf()), m_frac=_PMF)
    pos_ok = bp["beats_null"]
    integ_ok = bp["sign_base_full"] > bp1["sign_base_full"]           # block > one-step (integration shown)
    delay_ok = dl["beats_null"] and not dl1["beats_null"]             # block finds it, one-step blind
    null_ok = not nu["beats_null"]
    conf_ok = not cf["beats_null"]
    return {"P_BLOCKPOS": {**bp, "onestep_sign": bp1["sign_base_full"], "pass": bool(pos_ok and integ_ok)},
            "P_DELAY": {**dl, "onestep_beats": dl1["beats_null"], "pass": bool(delay_ok)},
            "P_BLOCKNULL": {**nu, "pass": bool(null_ok)}, "P_BLOCKCONF": {**cf, "pass": bool(conf_ok)},
            "ok": bool(pos_ok and integ_ok and delay_ok and null_ok and conf_ok)}


def main() -> int:
    print("=" * 84)
    print(f"H_012A-c — block-OUTCOME target (k={K}) · wrong-timescale check (context-matched, $0)")
    print("=" * 84)
    out = {"knn": H.KNN, "sign_pair": H.SIGN_PAIR, "K": K, "M_cap": M_CAP, "N_cap": N_CAP}

    print("\n[certify] block plants (P-BLOCKPOS integration · P-DELAY · P-BLOCKNULL · P-BLOCKCONF):")
    live = certify(); out["certify"] = live
    for k in ("P_BLOCKPOS", "P_DELAY", "P_BLOCKNULL", "P_BLOCKCONF"):
        print(f"  {k}: {json.dumps(live[k], ensure_ascii=False)}")
    print(f"  certify_ok = {live['ok']}")
    if not live["ok"]:
        out["verdict"] = "INSTRUMENT-INVALID — a block plant failed; fix before the real run."
        print("\n  VERDICT:", out["verdict"]); _dump(out); return 0

    print("\n[extract] scanning transcripts (content stays on disk) ...")
    trip = H.loop_pairs()
    print(f"  {len(trip)} loop pairs across {len({t[0] for t in trip})} sessions")
    rows_all = _blockrows(trip)
    print(f"  {len(rows_all)} block-windowed queries (k={K})")
    if len(rows_all) < 200:
        out["verdict"] = f"STANCE-UNIDENTIFIABLE (only {len(rows_all)} windowed queries)"; print("\n ", out["verdict"]); _dump(out); return 0
    stride = max(1, len(rows_all) // N_CAP)
    s1 = [rows_all[i] for i in range(0, len(rows_all), stride)][:N_CAP]
    s2 = [rows_all[i] for i in range(1, len(rows_all), stride)][:N_CAP]

    a = analyze_block(s1); b = analyze_block(s2)
    out["primary"], out["replication"] = a, b
    for nm, r in (("primary", a), ("replication", b)):
        print(f"\n[{nm}] n={r['n']} M={r['M']} sign_base_full={r['sign_base_full']:.3f} vs "
              f"null_p95={r['null_p95']:.3f} (threshold {H.SIGN_PAIR}) -> beats_null={r['beats_null']}")

    if a["beats_null"] and b["beats_null"]:
        out["verdict"] = (f"BLOCK-CLOSURE-FOUND — a SINGLE utterance shifts the owner's subsequent-WINDOW "
                          f"input statistics above the shift-null band on BOTH replicates (sign "
                          f"{a['sign_base_full']:.3f}/{b['sign_base_full']:.3f} > null "
                          f"{a['null_p95']:.3f}/{b['null_p95']:.3f}, k={K}). The one-step refuses (H_010/"
                          f"H_012A/H_012A-b) were at the WRONG TIMESCALE: closure lives at the window level "
                          f"(as it did in the proxy). Semi-interventional (cannot anchor) -> re-prices H_012B "
                          f"UP with a concrete windowed effect.")
    else:
        out["verdict"] = (f"BLOCK-REFUSE — even at the WINDOW level (k={K}) a single utterance does not shift "
                          f"the owner's subsequent-window input above the shift-null band (sign "
                          f"{a['sign_base_full']:.3f}/{b['sign_base_full']:.3f} vs null "
                          f"{a['null_p95']:.3f}/{b['null_p95']:.3f}). The refusal is ROBUST across TARGETS "
                          f"(text, behavior) AND TIMESCALES (one-step, window). Honest residue: the sequence-"
                          f"CONTINGENCY channel (yoked ghost) stays H_012B-only — cannot be excluded at $0.")
    print("\n  VERDICT:", out["verdict"])
    print("=" * 84)
    _dump(out)
    return 0


def _dump(m):
    with open(os.path.join(_HERE, "result_h012ac.json"), "w") as f:
        json.dump(m, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"artifact: {os.path.relpath(os.path.join(_HERE, 'result_h012ac.json'), _ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
