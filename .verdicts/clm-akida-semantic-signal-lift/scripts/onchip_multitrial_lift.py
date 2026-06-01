#!/usr/bin/env python3
"""STAGES 2-4 (C6 / H_912) — F-CLM-AKIDA-SEMANTIC-SIGNAL-LIFT across N paired on-chip trials.

H_912 sub-noise rescue probe: does the H_911 parallel>concat gap rise SIGNIFICANTLY POSITIVE
above the AKD1000 stochastic-plasticity noise floor once we apply the two HW-feasible levers --
(a) a LARGER 5-lang cross-lingual corpus and (b) N-EXPOSURE ACCUMULATION (each anchor presented
E times per arm per trial)? Last-layer AkidaUnsupervised Hebbian ONLY (HW constraint honored).

Identical machinery to the #1652 multitrial harness (int4 backbone H_877, shared per-trial init,
paired parallel/concat, integration = mean within-concept cross-lingual cosine of the LEARNED chip
readout) -- the ONLY changes are: larger corpus path + EXPOSURES repeats per anchor + N>=20 trials.

VERDICT (frozen prereg):
  GREEN iff learn_happened_hw on EVERY trial AND paired mean(par-con) > 0 with 95% CI lower bound > 0.
  RED   iff 95% CI includes 0 (lower bound <= 0) -> stronger closed-negative, H_911 does NOT transfer
        to AKD1000 last-layer Hebbian even with more signal + accumulation.
HONEST g63: no HW device -> RuntimeError (BLOCKED). Never a SW fallback labelled on-chip.
No single lucky draw -- decided on the paired N>=20 delta distribution.
"""
import os, sys, json, struct, hashlib, time
import numpy as np
import akida
from akida import Model, InputData, FullyConnected, AkidaUnsupervised

CORPUS = os.path.expanduser("~/clm_kosmos_akida_large/corpus")
OUT = os.path.expanduser("~/clm_kosmos_akida_large/out")
os.makedirs(OUT, exist_ok=True)
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
INC, UNITS, NWEIGHTS, LCOMP = 256, 32, 16, 0.1

# levers
NTRIALS  = int(os.environ.get("H912_NTRIALS", "20"))   # >= 20 paired trials (anti-cherry-pick)
EXPOSURES = int(os.environ.get("H912_EXPOSURES", "3"))  # N-exposure accumulation per anchor per arm
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
print(f"[lift] akida {akida.__version__} device {DEV.version} ip {DEV.ip_version}")
print(f"[lift] N={NTRIALS} paired trials  EXPOSURES={EXPOSURES} per anchor per arm")

def load(name):
    count, recs = read_limen(os.path.join(CORPUS, f"{name}.limen"))
    X = np.stack([encode_spikes(p) for (_,p) in recs]).astype(np.uint8).reshape(count,1,1,INC)
    heads = [h for (h,_) in recs]
    shard_sha = hashlib.sha256(open(os.path.join(CORPUS, f"{name}.limen"),"rb").read()).hexdigest()
    return count, X, heads, shard_sha

pc, pX, pheads, p_sha = load("parallel")
cc, cX, cheads, c_sha = load("concat")
print(f"[lift] corpus: parallel={pc} anchors  concat={cc} anchors  (concepts={len(set(h['concept'] for h in pheads))})")

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

def fit_forward(X, init_w, exposures):
    """on-chip fit with N-exposure accumulation: present every anchor `exposures` times
    in @corpus member order (lever b). Then read out the learned chip forward per anchor."""
    m = build_model(); set_w(m, init_w); m.map(DEV); set_w(m, init_w)
    pre = get_w(m)
    for _ in range(exposures):
        for i in range(X.shape[0]):
            m.fit(X[i:i+1])
    post = get_w(m)
    fwd = np.stack([np.array(m.forward(X[i:i+1])).astype(np.float64).ravel() for i in range(X.shape[0])])
    return fwd, bool(np.any(post != pre))

deltas, par_means, con_means, learn_all = [], [], [], True
for t in range(NTRIALS):
    init_w = get_w(build_model())   # per-trial init shared within the pair
    pf, pl = fit_forward(pX, init_w, EXPOSURES)
    cf, cl = fit_forward(cX, init_w, EXPOSURES)
    pm, cm = integration(pf, pheads), integration(cf, cheads)
    d = pm - cm
    deltas.append(d); par_means.append(pm); con_means.append(cm)
    learn_all = learn_all and pl and cl
    print(f"[lift] trial {t:2d}: par={pm:.5f} con={cm:.5f} delta={d:+.5f} learn_hw={pl and cl}", flush=True)

deltas = np.array(deltas)
mean_d = float(deltas.mean()); sd = float(deltas.std(ddof=1)); sem = sd/np.sqrt(len(deltas))
ci_lo, ci_hi = mean_d - 1.96*sem, mean_d + 1.96*sem
n_pos = int((deltas > 0).sum()); n_neg = int((deltas < 0).sum())
sign_stable = bool((n_pos == len(deltas)) or (n_neg == len(deltas)))
robust_parallel_better = bool(learn_all and (ci_lo > 0))   # frozen rule: CI lower bound strictly > 0

if not learn_all:
    verdict, reason = "RED", "on-chip learning failed on >=1 trial (could not measure C1)"
elif robust_parallel_better:
    verdict = "GREEN"
    reason = (f"SUPPORTED: on-chip learn live on all {len(deltas)} trials AND paired delta robustly > 0 "
              f"(mean={mean_d:.5f}, 95%CI=[{ci_lo:.5f},{ci_hi:.5f}] strictly > 0, {n_pos}/{len(deltas)} positive). "
              f"H_911 advantage was sub-noise and is RESCUED by larger corpus ({pc} anchors) + {EXPOSURES}x exposure accumulation.")
else:
    verdict = "RED"
    reason = (f"REFUTED: paired delta CI still includes 0 across {len(deltas)} chip trials with {pc}-anchor corpus + "
              f"{EXPOSURES}x exposure accumulation (mean={mean_d:.5f}, 95%CI=[{ci_lo:.5f},{ci_hi:.5f}], "
              f"{n_pos} pos / {n_neg} neg, sign_stable={sign_stable}). STRONGER closed-negative: H_911's cross-lingual "
              f"semantic-linkage advantage does NOT transfer to AKD1000 last-layer Hebbian edge-learn EVEN WITH MORE "
              f"SIGNAL -- the per-ordering gap stays within the chip's stochastic-plasticity noise floor (H_904). "
              f"Supersedes/strengthens #1652.")

res = {"hypothesis":"F-CLM-AKIDA-SEMANTIC-SIGNAL-LIFT","ties":["H_912","H_911","H_877","H_904","C1","C2","C3","C4","C6"],
       "method":f"N={len(deltas)} paired on-chip trials; per-trial shared init; AkidaUnsupervised fit() ON CHIP; "
                f"{EXPOSURES}x N-exposure accumulation per anchor per arm; larger {pc}-anchor 5-lang corpus; "
                f"integration=mean within-concept cross-lingual cosine of learned readout",
       "akida_version":akida.__version__,"device":str(DEV.version),"ip_version":str(DEV.ip_version),
       "ts":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
       "backbone_int4_sha256":BACKBONE_SHA,"inc":INC,"units":UNITS,"num_weights":NWEIGHTS,"learning_competition":LCOMP,
       "exposures":EXPOSURES,"n_concepts":len(set(h['concept'] for h in pheads)),
       "corpus_anchors":pc,"parallel_shard_sha256":p_sha,"concat_shard_sha256":c_sha,
       "n_trials":len(deltas),"deltas":deltas.tolist(),"par_means":par_means,"con_means":con_means,
       "mean_delta":mean_d,"delta_sd":sd,"delta_sem":sem,"ci95":[ci_lo,ci_hi],
       "n_positive":n_pos,"n_negative":n_neg,"sign_stable":sign_stable,
       "learn_happened_hw":learn_all,"robust_parallel_better":robust_parallel_better,
       "verdict":verdict,"verdict_reason":reason}
with open(os.path.join(OUT,"result_multitrial.json"),"w") as f: json.dump(res,f,indent=2,ensure_ascii=False)
print(f"\n[lift] mean_delta={mean_d:+.5f}  95%CI=[{ci_lo:+.5f},{ci_hi:+.5f}]  {n_pos} pos / {n_neg} neg  sign_stable={sign_stable}")
print(f"[lift] learn_happened_hw(all)={learn_all}  robust_parallel_better={robust_parallel_better}")
print(f"[lift] VERDICT {verdict} -- {reason}")
print(f"[lift] wrote {os.path.join(OUT,'result_multitrial.json')}")
