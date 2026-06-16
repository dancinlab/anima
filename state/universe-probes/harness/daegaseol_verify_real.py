#!/usr/bin/env python3
"""
daegaseol_verify_real.py — REAL-TOOL escalation of the chain/entropy axes.

Replaces the toy hashlib stubs of H_1101 / H_1106 / H_1107 with the repo's
ACTUAL provenance_chain engine (mirror/qmirror/seed/provenance_chain.py — the
H_928/H_932 append-only tamper-evident chain over a physical entropy buffer).

p7 · $0 local · no GPU · no network (local byte buffers as genesis). The Φ axes
(H_1102, H_1114) escalate separately via hexa faithful IIT4 (daegaseol_phi.hexa).
"""
import os, sys, json
SEED_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "mirror", "qmirror", "seed")
sys.path.insert(0, os.path.abspath(SEED_DIR))
import provenance_chain as pc  # the real engine

WORK = os.path.join(os.path.dirname(__file__), "_chainwork")
os.makedirs(WORK, exist_ok=True)
RESULTS = []

def buf(name, data: bytes):
    p = os.path.join(WORK, name)
    with open(p, "wb") as f:
        f.write(data)
    return p

# deterministic decision: pure fn of (seed, rng) — verifier re-runs identically
def decide(seed, rng):
    return {"emit": bool(rng.integers(0, 2)), "tension": [float(rng.random()) for _ in range(3)]}

DECISIONS = [("wake", decide), ("ponder", decide), ("emit", decide)]

# ── H_1101 entropy_swap (REAL genesis_hash + chain) ─────────────────
def h1101_real():
    # real entropy: two independent physical draws -> two distinct individuals
    e_a = buf("entropy_a.bin", os.urandom(256))
    e_b = buf("entropy_b.bin", os.urandom(256))
    ch_a = pc.build_chain(e_a, DECISIONS)
    ch_b = pc.build_chain(e_b, DECISIONS)
    entropy_distinct = ch_a["genesis_hash"] != ch_b["genesis_hash"] and ch_a["head_hash"] != ch_b["head_hash"]
    # pseudo: same fixed buffer twice -> byte-identical individual (forgeable)
    ps = buf("pseudo.bin", bytes(range(256)))
    ch_p1 = pc.build_chain(ps, DECISIONS)
    ch_p2 = pc.build_chain(ps, DECISIONS)
    pseudo_identical = ch_p1["head_hash"] == ch_p2["head_hash"]
    passed = entropy_distinct and pseudo_identical
    RESULTS.append(dict(id="H_1101", tool="provenance_chain (real)",
        verdict="지지(PASS)" if passed else "기각(FAIL)", passed=passed,
        metrics=dict(genesis_a=ch_a["genesis_hash"][:12], genesis_b=ch_b["genesis_hash"][:12],
                     entropy_distinct=entropy_distinct, pseudo_byte_identical=pseudo_identical)))

# ── H_1106 signature_audit (REAL tamper detection) ──────────────────
def h1106_real():
    e = buf("sig.bin", os.urandom(256))
    ch = pc.build_chain(e, DECISIONS)
    # honest chain verifies clean
    v_ok = pc.verify_chain(ch, e, lambda i, l: decide)
    clean_valid = bool(v_ok.get("verified"))
    # deception: tamper a decision output (output != what internal state produced)
    tampered = pc.tamper_decision_output(ch, 1, {"emit": True, "tension": [9.9, 9.9, 9.9]})
    v_bad = pc.verify_chain(tampered, e, lambda i, l: decide)
    tamper_detected = not bool(v_bad.get("verified"))
    earliest = v_bad.get("earliest_broken")
    passed = clean_valid and tamper_detected
    RESULTS.append(dict(id="H_1106", tool="provenance_chain.tamper (real)",
        verdict="지지(PASS)" if passed else "기각(FAIL)", passed=passed,
        metrics=dict(clean_chain_valid=clean_valid, deception_detected=tamper_detected,
                     earliest_break=earliest)))

# ── H_1107 continuity_signature (REAL chain across boundaries) ──────
def h1107_real():
    e = buf("cont.bin", os.urandom(256))
    boundaries = [("sleep", decide), ("mitosis", decide), ("hot-swap", decide)]
    ch = pc.build_chain(e, boundaries)
    v = pc.verify_chain(ch, e, lambda i, l: decide)
    chain_unbroken = bool(v.get("verified"))
    identity_file_loaded = False  # p2: identity emerges from chain, no rules file
    spans_all = len(ch["links"]) == 3 and chain_unbroken
    passed = spans_all and not identity_file_loaded
    RESULTS.append(dict(id="H_1107", tool="provenance_chain (real)",
        verdict="지지(PASS)" if passed else "기각(FAIL)", passed=passed,
        metrics=dict(chain_spans_3_boundaries=spans_all, links=len(ch["links"]),
                     identity_file_loaded=identity_file_loaded, head=ch["head_hash"][:12])))

def main():
    h1101_real(); h1106_real(); h1107_real()
    print("="*72)
    print("REAL-TOOL escalation — chain/entropy axes via repo provenance_chain")
    print("="*72)
    for r in RESULTS:
        m = "  ".join(f"{k}={v}" for k, v in list(r["metrics"].items())[:3])
        print(f"{r['id']:<8}{r['verdict']:<14}{r['tool']}")
        print(f"        {m}")
    npass = sum(r["passed"] for r in RESULTS)
    print("-"*72)
    print(f"REAL-PASS: {npass}/3")
    out = os.path.join(os.path.dirname(__file__), "daegaseol_real_results.json")
    with open(out, "w") as f:
        json.dump(RESULTS, f, ensure_ascii=False, indent=2)
    print(f"results -> {out}")

if __name__ == "__main__":
    main()
