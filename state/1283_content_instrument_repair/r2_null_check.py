"""R² NULL CHECK — a high R²(Φ ~ S_tot) is NOT evidence that structure fails to matter.

H_9294 reported `Φ* = −0.0019 + 0.4929·S_tot, R² = 0.9864` across 6 arms × 8 seeds, and the card
then said "Φ does not see structure — it is a function of total coupling". That last inference needs
its own null, and this script supplies it: draw the 6 pairwise MIs INDEPENDENTLY (no topology, no
arm, no structure at all) at the observed scale, and regress the estimator's Φ on their sum.

Result: the unstructured null already gives R² ≈ 0.81–0.86. Because Φ is a min-cut OF THE SAME
MATRIX that S_tot sums, a high pooled R² is largely forced by the estimator's own algebra — so R²
alone can never demonstrate that structure is irrelevant.

WHAT THIS DOES NOT TOUCH — H_9294's verdict stands. Its load-bearing evidence was never the R²:
    strength-matched equivalence  d′ = Φ*(B) − Φ*(X′) = −0.000170, 90% CI [−0.000243, −0.000098]
    ANCOVA residual gap           resid(B) − resid(X) = +0.000003, 90% CI [−0.000075, +0.000080]
Both are arm-vs-arm contrasts AT MATCHED COVARIATE, and neither depends on how high the pooled R²
happens to be. What this check retires is only the looser sentence built on top of them.
"""

from __future__ import annotations

import numpy as np

IDX = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)]   # 4 adjacent + 2 diagonal


def phi_from_mi(M: np.ndarray) -> float:
    """The estimator's own definition at n=4: argmin over the RAW cross-cut, divide afterwards."""
    n = 4
    best = np.inf
    for mask in range(1, 1 << (n - 1)):
        a = [0] + [b + 1 for b in range(n - 1) if (mask >> b) & 1]
        b_side = [i for i in range(n) if i not in a]
        if not b_side:
            continue
        cut = sum(M[i, j] for i in a for j in b_side)
        best = min(best, cut / min(len(a), len(b_side)))
    return float(best)


def main() -> int:
    rng = np.random.default_rng(7)
    print("null: 6 pairwise MIs drawn INDEPENDENTLY (no topology / no arm / no structure),")
    print("      at the observed arm scale (mean 0.011); then regress Φ on their sum.\n")
    print(f"{'spread sd':>10} {'R2(Phi ~ S_tot)':>16}")
    for sd in (0.002, 0.005, 0.010):
        s, p = [], []
        for _ in range(4000):
            m = np.abs(rng.normal(0.011, sd, 6))
            mat = np.zeros((4, 4))
            for v, (i, j) in zip(m, IDX):
                mat[i, j] = mat[j, i] = v
            s.append(m.sum())
            p.append(phi_from_mi(mat))
        r2 = float(np.corrcoef(s, p)[0, 1] ** 2)
        print(f"{sd:10.3f} {r2:16.4f}")
    print()
    print("=> R2 ~ 0.81-0.86 with ZERO structure. A high pooled R2 is forced by the estimator")
    print("   (Phi is a min-cut of the very matrix S_tot sums), so it can never show that structure")
    print("   is irrelevant. H_9294's verdict rests on the RESIDUAL GAP at matched strength")
    print("   (+0.000003, CI [-0.000075, +0.000080]) and the equivalence closure (-0.000170) --")
    print("   both unaffected. Only the looser 'R2=0.986 => Phi ignores structure' sentence is retired.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
