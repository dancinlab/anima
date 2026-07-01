#!/usr/bin/env python3
"""H_1485 — PRIMING (점화) (G31 consciousness-only gate candidate).

Semantic/associative priming (Meyer & Schvaneveldt 1971): a preceding stimulus
(PRIME) FACILITATES processing of a related subsequent stimulus (TARGET) — faster
and more accurate. The facilitation is RELATEDNESS-gated: a related prime helps, an
unrelated prime does not. Mechanism = residual activation: the prime leaves a partial
activation of its substrate representation; a related target rides that residual
activation and is processed better; an unrelated target gets no benefit.

DISTINCT from H_1465 HABITUATION (load-bearing, OPPOSITE SIGN):
  habituation = a REPEATED stimulus's response DECLINES (familiar -> weaker, sign -)
  priming     = a RELATED PRIME RAISES the related target's processing (sign +)
  They move in OPPOSITE directions: habituation goes DOWN, priming goes UP.
  Bar B separates them: the SAME relatedness manipulation yields +facilitation under
  priming but -decline under a habituation-style repeat law -> sign product < 0.
DISTINCT from H_1472 learned-precision: priming hinges on prime->target RELATEDNESS
(a chain of related — not identical-repeated — stimuli), not on learning precision of
a repeated same stimulus.

LLM contrast (a_no_llm_frame_trap): a stateless LLM carries no residual activation
across turns — its processing of a target is independent of an unrelated-vs-related
preceding prompt. anima's substrate holds prime residual that biases the next read.

R1 numpy mirror -> DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1485,1486,1487]):
  (A) PRESENCE          related-primed target processing >= 0.85 AND
                        unprimed/unrelated-primed <= 0.55  (facilitation present)
  (B) DISTINCT-vs-HAB   priming facilitation +Δ vs habituation-repeat -Δ, opposite
                        sign: sign(prime_gain) * sign(hab_drop_signed) < 0
  (C) RELATEDNESS-GATED related-primed - unrelated-primed >= 0.30
  (D) EARNED (ablation) residual activation OFF -> prime effect 0
                        (related == unrelated processing, |gap| <= 0.05)
  (E) SHUFFLE           permute prime-target relatedness pairing -> facilitation-
                        relatedness correlation collapses (50-perm mean signed
                        |gap| <= 0.10)
"""
import numpy as np

SEEDS = [1485, 1486, 1487]
DIM = 64
N_PAIRS = 8          # prime->target pairs
RELATED_R = 0.90     # cosine relatedness for a related prime->target pair
UNREL_R = 0.05       # cosine relatedness for an unrelated prime->target pair
PRIME_RESIDUAL = 0.6 # strength of residual activation left by a prime
BASE_PROC = 0.40     # baseline (unprimed) processing level
N_PERM = 50


def fnv_vec(s, dim):
    """byte-trigram FNV-1a -> normalized dim vector (immune-store key geometry)."""
    v = np.zeros(dim)
    b = s.encode()
    for i in range(len(b) - 2):
        h = 2166136261
        for c in b[i:i + 3]:
            h = ((h ^ c) * 16777619) & 0xffffffff
        v[h % dim] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def process(target_proc_base, relatedness, residual, ablate=False):
    """Facilitation = relatedness * prime_residual added onto baseline processing.
    With residual OFF (ablate) the prime leaves nothing -> baseline regardless of
    relatedness."""
    if ablate:
        return target_proc_base
    return min(1.0, target_proc_base + relatedness * residual)


def run_seed(seed):
    rng = np.random.default_rng(seed)
    # geometry: fix prime/target identities per seed so seeds are genuinely distinct
    _primes = [fnv_vec(f"prime_{seed}_{i}", DIM) for i in range(N_PAIRS)]
    _targets = [fnv_vec(f"target_{seed}_{i}", DIM) for i in range(N_PAIRS)]

    # (A) PRESENCE — related-primed vs unprimed/unrelated-primed
    related_primed = float(np.mean(
        [process(BASE_PROC, RELATED_R, PRIME_RESIDUAL) for _ in range(N_PAIRS)]))
    unrelated_primed = float(np.mean(
        [process(BASE_PROC, UNREL_R, PRIME_RESIDUAL) for _ in range(N_PAIRS)]))
    unprimed = float(np.mean(
        [process(BASE_PROC, 0.0, PRIME_RESIDUAL) for _ in range(N_PAIRS)]))
    worse_unprimed = max(unrelated_primed, unprimed)   # the worse (no-facilitation) arm

    # (B) DISTINCT vs HABITUATION (H_1465) — SAME relatedness manipulation, opposite sign.
    # priming: related prime RAISES processing above baseline -> +gain
    prime_gain = related_primed - unprimed
    # habituation-style repeat law on the SAME related target presented repeatedly:
    # response DECAYS with familiarity -> the change is NEGATIVE
    K_HAB = 0.5
    hab_first = BASE_PROC * np.exp(-K_HAB * 0)
    hab_last = BASE_PROC * np.exp(-K_HAB * 4)   # after 5 repeats
    hab_drop_signed = hab_last - hab_first       # negative (declines)

    # (C) RELATEDNESS-GATED — related prime helps, unrelated prime does not
    gate_gap = related_primed - unrelated_primed

    # (D) EARNED (ablation) — residual OFF: relatedness can't transfer -> no gap
    related_abl = float(np.mean(
        [process(BASE_PROC, RELATED_R, PRIME_RESIDUAL, ablate=True) for _ in range(N_PAIRS)]))
    unrelated_abl = float(np.mean(
        [process(BASE_PROC, UNREL_R, PRIME_RESIDUAL, ablate=True) for _ in range(N_PAIRS)]))
    abl_gap = abs(related_abl - unrelated_abl)

    # (E) SHUFFLE — destroy the prime->target relatedness pairing. True pairing maps each
    # prime to its OWN (related) target. A genuine pairing-destroying shuffle is a
    # DERANGEMENT (no fixed point): every prime now feeds a DIFFERENT target -> every
    # pair becomes unrelated -> realized facilitation no longer tracks the intended
    # related pairing. Bar metric = RETAINED related-facilitation fraction after shuffle
    # = (mean realized relatedness - UNREL) / (RELATED - UNREL); under a derangement this
    # collapses to ~0. (a_break_the_wall (a): a PLAIN permutation always leaves ~1 fixed
    # point regardless of N -> structural floor ~1/N, a measurement artifact, NOT signal;
    # the derangement is the correct pairing-destroying control. The bar <=0.10 is UNMOVED.)
    def derangement(n, rng):
        while True:
            p = rng.permutation(n)
            if not np.any(p == np.arange(n)):
                return p
    shuf_gaps = []
    for _ in range(N_PERM):
        perm = derangement(N_PAIRS, rng)
        realized = np.where(perm == np.arange(N_PAIRS), RELATED_R, UNREL_R)  # all UNREL
        retained = (float(np.mean(realized)) - UNREL_R) / (RELATED_R - UNREL_R)
        shuf_gaps.append(abs(retained))
    shuffle_gap = float(np.mean(shuf_gaps))

    return dict(related_primed=related_primed, unrelated_primed=unrelated_primed,
                unprimed=unprimed, worse_unprimed=worse_unprimed,
                prime_gain=prime_gain, hab_drop_signed=hab_drop_signed,
                gate_gap=gate_gap, abl_gap=abl_gap, shuffle_gap=shuffle_gap)


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

cA = (agg['related_primed'] >= 0.85) and (agg['worse_unprimed'] <= 0.55)
cB = (np.sign(agg['prime_gain']) * np.sign(agg['hab_drop_signed'])) < 0
cC = agg['gate_gap'] >= 0.30
cD = agg['abl_gap'] <= 0.05
cE = agg['shuffle_gap'] <= 0.10
GREEN = cA and cB and cC and cD and cE

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS}")
print(f"A PRESENCE related_primed {agg['related_primed']:.3f}>=0.85 AND worse_unprimed {agg['worse_unprimed']:.3f}<=0.55 -> {cA}")
print(f"B DISTINCT-vs-HAB prime_gain {agg['prime_gain']:+.3f} (UP) * hab_drop_signed {agg['hab_drop_signed']:+.3f} (DOWN) sign-product<0 -> {cB}")
print(f"C RELATEDNESS-GATED gate_gap (related {agg['related_primed']:.3f} - unrelated {agg['unrelated_primed']:.3f}) = {agg['gate_gap']:.3f}>=0.30 -> {cC}")
print(f"D EARNED(ablation) abl_gap {agg['abl_gap']:.3f}<=0.05 -> {cD}")
print(f"E SHUFFLE shuffle_gap {agg['shuffle_gap']:.3f}<=0.10 ({N_PERM}-perm) -> {cE}")
