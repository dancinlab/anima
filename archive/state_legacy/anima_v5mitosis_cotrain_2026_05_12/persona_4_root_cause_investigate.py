"""state/anima_v5mitosis_cotrain_2026_05_12/persona_4_root_cause_investigate.py

PURPOSE
    F-PERSONA-4 cotrained KL=0.0 root cause investigation.
    Cotrained ckpt (`ckpt_v5mitosis_cotrain_cotrain.pt`) re-measure FAILed F-PERSONA-4
    (mean KL across 5-category pairs = 0.0). 4 hypotheses to discriminate:

    (a) softmax-saturation/temperature: tension softmax(N=64) collapsed to ~delta or
        ~uniform → all per-prompt weight distributions identical → KL = 0.
    (b) gate_proj-rank-collapse: per-cell ffn_g (or ffn_a) weight matrix rank << 64
        across the cell pool → effective cell diversity dies post-cotrain.
    (c) corpus-category-mismatch: cotrain corpus (color_cosmology 1.3 MB) shares 0
        semantic surface area with identity_probe 5 categories
        (self_definition/values/boundary/emotion/self_knowledge) → no gradient
        signal differentiated cell pool across those axes during cotrain.
    (d) cell-pool-diversity-collapse: F-PERSONA-2 measured pre-cotrain mean cell
        pair cos dist 0.994 (orthogonal basis). Post-cotrain cells may have
        converged toward each other → diversity gone.

    Investigation produces JSON `persona_4_root_cause_results.json` + verdict.

    Phase 1 OUTPUT only — Phase 2/3 interventions decided based on these numbers.

OUTPUT
    state/anima_v5mitosis_cotrain_2026_05_12/persona_4_root_cause_results.json
        {
          "hypothesis_a_softmax_entropy": {...},   # per-prompt entropy distribution
          "hypothesis_b_gate_proj_rank":  {...},   # SVD rank of stacked ffn_g first linear
          "hypothesis_c_corpus_diversity":{...},   # per-category hidden state mean / pairwise
          "hypothesis_d_cell_diversity":  {...},   # cell_state pairwise cos dist
          "raw_tensions": [...],                   # per-prompt raw scalar tens (50, 64)
          "raw_weights":  [...],                   # softmax weights (50, 64)
          "primary_root_cause": "...",
          "intervention_recommendation": "..."
        }

USAGE
    python3 state/anima_v5mitosis_cotrain_2026_05_12/persona_4_root_cause_investigate.py
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

import torch
import torch.nn.functional as F

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "training"))

from mitosis_model_v5 import MitosisModelConfig, MitosisModelEngine  # noqa: E402


CKPT_PATH = HERE / "ckpts" / "ckpt_v5mitosis_cotrain_cotrain.pt"
IDENTITY_PROBE = HERE / "identity_probe.jsonl"
OUT_JSON = HERE / "persona_4_root_cause_results.json"


def text_to_bytes(text: str, max_len: int) -> List[int]:
    return list(text.encode("utf-8"))[:max_len]


def load_engine(device: torch.device) -> Tuple[MitosisModelEngine, Dict]:
    print(f"[LOAD] {CKPT_PATH}")
    # PyTorch 2.6 default weights_only=True trips on dataclass config dicts; use False.
    try:
        ckpt = torch.load(CKPT_PATH, map_location="cpu", weights_only=False)
    except TypeError:
        ckpt = torch.load(CKPT_PATH, map_location="cpu")
    cfg = MitosisModelConfig(**ckpt["config"])
    engine = MitosisModelEngine(cfg)
    target_n = ckpt["n_cells"]
    print(f"[LOAD] cfg n_layer={cfg.n_layer} d={cfg.d_model} cells_init={cfg.initial_cells} -> target={target_n}")
    # Replay split events to reach target cell count (force_split deepcopies + adds noise;
    # we'll overwrite weights via load_state_dict). attention_sharing='auto' triggers
    # shared attn at N>8 — replicates training topology.
    while engine.n_cells < target_n:
        ev = engine.force_split(parent_idx=0)
        if ev is None:
            break
    assert engine.n_cells == target_n, f"engine.n_cells={engine.n_cells} != target {target_n}"
    engine.load_state_dict(ckpt["model_state_dict"])
    engine.step_count = ckpt["step_count"]
    engine.split_threshold = ckpt["split_threshold"]
    engine._lorenz = ckpt["lorenz_state"]
    engine = engine.to(device)
    engine.eval()
    n_params = sum(p.numel() for p in engine.parameters())
    print(f"[LOAD] OK — n_cells={engine.n_cells} n_params={n_params:,}")
    return engine, ckpt


def collect_per_prompt_state(
    engine: MitosisModelEngine,
    probes: List[Dict],
    device: torch.device,
) -> Dict:
    """For each probe, run forward and capture:
       - raw tensions (pre-softmax, N,)
       - softmax weights (N,)
       - aggregated hidden state mean (D,)
    """
    max_seq = engine.cfg.max_seq
    raw_tens: List[List[float]] = []
    raw_weights: List[List[float]] = []
    agg_means: List[List[float]] = []
    cats: List[str] = []
    for p in probes:
        ids = text_to_bytes(p["prompt"], max_seq)
        if not ids:
            continue
        x = torch.tensor([ids], dtype=torch.long, device=device)
        with torch.no_grad():
            logits, info = engine(x)
        # Need raw tensions — info["tensions"] is the python list of scalars
        raw_tens.append([float(t) for t in info["tensions"]])
        raw_weights.append(info["weights"].detach().cpu().float().tolist())
        # aggregated hidden state — mean over token dim
        agg = info["aggregated"].detach().cpu().float().mean(dim=(0, 1)).tolist()
        agg_means.append(agg)
        cats.append(p["category"])
    return {
        "raw_tens": raw_tens,
        "raw_weights": raw_weights,
        "agg_means": agg_means,
        "categories": cats,
    }


# ─── Hypothesis (a) softmax entropy ───────────────────────────────────
def entropy(p: List[float]) -> float:
    s = 0.0
    for x in p:
        if x > 1e-12:
            s += -x * math.log(x)
    return s


def hypothesis_a(state: Dict) -> Dict:
    """Per-prompt softmax entropy + raw tension stats.

    Entropy interpretation (N=64 cells, log(64)=4.158):
      - entropy ≈ log(N) → near-uniform: every cell equal → KL=0 between categories
        (saturation = "uniform collapse", flat tensions)
      - entropy ≈ 0      → winner-take-all: one cell dominates → KL=0 across cats if
        same winner everywhere (saturation = "single-cell collapse")

    Both modes produce KL=0. We measure to distinguish.
    """
    weights = state["raw_weights"]
    tens = state["raw_tens"]
    ents = [entropy(w) for w in weights]
    # Tension scalar range per prompt
    tens_min = [min(t) for t in tens]
    tens_max = [max(t) for t in tens]
    tens_mean = [sum(t) / len(t) for t in tens]
    tens_spread = [mx - mn for mx, mn in zip(tens_max, tens_min)]
    # Tension std across prompts per cell (to see if tensions vary by prompt)
    n_prompts = len(tens)
    n_cells = len(tens[0]) if tens else 0
    per_cell_std = []
    for j in range(n_cells):
        col = [tens[i][j] for i in range(n_prompts)]
        m = sum(col) / len(col)
        v = sum((x - m) ** 2 for x in col) / len(col)
        per_cell_std.append(math.sqrt(v))
    log_n = math.log(n_cells) if n_cells > 0 else 0.0
    return {
        "n_cells": n_cells,
        "n_prompts": n_prompts,
        "log_n": log_n,
        "entropy_per_prompt_mean": sum(ents) / max(len(ents), 1),
        "entropy_per_prompt_min": min(ents) if ents else 0,
        "entropy_per_prompt_max": max(ents) if ents else 0,
        "entropy_ratio_to_uniform": (sum(ents) / max(len(ents), 1)) / max(log_n, 1e-9),
        "tension_spread_mean": sum(tens_spread) / max(len(tens_spread), 1),
        "tension_spread_min": min(tens_spread) if tens_spread else 0,
        "tension_spread_max": max(tens_spread) if tens_spread else 0,
        "tension_mean_across_prompts_min": min(tens_mean) if tens_mean else 0,
        "tension_mean_across_prompts_max": max(tens_mean) if tens_mean else 0,
        "per_cell_std_across_prompts_mean": sum(per_cell_std) / max(len(per_cell_std), 1),
        "per_cell_std_across_prompts_max": max(per_cell_std) if per_cell_std else 0,
        "interpretation": (
            "uniform_collapse" if (sum(ents) / max(len(ents), 1)) / max(log_n, 1e-9) > 0.95
            else ("single_cell_collapse" if (sum(ents) / max(len(ents), 1)) < 0.5
                  else "mixed_or_healthy")
        ),
    }


def _kl_pairs_from_dists(by_cat: Dict[str, List[List[float]]]) -> Tuple[float, int, Dict[str, List[float]]]:
    cat_names = sorted(by_cat.keys())
    avgs: Dict[str, List[float]] = {}
    for c in cat_names:
        rows = by_cat[c]
        if not rows:
            continue
        n = len(rows[0])
        agg = [0.0] * n
        for r in rows:
            for i in range(n):
                agg[i] += r[i]
        avgs[c] = [v / len(rows) for v in agg]
    pairs: List[float] = []
    for i, ci in enumerate(cat_names):
        for j, cj in enumerate(cat_names):
            if j <= i:
                continue
            p = avgs[ci]
            q = avgs[cj]
            kl = 0.0
            for k in range(len(p)):
                pi = p[k]
                qi = max(q[k], 1e-12)
                if pi > 1e-12:
                    kl += pi * math.log(pi / qi)
            pairs.append(kl)
    return (sum(pairs) / max(len(pairs), 1), len(pairs), avgs)


def hypothesis_a_temperature_sweep(state: Dict, temps: List[float]) -> Dict:
    """Re-apply softmax with different temperatures on the SAME raw tensions.
    If temperature scaling alone changes per-category distributions enough to
    produce KL ≥ 0.5, intervention (a) is $0 winnable.
    """
    raw_tens = state["raw_tens"]
    cats = state["categories"]
    results: Dict[str, Dict] = {}
    for T in temps:
        new_w: List[List[float]] = []
        for t in raw_tens:
            mx = max(t)
            exps = [math.exp((x - mx) / T) for x in t]
            s = sum(exps)
            new_w.append([e / s for e in exps])
        by_cat: Dict[str, List[List[float]]] = {}
        for w, c in zip(new_w, cats):
            by_cat.setdefault(c, []).append(w)
        mean_kl, n_pairs, _ = _kl_pairs_from_dists(by_cat)
        ents = [entropy(w) for w in new_w]
        results[f"T={T}"] = {
            "temperature": T,
            "mean_kl": mean_kl,
            "n_pairs": n_pairs,
            "kl_passes_threshold": mean_kl >= 0.5,
            "entropy_per_prompt_mean": sum(ents) / max(len(ents), 1),
        }
    return results


def hypothesis_a_mask_dominant_sweep(state: Dict, mask_top_k_list: List[int],
                                     temps: List[float]) -> Dict:
    """Mask top-K dominant cells (per prompt) and re-softmax the tail.
    Tests whether the non-dominant cells carry per-category information.
    """
    raw_tens = state["raw_tens"]
    cats = state["categories"]
    results: Dict[str, Dict] = {}
    n_cells = len(raw_tens[0]) if raw_tens else 0
    for K in mask_top_k_list:
        for T in temps:
            new_w: List[List[float]] = []
            for t in raw_tens:
                # Mask top-K (sort indices by tension desc, mask those)
                idx_sorted = sorted(range(len(t)), key=lambda i: -t[i])
                masked = list(t)
                for i in idx_sorted[:K]:
                    masked[i] = -1e9
                mx = max(masked)
                exps = [math.exp((x - mx) / T) if x > -1e8 else 0.0 for x in masked]
                s = sum(exps)
                new_w.append([e / max(s, 1e-30) for e in exps])
            by_cat: Dict[str, List[List[float]]] = {}
            for w, c in zip(new_w, cats):
                by_cat.setdefault(c, []).append(w)
            mean_kl, n_pairs, _ = _kl_pairs_from_dists(by_cat)
            ents = [entropy(w) for w in new_w]
            results[f"K={K}_T={T}"] = {
                "mask_top_k": K,
                "temperature": T,
                "mean_kl": mean_kl,
                "n_pairs": n_pairs,
                "kl_passes_threshold": mean_kl >= 0.5,
                "entropy_per_prompt_mean": sum(ents) / max(len(ents), 1),
            }
    return results


def hypothesis_a_zscore_sweep(state: Dict, temps: List[float]) -> Dict:
    """Per-cell z-score across the 50-prompt set, then softmax.
    Captures DEVIATIONS of each cell from its own baseline, which differ per
    category if the cells carry any category signal in their tension variations.
    """
    raw_tens = state["raw_tens"]
    cats = state["categories"]
    n_prompts = len(raw_tens)
    n_cells = len(raw_tens[0]) if n_prompts > 0 else 0
    # Per-cell mean/std across prompts
    means = [0.0] * n_cells
    stds = [0.0] * n_cells
    for j in range(n_cells):
        col = [raw_tens[i][j] for i in range(n_prompts)]
        m = sum(col) / len(col)
        v = sum((x - m) ** 2 for x in col) / len(col)
        means[j] = m
        stds[j] = math.sqrt(v) if v > 0 else 1.0
    # z-scored tensions per prompt
    z_tens = []
    for t in raw_tens:
        z_tens.append([(t[j] - means[j]) / stds[j] for j in range(n_cells)])

    results: Dict[str, Dict] = {}
    for T in temps:
        new_w: List[List[float]] = []
        for z in z_tens:
            mx = max(z)
            exps = [math.exp((x - mx) / T) for x in z]
            s = sum(exps)
            new_w.append([e / s for e in exps])
        by_cat: Dict[str, List[List[float]]] = {}
        for w, c in zip(new_w, cats):
            by_cat.setdefault(c, []).append(w)
        mean_kl, n_pairs, _ = _kl_pairs_from_dists(by_cat)
        ents = [entropy(w) for w in new_w]
        results[f"T={T}"] = {
            "temperature": T,
            "mean_kl": mean_kl,
            "n_pairs": n_pairs,
            "kl_passes_threshold": mean_kl >= 0.5,
            "entropy_per_prompt_mean": sum(ents) / max(len(ents), 1),
        }
    return results


def hypothesis_a_dominant_cell_audit(state: Dict) -> Dict:
    """Which cell wins on each prompt? Does the winner vary by category?
    If always same cell → static winner; if winner varies by category → category
    information IS in raw tensions, just buried by softmax saturation.
    """
    raw_tens = state["raw_tens"]
    cats = state["categories"]
    winners = []
    for t in raw_tens:
        winners.append(t.index(max(t)))
    # Winner frequency
    freq: Dict[int, int] = {}
    for w in winners:
        freq[w] = freq.get(w, 0) + 1
    # Per-category winner distribution
    by_cat: Dict[str, Dict[int, int]] = {}
    for w, c in zip(winners, cats):
        by_cat.setdefault(c, {})
        by_cat[c][w] = by_cat[c].get(w, 0) + 1
    # Runner-up audit
    runners: List[int] = []
    for t in raw_tens:
        idx_sorted = sorted(range(len(t)), key=lambda i: -t[i])
        runners.append(idx_sorted[1])
    runner_freq: Dict[int, int] = {}
    for r in runners:
        runner_freq[r] = runner_freq.get(r, 0) + 1
    by_cat_runner: Dict[str, Dict[int, int]] = {}
    for r, c in zip(runners, cats):
        by_cat_runner.setdefault(c, {})
        by_cat_runner[c][r] = by_cat_runner[c].get(r, 0) + 1
    return {
        "n_prompts": len(winners),
        "winners": winners,
        "unique_winners": sorted(freq.keys()),
        "winner_freq": freq,
        "winners_by_category": {c: dict(d) for c, d in by_cat.items()},
        "runners_up": runners,
        "unique_runners": sorted(runner_freq.keys()),
        "runner_freq": runner_freq,
        "runners_by_category": {c: dict(d) for c, d in by_cat_runner.items()},
    }


# ─── Hypothesis (b) gate_proj rank collapse ───────────────────────────
def hypothesis_b(engine: MitosisModelEngine) -> Dict:
    """SVD rank of stacked per-cell ffn_g first-linear weights.

    Each cell has ffn_g = nn.Sequential(Linear(D, FFN), GELU, Dropout, Linear(FFN, D)).
    We stack the FIRST Linear's weight (.weight is (FFN, D)) across cells → shape
    (N * FFN, D). Effective rank = #(singular values > rel_tol * max).

    Also stack flattened weight vectors across cells (N, FFN*D) and compute their
    rank — captures how many independent "cells" there are in ffn_g parameter space.
    """
    g_first_linears: List[torch.Tensor] = []
    a_first_linears: List[torch.Tensor] = []
    for c in engine.cells:
        # ffn_g[0] is the first Linear (D -> FFN); .weight shape (FFN, D)
        gw = c.ffn_g[0].weight.detach().cpu().float()
        aw = c.ffn_a[0].weight.detach().cpu().float()
        g_first_linears.append(gw)
        a_first_linears.append(aw)

    N = len(g_first_linears)
    FFN, D = g_first_linears[0].shape

    # (1) Per-cell SVD rank of ffn_g first linear (D-side singular values; max rank = min(D, FFN))
    per_cell_rank_g: List[int] = []
    per_cell_top_sv_g: List[float] = []
    per_cell_cond_g: List[float] = []
    for gw in g_first_linears:
        s = torch.linalg.svdvals(gw)
        smax = float(s[0].item())
        rel_tol = 1e-3
        rank = int((s > rel_tol * smax).sum().item())
        per_cell_rank_g.append(rank)
        per_cell_top_sv_g.append(smax)
        smin = float(s[-1].item()) if s.numel() else 0.0
        per_cell_cond_g.append(smax / max(smin, 1e-12))

    # (2) Cell-pool rank in ffn_g param space: stack flattened weights (N, FFN*D)
    flat_g = torch.stack([gw.flatten() for gw in g_first_linears])      # (N, FFN*D)
    flat_a = torch.stack([aw.flatten() for aw in a_first_linears])      # (N, FFN*D)
    sg = torch.linalg.svdvals(flat_g)
    sa = torch.linalg.svdvals(flat_a)
    rel = 1e-3
    pool_rank_g = int((sg > rel * sg[0].item()).sum().item())
    pool_rank_a = int((sa > rel * sa[0].item()).sum().item())

    # (3) Mean pairwise cosine dist between cells' ffn_g first linear (flattened)
    normed = flat_g / flat_g.norm(dim=1, keepdim=True).clamp(min=1e-8)
    cos_g = normed @ normed.t()
    mask = 1.0 - torch.eye(N)
    mean_cos_g = float(((cos_g) * mask).sum().item() / max(mask.sum().item(), 1))
    mean_dist_g = 1.0 - mean_cos_g

    normed_a = flat_a / flat_a.norm(dim=1, keepdim=True).clamp(min=1e-8)
    cos_a = normed_a @ normed_a.t()
    mean_cos_a = float(((cos_a) * mask).sum().item() / max(mask.sum().item(), 1))
    mean_dist_a = 1.0 - mean_cos_a

    return {
        "n_cells": N,
        "ffn_g_first_linear_shape": [FFN, D],
        "per_cell_rank_g_mean": sum(per_cell_rank_g) / max(N, 1),
        "per_cell_rank_g_min": min(per_cell_rank_g) if per_cell_rank_g else 0,
        "per_cell_rank_g_max": max(per_cell_rank_g) if per_cell_rank_g else 0,
        "per_cell_top_sv_g_mean": sum(per_cell_top_sv_g) / max(N, 1),
        "pool_rank_g": pool_rank_g,
        "pool_rank_a": pool_rank_a,
        "pool_max_rank": min(N, FFN * D),
        "mean_pairwise_dist_g": mean_dist_g,
        "mean_pairwise_dist_a": mean_dist_a,
        "g_singular_values_top10": sg[:10].tolist(),
        "a_singular_values_top10": sa[:10].tolist(),
        "interpretation": (
            "collapsed" if pool_rank_g < N * 0.5 else ("partial_collapse" if pool_rank_g < N * 0.9 else "diverse")
        ),
    }


# ─── Hypothesis (c) corpus / category mismatch — hidden state diversity by category ──
def hypothesis_c(state: Dict) -> Dict:
    """Per-category hidden state diversity.
    If category-level aggregated hidden state means cluster (within-category cohesion
    high, between-category separation high), then it's NOT corpus mismatch — the
    cells DO discriminate at hidden state level but softmax aggregation flattens.
    If clusters mix freely, corpus genuinely doesn't differentiate.
    """
    agg = state["agg_means"]
    cats = state["categories"]
    by_cat: Dict[str, List[torch.Tensor]] = {}
    for h, c in zip(agg, cats):
        by_cat.setdefault(c, []).append(torch.tensor(h))
    cat_names = sorted(by_cat.keys())

    # Per-category mean vector
    cat_means: Dict[str, torch.Tensor] = {}
    cat_within_mean_dist: Dict[str, float] = {}
    for c in cat_names:
        stack = torch.stack(by_cat[c])
        cat_means[c] = stack.mean(dim=0)
        # Within-category mean pairwise cos dist
        m = stack.shape[0]
        if m < 2:
            cat_within_mean_dist[c] = 0.0
            continue
        nd = stack / stack.norm(dim=1, keepdim=True).clamp(min=1e-8)
        cos = nd @ nd.t()
        mask = 1.0 - torch.eye(m)
        cat_within_mean_dist[c] = float(((1 - cos) * mask).sum().item() / max(mask.sum().item(), 1))

    # Between-category pairwise distances on category means
    nM = len(cat_names)
    means = torch.stack([cat_means[c] for c in cat_names])
    nd = means / means.norm(dim=1, keepdim=True).clamp(min=1e-8)
    cos = nd @ nd.t()
    pairs: List[float] = []
    for i in range(nM):
        for j in range(i + 1, nM):
            pairs.append(1.0 - float(cos[i, j].item()))
    between_mean_dist = sum(pairs) / max(len(pairs), 1)

    return {
        "categories": cat_names,
        "between_category_mean_pairwise_dist": between_mean_dist,
        "within_category_mean_pairwise_dist": cat_within_mean_dist,
        "within_avg": sum(cat_within_mean_dist.values()) / max(len(cat_within_mean_dist), 1),
        "ratio_between_within": between_mean_dist / max(
            sum(cat_within_mean_dist.values()) / max(len(cat_within_mean_dist), 1), 1e-9
        ),
        "interpretation": (
            "well_separated" if between_mean_dist > 0.1 and between_mean_dist > 1.5 * (sum(cat_within_mean_dist.values()) / max(len(cat_within_mean_dist), 1))
            else "mixed_corpus_mismatch"
        ),
    }


# ─── Hypothesis (d) cell pool diversity ───────────────────────────────
def hypothesis_d(engine: MitosisModelEngine) -> Dict:
    """Post-cotrain mean pairwise cosine distance between cell signatures.
    Pre-cotrain F-PERSONA-2: 0.994 (orthogonal). Post-cotrain expected: ?
    Two signature paths:
      (i) cell_state buffer (input-independent perturbation channel, used by _compute_iit_phi)
      (ii) per-cell ffn_g param vector (already captured in hypothesis_b)
    """
    states = torch.stack([c.cell_state.detach().cpu().float() for c in engine.cells])
    N = states.shape[0]
    nd = states / states.norm(dim=1, keepdim=True).clamp(min=1e-8)
    cos = nd @ nd.t()
    mask = 1.0 - torch.eye(N)
    mean_dist_cs = float(((1 - cos) * mask).sum().item() / max(mask.sum().item(), 1))

    # Norm distribution
    norms = states.norm(dim=1).tolist()

    return {
        "n_cells": N,
        "cell_state_dim": states.shape[1],
        "mean_pairwise_cos_dist_cell_state": mean_dist_cs,
        "cell_state_norm_mean": sum(norms) / max(len(norms), 1),
        "cell_state_norm_min": min(norms) if norms else 0,
        "cell_state_norm_max": max(norms) if norms else 0,
        "f_persona_2_pre_cotrain_reference": 0.994,
        "delta_vs_reference": mean_dist_cs - 0.994,
        "interpretation": (
            "diversity_collapsed" if mean_dist_cs < 0.5
            else ("diversity_degraded" if mean_dist_cs < 0.9 else "diversity_preserved")
        ),
    }


def main() -> int:
    # Mac local: prefer MPS for speed (PyTorch 2.8 supports it). CPU fallback fine for inference.
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    print(f"[INFO] device={device}")

    if not CKPT_PATH.exists():
        print(f"[ERROR] ckpt missing: {CKPT_PATH}")
        return 1
    if not IDENTITY_PROBE.exists():
        print(f"[ERROR] identity_probe missing: {IDENTITY_PROBE}")
        return 2

    t0 = time.time()
    engine, ckpt = load_engine(device)
    print(f"[TIMING] load {time.time()-t0:.2f}s")

    # Load probes
    probes: List[Dict] = []
    with open(IDENTITY_PROBE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            probes.append(json.loads(line))
    print(f"[INFO] {len(probes)} probes loaded")

    # Collect per-prompt state
    t0 = time.time()
    try:
        state = collect_per_prompt_state(engine, probes, device)
    except Exception as e:
        # MPS sometimes fails on certain ops — fallback CPU
        print(f"[WARN] {device} forward failed: {e} — fallback CPU")
        engine = engine.to("cpu")
        device = torch.device("cpu")
        state = collect_per_prompt_state(engine, probes, device)
    print(f"[TIMING] forward {time.time()-t0:.2f}s for {len(state['raw_tens'])} probes")

    # Hypotheses
    print("[H-a] softmax entropy / temperature collapse")
    ha = hypothesis_a(state)
    print(f"     mean_entropy={ha['entropy_per_prompt_mean']:.4f} log(N)={ha['log_n']:.4f} "
          f"ratio={ha['entropy_ratio_to_uniform']:.4f} -> {ha['interpretation']}")
    print(f"     tension_spread mean={ha['tension_spread_mean']:.6f} "
          f"per_cell_std mean={ha['per_cell_std_across_prompts_mean']:.6f}")

    print("[H-a*] temperature sweep")
    ha_sweep = hypothesis_a_temperature_sweep(state, temps=[1.0, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 2.0, 5.0, 50.0, 500.0])
    for k, v in ha_sweep.items():
        print(f"       {k}: KL={v['mean_kl']:.6f} entropy={v['entropy_per_prompt_mean']:.4f} "
              f"pass={v['kl_passes_threshold']}")

    print("[H-a**] dominant cell audit — who wins, varies by category?")
    ha_dom = hypothesis_a_dominant_cell_audit(state)
    print(f"       unique winners={ha_dom['unique_winners']} freq={ha_dom['winner_freq']}")
    print(f"       unique runners-up={ha_dom['unique_runners']} freq={ha_dom['runner_freq']}")
    print(f"       winners_by_cat={ha_dom['winners_by_category']}")

    print("[H-a***] mask-top-K + temperature sweep (look in the tail for category signal)")
    ha_mask = hypothesis_a_mask_dominant_sweep(state, mask_top_k_list=[1, 2, 3, 5], temps=[1.0, 0.5, 0.1])
    for k, v in ha_mask.items():
        print(f"       {k}: KL={v['mean_kl']:.6f} entropy={v['entropy_per_prompt_mean']:.4f} "
              f"pass={v['kl_passes_threshold']}")

    print("[H-a****] z-score (per-cell across prompts) + softmax sweep")
    ha_z = hypothesis_a_zscore_sweep(state, temps=[1.0, 0.5, 0.2, 2.0])
    for k, v in ha_z.items():
        print(f"       {k}: KL={v['mean_kl']:.6f} entropy={v['entropy_per_prompt_mean']:.4f} "
              f"pass={v['kl_passes_threshold']}")

    print("[H-b] gate_proj rank")
    hb = hypothesis_b(engine)
    print(f"     per_cell_rank_g mean={hb['per_cell_rank_g_mean']:.2f} pool_rank_g={hb['pool_rank_g']}/{hb['n_cells']} "
          f"pool_rank_a={hb['pool_rank_a']}/{hb['n_cells']} -> {hb['interpretation']}")
    print(f"     mean_pairwise_dist g={hb['mean_pairwise_dist_g']:.6f} a={hb['mean_pairwise_dist_a']:.6f}")

    print("[H-c] corpus / category separation")
    hc = hypothesis_c(state)
    print(f"     between_cat={hc['between_category_mean_pairwise_dist']:.6f} "
          f"within_avg={hc['within_avg']:.6f} ratio={hc['ratio_between_within']:.4f} -> {hc['interpretation']}")

    print("[H-d] cell pool diversity (cell_state buffer)")
    hd = hypothesis_d(engine)
    print(f"     mean_pairwise_cos_dist={hd['mean_pairwise_cos_dist_cell_state']:.6f} "
          f"(pre-ref 0.994) -> {hd['interpretation']}")

    # ─── Verdict synthesis ───────────────────────────────────────────
    # Primary root cause logic:
    #   (1) if temperature sweep finds T > 0 producing KL >= 0.5 → (a) is winnable cheaply
    #   (2) elif tension_spread_mean ≈ 0 → tensions are degenerate (b or d more likely)
    #   (3) elif within_avg vs between_cat shows mixed-cat hidden states → (c) corpus
    sweep_pass_temps = [v["temperature"] for v in ha_sweep.values() if v["kl_passes_threshold"]]
    mask_passes = [k for k, v in ha_mask.items() if v["kl_passes_threshold"]]
    z_passes = [k for k, v in ha_z.items() if v["kl_passes_threshold"]]

    if sweep_pass_temps:
        primary = "a_softmax_temperature"
        intervention = (
            f"INTERVENTION (a): apply softmax temperature scaling. Temperatures producing KL >= 0.5: "
            f"{sweep_pass_temps}. $0 inference-only re-measure. Add `temperature` knob to "
            f"MitosisModelEngine.forward."
        )
    elif mask_passes:
        primary = "a_mask_dominant_temperature"
        intervention = (
            f"INTERVENTION (a-mask): mask top-K dominant cell(s) + temperature recovers KL. "
            f"Passing configs: {mask_passes}. $0 inference-only. Indicates category info IS "
            f"in tail cells but cell-0 monopoly hides it."
        )
    elif z_passes:
        primary = "a_zscore_softmax"
        intervention = (
            f"INTERVENTION (a-zscore): per-cell z-score across prompt set + softmax recovers KL. "
            f"Passing configs: {z_passes}. $0 inference-only metric redefinition (F-PERSONA-4 §A2 spec)."
        )
    elif ha["tension_spread_mean"] < 1e-4 and ha["per_cell_std_across_prompts_mean"] < 1e-4:
        # Tensions collapsed to degenerate scalars per cell — they don't even vary with prompt.
        # Almost certainly gate_proj collapse (b) or cell-state collapse (d).
        if hb["interpretation"] == "collapsed":
            primary = "b_gate_proj_rank_collapse"
            intervention = (
                "INTERVENTION (b): gate_proj rank collapse — short retraining with diversity "
                "regularizer (orthogonality penalty across cells' ffn_g first linear flattened) "
                "+ noise re-injection. ~$5-10 H100 1K steps."
            )
        elif hd["interpretation"] == "diversity_collapsed":
            primary = "d_cell_state_collapse"
            intervention = (
                "INTERVENTION (d): cell pool cell_state buffer collapsed — re-cotrain with "
                "explicit cell-state orthogonality penalty + lorenz_calibration_factor up. "
                "$30-50 H100 full restart."
            )
        else:
            primary = "tension_degeneracy_unattributed"
            intervention = (
                "INTERVENTION (b+c hybrid): tensions degenerate but cell weights still diverse — "
                "the readout (a-g) mean collapsed across all prompts. Retry with multi-corpus "
                "(category-balanced) cotrain + temperature in softmax. $10-20 H100 1-2K steps."
            )
    elif hc["interpretation"] == "mixed_corpus_mismatch":
        primary = "c_corpus_category_mismatch"
        intervention = (
            "INTERVENTION (c): corpus does not differentiate categories — synthesize 5-category "
            "balanced corpus and short follow-up cotrain. ~$10-20 H100 1-2K steps + corpus gen 1-2 hr."
        )
    else:
        primary = "compound_or_unknown"
        intervention = (
            "INTERVENTION: ambiguous — try (a) temperature first ($0), then (c) corpus rebalance, "
            "then (b) gate_proj noise. Falsifier order: a → c → b → d."
        )

    out = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ckpt_path": str(CKPT_PATH),
        "n_cells": engine.n_cells,
        "hypothesis_a_softmax_entropy": ha,
        "hypothesis_a_temperature_sweep": ha_sweep,
        "hypothesis_a_dominant_cell_audit": ha_dom,
        "hypothesis_a_mask_dominant_sweep": ha_mask,
        "hypothesis_a_zscore_sweep": ha_z,
        "hypothesis_b_gate_proj_rank": hb,
        "hypothesis_c_corpus_diversity": hc,
        "hypothesis_d_cell_diversity": hd,
        "primary_root_cause": primary,
        "intervention_recommendation": intervention,
        # NB: raw tensors elided to keep JSON tractable; available via re-run if needed.
        "raw_summary": {
            "n_prompts": len(state["raw_tens"]),
            "first_prompt_tens": state["raw_tens"][0] if state["raw_tens"] else [],
            "first_prompt_weights": state["raw_weights"][0] if state["raw_weights"] else [],
        },
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, default=str))
    print(f"\n[RESULT] {OUT_JSON}")
    print(f"[VERDICT] primary={primary}")
    print(f"[REC] {intervention}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
