#!/usr/bin/env python3
# H_1870 — 봉합-VDJ 재조합 (suture-VDJ) DIRECTIONAL numpy probe.
# QUESTION (the ONLY thing this answers): does a discrete V-D-J segment
# selection+splice operator make two INDEPENDENT concepts COMPOSABLE
# (composed_distinct on HELD-OUT pairs > additive-nearest floor), a
# DIRECTIONAL signal — NEVER terminal (numpy mirror, no engine, no gradient).
#
# CONTRAST with the WALLED G1 combination-operator family:
#   Hadamard/TPR/HRR/circconv (H_1823) · predictive-coding (H_1816) ·
#   tension (H_1834) are all CONTINUOUS vector binds that collapse to
#   ADDITIVE in an additive trunk (composed_distinct=0). VDJ is a DISCRETE
#   combinatorial select+concat (immune V-D-J), a different mechanism class.
#
# TASK: 2 INDEPENDENT concepts A (K_A) x B (K_B). Target for pair (A,B) is a
#   sequence [V_seg(A), D_junction, J_seg(B)] — A drives the V library, B the
#   J library (concepts are DISJOINT / distant: A never touches J, B never
#   touches V). TRAIN sees only a subset of pairs; TEST = held-out pairs =
#   pure compositional generalization (systematicity). "distant/independent"
#   is enforced: no held-out pair shares BOTH its A and its B with any single
#   train pair — the correct output is never seen as a whole.
#
# BASELINES:
#   (i) ADDITIVE-NEAREST (the anima Voronoi/additive floor, H_1822 alpha/beta):
#       embed A + embed B, sum, retrieve nearest SEEN train pair's whole
#       output. Cannot construct a new whole -> nearest seen != correct.
#   (ii) VDJ operator: select V_seg from A's slot, J_seg from B's slot, splice
#       with D -> constructs the correct held-out whole.
#
# METRIC: composed_distinct = # of DISTINCT held-out pairs whose FULL output
#   sequence is produced EXACTLY correct.
#
# FROZEN BAR (set BEFORE run, not moved):
#   GREEN-DIRECTIONAL iff  vdj_composed_distinct >= additive_floor + 3
#   (margin 3 distinct correct held-out compositions). Expect additive~0.
#   Honest FALSIFIED/floor if VDJ does not clear the margin.
#
# CONTROL (earned, not trivial-concat artifact): SHUFFLE arm permutes the
#   A->V_slot mapping at splice time (wrong library lookup). If VDJ's lift
#   survives shuffle, the "composition" was fake (any concat scores). Earned
#   iff shuffle_composed_distinct <= additive_floor + 1.

import numpy as np
rng = np.random.default_rng(1870)

K_A, K_B = 6, 6                 # 36 pairs total
D = 24                          # embed dim
# each concept -> a UNIQUE segment token id (the "gene segment library")
V_lib = {a: 100 + a for a in range(K_A)}   # V segments driven by concept A
J_lib = {b: 200 + b for b in range(K_B)}   # J segments driven by concept B
D_junc = 50                                # constant D junction token

def target_seq(a, b):
    return (V_lib[a], D_junc, J_lib[b])

# TRAIN = a subset; enforce DISTANT held-out (no held-out pair's (a,b) whole seen)
all_pairs = [(a, b) for a in range(K_A) for b in range(K_B)]
rng.shuffle(all_pairs)
n_train = 18
train = all_pairs[:n_train]
held = all_pairs[n_train:]                  # 18 held-out compositional pairs
train_set = set(train)
# sanity: held-out wholes are genuinely unseen
held = [p for p in held if p not in train_set]

# concept embeddings (random, independent axes -> A and B distant/orthogonal-ish)
EA = rng.standard_normal((K_A, D))
EB = rng.standard_normal((K_B, D))
EA /= np.linalg.norm(EA, axis=1, keepdims=True)
EB /= np.linalg.norm(EB, axis=1, keepdims=True)

# ---- baseline (i): ADDITIVE-NEAREST (Voronoi over seen wholes) ----
train_vecs = np.array([EA[a] + EB[b] for (a, b) in train])
def additive_predict(a, b):
    q = EA[a] + EB[b]
    d = np.linalg.norm(train_vecs - q, axis=1)
    ta, tb = train[int(np.argmin(d))]
    return target_seq(ta, tb)               # returns a SEEN whole

# ---- operator (ii): VDJ select + splice ----
def vdj_predict(a, b, shuffle_map=None):
    va = a if shuffle_map is None else shuffle_map[a]
    return (V_lib[va], D_junc, J_lib[b])     # construct new whole from parts

# shuffle control: DERANGE the A->V slot (no fixed points — a fixed point would
# leak the correct V library and fake an "earned" failure; enforce derangement).
def derangement(n):
    while True:
        p = rng.permutation(n)
        if not np.any(p == np.arange(n)):
            return p
perm = derangement(K_A)
shuffle_map = {a: int(perm[a]) for a in range(K_A)}

def score(predict):
    ok = set()
    for (a, b) in held:
        if predict(a, b) == target_seq(a, b):
            ok.add((a, b))
    return len(ok)

additive_floor      = score(lambda a, b: additive_predict(a, b))
vdj_distinct        = score(lambda a, b: vdj_predict(a, b))
shuffle_distinct    = score(lambda a, b: vdj_predict(a, b, shuffle_map))

MARGIN = 3
green = (vdj_distinct >= additive_floor + MARGIN)
earned = (shuffle_distinct <= additive_floor + 1)

print("H_1870 suture-VDJ recombination — DIRECTIONAL numpy probe")
print(f"  pairs total={K_A*K_B}  train={len(train)}  held-out(distant)={len(held)}")
print(f"  FROZEN BAR: vdj_distinct >= additive_floor + {MARGIN}  (earned iff shuffle <= additive_floor+1)")
print(f"  additive_floor (Voronoi/nearest-seen) composed_distinct = {additive_floor} / {len(held)}")
print(f"  VDJ operator                          composed_distinct = {vdj_distinct} / {len(held)}")
print(f"  SHUFFLE control (wrong V lib)          composed_distinct = {shuffle_distinct} / {len(held)}")
print(f"  lift over additive = {vdj_distinct - additive_floor}")
verdict = "GREEN-DIRECTIONAL (REACHABLE)" if (green and earned) else \
          ("DIRECTIONAL floor (INERT)" if not green else "AMBIGUOUS (unearned/shuffle-passes)")
print(f"  BAR PASS={green}  EARNED(shuffle-collapses)={earned}  => {verdict}")
print("  SCOPE: numpy mirror = DIRECTIONAL by construction, NOT terminal. Shows the")
print("         OPERATOR is compositionally expressive (discrete select+splice");
print("         reaches held-out wholes an additive/Voronoi readout cannot). The")
print("         TRUNK-OBJECTIVE wall (can additive-CE LEARN to emit VDJ selection?)")
print("         is UNTESTED here — that is the H_1602/gamma cost-gated question.")
