"""H_012A — owner-loop-rct precheck: SAMPLER-TWIN semi-interventional screen ($0, stdlib).

H_010 tested the owner<->agent loop OBSERVATIONALLY (all pairs; context confounds) -> LOOP-REFUSED.
H_012A refines it toward the interventional target: decode stochasticity is a genuine LOCAL randomizer
of the agent utterance U_t given context. Among pairs where the agent faced NEAR-IDENTICAL context but
emitted DIFFERENT utterances (both genuinely produced), does the utterance still predict the owner's next
reply R_{t+1} above the certified shift-null floor? This is semi-interventional (valid under conditional
ignorability given the matched TEXT context; unobserved context can leak) so it can PRECHECK-UPGRADE or
PRECHECK-REFUSE, never ANCHOR (only the live H_012B randomization can).

The ONE change vs H_010's certified estimator: each query's LOO k-NN candidate pool is RESTRICTED to its
CONTEXT-MATCHED neighbors (the M nearest by distRt). Within a tight context stratum the utterance varies
quasi-randomly, so BASE-vs-FULL there isolates the utterance's marginal reply-predictive power.

Reuses H_010 verbatim: loop_pairs / build / features / _distmat / _knn_err / _sign_frac / _median /
echo_strip / constants. Purpose-built WITHIN-CONTEXT plants certify the estimator AS USED (H_010's
cross-context plant_pos would not — its signal lives across topics, which context-matching excludes).

Privacy (hard rule, H_010 invariant): NO owner content to the repo — only aggregate sign/rank/err scalars.
Run: python3 state/h012_owner-loop-rct_2026-07-17/run_h012a.py
"""

from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))
sys.path.insert(0, os.path.join(_ROOT, "state", "h010_loop-granger-gate_2026-07-16"))

import run_h010 as H          # certified estimator + loop_pairs + constants (import runs no main())

M_CAP = 60                    # max context-matched neighbors per query
M_FRAC = 0.04                 # or this fraction of N, whichever is smaller (>= KNN+2)
N_CAP = 2000                  # subsample cap (O(n^2) estimator; matches H_010's N_PRIMARY scale)


def _matched_cand(distRt, sess, sidx, n, M):
    """Per query, the M CONTEXT-NEAREST candidates by distRt (H_010's session-adjacent exclusion kept)."""
    out = []
    for i in range(n):
        base = [j for j in range(n) if j != i and not (sess[j] == sess[i] and abs(sidx[i] - sidx[j]) < 2)]
        base.sort(key=lambda j: (distRt[i][j], j))
        out.append(base[:M])
    return out


def analyze_matched(pairs, m_frac=M_FRAC, m_cap=M_CAP):
    n = len(pairs)
    sess = [p[0] for p in pairs]; sidx = [p[1] for p in pairs]
    fRt = [p[2] for p in pairs]; fU = [p[3] for p in pairs]
    tgt_s = [p[4] for p in pairs]; tgt_u = [p[5] for p in pairs]
    distRt = H._distmat(fRt); distU = H._distmat(fU)
    M = min(m_cap, max(H.KNN + 2, int(m_frac * n)))
    cand = _matched_cand(distRt, sess, sidx, n, M)

    def row_base(i):
        return distRt[i]

    def row_full(i):
        ri, ui = distRt[i], distU[i]
        return [ri[j] + ui[j] for j in range(n)]

    def signs(tgt):
        eb = H._knn_err(tgt, cand, row_base)
        ef = H._knn_err(tgt, cand, row_full)
        return H._sign_frac(eb, ef), sum(ef)

    sbf_s, ef_s = signs(tgt_s)               # stripped target (primary)
    sbf_u, _ = signs(tgt_u)                  # unstripped (echo diagnostic)

    # within-session shift-null on FULL (stripped), over the SAME restricted candidate pool
    sess_members = {}
    for i in range(n):
        sess_members.setdefault(sess[i], []).append(i)
    for s in sess_members:
        sess_members[s].sort(key=lambda i: sidx[i])
    shift_err = []
    for d in range(1, H.SHIFTS + 1):
        umap = list(range(n))
        for mem in sess_members.values():
            L = len(mem)
            if L < 3:
                continue
            for pos, i in enumerate(mem):
                umap[i] = mem[(pos + d) % L]
        row_shift = lambda i, um=umap: [distRt[i][j] + distU[um[i]][j] for j in range(n)]
        shift_err.append(sum(H._knn_err(tgt_s, cand, row_shift)))
    rank_full = sum(1 for se in shift_err if se <= ef_s)
    align_full = (H._median(shift_err) - ef_s) if shift_err else 0.0

    # context tightness: median distRt to the Mth matched neighbor vs a global distRt sample
    mth = [distRt[i][cand[i][-1]] for i in range(n) if cand[i]]
    glob = [distRt[i][j] for i in range(0, n, 5) for j in range(0, n, 5) if i != j]
    tight = (H._median(mth) / H._median(glob)) if glob and H._median(glob) else 1.0

    return {"n": n, "M": M, "sign_base_full": round(sbf_s, 4),
            "sign_base_full_unstripped": round(sbf_u, 4), "rank_full": rank_full,
            "n_shifts": len(shift_err), "align_full": round(align_full, 3),
            "ctx_tightness": round(tight, 3)}


# ---- WITHIN-CONTEXT plants (certify the restricted estimator AS USED) --------
def _plant_matched_pos(n=320, k_types=16, seed=411):
    """P-POS(matched): a SHARED context backdrop; the utterance carries a type token; the reply CIPHERS
    that type in a DISJOINT alphabet (survives echo-strip). Types RECUR across pairs, so within the
    (shared-context) matched pool FULL retrieves same-type neighbors whose cipher matches -> channel."""
    rng = H._LCG(seed)
    base_ctx = H._rand_text(rng, 200)                 # ONE shared context (so context-matching keeps all)
    base_rep = H._rand_text(rng, 120)
    trip = []
    for i in range(n):
        a = i % k_types
        u = bytes([65 + a]) * 200 + H._rand_text(rng, 30)          # utterance encodes the type
        sig = bytes([150 + a]) * 140                               # cipher, disjoint alphabet
        rt = base_ctx + H._rand_text(rng, 30)
        rt1 = base_rep + sig + H._rand_text(rng, 20)
        trip.append((f"S{i % 20}", i, rt[-H.RB:], u[-H.UB:], rt1[:H.RB]))
    return trip


def _plant_matched_null(n=300, seed=522):
    """P-NULL(matched): shared context, utterance RANDOM, reply independent of it -> must refuse."""
    rng = H._LCG(seed)
    base_ctx = H._rand_text(rng, 200); base_rep = H._rand_text(rng, 120)
    trip = []
    for i in range(n):
        u = H._rand_text(rng, 220)
        rt = base_ctx + H._rand_text(rng, 30)
        rt1 = base_rep + H._rand_text(rng, 160)
        trip.append((f"S{i % 20}", i, rt[-H.RB:], u[-H.UB:], rt1[:H.RB]))
    return trip


def _plant_matched_echo(n=320, k_q=16, seed=633):
    """P-ECHO(matched): shared context; U carries a RECURRING verbatim quote; R quotes it verbatim.
    Unstripped: FULL beats BASE (copy channel). Stripped: quote removed from R -> channel vanishes."""
    rng = H._LCG(seed)
    quotes = [H._rand_text(rng, 110) for _ in range(k_q)]
    base_ctx = H._rand_text(rng, 200)
    trip = []
    for i in range(n):
        q = i % k_q
        u = base_ctx[:60] + quotes[q] + H._rand_text(rng, 40)
        rt = base_ctx + H._rand_text(rng, 30)
        rt1 = quotes[q] + H._rand_text(rng, 120)                  # verbatim recurring quote in R
        trip.append((f"S{i % 20}", i, rt[-H.RB:], u[-H.UB:], rt1[:H.RB]))
    return trip


def certify():
    pos = analyze_matched(H.build(_plant_matched_pos()))
    nul = analyze_matched(H.build(_plant_matched_null()))
    ech = analyze_matched(H.build(_plant_matched_echo()))
    pos_ok = pos["sign_base_full"] >= H.SIGN_PAIR and pos["rank_full"] <= 2
    null_ok = nul["sign_base_full"] < H.SIGN_PAIR
    echo_ok = ech["sign_base_full_unstripped"] >= H.SIGN_PAIR and ech["sign_base_full"] < H.SIGN_PAIR
    return {"P-POS": {**pos, "pass": bool(pos_ok)}, "P-NULL": {**nul, "pass": bool(null_ok)},
            "P-ECHO": {"unstripped": ech["sign_base_full_unstripped"], "stripped": ech["sign_base_full"],
                       "pass": bool(echo_ok)}, "ok": bool(pos_ok and null_ok and echo_ok)}


def main() -> int:
    print("=" * 82)
    print("H_012A — owner-loop-rct precheck · SAMPLER-TWIN (context-matched, semi-interventional, $0)")
    print("=" * 82)
    out = {"knn": H.KNN, "sign_pair": H.SIGN_PAIR, "M_cap": M_CAP, "M_frac": M_FRAC, "N_cap": N_CAP}

    print("\n[certify] within-context plants (P-POS channel · P-NULL refuse · P-ECHO echo-only):")
    live = certify(); out["certify"] = live
    for k in ("P-POS", "P-NULL", "P-ECHO"):
        print(f"  {k}: {json.dumps(live[k], ensure_ascii=False)}")
    print(f"  certify_ok = {live['ok']}")
    if not live["ok"]:
        out["verdict"] = "INSTRUMENT-INVALID — the context-matched estimator failed a plant; fix before the real run."
        print("\n  VERDICT:", out["verdict"]); _dump(out); return 0

    print("\n[extract] scanning transcripts (content stays on disk) ...")
    trip = H.loop_pairs()
    n_sess = len({t[0] for t in trip})
    print(f"  {len(trip)} loop pairs across {n_sess} sessions (>= {H.MIN_PAIRS} each)")
    out["total_pairs"], out["total_sessions"] = len(trip), n_sess
    if len(trip) < 200:
        out["verdict"] = f"INSTRUMENT-INVALID (only {len(trip)} pairs — substrate too thin)"
        print("\n  VERDICT:", out["verdict"]); _dump(out); return 0

    stride = max(1, len(trip) // N_CAP)
    s1 = [trip[i] for i in range(0, len(trip), stride)][:N_CAP]
    s2 = [trip[i] for i in range(1, len(trip), stride)][:N_CAP]
    print(f"  primary N={len(s1)} · replication N={len(s2)} (stride {stride})")

    a = analyze_matched(H.build(s1)); b = analyze_matched(H.build(s2))
    out["primary"], out["replication"] = a, b
    for nm, r in (("primary", a), ("replication", b)):
        print(f"\n[{nm}] n={r['n']} M={r['M']} ctx_tightness={r['ctx_tightness']} "
              f"(matched pool distRt / global; <1 = tighter)")
        print(f"    sign(base>full)={r['sign_base_full']:.3f} (>= {H.SIGN_PAIR}?) · "
              f"rank_full={r['rank_full']}/{r['n_shifts']} (<=2?) · align_full={r['align_full']}")
        print(f"    (H_010 observational baseline: sign_base_full 0.406 — REFUSED)")

    upgrade = (a["sign_base_full"] >= H.SIGN_PAIR and a["rank_full"] <= 2)
    replicates = (b["sign_base_full"] >= H.SIGN_PAIR) == (a["sign_base_full"] >= H.SIGN_PAIR)
    out["replicates"] = bool(replicates)
    if upgrade:
        out["verdict"] = (f"PRECHECK-UPGRADE — within CONTEXT-MATCHED strata the utterance predicts the owner's "
                          f"next reply above the shift-null floor (sign_base_full {a['sign_base_full']:.3f} >= "
                          f"{H.SIGN_PAIR}, rank {a['rank_full']}/{a['n_shifts']}), where H_010's OBSERVATIONAL "
                          f"test refused (0.406). Semi-interventional (not identified) -> RAISES the prior that "
                          f"the live H_012B RCT anchors; does NOT itself anchor. Replicates={replicates}.")
    else:
        out["verdict"] = (f"PRECHECK-REFUSE — even semi-interventionally (context matched, utterance quasi-random) "
                          f"the utterance carries no reply-predictive info beyond context (sign_base_full "
                          f"{a['sign_base_full']:.3f} < {H.SIGN_PAIR}, rank {a['rank_full']}/{a['n_shifts']}) — "
                          f"consistent with H_010's observational REFUSE. A cheap negative that LOWERS the odds "
                          f"before spending owner consent on H_012B. Replicates={replicates}.")
    print("\n  VERDICT:", out["verdict"])
    print("=" * 82)
    _dump(out)
    return 0


def _dump(m):
    with open(os.path.join(_HERE, "result_h012a.json"), "w") as f:
        json.dump(m, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"artifact: {os.path.relpath(os.path.join(_HERE, 'result_h012a.json'), _ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
