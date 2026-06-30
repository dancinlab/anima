# UPduino enclosure thermal mitigation — 3-option comparison (2026-05-21)

Direct sibling of `upduino_enclosure_fem.py` baseline run. The base
cycle (G5 demiurge component, commit `6ea299145`) reported
**ΔT_max = 60.61 K**, **T_max = 80.6 °C**, headroom **4.4 °C** above
iCE40UP5K T_j,max = 85 °C (h = 10 W/m²K free convection, 1 W load).
Three mitigation strategies each re-run the same `solve_one_level()`
kernel with only the Robin BC `h_convection_w_per_m2k` adjusted.

## Result table

| Option | h_eff (W/m²K) | ΔT (K) FEM | ΔT (K) 1D | rel. err | T_max (°C) | Headroom (°C) | BOM ($) |
|--------|---------------|------------|-----------|----------|------------|---------------|---------|
| baseline (free conv)        |  10.0 | 60.610 | 60.610 | 1.7e-5  | 80.61 |  4.39 |  0 |
| **A — 40 mm fan**           |  50.0 | 12.125 | 12.125 | 7.2e-12 | 32.12 | **52.88** |  5 |
| **B — finned heatsink**     |  28.1 | 21.567 | 21.567 | 1.7e-12 | 41.57 | **43.43** |  3 |
| **C — pad + Al case**       | 121.2 + R_pad | 30.004 | 30.004 | 1.5e-11 | 50.00 | **35.00** | 17 |

(C row: FEM models the case-convection leg only at h_lumped = 121.2
W/m²K; the pad film ΔT = 25 K is added analytically from the Rth
network. BOM includes $2 pad + $15 Hammond Al case.)

## Recommendation

**Option A (40 mm fan)** if active cooling is acceptable — largest
headroom (53 °C, 12× the bare-plate margin), lowest T_max (32 °C, near
ambient), $5 BOM. Fan failure-mode caveat: a stalled fan reverts to
the baseline 4.4 °C headroom — design must include fan-tach feedback
or rated-life MTBF margin.

**Option B (finned heatsink)** if passive-only is mandated — 43 °C
headroom, $3 BOM, no moving parts. Best engineering trade-off for an
embedded-deployment FPGA: fan-free, < 10 g added mass, drop-in.

**Option C (pad + Al case)** if mechanical enclosure is required for
other reasons (IP-rating, structural protection). 35 °C headroom is
the smallest of the three, dominated by the R_pad = 25 K/W film. A
better thermal pad (Bergquist Sil-Pad TSP-A2000, k = 6.5 W/m·K) would
cut R_pad to 6.2 K/W and lift headroom to ~50 °C — see § honest C3.

## BOM ladder

```
$2  Bergquist Sil-Pad 900S thermal pad           (Option C only)
$3  Generic 50×33 mm 6-fin Al heatsink           (Option B)
$5  Noctua-class 40 mm 5 V axial fan + harness   (Option A)
$15 Hammond 1455T1601 100×80×25 mm Al case       (Option C only)
```

## Honest C3

1. The base FEM is **convection-limited** (Biot ≈ 6e-5); ΔT scales as
   1/h to machine precision, so the FEM is essentially a self-checking
   `ΔT = q/h` calculator for this geometry. Real thermal-mechanical
   coupling, transient warm-up, BGA-localised hot spots are NOT
   modelled (carried over from G5 scope_caveats #1, #3, #5).
2. h = 50 W/m²K for Option A is a textbook upper bound for 40 mm axial
   fans on Al — actual depends on fan curve, back-pressure, ambient
   noise floor. Wind-tunnel or CFD measurement required for GATE_CLOSED.
3. Option B's fin efficiency η = 0.996 assumes ideal pad-to-heatsink
   bonding and an isothermal base — a poorly bonded heatsink (air gaps)
   could halve the effective area and push headroom below 30 °C.
4. Option C's pad-resistance model is lumped; a true multi-body FEM
   (chip die + BGA + pad + Al case) would resolve spreading effects.
5. All options assume the 1 W steady-state load. The G5 scope_caveat
   #3 multi-load alternative (peak burst 2 W → CLB activity surge)
   is NOT swept here — would scale ΔT linearly, e.g. Option A peak
   ΔT = 24 K, headroom 41 °C — still safe but margin shrinks.

## Artifacts

```
option_A_fan.py            — FEM driver (h=50 override)
option_A_fan.json          — full record + mitigation metadata
option_A_fan.csv           — mesh convergence (4-level h-refinement)
option_B_finned.py / json / csv  — finned heatsink lumped-η model
option_C_padcase.py / json / csv — pad + case Rth network
out_A/ out_B/ out_C/       — per-option raw FEM artifact dirs
                             (mesh, STL, STEP, upduino_enclosure_thermal_*.json)
```

## Verdict

G5 scope_caveat #3 ("single thermal load case") **partially closed**:
the single 1 W load now has three design-validated mitigation paths
with FEM + 1D analytic cross-check. Multi-load sweep + measured-h
wind-tunnel + bench IR cross-check remain GATE_OPEN for full closure.
