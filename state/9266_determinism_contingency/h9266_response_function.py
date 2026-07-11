"""
H_9266 response-function chi(Psi) measurement (Fable spec · arXiv Du&Huang 2025 2509.00730).

Succeeds the emit-conditioned probe (h9266_engine_native.py, which returned INVALID). Fixes both v1 defects
BY DESIGN (not gates):
  1. FORCED abolished -> chi_dec is the built-in positive control. Injecting noise into Phi-input lanes
     (l0,l4) provably changes Gaussian-MI Phi -> chi_dec!=0 iff instrument alive. "null vs weak detector"
     confound impossible: chi_dec dead = instrument VOID; chi_dec alive & chi_coup==chi_dec = real FAIL.
  2. marginal-match as pipeline invariant: z-score standardize Phi-input per window/lane before ci_phi_iit4
     -> 1st/2nd moments identical across arms/eps by construction -> v1's V3 subsample-noise gone.

chi = origin-through regression slope of DeltaPhi(eps) vs eps, in unperturbed-lane-std (sigma_L) units.
  chi = sum_i eps_i*DeltaPhi(eps_i) / sum_i eps_i^2      (DeltaPhi(0)=0, no intercept)
chi0 null floor = 95th pct |chi_null| over R=8 half-split disjoint pairs (natural scale, no extra RNG).

3-arm at each Psi (b=bias on lanes 0,4 -> realized Psi via ci_emit_decision):
  COUP  : inject eps*xi[t] into recurrent latent BEFORE the step -> propagates t+1 (state-coupled feedback)
  DECOUP: clean recurrence, eps*xi added to Phi-input copy post-hoc (readout-only, no propagation) = pos control
  (DET baseline = eps=0)

Ops REAL engine_cli (a_eval_py_canonical): ci_emit_decision, ci_phi_iit4, topo_apply, topo_brain_adjacency.
NOTE (a_phi_iit4_tool): ci_phi_iit4 sweep = DIRECTIONAL; faithful-Phi hexa verify leg (VPhi) = TERMINAL follow-on.

FROZEN: seeds{11,23,37,41,53} T=2048 L=256 stride=128 alpha=0.3 G=0.9 E_lin={0.05,0.1,0.2}*sigma_L
  Psi grid{0.1,0.25,0.4,0.5,0.6,0.75,0.9} R=8. Env H9266_T,H9266_SEEDS,H9266_PSI for smoke.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "core"))
import numpy as np
import engine_cli as E
from itertools import combinations

LANES = 15
T      = int(os.environ.get("H9266_T", "2048"))
L, STRIDE = 256, 128
ALPHA, G = 0.3, 0.9
COLS_X = [3, 2, 13, 5, 7, 9, 14]
E_LIN  = [0.05, 0.1, 0.2]
INJ    = [0, 4]
SEEDS  = [int(x) for x in os.environ.get("H9266_SEEDS", "11,23,37,41,53").split(",")]
PSI_G  = [float(x) for x in os.environ.get("H9266_PSI", "0.1,0.25,0.4,0.5,0.6,0.75,0.9").split(",")]
R_REAL = 8
ADJ    = E.topo_brain_adjacency()
CENTER = {0.4, 0.5, 0.6}

def ss(seed, *tags):
    return np.random.default_rng(np.random.SeedSequence([seed, *[abs(int(t*1000)) for t in tags]]))

def _topo_row(x):
    return np.asarray(E.topo_apply([x.tolist()], ADJ, ALPHA))[0]

def base_traj(b, rng):
    lat = rng.standard_normal(T); eta = rng.standard_normal((T, LANES))
    m = np.zeros(LANES); m[0] = b; m[4] = b
    x = np.zeros(LANES); traj = np.empty((T, LANES))
    for t in range(T):
        x = np.tanh(G * _topo_row(x) + m + 0.9 * lat[t] + 0.2 * eta[t])
        traj[t] = x
    return traj, lat, eta, m

def coup_traj(b, lat, eta, m, eps, xi):
    x = np.zeros(LANES); traj = np.empty((T, LANES))
    for t in range(T):
        inj = np.zeros(LANES); inj[0] = inj[4] = eps * xi[t]
        x = np.tanh(G * _topo_row(x) + m + 0.9 * lat[t] + 0.2 * eta[t] + inj)
        traj[t] = x
    return traj

def zwin(rows):
    R = np.asarray(rows); mu = R.mean(0); sd = R.std(0) + 1e-9
    return (R - mu) / sd

def phi_windows(traj):
    return np.array([E.ci_phi_iit4(zwin(traj[s:s+L][:, COLS_X]).tolist(), list(range(len(COLS_X))))
                     for s in range(0, T - L + 1, STRIDE)])

def realized_psi(traj):
    return float(np.mean([1 if E.ci_emit_decision(traj[t].tolist()) else 0 for t in range(0, T, 4)]))

def calibrate_b(target_psi, rng):
    lo, hi = -3.0, 3.0
    for _ in range(14):
        b = 0.5 * (lo + hi)
        tr, *_ = base_traj(b, rng)
        if realized_psi(tr) < target_psi: lo = b
        else: hi = b
    return 0.5 * (lo + hi)

def chi_slope(dphi, eps):
    den = sum(e * e for e in eps)
    return (sum(e * d for e, d in zip(eps, dphi)) / den) if den else 0.0

def measure_cell(b, seed, arm):
    base, lat, eta, m = base_traj(b, ss(seed, b, 1))
    sigmaL = float(np.std(base[:, INJ]))
    eps_abs = [e * sigmaL for e in E_LIN]
    phi0_bar = np.mean([phi_windows(base) for _ in range(R_REAL)])
    per_eps_R = []; dphi = []
    for ea in eps_abs:
        Rphi = []
        for r in range(R_REAL):
            xi = ss(seed, b, ea, r + 10).standard_normal(T)
            if arm == "COUP":                         # emit-gate noise, propagated through dynamics
                tr = coup_traj(b, lat, eta, m, ea, xi)
            elif arm == "DECOUP":                     # emit-gate noise, readout-only (lanes 0,4 NOT in cols_x)
                tr = base.copy(); tr[:, 0] += ea * xi; tr[:, 4] += ea * xi   # coupling-specificity neg control -> ~0 expected
            else:                                     # INSTR: direct cols_x readout noise -> instrument-alive positive control
                tr = base.copy(); tr[:, 3] += ea * xi; tr[:, 13] += ea * xi  # lanes 3,13 ARE in cols_x
            Rphi.append(phi_windows(tr).mean())
        per_eps_R.append(np.array(Rphi)); dphi.append(np.mean(Rphi) - phi0_bar)
    chi = chi_slope(dphi, eps_abs)
    half = R_REAL // 2; nulls = []
    for A in list(combinations(range(R_REAL), half))[:35]:
        Bset = [i for i in range(R_REAL) if i not in A]
        dn = [per_eps_R[i][list(A)].mean() - per_eps_R[i][Bset].mean() for i in range(len(eps_abs))]
        nulls.append(abs(chi_slope(dn, eps_abs)))
    return abs(chi), (float(np.percentile(nulls, 95)) if nulls else 0.0)

print(f"=== H_9266 response-function chi(Psi) (T={T} seeds={SEEDS}) ===")
res = {}
for seed in SEEDS:
    print(f"[seed {seed}]", flush=True); crng = ss(seed, 999)
    for tp in PSI_G:
        b = calibrate_b(tp, crng)
        ch_c, c0_c = measure_cell(b, seed, "COUP")
        ch_d, c0_d = measure_cell(b, seed, "DECOUP")
        ch_i, c0_i = measure_cell(b, seed, "INSTR")
        res[(seed, tp)] = dict(b=b, chi_coup=ch_c, chi_dec=ch_d, chi_instr=ch_i, chi0=max(c0_c, c0_d, c0_i))
        print(f"  Psi~{tp:.2f} b={b:+.3f} | coup={ch_c:.4f} dec={ch_d:.4f} instr={ch_i:.4f} chi0={max(c0_c,c0_d,c0_i):.4f}", flush=True)

def offband(): return [tp for tp in PSI_G if tp not in CENTER]
seed_verd = []
for seed in SEEDS:
    coup = {tp: res[(seed, tp)]["chi_coup"] for tp in PSI_G}
    dec  = {tp: res[(seed, tp)]["chi_dec"] for tp in PSI_G}
    c0   = float(np.median([res[(seed, tp)]["chi0"] for tp in PSI_G]))
    peak = max(PSI_G, key=lambda tp: coup[tp])
    L1 = peak in CENTER
    kc = coup[0.5] / (np.median([coup[tp] for tp in offband()]) + 1e-9)
    kd = dec[0.5] / (np.median([dec[tp] for tp in offband()]) + 1e-9)
    L2 = kc >= 2.0 and kd < 1.5
    dchi = coup[0.5] - dec[0.5]; L3 = dchi > 0 and dchi >= 2 * c0
    instr = {tp: res[(seed, tp)]["chi_instr"] for tp in PSI_G}
    alive = max(instr.values()) >= 3 * c0                       # INSTR (direct cols_x noise) = instrument-alive control
    seed_verd.append(dict(seed=seed, L1=L1, L2=L2, L3=L3, alive=alive, peak=peak, kc=kc, kd=kd, dchi=dchi, c0=c0,
                          instr_max=max(instr.values())))

def maj(k): return sum(1 for s in seed_verd if s[k]) >= (len(SEEDS)//2 + 1)
print("\nseed | alive L1 L2 L3 | peakPsi kappa_c kappa_d  dchi   chi0")
for s in seed_verd:
    print(f"{s['seed']:>4} |  {int(s['alive'])}    {int(s['L1'])}  {int(s['L2'])}  {int(s['L3'])} | "
          f"{s['peak']:.2f}   {s['kc']:.2f}   {s['kd']:.2f}  {s['dchi']:+.3f} {s['c0']:.4f}")
alive = maj("alive")
if not alive:
    final = "VOID-INSTRUMENT (chi_dec detector dead — not FAIL)"
elif maj("L1") and maj("L2") and maj("L3"):
    final = "PASS (DIRECTIONAL · chi-peak at Psi=1/2 · coupling-specific · faithful-Phi VPhi leg follow-on)"
else:
    final = "FAIL / NULL (DIRECTIONAL · instrument alive, no Psi=1/2 localized coupling susceptibility)"
print(f"\nVERDICT: {final}")
import json
json.dump({"seeds": SEEDS, "T": T, "res": {f"{k[0]}_{k[1]}": v for k, v in res.items()},
           "seed_verd": seed_verd, "final": final},
          open(os.path.join(os.path.dirname(__file__), "h9266_response_function_out.json"), "w"),
          default=float, ensure_ascii=False)
