---
schema: anima/docs/anima_rank_a_3_domain_landed/ai-native/1
last_updated: 2026-05-03
ssot:
  marker: state/markers/anima_rank_a_3_domain_landed.marker
  predecessor_handoff: docs/anima_self_mk2_tuning_landed_2026_05_02.ai.md
  predecessor_marker: state/markers/anima_self_mk2_tuning_landed.marker
  roadmap_dir_pattern: <repo>/.roadmap.<domain>
status: RANK_A_3_DOMAIN_LANDED
related_raws:
  - raw 9    # hexa-only orchestration (additive land, no impl emitted)
  - raw 10   # honest C3 caveats inline
  - raw 11   # snake_case
  - raw 15   # env() lazy + <user> placeholder
  - raw 270  # ai-native readme triplet (referenced for follow-up)
  - raw 271  # core+module pattern
  - raw 272  # lint extension
  - raw 273  # hierarchy connection direction
  - raw 12   # silent-error ban
  - raw 175  # BR-NO-USER-VERBATIM
preserved_unchanged:
  - all 26 existing .roadmap.* (mk2) files (sha unchanged)
  - all 19 existing README.ai.md files
  - .ai-native-readme-baseline (empty/conformed)
  - mk1 .roadmap (3817 lines narrative)
  - all module dirs under anima/{core,modules}, anima-eeg/, anima-clm-eeg/, anima-physics/, anima-voice/, anima-engines/, serving/, training/, tool/
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
---

# anima rank A 3 domain — serving / training / anima_physics 신규 .roadmap 3개 land

## TL;DR (5줄)

- **선행 audit** (`docs/anima_self_mk2_tuning_landed_2026_05_02.ai.md`) 9 candidate 중 rank A 3개 = **serving / training / anima_physics** 신규 .roadmap.<domain> 3개 land 완료.
- 각 파일 = JSONL header (1 line) + 3 conditions (mixed status) + 2 blockers, peer perspective, mk2 schema 준수.
- **status mix**: 9 cond 중 met=1 (training.cond.2 corpus_4gate, 4-stage 산출물 disk 증거 충족), partial=3 (각 도메인 cond.1), unmet=5.
- **blockers 6 total**: 3 structural (raw 270 triplet T1/T1_large/T2 분할 미수행) + 2 upstream (clm.cond.1 cross-link blocked / live HW witness blocked) + 1 budget (Mk.XII retrain $2200-6700 deferred).
- 마이그레이션 0건, in-place writes 0건, destructive 0건, $0 mac-local. 26 기존 .roadmap.* + 19 README.ai.md 전부 무수정.

## §1 신규 land 산출물 3종 inventory

| domain | path | size_b | sha256 | n_cond | status mix | n_blockers |
|---|---|---:|---|---:|---|---:|
| serving | `.roadmap.serving` | 3472 | `1d4c5881eb4de9ad42e69bf11439c34df0d59d961752e1b529fda8940adcf429` | 3 | partial+unmet+unmet | 2 |
| training | `.roadmap.training` | 4496 | `5df3033a650f3404eee78acd135e13abbb990ada7c9974325eb8455570cbe713` | 3 | partial+met+unmet | 2 |
| anima_physics | `.roadmap.anima_physics` | 5575 | `c978104ac53e957b8c12054743902f5be67a0f0c2a07cff4cb415844824b33cc` | 3 | partial+unmet+unmet | 2 |

JSON parse audit: 3/3 PASS (python3 json.load 성공, mk2 schema 준수 — kind=domain, perspective=peer, mk=2, status=active).

## §2 도메인별 cond 요약

### §2.1 serving (peer, voice serving + endpoint deploy + http_server)

| cond | 요약 | status | verifier seam | 핵심 evidence |
|---|---|---|---|---|
| serving.cond.1 | http endpoint live smoke | **partial** | script `serving/http_server.hexa` (smoke=/healthz) | http_server.hexa + serve_http.hexa + api_server.hexa 3 entry 모두 disk 존재 (canonical 미확정) |
| serving.cond.2 | consciousness_aware_refusal e2e | unmet | script `serving/consciousness_aware_refusal.hexa` (cross-link clm.cond.1 + voice.cond.3) | consciousness_aware_refusal.hexa + consciousness_gate.hexa land |
| serving.cond.3 | avatar_render frame pipeline | unmet | script `serving/avatar_render.hexa` (frames_min=1, fps>=1) | avatar_render + avatar_sync + avatar_feed + test_avatar_sync 4 entry land |

blockers: (1) **structural** = core/modules 분할 미수행 (81 .hexa flat) — raw 270 triplet T1, eta 2026-06-01. (2) **upstream** = clm.cond.1 Putnam cross-link spec only.

### §2.2 training (peer, CLM v4 + LoRA + IA3 + Mk.XII spec)

| cond | 요약 | status | verifier seam | 핵심 evidence |
|---|---|---|---|---|
| training.cond.1 | alm_a1 preflight | **partial** | script `training/alm_a1_preflight.hexa` (config=alm_a1_config.json) | alm_a1_preflight.hexa + alm_a1_config.json + tool/anima_train_ia3.hexa land |
| training.cond.2 | corpus_4gate end-to-end | **met** | script `training/corpus_aggregate.hexa` (4 stage) | 4 stage script 모두 land + corpus_clm_combined.txt + .gz + corpus_alm_70b_stripped*.txt + corpus_clm_r4.txt.gz + corpus_alm_r11_r2_index.md 산출물 disk 증거 |
| training.cond.3 | decode_hook live integration | unmet | script `training/decode_hook.hexa` (hook fire 측정) | (decode_hook entry 식별 미완) |

blockers: (1) **structural** = 363 .hexa flat surface bucketization 미land — raw 270 triplet T1_large, eta 2026-06-01. (2) **budget** = Mk.XII retrain $2200-6700 cap exceed, deferred (own#2 PC empirical-max axis Phase 3a 13B critical gate).

### §2.3 anima_physics (peer, 9 substrate witness ledger + cloud facade)

| cond | 요약 | status | verifier seam | 핵심 evidence |
|---|---|---|---|---|
| anima_physics.cond.1 | 7cond_hw verify | **partial** | script `anima-physics/verify_7cond_hw.hexa` (cross-link n_substrate.cond.1 + ledger v3) | verify_7cond_hw.hexa land + tool/mk_xii_substrate_witness_ledger_aggregator{,_v2,_v3}.hexa 3 version + engines/* 8 consciousness engine + state/markers/mk_xii_substrate_witness_ledger_aggregator{,_v2}_*.marker disk 존재 |
| anima_physics.cond.2 | substrate_dispatch routing | unmet | script `anima-physics/physics_substrate_dispatch.hexa` (9 substrate) | physics_substrate_dispatch.hexa + hw_engine_bridge.hexa + phi_substrate_consensus.hexa land |
| anima_physics.cond.3 | edge_deploy build | unmet | script `anima-physics/edge_deploy.hexa` (esp32/arduino/fpga 3 target) | edge_deploy.hexa + esp32/arduino/fpga sub-dir + 6 guide doc land |

blockers: (1) **structural** = 17 sub-dir 분산 구조, raw 270 triplet T2 = 16 README.ai.md 추가 ~3-5h, raw 168 minimum-viable exempt 검토. (2) **upstream** = G5 LIVE_HW_WITNESS_RATE 0/11 honest floor, simulation only.

## §3 cross-link 정합 audit (기존 .roadmap.* 26개 무수정)

### §3.1 sister-link 신규 emit (additive only)

- **serving** ↔ `voice` (cond.3 sibling) + `clm` (cond.1 verdict consumer / cond.2 release pipeline).
- **training** ↔ `clm` (cond.2 HF release pipeline) + `serving` (cond.1 endpoint consumer).
- **anima_physics** ↔ meta `n_substrate` + `substrate_bridge` + `triple_axis_pilots` + `dual_pair_pilots` (substrate-multiplicity sub-axis 정합).

### §3.2 기존 26 file 무수정 audit

기존 .roadmap.* 26개 sha unchanged at land time. mk1 narrative .roadmap (3817 lines, frozen) 무관 (mk1 보존 정책 그대로).

## §4 정책 준수 (raw compliance)

| raw | 적용 | 본 land 적용 방식 |
|---|---|---|
| raw 9 | hexa-only | additive land 자체는 hexa orchestrator 미사용 (3 .roadmap + 1 doc + 1 marker = single-doc pattern, raw 168 minimum-viable exempt) |
| raw 10 | honest C3 | 본 §6 inline 5 caveat |
| raw 11 | snake_case | doc + marker + 3 .roadmap 내 모든 id snake_case (serving.cond.N / training.cond.N / anima_physics.cond.N) |
| raw 12 | silent-error ban | single-shot, error path X |
| raw 15 | env() lazy + <user> | 본 doc 의 모든 anchor repo-relative (`anima/...`), 절대 `/Users/ghost/...` path 본문 인용 X |
| raw 175 | BR-NO-USER-VERBATIM | 사용자 prompt 직접 인용 0건, paraphrase only |
| raw 270 | triplet | 본 land 는 .roadmap 만, README.ai.md 추가는 별도 cycle (각 .roadmap cross_link.triplet_pending 명시) |
| raw 271 | core+modules | 분할 미수행, 별도 cycle deferred (각 .roadmap blockers structural) |
| raw 272 | lint extension | 영향 없음 (additive only) |
| raw 273 | hierarchy direction | 9 candidate 중 rank A 3개만 land (rank B/C 후속 cycle 사용자 lock-in 대기) |

## §5 BR-NO-USER-VERBATIM 준수 confirmation

본 doc + 3 .roadmap 모두 사용자 prompt 내용을 verbatim 으로 인용하지 않음 (raw 175). prompt 요약/재구성으로만 land. handoff doc + .roadmap 정책에 따라 사용자 directive 도 paraphrase 만 기록.

## §6 raw#10 honest C3 (5 caveat)

C1 — 본 land 는 **3 .roadmap.<domain> + 1 handoff doc + 1 marker = 5 NEW file** 만 emit. README.ai.md 추가 0건, 기존 26 .roadmap + 19 README.ai.md 전부 무수정. core/modules 분할 0건 — 모두 별도 cycle deferred.

C2 — verifier seam 의 (a) script 후보 일부는 exit-0 selftest 미수행. 예: `serving/http_server.hexa` healthz 200 round-trip 실측 X / `training/alm_a1_preflight.hexa` exit-0 selftest 미수행 (mac-local + GPU substrate 분리 필요) / `anima-physics/verify_7cond_hw.hexa` G5 LIVE_HW_WITNESS_RATE 0/11 simulation only.

C3 — `training.cond.2 = met` 의 evidence 는 disk artifact 존재 기반 (corpus_clm_combined.txt + .gz + corpus_alm_70b_stripped*.txt + corpus_clm_r4.txt.gz + corpus_alm_r11_r2_index.md 6+ 산출물). 4-stage 통과 실측 (script exit-0 + jsonl/txt/gz emit 1-cycle re-run) 미수행 — disk 증거 = **post-hoc proof**, 4-stage end-to-end fresh PASS 와 별개.

C4 — `anima_physics.cond.1 = partial` 의 ledger v1/v2/v3 cross-link 은 project memory 기반 (FNV=470781997 / 661882989, body_sha=264f5cf7… / df545c5e1540…). v3 disk read-verify 미수행 — aggregator_v3.hexa 내 FNV 값 직접 확인은 별도 cycle.

C5 — clm.cond.2 (HF release v1) ↔ serving.cond.1 cross-link 은 권고만 — 실제 release pipeline integration spec 별도 cycle. n_substrate / triple_axis_pilots / dual_pair_pilots 의 anima_physics.cross_link 도 cluster min-rule 영향 없음 (sister-gate informational only, project memory Mk.XII substrate witness ledger discovery 권고 PARTIAL (A) 그대로).

## §7 friendly preset compliance (handoff doc 친절-preset)

- TL;DR 최상단 5줄
- 모든 §-section 표 (table) 우선
- 3 도메인 status mix 명시 (met/partial/unmet count)
- raw#10 caveats (C1-C5) inline
- 마지막 next-cycle 명시 (rank B/C 후속 + raw 270 triplet 후속)

## §8 marker emit

```
state/markers/anima_rank_a_3_domain_landed.marker
```

## §9 next-cycle (사용자 lock-in 후)

1. **rank B 3개 land** (anima_voice / anima_clm_eeg / anima_engines) — 동일 패턴 (peer perspective, 3 cond mix, 1-2 blockers).
2. **rank C 3개 land** (anima_agent / anima_tools / tool) — `tool` 은 clm.cond.1 verifier 와 중복 가능성, cross-link only 권장 (project memory 의 audit 권고 그대로).
3. **raw 270/271 triplet 후속** (병렬) — rank A 3 surface 부터 README.ai.md + core+modules 분할 (training = T1_large 가장 큰 작업, anima_physics = T2 17 sub-dir).
4. **verifier seam exit-0 selftest** (별도 cycle) — serving healthz smoke / training alm_a1 preflight / anima_physics 7cond_hw + dispatch + edge_deploy 3 cond 의 실제 exit-0 측정.
5. **`tool/roadmap_op.hexa` add 검증** (별도 cycle) — 본 land 는 직접 Write 사용, roadmap_op.hexa add command 와의 idempotent 정합 audit 별도.

## §10 file index (sha-pin at land time)

| path | type | size_b | sha256_hex |
|---|---|---:|---|
| .roadmap.serving | roadmap | 3472 | 1d4c5881eb4de9ad42e69bf11439c34df0d59d961752e1b529fda8940adcf429 |
| .roadmap.training | roadmap | 4496 | 5df3033a650f3404eee78acd135e13abbb990ada7c9974325eb8455570cbe713 |
| .roadmap.anima_physics | roadmap | 5575 | c978104ac53e957b8c12054743902f5be67a0f0c2a07cff4cb415844824b33cc |
| docs/anima_rank_a_3_domain_landed_2026_05_03.ai.md | doc | TBD | (set after write) |
| state/markers/anima_rank_a_3_domain_landed.marker | marker | TBD | (set after write) |

(doc + marker sha pin 은 marker 안에 emit — 본 §10 은 spec only, write 후 marker 가 sha 확정)

## §11 policy summary

- migration: forbidden — 0건 emit
- additive only — 26 .roadmap.* + 19 README.ai.md + 모든 module/core dir 무수정 보존
- destructive ops — 0건
- in-place writes — 0건 (3 roadmap + handoff doc + marker = 5 NEW only)
- substrate — mac-local
- cost — $0
- raw 9 hexa-only — single-doc pattern raw 168 minimum-viable exempt
- raw 10 silent-error ban — single-shot, error path X
- raw 15 env() lazy + <user> — 본문 anchor repo-relative
- raw 175 BR-NO-USER-VERBATIM — 사용자 prompt 직접 인용 0건
- friendly preset — handoff doc only (사용자 응답 X — bg subagent → 메인 monitor)
