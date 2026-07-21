"""H_010 — loop-granger-gate. reframe (C)'s FIRST $0 precheck: on the owner<->agent
conversation loop (a REAL interactive loop, not a passive stream), does the agent's own
utterance U_t carry utterance-SPECIFIC predictive information about the owner's NEXT reply
R_{t+1}, ABOVE (a) the owner's own prior state R_t, (b) a topic-matched WRONG utterance,
(c) the verbatim-echo copy channel?

ASYMMETRIC verdict semantics (Fable Q1): the interventional estimand P(R_{t+1}|do(U_t)) is
NOT identifiable from observational logs (context confounds every U->R association), so NO
$0 result can ANCHOR closed-loop causation. But causation implies dependence (barring the
forbidden faithfulness/exact-cancellation appeal), so the ABSENCE of utterance-specific
dependence above the floors KILLS the natural-loop entry at $0. This is a REFUSE-capable
SPEND GATE, structurally identical to how H_004/H_006/H_009 gated their twins:
  GATE-OPEN     -> licenses the paid live A/B build (NOT an aliveness anchor)
  ECHO-ONLY     -> the copy channel != closed-loop causation; thesis refused on the natural loop
  LOOP-REFUSED  -> no utterance-specific dependence; the $0 entry to reframe C is closed
  INSTRUMENT-INVALID -> a liveness plant failed; fix the instrument before any verdict

Estimator = the CERTIFIED H_009' shift-null LOO k-NN machinery, reused. Card frozen
2026-07-16. Privacy: NO owner message CONTENT is written to the repo — only aggregate
sign/rank/err numbers. The owner's words stay on their own disk.

Run: python3 state/h010_loop-granger-gate_2026-07-16/run_h010.py
"""

from __future__ import annotations

import glob
import heapq
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "tool"))
sys.path.insert(0, os.path.join(_ROOT, "state", "h009_f3-continuous-oracle_2026-07-16"))

from anima_v3 import binom_sf
from run_h009 import features, _sqdist, _median, _LCG   # certified machinery reused

TRANSCRIPTS = os.path.expanduser("~/.claude/projects/*/*.jsonl")
NOISE = re.compile(r'^(\s*<|Caveat:|\[Request interrupted|# |Contents of|system-reminder|<command-)')
UB, RB = 4096, 4096          # U_t tail bytes, R first bytes
MIN_PAIRS = 12               # sessions with >= this many loop pairs
N_PRIMARY = 2000             # deterministic-stride sample size (pool = the same sample)
KNN = 5
ECHO_G = 16                  # verbatim-echo n-gram (bytes)
SIGN_PAIR = 0.55             # LC-2 per-pair sign threshold
SIGN_SESS = 0.60             # LC-2 session-level threshold
SHIFTS = 24                  # within-session shift-null count (LC-1a)


# ---- transcript -> loop pairs (genuine owner typing only) --------------------
def _text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def session_turns(path: str) -> list:
    """Ordered [[role, text]] for one transcript, consecutive same-role collapsed.
    role 'O' = genuine owner typing (no tool_result / hook noise); 'A' = assistant text."""
    ev = []
    try:
        fh = open(path, encoding="utf-8", errors="replace")
    except OSError:
        return []
    for line in fh:
        try:
            r = json.loads(line)
        except ValueError:
            continue
        typ = r.get("type")
        if typ == "assistant":
            t = _text(r.get("message", {}).get("content")).strip()
            if t:
                ev.append(("A", t))
        elif typ == "user":
            c = r.get("message", {}).get("content")
            if isinstance(c, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in c):
                continue
            t = _text(c).strip()
            if len(t) < 3 or NOISE.match(t):
                continue
            ev.append(("O", t))
    coll = []
    for role, t in ev:
        if coll and coll[-1][0] == role:
            coll[-1][1] += "\n" + t
        else:
            coll.append([role, t])
    return coll


def loop_pairs():
    """All (R_t, U_t, R_{t+1}) byte-triples from O-A-O windows, sessions with >= MIN_PAIRS.
    Returns [(sess_id, sidx, Rt_bytes, U_bytes, Rt1_bytes)] chronological within session."""
    out = []
    for path in sorted(glob.glob(TRANSCRIPTS)):
        coll = session_turns(path)
        trip = []
        for i in range(len(coll) - 2):
            if coll[i][0] == "O" and coll[i + 1][0] == "A" and coll[i + 2][0] == "O":
                rt = coll[i][1].encode("utf-8", "replace")[-RB:]
                u = coll[i + 1][1].encode("utf-8", "replace")[-UB:]
                rt1 = coll[i + 2][1].encode("utf-8", "replace")[:RB]
                if len(rt1) >= 64:
                    trip.append((rt, u, rt1))
        if len(trip) >= MIN_PAIRS:
            sid = os.path.basename(path)
            for k, (rt, u, rt1) in enumerate(trip):
                out.append((sid, k, rt, u, rt1))
    return out


def echo_strip(rt1: bytes, u: bytes) -> bytes:
    """Mask every R byte covered by a >= ECHO_G verbatim substring of U (the copy channel)."""
    if len(u) < ECHO_G or len(rt1) < ECHO_G:
        return rt1
    grams = set()
    for i in range(len(u) - ECHO_G + 1):
        grams.add(u[i:i + ECHO_G])
    keep = [True] * len(rt1)
    for p in range(len(rt1) - ECHO_G + 1):
        if bytes(rt1[p:p + ECHO_G]) in grams:
            for q in range(p, p + ECHO_G):
                keep[q] = False
    stripped = bytes(b for b, k in zip(rt1, keep) if k)
    return stripped if len(stripped) >= 16 else b"  "


# ---- estimator: precompute distRt + distU; all arms reindex distU -----------
def _distmat(feats: list) -> list:
    n = len(feats)
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        fi = feats[i]
        row = D[i]
        for j in range(i + 1, n):
            d = _sqdist(fi, feats[j])
            row[j] = d
            D[j][i] = d
    return D


def _knn_err(targets, cand_of, distrow_fn, kk=KNN):
    """Per-pair LOO squared error. distrow_fn(i) -> full distance row for query i;
    cand_of[i] = allowed candidate indices (session-aware exclusion)."""
    n = len(targets)
    dim = len(targets[0])
    out = []
    for i in range(n):
        row = distrow_fn(i)
        nn = heapq.nsmallest(kk, cand_of[i], key=lambda j: (row[j], j))
        pred = [sum(targets[j][t] for j in nn) / len(nn) for t in range(dim)]
        out.append(_sqdist(targets[i], pred))
    return out


def _sign_frac(ea, eb):
    """fraction of pairs with ea > eb (i.e. arm-b predicts strictly better)."""
    return sum(1 for a, b in zip(ea, eb) if a > b) / len(ea)


def analyze(pairs):
    """pairs = [(sess, sidx, feat_Rt, feat_U, target_stripped, target_unstripped)].
    Uses distRt + distU precompute; the 4 arms reindex distU's first axis."""
    n = len(pairs)
    sess = [p[0] for p in pairs]
    sidx = [p[1] for p in pairs]
    fRt = [p[2] for p in pairs]
    fU = [p[3] for p in pairs]
    tgt_s = [p[4] for p in pairs]        # echo-stripped (primary)
    tgt_u = [p[5] for p in pairs]        # unstripped (diagnostic)

    distRt = _distmat(fRt)
    distU = _distmat(fU)

    cand_of = []
    for i in range(n):
        cand_of.append([j for j in range(n)
                        if j != i and not (sess[j] == sess[i] and abs(sidx[i] - sidx[j]) < 2)])

    topic_idx = list(range(n))
    for i in range(n):
        best, bd = i, float("inf")
        for j in range(n):
            if sess[j] == sess[i] and abs(sidx[i] - sidx[j]) >= 2 and distU[i][j] < bd:
                bd, best = distU[i][j], j
        topic_idx[i] = best
    by_sidx = {}
    for i in range(n):
        by_sidx.setdefault(sidx[i], []).append(i)
    xsess_idx = list(range(n))
    for i in range(n):
        cands = [j for j in by_sidx.get(sidx[i], []) if sess[j] != sess[i]]
        xsess_idx[i] = cands[0] if cands else (i + 1) % n

    def row_base(i):
        return distRt[i]

    def row_full(i):
        ri, ui = distRt[i], distU[i]
        return [ri[j] + ui[j] for j in range(n)]

    def row_map(i, umap):
        ri, ui = distRt[i], distU[umap[i]]
        return [ri[j] + ui[j] for j in range(n)]

    err_base = _knn_err(tgt_s, cand_of, row_base)
    err_full = _knn_err(tgt_s, cand_of, row_full)
    err_topic = _knn_err(tgt_s, cand_of, lambda i: row_map(i, topic_idx))
    err_xsess = _knn_err(tgt_s, cand_of, lambda i: row_map(i, xsess_idx))
    err_full_u = _knn_err(tgt_u, cand_of, row_full)
    err_topic_u = _knn_err(tgt_u, cand_of, lambda i: row_map(i, topic_idx))

    # within-session shift-null on FULL (LC-1a)
    sess_members = {}
    for i in range(n):
        sess_members.setdefault(sess[i], []).append(i)
    for s in sess_members:
        sess_members[s].sort(key=lambda i: sidx[i])
    shift_err = []
    for d in range(1, SHIFTS + 1):
        umap = list(range(n))
        for mem in sess_members.values():
            L = len(mem)
            if L < 3:
                continue
            for pos, i in enumerate(mem):
                umap[i] = mem[(pos + d) % L]
        shift_err.append(sum(_knn_err(tgt_s, cand_of, lambda i, um=umap: row_map(i, um))))
    e_full0 = sum(err_full)
    rank_full = sum(1 for se in shift_err if se <= e_full0)
    align_full = (_median(shift_err) - e_full0) if shift_err else 0.0

    per_sess = {}
    for i in range(n):
        per_sess.setdefault(sess[i], []).append(i)
    sess_pass = tot_sess = 0
    for mem in per_sess.values():
        if len(mem) < 3:
            continue
        tot_sess += 1
        if sum(1 for i in mem if err_topic[i] > err_full[i]) / len(mem) > 0.5:
            sess_pass += 1

    return {
        "n": n, "n_sess": len(per_sess),
        "sign_base_full": _sign_frac(err_base, err_full),
        "sign_topic_full": _sign_frac(err_topic, err_full),
        "sign_xsess_full": _sign_frac(err_xsess, err_full),
        "sign_base_xsess": _sign_frac(err_base, err_xsess),
        "sign_topic_full_unstripped": _sign_frac(err_topic_u, err_full_u),
        "rank_full": rank_full, "n_shifts": len(shift_err), "align_full": align_full,
        "sess_sign_frac": (sess_pass / tot_sess) if tot_sess else 0.0, "tot_sess": tot_sess,
        "err_full_sum": e_full0, "err_base_sum": sum(err_base), "err_topic_sum": sum(err_topic),
    }


def build(triples):
    """[(sess, sidx, Rt, U, Rt1)] -> [(sess, sidx, feat_Rt, feat_U, tgt_stripped, tgt_unstripped)]"""
    return [(sess, sidx, features(rt), features(u), features(echo_strip(rt1, u)), features(rt1))
            for sess, sidx, rt, u, rt1 in triples]


# ---- liveness plants (synthetic TEXT triples through the same pipeline) -------
def _rand_text(rng, n):
    return bytes(33 + int(rng.u() * 94) for _ in range(n))


def plant_pos(n_sess=24, per=16, n_act=16, seed=101):
    """P-POS: R carries a CIPHER of the agent's action (action run in U at alphabet 65+a -> reply
    signature in R at DISJOINT alphabet 150+a: a real map, zero verbatim overlap -> survives echo-
    strip), over a shared drifting topic. Same-action pairs cluster across sessions, so the true
    utterance retrieves same-action neighbours whose reply-signature matches. Must read GATE-OPEN."""
    rng = _LCG(seed)
    per = min(per, n_act)                                 # unique action per pair within a session
    trip = []
    for s in range(n_sess):
        topic = _rand_text(rng, 120)
        for k in range(per):
            a = k                                        # distinct within session -> topic floor picks a WRONG action
            u = bytes([65 + a]) * 200 + _rand_text(rng, 40)   # U encodes ONLY the action (so distU discriminates it)
            sig = bytes([150 + a]) * 160                     # cipher of a, disjoint alphabet
            rt = topic + _rand_text(rng, 80)
            rt1 = topic + sig + _rand_text(rng, 40)
            trip.append((f"P{s}", k, rt[-RB:], u[-UB:], rt1[:RB]))
    return trip


def plant_null(n_sess=20, per=15, seed=202):
    """P-NULL: U and R both driven by a shared latent topic, ZERO U->R coupling (the confound
    planted). Must read LOOP-REFUSED (FULL must NOT beat TOPIC)."""
    rng = _LCG(seed)
    trip = []
    for s in range(n_sess):
        for k in range(per):
            topic = _rand_text(rng, 250)
            u = topic + _rand_text(rng, 200)
            rt = topic + _rand_text(rng, 200)
            rt1 = topic + _rand_text(rng, 200)
            trip.append((f"N{s}", k, rt[-RB:], u[-UB:], rt1[:RB]))
    return trip


def plant_echo(n_sess=24, per=16, n_q=16, seed=303):
    """P-ECHO: R VERBATIM-quotes the agent (a RECURRING quote from a fixed set, so same-quote pairs
    cluster and the true utterance retrieves them). UNstripped: FULL beats TOPIC (the quote in U
    predicts the quote in R). STRIPPED: the quote is removed from R -> the copy channel vanishes ->
    FULL no longer beats TOPIC. The instrument must read ECHO-ONLY (unstripped pass, stripped fail)."""
    rng = _LCG(seed)
    quotes = [_rand_text(rng, 120) for _ in range(n_q)]
    per = min(per, n_q)                                  # unique quote per pair within a session
    trip = []
    for s in range(n_sess):
        topic = _rand_text(rng, 120)
        for k in range(per):
            q = k                                        # distinct within session -> topic floor picks a WRONG quote
            u = topic + quotes[q] + _rand_text(rng, 60)
            rt = topic + _rand_text(rng, 60)
            rt1 = quotes[q] + topic + _rand_text(rng, 60)     # verbatim recurring quote in R
            trip.append((f"E{s}", k, rt[-RB:], u[-UB:], rt1[:RB]))
    return trip


def _plant_gate_open(mm):
    return mm["rank_full"] <= 2 and mm["sign_base_full"] >= SIGN_PAIR and mm["sign_topic_full"] >= SIGN_PAIR


def liveness():
    pos = analyze(build(plant_pos()))
    nul = analyze(build(plant_null()))
    ech = analyze(build(plant_echo()))
    pos_ok = _plant_gate_open(pos)
    null_ok = nul["sign_topic_full"] < SIGN_PAIR
    echo_ok = ech["sign_topic_full_unstripped"] >= SIGN_PAIR and ech["sign_topic_full"] < SIGN_PAIR
    return {
        "P-POS": {"sign_topic_full": pos["sign_topic_full"], "sign_base_full": pos["sign_base_full"],
                  "rank_full": pos["rank_full"], "pass": bool(pos_ok)},
        "P-NULL": {"sign_topic_full": nul["sign_topic_full"], "pass": bool(null_ok)},
        "P-ECHO": {"unstripped": ech["sign_topic_full_unstripped"], "stripped": ech["sign_topic_full"],
                   "pass": bool(echo_ok)},
        "ok": bool(pos_ok and null_ok and echo_ok),
    }


def _dump(m):
    with open(os.path.join(_HERE, "result.json"), "w") as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"artifacts: {os.path.relpath(os.path.join(_HERE, 'result.json'), _ROOT)}")


def main() -> int:
    print("=" * 80)
    print("H_010 — loop-granger-gate · owner<->agent loop, utterance-specific dependence ($0)")
    print("=" * 80)
    m = {"knn": KNN, "sign_pair": SIGN_PAIR, "sign_sess": SIGN_SESS}

    print("\n[C-5 liveness] three plants (P-POS gate-open · P-NULL refuse · P-ECHO echo-only):")
    live = liveness()
    m["liveness"] = live
    for k in ("P-POS", "P-NULL", "P-ECHO"):
        print(f"  {k}: {json.dumps(live[k], ensure_ascii=False)}")
    print(f"  liveness_ok = {live['ok']}")

    print("\n[extract] scanning transcripts ...")
    trip = loop_pairs()
    n_sess = len({t[0] for t in trip})
    print(f"  {len(trip)} loop pairs across {n_sess} sessions (>= {MIN_PAIRS} pairs each)")
    m["total_pairs"], m["total_sessions"] = len(trip), n_sess
    if len(trip) < 200:
        m["verdict"] = f"INSTRUMENT-INVALID (only {len(trip)} loop pairs — substrate too thin)"
        print(f"\n  VERDICT: {m['verdict']}")
        _dump(m)
        return 0

    stride = max(1, len(trip) // N_PRIMARY)
    s1 = [trip[i] for i in range(0, len(trip), stride)][:N_PRIMARY]
    s2 = [trip[i] for i in range(1, len(trip), stride)][:N_PRIMARY]
    print(f"  primary N={len(s1)} · replication N={len(s2)} (stride {stride})")

    a = analyze(build(s1))
    b = analyze(build(s2))
    m["primary"], m["replication"] = a, b
    for name, r in (("primary", a), ("replication", b)):
        print(f"\n[{name}] n={r['n']} sess={r['n_sess']}")
        print(f"    LC-1 ceiling: rank_full={r['rank_full']}/{r['n_shifts']} (<=2?) · "
              f"sign(base>full)={r['sign_base_full']:.3f} (>= {SIGN_PAIR}?)")
        print(f"    LC-2 topic(PRIMARY): sign(topic>full)={r['sign_topic_full']:.3f} (pair >= {SIGN_PAIR}?) · "
              f"session_frac={r['sess_sign_frac']:.3f}/{r['tot_sess']} (>= {SIGN_SESS}?)")
        print(f"    LC-3 echo: unstripped sign(topic>full)={r['sign_topic_full_unstripped']:.3f} "
              f"(vs stripped {r['sign_topic_full']:.3f})")
        print(f"    LC-4 floors: sign(xsess>full)={r['sign_xsess_full']:.3f} · "
              f"sign(base>xsess)={r['sign_base_xsess']:.3f}")

    npair = a["n"]
    need = next((c for c in range(npair, 0, -1) if binom_sf(c - 1, npair, 0.5) < 0.05), npair)
    lc1 = a["rank_full"] <= 2 and a["sign_base_full"] >= SIGN_PAIR
    lc2_pair = a["sign_topic_full"] >= SIGN_PAIR
    lc2_sess = a["sess_sign_frac"] >= SIGN_SESS
    lc2 = lc2_pair and lc2_sess
    lc3_echo_only = a["sign_topic_full_unstripped"] >= SIGN_PAIR and a["sign_topic_full"] < SIGN_PAIR
    # LC-4 XSESS = DIAGNOSTIC ONLY (not a gate): the three-plant C-5 liveness already provides the
    # leak protection (P-POS = FULL-favoring works when signal is present; P-NULL = no false positive;
    # P-ECHO = the copy channel is not mistaken for causation). XSESS is confounded by query
    # dimensionality (BASE 256 vs U-arms 512) and by conversation-position correlation, so it is
    # reported, not gated. Ordering sanity (topic-matched TOPIC is a stronger floor than random XSESS).
    lc4_diag = {"xsess_full": a["sign_xsess_full"], "topic_full": a["sign_topic_full"],
                "base_xsess": a["sign_base_xsess"]}
    lc6 = (b["sign_topic_full"] >= SIGN_PAIR) == lc2_pair
    m.update({"lc1": lc1, "lc2_pair": lc2_pair, "lc2_sess": lc2_sess, "lc2": lc2,
              "lc3_echo_only": lc3_echo_only, "lc4_diag": lc4_diag, "lc6_replicates": lc6,
              "sign_need_frac": need / npair})

    if not live["ok"]:
        v = "INSTRUMENT-INVALID (a C-5 liveness plant failed — fix before any verdict)"
    elif lc3_echo_only:
        v = ("ECHO-ONLY — utterance-specific dependence is present UNSTRIPPED but vanishes after echo-strip: "
             "the owner is quoting the agent verbatim (the L11 copy channel), not responding causally. Thesis "
             "REFUSED on the natural loop; the copy channel != closed-loop causation.")
    elif lc1 and lc2:
        rep = "replicates" if lc6 else "does NOT replicate (LC-6 PARTIAL)"
        v = (f"GATE-OPEN — on echo-stripped targets the true utterance predicts the owner's next reply BEYOND "
             f"owner-state AND a topic-matched wrong utterance (sign(topic>full)={a['sign_topic_full']:.3f} "
             f">= {SIGN_PAIR} pair, session {a['sess_sign_frac']:.3f} >= {SIGN_SESS}; {rep}). NECESSARY condition "
             "ONLY — LICENSES the paid live A/B intervention build, NOT an aliveness anchor (P(R|do(U)) is not "
             "observationally identifiable · Fable Q1).")
    else:
        why = []
        if not lc1:
            why.append(f"LC-1 rank_full={a['rank_full']}/sign_base_full={a['sign_base_full']:.3f}")
        if not lc2_pair:
            why.append(f"LC-2 pair sign(topic>full)={a['sign_topic_full']:.3f}<{SIGN_PAIR}")
        elif not lc2_sess:
            why.append(f"LC-2 session {a['sess_sign_frac']:.3f}<{SIGN_SESS}")
        v = ("LOOP-REFUSED — the true utterance does NOT predict the owner's next reply above the topic-matched "
             f"floor on the natural loop ({'; '.join(why)}). The owner replies on-topic to anything relevant "
             "(topic decoration, the F3 pattern in loop clothing). The $0 entry to reframe C is closed; only the "
             "paid live A/B intervention remains (research-gated).")
    m["verdict"] = v
    print(f"\n{'-' * 80}\n  VERDICT: {v}\n{'=' * 80}")
    _dump(m)
    return 0


if __name__ == "__main__":
    sys.exit(main())
