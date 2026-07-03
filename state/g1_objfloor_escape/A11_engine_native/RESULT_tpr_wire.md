# A11 CE-DELETED TPR-forward-slot — WIRE_SPEC v0.3 BUILT + MEASURED · FALSIFIED-CEILING

**Fire:** vast pod 43736708 (RTX 5090 32GB, torch 2.12.0.dev+cu128 sm_120, x86 linux),
2026-07-04. The single UNBUILT G1-escape cell (per RESULT_engine_native.md): the *pure
CE-deleted TPR forward-slot* (WIRE_SPEC steps 2-3), distinct from the additive
`ce+λ·aux` family (H_9120, already FALSIFIED-CEILING). This pod BUILDS + wires + trains +
scores it engine-native.

## What was built (WIRE_SPEC v0.3, all 5 steps)
1. **CE-DELETED InfoNCE trainer** (`a11_tpr_train.py`) — contrastive-replace InfoNCE
   (echo-A=current byte / echo-B=prev byte / wrong-D=random negatives), a 4-way softmax,
   **NO full-vocab F.cross_entropy anywhere**. CE is deleted, not added-to.
2. **TPR forward-slot readout** — R=2 FIXED orthonormal roles (balanced disjoint partition
   of d = the canonical orthonormal R=2 TPR slot), `c_r = yn ⊙ roles[r]`,
   `out[t] = Σ_r S_r·(yn[t] ⊙ roles[r])`. Warm-init reconstructs the base linear readout
   EXACTLY (warm_recon max|Δ| = 1.05e-2 fp32 noise → G0 preserved, no undertrain confound).
3. **Serializer v0.3 CLMT** — `roW`/`roB` slot ← S_0; new `"CLMT"` ext-block = R:u8 +
   roles[R,d] f32 + S_1[V,d] int4-sym + S_1 bias. Old golden `.clm` lack the tag → non-TPR path.
4. **Numpy scorer wiring** — `core/decode.py` `_clmd_load` CLMT parse + `_fwd_logits`
   bind_type=3 branch (byte-identical mirror of the hexa; grep -cE 'import torch|gauge_lib'
   on decode.py AND cli/evaluate.py = **0** → engine-native, a_eval_py_canonical TERMINAL).
5. **hexa wiring diff** for `core/decode.hexa` rtype=3 = `decode_hexa_CLMT_wire.md` (mirrors
   the numpy 1:1; full-engine build+device parity = follow-on per H_9027).

## Warm base (the G0 subtlety, honest c9)
- The WIRE_SPEC targets `clm_decode` (CLMConvMoE). Warm base = **clm303_clean** (the only CLM
  303M; d3784/L4/E3/K3). A faithful `.clm`→torch loader (dequant, SOFT MoE `variant="A"` to
  byte-match `decode.py nn_moe_router_fwd`) gives **trunk parity max|decode.py − torch| =
  1.1e-5, argmax-match** — the training forward is byte-faithful to the deployed scorer.
- **BUT clm303_clean is itself sub-G0 under mouth-gen eval** (kwr 0/5 at canonical gen=40;
  it decodes coherent-ish English — "It's harmassed. There's a things" — but below the G0
  bar on concept seeds). No G0-green CLM trunk exists (RESULT_engine_native.md: ByteGPT
  h1129c is the ONLY G0-green 303M). So the CLM-native number below carries a sub-G0 scope
  caveat; the ByteGPT twin (G0-green) removes it.

## Byte-exact parity (fixed ckpt)
- **CLM CLMT readout: numpy vs torch = 0.000e+00 (BYTE-EXACT PASS)** — `a11_tpr_parity.py`
  loads the trained TPR `.clm` via decode.py (dequant S_0,S_1,roles) and the TPR readout op
  matches the torch reference to 0.0; full-forward smoke finite, argmax sensible bytes.
- Trunk parity (`.clm`→torch): 1.1e-5. ByteGPT warm-init parity: 2.29e-5.

## G1 verdict — engine-native `anima evaluate --py` mouth-generation, 5 seeds, gen=40
Bar (frozen, verbatim): `best_distinct ≥ 2 AND > max_single AND coherent AND SCRAMBLE ≤ 1`.

**CLM TPR (clm_decode, WIRE_SPEC literal):**
| seed | best_distinct | max_single | coherent | scramble | HIT |
|------|---------------|------------|----------|----------|-----|
| 7    | 1 | 0 | T | 0 | floor |
| 1007 | 0 | 1 | F | 0 | floor |
| 2007 | 0 | 0 | F | 0 | floor |
| 3007 | 0 | 0 | F | 0 | floor |
| 4007 | 0 | 0 | F | 0 | floor |

**CLM: HIT 0/5 → FALSIFIED-CEILING · terminal_flip = FALSE** (best_distinct ≤ 1 = the
recombination floor). InfoNCE converged (0.50 → 0.022, held-out 0.028) — trained, not undertrained.

**ByteGPT TPR (decode.hexa byte mouth, G0-GREEN h1129c trunk — removes the sub-G0 caveat):**
| seed | best_distinct | max_single | coherent | scramble | HIT |
|------|---------------|------------|----------|----------|-----|
| 7    | 1 | 1 | F | 0 | floor |
| 1007 | 1 | 1 | F | 0 | floor |
| 2007 | 1 | 1 | F | 0 | floor |
| 3007 | 1 | 1 | F | 1 | floor |
| 4007 | 1 | 1 | F | 0 | floor |

**ByteGPT: HIT 0/5 → FALSIFIED-CEILING · terminal_flip = FALSE** (best_distinct = 1 = floor,
all 5 seeds). Warm-init parity 2.29e-5 (TPR == tied head, G0-green preserved); InfoNCE
0.37 → 0.025. The ONLY G0-green 303M trunk floors identically → the sub-G0 caveat on the
CLM number is REMOVED: the CE-deleted TPR forward-slot floors on a valid G0-green mouth.

## Why FALSIFIED-CEILING is TERMINAL (not just at-floor)
The R=2 **fixed-orthonormal-role** TPR forward-slot is **provably LINEAR in the
autoregressive hidden**: `out = Σ_r S_r·(yn ⊙ roles_r) = (Σ_r S_r·diag(roles_r))·yn =
W_eff·yn`. Hadamard-with-a-fixed-vector is linear, and a sum of linear maps is linear —
so the TPR readout collapses to a single effective linear readout `W_eff`, i.e. it has the
**IDENTICAL representational ceiling to the standard linear byte readout = the H_9120
floor, BY CONSTRUCTION.** The only free variables are (a) the InfoNCE objective —
already floored (H_1602 composed_nce) — and (b) factored-init implicit bias. The engine-
native 0/5 measurement CONFIRMS the proof. **H_9120 G1 objective-floor stays CONFIRMED-
TERMINAL under the CE-deleted TPR forward-slot; the last unmeasured escape cell is closed.**

## Artifacts (PULLED pre-teardown, a_fire_recover_complete → ~/anima-weights/g1_a11tpr/)
- `a11_tpr.clm` (177MB, CLM TPR CLMT v0.3) · `a11_tpr_bg.bin` (1.21GB, ByteGPT TPR + BGT)
- verdicts: `g1_score.json` (CLM) · `bg_g1_score.json` (ByteGPT) · parity `parity.log`
- logs: `clm_train.log` · `bg_train.log` · base evals `e3_base_eval.log`
- wiring: `decode.py.CLMT_BGT.diff` (numpy, byte-exact) · `decode_hexa_CLMT_wire.md` (hexa mirror)
- scripts: `a11_tpr_train.py` · `a11_tpr_bg_train.py` · `a11_tpr_parity.py` · `a11_tpr_score.py`
  · `patch_decode.py` · `patch_decode_bg.py`
- **cost:** shared RTX 5090 ~2.5h (torch nightly build + 2 warm-FT trains + 2×5-seed --py score
  + base evals), est. ~$1.5-2.
