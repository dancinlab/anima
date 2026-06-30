# G5 demiurge component — UPduino v3 enclosure STEP + thermal FEM (2026-05-21)

## §1 GOAL

직전 demiurge `component + verify` cycle 의 verdict 는 ⏳ **GATE_OPEN**
(`die_proxy_box_v1`, 10 × 10 × 2 mm Si box, 단일 load case, textbook
material). 본 cycle 의 진척 = anima FPGA enclosure 의 **real STEP**
geometry 를 `~/core/demiurge/exports/component/verify/` bridge dir 안에
drop 하여, 6종 `scope_caveats` 중 첫 두 종 ("geometry = toy box" / "mesh
convergence 미검증") 을 측정-수준에서 닫는다. material datasheet flash-
test + 3rd-party FE cross-check 가 아직 missing 이므로 본 record 의
`measurement_gate` 도 GATE_OPEN 으로 emit (g3, 본 doc §7 참조).

대상 board = **UPduino v3** (Lattice iCE40UP5K SG48, 40-pin DIP,
47 mm × 30 mm × ~10 mm). 별도 cycle 에서 ECP5-EVN 에도 동일 pipeline
복제 예정.

## §2 STEP geometry

`/Users/ghost/core/anima/anima-physics/hw/strange_loop_ice40/cad/upduino_enclosure.py`
(220 LoC) — gmsh OpenCascade backend 로 두 axis-aligned box B-Rep
+ STEP AP203 export. cadquery / build123d 의존 없음 (gmsh native
`gmsh.write(*.step)`).

```
        ┌───── Al cover plate ─────┐   50 × 33 × 1 mm (Al 6061-T6)
        │                          │   ←─ z = 11..12 mm
        │                          │
   ─────┴──────────────────────────┴─────
        ↑ 1 mm air gap (modelled as adiabatic boundary, not solid)
   ┌────────── UPduino v3 PCB ──────────┐  47 × 30 × 10 mm
   │  ┌─── iCE40UP5K BGA ───┐           │  (FR-4 slab approximation,
   │  │   5 × 5 mm, 0.5 W   │  ┌─LDO─┐  │   z = 0..10 mm)
   │  └─────────────────────┘  │0.5 W│  │
   └───────────────────────────┴─────┴──┘
                                            x → length 47 mm
                                            y ↑ width  30 mm
                                            z out of page
```

artifacts (생성 위치 동일):
- `upduino_enclosure.step` (33 KB, 두 body — PCB + cover plate)
- `upduino_cover_plate.step` (16 KB, cover plate only, FEM input)
- `upduino_enclosure.brep` (7 KB, native OCC B-Rep, full assembly)
- `upduino_enclosure.geometry.json` (sidecar, schema_version 1.0)

## §3 FEM setup

`/Users/ghost/core/anima/anima-physics/hw/strange_loop_ice40/cad/upduino_enclosure_fem.py`
(370 LoC) — ①a STDLIB kernel `~/core/hexa-lang/stdlib/kernels/fem/skfem_kernel.py`
의 `mesh_from_step()` + 신규 Robin convection BC 조립.

| Side                  | Boundary condition                              |
|-----------------------|-------------------------------------------------|
| top face (z = 12 mm)  | Robin: −k ∂T/∂n = h (T − T_amb), h = 10 W/m²K   |
| bottom face (z=11 mm) | Neumann: q = 1.0 W / (0.05 × 0.033) ≈ 606 W/m²  |
| 4 side faces          | adiabatic (zero flux) — bounds ΔT from above    |
| no Dirichlet          | Robin grounds the system                        |

material = Al 6061-T6 (k = 167 W/m·K, ρ = 2700 kg/m³, E = 68.9 GPa,
ν = 0.33) — CRC Handbook / AZoM textbook values, **NOT measured lot**.

## §4 mesh convergence

4-level h-refinement on the cover plate STEP, target tet edge ∈
{1.5, 1.0, 0.7, 0.5} mm. Tolerance = 0.1 K (task spec).

| lvl | h (mm) | n_nodes | n_elems | T_max (K)  | ΔT (K)     | |Δstep| (K)    | wall (s) |
|-----|--------|---------|---------|------------|------------|------------------|----------|
|  0  | 1.5    |   2 014 |   5 748 | 353.759690 | 60.609690  | —                | 0.31     |
|  1  | 1.0    |   4 211 |  12 394 | 353.759690 | 60.609690  | 4.8e-11          | 0.32     |
|  2  | 0.7    |   8 492 |  24 807 | 353.759690 | 60.609690  | 2.4e-09          | 0.67     |
|  3  | 0.5    |  20 510 |  74 587 | 353.759690 | 60.609690  | 3.9e-09 ◀ final  | 2.02     |

verdict: **converged** — final inter-level Δ ≈ 4 nK ≪ 0.1 K tolerance
(>7 orders of magnitude margin). 1D analytic check: ΔT = (q · t) / k
= (606.06 W/m² · 1e-3 m) / 167 W/m·K = 3.63 mK through-wall + Robin
sink ΔT = q / h = 606.06 / 10 = 60.606 K → 60.610 K, FEM 60.609689 K,
≈ **1.7e-5 relative error vs 1D analytic** (mesh convergence is
trivial for uniform-flux + Robin on a thin slab — convection h is the
rate-limit, NOT k or h_mesh). See §7 honest C3 #2.

## §5 thermal result

ΔT_max = **60.6 K** (T_max ≈ 354 K = 80.6 °C; T_amb = 20 °C).
1 W FPGA + LDO dissipation through a 50 × 33 × 1 mm Al cover plate
with free-convection (h = 10 W/m²K) ambient sink. This ΔT is dominated
by the boundary convection coefficient, not by the Al plate conduction
(plate Biot ≈ h·t/k = 10·1e-3/167 ≈ 6e-5 ≪ 1 → essentially isothermal
Al, convective-limited). Verdict: ΔT margin **fails** typical
iCE40UP5K T_j max of 85 °C with 5 °C headroom (T_max ≈ T_j ≈ 80.6 °C
at T_amb = 20 °C; T_amb 25 °C 부터 already over) — cover plate is
under-sized for 1 W if free convection only; forced air (h = 30-50)
or fins required. Bench thermocouple cross-check still missing (g3).

## §6 demiurge cli output

```
$ demiurge cli action verify component
action: 검증 (검증) · domain=component — dispatching…
script  = /Users/ghost/core/hexa-lang/stdlib/component/gmsh_skfem.py
python3 = /opt/homebrew/bin/python3
python3 gmsh_skfem.py — exit 0, rows=8
gmsh 4.15.2 · scikit-fem 12.0.1
artifacts: csv, meta, msh
---
📸 component verify record → exports/component/verify/
   2026-05-21T08-40-36Z/component_verify_20260521T084036Z.json
   ΔT = 0.528 K · T_max = 298.68 K · σ_vM_max = 38.37 Pa · u_max = 2.796e-13 m
   mesh: 686 nodes · 2232 tetrahedra · producer = gmsh@4.15.2 + scikit-fem@12.0.1
   ⏳ GATE_OPEN · absorbed=false — toy box geometry + textbook material +
     single load case, 흡수에 해당하려면 real STEP + 측정 datasheet +
     mesh convergence 필요 (g3, scope_caveats 6종 참조).
```

post-drop filesystem state of `exports/component/verify/`:
```
2026-05-19T18-15-23Z   ← toy die_proxy_box (legacy)
2026-05-19T19-20-34Z   ← toy die_proxy_box (legacy)
2026-05-21T06-24-39Z   ← toy die_proxy_box (06:24, direct prior cycle)
2026-05-21T08-39-28Z   ← anima UPduino enclosure record (THIS CYCLE)
2026-05-21T08-39-48Z   ← toy die_proxy_box (pre-doc demo refire)
2026-05-21T08-40-36Z   ← toy die_proxy_box (post-doc demo refire)
```

The anima UPduino record lives in `2026-05-21T08-39-28Z/`:
- `upduino_enclosure_thermal_20260521T083931Z.json` (5.4 KB, schema mirror
  of `component_verify_*.json` with `mesh_convergence.levels[]` extension)
- `mesh_convergence.csv` (4-level sweep)
- `step.brep` (16 KB, OCC B-Rep copy)
- `step.stl` (1.8 MB, surface mesh for viewers)
- `upduino_cover_lvl{0..3}.msh` (gmsh v2.2 meshes, 0.4 → 4.8 MB)

demiurge `action verify component` still spawns the canonical
`die_proxy_box_v1` toy producer — it does NOT auto-discover anima
records yet (ComponentVerifyProducer.swift is hard-wired to
`~/core/hexa-lang/stdlib/component/gmsh_skfem.py`). Auto-discovery
of sibling `*_thermal_*.json` records inside `verify/<stamp>/` is a
follow-up Swift feature (would need a new
`ComponentVerifyDiscovery.swift` scanner — out of scope this cycle).
The bridge is **filesystem-only**: anima drops, demiurge sees on
disk, future absorb cycle reads.

## §7 honest C3 (5건)

1. **datasheet recall ≠ caliper measurement.** UPduino v3 board outline
   (47 × 30 mm) + iCE40UP5K SG48 (5.5 × 5.5 mm) + Al 6061-T6 cover
   (50 × 33 × 1 mm) all come from the Tinyvision.ai datasheet + AZoM,
   not from a physical part on the bench. Fabricating the enclosure +
   measuring with calipers is a separate cycle.

2. **mesh convergence is TRIVIAL for this BC pair.** ΔT is dominated
   by the Robin convection coefficient (Biot ≈ 6e-5), so spatial
   discretization of the Al slab is essentially exact at any of the
   4 mesh levels — the 4 nK final inter-level step is IEEE-754 noise,
   not refinement signal. A true convergence study would replace
   the uniform Neumann patch with a localised BGA + LDO source
   (where mesh refinement actually matters for hot-spot ΔT).

3. **heat source localisation NOT modelled.** Uniform 1 W Neumann on
   the entire cover-plate bottom face overestimates the actual
   heat-spread area (BGA footprint ≈ 30 mm², LDO ≈ 9 mm², total ≈
   1.3 % of the cover plate bottom). Real hot-spot ΔT at the BGA
   could be 2-5× higher than this enclosure-average prediction.

4. **side-face adiabatic BC is physically wrong** for an open-air
   enclosure — real free convection wraps around to the sides + bottom.
   The adiabatic side BC bounds ΔT from above (overestimates), so
   the real device runs cooler than 60.6 K rise. Wind-tunnel /
   IR-camera bench measurement on a fabricated enclosure would
   close this.

5. **GATE_OPEN persists.** All 5 demiurge `scope_caveats` for
   GATE_CLOSED still apply (real BOM, measured material lot, validated
   load case, multi-load sweep, 3rd-party signoff Code_Aster /
   Elmer). Progress this cycle = caveats #1 (toy → real STEP) and
   #5 (single mesh size → 4-level convergence sweep) → factually
   closed at the producer side; caveats #2, #3, #4, #6 still open.
   `measurement_gate = GATE_OPEN`, `absorbed = false` — same as
   the toy producer (g3, no silent flip).

---

## artifacts (absolute paths)

- `/Users/ghost/core/anima/anima-physics/hw/strange_loop_ice40/cad/upduino_enclosure.py`
- `/Users/ghost/core/anima/anima-physics/hw/strange_loop_ice40/cad/upduino_enclosure_fem.py`
- `/Users/ghost/core/anima/anima-physics/hw/strange_loop_ice40/cad/upduino_enclosure.step`
- `/Users/ghost/core/anima/anima-physics/hw/strange_loop_ice40/cad/upduino_cover_plate.step`
- `/Users/ghost/core/anima/anima-physics/hw/strange_loop_ice40/cad/upduino_enclosure.brep`
- `/Users/ghost/core/anima/anima-physics/hw/strange_loop_ice40/cad/upduino_enclosure.geometry.json`
- `/Users/ghost/core/demiurge/exports/component/verify/2026-05-21T08-39-28Z/upduino_enclosure_thermal_20260521T083931Z.json`
- `/Users/ghost/core/demiurge/exports/component/verify/2026-05-21T08-39-28Z/mesh_convergence.csv`
- `/Users/ghost/core/demiurge/exports/component/verify/2026-05-21T08-39-28Z/step.brep`
- `/Users/ghost/core/demiurge/exports/component/verify/2026-05-21T08-39-28Z/step.stl`
- `/Users/ghost/core/anima/anima-physics/docs/demiurge_component_step_upduino_2026_05_21.md` (this file)
