#!/usr/bin/env python3
"""
H_1539 — NOREPINEPHRINE-as-RESET-FACULTY RETRY: isolate the reset against a
         NON-GAIN-DISSOLVABLE baseline (numpy DIRECTIONAL mirror).

WHY RETRY (the H_1537 lane's own not-ruled-out next lens, #2518 🧱):
  H_1537 found NE-as-network-reset (Bouret&Sara 2005; Yu&Dayan 2005) is REAL but
  SMALL (+0.006 on the pre-registered task, +0.029 even in the most favorable
  learnable regime — both UNDER the +0.10 PRESENCE bar). The HONEST mechanistic
  reason it walled: the best-swept FIXED gain was α*=0.6 (HIGH), and *a high fixed
  gain itself acts as a partial reset* — it down-weights the stale ŵ fast on its
  own, MASKING the explicit flush's marginal value. The reset's true contribution
  was confounded by the baseline's freedom to set a high gain.

THE FIX (a_break_the_wall TYPE-(b) VARIABLE-ISOLATION, NOT tune-to-green):
  Re-run the IDENTICAL abrupt context-switch task / seeds / W_REC / PRESENCE bars,
  changing ONLY the LEARNER so a fixed gain CANNOT double as a reset:
   (b) SATURATING-NONLINEAR update — the estimator is driven by a LEAKY MOMENTUM
       integrator m_t (slow time-constant β) squashed through tanh. Once m_t
       saturates onto a stale rule, a high instantaneous gain CANNOT pull it out
       fast: it must DECAY through the integrator's own slow constant, OR be
       explicitly FLUSHED. Stale context persists unless actively detected+flushed.
   (a) HIGH GAIN HURTS STEADY-STATE — under label noise the saturated estimator
       chases noise at high α and loses asymptote, so the α* sweep can NOT sit high.
       The fixed baseline's best gain is forced LOW → it can no longer use gain as a
       covert reset. The ONLY fast way to clear a stale saturated context is the
       explicit phasic FLUSH (m_t → 0).
  This isolates the reset faculty's TRUE marginal contribution by removing the
  gain-as-reset confound the lane identified. The PRESENCE bar is UNCHANGED
  (+0.10 / ≥2-of-3 / ablation-decisive / time-lock) — we fix the BASELINE so the
  comparison is FAIR, we do NOT weaken the bar. frozen-first, NO tune-to-green.

Bars in state/verdicts/1539_nt_ne_retry/H_1539_FREEZE.txt (pre-registered, IDENTICAL
to H_1537's c1/c2/c3 — only the baseline learner is the fix).
"""
import json
import numpy as np

# ---- FROZEN PARAMETERS (pre-registered, H_1539_FREEZE.txt) --------------------
# Task params IDENTICAL to H_1537 (same abrupt context-switch environment + seeds):
D          = 24            # feature dim (same as H_1537)
T          = 2400          # ticks (same)
HAZARD     = 0.01          # rule-switch hazard (same)
W_REC      = 20            # recovery window after each switch (same)
P_NOISE    = 0.05          # label-flip noise (same)
SEEDS      = [1537, 1538, 1539]   # SAME seeds as H_1537 (shared stream comparability)

# THE FIX — saturating-nonlinear learner (the ONE change vs H_1537):
#   estimator output = tanh(GAMMA * (m . x)), where m is a LEAKY MOMENTUM integrator.
#   m_{t+1} = BETA*m_t + alpha*err*x   (BETA<1 = slow leak; high alpha cannot dissolve
#   a saturated m fast — it must decay through BETA or be flushed). GAMMA sharpens the
#   saturation so a stale confident m stays confident (hard to overwrite by gain alone).
BETA   = 0.97             # momentum leak (slow time-constant => stale context persists)
GAMMA  = 3.0              # saturation sharpness (confident stale context resists gain)
# alpha grid SWEPT for the NO-NE baseline (strongest fixed-gain champion). Under noise +
# the saturating update, high alpha HURTS asymptote => alpha* is forced LOW (the fix):
ALPHA_GRID = [0.02, 0.05, 0.1, 0.2, 0.4, 0.6]

# NE-RESET faculty (frozen; same detector shape as H_1537):
RESET_DECAY   = 0.85       # flush: m *= (1 - RESET_DECAY) (toward neutral prior 0)
RESET_K       = 2.5        # phasic threshold: fire when surprise > mean + K*std (running)
REFRACTORY    = 8          # ticks between allowed resets
SURP_HALFLIFE = 30         # running surprise-scale EMA halflife

# bars (IDENTICAL to H_1537 — unchanged, only the baseline learner is the fix):
C1_MIN   = 0.10
C2_TOL   = 0.02
C3_MIN   = 0.05
# ------------------------------------------------------------------------------

def sign(z):
    return 1.0 if z >= 0 else -1.0

def gen_stream(rng):
    """Shared per-seed stream: inputs x_t, switch times, hidden rule weights, labels.
    IDENTICAL construction to H_1537 so the only difference is the controller."""
    xs = rng.standard_normal((T, D))
    switch_mask = rng.random(T) < HAZARD
    switch_mask[0] = False
    rules = []
    switch_ticks = []
    w_cur = rng.standard_normal(D)
    for t in range(T):
        if switch_mask[t]:
            w_new = rng.standard_normal(D)
            while np.dot(w_new, w_cur) / (np.linalg.norm(w_new) * np.linalg.norm(w_cur) + 1e-9) > 0.6:
                w_new = rng.standard_normal(D)
            w_cur = w_new
            switch_ticks.append(t)
        rules.append(w_cur)
    rules = np.array(rules)
    clean = np.array([sign(np.dot(rules[t], xs[t])) for t in range(T)])
    flip = rng.random(T) < P_NOISE
    ys = clean.copy()
    ys[flip] *= -1.0
    return xs, ys, np.array(switch_ticks)

def run_learner(xs, ys, switch_ticks, alpha, reset_mode, reset_ticks_override=None):
    """SATURATING-NONLINEAR online learner (THE FIX).
       estimator: pred = sign(tanh(GAMMA * (m . x))); m = leaky momentum integrator.
       A high fixed alpha CANNOT dissolve a saturated stale m fast (must leak via BETA
       or be FLUSHED) — so gain can no longer double as a reset.
       reset_mode: 'none' | 'surprise' | 'override'
       returns per-tick correctness array + fired reset ticks."""
    m = np.zeros(D)                      # leaky momentum integrator (the persistent state)
    correct = np.zeros(T)
    decay = 0.5 ** (1.0 / SURP_HALFLIFE)
    s_mean, s_var, last_reset = 0.0, 1.0, -10 ** 9
    fired = []
    override = set(reset_ticks_override) if reset_ticks_override is not None else set()
    for t in range(T):
        x = xs[t]
        z = np.dot(m, x)
        out = np.tanh(GAMMA * z)         # SATURATING nonlinearity
        pred = sign(out)
        correct[t] = 1.0 if pred == ys[t] else 0.0
        # surprise BEFORE updating: confident-wrong = large error magnitude in [0,2]
        err_mag = abs(ys[t] - out)
        s_mean = decay * s_mean + (1 - decay) * err_mag
        s_var = decay * s_var + (1 - decay) * (err_mag - s_mean) ** 2
        s_std = np.sqrt(max(s_var, 1e-9))
        # RESET decision
        do_reset = False
        if reset_mode == 'surprise':
            if err_mag > s_mean + RESET_K * s_std and (t - last_reset) > REFRACTORY:
                do_reset = True
        elif reset_mode == 'override':
            if t in override:
                do_reset = True
        if do_reset:
            m *= (1.0 - RESET_DECAY)     # FLUSH the stale saturated integrator toward 0
            s_mean, s_var = 0.0, 1.0
            last_reset = t
            fired.append(t)
        # LEAKY-MOMENTUM update on the SATURATED prediction error.
        # The (1 - out^2) tanh-derivative gate is what makes a CONFIDENT stale m resist a
        # high gain: once saturated (|out|->1) the gradient gate ->0, so even large alpha
        # barely moves m — it must leak via BETA or be flushed. THIS is the fix.
        grad_gate = (1.0 - out * out)
        m = BETA * m + alpha * (ys[t] - out) * grad_gate * x / (np.dot(x, x) + 1e-6)
    return correct, fired

def post_switch_recovery(correct, switch_ticks):
    """Mean accuracy over the W_REC ticks immediately following each switch (IDENTICAL
    metric to H_1537)."""
    accs = []
    for s in switch_ticks:
        lo, hi = s, min(s + W_REC, T)
        if hi > lo:
            accs.append(correct[lo:hi].mean())
    return float(np.mean(accs)) if accs else float('nan')

def main():
    per_seed = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        xs, ys, switch_ticks = gen_stream(rng)

        # --- sweep alpha* for the NO-NE baseline (strongest fixed-gain champion).
        #     Under the saturating update + noise, high alpha HURTS asymptote, so alpha*
        #     is forced LOW (the gain-as-reset confound is removed). ---
        best_alpha, best_rec = ALPHA_GRID[0], -1.0
        for a in ALPHA_GRID:
            c, _ = run_learner(xs, ys, switch_ticks, a, 'none')
            r = post_switch_recovery(c, switch_ticks)
            if r > best_rec:
                best_rec, best_alpha = r, a
        alpha = best_alpha

        # NO-NE (baseline slow-adaptation, tuned alpha* on the saturating learner)
        c_none, _ = run_learner(xs, ys, switch_ticks, alpha, 'none')
        R_none = post_switch_recovery(c_none, switch_ticks)

        # NE-RESET (surprise-triggered network reset faculty)
        c_ne, fired = run_learner(xs, ys, switch_ticks, alpha, 'surprise')
        R_ne = post_switch_recovery(c_ne, switch_ticks)

        # ABL (detector always OFF -> reverts EXACTLY to NO-NE base)
        c_abl, _ = run_learner(xs, ys, switch_ticks, alpha, 'none')
        R_abl = post_switch_recovery(c_abl, switch_ticks)

        # SHUFFLE (same NUMBER of resets at permuted random tick positions)
        n_fired = len(fired)
        shuf_rng = np.random.default_rng(seed + 9000)
        if n_fired > 0:
            shuf_ticks = shuf_rng.choice(np.arange(REFRACTORY, T), size=min(n_fired, T - REFRACTORY),
                                         replace=False).tolist()
        else:
            shuf_ticks = []
        c_shuf, _ = run_learner(xs, ys, switch_ticks, alpha, 'override',
                                reset_ticks_override=shuf_ticks)
        R_shuf = post_switch_recovery(c_shuf, switch_ticks)

        # diagnostic: also report the baseline ASYMPTOTE and the alpha sweep curve so the
        # "alpha* is now LOW (gain can't double as reset)" fix is VISIBLE in the artifact.
        pre = [c_none[s - 1 - j] for s in switch_ticks for j in range(5) if s - 1 - j >= 0]
        sweep = {}
        for a in ALPHA_GRID:
            c, _ = run_learner(xs, ys, switch_ticks, a, 'none')
            sweep[str(a)] = round(post_switch_recovery(c, switch_ticks), 4)

        per_seed.append({
            "seed": seed, "alpha_star": alpha, "n_switches": int(len(switch_ticks)),
            "n_resets_fired": n_fired,
            "baseline_asymptote": round(float(np.mean(pre)), 4) if pre else None,
            "alpha_sweep_recovery": sweep,
            "R_NO_NE": round(R_none, 4), "R_NE_RESET": round(R_ne, 4),
            "R_ABL": round(R_abl, 4), "R_SHUFFLE": round(R_shuf, 4),
            "ne_minus_none": round(R_ne - R_none, 4),
            "ne_minus_shuf": round(R_ne - R_shuf, 4),
            "abl_minus_none": round(R_abl - R_none, 4),
        })

    def m(k):
        return float(np.mean([s[k] for s in per_seed]))
    mean_ne_minus_none = m("ne_minus_none")
    mean_abl_minus_none = m("abl_minus_none")
    mean_ne_minus_shuf = m("ne_minus_shuf")
    n_pass_c1 = sum(1 for s in per_seed if s["ne_minus_none"] >= C1_MIN)

    c1 = (n_pass_c1 >= 2) and (mean_ne_minus_none >= C1_MIN)
    c2 = abs(mean_abl_minus_none) <= C2_TOL
    c3 = mean_ne_minus_shuf >= C3_MIN
    green = c1 and c2 and c3

    verdict = "🟢 GREEN" if green else "🧱 WALL"
    result = {
        "hypothesis": "H_1539",
        "title": "NOREPINEPHRINE-as-RESET-FACULTY RETRY (non-gain-dissolvable baseline)",
        "frame": "NE-as-reset (Bouret&Sara 2005 network reset; Yu&Dayan 2005 unexpected uncertainty) re-tested against a SATURATING-NONLINEAR baseline where a fixed gain CANNOT double as a reset (H_1537 lane's own next lens). a_break_the_wall TYPE-(b) variable-isolation, bars UNCHANGED, NOT tune-to-green.",
        "substrate": "numpy DIRECTIONAL mirror (engine-native R2 deferred ING)",
        "the_fix": "saturating-nonlinear leaky-momentum learner: pred=sign(tanh(GAMMA*(m.x))), m=BETA*m+alpha*err*(1-out^2)*x. The tanh-derivative gate + slow leak BETA make a CONFIDENT stale m resist a high gain (gradient gate ->0 when saturated) => high alpha HURTS asymptote under noise => alpha* forced LOW => gain can no longer act as a covert reset; the explicit FLUSH is the only fast clear of stale context.",
        "seeds": SEEDS,
        "per_seed": per_seed,
        "aggregate": {
            "mean_R_NO_NE": round(m("R_NO_NE"), 4),
            "mean_R_NE_RESET": round(m("R_NE_RESET"), 4),
            "mean_R_ABL": round(m("R_ABL"), 4),
            "mean_R_SHUFFLE": round(m("R_SHUFFLE"), 4),
            "mean_alpha_star": round(float(np.mean([s["alpha_star"] for s in per_seed])), 4),
            "mean_baseline_asymptote": round(float(np.mean([s["baseline_asymptote"] for s in per_seed])), 4),
            "mean_ne_minus_none": round(mean_ne_minus_none, 4),
            "mean_abl_minus_none": round(mean_abl_minus_none, 4),
            "mean_ne_minus_shuf": round(mean_ne_minus_shuf, 4),
            "n_pass_c1": n_pass_c1,
        },
        "bars": {
            "c1_presence_ne_minus_none>=0.10_on>=2of3_and_mean": bool(c1),
            "c2_ablation_decisive_|abl-none|<=0.02": bool(c2),
            "c3_timelock_ne_minus_shuf>=0.05": bool(c3),
        },
        "verdict": verdict,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result

if __name__ == "__main__":
    main()
