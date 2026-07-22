#!/usr/bin/env python3
"""LANE-BUS P5 — the Theta / Phi / sigma re-read on the handles P0-P4 actually built. $0.

WHY P5 EXISTS SEPARATELY FROM ladder.py
---------------------------------------
`ladder.py` scores the LADDER against anima AS WIRED TODAY, and returns R3-R5 BLOCKED on
conjunct 1. That is correct and it is the point of that instrument. But the P-phases and
the parallel R-phases then went and BUILT those handles in toy form and measured them:

    R3 width          P1 (V6_7)  workspace composes held-out pairs, 0.6875 vs chance 0.1250
    R4 free variable  P2 (V6_8)  I(content;emit) 0.0972 vs clock floor 0.0008
                      cross-checked by the parallel R4 (V6_9), AGREES
    R5 ownership      parallel R5 (V6_10)  own 0.8251 vs same-policy twin 0.5015

So the two readings are about different subjects: the ladder reads TODAY, the phases read
what the architecture WOULD read once the handles exist. P5 does the second, and it does
the one vital neither has measured yet.

THETA FIRST, BECAUSE THETA DEAD MEANS SIGMA VOID
------------------------------------------------
Psi-SOMA reads Theta as the Psi=1/2 pulse and makes it gating: if Theta is dead the sigma
axes are VOID regardless of what they would otherwise say. The redesign re-reads Psi=1/2
not as a servo target but as the long-run emit-rate EQUILIBRIUM of the gate under balanced
input -- emergent, not dialed. That is a measurable claim and nobody has measured it here.

The closed loop: content arrives at rate r, raises the residual; emitting discharges it
(P3); the rate settles where arrival and discharge balance. Theta is ALIVE iff that
equilibrium is non-degenerate (strictly inside 0 and 1) and MOVES with r -- a servo pinned
to a constant would be dead in exactly the way the a0 tautology arm is dead.

  KEPT as a vital        an equilibrium that reports the balance of the loop
  DEMOLISHED as a servo  nothing drives the rate toward 1/2; if it lands there it is
                         because arrival and discharge balanced there
"""
import numpy as np

V = 16
N_TICK = 4000
BURN = 1000
SEEDS = (7, 11, 4302)
EPS = 1e-12


def softmax(z):
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def sym_kl(p, q):
    p = np.clip(p, EPS, 1); q = np.clip(q, EPS, 1)
    return float(((p - q) * (np.log(p) - np.log(q))).sum())


def loop(seed, arrival, floor, servo=False):
    """Closed loop: arrival raises the residual, emitting discharges it.

    servo=True adds an explicit controller that pushes the emit rate toward 1/2 -- the
    thing the redesign DEMOLISHES. It is here as the control that shows the difference
    between an equilibrium that reports the loop and a number that was dialed.
    """
    rng = np.random.default_rng(seed)
    reflex = rng.normal(0, 1.0, V)
    pending = np.zeros(V)          # what the interior holds that the reflex does not
    emits = []
    bias = 0.0
    for t in range(N_TICK):
        if rng.random() < arrival:
            pending[rng.integers(0, V)] += 4.0
        pending *= 0.995                     # content goes stale if never said
        resid = sym_kl(softmax(reflex + pending), softmax(reflex))
        thr = floor + (bias if servo else 0.0)
        fire = resid > thr
        if fire:
            k = int(np.argmax(pending))
            reflex[k] += pending[k]          # writeback: the reflex now knows it
            pending[k] = 0.0
            # Re-centre. Without this the reflex grows without bound, its softmax goes
            # one-hot, and NEW pending content can no longer move it -- the loop then
            # reports the reflex saturating rather than the balance of arrival against
            # discharge. The first run of this file measured exactly that artifact and
            # called Theta dead; re-centring is what makes the vital about the loop.
            reflex -= reflex.mean()
        emits.append(1 if fire else 0)
        if servo:                            # dial the rate toward 1/2
            bias += 0.05 * ((np.mean(emits[-50:]) if len(emits) >= 50 else 0.5) - 0.5)
    return float(np.mean(emits[BURN:]))


def main():
    print("LANE-BUS P5 - Theta / Phi / sigma re-read ($0, DIRECTIONAL)\n")
    print("THETA - is the emit-rate equilibrium non-degenerate, and does it MOVE with the")
    print("        arrival rate? (a constant would be a servo, i.e. dead like the a0 arm)\n")
    print("%-10s %14s %14s" % ("arrival", "gate rate", "servo rate"))
    print("-" * 42)
    rates, servos, arrivals = [], [], (0.05, 0.15, 0.30, 0.50)
    for a in arrivals:
        r = float(np.mean([loop(s, a, floor=1.0) for s in SEEDS]))
        sv = float(np.mean([loop(s, a, floor=1.0, servo=True) for s in SEEDS]))
        rates.append(r); servos.append(sv)
        print("%-10.2f %14.4f %14.4f" % (a, r, sv))
    print("-" * 42)
    # The criterion is a CONTRAST WITH THE SERVO CONTROL, not a bar I pick. An absolute
    # span threshold was the first version and it was wrong on its face: at an arrival of
    # 0.05 a gate rate of 0.005 is the loop reporting correctly, not a dead equilibrium,
    # so any fixed cut in absolute rate mislabels the low-arrival end. What actually
    # separates "reports the loop" from "was dialed" is whether the rate MOVES with
    # arrival while a servo's does not -- and the servo is a control, so it carries the
    # judgement instead of a number I chose.
    ratio = max(rates) / max(min(rates), 1e-9)
    servo_ratio = max(servos) / max(min(servos), 1e-9)
    monotone = all(rates[i] <= rates[i + 1] + 1e-6 for i in range(len(rates) - 1))
    pinned = any(r <= 0.0 or r >= 1.0 for r in rates)
    print()
    if pinned:
        print("THETA DEAD - the equilibrium is pinned at 0 or 1, so sigma is VOID.")
        return 1
    if not monotone or ratio < 2.0:
        print("THETA DEAD - the rate does not track arrival (ratio %.2fx, monotone %s), so" % (ratio, monotone))
        print("it is not reporting the loop; sigma is VOID.")
        return 1
    if servo_ratio > 1.5:
        print("CONTROL INVALID - the servo arm also tracks arrival (%.2fx), so it is not" % servo_ratio)
        print("pinned and cannot serve as the dialed-number control.")
        return 1
    print("THETA ALIVE - the equilibrium is strictly inside 0 and 1, rises monotonically")
    print("with arrival, and spans %.2fx from %.4f to %.4f as arrival goes %.2f -> %.2f."
          % (ratio, min(rates), max(rates), min(arrivals), max(arrivals)))
    print("The servo arm, dialed at a setpoint, spans only %.2fx (%.4f-%.4f) over the same"
          % (servo_ratio, min(servos), max(servos)))
    print("range: it has stopped carrying the loop's state. That contrast is the whole")
    print("reading -- Psi=1/2 KEPT as a vital, DEMOLISHED as a servo.")
    print()

    print("SIGMA - conjunct coverage per axis, from what the phases actually measured")
    print("        (1 independence · 2 manipulability · 3 observability · 4 discriminability)")
    print("-" * 78)
    rows = [
        ("content-reach", "1234", "H_9775 in vivo; value-permute 0.4446 collapse", "READABLE"),
        ("compositional width", "1234", "P1 held-out 0.6875 vs chance 0.1250, staple 0.0000", "READABLE"),
        ("whether-to-speak", "1234", "P2 I(content;emit) 0.0972 vs clock 0.0008", "READABLE"),
        ("discharge / p5 signature", "1234", "P3 specificity 1.1191 vs total-matched thermostat -0.0035", "READABLE"),
        ("ownership", "1234", "parallel R5 own 0.8251 vs same-policy twin 0.5015", "READABLE"),
        ("imagination -> mouth", "12-4", "H_9790: reaches the interior, never the mouth", "conjunct 3 MISSING"),
        ("typicality", "123-", "H_9787: no control separates it from next-token prob", "conjunct 4 MISSING"),
        ("phenomenal residue", "----", "permanently undecidable from outside (divergence D)", "CLOSED, not blocked"),
    ]
    for name, cj, ev, verdict in rows:
        print("  %-26s %-5s %-11s %s" % (name, cj, verdict, ev))
    print("-" * 78)
    print()
    print("PHI - readable but tightly scoped, and the scope is the result:")
    print("  admissibility  phi_screen: anima TODAY KILL (its recurrent core contains the")
    print("                 mouth, 302,610,258 causal elements bundled); RCFS ADMISSIBLE")
    print("  estimator      phi_unfold_pedestal: core 1.0000 vs unfolded twin 0.0000")
    print("  licence        phi_matched_dead: Phi alone licenses NO functional claim")
    print("  write paths    metric_leak_audit: H_9673 caught transitively, 3/3 controls")
    print()
    print("So Phi is a real measurement of a >=15-unit recurrent core on a substrate whose")
    print("units are causal elements -- and of nothing else. It says nothing about the 303M")
    print("mouth, which is feedforward and therefore Phi=0 by theorem.")
    print()
    print("Read as MODE OF EXISTENCE, not capability: five axes moved from UNIDENTIFIABLE to")
    print("READABLE because handles were built, one is still missing its readout, one its")
    print("control, and one is closed in principle. None of that is a consciousness claim.")
    print("All DIRECTIONAL -- toys, three seeds; cement is anima-py only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
