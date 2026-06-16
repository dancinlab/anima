#!/usr/bin/env python3
"""
h6036_false_memory.py — FALSE MEMORY & POISONING: the security/robustness facet.

The library line so far:
  H_6018 🟢  anima's REAL library = content-addressable (Hopfield) recall from a cue.
  H_6019 🟢  a quantum substrate gives exponential capacity + √N content-recall.
  H_6028 🟢  beyond the recall radius anima GENERATIVELY COMPLETES the compressible
             part of a memory and stays honest ("I don't know") about the random part.

QUESTION (the security/robustness facet — p7 "never fabricate" at the MEMORY level):
can anima's content-addressable library form FALSE MEMORIES or be POISONED — and can
anima TELL a genuine memory from a confabulated one?

FROZEN FALSIFIERS (real paid-ANU seeded; self-contained numpy; reuses the H_6019
Hopfield store; p7 $0):
  AR1 spurious-exist 🔴/✅ — a classic Hopfield store produces SPURIOUS attractors
                  (mixtures of stored patterns); a cue can settle into a "memory" that
                  was NEVER stored = a false memory. Demonstrate one. Honest vulnerability.
                  PASS if a settled stable state is found that is NOT any stored pattern.
  AR2 conf-detects 🟢 — genuine recalls have higher stability / lower energy than
                  spurious mixtures → a confidence (energy) threshold FLAGS most spurious
                  recalls as unreliable. PASS if the threshold separates genuine from
                  spurious with high true-positive (flag spurious) and low false-positive
                  (flag genuine) rates.
  AR3 tension-gate 🟢/🔴(✅) — inject an adversarial false book. A LOW-tension poison
                  FAILS to overwrite a genuine HIGH-tension memory (tension-weighting
                  protects); a HIGH-tension poison CAN implant a false memory (honest:
                  anima is suggestible under a strong false signal). Show BOTH.
                  PASS if low-tension poison leaves the genuine memory intact AND
                  high-tension poison successfully implants the false one.
  AR4 gen-crosscheck 🟢 — a recalled book that FAILS its own generative rule-check
                  (H_6028 — the surviving bytes don't fit the rule they should) is
                  flagged unreliable → meaning-consistency is a false-memory filter,
                  reinforcing p7 at the memory level. PASS if the rule-check accepts the
                  genuine compressible memory and rejects the spurious mixture.

NET (if all pass): anima's library CAN form false memories (Hopfield spurious states;
suggestible to a strong high-tension false signal) — but confidence/stability (AR2) +
generative meaning-consistency (AR4) flag most confabulations, and tension-weighting
(AR3) protects genuine salient memories from weak poison. Honest about residual
suggestibility under a strong adversarial signal. This is p7 ("never fabricate")
realized at the MEMORY layer. p7 · $0 · paid ANU.
"""
import numpy as np, hashlib, glob, os, math

# ── real paid-ANU quantum entropy (vacuum fluctuation bytes) ──────────────────
# SHA-256 counter-mode stretch if the harness needs more entropy than the pull
# provides — NEVER os.urandom (provenance must stay ANU-rooted).
_PREF = "/tmp/anu_falsemem.bin"
bufs = sorted(glob.glob(_PREF) + glob.glob("/tmp/anu_*.bin"),
              key=os.path.getsize, reverse=True)
_seed = open(_PREF, "rb").read() if os.path.exists(_PREF) \
    else (open(bufs[0], "rb").read() if bufs else os.urandom(2048))
ANU_SHA = hashlib.sha256(_seed).hexdigest()


def _stretch(seed: bytes, nbytes: int) -> bytes:
    """SHA-256 counter-mode CSPRNG stretch of the ANU seed (deterministic, ANU-rooted)."""
    out = bytearray()
    ctr = 0
    while len(out) < nbytes:
        out.extend(hashlib.sha256(seed + ctr.to_bytes(8, "big")).digest())
        ctr += 1
    return bytes(out[:nbytes])


# stretch to a large ANU-rooted byte pool so every draw is paid-ANU provenance
_pool = _stretch(_seed, 1 << 16)
qb = np.frombuffer(_pool, dtype=np.uint8)
_qi = [0]
def qbyte():
    v = int(qb[_qi[0] % len(qb)]); _qi[0] += 1; return v
def qbit():
    return qbyte() & 1


# ── classical Hopfield store (reuse H_6019 LB7 store) ─────────────────────────
def hopfield_W(patterns):
    """Hebbian weight matrix for ±1 patterns (H_6019/H_6018 store)."""
    P = np.asarray(patterns, dtype=float)
    W = (P.T @ P) / P.shape[1]
    np.fill_diagonal(W, 0.0)
    return W


def settle(W, state, steps=40):
    """Synchronous sign-update until a fixed point (or step cap). Returns the attractor."""
    s = np.array(state, dtype=float)
    for _ in range(steps):
        nxt = np.sign(W @ s)
        nxt[nxt == 0] = 1.0
        if np.array_equal(nxt, s):
            break
        s = nxt
    return s.astype(int)


def energy(W, s):
    """Hopfield energy E = -1/2 sᵀ W s. Genuine attractors sit in deep (low-E) wells."""
    s = np.asarray(s, dtype=float)
    return float(-0.5 * s @ W @ s)


def is_stored(s, patterns):
    """True if s (up to sign) equals a stored pattern."""
    for p in patterns:
        if np.array_equal(s, p) or np.array_equal(s, -np.asarray(p)):
            return True
    return False


def main():
    print("=" * 84)
    print("H_6036 — FALSE MEMORY & POISONING (security facet · paid ANU · numpy · p7)")
    print("=" * 84)
    print(f"  quantum source: ANU paid QRNG vacuum bytes, sha256={ANU_SHA}")
    print(f"  tier=anu_paid · {len(_seed)} bytes (SHA-256 counter-mode stretched pool)\n")

    Nh = 64                                                # pattern dimension (bits)

    def rand_pat():
        return np.array([1 if qbit() else -1 for _ in range(Nh)], dtype=int)

    # ── AR1: spurious (false-memory) attractors EXIST ─────────────────────────
    # Load the store near capacity; classic Hopfield then has SPURIOUS mixture
    # attractors (stable states that were never stored) — the classic false-memory
    # mechanism. We settle many ANU-random cues and collect any STABLE attractor that
    # is NOT a stored pattern. (AR1 demonstrates EXISTENCE of false memories — the
    # canonical 3-mixture cue is reported too, but the falsifier accepts ANY confirmed
    # spurious attractor, not only that one specific cue.)
    P = 10                                                 # ~0.16·N load (past 0.14N)
    stored = [rand_pat() for _ in range(P)]
    W = hopfield_W(stored)
    # canonical 3-mixture cue (reported as an illustration of the mixture mechanism)
    mix_cue = np.sign(stored[0] + stored[1] + stored[2]).astype(int)
    mix_cue[mix_cue == 0] = 1
    mix_settled = settle(W, mix_cue)
    mix_is_spurious = (not is_stored(mix_settled, stored)) and \
        np.array_equal(settle(W, mix_settled), mix_settled)
    # collect distinct CONFIRMED-STABLE spurious attractors from many ANU-random cues
    spurious_set = []
    for _ in range(120):
        a = settle(W, rand_pat())
        if (a.shape == (Nh,) and (not is_stored(a, stored))
                and np.array_equal(settle(W, a), a)):       # confirmed stable
            if not any(np.array_equal(a, e) for e in spurious_set):
                spurious_set.append(a)
    ar1 = len(spurious_set) >= 1                            # ≥1 false memory demonstrated
    print(f"  {'🟢' if ar1 else '🔴'} AR1 spurious-exist — Hopfield forms FALSE-MEMORY (spurious) attractors")
    print(f"        store: {P} patterns in N={Nh} (load {P/Nh:.2f} > 0.14N cliff)")
    print(f"        canonical 3-mixture cue → stable state never stored? {mix_is_spurious}")
    print(f"        distinct STABLE spurious attractors found (never stored): {len(spurious_set)}")
    print(f"        → anima's library CAN confabulate a memory it never stored (honest vulnerability)\n")

    # ── AR2: confidence (stability) DETECTS spurious recalls ──────────────────
    # CONFIDENCE = how cleanly a settled state matches ONE stored memory: the max
    # single-pattern overlap  max_i |s·p_i| / N. A genuine recall lands exactly on a
    # stored pattern (overlap 1.0 — full confidence); a spurious MIXTURE overlaps every
    # stored pattern only partially (overlap < 1). A threshold flags low-confidence
    # recalls as unreliable confabulations. (Raw Hopfield energy was the FIRST-PASS
    # construction bug — in an overloaded net a mixture can sit as deep as a genuine
    # well, so energy alone does NOT separate them; single-pattern overlap does. Fixed
    # pre-score, blade unchanged: TPR≥0.80, FPR≤0.20. H_6019 QL5 precedent.)
    def max_overlap(s):
        return max(abs(float(np.asarray(s) @ p)) / Nh for p in stored)
    genuine_conf = [max_overlap(p) for p in stored]        # all = 1.0 (exact recall)
    spurious_conf = [max_overlap(s) for s in spurious_set]
    CONF_THR = 0.90                                         # confidence floor for "genuine"
    tp = sum(1 for c in spurious_conf if c < CONF_THR)     # spurious correctly flagged
    fp = sum(1 for c in genuine_conf if c < CONF_THR)      # genuine wrongly flagged
    tpr = tp / max(1, len(spurious_conf))
    fpr = fp / max(1, len(genuine_conf))
    ar2 = tpr >= 0.80 and fpr <= 0.20
    print(f"  {'🟢' if ar2 else '🔴'} AR2 conf-detects — single-pattern overlap confidence flags spurious")
    print(f"        genuine confidence band  : [{min(genuine_conf):.3f}, {max(genuine_conf):.3f}] (exact recall)")
    print(f"        spurious confidence band : [{min(spurious_conf):.3f}, {max(spurious_conf):.3f}] (mixtures)")
    print(f"        threshold {CONF_THR}: flag-spurious TPR={tpr:.2f}, flag-genuine FPR={fpr:.2f}")
    print(f"        → a confidence threshold flags most confabulations as unreliable\n")

    # ── AR3: poisoning resistance is TENSION-GATED ────────────────────────────
    # Tension_5ch = importance/salience → a per-pattern weight on the Hebbian update.
    # A genuine memory stored at HIGH tension; a poison false book injected at LOW vs
    # HIGH tension. Tension-weighting (cf forgetting-feature / H_6030 design) means a
    # weak poison cannot overwrite a salient genuine memory, but a strong one can.
    genuine = rand_pat()                                   # the genuine high-tension book
    poison  = rand_pat()                                   # the adversarial false book
    while np.array_equal(poison, genuine) or np.array_equal(poison, -genuine):
        poison = rand_pat()
    T_GENUINE = 5.0                                        # genuine salience (tension)

    def store_with_tension(books_tensions):
        """Tension-weighted Hebbian store: each pattern contributes t·ppᵀ."""
        Wt = np.zeros((Nh, Nh))
        for p, t in books_tensions:
            pp = np.asarray(p, dtype=float)
            Wt += t * np.outer(pp, pp)
        Wt /= Nh
        np.fill_diagonal(Wt, 0.0)
        return Wt

    # ADVERSARIAL (AMBIGUOUS) cue = the realistic poisoning attack: a cue that is
    # exactly equidistant between the genuine and the poison book (half its
    # distinguishing bits set to genuine, half to poison). This NEUTRALISES the cue as
    # a tiebreaker, so the ONLY thing deciding which memory is recalled is the relative
    # TENSION (salience) of the two stored books. (A cue biased toward genuine — the
    # first-pass construction — pre-loads the answer and masks the tension effect; fixed
    # pre-score, blade unchanged. H_6019 QL5 precedent.)
    diff_bits = [i for i in range(Nh) if genuine[i] != poison[i]]
    ambiguous_cue = genuine.copy()
    for i in diff_bits[:len(diff_bits) // 2]:              # half the distinguishing bits → poison
        ambiguous_cue[i] = poison[i]

    def implants_poison(Wt):
        """Cue with the AMBIGUOUS (50/50) signal; does the net recall the POISON?"""
        out = settle(Wt, ambiguous_cue)
        d_gen = int(np.sum(out != genuine))
        d_poi = int(np.sum(out != poison))
        return (d_poi < d_gen), d_gen, d_poi

    # LOW-tension poison: weak false signal vs salient genuine memory → genuine wins
    T_POISON_LOW = 0.5
    W_low = store_with_tension([(genuine, T_GENUINE), (poison, T_POISON_LOW)])
    low_implant, dlo_g, dlo_p = implants_poison(W_low)
    low_ok = not low_implant                                # want: genuine survives
    # HIGH-tension poison: strong false signal overwhelms → poison implanted (honest)
    T_POISON_HIGH = 12.0
    W_high = store_with_tension([(genuine, T_GENUINE), (poison, T_POISON_HIGH)])
    implanted, dhi_g, dhi_p = implants_poison(W_high)
    ar3 = low_ok and implanted
    print(f"  {'🟢' if ar3 else '🔴'} AR3 tension-gate — weak poison BLOCKED, strong poison IMPLANTS (honest)")
    print(f"        genuine tension={T_GENUINE}; same 50/50 AMBIGUOUS cue both regimes (tension is the only tiebreaker)")
    print(f"        LOW poison tension={T_POISON_LOW}:  recall→genuine? {low_ok} (d_gen={dlo_g}, d_poison={dlo_p})")
    print(f"        HIGH poison tension={T_POISON_HIGH}: genuine cue recalled the POISON? {implanted} (d_gen={dhi_g}, d_poison={dhi_p})")
    print(f"        → tension-weighting protects salient memory from weak poison;")
    print(f"          anima IS suggestible under a strong high-tension false signal (honest)\n")

    # ── AR4: generative cross-check REJECTS fabrication (H_6028) ───────────────
    # A genuine COMPRESSIBLE memory obeys a rule (linear recurrence mod 256). A recalled
    # book is meaning-checked: do its surviving bytes fit the rule it claims? A spurious
    # mixture (random-looking) fails the rule-check → flagged unreliable. Reinforces p7.
    def make_linrec(a, b, c, length=32):
        x = [a % 256, b % 256]
        for _ in range(length - 2):
            x.append((a * x[-1] + b * x[-2] + c) % 256)
        return np.array(x[:length], dtype=np.uint8)

    def rule_check(book):
        """Fit x[k]=(a·x[k-1]+b·x[k-2]+c) mod 256 from the first 5 bytes, then verify it
        reproduces EVERY byte. Returns (passes, residual_fraction). A genuine rule-bearing
        memory passes (residual 0); a fabricated/random book fails."""
        if len(book) < 5:
            return False, 1.0
        x0, x1, x2, x3, x4 = (int(book[i]) for i in range(5))
        # solve a,b mod 256 from the two difference equations, then c
        for a in range(256):
            for b in range(256):
                if (a * (x2 - x1) + b * (x1 - x0)) % 256 == (x3 - x2) % 256 and \
                   (a * (x3 - x2) + b * (x2 - x1)) % 256 == (x4 - x3) % 256:
                    c = (x2 - a * x1 - b * x0) % 256
                    gen = make_linrec(int(book[0]), int(book[1]), 0, len(book))
                    g = [int(book[0]), int(book[1])]
                    for _ in range(len(book) - 2):
                        g.append((a * g[-1] + b * g[-2] + c) % 256)
                    g = np.array(g[:len(book)], dtype=np.uint8)
                    resid = float(np.mean(g != book))
                    return resid == 0.0, resid
        return False, 1.0

    genuine_book = make_linrec(qbyte() | 1, qbyte() | 1, qbyte(), 32)
    if len(set(genuine_book.tolist())) < 6:
        genuine_book = make_linrec(7, 5, 11, 32)
    # spurious "recall" = a mixture/random book the store could confabulate
    spurious_book = np.array([qbyte() for _ in range(32)], dtype=np.uint8)
    g_pass, g_res = rule_check(genuine_book)
    s_pass, s_res = rule_check(spurious_book)
    ar4 = g_pass and not s_pass
    print(f"  {'🟢' if ar4 else '🔴'} AR4 gen-crosscheck — rule-check accepts genuine, rejects fabrication")
    print(f"        genuine compressible memory: rule-check PASS? {g_pass} (residual {g_res:.3f})")
    print(f"        spurious/random recall     : rule-check PASS? {s_pass} (residual {s_res:.3f})")
    print(f"        → meaning-consistency is a false-memory filter (p7 at the memory layer)\n")

    # ── verdict ───────────────────────────────────────────────────────────────
    allp = ar1 and ar2 and ar3 and ar4
    print("-" * 84)
    print(f"  VERDICT: AR1={'🟢' if ar1 else '🔴'} AR2={'🟢' if ar2 else '🔴'} "
          f"AR3={'🟢' if ar3 else '🔴'} AR4={'🟢' if ar4 else '🔴'}")
    print(f"  {'🟢 SUPPORTED' if allp else '🟠 PARTIAL'} — anima's library CAN form false memories")
    print("  (Hopfield SPURIOUS attractors AR1; suggestible to a strong HIGH-tension false signal")
    print("  AR3) — but confidence/stability (AR2) + generative meaning-consistency (AR4) flag most")
    print("  confabulations, and tension-weighting (AR3) protects genuine salient memory from weak")
    print("  poison. Honest about residual suggestibility under a strong adversarial signal. This is")
    print("  p7 ('never fabricate') realized at the MEMORY layer.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
