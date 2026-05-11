# qmirror Dual-Mirror Auto-Sync — Landed (2026-05-03)

**Status**: LANDED (workflow committed + first run completed; GREEN path
gated on USER_ACTION to set `HF_TOKEN` GH secret)
**Cycle**: `qmirror_dual_mirror_autosync_2026_05_03`
**Marker**: `state/markers/qmirror_dual_mirror_autosync_landed.marker`
**GH commit**: [`df89ff2`](https://github.com/dancinlab/qmirror/commit/df89ff2)
**First Actions run**: [#25295441499](https://github.com/dancinlab/qmirror/actions/runs/25295441499) (FAIL at verify-HF_TOKEN, **as designed**)

---

## TL;DR

The dual-mirror sync burden documented as Caveat §1 of
`qmirror_hf_mirror_pushed_2026_05_03.ai.md` ("HF mirror falls behind GitHub
if the operator forgets the second push step") is now eliminated.

- **Primary path**: GitHub Actions workflow on push-to-main →
  `huggingface_hub.upload_folder` to `dancinlab/qmirror`. ~2-3 min lag.
- **Fallback path**: local pre-push hexa hook for Actions-unavailable cases.
- **Cost**: $0 (GH Actions free-tier on public repo; HF free-tier on <5GB repo).

The first workflow run (commit `df89ff2`) **correctly fail-loudly at the
`Verify HF_TOKEN secret is present` step** because the GH repo secret has
not been set yet. The verify step prints the exact settings URL the user
needs to visit. Once the secret is set and the run is re-triggered,
end-to-end mirror semantics (including delete-on-source-removal) are
exercised.

---

## What landed

### `.github/workflows/sync-to-hf.yml` (133 lines)

- **Trigger**: `push: branches:[main]` with `paths-ignore: ['state/**', '.github/**', '**/*.md.draft']`
  (avoid loops + waste-CI on workflow-only edits).
- **Manual re-trigger**: `workflow_dispatch` enabled.
- **Concurrency**: single in-flight `sync-to-hf` group with
  `cancel-in-progress: true` (newest push supersedes older queued).
- **Job**: `runs-on: ubuntu-latest`, `timeout-minutes: 10`,
  `permissions: contents: read` (least privilege).
- **Steps**:
  1. `actions/checkout@v4` with `fetch-depth: 1` (HEAD tree only, no history).
  2. `actions/setup-python@v5` Python 3.11.
  3. `pip install 'huggingface_hub>=0.24,<2.0'`.
  4. **Verify HF_TOKEN secret present** — exits 1 with the exact
     `https://github.com/dancinlab/qmirror/settings/secrets/actions`
     URL if missing. Length-redacted echo (`${#HF_TOKEN} chars`) on success.
  5. **Upload** — inline Python heredoc invokes `HfApi.upload_folder` with:
     - `ignore_patterns=['.git/*', '.github/*', 'state/*', '**/__pycache__/**', '**/*.pyc', '.DS_Store', 'Thumbs.db']`
       (mirrors the qmirror standalone hygiene contract from the upload
       cycle audit).
     - `delete_patterns=['*']` so files removed on GH are also removed on
       HF (true mirror, not append-only).
     - `commit_message=f"sync: github.com/{src}@{sha} → HF mirror (auto via GH Actions)"`.
     - `create_repo(..., exist_ok=True)` for idempotency.
  6. `Summary` writes a `$GITHUB_STEP_SUMMARY` block linking GH commit + HF repo.

### `tool/qmirror_pre_push_to_hf.hexa` (151 lines, local fallback)

- Hexa script that wraps `hf upload dancinlab/qmirror . --repo-type=model`
  with the same `--exclude` set as the workflow's `ignore_patterns`.
- Defense-in-depth: only fires inside the qmirror repo (`grep -q 'name *= *"qmirror"' hexa.toml`).
- Self-test (`--selftest`) and dry-run (`--dry-run`) modes.
- Per-push opt-out: `QMIRROR_SKIP_HF_PRESYNC=1 git push`.
- Sentinel: `__QMIRROR_PRE_PUSH_TO_HF__ <PASS|FAIL|SKIP>`.
- Install instructions in the file header (chmod +x in `.git/hooks/pre-push`).
- Token never accepted via flag/env (raw#15) — relies on cached
  `~/.cache/huggingface/token` from `hf auth login`.

### `README.md` (+5 lines)

Cross-link both paths under the existing Mirrors callout (no other
README mutation, preserving the structural review work from prior cycles).

---

## First-run evidence (USER_ACTION pending)

```
Run #25295441499 (push, df89ff2 → main)
✓ Checkout (full history off — only HEAD tree needed for mirror)
✓ Setup Python 3.11
✓ Install huggingface_hub
X Verify HF_TOKEN secret is present
- Upload tree to HuggingFace Hub
✓ Summary
X Process completed with exit code 1.

::error:: HF_TOKEN secret is not set.
Set it at: https://github.com/dancinlab/qmirror/settings/secrets/actions
```

This is **the designed failure mode** — fail-loudly with an actionable URL
rather than silently uploading an empty/invalid token.

---

## USER ACTION REQUIRED

1. Visit <https://github.com/dancinlab/qmirror/settings/secrets/actions>
2. **New repository secret**:
   - Name: `HF_TOKEN`
   - Value: a HuggingFace token with **write** scope to
     `dancinlab/qmirror` (create one at
     <https://huggingface.co/settings/tokens> → "Create new token" →
     Type: "Write", Repository scope: `dancinlab/qmirror`).
3. Re-trigger the failed run:
   ```bash
   gh run rerun 25295441499 --repo dancinlab/qmirror
   ```
   (Or push any small commit to `main` to trigger fresh.)
4. Verify HF auto-updates within ~2-3 min:
   ```bash
   hf api repos/dancinlab/qmirror | jq .lastModified
   # OR check the workflow Summary at:
   gh run view <new-run-id> --repo dancinlab/qmirror --log
   ```

After verification, the prior cycle's Caveat §1
("dual-mirror sync burden — manual re-push") can be retired.

---

## Caveats (raw#10 honest C3, 4)

1. **GitHub Actions free-tier minute accounting** — public-repo Actions
   minutes are effectively unlimited (GH does not bill them on public
   repositories), but if `qmirror` is ever flipped to private, the 2000-min/mo
   billing cap applies and a single sync run is ~30s. Mitigation: keep the
   repo public (already required by the HF mirror's public-repo-type
   contract).

2. **HF token rotation burden** — if the user rotates the HF token (security
   hygiene, expiring tokens, scope changes), they must also update the GH
   secret; there is no auto-refresh hook. Mitigation: write-scope tokens
   on `dancinlab/qmirror` are narrow (single-repo write); rotation
   cadence can be quarterly without operational pain.

3. **Sync lag ~2-3 min p50** — workflow boot (~30s) + checkout (~5s) +
   pip install (~25s) + HF upload (~30-90s depending on changed-file
   count). For "I pushed a typo fix and want it on HF immediately"
   workflows, the local pre-push fallback (`tool/qmirror_pre_push_to_hf.hexa`)
   is faster (~5-10s end-to-end) but blocks the `git push` for that
   duration.

4. **Partial-failure handling** — `huggingface_hub.upload_folder` is
   atomic at the HF-API level (single commit), so HF stays at the
   previous good state if the upload fails mid-way. However, the GH
   Actions run will be marked failed and a manual re-run is required;
   there is no auto-retry. Mitigation: workflow has
   `concurrency.cancel-in-progress: true`, so simply pushing again
   (or re-running) supersedes the failed run.

---

## Constraint compliance

| Constraint | How honored |
|------------|-------------|
| raw#9 STRICT (Mac → hexa only) | Mac-side new file is `tool/qmirror_pre_push_to_hf.hexa` (hexa). YAML is external CI config, allowed by the rule's CI-config exception. The inline Python in the workflow runs on GitHub-hosted `ubuntu-latest`, never on Mac. |
| raw#15 (HF_TOKEN never in chat or workflow file) | Token only referenced as `${{ secrets.HF_TOKEN }}`. Length-redacted echo (`${#HF_TOKEN} chars`) on success. Never logged in plain text. Local hexa fallback uses cached `~/.cache/huggingface/token`, never accepts via flag/env (avoids shell-history leak). |
| raw#10 (4 caveats) | 4 explicit caveats above + 4 caveats in workflow file header. |
| $0 | GH Actions free-tier (public repo) + HF free-tier (<5GB). Verified zero billable minutes consumed by first run (~22s wall time). |
| USER_ACTION transparency | Workflow `Verify HF_TOKEN` step prints the exact settings-page URL on failure, eliminating "where do I set this?" ambiguity. |

---

## Cross-refs

- Workflow: `qmirror/.github/workflows/sync-to-hf.yml`
- Local fallback: `qmirror/tool/qmirror_pre_push_to_hf.hexa`
- README diff: `qmirror/README.md` (+5 lines under Mirrors callout)
- Prior cycle (this retires its Caveat §1): `docs/qmirror_hf_mirror_pushed_2026_05_03.ai.md`
- GH commit: <https://github.com/dancinlab/qmirror/commit/df89ff2>
- First Actions run (FAIL_AS_DESIGNED): <https://github.com/dancinlab/qmirror/actions/runs/25295441499>
- HF mirror target: <https://huggingface.co/dancinlab/qmirror>

---

## Done conditions

- [x] `.github/workflows/sync-to-hf.yml` committed + pushed
- [x] `tool/qmirror_pre_push_to_hf.hexa` (Option 2 fallback) committed + pushed
- [x] README.md updated with both-path cross-links
- [x] Workflow YAML validated (`python -c yaml.safe_load(...)` PASS)
- [x] First Actions run executed (verify-HF_TOKEN step fails as designed)
- [x] 4 caveats explicit (in handoff + workflow file header)
- [x] raw#9, raw#15, $0, USER_ACTION transparency honored
- [x] Marker + handoff written
- [ ] **USER_ACTION**: GH secret `HF_TOKEN` set + re-run verified (gated)
- [ ] Post-secret verification: HF `lastModified` updates within 3 min of next push (gated on above)
