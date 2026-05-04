# Audit BG → Sister (token-rescue + push) BG handoff

## Audit complete (2026-05-04T07:10Z)

### Repos READY for HF_TOKEN secret set + workflow trigger (5)
All have valid YAML + canonical qmirror step-level loud-fail pattern. Just need secret.

| repo | gh repo | hf mirror | failure cause |
|---|---|---|---|
| qmirror | need-singularity/qmirror | 200 (public) | step-level loud-fail (no secret) |
| sim-universe | need-singularity/sim-universe | 200 (public) | step-level loud-fail (no secret) |
| honesty-monitor | need-singularity/honesty-monitor | 200 (public) | step-level loud-fail (no secret) |
| anima-agent | need-singularity/anima-agent | 401 (likely not yet pushed) | step-level loud-fail (no secret) |
| qrng | need-singularity/qrng | 401 (likely not yet pushed) | step-level loud-fail (no secret) |

For all 5: `gh secret set HF_TOKEN -R need-singularity/<repo> --body "$HF_WRITE_TOKEN"` then `gh workflow run sync-to-hf.yml -R need-singularity/<repo> -r main` (or just push a no-op commit).

### Repo NOT READY: hexa-bio
- Job-level conditional bug: `if: ${{ secrets.HF_TOKEN != '' }}` at job-level returns HTTP 422 startup-failure (zero jobs spawned, no logs).
- Patch staged at `/Users/ghost/core/hexa-bio/.github/workflows/sync-to-hf.yml.proposed` (YAML-validated, mirrors qmirror canonical pattern).
- DO NOT set hexa-bio secret yet — workflow will still 422 until patch is merged. Set hexa-bio secret AFTER user merges the .proposed patch.

### Token state
- All 6 repos: `gh secret list` returned `[]` (no HF_TOKEN set anywhere).
- Sister BG owns: token rescue from /Users/ghost/core/secret/bin/secret + push to GH repo secrets.

### raw#15 confirmed
Audit BG never read or printed token values; only verified absence via `gh secret list --json name`.
