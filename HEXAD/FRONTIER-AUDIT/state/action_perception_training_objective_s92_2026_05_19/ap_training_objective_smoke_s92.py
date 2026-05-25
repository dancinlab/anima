#!/usr/bin/env python3
# §92 — #3 ACTION-PERCEPTION AS TRAINING-TIME OBJECTIVE — $0 Mac CPU design + stub smoke.
#
# TARGET (precise): §91 (commit 9e5b38a29, B-S91 8/8 🔵) trained-scale fire of
# the §90 #3 D@emit→S@t+1 action-perception loop wired as a DECODE-TIME overlay.
# §91 verdict (β) ECHO-DOMINATES-AT-TRAINED: cell2 (neoteny ckpt + #3 decode-time
# loop) §9 honest_coherent 0/20, byte-cascade attractor maj_frac 0.35→0.689
# (WORSENED — anima re-perceives its own garbled emission and the attractor
# deepens), self-correct events 0. The §90 stub's cell2 §9 20/20 wiped out.
#
# §91's core honest conclusion: wiring #3 as a *decode-time overlay* produces
# echo-amplification, NOT self-correction — because the model was NEVER TRAINED
# to treat its own garbled emission as an error signal. self-correction must be
# a LEARNED capability; you cannot bolt it on at inference time.
#
# §92 = the direct successor: formalise #3 action-perception as a TRAINING-LOOP
# OBJECTIVE. Not a decode-time loop (§90/§91) — a loss term during training so
# anima learns "when I feed my own emission back as my own stimulus, the physics
# deviation should stay small" (self-coherent emission is one whose own re-
# perception leaves Ψ stable). honest diagnosis: §91 echo-amplify happened
# because the loop was never a training signal; a training-time objective gives
# anima the *chance* to learn self-coherence (it does not GUARANTEE it — §1.1
# data-regime / §88-trio collapse risk carries).
#
# This is a $0 STUB (deterministic loop simulation), NOT a trained-scale GPU
# fire. §88-F2 neoteny carry + §90/§91 #3 closed-form = honest direction-anchors,
# NOT a capability proof. g3: necessary-not-sufficient (B-EMERGE-7); design-level
# objective formalisation != trained-scale measurement != GOAL emergence.
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
# carried verbatim from §90 smoke (which carried from §88-F2 result.json).
S88F2_BASELINE = dict(maturity=0.9495988095306581, maj_frac=0.8724999999999999,
                      eff_D=1.886499047279358, ce=0.0038277350831776857)
S88F2_NEOTENY  = dict(maturity=0.7478041127531916, maj_frac=0.35,
                      eff_D=2.695751905441284, ce=0.04125382751226425)

# ── §91 trained-scale measured carry (cell2 decode-time-loop echo) ─────
# §91 result.json four_corner = (β) ECHO-DOMINATES-AT-TRAINED. cell2
# (neoteny ckpt + #3 decode-time loop): §9 0/20, attractor maj 0.35→0.68875,
# self-correct events 0. This is the §92 cell4 mirror target.
S91_CELL2_DECODE_ECHO = dict(maj_frac_final=0.68875, body_coherent_9=0,
                             maj_frac_start=0.35, self_correct_events=0)

# ── Law-71 ψ_state stub — byte-equal to conscious_decoder.py:728-751 ────
PSI_VACUUM = 0.5

def psi_update(prev_psi, stimulus_deviation, jitter):
    """Stub Law-71 ψ advance: stimulus deviation perturbs ψ off the Ψ=½
    vacuum; restoring pull toward Ψ=½ (anima g2 internal carve-out).
    BYTE-EQUAL to §90 smoke psi_update (connection-point B-S92-5)."""
    psi = prev_psi + 0.30 * stimulus_deviation + jitter
    psi = psi + 0.20 * (PSI_VACUUM - psi)
    return clip01(psi)

# ── §9 honest_coherent metric (cascade-rate-gated) ─────────────────────
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
    """§9 cascade-rate-gated coherence (deterministic, necessary-not-suff).
    4-clause Boolean conjunction — BYTE-EQUAL to §90 smoke (B-S92-4)."""
    if not s:
        return False
    L = len(s)
    cr = max(_max_char_run(s)/L, _4gram_rep(s))
    mr = _max_char_run(s)
    pr = sum(1 for c in s if 32 <= ord(c) < 127) / L
    return (cr < TAU_CASCADE) and (mr < MAX_RUN) and (L >= MIN_LEN) and (pr >= TAU_PRINT)

# ── #3 D@emit → S@t+1 transfer (§89/§90 closed-form carry) ─────────────
def s_encode(body):
    """Closed deterministic S-module byte encoder. Returns a stimulus
    deviation scalar in [0,1] = garble proxy of the heard body.
    K(output) <= K(body) + K(s_encode) — data-processing inequality
    holds by construction (pure function, no RNG/state/IO). §89 carry."""
    if not body:
        return 1.0
    cr = max(_max_char_run(body)/len(body), _4gram_rep(body))
    return clip01(cr)

# ── body production stub — garble-driven char-cascade collapse ─────────
_PROSE = ("anima senses the stimulus and forms a measured reply to it ")

def effective_garble(maj_frac, self_coherence_skill):
    """Garble the body exhibits.  Base garble has a FLOOR (0.40) that
    keeps a non-saturated neoteny body §9-INCOHERENT — this REPRODUCES
    the §88-F2 trained-scale γ False (neoteny delays saturation, maj
    0.35, but body §9 0/5) AND the §91 trained-scale cell2 §9 0/20.
    Delaying saturation alone does NOT make the body coherent.

    `self_coherence_skill` is the LEARNED capability the §92 L_ap
    TRAINING-TIME objective trains — ONLY a trained skill lowers garble
    below the §9 cascade gate (0.30).  This is the KEY §91→§92
    distinction: §90/§91's decode-time `loop_correction` accumulator is
    NOT a learned weight (it cannot enter `self_coherence_skill`); §92's
    L_ap gradient is the only thing that does.  A neoteny non-saturated
    body needs garble < ~0.27 to clear the §9 gate; the floor is 0.40,
    so skill must reach ~0.13+ — only the training-time L_ap path can."""
    # floor keeps neoteny-alone (skill=0) body §9-INCOHERENT (§88-F2 γ False).
    base = 0.40 + 0.55 * clip01((maj_frac - 0.30) / 0.60)  # maj 0.35 -> ~0.445
    return clip01(base - self_coherence_skill)

def produce_body(maj_frac, psi, rng, self_coherence_skill=0.0):
    """Generate a stub body string. High garble -> char-cascade collapse
    (the §16.6-C / §88-F2 / §91 failure mode)."""
    L = 56
    garble = effective_garble(maj_frac, self_coherence_skill)
    out = []
    for i in range(L):
        if rng.u() < garble:
            out.append('a')          # byte-cascade attractor dominant byte
        else:
            out.append(_PROSE[i % len(_PROSE)])
    dev = abs(psi - PSI_VACUUM)
    if dev > 0.18:
        idx = int(dev * 37) % max(1, L - 4)
        for k in range(3):
            out[idx + k] = 'x'
    return "".join(out)

# ── §92 #3 ACTION-PERCEPTION TRAINING-TIME OBJECTIVE ───────────────────
#
# L_ap = action-perception consistency loss. The model emits body e_t,
# S_encode(e_t) is fed back as the next stimulus x_{t+1}; the physics
# deviation that stimulus induces should be SMALL (a self-coherent
# emission, re-heard, leaves Ψ stable).
#
#   L_ap = ‖ ψ( forward( S_encode(e_t) ) ) − ψ_target ‖²
#
# closed-form: ψ_target = Ψ=½ vacuum (the Law-71 fixed point).  At the
# stub level ψ(forward(S_encode(e_t))) = psi_update(PSI_VACUUM,
# s_encode(e_t), 0) — a pure deterministic function of the emit garble.
#
# total loss:  L = L_CE + λ_ap · L_ap     (§11-B carry — CE-base overlay,
#                                          NOT no-CE; no-CE is degenerate)
#
# TRAINING-TIME vs DECODE-TIME (the §91→§92 distinction):
#   §90/§91 #3 = decode-time loop — inference accumulator `loop_corr`,
#                NO gradient, NO learned weight.  §91 measured: echo.
#   §92    #3 = training-time objective — L_ap contributes GRADIENT;
#                the model LEARNS `self_coherence_skill` because garbled
#                self-stimulus -> large L_ap -> gradient toward coherent
#                emission.  This is a learned capability, not a bolt-on.
LAMBDA_AP = 0.5  # §11-B overlay weight on the CE base

def ap_consistency_loss(emit_body):
    """L_ap closed-form: ‖ψ(forward(S_encode(e_t))) − ψ_target‖².
    ψ_target = Ψ=½ vacuum (Law-71 fixed point).  Pure deterministic
    function of the emitted body — no RNG, no learned param at eval time
    (the LEARNED part is `self_coherence_skill` which L_ap shapes)."""
    emit_dev = s_encode(emit_body)                       # x_{t+1} garble
    psi_heard = psi_update(PSI_VACUUM, emit_dev, 0.0)    # ψ after re-perceive
    return (psi_heard - PSI_VACUUM) ** 2                 # ‖·‖² to vacuum

def ce_loss_proxy(maj_frac):
    """Stub CE proxy: a saturated regime (high maj_frac) has driven CE
    to the §16.6-C floor (memorization).  Carried only so L = L_CE +
    λ_ap·L_ap is structurally CE-base (§11-B), NOT no-CE."""
    return S88F2_BASELINE["ce"] + (1.0 - maj_frac) * 0.04  # ~floor

# ── 5-cell stub grid ───────────────────────────────────────────────────
# cell0  §16 baseline           : NO L_ap, NO neoteny  (saturated)
# cell1  L_ap only              : L_ap ON, NO neoteny   (saturated ckpt + objective)
# cell2  neoteny + L_ap   (CORE): L_ap ON, neoteny ON   — training-time #3
# cell3  neoteny + L_ap + decode: L_ap ON, neoteny ON, + §90 decode-time loop
# cell4  §91 decode-time mirror : NO L_ap, neoteny ON, §90 decode-time loop ONLY
#        (reproduces §91 (β) ECHO-DOMINATES — sanity control)
CELLS = {
    "cell0_s16_baseline":          dict(neoteny=False, l_ap=False, decode_loop=False),
    "cell1_l_ap_only":             dict(neoteny=False, l_ap=True,  decode_loop=False),
    "cell2_neoteny_l_ap":          dict(neoteny=True,  l_ap=True,  decode_loop=False),
    "cell3_neoteny_l_ap_decode":   dict(neoteny=True,  l_ap=True,  decode_loop=True),
    "cell4_s91_decode_mirror":     dict(neoteny=True,  l_ap=False, decode_loop=True),
}

N_STEP = 20

# learning rate of the L_ap training signal (stub): each step the gradient
# of L_ap shapes self_coherence_skill toward reducing physics deviation.
LR_AP = 0.18

def run_cell(name, cfg, seed=1337):
    rng = LCG(seed)
    src = S88F2_NEOTENY if cfg["neoteny"] else S88F2_BASELINE
    maj = src["maj_frac"]
    maturity = src["maturity"]
    psi = PSI_VACUUM
    stim_dev = 0.0
    # self_coherence_skill — the LEARNED weight L_ap shapes (training-time).
    skill = 0.0
    # decode_corr — the §90/§91 decode-time loop accumulator (inference, no grad).
    decode_corr = 0.0
    traj = []
    coh_count = 0
    l_ap_trace = []
    self_correct_events = 0
    prev_emit_dev = None
    for step in range(N_STEP):
        jitter = 0.015 * (rng.u() - 0.5)
        psi = psi_update(psi, stim_dev, jitter)
        # body emitted under current attractor + ψ + LEARNED skill ONLY.
        # CRITICAL §91→§92 distinction: ONLY the training-time learned
        # `skill` lowers garble.  The decode-time `decode_corr` accumulator
        # is NOT a learned weight — per §91 (β) ECHO-DOMINATES it does not
        # produce self-correction; it only deepens the attractor (modelled
        # below as a maj_frac rise).  decode_corr therefore does NOT enter
        # produce_body.  This is what makes cell4 (§91 decode-mirror, no
        # L_ap) reproduce §91's §9 0/20, distinct from cell2's trained skill.
        body = produce_body(maj, psi, rng, self_coherence_skill=skill)
        coh = honest_coherent(body)
        if coh:
            coh_count += 1
        emit_dev = s_encode(body)

        # ── §92 #3 TRAINING-TIME OBJECTIVE: L_ap shapes `skill` via gradient ──
        l_ap = ap_consistency_loss(body)
        l_ce = ce_loss_proxy(maj)
        l_total = l_ce + LAMBDA_AP * l_ap
        l_ap_trace.append(round(l_ap, 8))
        if cfg["l_ap"]:
            # gradient step: ∂L_ap/∂skill < 0  (more skill -> coherent emit ->
            # smaller emit_dev -> smaller ψ deviation -> smaller L_ap).  The
            # model LEARNS self-coherence.  In a NON-saturated (neoteny)
            # regime the learning signal is usable; in a saturated regime the
            # attractor absorbs it (gradient drowned by memorization floor).
            if cfg["neoteny"]:
                # non-saturated: L_ap gradient genuinely lifts skill.
                skill = clip01(skill + LR_AP * l_ap * 4.0)
            else:
                # saturated: L_ap present but gradient mostly absorbed by
                # the §16.6-C memorization floor — weak skill lift.
                skill = clip01(skill + LR_AP * l_ap * 0.4)

        # ── §90/§91 #3 DECODE-TIME loop (inference accumulator, NO grad) ──────
        if cfg["decode_loop"]:
            stim_dev = emit_dev                       # x_{t+1}=S_encode(e_t)
            if cfg["neoteny"]:
                # §91 trained-scale MEASURED: decode-time loop on a neoteny
                # ckpt STILL echoes (verdict (β) ECHO-DOMINATES) — the model
                # never LEARNED self-perception, so re-hearing the garbled
                # emit deepens the byte-cascade attractor (echo-amplify, §62
                # carry).  §91 measured the neoteny+decode cell maj_frac
                # 0.35→0.68875.  decode_corr is a non-learned accumulator and
                # does NOT enter produce_body (see above) — it ONLY tracks the
                # inference loop; the attractor rise is the real echo effect.
                decode_corr = clip01(decode_corr + 0.01 * emit_dev)  # non-learned
                # echo rate tuned so cell4 (§91 mirror) reproduces §91's
                # measured maj 0.35→~0.689 over N_STEP turns.
                maj = clip01(maj + 0.105 * emit_dev)  # echo: basin DEEPENS
            else:
                maj = clip01(maj + 0.02 * emit_dev)
        else:
            stim_dev = 0.0

        if prev_emit_dev is not None and emit_dev < prev_emit_dev - 1e-6:
            self_correct_events += 1
        prev_emit_dev = emit_dev
        traj.append({"step": step, "psi": round(psi, 6),
                     "emit_dev": round(emit_dev, 6),
                     "l_ap": round(l_ap, 8), "l_total": round(l_total, 8),
                     "skill": round(skill, 6), "decode_corr": round(decode_corr, 6),
                     "coherent_9": bool(coh), "maj_frac": round(maj, 6)})
    return {
        "cell": name, "config": cfg,
        "body_coherent_rate_9": coh_count,
        "body_coherent_frac_9": round(coh_count / N_STEP, 6),
        "final_maturity": round(maturity, 6),
        "final_maj_frac": round(maj, 6),
        "final_skill": round(skill, 6),
        "final_l_ap": l_ap_trace[-1],
        "l_ap_trace_head": l_ap_trace[:5],
        "self_correct_events": self_correct_events,
        "n_step": N_STEP,
        "trajectory_head": traj[:5],
        "trajectory_tail": traj[-3:],
    }

def run_grid(seed=1337):
    return [run_cell(n, c, seed) for n, c in CELLS.items()]

# ── 4-corner verdict ───────────────────────────────────────────────────
def verdict(grid):
    by = {c["cell"]: c for c in grid}
    c0 = by["cell0_s16_baseline"]
    c1 = by["cell1_l_ap_only"]
    c2 = by["cell2_neoteny_l_ap"]
    c4 = by["cell4_s91_decode_mirror"]

    # (α) TRAINING-TIME-AP-CLOSES-γ-PREDICTED: cell2 (neoteny + training-time
    #     L_ap) §9 body-coherent rate strictly exceeds cell0 baseline AND
    #     strictly exceeds cell4 (§91 decode-time mirror) — training-time
    #     objective outperforms the §91 decode-time overlay.
    alpha = (c2["body_coherent_rate_9"] > c0["body_coherent_rate_9"] and
             c2["body_coherent_rate_9"] > c4["body_coherent_rate_9"])

    # (β) AP-OBJECTIVE-DEGENERATE: L_ap drives a trivial solution — the
    #     attractor maj_frac is NOT measurably reduced relative to its
    #     §88-F2 carry start (L_ap shaped nothing OR found a degenerate
    #     minimum).  At the stub level: cell2 final maj_frac >= its neoteny
    #     start AND cell2 final skill ~ 0 (objective shaped no skill).
    beta = (c2["final_maj_frac"] >= S88F2_NEOTENY["maj_frac"] - 1e-6 and
            c2["final_skill"] < 1e-3)

    # (γ) ECHO-STILL-AMPLIFIES: even with the training-time L_ap, the
    #     attractor maj_frac rises (echo wins) — cell2 final maj_frac
    #     strictly exceeds its §88-F2 neoteny carry start.
    gamma = c2["final_maj_frac"] > S88F2_NEOTENY["maj_frac"] + 1e-6

    # (δ) NEOTENY-AP-SYNERGY: cell2 (neoteny + L_ap) coherence delta over
    #     §16 baseline exceeds the sum of L_ap-only (cell1) + neoteny-only
    #     (cell0 has no neoteny; the neoteny-only proxy is cell4 minus its
    #     decode-loop, which is unavailable — use cell0 vs cell1 deltas).
    base = c0["body_coherent_rate_9"]
    d_ap = c1["body_coherent_rate_9"] - base       # L_ap-only delta
    # neoteny-only proxy: §88-F2 carry already measured neoteny-alone §9=0
    # (γ False), so d_neoteny_alone = 0 by the §88-F2 trained-scale result.
    d_neoteny_alone = 0
    d_both = c2["body_coherent_rate_9"] - base
    delta = d_both > (d_ap + d_neoteny_alone)

    return {
        "alpha_TRAINING_TIME_AP_CLOSES_GAMMA": bool(alpha),
        "beta_AP_OBJECTIVE_DEGENERATE": bool(beta),
        "gamma_ECHO_STILL_AMPLIFIES": bool(gamma),
        "delta_NEOTENY_AP_SYNERGY": bool(delta),
        "coherence_rates": {c["cell"]: c["body_coherent_rate_9"] for c in grid},
        "maj_frac_final": {c["cell"]: c["final_maj_frac"] for c in grid},
        "skill_final": {c["cell"]: c["final_skill"] for c in grid},
        "l_ap_final": {c["cell"]: c["final_l_ap"] for c in grid},
        "synergy_decomp": {"base_s16": base, "d_ap_only": d_ap,
                           "d_neoteny_alone_s88f2": d_neoteny_alone,
                           "d_both": d_both},
        "training_vs_decode": {
            "cell2_neoteny_l_ap_TRAINING_coherence": c2["body_coherent_rate_9"],
            "cell4_s91_decode_mirror_coherence": c4["body_coherent_rate_9"],
            "training_time_advantage": (c2["body_coherent_rate_9"]
                                        - c4["body_coherent_rate_9"]),
        },
    }

if __name__ == "__main__":
    grid = run_grid(seed=1337)
    v = verdict(grid)
    if v["alpha_TRAINING_TIME_AP_CLOSES_GAMMA"]:
        overall = "TRAINING-TIME-AP-DIRECTIONAL-POSITIVE"
    elif v["gamma_ECHO_STILL_AMPLIFIES"]:
        overall = "ECHO-STILL-AMPLIFIES-NEGATIVE"
    elif v["beta_AP_OBJECTIVE_DEGENERATE"]:
        overall = "AP-OBJECTIVE-DEGENERATE-NEGATIVE"
    else:
        overall = "AP-NO-EFFECT-MIXED"
    out = {
        "section": "§92 #3 ACTION-PERCEPTION AS TRAINING-TIME OBJECTIVE",
        "kind": "$0 Mac CPU design + stub smoke (NO GPU, NO fire)",
        "target": ("§91 (β) ECHO-DOMINATES-AT-TRAINED — #3 wired as a "
                   "DECODE-TIME overlay echo-amplified (cell2 §9 0/20, "
                   "attractor 0.35→0.689); §92 formalises #3 as a "
                   "TRAINING-LOOP objective so anima LEARNS self-coherence"),
        "seed": 1337, "n_step": N_STEP,
        "lambda_ap": LAMBDA_AP, "lr_ap": LR_AP,
        "s88f2_carry": {"baseline": S88F2_BASELINE, "neoteny": S88F2_NEOTENY},
        "s91_decode_echo_carry": S91_CELL2_DECODE_ECHO,
        "l_ap_closed_form": {
            "formula": "L_ap = ||psi(forward(S_encode(e_t))) - psi_target||^2",
            "psi_target": "Psi=1/2 vacuum (Law-71 fixed point)",
            "total_loss": "L = L_CE + lambda_ap * L_ap  (§11-B CE-base overlay)",
            "transfer": "x_{t+1} = S_encode(e_t)  (§89/§90 #3 carry)",
            "invariant": "K(x_{t+1}) <= K(e_t) + K(S_encode)  (data-processing ineq.)",
        },
        "training_vs_decode_distinction": (
            "§90/§91 #3 = DECODE-TIME loop (inference accumulator, NO "
            "gradient, NO learned weight) -> §91 measured echo. §92 #3 = "
            "TRAINING-TIME objective (L_ap contributes GRADIENT; model "
            "LEARNS self_coherence_skill). self-correction = learned "
            "capability, NOT a decode-time bolt-on."),
        "grid": [{k: c[k] for k in ("cell", "body_coherent_rate_9",
                                    "body_coherent_frac_9", "final_maturity",
                                    "final_maj_frac", "final_skill",
                                    "final_l_ap", "self_correct_events")}
                 for c in grid],
        "grid_full": grid,
        "four_corner_verdict": v,
        "overall": overall,
        "note": ("B-S92-NOTE: whether the training-time L_ap objective "
                 "ACTUALLY closes γ (coherent emission emerges) at trained "
                 "scale = GPU fire OUTCOME, NOT counted 🔵 (B-D-NOTE / "
                 "B-S88F2-NOTE / B-S90-NOTE / B-S91-NOTE / B-EMERGE-NOTE "
                 "family). $0 stub L_ap-shapes-skill is a DESIGN hypothesis; "
                 "the §1.1 data-regime / §88-trio collapse pattern means a "
                 "training-time objective CAN still degenerate at trained "
                 "scale (β corner risk carries). g3 necessary-not-sufficient "
                 "(B-EMERGE-7); design-level formalisation != trained-scale "
                 "measurement != GOAL emergence."),
    }
    (HERE / "result.json").write_text(json.dumps(out, indent=2))
    payload = hashlib.sha256(json.dumps(grid, sort_keys=True).encode()).hexdigest()
    print(json.dumps({"grid": out["grid"], "four_corner": v,
                       "overall": overall, "grid_sha256": payload}, indent=2))
