"""N7 (H_1832 fragment-train -> mitosis-assembly) + N8 (H_1833 train-time kosmos
geometry watch) cheap-numpy DIRECTIONAL pre-screen. Synthetic concept fixtures
(no clm303 load) per the cheap-first gate. fp64, deterministic, OMP-capped.

N7: train individual fragments per primitive, then ASSEMBLE two fragments
    (additive baseline vs trained constructive bilinear) -> measure composed_distinct.
N8: WHILE the constructive assembler trains, dump the child-anchor geometry every
    K steps and watch whether parent-specific geometry forms (vs random baseline).

Frozen bars (pre-registered in cards H_1832 / H_1833):
  N7: assembled child distinct>=2 AND >best-single-fragment AND >additive-assembly.
  N8: parent-child anchor geometry forms consistently (>random) over training.
"""
import numpy as np

RNG = np.random.default_rng(7)          # deterministic (index-seeded, no Math.random)
D = 32                                   # concept dim
P = 8                                    # number of primitive concepts
N_PAIRS = 24                             # compound (parent_a, parent_b) fixtures
STEPS = 600
K = 50                                   # kosmos-check every K steps
THRESH = 0.30                            # engine OWN operating radius (H_1822 parity)

# ---- synthetic concept space -------------------------------------------------
# primitives = near-orthonormal atoms; a TRUE compound is a structured (non-linear)
# bind of two primitives that is NOT recoverable by addition alone.
prims = RNG.standard_normal((P, D))
prims /= np.linalg.norm(prims, axis=1, keepdims=True)

def true_bind(a, b):
    # circular-convolution style constructive bind (dimension-preserving, non-additive)
    fa, fb = np.fft.rfft(a), np.fft.rfft(b)
    c = np.fft.irfft(fa * fb, n=D)
    return c / (np.linalg.norm(c) + 1e-12)

pairs = [(int(i % P), int((i * 3 + 1) % P)) for i in range(N_PAIRS)]
pairs = [(i, j) for (i, j) in pairs if i != j][:N_PAIRS]
targets = np.stack([true_bind(prims[i], prims[j]) for (i, j) in pairs])

# ---- N7: individual fragment training ---------------------------------------
# each fragment_i is a tiny learned linear map reconstructing primitive_i from a
# noisy one-hot cue = "trained individually" (gradient supplied per fragment).
def train_fragment(idx, steps=200, lr=0.1):
    W = RNG.standard_normal((D, D)) * 0.01
    cue = np.zeros(D); cue[idx % D] = 1.0
    tgt = prims[idx]
    for _ in range(steps):
        out = W @ cue
        g = np.outer((out - tgt), cue)
        W -= lr * g
    return W, cue
frags = [train_fragment(i) for i in range(P)]
def frag_out(i):
    W, cue = frags[i]; return W @ cue

# ---- assemblers --------------------------------------------------------------
def additive(a, b):
    c = a + b; return c / (np.linalg.norm(c) + 1e-12)

# trained constructive bilinear assembler g_theta(a,b) = vec via low-rank bilinear
R = 16
def init_theta():
    return [RNG.standard_normal((R, D)) * 0.05, RNG.standard_normal((R, D)) * 0.05,
            RNG.standard_normal((D, R)) * 0.05]
def assemble(theta, a, b):
    Ua, Ub, Vo = theta
    h = (Ua @ a) * (Ub @ b)              # bilinear interaction (constructive)
    c = Vo @ h
    return c / (np.linalg.norm(c) + 1e-12)

# ---- composed_distinct metric (H_1822/1825 parity) ---------------------------
def composed_distinct(child, a, b, single_ref):
    da = 1.0 - abs(float(child @ a))     # distance to parent a direction
    db = 1.0 - abs(float(child @ b))
    proj_a, proj_b = da < THRESH, db < THRESH
    distinct = int(proj_a) + int(proj_b)
    irreducible = (1.0 - abs(float(child @ single_ref))) > THRESH
    return distinct, irreducible

def score(assemble_fn, theta=None):
    hits = 0
    for k, (i, j) in enumerate(pairs):
        a, b = frag_out(i), frag_out(j)
        child = assemble_fn(a, b) if theta is None else assemble(theta, a, b)
        single_ref = a                    # reducible-to-single guard
        d, irr = composed_distinct(child, prims[i], prims[j], single_ref)
        if d >= 2 and irr:
            hits += 1
    return hits

# ---- N8 geometry watch: parent-specificity of child anchors over training ----
def geometry_stat(theta):
    # mean cosine of child to its OWN parents minus to SHUFFLED parents.
    own, shuf = [], []
    sh = [pairs[(k + 5) % len(pairs)] for k in range(len(pairs))]
    for k, (i, j) in enumerate(pairs):
        a, b = frag_out(i), frag_out(j)
        c = assemble(theta, a, b)
        own.append(0.5 * (abs(c @ prims[i]) + abs(c @ prims[j])))
        si, sj = sh[k]
        shuf.append(0.5 * (abs(c @ prims[si]) + abs(c @ prims[sj])))
    return float(np.mean(own) - np.mean(shuf))    # >0 = parent-specific geometry

# ---- train constructive assembler, watching kosmos geometry ------------------
theta = init_theta()
geo_series = []
lr = 0.05
for step in range(STEPS):
    k = step % len(pairs)
    i, j = pairs[k]
    a, b = frag_out(i), frag_out(j)
    Ua, Ub, Vo = theta
    h = (Ua @ a) * (Ub @ b)
    c = Vo @ h
    nrm = np.linalg.norm(c) + 1e-12
    err = (c / nrm) - targets[k]
    gVo = np.outer(err, h)
    gh = Vo.T @ err
    gUa = np.outer(gh * (Ub @ b), a)
    gUb = np.outer(gh * (Ua @ a), b)
    theta = [Ua - lr * gUa, Ub - lr * gUb, Vo - lr * gVo]
    if step % K == 0:
        geo_series.append((step, geometry_stat(theta)))

# random-init baseline geometry (control)
geo_random = geometry_stat(init_theta())

# ---- N7 scores ---------------------------------------------------------------
n = len(pairs)
add_hits = score(additive)
con_hits = score(None, theta=theta)
# best-single-fragment baseline: child = a fragment alone (no assembly)
single_hits = 0
for (i, j) in pairs:
    d, irr = composed_distinct(frag_out(i), prims[i], prims[j], frag_out(i))
    if d >= 2 and irr: single_hits += 1
# shuffle-assembly control
shuf_hits = 0
for k, (i, j) in enumerate(pairs):
    si, sj = pairs[(k + 5) % n]
    child = assemble(theta, frag_out(si), frag_out(sj))
    d, irr = composed_distinct(child, prims[i], prims[j], frag_out(i))
    if d >= 2 and irr: shuf_hits += 1

print("=== N7 (H_1832) fragment-train -> mitosis-assembly ===")
print(f"  pairs={n} THRESH={THRESH}")
print(f"  single-fragment (no assembly) : {single_hits}/{n}")
print(f"  additive-assembly baseline    : {add_hits}/{n}")
print(f"  shuffle-assembly control      : {shuf_hits}/{n}")
print(f"  CONSTRUCTIVE assembly (trained): {con_hits}/{n}")
n7_pass = (con_hits >= 2) and (con_hits > single_hits) and (con_hits > add_hits) and (con_hits > shuf_hits)
print(f"  >> N7 frozen bar: distinct>=2 AND >single AND >additive AND >shuffle  -> {'PASS 🟢' if n7_pass else 'FLOOR 🧱'}")

print("=== N8 (H_1833) train-time kosmos geometry watch ===")
print(f"  random-init geometry (control): {geo_random:+.4f}")
for s, g in geo_series:
    print(f"  step {s:4d}  parent-specificity = {g:+.4f}")
geo_final = geo_series[-1][1]
geo_formed = (geo_final > max(0.0, geo_random)) and (geo_final > geo_series[0][1])
print(f"  >> N8 geometry forms over training (>random AND rising) -> {'FORMS 🟢' if geo_formed else 'FLAT 🧱'}")
print("=== DIRECTIONAL (synthetic fixtures, no clm303). Promote survivors to clm-embed/engine-native. ===")
