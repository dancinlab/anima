# CsOs2O6 QE deck (RTSC_28) — non-magnetic β-pyrochlore flat-band ΔE

Real Quantum ESPRESSO (QE 7.5, PBE) deck for the **second pick** of the RTSC_28
flat-band-at-E_F screen: the **non-magnetic, ambient-pressure β-pyrochlore
superconductor CsOs2O6** (Tc ≈ 3.3 K, ambient — Yonezawa+ JPSJ 2004). The
A-site (Cs) sibling of RbOs2O6 — a built-in A-cation control: same Os-pyrochlore
flat-band net, larger rattling cage, lets the next fire test how the A-site
shifts ΔE_flat.

## Why this candidate (RTSC_28 screen result)
Same rationale as the RbOs2O6 deck (see `../rbos2o6/README.md`): the RTSC_28
MP-API screen (metallic ∧ non-magnetic ∧ ambient-stable, over flat-band-prone
families) ranked **CsOs2O6** alongside RbOs2O6 at the top — MP
total_magnetization ≈ 0 (mp-aaabfwkk), energy_above_hull = 0.0000 eV/atom
(ambient-stable), Fd-3m β-pyrochlore. CoSn (ΔE=−0.44, magnetic) and CsV3Sb5
(ΔE=+0.92) both already failed the ΔE axis; the pyrochlore osmates are the
clean, ambient, non-magnetic frontier (RTSC_16). Open question = **ΔE_flat**.

## Status — 🟠 DEFERRED (deck built; SCF not run — needs a free QE host)
Deliverable only ($0 screen + decks). Run on **aiden** (summer saturated) —
ONE QE job at a time; do NOT disturb tenants (bitcoind / milksad / python3).

## Structure (Fd-3m, #227, β-pyrochlore AB2O6 — origin choice 2)
- FCC primitive cell (ibrav=2), **1 formula unit = 9 atoms** (Cs·Os2·O6).
- celldm(1) = **19.2582 Bohr** (= conventional cubic a ≈ 10.191 Å; expt a ≈
  10.155 Å — PBE slightly overestimates, expected).
- Wyckoff: **Cs 8b** (3/8,3/8,3/8); **Os 16c** (0,0,0); **O 48f** (x,1/8,1/8)
  x ≈ 0.315 — transformed into the FCC primitive basis (QE ibrav=2 convention),
  computed not guessed (identical site set to RbOs2O6, A=Cs).

## Pseudopotentials (PSLibrary 1.0.0, PBE, scalar-relativistic USPP/RRKJUS)
- `Cs.pbe-spn-rrkjus_psl.1.0.0.UPF` (z=9; **use `spn`, NOT the corrupt-header
  `spnl` variant** — RTSC_26 hit z_valence parsed as −5.0 on the spnl Cs).
- `Os.pbe-spn-rrkjus_psl.1.0.0.UPF` (5d6s — the flat-band orbital).
- `O.pbe-n-rrkjus_psl.1.0.0.UPF` (2s2p).
- Download base: `https://pseudopotentials.quantum-espresso.org/upf_files/`.

## Cutoffs
- ecutwfc = 70 Ry, ecutrho = 560 Ry (8×). Converge a cutoff ladder before ΔE.

## Files
- `scf.in`  — SCF (nspin=1; MP smearing degauss 0.02; K 8×8×8; local-TF mixing).
- `bands.in` — bands along the FCC path **Γ–X–W–K–Γ–L–W**, nbnd=90.

## To run (on aiden — ONE QE job at a time; do not disturb tenants)
```
cd ~/rtsc_csos2o6
export OMP_NUM_THREADS=1
micromamba run -n qe mpirun -np 4 pw.x -i scf.in  > scf.out 2>&1
micromamba run -n qe mpirun -np 4 pw.x -i bands.in > bands.out 2>&1
# bands.x + projwfc.x -> Os-5d flat manifold; ΔE_flat = E_flat_center − E_Fermi
```

## Expected analysis (fill once SCF runs)
- Confirm non-magnetic (nspin=1; honest = a spin-seeded nspin=2 collapse test).
- Os-5d t2g flat manifold center vs E_F → **ΔE_flat** (sign + width).
- A-site comparison: ΔE_flat(Cs) vs ΔE_flat(Rb) — does the larger Cs cage push
  the flat band toward E_F? (the screen's design hope; the Tc ordering
  KOs2O6>RbOs2O6>CsOs2O6 hints the A-site tunes the electronic structure).

## Provenance / grade
- structure / magnetism / stability: 🟡 (Materials Project mp-aaabfwkk, live) +
  literature (Yonezawa+ 2004).
- flat-band ΔE: 🟠 **needs this DFT**.
