# Dirty Siblings Audit — 2026-05-04

**Cycle:** `own_mk1_cleanup_followup_2026_05_04`
**Scope:** Read-only audit of dirty git state in non-owned sister repos
**Authority:** raw#10 (no auto-clean); user-explicit decisions required for in-flight work

---

## Repo 1: `/Users/ghost/core/nexus` (branch=`main`)

**Total dirty:** 107 entries (1 modified, 106 untracked)

### Modified (tracked)

| File | Diff stat | Content type | Recommendation |
|------|-----------|--------------|----------------|
| `n6/atlas.n6` | +5 lines | ω-cycle absorption marker (ts=2026-05-04T08:49:49Z, shard=neuromorphic-substrate-independence-akida-physical-mathematical-limit-saturation, "0 facts auto-classified") | **commit** — auto-ingestion artifact, idempotent footer addition. Safe to commit as `chore(atlas): ω-cycle absorb 2026-05-04`. |

### Untracked (106 files/dirs)

#### Category A: `n6/atlas.append.*.n6` (43 files)

ω-cycle paradigm/atlas append shards. Examples:
- `atlas.append.akida-neuromorphic-x-nexus-sim-universe-paradigm-breakthrough.n6`
- `atlas.append.alien-grade-{5,v2,v3}.n6` (cycle18/19/21)
- `atlas.append.cycle{20..29}-*.n6` (cycle closures)
- `atlas.append.lean4-w{9..14}-*-cycle{18..20}.n6`
- `atlas.append.neuromorphic-substrate-independence-akida-*-paradigm-v{12..15}-axis-expansion.n6`
- `atlas.append.virocapsid-collision-audit-cycle21.n6`
- `atlas.append.json-ssot-enrichment-cycle19.n6`
- `atlas.append.stash-pop-loss-recovery-cycle17.n6`

**Recommendation:** **commit batch** — `chore(atlas): ω-cycle append shards cycle17-29 backlog`. These are auto-classified atlas shards consumed by the ω-cycle absorber (already ingested into `atlas.n6` per the modified marker above).

#### Category B: `state/kick/runs/*` (62 dirs)

Kick-infra run artifacts. Date range 2026-04-28 to 2026-05-02. Examples:
- `2026-04-28_void-sighup-resistant-tui/`
- `2026-04-29_kick-infra-roundtrip-smoke-2026-04-29/`
- `2026-04-30_r39-hive-direct-spawn/`, `r42`, `r43`, `r45-*` (multiple variants)
- `2026-05-01_block-{3,8,9,10,11,12,12c,X}-verify*/`
- `2026-05-02_noise-envelope-quantum-rng-universe-simulation-3-way-collab-rerun9/`

**Recommendation:** **defer to user triage** — many appear to be debug/verify runs (transient). Suggest:
1. Check `nexus/.gitignore` — may already cover `state/kick/runs/`. If so, `git status` mismatch is a config drift.
2. If runs contain reusable verdicts/artifacts → commit selectively.
3. If transient → add `state/kick/runs/` to `.gitignore`.

#### Category C: `scripts/safety/` (1 dir)

Untracked safety scripts directory. **Recommendation:** **user review** — content unknown without inspection (out of read-only audit scope). If it contains operational safeguards, commit; if scratch, discard or ignore.

---

## Repo 2: `/Users/ghost/core/orpheus` (branch=`main`)

**Total dirty:** 1 untracked dir (5 files inside)

| Path | Files | Content | Recommendation |
|------|-------|---------|----------------|
| `state/dormant_explorer/` | 5 | metrics jsonl (eval, metric), archive duckdb (dormant_atlas), queries jsonl (smoke fixture, q_2013_q1_high_balance) | **defer to user triage** — looks like in-flight dormant_explorer pipeline state from 2026-05-04 (today). Could be live data; auto-clean would destroy. |

**File-by-file:**

| File | Type | Likely status |
|------|------|---------------|
| `metrics/eval_20260504T084422.jsonl` | metric output | TODAY's eval |
| `metrics/metric_20260504T084040.jsonl` | metric output | TODAY's metric |
| `archive/dormant_atlas.duckdb` | database | Persistent state |
| `queries/_smoke_fixture.jsonl` | test fixture | Probably commit |
| `queries/q_2013_q1_high_balance_20260504T171938.jsonl` | query result | TODAY 17:19 |

**Recommendation:** Add `state/dormant_explorer/{metrics,queries,archive}/` to `.gitignore` if these are runtime artifacts. Commit the directory README (if any) + smoke fixture if reusable.

---

## hexa-lang notes (BG-Φ² overlap, NOT modified by this BG)

For completeness — the hexa-lang repo (BG-Φ² writes) also has dirty content:
- ` M tool/pkg/registry.tsv` (registry update; likely BG-Φ² in-flight)
- `?? stdlib/hf_hub.hexa` (BG-Φ² territory)
- `?? stdlib/ieee754.hexa`
- `?? stdlib/sentencepiece.hexa`
- `?? test/regression/{array_idx_assign,import_alias}_repro/state/`

**This BG did NOT touch any of these** per hard constraint. BG-Φ² owns the reconciliation.

---

## Top-level recommendations (priority order)

1. **nexus n6 ω-cycle batch commit** (1 modified + 43 atlas.append) — 완성도 high, low risk; clears 41% of dirty entries with one logical commit.
2. **nexus state/kick/runs gitignore** — likely the right answer (62 dirs); inspect a sample first.
3. **orpheus dormant_explorer gitignore** for runtime artifacts; commit fixtures separately.
4. **scripts/safety/ inspect** — unknown content blocks decision.
5. **hexa-lang push-as-branch** (`diag/orpheus-selftest-sigkill`) — see verdict.json `phase_2_hexa_lang_branch.recommended_push_cmd`.

---

**Audit completed read-only.** No mutations to nexus or orpheus. All recommendations require user authorization to act.
