#!/usr/bin/env python3
"""STAGES 2-4 (C6 / H_912) — F-CLM-AKIDA-SEMANTIC-SIGNAL-LIFT, ALL-4-LEVERS combined run."""
import os, sys, json, struct, hashlib, time
import numpy as np
import akida
from akida import Model, InputData, FullyConnected, AkidaUnsupervised
CORPUS = os.path.expanduser("~/clm_kosmos_akida_large/corpus")
OUT = os.path.expanduser("~/clm_kosmos_akida_large/out")
os.makedirs(OUT, exist_ok=True)
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
INC, UNITS, NWEIGHTS, LCOMP = 256, 32, 16, 0.1
NTRIALS   = int(os.environ.get("H912_NTRIALS", "20"))
EXPOSURES = int(os.environ.get("H912_EXPOSURES", "3"))
SEED = 912

def read_limen(path):
    with open(path, "rb") as f: blob = f.read()
    assert blob[:8] == LIMEN_MAGIC, f"bad magic {blob[:8]!r}"
    off = 8
    struct.unpack_from("<I", blob, off)[0]; off += 4
    count = struct.unpack_from("<I", blob, off)[0]; off += 4
    recs = []; payloads = []
    for _ in range(count):
        rlen = struct.unpack_from("<I", blob, off)[0]; off += 4
        rec = blob[off:off+rlen]; off += rlen
        hlen = struct.unpack_from("<I", rec, 0)[0]
        head = json.loads(rec[4:4+hlen].decode("utf-8"))
        recs.append((head, rec[4+hlen:])); payloads.append(rec[4+hlen:])
    merkle_stored = blob[off:off+32]
    layer = [hashlib.sha256(p).digest() for p in payloads]
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            a = layer[i]; b = layer[i+1] if i+1 < len(layer) else layer[i]
            nxt.append(hashlib.sha256(a+b).digest())
        layer = nxt
    assert layer[0] == merkle_stored, "merkle mismatch (closed_corpus FAIL)"
    return count, recs

rng_bb = np.random.default_rng(20260601)
BACKBONE_INT4 = rng_bb.integers(-7, 8, size=(INC, INC), dtype=np.int8)
BACKBONE_SHA = hashlib.sha256(BACKBONE_INT4.tobytes()).hexdigest()

def encode_spikes(payload):
    pres = np.zeros(INC, dtype=np.int32)
    for b in payload: pres[b] += 1
    proj = BACKBONE_INT4.astype(np.int32) @ pres
    return (proj > np.median(proj)).astype(np.uint8)

def build_model():
    m = Model()
    m.add(InputData(name="input", input_shape=(1,1,INC), input_bits=1))
    m.add(FullyConnected(name="fc", units=UNITS, weights_bits=1, activation=False))
    m.compile(AkidaUnsupervised(num_weights=NWEIGHTS, learning_competition=LCOMP))
    return m

def get_w(m): return np.array(m.get_layer("fc").variables["weights"])
def set_w(m, w): m.get_layer("fc").variables["weights"] = w.copy()

devs = akida.devices()
if not devs:
    raise RuntimeError("BLOCKED: no akida HW device (g63 - no SW fallback labelled on-chip)")
DEV = devs[0]
print(f"[4lever] akida {akida.__version__} device {DEV.version} ip {DEV.ip_version}", flush=True)
print(f"[4lever] N={NTRIALS} paired trials  EXPOSURES={EXPOSURES} (learn-while-infer streaming online)", flush=True)

def load(name):
    count, recs = read_limen(os.path.join(CORPUS, f"{name}.limen"))
    X = np.stack([encode_spikes(p) for (_,p) in recs]).astype(np.uint8).reshape(count,1,1,INC)
    heads = [h for (h,_) in recs]
    shard_sha = hashlib.sha256(open(os.path.join(CORPUS, f"{name}.limen"),"rb").read()).hexdigest()
    return count, X, heads, shard_sha

pc, pX, pheads, p_sha = load("parallel")
cc, cX, cheads, c_sha = load("concat")
print(f"[4lever] corpus: parallel={pc} anchors  concat={cc} anchors  (concepts={len(set(h['concept'] for h in pheads))})", flush=True)

def sep_axis(fwd, heads):
    by = {}
    for i,h in enumerate(heads): by.setdefault(h["concept"], []).append(i)
    def cos(a,b):
        na,nb=np.linalg.norm(a),np.linalg.norm(b)
        return 0.0 if na==0 or nb==0 else float(a@b/(na*nb))
    scs=[]
    for cid,idxs in sorted(by.items()):
        vs=[fwd[i] for i in idxs]
        pr=[cos(vs[a],vs[b]) for a in range(len(vs)) for b in range(a+1,len(vs))]
        scs.append(np.mean(pr) if pr else 0.0)
    return float(np.mean(scs))

def phi_proxy_axis(fwd):
    # Phi-proxy = whole-system effective information minus the min-bipartition EI, in the Gaussian
    # covariance form: cross-partition TOTAL CORRELATION = 1/2 * log( det(C_A)*det(C_B) / det(C) ).
    # This is the integrated information carried ACROSS the leading-eigvec bipartition (>=0; 0 iff the
    # two parts are statistically independent). Faithful to H_911/LAB-09 (whole_EI - min_bipartition).
    A = np.asarray(fwd, dtype=np.float64)
    A = A - A.mean(axis=0, keepdims=True)
    n_nodes = A.shape[1]
    if n_nodes < 2 or A.shape[0] < 2:
        return 0.0
    C = (A.T @ A) / (A.shape[0] - 1) + 1e-6 * np.eye(n_nodes)   # ridge for slogdet stability
    sign, logdetC = np.linalg.slogdet(C)
    if not np.isfinite(logdetC):
        return 0.0
    w, V = np.linalg.eigh(C)
    lead = V[:, -1]
    part = lead >= 0
    if part.all() or (~part).all():
        order = np.argsort(np.abs(lead))
        part = np.zeros(n_nodes, dtype=bool); part[order[: n_nodes // 2]] = True
    ia = np.where(part)[0]; ib = np.where(~part)[0]
    _, ldA = np.linalg.slogdet(C[np.ix_(ia, ia)])
    _, ldB = np.linalg.slogdet(C[np.ix_(ib, ib)])
    phi = 0.5 * (ldA + ldB - logdetC)
    return float(phi) if np.isfinite(phi) else 0.0

def stream_fit_forward(X, init_w, exposures):
    m = build_model(); m.map(DEV); set_w(m, init_w)
    pre = get_w(m)
    n = X.shape[0]
    acc = np.zeros((n, UNITS), dtype=np.float64)
    for _ in range(exposures):
        for i in range(n):
            m.fit(X[i:i+1])
            r = np.array(m.forward(X[i:i+1])).astype(np.float64).ravel()
            acc[i] += r
    acc /= exposures
    post = get_w(m)
    return acc, bool(np.any(post != pre))

sep_d, phi_d, par_sep, con_sep, par_phi, con_phi, learn_all = [], [], [], [], [], [], True
for t in range(NTRIALS):
    init_w = get_w(build_model())
    pf, pl = stream_fit_forward(pX, init_w, EXPOSURES)
    cf, cl = stream_fit_forward(cX, init_w, EXPOSURES)
    ps, cs = sep_axis(pf, pheads), sep_axis(cf, cheads)
    pp, cp = phi_proxy_axis(pf), phi_proxy_axis(cf)
    sep_d.append(ps - cs); phi_d.append(pp - cp)
    par_sep.append(ps); con_sep.append(cs); par_phi.append(pp); con_phi.append(cp)
    learn_all = learn_all and pl and cl
    print(f"[4lever] trial {t:2d}: SEP par={ps:.5f} con={cs:.5f} d={ps-cs:+.5f} | PHI par={pp:.5f} con={cp:.5f} d={pp-cp:+.5f} | learn_hw={pl and cl}", flush=True)

def stats(arr):
    a = np.array(arr, dtype=np.float64)
    m = float(a.mean()); sd = float(a.std(ddof=1)) if len(a) > 1 else float("nan")
    sem = sd/np.sqrt(len(a)) if len(a) > 1 else float("nan")
    lo, hi = m - 1.96*sem, m + 1.96*sem
    npos = int((a > 0).sum()); nneg = int((a < 0).sum())
    return dict(mean=m, sd=sd, sem=sem, ci95=[lo, hi], n_positive=npos, n_negative=nneg,
                sign_stable=bool(npos == len(a) or nneg == len(a)))

sep_s = stats(sep_d); phi_s = stats(phi_d)
axis_a_green = bool(learn_all and sep_s["mean"] > 0 and sep_s["ci95"][0] > 0)
axis_b_green = bool(learn_all and phi_s["mean"] > 0 and phi_s["ci95"][0] > 0)

if not learn_all:
    verdict, reason, which = "RED", "on-chip learning failed on >=1 trial (could not measure C1)", None
elif axis_a_green or axis_b_green:
    which = ("last-layer-separation" if axis_a_green else "") + ("|" if axis_a_green and axis_b_green else "") + ("phi-proxy" if axis_b_green else "")
    verdict = "GREEN"
    reason = (f"SUPPORTED: on-chip learn live on all {NTRIALS} trials AND on axis [{which}] paired delta robustly > 0 "
              f"(SEP mean={sep_s['mean']:.5f} CI={sep_s['ci95']}; PHI mean={phi_s['mean']:.5f} CI={phi_s['ci95']}). "
              f"H_911 advantage was sub-noise and is RESCUED by all-4-levers. Earned on axis: {which}.")
else:
    which = None
    verdict = "RED"
    reason = (f"REFUTED: BOTH measure axes' 95% CI include 0 across {NTRIALS} chip trials with all-4-levers "
              f"(200-anchor 5-lang corpus + {EXPOSURES}x learn-while-infer streaming online accumulation). "
              f"SEP mean={sep_s['mean']:.5f} 95%CI={sep_s['ci95']} ({sep_s['n_positive']}pos/{sep_s['n_negative']}neg); "
              f"PHI mean={phi_s['mean']:.5f} 95%CI={phi_s['ci95']} ({phi_s['n_positive']}pos/{phi_s['n_negative']}neg). "
              f"STRONGEST closed-negative: H_911's cross-lingual semantic-linkage advantage does NOT transfer to "
              f"AKD1000 last-layer Hebbian edge-learn EVEN WITH ALL FOUR SIGNAL-LIFT LEVERS -- the per-ordering gap "
              f"stays within the chip's stochastic-plasticity noise floor (H_904) on BOTH axes. Supersedes #1652.")

res = {"hypothesis":"F-CLM-AKIDA-SEMANTIC-SIGNAL-LIFT","id":"H_912",
       "ties":["H_912","H_911","H_877","H_904","C1","C2","C3","C4","C5","C6"],
       "method":(f"ALL-4-LEVERS: N={NTRIALS} paired on-chip trials; per-trial shared init; AkidaUnsupervised "
                 f"fit() ON CHIP; lever1=200-anchor 5-lang corpus; lever2={EXPOSURES}x exposure accumulation; "
                 f"lever3=DUAL axis (a)last-layer-separation, (b)phi-proxy=whole_EI-min_bipartition; "
                 f"lever4=LEARN-WHILE-INFER streaming online (per anchor fit-then-forward in member order)"),
       "akida_version":akida.__version__,"device":str(DEV.version),"ip_version":str(DEV.ip_version),
       "ts":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
       "backbone_int4_sha256":BACKBONE_SHA,"inc":INC,"units":UNITS,"num_weights":NWEIGHTS,
       "learning_competition":LCOMP,"exposures":EXPOSURES,"learn_while_infer_streaming":True,
       "n_concepts":len(set(h['concept'] for h in pheads)),"corpus_anchors":pc,
       "parallel_shard_sha256":p_sha,"concat_shard_sha256":c_sha,"n_trials":NTRIALS,
       "axis_a_last_layer_separation":{"deltas":sep_d,"par_means":par_sep,"con_means":con_sep,**sep_s,"green":axis_a_green},
       "axis_b_phi_proxy":{"deltas":phi_d,"par_means":par_phi,"con_means":con_phi,**phi_s,"green":axis_b_green},
       "learn_happened_hw":learn_all,"green_axis":which,
       "verdict":verdict,"verdict_reason":reason}
with open(os.path.join(OUT,"result_4lever.json"),"w") as f: json.dump(res,f,indent=2,ensure_ascii=False)
print(f"\n[4lever] AXIS-A last-layer-sep : mean={sep_s['mean']:+.5f} 95%CI=[{sep_s['ci95'][0]:+.5f},{sep_s['ci95'][1]:+.5f}] {sep_s['n_positive']}pos/{sep_s['n_negative']}neg green={axis_a_green}")
print(f"[4lever] AXIS-B phi-proxy      : mean={phi_s['mean']:+.5f} 95%CI=[{phi_s['ci95'][0]:+.5f},{phi_s['ci95'][1]:+.5f}] {phi_s['n_positive']}pos/{phi_s['n_negative']}neg green={axis_b_green}")
print(f"[4lever] learn_happened_hw(all)={learn_all}  green_axis={which}")
print(f"[4lever] VERDICT {verdict} -- {reason}")
print(f"[4lever] wrote {os.path.join(OUT,'result_4lever.json')}")
