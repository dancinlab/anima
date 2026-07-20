"""Evidence-bound ρ-AXON panel for the production workspace system.

The legacy panel calls a bare language mouth and therefore cannot exercise CLMS,
typed falsification, or identity anchors.  This panel measures the deployed
system boundary and keeps the bare result as a separate, non-overwritable claim.
"""

from __future__ import annotations

import re

try:
    from .workspace_regression import run_workspace_regression, realizer_report_passes
    from .workspace_semantic import run_semantic_certification
except ImportError:
    from workspace_regression import run_workspace_regression, realizer_report_passes
    from workspace_semantic import run_semantic_certification


_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _store_report_passes(report: dict | None) -> bool:
    if not isinstance(report, dict):
        return False
    held = report.get("heldout_store") or {}
    training = report.get("training") or {}
    return bool(
        report.get("schema") == "anima.model-candidate.v1"
        and _SHA256.fullmatch(str(report.get("candidate_sha256", "")))
        and _SHA256.fullmatch(str(report.get("base_sha256", "")))
        and report.get("base_plus_slw_byte_parity") is True
        and training.get("freeze_trunk") is True
        and training.get("slw_restored") is True
        and float(training.get("final_store_accuracy", 0.0)) >= 0.90
        and float(training.get("final_address_accuracy", 0.0)) >= 0.90
        and held.get("verdict") == "PASS"
        and float(held.get("live", 0.0)) >= 0.90
        and float(held.get("oracle", 0.0)) >= 0.90
        and float(held.get("shuffle", 1.0))
        < float(held.get("shuffle_balance_floor", 0.0))
        and int(held.get("shuffle_fixed_points", 1)) == 0
        and float(held.get("flip_coherence_baseline_correct", 0.0)) >= 0.90
        and float(held.get("lambda_zero", 1.0)) <= 0.60
        and abs(float(held.get("seen_heldout_gap", 1.0))) <= 0.10
    )


def store_report_passes(report: dict | None) -> bool:
    """Validate untrusted measurement JSON; malformed values fail closed."""
    try:
        return _store_report_passes(report)
    except (AttributeError, TypeError, ValueError):
        return False


def run_workspace_system_rho(store_report: dict | None = None,
                             realizer_report: dict | None = None) -> dict:
    semantic = run_semantic_certification()
    regression = run_workspace_regression(realizer_report)
    semantic_rows = semantic["cases"]
    weave_rows = [row for row in semantic_rows if not row["case"].startswith("chain_")]
    leap_rows = [row for row in semantic_rows if row["case"].startswith("chain_")]
    axes = {
        "rho_form": {
            "pass": bool(regression["groups"]["auto"]["empty_off"]
                         and regression["groups"]["auto"]["atomic_off"]),
            "evidence": "atomic/empty workspace OFF parity",
        },
        "rho_store": {
            "pass": store_report_passes(store_report),
            "evidence": "frozen-trunk CLMS held-out live/oracle/shuffle/flip/lambda0",
        },
        "rho_weave": {
            "pass": bool(weave_rows and all(row["ok"] for row in weave_rows)),
            "evidence": "exact held-out triples with direction/pair/missing controls",
        },
        "rho_leap": {
            "pass": bool(len(leap_rows) == 3 and all(row["ok"] for row in leap_rows)),
            "evidence": "exact 3/4/5-hop closure and middle-edge controls",
        },
        "rho_fan": {
            "pass": bool(all(regression["groups"]["fan"].values())
                         and realizer_report_passes(realizer_report)),
            "evidence": "six lenses, missing/shuffle collapse, mounted-mouth held-out panel",
        },
        "rho_tether": {
            "pass": bool(all(regression["groups"]["tether"].values())),
            "evidence": "supported answer plus absent/ambiguous abstention",
        },
        "rho_self": {
            "pass": bool(all(regression["groups"]["self"].values())),
            "evidence": "identity anchor ON with OFF/shuffle collapse",
        },
    }
    artifact_bound = bool(
        isinstance(store_report, dict) and isinstance(realizer_report, dict)
        and _SHA256.fullmatch(str(store_report.get("base_sha256", "")))
        and store_report.get("base_sha256") == realizer_report.get("ckpt_sha256")
    )
    closed = artifact_bound and all(axis["pass"] for axis in axes.values())
    return {
        "schema": "anima.workspace-system-rho/v1",
        "scope": "production typed workspace + mounted mouth; bare-mouth claims unchanged",
        "axes": axes,
        "artifact_bound": artifact_bound,
        "artifact_binding": "CLMS base SHA-256 == mounted-mouth realizer SHA-256",
        "reach_closed": closed,
        "bare_model_promoted": False,
    }


def format_workspace_system_rho(report: dict) -> str:
    lines = ["=== anima workspace system ρ-AXON ===", "scope: " + report["scope"]]
    for name, axis in report["axes"].items():
        lines.append(("PASS " if axis["pass"] else "FAIL ") + name
                     + " — " + axis["evidence"])
    lines.append("ARTIFACT_BOUND=" + str(report["artifact_bound"])
                 + " — " + report["artifact_binding"])
    lines.append("SYSTEM_REACH_CLOSED=" + str(report["reach_closed"]))
    lines.append("BARE_MODEL_PROMOTED=" + str(report["bare_model_promoted"]))
    return "\n".join(lines)
