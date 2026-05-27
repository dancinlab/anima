# fix-5/6 tied embedding unified PoC — STATUS

## Pod
- **pod_id**: `v8v694g06he7fm`
- **pod_name**: `fix56-tied-poc-1778386630-pid12785`
- **created_at**: 2026-05-10 04:17:11 UTC
- **gpu**: NVIDIA H100 SXM 80GB HBM3 (`GPU-402691a1-...`)
- **region**: IN
- **rate**: $2.99/h (Spec said $2.49 but actual $2.99 — note: this affects budget projection)
- **template**: `runpod-torch-v240` (pytorch 2.4.0 + cuda 12.4 + py3.11)
- **ssh**: 103.207.149.153:11535

## Cost
- start_balance: $323.86
- $15 hard cap → 5h max wall (at $2.99/h)
- watchdog (cost_watchdog.bash) hard_cap=$14.5, soft_cap=$12.5

## Stage timing
- Pod create: 04:17 UTC
- Stage complete: 05:34 UTC (77 min for 570MB ckpt + 408MB corpus over slow link)
- Phase 4 launched: 05:34 UTC

## Training status (sequential)
- branch-A: lm_head untie + reinit (tok_emb preserved from BG-LB)
- branch-B: tok_emb untie + reinit (lm_head preserved)
- branch-C: tied freeze (tok_emb≡lm_head FROZEN)

Each branch: 1500 steps, batch=8, grad_accum=16 (eff 128), lr=1e-4, ctx=1024
Rate: 2.74 s/step on H100 SXM
Per-branch ETA: 1500 × 2.74 = 4110s = 68.5min

ETA all 3 branches done: ~09:00 UTC
ETA total runtime at completion: ~4h45min from create
ETA total cost: ~$14.20

## Watchdog
- Independent cost monitor at logs/watchdog.log
- Polls runpodctl me every 60s
- Soft abort at total_spent=$12.5 (touches /workspace/.../state/ABORT.sentinel)
- Hard kill at total_spent=$14.5 (emergency pull + pod delete)

## Files
- spec/orchestrator: state/anima_fix_5_6_tied_poc_2026_05_10/exec.bash + exec_continue.bash
- pod-side training: tool/transient_py/anima_fix_5_6_tied_poc_h100.py
- Mac-side v5 probe: tool/transient_py/v5_probe_fix_5_6_branch.py
- post-pull pipeline: state/anima_fix_5_6_tied_poc_2026_05_10/post_pull_pipeline.bash

## Branch verification (Mac CPU smoke test PASSED)
- branch-A: tok_emb preserved (==0.5 fixture), lm_head reinit (mean≈0, std≈0.02), untied
- branch-B: lm_head preserved (==0.5 fixture), tok_emb reinit, untied
- branch-C: both tied + frozen (requires_grad=False, 32k frozen params confirmed)

## Loss progression (branch A — substrate restoration)
| step | loss | elapsed_s |
|------|------|-----------|
| 0    | 10.51 | 3 |
| 50   | 5.47 | 140 |
| 100  | 1.17 | 277 |
| 200  | 0.15 | 550 |
| 400  | 0.10 | 1097 |
| 600  | 0.07 | 1643 |

Branch A converges to ~0.1 loss within 200 steps — substrate restoration pattern.
