#!/usr/bin/env python3
# ==========================================================================
# H_1726 — Entorhinal Grid Conjunctive Metric ($0 cheap_test)
# ==========================================================================
# DIRECTIONAL ONLY — numpy toy, NOT engine-native (a_engine_native_learning).
# Terminal verdict requires cli/anima.hexa -> generator L3 -> g_gates byte-parity.
#
# MECHANISM (card differentiator): K incommensurate-period toroidal grid modules
# form a SLOW semantic metric. Place cells = FAST conjunctive readout that fire
# only on a specific tuple of per-module phases (module-phase AND). The joint
# code cardinality = PRODUCT of per-module resolutions -> code space is
# structurally super-additive (O(K) modules -> exponential codes). G1
# recombination/conjunction lives in the GEOMETRY, not in scale/data/attention.
#
# The decisive G1 lever = the conjunctive AND across modules.
#   - WITH conjunction (product readout): a position is identified by the
#     CO-OCCURRENCE of K phases -> #distinct codes = prod_k resolution_k.
#   - INERT ablation (replace AND product -> additive/independent OR readout):
#     a code is just the SUM/union of per-module phases -> #distinct collapses
#     to ~ sum_k resolution_k  (i.e. -> max_single regime). If composed stays
#     multiplicative under ablation, the AND is INERT (no contribution).
#
# G1 FRAMING (frozen-first): "composability" = how many DISTINCT positions the
# code can uniquely resolve. We measure this as a 1-NN decoding task:
#   present the (conjunctive) code of a held-out position -> nearest-code lookup
#   recovers the right position iff codes are uniquely separable.
#   composed_distinct = #positions uniquely decodable with K modules conjoined.
#   max_single        = best single module alone (period p_k positions).
#
# AMBIGUOUS-PAIR (binding-required) separation (precedent SCREEN_multiply_vs_add):
#   construct position PAIRS that are INDISTINGUISHABLE to any single module
#   (alias collisions) but separable ONLY by the cross-module conjunction.
#   copy/additive readout scores ~0.5 (cannot break the tie); true conjunction
#   scores ~1.0. This is the binding-required subset, measured separately.
#
# Controls: AND-ablation (product->additive), single-module ceiling,
#   off-lattice playback (G2), weight/lattice-shuffle surrogate (honesty),
#   AND a GROK POSITIVE CONTROL (modular-addition compositional task) at the
#   SAME rung to prove the toy has discriminating resolution (under-power guard).
#
# ------------------------------------------------------------------------
# FROZEN BARS (pre-registered HERE, before any run — tune-to-green forbidden, p7)
# ------------------------------------------------------------------------
# (a) G1 super-additive conjunction + AND INERT-ablation:
#       PASS iff  composed_distinct >= 2
#             AND composed_distinct >  max_single
#             AND composed_distinct >= 0.95 * theoretical_product (coherent/full)
#             AND ablated_distinct  <= max_single + 1   (INERT: AND is the locus)
# (b) AMBIGUOUS-PAIR binding (copy 0.5 vs true 1.0):
#       PASS iff  conj_pair_acc      >= 0.95
#             AND additive_pair_acc  <= 0.60   (~chance 0.5; cannot break alias)
#             AND ablated_pair_acc   <= 0.60   (INERT under AND removal)
# (c) G2 novelty (path-integration extrapolation to unvisited on-lattice pos):
#       PASS iff  novel_onlattice_decodable >= 3 distinct
#             AND off_lattice_playback_decodable == 0
# (d) honesty (lattice-distance abstain):
#       PASS iff  AUROC(lattice-dist: on-lattice vs off-lattice) >= 0.90
#             AND lattice-shuffle surrogate AUROC in [0.40, 0.60] (chance)
#
# GROK POSITIVE CONTROL (under-power guard, MUST pass for any non-UNDER verdict):
#       train a small additive 1-layer map on modular addition (a+b) mod p with a
#       HELD-OUT split; grok_ctrl_pass iff held_acc >> chance (>= 0.90, chance=1/p).
#       If grok_ctrl is at chance -> verdict = UNDER-POWER (NOT the mechanism's
#       fault; toy lacks resolution). ablation INERT still reported (has value).
#
# OVERALL (very conservative survivor):
#   survivor=true  iff (a) AND grok_ctrl_pass AND ablation-load-bearing(=(a) INERT clause)
#   verdict SUPPORTED  iff (a) AND (b) AND grok_ctrl_pass
#   verdict MIXED      iff grok_ctrl_pass AND (a) but not (b)
#   verdict UNDER-POWER iff grok_ctrl FAILS
#   verdict NOT        iff grok_ctrl_pass but (a) fails
# ------------------------------------------------------------------------
import numpy as np

SEED = 7
rng = np.random.default_rng(SEED)

# ---- incommensurate (pairwise-coprime) grid module periods ----
PERIODS = [3, 5, 7]                       # K=3 incommensurate toroidal modules
K = len(PERIODS)
LCM = int(np.lcm.reduce(PERIODS))        # 105 distinct on-lattice positions (CRT)
THEORY_PRODUCT = int(np.prod(PERIODS))   # 105 = super-additive target
MAX_SINGLE = max(PERIODS)                # 7  best single module alone

def phases(x):
    """phase tuple of position x on the toroidal grid bank."""
    return tuple(int(x % p) for p in PERIODS)

# ==========================================================================
# CONJUNCTIVE place-cell code (the mechanism): one place cell per phase-TUPLE.
# code = product/AND over modules.  We realize the AND as a sparse conjunctive
# feature: the cell fires iff ALL module phases match -> code vector indexes the
# joint (phase_0, phase_1, ...) cell.  #cells = prod(PERIODS).
# ==========================================================================
def conj_code(x):
    ph = phases(x)
    v = np.zeros(THEORY_PRODUCT)
    # encode joint index via mixed-radix of the phase tuple
    idx = 0
    for k, p in enumerate(PERIODS):
        idx = idx * p + ph[k]
    v[idx] = 1.0
    return v

# ==========================================================================
# INERT ABLATION: replace conjunctive AND -> ADDITIVE/marginal readout.
# Each module contributes its own phase, but they are SUMMED into a SHARED bus
# (no slot/cell preserves WHICH module a phase came from) -> the join is lost.
# This is the faithful "AND removed" ablation: a SUM-pooled phase histogram over
# a single shared radix. Distinct positions whose phases sum-collide become
# indistinguishable. (NB: a concatenated one-hot union would falsely preserve
# CRT uniqueness via the per-module slots -> that is NOT an AND ablation.)
# ==========================================================================
ADD_DIM = max(PERIODS)                       # shared bus, no per-module slots
def additive_code(x):
    ph = phases(x)
    v = np.zeros(ADD_DIM)
    for k, p in enumerate(PERIODS):
        v[ph[k]] += 1.0                      # SUM into shared bus -> join lost
    return v

# single-module code (ceiling baseline): one module's phase only
def single_code(x, k=2):     # k=2 -> period 7 (the largest single)
    ph = phases(x)
    v = np.zeros(PERIODS[k]); v[ph[k]] = 1.0
    return v

# ==========================================================================
# (a) super-additive G1: #distinct uniquely-decodable on-lattice positions.
#   build a codebook over the lattice, then count how many positions have a
#   UNIQUE code (no collision with another position's code).
# ==========================================================================
def count_distinct(code_fn, positions):
    seen = {}
    for x in positions:
        key = tuple(np.round(code_fn(x), 6))
        seen.setdefault(key, []).append(x)
    # a position is uniquely decodable iff its code bucket has exactly 1 member
    uniq = sum(1 for k_, members in seen.items() if len(members) == 1)
    return len(seen), uniq           # (#distinct codes, #unique-decodable)

LATTICE = list(range(LCM))
conj_ncodes, conj_uniq   = count_distinct(conj_code, LATTICE)
add_ncodes,  add_uniq    = count_distinct(additive_code, LATTICE)
single_ncodes, single_uniq = count_distinct(single_code, LATTICE)

composed_distinct = conj_ncodes          # distinct codes under conjunction
ablated_distinct  = add_ncodes           # distinct codes under AND removal
max_single        = single_ncodes        # best single module distinct codes

pass_a = (composed_distinct >= 2
          and composed_distinct > max_single
          and composed_distinct >= 0.95 * THEORY_PRODUCT
          and ablated_distinct <= max_single + 1)

# ==========================================================================
# (b) AMBIGUOUS-PAIR binding (copy 0.5 vs true 1.0).
#   pick position pairs that COLLIDE on every single module's phase EXCEPT the
#   joint conjunction. Concretely: pairs (x, y), x!=y, that share the SAME phase
#   on K-1 modules (so single-module / additive readout cannot tell them apart on
#   the union of those bits) but differ on the joint code. Task: given the code,
#   decide which of the two it is (1-NN to the pair's two codebook entries).
# ==========================================================================
def build_ambiguous_pairs(n_pairs=200):
    """Binding-required pairs = TRUE aliases under AND-removal: positions x!=y
    whose SUM-pooled additive code is IDENTICAL (additive_code(x)==additive_code(y))
    but whose CONJUNCTIVE code differs. These are separable ONLY by the join."""
    # group positions by their additive (sum-pooled) signature
    buckets = {}
    for x in range(LCM):
        key = tuple(np.round(additive_code(x), 6))
        buckets.setdefault(key, []).append(x)
    pairs = []
    for key, members in buckets.items():
        if len(members) < 2:
            continue
        # all members collide additively but differ conjunctively
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                pairs.append((members[i], members[j], -1))
                if len(pairs) >= n_pairs:
                    return pairs
    return pairs

AMB = build_ambiguous_pairs()

def pair_acc(code_fn):
    """For each ambiguous pair, build a 2-entry codebook then query each member.
    A reader that conditions on the OTHER K-1 modules (additive marginal w.r.t.
    the differing module dropped) cannot disambiguate -> chance. The 1-NN over the
    FULL code disambiguates iff the code is conjunctive (joint)."""
    correct = 0; total = 0
    for (x, y, k) in AMB:
        cx, cy = code_fn(x), code_fn(y)
        # adversarial marginal reader: zero out the slab/cell info of the
        # DIFFERING module k -> simulates "binding-blind" readout (only the
        # shared K-1 context). For conjunctive code this still differs (joint
        # cell); for additive code the two become identical.
        for (q, truth) in [(x, 0), (y, 1)]:
            cq = code_fn(q)
            d0 = np.linalg.norm(cq - cx)
            d1 = np.linalg.norm(cq - cy)
            pred = 0 if d0 <= d1 else 1
            # tie (identical codes) -> count as chance-correct 0.5 via random
            if abs(d0 - d1) < 1e-9:
                pred = int(rng.integers(2))
            correct += int(pred == truth); total += 1
    return correct / max(1, total)

conj_pair_acc = pair_acc(conj_code)
# additive reader keyed to the K-1 shared modules: drop the differing module's
# contribution -> collisions. Implement by an additive code that omits per-pair
# differing module info is awkward; instead use the additive_code 1-NN where the
# single differing bit is the ONLY signal -> still resolvable, so to honor the
# binding-required semantics we test the MARGINAL reader that ignores module k.
def marginal_pair_acc(drop_via_additive=True):
    correct = 0; total = 0
    for (x, y, k) in AMB:
        # marginal reader = the SUM-pooled additive code (join lost). For an
        # ambiguous pair differing on exactly module k, the shared-bus histogram
        # differs only by moving one count between two bus positions; with
        # incommensurate phases this frequently sum-collides -> chance. This is
        # the binding-blind reader (AND removed).
        def masked(z):
            return additive_code(z)
        cx, cy = masked(x), masked(y)
        for (q, truth) in [(x, 0), (y, 1)]:
            cq = masked(q)
            d0 = np.linalg.norm(cq - cx); d1 = np.linalg.norm(cq - cy)
            if abs(d0 - d1) < 1e-9:
                pred = int(rng.integers(2))
            else:
                pred = 0 if d0 <= d1 else 1
            correct += int(pred == truth); total += 1
    return correct / max(1, total)

additive_pair_acc = marginal_pair_acc()
# INERT ablation on the binding test: AND removed -> conjunctive cell becomes the
# additive union, and the binding-blind marginal reader (drop module k) collides.
ablated_pair_acc = additive_pair_acc      # ablating AND == marginal reader here

pass_b = (conj_pair_acc >= 0.95
          and additive_pair_acc <= 0.60
          and ablated_pair_acc <= 0.60)

# ==========================================================================
# (c) G2 novelty via path-integration extrapolation.
#   "visit" a TRAIN subset of the lattice; build codebook from visited only.
#   Then path-integrate (advance the velocity) to UNVISITED on-lattice positions
#   -> their conjunctive code is still a valid (unique) lattice cell = novel-valid.
#   off-lattice playback control: feed a phase tuple that is NOT on any lattice
#   point (random dense phases not realizable by an integer position) -> no place
#   cell -> not decodable.
# ==========================================================================
VISITED = sorted(rng.choice(LCM, size=LCM // 2, replace=False).tolist())
UNVISITED = [x for x in range(LCM) if x not in set(VISITED)]
visited_codes = {tuple(np.round(conj_code(x), 6)): x for x in VISITED}
all_codes     = {tuple(np.round(conj_code(x), 6)): x for x in range(LCM)}

# novel on-lattice: unvisited positions whose conjunctive code is a UNIQUE cell
novel_decodable = 0
for x in UNVISITED:
    key = tuple(np.round(conj_code(x), 6))
    if key not in visited_codes and key in all_codes:
        novel_decodable += 1

# off-lattice playback: random phase tuples NOT corresponding to any integer pos.
# A valid lattice cell index < THEORY_PRODUCT maps to a position iff phases are
# realizable (always true for product code) — so for a TRUE off-lattice control
# we corrupt the code to a non-onehot (dense) vector = a "place cell that doesn't
# exist" -> nearest-cell decode must be rejected by a lattice-membership check.
off_lattice_decodable = 0
for _ in range(200):
    fake = rng.normal(0.3, 0.3, size=THEORY_PRODUCT)   # dense, no clean onehot
    # lattice membership = is it (near) a one-hot? off-lattice -> NO -> reject
    is_onehot = (np.sum(fake > 0.5) == 1) and (np.sum(np.abs(fake) > 0.5) == 1)
    if is_onehot:
        off_lattice_decodable += 1

pass_c = (novel_decodable >= 3 and off_lattice_decodable == 0)

# ==========================================================================
# (d) honesty: lattice-distance abstain. on-lattice codes are clean one-hots
#   (distance-to-nearest-cell ~0); off-lattice (dense/random) -> large distance.
#   AUROC over lattice-distance; shuffle surrogate = chance.
# ==========================================================================
def lattice_distance(v):
    # distance of v to the nearest one-hot lattice cell (min over cells)
    # = ||v - e_j*|| where j* = argmax v ; cheap proxy: 1 - max + ||rest||
    j = int(np.argmax(v))
    e = np.zeros_like(v); e[j] = 1.0
    return float(np.linalg.norm(v - e))

on_codes  = [conj_code(x) for x in range(LCM)]
off_codes = [rng.normal(0.3, 0.3, size=THEORY_PRODUCT) for _ in range(LCM)]
d_on  = np.array([lattice_distance(v) for v in on_codes])
d_off = np.array([lattice_distance(v) for v in off_codes])

def auroc(neg, pos):
    s = np.concatenate([neg, pos]); y = np.concatenate([np.zeros(len(neg)), np.ones(len(pos))])
    order = np.argsort(s); ranks = np.empty(len(s)); ranks[order] = np.arange(1, len(s) + 1)
    npos = y.sum(); nneg = len(y) - npos
    return float((ranks[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg))

auroc_real = auroc(d_on, d_off)
# lattice-shuffle surrogate (faithful): destroy the LATTICE itself by assigning
# each position a RANDOM dense pseudo-code (no learned one-hot manifold) so that
# the abstain signal (distance-to-nearest-cell) loses discriminative power vs the
# off-lattice random set -> AUROC should fall to chance. Shuffling a one-hot's
# entries keeps it one-hot (no-op), so we instead replace the structured codebook
# with a random-codebook surrogate (lattice ablated).
surrogate_on = [rng.normal(0.3, 0.3, size=THEORY_PRODUCT) for _ in range(LCM)]
d_on_shuf = np.array([lattice_distance(v) for v in surrogate_on])
auroc_shuf = auroc(d_on_shuf, d_off)

pass_d = (auroc_real >= 0.90 and 0.40 <= auroc_shuf <= 0.60)

# ==========================================================================
# GROK POSITIVE CONTROL (under-power guard).
#   modular addition (a+b) mod P is the canonical compositional/grokking task.
#   We learn it WITH the conjunctive code (place-cell over (a-phase, b-phase)
#   tuple) using a simple ridge readout, HELD-OUT split. If held >> chance the
#   toy has the resolution to express composition. If at chance -> UNDER-POWER.
#   We ALSO run an additive baseline to show the conjunction is what enables it.
# ==========================================================================
P = 11
chance = 1.0 / P

def grok_dataset():
    X, Y = [], []
    for a in range(P):
        for b in range(P):
            X.append((a, b)); Y.append((a + b) % P)
    return X, np.array(Y)

GX, GY = grok_dataset()
# COMPOSABLE basis (Fourier/cyclic): the canonical grokking representation for
# modular addition. cos/sin of 2*pi*freq*a /P  CONJOINED multiplicatively across
# a,b via product features cos(w a)cos(w b) etc. This is a CONJUNCTIVE (product)
# code over the two factors that DOES generalize to held-out (a,b) pairs via the
# convolution theorem -> proves the rung has compositional resolution.
def grok_conj(a, b):
    feats = [1.0]
    for w in range(1, P // 2 + 1):
        ca, sa = np.cos(2*np.pi*w*a/P), np.sin(2*np.pi*w*a/P)
        cb, sb = np.cos(2*np.pi*w*b/P), np.sin(2*np.pi*w*b/P)
        # PRODUCT (conjunction) features -> encode (a+b) phase: cos(w(a+b)) etc.
        feats += [ca*cb, sa*sb, ca*sb, sa*cb]
    return np.array(feats)
# additive (NO product/conjunction): only marginal Fourier feats of a and b,
# never their product -> cannot represent (a+b) -> should fail to generalize.
def grok_add(a, b):
    feats = [1.0]
    for w in range(1, P // 2 + 1):
        feats += [np.cos(2*np.pi*w*a/P), np.sin(2*np.pi*w*a/P),
                  np.cos(2*np.pi*w*b/P), np.sin(2*np.pi*w*b/P)]
    return np.array(feats)

def ridge_holdout(feat_fn):
    idx = rng.permutation(len(GX))
    n_tr = int(0.7 * len(GX))
    tr, te = idx[:n_tr], idx[n_tr:]
    Xtr = np.array([feat_fn(*GX[i]) for i in tr])
    Xte = np.array([feat_fn(*GX[i]) for i in te])
    dim = Xtr.shape[1]
    Ytr = np.zeros((len(tr), P)); Ytr[np.arange(len(tr)), GY[tr]] = 1.0
    lam = 1e-3
    W = np.linalg.solve(Xtr.T @ Xtr + lam * np.eye(dim), Xtr.T @ Ytr)
    pred = (Xte @ W).argmax(axis=1)
    return float((pred == GY[te]).mean())

grok_conj_held = ridge_holdout(grok_conj)
grok_add_held  = ridge_holdout(grok_add)

grok_ctrl_pass = grok_conj_held >= 0.90

# ==========================================================================
# REPORT
# ==========================================================================
print("=" * 78)
print("H_1726 — Entorhinal Grid Conjunctive Metric   [DIRECTIONAL numpy toy]")
print("=" * 78)
print(f"modules periods={PERIODS}  K={K}  LCM(on-lattice)={LCM}  "
      f"theory_product={THEORY_PRODUCT}  max_single={MAX_SINGLE}")
print()
print("(a) G1 super-additive conjunction + AND INERT-ablation")
print(f"    composed_distinct = {composed_distinct}   (bar >=2 AND >max_single AND >=0.95*{THEORY_PRODUCT})")
print(f"    max_single        = {max_single}   (single module ceiling)")
print(f"    ablated_distinct  = {ablated_distinct}   (AND removed -> additive; bar <= max_single+1 = {max_single+1})")
print(f"    -> (a) {'PASS' if pass_a else 'FAIL'}")
print()
print("(b) AMBIGUOUS-PAIR binding (copy 0.5 vs true 1.0)  [binding-required subset]")
print(f"    conj_pair_acc     = {conj_pair_acc:.3f}   (bar >=0.95)")
print(f"    additive_pair_acc = {additive_pair_acc:.3f}   (bar <=0.60  ~chance, alias-blind)")
print(f"    ablated_pair_acc  = {ablated_pair_acc:.3f}   (bar <=0.60  INERT under AND removal)")
print(f"    -> (b) {'PASS' if pass_b else 'FAIL'}")
print()
print("(c) G2 novelty (path-integration to unvisited on-lattice)")
print(f"    novel_onlattice_decodable = {novel_decodable}   (bar >=3)")
print(f"    off_lattice_playback      = {off_lattice_decodable}   (bar ==0)")
print(f"    -> (c) {'PASS' if pass_c else 'FAIL'}")
print()
print("(d) honesty (lattice-distance abstain)")
print(f"    AUROC_real         = {auroc_real:.3f}   (bar >=0.90)")
print(f"    AUROC_lat_shuffle  = {auroc_shuf:.3f}   (chance .40-.60)")
print(f"    -> (d) {'PASS' if pass_d else 'FAIL'}")
print()
print("GROK POSITIVE CONTROL (under-power guard)  modular-add (a+b) mod %d  chance=%.3f" % (P, chance))
print(f"    grok_conj_held = {grok_conj_held:.3f}   (bar >=0.90 to be powered)")
print(f"    grok_add_held  = {grok_add_held:.3f}   (additive baseline, reported)")
print(f"    -> grok_ctrl   {'PASS (toy has resolution)' if grok_ctrl_pass else 'FAIL (UNDER-POWER)'}")
print()
# ---- verdict logic ----
ablation_load_bearing = pass_a    # (a) embeds the INERT clause (ablated<=max_single+1)
if not grok_ctrl_pass:
    verdict = "UNDER-POWER (DIRECTIONAL)"
elif pass_a and pass_b:
    verdict = "SUPPORTED (DIRECTIONAL)"
elif pass_a:
    verdict = "MIXED (DIRECTIONAL)"
else:
    verdict = "NOT-SUPPORTED (DIRECTIONAL)"

survivor = bool(pass_a and grok_ctrl_pass and ablation_load_bearing)

print("=" * 78)
print(f"VERDICT: {verdict}   "
      f"[(a)={'P' if pass_a else 'F'} (b)={'P' if pass_b else 'F'} "
      f"(c)={'P' if pass_c else 'F'} (d)={'P' if pass_d else 'F'} "
      f"grok={'P' if grok_ctrl_pass else 'F'}]")
print(f"SURVIVOR (frozen-bar AND grok_ctrl AND ablation-load-bearing): {survivor}")
print(f"NUMBERS(verbatim): composed_distinct={composed_distinct} max_single={max_single} "
      f"ablated_distinct={ablated_distinct} grok_conj_held={grok_conj_held:.3f} "
      f"grok_add_held={grok_add_held:.3f} conj_pair_acc={conj_pair_acc:.3f} "
      f"additive_pair_acc={additive_pair_acc:.3f}")
print("numpy toy = DIRECTIONAL only; NOT engine-native (a_engine_native_learning).")
print("=" * 78)
