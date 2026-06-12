"""
H_1160 — does the from-scratch inference+learning MITOSIS engine need a metronome
TICK to gate its cell-division growth, or is the tick EVENT / DERIVATIVE-driven?
(the user's "틱이 있어야 되나?")

The mitosis engine learns online from scratch (p8, NO train/infer split — it keeps
dividing during inference). Feeding a TIME-ORDERED stream (real text bytes / synthetic
audio frames) in, what should GATE the cell-division growth tick (engine_mitosis_tick,
CORE/engine_cli.hexa)? We reuse the H_1159 / H_1159b prototype-split mitosis substrate as
the ENGINE and swap ONLY the split-trigger gate among four candidates:

  METRONOME  (M2-like): split every N steps on a fixed exogenous clock (a wall-clock tick).
  POSITIONAL (M1-like): split keyed to absolute stream index (a fixed schedule of indices).
  DERIVATIVE (M3-like): split fires on a rising-edge of |d(input)/dt| — the data's own
                        CHANGE events drive the tick (the prior-evidence winner; the
                        time-dependence lives on the SPLIT TRIGGER, not the recorded state).
  NO-GATE   (control) : split BLINDLY at a fixed total count, IGNORING the input entirely
                        (same #splits budget as the others — isolates "tick-gating" from
                        "mere capacity-add").

PRIOR EVIDENCE this ELEVATES (toy-EEG -> general text/audio tick-gating):
  .discoveries/clm-time-encoding.tape  : M3 DERIVATIVE was the ONLY arm to beat the
     phase-shuffled control on toy EEG; M2 phase-CLOCK half-failed; M1/M4 failed. BUT note
     that result used a RECONSTRUCTION-FIDELITY + STAGE-DECODE metric, NOT next-step error.
  .discoveries/kosmos-time-axis.tape   : order matters (F-ORDER beats F-SHUFFLE).
  .discoveries/tensionlink-dim-time.tape: dF/dt beats shuffle.
  H_1160 asks the HARDER general question on the falsifier-mandated SUBSTRATE-NATIVE
  ONLINE NEXT-STEP PREDICTION ERROR metric (NOT decode/recon) — a different, stricter axis.

STREAMS:
  TEXT  (must-have, DECISIVE): real byte-stream from CORE/testdata/clm_mid_5lang_c4.txt fed
     in time-order (NO shuffle, NO epochs; seed picks only a deterministic start offset =
     a different real slice). Each step's FEATURE = a local byte-statistics vector over a
     sliding byte window (byte mean/var, non-ascii ratio, letter/digit/space/punct ratios).
     The DERIVATIVE = |d(feature)/dt| = local byte-change / novelty (script / language /
     word boundaries).
  AUDIO (confirmation): a SYNTHETIC RECURRING-REGIME stream — K regimes, each with its OWN
     constant drift vector + center, the schedule REVISITS regimes (a single global
     next-delta cannot serve all). FEATURE = per-frame state; derivative = |d(frame)/dt|
     (spikes at a regime transition). This is the structure where a tick-gate's PLACEMENT
     of scarce capacity can matter most; verdict is NOT blocked on it (TEXT is decisive).
  Capacity is kept SCARCE (small MAX_CELLS) on purpose: when capacity is abundant every gate
  eventually covers every regime and ties — the WHEN of the tick only matters when splits
  are scarce, so this is the regime where the tick-gate is even TESTABLE.

ONLINE NEXT-STEP PREDICTION (substrate-native, p7 — NOT perplexity / NOT CE):
  cells are prototype vectors (the H_1159 mitosis substrate). At each step the engine predicts
  the NEXT feature as current + the running per-cell "next-delta" of the cell that owns the
  CURRENT feature (a 1-step linear predictor anchored on the assigned prototype). The error =
  ||pred_next - true_next||. Online-mean updates the prototype and its next-delta (NO backprop,
  NO gradients, p8). The split-trigger gate decides WHEN a high-tension cell divides. Lower
  next-step error = the gate placed capacity where the stream's structure actually needed it.

  HONEST CONSTRUCTION NOTE (defect-diagnosis BEFORE scoring, a_completeness_over_cheap):
  a pre-scoring diagnostic showed that on a SMOOTH/near-stationary feature stream the
  next-step error is NOISE-FLOORED and INVISIBLE to cell-count (err ~flat from 2 to 32
  cells) — so the split-gate would be untestable and every arm would trivially tie. We did
  NOT paper over that: we (a) keep capacity SCARCE and (b) add the RECURRING-REGIME audio
  stream where a single global next-delta provably cannot serve all regimes, so the gate is
  genuinely testable. We did NOT tune the streams to manufacture a pass — the FROZEN
  falsifier bars below are unchanged from pre-registration.

FROZEN FALSIFIER (pre-registered BEFORE measuring; deterministic, >=8 seeds; metric =
substrate-native online next-step prediction error + ORDER-SENSITIVITY shuffle control, p7):
  F1 DERIVATIVE-WINS : on the time-ORDERED stream, DERIVATIVE-gated split achieves lower
     online next-step error than BOTH METRONOME and POSITIONAL, Cohen's d >= 0.8 each.
  F2 ORDER-SENSITIVE : the derivative arm's advantage VANISHES on a time-SHUFFLED control
     (it must exploit real temporal structure, not a static artifact) —
     derivative-vs-metronome d on the SHUFFLED stream < 0.3.
  F3 TICK-NECESSITY  : does ANY input-driven gate beat a NO-GATE baseline (blind fixed-count
     split)?  derivative beats no-gate with d >= 0.8  =>  a TICK IS needed AND should be
     event/derivative-driven.  If metronome ties derivative AND both tie no-gate =>
     "no special tick-gating needed, a blind clock suffices" (honest negative).
  SUPPORTED (GREEN, EVENT-DERIVATIVE-TICK) iff F1 AND F2 AND F3-derivative-beats-nogate.
  Otherwise CLOSED-NEGATIVE with the specific ruling
  ("metronome / blind clock suffices" / "no gate needed" / "derivative not order-sensitive").

Cohen's d is a PAIRED effect size (per-seed deltas; arms see the SAME stream per seed):
  d(A,B) = mean(err_A - err_B)/std(err_A - err_B), POSITIVE when B (2nd arg) is BETTER
  (lower error). We report d(metronome, derivative) etc. so a POSITIVE d means derivative wins.

toy ($0 CPU, numpy only, deterministic seeds). a_toy_scale_recheck / a_scale_honest_scope:
TOY ONLY — live CORE engine_mitosis_tick + real-audio + production scale UNVERIFIED.
Lane-M gradient-free growth lane (recorded SEPARATELY from Lane A AKIDA / Lane G forge /
Lane P torch per a_lane_akida_gpu_split).
"""
import json, math, os
import numpy as np

# ---- substrate / stream config (reuses the H_1159 mitosis hyper-params) -------------
DIM = 8                 # feature dim
T = 2400               # scored stream length (steps)
WARMUP = 250
N_SEEDS = 10
SEEDS = list(range(900, 900 + N_SEEDS))
WIN = 150              # running-tension + error window
LR = 0.08              # online-mean adaptation rate (prototype + next-delta)
MAX_CELLS = 6          # SCARCE capacity on purpose (so split PLACEMENT is testable)
DERIV_REFRAC = 30       # DERIVATIVE: refractory steps after a rising-edge fire
WIN_BYTES = 48          # sliding byte window for the text feature
STRIDE = 24             # step the byte window by this many bytes per stream-step
N_REGIMES_AUDIO = 6     # recurring-regime synthetic audio
CORPUS = os.path.join(os.path.dirname(__file__), "..", "CORE", "testdata", "clm_mid_5lang_c4.txt")

np.seterr(all="ignore")


# ====================================================================================
# STREAM BUILDERS  (time-ordered features; NO shuffle, NO epochs at build time)
# ====================================================================================
def _byte_feature(window):
    """8-d local byte-statistics over a byte window (the text 'input' vector)."""
    b = np.frombuffer(window, dtype=np.uint8).astype(float)
    if b.size == 0:
        return np.zeros(DIM)
    return np.array([
        b.mean() / 255.0,                       # mean byte value
        (b >= 128).mean(),                       # non-ascii / multibyte ratio (script changes)
        ((b >= 97) & (b <= 122)).mean(),         # lowercase-letter ratio
        (b == 32).mean(),                        # space ratio (word boundaries)
        ((b >= 48) & (b <= 57)).mean(),          # digit ratio
        b.var() / (255.0 ** 2),                  # byte-value variance (texture)
        ((b >= 33) & (b <= 64)).mean(),          # punctuation-ish ratio
        (b < 64).mean(),                         # low-byte ratio (control / structural)
    ], dtype=float) * 5.0                        # scale ~ H_1159 well-separated centers


def make_text_stream(seed):
    """Real text bytes in TIME-ORDER. seed only picks a deterministic START OFFSET into the
    corpus (a different real slice per seed) — the slice itself is NEVER shuffled."""
    data = open(CORPUS, "rb").read()
    need = WARMUP + T + 1
    span = WIN_BYTES + STRIDE * need
    if len(data) <= span + 1:
        data = data * (span // max(len(data), 1) + 2)
    rng = np.random.default_rng(seed)
    start = int(rng.integers(0, max(1, len(data) - span - 1)))
    X = np.empty((need, DIM))
    for i in range(need):
        p = start + i * STRIDE
        X[i] = _byte_feature(data[p:p + WIN_BYTES])
    return X


def make_audio_stream(seed):
    """SYNTHETIC RECURRING-REGIME audio-frame stream: K regimes, each with its OWN center +
    constant drift; the schedule REVISITS regimes for random dwell-times. A single global
    next-delta cannot serve all regimes (so capacity placement matters). The |d/dt| spikes
    at every regime transition (the event the derivative gate is meant to catch)."""
    rng = np.random.default_rng(seed + 1234)
    K = N_REGIMES_AUDIO
    centers = rng.standard_normal((K, DIM)) * 5.0
    drifts = rng.standard_normal((K, DIM)); drifts /= np.linalg.norm(drifts, axis=1, keepdims=True); drifts *= 0.8
    need = WARMUP + T + 1
    X = np.empty((need, DIM)); pos = centers[0].copy(); r = 0; dwell = 0
    for t in range(need):
        if dwell <= 0:
            r = int(rng.integers(K)); pos = centers[r].copy(); dwell = int(rng.integers(40, 90))
        pos = pos + drifts[r] + rng.standard_normal(DIM) * 0.12
        dwell -= 1
        X[t] = pos
    return X


# ====================================================================================
# MITOSIS ENGINE  (H_1159 prototype-split substrate; ONLY the split-gate is swapped)
# ====================================================================================
def assign(cells, x):
    d = np.linalg.norm(cells - x[None], axis=1)
    j = int(np.argmin(d))
    return j, float(d[j])


def run_arm(X, gate, seed):
    """Online next-step prediction with tension-driven prototype-split mitosis.
    gate in {METRONOME, POSITIONAL, DERIVATIVE, NOGATE}.
    Returns mean next-step error over the final window + #splits.

    All gates share THE SAME mitosis substrate, online update, tension bookkeeping, and
    MAX_CELLS cap. They differ ONLY in WHEN the (highest-tension) split fires:
      METRONOME : fire on a fixed exogenous clock (every metro_every steps).
      POSITIONAL: fire at a fixed schedule of absolute stream indices (evenly spaced).
      DERIVATIVE: fire on a rising-edge of |d(feature)/dt| (the input's own change events).
      NOGATE    : fire blindly on a clock to reach the SAME split budget, ignoring the input.
    When a gate fires, the cell that divides is always the HIGHEST-tension cell (p8) — so the
    arms are matched on WHICH cell splits, isolating WHEN (the tick-gate) as the only variable.
    All gates are budget-MATCHED to the expected derivative-fire count so capacity-add is equal.
    """
    rng = np.random.default_rng(seed + 5000)
    cells = X[:2].copy().astype(float)
    nexts = np.zeros((2, DIM))                       # per-cell running "next - current" delta
    for t in range(WARMUP - 1):
        j, _ = assign(cells, X[t])
        cells[j] += LR * (X[t] - cells[j])
        nexts[j] += LR * ((X[t + 1] - X[t]) - nexts[j])
    ten = np.zeros(len(cells))
    errs = np.empty(T)
    n_splits = 0
    last_fire = -10 ** 9

    # input |d/dt| + rising-edge threshold (derived from WARMUP only — no peeking at scored region)
    dnorm = np.linalg.norm(np.diff(X, axis=0, prepend=X[:1]), axis=1)
    dthr = np.quantile(dnorm[:WARMUP], 0.85)

    # shared split BUDGET = expected derivative-fire count (refractory-limited), capped to capacity
    deriv_fires = int(np.sum([(dnorm[t] > dthr) and (dnorm[t - 1] <= dthr)
                              for t in range(WARMUP, WARMUP + T)]))
    budget = int(np.clip(min(deriv_fires, MAX_CELLS - 2), 1, MAX_CELLS - 2))
    metro_every = max(1, T // max(budget, 1))
    pos_idx = set(int(WARMUP + (i + 1) * (T / (budget + 1))) for i in range(budget))

    def do_split(src):
        nonlocal cells, nexts, ten, n_splits
        daughter = cells[src] + rng.standard_normal(DIM) * 0.3
        cells = np.vstack([cells, daughter[None]])
        nexts = np.vstack([nexts, nexts[src][None]])
        ten = np.concatenate([ten, [0.0]]); ten[src] = 0.0
        n_splits += 1

    for i, t in enumerate(range(WARMUP, WARMUP + T)):
        x = X[t]
        j, d = assign(cells, x)
        pred_next = x + nexts[j]                       # 1-step prediction anchored on owner cell
        true_next = X[t + 1]
        errs[i] = float(np.linalg.norm(pred_next - true_next))
        # online (gradient-free) update, p8
        cells[j] += LR * (x - cells[j])
        nexts[j] += LR * ((true_next - x) - nexts[j])
        ten[j] += (d - ten[j]) / WIN                   # EMA assignment-tension of the hit cell

        # ---- the ONLY difference between arms: WHEN does a split fire? ----
        if gate == "METRONOME":
            fire = (i > 0 and i % metro_every == 0)
        elif gate == "POSITIONAL":
            fire = (t in pos_idx)
        elif gate == "DERIVATIVE":
            rising = (dnorm[t] > dthr) and (dnorm[t - 1] <= dthr)
            fire = rising and (i - last_fire) >= DERIV_REFRAC
        else:  # NOGATE — blind clock, ignores the input, same budget
            fire = (i > 0 and i % metro_every == 0)

        if fire and len(cells) < MAX_CELLS:
            src = int(np.argmax(ten))                  # divide the HIGHEST-tension cell (p8)
            do_split(src)
            last_fire = i

    return float(errs[-WIN:].mean()), n_splits


# ====================================================================================
# STATS
# ====================================================================================
def cohen_d_paired(err_a, err_b):
    """Paired effect size on per-seed deltas. POSITIVE => b (2nd arg) is BETTER (lower error)."""
    diff = np.asarray(err_a, float) - np.asarray(err_b, float)   # a - b ; >0 when a worse
    sd = np.std(diff)
    if sd < 1e-12:
        return 0.0
    return float(np.mean(diff) / sd)


def eval_stream(name, builder):
    arms = ("METRONOME", "POSITIONAL", "DERIVATIVE", "NOGATE")
    err = {a: [] for a in arms}
    err_shuf = {a: [] for a in arms}            # time-shuffled control (order destroyed)
    splits = {a: [] for a in arms}
    for s in SEEDS:
        X = builder(s)
        rngs = np.random.default_rng(s + 99991)
        perm = rngs.permutation(T)
        Xs = X.copy()
        Xs[WARMUP:WARMUP + T] = X[WARMUP:WARMUP + T][perm]   # shuffle the SCORED region's time order
        for a in arms:
            e, ns = run_arm(X, a, s); err[a].append(e); splits[a].append(ns)
            es, _ = run_arm(Xs, a, s); err_shuf[a].append(es)
    return {
        "stream": name,
        "mean_err": {a: float(np.mean(err[a])) for a in arms},
        "std_err": {a: float(np.std(err[a])) for a in arms},
        "mean_splits": {a: float(np.mean(splits[a])) for a in arms},
        "mean_err_shuffled": {a: float(np.mean(err_shuf[a])) for a in arms},
        "_raw": {a: err[a] for a in arms},
        "_raw_shuf": {a: err_shuf[a] for a in arms},
    }


def verdict_for(stats):
    d_metro = cohen_d_paired(stats["_raw"]["METRONOME"], stats["_raw"]["DERIVATIVE"])
    d_pos = cohen_d_paired(stats["_raw"]["POSITIONAL"], stats["_raw"]["DERIVATIVE"])
    d_nog = cohen_d_paired(stats["_raw"]["NOGATE"], stats["_raw"]["DERIVATIVE"])
    d_metro_shuf = cohen_d_paired(stats["_raw_shuf"]["METRONOME"], stats["_raw_shuf"]["DERIVATIVE"])
    d_metro_vs_nogate = cohen_d_paired(stats["_raw"]["NOGATE"], stats["_raw"]["METRONOME"])

    f1 = (d_metro >= 0.8) and (d_pos >= 0.8)
    f2 = (d_metro_shuf < 0.3)
    f3_deriv_beats_nogate = (d_nog >= 0.8)
    supported = bool(f1 and f2 and f3_deriv_beats_nogate)

    if supported:
        ruling = ("SUPPORTED (EVENT-DERIVATIVE-TICK): a TICK IS needed AND should be "
                  "event/derivative-driven — derivative-gated split beats BOTH metronome and "
                  "positional on the ordered stream (F1), its advantage VANISHES on the "
                  "time-shuffled control (F2 order-sensitive), and it beats the input-blind "
                  "no-gate baseline (F3). The growth-tick should fire on |d(input)/dt| events.")
    else:
        why = []
        if not f1:
            why.append(f"F1 fail: derivative does NOT clearly beat both metronome (d={d_metro:.2f}) "
                       f"and positional (d={d_pos:.2f}); >=0.8 each required")
        if not f2:
            why.append(f"F2 fail: advantage SURVIVES shuffle (d_shuf={d_metro_shuf:.2f} >= 0.3) — "
                       f"not exploiting real temporal structure")
        if not f3_deriv_beats_nogate:
            why.append(f"F3 fail: derivative does NOT beat no-gate (d={d_nog:.2f} < 0.8)")
        if (not f3_deriv_beats_nogate) and abs(d_metro) < 0.8 and abs(d_metro_vs_nogate) < 0.8:
            why.append("=> 'no special tick-gating needed, a blind clock roughly suffices': "
                       "metronome ties derivative and both tie no-gate at toy scale under "
                       "the next-step-error metric")
        ruling = "CLOSED-NEGATIVE: " + " | ".join(why)

    return {
        "stream": stats["stream"],
        "F1_derivative_wins": {"d_metro_vs_deriv": d_metro, "d_pos_vs_deriv": d_pos,
                               "bar": 0.8, "pass": bool(f1),
                               "note": "positive d => derivative (2nd arg) is better/lower-error"},
        "F2_order_sensitive": {"d_metro_vs_deriv_SHUFFLED": d_metro_shuf, "bar_below": 0.3,
                               "pass": bool(f2)},
        "F3_tick_necessity": {"d_nogate_vs_deriv": d_nog, "bar": 0.8,
                              "derivative_beats_nogate": bool(f3_deriv_beats_nogate),
                              "d_nogate_vs_metro": d_metro_vs_nogate},
        "supported": supported,
        "ruling": ruling,
    }


def main():
    print("=== H_1160 — does the mitosis growth-tick need a metronome, or is it "
          "DERIVATIVE/event-driven? (틱이 있어야 되나?) ===", flush=True)
    print(f"  4 tick-gates {{METRONOME, POSITIONAL, DERIVATIVE, NOGATE}} x stream x shuffle-control; "
          f"{N_SEEDS} seeds, T={T}, MAX_CELLS={MAX_CELLS} (scarce-on-purpose)", flush=True)
    print("  metric = substrate-native ONLINE NEXT-STEP prediction error (p7, NOT perplexity/CE); "
          "order-sensitivity via a time-SHUFFLE control\n", flush=True)

    results = {}
    print("--- STREAM: TEXT (real bytes, time-ordered, CORE/testdata/clm_mid_5lang_c4.txt) [DECISIVE] ---", flush=True)
    txt = eval_stream("text", make_text_stream)
    for a in ("METRONOME", "POSITIONAL", "DERIVATIVE", "NOGATE"):
        print(f"  {a:10s} err={txt['mean_err'][a]:.4f}±{txt['std_err'][a]:.4f}  "
              f"shuf={txt['mean_err_shuffled'][a]:.4f}  splits={txt['mean_splits'][a]:.1f}", flush=True)
    vtxt = verdict_for(txt); results["text"] = vtxt
    print(f"  TEXT ruling: {vtxt['ruling']}\n", flush=True)

    print("--- STREAM: AUDIO (synthetic RECURRING-REGIME drift; confirmation, non-blocking) ---", flush=True)
    aud = eval_stream("audio", make_audio_stream)
    for a in ("METRONOME", "POSITIONAL", "DERIVATIVE", "NOGATE"):
        print(f"  {a:10s} err={aud['mean_err'][a]:.4f}±{aud['std_err'][a]:.4f}  "
              f"shuf={aud['mean_err_shuffled'][a]:.4f}  splits={aud['mean_splits'][a]:.1f}", flush=True)
    vaud = verdict_for(aud); results["audio"] = vaud
    print(f"  AUDIO ruling: {vaud['ruling']}\n", flush=True)

    terminal_supported = vtxt["supported"]
    verdict = {
        "H": "H_1160",
        "title": "does the from-scratch inference+learning mitosis growth-tick need a metronome, "
                 "or is it DERIVATIVE/event-driven? (틱이 있어야 되나?)",
        "frozen_falsifier": {
            "F1": "derivative beats BOTH metronome and positional on ordered stream, d>=0.8 each",
            "F2": "derivative advantage vanishes on time-SHUFFLED control, d_metro_vs_deriv_shuf < 0.3",
            "F3": "derivative beats input-blind NO-GATE baseline, d>=0.8 (tick necessity + event-driven)",
            "SUPPORTED": "F1 and F2 and F3-derivative-beats-nogate",
            "metric": "substrate-native ONLINE NEXT-STEP prediction error (p7, NOT perplexity/CE)",
        },
        "TEXT_decisive": vtxt,
        "AUDIO_confirmation": vaud,
        "tick_answer": ("EVENT/DERIVATIVE TICK NEEDED — gate the growth tick on |d(input)/dt| "
                        "rising-edges, not on a metronome"
                        if terminal_supported else
                        "NO EVENT-DERIVATIVE TICK ADVANTAGE under next-step error at toy scale — "
                        "a blind clock roughly suffices for online next-step prediction; the WHEN "
                        "of the growth-tick barely changes next-step error (see TEXT ruling). NOTE: "
                        "the prior toy-EEG d/dt win (clm-time-encoding.tape) was on a DECODE/RECON "
                        "metric, NOT next-step error — so the derivative tick may still matter for "
                        "regime-decode/recon while being near-irrelevant for next-step prediction. "
                        "Ruling: " + vtxt["ruling"]),
        "supported": bool(terminal_supported),
        "audio_agrees": bool(vaud["supported"]),
        "scope": "TOY ONLY ($0 CPU numpy, %d seeds). Reuses the H_1159/H_1159b prototype-split "
                 "mitosis substrate; swaps ONLY the split-trigger gate. Capacity SCARCE (MAX_CELLS=%d) "
                 "so split-placement is testable. Live CORE engine_mitosis_tick (CORE/engine_cli.hexa) "
                 "+ real-audio + production scale UNVERIFIED (a_toy_scale_recheck, a_scale_honest_scope). "
                 "Lane-M gradient-free growth lane (separate from Lane A AKIDA / Lane G forge / "
                 "Lane P torch, a_lane_akida_gpu_split)." % (N_SEEDS, MAX_CELLS),
    }
    print("=== VERDICT (TEXT decisive; AUDIO confirmation) ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1160_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done]", flush=True)


if __name__ == "__main__":
    main()
