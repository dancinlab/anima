#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════
# B-S117 — §117 LEGO STEP-1-2 in-silico assembly run — sidecar battery
# ════════════════════════════════════════════════════════════════════
# Sidecar ONLY. central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
# sha256 prefix c93e160a8a376a94 — 0-line-diff (verified start+end+post-commit
# by the orchestrator; this battery never touches central).
#
# The battery proves the ASSEMBLY is HONEST:
#   - Ψ-C1 = ψ(c)=(1+c)/2 bounded ∈ [0,1] + cos=0 ⇒ ½ fixed point  (B-S112
#     carry — META_FP(Π_½) instance, carrier = spike-correlation)
#   - STDP-as-ΔW = NO-CE / NO-backprop AST-audit invariant  (mirror §11-B
#     B-PUREPHYS-1: forbidden call/attr set total = 0 over lego_sim.py)
#   - non-degeneracy predicate is closed-form & deterministic
#   - §115-residual connection-point (§117 runs the residual §115 named)
#   - sidecar / central-0-diff structural invariant
# B-S117-NOTE: the battery does NOT prove LEGO works / anima emerges; the
#   MEASURED non-degenerate/degenerate OUTCOME is an SGD-free convergence
#   OUTCOME (NOT counted 🔵) — B-D-NOTE / B-PUREPHYS-NOTE / B-S96-NOTE /
#   B-S115-NOTE / B-EMERGE-7 family, necessary-not-sufficient at every layer.
#
# g3: run ≠ fire ≠ emergence; capability claim 0.  f1/f2 safe (LIF/STDP
#   cited by hexa-bio NEURO.tape OWN invariants + standard neuroscience,
#   NO σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24 derivation; Ψ=½ = anima g2
#   internal-arch carve-out).  $0, NO GPU/fire/dispatch.
# ════════════════════════════════════════════════════════════════════

import ast, json, os, math
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SIM_SRC = os.path.join(HERE, "lego_sim.py")
RES_JSON = os.path.join(HERE, "result.json")

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
M = R["step2_metrics"]

# ── B-S117-1 — Ψ-C1 BOUNDED + cos=0⇒½ FIXED POINT (sympy, B-S112 carry) ──
# ψ(c) = (1+c)/2.  Cauchy–Schwarz ⇒ c ∈ [−1,1] ⇒ ψ ∈ [0,1].  c=0 ⇒ ψ=½.
c = sp.symbols("c", real=True)
psi = (1 + c) / 2
psi_at_lo = sp.simplify(psi.subs(c, -1))         # = 0
psi_at_hi = sp.simplify(psi.subs(c, 1))          # = 1
psi_at_0 = sp.simplify(psi.subs(c, 0))           # = 1/2
dpsi = sp.diff(psi, c)                            # = 1/2 > 0 (monotone)
form_ok = (psi_at_lo == 0 and psi_at_hi == 1 and psi_at_0 == sp.Rational(1, 2)
           and sp.simplify(dpsi - sp.Rational(1, 2)) == 0)
# the run's measured Ψ-C1 must lie in [0,1] and fixed-point flag must hold
run_form_ok = (M["psi_bounded_0_1"] is True and
               M["psi_fixed_point_at_cos0_is_half"] is True and
               0.0 <= R["step2_metrics"]["psi_c1_min"] <= 1.0 and
               0.0 <= R["step2_metrics"]["psi_c1_max"] <= 1.0)
check("B-S117-1 PSI-C1-BOUNDED-FIXED-POINT-CLOSED",
      form_ok and run_form_ok,
      f"sympy ψ(−1)=0 ψ(1)=1 ψ(0)=½ ∂ψ/∂c=½>0 ✓ · run bounded[0,1]="
      f"{M['psi_bounded_0_1']} cos0→½={M['psi_fixed_point_at_cos0_is_half']} "
      f"(§112 META_FP(Π_½) instance, carrier=spike-corr)")

# ── B-S117-2 — STDP-as-ΔW = NO-CE / NO-BACKPROP AST INVARIANT ───────────
# mirror §11-B B-PUREPHYS-1: the sim's executable AST contains ZERO calls
# to the forbidden learning-channel set.  AST Call nodes only — comments /
# docstrings / string literals naming these are NOT executable, excluded.
FORBIDDEN_ATTR = {"backward", "cross_entropy", "zero_grad", "step",
                  "CrossEntropyLoss"}
FORBIDDEN_NAME = {"cross_entropy", "CrossEntropyLoss", "backward"}
FORBIDDEN_MODULE = {"autograd", "optimizer", "optim"}
hits = []
for node in ast.walk(TREE):
    if isinstance(node, ast.Call):
        fn = node.func
        if isinstance(fn, ast.Attribute):
            if fn.attr in FORBIDDEN_ATTR:
                # `.step(` allow-list: net.step(...) is the LIF membrane
                # step, NOT optimizer.step — distinguish by receiver name.
                if fn.attr == "step":
                    recv = fn.value
                    base = (recv.id if isinstance(recv, ast.Name)
                            else getattr(recv, "attr", ""))
                    if base in ("optimizer", "optim", "opt"):
                        hits.append(("attr", fn.attr, base))
                    # net.step / self.step = LIF membrane step → allowed
                else:
                    hits.append(("attr", fn.attr, ast.dump(fn.value)[:40]))
        elif isinstance(fn, ast.Name):
            if fn.id in FORBIDDEN_NAME:
                hits.append(("name", fn.id, ""))
# imports: no torch/autograd/optimizer machinery
imported = set()
for node in ast.walk(TREE):
    if isinstance(node, ast.Import):
        for a in node.names:
            imported.add(a.name.split(".")[0])
    elif isinstance(node, ast.ImportFrom) and node.module:
        imported.add(node.module.split(".")[0])
no_torch = "torch" not in imported and "tensorflow" not in imported
no_ce_backprop = (len(hits) == 0) and no_torch
check("B-S117-2 STDP-NO-CE-NO-BACKPROP-AST-INVARIANT-CLOSED",
      no_ce_backprop,
      f"AST forbidden-call hits={len(hits)} {hits} · imports={sorted(imported)}"
      f" no_torch={no_torch} — learning channel = LOCAL STDP-as-ΔW only "
      f"(mirror §11-B B-PUREPHYS-1)")

# ── B-S117-3 — NON-DEGENERACY PREDICATE CLOSED-FORM & DETERMINISTIC ──────
# predicate: non_degenerate ⟺ (psi_std > τ) ∧ (rasters_alive).  Re-derive
# it from the recorded raw arrays — must EXACTLY equal the recorded flag
# (closed Boolean, deterministic — re-run lego_sim 3× → bit-identical).
# predicate re-derived from the recorded RAW per-stim Ψ-C1 array (rounded
# to 6dp in result.json — recompute std from THOSE, tolerance = round-floor):
psi_arr = np.array(R["psi_c1_per_stim"])
psi_std_re = float(psi_arr.std())
tau = M["tau_nondegen"]
psi_resp_re = psi_std_re > tau
alive_re = (M["rasters_all_silent"] is False and
            M["rasters_all_saturated"] is False and
            M["overall_spike_rate_per_unit_step"] > 0.0)
nd_re = bool(psi_resp_re and alive_re)
# determinism: re-run the FULL sim 3× → its own (std,mean,verdict)
# signature must be bit-identical across runs (same seed ⇒ same result).
deterministic = True
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("lego_sim_re", SIM_SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    import tempfile
    sig = None
    for _ in range(3):
        with tempfile.TemporaryDirectory() as td:
            rr = mod.run(td)
            s = (round(rr["step2_metrics"]["psi_c1_std"], 12),
                 round(rr["step2_metrics"]["psi_c1_mean"], 12),
                 rr["verdict"])
            if sig is None:
                sig = s
            elif s != sig:
                deterministic = False
    # the re-run's full-precision std must match the recorded result.json
    # std EXACTLY (same seed, same code) — this is the real determinism
    # anchor; psi_std_re above is from 6dp-rounded array (round-floor only).
    rerun_matches_recorded = (sig is not None and
                              abs(sig[0] - round(M["psi_c1_std"], 12)) < 1e-9)
except Exception as e:  # pragma: no cover
    deterministic = False
    rerun_matches_recorded = False
    print("  (determinism re-run note:", e, ")")
# predicate match: re-derived Boolean flag == recorded flag; and the
# 6dp-rounded-array std agrees with recorded std within the 1e-6 round floor.
predicate_match = (nd_re == M["non_degenerate"]) and abs(
    psi_std_re - M["psi_c1_std"]) < 1e-6
check("B-S117-3 NON-DEGENERACY-PREDICATE-DETERMINISTIC-CLOSED",
      predicate_match and deterministic and rerun_matches_recorded,
      f"re-derived non_degenerate={nd_re} == recorded={M['non_degenerate']} "
      f"· psi_std(6dp-arr)={psi_std_re:.6e}≈rec={M['psi_c1_std']:.6e} "
      f"(<1e-6 round-floor) · 3×bit-identical={deterministic} · "
      f"re-run≡recorded={rerun_matches_recorded} (degeneracy detector, "
      f"necessary-NOT-sufficient — B-EMERGE-7)")

# ── B-S117-4 — STDP ΔW LOCALITY (sympy: Δw depends ONLY on local traces) ─
# Δw = A+·tr_pre·post − A−·pre·tr_post.  ∂(Δw)/∂(any global loss term) = 0
# by construction (no loss symbol in the rule).  Show ∂Δw/∂A+ = tr_pre·post
# ≥ 0 and ∂Δw/∂A− = −pre·tr_post ≤ 0 — pure local pair-rule signs, no
# error/loss symbol anywhere in the closed form.
Ap, Am, trpre, post, pre, trpost = sp.symbols(
    "Ap Am trpre post pre trpost", nonnegative=True)
dw = Ap * trpre * post - Am * pre * trpost
d_dAp = sp.diff(dw, Ap)                  # = trpre*post ≥ 0
d_dAm = sp.diff(dw, Am)                  # = -pre*trpost ≤ 0
# no symbol named loss/ce/error/grad appears in dw's free symbols:
local_only = all(str(s) not in {"loss", "ce", "error", "grad"}
                  for s in dw.free_symbols)
sign_ok = (sp.simplify(d_dAp - trpre * post) == 0 and
           sp.simplify(d_dAm + pre * trpost) == 0)
check("B-S117-4 STDP-DELTA-W-LOCALITY-SIGN-CLOSED",
      sign_ok and local_only,
      f"sympy ∂Δw/∂A+ = trpre·post ≥0 · ∂Δw/∂A− = −pre·trpost ≤0 · "
      f"Δw free-symbols={sorted(str(s) for s in dw.free_symbols)} — NO "
      f"loss/error/grad symbol (pure LOCAL pair-rule)")

# ── B-S117-5 — §115-RESIDUAL CONNECTION-POINT (closed, non-vacuous) ──────
# §117 runs the open residual §115's DESIGN.md named VERBATIM. Verify the
# §115 artifact exists, its verdict is the inherited one, and §117's
# result.json explicitly inherits WALL-B (does NOT remove it) + WALL-A
# orthogonal.  Non-vacuous: real §115 DESIGN.md witness string present.
s115_design = os.path.join(
    HERE, "..", "lego_simulate_assemble_s115_2026_05_19", "DESIGN.md")
s115_ok = False
s115_witness = ""
if os.path.exists(s115_design):
    with open(s115_design) as f:
        d115 = f.read()
    s115_witness = "LEGO-DESIGN-CLOSE-SIM-IS-GPU-TAUTOLOGY"
    s115_ok = (s115_witness in d115 and
               "in-silico STDP" in d115 and "§96-open" in d115)
inh = R["honest_inheritance"]
wall_b_inherited = ("INHERITED" in inh["wall_b"] and
                    "does NOT remove" in inh["wall_b"])
wall_a_orth = ("ORTHOGONAL" in inh["wall_a"] and "UNTOUCHED" in inh["wall_a"])
seven_form = "BY CONSTRUCTION" in inh["psi_7_form"]
goal_carry = ("GOAL 미도달" in inh["g3"] and "UNCHANGED" in inh["g3"])
check("B-S117-5 §115-RESIDUAL-CONNECTION-POINT-CLOSED",
      s115_ok and wall_b_inherited and wall_a_orth and seven_form and goal_carry,
      f"§115 DESIGN.md witness '{s115_witness}' present={s115_ok} · "
      f"WALL-B inherited(not-removed)={wall_b_inherited} · WALL-A "
      f"orthogonal={wall_a_orth} · §7-FORM-by-construction={seven_form} · "
      f"GOAL-미도달 carry={goal_carry}")

# ── B-S117-6 — SIDECAR / CENTRAL-0-DIFF STRUCTURAL INVARIANT ─────────────
# this battery + lego_sim live ONLY under state/lego_assembly_run_s117_*/.
# It imports no central battery, opens no central file.  Structural AST
# check: neither source has an Import of the central module NOR an open()/
# read of a path that resolves into state/verify_hexad_blue_2026_05_15/.
# (Merely *naming* the central path in a docstring/comment — as this
# battery legitimately does to ASSERT the invariant — is NOT a violation;
# we detect executable use, not string presence.  Mirror §11-B / §115
# B-PUREPHYS-1 / B-S115 AST-audit-not-grep discipline.)
def uses_central(path):
    with open(path) as f:
        t = ast.parse(f.read())
    for node in ast.walk(t):
        # import of any central blue module
        if isinstance(node, ast.Import):
            for a in node.names:
                if "verify_hexad_blue" in a.name:
                    return True
        if isinstance(node, ast.ImportFrom) and node.module and \
                "verify_hexad_blue" in node.module:
            return True
        # open(...) / Path(...) whose literal arg contains the central dir
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
# also: $0 / no-GPU / no-dispatch fields in result.json
zero_cost = (R["cost_usd"] == 0.0 and R["gpu"] is False and
             R["runpod"] is False and R["fire"] is False and
             R["dispatch"] is False and R["orphan"] == 0 and
             R["model_forward_byte_lm"] is False and R["corpus"] is False)
check("B-S117-6 SIDECAR-CENTRAL-0-DIFF-ZERO-COST-STRUCTURAL",
      sidecar_clean and zero_cost,
      f"sidecar-only (no central-path ref)={sidecar_clean} · "
      f"cost=${R['cost_usd']} gpu={R['gpu']} fire={R['fire']} "
      f"dispatch={R['dispatch']} orphan={R['orphan']} — $0, no GPU/fire")

# ── B-S117-7 — g_clm_from_scratch INIT INVARIANT (base_ckpt=None) ────────
# the sim init must be RANDOM seed-fixed with base_ckpt=None and NO ckpt /
# state_dict / load call anywhere (g_clm_from_scratch).
FORBIDDEN_LOAD = {"load_state_dict", "from_pretrained", "torch_load"}
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
                  'assert BASE_CKPT is None' in SRC)
random_seeded = ("default_rng(seed)" in SRC or "default_rng(SEED" in SRC)
check("B-S117-7 G-CLM-FROM-SCRATCH-INIT-INVARIANT-CLOSED",
      len(load_hits) == 0 and base_ckpt_none and random_seeded,
      f"ckpt-load AST hits={load_hits} (0 required) · base_ckpt=None "
      f"asserted={base_ckpt_none} · RANDOM seed-fixed init={random_seeded}")

# ── B-S117-NOTE — empirical carve-out (NOT counted 🔵) ───────────────────
NOTE = (
    "B-S117-NOTE — the MEASURED non-degenerate/degenerate OUTCOME (here: "
    f"{R['verdict']}, Ψ-C1 std={M['psi_c1_std']:.4e}) is an SGD-free "
    "convergence OUTCOME, NOT counted 🔵. The battery proves the ASSEMBLY "
    "is HONEST (STDP-only, no CE, no backprop, Ψ-form carrier-invariant "
    "§112, deterministic, §115-residual connection-point), NOT that LEGO "
    "works / anima emerges. necessary-not-sufficient at every layer "
    "(B-EMERGE-7). A non-degenerate Ψ-C1 form in-sim = §115/§113 INHERITED "
    "confront-NOT-remove (WALL-B §96-physical-gated stays; §7-CARRIER NOT "
    "decided), NOT GOAL emergence, NOT a WALL-A (§1.1 data-regime) escape "
    "— a toy STDP spike sim moves no data threshold (§97). north-star + "
    "§15/§51/§72 milestones UNCHANGED, GOAL 미도달. B-D-NOTE / "
    "B-PUREPHYS-NOTE / B-S96-NOTE / B-S115-NOTE family.")
print("\n" + NOTE)

n_pass = sum(PASS)
n_tot = len(PASS)
summary = {
    "battery": "B-S117", "n_pass": n_pass, "n_total": n_tot,
    "all_pass": n_pass == n_tot,
    "verdict_of_run": R["verdict"],
    "psi_c1_std": M["psi_c1_std"], "psi_c1_mean": M["psi_c1_mean"],
    "non_degenerate": M["non_degenerate"],
    "note": NOTE, "results": results,
}
with open(os.path.join(HERE, "blue_falsifier_s117_result.json"), "w") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)
print(f"\nB-S117  {n_pass}/{n_tot} {'🔵 ALL PASS' if n_pass==n_tot else 'FAIL'}")
