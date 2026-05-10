# GROWTH_STAGES alignment diff — historical vs aligned

## Schemas

| | historical (worktree-2 GROWTH_STAGES, 4-stage) | aligned (5-stage, dev_stage merged) |
|---|---|---|
| stage 0 | min_int=0, 1/128/2 | newborn, min_int=0, 1/128/2 |
| stage 1 | min_int=**50**, 2/128/2 | infant, min_int=**100**, 2/128/2 |
| stage 2 | min_int=**200**, 3/192/3 | toddler, min_int=**500**, 3/192/3 |
| stage 3 | min_int=**800**, 6/384/4 | child, min_int=**2000**, 6/384/4 |
| stage 4 | (none) | adult, min_int=10000, 6/384/4 (topology stable) |

## Trade-off

Historical thresholds (50/200/800) are tighter and let mitosis fire ~4x
faster, which is what the RC-9 +52.76% evidence run likely consumed.
Aligned thresholds (100/500/2000) match `growth_engine.STAGES` developmental
psychology (newborn/infant/toddler/child/adult) — semantically coherent
but pushes full topology (6/384/4) past the 800-interaction mark that
RC-9 measured at. Adult stage is **topology-idempotent** (no further block
expansion); growth_engine declares adult as "stable self, slow learning."

## Reproducibility risk (honest C3)

C3-1: aligned thresholds NOT validated against RC-9 +52.76% baseline.
C3-2: 50→100, 200→500, 800→2000 changes effective curriculum length 2-2.5x
      per stage; LR schedule + curiosity decay rates were tuned for the
      faster historical curve.
C3-3: `growth_engine.mitosis_threshold` is 999 (unreachable) for newborn/
      infant — aligned schema's first allowed mitosis is at toddler
      (min_int=500), but `growing_conscious_lm` historically allowed
      mitosis at min_int=50 (infant). Hard semantic conflict.
C3-4: `growth_engine.STAGES` has 9 axes (LR/curiosity/habituation/mitosis_
      threshold/emotional_range/metacog_depth/homeostasis/dream/breath);
      aligned ref only encodes topology + min_interactions + dev_stage —
      the other 6 axes must be sourced from growth_engine at runtime.
C3-5: no test fixture exists that exercises both modules end-to-end;
      alignment is by-inspection only.

## Usage guidance

**Recommended**: monkeypatch at runtime, not source replacement.

```python
import growing_conscious_lm as gcl
from state.anima_lost_asset_fixes_2026_05_10.growth_stages_aligned import (
    GROWTH_STAGES_ALIGNED,
)
gcl.GROWTH_STAGES = GROWTH_STAGES_ALIGNED  # 5-entry; index 0..3 compatible
```

Direct edit of `worktree-2/growing_conscious_lm.py:20` is **not advised**
until RC-9 reproducibility is re-verified with aligned thresholds.
raw#15 additive: keep historical 4-stage as default, opt-in monkeypatch
for dev_stage-aware experiments.

If the experiment requires `growth_engine.GrowthEngine` and
`GrowingConsciousLM` to advance stages in lockstep, use the aligned shim;
otherwise leave both modules unchanged and document which clock is
authoritative for the run.
