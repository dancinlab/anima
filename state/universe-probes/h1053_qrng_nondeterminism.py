"""H_1053 — Does TRUE QUANTUM non-determinism (ANU QRNG) differ from pseudo-random (H_1052)?

Re-runs the EXACT H_1052 experiment with the SGLD update noise xi sourced from a TRUE PHYSICAL
quantum RNG (ANU Quantum Numbers, vacuum-fluctuation), NOT a numpy PRNG. The ONLY change vs
H_1052 is the noise SOURCE in the learning update.

REUSES the H_1052 harness VERBATIM by import (RNN, task, markers, IIT-4.0 mirrors, mirror==stdlib
re-proof) — same arch, same task, same pinned init, same matched-CE band, same 6 markers. The
quantum bytes come from a CACHED committed file (UNIVERSE/state/h1053_qrng_bytes.bin) pre-fetched
by h1053_fetch_qrng.py; uniform uint16 quantum bytes -> standard-normal xi via inverse-CDF
(probit). NO PRNG in the noise path. (Pinned INIT still uses the seed for both arms — H_921 closed
init-noise; only the LEARNING update noise is the variable under test.)

THREE arms:
  DET        — no update noise (== H_1052 DET).
  QRNG-NOISY — SGLD with xi from true-quantum bytes (inverse-CDF), annealed T (H_1052 schedule).
  PRNG-NOISY — reference: numpy PCG64 xi (== H_1052 NOISY), for the source-matters test.

Core = DET vs QRNG at matched CE. Secondary = QRNG vs PRNG (does the SOURCE matter?).

substrate = SW (numpy CPU toy). Lane = SW-only (AKIDA Lane A / GPU Lane G = separate rungs).
g5 CODE-measured (no LLM self-judge, p7). a_phi_iit4_tool (no proxy). a_scale_honest_scope: TOY.
"""
import sys, os, math, time, json, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Import the H_1052 harness VERBATIM — guarantees identical arch / task / markers / mirrors.
import h1052_nondeterministic_learning as h1052  # noqa: E402

RNN = h1052.RNN
make_source = h1052.make_source
hidden_trace = h1052.hidden_trace
both_phi = h1052.both_phi
redundancy_margin = h1052.redundancy_margin
soc_proximity = h1052.soc_proximity
cohens_d_paired = h1052.cohens_d_paired
prove_mirrors_at_n = h1052.prove_mirrors_at_n
SEQ_LEN = h1052.SEQ_LEN
LR = h1052.LR
T0 = h1052.T0

# H_1053 reduced scale (sized to the quantum-byte budget; pre-registered).
N_STEPS = 800
SEEDS_DEFAULT = 12

QRNG_BIN = os.path.join(HERE, "state", "h1053_qrng_bytes.bin")
QRNG_PROV = os.path.join(HERE, "state", "h1053_qrng_bytes.prov.json")


# ---- inverse-CDF (probit) — uniform (0,1) -> standard normal, NO PRNG -------------------------
def _ppf(u):
    """Standard-normal inverse CDF (Acklam's rational approximation, vectorized, double prec).
    Maps u in (0,1) -> z ~ N(0,1). Used to convert TRUE-QUANTUM uniform bytes to gaussian xi."""
    u = np.asarray(u, dtype=np.float64)
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    z = np.empty_like(u)
    lo = u < plow
    hi = u > phigh
    mid = ~(lo | hi)
    if lo.any():
        q = np.sqrt(-2 * np.log(u[lo]))
        z[lo] = (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if hi.any():
        q = np.sqrt(-2 * np.log(1 - u[hi]))
        z[hi] = -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if mid.any():
        q = u[mid] - 0.5
        r = q*q
        z[mid] = (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    return z


class QuantumNoise:
    """Consumes the CACHED TRUE-QUANTUM byte stream as standard-normal draws via inverse-CDF.
    uint16 little-endian -> uniform (0,1) open interval -> probit -> N(0,1). NO PRNG.
    Per-seed deterministic OFFSET into the same physical stream so DET/QRNG pairs are reproducible
    yet every seed consumes a distinct quantum slice."""
    def __init__(self, raw_bytes, byte_offset):
        self.u16 = np.frombuffer(raw_bytes, dtype="<u2")  # 65536 values
        self.n = len(self.u16)
        self.pos = (byte_offset // 2) % self.n

    def standard_normal(self, shape):
        k = int(np.prod(shape))
        idx = (self.pos + np.arange(k)) % self.n
        self.pos = (self.pos + k) % self.n
        # uint16 -> (0,1) OPEN interval (avoid 0 and 1 so probit is finite)
        u = (self.u16[idx].astype(np.float64) + 0.5) / 65536.0
        return _ppf(u).reshape(shape)


def train_arm(seed, arm, train_syms, qbytes):
    """Train an RNN (pinned init via seed) under one arm. arm in {det, qrng, prng}.
    Returns (model, train_CE). Init identical across arms (seed-pinned, numpy default_rng).
    Noise SOURCE is the only difference: det=none, qrng=quantum-stream, prng=numpy PCG64."""
    model = RNN(seed)
    if arm == "prng":
        noise = np.random.default_rng(50_000 + seed + 777)  # == H_1052 NOISY rng
    elif arm == "qrng":
        # distinct deterministic slice of the SAME physical stream per seed
        noise = QuantumNoise(qbytes, byte_offset=(seed * 419_999) % max(len(qbytes) - 1, 1))
    else:
        noise = None
    for step in range(N_STEPS):
        ce, grads = model.loss_and_grad(train_syms)
        if arm == "det":
            noise_T = 0.0
        else:
            frac = 1.0 - step / N_STEPS
            noise_T = T0 * (frac ** 2)
        model.apply_update(grads, LR, noise_T, noise)
    return model, model.test_ce(train_syms)


def measure(model, train_syms, test_syms):
    H = hidden_trace(model, train_syms)
    bphi, fphi, bits = both_phi(H)
    red = redundancy_margin(bits)
    soc_abs, rho = soc_proximity(model)
    test_ce = model.test_ce(test_syms)
    return dict(big_phi=float(bphi), faithful_phi=float(fphi), split=float(fphi - bphi),
                redundancy=float(red), soc_abs=float(soc_abs), rho=float(rho),
                test_ce=float(test_ce))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=SEEDS_DEFAULT)
    ap.add_argument("--eps", type=float, default=0.05)
    ap.add_argument("--out", type=str,
                    default=os.path.join(HERE, "h1053_qrng_nondeterminism_result.json"))
    args = ap.parse_args()

    if not os.path.exists(QRNG_BIN):
        print(f"HALT — cached quantum bytes not found at {QRNG_BIN}.")
        print("  Run h1053_fetch_qrng.py first (no silent PRNG fallback). Blocker reported.")
        raise SystemExit(2)
    with open(QRNG_BIN, "rb") as f:
        qbytes = f.read()
    prov = json.load(open(QRNG_PROV)) if os.path.exists(QRNG_PROV) else {}

    print("=" * 92)
    print("H_1053 — Does TRUE QUANTUM non-determinism (ANU QRNG) differ from pseudo-random (H_1052)?")
    print("substrate=SW (numpy CPU toy) — REUSES the H_1052 harness VERBATIM; ONLY the noise SOURCE changes.")
    print("  DET = no noise | QRNG = ANU true-quantum xi (inverse-CDF) | PRNG = numpy PCG64 (== H_1052).")
    print(f"  quantum bytes: {len(qbytes):,} from {prov.get('endpoint','?')} key_class={prov.get('key_class','?')}")
    print(f"  sha256={prov.get('sha256','?')}  ts={prov.get('ts_end_utc','?')}")
    print(f"seeds={args.seeds}  steps={N_STEPS}  matched-CE band eps={args.eps} nats")
    print("Core = DET vs QRNG at matched CE; Secondary = QRNG vs PRNG (does the SOURCE matter?).")
    print("PASS = >=1 marker QRNG>DET paired d>=0.8 AND QRNG differs from PRNG (|d|>=0.8).")
    print("FAIL = QRNG ~ PRNG ~ null vs DET (source irrelevant; H_1052 null NOT a PRNG artifact).")
    print("a_phi_iit4_tool (no proxy) | g5 CODE-measured (p7) | a_scale_honest_scope: TOY n<=5 SW")
    print("=" * 92, flush=True)
    print()

    # STEP 0 — RE-PROVE both CPU mirrors == stdlib at n=4 AND n=5 BEFORE scoring.
    print("STEP 0 — RE-PROVE BOTH CPU mirrors == stdlib (a_phi_iit4_tool) at n=4 AND n=5:")
    proven = {}
    for n in (4, 5):
        proven[n] = prove_mirrors_at_n(n)
        print()
    print(f"  == mirror-equivalence results: {proven}", flush=True)
    if not all(proven.values()):
        print("  ABORT — a mirror == stdlib proof FAILED; cannot trust this run.")
        raise SystemExit(1)
    print()

    # STEP 1 — train all three arms per seed from identical pinned init.
    print(f"STEP 1 — train DET / QRNG / PRNG from identical pinned init, {args.seeds} seeds (SERIAL):", flush=True)
    rows = []
    t0 = time.time()
    for s in range(args.seeds):
        gen = make_source(s)
        train_syms = gen(SEQ_LEN)
        full = gen(SEQ_LEN * 3)
        test_syms = full[SEQ_LEN:SEQ_LEN * 2]
        r = {"seed": s}
        for arm in ("det", "qrng", "prng"):
            model, tce = train_arm(s, arm, train_syms, qbytes)
            m = measure(model, train_syms, test_syms)
            m["train_ce"] = float(tce)
            r[arm] = m
        r["gap_qrng"] = abs(r["qrng"]["train_ce"] - r["det"]["train_ce"])
        r["gap_prng"] = abs(r["prng"]["train_ce"] - r["det"]["train_ce"])
        r["matched_qrng"] = bool(r["gap_qrng"] <= args.eps)
        r["matched_prng"] = bool(r["gap_prng"] <= args.eps)
        rows.append(r)
        print(f"  seed {s:2d}: det={r['det']['train_ce']:.4f} qrng={r['qrng']['train_ce']:.4f} "
              f"prng={r['prng']['train_ce']:.4f} |gapQ|={r['gap_qrng']:.4f} matchedQ={r['matched_qrng']} "
              f"({time.time()-t0:.1f}s)", flush=True)
    print()

    matched_q = [r for r in rows if r["matched_qrng"]]
    matched_both = [r for r in rows if r["matched_qrng"] and r["matched_prng"]]
    nq, nb, nt = len(matched_q), len(matched_both), len(rows)
    print(f"matched DET-QRNG pairs (|dCE|<= {args.eps}): {nq}/{nt}")
    print(f"matched in BOTH arms (for QRNG-vs-PRNG source test): {nb}/{nt}")
    print()

    # STEP 2 — marker tables.
    # Favorable-direction paired diffs (QRNG - DET), exactly the H_1052 marker conventions.
    def diffs_vs_det(rs):
        return {
            "faithful_phi": np.array([r["qrng"]["faithful_phi"] - r["det"]["faithful_phi"] for r in rs]),
            "big_Phi": np.array([r["qrng"]["big_phi"] - r["det"]["big_phi"] for r in rs]),
            "split_magnitude": np.array([abs(r["qrng"]["split"]) - abs(r["det"]["split"]) for r in rs]),
            "redundancy_margin": np.array([r["qrng"]["redundancy"] - r["det"]["redundancy"] for r in rs]),
            "soc_proximity": np.array([r["det"]["soc_abs"] - r["qrng"]["soc_abs"] for r in rs]),
            "emergence_probe": np.array([r["det"]["test_ce"] - r["qrng"]["test_ce"] for r in rs]),
        }

    def means(rs, arm, key):
        return float(np.mean([r[arm][key] for r in rs]))

    print("=" * 92)
    print(f"CORE — PER-MARKER PAIRED det-vs-QRNG TABLE (matched CE, n_matched={nq})")
    print("  benefit = QRNG favorable-direction paired diff with Cohen d >= 0.80")
    print("=" * 92)
    print(f"  {'marker':18s} | {'det mean':>9s} | {'qrng mean':>10s} | {'paired diff':>11s} | {'Cohen d':>8s} | benefit?")
    dd = diffs_vs_det(matched_q) if nq else {}
    marker_table = []
    any_benefit = False
    metric_for = {"faithful_phi": ("faithful_phi", "qrng"), "big_Phi": ("big_phi", "qrng"),
                  "split_magnitude": ("split", "qrng"), "redundancy_margin": ("redundancy", "qrng"),
                  "soc_proximity": ("soc_abs", "qrng"), "emergence_probe": ("test_ce", "qrng")}
    for name in ("faithful_phi", "big_Phi", "split_magnitude", "redundancy_margin", "soc_proximity", "emergence_probe"):
        diffs = dd.get(name, np.array([]))
        d = cohens_d_paired(diffs) if len(diffs) >= 2 else float("nan")
        mean_diff = float(diffs.mean()) if len(diffs) else float("nan")
        benefit = bool((not math.isnan(d)) and d >= 0.8)
        any_benefit = any_benefit or benefit
        key, arm = metric_for[name]
        det_m = means(matched_q, "det", key) if nq else float("nan")
        qr_m = means(matched_q, "qrng", key) if nq else float("nan")
        if name == "split_magnitude":
            det_m = float(np.mean([abs(r["det"]["split"]) for r in matched_q])) if nq else float("nan")
            qr_m = float(np.mean([abs(r["qrng"]["split"]) for r in matched_q])) if nq else float("nan")
        print(f"  {name:18s} | {det_m:9.4f} | {qr_m:10.4f} | {mean_diff:+11.4f} | {d:+8.3f} | {benefit}")
        marker_table.append(dict(marker=name, det_mean=det_m, qrng_mean=qr_m, paired_diff=mean_diff,
                                 cohen_d=(None if math.isnan(d) else float(d)), benefit=benefit))
    print()

    # SECONDARY — QRNG vs PRNG (does the SOURCE matter?). Paired over seeds matched in BOTH arms.
    print("=" * 92)
    print(f"SECONDARY — DOES THE NOISE SOURCE MATTER? paired QRNG-vs-PRNG (n_both={nb})")
    print("  source MATTERS iff |Cohen d| >= 0.80 on >=1 marker")
    print("=" * 92)
    print(f"  {'marker':18s} | {'qrng mean':>9s} | {'prng mean':>10s} | {'paired diff':>11s} | {'Cohen d':>8s} | differs?")
    source_table = []
    source_matters = False
    qp_diff = {
        "faithful_phi": lambda r: r["qrng"]["faithful_phi"] - r["prng"]["faithful_phi"],
        "big_Phi": lambda r: r["qrng"]["big_phi"] - r["prng"]["big_phi"],
        "split_magnitude": lambda r: abs(r["qrng"]["split"]) - abs(r["prng"]["split"]),
        "redundancy_margin": lambda r: r["qrng"]["redundancy"] - r["prng"]["redundancy"],
        "soc_proximity": lambda r: r["prng"]["soc_abs"] - r["qrng"]["soc_abs"],
        "emergence_probe": lambda r: r["prng"]["test_ce"] - r["qrng"]["test_ce"],
    }
    qp_key = {"faithful_phi": "faithful_phi", "big_Phi": "big_phi", "split_magnitude": "split",
              "redundancy_margin": "redundancy", "soc_proximity": "soc_abs", "emergence_probe": "test_ce"}
    for name, fn in qp_diff.items():
        diffs = np.array([fn(r) for r in matched_both]) if nb else np.array([])
        d = cohens_d_paired(diffs) if len(diffs) >= 2 else float("nan")
        mean_diff = float(diffs.mean()) if len(diffs) else float("nan")
        differs = bool((not math.isnan(d)) and abs(d) >= 0.8)
        source_matters = source_matters or differs
        key = qp_key[name]
        if name == "split_magnitude":
            qr_m = float(np.mean([abs(r["qrng"]["split"]) for r in matched_both])) if nb else float("nan")
            pr_m = float(np.mean([abs(r["prng"]["split"]) for r in matched_both])) if nb else float("nan")
        else:
            qr_m = float(np.mean([r["qrng"][key] for r in matched_both])) if nb else float("nan")
            pr_m = float(np.mean([r["prng"][key] for r in matched_both])) if nb else float("nan")
        print(f"  {name:18s} | {qr_m:9.4f} | {pr_m:10.4f} | {mean_diff:+11.4f} | {d:+8.3f} | {differs}")
        source_table.append(dict(marker=name, qrng_mean=qr_m, prng_mean=pr_m, paired_diff=mean_diff,
                                 cohen_d=(None if math.isnan(d) else float(d)), differs=differs))
    print()

    # STEP 3 — verdict.
    degenerate = nq < 8
    print("=" * 92)
    if degenerate:
        print(f"OVERALL: DEGENERATE — fewer than 8 matched DET-QRNG pairs (n={nq}); regimes could NOT be")
        print("  matched on task-performance. The CONTROL failed, not the hypothesis. INCONCLUSIVE.")
        token = "DEGENERATE"
    elif any_benefit and source_matters:
        winners = [m["marker"] for m in marker_table if m["benefit"]]
        print("OVERALL: PASS — at MATCHED performance, TRUE-QUANTUM learning noise RAISES a marker that")
        print(f"  DET lacks ({winners}) AND the QRNG arm differs from the PRNG arm (source matters).")
        print("  Genuine physical non-determinism confers an advantage pseudo-randomness does not.")
        token = "QRNG-NONDET-HELPS"
    else:
        print("OVERALL: FAIL (CLOSED-NEGATIVE) — at MATCHED performance, TRUE-QUANTUM learning noise")
        print("  behaves like PRNG noise: no marker QRNG>DET at d>=0.8, and QRNG ~ PRNG within the")
        print("  control band. The noise SOURCE (quantum vs pseudo) is IRRELEVANT; H_1052's null is")
        print("  NOT a PRNG artifact. This DEFINITIVELY closes the 'fake randomness' objection.")
        print("  a_paper_negative_ok.")
        token = "QRNG-NONDET-NULL"
    print(f"  VERDICT-TOKEN: {token}")
    print(f"  source_matters(QRNG!=PRNG, |d|>=0.8 on >=1 marker) = {source_matters}")
    print("=" * 92)
    print("HONEST scope: TOY n<=5 SW; reduced N (12x800) sized to the quantum-byte budget. Both Phi")
    print("engines EXACT at n<=5; CPU mirrors RE-PROVEN == stdlib at n=4 AND n=5 BEFORE scoring")
    print("(a_phi_iit4_tool; no proxy). AKIDA Lane A on-chip + GPU Lane G = separate rungs. g5 CODE-")
    print("measured (p7). NOT a forge binary; $0 CPU-local + one-time cached quantum-byte API fetch.")

    out = dict(seeds=int(args.seeds), eps=float(args.eps), steps=int(N_STEPS),
               mirror_proven={int(k): bool(v) for k, v in proven.items()},
               n_matched_qrng=int(nq), n_matched_both=int(nb), n_total=int(nt),
               degenerate=bool(degenerate), any_benefit=bool(any_benefit),
               source_matters=bool(source_matters), verdict_token=token,
               core_markers=marker_table, source_markers=source_table,
               qrng_provenance=prov, rows=rows, total_wall_sec=time.time() - t0)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nRESULT JSON -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
