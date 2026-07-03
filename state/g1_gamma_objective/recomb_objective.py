#!/usr/bin/env python3
"""γ recomb-objective — REFERENCE loss for the G1 L4 lever (DESIGN, not wired).

Drop-in for cli/train.py OBJECTIVE_BUILDERS as `recomb_objective`. teacher-forced,
NO sampling, NO aux params → operates on readout logits only, gradient flows
readout→trunk, and the `.clm` serialize path stays 100% open (no head to drop).

MATH (see DESIGN.md §(a) for derivation):
  m_c      = soft-OR over continuation positions & over c's keyword bytes of logp   (differentiable coverage)
  R(A,B)   = softmin(m_A, m_B)        # min-pool = echo-guard: BOTH concepts must be covered
  R_echo   = softmin(m_A, m_D)        # D = distractor not in seed (shuffle control)
  earned   = R(A,B) - R_echo
  L_recomb = mean( R_echo - R(A,B) )  = -earned
  L_total  = CE + gamma * L_recomb

This surrogate is the differentiable form of the FROZEN G1 metric (evaluate.py
g_eval_g1: cov>=2 AND cov>max_single). Verdict is DIRECTIONAL (torch) — TERMINAL only
via `anima evaluate --py <clm>` engine-native re-measure (a_engine_native_learning).

⚠️ DESIGN ARTIFACT — cost-gated. Not imported by production. Wiring = follow-on.
"""
from __future__ import annotations
import torch
import torch.nn as nn
import torch.nn.functional as F

RECOMB_GAMMA = 0.5      # γ — recomb aux weight (frozen, pre-registered)
RECOMB_TAU   = 0.5      # soft-pool temperature τ (τ→0 = hard max = exact metric)


def _soft_or(scores: torch.Tensor, tau: float, dim: int) -> torch.Tensor:
    """soft-OR = τ·logsumexp(scores/τ) — differentiable max (τ→0 → hard max)."""
    return tau * torch.logsumexp(scores / tau, dim=dim)


def _soft_min(a: torch.Tensor, b: torch.Tensor, tau: float) -> torch.Tensor:
    """softmin(a,b) = -τ·logsumexp(-[a,b]/τ) — differentiable min (the echo-guard)."""
    stk = torch.stack([a, b], dim=-1)
    return -tau * torch.logsumexp(-stk / tau, dim=-1)


class RecombObjective(nn.Module):
    """γ recomb-objective. Consumes per-window seed pair-labels + a byte-keyword table
    (constant, no params). Attach the pair metadata to the batch via `pair_ctx` (see
    build_heldout_corpus.py for how the composed corpus tags each window).

    NOTE: this reference expects the trainer to pass, per batch, alongside (logits, y):
      pair_ctx = {
        "cont_mask": BoolTensor(B, T),     # continuation positions C (post-seed)
        "A_bytes":   LongTensor(B, Ka),    # concept-A keyword discriminant bytes (pad=-1)
        "B_bytes":   LongTensor(B, Kb),    # concept-B keyword discriminant bytes (pad=-1)
        "D_bytes":   LongTensor(B, Kd),    # distractor keyword bytes (shuffle control)
      }
    The clean way to thread this in cli/train.py: extend get_batch() to also return
    pair_ctx for composed-corpus windows (None for register-anchor windows → term skipped),
    and pass it as a kwarg. Kept OUT of the generic objfn(logits,y,V,gen,penultimate=...)
    signature here for clarity; wiring adapts the call site (follow-on)."""

    def __init__(self, gamma: float = RECOMB_GAMMA, tau: float = RECOMB_TAU):
        super().__init__()
        self.gamma = gamma
        self.tau = tau

    def _concept_score(self, logp, cont_mask, kw_bytes):
        """m_c for one concept across the batch.
        logp: (B, T, V) log-softmax; cont_mask: (B,T); kw_bytes: (B, Kc) byte ids (pad=-1).
        Returns (B,) soft-OR-over-(positions × keyword-bytes) of logp at kw bytes."""
        B, T, V = logp.shape
        NEG = -1e9
        # gather logp at each keyword byte over all positions -> (B, T, Kc)
        kb = kw_bytes.clamp(min=0)                             # (B, Kc)
        Kc = kb.shape[1]
        idx = kb.unsqueeze(1).expand(B, T, Kc)                 # (B,T,Kc)
        g = torch.gather(logp, 2, idx)                         # (B,T,Kc)
        # mask padded keywords and non-continuation positions to NEG
        pad = (kw_bytes < 0).unsqueeze(1)                      # (B,1,Kc)
        g = g.masked_fill(pad, NEG)
        g = g.masked_fill(~cont_mask.unsqueeze(-1), NEG)       # (B,T,Kc)
        # soft-OR over positions then over keywords (any-position, any-keyword)
        s_pos = _soft_or(g, self.tau, dim=1)                   # (B,Kc)
        m_c = _soft_or(s_pos, self.tau, dim=1)                 # (B,)
        return m_c

    def forward(self, logits, targets, V, gen, pair_ctx=None):
        """logits: (B, V, T) — matches cli/train.py convention. pair_ctx per above."""
        ce = F.cross_entropy(
            logits.transpose(1, 2).reshape(-1, V), targets.reshape(-1))
        if pair_ctx is None:
            return ce, {}
        logp = F.log_softmax(logits.transpose(1, 2), dim=-1)   # (B,T,V)
        cm = pair_ctx["cont_mask"]
        m_A = self._concept_score(logp, cm, pair_ctx["A_bytes"])
        m_B = self._concept_score(logp, cm, pair_ctx["B_bytes"])
        m_D = self._concept_score(logp, cm, pair_ctx["D_bytes"])
        R      = _soft_min(m_A, m_B, self.tau)                 # (B,) both-covered reward
        R_echo = _soft_min(m_A, m_D, self.tau)                 # (B,) shuffle-control baseline
        earned = R - R_echo                                    # >0 iff right>wrong composition
        L_recomb = (R_echo - R).mean()                         # = -earned.mean()
        loss = ce + self.gamma * L_recomb
        return loss, {"recomb": float(L_recomb.detach()),
                      "earned": float(earned.mean().detach()),
                      "m_A": float(m_A.mean().detach()),
                      "m_B": float(m_B.mean().detach()),
                      "m_D": float(m_D.mean().detach())}


# ── ablations (pre-registered, DESIGN.md §(c)) ───────────────────────────────
class RecombAblateEcho(RecombObjective):
    """echo-guard OFF: softmin → mean (coverage-sum, no both-required). Must go INERT
    (not clear the frozen G1 bar) or the echo-guard isn't load-bearing."""
    def forward(self, logits, targets, V, gen, pair_ctx=None):
        ce = F.cross_entropy(logits.transpose(1, 2).reshape(-1, V), targets.reshape(-1))
        if pair_ctx is None:
            return ce, {}
        logp = F.log_softmax(logits.transpose(1, 2), dim=-1)
        cm = pair_ctx["cont_mask"]
        m_A = self._concept_score(logp, cm, pair_ctx["A_bytes"])
        m_B = self._concept_score(logp, cm, pair_ctx["B_bytes"])
        m_D = self._concept_score(logp, cm, pair_ctx["D_bytes"])
        R = 0.5 * (m_A + m_B); R_echo = 0.5 * (m_A + m_D)      # MEAN, not softmin
        L_recomb = (R_echo - R).mean()
        return ce + self.gamma * L_recomb, {"recomb_ablate_echo": float(L_recomb.detach())}


# γ=0 ablation = just use ce_marginal on the SAME composed corpus (no code needed).

# builder for cli/train.py OBJECTIVE_BUILDERS (follow-on wiring):
#   "recomb_objective": lambda d, V, dev: RecombObjective().to(dev)
# and add OBJ_NEEDS_PAIR_CTX = {"recomb_objective"} so main() threads pair_ctx.
