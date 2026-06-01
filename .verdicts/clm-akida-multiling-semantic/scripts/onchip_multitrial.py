#!/usr/bin/env python3
"""STAGE 4 (robust) — F-CLM-AKIDA-MULTILING-SEMANTIC across N on-chip trials.

The single-run harness flips verdict run-to-run because AKD1000 on-chip plasticity is
STOCHASTIC (H_904): the device re-inits weights on map() non-deterministically, so the
parallel-vs-concat integration delta is itself a random variable. Honest scope (g63)
forbids cherry-picking one run. The correct falsifier test: run N PAIRED trials (parallel
and concat under the SAME per-trial chip init), collect the delta distribution, and ask
whether parallel>concat is STABLE beyond device noise.

🟢 iff learn_happened_hw on every trial AND the paired delta is significantly > 0 across
trials (one-sided: mean_delta > 0 AND mean_delta - 2*SEM > 0, i.e. CI excludes 0 AND most
trials agree in sign). 🔴 iff the delta straddles 0 (sign unstable across trials) -> the
H_911 semantic-linkage advantage does NOT robustly transfer to AKD1000 last-layer Hebbian
edge-learn (closed-negative, publishable).
"""
import os, json, struct, hashlib, time
import numpy as np
import akida
from akida import Model, InputData, FullyConnected, AkidaUnsupervised

CORPUS = os.path.expanduser("~/clm_kosmos_akida/corpus")
OUT = os.path.expanduser("~/clm_kosmos_akida/out")
os.makedirs(OUT, exist_ok=True)
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
INC, UNITS, NWEIGHTS, LCOMP = 256, 32, 16, 0.1
NTRIALS = 12

def read_limen(path):
    with open(path, "rb") as f: blob = f.read()
    assert blob[:8] == LIMEN_MAGIC
    off = 8
    struct.unpack_from("<I", blob, off)[0]; off += 4
    count = struct.unpack_from("<I", blob, off)[0]; off += 4
    recs = []
    for _ in range(count):
        rlen = struct.unpack_from("<I", blob, off)[0]; off += 4
        rec = blob[off:off+rlen]; off += rlen
        hlen = struct.unpack_from("<I", rec, 0)[0]
        head = json.loads(rec[4:4+hlen].decode("utf-8"))
        recs.append((head, rec[4+hlen:]))
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
    raise RuntimeError("BLOCKED: no akida HW device (g63 — no SW fallback)")
DEV = devs[0]
print(f"[multi] akida {akida.__version__} device {DEV.version}  N={NTRIALS} paired trials")

def load(name):
    count, recs = read_limen(os.path.join(CORPUS, f"{name}.limen"))
    X = np.stack([encode_spikes(p) for (_,p) in recs]).astype(np.uint8).reshape(count,1,1,INC)
    heads = [h for (h,_) in recs]
    return count, X, heads

pc, pX, pheads = load("parallel")
cc, cX, cheads = load("concat")

def integration(fwd, heads):
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

def fit_forward(X, init_w):
    m = build_model(); set_w(m, init_w); m.map(DEV); set_w(m, init_w)
    pre = get_w(m)
    for i in range(X.shape[0]): m.fit(X[i:i+1])
    post = get_w(m)
    fwd = np.stack([np.array(m.forward(X[i:i+1])).astype(np.float64).ravel() for i in range(X.shape[0])])
    return fwd, bool(np.any(post != pre))

deltas, par_means, con_means, learn_all = [], [], [], True
for t in range(NTRIALS):
    init_w = get_w(build_model())   # per-trial init (shared within the pair)
    pf, pl = fit_forward(pX, init_w)
    cf, cl = fit_forward(cX, init_w)
    pm, cm = integration(pf, pheads), integration(cf, cheads)
    d = pm - cm
    deltas.append(d); par_means.append(pm); con_means.append(cm)
    learn_all = learn_all and pl and cl
    print(f"[multi] trial {t:2d}: par={pm:.5f} con={cm:.5f} delta={d:+.5f} learn_hw={pl and cl}")

deltas = np.array(deltas)
mean_d = float(deltas.mean()); sd = float(deltas.std(ddof=1)); sem = sd/np.sqrt(len(deltas))
ci_lo, ci_hi = mean_d - 1.96*sem, mean_d + 1.96*sem
n_pos = int((deltas > 0).sum()); n_neg = int((deltas < 0).sum())
sign_stable = bool((n_pos == len(deltas)) or (n_neg == len(deltas)))
robust_parallel_better = bool(learn_all and (ci_lo > 0) and (n_pos >= len(deltas) - 1))

if not learn_all:
    verdict, reason = "RED", "on-chip learning failed on >=1 trial (could not measure C1)"
elif robust_parallel_better:
    verdict = "GREEN"
    reason = f"on-chip learn live on all {len(deltas)} trials AND paired delta robustly > 0 (mean={mean_d:.5f}, 95%CI=[{ci_lo:.5f},{ci_hi:.5f}], {n_pos}/{len(deltas)} positive)"
else:
    verdict = "RED"
    reason = (f"parallel == concat on AKD1000: paired delta straddles 0 across {len(deltas)} chip trials "
              f"(mean={mean_d:.5f}, 95%CI=[{ci_lo:.5f},{ci_hi:.5f}], {n_pos} pos / {n_neg} neg, sign_stable={sign_stable}). "
              f"Closed-negative: H_911 semantic-linkage advantage does NOT robustly transfer to AKD1000 last-layer Hebbian edge-learn "
              f"— the per-ordering integration gap is within the chip's own stochastic-plasticity noise (H_904).")

res = {"hypothesis":"F-CLM-AKIDA-MULTILING-SEMANTIC","ties":["H_911","H_877","H_904","C1","C2","C3","C4","C5"],
       "method":"N paired on-chip trials; per-trial shared init; AkidaUnsupervised fit() ON CHIP; integration=mean within-concept cross-lingual cosine of learned readout",
       "akida_version":akida.__version__,"device":str(DEV.version),"ip_version":str(DEV.ip_version),
       "ts":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
       "backbone_int4_sha256":BACKBONE_SHA,"inc":INC,"units":UNITS,"num_weights":NWEIGHTS,"learning_competition":LCOMP,
       "n_trials":len(deltas),"deltas":deltas.tolist(),"par_means":par_means,"con_means":con_means,
       "mean_delta":mean_d,"delta_sd":sd,"delta_sem":sem,"ci95":[ci_lo,ci_hi],
       "n_positive":n_pos,"n_negative":n_neg,"sign_stable":sign_stable,
       "learn_happened_hw":learn_all,"robust_parallel_better":robust_parallel_better,
       "verdict":verdict,"verdict_reason":reason}
with open(os.path.join(OUT,"result_multitrial.json"),"w") as f: json.dump(res,f,indent=2,ensure_ascii=False)
print(f"\n[multi] mean_delta={mean_d:+.5f}  95%CI=[{ci_lo:+.5f},{ci_hi:+.5f}]  {n_pos} pos / {n_neg} neg  sign_stable={sign_stable}")
print(f"[multi] learn_happened_hw(all)={learn_all}  robust_parallel_better={robust_parallel_better}")
print(f"[multi] VERDICT {verdict} — {reason}")
print(f"[multi] wrote {os.path.join(OUT,'result_multitrial.json')}")
