"""H_1002 — big-Φ (system Φ_s) UPGRADE of the H_999/H_1001 imagination/planning finding.

MISSION
-------
H_999/H_1001 RE-OPENED the imagination/planning Φ-nulls (H_971/973/988/994 🔴)
by re-measuring with the FAITHFUL exact MIP-EI scalar Φ (iit4/faithful_phi.hexa):
internal generation RAISES Φ — imagination DRIFT d+2.09, planning depth-8 d+4.64
with a positive dose-response (rho +0.48), guided imagination null. faithful_phi
is a SINGLE information-partition scalar (min-cut MI / small-side).

This probe UPGRADES that to the FULL IIT 4.0 SYSTEM big-Φ (Φ_s) — the capstone
measure (`hexa-lang/stdlib/consciousness/iit4_bigphi.hexa`, M4) over the MIP of
the cause-effect STRUCTURE (distinctions M2 + 2nd-order relations M3), NOT just a
min-cut MI partition. big-Φ = the Φ-structure destroyed by the least-damaging
system bipartition. It is a STRONGER, structure-level measure.

QUESTION (H_1002): does the imagination/planning Φ-rise REPLICATE under big-Φ, or
was it specific to the MIP-EI scalar?

WHY A CPU MIRROR (and that it is the FAITHFUL big-Φ, proven ≡ the stdlib engine)
-------------------------------------------------------------------------------
The stdlib iit4_bigphi.hexa RUNS on this Mac (verified: COPY n=2 big-Φ=2.0,
SELF-COPY=0 — the iit4_test.hexa hand-verifiable cases reproduce; no fused GPU
natives, so the clm-decode-macos-link-gap does NOT apply). But it has no `hexa
verify` atom and its float `print` truncates, so the 30-seed Welch-t / Cohen-d
contrast is computed with a numpy mirror that reproduces the EXACT pipeline:
  TPM → distinctions (MICE small-φ over all purviews, all-bipartition MIP) →
  2nd-order congruent relations → big-Φ = min over directional bipartitions
  (unit 0 pinned to A) of (total − surviving structure).
The mirror is PROVEN byte-faithful against the stdlib engine on 9 reference TPMs
(n=2,3,4; the values are emitted by UNIVERSE/h1002_bigphi_ref.hexa as x1e9
integers and asserted here at |Δ|<1e-6) BEFORE it scores any condition. This is
the faithful IIT 4.0 big-Φ, NOT the H_912/H_931 proxy (a_phi_iit4_tool).

DISCRETIZATION (TPM, honest)
----------------------------
big-Φ needs a state-by-node TPM, NOT a continuous trajectory. For each regime's
toy WM latent trajectory we:
  - pick the top-N_UNITS variance latent channels (same selection rule as H_999);
  - BINARIZE each channel at its own median over the rollout → a binary state
    sequence (n-bit system state per timestep);
  - estimate the empirical state-by-node TPM:
    tpm[state*n + unit] = P(unit ON at t+1 | system in `state` at t),
    Laplace-smoothed (unseen state → uniform 0.5 row);
  - sys_state = the modal (most frequent) system state.
big-Φ is super-exponential (distinction search over 2^n mechanisms×purviews, MIP
over bipartitions), so N_UNITS is SMALL: N_UNITS=4 (vs H_999's n=8 faithful-Φ
discretization — a SMALLER toy rung, stated honestly per a_scale_honest_scope).
The SAME discretization is applied IDENTICALLY to every regime, so the CONTRAST
(the falsifier target) is fair. Toy single-rung; scale-transfer UNVERIFIED.

g5 CODE-measured (no LLM self-judge, p7).
"""
import sys, os, math, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "CWM", "probes"))
from cwm_probe_lib import LatentWorldModel, phi_proxy, cohens_d, welch_t, boot_ci, spearman, _aug1  # noqa: E402

# ═══════════════════════════════════════════════════════════════════════════
# CPU MIRROR of the stdlib IIT 4.0 big-Φ pipeline (iit4_tpm + iit4_distinction +
# iit4_relation + iit4_bigphi). Byte-faithful to the .hexa algorithm.
# ═══════════════════════════════════════════════════════════════════════════
def _bit(state, i):
    return (state // (2 ** i)) % 2

def _pow2(k):
    return 2 ** k

def _units(mask, n):
    return [i for i in range(n) if _bit(mask, i) == 1]

def _expand(compact, units):
    out = 0
    for b, u in enumerate(units):
        if _bit(compact, b) == 1:
            out += _pow2(u)
    return out

def _compact_index(abs_state, units):
    idx = 0
    for b, u in enumerate(units):
        if _bit(abs_state, u) == 1:
            idx += _pow2(b)
    return idx

# ── M1: TPM + repertoires + intrinsic difference ───────────────────────────
def tpm_on(tpm, n, state, unit):
    return tpm[state * n + unit]

def marginal_on(tpm, n, fix_mask, fix_state, target):
    full = _pow2(n)
    total = 0.0
    count = 0
    for s in range(full):
        ok = True
        for i in range(n):
            if _bit(fix_mask, i) == 1 and _bit(s, i) != _bit(fix_state, i):
                ok = False
                break
        if ok:
            total += tpm_on(tpm, n, s, target)
            count += 1
    return 0.0 if count == 0 else total / count

def effect_repertoire(tpm, n, mech_mask, mech_state, purview_mask):
    units = _units(purview_mask, n)
    k = len(units)
    p_on = [marginal_on(tpm, n, mech_mask, mech_state, u) for u in units]
    rep = []
    for cs in range(_pow2(k)):
        prob = 1.0
        for b in range(k):
            prob *= p_on[b] if _bit(cs, b) == 1 else (1.0 - p_on[b])
        rep.append(prob)
    return rep

def cause_repertoire(tpm, n, mech_mask, mech_state, purview_mask):
    p_units = _units(purview_mask, n)
    k = len(p_units)
    m_units = _units(mech_mask, n)
    raw = []
    total = 0.0
    for cs in range(_pow2(k)):
        pv_abs = _expand(cs, p_units)
        like = 1.0
        for mu in m_units:
            p1 = marginal_on(tpm, n, purview_mask, pv_abs, mu)
            like *= p1 if _bit(mech_state, mu) == 1 else (1.0 - p1)
        raw.append(like)
        total += like
    nstates = _pow2(k)
    if total > 0.0:
        return [r / total for r in raw]
    return [1.0 / nstates] * nstates

def unconstrained_effect(tpm, n, purview_mask):
    return effect_repertoire(tpm, n, 0, 0, purview_mask)

def unconstrained_cause(purview_mask, n):
    nstates = _pow2(len(_units(purview_mask, n)))
    return [1.0 / nstates] * nstates

def intrinsic_difference(p, q):
    ln2 = math.log(2.0)
    best_val = -1.0e308
    best_state = 0
    for x in range(len(p)):
        px = p[x]
        term = 0.0
        if px > 1.0e-12:
            qx = q[x] + 1.0e-10
            term = px * (math.log(px) - math.log(qx)) / ln2
        if term > best_val:
            best_val = term
            best_state = x
    return [best_val, best_state]

# ── M2: distinctions ───────────────────────────────────────────────────────
def part_effect(tpm, n, mech_state, m1, z1, m2, z2, purview_mask):
    units = _units(purview_mask, n)
    p_on = []
    for u in units:
        if _bit(z1, u) == 1:
            p_on.append(marginal_on(tpm, n, m1, mech_state, u))
        else:
            p_on.append(marginal_on(tpm, n, m2, mech_state, u))
    rep = []
    for cs in range(_pow2(len(units))):
        prob = 1.0
        for b in range(len(units)):
            prob *= p_on[b] if _bit(cs, b) == 1 else (1.0 - p_on[b])
        rep.append(prob)
    return rep

def part_cause_single(tpm, n, mech_state, mp, zp):
    if mp == 0:
        return unconstrained_cause(zp, n)
    return cause_repertoire(tpm, n, mp, mech_state, zp)

def part_cause(tpm, n, mech_state, m1, z1, m2, z2, purview_mask):
    cr1 = part_cause_single(tpm, n, mech_state, m1, z1)
    cr2 = part_cause_single(tpm, n, mech_state, m2, z2)
    zu = _units(purview_mask, n)
    z1u = _units(z1, n)
    z2u = _units(z2, n)
    rep = []
    for cs in range(_pow2(len(zu))):
        pv_abs = _expand(cs, zu)
        rep.append(cr1[_compact_index(pv_abs, z1u)] * cr2[_compact_index(pv_abs, z2u)])
    return rep

def phi_at(p, q, xstar):
    px = p[xstar]
    if px <= 1.0e-12:
        return 0.0
    qx = q[xstar] + 1.0e-10
    phi = px * (math.log(px) - math.log(qx)) / math.log(2.0)
    return phi if phi >= 0.0 else 0.0

def small_phi_effect(tpm, n, mech_mask, mech_state, purview_mask):
    p = effect_repertoire(tpm, n, mech_mask, mech_state, purview_mask)
    unc = unconstrained_effect(tpm, n, purview_mask)
    info = intrinsic_difference(p, unc)
    if info[0] <= 1.0e-12:
        return [0.0, info[1]]
    xstar = int(info[1])
    m_units = _units(mech_mask, n)
    z_units = _units(purview_mask, n)
    min_phi = 1.0e308
    for mi in range(_pow2(len(m_units))):
        m1 = _expand(mi, m_units)
        m2 = mech_mask - m1
        for zi in range(_pow2(len(z_units))):
            z1 = _expand(zi, z_units)
            z2 = purview_mask - z1
            identity = ((m1 == mech_mask) and (z1 == purview_mask)) or ((m1 == 0) and (z1 == 0))
            if not identity:
                q = part_effect(tpm, n, mech_state, m1, z1, m2, z2, purview_mask)
                pt = phi_at(p, q, xstar)
                if pt < min_phi:
                    min_phi = pt
    if min_phi > 1.0e307:
        min_phi = 0.0
    return [min_phi, info[1]]

def small_phi_cause(tpm, n, mech_mask, mech_state, purview_mask):
    p = cause_repertoire(tpm, n, mech_mask, mech_state, purview_mask)
    unc = unconstrained_cause(purview_mask, n)
    info = intrinsic_difference(p, unc)
    if info[0] <= 1.0e-12:
        return [0.0, info[1]]
    xstar = int(info[1])
    m_units = _units(mech_mask, n)
    z_units = _units(purview_mask, n)
    min_phi = 1.0e308
    for mi in range(_pow2(len(m_units))):
        m1 = _expand(mi, m_units)
        m2 = mech_mask - m1
        for zi in range(_pow2(len(z_units))):
            z1 = _expand(zi, z_units)
            z2 = purview_mask - z1
            identity = ((m1 == mech_mask) and (z1 == purview_mask)) or ((m1 == 0) and (z1 == 0))
            if not identity:
                q = part_cause(tpm, n, mech_state, m1, z1, m2, z2, purview_mask)
                pt = phi_at(p, q, xstar)
                if pt < min_phi:
                    min_phi = pt
    if min_phi > 1.0e307:
        min_phi = 0.0
    return [min_phi, info[1]]

def mice_effect(tpm, n, mech_mask, mech_state):
    full = _pow2(n)
    best_phi = -1.0
    best_pv = 0
    best_state = 0.0
    for pv in range(1, full):
        r = small_phi_effect(tpm, n, mech_mask, mech_state, pv)
        if r[0] > best_phi:
            best_phi = r[0]; best_pv = pv; best_state = r[1]
    return [best_phi, float(best_pv), best_state]

def mice_cause(tpm, n, mech_mask, mech_state):
    full = _pow2(n)
    best_phi = -1.0
    best_pv = 0
    best_state = 0.0
    for pv in range(1, full):
        r = small_phi_cause(tpm, n, mech_mask, mech_state, pv)
        if r[0] > best_phi:
            best_phi = r[0]; best_pv = pv; best_state = r[1]
    return [best_phi, float(best_pv), best_state]

def distinction(tpm, n, mech_mask, mech_state):
    ce = mice_cause(tpm, n, mech_mask, mech_state)
    ee = mice_effect(tpm, n, mech_mask, mech_state)
    phi_c, phi_e = ce[0], ee[0]
    phi_d = phi_c if phi_c < phi_e else phi_e
    return [phi_d, float(mech_mask), ce[1], ce[2], ee[1], ee[2], phi_c, phi_e]

# ── M3: relations ──────────────────────────────────────────────────────────
def overlap_congruent(pv_i, state_i, pv_j, state_j, n):
    units_i = _units(pv_i, n)
    units_j = _units(pv_j, n)
    abs_i = _expand(state_i, units_i)
    abs_j = _expand(state_j, units_j)
    overlap = 0
    congruent = 1
    for u in range(n):
        if _bit(pv_i, u) == 1 and _bit(pv_j, u) == 1:
            overlap += 1
            if _bit(abs_i, u) != _bit(abs_j, u):
                congruent = 0
    return 1 if (overlap > 0 and congruent == 1) else 0

def relation_2nd(d_i, d_j, n):
    c = overlap_congruent(int(d_i[2]), int(d_i[3]), int(d_j[2]), int(d_j[3]), n)
    e = overlap_congruent(int(d_i[4]), int(d_i[5]), int(d_j[4]), int(d_j[5]), n)
    if c == 1 or e == 1:
        return d_i[0] if d_i[0] < d_j[0] else d_j[0]
    return 0.0

# ── M4: system big-Φ ───────────────────────────────────────────────────────
def distinction_side(d, a_mask, n):
    mech = int(d[1]); cpv = int(d[2]); epv = int(d[4])
    in_a = 0; in_b = 0
    for u in range(n):
        involved = (_bit(mech, u) == 1) or (_bit(cpv, u) == 1) or (_bit(epv, u) == 1)
        if involved:
            if _bit(a_mask, u) == 1:
                in_a = 1
            else:
                in_b = 1
    if in_a == 1 and in_b == 1:
        return 0
    if in_a == 1:
        return 1
    return 2

def big_phi(tpm, n, sys_state):
    full = _pow2(n)
    dists = []
    sum_d = 0.0
    for m in range(1, full):
        d = distinction(tpm, n, m, sys_state)
        if d[0] > 1.0e-9:
            dists.append(d)
            sum_d += d[0]
    nd = len(dists)
    sum_r = 0.0
    for i in range(nd):
        for j in range(i + 1, nd):
            r = relation_2nd(dists[i], dists[j], n)
            if r > 1.0e-9:
                sum_r += r
    total = sum_d + sum_r
    if n < 2:
        return [0.0, total, sum_d, sum_r, float(nd)]
    all_mask = full - 1
    min_loss = 1.0e308
    for a in range(1, all_mask):
        if _bit(a, 0) == 1:
            sides = []
            surv = 0.0
            for k in range(nd):
                s = distinction_side(dists[k], a, n)
                sides.append(s)
                if s != 0:
                    surv += dists[k][0]
            for ii in range(nd):
                for jj in range(ii + 1, nd):
                    r = relation_2nd(dists[ii], dists[jj], n)
                    if r > 1.0e-9:
                        si, sj = sides[ii], sides[jj]
                        if si != 0 and sj != 0 and si == sj:
                            surv += r
            loss = total - surv
            if loss < min_loss:
                min_loss = loss
    if min_loss > 1.0e307:
        min_loss = 0.0
    if min_loss < 0.0:
        min_loss = 0.0
    return [min_loss, total, sum_d, sum_r, float(nd)]

# ═══════════════════════════════════════════════════════════════════════════
# STEP 0 — PROVE the mirror ≡ stdlib iit4_bigphi.hexa on reference TPMs.
# Reference values from `hexa run UNIVERSE/h1002_bigphi_ref.hexa` on THIS Mac
# (emitted as x1e9 integers; divided back here). See the captured stdlib output
# in .verdicts/1002_bigphi_upgrade/h1002_bigphi_ref_stdlib.txt.
# ═══════════════════════════════════════════════════════════════════════════
def _ring_tpm(n):
    t = []
    for s in range(_pow2(n)):
        for u in range(n):
            t.append(float(_bit(s, (u + 1) % n)))
    return t

def _embedded3():
    t = []
    for s in range(8):
        t += [float(_bit(s, 1)), float(_bit(s, 0)), float(_bit(s, 2))]
    return t

def prove_mirror():
    print("STEP 0 — prove CPU mirror ≡ stdlib iit4_bigphi.hexa (hexa run on this Mac)")
    copy2 = [0.0,0.0, 0.0,1.0, 1.0,0.0, 1.0,1.0]
    self2 = [0.0,0.0, 1.0,0.0, 0.0,1.0, 1.0,1.0]
    bias2 = [0.2,0.3, 0.1,0.8, 0.7,0.2, 0.9,0.85]
    noisyring3 = [0.1,0.1,0.1, 0.15,0.1,0.85, 0.1,0.8,0.12, 0.2,0.82,0.83,
                  0.78,0.12,0.13, 0.82,0.14,0.86, 0.8,0.83,0.12, 0.88,0.85,0.84]
    ring3 = _ring_tpm(3)
    ring4 = _ring_tpm(4)
    # (name, tpm, n, sys_state, hexa_ref_bigphi)  — refs from x1e9 integers / 1e9
    cases = [
        ("copy2_s3",      copy2,      2, 3, 1999999999 / 1e9),
        ("self2_s3",      self2,      2, 3, 0.0),
        ("bias2_s3",      bias2,      2, 3, 1379265832 / 1e9),
        ("embed3_s7",     _embedded3(),3, 7, 0.0),
        ("ring3_s7",      ring3,      3, 7, 2999999999 / 1e9),
        ("ring3_s5",      ring3,      3, 5, 2999999999 / 1e9),
        ("noisyring3_s7", noisyring3, 3, 7, 225488799 / 1e9),
        ("ring4_s15",     ring4,      4, 15, 2999999999 / 1e9),
        ("ring4_s10",     ring4,      4, 10, 2999999999 / 1e9),
    ]
    all_ok = True
    for name, tpm, n, s, ref in cases:
        got = big_phi(tpm, n, s)[0]
        ok = abs(got - ref) < 1e-6
        all_ok = all_ok and ok
        print(f"  {name:14s}: mirror={got:.9f}  hexa_ref={ref:.9f}  "
              f"|Δ|={abs(got-ref):.2e}  {'OK' if ok else 'MISMATCH'}")
    print(f"  MIRROR-FAITHFUL: {'PROVEN (≡ stdlib iit4_bigphi engine)' if all_ok else 'FAILED — DO NOT TRUST'}")
    print()
    if not all_ok:
        raise SystemExit("mirror does not match stdlib iit4_bigphi.hexa — aborting")
    return all_ok

# ═══════════════════════════════════════════════════════════════════════════
# DISCRETIZATION — toy WM latent trajectory → binarized state-by-node TPM (n≤4)
# ═══════════════════════════════════════════════════════════════════════════
N_UNITS = 4   # big-Φ is super-exponential; SMALL n (vs H_999 faithful-Φ n=8)

def latent_to_binary_seq(H, n_units=N_UNITS):
    """(n_steps × latent_dim) → (n_steps × n_units) binary, top-variance channels,
    each binarized at its OWN median over the rollout."""
    H = np.asarray(H, float)
    if H.ndim == 1:
        H = H[None, :]
    n_steps, d = H.shape
    var = H.var(axis=0)
    idx = np.sort(np.argsort(var)[::-1][:n_units])
    chans = H[:, idx]                       # (n_steps × n_units)
    med = np.median(chans, axis=0)
    bits = (chans > med).astype(int)        # ON if above own median
    return bits, n_units

def binary_seq_to_tpm(bits, n):
    """empirical state-by-node TPM: tpm[state*n+unit]=P(unit ON at t+1 | state at t).
    Laplace-smoothed; unseen state row -> uniform 0.5 (max-entropy)."""
    full = _pow2(n)
    on_count = np.zeros((full, n))
    state_count = np.zeros(full)
    T = bits.shape[0]
    for t in range(T - 1):
        st = 0
        for u in range(n):
            if bits[t, u] == 1:
                st += _pow2(u)
        state_count[st] += 1
        for u in range(n):
            if bits[t + 1, u] == 1:
                on_count[st, u] += 1
    tpm = [0.0] * (full * n)
    for s in range(full):
        for u in range(n):
            if state_count[s] > 0:
                # Laplace smoothing (+1 ON, +2 total) keeps probs in (0,1)
                tpm[s * n + u] = (on_count[s, u] + 1.0) / (state_count[s] + 2.0)
            else:
                tpm[s * n + u] = 0.5
    return tpm, state_count

def modal_state(state_count):
    return int(np.argmax(state_count))

def big_phi_of_trajectory(H):
    bits, n = latent_to_binary_seq(H)
    tpm, sc = binary_seq_to_tpm(bits, n)
    s = modal_state(sc)
    return big_phi(tpm, n, s)[0]

# ═══════════════════════════════════════════════════════════════════════════
# CONDITIONS — replicate the EXACT regimes of H_999/H_1001 (= H_971/973/988)
# ═══════════════════════════════════════════════════════════════════════════
IN_DIM = 6
LATENT = 24
N_SEEDS = 30
ROLL = 40

def fit_engine(rng, seed):
    wm = LatentWorldModel(IN_DIM, latent_dim=LATENT, seed=seed, retentive=False,
                          spectral_radius=0.95)
    T = 400
    t = np.arange(T)
    stream = np.stack([np.sin(0.2 * t + k) + 0.3 * rng.standard_normal(T)
                       for k in range(IN_DIM)], axis=1)
    Hs = wm.encode_seq(stream)
    wm.fit_transition(Hs[:-1], Hs[1:])
    return wm

def regimes_for_seed(seed):
    rng = np.random.default_rng(seed)
    wm = fit_engine(rng, seed)
    react_stream = np.stack([np.sin(0.2 * np.arange(ROLL) + k) +
                             0.3 * rng.standard_normal(ROLL) for k in range(IN_DIM)], axis=1)
    H_react = wm.encode_seq(react_stream)
    h0 = H_react[0]
    H_drift = wm.roll_latent(h0, ROLL)
    goal = wm.roll_latent(h0, ROLL)[-1]
    H_guided = _roll_guided(wm, h0, goal, ROLL, pull=0.3)
    return H_react, H_drift, H_guided

def _roll_guided(wm, h0, goal, steps, pull=0.3):
    out = []
    h = h0.copy()
    for _ in range(steps):
        h = (_aug1(h) @ wm.T)
        h = h + pull * (goal - h)
        out.append(h.copy())
    return np.array(out)

def planning_trajectories(seed, depth):
    rng = np.random.default_rng(1000 + seed)
    wm = fit_engine(rng, seed)
    start = np.stack([np.sin(0.2 * np.arange(ROLL) + k) +
                      0.3 * rng.standard_normal(ROLL) for k in range(IN_DIM)], axis=1)
    H0 = wm.encode_seq(start)
    h0 = H0[-1]
    H_greedy = H0
    branches = 4
    delib = []
    for b in range(branches):
        rb = np.random.default_rng(7000 + seed * 13 + b)
        h = h0.copy() + 0.05 * rb.standard_normal(LATENT)
        for _ in range(depth):
            h = wm.roll_latent(h, 1)[0]
            delib.append(h.copy())
    H_plan = np.array(delib) if delib else H_greedy
    return H_greedy, H_plan

# ═══════════════════════════════════════════════════════════════════════════
# MEASURE — big-Φ vs faithful_phi side-by-side (faithful numbers are the FROZEN
# H_999 verdict numbers, reported per-condition for the cross-measure table).
# ═══════════════════════════════════════════════════════════════════════════
# H_999 frozen faithful_phi contrasts (verbatim from H_999 verdict):
FAITHFUL_H999 = {
    "H_971_drift_react":  dict(internal=3.8087, external=2.2994, contrast=+1.5094, d=+2.086, p=7.195e-11),
    "H_988_guided_react": dict(internal=2.1202, external=2.2994, contrast=-0.1792, d=-0.276, p=2.902e-01),
    "H_973_plan_greedy":  dict(internal=7.7459, external=2.6516, contrast=+5.0943, d=+4.637, p=5.138e-21),
    "H_973_rho": +0.483,
}

def contrast_block(name, a, b, label_a, label_b, proxy_a, proxy_b, faithful_key):
    a, b = np.asarray(a, float), np.asarray(b, float)
    con = a.mean() - b.mean()
    d = cohens_d(a, b)
    try:
        t, p = welch_t(a, b)
    except Exception:
        t, p = float("nan"), float("nan")
    lo, hi = boot_ci(a - b) if len(a) == len(b) else (float("nan"), float("nan"))
    f = FAITHFUL_H999[faithful_key]
    print(f"--- {name} ---")
    print(f"  BIG-Φ      {label_a:8s} = {a.mean():.4f} ± {a.std():.4f}")
    print(f"  BIG-Φ      {label_b:8s} = {b.mean():.4f} ± {b.std():.4f}")
    print(f"  BIG-Φ contrast ({label_a}−{label_b}) = {con:+.4f}  "
          f"Cohen d={d:+.3f}  Welch t={t:+.3f} p={p:.3e}  CI=[{lo:+.4f},{hi:+.4f}]")
    print(f"  [faithful_phi, H_999]  {label_a}={f['internal']:.4f}  {label_b}={f['external']:.4f}  "
          f"faithful contrast={f['contrast']:+.4f} d={f['d']:+.3f} p={f['p']:.3e}")
    print(f"  [proxy, original]      {label_a}={proxy_a:.4f}  {label_b}={proxy_b:.4f}  "
          f"proxy contrast={proxy_a - proxy_b:+.4f}")
    return con, d, p

def main():
    print("=" * 78)
    print("H_1002 — big-Φ (system Φ_s) UPGRADE of the H_999/H_1001 imagination/planning Φ-rise")
    print("substrate=CPU-mirror (numpy) — BYTE-FAITHFUL mirror of stdlib")
    print("hexa-lang/stdlib/consciousness/iit4_bigphi.hexa (M4, proven ≡ below)")
    print("g5 CODE-measured (no LLM self-judge, p7) | a_scale_honest_scope: TOY rung n=4")
    print("=" * 78)
    print()
    prove_mirror()

    print(f"DISCRETIZATION: WM latent ({LATENT}-dim, {ROLL} steps) → top-{N_UNITS} variance")
    print(f"channels, binarized at own median → empirical state-by-node TPM (Laplace);")
    print(f"sys_state=modal state; faithful IIT 4.0 system big-Φ over the MIP of the")
    print(f"cause-effect structure (distinctions+relations). n={N_UNITS} (vs H_999 n=8).")
    print(f"Applied IDENTICALLY to every regime so the CONTRAST is fair.\n")

    fphi = {k: [] for k in ("react", "drift", "guided")}
    pphi = {k: [] for k in ("react", "drift", "guided")}
    for s in range(N_SEEDS):
        Hr, Hd, Hg = regimes_for_seed(s)
        fphi["react"].append(big_phi_of_trajectory(Hr))
        fphi["drift"].append(big_phi_of_trajectory(Hd))
        fphi["guided"].append(big_phi_of_trajectory(Hg))
        pphi["react"].append(phi_proxy(Hr)[0])
        pphi["drift"].append(phi_proxy(Hd)[0])
        pphi["guided"].append(phi_proxy(Hg)[0])
    for k in fphi:
        fphi[k] = np.array(fphi[k]); pphi[k] = np.array(pphi[k])

    print("################ H_971 — imagination(DRIFT) vs reaction ################")
    print("# faithful_phi (H_999): +1.5094 d+2.09 → RAISES Φ (PROXY-ARTIFACT reversal)")
    contrast_block("H_971 big-Φ: DRIFT(imagine) − REACT",
                   fphi["drift"], fphi["react"], "DRIFT", "REACT",
                   pphi["drift"].mean(), pphi["react"].mean(), "H_971_drift_react")
    print()
    print("############### H_988 — guided imagination vs reaction ###############")
    print("# faithful_phi (H_999): -0.1792 d-0.28 p0.29 → faithful NULL")
    contrast_block("H_988 big-Φ: GUIDED − REACT",
                   fphi["guided"], fphi["react"], "GUIDED", "REACT",
                   pphi["guided"].mean(), pphi["react"].mean(), "H_988_guided_react")
    print()

    print("################ H_973 — planning(MPC) vs greedy ################")
    print("# faithful_phi (H_999): +5.0943 d+4.64 rho+0.48 → RAISES Φ + positive dose-response")
    depths = [1, 2, 4, 8]
    plan_by_depth = {dpt: [] for dpt in depths}
    greedy_f = []
    plan_proxy_by_depth = {dpt: [] for dpt in depths}
    greedy_proxy = []
    for s in range(N_SEEDS):
        for dpt in depths:
            Hg, Hp = planning_trajectories(s, dpt)
            plan_by_depth[dpt].append(big_phi_of_trajectory(Hp))
            plan_proxy_by_depth[dpt].append(phi_proxy(Hp)[0])
            if dpt == depths[0]:
                greedy_f.append(big_phi_of_trajectory(Hg))
                greedy_proxy.append(phi_proxy(Hg)[0])
    greedy_f = np.array(greedy_f)
    greedy_proxy = np.array(greedy_proxy)
    for dpt in depths:
        plan_by_depth[dpt] = np.array(plan_by_depth[dpt])
        plan_proxy_by_depth[dpt] = np.array(plan_proxy_by_depth[dpt])
    deepest = depths[-1]
    contrast_block(f"H_973 big-Φ: PLAN(depth={deepest}) − GREEDY",
                   plan_by_depth[deepest], greedy_f, "PLAN", "GREEDY",
                   plan_proxy_by_depth[deepest].mean(), greedy_proxy.mean(), "H_973_plan_greedy")
    means = [plan_by_depth[dpt].mean() for dpt in depths]
    flat_depths = np.repeat(depths, N_SEEDS)
    flat_phi = np.concatenate([plan_by_depth[dpt] for dpt in depths])
    rho, prho = spearman(flat_depths, flat_phi)
    print(f"  big-Φ vs plan-depth: depths={depths} means={[f'{m:.4f}' for m in means]}")
    print(f"  dose-response Spearman rho={rho:+.3f} p={prho:.3e}  "
          f"(faithful_phi was rho {FAITHFUL_H999['H_973_rho']:+.2f})")
    print()

    # ── VERDICT ─────────────────────────────────────────────────────────────
    print("=" * 78)
    print("VERDICT MATRIX (big-Φ Φ_s  vs  faithful_phi Φ★  vs  proxy)")
    print("=" * 78)
    c971 = fphi["drift"].mean() - fphi["react"].mean()
    c988 = fphi["guided"].mean() - fphi["react"].mean()
    c973 = plan_by_depth[deepest].mean() - greedy_f.mean()
    d971 = cohens_d(fphi["drift"], fphi["react"])
    d988 = cohens_d(fphi["guided"], fphi["react"])
    d973 = cohens_d(plan_by_depth[deepest], greedy_f)

    def cmp(big_c, big_d, fkey):
        f = FAITHFUL_H999[fkey]
        big_dir = "RAISES" if big_c > 1e-3 else ("LOWERS" if big_c < -1e-3 else "NULL")
        f_dir = "RAISES" if f["contrast"] > 1e-3 else ("LOWERS" if f["contrast"] < -1e-3 else "NULL")
        agree = "AGREE" if big_dir == f_dir else "DISAGREE"
        return big_dir, f_dir, agree

    rows = [
        ("H_971 imagination(DRIFT) vs REACT", c971, d971, "H_971_drift_react"),
        ("H_988 guided imagination vs REACT", c988, d988, "H_988_guided_react"),
        ("H_973 planning(d8) vs GREEDY",      c973, d973, "H_973_plan_greedy"),
    ]
    agreements = []
    for label, bc, bd, fkey in rows:
        bdir, fdir, ag = cmp(bc, bd, fkey)
        agreements.append((label, ag, bdir, fdir, bc, bd))
        f = FAITHFUL_H999[fkey]
        print(f"  {label:36s}: big-Φ={bc:+.4f}(d{bd:+.2f})→{bdir:6s} | "
              f"faithful={f['contrast']:+.4f}(d{f['d']:+.2f})→{fdir:6s} | {ag}")
    print()

    # PASS-condition (frozen in the .md): big-Φ REPLICATES the faithful signs —
    #   imagination(DRIFT) RAISES (d>0.8), planning RAISES (d>0.8) + positive dose-
    #   response, guided NULL → 🟢 BIG-PHI-REPLICATES. Else 🔴/⚠ MEASURE-DEPENDENT.
    drift_raises = (c971 > 1e-3) and (d971 > 0.8)
    plan_raises = (c973 > 1e-3) and (d973 > 0.8)
    plan_dose = rho > 0.0
    guided_null = abs(d988) < 0.8       # not a large effect either way (faithful was null)
    replicates = drift_raises and plan_raises and plan_dose and guided_null

    print("PASS-condition (frozen): big-Φ replicates faithful signs — DRIFT raises (d>0.8),")
    print("  PLAN raises (d>0.8) + positive dose-response, GUIDED null.")
    print(f"  DRIFT raises d>0.8 : {drift_raises} (d={d971:+.2f})")
    print(f"  PLAN  raises d>0.8 : {plan_raises} (d={d973:+.2f})")
    print(f"  PLAN  dose rho>0   : {plan_dose} (rho={rho:+.3f})")
    print(f"  GUIDED null (|d|<0.8): {guided_null} (d={d988:+.2f})")
    print()
    if replicates:
        print("OVERALL: 🟢 BIG-PHI-REPLICATES — the FULL IIT 4.0 system big-Φ (structure-level,")
        print("  distinctions+relations over the MIP) AGREES with the faithful MIP-EI scalar:")
        print("  imagination & planning RAISE big-Φ (planning dose-response positive), guided")
        print("  null. The H_999/H_1001 finding is ROBUST ACROSS IIT4 MEASURES (strongest form).")
    else:
        print("OVERALL: ⚠ MEASURE-DEPENDENT — the system big-Φ does NOT replicate the faithful")
        print("  MIP-EI scalar's signs on all conditions. The Φ-rise was (partly) specific to")
        print("  the chosen measure — an important caveat on H_999/H_1001. See per-row above.")
    print("=" * 78)
    print("HONEST scope (a_scale_honest_scope): TOY single-rung — big-Φ is super-exponential,")
    print(f"so n={N_UNITS} (SMALLER than H_999's n=8 faithful-Φ discretization). The toy WM")
    print("latent is binarized to an n=4 state-by-node TPM; big-Φ is exact at that n but")
    print("scale-transfer is UNVERIFIED. The discretization (continuous→TPM) differs from")
    print("H_999 (continuous→MI); same procedure applied to every regime, contrast is fair.")
    print("Mirror PROVEN ≡ stdlib iit4_bigphi.hexa (|Δ|<1e-6, 9 ref TPMs). NOT a forge binary.")

if __name__ == "__main__":
    main()
