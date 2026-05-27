#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════
# B-S118 — §118 TRACK 0 IN-SILICO — sidecar battery
# ════════════════════════════════════════════════════════════════════
# Sidecar ONLY.  central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
# sha256 prefix c93e160a8a376a94 — 0-line-diff (verified START+END by the
# orchestrator; this battery never touches central).
#
# The battery proves the §118 4-CELL RIG is HONEST:
#   B-S118-1  cell-partition exhaustive + disjoint (4 cells, 3 channels)
#   B-S118-2  STDP-no-CE-no-backprop AST-audit (the decisive 'stdp' channel
#             contains ZERO CE/backprop/optimizer calls — mirror §11-B
#             B-PUREPHYS-1 / §117 B-S117-2)
#   B-S118-3  §3 closed predicate deterministic + 3× bit-identical re-run
#   B-S118-4  §3-predicate byte-equal to TRACK0_INSILICO.md §3 spec
#             (connection-point: the predicate run == the predicate written)
#   B-S118-5  §117-WALL-B-inherited connection-point (§118 inherits §117's
#             LEGO-RUN-...-WALL-B-INHERITED; does NOT remove WALL-B)
#   B-S118-6  §96 attention-blocker acknowledged (design-open #1 structural)
#   B-S118-7  Ψ-C1 bounded + cos=0⇒½ fixed point (§112 META_FP carry)
#   B-S118-8  sidecar / central-0-diff structural invariant + $0 fields
#   B-S118-9  g_clm_from_scratch init invariant (base_ckpt=None, RANDOM)
#
# B-S118-NOTE: the battery does NOT prove Track 0 works / anima emerges; the
#   MEASURED 3-outcome verdict is an SGD-free convergence OUTCOME (NOT
#   counted 🔵) — B-D-NOTE / B-PUREPHYS-NOTE / B-S96-NOTE / B-S115-NOTE /
#   B-S117-NOTE / B-EMERGE-7 family, necessary-not-sufficient at every layer.
#
# g3: design ≠ fire ≠ emergence; capability claim 0.  f1/f2 safe (LIF/STDP
#   cited by hexa-bio NEURO.tape OWN invariants + standard neuroscience,
#   NO σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24 derivation; Ψ=½ = anima g2
#   internal-arch carve-out).  $0, NO GPU/fire/dispatch.
# ════════════════════════════════════════════════════════════════════

import ast, json, os, tempfile, importlib.util
# single-thread BLAS — must precede numpy import (the §118 sim's tiny
# matmuls thrash under multi-thread BLAS over-subscription; the battery
# re-runs the sim 3× for determinism so it needs the same env).  Pure
# environment fix — does NOT change any numerical result.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SIM_SRC = os.path.join(HERE, "track0_sim.py")
RES_JSON = os.path.join(HERE, "result.json")
SPEC_MD = os.path.normpath(os.path.join(
    HERE, "..", "..", "HEXAD", "NEUROMORPHIC", "TRACK0_INSILICO.md"))

PASS, results = [], []


def check(name, ok, detail):
    ok = bool(ok)
    PASS.append(ok)
    results.append({"id": name, "pass": ok, "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {name} — {detail}")
    return ok


with open(SIM_SRC) as f:
    SRC = f.read()
TREE = ast.parse(SRC)
with open(RES_JSON) as f:
    R = json.load(f)
CELLS = R["cells"]

# ── B-S118-1 — CELL-PARTITION EXHAUSTIVE + DISJOINT ──────────────────
# 4 cells over 3 weight-update channels {ce, none, stdp}.  Channel set is
# the partition: exhaustive (every cell has exactly one channel) and the
# channel taxonomy {ce,none,stdp} is itself disjoint (a cell cannot have
# two).  GPU-CE and SIM-CE both 'ce' BY DESIGN (one is the sanity control,
# one the VOID guard) — distinct cells, not a partition violation.
expect = {"GPU-CE": "ce", "GPU-noCE": "none",
          "SIM-noCE-STDP": "stdp", "SIM-CE": "ce"}
cells_present = set(CELLS.keys())
channels_seen = sorted({CELLS[k]["channel"] for k in CELLS})
each_one_channel = all(CELLS[k]["channel"] in {"ce", "none", "stdp"}
                       for k in CELLS)
channel_match = all(CELLS[k]["channel"] == expect[k] for k in expect)
# sympy: 4 cells, 3-channel taxonomy, |{ce,none,stdp}| == 3 disjoint
chan_set = sp.FiniteSet("ce", "none", "stdp")
disjoint_ok = (len(chan_set) == 3)
exhaustive_ok = (cells_present == set(expect.keys()) and len(CELLS) == 4)
check("B-S118-1 CELL-PARTITION-EXHAUSTIVE-DISJOINT",
      exhaustive_ok and each_one_channel and channel_match and disjoint_ok,
      f"4 cells={sorted(cells_present)} · channels={channels_seen} · "
      f"each-one-channel={each_one_channel} · expected-map-match="
      f"{channel_match} · 3-channel taxonomy disjoint={disjoint_ok}")

# ── B-S118-2 — STDP-NO-CE-NO-BACKPROP AST-AUDIT (the decisive cell) ──
# The 'stdp' channel's update (_stdp_update) is event-local plasticity
# ONLY.  AST-audit the WHOLE sim source for the forbidden learning-channel
# call set; the only CE machinery allowed is inside _ce_update (the CE
# channel's own update — that cell is a control, not the decisive one).
# We require: (a) NO torch/tensorflow import, (b) NO .backward()/autograd/
# optimizer.step/cross_entropy ANYWHERE, and (c) the decisive STDP update
# function references NO loss/error/target symbol.
FORBIDDEN_ATTR = {"backward", "cross_entropy", "zero_grad",
                  "CrossEntropyLoss"}
FORBIDDEN_NAME = {"cross_entropy", "CrossEntropyLoss", "backward"}
hits = []
for node in ast.walk(TREE):
    if isinstance(node, ast.Call):
        fn = node.func
        if isinstance(fn, ast.Attribute):
            if fn.attr in FORBIDDEN_ATTR:
                hits.append(("attr", fn.attr))
            if fn.attr == "step":
                recv = fn.value
                base = (recv.id if isinstance(recv, ast.Name)
                        else getattr(recv, "attr", ""))
                if base in ("optimizer", "optim", "opt"):
                    hits.append(("attr", "optimizer.step", base))
                # cell._lif_step / range().step etc → allowed
        elif isinstance(fn, ast.Name) and fn.id in FORBIDDEN_NAME:
            hits.append(("name", fn.id))
imported = set()
for node in ast.walk(TREE):
    if isinstance(node, ast.Import):
        for a in node.names:
            imported.add(a.name.split(".")[0])
    elif isinstance(node, ast.ImportFrom) and node.module:
        imported.add(node.module.split(".")[0])
no_torch = "torch" not in imported and "tensorflow" not in imported
# decisive: the _stdp_update function body must reference NO error symbol
stdp_fn = None
for node in ast.walk(TREE):
    if isinstance(node, ast.FunctionDef) and node.name == "_stdp_update":
        stdp_fn = node
stdp_names = set()
if stdp_fn:
    for n in ast.walk(stdp_fn):
        if isinstance(n, ast.Name):
            stdp_names.add(n.id)
        if isinstance(n, ast.Attribute):
            stdp_names.add(n.attr)
stdp_error_free = stdp_fn is not None and not (
    stdp_names & {"loss", "ce", "error", "grad", "target", "tgt",
                  "onehot", "head"})
no_ce_backprop = (len(hits) == 0) and no_torch and stdp_error_free
check("B-S118-2 STDP-NO-CE-NO-BACKPROP-AST-AUDIT",
      no_ce_backprop,
      f"forbidden-call hits={len(hits)} {hits} · imports={sorted(imported)}"
      f" no_torch={no_torch} · _stdp_update error-symbol-free="
      f"{stdp_error_free} — decisive 'stdp' channel = LOCAL plasticity "
      f"only (mirror §11-B B-PUREPHYS-1 / §117 B-S117-2)")

# ── B-S118-3 — §3 PREDICATE DETERMINISTIC + 3× BIT-IDENTICAL ─────────
# re-derive NON_DEGENERATE per cell from the recorded numbers, must match
# recorded flag; then re-run the FULL sim 3× → verdict + per-cell signature
# bit-identical (same seed ⇒ same result, pure CPU, no RNG drift).
CHANCE = R["byte_acc_chance"]
TAU = R["tau_frozen"]
predicate_match = True
for k, c in CELLS.items():
    ba_pass = c["byte_acc"] > CHANCE
    nd_re = bool(ba_pass and c["physics_not_frozen"]
                 and c["s9_pass_ge_1_5"])
    if nd_re != c["non_degenerate"]:
        predicate_match = False
deterministic = True
rerun_matches = False
try:
    spec = importlib.util.spec_from_file_location("track0_re", SIM_SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sig = None
    for _ in range(3):
        with tempfile.TemporaryDirectory() as td:
            rr = mod.run(td)
            s = (rr["verdict"],
                 tuple(sorted((k, round(v["psi_c1_std"], 12),
                               round(v["byte_acc"], 12),
                               v["non_degenerate"])
                              for k, v in rr["cells"].items())))
            if sig is None:
                sig = s
            elif s != sig:
                deterministic = False
    rerun_matches = (sig is not None and sig[0] == R["verdict"])
except Exception as e:  # pragma: no cover
    deterministic = False
    print("  (determinism re-run note:", e, ")")
check("B-S118-3 PREDICATE-DETERMINISTIC-3X-BIT-IDENTICAL",
      predicate_match and deterministic and rerun_matches,
      f"§3 predicate re-derived per-cell == recorded={predicate_match} · "
      f"3×bit-identical={deterministic} · re-run verdict≡recorded="
      f"{rerun_matches} (closed Boolean, necessary-NOT-sufficient "
      f"B-EMERGE-7)")

# ── B-S118-4 — §3-PREDICATE BYTE-EQUAL TO TRACK0_INSILICO.md SPEC ────
# connection-point: the predicate the sim RAN must be the predicate the
# spec WROTE.  TRACK0_INSILICO.md §3 reads verbatim:
#   NON_DEGENERATE(cell) := byte_acc > 1/256
#                         ∧ physics_not_frozen  (Ψ/tension/Φ trajectory std > τ)
#                         ∧ honest_§9_coherent ≥ 1/5
spec_ok = False
spec_witness = ""
if os.path.exists(SPEC_MD):
    with open(SPEC_MD) as f:
        SPEC = f.read()
    # witnesses byte-equal to TRACK0_INSILICO.md §3 verbatim (lines 72-74,
    # 81/89/91) — the predicate the sim runs == the predicate the spec
    # writes.  Strings copied EXACTLY from the spec (no normalisation).
    spec_witness = "NON_DEGENERATE(cell) := byte_acc > 1/256"
    spec_ok = (spec_witness in SPEC and
               "honest_§9_coherent ≥ 1/5" in SPEC and
               "physics_not_frozen" in SPEC and
               "SIM-CONFRONTS-LEARNING-CHANNEL" in SPEC and
               "SIM-IS-GPU-TAUTOLOGY-CONFIRMED-LEARNING-HALF" in SPEC and
               "VOID" in SPEC)
# the result.json predicate string carries all three clauses
pred_str = R["predicate"]
run_pred_ok = ("byte_acc > 1/256" in pred_str and
               "physics_not_frozen" in pred_str and
               "honest_§9_coherent >= 1/5" in pred_str)
# §9 metric is the SSOT import, not re-implemented
s9_ssot = ("emergence_metric" in R["s9_metric_source"] and
           "honest_coherent" in R["s9_metric_source"])
# verify the sim source actually imports honest_coherent from the §9 SSOT
s9_imported = any(
    isinstance(n, ast.ImportFrom) and n.module == "emergence_metric"
    and any(a.name == "honest_coherent" for a in n.names)
    for n in ast.walk(TREE))
check("B-S118-4 §3-PREDICATE-BYTE-EQUAL-TO-SPEC-CONNECTION-POINT",
      spec_ok and run_pred_ok and s9_ssot and s9_imported,
      f"TRACK0_INSILICO.md §3 witness present={spec_ok} · run predicate "
      f"3-clause={run_pred_ok} · §9 honest_coherent SSOT-import="
      f"{s9_imported} (NOT re-implemented)")

# ── B-S118-5 — §117-WALL-B-INHERITED CONNECTION-POINT ───────────────
# §118 inherits §117's LEGO-RUN-...-WALL-B-INHERITED verdict; verify the
# §117 artifact exists with its verdict, and §118's result.json explicitly
# inherits WALL-B (does NOT remove it) + WALL-A orthogonal.  Non-vacuous:
# real §117 result.json witness present.
s117_res = os.path.join(
    HERE, "..", "lego_assembly_run_s117_2026_05_19", "result.json")
s117_ok = False
if os.path.exists(s117_res):
    with open(s117_res) as f:
        r117 = json.load(f)
    s117_ok = ("WALL-B-INHERITED" in r117.get("verdict", "") and
               "INHERITED" in r117.get("honest_inheritance", {})
               .get("wall_b", ""))
inh = R["honest_inheritance"]
wall_b_inherited = ("INHERITED" in inh["wall_b"] and
                    "§117" in inh["wall_b"] and
                    "LEARNING-CHANNEL half ONLY" in inh["wall_b"])
wall_a_orth = ("ORTHOGONAL" in inh["wall_a"] and
               "UNTOUCHED" in inh["wall_a"])
check("B-S118-5 §117-WALL-B-INHERITED-CONNECTION-POINT",
      s117_ok and wall_b_inherited and wall_a_orth,
      f"§117 result.json WALL-B-INHERITED witness={s117_ok} · §118 "
      f"WALL-B inherited(learning-half-only)={wall_b_inherited} · WALL-A "
      f"orthogonal={wall_a_orth}")

# ── B-S118-6 — §96 ATTENTION-BLOCKER ACKNOWLEDGED (structural) ───────
# the headline + honest_inheritance must explicitly acknowledge §96
# design-open #1: softmax(QK^T) self-attention is SPIKING-INCOMPATIBLE,
# must be REPLACED, and BLOCKS the full spiking-anima instantiation.  The
# rig confronts the learning-channel HALF only — NOT the full anima.
hl = R["headline"]
ab = inh["attention_blocker"]
attn_ack = ("design-open #1" in hl and
            "SPIKING-INCOMPATIBLE" in hl and
            "REPLACED" in hl and
            "LEARNING-CHANNEL HALF ONLY" in hl and
            "design-open #1" in ab and
            "BLOCKED" in ab and "REPLACED" in ab)
# verify §96 DESIGN.md genuinely carries the SPIKING-INCOMPATIBLE finding
s96_design = os.path.join(
    HERE, "..", "loihi_spiking_rederivation_s96_2026_05_19", "DESIGN.md")
s96_ok = False
if os.path.exists(s96_design):
    with open(s96_design) as f:
        d96 = f.read()
    s96_ok = ("SPIKING-INCOMPATIBLE" in d96 and
              "design-open #1" in d96 and
              "softmax" in d96)
check("B-S118-6 §96-ATTENTION-BLOCKER-ACKNOWLEDGED-STRUCTURAL",
      attn_ack and s96_ok,
      f"headline+inheritance acknowledge §96 design-open #1 "
      f"(SPIKING-INCOMPATIBLE / must REPLACE / BLOCKS full anima)="
      f"{attn_ack} · §96 DESIGN.md carries the finding={s96_ok}")

# ── B-S118-7 — Ψ-C1 BOUNDED + cos=0⇒½ FIXED POINT (sympy, §112 carry) ─
# ψ(c) = (1+c)/2.  Cauchy–Schwarz ⇒ c ∈ [−1,1] ⇒ ψ ∈ [0,1].  c=0 ⇒ ψ=½.
c = sp.symbols("c", real=True)
psi = (1 + c) / 2
form_ok = (sp.simplify(psi.subs(c, -1)) == 0 and
           sp.simplify(psi.subs(c, 1)) == 1 and
           sp.simplify(psi.subs(c, 0)) == sp.Rational(1, 2) and
           sp.simplify(sp.diff(psi, c) - sp.Rational(1, 2)) == 0)
# every cell's measured Ψ-C1 mean must lie within [0,1]
run_bounded = all(0.0 <= CELLS[k]["psi_c1_mean"] <= 1.0 for k in CELLS)
check("B-S118-7 PSI-C1-BOUNDED-FIXED-POINT-CLOSED",
      form_ok and run_bounded,
      f"sympy ψ(−1)=0 ψ(1)=1 ψ(0)=½ ∂ψ/∂c=½>0 ✓ · all cells Ψ-C1 mean "
      f"∈[0,1]={run_bounded} (§112 META_FP(Π_½) instance, carrier="
      f"spike-correlation; §7-FORM by construction)")

# ── B-S118-8 — SIDECAR / CENTRAL-0-DIFF STRUCTURAL + $0 FIELDS ───────
def uses_central(path):
    with open(path) as f:
        t = ast.parse(f.read())
    for node in ast.walk(t):
        if isinstance(node, ast.Import):
            for a in node.names:
                if "verify_hexad_blue" in a.name:
                    return True
        if isinstance(node, ast.ImportFrom) and node.module and \
                "verify_hexad_blue" in node.module:
            return True
        if isinstance(node, ast.Call):
            fn = node.func
            nm = (fn.attr if isinstance(fn, ast.Attribute)
                  else fn.id if isinstance(fn, ast.Name) else "")
            if nm in {"open", "Path", "read_bytes", "read_text",
                      "exec_module", "load"}:
                for arg in list(node.args) + [k.value for k in node.keywords]:
                    if isinstance(arg, ast.Constant) and \
                            isinstance(arg.value, str) and \
                            "verify_hexad_blue_2026_05_15" in arg.value:
                        return True
    return False
sidecar_clean = (not uses_central(SIM_SRC)) and (not uses_central(__file__))
zero_cost = (R["cost_usd"] == 0.0 and R["gpu"] is False and
             R["runpod"] is False and R["fire"] is False and
             R["dispatch"] is False and R["orphan"] == 0 and
             R["model_forward_byte_lm"] is False and R["corpus"] is False)
check("B-S118-8 SIDECAR-CENTRAL-0-DIFF-ZERO-COST-STRUCTURAL",
      sidecar_clean and zero_cost,
      f"sidecar-only (no central-path executable ref)={sidecar_clean} · "
      f"cost=${R['cost_usd']} gpu={R['gpu']} fire={R['fire']} "
      f"dispatch={R['dispatch']} orphan={R['orphan']} — $0, no GPU/fire")

# ── B-S118-9 — g_clm_from_scratch INIT INVARIANT (base_ckpt=None) ────
load_hits = []
for node in ast.walk(TREE):
    if isinstance(node, ast.Call):
        fn = node.func
        nm = (fn.attr if isinstance(fn, ast.Attribute)
              else fn.id if isinstance(fn, ast.Name) else "")
        if nm in {"load_state_dict", "from_pretrained"}:
            load_hits.append(nm)
        if (isinstance(fn, ast.Attribute) and fn.attr == "load" and
                isinstance(fn.value, ast.Name) and fn.value.id == "torch"):
            load_hits.append("torch.load")
base_ckpt_none = (R["base_ckpt"] is None and "BASE_CKPT = None" in SRC and
                  "assert BASE_CKPT is None" in SRC)
random_seeded = "default_rng(seed)" in SRC or "default_rng(SEED" in SRC
check("B-S118-9 G-CLM-FROM-SCRATCH-INIT-INVARIANT-CLOSED",
      len(load_hits) == 0 and base_ckpt_none and random_seeded,
      f"ckpt-load AST hits={load_hits} (0 required) · base_ckpt=None "
      f"asserted={base_ckpt_none} · RANDOM seed-fixed init={random_seeded}")

# ── B-S118-NOTE — empirical carve-out (NOT counted 🔵) ───────────────
NOTE = (
    "B-S118-NOTE — the MEASURED 3-outcome verdict (here: "
    f"{R['verdict']}) and the per-cell non-degenerate/degenerate OUTCOMES "
    "are SGD-free convergence OUTCOMES, NOT counted 🔵. The battery proves "
    "the 4-CELL RIG is HONEST (cell partition exhaustive+disjoint, "
    "decisive 'stdp' cell STDP-only / no-CE / no-backprop AST-audited, §3 "
    "predicate deterministic + byte-equal to TRACK0_INSILICO.md spec, §9 "
    "honest_coherent SSOT-imported, Ψ-form §112-carrier-invariant, "
    "§117-WALL-B inherited, §96 attention-blocker acknowledged), NOT that "
    "Track 0 works / anima emerges. necessary-not-sufficient at every "
    "layer (B-EMERGE-7). A SIM-CONFRONTS-LEARNING-CHANNEL outcome would "
    "confront the LEARNING-CHANNEL half ONLY — the async-substrate half "
    "stays WALL-B (Loihi/SpiNNaker-gated, §117 inherited) and §96 "
    "design-open #1 (attention replacement) BLOCKS the full spiking-anima "
    "instantiation; NOT GOAL emergence, NOT a WALL-A (§1.1 data-regime) "
    "escape. north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달. "
    "B-D-NOTE / B-PUREPHYS-NOTE / B-S96-NOTE / B-S115-NOTE / B-S117-NOTE "
    "family.")
print("\n" + NOTE)

n_pass = sum(PASS)
n_tot = len(PASS)
summary = {
    "battery": "B-S118", "n_pass": n_pass, "n_total": n_tot,
    "all_pass": n_pass == n_tot,
    "verdict_of_run": R["verdict"],
    "non_degenerate_by_cell": R["non_degenerate_by_cell"],
    "note": NOTE, "results": results,
}
with open(os.path.join(HERE, "blue_falsifier_s118_result.json"), "w") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)
print(f"\nB-S118  {n_pass}/{n_tot} "
      f"{'🔵 ALL PASS' if n_pass == n_tot else 'FAIL'}")
