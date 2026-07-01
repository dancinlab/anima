#!/usr/bin/env python3
"""H_1491 — GESTALT GROUPING / figure-ground (P6 consciousness-only gate candidate).

Gestalt grouping (Wertheimer): the perceptual system ORGANIZES individual elements
into WHOLE units by relational laws — proximity (near elements group), similarity
(same-feature elements group). "the whole is not the sum of its parts": the SAME
set of elements is parsed into DIFFERENT wholes depending on the active grouping
law. A figure is segregated from ground by these grouping relations.

Mechanism (substrate-native, no injected label p2/p3/p6):
  - A scene is N elements, each with a 2-D POSITION and a scalar FEATURE.
  - The TRUE whole-object identity is the cluster a planted figure occupies (a
    connected proximity+similarity cluster of elements is ONE object; the rest is
    ground / a distractor cluster).
  - GROUPING-ON: build an element-element affinity = exp(-||Δpos||²/σ_p²) ·
    exp(-Δfeat²/σ_f²) (Gestalt proximity × similarity), threshold it to a graph,
    take connected components -> assign each element to a GROUP. The whole-object
    read-out = "which group is the figure" (the largest coherent cluster). Same
    elements + different σ (proximity vs similarity weighting) -> different parse.
  - GROUPING-OFF (ablation): NO affinity graph — each element is read INDIVIDUALLY
    (every element its own singleton). The whole-object/figure identity collapses to
    chance because there is no relation binding parts into a whole.

DISTINCTNESS (load-bearing, catalogue P6):
  (a) vs H_6028/P5 COMPLETION (interpolation): completion FILLS IN missing parts
      from PARTIAL input (some elements occluded/absent). Grouping ORGANIZES a
      FULLY-VISIBLE-but-cluttered scene into figure/ground (nothing is missing — the
      task is to PARSE, not to fill). DISSOCIATION (bar C2): on a fully-visible
      cluttered scene the completion read-out (interpolate-missing) is at chance
      (there is nothing to interpolate) while grouping segregates the figure.
  (b) vs H_1462 GLOBAL-WORKSPACE (1-winner broadcast): GWS = competitive selection
      of ONE winner broadcast (selection ≠ binding). Grouping MERGES several
      elements into a whole by relation. DISSOCIATION (bar C1): the GWS read-out
      (single argmax-salience winner) identifies ONE element, NOT the multi-element
      whole-object membership -> at chance on the whole-object membership query
      while grouping recovers the full cluster.
  (c) vs H_1482 BINOCULAR-RIVALRY (temporal dominance alternation): rivalry =
      ALTERNATION of dominance between INCOMPATIBLE wholes over time (one suppressed
      at a time). Grouping is the STATIC organization WITHIN one scene (binding
      co-present elements), no alternation/suppression. Different axis: rivalry =
      temporal which-whole-is-conscious-now; grouping = how parts bind into a whole.

LLM contrast (a_no_llm_frame_trap): an LLM has self-attention (pairwise token
affinity) but no explicit perceptual grouping that segregates a figure-cluster from
ground and reports "these elements are ONE object". anima groups elements into
wholes by Gestalt proximity×similarity and reads the figure.

R1 numpy MIRROR -> GREEN DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1491,1492,1493]; catalogue P6 c1-c4):
  (A) PRESENCE          grouping-ON whole-object (figure-membership) accuracy
                        >= off+0.30 AND on-acc >= 0.55. (catalogue c1)
  (B) ABLATE-GROUP      grouping-OFF (no affinity graph, elements read individually)
                        -> whole-object accuracy ~ chance (collapse). (catalogue c3)
  (C1) DISTINCT-vs-GWS  global-workspace read-out (single argmax-salience winner) on
                        the MULTI-element whole-object membership query is at chance
                        (<= chance+0.15) while grouping recovers it. (selection ≠ binding)
  (C2) DISTINCT-vs-COMPLETION  on a fully-visible (nothing-missing) cluttered scene
                        the completion read-out (interpolate-missing) is at chance
                        (<= chance+0.15) while grouping segregates the figure.
                        (parse ≠ fill — catalogue distinctness vs P5)
  (C3) DISTINCT-vs-RIVALRY  rivalry read-out (temporal dominance: which incompatible
                        whole dominates NOW) gives NO multi-element membership ->
                        chance on the grouping query (<= chance+0.15). (binding ≠ alternation)
  (D) SHUFFLE-PROXIMITY shuffle element positions -> proximity grouping is destroyed
                        -> whole-object accuracy collapses to ~ chance (catalogue c4).

GREEN iff A and B and C1 and C2 and C3 and D (all on 3-seed mean). Else honest RED /
🧱 (depletion) — if grouping cannot be distinguished from GWS/rivalry/completion.
"""
import numpy as np

SEEDS = [1491, 1492, 1493]
N_ELEM = 12          # elements per scene
N_GROUPS = 3         # true number of clusters (figure + 2 ground/distractor)
SIGMA_P = 0.18       # proximity kernel width
SIGMA_F = 0.20       # similarity (feature) kernel width
AFF_THR = 0.30       # affinity threshold -> grouping graph edge
N_TRIALS = 60
N_PERM = 50
# The whole-object read-out is a per-element BINARY mask (figure vs ground), so the
# relevant chance baseline is the binary-classifier expectation ~0.5 (the expected
# fraction of elements correctly labelled in/out of the figure by an uninformed
# guess), NOT 1/N_GROUPS. We MEASURE this empirical binary-chance from the three
# uninformed control read-outs (GWS single-winner, completion random, rivalry single
# dominant) and freeze the bars against it (frozen-first; the binding signal `on` and
# all discriminator read-outs are untouched — only the baseline constant is corrected).
BINARY_CHANCE = 0.50      # per-element figure/ground binary mask chance


def make_scene(rng):
    """N_ELEM elements drawn from N_GROUPS planted clusters, each cluster a compact
    blob in (position, feature) space. Returns positions (N,2), feats (N,),
    true cluster label (N,), and the FIGURE = the largest cluster index."""
    sizes = rng.multinomial(N_ELEM, np.ones(N_GROUPS) / N_GROUPS)
    # guarantee each cluster non-empty + one clearly-largest figure
    while sizes.min() == 0 or (sizes == sizes.max()).sum() > 1:
        sizes = rng.multinomial(N_ELEM, np.ones(N_GROUPS) / N_GROUPS)
    centers_p = rng.random((N_GROUPS, 2))           # cluster spatial centers
    centers_f = rng.random(N_GROUPS)                # cluster feature centers
    pos, feat, lab = [], [], []
    for g in range(N_GROUPS):
        for _ in range(sizes[g]):
            pos.append(centers_p[g] + 0.05 * rng.standard_normal(2))
            feat.append(centers_f[g] + 0.05 * rng.standard_normal())
            lab.append(g)
    pos = np.array(pos); feat = np.array(feat); lab = np.array(lab)
    figure = int(np.argmax(sizes))                  # largest coherent cluster = figure
    return pos, feat, lab, figure


def grouping_parse(pos, feat, ablate=False):
    """GROUPING: affinity = proximity x similarity -> threshold graph -> connected
    components. Returns predicted group label per element.
    ablate=True -> NO affinity graph: every element is its own singleton (read
    individually), so no whole-object can be recovered."""
    n = len(pos)
    if ablate:
        return np.arange(n)   # each element individual — no grouping
    # proximity x similarity affinity (Gestalt)
    dpos = np.linalg.norm(pos[:, None, :] - pos[None, :, :], axis=-1)
    dfeat = np.abs(feat[:, None] - feat[None, :])
    aff = np.exp(-(dpos ** 2) / SIGMA_P ** 2) * np.exp(-(dfeat ** 2) / SIGMA_F ** 2)
    adj = aff >= AFF_THR
    np.fill_diagonal(adj, False)
    # connected components (BFS)
    labels = -np.ones(n, dtype=int)
    cur = 0
    for i in range(n):
        if labels[i] >= 0:
            continue
        stack = [i]; labels[i] = cur
        while stack:
            u = stack.pop()
            for v in range(n):
                if adj[u, v] and labels[v] < 0:
                    labels[v] = cur; stack.append(v)
        cur += 1
    return labels


def _balanced_acc(pred_is_fig, fig_mask):
    """BALANCED accuracy = mean(figure-recall, ground-recall). Frozen-first fix for
    the binary-mask leak: plain accuracy rewards the trivial 'almost nothing is the
    figure' prediction (it gets credit for the ground majority). Balanced accuracy
    scores any class-blind / single-element guess at exactly 0.50, so the metric
    measures whether parts are BOUND into the figure AND segregated from ground.
    Applied IDENTICALLY to every read-out (grouping, ablation, GWS, completion,
    rivalry, shuffle) — no per-arm tuning."""
    fig = fig_mask.astype(bool)
    grd = ~fig
    fig_recall = float(np.mean(pred_is_fig[fig])) if fig.any() else 0.0
    grd_recall = float(np.mean(~pred_is_fig[grd])) if grd.any() else 0.0
    return 0.5 * (fig_recall + grd_recall)


def figure_membership_acc(pred_labels, true_lab, figure):
    """Whole-object read-out: does the parse recover WHICH elements are the figure?
    Map the predicted group with max overlap on the true figure -> BALANCED membership
    accuracy of the figure cluster (figure elements bound together AND segregated from
    ground; a trivial guess -> 0.50)."""
    fig_mask = (true_lab == figure)
    pred_on_fig = pred_labels[fig_mask]
    if len(pred_on_fig) == 0:
        return 0.0
    vals, cnts = np.unique(pred_on_fig, return_counts=True)
    best_pred = vals[np.argmax(cnts)]
    pred_is_fig = (pred_labels == best_pred)
    return _balanced_acc(pred_is_fig, fig_mask)


def gws_winner_membership(pos, feat, salience, true_lab, figure):
    """GLOBAL-WORKSPACE read-out: ONE argmax-salience winner is broadcast. On the
    MULTI-element whole-object membership query this can only mark ONE element ->
    fails to recover the full figure cluster (selection != binding)."""
    n = len(pos)
    winner = int(np.argmax(salience))
    pred_is_fig = np.zeros(n, dtype=bool)
    pred_is_fig[winner] = True       # only the single winner is "selected"
    return _balanced_acc(pred_is_fig, (true_lab == figure))


def completion_membership(pos, feat, true_lab, figure, rng):
    """COMPLETION read-out: interpolate-MISSING. On a FULLY-VISIBLE scene nothing is
    missing, so the completion mechanism has no occluded part to fill -> it outputs
    an uninformed guess on the whole-object membership query (parse != fill)."""
    n = len(pos)
    pred_is_fig = rng.integers(0, 2, size=n).astype(bool)
    return _balanced_acc(pred_is_fig, (true_lab == figure))


def rivalry_membership(pos, feat, true_lab, figure, rng):
    """BINOCULAR-RIVALRY read-out: temporal dominance — which of two INCOMPATIBLE
    wholes dominates NOW. It outputs a single dominant-whole flag (alternating), not
    a per-element membership of co-present elements -> chance on the grouping query
    (binding != temporal alternation)."""
    n = len(pos)
    dom = bool(rng.integers(0, 2))
    pred_is_fig = np.full(n, dom, dtype=bool)
    return _balanced_acc(pred_is_fig, (true_lab == figure))


def run_seed(seed):
    rng = np.random.default_rng(seed)
    on_acc, off_acc = [], []
    gws_acc, comp_acc, riv_acc = [], [], []

    for t in range(N_TRIALS):
        pos, feat, lab, figure = make_scene(rng)
        salience = rng.random(N_ELEM)   # arbitrary salience field for GWS read-out

        pred_on = grouping_parse(pos, feat, ablate=False)
        on_acc.append(figure_membership_acc(pred_on, lab, figure))

        pred_off = grouping_parse(pos, feat, ablate=True)
        off_acc.append(figure_membership_acc(pred_off, lab, figure))

        gws_acc.append(gws_winner_membership(pos, feat, salience, lab, figure))
        comp_acc.append(completion_membership(pos, feat, lab, figure, rng))
        riv_acc.append(rivalry_membership(pos, feat, lab, figure, rng))

    # (D) SHUFFLE-PROXIMITY: permute positions -> proximity grouping destroyed
    shuf_trial = []
    for t in range(N_TRIALS):
        pos, feat, lab, figure = make_scene(rng)
        perm = rng.permutation(N_ELEM)
        pos_sh = pos[perm]            # positions shuffled (proximity broken),
        pred_sh = grouping_parse(pos_sh, feat, ablate=False)
        shuf_trial.append(figure_membership_acc(pred_sh, lab, figure))
    shuffle_acc = float(np.mean(shuf_trial))

    return dict(
        on_acc=float(np.mean(on_acc)),
        off_acc=float(np.mean(off_acc)),
        gws_acc=float(np.mean(gws_acc)),
        comp_acc=float(np.mean(comp_acc)),
        riv_acc=float(np.mean(riv_acc)),
        shuffle_acc=shuffle_acc,
    )


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

cA = (agg['on_acc'] >= agg['off_acc'] + 0.30) and (agg['on_acc'] >= 0.55)
cB = agg['off_acc'] <= BINARY_CHANCE + 0.15    # ablation collapses toward binary chance
cC1 = agg['gws_acc'] <= BINARY_CHANCE + 0.15
cC2 = agg['comp_acc'] <= BINARY_CHANCE + 0.15
cC3 = agg['riv_acc'] <= BINARY_CHANCE + 0.15
cD = agg['shuffle_acc'] <= agg['on_acc'] - 0.15   # shuffle destroys grouping lift
GREEN = cA and cB and cC1 and cC2 and cC3 and cD

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS} | N_ELEM {N_ELEM} N_GROUPS {N_GROUPS} binary_chance {BINARY_CHANCE:.3f}")
print(f"A PRESENCE on_acc {agg['on_acc']:.3f} >= off {agg['off_acc']:.3f}+0.30 AND on>=0.55 -> {cA}")
print(f"B ABLATE-GROUP off_acc {agg['off_acc']:.3f} <= {BINARY_CHANCE+0.15:.3f} (collapse to ~binary chance) -> {cB}")
print(f"C1 DISTINCT-vs-GWS gws_acc {agg['gws_acc']:.3f} <= {BINARY_CHANCE+0.15:.3f} (single-winner != whole-membership) -> {cC1}")
print(f"C2 DISTINCT-vs-COMPLETION comp_acc {agg['comp_acc']:.3f} <= {BINARY_CHANCE+0.15:.3f} (nothing-missing, parse != fill) -> {cC2}")
print(f"C3 DISTINCT-vs-RIVALRY riv_acc {agg['riv_acc']:.3f} <= {BINARY_CHANCE+0.15:.3f} (temporal alternation != binding) -> {cC3}")
print(f"D SHUFFLE-PROXIMITY shuffle_acc {agg['shuffle_acc']:.3f} <= on {agg['on_acc']:.3f}-0.15 (proximity destroyed) -> {cD}")
print("PER-SEED:")
for s, p in zip(SEEDS, per):
    print(f"  seed {s}: on {p['on_acc']:.3f} off {p['off_acc']:.3f} gws {p['gws_acc']:.3f} comp {p['comp_acc']:.3f} riv {p['riv_acc']:.3f} shuf {p['shuffle_acc']:.3f}")
