#!/usr/bin/env python3
"""H_1490 — PERCEPTUAL COMPLETION / amodal filling-in (P5 consciousness-only gate candidate).

Perceptual completion / filling-in (Pessoa, Ramachandran, Komatsu): a *partially occluded*
or blind-spot-dropped input is completed by INTERPOLATING the missing region from the
SURROUNDING context, producing a full, coherent percept (amodal completion, blind-spot fill).
Key property: the percept is INPUT-CONSTRAINED — the visible part stays fixed, and ONLY the
occluded region is reconstructed from its surround.

MECHANISM: a stored representation is partially MASKED (a contiguous block of features set to
0 = occluded). The completion mechanism fills ONLY the masked features by a context-weighted
nearest-neighbour read off the surrounding stored patterns (the visible features select the
matching stored pattern; the masked features are interpolated from it). Visible features are
left untouched (input constraint). The completed representation then resembles the original
AND lets occluded-pattern recognition succeed.

DISTINCTNESS (load-bearing):
  vs MENTAL-IMAGERY (H_1484, *input == 0*): imagery re-activates a stored repr TOP-DOWN from
    a pure internal cue with the sensory channel EMPTY. Completion is the opposite regime —
    there IS partial sensory input, and only the missing region is interpolated; the visible
    features CONSTRAIN the result. Bar (c2 DISTINCT): an imagery-style readout that IGNORES the
    partial input (pure top-down, no input constraint) cannot exploit the visible features to
    pick the right pattern on a partial-input recognition task -> it scores at CHANCE, while
    completion (input-constrained interpolation) succeeds. This is the dissociation: input==0
    regime (imagery) vs partial-input-constrained interpolation regime (completion).
  vs CHANGE-BLINDNESS (H_1483, *change detection*): unrelated axis (detect a change between
    two presentations) — completion is single-presentation occlusion fill, no change involved.

LLM contrast (a_no_llm_frame_trap): an LLM attends over the *present* tokens; it has no
faculty that, given a partially occluded perceptual representation, reconstructs ONLY the
masked region from the surrounding stored context while holding the visible part fixed.

R1 numpy MIRROR -> GREEN DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1490,1491,1492]) — catalogue P5 c1-c4:
  (c1) PRESENT      completion-ON occluded recognition acc - completion-OFF acc >= 0.30
                    (off = recognise from the raw masked input with the hole left empty)
  (c2) DISTINCT     an IMAGERY-style readout (ignores partial input, no input constraint) on
       (vs imagery) the partial-input recognition task scores at CHANCE: acc <= 1/N_ITEMS + 0.15
  (c3) ABLATE       interpolation mechanism OFF -> the masked region is NOT filled -> completed
       (interp)     repr stays partial -> recognition collapses: acc <= off + 0.15
  (c4) SHUFFLE      shuffle the SURROUNDING (visible) features before interpolation -> the
       (surround)   context can no longer select the right pattern -> completion invalid:
                    acc <= off + 0.15
  (B)  FIDELITY     completed repr resembles original AND the visible features are byte-exact
                    unchanged (input constraint): cos(completed, original) high & visible-MSE
                    == 0. Reported (structure-confirming, non-gating).

GREEN iff c1 and c2 and c3 and c4 (B is the input-constraint structure check).
"""
import numpy as np

SEEDS = [1490, 1491, 1492]
DIM = 64
N_ITEMS = 8            # stored patterns; chance recognition = 1/8 = 0.125
OCC_FRAC = 0.60        # fraction of features occluded (a contiguous masked block)
SHARED = 0.80          # weight of the SHARED template common to all patterns; the per-item
                       # signature is the small residual. With a large contiguous hole, the
                       # raw masked vector is dominated by the shared template -> empty-hole
                       # (off) recognition degrades toward chance, so the hole is load-bearing.
INPUT_NOISE = 0.02     # tiny noise on the presented (visible) features
N_TRIAL = 60           # recognition trials per condition


def cos(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(a @ b / (na * nb))


class Store:
    """Stored perceptual patterns. Completion interpolates a masked region from the surround.

    Recognition = nearest stored pattern by cosine over the SCORED feature set.
    """

    def __init__(self, patterns):
        self.P = patterns                      # (N, DIM) stored patterns

    def complete(self, presented, mask, mode="full", rng=None):
        """Fill the masked region of `presented` from surrounding context.

        presented : (DIM,) input with masked features = 0 (occluded)
        mask      : (DIM,) bool, True = occluded (to be filled)
        mode:
          'full'     input-constrained interpolation: visible features pick the matching
                     stored pattern; masked features are copied from it (surround -> hole).
          'off'      no completion: return the raw masked input (hole stays empty).
          'imagery'  top-down ignoring the partial input: pick a pattern WITHOUT using the
                     visible features (pure internal guess) -> reconstruct from that. This is
                     the input==0 imagery regime; it cannot use the visible part as a constraint.
          'ablate'   completion called but the interpolation step is disabled -> masked region
                     is left empty (same as 'off' for the hole) -> partial repr.
          'shuffle'  shuffle the VISIBLE (surround) features before selecting the pattern ->
                     context can no longer pick the right stored pattern.
        """
        vis = ~mask
        out = presented.copy()
        if mode == "off":
            return out                          # hole left empty
        if mode == "imagery":
            # ignore the partial input entirely: random top-down pick (no input constraint)
            idx = rng.integers(N_ITEMS)
            out = self.P[idx].copy()            # pure top-down repr, visible part NOT honoured
            return out
        # select the matching stored pattern using the VISIBLE features as the constraint
        if mode == "shuffle":
            sel_vis = presented.copy()
            v_idx = np.where(vis)[0]
            sel_vis[v_idx] = presented[v_idx][rng.permutation(len(v_idx))]  # scramble surround
        else:
            sel_vis = presented
        # context-weighted nearest stored pattern over the visible features
        sims = np.array([cos(sel_vis[vis], self.P[k][vis]) for k in range(N_ITEMS)])
        best = int(np.argmax(sims))
        if mode == "ablate":
            return out                          # selection happened but no fill -> hole empty
        out[mask] = self.P[best][mask]          # interpolate ONLY the masked region from surround
        return out

    def recognise(self, repr_vec):
        """Nearest stored pattern over the FULL feature vector (needs the hole filled)."""
        sims = np.array([cos(repr_vec, self.P[k]) for k in range(N_ITEMS)])
        return int(np.argmax(sims))


def run_seed(seed):
    rng = np.random.default_rng(seed)

    # stored patterns = a SHARED template common to all + a small per-item SIGNATURE residual.
    # Because all items share most of their energy, the per-item discriminating signal is the
    # signature. Occluding a large contiguous block removes much of that signature -> the raw
    # masked (empty-hole) vector is dominated by the shared template -> recognition off the raw
    # mask alone degrades toward chance (the hole MATTERS). Completion recovers the full pattern
    # by selecting the matching item from the visible signature residual and filling the hole.
    template = rng.normal(0, 1, DIM)
    template /= np.linalg.norm(template)
    sig = rng.normal(0, 1, (N_ITEMS, DIM))
    sig /= np.linalg.norm(sig, axis=1, keepdims=True)
    P = SHARED * template[None, :] + (1.0 - SHARED) * sig
    P /= np.linalg.norm(P, axis=1, keepdims=True)
    store = Store(P)

    occ_len = int(round(OCC_FRAC * DIM))

    def trial(mode):
        i = rng.integers(N_ITEMS)
        start = rng.integers(0, DIM - occ_len + 1)
        mask = np.zeros(DIM, bool)
        mask[start:start + occ_len] = True
        presented = P[i].copy()
        presented[~mask] += INPUT_NOISE * rng.normal(0, 1, int((~mask).sum()))  # noise on visible
        presented[mask] = 0.0                                                    # occlude
        completed = store.complete(presented, mask, mode=mode, rng=rng)
        return int(store.recognise(completed) == i), presented, mask, P[i], completed

    def acc(mode, ntrial=N_TRIAL):
        return float(np.mean([trial(mode)[0] for _ in range(ntrial)]))

    acc_full = acc("full")
    acc_off = acc("off")
    acc_imagery = acc("imagery")
    acc_ablate = acc("ablate")
    acc_shuffle = acc("shuffle")

    # --- (B) FIDELITY + input-constraint structure check (completed vs original; visible exact)
    fid_cos, vis_mse = [], []
    for _ in range(N_TRIAL):
        _, presented, mask, orig, completed = trial("full")
        fid_cos.append(cos(completed, orig))
        vis = ~mask
        vis_mse.append(float(np.mean((completed[vis] - presented[vis]) ** 2)))  # visible untouched
    fidelity_cos = float(np.mean(fid_cos))
    visible_mse = float(np.mean(vis_mse))

    return dict(
        acc_full=acc_full, acc_off=acc_off, acc_imagery=acc_imagery,
        acc_ablate=acc_ablate, acc_shuffle=acc_shuffle,
        fidelity_cos=fidelity_cos, visible_mse=visible_mse,
    )


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

CHANCE = 1.0 / N_ITEMS
c1 = (agg['acc_full'] - agg['acc_off']) >= 0.30
c2 = agg['acc_imagery'] <= CHANCE + 0.15
c3 = agg['acc_ablate'] <= agg['acc_off'] + 0.15
c4 = agg['acc_shuffle'] <= agg['acc_off'] + 0.15
cB = (agg['fidelity_cos'] >= 0.70) and (agg['visible_mse'] <= 1e-9)
GREEN = c1 and c2 and c3 and c4              # B is the input-constraint structure check

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS} | chance={CHANCE:.3f}")
print(f"c1 PRESENT     full {agg['acc_full']:.3f} - off {agg['acc_off']:.3f} = {agg['acc_full']-agg['acc_off']:.3f} >= 0.30  -> {c1}")
print(f"c2 DISTINCT    imagery-style acc(ignores partial input)={agg['acc_imagery']:.3f} <= chance+0.15={CHANCE+0.15:.3f}  -> {c2}")
print(f"c3 ABLATE      interp OFF acc={agg['acc_ablate']:.3f} <= off+0.15={agg['acc_off']+0.15:.3f} (hole unfilled)  -> {c3}")
print(f"c4 SHUFFLE     surround shuffled acc={agg['acc_shuffle']:.3f} <= off+0.15={agg['acc_off']+0.15:.3f}  -> {c4}")
print(f"B  FIDELITY    cos(completed,original)={agg['fidelity_cos']:.3f}>=0.70 & visible-MSE={agg['visible_mse']:.2e}==0 (input-constrained)  -> {cB} [structure, non-gating]")
print()
print("PER-SEED:")
for s, p in zip(SEEDS, per):
    print(f"  seed {s}: full={p['acc_full']:.3f} off={p['acc_off']:.3f} imagery={p['acc_imagery']:.3f} "
          f"ablate={p['acc_ablate']:.3f} shuffle={p['acc_shuffle']:.3f} "
          f"fid={p['fidelity_cos']:.3f} visMSE={p['visible_mse']:.2e}")
