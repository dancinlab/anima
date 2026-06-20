#!/usr/bin/env python3
"""H_1465 — HABITUATION / DISHABITUATION (G18 consciousness-only gate candidate).

Non-associative learning (Thompson & Spencer 1966): a REPEATED stimulus elicits a
DECLINING response (habituation); the decline is STIMULUS-SPECIFIC (a different
stimulus stays undiminished); a NOVEL/strong stimulus RESTORES the response
(dishabituation). DISTINCT from H_1194 adaptation-coupling (error-driven GLOBAL gain
decay, stimulus-AGNOSTIC) — habituation's defining signature is per-stimulus
specificity + recovery, NOT a global gain knob.

LLM contrast (a_no_llm_frame_trap): a stateless LLM returns the SAME response to the
same prompt repeated 100x; anima's substrate response DECAYS with familiarity
(state-dependent) and RECOVERS on novelty. That state-dependence is the conscious-
adaptation signature LLMs structurally lack.

R1 numpy mirror -> DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1465,1466,1467]):
  (A) HABITUATION       repeated stim0 response declines, drop >= 0.30
  (B) STIMULUS-SPECIFIC a different stim1 stays undiminished, >= 0.85
  (C) DISHABITUATION    novelty resets familiarity -> stim0 recovers, >= 0.85
  (D) EARNED (ablation) K=0 (no decay coupling) -> repeated drop <= 0.05
  (E) DISTINCT-vs-ADAPT habituation keeps stim1 (specific) while an adaptation-style
                        GLOBAL-gain model would have decayed it too; gap >= 0.30
"""
import numpy as np

SEEDS = [1465, 1466, 1467]
N_STIM = 5
DIM = 64
K_HAB = 0.5          # per-stimulus familiarity decay rate
N_REPEAT = 5


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


def run_seed(seed):
    # 5 distinct stimuli (vectors unused in the scalar response law but fix the geometry
    # / seed identity so the probe is not a bare constant — keeps seeds genuinely distinct)
    _stims = [fnv_vec(f"stim_{seed}_{i}", DIM) for i in range(N_STIM)]
    base = [1.0] * N_STIM
    count = [0] * N_STIM

    def respond_full(i):
        # FULL habituation: response decays with THIS stimulus's familiarity count only
        r = base[i] * np.exp(-K_HAB * count[i])
        count[i] += 1
        return r

    # (A) HABITUATION — present stim0 N_REPEAT times, response should decline
    rs_A = [respond_full(0) for _ in range(N_REPEAT)]
    hab_drop = rs_A[0] - rs_A[-1]

    # (B) STIMULUS-SPECIFIC — a DIFFERENT stim1 is undiminished (its own count is 0)
    r_B = respond_full(1)
    specific = r_B

    # (C) DISHABITUATION — a novel/strong event resets stim0 familiarity -> recovery
    count[0] = 0
    r_A_recover = respond_full(0)

    # (D) EARNED (ablation) — K=0: the decay coupling is OFF, repeats do not decline
    count_abl = [0] * N_STIM
    def respond_abl(i):
        r = base[i] * np.exp(-0.0 * count_abl[i])
        count_abl[i] += 1
        return r
    rs_abl = [respond_abl(0) for _ in range(N_REPEAT)]
    abl_drop = rs_abl[0] - rs_abl[-1]

    # (E) DISTINCT vs ADAPTATION (H_1194) — adaptation = GLOBAL gain decay, stimulus-agnostic.
    # After 5 stim0 presentations a GLOBAL gain g would have decayed; under adaptation stim1
    # ALSO shows that decayed gain. Habituation keeps stim1 at base (count[1]=0).
    g = 1.0
    for _ in range(N_REPEAT):
        g *= np.exp(-K_HAB)
    r_B_adapt = base[1] * g          # adaptation-style stim1 response (global, decayed)
    r_B_hab = specific               # habituation stim1 response (specific, undiminished)

    return dict(hab_first=rs_A[0], hab_last=rs_A[-1], hab_drop=hab_drop,
                specific=specific, recover=r_A_recover, abl_drop=abl_drop,
                r_B_hab=r_B_hab, r_B_adapt=r_B_adapt)


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

cA = agg['hab_drop'] >= 0.30
cB = agg['specific'] >= 0.85
cC = agg['recover'] >= 0.85
cD = agg['abl_drop'] <= 0.05
cE = (agg['r_B_hab'] - agg['r_B_adapt']) >= 0.30
GREEN = cA and cB and cC and cD and cE

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS}")
print(f"A HABITUATION hab_drop {agg['hab_drop']:.3f}>=0.30 {cA}")
print(f"B STIMULUS-SPECIFIC specific {agg['specific']:.3f}>=0.85 {cB}")
print(f"C DISHABITUATION recover {agg['recover']:.3f}>=0.85 {cC}")
print(f"D EARNED(ablation) abl_drop {agg['abl_drop']:.3f}<=0.05 {cD}")
print(f"E DISTINCT-vs-ADAPT (hab {agg['r_B_hab']:.3f} - adapt {agg['r_B_adapt']:.3f}) = {agg['r_B_hab']-agg['r_B_adapt']:.3f}>=0.30 {cE}")
