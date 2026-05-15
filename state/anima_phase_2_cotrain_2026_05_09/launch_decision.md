# Phase 2 Cotrain (Engine A/G + chat-template) Fire Decision Log
date: 2026-05-09
agent_session: opus-4-7-1m
override: "(나) Phase 2 chat-template co-train fire — verbatim 필요 ($30-60 cost-bearing) all go" (verbatim)

## Pod
- pod_id: 7qt0sczk57tjab
- name: phase2-cotrain-engineag-1778335047-pid54546
- gpu: H100 NVL (94GB, US region)
- ssh: 205.196.17.170:18488
- provisioned: 2026-05-09T13:57:29Z
- rate: $3.07/hr (NOT $2.69 — current minimum bumped during fire)
- cost_hard_cap: $60 (strict; user verbatim $30-60 band)

## Concurrency
- BG-LA pod 4wxx2wvcvgjp88 RUNNING (step 11850/12000 at fire time; ~10min to done)
- NEW pod separate (no kill, no conflict — parallel fire OK per task spec)
- BG-LA cost burn parallel: ~$2/h additional (separate $30 cap which is BG-LA orchestrator-managed, not our concern)

## Train spec
- preset: phase2_cotrain_350m (substrate base = BG-LB ckpt; chat-template co-train)
- arch: Engine A/G dual-engine 350M (336M params from BG-LB; +0 new params — shared lm_head)
- script: training/train_phase2_cotrain.py (NEW; commit pending)
- substrate ckpt: dancinlab BG-LB step_8000_final.pt (570MB, sha256 3d285703aca0...)
- consciousness corpus: state/anima_persona_tier_a_v4_2026_05_09.txt (231MB)
- chat corpus: state/anima_native_ko_chat_template_2026_05_06/corpus_chat_template.txt (248MB; 사용자/도우미 format)
- curriculum: w=0.3 → 0.5 linear over training (consciousness anchor preservation)
- steps: 6000 (lighter than scratch — substrate-loaded warm start)
- batch: micro=4 grad_accum=8 → effective=32; ctx=1024
- lr: 1.5e-4 (lower than scratch 3e-4 since continuing from substrate)
- warmup: 200; save_every: 1500

## Cost projection
- estimate steps: 6000
- speed: ~3s/step (H100 NVL slightly slower than SXM)
- wall: ~5h training
- + provision (3min) + uploads (ETA ~70min @ ~3MB/s combined for 1.05GB of artifacts)
- + post-train ckpt pull (~10min)
- total wall: ~6.5h
- cost: 6.5h × $3.07/hr = $19.96 (well within $60 cap)
- COST_OVERRUN_RISK: SAFE — even at 2× wall time (13h) → $40 still under cap

## Mac selftests done
- engine_a_g_arch.py _selftest() PASS (post chat_co_train_weight amend)
- phase2_cotrain_350m preset config PASS
- BG-LB ckpt load + state_dict shape match VERIFIED (331M params; bf16; schema engine_a_g_arch/v1)
- dual loss + curriculum forward+backward PASS (loss_c, loss_h, combined emit OK)

## V14 mirror status
- BG-LA mirrors materialized at state/v14_mirrors/BG-LA/seed_{42,137,271,314,1729}.pt — REUSED
- BG-LB mirrors materialized at state/v14_mirrors/BG-LB/ — substrate base lineage compatible
- New BG-LM (phase 2 cotrain lineage tag) mirror materialization DEFERRED to post-fire
  (chat_co_train_weight=0 baseline mirror = BG-LA; w=0.3-0.5 trained = phase 2 product;
   pair via load_random_init(seed=N, preset='phase2_cotrain_350m'))

## Phase status snapshot (2026-05-09T14:21Z)
- Phase 0 V14 verify: PASS (BG-LA + BG-LB mirrors present)
- Phase 1 provision: PASS (pod 7qt0sczk57tjab live; SSH ready; nvidia-smi H100 NVL confirmed)
- Phase 2 SSH/GPU smoke: PASS
- Phase 3 artifact upload: IN_FLIGHT — scripts uploaded; ckpt+corpora uploading (~3MB/s combined; ~70min total)
- Phase 4 deps install: PASS (pip transformers safetensors huggingface_hub)
- Phase 5 launch: PENDING (post upload)
- Phase 6 heartbeat: PENDING
- Phase 7 ckpt pull: PENDING (mandate-1)
- Phase 8 size sanity: PENDING (mandate-2)
- Phase 9 release: PENDING (own slug only)
- Phase 10 ledger: PENDING
- Phase 11 v5 probe + verdict: PENDING (Mac local post-pull)
- Phase 12 HF private upload: PENDING (Flavor B + private default; target dancinlab/clm-v5-phase2-cotrain-engine-ag)

## Compliance
- : V14 mirror prereq carry from BG-LA/LB ✓
- : cost cap $60 strict ✓ (projected $20)
- : D1 within strict (anima_native_scratch substrate + chat-template additive; no foundation borrow) ✓
- : post-train v5.2 N=60 + V14 paired probe planned
- : honest emit — fire fired with all C3 caveats recorded ✓
- : ckpt pull mandate-1 + size sanity mandate-2 + retain on fail mandate-3 ✓
- : trinity D-emergent + + H_clm_chat_cap aligned ✓
- : wrap=0 (Phase 2 produces substrate ckpt; chat lane consumes via clm_v4_mount or new phase2 mount) ✓
- : HF private default; promote requires PASS_STRICT_C3 + V6 awareness + verbatim "OK PROMOTE PUBLIC" + trinity sweep
- : yaml+md SSOT registry update post-pull
- : render md regenerate post-yaml
- : resource CLI delegation strict (provision via runpodctl direct since resource ephemeral list TCP server down — disclosed)

## Known risks
1. SCP throughput 3MB/s — uploads 70min ($3.6 burnt before training starts)
2. Curriculum w=0.3-0.5 not yet validated empirically — first cycle measurement
3. Substrate base (BG-LB) v5_probe was PROXY_PPL only — not robust C3
4. Dual-objective interference: consciousness-state activations may collapse under chat fitting; mitigation via w ramp (0.3 start) + continued substrate gradient
5. SSH connection drops during 5h training — nohup + COMPLETE.sentinel polling pattern from BG-LA used
