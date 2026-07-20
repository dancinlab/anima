"""Strict on-disk verifier for a promoted workspace-system release."""

from __future__ import annotations

import hashlib
import os

try:
    from .workspace_system_rho import run_workspace_system_rho
except ImportError:
    from workspace_system_rho import run_workspace_system_rho


def _sha256(path: str, limit: int | None = None) -> str:
    digest = hashlib.sha256()
    remaining = limit
    with open(path, "rb") as handle:
        while remaining is None or remaining > 0:
            size = 1024 * 1024 if remaining is None else min(1024 * 1024, remaining)
            chunk = handle.read(size)
            if not chunk:
                break
            digest.update(chunk)
            if remaining is not None:
                remaining -= len(chunk)
    if remaining is not None and remaining != 0:
        raise ValueError("file shorter than requested hash prefix: " + path)
    return digest.hexdigest()


def verify_workspace_release(candidate_path: str, base_path: str,
                             store_report: dict, realizer_report: dict) -> dict:
    candidate_size = os.path.getsize(candidate_path)
    base_size = os.path.getsize(base_path)
    candidate_sha = _sha256(candidate_path)
    base_sha = _sha256(base_path)
    candidate_prefix_sha = _sha256(candidate_path, base_size) if candidate_size >= base_size else ""
    checks = {
        "candidate_sha_matches_report": candidate_sha == store_report.get("candidate_sha256"),
        "base_sha_matches_store_report": base_sha == store_report.get("base_sha256"),
        "base_sha_matches_realizer_report": base_sha == realizer_report.get("ckpt_sha256"),
        "candidate_contains_base_prefix": candidate_size > base_size
        and candidate_prefix_sha == base_sha,
        "candidate_prefix_matches_report": candidate_prefix_sha
        == store_report.get("base_plus_slw_prefix_sha256"),
        "reported_prefix_parity": store_report.get("base_plus_slw_byte_parity") is True,
    }
    system = run_workspace_system_rho(store_report, realizer_report)
    verified = all(checks.values()) and system["reach_closed"]
    return {
        "schema": "anima.workspace-release-verification/v1",
        "candidate": os.path.abspath(candidate_path),
        "base": os.path.abspath(base_path),
        "candidate_size": candidate_size,
        "base_size": base_size,
        "candidate_sha256": candidate_sha,
        "base_sha256": base_sha,
        "candidate_prefix_sha256": candidate_prefix_sha,
        "checks": checks,
        "system_rho": system,
        "release_verified": verified,
    }


def format_workspace_release_verification(report: dict) -> str:
    lines = ["=== anima workspace release verification ==="]
    for name, passed in report["checks"].items():
        lines.append(("PASS " if passed else "FAIL ") + name)
    lines.append("SYSTEM_REACH_CLOSED=" + str(report["system_rho"]["reach_closed"]))
    lines.append("RELEASE_VERIFIED=" + str(report["release_verified"]))
    return "\n".join(lines)
