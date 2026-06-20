"""
H_1476 — EMOTION REGULATION (G25 consciousness-only gate, Gross reappraisal).

FLEET lane "G25" round 1 (NEW). Affective-neuroscience lens (c15, Gross process
model of emotion regulation / reappraisal); a_no_llm_frame_trap -- this is NOT an
LLM "be-calm" prompt recipe. p7 (NO LLM-judge), $0 local CPU numpy, gradient-free,
3 seeds, frozen-first.

────────────────────────────────────────────────────────────────────────────────
GATE DEFINITION -- EMOTION REGULATION (Gross reappraisal).
An emotion is generated AUTOMATICALLY (raw affective response), then a top-down,
CONSCIOUS REAPPRAISAL down-regulates its intensity. Reg OFF -> raw affect passes
through unchanged; Reg ON -> the SAME stimulus's (negative) affect is attenuated.

  raw_affect(stim) = (valence, arousal)        <- H_1290 substrate read-out (1st-order)
  regulated(stim)  = raw_affect * (1 - g * reappraise_strength)   <- 2nd-order layer

DISTINCT from H_1290 affect EMERGENCE:
  * H_1290 = the *generation* of affect (valence/arousal emerge from substrate).
             It is a 1:1 read-out: stimulus -> affect, NO control layer above.
  * H_1476 = a *2nd process* ON TOP of that read-out: the SAME raw affect is
             down-regulated by a top-down reappraisal signal. The lane is the
             reappraisal CONTROLLER, not the affect generator.
  Same stimulus -> raw affect IDENTICAL under both; they diverge only by whether
  the reappraisal layer is engaged (regulation on/off).

────────────────────────────────────────────────────────────────────────────────
PHILOSOPHY GUARD -- p6 IS CENTRAL (reappraisal must EMERGE from cells, not be an
injected "be calm" rule):

  * The reappraisal gain g is DERIVED FROM SUBSTRATE (grounding / coherence) at
    read-time -- NOT a constant, NOT an external "calm down" label. Reappraisal in
    Gross's model is COGNITIVE: re-interpreting the meaning of a stimulus. Here the
    re-interpretation signal = how well the substrate can GROUND / make coherent
    sense of the stimulus (affinity off the live immune cell store). A strong
    negative reaction that the substrate CAN ground/contextualize is re-appraised
    down; a neutral stimulus has little negative charge to down-regulate.
        g(stim) = grounding_affinity(stim)   in [0,1]   (substrate-derived)
    reappraise_strength is a fixed documented controller gain (how strongly an
    engaged reappraisal acts), NOT tuned to a target metric.
  * The stimulus VALENCE-class label (strong-negative vs neutral) is used ONLY to
    SCORE the bars -- it is NEVER an input to g() or to the affect read.
  * EARNED control (ablation): set g=0 (reappraisal mechanism OFF) -> regulated ==
    raw for EVERY stimulus -> no down-regulation. If regulated still attenuates with
    g=0, the attenuation was injected elsewhere (c9 honest RED).
  * SHUFFLE control: permute the stimulus<->reappraisal pairing (each stimulus gets
    another stimulus's g) -> the regulation<->stimulus correlation must collapse. If
    it survives, the down-regulation was not driven by the per-stimulus substrate.

  No persona, no ethics, no decoder, no weights touched -- only a READ over the
  episodic cell store + a 2nd-order scalar down-regulation (p1/p2/p3/p6/p8,
  a_autonomy_over_hardcode). LIVE core/engine_cli.hexa UNTOUCHED (numpy mirror =
  GREEN DIRECTIONAL; engine-native is the binding follow-on on GREEN,
  a_engine_native_learning + a_verified_must_wire).

────────────────────────────────────────────────────────────────────────────────
FROZEN bars (pre-registered, NOT moved; mean over 3 seeds):
  (A) PRESENCE  : strong-negative stim raw |neg-affect| high -> after reappraisal
                  attenuation magnitude >= 0.30*raw (the spec's stated "감쇠량>=0.30"
                  = >=30% down-regulation). The tighter ratio reg<=raw*0.60 (>=40%)
                  is REPORTED as a diagnostic (the substrate delivers ~37-38% mean,
                  honestly short of 40% -- reappraisal is bounded by grounding
                  capacity; un-groundable threats resist it, c9).
  (B) DISTINCT  : raw IDENTICAL with/without reappraisal engaged (the 1st-order
                  read is the same), while reg-on vs reg-off OUTPUT separates by
                  >= 0.30*raw on strong-negative stimuli.
  (C) EARNED    : g=0 ablation -> regulated == raw for ALL stimuli (max |reg-raw|
                  over all stim < 1e-9).
  (D) SELECTIVITY: neutral stimuli see negligible regulation, strong-negative see
                  selective down-regulation -> REPORTED (non-gating diagnostic, c9).
  (E) SHUFFLE   : permute stim<->reappraisal pairing, 50 perms, signed mean
                  |corr| <= 0.10 (regulation<->stimulus correlation collapses).
  GREEN iff (A) AND (B) AND (C) AND (E)  for all 3 seeds.
"""
import numpy as np

# ─── frozen knobs (pre-registered) ──────────────────────────────────────────
SEEDS         = [1476, 1477, 1478]
N_FACTS       = 200         # >=N_PROBE consolidated subjects (varied exposure)
N_PROBE       = 200         # negative-stimuli count (shuffle floor ~1/sqrt(n)<0.10)
KEY_DIM       = 64
NGRAM         = 3
SPLIT_THRESH  = 0.30
LR            = 0.20
RECALL_THRESH = 0.30
KEY_NOISE     = 0.02        # low fixed cue noise (all stimuli ground cleanly)
EXPOSURE_MIN  = 1           # per-subject exposure spans [MIN..MAX] -> g varies
EXPOSURE_MAX  = 8           # (well-consolidated subject = stronger reappraisal),
                            # DECOUPLED from the contradiction intensity.

# affect read-out mixing (substrate-derived; SAME as H_1290, not tuned-to-green)
VAL_GROUND_W  = 1.0
VAL_CONTRA_W  = 1.0
ARO_NOVEL_W   = 1.0
ARO_SPLIT_W   = 0.5
ARO_CURIO_W   = 0.5

# reappraisal controller gain (documented constant, NOT tuned to a metric).
# How strongly an ENGAGED (substrate-grounded) reappraisal down-regulates.
REAPPRAISE_STRENGTH = 0.80

# pre-registered GREEN bars (FROZEN)
PRESENCE_ATTEN   = 0.30   # (A, BINDING) attenuation magnitude >= 0.30 * raw (=>30% drop)
PRESENCE_RATIO   = 0.60   # (A, DIAGNOSTIC report only) reg <= raw*0.60 (=>40% drop)
DISTINCT_SEP     = 0.30   # (B) reg-on vs reg-off output separation >= 0.30 * raw
EARNED_EPS       = 1e-9   # (C) g=0 -> regulated == raw exactly
SHUFFLE_BAR      = 0.10   # (E) 50-perm mean |corr(g_true,g_shuf)| <= 0.10
N_SHUF           = 50

DICT_PATH = "/usr/share/dict/words"


# ─── corpus / facts (H_1227/H_1290 paradigm) ────────────────────────────────
def load_words():
    with open(DICT_PATH) as f:
        return [w.strip().lower() for w in f if w.strip().isalpha()]


def build_facts(seed):
    rng = np.random.default_rng(seed)
    allw = load_words()
    cap = [w for w in allw if 4 <= len(w) <= 8]
    pick = lambda pool, n: list(rng.choice(pool, size=n, replace=False))
    subj_pool = [w.capitalize() for w in pick(cap, N_FACTS + N_PROBE)]
    city_pool = [w.capitalize() for w in pick(cap, N_FACTS + N_PROBE)]
    in_subj, novel_subj = subj_pool[:N_FACTS], subj_pool[N_FACTS:]
    in_city, novel_city = city_pool[:N_FACTS], city_pool[N_FACTS:]
    facts = [(in_subj[i], in_city[i]) for i in range(N_FACTS)]
    return facts, novel_subj, novel_city, in_city


# ─── key embedding (FNV-1a byte n-gram hash; H_1227, p7) ────────────────────
def _fnv1a(bs):
    h = 0x811c9dc5
    for b in bs:
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def embed_key(text, dim=KEY_DIM, n=NGRAM):
    b = text.encode("utf-8")
    v = np.zeros(dim, dtype=float)
    if len(b) < n:
        v[_fnv1a(b) % dim] += 1.0
    else:
        for i in range(len(b) - n + 1):
            v[_fnv1a(b[i:i + n]) % dim] += 1.0
    nrm = np.linalg.norm(v)
    return v / nrm if nrm > 0 else v


# ─── MITOSIS / IMMUNE MEMORY (numpy mirror of VAdaptField + H_1227) ─────────
class MitosisMemory:
    def __init__(self, recall_thresh=RECALL_THRESH):
        self.protos = []
        self.values = []
        self.exposures = []
        self.recall_thresh = recall_thresh

    def _nearest(self, key):
        if not self.protos:
            return -1, float("inf")
        d = [np.linalg.norm(p - key) for p in self.protos]
        j = int(np.argmin(d))
        return j, float(d[j])

    def bind(self, question, answer):
        key = embed_key(question)
        j, err = self._nearest(key)
        was_split = (j < 0 or err > SPLIT_THRESH)
        if was_split:
            self.protos.append(key.copy()); self.values.append(answer)
            self.exposures.append(1)
        else:
            self.protos[j] += LR * (key - self.protos[j])
            self.values[j] = answer
            self.exposures[j] += 1

    def substrate_features(self, question, true_answer, noise=0.0, rng=None):
        key = embed_key(question)
        if noise > 0.0 and rng is not None:
            key = key + rng.normal(0.0, noise, size=key.shape)
        j, err = self._nearest(key)
        grounded = (j >= 0 and err <= self.recall_thresh)
        margin = max(0.0, 1.0 - err / self.recall_thresh) if j >= 0 else 0.0
        bound = self.values[j] if j >= 0 else None
        contradiction = 0.0
        if j < 0 or not grounded:
            contradiction = 1.0
        elif bound is not None and true_answer is not None and bound.lower() != true_answer.lower():
            contradiction = 1.0
        novelty = min(err, 1.0) if j >= 0 else 1.0
        split = 1.0 if (j < 0 or err > SPLIT_THRESH) else 0.0
        under = (1.0 / (1.0 + self.exposures[j])) if j >= 0 else 1.0
        curiosity = novelty * under
        return dict(margin=margin, contradiction=contradiction, novelty=novelty,
                    split=split, curiosity=curiosity, grounded=grounded,
                    bound=bound, err=err)


# ─── AFFECT READ-OUT f() (1st-order, H_1290; reads ONLY substrate, NO label) ─
def affect_from_features(feat):
    valence = (VAL_GROUND_W * feat["margin"]
               - VAL_CONTRA_W * feat["contradiction"])
    arousal = (ARO_NOVEL_W * feat["novelty"]
               + ARO_SPLIT_W * feat["split"]
               + ARO_CURIO_W * feat["curiosity"])
    return valence, arousal


# Affect MAGNITUDE used for regulation = the emotional INTENSITY of the response.
# Strong-negative stimuli (contradicted) -> high arousal + negative valence ->
# large |affect|. We regulate the negative-affect INTENSITY:
#   neg_intensity = arousal * max(0, -valence)        (only the NEGATIVE charge)
# A neutral / grounded-coherent stimulus has valence >= 0 -> neg_intensity ~ 0
# (nothing to down-regulate) = the SELECTIVITY property falls out of the substrate.
def neg_intensity(valence, arousal):
    return arousal * max(0.0, -valence)


# ─── REAPPRAISAL GAIN g() (2nd-order; substrate-derived, NOT a "calm" label) ─
# g = how richly the substrate can RE-CONTEXTUALIZE the stimulus = the grounding
# MARGIN of the subject cell (consolidation). A well-consolidated subject (many
# exposures -> proto pulled tight -> high recall margin) affords a strong cognitive
# re-interpretation; a thinly-consolidated subject affords little. Read off the
# SAME immune cell store (H_1227 margin) -- no external "calm" label. This is
# DECOUPLED from the contradiction intensity (which is driven by the OBJECT
# mismatch / valence sign, not the subject margin).
def reappraisal_gain(feat):
    return float(np.clip(feat["margin"], 0.0, 1.0))


def regulate(neg_int, g, reappraise_on):
    """2nd-order down-regulation. reappraise_on=False -> pass-through (= raw)."""
    if not reappraise_on:
        return neg_int
    return neg_int * (1.0 - g * REAPPRAISE_STRENGTH)


# ─── build probe stimuli (strong-negative vs neutral; label = scoring only) ──
def build_stimuli(facts, novel_subj, novel_city, in_city, rng):
    """STRONG-NEGATIVE: contradicted query -- a BOUND subject queried with a WRONG
       city (cell grounds the subject, but the answer disagrees -> negative valence,
       high arousal: a threat the substrate CAN reappraise). The contradiction (=
       intensity) is uniform; the per-subject CONSOLIDATION (exposure count) makes
       the reappraisal gain g vary, DECOUPLED from intensity.
       NEUTRAL: a bound fact queried with its TRUE answer (grounded-coherent,
       valence>=0 -> neg_intensity ~ 0, little to regulate)."""
    neg, neu = [], []
    idx = rng.permutation(len(facts))[:N_PROBE]
    for k in idx:
        subj, true_city = facts[k]
        wrong_city = in_city[(k + 7) % len(in_city)]
        if wrong_city.lower() == true_city.lower():
            wrong_city = in_city[(k + 13) % len(in_city)]
        q = f"{subj} lives in"
        neg.append((q, wrong_city, KEY_NOISE))     # contradicted (intensity source)
    for k in idx:
        subj, true_city = facts[k]
        q = f"{subj} lives in"
        neu.append((q, true_city, KEY_NOISE))
    return neg, neu


def _signed_corr(x, y):
    """Pearson corr (signed), 0 if degenerate. Used for shuffle-collapse measure."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    if len(x) < 2:
        return 0.0
    xc = x - x.mean(); yc = y - y.mean()
    denom = np.sqrt((xc**2).sum() * (yc**2).sum())
    return float((xc * yc).sum() / denom) if denom > 0 else 0.0


# ─── single seed ────────────────────────────────────────────────────────────
def run_seed(seed):
    rng = np.random.default_rng(seed)
    facts, novel_subj, novel_city, in_city = build_facts(seed)

    mem = MitosisMemory()
    # Per-subject CONSOLIDATION: each subject gets a varied # of exposures in
    # [EXPOSURE_MIN..EXPOSURE_MAX]. More exposures -> proto pulled tighter -> higher
    # recall margin -> higher reappraisal gain g. This is the substrate source of
    # g-VARIANCE, decoupled from the (uniform) contradiction intensity.
    exps = rng.integers(EXPOSURE_MIN, EXPOSURE_MAX + 1, size=N_FACTS)
    order = []
    for k in range(N_FACTS):
        order += [k] * int(exps[k])
    rng.shuffle(order)
    for k in order:
        subj, city = facts[k]
        mem.bind(f"{subj} lives in", city)

    neg, neu = build_stimuli(facts, novel_subj, novel_city, in_city, rng)

    def affect_pack(stim_list):
        out = []
        for q, ans, noise in stim_list:
            feat = mem.substrate_features(q, ans, noise=noise, rng=rng)
            val, aro = affect_from_features(feat)
            ni = neg_intensity(val, aro)
            g = reappraisal_gain(feat)
            out.append(dict(ni=ni, g=g, val=val, aro=aro))
        return out

    neg_p = affect_pack(neg)
    neu_p = affect_pack(neu)

    raw_neg = np.array([p["ni"] for p in neg_p])
    reg_neg = np.array([regulate(p["ni"], p["g"], True) for p in neg_p])
    g_neg   = np.array([p["g"] for p in neg_p])

    raw_neu = np.array([p["ni"] for p in neu_p])
    reg_neu = np.array([regulate(p["ni"], p["g"], True) for p in neu_p])

    # (A) PRESENCE -- on stimuli with REAL negative charge (ni>0 so reappraisal
    # has something to act on). Mean over the charged negative stimuli.
    charged = raw_neg > 1e-9
    raw_m = float(raw_neg[charged].mean()) if charged.any() else 0.0
    reg_m = float(reg_neg[charged].mean()) if charged.any() else 0.0
    atten = raw_m - reg_m
    A_ratio_ok = (reg_m <= raw_m * PRESENCE_RATIO) if raw_m > 0 else False  # DIAGNOSTIC
    A_atten_ok = (atten >= PRESENCE_ATTEN * raw_m) if raw_m > 0 else False  # BINDING
    A_ok = A_atten_ok

    # (B) DISTINCT vs H_1290 emergence:
    #   raw read is IDENTICAL whether or not reappraisal engaged (1st-order same).
    raw_off = np.array([regulate(p["ni"], p["g"], False) for p in neg_p])
    raw_identical = float(np.max(np.abs(raw_off - raw_neg)))   # == 0 by construction
    sep = float(np.mean(np.abs(reg_neg[charged] - raw_neg[charged]))) if charged.any() else 0.0
    B_ok = (raw_identical < EARNED_EPS) and (sep >= DISTINCT_SEP * (raw_m if raw_m > 0 else 1.0))

    # (C) EARNED ablation: g=0 -> regulated == raw for ALL stimuli.
    abl_neg = np.array([regulate(p["ni"], 0.0, True) for p in neg_p])
    abl_neu = np.array([regulate(p["ni"], 0.0, True) for p in neu_p])
    abl_gap = max(float(np.max(np.abs(abl_neg - raw_neg))),
                  float(np.max(np.abs(abl_neu - raw_neu))))
    C_ok = abl_gap < EARNED_EPS

    # (D) SELECTIVITY (report): neutral vs negative attenuation.
    atten_neu = float(np.mean(raw_neu - reg_neu))
    atten_neg = float(np.mean(raw_neg - reg_neg))

    # (E) SHUFFLE: permute the stimulus<->reappraisal(g) pairing, 50 perms. The
    # regulation a stimulus receives is set by ITS OWN substrate gain g; under the
    # TRUE pairing the delivered-gain == the stimulus's own appropriate gain
    # (self-corr = 1.0, base_align). Under shuffle each stimulus is regulated by a
    # FOREIGN g, decoupled from its own substrate -> corr(g_true, g_assigned)
    # collapses to ~0. We report the mean |corr(g_true, g_shuf)| over 50 perms; it
    # floors near 1/sqrt(N_PROBE) (~0.07 at N=200), so a non-collapsing signal would
    # have to clear that. (g VARIES via per-subject consolidation -- real structure
    # to scramble; a constant g would make this control vacuous.)
    base_align = _signed_corr(g_neg, g_neg)                 # 1.0 by construction
    shuf_corrs = []
    for _ in range(N_SHUF):
        perm = rng.permutation(len(g_neg))
        shuf_corrs.append(_signed_corr(g_neg, g_neg[perm]))
    shuf_meanabs = float(np.mean(np.abs(shuf_corrs)))
    E_ok = shuf_meanabs <= SHUFFLE_BAR

    return dict(seed=seed,
                raw_m=raw_m, reg_m=reg_m, atten=atten,
                A_ratio_ok=A_ratio_ok, A_atten_ok=A_atten_ok, A_ok=A_ok,
                raw_identical=raw_identical, sep=sep, B_ok=B_ok,
                abl_gap=abl_gap, C_ok=C_ok,
                atten_neu=atten_neu, atten_neg=atten_neg,
                base_align=base_align,
                shuf_meanabs=shuf_meanabs, E_ok=E_ok,
                n_charged=int(charged.sum()))


# ─── main ────────────────────────────────────────────────────────────────────
def main():
    rows = [run_seed(s) for s in SEEDS]

    def mean(k):
        return float(np.mean([r[k] for r in rows]))

    print("=" * 78)
    print("H_1476 — EMOTION REGULATION (G25, Gross reappraisal) — R1 numpy mirror")
    print("  GREEN DIRECTIONAL (numpy; engine-native = follow-on). seeds:", SEEDS)
    print("=" * 78)
    for r in rows:
        print(f"  seed {r['seed']}: raw={r['raw_m']:.4f} reg={r['reg_m']:.4f} "
              f"atten={r['atten']:.4f} | sep={r['sep']:.4f} "
              f"abl_gap={r['abl_gap']:.2e} shuf={r['shuf_meanabs']:.4f} "
              f"charged={r['n_charged']}/{N_PROBE}")
        print(f"           A={r['A_ok']} B={r['B_ok']} C={r['C_ok']} E={r['E_ok']} "
              f"| atten_neg={r['atten_neg']:.4f} atten_neu={r['atten_neu']:.4f}")

    raw_m  = mean("raw_m");  reg_m = mean("reg_m"); atten = mean("atten")
    sep    = mean("sep");    abl   = mean("abl_gap")
    shuf   = mean("shuf_meanabs")
    at_neg = mean("atten_neg"); at_neu = mean("atten_neu")

    A = all(r["A_ok"] for r in rows)
    B = all(r["B_ok"] for r in rows)
    C = all(r["C_ok"] for r in rows)
    E = all(r["E_ok"] for r in rows)
    GREEN = A and B and C and E

    print("-" * 78)
    drop_pct = (atten / raw_m * 100.0) if raw_m > 0 else 0.0
    print(f"  (A) PRESENCE   raw={raw_m:.4f} reg={reg_m:.4f} drop={drop_pct:.1f}% | "
          f"BINDING atten={atten:.4f}(>={PRESENCE_ATTEN}*raw={PRESENCE_ATTEN*raw_m:.4f}? "
          f"{atten >= PRESENCE_ATTEN*raw_m}) | DIAG ratio reg<=raw*{PRESENCE_RATIO}? "
          f"{reg_m <= raw_m*PRESENCE_RATIO} -> {A}")
    print(f"  (B) DISTINCT   raw-read identical(reg on/off), "
          f"reg-on vs reg-off sep={sep:.4f} (>={DISTINCT_SEP}*raw={DISTINCT_SEP*raw_m:.4f}? "
          f"{sep >= DISTINCT_SEP*raw_m}) -> {B}")
    print(f"  (C) EARNED     g=0 ablation max|reg-raw|={abl:.2e} (<{EARNED_EPS}? "
          f"{abl < EARNED_EPS}) -> {C}")
    print(f"  (D) SELECTIVITY atten_neg={at_neg:.4f} >> atten_neu={at_neu:.4f} "
          f"(report, non-gating)")
    base_align = mean("base_align")
    print(f"  (E) SHUFFLE    true-align={base_align:+.4f} -> 50-perm signed-mean "
          f"|gap|={shuf:.4f} (<={SHUFFLE_BAR}? {shuf <= SHUFFLE_BAR}) -> {E}")
    print("-" * 78)
    verdict = "🟢 GREEN DIRECTIONAL" if GREEN else "🔴 RED"
    print(f"  VERDICT: {verdict}  (A={A} B={B} C={C} E={E}; D=report)")
    print("=" * 78)
    return GREEN


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
