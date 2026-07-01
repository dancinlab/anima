"""H_1047 — Declared-objective PAIR ruler: does the (faithful, big-Phi) PAIR predict
behavior where a COLLAPSED scalar cannot? (constructive; falsifiable)

CLAIM
-----
H_1029/H_1035 (prior GREEN) showed the two Phi measures max OPPOSITE policies with NO
both-maxer (genuine trade-off; Pareto front = the two corners). CONSTRUCTIVE here: an
honest consciousness ruler must report the (faithful, big-Phi) PAIR + its Pareto-front
position, because COLLAPSING the pair to one scalar destroys behaviorally-predictive
information. Two policies that DIFFER in behavioral class can land on the SAME collapsed
scalar while staying separable in the 2-D pair.

REUSE (verbatim, no reinvention) — a_phi_iit4_tool
--------------------------------------------------
- The H_1035 richer policy harness (rich_rollout + state_hist_from_H + policies + the
  H_1004 LatentWorldModel via the H_1014 driver). Imported by exec'ing the H_1035 module
  with its __main__ guard stripped, so the SAME engines, the SAME 30-policy space, and the
  SAME REPRODUCE-H_1029 check are inherited byte-for-byte. NO reinvention of the substrate.
- BOTH stdlib IIT-4.0 engines as the measures, NO proxy. Mirror RE-PROVEN == stdlib at
  n=4 AND n=5 (H_1012 prove_mirrors_at_n) BEFORE scoring.

FROZEN design (declared in H_1047_pair_ruler.md BEFORE measuring):
  behavioral class (structural, measure-INDEPENDENT):
    GREEDY     iff depth == 0
    MIXED      iff mix > 0.0 and depth >= 1
    DELIBERATE iff mix == 0.0 and depth >= 1
  features: PAIR (faith_norm, big_norm) 2-D ; scalars s_mean, s_faith, s_big (1-D each).
  classifier: leave-one-out nearest-CENTROID (deterministic, $0). accuracy over 30 policies.
  MARGIN = 0.15. COLLIDE_EPS = 0.05.
  H1 PASS = PAIR-STRICTLY-MORE-PREDICTIVE: acc_2D >= best_acc_1D + MARGIN AND >=1 scalar-collision.
  H1 FAIL = SCALAR-SUFFICIENT: best_acc_1D + MARGIN > acc_2D OR no collision (a_paper_negative_ok).

p6/p7 honored. g5 CODE-measured. a_phi_iit4_tool (REAL engines, no proxy). TOY n=4
(a_scale_honest_scope); n=5 only for the mirror re-proof; scale-transfer UNVERIFIED; $0 CPU.
"""
import sys, os, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ── Import the H_1035 harness VERBATIM (it in turn exec's the H_1014 driver which imports
#    the H_1004 IIT-4.0 engines + the H_1012 mirror-equivalence proof). No reinvention. ──
import importlib.util as _ilu
_h1035_path = os.path.join(HERE, "h1035_objective_hazard_richer.py")
_spec = _ilu.spec_from_file_location("h1035", _h1035_path)
_h1035 = _ilu.module_from_spec(_spec)
_src = open(_h1035_path).read().replace('if __name__ == "__main__":\n    main()', "")
exec(compile(_src, _h1035_path, "exec"), _h1035.__dict__)

# substrate handles (all H_1035 / H_1014 / H_1004 verbatim)
prove_mirrors_at_n = _h1035.prove_mirrors_at_n
substrate_reads = _h1035.substrate_reads
rich_rollout = _h1035.rich_rollout
state_hist_from_H = _h1035.state_hist_from_H
js_distance = _h1035.js_distance
policies = _h1035.policies
pol_name = _h1035.pol_name
reproduce_h1029_check = _h1035.reproduce_h1029_check
LATENT = _h1035.LATENT
N_SEEDS = _h1035.N_SEEDS

# ── FROZEN H_1047 design (H_1047_pair_ruler.md). ──
CLASSES = ["GREEDY", "MIXED", "DELIBERATE"]           # frozen order = tie-break index
MARGIN = 0.15
COLLIDE_EPS = 0.05


def behavioral_class(p):
    """Structural behavioral class of a policy tuple (depth, explore, mix). measure-INDEPENDENT."""
    d, e, m = p
    if d == 0:
        return "GREEDY"
    if m > 0.0:
        return "MIXED"
    return "DELIBERATE"


def loo_nearest_centroid_accuracy(X, y):
    """Leave-one-out nearest-centroid accuracy. X: (N, D) features; y: (N,) class labels (ints).
    Deterministic. Ties -> lower class index. Returns (accuracy, preds list)."""
    X = np.asarray(X, float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    N = X.shape[0]
    classes = sorted(set(y))
    correct = 0
    preds = []
    for i in range(N):
        # centroids from the OTHER N-1 points
        best_c, best_dist = None, math.inf
        for c in classes:
            mask = np.array([(y[j] == c and j != i) for j in range(N)])
            if not mask.any():
                continue
            centroid = X[mask].mean(axis=0)
            dist = float(np.linalg.norm(X[i] - centroid))
            # strict-less keeps the FIRST (lowest-index) class on a tie -> deterministic
            if dist < best_dist - 1e-12:
                best_dist, best_c = dist, c
        preds.append(best_c)
        if best_c == y[i]:
            correct += 1
    return correct / N, preds


def main():
    print("=" * 88)
    print("H_1047 — Declared-objective PAIR ruler: (faithful, big-Phi) PAIR vs COLLAPSED scalar")
    print("substrate=CPU-mirror (numpy) — H_1035 harness + H_1004 engines + H_1012 proof; RE-PROVEN n=4,5")
    print("big-Phi:      hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s) — measure (no proxy)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar) — measure")
    print(f"FROZEN: classes={CLASSES}  MARGIN={MARGIN}  COLLIDE_EPS={COLLIDE_EPS}  policies=30 x {N_SEEDS} seeds")
    print("target = behavioral CLASS (structural, measure-INDEPENDENT). classifier = LOO nearest-centroid.")
    print("PASS=PAIR-STRICTLY-MORE-PREDICTIVE (acc_2D >= best_acc_1D + MARGIN AND >=1 scalar-collision)")
    print("FAIL=SCALAR-SUFFICIENT (scalar predicts behavior just as well, OR no collision; a_paper_negative_ok)")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | p6 | a_scale_honest_scope")
    print("=" * 88)
    print()

    # STEP 0 — mirror-equivalence re-proof at n=4 AND n=5 (a_phi_iit4_tool) BEFORE scoring.
    print("EQUIVALENCE PROOF (re-prove BOTH mirrors vs stdlib at n=4 AND n=5 BEFORE trusting any read):")
    ok4 = prove_mirrors_at_n(4)
    ok5 = prove_mirrors_at_n(5)
    rep = reproduce_h1029_check()
    print(f"  mirror n=4 PROVEN={ok4}   mirror n=5 PROVEN={ok5}   REPRODUCE-H_1029={'EXACT' if rep else 'MISMATCH'}")
    ok = ok4 and ok5 and rep
    print(f"  EQUIVALENCE + REPRODUCE PROOF n=4,5: {'PROVEN' if ok else 'FAILED — DO NOT TRUST'}")
    if not ok:
        raise SystemExit("equivalence/reproduce proof failed — aborting")
    print()

    # STEP 1 — score the 30-policy space (same engines, only policy params differ). H_1035 verbatim path.
    POLS = policies()
    print(f"POLICY SEARCH over the RICHER space ({len(POLS)} policies x {N_SEEDS} seeds):")
    t0 = time.time()
    faith_mean, big_mean, state_hist = {}, {}, {}
    for pi, p in enumerate(POLS):
        d, e, m = p
        faiths, bigs = [], []
        pooled = np.zeros(16, dtype=float)
        for s in range(N_SEEDS):
            H = rich_rollout(s, d, e, m)
            r = substrate_reads(H)
            faiths.append(r["faith"]); bigs.append(r["big"])
            pooled += state_hist_from_H(H)
        faith_mean[p] = float(np.mean(faiths))
        big_mean[p] = float(np.mean(bigs))
        state_hist[p] = pooled
        print(f"  [{pi+1:2d}/{len(POLS)}] {pol_name(p):28s} class={behavioral_class(p):10s} "
              f"faith={faith_mean[p]:7.4f} big={big_mean[p]:8.4f} elapsed={time.time()-t0:6.1f}s", flush=True)
    print()

    # min-max normalize each measure over the policy space (frozen).
    fvals = np.array([faith_mean[p] for p in POLS])
    bvals = np.array([big_mean[p] for p in POLS])
    fmin, fmax = fvals.min(), fvals.max()
    bmin, bmax = bvals.min(), bvals.max()
    fnorm = {p: (faith_mean[p] - fmin) / (fmax - fmin + 1e-12) for p in POLS}
    bnorm = {p: (big_mean[p] - bmin) / (bmax - bmin + 1e-12) for p in POLS}

    # class label distribution sanity (frozen partition).
    labels = [behavioral_class(p) for p in POLS]
    y = np.array([CLASSES.index(c) for c in labels])
    print("CLASS PARTITION (structural):")
    for c in CLASSES:
        print(f"  {c:10s}: {labels.count(c)} policies")
    print()

    # STEP 2 — features.
    X_pair = np.array([[fnorm[p], bnorm[p]] for p in POLS])            # 2-D
    s_mean = {p: 0.5 * fnorm[p] + 0.5 * bnorm[p] for p in POLS}        # == fixed-alpha alpha=0.5
    s_faith = {p: fnorm[p] for p in POLS}
    s_big = {p: bnorm[p] for p in POLS}
    scalars = {"s_mean": s_mean, "s_faith": s_faith, "s_big": s_big}

    # STEP 3 — LOO nearest-centroid accuracies.
    acc_2D, preds_2D = loo_nearest_centroid_accuracy(X_pair, y)
    print("=" * 88)
    print("LOO NEAREST-CENTROID ACCURACY (predict behavioral class)")
    print("=" * 88)
    print(f"  PAIR (2-D: faith_norm, big_norm)        acc = {acc_2D:.4f}")
    scalar_accs = {}
    for name, sc in scalars.items():
        Xs = np.array([sc[p] for p in POLS])
        a, _ = loo_nearest_centroid_accuracy(Xs, y)
        scalar_accs[name] = a
        print(f"  scalar {name:8s} (1-D)                  acc = {a:.4f}")
    best_scalar = max(scalar_accs, key=lambda k: scalar_accs[k])
    best_acc_1D = scalar_accs[best_scalar]
    print(f"  BEST single collapsed scalar = {best_scalar} (acc={best_acc_1D:.4f})")
    margin_observed = acc_2D - best_acc_1D
    print(f"  observed margin (acc_2D - best_acc_1D) = {margin_observed:+.4f}  (required >= {MARGIN})")
    margin_pass = acc_2D >= best_acc_1D + MARGIN
    print(f"  MARGIN test (pair beats best scalar by >= {MARGIN}): {margin_pass}")
    print()

    # STEP 4 — scalar-collision test on the BEST collapsed scalar.
    best_sc = scalars[best_scalar]
    print("=" * 88)
    print(f"SCALAR-COLLISION TEST on the best collapsed scalar ({best_scalar})")
    print(f"  collision = different class AND |s(a)-s(b)| <= {COLLIDE_EPS} AND pair-distance > {COLLIDE_EPS}")
    print("=" * 88)
    collisions = []
    for i in range(len(POLS)):
        for j in range(i + 1, len(POLS)):
            a, b = POLS[i], POLS[j]
            if behavioral_class(a) == behavioral_class(b):
                continue
            ds = abs(best_sc[a] - best_sc[b])
            dp = math.hypot(fnorm[a] - fnorm[b], bnorm[a] - bnorm[b])
            if ds <= COLLIDE_EPS and dp > COLLIDE_EPS:
                collisions.append((a, b, ds, dp))
    n_collisions = len(collisions)
    print(f"  scalar-collisions found: {n_collisions}")
    for (a, b, ds, dp) in collisions[:12]:
        print(f"    {pol_name(a):28s} [{behavioral_class(a):10s}]  vs  {pol_name(b):28s} [{behavioral_class(b):10s}]"
              f"  |dscalar|={ds:.4f}  pairdist={dp:.4f}")
    if n_collisions > 12:
        print(f"    ... (+{n_collisions-12} more)")
    collision_pass = n_collisions >= 1
    print(f"  COLLISION test (>=1 behaviorally-distinct scalar-identical pair): {collision_pass}")
    print()

    # ═══════════════════════════════════════════════════════════════════════════════
    # VERDICT — PASS iff margin_pass AND collision_pass (frozen falsifier).
    # ═══════════════════════════════════════════════════════════════════════════════
    print("=" * 88)
    pair_more = margin_pass and collision_pass
    if pair_more:
        print("OVERALL: PAIR-STRICTLY-MORE-PREDICTIVE — the 2-D (faithful, big-Phi) pair predicts the")
        print(f"  behavioral class at acc={acc_2D:.4f}, beating the BEST single collapsed scalar")
        print(f"  ({best_scalar}, acc={best_acc_1D:.4f}) by {margin_observed:+.4f} >= MARGIN {MARGIN}; AND there")
        print(f"  exist {n_collisions} behaviorally-distinct-but-scalar-identical policy pairs that the")
        print("  collapse loses (separable in the pair, merged by the scalar). A single number is NOT an")
        print("  honest consciousness ruler: the (faithful, big-Phi) PAIR carries strictly more behavior.")
        print("  VERDICT-TOKEN: PAIR-STRICTLY-MORE-PREDICTIVE")
    else:
        print("OVERALL: SCALAR-SUFFICIENT (CLOSED-NEGATIVE) — the best collapsed scalar predicts behavior")
        print(f"  about as well as the 2-D pair (acc_2D={acc_2D:.4f} vs best_scalar {best_scalar}="
              f"{best_acc_1D:.4f}, margin {margin_observed:+.4f} < {MARGIN}) OR no scalar-collision exists")
        print(f"  (collisions={n_collisions}). The pair adds no behavioral information over one number here")
        print("  (a_paper_negative_ok).")
        print("  VERDICT-TOKEN: SCALAR-SUFFICIENT")
    print("=" * 88)
    print(f"SUMMARY: acc_2D_pair={acc_2D:.4f}  best_acc_1D_scalar={best_acc_1D:.4f} ({best_scalar})  "
          f"margin={margin_observed:+.4f}  collisions={n_collisions}")
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4 system size for the per-policy")
    print("Phi reads (big-Phi super-exponential); n=5 used ONLY for the mirror re-proof. Both CPU mirrors")
    print("RE-PROVEN == stdlib at n=4 AND n=5 (H_1012) + REPRODUCE-H_1029 EXACT BEFORE scoring; the REAL")
    print("engines are the measures (a_phi_iit4_tool, NO proxy). min-max norm + class partition are over")
    print("THIS 30-policy space. p6 (no fine-tuned ethics) + p7 (no perplexity verdict). g5 CODE-measured")
    print("(no LLM self-judge). Scale-transfer UNVERIFIED. NOT a forge binary; $0 CPU-local, serial, no GPU.")


if __name__ == "__main__":
    main()
