"""H_1048 — Structure-reading ruler: does connectivity-weighted Phi catch arch-bound structure
that an I/O-only Phi ruler is blind to?  (controlled TOY pair -> DIRECTIONAL; real pair torch-gated.)

Two systems with MATCHED I/O statistics but DIFFERENT connectivity:
  A = STRUCTURED (ConvMoE-like local ring + dilated tap) ; B = FLAT (transformer-like all-to-all),
  coupling TUNED so MI(X_B) matches MI(X_A) total within MATCH_TOL (matched I/O -> I/O-only Phi equal).
Two rulers: I/O-only Phi = faithful_phi_from_mi(MI) ; structure Phi = faithful_phi_from_mi(MI (x) Ghat).
Engine = stdlib faithful_phi_from_mi (exact MIP-EI, mirror RE-PROVEN == stdlib at n=4,5). a_phi_iit4_tool.
Frozen bar: state/h104x_phi/H_1048_FREEZE.txt.

Run: python3 -u h1048_structure_reading_ruler.py [--n 6] [--seeds 5] [--T 4000]
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

build_mi_matrix = h1004.build_mi_matrix
faithful_phi_from_mi = h1004.faithful_phi_from_mi
binary_seq_to_faithful_state = h1004.binary_seq_to_faithful_state
prove_mirrors_at_n = h1012.prove_mirrors_at_n

# frozen bar
EPS_IO = 0.05
MARGIN = 0.15
MATCH_TOL = 0.10


def structured_graph(n, rng):
    """ConvMoE-like: ring (i-1,i+1) + one dilated tap (i+2) — local sparse connectivity."""
    G = np.zeros((n, n))
    for i in range(n):
        for j in (i - 1, i + 1, i + 2):
            G[i, j % n] = 1.0
    G = (G + G.T) > 0  # symmetric adjacency
    return G.astype(float)


def flat_graph(n):
    """Transformer-like: all-to-all diffuse connectivity."""
    G = np.ones((n, n)) - np.eye(n)
    return G


def simulate(G, beta, n, T, rng):
    """Gaussian graphical model: precision Omega = I - beta*A (A=adjacency); sample N(0, Omega^-1),
    binarize at per-unit median. Connectivity G directly shapes pairwise MI (no collapse/decorrelation).
    beta is the coupling knob; kept below 1/spectral-radius(A) for positive-definiteness."""
    A = G
    sr = float(np.max(np.abs(np.linalg.eigvalsh(A)))) if n > 1 else 1.0
    beta_eff = min(beta, 0.95 / (sr + 1e-9))
    Omega = np.eye(n) - beta_eff * A
    # symmetric PD guard
    Omega = 0.5 * (Omega + Omega.T)
    w = np.linalg.eigvalsh(Omega)
    if w.min() <= 1e-6:
        Omega += (1e-6 - w.min() + 1e-6) * np.eye(n)
    Sigma = np.linalg.inv(Omega)
    L = np.linalg.cholesky(0.5 * (Sigma + Sigma.T))
    Z = rng.standard_normal((T, n))
    X = Z @ L.T
    bits = (X > np.median(X, axis=0, keepdims=True)).astype(int)
    return bits


def mi_of_bits(bits, n):
    state, sn, dim = binary_seq_to_faithful_state(bits.astype(int), n)
    return build_mi_matrix(state, sn, dim, 2)


def normadj(G):
    Gh = G.copy()
    rs = Gh.sum(axis=1, keepdims=True)
    rs[rs == 0] = 1.0
    return Gh / rs


def rulers(bits, G, n):
    M = mi_of_bits(bits, n)
    io = faithful_phi_from_mi(M, n)
    Gh = normadj(G)
    # symmetric weight for the (symmetric) MI matrix
    Wm = 0.5 * (Gh + Gh.T)
    struct = faithful_phi_from_mi(M * Wm, n)
    return float(io), float(struct), float(np.triu(M, 1).sum())


def tune_flat_alpha(G_flat, target_mitot, n, T, seed, lo=0.0, hi=1.0, iters=24):
    """Bisection on flat coupling beta so MI_total(X_flat) ~= target_mitot (matched I/O)."""
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        rng = np.random.default_rng(seed + 777)
        bits = simulate(G_flat, mid, n, T, rng)
        mit = float(np.triu(mi_of_bits(bits, n), 1).sum())
        if mit < target_mitot:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--T", type=int, default=4000)
    ap.add_argument("--alphaA", type=float, default=0.12, help="structured-system coupling beta")
    ap.add_argument("--out", default=os.path.join(HERE, "h1048_structure_reading_ruler_result.json"))
    args = ap.parse_args()
    n = args.n

    print("=" * 92)
    print("H_1048 — structure-reading (connectivity-weighted) Phi vs I/O-only Phi on a matched arch-bound pair")
    print("engine=stdlib faithful_phi_from_mi (exact MIP-EI) | mirror RE-PROVEN == stdlib at n=4,5 | a_phi_iit4_tool")
    print(f"FROZEN BAR: PASS = |structPhi_A-structPhi_B|>=MARGIN({MARGIN}) AND |ioPhi_A-ioPhi_B|<=EPS_IO({EPS_IO})")
    print(f"           on a VALID matched pair (MI_total within MATCH_TOL={MATCH_TOL}). TOY -> DIRECTIONAL.")
    print(f"n={n} seeds={args.seeds} T={args.T}")
    print("=" * 92, flush=True)

    print("\nSTEP 0 — RE-PROVE CPU mirror == stdlib at n=4,5 (a_phi_iit4_tool):")
    proven = {k: bool(prove_mirrors_at_n(k)) for k in (4, 5)}
    print(f"  mirror-equivalence: {proven}")
    if not all(proven.values()):
        raise SystemExit("mirror proof FAILED — abort")

    per_seed = []
    t0 = time.time()
    for sd in range(args.seeds):
        rng = np.random.default_rng(500 + sd)
        G_A = structured_graph(n, rng)
        G_B = flat_graph(n)
        # System A (structured)
        bitsA = simulate(G_A, args.alphaA, n, args.T, np.random.default_rng(500 + sd))
        ioA, structA, mitotA = rulers(bitsA, G_A, n)
        # Tune B (flat) to match A's MI-total, then measure
        alphaB = tune_flat_alpha(G_B, mitotA, n, args.T, 500 + sd)
        bitsB = simulate(G_B, alphaB, n, args.T, np.random.default_rng(500 + sd + 777))
        ioB, structB, mitotB = rulers(bitsB, G_B, n)

        match_err = abs(mitotA - mitotB) / (abs(mitotA) + 1e-12)
        valid = match_err <= MATCH_TOL
        d_io = abs(ioA - ioB)
        d_struct = abs(structA - structB)
        io_matched = d_io <= EPS_IO
        struct_sep = d_struct >= MARGIN
        seed_pass = valid and io_matched and struct_sep
        per_seed.append(dict(seed=sd, alphaB=alphaB, mitotA=mitotA, mitotB=mitotB, match_err=match_err,
                             valid=valid, ioA=ioA, ioB=ioB, d_io=d_io, structA=structA, structB=structB,
                             d_struct=d_struct, io_matched=io_matched, struct_sep=struct_sep,
                             seed_pass=seed_pass))
        print(f"  seed {sd}: MI_tot A={mitotA:.3f} B={mitotB:.3f} match_err={match_err:.1%} valid={valid} | "
              f"ioPhi A={ioA:.3f} B={ioB:.3f} dIO={d_io:.3f}(<= {EPS_IO}:{io_matched}) | "
              f"structPhi A={structA:.3f} B={structB:.3f} dStruct={d_struct:.3f}(>= {MARGIN}:{struct_sep}) "
              f"-> pass={seed_pass}", flush=True)

    valid_seeds = [s for s in per_seed if s["valid"]]
    n_valid = len(valid_seeds)
    n_pass = sum(1 for s in valid_seeds if s["seed_pass"])
    if n_valid == 0:
        verdict = "INVALID-NO-MATCHED-PAIR"
        majority = False
    else:
        majority = n_pass > n_valid / 2
        verdict = "STRUCTURE-READING-ADDS-POWER-TOY" if majority else "IO-SUFFICIENT-TOY"

    print("\n" + "=" * 92)
    print(f"SUMMARY: valid matched pairs={n_valid}/{args.seeds}  PASS(struct separates & I/O matched)={n_pass}/{n_valid}")
    print("=" * 92)
    if n_valid == 0:
        print("OVERALL: INVALID — the flat comparator could not be tuned to a matched-I/O pair within MATCH_TOL")
        print("  on any seed (no valid arch-bound pair). Not a PASS/FAIL — a measurement-validity INVALID.")
    elif majority:
        print(f"OVERALL: PASS (DIRECTIONAL) — {verdict}. On matched-I/O pairs (I/O-only Phi within EPS_IO), the")
        print("  structure-reading (connectivity-weighted) Phi SEPARATES the structured (ConvMoE-like) system")
        print("  from the flat (transformer-like) one by >= MARGIN. Reading architecture adds discriminative")
        print("  power the I/O-only ruler lacks — 'instrument not score' at the MEASUREMENT level (toy).")
    else:
        print(f"OVERALL: FAIL (DIRECTIONAL, closed-negative) — {verdict}. On matched-I/O pairs the structure-")
        print("  reading Phi does NOT separate beyond the I/O-only ruler (< MARGIN) — connectivity weighting adds")
        print("  nothing; Phi-structure is already visible in I/O statistics (a_paper_negative_ok).")
    print(f"  VERDICT-TOKEN: {verdict}")
    print("=" * 92)
    print("HONEST SCOPE: TOY controlled pair -> DIRECTIONAL. TERMINAL rung = real trained ConvMoE .clm vs real")
    print("  transformer LoRA-matched to byte-I/O (H_1036 torch pipeline on summer GPU) + structure-reading Phi")
    print("  from the ACTUAL ConvMoE dilated-conv + MoE-routing graph — a torch build, recorded as the follow-on.")
    print(f"  total wall {time.time()-t0:.1f}s")

    out = dict(n=int(n), seeds=int(args.seeds), T=int(args.T), mirror_proven=proven,
               eps_io=EPS_IO, margin=MARGIN, match_tol=MATCH_TOL,
               n_valid=n_valid, n_pass=n_pass, majority=bool(majority), verdict_token=verdict,
               per_seed=per_seed, total_wall_sec=time.time() - t0)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nRESULT JSON -> {args.out}")


if __name__ == "__main__":
    main()
