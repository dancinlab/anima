# mc_integrate decouple + standalone extraction landed (2026-05-04)

## Summary
`mc_integrate` carved out from `nexus/modules/mc_integrate/` to standalone repo
`/Users/ghost/core/mc-integrate/` (commit `a55535c`, GitHub
`dancinlab/mc-integrate`).

Decouples the `anu_source` direct dependency: mc-integrate now consumes QRNG
bytes via `qrng` standalone CLI shellout (4-tier resolver) instead of importing
ANU REST internals directly.

## Artifacts
- Standalone repo: `/Users/ghost/core/mc-integrate/` (CHANGELOG, cli, examples, .git)
- Decouple audit: `state/mc_integrate_decouple_2026_05_04/audit.json`
- Before/after diff: `state/mc_integrate_decouple_2026_05_04/before_after.diff`
- Smoke test: `state/mc_integrate_decouple_2026_05_04/smoke.json`
- Baseline + post-patch selftest logs in same dir
- GitHub: <https://github.com/dancinlab/mc-integrate> (commit `a55535c` pushed)
- Marker: `state/markers/mc_integrate_decouple_landed.marker`

## HF mirror
NOT created (Option A policy 2026-05-04: CLI tools GitHub-only, HF reserved
for model weights / datasets).

## Nexus follow-up
`nexus/modules/mc_integrate/` SCRUB deferred — sister BG `aa896d07` was stopped
mid-flight (hexa runtime hang). Standalone repo is functionally complete; nexus
internal copy still present and unchanged. Apply 4-tier CLI shellout pattern in
nexus next cycle (mirror `nexus/cli/qrng.hexa` v0.1.0 layout).

## Caveats
1. Decouple BG was killed at ~90% — handoff doc + nexus consumer rewrite
   remained when stopped. This doc closes the standalone side; nexus side
   carries forward as a TODO.
2. `before_after.diff` shows the in-tree mc_integrate edit (`anu_source` →
   `qrng_shellout`); that edit is unstaged in nexus working tree per scrub BG
   handoff.
3. No HF API call attempted (Option A — see policy in
   `state/hf_mirror_delete_2026_05_04/audit.json`).
4. v1.0.0 ships as Apache-2.0 with provenance line in `hexa.toml` pointing at
   `nexus/modules/mc_integrate/` origin.
5. Smoke covers MC integral on toy distributions; full statistical
   self-validation deferred to consumer-side tests.
