# H_6120 — 생태 hybridization ADVERSARIAL DEEPENING (multi-lens controls)
# =============================================================================
# TARGET operator: "disjoint lane 둘의 hybrid lane 이 부모에 없던 조합 형질 담당"
#   = a third 'hybrid' lane holds the combination code by READING two disjoint
#     parent lanes. By construction that is concat(parentA, parentB) followed by
#     per-segment readout — the SAME operator class as H_6112 meiosis-crossover
#     (state/6112_gen_meiosis_crossover/probe.py: child=concat(cA[i],cB[j]),
#      headA reads seg1, headB reads seg2 -> numpy 0->1.0 REACHABLE).
#
# H_6112 already showed: that numpy 1.0 COLLAPSES on the real CLMConvMoE trunk
#   (arch_ab.py -> ARCH_AB_RESULT.txt: reach 0.022, 0/3 seed, train_fit=1.0).
#   So the numpy REACHABLE is a transfer artifact. This deepening asks the
#   COMPLEMENTARY adversarial question: WHY is the numpy 1.0 vacuous? Is it a
#   property of the *hybrid/meiosis mechanism*, or a generic property of
#   disjoint-partition STORAGE (any operator that keeps parents in separate
#   readable boxes)? Three controls:
#
# (C1) GENERIC-NONLINEARITY: replace the specific "hybrid" op with generic
#      nonlinearities over the SAME disjoint concat (tanh, random-proj MLP that
#      MIXES segments, elementwise A*B in shared space). If a generic op ALSO
#      hits the composed bar, the REACHABLE is an artifact of disjointness/
#      nonlinearity-in-general, NOT the ecological-hybrid mechanism -> ARTIFACT.
# (C2) BIND-RECOVERABILITY: fit linear readout C->A_idx and C->B_idx on TRAIN
#      (diagonal) pairs, test recovery on HELD-OUT off-diagonal. distinctness is
#      NECESSARY-not-SUFFICIENT; but note concat passes it TRIVIALLY because it
#      is partitioned STORAGE (parents never mixed) -> recoverability cannot
#      distinguish composition from storage here.
# (C3) SHUFFLE/ABLATION: turn the KEY ingredient (disjointness) OFF -> fold the
#      two segments into a SHARED superposition before readout. Must collapse to
#      the additive floor, proving disjointness (storage), not a learned combiner,
#      is what carries the toy.
#
# FROZEN BAR (set BEFORE run, p7/c9): the hybrid operator SURVIVES as a genuine
#   composition signal ONLY IF all three hold:
#     (A) generic nonlinearities do NOT match it (generic reach << hybrid reach)
#     (B) bind-recoverability beats additive by >= 0.30 AND is non-trivial
#     (C) disjointness-ablation collapses to additive floor (<=0.20)
#   If a GENERIC op matches OR the recoverability is trivial-storage -> ARTIFACT.
#   numpy = DIRECTIONAL by construction, NEVER terminal.
# =============================================================================
import numpy as np
K, DH, ALPHA = 8, 6, 1e-2
SEEDS = [1843, 1844, 1845]
BAR_LIFT, BAR_ADD_FLOOR = 0.30, 0.20

def ridge_fit(X, Y, a):
    d = X.shape[1]
    return np.linalg.solve(X.T@X + a*np.eye(d), X.T@Y)

def reach_disjoint(cA, cB, offd, xform_seg=None):
    """concat + per-segment readout; xform_seg optionally maps each seg (generic op)."""
    I = np.eye(K)
    sA = cA if xform_seg is None else xform_seg(cA)
    sB = cB if xform_seg is None else xform_seg(cB)
    WA = ridge_fit(sA, I, ALPHA); WB = ridge_fit(sB, I, ALPHA)
    ok = 0
    for (i,j) in offd:
        s1 = sA[i]; s2 = sB[j]
        if int(np.argmax(s1@WA))==i and int(np.argmax(s2@WB))==j: ok += 1
    return ok/len(offd)

def reach_shared(cA, cB, offd, combine):
    """both heads read a SHARED combined vector (superposition/mix)."""
    I = np.eye(K)
    Xtr = np.stack([combine(cA[i], cB[i]) for i in range(K)])
    Wa = ridge_fit(Xtr, I, ALPHA); Wb = ridge_fit(Xtr, I, ALPHA)
    ok = 0
    for (i,j) in offd:
        v = combine(cA[i], cB[j])
        if int(np.argmax(v@Wa))==i and int(np.argmax(v@Wb))==j: ok += 1
    return ok/len(offd)

def run(seed):
    rng = np.random.default_rng(seed)
    cA = rng.standard_normal((K,DH)); cA/=np.linalg.norm(cA,axis=1,keepdims=True)
    cB = rng.standard_normal((K,DH)); cB/=np.linalg.norm(cB,axis=1,keepdims=True)
    offd = [(i,j) for i in range(K) for j in range(K) if i!=j]

    # baseline + target
    additive = reach_shared(cA, cB, offd, lambda a,b: a+b)          # floor
    hybrid   = reach_disjoint(cA, cB, offd)                          # target op

    # C1 generic nonlinearities
    g_tanh_disj = reach_disjoint(cA, cB, offd, xform_seg=np.tanh)    # generic over disjoint
    # random-proj MLP that MIXES the two segments then reads (2*DH -> 2*DH tanh)
    P = rng.standard_normal((2*DH, 2*DH))/np.sqrt(2*DH)
    def mlp_reach():
        I=np.eye(K)
        Xtr=np.stack([np.tanh(np.concatenate([cA[i],cB[i]])@P) for i in range(K)])
        Wa=ridge_fit(Xtr,I,ALPHA); Wb=ridge_fit(Xtr,I,ALPHA); ok=0
        for (i,j) in offd:
            v=np.tanh(np.concatenate([cA[i],cB[j]])@P)
            if int(np.argmax(v@Wa))==i and int(np.argmax(v@Wb))==j: ok+=1
        return ok/len(offd)
    g_mlp_mix = mlp_reach()
    g_hadam   = reach_shared(cA, cB, offd, lambda a,b: a*b)          # elementwise shared

    # C2 bind-recoverability from concat C (recover A_idx & B_idx on held-out)
    #   trivially = hybrid reach (same disjoint readout) -> report + trivially label
    recov = hybrid  # C->A_idx and C->B_idx via per-seg readout == hybrid reach
    recov_lift = recov - additive

    # C3 ablation: disjointness OFF -> fold segments into shared superposition
    abl = reach_shared(cA, cB, offd, lambda a,b: a+b)  # == additive (segments merged)
    return dict(additive=additive, hybrid=hybrid, g_tanh_disj=g_tanh_disj,
                g_mlp_mix=g_mlp_mix, g_hadam=g_hadam, recov=recov,
                recov_lift=recov_lift, abl=abl)

print("H_6120 ECOLOGICAL-HYBRIDIZATION adversarial deepening (DIRECTIONAL numpy)")
print("operator == H_6112 meiosis concat/disjoint-read (dup verify + controls)")
print(f"K={K} seg-dim={DH} held-out off-diag/seed={K*(K-1)}")
print("FROZEN BAR: survives iff (generic NOT match) & (recov lift>=.30 nontrivial) & (ablation collapse)")
print("-"*74)
agg={}
for s in SEEDS:
    r=run(s)
    for k,v in r.items(): agg.setdefault(k,[]).append(v)
    print(f"seed {s}: ADD={r['additive']:.3f} HYBRID={r['hybrid']:.3f} | "
          f"C1 tanh-disj={r['g_tanh_disj']:.3f} mlp-mix={r['g_mlp_mix']:.3f} "
          f"hadam={r['g_hadam']:.3f} | C2 recov={r['recov']:.3f} | C3 abl={r['abl']:.3f}")
print("-"*74)
m={k:float(np.mean(v)) for k,v in agg.items()}
print(f"MEAN ADD={m['additive']:.3f} HYBRID={m['hybrid']:.3f}")
print(f"C1 generic: tanh-disjoint={m['g_tanh_disj']:.3f}  mlp-mix={m['g_mlp_mix']:.3f}  hadamard-shared={m['g_hadam']:.3f}")
print(f"C2 bind-recoverability={m['recov']:.3f} (lift vs add {m['recov_lift']:+.3f})")
print(f"C3 disjointness-ablation={m['abl']:.3f} (must collapse ~additive)")
print("-"*74)
# adjudicate
generic_matches = (m['g_tanh_disj'] >= m['hybrid']-0.05) or (m['g_mlp_mix'] >= m['hybrid']-0.05)
recov_ok = m['recov_lift'] >= BAR_LIFT
abl_collapse = m['abl'] <= BAR_ADD_FLOOR
print(f"C1 generic-nonlinearity MATCHES hybrid? {generic_matches}  "
      f"(tanh-disj {m['g_tanh_disj']:.3f} / mlp-mix {m['g_mlp_mix']:.3f} vs hybrid {m['hybrid']:.3f})")
print(f"C2 recoverability beats additive by>=.30? {recov_ok}  BUT trivially==hybrid readout (partitioned STORAGE, not learned combine)")
print(f"C3 ablation collapses to floor? {abl_collapse}")
survives = (not generic_matches) and recov_ok and abl_collapse and False  # storage-trivial recov -> not genuine
print("-"*74)
if generic_matches:
    print("VERDICT: ARTIFACT — a GENERIC nonlinearity over the SAME disjoint concat")
    print("  reaches the composed bar just as well as the 'ecological hybrid' op.")
    print("  The numpy REACHABLE is a property of DISJOINT-PARTITION STORAGE, not the")
    print("  proposed hybrid-lane mechanism. Recoverability is trivially satisfied by")
    print("  storage (parents never mixed) => necessary-not-sufficient, no composition.")
    print("  DUP-CONFIRMED: same operator class as H_6112 (concat/disjoint-read),")
    print("  which ALREADY collapsed on the real CLMConvMoE trunk (0.022, 0/3 seed).")
else:
    print("VERDICT: hybrid op distinct from generic -> would flag for real-trunk rung")
print("numpy = DIRECTIONAL, NEVER terminal. Real wall = trunk recomb-objective (H_1602, already 🧱).")
