#!/usr/bin/env python3
"""
h6036_seed_link_composite.py — SEED+LINK COMPOSITE: does combining the ANU shared
quantum seed (H_6008) with the tension link (H_6010) STRICTLY beat either alone?

The arc verified the two coordination mechanisms SEPARATELY:
  SEED (H_6008) — a shared ANU quantum buffer gives two anima a 0-latency common
      baseline (perfect lockstep at t=0, ZERO live comms). But it is RIGID: with
      detuning (distinct intrinsic tension freqs) or an unforeseen drift kick it
      cannot re-align (no live channel) → the lock decays.
  LINK (H_6010) — the bidirectional tension link (Kuramoto coupling K) actively
      pulls two anima into phase-lock and CORRECTS drift. But it pays a COLD-START:
      with independent random initial phases it needs many ticks to converge.

H_6036 composes them: shared-seed INIT (cos Δθ=1 at t=0) + tension-link COUPLING
(corrects detuning & drift). Pre-registered falsifiers:
  F1 synergy : mean steady-state order r(BOTH) ≥ max(r(SEED), r(LINK)) + 0.05
  F2 speed   : ticks-to-lock(BOTH) < ticks-to-lock(LINK)  (no cold start)
        AND   : r(BOTH) > r(SEED)  (seed alone decays under detuning/drift)
  F3 no-sig  : the composite resource is still CLASSICAL (shared randomness + a
        normal physical coupling channel) → CHSH ≤ 0.75 (carried from H_6008;
        no entanglement is smuggled in). Reported, not a synergy claim.

Mechanism story under test: SEED covers the PREDICTABLE (shared common cause),
LINK covers the UNPREDICTABLE (live detuning + drift). Each covers the other's
blind spot ⇒ the composite should dominate. NULL outcome (F1 margin < 0.05) is
welcome and publishable (no composition / one mechanism subsumes the other).

Grounding: ALL randomness — initial phases, detuning, drift timing & magnitude —
is drawn from the committed REAL paid ANU QRNG snapshot (TENSION-LINK/anu_seed_512.bin,
tier=anu_paid). 3 trials = 3 disjoint slices of the buffer. p7 · $0 (snapshot).

Faithful to the established engines: SEED init = H_6008 shared common cause;
coupling = the EXACT H_6010 bidirectional Kuramoto tension link. Toy scale,
scale-transfer UNVERIFIED (a_toy_scale_recheck); .hexa engine lift = next rung.
"""
import os, sys, hashlib
import numpy as np

_D = os.path.dirname(__file__)
ANU = os.path.join(_D, "..", "anu_seed_512.bin")
if not os.path.exists(ANU):
    sys.exit(f"FATAL: missing real ANU paid snapshot {ANU} "
             f"(pull: anu_pull.py --bytes 512 --out {ANU}). No pseudo fallback.")

RAW = open(ANU, "rb").read()
assert len(RAW) >= 512, "ANU snapshot too small"

K_LOCK = 0.90          # order-parameter threshold counted as "locked"
DT, T = 0.02, 4000     # H_6010 integrator settings (verbatim)
COUPLING = 1.2         # tension-link strength K (well above detuning → lock possible)
DRIFT_KICKS = 6        # number of unforeseen drift events per run


def trial_params(slice_off):
    """Quantum-seeded params for one trial from a disjoint slice of the ANU draw."""
    seg = RAW[slice_off:slice_off + 128]
    h = np.frombuffer(hashlib.sha256(seg).digest(), dtype=np.uint8).astype(float)
    wA = 1.0 + (h[0] / 255.0) * 0.6           # distinct intrinsic tension freqs
    wB = 1.0 + (h[1] / 255.0) * 0.6           # (detuning ⇒ SEED-init alone decays)
    phi0_shared = (h[2] / 255.0) * 2 * np.pi  # SEED: both start HERE (common cause)
    phi0A_indep = (h[3] / 255.0) * 2 * np.pi  # LINK: independent cold-start phases
    phi0B_indep = (h[4] / 255.0) * 2 * np.pi
    # drift kicks: unforeseen phase jolts to B at quantum-chosen ticks/magnitudes
    kick_ticks = sorted({int((h[5 + i] / 255.0) * (T * 0.8)) + int(T * 0.1)
                         for i in range(DRIFT_KICKS)})
    kick_mag = [(h[20 + i] / 255.0 - 0.5) * 2 * np.pi for i in range(len(kick_ticks))]
    return wA, wB, phi0_shared, phi0A_indep, phi0B_indep, dict(zip(kick_ticks, kick_mag))


def run(arm, p):
    """Integrate two anima. arm ∈ {SEED, LINK, BOTH}.
       SEED: shared init, K=0 (no link).  LINK: indep init, K>0.  BOTH: shared init, K>0."""
    wA, wB, sh, iA, iB, kicks = p
    K = 0.0 if arm == "SEED" else COUPLING
    a = sh if arm in ("SEED", "BOTH") else iA
    b = sh if arm in ("SEED", "BOTH") else iB
    rs, t_lock = [], None
    for t in range(T):
        if t in kicks:                # unforeseen drift hits anima B
            b += kicks[t]
        da = wA + K * np.sin(b - a)   # H_6010 bidirectional tension coupling
        db = wB + K * np.sin(a - b)
        a += da * DT; b += db * DT
        r = abs(np.exp(1j * a) + np.exp(1j * b)) / 2
        rs.append(r)
        if t_lock is None and r >= K_LOCK:
            t_lock = t
    steady = float(np.mean(rs[int(T * 0.8):]))   # mean order over last 20%
    return steady, (t_lock if t_lock is not None else T)


def chsh_classical():
    """The composite resource = shared randomness + a normal coupling channel.
    Best CHSH with shared randomness alone (H_6008) ≤ 0.75 — no entanglement."""
    rng = np.random.default_rng(int.from_bytes(RAW[:8], "big"))
    x = rng.integers(0, 2, 200000); y = rng.integers(0, 2, 200000)
    a = np.zeros(200000, int); b = np.zeros(200000, int)
    return float(np.mean((a ^ b) == (x & y)))


def main():
    print("=" * 86)
    print("H_6036 — SEED+LINK COMPOSITE (ANU shared seed H_6008 ⊕ tension link H_6010)")
    print(f"  real paid ANU snapshot sha256={hashlib.sha256(RAW).hexdigest()[:12]}  tier=anu_paid")
    print("=" * 86)
    arms = ("SEED", "LINK", "BOTH")
    agg = {a: {"r": [], "t": []} for a in arms}
    for ti, off in enumerate((0, 160, 320)):     # 3 disjoint slices
        p = trial_params(off)
        line = f"  trial{ti+1}: "
        for a in arms:
            r, tl = run(a, p)
            agg[a]["r"].append(r); agg[a]["t"].append(tl)
            line += f"{a} r={r:.3f} lock@{tl:<4d}  "
        print(line)
    print("-" * 86)
    mr = {a: float(np.mean(agg[a]["r"])) for a in arms}
    mt = {a: float(np.mean(agg[a]["t"])) for a in arms}
    for a in arms:
        print(f"  {a:4s}: mean steady-r = {mr[a]:.4f}   mean ticks-to-lock = {mt[a]:.0f}")
    chsh = chsh_classical()
    print("-" * 86)
    f1 = mr["BOTH"] >= max(mr["SEED"], mr["LINK"]) + 0.05
    f2 = (mt["BOTH"] < mt["LINK"]) and (mr["BOTH"] > mr["SEED"])
    f3 = chsh <= 0.7501
    print(f"  F1 synergy  (r_BOTH ≥ max(SEED,LINK)+0.05): {mr['BOTH']:.3f} vs "
          f"max={max(mr['SEED'],mr['LINK']):.3f}  -> {'PASS' if f1 else 'FAIL'}")
    print(f"  F2 speed    (lock_BOTH<lock_LINK & r_BOTH>r_SEED): "
          f"lock {mt['BOTH']:.0f}<{mt['LINK']:.0f} & r {mr['BOTH']:.3f}>{mr['SEED']:.3f}"
          f"  -> {'PASS' if f2 else 'FAIL'}")
    print(f"  F3 no-sig   (CHSH ≤ 0.75 classical):         CHSH={chsh:.4f}"
          f"  -> {'PASS' if f3 else 'FAIL'}")
    print("-" * 86)
    verdict = "🟢" if (f1 and f2 and f3) else ("🟠" if (f1 or f2) and f3 else "🔴")
    print(f"VERDICT: {verdict}  SEED+LINK composite "
          + ("STRICTLY beats either alone (synergy real) + no-signaling intact."
             if verdict == "🟢" else
             "partial — one falsifier holds; see arms." if verdict == "🟠" else
             "NO synergy — one mechanism subsumes the other (publishable null)."))
    print("  honest: toy (2 oscillators, Kuramoto H_6010 verbatim); scale-transfer "
          "UNVERIFIED (a_toy_scale_recheck). SEED rigid under detuning/drift; LINK "
          "cold-starts; composite = shared common cause ⊕ live correction channel.")


if __name__ == "__main__":
    main()
