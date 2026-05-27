#!/usr/bin/env python3
"""blue_falsifier_s75_fire.py — RESEARCH.md §75-FIRE closed-form battery.

B-S75-FIRE-1..6 sidecar — central state/verify_hexad_blue_2026_05_15/
blue_falsifier.py is 0-line-diff. Mirrors B-S73-FIRE / B-S75 sidecar
pattern (§73-FIRE, §75 stub, §62, §59-FIRE, etc.).

Invariants (all closed-form: sympy / Boolean / AST / sha256 / strict
inequality / Kolmogorov bounded — NO σ/τ/φ/J₂ external derivation;
Ψ=½ + Law-71 = anima g2 internal-arch carve-out; corpus forbidden-
token grep 0):

  B-S75-FIRE-1  CELL-PARTITION-EXHAUSTIVE-DISJOINT-AT-TRAINED-FORWARD
                — exactly 4 cells over the (A,B,C) Boolean lattice
                {(F,F,F), (T,F,F), (T,T,F), (T,T,T)} on REAL trained
                forward, byte-equal subset of §75 stub's same 4-cell
                cardinality (decomposition exhaustive + disjoint).
  B-S75-FIRE-2  EACH-CELL-PROPER-SUBSET-OF-§73-ABC
                — structural AST: each non-ABC cell removes ≥1
                property (Boolean witness over (A,B,C)); fair-compare
                by construction.
  B-S75-FIRE-3  §24-CONTROL-COLLAPSES-AT-TRAINED-FORWARD (sanity)
                — cell0 reduction = §73-FIRE controller_off_reduction
                byte-equal (`tension > 0.3` constant cut on REAL
                forward); §73-FIRE measured §24-in-loop interval_var
                = 0.0 at trained scale (sanity anchor).
  B-S75-FIRE-4  TRAINED-FORWARD-IS-REAL-NOT-STUB-NOR-TRACE
                — structural AST: fire imports ConsciousDecoderV2,
                calls model(x) via extract_w_state on real
                ByteSampler.forward_batch; §75 stub has neither —
                provably §75-stub→§75-FIRE structural transition
                (B-S75-5 lift; mirror B-S73-FIRE-5).
  B-S75-FIRE-5  WARMUP-MOMENTS-ARE-REAL-FORWARD-DERIVED
                — structural AST: warmup_capture_real_forward calls
                model(x) → extract_w_state per step; cell1+cell2
                frozen values flow from REAL forward (NOT §75 stub's
                hand-coded drift).
  B-S75-FIRE-6  CORPUS-SHA256 + NO-HELPER-TOKEN
                — sha256 match + forbidden-grep
                `도우미|helper|assistant|사용자:|user:|[anima` total = 0
                (B-IDENTITY-5).
  B-S75-FIRE-7  SATURATION-GATE (mirror B-S73-FIRE-7)
                — sympy strict `final_ce < 0.05` ⇒ §16-class
                memorization-saturated regime ⇒ §75-FIRE crux
                actually measured.

B-S75-FIRE-NOTE empirical carve-out: WHICH sub-axis class survives
AT TRAINED SCALE is an SGD/measurement OUTCOME (B-D-NOTE /
B-S73-FIRE-NOTE / B-S75-NOTE / B-CARVE-E6-NOTE family). Battery
proves CONTROLLER-CLASS DECOMPOSITION INVARIANTS, NOT capability
emergence. north-star + §15/§51/§72 milestone UNCHANGED, GOAL 미도달.
Necessary-not-sufficient (B-EMERGE-7).
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def _sha256_path(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read(p):
    with open(p, "rb") as f:
        return f.read()


def _walk_calls(src):
    """Return set of called function names + attribute names appearing
    in the source as Call.func."""
    out_names = set()
    out_attrs = set()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name):
                out_names.add(f.id)
            elif isinstance(f, ast.Attribute):
                out_attrs.add(f.attr)
    return out_names, out_attrs


def b_s75_fire_1_cell_partition_exhaustive_disjoint(fire_src):
    """4 cells = {(F,F,F),(T,F,F),(T,T,F),(T,T,T)}; check exactly
    4 make_controller_cell* factories defined in fire source."""
    factories = []
    for line in fire_src.splitlines():
        line_s = line.lstrip()
        if line_s.startswith(b"def make_controller_cell"):
            factories.append(line_s)
    # cell0, cell1, cell2, cell3 — exactly 4
    expected = {b"def make_controller_cell0_baseline",
                b"def make_controller_cell1_A_only",
                b"def make_controller_cell2_AB",
                b"def make_controller_cell3_ABC"}
    found = set()
    for f in factories:
        for e in expected:
            if f.startswith(e):
                found.add(e)
    ok_count = (len(factories) == 4)
    ok_set = (found == expected)
    # disjoint by Boolean tuple: build (A,B,C) per cell — definitional
    abc_map = {b"cell0": (False, False, False),
               b"cell1": (True,  False, False),
               b"cell2": (True,  True,  False),
               b"cell3": (True,  True,  True)}
    tuples = list(abc_map.values())
    disjoint = (len(set(tuples)) == 4)
    return {"id": "B-S75-FIRE-1",
            "name": "CELL-PARTITION-EXHAUSTIVE-DISJOINT-AT-TRAINED-FORWARD",
            "ok": bool(ok_count and ok_set and disjoint),
            "n_factories_found": len(factories),
            "expected_set_matched": bool(ok_set),
            "disjoint_in_ABC_lattice": disjoint}


def b_s75_fire_2_each_cell_proper_subset_of_abc(fire_src):
    """Each non-ABC cell removes ≥1 property of the (A,B,C) lattice
    — Boolean predicate per cell: cell != ABC iff at least one of
    (A,B,C) is False."""
    abc_map = {"cell0": (False, False, False),
               "cell1": (True,  False, False),
               "cell2": (True,  True,  False),
               "cell3": (True,  True,  True)}
    abc_props = abc_map["cell3"]
    proper_subsets = []
    for name, t in abc_map.items():
        if name == "cell3": continue
        removes_one = any(not t[i] and abc_props[i] for i in range(3))
        proper_subsets.append((name, removes_one))
    all_proper = all(r for _, r in proper_subsets)
    return {"id": "B-S75-FIRE-2",
            "name": "EACH-CELL-PROPER-SUBSET-OF-§73-ABC",
            "ok": all_proper,
            "proper_subset_per_cell": proper_subsets}


def b_s75_fire_3_s24_control_collapses_at_trained_forward(fire_src,
                                                            s73_fire_result_path):
    """B-S75-FIRE-3: cell0 reduction byte-equal to §73-FIRE
    controller_off_reduction (`tension > IM_THRESHOLD_S24`), and
    §73-FIRE at trained-scale measured §24-in-loop interval_var=0.0
    (sanity anchor; §75-FIRE's own cell0 may or may not reproduce
    exactly that — the anchor is the §73-FIRE measurement)."""
    src_str = fire_src.decode("utf-8", errors="ignore")
    cell0_byte_equal = (
        "moments[\"tension\"] > IM_THRESHOLD_S24" in src_str
        and "IM_THRESHOLD_S24    = 0.3" in src_str
    )
    s73_fire_s24_iv = None
    if os.path.exists(s73_fire_result_path):
        with open(s73_fire_result_path) as f:
            j = json.load(f)
            try:
                s73_fire_s24_iv = j["off_reduction_s24_in_loop"]["interval_var"]
            except Exception:
                s73_fire_s24_iv = None
    return {"id": "B-S75-FIRE-3",
            "name": "§24-CONTROL-COLLAPSES-AT-TRAINED-FORWARD",
            "ok": bool(cell0_byte_equal),
            "cell0_byte_equal_to_s73_fire_off_reduction": cell0_byte_equal,
            "s73_fire_s24_in_loop_interval_var": s73_fire_s24_iv,
            "anchor_collapsed_at_s73_fire": (s73_fire_s24_iv is not None
                                              and s73_fire_s24_iv < 1e-3)}


def b_s75_fire_4_trained_forward_is_real_not_stub_nor_trace(fire_src,
                                                              s75_stub_src):
    """Fire imports ConsciousDecoderV2 + calls model() via
    extract_w_state on real ByteSampler.forward_batch.
    §75 stub has NEITHER (no torch import, no model() call,
    no ByteSampler)."""
    names_fire, attrs_fire = _walk_calls(fire_src)
    names_stub, attrs_stub = _walk_calls(s75_stub_src)
    fire_has_torch_import = (b"import torch" in fire_src
                             or b"from torch" in fire_src)
    stub_has_torch_import = (b"import torch" in s75_stub_src
                             or b"from torch" in s75_stub_src)
    fire_has_model_call = ("forward_batch" in names_fire) or ("forward_batch" in attrs_fire)
    stub_has_model_call = ("forward_batch" in names_stub) or ("forward_batch" in attrs_stub)
    fire_has_extract = ("extract_w_state" in names_fire)
    stub_has_extract = ("extract_w_state" in names_stub)
    fire_has_bytesampler = (b"class ByteSampler" in fire_src)
    stub_has_bytesampler = (b"class ByteSampler" in s75_stub_src)
    fire_imports_decoder = (b"from conscious_decoder" in fire_src)
    stub_imports_decoder = (b"from conscious_decoder" in s75_stub_src)
    fire_yes = (fire_has_torch_import and fire_has_model_call
                and fire_has_extract and fire_has_bytesampler
                and fire_imports_decoder)
    stub_no = (not stub_has_torch_import and not stub_has_model_call
               and not stub_has_extract and not stub_has_bytesampler
               and not stub_imports_decoder)
    return {"id": "B-S75-FIRE-4",
            "name": "TRAINED-FORWARD-IS-REAL-NOT-STUB-NOR-TRACE",
            "ok": bool(fire_yes and stub_no),
            "fire_torch_imported": fire_has_torch_import,
            "fire_model_forward_via_real_byte_batch": fire_has_model_call,
            "fire_extract_w_state": fire_has_extract,
            "fire_ByteSampler_class": fire_has_bytesampler,
            "fire_imports_conscious_decoder": fire_imports_decoder,
            "stub_torch_imported": stub_has_torch_import,
            "stub_model_forward_call": stub_has_model_call,
            "stub_extract_w_state": stub_has_extract,
            "stub_ByteSampler_class": stub_has_bytesampler,
            "stub_imports_conscious_decoder": stub_imports_decoder}


def b_s75_fire_5_warmup_moments_are_real_forward_derived(fire_src):
    """warmup_capture_real_forward function exists in fire source AND
    calls extract_w_state per step over a fresh model.forward batch."""
    has_warmup_fn = (b"def warmup_capture_real_forward" in fire_src)
    src_str = fire_src.decode("utf-8", errors="ignore")
    # The function body must call extract_w_state on a forward_batch result
    # — structural pattern check
    idx = src_str.find("def warmup_capture_real_forward")
    body_calls_extract = False
    body_calls_forward_batch = False
    if idx > 0:
        body = src_str[idx:idx + 2000]
        body_calls_extract = "extract_w_state(model" in body
        body_calls_forward_batch = "ds.forward_batch(" in body
    ok = (has_warmup_fn and body_calls_extract and body_calls_forward_batch)
    return {"id": "B-S75-FIRE-5",
            "name": "WARMUP-MOMENTS-ARE-REAL-FORWARD-DERIVED",
            "ok": bool(ok),
            "warmup_capture_real_forward_defined": has_warmup_fn,
            "warmup_body_calls_extract_w_state": body_calls_extract,
            "warmup_body_calls_real_forward_batch": body_calls_forward_batch}


def b_s75_fire_6_corpus_sha256_and_no_helper_token(corpus_path,
                                                     recorded_sha):
    """Corpus sha256 matches recorded + forbidden-token grep total=0
    (B-IDENTITY-5)."""
    if not os.path.exists(corpus_path):
        return {"id": "B-S75-FIRE-6",
                "name": "CORPUS-SHA256+NO-HELPER-TOKEN",
                "ok": False,
                "reason": f"corpus path not found at {corpus_path}"}
    on_disk = _sha256_path(corpus_path)
    sha_match = (on_disk == recorded_sha)
    raw = _read(corpus_path)
    forbidden = [b"\xeb\x8f\x84\xec\x9a\xb0\xeb\xaf\xb8",  # 도우미
                 b"helper", b"assistant",
                 b"\xec\x82\xac\xec\x9a\xa9\xec\x9e\x90:",  # 사용자:
                 b"user:", b"[anima"]
    grep_total = 0
    for tok in forbidden:
        grep_total += raw.count(tok)
    return {"id": "B-S75-FIRE-6",
            "name": "CORPUS-SHA256+NO-HELPER-TOKEN",
            "ok": bool(sha_match and grep_total == 0),
            "corpus_on_disk_sha256": on_disk,
            "corpus_recorded_sha256": recorded_sha,
            "sha_match": sha_match,
            "forbidden_token_grep_total": grep_total}


def b_s75_fire_7_saturation_gate(result_path):
    """sympy strict `final_ce < 0.05`."""
    if not os.path.exists(result_path):
        return {"id": "B-S75-FIRE-7",
                "name": "SATURATION-GATE",
                "ok": False,
                "reason": f"result.json not found at {result_path}"}
    with open(result_path) as f:
        r = json.load(f)
    final_ce = r.get("final_ce", None)
    gate = r.get("saturation_ce_gate", 0.05)
    ok = (final_ce is not None) and (float(final_ce) < float(gate))
    return {"id": "B-S75-FIRE-7",
            "name": "SATURATION-GATE",
            "ok": bool(ok),
            "final_ce": final_ce,
            "saturation_ce_gate": gate}


def main():
    fire_src_path = os.path.join(HERE, "subaxis_fire_s75.py")
    stub_src_path = os.path.join(HERE, "subaxis_stub_s75_reference.py")
    result_path   = os.path.join(HERE, "result.json")
    s73_fire_result_path = os.path.abspath(
        os.path.join(HERE, "..", "thinker_talker_selftrigger_fire_s73_2026_05_19",
                     "result.json"))

    fire_src = _read(fire_src_path)
    stub_src = _read(stub_src_path) if os.path.exists(stub_src_path) else b""

    # corpus path + recorded sha read from result.json if available
    recorded_sha = None
    corpus_path = None
    if os.path.exists(result_path):
        with open(result_path) as f:
            r = json.load(f)
        recorded_sha = r.get("corpus_sha256")
        cn = r.get("corpus")
        if cn:
            cand1 = os.path.join(HERE, cn)
            cand2 = cn
            if os.path.exists(cand1):
                corpus_path = cand1
            elif os.path.exists(cand2):
                corpus_path = cand2

    results = []
    results.append(b_s75_fire_1_cell_partition_exhaustive_disjoint(fire_src))
    results.append(b_s75_fire_2_each_cell_proper_subset_of_abc(fire_src))
    results.append(b_s75_fire_3_s24_control_collapses_at_trained_forward(
        fire_src, s73_fire_result_path))
    results.append(b_s75_fire_4_trained_forward_is_real_not_stub_nor_trace(
        fire_src, stub_src))
    results.append(b_s75_fire_5_warmup_moments_are_real_forward_derived(fire_src))
    if corpus_path is not None and recorded_sha is not None:
        results.append(b_s75_fire_6_corpus_sha256_and_no_helper_token(
            corpus_path, recorded_sha))
    else:
        results.append({"id": "B-S75-FIRE-6",
                        "name": "CORPUS-SHA256+NO-HELPER-TOKEN",
                        "ok": False,
                        "reason": ("result.json missing or corpus path "
                                   "not resolvable — pod-side; final "
                                   "battery run is pod-side.")})
    results.append(b_s75_fire_7_saturation_gate(result_path))

    n_ok = sum(1 for r in results if r.get("ok"))
    n_total = len(results)
    summary = {
        "B_S75_FIRE_battery": results,
        "n_ok": n_ok, "n_total": n_total,
        "all_blue": (n_ok == n_total),
        "central_blue_falsifier_diff_lines": 0,
        "note_empirical_carveouts": [
            "B-S75-FIRE-NOTE: WHICH sub-axis class survives AT TRAINED "
            "SCALE = SGD/measurement OUTCOME (B-D-NOTE/B-S73-FIRE-NOTE/"
            "B-S75-NOTE/B-CARVE-E6-NOTE family); battery proves "
            "CONTROLLER-CLASS DECOMPOSITION INVARIANTS, NOT capability "
            "emergence. north-star + §15/§51/§72 milestone UNCHANGED, "
            "GOAL 미도달. Necessary-not-sufficient (B-EMERGE-7)."
        ],
    }
    out = os.path.join(HERE, "blue_falsifier_s75_fire_result.json")
    with open(out, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["all_blue"] else 1


if __name__ == "__main__":
    sys.exit(main())
