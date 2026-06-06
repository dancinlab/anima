"""H_982 — REM offline world-model consolidation (learning-in-imagination).

FROZEN FALSIFIER (honored):
  WAKE_1 (learn from real input) -> {arm-REM: imagined-rollout rehearsal | arm-CONTROL:
  idle / random-replay of equal budget} -> WAKE_2 (evaluate). N seeds.
  D1 = next-WAKE world-model prediction error (or task return), REM vs CONTROL.
  D2 = consolidation delta = error_CONTROL - error_REM (WAKE_2 benefit attributable to REM).
  D3 = idle and random-replay arms bound "any downtime helps"/"any replay helps".
  PASS: error_REM < error_CONTROL (and < random-replay) at WAKE_2 (d>=0.5, p<0.05).
  FAIL: error_REM ~ error_CONTROL OR REM does not beat random-replay.

Model: the WAKE_1 phase trains the latent transition on a LIMITED real sample (so the model
is undertrained). REM = generate imagined rollouts from the learned model and RE-FIT on them
(self-distillation / replay of imagined experience) -> regularizes/consolidates the operator.
random-replay = re-fit on RANDOM (non-model) sequences of equal budget. idle = no extra fit.
WAKE_2 = prediction error on held-out REAL trajectories.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import LDSWorldModel, _ridge, _aug, cohens_d, welch_t, header, verdict_line

ODIM = 2
T = 25
N_WAKE1 = 6           # VERY LIMITED real training (genuinely undertrained model)
N_REM = 200           # imagined-rollout rehearsal budget
WAKE1_NOISE = 0.5     # noisy WAKE1 observations -> the fit is imperfect, leaving room
                      # for REM rehearsal (clean imagined experience) to consolidate
N_TEST = 200
H_EVAL = 4
N_SEEDS = 25


def make_traj(rng):
    theta = 0.4
    R = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    pos = rng.standard_normal(2); v = rng.standard_normal(2) * 0.5
    out = [pos.copy()]
    for _ in range(T - 1):
        v = R @ v; pos = pos + 0.3 * v + 0.03 * rng.standard_normal(2); out.append(pos.copy())
    return np.array(out)


def eval_error(m, test):
    errs = []
    for tr in test:
        z = m.embed(tr)
        for t in range(3, T - H_EVAL, 3):
            zr = m.roll(z[t], H_EVAL)
            errs.append(np.mean((m.decode(zr) - tr[t + H_EVAL]) ** 2))
    return np.mean(errs)


def run_seed(seed):
    rng = np.random.default_rng(seed)
    wake1 = [make_traj(rng) + WAKE1_NOISE*rng.standard_normal((T,ODIM)) for _ in range(N_WAKE1)]
    test = [make_traj(np.random.default_rng(7000 + seed * 10 + i)) for i in range(N_TEST)]

    # WAKE_1: undertrained model on limited real data
    base = LDSWorldModel(ODIM, delay=3, ridge=1e-1).fit(wake1)
    err_idle = eval_error(base, test)

    # arm-REM: generate imagined rollouts, re-fit (consolidate) on real+imagined
    rem_trajs = list(wake1)
    rgen = np.random.default_rng(seed * 2 + 1)
    for _ in range(N_REM):
        z = base.embed(make_traj(rgen))[3]
        roll = [base.decode(base.roll(z, h)) for h in range(T)]
        rem_trajs.append(np.array(roll))
    rem = LDSWorldModel(ODIM, delay=3, ridge=1e-1).fit(rem_trajs)
    err_rem = eval_error(rem, test)

    # arm-CONTROL random-replay: re-fit on real + RANDOM sequences (equal budget)
    ctrl_trajs = list(wake1)
    rr = np.random.default_rng(seed * 2 + 2)
    for _ in range(N_REM):
        ctrl_trajs.append(rr.standard_normal((T, ODIM)) * 2.0)
    ctrl = LDSWorldModel(ODIM, delay=3, ridge=1e-1).fit(ctrl_trajs)
    err_ctrl = eval_error(ctrl, test)

    return err_rem, err_ctrl, err_idle


def main():
    header("H_982", "REM offline world-model consolidation (learning-in-imagination)")
    print(f"WAKE1 (limited n={N_WAKE1}) -> REM rehearsal (n={N_REM}) vs random-replay/idle -> WAKE2")
    print(f"N_seeds={N_SEEDS} eval-horizon={H_EVAL}\n")
    rem, ctrl, idle = [], [], []
    for s in range(N_SEEDS):
        a, b, c = run_seed(s)
        rem.append(a); ctrl.append(b); idle.append(c)
    rem, ctrl, idle = map(np.array, (rem, ctrl, idle))
    print(f"D1 WAKE_2 prediction error:")
    print(f"  REM rehearsal   = {rem.mean():.4f} ± {rem.std():.4f}")
    print(f"  random-replay   = {ctrl.mean():.4f} ± {ctrl.std():.4f}")
    print(f"  idle (no replay)= {idle.mean():.4f} ± {idle.std():.4f}")
    delta = ctrl.mean() - rem.mean()
    d = cohens_d(ctrl, rem); t, p = welch_t(rem, ctrl)
    di = cohens_d(idle, rem); ti, pi = welch_t(rem, idle)
    print(f"D2 consolidation delta (CONTROL−REM) = {delta:.4f}  d={d:.3f} p={p:.3e}")
    print(f"D3 REM vs idle: d={di:.3f} p={pi:.3e}")

    # the D3 IDLE arm is the decisive control: REM rehearsal must beat doing NOTHING to
    # claim consolidation. Beating random-replay alone is trivial (random-replay actively
    # CORRUPTS). Pure self-replay cannot add information absent from WAKE_1.
    beats_replay = (rem.mean() < ctrl.mean()) and p < 0.05 and d >= 0.5
    beats_idle = (rem.mean() < idle.mean() - 1e-4) and pi < 0.05 and di >= 0.5
    if beats_replay and beats_idle:
        verdict_line("H_982", "PASS",
                     f"error_REM {rem.mean():.3f} < random-replay {ctrl.mean():.3f} (d={d:.2f}) AND "
                     f"< idle {idle.mean():.3f} (d={di:.2f}) — REM consolidation / learning-in-"
                     f"imagination (toy).")
    elif not beats_idle:
        verdict_line("H_982", "FAIL",
                     f"REM rehearsal {rem.mean():.3f} ~ idle {idle.mean():.3f} (d={di:.2f}, p={pi:.2f}) "
                     f"— pure self-replay adds NO consolidation over doing nothing (it cannot add "
                     f"information absent from WAKE_1); it only beats random-replay because that "
                     f"arm corrupts. Closed-negative (a_paper_negative_ok).")
    else:
        verdict_line("H_982", "INCOMPLETE", f"d_idle={di:.2f} marginal; toy C3.")


if __name__ == "__main__":
    main()
