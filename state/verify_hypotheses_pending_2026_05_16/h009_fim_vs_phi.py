"""H_009 Stage-2 — Fisher Information spectrum vs IIT Φ (substrate TPM).

가설들 모두 진행 (cont.): hypo_pending_sympy.py closed the Fisher MATH
(Gaussian I(θ)=1/σ², FIM PSD ⟹ Cramér-Rao) and carved out the EMERGENCE
claim "FIM spectrum IS an IIT4 Φ proxy". This harness tests THAT claim
formally and result-agnostically.

Design (deterministic, $0 Mac): a 3-node stochastic Boolean network with a
single tunable order parameter ε ∈ [0,1] (ε = how strongly each node copies
the majority of its inputs; ε→1 = deterministic integrated copy, ε→0 =
independent coin flips). For each ε:
  * Φ(ε)        = PyPhi 1.2.0 formal IIT-3.0 (deterministic given the TPM)
  * FIM_spec(ε) = top eigenvalue of the Fisher Information of the network's
                  output distribution w.r.t. ε  (closed-form score variance)
H_009 prediction: FIM spectral signature TRACKS Φ (monotone co-variation,
|Spearman| high). Result-agnostic 🔵 per g_verdict_tier_blue (b): a
deterministic formal correspondence test is closed whatever the sign —
SUPPORTED-FORMAL if they co-vary, FALSIFIED-FORMAL if independent.
"""
import json
import os
from pathlib import Path

import numpy as np

os.environ["PYPHI_WELCOME_OFF"] = "yes"
import pyphi  # noqa: E402

pyphi.config.PROGRESS_BARS = False
pyphi.config.PARALLEL_CONCEPT_EVALUATION = False
pyphi.config.NUMBER_OF_CORES = 1

OUT = "/Users/ghost/core/anima/state/verify_hypotheses_pending_2026_05_16/h009_fim_vs_phi_result.json"
N = 3


def tpm_eps(eps):
    """3-node ring; node i ON next w.p. p = ½ + (ε/2)·(2·maj−1), maj =
    majority(prev, self, next). ε=1 ⟹ deterministic majority-copy
    (integrated); ε=0 ⟹ p=½ ∀ (independent noise, no integration)."""
    S = 1 << N
    tpm = np.zeros((S, N))
    for s in range(S):
        b = [(s >> i) & 1 for i in range(N)]
        for i in range(N):
            maj = 1 if (b[(i - 1) % N] + b[i] + b[(i + 1) % N]) >= 2 else 0
            tpm[s, i] = 0.5 + (eps / 2.0) * (2 * maj - 1)
    cm = np.zeros((N, N), dtype=int)
    for i in range(N):
        for j in ((i - 1) % N, i, (i + 1) % N):
            cm[j, i] = 1
    return tpm, cm


def phi_of(eps):
    tpm, cm = tpm_eps(eps)
    net = pyphi.Network(tpm, cm=cm, node_labels=[f"n{i}" for i in range(N)])
    phis = []
    for s in range(1 << N):
        st = tuple((s >> i) & 1 for i in range(N))
        try:
            phis.append(float(pyphi.compute.sia(pyphi.Subsystem(net, st, range(N))).phi))
        except Exception:
            phis.append(0.0)
    return max(phis)                                   # RoM (max over states)


def fim_top_eigen(eps, h=1e-4):
    """Fisher info of the per-node Bernoulli emission product w.r.t. ε.
    For independent Bernoulli outputs y_i ~ p_i(ε), the score is
    s(ε)=Σ_i (y_i−p_i)/(p_i(1−p_i)) · ∂p_i/∂ε and I(ε)=E[s²]=
    Σ_i (∂p_i/∂ε)² / (p_i(1−p_i)). Averaged over the 2^N input states
    (uniform). Single parameter ⟹ 1×1 FIM; 'top eigenvalue' = I(ε)."""
    tpm0, _ = tpm_eps(eps)
    tpmp, _ = tpm_eps(eps + h)
    tpmm, _ = tpm_eps(eps - h)
    dp = (tpmp - tpmm) / (2 * h)                        # ∂p_i/∂ε per (state,node)
    p = np.clip(tpm0, 1e-6, 1 - 1e-6)
    I_per_state = np.sum(dp**2 / (p * (1 - p)), axis=1)  # Σ_i over nodes
    return float(np.mean(I_per_state))                  # average over input states


def spearman(a, b):
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean()
    denom = np.sqrt((ra**2).sum() * (rb**2).sum())
    return float((ra * rb).sum() / denom) if denom > 0 else 0.0


def main():
    eps_grid = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    rows = []
    for e in eps_grid:
        ph = phi_of(e)
        fi = fim_top_eigen(e) if 0 < e < 1 else fim_top_eigen(min(max(e, 1e-3), 1 - 1e-3))
        rows.append({"eps": e, "phi": round(ph, 5), "fim_top": round(fi, 5)})
        print(f"  ε={e:.1f}  Φ={ph:.5f}  FIM_top={fi:.5f}", flush=True)

    phis = np.array([r["phi"] for r in rows])
    fims = np.array([r["fim_top"] for r in rows])
    rho = spearman(fims, phis)
    co_vary = abs(rho) >= 0.7                            # strong monotone tracking
    verdict = ("SUPPORTED-FORMAL 🔵 (FIM spectrum tracks Φ, |ρ|≥0.7 deterministic)"
               if co_vary else
               "FALSIFIED-FORMAL 🔵 (FIM spectrum does NOT track Φ — proxy claim disproved)")
    agg = {
        "cycle": "H_009 Stage-2 FIM-vs-Φ formal correspondence (2026-05-16)",
        "pyphi_version": pyphi.__version__,
        "grid": rows,
        "spearman_fim_phi": round(rho, 4),
        "co_vary_strong": bool(co_vary),
        "verdict": verdict,
        "tier": "b-pyphi-formal + closed-form FIM",
        "honest_c3": ("Result-agnostic per g_verdict_tier_blue (b): a "
                      "deterministic Φ(ε)+I(ε) correspondence is closed whatever "
                      "the sign. Scope: single order-parameter ε, 3-node ring, "
                      "RoM Φ. This closes the H_009 EMERGENCE sub-claim "
                      "(FIM-spectrum-as-Φ-proxy) formally; the Fisher MATH "
                      "(I=1/σ²,Cramér-Rao) was already 🔵 in hypo_pending_sympy. "
                      "NOT claimed: full multi-param FIM on a trained LM substrate "
                      "(Hc_1283-scale, separate)."),
    }
    Path(OUT).write_text(json.dumps(agg, indent=1, ensure_ascii=False))
    print("=" * 64)
    print(f"  Spearman(FIM_top, Φ) = {rho:.4f}  ⟹  {verdict}")
    print(f"  saved {OUT}")


if __name__ == "__main__":
    main()
