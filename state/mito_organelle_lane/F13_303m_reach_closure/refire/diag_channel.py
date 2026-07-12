#!/usr/bin/env python3
"""DIAGNOSTIC ONLY — does NOT and CANNOT change the pre-registered verdict (INVALID).

The refire's pre-registered V2 gate (channel-visibility on the headline m_B_conj) FAILED on
fresh disjoint items: SHOCK (router destroyed) does not significantly move the headline.
Two observationally distinct causes:

  (a) INSTRUMENT BLIND — the margin detector cannot register ANY change to the MoE mixing
      channel (then every capacity null is vacuous → INVALID, no lane conclusion licensed).
  (b) MARGIN-INVARIANT CHANNEL — router destruction DOES massively move the model's raw
      output (logP), but the conjunction margin (a double difference) cancels it → the mixing
      channel is real but ORTHOGONAL to the recombination axis.

This script measures the raw logP displacement caused by SHOCK/EXP vs c0 on the SAME items and
seed as the refire, so we can tell (a) from (b). It touches nothing in the verdict.
"""
import sys, os, json, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("PROBE_ONLY", "0")
import run_refire as R   # reuse the EXACT frozen pipeline (same seeds, same items)

clm = R.clm


def main():
    R.load_exclude()
    W = clm.clm_load_weights(R.CKPT)
    d, E, V = W["d"], W["E"], W["V"]
    R.KGRID = list(range(1, E + 1))
    T = R.T

    # θ — identical derivation to the frozen run
    import random
    with open(R.CORPUS[0], 'rb') as fh:
        fh.seek(400000); raw = fh.read(800000)
    rr = random.Random(R.THETA_PROBE_SEED)
    masses = []
    for _ in range(24):
        o = rr.randrange(0, len(raw) - T - 1)
        tk = np.frombuffer(raw[o:o + T], dtype=np.uint8).astype(np.float64)
        lr_p, _ = R.trunk_split(W, tk)
        masses.append(R.cum_mass(R.probs_of(lr_p, E))[:, 0])
    R.THETA_PREREG = float(np.median(np.concatenate(masses)))

    N_MAIN = R.N_BLOCK * R.ITEMS_PER_BLOCK
    N_PILOT = R.PILOT_BLOCKS * R.ITEMS_PER_BLOCK
    items, mode = R.mine_items(N_MAIN + N_PILOT)
    items = items[:N_MAIN]          # verdict set only
    print("[diag] items", len(items), "mode", mode, "theta", R.THETA_PREREG, flush=True)

    raw_abs = {"SHOCK": [], "EXP": [], "c1_k1": []}   # |Δ logP| vs c0, per sequence
    raw_sgn = {"SHOCK": [], "EXP": [], "c1_k1": []}
    router_l1 = {"SHOCK": [], "EXP": [], "c1_k1": []} # |Δ probs| vs c0, per position (channel size)
    marg = {"SHOCK": [], "EXP": [], "c1_k1": []}      # Δ m_B_conj vs c0, per item

    for idx, it in enumerate(items):
        C = R.ctxs(it)
        cache = {}
        for cname, xname in R.NEED:
            tok, rows, tgt = R.seq_rows(C[cname], it[xname])
            lr, ex = R.trunk_split(W, tok)
            cache[(cname, xname)] = {"ex": ex, "rows": rows, "tgt": tgt,
                                     "p": R.probs_of(lr, E)}

        def Pm_of(P, arm):
            if arm == "c0":
                return P
            if arm == "c1_k1":
                return R.apply_topk(P, np.full(T, 1))
            if arm == "EXP":
                return R.apply_topk(P, R.setpoint_k(P, R.THETA_PREREG))
            if arm == "SHOCK":
                return np.full_like(P, 1.0 / E)

        S = {}
        for arm in ("c0", "c1_k1", "EXP", "SHOCK"):
            S[arm] = {}
            for key, c in cache.items():
                P = Pm_of(c["p"], arm)
                lg = R.mix_logits(W, P, c["ex"], rows=c["rows"])
                S[arm][key] = R.logp(lg, c["tgt"])
                if arm != "c0":
                    router_l1[arm].append(float(np.abs(P - c["p"]).sum(axis=1).mean()))

        for arm in ("c1_k1", "EXP", "SHOCK"):
            for key in cache:
                dv = S[arm][key] - S["c0"][key]
                raw_abs[arm].append(abs(dv)); raw_sgn[arm].append(dv)

        def mB(s):
            lift = lambda c, x: s[(c, x)] - s[("null", x)]
            return lift("AB", "b") - lift("AB", "f")
        b0 = mB(S["c0"])
        for arm in ("c1_k1", "EXP", "SHOCK"):
            marg[arm].append(mB(S[arm]) - b0)
        if (idx + 1) % 20 == 0:
            print("[diag] %d/%d" % (idx + 1, len(items)), flush=True)

    out = {"note": "DIAGNOSTIC ONLY — verdict remains the pre-registered INVALID",
           "n_items": len(items), "arms": {}}
    for arm in ("c1_k1", "EXP", "SHOCK"):
        ra = np.array(raw_abs[arm]); rs = np.array(raw_sgn[arm])
        mg = np.array(marg[arm]); rl = np.array(router_l1[arm])
        out["arms"][arm] = {
            "router_probs_L1_shift_mean": float(rl.mean()),      # how big is the intervention?
            "raw_logP_abs_shift_mean": float(ra.mean()),         # does it reach the OUTPUT?
            "raw_logP_abs_shift_median": float(np.median(ra)),
            "raw_logP_signed_shift_mean": float(rs.mean()),
            "margin_m_B_conj_shift_mean": float(mg.mean()),      # does it reach the DETECTOR?
            "margin_abs_shift_mean": float(np.abs(mg).mean()),
            "ratio_margin_over_raw": float(np.abs(mg).mean() / ra.mean()) if ra.mean() > 0 else None,
        }
    print(json.dumps(out, indent=1))
    json.dump(out, open(os.environ.get("DIAG_OUT", "/home/aiden/h9285refire/diag.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
