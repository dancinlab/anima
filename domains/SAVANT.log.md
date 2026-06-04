# SAVANT (torch-cuda lane) — step log (append-only)

## 2026-06-04 — bootstrap (torch-cuda reference lane)

- Located the PROVEN recipe: `clm_ref_pytorch_cuda_7b.py` (the descent-PASS /
  util-GREEN 7.25B rung of the `clm-v1-ref-pytorch-cuda` ladder). Reused VERBATIM
  as `SAVANT-torch/savant_train_torch_cuda.py` (+ durability ckpting only).
- Wrote `SAVANT-torch/build_corpus_5lang_euro.py` (en·fr·de·es·ru wikipedia,
  CC-BY-SA, byte stream) + `pod_setup.sh`.
- Created `domains/SAVANT.md` (torch-cuda lane) — distinct from `SAVANT-7B.md`
  (forge lane, concurrent agent) per a_lane_akida_gpu_split.
