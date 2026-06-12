"""
H_1190 — is the LEARNED-SURPRISE gate GENERAL, or does it only RESCUE the modality
(text) where raw byte-change is uninformative?

H_1187 (MITOSIS-ENGINE, 🟢 SACCADIC-READING) showed that on REAL TEXT a
LEARNED-SURPRISE gate (split fires when −log2 P(next|ctx) exceeds its running mean+σ,
the saccade) RECOVERS a temporal stage-decode advantage over a uniform metronome scan
that the raw |dX/dt| DERIVATIVE gate (H_1186) could NOT find. Text's byte-feature
stages are NOT smoothly approached, so raw change is uninformative there — and a
learned predictability signal was load-bearing to read it.

H_1190 asks the natural generality question: does that learned-surprise gate ALSO beat
the raw DERIVATIVE on the modalities that are ALREADY TEMPORAL by construction —
  • NUMERIC  = per-regime AR(1) (smooth within-regime relaxation toward an attractor),
  • AUDIO    = drifting recurring regimes (smooth within-regime drift),
or is it REDUNDANT there? On these streams the raw derivative ALREADY reads the smooth
within-regime flow / regime cuts (H_1188 ranked both NUMERIC and AUDIO as TEMPORAL on
the raw-derivative axis), so a learned one-step-prediction surprise should add NOTHING
— the saccade and the derivative-rising-edge fire at the SAME regime transitions.

This tests whether "learned surprise" is a UNIVERSAL upgrade over a raw derivative, or
whether it only RESCUES the one modality (text) where raw change is uninformative.

CONTINUOUS-STREAM SURPRISE (the analogue of H_1187's byte-surprise): for a continuous
numeric/audio stream the "surprise" at tick t is the ONE-STEP PREDICTION ERROR of a
tiny per-stream LINEAR predictor — predict X[t] from X[t-1] via a least-squares fit on
the WARMUP span (a per-dim AR(1)-style map x̂_t = A·x_{t-1} + b), and
  surprise[t] = ||X[t] − x̂_t||.
High surprise = a tick the smooth per-step predictor did NOT see coming = a regime
transition / abrupt change = a fixation/saccade point. This is the direct continuous
analogue of H_1187's −log2 P(byte|ctx) (a learned predictor's miss), so the SAME
saccade machinery (grow_arm_surprise) applies, mirroring grow_arm's DERIVATIVE body
with the trigger swapped to surprise>running mean+σ.

FROZEN FALSIFIER (pre-registered BEFORE measuring; deterministic, H.SEEDS=10; metric =
STAGE-DECODE accuracy, p7 — NOT the predictor's loss, NOT next-step error):
  For EACH modality in {numeric, audio}:
    K* = argmax over the cap ladder {4,6,8,12,16,24,32,48,64} of
         d_derivative_vs_metro = cohen_d_paired(decode_DERIVATIVE, decode_METRONOME)
         — the stream's OWN coverage cap (same own-cap protocol as H_1186/H_1187,
         anchored on the DERIVATIVE arm because that is the incumbent gate H_1190 asks
         whether surprise improves upon).
    At that K*, report:
      d_surprise_vs_metro   = cohen_d_paired(decode_SURPRISE,    decode_METRONOME)
      d_derivative_vs_metro = cohen_d_paired(decode_DERIVATIVE,  decode_METRONOME)
      Δ = d_surprise_vs_metro − d_derivative_vs_metro
    CLASSIFY:
      REDUNDANT     iff |Δ| < 0.5   (surprise ≈ derivative — adds nothing)
      SURPRISE-ADDS iff Δ ≥ 0.5     (surprise meaningfully beats the raw derivative)
  F1: report each modality's REDUNDANT vs SURPRISE-ADDS classification (verbatim Δ).

  SUPPORTED framing = the PRE-REGISTERED prediction
    "surprise is REDUNDANT on the already-temporal numeric/audio streams (the raw
     derivative already reads their smooth flow), unlike text where surprise was
     load-bearing (H_1187)"
  is BORNE OUT iff BOTH modalities classify REDUNDANT.
  ELSE CLOSED-NEGATIVE (a_paper_negative_ok) — surprise ALSO helps on a smooth
  already-temporal modality ⇒ learned surprise is a (partially) UNIVERSAL upgrade, not
  just a text rescue, which is itself a finding.

cohen_d_paired is PAIRED on per-seed deltas; POSITIVE => 1st arg arm is BETTER (higher
stage-decode). d(SURPRISE,METRONOME) and d(DERIVATIVE,METRONOME) are both vs the same
metronome baseline so Δ directly compares the two gates' lift over a uniform scan.

SUBSTRATE REUSE (UNIVERSE/h1163_tick_decode_metric.py imported as H): grow_arm
(DERIVATIVE + METRONOME arms), stage_decode_accuracy, cohen_d_paired, assign,
make_audio_stream, SEEDS, MAX_CELLS (patched per cap), WARMUP, T, DIM, LR, WIN,
DERIV_REFRAC, N_REGIMES_AUDIO — all VERBATIM. make_numeric_stream is the H_1188 AR(1)
design reproduced locally (same coefficients/dwell). grow_arm_surprise mirrors
H_1163.grow_arm's DERIVATIVE body, swapping ONLY the split trigger to
surprise>running mean+σ — the SAME swap H_1187 made for text, now with a continuous
per-stream linear-predictor surprise.

HONESTY (a_scale_honest_scope, a_toy_scale_recheck): TOY ONLY — $0 CPU numpy, 10
deterministic seeds, SYNTHETIC numeric/audio streams, a TINY least-squares linear
predictor as the surprise model. Real continuous-modality data + a learned deep
predictor + live CORE engine_mitosis_tick + production scale UNVERIFIED. The
predictor's own one-step error is NEVER the verdict (p7) — stage-decode is.
a_completeness_over_cheap: any construction defect (predictor degenerate / surprise
flat / cap floor) is FIXED BEFORE scoring and stated — never tune-to-green after.
Lane-M gradient-free growth lane (separate from Lane A AKIDA / Lane G forge / Lane P
torch, a_lane_akida_gpu_split).
"""
import json, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import h1163_tick_decode_metric as H  # substrate: grow_arm / stage_decode / cohen_d / make_audio_stream / config

np.seterr(all="ignore")

# ---- frozen config -----------------------------------------------------------------
CAP_LADDER = (4, 6, 8, 12, 16, 24, 32, 48, 64)   # stream's-own coverage-cap sweep (H_1186/H_1187 protocol)
SURPRISE_SIGMA = 1.0          # split fires when surprise > running_mean + SIGMA*running_std (mirror H_1187)
SURPRISE_REFRAC = H.DERIV_REFRAC      # SAME refractory window as the derivative arm (verbatim)
N_REGIMES_NUMERIC = 6         # match AUDIO K so the two modalities are comparable (H_1188 value)
REDUNDANT_BAR = 0.5           # |Δ| < 0.5 => REDUNDANT ; Δ >= 0.5 => SURPRISE-ADDS


# ====================================================================================
# NUMERIC STREAM — the H_1188 per-regime AR(1) design reproduced VERBATIM (same seed
# offset, attractors, coefficients, dwell, no-teleport relaxation). stage = regime id.
# ====================================================================================
def make_numeric_stream(seed):
    """Toy NUMERIC time-series: K regimes, each a per-regime AR(1) process over the 8 dims
    with its OWN coefficient and mean (attractor). Regimes recur with dwell. stage = regime id.

        x_{t+1} = mu_r + a_r * (x_t - mu_r) + eps,   a_r in [0.55, 0.9]  (|a|<1 stable)

    On a regime CUT the state is carried over (NO teleport) so the process SMOOTHLY relaxes
    from the old attractor toward the new mu_r over the dwell -> a smooth, time-ordered
    approach the DERIVATIVE tick can fire on (this is exactly why H_1188 ranked numeric
    TEMPORAL on the raw-derivative axis). Same (X[need,DIM], stages) convention as
    H.make_audio_stream. REPRODUCED VERBATIM from H_1188 (seed+4242, mu*6.0, coef[0.55,0.9])."""
    rng = np.random.default_rng(seed + 4242)
    K = N_REGIMES_NUMERIC
    mus = rng.standard_normal((K, H.DIM)) * 6.0
    coefs = rng.uniform(0.55, 0.9, size=K)
    need = H.WARMUP + H.T + 1
    X = np.empty((need, H.DIM)); stages = np.empty(need, dtype=int)
    x = mus[0].copy(); r = 0; dwell = 0
    for t in range(need):
        if dwell <= 0:
            r = int(rng.integers(K)); dwell = int(rng.integers(40, 90))   # recur, no teleport
        x = mus[r] + coefs[r] * (x - mus[r]) + rng.standard_normal(H.DIM) * 0.4
        dwell -= 1
        X[t] = x
        stages[t] = r
    return X, stages


# ====================================================================================
# CONTINUOUS-STREAM SURPRISE — the analogue of H_1187's learned −log2 P(byte|ctx) for a
# continuous numeric/audio stream: the ONE-STEP PREDICTION ERROR of a tiny per-stream
# linear predictor x̂_t = A·x_{t-1} + b, least-squares-fit on the WARMUP span (the
# stream's own baseline dynamics; never sees the scored region's labels). surprise[t] =
# ||X[t] − x̂_t||. The predictor's own error is NEVER the verdict (p7).
# ====================================================================================
def surprise_track(X):
    """Fit a per-stream linear one-step predictor x̂_t = A·x_{t-1}+b on the WARMUP span by
    least squares, then surprise[t] = ||X[t] − x̂_t|| over the whole stream. High surprise =
    a tick the smooth predictor missed = a regime transition (a saccade/fixation point).
    This is the continuous analogue of H_1187's learned-predictor byte-surprise."""
    # design matrix on WARMUP: predict X[1:WARMUP] from X[0:WARMUP-1]
    prev = X[:H.WARMUP - 1]                     # (W-1, DIM)
    nxt = X[1:H.WARMUP]                         # (W-1, DIM)
    # augment with bias column -> [x_{t-1}, 1]; solve least squares for W = [A^T; b^T]
    Phi = np.concatenate([prev, np.ones((prev.shape[0], 1))], axis=1)   # (W-1, DIM+1)
    Wmat, *_ = np.linalg.lstsq(Phi, nxt, rcond=None)                    # (DIM+1, DIM)
    need = X.shape[0]
    surp = np.empty(need, dtype=float)
    surp[0] = 0.0                               # no predecessor for the first tick
    Phi_all = np.concatenate([X[:-1], np.ones((need - 1, 1))], axis=1)  # predict X[1:] from X[:-1]
    pred = Phi_all @ Wmat                       # (need-1, DIM)
    surp[1:] = np.linalg.norm(X[1:] - pred, axis=1)
    return surp


def surprise_degenerate(surp):
    """Construction-defect guard (a_completeness_over_cheap): the surprise signal must have
    real spread (a flat signal can never fire a meaningful saccade). Returns (is_degen, reason)."""
    spread = float(np.std(surp[H.WARMUP:H.WARMUP + H.T]))
    if spread <= 1e-6:
        return True, f"flat surprise (std={spread:.2e})"
    return False, ""


# ====================================================================================
# SURPRISE-GATED GROW ARM — H_1163.grow_arm's DERIVATIVE body copied VERBATIM, swapping
# ONLY the split TRIGGER to surprise[t] > running_mean+σ (the saccade), exactly the
# H_1187 swap. Cell-state online update, birth-stage record, owner-cell (highest-tension)
# split, MAX_CELLS cap, refractory — IDENTICAL to H.grow_arm.
# ====================================================================================
def grow_arm_surprise(X, stages, surprise, seed):
    rng = np.random.default_rng(seed + 5000)               # VERBATIM H.grow_arm seed offset
    cells = X[:2].copy().astype(float)
    nexts = np.zeros((2, H.DIM))
    cell_stage = [-1, -1]
    for t in range(H.WARMUP - 1):                          # VERBATIM warmup
        j, _ = H.assign(cells, X[t])
        cells[j] += H.LR * (X[t] - cells[j])
        nexts[j] += H.LR * ((X[t + 1] - X[t]) - nexts[j])
    ten = np.zeros(len(cells))
    last_fire = -10 ** 9

    # surprise threshold = WARMUP-span baseline mean + σ (analogue of dthr quantile, mirror H_1187)
    warm_surp = surprise[:H.WARMUP]
    s_thr = float(np.mean(warm_surp)) + SURPRISE_SIGMA * (float(np.std(warm_surp)) + 1e-9)

    def do_split(src, birth_stage):                        # VERBATIM H.grow_arm.do_split
        nonlocal cells, nexts, ten
        daughter = cells[src] + rng.standard_normal(H.DIM) * 0.3
        cells = np.vstack([cells, daughter[None]])
        nexts = np.vstack([nexts, nexts[src][None]])
        ten = np.concatenate([ten, [0.0]]); ten[src] = 0.0
        cell_stage.append(int(birth_stage))

    for i, t in enumerate(range(H.WARMUP, H.WARMUP + H.T)):
        x = X[t]
        j, d = H.assign(cells, x)
        true_next = X[t + 1]
        cells[j] += H.LR * (x - cells[j])                  # VERBATIM online update
        nexts[j] += H.LR * ((true_next - x) - nexts[j])
        ten[j] += (d - ten[j]) / H.WIN

        surprising = surprise[t] > s_thr                   # SACCADE trigger (mirror H_1187)
        fire = surprising and (i - last_fire) >= SURPRISE_REFRAC

        if fire and len(cells) < H.MAX_CELLS:              # VERBATIM cap + owner-cell split
            src = int(np.argmax(ten))
            do_split(src, stages[t])
            last_fire = i

    return cells, np.asarray(cell_stage, dtype=int)


# ====================================================================================
# EVAL — at a given cap, per-seed decode for SURPRISE / DERIVATIVE / METRONOME.
# ====================================================================================
def eval_at_cap(builder, n_stages, cap):
    saved = H.MAX_CELLS
    H.MAX_CELLS = cap
    dec_su, dec_de, dec_me = [], [], []
    su_cells = []
    for s in H.SEEDS:
        X, stages = builder(s)
        surp = surprise_track(X)
        st_su, cs_su = grow_arm_surprise(X, stages, surp, s)
        st_de, cs_de = H.grow_arm(X, stages, "DERIVATIVE", s)
        st_me, cs_me = H.grow_arm(X, stages, "METRONOME", s)
        dec_su.append(H.stage_decode_accuracy(st_su, cs_su, X, stages, n_stages))
        dec_de.append(H.stage_decode_accuracy(st_de, cs_de, X, stages, n_stages))
        dec_me.append(H.stage_decode_accuracy(st_me, cs_me, X, stages, n_stages))
        su_cells.append(int(len([c for c in cs_su if c >= 0])))
    H.MAX_CELLS = saved
    return {
        "cap": cap,
        "dec_surp": dec_su, "dec_deriv": dec_de, "dec_metro": dec_me,
        "mean_surp": float(np.mean(dec_su)), "mean_deriv": float(np.mean(dec_de)),
        "mean_metro": float(np.mean(dec_me)), "mean_surp_cells": float(np.mean(su_cells)),
        "d_surprise_vs_metro": H.cohen_d_paired(dec_su, dec_me),
        "d_derivative_vs_metro": H.cohen_d_paired(dec_de, dec_me),
    }


def eval_modality(name, builder, n_stages):
    print(f"--- MODALITY: {name.upper()} ({n_stages} stages; chance={1.0/n_stages:.3f}) ---", flush=True)
    # construction guard: surprise spread on seed0
    X0, _ = builder(H.SEEDS[0])
    sp0 = surprise_track(X0)
    degen, reason = surprise_degenerate(sp0)
    print(f"  surprise spread (std over seed0 scored region) = "
          f"{float(np.std(sp0[H.WARMUP:H.WARMUP+H.T])):.4f}  degenerate={degen} ({reason or 'ok'})", flush=True)

    ladder = {}
    for cap in CAP_LADDER:
        r = eval_at_cap(builder, n_stages, cap)
        ladder[cap] = r
        print(f"  cap={cap:3d}  surp={r['mean_surp']:.4f}  deriv={r['mean_deriv']:.4f}  "
              f"metro={r['mean_metro']:.4f}  d(surp,metro)={r['d_surprise_vs_metro']:+.2f}  "
              f"d(deriv,metro)={r['d_derivative_vs_metro']:+.2f}", flush=True)

    # K* = argmax d_derivative_vs_metro (anchor on the incumbent DERIVATIVE gate)
    kstar = max(CAP_LADDER, key=lambda c: ladder[c]["d_derivative_vs_metro"])
    r = ladder[kstar]
    d_surp = r["d_surprise_vs_metro"]
    d_deriv = r["d_derivative_vs_metro"]
    delta = d_surp - d_deriv
    redundant = abs(delta) < REDUNDANT_BAR
    adds = delta >= REDUNDANT_BAR
    cls = "REDUNDANT" if redundant else ("SURPRISE-ADDS" if adds else "SURPRISE-WORSE")
    print(f"  K* = {kstar} (argmax d(deriv,metro)):  d_surprise_vs_metro={d_surp:+.3f}  "
          f"d_derivative_vs_metro={d_deriv:+.3f}  Δ={delta:+.3f}  => {cls}\n", flush=True)
    return {
        "modality": name, "n_stages": n_stages, "chance": 1.0 / n_stages,
        "Kstar": kstar,
        "d_surprise_vs_metro": d_surp,
        "d_derivative_vs_metro": d_deriv,
        "delta": delta,
        "classification": cls,
        "redundant": bool(redundant),
        "surprise_adds": bool(adds),
        "surprise_degenerate": bool(degen), "degenerate_reason": reason,
        "mean_decode_at_Kstar": {"surprise": r["mean_surp"], "derivative": r["mean_deriv"],
                                 "metronome": r["mean_metro"]},
        "cap_ladder": {str(c): {"d_surprise_vs_metro": ladder[c]["d_surprise_vs_metro"],
                                "d_derivative_vs_metro": ladder[c]["d_derivative_vs_metro"],
                                "mean_surp": ladder[c]["mean_surp"],
                                "mean_deriv": ladder[c]["mean_deriv"],
                                "mean_metro": ladder[c]["mean_metro"]} for c in CAP_LADDER},
    }


def main():
    print("=== H_1190 — is the LEARNED-SURPRISE gate GENERAL, or only a TEXT rescue? "
          "Does surprise beat the raw DERIVATIVE on already-temporal numeric/audio? ===", flush=True)
    print(f"  continuous surprise = one-step linear-predictor error ||X[t]-x̂_t|| (analogue of "
          f"H_1187 byte-surprise); surprise-gated split (mean+{SURPRISE_SIGMA}σ saccade) vs raw "
          f"DERIVATIVE vs METRONOME", flush=True)
    print(f"  {len(H.SEEDS)} seeds; metric = STAGE-DECODE (p7, NOT predictor loss); per-modality "
          f"K* = argmax d(deriv,metro) over cap ladder {CAP_LADDER}", flush=True)
    print(f"  PRE-REG prediction: surprise is REDUNDANT (|Δ|<{REDUNDANT_BAR}) on already-temporal "
          f"numeric/audio (raw derivative already reads smooth flow), unlike text (H_1187)\n", flush=True)

    mods = []
    mods.append(eval_modality("numeric", make_numeric_stream, N_REGIMES_NUMERIC))
    mods.append(eval_modality("audio", H.make_audio_stream, H.N_REGIMES_AUDIO))

    both_redundant = all(m["redundant"] for m in mods)
    any_adds = any(m["surprise_adds"] for m in mods)
    supported = bool(both_redundant)

    if supported:
        ruling = ("SUPPORTED (SURPRISE-REDUNDANT-ON-TEMPORAL): on BOTH already-temporal modalities "
                  "(numeric AR(1), audio drifting-regimes) the learned one-step-surprise gate is "
                  "REDUNDANT with the raw |dX/dt| DERIVATIVE gate (|Δ|<%.1f each) — the raw derivative "
                  "ALREADY reads the smooth within-regime flow / regime cuts, so a learned predictor "
                  "adds nothing. The PRE-REGISTERED prediction is BORNE OUT: learned surprise is NOT a "
                  "universal upgrade — it specifically RESCUES the one modality (text, H_1187) where "
                  "raw byte-change is uninformative, and is redundant where raw change already encodes "
                  "the temporal structure. %s"
                  % (REDUNDANT_BAR,
                     "; ".join(f"{m['modality']}: Δ={m['delta']:+.2f} ({m['classification']})" for m in mods)))
    else:
        adds_mods = [m for m in mods if m["surprise_adds"]]
        ruling = ("CLOSED-NEGATIVE (a_paper_negative_ok): the PRE-REGISTERED 'surprise is redundant on "
                  "already-temporal streams' prediction FAILS — learned surprise ALSO BEATS the raw "
                  "derivative (Δ>=%.1f) on %s, so it is a (partially) UNIVERSAL upgrade, not only a text "
                  "rescue. %s. FINDING: a learned one-step predictor extracts decode-relevant "
                  "transition structure the raw |dX/dt| derivative misses even on a smooth temporal "
                  "stream."
                  % (REDUNDANT_BAR, ", ".join(m["modality"] for m in adds_mods),
                     "; ".join(f"{m['modality']}: Δ={m['delta']:+.2f} ({m['classification']})" for m in mods)))

    verdict = {
        "H": "H_1190",
        "title": "is the learned-surprise gate GENERAL (beats the raw derivative on already-temporal "
                 "numeric/audio too) or REDUNDANT there (only rescues text where raw change is "
                 "uninformative)?",
        "frozen_falsifier": {
            "Kstar": "per modality, argmax over cap ladder {4,6,8,12,16,24,32,48,64} of d_derivative_vs_metro",
            "delta": "Δ = d_surprise_vs_metro − d_derivative_vs_metro at K*",
            "REDUNDANT": "|Δ| < 0.5 (surprise ≈ derivative)",
            "SURPRISE_ADDS": "Δ >= 0.5 (surprise meaningfully beats raw derivative)",
            "SUPPORTED": "BOTH numeric AND audio classify REDUNDANT (pre-reg prediction borne out)",
            "ELSE": "CLOSED-NEGATIVE — surprise also helps a smooth modality = (partial) universal upgrade",
            "metric": "STAGE-DECODE accuracy (p7, NOT the predictor's one-step error)",
        },
        "modalities": {m["modality"]: {
            "Kstar": m["Kstar"],
            "d_surprise_vs_metro": m["d_surprise_vs_metro"],
            "d_derivative_vs_metro": m["d_derivative_vs_metro"],
            "delta": m["delta"],
            "classification": m["classification"],
            "redundant": m["redundant"],
            "surprise_adds": m["surprise_adds"],
            "mean_decode_at_Kstar": m["mean_decode_at_Kstar"],
            "surprise_degenerate": m["surprise_degenerate"],
        } for m in mods},
        "cap_ladders": {m["modality"]: m["cap_ladder"] for m in mods},
        "both_redundant": both_redundant,
        "any_surprise_adds": any_adds,
        "supported": supported,
        "ruling": ruling,
        "generality_answer": (
            "REDUNDANT ON BOTH — learned surprise is a TEXT-SPECIFIC rescue, NOT a universal upgrade: "
            "on already-temporal numeric AR(1) + audio drifting-regimes the raw |dX/dt| derivative "
            "already reads the smooth flow, so a learned one-step predictor adds nothing (|Δ|<0.5 "
            "each). Surprise was load-bearing in H_1187 precisely because text's byte-feature stages "
            "are NOT smoothly approached." if supported else
            "NOT REDUNDANT — learned surprise ALSO beats the raw derivative on a smooth already-temporal "
            "modality, so it is a (partially) universal upgrade rather than only a text rescue."),
        "scope": "TOY ONLY ($0 CPU numpy, %d seeds, synthetic numeric/audio streams, a TINY "
                 "least-squares linear one-step predictor as the surprise model). Reuses the H_1163 "
                 "grow_arm DERIVATIVE+METRONOME arms + stage_decode_accuracy + cohen_d_paired + "
                 "make_audio_stream VERBATIM; make_numeric_stream = H_1188 AR(1) reproduced verbatim; "
                 "grow_arm_surprise mirrors grow_arm's DERIVATIVE body (split trigger swapped to "
                 "surprise>mean+%gσ, the H_1187 swap). Real continuous-modality data + a learned deep "
                 "predictor + live CORE engine_mitosis_tick + production scale UNVERIFIED "
                 "(a_scale_honest_scope, a_toy_scale_recheck). Predictor's own error NOT the verdict "
                 "(p7). Lane-M gradient-free growth lane (a_lane_akida_gpu_split)."
                 % (len(H.SEEDS), SURPRISE_SIGMA),
    }
    print("=== VERDICT ===", flush=True)
    print(f"  {ruling}\n", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1190_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done]", flush=True)


if __name__ == "__main__":
    main()
