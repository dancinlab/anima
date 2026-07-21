"""H_012A-b — behavioral-stance target: is the owner-loop refusal a WRONG-TARGET artifact? ($0, stdlib).

H_010 + H_012A refused using the owner's next-reply TEXT embedding as the target. Owners reply on-topic to
anything, so text is topic-ceilinged and may HIDE closure. H_012A-b swaps the target to a binary STANCE —
does the owner CONTINUE on the agent's track vs CORRECT/redirect? — a lower-dim projection of the same
subsequent input. If the agent's SPECIFIC utterance (vs a context-matched twin) predicts stance above the
shift-null floor, closure lives in behavior and the text refusals were wrong-target; if not, the refusal is
robust across targets.

Reuses the certified context-matched estimator (run_h012a / run_h010) with a scalar Brier target. The
labeler reads the OWNER TURN ONLY (a hard label-leak rule; certified by plant P4). Still semi-
interventional (decode stochasticity is a local randomizer) -> can FIND closure-consistent evidence or
REFUSE, never ANCHOR. Privacy: no owner content to the repo, only aggregate scalars.

Run: python3 state/h012_owner-loop-rct_2026-07-17/run_h012ab.py
"""

from __future__ import annotations

import heapq
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))
sys.path.insert(0, os.path.join(_ROOT, "state", "h010_loop-granger-gate_2026-07-16"))
sys.path.insert(0, _HERE)

import run_h010 as H
import run_h012a as A          # _matched_cand, M params

N_CAP = A.N_CAP
M_CAP = A.M_CAP
M_FRAC = A.M_FRAC
N_MIN_INFORMATIVE = 200        # min surviving informative queries for a valid precheck

# ---- stance labeler (deterministic · OWNER TURN ONLY · EN+KO) ----------------
_HARD = ("[request interrupted by user]", "is not permitted", "n't permitted", "user rejected",
         "user doesn't want", "[request cancelled")
_CORR = ("no,", "no.", "nope", "actually", "instead", "wrong", "not what", "i said", "i meant",
         "you didn't", "you did not", "revert", "undo", "stop", "don't ", "do not ", "that's not",
         "thats not", "isn't", "incorrect", "rather",
         "아니", "아냐", "그게 아니", "말고", "다시", "잘못", "하지 마", "하지마", "틀렸", "아니라")
_CONT = ("yes", "yeah", "yep", "ok", "okay", "sure", "go ahead", "proceed", "continue", "thanks",
         "thank you", "lgtm", "perfect", "great", "do it", "sounds good", "looks good",
         "응", "네", "좋아", "그래", "진행", "계속", "고마워", "맞아", "오케")


def stance(rt1_bytes) -> int:
    """1 = CORRECT/redirect, 0 = CONTINUE. Reads the OWNER next turn ONLY (never the agent utterance)."""
    t = rt1_bytes.decode("utf-8", "replace").strip().lower()
    if any(h in t for h in _HARD):
        return 1
    first = t[:120]                                   # ~first clause
    if any(c in first for c in _CORR):
        return 1
    if any(c in first for c in _CONT) or len(t) < 40:
        return 0
    return 0                                          # default CONTINUE


# ---- scalar-target (Brier) context-matched estimator ------------------------
def _knn_brier(labels, cand_of, distrow_fn, kk=H.KNN):
    out = []
    for i in range(len(labels)):
        row = distrow_fn(i)
        nn = heapq.nsmallest(kk, cand_of[i], key=lambda j: (row[j], j))
        pred = sum(labels[j] for j in nn) / len(nn)
        out.append((labels[i] - pred) ** 2)
    return out


def analyze_stance(rows, m_frac=M_FRAC, m_cap=M_CAP):
    """rows = [(sess, sidx, feat_Rt, feat_U, label)]. Context-matched BASE-vs-FULL on the binary stance,
    restricted to INFORMATIVE strata (matched pool holds BOTH labels)."""
    n = len(rows)
    sess = [r[0] for r in rows]; sidx = [r[1] for r in rows]
    fRt = [r[2] for r in rows]; fU = [r[3] for r in rows]
    lab = [r[4] for r in rows]
    distRt = H._distmat(fRt); distU = H._distmat(fU)
    M = min(m_cap, max(H.KNN + 2, int(m_frac * n)))
    cand = A._matched_cand(distRt, sess, sidx, n, M)

    def row_base(i):
        return distRt[i]

    def row_full(i):
        ri, ui = distRt[i], distU[i]
        return [ri[j] + ui[j] for j in range(n)]

    eb = _knn_brier(lab, cand, row_base)
    ef = _knn_brier(lab, cand, row_full)
    # informative queries: matched pool holds both stance labels (else utterance cannot matter)
    inf = [i for i in range(n) if cand[i] and len({lab[j] for j in cand[i]}) > 1]
    n_inf = len(inf)
    sign_bf = (sum(1 for i in inf if eb[i] > ef[i]) / n_inf) if n_inf else 0.5

    # shift-null: WRONG-utterance (permute utterance within session) FULL, over informative queries
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
        ef_sh = _knn_brier(lab, cand, lambda i, um=umap: [distRt[i][j] + distU[um[i]][j] for j in range(n)])
        ns = (sum(1 for i in inf if eb[i] > ef_sh[i]) / n_inf) if n_inf else 0.5
        null_signs.append(ns)
    null_signs.sort()
    null_p95 = null_signs[int(0.95 * (len(null_signs) - 1))] if null_signs else 0.5
    base_rate = sum(lab) / n

    return {"n": n, "M": M, "n_informative": n_inf, "stance_rate": round(base_rate, 4),
            "sign_base_full": round(sign_bf, 4), "null_p95": round(null_p95, 4),
            "beats_null": bool(sign_bf > null_p95 and sign_bf >= H.SIGN_PAIR)}


# ---- within-context plants for the STANCE estimator -------------------------
def _mk(sess, sidx, ctx_bytes, u_bytes, label):
    return (sess, sidx, H.features(ctx_bytes[-H.RB:]), H.features(u_bytes[-H.UB:]), label)


def _plant_pos_stance(n=700, k=12, noise=0.0, seed=711):
    """P1: shared context; stance = deterministic fn of the utterance TYPE via a random type->{0,1} map;
    the type is assigned RANDOMLY per pair (never i%k — that aligns with the session stride and degenerates
    the shift-null). Optional injected label noise flips a fraction, calibrating the detectable floor. n is
    large so M reaches the real-data regime (60). Estimator must FIRE above the null band."""
    rng = H._LCG(seed)
    ctx = H._rand_text(rng, 200)
    typemap = [1 if H._LCG(seed + 1 + t).u() < 0.5 else 0 for t in range(k)]   # fixed random type->stance
    rows = []
    for i in range(n):
        a = int(rng.u() * k) % k                         # RANDOM type per pair (breaks stride alignment)
        u = bytes([65 + a]) * 200 + H._rand_text(rng, 20)
        y = typemap[a]
        if rng.u() < noise:
            y = 1 - y                                    # injected label noise
        rows.append(_mk(f"S{i % 20}", i, ctx + H._rand_text(rng, 20), u, y))
    return rows


def _plant_null_stance(n=700, seed=822):
    """P2: shared context; stance = seeded coin independent of the utterance. Must sit at the null band."""
    rng = H._LCG(seed)
    ctx = H._rand_text(rng, 200)
    rows = []
    for i in range(n):
        u = H._rand_text(rng, 200)
        rows.append(_mk(f"S{i % 20}", i, ctx + H._rand_text(rng, 20), u, 1 if rng.u() < 0.5 else 0))
    return rows


def _plant_confound_stance(n=700, seed=933):
    """P3: stance = fn(CONTEXT) only (parity of a per-context id), utterance irrelevant. FULL must NOT
    beat BASE (guards utterance features echoing context)."""
    rng = H._LCG(seed)
    rows = []
    for i in range(n):
        cid = i % 24
        ctx = bytes([40 + cid]) * 180 + H._rand_text(rng, 20)
        u = H._rand_text(rng, 200)
        rows.append(_mk(f"S{i % 20}", i, ctx, u, cid % 2))
    return rows


def _p4_label_leak_ok():
    """P4 (deterministic): the labeler must be invariant to the agent utterance — it takes ONLY the owner
    turn. Assert the signature is exactly (rt1_bytes,) so no utterance can enter the label."""
    import inspect
    params = list(inspect.signature(stance).parameters)
    return params == ["rt1_bytes"]


_PMF = 0.10          # plant m_frac: at plant n=700 gives M=min(60, 70)=60 = the real-data regime


def certify():
    p1 = analyze_stance(_plant_pos_stance(noise=0.0), m_frac=_PMF)
    p1n = {f"noise_{int(x*100)}": analyze_stance(_plant_pos_stance(noise=x), m_frac=_PMF)["sign_base_full"]
           for x in (0.15, 0.30)}
    p2 = analyze_stance(_plant_null_stance(), m_frac=_PMF)
    p3 = analyze_stance(_plant_confound_stance(), m_frac=_PMF)
    p4 = _p4_label_leak_ok()
    pos_ok = p1["beats_null"]
    null_ok = not p2["beats_null"]
    conf_ok = not p3["beats_null"]                       # utterance must NOT beat context-only signal
    floor = {"P1_clean_sign": p1["sign_base_full"], "P1_noise_signs": p1n}
    return {"P1_pos": {**p1, "pass": bool(pos_ok)}, "P1_noise_floor": floor,
            "P2_null": {**p2, "pass": bool(null_ok)}, "P3_confound": {**p3, "pass": bool(conf_ok)},
            "P4_label_leak_safe": bool(p4), "ok": bool(pos_ok and null_ok and conf_ok and p4)}


def build_stance(triples):
    """[(sess, sidx, Rt, U, Rt1)] -> [(sess, sidx, feat_Rt, feat_U, stance_label)]"""
    return [(s, k, H.features(rt), H.features(u), stance(rt1)) for s, k, rt, u, rt1 in triples]


def main() -> int:
    print("=" * 84)
    print("H_012A-b — behavioral-stance target · wrong-target-artifact check (context-matched, $0)")
    print("=" * 84)
    out = {"knn": H.KNN, "sign_pair": H.SIGN_PAIR, "M_cap": M_CAP, "N_cap": N_CAP, "N_min_inf": N_MIN_INFORMATIVE}

    print("\n[certify] stance-estimator plants (P1 channel+noise floor · P2 null · P3 confound · P4 leak):")
    live = certify(); out["certify"] = live
    for k in ("P1_pos", "P2_null", "P3_confound"):
        print(f"  {k}: {json.dumps(live[k], ensure_ascii=False)}")
    print(f"  P1 noise floor (detectable-effect calibration): {json.dumps(live['P1_noise_floor']['P1_noise_signs'])}")
    print(f"  P4_label_leak_safe = {live['P4_label_leak_safe']} · certify_ok = {live['ok']}")
    if not live["ok"]:
        out["verdict"] = "INSTRUMENT-INVALID — a stance-estimator plant failed; fix before the real run."
        print("\n  VERDICT:", out["verdict"]); _dump(out); return 0

    print("\n[extract] scanning transcripts (content stays on disk) ...")
    trip = H.loop_pairs()
    print(f"  {len(trip)} loop pairs across {len({t[0] for t in trip})} sessions")
    if len(trip) < 200:
        out["verdict"] = f"STANCE-UNIDENTIFIABLE (only {len(trip)} pairs)"; print("\n ", out["verdict"]); _dump(out); return 0
    stride = max(1, len(trip) // N_CAP)
    s1 = [trip[i] for i in range(0, len(trip), stride)][:N_CAP]
    s2 = [trip[i] for i in range(1, len(trip), stride)][:N_CAP]

    a = analyze_stance(build_stance(s1)); b = analyze_stance(build_stance(s2))
    out["primary"], out["replication"] = a, b
    for nm, r in (("primary", a), ("replication", b)):
        print(f"\n[{nm}] n={r['n']} M={r['M']} informative={r['n_informative']} stance_rate={r['stance_rate']}")
        print(f"    sign_base_full={r['sign_base_full']:.3f} vs null_p95={r['null_p95']:.3f} "
              f"(threshold {H.SIGN_PAIR}) -> beats_null={r['beats_null']}")

    rate_ok = 0.05 <= a["stance_rate"] <= 0.95
    inf_ok = a["n_informative"] >= N_MIN_INFORMATIVE and b["n_informative"] >= N_MIN_INFORMATIVE
    if not (rate_ok and inf_ok):
        out["verdict"] = (f"STANCE-UNIDENTIFIABLE — stance_rate {a['stance_rate']} or informative strata "
                          f"({a['n_informative']}/{b['n_informative']} < {N_MIN_INFORMATIVE}) insufficient.")
    elif a["beats_null"] and b["beats_null"]:
        out["verdict"] = (f"BEHAVIORAL-CLOSURE-FOUND — within CONTEXT-MATCHED strata the agent's SPECIFIC "
                          f"utterance predicts the owner's next-turn STANCE above the shift-null band on BOTH "
                          f"replicates (sign {a['sign_base_full']:.3f}/{b['sign_base_full']:.3f} > null "
                          f"{a['null_p95']:.3f}/{b['null_p95']:.3f}). The TEXT-target refusals (H_010 0.406, "
                          f"H_012A 0.424) were WRONG-TARGET artifacts: closure lives in behavior. Semi-"
                          f"interventional (closure-CONSISTENT, cannot anchor) -> RAISES the H_012B prior.")
    else:
        out["verdict"] = (f"BEHAVIORAL-REFUSE — even on the behavioral stance target the utterance does not "
                          f"predict the owner's next-turn stance above the shift-null band (sign "
                          f"{a['sign_base_full']:.3f}/{b['sign_base_full']:.3f} vs null "
                          f"{a['null_p95']:.3f}/{b['null_p95']:.3f}). The refusal is ROBUST ACROSS TARGETS "
                          f"(text AND behavior) — not a wrong-target artifact. Quotable with the P1 noise "
                          f"floor {live['P1_noise_floor']['P1_noise_signs']}. Strengthens H_010+H_012A.")
    print("\n  VERDICT:", out["verdict"])
    print("=" * 84)
    _dump(out)
    return 0


def _dump(m):
    with open(os.path.join(_HERE, "result_h012ab.json"), "w") as f:
        json.dump(m, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"artifact: {os.path.relpath(os.path.join(_HERE, 'result_h012ab.json'), _ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
