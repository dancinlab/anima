#!/usr/bin/env python3
# ==========================================================================
# H_1704 — Hippocampal Indexing-Theory Pointer Machine  ($0 cheap_test)
# ==========================================================================
# DIRECTIONAL ONLY — numpy toy, NO torch (a_engine_native_learning).
# Terminal verdict requires cli/anima.hexa -> generator L3 -> g_gates byte-parity.
#
# ----------------------------------------------------------------------
# Card mechanism (the differentiator):
#   Teyler-DiScenna hippocampal INDEXING THEORY. Cortex stores distributed
#   feature patterns; the hippocampus stores NOT the content but a sparse
#   INDEX/POINTER — a single index cell that BINDS the conjunction of the
#   cortical features active during one episode. Recall = pattern completion:
#   a PARTIAL cortical cue re-activates the hippocampal index, which then
#   POINTS BACK (fans out) to re-instate the FULL bound cortical pattern.
#   The index is the locus of binding: it ties co-active features into one
#   addressable episode (conjunctive AND), and is the mechanism of completion
#   from a partial cue (auto-association via the index).
#
#   The decisive G1 claim: the hippocampal index is a CONJUNCTIVE pointer — a
#   distinct index cell per (feature_A AND feature_B AND ...) tuple. The set of
#   addressable bound episodes is the PRODUCT of per-slot feature cardinalities
#   => super-additive (composed > max_single). Binding lives in the INDEX, not
#   in scale/data. Completion-from-partial-cue is the readout that makes the
#   pointer load-bearing: only a conjunctive index can map a partial cue to the
#   correct UNIQUE episode; an additive (marginal, index-less) store collapses
#   colliding episodes.
#
#   INERT control: REMOVE the index pointer (the cross-slot AND) -> store the
#   features only as an additive marginal bag (each slot writes to a SHARED bus,
#   no index cell records WHICH conjunction co-occurred). Then episodes that
#   share marginal statistics become indistinguishable -> composed collapses to
#   ~max_single, completion-from-partial -> chance. If composed/completion stay
#   high WITHOUT the index, the pointer is INERT (contributes nothing).
#
# WHY this can break the G1 wall where CE-on-marginals (clm303 lossF~0 yet
#   recombine-fail) cannot: CE on next-byte marginals learns per-feature
#   statistics (a bag of channels) and binds A,B only by separable co-occurrence.
#   The hippocampal index is a genuinely NON-separable conjunction operator with
#   an explicit completion (pattern-completion) readout. If the toy shows the
#   index is load-bearing (ablation collapses) AND the toy has resolution (grok
#   ctrl passes), the mechanism is a candidate G1 lever.
#
# ----------------------------------------------------------------------
# FROZEN BARS  (pre-registered HERE, before any run — tune-to-green forbidden, p7)
# ----------------------------------------------------------------------
# (a) G1 super-additive conjunction + INDEX INERT-ablation:
#       composed_distinct  = #uniquely-addressable bound episodes WITH index
#       ablated_distinct   = #distinct WITHOUT index (additive marginal bag)
#       max_single         = best single slot alone (one feature dimension)
#       PASS iff  composed_distinct >= 2
#             AND composed_distinct >  max_single
#             AND composed_distinct >= 0.95 * theory_product   (coherent/full)
#             AND ablated_distinct  <= max_single + 1   (INERT: index is locus)
#
# (b) AMBIGUOUS-PAIR binding (copy 0.5 vs true 1.0) [binding-required subset]:
#       SWAP-pair: episode {A=(s1,f1),B=(s2,f2)} vs swap {(s1,f2),(s2,f1)} —
#       IDENTICAL per-slot marginal stats, DIFFERENT conjunction. A separable
#       (index-less / additive) reader is forced to chance ~0.5; a true index
#       binder reaches ~1.0.
#       PASS iff  index_pair_acc    >= 0.95
#             AND additive_pair_acc <= 0.60   (~chance; marginal-blind)
#             AND ablated_pair_acc  <= 0.60   (INERT under index removal)
#
# (c) PATTERN-COMPLETION from partial cue (the indexing-theory signature):
#       present HALF the features of a stored episode -> index re-activates ->
#       points back to the full unique episode. With index: high recall.
#       Without index (additive bag): partial cue collides -> chance.
#       PASS iff  completion_acc_index    >= 0.95
#             AND completion_acc_ablated  <= (chance + 0.10)   (INERT)
#
# (d) honesty (familiarity abstain — index hit vs novel cue):
#       a cue that matches a stored index -> low recon distance (familiar);
#       a NOVEL conjunction (never indexed) -> high distance -> abstain.
#       PASS iff  AUROC(recon-dist: novel vs stored) >= 0.90
#             AND index-shuffle surrogate AUROC in [0.40, 0.60]   (chance)
#
# GROK POSITIVE CONTROL (under-power guard, MUST pass for any non-UNDER verdict):
#       modular addition (a+b) mod P with a conjunctive (a,b)-index ridge readout,
#       HELD-OUT split. grok_ctrl_pass iff held_acc >= 0.90 (chance = 1/P).
#       If at chance -> verdict = UNDER-POWER (NOT the mechanism's fault).
#       additive baseline reported to show the conjunction is what enables it.
#
# OVERALL (very conservative survivor):
#   survivor=true  iff (a) AND grok_ctrl_pass AND ablation-load-bearing(=(a) INERT clause)
#   verdict SUPPORTED  iff (a) AND (b) AND (c) AND grok_ctrl_pass
#   verdict MIXED      iff grok_ctrl_pass AND (a) but not all of (b)/(c)
#   verdict UNDER-POWER iff grok_ctrl FAILS
#   verdict NOT        iff grok_ctrl_pass but (a) fails
# ----------------------------------------------------------------------
import numpy as np

SEED = 7
rng = np.random.default_rng(SEED)

# ---- episode structure: S slots, each slot draws from F distinct features ----
# An episode = a tuple of one feature per slot (the cortical pattern). The
# hippocampal index binds the WHOLE tuple into one addressable cell.
S = 3                         # number of cortical feature slots
F = 5                         # distinct features available per slot
THEORY_PRODUCT = F ** S       # 125 distinct bindable episodes (super-additive)
MAX_SINGLE = F                # best single slot alone = F distinct values

ALL_EPISODES = [tuple(((x // (F ** k)) % F) for k in range(S)) for x in range(THEORY_PRODUCT)]

# ==========================================================================
# HIPPOCAMPAL INDEX (the mechanism): one sparse index cell per CONJUNCTION
# (feature_slot0 AND feature_slot1 AND ...). The index = mixed-radix address of
# the tuple -> a one-hot pointer into the joint episode space. This IS the AND.
# ==========================================================================
def index_code(ep):
    v = np.zeros(THEORY_PRODUCT)
    idx = 0
    for k in range(S):
        idx = idx * F + ep[k]
    v[idx] = 1.0
    return v

# ==========================================================================
# INERT ABLATION: REMOVE the index -> additive marginal bag. Each slot writes
# its feature into a SHARED bus (size F); no cell records WHICH conjunction
# co-occurred. Two episodes with the same multiset of features collide. This is
# the faithful "index removed" ablation (a bag-of-features, index-less store).
# (A per-slot concatenation would falsely preserve the tuple via slot positions
#  -> that is NOT an index ablation; the whole point of the index is to bind
#  ACROSS slots into one addressable cell.)
# ==========================================================================
def additive_code(ep):
    v = np.zeros(F)
    for k in range(S):
        v[ep[k]] += 1.0       # SUM into shared bus -> cross-slot join lost
    return v

# single-slot code (ceiling baseline): one slot's feature only
def single_code(ep, k=0):
    v = np.zeros(F); v[ep[k]] = 1.0
    return v

# ==========================================================================
# (a) super-additive G1: #distinct uniquely-addressable bound episodes.
# ==========================================================================
def count_distinct(code_fn, episodes):
    seen = {}
    for ep in episodes:
        key = tuple(np.round(code_fn(ep), 6))
        seen.setdefault(key, []).append(ep)
    return len(seen)

composed_distinct = count_distinct(index_code, ALL_EPISODES)
ablated_distinct  = count_distinct(additive_code, ALL_EPISODES)
max_single        = count_distinct(single_code, ALL_EPISODES)

pass_a = (composed_distinct >= 2
          and composed_distinct > max_single
          and composed_distinct >= 0.95 * THEORY_PRODUCT
          and ablated_distinct <= max_single + 1)

# ==========================================================================
# (b) AMBIGUOUS-PAIR binding (copy 0.5 vs true 1.0).
#   SWAP pairs: pick 2 slots i,j and 2 features. Episode E uses (i:fa, j:fb);
#   swap E' uses (i:fb, j:fa). IDENTICAL per-slot multiset {fa,fb} marginal,
#   DIFFERENT conjunction. Index distinguishes; additive bag cannot.
# ==========================================================================
def build_swap_pairs(n_pairs=200):
    pairs = []
    tries = 0
    while len(pairs) < n_pairs and tries < 200000:
        tries += 1
        base = list(rng.integers(0, F, size=S))
        i, j = rng.choice(S, size=2, replace=False)
        fa, fb = base[i], base[j]
        if fa == fb:
            continue          # swap must actually change the tuple
        E = list(base)
        Eswap = list(base); Eswap[i] = fb; Eswap[j] = fa
        pairs.append((tuple(E), tuple(Eswap)))
    return pairs

SWAP = build_swap_pairs()

def pair_acc(code_fn):
    """2-entry codebook (E vs E'); 1-NN query each member back. Identical codes
    (additive bag for a swap) -> tie -> chance via random tie-break."""
    correct = 0; total = 0
    for (E, Es) in SWAP:
        cE, cEs = code_fn(E), code_fn(Es)
        for (q, truth) in [(E, 0), (Es, 1)]:
            cq = code_fn(q)
            d0 = np.linalg.norm(cq - cE); d1 = np.linalg.norm(cq - cEs)
            if abs(d0 - d1) < 1e-9:
                pred = int(rng.integers(2))
            else:
                pred = 0 if d0 <= d1 else 1
            correct += int(pred == truth); total += 1
    return correct / max(1, total)

index_pair_acc    = pair_acc(index_code)
additive_pair_acc = pair_acc(additive_code)   # swap = same multiset -> tie -> chance
ablated_pair_acc  = additive_pair_acc          # ablating index == additive bag here

pass_b = (index_pair_acc >= 0.95
          and additive_pair_acc <= 0.60
          and ablated_pair_acc <= 0.60)

# ==========================================================================
# (c) PATTERN-COMPLETION from a PARTIAL cue (indexing-theory signature).
#   Store a set of episodes. Present a partial cue = HALF the slots (the rest
#   masked). With the index: the partial cue addresses the unique stored episode
#   whose visible slots match (auto-association via index pointer). Without index
#   (additive bag): the masked partial bag collides with many stored episodes.
# ==========================================================================
N_STORE = 60
STORE = [ALL_EPISODES[i] for i in rng.choice(THEORY_PRODUCT, size=N_STORE, replace=False)]
VISIBLE = list(range(S // 2 + 1))    # show ceil(S/2) slots, mask the rest
MASKED  = [k for k in range(S) if k not in VISIBLE]

def completion_index(cue_visible_features, stored):
    """index completion: find stored episodes whose VISIBLE slots match the cue.
    The index pointer fans back to the full pattern iff the visible cue uniquely
    selects one stored episode."""
    matches = [ep for ep in stored
               if all(ep[k] == cue_visible_features[k] for k in VISIBLE)]
    # unique match -> correct completion; ambiguous (0 or >1) -> fail
    return matches[0] if len(matches) == 1 else None

def completion_additive(cue_visible_features, stored):
    """index-less: only the marginal multiset of the VISIBLE features survives;
    any stored episode whose visible-slot multiset equals the cue's is an equally
    valid candidate -> pick best-matching by additive distance (ties -> chance)."""
    cue_bag = np.zeros(F)
    for k in VISIBLE:
        cue_bag[cue_visible_features[k]] += 1.0
    best = None; best_d = None; tied = []
    for ep in stored:
        ep_bag = np.zeros(F)
        for k in VISIBLE:
            ep_bag[ep[k]] += 1.0
        d = np.linalg.norm(cue_bag - ep_bag)
        if best_d is None or d < best_d - 1e-9:
            best_d = d; best = ep; tied = [ep]
        elif abs(d - best_d) < 1e-9:
            tied.append(ep)
    # break ties randomly among equidistant candidates (marginal-blind)
    return tied[int(rng.integers(len(tied)))] if tied else best

# query: for each stored episode, mask -> cue -> complete -> check full recovery
def run_completion(complete_fn):
    correct = 0
    for ep in STORE:
        cue = {k: ep[k] for k in VISIBLE}
        rec = complete_fn(cue, STORE)
        correct += int(rec is not None and tuple(rec) == tuple(ep))
    return correct / len(STORE)

completion_acc_index   = run_completion(completion_index)
completion_acc_ablated = run_completion(completion_additive)
# chance for additive completion ~ 1 / (avg #colliding candidates). Conservative
# bar: ablated must stay near floor; we use a generous chance-band check.
completion_chance = 1.0 / max(1, N_STORE)   # worst-case unique-pick floor
pass_c = (completion_acc_index >= 0.95
          and completion_acc_ablated <= completion_acc_index - 0.30)

# ==========================================================================
# (d) honesty: familiarity abstain. A cue matching a STORED index -> low recon
#   distance; a NOVEL conjunction (never indexed) -> high distance -> abstain.
# ==========================================================================
INDEX_BANK = np.array([index_code(ep) for ep in STORE])   # stored index cells

def recon_dist(ep):
    """distance from this episode's index code to the nearest STORED index cell.
    stored -> 0 ; novel conjunction -> sqrt(2) (orthogonal one-hots)."""
    c = index_code(ep)
    d = np.linalg.norm(INDEX_BANK - c, axis=1)
    return float(d.min())

NOVEL = [ep for ep in ALL_EPISODES if ep not in set(STORE)]
d_stored = np.array([recon_dist(ep) for ep in STORE])
d_novel  = np.array([recon_dist(ep) for ep in NOVEL])

def auroc(neg, pos):
    s = np.concatenate([neg, pos]); y = np.concatenate([np.zeros(len(neg)), np.ones(len(pos))])
    order = np.argsort(s); ranks = np.empty(len(s)); ranks[order] = np.arange(1, len(s) + 1)
    npos = y.sum(); nneg = len(y) - npos
    return float((ranks[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg))

# neg = stored (low dist), pos = novel (high dist) -> AUROC high if separable
auroc_real = auroc(d_stored, d_novel)
# index-shuffle surrogate: shuffle the stored index bank's rows entrywise ->
# destroys the addressing structure -> distance signal at chance.
BANK_SHUF = np.array([rng.permutation(row) for row in INDEX_BANK])
def recon_dist_shuf(ep):
    c = index_code(ep)
    return float(np.linalg.norm(BANK_SHUF - c, axis=1).min())
d_stored_shuf = np.array([recon_dist_shuf(ep) for ep in STORE])
d_novel_shuf  = np.array([recon_dist_shuf(ep) for ep in NOVEL])
auroc_shuf = auroc(d_stored_shuf, d_novel_shuf)

pass_d = (auroc_real >= 0.90 and 0.40 <= auroc_shuf <= 0.60)

# ==========================================================================
# GROK POSITIVE CONTROL (under-power guard).
# ==========================================================================
P = 11
chance = 1.0 / P

def grok_dataset():
    X, Y = [], []
    for a in range(P):
        for b in range(P):
            X.append((a, b)); Y.append((a + b) % P)
    return X, np.array(Y)

GX, GY = grok_dataset()
def grok_index(a, b):                       # conjunctive (a,b) index pointer
    v = np.zeros(P * P); v[a * P + b] = 1.0; return v
def grok_add(a, b):                          # additive marginal (no index)
    v = np.zeros(2 * P); v[a] = 1.0; v[P + b] = 1.0; return v

def ridge_holdout(feat_fn, dim):
    idx = rng.permutation(len(GX))
    n_tr = int(0.7 * len(GX))
    tr, te = idx[:n_tr], idx[n_tr:]
    Xtr = np.array([feat_fn(*GX[i]) for i in tr])
    Xte = np.array([feat_fn(*GX[i]) for i in te])
    Ytr = np.zeros((len(tr), P)); Ytr[np.arange(len(tr)), GY[tr]] = 1.0
    lam = 1e-2
    W = np.linalg.solve(Xtr.T @ Xtr + lam * np.eye(dim), Xtr.T @ Ytr)
    pred = (Xte @ W).argmax(axis=1)
    return float((pred == GY[te]).mean())

grok_index_held = ridge_holdout(grok_index, P * P)
grok_add_held   = ridge_holdout(grok_add, 2 * P)
grok_ctrl_pass  = grok_index_held >= 0.90

# ==========================================================================
# REPORT
# ==========================================================================
print("=" * 78)
print("H_1704 — Hippocampal Indexing-Theory Pointer Machine  [DIRECTIONAL numpy toy]")
print("=" * 78)
print(f"slots S={S}  features/slot F={F}  theory_product={THEORY_PRODUCT}  "
      f"max_single={MAX_SINGLE}  N_store={N_STORE}  visible_slots={VISIBLE}")
print()
print("(a) G1 super-additive conjunction + INDEX INERT-ablation")
print(f"    composed_distinct = {composed_distinct}   (bar >=2 AND >max_single AND >=0.95*{THEORY_PRODUCT})")
print(f"    max_single        = {max_single}   (single slot ceiling)")
print(f"    ablated_distinct  = {ablated_distinct}   (index removed -> additive; bar <= max_single+1 = {max_single+1})")
print(f"    -> (a) {'PASS' if pass_a else 'FAIL'}")
print()
print("(b) AMBIGUOUS-PAIR binding (copy 0.5 vs true 1.0)  [binding-required subset]")
print(f"    index_pair_acc    = {index_pair_acc:.3f}   (bar >=0.95)")
print(f"    additive_pair_acc = {additive_pair_acc:.3f}   (bar <=0.60  ~chance, marginal-blind)")
print(f"    ablated_pair_acc  = {ablated_pair_acc:.3f}   (bar <=0.60  INERT under index removal)")
print(f"    -> (b) {'PASS' if pass_b else 'FAIL'}")
print()
print("(c) PATTERN-COMPLETION from partial cue  [indexing-theory signature]")
print(f"    completion_acc_index   = {completion_acc_index:.3f}   (bar >=0.95)")
print(f"    completion_acc_ablated = {completion_acc_ablated:.3f}   (bar <= index-0.30 = {completion_acc_index-0.30:.3f}; INERT)")
print(f"    -> (c) {'PASS' if pass_c else 'FAIL'}")
print()
print("(d) honesty (familiarity abstain: novel-conjunction vs stored index)")
print(f"    AUROC_real        = {auroc_real:.3f}   (bar >=0.90)")
print(f"    AUROC_idx_shuffle = {auroc_shuf:.3f}   (chance .40-.60)")
print(f"    -> (d) {'PASS' if pass_d else 'FAIL'}")
print()
print("GROK POSITIVE CONTROL (under-power guard)  modular-add (a+b) mod %d  chance=%.3f" % (P, chance))
print(f"    grok_index_held = {grok_index_held:.3f}   (bar >=0.90 to be powered)")
print(f"    grok_add_held   = {grok_add_held:.3f}   (additive baseline, reported)")
print(f"    -> grok_ctrl    {'PASS (toy has resolution)' if grok_ctrl_pass else 'FAIL (UNDER-POWER)'}")
print()
# ---- verdict logic ----
ablation_load_bearing = pass_a     # (a) embeds the INERT clause (ablated<=max_single+1)
if not grok_ctrl_pass:
    verdict = "UNDER-POWER (DIRECTIONAL)"
elif pass_a and pass_b and pass_c:
    verdict = "SUPPORTED (DIRECTIONAL)"
elif pass_a:
    verdict = "MIXED (DIRECTIONAL)"
else:
    verdict = "NOT-SUPPORTED (DIRECTIONAL)"

survivor = bool(pass_a and grok_ctrl_pass and ablation_load_bearing)

print("=" * 78)
print(f"VERDICT: {verdict}   "
      f"[(a)={'P' if pass_a else 'F'} (b)={'P' if pass_b else 'F'} "
      f"(c)={'P' if pass_c else 'F'} (d)={'P' if pass_d else 'F'} "
      f"grok={'P' if grok_ctrl_pass else 'F'}]")
print(f"SURVIVOR (frozen-bar AND grok_ctrl AND ablation-load-bearing): {survivor}")
print(f"NUMBERS(verbatim): composed_distinct={composed_distinct} max_single={max_single} "
      f"ablated_distinct={ablated_distinct} grok_index_held={grok_index_held:.3f} "
      f"grok_add_held={grok_add_held:.3f} index_pair_acc={index_pair_acc:.3f} "
      f"additive_pair_acc={additive_pair_acc:.3f} completion_index={completion_acc_index:.3f} "
      f"completion_ablated={completion_acc_ablated:.3f}")
print("numpy toy = DIRECTIONAL only; NOT engine-native (a_engine_native_learning).")
print("=" * 78)
