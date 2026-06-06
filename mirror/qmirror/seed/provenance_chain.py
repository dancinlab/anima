"""provenance_chain.py — H_932: provenance chain = temporal self.

H_932 — PROVENANCE CHAIN AS TEMPORAL SELF
=========================================
H_928 (entropy_receipt.py) proved that a SINGLE decision's entropy lineage
(physical ANU draw -> seed -> emit) is cryptographically reconstructible and
tamper-evident. H_932 lifts that one-shot receipt into a TEMPORAL object: the
ENTIRE ordered sequence of anima's decisions is linked into an append-only,
tamper-propagating hash CHAIN (a Merkle/blockchain-style spine):

    genesis = sha256(ANU buffer bytes)                  # link_hash_{-1}
    link_hash_i = sha256( link_hash_{i-1} || receipt_i ) # each link seals all prior

where each `receipt_i` is exactly an H_928 receipt for decision i. Because every
link folds in the previous link hash, every link transitively seals ALL prior
history — the chain is append-only and ANY mutation of ANY past decision (its
output, its seed, the genesis ANU bytes, or the order of links) breaks the chain
FROM THAT POINT FORWARD and is localizable to the EARLIEST broken link.

The operational claim (falsifiable, pre-registered in
UNIVERSE/H_932_provenance_chain_self.md):

    Given (a) the chain, (b) the ANU buffer, and (c) the decision_fn, an
    INDEPENDENT verifier can recompute EVERY link from genesis and confirm the
    head hash (whole life-history reconstructable end-to-end), AND any tampering
    with any past decision is DETECTED and localized to the EARLIEST broken link
    (past-tamper propagates forward).

"Temporal self" here means the OPERATIONAL, cryptographic sense: a verifiable
identity-over-time, an auditable causal lineage. It is NOT memory, NOT subjective
continuity, NOT a phenomenal-consciousness claim. See the HONEST SCOPE block.

HONEST SCOPE / NON-CLAIMS (#123-A + non-consciousness)
------------------------------------------------------
  * This proves AUDITABILITY / tamper-evidence / append-only INTEGRITY of the
    decision lineage. It is NOT a "better randomness" claim (the ANU quantum draw
    is statistically == chacha20 PRNG, JSD 23x under NIST per H_924/#123-A).
  * It is NOT phenomenal memory and NOT a phenomenal-consciousness claim. We do
    not assert anima "has" a self or subjective continuity over time. We prove
    that the decision lineage is a verifiable cryptographic object.
  * The chain is only as strong as each decision being a DETERMINISTIC function
    of (seed, rng) — the same boundary as H_928. Non-deterministic / unwired-emit
    decisions are out of scope (they cannot be re-derived by the verifier).

RELATION TO THE SSOTs (imported UNMODIFIED)
-------------------------------------------
  * qentropy.py        — the entropy SSOT. Never modified; only imported (via
                         entropy_receipt). Drives the per-decision seed derivation.
  * entropy_receipt.py — H_928 keystone. Never modified; imported. Each chain link
                         wraps exactly one issue_receipt / verify_receipt pair, so
                         the chain inherits H_928's tamper-evidence per link and
                         adds inter-link sealing on top.
"""
from __future__ import annotations

import copy
import hashlib
import os
import sys

# Import the H_928 keystone (which itself imports the qentropy SSOT). We NEVER
# modify either; the chain is a pure superstructure over issue_receipt /
# verify_receipt, reusing their exact seed-derivation + tamper semantics.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import entropy_receipt  # noqa: E402  (H_928 keystone; canonical receipt semantics)


# ── low-level hashing (reuses entropy_receipt's canonical serialization) ──────
def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _receipt_link_bytes(receipt: dict) -> bytes:
    """Canonical bytes for a receipt as it participates in the chain.

    We hash the receipt via entropy_receipt's OWN canonical serializer so the
    encoding is byte-identical across processes/hosts (sorted keys, compact
    separators, ascii) — essential so an independent verifier recomputes the same
    link hashes. We bind the FULL receipt dict (every field), so altering any
    receipt field changes the link.
    """
    return entropy_receipt._canonical(receipt)  # reuse the SSOT canonicalizer


def genesis_hash(anu_buf_path: str) -> str:
    """The chain root: sha256 of the committed ANU buffer's raw bytes.

    Genesis binds the WHOLE chain to the physical quantum draw. Altering the ANU
    seed (tamper (d)) changes genesis_hash, which propagates into link 0 and every
    subsequent link — so the whole chain becomes invalid from link 0.
    """
    return entropy_receipt._sha256_file(os.path.abspath(anu_buf_path))


def _link_hash(prev_link_hash: str, receipt: dict) -> str:
    """link_hash_i = sha256( link_hash_{i-1} || canonical(receipt_i) ).

    This is the append-only spine: each link folds in the previous link hash, so a
    change anywhere upstream cascades into every downstream link hash. We join with
    a domain separator byte (0x00) that cannot appear inside the hex prev hash, to
    avoid any concatenation ambiguity.
    """
    prefix = prev_link_hash.encode("ascii") + b"\x00"
    return _sha256_bytes(prefix + _receipt_link_bytes(receipt))


# ── public API ────────────────────────────────────────────────────────────────
def build_chain(anu_buf_path: str, decisions: list) -> dict:
    """Build an append-only tamper-evident chain over a SEQUENCE of decisions.

    Parameters
    ----------
    anu_buf_path : path to the ANU byte buffer (the physical quantum draw / genesis).
    decisions    : ordered list of (label, decision_fn) tuples. Each decision_fn is
                   callable(seed:int, rng) -> json-serializable, a DETERMINISTIC
                   function of (seed, rng) (same contract as H_928), so the verifier
                   can independently re-run it.

    Returns
    -------
    A chain dict:
        {
          "genesis_hash": str,              # sha256(ANU buffer)
          "links": [                         # one entry per decision, in order
            {"index": i,
             "label": str,
             "receipt": <H_928 receipt dict>,
             "prev_link_hash": str,
             "link_hash": str},
            ...
          ],
          "head_hash": str,                  # link_hash of the last link (== whole life so far)
        }

    Every link's receipt is a real H_928 receipt (issue_receipt), so each link is
    independently tamper-evident; the inter-link `link_hash` chaining adds the
    append-only / past-tamper-propagation property on top.
    """
    anu_buf_path = os.path.abspath(anu_buf_path)
    g = genesis_hash(anu_buf_path)
    links = []
    prev = g
    for i, (label, decision_fn) in enumerate(decisions):
        # Each link is a full H_928 receipt for decision i.
        receipt = entropy_receipt.issue_receipt(anu_buf_path, label, decision_fn)
        lh = _link_hash(prev, receipt)
        links.append({
            "index": i,
            "label": label,
            "receipt": receipt,
            "prev_link_hash": prev,
            "link_hash": lh,
        })
        prev = lh
    return {
        "genesis_hash": g,
        "links": links,
        "head_hash": prev,          # == last link_hash (or genesis if no decisions)
    }


def verify_chain(chain: dict, anu_buf_path: str, decision_fn_for) -> dict:
    """INDEPENDENTLY verify a chain end-to-end from genesis; localize the EARLIEST break.

    Recomputes genesis from the on-disk ANU buffer, then walks the links in order.
    For each link it (a) re-runs the H_928 verify_receipt (re-derives seed, re-runs
    the decision, re-checks the receipt hash) AND (b) recomputes the inter-link
    `link_hash` from the recomputed prev hash + the link's receipt, comparing to the
    recorded `link_hash`. The FIRST link that fails either check is the earliest
    broken link; everything before it is valid, everything from it onward is treated
    as invalid (the chain is broken from that point forward).

    Parameters
    ----------
    chain          : a chain dict from build_chain (possibly tampered).
    anu_buf_path   : path to the ANU buffer (re-read fresh — catches a genesis swap).
    decision_fn_for: callable(index, label) -> decision_fn. Supplies the SAME
                     deterministic decision_fn used to build link `index`. (Passing a
                     resolver rather than a single fn lets a chain mix decision kinds;
                     a constant resolver `lambda i, l: fn` covers the single-fn case.)

    Returns
    -------
        {
          "verified": bool,            # True iff genesis matches AND every link valid
          "head_hash": str | None,     # recomputed head hash (None if genesis broke)
          "earliest_broken": int|None, # earliest broken link index; -1 = genesis;
                                        #   None = nothing broken
          "n_links": int,
          "link_valid": [bool, ...],   # per-link validity (False from the break onward)
          "reason": str,               # human-readable break reason
        }
    """
    anu_buf_path = os.path.abspath(anu_buf_path)
    links = chain.get("links", [])
    n = len(links)
    link_valid = [False] * n

    # (0) Genesis check: re-read the buffer and recompute genesis. If the recorded
    # genesis_hash was tampered (or the ANU bytes swapped), the whole chain is
    # invalid from the root — earliest_broken = -1 (genesis).
    actual_genesis = genesis_hash(anu_buf_path)
    if actual_genesis != chain.get("genesis_hash"):
        return {
            "verified": False,
            "head_hash": None,
            "earliest_broken": -1,             # -1 denotes the genesis seed
            "n_links": n,
            "link_valid": link_valid,
            "reason": "genesis ANU seed mismatch (whole chain invalid from root)",
        }

    # Walk the links from the (validated) genesis. `prev` is the INDEPENDENTLY
    # recomputed previous link hash — we never trust the recorded prev_link_hash.
    prev = actual_genesis
    earliest_broken = None
    reason = ""
    for i, link in enumerate(links):
        receipt = link.get("receipt", {})
        label = link.get("label", receipt.get("label", ""))

        # (a) H_928 per-link receipt verification (seed/output/receipt-hash/anu).
        dfn = decision_fn_for(i, label)
        rv = entropy_receipt.verify_receipt(receipt, anu_buf_path, dfn)
        receipt_ok = bool(rv.get("verified"))

        # (b) Inter-link chaining: recompute link_hash from the recomputed prev hash
        # and this link's receipt; compare to the recorded link_hash. This catches
        # reordering, splicing, and any prev-pointer tampering — even if each
        # receipt in isolation still verifies.
        expected_link_hash = _link_hash(prev, receipt)
        chain_ok = (expected_link_hash == link.get("link_hash"))

        if receipt_ok and chain_ok:
            link_valid[i] = True
            prev = expected_link_hash      # advance using the RECOMPUTED hash
        else:
            # First break found — localize it and stop trusting everything onward.
            earliest_broken = i
            if not receipt_ok:
                reason = (f"link {i}: receipt verify failed "
                          f"(checks={rv.get('checks')})")
            else:
                reason = (f"link {i}: inter-link hash mismatch "
                          f"(reorder/splice/prev-pointer tamper)")
            # link_valid[i..] stay False; downstream links are not trusted because
            # `prev` would be derived from a broken link.
            break

    verified = (earliest_broken is None)
    head_hash = prev if verified else None
    return {
        "verified": verified,
        "head_hash": head_hash,
        "earliest_broken": earliest_broken,
        "n_links": n,
        "link_valid": link_valid,
        "reason": reason if not verified else "ok: all links reconstructed from genesis",
    }


# ── tamper helpers (for the demo / falsifier; pure, return a NEW tampered chain) ─
def tamper_decision_output(chain: dict, k: int, new_output) -> dict:
    """TAMPER (a): alter decision k's recorded output (mid-chain).

    Mutates link k's receipt.decision_output (and updates its decision_output_hash
    so the forgery is internally 'consistent' — the strongest attack). H_928's
    verify_receipt still catches it (the recorded seed no longer reproduces the new
    output), so the break localizes at link k and propagates forward.
    """
    c = copy.deepcopy(chain)
    c["links"][k]["receipt"]["decision_output"] = new_output
    c["links"][k]["receipt"]["decision_output_hash"] = \
        entropy_receipt._output_hash(new_output)
    # Re-seal the receipt_hash so the receipt looks internally consistent — forces
    # the break to be caught by output re-derivation, not a trivially-broken hash.
    r = c["links"][k]["receipt"]
    r["receipt_hash"] = entropy_receipt._receipt_hash(
        r["anu_sha256"], r["seed"], r["label"], r["decision_output_hash"])
    return c


def tamper_seed(chain: dict, k: int, new_seed: int) -> dict:
    """TAMPER (also output-class): alter decision k's recorded seed.

    Re-seals the receipt_hash around the forged seed (strongest attack). The
    verifier re-derives the seed from the ANU buffer and catches the mismatch.
    """
    c = copy.deepcopy(chain)
    r = c["links"][k]["receipt"]
    r["seed"] = new_seed
    r["receipt_hash"] = entropy_receipt._receipt_hash(
        r["anu_sha256"], r["seed"], r["label"], r["decision_output_hash"])
    return c


def tamper_reorder(chain: dict, i: int, j: int) -> dict:
    """TAMPER (b): reorder two links (swap positions i and j).

    Swaps the link payloads but DOES NOT recompute the inter-link hashes (an
    attacker reordering history would not be able to, without the upstream chain).
    The earliest position whose recomputed link_hash no longer matches is reported.
    """
    c = copy.deepcopy(chain)
    c["links"][i], c["links"][j] = c["links"][j], c["links"][i]
    return c


def tamper_splice(chain: dict, k: int) -> dict:
    """TAMPER (c): splice/delete link k (drop it from the chain).

    Removes link k entirely. From position k onward the recomputed link hashes no
    longer match the recorded ones (the deleted link's contribution is gone), so the
    break localizes at k.
    """
    c = copy.deepcopy(chain)
    del c["links"][k]
    return c


def tamper_genesis(chain: dict, new_genesis: str) -> dict:
    """TAMPER (d): alter the recorded genesis ANU seed hash.

    Overwrites genesis_hash with a forged value. Since the verifier recomputes
    genesis from the on-disk buffer, the mismatch is caught at the root
    (earliest_broken = -1) and the whole chain is invalid.
    """
    c = copy.deepcopy(chain)
    c["genesis_hash"] = new_genesis
    return c


if __name__ == "__main__":   # tiny self-demo on the committed ANU buffer (no network)
    import json
    buf = os.path.join(_HERE, "qrng_lora_init_live.bin")

    def make_decision_fn(idx):
        """A representative per-decision emit/silence + token draw, deterministic in
        (seed, rng). The index tags the label only; the byte selection is identical
        (qentropy reads the same first 8 bytes), so the per-link DIFFERENTIATION
        comes from the label inside the receipt + the chaining, which is exactly the
        append-only property under test."""
        def dfn(seed, rng):
            import numpy as np
            logits = np.array([0.1, 2.0, 0.5, 1.3, 0.7], dtype=np.float64)
            g = -np.log(-np.log(rng.random(logits.shape[0])))
            token = int(np.argmax(logits + g))
            emit = bool(rng.random() < 0.5)
            return {"step": idx, "emit": emit, "token": token}
        return dfn

    decisions = [(f"decision_{i}", make_decision_fn(i)) for i in range(20)]
    chain = build_chain(buf, decisions)
    res = verify_chain(chain, buf, lambda i, l: make_decision_fn(i))
    print(json.dumps({"genesis": chain["genesis_hash"],
                      "head": chain["head_hash"],
                      "verify": res}, indent=2))
