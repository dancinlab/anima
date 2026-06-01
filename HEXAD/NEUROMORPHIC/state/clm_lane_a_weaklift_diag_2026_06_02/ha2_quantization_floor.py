#!/usr/bin/env python3
"""H-A2 — QUANTIZATION-FLOOR diagnostic (Lane A weak-lift).

Is the weak composed-lift a readout-QUANTIZATION artifact, NOT a corpus/capacity limit? The prior
ladder binarizes the paged unit's output with a per-feature-MEDIAN 1-bit threshold before computing
the cross-lingual concept-margin. A 1-bit readout throws away most of the analog activation spread;
if the cross-lingual linkage lives in finer gradations, a 1-bit Hamming margin would read ~0 even
when the underlying representation is well-separated.

THIS run holds EVERYTHING fixed (25 anchors, same paged ladder N{2,3,4,5}, same on-chip plastic
fit, live AKD1000) and ONLY swaps the readout quantization of the FINAL paged unit's analog forward
output: 1-bit (median, = the prior pipeline) vs 2-bit, 3-bit, 4-bit per-feature quantile readout.
For a B-bit readout each feature column is mapped to one of 2^B levels by per-feature quantiles, and
the concept-margin uses L1 (Manhattan) distance between the multi-level code vectors (1-bit L1 ==
Hamming, so B=1 reproduces the prior margin exactly as a sanity anchor). lift_B = composed - frozen
at bit-depth B. We bootstrap a 95% CI on lift over the 25-anchor pair set.

FALSIFIER (pre-registered):
  H-A2 TRUE  iff  multi-bit lift CI_lo > 0  while the 1-bit lift CI straddles 0
                 -> quantization is the bottleneck (the lift is REAL but the 1-bit readout hides it).
  H-A2 FALSE iff  multi-bit lift also straddles 0 (CI_lo <= 0) -> not a quantization artifact.

g63 honest: live AKD1000 ONLY; the on-chip plastic forward is identical to the prior ladder — only
the host-side READOUT quantization changes (a legitimate measurement choice, not a chip change).
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
UNIT_SCHED = [64, 32, 32, 32, 32]
LADDER_N = [2, 3, 4, 5]
N_CONCEPTS, N_LANGS = 5, 5
BACKBONE_SEED = 20260602
BIT_DEPTHS = [1, 2, 3, 4]
N_BOOT = 2000

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

rng_bb = np.random.default_rng(BACKBONE_SEED)
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
    b = (out2d > np.median(out2d, axis=0, keepdims=True)).astype(np.uint8)
    if b.shape[1] < INC: b = np.pad(b, ((0, 0), (0, INC - b.shape[1])))
    else: b = b[:, :INC]
    return b

def quantize_bits(out2d, bits):
    """per-feature quantile quantization to 2^bits levels. bits=1 (median) reproduces the prior
    1-bit Hamming readout exactly (codes in {0,1}, L1 == Hamming)."""
    L = 2 ** bits
    cols = []
    for c in range(out2d.shape[1]):
        col = out2d[:, c].astype(float)
        qs = np.quantile(col, np.linspace(0, 1, L + 1)[1:-1]) if L > 1 else np.array([np.median(col)])
        # bin index in [0, L-1] via how many thresholds the value exceeds
        code = np.sum(col[:, None] > qs[None, :], axis=1).astype(np.int32)
        cols.append(code)
    return np.stack(cols, axis=1)  # (n_anchors, n_features) integer codes in [0, L-1]

def margin_pairs(codes):
    """return within / between L1-distance lists over the 25-anchor concept-major layout."""
    n = codes.shape[0]
    concept = np.array([r // N_LANGS for r in range(n)])
    within, between = [], []
    for i in range(n):
        for j in range(i + 1, n):
            d = int(np.sum(np.abs(codes[i].astype(int) - codes[j].astype(int))))
            (within if concept[i] == concept[j] else between).append(d)
    return np.array(within, float), np.array(between, float)

def bootstrap_lift_ci(cw, cb, fw, fb, n_boot=N_BOOT, seed=12345):
    """lift = (between-within)_composed - (between-within)_frozen, bootstrapped over pair sets."""
    rng = np.random.default_rng(seed)
    lifts = []
    for _ in range(n_boot):
        cwm = cw[rng.integers(0, len(cw), len(cw))].mean()
        cbm = cb[rng.integers(0, len(cb), len(cb))].mean()
        fwm = fw[rng.integers(0, len(fw), len(fw))].mean()
        fbm = fb[rng.integers(0, len(fb), len(fb))].mean()
        lifts.append((cbm - cwm) - (fbm - fwm))
    lifts = np.array(lifts)
    return float(np.percentile(lifts, 2.5)), float(np.percentile(lifts, 97.5)), float(lifts.mean())

devs = akida.devices()
if not devs:
    raise RuntimeError("OPEN-BLOCKED (g63): no akida HW device on pi5-akida — NO SW fallback")
DEV = devs[0]
count, recs = read_limen(os.path.join(CORPUS, INPUT_NAME + ".limen"))
X0 = np.stack([encode_spikes(p) for (_, p) in recs]).astype(np.uint8).reshape(count, 1, 1, INC)
INPUT_SHA = h(X0)
print("[ha2] akida %s device %s ip %s seed=%d input_sha=%s"
      % (akida.__version__, DEV.version, DEV.ip_version, BACKBONE_SEED, INPUT_SHA))

def run_arm_final(N, plastic_deep):
    """Same paged ladder; RETURN the FINAL paged unit's RAW analog forward output (pre-quantize)."""
    X = X0; final_out = None; all_learned = True
    for li in range(N):
        units = UNIT_SCHED[li]; nw = max(1, units // 4)
        do_fit = plastic_deep or (li == 0)
        m = build_fc(INC, units, nw); m.map(DEV)
        pre = get_w(m)
        if do_fit:
            for i in range(X.shape[0]): m.fit(X[i:i+1])
        post = get_w(m)
        out = np.stack([np.array(m.forward(X[i:i+1])).astype(np.int64).ravel()
                        for i in range(X.shape[0])])
        if do_fit and not bool(np.any(post != pre)): all_learned = False
        final_out = out; del m
        if li < N - 1:
            X = binarize_to_inc(out).reshape(count, 1, 1, INC)
    return final_out, all_learned

rungs = []
for N in LADDER_N:
    comp_out, comp_learned = run_arm_final(N, plastic_deep=True)
    froz_out, _ = run_arm_final(N, plastic_deep=False)
    by_bits = {}
    for B in BIT_DEPTHS:
        cc = quantize_bits(comp_out, B); fc = quantize_bits(froz_out, B)
        cw, cb = margin_pairs(cc); fw, fb = margin_pairs(fc)
        lo, hi, mean = bootstrap_lift_ci(cw, cb, fw, fb)
        comp_margin = float(cb.mean() - cw.mean()); froz_margin = float(fb.mean() - fw.mean())
        by_bits[B] = {"composed_margin": comp_margin, "frozen_margin": froz_margin,
                      "lift": comp_margin - froz_margin, "lift_ci95": [lo, hi],
                      "lift_boot_mean": mean, "ci_lo_gt0": bool(lo > 0)}
        print("[ha2] N=%d %d-bit: lift=%+.4f CI95=[%+.4f,%+.4f] ci_lo>0=%s"
              % (N, B, comp_margin - froz_margin, lo, hi, lo > 0))
    rungs.append({"N": N, "composed_all_learned_hw": bool(comp_learned), "by_bits": by_bits})
    with open(os.path.join(OUT, "result_ha2_quantization.json"), "w") as f:
        json.dump({"hypothesis": "H-A2-QUANTIZATION-FLOOR", "partial": True, "rungs": rungs}, f, indent=2)

# ---- verdict: does multi-bit recover a CI_lo>0 lift that 1-bit misses? ----
def any_bit_pos(rung, bits_set):
    return any(rung["by_bits"][B]["ci_lo_gt0"] for B in bits_set if B in rung["by_bits"])
onebit_pos = any(r["by_bits"][1]["ci_lo_gt0"] for r in rungs)
multibit_pos = any(any_bit_pos(r, [2, 3, 4]) for r in rungs)
ha2_true = multibit_pos and not onebit_pos
verdict = ("H-A2-TRUE (quantization-floor: multi-bit recovers a CI_lo>0 lift the 1-bit readout hides)"
           if ha2_true else
           ("H-A2-FALSIFIED (multi-bit lift also straddles 0 — not a quantization artifact)"
            if not multibit_pos else
            "H-A2-INCONCLUSIVE (1-bit already CI_lo>0 — no quantization gap to recover)"))

res = {
    "hypothesis": "H-A2-QUANTIZATION-FLOOR",
    "ties": ["F-CLM-ONCHIP-LAYERPAGE-LADDER", "a_scale_honest_scope", "H_904"],
    "method": ("FIXED 25 anchors + FIXED backbone seed + IDENTICAL on-chip paged ladder N{2,3,4,5}; "
               "ONLY the host readout quantization of the final paged unit's analog forward output "
               "varies: 1/2/3/4-bit per-feature quantile codes, L1 concept-margin (1-bit==Hamming). "
               "lift = composed - frozen; 95%% bootstrap CI over the pair sets (n_boot=%d)." % N_BOOT),
    "akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "backbone_seed": BACKBONE_SEED, "backbone_int4_sha256": BACKBONE_SHA,
    "input": INPUT_NAME, "input_sha": INPUT_SHA, "anchor_count": count,
    "bit_depths": BIT_DEPTHS, "n_boot": N_BOOT, "rungs": rungs,
    "onebit_any_ci_lo_gt0": onebit_pos, "multibit_any_ci_lo_gt0": multibit_pos,
    "ha2_true": ha2_true, "verdict": verdict,
}
with open(os.path.join(OUT, "result_ha2_quantization.json"), "w") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
print("\n[ha2] VERDICT %s" % verdict)
print("[ha2] wrote " + os.path.join(OUT, "result_ha2_quantization.json"))
