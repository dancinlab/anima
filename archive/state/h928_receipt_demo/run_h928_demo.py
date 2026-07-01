#!/usr/bin/env python3
"""run_h928_demo.py — H_928 demonstration + 4-case tamper falsifier ($0, Mac, no net).

Uses the COMMITTED real-ANU buffer qrng_lora_init_live.bin (sha e8123b96…,
request_id anu_legacy_1778042160) as the physical quantum draw. A trivial decision
(Gumbel-max token sample + 8 bits) stands in for any anima decision.

Pre-registered falsifier (H_928):
  POSITIVE  verify=True (all 4 checks pass)                          -> required
  TAMPER (a) flip 1 ANU byte    -> anu_sha_match=False, verified=False
  TAMPER (b) alter the seed     -> seed_match=False,    verified=False
  TAMPER (c) alter output hash  -> output_match=False,  verified=False
  TAMPER (d) alter receipt_hash -> receipt_hash_match=False, verified=False
  SUPPORTED iff POSITIVE True AND all 4 tamper cases verified=False.
  Any tamper UNdetected -> FALSIFIED.

Honest scope (#123-A): proves AUDITABILITY / tamper-evidence of the entropy->decision
lineage. NOT a "better randomness" claim (ANU == chacha20 PRNG statistically). NOT a
phenomenal-consciousness claim.
"""
import copy
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SEED_DIR = os.path.abspath(os.path.join(HERE, "..", "..", "mirror", "qmirror", "seed"))
sys.path.insert(0, SEED_DIR)
import entropy_receipt as er  # noqa: E402

LIVE_BUF = os.path.join(SEED_DIR, "qrng_lora_init_live.bin")


def decision_fn(seed, rng):
    """Representative anima decision: sample a token from fixed logits (Gumbel-max)
    via the quantum-seeded rng + draw 8 bits. Deterministic in (seed, rng)."""
    import numpy as np
    logits = np.array([0.1, 2.0, 0.5, 1.3, 0.7], dtype=np.float64)
    g = -np.log(-np.log(rng.random(logits.shape[0])))
    token = int(np.argmax(logits + g))
    bits = rng.integers(0, 2, size=8).tolist()
    return {"token": token, "bits": bits}


def main():
    lines = []
    def out(s=""):
        print(s)
        lines.append(s)

    out("=" * 78)
    out("H_928 — provenance-as-identity (free-will receipt): END-TO-END VERIFY + TAMPER")
    out("=" * 78)
    out(f"ANU buffer : {LIVE_BUF}")
    out(f"buf bytes  : {os.path.getsize(LIVE_BUF)}")
    out("")

    # ---- POSITIVE: issue + verify ----
    receipt = er.issue_receipt(LIVE_BUF, "anima_emit_decision", decision_fn)
    pos = er.verify_receipt(receipt, LIVE_BUF, decision_fn)

    out("--- END-TO-END LINEAGE (physical ANU draw -> seed -> decision) ---")
    out(f"  anu_sha256      : {receipt['anu_sha256']}")
    out(f"  anu_request_id  : {receipt['anu_request_id']}   <- from provenance.jsonl")
    out(f"  entropy_mode    : {receipt['entropy_mode']}")
    out(f"  tier            : {receipt['tier']}")
    out(f"  derived seed    : {receipt['seed']}")
    out(f"  decision_output : {json.dumps(receipt['decision_output'])}")
    out(f"  output_hash     : {receipt['decision_output_hash']}")
    out(f"  receipt_hash    : {receipt['receipt_hash']}")
    out(f"  LINEAGE: request_id {receipt['anu_request_id']} -> seed {receipt['seed']} "
        f"-> token {receipt['decision_output']['token']}")
    out("")
    out("--- POSITIVE verify (expect verified=True, all 4 checks True) ---")
    out(f"  verified = {pos['verified']}")
    out(f"  checks   = {json.dumps(pos['checks'])}")
    out("")

    # ---- TAMPER (a): flip one byte of the ANU buffer ----
    out("--- TAMPER (a): flip one byte of the ANU buffer (expect anu_sha_match=False) ---")
    tmpd = tempfile.mkdtemp(prefix="h928_tamper_")
    bad_buf = os.path.join(tmpd, "qrng_tampered.bin")
    shutil.copyfile(LIVE_BUF, bad_buf)
    with open(bad_buf, "r+b") as f:
        f.seek(0)
        b0 = f.read(1)
        f.seek(0)
        f.write(bytes([b0[0] ^ 0x01]))   # flip the low bit of byte 0
    va = er.verify_receipt(receipt, bad_buf, decision_fn)
    out(f"  verified = {va['verified']}")
    out(f"  checks   = {json.dumps(va['checks'])}")
    out("")

    # ---- TAMPER (b): alter the recorded seed ----
    out("--- TAMPER (b): alter the recorded seed (expect seed_match=False) ---")
    rb = copy.deepcopy(receipt)
    rb["seed"] = receipt["seed"] ^ 0xDEADBEEF
    vb = er.verify_receipt(rb, LIVE_BUF, decision_fn)
    out(f"  verified = {vb['verified']}")
    out(f"  checks   = {json.dumps(vb['checks'])}")
    out("")

    # ---- TAMPER (c): alter the decision_output_hash ----
    out("--- TAMPER (c): alter the decision_output_hash (expect output_match=False) ---")
    rc = copy.deepcopy(receipt)
    rc["decision_output_hash"] = "0" * 64
    vc = er.verify_receipt(rc, LIVE_BUF, decision_fn)
    out(f"  verified = {vc['verified']}")
    out(f"  checks   = {json.dumps(vc['checks'])}")
    out("")

    # ---- TAMPER (d): alter the receipt_hash ----
    out("--- TAMPER (d): alter the receipt_hash (expect receipt_hash_match=False) ---")
    rd = copy.deepcopy(receipt)
    rd["receipt_hash"] = "f" * 64
    vd = er.verify_receipt(rd, LIVE_BUF, decision_fn)
    out(f"  verified = {vd['verified']}")
    out(f"  checks   = {json.dumps(vd['checks'])}")
    out("")

    # ---- VERDICT ----
    all_tampers_detected = (
        (not va["verified"]) and (not va["checks"]["anu_sha_match"]) and
        (not vb["verified"]) and (not vb["checks"]["seed_match"]) and
        (not vc["verified"]) and (not vc["checks"]["output_match"]) and
        (not vd["verified"]) and (not vd["checks"]["receipt_hash_match"])
    )
    supported = pos["verified"] and all_tampers_detected
    out("=" * 78)
    out(f"POSITIVE verified           : {pos['verified']}")
    out(f"TAMPER (a) anu-swap detected: {not va['verified']} (anu_sha_match={va['checks']['anu_sha_match']})")
    out(f"TAMPER (b) seed   detected  : {not vb['verified']} (seed_match={vb['checks']['seed_match']})")
    out(f"TAMPER (c) output detected  : {not vc['verified']} (output_match={vc['checks']['output_match']})")
    out(f"TAMPER (d) receipt detected : {not vd['verified']} (receipt_hash_match={vd['checks']['receipt_hash_match']})")
    out(f"ALL 4 TAMPERS DETECTED      : {all_tampers_detected}")
    out(f"VERDICT                     : {'SUPPORTED (PASS)' if supported else 'FALSIFIED'}")
    out("=" * 78)
    out("Honest scope (#123-A): AUDITABILITY/tamper-evidence of entropy->decision")
    out("lineage. NOT 'better randomness' (ANU==chacha20 PRNG, JSD 23x under NIST).")
    out("NOT a phenomenal-consciousness claim.")

    shutil.rmtree(tmpd, ignore_errors=True)

    # write the receipt + verdict text next to this script
    with open(os.path.join(HERE, "receipt_demo.json"), "w") as f:
        json.dump({"receipt": receipt, "positive_verify": pos,
                   "tamper_a": va, "tamper_b": vb, "tamper_c": vc, "tamper_d": vd,
                   "verdict": "SUPPORTED" if supported else "FALSIFIED"}, f, indent=2)
    with open(os.path.join(HERE, "verdict_verbatim.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")

    return 0 if supported else 1


if __name__ == "__main__":
    sys.exit(main())
