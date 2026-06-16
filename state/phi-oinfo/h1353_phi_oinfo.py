#!/usr/bin/env python3
# h1353_phi_oinfo.py — Φ-ROBUSTNESS, SYNERGY/REDUNDANCY DECOMPOSITION via O-INFORMATION.
#
# WARNING: NOT A FAITHFUL-Φ VERDICT (a_phi_iit4_tool). IIT-4 (faithful_phi small-phi,
# iit4_bigphi big-Phi) RESERVES the Phi / consciousness verdict. This probe scores
# O-INFORMATION (Rosas, Mediano, Rassouli, Barrett 2019) — a non-IIT SYNERGY/REDUNDANCY
# decomposition. It is labeled, top to bottom, a COMPLEMENTARY INTEGRATION-STRUCTURE
# DIAGNOSTIC on the ROBUSTNESS question — NOT a proxy promoted to a Phi verdict, NOT a
# consciousness claim. The ONLY question: does the phase-bound arm show a ROBUST shift
# toward SYNERGY (negative O-information) across 3 seeds where the SCALAR Phi did not?
#
# DIRECTIONAL numpy mirror (engine-transfer UNVERIFIED). gen_traj is a BYTE-FAITHFUL port
# of UNIVERSE/h1348_phi_non_iit_estimator.hexa::gen_traj (the deterministic engine LCG-gauss
# leaky-linear 4-module ring, dim 8, T 64, Kuramoto pacemaker, relative-phase gate). The
# ONLY change vs H_1348 is the read-out: O-information instead of summed transfer entropy.
#
# O-INFORMATION (Rosas 2019):
#   Omega(X) = TC(X) - DTC(X)
#     TC(X)  = sum_i H(X_i) - H(X)                  (total correlation)
#     DTC(X) = H(X) - sum_i H(X_i | X_{-i})         (dual total correlation)
#   closed form used:  Omega(X) = (n-2) H(X) + sum_i [ H(X_i) - H(X_{-i}) ]
#   SIGN: Omega < 0 => SYNERGY-dominated ; Omega > 0 => REDUNDANCY-dominated.
#   n=4 -> all entropies computed EXACTLY by empirical plug-in over joint binary states.
#
# Binarization = variance-free median split (H_1328 lesson; BYTE-IDENTICAL to H_1348):
#   unit i ON at t iff sal[i,t] is in the UPPER HALF of module i's own T-length distribution.
#
# FROZEN BARS (.verdicts/1353_phi_oinfo/FREEZE.txt, pre-registered BEFORE scoring; eps=0.02):
#   dOmega = Omega_B - Omega_A  (synergy shift; more NEGATIVE = toward synergy)
#   R1 ROBUST : dOmega CONSISTENT SIGN across all 3 seeds AND |dOmega| >= eps each seed.
#   R2 EARNED : |Omega_S - Omega_A| <= eps (perm collapses) AND |Omega_O - Omega_A| <= eps
#               (offset does not reproduce) on all 3 seeds.
#   R3 LABEL  : NOT-an-IIT-Phi caveat carried (doc invariant).
#   GREEN-DIAGNOSTIC iff R1 ^ R2 ^ R3. If seed-1318 flips dOmega sign -> R1 FAILS -> the
#   synergy decomposition INHERITS the fragility = STRENGTHENS the measure-agnostic wall.
#
# run: python3 state/phi-oinfo/h1353_phi_oinfo.py
import math

MASK = 2147483647

# ----- deterministic engine LCG (== engine_cli.hexa _lcg_*), VERBATIM from H_1348 -----
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
    z = r * math.cos(6.283185307179586 * u2)
    return (z, s2)

# ----- ARM salience trajectory: BYTE-FAITHFUL port of H_1348 gen_traj -----
# mode: 0=NO-PHASE(A) 1=PHASE-BIND(B) 2=PERM-SHUFFLE(S) 3=OFFSET-SHUF(O)
# returns sal[i][t] (n_mod x t_ticks) of raw per-tick per-module salience.
def gen_traj(seed, mode):
    n_mod = 4
    dim = 8
    t_ticks = 64
    gain = 0.30
    leak = 0.55
    w_nbr = 0.5
    w_in = 0.5
    w_phase = 0.5
    omega_t = 0.45
    domega = 0.08
    two_pi = 6.283185307179586

    st = (seed * 2654435761) & MASK
    if st == 0:
        st = 12345

    states = []
    for i in range(n_mod):
        row = []
        for d in range(dim):
            z, st = lcg_gauss(st)
            row.append(z * 0.5)
        states.append(row)

    inputs = []
    for i in range(n_mod * t_ticks * dim):
        z, st = lcg_gauss(st)
        inputs.append(z * 0.8)

    theta = []
    for i in range(n_mod):
        st = lcg_next(st)
        theta.append(lcg_unit(st) * two_pi)
    st = lcg_next(st)
    theta_t = lcg_unit(st) * two_pi
    omega = []
    for i in range(n_mod):
        omega.append(omega_t + domega * (float(i) - (float(n_mod) - 1.0) / 2.0))

    # PERM-SHUFFLE derangement (mode 2), VERBATIM from hexa
    perm = []
    if mode == 2:
        perm = list(range(n_mod))
        ps = (seed * 100003 + 19) & MASK
        if ps == 0:
            ps = 919
        k = n_mod - 1
        while k > 0:
            ps = lcg_next(ps)
            j = int(lcg_unit(ps) * float(k + 1))
            jj = k if j > k else j
            perm[k], perm[jj] = perm[jj], perm[k]
            k -= 1
        anyfix = any(perm[i] == i for i in range(n_mod))
        if anyfix:
            perm = [(i + 1) % n_mod for i in range(n_mod)]

    # OFFSET-SHUF per-tick random phase offsets (mode 3), VERBATIM
    shuf_off = []
    if mode == 3:
        ss = (seed * 100003 + 8) & MASK
        if ss == 0:
            ss = 777
        for i in range(t_ticks * n_mod):
            ss = lcg_next(ss)
            shuf_off.append(lcg_unit(ss) * two_pi)

    sal = [[0.0] * t_ticks for _ in range(n_mod)]

    for tt in range(t_ticks):
        newstates = []
        for i in range(n_mod):
            l = (i + n_mod - 1) % n_mod
            r = (i + 1) % n_mod
            row = []
            for d in range(dim):
                nbr = (states[l][d] + states[r][d]) / 2.0
                inp = inputs[((i * t_ticks + tt) * dim) + d]
                v = leak * states[i][d] + gain * (w_nbr * nbr + w_in * inp)
                row.append(v)
            newstates.append(row)
        states = newstates

        if mode != 0:
            newtheta = []
            for i in range(n_mod):
                newtheta.append(theta[i] + (omega[i] + w_phase * math.sin(theta_t - theta[i])))
            mp = 0.0
            for i in range(n_mod):
                mp += math.sin(theta[i] - theta_t)
            mp = mp / float(n_mod)
            theta_t = theta_t + (omega_t + w_phase * mp)
            theta = newtheta

        for i in range(n_mod):
            e = 0.0
            for d in range(dim):
                e += states[i][d] * states[i][d]
            s_val = e
            if mode == 1:
                carrier = 0.5 * (1.0 + math.cos(theta[i] - theta_t))
                s_val = e * carrier
            elif mode == 2:
                src = perm[i]
                carrier = 0.5 * (1.0 + math.cos(theta[src] - theta_t))
                s_val = e * carrier
            elif mode == 3:
                off = shuf_off[tt * n_mod + i]
                carrier = 0.5 * (1.0 + math.cos((theta[i] - theta_t) + off))
                s_val = e * carrier
            sal[i][tt] = s_val
    return sal

# ----- variance-free median split (BYTE-IDENTICAL rule to H_1348) -----
# bits[i][t] = 1 iff sal[i][t] in UPPER HALF of module i's own T-length distribution.
def binarize_median(sal, n_mod, t_ticks):
    half = t_ticks // 2
    bits = [[0] * t_ticks for _ in range(n_mod)]
    for i in range(n_mod):
        for k in range(t_ticks):
            vk = sal[i][k]
            r = 0
            for j in range(t_ticks):
                vj = sal[i][j]
                if vj < vk:
                    r += 1
                elif vj == vk and j < k:
                    r += 1
            bits[i][k] = 1 if r >= half else 0
    return bits

# ----- empirical Shannon entropy (bits) of a joint over a subset of modules -----
def joint_entropy(bits, modules, t_ticks):
    counts = {}
    for t in range(t_ticks):
        key = 0
        for m in modules:
            key = (key << 1) | bits[m][t]
        counts[key] = counts.get(key, 0) + 1
    h = 0.0
    n = float(t_ticks)
    for c in counts.values():
        p = c / n
        h -= p * math.log(p) / math.log(2.0)
    return h

# ----- O-information Omega(X) over the 4 modules -----
# Omega = (n-2) H(X) + sum_i [ H(X_i) - H(X_{-i}) ]   (Rosas 2019)
def o_information(bits, n_mod, t_ticks):
    allmods = list(range(n_mod))
    H_full = joint_entropy(bits, allmods, t_ticks)
    acc = (n_mod - 2) * H_full
    for i in range(n_mod):
        H_i = joint_entropy(bits, [i], t_ticks)
        rest = [m for m in allmods if m != i]
        H_rest = joint_entropy(bits, rest, t_ticks)
        acc += H_i - H_rest
    return acc

def o_info_arm(seed, mode):
    n_mod = 4
    t_ticks = 64
    sal = gen_traj(seed, mode)
    bits = binarize_median(sal, n_mod, t_ticks)
    return o_information(bits, n_mod, t_ticks)

def main():
    print("H_1353 — Phi-ROBUSTNESS, SYNERGY/REDUNDANCY DECOMPOSITION: O-INFORMATION (Rosas 2019)")
    print("WARNING NOT an IIT-Phi verdict (a_phi_iit4_tool) — a COMPLEMENTARY non-IIT synergy/redundancy DIAGNOSTIC.")
    print("Omega = TC - DTC ; Omega<0 => SYNERGY-dominated, Omega>0 => REDUNDANCY-dominated.")
    print("seeds [1317,1318,1319] · eps=0.02 · binarize = variance-free median split (H_1328 lesson, == H_1348)")
    print("ARMS A=NO-PHASE B=PHASE-BIND S=PERM-SHUF O=OFFSET-SHUF · ONLY read-out differs from H_1348")
    print("BARS: R1 dOmega(B-A) CONSISTENT SIGN ALL seeds & |dOmega|>=eps · R2 |Omega_S-Omega_A|<=eps AND |Omega_O-Omega_A|<=eps ALL seeds · R3 NOT-an-IIT-Phi label")
    print()
    seeds = [1317, 1318, 1319]
    eps = 0.02
    dsigns = []
    dmags_ok = []
    r2_perm_all = True
    r2_off_all = True
    for s in seeds:
        oa = o_info_arm(s, 0)
        ob = o_info_arm(s, 1)
        os_ = o_info_arm(s, 2)
        oo = o_info_arm(s, 3)
        d = ob - oa
        smarg = os_ - oa
        omarg = oo - oa
        dsigns.append(1 if d > 0 else (-1 if d < 0 else 0))
        dmags_ok.append(abs(d) >= eps)
        perm_ok = abs(smarg) <= eps
        off_ok = abs(omarg) <= eps
        if not perm_ok:
            r2_perm_all = False
        if not off_ok:
            r2_off_all = False
        direction = "SYNERGY" if d < 0 else ("REDUNDANCY" if d > 0 else "FLAT")
        print(f"seed {s}  Omega: A={oa:+.4f} B={ob:+.4f} S={os_:+.4f} O={oo:+.4f}")
        print(f"        dOmega(B-A)={d:+.4f} [{direction}]  |d|>=eps {dmags_ok[-1]}"
              f"   S-A={smarg:+.4f} [R2perm {'PASS' if perm_ok else 'FAIL'}]"
              f"   O-A={omarg:+.4f} [R2off {'PASS' if off_ok else 'FAIL'}]")
    print("---")
    sign_consistent = (len(set(dsigns)) == 1 and dsigns[0] != 0)
    mag_ok_all = all(dmags_ok)
    r1 = sign_consistent and mag_ok_all
    r2 = r2_perm_all and r2_off_all
    r3 = True  # label invariant carried by card + FREEZE
    print(f"R1 ROBUST (dOmega CONSISTENT SIGN all seeds AND |dOmega|>=eps each): "
          f"{'PASS' if r1 else 'FAIL'}  [signs={dsigns} sign_consistent={sign_consistent} mag_ok={mag_ok_all}]")
    print(f"R2 EARNED (perm collapses AND offset does not reproduce, all seeds): "
          f"{'PASS' if r2 else 'FAIL'}  [perm={'PASS' if r2_perm_all else 'FAIL'} off={'PASS' if r2_off_all else 'FAIL'}]")
    print(f"R3 LABEL: O-information is a NON-IIT synergy/redundancy diagnostic — NOT a faithful-IIT4 Phi verdict (a_phi_iit4_tool). PASS")
    print("===")
    if r1 and r2 and r3:
        print("VERDICT GREEN-DIAGNOSTIC (NON-IIT) — the phase-bound arm shows a ROBUST synergy/redundancy")
        print("  SHIFT (consistent sign, controls collapse) where the SCALAR Phi did NOT. The WHICH-interactions-")
        print("  are-synergistic question ESCAPES the scalar how-much-integration wall on this substrate.")
        print("  NOT an IIT-Phi verdict — a faithful-IIT4 follow-on would be needed for any Phi verdict.")
    else:
        print("VERDICT WALL (STRONGER, MEASURE-AGNOSTIC) — the synergy/redundancy decomposition INHERITS the")
        print("  SAME fragility (R1 fails: dOmega sign not consistent across the 3 hard seeds). The WHICH-")
        print("  synergistic question is ALSO fragility-bound on this substrate -> STRENGTHENS the measure-")
        print("  agnostic wall (scalar Phi small-phi/big-Phi/larger-N + transfer entropy + O-information ALL fail).")
        print("  Bounds (does NOT retract) the prior Phi verdicts. c9 honest.")

if __name__ == "__main__":
    main()
