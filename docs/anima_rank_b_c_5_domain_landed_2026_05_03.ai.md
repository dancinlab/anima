---
schema: anima/docs/anima_rank_b_c_5_domain_landed/ai-native/1
last_updated: 2026-05-03
ssot:
  marker: state/markers/anima_rank_b_c_5_domain_landed.marker
  predecessor_handoff: docs/anima_rank_a_3_domain_landed_2026_05_03.ai.md
  predecessor_marker: state/markers/anima_rank_a_3_domain_landed.marker
  roadmap_dir_pattern: <repo>/.roadmap.<domain>
status: RANK_B_C_5_DOMAIN_LANDED
related_raws:
  - raw 9    # hexa-only orchestration (additive land, single-doc pattern raw 168 minimum-viable exempt)
  - raw 10   # honest C3 caveats inline
  - raw 11   # snake_case
  - raw 15   # env() lazy + <user> placeholder
  - raw 168  # minimum-viable exempt
  - raw 175  # BR-NO-USER-VERBATIM
  - raw 270  # ai-native readme triplet (referenced for follow-up)
  - raw 271  # core+module pattern
  - raw 272  # lint extension
  - raw 273  # hierarchy connection direction
  - raw 12   # silent-error ban
preserved_unchanged:
  - all 44 existing .roadmap.* (mk2) files (sha unchanged including rank A 3 from previous cycle, full pre-cycle disk count audit)
  - all 19 existing README.ai.md files
  - mk1 .roadmap (3817 lines narrative)
  - all module dirs under anima/{core,modules}, anima-eeg/, anima-clm-eeg/, anima-physics/, anima-voice/, anima-engines/, anima-agent/, anima-agent-core/, anima-agent-channels/, anima-agent-providers/, serving/, training/, tool/
  - all configs
policy:
  migration: forbidden
  changes: additive_only
  in_place_writes: zero
  destructive_ops: zero
  cost_usd: 0
  substrate: mac-local
  br_no_user_verbatim: true
  friendly_preset: handoff_doc_only
  rank_b_correction: "rank B = 2 (anima_clm_eeg + anima_engines); anima_voice absorbed into .roadmap.voice per user directive"
---

# anima rank B + C 5 domain — anima_clm_eeg / anima_engines / anima_agent / anima_tools / tool 신규 .roadmap 5개 land

## TL;DR (5줄)

- **선행 BG-AN handoff doc** 9 candidate 중 BG-AN-A 측 rank A 3 (serving / training / anima_physics) 이미 land. 본 cycle = rank B 2 (사용자 directive 정정: anima_voice → .roadmap.voice 흡수, rank B = anima_clm_eeg + anima_engines) + rank C 3 (anima_agent + anima_tools + tool) = **5 도메인 신규 land**.
- 각 .roadmap = JSONL header (1 line) + 3 cond (mixed status met/partial/unmet) + 2 blockers, peer perspective, mk2 schema 준수.
- **status mix**: 5 file × 3 cond = 15 cond 통합 mix → met=1 (anima_engines.cond.1, training.cond.2 met 패턴 동일 disk artifact post-hoc proof) + partial=3 (anima_clm_eeg.1 + anima_agent.1 + tool.1) + unmet=11.
- **blockers 10 total**: 5 structural (363 .hexa flat / 17 sub-dir / hardcoded path / 539 entry flat / sub-tree migration) + 3 upstream (eeg cond.1 / w1 archive decision / clm verdict consumer) + 2 decision (anima/tool/ migration / engine_a/g axis 분리).
- 마이그레이션 0건, in-place writes 0건, destructive 0건, $0 mac-local. 44 기존 .roadmap.* (rank A 3 포함) + 19 README.ai.md 전부 무수정.

## §1 신규 land 산출물 5종 inventory

| domain | rank | path | size_b | sha256 | n_cond | status mix | n_blockers |
|---|---|---|---:|---|---:|---|---:|
| anima_clm_eeg | B | `.roadmap.anima_clm_eeg` | 7218 | `1974444c1b3ea54d594f545f2ad81d2bd3d031220034b2c7b1f461cc11b00026` | 3 | partial+unmet+unmet | 2 |
| anima_engines | B | `.roadmap.anima_engines` | 7958 | `12ba6115cdddbd7d51d3c0d9f4005d68be4604f44e05cb2f51f148b77713cfe0` | 3 | **met**+unmet+unmet | 2 |
| anima_agent | C | `.roadmap.anima_agent` | 7939 | `f38ed4f9eab8f758cfec192578fd61a4710fd1b7213e16b645772751ed9813b9` | 3 | partial+unmet+unmet | 2 |
| anima_tools | C | `.roadmap.anima_tools` | 7802 | `988bbfce9dbc2c21705d0fb7045b8ae4f488c45837219ddb57b7621508660c49` | 3 | unmet+unmet+unmet | 2 |
| tool | C | `.roadmap.tool` | 8317 | `5089699a0c2aeef12436c639bea093bd770be2103c24cfae8472892f853064f7` | 3 | partial+unmet+unmet | 2 |

JSON parse audit: 5/5 PASS (python3 json.load 성공, mk2 schema 준수 — kind=domain, perspective=peer, mk=2, status=active, name 일치).

## §2 도메인별 cond 요약

### §2.1 anima_clm_eeg (rank B, peer, EEG-CLM cross-substrate)

| cond | 요약 | status | verifier seam | 핵심 evidence |
|---|---|---|---|---|
| anima_clm_eeg.cond.1 | 5-metric harness pre-register PASS | **partial** | script `anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa` (5 sub-metric) | berger + gamma_theta + hjorth_real + lz76_real + pe_real 5 metric land + pre_register_v1 + v1_1 + 16ch synthetic fixture + clm_eeg_v1_1_patch_complete marker |
| anima_clm_eeg.cond.2 | DALI/SLI v3 input-mode 7-bb cross-link | unmet | script `clm_eeg_p1_lz_pre_register.hexa` (cross-link state/dali_sli_v3 + sister .roadmap.dual_pair_pilots) | dali_sli_v3_input_mode + v2_redesign + weighted_vote 3 산출물 + 4 landing doc + 2 marker, project memory #42 v3 mode coverage 2/3 |
| anima_clm_eeg.cond.3 | Mk.XII d-day cohort prep | unmet | script `mk_xii_hard_pass_composite.hexa` (4-cascade chain) | 4 entry land (preflight + d_day_simulated + eeg_corroboration + hard_pass_composite v1+v2) + 4 산출물 + d_day_session_2026_04_28 dir + handoff_20260427 marker |

blockers: (1) **upstream** = `.roadmap.eeg cond.1` (B1-B4 4관문) 미PASS — real 16ch EEG arrival blocker, synthetic only. (2) **structural** = 7-bb tally aggregator + 4-cascade composite live runner script 미land.

### §2.2 anima_engines (rank B, peer, 4-substrate registry + tension + 4-gen crystal)

| cond | 요약 | status | verifier seam | 핵심 evidence |
|---|---|---|---|---|
| anima_engines.cond.1 | engines.hexa registry post-hoc proof | **met** | disk_artifact `anima-engines/engines.hexa` (4 substrate registry land, bench_v2 측정 coefficient) | engines.hexa + 4 sibling engine entry (osc_laser/quantum/photonic/memristor) + tests/test_engine_bridge + 4 Law cross-link header docstring (Law 1+22+29+AN7), training.cond.2 met 동일 disk-artifact post-hoc 패턴 |
| anima_engines.cond.2 | tension calculator 5-variant cross-link | unmet | script `tool/alm_tension_field_bridge.hexa` (sister .roadmap.tensionlink + tlm_tension_lm + n51_alm_tension) | 5 tension_link variant (step / quantum_rho / vs_backprop_bench / causal / second_order) + 2 test + 2 experiment + 3 sister .roadmap peer 존재 |
| anima_engines.cond.3 | 4-gen crystallize tool integration | unmet | script `tool/edu_cell_4gen_crystallize.hexa` (H-CX-523 hypothesis cross-link) | tool entry + API doc + H-CX-523 time-crystal hypothesis doc + ready/ mirrored copy |

blockers: (1) **structural** = engines.hexa ENG_CONST_PATH hardcoded `/Users/ghost/Dev/anima/...` raw 15 env() lazy 위반. (2) **decision** = engine_a / engine_g 추상 axis 미세분 (header goal 명시 but registry entry 부재).

### §2.3 anima_agent (rank C, peer, agent loop 4-layer)

| cond | 요약 | status | verifier seam | 핵심 evidence |
|---|---|---|---|---|
| anima_agent.cond.1 | agent loop boot + Claude session | **partial** | script `anima-agent/anima_agent.hexa` (3 entry alternative, claude_provider chain) | 3 entry (anima_agent + core + full) + 4 provider + 4 channel + 6 test + agent.hexa registry + llm_claude_adapter + scope doc |
| anima_agent.cond.2 | agent_tools + tool_policy + unified_registry 3-layer | unmet | script `anima-agent-core/unified_registry.hexa` (sibling byte-equivalence) | core 6 entry (agent_sdk/agent_tools/tool_policy/unified_registry/run/code_guardian) + sibling hexa/agent_tools.hexa + docs/modules/agent_tools.md |
| anima_agent.cond.3 | memory + cron loop 4-layer integration | unmet | script `anima-agent/autonomy_loop.hexa` (sister .roadmap.w1_anima_as_substrate cross-link) | 3 autonomy entry + 2 .growth cron + 3 .growth audit + memory/ index + MEMORY.md 84KB (limit 24.4KB 3.4× 초과 honest) |

blockers: (1) **structural** = 3 entry + sibling pair canonical 미확정, ownership ambiguity. (2) **upstream** = sister `.roadmap.w1_anima_as_substrate` Phase 5 ARTIFACT_PERMANENT_DOWNGRADE 후 residual cron decision 미land (w1.blk.1 share).

### §2.4 anima_tools (rank C, peer, anima-domain tool ecosystem audit)

| cond | 요약 | status | verifier seam | 핵심 evidence |
|---|---|---|---|---|
| anima_tools.cond.1 | anima-prefix 189 entry inventory + ownership audit | unmet | script `tool/anima_tool_inventory_audit.hexa` (target_globs + anima/tool/ EMPTY 결정) | anima/tool/ EMPTY 0 entry confirm + 539 top-level entry 중 anima_*.hexa 189 entry + alm_/an11_/clm_/cmt_/cyborg_ family 다수 |
| anima_tools.cond.2 | sub-system tool family registration | unmet | script `tool/anima_roadmap_v11_register.hexa` (family_glob_chain × sister .roadmap) | 12 roadmap-meta tool + anima_nexus_roadmaps_consistency_auditor + anima_roadmap_lint 3 consistency tool |
| anima_tools.cond.3 | anima_session_handoff + memory + worktrees 3-class meta | unmet | script `tool/anima_memory_broken_refs_remediation.hexa` (8 meta-tool chain) | 2 session_handoff + 4 memory + 1 worktrees + 1 git_commit_chain auditor + state/worktrees_agent_inventory_auditor.json 산출물 |

blockers: (1) **decision** = anima/tool/ EMPTY 결정 — sub-tree migration vs top-level 유지 user lock-in pending. (2) **structural** = family-to-roadmap mapping spec 미land.

### §2.5 tool (rank C, peer, generic tool meta cross-cut)

| cond | 요약 | status | verifier seam | 핵심 evidence |
|---|---|---|---|---|
| tool.cond.1 | roadmap-meta 12 tool + idempotency PASS | **partial** | script `tool/roadmap_op.hexa` (12 meta chain + 3 sister) | roadmap_op + compile + render + html_render + lint + mistake_auto_fix + auto_reflect + diff_viz + integrity_guard + live_daemon + live_update + 83_auto_mark 12 entry + 3 anima sister meta |
| tool.cond.2 | lint + auto_changelog + repo_resolver 3-class generic meta | unmet | script `tool/lint_autofix.hexa` (6 generic meta chain) | lint_autofix + lint_rule_pack + auto_changelog + 3 underscore-prefix internal meta + 3 .py exempt 잔존 (project memory) |
| tool.cond.3 | raw 270/271 triplet + raw 168 minimum-viable exempt 정책 | unmet | script `tool/anima_nexus_roadmaps_consistency_auditor.hexa` (sister anima_tools.cond.1 share) | sister .roadmap.anima_tools land (본 cycle) + raw 270/271/168 정책 cross-link |

blockers: (1) **structural** = 539 entry flat surface, 6 topical bucket spec 미land (raw 270/271 T1_large). (2) **structural** = roadmap_op add 와 직접 Write idempotent 정합 audit 미수행 (predecessor handoff §9.5 deferred 그대로).

## §3 cross-link 정합 audit (기존 29 .roadmap.* 무수정)

### §3.1 sister-link 신규 emit (additive only)

- **anima_clm_eeg** ↔ `eeg` (cond.1 4관문 upstream) + `clm` (verdict consumer) + `slm_speech_eeg_lm` (3-modal sibling) + meta `dual_pair_pilots / triple_axis_pilots / tensionlink`.
- **anima_engines** ↔ `clm / training / anima_physics` (sister) + meta `tensionlink / tlm_tension_lm / n51_alm_tension / substrate_bridge / p10_substrate_poc`.
- **anima_agent** ↔ `w1_anima_as_substrate` (Phase 5 ARTIFACT 후 audit-only mode share) + `clm / serving` + meta `g1_g5_chat_substrate / omega_cycle`.
- **anima_tools** ↔ `tool` (ownership boundary 분리 sister) + 5 도메인 sister cross-link.
- **tool** ↔ `anima_tools` (sister) + `clm / training / serving` (cross-link only, condition 중복 X).

### §3.2 ownership 경계 명확 분리

**anima_tools** = anima-domain tool surface (anima_/alm_/an11_/clm_/cmt_/cyborg_ etc) | **tool** = generic meta cross-cut (roadmap_*/lint_*/auto_changelog/_omega_stdlib_*/_roadmap_repo_resolver/api_surface_extract/aot_cache_audit/artifact_*/auto_evolution_loop). 두 도메인 condition 중복 0건.

### §3.3 기존 44 file 무수정 audit

- 41 pre-rank-A .roadmap.* + 3 rank A (serving/training/anima_physics) = 44 파일 sha unchanged at land time (full disk inventory audit).
- mk1 narrative .roadmap (3817 lines, frozen) 무관 (mk1 보존 정책 그대로).
- 19 README.ai.md 전부 무수정 (raw 270 triplet 후속 cycle deferred).

## §4 정책 준수 (raw compliance)

| raw | 적용 | 본 land 적용 방식 |
|---|---|---|
| raw 9 | hexa-only | additive land 자체는 hexa orchestrator 미사용 (5 .roadmap + 1 doc + 1 marker = single-doc pattern, raw 168 minimum-viable exempt) |
| raw 10 | honest C3 | 본 §6 inline 6 caveat |
| raw 11 | snake_case | doc + marker + 5 .roadmap 내 모든 id snake_case (anima_clm_eeg.cond.N / anima_engines.cond.N / anima_agent.cond.N / anima_tools.cond.N / tool.cond.N) |
| raw 12 | silent-error ban | single-shot, error path X |
| raw 15 | env() lazy + <user> | 본 doc 의 모든 anchor repo-relative; 절대 path quote 만 marker sha-pin transparency 용 (predecessor 패턴 정합) |
| raw 168 | minimum-viable exempt | single-doc pattern 5-file land 적용 |
| raw 175 | BR-NO-USER-VERBATIM | 사용자 prompt 직접 인용 0건, paraphrase only |
| raw 270 | triplet | 본 land 는 .roadmap 만, README.ai.md 추가는 별도 cycle (각 .roadmap cross_link.triplet_pending 명시) |
| raw 271 | core+modules | 분할 미수행, 별도 cycle deferred (각 .roadmap blockers structural T1/T1_large/T2 명시) |
| raw 272 | lint extension | 영향 없음 (additive only) |
| raw 273 | hierarchy direction | rank B 정정 (anima_voice → .roadmap.voice 흡수, rank B=2) + rank C 3개 모두 land, 9 candidate 중 8 처리 (anima_voice = absorbed) |

## §5 BR-NO-USER-VERBATIM 준수 confirmation

본 doc + 5 .roadmap 모두 사용자 prompt 내용을 verbatim 으로 인용하지 않음 (raw 175). prompt 요약/재구성으로만 land. handoff doc + .roadmap 정책에 따라 사용자 directive (rank B 정정 + anima/tool/* 해석 + ownership 경계) 도 paraphrase 만 기록.

## §6 raw#10 honest C3 (6 caveat)

C1 — 본 land 는 **5 .roadmap.<domain> + 1 handoff doc + 1 marker = 7 NEW file** 만 emit. README.ai.md 추가 0건, 기존 44 .roadmap (41 pre-rank-A + rank A 3) + 19 README.ai.md 전부 무수정. core/modules 분할 0건 — 모두 별도 cycle deferred.

C2 — verifier seam 의 (a) script 후보 일부는 exit-0 selftest 미수행. 예: `anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa` 16ch synthetic only / `anima-engines/engines.hexa` ENG_CONST_PATH hardcoded blocker / `anima-agent/anima_agent.hexa` Claude API key + cap dependency / `tool/roadmap_op.hexa` 본 land 가 직접 Write 사용 (roadmap_op 미경유, predecessor handoff §9.5 deferred 그대로).

C3 — `anima_engines.cond.1 = met` 의 evidence 는 disk artifact 존재 + 4 sibling engine + bench_v2 measured coefficient 기반 (training.cond.2 met 동일 패턴). 4 substrate compile + selftest exit-0 fresh re-run 미수행 (ENG_CONST_PATH hardcoded blocker 해소 후속 cycle 의존). disk 증거 = **post-hoc proof**, fresh PASS 와 별개.

C4 — `anima_agent.cond.3` MEMORY.md 84KB 비대 (limit 24.4KB 3.4× 초과) honest 명시. cleanup cycle (anima_memory_* tool chain trigger condition) 별도 — 본 land 는 cleanup 미수행, status 그대로 유지.

C5 — `anima_tools.cond.1` anima/tool/ EMPTY 결정 = sub-tree migration vs top-level 유지 user lock-in pending (blk.1 decision). 사용자 directive header 'anima/tool/*' 명시 paraphrase = top-level tool/ anima-domain entry 의미로 해석 (anima/tool/ EMPTY 그대로 유지 권장 = raw 270/271 sister 정합). 정확한 의도 user lock-in 시 정정 가능.

C6 — `anima_engines.blk.2` engine_a / engine_g 추상 axis 미세분 = 사용자 directive header 'engine_a + engine_g' 명시 vs anima-engines/ 실제 entry 부재 (engines.hexa 전체 1 entry registry, 4 substrate canonical = osc_laser/quantum/photonic/memristor). a/g 분류 axis 정의는 unlock_keyword decision 별도. 본 land 는 engines.hexa SSOT 그대로 honest 기록.

## §7 friendly preset compliance (handoff doc 친절-preset)

- TL;DR 최상단 5줄
- 모든 §-section 표 (table) 우선
- 5 도메인 status mix 명시 (met/partial/unmet count, 5 file × 3 cond = 15 cond 통합)
- raw#10 caveats (C1-C6) inline
- 마지막 next-cycle 명시 (raw 270 triplet 후속 + verifier exit-0 selftest + decision unlock_keyword 6종)

## §8 marker emit

```
state/markers/anima_rank_b_c_5_domain_landed.marker
```

## §9 next-cycle (사용자 lock-in 후)

1. **raw 270/271 triplet 후속** (병렬) — rank B/C 5 surface 부터 README.ai.md + core+modules 분할. anima_engines (T1_large 166 entry) / anima_agent (T1_large 4 sub-package) / tool (T1_large 539 entry) 가 가장 큰 작업. anima_clm_eeg (T2 30 tool + 20 doc) 중간. anima_tools (sister 와 paired) T1_large.
2. **verifier seam exit-0 selftest** (별도 cycle) — 5 도메인 15 cond 의 실제 exit-0 측정. 우선순위: anima_engines.cond.1 (met 강화 fresh selftest, ENG_CONST_PATH 해소 후) → anima_clm_eeg.cond.1 (16ch synthetic harness_smoke first) → tool.cond.1 (roadmap_op idempotent).
3. **upstream blocker 해소 wait** — `.roadmap.eeg cond.1` (B1-B4 4관문 PASS) + `.roadmap.w1_anima_as_substrate` residual cron decision 2 unlock_keyword.
4. **decision unlock_keyword 6종** — (a) `OK W1 ARCHIVE` OR `OK W1 RESIDUAL_KEEP` (anima_agent.blk.2 + w1.blk.1 share) / (b) `OK ENGINES A/G_AXIS_DEFINE` (anima_engines.blk.2) / (c) `OK ANIMA_TOOLS TOP_LEVEL_KEEP` OR `OK ANIMA_TOOLS MIGRATION` (anima_tools.blk.1).
5. **anima_voice rank B 정정 후속** — `.roadmap.voice` 흡수 검증 cycle (사용자 directive 정정 honest 기록, voice domain cond.1/2/3 와 anima_voice 측 spec 정합 audit 별도).

## §10 file index (sha-pin at land time)

| path | type | size_b | sha256_hex |
|---|---|---:|---|
| .roadmap.anima_clm_eeg | roadmap | 7218 | 1974444c1b3ea54d594f545f2ad81d2bd3d031220034b2c7b1f461cc11b00026 |
| .roadmap.anima_engines | roadmap | 7958 | 12ba6115cdddbd7d51d3c0d9f4005d68be4604f44e05cb2f51f148b77713cfe0 |
| .roadmap.anima_agent | roadmap | 7939 | f38ed4f9eab8f758cfec192578fd61a4710fd1b7213e16b645772751ed9813b9 |
| .roadmap.anima_tools | roadmap | 7802 | 988bbfce9dbc2c21705d0fb7045b8ae4f488c45837219ddb57b7621508660c49 |
| .roadmap.tool | roadmap | 8317 | 5089699a0c2aeef12436c639bea093bd770be2103c24cfae8472892f853064f7 |
| docs/anima_rank_b_c_5_domain_landed_2026_05_03.ai.md | doc | TBD | (set after write) |
| state/markers/anima_rank_b_c_5_domain_landed.marker | marker | TBD | (set after write) |

(doc + marker sha pin 은 marker 안에 emit — 본 §10 은 spec only, write 후 marker 가 sha 확정)

## §11 policy summary

- migration: forbidden — 0건 emit
- additive only — 44 .roadmap.* + 19 README.ai.md + 모든 module/core dir 무수정 보존
- destructive ops — 0건
- in-place writes — 0건 (5 roadmap + handoff doc + marker = 7 NEW only)
- substrate — mac-local
- cost — $0
- raw 9 hexa-only — single-doc pattern raw 168 minimum-viable exempt
- raw 10 silent-error ban — single-shot, error path X
- raw 15 env() lazy + <user> — 본문 anchor repo-relative
- raw 175 BR-NO-USER-VERBATIM — 사용자 prompt 직접 인용 0건
- friendly preset — handoff doc only (사용자 응답 X — bg subagent → 메인 monitor)
- rank B correction — anima_voice absorbed into .roadmap.voice (사용자 directive paraphrase honest 반영)
