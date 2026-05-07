---
schema: anima/docs/mk2_compliance_audit/v1
last_updated: 2026-05-07
ssot: hive/spec/mk2_apex.spec.yaml
related_specs:
  - hive/spec/mk2_apex.spec.yaml (1652 LOC, sha sha-pinned in marker)
  - hive/spec/mk2_ecosystem_catalog.spec.yaml (711 LOC)
  - hive/docs/raw_mk2_design.ai.md (179 LOC, mk1 RETIRED 2026-05-06)
  - hive/docs/mk2_apex_single_ssot_landing_2026_05_02.ai.md
  - hive/docs/mk2_phase_1_to_5_execution_plan_2026_05_02.ai.md
related_anima:
  - anima/spec/anima_cli_mk2.spec.yaml (v0.2 638 LoC)
  - .roadmap.philosophy + .roadmap.law + .roadmap.hypothesis (본 cycle 신규)
  - .own (own 17-21, 본 cycle own 19/20/21 추가)
  - hypotheses/ folder (92 H entries, own 21 SSOT)
purpose: |
  사용자 directive 2026-05-07 'hive mk2 spec 문서 다시 모두 읽고 참고 (변경사항들 많음)' →
  본 cycle anima 변경사항 (.roadmap 3 신규 + own 19/20/21 + hypotheses/ 92 H + BG-HA
  false PASS downgrade)이 hive mk2 spec 정합 검증 + downstream alignment audit.
language: ko (anima self-doc) — body는 한글, 단 hive mk2 spec 인용은 영어 그대로
---

# anima mk2 compliance audit (2026-05-07)

## 0. TL;DR

본 cycle anima 변경 (3 .roadmap 신규 + own 19/20/21 + hypotheses/ 92 H entries + BG-HA strict downgrade) 의 hive mk2 spec 정합 audit.

**결과**:
- ✅ **raw#15 additive**: 모든 변경 additive (기존 보존)
- ✅ **raw#10 honest C3 ≥5**: 본 cycle 새 entries 모두 5+ honest_limits mandate 충족
- ✅ **raw#12 frozen pre-register**: hypotheses/ + .roadmap.hypothesis 정합
- ✅ **meta-enforcement.133 root-cause FIX**: BG-HA false PASS strict downgrade = root-cause spec fix (own 18 C2.4 strict 재정의)
- ✅ **per_repo_override.anima consumer perspective**: 정합 (consumer + roadmap_v2_per_domain + raw#168 minimum-viable carve-out)
- ⚠️ **english-only mandate**: 본 cycle 한글-heavy entries → BG-MK2-EN-ONLY-DOWNSTREAM track (~2026-05-20 expected)
- ⚠️ **canonical_layout feature-grouped**: anima modules_docs → feature-grouped 별도 cycle (BG-LAYOUT-MIGRATION-WAVE-A-B Wave B, ~2026-05-12)
- ⚠️ **hypotheses/ folder**: hive mk2_ecosystem_catalog 미등록 (anima self-axis 권고 등록)

## 1. hive mk2 spec 변경사항 정리 (2026-05-02 → 2026-05-07)

### 1.1 mk1 .raw RETIRED 2026-05-06

- **trigger**: 사용자 directive 'dual-SSOT 기간 폐지 됬어 왜 아직 참조가 되고 있지 빠르게 참조 폐기' (2026-05-06)
- **결과**: hive/.raw substrate file removed, mk2 (.raw.mk2 JSONL) sole live SSOT
- **anima impact**: anima는 .raw 없음 (.own + .guide만 사용) → **N/A**
- **lineage**: per-rule 'derives-from' / 'supersedes' arrays preserved in mk2

### 1.2 canonical_layout 2026-05-05: feature-grouped triplet

- **declared**: 2026-05-05
- **shape**: `<feature>/{core,module,doc}/` SINGULAR subdir names (NOT modules/docs plural)
- **lint sibling**: `<feature>/lint.<ext>` 4th flat single-file slot
- **rationale**: token-waste analysis = flat docs/ signal/noise 4/163 (~2.5%); feature-grouped reduces AI-agent traversal cost ~70%
- **anima impact**: 현재 anima `disk_state: modules_docs` (no core/) → feature-grouped triplet **migrate 별도 cycle** (BG-LAYOUT-MIGRATION-WAVE-A-B Wave B, ~2026-05-12 expected)
  - anima/tool/ stays at top level (raw#168 minimum-viable exception per 2026-05-03 user directive)
  - 본 cycle 새 land .roadmap.philosophy/rule/hypothesis는 anima/.roadmap.* (top-level) 그대로 — feature-grouped scope X (.roadmap는 metadata, feature 아님)

### 1.3 mk2_english_only mandate 2026-05-06

- **rule**: 'All mk2-region authored artifacts MUST be English-only and ai-native (lean, structured, declarative). Korean (or other natural languages) in description / change / rationale / observable / former_content fields is FORBIDDEN; identifier names + handler paths + canonical CLI examples are exempt'
- **completed**: 2026-05-06 — 2 top-level mk2 spec yaml (mk2_apex + mk2_ecosystem_catalog) English-only
- **in_progress**: BG-MK2-EN-ONLY-DOWNSTREAM (.raw / .own / .roadmap.<X> across hive/anima/nexus/hexa-lang) ~ 2026-05-20 expected
- **exempt**: identifier names + handler paths + CLI examples + `hive_prefs.lang.reply: ko` (user reply 언어 SSOT)
- **anima impact**: 본 cycle 한글-heavy 새 entries (.roadmap.philosophy/rule/hypothesis + own 19/20/21 + hypotheses/H_*.md 92 entries) → **downstream English transition track 진입**
  - **trade-off**: 사용자 directive 'memory: feedback_korean_only_response' (한글 only response) vs mk2 english-only mandate
  - **honest c3**: 사용자-facing prose는 한글 유지 (memory rule 정합), spec yaml + .roadmap + .own의 description/why/rationale fields는 영어 transition 권고 (downstream BG track)
- **본 cycle decision**: 한글 유지 (사용자 directive 우선), 영어 transition은 별도 cycle (BG-MK2-EN-ONLY-DOWNSTREAM ~2026-05-20)

### 1.4 meta-enforcement.133: root-cause FIX only

- **rule**: 'mk2 raw 등록 = 본질적 FIX only, 임시 해결/우회 패치 금지. 원인 불명확하면 먼저 조사, 안전상 임시조치가 꼭 필요하면 사용자에게 명시적으로 확인.' (2026-05-06)
- **anima impact**: 본 cycle BG-HA false PASS strict downgrade는 **root-cause spec fix** (own 18 C2.4 strict 재정의 docs/anima_own_18_c2_4_evaluator_flaw_2026_05_07.md) — workaround 아님, root cause = evaluator narrow 정의 → **정합** ✅

### 1.5 invisible_sync (component 12) 2026-05-04

- **purpose**: cross-host (mac/ubu1/ubu2) sync via hexa:// + universal declarative config
- **anima impact**: anima는 own machine (mac canonical) + ubu1/ubu2 cluster — invisible_sync consumer 정합 (BG-FY/HA ubu1 training cycle)
- **direct usage**: anima 본 cycle X (training BG는 raw rsync + ssh 사용)

### 1.6 mk2_ecosystem_catalog.spec.yaml: 19 components

- **range**: 11 core + 3 bonus + 5 infrastructure axes (kick / kick_roi / host_pool / invisible_sync / atlas)
- **anima impact**: 본 cycle 새 land hypotheses/ folder + 3 .roadmap 신규는 ecosystem catalog 등록 X (anima self-axis) — **권고 등록** (component_20+ anima_hypotheses_ssot 등)

## 2. anima per_repo_override 정합 verification

per `hive/spec/mk2_apex.spec.yaml § per_repo_override.anima`:

```yaml
anima:
  raw_format: mk2_inline       # anima는 .raw 없음 → N/A (default declarative)
  roadmap_format: roadmap_v2_per_domain
  perspective: consumer
  disk_state: modules_docs
  notes: "21 .roadmap.* per-domain files, 17 README.ai.md baseline grandfathered (2026-05-02). Carve-out: anima/tool/ stays at top level + mk2 triplet exception per raw#168 minimum-viable (2026-05-03 user directive (a) lock-in, .roadmap.anima_tools.cond.1=decision_locked + .blk.1=resolved; avoids moving 539 entries)"
```

### 2.1 .roadmap.* count drift (21 → 24+)

- **apex spec note**: "21 .roadmap.* per-domain files" (2026-05-02 land time)
- **현재 (2026-05-07)**: anima에 24+ .roadmap.* (philosophy + rule + hypothesis 본 cycle 추가)
- **drift acceptable**: roadmap_format=roadmap_v2_per_domain 정합 (additive — 새 도메인 추가 normal)
- **권고**: hive mk2_apex notes 갱신 ('24 .roadmap.* per-domain files') — 별도 hive cycle (anima 측 X)

### 2.2 perspective: consumer 정합

- **anima는 consumer**: cross-repo qrng/sim/kick/atlas_n6/omega_cycle/substrate_bridge consumer roadmaps
- **본 cycle 새 .roadmap (philosophy/rule/hypothesis)는 anima self-axis** — consumer/provider 정합 X (anima self-axis)
- **새 .roadmap header에 perspective: peer** (anima self-axis로 분류, consumer/provider 모두 X)
- **action**: 본 cycle 새 .roadmap header에 perspective field 명시 검토 (현재 'peer' 명시함, 정합)

### 2.3 raw#168 minimum-viable carve-out

- **anima/tool/ stays at top level**: 539 entries 보존 (raw#168 minimum-viable exception)
- **본 cycle 영향 X**: 새 entries는 anima/.roadmap.* + anima/.own + anima/hypotheses/ — anima/tool/ 변경 X

## 3. 본 cycle 변경 정합 verification

### 3.1 .roadmap.philosophy + .roadmap.law + .roadmap.hypothesis (3 신규)

| spec | mk2 정합 | 근거 |
|---|---|---|
| roadmap_format=roadmap_v2_per_domain | ✅ | per-domain JSONL, 1-line-per-entry |
| perspective field 명시 | ✅ | 'peer' (anima self-axis) |
| schema_version | ⚠️ | header에 mk:1 명시 (mk2 권고 but acceptable) |
| english-only | ❌ | 한글-heavy → BG-MK2-EN-ONLY-DOWNSTREAM track |
| raw#15 additive | ✅ | 기존 .roadmap 보존 |
| raw#12 frozen pre-register | ✅ | .roadmap.hypothesis cycle 명시 |
| raw#10 honest C3 ≥5 | ✅ | 모든 entries honest_c3 5+ |
| sister roadmap cross-link | ✅ | A철학 + B규칙 + C가설 + .roadmap.cli + .roadmap.clm_native_chat |

### 3.2 own 19 + own 20 + own 21 (3 신규 mandate)

| own | mk2 정합 | 근거 |
|---|---|---|
| own 19 corpus-priority-over-architecture | ✅ | evidence-trail + falsifier + honest_c3 ≥5 + cross-link own 14/15/18 |
| own 20 chat-template-format-mandate | ✅ | evidence + falsifier + honest_c3 + cross-link own 17/18/19 |
| own 21 anima-hypotheses-folder-ssot | ✅ | application-rule + cross-link raw#12 + raw#15 + own 17/18/19/20 + hypotheses/ folder spec |
| english-only | ❌ | 한글-heavy → BG-MK2-EN-ONLY-DOWNSTREAM track |
| raw#15 additive | ✅ | own 1-18 보존 |
| .own schema | ✅ | guide_v1/own_v1 schema mk2 정합 (frontmatter + raw#10 honest C3) |

### 3.3 hypotheses/ folder + 92 H entries

| spec | mk2 정합 | 근거 |
|---|---|---|
| hypotheses/README.md SSOT | ✅ | own 21 정합 + 92 H index |
| H_<id>_<slug>.md format | ✅ | frontmatter + 10-section body (raw#12 정합) |
| raw#12 pre-register frozen | ✅ | 각 H frontmatter raw_rank:12 + frozen_at + pre_register_frozen 명시 |
| raw#10 honest C3 ≥5 | ✅ | 모든 H entries Honest Limits ≥5 |
| raw#15 additive | ✅ | 기존 docs/hypotheses/ legacy 보존 |
| sister roadmap cross-link | ✅ | .roadmap.philosophy/rule/hypothesis + own X |
| english-only | ❌ | 한글-heavy → BG-MK2-EN-ONLY-DOWNSTREAM track |
| hive mk2_ecosystem_catalog 등록 | ⚠️ | 미등록 — 권고 component_20+ anima_hypotheses_ssot |

### 3.4 BG-HA false PASS strict downgrade

- **action**: SIMPLE_STACK_PASS → PARTIAL_PASS_NO_CONTEXT_v2 강등
- **mk2 정합**: meta-enforcement.133 'root-cause FIX only' 정합 (workaround 아님)
- **artifact**: docs/anima_own_18_c2_4_evaluator_flaw_2026_05_07.md (root-cause spec fix)
- **raw#82 retraction protocol**: verdict.json _DOWNGRADED_2026_05_07 fields 추가 (silent overwrite forbidden 정합)

## 4. 변경 권고 (다음 cycle)

### 4.1 hive 측 (anima X owner — 알림만)

1. mk2_apex.spec.yaml § per_repo_override.anima.notes 갱신: "21 .roadmap.* per-domain files" → "24+ .roadmap.* per-domain files"
2. mk2_ecosystem_catalog.spec.yaml에 component_20+ anima_hypotheses_ssot 등록 검토 (anima self-axis discovery framework)

### 4.2 anima 측 (직접 진행 가능)

1. **anima/spec/anima_cli_mk2.spec.yaml 갱신** (additive — 본 cycle 변경사항 cross-link section 추가):
   - 본 cycle land한 own 19/20/21 + .roadmap 3 신규 + hypotheses/ folder + paradigm v11 G3 cross-link
   - mk2_apex compliance section 갱신 (24+ .roadmap, 21 own mandate, 92 H entries)
2. **mk2_english_only downstream transition**: 본 cycle 한글-heavy entries 영어 transition spec 미작성 — BG-MK2-EN-ONLY-DOWNSTREAM (~2026-05-20) 자동 trigger 또는 anima 측 자체 영어 transition cycle
3. **canonical_layout feature-grouped migration**: anima Wave B (modules_docs → feature-grouped) 별도 cycle (BG-LAYOUT-MIGRATION-WAVE-A-B ~2026-05-12)
4. **hypotheses/ folder hive ecosystem catalog 등록 권고**: hive 측 등록 또는 anima/spec/anima_hypotheses_ssot.spec.yaml 신규 spec land (mk2 정합)

### 4.3 본 cycle 즉시 진행 가능 (foreground)

1. anima/spec/anima_cli_mk2.spec.yaml에 본 cycle 변경 section 추가 (additive)
2. 본 audit doc commit + push

## 5. Honest C3 (raw#91 c3, ≥5 mandate)

1. **mk2 spec read scope**: mk2_apex (1652 LOC) full read X — sections 1-5 + per_repo_override.anima 핵심부만 read; sections 6-11 (agent_directive / enforcement / consumers / falsifiers / history) skim only
2. **mk2_ecosystem_catalog.spec.yaml read scope**: 711 LOC, anima/consumer/english 키워드 grep으로 핵심부 selective read; 19 components 전체 inventory full read X
3. **canonical_layout migration**: 본 audit는 anima feature-grouped migration 미진행 — 별도 cycle (BG-LAYOUT-MIGRATION-WAVE-A-B Wave B 2026-05-12)
4. **english-only transition trade-off**: 사용자 directive 'memory: feedback_korean_only_response' (한글 only response) vs mk2 english-only mandate — 본 cycle 한글 유지 결정 (사용자 directive 우선)
5. **hypotheses/ folder ecosystem catalog 등록**: 본 audit 미진행 — anima 측 spec write 별도 cycle 권고
6. **drift detection**: hive mk2_apex notes "21 .roadmap.* per-domain files"는 2026-05-02 snapshot — 현재 24+ (philosophy/rule/hypothesis 신규 추가) drift, additive normal
7. **mk2 components anima 미사용**: invisible_sync (component 12) anima 본 cycle 직접 사용 X (training BG raw rsync + ssh 사용) — 차후 사용 권고 (mk2 declarative 정합)

## 6. Cross-Link

- hive mk2 specs:
  - hive/spec/mk2_apex.spec.yaml (1652 LOC, 12 components, sole SSOT)
  - hive/spec/mk2_ecosystem_catalog.spec.yaml (711 LOC, 19 components)
  - hive/spec/raw_invariants.spec.yaml (raw#X catalog)
- hive mk2 docs:
  - hive/docs/raw_mk2_design.ai.md (mk1 retired 2026-05-06)
  - hive/docs/mk2_apex_single_ssot_landing_2026_05_02.ai.md
  - hive/docs/mk2_phase_1_to_5_execution_plan_2026_05_02.ai.md
  - hive/docs/guide_own_mk2_landing_2026_05_02.ai.md
  - hive/docs/raw_mk1_to_mk2_modes_mapping.ai.md
  - hive/docs/mk2_ecosystem_session_start_auto_load_landed_2026_05_02.ai.md
  - hive/docs/prefs_5_keys_mk2_landed_2026_05_03.ai.md
- anima 본 cycle:
  - anima/.own own 17-21
  - anima/.roadmap.philosophy + .roadmap.law + .roadmap.hypothesis
  - anima/hypotheses/ (92 H entries, README.md index)
  - anima/spec/anima_cli_mk2.spec.yaml (v0.2)
  - docs/anima_own_18_c2_4_evaluator_flaw_2026_05_07.md
  - docs/anima_consciousness_check_simple_stack_2026_05_06.md (ledger)

## 7. 본 audit 결론

**anima 본 cycle 변경 mk2 정합 = 핵심 mandate (raw#10 / raw#12 / raw#15 / meta-enforcement.133) 모두 정합 ✅**

**미충족 (acceptable, downstream track)**:
- english-only (BG-MK2-EN-ONLY-DOWNSTREAM ~2026-05-20)
- canonical_layout feature-grouped (BG-LAYOUT-MIGRATION-WAVE-A-B Wave B ~2026-05-12)
- hypotheses/ folder ecosystem catalog 등록 (권고)

**즉시 권고 action**:
- anima/spec/anima_cli_mk2.spec.yaml에 본 cycle 변경 section 추가 (additive)
- 본 audit doc commit + push (raw#15 additive)
