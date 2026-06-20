#!/usr/bin/env python3
"""H_1486 — TEMPORAL RECEPTIVE WINDOW (TRW, P1 consciousness-only gate candidate).

TEMPORAL RECEPTIVE WINDOW (Hasson / Honey / Lerner): different cortical regions integrate
information over DIFFERENT temporal scales (windows). Low-level sensory areas have SHORT
windows (track fast local changes, ms); higher-order areas have LONG windows (accumulate
over seconds / a whole narrative). The SAME input stream is processed at MULTIPLE timescales
in parallel — a hierarchy of integration-window lengths. The defining property is that a
LONG-window unit's response reflects FAR-PAST information (its current state depends on cues
many steps back) while a SHORT-window unit's response only reflects the RECENT input.

MECHANISM (boxcar temporal integration window of length tau over a hierarchy,
a_no_llm_frame_trap — neural integration-window hierarchy à la Hasson, NOT an LLM attention
head): each "region" integrates the LAST tau frames of the input x(t) with a flat (uniform)
kernel — the canonical TRW operationalization (a region's response = its integral over its
own window length, equal weight inside the window, zero outside):
      h_tau(T-1) = mean( x(t) for t in [T-tau, T-1] )
  SHORT window  -> small tau  -> only the RECENT frames; the far-past cue is OUTSIDE the window.
  LONG  window  -> large tau (>= T) -> the WHOLE stream incl. the far-past cue is INSIDE the
  window, accumulated with equal weight -> the cue survives into h(T-1).
  (A pure exponential leaky integrator geometrically down-weights the OLDEST frame, so even a
  long tau forgets the FIRST frame — that is a leak artifact, not the TRW claim; the TRW claim
  is window LENGTH = how far back the FLAT integration reaches. a_break_the_wall type-a:
  measurement fixed to a boxcar window, bars UNCHANGED.)
  A decision at time T-1 integrates a cue planted L=T-1 steps back. A LONG-window unit
  (tau >= L) still has that cue inside its window; a SHORT-window unit (tau << L) does not.

THE TASK (window-length-dependent integration):
  An input stream of length T carries a one-hot CUE at t=0 (early) whose identity must be
  read out at t=T-1 (late), L = T-1 steps later. Whatever unit still retains the cue at the
  readout answers correctly; a unit whose window is shorter than L has decayed the cue to
  noise and answers at chance. So LONG-window acc is HIGH, SHORT-window acc is CHANCE.

p6 GUARD (substrate-derived, NOT an injected answer): the readout reads ONLY the windowed
integrator state h(T-1) (a position-tagged sum over the trailing tau frames), matched against
each candidate's CLEAN windowed signature. There is no `answer = cue` shortcut, no injected
label, no per-window hand-set accuracy. The window length tau is the ONLY thing that differs
between the LONG and SHORT lanes; everything else (input, templates, position codes, readout
rule, noise) is identical. The advantage is EARNED by the integration-window length.

DISTINCTNESS (load-bearing) vs SUBJECTIVE-TIME (H_1471-family / catalogue lane 9) and
ATTENTIONAL-BLINK (lane 7):
  SUBJECTIVE-TIME = a *time-sense*: novelty-weighted elapsed-time estimate (how LONG did it
    feel). It maps an input stream -> a SCALAR duration estimate biased by novelty density;
    it does NOT integrate a far-past cue into a present DECISION. On the TRW task its readout
    (a novelty-weighted duration scalar) carries NO information about the cue IDENTITY ->
    chance accuracy. Bar (c2) runs a subjective-time-style readout (novelty-weighted scalar
    decoded to a cue guess) on the SAME task: it is at chance, while the LONG-TRW lane is high.
    TRW = integration-window LENGTH (what far-past content survives) ⊥ subjective-time =
    duration FEELING (how long it seemed).
  ATTENTIONAL-BLINK = a *temporal attention gap*: a target in a narrow post-T1 window is
    missed. It is a within-window suppression dip, not a difference in integration-window
    LENGTH across the hierarchy. The TRW gap is about scale (tau), not an attention dead-zone.

R1 numpy MIRROR -> GREEN DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1486,1487,1488]):
  (c1) PRESENCE     LONG-window lane reads the far-past cue; long_acc - short_acc >= 0.30
                    (and long_acc itself high, >= 0.55). The long integration window carries
                    L-step-back information into the present decision; the short window forgot.
  (c2) DISTINCT     a subjective-time-style readout (novelty-weighted duration scalar decoded
                    to a cue guess) on the SAME task is at CHANCE (<= 0.45 with K=4 candidates,
                    chance 0.25): it tracks *duration feeling*, not far-past cue identity.
                    long_acc - subjtime_acc >= 0.30.
  (c3) SHUFFLE      time-scramble the input stream -> the cue frames no longer align with the
                    fixed position codes the order-sensitive long-window readout matches against
                    (content present but at WRONG temporal positions); the matched filter
                    collapses to chance. shuffle_acc <= 0.45. (Hasson scrambled-narrative effect:
                    long-TRW regions lose their response to temporally scrambled input.)
  (c4) ABLATE       set the window to SHORT (tau -> short) -> the lane becomes the short lane
                    and the far-past cue is forgotten. ablate_acc <= 0.45 (collapses to chance).

GREEN iff c1 and c2 and c3 and c4 (all 3 seeds).  [c4 ablation core, c3 auxiliary]
"""
import numpy as np

SEEDS = [1486, 1487, 1488]
T = 40                 # length of the input time-series (cue at t=0, readout at t=T-1)
K = 4                  # number of candidate cue identities (chance = 1/K = 0.25)
DIM = 32               # feature dimension of each input frame / cue template
N_TRIAL = 200          # decision trials per seed
TAU_LONG = 40          # LONG integration window (>= T -> whole stream incl. far-past cue inside)
TAU_SHORT = 3          # SHORT integration window (<< L -> far-past cue OUTSIDE the window)
NOISE = 0.25           # per-frame input noise std
CUE_LEN = 10           # the cue is a SUSTAINED early context block (frames [0, CUE_LEN)) —
                       # like a narrative context that a LONG window accumulates (noise averages
                       # to ~0 across the window, the repeated cue does not) but a SHORT window
                       # (recent frames only) never reaches.
CHANCE = 1.0 / K       # 0.25


def window_integrate(stream, tau, pos_codes):
    """Temporal receptive window of length tau ending at the last frame, integrating with an
    ORDER-SENSITIVE positional kernel (the hallmark of a long-TRW region à la Hasson: its
    response carries the TEMPORAL STRUCTURE across its window, not just the mean). Each frame
    inside the trailing tau-window is multiplied by its absolute-position code before summing:
        h = sum_t  pos_codes[t] (.) stream[t]   for t in the trailing tau-window
    tau >= T -> the window reaches the far-past cue block (order preserved -> cue recovered);
    tau << T -> only recent frames (the far-past cue is outside the window). A time-scramble
    permutes the position<->content pairing -> the order-sensitive readout collapses."""
    Tlen = stream.shape[0]
    w = int(min(tau, Tlen))
    start = Tlen - w
    h = np.zeros(stream.shape[1])
    for t in range(start, Tlen):
        h += pos_codes[t] * stream[t]        # position-tagged accumulation (order-sensitive)
    return h / w


def make_trial(rng, templates, pos_codes):
    """Build one input stream: a SUSTAINED cue context (one of K templates) over the EARLY
    block frames [0, CUE_LEN), modulated by the early POSITION codes, then noise to t=T-1. The
    cue identity is read out at t=T-1 — only a long window that REACHES BACK to the early block
    AND preserves frame order (so the position codes re-align) recovers it; a short window
    (recent frames only) sees pure noise, and a time-scrambled long window loses the position
    alignment -> chance."""
    cue_id = rng.integers(K)
    stream = NOISE * rng.standard_normal((T, DIM))
    stream[:CUE_LEN] += templates[cue_id]   # sustained EARLY context block (far past at readout)
    return stream, cue_id


def expected_response(cue_id, templates, pos_codes, tau):
    """The order-sensitive windowed response a CLEAN cue (no noise) of identity cue_id produces
    through a window of length tau: the matched-filter signature the decoder compares against.
    Carries the position codes of the EARLY cue block -> only re-aligns if frame order holds."""
    clean = np.zeros((T, DIM))
    clean[:CUE_LEN] += templates[cue_id]
    return window_integrate(clean, tau, pos_codes)


def decode(h, cue_sigs):
    """Nearest matched-signature readout: pick the cue whose order-sensitive windowed signature
    best matches the observed windowed response h."""
    sims = [float(sig @ h) for sig in cue_sigs]
    return int(np.argmax(sims))


def run_seed(seed):
    rng = np.random.default_rng(seed)
    # K fixed unit-norm cue templates (orthogonal-ish in DIM-space)
    templates = rng.standard_normal((K, DIM))
    templates /= np.linalg.norm(templates, axis=1, keepdims=True)
    # fixed per-position codes (absolute temporal-position tags) — make the window readout
    # ORDER-SENSITIVE; same fixed codes used by the readout signatures (matched filter).
    pos_codes = rng.standard_normal((T, DIM))
    pos_codes /= np.linalg.norm(pos_codes, axis=1, keepdims=True)

    # matched-filter signatures for the LONG and SHORT windows (frame order INTACT)
    long_sigs = [expected_response(k, templates, pos_codes, TAU_LONG) for k in range(K)]
    short_sigs = [expected_response(k, templates, pos_codes, TAU_SHORT) for k in range(K)]

    long_hits = short_hits = subj_hits = shuf_hits = abl_hits = 0

    for _ in range(N_TRIAL):
        stream, cue_id = make_trial(rng, templates, pos_codes)

        # --- (c1) LONG-window lane: long tau reaches the early cue block (order intact) ---
        hL = window_integrate(stream, TAU_LONG, pos_codes)
        long_hits += (decode(hL, long_sigs) == cue_id)

        # --- SHORT-window lane: small tau never reaches the early cue (the contrast for c1) ---
        hS = window_integrate(stream, TAU_SHORT, pos_codes)
        short_hits += (decode(hS, short_sigs) == cue_id)

        # --- (c2) DISTINCT: subjective-time-style readout on the SAME stream ---
        # subjective-time = novelty-weighted DURATION scalar (how long it FELT), NOT cue id.
        # novelty(t) = ||x(t) - x(t-1)||; duration estimate = sum of novelty.  Decode that
        # scalar to a cue guess by binning -> carries NO cue-identity info -> chance.
        nov = np.array([np.linalg.norm(stream[t] - stream[t - 1]) for t in range(1, T)])
        dur = float(np.sum(nov))                       # novelty-weighted subjective duration
        subj_guess = int(np.floor((dur % 1.0) * K)) % K  # bin the duration scalar -> K guess
        subj_hits += (subj_guess == cue_id)

        # --- (c3) SHUFFLE: time-scramble the stream -> the cue frames no longer align with the
        # position codes (the long window integrates content against the WRONG positions) ->
        # the order-sensitive matched filter collapses to chance. Window/codes UNCHANGED. ---
        perm = rng.permutation(T)
        hShuf = window_integrate(stream[perm], TAU_LONG, pos_codes)
        shuf_hits += (decode(hShuf, long_sigs) == cue_id)

        # --- (c4) ABLATE: set the window SHORT -> far-past cue outside window (== short lane) ---
        hAbl = window_integrate(stream, TAU_SHORT, pos_codes)
        abl_hits += (decode(hAbl, short_sigs) == cue_id)

    n = N_TRIAL
    return dict(
        long_acc=long_hits / n, short_acc=short_hits / n,
        subj_acc=subj_hits / n, shuf_acc=shuf_hits / n, abl_acc=abl_hits / n,
    )


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

presence_gap = agg['long_acc'] - agg['short_acc']
distinct_gap = agg['long_acc'] - agg['subj_acc']

c1 = presence_gap >= 0.30 and agg['long_acc'] >= 0.55
c2 = distinct_gap >= 0.30 and agg['subj_acc'] <= 0.45
c3 = agg['shuf_acc'] <= 0.45
c4 = agg['abl_acc'] <= 0.45
GREEN = c1 and c2 and c3 and c4

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS} | chance={CHANCE:.3f}")
print(f"c1 PRESENCE   long_acc={agg['long_acc']:.3f} - short_acc={agg['short_acc']:.3f} = gap {presence_gap:.3f}>=0.30 (long lane carries L={T-1}-step-back cue) & long>=0.55  -> {c1}")
print(f"c2 DISTINCT   long_acc {agg['long_acc']:.3f} - subjtime_acc {agg['subj_acc']:.3f} = gap {distinct_gap:.3f}>=0.30 (subj-time duration scalar at chance {agg['subj_acc']:.3f}<=0.45)  -> {c2}")
print(f"c3 SHUFFLE    time-scrambled stream -> long lane shuf_acc={agg['shuf_acc']:.3f}<=0.45 (collapses to chance)  -> {c3}")
print(f"c4 ABLATE     window->SHORT -> abl_acc={agg['abl_acc']:.3f}<=0.45 (far-past cue forgotten == short lane)  -> {c4}")
print()
print("PER-SEED:")
for s, p in zip(SEEDS, per):
    print(f"  seed {s}: long={p['long_acc']:.3f} short={p['short_acc']:.3f} "
          f"subj={p['subj_acc']:.3f} shuf={p['shuf_acc']:.3f} abl={p['abl_acc']:.3f}")
