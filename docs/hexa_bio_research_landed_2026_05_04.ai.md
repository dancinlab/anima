# hexa-bio research landed — 2026-05-04

> Status: deep research + canonical spec draft DELIVERED for standalone repo `hexa-bio` (4-verb molecular toolkit)
> Mode: Mac side, raw#9 STRICT, READ-ONLY on CANON, no extraction (sister BG handles extraction)
> Cycle: anima cycle 2026-05-04 — research arm

## What landed

| Artefact | Path | Size |
|----------|------|------|
| Canonical spec doc | `docs/hexa_bio_spec_2026_05_04.md` | ~280 LoC (4-verb spec + lattice + API + 4 falsifiers + 5 caveats) |
| Per-verb audit JSON | `state/hexa_bio_research_2026_05_04/per_verb_audit.json` | machine-readable per-verb summary + tetrahedron closure status |
| Literature anchors JSON | `state/hexa_bio_research_2026_05_04/literature_anchors.json` | per-verb canonical refs + cross-verb unification |
| n=6 lattice mapping JSON | `state/hexa_bio_research_2026_05_04/n6_lattice_mapping.json` | per-verb σ/τ/φ/J₂ projection + grade ranking + caveats |
| Marker | `state/markers/hexa_bio_research_landed_2026_05_04.marker` | landed marker for cycle audit |

## Key findings

1. **`nexus/modules/weave/` does not exist** — user comment "간단히 있다는" was a confusion with `nexus/sim_bridge/weave/` (Zlotnick T=1 cage simulator + Caspar-Klug Bayesian audit, belongs to VIROCAPSID assembly axis). hexa-bio MUST treat `nexus/sim_bridge/weave/` as READ-ONLY reference and consume it for the `virocapsid` subcommand.

2. **4 verbs registered in CANON as biology tetrahedron** (cycles 1, 13, 15, 19; all 2026-04-28; alien-grade 4.78):
   - WEAVE — write-side multi-strand composition; Landauer × NP ceiling; STRUCTURAL load-bearing
   - NANOBOT — single-device mechanical actuation; Brownian floor at 310 K; STRUCTURAL approximate
   - RIBOZYME — RNA catalysis; diffusion-limit ceiling 10⁹ M⁻¹ s⁻¹; STRUCTURAL-APPROXIMATE (corpus span 10–30 nt)
   - VIROCAPSID — icosahedral self-assembly; kinetic-trap ceiling; STRUCTURAL-EXACT (Bayesian posterior 0.9668 RESOLVED)

3. **n=6 invariant lattice grade is non-uniform** — only VIROCAPSID is STRUCTURAL-EXACT (Caspar-Klug topological invariant). The unifying-lens claim is preregistered as falsifier F-N6-LATTICE-DECORATIVE: if Bayesian model comparison on combined corpora shows H0 cannot be rejected at log-Bayes-factor ≥ 3 in 3 of 4 verbs, the lattice reduces to a coincidence-on-VIROCAPSID-only.

4. **All 4 verbs share 90-day MVP deadline 2026-07-28** — F-WEAVE-1 / F-NANOBOT-1 / F-RIBOZYME-1 / F-VIROCAPSID-1 with thresholds: 3.0 Å RMSD / 80% cycle fidelity / 10⁶-fold rate enhancement / 0.85 closed-shell yield (all initial-guess thresholds per raw 91 C3, calibration in cycle 25+).

5. **API surface designed**: `hexa-bio {weave,nanobot,ribozyme,virocapsid,status,selftest,falsifiers,cite,--version}` — 4 verb subcommands + 5 common, with shared `N6Invariant` API checked before any computation.

## What's NOT done (sister BG / next cycle)

- Repo extraction: NOT done by this research arm — sister BG handles `hexa-bio` standalone repo extraction
- Implementation: only spec; no Python / Hexa source code emitted
- Literature refresh: anchor lists cover founding + canonical refs but NOT 2021-2026 sweep (5 papers/verb estimated gap)
- Threshold calibration: F-{WEAVE,NANOBOT,RIBOZYME,VIROCAPSID}-1 thresholds are conservative-MVP estimates; cycle 25+ MVP runs must re-derive via leave-one-out validation
- Lean4 mechanical layer: only WEAVE has sorry-free lean4 + 7 named axioms; the other 3 verbs inherit OPTIONAL via `Foundation/Strand.lean`

## 5 honest C3 caveats (per raw#10)

1. Literature anchor incomplete (2021-2026 sweep gap, ~5 papers/verb)
2. Falsifier thresholds are initial-guess (no held-out test set calibration)
3. n=6 lattice claim speculative without proof for 3 of 4 verbs (only VIROCAPSID Bayesian-resolved)
4. AlphaFold contrast oversimplified (AF3 handles small complexes; genuine distinction is read-side vs write-side)
5. Drug discovery is NOT this MVP scope (clinical efficacy / FDA / proprietary target validation are downstream, not hexa-bio)

## Constraints honored

- raw#9 STRICT — Mac → markdown spec only, no code emitted, no model loading
- raw#10 — 5 honest C3 caveats explicitly enumerated
- raw#15 — research artefacts under `state/hexa_bio_research_2026_05_04/` not committed automatically
- $0 spend — pure file-IO research, no API calls, no GPU
- READ-ONLY on CANON (verified: only Read tool used on `CANON/`)
- Did NOT touch `nexus/sim_bridge/weave/` (sister assembly-axis SSOT, untouched)
- Did NOT touch `nexus/modules/weave/` (does not exist)
