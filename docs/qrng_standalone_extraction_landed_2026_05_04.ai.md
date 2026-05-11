# qrng standalone extraction — LANDED 2026-05-04

## TL;DR

`nexus/modules/qrng/` (5 backends, 1047 LoC) + `nexus/core/qrng/` (4
abstraction modules, 546 LoC) extracted as the **6th publishable HEXA-family
standalone package** at `/Users/ghost/core/qrng/` (v1.0.0, Apache-2.0).

- **GitHub**: <https://github.com/dancinlab/qrng>  (commit 429656c)
- **GitHub Release**: <https://github.com/dancinlab/qrng/releases/tag/v1.0.0>
- **HF mirror**: <https://huggingface.co/dancinlab/qrng>  (intended, **DEFERRED — USER_ACTION required**)
- **Registry**: `hexa-lang/tool/pkg/registry.tsv` L27

## Provenance

- Phase 2 audit: `anima/state/nexus_module_extraction_audit_phase2_2026_05_04/audit.json#qrng`
- Audit verdict: `extract_standalone_qrng_repo_with_caveats` (rank 7, score 7)
- Sister BG context: ad029bfc (audit), this BG = scaffold + push + handoff

## What ships

5 backends with tier coverage T0..T3:

| Tier | Name | is_quantum | Throughput | Cost |
|------|------|-----------:|------------|------|
| T0 | mock_qrng | 0 | 1 GB/s | $0 |
| T1 | curby (Bell-test) | 1 | 8.5 bps | $0 |
| T1 | anu (vacuum-fluctuation) | 1 | 1 KB/s | $0 |
| T1 | nist_beacon (mixed entropy) | 0 | 8.5 bps | $0 |
| T3 | hardware_qrng (PCIe/ESP32) | 1 | 240 MB/s | $5000 / $10 |

Plus 4 abstraction modules (`source.hexa` interface, `registry.hexa` dispatch,
`router.hexa` fallback chain, `qrng_main.hexa` aggregator) + 5 CLI subcmds +
3 examples + 7 fresh tests + install.hexa hx hook + GitHub Actions auto-mirror.

## raw invariants

- **raw#9 STRICT**: pure-hexa; ZERO Python deps; ZERO `_python_bridge`. Only
  system tools (curl + xxd + shasum/sha256sum + timeout).
- **raw#10**: 5 honest C3 caveats embedded (dual-home, 6 consumers, fresh
  tests, ANU rate-limit/ToS, license audit deferred).
- **raw#15**: no token leak; HF_TOKEN referenced only via `secret get` +
  GitHub Actions secret env.
- **cost**: $0 (public GitHub free + HF free tier).

## 5 honest C3 caveats (full text in README + RELEASE_NOTES + state/audit.json)

1. **Dual-home boundary risk** with `qmirror.qrng` — formally documented in
   `qrng/docs/dual_home_boundary.md` with falsifiers F-DUAL-1/2/3 and qmirror
   v3 migration path.
2. **6 external consumers** audit-listed; 4 require NO change (sibling
   implementations / channel-name strings only); 2 staged for review (anima
   `.roadmap.qrng` additive field + `nexus/cli/qrng.hexa` shellout refactor).
3. **Tests scaffolded fresh** — modularity 2→1 demotion remediated with
   7 smoke tests at extraction time; coverage tier 1.
4. **ANU rate-limit + ToS evolution risk** — 1 req/min T1.a legacy; mock LCG
   fallback always available with `QRNG_MOCK=1`.
5. **License audit deferred** — qrng core Apache-2.0 (clean); per-vendor
   data-rights for byte redistribution NOT formally audited (this package
   returns bytes to caller, does not redistribute).

## Consumer refactor (6 audited)

| ID | Consumer | Direct Import? | Action |
|----|----------|---------------:|--------|
| c1 | anima/.roadmap.qrng | no | STAGED — additive standalone_provider_2026_05_04 field |
| c2 | anima-physics/esp32/qrng_bridge.hexa | no | NO CHANGE — internal LCG sibling impl |
| c3 | anima-physics/verify_7cond_hw.hexa | no | NO CHANGE — local lcg_unit + qrng_bias_vec helper |
| c4 | anima-physics/hw_engine_bridge.hexa | no | NO CHANGE — channel-name "esp32_qrng" string only |
| c5 | anima-eeg | no | NO CHANGE — zero qrng matches in tree today |
| c6 | nexus/core/qrng provider stub + nexus/modules/qrng | YES | STAGED — qmirror v0.3.0 shellout pattern; delete origin after smoke |

Detail: `state/qrng_standalone_extraction_2026_05_04/refactor_log.jsonl`.

## nexus consumer refactor (qmirror v0.3.0 pattern, STAGED)

```
1. nexus/cli/qrng.hexa            — 4-tier shellout router (env > Mac > home > PATH)
2. nexus/engine/nexus_cli.hexa    — cmd_qrng dispatch addition
3. nexus/hexa.toml                — [dependencies] qrng = "^1.0.0"
4. nexus/install.hexa             — ensure_runtime_dep("qrng", "^1.0.0")
```

After smoke PASS: delete `nexus/modules/qrng/` + `nexus/core/qrng/` (1593 LoC).

## USER_ACTION

### P0 — HF mirror enable (BLOCKING for dual-mirror sync)

The stored HF token (`hf_LyKZ...`) is rejected by HF Hub API as 401
Unauthorized. To enable the auto-mirror workflow:

```bash
# 1. Re-issue write-scope token at https://huggingface.co/settings/tokens
# 2. Update local secret:
secret set huggingface.token <new_token>
# 3. Create HF model repo:
hf repos create dancinlab/qrng --type model --token "$(secret get huggingface.token)"
# 4. Set GitHub Actions secret:
#    https://github.com/dancinlab/qrng/settings/secrets/actions  →  HF_TOKEN
# 5. Trigger first mirror:
gh workflow run sync-to-hf.yml -R dancinlab/qrng
```

Until step 4 completes, the workflow runs but **fails loudly** (by design)
at "Verify HF_TOKEN secret is present".

### P1 — nexus consumer refactor (STAGED for user review)

Files NOT auto-committed (per repo policy):

- `nexus/cli/qrng.hexa` (NEW — qmirror v0.3.0 4-tier shellout pattern)
- `nexus/hexa.toml` (ADD: `qrng = "^1.0.0"` under `[dependencies]`)
- `nexus/install.hexa` (ADD: `ensure_runtime_dep("qrng", "^1.0.0")`)
- `nexus/engine/nexus_cli.hexa` (ADD: `cmd_qrng` dispatch case)
- After smoke PASS: `rm -rf nexus/modules/qrng/ nexus/core/qrng/` (1593 LoC)

### P1 — anima/.roadmap.qrng additive (STAGED)

Add field `standalone_provider_2026_05_04` to header object pointing at the
new repo (mutation_type: additive_field_only; semantics_preserved: true).

## Marker

`anima/state/markers/qrng_standalone_extraction_landed.marker`

## State artifacts

- `anima/state/qrng_standalone_extraction_2026_05_04/audit.json`
- `anima/state/qrng_standalone_extraction_2026_05_04/push_log.json`
- `anima/state/qrng_standalone_extraction_2026_05_04/refactor_log.jsonl`
- `anima/state/qrng_standalone_extraction_2026_05_04/dual_home_boundary_doc.md`
