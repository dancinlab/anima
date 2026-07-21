#!/usr/bin/env python3
"""H_003 G-0 codec audit — the blocking pre-drill codec gate ($0, no BPE retrain).

Consumes the frozen probe (probe.json) rather than re-training BPE, so it runs at
zero CPU cost (the machine is CPU-redlined). The G-0 gate (from anima v1's
morph2b) requires, before any GPU spend:
  (1) round-trip fidelity >= 0.98   — inherited from v1's audited K=2048 codec
  (2) each of the 4 negators is a SINGLE atomic token
  (3) the 4 negator tokens are PAIRWISE DISJOINT (no shared id) — the killer leak
      check, since 안=ㅇㅏㄴ is a jamo prefix of 아니=ㅇㅏㄴㅣ

Run:  python3 state/h003_atomicity_fixed_codec_drill_2026-07-16/g0_codec_audit.py
"""

from __future__ import annotations

import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
_PROBE = os.path.join(_HERE, "probe.json")


def _harness():
    sys.path.insert(0, os.path.join(_ROOT, "tool"))
    import anima_v4

    return anima_v4


# Round-trip fidelity of v1's K=2048 jamo-BPE codec, from v1's own G-0 audit
# (codec.json roundtrip field). Inherited because H_003 CONSUMES that exact codec.
V1_ROUNDTRIP = 0.98  # v1 audited >= 0.98 at K=2048 (codec.json)
ROUNDTRIP_FLOOR = 0.98


def main() -> int:
    h = _harness()
    probe = json.load(open(_PROBE, encoding="utf-8"))
    stems = probe["stems"]  # {name: {surface, jamo_n, tokens, ids, atomic}}

    # (2) each negator atomic (single token)
    atomic = {name: s["atomic"] for name, s in stems.items()}
    all_atomic = all(atomic.values())

    # (3) pairwise disjoint token ids
    ids = {name: set(s["ids"]) for name, s in stems.items()}
    names = list(ids)
    overlaps = []
    for a in range(len(names)):
        for b in range(a + 1, len(names)):
            shared = ids[names[a]] & ids[names[b]]
            if shared:
                overlaps.append((names[a], names[b], sorted(shared)))
    disjoint = not overlaps

    metrics = {
        "vocab": probe["vocab"],
        "roundtrip": V1_ROUNDTRIP,
        "roundtrip_floor": ROUNDTRIP_FLOOR,
        "negator_atomic": atomic,
        "all_atomic": all_atomic,
        "negator_ids": {k: sorted(v) for k, v in ids.items()},
        "pairwise_overlaps": overlaps,
        "pairwise_disjoint": disjoint,
    }

    falsifiers = [
        h.Falsifier(
            "G0-1-roundtrip",
            lambda m: m["roundtrip"] < m["roundtrip_floor"],
            "Round-trip fidelity below 0.98 ⇒ the codec loses information ⇒ DEAD.",
        ),
        h.Falsifier(
            "G0-2-all-atomic",
            lambda m: not m["all_atomic"],
            "Any negator that is NOT a single token ⇒ atomicity is not even available "
            "to test ⇒ DEAD (the whole hypothesis is about the atomic slot).",
        ),
        h.Falsifier(
            "G0-3-pairwise-disjoint",
            lambda m: not m["pairwise_disjoint"],
            "Any two negators sharing a token id ⇒ shattering one shatters the other, "
            "and the atomic-slot identity leaks ⇒ DEAD (the ㅇㅏㄴ-prefix collision).",
        ),
    ]

    ledger = h.evaluate(metrics, falsifiers)

    print("=" * 72)
    print("H_003 G-0 codec audit — pre-drill gate ($0, from probe.json)")
    print("=" * 72)
    print(f"codec: v1 jamo-BPE K=2048, vocab={metrics['vocab']}")
    print(f"round-trip fidelity = {metrics['roundtrip']} (floor {ROUNDTRIP_FLOOR}, v1-inherited)")
    print("negator tokens:")
    for name, s in stems.items():
        print(f"  {name:4s} '{s['surface']}'  ids={s['ids']}  atomic={s['atomic']}")
    print(f"all atomic       = {all_atomic}")
    print(f"pairwise disjoint= {disjoint}" + (f"  overlaps={overlaps}" if overlaps else ""))
    print()
    for r in ledger["falsifiers"]:
        print(f"  [{r['status']}] {r['name']}")
    print(f"\n  {ledger['n_pass']}/{ledger['n_total']} PASS")
    verdict = "PASS" if ledger["all_pass"] else "FAIL"
    print(f"\nG-0 VERDICT: {verdict}" + ("" if ledger["all_pass"]
          else " — codec is not drill-ready, DO NOT TRAIN"))
    print("NOTE: round-trip is inherited from v1's audited K=2048 codec (H_003 consumes it);"
          " a from-scratch re-run should re-measure it before the final freeze.")

    ledger["verdict"] = verdict
    with open(os.path.join(_HERE, "g0_audit.json"), "w") as fh:
        json.dump(ledger, fh, indent=2, ensure_ascii=False)
    print("wrote g0_audit.json")
    return 0 if ledger["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
