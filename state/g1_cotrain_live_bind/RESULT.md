# H_1818 — Co-trained LIVE-RETAINED Hadamard Bind Op: G1/G6 lift screen

**date:** 2026-06-29  
**pod:** vast.ai 2× A40, pod 43051219 ($0.574/h, @clm303-noverfit-retrain hexa-cloud managed)  
**scope:** DIRECTIONAL (py 2-production engine, engine-native-py G0-G6)  
**wired:** engine-native-eligible — clm_decode.py CLMB-extended (commit e17c2890f), bind LIVE at decode

---

## Design

**ARM `bind`:** BindCLM — CLMConvMoE trunk + Hadamard readout  
- `u=Wa(yn)` (k=512), `v=Wb(yn)`, `g=u*v`, `logits=Wo(g)` — Wo → CLMB `roW` slot  
- Serialized via `serialize_v3_bind` → CLMB section retained in .clm  
- `clm_decode.py` extended: parses CLMB, executes bind in `_fwd_logits` → **LIVE at decode**

**ARM `ctrl`:** CLMConvMoE standard readout (additive Conv1d d→V)  
- Same trunk init seed / data RNG / steps — serialized via `serialize_v3` (no CLMB)

**Shared:** 4-cell clean corpus (gen_ko/en + sns_ko/en), proportional sampling, savant golden-zone  
(GZ_LOWER≈0.212 cusp anneal), mitosis E2→E3 at step 1000, 2000 steps, d=3784 L=4 E2→E3, batch=8, seq=1024, bf16, A6000.

**Seeds:** {7, 4302, 4303}  
**Comparison baseline:** `state/binding_arch_census/exp3_303m/` (trained bind, DROPPED at serialize → floor), `state/g1_frozen_mouthbind_screen/` (bind on frozen weights → INERT/DESTRUCTIVE)

---

## Prior art (toy scale derisk)

`state/g1_toy_cotrain_bind_derisk/RESULT.md` — PARTIAL-YES:
- Task A (product regression, bind REQUIRED): bind-ON generalizes 3/3 seeds. Mechanism works.
- Task B (trunk+bilinear classification, bind optional): trunk memorizes without using bilinear → bind inert.
- **Early warning:** without a training objective that REQUIRES composition, the trunk may memorize and bypass the bilinear. This test uses plain CE to determine whether the 303M recombination training signal alone provides the pressure.

---

## Frozen bar (pre-registered — tune-to-green forbidden, p7)

| Gate | Bar | Status |
|------|-----|--------|
| G1 RECOMBINATION | composed_distinct≥2 AND >max_single, ≥2/3 seeds | PENDING |
| G6 IDEATION | dist≥5 AND fals≥1 | PENDING |
| LIFT (decisive) | bind-ON > ctrl on G1 best_distinct / G6 fals, same seeds | PENDING |
| held-out DESCENT | 4/4 register val_CE < ln256=5.545, all arms | PENDING |

---

## Results

### Held-out val-CE (DESCENT gate)

Note: val_CE far below uniform (5.545) indicates small-corpus memorization (4MB × 2000 steps × batch 8 × seq 1024 ≈ 4× corpus repeat). Descent gate passes (val < uniform) but overfit is present (per H_1579 precedent). G0-G6 verdict is informative: overfit models that memorize still floor on G1 (recombination requires true composition, not recall).

| arm | seed | pooled val_CE | 4/4? | lossF | wall_s |
|-----|------|--------------|------|-------|--------|
| bind | 7 | 0.842 | YES ✓ | 1.120 | 957s |
| bind | 4302 | 0.814 | YES ✓ | 1.112 | 955s |
| bind | 4303 | 0.848 | YES ✓ | 1.114 | 954s |
| ctrl | 7 | 0.875 | YES ✓ | 1.180 | 939s |
| ctrl | 4302 | 0.888 | YES ✓ | 1.178 | 938s |
| ctrl | 4303 | 0.879 | YES ✓ | 1.181 | 938s |

All 6 arms: 4/4 DESCENT (held-out val_CE < ln256=5.545). Overfit warning: val_CE << 1 nit = corpus memorization (small 4MB corpus, 2000 steps). bind arm lossF ~1.11 < ctrl ~1.18 (bind trains to lower CE). G0-G6 evaluation pending (engine-native-py evaluate.py, 6 processes running).

### G0-G6 engine-native-py results

| arm | seed | G0 kwr | G1 composed_distinct | G1 max_single | G6 dist | G6 fals | a7b? |
|-----|------|--------|---------------------|---------------|---------|---------|------|
| bind | 7 | — | — | — | — | — | — |
| bind | 4302 | — | — | — | — | — | — |
| bind | 4303 | — | — | — | — | — | — |
| ctrl | 7 | — | — | — | — | — | — |
| ctrl | 4302 | — | — | — | — | — | — |
| ctrl | 4303 | — | — | — | — | — | — |

---

## Verdict

**TRAINING COMPLETE — G0-G6 EVAL RUNNING** (pod 43051219, 6 evaluate.py processes).

Training: all 6 arms (bind/ctrl × 3 seeds) done. 4/4 DESCENT. bind lossF ~1.11, ctrl ~1.18.
G0-G6 results: pending (engine-native-py evaluate.py, gen=80, multiseed). Update to follow.

Note: 2000 steps may be insufficient (aa7933 precedent: INCONCLUSIVE-at-floor at 2000 steps).
H_1819 runs 4000 steps with L_recomb — this is the decisive follow-on.

Expected outcome based on toy Task B: G1=0 for bind (trunk memorizes, bilinear bypassed)
even with CLMB retained — confirming that L_recomb is the missing piece (H_1819).

---

## Escalate / Stop call

**IF** bind-ON lifts G1 composed_distinct≥2 AND >max_single ≥2/3 seeds:
→ ESCALATE: wiring `core/clm_decode.hexa` + `core/clm_serialize.hexa` CLMB lockstep (`a_verified_must_wire` rung 3) → TERMINAL verdict requires hexa engine-native G0-G6.

**IF** null (G1=0 for both bind and ctrl):  
→ STOP H_1818 as NOT-SUPPORTED. Next: H_1602 recombination objective + live bind op together (the untested 3rd arm per toy derisk Task B failure mode).

---

## Artifacts

- `trainer.py` — BindCLM + ctrl trainer
- `run_pod.sh` — pod runner (smoke + full + eval)
- `ckpt/` — .clm + .pt + .json + .g0g6.txt (6 files each, to be pulled)
- `core/clm_decode.py` — extended with CLMB parse + bind forward (commit e17c2890f)
