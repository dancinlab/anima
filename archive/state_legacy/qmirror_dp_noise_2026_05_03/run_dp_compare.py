#!/usr/bin/env python3
"""qmirror QRNG-based DP noise vs classical Laplace — falsifier F-QDP-1.

Hypothesis (F-QDP-1): qmirror QRNG-sampled Laplace noise yields
  utility(qmirror) >= utility(classical) AND
  privacy_bound_empirical(qmirror) <= privacy_bound_empirical(classical)
on a small synthetic logistic-regression DP-SGD task.

Method:
  1. Synthetic dataset: 1000 rows, 20 features, 2 informative, binary label
     (sklearn make_classification). 80/20 train/test split.
  2. DP-SGD on logistic regression (sigmoid + BCE):
       - per-sample gradient L2 clip to C=1.0
       - noise injected on summed clipped gradient with Laplace scale
         b = (2C/n_batch) / epsilon   (epsilon=1.0 per-step bound, simple)
       - Path A: torch.distributions.Laplace(0, b) sampling
       - Path B: same b, but Laplace samples synthesized via inverse-CDF
         from qmirror QRNG bytes (uniform U(0,1) -> Laplace inverse CDF)
       - 30 epochs, batch_size=64, SGD lr=0.05, identical seed for init,
         data, batch order; ONLY the noise source differs.
  3. Membership inference attack (MIA, Yeom et al. style):
       - For each member (train) and non-member (test) sample, compute
         per-sample loss under the DP model.
       - AUC of (1 - loss) discriminates members.
       - lower AUC = better empirical privacy.
  4. Multiple seeds (10) for statistical stability; report mean + SE.
  5. Falsifier verdict.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
from sklearn.datasets import make_classification
from sklearn.metrics import roc_auc_score

REPO = Path("/Users/ghost/core/anima")
OUT = REPO / "state" / "qmirror_dp_noise_2026_05_03"
OUT.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# qmirror QRNG byte source (extended deterministically from MOCK LCG).
# We mirror the Park-Miller / Numerical Recipes LCG used in
# qmirror_qrng_nist_tier1plus_2026_05_03/run_tier1plus.py:qmirror_mock_lcg_bytes
# (same coefficients a=1664525, c=1013904223, m=2^32, seed=12345). This keeps
# byte-for-byte parity with the canonical qmirror MOCK source already validated
# in the regression battery (regression_summary.txt: qmirror_qrng_mock_1024 PASS).
# -----------------------------------------------------------------------------
def qmirror_mock_lcg_bytes(n_bytes: int, seed: int = 12345) -> bytes:
    s = seed if seed > 0 else 12345
    out = bytearray(n_bytes)
    a = 1664525
    c = 1013904223
    m = 4294967296
    for i in range(n_bytes):
        s = (a * s + c) % m
        out[i] = s % 256
    return bytes(out)


class QmirrorByteStream:
    """Indexable byte stream that auto-extends via the same LCG as needed."""

    def __init__(self, seed: int = 12345, initial_bytes: int = 65536):
        self._seed = seed
        self._buf = bytearray(qmirror_mock_lcg_bytes(initial_bytes, seed=seed))
        # State for continuation: re-drive the LCG forward by initial_bytes
        s = seed
        a, c, m = 1664525, 1013904223, 4294967296
        for _ in range(initial_bytes):
            s = (a * s + c) % m
        self._lcg_state = s

    def _extend(self, more_bytes: int) -> None:
        s = self._lcg_state
        a, c, m = 1664525, 1013904223, 4294967296
        for _ in range(more_bytes):
            s = (a * s + c) % m
            self._buf.append(s % 256)
        self._lcg_state = s

    def take(self, n: int, offset: int) -> np.ndarray:
        """Return a uint8 ndarray of n bytes starting at offset."""
        end = offset + n
        if end > len(self._buf):
            self._extend(end - len(self._buf) + 1024)
        return np.frombuffer(bytes(self._buf[offset:end]), dtype=np.uint8)


def qmirror_uniform(n: int, stream: QmirrorByteStream, offset: int) -> np.ndarray:
    """Draw n uniforms in (0,1) from qmirror bytes via 4-byte concatenation
    -> uint32 -> /(2^32). Avoids 0 and 1 endpoints by clipping."""
    raw = stream.take(4 * n, offset).astype(np.uint32)
    # Pack 4 bytes -> uint32 (little-endian)
    u32 = (raw[0::4]
           | (raw[1::4] << 8)
           | (raw[2::4] << 16)
           | (raw[3::4] << 24))
    # uniform on (0,1), avoiding exact 0 / 1 for log() in inverse CDF
    u = (u32.astype(np.float64) + 0.5) / (2.0 ** 32)
    return u


def laplace_inverse_cdf(u: np.ndarray, scale: float) -> np.ndarray:
    """Standard Laplace(0, b) inverse CDF: F^{-1}(u) = -b sgn(u-0.5) ln(1-2|u-0.5|)."""
    v = u - 0.5
    return -scale * np.sign(v) * np.log1p(-2.0 * np.abs(v))


# -----------------------------------------------------------------------------
# DP-SGD logistic regression
# -----------------------------------------------------------------------------
def make_data(seed: int):
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=2,
        n_redundant=2,
        n_repeated=0,
        n_classes=2,
        n_clusters_per_class=1,
        flip_y=0.05,
        class_sep=1.0,
        random_state=seed,
    )
    # Standardise
    X = (X - X.mean(axis=0)) / X.std(axis=0)
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(X))
    n_train = 800
    tr, te = idx[:n_train], idx[n_train:]
    return (X[tr].astype(np.float32), y[tr].astype(np.float32),
            X[te].astype(np.float32), y[te].astype(np.float32))


def per_sample_grads(w, b, Xb, yb):
    """Per-sample gradient of BCE w.r.t. (w, b) for logistic regression.

    Returns:
      gw: (B, D) per-sample gradient w.r.t. w
      gb: (B,)   per-sample gradient w.r.t. b
    """
    logits = Xb @ w + b           # (B,)
    p = torch.sigmoid(logits)
    diff = (p - yb)               # (B,) dL/dz
    gw = diff.unsqueeze(1) * Xb   # (B, D)
    gb = diff                     # (B,)
    return gw, gb


def clip_per_sample(gw, gb, C):
    """L2-clip the per-sample gradient (gw,gb concatenated) to norm C."""
    flat = torch.cat([gw, gb.unsqueeze(1)], dim=1)  # (B, D+1)
    norms = flat.norm(dim=1, keepdim=True).clamp(min=1e-12)
    factor = (C / norms).clamp(max=1.0)
    flat_clipped = flat * factor
    return flat_clipped[:, :-1], flat_clipped[:, -1]


def train_dp_sgd(
    X_tr, y_tr, X_te, y_te,
    epsilon: float,
    noise_path: str,             # "classical" or "qmirror"
    qmirror_stream: QmirrorByteStream | None,
    qmirror_offset: list[int],   # mutable offset (single-element list)
    seed: int,
    n_epochs: int = 30,
    batch_size: int = 64,
    lr: float = 0.05,
    clip_C: float = 1.0,
):
    torch.manual_seed(seed)
    np.random.seed(seed)
    D = X_tr.shape[1]
    w = torch.zeros(D, dtype=torch.float64, requires_grad=False)
    b = torch.zeros((), dtype=torch.float64, requires_grad=False)

    Xt = torch.from_numpy(X_tr).double()
    yt = torch.from_numpy(y_tr).double()

    # Per-step Laplace scale: sensitivity 2C / batch_size, divided by epsilon
    # (we treat each minibatch step as one query at the given epsilon budget;
    #  this is a per-step bound, not an end-to-end composition — see caveats).
    sens = 2.0 * clip_C / batch_size
    scale = sens / epsilon

    rng = np.random.default_rng(seed)
    n = len(Xt)
    for ep in range(n_epochs):
        perm = rng.permutation(n)
        for start in range(0, n, batch_size):
            idx = perm[start:start + batch_size]
            if len(idx) < batch_size:
                continue
            Xb = Xt[idx]
            yb = yt[idx]
            gw, gb = per_sample_grads(w, b, Xb, yb)
            gw_c, gb_c = clip_per_sample(gw, gb, clip_C)
            # sum, then divide by batch_size (DP-SGD averaging post-noise)
            sum_w = gw_c.sum(dim=0)             # (D,)
            sum_b = gb_c.sum()                   # scalar

            # Noise
            if noise_path == "classical":
                # torch.distributions.Laplace seeded by torch.manual_seed above
                lap = torch.distributions.Laplace(
                    torch.zeros(D + 1, dtype=torch.float64),
                    torch.full((D + 1,), scale, dtype=torch.float64),
                )
                noise = lap.sample()
                noise_w = noise[:D]
                noise_b = noise[D]
            elif noise_path == "qmirror":
                u = qmirror_uniform(D + 1, qmirror_stream, qmirror_offset[0])
                qmirror_offset[0] += 4 * (D + 1)
                z = laplace_inverse_cdf(u, scale)
                noise_w = torch.from_numpy(z[:D])
                noise_b = torch.tensor(z[D], dtype=torch.float64)
            else:
                raise ValueError(noise_path)

            noisy_sum_w = sum_w + noise_w
            noisy_sum_b = sum_b + noise_b
            # average
            grad_w = noisy_sum_w / batch_size
            grad_b = noisy_sum_b / batch_size
            w = w - lr * grad_w
            b = b - lr * grad_b

    # Eval
    Xte_t = torch.from_numpy(X_te).double()
    yte_t = torch.from_numpy(y_te).double()
    with torch.no_grad():
        train_logits = Xt @ w + b
        train_p = torch.sigmoid(train_logits)
        train_loss = -(yt * torch.log(train_p.clamp(1e-12, 1 - 1e-12))
                       + (1 - yt) * torch.log((1 - train_p).clamp(1e-12, 1 - 1e-12)))
        train_acc = ((train_p > 0.5).double() == yt).double().mean().item()

        test_logits = Xte_t @ w + b
        test_p = torch.sigmoid(test_logits)
        test_loss = -(yte_t * torch.log(test_p.clamp(1e-12, 1 - 1e-12))
                      + (1 - yte_t) * torch.log((1 - test_p).clamp(1e-12, 1 - 1e-12)))
        test_acc = ((test_p > 0.5).double() == yte_t).double().mean().item()

    return {
        "train_acc": train_acc,
        "test_acc": test_acc,
        "train_loss_per_sample": train_loss.numpy(),
        "test_loss_per_sample": test_loss.numpy(),
        "w_norm": float(w.norm().item()),
        "b": float(b.item()),
    }


def membership_inference_auc(train_loss: np.ndarray, test_loss: np.ndarray) -> dict:
    """Yeom-style loss-threshold MIA. Members (train) tend to have lower loss.

    Score = -loss. Label = 1 for member, 0 for non-member.
    """
    scores = np.concatenate([-train_loss, -test_loss])
    labels = np.concatenate([np.ones(len(train_loss)), np.zeros(len(test_loss))])
    if np.std(scores) < 1e-12:
        return {"auc": 0.5, "advantage": 0.0,
                "advantage_note": "degenerate (no variance in scores)"}
    auc = float(roc_auc_score(labels, scores))
    # Yeom advantage: max over thresholds of (TPR - FPR). Approx: 2*|AUC-0.5|.
    advantage = 2.0 * abs(auc - 0.5)
    return {"auc": auc, "advantage": advantage}


def run_one_seed(seed: int, epsilon: float = 1.0) -> dict:
    X_tr, y_tr, X_te, y_te = make_data(seed)

    # Path A: classical
    res_c = train_dp_sgd(
        X_tr, y_tr, X_te, y_te,
        epsilon=epsilon,
        noise_path="classical",
        qmirror_stream=None,
        qmirror_offset=[0],
        seed=seed,
    )
    mia_c = membership_inference_auc(
        res_c["train_loss_per_sample"], res_c["test_loss_per_sample"]
    )

    # Path B: qmirror — fresh stream each seed, offset by seed*8192 to decorrelate
    qstream = QmirrorByteStream(seed=12345, initial_bytes=8192)
    qoffset = [seed * 8192 % 4096]
    res_q = train_dp_sgd(
        X_tr, y_tr, X_te, y_te,
        epsilon=epsilon,
        noise_path="qmirror",
        qmirror_stream=qstream,
        qmirror_offset=qoffset,
        seed=seed,
    )
    mia_q = membership_inference_auc(
        res_q["train_loss_per_sample"], res_q["test_loss_per_sample"]
    )

    # Non-private baseline (no noise) for reference
    res_np = train_dp_sgd(
        X_tr, y_tr, X_te, y_te,
        epsilon=1e9,                  # ~ zero noise
        noise_path="classical",
        qmirror_stream=None,
        qmirror_offset=[0],
        seed=seed,
    )
    mia_np = membership_inference_auc(
        res_np["train_loss_per_sample"], res_np["test_loss_per_sample"]
    )

    return {
        "seed": seed,
        "epsilon": epsilon,
        "classical": {
            "train_acc": res_c["train_acc"],
            "test_acc": res_c["test_acc"],
            "mia_auc": mia_c["auc"],
            "mia_advantage": mia_c["advantage"],
            "w_norm": res_c["w_norm"],
        },
        "qmirror": {
            "train_acc": res_q["train_acc"],
            "test_acc": res_q["test_acc"],
            "mia_auc": mia_q["auc"],
            "mia_advantage": mia_q["advantage"],
            "w_norm": res_q["w_norm"],
        },
        "non_private_ref": {
            "train_acc": res_np["train_acc"],
            "test_acc": res_np["test_acc"],
            "mia_auc": mia_np["auc"],
            "mia_advantage": mia_np["advantage"],
        },
    }


def aggregate(seeds_results: list[dict]) -> dict:
    def mean_se(vs):
        a = np.array(vs, dtype=float)
        return float(a.mean()), float(a.std(ddof=1) / max(1, math.sqrt(len(a))))

    out = {}
    for path in ("classical", "qmirror", "non_private_ref"):
        accs = [r[path]["test_acc"] for r in seeds_results]
        train_accs = [r[path]["train_acc"] for r in seeds_results]
        aucs = [r[path]["mia_auc"] for r in seeds_results]
        adv = [r[path]["mia_advantage"] for r in seeds_results]
        ma, sa = mean_se(accs)
        mtra, stra = mean_se(train_accs)
        mu, su = mean_se(aucs)
        mad, sad = mean_se(adv)
        out[path] = {
            "test_acc_mean": ma, "test_acc_se": sa,
            "train_acc_mean": mtra, "train_acc_se": stra,
            "mia_auc_mean": mu, "mia_auc_se": su,
            "mia_advantage_mean": mad, "mia_advantage_se": sad,
        }
    # Paired diffs (qmirror - classical) per seed
    d_acc = np.array([r["qmirror"]["test_acc"] - r["classical"]["test_acc"]
                      for r in seeds_results])
    d_auc = np.array([r["qmirror"]["mia_auc"] - r["classical"]["mia_auc"]
                      for r in seeds_results])
    d_adv = np.array([r["qmirror"]["mia_advantage"] - r["classical"]["mia_advantage"]
                      for r in seeds_results])
    out["paired_diff_qmirror_minus_classical"] = {
        "test_acc_diff_mean": float(d_acc.mean()),
        "test_acc_diff_se": float(d_acc.std(ddof=1) / math.sqrt(len(d_acc))),
        "mia_auc_diff_mean": float(d_auc.mean()),
        "mia_auc_diff_se": float(d_auc.std(ddof=1) / math.sqrt(len(d_auc))),
        "mia_advantage_diff_mean": float(d_adv.mean()),
        "mia_advantage_diff_se": float(d_adv.std(ddof=1) / math.sqrt(len(d_adv))),
    }
    return out


def evaluate_falsifier(agg: dict) -> dict:
    """F-QDP-1: utility(qmirror) >= utility(classical) AND
                 privacy_bound(qmirror) <= privacy_bound(classical)
    Operationalised:
       utility       := test_acc_mean
       privacy_bound := mia_advantage_mean (lower = better privacy)
    Falsified if either inequality fails by > 1 SE.
    Confirmed (provisional) if both hold within 1 SE.
    Inconclusive otherwise.
    """
    qm_acc = agg["qmirror"]["test_acc_mean"]
    cl_acc = agg["classical"]["test_acc_mean"]
    qm_adv = agg["qmirror"]["mia_advantage_mean"]
    cl_adv = agg["classical"]["mia_advantage_mean"]
    diff = agg["paired_diff_qmirror_minus_classical"]

    # 1 SE on the paired difference
    util_diff_mean = diff["test_acc_diff_mean"]
    util_diff_se = diff["test_acc_diff_se"]
    priv_diff_mean = diff["mia_advantage_diff_mean"]
    priv_diff_se = diff["mia_advantage_diff_se"]

    # qmirror beats classical on utility iff util_diff > 0
    # qmirror beats classical on privacy iff priv_diff < 0 (lower advantage)
    # 1-SE 'significance' bands:
    util_lower = util_diff_mean - util_diff_se
    util_upper = util_diff_mean + util_diff_se
    priv_lower = priv_diff_mean - priv_diff_se
    priv_upper = priv_diff_mean + priv_diff_se

    util_better = util_diff_mean >= 0
    util_significant = util_lower > 0
    util_worse_significant = util_upper < 0

    priv_better = priv_diff_mean <= 0
    priv_significant = priv_upper < 0
    priv_worse_significant = priv_lower > 0

    if util_worse_significant or priv_worse_significant:
        verdict = "FALSIFIED"
        reason = []
        if util_worse_significant:
            reason.append(f"qmirror utility worse by {-util_diff_mean:.4f} ± {util_diff_se:.4f} (1 SE upper bound < 0)")
        if priv_worse_significant:
            reason.append(f"qmirror privacy worse: MIA advantage higher by {priv_diff_mean:.4f} ± {priv_diff_se:.4f} (1 SE lower bound > 0)")
        reason = "; ".join(reason)
    elif util_significant and priv_significant:
        verdict = "CONFIRMED_PROVISIONAL"
        reason = (f"qmirror utility +{util_diff_mean:.4f} ± {util_diff_se:.4f} "
                  f"AND privacy improved by {-priv_diff_mean:.4f} ± {priv_diff_se:.4f} "
                  "(both 1 SE-significant)")
    elif util_better and priv_better:
        verdict = "CONSISTENT_BUT_WEAK"
        reason = ("Both directions favor qmirror but neither is 1 SE-significant — "
                  "noise-dominated regime, more seeds needed")
    else:
        verdict = "INCONCLUSIVE"
        reason = (f"util_diff={util_diff_mean:+.4f}±{util_diff_se:.4f}, "
                  f"priv_diff={priv_diff_mean:+.4f}±{priv_diff_se:.4f}; "
                  "no consistent direction")

    return {
        "falsifier_id": "F-QDP-1",
        "verdict": verdict,
        "reason": reason,
        "criteria": {
            "utility_better_qmirror_minus_classical_test_acc": util_diff_mean,
            "utility_better_qmirror_minus_classical_test_acc_se": util_diff_se,
            "privacy_better_qmirror_minus_classical_mia_advantage": priv_diff_mean,
            "privacy_better_qmirror_minus_classical_mia_advantage_se": priv_diff_se,
        },
        "absolute_means": {
            "qmirror_test_acc": qm_acc,
            "classical_test_acc": cl_acc,
            "qmirror_mia_advantage": qm_adv,
            "classical_mia_advantage": cl_adv,
        },
    }


def main():
    t0 = time.monotonic()
    seeds = list(range(10))
    epsilon = 1.0
    print(f"[{time.strftime('%H:%M:%S')}] Running F-QDP-1: seeds={seeds} eps={epsilon}", flush=True)

    seed_results = []
    curve_points = []
    for s in seeds:
        r = run_one_seed(s, epsilon=epsilon)
        seed_results.append(r)
        curve_points.append({
            "seed": s,
            "epsilon": epsilon,
            "classical_test_acc": r["classical"]["test_acc"],
            "classical_mia_advantage": r["classical"]["mia_advantage"],
            "qmirror_test_acc": r["qmirror"]["test_acc"],
            "qmirror_mia_advantage": r["qmirror"]["mia_advantage"],
            "non_private_test_acc": r["non_private_ref"]["test_acc"],
            "non_private_mia_advantage": r["non_private_ref"]["mia_advantage"],
        })
        print(f"  seed={s}  classical: acc={r['classical']['test_acc']:.4f} "
              f"mia_adv={r['classical']['mia_advantage']:.4f}  "
              f"qmirror: acc={r['qmirror']['test_acc']:.4f} "
              f"mia_adv={r['qmirror']['mia_advantage']:.4f}", flush=True)

    agg = aggregate(seed_results)
    falsifier = evaluate_falsifier(agg)
    elapsed = time.monotonic() - t0

    verdict_doc = {
        "task": "qmirror_dp_noise_compare",
        "date": "2026-05-03",
        "falsifier": falsifier,
        "n_seeds": len(seeds),
        "epsilon": epsilon,
        "aggregate": agg,
        "elapsed_seconds": elapsed,
        "honest_caveats": [
            "qmirror MOCK source = Park-Miller LCG (seed=12345, a=1664525, c=1013904223, m=2^32). "
            "This is statistically uniform per the regression battery (qmirror_qrng_regression_2026_05_03/regression_summary.txt PARTIAL: PASS at n=1024, FAIL at n=8192 for lag-1 autocorr) but contains ZERO true entropy. "
            "True quantum entropy from ANU live source was not used in this run — the F-QDP-1 verdict therefore tests the inverse-CDF transform pipeline against torch's classical Laplace, not LCG vs true QRNG. "
            "Live ANU substitution is a one-line change (replace QmirrorByteStream with anu_fetch_bytes) but requires NEXUS_QMIRROR_ANU_KEY + ~10s rate-limited HTTPS per 8KB.",

            "Privacy bound is empirical (Yeom MIA loss-threshold AUC) not a formal (eps, delta)-DP accountant. Per-step epsilon=1.0 with 30*12=360 steps composes (under simple sequential composition) to eps_total=360 — i.e., NO meaningful end-to-end DP guarantee. The comparison is purely about whether QRNG-sourced noise is empirically equivalent to PRNG-sourced noise at fixed scale. RDP/PRV accounting + amplification-by-subsampling would be needed for a deployable bound.",

            "n=10 seeds is small; paired-difference SE bands are wide. A definitive utility/privacy ordering at fixed scale would require (a) ≥100 seeds, (b) cross-validated MIA threshold rather than AUC, (c) shadow-model MIA (Shokri 2017) which is the state-of-the-art empirical bound. The CONSISTENT_BUT_WEAK / INCONCLUSIVE band of the verdict reflects this small-sample regime by design.",
        ],
    }

    (OUT / "verdict.json").write_text(json.dumps(verdict_doc, indent=2))
    (OUT / "utility_privacy_curve.json").write_text(json.dumps({
        "epsilon": epsilon,
        "per_seed_points": curve_points,
        "aggregate": agg,
    }, indent=2))

    print("\n" + "=" * 72, flush=True)
    print(f"FALSIFIER F-QDP-1 verdict: {falsifier['verdict']}", flush=True)
    print(f"Reason: {falsifier['reason']}", flush=True)
    print("=" * 72, flush=True)
    print(f"\nutility (test_acc):  classical={agg['classical']['test_acc_mean']:.4f}±{agg['classical']['test_acc_se']:.4f}   qmirror={agg['qmirror']['test_acc_mean']:.4f}±{agg['qmirror']['test_acc_se']:.4f}   non-priv ref={agg['non_private_ref']['test_acc_mean']:.4f}", flush=True)
    print(f"privacy (mia_adv):   classical={agg['classical']['mia_advantage_mean']:.4f}±{agg['classical']['mia_advantage_se']:.4f}   qmirror={agg['qmirror']['mia_advantage_mean']:.4f}±{agg['qmirror']['mia_advantage_se']:.4f}   non-priv ref={agg['non_private_ref']['mia_advantage_mean']:.4f}", flush=True)
    print(f"paired diff (qm-cl): util={agg['paired_diff_qmirror_minus_classical']['test_acc_diff_mean']:+.4f}±{agg['paired_diff_qmirror_minus_classical']['test_acc_diff_se']:.4f}   mia_adv={agg['paired_diff_qmirror_minus_classical']['mia_advantage_diff_mean']:+.4f}±{agg['paired_diff_qmirror_minus_classical']['mia_advantage_diff_se']:.4f}", flush=True)
    print(f"\nelapsed: {elapsed:.1f}s", flush=True)
    print(f"outputs: {OUT}/verdict.json, {OUT}/utility_privacy_curve.json", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
