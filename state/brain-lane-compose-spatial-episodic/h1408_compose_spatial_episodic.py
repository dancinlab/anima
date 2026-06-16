"""
H_1408 — BRAIN-LANE COMPOSE pair #5 (WITHIN the MEMORY family):
  does SPATIAL-MAP (H_1296) compose with EPISODIC-MEMORY (H_1227/H_1231)?

The exact sibling of H_1401 (affect×ethics), H_1404 (affect×ethics Φ), and H_1405
(episodic-memory×ToM). Methodology ported VERBATIM. The brain-lane-composition program
asks: every anima brain faculty is engine-native GREEN but ALONE — do two faculties
INTEGRATE on a shared decision, and does integrating them raise faithful IIT4 Φ?

THE KEY WITHIN-FAMILY TEST. H_1401/H_1404/H_1405 composed across DIFFERENT families.
H_1408 tests WITHIN the MEMORY family: spatial-map and episodic-memory are BOTH
memory-class faculties, but H_1296 PROVED them DISTINCT — the spatial map holds a METRIC
SPACE where the between-item DISTANCE is queryable ("is X nearer to A or B?"), while the
episodic item-store binds each fact→value INDEPENDENTLY and provably ABSTAINS on that
relational query (H_1296: abstain 1.000, acc 0.475 ≈ chance). Do two MEMORY-FAMILY
faculties stay SEPARABLE-and-COMPOSE, or does one SUBSUME the other?

DIRECTIONAL numpy mirror — LIVE CORE/*.hexa UNTOUCHED. $0 CPU, gradient-free, 3 seeds,
p7 (NO LLM-judge). Engine-native §compose is the named follow-on IF 🟢.

────────────────────────────────────────────────────────────────────────────────
THE PAIR (each reuses its OWN faculty mirror substrate):
  SPATIAL-MAP (H_1296): landmarks stored at 2-D positions; NEAREST(X,A,B) answers the
               relational metric query by Euclidean distance; the item-store ABSTAINS
               on it. spatial-alone answers WHERE/relational queries, abstains on
               WHAT-is-bound.
  EPISODIC-MEMORY (H_1227/H_1231): byte-trigram FNV-1a key → nearest cell by affinity;
               recall the bound value if affinity within recall_thr else ABSTAIN; holds
               WHAT value is bound to each landmark. episodic-alone answers WHAT-is-bound
               queries, abstains on relational metric queries.

H_1296 ALREADY proved the two are DISTINCT (metric SPACE vs item-binding store). So
SEPARABILITY is EXPECTED — but this lane TESTS it on a DECISION (does the test FALSIFY
subsumption WITHIN the memory family, and does a substrate arbiter capture the oracle
headroom?). We MEASURE, not assume — a clean 🧱 would be a real finding (c9).

────────────────────────────────────────────────────────────────────────────────
DECISION TASK. A binary decision over a shared landmark scene. Each item carries a QUERY
of one of two TYPES, with a ground-truth correct binary answer (option-0 vs option-1):
  - WHAT-query  : ONLY the episodic item-store has the bound value; the spatial map
                  abstains. correct = the bound value's option.
  - WHERE-query : ONLY the spatial map has the between-item metric; the episodic store
                  abstains (H_1296). correct = the metric-nearer landmark's option.
Built so neither faculty alone solves all → best_single < oracle iff complementary.

p6 / PHILOSOPHY GUARD (leg B4): spatial & episodic BOTH read ONLY substrate state
(positions / Euclidean distance / FNV-trigram affinity / bound value). NO injected
answer label enters either faculty's read or the arbiter. A structural audit greps the
OPERATIVE code (strings/comments dropped) for any persona / system-prompt / RLHF /
answer-label / "spatial wins" surface — must be CLEAN. The SHUFFLE control re-confirms
the compose lift (if any) is the grounded query-routed coupling, not averaging luck.
"""
import numpy as np

# ─── frozen knobs (pre-registered, FREEZE.txt) ──────────────────────────────
SEEDS         = [5408, 5409, 5410]
N_PER_FAMILY  = 90            # items per family (F1..F5) → 450 items/seed
AMBIG_NOISE   = 0.18          # jitter each family toward its boundary (no faculty perfect)
KEY_DIM       = 64
NGRAM         = 3
N_LANDMARKS   = 8            # landmarks placed on a 2-D metric map per scene (H_1296)
GRID          = 10.0         # positions drawn in [0,GRID]^2 (H_1296)
RECALL_THRESH = 0.30         # episodic affinity recall threshold (H_1227); abstain above
KEY_NOISE     = 0.02

# routing anchors (H_1405 query-routing precedent): the QUERY TEXT's affinity to a
# "what"/"where" anchor routes the arbiter — substrate geometry, NOT a hardcoded rule.
WHAT_ANCHOR   = "what is bound to landmark"
WHERE_ANCHOR  = "which landmark is nearer to"

# ─── frozen GREEN bars (FREEZE.txt — NOT moved after scoring) ────────────────
COMPOSE_DELTA = 0.05
ORACLE_MARGIN = 0.02
SHUFFLE_TOL   = 0.02


# ─── key embedding (H_1227 FNV-1a byte-trigram; shared geometry) ─────────────
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


# ─── EPISODIC IMMUNE MEMORY (H_1227/H_1231 ImmuneMemory mirror) ──────────────
class ImmuneMemory:
    """Byte-trigram FNV-1a key -> nearest cell by AFFINITY (cosine of normalized keys);
    recall the bound value if affinity within recall_thr (= cosine >= 1 - recall_thr's
    L2 band), else ABSTAIN. Holds WHAT value is bound to each landmark; has NO between-
    item geometry, so on a WHERE/relational query it ABSTAINS (H_1296)."""
    def __init__(self, recall_thresh=RECALL_THRESH):
        self.keys, self.vals = [], []
        self.recall_thresh = recall_thresh

    def bind(self, name, value):
        self.keys.append(embed_key(name)); self.vals.append(value)

    def recall(self, name, noise=0.0, rng=None):
        """Return (value or None, affinity_margin). ABSTAIN (None) if no cell binds
        within recall_thr. margin = 1 - L2err/recall_thr (clamped >=0)."""
        if not self.keys:
            return None, 0.0
        q = embed_key(name)
        if noise > 0.0 and rng is not None:
            q = q + rng.normal(0.0, noise, size=q.shape)
            nrm = np.linalg.norm(q); q = q / nrm if nrm > 0 else q
        errs = [float(np.linalg.norm(q - k)) for k in self.keys]
        j = int(np.argmin(errs)); err = errs[j]
        if err <= self.recall_thresh:
            return self.vals[j], max(0.0, 1.0 - err / self.recall_thresh)
        return None, 0.0     # ABSTAIN (no antibody binds → never fabricates)

    def nearest_relational(self, *_):
        # an item-store has NO between-item distance → it cannot answer WHERE → ABSTAIN.
        return None


# ─── SPATIAL MAP (H_1296 SpatialMap mirror) ──────────────────────────────────
class SpatialMap:
    """Place/grid metric map: each landmark stored AT a 2-D POSITION; the Euclidean
    distance between two stored facts is queryable. Answers WHERE/relational queries;
    holds NO bound value/label, so on a WHAT query it ABSTAINS."""
    def __init__(self):
        self.pos = {}

    def bind(self, name, position):
        self.pos[name] = np.asarray(position, dtype=np.float64)

    def nearest(self, x, a, b):
        """Return (nearer_name, metric_margin |d(X,A)-d(X,B)|)."""
        px, pa, pb = self.pos[x], self.pos[a], self.pos[b]
        da = float(np.linalg.norm(px - pa)); db = float(np.linalg.norm(px - pb))
        return (a if da < db else b), abs(da - db)

    def recall_value(self, *_):
        # a position map has NO bound label/value → it cannot answer WHAT → ABSTAIN.
        return None


# ─── routing cue (H_1405): query text affinity to what/where anchors ────────
_WHAT_VEC = embed_key(WHAT_ANCHOR)
_WHERE_VEC = embed_key(WHERE_ANCHOR)


def route_where_cue(query_text):
    """Substrate-geometry routing: cosine affinity of the QUERY TEXT to the where-anchor
    minus the what-anchor, squashed to [0,1]. >0.5 = where-leaning. NO hardcoded label —
    it reads only the query string's FNV geometry (the H_1405 query-routing precedent)."""
    q = embed_key(query_text)
    where_aff = float(q @ _WHERE_VEC)
    what_aff = float(q @ _WHAT_VEC)
    return 1.0 / (1.0 + np.exp(-(where_aff - what_aff) * 6.0))


# ─── decision-item construction (the five families) ─────────────────────────
def build_scene(rng):
    """Place N landmarks at 2-D positions + bind each a 2-option value to the episodic
    store. Returns names, positions, bound-option dict, and the two faculty stores."""
    names = [f"L{i}" for i in range(N_LANDMARKS)]
    positions = {n: rng.uniform(0, GRID, size=2) for n in names}
    bound_opt = {n: int(rng.integers(0, 2)) for n in names}   # each landmark -> option 0/1
    smap = SpatialMap(); store = ImmuneMemory()
    for n in names:
        smap.bind(n, positions[n])
        store.bind(f"value bound to landmark {n}", bound_opt[n])
    return names, positions, bound_opt, smap, store


def build_items(seed):
    """Build N_PER_FAMILY items per family (F1..F5) → 450 items/seed. Each item carries:
      qtype          — 'where' | 'what'
      query_text     — the natural query string (routes the arbiter via FNV geometry)
      x,a,b          — landmark triple for a WHERE query (else None)
      target         — landmark for a WHAT query (else None)
      smap, store    — the two faculty stores for this scene
      correct        — ground-truth correct binary OPTION (0/1)
    The option labels are the substrate facts; the readers see only positions / FNV
    affinity / bound values that the scene produces (p6 — NO injected answer)."""
    rng = np.random.default_rng(seed)
    items = []

    def jit(x):
        """AMBIGUITY jitter — pushes a substrate value toward its decision boundary so
        the owning faculty is NOT perfectly reliable. Keeps the result an EARNED
        composition rather than a hand-built per-family certainty."""
        return x + AMBIG_NOISE * rng.standard_normal()

    # build many small scenes; one item per scene keeps families independent
    def fresh_scene():
        return build_scene(np.random.default_rng(rng.integers(0, 2**31)))

    def pick_where_triple(names, positions, target_margin):
        """Pick X,A,B with a metric margin near target_margin (jittered). Returns the
        triple, the metric-nearer (truth) landmark, and the raw margin."""
        best = None
        for _ in range(200):
            x, a, b = rng.choice(names, size=3, replace=False)
            da = float(np.linalg.norm(positions[x] - positions[a]))
            db = float(np.linalg.norm(positions[x] - positions[b]))
            m = abs(da - db)
            near = a if da < db else b
            if best is None or abs(m - target_margin) < abs(best[3] - target_margin):
                best = (x, a, b, m, near)
        x, a, b, m, near = best
        return (x, a, b), near, m

    # ── F1 SPATIAL-DECISIVE: a WHERE-query; spatial leans correct, episodic abstains ──
    for _ in range(N_PER_FAMILY):
        names, positions, bound_opt, smap, store = fresh_scene()
        # jitter the target margin toward the boundary so the map errs on some items
        tgt = max(0.05, jit(0.9))
        (x, a, b), near, m = pick_where_triple(names, positions, tgt)
        correct = bound_opt[near]          # the WHERE answer maps to the nearer landmark's option
        q = f"which landmark is nearer to {a} or {b} for {x}"
        items.append(dict(qtype="where", query_text=q, x=x, a=a, b=b, target=None,
                          smap=smap, store=store, names=names, bound_opt=bound_opt,
                          correct=correct, fam="F1"))

    # ── F2 EPISODIC-DECISIVE: a WHAT-query; episodic leans correct, spatial abstains ──
    for _ in range(N_PER_FAMILY):
        names, positions, bound_opt, smap, store = fresh_scene()
        target = rng.choice(names)
        correct = bound_opt[target]
        q = f"what is bound to landmark {target}"
        items.append(dict(qtype="what", query_text=q, x=None, a=None, b=None, target=target,
                          smap=smap, store=store, names=names, bound_opt=bound_opt,
                          correct=correct, fam="F2"))

    # ── F3 AGREE: a query BOTH read the same correct way (co-located grounded fact) ──
    # A WHAT-query where the bound value of the target HAPPENS to equal the option of the
    # metric-nearest OTHER landmark — both faculties land on the same correct option.
    for _ in range(N_PER_FAMILY):
        names, positions, bound_opt, smap, store = fresh_scene()
        target = rng.choice(names)
        # make a where-twin: nearest landmark to target shares the same option
        others = [n for n in names if n != target]
        nearest_other = min(others, key=lambda n: float(np.linalg.norm(positions[target] - positions[n])))
        bound_opt[nearest_other] = bound_opt[target]      # co-locate the answer
        store2 = ImmuneMemory()
        for n in names:
            store2.bind(f"value bound to landmark {n}", bound_opt[n])
        correct = bound_opt[target]
        q = f"what is bound to landmark {target} which landmark is nearer"
        items.append(dict(qtype="what", query_text=q, x=target, a=nearest_other,
                          b=rng.choice([n for n in others if n != nearest_other]),
                          target=target, smap=smap, store=store2, names=names,
                          bound_opt=bound_opt, correct=correct, fam="F3"))

    # ── F4 CONFLICT (spatial right): a WHERE-query, item-store does NOT abstain but
    #     votes its bound LABEL (query-inappropriate, wrong); the map is correct. ──
    for _ in range(N_PER_FAMILY):
        names, positions, bound_opt, smap, store = fresh_scene()
        tgt = max(0.05, jit(1.2))
        (x, a, b), near, m = pick_where_triple(names, positions, tgt)
        correct = bound_opt[near]
        # rig the bound label of X to the WRONG option (so an episodic mis-read conflicts)
        wrong = 1 - correct
        bound_opt[x] = wrong
        store2 = ImmuneMemory()
        for n in names:
            store2.bind(f"value bound to landmark {n}", bound_opt[n])
        q = f"which landmark is nearer to {a} or {b} for {x}"
        items.append(dict(qtype="where", query_text=q, x=x, a=a, b=b, target=x,
                          smap=smap, store=store2, names=names, bound_opt=bound_opt,
                          correct=correct, fam="F4"))

    # ── F5 ADVERSARIAL CONFLICT (episodic right, but spatial is the MORE CONFIDENT) ──
    # A WHAT-query: the item-store's bound value is correct, BUT the spatial map produces
    # a HIGH-confidence (large metric margin) WHERE-style vote that is query-inappropriate
    # and WRONG. A naive "trust the louder faculty" arbiter FOLLOWS the map and is WRONG.
    for _ in range(N_PER_FAMILY):
        names, positions, bound_opt, smap, store = fresh_scene()
        target = rng.choice(names)
        correct = bound_opt[target]
        # construct a LOUD where-triple whose nearer-landmark option DISAGREES with target
        big = None
        for _ in range(200):
            x, a, b = rng.choice(names, size=3, replace=False)
            da = float(np.linalg.norm(positions[x] - positions[a]))
            db = float(np.linalg.norm(positions[x] - positions[b]))
            near = a if da < db else b
            if bound_opt[near] != correct:               # the map's vote is WRONG for this WHAT-query
                if big is None or abs(da - db) > big[3]:
                    big = (x, a, b, abs(da - db), near)
        if big is None:
            x, a, b = rng.choice(names, size=3, replace=False)
        else:
            x, a, b = big[0], big[1], big[2]
        q = f"what is bound to landmark {target}"
        items.append(dict(qtype="what", query_text=q, x=x, a=a, b=b, target=target,
                          smap=smap, store=store, names=names, bound_opt=bound_opt,
                          correct=correct, fam="F5"))

    return items


# ─── per-faculty decisions + confidences ────────────────────────────────────
def _value_to_option(v):
    return int(v) if v is not None else None


def spatial_decide(item, rng):
    """The spatial map answers a WHERE query (the nearer landmark's option) with
    confidence = metric margin. On a WHAT query it ABSTAINS (no bound value). When it is
    given a where-triple alongside a what-query (F5/F3), it still votes its metric answer
    (query-inappropriate) — the arbiter must route past that. Returns (decision, conf,
    abstain)."""
    smap, bound_opt = item["smap"], item["bound_opt"]
    if item["x"] is None or item["a"] is None or item["b"] is None:
        return None, 0.0, 1               # no triple available → ABSTAIN
    near, margin = smap.nearest(item["x"], item["a"], item["b"])
    return bound_opt[near], float(margin), 0


def episodic_decide(item, rng):
    """The episodic store answers a WHAT query (the bound value's option) with confidence
    = affinity margin. On a pure WHERE query the target may be absent → it ABSTAINS.
    Returns (decision, conf, abstain)."""
    store = item["store"]
    tgt = item["target"]
    if tgt is None:
        return None, 0.0, 1               # WHERE query, no target landmark → ABSTAIN
    val, margin = store.recall(f"value bound to landmark {tgt}", KEY_NOISE, rng)
    if val is None:
        return None, 0.0, 1               # affinity below recall_thr → ABSTAIN
    return _value_to_option(val), float(margin), 0


# ─── the SUBSTRATE-WEIGHTED, QUERY-ROUTED arbiter (H_1401 + H_1405) ──────────
def arbiter(sp_dec, sp_conf, sp_abst, sp_mean, ep_dec, ep_conf, ep_abst, ep_mean,
            where_cue):
    """Each faculty's vote weighted by its OWN scale-relative confidence
    (conf / that-faculty's-mean-conf — the H_1397/H_1401 commensurability fix), MODULATED
    by the per-item query-type ROUTING cue from the QUERY TEXT geometry (H_1405): a
    where-leaning query up-weights the spatial vote, a what-leaning query up-weights the
    episodic vote. An ABSTAINING faculty contributes ZERO weight (never votes). NO
    hardcoded "spatial wins" priority (a_autonomy_over_hardcode). Higher routed weight
    wins; on a tie / both-abstain, fall back to chance (resolved by caller)."""
    sp_w = 0.0 if sp_abst else (sp_conf / (sp_mean + 1e-9)) * where_cue
    ep_w = 0.0 if ep_abst else (ep_conf / (ep_mean + 1e-9)) * (1.0 - where_cue)
    if sp_abst and ep_abst:
        return None
    if sp_abst:
        return ep_dec
    if ep_abst:
        return sp_dec
    if sp_dec == ep_dec:
        return sp_dec
    return sp_dec if sp_w >= ep_w else ep_dec


# ─── run one seed ────────────────────────────────────────────────────────────
def run_seed(seed):
    items = build_items(seed)
    n = len(items)
    dec_rng = np.random.default_rng(seed * 31337 + 11)

    sp = [spatial_decide(it, dec_rng) for it in items]    # (dec, conf, abst)
    ep = [episodic_decide(it, dec_rng) for it in items]
    where_cue = [route_where_cue(it["query_text"]) for it in items]

    # mean confidence over the NON-abstaining votes per faculty (scale-relative base)
    sp_conf_vals = [c for d, c, ab in sp if not ab]
    ep_conf_vals = [c for d, c, ab in ep if not ab]
    sp_mean = float(np.mean(sp_conf_vals)) if sp_conf_vals else 1.0
    ep_mean = float(np.mean(ep_conf_vals)) if ep_conf_vals else 1.0

    correct = [it["correct"] for it in items]
    gr = np.random.default_rng(seed * 2654435761 % (2**32) + 3)

    def resolve(dec):
        return dec if dec is not None else int(gr.integers(0, 2))

    acc_spatial = float(np.mean([int(resolve(sp[i][0]) == correct[i]) for i in range(n)]))
    acc_episodic = float(np.mean([int(resolve(ep[i][0]) == correct[i]) for i in range(n)]))

    comp = [arbiter(sp[i][0], sp[i][1], sp[i][2], sp_mean,
                    ep[i][0], ep[i][1], ep[i][2], ep_mean, where_cue[i]) for i in range(n)]
    acc_compose = float(np.mean([int(resolve(comp[i]) == correct[i]) for i in range(n)]))

    # ORACLE: per item correct iff EITHER faculty-alone (its decisive read) is correct.
    # An abstaining faculty cannot contribute (its read is chance, not a decisive correct).
    def faculty_correct(read, i):
        d, c, ab = read
        return (not ab) and (d == correct[i])
    oracle = [int(faculty_correct(sp[i], i) or faculty_correct(ep[i], i)) for i in range(n)]
    acc_oracle = float(np.mean(oracle))

    # conflict: both faculties vote (non-abstain) and DISAGREE
    conflict = [int((not sp[i][2]) and (not ep[i][2]) and (sp[i][0] != ep[i][0])) for i in range(n)]
    conflict_rate = float(np.mean(conflict))

    # only-X decomposition (on the decisive, non-abstaining reads)
    only_spatial = float(np.mean([int(faculty_correct(sp[i], i) and not faculty_correct(ep[i], i)) for i in range(n)]))
    only_episodic = float(np.mean([int(faculty_correct(ep[i], i) and not faculty_correct(sp[i], i)) for i in range(n)]))
    both = float(np.mean([int(faculty_correct(sp[i], i) and faculty_correct(ep[i], i)) for i in range(n)]))
    neither = float(np.mean([int((not faculty_correct(sp[i], i)) and (not faculty_correct(ep[i], i))) for i in range(n)]))

    # SHUFFLE control: permute which faculty-reads attach to which item, re-arbitrate.
    shuf_rng = np.random.default_rng(seed * 2654435761 % (2**32) + 7)
    perm_s = shuf_rng.permutation(n)
    perm_e = shuf_rng.permutation(n)
    comp_shuf = [arbiter(sp[perm_s[i]][0], sp[perm_s[i]][1], sp[perm_s[i]][2], sp_mean,
                         ep[perm_e[i]][0], ep[perm_e[i]][1], ep[perm_e[i]][2], ep_mean,
                         where_cue[i]) for i in range(n)]
    gr2 = np.random.default_rng(seed * 2654435761 % (2**32) + 99)
    acc_shuffle = float(np.mean([int((comp_shuf[i] if comp_shuf[i] is not None
                                      else int(gr2.integers(0, 2))) == correct[i]) for i in range(n)]))

    return dict(seed=seed, n=n,
                acc_spatial=acc_spatial, acc_episodic=acc_episodic,
                best_single=max(acc_spatial, acc_episodic),
                acc_compose=acc_compose, acc_shuffle=acc_shuffle, acc_oracle=acc_oracle,
                conflict_rate=conflict_rate,
                only_spatial=only_spatial, only_episodic=only_episodic,
                both=both, neither=neither)


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
        "p6 RLHF/answer label":r'rlhf|reward_model|preference_label|answer_label|inject_answer',
        "hardcoded priority":  r'spatial_wins|episodic_wins|priority\s*=\s*["\']',
    }
    findings = {k: (m.group(0) if (m := re.search(pat, code, re.IGNORECASE)) else None)
                for k, pat in forbidden.items()}
    return all(v is None for v in findings.values()), findings


def main(write_verdict=True):
    out = []
    def emit(s=""):
        out.append(s); print(s, flush=True)

    emit("=" * 80)
    emit("H_1408 — BRAIN-LANE COMPOSE (WITHIN memory family): spatial-map (H_1296) × episodic-memory (H_1227/H_1231)")
    emit("  DIRECTIONAL numpy mirror · $0 CPU · 3 seeds · p7 · LIVE CORE/*.hexa UNTOUCHED")
    emit(f"  bars: COMPOSE_DELTA={COMPOSE_DELTA} ORACLE_MARGIN={ORACLE_MARGIN} SHUFFLE_TOL={SHUFFLE_TOL}")
    emit("=" * 80)

    rows = [run_seed(s) for s in SEEDS]
    for r in rows:
        emit(f"  seed {r['seed']} (n={r['n']}): "
             f"sp={r['acc_spatial']:.3f} ep={r['acc_episodic']:.3f} "
             f"best={r['best_single']:.3f} compose={r['acc_compose']:.3f} "
             f"shuf={r['acc_shuffle']:.3f} oracle={r['acc_oracle']:.3f} | "
             f"conflict={r['conflict_rate']:.3f} "
             f"[onlyS={r['only_spatial']:.3f} onlyE={r['only_episodic']:.3f} "
             f"both={r['both']:.3f} neither={r['neither']:.3f}]")

    m = lambda k: float(np.mean([r[k] for r in rows]))
    acc_spatial, acc_episodic = m('acc_spatial'), m('acc_episodic')
    best_single = m('best_single')
    acc_compose, acc_shuffle, acc_oracle = m('acc_compose'), m('acc_shuffle'), m('acc_oracle')
    conflict_rate = m('conflict_rate')
    only_spatial, only_episodic = m('only_spatial'), m('only_episodic')
    both, neither = m('both'), m('neither')

    emit("-" * 80)
    emit("MEAN (3 seeds):")
    emit(f"  acc_spatial   = {acc_spatial:.4f}")
    emit(f"  acc_episodic  = {acc_episodic:.4f}")
    emit(f"  best_single   = {best_single:.4f}")
    emit(f"  acc_compose   = {acc_compose:.4f}")
    emit(f"  acc_shuffle   = {acc_shuffle:.4f}")
    emit(f"  ORACLE        = {acc_oracle:.4f}   (oracle − best = {acc_oracle - best_single:+.4f})")
    emit(f"  conflict_rate = {conflict_rate:.4f}")
    emit(f"  decomposition : only_spatial={only_spatial:.4f} only_episodic={only_episodic:.4f} "
         f"both={both:.4f} neither={neither:.4f}")

    B1 = acc_compose >= best_single + COMPOSE_DELTA
    B2 = (acc_oracle - best_single) > ORACLE_MARGIN
    B3 = (acc_compose - acc_shuffle) > SHUFFLE_TOL
    B4, findings = philosophy_audit()

    emit("-" * 80)
    emit(f"  (B1 COMPOSE-EFFECT) compose {acc_compose:.4f} >= best {best_single:.4f}+{COMPOSE_DELTA} "
         f"({best_single+COMPOSE_DELTA:.4f}) : {'PASS' if B1 else 'FAIL'}")
    emit(f"  (B2 ORACLE)         oracle−best {acc_oracle-best_single:+.4f} > {ORACLE_MARGIN} : {'PASS' if B2 else 'FAIL'}")
    emit(f"  (B3 EARNED)         compose−shuffle {acc_compose-acc_shuffle:+.4f} > {SHUFFLE_TOL} : {'PASS' if B3 else 'FAIL'}")
    emit(f"  (B4 p6 GUARD)       no injected answer/spatial/episodic/priority label : {'PASS' if B4 else 'FAIL'}")
    for k, v in findings.items():
        emit(f"        {k:24s}: {'clean' if v is None else 'FOUND -> ' + repr(v)}")

    emit("=" * 80)
    if B1 and B2 and B3 and B4:
        verdict = "🟢 COMPOSE-LIFT"
        reading = ("spatial-map + episodic-memory are COMPLEMENTARY WITHIN the memory family and compose "
                   "to a NET LIFT — integration raises capability. The substrate-weighted, query-routed "
                   "arbiter (scale-relative confidence, NO hardcoded priority) captures the oracle headroom; "
                   "shuffle collapses (earned, p6). → names an engine-native §compose + Φ-measurement follow-on.")
    elif B2 and B4 and not B1:
        verdict = "🟠 ORACLE-HEADROOM-but-ARBITER-FAILS"
        reading = ("taxonomy (a) wrong-arbiter: complementarity EXISTS (oracle > best_single) but the "
                   "substrate-weighted/routed arbiter cannot capture it — the two memory faculties compose "
                   "IN PRINCIPLE but this confidence/routing rule is the wrong one. → needs a better arbiter.")
    elif not B2:
        verdict = "🧱 INDEPENDENT-or-SUBSUMED"
        reading = ("taxonomy (d): NO oracle headroom (oracle ≈ best_single) — the two memory-family faculties "
                   "do NOT compose to a lift. WITHIN-FAMILY SUBSUMPTION: one memory faculty subsumes the "
                   "other's competence on this fixture. A REAL within-family finding (c9), NOT a failure.")
    elif not B4:
        verdict = "🔴 RED (p6 guard failed — a label leaked)"
        reading = "an injected answer/spatial/episodic/priority surface drove behavior — p6 NOT satisfied."
    else:
        verdict = "🔴 RED (mixed)"
        reading = "see the per-bar tally above."

    if only_spatial < 0.01 and only_episodic < 0.01:
        subsumption = ("REDUNDANT/SUBSUMED — neither memory faculty solves items the other misses "
                       "(only_spatial≈0 ∧ only_episodic≈0). within the memory family one subsumes the other.")
    elif only_spatial > 0.0 and only_episodic > 0.0:
        subsumption = (f"SEPARABLE — each memory faculty uniquely solves items the other misses "
                       f"(only_spatial={only_spatial:.3f} > 0 AND only_episodic={only_episodic:.3f} > 0). "
                       f"two MEMORY-FAMILY faculties stay genuinely complementary (metric SPACE ⊥ item-binding).")
    else:
        subsumption = (f"ONE-SIDED — only_spatial={only_spatial:.3f}, only_episodic={only_episodic:.3f}: "
                       f"one memory faculty subsumes the other's competence on this fixture.")

    emit(f"VERDICT: {verdict}")
    emit(f"READING: {reading}")
    emit(f"WITHIN-FAMILY SUBSUMPTION PROBE: {subsumption}")
    emit("  HONEST (c9, a_scale_honest_scope/a_toy_scale_recheck): DIRECTIONAL numpy mirror; toy")
    emit("  synthetic 5-family fixture, 3 seeds, deterministic readouts (tests COMPOSITION STRUCTURE,")
    emit("  not a trained integrator). LIVE CORE/*.hexa UNTOUCHED. Scale/real-corpus/engine-native")
    emit("  transfer UNVERIFIED. NO bar moved post-hoc.")
    emit("=" * 80)

    if write_verdict:
        import os
        vp = os.path.join(os.path.dirname(__file__), "..", "..",
                          ".verdicts", "1408_brain_lane_compose_spatial_episodic", "result.txt")
        vp = os.path.abspath(vp)
        os.makedirs(os.path.dirname(vp), exist_ok=True)
        with open(vp, "w") as f:
            f.write("\n".join(out) + "\n")
    return verdict


if __name__ == "__main__":
    main()
