# SAVANT (torch-cuda lane) — step log (append-only)

## 2026-06-04 — bootstrap (torch-cuda reference lane)

- Located the PROVEN recipe: `clm_ref_pytorch_cuda_7b.py` (the descent-PASS /
  util-GREEN 7.25B rung of the `clm-v1-ref-pytorch-cuda` ladder). Reused VERBATIM
  as `SAVANT-torch/savant_train_torch_cuda.py` (+ durability ckpting only).
- Wrote `SAVANT-torch/build_corpus_5lang_euro.py` (en·fr·de·es·ru wikipedia,
  CC-BY-SA, byte stream) + `pod_setup.sh`.
- Created `domains/SAVANT.md` (torch-cuda lane) — distinct from `SAVANT-7B.md`
  (forge lane, concurrent agent) per a_lane_akida_gpu_split.

## 2026-06-04 — LAUNCH (single leak-safe pod 39416669)

- Rented EXACTLY ONE pod: vast `39416669` H100 SXM 80GB, 120 GB disk,
  `pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel`, ~$2.40/hr. Single rent, NO
  re-rent / NO escalation / NO rotation (hexa-lang #2686 no-autorent policy).
  Verified exactly 1 SAVANT-labeled pod alive (no orphans).
- Wrote `SAVANT-torch/pod_onramp.sh` — single-pod sequence (deps → rung0 corpus
  → rung0 train → IF descend: 7B corpus → 7B durable nohup). FAIL-LOUD on
  rung0 no-descent.
- scp'd 3 scripts to `/workspace/savant/`, launched onramp DETACHED
  (`setsid nohup`, survives orchestrator death).
- rung0 (d512/8L, 120 steps, 5-lang ~20 MB corpus) DESCENT CONFIRMED:
  val_ce step0=5.63565 → step20=3.27207, ~155K tok/s. Recipe + corpus + ckpt
  pipeline PROVEN leak-free, clean descent.
- 7B (d4096/36L/32H/block512 = 7.25B) launched DURABLY on the same pod
  (--ckpt-every 200 under /workspace, --resume-able). EXIT after launch — NOT
  babysat. Harvest plan + ETA recorded in SAVANT.md.
