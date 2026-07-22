#!/usr/bin/env python3
"""Is the held-out completion even DETERMINED? $0, exact count, milliseconds.

WHY THIS RUNS AFTER V6_P1c AND PARTLY OVERTURNS IT
--------------------------------------------------
V6_P1c concluded that generalization needs a bias matched to the data's structure, citing
three tables: cyclic generalizes (0.6875), latin does not (0.0417), arbitrary does not
(0.0208). That reading assumed all three ASK a well-posed question -- that the held-out
cells have an answer to get right.

They do not. Counting completions consistent with each table's own constraint, given the
48 training cells:

    cyclic      1 completion       the answer is determined
    latin       1 completion       determined -- so its failure is a REAL failure
    arbitrary   1152-2592          UNDERDETERMINED by three orders of magnitude

So the arbitrary arm was never a test. With over a thousand consistent fillings, no model
and no bias can do better than guess among them, and its 0.0208 says nothing about
composition. That column has to be WITHDRAWN as evidence rather than explained.

What survives is sharper, not weaker: the LATIN arm has a unique answer, and neither the
matched-bias model (0.0417) nor the universal-capacity model (0.0000) finds it, while the
group arm reaches 0.6875. The claim rests on latin alone now, and there it rests cleanly.

The lesson is the one this repo keeps paying for: check that the question has an answer
before reading a failure to answer it.
"""
import itertools, importlib.util, numpy as np
spec=importlib.util.spec_from_file_location("sc","p1_nongroup_scope.py")
sc=importlib.util.module_from_spec(spec); spec.loader.exec_module(sc)
N=sc.N

def count_completions(table, held, kind, cap=200000):
    """How many fillings of the held-out cells are consistent with the constraint the
    table kind imposes? 1 = the answer is determined; >1 = the model is being asked
    something the data does not decide."""
    held=list(held)
    rows=[set(table[i][j] for j in range(N) if (i,j) not in held) for i in range(N)]
    cols=[set(table[i][j] for i in range(N) if (i,j) not in held) for j in range(N)]
    n=0
    def rec(k, rows, cols):
        nonlocal n
        if n>cap: return
        if k==len(held):
            n+=1; return
        i,j=held[k]
        for v in range(N):
            if kind in ("cyclic","latin"):
                if v in rows[i] or v in cols[j]: continue
            else:  # arbitrary: only column balance is a constraint
                if v in cols[j]: continue
            rows[i].add(v); cols[j].add(v)
            rec(k+1, rows, cols)
            rows[i].discard(v); cols[j].discard(v)
    rec(0, rows, cols)
    return n

print("held-out DETERMINACY — is there exactly ONE consistent completion?")
print("if not, a 0.0000 held-out is the task having no answer, not the model failing\n")
print("%-11s %10s %14s"%("table","completions","reading"))
print("-"*40)
for kind in ("cyclic","latin","arbitrary"):
    cs=[]
    for s in sc.SEEDS:
        env=sc.build(s,kind)
        cs.append(count_completions(env["table"], env["test"], kind))
    med=int(np.median(cs))
    rd = "DETERMINED" if med==1 else "UNDERDETERMINED (%dx)"%med
    print("%-11s %10s %14s"%(kind, "/".join(str(c) for c in cs), rd))
print("-"*40)
print()
print("note: for cyclic the GROUP also determines it, which is a second, stronger")
print("constraint than the latin property alone.")
