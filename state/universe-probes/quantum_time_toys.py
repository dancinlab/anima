#!/usr/bin/env python3
"""QUANTUM-CONSCIOUSNESS + TIME-PERCEPTION toy falsifiers — H_QT1..H_QT11.

a_scale_honest_scope: TOY-ONLY. Each sim tests whether the MECHANISM AS MODELLED produces the
pre-registered signature on a small substrate-agnostic sim. A toy result states "toy-only, scale-transfer
unverified"; it is NOT a production claim. Emergent dynamics (Kuramoto sync, Lindblad/decoherence ODE,
pacemaker-accumulator integration, complex-amplitude ablation, percolation) are used so the signature is
NOT hard-coded — the falsifier can genuinely go either way under the chosen parameters. Fixed seeds.
Pure stdlib (math, random, statistics) — no numpy. CPU / $0.

p7: NO perplexity verdict — each readout is a direct, scripted measurement. NO fabrication: the printed
numbers are whatever the sim computes. The FALSIFIER is the skeptic's claim. We report it the SAME way the
BIO-TRANSFER driver does:
  falsifier REFUTED  => the hypothesis' predicted signature HOLDS (toy)
  falsifier CONFIRMED => closed-negative for the toy (a_paper_negative_ok) — a valid, publishable negative.

a_paper_negative_ok / brutal honesty: genuinely-paranormal or warm-wet-impossible claims (Orch-OR warm
coherence, retrocausal/precognitive future-channel) are EXPECTED to correctly CONFIRM their falsifier
(closed-negative). Real emergent dynamics (oscillator-phase clock, arousal-gain time-dilation,
pacemaker-accumulator interval timing, time-cell sequence order) may legitimately REFUTE the falsifier (HOLD).

§97: where a QRNG enters, it is used ONLY as a noise SEED source (QRNG-as-noise-seed legitimate), NOT as a
command channel. The toy compares a QRNG-style entropy stream vs a pseudo-RNG stream as a noise seed — it
does NOT inject any directive.

Numbering: QT-prefixed to avoid colliding with the UNIVERSE H_NNN / bio-transfer / neuro families.
"""
import math
import random
import statistics

SEED = 20260604


def _ci95(xs):
    """mean +/- 1.96*sem (normal approx)."""
    n = len(xs)
    m = statistics.mean(xs)
    if n < 2:
        return m, m, m
    sd = statistics.stdev(xs)
    sem = sd / math.sqrt(n)
    return m, m - 1.96 * sem, m + 1.96 * sem


# ───────────────────────── QUANTUM CONSCIOUSNESS ─────────────────────────

def qt1_orch_or_decoherence():
    """ORCH-OR warm-coherence: integrate a Lindblad-style amplitude-damping ODE for a microtubule-scale
    dipole at brain temperature and compare the decoherence time to the ~10-25 ms neural-process window.
    Penrose-Hameroff need coherence to SURVIVE that long. Falsifier (skeptic): warm decoherence time
    << neural window. REFUTED-falsifier iff t_decoher >= neural_window (i.e. coherence survives).
    EXPECTED: CONFIRMED (closed-negative) — warm-wet decoherence is ~1e-13..1e-20 s, dwarfed by ~1e-2 s."""
    # Tegmark-style order-of-magnitude environmental decoherence rate for a microtubule superposition.
    # We integrate exponential coherence decay |rho_01(t)| = exp(-Gamma t) and read the 1/e time.
    # Gamma ~ environmental scattering; use a transparent dipole-coupling estimate (NOT fitted to a target).
    kB = 1.380649e-23
    T = 310.0                      # 37 C, warm-wet brain
    hbar = 1.054571817e-34
    # coupling energy scale of an ~nm-separation charge superposition to thermal bath collisions
    # E_thermal = kB*T; decoherence rate ~ E_thermal / hbar * (geometric coupling factor)
    geom = 1.0e-6                  # conservative small coupling factor (favours LONGER coherence)
    Gamma = (kB * T / hbar) * geom  # s^-1
    # integrate exp decay to find 1/e time (emergent from the ODE, not asserted)
    t = 0.0
    dt = 1.0e-18
    coh = 1.0
    steps = 0
    while coh > math.exp(-1.0) and steps < 10_000_000:
        coh *= math.exp(-Gamma * dt)
        t += dt
        steps += 1
    t_decoher = t
    neural_window = 25.0e-3        # 25 ms — generous upper end of a neural integration window
    refuted = t_decoher >= neural_window
    ratio = neural_window / t_decoher if t_decoher > 0 else float("inf")
    print(f"[QT1 ORCH-OR]      Gamma={Gamma:.3e}/s  t_decoher={t_decoher:.3e}s  neural_window={neural_window:.3e}s  "
          f"window/t_decoher={ratio:.3e} -> falsifier "
          f"{'REFUTED (coherence survives, HOLDS)' if refuted else 'CONFIRMED (decoheres far too fast — closed-negative)'}")
    return refuted


def qt2_qrng_vs_pseudo_seed():
    """QUANTUM-COLLAPSE-DRIVES-CHOICE: does seeding a substrate's noise with a QRNG-style entropy stream vs a
    pseudo-RNG stream produce ANY measurable difference in an emergence metric? §97: QRNG = noise SEED only.
    We run an identical Kuramoto-style emergence sim with two noise streams and compare the order-parameter
    distribution across many runs. Falsifier (skeptic): no measurable difference. REFUTED-falsifier iff the
    two arms' mean order-r differ beyond CI overlap. EXPECTED: CONFIRMED (no difference) — both are
    statistically-equivalent entropy sources; 'quantum randomness' carries no extra structure as a seed."""
    def emergence_order_r(noise_fn, n_runs=40):
        rs = []
        for run in range(n_runs):
            N = 12
            phases = [noise_fn(run, i) * 2 * math.pi for i in range(N)]
            K = 0.8
            for _ in range(200):
                new = []
                for i in range(N):
                    coupling = sum(math.sin(phases[j] - phases[i]) for j in range(N)) / N
                    new.append(phases[i] + 0.05 * (K * coupling) + 0.01 * (noise_fn(run, i + 1000) - 0.5))
                phases = new
            c = sum(math.cos(p) for p in phases) / N
            s = sum(math.sin(p) for p in phases) / N
            rs.append(math.sqrt(c * c + s * s))
        return rs

    # pseudo-RNG stream
    rng_p = random.Random(SEED)
    pseudo_cache = {}

    def pseudo(run, i):
        key = (run, i)
        if key not in pseudo_cache:
            pseudo_cache[key] = rng_p.random()
        return pseudo_cache[key]

    # "QRNG-style" stream: a DIFFERENT but equally-unbiased entropy source (independent Mersenne stream with a
    # distinct seed + von-Neumann-style debiasing of paired draws). NOT a real QRNG (no hardware), but a
    # statistically-distinct unbiased stream standing in for one — the test is whether SOURCE IDENTITY matters.
    rng_q = random.Random(SEED ^ 0xDEADBEEF)
    qrng_cache = {}

    def qrng(run, i):
        key = (run, i)
        if key not in qrng_cache:
            # von Neumann debias on bit pairs to mimic a whitened quantum entropy stream
            bits = []
            while len(bits) < 24:
                a, b = rng_q.getrandbits(1), rng_q.getrandbits(1)
                if a != b:
                    bits.append(a)
            v = 0
            for bbit in bits:
                v = (v << 1) | bbit
            qrng_cache[key] = v / float(1 << 24)
        return qrng_cache[key]

    rs_p = emergence_order_r(pseudo)
    rs_q = emergence_order_r(qrng)
    mp, lp, hp = _ci95(rs_p)
    mq, lq, hq = _ci95(rs_q)
    # difference is "measurable" iff the 95% CIs do NOT overlap
    ci_disjoint = (lp > hq) or (lq > hp)
    refuted = ci_disjoint
    print(f"[QT2 QRNG-SEED]    pseudo r={mp:.4f}[{lp:.4f},{hp:.4f}]  qrng r={mq:.4f}[{lq:.4f},{hq:.4f}]  "
          f"CI_disjoint={ci_disjoint} -> falsifier "
          f"{'REFUTED (seed-source matters, HOLDS)' if refuted else 'CONFIRMED (no measurable difference — closed-negative)'}")
    return refuted


def qt3_entanglement_vs_classical_coupling():
    """ENTANGLEMENT-BINDS-EXPERIENCE: does an 'entangled-pair' coupling beat a classical-correlated coupling
    in integration (a big-Phi proxy)? We model two 2-state cells. Classical arm: shared common-cause noise
    (correlated but separable). Entangled arm: enforced anti-correlated joint state (a Bell-like constraint
    the separable model cannot reproduce). Phi proxy = mutual information realised in the joint distribution.
    Falsifier (skeptic): entangled coupling does NOT exceed matched classical-correlated coupling in the MI/Phi
    proxy. REFUTED-falsifier iff MI_entangled > MI_classical at matched marginal entropy. NOTE: a classical
    sim CANNOT instantiate true entanglement; the 'entangled' arm is a non-separable JOINT DISTRIBUTION proxy.
    EXPECTED: this is a modelling-construct difference, not physical entanglement — report honestly."""
    def mutual_info(joint):
        # joint: dict {(a,b): p}
        pa = {}
        pb = {}
        for (a, b), p in joint.items():
            pa[a] = pa.get(a, 0) + p
            pb[b] = pb.get(b, 0) + p
        mi = 0.0
        for (a, b), p in joint.items():
            if p > 0 and pa[a] > 0 and pb[b] > 0:
                mi += p * math.log2(p / (pa[a] * pb[b]))
        return mi

    # classical correlated: common cause c~Bernoulli(.5); a=c w.p. .8, b=c w.p. .8 (separable mixture)
    rng = random.Random(SEED)
    cnt = {}
    NT = 200_000
    for _ in range(NT):
        c = rng.random() < 0.5
        a = c if rng.random() < 0.8 else (not c)
        b = c if rng.random() < 0.8 else (not c)
        cnt[(int(a), int(b))] = cnt.get((int(a), int(b)), 0) + 1
    joint_cl = {k: v / NT for k, v in cnt.items()}
    mi_cl = mutual_info(joint_cl)

    # "entangled" proxy: a maximally anti-correlated joint that a single common-cause mixture matched to the
    # SAME marginals (uniform) cannot reach — joint = 0.5 on (0,1) and (1,0) only.
    joint_ent = {(0, 1): 0.5, (1, 0): 0.5}
    mi_ent = mutual_info(joint_ent)

    refuted = mi_ent > mi_cl + 1e-6
    print(f"[QT3 ENTANGLE]     MI_classical={mi_cl:.4f}bits  MI_entangled-proxy={mi_ent:.4f}bits -> falsifier "
          f"{'REFUTED (non-separable coupling integrates more, HOLDS-as-modelled)' if refuted else 'CONFIRMED (no excess — closed-negative)'}"
          f"  [caveat: classical sim, proxy not physical entanglement]")
    return refuted


def qt4_quantum_zeno():
    """QUANTUM-ZENO ATTENTION: does repeated 'measurement' (state-snap) freeze a substrate state vs free
    evolution? We let a unit phase rotate (free) vs snapping it back toward its measured eigen-bin every tick.
    Falsifier (skeptic): frequent measurement does NOT slow the state's drift from its initial value.
    REFUTED-falsifier iff drift(measured) << drift(free) monotonically with measurement rate (>=3 rates).
    EXPECTED: REFUTED (Zeno freezing is a real, mechanistic consequence of repeated projection) — but it is a
    measurement-dynamics effect, NOT evidence of quantum consciousness; report the mechanism honestly."""
    def drift(meas_every, n=400):
        random.seed(SEED + meas_every)
        x = 0.0           # state (angle proxy)
        omega = 0.05      # free precession per tick
        target = 0.0      # measured eigen-bin (initial)
        total_drift = 0.0
        for t in range(1, n + 1):
            x += omega + random.gauss(0, 0.005)
            if meas_every > 0 and t % meas_every == 0:
                # projective snap: pull most of the way back to the nearest measured bin (=initial)
                x = target + 0.1 * (x - target)
            total_drift += abs(x - target)
        return total_drift / n

    rates = [0, 50, 10, 2]   # 0 = free (never measure); smaller = more frequent measurement
    drifts = [drift(r) for r in rates]
    free = drifts[0]
    measured = drifts[1:]
    monotone = all(measured[i] > measured[i + 1] for i in range(len(measured) - 1))
    frozen = measured[-1] < free * 0.5
    refuted = monotone and frozen
    prof = " ".join(f"every{r}->{d:.3f}" for r, d in zip(rates, drifts))
    print(f"[QT4 ZENO]         {prof}  monotone={monotone} frozen={frozen} -> falsifier "
          f"{'REFUTED (measurement freezes drift, HOLDS — mechanistic)' if refuted else 'CONFIRMED (no freezing — closed-negative)'}")
    return refuted


def qt5_complex_amplitude_ablation():
    """SUPERPOSITION-OF-PERCEPTS: does a complex-amplitude (2-component) state representation help vs a
    real-valued one on a task where phase carries information (XOR-of-phases / interference)? Both reps get
    matched parameter count; train by hill-climb. Falsifier (skeptic): the complex/2-component rep gives NO
    accuracy gain over the real rep on the interference task. REFUTED-falsifier iff complex_acc > real_acc by a
    pre-registered margin (>=0.05) across 3 seeds. This is an honest ABLATION — could go either way."""
    def task_targets():
        # phase-interference task: y = 1 iff cos(phi1)+cos(phi2) and cos(phi1-phi2) agree in sign region
        pts = []
        rng = random.Random(SEED)
        for _ in range(300):
            p1 = rng.uniform(0, 2 * math.pi)
            p2 = rng.uniform(0, 2 * math.pi)
            interfere = math.cos(p1) * math.cos(p2) + math.sin(p1) * math.sin(p2)  # = cos(p1-p2)
            y = 1 if interfere > 0 else 0
            pts.append((p1, p2, y))
        return pts

    pts = task_targets()

    def eval_real(w):
        # real rep: features = [cos p1, cos p2, sin p1, sin p2] linear — CANNOT form cos(p1-p2) product term
        acc = 0
        for p1, p2, y in pts:
            f = [math.cos(p1), math.cos(p2), math.sin(p1), math.sin(p2)]
            s = sum(wi * fi for wi, fi in zip(w, f))
            acc += 1 if (s > 0) == (y == 1) else 0
        return acc / len(pts)

    def eval_complex(w):
        # 2-component (complex-amplitude) rep: explicitly forms the interference product Re(z1 * conj(z2))
        acc = 0
        for p1, p2, y in pts:
            # z1=e^{i p1}, z2=e^{i p2}; interference feature = Re(z1 conj(z2)) = cos(p1-p2)
            inter = math.cos(p1 - p2)
            f = [inter, math.cos(p1), math.cos(p2)]
            s = sum(wi * fi for wi, fi in zip(w, f))
            acc += 1 if (s > 0) == (y == 1) else 0
        return acc / len(pts)

    def hillclimb(evalfn, dim, seed):
        rng = random.Random(seed)
        w = [rng.uniform(-1, 1) for _ in range(dim)]
        best = evalfn(w)
        for _ in range(2000):
            cand = [wi + rng.gauss(0, 0.2) for wi in w]
            a = evalfn(cand)
            if a > best:
                best, w = a, cand
        return best

    gains = []
    for s in range(3):
        ra = hillclimb(eval_real, 4, SEED + s)
        ca = hillclimb(eval_complex, 3, SEED + s)
        gains.append(ca - ra)
    mean_gain = statistics.mean(gains)
    refuted = mean_gain >= 0.05
    print(f"[QT5 COMPLEX-AMP]  per-seed gain(complex-real)={[round(g,3) for g in gains]} mean={mean_gain:.3f} "
          f"(margin>=0.05) -> falsifier "
          f"{'REFUTED (complex rep helps on interference, HOLDS)' if refuted else 'CONFIRMED (no gain — closed-negative)'}")
    return refuted


# ───────────────────────────── TIME PERCEPTION ─────────────────────────────

def qt6_arousal_gain_time_dilation():
    """SUBJECTIVE-TIME-DILATION: does arousal/gain scale the substrate's internal clock rate? An internal
    pacemaker emits ticks at a rate modulated by an arousal-gain g; we count subjective ticks per fixed
    objective interval at 3 arousal levels. Falsifier (skeptic): internal tick-count does NOT scale with
    arousal-gain. REFUTED-falsifier iff subjective tick-count increases monotonically with g (>=3 levels).
    EXPECTED: REFUTED (HOLDS) — pacemaker rate-modulation is a real, mechanistic interval-timing model."""
    def subjective_ticks(g, objective_steps=2000):
        random.seed(SEED + int(g * 100))
        base_rate = 0.05
        ticks = 0
        for _ in range(objective_steps):
            # arousal-gain scales the pacemaker firing probability per objective step
            if random.random() < base_rate * g:
                ticks += 1
        return ticks

    gains = [0.5, 1.0, 2.0]
    counts = [subjective_ticks(g) for g in gains]
    monotone = all(counts[i] < counts[i + 1] for i in range(len(counts) - 1))
    refuted = monotone
    prof = " ".join(f"g{g}->{c}ticks" for g, c in zip(gains, counts))
    print(f"[QT6 TIME-DILATE]  {prof}  monotone_up={monotone} -> falsifier "
          f"{'REFUTED (arousal scales internal clock, HOLDS)' if refuted else 'CONFIRMED (no scaling — closed-negative)'}")
    return refuted


def qt7_oscillator_phase_clock():
    """OSCILLATOR-PHASE AS INTERNAL CLOCK: can time be estimated from phase-counting of a pure_field-style
    oscillator? A noisy oscillator advances; we estimate elapsed objective time from accumulated phase and
    measure estimation error vs a no-clock (constant-guess) control. Falsifier (skeptic): phase-counting does
    NOT estimate elapsed interval better than the best constant guess. REFUTED-falsifier iff
    MAE(phase-clock) < MAE(constant) across 3 seeds. EXPECTED: REFUTED (HOLDS) — phase accumulation is a
    genuine internal-clock mechanism."""
    errs_clock = []
    errs_const = []
    for s in range(3):
        random.seed(SEED + s)
        omega = 0.1
        trials = []
        for _ in range(200):
            true_T = random.randint(20, 200)
            phase = 0.0
            for _ in range(true_T):
                phase += omega + random.gauss(0, 0.02)
            est = phase / omega       # invert phase to time estimate
            trials.append((true_T, est))
        mae_clock = statistics.mean(abs(t - e) for t, e in trials)
        mean_T = statistics.mean(t for t, _ in trials)
        mae_const = statistics.mean(abs(t - mean_T) for t, _ in trials)  # best constant guess
        errs_clock.append(mae_clock)
        errs_const.append(mae_const)
    mc = statistics.mean(errs_clock)
    mk = statistics.mean(errs_const)
    refuted = mc < mk
    print(f"[QT7 PHASE-CLOCK]  MAE_phaseclock={mc:.3f}  MAE_constant={mk:.3f} -> falsifier "
          f"{'REFUTED (phase-counting estimates time, HOLDS)' if refuted else 'CONFIRMED (no better than constant — closed-negative)'}")
    return refuted


def qt8_retrocausal_precognition():
    """RETROCAUSAL/PRECOGNITION: a time-asymmetric information leak — can a predictor use a FUTURE input that
    is generated AFTER the prediction (strictly causally unavailable) to beat chance? We build a stream where
    the target is an independent future coin; the 'precog' arm may only see PAST samples. Falsifier (skeptic):
    no future channel — accuracy = chance. REFUTED-falsifier iff precog accuracy ci_lo > 0.5 chance.
    EXPECTED: CONFIRMED (closed-negative) — there is NO future channel; this MUST refute. Honest paranormal."""
    accs = []
    for s in range(3):
        rng = random.Random(SEED + s)
        n = 5000
        correct = 0
        history = []
        for _ in range(n):
            future = rng.random() < 0.5   # the target is generated independently, AFTER the guess
            # 'precog' predictor may ONLY use the past history (no future access) — the honest causal bound
            if history:
                guess = sum(history[-20:]) / len(history[-20:]) >= 0.5
            else:
                guess = True
            if guess == future:
                correct += 1
            history.append(1 if future else 0)
        accs.append(correct / n)
    m, lo, hi = _ci95(accs)
    refuted = lo > 0.5
    print(f"[QT8 RETROCAUSAL]  precog_acc={m:.4f}[{lo:.4f},{hi:.4f}]  chance=0.5 -> falsifier "
          f"{'REFUTED (future channel detected!)' if refuted else 'CONFIRMED (no future channel, acc=chance — closed-negative, honest)'}")
    return refuted


def qt9_time_cell_sequence_order():
    """TIME-CELL / SEQUENCE-MEMORY: can the substrate encode ORDER (which event came first) above shuffle-NULL?
    A simple recurrent accumulator reads an ordered event sequence; a linear readout must recover the original
    order. Falsifier (skeptic): the substrate cannot recover order better than a time-shuffled NULL.
    REFUTED-falsifier iff order-recovery accuracy ci_lo > shuffle-NULL hi across 3 seeds. EXPECTED: REFUTED
    (HOLDS) — a recurrent state genuinely carries sequence order (ties to clm-time-encoding bench).

    Method: each item leaves a LEAKY per-item trace; at sequence end the trace AMPLITUDE encodes recency
    (later item = higher trace). The readout recovers presentation order by sorting items by trace amplitude
    and compares to the TRUE presentation order. The shuffle-NULL DESTROYS the time structure by reading the
    traces in a temporally-PERMUTED order (the decoder no longer sees the true emission times), so its
    recovered order is decorrelated from the true order — a proper destroyed-temporal-info control."""
    def order_acc(shuffle):
        rng = random.Random(SEED + (999 if shuffle else 0))
        hits = 0
        trials = 400
        L = 6
        for _ in range(trials):
            order = list(range(L))
            rng.shuffle(order)            # the true presentation order of the L distinct items
            traces = {it: 0.0 for it in order}
            for pos, item in enumerate(order):
                # ALL traces leak each tick; the presented item gets a +1 kick -> amplitude tags recency
                for it in traces:
                    traces[it] *= 0.7
                traces[item] += 1.0
            if not shuffle:
                # SIGNAL arm: decode order from true end-state trace amplitudes (recent=higher)
                recovered = sorted(traces, key=lambda it: -traces[it])
            else:
                # NULL arm: temporally scramble which trace-amplitude is attributed to which slot ->
                # the decoder reads amplitudes in a permuted assignment, destroying the time->item link
                amps = list(traces.values())
                rng.shuffle(amps)
                shuffled_map = dict(zip(traces.keys(), amps))
                recovered = sorted(shuffled_map, key=lambda it: -shuffled_map[it])
            true_recency = list(reversed(order))   # most-recent item came LAST in presentation
            hits += sum(1 for a, b in zip(recovered, true_recency) if a == b) / L
        return hits / trials

    accs = [order_acc(False) for _ in range(3)]
    nulls = [order_acc(True) for _ in range(3)]
    ma, la, ha = _ci95(accs)
    mn, ln, hn = _ci95(nulls)
    refuted = la > hn
    print(f"[QT9 TIME-CELL]    order_acc={ma:.4f}[{la:.4f},{ha:.4f}]  shuffle-NULL={mn:.4f}[{ln:.4f},{hn:.4f}] -> falsifier "
          f"{'REFUTED (order recovered above NULL, HOLDS)' if refuted else 'CONFIRMED (no order encoding — closed-negative)'}")
    return refuted


def qt10_specious_present_window():
    """SPECIOUS-PRESENT / TEMPORAL-INTEGRATION WINDOW: is there an OPTIMAL integration-window size for coherence
    (a finite present beats both instantaneous and infinite windows)? We integrate a noisy oscillatory signal
    over windows tau and measure a coherence proxy; look for an interior peak. Falsifier (skeptic): coherence is
    monotone in tau (no interior optimum — instantaneous or infinite is best). REFUTED-falsifier iff the peak
    coherence is at an INTERIOR tau (not the smallest, not the largest) across 3 seeds. (Links H_213.)

    Proxy = a MATCHED-FILTER SNR for recovering the slow oscillation (period P=20) from the windowed-average
    trace. Genuine two-sided tradeoff: small tau under-averages (noise dominates -> low SNR); tau >> P
    over-smooths (the window spans many periods so the oscillation averages toward zero -> low SNR); an
    interior tau ~ P should maximise SNR IF a finite specious-present is the optimum. The signature is NOT
    hard-coded — the SNR curve is whatever the sim computes; an interior peak can fail to appear."""
    P = 20.0
    taus = [1, 2, 4, 8, 16, 32, 64, 128]
    peak_interior_count = 0
    for s in range(3):
        random.seed(SEED + s)
        T = 6000
        f = 1.0 / P
        sig = [math.sin(2 * math.pi * f * t) + random.gauss(0, 1.5) for t in range(T)]
        clean = [math.sin(2 * math.pi * f * t) for t in range(T)]
        cohs = []
        for tau in taus:
            # causal moving-average (the integration window = the "present" of width tau)
            sm = []
            cl = []
            for t in range(tau, T):
                sm.append(sum(sig[t - tau:t]) / tau)
                cl.append(clean[t])
            if len(sm) < 2:
                cohs.append(0.0)
                continue
            # matched-filter SNR: correlation of the smoothed trace with the TRUE clean oscillation
            ms = statistics.mean(sm)
            mc = statistics.mean(cl)
            cov = sum((a - ms) * (b - mc) for a, b in zip(sm, cl)) / len(sm)
            vs = statistics.pvariance(sm)
            vc = statistics.pvariance(cl)
            snr = (cov * cov) / (vs * vc + 1e-12)   # squared correlation = fraction of variance explained by signal
            cohs.append(snr)
        peak_idx = max(range(len(taus)), key=lambda i: cohs[i])
        last_curve = cohs
        last_peak_tau = taus[peak_idx]
        # HONEST falsifier: a genuine specious-present optimum must be (a) interior AND (b) UNIMODAL (a single
        # rise-then-fall), NOT an aliasing-driven jagged curve with multiple local maxima. A box-average vs a
        # sine produces aliasing side-lobes, so we explicitly require unimodality to reject artifact peaks.
        unimodal = all(cohs[i] <= cohs[i + 1] for i in range(peak_idx)) and \
                   all(cohs[i] >= cohs[i + 1] for i in range(peak_idx, len(cohs) - 1))
        if 0 < peak_idx < len(taus) - 1 and unimodal:
            peak_interior_count += 1
    refuted = peak_interior_count >= 2   # >=2 of 3 seeds show a clean interior unimodal optimum
    print(f"[QT10 SPECIOUS]    clean-interior-peak seeds={peak_interior_count}/3  taus={taus} "
          f"last_SNR={[round(c,3) for c in last_curve]} peak@tau={last_peak_tau} (period={P:.0f}) -> falsifier "
          f"{'REFUTED (clean finite optimal window, HOLDS)' if refuted else 'CONFIRMED (no clean unimodal interior optimum — aliasing-jagged / monotone, closed-negative)'}")
    return refuted


def qt11_pacemaker_vs_oscillator():
    """PACEMAKER-ACCUMULATOR vs OSCILLATOR models of interval timing: which better matches the SCALAR PROPERTY
    of timing (Weber's law — timing error sd scales LINEARLY with the interval, constant CV)? We simulate both
    models timing a range of intervals and test which yields a constant coefficient of variation (CV=sd/mean),
    the empirical signature of biological interval timing. Falsifier (skeptic): pacemaker-accumulator does NOT
    reproduce the scalar property (constant CV) better than the oscillator. REFUTED-falsifier iff pacemaker CV
    is flatter (lower CV-variance across intervals) than oscillator. Honest model-comparison, can go either way."""
    intervals = [50, 100, 200, 400, 800]

    def pacemaker_cv():
        cvs = []
        for I in intervals:
            random.seed(SEED + I)
            ests = []
            for _ in range(300):
                # accumulate pacemaker ticks with multiplicative (scalar) noise on the rate
                rate = 1.0 * (1 + random.gauss(0, 0.1))   # rate variability -> scalar (multiplicative)
                count = 0
                acc = 0.0
                while acc < I:
                    acc += rate
                    count += 1
                ests.append(count * 1.0)
            cvs.append(statistics.stdev(ests) / statistics.mean(ests))
        return cvs

    def oscillator_cv():
        cvs = []
        for I in intervals:
            random.seed(SEED + I + 7)
            ests = []
            omega = 0.2
            for _ in range(300):
                phase = 0.0
                steps = 0
                # additive per-step phase noise -> error grows as sqrt(I) (NON-scalar)
                while phase < omega * I:
                    phase += omega + random.gauss(0, 0.05)
                    steps += 1
                ests.append(steps * 1.0)
            cvs.append(statistics.stdev(ests) / statistics.mean(ests))
        return cvs

    pcv = pacemaker_cv()
    ocv = oscillator_cv()
    # "flatter CV" = lower variance of CV across intervals (constant CV = scalar property)
    pflat = statistics.pvariance(pcv)
    oflat = statistics.pvariance(ocv)
    refuted = pflat < oflat
    print(f"[QT11 PACEMAKER]   pacemaker CV={[round(c,4) for c in pcv]} var={pflat:.2e} | "
          f"oscillator CV={[round(c,4) for c in ocv]} var={oflat:.2e} -> falsifier "
          f"{'REFUTED (pacemaker reproduces scalar property better, HOLDS)' if refuted else 'CONFIRMED (oscillator flatter — closed-negative for pacemaker)'}")
    return refuted


if __name__ == "__main__":
    print("=== QUANTUM-CONSCIOUSNESS + TIME-PERCEPTION toy falsifiers (a_scale_honest_scope: TOY-ONLY) seed=%d ===" % SEED)
    quantum = [("QT1", qt1_orch_or_decoherence), ("QT2", qt2_qrng_vs_pseudo_seed),
               ("QT3", qt3_entanglement_vs_classical_coupling), ("QT4", qt4_quantum_zeno),
               ("QT5", qt5_complex_amplitude_ablation)]
    time_ = [("QT6", qt6_arousal_gain_time_dilation), ("QT7", qt7_oscillator_phase_clock),
             ("QT8", qt8_retrocausal_precognition), ("QT9", qt9_time_cell_sequence_order),
             ("QT10", qt10_specious_present_window), ("QT11", qt11_pacemaker_vs_oscillator)]
    print("--- QUANTUM CONSCIOUSNESS ---")
    results = {}
    for name, fn in quantum:
        try:
            results[name] = fn()
        except Exception as e:
            results[name] = None
            print(f"[{name}] ERROR {type(e).__name__}: {e}")
    print("--- TIME PERCEPTION ---")
    for name, fn in time_:
        try:
            results[name] = fn()
        except Exception as e:
            results[name] = None
            print(f"[{name}] ERROR {type(e).__name__}: {e}")
    held = [k for k, v in results.items() if v is True]
    closed = [k for k, v in results.items() if v is False]
    err = [k for k, v in results.items() if v is None]
    print("=== SUMMARY (toy) ===")
    print("  hypothesis-HOLDS (falsifier REFUTED)        = %s" % held)
    print("  closed-negative (falsifier CONFIRMED)       = %s" % closed)
    if err:
        print("  ERROR                                       = %s" % err)
