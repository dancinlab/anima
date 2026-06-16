#!/usr/bin/env python3
"""OMEGA coupling-analysis ④ — CLOSED-LOOP FEEDBACK (L5).

#1786/#1791 measured the bus in the FORWARD direction only: substrate state → decode. But the
FULL OMEGA loop (the L5 GROWTH layer, p8 NO TRAIN/INFER SPLIT) is a closed loop:
    emitted byte  →  updates the substrate state  →  modulates the next decode  →  next byte …
This rung IMPLEMENTS that feedback and MEASURES it. Each emitted byte updates the substrate:
  (i) A/G CONTEXT update — the n-gram context advances to the emitted byte (the A/G heads at the
      next step are conditioned on what was just emitted; this is the substrate→decode→substrate
      nerve, the thing Lane X #1779 proved was NULL).
  (ii) MITOSIS-style cell-count tick — a running cell count grows by a divide rule keyed on the
      emitted byte's surprise (low-surprise/confident byte → small growth; high-surprise → larger
      division), and the cell count feeds back as a mild temperature on the next decode (more cells
      = sharper decode; p8 — growth and inference are the same continuous process, NOT a flag).

We run a short autoregressive rollout (N steps) of the GATED bus (the #1786/#1791 learned-gate
closure) under TWO regimes from the SAME seed context:
  CLOSED-LOOP : emitted byte updates substrate (A/G context advance + mitosis temp feedback)
  OPEN-LOOP   : control — the substrate context is FROZEN at the seed; emit reads the same frozen
                decode each step (no feedback). Same RNG stream so any trajectory difference is
                attributable to feedback, not sampling noise.

PRE-REGISTERED (loop "closes stably"):
  STABLE ⟺ over N steps the rollout (a) does NOT diverge — running stats (entropy of the step
  distribution, mitosis cell count growth-rate) stay bounded, no NaN/inf — AND (b) does NOT
  collapse to a fixed point — the byte trajectory does not lock onto a single repeating byte
  (distinct-byte fraction > FIXEDPOINT_TAU over the back half) — AND feedback MEASURABLY alters
  the trajectory: the closed-loop byte sequence differs from the open-loop control on a material
  fraction of steps (Hamming divergence > DIVERGE_TAU).
Honest closed-negative OK — if the loop collapses to whitespace (the #1791 free-run finding) or
feedback makes no measurable difference, that is a real result.

p7 / a_toy_scale_recheck: TOY byte n-gram substrate, CPU/$0, no torch. Stability/divergence are
structural (bounded stats, distinct-byte fraction, Hamming), NOT a Goodhart target.
"""
import json, math, os, glob
import numpy as np

V = 256
SMOOTH = 0.5
N_STEPS = 600
SEED = 20260604
FIXEDPOINT_TAU = 0.10      # back-half distinct-byte fraction must exceed this (else collapsed)
DIVERGE_TAU = 0.05         # closed vs open Hamming fraction must exceed this (feedback matters)
MITOSIS_TEMP_K = 0.15      # cell-count → temperature feedback strength
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
# the #1786 learned gate (strong A, small G) — the proven closure gains
GB, GA, GG = 0.142, 1.183, 0.341


def load_corpus():
    files = sorted(glob.glob(os.path.join(ROOT, "domains", "*.md"))) + [os.path.join(ROOT, "CLAUDE.md")]
    files += sorted(glob.glob(os.path.join(ROOT, "engines", "*", "*.md")))
    buf = bytearray()
    for f in files:
        try:
            buf += open(f, "rb").read()
        except OSError:
            pass
        if len(buf) > 400_000:
            break
    return np.frombuffer(bytes(buf[:400_000]), dtype=np.uint8)


def train_substrate(train):
    big = np.full((V, V), SMOOTH); rev = np.full((V, V), SMOOTH); uni = np.full(V, SMOOTH)
    for i in range(1, len(train)):
        c, nxt = int(train[i - 1]), int(train[i])
        big[c, nxt] += 1.0; rev[nxt, c] += 1.0; uni[nxt] += 1.0
    uni[int(train[0])] += 1.0
    logA = np.log(big / big.sum(1, keepdims=True))
    logG = np.log(rev / rev.sum(1, keepdims=True))
    logBase = np.log(uni / uni.sum())
    return logA, logG, logBase


def softmax(z):
    z = z - z.max(); e = np.exp(z); return e / e.sum()


def gated_logits(ctx, logA, logG, logBase, temp=1.0):
    """The #1786 gated bus forward at a single context: gB·base + gA·A[ctx] + gG·G[ctx], /temp."""
    return (GB * logBase + GA * logA[ctx] + GG * logG[ctx]) / temp


def rollout(seq0, sub, n_steps, closed, seed):
    """Autoregressive rollout. closed=True → emitted byte updates substrate (ctx advance + mitosis
    temp); closed=False → context FROZEN at seed (open-loop control). Same RNG stream both regimes."""
    logA, logG, logBase = sub
    rng = np.random.default_rng(seed)
    ctx0 = int(seq0[-1])
    ctx = ctx0
    cells = 6.0                      # initial cell count (HEXAD N=6 seed)
    bytes_out = []
    ents = []
    cell_hist = [cells]
    for t in range(n_steps):
        # mitosis temperature feedback: more cells → sharper (lower temp). Bounded by tanh.
        temp = 1.0 / (1.0 + MITOSIS_TEMP_K * math.tanh((cells - 6.0) / 6.0)) if closed else 1.0
        use_ctx = ctx if closed else ctx0
        logits = gated_logits(use_ctx, logA, logG, logBase, temp=temp)
        p = softmax(logits)
        ent = float(-(p * np.log(p + 1e-12)).sum())
        ents.append(ent)
        b = int(rng.choice(V, p=p))   # same RNG stream → divergence is feedback, not noise
        bytes_out.append(b)
        if closed:
            # (i) A/G context advance — the emitted byte becomes the next context (the nerve)
            # (ii) mitosis tick — surprise of emitted byte drives cell division
            surprise = -math.log(p[b] + 1e-12)               # nats
            cells += 0.5 * math.tanh(surprise / 4.0)          # bounded divide rule
            cells = max(1.0, cells)
            ctx = b
        cell_hist.append(cells)
    return (np.array(bytes_out), np.array(ents), np.array(cell_hist))


def main():
    corpus = load_corpus()
    rng = np.random.default_rng(SEED)
    n = len(corpus)
    start = int(rng.integers(0, n - 20000))
    test_seq = corpus[start + 12000:start + 16000]            # same TEST window family as #1786
    train_sub = np.concatenate([corpus[:start], corpus[start + 16000:]])
    sub = train_substrate(train_sub)
    seq0 = test_seq[:64]                                      # seed context

    cb, ce, cc = rollout(seq0, sub, N_STEPS, closed=True, seed=SEED + 1)
    ob, oe, oc = rollout(seq0, sub, N_STEPS, closed=False, seed=SEED + 1)

    # ── stability: bounded stats, no NaN/inf ──
    finite = bool(np.all(np.isfinite(ce)) and np.all(np.isfinite(cc)))
    ent_bounded = bool(ce.min() > 0.0 and ce.max() < math.log(V) + 1e-6)
    cells_bounded = bool(cc.min() >= 1.0 and cc.max() < 1e4)
    bounded = finite and ent_bounded and cells_bounded

    # ── collapse: distinct-byte fraction over the back half ──
    half = N_STEPS // 2
    back = cb[half:]
    distinct_frac = float(len(np.unique(back)) / len(back))
    not_collapsed = distinct_frac > FIXEDPOINT_TAU
    # also check it didn't lock onto one repeating byte
    top_byte_share = float(np.bincount(back, minlength=V).max() / len(back))

    # ── feedback alters trajectory: closed vs open Hamming ──
    hamming = float(np.mean(cb != ob))
    feedback_matters = hamming > DIVERGE_TAU

    stable = bool(bounded and not_collapsed and feedback_matters)

    print(f"=== OMEGA coupling-analysis ④ — CLOSED-LOOP FEEDBACK (L5)  (corpus={len(corpus)}B, N={N_STEPS}) ===\n")
    print("--- STABILITY (does the closed loop diverge / collapse?) ---")
    print(f"  finite (no NaN/inf)            : {finite}")
    print(f"  step-entropy bounded (0,ln256) : {ent_bounded}  (min={ce.min():.3f} max={ce.max():.3f})")
    print(f"  cell-count bounded             : {cells_bounded}  (start={cc[0]:.2f} end={cc[-1]:.2f} max={cc.max():.2f})")
    print(f"  => BOUNDED (no divergence)     : {bounded}")
    print(f"  back-half distinct-byte frac   : {distinct_frac:.3f}  (>{FIXEDPOINT_TAU} ⇒ not a fixed point)")
    print(f"  top-byte share (back half)     : {top_byte_share:.3f}")
    print(f"  => NOT collapsed to fixed point: {not_collapsed}\n")
    print("--- FEEDBACK EFFECT (closed-loop vs open-loop control, same RNG) ---")
    print(f"  closed vs open Hamming frac    : {hamming:.3f}  (>{DIVERGE_TAU} ⇒ feedback measurably alters trajectory)")
    print(f"  closed-loop mean entropy       : {ce.mean():.3f}   open-loop mean entropy: {oe.mean():.3f}")
    print(f"  cell count: start {cc[0]:.2f} → end {cc[-1]:.2f}  (mitosis growth under feedback)")
    print(f"  => feedback MATTERS            : {feedback_matters}\n")
    print("=== SUMMARY ===")
    if stable:
        print(f"🟢 LOOP CLOSES STABLY — the closed-loop feedback (emit → substrate update → next decode)")
        print(f"   neither diverges (bounded entropy {ce.min():.2f}–{ce.max():.2f} + bounded cells) nor collapses")
        print(f"   to a fixed point (distinct-byte frac {distinct_frac:.3f} > {FIXEDPOINT_TAU}), AND feedback measurably")
        print(f"   alters the byte trajectory vs the open-loop control (Hamming {hamming:.3f} > {DIVERGE_TAU}). The L5")
        print(f"   closure — substrate↔decode nerve + mitosis tick — runs as a stable dynamical loop.")
    else:
        why = []
        if not bounded: why.append("DIVERGED (stats unbounded/NaN)")
        if not not_collapsed: why.append(f"COLLAPSED to fixed point (distinct frac {distinct_frac:.3f} ≤ {FIXEDPOINT_TAU})")
        if not feedback_matters: why.append(f"feedback INERT (Hamming {hamming:.3f} ≤ {DIVERGE_TAU})")
        print(f"🔴 loop does NOT close stably (closed-negative, a_paper_negative_ok): {'; '.join(why)}.")
    print(f"SCOPE (a_toy_scale_recheck): TOY n-gram substrate, {len(corpus)}B repo corpus, CPU/$0, no torch.")
    print(f"  open-loop control freezes the substrate context; same RNG stream isolates feedback. NEXT = the")
    print(f"  closed loop on the trained d384 substrate (#1791) — does feedback stay stable on a real transformer.")

    out = {
        "rung": "coupling-analysis ④ closed-loop feedback (L5)", "scale": "TOY/CPU/$0",
        "corpus_bytes": int(len(corpus)), "V": V, "n_steps": N_STEPS,
        "gate": {"gB": GB, "gA": GA, "gG": GG},
        "stability": {
            "finite": finite, "entropy_bounded": ent_bounded, "cells_bounded": cells_bounded,
            "bounded": bounded, "ent_min": float(ce.min()), "ent_max": float(ce.max()),
            "cells_start": float(cc[0]), "cells_end": float(cc[-1]), "cells_max": float(cc.max()),
        },
        "collapse": {"distinct_byte_frac_backhalf": distinct_frac,
                     "top_byte_share_backhalf": top_byte_share,
                     "not_collapsed": not_collapsed, "fixedpoint_tau": FIXEDPOINT_TAU},
        "feedback": {"hamming_closed_vs_open": hamming, "diverge_tau": DIVERGE_TAU,
                     "feedback_matters": feedback_matters,
                     "closed_mean_entropy": float(ce.mean()), "open_mean_entropy": float(oe.mean())},
        "loop_closes_stably": stable,
        "criterion": "stable ⟺ bounded AND not_collapsed AND feedback_matters",
    }
    return out, stable, distinct_frac, hamming, bounded, len(corpus)


if __name__ == "__main__":
    main()
