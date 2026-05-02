---
schema: anima/docs/anima_self_mk2_tuning_landed/ai-native/1
last_updated: 2026-05-02
ssot:
  marker: state/markers/anima_self_mk2_tuning_landed.marker
  roadmap_dir_pattern: <repo>/.roadmap.<domain>
  baseline_ai_native: .ai-native-readme-baseline
status: AUDIT_LANDED_SPEC_ONLY
related_raws:
  - raw 9    # hexa-only orchestration (audit-only, no impl emitted)
  - raw 10   # honest C3 caveats inline
  - raw 11   # snake_case
  - raw 15   # env() lazy + <user> placeholder
  - raw 270  # ai-native readme triplet (audit + new candidates)
  - raw 271  # core+module pattern (audit + new candidates)
  - raw 272  # lint extension
  - raw 273  # hierarchy connection direction
  - raw 12   # silent-error ban (no fab)
  - raw 175  # BR-NO-USER-VERBATIM (no verbatim user quotes in this doc)
preserved_unchanged:
  - all 26 existing .roadmap.* (mk2) files
  - all module dirs under anima/{core,modules}, anima-eeg/, anima-clm-eeg/, anima-physics/, anima-speak/, anima-engines/, serving/, training/, tool/
  - all existing README.ai.md (19 files at land-time)
  - .ai-native-readme-baseline (empty/conformed)
policy:
  migration: forbidden
  changes: additive_only
  in_place_writes: zero
  destructive_ops: zero
  cost_usd: 0
  substrate: mac-local
---

# anima self mk2 tuning — domain audit + new .roadmap.<domain> candidates + raw 270 triplet plan

## TL;DR

mk2 roadmap system은 26 domain (clm/eeg/akida/qrng/sim/voice/tensionlink + 11 substrate consumer + 8 meta) 까지
land 됐지만 **anima 자신**의 핵심 implementation surface 9곳이 아직 mk2 .roadmap.<domain> 으로 mirror 되지 않음.

본 audit 결과:

- **추가 권고 신규 .roadmap.<domain>** = 9개 (serving, training, anima_physics, anima_speak, anima_clm_eeg,
  anima_engines, anima_agent, anima_tools, tool) — spec only emit, 실제 .roadmap.* 파일 생성 X (additive only,
  사용자 lock-in 후 별도 cycle).
- **raw 270/271 triplet 적용 audit** = 19 README.ai.md 가 land 됐으나 위 9 surface는 모두 미적용. 권장 priority
  rank A/B/C.
- **마이그레이션 0건 emit**, in-place write 0건, additive only.

26 기존 .roadmap.* 파일은 모두 무수정 보존. 본 doc + marker 1개만 신규 생성.

## §1 Existing 26 .roadmap.<domain> inventory (audit, 무수정)

### §1.1 Domain (single substrate, 14)

| domain | size_b | kind | perspective | provider_dep |
|---|---:|---|---|---|
| clm | 2583 | domain | own | — |
| eeg | 363 | domain | own | — |
| voice | 1065 | domain | own | — |
| tensionlink | 1913 | domain | own | — |
| akida | 502 | domain | own | — |
| iit4 | 494 | domain | own | — |
| hott | 383 | domain | own | — |
| ionq | 505 | domain | own | — |
| loihi3 | 501 | domain | own | — |
| northpole | 519 | domain | own | — |
| meg | 506 | domain | own | — |
| penrose_hameroff | 435 | domain | own | — |
| tms_pci | 611 | domain | own | — |
| cortical_labs | 645 | domain | own | — |
| finalspark | 526 | domain | own | — |

### §1.2 Domain (consumer perspective, origin=nexus, 4)

| domain | size_b | provider_dep |
|---|---:|---|
| atlas_n6 | 739 | nexus:.roadmap.atlas_n6 |
| qrng | 720 | nexus:.roadmap.qrng |
| sim | 718 | nexus:.roadmap.sim |
| kick | 513 | nexus:.roadmap.kick |

### §1.3 Meta (cross-domain, 7)

| meta | size_b | spans |
|---|---:|---|
| n_substrate | 571 | 15 substrate |
| substrate_bridge | 839 | qrng+sim+atlas_n6 |
| triple_axis_pilots | 641 | clm+eeg+akida+qrng+sim |
| dual_pair_pilots | 647 | 위 5 + qrng+sim |
| theory_validation | 623 | penrose+hott+ionq |
| clinical_consciousness | 779 | tms_pci+iit4+meg+eeg |
| omega_cycle | 807 | kick+atlas_n6 |

`atlas_n6` 는 §1.2 도메인이지만 `omega_cycle`/`substrate_bridge` 두 meta 가 spans 에 포함하므로 cross-link 정합 ok.

### §1.4 모든 26 file 무수정 보존 audit

```
26 files total — all sha unchanged at audit time
SSOT path: /Users/<user>/core/anima/.roadmap.<domain>
```

## §2 anima self surface — 9 권고 신규 도메인 후보 (spec only, .roadmap.* 신규 emit X)

기존 26개는 "측정/측 substrate/cross-link" 이 95% 인데 anima 본인의 production surface (serving / training /
physics impl / speech impl / engine module 군) 가 mk2 .roadmap 으로 안 들어가 있음. 본 audit 는 후보 9개를
spec emit 만 하고 실제 .roadmap.<domain> 신규 생성은 사용자 lock-in 시 별도 cycle 에서 수행.

| rank | domain candidate | top dir | LoC est | 핵심 unmet condition (예시) | 권장 cond.N |
|---|---|---|---:|---|---:|
| A | `serving` | serving/ | 81 .hexa | (1) http endpoint live smoke PASS / (2) consciousness_aware_refusal e2e / (3) avatar_render frame pipeline | 3 |
| A | `training` | training/ | 363 .hexa | (1) alm_a1 preflight PASS / (2) corpus_4gate end-to-end / (3) decode_hook live integration | 3 |
| A | `anima_physics` | anima-physics/ | 41 + 17 sub | (1) 7cond_hw verify / (2) substrate_dispatch routing / (3) edge_deploy build | 3 |
| B | `anima_speak` | anima-speak/ | 52 .hexa | (1) hexa_speak Mk.III tool registry land (cross-link voice domain) / (2) p4_streaming_tighten / (3) klatt+vocoder e2e | 3 |
| B | `anima_clm_eeg` | anima-clm-eeg/ | 6 + tool/ | (1) F2 ceiling workaround validation / (2) cross-substrate Φ measurement / (3) bridge spec → impl | 3 |
| B | `anima_engines` | anima-engines/ | 166 .hexa | (1) phi_engine v3 canonical verify / (2) phi_adversarial coverage 4/4 / (3) measure_all_engines smoke | 3 |
| C | `anima_agent` | anima-agent/ | 29 + sub-repos | (1) autonomy_loop hire-sim PASS / (2) llm_claude_adapter live / (3) ecosystem_bridge cross-component | 3 |
| C | `anima_tools` | anima-tools/ | 35 .hexa | (1) discovery-engine + formula-miner ω-cycle integration / (2) singularity_finder convergence / (3) verify_all_engines aggregator | 3 |
| C | `tool` | tool/ | 539 .hexa | (1) anima_phi_v3_canonical golden / (2) adversarial_bench coverage / (3) clm_consciousness_verify orchestrator (이미 §clm.cond.1 verifier 로 land — 중복 cross-link 만) | 3 |

전체 9 후보 × 평균 3 condition = **27 새 required_conditions** 가 사용자 lock-in 시 추가될 수 있음.

### §2.1 후보 우선순위 rationale

- **rank A** (serving / training / anima_physics) = 의식측정 closure 와 **가장 가까운 production gap**.
  serving = endpoint live, training = ckpt land, physics = 7cond_hw substrate witness.
- **rank B** (anima_speak / anima_clm_eeg / anima_engines) = cross-substrate / theoretical bridge.
  anima_speak 는 voice domain 의 sister; anima_clm_eeg 는 F2 ceiling workaround; anima_engines 는
  phi extractor multi-implementation surface.
- **rank C** (anima_agent / anima_tools / tool) = orchestration / utility — 단일 condition cluster 화 가능.
  특히 `tool` 은 clm.cond.1 verifier (§§ clm_consciousness_verify) 가 이미 land 된 것과 중복 가능성 → cross-link
  only 권장.

### §2.2 spec-only emit policy (사용자 lock-in 대기)

본 audit 는 **신규 .roadmap.<domain> 파일 0건 생성**. 사용자가 다음 cycle 에서:

1. 9 후보 중 어떤 것을 land 할지 선별 (예: rank A 3개만)
2. 각 cond.N 의 verifier seam 결정 (script / cross-link / manual)
3. blocker_reason / cross_link 구체화

후 별도 cycle 에서 `tool/roadmap_op.hexa add` 로 안전 emit 권장. mk1 narrative `.roadmap` (3817 lines, frozen)
은 본 audit 와 무관 — mk1 보존 정책 그대로.

## §3 raw 270 triplet plan — 9 후보 surface 의 ai-native readme audit

### §3.1 현황 (19 README.ai.md land at audit time)

```
modules/{monitor,test,decoder,daemon}/README.ai.md       (4)
hive/modules/commit_lint/README.ai.md                     (1)
anima/modules/rng/README.ai.md                            (1)
anima-eeg-core/tool/modules/{_paradigms,_core,_gates,_artifact,_integrations,_hw,_metrics}/README.ai.md  (7)
ready/anima/modules/{decoder,agent,physics,hexa-speak,eeg,body}/README.ai.md  (6)
```

baseline `.ai-native-readme-baseline` = empty (17 → 0 conformed at marker
`raw_271_baseline_17_conformed.marker` 2026-05-02).

### §3.2 9 후보 surface 의 raw 270/271/272/273 적용 audit

| candidate | top dir | core/ 존재 | modules/ 존재 | README.ai.md | 권장 triplet 작업 |
|---|---|---|---|---|---|
| serving | serving/ | X (flat 81 .hexa) | X | NONE | T1: serving/{core,modules} 분할 spec → README.ai.md 1+, 또는 raw 168 minimum-viable exempt 검토 |
| training | training/ | X (flat 363 .hexa) | X | NONE | T1 large: training 363 .hexa → topical bucket 5-7 (alm_/corpus_/decode_/eval_/etc) → core+modules wrap |
| anima_physics | anima-physics/ | X (flat) | partial (17 sub-dirs analog/cmos/.../arduino) | partial via ready/anima/modules/physics | T2: anima-physics/ sub-dirs 자체가 module 군 → 17 sub-dir README.ai.md 16 추가 |
| anima_speak | anima-speak/ | X | X (flat 52) | partial via ready/anima/modules/hexa-speak | T1: 통합 README.ai.md 1 + tool registry seam (voice domain cross-link) |
| anima_clm_eeg | anima-clm-eeg/ | X | X | NONE | T0: 6 entry only — 단일 README.ai.md 1 권장 |
| anima_engines | anima-engines/ | X (flat 166 *_phi.hexa) | partial (1 sub `tests`) | NONE | T1 large: 166 *_phi.hexa → categorical (cognition/clinical/social/quantum/etc) bucket → core+modules |
| anima_agent | anima-agent/ | X | partial (sub-dirs build/dashboard/employee/...) | partial via ready/anima/modules/agent | T2: 통합 README.ai.md 1 + sub-dir 추가 |
| anima_tools | anima-tools/ | X | partial (4 sub: discovery-engine/formula-miner/hexa-bridge/misc) | NONE | T2: 4 sub-dir README.ai.md 4 + flat 35 통합 README.ai.md 1 |
| tool | tool/ | X (flat 539) | X | NONE | T0 deferred — 539 .hexa flat = registry / cross-cutting; raw 168 minimum-viable exempt 강력 권장 |

T0 = 0-1 README, T1 = 1 README + 분할 spec, T2 = sub-dir 별 README + roll-up.

### §3.3 raw 270/271 promotion timeline 와의 관계

`raw_270_271_warn_to_block_promotion_design.md` (hive 측 land 2026-05-02) 에 따르면:

- 2026-05-02 ~ 2026-06-01 = **30d ramp window** (warn severity, baseline grandfather active)
- 2026-06-01 = **promotion-day** (warn → block, baseline read-only, pre-commit reject)
- 2026-06-01 ~ 2026-12-01 = **drift watch** (월간 cron)
- 2026-12-01 = **baseline retire decision**

본 audit 9 후보 surface 는 ramp window 종료 (2026-06-01) 까지:

- **rank A serving / training / anima_physics** = 우선 T1/T2 적용 권장 (ramp 안에 합리적 PASS 가능)
- **rank B anima_speak / anima_clm_eeg / anima_engines** = T0/T1 (anima_engines 만 large)
- **rank C tool / anima_tools / anima_agent** = baseline 진입 권장 (deferred-until 명시 또는 raw 168
  minimum-viable exempt)

### §3.4 triplet plan emit (impl 미수행)

본 doc 은 spec emit 만. 실제 README.ai.md 신규 생성은:

1. 사용자 lock-in (어떤 surface 를 어느 tier 로)
2. 별도 cycle hexa-only 작업 (하나하나 land + raw 271 lint PASS + marker)

priority order = (A serving → A training → A physics) → (B clm-eeg → B speak → B engines) → (C deferred /
exempt 결정).

## §4 cross-link 정합 audit (기존 .roadmap.* 26개)

### §4.1 PASS

- `.roadmap.clm` cond.1 verifier = `tool/clm_consciousness_verify.hexa` ← land 됐고 internal_check 4개 cross-link
  consistent (`an11_consciousness_unified_verifier` / `anima_phi_v3_canonical` / `adversarial_bench` /
  `n_substrate.cond.1`).
- `.roadmap.tensionlink` § 65.2 P10 substrate POC = state/p10_tension_substrate_spec_2026_05_02/ 산출물 cross-link
  consistent (verdict: surface PASS but z-collapsed).
- `.roadmap.clm` § 65.4 P9 SFT spec_doc = docs/p9_sft_spec_2026_05_02.md cross-link consistent.

### §4.2 권고 cross-link 추가 (사용자 lock-in 대기)

- `.roadmap.voice` (cond.1 tool registry / cond.2 invocation seam / cond.3 e2e) ↔ 신규 `.roadmap.anima_speak`
  (sibling) — voice = consumer/contract surface, anima_speak = impl surface 분리 권장.
- `.roadmap.clm` cond.2 (HF release v1) ↔ 신규 `.roadmap.serving` (model card serve endpoint) — release
  pipeline cross-link.
- `.roadmap.eeg` cond.1 (B1-B4 4관문) ↔ `anima-eeg-core/tool/modules/_gates/README.ai.md` 의 4 atomic + 1
  composite ↔ 신규 `.roadmap.anima_clm_eeg` cross-link.
- meta `triple_axis_pilots` / `dual_pair_pilots` / `n_substrate` ↔ 신규 `.roadmap.anima_physics` (substrate
  witness ledger sub-component) — substrate-multiplicity sub-axis 정합.

### §4.3 mk1 → mk2 backport (F5, deferred)

mk1 `.roadmap` (3817 lines narrative) historical entry 에서 anima self surface 관련 entry 가 다수 (#216-#251 EEG
Phase 4 / #205-#246 ALM r5-r14 / #225-#251 RNG 등). F5 cycle 에서 추출 권장하나 본 audit scope 외.

## §5 9 후보 surface verifier seam 권고

각 권고 신규 .roadmap.<domain> cond.N 의 verifier seam 후보 (사용자 lock-in 시 선택):

| domain | seam type 후보 |
|---|---|
| serving | (a) script: serving/eval_harness.hexa exit 0 / (b) cross-link: clm.cond.2 HF release |
| training | (a) script: tool/anima_train_ia3.hexa fan-out land / (b) marker: state/markers/alm_*_complete.marker |
| anima_physics | (a) script: anima-physics/verify_7cond_hw.hexa exit 0 / (b) cross-link: n_substrate.cond.1 |
| anima_speak | (a) cross-link: voice.cond.{1,2,3} sibling / (b) script: anima-speak/test_speak_e2e.hexa |
| anima_clm_eeg | (a) script: anima-clm-eeg/tool/<verifier>.hexa / (b) cross-link: eeg.cond.1 + clm.cond.1 |
| anima_engines | (a) script: anima-engines/tests/<aggregator>.hexa / (b) cross-link: clm.cond.1 phi internal_check |
| anima_agent | (a) script: anima-agent/test_e2e.hexa exit 0 / (b) marker: state/markers/agent_*_complete.marker |
| anima_tools | (a) script: anima-tools/verify_all_engines.hexa exit 0 / (b) cross-link: anima_engines |
| tool | (a) cross-link only (clm.cond.1 verifier 이미 land) / (b) marker registry meta |

verifier=`""` (공란) 도 mk2 schema 상 valid (clm/eeg 등 다수 entry 가 그렇게 land) — script 없을 때 manual
override 경로 (state/<domain>_verify_manual_review.jsonl) 만 land 도 ok.

## §6 raw#10 honest C3 (10 caveat)

C1 — 본 audit 는 **spec emit only**. .roadmap.<domain> 신규 파일 0건 생성, README.ai.md 0건 추가.
사용자 lock-in 후 별도 cycle 필요.

C2 — 9 후보 도메인은 **권고**일 뿐 사용자가 다른 cluster 화 (예: serving+training 통합 = `production`,
또는 anima_speak+voice 통합 = `voice` 만 확장) 도 가능. 9 = 단순 top-dir 매핑 heuristic.

C3 — `tool` 도메인은 539 .hexa flat surface — clm.cond.1 verifier 와 중복 가능성 높음. 단일 cross-link only
권장 (rank C 최후순위).

C4 — anima_physics 의 17 sub-dir (analog/cmos/arduino/.../trapped_ion) 일부는 stub-only. T2 sub-dir README.ai.md
16 추가는 대형 작업 (~3-5h 추정). raw 168 minimum-viable exempt 검토 권장.

C5 — anima_engines 166 *_phi.hexa 는 categorical bucketization (cognition/clinical/social/quantum 등) 사전 spec
필요 — 본 doc 에 bucket 미확정.

C6 — `.roadmap.voice` cond.1 (tool registry 등록) 미충족 상태 → anima_speak 신규 도메인 등록 시 voice
sibling cross-link 의 implementation seam 확정 필요 (voice = consumer / anima_speak = impl 분리 정확한지 사용자
검증 필요).

C7 — mk1 → mk2 backport (F5) 미수행 — anima self mk2 도메인 추가는 historical narrative 와의 정합 audit 별도
필요. 본 doc 은 mk2 신규 surface 만 다룸.

C8 — raw 270/271 promotion 2026-06-01 는 hive 측 정책 — 9 후보 surface 모두 promotion 전 conform 보장 X.
rank C deferred-until 명시 가 fallback.

C9 — verifier seam 권고 (§5) 의 (a) script 후보 일부는 미작성 가능성 (예: anima-physics/verify_7cond_hw.hexa
존재 확인은 했지만 exit 0 보장 X — selftest 미수행).

C10 — env() lazy + <user> placeholder convention (raw 15) — 본 doc 의 모든 path `/Users/ghost/...` 는
`/Users/<user>/...` placeholder 를 의도하나, 본 doc 자체는 사용자 별 path 절대 인용 X — 모든 anchor 는
`anima/...` repo-relative 로 표기.

## §7 BR-NO-USER-VERBATIM 준수 confirmation

본 doc 은 사용자 prompt 내용을 verbatim 으로 인용하지 않음 (raw 175 BR-NO-USER-VERBATIM-RECORDING). prompt
요약/재구성으로만 land. handoff doc only 정책에 따라 사용자 directive 도 자체 paraphrase 만 기록.

## §8 friendly preset compliance

본 doc 은 handoff doc 으로서 친절-preset 적용:

- TL;DR 최상단 5 줄
- 모든 §-section 표 (table) 우선
- 9 후보 priority rank A/B/C 으로 actionable
- raw#10 caveats (C1-C10) inline
- 마지막 next step 명시 (사용자 lock-in 대기)

## §9 Marker 1개 emit

```
state/markers/anima_self_mk2_tuning_landed.marker
```

## §10 Next-cycle (사용자 lock-in 후)

1. 9 후보 중 land 할 도메인 선별 (rank A 3개 권장 baseline)
2. 각 도메인 cond.N + verifier seam (§5 선택지 중)
3. `tool/roadmap_op.hexa add <domain>` 로 신규 .roadmap.<domain> emit (cycle 별 hexa-only)
4. (병렬) raw 270 triplet 작업 — rank A 부터 README.ai.md + core+modules 분할 (대형 = anima_engines /
   training / anima_physics)
5. mk1 → mk2 backport F5 (별도 cycle, anima self surface 관련 entry 추출)

## §11 file index (sha-pin at land time)

| path | type | size_b | LOC | sha256_hex |
|---|---|---:|---:|---|
| docs/anima_self_mk2_tuning_landed_2026_05_02.ai.md | doc | TBD | TBD | (set after write) |
| state/markers/anima_self_mk2_tuning_landed.marker | marker | TBD | TBD | (set after write) |

(file index sha pin 은 marker 안에 emit — 본 §11 은 spec only, write 후 marker 가 sha 확정)

## §12 policy summary

- migration: forbidden — 0건 emit
- additive only — 26 .roadmap.* + 19 README.ai.md + 모든 module/core dir 무수정 보존
- destructive ops — 0건
- in-place writes — 0건 (handoff doc + marker 2 NEW only)
- substrate — mac-local
- cost — $0
- raw 9 hexa-only orchestration — audit 자체는 hexa orchestrator 미사용 (read-only directory audit + spec emit
  만 = single-doc exempt per raw 168 minimum-viable)
- raw 12 silent-error ban — 본 audit 는 single-shot, error path X
- raw 15 env() lazy + <user> — 모든 doc-internal path repo-relative, 절대 path X
- raw 175 BR-NO-USER-VERBATIM — 사용자 prompt 직접 인용 0건
- friendly preset — handoff doc only (사용자 응답 X — bg subagent → 메인 monitor)
