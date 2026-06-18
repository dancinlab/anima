#!/usr/bin/env python3
"""Lane A CAUSE-AXIS battery on live AKD1000. PROBE 1 (encoding) + 2 (objective/readout) + 3 (timing).
a_akida_native_train: every chip tier from REAL chip stdout. NO sw fallback. g63 honest.

Shared metric matches onchip_layerpage_ladder.py:concept_margin
  signal = mean_between_concept_Hamming - mean_within_concept_Hamming (bits) on per-feature-median binarized fwd.
For lift CI we use the chip's own stochastic plasticity (H_904): N paired trials, per-trial shared chip init,
treatment vs control under the SAME per-trial init; ci_lo = mean_lift - 1.96*SEM over trials.
PASS/REOPEN iff ci_lo>0 at >=1 rung; else lift<=0 hardens the closed-negative.
"""
import os, json, struct, hashlib, time
import numpy as np
import akida
from akida import Model, InputData, FullyConnected, AkidaUnsupervised

CORPUS = os.path.expanduser("~/clm_kosmos_akida/corpus")
OUT = os.path.expanduser("~/clm_kosmos_akida/out"); os.makedirs(OUT, exist_ok=True)
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
INC = 256
INPUT_NAME = "parallel"      # concept-major: row = concept*5 + lang
N_LANGS = 5
NTRIALS = 8                   # paired chip trials for the lift CI (stochastic init, H_904)
UNITS, NW, LCOMP = 32, 8, 0.1

def read_limen(path):
    blob = open(path, "rb").read(); assert blob[:8] == LIMEN_MAGIC
    off = 8; struct.unpack_from("<I", blob, off)[0]; off += 4
    count = struct.unpack_from("<I", blob, off)[0]; off += 4
    recs = []
    for _ in range(count):
        rlen = struct.unpack_from("<I", blob, off)[0]; off += 4
        rec = blob[off:off+rlen]; off += rlen
        hlen = struct.unpack_from("<I", rec, 0)[0]
        head = json.loads(rec[4:4+hlen].decode()); recs.append((head, rec[4+hlen:]))
    return count, recs

# ---- per-anchor byte histogram (the raw linguistic feature, pre-projection) ----
def byte_hist(payload):
    pres = np.zeros(INC, dtype=np.float64)
    for b in payload: pres[b] += 1.0
    return pres

# ---- ENCODERS (each maps a count×256 histogram matrix -> count×256 binary chip input) ----
def enc_random_int4(H, seed=20260602):
    rng = np.random.default_rng(seed)
    BB = rng.integers(-7, 8, size=(INC, INC), dtype=np.int8).astype(np.int32)
    proj = H.astype(np.int32) @ BB.T            # count×256
    return (proj > np.median(proj, axis=1, keepdims=True)).astype(np.uint8), "random_int4"

def enc_svd_structured(H):
    # structured linguistic encoder: SVD of the anchor histogram matrix -> int4-quantized loading projection
    Hc = H - H.mean(axis=0, keepdims=True)
    U, S, Vt = np.linalg.svd(Hc, full_matrices=False)   # Vt: k×256 structured axes
    k = Vt.shape[0]
    P = np.zeros((INC, INC))
    P[:k, :] = Vt                                        # rows = structured axes
    # int4 quantize the structured projection so chip input space sees a STRUCTURED (not random) basis
    scale = 7.0 / (np.max(np.abs(P)) + 1e-12)
    Pq = np.clip(np.round(P * scale), -7, 7).astype(np.int32)
    proj = H.astype(np.int32) @ Pq.T
    return (proj > np.median(proj, axis=1, keepdims=True)).astype(np.uint8), "svd_structured"

def enc_whitened(H):
    # covariance-whitened structured encoder
    Hc = H - H.mean(axis=0, keepdims=True)
    cov = (Hc.T @ Hc) / max(1, Hc.shape[0]-1) + 1e-3*np.eye(INC)
    w, V = np.linalg.eigh(cov)
    W = V @ np.diag(1.0/np.sqrt(np.maximum(w,1e-9))) @ V.T   # 256×256 whitening
    P = W
    scale = 7.0 / (np.max(np.abs(P)) + 1e-12)
    Pq = np.clip(np.round(P*scale), -7, 7).astype(np.int32)
    proj = H.astype(np.int32) @ Pq.T
    return (proj > np.median(proj, axis=1, keepdims=True)).astype(np.uint8), "whitened_structured"

def build_fc(wbits):
    m = Model()
    m.add(InputData(name="input", input_shape=(1,1,INC), input_bits=1))
    m.add(FullyConnected(name="fc", units=UNITS, weights_bits=wbits, activation=False))
    m.compile(AkidaUnsupervised(num_weights=NW, learning_competition=LCOMP))
    return m
def get_w(m): return np.array(m.get_layer("fc").variables["weights"])
def set_w(m, w): m.get_layer("fc").variables["weights"] = w.copy()

def concept_margin_from_binary(fb):
    n = fb.shape[0]; concept = np.array([r // N_LANGS for r in range(n)])
    within, between = [], []
    for i in range(n):
        for j in range(i+1, n):
            d = int(np.count_nonzero(fb[i] != fb[j]))
            (within if concept[i]==concept[j] else between).append(d)
    return (float(np.mean(between)) - float(np.mean(within)))

def margin_post1bit(out2d):
    fb = (out2d > np.median(out2d, axis=0, keepdims=True)).astype(np.uint8)
    return concept_margin_from_binary(fb)

def margin_analog(out2d):
    # PRE-binarization: concept margin in the int-valued forward space via L1 distance, sign matched to bits
    n = out2d.shape[0]; concept = np.array([r // N_LANGS for r in range(n)])
    within, between = [], []
    for i in range(n):
        for j in range(i+1, n):
            d = float(np.sum(np.abs(out2d[i].astype(np.float64) - out2d[j].astype(np.float64))))
            (within if concept[i]==concept[j] else between).append(d)
    return (float(np.mean(between)) - float(np.mean(within)))

# ---- live device gate ----
devs = akida.devices()
if not devs:
    raise RuntimeError("OPEN-BLOCKED (g63): no akida HW device on pi5-akida — NO SW fallback")
DEV = devs[0]
count, recs = read_limen(os.path.join(CORPUS, INPUT_NAME + ".limen"))
H = np.stack([byte_hist(p) for (_, p) in recs])     # 25×256 raw linguistic histograms
print("[cause] akida %s device %s ip %s  N=%d trials  units=%d" % (akida.__version__, DEV.version, DEV.ip_version, NTRIALS, UNITS))

# pre-encode all encoders ONCE (deterministic given H)
Xrand, _ = enc_random_int4(H)
Xsvd, _  = enc_svd_structured(H)
Xwhite, _= enc_whitened(H)
def to_chip(Xb): return Xb.astype(np.uint8).reshape(count,1,1,INC)
ENCS = {"random_int4": to_chip(Xrand), "svd_structured": to_chip(Xsvd), "whitened_structured": to_chip(Xwhite)}

def fit_forward(X, init_w, wbits):
    m = build_fc(wbits); set_w(m, init_w); m.map(DEV); set_w(m, init_w)
    pre = get_w(m)
    for i in range(X.shape[0]): m.fit(X[i:i+1])
    post = get_w(m)
    out = np.stack([np.array(m.forward(X[i:i+1])).astype(np.float64).ravel() for i in range(X.shape[0])])
    learned = bool(np.any(post != pre))
    del m
    return out, learned

def paired_lift(treat_X, ctrl_X, wbits_t=1, wbits_c=1, margin_fn=margin_post1bit, label=""):
    """N paired chip trials: lift = margin(treat) - margin(ctrl). When weight-bits match, the pair shares the
    SAME per-trial init (paired control of chip stochastic init, H_904). When bits differ the per-arm chip init
    is its own native init (shapes/precision differ) — still paired by trial index. returns dict."""
    lifts, tms, cms, learn_all = [], [], [], True
    same_bits = (wbits_t == wbits_c)
    for t in range(NTRIALS):
        init_t = get_w(build_fc(wbits_t))
        init_c = init_t.copy() if same_bits else get_w(build_fc(wbits_c))
        to, lt = fit_forward(treat_X, init_t, wbits_t)
        co, lc = fit_forward(ctrl_X,  init_c, wbits_c)
        tm, cm = margin_fn(to), margin_fn(co)
        lifts.append(tm - cm); tms.append(tm); cms.append(cm)
        learn_all = learn_all and lt and lc
        print("[cause] %-32s trial %d: treat=%.4f ctrl=%.4f lift=%+.4f learn=%s" % (label, t, tm, cm, tm-cm, lt and lc))
    lifts = np.array(lifts); mean = float(lifts.mean()); sd = float(lifts.std(ddof=1))
    sem = sd/np.sqrt(len(lifts)); ci_lo, ci_hi = mean-1.96*sem, mean+1.96*sem
    npos = int((lifts>0).sum())
    reopen = bool(learn_all and ci_lo > 0)
    return {"label": label, "n_trials": len(lifts), "lifts": lifts.tolist(),
            "treat_margins": tms, "ctrl_margins": cms,
            "mean_lift": mean, "sd": sd, "sem": sem, "ci95": [ci_lo, ci_hi],
            "n_positive": npos, "learn_all_hw": learn_all, "ci_lo": ci_lo,
            "REOPEN": reopen}

RESULTS = {"akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
           "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_trials": NTRIALS,
           "metric": "between-minus-within concept Hamming margin (bits); lift=treat-ctrl; ci_lo=mean-1.96SEM over chip trials",
           "probes": {}}

# ===================== PROBE 1 — INPUT ENCODING =====================
print("\n[cause] ========== PROBE 1 — INPUT ENCODING ==========")
p1 = {}
p1["svd_structured_vs_random"]   = paired_lift(ENCS["svd_structured"],   ENCS["random_int4"], label="P1 svd_vs_random")
json.dump(RESULTS|{"probes":{"P1_encoding":p1}}, open(os.path.join(OUT,"result_causeaxis.json"),"w"), indent=2)  # commit-early
p1["whitened_structured_vs_random"] = paired_lift(ENCS["whitened_structured"], ENCS["random_int4"], label="P1 whitened_vs_random")
p1["any_reopen"] = bool(p1["svd_structured_vs_random"]["REOPEN"] or p1["whitened_structured_vs_random"]["REOPEN"])
RESULTS["probes"]["P1_encoding"] = p1
json.dump(RESULTS, open(os.path.join(OUT,"result_causeaxis.json"),"w"), indent=2)

# ===================== PROBE 2 — OBJECTIVE + READOUT-LOCUS =====================
print("\n[cause] ========== PROBE 2 — OBJECTIVE + READOUT ==========")
p2 = {}
# (a) 4-bit weights vs 1-bit, BOTH on random encoder (isolate weight precision). treat=4bit ctrl=1bit
try:
    p2["a_4bit_vs_1bit"] = paired_lift(ENCS["random_int4"], ENCS["random_int4"], wbits_t=4, wbits_c=1, label="P2a 4bit_vs_1bit")
except Exception as e:
    p2["a_4bit_vs_1bit"] = {"error": repr(e), "REOPEN": False}
    print("[cause] P2a 4bit error:", repr(e))
# (b) supervised vs unsupervised — SDK probe
learn_classes = [x for x in dir(akida) if ("upervis" in x or "earn" in x.lower())]
has_supervised = any("Supervised" in x for x in learn_classes)
p2["b_supervised"] = {"sdk_learning_classes": learn_classes, "AkidaSupervisedLearning_present": has_supervised,
                      "status": "N/A-SDK: akida %s exposes ONLY %s — no supervised learning class to test (honest, not fabricated)" % (akida.__version__, learn_classes) if not has_supervised else "present",
                      "REOPEN": False}
print("[cause] P2b supervised:", p2["b_supervised"]["status"])
# (c) pre-binarization analog margin vs post-1bit. Same chip fits, two readouts.
print("[cause] P2c analog vs post-1bit readout (same chip fwd, two margin fns)")
analog_lifts, learn_all = [], True
for t in range(NTRIALS):
    init_w = get_w(build_fc(1))
    out, lh = fit_forward(ENCS["random_int4"], init_w, 1)
    m_analog = margin_analog(out); m_post = margin_post1bit(out)
    analog_lifts.append(m_analog - m_post)
    learn_all = learn_all and lh
    print("[cause] P2c trial %d: analog_margin=%.3f post1bit_margin=%.4f (analog space is L1, scale differs)" % (t, m_analog, m_post))
# For (c) the falsifier is whether the ANALOG margin itself is >0 where post-1bit was <=0 (sign of cross-lingual structure pre-binarize)
analog_abs = []
for t in range(NTRIALS):
    init_w = get_w(build_fc(1)); out,_ = fit_forward(ENCS["random_int4"], init_w, 1)
    analog_abs.append(margin_analog(out))
analog_abs = np.array(analog_abs); a_mean=float(analog_abs.mean()); a_sem=float(analog_abs.std(ddof=1)/np.sqrt(len(analog_abs)))
a_ci_lo = a_mean - 1.96*a_sem
p2["c_analog_readout"] = {"analog_margins": analog_abs.tolist(), "mean": a_mean, "sem": a_sem, "ci_lo": a_ci_lo,
                          "note": "analog (pre-1bit) L1 concept margin; >0 means cross-lingual structure exists pre-binarize",
                          "learn_all_hw": learn_all, "REOPEN": bool(learn_all and a_ci_lo > 0)}
print("[cause] P2c analog margin mean=%.3f ci_lo=%.3f REOPEN=%s" % (a_mean, a_ci_lo, p2["c_analog_readout"]["REOPEN"]))
p2["any_reopen"] = bool(p2["a_4bit_vs_1bit"].get("REOPEN") or p2["b_supervised"]["REOPEN"] or p2["c_analog_readout"]["REOPEN"])
RESULTS["probes"]["P2_objective_readout"] = p2
json.dump(RESULTS, open(os.path.join(OUT,"result_causeaxis.json"),"w"), indent=2)

# ===================== PROBE 3 — TEMPORAL CODE / SPIKE TIMING =====================
print("\n[cause] ========== PROBE 3 — TEMPORAL CODE ==========")
p3 = {}
# attempt spike-event capture
spike_api = [x for x in dir(akida) if "spike" in x.lower() or "event" in x.lower()]
model_methods = []
try:
    mm = build_fc(1); mm.map(DEV)
    model_methods = [x for x in dir(mm) if "spike" in x.lower() or "event" in x.lower() or "predict_class" in x.lower()]
    del mm
except Exception as e:
    model_methods = ["err:"+repr(e)]
p3["spike_capture_api"] = {"akida_spike_symbols": spike_api, "model_spike_methods": model_methods}
print("[cause] P3 spike API: akida=%s model=%s" % (spike_api, model_methods))
# Highest-resolution temporal proxy the chip exposes: per-unit activation-RANK order across the 25-anchor
# sequence (rate-resolution temporal proxy — NOT fabricated spike timing). Timing-aware margin = whether
# same-concept anchors share per-unit rank-order more than different-concept (Spearman on per-unit ranks).
def _rankdata(a):
    # average-rank (ties) without scipy
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), dtype=np.float64)
    ranks[order] = np.arange(1, len(a)+1)
    # average tied ranks
    a_sorted = a[order]
    i = 0
    while i < len(a):
        j = i
        while j+1 < len(a) and a_sorted[j+1] == a_sorted[i]:
            j += 1
        if j > i:
            avg = (ranks[order[i]] + ranks[order[j]]) / 2.0
            for k in range(i, j+1): ranks[order[k]] = avg
        i = j+1
    return ranks
def timing_proxy_margin(out2d):
    # rank each anchor's per-unit activation vector; same concept should have correlated rank profiles
    R = np.stack([_rankdata(out2d[i]) for i in range(out2d.shape[0])])  # 25×units rank profiles
    n = R.shape[0]; concept = np.array([r//N_LANGS for r in range(n)])
    def spear(a,b):
        ra,rb = a - a.mean(), b - b.mean()
        d = np.linalg.norm(ra)*np.linalg.norm(rb)
        return 0.0 if d==0 else float(ra@rb/d)
    within, between = [], []
    for i in range(n):
        for j in range(i+1,n):
            s = spear(R[i],R[j])
            (within if concept[i]==concept[j] else between).append(s)
    # timing margin: within-concept rank-corr MINUS between (higher=concept structure in timing/rank order)
    return float(np.mean(within)) - float(np.mean(between))
have_scipy = True  # rank computed numpy-only (no scipy dependency)
timing_lifts, learn_all = [], True
if have_scipy:
    for t in range(NTRIALS):
        init_w = get_w(build_fc(1)); out, lh = fit_forward(ENCS["random_int4"], init_w, 1)
        tm = timing_proxy_margin(out); timing_lifts.append(tm); learn_all = learn_all and lh
        print("[cause] P3 trial %d: timing_proxy_margin(within-between rankcorr)=%+.4f" % (t, tm))
    tl = np.array(timing_lifts); t_mean=float(tl.mean()); t_sem=float(tl.std(ddof=1)/np.sqrt(len(tl)))
    t_ci_lo = t_mean - 1.96*t_sem
    p3["timing_proxy"] = {"kind":"per-unit activation-RANK-order Spearman (within-minus-between concept); rate-resolution temporal proxy, NOT spike-timing",
                          "margins": tl.tolist(), "mean": t_mean, "sem": t_sem, "ci_lo": t_ci_lo,
                          "learn_all_hw": learn_all, "REOPEN": bool(learn_all and t_ci_lo > 0)}
    print("[cause] P3 timing-proxy margin mean=%+.4f ci_lo=%+.4f REOPEN=%s" % (t_mean, t_ci_lo, p3["timing_proxy"]["REOPEN"]))
else:
    p3["timing_proxy"] = {"status":"scipy unavailable on host; timing-proxy recomputed CPU-local from raw fwd", "REOPEN": None}
    print("[cause] P3 scipy unavailable -> timing-proxy deferred to CPU-local raw.npz re-score")
p3["spike_timing_available"] = bool(spike_api) and any("spike" in m.lower() for m in model_methods)
p3["any_reopen"] = bool(p3.get("timing_proxy",{}).get("REOPEN"))
RESULTS["probes"]["P3_temporal"] = p3
json.dump(RESULTS, open(os.path.join(OUT,"result_causeaxis.json"),"w"), indent=2)

# ---- overall disposition ----
any_reopen = bool(p1.get("any_reopen") or p2.get("any_reopen") or p3.get("any_reopen"))
RESULTS["disposition"] = "REOPENED" if any_reopen else "HARDENED-CLOSED-NEGATIVE"
RESULTS["disposition_reason"] = ("at least one cause-axis lift ci_lo>0 on chip -> Lane A P3 REOPENS" if any_reopen
    else "encoding + objective + 4bit + analog-readout + timing-proxy ALL ci_lo<=0 on live AKD1000 -> closed-negative HARDENS to cover the 4 cause-axes (8 axes total)")
json.dump(RESULTS, open(os.path.join(OUT,"result_causeaxis.json"),"w"), indent=2)
print("\n[cause] ========== DISPOSITION ==========")
print("[cause] P1 encoding any_reopen=%s | P2 objective any_reopen=%s | P3 timing any_reopen=%s" % (p1.get("any_reopen"), p2.get("any_reopen"), p3.get("any_reopen")))
print("[cause] DISPOSITION: %s" % RESULTS["disposition"])
print("[cause] %s" % RESULTS["disposition_reason"])
print("[cause] wrote " + os.path.join(OUT,"result_causeaxis.json"))
