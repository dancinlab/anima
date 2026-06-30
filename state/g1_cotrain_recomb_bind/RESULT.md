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

| arm | seed | pooled val_CE | 4/4? | descent_gate (heldout_ce) | lossF | l_recomb_final | wall_s |
|-----|------|--------------|------|---------------------------|-------|----------------|--------|
| op_plaince | 7 | 0.627 | ✓ 4/4 | ✓ PASS (1.438 < 5.545) | 1.072 | N/A | 2018.6 |
| op_plaince | 4302 | 0.639 | ✓ 4/4 | ✓ PASS (1.577 < 5.545) | 1.067 | N/A | 1906.1 |
| op_plaince | 4303 | — | — | — | — | N/A | — |
| obj_only | 7 | 0.849 | ✓ 4/4 | ✓ PASS (1.709 < 5.545) | 1.343 | 1.204 | 2077.4 |
| obj_only | 4302 | 0.809 | ✓ 4/4 | ✓ PASS (descent all 4/4) | 1.365 | 1.216 | 1930.5 |
| obj_only | 4303 | — | — | — | — | — | — |
| op_obj | 7 | 0.766 | ✓ 4/4 | ✓ PASS (1.401 < 5.545) | 1.255 | 1.436 | 2067.2 |
| op_obj | 4302 | 0.759 | ✓ 4/4 | ✓ PASS (4/4 DESCENT) | 1.304 | 1.405 | 1945.5 |
| op_obj | 4303 | — | — | — | — | — | — |

*seed7 ALL DONE (4/4 DESCENT each). seed4302 ALL DONE (4/4 DESCENT each). seed4303 training IN PROGRESS (3 arms parallel).*

---

## G0-G6 engine-native-py results

### DECISION TEST table (PREREG frozen bars)

| arm | seed | G0 kwr | G1 composed_distinct | G1 max_single | G6 dist | G6 fals | a7b? |
|-----|------|--------|---------------------|---------------|---------|---------|------|
| **op_plaince** | 7 | 3/5 FAIL | 0 ✗ | 0 | 3 | 0 | FAIL |
| **op_plaince** | 4302 | 3/5 FAIL | 0 ✗ | 1 | 2 | 0 | FAIL |
| **op_plaince** | 4303 | 3/5 FAIL | 0 ✗ | 1 | 1 | 0 | FAIL |
| **obj_only** | 7 | 3/5 FAIL | 0 ✗ | 0 | 3 | 0 | FAIL |
| **obj_only** | 4302 | 2/5 FAIL | 0 ✗ | 0 | 4 | 0 | FAIL |
| **obj_only** | 4303 | 4/5 PASS | 1 ✗ | 1 | 2 | 0 | FAIL |
| **op_obj** | 7 | 5/5 PASS | 0 ✗ | 0 | 2 | 0 | FAIL |
| **op_obj** | 4302 | 4/5 PASS | 0 ✗ | 0 | 2 | 0 | FAIL |
| **op_obj** | 4303 | 3/5 FAIL | 0 ✗ | 0 | 4 | 0 | FAIL |

**Decision test detail:**
- seed 7: g1(c)=0, g1(a)=0, g1(b)=0 | c>a=False c>b=False
- seed 4302: g1(c)=0, g1(a)=0, g1(b)=0 | c>a=False c>b=False
- seed 4303: g1(c)=0, g1(a)=0, g1(b)=1 | c>a=False c>b=False

Wins vs op_plaince: 0/3
Wins vs obj_only:   0/3
Wins BOTH:          0/3 (bar: >=2 = SUPPORTED)

**Decision test result:** 🔴 NOT-SUPPORTED
## Verdict

**🔴 NOT-SUPPORTED** (py 2-production engine, DIRECTIONAL scope)

**Scope:** py 2-production engine (`core/g_gates.py` + `core/clm_decode.py`, byte-parity proven). Not terminal — engine-native hexa retest required for terminal verdict.

**Decision test:** wins_both=0/3 (bar: >=2). NOT SUPPORTED..

**G0:** op_plaince: G0 0/3 PASS, obj_only: G0 1/3 PASS, op_obj: G0 2/3 PASS.

**Next step:** G1 wall persists even with bind op + L_recomb combined → explore H_1820 (low-inhibition) or other lenses.