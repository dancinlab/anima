"""
H_1163 — the H_1160 RESIDUAL: does the DERIVATIVE-gated mitosis TICK beat
METRONOME and POSITIONAL on a STAGE-DECODE / RECON-FIDELITY metric (NOT
next-step prediction), with a phase-shuffle control?

H_1160 (MITOSIS-ENGINE, 🔴 CLOSED-NEGATIVE) found that swapping the cell-division
split-trigger among {METRONOME, POSITIONAL, DERIVATIVE, NOGATE} gives NO advantage
on the substrate-native ONLINE NEXT-STEP PREDICTION ERROR metric — all four gates
tie within noise. But H_1160's honest residual was explicit:

  "a next-step-error metric is the wrong instrument to detect a tick-placement
   effect; a decode/recon re-test of the tick-gate (per clm-time-encoding) would
   be the decisive follow-up."

clm-time-encoding (🟢 NUMERICAL-TOY) had ALREADY shown — on the synthetic-EEG
mitosis harness — that M3 DERIVATIVE d/dt was the ONLY temporal-encoding arm to
BEAT the phase-shuffled control AND lift STAGE-DECODE to 1.000 (>> chance), while
M1 positional / M4 window failed (single-stage trigger collapse, decode 0.0) and
M2 phase-clock half-failed. CRUCIALLY that win was on a DECODE/RECON metric, NOT
next-step prediction. H_1160 left open whether the SAME derivative-tick advantage
recurs on the GENERAL H_1160 tick-gating substrate when scored on decode/recon.

THIS HYPOTHESIS (H_1163) tests exactly that residual: re-run the H_1160 4-gate
substrate on the H_1160 streams (TEXT real-bytes + AUDIO recurring-regime), but
score with the clm-time-encoding STAGE-DECODE accuracy + RECON-FIDELITY margin
(reused VERBATIM in spirit), NOT next-step error. The stream now carries a STAGE
label per tick (AUDIO = the active regime id; TEXT = a quantized byte-feature
stage) so stage-decode is well-defined. A cell records its BIRTH-STAGE; the
decoder builds per-stage centroids from cells grouped by birth-stage and
nearest-centroid-classifies each true tick (the clm-time-encoding decoder).

MECHANISM PREDICTION (from clm-time-encoding): the DERIVATIVE tick fires on a
rising-edge of |d(input)/dt| = a regime/stage TRANSITION, so cells are born under
DISTINCT stages -> the per-stage centroids separate -> high stage-decode. The
METRONOME/POSITIONAL/NOGATE clocks fire blind to the input, so birth-stage is the
stage that happens to be active on the clock tick (dwell-weighted, NOT
transition-aligned) -> birth-stage skews to the long-dwell stage -> fewer stages
spawn cells -> lower decode. If that mechanism holds GENERALLY (not just on
synthetic EEG) the derivative tick WINS on decode while H_1160 showed it ties on
next-step error: a clean METRIC-DEPENDENCE resolution of the residual.

FROZEN FALSIFIER (pre-registered BEFORE measuring; deterministic, >=8 seeds;
metric = STAGE-DECODE accuracy (primary) + RECON-fidelity margin (corroborating),
p7 — NOT perplexity, NOT next-step error):
  F1 DERIVATIVE-WINS-ON-DECODE : on the time-ORDERED stream, the DERIVATIVE-gated
     split achieves HIGHER stage-decode accuracy than BOTH METRONOME and
     POSITIONAL, paired Cohen's d >= 0.8 each.
  F2 ORDER-SENSITIVE : the derivative arm's decode advantage VANISHES on the
     phase-SHUFFLED control (it must exploit real temporal structure, not a static
     artifact) — derivative-vs-metronome decode d on the SHUFFLED stream < 0.3.
  F3 BEATS-NOGATE : the derivative arm beats the input-blind NO-GATE baseline on
     stage-decode, paired Cohen's d >= 0.8.
  SUPPORTED (GREEN) iff F1 AND F2 AND F3 -> the tick-gate DOES matter, but only on
  a dynamics/decode metric (resolving H_1160's metric-dependence honestly).
  Otherwise CLOSED-NEGATIVE -> tick-gating gives no advantage on EITHER metric axis
  at toy scale (a_paper_negative_ok).

Cohen's d is PAIRED on per-seed deltas (arms see the SAME stream per seed):
  d(deriv, other) = mean(acc_deriv - acc_other)/std(acc_deriv - acc_other),
  POSITIVE when DERIVATIVE (1st arg) is BETTER (higher decode accuracy). We report
  d(DERIVATIVE, METRONOME) etc. so a POSITIVE d means derivative wins on decode.

REUSE: the H_1160 4-gate mitosis substrate (UNIVERSE/h1160_derivative_gated_tick.py:
prototype-split engine, budget-matched split clocks, MAX_CELLS scarce cap, the
identical TEXT + recurring-regime AUDIO streams) + the clm-time-encoding
stage-decode + recon-fidelity metric (CLM/bench/clm_time_encoding.py:
stage_decode_accuracy nearest-centroid-from-birth-stage; temporal_reconstruct_error).
The ONLY changes vs H_1160: (1) each stream tick carries a STAGE label, (2) cells
record birth-stage, (3) the SCORE is stage-decode + recon margin instead of
next-step error. The split-gates, budget, capacity cap, online update are VERBATIM.

toy ($0 CPU, numpy only, deterministic seeds). a_toy_scale_recheck /
a_scale_honest_scope: TOY ONLY — live CORE engine_mitosis_tick + real-audio +
production scale UNVERIFIED. Lane-M gradient-free growth lane (recorded SEPARATELY
from Lane A AKIDA / Lane G forge / Lane P torch per a_lane_akida_gpu_split).
"""
import json, math, os
import numpy as np

# ---- substrate / stream config (VERBATIM from H_1160) -------------------------------
DIM = 8
T = 2400
WARMUP = 250
N_SEEDS = 10
SEEDS = list(range(900, 900 + N_SEEDS))
WIN = 150
LR = 0.08
MAX_CELLS = 6           # SCARCE capacity on purpose (split PLACEMENT testable)
DERIV_REFRAC = 30
WIN_BYTES = 48
STRIDE = 24
N_REGIMES_AUDIO = 6     # recurring-regime synthetic audio: K regimes = K stages
N_STAGES_TEXT = 4       # text stage = byte-feature cluster id (decode chance = 1/4)
CORPUS = os.path.join(os.path.dirname(__file__), "..", "CORE", "testdata", "clm_mid_5lang_c4.txt")

np.seterr(all="ignore")


# ====================================================================================
# STREAM BUILDERS — VERBATIM H_1160 features, PLUS a per-tick STAGE label so the
# clm-time-encoding stage-decode metric is defined on these streams.
# ====================================================================================
def _byte_feature(window):
    """8-d local byte-statistics over a byte window (VERBATIM H_1160 text feature)."""
    b = np.frombuffer(window, dtype=np.uint8).astype(float)
    if b.size == 0:
        return np.zeros(DIM)
    return np.array([
        b.mean() / 255.0,
        (b >= 128).mean(),
        ((b >= 97) & (b <= 122)).mean(),
        (b == 32).mean(),
        ((b >= 48) & (b <= 57)).mean(),
        b.var() / (255.0 ** 2),
        ((b >= 33) & (b <= 64)).mean(),
        (b < 64).mean(),
    ], dtype=float) * 5.0


def _text_stage(feat):
    """Derive a discrete STAGE label for a text tick from its byte feature.
    Stage = the script/register regime the window falls in, quantized from two
    feature axes the EEG analogue calls 'level' bands: non-ascii (multibyte/script)
    ratio x lowercase-letter ratio. 4 well-separated regimes (decode chance 0.25):
      0 = ascii-text-heavy (low non-ascii, high lowercase)  [latin prose]
      1 = ascii-structural (low non-ascii, low lowercase)   [digits/punct/markup]
      2 = multibyte-light  (mid non-ascii)                  [mixed script]
      3 = multibyte-heavy  (high non-ascii)                 [cjk / cyrillic runs]
    These are the SAME byte axes H_1160's feature already encodes; we only READ
    them out as a label (no new signal injected)."""
    nonascii = feat[1] / 5.0     # undo the *5.0 scale -> back to a ratio in [0,1]
    lower = feat[2] / 5.0
    if nonascii >= 0.30:
        return 3
    if nonascii >= 0.10:
        return 2
    return 0 if lower >= 0.25 else 1


def make_text_stream(seed):
    """Real text bytes in TIME-ORDER (VERBATIM H_1160) + a per-tick stage label."""
    data = open(CORPUS, "rb").read()
    need = WARMUP + T + 1
    span = WIN_BYTES + STRIDE * need
    if len(data) <= span + 1:
        data = data * (span // max(len(data), 1) + 2)
    rng = np.random.default_rng(seed)
    start = int(rng.integers(0, max(1, len(data) - span - 1)))
    X = np.empty((need, DIM))
    stages = np.empty(need, dtype=int)
    for i in range(need):
        p = start + i * STRIDE
        X[i] = _byte_feature(data[p:p + WIN_BYTES])
        stages[i] = _text_stage(X[i])
    return X, stages


def make_audio_stream(seed):
    """SYNTHETIC RECURRING-REGIME audio (VERBATIM H_1160) + per-tick stage = regime id.
    K regimes each w/ own center+drift; schedule REVISITS regimes. The active regime
    r IS the stage label (decode chance = 1/K)."""
    rng = np.random.default_rng(seed + 1234)
    K = N_REGIMES_AUDIO
    centers = rng.standard_normal((K, DIM)) * 5.0
    drifts = rng.standard_normal((K, DIM)); drifts /= np.linalg.norm(drifts, axis=1, keepdims=True); drifts *= 0.8
    need = WARMUP + T + 1
    X = np.empty((need, DIM)); stages = np.empty(need, dtype=int)
    pos = centers[0].copy(); r = 0; dwell = 0
    for t in range(need):
        if dwell <= 0:
            r = int(rng.integers(K)); pos = centers[r].copy(); dwell = int(rng.integers(40, 90))
        pos = pos + drifts[r] + rng.standard_normal(DIM) * 0.12
        dwell -= 1
        X[t] = pos
        stages[t] = r
    return X, stages


# ====================================================================================
# MITOSIS ENGINE — H_1160 prototype-split substrate VERBATIM; ONLY the split-gate is
# swapped. The single ADDITION vs H_1160: a cell records its BIRTH-STAGE (the true
# stage active at the tick it was spawned), so the clm-time-encoding stage-decode
# metric can group cells by birth-stage. Split timing, budget, capacity, online
# update, owner-cell selection are UNCHANGED.
# ====================================================================================
def assign(cells, x):
    d = np.linalg.norm(cells - x[None], axis=1)
    j = int(np.argmin(d))
    return j, float(d[j])


def grow_arm(X, stages, gate, seed):
    """Grow the mitosis structure under a given split-gate. Returns:
      cell_states  : (n_cells, DIM) final prototype vectors
      cell_stage   : (n_cells,) birth-stage of each cell (-1 for the 2 seed cells)
    The split-gates are VERBATIM H_1160 (METRONOME / POSITIONAL / DERIVATIVE / NOGATE),
    budget-matched to the expected derivative-fire count, capped at MAX_CELLS, and the
    cell that divides is always the HIGHEST-tension cell (p8)."""
    rng = np.random.default_rng(seed + 5000)
    cells = X[:2].copy().astype(float)
    nexts = np.zeros((2, DIM))
    cell_stage = [-1, -1]                       # seed cells have no birth-stage
    for t in range(WARMUP - 1):
        j, _ = assign(cells, X[t])
        cells[j] += LR * (X[t] - cells[j])
        nexts[j] += LR * ((X[t + 1] - X[t]) - nexts[j])
    ten = np.zeros(len(cells))
    last_fire = -10 ** 9

    dnorm = np.linalg.norm(np.diff(X, axis=0, prepend=X[:1]), axis=1)
    dthr = np.quantile(dnorm[:WARMUP], 0.85)

    deriv_fires = int(np.sum([(dnorm[t] > dthr) and (dnorm[t - 1] <= dthr)
                              for t in range(WARMUP, WARMUP + T)]))
    budget = int(np.clip(min(deriv_fires, MAX_CELLS - 2), 1, MAX_CELLS - 2))
    metro_every = max(1, T // max(budget, 1))
    pos_idx = set(int(WARMUP + (i + 1) * (T / (budget + 1))) for i in range(budget))

    def do_split(src, birth_stage):
        nonlocal cells, nexts, ten
        daughter = cells[src] + rng.standard_normal(DIM) * 0.3
        cells = np.vstack([cells, daughter[None]])
        nexts = np.vstack([nexts, nexts[src][None]])
        ten = np.concatenate([ten, [0.0]]); ten[src] = 0.0
        cell_stage.append(int(birth_stage))

    for i, t in enumerate(range(WARMUP, WARMUP + T)):
        x = X[t]
        j, d = assign(cells, x)
        true_next = X[t + 1]
        cells[j] += LR * (x - cells[j])
        nexts[j] += LR * ((true_next - x) - nexts[j])
        ten[j] += (d - ten[j]) / WIN

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
            src = int(np.argmax(ten))
            do_split(src, stages[t])            # birth-stage = the TRUE stage at this tick
            last_fire = i

    return cells, np.asarray(cell_stage, dtype=int)


# ====================================================================================
# DECODE / RECON METRIC — clm-time-encoding (CLM/bench/clm_time_encoding.py) reused.
#   stage_decode_accuracy : per-stage centroid from cells grouped by BIRTH-STAGE,
#       then nearest-centroid classify each TRUE-stream tick. Accuracy vs true stage.
#       chance = 1/n_stages. If cells of different stages are indistinguishable (the
#       clm-time-encoding single-stage-trigger collapse) -> ~chance / 0.
#   recon_fidelity_margin : the order-sensitivity recon read-out — mean nearest-cell
#       distance to each true tick (lower = the grown structure tiles the stream's
#       regimes better). A corroborating axis (clm-time-encoding metric (a)).
# ====================================================================================
def stage_decode_accuracy(cell_states, cell_stage, X, stages, n_stages):
    """clm-time-encoding stage_decode_accuracy: centroids from cells grouped by their
    birth-stage; nearest-centroid classify each true tick. Chance = 1/n_stages.
    If <2 stages spawned cells -> cannot decode -> 0.0 (honest, NOT chance)."""
    groups = {}
    for st, state in zip(cell_stage, cell_states):
        if st < 0:
            continue
        groups.setdefault(int(st), []).append(state)
    if len(groups) < 2:
        return 0.0
    labels = sorted(groups.keys())
    centroids = np.array([np.mean(groups[st], axis=0) for st in labels])
    Xs = X[WARMUP:WARMUP + T]
    ss = stages[WARMUP:WARMUP + T]
    dists = np.linalg.norm(Xs[:, None, :] - centroids[None, :, :], axis=2)  # (T, n_groups)
    pred = np.array(labels)[np.argmin(dists, axis=1)]
    return float(np.mean(pred == ss))


def recon_fidelity(cell_states, X):
    """clm-time-encoding temporal_reconstruct_error analogue: mean nearest-cell
    distance over the scored region (lower = better tiling of the stream's regimes).
    Returned as a FIDELITY = -error so 'higher is better' matches decode for d signs."""
    Xs = X[WARMUP:WARMUP + T]
    d = np.linalg.norm(Xs[:, None, :] - cell_states[None, :, :], axis=2)  # (T, n_cells)
    return float(-np.mean(np.min(d, axis=1)))


# ====================================================================================
# STATS — paired Cohen's d, POSITIVE => DERIVATIVE (1st arg) is BETTER (higher decode).
# ====================================================================================
def cohen_d_paired(acc_deriv, acc_other):
    diff = np.asarray(acc_deriv, float) - np.asarray(acc_other, float)   # deriv - other
    sd = np.std(diff)
    if sd < 1e-12:
        return 0.0
    return float(np.mean(diff) / sd)


def eval_stream(name, builder, n_stages):
    arms = ("METRONOME", "POSITIONAL", "DERIVATIVE", "NOGATE")
    dec = {a: [] for a in arms}
    dec_shuf = {a: [] for a in arms}
    rec = {a: [] for a in arms}
    n_birth_stages = {a: [] for a in arms}
    for s in SEEDS:
        X, stages = builder(s)
        # phase-shuffle control: destroy time order in the SCORED region (X AND stages
        # permuted TOGETHER so stage labels stay attached to their feature — the
        # clm-time-encoding phase-shuffle: identical marginals, temporal order destroyed)
        rngs = np.random.default_rng(s + 99991)
        perm = rngs.permutation(T)
        Xs = X.copy(); ss = stages.copy()
        Xs[WARMUP:WARMUP + T] = X[WARMUP:WARMUP + T][perm]
        ss[WARMUP:WARMUP + T] = stages[WARMUP:WARMUP + T][perm]
        for a in arms:
            states, cstage = grow_arm(X, stages, a, s)
            dec[a].append(stage_decode_accuracy(states, cstage, X, stages, n_stages))
            rec[a].append(recon_fidelity(states, X))
            n_birth_stages[a].append(int(len(set(int(c) for c in cstage if c >= 0))))
            states_s, cstage_s = grow_arm(Xs, ss, a, s)
            dec_shuf[a].append(stage_decode_accuracy(states_s, cstage_s, Xs, ss, n_stages))
    return {
        "stream": name, "n_stages": n_stages, "chance": 1.0 / n_stages,
        "mean_decode": {a: float(np.mean(dec[a])) for a in arms},
        "std_decode": {a: float(np.std(dec[a])) for a in arms},
        "mean_decode_shuffled": {a: float(np.mean(dec_shuf[a])) for a in arms},
        "mean_recon_fidelity": {a: float(np.mean(rec[a])) for a in arms},
        "mean_birth_stages_spawned": {a: float(np.mean(n_birth_stages[a])) for a in arms},
        "_raw_dec": {a: dec[a] for a in arms},
        "_raw_dec_shuf": {a: dec_shuf[a] for a in arms},
        "_raw_rec": {a: rec[a] for a in arms},
    }


def verdict_for(stats):
    d_metro = cohen_d_paired(stats["_raw_dec"]["DERIVATIVE"], stats["_raw_dec"]["METRONOME"])
    d_pos = cohen_d_paired(stats["_raw_dec"]["DERIVATIVE"], stats["_raw_dec"]["POSITIONAL"])
    d_nog = cohen_d_paired(stats["_raw_dec"]["DERIVATIVE"], stats["_raw_dec"]["NOGATE"])
    d_metro_shuf = cohen_d_paired(stats["_raw_dec_shuf"]["DERIVATIVE"], stats["_raw_dec_shuf"]["METRONOME"])
    # corroborating recon-fidelity margins (higher fidelity = better)
    d_metro_rec = cohen_d_paired(stats["_raw_rec"]["DERIVATIVE"], stats["_raw_rec"]["METRONOME"])
    d_pos_rec = cohen_d_paired(stats["_raw_rec"]["DERIVATIVE"], stats["_raw_rec"]["POSITIONAL"])
    d_nog_rec = cohen_d_paired(stats["_raw_rec"]["DERIVATIVE"], stats["_raw_rec"]["NOGATE"])

    f1 = (d_metro >= 0.8) and (d_pos >= 0.8)
    f2 = (d_metro_shuf < 0.3)
    f3 = (d_nog >= 0.8)
    supported = bool(f1 and f2 and f3)

    if supported:
        ruling = ("SUPPORTED (DERIVATIVE-WINS-ON-DECODE): the tick-gate DOES matter on a "
                  "decode metric — derivative-gated split beats BOTH metronome and positional "
                  "on STAGE-DECODE (F1), its advantage VANISHES on the phase-shuffled control "
                  "(F2 order-sensitive), and it beats the input-blind no-gate baseline (F3). "
                  "RESOLVES H_1160's metric-dependence: tick-gating is near-irrelevant for "
                  "next-step prediction (H_1160 🔴) but DECISIVE for regime/stage decode.")
    else:
        why = []
        if not f1:
            why.append(f"F1 fail: derivative does NOT clearly beat both metronome "
                       f"(decode d={d_metro:.2f}) and positional (d={d_pos:.2f}); >=0.8 each required")
        if not f2:
            why.append(f"F2 fail: decode advantage SURVIVES shuffle (d_shuf={d_metro_shuf:.2f} >= 0.3) "
                       f"— not exploiting real temporal structure")
        if not f3:
            why.append(f"F3 fail: derivative does NOT beat no-gate on decode (d={d_nog:.2f} < 0.8)")
        ruling = "CLOSED-NEGATIVE: " + " | ".join(why)

    return {
        "stream": stats["stream"],
        "F1_derivative_wins_decode": {"d_deriv_vs_metro": d_metro, "d_deriv_vs_pos": d_pos,
                                      "bar": 0.8, "pass": bool(f1),
                                      "note": "positive d => DERIVATIVE (1st arg) higher decode"},
        "F2_order_sensitive": {"d_deriv_vs_metro_SHUFFLED": d_metro_shuf, "bar_below": 0.3,
                               "pass": bool(f2)},
        "F3_beats_nogate": {"d_deriv_vs_nogate": d_nog, "bar": 0.8, "pass": bool(f3)},
        "corroborating_recon_fidelity_d": {"d_deriv_vs_metro": d_metro_rec,
                                           "d_deriv_vs_pos": d_pos_rec, "d_deriv_vs_nogate": d_nog_rec},
        "supported": supported,
        "ruling": ruling,
    }


def main():
    print("=== H_1163 — the H_1160 RESIDUAL: does the DERIVATIVE tick win on a "
          "DECODE/RECON metric (not next-step prediction)? ===", flush=True)
    print(f"  4 tick-gates {{METRONOME, POSITIONAL, DERIVATIVE, NOGATE}} x stream x phase-shuffle; "
          f"{N_SEEDS} seeds, T={T}, MAX_CELLS={MAX_CELLS} (scarce-on-purpose)", flush=True)
    print("  metric = clm-time-encoding STAGE-DECODE accuracy (primary) + RECON-fidelity "
          "(corroborating), p7 — NOT perplexity, NOT next-step error\n", flush=True)

    results = {}
    print("--- STREAM: AUDIO (recurring-regime; K=%d stages = regime ids) [DECISIVE for decode] ---"
          % N_REGIMES_AUDIO, flush=True)
    aud = eval_stream("audio", make_audio_stream, N_REGIMES_AUDIO)
    for a in ("METRONOME", "POSITIONAL", "DERIVATIVE", "NOGATE"):
        print(f"  {a:10s} decode={aud['mean_decode'][a]:.4f}±{aud['std_decode'][a]:.4f}  "
              f"shuf={aud['mean_decode_shuffled'][a]:.4f}  recon_fid={aud['mean_recon_fidelity'][a]:.3f}  "
              f"birth_stages={aud['mean_birth_stages_spawned'][a]:.2f}", flush=True)
    print(f"  (chance = {aud['chance']:.4f})", flush=True)
    vaud = verdict_for(aud); results["audio"] = vaud
    print(f"  AUDIO ruling: {vaud['ruling']}\n", flush=True)

    print("--- STREAM: TEXT (real bytes; %d quantized byte-feature stages) [confirmation] ---"
          % N_STAGES_TEXT, flush=True)
    txt = eval_stream("text", make_text_stream, N_STAGES_TEXT)
    for a in ("METRONOME", "POSITIONAL", "DERIVATIVE", "NOGATE"):
        print(f"  {a:10s} decode={txt['mean_decode'][a]:.4f}±{txt['std_decode'][a]:.4f}  "
              f"shuf={txt['mean_decode_shuffled'][a]:.4f}  recon_fid={txt['mean_recon_fidelity'][a]:.3f}  "
              f"birth_stages={txt['mean_birth_stages_spawned'][a]:.2f}", flush=True)
    print(f"  (chance = {txt['chance']:.4f})", flush=True)
    vtxt = verdict_for(txt); results["text"] = vtxt
    print(f"  TEXT ruling: {vtxt['ruling']}\n", flush=True)

    # AUDIO is the decisive arm for the DECODE metric (recurring regimes = clean stage
    # structure, the analogue of clm-time-encoding's well-separated EEG stages); TEXT is
    # a confirmation on real bytes (quantized stages are noisier).
    terminal_supported = vaud["supported"]
    verdict = {
        "H": "H_1163",
        "title": "the H_1160 RESIDUAL — does the DERIVATIVE-gated mitosis tick beat metronome "
                 "and positional on a STAGE-DECODE / RECON-fidelity metric (NOT next-step "
                 "prediction), with a phase-shuffle control?",
        "frozen_falsifier": {
            "F1": "derivative beats BOTH metronome and positional on STAGE-DECODE, d>=0.8 each",
            "F2": "derivative decode advantage vanishes on phase-SHUFFLED control, d_shuf < 0.3",
            "F3": "derivative beats input-blind NO-GATE baseline on decode, d>=0.8",
            "SUPPORTED": "F1 and F2 and F3 (decode metric resolves H_1160's metric-dependence)",
            "metric": "clm-time-encoding STAGE-DECODE accuracy + RECON-fidelity (p7, NOT next-step error)",
        },
        "AUDIO_decisive": vaud,
        "TEXT_confirmation": vtxt,
        "metric_dependence_answer": (
            "DERIVATIVE WINS ON DECODE — the tick-gate is metric-dependent: H_1160 showed all 4 "
            "gates tie on next-step prediction error, but on the stage-decode/recon metric the "
            "DERIVATIVE tick beats metronome/positional/no-gate (order-sensitive). The derivative "
            "rising-edge fires at regime TRANSITIONS so cells are born under distinct stages, "
            "separating the per-stage centroids — exactly the clm-time-encoding mechanism, now "
            "confirmed on the general H_1160 substrate."
            if terminal_supported else
            "NO DERIVATIVE DECODE ADVANTAGE on the general H_1160 substrate — tick-gating gives no "
            "advantage on EITHER metric axis (next-step error per H_1160 🔴, AND stage-decode/recon "
            "here) at toy scale. The clm-time-encoding M3 d/dt decode win does NOT generalize from "
            "the synthetic-EEG harness to the H_1160 recurring-regime/text streams under this "
            "decode metric. AUDIO ruling: " + vaud["ruling"]),
        "supported": bool(terminal_supported),
        "text_agrees": bool(vtxt["supported"]),
        "scope": "TOY ONLY ($0 CPU numpy, %d seeds). Reuses the H_1160 4-gate prototype-split "
                 "mitosis substrate VERBATIM (swaps ONLY the split-trigger gate; adds a birth-stage "
                 "record) + the clm-time-encoding stage-decode + recon-fidelity metric. Capacity "
                 "SCARCE (MAX_CELLS=%d). Live CORE engine_mitosis_tick + real-audio + production "
                 "scale UNVERIFIED (a_toy_scale_recheck, a_scale_honest_scope). Lane-M gradient-free "
                 "growth lane (separate from Lane A AKIDA / Lane G forge / Lane P torch, "
                 "a_lane_akida_gpu_split)." % (N_SEEDS, MAX_CELLS),
    }
    print("=== VERDICT (AUDIO decisive for decode; TEXT confirmation) ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1163_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done]", flush=True)


if __name__ == "__main__":
    main()
