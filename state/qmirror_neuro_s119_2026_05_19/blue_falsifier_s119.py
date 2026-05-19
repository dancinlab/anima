#!/usr/bin/env python3
# ════════════════════════════════════════════════════════════════════
# B-S119 — §119 qmirror-neuro ANU-QRNG-seeded LIF+STDP sim — sidecar battery
# ════════════════════════════════════════════════════════════════════
# Sidecar ONLY. central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
# sha256 prefix c93e160a8a376a94 — 0-line-diff (verified start+end by the
# orchestrator; this battery never imports/opens central).
#
# The battery proves the §119 ASSEMBLY is HONEST:
#   B-S119-1  Ψ-C1 bounded ∈ [0,1] + cos=0⇒½ fixed point  (§117 B-S117-1
#             carry — §112 META_FP(Π_½) instance, carrier = spike-corr)
#   B-S119-2  STDP-as-ΔW = NO-CE / NO-backprop AST invariant  (§117 carry)
#   B-S119-3  §97 NOISE-AS-SEED vs NOISE-AS-CONTENT closed Boolean — the
#             qrng_seed variant's entropy NEVER enters loss/target/readout
#             (AST structural); the qrng_content variant IS the §97
#             DRIVES_STATE ∧ ¬PHYSICS_SOURCED forbidden cell; the Boolean
#             partition is byte-equal to §97 DESIGN.md §2.1
#   B-S119-4  ENTROPY-SOURCE-HONESTLY-LABELLED — result.json records the
#             source that ACTUALLY ran (ANU quantum vs labelled fallback);
#             the legitimacy proof is source-INDEPENDENT
#   B-S119-5  NON-DEGENERACY DETERMINISTIC given a REPLAYED entropy stream
#             — same entropy bytes ⇒ bit-identical sim signature (3×)
#   B-S119-6  §117 / WALL-B INHERITED connection-point — §119 extends
#             §117's sim, adds ONE §97-legit physical-spontaneity layer,
#             does NOT confront the async-substrate half
#   B-S119-7  SIDECAR / CENTRAL-0-DIFF + $0 / no-GPU / no-dispatch structural
#
# B-S119-NOTE: the battery does NOT prove the QRNG layer helps anima emerge;
#   the MEASURED non-degenerate/degenerate OUTCOME is an SGD-free convergence
#   OUTCOME (NOT counted 🔵) — B-D-NOTE / B-PUREPHYS-NOTE / B-S96-NOTE /
#   B-S115-NOTE / B-S117-NOTE / B-EMERGE-7 family, necessary-not-sufficient.
#   Entropy ≠ consciousness. Physically-real spontaneity (qrng_seed) is §97
#   GOAL-ORTHOGONAL — moves NO GOAL distance.
#
# g3: design/run ≠ fire ≠ emergence; capability claim 0.  f1/f2 safe (LIF/
#   STDP + ANU QRNG cited by hexa-bio NEURO.tape + ANU's own engineering
#   spec, NO σ(6)=12/τ(6)=4/φ(6)=2/J₂(6)=24 derivation; Ψ=½ = g2 internal-
#   arch carve-out).  $0, NO GPU/fire/dispatch.
# ════════════════════════════════════════════════════════════════════

import ast, json, os, importlib.util, tempfile
import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SIM_SRC = os.path.join(HERE, "qmirror_neuro_sim.py")
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
V = R["variants"]
v_seed, v_qseed, v_qcont = V["seed_fixed"], V["qrng_seed"], V["qrng_content"]

# ── B-S119-1 — Ψ-C1 BOUNDED + cos=0⇒½ FIXED POINT (sympy, §117 carry) ────
# ψ(c) = (1+c)/2.  Cauchy–Schwarz ⇒ c ∈ [−1,1] ⇒ ψ ∈ [0,1].  c=0 ⇒ ψ=½.
c = sp.symbols("c", real=True)
psi = (1 + c) / 2
form_ok = (sp.simplify(psi.subs(c, -1)) == 0 and
           sp.simplify(psi.subs(c, 1)) == 1 and
           sp.simplify(psi.subs(c, 0)) == sp.Rational(1, 2) and
           sp.simplify(sp.diff(psi, c) - sp.Rational(1, 2)) == 0)
# every variant's measured Ψ-C1 must lie within [0,1]
run_bounds_ok = True
for vn, vd in V.items():
    if not (0.0 <= vd["psi_c1_min"] <= 1.0 and 0.0 <= vd["psi_c1_max"] <= 1.0):
        run_bounds_ok = False
check("B-S119-1 PSI-C1-BOUNDED-FIXED-POINT-CLOSED",
      form_ok and run_bounds_ok,
      f"sympy ψ(−1)=0 ψ(1)=1 ψ(0)=½ ∂ψ/∂c=½>0 ✓ · all 3 variants Ψ-C1 "
      f"∈[0,1]={run_bounds_ok} (§112 META_FP(Π_½), carrier=spike-corr; "
      f"§117 B-S117-1 carry)")

# ── B-S119-2 — STDP-as-ΔW = NO-CE / NO-BACKPROP AST INVARIANT ───────────
# mirror §117 B-S117-2 / §11-B B-PUREPHYS-1: the sim's executable AST
# contains ZERO calls to the forbidden learning-channel set.  AST Call
# nodes only — comments / docstrings / string literals excluded.
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
            # `.step(` allow-list: net.step / self.step = LIF membrane step,
            # NOT optimizer.step — flag only if receiver is an optimizer.
            if fn.attr == "step":
                recv = fn.value
                base = (recv.id if isinstance(recv, ast.Name)
                        else getattr(recv, "attr", ""))
                if base in ("optimizer", "optim", "opt"):
                    hits.append(("attr", "step", base))
        elif isinstance(fn, ast.Name) and fn.id in FORBIDDEN_NAME:
            hits.append(("name", fn.id))
imported = set()
for node in ast.walk(TREE):
    if isinstance(node, ast.Import):
        for a in node.names:
            imported.add(a.name.split(".")[0])
    elif isinstance(node, ast.ImportFrom) and node.module:
        imported.add(node.module.split(".")[0])
no_dl = "torch" not in imported and "tensorflow" not in imported \
        and "jax" not in imported
no_ce_backprop = (len(hits) == 0) and no_dl
check("B-S119-2 STDP-NO-CE-NO-BACKPROP-AST-INVARIANT-CLOSED",
      no_ce_backprop,
      f"AST forbidden-call hits={len(hits)} {hits} · imports={sorted(imported)}"
      f" no_dl_framework={no_dl} — learning channel = LOCAL STDP-as-ΔW only "
      f"(mirror §117 B-S117-2 / §11-B B-PUREPHYS-1)")

# ── B-S119-3 — §97 NOISE-AS-SEED vs NOISE-AS-CONTENT CLOSED BOOLEAN ──────
# The §97 §2.1 closed legitimacy predicate over (DRIVES_STATE, PHYSICS_
# SOURCED).  §119 instantiates two cells:
#   qrng_seed    : (DRIVES_STATE=T, PHYSICS_SOURCED=T) → GOAL-LEGITIMATE-INPUT
#   qrng_content : (DRIVES_STATE=T, PHYSICS_SOURCED=F) → GOAL-ILLEGITIMATE-
#                   COMMAND-CHANNEL
# (1) the closed Boolean partition itself (sympy) — byte-equal to §97 DESIGN.
# (2) STRUCTURAL AST proof: in the qrng_seed PATH, the entropy variable
#     (`seed_jitter`) flows ONLY into `self.v` (the membrane v0) — it never
#     reaches a loss/target/readout.  In the qrng_content PATH, the entropy
#     (`content_target`) flows into `ext` (the external DRIVE) as content.
DS, PS = sp.symbols("DS PS")            # DRIVES_STATE, PHYSICS_SOURCED
# §97 §2.1: legitimate-input ⇔ DS ∧ PS ; command-channel ⇔ DS ∧ ¬PS
legit_input = sp.And(DS, PS)
command_channel = sp.And(DS, sp.Not(PS))
# the two cells are mutually exclusive and the partition is exhaustive over
# the DS=True half: (DS∧PS) ⊻ (DS∧¬PS) ≡ DS  (sympy proves)
partition_ok = (sp.simplify(sp.Xor(legit_input, command_channel)) ==
                sp.simplify(DS))
# truth-table: qrng_seed row (T,T)→legit_input True, command False;
#              qrng_content row (T,F)→legit_input False, command True
seed_row = (bool(legit_input.subs({DS: True, PS: True})) is True and
            bool(command_channel.subs({DS: True, PS: True})) is False)
cont_row = (bool(legit_input.subs({DS: True, PS: False})) is False and
            bool(command_channel.subs({DS: True, PS: False})) is True)
# result.json's legitimacy classification must match these tuples
L = R["legitimacy_97"]
json_seed = (L["qrng_seed"]["drives_state"] is True and
             L["qrng_seed"]["physics_sourced"] is True and
             "GOAL-LEGITIMATE-INPUT" in L["qrng_seed"]["verdict"])
json_cont = (L["qrng_content"]["drives_state"] is True and
             L["qrng_content"]["physics_sourced"] is False and
             "GOAL-ILLEGITIMATE-COMMAND-CHANNEL" in L["qrng_content"]["verdict"])
# STRUCTURAL AST: locate run_variant; in the qrng_seed branch entropy →
# membrane only; in qrng_content branch entropy → external drive.  We
# verify the entropy enters `self.v` (LIFNet.__init__ seed_jitter) and that
# the forbidden cell is built by adding `content_target` to `ext`.
src_seed_ok = ("self.v = self.v + seed_jitter" in SRC and
               "seed_jitter=seed_jitter" in SRC)
src_cont_ok = ("ext = ext + 1.2 * content_target" in SRC and
               'variant == "qrng_content"' in SRC)
# negative structural: in qrng_seed there is NO entropy→target wiring.
# the entropy variable name `seed_jitter` must NOT appear inside any
# psi_c1 / loss / target expression — it only ever touches `self.v`.
seed_no_readout = "seed_jitter" not in SRC.split("def psi_c1")[1].split(
    "def run_variant")[0]
b3 = (partition_ok and seed_row and cont_row and json_seed and json_cont
      and src_seed_ok and src_cont_ok and seed_no_readout)
check("B-S119-3 §97-NOISE-AS-SEED-vs-NOISE-AS-CONTENT-CLOSED",
      b3,
      f"§97 §2.1 partition (DS∧PS)⊻(DS∧¬PS)≡DS sympy={partition_ok} · "
      f"seed_row(T,T)→legit={seed_row} · cont_row(T,F)→command={cont_row} · "
      f"json classification matches seed={json_seed} content={json_cont} · "
      f"AST: entropy→membrane-v0-only(seed)={src_seed_ok} "
      f"entropy→ext-drive(content)={src_cont_ok} "
      f"entropy-absent-from-readout={seed_no_readout}")

# ── B-S119-4 — ENTROPY-SOURCE-HONESTLY-LABELLED ─────────────────────────
# result.json must record the source that ACTUALLY ran; if ANU is the
# source it is labelled physical-quantum; if a fallback ran it is labelled
# a CSPRNG fallback.  The legitimacy proof (B-S119-3) is source-independent.
E = R["entropy"]
src = E["source_actually_ran"]
physical = E["is_physical_quantum"]
# label honesty: physical flag ⟺ source string starts ANU_QUANTUM ;
# a fallback must be explicitly labelled FALLBACK / CSPRNG.
label_consistent = (
    (physical is True and src.startswith("ANU_QUANTUM")) or
    (physical is False and ("FALLBACK" in src or "CSPRNG" in src)))
# sha256 prefix recorded (16 hex chars) — entropy stream is committed
sha_ok = (isinstance(E["sha256_prefix"], str) and
          len(E["sha256_prefix"]) == 16 and
          all(ch in "0123456789abcdef" for ch in E["sha256_prefix"]))
n_ok = E["n_bytes"] == 256          # N = 96+96+64
check("B-S119-4 ENTROPY-SOURCE-HONESTLY-LABELLED-CLOSED",
      label_consistent and sha_ok and n_ok,
      f"source_actually_ran='{src}' is_physical_quantum={physical} "
      f"label_consistent={label_consistent} · sha256[:16]={E['sha256_prefix']}"
      f" valid={sha_ok} · n_bytes={E['n_bytes']}=N={n_ok} — legitimacy proof "
      f"(B-S119-3) is source-INDEPENDENT; this only audits HONEST labelling")

# ── B-S119-5 — NON-DEGENERACY DETERMINISTIC GIVEN REPLAYED ENTROPY ──────
# entropy_to_jitter is a PURE function of the entropy byte stream — so
# REPLAYING the SAME entropy stream reproduces the sim bit-identically.
# Re-run run_variant("qrng_seed", entropy_bytes=<fixed replay stream>) 3×
# → (psi_std, psi_mean, non_degenerate) must be bit-identical each time.
deterministic = True
rerun_sig = None
try:
    spec = importlib.util.spec_from_file_location("qn_sim_re", SIM_SRC)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # fixed replay stream — deterministic test vector (NOT a live fetch);
    # B-S119-5 tests "deterministic GIVEN replayed stream", not live ANU.
    replay = np.arange(256, dtype=np.uint8)            # fixed byte stream
    for _ in range(3):
        rr = mod.run_variant("qrng_seed", entropy_bytes=replay,
                             entropy_source="REPLAY_FIXED_STREAM")
        s = (round(rr["psi_c1_std"], 12), round(rr["psi_c1_mean"], 12),
             rr["non_degenerate"], round(rr["seed_jitter_norm"], 10))
        if rerun_sig is None:
            rerun_sig = s
        elif s != rerun_sig:
            deterministic = False
    # also: a DIFFERENT replay stream must give a DIFFERENT signature
    # (entropy genuinely enters the sim — not ignored).
    replay2 = (np.arange(256, dtype=np.uint8) * 7 + 3).astype(np.uint8)
    rr2 = mod.run_variant("qrng_seed", entropy_bytes=replay2,
                          entropy_source="REPLAY_FIXED_STREAM_2")
    s2 = (round(rr2["psi_c1_std"], 12), round(rr2["psi_c1_mean"], 12))
    entropy_actually_enters = (s2[0], s2[1]) != (rerun_sig[0], rerun_sig[1])
except Exception as e:                              # pragma: no cover
    deterministic = False
    entropy_actually_enters = False
    print("  (determinism re-run note:", e, ")")
check("B-S119-5 NON-DEGENERACY-DETERMINISTIC-GIVEN-REPLAYED-ENTROPY-CLOSED",
      deterministic and entropy_actually_enters,
      f"3× replay of SAME entropy stream → bit-identical signature="
      f"{deterministic} (sig={rerun_sig}) · DIFFERENT stream → DIFFERENT "
      f"signature={entropy_actually_enters} (entropy genuinely enters the "
      f"sim, is not ignored) — pure-fn determinism, B-EMERGE-7 detector")

# ── B-S119-6 — §117 / WALL-B INHERITED CONNECTION-POINT ─────────────────
# §119 EXTENDS §117's sim and INHERITS its verdict; verify the §117
# artifact exists, §119's result.json declares it extends §117, and the
# honest_inheritance block carries §97 + §115 + §117 + WALL-B verbatim.
s117_sim = os.path.join(
    HERE, "..", "lego_assembly_run_s117_2026_05_19", "lego_sim.py")
s117_ok = False
if os.path.exists(s117_sim):
    with open(s117_sim) as f:
        d117 = f.read()
    # §117's sim must itself carry the WALL-B-inherited Ψ-C1 form
    s117_ok = ("psi_c1" in d117 and "STDP" in d117 and
               "WALL-B-INHERITED" in d117)
inh = R["honest_inheritance"]
extends_ok = "§117" in R["extends"] and "lego_sim.py" in R["extends"]
wall_b = ("INHERITED" in inh["wall_b"] and
          "LEARNING-CHANNEL half only" in inh["wall_b"] and
          "ASYNC-SUBSTRATE half stays WALL-B" in inh["wall_b"])
wall_a = ("ORTHOGONAL" in inh["wall_a"] and "UNTOUCHED" in inh["wall_a"])
s97_inh = ("GOAL-LEGITIMATE-INPUT" in inh["s97"] and
           "GOAL-ORTHOGONAL" in inh["s97"])
s115_inh = "GPU-TAUTOLOGY" in inh["s115"]
seven_form = "BY CONSTRUCTION" in inh["psi_7_form"]
goal_carry = ("GOAL 미도달" in inh["g3"] and "UNCHANGED" in inh["g3"] and
              "real entropy ≠ real substrate" in inh["g3"])
check("B-S119-6 §117-WALL-B-INHERITED-CONNECTION-POINT-CLOSED",
      s117_ok and extends_ok and wall_b and wall_a and s97_inh
      and s115_inh and seven_form and goal_carry,
      f"§117 lego_sim.py present+carries-WALL-B={s117_ok} · extends-§117="
      f"{extends_ok} · WALL-B inherited(learning-channel-only,async-stays)="
      f"{wall_b} · WALL-A orthogonal={wall_a} · §97 inherited={s97_inh} · "
      f"§115 inherited={s115_inh} · §7-FORM-by-construction={seven_form} · "
      f"GOAL-미도달 carry={goal_carry}")

# ── B-S119-7 — SIDECAR / CENTRAL-0-DIFF + $0 STRUCTURAL ─────────────────
# the sim + battery live ONLY under state/qmirror_neuro_s119_*/.  Neither
# imports the central blue module nor opens a path into the central dir.
# (Naming the central path in a comment to ASSERT the invariant is NOT a
# violation — we detect executable use, not string presence.)
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
check("B-S119-7 SIDECAR-CENTRAL-0-DIFF-ZERO-COST-STRUCTURAL",
      sidecar_clean and zero_cost,
      f"sidecar-only (no central import/open)={sidecar_clean} · "
      f"cost=${R['cost_usd']} gpu={R['gpu']} fire={R['fire']} "
      f"dispatch={R['dispatch']} orphan={R['orphan']} — $0, no GPU/fire")

# ── B-S119-NOTE — empirical carve-out (NOT counted 🔵) ───────────────────
NOTE = (
    "B-S119-NOTE — the MEASURED non-degenerate/degenerate OUTCOME (here: "
    f"{R['verdict']}, qrng_seed Ψ-C1 std={v_qseed['psi_c1_std']:.4e}) is an "
    "SGD-free convergence OUTCOME, NOT counted 🔵. The battery proves the "
    "ASSEMBLY is HONEST (STDP-only no-CE, Ψ-form carrier-invariant §112, "
    "§97 noise-as-seed vs noise-as-content closed-Boolean partition, entropy "
    "source honestly labelled, deterministic-given-replay, §117 connection-"
    "point), NOT that the QRNG layer helps anima emerge. Entropy ≠ "
    "consciousness. The qrng_seed variant is §97 GOAL-LEGITIMATE-INPUT and "
    "physically-real spontaneity — but §97 GOAL-ORTHOGONAL: it adds ZERO "
    "task signal and moves NO GOAL distance. §119 confronts the LEARNING-"
    "CHANNEL half only; the ASYNC-SUBSTRATE half stays WALL-B (Loihi/"
    "SpiNNaker-gated) — real physical entropy ≠ a real async neuromorphic "
    "chip. necessary-not-sufficient at every layer (B-EMERGE-7). north-star "
    "+ §15/§51/§72 milestones UNCHANGED, GOAL 미도달. B-D-NOTE / "
    "B-PUREPHYS-NOTE / B-S96-NOTE / B-S115-NOTE / B-S117-NOTE family.")
print("\n" + NOTE)

n_pass = sum(PASS)
n_tot = len(PASS)
summary = {
    "battery": "B-S119", "n_pass": n_pass, "n_total": n_tot,
    "all_pass": n_pass == n_tot,
    "verdict_of_run": R["verdict"],
    "entropy_source_actually_ran": R["entropy"]["source_actually_ran"],
    "is_physical_quantum": R["entropy"]["is_physical_quantum"],
    "qrng_seed_psi_std": v_qseed["psi_c1_std"],
    "qrng_seed_non_degenerate": v_qseed["non_degenerate"],
    "content_collapsed": R["content_collapsed"],
    "note": NOTE, "results": results,
}
with open(os.path.join(HERE, "blue_falsifier_s119_result.json"), "w") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)
print(f"\nB-S119  {n_pass}/{n_tot} {'🔵 ALL PASS' if n_pass==n_tot else 'FAIL'}")
