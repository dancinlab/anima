H_881 progressive freeze (BOUND E5 dynamic) — verdict backing dir (hexa-native-guard).

Canonical verdict + curve live in .verdicts/clm-progressive-freeze/
  F-CLM-PROG-FREEZE_prereg.txt  — frozen thresholds (bf98c01 verbatim, post-tuning 0)
  F-CLM-PROG-FREEZE.txt          — verdict verbatim (🟢/🔴 + schedule→checkpoint curve)
  clm_progressive_freeze_result.json  — full machine-readable per-schedule per-checkpoint result

Scaffold: CLM/model/h881_progressive_freeze.hexa
Hypothesis: UNIVERSE/H_881_clm_progressive_freeze.md

Builds on H_872 (🟢, .verdicts/clm-freeze-depth/): H_872 measured a STATIC freeze depth
at END of session only; H_881 moves the freeze boundary DYNAMICALLY across a 6-segment
session and checks RETAIN∧GAIN at EVERY checkpoint (sustained), not just at the end.
