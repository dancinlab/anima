"""train_v5mitosis_cotrain_v3_gumbel.py — (k) GUMBEL-SOFTMAX VARIANT PSCC §54.

Direct fork of train_v5mitosis_cotrain_v3_routing.py with ONE architectural delta:
- TopKMoERouter.forward replaces deterministic softmax with Gumbel-softmax
  (stochastic gate). tau=1.0 fixed (could be annealed). Top-K hard mask retained.
- Stochastic null distribution may differ from hard top-K — tests if A2-trap
  pattern (mean z=1.48 with v3-routing) breaks via gate stochasticity.

Roadmap path (k) per PERSONA.md §7. Expected $5-30 H100 single-seed.

Original docstring follows:
---
train_v5mitosis_cotrain_v3_routing.py — Phase 3 follow-up: ARCHITECTURAL ROUTING FIX.

PURPOSE
    v3-routing = v2 cotrain (entropy-reg + balanced corpus) + ARCHITECTURAL change to
    the cell-pool routing layer to break the winner-take-all softmax collapse that has
    blocked F-PERSONA-4a (routing variant) across cotrain v1 (PSCC §44), v2 (§45-FINAL),
    per-cat SMALL (§48), softmax-T sweep (§47).

ROOT CAUSE (PSCC §44-49 carry)
    Original `MitosisModelEngine.forward` computes:
        tens    = stack([cell(x).tension.mean() for cell in cells])  # (N,) scalar/cell
        weights = softmax(tens, dim=0)                                # (N,)  ONE vector / fwd
        aggregated = Σ_i weights_i * cell_out_i
    Problems:
      (1) No learnable router → routing cannot depend on the INPUT (prompt/category),
          so by construction every probe gets ≈ the same weights → KL between
          category-mean weight distributions ≈ 0.
      (2) Plain softmax over scalar tensions saturates (one cell ~793× tension
          dominance, PSCC §47) → wmax → 1.0 → entropy → 0 even with λ=0.1 reg.

THE FIX (path g, recommended g2+g3)
    Add a small LEARNABLE router on top of a pooled per-input representation, then:
      (g2) HARD TOP-K MoE GATING — top-K=4 cells active per input, rest masked,
           survivors renormalized → forces ≥ K cells to carry gradient, breaks
           winner-take-all (Switch/Mixtral pattern).
      (g3) LOAD-BALANCING AUX LOSS — Switch Transformer style:
           aux = α · N · Σ_i (fraction routed to cell i) · (mean gate prob to cell i)
           pushes the router to distribute load across cells (prevents the router
           from just learning a constant top-K monopoly).
      (g4 optional) ANNEALED entropy reg on the gate distribution as a secondary
           pressure (λ_init high → λ_final low, cosine).
    The router is the ONLY new module; the cell internals + mitosis loop are untouched
    (mitosis_model_v5.py body is NOT modified — fix is installed via a forward monkey-
    patch like v2's `_install_live_weights_hook`).

    The pooled representation is the mean (over batch & sequence) of the cells' shared
    INPUT embedding x = tok_emb + pos_emb — this is input-dependent (so different probes
    → different routing) and does not require touching cell forwards.  Router gates are
    computed PER-INPUT (one weight vector per forward call), which matches the F-PERSONA-4
    measurement protocol (per-prompt weight vector, category-mean KL).

    On a SPLIT the cell count N grows; the router output dim must grow with it. We
    register the router as a fresh Linear(d_router_in, max_cells) sized to cfg.max_cells
    up front and slice [:n_cells] each forward (extra rows stay near-zero-init, get
    gradient only once that cell exists). This keeps the router shape stable across
    mitosis events (no optimizer surgery needed).

USAGE (H100)
    python3 train_v5mitosis_cotrain_v3_routing.py \
        --corpus corpus/corpus_persona_balanced.txt \
        --output-dir output \
        --steps 8000 --batch 32 --ctx 256 --lr 1e-4 --warmup 500 \
        --d-model 384 --n-head 6 --ffn-dim 1536 --initial-cells 2 --max-cells 64 \
        --top-k 4 --aux-alpha 0.01 \
        --lambda-init 1.0 --lambda-final 0.01 --lambda-schedule cosine \
        --identity-probe probe/identity_probe.jsonl --n-perms 100

HONEST C3 (≥ 5)
    1. The router sees only a POOLED (batch×seq mean) embedding — coarse signal; if
       category distinctions live in token-position structure, this pooling discards it.
    2. d_router_in = d_model; no nonlinearity beyond the single Linear → router is a
       linear probe of the mean embedding. A 2-layer MLP router might separate
       categories better but adds params + risk; deliberately kept minimal.
    3. top-K=4 with N≤64 cells leaves 60 cells unrouted per input → those cells get
       gradient only via load-balancing aux + the (rare) inputs that route to them;
       slow specialization. K too small ⇒ monopoly among the K; K too large ⇒ back to
       soft-everything. K=4 is the Switch/Mixtral default, not tuned here.
    4. Mitosis still runs on the ORIGINAL scalar-tension signal (cell.tension.mean),
       NOT the router gates — split/merge dynamics are unchanged from v1/v2, so the
       routing fix and the mitosis dynamics are decoupled (intentional: don't perturb
       the F-V5MIT-1..5 regression surface).
    5. aux-alpha=0.01 is the Switch default; if the router still collapses (all inputs
       → same top-K), bump α to 0.05-0.1. If CE never converges, the aux is too strong.
    6. The router is randomly initialized and untrained for the first ~warmup steps
       while LR ramps; early routing is noise. n_perms=100 null test guards against a
       spurious "category-dependent" verdict from that noise.
    7. F-PERSONA-4b (M4 aggregated hidden cosine z) is RE-MEASURED here as a regression
       check (v2 carried z=3.20); the routing change re-weights `aggregated`, so 4b
       could move in either direction. Reported honestly.

ENVELOPE
    d=384 cells 2→64 8K step batch=32 ctx=256 ≈ same as v1/v2 (~33-50 min H100, $1-2).
    No scale caps — d/cells/steps can be bumped via flags (memory feedback_no_scale_caps).
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


# ─── Path bootstrap ──────────────────────────────────────────────────
def _bootstrap_path():
    here = Path(__file__).resolve().parent
    candidates = [
        Path("/workspace/anima/training"),
        here / "../training",
        here.parent / "training",
        Path("/Users/ghost/core/anima/training"),
        Path("/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_2026_05_12"),
        here,
    ]
    for c in candidates:
        if (c / "mitosis_model_v5.py").exists():
            sys.path.insert(0, str(c.resolve()))
            return
    raise RuntimeError("mitosis_model_v5.py not found in any search path")


_bootstrap_path()
from mitosis_model_v5 import MitosisModelConfig, MitosisModelEngine  # noqa: E402


# ─── Tokenizer / corpus / cost guard (self-contained; same shape as v2) ──
def text_to_bytes(text: str) -> List[int]:
    return list(text.encode("utf-8"))


def load_corpus_bytes(path: str) -> torch.Tensor:
    with open(path, "rb") as f:
        raw = f.read()
    return torch.tensor(list(raw), dtype=torch.long)


def sample_batch(corpus: torch.Tensor, batch_size: int, ctx: int, device: torch.device):
    N = corpus.size(0)
    if N <= ctx + 1:
        raise ValueError(f"corpus too small: N={N}, need > ctx+1={ctx + 1}")
    idx = torch.randint(0, N - ctx - 1, (batch_size,))
    rows = torch.stack([corpus[i: i + ctx + 1] for i in idx.tolist()])
    return rows[:, :ctx].to(device), rows[:, 1: ctx + 1].to(device)


class CostGuard:
    def __init__(self, cap_usd: float, per_hr: float):
        self.cap_usd = cap_usd
        self.per_hr = per_hr
        self.t0 = time.time()

    def elapsed_hr(self) -> float:
        return (time.time() - self.t0) / 3600.0

    def current_usd(self) -> float:
        return self.elapsed_hr() * self.per_hr

    def over(self) -> bool:
        return self.current_usd() >= self.cap_usd


# ─── Routing fix: learnable top-K MoE router installed via forward patch ──
class TopKMoERouter(nn.Module):
    """Learnable per-input router → top-K hard gating over the cell pool.

    Sized to `max_cells` up front; sliced to `n_cells` each forward.

    forward(x_emb, n_cells, top_k) → (weights (n_cells,), gate_full (n_cells,),
                                      dispatch_frac (n_cells,))
        weights:       hard top-K renormalized gate over ACTIVE cells (sums to 1)
        gate_full:     full softmax gate over ACTIVE cells (for aux loss / entropy)
        dispatch_frac: indicator over ACTIVE cells (1.0 for cells in top-K else 0.0)
    Per-input (batch & seq are mean-pooled before the router).
    """

    def __init__(self, d_in: int, max_cells: int):
        super().__init__()
        self.d_in = d_in
        self.max_cells = max_cells
        self.proj = nn.Linear(d_in, max_cells)
        # Small init so early routing is gentle (not a hard random monopoly).
        nn.init.normal_(self.proj.weight, std=0.02)
        nn.init.zeros_(self.proj.bias)

    def forward(self, x_emb: torch.Tensor, n_cells: int, top_k: int):
        # x_emb: (B, T, D) — the shared cell-input embedding (tok+pos)
        pooled = x_emb.mean(dim=(0, 1))                       # (D,)
        logits_full = self.proj(pooled)                      # (max_cells,)
        logits = logits_full[:n_cells]                       # (N,)
        # PSCC §54 (k) GUMBEL VARIANT: replace deterministic softmax with
        # stochastic Gumbel-softmax. tau=1.0 fixed. Stochastic gate may
        # produce different null distribution shape than hard top-K.
        if self.training:
            gate_full = F.gumbel_softmax(logits, tau=1.0, hard=False, dim=0)
        else:
            # Eval: deterministic softmax for reproducible measurement
            gate_full = F.softmax(logits, dim=0)
        k = min(top_k, n_cells)
        topv, topi = torch.topk(gate_full, k=k)              # (k,)
        mask = torch.zeros_like(gate_full)
        mask = mask.scatter(0, topi, 1.0)                    # (N,) hard indicator
        # Renormalize the surviving (top-K) gate probs → straight-through-ish weights.
        masked = gate_full * mask
        weights = masked / masked.sum().clamp(min=1e-12)     # (N,) sums to 1 over top-K
        return weights, gate_full, mask


def install_routing_fix(engine: MitosisModelEngine, top_k: int) -> TopKMoERouter:
    """Monkey-patch engine.forward to route via a learnable top-K MoE router.

    Mirrors v2's `_install_live_weights_hook` but REPLACES the routing math.
    Returns the router module so the trainer can add it to the optimizer.
    """
    device = next(engine.parameters()).device
    router = TopKMoERouter(d_in=engine.cfg.d_model, max_cells=engine.cfg.max_cells).to(device)
    # Keep a handle WITHOUT registering as an nn.Module submodule of engine (avoids
    # duplicate params in the optimizer when we add router.parameters() separately).
    object.__setattr__(engine, "_topk_router", router)

    def patched_forward(input_ids, readout_mode=None):
        if readout_mode is None:
            readout_mode = engine.cfg.readout_mode
        B, T = input_ids.shape
        assert T <= engine.max_seq
        pos = torch.arange(T, device=input_ids.device)
        x = engine.tok_emb(input_ids) + engine.pos_emb(pos).unsqueeze(0)   # (B,T,D)

        cell_outs: List[torch.Tensor] = []
        cell_tensions: List[torch.Tensor] = []
        for cell in engine.cells:
            out_i, tension_tok = cell(x, readout_mode=readout_mode)
            cell_outs.append(out_i)
            cell_tensions.append(tension_tok.mean())

        n = engine.n_cells
        weights, gate_full, dispatch_mask = router(x, n, top_k)             # (N,) each
        stacked = torch.stack(cell_outs, dim=0)                            # (N,B,T,D)
        aggregated = (weights.view(-1, 1, 1, 1) * stacked).sum(dim=0)      # (B,T,D)
        h = engine.final_ln(aggregated)
        logits = engine.lm_head(h)

        info = {
            "tensions": [t.item() for t in cell_tensions],     # mitosis still uses these
            "aggregated": aggregated,
            "weights": weights.detach(),                       # top-K renormalized
            "weights_live": weights,                           # graph-attached
            "gate_full_live": gate_full,                       # full softmax gate (live)
            "dispatch_mask": dispatch_mask,                    # (N,) top-K indicator
            "n_cells": n,
        }
        return logits, info

    engine.forward = patched_forward
    return router


def load_balance_aux(gate_full: torch.Tensor, dispatch_mask: torch.Tensor, n_cells: int) -> torch.Tensor:
    """Switch Transformer load-balancing aux (per-input variant).

    aux = N · Σ_i f_i · P_i
      f_i = fraction of "tokens" (here: this single pooled input) dispatched to cell i
            → for a single input, f_i = dispatch_mask_i / sum(mask)
      P_i = router prob mass to cell i (gate_full_i)
    Minimized when load (f) and confidence (P) are spread uniformly across cells.
    """
    denom = dispatch_mask.sum().clamp(min=1e-12)
    f = dispatch_mask / denom                          # (N,)
    return n_cells * (f * gate_full).sum()


# ─── F-PERSONA-4a routing measurement (per-prompt weights → category-mean KL) ──
def f_persona_4a_routing(engine, identity_probe_path, device, n_perms: int = 100,
                         seed: int = 42) -> Dict:
    probes = []
    with open(identity_probe_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                probes.append(json.loads(line))

    max_seq = engine.cfg.max_seq
    weights_per_prompt: List[List[float]] = []
    gate_full_per_prompt: List[List[float]] = []
    cats: List[str] = []
    engine.eval()
    for p in probes:
        ids = text_to_bytes(p["prompt"])[:max_seq]
        if not ids:
            continue
        x = torch.tensor([ids], dtype=torch.long, device=device)
        with torch.no_grad():
            _, info = engine(x)
        weights_per_prompt.append([float(v) for v in info["weights"].detach().cpu().float().tolist()])
        gf = info.get("gate_full_live")
        if gf is not None:
            gate_full_per_prompt.append([float(v) for v in gf.detach().cpu().float().tolist()])
        cats.append(p["category"])

    def _pad(rows):
        m = max(len(r) for r in rows)
        return [r + [0.0] * (m - len(r)) for r in rows]

    weights_per_prompt = _pad(weights_per_prompt)
    if gate_full_per_prompt:
        gate_full_per_prompt = _pad(gate_full_per_prompt)

    def cat_mean(rows, labels):
        by = {}
        for r, c in zip(rows, labels):
            by.setdefault(c, []).append(r)
        out = {}
        for c, rr in by.items():
            n = len(rr[0])
            agg = [0.0] * n
            for r in rr:
                for i in range(n):
                    agg[i] += r[i]
            out[c] = [v / len(rr) for v in agg]
        return out

    def mean_pairwise_kl(rows, labels):
        avgs = cat_mean(rows, labels)
        names = sorted(avgs.keys())
        kls = []
        for i, ci in enumerate(names):
            for j, cj in enumerate(names):
                if j <= i:
                    continue
                p, q = avgs[ci], avgs[cj]
                kl = 0.0
                for k in range(len(p)):
                    pi = p[k]
                    qi = max(q[k], 1e-12)
                    if pi > 1e-12:
                        kl += pi * math.log(pi / qi)
                kls.append(kl)
        return sum(kls) / max(len(kls), 1)

    def null_z(rows, labels):
        true_kl = mean_pairwise_kl(rows, labels)
        rng = random.Random(seed)
        nulls = []
        for _ in range(n_perms):
            sh = list(labels)
            rng.shuffle(sh)
            nulls.append(mean_pairwise_kl(rows, sh))
        nm = sum(nulls) / len(nulls)
        nv = sum((x - nm) ** 2 for x in nulls) / len(nulls)
        ns = math.sqrt(nv) if nv > 0 else 0.0
        z = (true_kl - nm) / ns if ns > 0 else float("inf")
        n_ge = sum(1 for x in nulls if x >= true_kl)
        p_val = n_ge / len(nulls)
        return {
            "mean_kl": true_kl, "null_mean": nm, "null_std": ns,
            "z_score_vs_null": z, "p_value_one_sided": p_val,
            "passes_null_test": (z > 3.0 or p_val < 0.01),
        }

    r_weights = null_z(weights_per_prompt, cats)
    r_gate = null_z(gate_full_per_prompt, cats) if gate_full_per_prompt else None

    cat_names = sorted(set(cats))
    primary = r_weights
    verdict = (
        "PASS" if (primary["mean_kl"] >= 0.5 and primary["passes_null_test"])
        else ("KL_PASS_NULL_FAIL" if primary["mean_kl"] >= 0.5 else "FAIL")
    )
    return {
        "metric": "F-PERSONA-4a routing (top-K MoE weights, per-prompt → category-mean pairwise KL)",
        "verdict": verdict,
        "threshold_kl": 0.5, "threshold_z": 3.0,
        "topk_weights": r_weights,
        "soft_gate": r_gate,
        "n_perms": n_perms,
        "categories": cat_names,
        "n_probes": len(weights_per_prompt),
        "cat_mean_topk_weights": cat_mean(weights_per_prompt, cats),
    }


# ─── F-PERSONA-4b regression: M4 aggregated hidden cosine z (vs null) ──
def f_persona_4b_content(engine, identity_probe_path, device, n_perms: int = 100,
                         seed: int = 45) -> Dict:
    probes = []
    with open(identity_probe_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                probes.append(json.loads(line))
    max_seq = engine.cfg.max_seq
    aggs: List[List[float]] = []
    cats: List[str] = []
    engine.eval()
    for p in probes:
        ids = text_to_bytes(p["prompt"])[:max_seq]
        if not ids:
            continue
        x = torch.tensor([ids], dtype=torch.long, device=device)
        with torch.no_grad():
            _, info = engine(x)
        aggs.append(info["aggregated"].detach().cpu().float().mean(dim=(0, 1)).tolist())
        cats.append(p["category"])

    def cos_dist(a, b):
        import math as _m
        dot = sum(x * y for x, y in zip(a, b))
        na = _m.sqrt(sum(x * x for x in a))
        nb = _m.sqrt(sum(x * x for x in b))
        if na == 0 or nb == 0:
            return 1.0
        return 1.0 - dot / (na * nb)

    def cat_mean(rows, labels):
        by = {}
        for r, c in zip(rows, labels):
            by.setdefault(c, []).append(r)
        out = {}
        for c, rr in by.items():
            n = len(rr[0])
            agg = [0.0] * n
            for r in rr:
                for i in range(n):
                    agg[i] += r[i]
            out[c] = [v / len(rr) for v in agg]
        return out

    def mean_pairwise(rows, labels):
        avgs = cat_mean(rows, labels)
        names = sorted(avgs.keys())
        ds = []
        for i, ci in enumerate(names):
            for j, cj in enumerate(names):
                if j <= i:
                    continue
                ds.append(cos_dist(avgs[ci], avgs[cj]))
        return sum(ds) / max(len(ds), 1)

    true_d = mean_pairwise(aggs, cats)
    rng = random.Random(seed)
    nulls = []
    for _ in range(n_perms):
        sh = list(cats)
        rng.shuffle(sh)
        nulls.append(mean_pairwise(aggs, sh))
    nm = sum(nulls) / len(nulls)
    nv = sum((x - nm) ** 2 for x in nulls) / len(nulls)
    ns = math.sqrt(nv) if nv > 0 else 0.0
    z = (true_d - nm) / ns if ns > 0 else float("inf")
    n_ge = sum(1 for x in nulls if x >= true_d)
    p_val = n_ge / len(nulls)
    return {
        "metric": "F-PERSONA-4b content (M4 aggregated hidden cosine, category-mean pairwise → null)",
        "true": true_d, "null_mean": nm, "null_std": ns,
        "z_score_vs_null": z, "p_value_one_sided": p_val,
        "passes_null_test": (z > 3.0 or p_val < 0.01),
        "verdict": "PASS" if (z > 3.0 or p_val < 0.01) else "FAIL",
        "n_perms": n_perms,
        "v2_carry_z": 3.2036695590259,
    }


# ─── F-V5MIT-1..5 lightweight regression checks ──────────────────────
def f_v5mit_regression(engine, splits_in_run: int, ce_final: float) -> Dict:
    """Cheap structural checks mirroring the v1/v2 F-V5MIT-1..5 surface.

    F-V5MIT-1: cells grew via split (mitosis active)              → n_cells > initial
    F-V5MIT-2: no merge cascade collapse                          → n_cells >= min_cells
    F-V5MIT-3: Φ ratchet held (best ≥ last-best, monotone non-dec)→ phi_best >= ~phi
    F-V5MIT-4: CE converged (not diverged)                        → ce_final < 5.0
    F-V5MIT-5: V14-STRICT proxy — split count > 0 AND <= max_cells (no runaway)
    """
    n = engine.n_cells
    phi = float(engine.phi)
    phi_best = float(engine._phi_best)
    checks = {
        "F-V5MIT-1_mitosis_active": {"pass": n > engine.cfg.initial_cells, "n_cells": n, "initial": engine.cfg.initial_cells},
        "F-V5MIT-2_no_collapse": {"pass": n >= engine.cfg.min_cells, "n_cells": n, "min": engine.cfg.min_cells},
        "F-V5MIT-3_phi_ratchet": {"pass": phi_best + 1e-6 >= phi, "phi": phi, "phi_best": phi_best},
        "F-V5MIT-4_ce_converged": {"pass": ce_final < 5.0, "ce_final": ce_final},
        "F-V5MIT-5_v14strict_proxy": {"pass": 0 < splits_in_run <= engine.cfg.max_cells, "splits": splits_in_run, "max_cells": engine.cfg.max_cells},
    }
    n_pass = sum(1 for v in checks.values() if v["pass"])
    return {"checks": checks, "n_pass": n_pass, "n_total": 5, "verdict": f"{n_pass}/5"}


# ─── Schedules ───────────────────────────────────────────────────────
def lambda_at(step, total, warmup, lam_init, lam_final, schedule="cosine"):
    if schedule == "constant":
        return lam_init
    if step < warmup:
        return lam_init
    progress = min(max((step - warmup) / max(total - warmup, 1), 0.0), 1.0)
    if schedule == "linear":
        return lam_init + (lam_final - lam_init) * progress
    if schedule == "cosine":
        return lam_final + 0.5 * (lam_init - lam_final) * (1.0 + math.cos(math.pi * progress))
    raise ValueError(schedule)


def save_ckpt(engine, router, cfg, path, step, top_k):
    ckpt = {
        "model_state_dict": engine.state_dict(),
        "router_state_dict": router.state_dict(),
        "router_top_k": top_k,
        "config": asdict(cfg),
        "n_cells": engine.n_cells,
        "step_count": engine.step_count,
        "phi": float(engine.phi),
        "phi_best": float(engine._phi_best),
        "split_threshold": float(engine.split_threshold),
        "cell_metadata": [
            {"cell_id": c.cell_id, "creation_step": c.creation_step,
             "parent_id": c.parent_id, "process_count": c.process_count}
            for c in engine.cells
        ],
        "lorenz_state": list(engine._lorenz),
        "saved_step": step,
        "saved_ts": time.time(),
        "trainer": "v3-routing (top-K MoE + load-balance aux)",
    }
    torch.save(ckpt, path)


# ─── Trainer ─────────────────────────────────────────────────────────
def cotrain(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] device={device} torch={torch.__version__} cuda={torch.cuda.is_available()}")
    if device.type == "cuda":
        print(f"[INFO] gpu={torch.cuda.get_device_name(0)}")
    torch.manual_seed(args.seed)
    random.seed(args.seed)

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    cost_guard = CostGuard(args.cost_cap_usd, args.cost_per_hr)
    if args.estimated_wall_hr * args.cost_per_hr > args.cost_cap_usd * 1.10:
        print("[ABORT] est cost > cap +10%")
        return 2

    cfg = MitosisModelConfig(
        vocab_size=256, d_model=args.d_model, n_head=args.n_head, ffn_dim=args.ffn_dim,
        max_seq=args.ctx, initial_cells=args.initial_cells, max_cells=args.max_cells,
        min_cells=2, split_patience=3, merge_threshold=0.005, merge_patience=30,
        noise_scale=0.10, lorenz_scale=0.05, adaptive_window=100,
        readout_mode=args.readout_mode, attention_sharing="auto",
        weight_tied_lm_head=True, dropout=0.0,
    )
    print(f"[INFO] cfg = {asdict(cfg)}")
    engine = MitosisModelEngine(cfg).to(device)
    router = install_routing_fix(engine, top_k=args.top_k)
    n_params = sum(p.numel() for p in engine.parameters()) + sum(p.numel() for p in router.parameters())
    print(f"[INFO] n_params(engine+router)={n_params:,}  router_out_dim={cfg.max_cells} top_k={args.top_k}")

    corpus = load_corpus_bytes(args.corpus)
    print(f"[INFO] corpus={args.corpus} bytes={corpus.numel():,}")

    optimizer = torch.optim.AdamW(
        list(engine.parameters()) + list(router.parameters()),
        lr=args.lr, betas=(0.9, 0.95), weight_decay=0.0)

    def lr_at(step):
        if step < args.warmup:
            return args.lr * (step + 1) / max(args.warmup, 1)
        progress = (step - args.warmup) / max(args.steps - args.warmup, 1)
        return args.lr * 0.5 * (1.0 + math.cos(math.pi * progress))

    hist = {k: [] for k in ("loss", "ce", "aux", "ent_gate", "wmax", "lambda", "cells",
                            "n_active_gt01", "gate_max")}
    splits_in_run = 0
    t_start = time.time()
    cost_aborted = False
    print(f"[INFO] top_k={args.top_k} aux_alpha={args.aux_alpha} "
          f"λ_init={args.lambda_init} λ_final={args.lambda_final} sched={args.lambda_schedule}")

    for step in range(args.steps):
        if cost_guard.over():
            print(f"[COST-ABORT] step={step}")
            cost_aborted = True
            break
        cur_lr = lr_at(step)
        for g in optimizer.param_groups:
            g["lr"] = cur_lr
        cur_lambda = lambda_at(step, args.steps, args.warmup,
                               args.lambda_init, args.lambda_final, args.lambda_schedule)

        engine.train()
        x, y = sample_batch(corpus, args.batch, args.ctx, device)
        optimizer.zero_grad()
        logits, info = engine(x)
        ce = F.cross_entropy(logits.reshape(-1, cfg.vocab_size), y.reshape(-1))
        gate_full = info["gate_full_live"]
        dispatch_mask = info["dispatch_mask"]
        n_now = info["n_cells"]
        aux = load_balance_aux(gate_full, dispatch_mask, n_now)
        ent_gate = -(gate_full.clamp(min=1e-12) * gate_full.clamp(min=1e-12).log()).sum()
        loss = ce + args.aux_alpha * aux - cur_lambda * ent_gate
        loss.backward()
        torch.nn.utils.clip_grad_norm_(list(engine.parameters()) + list(router.parameters()), max_norm=1.0)
        optimizer.step()

        mit_result = engine.mitosis_step(info)
        for ev in mit_result["events"]:
            if ev["type"] == "split":
                splits_in_run += 1

        w = info["weights"].detach()
        hist["loss"].append(loss.item())
        hist["ce"].append(ce.item())
        hist["aux"].append(float(aux.item()))
        hist["ent_gate"].append(float(ent_gate.item()))
        hist["wmax"].append(float(w.max().item()))
        hist["lambda"].append(cur_lambda)
        hist["cells"].append(engine.n_cells)
        hist["n_active_gt01"].append(int((w > 0.01).sum().item()))
        hist["gate_max"].append(float(gate_full.detach().max().item()))

        if step % args.log_every == 0 or step == args.steps - 1:
            def _m(k, n=50):
                arr = hist[k][-n:]
                return sum(arr) / max(len(arr), 1)
            print(f"[STEP {step:5d}] loss={loss.item():.4f} ce={_m('ce'):.4f} "
                  f"aux={_m('aux'):.4f} ent_gate={_m('ent_gate'):.4f}/{math.log(max(engine.n_cells,1)):.3f} "
                  f"wmax={_m('wmax'):.4f} active>.01={_m('n_active_gt01'):.1f}/{engine.n_cells} "
                  f"λ={cur_lambda:.4f} cells={engine.n_cells} splits={splits_in_run} "
                  f"cost=${cost_guard.current_usd():.2f}")
            sys.stdout.flush()

        if args.ckpt_every > 0 and (step + 1) % args.ckpt_every == 0 and (step + 1) != args.steps:
            cp = Path(args.output_dir) / f"ckpt_step_{step+1}.pt"
            save_ckpt(engine, router, cfg, cp, step + 1, args.top_k)
            # Mid-run persona snapshot (cheap, n_perms small).
            try:
                snap_a = f_persona_4a_routing(engine, args.identity_probe, device, n_perms=30)
                snap_b = f_persona_4b_content(engine, args.identity_probe, device, n_perms=30)
                print(f"  [SNAP {step+1}] 4a KL={snap_a['topk_weights']['mean_kl']:.4f} "
                      f"z={snap_a['topk_weights']['z_score_vs_null']:.2f} | "
                      f"4b cos_z={snap_b['z_score_vs_null']:.2f}")
            except Exception as e:
                print(f"  [SNAP {step+1}] failed: {e}")

    t_train = time.time() - t_start
    print(f"[INFO] training done wall={t_train:.1f}s cost=${cost_guard.current_usd():.2f}")
    save_ckpt(engine, router, cfg, Path(args.output_dir) / "ckpt_final.pt", len(hist["loss"]), args.top_k)

    print("\n=== F-PERSONA-4a routing (top-K MoE) ===")
    p4a = f_persona_4a_routing(engine, args.identity_probe, device, n_perms=args.n_perms)
    tw = p4a["topk_weights"]
    print(f"  verdict={p4a['verdict']} KL={tw['mean_kl']:.4f} null={tw['null_mean']:.4f}±{tw['null_std']:.4f} "
          f"z={tw['z_score_vs_null']:.2f} p={tw['p_value_one_sided']:.4f}")
    if p4a["soft_gate"]:
        sg = p4a["soft_gate"]
        print(f"  (soft gate) KL={sg['mean_kl']:.4f} z={sg['z_score_vs_null']:.2f}")

    print("\n=== F-PERSONA-4b content (M4 aggregated cosine) regression ===")
    p4b = f_persona_4b_content(engine, args.identity_probe, device, n_perms=args.n_perms)
    print(f"  verdict={p4b['verdict']} cos_dist={p4b['true']:.6f} null={p4b['null_mean']:.6f}±{p4b['null_std']:.6f} "
          f"z={p4b['z_score_vs_null']:.2f} p={p4b['p_value_one_sided']:.4f} (v2 carry z={p4b['v2_carry_z']:.2f})")

    print("\n=== F-V5MIT-1..5 regression ===")
    fv = f_v5mit_regression(engine, splits_in_run, sum(hist["ce"][-100:]) / max(min(100, len(hist["ce"])), 1))
    print(f"  {fv['verdict']}  " + " ".join(
        f"{k.split('_')[0]}={'P' if v['pass'] else 'F'}" for k, v in fv["checks"].items()))

    result = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "trainer": "v3-routing (architectural fix: top-K MoE router + load-balance aux + annealed gate-entropy)",
        "routing_fix": {
            "top_k": args.top_k, "aux_alpha": args.aux_alpha,
            "lambda_init": args.lambda_init, "lambda_final": args.lambda_final,
            "lambda_schedule": args.lambda_schedule,
            "router": "Linear(d_model -> max_cells), per-input (batch&seq mean-pooled), top-K hard gate + renorm",
        },
        "config": asdict(cfg),
        "n_params": n_params,
        "training": {
            "wall_seconds": t_train, "wall_hours": t_train / 3600.0,
            "cost_usd_actual": cost_guard.current_usd(), "cost_aborted": cost_aborted,
            "ce_final_avg100": sum(hist["ce"][-100:]) / max(min(100, len(hist["ce"])), 1),
            "aux_final_avg100": sum(hist["aux"][-100:]) / max(min(100, len(hist["aux"])), 1),
            "ent_gate_final_avg100": sum(hist["ent_gate"][-100:]) / max(min(100, len(hist["ent_gate"])), 1),
            "wmax_final_avg100": sum(hist["wmax"][-100:]) / max(min(100, len(hist["wmax"])), 1),
            "n_active_gt01_final_avg100": sum(hist["n_active_gt01"][-100:]) / max(min(100, len(hist["n_active_gt01"])), 1),
            "gate_max_final_avg100": sum(hist["gate_max"][-100:]) / max(min(100, len(hist["gate_max"])), 1),
            "lambda_final_avg100": sum(hist["lambda"][-100:]) / max(min(100, len(hist["lambda"])), 1),
            "log_N_target": math.log(max(engine.n_cells, 1)),
            "splits": splits_in_run, "n_cells_final": engine.n_cells,
            "phi_final": float(engine.phi), "phi_best": float(engine._phi_best),
        },
        "history_sample": {k: v[::max(1, len(v) // 200)] for k, v in hist.items()},
        "f_persona_4a_routing": p4a,
        "f_persona_4b_content": p4b,
        "f_v5mit_regression": fv,
    }
    out = Path(args.output_dir) / "cotrain_v3_routing_result.json"
    out.write_text(json.dumps(result, indent=2, default=str))
    print(f"\n[RESULT] {out}")
    print(f"[VERDICT] 4a={p4a['verdict']} (KL={tw['mean_kl']:.4f} z={tw['z_score_vs_null']:.2f}) | "
          f"4b={p4b['verdict']} (z={p4b['z_score_vs_null']:.2f}) | F-V5MIT={fv['verdict']}")
    return 0 if not cost_aborted else 3


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--steps", type=int, default=8000)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--ctx", type=int, default=256)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--warmup", type=int, default=500)
    ap.add_argument("--d-model", type=int, default=384)
    ap.add_argument("--n-head", type=int, default=6)
    ap.add_argument("--ffn-dim", type=int, default=1536)
    ap.add_argument("--initial-cells", type=int, default=2)
    ap.add_argument("--max-cells", type=int, default=64)
    ap.add_argument("--readout-mode", type=str, default="a_minus_g",
                    choices=["a_minus_g", "a_only", "a_plus_g"])
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--log-every", type=int, default=50)
    ap.add_argument("--ckpt-every", type=int, default=2000)
    ap.add_argument("--cost-cap-usd", type=float, default=8.0)
    ap.add_argument("--cost-per-hr", type=float, default=2.70)
    ap.add_argument("--estimated-wall-hr", type=float, default=1.5)
    ap.add_argument("--identity-probe", type=str, required=True)
    ap.add_argument("--top-k", type=int, default=4, help="top-K active cells per input (MoE gating)")
    ap.add_argument("--aux-alpha", type=float, default=0.01, help="Switch load-balancing aux coefficient")
    ap.add_argument("--lambda-init", type=float, default=1.0, help="annealed gate-entropy reg λ at warmup end")
    ap.add_argument("--lambda-final", type=float, default=0.01, help="annealed gate-entropy reg λ at end")
    ap.add_argument("--lambda-schedule", type=str, default="cosine", choices=["constant", "linear", "cosine"])
    ap.add_argument("--n-perms", type=int, default=100)
    return ap.parse_args()


if __name__ == "__main__":
    sys.exit(cotrain(parse_args()))
