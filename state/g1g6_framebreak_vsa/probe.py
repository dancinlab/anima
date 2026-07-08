#!/usr/bin/env python3
"""
$0 falsifier — Fable framebreak candidate #1 (VSA/HRR fixed-primitive bind + resonator decode).

Question the DPI operator-wall poses: is held-out RECOMBINATION escapable by a FIXED
(zero-trained) algebraic bind + fixed cleanup readout, where the CE gradient never touches
the composition? Distinct from #3108 γ (which kept a CE/bilinear-trained readout).

Honest, non-rigged metric (no tune-to-green): superposition-capacity partner recovery.
  - Bundle M random pairs (a_i, b_i) drawn from a codebook. Pairs are NEVER "trained"
    (VSA needs no training) and are disjoint samples => held-out by construction.
  - VSA:   S = Σ a_i ⊛ b_i ; query partner of a_j via S ⊛ inv(a_j) -> cleanup to codebook.
  - ADD:   S = Σ (a_i + b_i) ; query partner of a_j via (S - a_j) -> cleanup to codebook.
  - SHUF null: same VSA decode but cleanup-target list shuffled (destroys binding).
Recombination is real iff VSA >> ADD and VSA >> SHUF at capacity. ADD provably cannot
preserve which-a-pairs-with-which-b in a bundle (order/pairing collapses).

Also reports the DPI/information caveat: this tests the OPERATOR wall only. Predicting a
held-out pair's *follower* needs info the corpus lacks (#3109 information floor) — separate.
"""
import numpy as np

def circconv(x, y):   # binding ⊛ (circular convolution via FFT)
    return np.real(np.fft.ifft(np.fft.fft(x) * np.fft.fft(y)))

def circcorr(x, y):   # unbinding: correlate x with y  (== x ⊛ inv(y), inv = involution)
    return np.real(np.fft.ifft(np.fft.fft(x) * np.conj(np.fft.fft(y))))

def run(D=1024, N_codebook=512, M_bundle=8, trials=300, seed=7):
    rng = np.random.default_rng(seed)
    # unit-variance gaussian atoms (standard HRR); normalize for stable cleanup
    book = rng.standard_normal((N_codebook, D)) / np.sqrt(D)
    def cleanup(vec, exclude=None):
        sims = book @ vec / (np.linalg.norm(book, axis=1) * np.linalg.norm(vec) + 1e-12)
        if exclude is not None:
            sims[exclude] = -np.inf
        return int(np.argmax(sims))

    vsa_hit = add_hit = shuf_hit = 0
    for t in range(trials):
        idx = rng.choice(N_codebook, size=2 * M_bundle, replace=False)
        a_ids, b_ids = idx[:M_bundle], idx[M_bundle:]
        A = book[a_ids]; B = book[b_ids]
        # --- VSA bundle of bindings ---
        S_vsa = np.sum([circconv(A[i], B[i]) for i in range(M_bundle)], axis=0)
        # --- additive bundle (control) ---
        S_add = np.sum(A, axis=0) + np.sum(B, axis=0)
        # query a random slot's partner (held-out pairing; exclude the a atoms from cleanup)
        q = rng.integers(M_bundle)
        a_q, true_b = a_ids[q], b_ids[q]
        # VSA: unbind
        b_hat_vsa = circcorr(S_vsa, book[a_q])
        vsa_hit += (cleanup(b_hat_vsa, exclude=a_ids) == true_b)
        # ADD: subtract queried a, then cleanup remaining (best additive can do)
        b_hat_add = S_add - book[a_q]
        add_hit += (cleanup(b_hat_add, exclude=a_ids) == true_b)
        # SHUF null: unbind with a WRONG (shuffled) a -> binding destroyed
        wrong_a = book[a_ids[(q + 1) % M_bundle]]
        b_hat_shuf = circcorr(S_vsa, wrong_a)
        shuf_hit += (cleanup(b_hat_shuf, exclude=a_ids) == true_b)

    return dict(D=D, N_codebook=N_codebook, M_bundle=M_bundle, trials=trials,
                chance=1.0 / (N_codebook - M_bundle),
                vsa_acc=vsa_hit / trials, add_acc=add_hit / trials, shuf_acc=shuf_hit / trials)

if __name__ == "__main__":
    print("=== VSA fixed-primitive held-out recombination (operator-wall $0 falsifier) ===")
    for M in (4, 8, 16, 32):
        r = run(M_bundle=M)
        print(f"M={M:2d} bundle | VSA={r['vsa_acc']:.3f}  ADD={r['add_acc']:.3f}  "
              f"SHUF={r['shuf_acc']:.3f}  chance={r['chance']:.4f}")
    # verdict on the escapable-operator claim, evaluated at a mid capacity
    r = run(M_bundle=8)
    escapes = (r['vsa_acc'] > 0.66) and (r['vsa_acc'] > 5 * max(r['add_acc'], r['shuf_acc'], r['chance']))
    print("\nVERDICT:", "OPERATOR-WALL-ESCAPABLE (fixed VSA recombines held-out pairs >> additive/shuf)"
          if escapes else "no fixed-primitive advantage (collapses to additive floor)")
    print("CAVEAT: tests the OPERATOR wall only; the INFORMATION floor (#3109 novel-pair follower"
          " signal absent from corpus) is separate and unaddressed by any bind operator.")
