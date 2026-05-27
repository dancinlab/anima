"""V14 strict discriminability pre-check helper — cycle 2026-05-11 §74/§77/§78 follow-up.

V14 strict measurement 의 substrate-discriminability 가 ceiling-conditional 임이 확인됨
(§74 ceiling=15 LA-collapse). 이 helper 는 substrate run 전후의 cell_pool trajectory
divergence 측정 + threshold-based attractor-collapse 경고.

Usage (additive to run_max256.fire_substrate_engine_ag):

    from v14_discriminability_check import check_substrate_discriminability
    result = M.fire_substrate_engine_ag(sub_id, sub, log)
    discriminability = check_substrate_discriminability(
        substrate_id=sub_id,
        ckpt_path=sub["ckpt"],
        result=result,
        ceiling=current_ceiling,
        log_fn=log,
    )
    result["discriminability"] = discriminability
    if discriminability["warning"]:
        log(f"⚠️  WARN: V14 result may be attractor-collapsed (§77)")

Threshold values are empirically calibrated from cycle 2026-05-11 measurements.
Use this BEFORE trusting V14 verdict at non-default ceilings.
"""
from __future__ import annotations
import math
from typing import Dict, Any, List

# Empirical thresholds from cycle 2026-05-11
# Below these values → attractor collapse zone (V14 verdict unreliable)
DEFAULT_THRESHOLDS = {
    "min_early_phi_variance": 0.5,       # std of phi at turn 0,25,50
    "min_substrate_signature_divergence": 0.01,  # |trained_phi - reference_phi| / reference_phi
    "min_trained_random_separation_ratio": 1.1,  # trained_phi / max(random_phi)
}

# Known reference points (from REBORN §65-§78)
REFERENCE_TRAINED_PHI = {
    # Format: (substrate_lineage, ceiling) → trained_phi
    ("la_pretrain", 10.0): 1444.7,
    ("la_pretrain", 15.0): 1144.9186,    # collapse zone — same as B'
    ("la_pretrain", 20.0): 1562.4,
    ("la_pretrain", 1000.0): 49421.3,
    ("la_cotrain_bprime", 10.0): 1343.9,
    ("la_cotrain_bprime", 15.0): 1144.9186,  # collapse zone
    ("la_cotrain_bprime", 20.0): 1292.7,
    ("la_cotrain_bprime", 1000.0): 49855.0,
    ("lb_pretrain", 10.0): 1343.3,
    ("lb_pretrain", 15.0): 1234.4,
    ("lb_pretrain", 20.0): 1209.0,
    ("lb_pretrain", 1000.0): 42243.0,
    ("lb_cotrain_a", 10.0): 2412.1,
    ("lb_cotrain_a", 15.0): 3238.5,
    ("lb_cotrain_a", 20.0): 2514.2,
    ("lb_cotrain_a", 1000.0): 49736.3,
}

KNOWN_COLLAPSE_ZONES = [
    # (lineage_pair, ceiling) where collapse confirmed
    (("la_pretrain", "la_cotrain_bprime"), 15.0),  # §74
]


def check_substrate_discriminability(
    substrate_id: str,
    ckpt_path: str,
    result: Dict[str, Any],
    ceiling: float,
    log_fn=print,
    thresholds: Dict = None,
) -> Dict[str, Any]:
    """Check whether V14 strict result is in attractor collapse zone."""
    thresh = thresholds or DEFAULT_THRESHOLDS
    diag = {
        "substrate_id": substrate_id,
        "ceiling": ceiling,
        "warning": False,
        "reasons": [],
        "checks": {},
    }

    trained_phi = result.get("trained_phi")
    random_phi = result.get("random_phi", [])

    # Check 1: early-turn variance in trained trajectory
    snapshots = result.get("trained_run", {}).get("snapshots", [])
    if len(snapshots) >= 3:
        early_phis = [s.get("iit_phi_unnorm_b16", 0) for s in snapshots[:3]]
        early_var = (max(early_phis) - min(early_phis))
        diag["checks"]["early_phi_range"] = early_var
        if early_var < thresh["min_early_phi_variance"]:
            diag["warning"] = True
            diag["reasons"].append(f"early phi variance too low ({early_var:.4f} < {thresh['min_early_phi_variance']}) — substrate signal not differentiating in early turns")

    # Check 2: trained vs random separation
    if trained_phi and random_phi:
        max_random = max(random_phi)
        sep_ratio = trained_phi / max(max_random, 1e-6)
        diag["checks"]["trained_random_sep_ratio"] = sep_ratio
        if sep_ratio < thresh["min_trained_random_separation_ratio"]:
            diag["warning"] = True
            diag["reasons"].append(f"trained_random separation too small ({sep_ratio:.4f}× < {thresh['min_trained_random_separation_ratio']}×) — V14 may not discriminate")

    # Check 3: known collapse zone match
    for (lineage_pair, collapse_ceiling) in KNOWN_COLLAPSE_ZONES:
        if abs(ceiling - collapse_ceiling) < 0.1:
            diag["warning"] = True
            diag["reasons"].append(f"ceiling={ceiling} in known collapse zone for {lineage_pair} (§74)")
            break

    # Check 4: trained_phi matches known collapse-zone reference value
    if trained_phi:
        for (lineage, c), ref_phi in REFERENCE_TRAINED_PHI.items():
            if abs(ceiling - c) < 0.1 and abs(trained_phi - ref_phi) < 0.01:
                # Multiple substrates with same value → indicator of collapse
                same_value_lineages = [l for (l, c2), v in REFERENCE_TRAINED_PHI.items()
                                       if abs(c2 - ceiling) < 0.1 and abs(v - ref_phi) < 0.01]
                if len(same_value_lineages) > 1:
                    diag["warning"] = True
                    diag["reasons"].append(f"trained_phi {trained_phi:.4f} matches collapse-zone reference (lineages {same_value_lineages} converge to same attractor at ceiling={ceiling})")
                break

    if diag["warning"]:
        log_fn(f"⚠️  V14 discriminability warning for {substrate_id} @ ceiling={ceiling}:")
        for r in diag["reasons"]:
            log_fn(f"   - {r}")
        log_fn("   → V14 verdict may be attractor-collapsed; recommend cross-validation at different ceiling")
    return diag


if __name__ == "__main__":
    # smoke test with known collapse-zone values
    test_result = {
        "trained_phi": 1144.9186,
        "random_phi": [2245.7, 3550.1, 4629.7, 2923.8, 5238.4],
        "trained_run": {"snapshots": [
            {"iit_phi_unnorm_b16": 161.09},
            {"iit_phi_unnorm_b16": 1105.28},
            {"iit_phi_unnorm_b16": 833.17},
        ]},
    }
    diag = check_substrate_discriminability(
        substrate_id="B_prime_test", ckpt_path="dummy",
        result=test_result, ceiling=15.0,
    )
    import json
    print(json.dumps(diag, indent=2))
