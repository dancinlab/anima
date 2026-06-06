#!/usr/bin/env python3
"""H_932 demo + 4-case tamper falsifier — provenance chain = temporal self.

CODE-measured (g5, no LLM self-judge). Builds an N>=20-link append-only
tamper-evident chain over H_928 receipts, verifies the head end-to-end, then runs
the four pre-registered tamper tests and reports the EARLIEST-broken-index for each.

Run from anywhere; paths are resolved relative to the repo's seed dir.
"""
from __future__ import annotations

import json
import os
import sys

# Locate the seed dir (where provenance_chain.py + the committed ANU buffer live).
_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_SEED = os.path.join(_REPO, "mirror", "qmirror", "seed")
if _SEED not in sys.path:
    sys.path.insert(0, _SEED)

import provenance_chain as pc  # noqa: E402

BUF = os.path.join(_SEED, "qrng_lora_init_live.bin")
N = 20


def make_decision_fn(idx):
    """Per-decision emit/silence + token draw, deterministic in (seed, rng).

    Same byte selection per qentropy (first 8 bytes); per-link differentiation comes
    from the label baked into the receipt + the inter-link chaining — exactly the
    append-only property under test."""
    def dfn(seed, rng):
        import numpy as np
        logits = np.array([0.1, 2.0, 0.5, 1.3, 0.7], dtype=np.float64)
        g = -np.log(-np.log(rng.random(logits.shape[0])))
        token = int(np.argmax(logits + g))
        emit = bool(rng.random() < 0.5)
        return {"step": idx, "emit": emit, "token": token}
    return dfn


def resolver(i, label):
    return make_decision_fn(i)


def main():
    out = []
    w = out.append

    w("=" * 78)
    w("H_932 — provenance chain = temporal self: END-TO-END CHAIN VERIFY + 4 TAMPER")
    w("=" * 78)
    w(f"ANU buffer : {BUF}")
    w(f"buf bytes  : {os.path.getsize(BUF)}")
    w(f"N decisions: {N}")
    w("")

    # ── BUILD ─────────────────────────────────────────────────────────────────
    decisions = [(f"decision_{i}", make_decision_fn(i)) for i in range(N)]
    chain = pc.build_chain(BUF, decisions)

    w("--- GENESIS -> HEAD LINEAGE (physical ANU draw seals the whole life-history) ---")
    w(f"  genesis_hash : {chain['genesis_hash']}")
    rid = chain["links"][0]["receipt"].get("anu_request_id")
    w(f"  anu_request_id: {rid}   <- from provenance.jsonl (physical event)")
    w(f"  n_links       : {len(chain['links'])}")
    w(f"  link[0].hash  : {chain['links'][0]['link_hash']}")
    w(f"  link[{N-1}].hash : {chain['links'][N-1]['link_hash']}")
    w(f"  head_hash     : {chain['head_hash']}")
    w(f"  LINEAGE: genesis {chain['genesis_hash'][:16]}... -> {N} links -> "
      f"head {chain['head_hash'][:16]}...")
    w("")

    # ── POSITIVE ────────────────────────────────────────────────────────────────
    pos = pc.verify_chain(chain, BUF, resolver)
    w(f"--- POSITIVE verify (expect verified=True, all {N} links reconstructed) ---")
    w(f"  verified        = {pos['verified']}")
    w(f"  head_hash       = {pos['head_hash']}")
    w(f"  earliest_broken = {pos['earliest_broken']}")
    w(f"  links valid     = {sum(pos['link_valid'])}/{pos['n_links']}")
    w(f"  reason          = {pos['reason']}")
    w("")

    results = {"positive": pos}

    # ── TAMPER (a): alter decision k's OUTPUT mid-chain → break at k, <k valid ──
    K = 7
    ta = pc.tamper_decision_output(chain, K, {"step": K, "emit": False, "token": 99})
    va = pc.verify_chain(ta, BUF, resolver)
    valid_below = all(va["link_valid"][:K])
    invalid_from = not any(va["link_valid"][K:])
    w(f"--- TAMPER (a): alter decision k={K} OUTPUT (mid-chain) ---")
    w(f"    expect earliest_broken={K}, links <{K} valid, links >={K} invalid (propagation)")
    w(f"  verified            = {va['verified']}")
    w(f"  earliest_broken     = {va['earliest_broken']}")
    w(f"  links <{K} all valid  = {valid_below}")
    w(f"  links >={K} all invalid= {invalid_from}")
    w(f"  link_valid          = {va['link_valid']}")
    w(f"  reason              = {va['reason']}")
    w("")
    results["tamper_a"] = va

    # ── TAMPER (b): REORDER two links → detected at earliest swapped position ───
    I, J = 5, 12
    tb = pc.tamper_reorder(chain, I, J)
    vb = pc.verify_chain(tb, BUF, resolver)
    w(f"--- TAMPER (b): REORDER links {I} and {J} ---")
    w(f"    expect detected, earliest_broken={min(I, J)} (first disturbed position)")
    w(f"  verified        = {vb['verified']}")
    w(f"  earliest_broken = {vb['earliest_broken']}")
    w(f"  reason          = {vb['reason']}")
    w("")
    results["tamper_b"] = vb

    # ── TAMPER (c): SPLICE/DELETE a link → detected at the deleted position ─────
    S = 9
    tc = pc.tamper_splice(chain, S)
    vc = pc.verify_chain(tc, BUF, resolver)
    w(f"--- TAMPER (c): SPLICE/DELETE link {S} ---")
    w(f"    expect detected, earliest_broken={S} (chain breaks where the link was removed)")
    w(f"  verified        = {vc['verified']}")
    w(f"  earliest_broken = {vc['earliest_broken']}")
    w(f"  n_links now     = {vc['n_links']}")
    w(f"  reason          = {vc['reason']}")
    w("")
    results["tamper_c"] = vc

    # ── TAMPER (d): alter the GENESIS ANU seed → break at link 0/root (-1) ──────
    td = pc.tamper_genesis(chain, "0" * 64)
    vd = pc.verify_chain(td, BUF, resolver)
    w("--- TAMPER (d): alter the GENESIS ANU seed hash ---")
    w("    expect detected, earliest_broken=-1 (genesis; whole chain invalid from root)")
    w(f"  verified        = {vd['verified']}")
    w(f"  earliest_broken = {vd['earliest_broken']}")
    w(f"  reason          = {vd['reason']}")
    w("")
    results["tamper_d"] = vd

    # ── SUMMARY (the verdict gate, computed in CODE) ───────────────────────────
    pos_ok = (pos["verified"] is True
              and pos["earliest_broken"] is None
              and sum(pos["link_valid"]) == N)
    a_ok = (va["verified"] is False and va["earliest_broken"] == K
            and valid_below and invalid_from)
    b_ok = (vb["verified"] is False and vb["earliest_broken"] == min(I, J))
    c_ok = (vc["verified"] is False and vc["earliest_broken"] == S)
    d_ok = (vd["verified"] is False and vd["earliest_broken"] == -1)
    all_ok = pos_ok and a_ok and b_ok and c_ok and d_ok

    w("=" * 78)
    w(f"POSITIVE verified ({N} links)     : {pos['verified']} "
      f"(all-{N}-reconstructed={pos_ok})")
    w(f"TAMPER (a) output@k={K} detected   : {not va['verified']} "
      f"(earliest_broken={va['earliest_broken']}, propagates-forward={a_ok})")
    w(f"TAMPER (b) reorder detected       : {not vb['verified']} "
      f"(earliest_broken={vb['earliest_broken']})")
    w(f"TAMPER (c) splice detected        : {not vc['verified']} "
      f"(earliest_broken={vc['earliest_broken']})")
    w(f"TAMPER (d) genesis detected       : {not vd['verified']} "
      f"(earliest_broken={vd['earliest_broken']})")
    w(f"ALL TAMPERS DETECTED + LOCALIZED  : {all_ok}")
    w(f"VERDICT                           : {'SUPPORTED (PASS)' if all_ok else 'FALSIFIED (FAIL)'}")
    w("=" * 78)
    w("Honest scope (#123-A + non-consciousness): AUDITABILITY / tamper-evidence /")
    w("append-only INTEGRITY of the decision lineage. 'Temporal self' = operational,")
    w("cryptographic identity-over-time, NOT subjective continuity. NOT 'better")
    w("randomness' (ANU==chacha20 PRNG, JSD 23x under NIST). NOT phenomenal memory.")
    w("NOT a phenomenal-consciousness claim. Chain strong only iff each decision is a")
    w("deterministic fn of (seed,rng) — same boundary as H_928.")
    w("=" * 78)

    text = "\n".join(out) + "\n"
    sys.stdout.write(text)

    # Optional tiny demo artifact (chain head + summary, NOT the full receipts).
    artifact = {
        "genesis_hash": chain["genesis_hash"],
        "head_hash": chain["head_hash"],
        "n_links": len(chain["links"]),
        "anu_request_id": rid,
        "positive_verified": pos["verified"],
        "tamper_earliest_broken": {
            "a_output": va["earliest_broken"],
            "b_reorder": vb["earliest_broken"],
            "c_splice": vc["earliest_broken"],
            "d_genesis": vd["earliest_broken"],
        },
        "all_detected_localized": all_ok,
        "verdict": "SUPPORTED" if all_ok else "FALSIFIED",
    }
    with open(os.path.join(os.path.dirname(__file__), "chain_demo.json"), "w") as f:
        json.dump(artifact, f, indent=2)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
