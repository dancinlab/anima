#!/usr/bin/env python3
"""H-A3 — PLASTICITY-DEPTH diagnostic (Lane A weak-lift).

Is the weak lift limited by HOW MANY paged units learn on chip, not by corpus? The prior ladder's
"composed" arm fits EVERY paged unit and "frozen_head" fits only L1 — that contrast measures whether
deep plasticity helps at all relative to a fully-frozen tail. H-A3 asks a sharper, depth-resolved
question at FIXED N: does making the LAST TWO paged units plastic buy lift OVER making only the LAST
FC plastic?

Three arms at each rung N (identical paged pipeline, live AKD1000, same fixed backbone seed):
  - frozen_tail : only L1 fits on chip; L2..LN forward-only            (baseline, = prior frozen_head)
  - last_fc     : L1 fits AND the FINAL paged unit LN fits; middle units forward-only  (1-layer plastic tail)
  - two_layer   : L1 fits AND the final TWO paged units L(N-1),LN fit; rest forward-only (2-layer plastic tail)
lift_lastfc  = margin(last_fc)  - margin(frozen_tail)
lift_twolayer = margin(two_layer) - margin(frozen_tail)
depth_gain   = lift_twolayer - lift_lastfc   (does the SECOND plastic layer add lift?)

FALSIFIER (pre-registered):
  H-A3 TRUE  iff  two_layer adds lift over last_fc (depth_gain > 0 on >=1 rung, consistent sign)
                 -> depth-of-plasticity is a bottleneck (more plastic layers buy representational lift).
  H-A3 FALSE iff  no gain (depth_gain ~ 0 or sign-inconsistent) -> plasticity-depth is NOT the cause.

Only N in {3,4,5} carry a meaningful "two-layer tail vs one-layer tail" distinction (N=2 last_fc ==
two_layer == composed). g63 honest: live AKD1000 ONLY, no SW/CPU fallback; one FC resident at a time.
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
LADDER_N = [3, 4, 5]            # N=2 has no 2-layer-vs-1-layer-tail distinction
N_CONCEPTS, N_LANGS = 5, 5
BACKBONE_SEED = 20260602

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
    return bm - wm

devs = akida.devices()
if not devs:
    raise RuntimeError("OPEN-BLOCKED (g63): no akida HW device on pi5-akida — NO SW fallback")
DEV = devs[0]
count, recs = read_limen(os.path.join(CORPUS, INPUT_NAME + ".limen"))
X0 = np.stack([encode_spikes(p) for (_, p) in recs]).astype(np.uint8).reshape(count, 1, 1, INC)
INPUT_SHA = h(X0)
print("[ha3] akida %s device %s ip %s seed=%d input_sha=%s"
      % (akida.__version__, DEV.version, DEV.ip_version, BACKBONE_SEED, INPUT_SHA))

def run_arm(N, fit_set):
    """fit_set = set of 0-indexed layer indices that fit on chip (the rest forward-only)."""
    X = X0; final_out = None; all_learned = True
    for li in range(N):
        units = UNIT_SCHED[li]; nw = max(1, units // 4)
        do_fit = li in fit_set
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
    return concept_margin(final_out), all_learned

rungs = []
for N in LADDER_N:
    frozen_set = {0}                       # only L1
    lastfc_set = {0, N - 1}                # L1 + final unit
    twolayer_set = {0, N - 2, N - 1}       # L1 + final TWO units
    m_frozen, l_f = run_arm(N, frozen_set)
    m_lastfc, l_l = run_arm(N, lastfc_set)
    m_two,    l_t = run_arm(N, twolayer_set)
    lift_lastfc = m_lastfc - m_frozen
    lift_twolayer = m_two - m_frozen
    depth_gain = lift_twolayer - lift_lastfc
    rung = {"N": N, "frozen_margin": m_frozen, "lastfc_margin": m_lastfc, "twolayer_margin": m_two,
            "lift_lastfc": lift_lastfc, "lift_twolayer": lift_twolayer, "depth_gain": depth_gain,
            "all_learned_hw": bool(l_f and l_l and l_t)}
    rungs.append(rung)
    print("[ha3] N=%d frozen=%.4f lastfc=%.4f two=%.4f | lift_lastfc=%+.4f lift_two=%+.4f DEPTH_GAIN=%+.4f"
          % (N, m_frozen, m_lastfc, m_two, lift_lastfc, lift_twolayer, depth_gain))
    with open(os.path.join(OUT, "result_ha3_plasticity_depth.json"), "w") as f:
        json.dump({"hypothesis": "H-A3-PLASTICITY-DEPTH", "partial": True, "rungs": rungs}, f, indent=2)

gains = np.array([r["depth_gain"] for r in rungs], dtype=float)
n_pos = int(np.sum(gains > 0)); n_neg = int(np.sum(gains < 0))
sign_consistent = (n_pos == len(gains)) or (n_neg == len(gains))
ha3_true = bool((gains > 0).any() and sign_consistent and gains.mean() > 0)
verdict = ("H-A3-TRUE (depth-of-plasticity bottleneck: the 2nd plastic layer adds lift, gain>0 consistent)"
           if ha3_true else
           "H-A3-FALSIFIED (2-layer plastic adds no consistent lift over last-FC — depth not the cause)")

res = {
    "hypothesis": "H-A3-PLASTICITY-DEPTH",
    "ties": ["F-CLM-ONCHIP-LAYERPAGE-LADDER", "a_scale_honest_scope", "H_904", "a_akida_native_train"],
    "method": ("FIXED 25 anchors + FIXED backbone seed; 3 arms/rung N{3,4,5} on live AKD1000: "
               "frozen_tail (L1 only), last_fc (L1+final unit), two_layer (L1+final two units). "
               "lift vs frozen_tail; depth_gain = lift_twolayer - lift_lastfc. one FC resident at a time."),
    "akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "backbone_seed": BACKBONE_SEED, "backbone_int4_sha256": BACKBONE_SHA,
    "input": INPUT_NAME, "input_sha": INPUT_SHA, "anchor_count": count,
    "ladder_N": LADDER_N, "rungs": rungs,
    "depth_gains": gains.tolist(), "n_pos": n_pos, "n_neg": n_neg,
    "mean_depth_gain": float(gains.mean()), "sign_consistent": sign_consistent,
    "ha3_true": ha3_true, "verdict": verdict,
}
with open(os.path.join(OUT, "result_ha3_plasticity_depth.json"), "w") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
print("\n[ha3] depth_gains=%s mean=%+.4f n_pos=%d n_neg=%d sign_consistent=%s"
      % (gains.tolist(), gains.mean(), n_pos, n_neg, sign_consistent))
print("[ha3] VERDICT %s" % verdict)
print("[ha3] wrote " + os.path.join(OUT, "result_ha3_plasticity_depth.json"))
