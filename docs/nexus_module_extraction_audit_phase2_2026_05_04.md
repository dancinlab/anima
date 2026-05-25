# nexus module extraction audit — phase 2 (rank 4-6)

**date**: 2026-05-04
**phase**: 2 (re-audit of phase1 ranked rank 4-6 candidates, post batch-1 extraction)
**auditor**: subagent (anima cycle)
**scope**: fusion_ledger + tabletop_blackhole + chip_rtl_gen + qrng + mc_integrate
**constraint**: READ-ONLY on nexus, anima, hive, CANON, qmirror, sim-universe, honesty-monitor

## phase1 status snapshot

| rank | module | status | marker |
|------|--------|--------|--------|
| 1 | crystallography_n6 | EXTRACTED | crystallography_n6_extraction_landed.marker |
| 2 | honesty_monitor | EXTRACTED (standalone repo) | honesty_monitor_extraction_landed.marker |
| 3 | chip_isa_n6 | EXTRACTED | chip_isa_n6_extraction_landed.marker |
| 4-8 | fusion_ledger / tabletop_blackhole / chip_rtl_gen / qrng / mc_integrate | PENDING (this audit) | (none yet) |

## phase2 module table

| module | LoC drift | score Φ1→Φ2 | destination | readiness | effort hr |
|--------|-----------|-------------|-------------|-----------|-----------|
| fusion_ledger | 314 → 314 (0) | 8 → 8 | n6-arch/domains/energy/fusion/ | ZERO_COLLISION | 6 |
| tabletop_blackhole | 307 → 307 (0) | 8 → 8 | n6-arch/experiments/tabletop-blackhole/ | ZERO_COLLISION | 4 |
| chip_rtl_gen | 410 → 410 (0) | 8 → 8 | n6-arch/domains/compute/chip-rtl-gen/ | MERGE_REQUIRED | 10 |
| qrng | 1047 → 1047 (0) | 8 → 7 | NEW /Users/ghost/core/qrng/ | SCAFFOLD_FIRST | 16 |
| mc_integrate | 1425 → 1425 (0) | 8 → 8 | NEW /Users/ghost/core/mc-integrate/ | DECOUPLE_FIRST | 14 |

**LoC subtotal to extract**: 3,503 LoC (excludes templates + data assets + tests)

## per-module destination assessment

### rank 1 (phase2): fusion_ledger → n6-arch/domains/energy/fusion/

- **viability**: CLEAN_MERGE
- **predecessor**: `fusion.md` descriptor + `verify_fusion.hexa` 68-LoC stub at peer level — co-exists with fusion_ledger.hexa (could optionally fold the stub later)
- **alt**: `domains/energy/fusion-powerplant/` (also clean, 1 .md only). Preferred: `fusion/` (matches @tool slug + ITER constants are reactor-design canon, not powerplant-specific)
- **assets**: `data/iter_constants.json` must move with code

### rank 2 (phase2): tabletop_blackhole → n6-arch/experiments/tabletop-blackhole/

- **viability**: CLEAN_NEW_DIR
- **predecessor**: none (no hawking/blackhole/tabletop subdirs found in experiments/)
- **alt**: `domains/physics/` (no current sub for analog gravity, would need new dir). Preferred: `experiments/` (Steinhauer 2014 BEC analog Hawking is experimental in nature, fits the existing axis)
- **assets**: none — single .hexa + README + tests

### rank 3 (phase2): chip_rtl_gen → n6-arch/domains/compute/chip-rtl-gen/ (MERGE not REPLACE)

- **viability**: MERGE_REQUIRED — predecessor is ACTIVE (not a stub)
- **predecessor**: `rtl_generator.hexa` 472-LoC R25 legacy frozen (per @origin: `nexus/origins/hexa-rtl/rtl/*.hexa 미수정`)
  - **predecessor LARGER than nexus version (472 vs 410)** — divergence direction unclear
  - templates/ at predecessor are byte-identical to nexus templates (`diff -q` empty)
- **strategy**: install nexus 410-LoC as `chip_rtl_gen.hexa` ALONGSIDE preserved `rtl_generator.hexa` (parallel, NOT overwrite); README disambiguates
- **raw#15 issue**: `_core_root()` has hardcoded fallback `nexus/modules/chip_rtl_gen` — must be made root-agnostic before extraction

### rank 4 (phase2): mc_integrate → NEW /Users/ghost/core/mc-integrate/ (after DECOUPLE)

- **viability**: VIABLE_AFTER_ANU_DECOUPLING
- **stale coupling confirmed**: `mc_integrate.hexa` line: `let anu_src = home + "/core/nexus/sim_bridge/godel_q/anu_source.hexa"`
- **dual-home of anu_source.hexa**: lives at BOTH `nexus/sim_bridge/godel_q/` AND `sim-universe/modules/godel_q/`
- **same coupling in multiverse_nav (rank 9)** — coordinated decouple cycle warranted
- **decouple options**:
  - (A) swap to qmirror cli (qmirror.qrng path; already standalone, Apache-2.0) — **PREFERRED**
  - (B) swap to qrng cli (after qrng repo extracted) — creates rank-7-blocks-rank-8 dependency
  - (C) inline minimal anu_source bootstrap (smallest blast radius, breaks the cross-tree path before extraction)
- **@origin progenitor**: `CANON/experiments/anu_mc_verification/anu_mc_verify.hexa` — add deprecation note pointing to standalone after extraction

### rank 5 (phase2): qrng → NEW /Users/ghost/core/qrng/ (after SCAFFOLD)

- **viability**: VIABLE_BUT_HIGH_EFFORT
- **score downgrade 8→7**: modularity 2→1 (no module-level README + no `tests/` subdir)
- **dual-home risk**: `qmirror/modules/qrng.hexa` (193 LoC drop-in API copy with `@resolver-bypass`) — naming collision but DIFFERENT scope
  - qmirror.qrng = consumer-facing API drop-in (`qrng_bits / qrng_uint64 / qrng_choice`)
  - nexus/modules/qrng = 5-source provider registry (curby, anu, nist_beacon, hardware, mock)
  - **NO CODE OVERLAP CONFIRMED** — qmirror inlines minimal LCG fixture only
- **active consumers** (require migration plan):
  - `anima/.roadmap.qrng`
  - `anima/anima-physics/esp32/QRNG_SPEC.md`
  - `anima/anima-physics/esp32/qrng_bridge.hexa` (referenced)
  - `anima/anima-physics/verify_7cond_hw.hexa`
  - `anima/anima-physics/hw_engine_bridge.hexa` (esp32_qrng channel)
  - `anima-eeg` (per .roadmap.qrng consumers list)
- **paired with provider stub**: `nexus/core/qrng/` (Option D consumer/provider split — extraction must preserve via thin proxy or migration)
- **raw#15 issues**: `/tmp/nexus_qrng_*.bin` paths in curby/anu/nist_beacon; `NEXUS_QRNG_*` env vars must alias to `QRNG_*` in standalone
- **active week** (last touch 2026-05-03 per CURBy + NIST Beacon parser landings) — extraction window must coordinate with anima.qrng cycle

## coupling count summary (grep coverage)

| module | external consumers found | nexus-internal coupling |
|--------|--------------------------|------------------------|
| fusion_ledger | 0 (audit refs only) | 0 |
| tabletop_blackhole | 0 (audit refs only) | 0 |
| chip_rtl_gen | 0 (audit refs only) | 1 (`_core_root()` fallback path) |
| qrng | 6 (anima roadmap + anima-physics 3 files + anima-eeg + nexus/core/qrng provider stub) | 2 (`/tmp/nexus_qrng_*` paths + `NEXUS_QRNG_*` env) |
| mc_integrate | 0 external; same coupling pattern in `multiverse_nav` (rank 9) | 1 (hardcoded `nexus/sim_bridge/godel_q/anu_source.hexa`) |

## anti-pattern flags (new vs phase1)

- **NEW (chip_rtl_gen)**: predecessor in destination is ACTIVE 472-LoC R25 legacy (NOT older 305-LoC stub assumed in phase1) — merge strategy required, no blind overwrite
- **NEW (qrng)**: missing module README + missing tests/ subdir — modularity downgrade 2→1
- **NEW (mc_integrate)**: dual-home of `anu_source.hexa` between nexus/sim_bridge AND sim-universe/modules/godel_q — decouple to qmirror cli avoids picking either
- **CONFIRMED (qrng)**: dual-home with qmirror.qrng is API-surface-only (no code collision) — risk = future ambiguity
- **CONFIRMED (mc_integrate, multiverse_nav)**: shared ANU path coupling — single decouple cycle (~2hr) unblocks both

## ranked next-3 extraction batch (BG launch order)

**by completion-readiness lens** (lowest risk first):

1. **tabletop_blackhole** (4hr, ZERO_COLLISION, easiest in batch)
2. **fusion_ledger** (6hr, ZERO_COLLISION, 1 data asset to move)
3. **chip_rtl_gen** (10hr, MERGE_REQUIRED with known landmine: predecessor R25 472-LoC, raw#15 fix needed)

All three target CANON (existing standalone) — zero new repo overhead, zero env-var aliasing, zero consumer migration. Combined effort ~20hr; parallelizable as 3 BG subagents.

**deferred next cycle (batch 3)**: mc_integrate decouple cycle (2hr blast-radius-1, also unlocks multiverse_nav rank 9)
**deferred batch 4**: qrng scaffold cycle (4hr, README + tests/ + env alias plan)
**deferred batch 5**: qrng + mc_integrate standalone repo creation (14+16=30hr combined, after batches 3+4 land)

## 4 honest C3 caveats (raw#10)

1. **scoring re-evaluation may diverge from phase1**: only qrng dropped (8→7) due to missing README + tests/ subdir. Other 4 unchanged. Subjective: alternate weighting (e.g. activity 2x for qrng given last-touched 1d) would put qrng back at 8. Phase2 prefers conservatism (modularity gates promotion).

2. **destination decisions need validation by human**:
   - (a) `fusion/` vs `fusion-powerplant/` for fusion_ledger — chose `fusion/` (slug match + reactor-canon)
   - (b) `experiments/` vs `domains/physics/` for tabletop_blackhole — chose `experiments/` (Steinhauer-style is experimental)
   - (c) merge-not-replace strategy for chip_rtl_gen rtl_generator R25 legacy — chose preserve+parallel install (preserves R25 frozen contract)
   All three reversible.

3. **qrng dual-home risk** with qmirror/modules/qrng.hexa (193 LoC): API-surface-only collision (different scope: qmirror=consumer drop-in, nexus=provider registry). Risk = future ambiguity about which is canonical for new consumers. Mitigation: standalone qrng repo declares itself provider authority + qmirror.qrng adds `depends-on=qrng` note in v3.0.

4. **mc_integrate sim-universe coupling** via `anu_source.hexa` is dual-homed (lives in BOTH `nexus/sim_bridge/godel_q/` AND `sim-universe/modules/godel_q/`) — not a unique sim-universe issue but a stale-nexus-tree issue. Decouple to qmirror cli avoids picking either. Same coupling in multiverse_nav (rank 9, deferred). Honest: sim-universe is just-published and may not have stable cli surface yet — qmirror is more battle-tested.

## artifacts

- `/Users/ghost/core/anima/state/nexus_module_extraction_audit_phase2_2026_05_04/audit.json`
- `/Users/ghost/core/anima/state/nexus_module_extraction_audit_phase2_2026_05_04/ranked_candidates_phase2.json`
- `/Users/ghost/core/anima/state/nexus_module_extraction_audit_phase2_2026_05_04/launch_recipes_phase2.jsonl`
- `/Users/ghost/core/anima/state/markers/nexus_module_extraction_audit_phase2_2026_05_04.marker`

## handoff (next cycle)

**recommended primary action**: launch 3 parallel BG subagents using `launch_recipes_phase2.jsonl` rank 1+2+3 (tabletop_blackhole + fusion_ledger + chip_rtl_gen, ~20hr combined). All three target CANON (existing standalone).

**recommended secondary action** (post batch-2 land): launch 1 BG decouple cycle (mc_integrate + multiverse_nav anu_source path → qmirror cli, ~2hr).

**recommended tertiary action** (post decouple): launch 1 BG scaffold cycle (qrng module README + tests/, ~4hr).

**NOT recommended this cycle**: standalone repo creation for qrng + mc_integrate (30hr combined; depends on decouple + scaffold landing first).

cost: $0 (pure audit + planning, READ-ONLY).
