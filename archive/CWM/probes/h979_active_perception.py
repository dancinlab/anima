"""H_979 — Active perception / curiosity (engine picks informative glimpses).

FROZEN FALSIFIER (honored):
  a hidden toy world-state observable only through K selectable glimpses.
  arm-ACTIVE = engine picks the next glimpse to maximize expected uncertainty reduction;
  arm-PASSIVE = fixed raster / random glimpse order. Identical budget B glimpses.
  D1 = world-state reconstruction error after B glimpses (active vs passive).
  D2 = glimpses-to-threshold (to reach error<=eps), active vs passive.
  D3 = random-glimpse arm bounds "any selection helps"; active must beat random too.
  PASS: error_active < error_passive (and < random) at B (d>=0.5, p<0.05) AND
        glimpses-to-threshold_active < passive.
  FAIL: error_active ~ error_passive OR active does not beat random.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import cohens_d, welch_t, header, verdict_line

GRID = 16          # hidden world-state = GRID cells
B = 6              # glimpse budget
N = 200            # episodes
EPS = 0.25


def episode(rng):
    """hidden world-state: GRID cells, each a value; some cells are HIGH-variance
    (informative), most are low. A glimpse reveals one cell exactly. Reconstruction =
    estimate all cells; error = MSE on unseen cells (filled by prior mean)."""
    informativeness = rng.random(GRID) ** 3           # few cells carry most info
    informativeness /= informativeness.sum()
    state = rng.standard_normal(GRID) * (0.2 + 3.0 * informativeness)
    return state, informativeness


def reconstruct_error(state, seen_idx):
    est = np.zeros(GRID)
    for i in seen_idx:
        est[i] = state[i]
    return np.mean((est - state) ** 2)


def active_select(informativeness, seen, remaining_budget):
    """curiosity: pick the unseen cell with the highest expected uncertainty reduction
    (here: highest informativeness == expected variance explained)."""
    mask = np.ones(GRID, bool); mask[list(seen)] = False
    cand = np.where(mask)[0]
    return cand[np.argmax(informativeness[cand])]


def run_arm(rng, mode):
    errs, gtt = [], []
    for _ in range(N):
        state, info = episode(rng)
        seen = []
        order = rng.permutation(GRID) if mode == "random" else np.arange(GRID)
        reached = B + 1
        for step in range(B):
            if mode == "active":
                nxt = active_select(info, seen, B - step)
            elif mode == "passive":
                nxt = order[step]              # fixed raster
            else:
                nxt = order[step]              # random order
            seen.append(nxt)
            if reached > B and reconstruct_error(state, seen) <= EPS:
                reached = step + 1
        errs.append(reconstruct_error(state, seen))
        gtt.append(reached)
    return np.array(errs), np.array(gtt)


def main():
    header("H_979", "Active perception / curiosity (informative glimpse selection)")
    print(f"hidden world GRID={GRID} cells, glimpse budget B={B}, N={N}, eps={EPS}\n")
    rng = np.random.default_rng(0)
    eA, gA = run_arm(np.random.default_rng(1), "active")
    eP, gP = run_arm(np.random.default_rng(2), "passive")
    eR, gR = run_arm(np.random.default_rng(3), "random")
    print(f"D1 reconstruction error after B glimpses:")
    print(f"  active  = {eA.mean():.4f} ± {eA.std():.4f}")
    print(f"  passive = {eP.mean():.4f} ± {eP.std():.4f}")
    print(f"  random  = {eR.mean():.4f} ± {eR.std():.4f}")
    d_ap = cohens_d(eP, eA); t_ap, p_ap = welch_t(eA, eP)
    d_ar = cohens_d(eR, eA); t_ar, p_ar = welch_t(eA, eR)
    print(f"  active vs passive: d={d_ap:.3f} p={p_ap:.3e}")
    print(f"  active vs random : d={d_ar:.3f} p={p_ar:.3e}")
    print(f"D2 glimpses-to-threshold (<=eps): active={gA.mean():.3f} passive={gP.mean():.3f} "
          f"random={gR.mean():.3f}")

    beats_passive = (eA.mean() < eP.mean()) and p_ap < 0.05 and d_ap >= 0.5
    beats_random = (eA.mean() < eR.mean()) and p_ar < 0.05
    faster = gA.mean() < gP.mean()
    if beats_passive and beats_random and faster:
        verdict_line("H_979", "PASS",
                     f"error_active {eA.mean():.3f} < passive {eP.mean():.3f} (d={d_ap:.2f}) "
                     f"and < random {eR.mean():.3f}; faster-to-threshold ({gA.mean():.2f}<{gP.mean():.2f}) "
                     f"— active perception (toy).")
    elif not beats_passive or not beats_random:
        verdict_line("H_979", "FAIL",
                     f"active ~ passive (d={d_ap:.2f}) or active does not beat random — "
                     f"perception not agentive (closed-negative).")
    else:
        verdict_line("H_979", "INCOMPLETE", "marginal; toy C3.")


if __name__ == "__main__":
    main()
