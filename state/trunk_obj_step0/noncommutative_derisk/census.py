#!/usr/bin/env python3
"""STEP-0.5 de-risk / data exploration + cycle census.

Reproduces STEP-0 EXP-B intransitivity census (model-free) AND builds the
precedence matrix P[a->b] over top-N vocab that the frozen-residual R^2
regression (derisk.py) consumes.  $0 CPU-local, numpy only.
"""
import sys, re, json, collections
import numpy as np

CORPUS = "/Users/mini/dancinlab/anima/archive/state_legacy/anima_phase1a1_color_cosmology_2026_05_12/consciousness_anchor.txt"
OUT = "/Users/mini/dancinlab/anima/state/trunk_obj_step0/noncommutative_derisk"

TOP_N = 400          # vocab size (frequency-ranked) for precedence matrix
WINDOW = 0           # 0 = whole utterance (a before b anywhere in same line)

def tok(line):
    # 어절 = whitespace split; strip trailing punctuation glued to token edges
    return [w for w in line.strip().split() if w]

def main():
    freq = collections.Counter()
    lines = []
    with open(CORPUS, encoding="utf-8", errors="replace") as f:
        for line in f:
            ws = tok(line)
            if not ws:
                continue
            lines.append(ws)
            freq.update(ws)
    print(f"lines={len(lines)} total_tokens={sum(freq.values())} distinct={len(freq)}")

    vocab = [w for w, _ in freq.most_common(TOP_N)]
    vidx = {w: i for i, w in enumerate(vocab)}
    N = len(vocab)
    P = np.zeros((N, N), dtype=np.float64)  # P[i,j] = count(i precedes j in same line)

    for ws in lines:
        # keep only vocab tokens, preserve order, dedup within line to first occurrence
        seen = {}
        seq = []
        for w in ws:
            i = vidx.get(w)
            if i is None:
                continue
            if i not in seen:
                seen[i] = len(seq)
                seq.append(i)
        # ordered pairs: earlier index precedes later
        L = len(seq)
        for a in range(L):
            ia = seq[a]
            for b in range(a + 1, L):
                ib = seq[b]
                P[ia, ib] += 1.0

    # ---- cycle census over pairs with adequate mass ----
    MINC = 20  # min total directed mass on a pair to include in the tournament
    tot = P + P.T
    # dominance relation D[i,j] = 1 if i beats j (i precedes j more often), with mass>=MINC
    D = np.zeros((N, N), dtype=np.int8)
    strict = 0
    for i in range(N):
        for j in range(i + 1, N):
            m = tot[i, j]
            if m < MINC:
                continue
            if P[i, j] > P[j, i]:
                D[i, j] = 1
            elif P[j, i] > P[i, j]:
                D[j, i] = 1
            else:
                continue
            strict += 1

    # count triangles that are fully-connected (all 3 edges strict) -> transitive vs 3-cycle
    tri = 0
    cyc = 0
    active = [i for i in range(N) if (D[i].sum() + D[:, i].sum()) > 0]
    for ai in range(len(active)):
        i = active[ai]
        for aj in range(ai + 1, len(active)):
            j = active[aj]
            if not (D[i, j] or D[j, i]):
                continue
            for ak in range(aj + 1, len(active)):
                k = active[ak]
                e_ij = D[i, j] or D[j, i]
                e_jk = D[j, k] or D[k, j]
                e_ik = D[i, k] or D[k, i]
                if not (e_ij and e_jk and e_ik):
                    continue
                tri += 1
                out = {i: 0, j: 0, k: 0}
                out[i] += D[i, j] + D[i, k]
                out[j] += D[j, i] + D[j, k]
                out[k] += D[k, i] + D[k, j]
                # 3-cycle iff each node has out-degree exactly 1 (no source/sink)
                if sorted(out.values()) == [1, 1, 1]:
                    cyc += 1

    cyc_frac = cyc / tri if tri else 0.0
    print(f"strict_edges={strict} full_triangles={tri} three_cycles={cyc} cycle_frac={cyc_frac:.4f}")

    np.save(f"{OUT}/P.npy", P)
    with open(f"{OUT}/vocab.json", "w") as f:
        json.dump({"vocab": vocab, "TOP_N": TOP_N, "MINC_census": MINC}, f, ensure_ascii=False)
    with open(f"{OUT}/census.json", "w") as f:
        json.dump({"lines": len(lines), "distinct": len(freq), "N": N,
                   "strict_edges": int(strict), "full_triangles": int(tri),
                   "three_cycles": int(cyc), "cycle_frac": cyc_frac}, f)
    print("saved P.npy, vocab.json, census.json")

if __name__ == "__main__":
    main()
