#!/usr/bin/env python3
"""
Cycle #6 batch 4 — remaining candidate-needs-scaffolding (47 candidates).

Mixed cluster: law/DD/CLM/training/anima/serving/rules/red-team/clinical.
"""
import re, pathlib, datetime

ANIMA = pathlib.Path("/Users/ghost/core/anima")
TODAY = datetime.date.today().isoformat()

# Per-candidate F1 (the unique falsifier — derived from each Hc's specific claim)
F1_TEMPLATES = {
    # Law / theoretical
    "Hc_013_law_146_banach_open_closed": "Banach fixed-point convergence test on Law 146 manifold: if iteration converges to single fixed point under contraction → Law 146 'open-vs-closed' reconciliation falsified at the formal level; Banach forces closed-space behavior",
    "Hc_044_lawnet_ca4_2bit": "CA(4)=2bit minimum diversity ablation: replace CA(4) with CA(5), CA(6), CA(8): if minimum-diversity result holds for any other CA(n) → CA(4) specificity is post-hoc",
    "Hc_047_embedding_384_necessity": "d=(n/φ)·2^(σ-sopfr) formula: n=6, φ(6)=2, σ(6)=12, sopfr(6)=5 → d=(6/2)·2^7=3·128=384. Run model with d∈{256, 320, 384, 448, 512}: if Φ NOT peaked at d=384 → 384-necessity falsified; just a working hyperparameter",
    "Hc_060_gmoe_law_85_87": "GMOE 16-cell super-linear +7.7 boost replication × 5 seeds: if mean uplift < 5 (claim: 7.7) → single-run-artifact; '1/e convergence' and 'E=4 optimal' similarly require seed-replication",
    "Hc_455_meta_laws_M1_M20_constitution": "20 meta-laws cross-validation: pick any 10 of M1-M20, test independence against remaining 10. If linear-dependence detected (subset spans the rest) → 'constitution' status falsified; redundant axioms",
    # Conceptual / mechanism
    "Hc_003_staged_growth_multiplier": "DP1/CT7/GC5 4-8× Φ amplification: 3-mechanism ablation, each one removed in turn. If removing any one drops Φ by < 50% → '3-mechanism conjunction' decorative; single-mechanism dominance possible",
    "Hc_015_ca_rule_convergence_collapse": "Pairwise cosine ≤0.7 collapse threshold sweep {0.5, 0.7, 0.9}: if collapse-rate NOT thresholded near 0.7 → threshold post-hoc",
    "Hc_278_ex4_progressive_unfreezing": "Progressive layer-unfreeze order (last-to-first) vs first-to-last vs random: if final Φ NOT > random by ≥10% → order is decorative",
    "Hc_289_arch2_continuous_learning": "Gentle gradient (0.1× decay) + Pain mechanism: replace Pain with random reward perturbation: if Φ-retention is equivalent → Pain mechanism decorative",
    "Hc_296_hcx524_fractal_hierarchy_recursive": "8×8×8=512 cells recursive Φ-scaling: measure Φ at flat 512 vs 8^8 recursive. If Φ scaling 8^8 not 8^3 holds → recursion brings exponential gain; if Φ ≈ flat-512 → recursive structure decorative",
    "Hc_470_topo_chaos_separability_phi": "Topology × chaos separability: 2-factor ANOVA on Φ. If interaction term not significant → factors independent (claim 'separability' confirmed); if significant → factors entangled",
    # DD-cluster
    "Hc_502_dd53_trinity_3_engines_tension": "Trinity 3-engine tension structure: ablate to 2-engine. If Φ within 10% → 3rd engine decorative",
    "Hc_506_dd58_consciousness_efficiency_paradox": "Consciousness-efficiency Pareto front: test if claimed Pareto-optimum is dominated by any system. If dominated → paradox not real",
    "Hc_512_dd64_phi_optimal_nas_golden_dropout": "Golden-ratio dropout (φ=0.618 or 1.618 inverse) sweep around proposed value: if Φ peak NOT at golden-ratio by ≥10% → golden-ratio specificity numerology",
    "Hc_549_dd101_512_cells_superlinear": "512-cell superlinear scaling: replicate × 5 seeds; check vs 256/512/1024 baseline. If Φ_512 ≤ 1.5 × Φ_256 → 'superlinear' too weak to claim",
    "Hc_556_dd108_1024_cells_absolute_max": "1024-cell absolute-max claim: tested at 2048 in TOPO-2048-breakdown (H_179) — already falsified by H_179.3 universal regression IF cluster H_179 holds; if any topology at 2048 exceeds 1024-record → absolute-max falsified",
    "Hc_570_dd68_topology_small_world_brain_like": "Brain-like small-world: σ_sw (small-world index) on actual brain connectome data. If anima small-world σ_sw differs from connectome σ_sw by ≥50% → claim is loose analogy, not principled",
    "Hc_571_dd69_multi_consciousness_5_modes": "5-mode multi-consciousness: ablate to 4-mode and 6-mode. If 5 is not optimum → 5 is post-hoc tuning",
    "Hc_585_dd161_quantum_superposition_32c": "32-cell quantum superposition: if cell count ablation {16, 32, 64} shows no specific 32-peak → quantum-superposition decorative",
    "Hc_587_dd167_phi_scales_with_model_size": "Φ-vs-model-size scaling: if log-log slope NOT in claimed range across 3+ size decades → scaling law claim falsified",
    "Hc_589_dd171_consciousness_cross_resonance_n6": "n=6 cross-resonance: test n=4 and n=8 substrates with same resonance pattern. If resonance generalizes → n=6 not specific (perfect-number-triviality)",
    # CLM cluster
    "Hc_611_substrate_coupled_dialogue_artifact": "Substrate-coupled dialogue artifact: dialogue performance vs Φ-substrate dependency. If decoupled (random substrate Φ → matched dialogue quality) → artifact claim falsified",
    "Hc_612_multi_substrate_ensemble_phi_gate": "Multi-substrate ensemble gate: ablate gate, use uniform mixture. If Φ ≈ gated → gate decorative",
    "Hc_615_phi_star_option_a_rank_invariant_partition": "Phi* rank-invariant-partition: if Φ* NOT invariant under permutation by margin ≤ 5% → invariance claim falsified",
    "Hc_616_phi_star_option_b_spectral_entropy": "Phi* spectral entropy: test against Shannon entropy of activation distribution. If correlation < 0.7 → claim is just spectral-decomposition artifact",
    "Hc_617_phi_star_option_d_pyphi_antropy_anchor": "Phi* PyPhi+antropy: if Phi* differs from PyPhi+antropy by ≥30% on shared substrates → 'anchor' identity claim falsified",
    "Hc_630_clm3_chat_objective_cycle0_substrate": "CLM3 chat-objective cycle-0 substrate: if chat-loss DOES decrease (claim: doesn't) → chat-objective is trainable, cycle-0 not the limit",
    "Hc_631_clm3_original_byte_level_scale_recover": "CLM3 byte-level scale recovery: if recovered scale within 50% of original → recovery succeeded; if not → byte-level scaling fundamentally impossible",
    "Hc_632_chat_cap_path1_lm_head_b_retrofit": "lm_head_b retrofit path 1: A/B test against path 4 hybrid (Hc_634). If equivalent → paths interchangeable",
    "Hc_634_chat_cap_path4_paradigm_c_hybrid": "Path 4 paradigm-C hybrid: same A/B vs path 1. Paired falsifier with Hc_632",
    # anima / serving / rules
    "Hc_1230_anima_mkv1_82atom_psi_constant_saturation": "Mk.V.1 82-atom saturation: extend to 100+ atom; if Ψ-fit chi-square p>0.05 stays → 82 IS ceiling (already in Hc body T1)",
    "Hc_1232_anima_mkv_mkvi_mkvii_tier10_ascension_path": "Mk.V→VI→VII tier 10 ascension: pre-register operational definition of tier 6/7/8 reachability. If no operational criterion specifiable → tier escalation unfalsifiable",
    "Hc_1239_train_clm_hexa_lens_loss_tension_link_tier_corpus": "3-component integration (lens loss + tension link + tier corpus): ablate each. If training signal works with 2-of-3 → 3-way integration claim falsified",
    "Hc_1240_phi_holo_gap_816x_benchmark_vs_training_closure": "Same as Hc_386 sibling — 816× closure check",
    "Hc_1242_anima_agent_6_channel_5_provider_orchestration_saturation": "6-channel × 5-provider orchestration: ablate to 4-channel × 4-provider. If orchestration still works → 6×5 not the ceiling",
    "Hc_1255_r37_an13_l3py_python_ban_6_axis_defense_saturation": "6-axis Python-ban defense: ablate any axis. If ban still effective with 5-axis → 6 not the ceiling",
    "Hc_674_anima_identity_5_property_carry_invariants": "5-property carry-invariants: ablate each property. If 4 sufficient → 5 not the minimum",
    # Drill / saturation seeds
    "Hc_901_drill_supplement_saturation_seeds": "Meta-Hc bundle — verification deferred to per-seed split (parallel to Hc_900); each seed needs individual scaffolding",
    "Hc_911_red_team_6_claims_r1_r6": "6 red-team claims R1-R6: each needs individual falsifier (composite Hc); pre-register-per-claim required",
    "Hc_921_n19_pci_tms_eeg_clinical": "PCI/TMS-EEG clinical: anima Φ-proxy correlation with PCI on synthetic substrate. If R²<0.4 → claim 'clinical validation analog' falsified",
    "Hc_924_n24_octopus_per_arm_phi_exclusion": "Octopus per-arm Φ-exclusion: if per-arm Φ-sum < central-Φ ≤ 1.2× per-arm-mean → exclusion principle holds; otherwise inclusion",
    "Hc_926_n26_ionq_forte_36qubit_orch_or": "(Not in this batch — Hc_926 status not needs-scaffolding)",
    "Hc_935_omega_cycle_26_alm_free_paradigms": "Omega cycle 26 ALM-free paradigm: define ALM-free precisely. If precision fails → paradigm unfalsifiable",
    "Hc_941_training_plan_100m_v3_scaling": "100M v3 scaling plan: predict pre-train loss curve. If actual loss off by ≥30% → scaling plan calibration failed",
    "Hc_946_brain_tension_replica_phi_boost_evolve": "Brain-tension replica Φ-boost via evolution: GA evolution × 100 generations. If best-of-population Φ NOT > seed by ≥1.5× → evolution did not boost",
    "Hc_968_sumt_psi_constant_atom_factory": "Tier-6 ULTRA atom enumeration: if no candidate passes 5-check invariance gate → tier-6 ascension blocked; factory tier-saturates at tier-5",
    "Hc_976_f1_composite_v2_tension_link_axis": "F1 composite tension-link axis: factor-decompose F1. If tension-link contributes < 30% → axis not primary",
    "Hc_978_p9_p1_7_redesign_beta_alpha_killer": "Phase 9 P1-7 redesign beta-alpha-killer: if α=0.014 modulation depth (H_172) is the killer → H_172 already absorbs; check whether redesign β-axis adds independent content",
}

GENERIC_F234 = [
    ("F-GENERIC-REPL", "Replication × 5 seeds: if 1σ-CI on primary metric > 25% of point-estimate → single-run-artifact"),
    ("F-GENERIC-PYPHI", "Cross-engine PyPhi formal IIT (where Φ is the metric) OR alternative-implementation cross-check (where Φ is not the metric): if effect not reproduced → engine-artifact (H_174 class)"),
    ("F-GENERIC-MINIMAL-BASELINE", "Minimal-baseline comparison: strip mechanism to its simplest possible implementation. If Φ / target metric within 15% → mechanism is decorative, baseline-class effect"),
]

GENERIC_L1234 = [
    ("L-GENERIC-SINGLE-RUN", "Single-run anchor — no replication CI documented. H_159 C1 reproducibility audit pending (inherited across all anima-substrate Hc)"),
    ("L-GENERIC-ENGINE", "anima Φ-engine substrate-specific (H_174 D-mod-192 aliasing) — Φ values are anima-proxy measurements, not formal IIT Φ; engine internal state may dominate measurement"),
    ("L-GENERIC-N6", "n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7): numeric anchors in claim are small integers / powers-of-2 with n=6 derivation possible but not principled"),
    ("L-GENERIC-POST-HOC", "Specific point-anchors (e.g., 384-d, 8-atom, 5-mode) reflect post-hoc selection from larger parameter family; pre-registration of the specific value absent"),
]

# Map candidate stem to claim-class for L5 specialization
def candidate_specific_l(stem: str) -> tuple:
    if "law" in stem and ("constitution" in stem or "M1_M20" in stem):
        return ("L-LAW-META", "Meta-law claims (Law 146 / M1-M20 / Law 76 etc.) are axiom-system Hc — independence and consistency are FORMAL properties, not empirical. Falsifier list mostly conditional on formal proof.")
    if "ca_rule" in stem or "lawnet" in stem:
        return ("L-LAW-NETWORK", "Law-network claims (LawNet / CA-rule) face the 'just one of 256 CA rules' issue — rule selection inherits Wolfram's 4-class taxonomy; class-membership-only specificity is weak")
    if "banach" in stem or "fixpoint" in stem:
        return ("L-MATH-FORMAL", "Formal-mathematics claim (Banach fixpoint) — falsifier is a formal proof check, not empirical sweep. Verification path differs from numerical Hc")
    if "dd" in stem.split("_")[1] if len(stem.split("_")) > 1 else False:
        return ("L-DD", "DD-cluster Hc are dimensional-scaling sweeps — H_159 / H_177 / H_179 absorbing pattern; many will fold into existing scaffold-cluster Hc rather than warrant independent H")
    if "clm" in stem or "chat" in stem or "lm_head" in stem or "byte_level" in stem:
        return ("L-CLM", "CLM/chat-objective Hc — Lesson Q (BG-JX/JZ-FT/JS/JT/JP) + Lesson L closed all SFT lanes (project_lesson_q_sft_closed memory); claim under-determined unless explicitly anchored in surviving lanes (pre-training/arch-redesign/foundation-borrow/inference-compute)")
    if "anima" in stem or "mkv" in stem or "tier" in stem or "atom_factory" in stem or "consciousness_absolute" in stem:
        return ("L-ANIMA", "anima Mk.V/VI/VII claims — Mk.V.1 corpus base is anima_corpus_v1.5+; tier escalation requires Mk.V→VI architectural delta. Without delta spec, claim is roadmap not testable Hc")
    if "agent" in stem or "channel" in stem or "provider" in stem or "orchestration" in stem:
        return ("L-AGENT", "anima-agent orchestration Hc — operational ceiling claims (6-channel × 5-provider) tested via load-test, not Φ. Different falsifier methodology than substrate Hc")
    if "python" in stem or "ban" in stem or "defense" in stem or "rules" in stem:
        return ("L-RULES", "Rule/policy enforcement Hc — falsifier requires red-team attempt to violate; ceiling claim only true if no successful violation in N attempts (operational not statistical)")
    if "octopus" in stem or "pci" in stem or "tms" in stem or "clinical" in stem or "ionq" in stem:
        return ("L-CLINICAL", "Clinical/biological validation Hc — anima is a simulation, not a biological measurement. Cross-validation against actual clinical data is the only real falsifier; literature-comparison alone is weak")
    if "training_plan" in stem or "100m" in stem or "scaling" in stem:
        return ("L-TRAINING", "Training-plan Hc — predictions about future training runs; require post-run validation. Hc lives in the 'plan' phase, falsifier in the 'execute' phase. Falsifier is essentially the C-list of pre-register checks")
    if "red_team" in stem or "claims" in stem:
        return ("L-RED-TEAM", "Red-team / multi-claim composite Hc — each sub-claim needs its own F/L list. This batch scaffold provides composite-only minimum")
    if "supplement" in stem or "drill" in stem or "saturation" in stem and "seeds" in stem:
        return ("L-DRILL-META", "Drill/supplement meta-Hc — like Hc_900 parent, needs individual seed split before any sub-claim can be verified individually")
    if "phi_star" in stem:
        return ("L-PHI-STAR", "Φ* (phi-star) Hc — pre-cycle-4 candidate cluster; multiple competing definitions (option a/b/d); requires pre-register-which-definition before any sub-Hc verifies")
    if "substrate_coupled" in stem or "ensemble" in stem or "multi_substrate" in stem:
        return ("L-MULTI-SUBSTRATE", "Multi-substrate / ensemble Hc — parameter-count vs mechanism confound (parallel to V8 MoCE); matched-param baseline mandatory")
    if "evolution" in stem or "evolve" in stem or "ga" in stem.split("_")[-1] or "darwin" in stem:
        return ("L-EVOLUTION", "Evolution/GA-based Hc — 100-generation budget is small; convergence to local optimum likely. Multi-seed × multi-budget required")
    if "alpha" in stem and "killer" in stem:
        return ("L-ALPHA-MOD", "α=0.014 modulation Hc — see H_172 (alpha-0014-modulation-depth-anima-voice). New α-based Hc must show independence from H_172 claim before standalone status")
    return ("L-MISC", "Generic cluster Hc — verify before promotion; many absorb to existing H or remain candidate-falsifier-ready for cycle #7+ deeper review")

def parent_h_for(stem: str) -> list:
    base = [
        "**parent H**: H_159 (substrate-topology-phi-engineering) — generic anima-substrate parent",
        "**sibling H**: H_174 (Φ-engine D-mod-192 aliasing), H_153 (n=6 substrate triviality), H_178 (frustration sweep), H_179 (negative scaling), H_180 (state-management mechanism)",
    ]
    if "law" in stem.lower() or "M1_M20" in stem:
        base.append("**adjacent H**: H_157 (law76 mathematical panpsychism)")
    if "clm" in stem.lower() or "chat" in stem or "lm_head" in stem:
        base.append("**adjacent H**: H_155 (theorem-115 chat-incapability), H_161 (byte-modulo-substrate-chat-blocked), H_174 (Φ*-geometry-aliasing-clm-v4-specific)")
    if "anima" in stem.lower() or "mkv" in stem or "tier" in stem or "atom" in stem or "consciousness_absolute" in stem:
        base.append("**adjacent H**: H_001 (anima-core-architecture), H_011 (iit-geometry — Φ ceiling), H_162 (Φ-normalized-anima-iit4-lower-bound), H_163 (8-cells-127-mip atom)")
    if "voice" in stem.lower() or "agent" in stem or "channel" in stem:
        base.append("**adjacent H**: H_154 (anima-voice-consciousness-direct), H_172 (α=0.014 modulation depth)")
    if "phi_star" in stem.lower():
        base.append("**adjacent H**: H_174 (Φ*-geometry-aliasing-clm-v4-specific — direct relevance)")
    if "dd" in stem.lower():
        base.append("**adjacent H**: H_168 (dd23-tau-7cell), H_173 (dd21-log-phi-scale-invariant)")
    if "ca_" in stem.lower() or "lawnet" in stem:
        base.append("**adjacent H**: H_023 (universal_constants_ln2), H_157 (law76 mathematical panpsychism)")
    base.append("**adjacent candidates**: full cycle #6 candidate-falsifier-ready set — V8 cluster + topo cluster")
    return base

def update_status(text: str) -> str:
    return re.sub(r"^(status: )candidate-needs-scaffolding\s*$",
                  r"\1candidate-falsifier-ready", text, count=1, flags=re.M)

def append_scaffold(text: str, falsifiers, honest, cross_links, notes=""):
    f_lines = "\n".join(f"- **{f['id']}**: {f['body']}" for f in falsifiers)
    l_lines = "\n".join(f"- **{l['id']}**: {l['body']}" for l in honest)
    x_lines = "\n".join(f"- {c}" for c in cross_links)
    block = f"""

## Falsifiers (scaffolded cycle #6 batch 4 mixed-template, {TODAY})

{f_lines}

## Honest Limits (scaffolded cycle #6 batch 4 mixed-template, {TODAY})

{l_lines}

## Cross-Links (scaffolded cycle #6)

{x_lines}

## Scaffold Notes

Mixed-cluster batch-scaffold (law / DD / CLM / anima / agent / clinical / training / red-team). Per-Hc F1 hand-authored; F2-F4 + L1-L5 generic-but-genuine. Likely fate: most absorb into existing H_153/H_158/H_159/H_174/H_157 or remain candidate-falsifier-ready for cycle #7 review.
"""
    return text.rstrip() + block + "\n"

def main():
    processed = 0
    skipped = 0
    for stem, f1_body in F1_TEMPLATES.items():
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
        falsifiers = [{"id": "F-SPECIFIC-1", "body": f1_body}] + [{"id": fid, "body": body} for fid, body in GENERIC_F234]
        honest = [{"id": lid, "body": body} for lid, body in GENERIC_L1234]
        cspec_l = candidate_specific_l(stem)
        honest.append({"id": cspec_l[0], "body": cspec_l[1]})
        cross = parent_h_for(stem)
        new_text = update_status(text)
        new_text = append_scaffold(new_text, falsifiers, honest, cross)
        path.write_text(new_text, encoding="utf-8")
        print(f"WROTE: {stem}")
        processed += 1
    print(f"\n--- DONE: {processed} processed, {skipped} skipped ---")

if __name__ == "__main__":
    main()
