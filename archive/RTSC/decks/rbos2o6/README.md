# RbOs2O6 QE deck (RTSC_28) — non-magnetic β-pyrochlore flat-band ΔE

Real Quantum ESPRESSO (QE 7.5, PBE) deck for the **top pick** of the RTSC_28
flat-band-at-E_F screen: the **non-magnetic, ambient-pressure β-pyrochlore
superconductor RbOs2O6** (Tc ≈ 6.3 K, ambient — Yonezawa+ JPSJ 2004).

## Why this candidate (RTSC_28 screen result)
Two real kagome metals already failed under real QE DFT:
- CoSn (RTSC_21): flat band **ΔE = −0.44 eV** (far below E_F) **and magnetic** (0.43 μB).
- CsV3Sb5 (RTSC_26): flat band **ΔE = +0.92 eV** (far above E_F), non-magnetic.

Both fail on ΔE (flat band too far from E_F) ± magnetism. The RTSC_28 MP-API
screen (metallic ∧ non-magnetic ∧ ambient-stable, over flat-band-prone
families beyond Fe/Mn/Co) ranked the **β-pyrochlore osmates RbOs2O6 / CsOs2O6**
top: both **non-magnetic** (MP total_magnetization ≈ 0) and **on the convex
hull** (energy_above_hull = 0.0000 eV/atom → ambient-stable), in the
**pyrochlore** family that RTSC_16 flagged as the room-temp flat-band frontier
(multi-orbital ⟨g⟩ ≫ kagome). The Os-5d pyrochlore (corner-sharing tetrahedra)
hosts frustration-driven flat-ish bands; the open question this deck answers is
**the flat-band ΔE to E_F** (the lever the campaign is missing).

## Status — 🟠 DEFERRED (deck built; SCF not run — needs a free QE host)
This is the deliverable: a ready-to-fire deck so the next real QE fire hits a
non-magnetic, ambient, flat-band-prone candidate. Not run here ($0 screen +
decks only). Run on **aiden** (summer is saturated) — ONE QE job at a time;
do NOT disturb aiden's tenants (bitcoind / milksad / python3).

## Structure (Fd-3m, #227, β-pyrochlore AB2O6 — origin choice 2)
- FCC primitive cell (ibrav=2), **1 formula unit = 9 atoms** (Rb·Os2·O6).
- celldm(1) = **19.1845 Bohr** (= conventional cubic a ≈ 10.152 Å; expt a ≈
  10.114 Å, Rb β-pyrochlore — PBE slightly overestimates, expected).
- Wyckoff: **Rb 8b** (3/8,3/8,3/8); **Os 16c** (0,0,0); **O 48f** (x,1/8,1/8)
  with x ≈ 0.315. The ATOMIC_POSITIONS are these Wyckoff sites transformed into
  the FCC **primitive** basis (QE ibrav=2 convention a1=a/2(−1,0,1), a2=a/2(0,1,1),
  a3=a/2(−1,1,0)) — computed, not guessed.
- Os forms the corner-sharing-tetrahedra **pyrochlore net** (the flat-band lattice);
  Rb "rattles" in the oversized cage (the famous β-pyrochlore rattling mode).

## Pseudopotentials (PSLibrary 1.0.0, PBE, scalar-relativistic USPP/RRKJUS)
- `Rb.pbe-spn-rrkjus_psl.1.0.0.UPF` (semicore s/p).
- `Os.pbe-spn-rrkjus_psl.1.0.0.UPF` (5d6s + semicore p). **Os-5d is the flat-band
  orbital** — do not under-converge ecutrho.
- `O.pbe-n-rrkjus_psl.1.0.0.UPF` (2s2p).
- Download base: `https://pseudopotentials.quantum-espresso.org/upf_files/`.
- ⚠ Verify each UPF header z_valence on download (the csv3sb5 deck hit a
  corrupt-header Cs variant — RTSC_26). If `Os.pbe-spn` is unavailable, the
  `Os.pbe-spfn` / SG15 ONCV Os is an acceptable substitute (re-tune cutoffs).

## Cutoffs
- ecutwfc = 70 Ry, ecutrho = 560 Ry (8×). Os-5d + O-2p USPP — converge a
  cutoff ladder (60/65/70 wfc) on the SCF energy before trusting ΔE.

## Files
- `scf.in`  — SCF (nspin=1; MP smearing degauss 0.02; K 8×8×8; local-TF mixing).
- `bands.in` — bands along the FCC path **Γ–X–W–K–Γ–L–W**, nbnd=90 (enough to
  span the Os-5d manifold + O-2p; flat band sits within the 5d manifold).

## To run (on aiden — ONE QE job at a time; do not disturb tenants)
```
cd ~/rtsc_rbos2o6            # stage scf.in, bands.in, pseudo/ here
export OMP_NUM_THREADS=1
micromamba run -n qe mpirun -np 4 pw.x -i scf.in  > scf.out 2>&1   # E_Fermi, mag
micromamba run -n qe mpirun -np 4 pw.x -i bands.in > bands.out 2>&1 # bands
# then bands.x + projwfc.x to find the low-dispersion Os-5d (t2g) flat manifold
# ΔE_flat = E_flat_center − E_Fermi   (sign + magnitude vs CoSn −0.44 / CsV3Sb5 +0.92)
```

## Expected analysis (fill once SCF runs)
- Confirm total magnetization ≈ 0 (non-magnetic — MP proxy says yes; a real
  **nspin=2** spin-seeded test is the honest confirmation, cf RTSC_26 where a
  forced 2.8 μB seed collapsed to 0.01 μB).
- Identify the Os-5d t2g flat manifold (low dispersion across the full FCC path),
  measure its center vs E_F → **ΔE_flat** (sign + width) via projwfc.x weights.
- The screen's hope: a pyrochlore multi-orbital flat band closer to E_F than
  CoSn (−0.44) or CsV3Sb5 (+0.92). If |ΔE| ≲ 0.1 eV and non-magnetic confirmed,
  this becomes the cleanest RTSC base yet → then DFPT λ/Tc.
- Honest: this is the **high-T undistorted** β-pyrochlore; RbOs2O6 has a known
  structural transition / rattling anharmonicity — PBE here gives the ideal
  Fd-3m flat-band position, a screening estimate, not the final word.

## Provenance / grade
- structure + lattice + magnetism + ambient-stability: 🟡 (Materials Project
  mp-aaaaahmg, live query) + literature (Yonezawa+ 2004).
- flat-band ΔE: 🟠 **needs this DFT** — that is the entire point of this deck.
