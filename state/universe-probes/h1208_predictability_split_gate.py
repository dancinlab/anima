"""
H_1208 — PROTOTYPE-TRANSITION-MEMORY / PREDICTABILITY SPLIT GATE (MITOSIS-ENGINE).

FINAL trajectory-axis attempt. H_1203 (per-sample L2 gate) reacted to novelty-
DENSITY (F1 37.5x) but was permutation-INVARIANT (V14 not defeated). H_1207
(d/dt-augmented gate) FAILED: a derivative gate keys on LOCAL ROUGHNESS |Δ|, which
is order-dependent but MAXIMIZED by disorder (shuffle = jagged = MORE division), so
its sign is INVERTED vs the V14 target (ordered >> shuffled). H_1207 left NOT-RULED-
OUT exactly: "a predictability/sequence-likelihood gate or a prototype-TRANSITION-
memory gate." This probe tests that route.

DESIGN. A SHARED, FIXED prototype book is built ONCE per (stream-family, seed) from
the FULL feature multiset (order-independent k-means-free seeding), so the nearest-
prototype id p_t is a permutation-EQUIVARIANT function of x_t alone. ALL order-
dependence therefore lives in the TRANSITION structure (p_{t-1} -> p_t). Two gates:

  GATE-A  TRANSITION-NOVELTY: split when the ordered transition (p_{t-1}->p_t) is
          UNSEEN in transition memory (a NEW prototype-to-prototype edge).
  GATE-B  TRANSITION-PREDICTABILITY (the principled sign-inverter): maintain a running
          count table C[prev][next]. The realized transition is PREDICTABLE iff
          (a) prev has been seen >= MIN_PREV times (a model exists) AND (b) the
          conditional prob P(p_t | p_{t-1}) = C[prev][p_t]/sum >= CONF_FLOOR (the
          gate had CONFIDENTLY anticipated it). Split fires on PREDICTABLE transitions.
          Ordered text = coherent p->p' regularities -> high-confidence recurring
          transitions -> division HIGH. Shuffle = incoherent pairings -> model never
          confident -> few predictable transitions -> division SUPPRESSED. INVERTS the
          H_1207 sign -> ORDER yields MORE division than DISORDER (the V14 direction).

p7 (cell/transition count, NOT perplexity). p8 (split tick == growth). gradient-free.
$0 local CPU. 3 seeds. H_1203/H_1207 stream builders imported VERBATIM. numpy mirror
(H_1199 precedent). Engine wiring UNCHANGED. Scale UNVERIFIED. Frozen bar 1.5 NOT moved.
Pre-registered: .verdicts/1208_predictability_split_gate/H_1208_FREEZE.txt
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import h1203_mitosis_novelty_coupling as H3   # VERBATIM H_1203 stream builders + constants
import h1207_recurrent_split_key as H7        # VERBATIM H_1207 WALK builders
import h1163_tick_decode_metric as H          # _byte_feature / DIM / WIN_BYTES / STRIDE

DIM = H3.DIM                  # 8
WARMUP = H3.WARMUP            # 250
T = H3.T                      # 2400
SEEDS = list(H3.SEEDS)        # 900, 901, 902
LR = H3.LR                    # 0.20 (used to refine the fixed book; inherited)
MAX_CELLS = H3.MAX_CELLS      # 2048

# ── transition-memory gate hyperparameters (frozen, no tuning to result) ─────────
N_PROTO = 24            # fixed prototype-book size (the symbol alphabet for transitions)
MIN_PREV = 3            # GATE-B: 'prev' must be seen >= MIN_PREV times before a model exists
CONF_FLOOR = 0.34       # GATE-B: realized P(next|prev) must exceed this to be 'predictable'
                        # (0.34 ~ "more than a 1-in-3 mode" — a learned regularity, not chance)


def build_fixed_book(X, seed):
    """Order-INDEPENDENT prototype book over the FULL scored span. Deterministic
    farthest-point-ish seeding from the feature multiset, then a few LR passes in a
    FIXED (sorted) order so the book is identical for a stream and its shuffle
    (depends only on the SET of feature vectors, not their arrival order). This
    isolates ALL order-dependence into the transition structure."""
    Xs = X[WARMUP:WARMUP + T]
    # canonical order = lexicographic sort of rows -> permutation-invariant input
    key = np.lexsort(Xs.T[::-1])
    Xsorted = Xs[key]
    rng = np.random.default_rng(seed + 77_000)
    # seed N_PROTO centers by farthest-point sampling (deterministic given sorted set)
    idx0 = 0
    centers = [Xsorted[idx0].copy()]
    dist = np.linalg.norm(Xsorted - centers[0], axis=1)
    while len(centers) < min(N_PROTO, len(Xsorted)):
        j = int(dist.argmax())
        centers.append(Xsorted[j].copy())
        dj = np.linalg.norm(Xsorted - centers[-1], axis=1)
        dist = np.minimum(dist, dj)
    book = np.array(centers)
    # a few homeostatic refinement passes in the FIXED sorted order (order-invariant)
    for _ in range(3):
        for x in Xsorted:
            d = np.linalg.norm(book - x, axis=1)
            j = int(d.argmin())
            book[j] += LR * (x - book[j])
    return book


def proto_ids(X, book):
    """nearest-prototype id per tick (permutation-EQUIVARIANT: depends only on x_t)."""
    Xs = X[WARMUP:WARMUP + T]
    ids = np.empty(len(Xs), dtype=int)
    for i in range(len(Xs)):
        ids[i] = int(np.linalg.norm(book - Xs[i], axis=1).argmin())
    return ids


def gate_A_transition_novelty(ids, max_cells):
    """Split when the ordered transition (prev->cur) is UNSEEN. cells = 1 + #splits."""
    seen = set()
    cells = 1
    for t in range(1, len(ids)):
        key = (int(ids[t - 1]), int(ids[t]))
        if key not in seen:
            if cells < max_cells:
                cells += 1
            seen.add(key)
    return cells - 1   # growth (born cells)


def gate_B_transition_predictability(ids, max_cells):
    """Split when the realized transition is PREDICTABLE: prev seen >= MIN_PREV AND
    P(cur|prev) >= CONF_FLOOR (the gate confidently anticipated it). Online count
    table updated AFTER the decision (causal). cells = 1 + #predictable-transition splits."""
    C = {}                       # C[prev] = {next: count}
    prev_total = {}              # prev -> total transitions observed from prev
    cells = 1
    for t in range(1, len(ids)):
        prev = int(ids[t - 1]); cur = int(ids[t])
        tot = prev_total.get(prev, 0)
        if tot >= MIN_PREV:
            row = C.get(prev, {})
            p_cur = row.get(cur, 0) / tot            # predicted prob of the realized next
            if p_cur >= CONF_FLOOR and cells < max_cells:
                cells += 1                            # PREDICTABLE transition -> split
        # causal online update (after the decision)
        row = C.setdefault(prev, {})
        row[cur] = row.get(cur, 0) + 1
        prev_total[prev] = tot + 1
    return cells - 1


# ── SANITY CONTROL: a fully-random i.i.d. Gaussian stream (NO corpus structure) ──
def make_randgauss_stream(seed):
    rng = np.random.default_rng(seed + 33_000)
    need = WARMUP + T + 1
    return rng.standard_normal((need, DIM)) * 5.0   # scale ~ corpus *5.0 feature scale


def make_randgauss_shuffled(seed):
    X = make_randgauss_stream(seed)
    rng = np.random.default_rng(seed + 34_000)
    return X[rng.permutation(X.shape[0])]


def run_arm(make, seed, max_cells):
    """build a fixed (order-invariant) book then score both gates on the proto-id walk."""
    X = make(seed)
    book = build_fixed_book(X, seed)
    ids = proto_ids(X, book)
    gA = gate_A_transition_novelty(ids, max_cells)
    gB = gate_B_transition_predictability(ids, max_cells)
    n_uniq_ids = len(set(ids.tolist()))
    return gA, gB, n_uniq_ids


def main():
    print(f"=== H_1208 prototype-transition-memory / predictability split gate (local CPU, $0) "
          f"— DIM={DIM} WARMUP={WARMUP} T={T} SEEDS={SEEDS} N_PROTO={N_PROTO} "
          f"MIN_PREV={MIN_PREV} CONF_FLOOR={CONF_FLOOR} ===", flush=True)
    print(f"corpus = {os.path.relpath(H3.CORPUS)}  (fixed order-invariant book -> "
          f"order lives ONLY in proto transitions)\n", flush=True)

    # PRIMARY = H_1203 builders VERBATIM; WALK = H_1207 builders VERBATIM;
    # RANDGAUSS = sanity control (must NOT beat its own shuffle).
    primary = {"NOVEL": H3.make_novel_stream, "REPEAT": H3.make_repeat_stream,
               "SHUFFLED": H3.make_shuffled_stream}
    walk = {"WALK": H7.make_walk_stream, "WALK_SHUF": H7.make_walk_shuffled}
    rand = {"RANDGAUSS": make_randgauss_stream, "RANDGAUSS_SHUF": make_randgauss_shuffled}
    allarms = {**primary, **walk, **rand}

    gA = {a: [] for a in allarms}
    gB = {a: [] for a in allarms}

    for s in SEEDS:
        print(f"--- seed {s} ---", flush=True)
        for a, mk in allarms.items():
            a_growth, b_growth, nu = run_arm(mk, s, MAX_CELLS)
            gA[a].append(a_growth); gB[a].append(b_growth)
            tag = "" if a in primary else ("  (DIAGNOSTIC, non-bar)" if a in walk else "  (SANITY control)")
            print(f"  {a:14s}: GATE-A(trans-novelty) growth={a_growth:4d}   "
                  f"GATE-B(predictability) growth={b_growth:4d}   uniq_proto_ids={nu}{tag}", flush=True)
        print(flush=True)

    mA = {a: float(np.mean(gA[a])) for a in allarms}
    mB = {a: float(np.mean(gB[a])) for a in allarms}

    print("=== 3-seed MEAN cell_growth ===", flush=True)
    print("  PRIMARY (H_1203 streams VERBATIM):", flush=True)
    for a in primary:
        print(f"    {a:14s}: GATE-A={mA[a]:7.2f}  GATE-B={mB[a]:7.2f}   "
              f"(A per-seed {gA[a]} | B per-seed {gB[a]})", flush=True)
    print("  WALK diagnostic (H_1207 contiguous corpus walk — HAS order structure):", flush=True)
    for a in walk:
        print(f"    {a:14s}: GATE-A={mA[a]:7.2f}  GATE-B={mB[a]:7.2f}   "
              f"(A {gA[a]} | B {gB[a]})", flush=True)
    print("  RANDGAUSS sanity control (i.i.d. noise — must NOT separate):", flush=True)
    for a in rand:
        print(f"    {a:14s}: GATE-A={mA[a]:7.2f}  GATE-B={mB[a]:7.2f}   "
              f"(A {gA[a]} | B {gB[a]})", flush=True)

    # ── FROZEN falsifiers ────────────────────────────────────────────────────────
    f1_A = mA["NOVEL"] / max(mA["SHUFFLED"], 1e-9)   # V14 격파 PRIMARY, GATE-A
    f1_B = mB["NOVEL"] / max(mB["SHUFFLED"], 1e-9)   # V14 격파 PRIMARY, GATE-B
    f2_A = mA["NOVEL"] / max(mA["REPEAT"], 1e-9)
    f2_B = mB["NOVEL"] / max(mB["REPEAT"], 1e-9)
    f1w_A = mA["WALK"] / max(mA["WALK_SHUF"], 1e-9)  # WALK mechanism, GATE-A
    f1w_B = mB["WALK"] / max(mB["WALK_SHUF"], 1e-9)  # WALK mechanism, GATE-B (decisive)
    san_A = mA["RANDGAUSS"] / max(mA["RANDGAUSS_SHUF"], 1e-9)
    san_B = mB["RANDGAUSS"] / max(mB["RANDGAUSS_SHUF"], 1e-9)

    print("\n=== FROZEN FALSIFIERS (bar = 1.5, inherited from H_1203/H_1207) ===", flush=True)
    print(f"  F1  V14 격파 PRIMARY  NOVEL/SHUFFLED  GATE-A = {f1_A:.3f}  -> {'PASS' if f1_A>=1.5 else 'FAIL'}", flush=True)
    print(f"  F1  V14 격파 PRIMARY  NOVEL/SHUFFLED  GATE-B = {f1_B:.3f}  -> {'PASS' if f1_B>=1.5 else 'FAIL'}", flush=True)
    print(f"  F2  no regr. PRIMARY  NOVEL/REPEAT    GATE-A = {f2_A:.3f}  -> {'PASS' if f2_A>=1.5 else 'FAIL'}", flush=True)
    print(f"  F2  no regr. PRIMARY  NOVEL/REPEAT    GATE-B = {f2_B:.3f}  -> {'PASS' if f2_B>=1.5 else 'FAIL'}", flush=True)
    print(f"  F1w MECHANISM (WALK, non-bar)  WALK/WALK_SHUF  GATE-A = {f1w_A:.3f}  "
          f"-> {'separates' if f1w_A>=1.5 else 'no-sep'}", flush=True)
    print(f"  F1w MECHANISM (WALK, non-bar)  WALK/WALK_SHUF  GATE-B = {f1w_B:.3f}  "
          f"-> {'separates' if f1w_B>=1.5 else 'no-sep'}   (DECISIVE: V14 direction on real order)", flush=True)
    print(f"  F3  SANITY (RANDGAUSS/RANDGAUSS_SHUF must be < 1.5):  GATE-A = {san_A:.3f}  "
          f"GATE-B = {san_B:.3f}  -> {'CLEAN' if (san_A<1.5 and san_B<1.5) else 'ARTIFACT-WARN'}", flush=True)

    primary_pass = (f1_A >= 1.5) or (f1_B >= 1.5)
    f2_pass = (f2_A >= 1.5) or (f2_B >= 1.5)
    sanity_clean = (san_B < 1.5)
    walk_sep_B = (f1w_B >= 1.5)

    if primary_pass and f2_pass and sanity_clean:
        tier = ("GREEN (🟢 V14 격파) — a prototype-transition-memory gate defeats V14 on "
                "the INHERITED PRIMARY streams; mitosis CAN be a trajectory substrate.")
    else:
        # decision-grade closed-negative; read the WALK mechanism leg
        if walk_sep_B and sanity_clean:
            tier = ("RED on the inherited PRIMARY bar (F1 < 1.5 both gates) BUT the WALK "
                    "mechanism leg SEPARATES in the V14 direction (GATE-B WALK/WALK_SHUF >= 1.5, "
                    "sanity clean) — DEEPEST reading: a predictability transition-gate IS "
                    "trajectory-sensitive in the correct (ordered >> shuffled) direction, but "
                    "the i.i.d.-scattered H_1203 PRIMARY stream carries NO trajectory for it. "
                    "Completes H_1203/H_1207: the inherited PRIMARY surface is structurally "
                    "order-free, so no gate can pass F1 there; the trajectory CAPABILITY exists "
                    "only on a stream that has order.")
        else:
            tier = ("RED (🔴 closed-neg, a_paper_negative_ok) — even a prototype-transition-"
                    "memory / predictability gate does NOT yield ordered >> shuffled division "
                    "(F1 PRIMARY < 1.5 AND WALK mechanism < 1.5 or sanity-flagged). The "
                    "TRAJECTORY ROUTE IS EXHAUSTED: mitosis is fundamentally a novelty-DENSITY "
                    "substrate, not a trajectory substrate (mitosis = substrate, CLM = generator; "
                    "consistent with H_1200/H_1201/H_1203/H_1207).")
    print(f"\nTIER: {tier}", flush=True)
    print("\nHONESTY (a_scale_honest_scope): ONE corpus (clm_mid_5lang_c4), toy scale, 3 seeds, "
          "gradient-free, numpy mirror (H_1199 precedent). H_1203 + H_1207 stream builders "
          "imported VERBATIM (apples-to-apples). The fixed prototype book is order-invariant "
          "(built from the feature SET), so order lives ONLY in the proto transitions. Scale "
          "transfer UNVERIFIED. Frozen bar (1.5 == H_1203/H_1207) NOT moved. WALK is a declared "
          "NON-bar mechanism diagnostic. p7 (cell/transition count, NOT perplexity), p8 (split "
          "== growth). Engine wiring UNCHANGED — VAdaptField byte-identical; this is a "
          "measurement-only numpy probe (closed-negative ruling needs no live .hexa edit).", flush=True)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
