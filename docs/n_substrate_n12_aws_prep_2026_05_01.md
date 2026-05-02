# N-12 AWS Braket Round 2 — Local Artifacts Ready

**Date**: 2026-05-01
**Agent**: `n12_aws_braket_prep`
**Round 1 spec**: [`state/n_substrate_n12_prep_2026_05_01/`](../state/n_substrate_n12_prep_2026_05_01/)
**Round 2 manifests**: [`state/n_substrate_n12_aws_prep_2026_05_01/`](../state/n_substrate_n12_aws_prep_2026_05_01/)
**Off-repo scripts**: `/Users/ghost/n12_braket/` (HEXA-only repo policy)

---

## Mission

Round 1 produced the spec. Round 2 produces the **launchable artifacts** so
that the moment user finishes AWS Braket onboarding, the $20.90 MVP runs
with one command.

## Deliverables

### Off-repo (Mac local, NOT in anima git)

| Path | Purpose | Status |
|------|---------|--------|
| `/Users/ghost/n12_braket/submit_braket.py` | builds C1/C2/C3 circuits, submits to IonQ Forte 1, $50 hard-cap | READY |
| `/Users/ghost/n12_braket/verify_F_N12_1.py` | F-N12-1 falsifier verifier, computes tau_2 ratio, emits PASS/FAIL/INDETERMINATE | READY |
| `/Users/ghost/n12_braket/launch.sh` | one-command launcher (dry-run default, --live for spend) | READY |

### In-repo (anima)

| Path | Purpose |
|------|---------|
| `state/n_substrate_n12_aws_prep_2026_05_01/aws_onboarding_checklist.json` | 10-step user-facing checklist |
| `state/n_substrate_n12_aws_prep_2026_05_01/launch_manifest.json` | full artifact registry + verdict |
| `docs/n_substrate_n12_aws_prep_2026_05_01.md` | this file |

## One-liner launch

After AWS onboarding (10 steps in `aws_onboarding_checklist.json`):

```bash
# dry-run (no spend, validates circuits + cost)
bash /Users/ghost/n12_braket/launch.sh

# live submit ($20.90 spend on Forte 1)
export BRAKET_S3_BUCKET=amazon-braket-us-east-1-<acct-id>
bash /Users/ghost/n12_braket/launch.sh --live

# verify F-N12-1 after IonQ returns results (1-3 days)
python3 /Users/ghost/n12_braket/verify_F_N12_1.py \
    /Users/ghost/n12_braket/results_<ts>.json \
    --sc-tau2-us <PRNewswire-2025-03-value>
```

## Cost cap

- **Soft cap**: AWS CloudWatch billing alarm at $50 (notification only)
- **Hard cap**: script-side `HARD_CAP_USD = 50.00` rejects any submit that
  estimates above $50; also requires explicit `--confirm-spend-USD` matching
  estimate within $0.50

## Honest C3 — items pending user verification

| Item | Action |
|------|--------|
| Forte 1 ARN exact string | user verifies in Braket console; edit `DEVICE_ARN_PREDICTED` if differs |
| Pulse-level delay support | script uses identity-stack proxy (`delay_us // 8`); true pulse delay needs OpenQASM 3 device check |
| PRNewswire SC tau_2 numeric | user extracts from 2025-03 article and passes via `--sc-tau2-us` |
| S3 bucket name | discovered after Braket service enable (auto-named `amazon-braket-us-east-1-<acct-id>`) |

## Blockers

**Agent-side**: none. All local artifacts written and ready.
**User-side**: AWS onboarding (~80 min total user time, ~30 min hands-on),
PRNewswire reference extraction, IonQ scheduling wait (1-3 days).

## Verdict

`LOCAL_READY_AWAITING_USER_AWS_ONBOARDING`
