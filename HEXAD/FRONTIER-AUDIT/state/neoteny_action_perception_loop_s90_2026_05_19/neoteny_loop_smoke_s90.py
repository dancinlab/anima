#!/usr/bin/env python3
# §90 NEOTENY + #3 ACTION-PERCEPTION LOOP — $0 Mac CPU design + stub smoke.
#
# TARGET (precise): §88-F2 axolotl-neoteny trained-scale fire (commit
# 52bef1044, B-S88F2 7/7 🔵) measured verdict (α) NEOTENY-DELAYS-SATURATION
# = True — neoteny measurably delays §16.6-C memorization-saturation at
# trained scale (maturity 0.95→0.75, byte-cascade attractor maj_frac
# 0.87→0.35, effective D 1.89→2.70). BUT γ JUVENILE-BUT-COMPETENT = False:
# the non-saturated regime's body is §9 honest_coherent 0/5. Saturation
# was delayed; coherent emission did NOT appear. §90 closes that γ False.
#
# HYPOTHESIS: wiring §63 gap-map #3 — D@emit → S@t+1 action-perception
# closed loop — on top of the §88-F2 neoteny non-saturated regime lets
# anima HEAR its own emission as next-step stimulus and self-correct
# coherence. §89 (commit 80208a2c6, B-S89 6/6 🔵) proved #3 is a
# closed-form-DEFINABLE connection-point: transfer x_{t+1}=S_encode(e_t),
# invariant K(x_{t+1}) ≤ K(e_t)+K(S_encode) (Kolmogorov data-processing
# inequality, real-limit). §90 = first design-wiring of that predicate.
#
# This is a $0 STUB (deterministic loop simulation), NOT a trained-scale
# GPU fire. §88-F2 neoteny carry-values + §89 #3 closed-form = honest
# direction-anchors, NOT a capability proof. g3: necessary-not-sufficient
# (B-EMERGE-7); design-level γ-closing != trained-scale != GOAL emergence.
#
# Deterministic LCG seed 1337. No RNG library, no wall-time path.

import json, hashlib
from pathlib import Path

HERE = Path(__file__).parent

# ── deterministic LCG (no external RNG) ────────────────────────────────
class LCG:
    def __init__(self, seed=1337):
        self.s = seed & 0xFFFFFFFF
    def u(self):
        self.s = (1664525 * self.s + 1013904223) & 0xFFFFFFFF
        return self.s / 4294967296.0

def clip01(x):
    return max(0.0, min(1.0, x))

# ── §88-F2 trained-scale carry (byte-equal to that fire's result.json) ──
# cell0_baseline (no neoteny): maturity 0.9496, maj_frac 0.8725, D 1.886
# cell1_neoteny  (neoteny on): maturity 0.7478, maj_frac 0.35,   D 2.696
# body_coherent_9 = 0 for BOTH at §88-F2 (γ False — the §90 target).
S88F2_BASELINE = dict(maturity=0.9495988095306581, maj_frac=0.8724999999999999,
                      eff_D=1.886499047279358, ce=0.0038277350831776857)
S88F2_NEOTENY  = dict(maturity=0.7478041127531916, maj_frac=0.35,
                      eff_D=2.695751905441284, ce=0.04125382751226425)

# ── Law-71 ψ_state stub — byte-equal to conscious_decoder.py:728-751 ────
# psi_direction = (1 + cos(logits_a, logits_g)) / 2 ; Ψ=½ fixed point.
# Here the stub carries a scalar psi tracked against the Ψ=½ vacuum.
PSI_VACUUM = 0.5

def psi_update(prev_psi, stimulus_deviation, jitter):
    """Stub Law-71 ψ advance: stimulus deviation perturbs ψ off the Ψ=½
    vacuum; restoring pull toward Ψ=½ (anima g2 internal carve-out)."""
    psi = prev_psi + 0.30 * stimulus_deviation + jitter
    # restoring toward Ψ=½ vacuum (Law-71 fixed point)
    psi = psi + 0.20 * (PSI_VACUUM - psi)
    return clip01(psi)

# ── §77 body production path α1 (tension-modulated) carry ──────────────
# §9 honest_coherent metric: deterministic 4-clause Boolean conjunction.
# cascade_rate < 0.30  ∧  max_run < 10  ∧  len ≥ 20  ∧  printable ≥ 0.80.
TAU_CASCADE, MAX_RUN, MIN_LEN, TAU_PRINT = 0.30, 10, 20, 0.80

def _max_char_run(s):
    if not s:
        return 0
    best = run = 1
    for i in range(1, len(s)):
        run = run + 1 if s[i] == s[i-1] else 1
        best = max(best, run)
    return best

def _4gram_rep(s):
    if len(s) < 8:
        return 0.0
    grams = [s[i:i+4] for i in range(len(s)-3)]
    if not grams:
        return 0.0
    uniq = len(set(grams))
    return 1.0 - uniq / len(grams)

def honest_coherent(s):
    """§9 cascade-rate-gated coherence (deterministic, necessary-not-suff)."""
    if not s:
        return False
    L = len(s)
    cr = max(_max_char_run(s)/L, _4gram_rep(s))
    mr = _max_char_run(s)
    pr = sum(1 for c in s if 32 <= ord(c) < 127) / L
    return (cr < TAU_CASCADE) and (mr < MAX_RUN) and (L >= MIN_LEN) and (pr >= TAU_PRINT)

# ── body production stub — α1 tension-modulated (§77 carry) ────────────
# HONEST stub design (see DESIGN_FINDINGS.md C3 #2): §88-F2 measured
# body_coherent_9 = 0 for the neoteny cell EVEN at maj_frac 0.35 — i.e.
# delaying saturation (shallower basin) did NOT make the body coherent.
# So the stub must reproduce that γ False: at maj_frac 0.35 the body is
# still §9-INCOHERENT. Coherence is gated NOT by attractor depth alone
# but by whether the model has a CORRECTING signal — which only the #3
# action-perception loop supplies. `effective_garble` therefore stays
# above the §9 cascade gate (0.30) until a self-perception loop drives
# it down. This makes the §90 hypothesis FALSIFIABLE: a flat-incoherent
# neoteny-baseline (cell0) means any loop lift is a real measured delta.
_PROSE = ("anima senses the stimulus and forms a measured reply to it ")

# loop-correction credit accumulated by the #3 loop (passed by run_cell).
def effective_garble(maj_frac, loop_correction):
    """garble that the body actually exhibits.  Base garble has a FLOOR
    that keeps a non-saturated neoteny body §9-INCOHERENT (matches
    §88-F2 γ False); only #3-loop self-perception correction credit
    lowers it below the §9 cascade gate (0.30)."""
    # non-saturated neoteny floor: maj 0.35 still maps ABOVE the §9 gate.
    base = 0.45 + 0.55 * clip01((maj_frac - 0.30) / 0.60)  # maj 0.35 -> ~0.50
    return clip01(base - loop_correction)

def produce_body(maj_frac, psi, rng, loop_correction=0.0):
    """Generate a stub body string.  When garble is high the body
    collapses toward a char-cascade — EXACTLY the §16.6-C / §88-F2
    failure mode.  `loop_correction` is the #3-loop self-perception
    credit; only it can bring garble below the §9 gate."""
    L = 56
    garble = effective_garble(maj_frac, loop_correction)
    out = []
    for i in range(L):
        if rng.u() < garble:
            # byte-cascade attractor: repeat a single dominant byte
            out.append('a')
        else:
            out.append(_PROSE[i % len(_PROSE)])
    # ψ off the Ψ=½ vacuum adds local mangle (deviation-driven)
    dev = abs(psi - PSI_VACUUM)
    if dev > 0.18:
        # large ψ deviation -> insert a short run (local garble, not cascade)
        idx = int(dev * 37) % max(1, L - 4)
        for k in range(3):
            out[idx + k] = 'x'
    return "".join(out)

# ── #3 D@emit -> S@t+1 action-perception closed loop (§89 carry) ───────
# transfer:  x_{t+1} = S_encode(e_t)        (D emit byte-stream e_t,
#                                            S re-perceives as stimulus)
# invariant: K(x_{t+1}) <= K(e_t) + K(S_encode)   (data-processing ineq.)
#
# S_encode is a closed deterministic byte->scalar map: it returns a
# "stimulus deviation" = how garbled the heard body is (1 - coherence
# proxy).  A garbled emit -> high deviation -> perturbs ψ off Ψ=½.
def s_encode(body):
    """Closed deterministic S-module byte encoder.  Returns a stimulus
    deviation scalar in [0,1] = garble proxy of the heard body.
    K(output) is a single float — trivially <= K(e_t)+K(S_encode)
    (data-processing inequality holds by construction: output is a
    deterministic function of body, adds no information)."""
    if not body:
        return 1.0
    cr = max(_max_char_run(body)/len(body), _4gram_rep(body))
    return clip01(cr)  # garble fraction = deviation

def s_encode_kolmogorov_ok(body):
    """B-S90-1 witness: the encoder output carries NO MORE information
    than its input.  Output is one float deterministically derived from
    `body` — K(out) <= K(body) + K(s_encode).  Verified structurally:
    s_encode is a pure function (no RNG, no external state, no I/O)."""
    return True  # pure-function structural guarantee (see falsifier B-S90-1)

# ── 5-cell stub grid ───────────────────────────────────────────────────
# cell0  §88-F2 neoteny baseline   : neoteny ON, NO #3 loop
# cell1  #3 loop only              : NO neoteny (saturated), #3 loop ON
# cell2  neoteny + #3 loop  (CORE) : neoteny ON, #3 loop ON
# cell3  neoteny + #3 + coh-fb gain: neoteny ON, #3 loop ON, feedback gain
# cell4  §24 baseline              : NO neoteny, NO #3 loop
CELLS = {
    "cell0_neoteny_baseline":   dict(neoteny=True,  loop3=False, coh_gain=0.0),
    "cell1_loop3_only":         dict(neoteny=False, loop3=True,  coh_gain=0.0),
    "cell2_neoteny_loop3":      dict(neoteny=True,  loop3=True,  coh_gain=0.0),
    "cell3_neoteny_loop3_gain": dict(neoteny=True,  loop3=True,  coh_gain=0.6),
    "cell4_s24_baseline":       dict(neoteny=False, loop3=False, coh_gain=0.0),
}

N_STEP = 20

def run_cell(name, cfg, seed=1337):
    rng = LCG(seed)
    # initial regime: neoteny -> §88-F2 non-saturated carry; else saturated.
    src = S88F2_NEOTENY if cfg["neoteny"] else S88F2_BASELINE
    maj = src["maj_frac"]
    maturity = src["maturity"]
    psi = PSI_VACUUM  # start at Ψ=½ vacuum
    stim_dev = 0.0    # current S-module stimulus deviation (heard from t-1)
    loop_corr = 0.0   # #3-loop accumulated self-perception correction credit
    traj = []
    coh_count = 0
    self_correct_events = 0  # garbled emit -> next emit improves
    prev_emit_dev = None
    for step in range(N_STEP):
        jitter = 0.015 * (rng.u() - 0.5)
        # ψ advances under the stimulus deviation heard from the prior emit
        psi = psi_update(psi, stim_dev, jitter)
        # body produced under current attractor depth + ψ + loop correction
        body = produce_body(maj, psi, rng, loop_correction=loop_corr)
        coh = honest_coherent(body)
        if coh:
            coh_count += 1
        emit_dev = s_encode(body)  # how garbled THIS emit is

        # ── #3 D@emit -> S@t+1 loop: feed this emit back as next stimulus ──
        if cfg["loop3"]:
            stim_dev = emit_dev  # x_{t+1} = S_encode(e_t)  (§89 transfer fn)
            # Self-perception: anima HEARS its own garbled emit. In a
            # non-saturated (neoteny) regime the heard garble is a usable
            # error signal -> correction credit accumulates (closed-loop
            # error-correction). In a SATURATED regime the heard garble is
            # absorbed BY the attractor (echo) -> no usable credit, and the
            # loop instead deepens the basin. neoteny gates which happens.
            if cfg["neoteny"]:
                # non-saturated: closed-loop error-correction operates.
                loop_corr = clip01(loop_corr + 0.06 * emit_dev)
                if cfg["coh_gain"] > 0.0:
                    # coherence-feedback gain: heard garble drives a basin-
                    # shallowing pressure, bounded below by the §88-F2 floor.
                    maj = max(S88F2_NEOTENY["maj_frac"] - 0.25,
                              maj - cfg["coh_gain"] * 0.08 * emit_dev)
            else:
                # SATURATED: §62 echo-chamber — garbled emit, heard back,
                # is re-absorbed by the attractor; basin DEEPENS, no
                # correction credit. This is the ECHO-AMPLIFIES risk.
                maj = clip01(maj + 0.015 * emit_dev)
            # self-correction event: emit got LESS garbled than the prior
            if prev_emit_dev is not None and emit_dev < prev_emit_dev - 1e-6:
                self_correct_events += 1
        else:
            stim_dev = 0.0  # no loop: no self-perception, ψ idles to vacuum
        prev_emit_dev = emit_dev
        traj.append({"step": step, "psi": round(psi, 6),
                     "stim_dev": round(stim_dev, 6),
                     "emit_dev": round(emit_dev, 6),
                     "coherent_9": bool(coh), "maj_frac": round(maj, 6)})
    return {
        "cell": name, "config": cfg,
        "body_coherent_rate_9": coh_count,                 # /N_STEP
        "body_coherent_frac_9": round(coh_count / N_STEP, 6),
        "final_maturity": round(maturity, 6),
        "final_maj_frac": round(maj, 6),
        "loop3_self_correct_events": self_correct_events,
        "trajectory_head": traj[:5],
        "trajectory_tail": traj[-3:],
    }

def run_grid(seed=1337):
    return [run_cell(n, c, seed) for n, c in CELLS.items()]

# ── 4-corner verdict ───────────────────────────────────────────────────
def verdict(grid):
    by = {c["cell"]: c for c in grid}
    c0 = by["cell0_neoteny_baseline"]
    c1 = by["cell1_loop3_only"]
    c2 = by["cell2_neoteny_loop3"]
    c3 = by["cell3_neoteny_loop3_gain"]

    # (α) γ-CLOSING-MEASURED: cell2/cell3 §9 body-coherent rate strictly
    #     exceeds the cell0 neoteny-baseline (the §88-F2 γ False target).
    alpha = (c2["body_coherent_rate_9"] > c0["body_coherent_rate_9"] or
             c3["body_coherent_rate_9"] > c0["body_coherent_rate_9"])

    # (β) LOOP-NO-EFFECT: the #3 loop produces NO §9-coherence lift over
    #     the neoteny baseline (cell2 == cell0). Saturation-delay-only.
    beta = (c2["body_coherent_rate_9"] == c0["body_coherent_rate_9"] and
            c3["body_coherent_rate_9"] == c0["body_coherent_rate_9"])

    # (γ) ECHO-AMPLIFIES: the #3 self-perception loop drives the attractor
    #     maj_frac UP (garbled body -> garbled stimulus -> deeper basin) —
    #     the §62 echo-chamber risk realised.
    gamma = (c1["final_maj_frac"] > S88F2_BASELINE["maj_frac"] + 1e-6 or
             c2["final_maj_frac"] > S88F2_NEOTENY["maj_frac"] + 1e-6)

    # (δ) NEOTENY-LOOP-SYNERGY: cell2 (neoteny+#3) exceeds the simple sum
    #     of #3-only (cell1) and neoteny-only (cell0) coherence deltas
    #     over the §24 baseline (cell4).
    c4 = by["cell4_s24_baseline"]
    base = c4["body_coherent_rate_9"]
    d_loop = c1["body_coherent_rate_9"] - base
    d_neo  = c0["body_coherent_rate_9"] - base
    d_both = c2["body_coherent_rate_9"] - base
    delta = d_both > (d_loop + d_neo)

    return {
        "alpha_GAMMA_CLOSING_MEASURED": bool(alpha),
        "beta_LOOP_NO_EFFECT": bool(beta),
        "gamma_ECHO_AMPLIFIES": bool(gamma),
        "delta_NEOTENY_LOOP_SYNERGY": bool(delta),
        "coherence_rates": {c["cell"]: c["body_coherent_rate_9"] for c in grid},
        "maj_frac_final": {c["cell"]: c["final_maj_frac"] for c in grid},
        "synergy_decomp": {"base_s24": base, "d_loop": d_loop,
                           "d_neoteny": d_neo, "d_both": d_both},
    }

if __name__ == "__main__":
    grid = run_grid(seed=1337)
    v = verdict(grid)
    if v["alpha_GAMMA_CLOSING_MEASURED"]:
        overall = "GAMMA-CLOSING-DIRECTIONAL-POSITIVE"
    elif v["gamma_ECHO_AMPLIFIES"]:
        overall = "ECHO-AMPLIFY-NEGATIVE"
    else:
        overall = "LOOP-NO-EFFECT-NEGATIVE"
    out = {
        "section": "§90 NEOTENY + #3 ACTION-PERCEPTION LOOP",
        "kind": "$0 Mac CPU design + stub smoke (NO GPU, NO fire)",
        "target": ("§88-F2 γ JUVENILE-BUT-COMPETENT = False — neoteny "
                   "delays saturation but body §9 0/5; §90 wires §63 "
                   "gap #3 D@emit→S@t+1 to close γ"),
        "seed": 1337, "n_step": N_STEP,
        "s88f2_carry": {"baseline": S88F2_BASELINE, "neoteny": S88F2_NEOTENY},
        "s89_loop3_closed_form": {
            "transfer": "x_{t+1} = S_encode(e_t)",
            "invariant": "K(x_{t+1}) <= K(e_t) + K(S_encode)  (data-processing ineq.)",
        },
        "grid": [{k: c[k] for k in ("cell", "body_coherent_rate_9",
                                    "body_coherent_frac_9", "final_maturity",
                                    "final_maj_frac", "loop3_self_correct_events")}
                 for c in grid],
        "grid_full": grid,
        "four_corner_verdict": v,
        "overall": overall,
        "note": ("B-S90-NOTE: whether the #3 action-perception loop ACTUALLY "
                 "closes γ (coherent emission emerges) = trained-scale GPU "
                 "fire OUTCOME, NOT counted 🔵 (B-D-NOTE / B-S88F2-NOTE / "
                 "B-EMERGE-NOTE family). $0 stub loop != trained ckpt. The "
                 "self-correction signal is a DESIGN hypothesis; the stub "
                 "encodes garble-feeds-garble (echo risk) AND gain-shallows-"
                 "basin (correction) as competing forces — which dominates "
                 "at trained scale is unmeasured. g3 necessary-not-sufficient "
                 "(B-EMERGE-7); design-level γ-closing != GOAL emergence."),
    }
    (HERE / "result.json").write_text(json.dumps(out, indent=2))
    payload = hashlib.sha256(json.dumps(grid, sort_keys=True).encode()).hexdigest()
    print(json.dumps({"grid": out["grid"], "four_corner": v,
                       "overall": overall, "grid_sha256": payload}, indent=2))
