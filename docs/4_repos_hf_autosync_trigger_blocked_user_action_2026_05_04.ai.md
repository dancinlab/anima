# 4 Repos HF Auto-Sync Trigger — BLOCKED (User Action Required)

**Date:** 2026-05-04
**Status:** BLOCKED — user prerequisite ("HF 준비 됨" claim) was inaccurate; HF_TOKEN secret NOT set on any of 4 repos.
**Marker:** `state/markers/4_repos_hf_autosync_trigger_blocked_user_action_required_2026_05_04.marker`
**Audit:** `state/4_repos_hf_autosync_trigger_2026_05_04/{audit.json, run_results.jsonl}`

## Summary

| Repo | Dispatch | Run | Conclusion | Secret count | Root cause |
|---|---|---|---|---|---|
| qmirror | SUCCESS | 25305405327 | **failure** | 0 | HF_TOKEN missing (loud step-gate) |
| sim-universe | SUCCESS | 25305406595 | **failure** | 0 | HF_TOKEN missing (loud step-gate) |
| hexa-bio | **FAILED HTTP 422** | n/a | n/a | 0 | YAML syntax error (silent job-level `if: ${{ secrets.HF_TOKEN != '' }}` invalid) + secret missing |
| honesty-monitor | SUCCESS | 25305409672 | **failure** | 0 | HF_TOKEN missing (loud step-gate) |

## Verification Evidence

```
gh api repos/need-singularity/qmirror/actions/secrets         → {"total_count":0,"secrets":[]}
gh api repos/need-singularity/sim-universe/actions/secrets    → {"total_count":0,"secrets":[]}
gh api repos/need-singularity/hexa-bio/actions/secrets        → {"total_count":0,"secrets":[]}
gh api repos/need-singularity/honesty-monitor/actions/secrets → {"total_count":0,"secrets":[]}
```

Failed-run logs show explicit `::error::HF_TOKEN secret is not set.` with `HF_TOKEN: ` (empty) in env block.

## User Actions Required (3)

1. **Set HF_TOKEN secret on each of 4 repos** (write-scope token from https://huggingface.co/settings/tokens):
   ```
   gh secret set HF_TOKEN --repo need-singularity/qmirror         --body "hf_xxx..."
   gh secret set HF_TOKEN --repo need-singularity/sim-universe    --body "hf_xxx..."
   gh secret set HF_TOKEN --repo need-singularity/hexa-bio        --body "hf_xxx..."
   gh secret set HF_TOKEN --repo need-singularity/honesty-monitor --body "hf_xxx..."
   ```

2. **Fix hexa-bio workflow YAML** (line 20): replace job-level `if: ${{ secrets.HF_TOKEN != '' }}` (invalid — `secrets` ctx unavailable in job-level conditionals) with the loud step-gate pattern from qmirror/sim-universe/honesty-monitor. Until fixed, `workflow_dispatch` will keep returning HTTP 422 before any run is created.

3. **Re-trigger** all 4: `gh workflow run sync-to-hf.yml --repo need-singularity/<repo>` and verify SUCCESS.

## Caveats

1. User claim "HF 준비 됨" was empirically false (4/4 repos have 0 secrets) — recommend reverify human-side state before next claim of "준비 됨".
2. hexa-bio's silent job-level gate is structurally broken, not just unconfigured — ANY dispatch fails until YAML fixed (independent of HF_TOKEN).
3. HF `lastModified` timestamps observed today are stale (from prior pushes), not from today's failed dispatches.

## Cost

$0 (all GitHub Actions runs were public-repo free tier; failures consumed seconds-level minutes).
