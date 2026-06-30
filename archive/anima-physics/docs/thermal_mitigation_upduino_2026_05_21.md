# UPduino enclosure thermal mitigation — 3-option FEM (2026-05-21)

## §1 GOAL

직전 G5 demiurge component cycle (`upduino_enclosure_fem.py`, commit
`6ea299145`, doc `docs/demiurge_component_step_upduino_2026_05_21.md`)
는 UPduino v3 + 1 mm Al cover plate enclosure 의 FEM 을 돌려서
**ΔT_max = 60.61 K, T_max = 80.6 °C** (T_amb = 20 °C, P_total = 1 W,
h = 10 W/m²K free convection) 를 보고했다. iCE40UP5K SG48 의 datasheet
T_j,max = 85 °C 대비 **headroom = 4.4 °C 단**, 한자릿수 마진은 product-
grade 양산 enclosure 로 허용 불가 (PE-spec deratings 통상 ≥ 20 °C).

본 cycle = 3가지 mitigation alternative 의 FEM 재실행 + 1D 해석적
cross-check + BOM trade-off matrix. 목표 headroom **≥ 20 °C**.

artifacts root:
- `/Users/ghost/core/anima/anima-physics/hw/strange_loop_ice40/cad/thermal_mitigation_2026_05_21/`

## §2 3 options + parameter

### A — 40 mm DC axial fan (forced air)

```
         ┌─── 40 mm fan ──┐         ←── 5 V axial fan (Noctua-class)
         │ ▼ ▼ ▼ airflow  │             $5 BOM, h = 50 W/m²K
         └────────────────┘
   ┌─── Al cover plate ──┐  ←── 50×33×1 mm, geometry unchanged
   │  iCE40 + LDO (1 W)  │
```

BC change = `LOAD["h_convection_w_per_m2k"]: 10 → 50` (5× textbook
forced-air on Al, NOT wind-tunnel measured). Geometry, mesh, material
unchanged from baseline.

### B — Finned heatsink (passive, free convection)

```
   ╱╲╱╲╱╲╱╲╱╲╱╲                      ←── 6 fins × 25 L × 10 H × 1 t mm
   │ │ │ │ │ │ │                         (Al 6061 extrusion, $3 BOM)
   ─┴─┴─┴─┴─┴─┴─                      ←── thermal epoxy bond to cover
   ┌─── Al cover plate ──┐
   │  iCE40 + LDO (1 W)  │
```

Lumped to h_eff via Incropera fin-efficiency model (Ch. 3.6):

| param                       | value     |
|-----------------------------|-----------|
| A_base (50×33)              | 1650 mm²  |
| A_fin_each (2·25·10 + 25·1) | 525 mm²   |
| A_fin_total (×6)            | 3150 mm²  |
| A_unfin_base                | 1500 mm²  |
| A_eff                       | 4650 mm²  |
| area_ratio                  | 2.82      |
| fin efficiency η            | 0.9960    |
| h_eff = h·(A_unfin + η·A_fin)/A_top | **28.11 W/m²K** |

### C — Thermal pad + Al outer case (chip → case → ambient, 2-stage Rth)

```
   ┌── 100×80×25 mm Hammond Al case (1.5 mm wall) ──┐
   │                                                │
   │  ┌── Sil-Pad 900S ($2, k=1.6) ──┐              │  ←── case h_outer=8
   │  │  iCE40UP5K BGA top (5×5 mm)  │              │      A_case=0.025 m²
   │  └───────────────────────────────┘              │
   └────────────────────────────────────────────────┘
```

Lumped Rth network (chip → ambient):
- R_pad = t_pad / (k_pad · A_pad) = 1e-3 / (1.6 · 25e-6) = **25.0 K/W** (dominant)
- R_conv_case = 1 / (h · A) = 1 / (8 · 0.025) = **5.0 K/W**
- R_cover = negligible (Al, 1.5 mm)
- R_total = 30.0 K/W → ΔT @ 1 W = **30.0 K**

FEM leg = case-convection only (h_lumped = h_case · A_case / A_top
= 8 · 0.025 / 1.65e-3 = 121.2 W/m²K on the cover-plate domain). Pad
film added analytically.

## §3 FEM result table

(All runs: gmsh 4.15.2 + scikit-fem 12.0.1, Python 3.14.4, 4-level
mesh convergence 1.5 → 0.5 mm tet edge, converged < 0.1 K tolerance,
absolute paths in `/Users/ghost/core/anima/anima-physics/hw/strange_loop_ice40/cad/thermal_mitigation_2026_05_21/`.)

| Option              | h_eff (W/m²K) | ΔT_FEM (K) | T_max (°C) | Headroom (°C) | BOM ($) | meets ≥ 20 °C |
|---------------------|---------------|------------|------------|---------------|---------|---------------|
| baseline            |  10.0         | 60.610     | 80.61      |  4.39         |   0     | ✗             |
| **A — fan**         |  50.0         | 12.125     | 32.12      | **52.88**     |   5     | ✓ (best)      |
| **B — finned**      |  28.1         | 21.567     | 41.57      | **43.43**     |   3     | ✓             |
| **C — pad+case**    | 121.2 + R_pad | 30.004*    | 50.00      | **35.00**     |  17     | ✓             |

\* C row = FEM 5.00 K (case leg) + 25.00 K analytic pad film.

mesh convergence: all 3 options converged below 0.1 K tolerance at the
finest level (final inter-level Δ ≈ 1e-11 K — convection-limited Biot
regime, mesh-independence trivial as in baseline).

## §4 1D analytic verify (per option)

formula: ΔT_max = q · t / k (through-Al) + q / h (Newton sink)
where q = P / A_top = 1.0 / (0.05 · 0.033) = 606.06 W/m²

| Option         | ΔT_wall (mK) | ΔT_robin (K) | ΔT_total (K) | FEM (K)  | rel. err   |
|----------------|--------------|--------------|--------------|----------|------------|
| A — fan        | 3.63         | 12.121       | 12.125       | 12.125   | 7.2e-12    |
| B — finned     | 3.63         | 21.563       | 21.567       | 21.567   | 1.7e-12    |
| C — FEM leg    | 3.63         |  5.000       |  5.004       |  5.004   | 1.5e-11    |
| C — total      | (FEM leg)    | (+25.0 pad)  | 30.004       | 30.004†  | (lumped Rth) |

† C-total combines FEM case leg + analytic pad film; the FEM leg
agrees with its 1D analog to 1.5e-11 rel. err.

All FEM↔analytic rel. errors < 1e-11 — machine precision. The
convection-limited Biot regime (Bi = h·L/k ≈ 6e-5) means the mesh
captures the analytic answer essentially exactly; the FEM exists as
a self-checking consistency probe for the 1D formula (and as the
foundation for future multi-load / transient / structural sweeps).

## §5 Recommendation (BOM vs headroom)

```
headroom °C
    ▲
 60 │              ★ A (fan)              ← largest headroom, active
 50 │         ★ B (finned)                ← best passive trade-off
 40 │                ★ C (pad+case)       ← when case is required anyway
 30 │
 20 │ ─────── ≥20 °C derating floor ─────
 10 │
  4 │ ★ baseline                          ← unacceptable
    └────────────────────────────────────►  BOM $
      $0    $3       $5         $17
```

**Recommendation = Option B (finned heatsink, passive, $3 BOM,
43 °C headroom)** as the default. Reasoning:
1. Passive (no fan failure mode, no audible noise, no auxiliary power).
2. 43 °C headroom comfortably exceeds the 20 °C derating floor.
3. Lowest BOM that meets the spec.
4. Drop-in on the existing cover-plate geometry — no enclosure redesign.

**Use Option A** only if board operates in T_amb > 50 °C ambient
(automotive cabin / industrial control) where the extra 10 °C margin
matters.

**Use Option C** only when an outer Al enclosure is independently
required (IP-rating, RFI shielding, structural protection). Note its
35 °C headroom is pad-resistance-limited; a Bergquist TSP-A2000 pad
(k = 6.5 W/m·K) would cut R_pad from 25 to 6.2 K/W and lift headroom
to ~50 °C for an additional ~$3 BOM.

## §6 Honest C3

1. **Convection h values are textbook, not measured.** h = 10 (free),
   50 (forced-fan), 8 (mixed-orient case), 28.1 (lumped fin) are
   Incropera / Holman / CRC handbook values. Real fan curve,
   back-pressure, ambient airflow, surface roughness can shift h by
   ±30 %. GATE_CLOSED requires wind-tunnel or fan-curve datasheet
   + IR-camera bench measurement.
2. **Fin model is lumped η, not literal 3D mesh.** Option B collapses
   the 6 × 25 × 10 mm fins into an equivalent h_eff via the Incropera
   fin-efficiency closed form. A literal multi-body FEM (cover plate
   + 6 fins as separate B-Rep bodies) would double mesh size; the
   η = 0.996 result bounds the lumping error at < 1 % (Al at 1 mm
   thickness with H=10 mm is near-isothermal — fin is the textbook
   ideal case).
3. **Option C's Rth network is lumped, not coupled-FEM.** The pad +
   chip + case + ambient resistance chain is modelled as four
   series resistors. A true coupled-body FEM would resolve spreading
   effects (chip BGA → pad → case wall lateral conduction). The
   lumped model is conservative for the pad leg (no lateral spreading
   credit) and accurate for the case-convection leg (FEM cross-check
   rel. err 1.5e-11).
4. **Single steady-state 1 W load.** G5 scope_caveat #3 multi-load
   sweep (P_burst = 2 W during CLB activity surge, transient warm-up
   τ ≈ 30 s for the Al cover plate) is NOT modelled. Linear scaling
   would give Option A peak ΔT ≈ 24 K (headroom 41 °C — still safe),
   Option B peak ΔT ≈ 43 K (headroom 22 °C — at the floor), Option C
   peak ΔT ≈ 60 K (headroom 5 °C — fails). Multi-load deratings to
   be added in a follow-up cycle.
5. **measurement_gate = GATE_OPEN.** All three records produced by
   this cycle carry the same `GATE_OPEN / absorbed = false`
   provenance as the baseline. GATE_CLOSED requires (a) real BOM
   procurement, (b) fabricated enclosures, (c) bench IR + thermocouple
   measurement under each cooling configuration, (d) 3rd-party FE
   cross-check (Code_Aster or Elmer). This cycle closes scope_caveat
   #3 at the DESIGN level only (alternatives exist + are FEM-verified
   to 1e-11 precision), not at the MEASUREMENT level.

## §7 Cycle status

- G5 component scope_caveats:
  - #1 (toy geometry) — closed prior cycle (real STEP cover plate)
  - #2 (textbook material) — still GATE_OPEN (datasheet flash-test
    + Hot Disk pending)
  - **#3 (single thermal load alternative) — PARTIALLY CLOSED this
    cycle: 3 mitigation paths design-validated to 1e-11 rel. err,
    multi-load transient sweep still GATE_OPEN**
  - #4 (textbook h = 10) — REPLACED by 4 h values across options
    (10, 28.1, 50, 121.2) all still textbook — wind-tunnel measurement
    pending
  - #5 (GATE_OPEN) — unchanged
- artifacts: 3 × (py + json + csv) + comparison.md + this doc
- FEM cost: $0 Mac local, wall ≈ 12 s total across 3 options (gmsh
  + skfem 4-level mesh sweep each, all converged finest 0.5 mm edge)
- next cycle candidate: (a) multi-load transient sweep (peak 2 W /
  duty cycle 0.5), (b) wind-tunnel h-measurement bench for Option A,
  (c) 3rd-party Elmer FEM cross-check for one option.
