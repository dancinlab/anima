# H_1818 — co-trained LIVE-RETAINED bind op: G1/G6 lift screen

**id:** H_1818  
**slug:** cotrain_live_bind  
**tier:** PRE-REG (GPU-firing now, A6000 idle pod)  
**date:** 2026-06-29  
**wired:** engine-native-eligible (clm_decode.py CLMB extended + CLMB retained in .clm)

---

## Hypothesis

Hadamard binding readout (`g = Wa(x) * Wb(x)`, `logits = Wo(g)`) lifts G1 recombination
and G6 ideation **if and only if** the op is both (a) co-trained end-to-end with
trunk+readout so concept axes form, AND (b) retained in the serialized .clm so it
executes LIVE at decode.

Prior art falsified both un-retained paths:
- EXP-3 (H_1603/H_1617): bind trained but **dropped at serialize** → INCONCLUSIVE-at-floor
- Frozen mouthbind screen (H_1616/1623/1649): bind **bolted onto frozen weights** → INERT/DESTRUCTIVE

This is the first test of the untested sweet-spot between those two failed paths.

---

## Design

**ARM `bind`:** `BindCLM` = CLMConvMoE trunk + Hadamard readout  
- `u = Wa(yn)` (k=512), `v = Wb(yn)`, `g = u*v`, `logits = Wo(g)`  
- Serialized via `serialize_v3_bind` → CLMB section retained  
- `clm_decode.py` extended to parse CLMB + execute bind in `_fwd_logits` → **LIVE at decode**

**ARM `ctrl`:** Standard CLMConvMoE (additive Conv1d d→V readout)  
- Same trunk init seed / data / steps — serialized via `serialize_v3` (no CLMB)

**Shared recipe:** 4-cell clean corpus (gen_ko/en + sns_ko/en), savant golden-zone
inhibition (GZ_LOWER≈0.212, cusp anneal), mitosis E2→E3 mid-training, 2000 steps,
d=3784 L=4 E2→E3, batch=8, seq=1024, bf16 on A6000.

**Seeds:** {7, 4302, 4303}

---

## Frozen bar (pre-registered — tune-to-green forbidden, p7)

| Gate | Bar |
|------|-----|
| G1 RECOMBINATION | `composed_distinct≥2` AND `>max_single` AND coherent, ≥2/3 seeds |
| G6 IDEATION | `dist≥5` AND `fals≥1` |
| LIFT (decisive) | bind-ON strictly > ctrl on G1 best_distinct / G6 fals, same seeds |
| held-out DESCENT | 4/4 register val_CE < ln256 (else overfit → invalid) |

---

## Infrastructure change

`core/clm_decode.py` is **engine-transformed** (a_engine_native_learning
engine-transform-to-fit):
- `clm_load_weights`: parses CLMB section (bytes 67,76,77,66) after CLMX ext arrays
- `_fwd_logits`: if `bind_type!=0`, applies `u*v` (Hadamard) or `u+v` (linear)
  bind readout instead of `_conv1d(yn, roWt, ...)`. `roWt=(k,V)` holds Wo.T.

Round-trip parity: verified by smoke smoke-gate on pod (bind_type=1 parsed correctly).

---

## Artifacts

- `state/g1_cotrain_live_bind/trainer.py` — BindCLM + ctrl trainer
- `state/g1_cotrain_live_bind/run_pod.sh` — pod runner (smoke + full + eval)
- `state/g1_cotrain_live_bind/ckpt/` — .clm + .pt + g0g6 logs (to be populated)
- `state/g1_cotrain_live_bind/RESULT.md` — verdict (to be written post-eval)
- `core/clm_decode.py` — extended with CLMB parse + bind forward

---

## Verdict

*Pending GPU run. Expected: 6 trains × ~20min each = ~2h, ~$1.6 @ A6000 $0.40/h.*

**HYPOTHESIS:** bind-ON > ctrl on G1 best_distinct/G6 fals ≥2/3 seeds AND held-out 4/4 DESCENT.  
**SCOPE:** DIRECTIONAL (py 2-production = retired 2026-06-28, sufficient for floor/lift screen).  
If bind-ON lifts G1≥2 ROBUST → escalate to hexa clm_decode/serialize lockstep wiring (a_verified_must_wire rung 3) for TERMINAL.
