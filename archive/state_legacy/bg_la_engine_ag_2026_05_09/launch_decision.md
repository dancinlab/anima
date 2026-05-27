# BG-LA Engine A/G H100 Actual Fire Decision Log
date: 2026-05-09
agent_session: opus-4-7-1m (continuation of aa74ac73594b3c4ff)
override: "all bg go" (verbatim)

## Pod
- pod_id: 4wxx2wvcvgjp88
- slug: h100-runpod-4wxx2wvcvgjp88-1778300273
- name: bg-la-engine-ag-1778300268-pid36566 (unique tag — concurrency mitigated)
- gpu: H100 80GB SXM
- ssh: 87.120.211.205:10025
- provisioned: 2026-05-09T04:18:51Z
- rate: $2.99/hr

## Train
- preset: la_350m (Engine A/G dual-engine 298,764,288 params)
- corpus: anima_persona_tier_a_v4 (231MB, downloaded from HF dancinlab/anima-persona-tier-a-v4)
- script: anima_la_train.py (adapted from BG-LB pod_main; STEPS=12000, BATCH=8, GRAD_ACCUM=16, LR=3e-4, WARMUP=1500)
- launched: 2026-05-09T05:21:59Z
- estimated wall: ~9.3hr (12000 steps × 2.8s/step from initial sample)
- estimated cost: ~$28 (within $30 hard cap)

## Critical findings
1. tool/transient_py/anima_clm_la_h100.py is SPEC STUB (NotImplementedError).
   Adapted BG-LB's full pod_main implementation (anima_clm_lb_h100.py) which
   already supports both 'lb_350m_pretrain' AND 'la_350m' presets via
   EngineAGConfig.la_350m factory. Wrote /tmp/anima_la_train.py with reduced
   STEPS=12000 (vs LB's 30000) to fit $30 budget.
2. SCP throughput from Mac→pod was ~3KB/s (60min for 7MB of 68MB gz);
   killed and switched to HF download (231MB in 6.2s @ 39MB/s on pod).
3. Orchestrator hexa file had explicit `main()` call breaking hexa-strict
   auto-invoke; fixed (single-line removal).

## Initial training signal
- step 0: loss=10.5391
- step 50: loss=8.9727 (after 140s, lr=1.04e-05 in warmup)
- ✓ Loss decreasing, training viable.
