#!/usr/bin/env python3
"""§102 — Build CORPUS_S101 per §101 Q1.

CORPUS_S101 := byte_concat(S1 §16-verbatim, S2 Ψ-framings, S3* omitted,
                            S4* omitted, S5 anchor-expansion)

S3 and S4 are OMITTED honestly:
  - S3 dual-anima requires §36 echo-guard pre-check (Q1.I5). §36 stub passed,
    but §62 ECHO-COLLAPSE at trained scale = honest blocker. Full §36 pre-check
    against §16-class trained ckpt requires model.forward (NOT $0 build-tier).
    → OMIT S3 (Q1.I5 cannot be satisfied at $0 build-tier).
  - S4 action-perception requires §93 SCoRe 2-stage trained corrector (Q1.I6).
    §91 measured β ECHO-DOMINATES-AT-TRAINED; §92 reframed as training-time
    objective (NOT corpus material). → OMIT S4 (Q1.I6 cannot be satisfied at
    $0 build-tier; S4 is a trainer-level objective, not a corpus source).

S1 is re-generated from §16 generator (deterministic seed 1337). sha256
expected `422c64a09b89393aebabc7b62aec8753a3d394ae4c442fef467c5d228e1831ec`
per Q1.I1 + Q1.I2. We BYTE-CONCAT not re-shuffle (S1 stays a verbatim prefix).

S2 = §16 anchor SSOT × Ψ-physics framing variations (anima OWN Law-71
fields: vacuum_psi/basin_radius/category/top_emotion + deterministic frames).
Each S2 record = a NEW carving body for an existing §16 anchor, framed in a
distinct Ψ-region of the same anchor neighborhood. Diversity coefficient is
measured BEFORE-and-AFTER S2 inclusion (Q1.I4).

S5 = ANIMA-OWN .kosmos anchor coordinates (HEXAD/UNIVERSE-BRAIN-MAP/anchors/),
re-emitted as `<inner_carve>` records with the anchor's vacuum_psi /
basin_radius / category / top_emotion fields preserved. We DO NOT include the
raw .kosmos text payload because it begins with `[anima` (= a B-IDENTITY-5
forbidden token in chat-bleed audit). S5 is anchor-position expansion not
text re-injection.

g3: build ≠ fire ≠ emergence. The corpus is a SCAFFOLD for a future fire.
Q3 re-evaluation on the BUILT artifact is in BUILD.md / result.json.
"""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
S16_GEN = ROOT / "state" / "carving_dataregime_s16_2026_05_18" / "corpus_carving_s16_generator.py"
KOSMOS_DIR = ROOT / "HEXAD" / "UNIVERSE-BRAIN-MAP" / "anchors"

S1_EXPECTED_SHA = "422c64a09b89393aebabc7b62aec8753a3d394ae4c442fef467c5d228e1831ec"
S1_EXPECTED_RECORDS = 777_000
S1_EXPECTED_BYTES = 603_032_014

FORBIDDEN_TOKENS = ["[anima", "도우미", "helper", "assistant", "사용자", "user:"]
# external-grep proxies (Q1.I7): obvious external-LLM call surfaces in the
# corpus body itself. Records are JSON lines; this checks for any signal a
# record provenance left anima's substrate. NOT exhaustive — see honest C3.
EXTERNAL_PROVENANCE_TOKENS = [
    "openai.com", "anthropic.com", "huggingface.co/", "wikipedia.org",
    "commoncrawl", "https://", "http://",
]


def regenerate_s1(out_path: Path, n: int, seed: int) -> dict:
    """Re-generate S1 (= §16 corpus) by invoking the §16 generator."""
    if not S16_GEN.exists():
        raise SystemExit(f"FATAL: §16 generator missing at {S16_GEN}")
    cmd = [sys.executable, str(S16_GEN), "--out", str(out_path),
           "--n", str(n), "--seed", str(seed)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write(res.stdout + "\n" + res.stderr + "\n")
        raise SystemExit("FATAL: §16 generator failed")
    sha = hashlib.sha256(out_path.read_bytes()).hexdigest()
    return {"sha256": sha, "records": sum(1 for _ in out_path.open()),
            "bytes": out_path.stat().st_size}


# ── S2 Ψ-framing generator ─────────────────────────────────────────
# We import the §16 generator's anchor SSOT directly. Each S2 record is a
# carving body framed in a distinct Ψ-region for the SAME anchor.
sys.path.insert(0, str(S16_GEN.parent))
import corpus_carving_s16_generator as s16_gen  # noqa: E402

KNUTH_ANCHORS = s16_gen.KNUTH_ANCHORS  # 168 anchors, byte-identical SSOT


def _psi_frame(psi_x: float, psi_y: float, basin: float, frame_idx: int) -> str:
    """Deterministic Ψ-framing phrase. NO external LLM, NO RNG — pure fn of
    Ψ-coordinate and frame index. 5 framings × 168 anchors = 840 S2 records.

    Frames sweep the (psi_x, psi_y, basin) state space deterministically.
    """
    if frame_idx == 0:
        return ("Ψ-deviation framing: |ψ − ψ_vac| × basin = "
                f"{abs(psi_x - 0.5) * basin:.4f} — basin-edge approach signal.")
    if frame_idx == 1:
        return ("tension framing: Engine A⇄G cross-product near "
                f"(ψ_x={psi_x:.3f}, ψ_y={psi_y:.3f}) — restoring-sign in "
                "carving-form span.")
    if frame_idx == 2:
        return ("Φ-context framing: cell-pool partial-trace projection onto "
                f"anchor neighborhood r={basin:.3f} — IIT-axiom-bounded "
                "partial-Φ.")
    if frame_idx == 3:
        return ("controller framing: state-derived statistic τ_ema + λ·τ_std "
                f"at ψ=({psi_x:.3f}, {psi_y:.3f}) — §75-FIRE A-only lever "
                "trace.")
    return ("set-point framing: SAPIN error E = ‖ψ − ½‖² + ‖τ − τ*‖² + "
            f"‖Φ − Φ*‖² at basin r={basin:.3f} — §86 unified drive form.")


def build_s2(seed: int) -> list[dict]:
    """S2 = §16 anchor SSOT × 5 Ψ-framings (deterministic, no RNG)."""
    out = []
    for tier, name, dom, emotion, score, vac, basin in KNUTH_ANCHORS:
        for fi in range(5):
            body = _psi_frame(vac[0], vac[1], basin, fi)
            rec = {
                "source": "S2",
                "anchor_tier": tier,
                "anchor_name": name,
                "domain": dom,
                "top_emotion": emotion,
                "vacuum_psi": list(vac),
                "basin_radius": basin,
                "carving_form": "alpha",
                "frame_idx": fi,
                "body": body,
            }
            out.append(rec)
    return out


# ── S5 anchor-expansion ────────────────────────────────────────────
def build_s5() -> list[dict]:
    """S5 = ANIMA-OWN .kosmos anchor coordinates re-emitted as records.

    We do NOT include the raw .kosmos text payload (it starts with `[anima`
    = B-IDENTITY-5 forbidden token). S5 is COORDINATE expansion.
    """
    out = []
    if not KOSMOS_DIR.exists():
        return out
    for kf in sorted(KOSMOS_DIR.glob("*.kosmos")):
        raw = kf.read_text(encoding="utf-8", errors="replace")
        # Extract carving fields by regex (deterministic, no LLM).
        def _get(pat):
            m = re.search(pat, raw)
            return m.group(1) if m else None
        tier = _get(r"knuth_tier\s*=\s*(\d+)")
        category = _get(r"category\s*=\s*\"([^\"]+)\"")
        emotion = _get(r"top_emotion\s*=\s*\"([^\"]+)\"")
        coord_m = re.search(r"coord\s*=\s*\[([^,]+),\s*([^\]]+)\]", raw)
        lane = _get(r"lane\s*=\s*\"([^\"]+)\"")
        radius_m = re.search(r"radius\s*=\s*([0-9.]+)", raw)
        if tier and coord_m and radius_m:
            rec = {
                "source": "S5",
                "anchor_file": kf.name,
                "anchor_tier": int(tier),
                "category": category,
                "top_emotion": emotion,
                "vacuum_psi": [float(coord_m.group(1)),
                               float(coord_m.group(2))],
                "lane": lane,
                "basin_radius": float(radius_m.group(1)),
                "carving_form": "alpha",
                "body": (f"anchor knuth_{int(tier):03d} category={category} "
                         f"emotion={emotion} ψ=({coord_m.group(1).strip()},"
                         f"{coord_m.group(2).strip()}) basin"
                         f"={radius_m.group(1)} lane={lane}"),
            }
            out.append(rec)
    return out


# ── Diversity coefficient ──────────────────────────────────────────
def diversity_coeff(byte_stream: bytes, sample_n: int = 5_000_000) -> dict:
    """Q1.I4 — diversity coefficient measured as inverse Herfindahl
    concentration over 4-gram byte distribution. Higher = more diverse.

    HHI = sum(p_i^2) over 4-gram p; diversity = 1/HHI (= effective number
    of equally-frequent 4-grams). Sample first `sample_n` bytes for tractability.
    """
    sample = byte_stream[:sample_n]
    if len(sample) < 4:
        return {"n_sampled": len(sample), "distinct_4grams": 0,
                "hhi": 0.0, "diversity": 0.0}
    c = Counter()
    for i in range(len(sample) - 3):
        c[bytes(sample[i:i+4])] += 1
    total = sum(c.values())
    hhi = sum((cnt / total) ** 2 for cnt in c.values()) if total else 0.0
    return {
        "n_sampled": len(sample),
        "distinct_4grams": len(c),
        "hhi": hhi,
        "diversity": (1.0 / hhi) if hhi > 0 else 0.0,
    }


def forbidden_grep(byte_stream: bytes) -> dict:
    """Q1.I3 — forbidden-token grep over the 6 B-IDENTITY-5 tokens."""
    out = {}
    for tok in FORBIDDEN_TOKENS:
        # Both UTF-8 byte search; raw bytes for ASCII tokens, encode for Hangul.
        b = tok.encode("utf-8")
        out[tok] = byte_stream.count(b)
    return out


def external_grep(byte_stream: bytes) -> dict:
    """Q1.I7 — external-provenance proxy grep. NOT exhaustive (see C3)."""
    return {tok: byte_stream.count(tok.encode("utf-8"))
            for tok in EXTERNAL_PROVENANCE_TOKENS}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--s1-n", type=int, default=777_000)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--skip-s1", action="store_true",
                    help="reuse existing s1 corpus if already on disk")
    args = ap.parse_args()

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    s1_path = out_dir / "s1_s16_verbatim.jsonl"
    corpus_path = out_dir / "corpus_s101.jsonl"

    # ── S1: §16 verbatim ──
    if args.skip_s1 and s1_path.exists():
        s1_stat = {
            "sha256": hashlib.sha256(s1_path.read_bytes()).hexdigest(),
            "records": sum(1 for _ in s1_path.open()),
            "bytes": s1_path.stat().st_size,
        }
    else:
        sys.stderr.write(f"[§102] regenerating S1 → {s1_path} ...\n")
        s1_stat = regenerate_s1(s1_path, args.s1_n, args.seed)
    sys.stderr.write(
        f"[§102] S1 sha256={s1_stat['sha256']} bytes={s1_stat['bytes']} "
        f"records={s1_stat['records']}\n")

    # Q1.I2: hash(S1) must equal expected §16 sha
    s1_sha_match = s1_stat["sha256"] == S1_EXPECTED_SHA
    if not s1_sha_match:
        sys.stderr.write(
            f"[§102] WARNING: S1 sha mismatch — got {s1_stat['sha256']} "
            f"expected {S1_EXPECTED_SHA}. Q1.I2 will FAIL.\n")

    # ── S2: Ψ-framings ──
    s2 = build_s2(args.seed)
    sys.stderr.write(f"[§102] S2 records={len(s2)}\n")

    # ── S5: anchor expansion ──
    s5 = build_s5()
    sys.stderr.write(f"[§102] S5 records={len(s5)}\n")

    # ── ASSEMBLE: byte_concat(S1, S2, S5) — S3/S4 omitted honestly ──
    # Per Q1 §1.3, byte_concat means S1 is a verbatim PREFIX. We append
    # S2 and S5 as JSONL after S1 (preserving I1 accumulate-not-replace).
    s1_bytes = s1_path.read_bytes()
    s2_bytes = b"".join(
        (json.dumps(r, ensure_ascii=False) + "\n").encode("utf-8") for r in s2)
    s5_bytes = b"".join(
        (json.dumps(r, ensure_ascii=False) + "\n").encode("utf-8") for r in s5)
    corpus_bytes = s1_bytes + s2_bytes + s5_bytes
    corpus_path.write_bytes(corpus_bytes)

    # I1 byte-equal prefix check (S1 ⊂ CORPUS as prefix).
    s1_prefix_byte_equal = corpus_bytes[:len(s1_bytes)] == s1_bytes
    corpus_sha = hashlib.sha256(corpus_bytes).hexdigest()
    sys.stderr.write(
        f"[§102] CORPUS_S101 sha256={corpus_sha} bytes={len(corpus_bytes)} "
        f"records={s1_stat['records'] + len(s2) + len(s5)}\n")

    # I3 forbidden-token grep
    f_grep_s1 = forbidden_grep(s1_bytes)
    f_grep_corpus = forbidden_grep(corpus_bytes)
    forbidden_total = sum(f_grep_corpus.values())

    # I4 diversity coefficient: S1-only vs CORPUS
    s1_div = diversity_coeff(s1_bytes)
    corpus_div = diversity_coeff(corpus_bytes)
    diversity_increases = corpus_div["diversity"] > s1_div["diversity"]
    # ↑↑ requires meaningfully greater, not just numerically. Set 1.05× floor.
    diversity_double_arrow = (corpus_div["diversity"] >=
                              1.05 * s1_div["diversity"])

    # I5 echo-chamber guard: S3 was OMITTED → trivially PASS (no S3 records
    # to fail the guard on). Honest: this is not a §36 content-dep test on
    # actual trained-cell traces; it is the omission-as-honesty path.
    echo_guard_pass = True
    echo_guard_reason = ("S3 OMITTED — no dual-anima loop traces included; "
                         "§36 trained-scale pre-check requires model.forward "
                         "(out of $0 build scope). Q1.I5 PASSED VACUOUSLY "
                         "by omission, not by demonstration.")

    # I6 SCoRe-gate: S4 OMITTED → trivially PASS.
    score_gate_pass = True
    score_gate_reason = ("S4 OMITTED — action-perception is a trainer "
                         "objective per §92, NOT corpus material. Q1.I6 "
                         "PASSED VACUOUSLY by omission, not by demonstration.")

    # I7 external-source grep
    ext_grep = external_grep(corpus_bytes)
    external_total = sum(ext_grep.values())
    # honest: S1 has some https:// references in carving texts? Check.
    ext_grep_s1 = external_grep(s1_bytes)

    # Assemble manifest
    manifest = {
        "section": "§102",
        "title": "CORPUS_S101 build — §101 Q1 corpus assembly",
        "date": "2026-05-19",
        "tier": "BUILD-TIER ($0, NO GPU, NO fire)",
        "spec": "§101 Q1 (state/dataregime_threshold_control_design_s101_2026_05_19/)",
        "central_blue_sha_prefix_target": "c93e160a8a376a94",
        "sources_included": ["S1", "S2", "S5"],
        "sources_omitted": {
            "S3": ("dual-anima loop traces — §36 content-dep guard "
                   "(Q1.I5) requires trained-cell model.forward, "
                   "out of $0 build scope; §62 echo collapse at "
                   "trained scale is honest blocker."),
            "S4": ("action-perception loop records — §93 SCoRe-gated "
                   "(Q1.I6) requires trained 2-stage corrector; "
                   "§91 β ECHO-DOMINATES-AT-TRAINED; §92 reframed "
                   "as TRAINING OBJECTIVE not corpus material."),
        },
        "s1": {
            **s1_stat,
            "expected_sha256": S1_EXPECTED_SHA,
            "sha_byte_equal_to_expected": s1_sha_match,
        },
        "s2": {
            "records": len(s2),
            "framings_per_anchor": 5,
            "anchors": len(KNUTH_ANCHORS),
        },
        "s5": {
            "records": len(s5),
            "anchor_files": [
                str(p.relative_to(ROOT)) for p in sorted(KOSMOS_DIR.glob("*.kosmos"))
            ],
        },
        "corpus": {
            "path": str(corpus_path.relative_to(ROOT)),
            "sha256": corpus_sha,
            "bytes": len(corpus_bytes),
            "records": s1_stat["records"] + len(s2) + len(s5),
        },
        "invariants": {
            "I1_S1_byte_equal_prefix": s1_prefix_byte_equal,
            "I2_S1_sha_matches_expected": s1_sha_match,
            "I3_forbidden_grep": {
                "tokens": f_grep_corpus,
                "total": forbidden_total,
                "PASS": forbidden_total == 0,
            },
            "I4_diversity": {
                "s1_only_diversity_eff_4grams": s1_div["diversity"],
                "corpus_diversity_eff_4grams": corpus_div["diversity"],
                "ratio_corpus_over_s1": (
                    corpus_div["diversity"] / s1_div["diversity"]
                    if s1_div["diversity"] > 0 else 0.0),
                "increases_numerically": diversity_increases,
                "increases_double_arrow_1p05x": diversity_double_arrow,
                "sample_n_bytes": s1_div["n_sampled"],
                "s1_distinct_4grams": s1_div["distinct_4grams"],
                "corpus_distinct_4grams": corpus_div["distinct_4grams"],
                "PASS_strict": diversity_double_arrow,
            },
            "I5_echo_chamber_guard": {
                "S3_omitted": True,
                "vacuous_pass_via_omission": True,
                "reason": echo_guard_reason,
                "PASS": echo_guard_pass,
            },
            "I6_SCoRe_gate": {
                "S4_omitted": True,
                "vacuous_pass_via_omission": True,
                "reason": score_gate_reason,
                "PASS": score_gate_pass,
            },
            "I7_external_grep": {
                "corpus": ext_grep,
                "s1_only": ext_grep_s1,
                "corpus_total": external_total,
                "PASS": external_total == 0,
                "honest_caveat": (
                    "external-grep is a proxy over 7 surface tokens; "
                    "exhaustive provenance audit requires source-attribution "
                    "tracking, NOT in $0 build scope. §16 generator is "
                    "anima-OWN substrate, S2 uses anima Ψ-fields only, S5 "
                    "uses anima-OWN .kosmos files. NO external API calls in "
                    "build_corpus_s101.py (audit-grep this file)."),
            },
        },
    }

    manifest_path = out_dir / "corpus_s101_manifest.json"
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    sys.stderr.write(f"[§102] manifest → {manifest_path}\n")
    sys.stderr.write(f"[§102] corpus → {corpus_path}\n")


if __name__ == "__main__":
    main()
