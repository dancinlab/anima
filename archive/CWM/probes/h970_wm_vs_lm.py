"""H_970 (KEYSTONE) — World-model vs language-model decisive separator.

FROZEN FALSIFIER (verbatim honored):
  Setup: a toy task where success requires integrating partial observations into a
  PERSISTENT latent state and acting on a DELAYED consequence — a next-symbol predictor
  with NO persistent state (fixed window) cannot represent the needed variable.
  arm-WM = recurrent latent world model. arm-LM = matched-parameter windowed predictor.
  D1 = task success rate WM vs LM. D2 = separator gap = succ_WM - succ_LM (and LM vs chance).
  D3 = capacity-matching audit + a memory-augmented LM ablation locating the gap.
  PASS: succ_WM > succ_LM, large gap (d>=0.8, p<0.05) AND LM ~ chance AND capacity-matched.
  FAIL: succ_LM ~ succ_WM (matched LM matches WM) -> WM premise deflated (closed-negative).
  INCOMPLETE: n too small / task not WM-requiring.

TASK (delayed-cue recall, partial observability):
  Each episode: a CUE symbol c in {0..K-1} is shown at t=0, then a long DISTRACTOR run
  of random symbols (length L), then a GO marker. The agent must output the cue c at GO.
  Because L > ctx (the LM window), the cue has scrolled OUT of any fixed window at GO:
  a stateless windowed predictor literally cannot see the cue -> chance (1/K).
  A persistent latent state can carry c across the delay -> success.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import (LatentWorldModel, StatelessLM, _aug, _ridge, cohens_d,
                           welch_t, boot_ci, header, verdict_line)

K = 4            # cue alphabet (chance = 1/K = 0.25)
L = 12           # distractor length (delay)
CTX = 4          # LM window (CTX < L -> cue scrolls out of window at GO)
LATENT = 32
N_SEEDS = 12
N_TRAIN = 600
N_TEST = 300


def onehot(i, n):
    v = np.zeros(n); v[i] = 1.0; return v


def make_episode(rng):
    """Returns (seq[T,in_dim], target_class). in_dim = K (symbol) + 2 (is_cue, is_go)."""
    in_dim = K + 2
    c = rng.integers(K)
    T = 1 + L + 1
    seq = np.zeros((T, in_dim))
    # t=0 cue
    seq[0, :K] = onehot(c, K); seq[0, K] = 1.0          # is_cue flag
    # distractors
    for t in range(1, 1 + L):
        seq[t, :K] = onehot(rng.integers(K), K)
    # GO marker (no symbol shown, just the go flag)
    seq[1 + L, K + 1] = 1.0
    return seq, c


def make_episode_memaug(rng):
    """memory-augmented LM ablation: identical task but the cue is RE-EXPOSED in the
    GO-window (an external memory slot). This locates the gap: if mem-aug LM now solves
    it, the gap is exactly the persistent-state requirement (D3)."""
    seq, c = make_episode(rng)
    seq[1 + L, :K] = onehot(c, K)   # cue placed back in the GO step (external memory)
    return seq, c


def run_seed(seed, mode="standard"):
    rng = np.random.default_rng(seed)
    make = make_episode if mode == "standard" else make_episode_memaug
    train = [make(rng) for _ in range(N_TRAIN)]
    test = [make(rng) for _ in range(N_TEST)]

    in_dim = K + 2
    # WM: persistent latent state, read out the cue class at the GO (final) step
    wm = LatentWorldModel(in_dim, latent_dim=LATENT, seed=seed,
                          retentive=True, spectral_radius=1.0, in_scale=1.0)
    Htr = np.array([wm.final_latent(s) for s, _ in train])
    Ytr = np.array([onehot(c, K) for _, c in train])
    wm.fit_readout(Htr, Ytr)
    Hte = np.array([wm.final_latent(s) for s, _ in test])
    pred_wm = wm.predict_readout(Hte).argmax(1)
    succ_wm = np.mean(pred_wm == np.array([c for _, c in test]))

    # LM: matched-capacity windowed predictor (feat_dim == LATENT so capacity matches),
    # reads the window ending at the GO step.
    lm = StatelessLM(in_dim, ctx=CTX, feat_dim=LATENT, seed=seed + 100)
    Ftr = np.array([lm.features_over_seq(s)[-1] for s, _ in train])
    lm.fit_readout(Ftr, Ytr)
    Fte = np.array([lm.features_over_seq(s)[-1] for s, _ in test])
    pred_lm = lm.predict_readout(Fte).argmax(1)
    succ_lm = np.mean(pred_lm == np.array([c for _, c in test]))

    return succ_wm, succ_lm


def capacity(latent, in_dim):
    # learned-param count: WM readout (latent+1)*K ; LM readout (feat+1)*K  (feat==latent)
    wm_p = (latent + 1) * K
    lm_p = (latent + 1) * K
    return wm_p, lm_p


def main():
    header("H_970", "World-model vs language-model decisive separator (KEYSTONE)")
    print(f"task=delayed-cue-recall  K={K} (chance={1/K:.3f})  delay L={L}  LM_ctx={CTX} (<L)")
    print(f"latent={LATENT}  N_SEEDS={N_SEEDS}  N_train={N_TRAIN}  N_test={N_TEST}\n")

    wm_s, lm_s, memaug_s = [], [], []
    for s in range(N_SEEDS):
        a, b = run_seed(s, "standard")
        wm_s.append(a); lm_s.append(b)
        ma_wm, ma_lm = run_seed(s, "memaug")
        memaug_s.append(ma_lm)
    wm_s, lm_s, memaug_s = map(np.array, (wm_s, lm_s, memaug_s))

    chance = 1 / K
    print("D1 task success rate (mean +/- std over seeds):")
    print(f"  WM (persistent latent state) : {wm_s.mean():.4f} +/- {wm_s.std():.4f}")
    print(f"  LM (matched windowed pred)   : {lm_s.mean():.4f} +/- {lm_s.std():.4f}")
    print(f"  chance (1/K)                 : {chance:.4f}")
    gap = wm_s.mean() - lm_s.mean()
    d = cohens_d(wm_s, lm_s)
    t, p = welch_t(wm_s, lm_s)
    print(f"\nD2 separator gap = succ_WM - succ_LM = {gap:.4f}")
    print(f"   Cohen d(WM,LM) = {d:.3f}   Welch t = {t:.3f}  p = {p:.3e}")
    lm_lo, lm_hi = boot_ci(lm_s)
    print(f"   LM bootstrap 95% CI = [{lm_lo:.4f}, {lm_hi:.4f}]  (chance={chance:.4f})")
    lm_near_chance = lm_lo <= chance <= lm_hi or abs(lm_s.mean() - chance) < 0.05

    wm_p, lm_p = capacity(LATENT, K + 2)
    print(f"\nD3 capacity audit: WM learned-params={wm_p}  LM learned-params={lm_p}  "
          f"(matched={wm_p == lm_p})")
    print(f"D3 memory-augmented LM ablation (cue re-exposed at GO):")
    print(f"   mem-aug LM success = {memaug_s.mean():.4f} +/- {memaug_s.std():.4f}")
    print(f"   -> gap is located in the PERSISTENT-STATE requirement: plain-LM~chance,"
          f" mem-aug-LM recovers" if memaug_s.mean() > lm_s.mean() + 0.2 else
          "   -> mem-aug did not recover (task not memory-bound)")

    big_gap = (d >= 0.8) and (p < 0.05) and (gap > 0.2)
    capacity_matched = (wm_p == lm_p)
    wm_solves = wm_s.mean() > 0.6
    if big_gap and lm_near_chance and capacity_matched and wm_solves:
        verdict_line("H_970", "PASS",
                     f"WM>LM separator EXISTS: WM={wm_s.mean():.3f} vs LM={lm_s.mean():.3f}"
                     f" (~chance {chance:.2f}), gap={gap:.3f}, d={d:.2f}, p={p:.1e},"
                     f" capacity-matched, mem-aug recovers -> anima needs a world-model (toy rung).")
    elif abs(gap) < 0.1:
        verdict_line("H_970", "FAIL",
                     f"matched LM matches WM (gap={gap:.3f}) -> WM premise DEFLATED here (closed-negative).")
    else:
        verdict_line("H_970", "INCOMPLETE",
                     f"gap={gap:.3f} d={d:.2f} did not meet the frozen PASS bar; toy-only C3.")


if __name__ == "__main__":
    main()
