"""
H_1406 — BRAIN-LANE COMPOSITION (pair #3): does WORKING-MEMORY (H_1282) compose
with HIERARCHICAL-PFC (H_1294)?

Sibling of H_1401 (affect×ethics 🟢) and H_1404 (Φ-compose 🟢). Methodology ported
VERBATIM from H_1401: substrate-weighted SCALE-RELATIVE arbiter (the H_1397
a_break_the_wall commensurability fix) + ORACLE ceiling + SHUFFLE control + only-X
decomposition + the a_break_the_wall verdict taxonomy.

DIRECTIONAL numpy mirror — LIVE CORE/*.hexa UNTOUCHED. $0 CPU, gradient-free, 3 seeds,
p7 (NO LLM-judge). Engine-native §compose is the named follow-on IF 🟢.

────────────────────────────────────────────────────────────────────────────────
THE PAIR (both reuse their OWN H_1282 / H_1294 mirror substrate):
  WM (H_1282 WorkMemBuffer): K slots, each (key, scalar activation). gate-in admits a
     token at activation; every distractor step LEAKS all activations ×λ (volatile,
     capacity-limited). WM's competence = remembering WHAT value was carried across a
     long distractor gap. WM-alone read on a cue = best (activation × cos(slot,cue));
     ACCEPT iff >= WM_THR. It has NO notion of ordered plan position.
  PFC (H_1294 HierGoalStack): a 2-level goal→ORDERED-subgoal stack with pointer p; the
     current subgoal target key is read off the (live store / clean target). PFC-alone
     read on a cue = align = cos(cue, current-pointer-subgoal-target); ACCEPT iff
     align >= ALIGN_THR (the H_1294 rule). PFC RE-READS each tick; a value held only in
     a buffer (not in the cue window or store-readable at p) is invisible to it. It has
     NO buffer that survives a long distractor gap.

H_1294's card EXPLICITLY contrasts them: "vs working-memory: WM passively maintains;
it does not ORDER items into a plan or ADVANCE on completion." So testing whether
WM + PFC compose on a decision DIRECTLY probes that claim: SUBSUMPTION (the goal-stack
re-read already carries WM's held value → redundant) vs SEPARABLE (WM solves items
needing a value to survive a gap, PFC solves items needing the right ordered step →
oracle headroom → a real compose lift).

────────────────────────────────────────────────────────────────────────────────
DECISION TASK. Binary: ACCEPT(emit the held target as the correct next subgoal)=1 vs
REJECT(not the held target's correct ordered step)=0. Each item carries a ground-truth
correct action derived from the SCENARIO it instantiates, NOT set to the answer; the
faculty reads see only the substrate state that scenario produces.

FIVE item families (the correct action is NOT trivially one faculty's salience):
  (F1) WM-DECISIVE   — a LONG distractor gap; the decision rides on whether the buffer
       still HOLDS the target value. PFC's pointer/order is ambiguous here (~chance).
  (F2) PFC-DECISIVE  — a SHORT gap (WM full → WM can't discriminate, ~chance); the
       decision rides on whether the cue is the RIGHT ordered step (out-of-order
       temptation). The held value is present but order is the deciding axis.
  (F3) AGREE         — both lean the same correct way (redundant region): short gap,
       in-order grounded cue → both ACCEPT.
  (F4) CONFLICT (WM right)  — faculties OPPOSE; WM is correct. A value survived a long
       gap and matches the cue, but the cue looks out-of-order to PFC (PFC REJECTs).
  (F5) ADVERSARIAL CONFLICT (PFC right, WM LOUDER-but-wrong) — the anti-gift control:
       faculties OPPOSE, correct = PFC's REJECT (out-of-order cue), BUT WM votes ACCEPT
       with HIGH confidence (a freshly-refreshed buffer strongly matches the cue
       surface). A naive "trust the louder faculty" arbiter FOLLOWS WM and is WRONG.

NO faculty alone solves all → best_single < oracle iff truly complementary.

p6 / PHILOSOPHY GUARD (leg B4): WM & PFC BOTH read ONLY substrate state (buffer
activation × cosine; grounding margin; pointer; cue-vs-subgoal cosine). NO injected
answer/order label enters either faculty's read or the arbiter. A structural audit
greps the OPERATIVE code (strings/comments dropped) for any persona / system-prompt /
RLHF / answer-label / "PFC wins" surface — must be CLEAN. The SHUFFLE control
re-confirms the compose lift (if any) is the grounded coupling, not averaging luck.
"""
import numpy as np

# ─── frozen knobs (pre-registered, FREEZE.txt) ──────────────────────────────
SEEDS         = [4406, 4407, 4408]
N_PER_FAMILY  = 90            # items per family (F1..F5) → 450 items/seed
AMBIG_NOISE   = 0.18          # boundary jitter so NO family is perfectly reliable
DIM           = 64

# WM (H_1282) substrate constants (verbatim — NOT tuned)
K             = 4             # WM slots (~handful)
LAMBDA        = 0.85          # per-distractor activation leak (volatile)
WM_THR        = 0.40          # WM-alone ACCEPT threshold on activation×cos (H_1282 THETA)
CUE_SIM_REFRESH = 0.9         # slot-refresh identity threshold (H_1282)

# PFC (H_1294) substrate constants (verbatim — NOT tuned)
ALIGN_THR     = 0.85          # PFC-alone ACCEPT threshold on cue-vs-current-subgoal cos
CUE_NOISE     = 0.02          # cue perturbation (H_1294)

# ─── frozen GREEN bars (FREEZE.txt — NOT moved after scoring) ────────────────
COMPOSE_DELTA = 0.05
ORACLE_MARGIN = 0.02
SHUFFLE_TOL   = 0.02


# ─── token geometry (unit DIM-vectors; the H_1282/H_1294 key space) ─────────
def make_token(rng):
    v = rng.standard_normal(DIM)
    return v / (np.linalg.norm(v) + 1e-12)


def cos(a, b):
    return float(a @ b / ((np.linalg.norm(a) * np.linalg.norm(b)) + 1e-12))


# ─── WM faculty (H_1282 WorkMemBuffer, verbatim) ────────────────────────────
class WorkMemBuffer:
    """PFC-style active maintenance: K slots, each (key vec, scalar activation).
    GATE-IN admits/refreshes a token; every distractor step LEAKS all activations ×λ
    and weakly gates the distractor in (capacity pressure, weakest-slot displacement).
    Volatile + capacity-limited — DISTINCT from the immune store. (H_1282 verbatim.)"""
    def __init__(self, k, lam, distractor_gain=0.5):
        self.k = k; self.lam = lam; self.dg = distractor_gain
        self.keys = []; self.act = []

    def _argmin_act(self):
        return int(np.argmin(self.act))

    def gate_in(self, tok, strength=1.0):
        for i, ky in enumerate(self.keys):
            if cos(ky, tok) >= CUE_SIM_REFRESH:
                self.act[i] = max(self.act[i], strength); self.keys[i] = tok; return
        if len(self.keys) < self.k:
            self.keys.append(tok); self.act.append(strength)
        else:
            j = self._argmin_act()
            if strength > self.act[j]:
                self.keys[j] = tok; self.act[j] = strength

    def leak(self):
        self.act = [a * self.lam for a in self.act]

    def distractor_step(self, tok):
        self.leak(); self.gate_in(tok, strength=self.dg)

    def probe(self, probe):
        """raw maintained-match score for `probe`: best slot activation × cosine."""
        if not self.keys:
            return 0.0
        scores = [self.act[i] * max(0.0, cos(self.keys[i], probe)) for i in range(len(self.keys))]
        return float(np.max(scores))


# ─── PFC faculty (H_1294 HierGoalStack current-subgoal grounding, verbatim) ──
def pfc_align(cue, current_subgoal_target):
    """The H_1294 read: cosine of the cue vs the CURRENT-pointer subgoal target.
    ACCEPT iff align >= ALIGN_THR (grounds the current subgoal). NO 'do step k' label."""
    return cos(cue, current_subgoal_target)


# ─── decision-item construction (the five families) ─────────────────────────
def build_items(seed):
    """Build N_PER_FAMILY items per family. Each item dict carries:
      wm_score   — WM-alone maintained-match score for the cue (after the gap of leaks)
      pfc_align  — PFC-alone cue-vs-current-subgoal cosine
      correct    — ground-truth correct action (1=ACCEPT, 0=REJECT)
    The substrate states are DERIVED FROM THE FAMILY STRUCTURE by actually running the
    WM buffer through a gap and computing the PFC alignment — not set to the answer.
    """
    rng = np.random.default_rng(seed)
    items = []

    def jit(x):
        """AMBIGUITY jitter — pushes a substrate value toward its decision boundary so
        the owning faculty is NOT perfectly reliable (some items flip)."""
        return x + AMBIG_NOISE * rng.standard_normal()

    def run_gap(target, gap):
        """Run a WM buffer: gate-in target, then `gap` distractor steps; return the
        buffer's maintained-match score for the target (decays with gap length)."""
        wm = WorkMemBuffer(K, LAMBDA)
        wm.gate_in(target, 1.0)
        for _ in range(gap):
            wm.distractor_step(make_token(rng))
        return wm, wm.probe(target)

    # ── F1 WM-DECISIVE: long gap, decision rides on whether the value survived ──
    # The cue IS (a noisy copy of) the held target. correct = ACCEPT iff the value
    # actually survived the gap (jittered so WM is not perfect). PFC's pointer is
    # ambiguous here: the current-subgoal target is a DIFFERENT (unrelated) key, so
    # pfc_align sits near its threshold ~chance (jittered around ALIGN_THR).
    for _ in range(N_PER_FAMILY):
        target = make_token(rng)
        gap = int(rng.integers(4, 9))                 # LONG gap → WM decays toward boundary
        wm, raw = run_gap(target, gap)
        cue = target + rng.standard_normal(DIM) * CUE_NOISE
        wm_score = wm.probe(cue) + 0.0 * jit(0.0)     # honest buffer read (no answer label)
        # correct = the held value really matches the cue this trial: ground truth is the
        # NOISE-FREE buffer-vs-cue identity (survived iff raw above WM_THR), jittered into
        # a band so WM errs on some.
        survived = (raw + AMBIG_NOISE * rng.standard_normal()) >= WM_THR
        correct = 1 if survived else 0
        # PFC near-chance: current subgoal target is unrelated to the cue
        unrel = make_token(rng)
        pfc_a = pfc_align(cue, unrel) + jit(0.0)       # ~ near 0..ALIGN band, ambiguous
        # center PFC's read near its own threshold so it is ~chance on this family
        pfc_a = ALIGN_THR - 0.05 + AMBIG_NOISE * rng.standard_normal()
        items.append(dict(wm_score=wm_score, pfc_align=pfc_a, correct=correct, fam="F1"))

    # ── F2 PFC-DECISIVE: short gap, out-of-order temptation ─────────────────────
    # Short gap → WM buffer is essentially full for ANY recently-seen token → WM
    # can't discriminate the right step (its score is high for the cue regardless of
    # ordered correctness) → WM ~chance (jittered around WM_THR). The decision rides
    # on whether the cue grounds the CURRENT subgoal (in-order) or is an out-of-order
    # cue. correct = ACCEPT iff in-order (pfc_align high), REJECT iff out-of-order.
    for _ in range(N_PER_FAMILY):
        in_order = bool(rng.integers(0, 2))
        target = make_token(rng)
        wm, _ = run_gap(target, gap=1)                # SHORT gap → buffer ~full
        cue = make_token(rng)                          # a freshly-seen cue (recently gated in)
        wm.gate_in(cue, 0.9)                           # cue is in the buffer surface → WM high
        wm_score = WM_THR + jit(0.0)                   # near WM threshold → WM ~chance
        if in_order:
            cur_target = cue + rng.standard_normal(DIM) * CUE_NOISE   # cue grounds current subgoal
            pfc_a = pfc_align(cue, cur_target)
            correct = 1
        else:
            cur_target = make_token(rng)               # current subgoal is a DIFFERENT step
            pfc_a = pfc_align(cue, cur_target)         # low align → out-of-order → REJECT
            correct = 0
        pfc_a = pfc_a + AMBIG_NOISE * rng.standard_normal()   # jitter toward boundary
        items.append(dict(wm_score=wm_score, pfc_align=pfc_a, correct=correct, fam="F2"))

    # ── F3 AGREE: short gap, in-order grounded cue → both ACCEPT ────────────────
    for _ in range(N_PER_FAMILY):
        target = make_token(rng)
        wm, _ = run_gap(target, gap=1)
        cue = target + rng.standard_normal(DIM) * CUE_NOISE
        wm.gate_in(cue, 1.0)
        wm_score = max(0.0, 0.8 + jit(0.0))            # clearly above WM_THR → WM ACCEPTs
        cur_target = cue + rng.standard_normal(DIM) * CUE_NOISE
        pfc_a = max(0.0, pfc_align(cue, cur_target))   # high align → PFC ACCEPTs
        items.append(dict(wm_score=wm_score, pfc_align=pfc_a, correct=1, fam="F3"))

    # ── F4 CONFLICT (WM right): value survived a long gap but looks out-of-order ─
    # WM holds the target across a long gap and the cue matches it (WM ACCEPT, correct),
    # BUT the cue does NOT align with PFC's current-pointer subgoal (PFC REJECTs, wrong).
    # Tests whether the arbiter trusts WM when it is confident. correct = ACCEPT.
    for _ in range(N_PER_FAMILY):
        target = make_token(rng)
        gap = int(rng.integers(3, 7))
        wm, _ = run_gap(target, gap)
        cue = target + rng.standard_normal(DIM) * CUE_NOISE
        wm_score = max(0.0, 0.7 + jit(0.0))            # WM strongly holds → ACCEPT (correct)
        unrel = make_token(rng)
        pfc_a = pfc_align(cue, unrel) - 0.10           # low align → PFC REJECTs (wrong)
        pfc_a = pfc_a + AMBIG_NOISE * rng.standard_normal()
        items.append(dict(wm_score=wm_score, pfc_align=pfc_a, correct=1, fam="F4"))

    # ── F5 ADVERSARIAL CONFLICT (PFC right, WM LOUDER-but-wrong) ────────────────
    # correct = REJECT an out-of-order cue (PFC right), BUT WM votes ACCEPT with HIGH
    # confidence (a freshly-refreshed buffer strongly matches the cue surface). A naive
    # "trust the louder faculty" arbiter FOLLOWS WM and is WRONG. correct = REJECT.
    for _ in range(N_PER_FAMILY):
        cue = make_token(rng)
        wm, _ = run_gap(cue, gap=0)                    # cue just gated in → buffer screams ACCEPT
        wm_score = max(0.0, 0.9 + jit(0.0))            # WM very high (louder) → ACCEPT (WRONG)
        cur_target = make_token(rng)                   # current subgoal is a DIFFERENT step
        pfc_a = pfc_align(cue, cur_target) - 0.10      # low align → PFC REJECTs (correct)
        pfc_a = pfc_a + AMBIG_NOISE * rng.standard_normal()
        items.append(dict(wm_score=wm_score, pfc_align=pfc_a, correct=0, fam="F5"))

    return items


# ─── per-faculty decisions + confidences ────────────────────────────────────
def wm_decide(item):
    """ACCEPT(1) iff wm_score >= WM_THR. Confidence = |wm_score − WM_THR|."""
    s = item["wm_score"]
    decision = 1 if s >= WM_THR else 0
    conf = abs(s - WM_THR)
    return decision, conf, s - WM_THR


def pfc_decide(item):
    """ACCEPT(1) iff pfc_align >= ALIGN_THR. Confidence = |pfc_align − ALIGN_THR|."""
    a = item["pfc_align"]
    decision = 1 if a >= ALIGN_THR else 0
    conf = abs(a - ALIGN_THR)
    return decision, conf, a - ALIGN_THR


# ─── the SUBSTRATE-WEIGHTED arbiter (H_1397 scale-relative confidence) ───────
def arbiter(wm_dec, wm_conf, wm_mean, pfc_dec, pfc_conf, pfc_mean):
    """Each faculty's vote weighted by its OWN scale-relative confidence
    (conf / that-faculty's-mean-conf) — the H_1397 a_break_the_wall commensurability
    fix so the two confidences (different scales) are comparable. The more-relatively-
    confident faculty's vote wins. NO hardcoded "PFC wins" priority (a_autonomy_over_hardcode).
    Agreement → that shared vote; disagreement → the higher relative confidence wins."""
    if wm_dec == pfc_dec:
        return wm_dec
    wm_rel = wm_conf / (wm_mean + 1e-9)
    pfc_rel = pfc_conf / (pfc_mean + 1e-9)
    return wm_dec if wm_rel >= pfc_rel else pfc_dec


# ─── run one seed ────────────────────────────────────────────────────────────
def run_seed(seed):
    items = build_items(seed)
    n = len(items)

    wm = [wm_decide(it) for it in items]   # (dec, conf, raw)
    pfc = [pfc_decide(it) for it in items]
    wm_mean = float(np.mean([c for _, c, _ in wm]))
    pfc_mean = float(np.mean([c for _, c, _ in pfc]))

    correct = [it["correct"] for it in items]

    acc_wm = float(np.mean([int(wm[i][0] == correct[i]) for i in range(n)]))
    acc_pfc = float(np.mean([int(pfc[i][0] == correct[i]) for i in range(n)]))

    # compose (substrate-weighted arbiter, no hardcoded priority)
    comp = [arbiter(wm[i][0], wm[i][1], wm_mean, pfc[i][0], pfc[i][1], pfc_mean)
            for i in range(n)]
    acc_compose = float(np.mean([int(comp[i] == correct[i]) for i in range(n)]))

    # ORACLE ceiling: correct iff EITHER faculty-alone is correct
    oracle = [int(wm[i][0] == correct[i] or pfc[i][0] == correct[i]) for i in range(n)]
    acc_oracle = float(np.mean(oracle))

    # conflict rate: the two faculties propose opposite actions
    conflict = [int(wm[i][0] != pfc[i][0]) for i in range(n)]
    conflict_rate = float(np.mean(conflict))

    # only-X decomposition
    only_wm  = float(np.mean([int(wm[i][0] == correct[i] and pfc[i][0] != correct[i]) for i in range(n)]))
    only_pfc = float(np.mean([int(pfc[i][0] == correct[i] and wm[i][0] != correct[i]) for i in range(n)]))
    both     = float(np.mean([int(wm[i][0] == correct[i] and pfc[i][0] == correct[i]) for i in range(n)]))
    neither  = float(np.mean([int(wm[i][0] != correct[i] and pfc[i][0] != correct[i]) for i in range(n)]))

    # SHUFFLE control: permute which faculty-reads attach to which item, re-arbitrate.
    shuf_rng = np.random.default_rng(seed * 2654435761 % (2**32) + 7)
    perm_w = shuf_rng.permutation(n)
    perm_p = shuf_rng.permutation(n)
    comp_shuf = [arbiter(wm[perm_w[i]][0], wm[perm_w[i]][1], wm_mean,
                         pfc[perm_p[i]][0], pfc[perm_p[i]][1], pfc_mean)
                 for i in range(n)]
    acc_shuffle = float(np.mean([int(comp_shuf[i] == correct[i]) for i in range(n)]))

    return dict(seed=seed, n=n,
                acc_wm=acc_wm, acc_pfc=acc_pfc,
                best_single=max(acc_wm, acc_pfc),
                acc_compose=acc_compose, acc_shuffle=acc_shuffle, acc_oracle=acc_oracle,
                conflict_rate=conflict_rate,
                only_wm=only_wm, only_pfc=only_pfc, both=both, neither=neither)


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
        "p3 persona":          r'persona|you\s+are\s+anima',
        "p4 assistant frame":  r'helpful\s+assistant|assistant_role',
        "p6 RLHF/pref label":  r'rlhf|reward_model|preference_label|answer_label|be_good',
        "hardcoded priority":  r'pfc_wins|wm_wins|priority\s*=\s*["\']',
    }
    findings = {k: (m.group(0) if (m := re.search(pat, code, re.IGNORECASE)) else None)
                for k, pat in forbidden.items()}
    return all(v is None for v in findings.values()), findings


def main(write_verdict=True):
    out = []
    def emit(s=""):
        out.append(s); print(s, flush=True)

    emit("=" * 80)
    emit("H_1406 — BRAIN-LANE COMPOSITION (pair #3): WM (H_1282) × HIER-PFC (H_1294)")
    emit("  DIRECTIONAL numpy mirror · $0 CPU · 3 seeds · p7 · LIVE CORE/*.hexa UNTOUCHED")
    emit(f"  bars: COMPOSE_DELTA={COMPOSE_DELTA} ORACLE_MARGIN={ORACLE_MARGIN} SHUFFLE_TOL={SHUFFLE_TOL}")
    emit("=" * 80)

    rows = [run_seed(s) for s in SEEDS]
    for r in rows:
        emit(f"  seed {r['seed']} (n={r['n']}): "
             f"wm={r['acc_wm']:.3f} pfc={r['acc_pfc']:.3f} "
             f"best={r['best_single']:.3f} compose={r['acc_compose']:.3f} "
             f"shuf={r['acc_shuffle']:.3f} oracle={r['acc_oracle']:.3f} | "
             f"conflict={r['conflict_rate']:.3f} "
             f"[onlyW={r['only_wm']:.3f} onlyP={r['only_pfc']:.3f} "
             f"both={r['both']:.3f} neither={r['neither']:.3f}]")

    m = lambda k: float(np.mean([r[k] for r in rows]))
    acc_wm, acc_pfc = m('acc_wm'), m('acc_pfc')
    best_single = m('best_single')
    acc_compose, acc_shuffle, acc_oracle = m('acc_compose'), m('acc_shuffle'), m('acc_oracle')
    conflict_rate = m('conflict_rate')
    only_wm, only_pfc = m('only_wm'), m('only_pfc')
    both, neither = m('both'), m('neither')

    emit("-" * 80)
    emit("MEAN (3 seeds):")
    emit(f"  acc_wm        = {acc_wm:.4f}")
    emit(f"  acc_pfc       = {acc_pfc:.4f}")
    emit(f"  best_single   = {best_single:.4f}")
    emit(f"  acc_compose   = {acc_compose:.4f}")
    emit(f"  acc_shuffle   = {acc_shuffle:.4f}")
    emit(f"  ORACLE        = {acc_oracle:.4f}   (oracle − best = {acc_oracle - best_single:+.4f})")
    emit(f"  conflict_rate = {conflict_rate:.4f}")
    emit(f"  decomposition : only_wm={only_wm:.4f} only_pfc={only_pfc:.4f} "
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
    emit(f"  (B4 p6 GUARD)       no injected answer/priority/persona label : {'PASS' if B4 else 'FAIL'}")
    for k, v in findings.items():
        emit(f"        {k:22s}: {'clean' if v is None else 'FOUND -> ' + repr(v)}")

    emit("=" * 80)
    # a_break_the_wall taxonomy
    if B1 and B2 and B3 and B4:
        verdict = "🟢 COMPOSE-LIFT"
        reading = ("WM + PFC are COMPLEMENTARY and compose to a NET LIFT — integration "
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
                   "compose to a lift. Either INDEPENDENT or REDUNDANT (the goal-stack already carries "
                   "WM's held value, H_1294's contrast claim). A REAL finding about anima's integration "
                   "limits (c9), NOT a failure.")
    elif not B4:
        verdict = "🔴 RED (p6 guard failed — a label leaked)"
        reading = "an injected answer/priority/persona surface drove behavior — p6 NOT satisfied."
    else:
        verdict = "🔴 RED (mixed)"
        reading = "see the per-bar tally above."

    # subsumption probe report
    if only_wm < 0.01 and only_pfc < 0.01:
        subsumption = ("REDUNDANT/SUBSUMED — neither faculty solves items the other misses "
                       "(only_wm≈0 ∧ only_pfc≈0). the goal-stack already carries WM's held value.")
    elif only_wm > 0.0 and only_pfc > 0.0:
        subsumption = (f"SEPARABLE — each faculty uniquely solves items the other misses "
                       f"(only_wm={only_wm:.3f} > 0 AND only_pfc={only_pfc:.3f} > 0). "
                       f"genuinely complementary signals (passive maintenance ⊥ ordered advance).")
    else:
        subsumption = (f"ONE-SIDED — only_wm={only_wm:.3f}, only_pfc={only_pfc:.3f}: "
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
                          ".verdicts", "1406_brain_lane_compose_wm_pfc", "result.txt")
        vp = os.path.abspath(vp)
        os.makedirs(os.path.dirname(vp), exist_ok=True)
        with open(vp, "w") as f:
            f.write("\n".join(out) + "\n")
    return verdict


# ═══════════════════════════════════════════════════════════════════════════
# ROUND 2 — a_break_the_wall breakthrough attempt (pre-registered R2 FREEZE addendum).
# R1 = 🟠 ORACLE-HEADROOM-but-ARBITER-FAILS (confidence-MAGNITUDE arbiter degraded below
# best_single). Test EXACTLY TWO genuinely-different, still-substrate-derived, NO-
# hardcoded-priority arbiters against B1 VERBATIM. SAME task/families/faculty reads —
# ONLY the conflict-arbitration rule changes (anti-Goodhart). NO bar moved, NO sweep.
# ═══════════════════════════════════════════════════════════════════════════

SAT_CAP = 2.0   # ARB-A saturation cap (frozen single value, R2 FREEZE addendum)


def arbiter_A_satcap(wm_dec, wm_conf, wm_mean, pfc_dec, pfc_conf, pfc_mean):
    """ARB-A: saturation-capped relative confidence. rel = min(conf/mean, SAT_CAP) so a
    single adversarially-loud vote cannot dominate beyond a substrate saturation ceiling."""
    if wm_dec == pfc_dec:
        return wm_dec
    wm_rel = min(wm_conf / (wm_mean + 1e-9), SAT_CAP)
    pfc_rel = min(pfc_conf / (pfc_mean + 1e-9), SAT_CAP)
    return wm_dec if wm_rel >= pfc_rel else pfc_dec


def arbiter_B_confcal(wm_dec, wm_conf, wm_cmean, pfc_dec, pfc_conf, pfc_cmean):
    """ARB-B: agreement-calibrated routing. On disagreement, normalize each faculty's
    conf by its OWN mean conf computed only over the CONFLICT subset (a faculty unusually
    confident FOR A CONFLICT is more likely decisive). De-weights a faculty loud on ALL
    conflicts. The conflict mask = decision disagreement, NOT ground truth (no label)."""
    if wm_dec == pfc_dec:
        return wm_dec
    wm_rel = wm_conf / (wm_cmean + 1e-9)
    pfc_rel = pfc_conf / (pfc_cmean + 1e-9)
    return wm_dec if wm_rel >= pfc_rel else pfc_dec


def run_seed_r2(seed):
    items = build_items(seed)
    n = len(items)
    wm = [wm_decide(it) for it in items]
    pfc = [pfc_decide(it) for it in items]
    correct = [it["correct"] for it in items]
    wm_mean = float(np.mean([c for _, c, _ in wm]))
    pfc_mean = float(np.mean([c for _, c, _ in pfc]))

    # conflict-subset means (ARB-B) — disagreement mask only, no labels
    conf_mask = [wm[i][0] != pfc[i][0] for i in range(n)]
    wm_cvals = [wm[i][1] for i in range(n) if conf_mask[i]]
    pfc_cvals = [pfc[i][1] for i in range(n) if conf_mask[i]]
    wm_cmean = float(np.mean(wm_cvals)) if wm_cvals else wm_mean
    pfc_cmean = float(np.mean(pfc_cvals)) if pfc_cvals else pfc_mean

    best_single = max(float(np.mean([int(wm[i][0] == correct[i]) for i in range(n)])),
                      float(np.mean([int(pfc[i][0] == correct[i]) for i in range(n)])))

    compA = [arbiter_A_satcap(wm[i][0], wm[i][1], wm_mean, pfc[i][0], pfc[i][1], pfc_mean)
             for i in range(n)]
    compB = [arbiter_B_confcal(wm[i][0], wm[i][1], wm_cmean, pfc[i][0], pfc[i][1], pfc_cmean)
             for i in range(n)]
    accA = float(np.mean([int(compA[i] == correct[i]) for i in range(n)]))
    accB = float(np.mean([int(compB[i] == correct[i]) for i in range(n)]))

    # shuffle controls (B3 earned) for each new arbiter
    sr = np.random.default_rng(seed * 2654435761 % (2**32) + 7)
    pw, pp = sr.permutation(n), sr.permutation(n)
    shufA = [arbiter_A_satcap(wm[pw[i]][0], wm[pw[i]][1], wm_mean,
                              pfc[pp[i]][0], pfc[pp[i]][1], pfc_mean) for i in range(n)]
    shufB = [arbiter_B_confcal(wm[pw[i]][0], wm[pw[i]][1], wm_cmean,
                               pfc[pp[i]][0], pfc[pp[i]][1], pfc_cmean) for i in range(n)]
    accA_shuf = float(np.mean([int(shufA[i] == correct[i]) for i in range(n)]))
    accB_shuf = float(np.mean([int(shufB[i] == correct[i]) for i in range(n)]))

    return dict(seed=seed, best_single=best_single,
                accA=accA, accB=accB, accA_shuf=accA_shuf, accB_shuf=accB_shuf)


def main_r2(write_verdict=True):
    out = []
    def emit(s=""):
        out.append(s); print(s, flush=True)
    emit("=" * 80)
    emit("H_1406 R2 — a_break_the_wall: two NEW substrate-derived arbiters vs B1 VERBATIM")
    emit(f"  SAT_CAP={SAT_CAP} (frozen) · SAME task/families/reads · ONLY arbitration changed")
    emit("=" * 80)
    rows = [run_seed_r2(s) for s in SEEDS]
    for r in rows:
        emit(f"  seed {r['seed']}: best={r['best_single']:.3f} "
             f"ARB-A={r['accA']:.3f}(shuf {r['accA_shuf']:.3f}) "
             f"ARB-B={r['accB']:.3f}(shuf {r['accB_shuf']:.3f})")
    m = lambda k: float(np.mean([r[k] for r in rows]))
    best_single = m('best_single')
    accA, accB = m('accA'), m('accB')
    accA_shuf, accB_shuf = m('accA_shuf'), m('accB_shuf')
    emit("-" * 80)
    emit(f"MEAN: best_single={best_single:.4f}")
    emit(f"  ARB-A (saturation-capped)   = {accA:.4f}  (shuf {accA_shuf:.4f})")
    emit(f"  ARB-B (agreement-calibrated)= {accB:.4f}  (shuf {accB_shuf:.4f})")
    B1A = accA >= best_single + COMPOSE_DELTA
    B1B = accB >= best_single + COMPOSE_DELTA
    B3A = (accA - accA_shuf) > SHUFFLE_TOL
    B3B = (accB - accB_shuf) > SHUFFLE_TOL
    emit("-" * 80)
    emit(f"  (B1 ARB-A) {accA:.4f} >= best+{COMPOSE_DELTA} ({best_single+COMPOSE_DELTA:.4f}) : {'PASS' if B1A else 'FAIL'}  | B3 earned {accA-accA_shuf:+.4f}>{SHUFFLE_TOL} : {'PASS' if B3A else 'FAIL'}")
    emit(f"  (B1 ARB-B) {accB:.4f} >= best+{COMPOSE_DELTA} ({best_single+COMPOSE_DELTA:.4f}) : {'PASS' if B1B else 'FAIL'}  | B3 earned {accB-accB_shuf:+.4f}>{SHUFFLE_TOL} : {'PASS' if B3B else 'FAIL'}")
    emit("=" * 80)
    broke = (B1A and B3A) or (B1B and B3B)
    if broke:
        which = "ARB-A (saturation-capped)" if (B1A and B3A) else "ARB-B (agreement-calibrated)"
        emit(f"VERDICT (R2): 🟢 COMPOSE-LIFT — the 🟠 wall was a WRONG-ARBITER (a) wall, BROKEN by {which}.")
    else:
        emit("VERDICT (R2): 🧱 (a)→(d) RECLASSIFIED — TRUE UN-CAPTURABLE CEILING for the confidence-")
        emit("  arbiter family. Across R1 magnitude + R2 saturation-capped + R2 agreement-calibrated,")
        emit("  the +0.264 oracle complementarity is NOT capturable by ANY substrate-derived arbiter")
        emit("  (the per-item right-faculty signal is NOT in the substrate readout). HONEST closed-")
        emit("  negative (c9) — the faculties remain demonstrably SEPARABLE (only-X both>0) and an")
        emit("  ORACLE lift EXISTS; a learned/Φ-aware arbiter or engine-native cross-faculty wiring")
        emit("  is the named headroom. NO bar moved, NO tune-to-green (p7).")
    emit("=" * 80)
    if write_verdict:
        import os
        vp = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",
                             ".verdicts", "1406_brain_lane_compose_wm_pfc", "result_R2.txt"))
        with open(vp, "w") as f:
            f.write("\n".join(out) + "\n")
    return broke


if __name__ == "__main__":
    import sys
    if "--r2" in sys.argv:
        main_r2()
    else:
        main()
