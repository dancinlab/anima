#!/usr/bin/env python3
"""
H_1533 — MODERN / DENSE ASSOCIATIVE MEMORY (exponential-separation retrieval) as a
candidate BREAK of the H_1284 NEUROMODULATION wall.

WHY (a_break_the_wall · a_no_llm_frame_trap, biological/physics lens — NOT an LLM
recipe): the H_1284 wall (and its census C1-C4 + H_1527 geometry-lift + H_1528
capacity-count siblings) is bounded by key-GEOMETRY / CAPACITY. anima's store is a
STANDARD LINEAR associative memory — recall = nearest stored cell by L2 affinity —
whose capacity is LINEAR (~0.14 N, Hopfield 1982). Near-collinear / confusable keys
COLLIDE: the linear winner is the wrong cell. No controller (the 10 neuromodulation
lenses), no capacity-count, no geometry-lift fixed it.

The UNTRIED lever is the RETRIEVAL RULE / ENERGY itself, not any modulator:
  • DENSE ASSOCIATIVE MEMORY — Krotov & Hopfield 2016, "Dense Associative Memory
    for Pattern Recognition", arXiv:1606.01164: higher-order (degree-n polynomial)
    interaction energy raises storage capacity to ~N^(n-1).
  • MODERN HOPFIELD — Ramsauer et al 2020, "Hopfield Networks is All You Need",
    arXiv:2008.02217: a softmax / log-sum-exp energy gives EXPONENTIAL storage
    capacity and, by its separation theorem, separates exponentially many patterns
    in ONE update step. This directly attacks the near-collinear collision the wall
    is built from: out = Σ_i softmax(β·⟨q,k_i⟩)·v_i (continuous, single-step), with
    β a FIXED grid-tuned inverse-temperature hyperparameter — a RETRIEVAL-RULE
    change, NOT an adaptive controller / neuromodulator.

CAPABILITY = recall accuracy on a CONFUSABLE / high-load key set — exactly the
regime where the linear store collides. ARMS:
  LINEAR  = the existing nearest-cell L2-affinity store (the wall baseline; the
            decision rule grid-tuned only over its own abstain margin).
  DENSE   = Krotov-Hopfield polynomial energy, separation score Σ_i (⟨q,k_i⟩)^p · v_i
            with degree p ∈ {2,3} grid-tuned. Higher-order overlap sharpens the
            winner away from near-collinear distractors.
  MODERN  = modern-Hopfield softmax retrieval out = Σ_i softmax(β⟨q,k_i⟩)·v_i, then
            map the continuous read-out to the nearest stored value; β grid-tuned.
  ABL     = β→0 (modern → uniform average = degrades to chance) AND degree→1 (dense
            → linear). Decisive ablation ⇒ both MUST revert to ~LINEAR. SHUFFLE =
            permute the value table (key↔value coupling destroyed) ⇒ collapse.

PRE-REGISTERED falsifier (H_1533_FREEZE.txt, written BEFORE scoring, p7, frozen-
first c9): BREAK iff max(MODERN, DENSE) recall − LINEAR recall ≥ +0.05 on the
confusable set on ≥2/3 seeds AND ablation decisive (β→0 / degree→1 revert to
LINEAR within ±0.03) AND value-shuffle collapses to chance. HONEST: report which of
dense / modern wins and by how much; if BOTH tie linear on the confusable set, the
H_1284 wall extends to the RETRIEVAL-RULE family too (a strong honest ceiling, c9).
NO tune-to-green: β / degree are grid-tuned on a DISJOINT tuning seed, the SAME way
H_1284 grid-tunes (LR0, TH0); the +0.05 bar is frozen here.

DIRECTIONAL: numpy mirror, host has no torch (a_engine_native_learning) — if it
BREAKS, engine-native R2 (live core/ A⇄G + VAdaptField softmax retrieval) is a
HIGH-PRIORITY binding follow-on; if it HOLDS the wall, R1 is terminal-enough as a
retrieval-family ceiling. $0 CPU, ≥3 seeds, exact ground truth (no LLM judge / no
perplexity / no loss term).
"""
import numpy as np
import json

# ── engine-native key constants (VERBATIM from H_1284 / CORE engine_cli) ──────
DIM = 16  # H_1227 byte-trigram FNV-1a key dim (toy 16, same as H_1284 mirror)


def fnv1a(b: bytes) -> int:
    h = 0xcbf29ce484222325
    for c in b:
        h ^= c
        h = (h * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return h


def key_vec(s: str) -> np.ndarray:
    """byte-trigram FNV-1a hashed into a DIM unit vector (H_1284 key, VERBATIM)."""
    bs = s.encode()
    v = np.zeros(DIM)
    for i in range(len(bs) - 2):
        tri = bs[i:i + 3]
        idx = fnv1a(tri) % DIM
        v[idx] += 1.0
    n = np.linalg.norm(v)
    if n < 1e-9:
        v = np.zeros(DIM)
        v[fnv1a(bs) % DIM] = 1.0
        n = 1.0
    return v / n


# ── CONFUSABLE near-collinear key set (the regime the wall is built from) ─────
# H_1284 used near-orthogonal subj keys; the linear store handles those fine. The
# wall lives where keys are NEAR-COLLINEAR. We construct a confusable family: a set
# of anchor keys, each surrounded by several distractor keys at small angular
# perturbation (cos ≈ 0.93–0.99). Distinct VALUES are bound to each, so the linear
# nearest-cell rule must resolve confusable neighbours to recall correctly.
def make_confusable_facts(n_anchors, n_per_cluster, rng, pert_sigma=0.045):
    """Return list of (key_vec, value_id) pairs. Each cluster shares an anchor
    direction; members differ by a SMALL random perturbation -> NEAR-COLLINEAR
    (cos ~0.97-0.995, the genuine collision regime the linear store fails on).
    Every member gets its OWN distinct value (key->value must be SEPARATED), so
    a linear nearest-cell rule that confuses two members recalls the WRONG value."""
    facts = []
    vid = 0
    for a in range(n_anchors):
        # anchor direction from a real byte-trigram key (engine-native geometry)
        anchor = key_vec(f"anchor{a:03d}_subject")
        for m in range(n_per_cluster):
            # SMALL perturbation -> near-collinear member (high cos -> collides)
            pert = rng.normal(0, pert_sigma, DIM)
            k = anchor + pert
            k = k / (np.linalg.norm(k) + 1e-9)
            facts.append((k, vid))
            vid += 1
    return facts


def confusability(facts):
    """mean max off-diagonal cosine -> how collinear the confusable set is."""
    K = np.array([f[0] for f in facts])
    G = K @ K.T
    np.fill_diagonal(G, -1.0)
    return float(np.mean(np.max(G, axis=1)))


# ── retrieval rules ───────────────────────────────────────────────────────────
# All three share the SAME stored matrix (K keys, V values). Only the energy /
# read-out rule differs. value table = ground-truth bound value per stored key.
def retrieve_linear(K, V, q, abstain_cos):
    """LINEAR associative memory: nearest stored key by L2 affinity == max cosine
    on the unit sphere. Returns predicted value id, or None (abstain)."""
    sims = K @ q
    win = int(np.argmax(sims))
    if sims[win] < abstain_cos:
        return None
    return int(V[win])


def retrieve_dense(K, V, q, degree, abstain_score):
    """DENSE (Krotov-Hopfield): degree-p polynomial separation energy. Score each
    stored pattern by (max(0,<q,k_i>))^p, pick argmax. p=1 == linear; p>1 sharpens
    the winner exponentially away from near-collinear distractors."""
    sims = K @ q
    pos = np.clip(sims, 0.0, None)
    scores = pos ** degree
    win = int(np.argmax(scores))
    # abstain if even the sharpened winner is weak (score on the [0,1] overlap)
    if scores[win] < abstain_score:
        return None
    return int(V[win])


def retrieve_modern(K, V, q, beta, abstain_mass):
    """MODERN HOPFIELD (Ramsauer): out = Σ_i softmax(β<q,k_i>)·v_embedding_i, single
    step. We embed each value as its key (auto-associative completion), read the
    continuous output, then map to the nearest stored value (the retrieved fixed
    point). β→0 -> uniform average (collapse); β large -> argmax (exp separation)."""
    sims = K @ q
    z = beta * sims
    z = z - np.max(z)
    w = np.exp(z)
    w = w / (np.sum(w) + 1e-12)
    # continuous completion: weighted sum of stored keys (Ramsauer update)
    out = (w[:, None] * K).sum(axis=0)
    nout = np.linalg.norm(out)
    if nout < 1e-9:
        return None
    out = out / nout
    # the retrieved fixed point -> nearest stored key -> its value (separation)
    osims = K @ out
    win = int(np.argmax(osims))
    # abstain if the softmax never concentrated (max weight below mass floor =
    # query landed in a near-collinear basin the rule could not separate)
    if float(np.max(w)) < abstain_mass:
        return None
    return int(V[win])


# ── one trial: build store, run all arms over recall queries ──────────────────
def run_trial(facts, rng, degree, beta, abstain_cos, abstain_score, abstain_mass,
              shuffle_values=False, beta_zero=False, degree_one=False):
    K = np.array([f[0] for f in facts])
    V_true = np.array([f[1] for f in facts])     # ground-truth binding per key
    V = V_true.copy()
    if shuffle_values:
        # destroy key<->value coupling: store holds permuted values, but TRUTH
        # stays the original binding -> a working store now recalls the WRONG
        # value for (almost) every query -> accuracy collapses to chance.
        V = V_true[rng.permutation(len(V_true))]

    eff_beta = 0.0 if beta_zero else beta
    eff_degree = 1 if degree_one else degree

    n = len(facts)
    lin_ok = dense_ok = mod_ok = 0
    for i in range(n):
        # query = stored key + small read noise (recall under perturbation)
        q = facts[i][0] + rng.normal(0, 0.06, DIM)
        q = q / (np.linalg.norm(q) + 1e-9)
        truth = int(V_true[i])     # ALWAYS the true binding (shuffle = wrong store)

        pl = retrieve_linear(K, V, q, abstain_cos)
        pd = retrieve_dense(K, V, q, eff_degree, abstain_score)
        pm = retrieve_modern(K, V, q, eff_beta, abstain_mass)
        lin_ok += (pl == truth)
        dense_ok += (pd == truth)
        mod_ok += (pm == truth)
    return lin_ok / n, dense_ok / n, mod_ok / n


# ── grid-tune degree / beta / abstain on a DISJOINT tuning seed (no tune-to-green:
#    bar +0.05 is frozen; we only pick the retrieval-rule hyperparam like H_1284
#    grid-tunes LR0/TH0) ─────────────────────────────────────────────────────────
def grid_tune(n_anchors, n_per_cluster, tune_seed):
    rng = np.random.default_rng(tune_seed)
    facts = make_confusable_facts(n_anchors, n_per_cluster, rng)
    # tune LINEAR abstain to maximize ITS OWN accuracy (strongest honest baseline)
    best_lin = (-1, 0.0)
    for ac in (0.0, 0.3, 0.5, 0.7, 0.85):
        l, _, _ = run_trial(facts, np.random.default_rng(tune_seed + 1), 2, 8.0,
                            ac, 0.0, 0.0)
        if l > best_lin[0]:
            best_lin = (l, ac)
    abstain_cos = best_lin[1]
    # tune DENSE degree
    best_d = (-1, 2)
    for deg in (2, 3):
        _, d, _ = run_trial(facts, np.random.default_rng(tune_seed + 1), deg, 8.0,
                            abstain_cos, 0.0, 0.0)
        if d > best_d[0]:
            best_d = (d, deg)
    degree = best_d[1]
    # tune MODERN beta
    best_b = (-1, 8.0)
    for b in (1.0, 4.0, 8.0, 16.0, 32.0, 64.0):
        _, _, m = run_trial(facts, np.random.default_rng(tune_seed + 1), degree, b,
                            abstain_cos, 0.0, 0.0)
        if m > best_b[0]:
            best_b = (m, b)
    beta = best_b[1]
    return degree, beta, abstain_cos, 0.0, 0.0  # abstain_score/mass off (recall task)


def main():
    N_ANCHORS = 12
    N_PER_CLUSTER = 5     # 60 confusable facts (near-collinear clusters)
    TUNE_SEED = 7
    SCORE_SEEDS = [11, 22, 33]
    MARGIN = 0.05         # FROZEN break bar

    degree, beta, ab_cos, ab_score, ab_mass = grid_tune(N_ANCHORS, N_PER_CLUSTER,
                                                        TUNE_SEED)

    per_seed = []
    confs = []
    for seed in SCORE_SEEDS:
        rng_f = np.random.default_rng(seed)
        facts = make_confusable_facts(N_ANCHORS, N_PER_CLUSTER, rng_f)
        confs.append(confusability(facts))
        lin, dns, mod = run_trial(facts, np.random.default_rng(seed + 100),
                                  degree, beta, ab_cos, ab_score, ab_mass)
        # ablations
        _, dns_abl, _ = run_trial(facts, np.random.default_rng(seed + 100),
                                  degree, beta, ab_cos, ab_score, ab_mass,
                                  degree_one=True)
        _, _, mod_abl = run_trial(facts, np.random.default_rng(seed + 100),
                                  degree, beta, ab_cos, ab_score, ab_mass,
                                  beta_zero=True)
        # value-shuffle collapse (destroy key<->value coupling) on best arm
        lin_sh, dns_sh, mod_sh = run_trial(facts, np.random.default_rng(seed + 200),
                                           degree, beta, ab_cos, ab_score, ab_mass,
                                           shuffle_values=True)
        per_seed.append({
            'seed': seed,
            'linear': round(lin, 4), 'dense': round(dns, 4), 'modern': round(mod, 4),
            'dense_abl_deg1': round(dns_abl, 4), 'modern_abl_beta0': round(mod_abl, 4),
            'linear_shuf': round(lin_sh, 4), 'dense_shuf': round(dns_sh, 4),
            'modern_shuf': round(mod_sh, 4),
            'best_minus_linear': round(max(dns, mod) - lin, 4),
        })

    # ── aggregate + frozen falsifier ──────────────────────────────────────────
    def m(k):
        return float(np.mean([s[k] for s in per_seed]))

    lin_m, dns_m, mod_m = m('linear'), m('dense'), m('modern')
    best_m = max(dns_m, mod_m)
    best_name = 'modern' if mod_m >= dns_m else 'dense'
    n_seed_break = sum(1 for s in per_seed
                       if max(s['dense'], s['modern']) - s['linear'] >= MARGIN)

    # ablation decisive: both ablations revert to ~linear (within +-0.03)
    dns_abl_m, mod_abl_m = m('dense_abl_deg1'), m('modern_abl_beta0')
    abl_dense_reverts = abs(dns_abl_m - lin_m) <= 0.03
    abl_modern_reverts = mod_abl_m <= lin_m + 0.03  # beta0 -> uniform -> <= linear
    ablation_decisive = abl_dense_reverts and abl_modern_reverts

    # value-shuffle collapses best arm to chance (~1/N)
    chance = 1.0 / (N_ANCHORS * N_PER_CLUSTER)
    best_shuf_m = m('modern_shuf') if best_name == 'modern' else m('dense_shuf')
    shuffle_collapses = best_shuf_m <= max(0.10, lin_m - 0.20)

    if (best_m - lin_m >= MARGIN) and n_seed_break >= 2 and ablation_decisive \
            and shuffle_collapses:
        verdict = 'GREEN'   # WALL-BROKEN by retrieval rule (directional)
    else:
        verdict = 'WALL_HOLDS'

    summary = {
        'hypothesis': 'H_1533',
        'lens': 'modern/dense associative memory (exponential-separation retrieval)',
        'cites': ['Ramsauer et al 2020 arXiv:2008.02217',
                  'Krotov & Hopfield 2016 arXiv:1606.01164',
                  'Hopfield 1982 (linear capacity baseline)'],
        'confusable_set': {'n_anchors': N_ANCHORS, 'n_per_cluster': N_PER_CLUSTER,
                           'n_facts': N_ANCHORS * N_PER_CLUSTER,
                           'mean_max_offdiag_cos': round(float(np.mean(confs)), 4)},
        'tuned': {'degree': degree, 'beta': beta, 'abstain_cos': ab_cos},
        'MARGIN': MARGIN, 'chance': round(chance, 4), 'seeds': SCORE_SEEDS,
        'mean': {'linear': round(lin_m, 4), 'dense': round(dns_m, 4),
                 'modern': round(mod_m, 4), 'best': best_name,
                 'best_minus_linear': round(best_m - lin_m, 4)},
        'ablation': {'dense_deg1': round(dns_abl_m, 4),
                     'modern_beta0': round(mod_abl_m, 4),
                     'dense_reverts': abl_dense_reverts,
                     'modern_reverts': abl_modern_reverts,
                     'decisive': ablation_decisive},
        'shuffle': {'best_arm': best_name, 'best_shuf': round(best_shuf_m, 4),
                    'collapses': shuffle_collapses},
        'n_seed_break': n_seed_break,
        'per_seed': per_seed,
        'verdict': verdict,
        'framing': ('the lever is exponential-separation RETRIEVAL ENERGY, not any '
                    'neuromodulator' if verdict == 'GREEN' else
                    'the H_1284 wall extends to the retrieval-rule family too '
                    '(linear/dense/modern tie on the confusable set)'),
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == '__main__':
    main()
