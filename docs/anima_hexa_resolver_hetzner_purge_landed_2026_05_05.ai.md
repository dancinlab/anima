# anima · hexa-resolver hetzner/htz purge — landed 2026-05-05

**Lane**: `BG-HEXA-RESOLVER-HETZNER-PURGE`
**Status**: complete
**User-facing impact**: hexa-resolver no longer attempts retired hetzner/htz hosts; DNS-fail noise eliminated.

## Why

User directive 2026-05-05: hetzner/htz subscription cancelled. Resolver was iterating
chain `[hetzner, ubu1, ubu2, htz]` — each invocation produced two `DNS 해석 실패` lines
before reaching ubu1/ubu2. Active references existed across `~/.hx/bin/`, nexus
scripts, hexa-url-handler, .workspace, and hive-resource toml.

## Pre-purge selftest evidence

```
$ HEXA_RESOLVER_VERBOSE=1 hexa run /tmp/test.hexa
hexa-resolver: route=external reason=pool_reachable
hexa_remote: host=hetzner 실패: DNS 해석 실패
hexa_remote: host=htz 실패: DNS 해석 실패
hexa_remote: LB=score pick=ubu2 ...
```

## Files modified (6)

| Path | Change |
|---|---|
| `/Users/ghost/core/nexus/scripts/bin/hexa_remote` | `_DYNAMIC_HOSTS` fallback chain `"hetzner ubu1 ubu2 htz"` → `"ubu1 ubu2"`; htz->hetzner normalization → retired-alias→ubu1 fallback; heavy-compute always-hetzner pin removed |
| `/Users/ghost/.hx/bin/_cache.sh` | nc reachability fallback dropped 157.180.8.154/hetzner branch (kept ubu1 → tailscale → vast) |
| `/Users/ghost/.hx/bin/cargo` | airgenome cargo wrapper hetzner SSH fallback removed; hexa-lang offload now ubu1-only |
| `/Users/ghost/.hx/bin/hexa-url-handler.sh` | `htz/rescue` + `htz/poll` URL handlers deleted; `recovery/fleet` hardcoded fallback `"ubu1 ubu2 hetzner"` → `"ubu1 ubu2"` |
| `/Users/ghost/core/.workspace` | host_pool_summary htz line marked DEPRECATED; `resource host.htz` block replaced with deprecation comment; member exports/imports for nexus/anima/void/hive dropped `host.htz@nexus`; `command offload` description updated |
| `/Users/ghost/.hx/packages/hive-resource/hexa.toml` | description string dropped "hetzner" from inventory examples |

## Files preserved (raw#15 historical)

- `~/.hx/bin/hexa` (uchg-sealed) — runtime is host-agnostic via `_pool_any_reachable`; comment-only refs left intact
- `~/.hx/bin/nexus` — comment narrative only
- `~/.hx/packages/orpheus/state/system/{hexa.resolver.2026_05_04.bash, README.md}` — backup + handoff
- `~/.hx/packages/orpheus/dormant_explorer/module/metrics.hexa` — `impl_hetzner_full_retire_propagation` status=done (THIS work's roadmap entry)
- `~/.hx/log/*.{log,err}`, `~/.hx/packages/orpheus/docs/*.ai.md` — historical artifacts
- `core/hexa-brain/eeg/*.hexa` — comment narrative about argv portability
- `core/hive/{kick/lint/*, design/kick/*.json}` — kick witness JSONs (commit + audit history)
- `core/anima/state/*` — jsonl/log/landed artifacts
- `~/.ssh/config` — already cleaned 2026-05-01 (REMOVED stanza); no edit needed this cycle

## Post-purge selftest

```
$ HEXA_RESOLVER_VERBOSE=1 hexa run /tmp/test.hexa  (x2)
hexa-resolver: route=external reason=pool_reachable
hexa_remote: LB=score pick=ubu2 (avail=28485MB ...) among: ubu1(...) ubu2(...)
hexa_remote: ubu2 에서 원격 실행 중

$ cat ~/.hx/cache/remote_preflight.json
{"ts":1777975130,"hosts":["ubu1","ubu2"],"port":22,"ok":["ubu1","ubu2"]}
```

Zero `hetzner`, zero `htz`, zero `DNS 해석 실패` lines. Pool auto-converged to `[ubu1, ubu2]`.

## Honest C3 (8)

See `state/hexa_resolver_hetzner_purge_2026_05_05/verdict.json` for full list. Highlights:

1. `~/.hx/bin/hexa` (uchg-sealed) **not modified** — host-agnostic at runtime; uchg unseal would add diff surface without behavior delta.
2. Dead-code branch at `hexa_remote:1808` (`if HOST = hetzner|htz: MEM_MAX=80G`) deliberately left intact (unreachable but cosmetic to remove).
3. `metrics.hexa` action `impl_hetzner_full_retire_propagation` is THIS retirement work's roadmap entry (status=done) — preserved as completion evidence.
4. `remote_preflight.json` cache **auto-regenerated** post-edit, organically dropping retired hosts. Cleanest signal of active-path propagation.
5. ssh config already pristine (cleaned 2026-05-01).

## Follow-up (optional, non-blocking)

- Prune dead `hexa_remote:1808` HOST=hetzner branch (cosmetic).
- Cycle uchg-sealed `~/.hx/bin/hexa` to strip 7 historical comment refs (no behavior change).
- Doc-only sweep through `hexa-brain/eeg/*.hexa` argv portability comments.

## raw compliance

- raw#9 (config + .ai.md companion): YES
- raw#10 (≥5 honest C3): YES (8)
- raw#15 (active config purge OK + historical preserve): YES

## No git commits made

Per session spec: anima/hexa-lang/hive/hexa-brain all left dirty for user review. Working
tree contains the 6 modifications above plus this companion doc + verdict.json.
