#!/usr/bin/env python3
"""L3 G6-falsifiability FALSIFY round — non-commutativity A of h1129 303M self-composition.

engine-native: core/decode.py py-canonical (== anima evaluate --py 2-production, a_eval_py_canonical).
rep = forward-last hidden lastrow[d], canonical decode.py ops reused byte-exact.
See PREREGISTRATION.md for the pre-registered bar.
"""
import sys, os, json, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'core'))
import numpy as np
import decode as D

BIN = os.path.expanduser('~/anima-weights/bytegpt303_h1129/h1129.bin')
SUF = " is"   # common probe suffix -> identical last token both orders -> isolates composition-order

W = D.bg_load(BIN)
d = W['d']; nlay = W['nlay']; nh = W['nh']

def rep(s):
    """forward-last hidden lastrow[d] via canonical decode.py ops (byte-exact path)."""
    ids = list(s.encode('utf-8')); T = len(ids)
    idsa = np.asarray(ids, dtype=np.int64)
    x = W['tok'][idsa] + W['pos'][0:T]
    for Lr in range(nlay):
        nrm = D._bg_layernorm_rows(x, W['ln1w'][Lr], W['ln1b'][Lr], T, d)
        aout = D._bg_mha(nrm, W['inW'][Lr], W['inB'][Lr], W['oW'][Lr], W['oB'][Lr], T, d, nh)
        x = x + aout
        nrm = D._bg_layernorm_rows(x, W['ln2w'][Lr], W['ln2b'][Lr], T, d)
        h4 = nrm @ W['m0W'][Lr].T + W['m0B'][Lr]; h4 = D._bg_gelu(h4)
        mlpo = h4 @ W['m2W'][Lr].T + W['m2B'][Lr]; x = x + mlpo
    lastrow = D._bg_layernorm_rows(x[T-1:T], W['lnfw'], W['lnfb'], 1, d)[0]
    return lastrow

def cosd(a, b):
    na = np.linalg.norm(a); nb = np.linalg.norm(b)
    if na == 0 or nb == 0: return 0.0
    return float(np.dot(a, b) / (na * nb))

def A_of(x, y, suf=""):
    rXY = rep(x + " " + y + suf)
    rYX = rep(y + " " + x + suf)
    return 1.0 - cosd(rXY, rYX), rXY, rYX

# ---- byte-exact canonical sanity ----
_lr = rep("cat dog")
_lg_canon = D.bg_forward_last_W(W, list("cat dog".encode()), len("cat dog".encode()))
byte_exact = float(np.max(np.abs((W['head'] @ _lr) - _lg_canon)))

# ---- held-out meaningful concept pairs ----
CONCEPTS = ["cat", "dog", "fire", "water", "king", "queen", "sun", "moon",
            "fish", "bird", "tree", "stone", "gold", "iron", "north", "south",
            "hot", "cold", "war", "peace", "day", "night", "left", "right",
            "wolf", "sheep", "rain", "snow", "mother", "child", "door", "key"]
rng = random.Random(1129)
pairs = []
seen = set()
while len(pairs) < 60:
    a, b = rng.sample(CONCEPTS, 2)
    k = (a, b)
    if k in seen or (b, a) in seen: continue
    seen.add(k); pairs.append((a, b))

# ---- random-string positional-floor control (length-matched-ish) ----
def rand_word(n):
    return "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(n))
rand_pairs = [(rand_word(len(a)), rand_word(len(b))) for (a, b) in pairs]

# ---- measure ----
A_naive, A_probe = [], []
antisym_frac = []   # ||D||/||T|| for probe target (FM: additive floor cannot represent D)
XY_probe_reps = []
for (a, b) in pairs:
    an, _, _ = A_of(a, b, "")
    ap, rXY, rYX = A_of(a, b, SUF)
    A_naive.append(an); A_probe.append(ap)
    Dv = 0.5 * (rXY - rYX)
    antisym_frac.append(float(np.linalg.norm(Dv) / np.linalg.norm(rXY)))
    XY_probe_reps.append((a, b, rXY, rYX))

A_rand = []
for (a, b) in rand_pairs:
    ap, _, _ = A_of(a, b, SUF)
    A_rand.append(ap)

# self-identity byte control
r1 = rep("cat dog is"); C_self = 1.0 - cosd(r1, r1)

# derangement control: pair X_i with Y_j (j != i), antisym frac
idx = list(range(len(pairs)))
der = idx[1:] + idx[:1]  # cyclic shift derangement
antisym_der = []
for i, j in zip(idx, der):
    a = pairs[i][0]; b = pairs[j][1]
    if a == b: continue
    _, rXY, rYX = A_of(a, b, SUF)
    antisym_der.append(float(np.linalg.norm(0.5*(rXY-rYX)) / np.linalg.norm(rXY)))

def med(v): return float(np.median(v))
def mean(v): return float(np.mean(v))
def std(v): return float(np.std(v))

m_naive = med(A_naive); m_probe = med(A_probe); r_probe = med(A_rand)
earned_margin = med(antisym_frac); derange_ctrl = med(antisym_der)

# ---- pre-registered decision ----
if m_probe < 0.02 or m_probe <= 1.2 * r_probe:
    verdict = "REFUTED-G6-universal-wall"
elif m_probe >= 0.05 and m_probe >= 1.5 * r_probe:
    verdict = "SUPPORTED-reopen"
else:
    verdict = "DIRECTIONAL"

out = {
    "model": "h1129 303M ByteGPT", "bin": BIN,
    "engine": "core/decode.py py-canonical (anima evaluate --py 2-production)",
    "byte_exact_head_lastrow_maxabs": byte_exact,
    "n_pairs": len(pairs), "probe_suffix": SUF,
    "A_naive": {"median": m_naive, "mean": mean(A_naive), "std": std(A_naive),
                "min": float(np.min(A_naive)), "max": float(np.max(A_naive))},
    "A_probe": {"median": m_probe, "mean": mean(A_probe), "std": std(A_probe),
                "min": float(np.min(A_probe)), "max": float(np.max(A_probe))},
    "control": {
        "C_self_must_be_0": C_self,
        "C_rand_probe_median": r_probe, "C_rand_probe_mean": mean(A_rand), "C_rand_probe_std": std(A_rand),
        "ratio_m_probe_over_r_probe": (m_probe / r_probe) if r_probe else None,
    },
    "FM_full_vs_additive": {
        "target": "rep('X Y'+SUF)[d] ; additive(commutative) can produce only S=(rXY+rYX)/2, error>=||D||",
        "earned_margin_median_antisymfrac": earned_margin,
        "earned_margin_mean": mean(antisym_frac),
        "derange_control_median": derange_ctrl,
        "earned_over_derange_ratio": (earned_margin / derange_ctrl) if derange_ctrl else None,
    },
    "prereg_thresholds": {
        "REFUTED_if": "m_probe<0.02 OR m_probe<=1.2*r_probe",
        "SUPPORTED_if": "m_probe>=0.05 AND m_probe>=1.5*r_probe",
    },
    "verdict": verdict,
}
print(json.dumps(out, indent=2))
with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
    json.dump(out, f, indent=2)
