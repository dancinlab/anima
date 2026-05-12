#!/bin/bash
# state/anima_v5mitosis_cotrain_2026_05_12/finalize_on_result.sh
#
# Run this AFTER cotrain_result.json is pulled to local.
# Prints summary + suggested edits for:
#   - docs/anima_clm_v5_mitosis_cond5_cotrain_2026_05_12.md (TODO[FILL_ON_RESULT])
#   - GOAL.md cond #3 D3 status transition
#   - PSCC §44 append entry
#   - memory project_v5_mitosis_cond5_cotrain_2026_05_12.md status field
#
# usage: bash finalize_on_result.sh

set -euo pipefail

RESULT_JSON="/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_2026_05_12/cotrain_result.json"

if [ ! -f "$RESULT_JSON" ]; then
    echo "ERROR: result.json not found at $RESULT_JSON"
    echo "  This script must be run AFTER cotrain_result.json is pulled (Phase 8 of dispatch)."
    exit 1
fi

echo "=== cotrain result summary ==="
python3 -c "
import json
with open('$RESULT_JSON') as f:
    d = json.load(f)

t = d.get('training', {})
fa = d.get('falsifier_aggregate', {})
fs = d.get('falsifiers', {})
p4 = d.get('f_persona_4_remeasure', {})
cfg = d.get('config', {})

print('== Training ==')
print(f\"  wall (hr):            {t.get('wall_hours',0):.2f}\")
print(f\"  cost (\\$):             {t.get('cost_usd_actual',0):.2f}\")
print(f\"  cap (\\$):              {t.get('cost_cap_usd',0):.2f}\")
print(f\"  cost_aborted:         {t.get('cost_aborted')}\")
print(f\"  steps actual:         {t.get('steps_actual')}/{t.get('steps_planned')}\")
print(f\"  n_cells_final:        {t.get('n_cells_final')}\")
print(f\"  splits total:         {t.get('splits')}\")
print(f\"  merges total:         {t.get('merges')}\")
print(f\"  n_params_final:       {t.get('n_params_final'):,}\")
print(f\"  loss initial avg100:  {t.get('loss_initial_avg100'):.4f}\")
print(f\"  loss final avg100:    {t.get('loss_final_avg100'):.4f}\")
print(f\"  loss delta:           {t.get('loss_delta'):.4f}\")
print(f\"  phi best:             {t.get('phi_best',0):.4f}\")
print(f\"  phi final:            {t.get('phi_final',0):.4f}\")

print('\\n== Falsifiers ==')
for fid in ['F-V5MIT-1','F-V5MIT-2','F-V5MIT-3','F-V5MIT-4','F-V5MIT-5']:
    f = fs.get(fid, {})
    p = f.get('passed')
    verdict = 'PASS' if p else 'FAIL'
    print(f\"  {fid}: {verdict}\")
    for k, v in f.items():
        if k not in ('test', 'passed', 'details'):
            print(f\"      {k}: {v}\")

print(f\"\\n  aggregate: {fa.get('n_pass')}/{fa.get('n_total')} {fa.get('verdict')}\")

print('\\n== F-PERSONA-4 cotrained-pool re-measure ==')
print(f\"  verdict:    {p4.get('verdict')}\")
print(f\"  mean_kl:    {p4.get('mean_kl',0):.6f} nats\")
print(f\"  threshold:  {p4.get('threshold',0.5)}\")
print(f\"  n_pairs:    {p4.get('n_pairs')}\")
print(f\"  categories: {p4.get('categories')}\")
mat = p4.get('kl_matrix') or []
print(f\"  kl_matrix:\")
for r, row in enumerate(mat):
    print(f\"    [{r}] {row}\")

print('\\n== D3 cond #3 status transition ==')
strong_to_done = p4.get('verdict') == 'PASS'
print(f\"  cheap-path baseline (PSCC §42): STRONG 4/5 (F-PERSONA-4 FAIL @ untrained)\")
print(f\"  cotrained-pool result:           F-PERSONA-4 {p4.get('verdict')}\")
print(f\"  D3 transition:                   STRONG → {'☑ DONE 5/5' if strong_to_done else '☑ STRONG 4/5 carry'}\")

print('\\n== v5-mitosis lane verdict ==')
f5_pass = fs.get('F-V5MIT-5', {}).get('passed', False)
print(f\"  F-V5MIT-5 V14-STRICT: {'PASS — v5-anima toy substrate 한계 극복' if f5_pass else 'FAIL — substrate-coupled emergence 부재 carry'}\")
print(f\"  lane closure ready:   {'YES (cond.5 met)' if f5_pass else 'NO (cond.5 unmet, alternative granularity ablation 필요)'}\")
"
