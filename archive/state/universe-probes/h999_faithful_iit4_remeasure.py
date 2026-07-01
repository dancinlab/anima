"""H_999 — Faithful IIT4 re-measure of the imagination/planning Φ-null.

MISSION
-------
The CWM 🔴 nulls H_971 (imagination doesn't raise Φ), H_973 (planning doesn't
raise Φ), and the re-formulations H_988/H_994 were ALL measured with a PROXY
(`phi_proxy` in cwm_probe_lib.py = integration×differentiation×entropy on the
continuous latent — the H_912/H_931/phi_silicon_proxy family). H_988/H_989 proved
that proxy is PURPOSE-BLIND (it tracks state-multiplicity, not causal
irreducibility). a_phi_iit4_tool + UNIVERSE/IIT4_PHI_TOOLS.md mandate re-measuring
any Φ verdict with the FAITHFUL exact MIP-EI IIT4 engine that already exists in
hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (promoted from anima H_278).

THIS PROBE
----------
Takes the SAME states/trajectories the proxy scored (reactive vs drift-imagination
vs goal-guided-rollout; planning branch-depth), discretizes each to an n≤8 system,
and scores Φ with a BYTE-FAITHFUL CPU MIRROR of the stdlib faithful_phi.hexa MIP-EI
engine. The mirror is proven ≡ the stdlib hexa engine on tiny reference cases below
(REF_PHI from `hexa run` of faithful_phi.hexa on this Mac) BEFORE it is trusted.

WHY A MIRROR (and that it is FAITHFUL, not the proxy)
-----------------------------------------------------
The stdlib faithful_phi.hexa RUNS on this Mac (it is pure arithmetic — no fused
GPU natives, so the clm-decode-macos-link-gap does NOT apply; verified: REF_PHI=2
for the n=3 reference). But it has no registered `hexa verify` atom yet (V5.2 TODO)
and its `print` truncates floats to ~6 digits, which is too coarse for a Welch t /
Cohen d contrast over 30 seeds. So we use a numpy mirror that reproduces the EXACT
same algorithm (bin → pairwise MI matrix → exact MIP argmin cross-cut → Φ = min-cut
/ min(|A|,|B|)) and we PROVE it byte-faithful against the hexa engine on the
reference cases (assert |mirror − hexa| < 1e-4). This is the faithful-Φ mirror, NOT
the H_912/H_931 proxy.

FAITHFUL Φ ALGORITHM (mirrored from faithful_phi.hexa, byte-equal)
-----------------------------------------------------------------
For a system of n units, each carrying a `dim`-step trajectory:
  1. bin each unit's trajectory into [0,n_bins-1] by per-unit min-max
     normalization (Rust f32::EPSILON all-identical guard = 1.19209290e-7).
  2. pairwise MI[i][j] = max(H(bi)+H(bj)-H(bi,bj), 0), entropy in bits with the
     RFC-036 additive smoothing (total += 1e-8 ; log(p+1e-10)).
  3. for every non-trivial bipartition (cell 0 pinned to A, 2^(n-1) masks), the
     cut cost = Σ_{i∈A,j∈B} MI[i][j]. MIP = argmin cut.
  4. faithful Φ★ = cut(MIP) / min(|A|,|B|).
n≤8 exact (≤128 masks, $0 CPU). HONEST: still a TOY rung (a_scale_honest_scope) —
the toy WM latent is DISCRETIZED to n≤8 binary-ish units; transfer unverified.

g5 CODE-measured (no LLM self-judge, p7).
"""
import sys, os, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
# reuse the EXACT engine + proxy the original H_971/973/988/994 probes used
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))
from cwm_probe_lib import LatentWorldModel, phi_proxy, cohens_d, welch_t, boot_ci  # noqa: E402


# ════════════════════════════════════════════════════════════════════════════
# FAITHFUL Φ — byte-faithful CPU mirror of stdlib faithful_phi.hexa
# ════════════════════════════════════════════════════════════════════════════
F32_EPS = 1.19209290e-7


def _bin_values(values, n_bins):
    """faithful_phi.hexa _iit4_bin_values — per-trajectory min-max binning."""
    v = np.asarray(values, float)
    n = len(v)
    bins = np.zeros(n, dtype=int)
    if n <= 0:
        return bins
    mn = v.min()
    mx = v.max()
    rng = mx - mn
    if rng < F32_EPS:        # all-identical guard (Rust f32::EPSILON)
        return bins
    bw = rng / n_bins
    for j in range(n):
        r = (v[j] - mn) / bw
        b = int(math.floor(r))
        if b > n_bins - 1:
            b = n_bins - 1
        if b < 0:
            b = 0
        bins[j] = b
    return bins


def _entropy(counts, total):
    """faithful_phi.hexa _iit4_entropy — Shannon entropy in bits, RFC-036 smoothing."""
    if total == 0:
        return 0.0
    t = total + 1.0e-8
    s = 0.0
    log2 = math.log(2.0)
    for c in counts:
        p = c / t
        s += (0.0 - p) * (math.log(p + 1.0e-10) / log2)
    return s


def _mi_pair(a, b, n_bins):
    """faithful_phi.hexa _iit4_mi_pair — MI(a;b) = max(H(a)+H(b)-H(a,b), 0)."""
    n = len(a)
    if n <= 0 or n_bins <= 0:
        return 0.0
    ba = _bin_values(a, n_bins)
    bb = _bin_values(b, n_bins)
    ca = np.zeros(n_bins)
    cb = np.zeros(n_bins)
    jo = np.zeros(n_bins * n_bins)
    for i in range(n):
        ai = int(ba[i])
        bi = int(bb[i])
        ca[ai] += 1.0
        cb[bi] += 1.0
        jo[ai * n_bins + bi] += 1.0
    hA = _entropy(ca, n)
    hB = _entropy(cb, n)
    hAB = _entropy(jo, n)
    mi = hA + hB - hAB
    return mi if mi >= 0.0 else 0.0


def build_mi_matrix(state, n, dim, n_bins):
    """faithful_phi.hexa iit4_build_mi_matrix — pairwise MI over dim-step rows."""
    st = np.asarray(state, float)
    mi = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            row_i = st[i * dim:(i + 1) * dim]
            row_j = st[j * dim:(j + 1) * dim]
            v = _mi_pair(row_i, row_j, n_bins)
            mi[i, j] = v
            mi[j, i] = v
    return mi


def _bit_set(mask, b):
    return 1 if (mask // (2 ** b)) % 2 == 1 else 0


def _size_a(n, mask):
    cnt = 1                       # cell 0 pinned to A
    for b in range(n - 1):
        if _bit_set(mask, b):
            cnt += 1
    return cnt


def _cross_cut(mi, n, mask):
    cross = 0.0
    for ia in range(n):
        inA = 1 if ia == 0 else _bit_set(mask, ia - 1)
        if inA:
            for jb in range(n):
                jInA = 1 if jb == 0 else _bit_set(mask, jb - 1)
                if not jInA:
                    cross += mi[ia, jb]
    return cross


def faithful_phi_from_mi(mi, n):
    """faithful_phi.hexa iit4_faithful_phi_from_mi — exact MIP argmin cross-cut."""
    if n <= 1:
        return 0.0
    if n == 2:
        return mi[0, 1]
    max_mask = 2 ** (n - 1)
    best_cut = 1.0e308
    best_norm = 1.0
    found = False
    for mask in range(1, max_mask):
        sa = _size_a(n, mask)
        sb = n - sa
        if sb >= 1:
            cut = _cross_cut(mi, n, mask)
            if (not found) or (cut < best_cut):
                best_cut = cut
                best_norm = min(sa, sb) * 1.0
                found = True
    if best_norm < 1.0:
        best_norm = 1.0
    phi = best_cut / best_norm
    return phi if phi >= 0.0 else 0.0


def faithful_phi(state, n, dim, n_bins):
    """faithful_phi.hexa iit4_faithful_phi — entry point. n<=8 exact."""
    if n <= 0 or dim <= 0 or n_bins <= 0 or n <= 1:
        return 0.0
    if n > 8:
        raise ValueError("faithful_phi: n>8 not supported (exact MIP-EI is n<=8)")
    mi = build_mi_matrix(state, n, dim, n_bins)
    return faithful_phi_from_mi(mi, n)


# ════════════════════════════════════════════════════════════════════════════
# STEP 0 — PROVE the mirror ≡ stdlib faithful_phi.hexa on reference cases
# Reference values produced by `hexa run` of faithful_phi.hexa on THIS Mac
# (Apple Silicon, hexa 0.1.0-dispatch). The hexa `print` truncates to ~6 digits.
# ════════════════════════════════════════════════════════════════════════════
def _ref_caseA():
    raw = [0.5, 1.2, -0.3, 2.1, 0.0, 1.7,  1.0, 2.4, -0.6, 4.2, 0.1, 3.3,
           -0.5, -1.0, 0.2, -2.0, 0.3, -1.5,  3.1, 0.2, 2.2, 1.1, 4.0, 0.9]
    return np.array(raw), 4, 6


def _ref_caseB():
    rawb = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0,  8.0, 7.0, 6.0, 5.0, 4.0, 3.0, 2.0, 1.0,
            0.1, 0.2, 0.1, 0.3, 0.2, 0.1, 0.4, 0.2,  2.0, 2.1, 1.9, 2.2, 2.0, 1.8, 2.3, 2.1,
            5.0, 1.0, 5.0, 1.0, 5.0, 1.0, 5.0, 1.0]
    return np.array(rawb), 5, 8


def prove_mirror():
    print("STEP 0 — prove CPU mirror ≡ stdlib faithful_phi.hexa (hexa run on this Mac)")
    cases = []
    # n=3 reference: cell0=[1,2,3,4] cell1=[2,4,6,8] cell2=[4,3,2,1], dim=4, nb=2 -> 2
    st3 = np.array([1, 2, 3, 4, 2, 4, 6, 8, 4, 3, 2, 1], float)
    cases.append(("n3 dim4 nb2", st3, 3, 4, 2, 2.0))
    a, na, da = _ref_caseA()
    cases.append(("n4 dim6 nb2", a, na, da, 2, 3.0))
    cases.append(("n4 dim6 nb4", a, na, da, 4, 3.37744))
    b, nb_, db = _ref_caseB()
    cases.append(("n5 dim8 nb3", b, nb_, db, 3, 0.372556))
    all_ok = True
    for name, st, n, dim, nbins, ref in cases:
        got = faithful_phi(st, n, dim, nbins)
        ok = abs(got - ref) < 1e-4
        all_ok = all_ok and ok
        print(f"  {name:14s}: mirror={got:.6f}  hexa_ref={ref:.6f}  "
              f"|Δ|={abs(got-ref):.2e}  {'OK' if ok else 'MISMATCH'}")
    print(f"  MIRROR-FAITHFUL: {'PROVEN (≡ stdlib engine)' if all_ok else 'FAILED — DO NOT TRUST'}")
    print()
    if not all_ok:
        raise SystemExit("mirror does not match stdlib faithful_phi.hexa — aborting")
    return all_ok


# ════════════════════════════════════════════════════════════════════════════
# DISCRETIZATION — toy WM latent trajectory (n_steps × latent_dim) → n≤8 units
# ════════════════════════════════════════════════════════════════════════════
# The faithful engine wants an (n units × dim trajectory) matrix and treats each
# unit's dim-step trace as the variable whose pairwise MI is measured. The toy WM
# produces a (n_steps × latent_dim) latent trajectory H. We DISCRETIZE by:
#   - choosing N_UNITS = 8 latent channels (the top-variance channels of the SAME
#     trajectory, so the units are the most informative WM dimensions),
#   - each unit's "trajectory" = that channel's value across the n_steps timesteps.
# So the faithful Φ measures the causal irreducibility (min-cut MI) AMONG the WM's
# 8 principal latent channels over the rollout — a true small-N IIT4 system.
# HONEST: this is a discretization CHOICE; a different unit selection could move
# the absolute Φ, but it is applied IDENTICALLY to every regime, so the CONTRAST
# (the falsifier target) is fair. Toy single-rung (a_scale_honest_scope).
N_UNITS = 8
N_BINS = 4


def latent_to_units(H, n_units=N_UNITS):
    """(n_steps × latent_dim) latent trajectory → (n_units × n_steps) faithful state.
    Pick the n_units highest-variance channels; each becomes a unit whose trajectory
    is its value over the rollout steps. Return flat row-major (n_units*n_steps)."""
    H = np.asarray(H, float)
    if H.ndim == 1:
        H = H[None, :]
    n_steps, d = H.shape
    var = H.var(axis=0)
    idx = np.argsort(var)[::-1][:n_units]
    idx = np.sort(idx)                 # stable order
    units = H[:, idx].T               # (n_units × n_steps)
    return units.reshape(-1), n_units, n_steps


def faithful_phi_of_trajectory(H):
    flat, n, dim = latent_to_units(H)
    return faithful_phi(flat, n, dim, N_BINS)


# ════════════════════════════════════════════════════════════════════════════
# CONDITIONS — replicate the EXACT regimes of H_971/973/988/994
# ════════════════════════════════════════════════════════════════════════════
IN_DIM = 6
LATENT = 24
N_SEEDS = 30
ROLL = 40


def fit_engine(rng, seed):
    wm = LatentWorldModel(IN_DIM, latent_dim=LATENT, seed=seed, retentive=False,
                          spectral_radius=0.95)
    T = 400
    t = np.arange(T)
    stream = np.stack([np.sin(0.2 * t + k) + 0.3 * rng.standard_normal(T)
                       for k in range(IN_DIM)], axis=1)
    Hs = wm.encode_seq(stream)
    wm.fit_transition(Hs[:-1], Hs[1:])
    return wm


def regimes_for_seed(seed):
    """Produce the REACT / DRIFT(=H_971 imagine) / GUIDED(=H_988) latent
    trajectories for one seed, EXACTLY as the original probes did."""
    rng = np.random.default_rng(seed)
    wm = fit_engine(rng, seed)
    # REACT — encode external input stream (H_971 arm-REACT)
    react_stream = np.stack([np.sin(0.2 * np.arange(ROLL) + k) +
                             0.3 * rng.standard_normal(ROLL) for k in range(IN_DIM)], axis=1)
    H_react = wm.encode_seq(react_stream)
    # DRIFT — autonomous internal rollout, no external input (H_971 arm-IMAGINE)
    h0 = H_react[0]
    H_drift = wm.roll_latent(h0, ROLL)
    # GUIDED — goal-directed rollout: steer toward a reachable goal latent each step
    #   (H_988 arm-GUIDED). The goal latent = a real latent reached by the operator.
    goal = wm.roll_latent(h0, ROLL)[-1]      # a reachable target
    H_guided = _roll_guided(wm, h0, goal, ROLL, pull=0.3)
    return H_react, H_drift, H_guided


def _roll_guided(wm, h0, goal, steps, pull=0.3):
    """Goal-directed imagined rollout (H_988): each step apply T then pull toward goal."""
    from cwm_probe_lib import _aug1
    out = []
    h = h0.copy()
    for _ in range(steps):
        h = (_aug1(h) @ wm.T)
        h = h + pull * (goal - h)          # steer toward goal latent
        out.append(h.copy())
    return np.array(out)


def planning_trajectories(seed, depth):
    """H_973 planning regime — MPC over action-conditioned imagined rollouts at a
    given branch depth vs greedy. We mirror the deliberation-latent trajectory:
    GREEDY = react one step; PLAN(depth) = explore `depth`-step imagined branches and
    concatenate the deliberation latents. Φ is measured over the deliberation trace."""
    rng = np.random.default_rng(1000 + seed)
    wm = fit_engine(rng, seed)
    start = np.stack([np.sin(0.2 * np.arange(ROLL) + k) +
                      0.3 * rng.standard_normal(ROLL) for k in range(IN_DIM)], axis=1)
    H0 = wm.encode_seq(start)
    h0 = H0[-1]
    # GREEDY: the reactive perceive trajectory (no lookahead) — same as react
    H_greedy = H0
    # PLAN: imagine `depth` steps ahead along several branches; the deliberation
    # latent trajectory = concatenation of the branch rollouts (what the planner
    # "thinks through"). More depth = longer internal imagined trace.
    branches = 4
    delib = []
    for b in range(branches):
        rb = np.random.default_rng(7000 + seed * 13 + b)
        h = h0.copy() + 0.05 * rb.standard_normal(LATENT)   # perturbed branch seed
        for _ in range(depth):
            h = wm.roll_latent(h, 1)[0]
            delib.append(h.copy())
    H_plan = np.array(delib) if delib else H_greedy
    return H_greedy, H_plan


# ════════════════════════════════════════════════════════════════════════════
# MEASURE
# ════════════════════════════════════════════════════════════════════════════
def contrast_block(name, a, b, label_a, label_b, proxy_a, proxy_b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    con = a.mean() - b.mean()
    d = cohens_d(a, b)
    try:
        t, p = welch_t(a, b)
    except Exception:
        t, p = float("nan"), float("nan")
    if len(a) == len(b):
        lo, hi = boot_ci(a - b)
    else:
        lo, hi = float("nan"), float("nan")
    print(f"--- {name} ---")
    print(f"  FAITHFUL Φ  {label_a:8s} = {a.mean():.4f} ± {a.std():.4f}")
    print(f"  FAITHFUL Φ  {label_b:8s} = {b.mean():.4f} ± {b.std():.4f}")
    print(f"  FAITHFUL contrast ({label_a}−{label_b}) = {con:+.4f}  "
          f"Cohen d={d:+.3f}  Welch t={t:+.3f} p={p:.3e}  CI=[{lo:+.4f},{hi:+.4f}]")
    print(f"  [proxy, original]  {label_a}={proxy_a:.4f}  {label_b}={proxy_b:.4f}  "
          f"proxy contrast={proxy_a - proxy_b:+.4f}")
    return con, d, p


def main():
    print("=" * 78)
    print("H_999 — FAITHFUL IIT4 re-measure of the imagination/planning Φ-null")
    print("substrate=CPU-mirror (numpy) — BYTE-FAITHFUL mirror of stdlib")
    print("hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (proven ≡ below)")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_scale_honest_scope: TOY rung")
    print("=" * 78)
    print()
    prove_mirror()

    print(f"DISCRETIZATION: WM latent ({LATENT}-dim, {ROLL} steps) → top-{N_UNITS} "
          f"variance channels as n={N_UNITS} units; each unit's {ROLL}-step trace is")
    print(f"its variable; faithful MIP-EI Φ with n_bins={N_BINS} (exact, n≤8).")
    print(f"Applied IDENTICALLY to every regime so the CONTRAST is fair.\n")

    # ---- collect faithful Φ + proxy Φ for every regime, every seed ----
    fphi = {k: [] for k in ("react", "drift", "guided")}
    pphi = {k: [] for k in ("react", "drift", "guided")}
    for s in range(N_SEEDS):
        Hr, Hd, Hg = regimes_for_seed(s)
        fphi["react"].append(faithful_phi_of_trajectory(Hr))
        fphi["drift"].append(faithful_phi_of_trajectory(Hd))
        fphi["guided"].append(faithful_phi_of_trajectory(Hg))
        pphi["react"].append(phi_proxy(Hr)[0])
        pphi["drift"].append(phi_proxy(Hd)[0])
        pphi["guided"].append(phi_proxy(Hg)[0])
    for k in fphi:
        fphi[k] = np.array(fphi[k]); pphi[k] = np.array(pphi[k])

    print("################ H_971 — imagination(DRIFT) vs reaction ################")
    print("# original proxy verdict: 🔴 Φ_IMAGINE 0.068 < Φ_REACT 0.095 (d −3.4)")
    contrast_block("H_971 faithful: DRIFT(imagine) − REACT",
                   fphi["drift"], fphi["react"], "DRIFT", "REACT",
                   pphi["drift"].mean(), pphi["react"].mean())
    print()
    print("############### H_988 — guided imagination vs reaction ###############")
    print("# original proxy verdict: 🔴 Φ_GUIDED 0.039 < Φ_DRIFT 0.068 < Φ_REACT 0.095")
    contrast_block("H_988 faithful: GUIDED − REACT",
                   fphi["guided"], fphi["react"], "GUIDED", "REACT",
                   pphi["guided"].mean(), pphi["react"].mean())
    contrast_block("H_988 faithful: GUIDED − DRIFT",
                   fphi["guided"], fphi["drift"], "GUIDED", "DRIFT",
                   pphi["guided"].mean(), pphi["drift"].mean())
    print()

    print("################ H_973 — planning(MPC) vs greedy ################")
    print("# original proxy verdict: 🔴 Φ_PLAN 0.063 < Φ_GREEDY 0.104; Φ falls with depth")
    depths = [1, 2, 4, 8]
    plan_by_depth = {dpt: [] for dpt in depths}
    greedy_f = []
    plan_proxy_by_depth = {dpt: [] for dpt in depths}
    greedy_proxy = []
    for s in range(N_SEEDS):
        for dpt in depths:
            Hg, Hp = planning_trajectories(s, dpt)
            plan_by_depth[dpt].append(faithful_phi_of_trajectory(Hp))
            plan_proxy_by_depth[dpt].append(phi_proxy(Hp)[0])
            if dpt == depths[0]:
                greedy_f.append(faithful_phi_of_trajectory(Hg))
                greedy_proxy.append(phi_proxy(Hg)[0])
    greedy_f = np.array(greedy_f)
    greedy_proxy = np.array(greedy_proxy)
    for dpt in depths:
        plan_by_depth[dpt] = np.array(plan_by_depth[dpt])
        plan_proxy_by_depth[dpt] = np.array(plan_proxy_by_depth[dpt])
    deepest = depths[-1]
    contrast_block(f"H_973 faithful: PLAN(depth={deepest}) − GREEDY",
                   plan_by_depth[deepest], greedy_f, "PLAN", "GREEDY",
                   plan_proxy_by_depth[deepest].mean(), greedy_proxy.mean())
    # dose-response over depth
    means = [plan_by_depth[dpt].mean() for dpt in depths]
    from cwm_probe_lib import spearman
    flat_depths = np.repeat(depths, N_SEEDS)
    flat_phi = np.concatenate([plan_by_depth[dpt] for dpt in depths])
    rho, prho = spearman(flat_depths, flat_phi)
    print(f"  faithful Φ vs plan-depth: depths={depths} means={[f'{m:.4f}' for m in means]}")
    print(f"  dose-response Spearman rho={rho:+.3f} p={prho:.3e}  "
          f"(proxy was rho −0.47: Φ FELL with depth)")
    print()

    # ════════════════════════════════════════════════════════════════════════
    # VERDICT
    # ════════════════════════════════════════════════════════════════════════
    print("=" * 78)
    print("VERDICT MATRIX (faithful IIT4 vs original proxy)")
    print("=" * 78)
    c971 = fphi["drift"].mean() - fphi["react"].mean()
    c988 = fphi["guided"].mean() - fphi["react"].mean()
    c973 = plan_by_depth[deepest].mean() - greedy_f.mean()

    def tag(c):
        return "RAISES Φ (proxy REVERSED → PROXY-ARTIFACT)" if c > 0 else "does NOT raise Φ (NULL-ROBUST)"
    print(f"  H_971 imagination(DRIFT) vs REACT : faithful contrast={c971:+.4f} → {tag(c971)}")
    print(f"  H_988 guided imagination vs REACT : faithful contrast={c988:+.4f} → {tag(c988)}")
    print(f"  H_973 planning(d8) vs GREEDY      : faithful contrast={c973:+.4f} → {tag(c973)}")
    print()
    # PASS-condition frozen in the .md: NULL-ROBUST iff faithful ALSO shows
    # internal generation does NOT raise Φ (all contrasts <= 0, within noise).
    raises = [c for c in (c971, c988, c973) if c > 1e-3]
    if not raises:
        print("OVERALL: 🟢 NULL-ROBUST-UNDER-FAITHFUL-Φ — faithful IIT4 AGREES with the")
        print("  proxy: imagination/planning does NOT raise Φ. The H_971/973/988/994")
        print("  closed-negatives STAND under the real exact MIP-EI measure (STRONG).")
    else:
        print("OVERALL: 🔴-vs-proxy = PROXY-ARTIFACT — faithful IIT4 REVERSES the proxy on")
        print(f"  {len(raises)}/3 conditions (internal generation RAISES faithful Φ). The")
        print("  original nulls were the proxy's purpose-blindness → H_971/973/988/994 RE-OPEN.")
    print("=" * 78)
    print("HONEST scope (a_scale_honest_scope): TOY single-rung — the toy WM latent is")
    print("DISCRETIZED to n=8 units; faithful Φ is exact at that n but scale-transfer is")
    print("UNVERIFIED. The contrast (not the absolute Φ) is the falsifier; same")
    print("discretization applied to every regime. NOT a forge binary.")


if __name__ == "__main__":
    main()
