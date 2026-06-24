# clm303.clm garble integrity — 3-way decode check (CONTROLLED)

**Verdict: 🔴 clm303.clm SERIALIZATION/CKPT DEFECT confirmed. Engine decode path is INTACT. Any G0–G6 score on this ckpt is garbage (decode-integrity prerequisite FAILS).**

Date 2026-06-24 · ckpt `state/clm303_savant_mitosis_train/clm303.clm` (sha 75b04897, v0.3 L4·d3784·E3·V256, savant+mitosis) · frozen prompt `"a new idea about consciousness: "` · gen=40 top_k=40 temp=0.700.

## 3-way decode (same frozen prompt)

| arm | implementation | result |
|---|---|---|
| **GPU forge** | live `core/clm_decode.hexa`, pod RTX 4090, `cuda_available=1`, `[OWN-GEMM-FIRED] _hx_k_gemm DEVICE path` | `ggndtle_oppa:ggndlle__\xffrlen_antag_ndll` — garble (48 B) |
| **CPU farr** | live `core/clm_decode.hexa`, mac, `cuda_available=0` (single-thread scalar) | `ggndtle_oppa:ggndlle__\xffrlen_antag_ndll` — garble (48 B) — **BYTE-IDENTICAL to GPU** |
| **numpy mirror (golden)** | `state/mid_convmoe_fire/clm_decode_mirror.py` — independent pure-numpy reimpl of `_clmd_load`+`_clmd_fwd_logits`, reads the `.clm` BYTES directly (int4 dequant w=code·scale + causal dilated conv1d + GN VERBATIM), v0.3 (L,E) derivation correct | next-byte CE on ko heldout (64 win): **NO-DESCENT** |

## numpy mirror CE (the discriminator)

| ckpt | CE_real (ko heldout) | CE_uniform (ln 256) | BELOW_UNIFORM | VERDICT |
|---|---|---|---|---|
| **clm303.clm** (test) | **7.622** | 5.545 | **0** | **NO-DESCENT** |
| **clm_d768_e2l1.clm** (CONTROL, known-good Lane-P) | **4.442** | 5.545 | **1** | **GREEN (DESCENT)** |

The control proves the mirror is correct: a healthy v0.2 ckpt decodes to descent (CE 4.44 < uniform) even on Korean; clm303 does NOT (CE 7.62 > uniform = worse than random).

## Diagnosis (2-axis isolation)

1. **GPU forge ≡ CPU farr, BYTE-IDENTICAL** → the engine decode path is intact and deterministic (forge own-GEMM byte-matches farr). The `summer-sm120` "CPU-farr defect" hypothesis is **rejected** — the "GPU coherent ⇒ CPU defect" branch does not fire (GPU also garbles).
2. **Independent numpy mirror = NO-DESCENT** (controlled GREEN on a known-good ckpt) → the **serialized `.clm` weights themselves** do not predict text. The defect is in serialization (`pt_to_engine_bin` / `clm_serialize_v2` int4→v0.3), NOT decode.

The training-reported `ko heldout CE 3.351 ✅` was a **torch-side (pre-serialization)** measurement; the serialized artifact is a separate, corrupted product (mirror CE 7.62). Same family as the `clm303_L4_d3784` German-garble serialization anomaly.

## Implication

`anima eval clm303.clm` would produce G0–G6 scores, but all are garbage — the decode-integrity prerequisite fails. The fix is RE-SERIALIZATION from an intact torch ckpt (vast 42222605), verified by re-running the mirror until CE < uniform, NOT a decode-path change.
