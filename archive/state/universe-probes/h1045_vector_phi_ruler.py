"""H_1045 — Vector-Phi ruler: does a 3-component measure (faithful_phi, big-Phi,
redundancy-margin) linearly SEPARATE planning/integrated states from matched controls
BETTER than the best single scalar component?

CONSTRUCTIVE follow-up of the Phi measure-dependence arc (all prior GREEN, H_1004 ->
H_1037): the two canonical IIT-4.0 measures DISAGREE IN SIGN under planning (faithful_phi
RISES, big-Phi FALLS), and the mechanism (H_1017/H_1020) is redundancy-dominance. If no
single scalar captures "integrated/planning-like" state, a consciousness ruler should be a
VECTOR. This script TESTS that: vector LDA vs best-single-scalar LDA, LEAVE-ONE-OUT AUC,
over a >=6-substrate battery at n<=6 EXACT, >=20 seeds.

ENGINES — BOTH stdlib IIT-4.0 CPU mirrors, RE-PROVEN == stdlib at n=4 AND n=5 (H_1012
prove_mirrors_at_n) BEFORE scoring (a_phi_iit4_tool — real engines, NO proxy). big-Phi
distinctions+relations EXACT, MIP bipartition FULLY ENUMERATED at every n<=6. The PID
redundancy-margin is the H_1017 pid_system on the SAME bits (the EXPLANATORY axis, NOT a
Phi proxy), validated on canonical COPY(redundant)/XOR(synergy) cases.

real-module-name imports (NO importlib custom-name); SERIAL at n<=6 toy. $0 CPU-local, no
GPU, not a forge binary. g5 CODE-measured (no LLM self-judge, p7). a_scale_honest_scope:
TOY n<=6; production transfer UNVERIFIED.

PRE-REGISTERED FALSIFIER (frozen in UNIVERSE/cards/H_1045_vector_phi_ruler.md; TEXT only):
  MARGIN = +0.05 AUC. best single scalar = per-substrate-mean LOO-AUC argmax.
  PASS requires BOTH:
    (a) mean-over-substrates vector LOO-AUC >= best-single-scalar mean LOO-AUC + 0.05
    (b) NEEDS-VECTOR: >=1 substrate with vector LOO-AUC >= 0.75 AND every scalar < 0.75.
  FAIL = NOT(a AND b): one scalar suffices (a_paper_negative_ok).
"""
import sys, os, math, time, json, argparse
import numpy as np
import multiprocessing as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))
sys.path.insert(0, HERE)

# real-module-name imports (forked-pickle safe; we run SERIAL but keep the discipline)
import h1004_bigphi_faithful_clean as h1004      # noqa: E402
import h1012_bigphi_faithful_larger_n as h1012   # noqa: E402
import h1037_n6_discretization as h1037          # noqa: E402
import h1017_split_redundancy_mechanism as h1017  # noqa: E402

# engines + substrate plumbing (all stdlib mirrors, verbatim)
big_phi = h1004.big_phi
faithful_phi = h1004.faithful_phi
binary_seq_to_tpm = h1004.binary_seq_to_tpm
modal_state = h1004.modal_state
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
planning_trajectories = h1004.planning_trajectories
regimes_for_seed = h1004.regimes_for_seed
prove_mirrors_at_n = h1012.prove_mirrors_at_n
latent_to_binary_seq_disc = h1037.latent_to_binary_seq_disc  # (H, n, nb, scheme)->(bits,n)
pid_system = h1017.pid_system                                # WB I_min PID on bits

# ── matched discretization for EVERY read: nb=2 quantile (median baseline; ==
#    H_1012/H_1017/H_1024/H_1037 baseline). The ONLY thing that varies across substrates
#    is the SUBSTRATE (n + contrast), never the read recipe. ──
NB = 2
SCHEME = "quantile"


def reads_at_n(H, n):
    """ONE latent trajectory -> the 3-vector (faithful_phi, big_phi, redundancy_margin)
    on the SAME nb=2 quantile bits at size n. Phi from stdlib mirrors; redundancy-margin
    from the H_1017 PID on those same bits. Returns dict(faith, big, redmargin)."""
    bits, nn = latent_to_binary_seq_disc(H, n, NB, SCHEME)
    # big-Phi EXACT (MIP fully enumerated)
    tpm, sc = binary_seq_to_tpm(bits, nn)
    bphi = big_phi(tpm, nn, modal_state(sc))[0]
    # faithful_phi EXACT (MIP-EI scalar) on the SAME bits
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, nn)
    fphi = faithful_phi(fstate, fn, fdim, 2)
    # redundancy-margin = red_total - syn_total (H_1017 WB I_min PID on the SAME bits)
    p = pid_system(bits)
    redmargin = float(p["red_total"] - p["syn_total"])
    return dict(faith=float(fphi), big=float(bphi), redmargin=redmargin)


# ═══════════════════════════════════════════════════════════════════════════
# SUBSTRATE BATTERY — >= 6 substrates. Each yields (pos_H, neg_H) per seed.
#   pos = planning / deeper-deliberation (the "integrated" side)
#   neg = matched greedy / drift / guided / shallow control.
# ═══════════════════════════════════════════════════════════════════════════
def sub_plan_greedy(seed, n, depth=8):
    Hg, Hp = planning_trajectories(seed, depth)
    return Hp, Hg, n


def sub_plan_drift(seed, n=4, depth=8):
    _Hg, Hp = planning_trajectories(seed, depth)
    _react, H_drift, _guided = regimes_for_seed(seed)
    return Hp, H_drift, n


def sub_plan_guided(seed, n=4, depth=8):
    _Hg, Hp = planning_trajectories(seed, depth)
    _react, _drift, H_guided = regimes_for_seed(seed)
    return Hp, H_guided, n


def sub_deep_shallow(seed, n=4, deep=12, shallow=2):
    _Hg_d, Hp_deep = planning_trajectories(seed, deep)
    _Hg_s, Hp_shallow = planning_trajectories(seed, shallow)
    return Hp_deep, Hp_shallow, n


# frozen battery (>=6 substrates) — name only; build_substrate() dispatches by name so
# forked Pool workers can rebuild the (pos,neg) pair without pickling a lambda/closure.
BATTERY_NAMES = [
    "S1_n4_plan_greedy",
    "S2_n5_plan_greedy",
    "S3_n6_plan_greedy",
    "S4_n4_plan_drift",
    "S5_n4_plan_guided",
    "S6_n4_deep_shallow",
]


def build_substrate(name, seed):
    """Dispatch a substrate by NAME (picklable for forked workers). Returns (posH,negH,n)."""
    if name == "S1_n4_plan_greedy":
        return sub_plan_greedy(seed, 4, 8)
    if name == "S2_n5_plan_greedy":
        return sub_plan_greedy(seed, 5, 8)
    if name == "S3_n6_plan_greedy":
        return sub_plan_greedy(seed, 6, 8)
    if name == "S4_n4_plan_drift":
        return sub_plan_drift(seed, 4, 8)
    if name == "S5_n4_plan_guided":
        return sub_plan_guided(seed, 4, 8)
    if name == "S6_n4_deep_shallow":
        return sub_deep_shallow(seed, 4, 12, 2)
    raise ValueError(f"unknown substrate {name}")


FEATURES = ["faith", "big", "redmargin"]


# ── top-level Pool worker — ONE (substrate, seed) -> both sides' 3-vectors. Top-level so
#    forked workers can pickle it (H_1022 lesson). EXACT, pure fn of (name, seed). ──
def _eval_pair(args):
    name, seed = args
    posH, negH, n = build_substrate(name, seed)
    rp = reads_at_n(posH, n)
    rn = reads_at_n(negH, n)
    return (name, seed, n,
            [rp[f] for f in FEATURES], [rn[f] for f in FEATURES])


# ═══════════════════════════════════════════════════════════════════════════
# Fisher LDA + LEAVE-ONE-OUT AUC. Closed-form, pure numpy, no sklearn dependency
# (deterministic, auditable). Per-feature z-standardization fit on the TRAIN fold only.
# ═══════════════════════════════════════════════════════════════════════════
def _lda_direction(Xpos, Xneg):
    """Fisher LDA direction w ∝ Sw^-1 (mu_pos - mu_neg). X = (m, d)."""
    mu_p = Xpos.mean(axis=0)
    mu_n = Xneg.mean(axis=0)
    d = Xpos.shape[1]
    Sw = np.zeros((d, d))
    for X, mu in ((Xpos, mu_p), (Xneg, mu_n)):
        C = X - mu
        Sw += C.T @ C
    Sw += 1e-6 * np.eye(d)  # ridge for invertibility (n<=6 toy, small samples)
    w = np.linalg.solve(Sw, (mu_p - mu_n))
    return w


def _auc(scores, labels):
    """ROC AUC via rank statistic (Mann-Whitney). labels in {0,1}, 1=positive."""
    labels = np.asarray(labels)
    pos = scores[labels == 1]
    neg = scores[labels == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    order = np.argsort(np.concatenate([pos, neg]), kind="mergesort")
    ranks = np.empty(len(order), float)
    ranks[order] = np.arange(1, len(order) + 1)
    # average ranks for ties
    allv = np.concatenate([pos, neg])
    sidx = np.argsort(allv, kind="mergesort")
    sv = allv[sidx]
    sr = ranks[sidx]
    i = 0
    while i < len(sv):
        j = i
        while j + 1 < len(sv) and sv[j + 1] == sv[i]:
            j += 1
        if j > i:
            sr[i:j + 1] = sr[i:j + 1].mean()
        i = j + 1
    ranks[sidx] = sr
    rp = ranks[:len(pos)].sum()
    auc = (rp - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg))
    return float(auc)


def loo_auc(X, y, feat_idx):
    """Leave-one-out CV LDA on columns feat_idx of X; ROC AUC of held-out scores.
    Standardization + LDA direction are fit on the TRAIN fold only each leave-one-out.
    Returns sign-agnostic AUC = max(auc, 1-auc)."""
    X = np.asarray(X, float)[:, feat_idx]
    if X.ndim == 1:
        X = X[:, None]
    y = np.asarray(y)
    m = len(y)
    held = np.empty(m, float)
    for i in range(m):
        tr = np.ones(m, bool); tr[i] = False
        Xtr, ytr = X[tr], y[tr]
        mu = Xtr.mean(axis=0); sd = Xtr.std(axis=0); sd[sd < 1e-12] = 1.0
        Ztr = (Xtr - mu) / sd
        Zi = (X[i] - mu) / sd
        w = _lda_direction(Ztr[ytr == 1], Ztr[ytr == 0])
        held[i] = float(Zi @ w)
    a = _auc(held, y)
    if math.isnan(a):
        return a
    return max(a, 1.0 - a)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=24, help=">=20 seeds per substrate")
    ap.add_argument("--margin", type=float, default=0.05, help="pre-set AUC margin (frozen)")
    ap.add_argument("--needs-thr", type=float, default=0.75,
                    help="NEEDS-VECTOR per-substrate AUC threshold (frozen)")
    ap.add_argument("--workers", type=int, default=max(1, mp.cpu_count() - 1),
                    help="parallel Pool workers (a_wall_first)")
    ap.add_argument("--pool-timeout", type=float, default=7200.0,
                    help="hard Pool timeout in seconds")
    ap.add_argument("--out", type=str,
                    default=os.path.join(HERE, "h1045_vector_phi_ruler_result.json"))
    args = ap.parse_args()
    MARGIN = args.margin
    NEEDS_THR = args.needs_thr

    print("=" * 90)
    print("H_1045 — Vector-Phi ruler: does (faithful_phi, big-Phi, redundancy-margin)")
    print("         linearly SEPARATE planning/integrated states from matched controls")
    print("         BETTER than the best single scalar?  Constructive follow-up of H_1004->H_1037.")
    print("substrate=CPU-mirror (numpy) — H_1004 engines + H_1012 proof, RE-PROVEN == stdlib per n")
    print("big-Phi: hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (system Phi_s, MIP enumerated)")
    print("faithful_phi: hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar)")
    print("redundancy-margin: H_1017 Williams-Beer I_min PID (red_total - syn_total) on the SAME bits")
    print(f"matched read = nb={NB} {SCHEME} (median baseline) for EVERY substrate; only the SUBSTRATE varies")
    print(f"classifier = Fisher LDA, LEAVE-ONE-OUT CV, sign-agnostic ROC AUC | seeds/substrate={args.seeds}")
    print(f"PRE-FROZEN FALSIFIER: MARGIN=+{MARGIN} AUC ; NEEDS-VECTOR thr={NEEDS_THR}")
    print("  PASS = (vector mean-AUC >= best-scalar mean-AUC + MARGIN) AND (>=1 substrate vector>=thr & all scalars<thr)")
    print("  FAIL = NOT both -> one scalar suffices (a_paper_negative_ok)")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_phi_iit4_tool | a_scale_honest_scope | $0 CPU")
    print("=" * 90, flush=True)
    print()

    # ── STEP 0: RE-PROVE BOTH mirrors == stdlib at n=4 AND n=5 BEFORE scoring ──
    print("STEP 0 — RE-PROVE BOTH CPU mirrors == stdlib (a_phi_iit4_tool) at n=4 AND n=5")
    print("         BEFORE scoring (H_1012 prove_mirrors_at_n; LIVE stdlib refs):", flush=True)
    proven = {}
    for n in (4, 5):
        proven[n] = bool(prove_mirrors_at_n(n))
        print()
    print(f"  == mirror-equivalence results: {proven}", flush=True)
    if not all(proven.values()):
        print("  ABORT — a mirror == stdlib proof FAILED; cannot trust this run.")
        raise SystemExit(1)

    # PID validity (canonical COPY redundant / XOR synergy), determinism re-run.
    Tc = np.array([0, 1, 0, 1, 1, 0, 1, 0]); Tc2 = np.stack([Tc, Tc], 1)
    rc = pid_system(np.stack([Tc, Tc, Tc, Tc], 1))
    Xa = np.array([0, 0, 1, 1, 0, 0, 1, 1]); Xb = np.array([0, 1, 0, 1, 0, 1, 0, 1])
    Xt = Xa ^ Xb
    rx = pid_system(np.stack([Xt, Xa, Xb, Xt], 1))
    copy_ok = rc["red_total"] > 0.0 and abs(rc["syn_total"]) < 1e-6
    xor_ok = rx["syn_total"] > 0.0
    print(f"  PID canonical-case check: COPY red={rc['red_total']:.3f} syn={rc['syn_total']:.3f} (red>0,syn~0:{copy_ok}) | "
          f"XOR red={rx['red_total']:.3f} syn={rx['syn_total']:.3f} (syn>0:{xor_ok})", flush=True)
    # determinism of the full reads_at_n path
    Hg0, Hp0 = planning_trajectories(0, 8)
    r1 = reads_at_n(Hp0, 4); r2 = reads_at_n(Hp0, 4)
    det_ok = all(abs(r1[k] - r2[k]) < 1e-12 for k in FEATURES)
    print(f"  reads_at_n deterministic re-run (n=4): {det_ok}  "
          f"(faith={r1['faith']:.4f} big={r1['big']:.4f} redmargin={r1['redmargin']:.4f})", flush=True)
    if not (copy_ok and xor_ok and det_ok):
        print("  ABORT — PID validity / determinism guard failed.")
        raise SystemExit(1)
    print()

    # ── STEP 1: score the battery. Dispatch ALL (substrate, seed) read-pairs over a
    #    GUARDED multiprocessing Pool (a_wall_first — the n=6 big-Phi read is ~6min/eval, so
    #    a serial chain over 6 substrates x seeds is hours; the reads are an EXACT pure fn of
    #    (name, seed), independent, so they parallelize cleanly). Hard per-pool timeout.
    #    Each (substrate,seed) returns BOTH sides' 3-vectors; we then assemble per-substrate
    #    LOO-AUC for the vector and each single scalar. ──
    print(f"STEP 1 — score the {len(BATTERY_NAMES)}-substrate battery, {args.seeds} seeds each "
          f"(PARALLEL Pool, EXACT) over {args.workers} workers", flush=True)
    t0 = time.time()
    jobs = [(name, s) for name in BATTERY_NAMES for s in range(args.seeds)]
    pool = mp.Pool(processes=args.workers)
    try:
        async_res = pool.map_async(_eval_pair, jobs)
        results = async_res.get(timeout=args.pool_timeout)  # hard timeout
    finally:
        pool.close()
        pool.join()
    print(f"  all {len(jobs)} (substrate,seed) read-pairs DONE in {time.time()-t0:.1f}s wall "
          f"({2*len(jobs)} EXACT reads)", flush=True)

    # assemble per-substrate (X,y) and score
    per_sub = []
    for sname in BATTERY_NAMES:
        rows = [r for r in results if r[0] == sname]
        rows.sort(key=lambda r: r[1])  # by seed (determinism of table)
        n = rows[0][2]
        X = []; y = []
        for (_nm, _s, _n, pvec, nvec) in rows:
            X.append(pvec); y.append(1)
            X.append(nvec); y.append(0)
        X = np.array(X, float); y = np.array(y, int)
        scalar_auc = {FEATURES[i]: loo_auc(X, y, [i]) for i in range(len(FEATURES))}
        vec_auc = loo_auc(X, y, [0, 1, 2])
        best_scalar = max(scalar_auc, key=lambda k: scalar_auc[k])
        best_scalar_auc = scalar_auc[best_scalar]
        all_scalars_below = all(v < NEEDS_THR for v in scalar_auc.values())
        needs_vector = (vec_auc >= NEEDS_THR) and all_scalars_below
        print(f"  {sname:20s} (n={n}, {args.seeds} seeds): "
              f"faith={scalar_auc['faith']:.3f} big={scalar_auc['big']:.3f} "
              f"redmargin={scalar_auc['redmargin']:.3f} | VECTOR={vec_auc:.3f} | "
              f"best-scalar={best_scalar}({best_scalar_auc:.3f}) | needs-vector={needs_vector}",
              flush=True)
        per_sub.append(dict(name=sname, n=int(n), seeds=int(args.seeds),
                            scalar_auc=scalar_auc, vector_auc=float(vec_auc),
                            best_scalar=best_scalar, best_scalar_auc=float(best_scalar_auc),
                            needs_vector=bool(needs_vector)))
    print(f"  battery scored in {time.time()-t0:.1f}s", flush=True)
    print()

    # ── FALSIFIER ──
    print("=" * 90)
    print("PER-SUBSTRATE LOO-AUC TABLE (sign-agnostic Fisher-LDA leave-one-out)")
    print("=" * 90)
    print(f"  {'substrate':20s} | {'n':>1s} | {'faith':>6s} | {'big':>6s} | {'redmrg':>6s} | "
          f"{'VECTOR':>6s} | {'best-scalar':>14s} | {'needs-vec':>9s}")
    for r in per_sub:
        sa = r["scalar_auc"]
        print(f"  {r['name']:20s} | {r['n']:>1d} | {sa['faith']:6.3f} | {sa['big']:6.3f} | "
              f"{sa['redmargin']:6.3f} | {r['vector_auc']:6.3f} | "
              f"{r['best_scalar']+'('+format(r['best_scalar_auc'],'.3f')+')':>14s} | "
              f"{str(r['needs_vector']):>9s}")
    print()

    # mean-over-substrates AUC, per scalar + vector
    mean_scalar = {f: float(np.mean([r["scalar_auc"][f] for r in per_sub])) for f in FEATURES}
    mean_vector = float(np.mean([r["vector_auc"] for r in per_sub]))
    best_scalar_overall = max(mean_scalar, key=lambda k: mean_scalar[k])
    best_scalar_overall_auc = mean_scalar[best_scalar_overall]
    margin_gain = mean_vector - best_scalar_overall_auc
    cond_a = margin_gain >= MARGIN
    needs_subs = [r["name"] for r in per_sub if r["needs_vector"]]
    cond_b = len(needs_subs) > 0
    PASS = bool(cond_a and cond_b)

    print(f"mean-over-substrates LOO-AUC:  faith={mean_scalar['faith']:.4f}  "
          f"big={mean_scalar['big']:.4f}  redmargin={mean_scalar['redmargin']:.4f}  "
          f"|  VECTOR={mean_vector:.4f}")
    print(f"best single scalar (mean): {best_scalar_overall} = {best_scalar_overall_auc:.4f}")
    print(f"vector - best-scalar margin = {margin_gain:+.4f}  (pre-set MARGIN = +{MARGIN})")
    print(f"  cond(a) vector beats best scalar by >= MARGIN : {cond_a}")
    print(f"  cond(b) NEEDS-VECTOR substrate exists (vector>={NEEDS_THR} & all scalars<{NEEDS_THR}): "
          f"{cond_b}  {needs_subs}")
    print()
    print("=" * 90)
    if PASS:
        print("OVERALL: VECTOR-RULER-STRICTLY-MORE-INFORMATIVE — the 3-vector (faithful_phi, big-Phi,")
        print(f"  redundancy-margin) separates planning/integrated from control BETTER than the best")
        print(f"  single scalar by {margin_gain:+.4f} AUC (>= the pre-set +{MARGIN}), AND at least one")
        print(f"  substrate NEEDS the vector ({needs_subs}): every single scalar fails to separate it")
        print(f"  (<{NEEDS_THR}) while the vector does (>= {NEEDS_THR}). A consciousness ruler is a")
        print(f"  VECTOR, not one scalar — the measure-dependence (H_1004->H_1037) demands >=2 axes.")
        print("  VERDICT-TOKEN: VECTOR-RULER-STRICTLY-MORE-INFORMATIVE")
    else:
        why = []
        if not cond_a:
            why.append(f"vector beats best scalar by only {margin_gain:+.4f} < +{MARGIN}")
        if not cond_b:
            why.append("no substrate needs the vector (best scalar separates everything it can)")
        print("OVERALL: ONE-SCALAR-SUFFICES (CLOSED-NEGATIVE) — the vector ruler is NOT strictly more")
        print(f"  informative: {' AND '.join(why)}. The best single scalar ({best_scalar_overall}) is the")
        print("  ruler; the 3-vector adds nothing decisive beyond it on this battery (a_paper_negative_ok).")
        print("  VERDICT-TOKEN: ONE-SCALAR-SUFFICES")
    print("=" * 90)
    print("HONEST scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n<=6 (largest EXACT big-Phi);")
    print("BOTH CPU mirrors RE-PROVEN == stdlib at n=4 AND n=5 BEFORE scoring (a_phi_iit4_tool, no")
    print("proxy); big-Phi MIP fully enumerated, distinctions+relations EXACT; PID validated on")
    print("canonical COPY/XOR; reads deterministic. LOO-AUC is sign-agnostic (no orientation penalty).")
    print("Production-scale transfer UNVERIFIED. g5 CODE-measured (no LLM self-judge, p7). $0 CPU-local.")

    out = dict(seeds=int(args.seeds), margin=float(MARGIN), needs_thr=float(NEEDS_THR),
               mirror_proven={int(k): bool(v) for k, v in proven.items()},
               copy_ok=bool(copy_ok), xor_ok=bool(xor_ok), det_ok=bool(det_ok),
               per_substrate=per_sub,
               mean_scalar_auc=mean_scalar, mean_vector_auc=float(mean_vector),
               best_scalar_overall=best_scalar_overall,
               best_scalar_overall_auc=float(best_scalar_overall_auc),
               margin_gain=float(margin_gain), cond_a=bool(cond_a), cond_b=bool(cond_b),
               needs_vector_substrates=needs_subs, PASS=bool(PASS),
               verdict_token=("VECTOR-RULER-STRICTLY-MORE-INFORMATIVE" if PASS
                              else "ONE-SCALAR-SUFFICES"),
               total_wall_sec=time.time() - t0)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nRESULT JSON -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
