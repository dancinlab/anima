"""H_973 — Planning-as-consciousness: does deliberative planning raise Φ over greedy?

FROZEN FALSIFIER (honored):
  arm-PLAN = MPC over imagined action-conditioned rollouts; arm-GREEDY = reactive action
  (no lookahead). Φ (proxy H_912/H_931) sampled DURING each decision. matched config.
  D1 = Φ contrast = Φ_PLAN − Φ_GREEDY (Welch t, Cohen d).
  D2 = Φ vs plan-depth (dose-response).
  D3 = "fake plan" control (random rollouts, SAME compute) isolates meaningful
       deliberation vs mere extra compute.
  PASS: Φ_PLAN>Φ_GREEDY (CI_lo>0,d>=0.5,p<0.05) AND Φ rises with depth AND beats fake-plan.
  FAIL: Φ_PLAN<=Φ_GREEDY OR rise fully explained by the fake-plan (compute) control.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import (LatentWorldModel, phi_proxy, welch_t, cohens_d, boot_ci,
                           spearman, header, verdict_line)

IN_DIM = 6
LATENT = 24
N_ACT = 4
N_DECISIONS = 40
DEPTHS = [1, 2, 4, 8]


def make_engine(seed):
    rng = np.random.default_rng(seed)
    wm = LatentWorldModel(IN_DIM, latent_dim=LATENT, seed=seed, spectral_radius=0.95)
    T = 400; t = np.arange(T)
    stream = np.stack([np.sin(0.2 * t + k) + 0.3 * rng.standard_normal(T) for k in range(IN_DIM)], axis=1)
    H = wm.encode_seq(stream)
    wm.fit_transition(H[:-1], H[1:])
    # an action-conditioned perturbation set (each action nudges the latent differently)
    act_vecs = rng.standard_normal((N_ACT, LATENT)) * 0.3
    return wm, act_vecs, rng


def plan_decision(wm, act_vecs, h0, depth, fake=False, rng=None):
    """MPC: for each action, roll the latent forward `depth` steps (action applied at
    step 0), collect the deliberation trajectory; pick best by a value readout proxy
    (latent norm here). Returns the full deliberation latent trajectory for Φ sampling.
    fake=True: same compute but random (meaningless) rollouts."""
    traj = [h0]
    for a in range(N_ACT):
        h = h0 + (rng.standard_normal(LATENT) * 0.3 if fake else act_vecs[a])
        for _ in range(depth):
            h = wm.roll_latent(h, 1)[0]
            if fake:
                h = h + rng.standard_normal(LATENT) * 0.05
            traj.append(h.copy())
    return np.array(traj)


def greedy_decision(wm, act_vecs, h0, rng):
    """No lookahead: just the current latent + the immediate action candidates (depth 0)."""
    traj = [h0] + [h0 + act_vecs[a] for a in range(N_ACT)]
    return np.array(traj)


def main():
    header("H_973", "Planning-as-consciousness — does deliberation raise Φ?")
    print(f"arm-PLAN=MPC over imagined rollouts, arm-GREEDY=reactive; Φ sampled per decision")
    print(f"depths={DEPTHS} N_decisions={N_DECISIONS}\n")

    phi_plan_full, phi_greedy, phi_fake = [], [], []
    depth_phi = {dd: [] for dd in DEPTHS}
    for s in range(N_DECISIONS):
        wm, act_vecs, rng = make_engine(s)
        h0 = wm.encode_seq(np.stack([np.sin(0.2 * np.arange(10) + k) for k in range(IN_DIM)], 1))[-1]
        # greedy
        phi_g, _ = phi_proxy(greedy_decision(wm, act_vecs, h0, rng))
        phi_greedy.append(phi_g)
        # plan at full depth (8) and fake at full depth
        phi_p, _ = phi_proxy(plan_decision(wm, act_vecs, h0, 8, fake=False, rng=rng))
        phi_plan_full.append(phi_p)
        phi_f, _ = phi_proxy(plan_decision(wm, act_vecs, h0, 8, fake=True, rng=rng))
        phi_fake.append(phi_f)
        # dose-response over depths
        for dd in DEPTHS:
            pp, _ = phi_proxy(plan_decision(wm, act_vecs, h0, dd, fake=False, rng=rng))
            depth_phi[dd].append(pp)

    phi_plan_full = np.array(phi_plan_full); phi_greedy = np.array(phi_greedy); phi_fake = np.array(phi_fake)
    contrast = phi_plan_full.mean() - phi_greedy.mean()
    d = cohens_d(phi_plan_full, phi_greedy); t, p = welch_t(phi_plan_full, phi_greedy)
    diff = phi_plan_full - phi_greedy; lo, hi = boot_ci(diff)
    print("D1 Φ contrast (PLAN depth=8 vs GREEDY):")
    print(f"  Φ_PLAN={phi_plan_full.mean():.4f}±{phi_plan_full.std():.4f}  "
          f"Φ_GREEDY={phi_greedy.mean():.4f}±{phi_greedy.std():.4f}")
    print(f"  contrast={contrast:.4f} d={d:.3f} t={t:.3f} p={p:.3e} CI=[{lo:.4f},{hi:.4f}]")

    depths_arr = np.array(DEPTHS)
    means = np.array([np.mean(depth_phi[dd]) for dd in DEPTHS])
    rho, prho = spearman(np.repeat(depths_arr, N_DECISIONS),
                         np.concatenate([depth_phi[dd] for dd in DEPTHS]))
    print(f"D2 Φ vs plan-depth: means={dict(zip(DEPTHS, np.round(means,4)))}  Spearman rho={rho:.3f} p={prho:.3e}")

    # D3 fake-plan control: PLAN must beat fake (same compute)
    contrast_fake = phi_plan_full.mean() - phi_fake.mean()
    df = cohens_d(phi_plan_full, phi_fake); tf, pf = welch_t(phi_plan_full, phi_fake)
    print(f"D3 fake-plan control: Φ_PLAN−Φ_FAKE={contrast_fake:.4f} d={df:.3f} p={pf:.3e} "
          f"(Φ_FAKE={phi_fake.mean():.4f})")

    rises = (rho > 0 and prho < 0.05)
    beats_fake = (contrast_fake > 0 and pf < 0.05)
    if contrast > 0 and lo > 0 and d >= 0.5 and p < 0.05 and rises and beats_fake:
        verdict_line("H_973", "PASS",
                     f"Φ_PLAN>Φ_GREEDY contrast={contrast:.3f} d={d:.2f}, rises with depth "
                     f"(rho={rho:.2f}), beats fake-plan — planning-as-consciousness (toy).")
    elif contrast <= 0 or hi < 0 or not beats_fake:
        verdict_line("H_973", "FAIL",
                     f"Φ_PLAN<=Φ_GREEDY (contrast={contrast:.3f}) OR rise explained by compute "
                     f"(beats_fake={beats_fake}) — planning carries no extra Φ (closed-negative).")
    else:
        verdict_line("H_973", "INCOMPLETE", f"contrast={contrast:.3f} did not clear the bar; toy C3.")


if __name__ == "__main__":
    main()
