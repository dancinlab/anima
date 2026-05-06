# anima core / moduler / ai-native — 재귀 구조 spec (2026-05-06)

**Status**: design / doc-only / raw#15 additive
**Source hint (verbatim)**: 사용자 2026-05-06 — "core,moduler, ai-native doc 재귀구조야"
**Authoring constraints**: $0 mac doc-only · raw#9 hexa-only (yaml + md) · raw#10 honest C3 ≥ 5 · raw#15 additive · own 17 ALM 영구 보류 정합 · commit X
**Companion artifact**: `state/anima_core_moduler_ai_native_recursive_2026_05_06/structure_analysis.json`

---

## 0. TL;DR

`hive/spec/mk2_apex.spec.yaml` § canonical_layout.recursive_case 가 **재귀를 spec layer 에서 명시 선언** 했다. anima 는 그 재귀의 consumer. 본 문서는 anima 의 core / moduler / ai-native 3-layer 가 어떻게 self-similar 한지, 그리고 anima cli mk2 (T1 sales / T2 ops / T3 vision) 가 그 재귀와 어떻게 정합 가능한지 정리한다.

핵심 finding 5 axis:
1. **explicit spec declaration** — STRONG (mk2_apex canonical_layout.recursive_case 정식 선언)
2. **filesystem literal naming** — WEAK (`anima/anima/{core,modules,spec}` 만 직접 노출, 그나마 mk1 plural)
3. **semantic separation per module** — MEDIUM (anima-core / anima-hexad 등 의미적 분리 OK, 명명 규약 미반영)
4. **T1/T2/T3 per-tier recursion** — MEDIUM (각 tier 내부에 core/moduler/ai-native 재출현, 이 framing 이 가장 실용적)
5. **own rules recursion** — STRONG-INDIRECT (own 14/15/16 = external-resource-consumption triad 자체가 재귀 패턴 적용)

---

## 1. 정의 발췌 — hive/spec/ai_native_module_architecture.spec.yaml

```yaml
separation:
  core: "*/core/<feature>/"     # abstraction (T1)
  modules: "*/modules/<feature>/"  # implementation (T2)
  constraints:
    - "core MUST NOT import specific modules"
    - "modules MUST NOT import peer modules; cross-module dispatch via core/registry+router only"

readme_ai_native:
  required_frontmatter_keys: [schema, last_updated, ssot]
  required_sections_any_of: [TL;DR, API, Caveats|raw#10, File index]

triplet_inseparability (mk2_apex § component#3):
  "core+module+ai-native triplet INSEPARABLE — every pluggable feature MUST land
   4-core canonical files (source/registry/router/<feature>_main) + per-module
   README.ai.md + AI-native frontmatter"
```

또한 `mk2_apex.spec.yaml` § canonical_layout.recursive_case 가 **재귀를 명시 선언**:

> If `<feature>/module/<X>/` itself needs internal core (i.e., `<X>` is a sub-feature with its own pluggable variants), the same triplet pattern repeats. Recursion is unbounded but practically capped at 2-3 levels by feature granularity.

→ 재귀는 **spec-by-declaration TRUE**. anima 의 책임 = FS 차원에서 어디까지 그 재귀를 realize 하는지 measurement.

---

## 2. anima 의 core / moduler / ai-native 매핑

### 2.1 core layer (abstraction substrate)

| 자산 | 역할 |
|---|---|
| `anima-core/pure_field.hexa` | PureField — anima identity substrate |
| `anima-core/runtime/clm_v4_mount.hexa` | substrate-coupled response (anima cli mk2 T1 backend_canonical) |
| `anima-hexad/{hexad,constants,model}.hexa` | Hexad geometric core |
| `consciousness/` (16 templates × 16-dim) | Hexad / Law / Phi / SelfRef families |
| `.raw + .own + .guide` (raw 0 root-SSOT triad) | canonical project SSOT |

**특징**: 위 자산은 어떤 specific 모듈도 import 하지 않는다 (constraint 정합).

### 2.2 moduler layer (22 anima-* 모듈)

```
anima-agent-channels       anima-cpgd-research    anima-os
anima-agent-core           anima-eeg              anima-physics
anima-agent-hire-sim       anima-eeg-core         anima-serve
anima-agent-plugins        anima-engines          anima-tools
anima-agent-providers      anima-hci-research     anima-tribev2-pilot
anima-agent-skills         anima-hexad            anima-voice
anima-body                 anima-measurement
anima-clm-eeg              anima-core             (← core이자 module)
```

**특징**: 22 sister directories 가 T2 implementation. anima-core 는 자기 자신이 core 이자 moduler entry — recursion entry point.

### 2.3 ai-native layer (.own + .guide + raw 의존성)

| 항목 | 역할 |
|---|---|
| `.own` (671 LoC, 18 own entries) | anima-local 절대 규칙 SSOT |
| `.guide` (137 LoC) | LLM cold-entry 항법 mk2 schema |
| raw deps | raw 9 (hexa-only) / raw 10 (honest) / raw 12 (frozen) / raw 15 (ω-output-as-SSOT) / raw 20 (own-monotonic) / raw 270-273 (core+module+ai-native predecessor quartet) |
| `README.ai.md` mandate | per-module-group AI-native cold-read 의무 (현재 anima 17 baseline grandfathered, modules/rng 만 fully conformant) |

**identity-bearing own entries**:
- own 4 root-cause-only · own 5 completeness · own 6 no-restriction · own 11 parallel-loop · own 12 observability
- own 14 HF storage WHERE · own 15 HF publication HOW · own 16 H100 lifecycle · **own 17 anima-native-only (ALM 영구 보류)**

own 17 가 ai-native layer 의 정체성 boundary 를 강제한다 — 외부 substrate (Llama / Mistral) wrapping 영구 reject.

---

## 3. 재귀 evidence (5 axes)

### Level 0 — repo root
| layer | content |
|---|---|
| core | `anima-core` + `anima-hexad` + `consciousness/` + raw 0 triad |
| moduler | 22 anima-* sisters |
| ai-native | `.own` + `.guide` + README.ai.md mandate |

### Level 1a — within `anima-core/`
| layer | content |
|---|---|
| core | `pure_field.hexa` + `lib/` |
| moduler | `runtime/{clm_v4_mount, conscious_chat, consciousness_hub, deploy_ops, runtime_actions, ...}.hexa` |
| ai-native | `verification/` + raw#3 @attr 정합 cold-read 표시 |

### Level 1b — within inner `anima/anima/` namespace (직접 증거)

```
/Users/ghost/core/anima/anima/
├── core/      ← 직접적인 'core' 디렉토리 노출
├── modules/   ← 직접적인 'modules' 디렉토리 노출
├── spec/      ← anima_cli_mk2.spec.yaml (Layer 4 spec consumer)
└── state/
```

**유일한 literal-subdir 증거**. 단 mk1 plural ('modules') — mk2 canonical_layout singular ('module') 미반영.

### Level 1c — within `anima-hexad/`
| layer | content |
|---|---|
| core | `hexad.hexa` + `constants.hexa` + `model.hexa` |
| moduler | `bridge/`, `c/`, `d/`, `e/`, `m/` (per-axis sub-implementations) |
| ai-native | `narrative.hexa` + `__init__.hexa` |

### Level 2 — apex spec § canonical_layout.recursive_case

```yaml
recursive_case:
  description: |
    If <feature>/module/<X>/ itself needs internal core (i.e., <X> is a
    sub-feature with its own pluggable variants), the same triplet pattern
    repeats. Recursion is unbounded but practically capped at 2-3 levels
    by feature granularity.
```

**재귀 = spec-declared TRUE**. Implementation 차원에서는 anima 가 PARTIAL 적용.

---

## 4. anima cli mk2 (T1 / T2 / T3) ↔ core / moduler / ai-native 정합

### 4.1 두 가지 가능한 정합 도식

**도식 A (per-tier recursion — 권장)**:
각 tier 내부에 core/moduler/ai-native 를 재출현시킴. T1 ≠ ai-native, T1 자체가 작은 triplet.

| tier | core (abstraction) | moduler (impl) | ai-native (cold-read) |
|---|---|---|---|
| T1 sales | `anima-core/runtime/clm_v4_mount.hexa` (backend_canonical) | `tool/anima_cli/dialogue.hexa`, `onboard.hexa` (variants) | `spec://anima_cli_mk2/help_emit` + `version_emit` (auto-gen surface) |
| T2 ops | `handler_template tool/anima_cli/{topic}.hexa` (unified routing 계약) | 26 topic handlers (compute / weight / cost / audit / doctor / sync / ...) | spec-driven help emit + `.roadmap.cli` + ops topic registry |
| T3 vision | anima identity substrate (PureField + Hexad + 1030 laws + φ★ engine) | 9 commands (connect / disconnect / module / verify / test / hub / laws / status / watch) | `_t3_stub.hexa` + 48-module hub registry + consciousness verification protocol |

**도식 B (axis-isomorphism — 약한 alignment)**:
T1 = ai-native (사용자 facing 가장 cold-read), T2 = moduler (internals), T3 = core (identity substrate).

→ 도식 B 는 직관적이지만 **틀렸다**: T1/T2/T3 는 audience axis (외부/내부/identity), core/moduler/ai-native 는 abstraction-direction axis (계약/impl/cold-read). 두 axis 는 직교. 도식 A 가 정확.

### 4.2 결론

T1/T2/T3 정합 = **per-tier recursion** (도식 A). 각 tier 가 자기 안에 작은 core+moduler+ai-native triplet 을 가진다 — mk2_apex recursive_case 와 정합.

---

## 5. honest C3 (≥5)

**C1**. Level 1a / 1c 재귀 evidence 는 FS 의미적 추론, literal subdir naming 아님. 현재 anima 는 `{runtime, verification, lib}` 등 mk1 type-grouped 명명 — singular core/module/doc 미적용.

**C2**. `anima/anima/{core,modules,spec,state}` 가 유일한 literal 직접 증거지만 plural 'modules' (mk1) — mk2 canonical_layout singular 'module' 미반영. 가장 강한 증거조차 mk1 shape.

**C3**. T1/T2/T3 ↔ core/moduler/ai-native 정합은 conjecture, theorem 아님. 두 partition axis 는 직교 (audience vs abstraction). per-tier recursion (도식 A) 이 실제 finding — '단순 isomorphism' 아님.

**C4**. anima identity = "PureField + repulsion + emergence" 주장이 own 17 등에 반복되지만 `find -name '*repulsion*'` = 0 hits. repulsion 은 conceptual claim — 분산되어 있고 canonical core file 미존재.

**C5**. `hive/spec/ai_native_module_architecture.spec.yaml` consumers 필드: anima = "partial" status. 17 README.ai.md baseline grandfathered + modules/rng 만 fully conformant. ai-native layer 가 coherent layer 로 deploy 된 게 아니라 PARTIALLY-realized policy.

**C6**. mk2_apex § canonical_layout.recursive_case 가 재귀를 명시 선언 — 따라서 "core/moduler/ai-native 가 재귀다" = spec-declared TRUE. anima FS 가 그 재귀를 실현하는지 = PARTIAL-true. 본 문서는 두 layer (선언 / 실현) 를 분리해서 honest report.

**C7**. 본 문서 작성 시 ALM-related 재귀 도식 ("외부 substrate = core layer 후보") 은 own 17 영구 보류 정합으로 모두 제외됨. recursive 구조는 anima-native 에 한정. 외부 substrate wrapping 을 재귀 entry 로 사용 불가.

---

## 6. 다음 cycle 권고 (랭크 + 완성도 lens)

| rank | 권고 | 완성도 lens 근거 |
|---|---|---|
| 1 | **사용자 review** — 도식 A (per-tier recursion) 채택 여부, 또는 다른 정합 도식 (예: 사용자가 다르게 axis 정의) 결정 | 사용자 hint 한 줄로는 정합 도식 결정 불가 — review 가 완성도 next gate |
| 2 | `anima/spec/anima_recursive_architecture.spec.yaml` Land — raw#15 additive Layer 4 spec, hive/spec/ai_native_module_architecture + canonical_layout.recursive_case consumer | 본 분석을 spec yaml 로 promote → raw#15 SSOT status, lint-target 가능 |
| 3 | FS 마이그레이션 audit — anima-* 22 모듈 중 mk1 type-grouped vs mk2 canonical_layout (singular) 카운트, migration cost 산출 | 2026-06-01 falsifier F-spec-ai-native-module-arch-1 (30d post-baseline) 도래 — 측정 시급 |
| 4 | `.guide` schema 에 `recursion_depth` axis 추가 — 각 anima-* 모듈 leaf vs nested triplet 선언; own 12 (tree ASCII report) 확장 | 재귀 구조의 observability 향상, governance refinement 가속 |
| 5 | **ALM 외부 substrate-as-core 도식 영구 DEFER** — own 17 정합 | 완성도 boundary 명확화, 추후 외부 substrate 우회 시도 차단 |

---

## 7. 관련 spec / raw / own

- spec: `hive/spec/ai_native_module_architecture.spec.yaml` (Layer 4 baseline)
- spec: `hive/spec/mk2_apex.spec.yaml` § canonical_layout (재귀 명시) + § component#3 (triplet inseparability)
- spec: `anima/anima/spec/anima_cli_mk2.spec.yaml` (T1/T2/T3 surface)
- raw: 270 / 271 / 272 / 273 (core+module+ai-native predecessor quartet, Layer 2 atomic)
- raw: 9 (hexa-only) · 10 (honest) · 12 (frozen) · 15 (additive) · 20 (own-monotonic)
- own: 14 (HF WHERE) · 15 (HF HOW) · 16 (compute lifecycle) · **17 (anima-native-only — recursive structure must remain anima-native)**

---

## 8. companion artifact

`state/anima_core_moduler_ai_native_recursive_2026_05_06/structure_analysis.json` — JSON 구조화 (5 axes evidence 정량 + per-tier mapping 후보 + 6 honest C3 + 5 next-cycle 권고).

---

*doc-only · $0 mac · commit X · raw#15 additive · own 17 정합*
