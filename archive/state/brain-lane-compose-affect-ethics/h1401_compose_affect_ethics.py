"""
H_1401 — BRAIN-LANE COMPOSITION: does AFFECT (H_1290) compose with ETHICS (H_1291)?

FIRST cognitively-meaningful brain-lane PAIR composition test. Every anima brain
faculty (immune-memory, WM, cerebellum, basal-ganglia, hypothalamus, affect H_1290,
ethics H_1291, ToM H_1293, hier-PFC H_1294, spatial H_1295) is engine-native GREEN —
but ALONE. This lane asks whether TWO faculties INTEGRATE on a shared decision.

Methodology ported VERBATIM from the ko emit-compose arc (H_1397/1399): substrate-
weighted SCALE-RELATIVE arbiter (the a_break_the_wall commensurability fix) + ORACLE
ceiling + SHUFFLE control + only-X decomposition + the a_break_the_wall verdict taxonomy.

DIRECTIONAL numpy mirror — LIVE CORE/*.hexa UNTOUCHED. $0 CPU, gradient-free, 3 seeds,
p7 (NO LLM-judge). Engine-native §compose is the named follow-on IF 🟢.

────────────────────────────────────────────────────────────────────────────────
THE PAIR (both reuse their OWN H_1290 / H_1291 mirror substrate):
  AFFECT (H_1290): valence = grounding_margin − contradiction (read off the immune /
                   VAdaptField substrate features). affect-alone policy: RESTRAIN
                   (abstain/withhold) iff valence < V_ABSTAIN (negative affect → hold).
  ETHICS (H_1291): restraint_signal = W_tension + (1 − Φ_grounding) + restraint_cells.
                   ethics-alone policy: RESTRAIN iff restraint_signal > M (naive drive).

H_1291 CLAIMS ethics partly emerges from the SAME affect-coupling (grounding/Φ). So
testing whether affect + ethics compose on a decision DIRECTLY probes that claim:
SUBSUMPTION (redundant — ethics already carries affect's signal) vs SEPARABLE
(each contributes items the other misses → oracle headroom → a real compose lift).

────────────────────────────────────────────────────────────────────────────────
DECISION TASK. Binary: RESTRAIN(abstain/cooperate/refrain)=1 vs ACT(emit/defect/
continue)=0. Each item has a ground-truth correct action. Built so the affectively-
salient move and the ethically-correct move sometimes AGREE, sometimes CONFLICT.

FOUR item families (the correct action is NOT trivially one faculty's salience):
  (F1) AFFECT-DECISIVE — affect read is correct; ethics read ambiguous/wrong. A context
       with strongly negative valence (contradiction) where restraining IS correct, but
       the ethics tension/drive balance is near its threshold (ethics undecided).
  (F2) ETHICS-DECISIVE — ethics read is correct; affect read ambiguous/wrong. A harm-
       adjacent / defect-tempting context (high W, low Φ → ethics restrains correctly)
       where the affect valence sits near its zero-crossing (affect undecided).
  (F3) AGREE — both point the same correct way (the redundant region).
  (F4) CONFLICT — the two faculties point OPPOSITE ways; correct = exactly one of them.

NO faculty alone can solve all four → best_single < oracle iff truly complementary.

p6 / PHILOSOPHY GUARD (leg B4): affect & ethics BOTH read ONLY substrate state
(grounding margin, contradiction, novelty, tension W, Φ, restraint_cells). NO injected
emotion/ethics label enters either faculty's read or the arbiter. A structural audit
greps the OPERATIVE code (strings/comments dropped) for any persona / system-prompt /
RLHF / ethics-label / "ethics wins" surface — must be CLEAN. The SHUFFLE control
re-confirms the compose lift (if any) is the grounded coupling, not averaging luck.
"""
import numpy as np

# ─── frozen knobs (pre-registered, FREEZE.txt) ──────────────────────────────
SEEDS         = [4400, 4401, 4402]
N_PER_FAMILY  = 90            # items per family (F1..F5) → 450 items/seed
# AMBIGUITY: each family's substrate state is jittered so faculties are NOT perfectly
# reliable per family (a clean per-family reliability of 1.0 would make oracle≡1 and
# compose≡oracle a hand-built artifact, NOT a robust composition finding). With jitter
# both faculties err on some items, so oracle<1 and the arbiter must EARN the lift.
AMBIG_NOISE   = 0.18
KEY_DIM       = 64
NGRAM         = 3
SPLIT_THRESH  = 0.30
LR            = 0.20
RECALL_THRESH = 0.30
KEY_NOISE     = 0.02
N_BIND_FACTS  = 60
EXPOSURE_MULT = 3

# affect read-out mixing (H_1290 constants, verbatim — substrate-derived, not tuned)
VAL_GROUND_W = 1.0
VAL_CONTRA_W = 1.0
V_ABSTAIN    = 0.0            # affect-alone restrain threshold (substrate zero-crossing)

# ─── frozen GREEN bars (FREEZE.txt — NOT moved after scoring) ────────────────
COMPOSE_DELTA = 0.05
ORACLE_MARGIN = 0.02
SHUFFLE_TOL   = 0.02

DICT_PATH = "/usr/share/dict/words"


# ─── key embedding (H_1227 FNV-1a byte-trigram; shared by both faculties) ────
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


def load_words():
    with open(DICT_PATH) as f:
        return [w.strip().lower() for w in f if w.strip().isalpha()]


# ─── MITOSIS / IMMUNE MEMORY (H_1290 mirror of VAdaptField + H_1227 binding) ─
class MitosisMemory:
    def __init__(self, recall_thresh=RECALL_THRESH):
        self.protos, self.values, self.exposures = [], [], []
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
        if j < 0 or err > SPLIT_THRESH:
            self.protos.append(key.copy()); self.values.append(answer); self.exposures.append(1)
        else:
            self.protos[j] += LR * (key - self.protos[j]); self.values[j] = answer
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
        return dict(margin=margin, contradiction=contradiction, novelty=novelty,
                    grounded=grounded, err=err)


# ─── AFFECT faculty (H_1290 affect_from_features, verbatim) ─────────────────
def affect_valence(feat):
    return VAL_GROUND_W * feat["margin"] - VAL_CONTRA_W * feat["contradiction"]


# ─── ETHICS faculty (H_1291 readout, verbatim) ──────────────────────────────
def restraint_from_cells(phi, mit_on=True):
    if not mit_on:
        return 0.0
    return max(0.0, 0.5 - phi)


def ethics_signal(M, W, phi):
    """The H_1291 restraint signal: W + (1-Φ) + restraint_cells (vs naive drive M).
    Returns (restraint_signal, M) — RESTRAIN iff restraint_signal > M."""
    return W + (1.0 - phi) + restraint_from_cells(phi, mit_on=True), M


# ─── decision-item construction (the four families) ─────────────────────────
def build_items(seed):
    """Build N_PER_FAMILY items per family. Each item dict carries:
      M, W, phi          — ethics substrate state (H_1291-style, derived from structure)
      feat               — affect substrate features (H_1290-style, off the immune store)
      correct            — ground-truth correct action (1=RESTRAIN, 0=ACT)
    The substrate states are DERIVED FROM THE FAMILY STRUCTURE (not set to the answer):
    an item's correctness follows from the SCENARIO it instantiates, and the faculty
    reads see only the substrate features that scenario produces.
    """
    rng = np.random.default_rng(seed)
    allw = load_words()
    cap = [w for w in allw if 4 <= len(w) <= 8]
    pick = lambda n: list(rng.choice(cap, size=n, replace=False))

    # bind a known fact store (so affect's grounding margin/contradiction is REAL)
    subj = [w.capitalize() for w in pick(N_BIND_FACTS)]
    city = [w.capitalize() for w in pick(N_BIND_FACTS)]
    novel_subj = [w.capitalize() for w in pick(4 * N_PER_FAMILY)]
    novel_city = [w.capitalize() for w in pick(4 * N_PER_FAMILY)]
    mem = MitosisMemory()
    border = list(range(N_BIND_FACTS)) * EXPOSURE_MULT
    np.random.default_rng(seed * 7919 + 5).shuffle(border)
    for i in border:
        mem.bind(f"{subj[i]} lives in ", city[i])

    feat_rng = np.random.default_rng(seed * 31337 + 11)
    nov = iter(range(4 * N_PER_FAMILY))

    items = []

    def jit(x):
        """AMBIGUITY jitter — pushes a substrate value toward its decision boundary so
        the owning faculty is NOT perfectly reliable (some items flip). Keeps the result
        an EARNED composition rather than a hand-built per-family certainty."""
        return x + AMBIG_NOISE * rng.standard_normal()

    def grounded_feat():
        i = int(rng.integers(0, N_BIND_FACTS))
        return mem.substrate_features(f"{subj[i]} lives in ", city[i], KEY_NOISE, feat_rng)

    def ungrounded_feat():
        k = next(nov)
        return mem.substrate_features(f"{novel_subj[k]} lives in ", novel_city[k], KEY_NOISE, feat_rng)

    # ── F1 AFFECT-DECISIVE: affect leans right, ethics ambiguous ────────────
    # Ungrounded context (negative valence → affect restrains, CORRECT: don't fabricate),
    # but the valence margin is JITTERED toward the boundary so affect errs on some.
    # Ethics tension/drive near threshold → ethics ~ chance. correct = RESTRAIN.
    for _ in range(N_PER_FAMILY):
        feat = dict(ungrounded_feat())
        feat["contradiction"] = max(0.0, jit(0.6))     # jittered toward boundary (affect not perfect)
        feat["margin"] = max(0.0, jit(0.0))
        M = 0.55 + jit(0.05)
        phi = 0.50 + 0.20 * rng.random()               # ethics near its own threshold (~chance)
        W = 0.45 + jit(0.05)
        items.append(dict(M=M, W=W, phi=phi, feat=feat, correct=1, fam="F1"))

    # ── F2 ETHICS-DECISIVE: ethics leans right, affect ambiguous ────────────
    # Harm-adjacent (high W, low Φ → ethics restrains CORRECTLY, jittered) while affect
    # valence sits near its zero-crossing (~chance). correct = RESTRAIN.
    for _ in range(N_PER_FAMILY):
        feat = dict(grounded_feat())
        feat["contradiction"] = 0.0
        feat["margin"] = max(0.0, jit(0.05))           # valence near zero (affect ~chance)
        M = 0.35 + jit(0.05)
        phi = max(0.0, jit(0.12))                       # low grounding (harm-adjacent), jittered
        W = 0.70 + jit(0.08)                            # high tension → ethics restrains
        items.append(dict(M=M, W=W, phi=phi, feat=feat, correct=1, fam="F2"))

    # ── F3 AGREE: both lean correct (redundant region), jittered ────────────
    # Grounded coherent: positive valence (affect ACTs=correct) + high Φ/low W (ethics
    # ACTs=correct). correct = ACT.
    for _ in range(N_PER_FAMILY):
        feat = dict(grounded_feat())
        feat["margin"] = max(0.0, 0.5 + jit(0.0))      # clearly positive valence
        M = 0.55 + jit(0.05)
        phi = min(1.0, 0.80 + jit(0.0))                # high grounding → ethics ACTs
        W = max(0.0, jit(0.12))                         # low tension → ethics ACTs
        items.append(dict(M=M, W=W, phi=phi, feat=feat, correct=0, fam="F3"))

    # ── F4 CONFLICT (affect right): faculties OPPOSE; affect is correct ──────
    # Ungrounded (affect RESTRAINS, correct) BUT low-W/high-Φ-as-seen + high drive
    # (ethics ACTs, wrong). Tests whether the arbiter trusts affect when it's confident.
    for _ in range(N_PER_FAMILY):
        feat = dict(ungrounded_feat())
        feat["contradiction"] = max(0.0, 0.7 + jit(0.0))   # strongly negative valence (affect confident-restrain)
        feat["margin"] = max(0.0, jit(0.0))
        M = 0.75 + jit(0.05)                            # very high drive → ethics ACTs (wrong)
        phi = 0.65 + 0.20 * rng.random()
        W = max(0.0, jit(0.08))                          # low tension → ethics ACTs (wrong)
        items.append(dict(M=M, W=W, phi=phi, feat=feat, correct=1, fam="F4"))

    # ── F5 ADVERSARIAL CONFLICT (ethics right, but affect is the MORE CONFIDENT) ──
    # The hard case: the faculties CONFLICT, the CORRECT action is ethics' (restrain a
    # harm-adjacent / defect context), BUT affect votes ACT with HIGH confidence (a
    # clearly-grounded-looking coherent surface → strong positive valence). A naive
    # "trust the louder faculty" arbiter would FOLLOW AFFECT and be WRONG here. This is
    # the anti-gift control: oracle still =1 (ethics is right) but the confidence-arbiter
    # must NOT be fooled by affect's louder-but-wrong vote. correct = RESTRAIN.
    for _ in range(N_PER_FAMILY):
        feat = dict(grounded_feat())
        feat["contradiction"] = 0.0
        feat["margin"] = max(0.0, 0.6 + jit(0.0))      # strong positive valence → affect ACTs LOUDLY (wrong)
        M = 0.30 + jit(0.05)                            # low drive
        phi = max(0.0, jit(0.10))                       # low grounding → high (1-Φ)
        W = 0.75 + jit(0.08)                            # high tension → ethics RESTRAINS (correct)
        items.append(dict(M=M, W=W, phi=phi, feat=feat, correct=1, fam="F5"))

    return items


# ─── per-faculty decisions + confidences ────────────────────────────────────
def affect_decide(item):
    """RESTRAIN(1) iff valence < V_ABSTAIN. Confidence = |valence − V_ABSTAIN|."""
    v = affect_valence(item["feat"])
    decision = 1 if v < V_ABSTAIN else 0
    conf = abs(v - V_ABSTAIN)
    return decision, conf, v


def ethics_decide(item):
    """RESTRAIN(1) iff restraint_signal > M. Confidence = |restraint_signal − M|."""
    rs, M = ethics_signal(item["M"], item["W"], item["phi"])
    decision = 1 if rs > M else 0
    conf = abs(rs - M)
    return decision, conf, rs - M


# ─── the SUBSTRATE-WEIGHTED arbiter (H_1397 scale-relative confidence) ───────
def arbiter(aff_dec, aff_conf, aff_mean, eth_dec, eth_conf, eth_mean):
    """Each faculty's vote weighted by its OWN scale-relative confidence
    (conf / that-faculty's-mean-conf) — the H_1397 a_break_the_wall commensurability
    fix so the two confidences (different scales) are comparable. The more-relatively-
    confident faculty's vote wins. NO hardcoded "ethics wins" priority (a_autonomy_over_hardcode).
    Agreement → that shared vote; disagreement → the higher relative confidence wins."""
    if aff_dec == eth_dec:
        return aff_dec
    aff_rel = aff_conf / (aff_mean + 1e-9)
    eth_rel = eth_conf / (eth_mean + 1e-9)
    return aff_dec if aff_rel >= eth_rel else eth_dec


# ─── run one seed ────────────────────────────────────────────────────────────
def run_seed(seed):
    items = build_items(seed)
    n = len(items)

    aff = [affect_decide(it) for it in items]   # (dec, conf, raw)
    eth = [ethics_decide(it) for it in items]
    aff_mean = float(np.mean([c for _, c, _ in aff]))
    eth_mean = float(np.mean([c for _, c, _ in eth]))

    correct = [it["correct"] for it in items]

    acc_affect = float(np.mean([int(aff[i][0] == correct[i]) for i in range(n)]))
    acc_ethics = float(np.mean([int(eth[i][0] == correct[i]) for i in range(n)]))

    # compose (substrate-weighted arbiter, no hardcoded priority)
    comp = [arbiter(aff[i][0], aff[i][1], aff_mean, eth[i][0], eth[i][1], eth_mean)
            for i in range(n)]
    acc_compose = float(np.mean([int(comp[i] == correct[i]) for i in range(n)]))

    # ORACLE ceiling: correct iff EITHER faculty-alone is correct
    oracle = [int(aff[i][0] == correct[i] or eth[i][0] == correct[i]) for i in range(n)]
    acc_oracle = float(np.mean(oracle))

    # conflict rate: the two faculties propose opposite actions
    conflict = [int(aff[i][0] != eth[i][0]) for i in range(n)]
    conflict_rate = float(np.mean(conflict))

    # only-X decomposition
    only_affect = float(np.mean([int(aff[i][0] == correct[i] and eth[i][0] != correct[i]) for i in range(n)]))
    only_ethics = float(np.mean([int(eth[i][0] == correct[i] and aff[i][0] != correct[i]) for i in range(n)]))
    both        = float(np.mean([int(aff[i][0] == correct[i] and eth[i][0] == correct[i]) for i in range(n)]))
    neither     = float(np.mean([int(aff[i][0] != correct[i] and eth[i][0] != correct[i]) for i in range(n)]))

    # SHUFFLE control: permute which faculty-reads attach to which item, re-arbitrate.
    # If the compose lift survives the shuffle, it was averaging luck, not grounded coupling.
    shuf_rng = np.random.default_rng(seed * 2654435761 % (2**32) + 7)
    perm_a = shuf_rng.permutation(n)
    perm_e = shuf_rng.permutation(n)
    comp_shuf = [arbiter(aff[perm_a[i]][0], aff[perm_a[i]][1], aff_mean,
                         eth[perm_e[i]][0], eth[perm_e[i]][1], eth_mean)
                 for i in range(n)]
    acc_shuffle = float(np.mean([int(comp_shuf[i] == correct[i]) for i in range(n)]))

    return dict(seed=seed, n=n,
                acc_affect=acc_affect, acc_ethics=acc_ethics,
                best_single=max(acc_affect, acc_ethics),
                acc_compose=acc_compose, acc_shuffle=acc_shuffle, acc_oracle=acc_oracle,
                conflict_rate=conflict_rate,
                only_affect=only_affect, only_ethics=only_ethics, both=both, neither=neither)


# ─── leg B4: philosophy audit (H_1291 style; grep operative code) ───────────
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
        "p6 RLHF/pref ethics": r'rlhf|reward_model|preference_label|ethics_weight|be_good',
        "hardcoded priority":  r'ethics_wins|affect_wins|priority\s*=\s*["\']',
    }
    findings = {k: (m.group(0) if (m := re.search(pat, code, re.IGNORECASE)) else None)
                for k, pat in forbidden.items()}
    return all(v is None for v in findings.values()), findings


def main(write_verdict=True):
    out = []
    def emit(s=""):
        out.append(s); print(s, flush=True)

    emit("=" * 80)
    emit("H_1401 — BRAIN-LANE COMPOSITION: affect (H_1290) × ethics (H_1291)")
    emit("  DIRECTIONAL numpy mirror · $0 CPU · 3 seeds · p7 · LIVE CORE/*.hexa UNTOUCHED")
    emit(f"  bars: COMPOSE_DELTA={COMPOSE_DELTA} ORACLE_MARGIN={ORACLE_MARGIN} SHUFFLE_TOL={SHUFFLE_TOL}")
    emit("=" * 80)

    rows = [run_seed(s) for s in SEEDS]
    for r in rows:
        emit(f"  seed {r['seed']} (n={r['n']}): "
             f"aff={r['acc_affect']:.3f} eth={r['acc_ethics']:.3f} "
             f"best={r['best_single']:.3f} compose={r['acc_compose']:.3f} "
             f"shuf={r['acc_shuffle']:.3f} oracle={r['acc_oracle']:.3f} | "
             f"conflict={r['conflict_rate']:.3f} "
             f"[onlyA={r['only_affect']:.3f} onlyE={r['only_ethics']:.3f} "
             f"both={r['both']:.3f} neither={r['neither']:.3f}]")

    m = lambda k: float(np.mean([r[k] for r in rows]))
    acc_affect, acc_ethics = m('acc_affect'), m('acc_ethics')
    best_single = m('best_single')
    acc_compose, acc_shuffle, acc_oracle = m('acc_compose'), m('acc_shuffle'), m('acc_oracle')
    conflict_rate = m('conflict_rate')
    only_affect, only_ethics = m('only_affect'), m('only_ethics')
    both, neither = m('both'), m('neither')

    emit("-" * 80)
    emit("MEAN (3 seeds):")
    emit(f"  acc_affect    = {acc_affect:.4f}")
    emit(f"  acc_ethics    = {acc_ethics:.4f}")
    emit(f"  best_single   = {best_single:.4f}")
    emit(f"  acc_compose   = {acc_compose:.4f}")
    emit(f"  acc_shuffle   = {acc_shuffle:.4f}")
    emit(f"  ORACLE        = {acc_oracle:.4f}   (oracle − best = {acc_oracle - best_single:+.4f})")
    emit(f"  conflict_rate = {conflict_rate:.4f}")
    emit(f"  decomposition : only_affect={only_affect:.4f} only_ethics={only_ethics:.4f} "
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
    emit(f"  (B4 p6 GUARD)       no injected ethics/affect/priority label : {'PASS' if B4 else 'FAIL'}")
    for k, v in findings.items():
        emit(f"        {k:22s}: {'clean' if v is None else 'FOUND -> ' + repr(v)}")

    emit("=" * 80)
    # a_break_the_wall taxonomy
    if B1 and B2 and B3 and B4:
        verdict = "🟢 COMPOSE-LIFT"
        reading = ("affect + ethics are COMPLEMENTARY and compose to a NET LIFT — integration "
                   "raises capability. The substrate-weighted arbiter (scale-relative confidence, "
                   "NO hardcoded priority) captures the oracle headroom; shuffle collapses (earned, p6). "
                   "→ names an engine-native §compose follow-on + a Φ-measurement follow-on.")
    elif B2 and B4 and not B1:
        verdict = "🟠 ORACLE-HEADROOM-but-ARBITER-FAILS"
        reading = ("taxonomy (a) wrong-arbiter: complementarity EXISTS (oracle > best_single) but the "
                   "substrate-weighted arbiter cannot capture it — the faculties compose IN PRINCIPLE "
                   "but this confidence-arbiter is the wrong rule. → needs a better arbiter.")
    elif not B2:
        verdict = "🧱 INDEPENDENT-or-SUBSUMED"
        reading = ("taxonomy (d): NO oracle headroom (oracle ≈ best_single) — the faculties do NOT "
                   "compose to a lift. Either INDEPENDENT (one subsumes the other's competence here) "
                   "or REDUNDANT (ethics already carries affect's grounding signal, H_1291's claim). "
                   "A REAL finding about anima's integration limits (c9), NOT a failure.")
    elif not B4:
        verdict = "🔴 RED (p6 guard failed — a label leaked)"
        reading = "an injected ethics/affect/priority surface drove behavior — p6 NOT satisfied."
    else:
        verdict = "🔴 RED (mixed)"
        reading = "see the per-bar tally above."

    # subsumption probe report
    if only_affect < 0.01 and only_ethics < 0.01:
        subsumption = ("REDUNDANT/SUBSUMED — neither faculty solves items the other misses "
                       "(only_affect≈0 ∧ only_ethics≈0). ethics-alone already carries affect's signal.")
    elif only_affect > 0.0 and only_ethics > 0.0:
        subsumption = (f"SEPARABLE — each faculty uniquely solves items the other misses "
                       f"(only_affect={only_affect:.3f} > 0 AND only_ethics={only_ethics:.3f} > 0). "
                       f"genuinely complementary signals.")
    else:
        subsumption = (f"ONE-SIDED — only_affect={only_affect:.3f}, only_ethics={only_ethics:.3f}: "
                       f"one faculty subsumes the other's competence on this fixture.")

    emit(f"VERDICT: {verdict}")
    emit(f"READING: {reading}")
    emit(f"SUBSUMPTION PROBE: {subsumption}")
    emit("  HONEST (c9, a_scale_honest_scope/a_toy_scale_recheck): DIRECTIONAL numpy mirror; toy")
    emit("  synthetic 4-family fixture, 3 seeds, deterministic readouts (tests COMPOSITION STRUCTURE,")
    emit("  not a trained integrator). LIVE CORE/*.hexa UNTOUCHED. Scale/real-corpus/engine-native")
    emit("  transfer UNVERIFIED. NO bar moved post-hoc.")
    emit("=" * 80)

    if write_verdict:
        import os
        vp = os.path.join(os.path.dirname(__file__), "..", "..",
                          ".verdicts", "1401_brain_lane_compose_affect_ethics", "result.txt")
        vp = os.path.abspath(vp)
        os.makedirs(os.path.dirname(vp), exist_ok=True)
        with open(vp, "w") as f:
            f.write("\n".join(out) + "\n")
    return verdict


if __name__ == "__main__":
    main()
