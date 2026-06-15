"""
H_1285 — AMYGDALA (편도체): salience-weighted binding of the immune memory store.

MISSING-BRAIN-STRUCTURE LADDER (neuro lens, c15; NOT an LLM recipe). p7, $0 local
CPU numpy, gradient-free. Builds DIRECTLY on H_1227 (immune/clonal memory mirror
GREEN), H_1231 (engine-native GREEN on the LIVE CORE/engine_cli.hexa VAdaptField),
and H_1230 (the capacity/noise-geometry bottleneck: under a finite repertoire,
LRU eviction is SYMMETRIC and active teaching gave ZERO retention lift).

THESIS. The hippocampus gap is filled by the immune memory; H_1230 found its
bottleneck is CAPACITY/NOISE GEOMETRY (cells << facts → LRU eviction, every fact
equally evictable). The missing structure here is the AMYGDALA: fast salience/
valence tagging that PRIORITIZES which inputs get bound (stronger/protected) and
which drive emit, by surprise/novelty/importance. The immune store binds every
fact UNIFORMLY (H_1227/H_1231); there is NO tagger that protects a salient cell
from eviction. H_1230 explicitly did NOT test salience-weighted binding — it is the
candidate lever this H probes.

  does deriving a SALIENCE signal from the substrate (surprise/novelty/tension) and
  using it to PROTECT high-salience cells from eviction lift retention of the
  IMPORTANT facts under the SAME capacity stress H_1230 left open?

────────────────────────────────────────────────────────────────────────────────
PHILOSOPHY GUARD — p6 IS CENTRAL (the salience-vs-label separation, stated):

  Salience MUST be a SUBSTRATE SIGNAL derived from surprise/novelty/tension
  (E+W+MITOSIS), NOT injected emotion, NOT RLHF valence, NOT a hardcoded
  "this is important" label fed INTO the mechanism.

   * The tagger DERIVES salience ONLY from the substrate at bind time:
       salience = f( SURPRISE = VAdaptField recon-err (L2 novelty of the key vs the
                                current cell population),
                     NOVELTY  = whether the key triggers a fresh clonal split,
                     TENSION  = repetition/reinforcement pressure across exposures ).
     All three are read off the mitosis substrate (recon-err, split, exposure count)
     — the SAME signals VAdaptField already computes. f() reads NO emotion, NO RLHF
     reward, NO label.
   * We DO label a subset "important" — used ONLY to SCORE the metric, NEVER as an
     input to f(). To make substrate-salience CORRELATE with importance WITHOUT
     leaking the label, the important facts genuinely recur/surprise more in the
     input stream (an environmental property; a biologically salient event recurs).
     The tagger senses only the surprise/novelty/tension.
   * NEGATIVE-CONTROL (B-shuffle): salience tags PERMUTED across cells (same
     distribution, decorrelated from importance). If B beats A but B-shuffle does
     NOT, the lift came from salience TRACKING importance via the substrate signal,
     not a label leak or mere score variance. If B-shuffle ALSO lifts → label-leak
     → RED on the honest reading.

  No persona, no ethics, no decoder, no weights are taught — only the EPISODIC cell
  store's eviction PRIORITY changes (p1/p2/p3/p6/p8, a_autonomy_over_hardcode).
────────────────────────────────────────────────────────────────────────────────

SUBSTRATE. numpy mirror of CORE/engine_cli.hexa VAdaptField + H_1227 immune value-
binding (proto keys; nearest by L2; recon-err=L2; novelty-split when recon-err >
SPLIT_THRESH=0.30; LR=0.20 winner pull; finite repertoire eviction). Keys = byte-
trigram FNV-1a hash DIM=64 (H_1227). Corpus = H_1222/H_1227/H_1230 "<subj> lives in
<city>". The ONLY added mechanism = SALIENCE-WEIGHTED EVICTION (evict lowest
salience+recency instead of LRU). LIVE .hexa engine UNTOUCHED (numpy mirror is
DIRECTIONAL; engine-native is the follow-on on GREEN, a_engine_native_learning).

REGIME. STRESS (JUDGED) = H_1230 rung: MAX_CELLS=40 << N_FACTS=60, cue noise 0.02,
RECALL_THRESH=0.30 — eviction is the lossy factor, headroom exists. CLEAN (control)
= unbounded, byte-exact, saturating non-separator.

FROZEN bars (see H_1285_FREEZE.txt — pre-registered, NOT moved):
  GREEN iff  (c1) B.imp-recall >= A.imp-recall + 0.10
        AND  (c2) B-shuffle.imp-recall < A.imp-recall + 0.10
        AND  (c3) B.fabrication <= 0.10.
"""
import numpy as np

# ─── frozen knobs (pre-registered — inherited from H_1227/H_1230) ───────────
SEEDS         = [900, 901, 902]
N_FACTS       = 60
N_OUT         = 60
N_IMPORTANT   = 20                # labeled-important subset (scored only)
KEY_DIM       = 64
NGRAM         = 3
SPLIT_THRESH  = 0.30              # VAdaptField novelty split (CORE/engine_cli.hexa)
LR            = 0.20              # winner online pull (VAdaptField)

# EQUAL exposure budget BOTH arms; salience comes from the input-stream recurrence
# of the important facts (environmental property the substrate SENSES, not a label).
EXPOSURE_MULT     = 3             # base budget = N_FACTS * EXPOSURE_MULT
SALIENCE_RECUR    = 3             # important facts get this many EXTRA exposures each,
                                  # woven into the SAME total budget (no extra data:
                                  # unimportant facts drop a proportional count so the
                                  # TOTAL exposures are identical across arms & equal
                                  # to N_FACTS*EXPOSURE_MULT).

# STRESS regime — the H_1230 decisive rung (finite repertoire + small cue noise).
STRESS_MAX_CELLS     = 40
STRESS_KEY_NOISE     = 0.02
STRESS_RECALL_THRESH = 0.30

# pre-registered GREEN bars (FROZEN)
IMP_MARGIN = 0.10
FAB_BAR    = 0.10

# salience tag mixing (substrate-derived; documented constants, not tuned-to-green).
# salience_tag = SURPRISE_W*recon_err_at_bind + NOVELTY_W*was_split + TENSION_W*reinforce
SURPRISE_W = 1.0
NOVELTY_W  = 0.5
TENSION_W  = 0.5

DICT_PATH = "/usr/share/dict/words"


# ─── corpus / facts (known ground truth, H_1222/H_1227 paradigm) ────────────
def load_words():
    with open(DICT_PATH) as f:
        return [w.strip().lower() for w in f if w.strip().isalpha()]


def build_facts(seed):
    rng = np.random.default_rng(seed)
    allw = load_words()
    cap = [w for w in allw if 4 <= len(w) <= 8]
    pick = lambda pool, n: list(rng.choice(pool, size=n, replace=False))
    subj_pool = [w.capitalize() for w in pick(cap, N_FACTS + N_OUT)]
    cities    = [w.capitalize() for w in pick(cap, N_FACTS + N_OUT)]
    in_subj, out_subj = subj_pool[:N_FACTS], subj_pool[N_FACTS:]
    facts = [(in_subj[i], cities[i]) for i in range(N_FACTS)]
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
    b = text.encode("utf-8")
    v = np.zeros(dim, dtype=float)
    if len(b) < n:
        v[_fnv1a(b) % dim] += 1.0
    else:
        for i in range(len(b) - n + 1):
            v[_fnv1a(b[i:i + n]) % dim] += 1.0
    nrm = np.linalg.norm(v)
    return v / nrm if nrm > 0 else v


# ─── MITOSIS MEMORY (numpy mirror of VAdaptField + immune value-binding +
#     SALIENCE-WEIGHTED EVICTION — the only added mechanism) ────────────────
class MitosisMemory:
    """A population of memory cells (proto key, bound answer, salience tag).
    Mirrors CORE/engine_cli.hexa vadapt_field_step (nearest by L2, recon-err = L2,
    novelty-split when err > SPLIT_THRESH, LR winner-pull on a hit). The immune
    value-binding (H_1227) stores a bound answer per cell. The AMYGDALA extension
    (H_1285) stores a per-cell SALIENCE tag and, under a finite repertoire, evicts
    the LOWEST salience+recency cell instead of pure LRU.

    salience_mode:
      'none'     — pure LRU eviction (ARM A, H_1227/H_1230 baseline; tag ignored).
      'salience' — evict lowest (salience_tag + recency) (ARM B).
      'shuffle'  — same as 'salience' but the salience tags are PERMUTED across
                   cells once binding is done — NEGATIVE CONTROL (decorrelated from
                   importance; tests whether the lift TRACKS importance, p6 guard).

    The salience TAG is computed from the SUBSTRATE ONLY (recon-err at bind = surprise,
    was-split = novelty, reinforcement count = tension). NO label is read here."""

    def __init__(self, max_cells=None, recall_thresh=STRESS_RECALL_THRESH,
                 salience_mode='none'):
        self.protos = []
        self.values = []
        self.last_used = []
        self.salience = []          # per-cell substrate-derived salience tag
        self.max_cells = max_cells
        self.recall_thresh = recall_thresh
        self.salience_mode = salience_mode
        self._tick = 0

    def _nearest(self, key):
        if not self.protos:
            return -1, float("inf")
        d = [np.linalg.norm(p - key) for p in self.protos]
        j = int(np.argmin(d))
        return j, float(d[j])

    def _evict_index(self):
        """Which cell to evict when at capacity.
        ARM A ('none'): least-recently-used (the H_1227/H_1230 rule).
        ARM B ('salience'/'shuffle'): lowest (salience + normalized recency) — a
        high-salience cell is PROTECTED. recency is normalized to the same scale as
        salience so both contribute (amygdala: salient memories resist decay)."""
        if self.salience_mode == 'none':
            return int(np.argmin(self.last_used))
        # normalize recency to [0,1] over current cells, add salience tag
        lu = np.asarray(self.last_used, dtype=float)
        rng = lu.max() - lu.min()
        rec = (lu - lu.min()) / rng if rng > 0 else np.zeros_like(lu)
        protect = np.asarray(self.salience, dtype=float) + rec
        return int(np.argmin(protect))

    def _add_cell(self, key, answer, salience):
        self._tick += 1
        if self.max_cells is not None and len(self.protos) >= self.max_cells:
            e = self._evict_index()
            self.protos[e] = key.copy(); self.values[e] = answer
            self.last_used[e] = self._tick; self.salience[e] = salience
        else:
            self.protos.append(key.copy()); self.values.append(answer)
            self.last_used.append(self._tick); self.salience.append(salience)

    def bind(self, question, answer):
        """One EXPOSURE. SUBSTRATE-derived salience: surprise = recon-err of the key
        vs the current population BEFORE binding; novelty = whether it splits; tension
        = reinforcement (a hit refreshes + RAISES the existing cell's salience). The
        tag is read off the substrate, not from any label."""
        self._tick += 1
        key = embed_key(question)
        j, err = self._nearest(key)
        was_split = (j < 0 or err > SPLIT_THRESH)
        # SURPRISE: recon-err to nearest BEFORE binding (∞→1.0 for the empty store).
        surprise = 1.0 if j < 0 else min(err, 1.0)
        novelty = 1.0 if was_split else 0.0
        tag = SURPRISE_W * surprise + NOVELTY_W * novelty   # TENSION added on reinforce
        if was_split:
            self._add_cell(key, answer, tag)
        else:
            self.protos[j] += LR * (key - self.protos[j])   # clonal expansion
            self.values[j] = answer
            self.last_used[j] = self._tick
            # TENSION: reinforcement raises the cell's salience (repetition-pressure).
            self.salience[j] += TENSION_W

    def freeze_shuffle(self, rng):
        """B-shuffle control: PERMUTE the salience tags across cells so they are
        decorrelated from importance (same distribution, no label tracking)."""
        if self.salience_mode == 'shuffle' and self.salience:
            perm = rng.permutation(len(self.salience))
            self.salience = [self.salience[i] for i in perm]

    def recall(self, question, noise=0.0, rng=None):
        key = embed_key(question)
        if noise > 0.0 and rng is not None:
            key = key + rng.normal(0.0, noise, size=key.shape)
        j, err = self._nearest(key)
        if j < 0 or err > self.recall_thresh:
            return None
        self.last_used[j] = max(self.last_used[j], self._tick)
        return self.values[j]


# ─── exposure stream (identical for ALL arms; salience from RECURRENCE) ─────
def build_stream(facts, important_idx, rng):
    """Build ONE exposure list (fact indices) of the SAME total length for all arms.
    Important facts RECUR more (SALIENCE_RECUR extra exposures each) — an
    environmental property; the substrate later SENSES it via reinforcement-tension.
    Total budget held EXACTLY at N_FACTS*EXPOSURE_MULT by dropping a proportional
    number of unimportant exposures (NO extra data; same byte-budget both arms)."""
    budget = N_FACTS * EXPOSURE_MULT
    imp = set(important_idx)
    # base: one exposure per fact
    stream = list(range(N_FACTS))
    # add SALIENCE_RECUR extra exposures of each important fact
    for i in important_idx:
        stream += [i] * SALIENCE_RECUR
    # fill the rest of the budget with round-robin over UNIMPORTANT facts (so the
    # extra weight is spent on importance, not on padding everything equally)
    unimp = [i for i in range(N_FACTS) if i not in imp]
    k = 0
    while len(stream) < budget:
        stream.append(unimp[k % len(unimp)]); k += 1
    # if we overshot the budget (recurrence > remaining), TRUNCATE deterministically
    # but keep every fact at least once + every important recurrence (drop unimp tail)
    if len(stream) > budget:
        # remove from the trailing unimportant fill first
        head = list(range(N_FACTS)) + [i for i in important_idx for _ in range(SALIENCE_RECUR)]
        extra = budget - len(head)
        stream = head + ([unimp[j % len(unimp)] for j in range(max(0, extra))] if extra > 0 else [])
        stream = stream[:budget]
    rng.shuffle(stream)   # interleave (same shuffled stream handed to every arm)
    return stream


# ─── retention helpers ──────────────────────────────────────────────────────
def recall_subset(mem, facts, idxs, noise, rng):
    hits = 0
    for i in idxs:
        subj, city = facts[i]
        r = mem.recall(f"{subj} lives in ", noise=noise, rng=rng)
        if r is not None and r.lower() == city.lower():
            hits += 1
    return hits / max(1, len(idxs))


def fab_rate(mem, out_truth, noise, rng):
    fires = sum(1 for subj, _ in out_truth
                if mem.recall(f"{subj} lives in ", noise=noise, rng=rng) is not None)
    return fires / max(1, len(out_truth))


# ─── run one arm over a fixed stream ────────────────────────────────────────
def run_arm(facts, stream, cfg, salience_mode, shuffle_rng=None):
    mem = MitosisMemory(max_cells=cfg["max_cells"], recall_thresh=cfg["recall_thresh"],
                        salience_mode=salience_mode)
    for i in stream:
        subj, city = facts[i]
        mem.bind(f"{subj} lives in ", city)
    if salience_mode == 'shuffle':
        mem.freeze_shuffle(shuffle_rng)
    return mem


def run_seed(seed, cfg):
    facts, out_truth = build_facts(seed)
    stream_rng = np.random.default_rng(seed * 7919 + 5)
    important_idx = list(range(N_IMPORTANT))   # labeled subset (METRIC ONLY)
    unimportant_idx = list(range(N_IMPORTANT, N_FACTS))
    stream = build_stream(facts, important_idx, stream_rng)

    def evals(mem):
        er = np.random.default_rng(seed * 104729 + 3)   # SAME eval-noise stream/arm
        imp = recall_subset(mem, facts, important_idx, cfg["noise"], er)
        er2 = np.random.default_rng(seed * 104729 + 3)
        tot = recall_subset(mem, facts, list(range(N_FACTS)), cfg["noise"], er2)
        er3 = np.random.default_rng(seed * 104729 + 3)
        unimp = recall_subset(mem, facts, unimportant_idx, cfg["noise"], er3)
        er4 = np.random.default_rng(seed * 104729 + 99)
        fab = fab_rate(mem, out_truth, cfg["noise"], er4)
        return imp, tot, unimp, fab

    memA = run_arm(facts, stream, cfg, 'none')
    impA, totA, unimpA, fabA = evals(memA)

    memB = run_arm(facts, stream, cfg, 'salience')
    impB, totB, unimpB, fabB = evals(memB)

    sh_rng = np.random.default_rng(seed * 31337 + 11)
    memS = run_arm(facts, stream, cfg, 'shuffle', shuffle_rng=sh_rng)
    impS, totS, unimpS, fabS = evals(memS)

    return dict(seed=seed,
                impA=impA, totA=totA, unimpA=unimpA, fabA=fabA, cellsA=len(memA.protos),
                impB=impB, totB=totB, unimpB=unimpB, fabB=fabB, cellsB=len(memB.protos),
                impS=impS, totS=totS, unimpS=unimpS, fabS=fabS)


def run_regime(name, cfg, judged):
    print(f"── REGIME: {name}  "
          f"(max_cells={cfg['max_cells']}, key_noise={cfg['noise']}, recall_thresh={cfg['recall_thresh']})"
          f"{'   [JUDGED]' if judged else '   [control]'}", flush=True)
    rows = [run_seed(s, cfg) for s in SEEDS]
    for r in rows:
        print(f"  seed {r['seed']}: "
              f"(A uniform) imp={r['impA']:.3f} tot={r['totA']:.3f} unimp={r['unimpA']:.3f} fab={r['fabA']:.3f} cells={r['cellsA']} | "
              f"(B salience) imp={r['impB']:.3f} tot={r['totB']:.3f} unimp={r['unimpB']:.3f} fab={r['fabB']:.3f} cells={r['cellsB']} | "
              f"(B-shuf) imp={r['impS']:.3f}", flush=True)
    m = lambda k: float(np.mean([r[k] for r in rows]))
    impA, impB, impS = m('impA'), m('impB'), m('impS')
    totA, totB = m('totA'), m('totB')
    unimpA, unimpB = m('unimpA'), m('unimpB')
    fabA, fabB = m('fabA'), m('fabB')
    print(f"  MEAN (A uniform)  imp={impA:.3f} tot={totA:.3f} unimp={unimpA:.3f} fab={fabA:.3f}", flush=True)
    print(f"  MEAN (B salience) imp={impB:.3f} tot={totB:.3f} unimp={unimpB:.3f} fab={fabB:.3f}", flush=True)
    print(f"  MEAN (B-shuffle)  imp={impS:.3f}  [negative control: salience decorrelated from importance]", flush=True)
    print(f"  Δ important-recall (B-A) = {impB-impA:+.3f}   Δ total (B-A) = {totB-totA:+.3f}   Δ unimp (B-A) = {unimpB-unimpA:+.3f}", flush=True)
    c1 = (impB >= impA + IMP_MARGIN)
    c2 = (impS <  impA + IMP_MARGIN)
    c3 = (fabB <= FAB_BAR)
    green = c1 and c2 and c3
    print(f"  CHECK c1 imp-margin:  B {impB:.3f} {'>=' if c1 else '<'} A {impA:.3f}+{IMP_MARGIN} -> {'PASS' if c1 else 'FAIL'}", flush=True)
    print(f"  CHECK c2 shuffle-ctrl: B-shuf {impS:.3f} {'<' if c2 else '>='} A {impA:.3f}+{IMP_MARGIN} -> {'PASS' if c2 else 'FAIL'}", flush=True)
    print(f"  CHECK c3 fabrication:  B {fabB:.3f} {'<=' if c3 else '>'} {FAB_BAR} -> {'PASS' if c3 else 'FAIL'}", flush=True)
    print(f"  -> {name}: {'🟢 GREEN' if green else '🔴 RED'}", flush=True)
    print("", flush=True)
    return dict(name=name, green=green, impA=impA, impB=impB, impS=impS,
                totA=totA, totB=totB, unimpA=unimpA, unimpB=unimpB,
                fabA=fabA, fabB=fabB, c1=c1, c2=c2, c3=c3)


def main():
    print("=== H_1285 AMYGDALA salience-weighted binding of the immune memory (local CPU, $0, p7) ===", flush=True)
    print(f"    N_FACTS={N_FACTS} (N_IMPORTANT={N_IMPORTANT} labeled subset, METRIC-ONLY)  N_OUT={N_OUT} untaught  SEEDS={SEEDS}", flush=True)
    print(f"    substrate = VAdaptField mirror (split>{SPLIT_THRESH}, LR={LR}); key = byte-{NGRAM}gram FNV-1a dim={KEY_DIM}", flush=True)
    print(f"    salience tag = {SURPRISE_W}*surprise(recon-err) + {NOVELTY_W}*novelty(split) + {TENSION_W}*tension(reinforce)  [SUBSTRATE-DERIVED, no label]", flush=True)
    print(f"    EQUAL budget = N_FACTS*{EXPOSURE_MULT} = {N_FACTS*EXPOSURE_MULT} exposures; important facts recur +{SALIENCE_RECUR} each (environmental salience)", flush=True)
    print(f"    (A) uniform LRU eviction (H_1227/H_1230)  vs  (B) salience-protected eviction  vs  (B-shuffle) permuted-salience control", flush=True)
    print(f"    PRE-REGISTERED GREEN (STRESS): (B)imp >= (A)imp+{IMP_MARGIN} AND (B-shuf)imp < (A)imp+{IMP_MARGIN} AND (B)fab <= {FAB_BAR}", flush=True)
    print("", flush=True)

    clean_cfg  = dict(max_cells=None, noise=0.0, recall_thresh=0.15)
    stress_cfg = dict(max_cells=STRESS_MAX_CELLS, noise=STRESS_KEY_NOISE, recall_thresh=STRESS_RECALL_THRESH)

    clean  = run_regime("CLEAN  (unbounded, byte-exact cue)", clean_cfg,  judged=False)
    stress = run_regime("STRESS (finite repertoire 40<<60, modest noise)", stress_cfg, judged=True)

    green = stress["green"]
    print("════════════════════════════════════════════════════════════════════", flush=True)
    print(f"  CLEAN  control: A imp={clean['impA']:.3f} B imp={clean['impB']:.3f}  (saturating — no eviction, no headroom)", flush=True)
    print(f"  STRESS judged : A imp={stress['impA']:.3f} B imp={stress['impB']:.3f} Δ={stress['impB']-stress['impA']:+.3f}  "
          f"B-shuf imp={stress['impS']:.3f}  fabB={stress['fabB']:.3f}", flush=True)
    print(f"  STRESS trade-off: total A={stress['totA']:.3f} B={stress['totB']:.3f}   unimportant A={stress['unimpA']:.3f} B={stress['unimpB']:.3f}", flush=True)
    print("", flush=True)
    print(f"  FINAL VERDICT: {'🟢 GREEN' if green else '🔴 RED'}  "
          f"[substrate-salience-weighted eviction {'PROTECTS' if green else 'does NOT protect'} important facts "
          f"under capacity stress, STRESS rung]", flush=True)
    print(f"  philosophy guard: salience DERIVED from substrate (surprise/novelty/tension), NOT a label; "
          f"B-shuffle control decorrelates salience from importance (c2). No decoder/weights/persona/ethics (p1/p2/p3/p6/p8).", flush=True)
    print("[done]", flush=True)
    return green, clean, stress


if __name__ == "__main__":
    main()
