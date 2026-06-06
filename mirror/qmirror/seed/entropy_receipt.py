"""entropy_receipt.py — provenance-as-identity ("free-will receipt") for anima decisions.

H_928 — PROVENANCE-AS-IDENTITY
==============================
This module makes the entropy lineage of ANY anima decision INDEPENDENTLY VERIFIABLE
and TAMPER-EVIDENT. The operational claim (falsifiable):

    Given (a) a decision output, (b) its recorded provenance receipt, and (c) the ANU
    byte buffer, an INDEPENDENT verifier can DETERMINISTICALLY RECONSTRUCT the exact
    seed and RE-DERIVE the identical decision — proving the decision provably
    originated from that physical quantum draw — AND any tampering (swapping the ANU
    bytes, the recorded seed, or the output) is DETECTED.

In other words: "this choice came from physical quantum event X (request_id ...) at
time T" becomes an auditable, cryptographically-checkable RECEIPT. That is the
operational meaning of substrate-native free-will *provenance*.

HONEST SCOPE / NON-CLAIMS (#123-A QA6 audit, NIST SP 800-22 7/7)
----------------------------------------------------------------
  * This is an AUDITABILITY / tamper-evidence result, NOT a "better randomness" claim.
    The STATISTICAL quality of ANU quantum entropy == chacha20 PRNG (JSD 0.000433,
    23x under the NIST threshold). We do NOT assert the quantum draw is "more random".
  * The value proven here is exactly what H_924 identified as the value of quantum
    entropy: PROVENANCE · auditability · physical-origin ontology — the bit
    distribution is irrelevant to this hypothesis.
  * This is NOT a phenomenal-consciousness claim. We are not asserting anima "has"
    free will or subjective experience. We are proving that the entropy→decision
    lineage of a decision is cryptographically reconstructible and tamper-evident —
    a property of the audit trail, nothing more.

RELATION TO THE ENTROPY SSOT (qentropy.py — NOT modified, only imported)
------------------------------------------------------------------------
The receipt's seed MUST be derived the SAME way the real runtime derives it, or the
receipt would be inconsistent with the actual decision path. We therefore IMPORT
`qentropy` and drive the decision through `qentropy.rng(label)` /
`qentropy.qentropy_seed(label)` under quantum mode, with the ANU buffer pinned via
the `ANIMA_QRNG_BUF` env that qentropy's resolution-order (a) already honors. This
guarantees the receipt is consistent with the canonical SSOT path — the same code an
on-chip / SW decision would take.

Seed-derivation note (matches qentropy exactly): in quantum mode `qentropy_seed()`
reads the FIRST 8 bytes of the resolved pool (cursor starts at 0 on a fresh resolve)
and computes `int.from_bytes(b, "little") & ((1<<63)-1)`. The `label` only tags
provenance; it does NOT change which bytes are read. The verifier reproduces this in
a FRESH process (fresh cursor), so issue and verify see the identical 8 bytes.

RECEIPT SHAPE
-------------
    {
      "anu_sha256":          sha256(ANU buffer bytes)               # binds the physical draw
      "anu_request_id":      request_id from provenance.jsonl       # physical event id (or null)
      "entropy_mode":        "quantum" | "quantum_fallback_prng" ...# from qentropy.last_provenance
      "tier":                "anu_explicit" | "anu_committed" | ... # from qentropy.last_provenance
      "seed":                int (qentropy_seed-derived 63-bit seed) # the derived seed
      "label":               str                                    # decision label
      "decision_output":     <json-serializable>                    # the decision the seed produced
      "decision_output_hash":sha256(canonical(decision_output))     # binds the output
      "receipt_hash":        sha256(canonical({anu_sha256, seed, label, decision_output_hash}))
    }

`receipt_hash` binds the four load-bearing fields together: swap ANY of the ANU bytes,
the seed, the label, or the output, and the recomputed receipt_hash diverges. That is
the tamper-evidence anchor.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import os
import sys

# Import the entropy SSOT. We NEVER modify it; we drive decisions through it so the
# receipt's seed derivation is identical to the real runtime path.
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import qentropy  # noqa: E402  (the unmodified SSOT)

# Where the live ANU puller records its provenance rows (one JSON object per line).
_PROVENANCE_JSONL = os.path.join(_HERE, "provenance.jsonl")


# ── canonical serialization (stable across processes → stable hashes) ─────────
def _canonical(obj) -> bytes:
    """Deterministic, cross-process-stable JSON bytes for hashing.

    sort_keys + compact separators + ensure_ascii give a byte-identical encoding
    regardless of dict insertion order or platform — essential so issue and verify
    (potentially different processes/hosts) compute the SAME hash over the SAME data.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("utf-8")


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sha256_file(path: str) -> str:
    """sha256 of a file's raw bytes (the ANU buffer). Read fresh every call so the
    verifier genuinely re-reads the on-disk buffer (catches a byte swap)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _output_hash(decision_output) -> str:
    """sha256 over the canonical-serialized decision output (binds the exact output)."""
    return _sha256_bytes(_canonical(decision_output))


def _receipt_hash(anu_sha256: str, seed: int, label: str, output_hash: str) -> str:
    """The tamper-evidence anchor: one sha256 binding the four load-bearing fields.

    Any mutation of the ANU bytes (→ anu_sha256), the seed, the label, or the output
    (→ output_hash) changes this hash. The verifier recomputes it independently."""
    return _sha256_bytes(_canonical({
        "anu_sha256": anu_sha256,
        "seed": seed,
        "label": label,
        "decision_output_hash": output_hash,
    }))


def _lookup_request_id(anu_sha256: str) -> str | None:
    """Find the physical-event request_id for this ANU buffer by its sha256.

    This is the END-TO-END LINEAGE link: the committed buffer's sha256 maps, via the
    puller's provenance.jsonl, to the exact physical ANU draw (e.g.
    request_id anu_legacy_1778042160) that produced it. Returns None if no row matches
    (e.g. a fresh buffer not yet recorded) — absence is honest, not an error."""
    if not os.path.exists(_PROVENANCE_JSONL):
        return None
    rid = None
    with open(_PROVENANCE_JSONL, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            # last matching row wins (the most recent recording of these exact bytes)
            if row.get("sha256") == anu_sha256 and row.get("request_id"):
                rid = row["request_id"]
    return rid


def _seed_from_buffer(anu_buf_path: str, label: str) -> tuple[int, dict]:
    """Derive the seed THE SAME WAY qentropy does, with the ANU buffer pinned.

    We pin the buffer via ANIMA_QRNG_BUF (qentropy resolution-order (a)) and force
    quantum mode, then RELOAD qentropy so its module-level env snapshot + pool reset
    to this buffer with a FRESH cursor (cursor=0). This is exactly what a real
    quantum-mode decision seeded from this buffer would compute, and it is
    reproducible in any fresh verifier process.

    Returns (seed, provenance_dict_from_qentropy).
    """
    os.environ["ANIMA_ENTROPY_MODE"] = "quantum"
    os.environ["ANIMA_QRNG_BUF"] = os.path.abspath(anu_buf_path)
    os.environ["ANIMA_QRNG_LIVE"] = "0"      # never go to the network during a receipt
    importlib.reload(qentropy)               # re-snapshot env + reset pool/cursor
    seed = qentropy.qentropy_seed(label)     # reads first 8 bytes of THIS buffer
    return seed, qentropy.last_provenance()


# ── public API ────────────────────────────────────────────────────────────────
def issue_receipt(anu_buf_path: str, label: str, decision_fn) -> dict:
    """Run `decision_fn` under quantum mode seeded from the ANU buffer; emit a RECEIPT.

    Parameters
    ----------
    anu_buf_path : path to the ANU byte buffer (the physical quantum draw).
    label        : decision label (tags provenance; does not change byte selection).
    decision_fn  : callable(seed:int, rng:np.random.Generator) -> json-serializable.
                   The decision MUST be a deterministic function of (seed, rng) so the
                   verifier can re-run it identically. `rng` is qentropy.rng(label),
                   i.e. a numpy Generator quantum-seeded from THIS buffer.

    Returns the receipt dict (see module docstring for the shape).
    """
    anu_buf_path = os.path.abspath(anu_buf_path)
    anu_sha256 = _sha256_file(anu_buf_path)
    request_id = _lookup_request_id(anu_sha256)

    # Derive the seed via the SSOT (pinned buffer, fresh cursor), then build the rng.
    seed, prov = _seed_from_buffer(anu_buf_path, label)
    # qentropy.rng(label) draws ANOTHER 8 bytes (cursor advances); to keep the rng a
    # pure function of the recorded `seed`, we seed numpy directly from it — this is
    # exactly what qentropy.rng does internally (default_rng(qentropy_seed)) but pinned
    # to the seed we recorded, so the verifier reproduces it from `seed` alone.
    import numpy as np  # local import: numpy is a qentropy dep, always available here
    decision_rng = np.random.default_rng(seed)

    decision_output = decision_fn(seed, decision_rng)
    output_hash = _output_hash(decision_output)
    rhash = _receipt_hash(anu_sha256, seed, label, output_hash)

    return {
        "anu_sha256": anu_sha256,
        "anu_request_id": request_id,
        "entropy_mode": prov.get("mode"),
        "tier": prov.get("tier"),
        "seed": seed,
        "label": label,
        "decision_output": decision_output,
        "decision_output_hash": output_hash,
        "receipt_hash": rhash,
    }


def verify_receipt(receipt: dict, anu_buf_path: str, decision_fn) -> dict:
    """INDEPENDENTLY verify a receipt against the ANU buffer + decision_fn.

    Re-does every binding from scratch and compares to the recorded values:

      1. anu_sha_match     — re-read the buffer, recompute its sha256; must equal
                             receipt.anu_sha256 (else: the ANU bytes were SWAPPED).
      2. seed_match        — re-derive the seed the SAME way qentropy does from the
                             buffer; must equal receipt.seed (else: seed ALTERED, or
                             the buffer no longer produces it).
      3. output_match      — re-run decision_fn(seed, rng), hash the output; must equal
                             receipt.decision_output_hash (else: output FORGED).
      4. receipt_hash_match— recompute the binding hash over (anu_sha256, seed, label,
                             output_hash); must equal receipt.receipt_hash (else: the
                             receipt itself was TAMPERED).

    `verified` is True iff ALL FOUR checks pass.

    Returns {"verified": bool, "checks": {anu_sha_match, seed_match, output_match,
             receipt_hash_match}}.
    """
    anu_buf_path = os.path.abspath(anu_buf_path)

    # (1) Re-read the buffer and recompute its sha256 — detects a byte swap.
    actual_anu_sha = _sha256_file(anu_buf_path)
    anu_sha_match = (actual_anu_sha == receipt.get("anu_sha256"))

    # (2) Re-derive the seed from the buffer THE SAME WAY qentropy does.
    derived_seed, _prov = _seed_from_buffer(anu_buf_path, receipt.get("label", ""))
    seed_match = (derived_seed == receipt.get("seed"))

    # (3) Re-run the decision from the RECORDED seed and hash the output. We use the
    # recorded seed (not the re-derived one) so this check isolates output-forgery
    # from seed-tampering: seed_match already covers the seed; here we ask "does the
    # recorded seed reproduce the recorded output?".
    import numpy as np
    recorded_seed = receipt.get("seed")
    output_match = False
    if isinstance(recorded_seed, int):
        decision_rng = np.random.default_rng(recorded_seed)
        recomputed_output = decision_fn(recorded_seed, decision_rng)
        recomputed_output_hash = _output_hash(recomputed_output)
        output_match = (recomputed_output_hash == receipt.get("decision_output_hash"))

    # (4) Recompute the binding hash from the receipt's own fields — detects any
    # mutation of the four bound fields (incl. a hand-edited receipt_hash).
    recomputed_rhash = _receipt_hash(
        receipt.get("anu_sha256"),
        receipt.get("seed"),
        receipt.get("label"),
        receipt.get("decision_output_hash"),
    )
    receipt_hash_match = (recomputed_rhash == receipt.get("receipt_hash"))

    checks = {
        "anu_sha_match": bool(anu_sha_match),
        "seed_match": bool(seed_match),
        "output_match": bool(output_match),
        "receipt_hash_match": bool(receipt_hash_match),
    }
    return {"verified": all(checks.values()), "checks": checks}


if __name__ == "__main__":   # tiny self-demo on the committed ANU buffer (no network)
    buf = os.path.join(_HERE, "qrng_lora_init_live.bin")

    def demo_decision(seed: int, rng):
        # A trivial but representative decision: sample a token from fixed logits via
        # the quantum-seeded rng (Gumbel-max argmax), plus draw 8 bits. Deterministic
        # in (seed, rng) so it is re-derivable by the verifier.
        import numpy as np
        logits = np.array([0.1, 2.0, 0.5, 1.3, 0.7], dtype=np.float64)
        g = -np.log(-np.log(rng.random(logits.shape[0])))
        token = int(np.argmax(logits + g))
        bits = rng.integers(0, 2, size=8).tolist()
        return {"token": token, "bits": bits}

    r = issue_receipt(buf, "demo", demo_decision)
    v = verify_receipt(r, buf, demo_decision)
    print(json.dumps({"receipt": r, "verify": v}, indent=2))
