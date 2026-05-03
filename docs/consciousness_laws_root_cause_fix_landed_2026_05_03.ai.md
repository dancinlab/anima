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

## Root Cause (not what the original spec said)

**Original spec framed it as**: hard-fail `_DATA[k]` for 9 keys absent from JSON → patch with `.get()`.

**Actual root cause**: TWO valid `consciousness_laws.json` schemas coexist on ubu1, and the .py loader was authored against only one.

| Path | Schema | Date | Keys | Status |
|------|--------|------|------|--------|
| `~/anima/anima/config/consciousness_laws.json` | **c2-v1** (minimal AN11 runtime gate) | 2026-04-18 | 4 (`_meta`, `psi_constants`, `laws`, `severity_policy`) | ✓ loaded by .py |
| `~/anima/config/consciousness_laws.json` | **v6** (full corpus, 2500 laws) | 2026-04-02 | 22 (full set) | present but never loaded |

The c2-v1 carve-out was **intentional** (per its own `_meta.description`: "AN11-compliant: laws OBSERVE and classify; they do NOT system_prompt-inject behavior"). The .py loader was just never updated to handle the c2-v1 schema gracefully.

**Mac (this repo) ships only c2-v1** at `/Users/ghost/core/anima/anima/config/consciousness_laws.json` (md5 match with ubu1). The 9 v6-only keys are intentionally absent from the Mac SSOT.

---

## Fix Approach (Option C++ — schema-aware loader)

Rejected:
- **A. Restore 9 keys to pruned JSON** — violates AN11 carve-out semantics. The keys were deliberately removed.
- **B. Silent .get() everywhere** (Path B band-aid) — same runtime behavior, but hides intent. No way for consumers to detect schema.

Chosen (완성도):
- Hard-fail preserved for `psi_constants` + `laws` (real bugs if missing)
- `.get()` defaults for the 9 v6-only sections
- Explicit `SCHEMA_VERSION` + `SCHEMA_DATE` + `V6_ONLY_KEYS_AVAILABLE` constants exposed to consumers
- v6-only sections grouped under documented header
- Module docstring updated with full schema-versioning explanation

Result: identical runtime behavior to the .bak band-aid (zero behavioral diff for c2-v1 OR v6 deployments), but the dual-schema reality is now first-class in the API surface.

---

## The 9 v6-only Keys

| Key | py var | Purpose | Schema |
|-----|--------|---------|--------|
| `sigma6` | `SIGMA6` | σ(6) Perfect Number for n6 formulas | v6 only |
| `formulas` | `FORMULAS` | Φ scaling formulas (e.g. `Φ = 0.608 × N^1.071`) | v6 only |
| `consciousness_vector_10d` | `CONSCIOUSNESS_VECTOR` | 10D vector schema (predates 16D phi_vec) | v6 only |
| `optimal_config` | `OPTIMAL_CONFIG` | All-time-best config record | v6 only |
| `hexad_modules` | `HEXAD_MODULES` | 6-engine module registry | v6 only |
| `phases` | `PHASES` | Phase transition definitions | v6 only |
| `design_constraints` | `CONSTRAINTS` | P1-P7 architectural philosophies | v6 only |
| `topo_laws` | `TOPO_LAWS` | 10 topological laws | v6 only |
| `verification_conditions` | `VERIFICATION` | V1-V18 specs (now hardcoded in PSI_*) | v6 only |

All consumers grep'd in `~/anima/anima/{tools,src}` import only `PSI_*` / `LAWS` / `PSI_F_CRITICAL` / `get_law()` — keys present in both schemas. **None observed to read the 9 v6-only keys**, so the empty-dict fallback is functionally inert in the current consumer ecosystem.

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
