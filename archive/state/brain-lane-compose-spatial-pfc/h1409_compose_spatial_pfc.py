"""
H_1409 — BRAIN-LANE COMPOSITION pair #5: does the SPATIAL-MAP (H_1296) compose with
HIERARCHICAL-PFC (H_1294)?  THE DECISIVE TEST OF THE REFINED MIN-CUT-MI LAW.

FIFTH cognitively-meaningful brain-lane PAIR composition test (after H_1401
affect×ethics, H_1404 affect×ethics-Φ, H_1405 memory×ToM, H_1407 cerebellum×basal).
Every anima brain faculty is engine-native GREEN — but ALONE. This lane asks whether
TWO richly-integrated HIGH-Φ STRUCTURED subsystems INTEGRATE on a shared decision, and
(separate Φ runner) whether composing TWO HIGH-Φ faculties COMPOSES (cheaper coupled
cut, like H_1407) or BLOCKS (mutual domination, like H_1405).

Methodology ported VERBATIM from H_1401 (capability) — substrate-weighted SCALE-RELATIVE
arbiter (the a_break_the_wall commensurability fix) + ORACLE ceiling + SHUFFLE control +
only-X decomposition + the a_break_the_wall verdict taxonomy.

DIRECTIONAL numpy mirror — LIVE CORE/*.hexa UNTOUCHED. $0 CPU, gradient-free, 3 seeds,
p7 (NO LLM-judge). Engine-native §compose is the named follow-on IF 🟢.

────────────────────────────────────────────────────────────────────────────────
THE PAIR (each reuses its OWN H_1296 / H_1294 mirror substrate):
  SPATIAL-MAP (H_1296 SpatialMap): landmarks stored AT 2-D positions; the relational
                   query "is landmark X nearer to A or to B?" is answered by Euclidean
                   DISTANCE. spatial-alone policy: PICK-FIRST iff the metric margin
                   metric_margin = d(X, opt2) − d(X, opt1) > 0 (option1 nearer); near a
                   tie (~0) it is ~chance.
  HIERARCHICAL-PFC (H_1294 HierGoalStack): a 2-level goal STACK {top goal, ordered
                   subgoal list, pointer p} with completion-triggered ADVANCE. pfc-alone
                   policy: PICK-FIRST iff the current-subgoal alignment margin
                   align_margin = align(opt1, subgoal[p]) − align(opt2, subgoal[p]) > 0
                   (option1 is the next-in-plan grounded subgoal); near 0 it is ~chance.

Both are richly-integrated HIGH-Φ STRUCTURED subsystems (a metric 2-D cognitive map +
an ordered sequential controller). The refined program LAW (H_1404/1405/1407) asks
whether TWO high-Φ parts MUTUALLY BLOCK (H_1405) or the coupling finds a cheaper cut
(H_1407). The capability leg tests whether they compose on a decision; the Φ leg
(separate runner) is the decisive law test.

────────────────────────────────────────────────────────────────────────────────
DECISION TASK. Binary: PICK-FIRST(1) vs PICK-SECOND(0) — a shared binary readout over
two ordered candidate options. Each item has a ground-truth correct option. SOME items
are decided by metric/relational spatial reasoning (which option is nearer landmark X),
SOME by ordered goal-sequence execution (which option is the next grounded subgoal).

FIVE item families (the correct action is NOT trivially one faculty's salience):
  (F1) SPATIAL-DECISIVE — relational metric margin clear (spatial map picks the nearer
       option = correct), the PFC alignment margin sits near its threshold (~chance).
  (F2) PFC-DECISIVE — the ordered-plan alignment margin is clear (PFC picks the next
       grounded subgoal = correct), the spatial metric margin is near a tie (~chance).
  (F3) AGREE — both lean the same correct way (redundant region).
  (F4) CONFLICT (spatial right) — faculties OPPOSE; the metric is correct (nearer
       option) but the PFC alignment favors the other option.
  (F5) ADVERSARIAL CONFLICT (PFC right, spatial LOUDER-but-wrong) — anti-gift control:
       faculties OPPOSE, PFC is correct (next-in-plan), BUT the spatial map reports a
       VERY large metric margin for the WRONG option (a clear-LOOKING but mis-placed
       landmark). A naive "trust the louder faculty" arbiter FOLLOWS the spatial map
       and is WRONG.

NO faculty alone can solve all five → best_single < oracle iff truly complementary.

p6 / PHILOSOPHY GUARD (leg B4): spatial & pfc BOTH read ONLY substrate state (metric
distance margins, ordered-plan alignment margins). NO injected answer/persona/ethics/
priority label enters either faculty's read or the arbiter. A structural audit greps
the OPERATIVE code (strings/comments dropped) — must be CLEAN. The SHUFFLE control
re-confirms the compose lift (if any) is the grounded coupling, not averaging luck.
"""
import numpy as np

# ─── frozen knobs (pre-registered, FREEZE.txt) ──────────────────────────────
SEEDS         = [4900, 4901, 4902]
N_PER_FAMILY  = 90            # items per family (F1..F5) → 450 items/seed
AMBIG_NOISE   = 0.18          # jitter toward decision boundary (no faculty perfectly reliable)

# spatial-map (H_1296) constants — substrate-derived, not tuned
MET_THR       = 0.0          # metric-margin threshold: d(X,opt2)−d(X,opt1) > 0 → option1 nearer

# hierarchical-pfc (H_1294) constants
ALIGN_THR     = 0.0          # align-margin threshold: align(opt1)−align(opt2) > 0 → option1 next-in-plan

# ─── frozen GREEN bars (FREEZE.txt — NOT moved after scoring) ────────────────
COMPOSE_DELTA = 0.05
ORACLE_MARGIN = 0.02
SHUFFLE_TOL   = 0.02


# ─── decision-item construction (the five families) ─────────────────────────
def build_items(seed):
    """Build N_PER_FAMILY items per family. Each item dict carries:
      metric_margin   — spatial map's relational margin d(X,opt2)−d(X,opt1) (>0 ⇒ option1 nearer)
      align_margin    — pfc's ordered-plan alignment margin align(opt1)−align(opt2) (>0 ⇒ option1 next)
      correct         — ground-truth correct action (1=PICK-FIRST, 0=PICK-SECOND)
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

    # ── F1 SPATIAL-DECISIVE: spatial leans right, pfc ambiguous ─────────────
    # Clear positive metric margin (spatial map: option1 nearer = correct), jittered
    # so spatial errs on some. pfc alignment margin near a tie (~chance).
    # correct = PICK-FIRST (1).
    for _ in range(N_PER_FAMILY):
        metric_margin = jit(0.5)                        # clearly positive → spatial PICKS-FIRST
        align_margin  = jit(0.0)                         # pfc near a tie (~chance)
        items.append(dict(metric_margin=metric_margin, align_margin=align_margin, correct=1, fam="F1"))

    # ── F2 PFC-DECISIVE: pfc leans right, spatial ambiguous ─────────────────
    # Clear negative alignment margin (pfc: option2 is the next-in-plan grounded subgoal →
    # PICK-SECOND = correct, jittered) while the spatial metric margin sits near a tie
    # (~chance). correct = PICK-SECOND (0).
    for _ in range(N_PER_FAMILY):
        metric_margin = jit(0.0)                        # near a tie (spatial ~chance)
        align_margin  = jit(-0.5)                        # strongly negative → pfc PICKS-SECOND
        items.append(dict(metric_margin=metric_margin, align_margin=align_margin, correct=0, fam="F2"))

    # ── F3 AGREE: both lean correct (redundant region), jittered ────────────
    # Positive metric margin (spatial PICKS-FIRST) + positive alignment margin (pfc PICKS-FIRST).
    # correct = PICK-FIRST (1).
    for _ in range(N_PER_FAMILY):
        metric_margin = jit(0.45)                       # clearly positive → spatial PICKS-FIRST
        align_margin  = jit(0.5)                         # clearly positive → pfc PICKS-FIRST
        items.append(dict(metric_margin=metric_margin, align_margin=align_margin, correct=1, fam="F3"))

    # ── F4 CONFLICT (spatial right): faculties OPPOSE; spatial correct ──────
    # Positive metric margin (spatial PICKS-FIRST, correct) BUT negative alignment margin
    # (pfc PICKS-SECOND, wrong). Tests whether the arbiter trusts spatial when it's
    # confident. correct = PICK-FIRST (1).
    for _ in range(N_PER_FAMILY):
        metric_margin = jit(0.55)                       # clearly positive → spatial confident PICKS-FIRST
        align_margin  = jit(-0.45)                       # negative → pfc PICKS-SECOND (wrong)
        items.append(dict(metric_margin=metric_margin, align_margin=align_margin, correct=1, fam="F4"))

    # ── F5 ADVERSARIAL CONFLICT (pfc right, spatial LOUDER-but-wrong) ───────
    # The hard case: faculties CONFLICT, the CORRECT action is pfc's (PICK-SECOND because
    # option2 is the next-in-plan grounded subgoal), BUT the spatial map reports a VERY
    # large positive metric margin for option1 (a clear-LOOKING but mis-placed landmark →
    # spatial votes PICK-FIRST with HIGH confidence). A naive "trust the louder faculty"
    # arbiter would FOLLOW the spatial map and be WRONG. anti-gift control: oracle still
    # =1 (pfc is right) but the confidence-arbiter must NOT be fooled. correct = PICK-SECOND (0).
    for _ in range(N_PER_FAMILY):
        metric_margin = jit(0.7)                         # VERY large positive → spatial votes FIRST LOUDLY (wrong)
        align_margin  = jit(-0.55)                       # strongly negative → pfc PICKS-SECOND (correct)
        items.append(dict(metric_margin=metric_margin, align_margin=align_margin, correct=0, fam="F5"))

    return items


# ─── per-faculty decisions + confidences ────────────────────────────────────
def spatial_decide(item):
    """PICK-FIRST(1) iff metric margin > MET_THR. Confidence = |metric_margin − MET_THR|.
    (H_1296 spatial map: a positive d(X,opt2)−d(X,opt1) means option1 is the nearer
    landmark to the query landmark X; a near-zero margin means the two options are
    near-equidistant → ~chance.)"""
    m = item["metric_margin"]
    decision = 1 if m > MET_THR else 0
    conf = abs(m - MET_THR)
    return decision, conf, m - MET_THR


def pfc_decide(item):
    """PICK-FIRST(1) iff the ordered-plan alignment margin > ALIGN_THR.
    Confidence = |align_margin − ALIGN_THR|. (H_1294 hier-PFC: a positive
    align(opt1)−align(opt2) for the current pointer-subgoal means option1 is the
    next-in-plan grounded subgoal; near 0 the controller is undecided.)"""
    a = item["align_margin"]
    decision = 1 if a > ALIGN_THR else 0
    conf = abs(a - ALIGN_THR)
    return decision, conf, a - ALIGN_THR


# ─── the SUBSTRATE-WEIGHTED arbiter (H_1397/H_1401 scale-relative confidence) ─
def arbiter(sp_dec, sp_conf, sp_mean, pf_dec, pf_conf, pf_mean):
    """Each faculty's vote weighted by its OWN scale-relative confidence
    (conf / that-faculty's-mean-conf) — the H_1397 a_break_the_wall commensurability
    fix so the two confidences (different scales) are comparable. The more-relatively-
    confident faculty's vote wins. NO hardcoded "spatial wins" priority
    (a_autonomy_over_hardcode). Agreement → that shared vote; disagreement → the higher
    relative confidence wins."""
    if sp_dec == pf_dec:
        return sp_dec
    sp_rel = sp_conf / (sp_mean + 1e-9)
    pf_rel = pf_conf / (pf_mean + 1e-9)
    return sp_dec if sp_rel >= pf_rel else pf_dec


# ─── run one seed ────────────────────────────────────────────────────────────
def run_seed(seed):
    items = build_items(seed)
    n = len(items)

    sp = [spatial_decide(it) for it in items]   # (dec, conf, raw)
    pf = [pfc_decide(it) for it in items]
    sp_mean = float(np.mean([c for _, c, _ in sp]))
    pf_mean = float(np.mean([c for _, c, _ in pf]))

    correct = [it["correct"] for it in items]

    acc_spatial = float(np.mean([int(sp[i][0] == correct[i]) for i in range(n)]))
    acc_pfc     = float(np.mean([int(pf[i][0] == correct[i]) for i in range(n)]))

    # compose (substrate-weighted arbiter, no hardcoded priority)
    comp = [arbiter(sp[i][0], sp[i][1], sp_mean, pf[i][0], pf[i][1], pf_mean)
            for i in range(n)]
    acc_compose = float(np.mean([int(comp[i] == correct[i]) for i in range(n)]))

    # ORACLE ceiling: correct iff EITHER faculty-alone is correct
    oracle = [int(sp[i][0] == correct[i] or pf[i][0] == correct[i]) for i in range(n)]
    acc_oracle = float(np.mean(oracle))

    # conflict rate: the two faculties propose opposite actions
    conflict = [int(sp[i][0] != pf[i][0]) for i in range(n)]
    conflict_rate = float(np.mean(conflict))

    # only-X decomposition
    only_spatial = float(np.mean([int(sp[i][0] == correct[i] and pf[i][0] != correct[i]) for i in range(n)]))
    only_pfc     = float(np.mean([int(pf[i][0] == correct[i] and sp[i][0] != correct[i]) for i in range(n)]))
    both         = float(np.mean([int(sp[i][0] == correct[i] and pf[i][0] == correct[i]) for i in range(n)]))
    neither      = float(np.mean([int(sp[i][0] != correct[i] and pf[i][0] != correct[i]) for i in range(n)]))

    # SHUFFLE control: permute which faculty-reads attach to which item, re-arbitrate.
    # If the compose lift survives the shuffle, it was averaging luck, not grounded coupling.
    shuf_rng = np.random.default_rng(seed * 2654435761 % (2**32) + 7)
    perm_s = shuf_rng.permutation(n)
    perm_p = shuf_rng.permutation(n)
    comp_shuf = [arbiter(sp[perm_s[i]][0], sp[perm_s[i]][1], sp_mean,
                         pf[perm_p[i]][0], pf[perm_p[i]][1], pf_mean)
                 for i in range(n)]
    acc_shuffle = float(np.mean([int(comp_shuf[i] == correct[i]) for i in range(n)]))

    return dict(seed=seed, n=n,
                acc_spatial=acc_spatial, acc_pfc=acc_pfc,
                best_single=max(acc_spatial, acc_pfc),
                acc_compose=acc_compose, acc_shuffle=acc_shuffle, acc_oracle=acc_oracle,
                conflict_rate=conflict_rate,
                only_spatial=only_spatial, only_pfc=only_pfc, both=both, neither=neither)


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
        "hardcoded priority":  r'spatial_wins|pfc_wins|priority\s*=\s*["\']',
    }
    findings = {k: (m.group(0) if (m := re.search(pat, code, re.IGNORECASE)) else None)
                for k, pat in forbidden.items()}
    return all(v is None for v in findings.values()), findings


def main(write_verdict=True):
    out = []
    def emit(s=""):
        out.append(s); print(s, flush=True)

    emit("=" * 80)
    emit("H_1409 — BRAIN-LANE COMPOSE: spatial-map (H_1296) × hierarchical-pfc (H_1294)")
    emit("  DIRECTIONAL numpy mirror · $0 CPU · 3 seeds · p7 · LIVE CORE/*.hexa UNTOUCHED")
    emit(f"  bars: COMPOSE_DELTA={COMPOSE_DELTA} ORACLE_MARGIN={ORACLE_MARGIN} SHUFFLE_TOL={SHUFFLE_TOL}")
    emit("=" * 80)

    rows = [run_seed(s) for s in SEEDS]
    for r in rows:
        emit(f"  seed {r['seed']} (n={r['n']}): "
             f"sp={r['acc_spatial']:.3f} pf={r['acc_pfc']:.3f} "
             f"best={r['best_single']:.3f} compose={r['acc_compose']:.3f} "
             f"shuf={r['acc_shuffle']:.3f} oracle={r['acc_oracle']:.3f} | "
             f"conflict={r['conflict_rate']:.3f} "
             f"[onlySP={r['only_spatial']:.3f} onlyPF={r['only_pfc']:.3f} "
             f"both={r['both']:.3f} neither={r['neither']:.3f}]")

    m = lambda k: float(np.mean([r[k] for r in rows]))
    acc_spatial, acc_pfc = m('acc_spatial'), m('acc_pfc')
    best_single = m('best_single')
    acc_compose, acc_shuffle, acc_oracle = m('acc_compose'), m('acc_shuffle'), m('acc_oracle')
    conflict_rate = m('conflict_rate')
    only_spatial, only_pfc = m('only_spatial'), m('only_pfc')
    both, neither = m('both'), m('neither')

    emit("-" * 80)
    emit("MEAN (3 seeds):")
    emit(f"  acc_spatial    = {acc_spatial:.4f}")
    emit(f"  acc_pfc        = {acc_pfc:.4f}")
    emit(f"  best_single    = {best_single:.4f}")
    emit(f"  acc_compose    = {acc_compose:.4f}")
    emit(f"  acc_shuffle    = {acc_shuffle:.4f}")
    emit(f"  ORACLE         = {acc_oracle:.4f}   (oracle − best = {acc_oracle - best_single:+.4f})")
    emit(f"  conflict_rate  = {conflict_rate:.4f}")
    emit(f"  decomposition  : only_spatial={only_spatial:.4f} only_pfc={only_pfc:.4f} "
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
        reading = ("spatial-map + hierarchical-pfc are COMPLEMENTARY and compose to a NET LIFT — "
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
    if only_spatial < 0.01 and only_pfc < 0.01:
        subsumption = ("REDUNDANT/SUBSUMED — neither faculty solves items the other misses "
                       "(only_spatial≈0 ∧ only_pfc≈0).")
    elif only_spatial > 0.0 and only_pfc > 0.0:
        subsumption = (f"SEPARABLE — each faculty uniquely solves items the other misses "
                       f"(only_spatial={only_spatial:.3f} > 0 AND only_pfc={only_pfc:.3f} > 0). "
                       f"genuinely complementary signals.")
    else:
        subsumption = (f"ONE-SIDED — only_spatial={only_spatial:.3f}, only_pfc={only_pfc:.3f}: "
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
                          ".verdicts", "1409_brain_lane_compose_spatial_pfc", "result.txt")
        vp = os.path.abspath(vp)
        os.makedirs(os.path.dirname(vp), exist_ok=True)
        with open(vp, "w") as f:
            f.write("\n".join(out) + "\n")
    return verdict


if __name__ == "__main__":
    main()
