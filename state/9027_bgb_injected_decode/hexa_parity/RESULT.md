# decode.hexa BGB byte-parity — TASK #2 (H_9027 / H_6170 wire-in)

VERDICT: PASS (engine-native byte-parity, host CPU `mm` path) — decode.hexa now HAS
BGB injected-attention at byte-parity with decode.py.

## What was verified
core/decode.hexa BGB path (bg_load `_bg_read_bind_trailer` + `_bg_apply_bind` after
the L base blocks before ln_f + `bytegpt_decode_argmax` KV-guard) produces token
streams BYTE-IDENTICAL to core/decode.py (the numpy `--py` scorer, validated math-
correct vs torch f64 in ../verify.txt / H_6170) for, seed="hello world " gen=48:
  base   (plain, no trailer)      hexa == py   (no-regression)      PASS
  I1     (N=1 bind, gate=0.7)     hexa == py                        PASS
  I2     (N=2 bind, gate=0.5,-0.4) hexa == py                       PASS
  gate0  (N=1 bind, gate=0.0)     hexa == py AND == base (no-op)    PASS
All 48/48 tokens identical per fixture. Streams in hexa_streams.txt.

## How (honest scope, c9)
- Fixtures: gen_fixtures.py writes tiny (vocab256 d32 nlay2 nh4 block16) .bin in the
  bg_load byte layout DIRECTLY (torch-free; torch unavailable on mac) + BGB trailer;
  decode.py `.pyids` are the reference. Math-correctness already gated by verify.txt.
- hexa run: bgb_host_extract.hexa = VERBATIM extract (extract_host.py, byte-for-byte
  copy) of decode.hexa's host-scalar functions, run on aiden pool (hexa v0.513.0),
  HEXA_DET=1, CUDA_VISIBLE_DEVICES="" (CPU `mm` = byte-faithful to numpy).

## PRE-EXISTING TOOLCHAIN WALL (BLOCKED-INFRA, not a BGB defect)
The FULL core/decode.hexa does NOT compile on fleet hexa v0.511/v0.513 — its device
path references forge_dispatch_* / farr_attn_dt_decode_gpu / farr_attn_dt_decode_
batch_gpu builtins ABSENT from these hexa builds. UNMODIFIED origin/main decode.hexa
fails to compile IDENTICALLY (verified on aiden). Hence eval runs `anima evaluate
--py` (session policy). The byte-parity test therefore ran a verbatim host-scalar
extract. GPU `mm` (cuda=1) flips argmax on the tiny RANDOM model (tiny logit margins;
base itself diverges under GPU mm) — not a BGB issue; byte-parity is the CPU-path
claim, which is exactly what decode.py mirrors. Full device-path BGB + a fleet hexa
carrying the forge builtins is a follow-on (ING).
