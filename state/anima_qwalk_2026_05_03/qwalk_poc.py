#!/usr/bin/env python3
"""
Quantum-walk node init for anima knowledge graph + benchmark vs classical random walk.

Substrates:
  (A) EEG 16-channel coupling graph (synthetic, anima-eeg style, 4 functional clusters)
  (B) Stochastic Block Model graph (3 communities, n=60) — downstream node classification

Pipeline:
  1. Build adjacency A
  2. Continuous-time quantum walk (CTQW): U(t) = exp(-i H t), H = -A (or H = L)
     - long-time-averaged occupation P_qw(i,j) = lim_T (1/T) ∫_0^T |<i|U(t)|j>|^2 dt
       = sum over eigen-projectors with degeneracy handling
  3. Classical random walk stationary π_rw = D / sum(D) for connected undirected
  4. Node embeddings:
     - rw_emb: top-k eigenvectors of P (transition matrix)  [spectral / DeepWalk-lite]
     - qw_emb: top-k eigenvectors of mixing matrix M_qw = sum_k |v_k><v_k| ⊗ |v_k><v_k|
       (we use the concatenation: classical spectral row + qw long-time amp row, normalized)
     - To make a clean A vs B comparison: use the *rows* of P_rw and P_qw as embeddings
       reduced via PCA to d=k.
  5. Downstream:
     - Task: node classification on SBM (true block labels) — logistic regression CV
     - Falsifier F-QWALK-1: qwalk_acc - rw_acc > +5% on held-out fold mean

Constraints:
  - $0 Mac/ubu local
  - numpy + scipy + sklearn + networkx only (no GPU, no quantum SDK)
  - Deterministic seeds
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
import networkx as nx
from numpy.linalg import eigh
from scipy.linalg import expm
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler

SEED = 20260503
RNG = np.random.default_rng(SEED)
EPS = 1e-12

# ----------------------------- substrate builders -----------------------------

def build_eeg16_coupling() -> tuple[np.ndarray, np.ndarray]:
    """16-channel EEG coupling graph (4 functional clusters of 4: frontal,
    central, parietal, occipital). Edge weights from synthetic phase-locking
    values (PLV) drawn from cluster-conditional Beta distributions.
    Returns (A symmetric, labels)."""
    n = 16
    labels = np.repeat(np.arange(4), 4)  # 4 clusters x 4 channels
    A = np.zeros((n, n))
    rng = np.random.default_rng(SEED + 1)
    for i in range(n):
        for j in range(i + 1, n):
            if labels[i] == labels[j]:
                w = rng.beta(8.0, 2.0)   # within-cluster strong PLV
            else:
                w = rng.beta(1.5, 8.0)   # cross-cluster weak PLV
            # Threshold weak edges to keep sparsity moderate
            A[i, j] = w if w > 0.15 else 0.0
            A[j, i] = A[i, j]
    return A, labels


def build_sbm(n_per_block: int = 20, n_blocks: int = 3,
              p_in: float = 0.35, p_out: float = 0.04
              ) -> tuple[np.ndarray, np.ndarray]:
    """SBM for downstream node classification."""
    sizes = [n_per_block] * n_blocks
    probs = (np.ones((n_blocks, n_blocks)) * p_out
             + np.eye(n_blocks) * (p_in - p_out))
    G = nx.stochastic_block_model(sizes, probs.tolist(), seed=SEED + 2)
    A = nx.to_numpy_array(G, dtype=float)
    labels = np.repeat(np.arange(n_blocks), n_per_block)
    # Make sure connected (drop isolates by linking them to nearest block-mate)
    for i in np.where(A.sum(axis=1) == 0)[0]:
        j = int(np.where(labels == labels[i])[0][0])
        if j == i:
            j = (i + 1) % len(labels)
        A[i, j] = 1.0
        A[j, i] = 1.0
    return A, labels


# ----------------------------- walks -----------------------------------------

def random_walk_transition(A: np.ndarray) -> np.ndarray:
    d = A.sum(axis=1)
    d_safe = np.where(d > 0, d, 1.0)
    P = A / d_safe[:, None]
    return P


def random_walk_stationary(A: np.ndarray) -> np.ndarray:
    """For undirected connected graph: pi_i = d_i / 2|E|."""
    d = A.sum(axis=1)
    return d / max(d.sum(), EPS)


def ctqw_long_time_average(A: np.ndarray,
                           hamiltonian: str = "adjacency"
                           ) -> tuple[np.ndarray, np.ndarray]:
    """Continuous-time quantum walk long-time-average occupation matrix.

    H = A (adjacency) or H = L = D - A (Laplacian). Real symmetric => H = sum_k λ_k |v_k><v_k|.
    P_qw(i,j) = lim_T (1/T) ∫_0^T |<i| e^{-iHt} |j>|^2 dt
              = sum over distinct eigenvalues λ:  ( sum_{k:λ_k=λ} v_k(i) v_k(j) )^2
    With degeneracy handling via grouping eigenvalues within tol.

    Returns (P_qw, stationary_qw) where stationary_qw_j = (1/N) * sum_i P_qw(i,j).
    """
    if hamiltonian == "adjacency":
        H = A
    elif hamiltonian == "laplacian":
        d = A.sum(axis=1)
        H = np.diag(d) - A
    else:
        raise ValueError(hamiltonian)

    w, V = eigh(H)
    n = H.shape[0]
    # group by distinct eigenvalues (tolerance 1e-8)
    order = np.argsort(w)
    w_sorted = w[order]
    V_sorted = V[:, order]
    P_qw = np.zeros((n, n))
    k = 0
    while k < n:
        j = k + 1
        while j < n and abs(w_sorted[j] - w_sorted[k]) < 1e-8:
            j += 1
        # block [k:j] shares eigenvalue
        Vk = V_sorted[:, k:j]
        # projector onto eigenspace: Pi = Vk Vk^T
        Pi = Vk @ Vk.T
        # contribution: (Pi[i,j])^2  elementwise
        P_qw += Pi * Pi
        k = j
    # P_qw is symmetric, rows sum to 1 (since sum_λ Pi = I and the off-diagonal cross terms
    # vanish under long-time average). Verify:
    row = P_qw.sum(axis=1)
    # uniform "stationary" of qw on regular graphs; on irregular graphs it's non-uniform
    # but column-mean (assuming start = uniform) gives the long-time occupancy.
    stationary = P_qw.mean(axis=0)
    stationary = stationary / max(stationary.sum(), EPS)
    return P_qw, stationary, row


# ----------------------------- embeddings & downstream ------------------------

def embedding_from_matrix(M: np.ndarray, dim: int) -> np.ndarray:
    """PCA the rows of M down to `dim`. Standardize first to make scales comparable."""
    Xs = StandardScaler(with_mean=True, with_std=True).fit_transform(M)
    d_eff = min(dim, Xs.shape[1], Xs.shape[0] - 1)
    pca = PCA(n_components=d_eff, random_state=SEED)
    return pca.fit_transform(Xs)


def cv_node_classification(emb: np.ndarray, labels: np.ndarray,
                           n_splits: int = 5) -> dict:
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=SEED)
    accs = []
    for tr, te in skf.split(emb, labels):
        clf = LogisticRegression(max_iter=2000, C=1.0,
                                 random_state=SEED)
        clf.fit(emb[tr], labels[tr])
        accs.append(float(clf.score(emb[te], labels[te])))
    return {"acc_mean": float(np.mean(accs)),
            "acc_std": float(np.std(accs)),
            "folds": accs}


# ----------------------------- comparisons -----------------------------------

def kl_div(p: np.ndarray, q: np.ndarray) -> float:
    p = np.clip(p, EPS, None); p /= p.sum()
    q = np.clip(q, EPS, None); q /= q.sum()
    return float(np.sum(p * np.log(p / q)))


def js_div(p: np.ndarray, q: np.ndarray) -> float:
    m = 0.5 * (p / p.sum() + q / q.sum())
    return 0.5 * kl_div(p, m) + 0.5 * kl_div(q, m)


def tvd(p: np.ndarray, q: np.ndarray) -> float:
    p = p / p.sum(); q = q / q.sum()
    return 0.5 * float(np.sum(np.abs(p - q)))


# ----------------------------- main ------------------------------------------

@dataclass
class Verdict:
    falsifier_id: str
    threshold_pct: float
    eeg16_rw_acc: float
    eeg16_qw_acc: float
    eeg16_delta_pct: float
    sbm_rw_acc: float
    sbm_qw_acc: float
    sbm_delta_pct: float
    decision: str   # "F-QWALK-1 PASS" or "F-QWALK-1 FAIL"
    notes: str


def run() -> dict:
    out = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "seed": SEED,
           "substrates": {}}

    # ---------------- (A) EEG 16-channel coupling -----------------
    A_eeg, lbl_eeg = build_eeg16_coupling()
    P_rw_eeg = random_walk_transition(A_eeg)
    pi_rw_eeg = random_walk_stationary(A_eeg)
    P_qw_eeg, pi_qw_eeg, rowsum_eeg = ctqw_long_time_average(A_eeg, "adjacency")

    eeg_dim = 8
    emb_rw_eeg = embedding_from_matrix(P_rw_eeg, eeg_dim)
    emb_qw_eeg = embedding_from_matrix(P_qw_eeg, eeg_dim)
    cv_rw_eeg = cv_node_classification(emb_rw_eeg, lbl_eeg, n_splits=4)
    cv_qw_eeg = cv_node_classification(emb_qw_eeg, lbl_eeg, n_splits=4)

    out["substrates"]["eeg16_coupling"] = {
        "n_nodes": int(A_eeg.shape[0]),
        "n_edges": int((A_eeg > 0).sum() // 2),
        "edge_density": float((A_eeg > 0).sum() / (A_eeg.shape[0] * (A_eeg.shape[0] - 1))),
        "stationary_rw": pi_rw_eeg.tolist(),
        "stationary_qw": pi_qw_eeg.tolist(),
        "kl_qw_vs_rw": kl_div(pi_qw_eeg, pi_rw_eeg),
        "kl_rw_vs_qw": kl_div(pi_rw_eeg, pi_qw_eeg),
        "js_div": js_div(pi_qw_eeg, pi_rw_eeg),
        "tvd": tvd(pi_qw_eeg, pi_rw_eeg),
        "qw_rowsum_max_dev_from_1": float(np.max(np.abs(rowsum_eeg - 1.0))),
        "downstream_task": "4-cluster_node_classification",
        "rw_cv_acc": cv_rw_eeg,
        "qw_cv_acc": cv_qw_eeg,
        "delta_acc_pct": (cv_qw_eeg["acc_mean"] - cv_rw_eeg["acc_mean"]) * 100.0,
    }

    # ---------------- (B) SBM for clean classification benchmark -----
    A_sbm, lbl_sbm = build_sbm()
    P_rw_sbm = random_walk_transition(A_sbm)
    pi_rw_sbm = random_walk_stationary(A_sbm)
    P_qw_sbm, pi_qw_sbm, rowsum_sbm = ctqw_long_time_average(A_sbm, "adjacency")

    sbm_dim = 16
    emb_rw_sbm = embedding_from_matrix(P_rw_sbm, sbm_dim)
    emb_qw_sbm = embedding_from_matrix(P_qw_sbm, sbm_dim)
    cv_rw_sbm = cv_node_classification(emb_rw_sbm, lbl_sbm, n_splits=5)
    cv_qw_sbm = cv_node_classification(emb_qw_sbm, lbl_sbm, n_splits=5)

    out["substrates"]["sbm_3block"] = {
        "n_nodes": int(A_sbm.shape[0]),
        "n_edges": int((A_sbm > 0).sum() // 2),
        "edge_density": float((A_sbm > 0).sum() / (A_sbm.shape[0] * (A_sbm.shape[0] - 1))),
        "stationary_rw": pi_rw_sbm.tolist(),
        "stationary_qw": pi_qw_sbm.tolist(),
        "kl_qw_vs_rw": kl_div(pi_qw_sbm, pi_rw_sbm),
        "kl_rw_vs_qw": kl_div(pi_rw_sbm, pi_qw_sbm),
        "js_div": js_div(pi_qw_sbm, pi_rw_sbm),
        "tvd": tvd(pi_qw_sbm, pi_rw_sbm),
        "qw_rowsum_max_dev_from_1": float(np.max(np.abs(rowsum_sbm - 1.0))),
        "downstream_task": "3-block_node_classification",
        "rw_cv_acc": cv_rw_sbm,
        "qw_cv_acc": cv_qw_sbm,
        "delta_acc_pct": (cv_qw_sbm["acc_mean"] - cv_rw_sbm["acc_mean"]) * 100.0,
    }

    # ---------------- verdict ----------------
    delta_eeg = out["substrates"]["eeg16_coupling"]["delta_acc_pct"]
    delta_sbm = out["substrates"]["sbm_3block"]["delta_acc_pct"]
    # Falsifier on the canonical downstream substrate (SBM, since EEG cluster sizes
    # are degenerate by symmetry — qw projector preserves degenerate eigenspaces and
    # may perfectly recover the partition; we report both for transparency).
    decision_sbm = "PASS" if delta_sbm > 5.0 else "FAIL"
    notes = ("Primary falsifier evaluated on SBM (clean ground-truth blocks). "
             "EEG16 substrate reported alongside as an exploratory anima-domain check "
             "with synthetic PLV weights — not a held-out empirical EEG dataset.")

    verdict = Verdict(
        falsifier_id="F-QWALK-1",
        threshold_pct=5.0,
        eeg16_rw_acc=out["substrates"]["eeg16_coupling"]["rw_cv_acc"]["acc_mean"],
        eeg16_qw_acc=out["substrates"]["eeg16_coupling"]["qw_cv_acc"]["acc_mean"],
        eeg16_delta_pct=delta_eeg,
        sbm_rw_acc=out["substrates"]["sbm_3block"]["rw_cv_acc"]["acc_mean"],
        sbm_qw_acc=out["substrates"]["sbm_3block"]["qw_cv_acc"]["acc_mean"],
        sbm_delta_pct=delta_sbm,
        decision=f"F-QWALK-1 {decision_sbm}",
        notes=notes,
    )
    out["verdict"] = asdict(verdict)
    return out


def main():
    state_dir = Path("/Users/ghost/core/anima/state/anima_qwalk_2026_05_03")
    tmp_dir = Path("/tmp/anima_qwalk_2026_05_03")
    state_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    out = run()
    out["wall_seconds"] = round(time.time() - t0, 3)

    # walk_comparison.json (full numerical detail)
    (state_dir / "walk_comparison.json").write_text(json.dumps(out, indent=2))
    (tmp_dir / "walk_comparison.json").write_text(json.dumps(out, indent=2))

    # verdict.json (slim)
    verdict_doc = {
        "timestamp": out["timestamp"],
        "wall_seconds": out["wall_seconds"],
        "seed": SEED,
        **out["verdict"],
        "summary_metrics": {
            "eeg16": {
                "kl_qw_vs_rw": out["substrates"]["eeg16_coupling"]["kl_qw_vs_rw"],
                "js_div":      out["substrates"]["eeg16_coupling"]["js_div"],
                "tvd":         out["substrates"]["eeg16_coupling"]["tvd"],
            },
            "sbm_3block": {
                "kl_qw_vs_rw": out["substrates"]["sbm_3block"]["kl_qw_vs_rw"],
                "js_div":      out["substrates"]["sbm_3block"]["js_div"],
                "tvd":         out["substrates"]["sbm_3block"]["tvd"],
            },
        },
    }
    (state_dir / "verdict.json").write_text(json.dumps(verdict_doc, indent=2))
    (tmp_dir / "verdict.json").write_text(json.dumps(verdict_doc, indent=2))

    print(json.dumps(verdict_doc, indent=2))


if __name__ == "__main__":
    main()
