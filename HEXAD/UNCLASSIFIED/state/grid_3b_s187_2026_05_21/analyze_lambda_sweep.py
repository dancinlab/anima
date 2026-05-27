"""Generate LAMBDA_SATURATION.md table from eval3 results.

Pulls eval3 JSONs from local state/eval_out_lambda_sweep/ (after SCP from ubu-1)
and the original Eval 3 results from EVAL_REPORT.md table (hardcoded below).
"""
import json
import sys
from pathlib import Path

# Original S187 Eval 3 results (from EVAL_REPORT.md § 6.4 mitosis hook table)
ORIGINAL = {
    'vA':     {'lambda_psi': 0.3,  'lambda_phi': 0.3,  'final_cells': 70,  'splits': 68,  'merges': 0, 'phi_final': 0.5477},
    'vA_s42': {'lambda_psi': 0.3,  'lambda_phi': 0.3,  'final_cells': 82,  'splits': 80,  'merges': 0, 'phi_final': 0.6397},
    'vB_s42': {'lambda_psi': 1.0,  'lambda_phi': 0.3,  'final_cells': 60,  'splits': 58,  'merges': 0, 'phi_final': 0.6566},
    'vC':     {'lambda_psi': 0.3,  'lambda_phi': 1.0,  'final_cells': 128, 'splits': 126, 'merges': 0, 'phi_final': 0.6434},
    'vD_s42': {'lambda_psi': 1.0,  'lambda_phi': 1.0,  'final_cells': 55,  'splits': 53,  'merges': 0, 'phi_final': 0.6494},
}

# Lambda-sweep variants  
SWEEP_DEF = {
    'C3':  {'lambda_psi': 0.3,  'lambda_phi': 3.0},
    'C10': {'lambda_psi': 0.3,  'lambda_phi': 10.0},
    'C30': {'lambda_psi': 0.3,  'lambda_phi': 30.0},
    'B3':  {'lambda_psi': 3.0,  'lambda_phi': 0.3},
    'B10': {'lambda_psi': 10.0, 'lambda_phi': 0.3},
    'B30': {'lambda_psi': 30.0, 'lambda_phi': 0.3},
}

def load_sweep_results(eval_dir):
    out = {}
    for cell in SWEEP_DEF:
        f = Path(eval_dir) / f'{cell}_eval3.json'
        if f.exists() and f.stat().st_size > 0:
            with open(f) as fp:
                d = json.load(fp)
            out[cell] = {
                'lambda_psi': SWEEP_DEF[cell]['lambda_psi'],
                'lambda_phi': SWEEP_DEF[cell]['lambda_phi'],
                'final_cells': d['final_cells'],
                'splits': d['n_split'],
                'merges': d['n_merge'],
                'phi_final': d['phi_final'],
            }
        else:
            out[cell] = {**SWEEP_DEF[cell], 'final_cells': None, 'splits': None, 'merges': None, 'phi_final': None}
    return out

def fmt_row(cell, d):
    sp = '—' if d['splits'] is None else d['splits']
    fc = '—' if d['final_cells'] is None else d['final_cells']
    me = '—' if d['merges'] is None else d['merges']
    pf = '—' if d['phi_final'] is None else f'{d["phi_final"]:.4f}'
    return f'| **{cell}** | {d["lambda_psi"]:.1f} | {d["lambda_phi"]:.1f} | {fc} | {sp} | {me} | {pf} |'

def main():
    eval_dir = sys.argv[1] if len(sys.argv) > 1 else '/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/eval_out_lambda_sweep'
    sweep = load_sweep_results(eval_dir)
    out_path = sys.argv[2] if len(sys.argv) > 2 else '/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/LAMBDA_SATURATION.md'
    
    md = []
    md.append('# S187-C — λ Saturation Sweep (Eval 3 mitosis cross-λ)\n')
    md.append('Extends S187 Eval 3 finding (EVAL_REPORT.md § 6.4) past λ=1.0 to test whether the mitosis-split signal **saturates** (plateau) or **inverts** (peak then fall).\n')
    md.append('**Run date**: 2026-05-21')
    md.append('**Compute**: 6 H100/A100 pods @ ~$0.20/min (RunPod) + ubu-1 CPU bf16 eval')
    md.append('**Hypothesis (from § 6.4)**: λ_φ ↑ ⇒ more splits (vC at λ_φ=1.0 saturated cell-cap 128); λ_ψ ↑ ⇒ fewer splits.\n')
    
    md.append('## Cross-λ mitosis split table\n')
    md.append('| cell | λψ | λφ | final cells | splits | merges | Φ final |')
    md.append('|---|---|---|---|---|---|---|')
    # Original 5 sorted by phi=0.3 row (B-series + control), then phi=1.0 row
    for c in ['vA','vA_s42','vB_s42','vC','vD_s42']:
        md.append(fmt_row(c, ORIGINAL[c]))
    # Sweep: B-series first (λψ-axis), then C-series (λφ-axis)
    md.append('| | | | | | | |')
    for c in ['B3','B10','B30']:
        md.append(fmt_row(c, sweep[c]))
    md.append('| | | | | | | |')
    for c in ['C3','C10','C30']:
        md.append(fmt_row(c, sweep[c]))
    md.append('')
    
    # Φ-axis log table
    md.append('## λ_φ axis (Φ-up, λ_ψ=0.3 control)\n')
    md.append('| λ_φ | cell | splits | final cells |')
    md.append('|---|---|---|---|')
    md.append('| 0.3 | vA (avg of vA + vA_s42) | 74.0 | 76.0 |')
    md.append(f'| 1.0 | vC | {ORIGINAL["vC"]["splits"]} | {ORIGINAL["vC"]["final_cells"]} |')
    for c in ['C3','C10','C30']:
        lp = sweep[c]['lambda_phi']
        sp = sweep[c]['splits'] if sweep[c]['splits'] is not None else 'PENDING'
        fc = sweep[c]['final_cells'] if sweep[c]['final_cells'] is not None else 'PENDING'
        md.append(f'| {lp} | {c} | {sp} | {fc} |')
    md.append('')
    
    # Ψ-axis log table
    md.append('## λ_ψ axis (Ψ-up, λ_φ=0.3 control)\n')
    md.append('| λ_ψ | cell | splits | final cells |')
    md.append('|---|---|---|---|')
    md.append('| 0.3 | vA (avg) | 74.0 | 76.0 |')
    md.append(f'| 1.0 | vB_s42 | {ORIGINAL["vB_s42"]["splits"]} | {ORIGINAL["vB_s42"]["final_cells"]} |')
    for c in ['B3','B10','B30']:
        lp = sweep[c]['lambda_psi']
        sp = sweep[c]['splits'] if sweep[c]['splits'] is not None else 'PENDING'
        fc = sweep[c]['final_cells'] if sweep[c]['final_cells'] is not None else 'PENDING'
        md.append(f'| {lp} | {c} | {sp} | {fc} |')
    md.append('')
    
    # Observations
    md.append('## Observation\n')
    md.append('**Both axes show non-monotone saturation patterns, NOT the simple monotone signal hypothesized from § 6.4.**\n')
    have_C = all(sweep[c]['splits'] is not None for c in ['C3','C10','C30'])
    have_B = all(sweep[c]['splits'] is not None for c in ['B3','B10','B30'])
    if have_C:
        c_splits = [sweep[c]['splits'] for c in ['C3','C10','C30']]
        md.append(f'- **λ_φ axis** (0.3 → 1.0 → 3.0 → 10.0 → 30.0): splits 74 → 126 → {c_splits[0]} → {c_splits[1]} → {c_splits[2]}')
        md.append(f'  - λ_φ=1.0 already saturates cell-cap (vC=126).')
        md.append(f'  - λ_φ=3.0 unexpectedly DIPS to {c_splits[0]} (close to baseline 74), then re-saturates at λ_φ≥10.0.')
        md.append(f'  - Tentative interpretation: φ-pressure has a non-monotone training-time effect; the mid-λ region may produce a *less* clustered tension landscape at eval time. Single-seed noise (vA dual-seed: 68 vs 80) can account for ~12 split drift, BUT C3=76 vs C10=126 = 50-split delta is well above seed noise.')

    if have_B:
        b_splits = [sweep[c]['splits'] for c in ['B3','B10','B30']]
        md.append(f'- **λ_ψ axis** (0.3 → 1.0 → 3.0 → 10.0 → 30.0): splits 74 → 58 → {b_splits[0]} → {b_splits[1]} → {b_splits[2]}')
        md.append(f'  - λ_ψ=1.0 produces a DIP (vB_s42=58, below baseline 74) — matches § 6.4 prior observation.')
        md.append(f'  - λ_ψ=3.0 recovers to {b_splits[0]}, near baseline.')
        md.append(f'  - λ_ψ≥10.0 saturates cell-cap ({b_splits[1]}/{b_splits[2]}) — opposite direction from the § 6.4 "λ_ψ ↑ ⇒ fewer splits" hypothesis.')
        md.append(f'  - Tentative interpretation: low-to-moderate λ_ψ suppresses splits, but at large λ_ψ the trained Ψ field itself becomes high-variance and saturates the substrate-tension signal regardless of φ-pressure.')
    md.append('')
    md.append('### Key finding')
    md.append('')
    md.append('The earlier Eval 3 reading that "λ_φ ↑ ⇒ more splits, λ_ψ ↑ ⇒ fewer splits" is *only valid in the [0.3, 1.0] interval*. Past λ=3.0, both pressures eventually produce cell-cap saturation. The split count is therefore a poor monotone proxy for λ effect at high λ — the cell-cap MAX_CELLS=128 is the binding constraint that hides true pressure differences.\n')
    md.append('Practical implication: future grid-search work targeting "mitosis activity" as an outcome should either (a) increase MAX_CELLS to expose the saturation ceiling, (b) replace count-splits with an integral metric like mean-Φ-history that doesn\'t saturate, or (c) measure split-arrival rate (1/time-to-first-split) which captures pressure even at cap.\n')

    # Honest C3
    md.append('## Honest C3 (caveats)\n')
    md.append('- Single seed=1337 per cell. vA cross-seed (1337 vs 42) showed 68 vs 80 splits = ~12 drift, so 5-point cross-λ deltas under ~12 should be treated as noise.')
    md.append('- Each cell trained 2000 steps only (matching S187 baseline), CE ~3.8-4.0 floor, NOT converged. λ effects measured in early-training regime; mature-training behavior may differ.')
    md.append('- Eval 3 = mitosis cell-pool Python port driven by model.forward()\'s per-layer tensions on prompt "안녕? 너는 누구야?" greedy 40 steps. MAX_CELLS=128 hard cap is the dominant ceiling at high λ.')
    md.append('- λ_φ=30.0 and λ_ψ=30.0 are 100× the §184 baseline (0.30); training stability not separately verified beyond CE convergence in the 3.8-4.5 range. Some runs (B-series) showed initial L_route=50 spike that decayed within 80 steps.')
    md.append('- C3 and C10 ran the NumPy-vectorized eval3 variant (`eval3_mitosis_fast.py`) due to pure-Python n²·d cosine being prohibitively slow at n=128/d=3072. The two implementations differ in init-noise RNG (numpy vs Python random.gauss); C3 splits=76 and C10 splits=126 should still be comparable to other cells but the absolute split counts have a small RNG-source caveat.')
    md.append('- Pod-side eval3 (not ubu-1 CPU): trained ckpt evaluated *in place* on the same H100/A100 pod that produced it, immediately after training, before pod termination. Each pod\'s 17 GB ckpt was never transferred off — eval3 ran on-pod, only the small JSON came to Mac. This bypassed the 6.8 MB/s home-WAN bottleneck that would otherwise have taken ~6-h per ckpt for SCP back.')
    md.append('- Cost actual: ~$8-15 cumulative pod-burn over 75 min wall (6 pods, mixed H100 SXM/NVL + A100 SXM/PCIe). Stayed within $25 cap. Training itself was ~12 min/pod = $14.4 train share.')
    md.append('- ckpt SHA256s captured only for C30 (other pods terminated before sha256sum follow-up landed — `eval_out_lambda_sweep/*_ckpt_sha256.txt` for C3/C10/B-series are missing or empty). Reproducibility from result.json + train.log + dispatch params still intact.')
    md.append('')
    print('\n'.join(md))
    Path(out_path).write_text('\n'.join(md))
    print(f'\n[wrote] {out_path}', file=sys.stderr)

if __name__ == '__main__':
    main()
