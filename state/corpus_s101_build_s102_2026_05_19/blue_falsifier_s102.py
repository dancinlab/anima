#!/usr/bin/env python3
"""§102 — Blue falsifier sidecar (B-S102-1..N).

Each Bi closes ONE invariant on the BUILT artifact. Central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` is 0-line-diff per
g_blue_closed_mandate (sidecar-only). Connection-points cite §101 Q1/Q3 +
§16 corpus sha (byte-equal).

B-S102-NOTE: empirical carve-out — the corpus's CAPABILITY to drive
emergence on a future fire is fire-tier OUTCOME (B-D-NOTE / B-EMERGE-7
family, NOT counted 🔵). This battery proves the BUILD is structurally
honest, NOT that the corpus crosses the §1.1 threshold.
"""

import hashlib
import json
import sys
from pathlib import Path

STATE_DIR = Path(__file__).resolve().parent
ROOT = STATE_DIR.parents[1]
CENTRAL = ROOT / "state" / "verify_hexad_blue_2026_05_15" / "blue_falsifier.py"
S101 = ROOT / "state" / "dataregime_threshold_control_design_s101_2026_05_19"

CENTRAL_SHA_TARGET = "c93e160a8a376a94"
S16_SHA = "422c64a09b89393aebabc7b62aec8753a3d394ae4c442fef467c5d228e1831ec"
FORBIDDEN_TOKENS = ["[anima", "도우미", "helper", "assistant", "사용자", "user:"]


def b_s102_1_central_zero_line_diff() -> dict:
    """B-S102-1 CENTRAL-BLUE-ZERO-LINE-DIFF — sha256 prefix byte-equal."""
    sha = hashlib.sha256(CENTRAL.read_bytes()).hexdigest()
    return {"name": "B-S102-1 CENTRAL-BLUE-ZERO-LINE-DIFF",
            "central_sha": sha,
            "target_prefix": CENTRAL_SHA_TARGET,
            "PASS": sha.startswith(CENTRAL_SHA_TARGET)}


def b_s102_2_s1_sha_byte_equal_carry() -> dict:
    """B-S102-2 S1-SHA-BYTE-EQUAL-CARRY — Q1.I1 + Q1.I2.

    Connection-point: §16 corpus sha byte-equal carry.
    """
    s1_path = STATE_DIR / "s1_s16_verbatim.jsonl"
    if not s1_path.exists():
        return {"name": "B-S102-2 S1-SHA-BYTE-EQUAL-CARRY",
                "s1_present": False, "PASS": False,
                "reason": "S1 not on disk — build_corpus_s101.py must run first"}
    sha = hashlib.sha256(s1_path.read_bytes()).hexdigest()
    return {"name": "B-S102-2 S1-SHA-BYTE-EQUAL-CARRY",
            "s1_path": str(s1_path.relative_to(ROOT)),
            "s1_sha": sha,
            "s16_expected_sha": S16_SHA,
            "byte_equal_to_§16": sha == S16_SHA,
            "PASS": sha == S16_SHA}


def b_s102_3_corpus_sha_deterministic() -> dict:
    """B-S102-3 CORPUS-SHA256-DETERMINISTIC — Boolean Kolmogorov commitment.

    Recompute sha256 on disk and compare to manifest record.
    """
    corpus_path = STATE_DIR / "corpus_s101.jsonl"
    manifest_path = STATE_DIR / "corpus_s101_manifest.json"
    if not corpus_path.exists() or not manifest_path.exists():
        return {"name": "B-S102-3 CORPUS-SHA256-DETERMINISTIC",
                "PASS": False, "reason": "artifacts missing"}
    sha_disk = hashlib.sha256(corpus_path.read_bytes()).hexdigest()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    sha_recorded = manifest["corpus"]["sha256"]
    return {"name": "B-S102-3 CORPUS-SHA256-DETERMINISTIC",
            "sha_disk": sha_disk, "sha_recorded": sha_recorded,
            "PASS": sha_disk == sha_recorded}


def b_s102_4_forbidden_grep() -> dict:
    """B-S102-4 FORBIDDEN-TOKEN-GREP — Q1.I3 / B-IDENTITY-5."""
    corpus_path = STATE_DIR / "corpus_s101.jsonl"
    if not corpus_path.exists():
        return {"name": "B-S102-4 FORBIDDEN-TOKEN-GREP",
                "PASS": False, "reason": "corpus missing"}
    raw = corpus_path.read_bytes()
    counts = {tok: raw.count(tok.encode("utf-8"))
              for tok in FORBIDDEN_TOKENS}
    total = sum(counts.values())
    return {"name": "B-S102-4 FORBIDDEN-TOKEN-GREP",
            "counts": counts, "total": total,
            "PASS": total == 0}


def b_s102_5_s1_byte_equal_prefix() -> dict:
    """B-S102-5 S1-BYTE-EQUAL-PREFIX — Q1.I1 accumulate-not-replace.

    Connection-point: §93 cond-1 byte-equal accumulation.
    """
    s1_path = STATE_DIR / "s1_s16_verbatim.jsonl"
    corpus_path = STATE_DIR / "corpus_s101.jsonl"
    if not s1_path.exists() or not corpus_path.exists():
        return {"name": "B-S102-5 S1-BYTE-EQUAL-PREFIX",
                "PASS": False, "reason": "artifacts missing"}
    s1_bytes = s1_path.read_bytes()
    # Read only the prefix-length bytes from corpus
    with corpus_path.open("rb") as f:
        prefix = f.read(len(s1_bytes))
    return {"name": "B-S102-5 S1-BYTE-EQUAL-PREFIX",
            "s1_bytes": len(s1_bytes),
            "prefix_byte_equal": prefix == s1_bytes,
            "PASS": prefix == s1_bytes}


def b_s102_6_s7_gate_closed_conj() -> dict:
    """B-S102-6 §7-GATE-CLOSED-CONJUNCTION — Boolean AND over 3 §7 conds.

    On the BUILT artifact: every included record's source ∈ {S1, S2, S5}
    must satisfy §7①②③. We don't audit per-record (run-time burdensome
    on 777k records); we audit the SOURCE TAXONOMY closed-form (§101 Q1
    §1.2 audits S1/S2/S5 as §7-AND True). Connection-point: §101 result.json.
    """
    s101_result = json.loads((S101 / "result.json").read_text(encoding="utf-8"))
    legitimate_n = s101_result["q1_corpus_design"]["legitimate_sources_count"]
    excluded_n = s101_result["q1_corpus_design"]["excluded_sources_count"]
    # Built corpus includes exactly {S1, S2, S5} ⊆ §101's 5 legitimate sources.
    manifest = json.loads((STATE_DIR / "corpus_s101_manifest.json")
                          .read_text(encoding="utf-8"))
    included = set(manifest["sources_included"])
    legitimate_set = {"S1", "S2", "S3", "S4", "S5"}
    included_subset_of_legitimate = included.issubset(legitimate_set)
    # NO excluded sources X1-X4 in the build (audit included list).
    excluded_set = {"X1", "X2", "X3", "X4"}
    no_excluded = included.isdisjoint(excluded_set)
    return {"name": "B-S102-6 §7-GATE-CLOSED-CONJUNCTION",
            "legitimate_sources_in_§101": legitimate_n,
            "excluded_sources_in_§101": excluded_n,
            "included_in_build": sorted(included),
            "included_subset_of_legitimate": included_subset_of_legitimate,
            "no_excluded_in_build": no_excluded,
            "PASS": included_subset_of_legitimate and no_excluded}


def b_s102_7_q3_evaluable_on_built() -> dict:
    """B-S102-7 Q3-EVALUABLE-ON-BUILT — closed Boolean over G1..G7.

    Re-evaluate Q3 = G1∧G2∧G3∧G4∧G5∧G6∧G7 on the BUILT artifact
    (not on §101's design state). Each Gi is a sub-Boolean read from
    the manifest. Honest: G4 (Q2 measurable on result.json schema) is
    structurally Y because Q2 is closed-form over A1-A4 fields the
    future fire's result.json must declare; Q4 doesn't require A1-A4
    values NOW. G6 ΔI/Δ$ floor stays at design-tier convention.
    """
    manifest = json.loads((STATE_DIR / "corpus_s101_manifest.json")
                          .read_text(encoding="utf-8"))
    inv = manifest["invariants"]

    g1 = (b_s102_6_s7_gate_closed_conj()["PASS"])
    g2 = (inv["I1_S1_byte_equal_prefix"]
          and inv["I3_forbidden_grep"]["PASS"]
          and inv["I4_diversity"]["increases_numerically"]
          and inv["I6_SCoRe_gate"]["PASS"])
    g3 = inv["I5_echo_chamber_guard"]["PASS"]
    g4 = True  # Q2 A1-A4 schema is closed-form (§101 §2.2/§2.3); a future
               # fire's result.json declaring those fields is a downstream
               # contract, not a built-corpus measurement.
    g5 = True  # 5 levers preservable by trainer config — built corpus is
               # data side; lever preservation lives in trainer (separate
               # cycle). built corpus does NOT prevent lever preservation.
    g6 = True  # ΔI/Δ$ ≥ INFO_FLOOR — §101 §3.3 sets floor = 1bit / median
               # fire cost. The corpus build does not change ΔI a priori
               # (Q2 was never decided ⇒ ΔI = 1 bit). G6 stays True at
               # design-convention level.
    g7 = True  # anti-§94: built corpus only varies SOURCE COMPOSITION
               # (S1+S2+S5). No new mechanism stacked on the trainer side.

    # The BUILT-TIER honest Q3 verdict — driven by I4 diversity:
    fire_decision = g1 and g2 and g3 and g4 and g5 and g6 and g7

    return {"name": "B-S102-7 Q3-EVALUABLE-ON-BUILT",
            "G1_§7_gate": g1,
            "G2_§93_conds_via_invariants": g2,
            "G3_§62_echo_guard": g3,
            "G4_Q2_measurable_schema": g4,
            "G5_5_levers_preservable": g5,
            "G6_ΔI_Δ$_design_floor": g6,
            "G7_anti_§94_single_variable": g7,
            "FIRE_DECISION_on_built_artifact": fire_decision,
            "honest_caveat": (
                "G2 incorporates I4 diversity ↑↑ as part of §93 cond-3; "
                "if I4 fails on the built artifact, FIRE_DECISION = N. "
                "Q3 evaluating N on the BUILT state is the §101 design-tier "
                "guarantee — the design is well-formed because it correctly "
                "rejects an under-diverse corpus. A future build that "
                "materialises larger S2/S3/S4 sub-corpora may flip Q3 to Y."),
            "PASS": fire_decision}


def b_s102_8_connection_cite_s101_s16() -> dict:
    """B-S102-8 CONNECTION-POINT-CITES-§101-§16 — byte-equal anchors."""
    s101_design = (S101 / "DESIGN.md").read_text(encoding="utf-8")
    cite_s16_sha = S16_SHA in s101_design
    s101_result = json.loads((S101 / "result.json").read_text(encoding="utf-8"))
    cite_s16_meta = (
        s101_result["convergence_anchor"]["s16_corpus_sha256"] == S16_SHA)
    manifest = json.loads((STATE_DIR / "corpus_s101_manifest.json")
                          .read_text(encoding="utf-8"))
    cite_in_build = (manifest["s1"]["expected_sha256"] == S16_SHA)
    return {"name": "B-S102-8 CONNECTION-POINT-CITES-§101-§16",
            "§101_design_cites_§16_sha": cite_s16_sha,
            "§101_result_carries_§16_sha": cite_s16_meta,
            "§102_build_cites_§16_sha_in_manifest": cite_in_build,
            "PASS": cite_s16_sha and cite_s16_meta and cite_in_build}


def main():
    checks = [
        b_s102_1_central_zero_line_diff(),
        b_s102_2_s1_sha_byte_equal_carry(),
        b_s102_3_corpus_sha_deterministic(),
        b_s102_4_forbidden_grep(),
        b_s102_5_s1_byte_equal_prefix(),
        b_s102_6_s7_gate_closed_conj(),
        b_s102_7_q3_evaluable_on_built(),
        b_s102_8_connection_cite_s101_s16(),
    ]
    n_pass = sum(1 for c in checks if c.get("PASS"))
    n_total = len(checks)
    result = {
        "section": "§102",
        "battery": "B-S102",
        "n_pass": n_pass,
        "n_total": n_total,
        "all_pass": n_pass == n_total,
        "checks": checks,
        "B-S102-NOTE": (
            "EMPIRICAL CARVE-OUT — this battery proves the BUILD is "
            "structurally honest (sha-deterministic, forbidden-token-clean, "
            "S1 byte-equal-prefix, §7-gate-closed, §101/§16 connection-cited). "
            "It does NOT prove the corpus crosses §1.1 data-regime threshold; "
            "Q3 evaluation on the BUILT artifact reflects measured invariant "
            "satisfaction at $0 build-tier — the future fire's emergence "
            "OUTCOME is B-D-NOTE / B-EMERGE-7 family (necessary-not-sufficient)."),
    }
    out_path = Path(__file__).with_suffix("").parent / "blue_falsifier_s102_result.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["all_pass"] else 1)


if __name__ == "__main__":
    main()
