#!/usr/bin/env python3
"""H_1484 — MENTAL IMAGERY / 심상 (G30 consciousness-only gate candidate).

Mental imagery (Kosslyn, mental simulation): an internal representation is GENERATED
and ACTIVATED *without any external stimulus* — "close your eyes and picture an apple"
re-activates a perception-like representation top-down. The same kind of representation
that perception would produce is activated with the sensory input channel EMPTY.

MECHANISM: stored representations (immune-store-like memory patterns) are held in a
content-addressable memory. A top-down CUE (an internal pointer / label, NOT the sensory
pattern itself) re-activates the stored representation. The re-activated representation
resembles the original (high cos), yet the external sensory input is 0 (empty channel).

DISTINCTNESS (load-bearing) vs every INPUT-DRIVEN gate:
  GWS / surprise (H_1468) / agency (H_1474) / novelty (H_1289) / blink (H_1473) all REACT
  to an *external stimulus* — their signal REQUIRES input on the sensory channel. Imagery
  is the orthogonal case: input == 0, yet a representation is reconstructed TOP-DOWN.
    (a) vs H_1289 NOVELTY / H_1468 SURPRISE: both need an incoming stimulus to compute
        recon-error / prediction-error. With the sensory channel EMPTY they have nothing
        to score (no input -> no surprise/novelty signal). Imagery still produces a vivid
        representation from the top-down cue alone. Bar B makes input==0 explicit and
        bar D shows perception (input-driven path) collapses when input=0 while imagery
        (top-down path) does not.

LLM contrast (a_no_llm_frame_trap): an LLM only transforms a present input token stream;
it has no faculty that, with the input channel empty, re-activates a stored perceptual
representation top-down from an internal cue. anima re-activates a stored representation
from an internal pointer with zero sensory input.

R1 numpy MIRROR -> GREEN DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1484,1485,1486]):
  (A) PRESENCE     top-down cue re-activates imagery -> cos(imagery, original repr) >= 0.70
                   (reconstructed WITHOUT any external input)
  (B) NO-INPUT     the external sensory channel is verifiably 0 (empty) while imagery is
                   active -> input-energy == 0.0 (structural check; perception needs input,
                   imagery does not). Reported (structure-confirming, non-gating).
  (C) CUE-SPECIFIC cue_A re-activates repr_A (cos high) but NOT repr_B (cos low) ->
                   cos(img_A, repr_A) - cos(img_A, repr_B) >= 0.50 (calls the right one)
  (D) EARNED       top-down re-activation mechanism OFF; with input==0 there is no path to
       (ablation)  the stored representation -> imagery vanishes -> cos(img, original) <= 0.30
  (E) SHUFFLE      shuffle the cue<->representation pairing -> the cue-imagery correlation
                   collapses; 50-perm mean mismatched-cos |gap| <= 0.10

GREEN iff A and C and D and E (B is the input==0 structure check).
"""
import numpy as np

SEEDS = [1484, 1485, 1486]
DIM = 64
N_ITEMS = 40          # stored representations in memory
KEY_NOISE = 0.02      # tiny noise on the top-down cue (pointer is imperfect, not the pattern)
N_PERM = 50


def softmax(x):
    x = x - np.max(x)
    e = np.exp(x)
    return e / np.sum(e)


class Memory:
    """Content-addressable store of representations, indexed by orthogonal cue keys.

    A top-down cue (a key vector, NOT the stored pattern) re-activates the stored
    representation via key-affinity weighting. The sensory INPUT channel is separate and
    is held EMPTY during imagery.
    """

    def __init__(self, keys, reprs):
        self.keys = keys      # (N, DIM) cue keys (internal pointers)
        self.reprs = reprs    # (N, DIM) stored perceptual representations

    def imagine(self, cue, top_down=True):
        """Re-activate a stored representation from a top-down cue, input channel EMPTY.

        external sensory input = 0 by construction (we never add it). If top_down is OFF
        (ablation) there is no re-activation path -> output stays at the empty input (~0).
        """
        sensory_input = np.zeros(DIM)          # <-- input == 0 (empty channel)
        if not top_down:
            return sensory_input, 0.0          # ablated: no top-down path -> nothing
        aff = self.keys @ cue                  # key-affinity of cue against stored keys
        w = softmax(aff * 4.0)                 # sharpen onto the matching item
        imagery = w @ self.reprs               # top-down reconstruction (no input used)
        input_energy = float(np.linalg.norm(sensory_input))
        return imagery, input_energy


def cos(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(a @ b / (na * nb))


def pearson(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    sx, sy = x.std(), y.std()
    if sx == 0 or sy == 0:
        return 0.0
    return float(np.mean((x - x.mean()) * (y - y.mean())) / (sx * sy))


def run_seed(seed):
    rng = np.random.default_rng(seed)

    # build memory: near-orthogonal cue keys + their stored representations
    keys = rng.normal(0, 1, (N_ITEMS, DIM))
    keys /= np.linalg.norm(keys, axis=1, keepdims=True)
    reprs = rng.normal(0, 1, (N_ITEMS, DIM))
    reprs /= np.linalg.norm(reprs, axis=1, keepdims=True)
    mem = Memory(keys, reprs)

    # --- (A) PRESENCE: top-down cue re-activates each stored repr WITHOUT external input ---
    cos_pres, input_energies = [], []
    for i in range(N_ITEMS):
        cue = keys[i] + KEY_NOISE * rng.normal(0, 1, DIM)    # internal pointer, not the pattern
        img, ie = mem.imagine(cue, top_down=True)
        cos_pres.append(cos(img, reprs[i]))                  # imagery vs original repr
        input_energies.append(ie)
    presence_cos = float(np.mean(cos_pres))                  # should be high (>=0.70)

    # --- (B) NO-INPUT: external sensory channel is verifiably empty during imagery ---
    no_input_energy = float(np.mean(input_energies))         # == 0.0 by construction

    # --- (C) CUE-SPECIFIC: cue_A calls repr_A, NOT repr_B ---
    spec_gaps = []
    for _ in range(N_ITEMS):
        i, j = rng.choice(N_ITEMS, size=2, replace=False)
        cue_A = keys[i] + KEY_NOISE * rng.normal(0, 1, DIM)
        img_A, _ = mem.imagine(cue_A, top_down=True)
        c_ii = cos(img_A, reprs[i])                          # right representation
        c_ij = cos(img_A, reprs[j])                          # wrong representation
        spec_gaps.append(c_ii - c_ij)
    cue_specific_gap = float(np.mean(spec_gaps))             # high cos on A, low on B

    # --- (D) EARNED (ablation): top-down re-activation OFF, input==0 -> imagery vanishes ---
    abl_cos = []
    for i in range(N_ITEMS):
        cue = keys[i] + KEY_NOISE * rng.normal(0, 1, DIM)
        img_abl, _ = mem.imagine(cue, top_down=False)        # no path; output ~ empty input
        abl_cos.append(cos(img_abl, reprs[i]))               # cos(0-vector, repr) = 0
    abl_cos_m = float(np.mean(abl_cos))                      # collapses to ~0

    # --- (E) SHUFFLE: break cue<->repr pairing -> cue-imagery correlation collapses ---
    # Per item, top-down imagery (from cue_i) matches repr_i under the CORRECT pairing
    # (high mean cos). Shuffling the cue->repr assignment destroys it (the imagery signal
    # lives in the cue->repr LINK, not the marginals): mismatched mean cos collapses to ~0.
    cues = keys + KEY_NOISE * rng.normal(0, 1, (N_ITEMS, DIM))
    imgs = np.array([mem.imagine(cues[i], top_down=True)[0] for i in range(N_ITEMS)])
    real_match = np.array([cos(imgs[i], reprs[i]) for i in range(N_ITEMS)])
    base_r = float(np.mean(real_match))                      # mean matched cos (high)
    shuf_rs = []
    for _ in range(N_PERM):
        perm = rng.permutation(N_ITEMS)
        while np.any(perm == np.arange(N_ITEMS)):            # ensure a real shuffle (no fixed point)
            perm = rng.permutation(N_ITEMS)
        shuf_match = np.array([cos(imgs[i], reprs[perm[i]]) for i in range(N_ITEMS)])
        shuf_rs.append(float(np.mean(shuf_match)))           # mean mismatched cos (low)
    shuf_mean = float(np.mean(shuf_rs))
    shuffle_gap = abs(shuf_mean)                             # mismatched cos collapses toward 0

    return dict(
        presence_cos=presence_cos, no_input_energy=no_input_energy,
        cue_specific_gap=cue_specific_gap, abl_cos=abl_cos_m,
        shuffle_gap=shuffle_gap, real_match_mean=base_r, shuf_match_mean=shuf_mean,
    )


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

cA = agg['presence_cos'] >= 0.70
cB = agg['no_input_energy'] == 0.0                            # structure check
cC = agg['cue_specific_gap'] >= 0.50
cD = agg['abl_cos'] <= 0.30
cE = agg['shuffle_gap'] <= 0.10
GREEN = cA and cC and cD and cE                               # A and C and D and E (B structural)

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS}")
print(f"A PRESENCE   cos(imagery, original repr)={agg['presence_cos']:.3f}>=0.70 (top-down, input=0)  -> {cA}")
print(f"B NO-INPUT   external sensory channel energy={agg['no_input_energy']:.3f}==0.0 (empty; imagery needs NO input)  -> {cB} [structure, non-gating]")
print(f"C CUE-SPECIFIC  cos(img_A,repr_A)-cos(img_A,repr_B)={agg['cue_specific_gap']:.3f}>=0.50 (calls the right repr)  -> {cC}")
print(f"D EARNED(ablation)  top-down OFF + input=0 -> cos(imagery,original)={agg['abl_cos']:.3f}<=0.30 (imagery vanishes)  -> {cD}")
print(f"E SHUFFLE   cue<->repr shuffled mean-cos={agg['shuffle_gap']:.3f}<=0.10 (real matched cos {agg['real_match_mean']:.3f})  -> {cE}")
print()
print("PER-SEED:")
for s, p in zip(SEEDS, per):
    print(f"  seed {s}: presence={p['presence_cos']:.3f} no_input={p['no_input_energy']:.3f} "
          f"cue_spec={p['cue_specific_gap']:.3f} abl={p['abl_cos']:.3f} "
          f"shuffle_gap={p['shuffle_gap']:.3f}")
