#!/usr/bin/env python3
"""
H_1537 — NOREPINEPHRINE as a NETWORK-RESET FACULTY (unexpected-uncertainty detector)
         numpy DIRECTIONAL mirror (engine-native R2 deferred ING).

REFRAME (a_no_llm_frame_trap, a_break_the_wall): 13 prior NE lenses treated NE as a
scalar GAIN/TEMPERATURE knob over an existing controller and were INERT against a tuned
fixed gain (the peeled meta-law). NE's real computation (Bouret & Sara 2005 "network
reset"; Yu & Dayan 2005 "unexpected uncertainty") is a PHASIC NETWORK RESET on a detected
CONTEXT/REGIME change: ABANDON the stale model, trigger re-learning. This is a faculty
anima LACKS — "the world changed → flush the stale context, don't keep fitting it."

CAPABILITY = ABRUPT CONTEXT-SWITCH adaptation: the input->output mapping (rule) flips
abruptly at UNKNOWN times; measure POST-SWITCH RECOVERY speed. A reset faculty recovers
fast; a slow-adaptation baseline lags (must un-learn the stale mapping). PRESENCE test
(faculty adds fast reswitch), frozen-first, NO tune-to-green. Honest if reset doesn't win.

Bars in state/verdicts/1537_nt_norepinephrine/H_1537_FREEZE.txt (pre-registered).
"""
import json
import numpy as np

# ---- FROZEN PARAMETERS (pre-registered, H_1537_FREEZE.txt) --------------------
D          = 24            # feature dim
T          = 2400          # ticks
HAZARD     = 0.01          # rule-switch hazard (abrupt, unknown times)
W_REC      = 20            # recovery window after each switch
P_NOISE    = 0.05          # label-flip noise
ALPHA_GRID = [0.02, 0.05, 0.1, 0.2, 0.4]
SEEDS      = [1537, 1538, 1539]
# NE-RESET faculty (frozen):
RESET_DECAY   = 0.85       # flush: w_hat *= (1 - RESET_DECAY)  (toward neutral prior 0)
RESET_K       = 2.5        # phasic threshold: fire when surprise > mean + K*std (running)
REFRACTORY    = 8          # ticks between allowed resets
SURP_HALFLIFE = 30         # running surprise-scale EMA halflife
# bars:
C1_MIN   = 0.10
C2_TOL   = 0.02
C3_MIN   = 0.05
# ------------------------------------------------------------------------------

def sign(z):
    return 1.0 if z >= 0 else -1.0

def gen_stream(rng):
    """Shared per-seed stream: inputs x_t, switch times, hidden rule weights, labels.
    The SAME stream feeds every arm so only the controller differs."""
    xs = rng.standard_normal((T, D))
    # rule sequence: start with rule 0, switch with hazard to a fresh random hyperplane
    switch_mask = rng.random(T) < HAZARD
    switch_mask[0] = False
    rules = []           # w_r active at each tick
    switch_ticks = []
    w_cur = rng.standard_normal(D)
    for t in range(T):
        if switch_mask[t]:
            w_new = rng.standard_normal(D)
            # ensure it is a DIFFERENT rule (flip if too aligned)
            while np.dot(w_new, w_cur) / (np.linalg.norm(w_new) * np.linalg.norm(w_cur) + 1e-9) > 0.6:
                w_new = rng.standard_normal(D)
            w_cur = w_new
            switch_ticks.append(t)
        rules.append(w_cur)
    rules = np.array(rules)
    # labels with noise
    clean = np.array([sign(np.dot(rules[t], xs[t])) for t in range(T)])
    flip = rng.random(T) < P_NOISE
    ys = clean.copy()
    ys[flip] *= -1.0
    return xs, ys, np.array(switch_ticks)

def run_learner(xs, ys, switch_ticks, alpha, reset_mode, reset_ticks_override=None):
    """Online delta-rule linear learner.
       reset_mode: 'none' | 'surprise' | 'override'
       returns per-tick correctness array + fired reset ticks."""
    w_hat = np.zeros(D)
    correct = np.zeros(T)
    # running surprise scale (EMA mean/var of |error magnitude|)
    decay = 0.5 ** (1.0 / SURP_HALFLIFE)
    s_mean, s_var, last_reset = 0.0, 1.0, -10 ** 9
    fired = []
    override = set(reset_ticks_override) if reset_ticks_override is not None else set()
    for t in range(T):
        x = xs[t]
        pred = sign(np.dot(w_hat, x))
        correct[t] = 1.0 if pred == ys[t] else 0.0
        # surprise BEFORE updating (margin-based: how wrong/uncertain)
        margin = np.dot(w_hat, x)
        err_mag = abs(ys[t] - np.tanh(margin))   # in [0,2]; large when confidently wrong
        # update running surprise scale
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
            w_hat *= (1.0 - RESET_DECAY)   # FLUSH stale context toward neutral prior
            s_mean, s_var = 0.0, 1.0        # reset surprise scale (re-acquire)
            last_reset = t
            fired.append(t)
        # delta-rule update on prediction error
        w_hat = w_hat + alpha * (ys[t] - np.dot(w_hat, x)) * x / (np.dot(x, x) + 1e-6)
    return correct, fired

def post_switch_recovery(correct, switch_ticks):
    """Mean accuracy over the W_REC ticks immediately following each switch."""
    accs = []
    for s in switch_ticks:
        lo, hi = s, min(s + W_REC, T)
        if hi > lo:
            accs.append(correct[lo:hi].mean())
    return float(np.mean(accs)) if accs else float('nan')

def learnable_regime_diagnostic():
    """NON-GATING (a_break_the_wall multi-lens). Recurring-prototype task where each rule
    IS learnable (high asymptote) so the baseline genuinely lags after a switch and a flush
    has real stale context to clear. Measures whether the reset earns recovery EVEN in the
    regime most favorable to it, vs the STRONGEST swept fixed gain. Frozen-first: this does
    NOT move the c1/c2/c3 bars; it only characterizes WHY the faculty walls."""
    Dd, Td, Hz, Wr, NP = 8, 4000, 0.004, 25, 0.0
    def runl(xs, ys, st, alpha, mode='none', decay=0.85, reset_k=2.0, refr=8):
        w = np.zeros(Dd); cor = np.zeros(Td); sm, sv, last = 0.0, 1.0, -10 ** 9
        dec = 0.5 ** (1 / 30); fired = []
        for t in range(Td):
            x = xs[t]; cor[t] = 1.0 if sign(np.dot(w, x)) == ys[t] else 0.0
            em = abs(ys[t] - np.tanh(np.dot(w, x)))
            sm = dec * sm + (1 - dec) * em; sv = dec * sv + (1 - dec) * (em - sm) ** 2
            ss = np.sqrt(max(sv, 1e-9))
            if mode == 'surprise' and em > sm + reset_k * ss and (t - last) > refr:
                w *= (1 - decay); sm, sv = 0.0, 1.0; last = t; fired.append(t)
            w = w + alpha * (ys[t] - np.dot(w, x)) * x / (np.dot(x, x) + 1e-6)
        return cor, fired
    def recl(c, st):
        return float(np.mean([c[s + k] for s in st for k in range(Wr) if s + k < Td]))
    rows = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        protos = rng.standard_normal((12, Dd)); idx = rng.integers(0, 12, Td)
        xs = protos[idx]; sw = rng.random(Td) < Hz; sw[0] = False
        w_cur = rng.standard_normal(Dd); rules = []; st = []
        for t in range(Td):
            if sw[t]:
                w_cur = rng.standard_normal(Dd); st.append(t)
            rules.append(w_cur)
        rules = np.array(rules); st = np.array(st)
        ys = np.array([sign(np.dot(rules[t], xs[t])) for t in range(Td)])
        ba, br = 0.1, -1.0
        for a in [0.1, 0.2, 0.3, 0.4, 0.6]:
            c, _ = runl(xs, ys, st, a, 'none'); r = recl(c, st)
            if r > br: br, ba = r, a
        cb, _ = runl(xs, ys, st, ba, 'none'); Rb = recl(cb, st)
        cn, fired = runl(xs, ys, st, ba, 'surprise'); Rn = recl(cn, st)
        pre = [cb[s - 1 - j] for s in st for j in range(5) if s - 1 - j >= 0]
        rows.append({"seed": seed, "alpha_star": ba, "asymptote": round(float(np.mean(pre)), 3),
                     "R_base": round(Rb, 4), "R_ne": round(Rn, 4),
                     "ne_minus_base": round(Rn - Rb, 4), "n_resets": len(fired)})
    return {"note": "NON-GATING diagnostic (learnable-rule regime); bars NOT moved",
            "per_seed": rows,
            "mean_asymptote": round(float(np.mean([r["asymptote"] for r in rows])), 3),
            "mean_ne_minus_base": round(float(np.mean([r["ne_minus_base"] for r in rows])), 4)}


def main():
    per_seed = []
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        xs, ys, switch_ticks = gen_stream(rng)

        # --- sweep alpha* for the NO-NE baseline (strongest fixed-gain champion) ---
        best_alpha, best_rec = ALPHA_GRID[0], -1.0
        for a in ALPHA_GRID:
            c, _ = run_learner(xs, ys, switch_ticks, a, 'none')
            r = post_switch_recovery(c, switch_ticks)
            if r > best_rec:
                best_rec, best_alpha = r, a
        alpha = best_alpha

        # NO-NE (baseline slow-adaptation, tuned alpha*)
        c_none, _ = run_learner(xs, ys, switch_ticks, alpha, 'none')
        R_none = post_switch_recovery(c_none, switch_ticks)

        # NE-RESET (surprise-triggered network reset faculty)
        c_ne, fired = run_learner(xs, ys, switch_ticks, alpha, 'surprise')
        R_ne = post_switch_recovery(c_ne, switch_ticks)

        # ABL (detector always OFF -> reverts to NO-NE base)
        c_abl, _ = run_learner(xs, ys, switch_ticks, alpha, 'none')  # threshold=+inf == none
        R_abl = post_switch_recovery(c_abl, switch_ticks)

        # SHUFFLE (same NUMBER of resets, but at permuted random tick positions,
        #          decoupled from real surprise/switch times)
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

        per_seed.append({
            "seed": seed, "alpha_star": alpha, "n_switches": int(len(switch_ticks)),
            "n_resets_fired": n_fired,
            "R_NO_NE": round(R_none, 4), "R_NE_RESET": round(R_ne, 4),
            "R_ABL": round(R_abl, 4), "R_SHUFFLE": round(R_shuf, 4),
            "ne_minus_none": round(R_ne - R_none, 4),
            "ne_minus_shuf": round(R_ne - R_shuf, 4),
            "abl_minus_none": round(R_abl - R_none, 4),
        })

    # aggregate
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

    # --- SECONDARY DIAGNOSTIC (NON-GATING, a_break_the_wall multi-lens) ----------
    # The pre-registered regime (D=24, HAZARD=0.01, P_NOISE=0.05) makes EACH rule
    # barely learnable in the inter-switch interval (asymptote ~0.56-0.68) -> there is
    # little "stale confident context" to flush. To classify the wall honestly we ALSO
    # measure in a LEARNABLE regime (recurring input prototypes, low noise, longer
    # inter-switch intervals) where the baseline DOES reach high asymptote (~0.9) and
    # genuinely lags after a switch. This is a DIAGNOSTIC, NOT a re-frozen bar.
    diag = learnable_regime_diagnostic()
    # -----------------------------------------------------------------------------

    verdict = "🧱 WALL" if not green else "🟢 GREEN"
    result = {
        "hypothesis": "H_1537",
        "title": "NOREPINEPHRINE as a NETWORK-RESET FACULTY (unexpected-uncertainty detector)",
        "frame": "NE-as-reset-faculty (Bouret&Sara 2005 network reset; Yu&Dayan 2005 unexpected uncertainty) — NOT a gain knob",
        "substrate": "numpy DIRECTIONAL mirror (engine-native R2 deferred ING)",
        "seeds": SEEDS,
        "per_seed": per_seed,
        "aggregate": {
            "mean_R_NO_NE": round(m("R_NO_NE"), 4),
            "mean_R_NE_RESET": round(m("R_NE_RESET"), 4),
            "mean_R_ABL": round(m("R_ABL"), 4),
            "mean_R_SHUFFLE": round(m("R_SHUFFLE"), 4),
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
        "secondary_diagnostic_learnable_regime": diag,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result

if __name__ == "__main__":
    main()
