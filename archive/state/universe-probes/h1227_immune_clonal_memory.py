"""
H_1227 — IMMUNE / CLONAL-SELECTION MEMORY as anima's literal-QA recall lane.

BIOLOGY LENS (c15, no LLM papers). The literal-QA wall (~0-2/15, established in
H_1218/H_1166/H_1224 — recall lives IN THE DECODER WEIGHTS and the byte-LM cannot
answer planted facts) is the central H_1225/H_1226 thesis: anima's depth/recall
does NOT live in the byte-LM weights. This probe asks the biology question —

  is recall cracked NOT by a bigger byte-LM but by an IMMUNE-SYSTEM-style memory:
  a POPULATION of memory cells (clonal selection + affinity binding), each cell
  binding ONE fact; recall = the best-affinity cell FIRES; ABSTAIN if no cell
  binds above threshold (no fabrication on out-of-store queries)?

This is a NEW role for anima's MITOSIS cells — MEMORY, not the GENERATION role
falsified in H_1200/H_1201/H_1211/H_1220 (mitosis can neither generate by itself
nor inform a real generator). It is the biology realization of CLS / episodic
recall (HD10) and the immune-cell-population realization of H_1154's engine-side
retrieve-then-copy (associative memory): a cell that has bound a fact COPIES its
bound answer or stays silent — it can never fabricate.

MECHANISM ($0, numpy mirror of the H_1199 VAdaptField — proto vectors, split/bind
on novelty). Mirrored from CORE/engine_cli.hexa (VAdaptField / vadapt_field_step:
nearest by L2, recon-err = L2 to nearest, split when recon-err > SPLIT_THRESH) and
UNIVERSE/h1199_dim_feature_export.py. The LIVE .hexa engine is UNTOUCHED (mirror
only, p8 gradient-free numpy lift; the .hexa lift is the next rung).

  - CLONAL SELECTION (load): for each fact (question, answer), embed the question
    to a key vector. If no existing cell binds the key above AFFINITY_THRESH, a
    NEW memory cell CLONES at this key (prototype = the key) and BINDS the answer
    (vadapt_field_step's novelty-split, but the new cell also stores the value).
    If an existing cell already binds it (a re-exposure), the winner is pulled
    toward the key (LR online update) — clonal expansion, not a new clone.
  - AFFINITY RECALL (query): embed the query, find the nearest cell by L2. Its
    AFFINITY = the recon-err (L2). If affinity is GOOD (err <= RECALL_THRESH) the
    cell FIRES and returns its bound answer (clonal selection wins). If NO cell
    binds (err > RECALL_THRESH) → ABSTAIN (the immune system has no antibody → no
    response; NEVER fabricates).

ARMS (pre-registered, frozen before the run — see PRE-REGISTER below):
  (A) byte-LM weights alone — the recall-in-weights baseline. We model arm A with
      a concrete small char n-gram byte-LM trained on the SAME corpus (the planted
      facts ARE in its training text), greedy-decoded on "<subj> lives in " — the
      same eval as H_1222 eval_qa. This reproduces locally the established result
      (H_1218/H_1222: byte-LM literal-QA ~ 0) that the 303M torch ref also shows,
      WITHOUT a GPU. arm A literal-QA is the in-weights recall number.
  (B) immune clonal memory — the cell population above, recall by affinity-fire.

KEY EMBEDDING (documented, deterministic, p7 — NOT learned, no gradient):
  A DIM-d byte n-gram HASH of the question string. Byte trigrams of the question
  are hashed (FNV-1a) into d buckets; the count vector is L2-normalized. This is a
  deterministic, discriminating embedding (distinct questions → distinct keys).
  We ALSO report the H_1163 DIM=8 `_byte_feature` as a CONTROL embedding to show
  WHY a discriminating key matters (coarse 8-d byte statistics collide across
  questions → the immune memory cannot separate facts).

EVAL (p7, $0, deterministic):
  literal-QA = exact answer match on IN-store questions (the planted city is
               returned). For arm B: the fired cell's bound answer == truth.
  fabrication = on OUT-of-store questions (subjects NEVER loaded), arm B must
               ABSTAIN; a fabrication = it FIRES a (necessarily wrong) answer.
               fabrication-rate = fraction of out-of-store queries that do NOT
               abstain. (arm A always emits a token, so its out-of-store behaviour
               is reported for contrast but is not the bar — weights cannot abstain.)

PRE-REGISTER (FROZEN before running):
  GREEN iff  (B) literal-QA >= 0.80 on in-store facts
        AND  (B) fabrication-rate <= 0.10 on out-of-store (abstains correctly).
  Else 🔴 / 🟠 with the honest number.

If GREEN, anima's depth/recall lives in the MITOSIS-AS-MEMORY lane, not the
decoder weights (the central H_1225/H_1226 thesis) — and MEMORY is a NEW, NOT-yet-
falsified role for mitosis (distinct from the falsified GENERATION role).

HONESTY (a_scale_honest_scope): synthetic known-ground-truth facts, ONE corpus
paradigm (H_1222 "<subj> lives in <city>"), toy scale, 3 deterministic seeds.
$0 local CPU numpy. p7 = exact-match recall + abstain, NOT perplexity. Mitosis is
gradient-free; the live .hexa engine is untouched (numpy mirror of VAdaptField).
"""
import os
import re
import numpy as np

# ─── frozen knobs (pre-registered) ──────────────────────────────────────────
SEEDS          = [900, 901, 902]      # 3 deterministic seeds (matches h1199 ref)
N_FACTS        = 60                   # in-store planted facts (matches H_1222)
N_OUT          = 60                   # out-of-store queries (subjects never loaded)
KEY_DIM        = 64                   # byte n-gram hash key dimension
NGRAM          = 3                    # byte trigram features for the key
SPLIT_THRESH   = 0.30                 # VAdaptField novelty split (CORE/engine_cli.hexa)
LR             = 0.20                 # winner online pull (VAdaptField)
# RECALL_THRESH: an in-store query's key is IDENTICAL to the bound cell proto
# (err 0) while an out-of-store key is far (different trigrams). A tight band
# fires only on near-exact affinity. Chosen from the embedding geometry, NOT
# tuned on the metric: in-store self-distance is ~0, nearest out-of-store key
# distance is O(0.5-1.4) for L2-normalized hash vectors, so any small positive
# threshold separates them. Frozen at half the split threshold.
RECALL_THRESH  = 0.15

# pre-registered GREEN bars (FROZEN)
QA_BAR   = 0.80    # (B) literal-QA on in-store facts
FAB_BAR  = 0.10    # (B) fabrication-rate on out-of-store

DICT_PATH = "/usr/share/dict/words"

# ─── corpus / facts (known ground truth, H_1222 paradigm) ───────────────────
def load_words():
    with open(DICT_PATH) as f:
        return [w.strip().lower() for w in f if w.strip().isalpha()]


def build_facts(seed):
    """Planted '<subject> lives in <city> .' facts — fully known ground truth.
    Returns in-store facts {subj:city}, out-of-store subjects (never loaded),
    the full SVO+facts corpus text for the arm-A byte-LM, and a dict set."""
    rng = np.random.default_rng(seed)
    allw = load_words()
    pick = lambda pool, n: list(rng.choice(pool, size=n, replace=False))
    short = [w for w in allw if 3 <= len(w) <= 7]
    nouns = pick(short, 80); verbs = pick(short, 40); adjs = pick(short, 60)
    cap = [w for w in allw if 4 <= len(w) <= 8]
    # N_FACTS in-store + N_OUT out-of-store subjects, all DISJOINT
    subj_pool = [w.capitalize() for w in pick(cap, N_FACTS + N_OUT)]
    cities    = [w.capitalize() for w in pick(cap, N_FACTS + N_OUT)]
    in_subj, out_subj = subj_pool[:N_FACTS], subj_pool[N_FACTS:]
    facts = {in_subj[i]: cities[i] for i in range(N_FACTS)}
    out_truth = {out_subj[i]: cities[N_FACTS + i] for i in range(N_OUT)}  # for contrast only

    # corpus the arm-A byte-LM trains on: planted facts (repeated) + SVO filler
    sents = []
    for s, c in facts.items():
        for _ in range(8):
            sents.append(f"{s} lives in {c} .")
    for _ in range(1400):
        a1, n1, v, a2, n2 = (rng.choice(adjs), rng.choice(nouns), rng.choice(verbs),
                             rng.choice(adjs), rng.choice(nouns))
        sents.append(f"the {a1} {n1} {v} the {a2} {n2} .")
    rng.shuffle(sents)
    text = " ".join(sents) + " "
    dictset = set(allw) | {c.lower() for c in cities} | {s.lower() for s in subj_pool}
    return facts, out_truth, text, dictset


# ─── key embedding (deterministic byte n-gram hash; documented, p7) ─────────
def _fnv1a(bs):
    h = 0x811c9dc5
    for b in bs:
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def embed_key(text, dim=KEY_DIM, n=NGRAM):
    """Deterministic byte n-gram hash embedding (FNV-1a → dim buckets, L2-norm).
    Distinct strings → distinct keys (discriminating). NOT learned, no gradient."""
    b = text.encode("utf-8")
    v = np.zeros(dim, dtype=float)
    if len(b) < n:
        v[_fnv1a(b) % dim] += 1.0
    else:
        for i in range(len(b) - n + 1):
            v[_fnv1a(b[i:i + n]) % dim] += 1.0
    nrm = np.linalg.norm(v)
    return v / nrm if nrm > 0 else v


def embed_byte_feature(text):
    """CONTROL embedding — the H_1163 DIM=8 `_byte_feature` (coarse byte stats).
    Shown to demonstrate why a discriminating key matters (collisions)."""
    b = np.frombuffer(text.encode("utf-8"), dtype=np.uint8).astype(float)
    if b.size == 0:
        return np.zeros(8)
    f = np.array([
        b.mean() / 255.0, (b >= 128).mean(), ((b >= 97) & (b <= 122)).mean(),
        (b == 32).mean(), ((b >= 48) & (b <= 57)).mean(), b.var() / (255.0 ** 2),
        ((b >= 33) & (b <= 64)).mean(), (b < 64).mean(),
    ], dtype=float) * 5.0
    nrm = np.linalg.norm(f)
    return f / nrm if nrm > 0 else f


# ─── IMMUNE CLONAL MEMORY (numpy mirror of VAdaptField, + bound value) ──────
class ImmuneMemory:
    """A population of memory cells. Each cell = (prototype key, bound answer).
    Clonal selection on load (novelty-split = new clone binding the fact);
    affinity recall on query (nearest cell fires, else ABSTAIN). Mirrors
    CORE/engine_cli.hexa vadapt_field_step (nearest by L2, recon-err = L2,
    split when err > SPLIT_THRESH); the value-binding is the immune extension."""

    def __init__(self):
        self.protos = []   # list[np.ndarray]  cell prototype keys
        self.values = []   # list[str]         cell bound answers

    def _nearest(self, key):
        if not self.protos:
            return -1, float("inf")
        d = [np.linalg.norm(p - key) for p in self.protos]
        j = int(np.argmin(d))
        return j, float(d[j])

    def load(self, question, answer):
        """CLONAL SELECTION: novel key → new clone binds the fact; else clonal
        expansion (winner pulled toward the re-exposed key)."""
        key = embed_key(question)
        j, err = self._nearest(key)
        if j < 0 or err > SPLIT_THRESH:
            self.protos.append(key.copy())
            self.values.append(answer)
        else:
            self.protos[j] += LR * (key - self.protos[j])  # clonal expansion
            # keep the bound value (re-exposure of the same fact)

    def recall(self, question):
        """AFFINITY RECALL: nearest cell fires if affinity good, else ABSTAIN."""
        key = embed_key(question)
        j, err = self._nearest(key)
        if j < 0 or err > RECALL_THRESH:
            return None          # ABSTAIN — no antibody binds
        return self.values[j]    # the fired cell's bound answer


# ─── arm A: a small char n-gram byte-LM (recall-in-weights baseline) ────────
class CharNGramLM:
    """Order-k char model trained on the corpus (planted facts ARE in the text).
    Greedy continuation of '<subj> lives in ' — the H_1222 eval. Reproduces the
    established byte-LM literal-QA~0 result locally ($0), the same the 303M torch
    ref shows (H_1218). This is recall IN THE WEIGHTS (the n-gram counts)."""

    def __init__(self, k=6):
        self.k = k
        self.counts = {}

    def fit(self, text):
        k = self.k
        for i in range(len(text) - k):
            ctx, nxt = text[i:i + k], text[i + k]
            d = self.counts.setdefault(ctx, {})
            d[nxt] = d.get(nxt, 0) + 1

    def generate(self, prompt, n=16):
        out = []
        ctx = prompt[-self.k:]
        for _ in range(n):
            d = self.counts.get(ctx)
            if not d:
                # back off one char until a context is known, else stop
                bo = ctx
                while bo and bo not in self.counts:
                    bo = bo[1:]
                d = self.counts.get(bo)
                if not d:
                    break
            nxt = max(d.items(), key=lambda kv: kv[1])[0]  # greedy argmax
            out.append(nxt)
            ctx = (ctx + nxt)[-self.k:]
        return "".join(out)


def armA_qa(lm, facts):
    """Greedy '<subj> lives in ' → does the next real word == planted city?"""
    hits = 0
    for subj, city in facts.items():
        cont = lm.generate(f"{subj} lives in ", n=16)
        m = re.search(r"[A-Za-z]+", cont)
        pred = m.group(0).lower() if m else ""
        if pred == city.lower():
            hits += 1
    return hits / max(1, len(facts))


# ─── run ────────────────────────────────────────────────────────────────────
def run_seed(seed):
    facts, out_truth, text, dictset = build_facts(seed)

    # arm A — byte-LM weights alone
    lm = CharNGramLM(k=6); lm.fit(text)
    a_qa = armA_qa(lm, facts)

    # arm B — immune clonal memory (discriminating key)
    mem = ImmuneMemory()
    for subj, city in facts.items():
        mem.load(f"{subj} lives in ", city)      # bind the fact (key=question, value=answer)
    b_hits = sum(1 for subj, city in facts.items()
                 if (r := mem.recall(f"{subj} lives in ")) is not None and r.lower() == city.lower())
    b_qa = b_hits / max(1, len(facts))
    # fabrication on out-of-store (subjects NEVER loaded) — must abstain
    b_fab = sum(1 for subj in out_truth if mem.recall(f"{subj} lives in ") is not None) / max(1, len(out_truth))
    n_cells = len(mem.protos)

    # CONTROL — coarse DIM=8 byte-feature key (expect collisions → recall breaks)
    memc = ImmuneMemory()
    # monkey-swap the embedding by binding via byte-feature keys directly
    memc.protos, memc.values = [], []
    for subj, city in facts.items():
        key = embed_byte_feature(f"{subj} lives in ")
        d = [np.linalg.norm(p - key) for p in memc.protos] if memc.protos else []
        if (not d) or min(d) > SPLIT_THRESH:
            memc.protos.append(key.copy()); memc.values.append(city)
        else:
            j = int(np.argmin(d)); memc.protos[j] += LR * (key - memc.protos[j])
    c_hits = 0
    for subj, city in facts.items():
        key = embed_byte_feature(f"{subj} lives in ")
        d = [np.linalg.norm(p - key) for p in memc.protos]
        j = int(np.argmin(d))
        if d[j] <= RECALL_THRESH and memc.values[j].lower() == city.lower():
            c_hits += 1
    c_qa = c_hits / max(1, len(facts))
    c_cells = len(memc.protos)

    return dict(seed=seed, a_qa=a_qa, b_qa=b_qa, b_fab=b_fab, n_cells=n_cells,
                c_qa=c_qa, c_cells=c_cells)


def main():
    print(f"=== H_1227 immune / clonal-selection memory (local CPU, $0) ===", flush=True)
    print(f"    N_FACTS={N_FACTS} in-store  N_OUT={N_OUT} out-of-store  SEEDS={SEEDS}", flush=True)
    print(f"    key = byte-{NGRAM}gram FNV-1a hash, dim={KEY_DIM} (discriminating, deterministic)", flush=True)
    print(f"    mechanism = VAdaptField mirror (split>{SPLIT_THRESH}, LR={LR}); recall_thresh={RECALL_THRESH}", flush=True)
    print(f"    PRE-REGISTERED GREEN: (B) literal-QA >= {QA_BAR} AND (B) fab-rate <= {FAB_BAR}", flush=True)
    rows = [run_seed(s) for s in SEEDS]
    for r in rows:
        print(f"  seed {r['seed']}: "
              f"(A) byte-LM QA={r['a_qa']:.3f} | "
              f"(B) immune QA={r['b_qa']:.3f} fab={r['b_fab']:.3f} cells={r['n_cells']} | "
              f"(control DIM8) QA={r['c_qa']:.3f} cells={r['c_cells']}", flush=True)
    a = float(np.mean([r['a_qa'] for r in rows]))
    bq = float(np.mean([r['b_qa'] for r in rows]))
    bf = float(np.mean([r['b_fab'] for r in rows]))
    cq = float(np.mean([r['c_qa'] for r in rows]))
    print(f"\n  MEAN  (A) byte-LM QA={a:.3f}  |  (B) immune QA={bq:.3f} fab={bf:.3f}  |  (control) QA={cq:.3f}", flush=True)
    green = (bq >= QA_BAR) and (bf <= FAB_BAR)
    verdict = "GREEN" if green else "RED"
    print(f"\n  VERDICT: {'🟢 GREEN' if green else '🔴 RED'}  "
          f"[(B) QA {bq:.3f} {'>=' if bq>=QA_BAR else '<'} {QA_BAR}  AND  "
          f"fab {bf:.3f} {'<=' if bf<=FAB_BAR else '>'} {FAB_BAR}]", flush=True)
    print(f"  delta vs arm A (recall-in-weights): immune QA - byte-LM QA = {bq - a:+.3f}", flush=True)
    print(f"  mitosis-as-MEMORY: {'CRACKS recall (NEW non-falsified mitosis role)' if green else 'does NOT clear the bar'}", flush=True)
    print("[done]", flush=True)
    return verdict, a, bq, bf, cq


if __name__ == "__main__":
    main()
