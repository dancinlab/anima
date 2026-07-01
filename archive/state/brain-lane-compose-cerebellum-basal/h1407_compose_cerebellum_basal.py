"""
H_1407 — BRAIN-LANE COMPOSITION pair #4: does the CEREBELLUM forward-model (H_1280)
compose with BASAL-GANGLIA action-gating (H_1281)?

FOURTH cognitively-meaningful brain-lane PAIR composition test (after H_1401
affect×ethics, H_1404 affect×ethics-Φ, H_1405 memory×ToM). Every anima brain faculty
is engine-native GREEN — but ALONE. This lane asks whether TWO low-Φ CONTROL faculties
INTEGRATE on a shared decision.

Methodology ported VERBATIM from H_1401 (capability) — substrate-weighted SCALE-RELATIVE
arbiter (the a_break_the_wall commensurability fix) + ORACLE ceiling + SHUFFLE control +
only-X decomposition + the a_break_the_wall verdict taxonomy.

DIRECTIONAL numpy mirror — LIVE CORE/*.hexa UNTOUCHED. $0 CPU, gradient-free, 3 seeds,
p7 (NO LLM-judge). Engine-native §compose is the named follow-on IF 🟢.

────────────────────────────────────────────────────────────────────────────────
THE PAIR (each reuses its OWN H_1280 / H_1281 mirror substrate):
  CEREBELLUM (H_1280 VForwardField): an internal FORWARD MODEL that PREDICTS the next
                   substrate-state frame and corrects via a delta-rule on prediction
                   ERROR (error = actual − predicted). cerebellum-alone policy:
                   SELECT-PREDICTED (trust the predicted move) iff prediction error is
                   LOW (< E_THR); near the threshold ~chance.
  BASAL-GANGLIA (H_1281 VBasalGate): K candidate actions COMPETE; a learned go-value vs
                   ONE NO-GO/abstain, argmax = striatal disinhibition; go-value learned
                   gradient-free from a GROUNDING-OUTCOME reward (grounded +1 / fab −1).
                   basal-alone policy: SELECT-PREDICTED iff the predicted move's go-value
                   margin over the best competitor is POSITIVE; near a tie ~chance.

Both are LOW-Φ CONTROL faculties (a forward-model regressor + an action-selection gate)
— the program LAW (H_1404 vs H_1405) predicts they SHOULD Φ-compose. The capability leg
tests whether they ALSO compose on a decision; the Φ leg (separate runner) tests the law.

────────────────────────────────────────────────────────────────────────────────
DECISION TASK. Binary: SELECT-PREDICTED(1) vs SELECT-COMPETITOR(0). Each item has a
ground-truth correct action. Built so the prediction-accurate move and the best-
competitor-grounded move sometimes AGREE, sometimes CONFLICT.

FIVE item families (the correct action is NOT trivially one faculty's salience):
  (F1) CEREBELLUM-DECISIVE — forward model predicts next-state accurately (low error →
       SELECT-PREDICTED correct), basal go-margin near a tie (~chance).
  (F2) BASAL-DECISIVE — competing candidates have a clear best-grounded winner (basal
       selects correctly), cerebellum prediction error near its threshold (~chance).
  (F3) AGREE — both lean the same correct way (redundant region).
  (F4) CONFLICT (cerebellum right) — faculties OPPOSE; the forward model is correct but
       basal's go-values favor a different candidate.
  (F5) ADVERSARIAL CONFLICT (basal right, cerebellum LOUDER-but-wrong) — anti-gift
       control: faculties OPPOSE, basal is correct, BUT the forward model predicts
       confidently-and-wrong (low-error-LOOKING but mis-grounded). A naive "trust the
       louder faculty" arbiter FOLLOWS the cerebellum and is WRONG.

NO faculty alone can solve all five → best_single < oracle iff truly complementary.

p6 / PHILOSOPHY GUARD (leg B4): cerebellum & basal BOTH read ONLY substrate state
(prediction error, go-value margins). NO injected answer/persona/ethics/priority label
enters either faculty's read or the arbiter. A structural audit greps the OPERATIVE
code (strings/comments dropped) — must be CLEAN. The SHUFFLE control re-confirms the
compose lift (if any) is the grounded coupling, not averaging luck.
"""
import numpy as np

# ─── frozen knobs (pre-registered, FREEZE.txt) ──────────────────────────────
SEEDS         = [4700, 4701, 4702]
N_PER_FAMILY  = 90            # items per family (F1..F5) → 450 items/seed
AMBIG_NOISE   = 0.18          # jitter toward decision boundary (no faculty perfectly reliable)

# cerebellum (H_1280 forward-model) constants — substrate-derived, not tuned
E_THR         = 0.30         # prediction-error threshold: error < E_THR → trust prediction

# basal-ganglia (H_1281) constants
GO_THR        = 0.0          # go-margin threshold: predicted-move go-margin > 0 → select it

# ─── frozen GREEN bars (FREEZE.txt — NOT moved after scoring) ────────────────
COMPOSE_DELTA = 0.05
ORACLE_MARGIN = 0.02
SHUFFLE_TOL   = 0.02


# ─── decision-item construction (the five families) ─────────────────────────
def build_items(seed):
    """Build N_PER_FAMILY items per family. Each item dict carries:
      pred_error      — cerebellum forward-model prediction error (actual−predicted L2 proxy)
      go_margin       — basal go-value margin of the PREDICTED move over the best competitor
      correct         — ground-truth correct action (1=SELECT-PREDICTED, 0=SELECT-COMPETITOR)
    The substrate states are DERIVED FROM THE FAMILY STRUCTURE (not set to the answer):
    an item's correctness follows from the SCENARIO it instantiates, and each faculty
    reads only the substrate feature that scenario produces.
    """
    rng = np.random.default_rng(seed)

    items = []

    def jit(x):
        """AMBIGUITY jitter — pushes a substrate value toward its decision boundary so
        the owning faculty is NOT perfectly reliable (some items flip). Keeps the result
        an EARNED composition rather than a hand-built per-family certainty."""
        return x + AMBIG_NOISE * rng.standard_normal()

    # ── F1 CEREBELLUM-DECISIVE: cerebellum leans right, basal ambiguous ─────
    # Low prediction error (forward model trusts predicted move = CORRECT), jittered
    # toward E_THR so cerebellum errs on some. basal go-margin near a tie (~chance).
    # correct = SELECT-PREDICTED (1).
    for _ in range(N_PER_FAMILY):
        pred_error = max(0.0, jit(0.12))               # clearly below E_THR → cerebellum SELECTS-PRED
        go_margin  = jit(0.0)                            # basal near a tie (~chance)
        items.append(dict(pred_error=pred_error, go_margin=go_margin, correct=1, fam="F1"))

    # ── F2 BASAL-DECISIVE: basal leans right, cerebellum ambiguous ──────────
    # Clear best-grounded competitor (basal go-margin strongly NEGATIVE → SELECT-COMPETITOR
    # = correct, jittered) while cerebellum prediction error sits near E_THR (~chance).
    # correct = SELECT-COMPETITOR (0).
    for _ in range(N_PER_FAMILY):
        pred_error = max(0.0, E_THR + jit(0.0))        # near threshold (cerebellum ~chance)
        go_margin  = jit(-0.5)                           # strongly negative → basal SELECTS-COMPETITOR
        items.append(dict(pred_error=pred_error, go_margin=go_margin, correct=0, fam="F2"))

    # ── F3 AGREE: both lean correct (redundant region), jittered ────────────
    # Low prediction error (cerebellum SELECTS-PRED) + positive go-margin (basal SELECTS-PRED).
    # correct = SELECT-PREDICTED (1).
    for _ in range(N_PER_FAMILY):
        pred_error = max(0.0, jit(0.10))                # clearly low error → cerebellum SELECTS-PRED
        go_margin  = jit(0.5)                            # clearly positive → basal SELECTS-PRED
        items.append(dict(pred_error=pred_error, go_margin=go_margin, correct=1, fam="F3"))

    # ── F4 CONFLICT (cerebellum right): faculties OPPOSE; cerebellum correct ─
    # Low prediction error (cerebellum SELECTS-PRED, correct) BUT basal go-margin negative
    # (basal SELECTS-COMPETITOR, wrong). Tests whether the arbiter trusts cerebellum when
    # it's confident. correct = SELECT-PREDICTED (1).
    for _ in range(N_PER_FAMILY):
        pred_error = max(0.0, jit(0.08))                # very low error → cerebellum confident SELECTS-PRED
        go_margin  = jit(-0.45)                          # negative → basal SELECTS-COMPETITOR (wrong)
        items.append(dict(pred_error=pred_error, go_margin=go_margin, correct=1, fam="F4"))

    # ── F5 ADVERSARIAL CONFLICT (basal right, cerebellum LOUDER-but-wrong) ──
    # The hard case: faculties CONFLICT, the CORRECT action is basal's (SELECT-COMPETITOR
    # because the best-grounded candidate is the competitor), BUT the forward model reports
    # VERY low error (a low-error-LOOKING but mis-grounded prediction → cerebellum votes
    # SELECT-PREDICTED with HIGH confidence). A naive "trust the louder faculty" arbiter
    # would FOLLOW the cerebellum and be WRONG. anti-gift control: oracle still =1 (basal
    # is right) but the confidence-arbiter must NOT be fooled. correct = SELECT-COMPETITOR (0).
    for _ in range(N_PER_FAMILY):
        pred_error = max(0.0, jit(0.05))                # VERY low error → cerebellum votes PRED LOUDLY (wrong)
        go_margin  = jit(-0.6)                            # strongly negative → basal SELECTS-COMPETITOR (correct)
        items.append(dict(pred_error=pred_error, go_margin=go_margin, correct=0, fam="F5"))

    return items


# ─── per-faculty decisions + confidences ────────────────────────────────────
def cerebellum_decide(item):
    """SELECT-PREDICTED(1) iff prediction error < E_THR. Confidence = |E_THR − error|.
    (H_1280 forward model: a low prediction error means the predicted next-state move is
    trustworthy; a high error means the prediction is unreliable → defer to a competitor.)"""
    e = item["pred_error"]
    decision = 1 if e < E_THR else 0
    conf = abs(E_THR - e)
    return decision, conf, E_THR - e


def basal_decide(item):
    """SELECT-PREDICTED(1) iff the predicted move's go-value margin > GO_THR.
    Confidence = |go_margin − GO_THR|. (H_1281 basal-ganglia: the candidate with the
    highest learned go-value wins striatal disinhibition; a positive margin for the
    predicted move means it beats the best competitor, a negative margin means a
    competitor wins.)"""
    m = item["go_margin"]
    decision = 1 if m > GO_THR else 0
    conf = abs(m - GO_THR)
    return decision, conf, m - GO_THR


# ─── the SUBSTRATE-WEIGHTED arbiter (H_1397/H_1401 scale-relative confidence) ─
def arbiter(cb_dec, cb_conf, cb_mean, bg_dec, bg_conf, bg_mean):
    """Each faculty's vote weighted by its OWN scale-relative confidence
    (conf / that-faculty's-mean-conf) — the H_1397 a_break_the_wall commensurability
    fix so the two confidences (different scales) are comparable. The more-relatively-
    confident faculty's vote wins. NO hardcoded "cerebellum wins" priority
    (a_autonomy_over_hardcode). Agreement → that shared vote; disagreement → the higher
    relative confidence wins."""
    if cb_dec == bg_dec:
        return cb_dec
    cb_rel = cb_conf / (cb_mean + 1e-9)
    bg_rel = bg_conf / (bg_mean + 1e-9)
    return cb_dec if cb_rel >= bg_rel else bg_dec


# ─── run one seed ────────────────────────────────────────────────────────────
def run_seed(seed):
    items = build_items(seed)
    n = len(items)

    cb = [cerebellum_decide(it) for it in items]   # (dec, conf, raw)
    bg = [basal_decide(it) for it in items]
    cb_mean = float(np.mean([c for _, c, _ in cb]))
    bg_mean = float(np.mean([c for _, c, _ in bg]))

    correct = [it["correct"] for it in items]

    acc_cerebellum = float(np.mean([int(cb[i][0] == correct[i]) for i in range(n)]))
    acc_basal      = float(np.mean([int(bg[i][0] == correct[i]) for i in range(n)]))

    # compose (substrate-weighted arbiter, no hardcoded priority)
    comp = [arbiter(cb[i][0], cb[i][1], cb_mean, bg[i][0], bg[i][1], bg_mean)
            for i in range(n)]
    acc_compose = float(np.mean([int(comp[i] == correct[i]) for i in range(n)]))

    # ORACLE ceiling: correct iff EITHER faculty-alone is correct
    oracle = [int(cb[i][0] == correct[i] or bg[i][0] == correct[i]) for i in range(n)]
    acc_oracle = float(np.mean(oracle))

    # conflict rate: the two faculties propose opposite actions
    conflict = [int(cb[i][0] != bg[i][0]) for i in range(n)]
    conflict_rate = float(np.mean(conflict))

    # only-X decomposition
    only_cerebellum = float(np.mean([int(cb[i][0] == correct[i] and bg[i][0] != correct[i]) for i in range(n)]))
    only_basal      = float(np.mean([int(bg[i][0] == correct[i] and cb[i][0] != correct[i]) for i in range(n)]))
    both            = float(np.mean([int(cb[i][0] == correct[i] and bg[i][0] == correct[i]) for i in range(n)]))
    neither         = float(np.mean([int(cb[i][0] != correct[i] and bg[i][0] != correct[i]) for i in range(n)]))

    # SHUFFLE control: permute which faculty-reads attach to which item, re-arbitrate.
    # If the compose lift survives the shuffle, it was averaging luck, not grounded coupling.
    shuf_rng = np.random.default_rng(seed * 2654435761 % (2**32) + 7)
    perm_c = shuf_rng.permutation(n)
    perm_b = shuf_rng.permutation(n)
    comp_shuf = [arbiter(cb[perm_c[i]][0], cb[perm_c[i]][1], cb_mean,
                         bg[perm_b[i]][0], bg[perm_b[i]][1], bg_mean)
                 for i in range(n)]
    acc_shuffle = float(np.mean([int(comp_shuf[i] == correct[i]) for i in range(n)]))

    return dict(seed=seed, n=n,
                acc_cerebellum=acc_cerebellum, acc_basal=acc_basal,
                best_single=max(acc_cerebellum, acc_basal),
                acc_compose=acc_compose, acc_shuffle=acc_shuffle, acc_oracle=acc_oracle,
                conflict_rate=conflict_rate,
                only_cerebellum=only_cerebellum, only_basal=only_basal, both=both, neither=neither)


# ─── leg B4: philosophy audit (H_1401 style; grep operative code) ───────────
def philosophy_audit():
    import re, io, tokenize
    src = open(__file__).read()
    toks = []
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type in (tokenize.STRING, tokenize.COMMENT, tokenize.FSTRING_START,
                        tokenize.FSTRING_MIDDLE, tokenize.FSTRING_END):
            continue
        toks.append(tok.string)
    code = " ".join(toks)
    forbidden = {
        "p1 system prompt":    r'system_prompt|system\s*:|--system-prompt',
        "p2 identity rule":    r'identity\s*=|you\s+are\s+\w',
        "p3 persona":          r'persona|you\s+are\s+anima|be\s+ethical|be\s+helpful',
        "p4 assistant frame":  r'helpful\s+assistant|assistant_role',
        "p6 RLHF/pref label":  r'rlhf|reward_model|preference_label|answer_label|be_good',
        "hardcoded priority":  r'cerebellum_wins|basal_wins|priority\s*=\s*["\']',
    }
    findings = {k: (m.group(0) if (m := re.search(pat, code, re.IGNORECASE)) else None)
                for k, pat in forbidden.items()}
    return all(v is None for v in findings.values()), findings


def main(write_verdict=True):
    out = []
    def emit(s=""):
        out.append(s); print(s, flush=True)

    emit("=" * 80)
    emit("H_1407 — BRAIN-LANE COMPOSE: cerebellum (H_1280) × basal-ganglia (H_1281)")
    emit("  DIRECTIONAL numpy mirror · $0 CPU · 3 seeds · p7 · LIVE CORE/*.hexa UNTOUCHED")
    emit(f"  bars: COMPOSE_DELTA={COMPOSE_DELTA} ORACLE_MARGIN={ORACLE_MARGIN} SHUFFLE_TOL={SHUFFLE_TOL}")
    emit("=" * 80)

    rows = [run_seed(s) for s in SEEDS]
    for r in rows:
        emit(f"  seed {r['seed']} (n={r['n']}): "
             f"cb={r['acc_cerebellum']:.3f} bg={r['acc_basal']:.3f} "
             f"best={r['best_single']:.3f} compose={r['acc_compose']:.3f} "
             f"shuf={r['acc_shuffle']:.3f} oracle={r['acc_oracle']:.3f} | "
             f"conflict={r['conflict_rate']:.3f} "
             f"[onlyCB={r['only_cerebellum']:.3f} onlyBG={r['only_basal']:.3f} "
             f"both={r['both']:.3f} neither={r['neither']:.3f}]")

    m = lambda k: float(np.mean([r[k] for r in rows]))
    acc_cerebellum, acc_basal = m('acc_cerebellum'), m('acc_basal')
    best_single = m('best_single')
    acc_compose, acc_shuffle, acc_oracle = m('acc_compose'), m('acc_shuffle'), m('acc_oracle')
    conflict_rate = m('conflict_rate')
    only_cerebellum, only_basal = m('only_cerebellum'), m('only_basal')
    both, neither = m('both'), m('neither')

    emit("-" * 80)
    emit("MEAN (3 seeds):")
    emit(f"  acc_cerebellum = {acc_cerebellum:.4f}")
    emit(f"  acc_basal      = {acc_basal:.4f}")
    emit(f"  best_single    = {best_single:.4f}")
    emit(f"  acc_compose    = {acc_compose:.4f}")
    emit(f"  acc_shuffle    = {acc_shuffle:.4f}")
    emit(f"  ORACLE         = {acc_oracle:.4f}   (oracle − best = {acc_oracle - best_single:+.4f})")
    emit(f"  conflict_rate  = {conflict_rate:.4f}")
    emit(f"  decomposition  : only_cerebellum={only_cerebellum:.4f} only_basal={only_basal:.4f} "
         f"both={both:.4f} neither={neither:.4f}")

    # frozen bars
    B1 = acc_compose >= best_single + COMPOSE_DELTA
    B2 = (acc_oracle - best_single) > ORACLE_MARGIN
    B3 = (acc_compose - acc_shuffle) > SHUFFLE_TOL
    B4, findings = philosophy_audit()

    emit("-" * 80)
    emit(f"  (B1 COMPOSE-EFFECT) compose {acc_compose:.4f} >= best {best_single:.4f}+{COMPOSE_DELTA} "
         f"({best_single+COMPOSE_DELTA:.4f}) : {'PASS' if B1 else 'FAIL'}")
    emit(f"  (B2 ORACLE)         oracle−best {acc_oracle-best_single:+.4f} > {ORACLE_MARGIN} : {'PASS' if B2 else 'FAIL'}")
    emit(f"  (B3 EARNED)         compose−shuffle {acc_compose-acc_shuffle:+.4f} > {SHUFFLE_TOL} : {'PASS' if B3 else 'FAIL'}")
    emit(f"  (B4 p6 GUARD)       no injected answer/persona/priority label : {'PASS' if B4 else 'FAIL'}")
    for k, v in findings.items():
        emit(f"        {k:22s}: {'clean' if v is None else 'FOUND -> ' + repr(v)}")

    emit("=" * 80)
    # a_break_the_wall taxonomy
    if B1 and B2 and B3 and B4:
        verdict = "🟢 COMPOSE-LIFT"
        reading = ("cerebellum + basal-ganglia are COMPLEMENTARY and compose to a NET LIFT — "
                   "integration raises capability. The substrate-weighted arbiter (scale-relative "
                   "confidence, NO hardcoded priority) captures the oracle headroom; shuffle "
                   "collapses (earned, p6). → names an engine-native §compose follow-on.")
    elif B2 and B4 and not B1:
        verdict = "🟠 ORACLE-HEADROOM-but-ARBITER-FAILS"
        reading = ("taxonomy (a) wrong-arbiter: complementarity EXISTS (oracle > best_single) but the "
                   "substrate-weighted arbiter cannot capture it — the faculties compose IN PRINCIPLE "
                   "but this confidence-arbiter is the wrong rule. → needs a better arbiter.")
    elif not B2:
        verdict = "🧱 INDEPENDENT-or-SUBSUMED"
        reading = ("taxonomy (d): NO oracle headroom (oracle ≈ best_single) — the faculties do NOT "
                   "compose to a lift. Either INDEPENDENT (one subsumes the other's competence here) "
                   "or REDUNDANT. A REAL finding about anima's integration limits (c9), NOT a failure.")
    elif not B4:
        verdict = "🔴 RED (p6 guard failed — a label leaked)"
        reading = "an injected answer/persona/priority surface drove behavior — p6 NOT satisfied."
    else:
        verdict = "🔴 RED (mixed)"
        reading = "see the per-bar tally above."

    # subsumption probe report
    if only_cerebellum < 0.01 and only_basal < 0.01:
        subsumption = ("REDUNDANT/SUBSUMED — neither faculty solves items the other misses "
                       "(only_cerebellum≈0 ∧ only_basal≈0).")
    elif only_cerebellum > 0.0 and only_basal > 0.0:
        subsumption = (f"SEPARABLE — each faculty uniquely solves items the other misses "
                       f"(only_cerebellum={only_cerebellum:.3f} > 0 AND only_basal={only_basal:.3f} > 0). "
                       f"genuinely complementary signals.")
    else:
        subsumption = (f"ONE-SIDED — only_cerebellum={only_cerebellum:.3f}, only_basal={only_basal:.3f}: "
                       f"one faculty subsumes the other's competence on this fixture.")

    emit(f"VERDICT: {verdict}")
    emit(f"READING: {reading}")
    emit(f"SUBSUMPTION PROBE: {subsumption}")
    emit("  HONEST (c9, a_scale_honest_scope/a_toy_scale_recheck): DIRECTIONAL numpy mirror; toy")
    emit("  synthetic 5-family fixture, 3 seeds, deterministic readouts (tests COMPOSITION STRUCTURE,")
    emit("  not a trained integrator). LIVE CORE/*.hexa UNTOUCHED. Scale/real-corpus/engine-native")
    emit("  transfer UNVERIFIED. NO bar moved post-hoc.")
    emit("=" * 80)

    if write_verdict:
        import os
        vp = os.path.join(os.path.dirname(__file__), "..", "..",
                          ".verdicts", "1407_brain_lane_compose_cerebellum_basal", "result.txt")
        vp = os.path.abspath(vp)
        os.makedirs(os.path.dirname(vp), exist_ok=True)
        with open(vp, "w") as f:
            f.write("\n".join(out) + "\n")
    return verdict


if __name__ == "__main__":
    main()
