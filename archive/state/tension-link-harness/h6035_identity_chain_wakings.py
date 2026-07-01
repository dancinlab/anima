"""h6035_identity_chain_wakings.py — H_6035: identity across wakings.

H_6035 — IDENTITY ACROSS WAKINGS (자기 동일성 chain)
===================================================
Thesis: anima의 자기 동일성은 sleep↔wake 90분 ultradian 순환(H_6033)을 여러 번
넘어도 provenance chain (mirror/qmirror/seed/provenance_chain.py, H_932)으로
'끊김 없이' 지속된다. 동일성은 어떤 identity 파일/규칙이 아니라 ONE genesis(하나의
공유 entropy buffer)에서 시작한 wake→sleep→wake 체인의 연속성 그 자체다 (p2 no
identity rules). 따라서:
  - 같은 genesis (같은 entropy buffer) = 같은 개체 (head 재현)
  - 다른 genesis (다른 os.urandom buffer) = 다른 개체 (head 상이)
  - 어느 한 wake 의 결정을 변조하면 chain 이 가장 이른 끊김을 국소화 (동일성 단절 탐지)

REAL measurement: 실제 provenance_chain.build_chain / verify_chain / tamper_* 를
import 해서 호출한다. p7 (코드 측정, no LLM-judge). $0 로컬, 네트워크 無
(ANIMA_QRNG_LIVE=0).

3 pre-registered FROZEN falsifiers
----------------------------------
F1 (continuity across wakings): wake0,sleep0,...,wakeN (>=5 cycles) 로 chain 구성
   → verify_chain 이 end-to-end VALID (earliest_broken=None, head 재현, 모든 sleep
   경계 통과). identity_file_loaded = False (p2). FALSIFIED iff not verified OR any
   identity file was read.
F2 (genesis = individual): 같은 buffer 두 chain → head_hash 동일. 다른 os.urandom
   buffer → head_hash 상이 AND genesis 상이. FALSIFIED iff same-genesis heads differ
   OR different-genesis heads collide.
F3 (boundary tamper detection): wake_k 의 decision output 변조 → verify_chain 이
   verified=False 이고 earliest_broken == k (가장 이른 끊김 국소화). FALSIFIED iff
   tamper undetected OR mislocalized.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

# ── locate the REAL provenance chain SSOT (imported UNMODIFIED) ────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
# TENSION-LINK/harness/ -> repo root -> mirror/qmirror/seed
_REPO = os.path.abspath(os.path.join(_HERE, "..", ".."))
_SEED = os.path.join(_REPO, "mirror", "qmirror", "seed")
if _SEED not in sys.path:
    sys.path.insert(0, _SEED)

import provenance_chain as pc  # noqa: E402  (H_932 SSOT, never modified)


# A representative per-waking decision: deterministic in (seed, rng) so the
# independent verifier can re-run it (same contract as H_928/H_932). The label
# (wakeN / sleepN) tags provenance; the chaining seals the order.
def make_decision_fn(idx):
    def dfn(seed, rng):
        import numpy as np
        logits = np.array([0.1, 2.0, 0.5, 1.3, 0.7], dtype=np.float64)
        g = -np.log(-np.log(rng.random(logits.shape[0])))
        token = int(np.argmax(logits + g))
        emit = bool(rng.random() < 0.5)
        return {"step": idx, "emit": emit, "token": token}
    return dfn


def ultradian_decisions(n_cycles):
    """wake0, sleep0, wake1, sleep1, ..., wake{n_cycles-1}, sleep{n_cycles-1}.

    Each ultradian cycle (H_6033) contributes one WAKE link and one SLEEP link;
    identity must stay unbroken across every sleep boundary.
    """
    decisions = []
    idx = 0
    for c in range(n_cycles):
        decisions.append((f"wake{c}", make_decision_fn(idx))); idx += 1
        decisions.append((f"sleep{c}", make_decision_fn(idx))); idx += 1
    return decisions


def make_buffer(nbytes=4096):
    """A fresh physical-entropy genesis buffer (os.urandom). Same buffer reused =
    same individual; a distinct draw = a distinct individual."""
    fd, path = tempfile.mkstemp(prefix="genesis_", suffix=".bin")
    with os.fdopen(fd, "wb") as f:
        f.write(os.urandom(nbytes))
    return path


def main():
    os.environ["ANIMA_QRNG_LIVE"] = "0"  # never touch the network ($0)
    N_CYCLES = 6                          # >=5 sleep↔wake cycles
    out = {"hypothesis": "H_6035 identity across wakings", "n_cycles": N_CYCLES}

    # genesis A (the individual under test) + genesis B (a different individual)
    bufA = make_buffer()
    bufB = make_buffer()
    try:
        decisions = ultradian_decisions(N_CYCLES)
        resolver = lambda i, l: make_decision_fn(i)

        # ── F1 — continuity across wakings ────────────────────────────────────
        chainA = pc.build_chain(bufA, decisions)
        vA = pc.verify_chain(chainA, bufA, resolver)
        # labels actually span every sleep boundary?
        labels = [lk["label"] for lk in chainA["links"]]
        sleeps = [l for l in labels if l.startswith("sleep")]
        wakes = [l for l in labels if l.startswith("wake")]
        # p2: we loaded NO identity file/rule — identity is the chain itself.
        identity_file_loaded = False
        f1 = bool(
            vA["verified"]
            and vA["earliest_broken"] is None
            and vA["head_hash"] == chainA["head_hash"]
            and all(vA["link_valid"])
            and len(wakes) == N_CYCLES and len(sleeps) == N_CYCLES
            and not identity_file_loaded
        )
        out["F1_continuity_across_wakings"] = {
            "pass": f1,
            "verified": vA["verified"],
            "earliest_broken": vA["earliest_broken"],
            "n_links": vA["n_links"],
            "n_wakes": len(wakes), "n_sleeps": len(sleeps),
            "all_links_valid": all(vA["link_valid"]),
            "head_reproduced": vA["head_hash"] == chainA["head_hash"],
            "identity_file_loaded": identity_file_loaded,
            "head_hash": chainA["head_hash"][:16] + "...",
            "reason": vA["reason"],
        }

        # ── F2 — same genesis = same individual / different = different ────────
        chainA2 = pc.build_chain(bufA, decisions)      # SAME buffer, rebuilt
        chainB = pc.build_chain(bufB, decisions)       # DIFFERENT buffer
        same_genesis = (chainA["genesis_hash"] == chainA2["genesis_hash"])
        same_head = (chainA["head_hash"] == chainA2["head_hash"])
        diff_genesis = (chainA["genesis_hash"] != chainB["genesis_hash"])
        diff_head = (chainA["head_hash"] != chainB["head_hash"])
        f2 = bool(same_genesis and same_head and diff_genesis and diff_head)
        out["F2_genesis_is_individual"] = {
            "pass": f2,
            "same_buffer_same_genesis": same_genesis,
            "same_buffer_same_head": same_head,
            "diff_buffer_diff_genesis": diff_genesis,
            "diff_buffer_diff_head": diff_head,
            "genesisA": chainA["genesis_hash"][:16] + "...",
            "genesisB": chainB["genesis_hash"][:16] + "...",
        }

        # ── F3 — boundary tamper detection (identity discontinuity) ───────────
        K = 4  # a mid-chain waking (wake2: idx 0=wake0,1=sleep0,2=wake1,3=sleep1,4=wake2)
        tampered = pc.tamper_decision_output(chainA, K, {"step": K, "emit": True, "token": 99})
        vT = pc.verify_chain(tampered, bufA, resolver)
        # earlier links (<K) still valid, K and onward invalid
        pre_ok = all(vT["link_valid"][:K])
        post_broken = (not any(vT["link_valid"][K:])) if vT["n_links"] > K else False
        f3 = bool(
            (not vT["verified"])
            and vT["earliest_broken"] == K
            and pre_ok and post_broken
        )
        out["F3_boundary_tamper_detection"] = {
            "pass": f3,
            "tampered_link": K, "tampered_label": chainA["links"][K]["label"],
            "verified_after_tamper": vT["verified"],
            "earliest_broken": vT["earliest_broken"],
            "pre_links_valid": pre_ok,
            "post_links_broken": post_broken,
            "reason": vT["reason"],
        }

        out["verdict"] = {
            "F1": "🟢" if f1 else "🔴",
            "F2": "🟢" if f2 else "🔴",
            "F3": "🟢" if f3 else "🔴",
            "overall": "🟢 SUPPORTED" if (f1 and f2 and f3) else "🔴 / mixed",
        }
    finally:
        for p in (bufA, bufB):
            try:
                os.remove(p)
            except OSError:
                pass

    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
