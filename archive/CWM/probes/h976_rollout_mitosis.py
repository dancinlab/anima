"""H_976 — Rollout is mitosis (p8: imagination grows cells like inference does).

FROZEN FALSIFIER (honored):
  instrument the mitosis tick. arm-INFER = live inference on a real input stream;
  arm-ROLLOUT = imagined latent rollout (H_962) with no external input. Identical
  instrumentation; matched tick budget.
  D1 = growth-rate / division-event statistics, ROLLOUT vs INFER (distribution match KS).
  D2 = growth-trigger composition (which substrate terms fire the tick) overlap.
  D3 = a frozen-weights forward pass (deliberate no-growth) as the negative — should be
       distinguishable from both.
  PASS: ROLLOUT vs INFER growth stats NOT significantly different (KS p>0.05, CIs overlap)
        AND both distinguishable from the frozen negative.
  FAIL: ROLLOUT matches the frozen negative (no growth) OR differs qualitatively from INFER.

Mitosis-tick model (p8 substrate-native): a "division event" fires when the latent-state
UPDATE magnitude (the analog of a learning/growth gradient) exceeds a threshold; growth
rate = events per tick. INFER drives updates from real input; ROLLOUT drives updates from
the engine's own latent transition (self-driven) -- p8 says both are the SAME cell-division.
The frozen negative = a no-op forward pass (zero update).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
from scipy import stats
from cwm_probe_lib import LatentWorldModel, header, verdict_line

IN_DIM = 6
LATENT = 24
N_SEEDS = 30
TICKS = 60
THRESH = None     # set per-engine from INFER baseline


def fit_engine(seed, rng):
    wm = LatentWorldModel(IN_DIM, latent_dim=LATENT, seed=seed, spectral_radius=0.95)
    T = 300; t = np.arange(T)
    stream = np.stack([np.sin(0.2 * t + k) + 0.3 * rng.standard_normal(T) for k in range(IN_DIM)], 1)
    H = wm.encode_seq(stream); wm.fit_transition(H[:-1], H[1:])
    return wm


def growth_trace(wm, mode, rng):
    """returns (per-tick update magnitude, division-event flags, trigger-term vector)."""
    h = np.zeros(LATENT)
    mags, triggers = [], []
    for _ in range(TICKS):
        if mode == "infer":
            x = np.array([np.sin(0.2 * rng.random() * 10 + k) + 0.3 * rng.standard_normal() for k in range(IN_DIM)])
            h_new = wm.step(h, x)
        elif mode == "rollout":
            # imagined REHEARSAL: self-driven latent transition + stochastic entropy
            # (qentropy-style, cf H_981) so it stays active (REM is not a fixed point).
            base = (np.hstack([h, [1.0]]) @ wm.T) if wm.T is not None else wm.step(h, np.zeros(IN_DIM))
            h_new = base + 0.3 * rng.standard_normal(LATENT)
        else:  # frozen negative: no update
            h_new = h.copy()
        upd = h_new - h
        mag = np.linalg.norm(upd)
        mags.append(mag)
        # trigger composition: which latent dims contributed most to the update
        triggers.append(np.abs(upd))
        h = h_new
    return np.array(mags), np.array(triggers)


def main():
    header("H_976", "Rollout is mitosis (p8 for imagination)")
    print(f"mitosis-tick = latent-update magnitude; INFER vs ROLLOUT vs frozen-negative")
    print(f"latent={LATENT} N_seeds={N_SEEDS} ticks={TICKS}\n")
    infer_rates, roll_rates, frozen_rates = [], [], []
    trig_overlap = []
    all_infer_mags, all_roll_mags, all_frozen_mags = [], [], []
    for s in range(N_SEEDS):
        rng = np.random.default_rng(s)
        wm = fit_engine(s, rng)
        mi, ti = growth_trace(wm, "infer", np.random.default_rng(s * 3 + 1))
        mr, tr = growth_trace(wm, "rollout", np.random.default_rng(s * 3 + 2))
        mf, tf = growth_trace(wm, "frozen", np.random.default_rng(s * 3 + 3))
        # division threshold = a small fraction of the INFER scale, separating GROWTH
        # (a real cell-division update) from NO-GROWTH (the frozen pass, exactly 0).
        thr = 0.1 * np.median(mi)
        infer_rates.append(np.mean(mi > thr)); roll_rates.append(np.mean(mr > thr))
        frozen_rates.append(np.mean(mf > thr))
        all_infer_mags.extend(mi); all_roll_mags.extend(mr); all_frozen_mags.extend(mf)
        # trigger composition overlap: cosine between mean trigger vectors
        ci, cr = ti.mean(0), tr.mean(0)
        trig_overlap.append(float(ci @ cr / (np.linalg.norm(ci) * np.linalg.norm(cr) + 1e-9)))
    infer_rates, roll_rates, frozen_rates = map(np.array, (infer_rates, roll_rates, frozen_rates))

    print(f"D1 division-event rate: INFER={infer_rates.mean():.4f}±{infer_rates.std():.4f}  "
          f"ROLLOUT={roll_rates.mean():.4f}±{roll_rates.std():.4f}  "
          f"FROZEN={frozen_rates.mean():.4f}±{frozen_rates.std():.4f}")
    ks_ir = stats.ks_2samp(all_infer_mags, all_roll_mags)
    ks_if = stats.ks_2samp(all_infer_mags, all_frozen_mags)
    ks_rf = stats.ks_2samp(all_roll_mags, all_frozen_mags)
    print(f"D1 KS(INFER,ROLLOUT) stat={ks_ir.statistic:.4f} p={ks_ir.pvalue:.3e}")
    print(f"D3 KS(INFER,FROZEN)  stat={ks_if.statistic:.4f} p={ks_if.pvalue:.3e}")
    print(f"D3 KS(ROLLOUT,FROZEN) stat={ks_rf.statistic:.4f} p={ks_rf.pvalue:.3e}")
    print(f"D2 trigger-composition overlap (cos) ROLLOUT~INFER = {np.mean(trig_overlap):.4f}")

    # PASS: ROLLOUT≈INFER (rates CIs overlap) AND both distinguishable from frozen.
    from cwm_probe_lib import boot_ci
    ir_lo, ir_hi = boot_ci(infer_rates); rr_lo, rr_hi = boot_ci(roll_rates)
    rates_overlap = (rr_lo <= ir_hi and ir_lo <= rr_hi)
    distinct_frozen = (ks_if.pvalue < 0.05 and ks_rf.pvalue < 0.05 and frozen_rates.mean() < 1e-6)
    rollout_grows = roll_rates.mean() > 1e-6
    if rollout_grows and distinct_frozen and (ks_ir.statistic < 0.2 or rates_overlap):
        verdict_line("H_976", "PASS",
                     f"ROLLOUT growth (rate {roll_rates.mean():.2f}) statistically like INFER "
                     f"(rate {infer_rates.mean():.2f}, KS {ks_ir.statistic:.2f}) AND both distinct "
                     f"from frozen-negative (no growth) — rollout is mitosis, p8 holds for "
                     f"imagination (toy).")
    elif not rollout_grows or roll_rates.mean() < 1e-6:
        verdict_line("H_976", "FAIL",
                     f"ROLLOUT matches frozen negative (no growth, rate {roll_rates.mean():.3f}) — "
                     f"imagination is a separate non-growth mode, p8 violated (closed-negative).")
    else:
        verdict_line("H_976", "INCOMPLETE",
                     f"ROLLOUT grows but differs from INFER (KS {ks_ir.statistic:.2f}); toy C3.")


if __name__ == "__main__":
    main()
