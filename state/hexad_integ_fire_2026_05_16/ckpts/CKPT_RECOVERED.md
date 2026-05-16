# ckpt RECOVERED (R3 HEXAD integration fire — T1 deterministic refire, 2026-05-16)

**Supersedes `CKPT_LOST_EVIDENCE_ONLY.md`.** The original R3 #108 fire
(instance 36852855) produced a durable **9/9 SUPPORTED-STRONG** verdict but
its 345 MB `ckpt_hexad_integ_final.pt` was LOST to vast.ai proxy degradation
pre-pull (the cycle-88 `.clm v1` precedent — `g_fire_dispatch_robust` /
`g_hf_naming` process_upload_mandate (d)).

The fire is **deterministic** (RANDOM-INIT seed-fixed, seed=0,
`g_clm_from_scratch` — no `load_state_dict` / `torch.load` path; F-INTEG-3
AST-checked). T1 re-dispatched the SAME config/seed → the SAME 9/9 verdict
and **this time the ckpt was PULLED and byte-verified.**

## Recovered ckpt

| field | value |
|---|---|
| local path | `state/hexad_integ_fire_2026_05_16/ckpts/ckpt_hexad_integ_fire_final.pt` |
| size | **345,504,632 bytes** (== original on-pod) |
| sha256 | `230df953051f47dc1278d6052f06a35f543f7339a0c4f4cc0dc1a6e02f6e4b27` |
| md5 | `156113eaeada1e1046096b41c9e95a53` |
| remote on-pod md5 | `156113eaeada1e1046096b41c9e95a53` — **MATCHED (byte-identical)** |
| contents | `d_state_dict` (293 tensors) + `bridge_state_dict` (14 tensors); Group-A (D+Bridge) only — C/S/W/M/E gradient-group-B / non-param per φ(6)=2 barrier |
| param_hash_init | `408403506a965220` (== original — determinism proven) |
| trainable_param_count | 85,822,840 |
| scale | seed=0, vocab=256, d_model=512, n_layer=8, max_cells=64, seq_len=256, n_steps=400 |

## Provenance

- **Refire instance**: vast.ai `36854209`, A100 SXM4, $0.6023/hr.
- **Refire wall / cost**: 151.24 s / **$0.0253** actual (original was 163.6 s
  / $0.03 — only wall differs; all metrics are seed-deterministic and matched
  bit-for-bit).
- **Reproduction**: BIT-EXACT 9/9 SUPPORTED-STRONG. loss 6.0194→5.5795
  (avg100 5.6425→5.5743), cells 3→5 (max 10), phi_best 4.4153,
  param_hash_init 408403506a965220 — all identical to the original LOST fire.
- **Recovery mechanism**: `g_fire_dispatch_robust` worked exactly as designed.
  The same proxy degradation that LOST the original ckpt reset the scp at
  ~92% on attempt 1; the **retry 2/3 logic + SAVE_POD=1 auto-promote**
  (pod retained until pulled) completed the pull on the second attempt. The
  on-pod `result.json` md5-matched the local copy.
- **Pod lifecycle**: instance `36854209` destroyed explicitly post-pull
  (dispatch "[OK] all artifacts pulled — destroying instance now" path);
  **zero orphan vast instances** confirmed at end.

## Honest tiering (no over-claim)

- Verdict is **EMPIRICAL SUPPORTED-STRONG, NOT 🔵**. F-INTEG-5 CE-descent =
  SGD OUTCOME (B-D-NOTE pattern). Synthetic byte-corpus integration WIRING
  fire — **no language-quality / fluency claim**.
- anima verdict 🔵 (B-D 4/4, 7/7) is independent + already max — this
  recovery does **not** move it; it only restores the ckpt artifact.
- Per `g_hf_naming` (2026-05-16): HF canonical = NONE (HEXAD pivot;
  dancinlife/* = deprecated junk). **No HF upload** for this substrate
  integration WIRING ckpt. The ckpt stays **local + git-tracked provenance**
  (the 345 MB binary is git-excluded as noise — like the MACSMOKE ckpt;
  this doc + result.json carry the sha256/size/provenance).
