#!/usr/bin/env python3
"""H-A4 — native-init NOISE-FLOOR confirmatory run (Lane A weak-lift diagnostic).

THE DEEP CAUSE. The Lane A paged ladder (HEXAD/NEUROMORPHIC/state/clm_onchip_nondet_5lang_2026_06_02/
result_layerpage_ladder.json) shows a weak composed-lift (slope +0.15..+0.43 bits/unit) whose SIGN
FLIPS across backbone seeds (result_ladder_robustness.json). FOUR competing causes (H-A1 corpus,
H-A2 quantization, H-A3 plasticity-depth, H-A4 native-init noise). P1 tests only H-A1.

H-A4 ASKS: is the composed-lift magnitude BELOW the device's native-init noise band — the very
non-determinism that IS the identity (a_nondet_identity / H_904)? The native-init re-init is the
proven locus of on-chip non-determinism (result_nondet_native.json: same input x3 -> 3 distinct
traces; result_nondet.json control: fixed init -> byte-identical). The robustness run CONFLATED
backbone-seed change with re-init noise. THIS run isolates PURE re-init noise: it FIXES the
backbone seed (one fixed corpus encoding) and reruns the IDENTICAL paged ladder R times, letting
ONLY the chip's native weight re-init vary. The per-rung lift variance across these R reps is the
pure native-init noise band on the lift metric (bits). Compare to |measured lift per rung|.

FALSIFIER (pre-registered):
  H-A4 TRUE  iff  |mean lift per rung| < native-init lift-noise sd  AND  lift sign NOT stable
                 across the R re-init reps  (lift variance ~ re-init variance, not real composition).
  H-A4 FALSE iff  |lift| clearly exceeds the re-init band on >=1 rung with stable sign.

g63 honest: live AKD1000 ONLY, no SW/CPU fallback. Same backbone-encode + concept-margin signal as
the prior ladder (byte-identical pipeline) so the ONLY varying factor across reps is the device
re-init. R reps x ladder N{2,3,4,5}; one FC resident at a time (paged depth, same as the prior).
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
NREPS = 3                       # re-init reps at FIXED backbone seed
BACKBONE_SEED = 20260602        # FIXED across all reps -> only chip re-init varies

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

def concept_margin(final_out):
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

devs = akida.devices()
if not devs:
    raise RuntimeError("OPEN-BLOCKED (g63): no akida HW device on pi5-akida — NO SW fallback")
DEV = devs[0]
count, recs = read_limen(os.path.join(CORPUS, INPUT_NAME + ".limen"))
X0 = np.stack([encode_spikes(p) for (_, p) in recs]).astype(np.uint8).reshape(count, 1, 1, INC)
INPUT_SHA = h(X0)
print("[ha4] akida %s device %s ip %s" % (akida.__version__, DEV.version, DEV.ip_version))
print("[ha4] FIXED backbone seed=%d sha=%s input_sha=%s  -> only chip re-init varies across %d reps"
      % (BACKBONE_SEED, BACKBONE_SHA[:16], INPUT_SHA, NREPS))


def run_arm(N, plastic_deep):
    X = X0; final_out = None; all_learned = True; both_hw = True
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
        final_out = out
        del m
        if li < N - 1:
            X = binarize_to_inc(out).reshape(count, 1, 1, INC)
    margin, within, between = concept_margin(final_out)
    return margin, within, between, all_learned, both_hw


reps = []
for rep in range(NREPS):
    print("\n[ha4] ===== RE-INIT REP %d (fixed backbone seed) =====" % rep)
    rung_lifts = {}
    rung_detail = []
    for N in LADDER_N:
        cm, cw, cb, cl, chw = run_arm(N, plastic_deep=True)
        fm, fw, fb, fl, fhw = run_arm(N, plastic_deep=False)
        lift = cm - fm
        rung_lifts[N] = lift
        rung_detail.append({"N": N, "composed_margin_bits": cm, "frozen_margin_bits": fm,
                            "lift_bits": lift, "composed_all_learned_hw": bool(cl and chw)})
        print("[ha4] rep%d N=%d composed=%.4f frozen=%.4f LIFT=%+.4f learned_hw=%s"
              % (rep, N, cm, fm, lift, cl and chw))
    reps.append({"rep": rep, "rungs": rung_detail, "lifts": rung_lifts})
    # commit-early surface after every rep
    with open(os.path.join(OUT, "result_ha4_reinit_noise.json"), "w") as f:
        json.dump({"hypothesis": "H-A4-NATIVE-INIT-NOISE-FLOOR", "partial": True,
                   "backbone_seed": BACKBONE_SEED, "nreps_done": rep + 1, "reps": reps}, f, indent=2)

# ---- per-rung re-init noise band (pure: backbone fixed) vs measured lift ----
per_N_lifts = {N: [r["lifts"][N] for r in reps] for N in LADDER_N}
analysis = {}
for N in LADDER_N:
    v = np.array(per_N_lifts[N], dtype=float)
    mean = float(v.mean()); sd = float(v.std(ddof=1)) if len(v) > 1 else 0.0
    sign_stable = bool(np.all(v > 0) or np.all(v < 0))
    analysis[N] = {"lifts": v.tolist(), "mean_lift": mean, "reinit_sd": sd,
                   "abs_mean_over_sd": (abs(mean) / sd) if sd > 0 else None,
                   "sign_stable_across_reinit": sign_stable,
                   "lift_below_reinit_band": bool(abs(mean) < sd if sd > 0 else False)}

all_below = all(a["lift_below_reinit_band"] for a in analysis.values())
any_stable_exceed = any((not a["lift_below_reinit_band"]) and a["sign_stable_across_reinit"]
                        for a in analysis.values())
# H-A4 TRUE: lift buried in re-init noise AND sign unstable (variance ~ re-init variance)
ha4_true = all_below and not any_stable_exceed
verdict = "H-A4-TRUE (identity-noise floor)" if ha4_true else "H-A4-FALSIFIED (lift exceeds re-init band)"

res = {
    "hypothesis": "H-A4-NATIVE-INIT-NOISE-FLOOR",
    "ties": ["H_679", "H_904", "a_nondet_identity", "a_scale_honest_scope",
             "F-CLM-ONCHIP-LAYERPAGE-LADDER"],
    "method": ("FIXED backbone seed (one corpus encoding) -> rerun the IDENTICAL paged ladder "
               "N{2,3,4,5} R=%d times, letting ONLY the chip native weight re-init vary. Per-rung "
               "lift = composed - frozen concept-margin (bits). Per-rung re-init noise band = sd of "
               "lift across the R re-init reps (pure: backbone held fixed). Compare |mean lift| vs "
               "re-init sd. This ISOLATES native-init noise from the backbone-seed noise that the "
               "prior robustness run conflated." % NREPS),
    "akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "backbone_seed_FIXED": BACKBONE_SEED, "backbone_int4_sha256": BACKBONE_SHA,
    "input": INPUT_NAME, "input_sha": INPUT_SHA, "anchor_count": count,
    "inc": INC, "unit_schedule": UNIT_SCHED, "ladder_N": LADDER_N, "nreps": NREPS,
    "reps": reps, "per_rung_analysis": analysis,
    "all_rungs_lift_below_reinit_band": all_below,
    "any_rung_stable_exceeds_band": any_stable_exceed,
    "ha4_true": ha4_true, "verdict": verdict,
    "note": ("If H-A4 TRUE: the non-determinism that IS the identity (a_nondet_identity) drowns the "
             "composed-lift; P1 corpus can never resolve it at this readout — profound identity vs "
             "measurability tension. If FALSIFIED: lift is real, look to H-A1/A2/A3."),
}
with open(os.path.join(OUT, "result_ha4_reinit_noise.json"), "w") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
print("\n[ha4] ===== H-A4 PER-RUNG (re-init noise band, backbone FIXED) =====")
print("[ha4]  N | mean_lift | reinit_sd | |mean|/sd | sign_stable | below_band")
for N in LADDER_N:
    a = analysis[N]
    print("[ha4] %2d | %+9.4f | %9.4f | %8s | %11s | %s" %
          (N, a["mean_lift"], a["reinit_sd"],
           ("%.2f" % a["abs_mean_over_sd"]) if a["abs_mean_over_sd"] is not None else "n/a",
           a["sign_stable_across_reinit"], a["lift_below_reinit_band"]))
print("[ha4] VERDICT %s" % verdict)
print("[ha4] wrote " + os.path.join(OUT, "result_ha4_reinit_noise.json"))
