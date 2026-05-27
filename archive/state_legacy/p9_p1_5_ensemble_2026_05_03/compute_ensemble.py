"""P9 P1.5 ensemble cv compute (s42, s43, s44, [s45]) — also B ensemble comparison.

Inputs (local paths; v2 per_prompt files):
  P1.5 s42: state/p9_p1_holdout500_reeval_2026_05_03/v2_per_prompt/phase1_5_per_prompt.json
  P1.5 s43/s44: state/p9_p1_5_ensemble_2026_05_03/{phase1_5_seed43,phase1_5_seed44}_per_prompt.json
  P1.5 s45: optional (only if seed45 finalized + reeval'd)

  B s42: state/p9_p1_holdout500_reeval_2026_05_03/v2_per_prompt/ablation_B_per_prompt.json
  B s43/s44/s45: state/p9_p1_holdout500_reeval_2026_05_03/v2_per_prompt/ablation_B_seed{43,44,45}_per_prompt.json

Outputs:
  state/p9_p1_5_ensemble_2026_05_03/per_seed_results.json
  state/p9_p1_5_ensemble_2026_05_03/verdict_4seed.json
  state/p9_p1_5_ensemble_2026_05_03/comparison_vs_b_ensemble.json
"""
import json, os, sys, math
from datetime import datetime, timezone

ROOT = '/Users/ghost/core/anima'
V2_DIR = f'{ROOT}/state/p9_p1_holdout500_reeval_2026_05_03/v2_per_prompt'
OUT_DIR = f'{ROOT}/state/p9_p1_5_ensemble_2026_05_03'

P15_SOURCES = {
    'phase1_5_seed42': f'{V2_DIR}/phase1_5_per_prompt.json',
    'phase1_5_seed43': f'{OUT_DIR}/phase1_5_seed43_per_prompt.json',
    'phase1_5_seed44': f'{OUT_DIR}/phase1_5_seed44_per_prompt.json',
    'phase1_5_seed45': f'{OUT_DIR}/phase1_5_seed45_per_prompt.json',
}

B_SOURCES = {
    'ablation_B_seed42': f'{V2_DIR}/ablation_B_per_prompt.json',
    'ablation_B_seed43': f'{V2_DIR}/ablation_B_seed43_per_prompt.json',
    'ablation_B_seed44': f'{V2_DIR}/ablation_B_seed44_per_prompt.json',
    'ablation_B_seed45': f'{V2_DIR}/ablation_B_seed45_per_prompt.json',
}

ABLATION_A = f'{V2_DIR}/ablation_A_per_prompt.json'

METRICS = ['bleu_1', 'rouge_l', 'chrf']
CV_THRESHOLD = 0.30  # cv < 0.30 = real lift, >= 0.30 = seed luck


def load_summary(path):
    if not os.path.isfile(path):
        return None
    with open(path) as f:
        d = json.load(f)
    return d.get('summary', d)


def cv(values):
    if not values:
        return None
    n = len(values)
    mean = sum(values) / n
    if mean == 0:
        return float('inf') if any(v != 0 for v in values) else 0.0
    var = sum((v - mean) ** 2 for v in values) / max(1, n - 1)
    std = math.sqrt(var)
    return std / mean


def ensemble_stats(per_seed_means_by_metric):
    """per_seed_means_by_metric: {metric: [val_seed1, val_seed2, ...]} -> {metric: {mean,std,cv}}"""
    out = {}
    for m, vals in per_seed_means_by_metric.items():
        n = len(vals)
        mean = sum(vals) / n if n else 0.0
        var = sum((v - mean) ** 2 for v in vals) / max(1, n - 1) if n > 1 else 0.0
        std = math.sqrt(var)
        out[m] = {
            'n_seeds': n,
            'values': vals,
            'mean': mean,
            'std': std,
            'cv': (std / mean) if mean != 0 else (float('inf') if any(v != 0 for v in vals) else 0.0),
        }
    return out


def collect(sources):
    """Return {seed_name: {metric: mean}} dict for available seeds only."""
    per_seed = {}
    for name, path in sources.items():
        s = load_summary(path)
        if s is None:
            print(f'  [skip] {name}: missing {path}', file=sys.stderr)
            continue
        if 'mean' not in s:
            print(f'  [skip] {name}: no mean in summary', file=sys.stderr)
            continue
        per_seed[name] = {m: s['mean'].get(m, 0.0) for m in METRICS}
    return per_seed


def verdict_from_cv(stats):
    cv_bleu = stats['bleu_1']['cv']
    cv_rouge = stats['rouge_l']['cv']
    cv_chrf = stats['chrf']['cv']
    bleu_real = cv_bleu < CV_THRESHOLD
    rouge_real = cv_rouge < CV_THRESHOLD
    chrf_real = cv_chrf < CV_THRESHOLD
    if bleu_real and rouge_real:
        v = 'PHASE_1_5_REAL_LIFT'
    elif chrf_real and not (bleu_real or rouge_real):
        v = 'PHASE_1_5_PARTIAL'
    else:
        v = 'PHASE_1_5_SEED_LUCK'
    return {
        'verdict': v,
        'cv_threshold': CV_THRESHOLD,
        'cv_bleu_1': cv_bleu,
        'cv_rouge_l': cv_rouge,
        'cv_chrf': cv_chrf,
        'bleu_real_lift': bleu_real,
        'rouge_real_lift': rouge_real,
        'chrf_real_lift': chrf_real,
    }


def main():
    print('=== P1.5 ensemble (s42/s43/s44/[s45]) ===')
    p15 = collect(P15_SOURCES)
    print(f'  P1.5 seeds available: {list(p15.keys())}')

    print('=== B ensemble (s42/s43/s44/s45) ===')
    bens = collect(B_SOURCES)
    print(f'  B seeds available: {list(bens.keys())}')

    # Ablation A (single seed) for context
    a_summary = load_summary(ABLATION_A)
    a_means = {m: a_summary['mean'].get(m, 0.0) for m in METRICS} if a_summary else None

    # Build per-metric arrays (ordered)
    def to_arr(per_seed_dict):
        return {m: [per_seed_dict[s][m] for s in sorted(per_seed_dict.keys())] for m in METRICS}

    p15_arr = to_arr(p15)
    p15_stats = ensemble_stats(p15_arr)
    p15_verdict = verdict_from_cv(p15_stats)

    bens_arr = to_arr(bens)
    bens_stats = ensemble_stats(bens_arr)
    # B verdict: same labels but for B
    bens_verdict_label = (
        'B_REAL_LIFT' if bens_stats['bleu_1']['cv'] < CV_THRESHOLD and bens_stats['rouge_l']['cv'] < CV_THRESHOLD
        else ('B_PARTIAL' if bens_stats['chrf']['cv'] < CV_THRESHOLD else 'B_SEED_LUCK')
    )

    # Per-seed dump
    per_seed_out = {
        'schema': 'anima/p9/p1_5_ensemble/v1',
        'date_utc': datetime.now(timezone.utc).isoformat(),
        'metrics_set': METRICS,
        'ablation_A_baseline': a_means,
        'phase1_5_per_seed': p15,
        'ablation_B_per_seed': bens,
    }

    # Verdict dump
    verdict_out = {
        'schema': 'anima/p9/p1_5_ensemble/verdict/v1',
        'date_utc': datetime.now(timezone.utc).isoformat(),
        'cv_threshold': CV_THRESHOLD,
        'phase1_5': {
            'n_seeds': len(p15),
            'seeds': sorted(p15.keys()),
            'metric_stats': p15_stats,
            'verdict': p15_verdict['verdict'],
            'detail': p15_verdict,
        },
        'ablation_B': {
            'n_seeds': len(bens),
            'seeds': sorted(bens.keys()),
            'metric_stats': bens_stats,
            'verdict': bens_verdict_label,
        },
    }

    # Comparison vs B + interpretation
    p15_v = p15_verdict['verdict']
    b_v = bens_verdict_label
    if p15_v.endswith('SEED_LUCK') and b_v.endswith('SEED_LUCK'):
        signal = 'BOTH_NOISE_FLOOR'
        interp = (
            'Both P1.5 and B are at noise floor under multi-seed cv test. '
            'Confirms BLEU/ROUGE benchmark is incapable of resolving real lift at this scale; '
            'A\' switch decision (qualitative gates) is re-confirmed.'
        )
    elif p15_v == 'PHASE_1_5_REAL_LIFT' and b_v.endswith('SEED_LUCK'):
        signal = 'P1_5_ONLY_REAL'
        interp = (
            'P1.5 shows real (low-cv) lift while B is seed-luck noise. '
            'P1.5 is the only non-luck cell — the original lift claim survives multi-seed scrutiny.'
        )
    elif p15_v == 'PHASE_1_5_REAL_LIFT' and b_v.endswith('REAL_LIFT'):
        signal = 'BOTH_REAL'
        interp = 'Both P1.5 and B show stable lift across seeds; benchmark resolves at this level.'
    else:
        signal = 'MIXED'
        interp = f'Mixed: P1.5={p15_v}, B={b_v}.'

    comparison_out = {
        'schema': 'anima/p9/p1_5_ensemble/comparison/v1',
        'date_utc': datetime.now(timezone.utc).isoformat(),
        'signal': signal,
        'interpretation': interp,
        'phase1_5_verdict': p15_v,
        'ablation_B_verdict': b_v,
        'phase1_5_cv': {
            'bleu_1': p15_stats['bleu_1']['cv'],
            'rouge_l': p15_stats['rouge_l']['cv'],
            'chrf': p15_stats['chrf']['cv'],
        },
        'ablation_B_cv': {
            'bleu_1': bens_stats['bleu_1']['cv'],
            'rouge_l': bens_stats['rouge_l']['cv'],
            'chrf': bens_stats['chrf']['cv'],
        },
        'phase1_5_means': {m: p15_stats[m]['mean'] for m in METRICS},
        'ablation_B_means': {m: bens_stats[m]['mean'] for m in METRICS},
        'ablation_A_means': a_means,
        'ranked_means_bleu_1': sorted(
            [
                ('phase1_5_ensemble', p15_stats['bleu_1']['mean']),
                ('ablation_B_ensemble', bens_stats['bleu_1']['mean']),
                ('ablation_A_single', a_means['bleu_1'] if a_means else None),
            ],
            key=lambda kv: (kv[1] is None, -(kv[1] or 0)),
        ),
    }

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(f'{OUT_DIR}/per_seed_results.json', 'w') as f:
        json.dump(per_seed_out, f, indent=2)
    with open(f'{OUT_DIR}/verdict_4seed.json', 'w') as f:
        json.dump(verdict_out, f, indent=2)
    with open(f'{OUT_DIR}/comparison_vs_b_ensemble.json', 'w') as f:
        json.dump(comparison_out, f, indent=2)

    # Console summary
    print()
    print(f'P1.5 ensemble (n={len(p15)}):')
    for m in METRICS:
        s = p15_stats[m]
        print(f'  {m}: mean={s["mean"]:.6f}  std={s["std"]:.6f}  cv={s["cv"]:.4f}')
    print(f'  -> verdict: {p15_v}')
    print()
    print(f'B ensemble (n={len(bens)}):')
    for m in METRICS:
        s = bens_stats[m]
        print(f'  {m}: mean={s["mean"]:.6f}  std={s["std"]:.6f}  cv={s["cv"]:.4f}')
    print(f'  -> verdict: {b_v}')
    print()
    print(f'Signal: {signal}')
    print(f'Interp: {interp}')


if __name__ == '__main__':
    main()
