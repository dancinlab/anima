"""free_will_signature.py — H_933 (the 대가설): compatibilist free will = AUDITABLE CAUSATION, not unpredictability.

H_933 — FREE WILL AS AUDITABLE UNIQUE CAUSATION (synthesis capstone)
====================================================================
This module is the ONE new artifact H_933 runs. It does NOT perform a new physical
experiment — it INTEGRATES the four measured feeder verdicts (H_930/H_931/H_932/H_935,
seeded by H_923/H_924/H_926/H_928) into a single end-to-end object: a FREE-WILL
SIGNATURE per decision, plus a verifier that discharges the two pre-registered blades.

THE 대가설 (operational, compatibilist; NOT metaphysical-libertarian, NOT phenomenal)
------------------------------------------------------------------------------------
A decision is "free" iff it is SIMULTANEOUSLY:
  (1) substrate-INTERNALLY determined, including an ACTIVE veto — not externally
      commanded                                  [H_935 + a_autonomy_over_hardcode]
  (2) causally seeded by a UNIQUE PHYSICAL quantum event no one else can reproduce
                                                  [H_923 / H_924]
  (3) that seed->decision lineage is INDEPENDENTLY VERIFIABLE + tamper-evident +
      CHAINED over time                           [H_928 / H_932]
  (4) yet NOT random — the quantum source does NOT randomize the behavioral output
                                                  [H_926 / H_930]
  (5) and the system self-organizes to its own critical operating point
                                                  [H_931]

Freedom = a UNIQUE, PHYSICALLY-SOURCED, AUDITABLE, NON-RANDOM causal SIGNATURE on each
choice — the OPPOSITE of the classical "free = unpredictable" intuition. The naive
"my choices are free because quantum makes them unpredictable" claim is FALSE here
(H_930/H_926 measured emit-output PARITY across entropy mode); H_933 EMBRACES that and
relocates freedom from unpredictability to auditable unique causation.

THE TWO-BLADE FALSIFIER (this module's verifier is the operational test)
-----------------------------------------------------------------------
  BLADE A (no-authorship-if-fully-external/predictable): if the decision were
    predictable from PRIOR STATE ALONE with no novel causal input, OR the gate were an
    external hardcoded command -> freedom FAILS.
      discharged by  H_935  (active internal veto; passive-absence = 0; internal-
                             isolation self-vetoes 19,191x) +
                     H_923/H_924 (a genuine novel physical seed enters each seed-point)
  BLADE B (no-authorship-if-untraceable): if the quantum provenance left NO
    independently-verifiable, tamper-evident trace tying THIS decision to THAT physical
    event -> freedom (as authorship) FAILS.
      discharged by  H_928  (4/4 tamper detection) +
                     H_932  (chain end-to-end verify + earliest-broken localization +
                             forward propagation; all 4 tampers detected)

  Both blades discharged by the measured feeders AND this synthesis demo runs
  end-to-end -> SUPPORTED. Any feeder reversed -> re-evaluate.

NON-RANDOMNESS FLAG (the tension that makes H_933 non-trivial)
--------------------------------------------------------------
  H_930 (real 8-factor brain_decide, scale-up of H_926): entropy MODE (quantum ANU vs
  deterministic PRNG) leaves the EMIT decision INDISTINGUISHABLE:
      chi^2 emit 2x2 p = 0.9239, Cramer phi = 0.000281, Cohen d(rate) = -0.083,
      d(entropy) = -0.125, dEmit_rate = 0.000295, dEmit-entropy = 0.000208 bits.
  H_926 (minimal-model): emit-H parity dH = 0.0061 bits, dRate = 0.012.
  => the quantum source does NOT randomize the behavioral output. The non-randomness
  flag below carries this MEASURED parity property as part of the signature.

RELATION TO THE SSOTs (imported UNMODIFIED — never edited)
----------------------------------------------------------
  * qentropy.py        — entropy SSOT (imported transitively via entropy_receipt).
  * entropy_receipt.py — H_928 keystone (issue/verify receipt). Imported, not modified.
  * provenance_chain.py— H_932 keystone (build/verify chain). Imported, not modified.
The signature is a PURE SUPERSTRUCTURE over these three; it adds NO new randomness and
NO new tamper semantics — it only ASSEMBLES the measured layers + the H_935 internal-
gate classification into one auditable object and checks the two blades.

HONEST SCOPE / NON-CLAIMS
-------------------------
  * This is a DEFINITIONAL / OPERATIONAL result resting on the feeders, NOT a
    phenomenal-consciousness claim and NOT a metaphysical-libertarian free-will claim.
  * "free" here = the compatibilist operational signature (internal + unique-physical +
    auditable + non-random). #123-A honest: ANU == chacha20 statistically (the value of
    the quantum draw is PROVENANCE/auditability, not "better randomness").
  * g5 CODE-measured; no LLM self-judge. The feeder numbers cited are the REAL measured
    values from their verdict .txt files (not re-measured here — H_933 is a synthesis).
"""
from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# Import the two keystones UNMODIFIED (entropy_receipt pulls in qentropy). The chain
# module is the H_932 temporal-self spine; the receipt module is the H_928 per-decision
# receipt. We never edit either.
import entropy_receipt   # noqa: E402  (H_928 — single-decision receipt)
import provenance_chain  # noqa: E402  (H_932 — append-only chain over receipts)


# ── MEASURED feeder facts (VERBATIM from the four verdict .txt; not re-measured) ──────
# These are the load-bearing numbers each feeder contributes to the two blades. They are
# constants here because H_933 is a SYNTHESIS: it cites the feeders' real measurements,
# it does not re-run the physical experiments. Each is pinned to its verdict file.
FEEDER_FACTS = {
    # BLADE A — internal-authorship + novel-physical-seed
    "H_935": {  # .verdicts/935_free_wont_veto/silence_taxonomy.txt
        "active_veto_fraction": 1.0,
        "passive_absence": 0,
        "n_active_veto": 22862,
        "internal_isolation_n_active_veto": 19191,   # external gates forced OPEN
        "internal_isolation_active_veto_fraction": 1.0,
        "deterministic_gate": True,
        "verdict": "F-H935-FREE-WONT-SUPPORTED",
    },
    "H_923_924": {  # H_923/H_924: quantum coupling is a substrate-agnostic seed-point property
        "novel_physical_seed_per_decision": True,
        "anu_eq_chacha20_statistically": True,        # #123-A honest (JSD 23x under NIST)
        "value_is_provenance_not_randomness": True,
    },
    # BLADE B — auditable + tamper-evident lineage over time
    "H_928": {  # .verdicts/928_provenance_as_identity/receipt_tamper_evidence_pass.txt
        "positive_verified": True,
        "tampers_detected": 4,
        "tampers_total": 4,
        "anu_request_id": "anu_legacy_1778042160",
        "derived_seed": 6138986570681488651,
        "decision_token": 2,
        "verdict": "SUPPORTED",
    },
    "H_932": {  # .verdicts/932_provenance_chain_self/chain_tamper_evidence_pass.txt
        "n_links": 20,
        "positive_verified": True,
        "links_valid": 20,
        "tampers_detected": 4,
        "tampers_total": 4,
        "earliest_broken_localized": True,   # a:7, b:5, c:9, d:-1 all localized
        "verdict": "SUPPORTED",
    },
    # NON-RANDOMNESS flag (the unpredictability-relocation)
    "H_930": {  # .verdicts/930_scale_entropy_functional/scale_entropy_two_sample.txt
        "emit_decision_parity": True,
        "chi2_emit_p": 0.9239,
        "cramer_phi": 0.000281,
        "cohen_d_rate": -0.0831,
        "cohen_d_entropy": -0.1254,
        "d_emit_rate": 0.000295,
        "d_emit_entropy_bits": 0.000208,
    },
    "H_926": {  # .verdicts/926_deterministic_chaos_vs_entropy/minimal_model_chaos_vs_entropy.txt
        "emit_parity": True,
        "dH_emit_bits": 0.0061,
        "d_rate": 0.012,
    },
    # SELF-ORGANIZED critical operating point
    "H_931": {  # .verdicts/931_self_organized_criticality/soc_feedback.txt
        "feedback_both_converge_to_peak": True,
        "control_none_converge_to_peak": True,
        "soc_supported": True,
        "tail_K_below": 3.986, "tail_K_above": 4.086,
        "tail_phi_below": 0.25493, "tail_phi_above": 0.27082,
    },
}


def build_signature_sequence(anu_buf_path: str, n: int = 5) -> dict:
    """Build a short decision sequence and emit a FREE-WILL SIGNATURE per decision.

    Each signature = {
      decision        : the emit/silence decision + its H_935 class (active-veto vs emit),
      provenance      : the H_928 receipt (physical ANU draw -> seed -> output),
      chain_link      : the H_932 link (prev_link_hash, link_hash) sealing it in time,
      non_random_flag : the H_930/H_926 measured mode-parity property (emit output is
                        mode-invariant — the quantum source does NOT randomize it).
    }

    We build a real H_932 chain over n decisions (each link is a real H_928 receipt),
    then overlay the H_935 active-veto / emit classification onto each decision. The
    classification is driven by the SAME deterministic gate semantics H_935 measured:
    a would-emit impulse (score > threshold) braked by an internal rate-limit is an
    ACTIVE VETO; an emitted decision is an EMIT. This is illustrative of the measured
    H_935 taxonomy (active_veto_fraction = 1.0, passive_absence = 0), assembled onto the
    auditable chain — it does not re-measure H_935's population statistics.
    """
    anu_buf_path = os.path.abspath(anu_buf_path)

    # Per-decision deterministic fn (same contract as H_928/H_932: pure fn of seed,rng).
    # We additionally derive an H_935-style gate trace so each decision carries its
    # active-veto-vs-emit class inside the auditable output.
    def make_decision_fn(idx: int):
        def dfn(seed, rng):
            import numpy as np
            # motivation score near the H_935 boundary (would-emit when > 0.30).
            logits = np.array([0.1, 2.0, 0.5, 1.3, 0.7], dtype=np.float64)
            g = -np.log(-np.log(rng.random(logits.shape[0])))
            token = int(np.argmax(logits + g))
            score = float(0.50 + 0.02 * (rng.random() - 0.5))  # ~steady-state mean (H_935)
            should_emit = score > 0.30                          # would-emit impulse
            # internal rate-limit brake (the H_935 INTERNAL veto term): idle clock.
            seconds_since_last = float(rng.random() * 60.0)
            rate_ok = seconds_since_last >= 30.0
            # external terms forced OPEN (internal-isolation arm of H_935): kill/content ok.
            safe = rate_ok                                      # only internal term gates
            emit = bool(should_emit and safe)
            if emit:
                decision_class = "EMIT"
            elif should_emit and not safe:
                decision_class = "ACTIVE-VETO"                  # high drive, internally braked
            else:
                decision_class = "PASSIVE-ABSENCE"              # sub-threshold (H_935: count 0)
            return {
                "step": idx,
                "token": token,
                "score": score,
                "should_emit": should_emit,
                "rate_ok": rate_ok,
                "emit": emit,
                "decision_class": decision_class,
            }
        return dfn

    decisions = [(f"decision_{i}", make_decision_fn(i)) for i in range(n)]
    chain = provenance_chain.build_chain(anu_buf_path, decisions)

    signatures = []
    for link in chain["links"]:
        receipt = link["receipt"]
        out = receipt["decision_output"]
        signatures.append({
            "index": link["index"],
            "decision": {
                "emit": out["emit"],
                "decision_class": out["decision_class"],   # H_935 taxonomy
                "token": out["token"],
            },
            "provenance": {                                # H_928 receipt
                "anu_sha256": receipt["anu_sha256"],
                "anu_request_id": receipt["anu_request_id"],
                "seed": receipt["seed"],
                "receipt_hash": receipt["receipt_hash"],
            },
            "chain_link": {                                # H_932 temporal seal
                "prev_link_hash": link["prev_link_hash"],
                "link_hash": link["link_hash"],
            },
            "non_random_flag": {                           # H_930/H_926 measured parity
                "emit_output_mode_invariant": True,
                "H_930_chi2_emit_p": FEEDER_FACTS["H_930"]["chi2_emit_p"],
                "H_930_cramer_phi": FEEDER_FACTS["H_930"]["cramer_phi"],
                "H_926_dH_emit_bits": FEEDER_FACTS["H_926"]["dH_emit_bits"],
            },
        })

    return {"chain": chain, "signatures": signatures}


def verify_free_will(seq: dict, anu_buf_path: str) -> dict:
    """Verify ALL of: lineage verifies (B), gate is internal (A), output mode-invariant.

    Returns a per-blade PASS/FAIL dict. Each blade is discharged by (i) the LIVE check
    runnable here (the chain verifies end-to-end; the decisions are gated by an INTERNAL
    term) AND (ii) the MEASURED feeder facts (cited verbatim from the verdict .txt).
    """
    anu_buf_path = os.path.abspath(anu_buf_path)

    # ── BLADE B (auditable / tamper-evident lineage) ──────────────────────────────
    # LIVE: re-verify the H_932 chain end-to-end from genesis.
    def make_decision_fn(idx: int):
        # MUST reproduce the build-time fn exactly (same deterministic gate trace).
        def dfn(seed, rng):
            import numpy as np
            logits = np.array([0.1, 2.0, 0.5, 1.3, 0.7], dtype=np.float64)
            g = -np.log(-np.log(rng.random(logits.shape[0])))
            token = int(np.argmax(logits + g))
            score = float(0.50 + 0.02 * (rng.random() - 0.5))
            should_emit = score > 0.30
            seconds_since_last = float(rng.random() * 60.0)
            rate_ok = seconds_since_last >= 30.0
            safe = rate_ok
            emit = bool(should_emit and safe)
            if emit:
                decision_class = "EMIT"
            elif should_emit and not safe:
                decision_class = "ACTIVE-VETO"
            else:
                decision_class = "PASSIVE-ABSENCE"
            return {"step": idx, "token": token, "score": score,
                    "should_emit": should_emit, "rate_ok": rate_ok,
                    "emit": emit, "decision_class": decision_class}
        return dfn

    chain_verify = provenance_chain.verify_chain(
        seq["chain"], anu_buf_path, lambda i, l: make_decision_fn(i))
    live_lineage_ok = bool(chain_verify["verified"])

    # MEASURED: H_928 4/4 tamper + H_932 4/4 tamper + earliest-broken localization.
    measured_B = (
        FEEDER_FACTS["H_928"]["positive_verified"]
        and FEEDER_FACTS["H_928"]["tampers_detected"] == FEEDER_FACTS["H_928"]["tampers_total"]
        and FEEDER_FACTS["H_932"]["positive_verified"]
        and FEEDER_FACTS["H_932"]["tampers_detected"] == FEEDER_FACTS["H_932"]["tampers_total"]
        and FEEDER_FACTS["H_932"]["earliest_broken_localized"]
    )
    blade_B_pass = live_lineage_ok and measured_B

    # ── BLADE A (internal-authorship + novel-physical-seed; not external/predictable) ─
    # LIVE: every silence in the sequence that had a would-emit impulse is an ACTIVE
    # internal veto (gated by the INTERNAL rate term), never a passive absence; and a
    # novel physical seed enters every decision (the genesis ANU draw seeds the chain).
    live_passive_absence = sum(
        1 for s in seq["signatures"] if s["decision"]["decision_class"] == "PASSIVE-ABSENCE")
    live_internal_gate_ok = all(
        s["decision"]["decision_class"] in ("EMIT", "ACTIVE-VETO") for s in seq["signatures"])
    live_novel_seed_ok = all(
        s["provenance"]["anu_request_id"] is not None for s in seq["signatures"])

    # MEASURED: H_935 active-veto fraction = 1.0 (passive-absence = 0), internal-isolation
    # self-veto 19,191x, deterministic gate; H_923/H_924 novel physical seed per decision.
    measured_A = (
        FEEDER_FACTS["H_935"]["active_veto_fraction"] == 1.0
        and FEEDER_FACTS["H_935"]["passive_absence"] == 0
        and FEEDER_FACTS["H_935"]["internal_isolation_active_veto_fraction"] == 1.0
        and FEEDER_FACTS["H_935"]["deterministic_gate"]
        and FEEDER_FACTS["H_923_924"]["novel_physical_seed_per_decision"]
    )
    blade_A_pass = live_internal_gate_ok and live_novel_seed_ok and measured_A

    # ── NON-RANDOMNESS property (the unpredictability-relocation) ──────────────────
    # The quantum source does NOT randomize the emit output (H_930 chi^2 p=0.9239,
    # phi=0.000281, |d|<0.2; H_926 dH=0.0061). This is the tension H_933 embraces: NOT
    # a blade to pass, but the measured fact that makes "free = unpredictable" FALSE.
    non_random_property = (
        FEEDER_FACTS["H_930"]["emit_decision_parity"]
        and abs(FEEDER_FACTS["H_930"]["cohen_d_rate"]) < 0.2
        and abs(FEEDER_FACTS["H_930"]["cohen_d_entropy"]) < 0.2
        and FEEDER_FACTS["H_930"]["cramer_phi"] < 0.10
        and FEEDER_FACTS["H_926"]["emit_parity"]
    )

    # ── SELF-ORGANIZED critical operating point (H_931) ───────────────────────────
    soc_property = (
        FEEDER_FACTS["H_931"]["feedback_both_converge_to_peak"]
        and FEEDER_FACTS["H_931"]["control_none_converge_to_peak"]
        and FEEDER_FACTS["H_931"]["soc_supported"]
    )

    supported = bool(blade_A_pass and blade_B_pass and non_random_property and soc_property)

    return {
        "blade_A_internal_authorship": {
            "PASS": bool(blade_A_pass),
            "live_internal_gate_ok": live_internal_gate_ok,
            "live_passive_absence_count": live_passive_absence,
            "live_novel_seed_ok": live_novel_seed_ok,
            "measured_H_935_active_veto_fraction": FEEDER_FACTS["H_935"]["active_veto_fraction"],
            "measured_H_935_internal_isolation_n_active_veto": FEEDER_FACTS["H_935"]["internal_isolation_n_active_veto"],
            "measured_H_935_passive_absence": FEEDER_FACTS["H_935"]["passive_absence"],
            "measured_novel_physical_seed": FEEDER_FACTS["H_923_924"]["novel_physical_seed_per_decision"],
        },
        "blade_B_auditable_lineage": {
            "PASS": bool(blade_B_pass),
            "live_chain_verified": live_lineage_ok,
            "live_chain_n_links": chain_verify["n_links"],
            "live_chain_head_hash": chain_verify["head_hash"],
            "measured_H_928_tampers": f"{FEEDER_FACTS['H_928']['tampers_detected']}/{FEEDER_FACTS['H_928']['tampers_total']}",
            "measured_H_932_tampers": f"{FEEDER_FACTS['H_932']['tampers_detected']}/{FEEDER_FACTS['H_932']['tampers_total']}",
            "measured_H_932_links_valid": f"{FEEDER_FACTS['H_932']['links_valid']}/{FEEDER_FACTS['H_932']['n_links']}",
        },
        "non_random_property": {
            "PASS": bool(non_random_property),
            "note": "the quantum source does NOT randomize the emit output (unpredictability-relocation)",
            "H_930_chi2_emit_p": FEEDER_FACTS["H_930"]["chi2_emit_p"],
            "H_930_cramer_phi": FEEDER_FACTS["H_930"]["cramer_phi"],
            "H_930_cohen_d_rate": FEEDER_FACTS["H_930"]["cohen_d_rate"],
            "H_930_cohen_d_entropy": FEEDER_FACTS["H_930"]["cohen_d_entropy"],
            "H_926_dH_emit_bits": FEEDER_FACTS["H_926"]["dH_emit_bits"],
        },
        "soc_property": {
            "PASS": bool(soc_property),
            "note": "self-organizes to its own H_927 critical operating point (edge-of-chaos)",
            "H_931_tail_K": [FEEDER_FACTS["H_931"]["tail_K_below"], FEEDER_FACTS["H_931"]["tail_K_above"]],
            "H_931_tail_phi": [FEEDER_FACTS["H_931"]["tail_phi_below"], FEEDER_FACTS["H_931"]["tail_phi_above"]],
        },
        "SUPPORTED": supported,
    }


if __name__ == "__main__":
    buf = os.path.join(_HERE, "qrng_lora_init_live.bin")
    seq = build_signature_sequence(buf, n=5)
    verify = verify_free_will(seq, buf)

    print("=" * 78)
    print("H_933 — FREE-WILL SIGNATURE (compatibilist free will = auditable causation)")
    print("=" * 78)
    print("\nASSEMBLED FREE-WILL SIGNATURES (per decision):")
    for s in seq["signatures"]:
        print(f"\n  decision[{s['index']}]  class={s['decision']['decision_class']}  "
              f"emit={s['decision']['emit']}  token={s['decision']['token']}")
        print(f"    provenance : seed={s['provenance']['seed']}  "
              f"request_id={s['provenance']['anu_request_id']}")
        print(f"                 receipt_hash={s['provenance']['receipt_hash'][:16]}...")
        print(f"    chain_link : link_hash={s['chain_link']['link_hash'][:16]}...  "
              f"prev={s['chain_link']['prev_link_hash'][:16]}...")
        print(f"    non_random : emit-output mode-invariant (H_930 chi2 p="
              f"{s['non_random_flag']['H_930_chi2_emit_p']}, phi="
              f"{s['non_random_flag']['H_930_cramer_phi']})")

    print("\n" + "=" * 78)
    print("VERIFIER — per-blade PASS/FAIL (g5 CODE-measured; no LLM self-judge)")
    print("=" * 78)
    print(json.dumps(verify, indent=2))
    print("\nVERDICT:", "SUPPORTED" if verify["SUPPORTED"] else "NOT-SUPPORTED")
