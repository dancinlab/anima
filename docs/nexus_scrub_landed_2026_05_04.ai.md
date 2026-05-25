# nexus scrub — 6 standalone modules carved out of nexus internal tree

**Cycle**: 2026-05-04
**Branch**: `feat/qmirror-cli-programmatic-consumption` (nexus repo)
**Commits**: `5b1332ba` (scrub) + `036f1e79` (wire-up)
**Status**: LANDED (local commits only; not pushed)

## Summary

Scrubbed 6 internal modules from `~/core/nexus/` that already exist as
standalone repos in `dancinlab/*`. Refactored consumers to invoke
the standalones via a 4-tier shellout resolver (env → Mac dev path → home
path → PATH bin), with hard-fail + actionable hint when no tier resolves.

## What landed

### Commit 5b1332ba — scrub (deletions)

19 files / 3,131 lines deleted:

- `modules/qrng/` (7 files: anu, curby, hardware_qrng, mock_qrng, nist_beacon, 2 fixtures)
- `core/qrng/` (4 files: qrng_main, registry, router, source)
- `modules/honesty_monitor/` (2 files)
- `modules/crystallography_n6/` (2 files)
- `modules/fusion_ledger/` (2 files; was D-staged from prior session)
- `modules/tabletop_blackhole/` (2 files; was D-staged from prior session)

### Commit 036f1e79 — wire-up

9 files / +1,897 −3:

- **NEW** `cli/qrng.hexa` (v0.1.0) — 4-tier router for standalone qrng v1.0.0
- **NEWLY TRACKED** `cli/honesty.hexa` (v0.1.0), `cli/sim.hexa` (v0.1.0),
  `cli/bio.hexa` (v0.1.0), `cli/agent.hexa` (v0.1.0) — all already
  implemented 4-tier pattern from prior cycles
- `engine/nexus_cli.hexa` — `cmd_qrng` dispatch added; help/subhelp text
  updated to surface qrng + sister CLIs
- `hexa.toml` — `qrng = "^1.0.0"` added; n=6 alignment comment updated
- `install.hexa` — `ensure_runtime_dep("qrng", "^1.0.0")` added
- `README.md` — runtime dependencies table now lists all 6 standalones

## 4-tier resolver pattern (canonical, mirrors qmirror v0.3.0)

```
fn _resolve_<name>_invocation() -> str {
    // tier 1: $<NAME>_ROOT env
    // tier 2: /Users/ghost/core/<name>
    // tier 3: $HOME/core/<name>
    // tier 4: PATH-resolved binary
    // else: return "none|" → caller emits structured 4-tier failure msg + exit 127
}
```

## Smoke results

| Smoke | Result |
|---|---|
| `hexa run cli/qrng.hexa help` | PASS exit 0, "nexus qrng 0.1.0" header |
| `hexa run cli/honesty.hexa help` | PASS exit 0, "nexus honesty 0.1.0" header |
| `hexa run cli/qmirror.hexa help` | PASS exit 0, "nexus qmirror 0.3.0" header |
| `hexa run engine/nexus_cli.hexa qrng help` | PASS exit 0 (dispatch wire OK) |
| `hexa run cli/qrng.hexa status` | PASS exit 0 (standalone resolves via tier 2 → `/Users/ghost/core/qrng`) |

## What was NOT done (honest)

1. **mc_integrate intentionally skipped** — sister BG `aa896d07b3fd43efb`
   is mid-extraction (last activity 07:19 UTC, ~last commit timestamp);
   `modules/mc_integrate/mc_integrate.hexa` working-tree modification was
   left unstaged to avoid racing the sister BG. Follow-up cycle after
   sister lands: scrub `modules/mc_integrate/` + add `cli/mc_integrate.hexa`
   + `cmd_mc_integrate` dispatch + hexa.toml dep + install.hexa.
2. **No remote push** (per constraint).
3. **No PR creation** (per constraint).
4. **No merge to main** (per constraint).
5. **Smoke not exhaustive** — only `--help` and `qrng status` exercised.
   Full subcmd surface (`collect`, `chain`, `meta`, `selftest` etc.) deferred
   to actual callers; the loud-fail contract is the safety net.
6. **n6-arch standalone not yet a hexa.toml dep** — `CANON` is
   the absorber for chip_isa_n6/crystallography_n6/fusion_ledger/tabletop,
   but it has no `cli/<name>.hexa` thin router and is not declared in
   `[dependencies]`. Those 4 modules had zero nexus surface consumers,
   so a thin CLI was unnecessary. If a future consumer surfaces in nexus,
   wire-up will be a follow-up cycle.
7. **Pre-existing working-tree modifications** (`.roadmap.qmirror`,
   `engine/nexus_cli_spec.json`) intentionally NOT included in either
   commit — those are independent in-flight work from prior sessions.

## File paths (absolute)

- Scrub commit: `~/core/nexus@5b1332ba`
- Wire-up commit: `~/core/nexus@036f1e79`
- New thin CLI: `/Users/ghost/core/nexus/cli/qrng.hexa`
- Audit: `/Users/ghost/core/anima/state/nexus_scrub_2026_05_04/audit.json`
- Marker: `/Users/ghost/core/anima/state/markers/nexus_scrub_landed.marker`

## Constraints honored

- raw#9 (hexa-only): all new code is pure `.hexa`; zero new `.py` on Mac
- raw#10 (5 caveats per scrub): documented in commit messages + this handoff
- No git race: sister BG `aa896d07b3fd43efb` owns mc_integrate; this BG
  owns nexus repo exclusively for the 7 other modules; no overlap
- 30-min budget: completed within window
