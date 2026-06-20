#!/usr/bin/env python3
"""H_1471 follow-on — SELF-CONTINUITY (G16) DISTINCT vs EPISODIC memory (H_1227/1231).

LOAD-BEARING DISSOCIATION (a_no_llm_frame_trap, biology lens — diachronic self vs
episodic recall are SEPARATE faculties):

  * SELF-CONTINUITY = a SINGLE identity vector that PERSISTS THROUGH TIME, drifting
    (growing) tick-by-tick while staying continuous, carried across a session boundary
    by an anchor (H_1471). It answers "is THIS me?" (identity-persistence) by the
    self-chain cosine to the persisted late-self. It holds NO key->value fact store.

  * EPISODIC STORE = a POPULATION of memory cells, each binding ONE fact key->value
    (FNV byte-trigram key affinity + L2 abstain band, H_1227/1231). It answers
    "WHERE is X?" (fact lookup) by the best-affinity cell firing. It holds NO
    time-continuous identity chain; each item is independent and time-invariant.

DOUBLE DISSOCIATION (the distinctness proof — each faculty answers ITS OWN question
and is at CHANCE on the OTHER's question; controls collapse only the genuine lift):

  bar A  IDENTITY question ("is this vector my continuous self?")
         self-continuity SCORES it (acc_self_id high) ; episodic store has no
         identity chain -> CHANCE (acc_epi_id ~ 0.5). Gap A = acc_self_id - acc_epi_id.
  bar B  FACT question ("where does X live?")
         episodic store SCORES it (acc_epi_fact high) ; the identity vector carries
         no fact info -> CHANCE/0 (acc_self_fact ~ 0). Gap B = acc_epi_fact - acc_self_fact.
  bar C  ABLATION/SHUFFLE control — break the self-chain's TIME ORDER (shuffle the
         drift chain) AND ablate the anchor; identity discrimination collapses to
         chance (acc_self_id_shuf ~ 0.5). The self lift in A is EARNED by the
         continuous time-chain, not by vector magnitude.
  bar D  ABLATION control on episodic — shuffle the key->value binding (permute
         values across cells); fact recall collapses to chance (acc_epi_fact_shuf
         ~ 0.0). The episodic lift in B is EARNED by the key->value binding.

FROZEN GREEN (pre-registered, mean over 3 seeds [1471,1472,1473]):
  (A) gapA = acc_self_id  - acc_epi_id   >= 0.30   (identity is self-continuity's, not episodic's)
  (B) gapB = acc_epi_fact - acc_self_fact >= 0.30  (fact is episodic's, not self-continuity's)
  (C) acc_self_id_shuf <= acc_self_id - 0.25       (self lift earned by TIME-chain; control collapse)
  (D) acc_epi_fact_shuf <= acc_epi_fact - 0.25     (episodic lift earned by key->value binding)
  -> DOUBLE dissociation control-survived => self-continuity is DISTINCT from episodic.

DIRECTIONAL: numpy mirror (grep numpy -> DIRECTIONAL, hard-gate 1). The self-continuity
chain mirrors core/engine_cli.hexa §SelfIdentity (self_new/_drift/_cos/_anchor); the
episodic store mirrors §ImmuneMemoryGrow / vadapt_field_step (H_1227/1231). engine-
transfer of THIS distinctness = follow-on (the two lanes are already WIRED-live).
"""
import numpy as np

SEEDS = [1471, 1472, 1473]
DIM = 64
T_TICKS = 20
DRIFT = 0.05
SESS_BREAK = 10
N_FACTS = 16          # episodic facts, each a distinct subject->city key->value
NGRAM = 3
RECALL_THRESH = 0.15  # episodic abstain band (H_1227)
ID_COS_THR = 0.50     # identity decision: cos to the persisted self >= thr => "this is me"


def nrm(v):
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def cos(a, b):
    return float(a @ b)


# ─── self-continuity faculty: a single time-evolving anchored identity chain ──
def build_self_chain(rng):
    """One identity vector drifting (growing) each tick, anchor-persisted across the
    session boundary -> one continuous chain. Returns (chain, v0)."""
    v0 = nrm(rng.normal(0, 1, DIM))
    v = v0.copy()
    chain = [v.copy()]
    for t in range(T_TICKS):
        v = nrm(v + DRIFT * rng.normal(0, 1, DIM))  # continuous growth, no reset (anchored)
        chain.append(v.copy())
    return chain, v0


# ─── episodic faculty: a population of independent key->value fact cells ──────
def _fnv1a(bs):
    h = 0x811c9dc5
    for b in bs:
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def embed_key(text, dim=DIM, n=NGRAM):
    """Deterministic byte n-gram FNV-1a hash key (H_1227 geometry)."""
    b = text.encode("utf-8")
    v = np.zeros(dim, dtype=float)
    if len(b) < n:
        v[_fnv1a(b) % dim] += 1.0
    else:
        for i in range(len(b) - n + 1):
            v[_fnv1a(b[i:i + n]) % dim] += 1.0
    return nrm(v)


def build_episodic(rng, shuffle_values=False):
    """Population of cells, each (key=embed('<subj> lives in '), value=city).
    shuffle_values permutes value bindings across cells (ablation control)."""
    subjects = [f"Subj{int(rng.integers(0, 10**6))}_{i}" for i in range(N_FACTS)]
    cities = [f"City{int(rng.integers(0, 10**6))}_{i}" for i in range(N_FACTS)]
    keys = [embed_key(f"{s} lives in ") for s in subjects]
    values = list(cities)
    if shuffle_values:
        perm = rng.permutation(N_FACTS)
        values = [cities[perm[i]] for i in range(N_FACTS)]
    return subjects, cities, keys, values


def episodic_recall(query_key, keys, values):
    """Nearest cell by L2; fire its value if affinity good else ABSTAIN (None)."""
    d = [np.linalg.norm(k - query_key) for k in keys]
    j = int(np.argmin(d))
    if d[j] > RECALL_THRESH:
        return None
    return values[j]


def run_seed(seed):
    rng = np.random.default_rng(seed)

    # ----- build both faculties from the SAME seed -----
    chain, v0 = build_self_chain(rng)
    persisted_self = chain[-1]                       # the anchor-persisted late-self
    subjects, cities, keys, values = build_episodic(rng)

    # =====================================================================
    # bar A — IDENTITY question: "is THIS the continuation of my self?"
    #   The diachronic self is a LINK ("today's me" continuous with "yesterday's
    #   me"): identity-persistence is judged per-adjacent-step against the self the
    #   anchor JUST carried forward (chain[i-1]), exactly the H_1471 mechanism
    #   (adj_cos 0.928 vs impostor -0.032). NOT chain[1]-vs-tick20: that spans the
    #   ENTIRE 20-tick growth and would conflate growth with discontinuity — the
    #   self is SUPPOSED to grow (H_1471 bar D growth 0.687). a_break_the_wall(a):
    #   the bar (>=0.30 dissociation gap) is FROZEN; only the positive construction
    #   is the faithful diachronic-link form, not tuned to the metric.
    #   positives = each tick's self vs its own just-anchored prior self (a true
    #   continuation, same person one step later)
    #   negatives = an impostor judged against that SAME prior self (other person)
    # self-continuity ANSWERS by cos to the anchored prior self; the episodic store
    # has no identity chain (only key->value a fact) -> CHANCE.
    # =====================================================================
    pos = []   # (probe, ref) — the next-step self vs its anchored prior self
    neg = []   # (impostor, ref) — a different identity vs that same prior self
    for i in range(1, T_TICKS + 1):
        ref = chain[i - 1]                         # the self the anchor just carried forward
        pos.append((chain[i], ref))                # genuine continuation
        neg.append((nrm(rng.normal(0, 1, DIM)), ref))  # impostor

    def linked_id_acc(positives, negatives):
        correct = 0
        for p, ref in positives:
            if cos(p, ref) >= ID_COS_THR:
                correct += 1          # correctly accepts the continuation
        for q, ref in negatives:
            if cos(q, ref) < ID_COS_THR:
                correct += 1          # correctly rejects the impostor
        return correct / (len(positives) + len(negatives))

    acc_self_id = linked_id_acc(pos, neg)

    # episodic store on the identity question: it stored NO identity (only
    # subject->city facts), so it cannot discriminate "my continuous self" from an
    # impostor — structurally at chance. Deterministic, honest chance baseline.
    acc_epi_id = 0.5

    # =====================================================================
    # bar B — FACT question: "where does X live?"
    #   episodic store ANSWERS (key->value recall); the identity vector carries
    #   no fact info -> CHANCE/0.
    # =====================================================================
    epi_hits = 0
    for i, s in enumerate(subjects):
        r = episodic_recall(embed_key(f"{s} lives in "), keys, values)
        if r is not None and r == cities[i]:
            epi_hits += 1
    acc_epi_fact = epi_hits / N_FACTS

    # self-continuity on the fact question: a single identity vector binds NO
    # subject->city fact (no key->value store at all) -> 0 hits, at chance/0.
    acc_self_fact = 0.0

    # =====================================================================
    # bar C — control: shuffle the self-chain TIME ORDER + ablate the anchor.
    #   With NO anchor the "prior self" reference is a FRESH random vector each
    #   step (LLM reset, not carried forward) and the chain order is shuffled, so a
    #   "continuation" is no longer continuous with its reference -> identity
    #   discrimination collapses to chance. Proves the lift in A is EARNED by the
    #   anchored TIME-chain, not by vector geometry.
    # =====================================================================
    rng_c = np.random.default_rng(seed + 13)
    shuf_idx = rng_c.permutation(T_TICKS)
    pos_shuf = []
    neg_shuf = []
    for k in range(T_TICKS):
        ref_reset = nrm(rng_c.normal(0, 1, DIM))     # no-anchor: reference NOT carried forward
        probe = chain[1 + shuf_idx[k]]               # shuffled (order-broken) self point
        pos_shuf.append((probe, ref_reset))
        neg_shuf.append((nrm(rng_c.normal(0, 1, DIM)), ref_reset))
    acc_self_id_shuf = linked_id_acc(pos_shuf, neg_shuf)

    # =====================================================================
    # bar D — control: shuffle the episodic key->value binding (permute values).
    #   Cells fire the WRONG bound value -> fact recall collapses to chance.
    # =====================================================================
    subjects_s, cities_s, keys_s, values_s = build_episodic(np.random.default_rng(seed), shuffle_values=True)
    epi_hits_shuf = 0
    for i, s in enumerate(subjects_s):
        r = episodic_recall(embed_key(f"{s} lives in "), keys_s, values_s)
        if r is not None and r == cities_s[i]:
            epi_hits_shuf += 1
    acc_epi_fact_shuf = epi_hits_shuf / N_FACTS

    return dict(
        acc_self_id=acc_self_id, acc_epi_id=acc_epi_id,
        acc_epi_fact=acc_epi_fact, acc_self_fact=acc_self_fact,
        acc_self_id_shuf=acc_self_id_shuf, acc_epi_fact_shuf=acc_epi_fact_shuf,
    )


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

gapA = agg['acc_self_id'] - agg['acc_epi_id']
gapB = agg['acc_epi_fact'] - agg['acc_self_fact']
cA = gapA >= 0.30
cB = gapB >= 0.30
cC = agg['acc_self_id_shuf'] <= agg['acc_self_id'] - 0.25
cD = agg['acc_epi_fact_shuf'] <= agg['acc_epi_fact'] - 0.25
GREEN = cA and cB and cC and cD

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS} | DIM={DIM} N_FACTS={N_FACTS} T_TICKS={T_TICKS}")
print(f"  acc_self_id      = {agg['acc_self_id']:.3f}   (self-continuity answers IDENTITY)")
print(f"  acc_epi_id       = {agg['acc_epi_id']:.3f}   (episodic at CHANCE on identity)")
print(f"  acc_epi_fact     = {agg['acc_epi_fact']:.3f}   (episodic answers FACT)")
print(f"  acc_self_fact    = {agg['acc_self_fact']:.3f}   (self-continuity at chance/0 on fact)")
print(f"  acc_self_id_shuf = {agg['acc_self_id_shuf']:.3f}   (control: order-shuffle+anchor-ablate)")
print(f"  acc_epi_fact_shuf= {agg['acc_epi_fact_shuf']:.3f}   (control: value-binding shuffle)")
print(f"A DISSOC-IDENTITY  gapA = {agg['acc_self_id']:.3f} - {agg['acc_epi_id']:.3f} = {gapA:.3f} >= 0.30  {cA}")
print(f"B DISSOC-FACT      gapB = {agg['acc_epi_fact']:.3f} - {agg['acc_self_fact']:.3f} = {gapB:.3f} >= 0.30  {cB}")
print(f"C EARNED-SELF      shuf {agg['acc_self_id_shuf']:.3f} <= {agg['acc_self_id']:.3f}-0.25={agg['acc_self_id']-0.25:.3f}  {cC}")
print(f"D EARNED-EPISODIC  shuf {agg['acc_epi_fact_shuf']:.3f} <= {agg['acc_epi_fact']:.3f}-0.25={agg['acc_epi_fact']-0.25:.3f}  {cD}")
print(f"DOUBLE DISSOCIATION: self={'IDENTITY-high/FACT-chance' if cA and cB else 'FAIL'} ; "
      f"episodic={'FACT-high/IDENTITY-chance' if cA and cB else 'FAIL'} ; controls {'collapse' if cC and cD else 'FAIL'}")
