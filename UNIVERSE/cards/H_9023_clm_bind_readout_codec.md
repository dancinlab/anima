# H_9023 — `.clm` bind-readout (Hadamard) codec extension

**tier:** 🟢 ENGINE-NATIVE (codec implemented + hexa≡py byte-parity + backward-compat 0-regression). The G1/G6 *capability* verdict on a real ARM-BIND ckpt is a follow-on (needs the trained bind303m ckpt + GPU).

**wired:** WIRED-live — `core/clm_decode.{hexa,py}` (lockstep, byte-parity) + serializer/verifier; bind `.clm` enters the SAME generator L3 slot (`a_core_engine_map`); ARCHITECTURE.json clm node updated.

## Claim

The `.clm` format + decode are extended to support a **bind-readout (Hadamard) op** as a first-class readout, so EXP-3 ARM-BIND ckpts (H_1603/H_1617: `g=u⊙v`, multiplicative coincidence readout) can be serialized → CORE-decoded → measured engine-native. Previously the `.clm` codec knew only an additive `Conv1d(d→V)` readout, so bind/bind_linear were **`.clm`-BLOCKED-by-construction** and engine-native G1/G6 was impossible (torch-side probe only = DIRECTIONAL).

This is `a_engine_native_learning` **engine-transform-to-fit-the-learning**: the engine grows to fit the op the research needs (precedent: AdaptField scalar→vector H_1199).

## Format design (in-place, backward-compatible — no magic bump)

- **readout-type flag** lives in an OPTIONAL `CLMB` trailer (sentinel `67,76,77,66` = "CLMB") appended AFTER the CLMX ext arrays. Absent ⇒ `readout_type=0` (additive — existing `.clm` decode byte-identical).
- bind layout: the output proj **Wo** rides the EXISTING `roW` slot (`cout=V, rest=k` — self-describing, so `(d,E,V,L,K)` recovery is UNCHANGED); the CLMB trailer carries `readout_type:u8` (1=Hadamard `u*v`, 2=linear `u+v`) + `Wa`/`Wb` int4 conv blocks (`k,d`) + `Wa`/`Wb` bias ext.
- bind forward: `u=Wa(yn)`, `v=Wb(yn)`, `g = u*v | u+v`, `logits = Wo(g)` (1:1 with `BindCLM`, trainer.py).

## Files changed (2-production lockstep)

- `core/clm_decode.hexa` — CLMB parse in `_clmd_load` (rtype/Wa/Wb/ro_rest), bind branch in `_clmd_scratch_new`/`_free`/`_clmd_fwd_logits_sc`/`_clmd_fwd_logits`, pub `clm_readout_type`, rtype in `clm_forward_ce`.
- `core/clm_decode.py` — byte-parity mirror (CLMB parse + bind `_fwd_logits` branch).
- `train/clm/model/clm_serialize_v2.py` — `serialize_v3_bind` (+`_pack_main_blob` refactor, `CLMB` const).
- `train/clm/model/verify_clm_v2.py` — CLMB parse in `parse_clm`/`_load_clm_weights`, bind `_fwd_logits`, bind round-trip tests.
- `state/1620_clm_bind_codec/` — QA harness (`build_bind_clm.py`, `decode_hx.hexa`, `decode_py.py`, `golden_bind.py`, `export_bind_clm.py`).

## QA (all on mac arm64 CPU, $0)

- **byte-parity hexa≡py** (single-decode oracle, synth bind .clm): bind-Hadamard, bind-linear, AND additive — `model_ce` to 6 decimals + argmax bytes IDENTICAL. **PASS**.
- **exact-numpy golden** (independent math.erf-gelu fwd vs py engine): argmax match all 3; residual = gelu-approx (same magnitude in the additive twin → bind adds 0 error). **PASS**.
- **backward-compat**: real d768 additive golden `clm_d768_e2l1.clm` → `readout_type=0`, `model_ce 2.51 < shuffle 4.58` (decodes correctly); serializer V2/V3 byte-eq + round-trip tests still pass = **regression 0**.
- **held-out mirror-DESCENT bind path**: gate fires on random bind (NO-DESCENT, correctly rejected) and passes on trained additive (DESCENT). **PASS**.
- **torch 3-way** (torch == hexa == py): torch absent on mac (heavy work → pool/torch host); `golden_bind.py torch` provided to run on the trainer host. The hexa≡py byte-exact parity + the exact-numpy golden already validate the bind readout end-to-end through the format.

## Follow-on

1. On a torch host: run `golden_bind.py torch` (torch ARM-BIND fwd ≡ .clm decode).
2. Train/recover a real bind303m ckpt (EXP-3 ARM-BIND, H_1603/H_1617) → `export_bind_clm.py` → bind .clm → held-out descent gate → **engine-native G1/G6** via `cli/anima.hexa -- eval` (the previously-BLOCKED measurement, now unblocked).
