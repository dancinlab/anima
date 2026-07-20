# Typed workspace production falsification result

## Verdict

**WIRED and causally active.** This closes the earlier boundary where G6 produced falsifiable form
but selected before reading evidence.

The canonical 303M run used one typed `.kosmos` contradiction fact targeting the first G6 primary
candidate. The same frozen G1/G6 functions and checkpoint were used.

```text
evidence: 1 typed fact(s)
G1 pass=True best_distinct=5 max_single=2 noecho=3 echo_suspect=False
G6 pass=True dist=6 fals=6 coherent=6 frame_leaks=0
FALSIFY rejected=1 abstained=0 decisions=10
decision[4]
  candidates=workspace-claim-33ecc325-0,workspace-claim-32ecc192-1
  selected=workspace-claim-32ecc192-1
  rejected=workspace-claim-33ecc325-0
WORKSPACE_REACH: PASS
```

Controls covered by `tests/test_cognitive_workspace.py`:

- OFF: primary remains selected.
- ON: matching primary contradiction selects the alternative.
- SHUFFLE: non-matching evidence leaves output identical to OFF.
- ALL-FALSIFIED: no candidate reaches the mouth; explicit abstention is returned.
- `.kosmos` round-trip: evidence written by the canonical writer changes live mouth selection after
  reading through the canonical loader.

## Scope

This proves that grounded evidence can causally change or suppress a production workspace decision.
It does not certify that every evidence source is true: evidence provenance remains a trust boundary.
The live affect comparator can create contradiction facts, while `--workspace-evidence` supplies the
production persistence/read seam.
