"""
H_9266 $0 toy probe — determinism vs contingency: is stochasticity Psi-localized (load-bearing only at Psi~1/2)?

DIRECTIONAL (toy ByteGPT-free minimal A<->G substrate). NOT terminal (303M anima-py = terminal).

Pre-registered bar (card H_9266 section 4, frozen BEFORE run):
  PASS  = Dsigma peaks at Psi=1/2 (b=0) AND decays with |Psi-1/2| AND sigma(COUP)!=sigma(DECOUP) AND ARM-SHOCK detected.
  FAIL  = Dsigma flat across Psi (FORM knob) OR sigma(COUP)~=sigma(DECOUP) (coupling-irrelevant).

Model (anima-native A<->G): A pushes emit(+), G pushes silence(-). bias b = 2*Psi - 1 (b=0 <=> A=G balanced <=> Psi=1/2).
  recurrent substrate state:  x_{t+1} = tanh( g*x_t + b + inject_t )   ; g=1.05 slightly bistable (edge, two basins).
  DET   : inject=0 ; emit = 1[x_t > 0]                          (noise-free)
  COUP  : inject = alpha*noise_t  INTO recurrent x               (kick at the collapse -> Kramers hop -> telegraph memory)
  DECOUP: x evolves noise-free ; emit = 1[x_t + alpha*noise'_t > 0]  (SAME noise marginal, on readout only -> iid flips, no organized structure)
sigma = excess entropy E of the emit stream (predictive information; computational mechanics).
        telegraph/metastable switching -> E>0 ; constant OR iid-white -> E~=0. rewards ORGANIZED structure, not degeneracy.

FIXED params (committed here, no tuning): g=1.05, alpha=0.9, T=4000, Lmax=10, seeds=5.
"""
import numpy as np

G_GAIN = 1.05
ALPHA  = 0.9
T      = 4000
LMAX   = 10
SEEDS  = [7, 4302, 4303, 11, 29]
B_GRID = [0.0, 0.1, 0.25, 0.5, 1.0, 2.0]   # |b| = |2Psi-1| ; b=0 is Psi=1/2 (critical/balanced)

def _mi_binary(a, b):
    """MI(a;b) for two aligned binary arrays via 2x2 contingency (well-sampled at T=4000)."""
    n = len(a)
    if n == 0: return 0.0
    mi = 0.0
    for va in (0, 1):
        pa = np.mean(a == va)
        if pa == 0: continue
        for vb in (0, 1):
            pb = np.mean(b == vb)
            pab = np.mean((a == va) & (b == vb))
            if pab == 0 or pb == 0: continue
            mi += pab * np.log2(pab / (pa * pb))
    return max(mi, 0.0)

def excess_entropy(bits, Lmax=LMAX):
    """sigma = delayed mutual information summed over lags 1..Lmax (predictive-info proxy).
    telegraph/metastable switching -> correlated -> high ; iid-white OR constant -> ~0.
    Robust to undersampling (each lag is a 2x2 table), unlike block-entropy at L=10."""
    bits = np.asarray(bits, dtype=np.int64)
    return float(sum(_mi_binary(bits[:-lag], bits[lag:]) for lag in range(1, Lmax + 1)))

def run_arm(arm, b, rng, arm_shock=False):
    x = 0.0
    emit = np.empty(T, dtype=np.int64)
    noise  = rng.standard_normal(T)
    noise2 = rng.permutation(noise.copy())   # same marginal, decorrelated from the collapse (DECOUP)
    for t in range(T):
        bt = b
        if arm_shock:                        # phasic urgency (positive control): ALTERNATING pulse -> organized switching
            bt = b + (2.5 if (t // 20) % 2 == 0 else -2.5)
        if arm == "DET":
            x = np.tanh(G_GAIN * x + bt)
            emit[t] = 1 if x > 0 else 0
        elif arm == "COUP":
            x = np.tanh(G_GAIN * x + bt + ALPHA * noise[t])
            emit[t] = 1 if x > 0 else 0
        elif arm == "DECOUP":
            x = np.tanh(G_GAIN * x + bt)                 # recurrence noise-free
            emit[t] = 1 if (x + ALPHA * noise2[t]) > 0 else 0
    return emit

def sigma(arm, b, seed, arm_shock=False):
    rng = np.random.default_rng(seed * 131 + int(b * 1000) + (999 if arm_shock else 0))
    return excess_entropy(run_arm(arm, b, rng, arm_shock))

print("=== H_9266 toy probe (DIRECTIONAL) ===")
print(f"g={G_GAIN} alpha={ALPHA} T={T} Lmax={LMAX} seeds={SEEDS}")
print(f"{'|b|':>5} {'Psi':>6} | {'DET':>12} {'COUP':>12} {'DECOUP':>12} | {'Dsig=COUP-DECOUP':>18}")
profile = []
for b in B_GRID:
    psi = 0.5 + b / 2.0
    det = np.mean([sigma("DET", b, s) for s in SEEDS])
    cou = np.mean([sigma("COUP", b, s) for s in SEEDS])
    dec = np.mean([sigma("DECOUP", b, s) for s in SEEDS])
    dsig = cou - dec
    profile.append((b, det, cou, dec, dsig))
    print(f"{b:>5.2f} {psi:>6.3f} | {det:>12.4f} {cou:>12.4f} {dec:>12.4f} | {dsig:>18.4f}")

# --- verdict logic against pre-registered bar ---
dsig_at_half = profile[0][4]                 # b=0 (Psi=1/2)
dsig_far     = np.mean([p[4] for p in profile if p[0] >= 1.0])  # |b|>=1
peak_at_half = all(dsig_at_half >= p[4] for p in profile)       # max at b=0
decays       = dsig_at_half > dsig_far + 1e-3
coupling_specific = dsig_at_half > 0.05                          # COUP != DECOUP at criticality

# ARM-SHOCK positive control at b=0: detector must register a change vs plain DET
det_plain = np.mean([sigma("DET", 0.0, s) for s in SEEDS])
det_shock = np.mean([sigma("DET", 0.0, s, arm_shock=True) for s in SEEDS])
arm_shock_detected = abs(det_shock - det_plain) > 0.05

print("\n=== verdict vs frozen bar ===")
print(f"Dsigma@Psi=1/2 = {dsig_at_half:.4f}  | Dsigma_far(|b|>=1) = {dsig_far:.4f}")
print(f"peak_at_half      = {peak_at_half}")
print(f"decays_off_half   = {decays}")
print(f"coupling_specific = {coupling_specific} (Dsig@half>0.05)")
print(f"ARM-SHOCK detected= {arm_shock_detected} (DET plain {det_plain:.4f} vs shock {det_shock:.4f})")
PASS = peak_at_half and decays and coupling_specific and arm_shock_detected
print(f"\nVERDICT: {'PASS (DIRECTIONAL)' if PASS else 'FAIL / NULL (DIRECTIONAL)'}")
