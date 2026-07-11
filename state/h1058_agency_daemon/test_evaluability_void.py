#!/usr/bin/env python3
"""T2 negative/degenerate control (FABLE Φ-leg redesign) — FROZEN regression for the
H_9269 leg-b false-PASS bug: a shuffle-null vs a (near-)constant `other` must render VOID,
never PASS. Run: python3 test_evaluability_void.py  (exit 0 = all pass)."""
import random
import agency_T as A

def _T(n, seed=7):
    r = random.Random(seed)
    return [r.gauss(0, 1) for _ in range(n)]

def main():
    fails = []
    T = _T(240)

    # 1) DEGENERATE: constant Φ (the exact H_9269 condition, min==max) -> VOID, not PASS.
    const_phi = [0.060394] * 240
    b = A.shuffle_null(T, const_phi, min_other_sd=A.PHI_VAR_EPS)
    if not b.get("void"):
        fails.append("constant Φ not flagged void: %r" % b)
    if b.get("within_2sigma_null") is not False and b.get("within_2sigma_null") is not None:
        # must NOT be True (the old false-PASS)
        pass
    if b.get("within_2sigma_null") is True:
        fails.append("constant Φ rendered within_2sigma_null=True (FALSE PASS regression!)")

    # 2) LOW-VARIANCE but non-constant Φ below the frozen bar -> still VOID.
    low_phi = [0.0603 + (i % 2) * 0.001 for i in range(240)]  # sd ~5e-4 < 0.005
    b2 = A.shuffle_null(T, low_phi, min_other_sd=A.PHI_VAR_EPS)
    if not b2.get("void"):
        fails.append("sub-bar Φ (sd<%.3g) not void: %r" % (A.PHI_VAR_EPS, b2))

    # 3) POSITIVE: Φ with real variance -> EVALUABLE (a real bool, not void).
    r = random.Random(11)
    var_phi = [0.05 + r.gauss(0, 0.03) for _ in range(240)]
    b3 = A.shuffle_null(T, var_phi, min_other_sd=A.PHI_VAR_EPS)
    if b3.get("void"):
        fails.append("varying Φ wrongly voided: %r" % b3)
    if not isinstance(b3.get("within_2sigma_null"), bool):
        fails.append("varying Φ within_2sigma_null not a bool: %r" % b3)

    # 4) leg (c) sanity: T vs t_idx (always varies) must remain EVALUABLE.
    b4 = A.shuffle_null(T, list(range(240)))
    if b4.get("void"):
        fails.append("leg-c (T vs t) wrongly voided: %r" % b4)

    if fails:
        print("FAIL (%d):" % len(fails))
        for f in fails:
            print("  -", f)
        return 1
    print("PASS 4/4: constant→VOID · sub-bar→VOID · varying→EVALUABLE(bool) · leg-c→EVALUABLE")
    print("  (H_9269 false-PASS bug can no longer render a degenerate Φ leg as PASS)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
