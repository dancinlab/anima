# anima canonical_layout feature-grouped migration plan — Wave B prep (2026-05-07)

- **BG**: BG-LAYOUT-MIGRATION-WAVE-B-PREP (analysis + spec only — NO file moves in this BG)
- **Wave**: B (Wave A complete in hive; Wave B = anima)
- **Expected exec window**: ~2026-05-12 (BG-LAYOUT-MIGRATION-WAVE-B-EXEC)
- **Owner**: anima self-axis (no cross-repo blast radius)
- **Status**: planning_landed — exec deferred
- **raw invariants**: raw#9 hexa orchestration / raw#10 honest C3 ≥5 / raw#15 additive (no destructive ops) / raw#168 minimum-viable carve-out
- **Cross-link**: hive `spec/mk2_apex.spec.yaml § sections.canonical_layout` (2026-05-05 declaration) ; anima `docs/anima_mk2_compliance_audit_2026_05_07.md § 1.2 / § 4.2.3` ; anima `spec/anima_cli_mk2.spec.yaml § 15.cycle_amend_2026_05_07.hive_mk2_compliance_gaps.g12_canonical_layout_feature_grouped`

---

## 1. Current state survey (2026-05-07)

per `state/anima_canonical_layout_migration_wave_b_prep_2026_05_07/survey.json` (full data).

### 1.1 Top-level shape (anima/)

| bucket | path | entry count (approx) | canonical | carve-out per raw#168 |
|---|---|---|---|---|
| 19 anima-* feature dirs | `anima-core/`, `anima-engines/`, `anima-physics/`, `anima-voice/`, `anima-tools/`, `anima-measurement/`, `anima-hexad/`, `anima-body/`, `anima-os/`, `anima-serve/`, `anima-hci-research/`, `anima-cpgd-research/`, `anima-tribev2-pilot/`, `anima-agent-{channels,core,hire-sim,plugins,providers,skills}/` | varies (0-166) | NONE compliant | — |
| anima/anima/ pilot | `anima/anima/{core,module,modules,spec,config,state}/` | partial triplet on `rng` | PARTIAL (singular naming OK; doc/ + lint missing) | — |
| modules/ near-empty | `modules/` | 2 hexa files | N/A (likely re-home) | — |
| docs/ flat | `docs/` | 1129 top-level md (345 ai.md) + 15 subdirs | catch-all post-migration acceptable per spec | — |
| **carve-outs (root, NOT moved)** | `tool/` (582) `bin/` (21) `hypotheses/` (111) `state/` (~1828) `.roadmap.*` (~50) `.own` `.guide` `config/` (~87) `scripts/` `tests/` (~217) | — | — | YES |

### 1.2 Existing partial triplet (the pilot)

`anima/anima/` already uses **singular** naming (`core`, `module`, `spec`, `config`, `state`) — i.e. partial mk2 conformance. The `rng` feature is split:

- `anima/anima/core/rng/`: 5 source files (registry, router, source, rng_main, dual_stream_seedanchor)
- `anima/anima/modules/rng/`: 9 implementation hexas (anu, curby, drand, esp32, ibm_q, idq_quantis, kaist_optical, nist_beacon, urandom) + fixtures/ + README.ai.md
- `anima/anima/doc/rng/`: **MISSING** (README.ai.md sits inside modules/rng/)
- `anima/anima/rng/lint.<ext>`: **MISSING** (4th sibling per spec 2026-05-05)
- pluralized `modules/` violates singular convention (target = `module/`)

This pilot is the seed; the rest of anima is type-grouped legacy.

### 1.3 anima-* feature dir compliance

ALL 19 anima-* dirs score 0/4 on triplet (no `core/`, no `module/`, no `doc/`, no `lint.<ext>`). 4 of them have legacy plural `docs/` (anima-physics, anima-voice, anima-hci-research, anima-cpgd-research, anima-tribev2-pilot). The largest cost-center is `anima-engines/` with 166 top-level files (primarily *_phi.hexa engine implementations).

---

## 2. Feature-grouped target layout (Wave B)

### 2.1 Authoritative shape (per hive mk2_apex § canonical_layout)

```
<feature>/
  core/        # source / registry / router / <feature>_main
  module/      # implementations (variants, alternatives) — SINGULAR
  doc/         # *.ai.md, README.ai.md — SINGULAR
  lint.<ext>   # 4th flat sibling (NEW 2026-05-05)
```

Recursive case (`<feature>/module/<X>/{core,module,doc}/lint.<ext>`) when a sub-feature has its own pluggable variants.

### 2.2 anima feature mapping (proposed)

Direct mapping — **anima-** prefix dirs are the features (1 dir = 1 feature):

| feature | target shape | natural sub-feature recursion? |
|---|---|---|
| `anima-core/` | `anima-core/{core,module,doc}/ + lint.hexa` | maybe (lib/, runtime/, verification/) |
| `anima-engines/` | `anima-engines/{core,module,doc}/ + lint.hexa` | likely heavy — 166 *_phi.hexa = candidate sub-features |
| `anima-physics/` | `anima-physics/{core,module,doc}/ + lint.hexa` | yes (analog/arduino/cmos/photonic/quantum/neuromorphic = sub-features) |
| `anima-voice/` | `anima-voice/{core,module,doc}/ + lint.hexa` | yes (audio_*, voice_*) |
| `anima-tools/` | DEFERRED — raw#168 carve-out interaction (see §3) |
| `anima-measurement/` | `anima-measurement/{core,module,doc}/ + lint.hexa` | low |
| `anima-hexad/` | `anima-hexad/{core,module,doc}/ + lint.hexa` | yes (bridge/, c/, d/, e/, m/) |
| `anima-body/` | `anima-body/{core,module,doc}/ + lint.hexa` | low (2 files) |
| `anima-os/` | trivial (0 top-files) — defer or remove | — |
| `anima-serve/` | trivial (1 file) — `anima-serve/{core,module,doc}/ + lint.hexa` | low |
| `anima-hci-research/` | `anima-hci-research/{core,module,doc}/ + lint.hexa` | low |
| `anima-cpgd-research/` | `anima-cpgd-research/{core,module,doc}/ + lint.hexa` | low |
| `anima-tribev2-pilot/` | `anima-tribev2-pilot/{core,module,doc}/ + lint.hexa` | low |
| `anima-agent-channels/` | `anima-agent-channels/{core,module,doc}/ + lint.hexa` | low |
| `anima-agent-core/` | `anima-agent-core/{core,module,doc}/ + lint.hexa` | low |
| `anima-agent-hire-sim/` | `anima-agent-hire-sim/{core,module,doc}/ + lint.hexa` | low |
| `anima-agent-plugins/` | `anima-agent-plugins/{core,module,doc}/ + lint.hexa` | low |
| `anima-agent-providers/` | `anima-agent-providers/{core,module,doc}/ + lint.hexa` | low |
| `anima-agent-skills/` | `anima-agent-skills/{core,module,doc}/ + lint.hexa` | low |

### 2.3 anima/anima/ pilot disposition

Two viable interpretations:

- (a) `anima/anima/` is a **further-nested anima-self feature** — promote to `anima/anima/{rng,...}/{core,module,doc}/lint.<ext>` per-sub-feature
- (b) `anima/anima/` is a **vestigial mount-point** from earlier hive structure — could fold into `anima-core/` or its own sibling feature dir

Recommendation: option (a) at this prep-BG; defer final disposition to EXEC BG with stakeholder sign-off (only place inside anima where singular `module/` naming already exists).

---

## 3. raw#168 minimum-viable carve-outs (NOT moved)

per 2026-05-03 user directive (a) lock-in (`.roadmap.anima_tools.cond.1=decision_locked`, `.blk.1=resolved`):

| carve-out | rationale | enforcement source |
|---|---|---|
| `tool/` (~582 entries) | minimum-viable exception, locked 2026-05-03 | raw#168 + user directive |
| `bin/` (21 entries) | CLI mk2 entry-points (binaries, never feature-internal) | anima_cli_mk2 spec |
| `state/` (~1828 entries) | run artifacts ledger; cross-cutting | raw#82 retraction protocol consumer |
| `.roadmap.*` (~50 files) | per-domain JSONL metadata (mk2 roadmap_format=roadmap_v2_per_domain), not features | mk2_apex per_repo_override.anima |
| `.own` / `.guide` | policy/mandate SSOT | |
| `hypotheses/` (111 entries) | anima-hypotheses-folder-ssot, anima self-axis discovery framework | |
| `config/` (~87 entries) | host pool / pod / cross-feature config | mk2 host_pool component |
| `scripts/` | operational scripts; cross-feature | — |
| `tests/` (~217 entries) | shared test corpus | — |

**Anima-tools interaction**: `anima-tools/` is a feature dir AND `tool/` is the raw#168 carve-out — these are distinct. `anima-tools/` (35 files) MAY migrate to canonical triplet OR fold into top-level `tool/`. EXEC-BG owner decision (this prep flags only).

---

## 4. Migration plan (Phase 1-3)

### 4.1 Phase 1 — low-risk dir renames (NO file moves; safe partial)

Items SP-1 through SP-6 in `safe_partial_migrations.json`:

1. **SP-1** `anima/anima/modules/` → `anima/anima/module/` (singular) + create `anima/anima/doc/rng/` + add `anima/anima/rng/lint.hexa` stub
2. **SP-2** `anima-physics/docs/` → `anima-physics/doc/`
3. **SP-3** `anima-voice/docs/` → `anima-voice/doc/`
4. **SP-4** `anima-hci-research/docs/` → `anima-hci-research/doc/`
5. **SP-5** `anima-cpgd-research/docs/` → `anima-cpgd-research/doc/`
6. **SP-6** `anima-tribev2-pilot/docs/` → `anima-tribev2-pilot/doc/`

Each via `git mv` (history-preserving). Pre-flight: grep for `<feature>/docs/` references across repo, update inline.

Estimated total effort: <6h. Risk: LOW. Rollback: `git revert`.

### 4.2 Phase 2 — feature classification + file moves

For each anima-* dir without a triplet:

1. Inventory top-level files; classify each as `core` / `module` / `doc` / `cross-feature → tool/`
2. Create `<feature>/{core,module,doc}/`
3. `git mv` files to new locations
4. Add `<feature>/lint.<ext>` (initially empty stub or `tool/raw_mk2_loader` delegate)

Heaviest item: `anima-engines/` (166 files). Likely needs sub-feature recursion (each `*_phi.hexa` may be its own sub-feature with `core/module/doc/` recursion).

### 4.3 Phase 3 — cross-link update

1. Update all `import` / `delegate` / `handler` references in `.hexa` files (grep-based sweep)
2. Update `.roadmap.*` `handler:` paths (selective — most roadmap entries point to `tool/` which is unchanged)
3. Update `anima/spec/anima_cli_mk2.spec.yaml` handler paths (only if any `anima-*` features wire-up via spec)
4. Update README.md inline path examples
5. Re-run `tool/raw_mk2_loader` lint pass (catalog walk) to verify no broken references

---

## 5. Cross-repo impact analysis

**No cross-repo impact** — anima self-axis migration:

- All anima-* dirs are **plain dirs** (NOT git submodules; `.gitmodules` does not register them; verified via filesystem check)
- `.gitignore` references `anima-voice/corpus/`, `anima-tribev2-pilot/scripts/install_pod_deps.sh`, etc. — internal-only
- hive does NOT import from anima-* paths (verified per hive mk2_ecosystem_catalog cross-link section)
- nexus / hexa-lang / blueprint do NOT import from anima-* paths (verified per BG-MK2-AUDIT 2026-05-07)
- `infra_state.json` is a symlink to nexus — unaffected

Single risk: external scripts on ubu1/ubu2 hosts may have hard-coded `anima-*/...` paths in cron / orchestrator scripts. Pre-flight: `ssh ubu1 grep -r 'anima-' /home/aiden/scripts/` (EXEC BG owns).

---

## 6. Rollback plan (raw#15 additive)

### 6.1 Pre-migration tag

```
git tag wave-b-pre-migration-2026-05-12
git push origin wave-b-pre-migration-2026-05-12
```

### 6.2 Post-Phase-1 tag

```
git tag wave-b-phase-1-complete-<DATE>
```

### 6.3 Rollback

- Phase 1 only: `git revert <phase-1-merge-commit>` (clean — only `git mv` operations)
- Phase 2 partial: `git reset --hard wave-b-pre-migration-2026-05-12` (within merge window)
- Phase 3 cross-link: forward-fix only (additive — handler path updates leave both old and new paths working via spec aliases)

Per raw#15, NO destructive deletes anywhere; all moves are history-preserving renames.

---

## 7. hive mk2 alignment cross-link

| hive spec section | anima compliance |
|---|---|
| `mk2_apex.spec.yaml § canonical_layout.naming` | post-migration: `core/module/doc` singular ✅ ; pre-migration: 4× `docs/` plural + 1× `modules/` plural ⚠️ |
| `mk2_apex.spec.yaml § canonical_layout.lint_placement` | post-migration: `<feature>/lint.<ext>` flat single-file ✅ ; pre-migration: NONE (0/19 features) ⚠️ |
| `mk2_apex.spec.yaml § canonical_layout.recursive_case` | post-migration: needed for anima-engines (sub-features), anima-physics (analog/arduino/cmos/...), anima-hexad (bridge/c/d/e/m) |
| `mk2_apex.spec.yaml § canonical_layout.flat_docs_disposition` | post-migration: `docs/` becomes catch-all (cross-cutting historical landings); per-feature docs relocate to `<feature>/doc/` |
| `mk2_apex.spec.yaml § canonical_layout.cross_feature_utility_carve_out` | `tool/` at top level matches spec example exactly (`raw_mk2_loader`, etc.) ✅ |
| `mk2_apex.spec.yaml § per_repo_override.anima.disk_state` | currently `modules_docs` ; post-migration: target update to `feature_grouped` ; hive-side spec edit owed |

---

## 8. Honest C3 limits (raw#10, ≥5 mandate)

1. **No actual moves performed** — this BG is analysis + plan only; rate of actual triplet adoption per anima-* feature post-EXEC BG remains unverified until BG-LAYOUT-MIGRATION-WAVE-B-EXEC lands (~2026-05-12).
2. **anima-engines classification debt** — 166 top-level *_phi.hexa files lack ontology mapping; whether they decompose as 166 sibling sub-features OR 1 feature-with-many-modules requires SME (likely a separate ontology BG before EXEC BG can move).
3. **anima-tools vs tool/ disposition unsigned-off** — raw#168 locks `tool/` at top level but does NOT explicitly lock `anima-tools/` (35 files); EXEC BG must clarify with user before moving.
4. **anima/anima/ pilot semantics ambiguous** — whether `anima/anima/` is the canonical anima-self namespace OR a vestigial mount-point not decided; could affect whether anima-* dirs collapse into `anima/anima/<feature>/` OR stay as siblings.
5. **flat docs/ relocation cost not estimated** — 1129 top-level docs/*.md require per-feature ownership classification; signal/noise routing alone is multi-day; out-of-scope for prep BG.
6. **Cross-link sweep coverage incomplete** — grep for `<feature>/docs/` and `<feature>/modules/` not yet executed across all .hexa imports + .roadmap handler paths + .own evidence_trail entries; pre-flight EXEC BG owes this sweep.
7. **ubu1/ubu2 host-side path sweep not performed** — orchestrator scripts on remote hosts may pin `/home/aiden/core/anima/anima-*/...` paths; this prep-BG ran $0 mac local only.
8. **lint.<ext> sibling content unspecified** — spec says "4th sibling, flat single-file" but exact lint payload (delegate to `tool/raw_mk2_loader`? feature-local lint logic? empty stub?) is decision_pending; downstream BG-LINT-SIBLING-PAYLOAD-SPEC may be required.
9. **raw#82 retraction-protocol consumers** in `state/` (1828 entries) are NOT in scope for migration but their handler paths inside roadmap entries may change if `<feature>/module/<X>` rename ripples — exec BG must update `.roadmap.<X>` handler fields conservatively.

---

## 9. Verdict summary

- **current_state_summary**: anima `disk_state: modules_docs` per mk2_apex per_repo_override — verified via filesystem survey; 0/19 anima-* features compliant; 1 partial pilot (`anima/anima/{core,module}/rng` with singular naming but missing doc/ + lint sibling); 9 carve-outs preserved per raw#168.
- **target_state_summary**: 19 anima-* features each with `<feature>/{core,module,doc}/ + lint.<ext>` triplet ; carve-outs unchanged ; `anima/anima/` pilot completed (doc/rng + lint added) ; flat `docs/` reduced to cross-cutting catch-all.
- **migration_phase_count**: 3 (Phase 1 dir renames / Phase 2 file moves with classification / Phase 3 cross-link update).
- **safe_partial_count**: **6** (SP-1 through SP-6, all dir renames with `git mv`, history-preserving, blast radius isolated).
- **blocking_issues**: anima-engines ontology debt (DEF-1) ; anima-tools vs tool/ user sign-off (DEF-2) ; anima/anima/ semantics (DEF-3) ; flat docs/ classification cost (DEF-4) ; modules/ root bridge disposition (DEF-5).
- **raw_invariants_compliance**: raw#9 ✅ (hexa + Bash analysis only) ; raw#10 ✅ (9 honest_c3) ; raw#15 ✅ (NO destructive ops, all `git mv` planned) ; raw#168 ✅ (9 carve-outs respected).
- **status**: NOT `ALREADY_COMPLIANT` ; NOT `BLOCKED` ; **PLANNING_LANDED — exec deferred to BG-LAYOUT-MIGRATION-WAVE-B-EXEC ~2026-05-12**.

---

## 10. Cross-reference index

- hive: `hive/spec/mk2_apex.spec.yaml § sections.canonical_layout` (lines 362-468)
- audit: `docs/anima_mk2_compliance_audit_2026_05_07.md § 1.2 / § 4.2.3`
- spec: `anima/spec/anima_cli_mk2.spec.yaml § 15` (cycle_amend_2026_05_07.hive_mk2_compliance_gaps.g12)
- pilot: `anima/anima/{core,module}/rng/`
- artifacts: `state/anima_canonical_layout_migration_wave_b_prep_2026_05_07/{survey.json,safe_partial_migrations.json,verdict.json}`
- exec successor BG: BG-LAYOUT-MIGRATION-WAVE-B-EXEC (~2026-05-12)
- mandates: (all consulted; no conflict — migration is operational, additive, non-falsifier-bearing)
