# hexa-bio — canonical specification (4-verb molecular toolkit)

> Date: 2026-05-04
> Status: research + spec draft (raw#9 STRICT — Mac side, no extraction, READ-ONLY on n6-architecture)
> Scope: standalone repo `hexa-bio` containing 4 sister CLI subcommands (`weave` / `nanobot` / `ribozyme` / `virocapsid`)
> SSOT lineage: declarative @ `n6-architecture/domains/biology/hexa-{weave,nanobot,ribozyme,virocapsid}/`; empirical (assembly axis only) @ `nexus/sim_bridge/weave/`
> Out of scope: extraction work (handled by sister BG); edits to existing `nexus/modules/weave/` (none exists; `nexus/sim_bridge/weave/` left untouched)

## §0 Executive summary

`hexa-bio` is a standalone CLI tool that exposes the four sister "Molecular Toolkit (HEXA family)" verbs as a single binary with four subcommands plus shared `status` and `selftest`. The four verbs are orthogonal in genus (composition / actuation / catalysis / assembly) but share the same `n=6` invariant lattice (σ(6)=12, τ(6)=4, φ(6)=2, J₂=24, master identity σ·φ = n·τ = J₂ = 24). Each verb has an explicit primary constraint (Landauer × NP / Brownian / diffusion / kinetic-trap), a literature anchor set, and a 90-day MVP falsifier. The n=6 invariant grade ranges from STRUCTURAL-EXACT (VIROCAPSID, Bayesian posterior 0.9668 RESOLVED) to STRUCTURAL-APPROXIMATE (RIBOZYME, corpus span 10–30 nt) per raw 91 C3 honest disclosure.

| Verb | Icon | Genus | Primary constraint | n=6 grade |
|------|------|-------|--------------------|-----------|
| WEAVE | knit | compose strands | Landauer × NP-search ceiling | STRUCTURAL load-bearing |
| NANOBOT | robot | actuate atoms | kT Brownian floor at 310 K | STRUCTURAL approximate |
| RIBOZYME | scissors | catalyse bonds | k_cat/K_M ≤ 10⁹ M⁻¹s⁻¹ diffusion ceiling | STRUCTURAL-APPROXIMATE |
| VIROCAPSID | virus | assemble shells | kinetic-trap aberrant fraction ceiling | STRUCTURAL-EXACT |

## §1 Existing nexus state (audit)

### §1.1 What exists

- `nexus/modules/weave/` — **does not exist** (verified by `find` 2026-05-04). The user comment "간단히 있다는" appears to be a confusion with `nexus/sim_bridge/weave/`.
- `nexus/sim_bridge/weave/` — **exists**, 5 files, ~50 KB total:
  - `cage_assembly_simulation.py` (26.9 KB) — T=1 60-subunit Zlotnick 4-state ODE (Euler + RK4)
  - `polyhedral_cage_bayesian_audit.py` (17.0 KB) — Caspar-Klug n=34 textbook corpus + Bayesian posterior
  - `README.md` (5.5 KB) — module documentation
  - `runner.sh` — execution wrapper
  - `runs/` — append-only JSONL ledger (raw 77 schema)
- Constraint: `python3` stdlib only — no numpy/scipy/torch (raw 14 ext-ssot 외부의존성 0)
- Belongs to: VIROCAPSID axis (cage assembly + Bayesian audit)
- Read-only contract: hexa-bio MUST NOT modify `nexus/sim_bridge/weave/` — it consumes its outputs as a reference implementation

### §1.2 What does NOT exist

- No CLI wrapper (no `hexa-bio` binary or subcommand dispatch)
- No WEAVE empirical sandbox (composition pipeline is theoretical-only per `n6-architecture/domains/biology/hexa-weave/`)
- No NANOBOT simulation (4-state 12-vertex DNA-origami simulation pending F-NB-4 deadline 2026-07-28)
- No RIBOZYME chemical-kinetics simulation (hammerhead 12-nt 4-state pending F-RB-4 deadline 2026-07-28)
- No unified `n6-invariant.{sigma,tau,phi,J2}` API across the 4 verbs

### §1.3 Repo scope decision

`hexa-bio` is the standalone repo that fills the gap: a single CLI binary unifying the 4 verbs with a shared n=6 lattice API, where each verb has its own subcommand and shares common infrastructure (status / selftest / falsifier registry). The existing `nexus/sim_bridge/weave/` is consumed as the **assembly axis (VIROCAPSID) reference simulator** — `hexa-bio virocapsid` may shell out to it or re-implement equivalent primitives in stdlib.

## §2 The n=6 invariant lattice

### §2.1 Quartet definition

| Symbol | Value | Definition | Mathematical anchor |
|--------|-------|------------|---------------------|
| σ(6) | 12 | sum of divisors of 6: 1+2+3+6 | classical multiplicative function |
| τ(6) | 4 | number of divisors of 6: \|{1,2,3,6}\| | classical multiplicative function |
| φ(6) | 2 | Euler totient of 6: \|{1,5}\| | Euler 1763 |
| J₂ | 24 | octahedral O = \|S₄\| (n6-corpus shorthand) | classical group theory |
| sopfr(6) | 5 | sum of prime factors with repetition: 2+3 | OEIS A001414 |

**Master identity** (canonical n6 binding):

```
σ(6) · φ(6) = 12 · 2 = 24
n · τ(6)    =  6 · 4 = 24
J₂          =          24
```

i.e., **σ(6)·φ(6) = n·τ(6) = J₂ = 24** holds at n=6.

### §2.2 Honest dual-usage caveat (per raw 91 C3)

`J₂` in the n6-architecture corpus is used as a **shorthand for the octahedral group O of order 24**, NOT for the Hall–Janko sporadic group J₂ of order 604,800. The naming collision is documented in `n6-architecture/papers/`. In the four-verb projections below, J₂=24 refers to the 24-element pose-equivalence group (octahedral / per-cube / TS-pose-class), not the sporadic.

### §2.3 Per-verb lattice projection summary

| Verb | σ(6)=12 | τ(6)=4 | φ(6)=2 | J₂=24 | Grade |
|------|---------|--------|--------|-------|-------|
| WEAVE | 12 raw-strategies in kernel | 4-axis architecture | hydrophobic/hydrophilic bit | M₂₄ Mathieu / Leech-24 ambient | STRUCTURAL load-bearing |
| NANOBOT | 12-vertex polyhedral skeleton | 4 motor states | open/closed binary actuator | octahedral pose-equivalence \|O\|=24 | STRUCTURAL approximate |
| RIBOZYME | ~12 catalytic-core nucleotides (10–30 nt span) | 4 reaction states | cleaved/intact binary | trigonal-bipyramidal TS pose cover | STRUCTURAL-APPROXIMATE |
| VIROCAPSID | 12 pentameric vertices on T=1 (Caspar-Klug EXACT, posterior 0.9668) | 4 assembly states (Zlotnick) | free/assembled dichotomy | octahedral O subgroup of icosahedral I via 5-inscribed-cube action | STRUCTURAL-EXACT |

The grade ranges from EXACT (VIROCAPSID, topologically forced by Euler V−E+F=2 and Caspar-Klug 1962) to APPROXIMATE (RIBOZYME, where the catalytic-core size varies 10–30 nt across the 7-class corpus). This grade variation is **load-bearing honesty** per raw 91 C3 — the lattice is a unifying analytical lens, not a proven physical-causal law uniformly across all four verbs.

## §3 Per-verb specifications

### §3.1 HEXA-WEAVE — compose

#### Position
Knit-AI for multi-strand molecular bundles. Where AlphaFold answers *"given a sequence, what is its structure?"*, WEAVE answers *"given a target multi-molecule context, design the strand-set that produces it."* The contrast is between paper-folding one strand (AF) and weaving many strands (WEAVE).

#### Object scale
P up to 10⁴ proteins, N=350 aa per strand, 10⁷ to 10⁹ atoms per bundle.

#### Primary constraint
**Landauer × NP-search ceiling** — irreversible bit erasure costs kT ln 2 per bit (Landauer 1961), and inverse-folding is NP-complete in the HP model (Berger-Leighton 1998), so whole-proteome inverse design is jointly bounded by computational complexity (Π^p_2 verifier) and thermodynamic accounting (cellular heat budget per Brown 2009).

#### Canonical literature anchors
- AlphaFold 3 (Abramson 2024) — read-side oracle counterpart
- Berger-Leighton 1998 — HP-model NP-completeness
- Hart-Istrail 1996 — 3D extension
- Garey-Johnson 1979 — polynomial-hierarchy ladder
- Landauer 1961 — irreversibility floor
- Bennett 1982 — reversibility complement
- Brown 2009 — cellular heat budget
- IsoDDE (Isomorphic Labs 2026-02) — proprietary closed write-side benchmark

#### 4-axis architecture (τ(6)=4)
- Axis A: Strand catalogue (single-chain folds from AF3-class oracle, indexed by sequence)
- Axis B: Composition kernel (inverse-search over bundle compatibility, σ(6)=12 raw-strategies)
- Axis C: Thermodynamic gate (Landauer floor check + cellular heat budget)
- Axis D: Closure certifier (Π¹_1-CA₀ totality + Π^p_2 verifier + falsifier registry)

#### Falsifier F-WEAVE-1 (90-day MVP)
- **Claim**: end-to-end MVP run with P≥10 strands, N≥50 aa per strand by 2026-07-28
- **Threshold**: ternary structure RMSD ≤ **3.0 Å** vs experimental crystal on 3 reference complexes (initial-guess threshold; calibrate in cycle 25+)
- **MISS criterion**: failure to deliver MVP, OR RMSD > 3.0 Å on ≥2 of 3 references
- **Counter-class**: a single-chain AF3 prediction of any one of the 3 strands suffices — would falsify the "multi-strand composition is qualitatively distinct from single-chain prediction" claim

### §3.2 HEXA-NANOBOT — actuate

#### Position
Tiny robot arm — open/close, grab/release. Designs molecular kinematics: how molecules MOVE (actuate), not how many strands compose (WEAVE) or how RNA cuts (RIBOZYME). Builds on DNA-origami literature (Yan group, Rothemund 2006, Seeman 1982 lattices) and Drexler 1986 productive-nanotechnology framework.

#### Object scale
10⁰ to 10² atoms per actuator (Rothemund-class scaffold up to 10⁴ atoms). Single device per spec — networks of N>1 cross into WEAVE composition regime (L7 boundary).

#### Primary constraint
**kT thermal noise floor at 310 K** — kT = 4.28×10⁻²¹ J at body temperature; work-per-cycle below 10·kT is Brownian-noise-limited (Bustamante 2005). Stochastic ratchets (Astumian 1997) are a falsifier candidate for the power-stroke quartet model.

#### Canonical literature anchors
- Drexler 1986 — productive nanotechnology (power-stroke quartet)
- Seeman 1982 — immobile-junction DNA scaffolds (vertex skeleton precursor)
- Rothemund 2006 — DNA origami (12-vertex polyhedral cage implicit)
- Yan group (Yan 2003 et seq.) — DNA-templated self-assembly
- Goodsell 2009 — molecular-machine taxonomy
- Howard 2001 — power-stroke kinetics + free-energy landscape
- Bath-Turberfield 2007 — DNA nanomachines state-machine reference
- Astumian 1997 — Brownian-motor / stochastic-ratchet alternative

#### 4-axis architecture (τ(6)=4)
- Axis A: Vertex skeleton (12-vertex polyhedral DNA-origami; truncated tetrahedron / icosahedron / cuboctahedron)
- Axis B: Power-stroke kinetics (4 motor states: idle / forward-stroke / backward-stroke / reset)
- Axis C: Pose-symmetry group (octahedral |O|=24 quotient; 24-fold simulation state-space reduction)
- Axis D: Binary actuator output (open/closed clamp, bound/unbound substrate)

#### Falsifier F-NANOBOT-1 (90-day MVP)
- **Claim**: 4-state 12-vertex DNA-origami coarse-grained MD simulation by 2026-07-28
- **Threshold**: open↔close cycle fidelity ≥ **80%** over N=100 cycles at 310 K (initial-guess threshold; the published Bath-Turberfield 2007 DNA tweezers reach ~95% in idealized buffer, so 80% is a conservative MVP margin)
- **MISS criterion**: cycle fidelity < 80%, OR work-per-cycle drops below 10·kT (Brownian-floor violation), OR a published 5-motor-state device with equal fidelity is found (falsifies τ(6)=4 binding)
- **Counter-class**: any DNA-origami device with non-12 vertex skeleton outperforming 12-vertex variants would falsify σ(6)=12 binding

### §3.3 HEXA-RIBOZYME — catalyse

#### Position
RNA scissors — RNA cuts itself without a protein enzyme. Designs catalytic cores for phosphodiester bond cleavage / ligation. The 4 canonical instances are hammerhead / HDV / hairpin / ribosome PTC (peptidyl transferase center). Plus group-I intron (Cech 1982) and RNase P (Guerrier-Takada 1983) as the 2 founding discoveries.

#### Object scale
10² to 10³ atoms per active site (~12–30 nt catalytic core). Multi-active-site assemblies cross into WEAVE composition regime (L7 boundary).

#### Primary constraint
**Diffusion-limit ceiling k_cat/K_M ≤ 10⁸ to 10⁹ M⁻¹ s⁻¹** (Eigen-Hammes 1963) — second-order rate constants cannot exceed the diffusion-encounter rate. Below this ceiling, ribozymes vary by >5 orders of magnitude in catalytic enhancement.

#### Canonical literature anchors (4 instances + 2 founders)
1. **hammerhead** — Symons 1981 avocado sunblotch viroid; minimal type-II+III conserved core ~13 nt
2. **HDV** — Wu-Lai 1989 hepatitis delta virus; antigenomic ~12 nt catalytic core
3. **hairpin** — Buzayan 1986 plant virus satellite; A-loop + B-loop ~12 conserved nt
4. **ribosome PTC** — Nissen-Steitz 2000; peptidyl transferase center as the largest natural ribozyme
- group-I intron — Cech 1982 Tetrahymena self-splicing (founding catalytic-RNA literature)
- RNase P RNA — Guerrier-Takada-Altman 1983 (RNA-only cleavage of pre-tRNA)
- Steitz-Steitz 1993 — two-metal-ion mechanism (TS pose-symmetry foundational)
- Eigen-Hammes 1963 — diffusion-limit ceiling
- Turner-Mathews 2010 NNDB — nearest-neighbour free-energy parameters
- Tang-Breaker 2000 — structural diversity of self-cleaving ribozymes (Bayesian audit corpus)

#### Chemical mechanism (4 canonical instances)
- **hammerhead / hairpin / HDV**: 2'-OH nucleophilic attack on adjacent phosphodiester, in-line SN2-like trigonal-bipyramidal TS at phosphorus, 2',3'-cyclic phosphate + 5'-OH product. Acid-base catalysis with active-site nucleotides plus Mg²⁺ co-factor.
- **ribosome PTC**: peptidyl-tRNA aminolysis; A-site amino group attacks P-site carbonyl C; substrate-assisted catalysis with 2'-OH of A76 of P-site tRNA as proton shuttle; entropy-driven (Sievers-Steitz 2004).

#### 4-axis architecture (τ(6)=4)
- Axis A: Catalytic-core residues (σ(6)=12 conserved nucleotides; STRUCTURAL-APPROXIMATE)
- Axis B: Reaction-state ladder (4 states: substrate-bound / TS / cleaved / product-released)
- Axis C: TS symmetry group (J₂=24 trigonal-bipyramidal phosphate cover via octahedral rotation)
- Axis D: Binary cleavage outcome (cleaved/intact, cis/trans)

#### Falsifier F-RIBOZYME-1 (90-day MVP)
- **Claim**: hammerhead-minimal 12-nt-core 4-state chemical-kinetics simulation by 2026-07-28
- **Threshold**: catalytic rate enhancement ≥ **10⁶-fold vs uncatalyzed** (initial-guess based on published hammerhead k_cat ~1 s⁻¹ vs uncatalyzed RNA half-life ~10⁸ s at neutral pH 25 °C per Li-Breaker 1999; ~10⁸-fold enhancement is the mid-range; 10⁶ is the conservative MVP margin)
- **MISS criterion**: rate enhancement < 10⁶, OR k_cat/K_M > 10⁹ M⁻¹ s⁻¹ (diffusion-ceiling violation = internal contradiction → retract)
- **Counter-class**: a published ribozyme with 5+ reaction states OR catalytic-core outside 10–15 nt range with comparable k_cat/K_M would falsify the τ(6)=4 / σ(6)=12 cardinality binding

### §3.4 HEXA-VIROCAPSID — assemble

#### Position
Virus shell — 60 identical "Lego blocks" self-organize into an icosahedral cage. T=1 60-subunit cage is the reference target. Applications: VLP vaccines (HPV L1 T=7, HBV core T=4), drug capsule (CCMV, CPMV plant-virus nanoparticles), nano-cage (controlled-release).

#### Object scale
10⁵ to 10⁷ atoms per capsid; 60 to 420 subunits depending on T-number (T=1: 60, T=3: 180, T=4: 240, T=7: 420; subunit count = 60·T per Caspar-Klug 1962).

#### Primary constraint
**Kinetic-trap ceiling on aberrant-aggregate fraction** — Zlotnick 2003 nucleation-elongation: assembly proceeds via nucleation barrier then elongation; if rate constants are too fast or concentration too high, kinetic traps (off-pathway aggregates) dominate over closed-shell yield. The current Zlotnick simulation in `nexus/sim_bridge/weave/cage_assembly_simulation.py` plateaus at 0.68 yield under default rate constants (calibration gap, F-CAGE-MVP-1 deadline 2026-07-28).

#### Canonical literature anchors
- Caspar-Klug 1962 — quasi-equivalence theory; T = h² + h·k + k²
- Crick-Watson 1956 — small-virus geometric reasoning predecessor
- Rossmann-Johnson 1985 — atomic-resolution capsid synthesis (poliovirus T=3)
- Harrison 1978 — first atomic-resolution T=3 (TBSV)
- Liljas 1982 — T=1 60-subunit minimal capsid (STNV) — canonical T=1 12-vertex EXACT
- Zlotnick 2003 — nucleation-elongation kinetic theory
- Zlotnick 1996 — HBV T=3/T=4 dimorphism
- Twarock-Luque 2016 — generalized PCK; non-quasi-equivalent extensions
- Bruinsma 2003 — thermodynamic capsid-assembly framework
- Endres-Zlotnick 2002 — concrete master-equation reference
- Mannige-Brooks 2010 — periodic table of virus capsids (Bayesian-audit corpus n>30)
- VLP vaccines: Schiller-Lowy 2018 (HPV L1), Zhao 2012 (HBV core), Zhao 2013 (review)
- Drug delivery: Bruckman 2014 (TMV MRI), Lee 2016 (CPMV chemotherapy)

#### 4-axis architecture (τ(6)=4)
- Axis A: Vertex cardinality (σ(6)=12 vertex on T=1, STRUCTURAL-EXACT for every T-number)
- Axis B: Assembly-state ladder (4 states: free CP / pentamer / hexamer-mixed / closed cage)
- Axis C: Symmetry pose-equivalence (J₂=24 octahedral O ⊂ icosahedral I via 5-inscribed-cube action)
- Axis D: Binary shell-closure (closed/open; sealed vs aperture-bearing)

#### Falsifier F-VIROCAPSID-1 (90-day MVP)
- **Claim**: T=1 minimal 60-subunit 4-state Zlotnick-class kinetic simulation reaches assembly yield ≥ threshold by 2026-07-28
- **Threshold**: closed-shell yield ≥ **0.85** over Y=10 independent rate-constant calibrations on 3 reference capsids (HBV / CCMV / STNV) — initial-guess threshold; current `cage_assembly_simulation.py` plateaus at 0.68 (calibration gap), so 0.85 is the MVP target with ~25% headroom; published T=1 STNV in vitro reassembly reaches >0.9 yield
- **MISS criterion**: yield < 0.85 reproducible across 3 reference capsids → calibration gap confirmed; aberrant-aggregate fraction > closed-shell yield → kinetic-trap-ceiling violation = internal contradiction → retract
- **Counter-class**: helical TMV (rod-shape, no icosahedral 12-vertex) is the pre-registered counter-class that confirms σ(6)=12 binds only on the icosahedral subset of the capsid taxonomy

## §4 API surface — CLI subcommands

### §4.1 Top-level binary

```
hexa-bio <subcommand> [options]
```

### §4.2 Per-verb subcommands

| Subcommand | Purpose | Required args | Optional args |
|------------|---------|---------------|---------------|
| `hexa-bio weave` | Multi-strand bundle composition | `--input <pdb,...>` `--target <ternary-context.json>` | `--max-strands N` `--landauer-budget J` `--out-dir DIR` |
| `hexa-bio nanobot` | DNA-origami molecular gripper design | `--vertex-count 12` `--motor-states 4` | `--scaffold <caDNAno.json>` `--temperature K` `--cycles N` |
| `hexa-bio ribozyme` | Catalytic RNA design | `--class {hammerhead,HDV,hairpin,PTC}` `--substrate <seq>` | `--core-nt 12` `--metal Mg2+` `--ph 7.4` |
| `hexa-bio virocapsid` | Icosahedral capsid self-assembly simulation | `--T-number {1,3,4,7}` `--coat-protein <fasta>` | `--rate-constants <json>` `--cargo {none,RNA,drug}` `--t-end 1000` |

### §4.3 Common subcommands

| Subcommand | Purpose | Output |
|------------|---------|--------|
| `hexa-bio status` | Show n=6 lattice + per-verb registration grade + last-run timestamps | JSON to stdout |
| `hexa-bio selftest` | Run all 4 verb selftests + n=6 invariant verification + cite-graph lint | exit 0 on PASS, non-zero on any FAIL |
| `hexa-bio falsifiers` | List all preregistered falsifiers + deadlines + status | table (markdown / JSON) |
| `hexa-bio cite` | Print literature anchors for a verb (or all) | markdown / BibTeX |
| `hexa-bio --version` | Version + n6-architecture commit hash + build timestamp | string |

### §4.4 Shared invariant API

```python
# Stub interface; implementation lives in hexa-bio/lattice.py
from hexa_bio.lattice import N6Invariant

inv = N6Invariant(n=6)
assert inv.sigma == 12
assert inv.tau == 4
assert inv.phi == 2
assert inv.J2 == 24
assert inv.master_identity_holds()  # sigma * phi == n * tau == J2 == 24
```

Each verb subcommand checks the n=6 invariant before any computation; failure aborts with non-zero exit (raw 71 falsifier-registry contract).

## §5 Falsifier registry summary

| ID | Verb | Claim | Threshold | Deadline |
|----|------|-------|-----------|----------|
| F-WEAVE-1 | WEAVE | end-to-end MVP P≥10 N≥50 | RMSD ≤ 3.0 Å vs experimental on 3 refs | 2026-07-28 |
| F-NANOBOT-1 | NANOBOT | 4-state 12-vertex MD sim | open↔close cycle fidelity ≥ 80% over N=100 | 2026-07-28 |
| F-RIBOZYME-1 | RIBOZYME | hammerhead-minimal 12-nt sim | rate enhancement ≥ 10⁶-fold vs uncatalyzed | 2026-07-28 |
| F-VIROCAPSID-1 | VIROCAPSID | T=1 60-subunit Zlotnick sim | closed-shell yield ≥ 0.85 over 10 calibrations on 3 refs | 2026-07-28 |
| F-N6-LATTICE-DECORATIVE | shared | n=6 lattice not load-bearing | Bayesian H0 cannot be rejected at log-Bayes-factor ≥ 3 in 3 of 4 verbs | 2026-09-28 |

All thresholds are **initial-guess** per raw 91 C3 (see §6 caveat 2). Calibration in cycle 25+ MVP runs may revise.

## §6 Honest C3 caveats (per raw 10, 5 caveats)

1. **Literature anchor incomplete** — the per-verb anchor lists in §3 cover the founding + canonical references but are not exhaustive of the past 5 years (2021–2026). Notable gaps: (a) AlphaFold 2026 successor work; (b) recent DNA-origami Wyss Institute publications post-2023; (c) post-2020 ribozyme deep-mutational-scanning campaigns; (d) recent VLP vaccine clinical-trial readouts (HPV9 / RSV-VLP). A literature-refresh sweep targeting the last 24 months is required before any 90-day MVP gate is asserted as hit/miss.

2. **Falsifier thresholds are initial-guess** — F-WEAVE-1 (3.0 Å RMSD), F-NANOBOT-1 (80% cycle fidelity), F-RIBOZYME-1 (10⁶-fold rate enhancement), F-VIROCAPSID-1 (0.85 yield) are all conservative-MVP estimates derived from published canonical instances (Bath-Turberfield 95% DNA tweezers, Symons-1981 hammerhead k_cat ~1 s⁻¹, in-vitro STNV reassembly >0.9). They have NOT been calibrated on a held-out test set. Cycle 25+ MVP runs must explicitly re-derive thresholds from a leave-one-out validation across the 3 reference instances per verb.

3. **n=6 lattice claim is speculative without proof** — only HEXA-VIROCAPSID has STRUCTURAL-EXACT evidence (Caspar-Klug topological invariant + Bayesian posterior 0.9668 on n=34 corpus). HEXA-WEAVE / HEXA-NANOBOT / HEXA-RIBOZYME are STRUCTURAL-LOAD-BEARING / APPROXIMATE / APPROXIMATE respectively. The unifying-lens claim is preregistered as falsifier F-N6-LATTICE-DECORATIVE: if Bayesian model comparison on combined corpora shows H0 (random cardinalities) cannot be rejected at log-Bayes-factor ≥ 3 in 3 of 4 verbs, the n=6 lattice reduces to a coincidence-on-VIROCAPSID-only and the "unifying invariant" framing collapses.

4. **AlphaFold contrast is oversimplified** — the §3.1 "AlphaFold = paper-folding 1 strand, WEAVE = weaving many strands" framing is pedagogically useful but technically imprecise: AlphaFold 3 (Abramson 2024) does handle small complexes (DNA / RNA / ligand co-folds), so AF3 is not strictly "1 strand". The genuine distinction is **read-side (predict structure given sequence) vs write-side (design sequence/composition given target structure)** — AF3 covers some of the multi-molecule space on the read side but does not solve the inverse-search composition problem. Similarly, AlphaFold can structurally predict ribozymes (RIBOZYME) and capsid subunits (VIROCAPSID), but does not design new catalytic cores or self-assembly trajectories.

5. **Drug discovery is NOT this MVP scope** — `hexa-bio` is a 4-verb MOLECULAR ARCHITECTURE toolkit (composition / actuation / catalysis / assembly), not a drug-discovery platform. The IsoDDE (Isomorphic Labs 2026-02) closed proprietary system is cited only as a positioning benchmark for HEXA-WEAVE — the open WEAVE write-side counterpart. `hexa-bio` MVP gates (F-WEAVE-1 through F-VIROCAPSID-1) target architectural primitives + Bayesian-audit thresholds, NOT clinical efficacy, NOT FDA-approval-grade ADMET, NOT proprietary target validation. Any drug-discovery lift is a downstream hand-off to `domains/life/bio-pharma/` or `domains/life/therapeutic-nanobot/`.

## §7 References (consolidated)

(Per-verb anchors are listed in §3; canonical inheritance from `n6-architecture/domains/biology/hexa-{weave,nanobot,ribozyme,virocapsid}/*.md` §15 REFERENCES sections.)

- WEAVE: Abramson 2024, Berger-Leighton 1998, Hart-Istrail 1996, Garey-Johnson 1979, Landauer 1961, Bennett 1982, Brown 2009, IsoDDE 2026-02
- NANOBOT: Drexler 1986, Seeman 1982, Rothemund 2006, Yan 2003, Goodsell 2009, Howard 2001, Bath-Turberfield 2007, Astumian 1997, Bustamante 2005, Goddard 2003
- RIBOZYME: Cech 1982, Guerrier-Takada-Altman 1983, Symons 1981, Wu-Lai 1989, Buzayan 1986, Steitz-Steitz 1993, Nissen-Steitz 2000, Eigen-Hammes 1963, Turner-Mathews 2010, Hofacker 1994, Zuker 1989, Tang-Breaker 2000, Wilson-Lilley 2009
- VIROCAPSID: Caspar-Klug 1962, Crick-Watson 1956, Rossmann-Johnson 1985, Harrison 1978, Liljas 1982, Zlotnick 2003, Zlotnick 1996, Twarock-Luque 2016, Bruinsma 2003, Endres-Zlotnick 2002, Mannige-Brooks 2010, Sun-Rao-Rossmann 2010, Stockley 2013, Schiller-Lowy 2018, Zhao 2012, Zhao 2013, Bruckman 2014, Lee 2016

### SSOT cross-link
- declarative SSOT: `~/core/n6-architecture/domains/biology/hexa-{weave,nanobot,ribozyme,virocapsid}/`
- formal SSOT: `~/core/n6-architecture/lean4-n6/N6/MechVerif/` (WEAVE only, sorry-free + 7 named axioms)
- paper SSOT: `~/core/n6-architecture/papers/hexa-weave-formal-mechanical-w2-2026-04-28.md`
- empirical SSOT (assembly axis only): `~/core/nexus/sim_bridge/weave/` (Zlotnick T=1 + Caspar-Klug Bayesian audit; READ-ONLY for hexa-bio)
- this spec: `~/core/anima/docs/hexa_bio_spec_2026_05_04.md`
- research artefacts: `~/core/anima/state/hexa_bio_research_2026_05_04/{per_verb_audit.json, literature_anchors.json, n6_lattice_mapping.json}`
