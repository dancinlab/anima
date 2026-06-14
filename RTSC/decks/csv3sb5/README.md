# CsV3Sb5 QE deck (RTSC_26) — non-magnetic kagome flat-band ΔE

Real Quantum ESPRESSO (QE 7.5, PBE) deck to measure whether the **non-magnetic**
kagome superconductor CsV3Sb5 has its V-kagome flat band **shallower** to E_F than
CoSn's (RTSC_21: CoSn ΔE = −0.44 eV below E_F, and CoSn turned out magnetic — both
disqualify it). CsV3Sb5 fixes CoSn's magnetism defect (nspin=1); the open question
is the flat-band ΔE.

## Status — 🟠 DEFERRED (deck built + validated; SCF not run)
The SCF/bands run was **NOT** completed: summer was continuously oversubscribed
(load 60–72 on 12 cores) by an **independent, pre-existing CoSn QE `nscf` bands job**
(another RTSC session) plus other heavy tenants (a 621% python verify, 2×
`test_array_methods`, the rbfe co-tenant). HARD CONSTRAINT = run only ONE QE job at a
time (oversubscription starves jobs) and do NOT thrash. The deck is fully built and
QE-input-validated (see below); it is one command away from running once summer frees.

## Structure (hexagonal P6/mmm, #191)
- a = 5.45 Å, c = 9.31 Å (experimental).
- Cs 1a (0,0,0); V 3g (1/2,0,1/2) — kagome net at z=1/2; Sb1 1b (0,0,1/2);
  Sb2 4h (1/3,2/3,z) with z≈0.74 (honeycomb above/below the V-kagome plane).
- 9 atoms/cell, 73 valence e⁻ (Cs 9 + 3×V 13 + 5×Sb 5). nspin=1 (non-magnetic — the
  key contrast vs CoSn's nspin=2 / mag 0.43 μB).

## Pseudopotentials (PSLibrary 1.0.0, PBE, scalar-relativistic USPP/RRKJUS)
- `Cs.pbe-spn-rrkjus_psl.1.0.0.UPF` (z=9). NOTE: the `spnl` (f-semicore) Cs variant
  on the official site has a **corrupt header** (z_valence parsed as −5.0); use `spn`.
- `V.pbe-spnl-rrkjus_psl.1.0.0.UPF` (z=13; 3s3p semicore + 3d4s). Suggested rho cutoff
  = **645 Ry** (hard, V-3d ultrasoft) — this sets ecutrho.
- `Sb.pbe-n-rrkjus_psl.1.0.0.UPF` (z=5; 5s5p).
- Download base: `https://pseudopotentials.quantum-espresso.org/upf_files/`.

## Cutoffs
- ecutwfc = 65 Ry, ecutrho = 650 Ry. ecutrho is set by V's hard 645 Ry rho
  requirement (USPP V-3d) — cutting it lower would corrupt the very flat band being
  measured. Heavier than 8×wfc, but required for correctness.

## Files
- `scf.in`  — SCF (nspin=1, MP smearing degauss 0.02, K 12×12×6, local-TF mixing).
              Validated: pw.x reads it cleanly — "number of atoms/cell = 9",
              "number of electrons = 73.00", ibrav=4, "24 Sym. Ops., with inversion".
- `bands.in` — bands along Γ–M–K–Γ–A–L–H–A (kagome flat-band momenta), nbnd=60.

## To run (on summer, when load is clear — ONE QE job at a time)
```
cd ~/rtsc_csv3sb5            # stage scf.in, bands.in, pseudo/ here
export OMP_NUM_THREADS=1
micromamba run -n qe mpirun -np 4 pw.x -i scf.in  > scf.out 2>&1   # SCF: E_Fermi, mag(≈0)
micromamba run -n qe mpirun -np 4 pw.x -i bands.in > bands.out 2>&1 # bands
# then bands.x to extract eigenvalues; find the low-dispersion V-3d (xy/x²−y²) manifold
# ΔE_flat = E_flat_center − E_Fermi  (sign + magnitude vs CoSn's −0.44 eV)
```

## Expected analysis (to fill once SCF runs)
- Confirm total magnetization ≈ 0 (non-magnetic — fixes CoSn defect).
- Identify V-kagome flat band (low dispersion across full path incl Γ–A), measure its
  center vs E_F → ΔE_flat (with sign) and dispersion width.
- Compare to CoSn (ΔE = −0.44 eV): is |ΔE| < 0.44 eV (shallower)? Which side of E_F?
- Caveat: CsV3Sb5 has a ~94 K CDW that gaps part of the Fermi surface — PBE here is
  the high-T undistorted P6/mmm cell (no CDW superstructure), so ΔE is the parent-phase
  flat-band position.
