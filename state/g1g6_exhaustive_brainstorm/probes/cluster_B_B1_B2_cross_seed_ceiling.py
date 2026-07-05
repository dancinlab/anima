#!/usr/bin/env python3
"""Cluster B - B1/B2 $0 cross-seed set-selection CEILING probe (numpy only, no model)."""
import json, os, re, glob
import numpy as np

D = '/Users/mini/dancinlab/anima/state/g6_bind_gate/decode_terminal/engine_native_frame_out'
RECS = []
for f in sorted(glob.glob(os.path.join(D, '*.out'))):
    m = re.search(r'arm=(\w+)\s+seed=(\d+)\s+frame=(\d+)\s+a=(\d+)\s+b=(\d+)\s+kwr=([\d.]+)\s+fb=(\d+)', open(f).read())
    if m:
        RECS.append({'arm': m.group(1), 'seed': int(m.group(2)), 'frame': int(m.group(3)),
                     'a': int(m.group(4)), 'b': int(m.group(5)), 'kwr': float(m.group(6)), 'fb': int(m.group(7))})
SEEDS = [7, 4302, 4303]
TAR = [r for r in RECS if r['arm'] == 'targeted']
print('=' * 70); print('CLUSTER B - B1/B2 cross-seed set-selection CEILING probe ($0 numpy)'); print('=' * 70)

# Q3 overlap control
print('\n[Q3] concept-pair schedule per seed (overlap control):')
for s in SEEDS:
    pairs = [(r['a'], r['b']) for r in sorted([x for x in TAR if x['seed'] == s], key=lambda x: x['frame'])]
    print(f'  seed {s}: pairs={pairs}')
psets = [set((r['a'], r['b']) for r in TAR if r['seed'] == s) for s in SEEDS]
overlap = psets[0] & psets[1] & psets[2]
print(f'  3-seed pair intersection size={len(overlap)} => FIXED pair schedule; variance = decode-trajectory only.')

# Q1 capacity floor
print('\n[Q1] per concept-pair fb across the 3-seed union (CAPACITY floor):')
pair_max = {}
for r in TAR:
    p = (r['a'], r['b']); pair_max[p] = max(pair_max.get(p, 0), r['fb'])
for p in sorted(pair_max):
    per_seed = [next((r['fb'] for r in TAR if r['seed'] == s and (r['a'], r['b']) == p), 0) for s in SEEDS]
    print(f'  pair {p}: per-seed fb={per_seed}  max={pair_max[p]}')
n_pairs_ever_pass = sum(1 for v in pair_max.values() if v >= 1)
print(f'  => {n_pairs_ever_pass}/{len(pair_max)} concept-pairs have >=1 seed with fb=1')
Q1_PASS = n_pairs_ever_pass >= 4
print(f'  Q1 CAPACITY-FLOOR test (>=4 pairs ever pass): {"MET" if Q1_PASS else "NOT-MET"}')

# Q2 greedy marginal-gain 6-set over 18-candidate union
print('\n[Q2] greedy marginal-gain 6-set over 18-candidate union (B1/B2 at pair res):')
union = list(TAR); chosen = []; seen_pairs = set(); remaining = list(union)
for _ in range(6):
    best = None; best_score = -1
    for r in remaining:
        novelty = 1 if (r['a'], r['b']) not in seen_pairs else 0
        score = r['fb'] * 2 + novelty + r['kwr']
        if score > best_score: best_score = score; best = r
    chosen.append(best); seen_pairs.add((best['a'], best['b'])); remaining.remove(best)
set_fb = sum(r['fb'] for r in chosen)
print(f'  chosen 6: fb_sum={set_fb}, source_seeds={[r["seed"] for r in chosen]}')
print(f'  Q2 SET-CEILING (union best-6 fb_sum >= 4): {"MET" if set_fb >= 4 else "NOT-MET"} (={set_fb})')

# within-seed plausibility
print('\n[B1 within-seed plausibility] cross-seed per-pair pass-rate (optimistic ceiling):')
rate = {p: float(np.mean([next((r['fb'] for r in TAR if r['seed'] == s and (r['a'], r['b']) == p), 0) for s in SEEDS])) for p in pair_max}
for p in sorted(rate): print(f'  pair {p}: cross-seed pass-rate = {rate[p]:.2f}')
exp_per_seed = sum(rate.values())
print(f'  => expected fb per (hypothetical diverse) seed = {exp_per_seed:.2f}  (frozen bar = 4)')

print('\n' + '=' * 70); print('VERDICT'); print('=' * 70)
if Q1_PASS and n_pairs_ever_pass == 6:
    verdict = 'GREEN-toward-GPU (search-wall plausible; B1 GPU fire warranted)'
    print('CAPACITY-FLOOR: ALL 6 concept-pairs can be bound by the model on some seed.')
    print('  => per-seed 3/6 shortfall consistent with SEARCH/trajectory wall, NOT capacity.')
    print('  => B1 (set-wise selection over within-seed K-pool) DIRECTIONALLY motivated.')
elif Q1_PASS:
    verdict = 'WALL-partial (search lever helps subset only)'
    print(f'CAPACITY-FLOOR PARTIAL: {n_pairs_ever_pass}/6 pairs ever pass.')
else:
    verdict = 'WALL (capacity floor; B1 GPU fire NOT warranted)'
    print(f'CAPACITY-FLOOR: only {n_pairs_ever_pass}/6 pairs ever pass. Do NOT fire B1.')
print(f'\nfinal: {verdict}')
print('scope: DIRECTIONAL $0 proxy (cross-seed leaks per-seed independence; not terminal).')
out = {'probe': 'cluster_B B1/B2 cross-seed set-selection CEILING ($0 numpy)',
       'pairs_ever_pass': n_pairs_ever_pass, 'pairs_total': len(pair_max),
       'per_pair_max_fb': {str(p): v for p, v in pair_max.items()},
       'union_best6_fb': set_fb, 'expected_fb_diverse_seed': exp_per_seed,
       'frozen_bar': '>=4/6 on >=2/3 seeds (per-seed independence)',
       'verdict': verdict,
       'scope': 'DIRECTIONAL (cross-seed union leaks per-seed independence; not terminal)',
       'caveat': 'stored data has K=1/frame + no candidate texts => within-seed-K + Jaccard need GPU'}
json.dump(out, open('/Users/mini/dancinlab/anima/state/g1g6_exhaustive_brainstorm/probes/cluster_B_B1_B2_result.json', 'w'), indent=2)
print('wrote state/g1g6_exhaustive_brainstorm/probes/cluster_B_B1_B2_result.json')
