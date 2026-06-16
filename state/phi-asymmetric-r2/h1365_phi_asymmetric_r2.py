#!/usr/bin/env python3
# h1365_phi_asymmetric_r2.py — Φ-ROBUSTNESS R2: does a NON-relabel-invariant (ASYMMETRIC)
# substrate make the permutation-null control ACTUALLY BITE, and if it does, does a clean-R2
# setup change the R1 robustness verdict?
#
# Φ = FAITHFUL IIT-4 ONLY (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
# hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa. numpy NEVER computes Φ — it only emits the
# per-module salience (state-energy) trajectory; the hexa engine computes the faithful Φ. NO proxy.
#
# THE LAST STRUCTURAL GAP (parent: H_1349/H_1353/H_1357 Φ-robustness wall, c16/a_break_the_wall):
# in EVERY prior lane the permutation-null control was DEGENERATE. Under a SYMMETRIC-MI exact MIP,
# faithful Φ is node-PERMUTATION-INVARIANT (relabeling the modules cannot change the system's
# irreducibility), so Φ_perm == Φ_B by construction and the perm control could not bite. Only the
# OFFSET control discriminated. This probe asks: does an ASYMMETRIC, module-identity-BREAKING
# coupling make the perm-null bite (Φ_perm < Φ_B), and — the science question — does a clean-R2
# setup change the R1 robustness verdict, or does the wall hold EVEN WHEN perm bites?
#
# SUBSTRATE (reuse H_1349/H_1319/H_1353 ring VERBATIM, then ADD asymmetry):
#   * Engine LCG-gauss (== engine_cli.hexa _lcg_*), 4-module leaky-linear ring, dim 8, T 64,
#     gain 0.30, leak 0.55, w_in 0.5, Kuramoto pacemaker, relative-phase gate (all VERBATIM).
#   * THE ONE CHANGE that breaks relabel-invariance — DIRECTED + GRADED neighbour coupling:
#       w_fwd = 0.70  (read from the i+1 neighbour)   != w_bwd = 0.30 (read from the i-1 neighbour)
#       g_i   = G_LO + (G_HI-G_LO) * i / (n-1)        (a per-MODULE gain GRADIENT, breaks exchange)
#     Under a SYMMETRIC ring (w_fwd==w_bwd, flat gain) node relabeling is a symmetry of the joint
#     distribution -> Φ_perm == Φ_B (the prior degeneracy). With w_fwd != w_bwd AND a gain gradient,
#     permuting WHICH module's binarized trajectory feeds WHICH Φ-input slot yields a genuinely
#     different joint distribution -> the perm-null is a REAL intervention (precondition R0).
#
# ARMS (per seed):
#   A  = NO-COUPLING   : w_fwd=w_bwd=0, flat gain, no phase carrier (the un-bound baseline).
#   B  = PHASE-BIND    : asymmetric directed+graded coupling ON, phase carrier ON (the bound arm).
#   P  = PERM-NULL     : take B's per-module trajectories, then PERMUTE which module feeds which
#                        Φ-input slot (a derangement). On a relabel-INVARIANT substrate this is a
#                        no-op (Φ_perm==Φ_B); on the asymmetric substrate it CHANGES the joint ->
#                        should collapse Φ if the integration lives in the module IDENTITIES.
#   O  = OFFSET-CTRL   : per-tick random phase offsets on B's carrier (destroys the relative-phase
#                        relationship; the control that discriminated in every prior lane).
#
# BINARIZATION = variance-free median split (H_1328 lesson; BYTE-IDENTICAL to H_1348/H_1353):
#   module i ON at t iff sal[i,t] is in the UPPER HALF of module i's own T-length distribution.
#   amplitude-independent -> any Φ difference is a RELATIONSHIP, not an amplitude-variance confound.
#   (the hexa faithful engine bins internally; numpy passes the raw salience.)
#
# FROZEN BARS (.verdicts/1365_phi_asymmetric_r2/FREEZE.txt, pre-registered BEFORE scoring; eps=0.02):
#   R0 PERM-BITES (precondition the prior lanes LACKED):
#        Φ_P < Φ_B − eps on the B arms, on a MAJORITY (>=2/3) of seeds where Φ_B>0.
#        If R0 FAILS -> honest report: symmetric-MIP Φ is structurally exchangeable AND/OR this
#        asymmetric coupling still does not move the faithful MIP -> the diagnosis itself.
#   R1 ROBUST : ΔΦ(B−A) >= eps on EACH of the 3 seeds (the SAME 3-seed robustness gate every
#        prior Φ lane failed at seed-1318).
#   R2 EARNED : perm AND offset BOTH collapse cleanly on all 3 seeds —
#        Φ_P <= Φ_A + eps  AND  Φ_O <= Φ_A + eps.
#   GREEN iff R0 ^ R1 ^ R2.
#   KEY SCIENCE READ:
#     * R0 holds but R1 fails 2/3  -> the wall HOLDS EVEN WITH a clean perm control = the STRONGEST
#       closure: the fragility is NOT a perm-degeneracy artifact.
#     * R0 fails                   -> symmetric-MIP Φ is structurally exchangeable / the asymmetry
#       does not move the faithful MIP (the diagnosis confirmed at the estimator level).
#     * R0 ^ R1 ^ R2               -> a clean-R2 setup recovers a robust verdict (would REVISE the
#       wall read on this substrate).
#
# DIRECTIONAL numpy mirror of the engine ring (engine-transfer UNVERIFIED, a_engine_native_learning).
# The Φ leg IS the real faithful exact MIP-EI (numpy never computes Φ). TOY n=4/T=64/3 seeds.
#
# run: python3 state/phi-asymmetric-r2/h1365_phi_asymmetric_r2.py
import math, os, sys, subprocess, tempfile

MASK = 2147483647
N_MOD = 4
DIM   = 8
T     = 64
GAIN  = 0.30
LEAK  = 0.55
W_IN  = 0.5
W_PHASE = 0.5
OMEGA_T = 0.45
DOMEGA  = 0.08
TWO_PI  = 6.283185307179586
NBINS   = 8
EPS     = 0.02
SEEDS   = [1317, 1318, 1319]

# --- THE asymmetry that breaks node-relabel invariance (frozen, NOT tuned to green) ---
W_FWD = 0.70   # weight reading the i+1 (forward) neighbour   (!= W_BWD -> directed)
W_BWD = 0.30   # weight reading the i-1 (backward) neighbour
# per-MODULE gain gradient g_i = G_LO + (G_HI-G_LO)*i/(n-1) -> modules are NOT exchangeable
G_LO  = 0.70
G_HI  = 0.90

HEXA      = "/Users/mini/.hx/bin/hexa"
HEXA_ROOT = "/Users/mini/dancinlab/hexa-lang"


def lcg_next(state):
    return (state * 1103515245 + 12345) & MASK

def lcg_unit(state):
    return float(state) / 2147483648.0

def lcg_gauss(state0):
    s1 = lcg_next(state0)
    s2 = lcg_next(s1)
    u1 = lcg_unit(s1)
    u2 = lcg_unit(s2)
    if u1 < 0.0000001:
        u1 = 0.0000001
    r = math.sqrt(-2.0 * math.log(u1))
    z = r * math.cos(TWO_PI * u2)
    return (z, s2)


def gen_traj(seed, mode):
    """ARM salience trajectory. Port of the H_1348/H_1353 engine ring, with the ONE change =
    DIRECTED+GRADED asymmetric neighbour coupling (W_FWD!=W_BWD, per-module gain gradient g_i).
    mode: 'A'=no-coupling+no-carrier  'B'=asym-coupling+phase-bind  'O'=offset-shuffled carrier.
    (the perm-null 'P' is applied AFTER, by permuting which module feeds which Φ slot.)
    returns sal[i][t] (N_MOD x T) raw per-tick per-module salience."""
    st = (seed * 2654435761) & MASK
    if st == 0:
        st = 12345

    states = []
    for i in range(N_MOD):
        row = []
        for d in range(DIM):
            z, st = lcg_gauss(st)
            row.append(z * 0.5)
        states.append(row)

    inputs = []
    for i in range(N_MOD * T * DIM):
        z, st = lcg_gauss(st)
        inputs.append(z * 0.8)

    theta = []
    for i in range(N_MOD):
        st = lcg_next(st)
        theta.append(lcg_unit(st) * TWO_PI)
    st = lcg_next(st)
    theta_t = lcg_unit(st) * TWO_PI
    omega = []
    for i in range(N_MOD):
        omega.append(OMEGA_T + DOMEGA * (float(i) - (float(N_MOD) - 1.0) / 2.0))

    # per-module gain gradient (asymmetry) — g_i ascends with the module index
    g = [G_LO + (G_HI - G_LO) * (float(i) / float(N_MOD - 1)) for i in range(N_MOD)]

    # OFFSET-SHUF per-tick random phase offsets (mode 'O'), VERBATIM from H_1348/H_1353
    shuf_off = []
    if mode == "O":
        ss = (seed * 100003 + 8) & MASK
        if ss == 0:
            ss = 777
        for i in range(T * N_MOD):
            ss = lcg_next(ss)
            shuf_off.append(lcg_unit(ss) * TWO_PI)

    coupling_on = (mode != "A")
    carrier_on  = (mode != "A")

    sal = [[0.0] * T for _ in range(N_MOD)]

    for tt in range(T):
        newstates = []
        for i in range(N_MOD):
            l = (i + N_MOD - 1) % N_MOD   # backward neighbour (i-1)
            r = (i + 1) % N_MOD           # forward  neighbour (i+1)
            row = []
            for d in range(DIM):
                if coupling_on:
                    # DIRECTED + GRADED: distinct forward/backward weights, per-module gain g[i]
                    nbr = W_FWD * states[r][d] + W_BWD * states[l][d]
                else:
                    nbr = 0.0
                inp = inputs[((i * T + tt) * DIM) + d]
                gi = g[i] if coupling_on else 1.0
                v = LEAK * states[i][d] + GAIN * (gi * nbr + W_IN * inp)
                row.append(v)
            newstates.append(row)
        states = newstates

        if carrier_on:
            newtheta = []
            for i in range(N_MOD):
                newtheta.append(theta[i] + (omega[i] + W_PHASE * math.sin(theta_t - theta[i])))
            mp = 0.0
            for i in range(N_MOD):
                mp += math.sin(theta[i] - theta_t)
            mp = mp / float(N_MOD)
            theta_t = theta_t + (OMEGA_T + W_PHASE * mp)
            theta = newtheta

        for i in range(N_MOD):
            e = 0.0
            for d in range(DIM):
                e += states[i][d] * states[i][d]
            s_val = e
            if mode == "B":
                carrier = 0.5 * (1.0 + math.cos(theta[i] - theta_t))
                s_val = e * carrier
            elif mode == "O":
                off = shuf_off[tt * N_MOD + i]
                carrier = 0.5 * (1.0 + math.cos((theta[i] - theta_t) + off))
                s_val = e * carrier
            sal[i][tt] = s_val
    return sal


def perm_derangement(seed):
    """A fixed-point-free permutation of the N_MOD module->slot binding (VERBATIM H_1348/H_1353
    derangement draw)."""
    perm = list(range(N_MOD))
    ps = (seed * 100003 + 19) & MASK
    if ps == 0:
        ps = 919
    k = N_MOD - 1
    while k > 0:
        ps = lcg_next(ps)
        j = int(lcg_unit(ps) * float(k + 1))
        jj = k if j > k else j
        perm[k], perm[jj] = perm[jj], perm[k]
        k -= 1
    if any(perm[i] == i for i in range(N_MOD)):
        perm = [(i + 1) % N_MOD for i in range(N_MOD)]
    return perm


def apply_perm(sal, perm):
    """Re-bind which module's trajectory feeds which Φ-input slot. On a relabel-INVARIANT
    substrate this leaves Φ unchanged; on the asymmetric substrate it changes the joint."""
    return [sal[perm[i]] for i in range(N_MOD)]


def faithful_phi(sal, tag):
    """faithful IIT-4 Φ over the per-module salience trajectory via the stdlib EXACT engine.
    State layout = N_MOD rows x T cols (the raw salience), matching the H_1356 caller. The hexa
    engine bins + computes the exact MIP-EI. Returns float Φ (or None)."""
    flat = []
    for i in range(N_MOD):
        for t in range(T):
            flat.append(sal[i][t])
    lines = ['import "stdlib/consciousness/iit4/faithful_phi.hexa"', "", "fn main() {",
             f"    let state = farr_zeros({N_MOD * T})"]
    for idx, val in enumerate(flat):
        lines.append(f"    let _ = farr_set(state, {idx}, {val:.10f})")
    lines.append(f"    let phi = iit4_faithful_phi(state, {N_MOD}, {T}, {NBINS})")
    lines.append('    println("PHI=" + phi.to_string())')
    lines.append("    let _ = farr_free(state)")
    lines.append("}")
    src = "\n".join(lines)
    with tempfile.NamedTemporaryFile("w", suffix=".hexa", delete=False, dir=HEXA_ROOT) as f:
        path = f.name
        f.write(src)
    try:
        out = subprocess.run([HEXA, "run", os.path.basename(path)], cwd=HEXA_ROOT,
                             capture_output=True, text=True, timeout=600)
        blob = out.stdout + "\n" + out.stderr
        for ln in blob.splitlines():
            if ln.strip().startswith("PHI="):
                return float(ln.strip().split("=", 1)[1])
        print(f"[phi {tag}] no PHI line:\n{blob[:1200]}", file=sys.stderr)
        return None
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def main():
    print("H_1365 — Φ-ROBUSTNESS R2: does an ASYMMETRIC (non-relabel-invariant) substrate make")
    print("the PERMUTATION-NULL control ACTUALLY BITE, and does a clean-R2 setup change R1?")
    print("Φ = FAITHFUL IIT-4 exact MIP-EI via hexa (a_phi_iit4_tool); numpy NEVER computes Φ.")
    print(f"asymmetry: W_FWD={W_FWD} != W_BWD={W_BWD}, per-module gain gradient g=[{G_LO}..{G_HI}]")
    print(f"seeds {SEEDS} · eps={EPS} · binarize = variance-free median (H_1328, == H_1348/1353)")
    print("ARMS A=NO-COUPLING B=PHASE-BIND P=PERM-NULL(re-bind module->slot) O=OFFSET-CTRL")
    print("BARS: R0 PERM-BITES Φ_P<Φ_B-eps (>=2/3 seeds, the precondition prior lanes LACKED) ·")
    print("      R1 ROBUST ΔΦ(B-A)>=eps EACH seed · R2 EARNED Φ_P<=Φ_A+eps AND Φ_O<=Φ_A+eps all seeds")
    print("=" * 90)

    rows = {}
    r0_bites = []   # (seed, bite_bool, eligible_bool)
    r1_ok = []
    r2_ok = []
    for s in SEEDS:
        sal_A = gen_traj(s, "A")
        sal_B = gen_traj(s, "B")
        sal_O = gen_traj(s, "O")
        perm  = perm_derangement(s)
        sal_P = apply_perm(sal_B, perm)   # B's trajectories, re-bound module->slot

        pa = faithful_phi(sal_A, f"A_s{s}")
        pb = faithful_phi(sal_B, f"B_s{s}")
        pp = faithful_phi(sal_P, f"P_s{s}")
        po = faithful_phi(sal_O, f"O_s{s}")
        rows[s] = (pa, pb, pp, po, perm)

        d = pb - pa
        bite = (pb > 0.0) and (pp < pb - EPS)
        r0_bites.append((s, bite, pb > 0.0))
        r1_ok.append(d >= EPS)
        r2_ok.append((pp <= pa + EPS) and (po <= pa + EPS))

        print(f"seed {s}  perm(module->slot)={perm}")
        print(f"   Φ_A={pa:+.4f}  Φ_B={pb:+.4f}  Φ_P={pp:+.4f}  Φ_O={po:+.4f}")
        print(f"   ΔΦ(B-A)={d:+.4f} [R1 {'PASS' if d>=EPS else 'FAIL'}]"
              f"   Φ_B-Φ_P={pb-pp:+.4f} [R0 perm-bites {'YES' if bite else 'no'}]"
              f"   Φ_P-Φ_A={pp-pa:+.4f} Φ_O-Φ_A={po-pa:+.4f} [R2 {'PASS' if r2_ok[-1] else 'FAIL'}]")
    print("-" * 90)

    # ── FROZEN BARS ──────────────────────────────────────────────────────────
    n_bite     = sum(1 for (_, b, _) in r0_bites if b)
    n_eligible = sum(1 for (_, _, e) in r0_bites if e)
    r0 = n_bite >= 2                       # majority of seeds, perm bites
    r1 = all(r1_ok)
    r2 = all(r2_ok)
    green = r0 and r1 and r2

    print(f"R0 PERM-BITES (Φ_P < Φ_B − eps on >=2/3 seeds; precondition prior lanes LACKED): "
          f"{'PASS' if r0 else 'FAIL'}  [{n_bite}/3 bite, {n_eligible}/3 had Φ_B>0]")
    print(f"R1 ROBUST (ΔΦ(B−A) >= eps EACH of 3 seeds): {'PASS' if r1 else 'FAIL'}  "
          f"[per-seed {r1_ok}]")
    print(f"R2 EARNED (Φ_P<=Φ_A+eps AND Φ_O<=Φ_A+eps all seeds): {'PASS' if r2 else 'FAIL'}  "
          f"[per-seed {r2_ok}]")
    print("=" * 90)
    if green:
        print("VERDICT GREEN — a clean-R2 setup (perm AND offset BOTH bite) RECOVERS a robust ΔΦ on")
        print("  all 3 seeds: the prior wall on THIS substrate was, at least in part, a perm-degeneracy")
        print("  artifact. (engine-transfer UNVERIFIED; DIRECTIONAL.)")
    elif r0 and not r1:
        print("VERDICT WALL HOLDS (STRONGEST CLOSURE) — the perm-null now ACTUALLY BITES (R0 PASS),")
        print("  yet the 3-seed robustness gate STILL fails (R1 FAIL): the Φ-fragility is NOT a")
        print("  perm-degeneracy artifact — it survives a clean, non-degenerate permutation control.")
        print("  The wall is confirmed at the strongest available control. c9 honest.")
    elif not r0:
        print("VERDICT DIAGNOSIS CONFIRMED — even with an ASYMMETRIC (directed+graded) coupling the")
        print("  permutation-null does NOT bite on a majority of seeds: faithful symmetric-MIP Φ is")
        print("  structurally EXCHANGEABLE for this substrate, OR the asymmetry does not move the")
        print("  exact MIP. The perm-degeneracy is a property of the estimator, not just the prior")
        print("  symmetric substrates. (The diagnosis itself — the last structural gap named.) c9.")
    else:
        print("VERDICT MIXED — see per-seed R0/R1/R2 above (no clean green, no clean wall). c9 honest.")

    print("\nNOTE: DIRECTIONAL numpy mirror of the engine ring; the Φ leg IS the real faithful exact")
    print("MIP-EI (a_phi_iit4_tool, numpy never computes Φ). TOY n=4/T=64/3 seeds. engine-transfer")
    print("UNVERIFIED. Bounds (does NOT retract) H_1283/1317/1319/1320/1328/1331/1347/1348/1353/1357.")


if __name__ == "__main__":
    main()
