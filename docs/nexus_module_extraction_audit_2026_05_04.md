# Nexus Module Extraction Audit — 2026-05-04

**Scope**: comprehensive READ-ONLY audit of `/Users/ghost/core/nexus/modules/` to identify next-wave standalone-extraction candidates after qmirror v2.0 (closure 13/13, GitHub PUBLIC) and sim-universe v1.0 (just published, finish in flight).

**Cost**: $0. Pure planning + ranking. No extraction performed.

---

## §1. Module inventory (15 directories, 12 non-empty)

| # | Module | LoC | files | README | tests | Last commit | Notes |
|---|--------|-----|-------|--------|-------|-------------|-------|
| 1 | atlas_n6 | 0 | 0 | N | N | 2026-05-03 | EMPTY placeholder; provider in `nexus/core/atlas_n6/` |
| 2 | bind | 210 | 1 | Y | N | 2026-05-02 | axis subscriber wrapper |
| 3 | chip_isa_n6 | 445 | 1 | Y | N | 2026-04-27 | 24-bit Xn6 ISA |
| 4 | chip_rtl_gen | 410 | 1 | Y | N | 2026-04-27 | 6-prim Verilog gen + templates |
| 5 | crystallography_n6 | 402 | 1 | Y | N | 2026-04-27 | Fedorov 230 / Bravais 14 enum |
| 6 | fusion_ledger | 314 | 1 | Y | N | 2026-04-27 | ITER + n=6 27 constants |
| 7 | honesty_monitor | 240 | 1 | Y | N | 2026-04-27 | BT-AI2 falsifier API |
| 8 | kick | 393 | 3 | N | N | 2026-05-02 | ω-cycle dispatch (router/mac/claude) |
| 9 | mc_integrate | 1425 | 2 | Y | N | 2026-04-27 | ANU MC integrator (largest) |
| 10 | multiverse_nav | 413 | 1 | Y | N | 2026-04-27 | Bostrom 144-branch trilemma |
| 11 | qrng | 1047 | 5 | N | N | 2026-05-03 | 5-source registry (most active) |
| 12 | sim | 0 | 0 | N | N | 2026-05-03 | EMPTY (post sim-universe extraction) |
| 13 | tabletop_blackhole | 307 | 1 | Y | N | 2026-04-27 | BEC Hawking T simulator |
| 14 | verify_batch | 402 | 1 | Y | N | 2026-04-27 | discover/run verify_*.hexa |

**Totals**: 6,008 hexa LoC across 19 .hexa files in 12 non-empty modules.

---

## §2. 5-axis scoring (max 10)

Axes: **coupling** (low coupling = high) | **reusability** (generic external value) | **maturity** (closure cond + falsifiers + docs) | **activity** (recent commits) | **modularity** (clean CLI + lib + sentinel).

| Module | Coup | Reuse | Mat | Act | Mod | **Total** | Tier |
|--------|-----:|------:|----:|----:|----:|----------:|------|
| **crystallography_n6** | 2 | 2 | 2 | 1 | 2 | **9** | extract_immediately |
| **honesty_monitor** | 2 | 2 | 2 | 1 | 2 | **9** | extract_immediately |
| **chip_isa_n6** | 2 | 2 | 2 | 1 | 2 | **9** | extract_immediately |
| fusion_ledger | 2 | 1 | 2 | 1 | 2 | 8 | extract_immediately |
| tabletop_blackhole | 2 | 1 | 2 | 1 | 2 | 8 | extract_immediately |
| chip_rtl_gen | 1 | 2 | 2 | 1 | 2 | 8 | extract_immediately |
| qrng | 1 | 2 | 1 | 2 | 2 | 8 | extract_immediately |
| mc_integrate | 1 | 2 | 2 | 1 | 2 | 8 | extract_immediately |
| multiverse_nav | 1 | 1 | 2 | 1 | 2 | 7 | extract_next_quarter (merge → sim-universe) |
| verify_batch | 1 | 1 | 2 | 1 | 2 | 7 | extract_next_quarter |
| bind | 0 | 0 | 1 | 2 | 1 | 4 | keep_in_nexus |
| kick | 0 | 0 | 1 | 2 | 1 | 4 | keep_in_nexus |
| atlas_n6 | 0 | 0 | 0 | 1 | 0 | 1 | keep (placeholder) |
| sim | 0 | 0 | 0 | 1 | 0 | 1 | DELETE (post sim-universe) |

**Tier counts**: 8 immediate (8-10), 2 next-quarter (6-7), 0 eventual (4-5), 4 keep-in-nexus (<4).

---

## §3. Top 5 ranked candidates

### Rank 1 — `crystallography_n6` (score 9)

- **Why**: pure n=6 closed-form Fedorov-230 / Bravais-14 / 7-systems / 32-pt-groups enumerator. Zero external deps. IUCr-canonical reference. Sentinel `__CRYSTALLOGRAPHY_N6__ PASS|FAIL`.
- **Destination**: `/Users/ghost/core/n6-architecture/domains/structure/crystallography/` (existing standalone repo).
- **Effort**: ~4hr (file move + INDEX update + test author + nexus rm).
- **Risk**: minimal — no consumers in nexus today.

### Rank 2 — `honesty_monitor` (score 9)

- **Why**: BT-AI2 honesty-bit falsifier (claimed-vs-actual ML loss audit). F-AI2-A (claimed PASS but >5% divergence) + F-AI2-B (claimed FAIL but <1% divergence). Generic ML-safety value beyond n6/anima ecosystem.
- **Destination**: NEW standalone repo `/Users/ghost/core/honesty-monitor/` (mirror qmirror layout: cli/ modules/ tests/ docs/ + hexa.toml + install.hexa).
- **Effort**: ~8hr (new repo bootstrap + GitHub create + hx install hook + README).
- **Risk**: low — single-process state caveat preserved in README; threshold sensitivity disclosed.

### Rank 3 — `chip_isa_n6` (score 9)

- **Why**: 24-bit Xn6 ISA encoder/decoder (24 mnemonics × 4 variants). Lossless roundtrip falsifier. Master identity σ·φ = n·τ = J₂ = 24.
- **Destination**: `/Users/ghost/core/n6-architecture/domains/compute/chip-isa-n6/` (predecessor 305-LOC stub already there per @origin tag — REPLACE with productized 445-LOC).
- **Effort**: ~6hr (replace + sha-mismatch reconciliation + test author).
- **Risk**: low-medium — destination predecessor may have divergent edits requiring merge audit.

### Rank 4 — `fusion_ledger` (score 8)

- **Why**: ITER + n=6 fusion-design constants verifier. 27 measured constants vs closed-form (σ, τ, φ, sopfr, J₂). **Honesty preserved**: 26/27 PASS, lawson_triple falsified by 1 decade — explicitly NOT inflated.
- **Destination**: `/Users/ghost/core/n6-architecture/domains/energy/fusion/`.
- **Effort**: ~6hr (move + data/iter_constants.json migration + INDEX).
- **Risk**: low — niche audience (fusion + n6 enthusiasts).

### Rank 5 — `tabletop_blackhole` (score 8)

- **Why**: BEC analog Hawking-temperature simulator (Steinhauer 2014). n=6 anchors: T_H = σ/(τ·n) = 0.5 nK; B_trap = σ·τ = 48 T. Zero external deps.
- **Destination**: `/Users/ghost/core/n6-architecture/experiments/`.
- **Effort**: ~4hr (move + experiment registration).
- **Risk**: low.

---

## §4. Anti-pattern flags found

1. **`_python_bridge` heavy dep**: NONE in modules/ (only qmirror standalone has _python_bridge subdir per raw#9 concession). Modules are hexa-pure.
2. **No clear API (research-stage code)**: `atlas_n6` (empty), `sim` (empty), `kick/mac_kick.hexa` (WRAPPED stub T2, not IMPLEMENTED).
3. **Already migrated elsewhere**:
   - `sim` → fully absorbed by `/Users/ghost/core/sim-universe/` (recommend `rm -rf modules/sim/`).
   - `chip_isa_n6` + `chip_rtl_gen` + `crystallography_n6` + `fusion_ledger` + `tabletop_blackhole` → all have @origin tags pointing to `~/core/n6-architecture/` predecessors. n6-architecture standalone EXISTS with rich domain layout (`domains/compute/`, `domains/energy/`, `domains/structure/`, `experiments/`, `papers/`, `lean4-n6/`).
4. **Cross-tree path coupling (broken post-extraction)**:
   - `mc_integrate.hexa` references `nexus/sim_bridge/godel_q/anu_source.hexa` — but sim_bridge contents extracted to sim-universe (path now broken / will break when sim_bridge is rm'd from nexus).
   - `multiverse_nav.hexa` same coupling to `nexus/sim_bridge/godel_q/anu_source.hexa`.
   - **Action item**: before extracting mc_integrate / multiverse_nav, swap ANU source dep to `qmirror cli` or `qrng cli` invocation.
5. **Empty test directories**: every module has `tests/__pycache__/` only — no actual hexa tests landed. Test authoring is part of every extraction recipe.

---

## §5. Recommended next-cycle action

**Batch 1 (parallel BG extraction, ~18hr total)**: launch 3 BG subagents in parallel for the 3 score-9 modules:

1. BG-A: extract `crystallography_n6` → n6-architecture
2. BG-B: extract `honesty_monitor` → NEW standalone repo `/Users/ghost/core/honesty-monitor/`
3. BG-C: extract `chip_isa_n6` → n6-architecture (with predecessor sha audit)

**Batch 2 (next cycle)**: `chip_rtl_gen` + `fusion_ledger` + `tabletop_blackhole` (all → n6-architecture; can be batched with shared test scaffold).

**Batch 3 (deferred)**:
- `qrng` (14hr — needs anima-eeg consumer migration plan first; high-priority due to most-active status)
- `mc_integrate` (12hr — decouple ANU dep first via qrng-cli swap)
- `multiverse_nav` (5hr — merge into sim-universe AFTER finish-in-flight settles)
- `verify_batch` (6hr — make root-agnostic by removing `nexus/state/` cache default)

**Skip / keep**:
- `bind`, `kick`: tightly coupled to nexus framework — keep.
- `atlas_n6`: placeholder — keep as marker.
- `sim`: empty post sim-universe — `rm -rf` recommended.

---

## §6. Honest C3 caveats (raw#10)

1. **Scoring is subjective**: 5-axis equal-weight sum may not match real extraction value; alternate weighting (e.g. activity 2x for production-critical modules) would re-rank. `qrng` would jump to top under activity-weighted scoring.
2. **Ranking depends on nexus future direction**: if nexus shifts toward monolith-first integration, all extraction candidates downgrade to "keep_in_nexus". If nexus shifts toward thin orchestrator, all 8 immediate candidates accelerate.
3. **Extraction adds dual-mirror burden**: each new repo = GitHub + HuggingFace mirror + per-repo CHANGELOG + release notes + CI maintenance + version-skew risk. qmirror v2.0 has `CHANGELOG_v2_entry.md.draft` + `RELEASE_NOTES_v2.0.0.md.draft` + `registry_v2_entry.tsv.draft` overhead unaccounted for in ranking.
4. **Audit may miss inter-module hidden coupling**: only @origin tags + nexus-path string-match + sim_bridge cross-ref were checked. Hidden coupling channels NOT enumerated: shared sentinel-token namespaces, env-var convention sharing (`NEXUS_QRNG_*`), atlas-absorb downstream consumer chains, hexa-resolver bypass markers, host-pin marker file dependencies. A pre-extraction sweep with `grep -r <module_name>` across nexus + anima + hive + n6-architecture is REQUIRED before each batch.

---

## §7. Artifacts

- `/Users/ghost/core/anima/state/nexus_module_extraction_audit_2026_05_04/audit.json` — full per-module audit data (5-axis scores + anti-patterns + verdict + rationale)
- `/Users/ghost/core/anima/state/nexus_module_extraction_audit_2026_05_04/ranked_candidates.json` — ranked list with effort estimates + destination breakdown
- `/Users/ghost/core/anima/state/nexus_module_extraction_audit_2026_05_04/launch_recipes.jsonl` — BG prompt templates for top 3 candidates
- `/Users/ghost/core/anima/state/markers/nexus_module_extraction_audit_2026_05_04.marker` — completion marker

---

## §8. Reference: standalone repo layout (qmirror / sim-universe)

Both extracted repos use this canonical layout (mirror this for new extractions):

```
<repo>/
├── cli/<repo>.hexa           # thin CLI dispatcher
├── modules/                   # hexa source files (+ optional _python_bridge/ for raw#9 concession)
├── docs/                      # closure docs + handoffs
├── examples/                  # usage examples
├── state/                     # per-extraction state (markers, etc.)
├── tests/                     # hexa selftest files
├── tool/                      # utility scripts
├── hexa.toml                  # package manifest (name, version, license, repo, mirror_url, [lib], [[bin]], [test])
├── install.hexa               # hx install hook (pre/post; checks deps, runs --selftest)
├── README.md                  # user-facing docs
└── LICENSE                    # Apache-2.0
```

Key fields in `hexa.toml`:
- `[package].name`, `version` (semver), `entry` = `cli/<repo>.hexa`
- `repository` = `https://github.com/need-singularity/<repo>`
- `mirror_url` = `https://huggingface.co/need-singularity/<repo>`
- `[lib].entry` = importable hexa module (often `modules/<main>.hexa` or `modules/selftest.hexa`)
- `[[bin]]` = CLI binary name + path
- `[test].runner` = `hexa`, `[test].files` = explicit list of selftest files
