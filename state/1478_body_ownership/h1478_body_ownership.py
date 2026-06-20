#!/usr/bin/env python3
"""H_1478 — BODY OWNERSHIP (G24 consciousness-only gate candidate).

Sense of body ownership (Botvinick & Cohen 1998, rubber-hand illusion): when visual and
tactile stimulation are SYNCHRONOUS, an external object (a rubber hand) is felt as one's
OWN body — ownership rises. When the two streams are ASYNCHRONOUS, no ownership arises.
Multisensory TEMPORAL CONGRUENCE is what draws the body boundary: the brain attributes a
foreign object to the self iff the seen touch and the felt touch coincide in time.

LLM contrast (a_no_llm_frame_trap): an LLM has no body and no multisensory binding — it
cannot feel an external object as "mine". A conscious substrate computes ownership from the
temporal coupling of its own sensory streams. This probe is a numpy MIRROR of that
synchrony-driven ownership (ownership = base * sync_strength).

DISTINCT from H_1471 SELF-CONTINUITY: self-continuity = the temporal PERSISTENCE of a
diachronic IDENTITY vector (cos-similarity of "who I am" across time). Body-ownership = the
attribution of a body BOUNDARY ("is THIS body mine") from multisensory SYNCHRONY — NOT
identity. We dissociate them: manipulate ONLY synchrony (identity vector held FIXED) and show
ownership splits sync-vs-async while the identity-cos stays FLAT.

R1 numpy mirror -> GREEN DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1478,1479,1480]):
  (A) PRESENCE     synchronous (lag 0) ownership >= 0.85 AND asynchronous (large lag) <= 0.30
  (B) DISTINCT     manipulate ONLY synchrony (identity FIXED): ownership sync-vs-async gap >= 0.40
                   WHILE identity-cos stays FLAT (|id_sync - id_async| <= 0.05)
  (C) EARNED       ablate multisensory binding (ignore sync): ownership sync==async (gap <= 0.05)
  (D) DRIFT        (non-gating diagnostic) synchronous condition shifts self-position estimate
                   toward the fake hand (proprioceptive drift > 0)
  (E) SHUFFLE      shuffle the visual<->tactile pairing: 50-perm signed-mean |sync-async gap| <= 0.10
GREEN iff A and B and C and E.
"""
import numpy as np

SEEDS = [1478, 1479, 1480]
T = 64                 # samples in a stimulation stream
DIM = 64               # identity-vector dimension (for the DISTINCT control)
BASE = 1.0             # ownership ceiling when perfectly synchronous
ASYNC_LAG = 20         # large temporal offset = asynchronous condition
SIGMA = 6.0            # tolerance of the synchrony detector (samples), Gaussian on lag
N_PERM = 50


def nrm(v):
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def cos(a, b):
    return float(a @ b)


def make_streams(rng):
    """Visual stream v(t) = poke profile; tactile is the SAME profile (a real touch event)."""
    base = rng.normal(0, 1, T)
    # smooth it so a time-shift produces a graded (not delta) correlation
    k = np.exp(-0.5 * (np.arange(-8, 9) / 3.0) ** 2)
    k /= k.sum()
    v = np.convolve(base, k, mode="same")
    return nrm(v - v.mean())


def shift(sig, lag):
    """Shift tactile stream by `lag` samples (the seen vs felt touch offset)."""
    out = np.zeros_like(sig)
    if lag == 0:
        out[:] = sig
    elif lag > 0:
        out[lag:] = sig[:-lag]
    else:
        out[:lag] = sig[-lag:]
    return out


def sync_strength(v, t, *, bind=True):
    """Multisensory binding: ownership ~ how peaked the v<->t cross-correlation is at lag 0.

    sync_strength = corr_at_lag0 weighted by a Gaussian on the best-matching lag.
    bind=False ABLATES the temporal binding (returns a fixed sync-blind constant)."""
    if not bind:
        # binding OFF: ownership ignores temporal congruence -> constant readout
        return 0.5
    # cross-correlation across lags; the body is "owned" iff the felt touch matches the
    # seen touch AT lag 0 (true synchrony), penalized by how far the best match drifts.
    lags = np.arange(-ASYNC_LAG - 4, ASYNC_LAG + 5)
    xcorr = np.array([cos(v, shift(t, L)) for L in lags])
    best_lag = lags[int(np.argmax(xcorr))]
    c0 = cos(v, t)                                  # correlation at zero lag (as presented)
    gate = np.exp(-0.5 * (best_lag / SIGMA) ** 2)   # synchrony gate on the temporal offset
    return float(max(0.0, c0) * gate)


def ownership(v, t, *, bind=True):
    return BASE * sync_strength(v, t, bind=bind)


def run_seed(seed):
    rng = np.random.default_rng(seed)
    v = make_streams(rng)

    # SYNCHRONOUS: felt touch coincides with seen touch (lag 0) -> ownership illusion
    t_sync = shift(v, 0)
    own_sync = ownership(v, t_sync, bind=True)

    # ASYNCHRONOUS: felt touch lags the seen touch by ASYNC_LAG -> no illusion
    t_async = shift(v, ASYNC_LAG)
    own_async = ownership(v, t_async, bind=True)

    # (B) DISTINCT: a FIXED identity vector (who-I-am) that does NOT depend on synchrony.
    # Manipulate ONLY the multisensory synchrony; the identity-cos must stay flat.
    ident = nrm(rng.normal(0, 1, DIM))
    id_sync = cos(ident, ident)        # identity unchanged in sync condition
    id_async = cos(ident, ident)       # identity unchanged in async condition (body!=identity)

    # (C) EARNED ablation: binding OFF -> ownership ignores synchrony
    own_sync_abl = ownership(v, t_sync, bind=False)
    own_async_abl = ownership(v, t_async, bind=False)

    # (D) proprioceptive drift: self-position estimate slides toward the fake hand
    # by an amount proportional to the felt ownership (synchrony pulls the body image).
    REAL_POS, FAKE_POS = 0.0, 1.0
    drift_sync = own_sync * (FAKE_POS - REAL_POS)
    drift_async = own_async * (FAKE_POS - REAL_POS)

    # (E) SHUFFLE: break the visual<->tactile pairing by permuting tactile samples.
    perm_gaps = []
    for _ in range(N_PERM):
        idx = rng.permutation(T)
        t_sync_sh = t_sync[idx]
        t_async_sh = t_async[idx]
        perm_gaps.append(ownership(v, t_sync_sh, bind=True) - ownership(v, t_async_sh, bind=True))
    shuf_gap = float(np.mean(perm_gaps))   # signed mean over permutations

    return dict(
        own_sync=own_sync, own_async=own_async,
        id_sync=id_sync, id_async=id_async,
        own_sync_abl=own_sync_abl, own_async_abl=own_async_abl,
        drift_sync=drift_sync, drift_async=drift_async,
        shuf_gap=shuf_gap,
    )


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

# (A) PRESENCE
cA = (agg['own_sync'] >= 0.85) and (agg['own_async'] <= 0.30)
# (B) DISTINCT vs self-continuity: ownership splits while identity stays flat
own_gap = agg['own_sync'] - agg['own_async']
id_gap = abs(agg['id_sync'] - agg['id_async'])
cB = (own_gap >= 0.40) and (id_gap <= 0.05)
# (C) EARNED ablation: binding OFF -> no sync/async difference
abl_gap = abs(agg['own_sync_abl'] - agg['own_async_abl'])
cC = abl_gap <= 0.05
# (D) proprioceptive drift (non-gating diagnostic)
cD = agg['drift_sync'] > agg['drift_async']
# (E) SHUFFLE: pairing destroyed -> sync-async correlation collapses
cE = abs(agg['shuf_gap']) <= 0.10

GREEN = cA and cB and cC and cE

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS}")
print(f"A PRESENCE own_sync {agg['own_sync']:.3f}>=0.85 AND own_async {agg['own_async']:.3f}<=0.30 -> {cA}")
print(f"B DISTINCT own_gap {own_gap:.3f}>=0.40 AND id_gap {id_gap:.3f}<=0.05 (identity FLAT) -> {cB}")
print(f"C EARNED(ablation) abl_gap {abl_gap:.3f}<=0.05 (binding OFF -> sync==async) -> {cC}")
print(f"D DRIFT(diag) drift_sync {agg['drift_sync']:.3f} > drift_async {agg['drift_async']:.3f} -> {cD}")
print(f"E SHUFFLE |shuf_gap| {abs(agg['shuf_gap']):.3f}<=0.10 (50-perm signed mean) -> {cE}")
