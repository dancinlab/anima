# fusion_ledger extraction handoff (2026-05-04)

## Status: LANDED (n6-arch) + STAGED (nexus delete, awaiting user commit)

## What landed

- `CANON/domains/energy/fusion/fusion_ledger.hexa` (314 LoC)
- `CANON/domains/energy/fusion/fusion_ledger.README.md` (62 LoC)
- Co-located with `fusion.md` + `verify_fusion.hexa` predecessors

## Smoke (n6-arch root)

```
$ hexa run domains/energy/fusion/fusion_ledger.hexa --self-test
__FUSION_LEDGER__ PASS total=27 matched=26 falsified=1 pct=96.2963
```

Honest 26/27 PASS preserved (lawson_triple one-decade gap is intentional).

## n6-arch git

- branch: `main`
- commit: `b59d38b3` (joined with sister tabletop_blackhole)
- pushed to GitHub: yes

## nexus cleanup pending (user action)

```sh
cd /Users/ghost/core/nexus
git status modules/fusion_ledger
# Confirm 2 deletions staged:
#   deleted: modules/fusion_ledger/README.md
#   deleted: modules/fusion_ledger/fusion_ledger.hexa
git commit -m 'refactor(nexus): remove fusion_ledger module — absorbed into CANON@b59d38b3'
```

`__pycache__/`, `data/iter_constants.json`, and `tests/__pycache__/` remain
untracked under nexus (gitignored). Optionally `rm -rf modules/fusion_ledger/`
after commit if a fully clean delete is preferred.

## Caveats (4 honest)

1. `data/iter_constants.json` not relocated — n6-arch .gitignore excludes
   `data/` recursively. JSON mirror stays at nexus side; .hexa is
   self-contained via inline 27-entry table. Future: re-add under non-data/
   path if external override hooks needed.
2. tests/ subdir contains only stale .pyc remnants (no .hexa/.py source).
   --self-test in CLI covers all 5 falsifier checks.
3. lawson_triple one-decade gap (5.6e21 measured vs 5.6e20 closed-form)
   is the deliberate honesty contract. Self-test will FAIL if anyone
   silently inflates 26→27.
4. n=6 closed-form ownership ambiguity: same 7 anchors duplicated across
   atlas_n6 + crystallography_n6 + chip_isa_n6 + fusion_ledger.
   Intentional decoupling per raw#15; drift risk documented.

## Marker

`anima/state/markers/fusion_ledger_extraction_landed.marker`
