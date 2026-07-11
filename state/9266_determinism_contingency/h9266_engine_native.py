"""
H_9266 engine-native — determinism vs contingency, RIGOROUS spec (Fable design · frozen bar = FROZEN_BAR.md).

Supersedes the earlier quick probe (which was RIGGED: DECOUP used a clean/noise-free latent for Phi ->
"noise raises Phi" artifact, inflated Dsigma). Fable caught it. This version:
  - DECOUP shares COUP's base B + independent eps'' -> Phi-input marginal matched (only the joint mask<->rows differs)
  - sigma = EMIT-CONDITIONED, SHUFFLE-REFERENCED Phi difference (joint signature, not unconditional Phi)
  - cols_x excludes gate lane 0 (leakage defense) ; alpha=0 arm decomposes cross-lane vs gate-overlap
  - V-gates (FORCED detector-alive, NULL false-positive, marginal-match) -> INVALID not FAIL

ALL ops REAL engine_cli (a_eval_py_canonical, TERMINAL-eligible): ci_emit_decision, ci_phi_iit4,
ci_emit_drive, topo_apply, topo_brain_adjacency.

Env: H9266_T (default 8192), H9266_SEEDS (csv, default full), H9266_BSCALE (subset for smoke).
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "core"))
import numpy as np
import engine_cli as E

LANES   = 15
T       = int(os.environ.get("H9266_T", "8192"))
SEEDS   = [int(x) for x in os.environ.get("H9266_SEEDS", "7,11,13,17,23").split(",")]
COLS_X  = [3, 2, 13, 5, 7, 9, 14]       # gate-lane-0 EXCLUDED core (primary sigma)
CORE    = [0, 3, 2, 13, 5, 7, 9, 14]    # full core (secondary)
ALPHA   = 0.3
N_STAR  = 64
J_SUB   = 8
K_PERM  = 8
KAPPA_F = 0.5
ADJ     = E.topo_brain_adjacency()
BSCALE  = [float(x) for x in os.environ.get("H9266_BSCALE",
           "0,0.25,-0.25,0.5,-0.5,0.75,-0.75,1.0,-1.0,1.5,-1.5,2.5,-2.5").split(",")]

def rng_(seed, off): return np.random.default_rng(seed * 1000 + off)

def build_base(seed):
    rb = rng_(seed, 0)
    lat = rb.standard_normal(T)
    eta = rb.standard_normal((T, LANES))
    m = np.zeros(LANES); m[0] = 0.5; m[4] = 0.5
    return m[None, :] + 0.9 * lat[:, None] + 0.2 * eta      # T×15

def inject(X, v):
    Y = X.copy(); Y[:, 0] += v; Y[:, 4] += v; return Y

def couple(X, alpha=ALPHA):
    return np.asarray(E.topo_apply(X.tolist(), ADJ, alpha))

def emit_mask(P):
    return np.fromiter((1 if E.ci_emit_decision(P[t].tolist()) else 0 for t in range(len(P))),
                       dtype=np.int64, count=len(P))

def _phi_hat(rows, cols, rng):
    n = len(rows)
    if n < N_STAR: return None
    return float(np.mean([E.ci_phi_iit4(rows[rng.choice(n, N_STAR, replace=False)].tolist(), cols)
                          for _ in range(J_SUB)]))

def sigma_cond(rows, mask, cols, paired_seed):
    """emit-conditioned shuffle-referenced sigma. paired_seed shared COUP<->DECOUP -> identical idx/perm."""
    rng = np.random.default_rng(paired_seed)
    em = rows[mask == 1]; si = rows[mask == 0]
    if len(em) < N_STAR or len(si) < N_STAR: return None      # bin PENDING (V4)
    pe = _phi_hat(em, cols, rng); ps = _phi_hat(si, cols, rng)
    D_real = abs(pe - ps)
    Dpi = []
    for _ in range(K_PERM):
        mp = rng.permutation(mask)
        Dpi.append(abs(_phi_hat(rows[mp == 1], cols, rng) - _phi_hat(rows[mp == 0], cols, rng)))
    return D_real - float(np.median(Dpi))

def fold_bin(psi):
    d = abs(psi - 0.5)
    if d < 0.05: return "knife"
    if d < 0.20: return "mid"
    if d < 0.40: return "shoulder"
    return "sat"

def measure_seed(seed):
    B = build_base(seed)
    reps = rng_(seed, 1); reps2 = rng_(seed, 2)
    # calibration sigma_d from DET @ b=0
    P0 = couple(inject(B, 0.0))
    sigma_d = float(np.std([E.ci_emit_drive(P0[t].tolist()) for t in range(min(T, 2048))]))
    eps  = reps.standard_normal(T)  * sigma_d          # COUP noise
    eps2 = reps2.standard_normal(T) * sigma_d          # DECOUP independent, same dist
    rows_out = []  # per b-point: dict
    null_mask_src = emit_mask(couple(inject(build_base(seed + 97), 0.0)))  # foreign mask for NULL
    for bs in BSCALE:
        b = bs * sigma_d
        P_DET = couple(inject(B, b))
        P_C   = couple(inject(B, b + eps))
        P_D   = couple(inject(B, b + eps2))
        mC = emit_mask(P_C)
        psi = float(mC.mean())
        ps = seed * 100000 + int((bs + 3) * 1000)      # paired seed for this b-point
        s_det = sigma_cond(P_DET, emit_mask(P_DET), COLS_X, ps)
        s_cou = sigma_cond(P_C, mC, COLS_X, ps)
        s_dec = sigma_cond(P_D, mC, COLS_X, ps)         # SAME mask mC, rows=P_D (marginal-matched)
        # FORCED (detector-alive positive control): imprint mask-correlated SHARED structure across
        # cols_x -> emit-class genuinely MORE integrated (real Phi lift, not a mean shift Phi ignores).
        lane_std = float(np.std(P_C[:, COLS_X]))
        g_shared = rng_(seed, 5).standard_normal(T)
        P_F = P_C.copy()
        for c in COLS_X:
            P_F[:, c] += KAPPA_F * lane_std * mC * g_shared
        s_forced = sigma_cond(P_F, mC, COLS_X, ps)
        # NULL (false-positive control): foreign mask, COUP rows
        s_null = sigma_cond(P_C, null_mask_src, COLS_X, ps)
        # alpha=0 decomposition (gate-lane leakage vs cross-lane)
        P_C0 = couple(inject(B, b + eps), alpha=0.0); P_D0 = couple(inject(B, b + eps2), alpha=0.0)
        s_cou0 = sigma_cond(P_C0, emit_mask(P_C0), COLS_X, ps)
        s_dec0 = sigma_cond(P_D0, emit_mask(P_C0), COLS_X, ps)
        # marginal V3: unconditional Phi COUP vs DECOUP
        rphi = np.random.default_rng(ps + 7)
        phi_uc = _phi_hat(P_C, COLS_X, rphi); phi_ud = _phi_hat(P_D, COLS_X, rphi)
        rows_out.append(dict(bs=bs, psi=psi, bin=fold_bin(psi),
                             det=s_det, coup=s_cou, dec=s_dec, forced=s_forced, null=s_null,
                             coup0=s_cou0, dec0=s_dec0, phi_uc=phi_uc, phi_ud=phi_ud))
    return rows_out

def agg(points, key):
    vals = [p[key] for p in points if p[key] is not None]
    return float(np.median(vals)) if vals else None

print(f"=== H_9266 ENGINE-NATIVE (Fable spec · T={T} seeds={SEEDS}) ===")
all_rows = {}
for sd in SEEDS:
    print(f"[seed {sd}] measuring...", flush=True)
    all_rows[sd] = measure_seed(sd)

# aggregate per fold-bin across b-points, per seed, then 5-seed
BINS = ["knife", "mid", "shoulder", "sat"]
def dsig_bin(rows, bn):
    pts = [p for p in rows if p["bin"] == bn]
    c = agg(pts, "coup"); d = agg(pts, "dec")
    return (c - d) if (c is not None and d is not None) else None

print(f"\n{'seed':>5} | " + " ".join(f"{b:>9}" for b in BINS) + " | forced@knife null@knife V3marg")
seed_pass = []
for sd in SEEDS:
    rows = all_rows[sd]
    dvals = {b: dsig_bin(rows, b) for b in BINS}
    kn = [p for p in rows if p["bin"] == "knife"]
    forced_k = agg(kn, "forced"); null_k = agg(kn, "null")
    v3 = max((abs(p["phi_uc"] - p["phi_ud"]) for p in rows if p["phi_uc"] and p["phi_ud"]), default=9.9)
    def fmt(x): return f"{x:>9.4f}" if x is not None else f"{'PEND':>9}"
    print(f"{sd:>5} | " + " ".join(fmt(dvals[b]) for b in BINS) +
          f" | {fmt(forced_k)} {fmt(null_k)} {v3:.3f}")
    dk = dvals["knife"]; dsat = dvals["sat"]; dmid = dvals["mid"]; dsh = dvals["shoulder"]
    v1 = forced_k is not None and forced_k >= 0.10
    v2 = null_k is not None and abs(null_k) <= 0.02
    v3ok = v3 <= 0.05
    invalid = not (v1 and v2 and v3ok)
    p_pass = (dk is not None and dk >= 0.10 and
              (dsat is None or dk - dsat >= 0.05) and
              (dmid is None or dk > dmid) and (dsh is None or dk > dsh))
    seed_pass.append(("INVALID" if invalid else ("PASS" if p_pass else "FAIL"),
                      dict(v1=v1, v2=v2, v3=v3ok, dk=dk)))

verds = [s[0] for s in seed_pass]
npass = verds.count("PASS"); ninval = verds.count("INVALID")
print(f"\nseed verdicts: {verds}")
print(f"5-seed: PASS={npass} FAIL={verds.count('FAIL')} INVALID={ninval}")
if ninval >= 3:
    final = "INVALID (V-gate majority)"
elif npass >= 3:
    final = "PASS (ENGINE-NATIVE · Ψ=½ 국소 BIND · Fable spec)"
else:
    final = "FAIL / NULL (ENGINE-NATIVE)"
print(f"\nVERDICT: {final}")
json.dump({"seeds": SEEDS, "T": T, "rows": {str(k): v for k, v in all_rows.items()},
           "verdicts": verds, "final": final},
          open(os.path.join(os.path.dirname(__file__), "h9266_engine_native_out.json"), "w"),
          default=lambda o: None, ensure_ascii=False)
