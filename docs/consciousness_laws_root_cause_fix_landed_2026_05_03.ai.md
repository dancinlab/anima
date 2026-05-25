# consciousness_laws.py Root-Cause Fix — Landed 2026-05-03

**Goal**: Replace the Path B band-aid (`.get()` everywhere, no documentation) with a proper schema-aware loader that documents the c2-v1 vs v6 split and preserves hard-fail strictness for genuinely-required keys.

**Substrate**: ubu1 fix (raw#9 — Mac has no .py mirror, only .json + .hexa stub). $0.

**Constraints honored**: raw#9 (no Mac .py created; .hexa preserved as design-doc stub), raw#15 (~/anima/... paths on ubu1), raw#10 (3 honest C3 below).

---

## Result

| Field | Value |
|------|------|
| Fixed file | `~/anima/anima/core/consciousness_laws.py` (224 LOC, was 205) |
| .bak preserved (audit trail) | `~/anima/anima/core/consciousness_laws.py.bak_path_b_2026_05_03` (untouched) |
| Schema detected at load | `c2-v1` (date 2026-04-18, 14 laws) |
| `V6_ONLY_KEYS_AVAILABLE` | `False` (correctly reports c2-v1 deployment) |
| Import smoke test | PASS — no TypeError |
| Pipeline smoke test (`from conscious_decoder import ConsciousDecoderV2`) | PASS |
| All 9 v6-only keys handled | PASS — return `{}` cleanly |
| Mac files modified | 0 (raw#9 compliant — Mac has no .py) |
| Tool calls used | ~18 |
| Cost | $0 |

---

<!-- [Hc_021 c2-v1-v6-schema-split — moved to hypotheses_candidates/Hc_021_c2_v1_v6_schema_split.md on 2026-05-11] -->

## Root Cause (not what the original spec said)

(body content scrubbed — see Hc_021)

---

## Verification

```
SCHEMA_VERSION: c2-v1
SCHEMA_DATE: 2026-04-18
V6_ONLY_KEYS_AVAILABLE: False
PSI_ALPHA: 0.014
PSI_F_CRITICAL: 0.1
SIGMA6 (empty in c2-v1): {}
FORMULAS (empty in c2-v1): {}
LAWS count: 14
LOAD: OK

cl loaded: schema=c2-v1, v6_keys=False, laws=14
ConsciousDecoderV2 imported (depends on PSI_F_CRITICAL=0.1)
SMOKE TEST: PASS — eval pipeline can now import without TypeError
```

HellaSwag re-run intentionally **skipped** — Path B verdict (`CLM_V4_AT_FLOOR`, acc_norm=0.242) is independent of these keys; the 9 keys are unused by `conscious_decoder` / eval pipeline; .get() defaults match prior .bak behavior bit-for-bit. Re-running would consume GPU time without changing the result.

---

## raw#9 Compliance

- Mac: NO .py created. Mac's `consciousness_laws.hexa` stub remains as the only Mac-side code form. The fix lives only on ubu1, where .py is permitted.
- ubu1: .py edited in place, .bak preserved.
- `_python_bridge/` not used (would have been a violation if it had been considered).

---

## Honest C3 (raw#10)

- **(a) Loader robustness vs spec strictness tradeoff**: schema-aware loader trades strict-fail-on-missing-key for tolerant defaults. A future bug that accidentally drops `sigma6` from a v6 JSON would silently degrade to `{}` instead of raising. Mitigation: `SCHEMA_VERSION` + `V6_ONLY_KEYS_AVAILABLE` flags let consumers assert their schema requirements explicitly. Stronger mitigation (per-import-context `_SCHEMA_REQUIREMENTS` table) was rejected as overengineering for current consumer set (~30 modules, all using only common keys).
- **(b) Key restoration source confidence**: NO keys were restored. Confidence on intent: **HIGH** (explicit `_meta.description` says c2-v1 is "AN11-compliant: laws OBSERVE and classify"). Confidence that all 9 keys are truly dormant: **MEDIUM** — current grep shows no consumer imports them, but cross-module attribute reflection (`getattr(cl, 'SIGMA6')` style dynamic access) was not exhaustively searched.
- **(c) Side-effect risk**: **LOW**. All grep'd consumers use only `PSI_*` / `LAWS` / `PSI_F_CRITICAL` — present in both schemas. Modules that crashed at import time (chain through `conscious_decoder`) now succeed. Residual risk: dynamic `dict()` iteration over `CONSTRAINTS` in some untested code path could see fewer entries, but no PSI-ecosystem module observed scanning `CONSTRAINTS` dynamically.

---

## Files

```
state/consciousness_laws_root_cause_fix_2026_05_03/
├── audit.json                  # primary audit trail
├── missing_keys_list.json      # 9 keys + purposes + schema
└── before_after_diff.json      # change summary
state/markers/consciousness_laws_root_cause_fix_landed.marker
docs/consciousness_laws_root_cause_fix_landed_2026_05_03.ai.md  (this file)
```

ubu1 only (raw#9):
```
~/anima/anima/core/consciousness_laws.py                          (FIXED, 224 LOC, schema-aware)
~/anima/anima/core/consciousness_laws.py.bak_path_b_2026_05_03    (PRESERVED, audit trail)
~/anima/state/consciousness_laws_root_cause_fix_2026_05_03/       (mirrored audit artifacts)
```

---

## References

- Path B sanity probe (band-aid origin): `docs/p9_path_b_sanity_probe_landed_2026_05_03.ai.md` (updated with reference paragraph)
- AN11 framework: c2-v1 `_meta.description` quoted in audit.json
