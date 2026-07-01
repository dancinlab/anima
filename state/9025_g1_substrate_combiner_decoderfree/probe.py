#!/usr/bin/env python3
"""H_9025 Rung0 — decoder-free substrate-G1 harness (numpy, DIRECTIONAL).

Purpose (HONEST SCOPE, c9): NOT a new G1 verdict. It is
  (1) the decoder-free measurement harness (no mouth / no clm_decode / no next-byte),
  (2) a prototype of the MISSING constructive-combiner op (H_1822: live substrate has none),
  (3) a SHUFFLE-CONTROLLED calibration separating a genuine key-locked bind from additive.

Rung0 finding drove the harness fix: raw recover is SPOOFABLE — additive stores B linearly
in C=a+b, so a key-agnostic subtraction "recovers" B with ANY key. The honest gate is
M2-EARNED = right key recovers B AND wrong (shuffled) key FAILS. Even so, EARNED recovery is
a key-locked STORAGE/binding property (hrr has it, additive doesn't); H_1840 already showed
even invertible ⊛ does NOT beat additive on the held-out RECOMBINATION target. So held-out
compositional generalization (the real G1 lever) needs a TRAINED W_bind under a recomb
objective = Rung1 GPU, prior LOW. Do NOT read a GREEN off this file.

grep-clean: numpy only (no torch / no gauge_lib).
"""
import sys
import numpy as np

D = 128
N_PAIRS = 40
SPLIT_THRESH = 0.30
RECOVER_THRESH = 0.30
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 7


def unit(v):
    n = np.linalg.norm(v, axis=-1, keepdims=True)
    return v / np.where(n == 0, 1, n)


# --- constructive-combiner ops (the lane the live substrate lacks) ---
def op_additive(a, b):
    return unit(a + b)

def op_hrr(a, b):
    return unit(np.real(np.fft.ifft(np.fft.fft(a) * np.fft.fft(b))))

def make_tensorproj(P):
    return lambda a, b: unit(np.outer(a, b).reshape(-1) @ P)


def recover_hrr(c, key):
    return unit(np.real(np.fft.ifft(np.fft.fft(c) * np.conj(np.fft.fft(key)))))

def recover_additive(c, key):
    k = unit(key)
    return unit(c - k * (c @ k))


def basin_dist(x, y):
    return 1.0 - float(unit(x) @ unit(y))


def eval_op(name, combine, recover, A, B, Ashuf):
    n = len(A)
    dist_ok = rec_raw = shuf_collapse = earned = ablate_earned = 0
    for i in range(n):
        c = combine(A[i], B[i])
        if basin_dist(c, A[i]) > SPLIT_THRESH and basin_dist(c, B[i]) > SPLIT_THRESH:
            dist_ok += 1
        rr = float(unit(recover(c, A[i])) @ unit(B[i]))        # right key
        rw = float(unit(recover(c, Ashuf[i])) @ unit(B[i]))    # wrong (shuffled) key
        if rr > RECOVER_THRESH:
            rec_raw += 1
        if rw <= RECOVER_THRESH:
            shuf_collapse += 1
        if rr > RECOVER_THRESH and rw <= RECOVER_THRESH:       # M2 EARNED
            earned += 1
        # ablation: op -> additive, EARNED metric (must go inert if lift is the op)
        c_ab = op_additive(A[i], B[i])
        ar = float(unit(recover_additive(c_ab, A[i])) @ unit(B[i]))
        aw = float(unit(recover_additive(c_ab, Ashuf[i])) @ unit(B[i]))
        if ar > RECOVER_THRESH and aw <= RECOVER_THRESH:
            ablate_earned += 1
    return dict(op=name, distinct=f"{dist_ok}/{n}", recover_raw=f"{rec_raw}/{n}",
                shuf_collapse=f"{shuf_collapse}/{n}", earned=f"{earned}/{n}",
                ablate_earned=f"{ablate_earned}/{n}")


def main():
    rng = np.random.default_rng(SEED)
    basis = unit(rng.standard_normal((8, D)))
    def concept():
        w = rng.standard_normal(8)
        return unit(w @ basis + 0.15 * rng.standard_normal(D))
    A = np.stack([concept() for _ in range(N_PAIRS)])
    B = np.stack([concept() for _ in range(N_PAIRS)])
    Ashuf = A[rng.permutation(N_PAIRS)]                        # wrong keys for shuffle control
    P = rng.standard_normal((D * D, D)) / np.sqrt(D * D)

    rows = [
        eval_op("additive", op_additive, recover_additive, A, B, Ashuf),
        eval_op("hrr_conv", op_hrr, recover_hrr, A, B, Ashuf),
        eval_op("tensorproj", make_tensorproj(P), recover_additive, A, B, Ashuf),
    ]
    st = float(unit(recover_hrr(op_hrr(A[0], B[0]), A[0])) @ unit(B[0]))
    print(f"SEED={SEED} D={D} N={N_PAIRS} SPLIT_THRESH={SPLIT_THRESH} RECOVER_THRESH={RECOVER_THRESH}")
    print(f"SELFTEST hrr unbind(B) cos={st:.3f} -> {'PASS' if st>RECOVER_THRESH else 'FAIL'}")
    print(f"{'op':<12}{'M1 distinct':<13}{'recover_raw':<13}{'shuf_collapse':<15}{'M2 EARNED':<12}{'ablate_earned'}")
    for r in rows:
        print(f"{r['op']:<12}{r['distinct']:<13}{r['recover_raw']:<13}{r['shuf_collapse']:<15}{r['earned']:<12}{r['ablate_earned']}")
    print()
    print("READ (c9): shuffle-controlled. additive recover_raw high but M2-EARNED ~0")
    print("(key-agnostic = fake). hrr M2-EARNED high (key-locked bind). ablate_earned ~0")
    print("everywhere confirms lift is the OP not the recover fn. STILL harness-QA only:")
    print("earned recovery = storage property; held-out RECOMBINATION (real G1) needs a")
    print("TRAINED W_bind (Rung1 GPU, prior LOW per H_1840 fair-gate + DPI).")


if __name__ == "__main__":
    main()
