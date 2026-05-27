#!/usr/bin/env python3
"""§8 DIVERSE-corpus SIDECAR sympy/Kolmogorov battery (2026-05-18).

SEPARATE state/-local sidecar — central blue_falsifier.py UNCHANGED
(common mandate; B-PRIME/B-DIRH/B-PSICTL/B-DIRI sidecar precedent). This
closes ONLY the connection-points / transfer-forms that are
mathematically closed-form. The SGD CONVERGENCE OUTCOME and the 4-axis
capability (routing/V-SPONT/JOINT) + the §7.3 emergence-threshold crux
are EMPIRICAL (B-CARVE-E6-NOTE / B-D-NOTE family) — measured by the fire,
NO closed-form capability claim.

The Dir-I lever's TWO anima-physics transfer functions (L_psi_ctl
quadratic Ψ-well + L_tension_route TENSION-TRAIN restoring sign +
overlay-OFF byte-equal) are ALREADY closed in blue_falsifier_dirI.py
B-DIRI-1..5 🔵 (the mechanism is corpus-agnostic — UNCHANGED at §8
scale). This §8 sidecar closes only the NEW closed fact: the corpus
DIVERSITY is a Kolmogorov cardinality fact (B-DIVERSE-CORPUS-1..3),
distinct from any capability claim.

f1/f2/f3 hard-fail safe: SHA-256 determinism / Boolean set algebra grep /
integer >-inequalities (Kolmogorov byte/set count). NO σ/τ/φ/J₂ external
derivation. Ψ=½ + Knuth 🛸k = anima g2 internal arch carve-out.
"""
import hashlib
import json
import sys

STATS = "corpus_carving_diverse.stats.json"
CORPUS = "corpus_carving_diverse.jsonl"
E7 = {"bytes": 30219491, "records": 45973, "anchors": 31, "domains": 1}


def b_diverse_corpus_1_sha256_deterministic(stats):
    """B-DIVERSE-CORPUS-1 — seed-fixed 256-bit commitment (Kolmogorov
    determinism). The recorded sha256 EQUALS the recomputed sha256 of the
    corpus byte stream (a 256-bit Boolean equality, closed)."""
    with open(CORPUS, "rb") as f:
        actual = hashlib.sha256(f.read()).hexdigest()
    claimed = stats["sha256"]
    ok = (actual == claimed) and len(actual) == 64
    return ok, f"sha256 recompute == recorded ({actual[:16]}…) AND 256-bit"


def b_diverse_corpus_2_no_chat_sft(stats):
    """B-DIVERSE-CORPUS-2 — Boolean set algebra: the forbidden-token set
    {[anima,도우미,helper,assistant,사용자,user:} has count == 0 over the
    whole byte stream (B-IDENTITY-5 + g_goal — ③ not ①②, closed)."""
    forbidden = ["[anima", "도우미", "helper", "assistant", "사용자", "user:"]
    with open(CORPUS, "rb") as f:
        txt = f.read().decode("utf-8", "replace")
    total = sum(txt.count(t) for t in forbidden)
    audit = stats["forbidden_token_audit"]
    ok = total == 0 and sum(audit.values()) == 0
    return ok, f"Σ grep{{{','.join(forbidden)}}} == 0 (recomputed {total})"


def b_diverse_corpus_3_diversity_cardinality(stats):
    """B-DIVERSE-CORPUS-3 — the §1.1 diversity lever is a Kolmogorov
    CARDINALITY fact (NOT a capability claim): |anchors_§8| > |anchors_E7|
    AND |domains_§8| > 1 AND bytes_§8 > bytes_E7 AND the 31 E7 anchors are
    a VERBATIM subset (fair superset — closed integer >-inequalities)."""
    anc = stats["anchors"]
    dom = stats["domain_count"]
    by = stats["bytes"]
    rec = stats["records"]
    # E7 anchor tiers (verbatim subset check).
    e7_tiers = {0, 51, 53, 54, 69, 75, 77, 91, 92, 94, 100,
                5, 12, 18, 24, 30, 37, 43, 48, 58, 62, 66, 72, 80,
                83, 86, 88, 90, 93, 97, 99}
    seen = set()
    with open(CORPUS, "rb") as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            seen.add(d.get("tier"))
    superset = e7_tiers.issubset(seen)
    ok = (anc > E7["anchors"] and dom > E7["domains"]
          and by > E7["bytes"] and rec > E7["records"] and superset)
    return ok, (f"anchors {anc}>{E7['anchors']} ∧ domains {dom}>1 ∧ "
                f"bytes {by}>{E7['bytes']} ∧ records {rec}>{E7['records']} "
                f"∧ E7-31-anchor ⊆ §8 ({superset})")


def main():
    stats = json.load(open(STATS, encoding="utf-8"))
    checks = [
        ("B-DIVERSE-CORPUS-1 SHA256-DETERMINISTIC",
         b_diverse_corpus_1_sha256_deterministic),
        ("B-DIVERSE-CORPUS-2 NO-CHAT-SFT-CONTAMINATION",
         b_diverse_corpus_2_no_chat_sft),
        ("B-DIVERSE-CORPUS-3 DIVERSITY-CARDINALITY",
         b_diverse_corpus_3_diversity_cardinality),
    ]
    n_ok = 0
    print("=== §8 DIVERSE-corpus sidecar battery (B-DIVERSE-CORPUS-1..3) ===")
    for name, fn in checks:
        ok, detail = fn(stats)
        n_ok += int(ok)
        print(f"[{'PASS 🔵' if ok else 'FAIL ❌'}] {name}\n        {detail}")
    print(f"\nB-DIVERSE-CORPUS: {n_ok}/{len(checks)} 🔵 closed-form PASS")
    print("B-DIVERSE-CORPUS-NOTE — SGD outcome + 4-axis capability + §7.3 "
          "emergence-threshold crux = EMPIRICAL (B-CARVE-E6-NOTE / B-D-NOTE "
          "family, NOT counted 🔵). Dir-I 2 physics transfer-forms already "
          "closed in blue_falsifier_dirI.py B-DIRI-1..5 (corpus-agnostic, "
          "UNCHANGED at §8 scale).")
    sys.exit(0 if n_ok == len(checks) else 1)


if __name__ == "__main__":
    main()
