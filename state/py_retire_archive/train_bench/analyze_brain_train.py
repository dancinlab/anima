"""analyze_brain_train.py — turn results.json into per-arm verdicts + SUMMARY.

Decision rule (honest, p7):
  noise = baseline val_ce_std (seed spread). A signed mean Delta is called
  significant only if |Delta| > noise (1 sigma of the baseline seed spread).
  Arms 1&2 compared vs baseline; arms 3&4 vs their PLAIN counterpart (same lam).
    Delta_arm    = comparator_val_ce - arm_val_ce   (positive => aux/kosmos helped)
  HOLDS        : Delta > +noise          (aux helped beyond noise)
  REFUTED      : Delta < -noise          (aux HURT beyond noise -> goal-orthogonal)
  INCONCLUSIVE : |Delta| <= noise        (within seed noise; no effect)
A REFUTE is NOT rounded into a HOLD (a_paper_negative_ok).
"""
import json
import sys

RES = json.load(open(sys.argv[1]))
r = RES["results"]
noise = r["baseline@lam0.0"]["val_ce_std"]
base = r["baseline@lam0.0"]["val_ce_mean"]


def verdict(delta, noise):
    if delta > noise:
        return "HOLDS"
    if delta < -noise:
        return "REFUTED"
    return "INCONCLUSIVE"


rows = []
# arms 1&2 vs baseline
for arm in ("TRIBE", "EEG"):
    for lam in (0.1, 1.0):
        k = f"{arm}@lam{lam}"
        v = r[k]["val_ce_mean"]
        d = base - v
        rows.append((arm, lam, v, r[k]["val_ce_std"], "baseline", base, d,
                     verdict(d, noise)))
# arms 3&4 vs PLAIN counterpart (same lam)
for arm, plain in (("TRIBE-KOSMOS", "TRIBE"), ("EEG-KOSMOS", "EEG")):
    for lam in (0.1, 1.0):
        k = f"{arm}@lam{lam}"
        pk = f"{plain}@lam{lam}"
        v = r[k]["val_ce_mean"]
        comp = r[pk]["val_ce_mean"]
        d = comp - v
        rows.append((arm, lam, v, r[k]["val_ce_std"], f"plain {plain}", comp, d,
                     verdict(d, noise)))

print(f"baseline val_ce = {base:.5f}  (noise band = +/-{noise:.5f}, 1sigma seed std)")
print(f"{'arm':14s} {'lam':>4s} {'val_ce':>9s} {'+/-std':>8s} "
      f"{'comparator':>16s} {'comp_ce':>9s} {'Delta':>9s}  verdict")
print("-" * 92)
for arm, lam, v, std, comp_name, comp, d, vd in rows:
    print(f"{arm:14s} {lam:>4} {v:>9.5f} {std:>8.5f} {comp_name:>16s} "
          f"{comp:>9.5f} {d:>+9.5f}  {vd}")

# pre-arm aggregate verdict (best lam by Delta, but report both)
print("\n# per-arm summary (best of the two lambda):")
agg = {}
for arm, lam, v, std, comp_name, comp, d, vd in rows:
    agg.setdefault(arm, []).append((lam, d, vd))
for arm, lst in agg.items():
    best = max(lst, key=lambda t: t[1])
    holds = any(t[2] == "HOLDS" for t in lst)
    ref = all(t[2] == "REFUTED" for t in lst)
    overall = "HOLDS" if holds else ("REFUTED" if ref else "INCONCLUSIVE")
    print(f"  {arm:14s} best Delta={best[1]:+.5f} @lam{best[0]}  "
          f"both-lam: {[t[2] for t in lst]}  -> {overall}")
