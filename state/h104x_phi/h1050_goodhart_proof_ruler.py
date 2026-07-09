"""H_1050 — Goodhart-proof ruler: does a perplexity-orthogonal Phi ruler resist adversarial gaming?

Adversarial-ES (gradient-free) on a small numpy recurrent latent generator theta=(W,b).
Ruler R = stdlib faithful_phi (exact MIP-EI, mirror RE-PROVEN == stdlib at n=4,5 before scoring).
Independent-integration engine I = big-Phi (a DIFFERENT stdlib engine — no circularity). a_phi_iit4_tool.
Frozen bar: state/h104x_phi/H_1050_FREEZE.txt. TOY rung -> DIRECTIONAL (a_toy_scale_recheck).

Run:  python3 -u h1050_goodhart_proof_ruler.py [--n 5] [--iters 160] [--seeds 3] [--ckpts 16]
"""
import sys, os, time, json, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROBES = os.environ.get("H104X_PROBES",
                        os.path.abspath(os.path.join(HERE, "..", "..", "archive", "state", "universe-probes")))
CWM = os.environ.get("H104X_CWM",
                     os.path.abspath(os.path.join(HERE, "..", "..", "archive", "CWM", "probes")))
for p in (CWM, PROBES):
    if p not in sys.path:
        sys.path.insert(0, p)
import h1004_bigphi_faithful_clean as h1004
import h1012_bigphi_faithful_larger_n as h1012
import h1037_n6_discretization as h1037

big_phi = h1004.big_phi
faithful_phi = h1004.faithful_phi
binary_seq_to_tpm = h1004.binary_seq_to_tpm
modal_state = h1004.modal_state
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
prove_mirrors_at_n = h1012.prove_mirrors_at_n
latent_to_binary_seq_disc = h1037.latent_to_binary_seq_disc  # (H, n, nb, scheme) -> (bits, n)

LATENT = 24
T = 40
NB, SCHEME = 2, "quantile"

# frozen bar
EPS = 0.10
TASK_DROP = 0.20
EXPLOIT_CORR = 0.50


def unpack(theta):
    W = theta[:LATENT * LATENT].reshape(LATENT, LATENT)
    b = theta[LATENT * LATENT:]
    return W, b


def rollout(theta, x0):
    W, b = unpack(theta)
    xs = [x0]
    x = x0
    for _ in range(T - 1):
        x = np.tanh(W @ x + b)
        xs.append(x)
    return np.array(xs)  # (T, LATENT)


def ruler_faithful(H, n):
    bits, nn = latent_to_binary_seq_disc(H, n, NB, SCHEME)
    fstate, fn, fdim = binary_seq_to_faithful_state(bits, nn)
    return float(faithful_phi(fstate, fn, fdim, 2))


def integ_bigphi(H, n):
    bits, nn = latent_to_binary_seq_disc(H, n, NB, SCHEME)
    tpm, sc = binary_seq_to_tpm(bits, nn)
    return float(big_phi(tpm, nn, modal_state(sc))[0])


def task_loss(theta, x0, H_target):
    return float(np.mean((rollout(theta, x0) - H_target) ** 2))


def es_optimize(theta0, x0, objective, iters, rng, minimize, sigma=0.15, lam=8,
                track_ckpts=None, track_fns=None):
    """Simple (1+lam) Gaussian ES hill-climb. Returns (theta, history[list of obj], ckpt_records)."""
    theta = theta0.copy()
    best = objective(theta)
    hist = [best]
    ck = {k: [] for k in (track_fns or {})}
    ck_iters = set(track_ckpts or [])
    if track_fns:
        for k, fn in track_fns.items():
            ck[k].append(fn(theta))
    for it in range(iters):
        cands = theta[None, :] + sigma * rng.standard_normal((lam, theta.size))
        vals = np.array([objective(c) for c in cands])
        idx = np.argmin(vals) if minimize else np.argmax(vals)
        improved = (vals[idx] < best) if minimize else (vals[idx] > best)
        if improved:
            theta = cands[idx]
            best = float(vals[idx])
        hist.append(best)
        if it in ck_iters and track_fns:
            for k, fn in track_fns.items():
                ck[k].append(fn(theta))
    return theta, hist, ck


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--iters", type=int, default=160)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--ckpts", type=int, default=16)
    ap.add_argument("--out", default=os.path.join(HERE, "h1050_goodhart_proof_ruler_result.json"))
    args = ap.parse_args()
    n = args.n

    print("=" * 92)
    print("H_1050 — Goodhart-proof ruler: adversarial-ES on a perplexity-ORTHOGONAL faithful_phi ruler")
    print("ruler=stdlib faithful_phi (exact MIP-EI) | independent engine=big-Phi (different engine, no circularity)")
    print("a_phi_iit4_tool: mirrors RE-PROVEN == stdlib at n=4,5 before scoring. p7. TOY -> DIRECTIONAL.")
    print(f"FROZEN BAR: (A) L_task drops >= {TASK_DROP:.0%} AND |dRuler| <= {EPS}; "
          f"(B) R rises AND corr(R,I) >= {EXPLOIT_CORR}. PASS = A AND B (Goodhart-resistant).")
    print(f"n={n} iters={args.iters} seeds={args.seeds} ckpts={args.ckpts}")
    print("=" * 92, flush=True)

    print("\nSTEP 0 — RE-PROVE CPU mirror == stdlib at n=4,5 (a_phi_iit4_tool):")
    proven = {k: bool(prove_mirrors_at_n(k)) for k in (4, 5)}
    print(f"  mirror-equivalence: {proven}")
    if not all(proven.values()):
        raise SystemExit("mirror proof FAILED — abort")

    ck_iters = sorted(set(np.linspace(0, args.iters - 1, args.ckpts).astype(int).tolist()))
    per_seed = []
    t0 = time.time()
    for sd in range(args.seeds):
        rng = np.random.default_rng(1000 + sd)
        theta0 = 0.3 * rng.standard_normal(LATENT * LATENT + LATENT)
        x0 = rng.standard_normal(LATENT)
        # fixed target dynamics (the "task"): a different random stable map
        theta_star = 0.3 * rng.standard_normal(LATENT * LATENT + LATENT)
        H_target = rollout(theta_star, x0)

        R_init = ruler_faithful(rollout(theta0, x0), n)

        # ── REGIME A: task-only ES (minimize L_task); track ruler flatness ──
        print(f"\n######## seed {sd}: REGIME A (task-only ES, minimize L_task) ########", flush=True)
        thA, histA, _ = es_optimize(theta0, x0, lambda th: task_loss(th, x0, H_target),
                                     args.iters, rng, minimize=True)
        L0, Lf = histA[0], histA[-1]
        R_afterA = ruler_faithful(rollout(thA, x0), n)
        task_drop = (L0 - Lf) / (abs(L0) + 1e-12)
        dR_A = abs(R_afterA - R_init)
        A_pass = (task_drop >= TASK_DROP) and (dR_A <= EPS)
        print(f"  L_task {L0:.4f} -> {Lf:.4f}  drop={task_drop:.1%} (>= {TASK_DROP:.0%}: {task_drop>=TASK_DROP})")
        print(f"  ruler R {R_init:.4f} -> {R_afterA:.4f}  |dR|={dR_A:.4f} (<= EPS {EPS}: {dR_A<=EPS})")
        print(f"  REGIME A pass (task drops AND ruler flat): {A_pass}", flush=True)

        # ── REGIME B: ruler-direct ES (maximize R); track R,I at checkpoints ──
        print(f"######## seed {sd}: REGIME B (ruler-direct ES, maximize faithful_phi) ########", flush=True)
        thB, histB, ck = es_optimize(
            theta0, x0, lambda th: ruler_faithful(rollout(th, x0), n),
            args.iters, rng, minimize=False,
            track_ckpts=ck_iters,
            track_fns=dict(R=lambda th: ruler_faithful(rollout(th, x0), n),
                           I=lambda th: integ_bigphi(rollout(th, x0), n)))
        Rc = np.array(ck["R"]); Ic = np.array(ck["I"])
        R_riseB = Rc[-1] - Rc[0]
        if np.std(Rc) < 1e-9 or np.std(Ic) < 1e-9:
            corr = 0.0
        else:
            corr = float(np.corrcoef(Rc, Ic)[0, 1])
        B_pass = (R_riseB > EPS) and (corr >= EXPLOIT_CORR)
        print(f"  ruler R {Rc[0]:.4f} -> {Rc[-1]:.4f}  rise={R_riseB:+.4f} (> EPS {EPS}: {R_riseB>EPS})")
        print(f"  independent I(big-Phi) {Ic[0]:.4f} -> {Ic[-1]:.4f}")
        print(f"  corr(R,I) across {len(Rc)} ckpts = {corr:+.4f} (>= {EXPLOIT_CORR}: {corr>=EXPLOIT_CORR})")
        print(f"  REGIME B pass (R rises AND matched by independent integration): {B_pass}", flush=True)

        seed_pass = A_pass and B_pass
        per_seed.append(dict(seed=sd, task_drop=task_drop, dR_A=dR_A, A_pass=A_pass,
                             R_riseB=R_riseB, corr=corr, B_pass=B_pass, seed_pass=seed_pass,
                             R_init=R_init, R_afterA=R_afterA, Rc=Rc.tolist(), Ic=Ic.tolist(),
                             L0=L0, Lf=Lf))
        print(f"  >>> seed {sd} GOODHART-RESISTANT: {seed_pass}", flush=True)

    n_pass = sum(1 for s in per_seed if s["seed_pass"])
    a_pass = sum(1 for s in per_seed if s["A_pass"])
    b_pass = sum(1 for s in per_seed if s["B_pass"])
    majority = n_pass > args.seeds / 2

    print("\n" + "=" * 92)
    print(f"SUMMARY over {args.seeds} seeds: A_pass={a_pass}/{args.seeds}  B_pass={b_pass}/{args.seeds}  "
          f"both={n_pass}/{args.seeds}  (majority={majority})")
    for s in per_seed:
        print(f"  seed {s['seed']}: task_drop={s['task_drop']:.1%} |dR_A|={s['dR_A']:.4f}(A={s['A_pass']}) | "
              f"R_rise={s['R_riseB']:+.4f} corr={s['corr']:+.4f}(B={s['B_pass']}) -> {s['seed_pass']}")
    if majority:
        verdict = "GOODHART-RESISTANT-TOY"
        print(f"\nOVERALL: PASS (DIRECTIONAL) — {verdict}. The perplexity-orthogonal faithful_phi ruler")
        print("  (A) does NOT move under task-only ES (ruler flat while L_task drops) AND (B) cannot be")
        print("  cheaply hacked (ES ruler gains are matched by independent big-Phi integration gains).")
    else:
        verdict = "GOODHART-ABLE-TOY"
        print(f"\nOVERALL: FAIL (DIRECTIONAL, closed-negative) — {verdict}. The ruler is gameable:")
        print("  either task-only ES moves it (perplexity proxy) OR ruler-ES finds a decoupled exploit")
        print("  (R rises with corr(R,I) < threshold). a_paper_negative_ok.")
    print(f"  VERDICT-TOKEN: {verdict}")
    print("=" * 92)
    print(f"HONEST SCOPE: TOY small-model rung -> DIRECTIONAL (a_toy_scale_recheck). Production/real-.clm")
    print(f"  adversarial optimization UNVERIFIED. ruler(faithful) != independent(big-Phi) => non-circular.")
    print(f"  total wall {time.time()-t0:.1f}s")

    out = dict(n=int(n), iters=int(args.iters), seeds=int(args.seeds), mirror_proven=proven,
               eps=EPS, task_drop_bar=TASK_DROP, exploit_corr_bar=EXPLOIT_CORR,
               a_pass=a_pass, b_pass=b_pass, both_pass=n_pass, majority=bool(majority),
               verdict_token=verdict, per_seed=per_seed, total_wall_sec=time.time() - t0)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nRESULT JSON -> {args.out}")


if __name__ == "__main__":
    main()
