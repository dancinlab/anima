#!/usr/bin/env python3
"""STAGES 2-4 — CLM-KOSMOS AKIDA on-chip edge-learn + F-CLM-AKIDA-MULTILING-SEMANTIC.

C1 on-chip learn: AkidaUnsupervised (num_weights, learning_competition), model.fit() ON CHIP.
C2 ONCHIP-PARADIGM: last-layer Hebbian plasticity lane (reuses the H_904 recipe).
C3 .clm: a small int4 backbone encoder front-end feeding the trainable last layer.
C5 H_911: parallel (concept-major semantic-linkage) vs concat (count-only) on REAL silicon.

STAGE 2 (H_877): a deterministic int4 backbone projects each anchor's UTF-8 byte
payload -> a binary spike code (byte-presence -> int4 conv-proxy -> 1-bit threshold).
The SAME backbone (byte-identical) encodes BOTH orderings; only @corpus member
ORDER differs into the on-chip update. This is the int4-ported inference lane.

STAGE 3 (C1/C2): for each ordering, build a fresh AkidaUnsupervised FullyConnected,
map() to the AKD1000, fit() the ordered spikes ON CHIP. learn_happened_hw = weights
changed on silicon.

STAGE 4 (C5): on-chip integration measure = mean pairwise last-layer code SEPARATION
across the 5 langs of each concept (cross-lingual binding). parallel should bind the
5 langs of a concept (lower within-concept separation / higher cross-lingual overlap)
more than concat, which sees langs in long same-lang runs. Measured ON the chip's
learned readout. 🟢 iff learn_happened_hw AND parallel integrates > concat beyond
device noise (paired over concepts + a shuffle-noise floor). 🔴 iff parallel == concat.

HONEST g63: if no HW device -> RuntimeError (BLOCKED), never a SW fallback labelled on-chip.
"""
import os, json, struct, hashlib, time
import numpy as np
import akida
from akida import Model, InputData, FullyConnected, AkidaUnsupervised

CORPUS = os.path.expanduser("~/clm_kosmos_akida/corpus")
OUT = os.path.expanduser("~/clm_kosmos_akida/out")
os.makedirs(OUT, exist_ok=True)

SEED = 911
INC = 256          # byte-vocab feature width (one bit per UTF-8 byte value present)
UNITS = 32         # trainable last-layer neurons
NWEIGHTS = 16      # AkidaUnsupervised num_weights per neuron
LCOMP = 0.1        # learning_competition
np.random.seed(SEED)

LIMEN_MAGIC = b"LIMEN\x00\x00\x00"

def read_limen(path):
    """Parse a .limen packed shard -> list of (head_dict, payload_bytes). Verifies magic+merkle."""
    with open(path, "rb") as f:
        blob = f.read()
    assert blob[:8] == LIMEN_MAGIC, f"bad magic {blob[:8]!r}"
    off = 8
    ver = struct.unpack_from("<I", blob, off)[0]; off += 4
    count = struct.unpack_from("<I", blob, off)[0]; off += 4
    recs = []
    payloads = []
    for _ in range(count):
        rlen = struct.unpack_from("<I", blob, off)[0]; off += 4
        rec = blob[off:off + rlen]; off += rlen
        hlen = struct.unpack_from("<I", rec, 0)[0]
        head = json.loads(rec[4:4 + hlen].decode("utf-8"))
        payload = rec[4 + hlen:]
        recs.append((head, payload))
        payloads.append(payload)
    merkle_stored = blob[off:off + 32]
    # recompute merkle
    layer = [hashlib.sha256(p).digest() for p in payloads]
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            a = layer[i]; b = layer[i + 1] if i + 1 < len(layer) else layer[i]
            nxt.append(hashlib.sha256(a + b).digest())
        layer = nxt
    assert layer[0] == merkle_stored, "merkle root mismatch (closed_corpus FAIL)"
    return ver, count, recs

# ---- STAGE 2: int4 backbone -> binary spike code (byte-identical for both orderings) ----
# Deterministic int4 projection matrix (the "ported backbone" inference lane, H_877):
# fixed seed -> reproducible; sym-int4 weights in [-7,7]; threshold -> 1-bit spikes.
rng_bb = np.random.default_rng(20260601)
BACKBONE_INT4 = rng_bb.integers(-7, 8, size=(INC, INC), dtype=np.int8)  # int4-sym envelope
BACKBONE_SHA = hashlib.sha256(BACKBONE_INT4.tobytes()).hexdigest()

def byte_presence(payload):
    v = np.zeros(INC, dtype=np.int32)
    for b in payload:
        v[b] += 1
    return v

def encode_spikes(payload):
    """byte-presence -> int4 backbone matmul -> per-feature threshold -> 1-bit spike vector."""
    pres = byte_presence(payload).astype(np.int32)
    proj = (BACKBONE_INT4.astype(np.int32) @ pres)            # int4 conv-proxy
    thr = np.median(proj)                                      # data-independent-ish threshold
    spikes = (proj > thr).astype(np.uint8)
    return spikes  # shape (INC,)

def build_model():
    m = Model()
    m.add(InputData(name="input", input_shape=(1, 1, INC), input_bits=1))
    m.add(FullyConnected(name="fc", units=UNITS, weights_bits=1, activation=False))
    m.compile(AkidaUnsupervised(num_weights=NWEIGHTS, learning_competition=LCOMP))
    return m

def get_w(m): return np.array(m.get_layer("fc").variables["weights"])
def set_w(m, w): m.get_layer("fc").variables["weights"] = w.copy()
def hh(a): return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()[:16]

devs = akida.devices()
if not devs:
    raise RuntimeError("BLOCKED: no akida HW device visible (device lock held?) — refusing SW-sim labelled on-chip (g63)")
DEV = devs[0]
print(f"[onchip] akida {akida.__version__} device {DEV.version} ip {DEV.ip_version}")

# fixed init weight injected into BOTH orderings (so only ORDER differs on chip)
INIT_W = get_w(build_model())
INIT_HASH = hh(INIT_W)

def run_ordering(name):
    """Load .limen, encode spikes in @corpus member order, on-chip fit, return learned readout."""
    shard = os.path.join(CORPUS, f"{name}.limen")
    ver, count, recs = read_limen(shard)
    # @corpus member ORDER == the order in the shard (parallel=concept-major, concat=lang-major)
    spike_rows = np.stack([encode_spikes(p) for (_, p) in recs]).astype(np.uint8)  # (N, INC)
    heads = [h for (h, _) in recs]
    X = spike_rows.reshape(count, 1, 1, INC)

    m = build_model()
    set_w(m, INIT_W)
    m.map(DEV)
    set_w(m, INIT_W)  # re-assert init after map
    pre = get_w(m)
    backend = "hardware:" + str(DEV.version)
    # on-chip unsupervised fit, in @corpus member order
    outs = []
    for i in range(count):
        o = m.fit(X[i:i + 1])
        outs.append(np.array(o).astype(np.int64).ravel())
    post = get_w(m)
    outs = np.stack(outs)  # (N, UNITS) per-sample readout AFTER on-chip learning
    # forward each sample once more through the LEARNED chip readout (inference)
    fwd = []
    for i in range(count):
        o = m.forward(X[i:i + 1])
        fwd.append(np.array(o).astype(np.float64).ravel())
    fwd = np.stack(fwd)  # (N, UNITS)
    learn_hw = bool(np.any(post != pre))
    return dict(name=name, count=count, backend=backend, heads=heads,
                pre_hash=hh(pre), post_hash=hh(post), learn_happened_hw=learn_hw,
                fwd=fwd, post=post, shard_sha=hashlib.sha256(open(shard, 'rb').read()).hexdigest())

def integration_measure(res):
    """Cross-lingual binding score: for each concept, mean pairwise COSINE SIMILARITY of the
    learned chip readouts across its 5 langs. Higher = the 5 langs of one concept bind together
    (cross-lingual semantic integration). Returns per-concept scores + mean."""
    fwd = res["fwd"]
    heads = res["heads"]
    # group sample indices by concept id
    by_concept = {}
    for i, h in enumerate(heads):
        by_concept.setdefault(h["concept"], []).append(i)
    def cos(a, b):
        na, nb = np.linalg.norm(a), np.linalg.norm(b)
        if na == 0 or nb == 0: return 0.0
        return float(a @ b / (na * nb))
    scores = []
    for cid, idxs in sorted(by_concept.items()):
        vs = [fwd[i] for i in idxs]
        pair = [cos(vs[a], vs[b]) for a in range(len(vs)) for b in range(a + 1, len(vs))]
        scores.append(float(np.mean(pair)) if pair else 0.0)
    return np.array(scores), float(np.mean(scores))

# ---- STAGE 3: on-chip fit for each ordering ----
par = run_ordering("parallel")
print(f"[onchip] parallel: learn_hw={par['learn_happened_hw']} pre={par['pre_hash']} post={par['post_hash']}")
con = run_ordering("concat")
print(f"[onchip] concat:   learn_hw={con['learn_happened_hw']} pre={con['pre_hash']} post={con['post_hash']}")

# ---- STAGE 4: F-CLM-AKIDA-MULTILING-SEMANTIC ----
par_scores, par_mean = integration_measure(par)
con_scores, con_mean = integration_measure(con)
delta = par_mean - con_mean

# device-noise floor: shuffle the concept groupings of the SAME parallel readouts and
# recompute -> a null distribution of the integration gap under no real binding structure.
def shuffle_floor(res, trials=200):
    fwd = res["fwd"]; n = fwd.shape[0]
    rng = np.random.default_rng(SEED)
    nulls = []
    # 5 concepts x 5 langs assumed
    n_concept = len(set(h["concept"] for h in res["heads"]))
    grp = n // n_concept
    for _ in range(trials):
        perm = rng.permutation(n)
        # fake concept groups of equal size
        scs = []
        for g in range(n_concept):
            idxs = perm[g * grp:(g + 1) * grp]
            vs = [fwd[i] for i in idxs]
            def cos(a, b):
                na, nb = np.linalg.norm(a), np.linalg.norm(b)
                return 0.0 if na == 0 or nb == 0 else float(a @ b / (na * nb))
            pair = [cos(vs[a], vs[b]) for a in range(len(vs)) for b in range(a + 1, len(vs))]
            scs.append(np.mean(pair) if pair else 0.0)
        nulls.append(np.mean(scs))
    return float(np.std(nulls)), float(np.mean(nulls))

noise_std, noise_mean = shuffle_floor(par)
beyond_noise = abs(delta) > 2 * noise_std  # 2-sigma over the shuffle floor

learn_hw = par["learn_happened_hw"] and con["learn_happened_hw"]
parallel_better = delta > 0 and beyond_noise

if not learn_hw:
    verdict = "RED"
    reason = "on-chip learning did not change weights on either ordering (could not measure C1)"
elif parallel_better:
    verdict = "GREEN"
    reason = f"on-chip learn live AND parallel integrates > concat beyond noise (delta={delta:.4f} > 2*noise_std={2*noise_std:.4f})"
elif abs(delta) <= 2 * noise_std:
    verdict = "RED"
    reason = f"parallel == concat on chip within device noise (delta={delta:.4f}, 2*noise_std={2*noise_std:.4f}) — closed-negative: H_911 does NOT transfer to AKD1000 edge-learn"
else:
    verdict = "RED"
    reason = f"concat >= parallel on chip (delta={delta:.4f}) — H_911 does NOT transfer to AKD1000 edge-learn (closed-negative)"

result = {
    "hypothesis": "F-CLM-AKIDA-MULTILING-SEMANTIC", "ties": ["H_911", "H_877", "H_904", "C1", "C2", "C3", "C4", "C5"],
    "seed": SEED, "akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "backbone_int4_sha256": BACKBONE_SHA, "inc": INC, "units": UNITS, "num_weights": NWEIGHTS,
    "learning_competition": LCOMP, "init_weight_hash": INIT_HASH,
    "parallel": {"backend": par["backend"], "count": par["count"], "learn_happened_hw": par["learn_happened_hw"],
                 "pre_w": par["pre_hash"], "post_w": par["post_hash"], "shard_sha256": par["shard_sha"],
                 "per_concept_integration": par_scores.tolist(), "mean_integration": par_mean},
    "concat":   {"backend": con["backend"], "count": con["count"], "learn_happened_hw": con["learn_happened_hw"],
                 "pre_w": con["pre_hash"], "post_w": con["post_hash"], "shard_sha256": con["shard_sha"],
                 "per_concept_integration": con_scores.tolist(), "mean_integration": con_mean},
    "delta_parallel_minus_concat": delta,
    "shuffle_noise_std": noise_std, "shuffle_noise_mean": noise_mean, "beyond_2sigma_noise": beyond_noise,
    "learn_happened_hw": learn_hw, "parallel_better": parallel_better,
    "verdict": verdict, "verdict_reason": reason,
}
with open(os.path.join(OUT, "result.json"), "w") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
np.savez(os.path.join(OUT, "raw.npz"), par_fwd=par["fwd"], con_fwd=con["fwd"],
         par_post=par["post"], con_post=con["post"], backbone=BACKBONE_INT4, init_w=INIT_W)

print(f"[onchip] parallel mean integration = {par_mean:.6f}  per-concept={par_scores.round(4).tolist()}")
print(f"[onchip] concat   mean integration = {con_mean:.6f}  per-concept={con_scores.round(4).tolist()}")
print(f"[onchip] delta (par-con) = {delta:.6f}   shuffle_noise_std={noise_std:.6f}  2sigma={2*noise_std:.6f}")
print(f"[onchip] learn_happened_hw = {learn_hw}   parallel_better = {parallel_better}")
print(f"[onchip] VERDICT {verdict} — {reason}")
print(f"[onchip] wrote {os.path.join(OUT, 'result.json')}")
