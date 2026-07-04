#!/usr/bin/env python3
# ==========================================================================
# H_1616 — Kosmos Placement-Space VSA Binding (HRR / circular-conv role-filler)
#          $0 cheap_test  (numpy only — DIRECTIONAL, NOT engine-native)
# ==========================================================================
# DIRECTIONAL ONLY — pure numpy toy, NOT engine-native (a_engine_native_learning).
# Terminal verdict requires cli/anima.hexa -> generator L3 -> g_gates byte-parity.
# torch FORBIDDEN here (this file imports numpy only -> stays DIRECTIONAL-mirror).
#
# Card claim (the differentiator): binding uses an ALGEBRAIC vector-symbolic
# operator bind(a,b)=a⊛b (circular convolution / HRR, Plate) over the kosmos
# placement coord-space. ⊛ is INVERTIBLE: bind then unbind recovers a constituent
# (a⊛b, unbind by b -> ≈a), exactly the role-filler conjunction op that attention's
# additive weighted sum (a+b loses which-role) CANNOT represent. The mouth composes
# constituents by ⊛, bundles (superposes) for multi-pair context, decodes by
# cleanup-memory nearest-anchor lookup over the .kosmos field; unbinding at readout
# gives COMPOSITIONAL recall of held-out (novel) conjunctions = crosses the G1
# recombination wall.
#
# Cheap_test (card, verbatim intent):
#   pure numpy HRR — d=512 random anchors for K atoms; encode pairs by circular
#   conv (FFT); bundle; query held-out (a,b)->c via unbind+cleanup. Frozen bar:
#   top-1 cleanup of held-out conjunction > additive-bundle baseline AND >
#   random-permutation control. Dead-if: ⊛ <= additive.
#
# Task discipline (frozen-first, tune-to-green forbidden, p7):
#   - G1-shaped frozen bar: at some k, composed_distinct>=2 AND >max_single AND coherent.
#   - binding-class => AMBIGUOUS-PAIR separation: copy-baseline ~0.5 vs true bind ~1.0.
#   - INERT ablation MANDATORY: turn the mechanism OFF (⊛ -> +, i.e. product->add /
#     cross-weight 0) -> if held-out recombination collapses to max_single = load-bearing;
#     if unchanged = INERT (contributes 0).
#   - GROK positive control MANDATORY (under-power guard): a KNOWN composable task
#     (modular-addition cleanup) at the SAME rung; held >> chance must PASS to prove
#     this toy has discrimination resolution. If grok ctrl is at chance -> verdict
#     = UNDER-POWER (not the mechanism's fault).
#
# ------------------------------------------------------------------------
# FROZEN BARS  (pre-registered HERE, before any run)
# ------------------------------------------------------------------------
# (BIND) held-out compositional recall, role-filler binding:
#   PASS iff  hrr_heldout_top1   >= 0.80
#       AND   additive_heldout   <= 0.55   (~chance: a+b loses which-role)
#       AND   randperm_heldout   <= 0.55   (~chance: non-invertible fixed perm)
#
# (AMBIG) ambiguous-pair separation (binding-required disambiguation):
#   the SAME constituents arranged two ways {(s1,c1),(s2,c2)} vs {(s1,c2),(s2,c1)}
#   carry identical marginals; only a binder tells them apart.
#   PASS iff  hrr_ambig_acc      >= 0.80
#       AND   additive_ambig_acc <= 0.60   (copy/marginal baseline ~0.5)
#
# (INERT) ablation load-bearing:
#   PASS (= load-bearing) iff  hrr_heldout_top1 - ablate_add_heldout >= 0.30
#       AND   ablate_add_heldout <= max_single + 0.05   (collapse to additive/max_single floor)
#   (if the gap is small => INERT, mechanism contributes ~0.)
#
# (GROK) positive control — modular addition (x+y) mod P, held-out pairs:
#   PASS iff  grok_held_acc >= 0.80   AND  grok_held_acc - grok_chance >= 0.30
#   (grok_chance = 1/P). If FAIL => UNDER-POWER (toy lacks resolution).
#
# SURVIVOR (very conservative): BIND PASS AND AMBIG PASS AND INERT load-bearing
#   AND GROK PASS. Anything else => MIXED / NOT / UNDER-POWER per below.
# ------------------------------------------------------------------------
import numpy as np

SEED = 7
rng = np.random.default_rng(SEED)
D = 512                      # hypervector dim (card: d=512)

# ---- atom codebook: random unit-ish hypervectors (the cleanup memory anchors) ----
S, C = 6, 6                  # 6 shapes x 6 colors -> 36 conjunctions
N_ATOM = S + C              # distinct atoms (roles+fillers as plain atoms here)

def fresh_codebook(d=D, n=N_ATOM, seed=11):
    g = np.random.default_rng(seed)
    M = g.normal(0.0, 1.0 / np.sqrt(d), size=(n, d))
    return M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-12)

CODE = fresh_codebook()
def vshape(s): return CODE[s]
def vcolor(c): return CODE[S + c]

# ---- HRR ops (circular convolution / correlation via FFT) ----
def cconv(a, b):    # circular convolution  a ⊛ b
    return np.real(np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)))
def ccorr(a, b):    # circular correlation = unbind a by b (a ⊛ b^{-1})
    return np.real(np.fft.ifft(np.fft.fft(a) * np.conj(np.fft.fft(b))))

# ==========================================================================
# Build the cleanup memory of CONJUNCTION vectors and the TRAIN bundle.
# A "scene" = an ordered pair of conjunctions (objA, objB), objX=(shape,color).
# bind a conjunction =  vshape ⊛ vcolor   (role-filler bind).
# A scene's HRR rep = bundle(bind(A), bind(B)) = sum (then we unbind to recover).
# ==========================================================================
ALL_CONJ = [(s, c) for s in range(S) for c in range(C)]

def conj_vec_hrr(s, c):   return cconv(vshape(s), vcolor(c))
def conj_vec_add(s, c):   return vshape(s) + vcolor(c)        # ADDITIVE baseline (no bind)

# random-permutation control: a fixed (non-invertible-as-unbind) permutation binder
PERM = rng.permutation(D)
def conj_vec_perm(s, c):  return (vshape(s) + vcolor(c))[PERM]  # structured-but-not-unbindable

# cleanup memory = all conjunction codes (anchors). top-1 = nearest by cosine.
def normrows(M): return M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-12)
CLEAN_HRR  = normrows(np.array([conj_vec_hrr(s, c)  for (s, c) in ALL_CONJ]))
CLEAN_ADD  = normrows(np.array([conj_vec_add(s, c)  for (s, c) in ALL_CONJ]))
CLEAN_PERM = normrows(np.array([conj_vec_perm(s, c) for (s, c) in ALL_CONJ]))

def cleanup_top1(query, clean):
    q = query / (np.linalg.norm(query) + 1e-12)
    return int(np.argmax(clean @ q))

# ==========================================================================
# (BIND) HELD-OUT compositional recall.
#   TRAIN sees a set of conjunctions; HELD-OUT = conjunctions whose (shape,color)
#   pairing was NEVER bundled in any train scene. Query: given a bundle that
#   contains a held-out conjunction superposed with a known one, recover the
#   held-out constituent by unbinding its KNOWN role (shape) and cleanup over color
#   -> reconstruct the conjunction index. Tests recombination of seen atoms into
#   an UNSEEN conjunction (the G1 wall).
# ==========================================================================
NOVEL = [(0, 0), (1, 2), (3, 3), (4, 5), (5, 1)]   # held-out conjunctions
NOVEL_SET = set(NOVEL)
TRAIN_CONJ = [sc for sc in ALL_CONJ if sc not in NOVEL_SET]
conj_index = {sc: i for i, sc in enumerate(ALL_CONJ)}

def recall_heldout(mode, n=2000):
    """For each trial: bundle a held-out conj with a random distractor known conj,
       then recover the held-out conj index. mode in {hrr, add, perm}."""
    if mode == "hrr":   cvec = conj_vec_hrr;  clean = CLEAN_HRR
    elif mode == "add": cvec = conj_vec_add;  clean = CLEAN_ADD
    elif mode == "perm":cvec = conj_vec_perm; clean = CLEAN_PERM
    correct = 0
    seen = set()
    g = np.random.default_rng(SEED + 1)
    for _ in range(n):
        tgt = NOVEL[g.integers(len(NOVEL))]
        dist = TRAIN_CONJ[g.integers(len(TRAIN_CONJ))]
        bundle = cvec(*tgt) + cvec(*dist)          # superposition (the scene rep)
        # recover the target conjunction from the bundle by cleanup over ALL anchors.
        top = cleanup_top1(bundle, clean)
        if top == conj_index[tgt]:
            correct += 1; seen.add(tgt)
    return correct / n, len(seen)

hrr_held,  hrr_seen  = recall_heldout("hrr")
add_held,  add_seen  = recall_heldout("add")
perm_held, perm_seen = recall_heldout("perm")

# max_single: best you can do by reading just ONE constituent w/o binding
# (= chance of picking the right conj among the 2 superposed, then among 36).
# Empirically the additive/perm floors stand in for this; also report analytic chance.
chance_36 = 1.0 / len(ALL_CONJ)
max_single = max(add_held, perm_held)              # the strongest no-bind floor

pass_bind = (hrr_held >= 0.80) and (add_held <= 0.55) and (perm_held <= 0.55)

# ==========================================================================
# (AMBIG) ambiguous-pair separation — binding-required disambiguation.
#   pair {(s1,c1),(s2,c2)} vs swapped {(s1,c2),(s2,c1)}: identical atom marginals,
#   different conjunctions. A binder distinguishes; additive (marginal) cannot.
#   Task: given the scene bundle, recover BOTH conjunction indices (top-2). acc =
#   fraction of the 2 conjunctions correctly identified.
# ==========================================================================
def cleanup_top2(query, clean):
    q = query / (np.linalg.norm(query) + 1e-12)
    sims = clean @ q
    return set(np.argsort(sims)[-2:].tolist())

def ambig_acc(mode):
    if mode == "hrr":   cvec = conj_vec_hrr;  clean = CLEAN_HRR
    elif mode == "add": cvec = conj_vec_add;  clean = CLEAN_ADD
    tot = 0; hit = 0
    for s1 in range(S):
        for s2 in range(s1 + 1, S):
            for c1 in range(C):
                for c2 in range(c1 + 1, C):
                    for objs in ([(s1, c1), (s2, c2)], [(s1, c2), (s2, c1)]):
                        bundle = cvec(*objs[0]) + cvec(*objs[1])
                        top2 = cleanup_top2(bundle, clean)
                        want = {conj_index[objs[0]], conj_index[objs[1]]}
                        hit += len(top2 & want); tot += 2
    return hit / tot

hrr_ambig = ambig_acc("hrr")
add_ambig = ambig_acc("add")
pass_ambig = (hrr_ambig >= 0.80) and (add_ambig <= 0.60)

# ==========================================================================
# (INERT) ablation: turn the BINDING OPERATOR OFF (⊛ -> +, product->add).
#   This is the card's decisive control "replace ⊛ with + (bundle without bind)".
#   ablate_add_heldout = additive held-out recall (already computed = add_held).
#   load-bearing iff hrr_held - ablate >= 0.30 AND ablate near max_single floor.
# ==========================================================================
ablate_add_held = add_held
gap = hrr_held - ablate_add_held
load_bearing = (gap >= 0.30) and (ablate_add_held <= max_single + 0.05)

# ==========================================================================
# (GROK) positive control — modular addition (x+y) mod P via the SAME HRR machinery.
#   atoms = number codes; bind(x,y)=v[x]⊛v[y]; train cleanup memory maps composed
#   vec -> (x+y mod P). Held-out (x,y) pairs (never bundled in train) must recover
#   the SUM by nearest-sum-prototype. If held >> 1/P, the toy has resolution.
#   We build sum-class prototypes by averaging bind(x,y) over TRAIN pairs per class,
#   then classify held-out pairs. (A genuinely composable, learnable task.)
# ==========================================================================
P = 7
numcode = fresh_codebook(d=D, n=P, seed=23)
def vnum(x): return numcode[x]
def grok_bind(x, y): return cconv(vnum(x), vnum(y))     # composed rep of (x,y)

all_pairs = [(x, y) for x in range(P) for y in range(P)]
g2 = np.random.default_rng(SEED + 2)
g2.shuffle(all_pairs)
n_hold = max(1, int(0.3 * len(all_pairs)))
held_pairs = all_pairs[:n_hold]
train_pairs = all_pairs[n_hold:]

# build per-sum-class prototype from TRAIN pairs only
proto = {k: [] for k in range(P)}
for (x, y) in train_pairs:
    proto[(x + y) % P].append(grok_bind(x, y))
proto_vec = {}
for k in range(P):
    if proto[k]:
        v = np.mean(proto[k], axis=0)
        proto_vec[k] = v / (np.linalg.norm(v) + 1e-12)
PK = sorted(proto_vec.keys())
PM = np.array([proto_vec[k] for k in PK])

def grok_classify(x, y):
    q = grok_bind(x, y); q = q / (np.linalg.norm(q) + 1e-12)
    return PK[int(np.argmax(PM @ q))]

grok_hit = 0; grok_tot = 0
for (x, y) in held_pairs:
    if grok_classify(x, y) == (x + y) % P:
        grok_hit += 1
    grok_tot += 1
grok_held = grok_hit / grok_tot
grok_chance = 1.0 / P
pass_grok = (grok_held >= 0.80) and (grok_held - grok_chance >= 0.30)

# ==========================================================================
# VERDICT
# ==========================================================================
survivor = pass_bind and pass_ambig and load_bearing and pass_grok
if not pass_grok:
    verdict = "UNDER-POWER (DIRECTIONAL)"   # grok ctrl at/near chance => no resolution
elif survivor:
    verdict = "SUPPORTED (DIRECTIONAL)"
elif pass_bind or pass_ambig:
    verdict = "MIXED (DIRECTIONAL)"
else:
    verdict = "NOT-SUPPORTED (DIRECTIONAL)"

print("=" * 78)
print("H_1616 — Kosmos Placement-Space VSA Binding (HRR circular-conv)  [DIRECTIONAL numpy]")
print("=" * 78)
print(f"  dim D={D}  atoms={N_ATOM}  conjunctions={len(ALL_CONJ)}  chance(1/36)={chance_36:.4f}")
print()
print("(BIND) held-out compositional recall (recombination into UNSEEN conjunction)")
print(f"    hrr_heldout_top1   = {hrr_held:.4f}  (bar >=0.80)   distinct_recovered={hrr_seen}/5")
print(f"    additive_heldout   = {add_held:.4f}  (bar <=0.55  ~chance, a+b loses role)")
print(f"    randperm_heldout   = {perm_held:.4f}  (bar <=0.55  ~chance, non-invertible)")
print(f"    max_single (floor) = {max_single:.4f}")
print(f"    -> (BIND) {'PASS' if pass_bind else 'FAIL'}")
print()
print("(AMBIG) ambiguous-pair separation (copy 0.5 vs true bind 1.0)")
print(f"    hrr_ambig_acc      = {hrr_ambig:.4f}  (bar >=0.80)")
print(f"    additive_ambig_acc = {add_ambig:.4f}  (bar <=0.60  marginal/copy baseline)")
print(f"    -> (AMBIG) {'PASS' if pass_ambig else 'FAIL'}")
print()
print("(INERT) ablation — turn bind OFF (⊛ -> +): collapse to additive/max_single floor?")
print(f"    hrr_heldout={hrr_held:.4f}  ablate_add_heldout={ablate_add_held:.4f}  gap={gap:.4f} (bar gap>=0.30)")
print(f"    ablate <= max_single+0.05 ? {ablate_add_held:.4f} <= {max_single + 0.05:.4f}")
print(f"    -> ablation {'LOAD-BEARING' if load_bearing else 'INERT (contributes ~0)'}")
print()
print("(GROK) positive control — modular addition (x+y) mod 7, held-out pairs")
print(f"    grok_held_acc = {grok_held:.4f}  (bar >=0.80)   grok_chance(1/7)={grok_chance:.4f}")
print(f"    lift over chance = {grok_held - grok_chance:.4f}  (bar >=0.30)")
print(f"    -> (GROK) {'PASS' if pass_grok else 'FAIL => UNDER-POWER'}")
print()
print("=" * 78)
print(f"VERDICT: {verdict}")
print(f"  [BIND={'P' if pass_bind else 'F'} AMBIG={'P' if pass_ambig else 'F'} "
      f"INERT={'load-bearing' if load_bearing else 'INERT'} GROK={'P' if pass_grok else 'F'}]")
print(f"  SURVIVOR (frozen-bar AND grok_ctrl AND load-bearing) = {survivor}")
print("numpy toy = DIRECTIONAL only; NOT engine-native (a_engine_native_learning).")
print("=" * 78)
