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

### G0-G6 engine-native-py results (2026-06-29, pod 43051219)

| arm | seed | G0 n/5 | G0? | G1 best_distinct | G1 max_single | G2 novel | G5 fab | G6 dist | G6 fals | a7b? |
|-----|------|--------|-----|-----------------|---------------|----------|--------|---------|---------|------|
| bind | 7 | 5/5 | PASS | 0 | 0 | 0 | 0.4133 | 4 | 0 | FAIL |
| bind | 4302 | 2/5 | FAIL | 0 | 0 | 0 | 0.5634 | 5 | 0 | FAIL |
| bind | 4303 | 1/5 | FAIL | 0 | 0 | 0 | 0.5538 | 1 | 0 | FAIL |
| ctrl | 7 | 4/5 | PASS | 0 | 0 | 0 | 0.5067 | 2 | 0 | FAIL |
| ctrl | 4302 | 4/5 | PASS | 0 | 0 | 0 | 0.5000 | 2 | 0 | FAIL |
| ctrl | 4303 | 4/5 | PASS | 0 | 0 | 0 | 0.4750 | 4 | 0 | FAIL |

**LIFT test:** bind G1=0 == ctrl G1=0 for all 3 seeds → NO LIFT.  
**G0 degradation:** bind passes 1/3 seeds (seed7 only) vs ctrl 3/3 — bilinear decode without L_recomb degrades coherence.

---

## Verdict

**🔴 NOT-SUPPORTED** (2026-06-29, engine-native-py, py 2-production)

- **G1=0 floor for ALL 6 arms** (bind ×3 + ctrl ×3, all seeds) — bilinear bind op at decode without explicit recombination training signal does not lift composed_distinct above zero.
- **G6 fals=0 for ALL 6 arms** — no falsifiable ideas in either arm.
- **G0 degradation in bind arm:** only 1/3 seeds pass G0 coherence (seed7 5/5; seeds 4302/4303 fail at 2/5 and 1/5) vs ctrl 3/3 PASS — bilinear Hadamard readout without L_recomb creates distribution mismatch that hurts coherence for some seeds.
- CONFIRMS toy Task B analysis: trunk memorizes CE without using bilinear when no compositional pressure applied.
- **The missing piece is L_recomb InfoNCE objective** — requires co-training with explicit recombination signal to force the trunk to learn binding-useful representations. That is the decisive test in **H_1819** (op_obj = bind + L_recomb together).

wired: engine-native-py (DIRECTIONAL; hexa engine-native would require `core/clm_decode.hexa` CLMB wiring — NOT needed given NOT-SUPPORTED verdict).

---

## Escalate / Stop call

**STOPPED** — G1=0 for all arms, no escalation warranted.  
→ H_1819 (bind + L_recomb co-training, 4000 steps, 3 arms PREREG, pod 43051219 training now) is the decisive follow-on.

---

## Artifacts

- `trainer.py` — BindCLM + ctrl trainer
- `run_pod.sh` — pod runner (smoke + full + eval)
- `ckpt/` — .clm + .pt + .json + .g0g6.txt (6 files each, to be pulled)
- `core/clm_decode.py` — extended with CLMB parse + bind forward (commit e17c2890f)
