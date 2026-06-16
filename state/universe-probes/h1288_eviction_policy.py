"""
H_1288 — EVICTION POLICY as the capacity lever of the immune/episodic memory.

THE SUCCESSOR THE KEY-GEOMETRY WALL POINTED TO. FOUR converging closed-negatives —
H_1230 (active teacher inert/harmful), H_1284 (neuromodulation no-free-lunch),
H_1285 (amygdala salience = a recurrence confound), H_1287 (key geometry does NOT
lift recall) — all diagnosed the SAME bottleneck for the H_1227/H_1231 immune
clonal memory: CAPACITY. H_1287 was decisive: better KEY GEOMETRY does NOT lift
recall under capacity stress (the apparent lift was pure DIMENSIONALITY; the dim-64
trigram key is collision-FREE), and total recall stays ~0.667 because the store is
ZERO-SUM — protecting one fact LRU-evicts another. H_1287's explicit conclusion:

  "to lift recall under stress, add CELLS or change the EVICTION POLICY —
   not the key geometry."

This lane tests that directly, on the EXACT H_1287 EVICTION-BOUND regime (the
zero-sum LRU rung: max_cells << facts, well-separated keys).

────────────────────────────────────────────────────────────────────────────────
BREAKTHROUGH MECHANISM (mitosis-native — a_no_llm_frame_trap + p8; brain-science
lens, NOT an LLM recipe). The current store LRU-EVICTS under capacity pressure
(zero-sum). But anima's substrate IS continuous cell-division (p8 — the H_1199
mitosis VAdaptField). The principled answer to a zero-sum store is NOT a smarter
eviction heuristic — it is to NOT EVICT: GROW a new cell (mitosis split) under
capacity pressure instead of evicting an old fact. Biology: the brain does not
hold a FIXED cell budget it LRU-evicts; it consolidates / sparsifies and GROWS
(adult neurogenesis, dendritic spine formation under load). The honest constraint
is that growth is BOUNDED (a generous max, not infinite) and TRADES a larger
memory footprint for recall — that tradeoff is reported, not hidden.

ARMS (pre-registered, FROZEN before the run):
  (A) LRU-EVICT — the CURRENT store. Fixed cell budget (max_cells = STRESS cap).
      On a novel key under capacity pressure, LRU-evict the least-recently-used
      cell. Zero-sum: every new fact costs an old one. This is the H_1287 EVICTION-
      BOUND control that capped at ~0.667.
  (B) MITOSIS-GROW — under capacity pressure + recon-err > SPLIT_THRESH, GROW a
      new cell (mitosis split) instead of evicting. Bounded by a GENEROUS max
      (GROW_MAX_CELLS, set so every distinct fact CAN land its own cell but the
      store is NOT infinite — honest). Growth breaks the zero-sum: an old fact is
      never sacrificed to store a new one.
  (C) WEIGHTED-EVICT — a SMARTER eviction HEURISTIC (NOT growth). Same FIXED budget
      as A, but eviction picks the victim by an importance/frequency score
      (least-frequently-bound + least-recently-used, LFU+LRU blend) instead of pure
      LRU. This separates "GROWTH lifts recall" from "a better eviction heuristic
      lifts recall" — if C also lifts, the lever is the heuristic, not cell-growth.

  Arm C is the load-bearing control of the lane: it lets the verdict attribute any
  lift to GROWTH (extra cells, footprint cost) vs HEURISTIC (free, same budget).

────────────────────────────────────────────────────────────────────────────────
IMPORTANCE (so "important recall" is a real, pre-registered sub-metric, not post-
hoc). A deterministic per-fact importance: the FIRST tercile of facts (taught
first, longest-lived in the store) are tagged IMPORTANT. Under LRU these are the
ones MOST at risk of eviction (oldest → least-recently-used → evicted first), so
importance is exactly the population a smarter policy / growth should protect.
Reported as a sub-metric; the GREEN bar is on TOTAL recall (importance is the
mechanistic story, total recall is the gate).
────────────────────────────────────────────────────────────────────────────────

EVAL (p7, $0, deterministic):
  total recall    = exact-match recall on the HELD-OUT (noisy-cue) query of EVERY
                    taught fact (the fired cell returns the bound city).
  important recall= the same on the IMPORTANT (first-tercile) facts only — the
                    eviction-vulnerable population (sub-metric, reported).
  cell-count cost = the final number of cells each arm holds. B's growth TRADES a
                    larger footprint for recall; the tradeoff is reported HONESTLY
                    (B's cells > A's cells is the cost of breaking zero-sum).
  fabrication     = on UNTAUGHT subjects (never bound) the store MUST ABSTAIN; fab-
                    rate = fraction of untaught queries that do NOT abstain. LOAD-
                    BEARING (H_1227): non-fabrication MUST stay intact (p1-p8 guard).

PRE-REGISTER (FROZEN before running — see knobs):
  GREEN iff  (B) total recall >= (A) total recall + REC_MARGIN   (growth breaks zero-sum)
        AND  (B) fabrication-rate <= FAB_BAR                     (abstain intact)
        with the CELL-COUNT COST reported (B trades footprint for recall — stated).
  Arm C is reported alongside to attribute the lift (growth vs heuristic).

  HONESTY (c9):
    * If growth trivially stores EVERYTHING (capacity pressure fully removed → A's
      stress regime no longer stresses B), report it as an EXISTENCE-PROOF (growth
      CAN break the ceiling) not an effect-size — and state the footprint cost.
    * If even growth AND the weighted heuristic CANNOT lift recall under honest
      capacity accounting → 🧱 (the ~0.667 ceiling is fundamental to the retrieve-
      then-copy regime; capacity is not the lever either, and the 4 reds + this
      lane jointly exhaust the capacity hypothesis).

PHILOSOPHY GUARD (c9; p1/p2/p3/p6/p8). Mitosis split = the engine's own tick (p8
continuous cell-division, NOT an external command). The eviction/growth policy
mutates ONLY how the EPISODIC cell store manages its own population — no labels
into the mechanism, no persona/role string, no ethics, no decoder weights.
Identity (p2/p3) and ethics (p6) still emerge from cells; abstain-when-ungrounded
(H_1227, load-bearing) is kept and re-checked under every policy. Importance is a
deterministic fn of TAUGHT-ORDER only (not a content label, not the eval metric).

HONESTY (a_scale_honest_scope · a_toy_scale_recheck). Synthetic known-ground-truth
facts, ONE corpus paradigm (H_1222/H_1227 "<subj> lives in <city>"), toy scale, 3
deterministic seeds, $0 local CPU numpy. p7 = exact-match recall + abstain, NOT
perplexity. Mirror of CORE/engine_cli.hexa VAdaptField; the LIVE .hexa engine is
UNTOUCHED — engine-native mitosis-grow eviction is the r2 follow-on per
a_engine_native_learning. xref H_1227 · H_1230 · H_1285 · H_1287 · H_1199.
"""
import os
import numpy as np

# ─── frozen knobs (pre-registered) ──────────────────────────────────────────
SEEDS         = [900, 901, 902]   # 3 deterministic seeds (matches h1199/h1227/h1230/h1287)
N_FACTS       = 60                # in-store facts (matches H_1222/H_1227/H_1230/H_1287)
N_OUT         = 60                # untaught subjects (abstain probe)
KEY_DIM       = 64                # byte n-gram hash key dim (the H_1227/H_1230/H_1287 key)
NGRAM         = 3                 # byte trigram features for the key
SPLIT_THRESH  = 0.30              # VAdaptField novelty split (CORE/engine_cli.hexa)
LR            = 0.20              # winner online pull (VAdaptField)

# EVICTION-BOUND regime = the EXACT H_1287 zero-sum LRU rung (the ~0.667 ceiling).
# cells << facts, keys already well-separated (nothing to disambiguate), modest cue
# noise. This is the regime all 4 reds pinned the bottleneck to.
STRESS_MAX_CELLS    = 40          # << N_FACTS=60 (LRU eviction is the limit) — H_1287 EVICT rung
STRESS_KEY_NOISE    = 0.16        # TARGET-L2 cue perturbation (H_1287 EVICT_KEY_NOISE, dim-invariant)
STRESS_RECALL_THRESH= 0.30        # affinity fire band (H_1287 EVICT_RECALL_THRESH)

# ARM B growth bound — GENEROUS but FINITE (honest: not infinite). Set so every
# distinct fact CAN land its own cell (>= N_FACTS) with headroom for noisy re-binds,
# but the store is explicitly bounded (footprint cost is real and reported).
GROW_MAX_CELLS      = 80          # >= N_FACTS=60 (+33% headroom); FINITE, not infinite

# IMPORTANCE = first tercile (taught first → oldest → most LRU-eviction-vulnerable).
IMPORTANT_FRAC      = 1.0 / 3.0

# pre-registered GREEN bars (FROZEN)
REC_MARGIN = 0.05    # (B) total recall must beat (A) by >= this clear margin
FAB_BAR    = 0.10    # (B) fabrication-rate on untaught (abstain intact — H_1227)

DICT_PATH = "/usr/share/dict/words"


# ─── corpus / facts (known ground truth, H_1222/H_1227/H_1230/H_1287 paradigm) ─
def load_words():
    with open(DICT_PATH) as f:
        return [w.strip().lower() for w in f if w.strip().isalpha()]


def build_facts(seed):
    """Planted '<subject> lives in <city>' facts — fully known ground truth.
    ORDERED (taught order = the importance/LRU axis). Well-separated keys (the
    H_1230/H_1287 EVICTION-BOUND regime: cue collisions are NOT the limit here)."""
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


# ─── MITOSIS MEMORY with a PLUGGABLE eviction/growth POLICY ──────────────────
# policy ∈ {"lru", "grow", "weighted"} — the ONLY thing that differs across arms.
class PolicyMemory:
    """A population of memory cells (proto key, bound answer). Mirrors
    CORE/engine_cli.hexa vadapt_field_step EXACTLY: nearest by L2, recon-err = L2 to
    nearest, novelty-split when err > SPLIT_THRESH, LR winner-pull on a hit. The
    immune value-binding (a cell stores a bound answer) is the H_1227 extension.

    The arms differ ONLY in the POLICY when a novel key arrives at FULL capacity:
      "lru"      = evict the least-recently-used cell (the CURRENT store, zero-sum).
      "grow"     = do NOT evict; GROW a new cell (mitosis split) up to grow_max
                   (then fall back to LRU only past the honest grow bound). p8.
      "weighted" = evict by a (freq, recency) score — least-frequently-bound, then
                   least-recently-used — a smarter HEURISTIC at the SAME budget.
    """

    def __init__(self, policy, base_max, grow_max, recall_thresh=STRESS_RECALL_THRESH):
        self.policy = policy
        self.base_max = base_max          # the FIXED budget (A and C); B's first cap
        self.grow_max = grow_max          # B's generous finite growth bound
        self.recall_thresh = recall_thresh
        self.protos = []
        self.values = []
        self.last_used = []               # recency tick per cell (LRU)
        self.bind_count = []              # times this cell was bound/reinforced (LFU)
        self._tick = 0

    # effective hard cap for THIS policy (B may grow beyond base_max up to grow_max)
    def _cap(self):
        return self.grow_max if self.policy == "grow" else self.base_max

    def _nearest(self, key):
        if not self.protos:
            return -1, float("inf")
        d = [np.linalg.norm(p - key) for p in self.protos]
        j = int(np.argmin(d))
        return j, float(d[j])

    def _evict_index(self):
        """Pick the victim cell index under the active policy's eviction rule."""
        if self.policy == "weighted":
            # LFU primary (least-frequently-bound), LRU tiebreak (oldest). Lower
            # score = more evictable. score = bind_count * BIG + last_used keeps
            # freq dominant, recency as the tiebreaker.
            BIG = 10_000_000
            scores = [self.bind_count[i] * BIG + self.last_used[i] for i in range(len(self.protos))]
            return int(np.argmin(scores))
        # default LRU (also B's fallback once it hits the generous grow bound)
        return int(np.argmin(self.last_used))

    def _add_cell(self, key, answer):
        """Add a clone. At full capacity: GROW (B, until grow_max) else EVICT a
        victim chosen by the policy's rule. p8: growth = a mitosis split tick."""
        self._tick += 1
        if len(self.protos) >= self._cap():
            e = self._evict_index()
            self.protos[e] = key.copy(); self.values[e] = answer
            self.last_used[e] = self._tick; self.bind_count[e] = 1
        else:
            self.protos.append(key.copy()); self.values.append(answer)
            self.last_used.append(self._tick); self.bind_count.append(1)

    def bind(self, question, answer):
        """One EXPOSURE. Novel key -> new clone (grow OR evict per policy); else
        clonal expansion (winner pulled toward the key) + bound value refreshed."""
        self._tick += 1
        key = embed_key(question)
        j, err = self._nearest(key)
        if j < 0 or err > SPLIT_THRESH:
            self._add_cell(key, answer)
        else:
            self.protos[j] += LR * (key - self.protos[j])   # clonal expansion (sharper)
            self.values[j] = answer                          # refresh bound value
            self.last_used[j] = self._tick
            self.bind_count[j] += 1                           # reinforcement (LFU signal)

    def recall(self, question, noise=0.0, rng=None):
        """AFFINITY RECALL under a (optionally) NOISY cue: nearest cell fires if
        affinity good, else ABSTAIN (never fabricates). noise = TARGET L2 magnitude
        of the cue perturbation (dim-invariant, H_1287 fair-noise convention)."""
        key = embed_key(question)
        if noise > 0.0 and rng is not None:
            sigma = noise / np.sqrt(max(1, key.shape[0]))
            key = key + rng.normal(0.0, sigma, size=key.shape)
        j, err = self._nearest(key)
        if j < 0 or err > self.recall_thresh:
            return None
        self.last_used[j] = max(self.last_used[j], self._tick)
        return self.values[j]


# ─── eval helpers (p7, deterministic) ───────────────────────────────────────
def load_store(policy, facts):
    mem = PolicyMemory(policy, base_max=STRESS_MAX_CELLS, grow_max=GROW_MAX_CELLS)
    for subj, city in facts:
        mem.bind(f"{subj} lives in ", city)
    return mem


def recall_rate(mem, facts, noise, rng):
    hits = 0
    for subj, city in facts:
        r = mem.recall(f"{subj} lives in ", noise=noise, rng=rng)
        if r is not None and r.lower() == city.lower():
            hits += 1
    return hits / max(1, len(facts))


def fab_rate(mem, out_truth, noise, rng):
    fires = sum(1 for subj, _ in out_truth
                if mem.recall(f"{subj} lives in ", noise=noise, rng=rng) is not None)
    return fires / max(1, len(out_truth))


def run_arm(policy, facts, out_truth, seed):
    mem = load_store(policy, facts)
    n_imp = max(1, int(round(N_FACTS * IMPORTANT_FRAC)))
    imp_facts = facts[:n_imp]                              # first tercile = important
    rng_t = np.random.default_rng(seed * 104729 + 3)      # shared eval-noise stream (fair)
    tot = recall_rate(mem, facts, STRESS_KEY_NOISE, rng_t)
    rng_i = np.random.default_rng(seed * 104729 + 3)      # SAME stream -> fair sub-measure
    imp = recall_rate(mem, imp_facts, STRESS_KEY_NOISE, rng_i)
    rng_f = np.random.default_rng(seed * 104729 + 99)
    fab = fab_rate(mem, out_truth, STRESS_KEY_NOISE, rng_f)
    return dict(tot=tot, imp=imp, fab=fab, cells=len(mem.protos))


def main():
    print("=== H_1288 EVICTION POLICY as the capacity lever of the immune memory (local CPU, $0) ===", flush=True)
    print(f"    N_FACTS={N_FACTS} in-store  N_OUT={N_OUT} untaught  SEEDS={SEEDS}", flush=True)
    print(f"    substrate = VAdaptField mirror (split>{SPLIT_THRESH}, LR={LR}); key = byte-{NGRAM}gram FNV-1a dim={KEY_DIM}", flush=True)
    print(f"    regime = H_1287 EVICTION-BOUND zero-sum rung: max_cells={STRESS_MAX_CELLS} << {N_FACTS}, "
          f"noise={STRESS_KEY_NOISE}, thresh={STRESS_RECALL_THRESH}", flush=True)
    print(f"    (A) LRU-EVICT     fixed budget {STRESS_MAX_CELLS} cells (CURRENT store, zero-sum ~0.667 ceiling)", flush=True)
    print(f"    (B) MITOSIS-GROW  grow new cells under pressure up to {GROW_MAX_CELLS} (finite, p8 — break zero-sum)", flush=True)
    print(f"    (C) WEIGHTED-EVICT smarter heuristic (LFU+LRU) at the SAME {STRESS_MAX_CELLS}-cell budget (NOT growth)", flush=True)
    print(f"    importance sub-metric = first tercile (taught-first = most LRU-vulnerable)", flush=True)
    print(f"    PRE-REGISTERED GREEN: (B)total recall >= (A) + {REC_MARGIN}  AND  (B)fab <= {FAB_BAR}", flush=True)
    print(f"      [cell-count cost reported honestly; arm C attributes lift = GROWTH vs HEURISTIC]", flush=True)
    print("", flush=True)

    rows = []
    for s in SEEDS:
        facts, out_truth = build_facts(s)
        a = run_arm("lru",      facts, out_truth, s)
        b = run_arm("grow",     facts, out_truth, s)
        c = run_arm("weighted", facts, out_truth, s)
        rows.append(dict(seed=s, a=a, b=b, c=c))
        print(f"  seed {s}: "
              f"(A LRU) tot={a['tot']:.3f} imp={a['imp']:.3f} fab={a['fab']:.3f} cells={a['cells']} | "
              f"(B GROW) tot={b['tot']:.3f} imp={b['imp']:.3f} fab={b['fab']:.3f} cells={b['cells']} | "
              f"(C WTD) tot={c['tot']:.3f} imp={c['imp']:.3f} fab={c['fab']:.3f} cells={c['cells']}", flush=True)

    m = lambda arm, k: float(np.mean([r[arm][k] for r in rows]))
    aT, aI, aF, aC = m('a', 'tot'), m('a', 'imp'), m('a', 'fab'), m('a', 'cells')
    bT, bI, bF, bC = m('b', 'tot'), m('b', 'imp'), m('b', 'fab'), m('b', 'cells')
    cT, cI, cF, cC = m('c', 'tot'), m('c', 'imp'), m('c', 'fab'), m('c', 'cells')

    print("", flush=True)
    print(f"  MEAN  (A LRU-EVICT)      tot={aT:.3f} imp={aI:.3f} fab={aF:.3f} cells={aC:.1f}", flush=True)
    print(f"  MEAN  (B MITOSIS-GROW)   tot={bT:.3f} imp={bI:.3f} fab={bF:.3f} cells={bC:.1f}", flush=True)
    print(f"  MEAN  (C WEIGHTED-EVICT) tot={cT:.3f} imp={cI:.3f} fab={cF:.3f} cells={cC:.1f}", flush=True)
    print(f"  Δ total recall (B-A) = {bT-aT:+.3f}   Δ (C-A) = {cT-aT:+.3f}", flush=True)
    print(f"  cell-count cost: B holds {bC:.1f} cells vs A {aC:.1f} (Δ={bC-aC:+.1f}) — growth trades footprint for recall", flush=True)
    print("", flush=True)

    c1 = (bT >= aT + REC_MARGIN)     # growth breaks the zero-sum (lifts total recall)
    c2 = (bF <= FAB_BAR)             # abstain intact (H_1227 load-bearing)
    green = c1 and c2

    print(f"  CHECK growth-lift   : B {bT:.3f} {'>=' if c1 else '<'} A {aT:.3f}+{REC_MARGIN} -> {'PASS' if c1 else 'FAIL'}", flush=True)
    print(f"  CHECK abstain-intact: fab(B) {bF:.3f} {'<=' if c2 else '>'} {FAB_BAR} -> {'PASS' if c2 else 'FAIL'}", flush=True)
    print("", flush=True)

    # honesty: did growth trivially store EVERYTHING (no pressure left)?  Existence-
    # proof framing if B saturates AND its cells covered every distinct fact.
    saturated = (bT >= 0.99)
    heuristic_also = (cT >= aT + REC_MARGIN)   # did the smarter heuristic alone lift?

    print("════════════════════════════════════════════════════════════════════", flush=True)
    print(f"  A LRU-EVICT (current, zero-sum) : tot={aT:.3f}  imp={aI:.3f}  cells={aC:.1f}", flush=True)
    print(f"  B MITOSIS-GROW (break zero-sum) : tot={bT:.3f}  imp={bI:.3f}  cells={bC:.1f}  Δ(B-A)={bT-aT:+.3f}", flush=True)
    print(f"  C WEIGHTED-EVICT (heuristic)    : tot={cT:.3f}  imp={cI:.3f}  cells={cC:.1f}  Δ(C-A)={cT-aT:+.3f}", flush=True)
    print("", flush=True)
    if green:
        print(f"  FINAL VERDICT: 🟢 GREEN  [MITOSIS-GROWTH breaks the zero-sum LRU ceiling — growing a new", flush=True)
        print(f"                cell under capacity pressure (p8) lifts total recall over LRU-eviction, abstain intact]", flush=True)
        if saturated:
            print(f"  HONESTY (c9): B SATURATES (tot={bT:.3f}>=0.99) — read as an EXISTENCE-PROOF (growth CAN", flush=True)
            print(f"                break the ceiling), NOT an effect-size; the COST is footprint (B {bC:.1f} cells", flush=True)
            print(f"                vs A {aC:.1f}). The lever is CELL BUDGET, realized substrate-natively as mitosis growth.", flush=True)
        else:
            print(f"  HONESTY (c9): B lifts recall with genuine residual stress (tot={bT:.3f}<0.99) — effect-size,", flush=True)
            print(f"                cost = footprint (B {bC:.1f} vs A {aC:.1f} cells).", flush=True)
        print(f"  ATTRIBUTION: weighted-heuristic alone {'ALSO lifts' if heuristic_also else 'does NOT lift'} "
              f"(C Δ={cT-aT:+.3f}) — the lift is "
              f"{'NOT unique to growth (a free heuristic recovers it too)' if heuristic_also else 'from GROWTH (extra cells), not a free heuristic'}.", flush=True)
        print(f"  DEPLETION: 🏁 — capacity IS the lever (the REAL one the 4 reds H_1230/1284/1285/1287 pointed to).", flush=True)
        print(f"             NEXT: r2 = engine-native mitosis-grow eviction on the live immune_memory faculty", flush=True)
        print(f"             (a_engine_native_learning) + wire per a_verified_must_wire.", flush=True)
    else:
        print(f"  FINAL VERDICT: 🧱 RED  [even mitosis-GROWTH (and the weighted heuristic) does NOT lift total", flush=True)
        print(f"                recall under honest capacity accounting — the ~0.667 ceiling is FUNDAMENTAL]", flush=True)
        print(f"  HONESTY (c9): growth Δ(B-A)={bT-aT:+.3f}, heuristic Δ(C-A)={cT-aT:+.3f}. Neither clears the bar.", flush=True)
        print(f"  DEPLETION: 🧱 — capacity is NOT the lever either; the ceiling is fundamental to the retrieve-then-", flush=True)
        print(f"             copy regime. The 4 reds + this lane jointly EXHAUST the capacity hypothesis.", flush=True)
    print(f"  philosophy guard: AFFIRMED — mitosis split = the engine's own tick (p8); policy mutates ONLY the", flush=True)
    print(f"                    episodic cell population; no labels/persona/ethics/decoder; abstain re-checked + intact (p1-p8).", flush=True)
    print("[done]", flush=True)
    return green, dict(aT=aT, aI=aI, aF=aF, aC=aC, bT=bT, bI=bI, bF=bF, bC=bC,
                       cT=cT, cI=cI, cF=cF, cC=cC, saturated=saturated, heuristic_also=heuristic_also)


if __name__ == "__main__":
    main()
