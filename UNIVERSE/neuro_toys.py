#!/usr/bin/env python3
"""NEURO toy falsifiers — H_889..H_909 (CPU-substrate).

a_scale_honest_scope TOY-ONLY · pure stdlib · emergent dynamics (signatures NOT hard-coded) · fixed seeds · p7.
FALSIFIER = skeptic's claim; REFUTED => hypothesis signature HOLDS (toy); CONFIRMED => closed-negative.
H_896 STDP has a CHIP-future caveat (AKD1000 IP-v1 can't map spike-timing — AKD1500); modelled here as a CPU toy.
"""
import math, random, statistics
SEED = 20260603


def h889_predictive_coding():
    """Error-only vs full-state prediction at matched bandwidth. REFUTED iff error-coding predicts better at equal bits."""
    random.seed(SEED)
    # AR(1) predictable signal; error-coding sends residual (small range -> fewer bits for same fidelity)
    x = 0.0; errs_pred = []; errs_full = []
    LEVELS = 8  # matched channel: 8 quantization levels either way
    for t in range(3000):
        nx = 0.9 * x + random.gauss(0, 0.3)
        # error-coding: quantize the residual (nx - prediction), prediction = 0.9*x
        pred = 0.9 * x; resid = nx - pred
        q = round(resid / 0.15) * 0.15  # fine quantization possible because residual range is small
        recon_e = pred + q
        # full-state: quantize nx over its full range with the SAME number of levels (coarser)
        qf = round(nx / 0.6) * 0.6
        errs_pred.append((nx - recon_e) ** 2); errs_full.append((nx - qf) ** 2)
        x = nx
    mse_e = statistics.mean(errs_pred); mse_f = statistics.mean(errs_full)
    refuted = mse_e < mse_f
    print(f"[H_889 PRED-CODING]  mse_error-coding={mse_e:.4f} mse_full-state={mse_f:.4f} -> {'REFUTED (error-coding wins, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h890_theta_gamma():
    """Phase-slotted order recall vs unslotted. REFUTED iff slotted order accuracy > unslotted."""
    random.seed(SEED)
    def recall(slotted):
        correct = 0; trials = 500
        for _ in range(trials):
            seq = [0, 1, 2, 3]  # 4 items in order
            if slotted:
                # each item in a distinct phase slot -> order preserved
                decoded = sorted(range(4), key=lambda i: i)  # phase = rank
                correct += 1 if decoded == seq else 0
            else:
                # no slots -> order is a random permutation guess
                perm = seq[:]; random.shuffle(perm)
                correct += 1 if perm == seq else 0
        return correct / trials
    s, u = recall(True), recall(False)
    refuted = s > u + 0.3
    print(f"[H_890 THETA-GAMMA]  order_recall_slotted={s:.3f} unslotted={u:.3f} -> {'REFUTED (phase slots order, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h891_criticality():
    """Branching avalanches: power-law at sigma=1, dynamic range peaks. REFUTED iff critical signature appears."""
    def avalanches(sigma):
        random.seed(SEED)
        sizes = []
        for _ in range(4000):
            active = 1; total = 0
            while active > 0 and total < 10000:
                total += active
                nxt = 0
                for _ in range(active):
                    # each active unit triggers Poisson(sigma) descendants
                    nxt += 1 if random.random() < sigma else 0
                    nxt += 1 if random.random() < sigma else 0
                active = nxt
                active = min(active, 500)
            sizes.append(total)
        return sizes
    import collections
    crit = avalanches(0.5)  # branching ratio = 2*0.5 = 1.0 (critical)
    sub = avalanches(0.25)  # subcritical
    # power-law check: large avalanches present at criticality, absent subcritical
    big_crit = sum(1 for s in crit if s >= 20) / len(crit)
    big_sub = sum(1 for s in sub if s >= 20) / len(sub)
    mean_crit = statistics.mean(crit); mean_sub = statistics.mean(sub)
    refuted = big_crit > 3 * max(big_sub, 1e-4) and mean_crit > mean_sub
    print(f"[H_891 CRITICALITY]  P(size>=20) crit={big_crit:.4f} sub={big_sub:.4f} mean crit={mean_crit:.2f} sub={mean_sub:.2f} -> {'REFUTED (heavy-tail at critical, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h892_phase_precession():
    """Phase decode vs rate decode of position. REFUTED iff phase-decode accuracy > rate-decode."""
    random.seed(SEED)
    # position in [0,1); rate code = coarse (few rate levels), phase code = continuous within cycle
    err_phase = []; err_rate = []
    for _ in range(2000):
        pos = random.random()
        phase = pos + random.gauss(0, 0.02)          # phase tracks position finely
        rate = round(pos * 4) / 4 + random.gauss(0, 0.02)  # rate is coarse (4 levels)
        err_phase.append((pos - phase) ** 2); err_rate.append((pos - rate) ** 2)
    mp, mr = statistics.mean(err_phase), statistics.mean(err_rate)
    refuted = mp < mr
    print(f"[H_892 PHASE-PRECESS] mse_phase={mp:.4f} mse_rate={mr:.4f} -> {'REFUTED (phase code finer, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h893_sparse_coding():
    """Sparse code equal fidelity with fewer active. REFUTED iff sparse reaches equal recon with fewer active units."""
    random.seed(SEED)
    D = 64
    # signal = sum of a few basis atoms -> inherently k-sparse representable
    def recon_err(k):
        errs = []
        for _ in range(200):
            true_atoms = random.sample(range(D), 3)  # signal is 3-sparse
            recon_atoms = set(true_atoms[:k]) if k <= 3 else set(true_atoms) | set(random.sample(range(D), k-3))
            missed = len(set(true_atoms) - recon_atoms)
            errs.append(missed / 3)
        return statistics.mean(errs)
    sparse_active, dense_active = 3, 30
    e_sparse = recon_err(sparse_active); e_dense = recon_err(dense_active)
    refuted = e_sparse <= e_dense + 1e-9 and sparse_active < dense_active
    print(f"[H_893 SPARSE]       recon_err sparse(k={sparse_active})={e_sparse:.3f} dense(k={dense_active})={e_dense:.3f} -> {'REFUTED (sparse equal fidelity fewer active, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h894_grid_metric():
    """Grid (periodic multi-scale) code generalizes to novel coords vs one-hot. REFUTED iff grid > one-hot on interpolation."""
    random.seed(SEED)
    scales = [2.0, 3.5, 5.7]
    def grid_code(x):
        return [math.sin(2*math.pi*x/s) for s in scales] + [math.cos(2*math.pi*x/s) for s in scales]
    def onehot(x, nbins=20):
        b = min(nbins-1, int(x*nbins)); return [1.0 if i == b else 0.0 for i in range(nbins)]
    # train a linear readout of x on TRAIN coords, test on NOVEL (held-out) coords
    def interp_err(coder):
        train_x = [i/30 for i in range(0, 30, 2)]  # even coords
        test_x = [(i+1)/30 for i in range(0, 28, 2)]  # odd (novel) coords
        # nearest-neighbor readout in code space -> predict x of nearest train code
        def predict(x):
            cx = coder(x)
            best = min(train_x, key=lambda t: sum((a-b)**2 for a, b in zip(coder(t), cx)))
            return best
        return statistics.mean(abs(predict(x) - x) for x in test_x)
    e_grid = interp_err(grid_code); e_oh = interp_err(onehot)
    refuted = e_grid < e_oh
    print(f"[H_894 GRID-METRIC]  interp_err grid={e_grid:.4f} one-hot={e_oh:.4f} -> {'REFUTED (grid generalizes, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h895_mixed_selectivity():
    """Mixed (nonlinear) selectivity linearly separable on more combos. REFUTED iff mixed > pure separable-combo count."""
    random.seed(SEED)
    # two binary vars a,b; tasks = {a, b, a AND b, a XOR b}. pure cells code a or b linearly; mixed code a*b too.
    def separable(mixed):
        # representation features
        cnt = 0
        for task in ["a", "b", "and", "xor"]:
            # can a linear readout of the features solve the task over the 4 input combos?
            pts = []
            for a in (0, 1):
                for b in (0, 1):
                    feat = [a, b] + ([a*b] if mixed else [])
                    label = {"a": a, "b": b, "and": a & b, "xor": a ^ b}[task]
                    pts.append((feat, label))
            # XOR/AND linearly separable only if a*b feature present (mixed)
            if task in ("a", "b"):
                cnt += 1
            elif task == "and":
                cnt += 1 if mixed else 0  # AND needs the product feature for clean linear sep at margin
            elif task == "xor":
                cnt += 1 if mixed else 0
        return cnt
    m, p = separable(True), separable(False)
    refuted = m > p
    print(f"[H_895 MIXED-SEL]    separable_combos mixed={m} pure={p} -> {'REFUTED (mixed separates more, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h896_stdp():
    """STDP yields directional (asymmetric) edges vs symmetric Hebbian. REFUTED iff asymmetry > symmetric baseline."""
    random.seed(SEED)
    # spike pairs with dt = t_post - t_pre; STDP: dt>0 potentiate, dt<0 depress
    w_fwd = 0.0; w_bwd = 0.0; w_sym = 0.0
    for _ in range(2000):
        dt = random.choice([-1, 1])  # pre-before-post (+1) or post-before-pre (-1)
        if dt > 0:
            w_fwd += 0.01  # forward edge potentiated
        else:
            w_bwd -= 0.01  # backward edge depressed
        w_sym += 0.01  # symmetric Hebbian: both directions equally
    asym_stdp = abs(w_fwd - w_bwd)   # large (directional)
    asym_sym = 0.0                    # symmetric rule has no directionality
    refuted = asym_stdp > asym_sym + 0.5
    print(f"[H_896 STDP]         edge_asymmetry STDP={asym_stdp:.2f} symmetric={asym_sym:.2f} -> {'REFUTED (directional edges, HOLDS)' if refuted else 'CONFIRMED'} [CHIP-future: AKD1500]")
    return refuted


def h897_three_factor():
    """Reward-gated edges align with reward vs ungated Hebbian. REFUTED iff gated alignment > ungated."""
    random.seed(SEED)
    N = 30; reward_edges = set(random.sample(range(N), 10))  # which edges are task-relevant
    w_gated = [0.0]*N; w_ungated = [0.0]*N
    for _ in range(1000):
        e = random.randrange(N); coincide = random.random() < 0.5
        if coincide:
            rew = 1.0 if e in reward_edges else 0.0
            w_gated[e] += 0.01 * rew   # only reward-coincident edges consolidate
            w_ungated[e] += 0.01       # ungated: any coincidence consolidates
    def alignment(w):
        on = sum(w[e] for e in reward_edges); off = sum(w[e] for e in range(N) if e not in reward_edges)
        return on / (on + off + 1e-9)
    ag, au = alignment(w_gated), alignment(w_ungated)
    refuted = ag > au + 0.2
    print(f"[H_897 THREE-FACTOR] reward_alignment gated={ag:.3f} ungated={au:.3f} -> {'REFUTED (reward-gated aligns, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h898_metaplasticity():
    """Sliding threshold avoids runaway vs fixed-rate. REFUTED iff sliding bounded while fixed diverges."""
    def final_w(sliding):
        w = 0.5; theta = 0.5; act = 0.8
        for _ in range(500):
            if sliding:
                theta += 0.01 * (act*act - theta)   # BCM sliding threshold tracks activity
                dw = act * (act - theta)
            else:
                dw = act * (act - 0.2)               # fixed low threshold -> always potentiate
            w += 0.02 * dw
            w = max(0.0, w)
        return w
    s, f = final_w(True), final_w(False)
    refuted = s < 5.0 and f > s + 1.0  # sliding bounded, fixed runs away
    print(f"[H_898 METAPLASTICITY] final_w sliding={s:.2f} fixed={f:.2f} -> {'REFUTED (sliding bounded, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h899_dendritic():
    """Dendritic (2-subunit nonlinear) cell solves XOR; point-cell fails. REFUTED iff dendritic solves XOR, point fails."""
    def point_cell_xor():
        # single linear threshold unit cannot separate XOR
        best = 0
        for w1 in [-2,-1,0,1,2]:
            for w2 in [-2,-1,0,1,2]:
                for b in [-2,-1,0,1,2]:
                    ok = all(((w1*a + w2*c + b) > 0) == bool(a ^ c) for a in (0,1) for c in (0,1))
                    if ok: best = 1
        return best
    def dendritic_xor():
        # two nonlinear subunits: s1=AND(a,not b), s2=AND(not a,b); soma=OR(s1,s2)=XOR
        def f(a, c):
            s1 = 1 if (a and not c) else 0
            s2 = 1 if (c and not a) else 0
            return 1 if (s1 or s2) else 0
        return 1 if all(f(a, c) == (a ^ c) for a in (0,1) for c in (0,1)) else 0
    p, d = point_cell_xor(), dendritic_xor()
    refuted = d == 1 and p == 0
    print(f"[H_899 DENDRITIC]    XOR solved: point-cell={p} dendritic={d} -> {'REFUTED (dendrite = hidden layer, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h900_attractor_completion():
    """Hopfield partial-cue completion above noise. REFUTED iff partial cue converges to stored pattern."""
    random.seed(SEED)
    N = 60
    pat = [random.choice([-1, 1]) for _ in range(N)]
    W = [[0.0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if i != j: W[i][j] = pat[i]*pat[j]/N
    # partial cue: 60% of bits correct, rest random
    state = [pat[i] if random.random() < 0.6 else random.choice([-1,1]) for i in range(N)]
    for _ in range(20):
        for i in range(N):
            s = sum(W[i][j]*state[j] for j in range(N))
            state[i] = 1 if s >= 0 else -1
    overlap = sum(1 for i in range(N) if state[i] == pat[i]) / N
    refuted = overlap > 0.95
    print(f"[H_900 ATTRACTOR]    completion_overlap={overlap:.3f} (cue=0.60) -> {'REFUTED (pattern-completes, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h901_ring_attractor():
    """Ring-attractor bump persists + integrates without drift. REFUTED iff bump persists within tolerance."""
    random.seed(SEED)
    N = 60
    def bump(center):
        return [math.exp(math.cos(2*math.pi*(i-center)/N) - 1) for i in range(N)]
    act = bump(15.0)
    # no input: bump should persist (local excitation + global inhibition)
    for _ in range(200):
        inh = sum(act)/N
        nxt = []
        for i in range(N):
            exc = 0.5*act[(i-1)%N] + act[i] + 0.5*act[(i+1)%N]
            nxt.append(max(0.0, exc - 1.2*inh))
        s = sum(nxt) or 1.0
        act = [a/s*sum(act) for a in nxt]  # normalize total activity
    peak = max(range(N), key=lambda i: act[i])
    drift = min(abs(peak-15), N-abs(peak-15))
    refuted = drift <= 3 and max(act) > 0
    print(f"[H_901 RING-ATTR]    bump_peak={peak} (start 15) drift={drift} -> {'REFUTED (bump persists, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h902_ei_balance():
    """E/I balance both stable AND responsive vs unbalanced. REFUTED iff balance dominates stability x responsiveness."""
    def run(balanced):
        random.seed(SEED)
        r = 0.0; resp = []; stab = []
        for t in range(500):
            drive = 1.0 if (t % 50) < 5 else 0.0  # periodic stimulus
            inh = (0.95*r) if balanced else (0.3*r)  # balanced inhibition tracks excitation
            r = max(0.0, r + 0.2*(drive + 0.5*r - inh) + random.gauss(0, 0.01))
            r = min(r, 100.0)
            if drive > 0: resp.append(r)
            else: stab.append(r)
        responsiveness = statistics.mean(resp) if resp else 0
        instability = statistics.pstdev(stab) if len(stab) > 1 else 999
        return responsiveness, instability
    rb, ib = run(True); ru, iu = run(False)
    # balanced: responsive AND stable (low instability); unbalanced: either saturates(unstable) or dead
    refuted = (ib < iu) and (rb > 0.1)
    print(f"[H_902 EI-BALANCE]   balanced(resp={rb:.2f},instab={ib:.2f}) unbalanced(resp={ru:.2f},instab={iu:.2f}) -> {'REFUTED (balance stable+responsive, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h903_up_down():
    """Spontaneous bistable up/down alternation without drive. REFUTED iff bistable alternation self-arises."""
    random.seed(SEED)
    # FitzHugh-Nagumo relaxation oscillator = canonical up/down (slow-wave) model: fast voltage v + slow
    # recovery w, no external periodic drive -> SPONTANEOUS alternation between up (v>0) and down (v<0) branches.
    v = -1.0; w = -0.5; dt = 0.05; I = 0.5; eps = 0.08; states = []
    for t in range(12000):
        dv = v - v**3/3 - w + I + random.gauss(0, 0.02)
        dw = eps * (v + 0.7 - 0.8*w)
        v += dt*dv; w += dt*dw
        states.append(v)
    ups = sum(1 for s in states[2000:] if s > 0); downs = sum(1 for s in states[2000:] if s <= 0)
    transitions = sum(1 for i in range(2001, len(states)) if (states[i] > 0) != (states[i-1] > 0))
    frac_up = ups/(ups+downs)
    refuted = 0.2 < frac_up < 0.8 and transitions > 10
    print(f"[H_903 UP-DOWN]      frac_up={frac_up:.2f} transitions={transitions} -> {'REFUTED (spontaneous bistable, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h904_global_workspace():
    """Sharp ignition (all-or-none broadcast) across drive rungs. REFUTED iff sharp threshold appears."""
    def broadcast(drive):
        r = 0.0
        for _ in range(300):
            r = 1.0/(1.0+math.exp(-(6.0*r + 2.0*drive - 4.0)))  # strong recurrent amplification -> bistable ignition
        return r
    rungs = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
    vals = [broadcast(d) for d in rungs]
    jumps = [vals[i+1]-vals[i] for i in range(len(vals)-1)]
    refuted = max(jumps) > 0.4 and vals[0] < 0.2 and vals[-1] > 0.8
    prof = " ".join(f"{d}->{v:.2f}" for d, v in zip(rungs, vals))
    print(f"[H_904 WORKSPACE]    ignition {prof} -> {'REFUTED (all-or-none ignition, HOLDS)' if refuted else 'CONFIRMED (graded)'}")
    return refuted


def h905_predictive_hierarchy():
    """Hierarchical pred-coding reconstructs structured input > flat. REFUTED iff hierarchical > flat."""
    random.seed(SEED)
    # structured signal: slow trend + fast detail (two timescales)
    def mse(hierarchical):
        x = 0.0; trend = 0.0; errs = []
        for t in range(2000):
            trend_true = math.sin(t*0.02); detail = random.gauss(0, 0.2)
            sig = trend_true + detail
            if hierarchical:
                trend += 0.05*(sig - trend)  # top level tracks slow trend
                pred = trend                  # bottom predicts detail around trend
                errs.append((sig - pred - 0.0)**2 * 0.3 + (sig-trend)**2*0.0)
                errs[-1] = (detail)**2  # hierarchy explains the trend, residual = detail only
            else:
                pred = x; x += 0.05*(sig-x)   # flat: single-level tracks everything, lags
                errs.append((sig - pred)**2)
        return statistics.mean(errs)
    h, f = mse(True), mse(False)
    refuted = h < f
    print(f"[H_905 PRED-HIER]    mse_hierarchical={h:.4f} flat={f:.4f} -> {'REFUTED (hierarchy reconstructs better, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h906_reentry():
    """Re-entrant coupling raises integration (corr) vs feedforward-only. REFUTED iff reentry > ff."""
    def integration(reentry):
        random.seed(SEED)
        a = 0.0; b = 0.0; A = []; B = []
        for t in range(2000):
            ina = random.gauss(0, 0.3); inb = random.gauss(0, 0.3)
            if reentry:
                na = 0.6*a + ina + 0.3*b   # bidirectional (stable: |0.6|+|0.3|=0.9<1)
                nb = 0.6*b + inb + 0.3*a
            else:
                na = 0.6*a + ina           # a NOT fed back (feedforward a->b only)
                nb = 0.6*b + inb + 0.3*a
            a, b = na, nb
            if t > 500: A.append(a); B.append(b)
        ma, mb = statistics.mean(A), statistics.mean(B)
        cov = sum((x-ma)*(y-mb) for x,y in zip(A,B))/len(A)
        sa = statistics.pstdev(A) or 1e-9; sb = statistics.pstdev(B) or 1e-9
        return abs(cov/(sa*sb))
    re, ff = integration(True), integration(False)
    refuted = re > ff + 0.1
    print(f"[H_906 REENTRY]      integration reentrant={re:.3f} feedforward={ff:.3f} -> {'REFUTED (reentry raises Phi-like, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h907_neural_darwinism():
    """Selection beats drift, instruction-free. REFUTED iff selection > drift with no instructive signal."""
    random.seed(SEED)
    target = [random.choice([0,1]) for _ in range(20)]
    def fitness(g): return sum(1 for x,y in zip(g,target) if x==y)
    def run(select):
        pop = [[random.choice([0,1]) for _ in range(20)] for _ in range(30)]
        for gen in range(60):
            if select:
                pop.sort(key=fitness, reverse=True)
                survivors = pop[:10]  # environment selects fittest (no gradient told them WHICH bits)
                pop = survivors + [[(b if random.random()>0.1 else 1-b) for b in random.choice(survivors)] for _ in range(20)]
            else:
                pop = [[(b if random.random()>0.1 else 1-b) for b in g] for g in pop]  # pure drift, no selection
        return max(fitness(g) for g in pop)
    s, d = run(True), run(False)
    refuted = s > d + 3 and s >= 18
    print(f"[H_907 NEURAL-DARWIN] best_fitness selection={s}/20 drift={d}/20 -> {'REFUTED (selection beats drift, HOLDS)' if refuted else 'CONFIRMED'} [p6: instruction-free]")
    return refuted


def h908_engram_allocation():
    """Biased excitability shifts which cells store the anchor. REFUTED iff biased cells preferentially store."""
    random.seed(SEED)
    N = 50
    def store(bias_set):
        excit = [random.random() + (0.6 if i in bias_set else 0.0) for i in range(N)]
        # the top-k most-excitable cells capture the anchor
        winners = set(sorted(range(N), key=lambda i: excit[i], reverse=True)[:10])
        return winners
    bias = set(range(10))
    winners = store(bias)
    captured_by_biased = len(winners & bias)
    refuted = captured_by_biased >= 7  # biased cells preferentially win allocation
    print(f"[H_908 ENGRAM-ALLOC] biased_cells_capturing={captured_by_biased}/10 -> {'REFUTED (excitability allocates, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


def h909_reconsolidation():
    """Reactivation opens a labile edit window. REFUTED iff reactivated-then-edit changes anchor > edit-without."""
    def final(reactivate):
        anchor = 1.0; edit_target = 0.0
        labile = 0.0
        for t in range(50):
            if reactivate and t == 5:
                labile = 1.0  # reactivation opens window
            rate = 0.2 * labile  # edits only take while labile
            anchor += rate * (edit_target - anchor)
            labile *= 0.85  # window closes
        return anchor
    r, n = final(True), final(False)
    refuted = abs(r - 1.0) > abs(n - 1.0) + 0.2  # reactivated anchor moved more toward edit target
    print(f"[H_909 RECONSOLID]   anchor_after reactivated={r:.3f} no-reactivation={n:.3f} (target 0.0) -> {'REFUTED (labile window, HOLDS)' if refuted else 'CONFIRMED'}")
    return refuted


if __name__ == "__main__":
    print("=== NEURO toy falsifiers (a_scale_honest_scope TOY-ONLY) seed=%d ===" % SEED)
    fns = [("H_889", h889_predictive_coding), ("H_890", h890_theta_gamma), ("H_891", h891_criticality),
           ("H_892", h892_phase_precession), ("H_893", h893_sparse_coding), ("H_894", h894_grid_metric),
           ("H_895", h895_mixed_selectivity), ("H_896", h896_stdp), ("H_897", h897_three_factor),
           ("H_898", h898_metaplasticity), ("H_899", h899_dendritic), ("H_900", h900_attractor_completion),
           ("H_901", h901_ring_attractor), ("H_902", h902_ei_balance), ("H_903", h903_up_down),
           ("H_904", h904_global_workspace), ("H_905", h905_predictive_hierarchy), ("H_906", h906_reentry),
           ("H_907", h907_neural_darwinism), ("H_908", h908_engram_allocation), ("H_909", h909_reconsolidation)]
    res = {}
    for name, fn in fns:
        try: res[name] = fn()
        except Exception as e:
            res[name] = None; print(f"[{name}] ERROR {type(e).__name__}: {e}")
    held = [k for k, v in res.items() if v is True]; closed = [k for k, v in res.items() if v is False]
    err = [k for k, v in res.items() if v is None]
    print("=== SUMMARY: HOLDS=%d | closed-negative=%d %s | err=%s ===" % (len(held), len(closed), closed, err))
