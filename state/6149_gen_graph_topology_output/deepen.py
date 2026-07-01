# H_6149 ADVERSARIAL DEEPENING — refute the graph-topology REACHABLE
# ===========================================================================
# Original screen: graph output reaches composed_distinct=1.0 vs additive 0.75.
# It already FAILED the frozen bar (additive not <=0.20), but the graph 1.0 is
# suspiciously clean. HYPOTHESIS OF THIS DEEPENING: the graph 1.0 is a METRIC
# ARTIFACT of COORDINATE SEPARATION (concat: 2x capacity, no superposition),
# not of any "graph/edge combination" MECHANISM. Precedent H_6112: numpy
# REACHABLE 1.0 collapsed to 0.022 on the real CLMConvMoE trunk.
#
# FROZEN BAR (set BEFORE running) — the operator SURVIVES only if ALL hold:
#   (C1) a GENERIC nonlinearity / trivial per-slot store must NOT also reach
#        the graph score at MATCHED capacity. If generic == graph -> ARTIFACT.
#   (C2) BIND-RECOVERABILITY: at FIXED capacity D (same as additive), a linear
#        readout trained on TRAIN pairs must recover BOTH legs on HELD-OUT
#        pairs and beat additive by >= +0.30. (distinctness is necessary,
#        recoverability-under-shared-capacity is the real composition test.)
#   (C3) ABLATION: turning OFF coordinate-separation (force superposition into
#        one slot) must NOT collapse the graph to the additive floor. If it
#        DOES collapse, the "graph mechanism" is inert -> capacity is the cause.
# Default to ARTIFACT if uncertain. numpy == DIRECTIONAL, never terminal.
# ===========================================================================
import numpy as np

K = 8       # concept prototypes
D = 6       # feature dims per slot

def dictionary(seed):
    rng = np.random.default_rng(seed)
    C = rng.standard_normal((K, D))
    C /= np.linalg.norm(C, axis=1, keepdims=True)
    return C

def both_recovered_argmax(C, recA, recB, i, j):
    return int(np.argmax(C @ recA)) == i and int(np.argmax(C @ recB)) == j

def score_by_construction(C):
    """Original graph metric: each leg in its own coord, per-node argmax."""
    pairs = [(i, j) for i in range(K) for j in range(K) if i != j]
    hit = sum(both_recovered_argmax(C, C[i], C[j], i, j) for (i, j) in pairs)
    return hit / len(pairs)

def score_additive_top2(C):
    pairs = [(i, j) for i in range(K) for j in range(K) if i != j]
    hit = 0
    for (i, j) in pairs:
        s = C[i] + C[j]
        top2 = set(np.argsort(C @ s)[-2:].tolist())
        hit += ({i, j} == top2)
    return hit / len(pairs)

# ---- C1: GENERIC per-slot store (NO graph/edge semantics) ------------------
# Identity concat of the two legs with a GENERIC random rotation per slot.
# If this reaches the graph score, "graph topology" adds nothing.
def score_generic_concat(C, seed):
    rng = np.random.default_rng(seed + 777)
    R = rng.standard_normal((D, D))  # generic invertible-ish rotation, no graph meaning
    Rinv = np.linalg.pinv(R)
    pairs = [(i, j) for i in range(K) for j in range(K) if i != j]
    hit = 0
    for (i, j) in pairs:
        # store rotated legs in two separate coords (generic, no edge)
        slotA = C[i] @ R; slotB = C[j] @ R
        recA = slotA @ Rinv; recB = slotB @ Rinv
        hit += both_recovered_argmax(C, recA, recB, i, j)
    return hit / len(pairs)

# ---- C1b: generic nonlinearities at MATCHED (2D) capacity ------------------
# tanh(concat), elementwise-product-augmented concat — do they also reach 1.0?
def score_generic_nonlin(C, mode):
    pairs = [(i, j) for i in range(K) for j in range(K) if i != j]
    # build train set for a linear readout that inverts the nonlinearity to legs
    X = []; YA = []; YB = []
    for (i, j) in pairs:
        if mode == "tanh":
            feat = np.tanh(np.concatenate([C[i], C[j]]))
        elif mode == "mult":
            feat = np.concatenate([C[i] * C[j], C[i] + C[j]])
        X.append(feat); YA.append(C[i]); YB.append(C[j])
    X = np.array(X); YA = np.array(YA); YB = np.array(YB)
    ntr = int(len(X) * 0.7)
    idx = np.arange(len(X)); np.random.default_rng(0).shuffle(idx)
    tr, te = idx[:ntr], idx[ntr:]
    WA = np.linalg.lstsq(X[tr], YA[tr], rcond=None)[0]
    WB = np.linalg.lstsq(X[tr], YB[tr], rcond=None)[0]
    hit = 0
    for k in te:
        recA = X[k] @ WA; recB = X[k] @ WB
        i, j = pairs[k]
        hit += both_recovered_argmax(C, recA, recB, i, j)
    return hit / len(te)

# ---- C2: BIND-RECOVERABILITY at FIXED capacity D, held-out ------------------
# Fair test: compress the composed object into D dims (same budget as one
# concept / as additive), learn linear readouts on TRAIN pairs, test HELD-OUT.
def score_fixedcap_recoverability(C, mode, seed):
    rng = np.random.default_rng(seed + 13)
    pairs = [(i, j) for i in range(K) for j in range(K) if i != j]
    X = []; YA = []; YB = []
    Pi = rng.standard_normal((D, D)); Pj = rng.standard_normal((D, D))  # role bindings
    for (i, j) in pairs:
        if mode == "additive":
            comp = C[i] + C[j]                       # D dims, superposed
        elif mode == "role_bind":                    # role-filler binding, D dims
            comp = C[i] @ Pi + C[j] @ Pj
        elif mode == "circconv":                     # circular convolution, D dims
            comp = np.real(np.fft.ifft(np.fft.fft(C[i]) * np.fft.fft(C[j])))
        elif mode == "graph_fixedcap":               # graph but squeezed to D dims
            comp = (np.concatenate([C[i], C[j]]))[:D] # only half fits -> lossy
        X.append(comp); YA.append(C[i]); YB.append(C[j])
    X = np.array(X); YA = np.array(YA); YB = np.array(YB)
    ntr = int(len(X) * 0.7)
    idx = np.arange(len(X)); np.random.default_rng(1).shuffle(idx)
    tr, te = idx[:ntr], idx[ntr:]
    WA = np.linalg.lstsq(X[tr], YA[tr], rcond=None)[0]
    WB = np.linalg.lstsq(X[tr], YB[tr], rcond=None)[0]
    hit = 0
    for k in te:
        i, j = pairs[k]
        hit += both_recovered_argmax(C, X[k] @ WA, X[k] @ WB, i, j)
    return hit / len(te)

# ---- C3: ABLATION — turn OFF coordinate separation (force superposition) ----
def score_graph_ablate_superpose(C):
    """graph mechanism with its key ingredient (separate coords) OFF:
    both legs written into ONE shared slot -> should collapse to additive."""
    pairs = [(i, j) for i in range(K) for j in range(K) if i != j]
    hit = 0
    for (i, j) in pairs:
        shared = C[i] + C[j]            # separation OFF -> one slot
        recA = shared; recB = shared    # per-node readout now identical
        top2 = set(np.argsort(C @ shared)[-2:].tolist())
        hit += ({i, j} == top2)
    return hit / len(pairs)

seeds = [6149, 6150, 6151]
print("H_6149 ADVERSARIAL DEEPENING — is graph 1.0 a capacity/metric artifact?")
print(f"K={K} D={D}  off-diag pairs/seed={K*(K-1)}")
print("FROZEN BAR: survives iff (C1 generic != graph) AND (C2 fixedcap-bind beats")
print("            additive by >=+0.30 held-out) AND (C3 ablation does NOT collapse)")
print("="*74)

c1_fail = c2_fail = c3_fail = 0
for s in seeds:
    C = dictionary(s)
    graph = score_by_construction(C)
    add   = score_additive_top2(C)
    gen_concat = score_generic_concat(C, s)
    gen_tanh   = score_generic_nonlin(C, "tanh")
    gen_mult   = score_generic_nonlin(C, "mult")
    # C2 fixed-capacity held-out recoverability
    r_add  = score_fixedcap_recoverability(C, "additive", s)
    r_role = score_fixedcap_recoverability(C, "role_bind", s)
    r_conv = score_fixedcap_recoverability(C, "circconv", s)
    r_gfc  = score_fixedcap_recoverability(C, "graph_fixedcap", s)
    best_bind = max(r_role, r_conv, r_gfc)
    # C3 ablation
    abl = score_graph_ablate_superpose(C)

    # verdict components
    c1 = (gen_concat >= graph - 1e-9)          # generic MATCHES graph -> artifact
    c2 = (best_bind - r_add >= 0.30)           # fixed-cap bind beats additive
    c3 = (abl > add - 0.05)                     # ablation did NOT collapse (>= additive)
    c1_fail += c1; c2_fail += (not c2); c3_fail += (not c3)
    print(f"seed {s}:")
    print(f"  graph(by-construction)={graph:.3f}  additive(top2)={add:.3f}")
    print(f"  C1 generic_concat={gen_concat:.3f}  gen_tanh(heldout)={gen_tanh:.3f}  gen_mult={gen_mult:.3f}"
          f"   -> generic MATCHES graph? {c1}")
    print(f"  C2 fixedcap heldout: additive={r_add:.3f} role_bind={r_role:.3f} circconv={r_conv:.3f} "
          f"graph_squeezed={r_gfc:.3f}  best-add={best_bind-r_add:+.3f}  bind>add+0.30? {c2}")
    print(f"  C3 ablation(superpose)={abl:.3f} vs additive={add:.3f}  -> stays up (no collapse)? {c3}")
    print("-"*74)

print("="*74)
survives = (c1_fail == 0) and (c2_fail == 0) and (c3_fail == 0)
print(f"C1 generic-matched-graph on {c1_fail}/3 seeds (any>0 => ARTIFACT)")
print(f"C2 fixedcap-bind FAILED to beat additive on {c2_fail}/3 seeds (any>0 => no real bind)")
print(f"C3 ablation COLLAPSED graph->additive on {3-c3_fail}/3 seeds (collapse => capacity was the cause)")
verdict = "SURVIVES (flag real-trunk rung)" if survives else "ARTIFACT (numpy REACHABLE was a metric/capacity artifact)"
print(f"VERDICT: {verdict}   [numpy = DIRECTIONAL, never terminal]")
print("TRANSFER CAVEAT: even a survivor would need the H_6112 real-trunk gate")
print("(numpy 1.0 -> CLMConvMoE 0.022). This deepening only removes false hope.")
