# H_1819 — co-trained bind op × recombination objective: 3-arm decisive G1 result

**date:** 2026-06-29  
**pod:** vast.ai 2× A40, pod 43051219 ($0.574/h, hexa-cloud managed @clm303-noverfit-retrain)  
**scope:** DIRECTIONAL (py 2-production engine, engine-native-py G0-G6)  
**wired:** engine-native-eligible — clm_decode.py CLMB-extended (H_1818 commit e17c2890f), bind LIVE at decode for op_plaince + op_obj arms

---

## Design (PREREG frozen — see PREREG.md)

**3-arm causal isolation** (matched seed/data/steps = 4000):

| arm | training signal | role |
|-----|----------------|------|
| (a) `op_plaince` | BindCLM + plain CE (H_1818 redux at 4000 steps) | negative control: op without L_recomb |
| (b) `obj_only` | additive CLM + L_recomb InfoNCE (discarded at serialize) | negative control: L_recomb without bind op at decode |
| (c) `op_obj` | BindCLM + L_recomb InfoNCE (Pa=Wa,Pb=Wb shared) | ★ decisive: structure + objective together |

**Decision test (PREREG frozen):** (c) strictly > (a) AND (c) strictly > (b) on G1 composed_distinct → "bind op + recomb objective together lift G1".

**L_recomb (InfoNCE):** z_a=trunk[T//3], z_b=trunk[2*T//3], z_c=trunk[T-1]; g=Pa(z_a)*Pb(z_b) (Hadamard in k=512 space); InfoNCE predict z_c from g vs cross-batch; τ=0.1, λ_recomb=0.1.

---

## Frozen bar (pre-registered)

| Gate | Bar | Status |
|------|-----|--------|
| G1 RECOMBINATION | composed_distinct≥2 AND >max_single, ≥2/3 seeds | PENDING |
| G6 IDEATION | dist≥5 AND fals≥1 | PENDING |
| LIFT (decisive) | (c) > (a) AND (c) > (b) on G1 best_distinct / G6 fals, per seed | PENDING |
| held-out DESCENT | 4/4 register val_CE < ln256=5.545, all 3 arms | PENDING |
| G0 pass | kwr≥0.50, ≥4/5 seeds | PENDING |

---

## Training results

### Held-out val-CE (DESCENT gate, math.log mirror)

| arm | seed | pooled val_CE | 4/4? | lossF | l_recomb_final | wall_s |
|-----|------|--------------|------|-------|----------------|--------|
| op_plaince | 7 | 0.627 | ✓ 4/4 | 1.072 | N/A | 2018.6 |
| op_plaince | 4302 | — | — | — | N/A | — |
| op_plaince | 4303 | — | — | — | N/A | — |
| obj_only | 7 | 0.849 | ✓ 4/4 | 1.343 | 1.204 | 2077.4 |
| obj_only | 4302 | — | — | — | — | — |
| obj_only | 4303 | — | — | — | — | — |
| op_obj | 7 | — | — | — | — | — |
| op_obj | 4302 | — | — | — | — | — |
| op_obj | 4303 | — | — | — | — | — |

*Note: op_plaince/obj_only seed7 training complete (2026-06-29 ~12:46 UTC). op_obj seed7 training starting after descent_gate verification (~13:00 UTC). Seeds 4302/4303 follow sequentially.*

---

## G0-G6 engine-native-py results

### DECISION TEST table (PREREG frozen bars)

| arm | seed | G0 kwr | G1 composed_distinct | G1 max_single | G6 dist | G6 fals | a7b? |
|-----|------|--------|---------------------|---------------|---------|---------|------|
| **op_plaince** | 7 | — | — | — | — | — | — |
| **op_plaince** | 4302 | — | — | — | — | — | — |
| **op_plaince** | 4303 | — | — | — | — | — | — |
| **obj_only** | 7 | — | — | — | — | — | — |
| **obj_only** | 4302 | — | — | — | — | — | — |
| **obj_only** | 4303 | — | — | — | — | — | — |
| **op_obj** | 7 | — | — | — | — | — | — |
| **op_obj** | 4302 | — | — | — | — | — | — |
| **op_obj** | 4303 | — | — | — | — | — | — |

**Decision test result:** PENDING

---

## Verdict

**TRAINING IN PROGRESS** — G0-G6 evals pending.

*Results will be filled in upon completion.*

---

## Artifacts

- `trainer.py` — 3-arm trainer (BindCLM / ObjOnlyCLM / BindRecombCLM)
- `run_pod.sh` — pod runner (smoke → train → eval → summary)
- `PREREG.md` — frozen specification
- `ckpt/` — .clm + .pt + .json + .g0g6.txt (9 each, pulled post-eval)
- `core/clm_decode.py` — CLMB extension (H_1818, shared by op_plaince + op_obj)

**Pod:** 43051219 (teardown pending — after ckpt PULL + G0-G6 complete, a_fire_recover_complete)
