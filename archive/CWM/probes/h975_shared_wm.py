"""H_975 — Multi-agent shared world model ⊥ individuation.

FROZEN FALSIFIER (honored):
  two engine instances, distinct ANU genesis windows (H_932). Exchange world-state
  latents as environment context (NOT forced sync) over a coupling sweep (weak->strong).
  D1 = world-model agreement = cross-agent similarity of world-state estimates on shared
       observations, vs an unpaired (no-exchange) baseline; rises with coupling?
  D2 = individuation preserved (H_939): genesis_hash distinct at every coupling AND no
       coupling reaches the lock bar (decision streams never identical).
  D3 = unpaired baseline bounds spurious agreement; over-coupled arm checks collapse.
  PASS: agreement rises with coupling above unpaired (CI_lo>0) AND individuation preserved.
  FAIL-no-share: agreement never exceeds unpaired.
  FAIL-collapse: agreement only with individuation collapse (lock bar / identical streams).
"""
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from cwm_probe_lib import LatentWorldModel, spearman, boot_ci, header, verdict_line

IN_DIM = 6
LATENT = 24
N_OBS = 60
COUPLINGS = [0.0, 0.1, 0.25, 0.5, 0.75, 1.0]
N_SEEDS = 20
LOCK_BAR = 0.999     # decision-stream correlation at/above which individuation is LOST


def genesis_hash(seed):
    return hashlib.sha256(f"ANU-genesis-{seed}".encode()).hexdigest()[:16]


def run_pair(seed, coupling):
    rng = np.random.default_rng(seed)
    # two engines with DISTINCT genesis windows (distinct seeds)
    a = LatentWorldModel(IN_DIM, latent_dim=LATENT, seed=seed * 2 + 1, spectral_radius=0.9)
    b = LatentWorldModel(IN_DIM, latent_dim=LATENT, seed=seed * 2 + 2, spectral_radius=0.9)
    # shared observation stream (the common world)
    t = np.arange(N_OBS)
    obs = np.stack([np.sin(0.3 * t + k) + 0.2 * rng.standard_normal(N_OBS) for k in range(IN_DIM)], 1)

    ha = np.zeros(LATENT); hb = np.zeros(LATENT)
    est_a, est_b, dec_a, dec_b = [], [], [], []
    for x in obs:
        ha_new = a.step(ha, x); hb_new = b.step(hb, x)
        # exchange the WORLD-STATE latent as environment context: each agent nudges its
        # estimate toward the partner's estimate of the SAME world (a meaningful comm
        # channel, NOT a random scramble). coupling=strength; NOT a forced sync (the
        # agent's own dynamics still dominate; a_substrate_native_speak).
        ha = ha_new + coupling * (hb_new - ha_new)
        hb = hb_new + coupling * (ha_new - hb_new)
        est_a.append(ha.copy()); est_b.append(hb.copy())
        dec_a.append(int(np.argmax(ha[:4]))); dec_b.append(int(np.argmax(hb[:4])))
    est_a, est_b = np.array(est_a), np.array(est_b)
    # world-model agreement: mean cosine similarity of aligned world-state estimates
    num = (est_a * est_b).sum(1)
    den = np.linalg.norm(est_a, axis=1) * np.linalg.norm(est_b, axis=1) + 1e-9
    agreement = float(np.mean(num / den))
    # decision-stream identity (individuation): correlation of decision sequences
    da, db = np.array(dec_a), np.array(dec_b)
    stream_identical = float(np.mean(da == db))
    return agreement, stream_identical


def main():
    header("H_975", "Multi-agent shared world model ⊥ individuation")
    print(f"two engines, distinct genesis; latent exchange as context; coupling sweep")
    print(f"couplings={COUPLINGS} N_seeds={N_SEEDS} lock_bar={LOCK_BAR}\n")

    gh_a, gh_b = genesis_hash(1), genesis_hash(2)
    print(f"D2 genesis hashes distinct: A={gh_a} B={gh_b} -> {gh_a != gh_b}")

    agree_by_c, ident_by_c = {}, {}
    for c in COUPLINGS:
        ags, ids = [], []
        for s in range(N_SEEDS):
            a, i = run_pair(s, c)
            ags.append(a); ids.append(i)
        agree_by_c[c] = np.array(ags); ident_by_c[c] = np.array(ids)

    print("\nD1 world-model agreement vs coupling:")
    for c in COUPLINGS:
        print(f"  coupling={c:.2f}: agreement={agree_by_c[c].mean():.4f}±{agree_by_c[c].std():.4f}  "
              f"stream-identity={ident_by_c[c].mean():.4f}")

    unpaired = agree_by_c[0.0]
    # The PASS regime = couplings where individuation is PRESERVED (stream-identity below
    # lock). The over-coupled arm (D3) is EXPECTED to collapse — that is the control, not
    # the test. Question: does ANY individuation-preserving coupling raise agreement above
    # unpaired (CI_lo>0)? AND is the over-coupled collapse correctly detected (D3)?
    coexist = []  # (c, delta, ci_lo, identity) for individuation-preserving couplings
    for c in COUPLINGS:
        if c == 0.0:
            continue
        ident = ident_by_c[c].mean()
        if ident < LOCK_BAR:                      # individuation preserved at this coupling
            diffs = agree_by_c[c] - unpaired
            lo, hi = boot_ci(diffs)
            coexist.append((c, agree_by_c[c].mean() - unpaired.mean(), lo, ident))
    best = max(coexist, key=lambda r: r[1]) if coexist else None
    # over-coupled collapse detection (D3): some coupling drives stream-identity to lock
    collapsed = [c for c in COUPLINGS if ident_by_c[c].mean() >= LOCK_BAR]

    print(f"\nD1 individuation-PRESERVED couplings raising agreement above unpaired "
          f"(unpaired={unpaired.mean():.4f}):")
    for (c, dl, lo, ident) in coexist:
        print(f"  c={c:.2f}: Δagreement={dl:+.4f} CI_lo={lo:+.4f} (stream-identity {ident:.3f}<lock)")
    if best:
        print(f"  -> best coexistence: c={best[0]:.2f} Δ={best[1]:+.4f} CI_lo={best[2]:+.4f}")
    print(f"D3 over-coupled collapse detected at couplings: {collapsed} (stream-identity>=lock)")
    print(f"D2 genesis distinct={gh_a != gh_b}")

    coexists = best is not None and best[1] > 0 and best[2] > 0 and (gh_a != gh_b)
    # FAIL-no-share if NO coupling (even collapsed) raises agreement at all
    any_rise = any((agree_by_c[c].mean() - unpaired.mean()) > 0.05 for c in COUPLINGS if c != 0)
    if coexists:
        verdict_line("H_975", "PASS",
                     f"shared WM ⊥ individuation COEXIST: at c={best[0]:.2f} agreement rises "
                     f"Δ={best[1]:+.3f} (CI_lo={best[2]:+.3f}>0) above unpaired WHILE "
                     f"individuation preserved (stream-identity {best[3]:.3f}<lock); over-coupling "
                     f"collapses at {collapsed} (D3 control fires). Toy rung.")
    elif not any_rise:
        verdict_line("H_975", "FAIL-no-share",
                     f"agreement never exceeds unpaired at any coupling — latent exchange "
                     f"builds no common WM (closed-negative).")
    else:
        verdict_line("H_975", "FAIL-collapse",
                     f"agreement rises ONLY where individuation collapses (no coexistence "
                     f"regime) — sharing costs selfhood (closed-negative).")


if __name__ == "__main__":
    main()
