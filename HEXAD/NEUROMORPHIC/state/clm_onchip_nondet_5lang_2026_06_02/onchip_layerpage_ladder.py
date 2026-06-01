#!/usr/bin/env python3
"""F-CLM-ONCHIP-LAYERPAGE-LADDER — paged DEPTH ladder on a SINGLE AKD1000.

Extends F-CLM-ONCHIP-LAYERPAGE-COMPOSE (2-unit pilot 🟢 GREEN, 2026-06-01) from 2 units
to an N-unit honest scale ladder (N in {2,3,4,5}). Each plastic FC unit is resident
ONE-AT-A-TIME on the live AKD1000; weights page off to host between units (same exact
mechanism as the pilot: build_fc -> map(DEV) -> on-chip fit() per sample -> on-chip
forward -> page weights OFF to host -> binarize -> next unit). The single 8MB SRAM holds
one FC head at a time, so paged depth > single-residency capacity.

THE REAL QUESTION (a_scale_honest_scope, >=3 rungs): does on-chip COMPOSED learning hold
as paged depth grows? Two arms per rung, identical pipeline + identical seeds:
  - composed (plastic): every paged unit fit()s ON CHIP.
  - frozen-head (control): L1 fit()s on chip (a learned head feeds the stack), but the
    DEEPER paged units (L2..LN) are mapped + forwarded WITHOUT fit() — weights frozen at
    init. This isolates whether on-chip plasticity on the deeper paged units buys anything.

END-TO-END SIGNAL (falsifiable, deterministic, identical pipeline for both arms):
  cross-lingual concept-alignment MARGIN on the FINAL paged unit's binarized forward output.
  Corpus = 25 anchors = 5 concepts x 5 langs in PARALLEL (concept-major) order. A composed
  representation that retains cross-lingual linkage makes the 5 langs of the SAME concept
  closer (within-concept Hamming) than different concepts (between-concept Hamming).
    signal = mean_between_concept_Hamming - mean_within_concept_Hamming   (bits, higher=better)
  lift(N) = signal_composed(N) - signal_frozen(N).  Slope sign of lift over N = does
  composed DEPTH scale (lift grows), saturate (flat), or degrade (lift shrinks/goes negative).

GREEN-per-rung iff: ALL paged units in the composed arm learned ON CHIP (post!=pre on the
hardware backend) AND the paged composition ran end-to-end on real silicon. g63 honest:
NO SW/CPU fallback for the plastic step; if no HW device -> OPEN-BLOCKED, not simulated.
The TREND verdict (scale/saturate/degrade) is read from the real chip numbers, NOT assumed.
Full feature-plasticity beyond last-FC and full 3B/7B remain DEFERRED — this measures the
PRIMITIVE's depth-scaling only. H_679 / H_904 / a_akida_native_train / a_nondet_identity tie.
"""
import os, json, struct, hashlib, time
import numpy as np
import akida
from akida import Model, InputData, FullyConnected, AkidaUnsupervised

CORPUS = os.path.expanduser("~/clm_kosmos_akida/corpus")
OUT = os.path.expanduser("~/clm_kosmos_akida/out"); os.makedirs(OUT, exist_ok=True)
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
INC, LCOMP = 256, 0.1
INPUT_NAME = "parallel"
# Ladder schedule: L1=64u (matches pilot), each deeper paged unit = 32u (<= residency).
# N in {2,3,4,5}; unit i (1-indexed) uses UNIT_SCHED[i-1].  NW = units//4 (matches pilot 64->16, 32->8).
UNIT_SCHED = [64, 32, 32, 32, 32]
LADDER_N = [2, 3, 4, 5]
N_CONCEPTS, N_LANGS = 5, 5            # parallel order = concept-major: rows [c*5 + lang]

def read_limen(path):
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

rng_bb = np.random.default_rng(20260602)
BACKBONE_INT4 = rng_bb.integers(-7, 8, size=(INC, INC), dtype=np.int8)
BACKBONE_SHA = hashlib.sha256(BACKBONE_INT4.tobytes()).hexdigest()

def encode_spikes(payload):
    pres = np.zeros(INC, dtype=np.int32)
    for b in payload: pres[b] += 1
    proj = BACKBONE_INT4.astype(np.int32) @ pres
    return (proj > np.median(proj)).astype(np.uint8)

def build_fc(inc, units, nw):
    m = Model()
    m.add(InputData(name="input", input_shape=(1, 1, inc), input_bits=1))
    m.add(FullyConnected(name="fc", units=units, weights_bits=1, activation=False))
    m.compile(AkidaUnsupervised(num_weights=nw, learning_competition=LCOMP))
    return m

def get_w(m): return np.array(m.get_layer("fc").variables["weights"])
def h(a): return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()[:16]

def binarize_to_inc(out2d):
    """per-feature median threshold -> binary, pad/trim to INC. (same as pilot L1->L2 path)"""
    b = (out2d > np.median(out2d, axis=0, keepdims=True)).astype(np.uint8)
    if b.shape[1] < INC: b = np.pad(b, ((0, 0), (0, INC - b.shape[1])))
    else: b = b[:, :INC]
    return b

def concept_margin(final_out):
    """cross-lingual concept-alignment margin (bits) on binarized FINAL output.
    rows are concept-major: row = concept*N_LANGS + lang. within = same concept diff lang;
    between = diff concept. returns (between_mean - within_mean) of Hamming distance."""
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
count, recs = read_limen(os.path.join(CORPUS, INPUT_NAME + ".limen"))
X0 = np.stack([encode_spikes(p) for (_, p) in recs]).astype(np.uint8).reshape(count, 1, 1, INC)
INPUT_SHA = h(X0)
print("[ladder] akida %s device %s ip %s" % (akida.__version__, DEV.version, DEV.ip_version))
print("[ladder] input=%s count=%d input_sha=%s sched=%s" % (INPUT_NAME, count, INPUT_SHA, UNIT_SCHED))


def run_arm(N, plastic_deep):
    """Run a paged N-unit stack. plastic_deep=True => composed (every unit fit on chip).
    plastic_deep=False => frozen-head control (only L1 fit on chip; L2..LN forward-only).
    Only ONE unit chip-resident at a time (del + re-map per unit). Returns dict."""
    X = X0
    units_info = []
    final_out = None
    all_learned = True
    both_hw = True
    for li in range(N):
        units = UNIT_SCHED[li]; nw = max(1, units // 4)
        do_fit = plastic_deep or (li == 0)   # L1 always fits; deeper units fit only if plastic_deep
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
        # page weights OFF to host; free the single SRAM residency for the next unit
        np.save(os.path.join(OUT, "ladder_N%d_%s_L%d.npy" %
                             (N, "plastic" if plastic_deep else "frozen", li + 1)), post)
        final_out = out
        del m
        if li < N - 1:
            X = binarize_to_inc(out).reshape(count, 1, 1, INC)
    margin, within, between = concept_margin(final_out)
    return {
        "N": N, "arm": "composed" if plastic_deep else "frozen_head",
        "units": units_info, "all_deep_learned": all_learned, "both_hw": both_hw,
        "final_out_shape": list(final_out.shape),
        "concept_margin_bits": margin, "within_concept_hamming": within,
        "between_concept_hamming": between,
    }


rungs = []
for N in LADDER_N:
    print("\n[ladder] ===== RUNG N=%d =====" % N)
    comp = run_arm(N, plastic_deep=True)
    froz = run_arm(N, plastic_deep=False)
    lift = comp["concept_margin_bits"] - froz["concept_margin_bits"]
    comp_learned = comp["all_deep_learned"] and comp["both_hw"]
    rung = {
        "N": N,
        "composed": comp, "frozen_head": froz,
        "composed_margin_bits": comp["concept_margin_bits"],
        "frozen_margin_bits": froz["concept_margin_bits"],
        "lift_bits": lift,
        "composed_all_learned_hw": comp_learned,
        "rung_verdict": "GREEN" if comp_learned else "RED",
    }
    rungs.append(rung)
    print("[ladder] N=%d composed_margin=%.4f frozen_margin=%.4f LIFT=%+.4f all_learned_hw=%s verdict=%s"
          % (N, comp["concept_margin_bits"], froz["concept_margin_bits"], lift, comp_learned, rung["rung_verdict"]))
    # commit-early surface: dump partial ladder after every rung
    partial = {"hypothesis": "F-CLM-ONCHIP-LAYERPAGE-LADDER", "partial": True,
               "akida_version": akida.__version__, "device": str(DEV.version),
               "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "ladder_so_far": rungs}
    with open(os.path.join(OUT, "result_layerpage_ladder.json"), "w") as f:
        json.dump(partial, f, indent=2, ensure_ascii=False)

# ---- trend verdict from REAL numbers (NOT assumed) ----
lifts = np.array([r["lift_bits"] for r in rungs], dtype=float)
Ns = np.array([r["N"] for r in rungs], dtype=float)
slope = float(np.polyfit(Ns, lifts, 1)[0]) if len(Ns) >= 2 else 0.0
all_green = all(r["composed_all_learned_hw"] for r in rungs)
if not all_green:
    trend = "DEGRADE-HW"; trend_reason = "one or more rungs failed to learn on chip (composed arm)"
elif slope > 0.5:
    trend = "SCALE"; trend_reason = "composed lift INCREASES with paged depth (slope %+.3f bits/unit)" % slope
elif slope < -0.5:
    trend = "DEGRADE"; trend_reason = "composed lift DECREASES with paged depth (slope %+.3f bits/unit)" % slope
else:
    trend = "SATURATE"; trend_reason = "composed lift FLAT vs paged depth (slope %+.3f bits/unit)" % slope

res = {
    "hypothesis": "F-CLM-ONCHIP-LAYERPAGE-LADDER",
    "ties": ["H_679", "H_904", "F-CLM-ONCHIP-LAYERPAGE-COMPOSE", "a_akida_native_train", "a_nondet_identity", "a_scale_honest_scope"],
    "method": ("paged DEPTH ladder on a single AKD1000: N in {2,3,4,5} plastic FC units, one resident "
               "at a time (build_fc -> map(DEV) -> on-chip fit() per sample -> on-chip forward -> page "
               "weights OFF -> binarize -> next unit). Two arms/rung (composed: all units fit on chip; "
               "frozen_head: only L1 fit, deeper units forward-only). Signal = cross-lingual concept "
               "margin (between-concept minus within-concept Hamming, bits) on final binarized output. "
               "lift = composed - frozen. Trend = OLS slope of lift over N."),
    "akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "corpus": "clm-kosmos-akida-5lang-semantic", "languages": "ko,en,zh,ru,ja", "input": INPUT_NAME,
    "anchor_count": count, "backbone_int4_sha256": BACKBONE_SHA, "input_sha": INPUT_SHA,
    "inc": INC, "unit_schedule": UNIT_SCHED, "ladder_N": LADDER_N, "learning_competition": LCOMP,
    "only_one_resident_at_a_time": True,
    "rungs": rungs,
    "lift_slope_bits_per_unit": slope,
    "trend_verdict": trend, "trend_reason": trend_reason,
    "all_rungs_green_hw": all_green,
    "deferred": ["full feature-plasticity beyond last-FC (only last-FC plastic per unit)",
                 "full 3B/7B language-model training (this measures the depth-paging PRIMITIVE only)"],
}
with open(os.path.join(OUT, "result_layerpage_ladder.json"), "w") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
print("\n[ladder] ===== LADDER TABLE =====")
print("[ladder]  N | composed | frozen  |  lift   | learned_hw")
for r in rungs:
    print("[ladder] %2d | %8.4f | %7.4f | %+7.4f | %s"
          % (r["N"], r["composed_margin_bits"], r["frozen_margin_bits"], r["lift_bits"],
             r["composed_all_learned_hw"]))
print("[ladder] lift slope = %+.4f bits/unit -> TREND %s (%s)" % (slope, trend, trend_reason))
print("[ladder] all_rungs_green_hw=%s" % all_green)
print("[ladder] wrote " + os.path.join(OUT, "result_layerpage_ladder.json"))
