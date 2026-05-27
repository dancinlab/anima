#!/usr/bin/env python3
# tool/_all_kick_extract_run.py — extract Python from .hexa parts.push() and run.
# Bypass for hexa CLI dispatch-only mode (#196/#200) — declarative emit only, no execution.
# raw#37 transient runner. Not committed; repo-local convenience.
import os, re, subprocess, sys, tempfile, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

HELPERS = [
    ("cycle1_r46",          "tool/anima_r46_primary_zone_resolver.hexa",
                            {"ANIMA_OUTPUT": "state/r46_primary_zone_candidates.json"}),
    ("cycle2_cmt_v2_5bb",   "tool/anima_cmt_v2_5bb_retest_dispatch.hexa",
                            {"ANIMA_OUTPUT": "state/cmt_v2_5bb_retest_pre_register.json"}),
    ("cycle3_axis96_llama", "tool/anima_axis96_llama_stride1_dispatch.hexa",
                            {"ANIMA_OUTPUT": "state/axis96_llama_stride1_pre_register.json"}),
    ("cycle4_mk_xii_gemma", "tool/anima_mk_xii_3a_gemma_familyinternal_dispatch.hexa",
                            {"ANIMA_OUTPUT": "state/mk_xii_3a_gemma_familyinternal_pre_register.json"}),
    ("cycle5_axis96_6th",   "tool/anima_axis96_6th_bb_arch_separator_dispatch.hexa",
                            {"ANIMA_OUTPUT": "state/axis96_6th_bb_arch_separator_pre_register.json", "ANIMA_BB_PICK": "all"}),
    ("cycle6_pilot_t2",     "tool/anima_pilot_t2_launch_gate_dispatch.hexa",
                            {"ANIMA_OUTPUT": "state/pilot_t2_launch_gate_dispatch.json"}),
    ("cycle7_own3_de",      "tool/anima_own3_de_wording_revision_verifier.hexa",
                            {"ANIMA_OUTPUT": "state/own3_de_wording_revision_verifier.json"}),
    ("cycle8_r45_v4",       "tool/anima_zombie_posterior_v4_17sub_candidate_selector.hexa",
                            {"ANIMA_OUTPUT": "state/zombie_posterior_v4_17sub_candidate_selector.json"}),
    ("cycle9_mk_xii_3b_70b","tool/anima_mk_xii_3b_70b_prep_dispatch.hexa",
                            {"ANIMA_OUTPUT": "state/mk_xii_3b_70b_prep.json"}),
    ("cycle10_eeg_cp2_7day","tool/anima_eeg_cp2_7day_arrival_gate_dispatch.hexa",
                            {"ANIMA_OUTPUT": "state/eeg_cp2_7day_arrival_gate.json"}),
    ("cycle11_mk_xii_llama","tool/anima_mk_xii_3a_llama_familyinternal_dispatch.hexa",
                            {"ANIMA_OUTPUT": "state/mk_xii_3a_llama_familyinternal_pre_register.json"}),
    ("cycle12_r46_verdict", "tool/anima_r46_verdict_consolidator.hexa",
                            {"ANIMA_OUTPUT": "state/r46_verdict_consolidator.json"}),
    ("cycle13_h100_p1",     "tool/anima_h100_p1_single_pilot_precheck.hexa",
                            {"ANIMA_OUTPUT": "state/h100_p1_single_pilot_precheck.json"}),
    ("cycle14_v11_filter",  "tool/anima_paradigm_v11_axis_filter_consolidator.hexa",
                            {"ANIMA_OUTPUT": "state/paradigm_v11_axis_filter_consolidator.json"}),
    ("cycle15_composite",   "tool/anima_composite_production_gate_aggregator.hexa",
                            {"ANIMA_OUTPUT": "state/anima_composite_production_gate.json"}),
    ("cycle16_axis82",      "tool/anima_axis82_4axis_exhaustion_closure_consolidator.hexa",
                            {"ANIMA_OUTPUT": "state/axis82_4axis_exhaustion_closure.json"}),
    ("cycle17_atlas_intg",  "tool/anima_atlas_rtier_integrity_verifier.hexa",
                            {"ANIMA_OUTPUT": "state/atlas_rtier_integrity_verifier.json"}),
    ("cycle18_atlas_remed", "tool/anima_atlas_drift_remediation_proposer.hexa",
                            {"ANIMA_OUTPUT": "state/atlas_drift_remediation_proposer.json"}),
    ("cycle20_handoff_ext", "tool/anima_session_handoff_extension_generator.hexa",
                            {"ANIMA_OUTPUT": "state/session_handoff_extension_generator.json",
                             "ANIMA_HANDOFF_OUT": "docs/session_handoff_20260427_extension.md"}),
    ("cycle21_chflags",     "tool/anima_ssot_chflags_lock_state_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/ssot_chflags_lock_state_auditor.json"}),
    ("cycle22_inventory",   "tool/anima_tool_dir_helper_inventory.hexa",
                            {"ANIMA_OUTPUT": "state/tool_dir_helper_inventory.json"}),
    ("cycle23_state_inv",   "tool/anima_state_dir_inventory_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/state_dir_inventory_auditor.json"}),
    ("cycle24_docs_md",     "tool/anima_docs_dir_md_integrity_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/docs_dir_md_integrity_auditor.json"}),
    ("cycle25_memory_stale","tool/anima_memory_dir_staleness_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/memory_dir_staleness_auditor.json"}),
    ("cycle26_gitignore",   "tool/anima_gitignore_comprehensive_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/gitignore_comprehensive_auditor.json"}),
    ("cycle27_nexus",       "tool/anima_nexus_roadmaps_consistency_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/nexus_roadmaps_consistency_auditor.json"}),
    ("cycle28_ci",          "tool/anima_ci_workflows_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/ci_workflows_auditor.json"}),
    ("cycle29_refs_dep",    "tool/anima_references_external_dep_tree_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/references_external_dep_tree_auditor.json"}),
    ("cycle30_subrepos",    "tool/anima_subrepo_cross_link_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/subrepo_cross_link_auditor.json"}),
    ("cycle31_ready",       "tool/anima_ready_dir_audit.hexa",
                            {"ANIMA_OUTPUT": "state/ready_dir_audit.json"}),
    ("cycle32_ws_siblings", "tool/anima_workspace_sibling_repos_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/workspace_sibling_repos_auditor.json"}),
    ("cycle33_worktrees",   "tool/anima_worktrees_agent_inventory_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/worktrees_agent_inventory_auditor.json"}),
    ("cycle34_bin",         "tool/anima_bin_executables_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/bin_executables_auditor.json"}),
    ("cycle35_archives",    "tool/anima_workspace_archives_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/workspace_archives_auditor.json"}),
    ("cycle36_ws_full",     "tool/anima_workspace_full_repo_inventory.hexa",
                            {"ANIMA_OUTPUT": "state/workspace_full_repo_inventory.json"}),
    ("cycle37_hive",        "tool/anima_hive_repo_deep_audit.hexa",
                            {"ANIMA_OUTPUT": "state/hive_repo_deep_audit.json"}),
    ("cycle38_nexus",       "tool/anima_nexus_repo_deep_audit.hexa",
                            {"ANIMA_OUTPUT": "state/nexus_repo_deep_audit.json"}),
    ("cycle39_void",        "tool/anima_void_repo_deep_audit.hexa",
                            {"ANIMA_OUTPUT": "state/void_repo_deep_audit.json"}),
    ("cycle40_papers",      "tool/anima_papers_repo_deep_audit.hexa",
                            {"ANIMA_OUTPUT": "state/papers_repo_deep_audit.json"}),
    ("cycle41_n6",          "tool/anima_n6_architecture_repo_deep_audit.hexa",
                            {"ANIMA_OUTPUT": "state/n6_architecture_repo_deep_audit.json"}),
    ("cycle42_capstone",    "tool/anima_ecosystem_cross_repo_capstone.hexa",
                            {"ANIMA_OUTPUT": "state/ecosystem_cross_repo_capstone.json"}),
    ("cycle43_remaining8",  "tool/anima_remaining_8_repos_batch_audit.hexa",
                            {"ANIMA_OUTPUT": "state/remaining_8_repos_batch_audit.json"}),
    ("cycle44_subrepos_deep","tool/anima_subrepos_deep_composite_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/subrepos_deep_composite_auditor.json"}),
    ("cycle45_super_capstone","tool/anima_final_super_aggregator_cycles_1_44.hexa",
                            {"ANIMA_OUTPUT": "state/final_super_aggregator_cycles_1_44.json"}),
    ("cycle46_contact",     "tool/anima_contact_repo_deep_audit.hexa",
                            {"ANIMA_OUTPUT": "state/contact_repo_deep_audit.json"}),
    ("cycle47_dynamic_ssot","tool/anima_dynamic_ssot_activity_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/dynamic_ssot_activity_auditor.json"}),
    ("cycle48_handoff_v2",  "tool/anima_session_handoff_extension_v2_generator.hexa",
                            {"ANIMA_OUTPUT": "state/session_handoff_extension_v2_generator.json",
                             "ANIMA_HANDOFF_OUT": "docs/session_handoff_20260427_extension_v2.md"}),
    ("cycle49_pi_telegram", "tool/anima_pi_telegram_minor_audit.hexa",
                            {"ANIMA_OUTPUT": "state/pi_telegram_minor_audit.json"}),
    ("cycle50_git_chain",   "tool/anima_session_git_commit_chain_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/session_git_commit_chain_auditor.json"}),
    ("cycle51_engines",     "tool/anima_engines_subrepo_deep_audit.hexa",
                            {"ANIMA_OUTPUT": "state/engines_subrepo_deep_audit.json"}),
    ("cycle52_runpod_active","tool/anima_runpod_active_pods_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/runpod_active_pods_auditor.json"}),
    ("cycle53_external_gpu","tool/anima_external_gpu_combined_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/external_gpu_combined_auditor.json"}),
    ("cycle54_runaway",     "tool/anima_runpod_runaway_cost_incident_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/runpod_runaway_cost_incident_auditor.json"}),
    ("cycle56_ssh_activity","tool/anima_runpod_pods_ssh_activity_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/runpod_pods_ssh_activity_auditor.json"}),
    ("cycle57_root_cause",  "tool/anima_h100_cap_enforcement_root_cause_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/h100_cap_enforcement_root_cause_auditor.json"}),
    ("cycle58_full_chain",  "tool/anima_h100_full_chain_remediation_proposer.hexa",
                            {"ANIMA_OUTPUT": "state/h100_full_chain_remediation.json"}),
    ("cycle59_incident_capstone","tool/anima_runpod_incident_chain_capstone.hexa",
                            {"ANIMA_OUTPUT": "state/runpod_incident_chain_capstone.json"}),
    ("cycle60_super_super","tool/anima_super_super_capstone_cycles_1_59.hexa",
                            {"ANIMA_OUTPUT": "state/super_super_capstone_cycles_1_59.json"}),
    ("cycle61_local_system","tool/anima_local_system_background_auditor.hexa",
                            {"ANIMA_OUTPUT": "state/local_system_background_auditor.json"}),
    ("cycle62_secrets",     "tool/anima_secrets_dir_metadata_audit.hexa",
                            {"ANIMA_OUTPUT": "state/secrets_dir_metadata_audit.json"}),
]

PUSH_RE = re.compile(r'parts\.push\("((?:\\.|[^"\\])*)"\)')

def extract_python(hexa_path):
    with open(hexa_path) as f:
        src = f.read()
    pieces = []
    for m in PUSH_RE.finditer(src):
        raw = m.group(1)
        decoded = raw.encode('utf-8').decode('unicode_escape')
        pieces.append(decoded)
    return "".join(pieces)

results = []
for name, hexa, env in HELPERS:
    py = extract_python(hexa)
    if not py.strip():
        results.append((name, "EXTRACT_EMPTY", ""))
        continue
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, dir='/tmp', prefix=f'allkick_{name}_') as tf:
        tf.write(py)
        tmp_path = tf.name
    full_env = os.environ.copy()
    full_env.update(env)
    try:
        r = subprocess.run(['python3', tmp_path], env=full_env, capture_output=True, text=True, timeout=30)
        results.append((name, 'OK' if r.returncode == 0 else f'FAIL_rc{r.returncode}',
                        (r.stdout or '').strip().splitlines()[-1] if r.stdout else (r.stderr or '').strip().splitlines()[-1] if r.stderr else ''))
    except subprocess.TimeoutExpired:
        results.append((name, 'TIMEOUT', ''))
    except Exception as e:
        results.append((name, f'EXC_{type(e).__name__}', str(e)))

print("=== all_kick result ===")
for name, status, last in results:
    print(f"  {name:30s} {status:12s} {last}")
print()
print(f"summary: ok={sum(1 for _,s,_ in results if s=='OK')}/{len(results)}")
