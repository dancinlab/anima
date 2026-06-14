---
id: RTSC_24
slug: cosn-doping
title: CoSn rigid-band hole-doping sweep — x ~ 4.7 e/cell pulls E_F onto the Co-kagome flat band, N(E_F) x3.26 (5.15 -> 16.8 states/eV/cell). Corrects RTSC_21's path-sampled "~0.6-0.8 e/cell" (order-of-mag low).
domain: rtsc qe dft cosn kagome flat-band rigid-band doping dos tc
status_grade: 🟠 INDICATIVE (rigid-band on converged QE 7.5 SCF; BZ-grid weighted; tot_charge SCF cross-check)
verification_method: rigid-band integral of converged scf.out eigenvalues+wk (nspin=2, 6x6x6 tetra grid) on summer; gaussian occ sig=0.10eV; sanity N(E_F)=93.04; verbatim; p7
since: 2026-06-14
sister: RTSC_21, RTSC_13, RTSC_14, RTSC_22
verdict: 🟠 Rigid-band (BZ tetrahedron-grid weighted, sanity N(E_F)=93.04≈93) over the converged QE 7.5 CoSn SCF (E_F=14.7132eV, flat band45 @14.2697eV = ΔE −0.4435eV). To lower E_F by ~0.44eV ONTO the flat band needs **hole-doping x ~ 4.72 e/cell** (~1.57 holes/Co); at alignment **N(E_F) ~ 16.78 states/eV/cell vs undoped 5.15 → x3.26** — the Tc-relevant DOS spike. **CORRECTS RTSC_21's "~0.6-0.8 e/cell"** which was a path-sampled-DOS underestimate (only path-crossing bands counted); the full BZ integral counts ALL bands between E_F and the flat band → ~6x larger x. HONEST: rigid-band = order-of-mag (frozen bands; 4.7e/cell is a LARGE perturbation where rigid-band is least reliable → x is an indicative upper-bound-ish figure); sig=0.10eV smears the spike (true N(E_F) could be higher); 6x6x6 not k-converged. tot_charge SCF cross-check: dispatched tot_charge=+4.0 (charge renorm 93→89 confirmed = doping correctly wired) but did NOT converge in-window — summer box oversubscribed by sibling lanes (load ~31-37/12 cores), first nspin=2 diagonalization starved at iter#1; own job stopped, co-tenant rbfe untouched & alive. SCF confirmation pending an uncontended re-run.
---
# RTSC_24 — CoSn rigid-band hole-doping → flat band alignment
## 측정 (rigid-band over converged QE 7.5 SCF, summer, verbatim · verdicts/cosn_doping.txt)
- Source: converged `scf.out` (nspin=2, 93 e⁻, **E_F=14.7132 eV**); flat band45 @14.2697 eV (RTSC_21).
- Method: N(E_F) = Σ_{spin,k,band} wk·f(ε−E_F), Gaussian occ σ=0.10 eV, wk from the converged 6×6×6 tetrahedron grid (28 irred k × 56 bands × 2 spins). **Sanity N(14.7132)=93.04 ≈ 93** → integrator validated.
- Δn(hole) = N(14.7132) − N(E_F_target).

| E_F target (eV) | Δn hole (e/cell) | N(E_F) states/eV/cell |
|---|---|---|
| 14.71 (undoped) | 0.02 | 5.20 |
| 14.56 | 1.00 | 8.09 |
| 14.41 | 2.56 | 13.14 |
| 14.31 | 4.05 | 16.38 |
| **14.27 (FLAT BAND)** | **4.72** | **16.78** |
| 14.21 | 5.72 | 16.26 |

## 결론
🟠 **x ~ 4.72 e/cell hole-doping aligns E_F with the Co-kagome flat band**, giving **N(E_F) ~16.8 vs 5.15 undoped (×3.26)** — a >3× DOS spike (Tc lever). The DOS peaks ~14.26 eV (right at the flat band) then falls, confirming the flat band is the N(E_F) maximum. **Corrects RTSC_21** (path-sampled "~0.6-0.8 e/cell" was order-of-mag low). 정직: rigid-band frozen-band assumption is weakest at this large 4.7 e/cell perturbation → indicative; σ=0.10 eV smears the flat-band δ-like spike (real peak likely higher with finer k + smaller σ); 6×6×6 DOS not converged. 다음: 정밀 tetrahedron DOS(dense nscf) + DFPT λ(x)/Tc at the aligned filling.
verdict: `RTSC/verdicts/cosn_doping.txt`
