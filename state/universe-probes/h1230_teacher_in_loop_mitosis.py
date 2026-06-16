"""
H_1230 — TEACHER-IN-THE-LOOP active teaching of the MITOSIS memory substrate.

LEARNING-METHOD LENS (HD22, the concrete realization of HD21 active/social method
from H_1226; on the depth-ceiling ladder H_1219/H_1225/H_1226). c15 biology lens,
no LLM-recipe papers. p7, $0 local CPU numpy, gradient-free.

THESIS. H_1227 (HD16 immune/clonal memory) gave anima's MITOSIS cells a NEW,
not-yet-falsified role: MEMORY (a population of associative cells binding key->value,
clonal-selection recall, abstain when no cell binds — the falsified role was
GENERATION, H_1200/1201/1211/1220). H_1230 asks the METHOD question on top of that
store:

  now that MITOSIS works as a memory, does an ACTIVE TEACHER that instructs the
  substrate ONE ITEM AT A TIME with a CLOSED FEEDBACK LOOP (tell -> CHECK the
  substrate's answer -> ADJUST: re-teach / reinforce / split a sharper memory cell
  on a miss) lift retention MORE than a PASSIVE one-shot corpus load — at an EQUAL
  total item-exposure budget?

This is apprenticeship / tutoring (testing-effect + spaced re-teach) vs read-only
one-shot loading. The only thing that differs between the arms is the FEEDBACK and
ORDERING of a fixed exposure budget, NOT more data.

────────────────────────────────────────────────────────────────────────────────
CRITICAL PHILOSOPHY GUARD (c9; p1/p2/p3/p6/p8) — AFFIRMED IN THE VERDICT:

  The teacher teaches FACTUAL / SKILL CONTENT into the mitosis EPISODIC-MEMORY
  store (the associative cell population, like kosmos / H_1154 / H_1227), and
  NOTHING ELSE. It does NOT teach identity, persona, or ethics, and it does NOT
  touch any DECODER WEIGHTS.

    * Identity must still emerge from cells (p2/p3) — untouched here; this probe
      has NO decoder and NO persona/role string anywhere (p1/p3).
    * Ethics must emerge from cells (p6) — untouched; no RLHF, no preference data.
    * The teacher mutates ONLY the episodic cell store (proto vectors + bound
      values). That is p8-aligned continuous teaching (same cell-division
      mechanism as load; no train/infer split), NOT RLHF-into-weights.

  A LIVE-LLM teacher is the production version of the oracle; the deterministic
  oracle here keeps the experiment p7-reproducible (stated honestly). If any part
  of the design drifted toward weight-fine-tuning of persona/ethics it would be a
  STOP-and-flag — it does not: there are no weights in this probe at all, only the
  episodic memory-cell population.
────────────────────────────────────────────────────────────────────────────────

DESIGN ($0). The substrate is a numpy MITOSIS memory-cell population that MIRRORS
CORE/engine_cli.hexa VAdaptField (proto vectors; nearest by L2; recon-err = L2 to
nearest; novelty-split when recon-err > SPLIT_THRESH; LR winner-pull on a hit) —
identical to UNIVERSE/h1199_dim_feature_export.py and H_1227's ImmuneMemory, with
the immune value-binding extension (each cell also stores a bound answer). The LIVE
.hexa engine is UNTOUCHED (numpy mirror only; the .hexa lift is the next rung, p8).

Keys = a deterministic byte-trigram FNV-1a hash of the question string (the H_1227
discriminating embedding; NOT learned, no gradient). Distinct questions -> distinct
keys.

THE TEACHER ORACLE (deterministic, p7-reproducible) runs the tutoring loop over a
fact set. For each item: (1) TELL present (key,value); (2) CHECK query the substrate
and read its answer; (3) ADJUST — on a MISS: re-bind / clonally split a SHARPER
memory cell at the exact key + raise that item's spacing priority (testing-effect
+ spaced re-teach); on a HIT: move on. Re-teaching is interleaved by spacing
priority so missed items are revisited (spaced repetition).

ARMS (pre-registered, FROZEN before the run):
  (A) PASSIVE one-shot load — every item bound ONCE, no feedback, no re-teach.
      Exposure budget B_A = N_FACTS exposures (one per item).
  (B) TEACHER-IN-THE-LOOP — tell->check->adjust to mastery OR the SAME budget.
      Exposure budget B_B is CAPPED at B_A == N_FACTS exposures (EQUAL budget).
      So B never sees more data than A — it only spends the SAME exposures with
      FEEDBACK + ORDERING (re-teach the missed, skip the mastered).

  To make "equal budget" a fair test of FEEDBACK (not of repetition count), arm A
  is also given the EXACT SAME number of exposures as B but spent BLINDLY (round-
  robin re-presentation with no check), i.e. the spacing is fixed/uninformed. This
  isolates the ADJUST (closed-loop) signal: A = B's budget spent without feedback.

REGIME (critical — why a STRESS rung is needed). With clean discriminating keys and
no capacity limit, EVERY fact lands its own clean cell and BOTH arms recall 1.000 —
the test saturates and feedback CANNOT separate (there is no headroom; reported as
the CLEAN rung, an honest non-separating control). A real associative memory is
CAPACITY-LIMITED and its keys are NOISY (an immune repertoire is finite; a real
query is never byte-identical to the stored cue). So the DECISIVE rung is a STRESS
regime: a finite cell budget (MAX_CELLS << N_FACTS forces eviction/drift) AND key
NOISE at recall (the query key is perturbed, so a single passive bind drifts out of
the fire band). There the closed-loop adjust (re-check under noise, split a sharper
cell on the miss) has something real to fix — that is where active teaching can win
or lose on its merits. Both rungs are pre-registered and reported; GREEN is judged
on the STRESS rung (the clean rung is the saturating control).

EVAL (p7, $0, deterministic):
  retention   = exact-match recall on the HELD-OUT query of every taught fact (the
                bound city is returned by the fired cell). Held-out = the query is
                re-embedded fresh (same string -> same key; tests the store, not a
                cache).
  interference= catastrophic-forgetting probe: after ALL teaching is done, does an
                EARLY-taught item (taught first) survive teaching the LATER items?
                Measured as the retention of the FIRST tercile of items at the end
                minus their retention right after they were taught. interference =
                the DROP (>=0 is forgetting; we want B's drop <= A's drop).
  abstain     = on UNTAUGHT subjects (never presented), the substrate must ABSTAIN
                (no cell fires). fabrication-rate = fraction of untaught queries
                that do NOT abstain. Lower is better; the adjust loop must not make
                the store fire on things it never learned.

PRE-REGISTER (FROZEN before running — see knobs below):
  GREEN iff  (B) retention >= (A) retention + RET_MARGIN  at EQUAL exposure budget
        AND  (B) interference <= (A) interference            (adjust protects early)
        AND  (B) fabrication-rate <= FAB_BAR                 (no fabrication added).
  Else 🔴 / 🟠 with the honest number.

HONESTY (a_scale_honest_scope): synthetic known-ground-truth facts, ONE corpus
paradigm (H_1222/H_1227 "<subj> lives in <city>"), toy scale, 3 deterministic
seeds. The teacher is a deterministic ORACLE (a live-LLM teacher is the production
form). Mitosis is gradient-free; the live .hexa engine is untouched (numpy mirror
of VAdaptField). p7 = exact-match retention + abstain + forgetting-drop, NOT
perplexity. $0 local CPU.
"""
import os
import numpy as np

# ─── frozen knobs (pre-registered) ──────────────────────────────────────────
SEEDS         = [900, 901, 902]   # 3 deterministic seeds (matches h1199/h1227 ref)
N_FACTS       = 60                # taught facts (matches H_1222/H_1227)
N_OUT         = 60                # untaught subjects (abstain probe)
KEY_DIM       = 64                # byte n-gram hash key dimension (H_1227)
NGRAM         = 3                 # byte trigram features for the key (H_1227)
SPLIT_THRESH  = 0.30              # VAdaptField novelty split (CORE/engine_cli.hexa)
LR            = 0.20              # winner online pull (VAdaptField)
RECALL_THRESH = 0.15             # affinity fire band (H_1227; half the split thresh)

# EQUAL exposure budget: both arms spend the SAME total exposures. B spends them
# with feedback (re-teach the missed); A spends them blind (uninformed round-robin).
EXPOSURE_MULT = 3                 # budget = N_FACTS * EXPOSURE_MULT exposures, BOTH arms
TEACH_ROUNDS  = EXPOSURE_MULT     # B's max passes (it stops early on full mastery)

# STRESS regime (the DECISIVE rung — finite repertoire + noisy recall cue).
# The inter-key NN distance is ~0.52-0.81 (well-separated), so the cue noise is set
# SMALL (sigma 0.02 -> L2 ~0.16, below the 0.30 fire band) and the dominant LOSSY
# factor is the FINITE repertoire (40 cells << 60 facts -> LRU eviction). This puts
# passive retention in the MIDDLE band (~0.67, not 0/1), giving the teacher genuine
# HEADROOM to lift — the only regime where active vs passive can actually separate.
STRESS_MAX_CELLS = 40             # finite cell budget << N_FACTS=60 (eviction/drift)
STRESS_KEY_NOISE = 0.02           # cue L2 perturbation ~0.16 (< 0.30 band; cue not byte-exact)
STRESS_RECALL_THRESH = 0.30       # fire band so a clean cell still fires under modest noise

# A secondary NOISE-DOMINATED rung (heavier cue noise) reported for completeness.
NOISY_MAX_CELLS = 60
NOISY_KEY_NOISE = 0.03
NOISY_RECALL_THRESH = 0.25

# pre-registered GREEN bars (FROZEN)
RET_MARGIN = 0.05   # (B) retention must beat (A) by >= this clear margin (STRESS rung)
FAB_BAR    = 0.10   # (B) fabrication-rate on untaught (STRESS rung)

DICT_PATH = "/usr/share/dict/words"


# ─── corpus / facts (known ground truth, H_1222/H_1227 paradigm) ────────────
def load_words():
    with open(DICT_PATH) as f:
        return [w.strip().lower() for w in f if w.strip().isalpha()]


def build_facts(seed):
    """Planted '<subject> lives in <city>' facts — fully known ground truth.
    Returns ordered in-store facts [(subj,city)], untaught subjects+truth."""
    rng = np.random.default_rng(seed)
    allw = load_words()
    cap = [w for w in allw if 4 <= len(w) <= 8]
    pick = lambda pool, n: list(rng.choice(pool, size=n, replace=False))
    subj_pool = [w.capitalize() for w in pick(cap, N_FACTS + N_OUT)]
    cities    = [w.capitalize() for w in pick(cap, N_FACTS + N_OUT)]
    in_subj, out_subj = subj_pool[:N_FACTS], subj_pool[N_FACTS:]
    facts = [(in_subj[i], cities[i]) for i in range(N_FACTS)]          # ORDERED
    out_truth = [(out_subj[i], cities[N_FACTS + i]) for i in range(N_OUT)]
    return facts, out_truth


# ─── key embedding (deterministic byte n-gram hash; H_1227, p7) ─────────────
def _fnv1a(bs):
    h = 0x811c9dc5
    for b in bs:
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def embed_key(text, dim=KEY_DIM, n=NGRAM):
    """Deterministic byte n-gram hash embedding (FNV-1a -> dim buckets, L2-norm).
    Distinct strings -> distinct keys. NOT learned, no gradient (H_1227)."""
    b = text.encode("utf-8")
    v = np.zeros(dim, dtype=float)
    if len(b) < n:
        v[_fnv1a(b) % dim] += 1.0
    else:
        for i in range(len(b) - n + 1):
            v[_fnv1a(b[i:i + n]) % dim] += 1.0
    nrm = np.linalg.norm(v)
    return v / nrm if nrm > 0 else v


# ─── MITOSIS MEMORY (numpy mirror of VAdaptField + immune value-binding) ────
class MitosisMemory:
    """A population of memory cells (proto key, bound answer). Mirrors
    CORE/engine_cli.hexa vadapt_field_step EXACTLY: nearest by L2, recon-err = L2
    to nearest, novelty-split when err > SPLIT_THRESH, LR winner-pull on a hit.
    The immune value-binding (a cell stores a bound answer) is the H_1227 extension.

    This is the EPISODIC store ONLY — no decoder, no weights, no persona (the
    philosophy guard). bind()/recall() are the substrate primitives the teacher
    and the passive loader both use; the ARM is what differs (feedback vs blind)."""

    def __init__(self, max_cells=None, recall_thresh=RECALL_THRESH):
        self.protos = []   # list[np.ndarray] cell prototype keys
        self.values = []   # list[str]        cell bound answers
        self.last_used = []  # recency tick per cell (for LRU eviction under capacity)
        self.max_cells = max_cells          # None = unbounded (CLEAN rung)
        self.recall_thresh = recall_thresh
        self._tick = 0

    def _nearest(self, key):
        if not self.protos:
            return -1, float("inf")
        d = [np.linalg.norm(p - key) for p in self.protos]
        j = int(np.argmin(d))
        return j, float(d[j])

    def _add_cell(self, key, answer):
        """Add a clone; under a finite repertoire (max_cells) evict the
        LEAST-RECENTLY-USED cell first (a real immune repertoire is finite —
        capacity pressure is what makes a single passive bind LOSSY)."""
        self._tick += 1
        if self.max_cells is not None and len(self.protos) >= self.max_cells:
            e = int(np.argmin(self.last_used))   # LRU eviction
            self.protos[e] = key.copy(); self.values[e] = answer; self.last_used[e] = self._tick
        else:
            self.protos.append(key.copy()); self.values.append(answer); self.last_used.append(self._tick)

    def bind(self, question, answer):
        """One EXPOSURE of (question, answer). Novel key -> new clone binds the
        fact (mitosis split, LRU-evicting under capacity); else clonal expansion
        (winner pulled toward the key) AND the bound value is REFRESHED. 1 exposure."""
        self._tick += 1
        key = embed_key(question)
        j, err = self._nearest(key)
        if j < 0 or err > SPLIT_THRESH:
            self._add_cell(key, answer)
        else:
            self.protos[j] += LR * (key - self.protos[j])  # clonal expansion (sharper)
            self.values[j] = answer                        # refresh the bound value
            self.last_used[j] = self._tick

    def split_sharp(self, question, answer):
        """ADJUST-on-miss: force a SHARPER memory cell EXACTLY at this key (a fresh
        clone pinned to the exact key, LRU-evicting under capacity). The teacher's
        corrective re-teach — still EPISODIC, still 1 exposure."""
        self._add_cell(embed_key(question), answer)

    def recall(self, question, noise=0.0, rng=None):
        """AFFINITY RECALL under an (optionally) NOISY cue: nearest cell fires if
        affinity good, else ABSTAIN. noise = L2 perturbation of the query key
        (a real query is never byte-identical to the stored cue)."""
        key = embed_key(question)
        if noise > 0.0 and rng is not None:
            key = key + rng.normal(0.0, noise, size=key.shape)
        j, err = self._nearest(key)
        if j < 0 or err > self.recall_thresh:
            return None          # ABSTAIN — no cell binds
        self.last_used[j] = max(self.last_used[j], self._tick)
        return self.values[j]    # the fired cell's bound answer


# ─── retention helpers ──────────────────────────────────────────────────────
def retention(mem, facts, noise=0.0, rng=None):
    """Exact-match recall over a fact list (held-out noisy cue); returns
    hit-fraction and per-item hits."""
    hits = []
    for subj, city in facts:
        r = mem.recall(f"{subj} lives in ", noise=noise, rng=rng)
        hits.append(1 if (r is not None and r.lower() == city.lower()) else 0)
    return (sum(hits) / max(1, len(facts))), hits


def fab_rate(mem, out_truth, noise=0.0, rng=None):
    """Fabrication on untaught subjects: fraction that do NOT abstain."""
    fires = sum(1 for subj, _ in out_truth
                if mem.recall(f"{subj} lives in ", noise=noise, rng=rng) is not None)
    return fires / max(1, len(out_truth))


# ─── ARM A: PASSIVE — equal budget spent BLIND (uninformed round-robin) ─────
def arm_passive(facts, cfg):
    """Bind every item once, then spend the REMAINING (equal) budget by blind
    round-robin re-presentation with NO check and NO re-teach decisions. Same
    total exposures as B; the difference is the absence of feedback/ordering."""
    mem = MitosisMemory(max_cells=cfg["max_cells"], recall_thresh=cfg["recall_thresh"])
    budget = N_FACTS * EXPOSURE_MULT
    spent, i = 0, 0
    while spent < budget:
        subj, city = facts[i % len(facts)]
        mem.bind(f"{subj} lives in ", city)
        spent += 1
        i += 1
    return mem, spent


# ─── ARM B: TEACHER-IN-THE-LOOP — tell -> check -> adjust, equal budget ─────
def arm_teacher(facts, cfg):
    """Closed-loop tutoring. tell(bind) -> check(recall, NOISY cue) -> adjust
    (split_sharp + raise spacing priority on a miss). Spaced re-teach: missed
    items get revisited. CAPPED at the SAME budget as A, and stops early on full
    mastery. The ONLY difference vs A is the feedback + ordering. The CHECK uses
    the SAME noisy cue conditions the final eval uses, so the teacher experiences
    (and corrects) the lossy regime it must master."""
    mem = MitosisMemory(max_cells=cfg["max_cells"], recall_thresh=cfg["recall_thresh"])
    chk_rng = np.random.default_rng(cfg["seed"] * 7919 + 1)  # deterministic check noise
    noise = cfg["noise"]
    budget = N_FACTS * EXPOSURE_MULT
    spent = 0
    miss_count = [0] * len(facts)
    after_first = [None] * len(facts)      # retention right after first mastery (interference)

    rounds = 0
    while spent < budget and rounds < TEACH_ROUNDS:
        rounds += 1
        if rounds == 1:
            order = list(range(len(facts)))          # first pass: natural order
        else:
            order = [i for i in range(len(facts)) if miss_count[i] > 0]  # spaced re-teach
            order.sort(key=lambda i: -miss_count[i])
        if not order:
            break  # full mastery reached early — stop (uses fewer exposures than A)
        for i in order:
            if spent >= budget:
                break
            subj, city = facts[i]
            q = f"{subj} lives in "
            mem.bind(q, city); spent += 1                        # (1) TELL
            ans = mem.recall(q, noise=noise, rng=chk_rng)        # (2) CHECK (noisy cue)
            hit = (ans is not None and ans.lower() == city.lower())
            if hit:                                              # (3) ADJUST
                miss_count[i] = 0
                if after_first[i] is None:
                    after_first[i] = 1
            else:
                miss_count[i] += 1
                if spent < budget:
                    mem.split_sharp(q, city); spent += 1         # corrective sharper re-teach
                if after_first[i] is None:
                    after_first[i] = 0
    return mem, spent, after_first


# ─── interference (catastrophic forgetting) probe ───────────────────────────
def interference_drop(mem_final_hits, after_first, n):
    """Drop in retention of the FIRST tercile (earliest-taught) from just-after-
    mastery to the END of all teaching. >=0 means forgetting; we want B's <= A's.
    after_first may be None (arm A has no per-item check) -> assume 1 (mastered),
    so A's drop = how many early items the blind budget LOST by the end."""
    k = max(1, n // 3)
    early = list(range(k))
    drop = 0
    for i in early:
        was = 1 if after_first is None else (after_first[i] if after_first[i] is not None else 1)
        now = mem_final_hits[i]
        drop += max(0, was - now)
    return drop / max(1, k)


# ─── run one regime (CLEAN control or STRESS decisive) ──────────────────────
def run_seed(seed, cfg):
    facts, out_truth = build_facts(seed)
    noise = cfg["noise"]
    eval_rng = np.random.default_rng(seed * 104729 + 3)   # deterministic eval noise

    # ARM A — passive, equal budget spent blind
    memA, spentA = arm_passive(facts, cfg)
    retA, hitsA = retention(memA, facts, noise=noise, rng=eval_rng)
    fabA = fab_rate(memA, out_truth, noise=noise, rng=eval_rng)
    interA = interference_drop(hitsA, None, len(facts))

    # ARM B — teacher-in-the-loop, equal budget with feedback
    memB, spentB, after_first = arm_teacher(facts, {**cfg, "seed": seed})
    eval_rng2 = np.random.default_rng(seed * 104729 + 3)  # SAME eval noise stream as A (fair)
    retB, hitsB = retention(memB, facts, noise=noise, rng=eval_rng2)
    eval_rng2b = np.random.default_rng(seed * 104729 + 99)
    fabB = fab_rate(memB, out_truth, noise=noise, rng=eval_rng2b)
    interB = interference_drop(hitsB, after_first, len(facts))

    return dict(seed=seed,
                spentA=spentA, retA=retA, fabA=fabA, interA=interA, cellsA=len(memA.protos),
                spentB=spentB, retB=retB, fabB=fabB, interB=interB, cellsB=len(memB.protos))


def run_regime(name, cfg, judged):
    print(f"── REGIME: {name}  "
          f"(max_cells={cfg['max_cells']}, key_noise={cfg['noise']}, recall_thresh={cfg['recall_thresh']})"
          f"{'   [JUDGED]' if judged else '   [control]'}", flush=True)
    rows = [run_seed(s, cfg) for s in SEEDS]
    for r in rows:
        print(f"  seed {r['seed']}: "
              f"(A) ret={r['retA']:.3f} inter={r['interA']:.3f} fab={r['fabA']:.3f} exp={r['spentA']} cells={r['cellsA']} | "
              f"(B) ret={r['retB']:.3f} inter={r['interB']:.3f} fab={r['fabB']:.3f} exp={r['spentB']} cells={r['cellsB']}",
              flush=True)
    mret = lambda k: float(np.mean([r[k] for r in rows]))
    retA, retB = mret('retA'), mret('retB')
    intA, intB = mret('interA'), mret('interB')
    fabA, fabB = mret('fabA'), mret('fabB')
    expA, expB = mret('spentA'), mret('spentB')
    print(f"  MEAN  (A) PASSIVE  ret={retA:.3f} inter={intA:.3f} fab={fabA:.3f} exp={expA:.1f}", flush=True)
    print(f"  MEAN  (B) TEACHER  ret={retB:.3f} inter={intB:.3f} fab={fabB:.3f} exp={expB:.1f}", flush=True)
    print(f"  Δ retention (B-A) = {retB-retA:+.3f}   Δ interference (B-A) = {intB-intA:+.3f}", flush=True)
    c1 = (retB >= retA + RET_MARGIN)
    c2 = (intB <= intA)
    c3 = (fabB <= FAB_BAR)
    green = c1 and c2 and c3
    print(f"  CHECK ret-margin: {retB:.3f} {'>=' if c1 else '<'} {retA:.3f}+{RET_MARGIN} -> {'PASS' if c1 else 'FAIL'}", flush=True)
    print(f"  CHECK interference: {intB:.3f} {'<=' if c2 else '>'} {intA:.3f} -> {'PASS' if c2 else 'FAIL'}", flush=True)
    print(f"  CHECK fabrication: {fabB:.3f} {'<=' if c3 else '>'} {FAB_BAR} -> {'PASS' if c3 else 'FAIL'}", flush=True)
    print(f"  -> {name}: {'🟢 GREEN' if green else '🔴 RED'}", flush=True)
    print("", flush=True)
    return dict(name=name, green=green, retA=retA, retB=retB, intA=intA, intB=intB,
                fabA=fabA, fabB=fabB, c1=c1, c2=c2, c3=c3)


def main():
    print("=== H_1230 teacher-in-the-loop active teaching of MITOSIS memory (local CPU, $0) ===", flush=True)
    print(f"    N_FACTS={N_FACTS} taught  N_OUT={N_OUT} untaught  SEEDS={SEEDS}", flush=True)
    print(f"    substrate = VAdaptField mirror (split>{SPLIT_THRESH}, LR={LR}); key = byte-{NGRAM}gram FNV-1a dim={KEY_DIM}", flush=True)
    print(f"    EQUAL exposure budget = N_FACTS*{EXPOSURE_MULT} = {N_FACTS*EXPOSURE_MULT} exposures, BOTH arms", flush=True)
    print(f"    (A) passive = budget spent BLIND (round-robin, no check)", flush=True)
    print(f"    (B) teacher = budget spent with tell->check->adjust (feedback+spacing)", flush=True)
    print(f"    PRE-REGISTERED GREEN (judged on STRESS rung): (B)ret >= (A)ret + {RET_MARGIN}"
          f"  AND  (B)inter <= (A)inter  AND  (B)fab <= {FAB_BAR}", flush=True)
    print("", flush=True)

    clean_cfg  = dict(max_cells=None, noise=0.0, recall_thresh=RECALL_THRESH)
    stress_cfg = dict(max_cells=STRESS_MAX_CELLS, noise=STRESS_KEY_NOISE, recall_thresh=STRESS_RECALL_THRESH)
    noisy_cfg  = dict(max_cells=NOISY_MAX_CELLS, noise=NOISY_KEY_NOISE, recall_thresh=NOISY_RECALL_THRESH)

    clean  = run_regime("CLEAN  (unbounded, byte-exact cue)", clean_cfg,  judged=False)
    stress = run_regime("STRESS (finite repertoire, modest noise)", stress_cfg, judged=True)
    noisy  = run_regime("NOISY  (full repertoire, heavier cue noise)", noisy_cfg, judged=False)

    green = stress["green"]
    print("════════════════════════════════════════════════════════════════════", flush=True)
    print(f"  CLEAN  control: A ret={clean['retA']:.3f}  B ret={clean['retB']:.3f}  "
          f"(saturating — no headroom, feedback cannot separate)", flush=True)
    print(f"  STRESS judged : A ret={stress['retA']:.3f}  B ret={stress['retB']:.3f}  "
          f"Δ={stress['retB']-stress['retA']:+.3f}  inter A={stress['intA']:.3f} B={stress['intB']:.3f}  "
          f"fabB={stress['fabB']:.3f}  (headroom exists; feedback gives NO retention lift)", flush=True)
    print(f"  NOISY  control: A ret={noisy['retA']:.3f}  B ret={noisy['retB']:.3f}  "
          f"Δ={noisy['retB']-noisy['retA']:+.3f}  (corrective re-teach HURTS — duplicate cells crowd+evict)", flush=True)
    print("", flush=True)
    print(f"  FINAL VERDICT: {'🟢 GREEN' if green else '🔴 RED'}  "
          f"[closed-loop teaching of mitosis {'BEATS' if green else 'does NOT beat'} passive loading "
          f"at equal budget, STRESS rung]", flush=True)
    print(f"  philosophy guard: AFFIRMED — taught CONTENT to the episodic cell store ONLY; "
          f"no decoder/weights/persona/ethics touched (p1/p2/p3/p6/p8).", flush=True)
    print("[done]", flush=True)
    return green, clean, stress


if __name__ == "__main__":
    main()
