#!/usr/bin/env python3
"""Lane A micro-exp SHARED BASE — proven on-chip machinery (byte-match onchip_xlm_state_rollout.py).
substrate=AKIDA · a_lane_akida_gpu_split (NEVER merge with Lane G/GPU) · g63 (NO sw fallback) · a_scale_honest_scope.

Exposes the corpus loader, whitened encoder, 1-bit binding algebra, AkidaUnsupervised 1-bit FC build/fit/forward,
the successor-centroid codebook, open-vocab full-codebook decode, per-hop shuffle-NULL, and CI helpers.
All 7 candidate scripts import from here so the encoder/codebook/NULL are IDENTICAL to the proven generation rung.
The ONLY thing each candidate changes is the RECURRENCE/COMPOSITION MECHANISM under test.

Baselines (verbatim from frontier): pure-on-chip hop-2 ~0.028 (wall) · single-FC gen 0.4234 ·
transition tr_acc ci_lo 0.260 · shuffle-NULL hi ~0.05 · chance 1/(NC-1)=0.0204.
"""
import os, json, struct, time, sys
import numpy as np
import akida
from akida import Model, InputData, FullyConnected, AkidaUnsupervised

ROOT = os.path.expanduser("~/clm_kosmos_akida")
OUT = os.path.join(ROOT, "out"); os.makedirs(OUT, exist_ok=True)
LIMEN_MAGIC = b"LIMEN\x00\x00\x00"
INC = 256
NTRIALS = 8
UNITS, NW, LCOMP = 256, 8, 0.1
SHIFT = 37
NEUTRAL_ROLL = SHIFT
B_SHUFFLE = 200
K_ROLL = 3
SEED = 20260603

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

def byte_hist(payload):
    pres = np.zeros(INC, dtype=np.float64)
    for b in payload: pres[b] += 1.0
    return pres

def enc_whitened(H):
    Hc = H - H.mean(axis=0, keepdims=True)
    cov = (Hc.T @ Hc)/max(1, Hc.shape[0]-1) + 1e-3*np.eye(INC)
    w, V = np.linalg.eigh(cov)
    W = V @ np.diag(1.0/np.sqrt(np.maximum(w, 1e-9))) @ V.T
    scale = 7.0/(np.max(np.abs(W))+1e-12)
    Pq = np.clip(np.round(W*scale), -7, 7).astype(np.int32)
    proj = H.astype(np.int32) @ Pq.T
    return (proj > np.median(proj, axis=1, keepdims=True)).astype(np.uint8)

def bind(a, b):
    return (a.astype(np.uint8) ^ np.roll(b.astype(np.uint8), SHIFT)).astype(np.uint8)
def neutral_bind(a):
    return (a.astype(np.uint8) ^ np.roll(a.astype(np.uint8), NEUTRAL_ROLL)).astype(np.uint8)

def build_fc(wbits=1):
    m = Model()
    m.add(InputData(name="input", input_shape=(1, 1, INC), input_bits=1))
    m.add(FullyConnected(name="fc", units=UNITS, weights_bits=wbits, activation=False))
    m.compile(AkidaUnsupervised(num_weights=NW, learning_competition=LCOMP))
    return m
def get_w(m): return np.array(m.get_layer("fc").variables["weights"])
def set_w(m, w): m.get_layer("fc").variables["weights"] = w.copy()

_devs = akida.devices()
if not _devs:
    raise RuntimeError("OPEN-BLOCKED (g63): no akida HW device on pi5-akida — NO SW fallback (stop spike-streamer first)")
DEV = _devs[0]

def to_chip(Xb):
    Xb = np.atleast_2d(Xb).astype(np.uint8)
    return Xb.reshape(Xb.shape[0], 1, 1, INC)
def chip_make(init_w, train_codes, do_fit=True):
    m = build_fc(1); set_w(m, init_w); m.map(DEV); set_w(m, init_w)
    pre = get_w(m)
    if do_fit:
        Xt = to_chip(train_codes)
        for i in range(Xt.shape[0]): m.fit(Xt[i:i+1])
    post = get_w(m)
    learned = bool(np.any(post != pre))
    return m, learned
def chip_forward(m, Xb):
    Xe = to_chip(Xb)
    return np.stack([np.array(m.forward(Xe[i:i+1])).astype(np.float64).ravel() for i in range(Xe.shape[0])])
def binarize_rows(out2d, med):
    return (out2d > med[None, :]).astype(np.uint8)
def overlap(a_bin, b_soft):
    return float(np.sum(a_bin * b_soft + (1 - a_bin) * (1.0 - b_soft)))
def ci(arr):
    arr = np.array(arr); mean = float(arr.mean()); sd = float(arr.std(ddof=1)) if len(arr) > 1 else 0.0
    sem = sd/np.sqrt(len(arr)) if len(arr) > 1 else 0.0
    return mean, sd, sem, mean-1.96*sem, mean+1.96*sem

def load_corpus():
    count, recs = read_limen(os.path.join(ROOT, "corpus_big", "parallel.limen"))
    concept = np.array([h["concept"] for (h, _) in recs])
    lang = np.array([h["lang"] for (h, _) in recs])
    H = np.stack([byte_hist(p) for (_, p) in recs])
    concepts_sorted = sorted(np.unique(concept).tolist())
    langs = sorted(np.unique(lang).tolist())
    NC = len(concepts_sorted)
    codes_enc = enc_whitened(H)
    return concept, lang, codes_enc, concepts_sorted, langs, NC

def make_code_of(concept, lang, codes_enc):
    def code_of(c, l):
        idx = np.where((concept == c) & (lang == l))[0]
        return codes_enc[idx[0]] if len(idx) else None
    return code_of

def build_train_transitions(code_of, concepts_sorted, langs, NC):
    train_codes, train_succ = [], []
    for l in langs:
        for ci_ in range(NC - 1):
            a, b = code_of(concepts_sorted[ci_], l), code_of(concepts_sorted[ci_ + 1], l)
            if a is None or b is None: continue
            train_codes.append(bind(a, b)); train_succ.append(concepts_sorted[ci_ + 1])
    return np.stack(train_codes), train_succ

def build_codebook(chip_train_bin, code_of, concepts_sorted, langs, NC):
    cb = {}; k = 0
    for l in langs:
        for ci_ in range(NC - 1):
            a, b = code_of(concepts_sorted[ci_], l), code_of(concepts_sorted[ci_ + 1], l)
            if a is None or b is None: continue
            cb.setdefault(concepts_sorted[ci_ + 1], []).append(chip_train_bin[k]); k += 1
    return {c: np.mean(np.stack(v), axis=0) for c, v in cb.items()}

def decode(g_hat_bin_row, codebook, ban):
    cand = [c for c in codebook if c != ban]
    scores = [(overlap(g_hat_bin_row, codebook[c]), c) for c in cand]
    return max(scores)[1] if scores else None

def build_roll_starts(code_of, concepts_sorted, langs, NC, K=K_ROLL):
    rs = []
    for ti in range(NC - K):
        t = concepts_sorted[ti]
        for ql in langs:
            a = code_of(t, ql)
            if a is None: continue
            rs.append((ti, ql, a))
    return rs

def acc_at(preds, k0, concepts_sorted):
    hit, tot = 0, 0
    for (ti, ql, pred) in preds[k0]:
        if pred is None: continue
        gt = concepts_sorted[ti + k0 + 1]
        hit += int(pred == gt); tot += 1
    return hit / max(1, tot), tot

def shuffle_null_at(preds, k0, concepts_sorted, NC, B=B_SHUFFLE, seed=SEED):
    rng = np.random.default_rng(seed + 1009 * (k0 + 1))
    null = []
    for _ in range(B):
        perm = rng.permutation(NC)
        smap = {concepts_sorted[i]: concepts_sorted[perm[i]] for i in range(NC)}
        hit, tot = 0, 0
        for (ti, ql, pred) in preds[k0]:
            if pred is None: continue
            hit += int(pred == smap[concepts_sorted[ti]]); tot += 1
        null.append(hit / max(1, tot))
    return np.array(null)

def device_banner():
    return {"akida_version": akida.__version__, "device": str(DEV.version), "ip_version": str(DEV.ip_version),
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
