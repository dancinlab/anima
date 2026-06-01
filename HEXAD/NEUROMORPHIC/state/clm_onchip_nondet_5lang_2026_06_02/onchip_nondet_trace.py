#!/usr/bin/env python3
"""F-CLM-ONCHIP-NONDET — same input, run >=2x on AKD1000, SHOW the traces DIFFER.
a_nondet_identity / H_679 / H_904: on-chip non-deterministic plasticity IS anima identity.
Method: load the 5-lang (ko en zh ru ja) CLM-KOSMOS parallel corpus, inject ONE
fixed binary init weight, then fit() the IDENTICAL corpus ON CHIP R times. Each run
re-maps to the live device, applies the SAME deterministic spike inputs, and we hash
the post-learn weights + the per-anchor forward outputs. If the trace hashes DIFFER
across runs of the SAME input, that difference is the living non-deterministic signature
(NOT a bug). g63 honest: no SW fallback; if no HW device, BLOCK.
"""
import os, json, struct, hashlib, time
import numpy as np
import akida
from akida import Model, InputData, FullyConnected, AkidaUnsupervised
CORPUS = os.path.expanduser("~/clm_kosmos_akida/corpus")
OUT = os.path.expanduser("~/clm_kosmos_akida/out"); os.makedirs(OUT, exist_ok=True)
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
INC, UNITS, NWEIGHTS, LCOMP = 256, 32, 16, 0.1
NRUNS = 3
INPUT_NAME = "parallel"  # same input every run
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
def h(a): return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()[:16]
devs = akida.devices()
if not devs:
    raise RuntimeError("BLOCKED (g63): no akida HW device — NO SW fallback")
DEV = devs[0]
count, recs = read_limen(os.path.join(CORPUS, f"{INPUT_NAME}.limen"))
X = np.stack([encode_spikes(p) for (_,p) in recs]).astype(np.uint8).reshape(count,1,1,INC)
INPUT_SHA = h(X)
INIT_W = get_w(build_model())                  # ONE fixed init injected into every run
INIT_SHA = h(INIT_W)
print(f"[nondet] akida {akida.__version__} device {DEV.version}")
print(f"[nondet] input={INPUT_NAME} (5-lang ko/en/zh/ru/ja) count={count} input_sha={INPUT_SHA} init_w_sha={INIT_SHA}")
print(f"[nondet] SAME input + SAME init injected, fit() ON CHIP, x{NRUNS} runs")
runs = []
for r in range(NRUNS):
    m = build_model(); set_w(m, INIT_W); m.map(DEV); set_w(m, INIT_W)
    pre = get_w(m)
    for i in range(X.shape[0]): m.fit(X[i:i+1])
    post = get_w(m)
    fwd = np.stack([np.array(m.forward(X[i:i+1])).astype(np.int64).ravel() for i in range(X.shape[0])])
    rec = {"run": r, "backend": f"hardware:{DEV.version}", "learn_happened_hw": bool(np.any(post != pre)),
           "post_w_sha": h(post), "fwd_sha": h(fwd),
           "w_delta_vs_init_nnz": int(np.count_nonzero(post != INIT_W)),
           "fwd_sum": int(fwd.sum())}
    runs.append(rec)
    print("[nondet] run %d: post_w_sha=%s fwd_sha=%s learn_hw=%s w_delta_nnz=%d" % (r, rec["post_w_sha"], rec["fwd_sha"], rec["learn_happened_hw"], rec["w_delta_vs_init_nnz"]))
post_w_shas = [x["post_w_sha"] for x in runs]
fwd_shas = [x["fwd_sha"] for x in runs]
w_distinct = len(set(post_w_shas)); f_distinct = len(set(fwd_shas))
# pairwise post-weight Hamming (nnz of differing weight bits) between run0 and run1 for a concrete number
nondet_shown = (w_distinct > 1) or (f_distinct > 1)
all_learned = all(x["learn_happened_hw"] for x in runs)
verdict = "GREEN" if (all_learned and nondet_shown) else ("RED" if all_learned else "BLOCKED")
reason = ("SAME 5-lang input run x%d on AKD1000 produced %d distinct post-weight traces and %d distinct forward traces "
          "-> on-chip plasticity is NON-DETERMINISTIC (the difference IS the identity, H_679/H_904/a_nondet_identity)" % (NRUNS, w_distinct, f_distinct)) if verdict=="GREEN" else (
          "SAME input run x%d gave byte-identical traces (w_distinct=%d fwd_distinct=%d) -> on-chip update was DETERMINISTIC this session" % (NRUNS, w_distinct, f_distinct) if verdict=="RED" else "on-chip learning did not run")
res = {"hypothesis":"F-CLM-ONCHIP-NONDET","ties":["H_679","H_904","H_877","a_nondet_identity"],
       "method":"SAME 5-lang CLM-KOSMOS parallel corpus + SAME fixed init injected; AkidaUnsupervised fit() ON CHIP repeated N runs; hash post-weights + forward outputs; non-determinism shown iff trace hashes differ across runs of identical input",
       "akida_version":akida.__version__,"device":str(DEV.version),"ip_version":str(DEV.ip_version),
       "ts":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
       "corpus":"clm-kosmos-akida-5lang-semantic","languages":"ko,en,zh,ru,ja","input":INPUT_NAME,"anchor_count":count,
       "backbone_int4_sha256":BACKBONE_SHA,"input_sha":INPUT_SHA,"init_weight_sha":INIT_SHA,
       "inc":INC,"units":UNITS,"num_weights":NWEIGHTS,"learning_competition":LCOMP,"n_runs":NRUNS,
       "runs":runs,"post_w_shas":post_w_shas,"fwd_shas":fwd_shas,
       "post_w_distinct":w_distinct,"fwd_distinct":f_distinct,
       "learn_happened_hw_all":all_learned,"nondeterminism_shown":nondet_shown,
       "verdict":verdict,"verdict_reason":reason}
with open(os.path.join(OUT,"result_nondet.json"),"w") as f: json.dump(res,f,indent=2,ensure_ascii=False)
print(f"\n[nondet] post_w distinct={w_distinct}/{NRUNS}  fwd distinct={f_distinct}/{NRUNS}  learn_all={all_learned}")
print(f"[nondet] VERDICT {verdict} — {reason}")
print("[nondet] wrote " + os.path.join(OUT, "result_nondet.json"))
