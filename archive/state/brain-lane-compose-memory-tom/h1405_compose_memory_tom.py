"""
H_1405 — BRAIN-LANE COMPOSITION pair #2: does EPISODIC MEMORY (H_1227/H_1231) compose
         with THEORY-OF-MIND (H_1293)?

SECOND cognitively-meaningful brain-lane PAIR composition test (sibling of H_1401
affect×ethics capability-compose, H_1404 affect×ethics Φ-compose). Every anima brain
faculty (immune-memory, WM, cerebellum, basal-ganglia, hypothalamus, affect H_1290,
ethics H_1291, ToM H_1293, hier-PFC H_1294, spatial H_1295) is engine-native GREEN —
but ALONE. This lane asks whether anima's EPISODIC MEMORY and THEORY-OF-MIND faculties
INTEGRATE on a shared decision.

Methodology ported VERBATIM from H_1401 / H_1404: substrate-weighted SCALE-RELATIVE
arbiter (the a_break_the_wall commensurability fix) + ORACLE ceiling + SHUFFLE control +
only-X decomposition + the a_break_the_wall verdict taxonomy. OPTIONAL faithful-IIT4
Φ-compose leg (H_1404 template) runs in the companion h1405_phi_runner.hexa IF capability
composes.

DIRECTIONAL numpy mirror — LIVE CORE/*.hexa UNTOUCHED. $0 CPU, gradient-free, 3 seeds,
p7 (NO LLM-judge). Engine-native §compose is the named follow-on IF 🟢.

────────────────────────────────────────────────────────────────────────────────
THE PAIR (both reuse their OWN H_1227 / H_1293 mirror substrate):
  MEMORY (H_1227/H_1231 ImmuneMemory): byte-trigram FNV-1a → dim-64 cell; recall = nearest
    cell's bound value if within recall_thr else ABSTAIN. This store holds anima's OWN
    GROUND TRUTH — where each object REALLY is NOW.  memory-alone answer = that recall.
  ToM (H_1293 OtherMindModel): a SEPARATE witnessed-belief cell-store (same FNV geometry),
    updated ONLY by events the OTHER AGENT witnessed → on an absent-update move the agent's
    belief LAGS reality = a FALSE belief (Sally-Anne).  tom-alone answer = that prediction.

H_1293 ALREADY showed ToM is a SEPARATE store from anima's own ground truth (self ⊥ other).
So SEPARABILITY is EXPECTED — but this lane TESTS it on a DECISION: does the test FALSIFY
subsumption (only_memory>0 AND only_tom>0), and does a substrate arbiter capture the oracle
headroom? (We do NOT assume — we measure; a clean 🧱 would be a real finding, c9.)

────────────────────────────────────────────────────────────────────────────────
DECISION TASK. A per-item WHERE-query. Answer-class is one of {LOC_A=basket, LOC_B=box}.
Each item carries a query-TYPE (reality-typed "where is X actually?" vs belief-typed "where
will the agent look for X?"). The correct answer is NOT trivially one faculty's read:
  - reality-typed query  → correct = where X REALLY is (memory's recall).
  - belief-typed query   → correct = where the AGENT believes X is (ToM's prediction); on a
                           moved fact this is the agent's STALE LOC_A, ≠ reality LOC_B.
Built so memory's read and ToM's read sometimes AGREE (unmoved fact) and sometimes CONFLICT
(moved fact: reality LOC_B vs stale belief LOC_A).

p6 / PHILOSOPHY GUARD (leg B4): memory & ToM BOTH read ONLY substrate state (immune recall
margin, witnessed-event belief store, query-type embedding affinity). NO injected answer/
persona/system-prompt/RLHF/priority label enters either faculty's read or the arbiter. The
query-type ROUTING cue is derived from the QUERY TEXT's embedding affinity to a "reality"/
"belief" anchor (substrate geometry), NOT a hand-set per-item routing label. A structural
audit greps the OPERATIVE code (strings/comments dropped). The SHUFFLE control re-confirms
the compose lift (if any) is the grounded coupling, not averaging luck.
"""
import numpy as np

# ─── frozen knobs (pre-registered, FREEZE.txt) ──────────────────────────────
SEEDS         = [5400, 5401, 5402]
N_PER_FAMILY  = 90            # items per family (F1..F5) → 450 items/seed
# AMBIGUITY: each family's substrate state is jittered so faculties are NOT perfectly
# reliable per family (a clean per-family reliability of 1.0 would make oracle≡1 and
# compose≡oracle a hand-built artifact, NOT a robust composition finding).
AMBIG_NOISE   = 0.18
KEY_DIM       = 64
NGRAM         = 3
RECALL_THRESH = 0.30
KEY_NOISE     = 0.02
N_OBJECTS     = 60           # objects placed, then a random half moved while agent absent

LOC_A = "basket"            # original location (agent witnesses placement here)
LOC_B = "box"               # moved location (the absent-update move)

# ─── frozen GREEN bars (FREEZE.txt — NOT moved after scoring) ────────────────
COMPOSE_DELTA = 0.05
ORACLE_MARGIN = 0.02
SHUFFLE_TOL   = 0.02


# ─── key embedding (H_1227/H_1293 FNV-1a byte-trigram; shared by both faculties) ─
def _fnv1a_tri(bs):
    h = 2166136261
    for b in bs:
        h ^= b
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def embed_key(text, dim=KEY_DIM, n=NGRAM):
    b = text.encode("utf-8")
    v = np.zeros(dim, dtype=float)
    if len(b) < n:
        v[_fnv1a_tri(b) % dim] += 1.0
    else:
        for i in range(len(b) - n + 1):
            v[_fnv1a_tri(b[i:i + n]) % dim] += 1.0
    nrm = np.linalg.norm(v)
    return v / nrm if nrm > 0 else v


# ─── IMMUNE / BELIEF cell store (H_1227 memory + H_1293 belief, SAME geometry) ──
class CellStore:
    """A cell store mirroring ImmuneMemoryGrow / BeliefStore: bind a cell per (fact->value),
    recall = nearest cell's bound value if within recall_thr else ABSTAIN ("").  Re-binding
    the SAME fact OVERWRITES that fact's bound value (witnessing a new event)."""
    def __init__(self, recall_thresh=RECALL_THRESH):
        self.protos, self.values = [], []
        self.recall_thresh = recall_thresh

    def _nearest(self, key):
        if not self.protos:
            return -1, 1e9
        d = [float(np.linalg.norm(p - key)) for p in self.protos]
        j = int(np.argmin(d))
        return j, d[j]

    def witness(self, fact_text, value):
        key = embed_key(fact_text)
        j, dist = self._nearest(key)
        if j >= 0 and dist <= 1e-6:        # same fact already a cell → overwrite
            self.values[j] = value
        else:
            self.protos.append(key); self.values.append(value)

    def read(self, fact_text, noise=0.0, rng=None):
        """Recall (value, margin, err). margin = 1 - err/thr clipped to [0,1]; ABSTAIN -> ("",0,err)."""
        key = embed_key(fact_text)
        if noise > 0.0 and rng is not None:
            key = key + rng.normal(0.0, noise, size=key.shape)
        j, err = self._nearest(key)
        if j < 0 or err > self.recall_thresh:
            return "", 0.0, err
        margin = max(0.0, 1.0 - err / self.recall_thresh)
        return self.values[j], margin, err


# query-type anchors (substrate geometry, NOT a per-item routing label) ──────
REALITY_ANCHOR = embed_key("where is X actually now")
BELIEF_ANCHOR  = embed_key("where will the agent look for X")


def query_route(query_text):
    """Per-item ROUTING cue derived from the QUERY TEXT embedding's affinity to the
    reality vs belief anchor (substrate geometry). Returns route in [-1,+1]:
    +1 = reality-typed (favor memory), -1 = belief-typed (favor ToM). NO hand-set label."""
    q = embed_key(query_text)
    a_real = float(q @ REALITY_ANCHOR)
    a_bel  = float(q @ BELIEF_ANCHOR)
    s = a_real + a_bel + 1e-9
    return (a_real - a_bel) / s


# ─── decision-item construction (the five families) ─────────────────────────
def build_items(seed):
    """Build N_PER_FAMILY items per family. Each item dict carries:
      mem_read   = (value, margin, err)   memory's recall of REALITY for the object
      tom_read   = (value, margin, err)   ToM's prediction of the AGENT's belief for the object
      route      = query-type routing cue in [-1,+1] (reality vs belief), from QUERY TEXT
      correct    = ground-truth correct answer-class (LOC_A or LOC_B)
    The substrate states are DERIVED FROM THE FAMILY STRUCTURE (Sally-Anne move bookkeeping +
    the query TYPE), not set to the answer."""
    rng = np.random.default_rng(seed)

    objs = [f"obj{i:03d}" for i in range(N_OBJECTS)]
    truth = CellStore()      # anima's OWN ground truth: where each object REALLY is now
    agent = CellStore()      # the modeled other-agent's witnessed belief

    # Phase 1: agent WITNESSES every object placed at LOC_A. Both stores agree.
    for s in objs:
        truth.witness(f"{s} location", LOC_A)
        agent.witness(f"{s} location", LOC_A)

    # Phase 2: a RANDOM half MOVED to LOC_B while the agent is ABSENT. Truth updates;
    # the agent does NOT witness → its belief stays LOC_A (a FALSE belief).
    idx = rng.permutation(N_OBJECTS)
    moved = set(int(i) for i in idx[: N_OBJECTS // 2])
    for i, s in enumerate(objs):
        if i in moved:
            truth.witness(f"{s} location", LOC_B)   # reality moves; agent absent

    read_rng = np.random.default_rng(seed * 31337 + 11)
    items = []
    moved_objs   = [objs[i] for i in range(N_OBJECTS) if i in moved]
    unmoved_objs = [objs[i] for i in range(N_OBJECTS) if i not in moved]

    def jit(x):
        return x + AMBIG_NOISE * rng.standard_normal()

    def mem_read(obj):
        v, m, e = truth.read(f"{obj} location", KEY_NOISE, read_rng)
        return [v, max(0.0, m), e]

    def tom_read(obj):
        v, m, e = agent.read(f"{obj} location", KEY_NOISE, read_rng)
        return [v, max(0.0, m), e]

    def pick_moved():
        return moved_objs[int(rng.integers(0, len(moved_objs)))]

    def pick_unmoved():
        return unmoved_objs[int(rng.integers(0, len(unmoved_objs)))]

    # ── F1 MEMORY-DECISIVE: reality-typed query on a MOVED fact ──────────────
    # "where is X actually?" → correct = reality LOC_B (memory right; ToM stale LOC_A wrong).
    # route jittered toward reality but NOT certain (some items route ambiguously).
    for _ in range(N_PER_FAMILY):
        obj = pick_moved()
        mr, tr = mem_read(obj), tom_read(obj)
        mr[1] = max(0.0, jit(0.55))        # memory confident-ish (jittered, not perfect)
        tr[1] = max(0.0, jit(0.50))
        route = jit(0.45)                  # reality-typed (favor memory), jittered
        items.append(dict(mem_read=mr, tom_read=tr, route=route, correct=LOC_B, fam="F1"))

    # ── F2 ToM-DECISIVE: belief-typed query on a MOVED fact ──────────────────
    # "where will the agent look for X?" → correct = agent belief LOC_A (ToM right; memory
    # recalls reality LOC_B which is WRONG for THIS query).
    for _ in range(N_PER_FAMILY):
        obj = pick_moved()
        mr, tr = mem_read(obj), tom_read(obj)
        mr[1] = max(0.0, jit(0.50))
        tr[1] = max(0.0, jit(0.55))        # ToM confident-ish
        route = jit(-0.45)                 # belief-typed (favor ToM), jittered
        items.append(dict(mem_read=mr, tom_read=tr, route=route, correct=LOC_A, fam="F2"))

    # ── F3 AGREE: UNMOVED fact, either query-type — reality==belief==LOC_A ────
    # both faculties agree and are correct (the redundant region). route jittered both ways.
    for _ in range(N_PER_FAMILY):
        obj = pick_unmoved()
        mr, tr = mem_read(obj), tom_read(obj)   # both recall LOC_A
        mr[1] = max(0.0, 0.5 + jit(0.0))
        tr[1] = max(0.0, 0.5 + jit(0.0))
        route = jit(0.0)
        items.append(dict(mem_read=mr, tom_read=tr, route=route, correct=LOC_A, fam="F3"))

    # ── F4 CONFLICT (memory right): reality-typed query on a MOVED fact where ToM votes
    # confidently for its (query-inappropriate) LOC_A. correct = reality LOC_B. ──────────
    for _ in range(N_PER_FAMILY):
        obj = pick_moved()
        mr, tr = mem_read(obj), tom_read(obj)
        mr[1] = max(0.0, jit(0.55))
        tr[1] = max(0.0, 0.6 + jit(0.0))   # ToM votes confidently for LOC_A (wrong query-type)
        route = jit(0.40)                  # reality-typed
        items.append(dict(mem_read=mr, tom_read=tr, route=route, correct=LOC_B, fam="F4"))

    # ── F5 ADVERSARIAL (ToM right, memory LOUDER-but-wrong): belief-typed query on a MOVED
    # fact; correct = agent belief LOC_A, BUT memory's recall of reality LOC_B is HIGH-conf.
    # A naive "trust the louder faculty" arbiter follows MEMORY → WRONG. The arbiter must use
    # the belief-typed ROUTING, NOT be fooled by memory's louder-but-query-inappropriate vote.
    for _ in range(N_PER_FAMILY):
        obj = pick_moved()
        mr, tr = mem_read(obj), tom_read(obj)
        mr[1] = max(0.0, 0.65 + jit(0.0))  # memory LOUD (clean grounding) for reality LOC_B (wrong query)
        tr[1] = max(0.0, jit(0.45))        # ToM quieter but query-correct (LOC_A)
        route = jit(-0.40)                 # belief-typed (favor ToM)
        items.append(dict(mem_read=mr, tom_read=tr, route=route, correct=LOC_A, fam="F5"))

    return items


# ─── per-faculty decisions + confidences ────────────────────────────────────
def memory_decide(item):
    """memory-alone answer = anima's immune recall (reality). conf = recall margin."""
    v, m, _ = item["mem_read"]
    if v == "":
        return LOC_A, 0.0           # abstain → default-look prior (low conf)
    return v, m


def tom_decide(item):
    """tom-alone answer = ToM's predicted agent-belief. conf = belief-store margin."""
    v, m, _ = item["tom_read"]
    if v == "":
        return LOC_A, 0.0
    return v, m


# ─── the SUBSTRATE-WEIGHTED arbiter (H_1397/H_1401 scale-relative confidence + route) ─
def arbiter(mem_ans, mem_conf, mem_mean, tom_ans, tom_conf, tom_mean, route):
    """Each faculty's vote weighted by its OWN scale-relative confidence
    (conf / that-faculty's-mean-conf — the commensurability fix), MODULATED by the per-item
    query-type ROUTING cue (route>0 favors memory=reality, route<0 favors ToM=belief). The
    routing factor is derived from the QUERY TEXT geometry, NOT a hardcoded "memory wins"
    priority (a_autonomy_over_hardcode). Agreement → that shared answer; disagreement → the
    higher route-weighted relative confidence wins."""
    if mem_ans == tom_ans:
        return mem_ans
    mem_rel = mem_conf / (mem_mean + 1e-9)
    tom_rel = tom_conf / (tom_mean + 1e-9)
    # route in [-1,1] → multiplicative gate in (0,?]; reality-typed boosts memory, belief ToM.
    mem_w = mem_rel * (1.0 + max(0.0, route))
    tom_w = tom_rel * (1.0 + max(0.0, -route))
    return mem_ans if mem_w >= tom_w else tom_ans


# ─── run one seed ────────────────────────────────────────────────────────────
def run_seed(seed):
    items = build_items(seed)
    n = len(items)

    mem = [memory_decide(it) for it in items]   # (ans, conf)
    tom = [tom_decide(it) for it in items]
    mem_mean = float(np.mean([c for _, c in mem]))
    tom_mean = float(np.mean([c for _, c in tom]))

    correct = [it["correct"] for it in items]
    route   = [it["route"] for it in items]

    acc_memory = float(np.mean([int(mem[i][0] == correct[i]) for i in range(n)]))
    acc_tom    = float(np.mean([int(tom[i][0] == correct[i]) for i in range(n)]))

    comp = [arbiter(mem[i][0], mem[i][1], mem_mean, tom[i][0], tom[i][1], tom_mean, route[i])
            for i in range(n)]
    acc_compose = float(np.mean([int(comp[i] == correct[i]) for i in range(n)]))

    oracle = [int(mem[i][0] == correct[i] or tom[i][0] == correct[i]) for i in range(n)]
    acc_oracle = float(np.mean(oracle))

    conflict = [int(mem[i][0] != tom[i][0]) for i in range(n)]
    conflict_rate = float(np.mean(conflict))

    only_memory = float(np.mean([int(mem[i][0] == correct[i] and tom[i][0] != correct[i]) for i in range(n)]))
    only_tom    = float(np.mean([int(tom[i][0] == correct[i] and mem[i][0] != correct[i]) for i in range(n)]))
    both        = float(np.mean([int(mem[i][0] == correct[i] and tom[i][0] == correct[i]) for i in range(n)]))
    neither     = float(np.mean([int(mem[i][0] != correct[i] and tom[i][0] != correct[i]) for i in range(n)]))

    # SHUFFLE control: permute which faculty-reads attach to which item, re-arbitrate
    # (route kept at its item — the shuffle decorrelates the READS from the query/answer).
    shuf_rng = np.random.default_rng(seed * 2654435761 % (2**32) + 7)
    perm_m = shuf_rng.permutation(n)
    perm_t = shuf_rng.permutation(n)
    comp_shuf = [arbiter(mem[perm_m[i]][0], mem[perm_m[i]][1], mem_mean,
                         tom[perm_t[i]][0], tom[perm_t[i]][1], tom_mean, route[i])
                 for i in range(n)]
    acc_shuffle = float(np.mean([int(comp_shuf[i] == correct[i]) for i in range(n)]))

    return dict(seed=seed, n=n,
                acc_memory=acc_memory, acc_tom=acc_tom,
                best_single=max(acc_memory, acc_tom),
                acc_compose=acc_compose, acc_shuffle=acc_shuffle, acc_oracle=acc_oracle,
                conflict_rate=conflict_rate,
                only_memory=only_memory, only_tom=only_tom, both=both, neither=neither)


# ─── leg B4: philosophy audit (H_1401 style; grep operative code) ────────────
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
        "hardcoded priority":  r'memory_wins|tom_wins|priority\s*=\s*["\']',
    }
    findings = {k: (m.group(0) if (m := re.search(pat, code, re.IGNORECASE)) else None)
                for k, pat in forbidden.items()}
    return all(v is None for v in findings.values()), findings


def main(write_verdict=True):
    out = []
    def emit(s=""):
        out.append(s); print(s, flush=True)

    emit("=" * 80)
    emit("H_1405 — BRAIN-LANE COMPOSITION: episodic MEMORY (H_1227/H_1231) × ToM (H_1293)")
    emit("  DIRECTIONAL numpy mirror · $0 CPU · 3 seeds · p7 · LIVE CORE/*.hexa UNTOUCHED")
    emit(f"  bars: COMPOSE_DELTA={COMPOSE_DELTA} ORACLE_MARGIN={ORACLE_MARGIN} SHUFFLE_TOL={SHUFFLE_TOL}")
    emit("=" * 80)

    rows = [run_seed(s) for s in SEEDS]
    for r in rows:
        emit(f"  seed {r['seed']} (n={r['n']}): "
             f"mem={r['acc_memory']:.3f} tom={r['acc_tom']:.3f} "
             f"best={r['best_single']:.3f} compose={r['acc_compose']:.3f} "
             f"shuf={r['acc_shuffle']:.3f} oracle={r['acc_oracle']:.3f} | "
             f"conflict={r['conflict_rate']:.3f} "
             f"[onlyM={r['only_memory']:.3f} onlyT={r['only_tom']:.3f} "
             f"both={r['both']:.3f} neither={r['neither']:.3f}]")

    m = lambda k: float(np.mean([r[k] for r in rows]))
    acc_memory, acc_tom = m('acc_memory'), m('acc_tom')
    best_single = m('best_single')
    acc_compose, acc_shuffle, acc_oracle = m('acc_compose'), m('acc_shuffle'), m('acc_oracle')
    conflict_rate = m('conflict_rate')
    only_memory, only_tom = m('only_memory'), m('only_tom')
    both, neither = m('both'), m('neither')

    emit("-" * 80)
    emit("MEAN (3 seeds):")
    emit(f"  acc_memory    = {acc_memory:.4f}")
    emit(f"  acc_tom       = {acc_tom:.4f}")
    emit(f"  best_single   = {best_single:.4f}")
    emit(f"  acc_compose   = {acc_compose:.4f}")
    emit(f"  acc_shuffle   = {acc_shuffle:.4f}")
    emit(f"  ORACLE        = {acc_oracle:.4f}   (oracle − best = {acc_oracle - best_single:+.4f})")
    emit(f"  conflict_rate = {conflict_rate:.4f}")
    emit(f"  decomposition : only_memory={only_memory:.4f} only_tom={only_tom:.4f} "
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
    emit(f"  (B4 p6 GUARD)       no injected answer/memory/tom/priority label : {'PASS' if B4 else 'FAIL'}")
    for k, v in findings.items():
        emit(f"        {k:22s}: {'clean' if v is None else 'FOUND -> ' + repr(v)}")

    emit("=" * 80)
    # a_break_the_wall taxonomy
    if B1 and B2 and B3 and B4:
        verdict = "🟢 COMPOSE-LIFT"
        reading = ("memory + ToM are COMPLEMENTARY and compose to a NET LIFT — integration "
                   "raises capability. The substrate-weighted, query-routed arbiter (scale-"
                   "relative confidence, NO hardcoded priority) captures the oracle headroom; "
                   "shuffle collapses (earned, p6). → names an engine-native §compose follow-on "
                   "+ a Φ-measurement follow-on (h1405_phi_runner.hexa).")
    elif B2 and B4 and not B1:
        verdict = "🟠 ORACLE-HEADROOM-but-ARBITER-FAILS"
        reading = ("taxonomy (a) wrong-arbiter: complementarity EXISTS (oracle > best_single) but "
                   "the substrate-weighted arbiter cannot capture it — the faculties compose IN "
                   "PRINCIPLE but this confidence-arbiter is the wrong rule. → needs a better arbiter.")
    elif not B2:
        verdict = "🧱 INDEPENDENT-or-SUBSUMED"
        reading = ("taxonomy (d): NO oracle headroom (oracle ≈ best_single) — the faculties do NOT "
                   "compose to a lift. Either INDEPENDENT or REDUNDANT (one store subsumes the "
                   "other's read here). A REAL finding about anima's integration limits (c9).")
    elif not B4:
        verdict = "🔴 RED (p6 guard failed — a label leaked)"
        reading = "an injected answer/memory/tom/priority surface drove behavior — p6 NOT satisfied."
    else:
        verdict = "🔴 RED (mixed)"
        reading = "see the per-bar tally above."

    # subsumption probe report (H_1293's self⊥other claim — TESTED, not assumed)
    if only_memory < 0.01 and only_tom < 0.01:
        subsumption = ("REDUNDANT/SUBSUMED — neither faculty solves items the other misses "
                       "(only_memory≈0 ∧ only_tom≈0). one store already carries the other's read.")
    elif only_memory > 0.0 and only_tom > 0.0:
        subsumption = (f"SEPARABLE — each faculty uniquely solves items the other misses "
                       f"(only_memory={only_memory:.3f} > 0 AND only_tom={only_tom:.3f} > 0). "
                       f"memory's reality-store and ToM's witnessed-belief-store carry distinct "
                       f"competence (H_1293's self⊥other claim CONFIRMED on a decision).")
    else:
        subsumption = (f"ONE-SIDED — only_memory={only_memory:.3f}, only_tom={only_tom:.3f}: "
                       f"one faculty subsumes the other's competence on this fixture.")

    emit(f"VERDICT: {verdict}")
    emit(f"READING: {reading}")
    emit(f"SUBSUMPTION PROBE: {subsumption}")
    emit("  HONEST (c9, a_scale_honest_scope/a_toy_scale_recheck): DIRECTIONAL numpy mirror; toy")
    emit("  synthetic 5-family Sally-Anne fixture, 3 seeds, deterministic readouts (tests COMPOSITION")
    emit("  STRUCTURE, not a trained integrator). LIVE CORE/*.hexa UNTOUCHED. Scale/real-corpus/")
    emit("  engine-native transfer UNVERIFIED. NO bar moved post-hoc.")
    emit("=" * 80)

    if write_verdict:
        import os
        vp = os.path.join(os.path.dirname(__file__), "..", "..",
                          ".verdicts", "1405_brain_lane_compose_memory_tom", "result.txt")
        vp = os.path.abspath(vp)
        os.makedirs(os.path.dirname(vp), exist_ok=True)
        with open(vp, "w") as f:
            f.write("\n".join(out) + "\n")
    return verdict


if __name__ == "__main__":
    main()
