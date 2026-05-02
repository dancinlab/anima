# Upstream tribev2 PR Results — 2026-05-02

## Verdict: PASS — PR #60 OPEN against `facebookresearch/tribev2`

- PR URL: https://github.com/facebookresearch/tribev2/pull/60
- PR title: `docs: anima integration proposal addendum (Framing D 3-way bridge: EEG<->CLM<->TRIBE BOLD)`
- Branch: `dancinlife:docs/anima-integration-addendum-2026-05-02`
- Diff: +102 lines, 1 file (`ANIMA_INTEGRATION_PROPOSAL_ADDENDUM_2026_05_02_EN.md`)

This is anima's first external academic-track contribution (separate trajectory from the Levin Lab outreach #N-22 sent the same day).

## Phase-by-phase

| phase | task | result |
|---|---|---|
| 1 | Setup verify (remotes, gh auth, fork sync) | PASS — note: remote names `origin`/`fork` were swapped from mission spec (origin = facebookresearch, fork = dancinlife). Adapted operations without modifying remote config. |
| 2 | English translation of Korean addendum | PASS — 1223 EN words from 1133 KR source; all 8 sections (§1 frozen baseline note, §2 #95 finding, §3 Axis 3 REVISE, §4 4-framing matrix, §5 Top-3 falsifiers, §6 pilot status, §7 5-axis fit, §8 honest C3) preserved verbatim. |
| 3 | Branch + commit + push to fork | PASS — branched from `origin/main` (upstream 7239908) so PR diff shows only the new EN file. Commit `1731059` pushed to `fork/docs/anima-integration-addendum-2026-05-02`. Authored as Min Woo Park <nerve011235@gmail.com>. |
| 4 | Submodule pointer commit in parent repo | PASS — anima parent commit `329dfd890` bumps `references/tribev2`. Not pushed (per HARD constraint — user controls main repo push timing). |
| 5 | PR open | PASS — PR #60 OPEN. |
| 6 | Ledger + report | PASS — `state/upstream_tribev2_pr_2026_05_02/pr_status.json` and this doc. |

## Files touched

- `references/tribev2/ANIMA_INTEGRATION_PROPOSAL_ADDENDUM_2026_05_02_EN.md` (new, in submodule on PR branch)
- `state/upstream_tribev2_pr_2026_05_02/pr_status.json` (new)
- `docs/upstream_tribev2_pr_results_2026_05_02.md` (this file, new)
- Parent submodule pointer for `references/tribev2` (committed, not pushed)

## Files NOT touched (per HARD constraints)

- `references/tribev2/ANIMA_INTEGRATION_PROPOSAL.md` — frozen baseline, raw#1 immutability preserved.
- `references/tribev2/ANIMA_INTEGRATION_PROPOSAL_ADDENDUM_2026_05_02.md` — Korean original preserved unmodified (lives on fork's main branch, not in this PR's diff).
- Parent anima repo not pushed.

## 5-line excerpt of EN addendum (§3 Axis 3 REVISE opening)

```
**Original baseline §1 Axis 3 grounds for "No fit"**:
1. "wrapper would be large in scale"
2. "scientific value unclear (need to define a meaningful mapping between cortical vertices and cell state)"

**Under Framing D (bridge anchor), both grounds are false**:
```

## Honest C3 (3 items)

1. **Maintainer rejection risk** — facebookresearch maintainers may decline a documentation-only PR proposing a third-party integration as outside the encoder's intended scope. Mitigation: PR body explicitly invites relocation (third-party README link, `examples/` dir).
2. **Translation semantic-drift risk** — English text is Claude-produced and not human-reviewed; subtle Korean technical phrasing may have shifted (e.g. the "Strong fit conditional on Framing D actually working" framing in §8.4, the "rollback" wording in §8.3). Mitigation: Korean original remains canonical on the fork's main branch for cross-reference; future addenda can append corrections without touching either baseline.
3. **PR scope vs fork-main divergence** — the PR is branched from `origin/main` (upstream `7239908`), so the diff is exactly +1 EN file. The Korean addendum (commit `86ed480` already on fork/main) is NOT in this PR's diff. Reviewers wanting Korean<->English parity must visit the dancinlife fork directly. This is the correct behavior for a clean upstream-bound docs PR but worth flagging.

## Cost

- gh API calls: $0
- Wallclock: ~10 min (translation dominated)

## Next steps (out of scope here)

- Watch for maintainer response on PR #60 (typical OSS PR review: days to weeks).
- If accepted: cumulative addendum chain convention is now upstream-blessed.
- If rejected with relocation request: open a follow-up addendum file noting where the EN doc finally lives.
- Push parent anima repo when user signals (parent commit `329dfd890` is local-only).
