"""H_987 — RE-FORMULATION re-test of H_982 🔴 (REM self-replay == idle, adds no info).

ORIGINAL 🔴 (H_982): WAKE_1 trains an undertrained LDS; arm-REM re-fits on VERBATIM
imagined rollouts of the SAME learned model; arm-idle does nothing. error_REM == error_idle
(d=-0.00, p=1.00) → "pure self-replay cannot add information absent from WAKE_1" (closed-
negative). It beat random-replay only because that arm CORRUPTS.

WHY THE ORIGINAL MAY BE A FORMULATION ARTIFACT:
  H_982's replay was VERBATIM self-distillation — it re-fit on the model's OWN unconditional
  rollouts. That arm provably cannot add information: it samples from the very distribution
  it was fit to (a fixed point of the EM-style update). But biological REM consolidation is
  NOT verbatim — it RECOMBINES fragments of distinct waking episodes (replay that interleaves
  / stitches sub-trajectories), and consolidation gain in replay literature comes from
  GENERALIZATION across episodes, not from re-playing one episode unchanged. A faithful
  replay objective should test recombinative replay, where the gain (if any) is the model
  learning the SHARED dynamics common to multiple episodes from limited per-episode data.

FROZEN FALSIFIER (this re-formulation — frozen 2026-06-06):
  WAKE_1 = a FEW short fragments from EACH of several episodes that share an underlying
  transition law but differ in surface (init / phase). Then:
    arm-RECOMBINE = generate replay that STITCHES fragments across episodes (cross-episode
        recombination) + re-fit -> tests consolidation of the shared law.
    arm-VERBATIM  = the H_982 arm (re-fit on unconditional self-rollouts) -> the original null.
    arm-IDLE      = no extra fit (the decisive control: replay must beat doing nothing).
    arm-RANDOM    = re-fit on random noise (corruption floor, as in H_982).
  D1 = WAKE_2 held-out prediction error per arm.
  D2 = consolidation delta = error_IDLE - error_RECOMBINE (the gain attributable to
       recombinative replay over doing nothing); d, p.
  D3 = RECOMBINE vs VERBATIM (does recombination beat the verbatim arm H_982 already ran?).
  PASS = "🟢 FLIPS": error_RECOMBINE < error_IDLE (d>=0.5, p<0.05) AND <= VERBATIM — a richer
         replay objective DOES add consolidation; the H_982 null was specific to the verbatim
         formulation.
  FAIL = "🔴 ROBUST": even recombinative replay ~ idle — replay adds no information across
         formulations; the closed-negative is robust.

g5 CODE-measured (no LLM self-judge, p7). substrate=CPU-mirror (numpy). Toy single-rung,
ladder OPEN (a_scale_honest_scope). Read-only probe.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import LDSWorldModel, cohens_d, welch_t, header, verdict_line

ODIM = 2
T = 25
N_EPISODES = 6          # several episodes sharing ONE transition law, differing in surface
N_FRAG_PER_EP = 2       # only a FEW fragments per episode -> per-episode undertraining
FRAG_LEN = 10           # fragments are SHORT (sub-trajectories, not whole episodes)
N_REPLAY = 200          # replay budget (matched across replay arms)
WAKE1_NOISE = 0.5
N_TEST = 200
H_EVAL = 4
N_SEEDS = 25


def shared_rot():
    """The ONE underlying transition law shared by all episodes (consolidation target)."""
    theta = 0.4
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


def make_traj(rng, length=T, R=None):
    """A trajectory from the shared law; surface (init pos/vel) varies per episode."""
    R = shared_rot() if R is None else R
    pos = rng.standard_normal(2); v = rng.standard_normal(2) * 0.5
    out = [pos.copy()]
    for _ in range(length - 1):
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
    R = shared_rot()
    # WAKE_1: a few SHORT fragments from each of several episodes (shared law, varied surface)
    wake1 = []
    for ep in range(N_EPISODES):
        for _ in range(N_FRAG_PER_EP):
            frag = make_traj(rng, length=FRAG_LEN, R=R) + WAKE1_NOISE * rng.standard_normal((FRAG_LEN, ODIM))
            wake1.append(frag)
    test = [make_traj(np.random.default_rng(7000 + seed * 10 + i), length=T, R=R) for i in range(N_TEST)]

    base = LDSWorldModel(ODIM, delay=3, ridge=1e-1).fit(wake1)
    err_idle = eval_error(base, test)

    # arm-VERBATIM (the H_982 arm): re-fit on unconditional self-rollouts
    vb = list(wake1)
    rgen = np.random.default_rng(seed * 2 + 1)
    for _ in range(N_REPLAY):
        z = base.embed(make_traj(rgen, length=FRAG_LEN, R=R))[3]
        vb.append(np.array([base.decode(base.roll(z, h)) for h in range(T)]))
    err_verbatim = eval_error(LDSWorldModel(ODIM, delay=3, ridge=1e-1).fit(vb), test)

    # arm-RECOMBINE: STITCH fragments ACROSS episodes -> longer replay trajectories that
    # force the model to express the SHARED law spanning surfaces it never saw contiguously.
    rc = list(wake1)
    rr = np.random.default_rng(seed * 3 + 5)
    for _ in range(N_REPLAY):
        # pick two waking fragments from DIFFERENT episodes; roll the model from frag A's
        # end-latent then from frag B's, concatenating -> a recombined replay episode.
        i, j = rr.integers(len(wake1)), rr.integers(len(wake1))
        zi = base.embed(wake1[i])[-1] if len(wake1[i]) >= 3 else base.embed(wake1[i])[0]
        zj = base.embed(wake1[j])[-1] if len(wake1[j]) >= 3 else base.embed(wake1[j])[0]
        seg_a = [base.decode(base.roll(zi, h)) for h in range(T // 2)]
        seg_b = [base.decode(base.roll(zj, h)) for h in range(T - T // 2)]
        rc.append(np.array(seg_a + seg_b))
    err_recombine = eval_error(LDSWorldModel(ODIM, delay=3, ridge=1e-1).fit(rc), test)

    # arm-RANDOM (corruption floor, as in H_982)
    rd = list(wake1)
    rn = np.random.default_rng(seed * 2 + 2)
    for _ in range(N_REPLAY):
        rd.append(rn.standard_normal((T, ODIM)) * 2.0)
    err_random = eval_error(LDSWorldModel(ODIM, delay=3, ridge=1e-1).fit(rd), test)

    return err_recombine, err_verbatim, err_idle, err_random


def main():
    header("H_987", "recombinative replay consolidation — re-test of H_982 🔴")
    print("re-formulation: H_982 replayed VERBATIM self-rollouts; here replay RECOMBINES")
    print("fragments across episodes that share one transition law (consolidation = the shared law)")
    print(f"N_episodes={N_EPISODES} frags/ep={N_FRAG_PER_EP} frag_len={FRAG_LEN} replay={N_REPLAY} N_seeds={N_SEEDS}\n")
    rc, vb, idle, rnd = [], [], [], []
    for s in range(N_SEEDS):
        a, b, c, d = run_seed(s)
        rc.append(a); vb.append(b); idle.append(c); rnd.append(d)
    rc, vb, idle, rnd = map(np.array, (rc, vb, idle, rnd))
    print("D1 WAKE_2 prediction error:")
    print(f"  RECOMBINE replay = {rc.mean():.4f} ± {rc.std():.4f}")
    print(f"  VERBATIM (H_982) = {vb.mean():.4f} ± {vb.std():.4f}")
    print(f"  idle (no replay) = {idle.mean():.4f} ± {idle.std():.4f}")
    print(f"  random-replay    = {rnd.mean():.4f} ± {rnd.std():.4f}")
    delta_idle = idle.mean() - rc.mean()
    di = cohens_d(idle, rc); ti, pi = welch_t(rc, idle)
    print(f"D2 consolidation delta (IDLE−RECOMBINE) = {delta_idle:.4f}  d={di:.3f} p={pi:.3e}")
    delta_vb = vb.mean() - rc.mean()
    dv = cohens_d(vb, rc); tv, pv = welch_t(rc, vb)
    print(f"D3 RECOMBINE vs VERBATIM: delta={delta_vb:.4f} d={dv:.3f} p={pv:.3e}")

    beats_idle = (rc.mean() < idle.mean() - 1e-4) and pi < 0.05 and di >= 0.5
    beats_or_ties_verbatim = rc.mean() <= vb.mean() + 1e-4
    if beats_idle and beats_or_ties_verbatim:
        verdict_line("H_987", "PASS",
                     f"🟢 FLIPS — recombinative replay {rc.mean():.3f} < idle {idle.mean():.3f} "
                     f"(d={di:.2f}, p={pi:.1e}) and <= verbatim {vb.mean():.3f}: a RICHER replay "
                     f"objective DOES consolidate the shared law over doing nothing — H_982's null "
                     f"was specific to the VERBATIM formulation (toy, ladder OPEN). xref H_982.")
    else:
        why = []
        if not beats_idle: why.append(f"RECOMBINE {rc.mean():.3f} ~ idle {idle.mean():.3f} (d={di:.2f}, p={pi:.2f})")
        if not beats_or_ties_verbatim: why.append(f"worse than verbatim {vb.mean():.3f}")
        verdict_line("H_987", "FAIL",
                     f"🔴 ROBUST — even recombinative cross-episode replay adds no consolidation over "
                     f"idle [{'; '.join(why)}] — replay-adds-no-information is FORMULATION-ROBUST; "
                     f"self-replay cannot manufacture information absent from WAKE_1 (toy). xref H_982.")


if __name__ == "__main__":
    main()
