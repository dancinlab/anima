#!/usr/bin/env python3
"""LANE A PHASE-1 — lift signal resolution: does the weak-positive composed-lift slope
SURVIVE past the 25-anchor noise floor when the real FLORES corpus grows 10x?

IDENTICAL mechanism + IDENTICAL lift metric as F-CLM-ONCHIP-LAYERPAGE-LADDER
(onchip_layerpage_ladder.py, commits 90b29bcb6/a9e54140d/7d7a4d999). The ONLY changes:
  1. corpus path is a PARAMETER (run 25-anchor AND big-anchor with the same code path),
  2. >=3 backbone seeds per corpus for a seed noise band on the lift,
  3. side-by-side table 25 vs big.
Everything load-bearing is byte-for-byte the prior script: read_limen, encode_spikes,
BACKBONE per-seed int4 random proj, build_fc, binarize_to_inc, concept_margin (between-
minus within-concept Hamming, bits), run_arm (one FC unit chip-resident at a time, page
weights OFF to host, binarize, next unit; composed = all units fit on chip, frozen_head =
only L1 fit, deeper forward-only). lift(N) = margin_composed(N) - margin_frozen(N).

g63 honest: NO SW/CPU fallback. If no HW device -> OPEN-BLOCKED, never simulated. Every
learned_hw flag + margin number is read from the live AKD1000.

Big-anchor corpus = subsample of the FULL FLORES-200 dev+devtest 5-way line-aligned parallel
set (CC-BY-SA-4.0, 2009 concepts available; this run uses 50 concepts x 5 langs = 250 anchors,
10x the prior 25). REAL data, concept-major, byte-identical payloads to the H_911 trainset.
"""
import os, sys, json, struct, hashlib, time
import numpy as np
import akida
from akida import Model, InputData, FullyConnected, AkidaUnsupervised

OUT = os.path.expanduser("~/clm_kosmos_akida/out_phase1"); os.makedirs(OUT, exist_ok=True)
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
INC, LCOMP = 256, 0.1
INPUT_NAME = "parallel"
UNIT_SCHED = [64, 32, 32, 32, 32]          # IDENTICAL to prior ladder
LADDER_N = [2, 3, 4, 5]                     # IDENTICAL
N_LANGS = 5                                  # concept-major: row = concept*N_LANGS + lang
SEEDS = [20260602, 20260603, 20260604]      # IDENTICAL 3 backbone seeds (prior robustness run)

# corpus_name -> abs path to its parallel.limen on the chip host
CORPORA = {
    "anchor25": os.path.expanduser("~/clm_kosmos_akida/corpus/parallel.limen"),
    "anchorBIG": os.path.expanduser("~/clm_kosmos_akida/corpus_big/parallel.limen"),
}


def read_limen(path):                       # verbatim
    with open(path, "rb") as f: blob = f.read()
    assert blob[:8] == LIMEN_MAGIC
    off = 8; struct.unpack_from("<I", blob, off)[0]; off += 4
    count = struct.unpack_from("<I", blob, off)[0]; off += 4
    recs = []
    for _ in range(count):
        rlen = struct.unpack_from("<I", blob, off)[0]; off += 4
        rec = blob[off:off+rlen]; off += rlen
        hlen = struct.unpack_from("<I", rec, 0)[0]
        head = json.loads(rec[4:4+hlen].decode("utf-8"))
        recs.append((head, rec[4+hlen:]))
    return count, recs


def h(a): return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()[:16]


def build_fc(inc, units, nw):               # verbatim
    m = Model()
    m.add(InputData(name="input", input_shape=(1, 1, inc), input_bits=1))
    m.add(FullyConnected(name="fc", units=units, weights_bits=1, activation=False))
    m.compile(AkidaUnsupervised(num_weights=nw, learning_competition=LCOMP))
    return m


def get_w(m): return np.array(m.get_layer("fc").variables["weights"])


def binarize_to_inc(out2d):                 # verbatim
    b = (out2d > np.median(out2d, axis=0, keepdims=True)).astype(np.uint8)
    if b.shape[1] < INC: b = np.pad(b, ((0, 0), (0, INC - b.shape[1])))
    else: b = b[:, :INC]
    return b


def concept_margin(final_out):              # verbatim (row = concept*N_LANGS + lang)
    fb = (final_out > np.median(final_out, axis=0, keepdims=True)).astype(np.uint8)
    n = fb.shape[0]
    concept = np.array([r // N_LANGS for r in range(n)])
    within, between = [], []
    for i in range(n):
        for j in range(i + 1, n):
            d = int(np.count_nonzero(fb[i] != fb[j]))
            (within if concept[i] == concept[j] else between).append(d)
    wm = float(np.mean(within)) if within else 0.0
    bm = float(np.mean(between)) if between else 0.0
    return bm - wm, wm, bm


# ---- live device gate (g63: NO sw fallback) ----
devs = akida.devices()
if not devs:
    raise RuntimeError("OPEN-BLOCKED (g63): no akida HW device on pi5-akida — NO SW fallback")
DEV = devs[0]
print("[p1] akida %s device %s ip %s" % (akida.__version__, DEV.version, DEV.ip_version))


def make_encoder(seed):
    """Per-seed int4 random backbone projection -> spike encoder (verbatim mechanism)."""
    rng_bb = np.random.default_rng(seed)
    BACKBONE_INT4 = rng_bb.integers(-7, 8, size=(INC, INC), dtype=np.int8)
    sha = hashlib.sha256(BACKBONE_INT4.tobytes()).hexdigest()

    def encode_spikes(payload):
        pres = np.zeros(INC, dtype=np.int32)
        for b in payload: pres[b] += 1
        proj = BACKBONE_INT4.astype(np.int32) @ pres
        return (proj > np.median(proj)).astype(np.uint8)
    return encode_spikes, sha


def run_arm(X0, count, N, plastic_deep):    # verbatim mechanism, X0/count parameterized
    X = X0
    units_info = []
    final_out = None
    all_learned = True
    both_hw = True
    for li in range(N):
        units = UNIT_SCHED[li]; nw = max(1, units // 4)
        do_fit = plastic_deep or (li == 0)
        m = build_fc(INC, units, nw); m.map(DEV)
        backend = "hardware:%s" % DEV.version
        pre = get_w(m)
        if do_fit:
            for i in range(X.shape[0]): m.fit(X[i:i+1])
        post = get_w(m)
        out = np.stack([np.array(m.forward(X[i:i+1])).astype(np.int64).ravel()
                        for i in range(X.shape[0])])
        learned = bool(np.any(post != pre)) if do_fit else False
        if do_fit and not learned: all_learned = False
        if not backend.startswith("hardware"): both_hw = False
        units_info.append({
            "unit": li + 1, "units": units, "num_weights": nw, "backend": backend,
            "fit_on_chip": bool(do_fit), "learned_hw": learned,
            "pre_w_sha": h(pre), "post_w_sha": h(post),
            "w_delta_nnz": int(np.count_nonzero(post != pre)) if do_fit else 0,
            "fwd_sum": int(out.sum()),
        })
        final_out = out
        del m
        if li < N - 1:
            X = binarize_to_inc(out).reshape(count, 1, 1, INC)
    margin, within, between = concept_margin(final_out)
    return {
        "N": N, "arm": "composed" if plastic_deep else "frozen_head",
        "units": units_info, "all_deep_learned": all_learned, "both_hw": both_hw,
        "concept_margin_bits": margin, "within_concept_hamming": within,
        "between_concept_hamming": between,
    }


def run_corpus_seed(corpus_name, limen_path, seed):
    count, recs = read_limen(limen_path)
    encode_spikes, bb_sha = make_encoder(seed)
    X0 = np.stack([encode_spikes(p) for (_, p) in recs]).astype(np.uint8).reshape(count, 1, 1, INC)
    input_sha = h(X0)
    print("[p1] corpus=%s seed=%d count=%d input_sha=%s bb=%s"
          % (corpus_name, seed, count, input_sha, bb_sha[:16]))
    rungs = []
    for N in LADDER_N:
        comp = run_arm(X0, count, N, plastic_deep=True)
        froz = run_arm(X0, count, N, plastic_deep=False)
        lift = comp["concept_margin_bits"] - froz["concept_margin_bits"]
        comp_learned = comp["all_deep_learned"] and comp["both_hw"]
        rungs.append({
            "N": N,
            "composed_margin_bits": comp["concept_margin_bits"],
            "frozen_margin_bits": froz["concept_margin_bits"],
            "lift_bits": lift,
            "composed_all_learned_hw": comp_learned,
            "composed_units": comp["units"],
            "rung_verdict": "GREEN" if comp_learned else "RED",
        })
        print("[p1]   N=%d comp=%.4f froz=%.4f LIFT=%+.4f learned_hw=%s"
              % (N, comp["concept_margin_bits"], froz["concept_margin_bits"], lift, comp_learned))
    return {"corpus": corpus_name, "limen_path": limen_path, "seed": seed,
            "anchor_count": count, "input_sha": input_sha, "backbone_sha256": bb_sha,
            "rungs": rungs}


def summarize(corpus_name, per_seed):
    """Per-N mean lift + seed band (min/max/std) + per-seed OLS slope + sign-stability."""
    byN = {N: [] for N in LADDER_N}
    slopes = {}
    all_green = True
    for r in per_seed:
        Ns = np.array([x["N"] for x in r["rungs"]], dtype=float)
        Ls = np.array([x["lift_bits"] for x in r["rungs"]], dtype=float)
        slopes[str(r["seed"])] = float(np.polyfit(Ns, Ls, 1)[0])
        for x in r["rungs"]:
            byN[x["N"]].append(x["lift_bits"])
            if not x["composed_all_learned_hw"]: all_green = False
    per_N = {}
    for N in LADDER_N:
        v = np.array(byN[N], dtype=float)
        per_N[str(N)] = {
            "lifts": [float(z) for z in v],
            "mean": float(v.mean()), "std": float(v.std(ddof=0)),
            "min": float(v.min()), "max": float(v.max()),
            "sign_stable": bool(np.all(v > 0) or np.all(v < 0)),
            "mean_positive": bool(v.mean() > 0),
        }
    sl = np.array(list(slopes.values()), dtype=float)
    return {
        "corpus": corpus_name, "anchor_count": per_seed[0]["anchor_count"],
        "seeds": [r["seed"] for r in per_seed],
        "per_seed_slope": slopes,
        "slope_mean": float(sl.mean()), "slope_std": float(sl.std(ddof=0)),
        "slope_sign_stable": bool(np.all(sl > 0) or np.all(sl < 0)),
        "per_N_lift": per_N,
        "all_rungs_green_hw": all_green,
    }


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    targets = list(CORPORA) if which == "all" else [which]
    result = {
        "hypothesis": "LANE-A-PHASE1-LIFT-SIGNAL-RESOLUTION",
        "ties": ["F-CLM-ONCHIP-LAYERPAGE-LADDER", "a_scale_honest_scope", "a_toy_scale_recheck",
                 "H_904", "a_akida_native_train"],
        "method": ("IDENTICAL paged DEPTH ladder + IDENTICAL cross-lingual concept-margin lift "
                   "metric as the prior 25-anchor ladder; only the corpus size and seed-count "
                   "vary. composed=all units fit on chip; frozen_head=only L1 fit. "
                   "lift=composed-frozen margin (bits). big corpus = subsample of FULL FLORES-200 "
                   "5-way parallel (CC-BY-SA-4.0, real). 3 backbone seeds for the noise band."),
        "akida_version": akida.__version__, "device": str(DEV.version),
        "ip_version": str(DEV.ip_version),
        "unit_schedule": UNIT_SCHED, "ladder_N": LADDER_N, "seeds": SEEDS,
        "learning_competition": LCOMP, "inc": INC,
        "ts_start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "corpora": {},
    }
    for cname in targets:
        per_seed = []
        for seed in SEEDS:
            t0 = time.time()
            rs = run_corpus_seed(cname, CORPORA[cname], seed)
            rs["wall_s"] = round(time.time() - t0, 1)
            per_seed.append(rs)
            # commit-early: dump partial after every seed
            result["corpora"][cname] = {"per_seed": per_seed}
            with open(os.path.join(OUT, "result_phase1.json"), "w") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print("[p1] %s seed=%d done in %.1fs (partial written)" % (cname, seed, rs["wall_s"]))
        result["corpora"][cname]["summary"] = summarize(cname, per_seed)
        with open(os.path.join(OUT, "result_phase1.json"), "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    # side-by-side verdict (only if both corpora present)
    if "anchor25" in result["corpora"] and "anchorBIG" in result["corpora"]:
        s25 = result["corpora"]["anchor25"]["summary"]
        sBIG = result["corpora"]["anchorBIG"]["summary"]
        # resolution test: does big-corpus shrink the per-N seed band AND become sign-stable positive?
        band25 = np.mean([s25["per_N_lift"][str(N)]["std"] for N in LADDER_N])
        bandBIG = np.mean([sBIG["per_N_lift"][str(N)]["std"] for N in LADDER_N])
        big_all_signstable = all(sBIG["per_N_lift"][str(N)]["sign_stable"] for N in LADDER_N)
        big_all_pos = all(sBIG["per_N_lift"][str(N)]["mean_positive"] for N in LADDER_N)
        big_all_neg = all(not sBIG["per_N_lift"][str(N)]["mean_positive"] for N in LADDER_N)
        if big_all_signstable and big_all_pos and bandBIG < band25:
            verdict = "RESOLVED-POSITIVE"
            reason = "10x corpus: every N sign-stable POSITIVE + seed band shrank (composition helps depth)"
        elif (big_all_neg and big_all_signstable) or (abs(sBIG["slope_mean"]) < 0.1 and bandBIG < band25):
            verdict = "COLLAPSE-NULL"
            reason = "10x corpus: lift collapses to ~0 / negative — prior weak-positive was small-sample artifact"
        else:
            verdict = "STILL-AMBIGUOUS"
            reason = "10x corpus: lift sign still not stable across seeds (band did not resolve)"
        result["resolution_verdict"] = {
            "verdict": verdict, "reason": reason,
            "mean_seed_band_bits_25": float(band25),
            "mean_seed_band_bits_BIG": float(bandBIG),
            "band_shrank": bool(bandBIG < band25),
            "big_slope_mean": sBIG["slope_mean"], "big_slope_sign_stable": sBIG["slope_sign_stable"],
            "big_all_N_sign_stable": big_all_signstable,
            "big_all_N_mean_positive": big_all_pos,
        }
    result["ts_end"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(os.path.join(OUT, "result_phase1.json"), "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("\n[p1] ===== PHASE-1 SUMMARY =====")
    for cname in result["corpora"]:
        s = result["corpora"][cname].get("summary")
        if not s: continue
        print("[p1] %s (n=%d): slope_mean=%+.4f band_shrink_ref; green_hw=%s"
              % (cname, s["anchor_count"], s["slope_mean"], s["all_rungs_green_hw"]))
        for N in LADDER_N:
            p = s["per_N_lift"][str(N)]
            print("[p1]   N=%d lift mean=%+.4f [%+.4f..%+.4f] std=%.4f signstable=%s"
                  % (N, p["mean"], p["min"], p["max"], p["std"], p["sign_stable"]))
    if "resolution_verdict" in result:
        rv = result["resolution_verdict"]
        print("[p1] RESOLUTION: %s — %s" % (rv["verdict"], rv["reason"]))
        print("[p1] seed band 25=%.4f BIG=%.4f shrank=%s" %
              (rv["mean_seed_band_bits_25"], rv["mean_seed_band_bits_BIG"], rv["band_shrank"]))
    print("[p1] wrote " + os.path.join(OUT, "result_phase1.json"))


if __name__ == "__main__":
    main()
