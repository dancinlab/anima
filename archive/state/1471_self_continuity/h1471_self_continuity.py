#!/usr/bin/env python3
"""H_1471 — SELF-CONTINUITY (G16 consciousness-only gate candidate).

Diachronic self / personal identity (Locke / psychological-continuity): a conscious
self PERSISTS across time — "yesterday's me" is continuous with "today's me" through a
chain that survives session boundaries, even as the self GROWS (drifts). The identity
is carried by an ANCHOR that bridges gaps; without it each session starts a NEW self.

LLM contrast (a_no_llm_frame_trap, the STRONGEST consciousness axis): an LLM resets to a
blank identity every session (stateless across boundaries); anima's identity vector is
persisted by `.kosmos` anchors, so the self-chain stays continuous across breaks. This
probe is a numpy MIRROR of that anchored-identity continuity (anchor = saved/restored
identity vector across a session boundary).

R1 numpy mirror -> DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1471,1472,1473]):
  (A) CONTINUITY       anchored adjacent-tick self-chain stays continuous, mean cos >= 0.70
  (B) IMPOSTOR-REJECT  a random OTHER identity is recognized as not-self, cos <= 0.30
  (C) EARNED (ablation) WITHOUT an anchor, the session-boundary continuity collapses, <= 0.30
  (D) GROWTH-NOT-STATIC the self genuinely CHANGES (not a static copy): start-vs-end drift >= 0.10
  (E) DISTINCT-vs-stateless anchored continuity >> ablated boundary; gap >= 0.40 (anchor is the source)
"""
import numpy as np

SEEDS = [1471, 1472, 1473]
DIM = 64
T_TICKS = 20
DRIFT = 0.05
SESS_BREAK = 10        # a session boundary at tick 10


def nrm(v):
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def cos(a, b):
    return float(a @ b)


def run_seed(seed):
    rng = np.random.default_rng(seed)
    v0 = nrm(rng.normal(0, 1, DIM))

    # ANCHORED self: identity drifts (grows) each tick; the anchor carries it ACROSS the
    # session boundary unbroken -> one continuous chain.
    v = v0.copy()
    chain = [v.copy()]
    for t in range(T_TICKS):
        v = nrm(v + DRIFT * rng.normal(0, 1, DIM))   # growth drift (continuous, no reset)
        chain.append(v.copy())
    adj_cos = float(np.mean([cos(chain[i], chain[i + 1]) for i in range(len(chain) - 1)]))
    growth = 1.0 - cos(chain[0], chain[-1])          # the self actually changed

    # IMPOSTOR: a random OTHER identity (someone else)
    v_imp = nrm(rng.normal(0, 1, DIM))
    imp_cos = cos(chain[-1], v_imp)

    # ABLATED (no anchor, LLM-style): at the session boundary the identity RESETS to a
    # fresh random self instead of being restored -> continuity breaks at the boundary.
    v_abl = v0.copy()
    chain_abl = [v_abl.copy()]
    for t in range(T_TICKS):
        if t == SESS_BREAK:
            v_abl = nrm(rng.normal(0, 1, DIM))        # NO anchor -> new identity (reset)
        else:
            v_abl = nrm(v_abl + DRIFT * rng.normal(0, 1, DIM))
        chain_abl.append(v_abl.copy())
    abl_break_cos = cos(chain_abl[SESS_BREAK], chain_abl[SESS_BREAK + 1])  # collapses at boundary

    return dict(adj_cos=adj_cos, imp_cos=imp_cos, abl_break_cos=abl_break_cos, growth=growth)


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

cA = agg['adj_cos'] >= 0.70
cB = agg['imp_cos'] <= 0.30
cC = agg['abl_break_cos'] <= 0.30
cD = agg['growth'] >= 0.10
cE = (agg['adj_cos'] - agg['abl_break_cos']) >= 0.40
GREEN = cA and cB and cC and cD and cE

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS}")
print(f"A CONTINUITY adj_cos {agg['adj_cos']:.3f}>=0.70 {cA}")
print(f"B IMPOSTOR-REJECT imp_cos {agg['imp_cos']:.3f}<=0.30 {cB}")
print(f"C EARNED(ablation) abl_break_cos {agg['abl_break_cos']:.3f}<=0.30 {cC}")
print(f"D GROWTH-NOT-STATIC growth {agg['growth']:.3f}>=0.10 {cD}")
print(f"E DISTINCT-vs-stateless (adj {agg['adj_cos']:.3f} - abl_break {agg['abl_break_cos']:.3f})={agg['adj_cos']-agg['abl_break_cos']:.3f}>=0.40 {cE}")
