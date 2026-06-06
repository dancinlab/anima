"""H_989 — RE-FORMULATION re-test of H_973 🔴 (planning does NOT raise Φ).

ORIGINAL 🔴 (H_973): arm-PLAN = MPC over imagined action-conditioned rollouts (the
deliberation trajectory = h0 then, per action, depth steps of free rollout); arm-GREEDY =
current latent + immediate action candidates (depth 0). Φ_PLAN 0.063 < Φ_GREEDY 0.104,
no dose-response (rho=-0.47), fails the fake-plan control → "planning carries no extra Φ".
Mechanistically consistent with H_971: the per-action ROLLOUTS in the plan trajectory are
free-running drifts that decay toward the attractor, dragging Φ down with depth.

WHY THE ORIGINAL MAY BE A FORMULATION ARTIFACT:
  Two coupled issues. (1) H_973's plan trajectory was built by CONCATENATING per-action
  free-running rollouts (depth-many drift steps each) — so deeper plans = more drift =
  mechanically lower Φ (the H_971 effect), confounding "deliberation" with "drift length".
  A faithful planner compares CANDIDATE BRANCHES at a horizon and integrates across them
  (a search TREE / branching frontier), not a long single drift. (2) the Φ-proxy weighting
  may itself disfavor the branch structure. Re-formulate planning as a BRANCHING search
  frontier (compare N candidate first-actions, each rolled a fixed short horizon, the
  deliberation state = the SET of branch endpoints held simultaneously) and vary BRANCHING
  (not drift depth); measure Φ with an alternative proxy.

FROZEN FALSIFIER (this re-formulation — frozen 2026-06-06):
  Same engine as H_973. arm-PLAN = a branching frontier: B candidate actions each rolled a
  FIXED short horizon h0; the deliberation latent = the stacked branch-endpoint set (the
  simultaneously-held alternatives) — branching = the deliberation dose, drift length FIXED.
  arm-GREEDY = single immediate action candidate set (no branching).
  D1 = Φ contrast PLAN(max branching) − GREEDY (Welch t, d, CI), on the ALTERNATIVE proxy.
  D2 = Φ vs BRANCHING factor B (dose-response over B, drift length held fixed) — the clean
       deliberation axis the original confounded with drift depth.
  D3 = fake-branch control (B random endpoints, same compute) — meaningful branches must
       beat random ones. ALSO report the original-proxy contrast for transparency.
  PASS = "🟢 FLIPS": Φ_PLAN > Φ_GREEDY (CI_lo>0, d>=0.5, p<0.05) AND rises with branching AND
         beats fake-branch — under a branching (not drift-depth) formulation, planning raises
         Φ; H_973's null was a drift-confounded formulation artifact.
  FAIL = "🔴 ROBUST": even a branching frontier (drift held fixed) does not raise Φ — planning-
         raises-Φ false across formulations (closed-negative robust).

g5 CODE-measured (no LLM self-judge, p7). substrate=CPU-mirror (numpy). Φ is a PROXY
(H_912/H_931 family, NOT IIT4). Toy single-rung, ladder OPEN (a_scale_honest_scope).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import (LatentWorldModel, phi_proxy, welch_t, cohens_d, boot_ci,
                           spearman, header, verdict_line)

IN_DIM = 6
LATENT = 24
N_DECISIONS = 40
HORIZON = 3              # FIXED short rollout horizon per branch (drift length held constant)
BRANCHES = [1, 2, 4, 8]  # the deliberation dose = BRANCHING factor (NOT drift depth)


def make_engine(seed):
    rng = np.random.default_rng(seed)
    wm = LatentWorldModel(IN_DIM, latent_dim=LATENT, seed=seed, spectral_radius=0.95)
    T = 400; t = np.arange(T)
    stream = np.stack([np.sin(0.2 * t + k) + 0.3 * rng.standard_normal(T) for k in range(IN_DIM)], axis=1)
    H = wm.encode_seq(stream)
    wm.fit_transition(H[:-1], H[1:])
    act_vecs = rng.standard_normal((8, LATENT)) * 0.3   # up to 8 candidate first-actions
    return wm, act_vecs, rng


def frontier(wm, act_vecs, h0, n_branch, horizon, fake=False, rng=None):
    """Branching deliberation: n_branch candidate first-actions, each rolled a FIXED horizon;
    deliberation state = the SET of branch endpoints held simultaneously (the frontier).
    drift length is FIXED (=horizon) so the dose is BRANCHING, not drift depth."""
    endpoints = [h0]
    for b in range(n_branch):
        h = h0 + (rng.standard_normal(LATENT) * 0.3 if fake else act_vecs[b % len(act_vecs)])
        for _ in range(horizon):
            h = wm.roll_latent(h, 1)[0]
        endpoints.append(h.copy())
    return np.array(endpoints)


def phi_alt(H):
    """Alternative Φ-proxy (same as H_988): differentiation enters linearly + double-weighted
    — a different axis-weighting so a real branching effect survives a proxy change."""
    H = np.asarray(H, float)
    if H.ndim == 1:
        H = H[None, :]
    _, base = phi_proxy(H)
    integ, diff, ent = base["integration"], base["differentiation"], base["entropy"]
    return integ * (diff ** 0.5) * (0.5 + 0.5 * ent) * (1.0 + diff)


def main():
    header("H_989", "planning raises Φ under a BRANCHING formulation + alt-proxy — re-test of H_973 🔴")
    print("re-formulation: H_973 confounded deliberation with DRIFT depth; here drift is FIXED")
    print("and the dose is BRANCHING (a search frontier of simultaneously-held alternatives)")
    print(f"horizon(fixed)={HORIZON} branches={BRANCHES} N_decisions={N_DECISIONS}\n")

    phi_plan, phi_greedy, phi_fake = [], [], []
    phi_plan_orig, phi_greedy_orig = [], []   # original-proxy, for transparency
    branch_phi = {b: [] for b in BRANCHES}
    Bmax = BRANCHES[-1]
    for s in range(N_DECISIONS):
        wm, act_vecs, rng = make_engine(s)
        h0 = wm.encode_seq(np.stack([np.sin(0.2 * np.arange(10) + k) for k in range(IN_DIM)], 1))[-1]
        g = frontier(wm, act_vecs, h0, 1, HORIZON, fake=False, rng=rng)   # greedy = 1 branch
        p = frontier(wm, act_vecs, h0, Bmax, HORIZON, fake=False, rng=rng)
        f = frontier(wm, act_vecs, h0, Bmax, HORIZON, fake=True, rng=rng)
        phi_greedy.append(phi_alt(g)); phi_plan.append(phi_alt(p)); phi_fake.append(phi_alt(f))
        phi_greedy_orig.append(phi_proxy(g)[0]); phi_plan_orig.append(phi_proxy(p)[0])
        for b in BRANCHES:
            branch_phi[b].append(phi_alt(frontier(wm, act_vecs, h0, b, HORIZON, fake=False, rng=rng)))

    phi_plan = np.array(phi_plan); phi_greedy = np.array(phi_greedy); phi_fake = np.array(phi_fake)
    contrast = phi_plan.mean() - phi_greedy.mean()
    d = cohens_d(phi_plan, phi_greedy); t, p = welch_t(phi_plan, phi_greedy)
    lo, hi = boot_ci(phi_plan - phi_greedy)
    print("D1 Φ contrast (PLAN max-branch vs GREEDY, ALT proxy):")
    print(f"  Φ_PLAN={phi_plan.mean():.4f}±{phi_plan.std():.4f}  Φ_GREEDY={phi_greedy.mean():.4f}±{phi_greedy.std():.4f}")
    print(f"  contrast={contrast:.4f} d={d:.3f} t={t:.3f} p={p:.3e} CI=[{lo:.4f},{hi:.4f}]")
    orig_contrast = np.array(phi_plan_orig).mean() - np.array(phi_greedy_orig).mean()
    print(f"  (transparency: original-proxy contrast={orig_contrast:.4f})")

    means = np.array([np.mean(branch_phi[b]) for b in BRANCHES])
    rho, prho = spearman(np.repeat(np.array(BRANCHES), N_DECISIONS),
                         np.concatenate([branch_phi[b] for b in BRANCHES]))
    print(f"D2 Φ vs BRANCHING (drift fixed): means={dict(zip(BRANCHES, np.round(means,4)))}  "
          f"Spearman rho={rho:.3f} p={prho:.3e}")

    contrast_fake = phi_plan.mean() - phi_fake.mean()
    df = cohens_d(phi_plan, phi_fake); tf, pf = welch_t(phi_plan, phi_fake)
    print(f"D3 fake-branch control: Φ_PLAN−Φ_FAKE={contrast_fake:.4f} d={df:.3f} p={pf:.3e} "
          f"(Φ_FAKE={phi_fake.mean():.4f})")

    rises = (rho > 0 and prho < 0.05)
    beats_fake = (contrast_fake > 0 and pf < 0.05)
    flips = contrast > 0 and lo > 0 and d >= 0.5 and p < 0.05 and rises and beats_fake
    if flips:
        verdict_line("H_989", "PASS",
                     f"🟢 FLIPS — under a BRANCHING formulation (drift fixed) Φ_PLAN {phi_plan.mean():.3f} "
                     f"> Φ_GREEDY {phi_greedy.mean():.3f} (contrast {contrast:.3f}, d={d:.2f}), rises with "
                     f"branching (rho={rho:.2f}), beats fake-branch (d={df:.2f}) — H_973's null was a "
                     f"DRIFT-CONFOUNDED formulation artifact; deliberation-as-branching raises Φ (toy). xref H_973.")
    else:
        why = []
        if contrast <= 0: why.append(f"Φ_PLAN {phi_plan.mean():.3f} <= Φ_GREEDY {phi_greedy.mean():.3f}")
        elif lo <= 0 or p >= 0.05: why.append("contrast not significant")
        if not rises: why.append(f"no dose-response (rho={rho:.2f}, p={prho:.2f})")
        if not beats_fake: why.append(f"fails fake-branch control (d={df:.2f})")
        verdict_line("H_989", "FAIL",
                     f"🔴 ROBUST — even a branching search frontier (drift held fixed, alt-proxy) does "
                     f"not raise Φ over greedy [{'; '.join(why)}] — planning-raises-Φ is false across "
                     f"formulations; the H_973 closed-negative is FORMULATION-ROBUST (toy). xref H_973.")


if __name__ == "__main__":
    main()
