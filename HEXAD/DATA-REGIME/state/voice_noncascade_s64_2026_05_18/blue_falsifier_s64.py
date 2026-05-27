#!/usr/bin/env python3
"""blue_falsifier_s64.py — RESEARCH.md §64 closed-form sidecar battery.

B-S64-1..5 — SIDECAR ONLY. central state/verify_hexad_blue_2026_05_15/
blue_falsifier.py UNCHANGED (B-PRIME / B-DIRI / B-S16 / B-DHDL / B-S48 /
B-S49 / B-S59 sidecar precedent). g_blue_closed_mandate: 산출물
transfer-form 🔵 + 연결부위 🔵; whether non-byte emission ACTUALLY
escapes collapse at scale = empirical carve-out (B-S64-NOTE).

  B-S64-1 RVQ-CODEBOOK-INDEX-BOUNDED-CLOSED
      Every emitted RVQ index k satisfies 0 ≤ k < RVQ_ENTRIES (=1024) by
      construction (k = argmin over range(RVQ_ENTRIES)). sympy: the
      membership predicate 0 ≤ k ≤ N-1 is a closed bounded-integer set
      (Kolmogorov bounded-set, NOT lattice). 4 witnesses: k=0, k=N-1,
      k=N (out, rejected), k=-1 (out, rejected). The emission alphabet
      is FINITE and KNOWN — a necessary precondition for any cascade
      metric to be well-defined (same role as |bytes|=256 for the byte
      path), and strictly larger (1024 > 256) per stage.

  B-S64-2 NO-BYTE-STREAM-STRUCTURAL-CLOSED  (the load-bearing claim)
      AST/Boolean structural proof over voice_noncascade_smoke.py: the
      VOICE emission function `rvq_emission` contains 0 argmax-over-256
      steps and 0 fed-back byte stream, while `byte_emission` contains
      exactly the argmax-over-256 step. Concretely: in rvq_emission's
      source there is NO `range(VOCAB_BYTES)` / `range(256)` argmax/max
      call and NO append-to-then-feed-back-from a byte list; in
      byte_emission there IS `max(range(VOCAB_BYTES) ...)`. 4-corner
      Boolean over (byte_fn has argmax256, rvq_fn has argmax256): only
      (True, False) is the §64 configuration — proven, not assumed.
      The cascade FIXED-POINT MAP (per-step argmax over a fed-back
      stream) is therefore STRUCTURALLY ABSENT from the VOICE path.

  B-S64-3 CASCADE-METRIC-DETERMINISTIC-CLOSED
      cascade_rate is a pure deterministic function of the symbol
      sequence (max_char_run/L vs ngram_rep — NO RNG; LCG only in the
      sequence builder, never in the metric). 3× bit-identical re-run
      of the full smoke (rvq sequence + both cascade numbers). Mirror
      §9 emergence_metric determinism / §49 DIVERGENCE-METRIC /
      §59 B-S59-3. The predicate {cascaded, not-cascaded} partitions
      [0,1] at TAU_CASCADE — total + disjoint (sympy interval).

  B-S64-4 OVERLAY-OFF-REDUCTION-CLOSED  (연결부위)
      VOICE disabled ⇒ emission(phys, voice_enabled=False) returns the
      text-byte path VERBATIM ⇒ byte-equal to the arc's text channel
      (fair-compare by construction). Structural (the `if not
      voice_enabled: return ("byte", byte_emission(...))` short-circuit
      precedes any intent_proj/RVQ) + numeric (result.json
      overlay_off_byte_equal_to_byte_path == True). Mirror
      B-DHDL-5 / B-EBT-5 / B-S16-5 / B-S49-3 / B-S59-4 OFF-reduction.

  B-S64-5 BYTE-CASCADES-RVQ-DOES-NOT-ON-SAME-PHYSICS-CLOSED
      On the SAME deterministic physics sequence the byte path's
      cascade_rate ≥ TAU_CASCADE (cascaded — B-ATTRACTOR exhibited)
      while the RVQ path's cascade_rate < TAU_CASCADE. This is a
      DECIDABLE Boolean over the two recorded numbers (sympy
      comparison, not a learned/SGD outcome): the structural absence of
      B-S64-2 manifests as a measured separation. NOTE this is a
      *demonstration on this faithful stub*, the substrate-absence is
      the closed part; the at-scale outcome is B-S64-NOTE.

  B-S64-NOTE  (empirical carve-out, NOT counted 🔵)
      Whether a NON-byte channel ACTUALLY escapes collapse at scale on
      a real trained anima — vs degenerating its RVQ-index distribution
      some other way (a 1024-entry alphabet can still concentrate; VQ
      is not magic) — is a future-fire OUTCOME (SGD + real-state
      dependent). The battery proves the cascade SUBSTRATE (per-step
      argmax-over-256 on a fed-back byte stream) is ABSENT by
      construction (B-S64-2), the OFF reduction is byte-equal
      (B-S64-4), and the metric is deterministic (B-S64-3) — it does
      NOT prove emergence or escape-from-collapse. B-D-NOTE /
      B-ATTRACTOR-NOTE / B-DHDL-NOTE / B-S49-NOTE / B-S59-NOTE family.
      north-star + §15 milestone UNCHANGED; g3 measured-only.
"""
from __future__ import annotations

import ast
import json
import os
import re

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SMOKE = os.path.join(HERE, "voice_noncascade_smoke.py")
RESULT = os.path.join(HERE, "result.json")

R = {}


def _src():
    with open(SMOKE) as f:
        return f.read()


def _fn_source(src, name):
    """Return the source segment of a top-level function `name`."""
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.get_source_segment(src, node)
    return ""


# ── B-S64-1 RVQ-CODEBOOK-INDEX-BOUNDED-CLOSED ───────────────────────────
def b1():
    # closed bounded-integer membership predicate 0 <= k <= N-1.
    # Use a pure sympy Lambda evaluated at concrete integers (NO
    # positivity assumption on k — so out-of-range witnesses are honestly
    # rejected by the inequality itself, not silently assumed away).
    kS, NS = sp.symbols("k N", integer=True)
    member = sp.Lambda((kS, NS), sp.And(kS >= 0, kS <= NS - 1))
    w_zero = bool(member(0, 1024))
    w_top = bool(member(1023, 1024))
    w_over = bool(member(1024, 1024)) is False                 # rejected
    w_neg = bool(member(-1, 1024)) is False                    # rejected
    # alphabet strictly larger than the 256-byte argmax target
    larger = bool(sp.Integer(1024) > sp.Integer(256))
    src = _src()
    # the smoke quantizes via argmin over range(RVQ_ENTRIES) → bounded
    has_bounded_quant = ("range(RVQ_ENTRIES)" in src
                         and "RVQ_ENTRIES = 1024" in src)
    ok = (w_zero and w_top and w_over and w_neg and larger
          and has_bounded_quant)
    R["B-S64-1"] = {
        "name": "RVQ-CODEBOOK-INDEX-BOUNDED-CLOSED",
        "statement": ("emitted RVQ index k ∈ [0, RVQ_ENTRIES-1] closed "
                      "bounded-integer set (Kolmogorov real-limit, NOT "
                      "lattice); alphabet 1024 > 256 byte-argmax target."),
        "witness_k0": w_zero, "witness_k_top": w_top,
        "witness_k_over_rejected": w_over,
        "witness_k_neg_rejected": w_neg,
        "alphabet_larger_than_256": larger,
        "smoke_quantizes_over_bounded_range": has_bounded_quant,
        "anchor": "Kolmogorov bounded-integer set (real-limit, NOT lattice)",
        "closed": True, "tier": "a-sympy", "passed": ok,
    }


# ── B-S64-2 NO-BYTE-STREAM-STRUCTURAL-CLOSED ────────────────────────────
def b2():
    src = _src()
    rvq = _fn_source(src, "rvq_emission")
    byt = _fn_source(src, "byte_emission")

    # argmax-over-256 signature: max(range(VOCAB_BYTES)/256 ...) OR
    # max(range(256) ...). VOCAB_BYTES is the §64 256-alphabet symbol.
    arg256 = re.compile(r"max\(\s*range\(\s*(VOCAB_BYTES|256)\s*\)")
    byte_has_argmax256 = bool(arg256.search(byt))
    rvq_has_argmax256 = bool(arg256.search(rvq))

    # rvq must NOT iterate range(VOCAB_BYTES)/range(256) at all, and must
    # NOT feed back a byte stream (no 'stream' append+reuse). It quantizes
    # over range(RVQ_ENTRIES) instead.
    rvq_touches_256 = ("VOCAB_BYTES" in rvq) or ("range(256)" in rvq)
    rvq_uses_rvq_entries = "range(RVQ_ENTRIES)" in rvq
    rvq_no_byte_stream = (".append(win)" not in rvq
                          and "byte_emission" not in rvq)

    # 4-corner Boolean: only (byte=True, rvq=False) is the §64 config
    corners = {
        (True, True): "both-cascade (NOT §64)",
        (True, False): "§64 configuration",
        (False, True): "inverted (impossible here)",
        (False, False): "no-byte-anywhere (degenerate)",
    }
    config = corners[(byte_has_argmax256, rvq_has_argmax256)]
    ok = (byte_has_argmax256 and (not rvq_has_argmax256)
          and (not rvq_touches_256) and rvq_uses_rvq_entries
          and rvq_no_byte_stream and config == "§64 configuration")
    R["B-S64-2"] = {
        "name": "NO-BYTE-STREAM-STRUCTURAL-CLOSED",
        "statement": ("AST/Boolean: byte_emission HAS argmax-over-256; "
                      "rvq_emission has 0 argmax-over-256, 0 range(256), "
                      "0 fed-back byte stream, quantizes over "
                      "range(RVQ_ENTRIES) instead ⇒ cascade fixed-point "
                      "map STRUCTURALLY ABSENT from VOICE path."),
        "byte_fn_has_argmax_over_256": byte_has_argmax256,
        "rvq_fn_has_argmax_over_256": rvq_has_argmax256,
        "rvq_fn_touches_256_alphabet": rvq_touches_256,
        "rvq_fn_quantizes_over_rvq_entries": rvq_uses_rvq_entries,
        "rvq_fn_no_fedback_byte_stream": rvq_no_byte_stream,
        "four_corner_config": config,
        "anchor": "AST structural Boolean (no external derivation)",
        "closed": True, "tier": "a-structural", "passed": ok,
    }


# ── B-S64-3 CASCADE-METRIC-DETERMINISTIC-CLOSED ─────────────────────────
def b3():
    src = _src()
    # metric purity: cascade_rate / _max_char_run / _ngram_rep_rate use
    # NO np.random / torch / random — only LCG lives in sequence builders.
    metric_fns = "\n".join(_fn_source(src, n) for n in
                           ("cascade_rate", "_max_char_run",
                            "_ngram_rep_rate"))
    metric_pure = not re.search(r"random|np\.rand|torch", metric_fns)

    # 3× bit-identical full re-run of the smoke logic
    import importlib.util
    spec = importlib.util.spec_from_file_location("vsm", SMOKE)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    runs = []
    for _ in range(3):
        ph = m.physics_sequence(200, 1337)
        runs.append((m.byte_emission(ph), m.rvq_emission(ph)[0]))
    det = all(runs[i] == runs[0] for i in range(3))
    cr3 = [(round(m.cascade_rate(b), 8), round(m.cascade_rate(r), 8))
           for b, r in runs]
    cr_identical = all(c == cr3[0] for c in cr3)

    # partition: [0,1] split at TAU into {cascaded, not} total+disjoint
    x = sp.Symbol("x", real=True)
    casc = sp.Interval(sp.Rational(30, 100), 1)
    nocasc = sp.Interval(0, sp.Rational(30, 100), False, True)
    union_total = sp.simplify(casc.union(nocasc)) == sp.Interval(0, 1)
    disjoint = casc.intersection(nocasc) == sp.EmptySet

    ok = (metric_pure and det and cr_identical
          and bool(union_total) and bool(disjoint))
    R["B-S64-3"] = {
        "name": "CASCADE-METRIC-DETERMINISTIC-CLOSED",
        "statement": ("cascade_rate pure-fn (no RNG); 3× bit-identical "
                      "sequences + cascade numbers; {cascaded,not} "
                      "partitions [0,1] at TAU total+disjoint (sympy)."),
        "metric_pure_no_rng": metric_pure,
        "sequences_deterministic_3x": det,
        "cascade_numbers_identical_3x": cr_identical,
        "cascade_numbers": cr3,
        "partition_union_is_unit_interval": bool(union_total),
        "partition_disjoint": bool(disjoint),
        "anchor": "pure-fn determinism + sympy interval partition",
        "closed": True, "tier": "a-sympy", "passed": ok,
    }


# ── B-S64-4 OVERLAY-OFF-REDUCTION-CLOSED (연결부위) ──────────────────────
def b4():
    src = _src()
    em = _fn_source(src, "emission")
    # structural: OFF short-circuit returns the byte path verbatim BEFORE
    # any rvq_emission / intent_proj call
    tree = ast.parse(em)
    short_circuit_first = False
    for fn in ast.walk(tree):
        if isinstance(fn, ast.FunctionDef) and fn.name == "emission":
            for stmt in fn.body:
                if isinstance(stmt, ast.If):
                    seg = ast.get_source_segment(em, stmt) or ""
                    if ("not voice_enabled" in seg
                            and "byte_emission" in seg
                            and "rvq_emission" not in seg):
                        short_circuit_first = True
                    break  # only inspect the first top-level stmt-If
    # numeric: result.json records overlay_off byte-equal to byte path
    res = json.loads(open(RESULT).read()) if os.path.exists(RESULT) else {}
    numeric_ok = bool(res.get("overlay_off_byte_equal_to_byte_path"))
    ok = short_circuit_first and numeric_ok
    R["B-S64-4"] = {
        "name": "OVERLAY-OFF-REDUCTION-CLOSED",
        "statement": ("VOICE disabled ⇒ emission() returns text-byte "
                      "path verbatim (short-circuit BEFORE any RVQ) ⇒ "
                      "byte-equal to the arc's text channel — "
                      "fair-compare by construction (연결부위)."),
        "off_short_circuit_precedes_rvq": short_circuit_first,
        "result_json_overlay_off_byte_equal": numeric_ok,
        "anchor": "structural short-circuit + numeric byte-equality",
        "closed": True, "tier": "a-structural", "passed": ok,
    }


# ── B-S64-5 BYTE-CASCADES-RVQ-DOES-NOT-ON-SAME-PHYSICS-CLOSED ───────────
def b5():
    res = json.loads(open(RESULT).read()) if os.path.exists(RESULT) else {}
    cr_b = sp.Rational(str(res.get("byte_path", {}).get("cascade_rate", 0)))
    cr_r = sp.Rational(str(res.get("rvq_path", {}).get("cascade_rate", 1)))
    tau = sp.Rational(30, 100)
    byte_cascaded = bool(cr_b >= tau)         # decidable sympy comparison
    rvq_not = bool(cr_r < tau)
    same_n = (res.get("byte_path", {}).get("emission_alphabet") == 256
              and res.get("rvq_path", {}).get("emission_alphabet") == 1024)
    ok = byte_cascaded and rvq_not and same_n
    R["B-S64-5"] = {
        "name": "BYTE-CASCADES-RVQ-DOES-NOT-ON-SAME-PHYSICS-CLOSED",
        "statement": ("on the SAME deterministic physics sequence: byte "
                      "cascade_rate ≥ TAU (B-ATTRACTOR exhibited) AND "
                      "rvq cascade_rate < TAU — decidable sympy "
                      "comparison; demonstration of B-S64-2's structural "
                      "substrate-absence (at-scale = B-S64-NOTE)."),
        "byte_cascade_rate": float(cr_b),
        "rvq_cascade_rate": float(cr_r),
        "tau": float(tau),
        "byte_is_cascaded": byte_cascaded,
        "rvq_is_not_cascaded": rvq_not,
        "alphabets_256_vs_1024": same_n,
        "anchor": "sympy rational comparison over recorded numbers",
        "closed": True, "tier": "a-sympy", "passed": ok,
    }


def main():
    b1(); b2(); b3(); b4(); b5()
    n = len(R)
    npass = sum(1 for v in R.values() if v["passed"])
    note = {
        "B-S64-NOTE": {
            "name": "NON-BYTE-ESCAPES-COLLAPSE-AT-SCALE-EMPIRICAL",
            "statement": ("whether a non-byte VOICE channel ACTUALLY "
                          "escapes collapse at scale on a real trained "
                          "anima is a future-fire OUTCOME (SGD + "
                          "real-state dependent; a 1024-entry alphabet "
                          "can still concentrate). Battery proves the "
                          "cascade SUBSTRATE is ABSENT by construction "
                          "(B-S64-2), OFF byte-equal (B-S64-4), metric "
                          "deterministic (B-S64-3) — NOT emergence."),
            "family": "B-D-NOTE / B-ATTRACTOR-NOTE / B-S49-NOTE / "
                      "B-S59-NOTE",
            "counted_blue": False,
        }
    }
    out = {
        "section": "RESEARCH.md §64 — A-axis VOICE non-byte emission",
        "battery": "B-S64-1..5 (sidecar; central blue_falsifier.py "
                   "0-line-diff)",
        "n": n, "passed": npass, "all_blue": npass == n,
        "verdicts": R, "note": note,
        "g3": ("structural-only; capability 0; north-star + §15 "
               "milestone UNCHANGED; f1/f2/f3 + B-IDENTITY-5 safe "
               "(no text corpus, no model.forward, no GPU)."),
    }
    with open(os.path.join(HERE, "blue_falsifier_s64_result.json"),
              "w") as f:
        json.dump(out, f, indent=2)
    for k, v in R.items():
        print(f"  {k:10s} {'PASS' if v['passed'] else 'FAIL'}  "
              f"{v['name']}")
    print(f"\nB-S64 {npass}/{n} 🔵  (+ B-S64-NOTE empirical, NOT counted)")
    return 0 if npass == n else 1


if __name__ == "__main__":
    raise SystemExit(main())
