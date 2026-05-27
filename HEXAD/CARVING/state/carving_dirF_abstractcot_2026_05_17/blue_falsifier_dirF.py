#!/usr/bin/env python3
"""Dir-F ABSTRACT-COT closed-form falsifier battery (2026-05-17).
g_multidirectional_explore parallel direction F.

The Dir-F CLOSED side is the reserved-vocab discreteness of the abstract-CoT
reasoning surface — a finite, deterministic, set-membership property of the
corpus that is PROVABLE without any SGD outcome (g3 transfer-form 🔵). The
SGD convergence + the Dir-F vs UBM-E7 α JOINT comparison are EMPIRICAL
(B-CARVE-E6-NOTE / B-D-NOTE family, NOT closed — honest carve-out).

  F-DIRF-CORPUS-1  SHA256-DETERMINISTIC-CLOSED
      seed-fixed 256-bit commitment over the generated corpus byte stream
      (Kolmogorov determinism). re-running the seed-fixed generator yields a
      byte-identical corpus → identical sha256. Boolean 256-bit equality.

  F-DIRF-CORPUS-2  NO-CHAT-SFT-CONTAMINATION-CLOSED
      Boolean set algebra over the byte stream: grep of the forbidden
      role-label set {[anima, 도우미, helper, assistant, 사용자, user:}
      → total count == 0 (B-IDENTITY-5 + forbidden_chat_sft_use). f3 safe.

  F-DIRF-CORPUS-3  RESERVED-VOCAB-CLOSED
      The abstract-CoT discreteness invariant (the Dir-F-specific closed
      property, arxiv 2604.22709). Three conjoined sub-claims:
        (a) every reserved block's tokens ∈ the fixed 56-symbol alphabet
            Σ = {R0..R3, T0..T9, C00..C16, E00..E17, V0..V3, Ore/Ofz/Onv}
            (closed finite set membership);
        (b) zero natural-language byte inside any ⟪ ⟫ span (the alphabet's
            character set is the only permitted byte set — discreteness);
        (c) integer cardinality conservation: exactly one reserved block
            per record (|reserved blocks| == |records|, and each block
            wrapped in exactly one ⟪ ⟫ pair).
      All three are Boolean/integer predicates over the byte stream — NO
      SGD, NO model forward. This is the closed-form side of Dir-F.

f1/f2 SAFE: |Σ|=56 is the reserved-alphabet cardinality (a Kolmogorov byte
count over an internal corpus-design artefact), NOT a σ/τ/φ/J₂ lattice
derivation and NOT a claim about any external entity.
"""
import json
import sys
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from corpus_carving_generator_dirF import (  # noqa: E402
    RESERVED_ALPHABET, RV_OPEN, RV_CLOSE, audit_reserved_blocks, build_corpus,
)

CORPUS = HERE / "corpus_carving_dirF.jsonl"
STATS = HERE / "corpus_carving_dirF.stats.json"
SEED = 1337


def f_dirf_corpus_1():
    """SHA256-DETERMINISTIC-CLOSED — re-derive the seed-fixed corpus and
    confirm a byte-identical sha256 (256-bit Boolean equality)."""
    stats = json.loads(STATS.read_text())
    recorded = stats["sha256"]
    # re-build with the same seed + record count, serialise the same way.
    recs = build_corpus(stats["records"], SEED)
    buf = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recs)
    redrived = hashlib.sha256(buf.encode("utf-8")).hexdigest()
    on_disk = hashlib.sha256(CORPUS.read_bytes()).hexdigest()
    ok = (recorded == on_disk == redrived)
    return ok, {"recorded": recorded, "on_disk": on_disk,
                "rederived": redrived, "equal_256bit": ok}


def f_dirf_corpus_2():
    """NO-CHAT-SFT-CONTAMINATION-CLOSED — Boolean set algebra grep == 0."""
    raw = CORPUS.read_text(encoding="utf-8")
    forbidden = ["[anima", "도우미", "helper", "assistant", "사용자", "user:"]
    counts = {t: raw.count(t) for t in forbidden}
    total = sum(counts.values())
    ok = (total == 0)
    return ok, {"forbidden_counts": counts, "total": total,
                "contamination_free": ok}


def f_dirf_corpus_3():
    """RESERVED-VOCAB-CLOSED — alphabet membership + discreteness +
    cardinality conservation (3 conjoined Boolean/integer predicates)."""
    recs = [json.loads(l) for l in CORPUS.read_text(
        encoding="utf-8").splitlines() if l.strip()]
    a = audit_reserved_blocks(recs)
    sub_a = (a["bad_token_total"] == 0)              # alphabet membership
    sub_b = (a["nl_byte_in_span"] == 0)              # discreteness (no NL)
    sub_c = (a["cardinality_conserved"]              # 1 block / record
             and a["n_reserved_blocks"] == len(recs))
    ok = sub_a and sub_b and sub_c and a["reserved_vocab_closed"]
    return ok, {"alphabet_size": len(RESERVED_ALPHABET),
                "sub_a_alphabet_membership": sub_a,
                "sub_b_no_nl_byte_in_span": sub_b,
                "sub_c_cardinality_conserved": sub_c,
                "n_reserved_blocks": a["n_reserved_blocks"],
                "n_records": len(recs),
                "bad_token_total": a["bad_token_total"],
                "nl_byte_in_span": a["nl_byte_in_span"],
                "reserved_vocab_closed": ok}


def main():
    battery = [
        ("F-DIRF-CORPUS-1 SHA256-DETERMINISTIC-CLOSED", f_dirf_corpus_1),
        ("F-DIRF-CORPUS-2 NO-CHAT-SFT-CONTAMINATION-CLOSED", f_dirf_corpus_2),
        ("F-DIRF-CORPUS-3 RESERVED-VOCAB-CLOSED", f_dirf_corpus_3),
    ]
    results = []
    n_pass = 0
    for name, fn in battery:
        try:
            ok, detail = fn()
        except Exception as e:  # pragma: no cover
            ok, detail = False, {"exception": repr(e)}
        if ok:
            n_pass += 1
        results.append({"falsifier": name, "verdict": "PASS" if ok else "FAIL",
                        "detail": detail})
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        print("   " + json.dumps(detail, ensure_ascii=False))

    summary = {
        "battery": "Dir-F ABSTRACT-COT reserved-vocab closed-form",
        "tier": ("🔵 SUPPORTED-FORMAL (reserved-vocab discreteness is the "
                 "closed side; SGD OUTCOME + Dir-F vs UBM-E7 α JOINT compare "
                 "= EMPIRICAL B-CARVE-E6-NOTE / B-D-NOTE family, NOT closed)"),
        "n_pass": n_pass, "n_total": len(battery),
        "all_pass": n_pass == len(battery),
        "f1_f2_safe": ("|Σ|=56 is the reserved-alphabet Kolmogorov byte "
                       "count over an internal corpus artefact, NOT a "
                       "σ/τ/φ/J₂ derivation and NOT an external-entity claim"),
        "results": results,
    }
    out = HERE / "blue_falsifier_dirF_result.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\n{n_pass}/{len(battery)} PASS  ->  {out.name}")
    if n_pass != len(battery):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
