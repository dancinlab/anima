#!/usr/bin/env python3
"""BG-CAP-VS-TRAINING-RATIO-AUDIT — multi-factor regression / decision-tree.

Inputs:
- data_table.json (this directory)

Outputs:
- regression_result.json
"""
from __future__ import annotations
import json
import math
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr, kendalltau
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score

HERE = Path(__file__).resolve().parent

with open(HERE / "data_table.json") as fh:
    data = json.load(fh)

rows = data["rows"]


def encode_ratio(row, inf_substitute=1.0):
    """Substitute ratio for ∞ rows: training_observed_max=inf_substitute -> ratio=inference_cap/inf_substitute."""
    if row["ratio_inf_over_obs"] is not None:
        return row["ratio_inf_over_obs"]
    return row["inference_cap"] / inf_substitute


# Build features
def build_X_y(rows, inf_sub=1.0):
    X = []
    y = []
    for r in rows:
        ratio = encode_ratio(r, inf_substitute=inf_sub)
        X.append([
            ratio,                       # 0: ratio (cap-vs-training)
            r["inference_cap"],          # 1: inference_cap (continuous)
            r["chat_cotrain"],           # 2: chat-cotrain regime (binary)
            r["mitosis_aware"],          # 3: mitosis-aware paradigm (binary)
            r["params_M"],               # 4: model capacity in M params
            1 if r["schema"] == "engine_ag" else 0,  # 5: engine_ag schema (binary)
        ])
        y.append(r["verdict_score"])
    return np.array(X, dtype=float), np.array(y, dtype=int)


X, y = build_X_y(rows, inf_sub=1.0)
feature_names = [
    "ratio_cap_over_training_obs",
    "inference_cap",
    "chat_cotrain",
    "mitosis_aware",
    "params_M",
    "is_engine_ag",
]


# === Univariate correlations: ratio vs verdict ===
ratios = X[:, 0]
verdicts = y.astype(float)
sp_rho, sp_p = spearmanr(ratios, verdicts)
kd_tau, kd_p = kendalltau(ratios, verdicts)

# also test with inf_sub=10 (to mute ∞ -> 25.6x effect)
X10, _ = build_X_y(rows, inf_sub=10.0)
sp_rho10, sp_p10 = spearmanr(X10[:, 0], verdicts)

# inference_cap alone
cap_rho, cap_p = spearmanr(X[:, 1], verdicts)

# Threshold scan: find ratio threshold that best separates PASS (+1) from VIOLATED (-1)
# (ignore AMBIGUOUS=0 for binary threshold; collapse to PASS/non-PASS)
threshold_scan = []
for t in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 10.0, 50.0, 100.0]:
    pred_pass = (ratios > t).astype(int)
    actual_pass = (verdicts > 0).astype(int)
    actual_viol = (verdicts < 0).astype(int)
    # accuracy on pass-vs-non-pass
    acc_pass = (pred_pass == actual_pass).mean()
    # accuracy on pass-vs-violated only (ignore ambiguous)
    mask_decisive = (verdicts != 0)
    if mask_decisive.sum() > 0:
        acc_decisive = (pred_pass[mask_decisive] == actual_pass[mask_decisive]).mean()
    else:
        acc_decisive = float("nan")
    threshold_scan.append({
        "threshold": t,
        "n_pred_pass": int(pred_pass.sum()),
        "n_actual_pass": int(actual_pass.sum()),
        "acc_full_9": float(acc_pass),
        "acc_decisive_only": float(acc_decisive),
        "n_decisive": int(mask_decisive.sum()),
    })


# === Multinomial logistic regression: predict {-1,0,1} ===
# Standardize features
def zscore(M):
    mu = M.mean(axis=0)
    sd = M.std(axis=0)
    sd[sd == 0] = 1.0
    return (M - mu) / sd, mu, sd


Xz, mu, sd = zscore(X)
clf_lr = LogisticRegression(max_iter=2000, penalty="l2", C=10.0)
clf_lr.fit(Xz, y)
y_pred_lr = clf_lr.predict(Xz)
acc_lr = accuracy_score(y, y_pred_lr)

# coefficients per class
classes = clf_lr.classes_.tolist()
coefs_per_class = []
if clf_lr.coef_.shape[0] == 1:
    # binary case (shouldn't happen with 3 classes, but safe)
    coefs_per_class.append({"class": int(classes[0]), "coefs": dict(zip(feature_names, clf_lr.coef_[0].tolist()))})
else:
    for cls_idx, cls in enumerate(classes):
        coefs_per_class.append({
            "class": int(cls),
            "coefs": dict(zip(feature_names, clf_lr.coef_[cls_idx].tolist())),
            "intercept": float(clf_lr.intercept_[cls_idx]),
        })

# Approximate feature importance: max |coef| across classes per feature
feat_importance_lr = {}
for fi, fname in enumerate(feature_names):
    vals = [abs(clf_lr.coef_[cls_idx, fi]) for cls_idx in range(clf_lr.coef_.shape[0])]
    feat_importance_lr[fname] = max(vals)

# Sorted by importance
feat_importance_lr_sorted = sorted(feat_importance_lr.items(), key=lambda kv: -kv[1])


# === Decision tree (depth 2, 3) ===
trees = {}
for max_depth in (1, 2, 3):
    clf_dt = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    clf_dt.fit(X, y)
    y_pred_dt = clf_dt.predict(X)
    acc_dt = accuracy_score(y, y_pred_dt)
    fi_dt = dict(zip(feature_names, clf_dt.feature_importances_.tolist()))
    fi_dt_sorted = sorted(fi_dt.items(), key=lambda kv: -kv[1])
    tree_text = export_text(clf_dt, feature_names=feature_names)
    trees[f"depth_{max_depth}"] = {
        "accuracy_train": float(acc_dt),
        "feature_importances": fi_dt,
        "feature_importances_sorted": fi_dt_sorted,
        "tree_rules": tree_text,
        "predictions": y_pred_dt.tolist(),
        "n_correct": int((y_pred_dt == y).sum()),
        "n_total": int(len(y)),
    }


# === Per-row predictions table ===
per_row = []
for i, r in enumerate(rows):
    per_row.append({
        "id": r["id"],
        "ratio_used": float(ratios[i]),
        "verdict_actual": int(y[i]),
        "verdict_lr_pred": int(y_pred_lr[i]),
        "verdict_dt2_pred": int(trees["depth_2"]["predictions"][i]),
        "verdict_dt3_pred": int(trees["depth_3"]["predictions"][i]),
    })


# === Subset analyses ===
# Drop ∞-ratio rows and re-correlate (only finite-ratio: C/D)
finite_mask = np.array([r["ratio_inf_over_obs"] is not None for r in rows])
X_fin = X[finite_mask]
y_fin = y[finite_mask]
if finite_mask.sum() >= 3:
    fin_rho, fin_p = spearmanr(X_fin[:, 0], y_fin.astype(float))
    fin_kt, fin_kp = kendalltau(X_fin[:, 0], y_fin.astype(float))
else:
    fin_rho = fin_p = fin_kt = fin_kp = float("nan")

# Within-substrate cap polarity flip: for each substrate, polarity ordered by inf_cap
substrates = {}
for r in rows:
    substrates.setdefault(r["substrate"], []).append((r["inference_cap"], r["verdict_score"], r["section"]))

within_substrate_cap_flips = {}
for sub_id, lst in substrates.items():
    lst_sorted = sorted(lst, key=lambda x: x[0])
    within_substrate_cap_flips[sub_id] = [
        {"inference_cap": c, "verdict_score": v, "section": s} for c, v, s in lst_sorted
    ]


# === Falsifier evaluation ===
falsifier_evaluation = {
    "F-RATIO-1": {
        "predicate": "Spearman ratio-vs-verdict < 0.5 -> ratio insufficient",
        "spearman_rho_inf_sub_1": float(sp_rho),
        "spearman_p_inf_sub_1": float(sp_p),
        "spearman_rho_inf_sub_10": float(sp_rho10),
        "fired": bool(abs(sp_rho) < 0.5),
        "interpretation": ("ratio is INSUFFICIENT alone — Spearman < 0.5"
                           if abs(sp_rho) < 0.5
                           else "ratio is sufficient single predictor (Spearman >= 0.5)"),
    },
    "F-RATIO-2": {
        "predicate": "infinite-ratio rows show both PASS and VIOLATED -> ratio not driving",
        "inf_ratio_rows": [
            {"id": r["id"], "verdict": r["verdict"]}
            for r in rows if r["ratio_inf_over_obs"] is None
        ],
        "fired": True,
        "interpretation": (
            "B(VIOLATED), E_47(VIOLATED), A_38(STRICT_PASS), A_51(PASS), E_51(PASS) -- "
            "∞-ratio data shows BOTH polarities. Ratio alone cannot disambiguate."
        ),
    },
    "F-RATIO-3": {
        "predicate": "9 data points underpowered for stat decision",
        "n": int(len(rows)),
        "fired": True,
        "interpretation": (
            "n=9 is small; Spearman/Kendall p>0.05 typical, multi-factor LR/DT have "
            "near-saturation accuracy -> overfit risk."
        ),
    },
}


# === Compose result ===
result = {
    "schema": "bg_cap_vs_training_ratio_audit/regression/v1",
    "n_rows": len(rows),
    "feature_names": feature_names,
    "univariate_correlations": {
        "ratio_inf_sub_1_vs_verdict": {
            "spearman_rho": float(sp_rho), "spearman_p": float(sp_p),
            "kendall_tau": float(kd_tau), "kendall_p": float(kd_p),
        },
        "ratio_inf_sub_10_vs_verdict": {
            "spearman_rho": float(sp_rho10), "spearman_p": float(sp_p10),
        },
        "inference_cap_vs_verdict": {
            "spearman_rho": float(cap_rho), "spearman_p": float(cap_p),
        },
        "ratio_finite_only_vs_verdict (n=3, C/D rows only)": {
            "n": int(finite_mask.sum()),
            "spearman_rho": float(fin_rho) if not math.isnan(fin_rho) else None,
            "spearman_p": float(fin_p) if not math.isnan(fin_p) else None,
            "kendall_tau": float(fin_kt) if not math.isnan(fin_kt) else None,
        },
    },
    "threshold_scan_ratio": threshold_scan,
    "logistic_regression": {
        "classes": classes,
        "feature_means": dict(zip(feature_names, mu.tolist())),
        "feature_stds": dict(zip(feature_names, sd.tolist())),
        "coefficients_per_class": coefs_per_class,
        "feature_importance_max_abs_coef": feat_importance_lr,
        "feature_importance_sorted": feat_importance_lr_sorted,
        "accuracy_train": float(acc_lr),
        "predictions": y_pred_lr.tolist(),
        "n_correct": int((y_pred_lr == y).sum()),
        "n_total": int(len(y)),
    },
    "decision_trees": trees,
    "per_row_predictions": per_row,
    "within_substrate_cap_polarity_flips": within_substrate_cap_flips,
    "falsifier_evaluation": falsifier_evaluation,
}

with open(HERE / "regression_result.json", "w") as fh:
    json.dump(result, fh, indent=2)

print("=== summary ===")
print(f"n_rows = {len(rows)}")
print(f"Spearman(ratio vs verdict, ∞→1):  rho={sp_rho:.3f}, p={sp_p:.3f}")
print(f"Spearman(ratio vs verdict, ∞→10): rho={sp_rho10:.3f}, p={sp_p10:.3f}")
print(f"Spearman(inference_cap vs verdict): rho={cap_rho:.3f}, p={cap_p:.3f}")
print(f"Logistic regression train accuracy = {acc_lr:.3f} ({(y_pred_lr == y).sum()}/{len(y)})")
print(f"Decision tree depth=1 acc = {trees['depth_1']['accuracy_train']:.3f}")
print(f"Decision tree depth=2 acc = {trees['depth_2']['accuracy_train']:.3f}")
print(f"Decision tree depth=3 acc = {trees['depth_3']['accuracy_train']:.3f}")
print()
print("LR feature importance (|coef|, std features):")
for fname, val in feat_importance_lr_sorted:
    print(f"  {fname:35s} {val:.3f}")
print()
print("DT depth=2 feature importance:")
for fname, val in trees["depth_2"]["feature_importances_sorted"]:
    print(f"  {fname:35s} {val:.3f}")
print()
print("DT depth=2 rules:")
print(trees["depth_2"]["tree_rules"])
print()
print("Threshold scan (ratio):")
for ts in threshold_scan:
    print(f"  t={ts['threshold']:>6.1f}  n_pred_pass={ts['n_pred_pass']}  acc_full={ts['acc_full_9']:.2f}  acc_decisive={ts['acc_decisive_only']:.2f}")
