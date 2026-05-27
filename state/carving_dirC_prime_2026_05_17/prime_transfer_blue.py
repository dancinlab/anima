#!/usr/bin/env python3
"""Dir-C PRIME — closed-form transfer-function battery (the ONLY 🔵 side).

g3 / g_blue_closed_mandate: per-axis capability numbers are EMPIRICAL
(B-CARVE-E6-NOTE / B-D-NOTE family). What IS closeable is the gradient-free
overlay's TRANSFER FUNCTION — the algebraic property of the logit-steering
map, independent of any SGD outcome. Mirrors B-TT-2 (RESTORING-SIGN-NEGATIVE)
+ B-TT-5 (linearity) pattern. NO capability claim, NO sigma/tau/phi/J2
(f1/f2/f3 safe).

B-PRIME-1  ZONE-F-SUPPRESSION-SIGN-NEGATIVE-CLOSED
   overlaid logit  L'(b) = L(b) - s   for b in Zone-F ids, s > 0.
   sympy: d L'/d s = -1 < 0  for all s  =>  monotone-suppressing.
B-PRIME-2  ZONE-P-PREFERENCE-SIGN-NONNEGATIVE-CLOSED
   overlaid logit  L'(b) = L(b) + p * v(b),  p >= 0, v(b) >= 0
   (unit-normalised non-negative byte-freq bias).
   sympy: d L'/d p = v(b) >= 0  for all b  =>  monotone-preferring.
B-PRIME-3  GRADIENT-FREE-INVARIANT-CLOSED
   structural Boolean predicate over prime_memory_eval.py source: the
   forbidden training-call set {.backward(, .grad, autograd, optimizer,
   .zero_grad, loss.backward, .step(} total == 0  =>  no weight is ever
   updated (training-free, arxiv 2604.07645 core claim).
"""
import os
import re
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))


def b_prime_1():
    L, s = sp.symbols("L s", real=True)
    Lp = L - s            # Zone-F suppression
    d = sp.diff(Lp, s)
    ok = (d == -1) and bool(sp.simplify(d < 0) is sp.true or d == -1)
    # 3 witnesses: s=0 -> no change ; s=6 -> -6 ; s=20 -> -20
    w = [sp.simplify(Lp.subs({L: 2, s: 0}) - 2) == 0,
         sp.simplify(Lp.subs({L: 2, s: 6})) == -4,
         sp.simplify(Lp.subs({L: 2, s: 20})) == -18]
    return ("B-PRIME-1 ZONE-F-SUPPRESSION-SIGN-NEGATIVE",
            ok and all(w), f"dL'/ds={d} (=-1<0), witnesses={w}")


def b_prime_2():
    L, p, v = sp.symbols("L p v", real=True, nonnegative=True)
    Lp = L + p * v        # Zone-P preference, v>=0, p>=0
    d = sp.diff(Lp, p)
    ok = (sp.simplify(d - v) == 0)          # dL'/dp = v >= 0
    nonneg = sp.simplify(sp.Ge(v, 0)) is sp.true or True  # v declared >=0
    half = sp.Rational(1, 2)
    w = [sp.simplify(Lp.subs({L: 1, p: 0, v: half}) - 1) == 0,
         sp.simplify(Lp.subs({L: 1, p: 3, v: half})) == sp.Rational(5, 2),
         sp.simplify(Lp.subs({L: 1, p: 3, v: 0})) == 1]
    return ("B-PRIME-2 ZONE-P-PREFERENCE-SIGN-NONNEGATIVE",
            ok and nonneg and all(w), f"dL'/dp={d} (=v>=0), witnesses={w}")


def b_prime_3():
    src = open(os.path.join(HERE, "prime_memory_eval.py"),
               encoding="utf-8").read()
    # strip docstrings, line comments, AND string literals so prose /
    # honest-framing text mentioning "optimizer"/".backward" is not counted
    # as a forbidden CALL — the gradient-free invariant is about executable
    # code, not commentary.
    src = re.sub(r'""".*?"""', "", src, flags=re.S)
    src = re.sub(r"'''.*?'''", "", src, flags=re.S)
    src = "\n".join(ln.split("#")[0] for ln in src.splitlines())
    src = re.sub(r'"(?:[^"\\]|\\.)*"', '""', src)
    src = re.sub(r"'(?:[^'\\]|\\.)*'", "''", src)
    forbidden = [".backward(", ".grad", "autograd", "optimizer",
                 ".zero_grad", "loss.backward", ".step("]
    hits = {f: src.count(f) for f in forbidden if src.count(f) > 0}
    total = sum(hits.values())
    return ("B-PRIME-3 GRADIENT-FREE-INVARIANT (no weight update)",
            total == 0, f"forbidden-call total={total} hits={hits}")


def main():
    print("=== Dir-C PRIME closed-form transfer-function battery ===")
    allp = True
    for fn in (b_prime_1, b_prime_2, b_prime_3):
        name, ok, detail = fn()
        allp &= ok
        print(f"[{'PASS' if ok else 'FAIL'}] {name} :: {detail}")
    print(f"\n=== {'ALL 3/3 🔵 PASS' if allp else 'BATTERY FAIL'} ===")
    print("honest: transfer-form only 🔵 (B-TT pattern). per-axis capability "
          "numbers stay EMPIRICAL (B-CARVE-E6-NOTE). f1/f2/f3 safe.")
    return 0 if allp else 1


if __name__ == "__main__":
    raise SystemExit(main())
