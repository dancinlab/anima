# tabletop_blackhole extraction handoff (2026-05-04)

## Status: LANDED (n6-arch) + STAGED (nexus delete, awaiting user commit)

## What landed

- `CANON/domains/physics/tabletop-blackhole/tabletop_blackhole.hexa` (307 LoC)
- `CANON/domains/physics/tabletop-blackhole/tabletop_blackhole.README.md` (49 LoC)
- Co-located with `tabletop-blackhole.md` (TBHL-01..08 research spec)

## Destination divergence (vs recipe)

Recipe specified `experiments/tabletop-blackhole/`. Actual destination is
`domains/physics/tabletop-blackhole/` to co-locate .hexa with the existing
research spec — matches Phase-1 absorb pattern (crystallography_n6,
chip_isa_n6 both used `domains/<sub>/<topic>/` co-location).

## Smoke (n6-arch root)

```
$ hexa run domains/physics/tabletop-blackhole/tabletop_blackhole.hexa --self-test
__TABLETOP_BLACKHOLE__ PASS
case1=PASS case2=PASS case3=PASS
```

3 cases: locked (n=6 anchors fire), off-lock (B=1T → diagnostic OFFLOCK),
edge input (N<0 → FAIL:input rejection).

## n6-arch git

- branch: `main`
- commit: `b59d38b3` (joined with sister fusion_ledger)
- pushed to GitHub: yes

## nexus cleanup pending (user action)

```sh
cd /Users/ghost/core/nexus
git status modules/tabletop_blackhole
# Confirm 2 deletions staged:
#   deleted: modules/tabletop_blackhole/README.md
#   deleted: modules/tabletop_blackhole/tabletop_blackhole.hexa
git commit -m 'refactor(nexus): remove tabletop_blackhole module — absorbed into CANON@b59d38b3'
```

`__pycache__/` and `tests/__pycache__/` remain untracked under nexus
(gitignored). `state/markers/tabletop_blackhole_*.marker` historical run
markers preserved as audit trail.

## Caveats (4 honest)

1. Destination diverged from recipe (experiments/ → domains/physics/)
   for co-location consistency with predecessor research spec.
2. Steinhauer-2014 specificity: independent replications (Dornheim 2019,
   etc.) NOT encoded as additional anchor sets.
3. n=6 anchors are heuristic post-hoc mappings (sigma·tau=48,
   sigma−phi=10, sigma/(tau·n)=0.5) — NOT derived from QFT-curved-spacetime
   first principles. Underlying physics derivation lives in tabletop-blackhole.md
   TBHL-01..08, NOT verified by this module.
4. tests/ pyc-only (no source) + cross-tree git history split between
   n6-arch@b59d38b3 and nexus@bcadbf6d. @origin SHA documented in
   .README.md but not enforced via git mechanism.

## Marker

`anima/state/markers/tabletop_blackhole_extraction_landed.marker`
