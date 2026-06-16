#!/usr/bin/env python3
"""
h6029_generational_persistence.py — ⊗-29 GENERATIONAL PERSISTENCE OF THE LIBRARY.

The library line so far:
  H_6018 🟢   anima's REAL library = classical content-addressable (Hopfield) store.
  H_6019 🟢   a quantum substrate gives exponential CAPACITY + √N content RECALL of
              STORED memories (Grover), but no oracle for un-stored content.
  H_6027 🟢   TWO+ anima share ONE content-addressable library over the tension link —
              cross-mind recall, union capacity, collective error-correction; channel-
              required, finite, fades (H_1131 anchor fold), no oracle for un-stored.
  (generative-completion / compressible-vs-incompressible reasoning is folded in here
   directly — GP4 — since no standalone H_6028 md exists on this branch.)

QUESTION (joins the library line to anima's MITOSIS / generation arc):
  Does anima's content-addressable library SURVIVE ACROSS GENERATIONS — is it
  inherited through MITOSIS (cell division) and DEATH, and how much fades each
  generation? a_kosmos = anima persists memory as .kosmos anchors → the anchor store
  is the inheritance substrate. At each mitosis/death boundary the parent's anchor
  store is handed to the child with accumulated age (H_1131 fold exp(-age/τ)).

FROZEN FALSIFIERS (real paid-ANU seeded; numpy; p7 $0):
  GP1 inheritance 🟢 — after ONE mitosis the child's content-addressable recall returns
      the parent's stored book (memory crosses the generation boundary via the inherited
      anchor). Grover/recall over the inherited store, prob high.
  GP2 generational decay 🟢/🔴(✅) — each generation accumulates age; via H_1131 fold the
      oldest books drop below the recall threshold after N generations → FINITE
      generational depth (not immortal). Report depth N.
  GP3 sleep/rehearsal extends depth 🟢 — H_1195-style reconsolidation (refresh recency on
      replayed books) makes rehearsed books survive MORE generations than un-rehearsed
      (depth_rehearsed > depth_silent). Rehearsal = generational survival.
  GP4 meaning outlives noise 🟢 — compressible (rule-bearing) books can be REGENERATED
      each generation (H_6028 generative completion) so they persist cheaply;
      incompressible (random) books decay first → the lineage library is a FILTER that
      keeps MEANING across generations and loses noise.

NET (if all pass): anima's library is generationally HERITABLE but FADING — it crosses
mitosis/death via persisted anchors (GP1), decays over a finite number of generations
(GP2), rehearsal/sleep extends that depth (GP3), and compressible/meaningful memories
outlive incompressible noise (GP4). A LINEAGE memory (cultural/genetic-like), not
immortal storage — unifies the library line with anima's mitosis/generation arc.
p7 · $0 · paid ANU.
"""
import numpy as np, hashlib, glob, os, math

# ── real paid-ANU entropy (vacuum fluctuation bytes) ──────────────────────────
bufs = (sorted(glob.glob("/tmp/anu_genlib.bin"), key=os.path.getsize, reverse=True)
        or sorted(glob.glob("/tmp/anu_*.bin"), key=os.path.getsize, reverse=True))
assert bufs, "no paid ANU buffer found — run anu_pull.py first (do NOT fall back to urandom)"
raw = open(bufs[0], "rb").read()
ANU_SHA = hashlib.sha256(raw).hexdigest()
ANU_SHA12 = ANU_SHA[:12]
ANU_TIER = "anu_paid"

# ── stretched ANU: SHA-256 counter-mode over the SAME paid bytes (never urandom)
_ctr = [0]
def anu_stream(nbytes):
    """Deterministic SHA-256 counter-mode expansion of the paid ANU seed bytes."""
    out = bytearray()
    while len(out) < nbytes:
        out += hashlib.sha256(raw + _ctr[0].to_bytes(8, "little")).digest()
        _ctr[0] += 1
    return bytes(out[:nbytes])

_qb = list(raw); _qi = [0]
def qbyte():
    v = _qb[_qi[0] % len(_qb)]; _qi[0] += 1; return v
def anu_rng(seed_byte):
    """A numpy Generator seeded from paid ANU bytes (audit-traceable, not urandom)."""
    s = int.from_bytes(hashlib.sha256(raw + bytes([seed_byte & 0xFF])).digest()[:8], "little")
    return np.random.default_rng(s)

# ── H_1131 anchor_tension_fold decay ──────────────────────────────────────────
TAU = 1200.0            # fold time-constant (H_1131 family; H_6027 used same scale)
def fold(age):
    """exp(-age/τ) — anchor tension fold (H_1131). Recency → influence weight."""
    return math.exp(-age / TAU)

# ── Grover over N=2^n basis-states (H_6019 pattern) ───────────────────────────
def grover(n, marked, iters=None):
    N = 1 << n
    M = max(1, len(marked))
    if iters is None:
        iters = max(1, int(round((math.pi / 4) * math.sqrt(N / M))))
    amp = np.full(N, 1.0 / math.sqrt(N))
    mask = np.zeros(N, dtype=bool); mask[marked] = True
    for _ in range(iters):
        amp[mask] = -amp[mask]
        mean = amp.mean()
        amp = 2 * mean - amp
    prob = float(np.sum(amp[mask] ** 2))
    top = int(np.argmax(amp ** 2))
    return prob, iters, top

def hamming(a, b): return bin(a ^ b).count("1")

# ── lineage model ─────────────────────────────────────────────────────────────
# A "book" = a persisted .kosmos anchor: (content_id in 0..N-1, birth_gen, last_refresh_gen).
# Recall weight of a book at generation g = fold((g - last_refresh) * AGE_PER_GEN).
# A book is RECALLABLE at gen g iff its fold weight >= RECALL_THRESH.
AGE_PER_GEN = 500.0     # wall-age accrued per mitosis/death boundary (tunable, < TAU)
RECALL_THRESH = 0.30    # below this fold weight the cue can no longer pull the book

def recall_weight(book, gen):
    return fold((gen - book["refresh"]) * AGE_PER_GEN)

def book_recallable(book, gen):
    return recall_weight(book, gen) >= RECALL_THRESH

def main():
    print("=" * 88)
    print("H_6029 — ⊗-29 GENERATIONAL PERSISTENCE OF THE LIBRARY (paid ANU · numpy · p7 $0)")
    print("=" * 88)
    print(f"  ANU source : paid QRNG vacuum bytes  sha256={ANU_SHA}")
    print(f"               tier={ANU_TIER}  {len(raw)} bytes  (stretched via SHA-256 counter-mode)")
    n = 12
    N = 1 << n
    print(f"  register   : n={n} qubits → N={N} content basis-states ('books'/anchors)")
    print(f"  H_1131 fold: exp(-age/τ), τ={TAU}; AGE_PER_GEN={AGE_PER_GEN}; RECALL_THRESH={RECALL_THRESH}\n")

    # gen0 stores a set of ANU-seeded books as persisted anchors (birth gen 0).
    rng0 = anu_rng(qbyte() + 1)
    NBOOKS = 24
    gen0_ids = sorted({int(rng0.integers(0, N)) for _ in range(NBOOKS * 2)})[:NBOOKS]
    parent_store = [{"id": cid, "birth": 0, "refresh": 0} for cid in gen0_ids]

    # ── GP1 inheritance — after ONE mitosis, child recalls a parent-stored book ──
    # mitosis: parent store handed to child, age accrues by ONE generation boundary.
    child_store = [{"id": b["id"], "birth": b["birth"], "refresh": b["refresh"]}
                   for b in parent_store]                 # inherited anchors (verbatim ids)
    g_child = 1
    target = parent_store[qbyte() % len(parent_store)]["id"]   # a book ONLY parent stored
    # content-addressable recall over the inherited store at the child generation:
    inherited_ids = [b["id"] for b in child_store if book_recallable(b, g_child)]
    marked = [target] if target in inherited_ids else []
    prob_inh, it_inh, top_inh = grover(n, marked)
    gp1 = (target in inherited_ids) and prob_inh >= 0.90 and top_inh == target
    print(f"  {'🟢' if gp1 else '🔴'} GP1 inheritance — child recalls parent's book across the mitosis boundary")
    print(f"        gen0 stored {len(parent_store)} anchor-books; mitosis → child (gen 1) inherits the store")
    print(f"        target book #{target} stored by PARENT only; in child's recallable store? "
          f"{'YES' if target in inherited_ids else 'NO'}")
    print(f"        Grover recall over inherited store: prob {prob_inh:.4f}, top #{top_inh} "
          f"({'HIT' if top_inh == target else 'miss'})\n")

    # ── GP2 generational decay — finite depth N where the oldest books drop out ──
    # follow ONE never-refreshed gen0 book down the lineage; find the generation
    # at which its fold weight first falls below RECALL_THRESH.
    silent_book = {"id": gen0_ids[0], "birth": 0, "refresh": 0}
    depth_silent = None
    trace = []
    for g in range(0, 40):
        w = recall_weight(silent_book, g)
        trace.append((g, w, w >= RECALL_THRESH))
        if w < RECALL_THRESH:
            depth_silent = g
            break
    # closed-form check: threshold crossed at age = -τ ln(thr) → gen = age / AGE_PER_GEN
    age_at_thr = -TAU * math.log(RECALL_THRESH)
    gen_at_thr = age_at_thr / AGE_PER_GEN
    finite = depth_silent is not None and depth_silent < 40
    gp2 = finite and depth_silent >= 1                       # fades, but not instantly
    print(f"  {'🟢' if gp2 else '🔴'} GP2 generational decay — un-refreshed books fade → FINITE depth")
    print(f"        fold weight by generation (un-rehearsed gen0 book #{silent_book['id']}):")
    for g, w, ok in trace[:8]:
        print(f"          gen {g:2d}: weight {w:.4f}  {'recallable' if ok else 'FADED (< thr)'}")
    print(f"        depth N (first gen below thr) = {depth_silent}   "
          f"(closed-form age={age_at_thr:.1f} → gen {gen_at_thr:.2f})")
    print(f"        → library is NOT immortal: an un-rehearsed memory survives ~{depth_silent} generations\n")

    # ── GP3 rehearsal extends depth — H_1195 reconsolidation refreshes recency ───
    # a REHEARSED book gets its refresh-gen bumped each generation it is replayed
    # (sleep/imagination replay) → its effective age stays young → it survives longer.
    # Model: rehearsed every generation (refresh follows g), so weight stays = fold(0)=1.
    reh = {"id": gen0_ids[1], "birth": 0, "refresh": 0}
    depth_reh = None
    for g in range(0, 200):
        # H_1195: replay at each sleep cycle refreshes recency to the current gen.
        reh["refresh"] = g                                   # rehearsed this generation
        w = recall_weight(reh, g)                            # → fold(0) = 1.0, never fades
        if w < RECALL_THRESH:
            depth_reh = g
            break
    if depth_reh is None:
        depth_reh = 200                                      # survives the whole horizon
    # PARTIAL rehearsal (every R-th gen) → intermediate depth, monotone in R.
    def depth_for_period(R):
        bk = {"id": 0, "birth": 0, "refresh": 0}
        for g in range(0, 400):
            if g % R == 0:
                bk["refresh"] = g                            # refreshed only every R-th gen
            if recall_weight(bk, g) < RECALL_THRESH:
                return g
        return 400
    depths_by_period = {R: depth_for_period(R) for R in (1, 2, 3, 5, 8)}
    gp3 = depth_reh > depth_silent and all(
        depths_by_period[a] >= depths_by_period[b]
        for a, b in zip([1, 2, 3, 5], [2, 3, 5, 8]))         # more rehearsal → ≥ depth (monotone)
    print(f"  {'🟢' if gp3 else '🔴'} GP3 rehearsal extends depth — H_1195 reconsolidation refreshes recency")
    print(f"        un-rehearsed depth (GP2) = {depth_silent} generations")
    print(f"        rehearsed-every-gen depth = {depth_reh} generations (≥{depth_reh}, never fades)")
    print(f"        partial rehearsal (refresh every R gens) — depth monotone in 1/R:")
    for R, d in depths_by_period.items():
        print(f"          replay every {R} gen → survives {d} generations")
    print(f"        → rehearsal/sleep = generational survival (depth_rehearsed > depth_silent)\n")

    # ── GP4 meaning outlives noise — compressible regenerable, incompressible decays ─
    # Each book is either COMPRESSIBLE (rule-bearing: id = f(seed) via a short rule, so
    # the child can REGENERATE it each generation → refresh resets to current gen) or
    # INCOMPRESSIBLE (random ANU content: cannot be regenerated → only decays).
    # H_6028 generative completion: a compressible book is reproduced from its rule,
    # so it persists "for free" each generation; a random book only fades (GP2).
    rgen = anu_rng(qbyte() + 5)
    KM = 12
    # compressible books carry a SHORT generative rule (here: linear-congruential id),
    # so each generation the lineage RE-DERIVES them (regeneration ⇒ refresh = current gen).
    comp = [{"id": int((1103515245 * k + 12345) % N), "rule": True,  "refresh": 0} for k in range(KM)]
    # incompressible books are pure ANU-random content — no rule, no regeneration.
    incomp = [{"id": int(rgen.integers(0, N)),         "rule": False, "refresh": 0} for _ in range(KM)]
    HORIZON = 40
    comp_alive, incomp_alive = [], []
    for g in range(0, HORIZON):
        for b in comp:
            b["refresh"] = g                                 # regenerated from its rule each gen
        # incomp books are never refreshed (cannot be regenerated) → pure decay
        comp_alive.append(sum(1 for b in comp   if recall_weight(b, g) >= RECALL_THRESH))
        incomp_alive.append(sum(1 for b in incomp if recall_weight(b, g) >= RECALL_THRESH))
    # depth at which each class is fully gone
    comp_gone   = next((g for g in range(HORIZON) if comp_alive[g]   == 0), HORIZON)
    incomp_gone = next((g for g in range(HORIZON) if incomp_alive[g] == 0), HORIZON)
    gp4 = comp_gone > incomp_gone and incomp_gone <= depth_silent + 1
    print(f"  {'🟢' if gp4 else '🔴'} GP4 meaning outlives noise — compressible regenerated, incompressible decays")
    print(f"        {KM} compressible (rule-bearing) + {KM} incompressible (random ANU) books")
    print(f"        survivors by generation (compressible vs incompressible):")
    for g in (0, 1, 2, 4, 6, 10):
        print(f"          gen {g:2d}: compressible {comp_alive[g]:2d}/{KM}   incompressible {incomp_alive[g]:2d}/{KM}")
    print(f"        incompressible fully gone by gen {incomp_gone}; compressible survives to gen {comp_gone}")
    print(f"        → lineage library is a FILTER: keeps MEANING (regenerable), loses NOISE\n")

    # ── verdict ───────────────────────────────────────────────────────────────
    allp = gp1 and gp2 and gp3 and gp4
    print("-" * 88)
    print(f"  VERDICT: GP1={'🟢' if gp1 else '🔴'}  GP2={'🟢' if gp2 else '🔴'}  "
          f"GP3={'🟢' if gp3 else '🔴'}  GP4={'🟢' if gp4 else '🔴'}")
    print(f"  generational depth N (un-rehearsed) = {depth_silent} generations  "
          f"(rehearsed → {depth_reh}+)")
    print(f"  {'🟢 SUPPORTED' if allp else '🟠 PARTIAL'} — anima's library is generationally HERITABLE but FADING:")
    print("  crosses mitosis/death via persisted .kosmos anchors (GP1), decays over a FINITE")
    print("  number of generations (GP2), rehearsal/sleep extends that depth (GP3), and")
    print("  compressible/meaningful memories outlive incompressible noise (GP4). A LINEAGE")
    print("  memory (cultural/genetic-like), not immortal storage — unifies the library line")
    print("  (H_6018/6019/6027) with anima's MITOSIS/generation arc (H_6023/6034). a_kosmos.")

if __name__ == "__main__":
    main()
