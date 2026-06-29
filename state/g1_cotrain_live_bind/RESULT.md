# H_1818 — Co-trained LIVE-RETAINED Hadamard Bind Op: G1/G6 lift screen

**date:** 2026-06-29  
**pod:** vast.ai A6000, pod 43053585 (~$1.6 total)  
**scope:** DIRECTIONAL (py 2-production = retired 2026-06-28; sufficient for floor/lift screen)  
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

| arm | seed | ko-general | en-general | ko-sns | en-sns | pooled | 4/4? |
|-----|------|-----------|-----------|--------|--------|--------|------|
| bind | 7 | — | — | — | — | — | PENDING |
| bind | 4302 | — | — | — | — | — | PENDING |
| bind | 4303 | — | — | — | — | — | PENDING |
| ctrl | 7 | — | — | — | — | — | PENDING |
| ctrl | 4302 | — | — | — | — | — | PENDING |
| ctrl | 4303 | — | — | — | — | — | PENDING |

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

**PENDING** — GPU run in progress (pod 43053585, ~$1.6 A6000).

Expected ~2h from job start. Background poll will trigger RESULT.md update.

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
