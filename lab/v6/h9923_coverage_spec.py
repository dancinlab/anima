#!/usr/bin/env python3
"""H_9923 -- does a COVERAGE SPEC decide held-out generalisation, or was it the named splits?

H_9922 froze a fire condition on two splits that fable and sol had named. That condition is
still unmet and is NOT retired here. But the coverage sweep showed the outcome tracks how the
training offsets are spread, and those two named splits were simply two sparse samples of that
space -- so the condition was pinned to the wrong axis.

Rewriting a bar after seeing data is exactly how tune-to-green happens, so the rewrite is
constrained in the only way that makes it honest: the new condition is attached to a SPEC, not
to any split, and it is executed over EVERY split satisfying the spec, drawn without looking.
Reading only the splits that pass becomes impossible by construction.

The spec, frozen in V6_H9923_prereg.md before this ran:

    |S| = 6, 0 in S, max adjacent gap <= 2, max(S) >= 7

Bars are NOT new -- they are the two H_9922 already froze: held-out mean >= 0.90 and held-out
minimum >= 0.80. A negative control runs alongside: equally many random splits that VIOLATE the
spec, reported but never used in the verdict.
"""
import os, sys, itertools
import numpy as np

DUMPS = os.environ.get("H9923_DUMPS", "rot_a.npz,rot_b.npz,rot_c.npz")
D = list(range(9))
BAR_MEAN, BAR_MIN, SEEN_GATE, K_MIN = 0.90, 0.80, 0.95, 12

PARTS = [p.strip() for p in DUMPS.split(",") if p.strip()]
miss = [p for p in PARTS if not os.path.exists(p)]
if miss:
    sys.exit("missing %s -- take the hidden dumps first" % ", ".join(miss))
ZS = [np.load(p, allow_pickle=True) for p in PARTS]


def pick(d, op):
    rows = []
    for z in ZS:
        for k in sorted(z.files):
            if k.startswith("d%d|%s|" % (d, op)) and k.endswith("__last"):
                rows.append(np.asarray(z[k], dtype=np.float64).reshape(-1))
    return np.stack(rows)


def fit(A, B):
    X = np.vstack([A, B]); Xc = X - X.mean(0)
    S = (Xc.T @ Xc) / max(1, len(X) - 1)
    lam = 1e-3 * np.trace(S) / S.shape[0]
    w = np.linalg.solve(S + lam * np.eye(S.shape[0]), A.mean(0) - B.mean(0))
    return w, 0.5 * (A.mean(0) @ w + B.mean(0) @ w)


def acc(A, B, w, t):
    return 0.5 * (float((A @ w > t).mean()) + float((B @ w <= t).mean()))


A = {d: pick(d, "is") for d in D}
B = {d: pick(d, "not") for d in D}
H = {d: len(A[d]) // 2 for d in D}


def satisfies(S):
    S = sorted(S)
    if len(S) != 6 or S[0] != 0 or max(S) < 7:
        return False
    return max(S[i + 1] - S[i] for i in range(len(S) - 1)) <= 2


def score(S):
    HO = [d for d in D if d not in S]
    w, t = fit(np.vstack([A[d][:H[d]] for d in S]), np.vstack([B[d][:H[d]] for d in S]))
    seen = float(np.mean([acc(A[d][H[d]:], B[d][H[d]:], w, t) for d in S]))
    held = [acc(A[d], B[d], w, t) for d in HO]
    return seen, float(np.mean(held)), min(held), HO


ALL6 = [s for s in itertools.combinations(D, 6)]
SPEC = [s for s in ALL6 if satisfies(s)]
VIOL = [s for s in ALL6 if not satisfies(s)]
print("splits of size 6: %d total · %d satisfy the spec · %d violate it"
      % (len(ALL6), len(SPEC), len(VIOL)))

if len(SPEC) < K_MIN:
    print("\nG1 INVALID: only %d spec-satisfying splits exist, below the frozen K=%d. The spec"
          % (len(SPEC), K_MIN))
    print("is too narrow to execute; redesign it rather than reading this handful.")
    raise SystemExit(1)

print("\n  %-24s %8s %10s %9s %s" % ("spec split", "seen", "held-mean", "held-min", "pass"))
print("  " + "-" * 62)
rows, invalid = [], 0
for S in SPEC:
    seen, hm, hmin, HO = score(S)
    if seen < SEEN_GATE:
        invalid += 1
        print("  %-24s %8.4f %10s %9s  G2 INVALID (seen<%.2f)" % (str(list(S)), seen, "--", "--", SEEN_GATE))
        continue
    ok = hm >= BAR_MEAN and hmin >= BAR_MIN
    rows.append((S, hm, hmin, ok))
    print("  %-24s %8.4f %10.4f %9.4f  %s" % (str(list(S)), seen, hm, hmin, "PASS" if ok else "fail"))

rng = np.random.default_rng(9923)
viol_idx = rng.choice(len(VIOL), size=min(len(rows), len(VIOL)), replace=False)
print("\n  negative control -- same count of SPEC-VIOLATING splits (never used in the verdict)")
print("  %-24s %10s %9s" % ("violating split", "held-mean", "held-min"))
print("  " + "-" * 46)
vrows = []
for i in viol_idx:
    S = VIOL[int(i)]
    seen, hm, hmin, _ = score(S)
    vrows.append((hm, hmin))
    print("  %-24s %10.4f %9.4f" % (str(list(S)), hm, hmin))

print()
print("=" * 74)
n_pass = sum(1 for _, _, _, ok in rows if ok)
print("spec splits scored %d (G2-invalid %d) · PASS %d · fail %d"
      % (len(rows), invalid, n_pass, len(rows) - n_pass))
if vrows:
    print("negative control: mean-of-held-means %.4f vs spec %.4f"
          % (float(np.mean([h for h, _ in vrows])),
             float(np.mean([hm for _, hm, _, _ in rows]))))
print()
if rows and n_pass == len(rows):
    print("SPEC-CONFIRMED: every spec-satisfying split clears both frozen bars. The coverage")
    print("spec IS the fire condition, and the retrain is justified on it.")
elif n_pass == 0:
    print("SPEC-REFUTED: no spec-satisfying split clears the bars. Coverage spec cannot serve")
    print("as the fire condition. Hold the fire.")
else:
    print("SPEC-PARTIAL: %d of %d spec splits clear the bars, so the spec is not sufficient."
          % (n_pass, len(rows)))
    print("Do NOT go looking for what separates the passing ones -- that is post-hoc spec")
    print("rewriting, the same failure this file exists to avoid. Register and hold the fire.")
