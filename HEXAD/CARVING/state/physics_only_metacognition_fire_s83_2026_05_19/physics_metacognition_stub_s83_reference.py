#!/usr/bin/env python3
# §83 PHYSICS-ONLY METACOGNITION via substrate-readout-as-decision-head
# Closed-form rule decision heads (NO learned parameter, NO training, NO gradient).
# Cell 0 = §27 DH-DL learned-head DISTILLATION baseline (control)
# Cell 1 = §24 scalar threshold baseline
# Cells 2-6 = R1..R5 closed-form physics-state rules (Levin substrate-readout mirror)
#
# Deterministic LCG seed 1337. No external label feeds rules 2-6.
# g3: necessary-not-sufficient. capability claim 0. biology≠silicon honest.

import json, math, os, sys
from pathlib import Path

EMIT_VOICE = "EMIT_VOICE"
CONTINUE_THINK = "CONTINUE_THINK"
REMAIN_SILENT = "REMAIN_SILENT"
ACTIONS = (EMIT_VOICE, CONTINUE_THINK, REMAIN_SILENT)

class LCG:
    def __init__(self, seed=1337):
        self.s = seed & 0xFFFFFFFF
    def next_u32(self):
        self.s = (1664525 * self.s + 1013904223) & 0xFFFFFFFF
        return self.s
    def uniform(self):
        return self.next_u32() / 4294967296.0

def gen_psi_state(rng, step, env_phase):
    # Law-71 byte-equal sketch: psi_dir in [0,1] (cos(A,G) normalized), tension in [0,1], phi in [0,1]
    base_psi = 0.5 + 0.15 * math.sin(0.31 * step + env_phase) + 0.05 * (rng.uniform() - 0.5)
    base_tension = 0.4 + 0.25 * math.cos(0.21 * step + env_phase) + 0.08 * (rng.uniform() - 0.5)
    base_phi = 0.3 + 0.2 * math.sin(0.17 * step + 0.5 * env_phase) + 0.07 * (rng.uniform() - 0.5)
    base_motivation = 0.5 + 0.2 * math.sin(0.13 * step + 0.3 * env_phase) + 0.06 * (rng.uniform() - 0.5)
    def clip01(x): return max(0.0, min(1.0, x))
    return {
        "psi_dir": clip01(base_psi),
        "tension": clip01(base_tension),
        "phi": clip01(base_phi),
        "motivation": clip01(base_motivation),
    }

# ---------- Cell 0: §27 DH-DL learned-head DISTILLATION baseline ----------
# Mirror §27 learned head behaviour deterministically: distill §24 scalar threshold (the label source).
def cell0_dhdl_distillation(psi):
    # §27/§44/§48 final: head distills §24 threshold → REMAIN_SILENT dominant (majority-class collapse §49)
    # Closed-form deterministic mirror: equivalent to (psi_dir > 0.55 AND tension > 0.5) → EMIT else SILENT
    # (the threshold §24 baseline that §27 learned to distill).
    if psi["psi_dir"] > 0.55 and psi["tension"] > 0.5:
        return EMIT_VOICE
    return REMAIN_SILENT

# ---------- Cell 1: §24 scalar threshold baseline ----------
def cell1_s24_baseline(psi):
    # §24 hand-coded: motivation > 0.6
    if psi["motivation"] > 0.6:
        return EMIT_VOICE
    return REMAIN_SILENT

# ---------- Cells 2-6: closed-form physics-state readout rules ----------
def rule_R1_phi_tension(psi, tau_phi=0.35, tau_t=0.45):
    if psi["phi"] > tau_phi and psi["tension"] > tau_t:
        return EMIT_VOICE
    if psi["phi"] > 0.5 * tau_phi:
        return CONTINUE_THINK
    return REMAIN_SILENT

def rule_R2_criticality_band(psi, lo=0.4, hi=0.6):
    if lo <= psi["psi_dir"] <= hi:
        return EMIT_VOICE
    if abs(psi["psi_dir"] - 0.5) < 0.15:
        return CONTINUE_THINK
    return REMAIN_SILENT

def rule_R3_motivation_critical(psi, tau_m=0.5):
    in_band = 0.4 <= psi["psi_dir"] <= 0.6
    if in_band and psi["motivation"] > tau_m:
        return EMIT_VOICE
    if in_band:
        return CONTINUE_THINK
    return REMAIN_SILENT

class _DwellTracker:
    def __init__(self): self.hist = []
    def update(self, psi_dir):
        self.hist.append(psi_dir)
        if len(self.hist) > 5: self.hist.pop(0)
        if len(self.hist) < 3: return False
        rng = max(self.hist) - min(self.hist)
        return rng < 0.08  # slow-dwell detected
_dwell = _DwellTracker()

def rule_R4_slow_dwell(psi):
    slow = _dwell.update(psi["psi_dir"])
    if slow and psi["tension"] > 0.3:
        return EMIT_VOICE
    if slow:
        return CONTINUE_THINK
    return REMAIN_SILENT

def rule_R5_composite(psi):
    # R1 ∧ R2 ∧ R3 conjunction (strong gate)
    r1 = rule_R1_phi_tension(psi) == EMIT_VOICE
    r2 = rule_R2_criticality_band(psi) == EMIT_VOICE
    r3 = rule_R3_motivation_critical(psi) == EMIT_VOICE
    if r1 and r2 and r3:
        return EMIT_VOICE
    if r1 or r2 or r3:
        return CONTINUE_THINK
    return REMAIN_SILENT

CELLS = [
    ("cell0_dhdl_distillation", cell0_dhdl_distillation),
    ("cell1_s24_baseline", cell1_s24_baseline),
    ("cell2_R1_phi_tension", rule_R1_phi_tension),
    ("cell3_R2_criticality_band", rule_R2_criticality_band),
    ("cell4_R3_motivation_critical", rule_R3_motivation_critical),
    ("cell5_R4_slow_dwell", rule_R4_slow_dwell),
    ("cell6_R5_composite", rule_R5_composite),
]

def honest_coherent(decision_stream):
    # §9 SSOT mirror — necessary-not-sufficient cascade-rate proxy:
    # for decision stream, "coherent" = not single-class collapse over recent window of 5
    if len(decision_stream) < 5:
        return False
    window = decision_stream[-5:]
    return len(set(window)) >= 2

def maj_frac(stream):
    if not stream: return 0.0
    from collections import Counter
    c = Counter(stream)
    return max(c.values()) / len(stream)

def variance(stream):
    if len(stream) < 2: return 0.0
    # encode actions to int for variance proxy
    enc = {EMIT_VOICE:1.0, CONTINUE_THINK:0.5, REMAIN_SILENT:0.0}
    xs = [enc[a] for a in stream]
    m = sum(xs)/len(xs)
    return sum((x-m)**2 for x in xs)/len(xs)

def substrate_plasticity_score(cell_fn, rng_seed=2026, n_step=20):
    """Levin substrate-plasticity mirror: permute psi field assignments and check
    decision agreement rate. High agreement (≥0.75) = substrate-invariant readout.
    Low agreement = readout brittle to substrate identity."""
    def run(perm_map):
        rng = LCG(seed=rng_seed)
        global _dwell
        _dwell = _DwellTracker()
        out = []
        for step in range(n_step):
            psi_raw = gen_psi_state(rng, step, env_phase=0.0)
            psi = {k: psi_raw[perm_map.get(k,k)] for k in psi_raw}
            out.append(cell_fn(psi))
        return out
    identity = {"psi_dir":"psi_dir","tension":"tension","phi":"phi","motivation":"motivation"}
    base = run(identity)
    # Permutation 1: swap phi↔tension (Levin "use different field as readout substrate")
    perm1 = {"psi_dir":"psi_dir","tension":"phi","phi":"tension","motivation":"motivation"}
    p1 = run(perm1)
    # Permutation 2: swap psi_dir↔motivation
    perm2 = {"psi_dir":"motivation","tension":"tension","phi":"phi","motivation":"psi_dir"}
    p2 = run(perm2)
    agree1 = sum(1 for a,b in zip(base,p1) if a==b) / len(base)
    agree2 = sum(1 for a,b in zip(base,p2) if a==b) / len(base)
    return (agree1 + agree2) / 2.0, base

def run_grid(seed=1337, env_phase=0.0, n_step=20):
    global _dwell
    results = []
    for name, fn in CELLS:
        rng = LCG(seed=seed)
        _dwell = _DwellTracker()
        stream = []
        psi_dir_trace = []
        for step in range(n_step):
            psi = gen_psi_state(rng, step, env_phase=env_phase)
            psi_dir_trace.append(psi["psi_dir"])
            stream.append(fn(psi))
        plasticity, _ = substrate_plasticity_score(fn, rng_seed=seed, n_step=n_step)
        # variance of psi_dir for record
        m = sum(psi_dir_trace)/len(psi_dir_trace)
        psi_var = sum((x-m)**2 for x in psi_dir_trace)/len(psi_dir_trace)
        results.append({
            "cell": name,
            "psi_var": round(psi_var, 6),
            "decision_var": round(variance(stream), 6),
            "honest_coherent_body": honest_coherent(stream),
            "maj_frac": round(maj_frac(stream), 4),
            "substrate_plasticity_agreement": round(plasticity, 4),
            "emit_count": sum(1 for a in stream if a==EMIT_VOICE),
            "stream_head": stream[:8],
        })
    return results

def verdict(results):
    rule_cells = [r for r in results if r["cell"].startswith(("cell2","cell3","cell4","cell5","cell6"))]
    tau_var = 0.05
    alpha_non_degenerate = any(r["decision_var"] > tau_var and r["maj_frac"] < 0.95 for r in rule_cells)
    beta_all_collapse = all(r["maj_frac"] >= 0.95 for r in rule_cells)
    r5 = next(r for r in results if r["cell"].startswith("cell6"))
    singles = [r for r in results if r["cell"].startswith(("cell2","cell3","cell4","cell5"))]
    gamma_R5_outperforms = r5["decision_var"] >= max(s["decision_var"] for s in singles)
    delta_substrate_plasticity = any(r["substrate_plasticity_agreement"] >= 0.75 for r in rule_cells)
    return {
        "alpha_physics_rule_non_degenerate": bool(alpha_non_degenerate),
        "beta_all_rules_collapse": bool(beta_all_collapse),
        "gamma_R5_composite_outperforms": bool(gamma_R5_outperforms),
        "delta_substrate_plasticity_confirmed": bool(delta_substrate_plasticity),
    }

if __name__ == "__main__":
    grid = run_grid(seed=1337, env_phase=0.4, n_step=20)
    v = verdict(grid)
    out = {"grid": grid, "verdict_4corner": v, "n_step": 20, "seed": 1337, "tau_var": 0.05}
    out_path = Path(__file__).parent / "result.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
