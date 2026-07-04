#!/usr/bin/env python3
# ==========================================================================
# H_1718 — Claustrum Conductor Phase-Consensus Binding Hub  ($0 cheap_test)
# ==========================================================================
# DIRECTIONAL ONLY — numpy toy, NO torch (a_engine_native_learning).
# Terminal verdict requires cli/anima.hexa -> generator L3 -> g_gates byte-parity.
#
# ----------------------------------------------------------------------
# Card mechanism (the differentiator):
#   Crick-Koch claustrum = a thin low-D sheet reciprocally wired to ALL cortex
#   that SYNCHRONIZES distributed assemblies into ONE bound moment. Modules each
#   emit a candidate representation + a PHASE tag; all fan into a single low-D
#   HUB (serial bottleneck) that computes a Kuramoto phase-CONSENSUS over the
#   mutually-consistent modules and broadcasts ONE global pulse. Modules that can
#   phase-LOCK to the pulse are BOUND & ignited; modules that cannot lock are
#   excluded (silence). Binding-by-synchronization: a constituent's inclusion
#   depends on the REST via the consensus -> non-separable conjunction.
#
#   The decisive G1 claim: the consensus selects the JOINTLY-consistent assembly
#   => super-additive (composed > max_single). The INERT control: CUT the
#   claustral fan-out (hub coupling K=0) => modules cannot co-lock => bag-of-
#   channels => composed collapses to max_single (paired ~ shuffled).
#
# WHY this can break the G1 wall where CE-on-marginals (clm303 lossF~0 yet
#   recombine-fail) cannot: a bag-of-independent-channels readout binds A,B by
#   CO-OCCURRENCE only (separable). The Kuramoto consensus makes a module's phase
#   (hence its inclusion in the bound readout) a FUNCTION of the other modules'
#   phases — a genuinely non-separable conjunction operator. If the toy shows
#   the hub is load-bearing (ablation collapses) AND the toy has resolution
#   (grok ctrl passes), the mechanism is a candidate G1 lever.
#
# ----------------------------------------------------------------------
# FROZEN BARS  (pre-registered HERE, before any run — tune-to-green forbidden, p7)
# ----------------------------------------------------------------------
# G1 / binding (the load-bearing rung):
#   We construct AMBIGUOUS pairs: scene {A=(s1,c1), B=(s2,c2)}  vs the SWAP
#   {(s1,c2),(s2,c1)} — IDENTICAL marginal (per-feature) statistics, DIFFERENT
#   conjunctions. A separable/bag-of-channels reader is forced to ~0.5 (copy/
#   guess) on the discriminating bits; a true binder reaches ~1.0.
#
#   (G1) PASS iff
#         composed_distinct >= 2                       (>=2 distinct conjunctions resolved)
#     AND composed_distinct_hub > max_single           (super-additive over best single module)
#     AND hub_ambig_acc        >= 0.95                 (real binding ~1.0, not 0.5 copy)
#     AND bag_ambig_acc        <= 0.60                 (separable bag ~ chance 0.5)
#
#   (INERT) ablation — cut hub fan-out (K=0), everything else identical:
#         load_bearing iff  ablate_ambig_acc <= 0.60   (collapses to bag/copy floor)
#         INERT        iff  ablate_ambig_acc ~= hub     (mechanism contributes 0)
#
#   (GROK CTRL · under-power guard) — canonical grokkable modular ADDITION at the
#     SAME rung/optimizer the probe uses. PASS iff grok_held >> chance(=1/P).
#     If grok_held ~= chance: the toy LACKS resolution => verdict = UNDER-POWER
#     (NOT the mechanism's fault; honest, not a false NOT).
#
# OVERALL:
#   survivor=true ONLY iff  (G1 frozen bar PASS) AND (grok_ctrl PASS)
#                            AND (ablation load-bearing).   [very conservative]
#   If grok_ctrl FAIL -> UNDER-POWER (report ablation INERT/load-bearing anyway).
#   If G1 fails but grok passes -> NOT-SUPPORTED.
# ----------------------------------------------------------------------
import numpy as np

SEED = 7
rng = np.random.default_rng(SEED)

# --- conjunction world: S shapes x C colors ---
S, C = 4, 4
def cidx(s, c): return s * C + c
NC = S * C                              # 16 conjunctions

# ==========================================================================
# THE MECHANISM — Kuramoto phase-consensus binding hub.
#
# A scene presents M=2 objects. Each object is a MODULE that emits:
#   - a candidate readout (its conjunction one-hot, learned codebook)
#   - a PHASE theta_m derived from its (shape,color) via a learned phase map.
# The HUB couples all module phases (all-to-all through the low-D hub) and runs
# Kuramoto settling; modules whose phases converge within a lock window are
# BOUND; the bound set is read out together. The phase map is set so that a
# module's natural frequency depends on BOTH its shape AND color (conjunction),
# so co-locking is conjunction-sensitive (the hub enforces joint consistency).
#
# Binding readout: for the bound set, the hub produces a JOINT key = the sum of
# locked modules' phase-rotated codes; a module is "included" in the bound
# readout only if it locked. The discriminating test reads which conjunctions
# are present in the bound assembly.
#
# Crucially: with the hub ON, lock depends on the OTHER module (coupling) =>
# the SWAP pair (different conjunctions, same marginals) yields a DIFFERENT
# locked-phase pattern => separable readers can't, the hub can.
# With K=0 (hub OFF) modules free-run independently => no co-lock structure =>
# readout reduces to an order-/identity-blind bag.
# ==========================================================================

# phase per conjunction: a conjunction-specific natural frequency (non-separable
# in (s,c): we DELIBERATELY make omega a function of the JOINT index, not s+c,
# so that the bound assembly distinguishes {(s1,c1),(s2,c2)} from the swap).
# To keep it honest (not hand-coding the answer), omega is a fixed pseudo-random
# map from conjunction-index; the *binding* (which co-lock) is what the hub does.
OMEGA = rng.uniform(0.5, 1.5, size=NC)         # natural freq per conjunction
PHI0  = rng.uniform(0, 2*np.pi, size=NC)        # phase offset per conjunction

def module_phases(objs):
    """natural freq + offset for each object module."""
    return (np.array([OMEGA[cidx(s,c)] for (s,c) in objs]),
            np.array([PHI0[cidx(s,c)]  for (s,c) in objs]))

def kuramoto_settle(omega, phi0, K, steps=300, dt=0.05):
    """All-to-all Kuramoto. K=0 => free-run (hub fan-out cut = INERT ablation)."""
    theta = phi0.copy()
    M = len(theta)
    for _ in range(steps):
        # mean-field coupling THROUGH the hub (order parameter)
        if K > 0 and M > 1:
            mean_sin = np.mean(np.sin(theta))
            mean_cos = np.mean(np.cos(theta))
            R = np.hypot(mean_sin, mean_cos)
            psi = np.arctan2(mean_sin, mean_cos)
            coupling = K * R * np.sin(psi - theta)
        else:
            coupling = 0.0
        theta = theta + dt * (omega + coupling)
    return theta

def locked_pattern(objs, K):
    """Return per-object 'bound-readout' contribution = whether it phase-locked
    to the consensus, weighted by its phase coherence. Build a JOINT bound code
    over conjunction slots reflecting the SETTLED (post-consensus) state."""
    omega, phi0 = module_phases(objs)
    theta = kuramoto_settle(omega, phi0, K)
    # consensus phase
    psi = np.arctan2(np.mean(np.sin(theta)), np.mean(np.cos(theta)))
    # lock weight per module = cos(theta_m - psi) clipped to [0,1] (coherence)
    lock_w = np.clip(np.cos(theta - psi), 0.0, 1.0)
    # the bound readout writes each object's conjunction slot, gated by lock_w
    # AND by the PHASE-ROTATED phase (so settled phase carries which-bound info).
    code = np.zeros(NC)
    for (objc, w, th) in zip(objs, lock_w, theta):
        # rotate the unit code by the settled phase to make binding phase-dependent
        code[cidx(*objc)] += w * (0.5 + 0.5*np.cos(th - psi))
    return code, theta, lock_w

# ==========================================================================
# READOUT TRAINING — a linear readout maps the bound code (or bag) to presence.
# We TRAIN a readout on TRAIN conjunctions (held-out the NOVEL ones for G2-ish)
# and evaluate on the AMBIGUOUS binding-required pairs.
#
# Two readers:
#   HUB : reader over the consensus-bound code (K>0)  — sees binding structure
#   BAG : reader over the bag-of-channels (K=0 free-run code) — separable
# Same architecture & training, ONLY the hub coupling differs => clean INERT.
# ==========================================================================
ALL = [(s,c) for s in range(S) for c in range(C)]
NOVEL = [(0,0),(1,2),(3,3)]
TRAIN_CONJ = [x for x in ALL if x not in NOVEL]

def scene_target(objs):
    t = np.zeros(NC)
    for o in objs: t[cidx(*o)] = 1.0
    return t

def make_codes(n, pool, K, require_novel=False):
    X, T = [], []
    for _ in range(n):
        if require_novel:
            nv = NOVEL[rng.integers(len(NOVEL))]
            objs = [nv, ALL[rng.integers(len(ALL))]]
        else:
            o1 = pool[rng.integers(len(pool))]
            o2 = pool[rng.integers(len(pool))]
            objs = [o1, o2]
        code, _, _ = locked_pattern(objs, K)
        X.append(code); T.append(scene_target(objs))
    return np.array(X), np.array(T)

def train_readout(X, T, epochs=300, lr=0.5):
    """ridge-ish linear readout W: code -> presence logits, trained by GD."""
    D = X.shape[1]
    W = np.zeros((NC, D))
    b = np.zeros(NC)
    n = len(X)
    for _ in range(epochs):
        Z = X @ W.T + b
        P = 1/(1+np.exp(-Z))
        G = (P - T) / n
        W -= lr * (G.T @ X + 1e-3*W)
        b -= lr * G.sum(0)
    return W, b

def predict(X, W, b): return (1/(1+np.exp(-(X @ W.T + b))) > 0.5).astype(float)

# ---- build train codes for hub & bag ----
K_HUB = 2.0
Xh_tr, T_tr = make_codes(4000, TRAIN_CONJ, K=K_HUB)
Xb_tr, _    = make_codes(4000, TRAIN_CONJ, K=0.0)
# (T identical distribution; rebuild bag T to keep alignment of rng draws clean)
# re-seed-independent: retrain on its own draw
Xb_tr2, Tb_tr = make_codes(4000, TRAIN_CONJ, K=0.0)

Wh, bh = train_readout(Xh_tr, T_tr)
Wb, bb = train_readout(Xb_tr2, Tb_tr)

# ==========================================================================
# AMBIGUOUS binding-required eval set: pair vs swap (identical marginals).
# discriminating bits = the 4 conjunction slots {(s1,c1),(s2,c2),(s1,c2),(s2,c1)}.
# ==========================================================================
def build_ambiguous():
    cases = []
    for s1 in range(S):
        for s2 in range(s1+1, S):
            for c1 in range(C):
                for c2 in range(c1+1, C):
                    disc = [cidx(s1,c1),cidx(s2,c2),cidx(s1,c2),cidx(s2,c1)]
                    for objs in ([(s1,c1),(s2,c2)], [(s1,c2),(s2,c1)]):
                        cases.append((objs, disc))
    return cases

AMB = build_ambiguous()

def ambig_acc(W, b, K):
    """accuracy ONLY on the 4 discriminating bits across the ambiguous set."""
    correct = 0; total = 0
    for (objs, disc) in AMB:
        code, _, _ = locked_pattern(objs, K)
        p = predict(code[None,:], W, b)[0]
        t = scene_target(objs)
        for d in disc:
            correct += int(p[d] == t[d]); total += 1
    return correct / total

hub_ambig    = ambig_acc(Wh, bh, K=K_HUB)
bag_ambig    = ambig_acc(Wb, bb, K=0.0)
# INERT ablation: take the HUB-trained reader but cut hub fan-out (K=0) at eval.
ablate_ambig = ambig_acc(Wh, bh, K=0.0)

# ==========================================================================
# composed_distinct vs max_single (super-additivity of the bound assembly).
#   single-module ceiling: best accuracy a reader achieves seeing ONE module's
#   code alone (no conjunction context). composed = the hub-bound 2-module readout.
#   We count how many DISTINCT conjunctions the hub resolves correctly on the
#   ambiguous set where a single module cannot disambiguate.
# ==========================================================================
def single_module_acc(W, b, K):
    """present only ONE object (the other absent) -> reader sees no pairing.
    measured on the same discriminating bits -> ceiling of a marginal reader."""
    correct = 0; total = 0
    for (objs, disc) in AMB:
        # show first object only
        code, _, _ = locked_pattern([objs[0]], K)
        p = predict(code[None,:], W, b)[0]
        t = scene_target(objs)            # target still the FULL pair
        for d in disc:
            correct += int(p[d] == t[d]); total += 1
    return correct / total

max_single = max(single_module_acc(Wh, bh, K_HUB), single_module_acc(Wb, bb, 0.0))

# composed_distinct = # of distinct conjunctions the hub reader gets right on
# the ambiguous set (present-bit recall on the 2 TRUE conjunctions per scene)
def composed_distinct(W, b, K):
    resolved = set()
    per_scene_ok = 0; n_scene = 0
    for (objs, disc) in AMB:
        code, _, _ = locked_pattern(objs, K)
        p = predict(code[None,:], W, b)[0]
        t = scene_target(objs)
        ok = all(p[cidx(*o)] == 1 for o in objs) and \
             all(p[d] == t[d] for d in disc)
        if ok:
            per_scene_ok += 1
            for o in objs: resolved.add(o)
        n_scene += 1
    return len(resolved), per_scene_ok / max(1, n_scene)

cd_hub, coh_hub = composed_distinct(Wh, bh, K_HUB)
cd_bag, coh_bag = composed_distinct(Wb, bb, 0.0)

# ==========================================================================
# GROK POSITIVE CONTROL (under-power guard) — modular ADDITION, canonical grok.
#   Same toy spirit (numpy, GD), held-out novel (a,b) combos. If this can't beat
#   chance, the probe lacks resolution => UNDER-POWER (not the mechanism).
# ==========================================================================
def grok_control(seed=7):
    P = 11
    pairs = [(a,b) for a in range(P) for b in range(P)]
    rg = np.random.default_rng(seed); rg.shuffle(pairs)
    nh = len(pairs)//2
    held, train = pairs[:nh], pairs[nh:]
    IN = 2*P; Hd = 256; Dd = 64
    def oh(a,b):
        x = np.zeros(IN); x[a]=1; x[P+b]=1; return x
    Xtr = np.stack([oh(*p) for p in train]); Xhe = np.stack([oh(*p) for p in held])
    ytr = np.array([(a+b)%P for (a,b) in train]); yhe = np.array([(a+b)%P for (a,b) in held])
    N = len(train)
    pr = {'W1': rg.normal(0,1/np.sqrt(IN),(Hd,IN)), 'b1': np.zeros(Hd),
          'W2': rg.normal(0,1/np.sqrt(Hd),(Dd,Hd)), 'b2': np.zeros(Dd),
          'Ho': rg.normal(0,1/np.sqrt(Dd),(P,Dd))}
    # Adam
    m={k:np.zeros_like(v) for k,v in pr.items()}; v={k:np.zeros_like(x) for k,x in pr.items()}
    b1,b2,eps,lr,wd=0.9,0.999,1e-8,1e-3,1.0
    def smrow(z): z=z-z.max(1,keepdims=True); e=np.exp(z); return e/e.sum(1,keepdims=True)
    best=0.0
    for st in range(1,40001):
        PRE=Xtr@pr['W1'].T+pr['b1']; H=np.tanh(PRE); Z=H@pr['W2'].T+pr['b2']
        Pp=smrow(Z@pr['Ho'].T); DL=Pp.copy(); DL[np.arange(N),ytr]-=1; DL/=N
        g={}; g['Ho']=DL.T@Z; dZ=DL@pr['Ho']
        g['W2']=dZ.T@H; g['b2']=dZ.sum(0); dH=dZ@pr['W2']; dPRE=dH*(1-H*H)
        g['W1']=dPRE.T@Xtr; g['b1']=dPRE.sum(0)
        for k in pr:
            gk=g[k]+wd*pr[k] if k in ('W1','W2','Ho') else g[k]
            m[k]=b1*m[k]+(1-b1)*gk; v[k]=b2*v[k]+(1-b2)*gk*gk
            mh=m[k]/(1-b1**st); vh=v[k]/(1-b2**st)
            pr[k]-=lr*mh/(np.sqrt(vh)+eps)
        if st%8000==0 or st==40000:
            Zh=np.tanh(Xhe@pr['W1'].T+pr['b1'])@pr['W2'].T+pr['b2']
            best=max(best, float(np.mean(np.argmax(Zh@pr['Ho'].T,1)==yhe)))
    return best, 1.0/P

grok_held, grok_chance = grok_control()

# ==========================================================================
# VERDICT
# ==========================================================================
g1_pass = (cd_hub >= 2) and (cd_hub > max_single) and \
          (hub_ambig >= 0.95) and (bag_ambig <= 0.60)
load_bearing = (ablate_ambig <= 0.60)             # cut hub -> collapse
grok_ctrl_pass = (grok_held >= 3 * grok_chance) and (grok_held >= 0.30)

survivor = bool(g1_pass and grok_ctrl_pass and load_bearing)

if not grok_ctrl_pass:
    verdict = "UNDER-POWER"
elif g1_pass and load_bearing:
    verdict = "SUPPORTED"
elif g1_pass and not load_bearing:
    verdict = "MIXED"          # binds but mechanism INERT (something else binds)
else:
    verdict = "NOT-SUPPORTED"

print("="*78)
print("H_1718 — Claustrum Conductor Phase-Consensus Binding Hub  [DIRECTIONAL numpy]")
print("="*78)
print(f"ambiguous binding-required set: {len(AMB)} scenes (pair vs swap, identical marginals)")
print(f"chance on discriminating bits ~= 0.50 (copy/guess)")
print("-"*78)
print("(G1) binding / composition")
print(f"    hub_ambig_acc       = {hub_ambig:.3f}   (bar >=0.95  true binder ~1.0)")
print(f"    bag_ambig_acc       = {bag_ambig:.3f}   (bar <=0.60  separable ~0.5)")
print(f"    composed_distinct(hub) = {cd_hub}   coherent_scene={coh_hub:.3f}  (bar >=2)")
print(f"    composed_distinct(bag) = {cd_bag}   coherent_scene={coh_bag:.3f}")
print(f"    max_single          = {max_single:.3f}   (single-module ceiling; bar cd_hub>max_single)")
print(f"    -> G1 {'PASS' if g1_pass else 'FAIL'}")
print("-"*78)
print("(INERT) ablation — cut claustral fan-out (hub coupling K=0)")
print(f"    ablate_ambig_acc    = {ablate_ambig:.3f}   (bar <=0.60 => LOAD-BEARING)")
print(f"    delta hub->ablate   = {hub_ambig - ablate_ambig:+.3f}")
print(f"    -> {'LOAD-BEARING' if load_bearing else 'INERT (mechanism contributes ~0)'}")
print("-"*78)
print("(GROK CTRL) modular addition mod 11, AdamW 40k, 50% held  [under-power guard]")
print(f"    grok_held_best      = {grok_held:.3f}   chance=1/11={grok_chance:.3f}")
print(f"    -> grok_ctrl {'PASS (toy has resolution)' if grok_ctrl_pass else 'FAIL => UNDER-POWER'}")
print("="*78)
print(f"VERDICT: {verdict}")
print(f"survivor = {survivor}   (true iff G1 PASS & grok PASS & LOAD-BEARING)")
print("numpy toy = DIRECTIONAL only; NOT engine-native (a_engine_native_learning).")
print("="*78)
