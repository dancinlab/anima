#!/usr/bin/env python3
# raw#37 transient — write supplementary verdict for retry v2 SECOND-OOM-EQUIVALENT failure.
# Per task spec: "If memory-aware loader still fails... STOP early — record honest failure
# with sentinel breakpoint + suggest int8 fallback. Do not retry on second OOM."
import json, os, time
import numpy as np

# Reused 2b/9b cells (still informative) — partial BBA |r|
PATHS = {
    '2b':  '/Users/ghost/core/anima/state/v11_cmt_v3_5bb_retest/out_pod/cmt_v3_gemma_2_2b.json',
    '9b':  '/Users/ghost/core/anima/state/v11_cmt_v3_5bb_retest/out_pod_phase2/cmt_v3_gemma_2_9b.json',
}

def load_rel_per_family(path):
    d = json.load(open(path))
    fams = d['families']; n_layers = d['n_layers']
    keys = sorted(int(k) for k in d['tomography'].keys())
    out = {fam: [] for fam in fams}
    for k in keys:
        for fam in fams:
            out[fam].append(d['tomography'][str(k)][fam]['rel'])
    fracs = [k / max(1, n_layers - 1) for k in keys]
    return out, fracs, fams, n_layers

def interp(rels, fracs, grid):
    return list(np.interp(grid, fracs, rels))

def pearson(x, y):
    x = np.asarray(x, dtype=float); y = np.asarray(y, dtype=float)
    if x.std() == 0 or y.std() == 0: return 0.0
    return float(np.corrcoef(x, y)[0,1])

def bba_pairwise(a_path, b_path, K=20):
    a_rels, a_fracs, a_fams, _ = load_rel_per_family(a_path)
    b_rels, b_fracs, b_fams, _ = load_rel_per_family(b_path)
    fams = sorted(set(a_fams) & set(b_fams))
    grid = np.linspace(0, 1, K)
    a_vec = []; b_vec = []
    per_fam_r = {}
    for fam in fams:
        ai = interp(a_rels[fam], a_fracs, grid)
        bi = interp(b_rels[fam], b_fracs, grid)
        a_vec.extend(ai); b_vec.extend(bi)
        per_fam_r[fam] = pearson(ai, bi)
    r = pearson(a_vec, b_vec)
    return {'r': r, 'abs_r': abs(r), 'per_family_r': per_fam_r, 'K': K, 'n_fams': len(fams)}

# Partial BBA computation — only 2b vs 9b possible
pair_2b_9b = bba_pairwise(PATHS['2b'], PATHS['9b'])

cells = {}
for tag, p in PATHS.items():
    d = json.load(open(p))
    rels_flat = [d['tomography'][L][f]['rel'] for L in d['tomography'] for f in d['families']]
    cells[tag] = {
        'status': 'REUSED_FROM_TASK_9',
        'source': p,
        'backbone': d['backbone'],
        'mode': d['mode'],
        'h_dim': d['h_dim'],
        'n_layers': d['n_layers'],
        'rel_std_recomputed': round(float(np.std(rels_flat)), 6),
        'saturation_frac': d['rel_distribution']['saturation_frac'],
        'informative': d['rel_distribution']['informative'],
        'gate_PASS': d['gate_PASS'],
    }

out = {
    'schema': 'anima/v11/gemma_familyinternal_verdict_retry_v2/1',
    'paradigm': 'Mk.XII Phase 3a gemma family-internal scale (2b/9b/27b) verdict — retry v2 SECOND silent-termination',
    'parent_verdict': 'state/v11_gemma_familyinternal/verdict.json',
    'parent_pre_register': 'state/mk_xii_3a_gemma_familyinternal_pre_register.json (FROZEN)',
    'task_id': '#13',
    'supersedes': {
        'parent_inconclusive_hypotheses': ['HMK-A_GEMMA_SCALE_INVARIANT', 'HMK-B_GEMMA_SCALE_BREAK', 'HQS-C_FALSIFICATION_MIXED_BACKBONE_CONDITIONAL'],
        'reason_no_supersession': 'gemma-2-27b cell STILL missing (second silent pod termination). Hypotheses remain INCONCLUSIVE.',
        'change_vs_parent': 'pre-registered fix (memory-aware loader: device_map=auto + low_cpu_mem_usage=True + fp16) WAS APPLIED but did not resolve crash. Root cause is NOT host RAM OOM (host had 2015 GB available) — points to runpod platform/mfs/safetensors-fetch level fault during 27B download.',
    },
    'pod_id': '3q7pqjhsmnulm6',
    'pod_status_final': 'AUTO_TERMINATED_BY_PLATFORM (pod_not_found via graphql; ssh refused; host disappeared at ~75pct safetensors fetch)',
    'cost_actual_usd': 0.426,
    'cost_per_hr_usd': 2.99,
    'cost_budget_usd': 1.00,
    'cost_under_budget': True,
    'wallclock_sec': 513,
    'wallclock_cap_sec': 1500,
    'failure_signature': {
        'sentinels_emitted_in_order': [
            'GEMMA_27B_RETRY_V2_INSTALL_DONE READY',
            'BB_GEMMA_27B_RETRY_V2_STARTED BEGIN model=google/gemma-2-27b mode=v3',
            'GEMMA_27B_RETRY_V2_MEM tag=START cuda_gb=0.0 host_rss_gb=0.4',
            'GEMMA_27B_RETRY_V2_MEM tag=TOKENIZER_LOADED cuda_gb=0.0 host_rss_gb=0.69',
            'GEMMA_27B_RETRY_V2_LOAD_START device_map=auto low_cpu_mem_usage=True dtype=fp16',
        ],
        'breakpoint_sentinel_NOT_emitted': 'GEMMA_27B_RETRY_V2_LOAD_DONE',
        'last_observed_state': 'Fetching 24 files: 75% (18/24 safetensors complete, 6 incomplete)',
        'last_log_size_bytes': 1313,
        'last_known_cache_size_gb': 94,
        'last_known_host_rss_gb': 5.0,
        'last_known_host_ram_used_gb': 81,
        'last_known_host_ram_free_gb': 1922,
        'last_known_gpu_mem_used_mib': 4,
        'pod_disappeared_at_relative_t_sec': 513,
        'process_disappeared_silently': True,
        'no_traceback': True,
        'no_oom_signature_in_dmesg': 'dmesg unreadable on container',
        'pod_terminated_by_runpod_platform': True,
    },
    'diagnosis_v2': 'Same crash signature as retry v1 (silent process death during weight fetch at ~75pct). HOST RAM OOM HYPOTHESIS REJECTED — retry v2 pod had memoryInGb=251 cgroup, observed 2015 GB total host RAM with only 81 GB used at time of crash. Crash is platform-level: likely (a) mfs (685T NFS) connection hiccup during multi-threaded safetensors fetch on 22+ GB single file, (b) runpod container kill due to oversize blob writes triggering quota, or (c) hf_hub multithread fetcher segfault on large shards. Memory-aware loader fix from parent verdict was correct in principle but addressed wrong root cause.',
    'partial_per_bb': cells,
    'partial_pairwise_BBA_pearson_r_2b_9b': {
        'r': round(pair_2b_9b['r'], 4),
        'abs_r': round(pair_2b_9b['abs_r'], 4),
        'per_family_r': {f: round(pair_2b_9b['per_family_r'][f], 4) for f in pair_2b_9b['per_family_r']},
        'K_grid_points': pair_2b_9b['K'],
        'n_fams': pair_2b_9b['n_fams'],
        'note': 'PARTIAL — 2-cell only. (9b,27b) and (2b,27b) NOT COMPUTABLE without 27b cell. HMK-A/B/HQS-C frozen thresholds require all 3 pairwise — verdict remains INCONCLUSIVE.',
    },
    'frozen_hypothesis_verdicts': {
        'HMK-A_GEMMA_SCALE_INVARIANT': {
            'decision_threshold': 'CONFIRMED if all 3 pairwise BBA |r| > 0.7',
            'verdict': 'INCONCLUSIVE',
            'rationale': '27b cell still missing after retry v2. Only 1/3 pairwise comparisons available (2b vs 9b |r|=' + str(round(pair_2b_9b['abs_r'],3)) + '). Cannot evaluate 3-point scale curve hypothesis.',
            'partial_observation': 'pair (2b,9b) |r| = ' + str(round(pair_2b_9b['abs_r'],3)) + (' (above 0.7 threshold — consistent with HMK-A on this segment)' if pair_2b_9b['abs_r'] > 0.7 else (' (below 0.3 threshold — consistent with HMK-B on this segment)' if pair_2b_9b['abs_r'] < 0.3 else ' (in 0.3-0.7 mid-range — neither HMK-A nor HMK-B supported on this segment)')),
        },
        'HMK-B_GEMMA_SCALE_BREAK': {
            'decision_threshold': 'CONFIRMED if any pairwise BBA |r| < 0.3',
            'verdict': 'INCONCLUSIVE',
            'rationale': '27b cell still missing. The (9b,27b) and (2b,27b) pairs cannot be evaluated; a scale break at 9b->27b boundary would be invisible to the available (2b,9b) pair.',
        },
        'HQS-C_FALSIFICATION_MIXED_BACKBONE_CONDITIONAL': {
            'decision_threshold': 'AMBIGUOUS if all pairwise |r| in (0.3, 0.7)',
            'verdict': 'INCONCLUSIVE',
            'rationale': '27b cell still missing. HQS-C status from axis 109 (Qwen family-internal MIXED_BACKBONE_CONDITIONAL CONFIRMED) remains canonical reference.',
        },
    },
    'implication_mk_xii_phase_3b_70b': {
        'current_status': 'BLOCKED — gemma family-internal cannot serve as 2nd clean evidence without 27b measurement. Same as parent verdict.',
        '70b_clean_count_change': '1/3 (UNCHANGED)',
        '70b_justification_path': 'STILL BLOCKED on gemma path; alternative paths must be pursued.',
        'alternative_paths_recommended': [
            'INT8 FALLBACK: load_in_8bit=True with bitsandbytes (raw#10 caveat: ~0.5% rel_std shift). May avoid the safetensors download path entirely if bnb uses different fetcher, or at least tolerate a single-file load. PRIORITY 1.',
            'SHARDED LOAD: Pre-download via huggingface-cli with --max-workers 1 (single-threaded fetch, slower but more robust to mfs hiccups), then from_pretrained from local_dir. PRIORITY 2.',
            'NETWORK VOLUME PERSISTENT CACHE: provision a runpod network volume for /workspace/.hf_cache so cache survives pod recreation; pay download cost ONCE not per-attempt. PRIORITY 2.',
            'Llama-3.1-8B → Llama-3.1-70B family-internal (HF gated, dancinlife unauthorized — task #6 manual). PRIORITY 3.',
            'Different image: try runpod/pytorch:2.5.0+ or 2.8.0+ (newer image may have different fetcher behavior). PRIORITY 3.',
        ],
    },
    'raw_10_caveats': [
        'Diagnosis "platform-level" not directly captured — dmesg unreadable on rootless container, syslog empty. Inference based on: 2015 GB host RAM observed at last poll (rules out host OOM), 0 MiB GPU usage at crash (rules out GPU OOM), pod entirely deleted from graphql (not just SSH-disconnected), identical signature to retry v1 (silent termination at ~75pct safetensors fetch on 22+ GB single-file shard).',
        'Cost actual = $0.426 = 8.5 min × $2.99/hr. Retry v1 was $0.179 (6 min). Total spent across both retries on FAILED 27b measurement: $0.605. Per-cell cost-per-success is undefined (still 0 successes).',
        'Partial BBA (2b,9b) |r| computed via interpolation onto common K=20 fractional-depth grid; |r| is sensitive to grid choice but coarse-grain features (overall structural similarity) should be stable across K=10..30.',
        'Pre-registered hypotheses HMK-A/B/HQS-C are TIGHTLY COUPLED to the 3-cell scale curve. NO partial evaluation is admissible per pre-register thresholds — partial_pairwise is reported for diagnostic value only, NOT as a hypothesis verdict.',
        'Task spec explicitly instructed "Do not retry on second OOM" — this verdict honors that constraint. A 3rd attempt would require either int8 fallback (different code path, may avoid the platform fault) or persistent-volume cache (different infra).',
    ],
    'result_files': {
        'this_verdict': 'state/v11_gemma_familyinternal/verdict_retry_v2.json',
        'parent_verdict': 'state/v11_gemma_familyinternal/verdict.json',
        'wrapper_attempt1_log': 'state/v11_gemma_familyinternal/gemma_27b_retry_v2/wrapper_attempt1.log',
        'dispatch_log': 'state/v11_gemma_familyinternal/gemma_27b_retry_v2/dispatch.log',
        'pod_smoke_log': 'state/v11_gemma_familyinternal/gemma_27b_retry_v2/pod_smoke.log',
        'pod_id_txt': 'state/v11_gemma_familyinternal/gemma_27b_retry_v2/pod_id.txt',
        'reused_2b_cell': 'state/v11_cmt_v3_5bb_retest/out_pod/cmt_v3_gemma_2_2b.json',
        'reused_9b_cell': 'state/v11_cmt_v3_5bb_retest/out_pod_phase2/cmt_v3_gemma_2_9b.json',
        'wrapper_transient': '/tmp/gemma_27b_retry_v2_wrapper.py (raw#37 transient — NOT in git)',
    },
    'next_cycle_recommendations': [
        '(highest) Try int8 fallback: bitsandbytes load_in_8bit=True. Different code path may avoid the platform fault that killed retry v1+v2 at ~75pct safetensors fetch.',
        '(high) Use runpod NETWORK VOLUME for persistent /workspace/.hf_cache so 80+ GB cache survives pod death; only pay download cost once.',
        '(high) Pre-stage cache via huggingface-cli with --max-workers 1 (single-threaded, more robust); separate download from load to bisect platform fault.',
        '(medium) Investigate Llama family-internal as alternative 2nd clean evidence (depends on task #6 HF unblock).',
        '(low) Try gemma-2-9b/27b on different runpod image (e.g. pytorch:2.5.0 or 2.8.0).',
    ],
    'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
}

OUT_PATH = '/Users/ghost/core/anima/state/v11_gemma_familyinternal/verdict_retry_v2.json'
with open(OUT_PATH, 'w') as f:
    json.dump(out, f, indent=2)
print(json.dumps(out, indent=2))
print(f"\n[verdict] wrote -> {OUT_PATH}")
print(f"\n[partial BBA |r| 2b vs 9b] r={pair_2b_9b['r']:.4f} |r|={pair_2b_9b['abs_r']:.4f} per_fam={pair_2b_9b['per_family_r']}")
