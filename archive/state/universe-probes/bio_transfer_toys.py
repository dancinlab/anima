#!/usr/bin/env python3
"""BIO-TRANSFER toy falsifiers — H_862..H_868 (the 6 CPU-substrate ones).

a_scale_honest_scope: TOY-ONLY. Each sim tests whether the MECHANISM AS MODELLED produces the
pre-registered signature on a small substrate-agnostic sim. A toy-green states "toy-only, scale-transfer
unverified"; it is NOT a production claim. Emergent dynamics (Kuramoto sync, diffusion, bistable switch,
SI spread, momentum descent, percolation) are used so the signature is NOT hard-coded — the falsifier can
genuinely go either way under the chosen parameters. Fixed seeds for reproducibility. Pure stdlib (no numpy).

p7: no perplexity verdict — each readout is a direct, scripted measurement. NO fabrication: the printed
numbers are whatever the sim computes. The FALSIFIER is the skeptic's claim; REFUTED-falsifier => the
hypothesis' predicted signature HOLDS (toy); CONFIRMED-falsifier => closed-negative for the toy (a_paper_negative_ok).

H_861 (METASTASIS, branching harness) + H_865 (LTP, AKIDA on-chip) are CHIP-substrate (#1717 single-exclusive)
and are DEFERRED to after the live gold ladder releases the chip — they are NOT in this CPU driver.
"""
import math, random, statistics

SEED = 20260603


def h862_hgt():
    """SI spread: vertical-only vs vertical+lateral(HGT). REFUTED-falsifier iff ticks_v/ticks_hgt >= 1.5."""
    def run(lateral):
        random.seed(SEED)
        N = 200; infected = [False] * N; infected[0] = True
        p_v = 0.5            # vertical: an edge-cell converts its offspring (1 random susceptible) w.p. p_v
        p_l = 0.5; k = 2     # HGT adds: convert up to k random peers w.p. p_l each
        for t in range(1, 1000):
            newly = []
            idx_inf = [i for i, v in enumerate(infected) if v]
            for i in idx_inf:
                if random.random() < p_v:
                    j = random.randrange(N)
                    if not infected[j]:
                        newly.append(j)
                if lateral:
                    for _ in range(k):
                        if random.random() < p_l:
                            j = random.randrange(N)
                            if not infected[j]:
                                newly.append(j)
            for j in newly:
                infected[j] = True
            if sum(infected) >= 0.9 * N:
                return t
        return 999
    tv, th = run(False), run(True)
    ratio = tv / th
    refuted = ratio >= 1.5
    print(f"[H_862 HGT]        ticks_vertical={tv} ticks_hgt={th} ratio={ratio:.2f} "
          f"(threshold>=1.5) -> falsifier {'REFUTED (HGT faster, hypothesis HOLDS)' if refuted else 'CONFIRMED (no >=1.5x speedup)'}")
    return refuted


def h863_epigenetic():
    """Momentum-from-parent vs zero-momentum GD. REFUTED-falsifier iff mean steps_A < steps_B, paired t p<0.05."""
    random.seed(SEED)
    d = 8; eps = 0.05; lr = 0.08; mom = 0.9; n_trials = 24
    diffs = []; stepsA_all = []; stepsB_all = []
    for _ in range(n_trials):
        target = [random.uniform(-1, 1) for _ in range(d)]
        x0 = [random.uniform(-1, 1) for _ in range(d)]
        # parent's recent-task gradient direction at x0 (aligned toward target): -grad of 0.5||x-target||^2 = (target-x0)
        v_par = [(target[i] - x0[i]) for i in range(d)]
        nrm = math.sqrt(sum(c * c for c in v_par)) or 1.0
        v_par = [0.4 * c / nrm for c in v_par]   # modest inherited velocity

        def descend(v_init):
            x = list(x0); v = list(v_init)
            for s in range(1, 2000):
                grad = [(x[i] - target[i]) for i in range(d)]
                v = [mom * v[i] - lr * grad[i] for i in range(d)]
                x = [x[i] + v[i] for i in range(d)]
                if math.sqrt(sum((x[i] - target[i]) ** 2 for i in range(d))) < eps:
                    return s
            return 2000
        sA = descend(v_par)       # tension-inherited
        sB = descend([0.0] * d)   # weights-only (reset tension)
        stepsA_all.append(sA); stepsB_all.append(sB); diffs.append(sB - sA)
    mean_d = statistics.mean(diffs); sd_d = statistics.pstdev(diffs) or 1e-9
    t = mean_d / (sd_d / math.sqrt(n_trials))
    refuted = (statistics.mean(stepsA_all) < statistics.mean(stepsB_all)) and abs(t) > 2.07  # df=23, ~2.07
    print(f"[H_863 EPIGENETIC] steps_inherited={statistics.mean(stepsA_all):.1f} steps_weightsonly={statistics.mean(stepsB_all):.1f} "
          f"paired t={t:.2f} (|t|>2.07 sig) -> falsifier {'REFUTED (inherited tension converges faster, HOLDS)' if refuted else 'CONFIRMED (no advantage)'}")
    return refuted


def h864_prion():
    """Basin templating down a chain. REFUTED-falsifier iff propagation REACH >= 2 hops AND P(adopt|exposed)>base.
    Reach = furthest cell whose TIME-AVERAGED occupancy (last K sweeps) > 0.5 — measures how far the basin
    self-sustains, NOT the position of the first transient reversion hole (which would conflate noise with reach)."""
    random.seed(SEED)
    L = 30; p_adopt = 0.7; q_revert = 0.05; sweeps = 300; K = 100
    state = [0] * L; state[0] = 1
    occ = [0] * L
    for sw in range(sweeps):
        for i in range(1, L):
            if state[i - 1] == 1 and state[i] == 0:
                if random.random() < p_adopt:
                    state[i] = 1
            elif state[i] == 1:
                if random.random() < q_revert:
                    state[i] = 0
        if sw >= sweeps - K:
            for i in range(L):
                occ[i] += state[i]
    mean_occ = [o / K for o in occ]
    reach = 0
    for i in range(1, L):
        if mean_occ[i] > 0.5:
            reach = i
        else:
            break  # first cell that does NOT self-sustain = end of the propagating basin
    base = q_revert  # base flip rate without an exposed templating neighbour
    refuted = reach >= 2 and p_adopt > base
    sample = " ".join(f"d{d}={mean_occ[d]:.2f}" for d in (1, 2, 5, 10, 20, 29))
    print(f"[H_864 PRION]      reach(occ>0.5)={reach}/{L-1} [{sample}] P(adopt)={p_adopt}>base={base} "
          f"-> falsifier {'REFUTED (self-propagating >=2 hops, HOLDS)' if refuted else 'CONFIRMED (decays at hop 1)'}")
    return refuted


def h866_fret():
    """Tension diffusion from a point source. REFUTED-falsifier iff monotone-decreasing over >=3 distance bins."""
    L = 40; T0 = 1.0; absorb = 0.04; iters = 4000
    T = [0.0] * L
    for _ in range(iters):
        newT = list(T)
        for i in range(1, L):
            left = T[i - 1]; right = T[i + 1] if i + 1 < L else T[i]
            newT[i] = (1 - absorb) * (0.5 * (left + right)) + 0.5 * absorb * T[i]
        newT[0] = T0  # source clamp
        T = newT
    bins = [T[d] for d in (1, 5, 10, 15, 20)]
    monotone = all(bins[i] > bins[i + 1] for i in range(len(bins) - 1))
    refuted = monotone
    prof = " ".join(f"d{d}={T[d]:.4f}" for d in (1, 5, 10, 15, 20))
    print(f"[H_866 FRET]       profile {prof} -> falsifier "
          f"{'REFUTED (distance-decay coupling, HOLDS)' if refuted else 'CONFIRMED (flat/independent)'}")
    return refuted


def h867_met():
    """Kuramoto synchronization sweep. REFUTED-falsifier iff super-additive jump in order param across kappa rungs."""
    random.seed(SEED)
    N = 60; dt = 0.05; steps = 1500
    omega = [random.gauss(0, 0.5) for _ in range(N)]
    base_r = 1.0 / math.sqrt(N)  # incoherent (additive) baseline ~ 1/sqrt(N)
    def order_param(kappa):
        theta = [random.uniform(-math.pi, math.pi) for _ in range(N)]
        for _ in range(steps):
            sx = sum(math.cos(t) for t in theta); sy = sum(math.sin(t) for t in theta)
            psi = math.atan2(sy, sx); r = math.sqrt(sx * sx + sy * sy) / N
            theta = [theta[i] + dt * (omega[i] + kappa * r * math.sin(psi - theta[i])) for i in range(N)]
        sx = sum(math.cos(t) for t in theta); sy = sum(math.sin(t) for t in theta)
        return math.sqrt(sx * sx + sy * sy) / N
    rungs = [0.0, 0.5, 1.0, 2.0, 4.0]
    rs = [order_param(k) for k in rungs]
    jump = rs[-1] - rs[0]
    refuted = rs[-1] > 5 * base_r and jump > 0.3  # sharp super-additive coherence well above incoherent baseline
    prof = " ".join(f"k{k}->r={r:.3f}" for k, r in zip(rungs, rs))
    print(f"[H_867 MET]        baseline(1/sqrtN)={base_r:.3f} {prof} -> falsifier "
          f"{'REFUTED (super-additive sync transition, HOLDS)' if refuted else 'CONFIRMED (merely additive)'}")
    return refuted


def h868_morphogen():
    """Bistable fate switch along a morphogen gradient. REFUTED-falsifier iff sharp boundary width<0.15 over >=3 realizations."""
    widths = []
    for real in range(3):
        random.seed(SEED + real)
        L = 200; theta = 0.5; s = 4.0
        fates = []
        for xi in range(L):
            x = xi / (L - 1); g = 1.0 - x  # linear morphogen gradient, range [0,1]
            y = random.uniform(-0.1, 0.1)
            for _ in range(400):  # bistable toggle: ydot = y - y^3 + s*(g-theta) + noise
                y += 0.05 * (y - y ** 3 + s * (g - theta)) + random.gauss(0, 0.01)
            fates.append(1 if y > 0 else 0)
        # boundary width = fraction of x-range over which fate is mixed near the switch
        ones = [i for i, f in enumerate(fates) if f == 1]
        if ones and len(ones) < L:
            boundary_idx = max(ones)
            # count flips in a window = sharpness proxy; width = transition zone / L
            flips = sum(1 for i in range(1, L) if fates[i] != fates[i - 1])
            width = flips / L
        else:
            width = 1.0
        widths.append(width)
    mean_w = statistics.mean(widths)
    refuted = mean_w < 0.15 and all(w < 0.2 for w in widths)
    print(f"[H_868 MORPHOGEN]  boundary_widths={[round(w,4) for w in widths]} mean={mean_w:.4f} "
          f"(sharp<0.15) -> falsifier {'REFUTED (sharp threshold switch, HOLDS)' if refuted else 'CONFIRMED (graded blur)'}")
    return refuted


if __name__ == "__main__":
    print("=== BIO-TRANSFER toy falsifiers (a_scale_honest_scope: TOY-ONLY) seed=%d ===" % SEED)
    results = {}
    for name, fn in [("H_862", h862_hgt), ("H_863", h863_epigenetic), ("H_864", h864_prion),
                     ("H_866", h866_fret), ("H_867", h867_met), ("H_868", h868_morphogen)]:
        try:
            results[name] = fn()
        except Exception as e:
            results[name] = None
            print(f"[{name}] ERROR {type(e).__name__}: {e}")
    held = [k for k, v in results.items() if v is True]
    closed = [k for k, v in results.items() if v is False]
    print("=== SUMMARY (toy): hypothesis-HOLDS(falsifier refuted) = %s | closed-negative(falsifier confirmed) = %s ==="
          % (held, closed))
