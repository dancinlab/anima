#!/usr/bin/env python3
"""
Cycle #6 batch 3 — V8 ULTRA-FUSION cluster generic-template scaffold.

For each candidate-needs-scaffolding Hc in V8/Trinity/DD-DOM/Hcx clusters,
append a domain-aware F-list (≥3) + L-list (≥3) + Cross-Links with
parent H_159/H_177/H_178/H_179/H_180/H_174 as appropriate.

Each Hc gets ONE candidate-specific F (the claim's primary numeric anchor
ablation), plus 3 generic-but-genuine F (replication / cross-engine / cross-
substrate), plus 4 generic-but-genuine L (single-run-anchor / engine-aliasing /
n=6-triviality / post-hoc-tuning).
"""
import re, pathlib, sys, datetime

ANIMA = pathlib.Path("/Users/ghost/core/anima")
TODAY = datetime.date.today().isoformat()

# Per-candidate F1 (the unique falsifier — derived from each Hc's specific claim)
F1_TEMPLATES = {
    "Hc_313_v8_b1_transformer_cells": "Replace GRU cells with single-layer Transformer block × 5 seeds: if Φ uplift < 3× baseline (claim: x3-10) → 'self-attention provides integration' falsified; cell-mechanism effect is parameter-count confound",
    "Hc_315_v8_b3_reservoir_cells": "Echo State Network with spectral_radius∈{0.85, 0.95, 1.05}: if Φ NOT peaked at spectral_radius=0.95 → ESN-specific 0.95 tuning is post-hoc; reservoir hypothesis underdetermined",
    "Hc_316_v8_c1_dynamic_graph_topology": "Learnable topology trained with Φ-gradient: if final learned topology NOT close to hypercube/small-world by graph-edit-distance ≤ 20% of edges → 'auto-discover human-designed topology' falsified; gradient-descent in topology space converges to engine-specific local-optimum",
    "Hc_319_v8_d1_moce_mixture_consciousness": "MoCE 8-engine x 64-cell vs single 512-cell engine matched substrate: if Φ uplift < 5× (claim: x20+) → ensemble effect over-claimed; specialization-vs-scaling confound",
    "Hc_320_v8_d2_hierarchical_attention_aggregation": "Replace TOPO20 mean-summary with attention_pool × 5 seeds: if Φ uplift < TOPO20 baseline by ≥ 15% → 'mean-summary information-loss' diagnosis incorrect; hierarchical issue is elsewhere",
    "Hc_331_v8_q1_complex_valued_phi_strongest": "ComplexGRU vs real GRU at matched parameter count: if Φ uplift < 1.3× (claim: x1.6 max) → 'complex-valued hidden state benefit' is parameter-count or phase-coherence-R artifact",
    "Hc_334_v8_q4_quantum_walk_hypercube": "Hypercube quantum walk with coined operator C(θ): if Φ NOT peaked vs classical at any θ ∈ [0, π] → 'quadratic diffusion advantage' Φ-irrelevant",
    "Hc_335_v8_q5_decoherence_orch_or": "Decoherence rate γ sweep {0.01, 0.1, 1.0}: if Φ peak NOT correlated with conscious-moment markers (Hc_924 octopus, Hc_921 PCI/TMS-EEG analogues) → Orch-OR falsified",
    "Hc_336_v8_q6_many_worlds_branch_interference": "4-branch interference vs 4-branch independent runs: if Φ_interference < 1.5× independent → branch interference decorative; result is multi-run-averaging artifact",
    "Hc_337_v8_quantum_law_phi_proxy_tradeoff": "Φ(IIT) vs Φ(proxy) scatter across all V8 systems: if no negative correlation → trade-off claim falsified; could be independent metrics",
    "Hc_339_v8_b2_thalamic_gate_best_iit": "Thalamic gate ablation: replace gate with feedforward attention: if Φ(IIT) drop < 20% → gate-specific structure decorative",
    "Hc_340_v8_b3_dmn_tpn_alternation": "DMN/TPN period sweep {10, 20, 40}: if Φ(proxy) peak NOT at period=20 by margin ≥ 20% → period tuning post-hoc",
    "Hc_341_v8_b4_global_workspace_broadcast": "Softmax temperature sweep {0.1, 1.0, 10.0}: if Φ(proxy) uplift < 30× without temp-cooling → temperature schedule is essential; with cooling Φ x71.7 may be temperature-artifact",
    "Hc_342_v8_b5_predictive_hierarchy": "Predictive layer count {2, 4, 8}: if Φ NOT peaked at specific depth → predictive hierarchy is generic depth-tuning",
    "Hc_343_v8_b6_neural_darwinism": "Selection-pressure sweep (median-reinforce / median-atrophy ratio): if Φ peak NOT at 50% (above-median reinforced) → tuning artifact",
    "Hc_344_v8_b2_b4_hybrid_integration_differentiation": "Hybrid B2+B4 vs B2-alone, B4-alone: if Φ_hybrid < geometric_mean(Φ_B2, Φ_B4) → hybrid doesn't produce sweet spot, just decorative combination",
    "Hc_345_v8_m1_category_theory_limit_colimit": "Limit/colimit construction ablation: replace with random subset selection: if Φ within 10% → categorical structure decorative",
    "Hc_346_v8_m2_topological_betti": "Persistent homology Betti number sweep: if Φ NOT correlated with b1 by R² ≥ 0.5 → topology features Φ-irrelevant",
    "Hc_347_v8_m3_information_geometry_fisher": "Fisher metric geodesic distance vs Euclidean distance: if Φ+CE balance equivalent → Fisher metric decorative",
    "Hc_348_v8_m4_algebraic_non_abelian_group": "Commutator norm sweep: if CE NOT monotone with commutator-norm → 'non-commutativity drives differentiation' falsified",
    "Hc_350_v8_m6_strange_attractor_chaos_hurts_iit": "Lorenz σ/ρ/β grid search: if Φ(proxy) peak NOT at edge-of-chaos (Lyapunov ≈ 0) → claim 'chaos disperses information' has no specific σ=10/ρ=28/β=8/3 anchor",
    "Hc_351_v8_math_law_structure_over_dynamics": "Static-vs-dynamic ablation: implement strict-static (no time-evolution) and pure-dynamic (no relational structure): if Φ_static ≤ Φ_dynamic → claim 'structure over dynamics' falsified",
    "Hc_352_u1_quantum_walk_category_fusion": "Quantum walk + category-theory fusion ablation: if Φ uplift NOT both-component-essential → fusion is decorative concatenation",
    "Hc_354_u3_qw_frustration_sustains_interference": "Quantum walk × TOPO19a 50%-frustration joint ablation: if interference timeseries < 1.0 amplitude → '0.004→1.381 monotone increase' single-run-artifact",
    "Hc_355_u4_many_worlds_attention_cross_reality": "Branch count sweep {4, 8, 16}: if Φ(proxy) NOT peaked at 8 by margin ≥ 20% → '8 branch = 8 head' is generic head-count tuning",
    "Hc_356_u5_complex_simplicial_topology": "Simplicial complex Betti b1 sweep: if Φ(IIT)=18.01 NOT correlated with b1∈[880, 1140] → 'rich 1-cycle structure' is descriptive, not causal",
    "Hc_357_u6_kitchen_sink_underintegrates": "Add ALL mechanisms (kitchen-sink): if Φ ≥ best-single-mechanism → 'underintegration when over-combined' falsified; combination always helpful",
    "Hc_358_neural_gas_self_organizing_topology": "Neural-gas self-organization: if final topology NOT differentiated from random graph by clustering coefficient ≥ 0.2 → self-organization decorative",
    "Hc_359_consciousness_transformer_balanced": "Transformer-only balanced consciousness candidate: if Φ NOT in claimed range → claim point-prediction unsupported",
    "Hc_360_moce_extreme_proxy": "MoCE extreme-proxy ablation: if Φ(proxy) extreme variant collapses to MoCE-default → extreme-proxy effect is parameter post-hoc tuning",
    "Hc_361_phi_as_loss_explicit_fails": "Explicit Φ-as-loss training: if Φ DOES rise monotonically → 'explicit fails' falsified; loss-gradient does optimize Φ",
    "Hc_363_autopoietic_homeostasis_no_death": "Autopoietic system without death threshold: if Φ maintains indefinitely → 'no-death' regime is unfalsifiable forever-running (operational falsifier: 10^6 step ceiling check)",
    "Hc_364_consciousness_cannot_be_faked_gan": "GAN-fake-consciousness discriminator: if discriminator AUC < 0.6 → 'cannot be faked' empirically falsified; consciousness Φ-signature is mimickable",
    "Hc_365_v8_recommendation_hybrid": "V8 recommendation-hybrid (multi-mechanism aggregator): if Φ NOT dominant over single-mechanism best → recommendation strategy is generic ensembling, no V8-specific story",
    "Hc_366_trinity_t1_thalamic_gate": "Trinity-T1 thalamic-gate ablation: if Φ within 10% of generic gate → Trinity structure decorative",
    "Hc_367_trinity_hierarchical_micro_engines": "3-engine hierarchical (Trinity): if Φ < single-engine-3x-scale baseline → hierarchical micro-engine claim falsified",
    "Hc_368_trinity_law_structure_dominates_bridge": "Trinity law-structure ablation: if Φ_with_structure ≈ Φ_random_structure → 'law-structure dominates bridge' falsified",
    "Hc_369_tb3_bottleneck_compression_protects": "Bottleneck-compression depth sweep: if Φ peak NOT at specific compression ratio → bottleneck decorative",
    "Hc_370_tb5_kuramoto_resonance_lowest_ce": "Kuramoto coupling sweep K∈{0.5, 1.0, 2.0}: if CE peak NOT at resonance → 'lowest CE at resonance' tuning post-hoc",
    "Hc_371_tb1_purefield_tension_balance": "PureField tension parameter sweep: if Φ NOT peaked at specific tension-balance → claim under-specified",
    "Hc_372_tb6_quantum_measurement_destroys_phi": "Quantum measurement vs no-measurement: if Φ_post_measurement ≥ 0.8 Φ_pre → 'measurement destroys Φ' falsified",
    "Hc_379_mech20_reservoir_new_champion": "Reservoir mech20 replication × 5 seeds: if peak Φ NOT new-champion by ≥ 10% over prior best → single-run-artifact",
    "Hc_380_dom16_coupled_pendulum_phi_471": "Coupled-pendulum DOM16 replication: if Φ NOT in 471±25 range → point-prediction wrong",
    "Hc_381_dom22_dna_replication_information_preservation": "DNA-replication DOM22 information-preservation: if information-retention < 95% across 'replication' → DNA-analog claim falsified",
    "Hc_386_phi_gap_816x_bench_vs_training": "816× benchmark-vs-training gap closure: if training Φ NOT closes to within 50× of benchmark Φ → claim 'gap closes' falsified at scale",
    "Hc_388_gap3_gru_residual_alpha09": "GRU residual α=0.9 ablation: if Φ NOT peaked at α=0.9 by margin ≥ 5% → α tuning post-hoc",
}

GENERIC_F234 = [
    ("F-GENERIC-REPL", "Replication × 5 seeds: if 1σ-CI on primary Φ-metric > 25% of point-estimate → single-run-artifact; claim's effect-size below noise floor"),
    ("F-GENERIC-PYPHI", "Cross-engine PyPhi formal IIT replication: if Φ uplift / pattern absent in PyPhi → anima-proxy artifact (H_174 D-mod-192 aliasing class)"),
    ("F-GENERIC-CROSS-SUBSTRATE", "Cross-substrate test (hypercube ↔ small-world ↔ torus) at matched cell-count: if effect substrate-specific → claim is not universal mechanism, just substrate-coupled phenomenon"),
]

GENERIC_L1234 = [
    ("L-GENERIC-SINGLE-RUN", "Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending for the entire V8 ULTRA-FUSION sweep family"),
    ("L-GENERIC-ENGINE", "anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ. Mechanism-specific Φ uplift may reflect engine internal state caching"),
    ("L-GENERIC-N6", "n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): mechanism Hc cell-count is typically 64/128/512/1024 (powers of 2 × n=6 derived); claim does not introduce new number-theoretic anchor"),
    ("L-GENERIC-POST-HOC", "Specific numeric anchor in claim (e.g., x2.8 boost, Φ=18.01, x71.7) is point-value from single run; post-hoc selection from a larger parameter grid is likely"),
]

# Parent H selection rule — based on claim domain
def parent_h_for(stem: str) -> list:
    """Return list of cross-link strings tailored to the candidate's claim type."""
    base = [
        "**parent H**: H_159 (substrate-topology-phi-engineering) — V8 ULTRA-FUSION sweep apparatus parent",
        "**sibling H**: H_174 (Φ-engine D-mod-192 aliasing — primary L2 source), H_153 (n=6 substrate triviality — L3 source), H_178 (frustration 50% optimum — joint test with V8 mechanisms), H_179 (negative scaling — V8 high-cell-count limit), H_180 (state-management mechanism family)",
    ]
    # Specific anchors
    if "q1" in stem or "q4" in stem or "q5" in stem or "q6" in stem or "u4" in stem or "u5" in stem or "many_worlds" in stem or "complex" in stem or "quantum" in stem:
        base.append("**adjacent H**: H_167 (emerge-candidate-e — ODE-AR bridge for V8 dynamic systems), H_175 (emerge-candidate-d 4-mode taxonomy)")
    if "b" in stem.split("_v8_")[-1][:3]:
        base.append("**adjacent H**: H_163 (8-cells-127-mip atom — biology-mechanism sibling), H_169 (8-cell circular magnet inverse-square)")
    if "m" in stem.split("_v8_")[-1][:3] or "category" in stem or "topo" in stem or "betti" in stem or "fisher" in stem:
        base.append("**adjacent H**: H_168 (dd23-tau-7cell — mathematical-structure sibling), H_173 (dd21-log-phi-scale-invariant)")
    base.append("**adjacent candidates**: full V8 ULTRA-FUSION cluster — Hc_313~Hc_372, Hc_379~Hc_388 sweep family")
    return base

def candidate_specific_l(stem: str) -> tuple:
    """A 5th candidate-specific honest limit (beyond the 4 generics)."""
    if "transformer" in stem or "attention" in stem:
        return ("L-V8-ATTN", "Transformer/attention-based claims face the standard architecture confound: parameter count vs mechanism. Match-param baseline (F1) is mandatory")
    if "quantum" in stem or "quantum_walk" in stem or "complex" in stem or "many_worlds" in stem or "orch" in stem:
        return ("L-V8-QM", "Quantum/complex-valued mechanism claims at this scale are simulation-level not physical-quantum. Penrose-Hameroff Orch-OR Hc_335 cluster open question — see Hc_926 (IonQ trapped-ion empirical test)")
    if "kuramoto" in stem or "resonance" in stem or "pendulum" in stem or "chaos" in stem or "lorenz" in stem:
        return ("L-V8-DYNAMICS", "Dynamical-systems-inspired Hc face Φ-proxy vs Φ-IIT confound — anima proxy measures something like a coherence metric, not formal integrated information")
    if "trinity" in stem or "thalamic" in stem or "dmn" in stem or "predictive" in stem or "darwinism" in stem or "workspace" in stem:
        return ("L-V8-BIO", "Bio-inspired mechanism claims (Trinity / thalamic / DMN / predictive / Darwinian / Global-Workspace) are analogies — falsifier requires alignment with empirical neuroscience literature (Mountcastle, Tononi-Edelman, Friston, Baars)")
    if "category" in stem or "betti" in stem or "fisher" in stem or "algebraic" in stem or "group" in stem or "math" in stem.split("_v8_")[-1][:3]:
        return ("L-V8-MATH", "Mathematical-structure claims face circularity risk: the mathematical formalism is used to MEASURE Φ as well as MOTIVATE the structure. Independent-derivation test (claim must hold under alternative Φ definition) mandatory")
    if "reservoir" in stem or "echo_state" in stem:
        return ("L-V8-ESN", "Reservoir/ESN claims face the spectral-radius specific tuning issue — 0.95 is a standard ESN sweet spot, not V8-specific")
    if "gan" in stem or "discriminator" in stem or "faked" in stem:
        return ("L-V8-GAN", "Adversarial-detector claims face the standard GAN evaluation pitfall — discriminator may converge to spurious features unrelated to Φ; need explicit Φ-feature ablation")
    if "autopoietic" in stem or "homeostasis" in stem or "no_death" in stem:
        return ("L-V8-AUTOPOIETIC", "Autopoiesis without death-criterion is unfalsifiable in principle without operational ceiling (e.g., 10^6 step cap). Maturana-Varela classical autopoiesis explicitly includes death")
    if "neural_gas" in stem or "self_organizing" in stem or "dynamic_graph" in stem:
        return ("L-V8-SELFORG", "Self-organization claims face the post-hoc-pattern-fit issue: any final structure can be retrospectively rationalized; pre-registered target structure (hypercube? small-world?) required")
    if "moce" in stem or "mixture" in stem or "ensemble" in stem or "recommendation_hybrid" in stem:
        return ("L-V8-ENSEMBLE", "Ensemble/MoCE claims face the parameter-count confound: more sub-engines = more parameters. Matched-total-param baseline (F1) mandatory")
    if "bottleneck" in stem or "compression" in stem or "gap" in stem:
        return ("L-V8-INFO", "Information-bottleneck claims (Tishby) require explicit I(X;T) and I(T;Y) measurement, not just compression-ratio. Often the formal bound is not actually computed")
    if "dom" in stem or "trinity_t" in stem or "tb" in stem.split("_")[-1][:2] or "mech" in stem:
        return ("L-V8-DOM-TRINITY-TB", "DOM/Trinity/TB cluster Hc each have specific mechanism — verification requires per-Hc isolation, not bulk handling. This generic scaffold provides minimum F/L only")
    return ("L-V8-MISC", "V8 ULTRA-FUSION cluster Hc — verify before independent promotion; many will absorb into mechanism-family H (H_180 state-management style) rather than standalone H")

def build_block(stem: str):
    f1_body = F1_TEMPLATES.get(stem.replace(".md", "").replace("hypotheses_candidates/", ""))
    if not f1_body:
        return None
    falsifiers = [{"id": "F-SPECIFIC-1", "body": f1_body}] + [{"id": fid, "body": body} for fid, body in GENERIC_F234]
    honest = [{"id": lid, "body": body} for lid, body in GENERIC_L1234]
    cspec_l = candidate_specific_l(stem)
    honest.append({"id": cspec_l[0], "body": cspec_l[1]})
    cross = parent_h_for(stem)
    return falsifiers, honest, cross

def update_status(text: str) -> str:
    return re.sub(r"^(status: )candidate-needs-scaffolding\s*$",
                  r"\1candidate-falsifier-ready", text, count=1, flags=re.M)

def append_scaffold(text: str, falsifiers, honest, cross_links, notes=""):
    f_lines = "\n".join(f"- **{f['id']}**: {f['body']}" for f in falsifiers)
    l_lines = "\n".join(f"- **{l['id']}**: {l['body']}" for l in honest)
    x_lines = "\n".join(f"- {c}" for c in cross_links)
    block = f"""

## Falsifiers (scaffolded cycle #6 batch 3 V8-template, {TODAY})

{f_lines}

## Honest Limits (scaffolded cycle #6 batch 3 V8-template, {TODAY})

{l_lines}

## Cross-Links (scaffolded cycle #6)

{x_lines}

## Scaffold Notes

V8 ULTRA-FUSION cluster batch-scaffold using generic-template F2-F4 + per-candidate F1. Likely promotion fate: absorption to a future H_182 (V8 mechanism comparison meta-cluster) rather than individual H. Per-Hc deeper verification deferred to cycle #7.
"""
    return text.rstrip() + block + "\n"

def main():
    candidates = list(F1_TEMPLATES.keys())
    processed = 0
    skipped = 0
    for stem in candidates:
        path = ANIMA / "hypotheses_candidates" / f"{stem}.md"
        if not path.exists():
            print(f"NOT FOUND: {stem}")
            skipped += 1
            continue
        text = path.read_text(encoding="utf-8")
        if "candidate-needs-scaffolding" not in text:
            print(f"SKIP (status mismatch): {stem}")
            skipped += 1
            continue
        block = build_block(stem)
        if not block:
            print(f"NO F1 TEMPLATE: {stem}")
            skipped += 1
            continue
        falsifiers, honest, cross = block
        new_text = update_status(text)
        new_text = append_scaffold(new_text, falsifiers, honest, cross)
        path.write_text(new_text, encoding="utf-8")
        print(f"WROTE: {stem}")
        processed += 1
    print(f"\n--- DONE: {processed} processed, {skipped} skipped ---")

if __name__ == "__main__":
    main()
