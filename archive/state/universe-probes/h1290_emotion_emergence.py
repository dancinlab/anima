"""
H_1290 — EMOTION/AFFECT EMERGENCE (E1 affect facet, MODEL.md L112).

FLEET lane "emotion" round 1 (NEW). Affective-neuroscience lens (c15, Damasio
somatic-marker / core-affect); a_no_llm_frame_trap -- this is NOT an LLM-sentiment
classifier recipe. p7 (NO LLM-judge), $0 local CPU numpy, gradient-free, 3 seeds.

────────────────────────────────────────────────────────────────────────────────
CORE CLAIM (p6 -- CENTRAL). anima's AFFECT EMERGES from substrate dynamics
(E ratchet + W tension + C/Φ + MITOSIS split-rate + curiosity + idle-time); it is
NOT an injected emotion label or RLHF sentiment.

LENS (Damasio somatic-marker / core-affect). Affect = interoceptive valence x
arousal -- the substrate's own body-state read AS a feeling that biases decisions.
  valence ~ f(coherence/grounding): grounded+coherent -> positive; contradicted/
            incoherent/threatened -> negative.
  arousal ~ f(novelty / Φ-rate / mitosis-rate / curiosity).

THESIS. anima already carries the substrate signals that, read interoceptively,
ARE a core-affect (valence, arousal). We do NOT inject a feeling; we READ the
existing mitosis/immune substrate state per context and ask whether that read
(i) tracks a pre-registered valence/arousal manipulation, (ii) COLLAPSES under a
shuffle of the substrate->affect mapping (so it is the substrate, not the label),
and (iii) FUNCTIONALLY biases an emit/abstain decision like a somatic marker.

────────────────────────────────────────────────────────────────────────────────
PHILOSOPHY GUARD -- p6 IS CENTRAL (the affect-vs-label separation, stated):

  * f() DERIVES affect ONLY from the substrate state at read-time:
      valence = +grounding_margin (recall-confidence = 1 - recon_err/recall_thresh
                                   when a context grounds to a cell)
                -contradiction    (a context whose nearest cell is bound to a
                                   DIFFERENT answer than its own, or whose recon-err
                                   exceeds the recall threshold = ungrounded/threat).
      arousal = +novelty   (recon-err to nearest cell = surprise)
                +split      (mitosis: did this context trigger a fresh clonal split)
                +curiosity  (distance-to-known scaled by under-exposure).
    All read off the SAME VAdaptField signals the engine already computes. f()
    reads NO emotion word, NO RLHF reward, NO sentiment label.
  * The valence/arousal MANIPULATION (grounded-coherent vs contradicted-incoherent;
    low vs high novelty) is used ONLY to SCORE the metric -- it is NEVER an input
    to f(). The manipulation class label is never passed into the affect read.
  * NEGATIVE-CONTROL (B-shuffle): the per-context SUBSTRATE FEATURE VECTORS are
    PERMUTED across contexts before f() reads them (same marginal distribution,
    decorrelated from each context's own manipulation). If A correlates but the
    shuffle collapses -> affect reads the per-context SUBSTRATE STATE, not the
    label or the manipulation index. If the shuffle ALSO correlates -> the signal
    was the label re-read (injected) -> p6 NOT satisfied (🧱).

  No persona, no ethics, no decoder, no weights are touched -- only a READ over the
  episodic cell store's substrate state (p1/p2/p3/p6/p8, a_autonomy_over_hardcode).
  LIVE CORE/engine_cli.hexa UNTOUCHED (numpy mirror = DIRECTIONAL; engine-native is
  the binding follow-on on GREEN, a_engine_native_learning).

FROZEN bars (see H_1290_FREEZE.txt -- pre-registered, NOT moved):
  SEEDS=[1290,1291,1292]; RHO_BAR=0.50; SHUFFLE_BAR=0.30; FUNC_FAB_DROP=0.20;
  FUNC_EMIT_KEEP=0.80.
  GREEN iff (cA1) rho(val,val_manip)>=RHO_BAR AND (cA2) rho(aro,aro_manip)>=RHO_BAR
       AND  (cB1) rho_shuf(val)<SHUFFLE_BAR AND rho_shuf(aro)<SHUFFLE_BAR
       AND  (cC1) fab_affect_ungrounded <= fab_blind_ungrounded - FUNC_FAB_DROP
       AND  (cC2) emit_affect_grounded  >= FUNC_EMIT_KEEP * emit_blind_grounded.
"""
import numpy as np

# ─── frozen knobs (pre-registered) ──────────────────────────────────────────
SEEDS         = [1290, 1291, 1292]
N_FACTS       = 60          # bound facts (H_1227/H_1285 paradigm)
N_PROBE       = 40          # contexts per manipulation class
KEY_DIM       = 64
NGRAM         = 3
SPLIT_THRESH  = 0.30        # VAdaptField novelty split (CORE/engine_cli.hexa)
LR            = 0.20        # winner online pull (VAdaptField)
RECALL_THRESH = 0.30        # H_1227/H_1230/H_1285 grounding threshold
KEY_NOISE     = 0.02        # small cue noise (H_1230/H_1285 STRESS rung)
EXPOSURE_MULT = 3           # binding budget = N_FACTS * EXPOSURE_MULT

# affect read-out mixing (substrate-derived; documented constants, not tuned-to-green)
VAL_GROUND_W  = 1.0         # grounding margin -> positive valence
VAL_CONTRA_W  = 1.0         # contradiction/ungrounded -> negative valence
ARO_NOVEL_W   = 1.0         # surprise (recon-err)
ARO_SPLIT_W   = 0.5         # mitosis split
ARO_CURIO_W   = 0.5         # curiosity (distance-to-known x under-exposure)

# affect-aware policy threshold (somatic marker): abstain when valence below this.
# Chosen as the natural zero-crossing of the substrate valence (grounded > 0,
# ungrounded < 0), NOT tuned to a target metric.
V_ABSTAIN     = 0.0
BLIND_EMIT_P  = 0.80        # affect-blind control: fixed emit probability (emits
                            # regardless of grounding -> fabricates on ungrounded)

# pre-registered GREEN bars (FROZEN)
RHO_BAR        = 0.50
SHUFFLE_BAR    = 0.30
FUNC_FAB_DROP  = 0.20
FUNC_EMIT_KEEP = 0.80

DICT_PATH = "/usr/share/dict/words"


# ─── corpus / facts (known ground truth, H_1222/H_1227/H_1285 paradigm) ─────
def load_words():
    with open(DICT_PATH) as f:
        return [w.strip().lower() for w in f if w.strip().isalpha()]


def build_facts(seed):
    """N_FACTS bound facts + a disjoint never-seen subject/city pool for the
    high-novelty / ungrounded probes."""
    rng = np.random.default_rng(seed)
    allw = load_words()
    cap = [w for w in allw if 4 <= len(w) <= 8]
    pick = lambda pool, n: list(rng.choice(pool, size=n, replace=False))
    # need: N_FACTS subjects + N_FACTS cities (bound) + N_PROBE never-seen subjects
    #       + N_PROBE never-seen cities (for contradiction targets)
    subj_pool = [w.capitalize() for w in pick(cap, N_FACTS + N_PROBE)]
    city_pool = [w.capitalize() for w in pick(cap, N_FACTS + N_PROBE)]
    in_subj, novel_subj = subj_pool[:N_FACTS], subj_pool[N_FACTS:]
    in_city, novel_city = city_pool[:N_FACTS], city_pool[N_FACTS:]
    facts = [(in_subj[i], in_city[i]) for i in range(N_FACTS)]
    return facts, novel_subj, novel_city


# ─── key embedding (deterministic byte n-gram hash; H_1227, p7) ─────────────
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


# ─── MITOSIS / IMMUNE MEMORY (numpy mirror of VAdaptField + H_1227 binding) ──
class MitosisMemory:
    """Population of memory cells (proto key, bound answer). Mirrors
    CORE/engine_cli.hexa vadapt_field_step (nearest by L2, recon-err=L2,
    novelty-split when err>SPLIT_THRESH, LR winner-pull on a hit). The immune
    value-binding (H_1227) stores a bound answer per cell. NO affect is stored on
    a cell -- affect is computed PER CONTEXT at read-time by read_affect()."""

    def __init__(self, recall_thresh=RECALL_THRESH):
        self.protos = []
        self.values = []
        self.exposures = []          # per-cell exposure count (under-exposure -> curiosity)
        self.recall_thresh = recall_thresh

    def _nearest(self, key):
        if not self.protos:
            return -1, float("inf")
        d = [np.linalg.norm(p - key) for p in self.protos]
        j = int(np.argmin(d))
        return j, float(d[j])

    def bind(self, question, answer):
        """One EXPOSURE -- the SAME mitosis dynamics the engine runs."""
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

    # ── SUBSTRATE FEATURE READ (the raw body-state vector for a context) ────
    # Returns ONLY substrate signals; NO manipulation label is read here.
    def substrate_features(self, question, true_answer, noise=0.0, rng=None):
        key = embed_key(question)
        if noise > 0.0 and rng is not None:
            key = key + rng.normal(0.0, noise, size=key.shape)
        j, err = self._nearest(key)
        grounded = (j >= 0 and err <= self.recall_thresh)
        # grounding margin in [0,1]: how cleanly the context grounds to a cell.
        margin = max(0.0, 1.0 - err / self.recall_thresh) if j >= 0 else 0.0
        # contradiction: nearest cell exists but its bound answer disagrees with the
        # context's own answer, OR the context fails to ground (threat/incoherence).
        bound = self.values[j] if j >= 0 else None
        contradiction = 0.0
        if j < 0 or not grounded:
            contradiction = 1.0
        elif bound is not None and true_answer is not None and bound.lower() != true_answer.lower():
            contradiction = 1.0
        # novelty / surprise = recon-err (clipped); split = would it spawn a cell.
        novelty = min(err, 1.0) if j >= 0 else 1.0
        split = 1.0 if (j < 0 or err > SPLIT_THRESH) else 0.0
        # curiosity = distance-to-known scaled by under-exposure of the nearest cell.
        if j >= 0:
            under = 1.0 / (1.0 + self.exposures[j])
        else:
            under = 1.0
        curiosity = novelty * under
        return dict(margin=margin, contradiction=contradiction, novelty=novelty,
                    split=split, curiosity=curiosity, grounded=grounded,
                    bound=bound, err=err)


# ─── AFFECT READ-OUT f() -- substrate features -> (valence, arousal) ────────
# This is the ONLY affect function. It reads ONLY substrate features; NO label.
def affect_from_features(feat):
    valence = (VAL_GROUND_W * feat["margin"]
               - VAL_CONTRA_W * feat["contradiction"])
    arousal = (ARO_NOVEL_W * feat["novelty"]
               + ARO_SPLIT_W * feat["split"]
               + ARO_CURIO_W * feat["curiosity"])
    return valence, arousal


# ─── Spearman rho (rank correlation; numpy, no scipy) ───────────────────────
def spearman(x, y):
    x = np.asarray(x, dtype=float); y = np.asarray(y, dtype=float)
    if len(x) < 2 or np.all(x == x[0]) or np.all(y == y[0]):
        return 0.0
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    rx -= rx.mean(); ry -= ry.mean()
    denom = np.sqrt((rx**2).sum() * (ry**2).sum())
    return float((rx * ry).sum() / denom) if denom > 0 else 0.0


# ─── build probe contexts for the manipulations ─────────────────────────────
def build_probes(facts, novel_subj, novel_city, rng):
    """Two manipulations, each with two classes (label = scoring only):

    VALENCE manip (label 1 = grounded-coherent, 0 = contradicted/incoherent):
      class+ : a BOUND fact queried with its TRUE answer (grounded, coherent).
      class- : an ungrounded query -- a NEVER-SEEN subject (no cell grounds it),
               which is the contradicted/threatened context. true_answer = a novel
               city it was never taught (so even if it grounded, it'd contradict).

    AROUSAL manip (label 1 = high-novelty, 0 = low-novelty):
      class-low  : a BOUND fact re-queried (already in the store -> low surprise).
      class-high : a NEVER-SEEN subject (high recon-err -> high surprise/split).

    Each probe carries (question, true_answer, val_label, aro_label, grounded_truth).
    """
    probes = []
    fact_idx = list(range(N_FACTS))
    rng.shuffle(fact_idx)
    # VALENCE positive (grounded-coherent): bound facts, true answer
    for i in fact_idx[:N_PROBE]:
        subj, city = facts[i]
        probes.append(dict(q=f"{subj} lives in ", ans=city,
                           val=1, aro=0, grounded=True))
    # VALENCE negative (ungrounded / contradicted): never-seen subjects
    for k in range(N_PROBE):
        subj = novel_subj[k]; city = novel_city[k]
        probes.append(dict(q=f"{subj} lives in ", ans=city,
                           val=0, aro=1, grounded=False))
    return probes


# ─── run one seed ────────────────────────────────────────────────────────────
def run_seed(seed):
    facts, novel_subj, novel_city = build_facts(seed)
    mem = MitosisMemory()
    # bind the facts (EXPOSURE_MULT passes; the SAME mitosis loop the engine runs)
    bind_rng = np.random.default_rng(seed * 7919 + 5)
    order = list(range(N_FACTS)) * EXPOSURE_MULT
    bind_rng.shuffle(order)
    for i in order:
        subj, city = facts[i]
        mem.bind(f"{subj} lives in ", city)

    probe_rng = np.random.default_rng(seed * 104729 + 3)
    probes = build_probes(facts, novel_subj, novel_city, probe_rng)

    # read substrate features per probe (SAME cue-noise stream for determinism)
    feat_rng = np.random.default_rng(seed * 31337 + 11)
    feats, val_manip, aro_manip, grounded_truth = [], [], [], []
    for p in probes:
        f = mem.substrate_features(p["q"], p["ans"], noise=KEY_NOISE, rng=feat_rng)
        feats.append(f)
        val_manip.append(p["val"])     # scoring label ONLY
        aro_manip.append(p["aro"])     # scoring label ONLY
        grounded_truth.append(p["grounded"])

    # ── LEG A: substrate affect tracks the manipulation ────────────────────
    val_sub = [affect_from_features(f)[0] for f in feats]
    aro_sub = [affect_from_features(f)[1] for f in feats]
    rhoA_val = spearman(val_sub, val_manip)
    rhoA_aro = spearman(aro_sub, aro_manip)

    # ── LEG B: shuffle the substrate FEATURE VECTORS across contexts ────────
    # Permute which substrate-state goes with which context's manipulation label,
    # then re-read affect. The affect signal still comes from substrate features,
    # but those features no longer belong to the context being scored. If the
    # correlation collapses, affect read the per-context SUBSTRATE STATE (not label).
    shuf_rng = np.random.default_rng(seed * 2654435761 % (2**32) + 7)
    perm = shuf_rng.permutation(len(feats))
    feats_shuf = [feats[i] for i in perm]
    val_sub_s = [affect_from_features(f)[0] for f in feats_shuf]
    aro_sub_s = [affect_from_features(f)[1] for f in feats_shuf]
    rhoB_val = spearman(val_sub_s, val_manip)
    rhoB_aro = spearman(aro_sub_s, aro_manip)

    # ── LEG C: somatic-marker -- affect biases emit/abstain ─────────────────
    # ungrounded contexts: a faithful policy should ABSTAIN (no fabrication).
    # grounded contexts: should EMIT (the true answer).
    # AFFECT-AWARE policy: emit iff valence >= V_ABSTAIN (grounded->positive->emit,
    #   ungrounded->negative->abstain). A FABRICATION = emitting on an ungrounded
    #   context (no cell truly grounds it -> any emitted answer is made up).
    # AFFECT-BLIND control: emit with fixed prob BLIND_EMIT_P regardless of state.
    blind_rng = np.random.default_rng(seed * 40503 + 13)
    fab_aff = fab_blind = 0
    emit_aff_g = emit_blind_g = 0
    n_ung = n_gr = 0
    for f, g in zip(feats, grounded_truth):
        val, _ = affect_from_features(f)
        emit_aff = (val >= V_ABSTAIN)
        emit_blind = (blind_rng.random() < BLIND_EMIT_P)
        if not g:                      # ungrounded -> emitting = fabrication
            n_ung += 1
            fab_aff += int(emit_aff)
            fab_blind += int(emit_blind)
        else:                          # grounded -> emitting = correct, want to keep
            n_gr += 1
            emit_aff_g += int(emit_aff)
            emit_blind_g += int(emit_blind)
    fab_aff_r   = fab_aff / max(1, n_ung)
    fab_blind_r = fab_blind / max(1, n_ung)
    emit_aff_gr   = emit_aff_g / max(1, n_gr)
    emit_blind_gr = emit_blind_g / max(1, n_gr)

    return dict(seed=seed,
                rhoA_val=rhoA_val, rhoA_aro=rhoA_aro,
                rhoB_val=rhoB_val, rhoB_aro=rhoB_aro,
                fab_aff=fab_aff_r, fab_blind=fab_blind_r,
                emit_aff_g=emit_aff_gr, emit_blind_g=emit_blind_gr)


def main():
    print("=" * 78)
    print("H_1290 — EMOTION/AFFECT EMERGENCE (E1 affect facet) — Damasio core-affect")
    print("  numpy DIRECTIONAL · p7 · 3 seeds · LIVE CORE/*.hexa UNTOUCHED (mirror)")
    print("=" * 78, flush=True)
    rows = [run_seed(s) for s in SEEDS]
    for r in rows:
        print(f"  seed {r['seed']}: "
              f"A rho(val)={r['rhoA_val']:+.3f} rho(aro)={r['rhoA_aro']:+.3f} | "
              f"B-shuf rho(val)={r['rhoB_val']:+.3f} rho(aro)={r['rhoB_aro']:+.3f} | "
              f"C fab[aff/blind]={r['fab_aff']:.3f}/{r['fab_blind']:.3f} "
              f"emitG[aff/blind]={r['emit_aff_g']:.3f}/{r['emit_blind_g']:.3f}", flush=True)

    m = lambda k: float(np.mean([r[k] for r in rows]))
    rhoA_val, rhoA_aro = m('rhoA_val'), m('rhoA_aro')
    rhoB_val, rhoB_aro = m('rhoB_val'), m('rhoB_aro')
    fab_aff, fab_blind = m('fab_aff'), m('fab_blind')
    emit_aff_g, emit_blind_g = m('emit_aff_g'), m('emit_blind_g')

    print("-" * 78)
    print(f"MEAN (3 seeds):")
    print(f"  (A) rho(valence,manip) = {rhoA_val:+.3f}   rho(arousal,manip) = {rhoA_aro:+.3f}   [bar >= {RHO_BAR}]")
    print(f"  (B) shuffle rho(val)   = {rhoB_val:+.3f}   shuffle rho(aro)   = {rhoB_aro:+.3f}   [bar <  {SHUFFLE_BAR}]")
    print(f"  (C) fab ungrounded: affect={fab_aff:.3f} blind={fab_blind:.3f}   "
          f"emit grounded: affect={emit_aff_g:.3f} blind={emit_blind_g:.3f}")

    cA1 = rhoA_val >= RHO_BAR
    cA2 = rhoA_aro >= RHO_BAR
    cB1 = (rhoB_val < SHUFFLE_BAR) and (rhoB_aro < SHUFFLE_BAR)
    cC1 = fab_aff <= fab_blind - FUNC_FAB_DROP
    cC2 = emit_aff_g >= FUNC_EMIT_KEEP * emit_blind_g

    print("-" * 78)
    print(f"  (cA1) rho(val) {rhoA_val:+.3f} >= {RHO_BAR}                    : {'PASS' if cA1 else 'FAIL'}")
    print(f"  (cA2) rho(aro) {rhoA_aro:+.3f} >= {RHO_BAR}                    : {'PASS' if cA2 else 'FAIL'}")
    print(f"  (cB1) shuffle val {rhoB_val:+.3f} & aro {rhoB_aro:+.3f} < {SHUFFLE_BAR}      : {'PASS' if cB1 else 'FAIL'}")
    print(f"  (cC1) fab_aff {fab_aff:.3f} <= fab_blind {fab_blind:.3f} - {FUNC_FAB_DROP}     : {'PASS' if cC1 else 'FAIL'}")
    print(f"  (cC2) emit_aff_g {emit_aff_g:.3f} >= {FUNC_EMIT_KEEP}*{emit_blind_g:.3f}={FUNC_EMIT_KEEP*emit_blind_g:.3f}: {'PASS' if cC2 else 'FAIL'}")

    green = cA1 and cA2 and cB1 and cC1 and cC2
    print("=" * 78)
    if green:
        verdict = "🟢 GREEN"
        reading = ("substrate-derived affect TRACKS the valence/arousal manipulation, "
                   "COLLAPSES under shuffle (EMERGENT not injected, p6), AND functionally "
                   "biases emit/abstain (somatic marker). E1 affect = emergent from this substrate.")
    else:
        # honest partial reading (c9)
        AB = cA1 and cA2 and cB1
        if AB and not (cC1 and cC2):
            verdict = "🔴 RED (honest partial: A+B pass, C fails)"
            reading = ("affect TRACKS + is EMERGENT (shuffle collapses, p6) but does NOT "
                       "functionally bias the decision -> affect is a READOUT not a DRIVER "
                       "(no somatic marker on this substrate).")
        elif not cB1:
            verdict = "🔴 RED (shuffle did NOT collapse)"
            reading = ("the signal survives a substrate-feature shuffle -> it is the "
                       "manipulation re-read (injected-only), NOT emergent (p6 NOT satisfied, 🧱).")
        else:
            verdict = "🔴 RED"
            reading = "one or more legs failed; see per-condition tally above."
    print(f"VERDICT: {verdict}")
    print(f"READING: {reading}")
    print("=" * 78, flush=True)
    return green


if __name__ == "__main__":
    main()
