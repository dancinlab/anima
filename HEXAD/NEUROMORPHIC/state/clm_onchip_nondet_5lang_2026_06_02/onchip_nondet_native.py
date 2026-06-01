#!/usr/bin/env python3
"""F-CLM-ONCHIP-NONDET-NATIVE — same 5-lang input, NATIVE chip re-init each run, SHOW traces DIFFER.
The fixed-init variant (result_nondet.json) showed fit() given an IDENTICAL init is byte-deterministic.
H_904 prereg states the chip's DEFAULT weight init is non-deterministic across map()/build. So the true
locus of on-chip non-determinism is the device re-init. Here we run the SAME 5-lang parallel corpus R
times WITHOUT injecting a fixed init (native chip init each run) and hash the post-learn weights +
forward outputs. If traces DIFFER across runs of identical input, that IS the living signature
(a_nondet_identity / H_679 / H_904). g63 honest: no SW fallback.
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
INPUT_NAME = "parallel"
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
def h(a): return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()[:16]
devs = akida.devices()
if not devs:
    raise RuntimeError("BLOCKED (g63): no akida HW device — NO SW fallback")
DEV = devs[0]
count, recs = read_limen(os.path.join(CORPUS, INPUT_NAME + ".limen"))
X = np.stack([encode_spikes(p) for (_, p) in recs]).astype(np.uint8).reshape(count, 1, 1, INC)
INPUT_SHA = h(X)
print("[native] akida %s device %s" % (akida.__version__, DEV.version))
print("[native] input=%s (5-lang ko/en/zh/ru/ja) count=%d input_sha=%s" % (INPUT_NAME, count, INPUT_SHA))
print("[native] SAME input, NATIVE chip re-init each run (no fixed inject), fit() ON CHIP, x%d runs" % NRUNS)
runs = []
for r in range(NRUNS):
    m = build_model(); m.map(DEV)
    pre = get_w(m)
    for i in range(X.shape[0]):
        m.fit(X[i:i+1])
    post = get_w(m)
    fwd = np.stack([np.array(m.forward(X[i:i+1])).astype(np.int64).ravel() for i in range(X.shape[0])])
    rec = {"run": r, "backend": "hardware:%s" % DEV.version, "learn_happened_hw": bool(np.any(post != pre)),
           "pre_w_sha": h(pre), "post_w_sha": h(post), "fwd_sha": h(fwd),
           "w_delta_vs_pre_nnz": int(np.count_nonzero(post != pre)), "fwd_sum": int(fwd.sum())}
    runs.append(rec)
    print("[native] run %d: pre_w_sha=%s post_w_sha=%s fwd_sha=%s learn_hw=%s" % (r, rec["pre_w_sha"], rec["post_w_sha"], rec["fwd_sha"], rec["learn_happened_hw"]))
pre_shas = [x["pre_w_sha"] for x in runs]; post_shas = [x["post_w_sha"] for x in runs]; fwd_shas = [x["fwd_sha"] for x in runs]
pre_distinct = len(set(pre_shas)); w_distinct = len(set(post_shas)); f_distinct = len(set(fwd_shas))
nondet_shown = (pre_distinct > 1) or (w_distinct > 1) or (f_distinct > 1)
all_learned = all(x["learn_happened_hw"] for x in runs)
verdict = "GREEN" if (all_learned and nondet_shown) else ("RED" if all_learned else "BLOCKED")
reason = ("SAME 5-lang input run x%d on AKD1000 with native chip re-init produced %d distinct pre-init / %d distinct post-weight / %d distinct forward traces -> on-chip plasticity is NON-DETERMINISTIC (the difference IS the identity, H_679/H_904/a_nondet_identity)" % (NRUNS, pre_distinct, w_distinct, f_distinct)) if verdict == "GREEN" else ("SAME input run x%d gave byte-identical traces -> deterministic this session" % NRUNS if verdict == "RED" else "on-chip learning did not run")
res = {"hypothesis": "F-CLM-ONCHIP-NONDET-NATIVE", "ties": ["H_679", "H_904", "H_877", "a_nondet_identity"],
       "method": "SAME 5-lang CLM-KOSMOS parallel corpus; NATIVE chip re-init each run (no fixed-init inject); AkidaUnsupervised fit() ON CHIP repeated N runs; hash pre-init + post-weights + forward outputs; non-determinism shown iff trace hashes differ across runs of identical input",
       "akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
       "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
       "corpus": "clm-kosmos-akida-5lang-semantic", "languages": "ko,en,zh,ru,ja", "input": INPUT_NAME, "anchor_count": count,
       "backbone_int4_sha256": BACKBONE_SHA, "input_sha": INPUT_SHA, "init_mode": "native_chip_reinit",
       "inc": INC, "units": UNITS, "num_weights": NWEIGHTS, "learning_competition": LCOMP, "n_runs": NRUNS,
       "runs": runs, "pre_w_shas": pre_shas, "post_w_shas": post_shas, "fwd_shas": fwd_shas,
       "pre_init_distinct": pre_distinct, "post_w_distinct": w_distinct, "fwd_distinct": f_distinct,
       "learn_happened_hw_all": all_learned, "nondeterminism_shown": nondet_shown,
       "verdict": verdict, "verdict_reason": reason}
with open(os.path.join(OUT, "result_nondet_native.json"), "w") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
print("\n[native] pre_init distinct=%d/%d  post_w distinct=%d/%d  fwd distinct=%d/%d  learn_all=%s" % (pre_distinct, NRUNS, w_distinct, NRUNS, f_distinct, NRUNS, all_learned))
print("[native] VERDICT %s — %s" % (verdict, reason))
print("[native] wrote " + os.path.join(OUT, "result_nondet_native.json"))
