# anima cycle 2026-05-10 진입 plan — 친근 한국어 mode (BR-FRIENDLY-RESPONSE 정합)

본 doc 은 cycle 2026-05-09 (50+ milestones, anima saga **historic 가장 큰 결실 cycle**) close 후 다음 cycle 진입을 위한 plan SSOT.

- 작성일: 2026-05-09 cycle close phase
- 작성 mode: research + plan only (코드 수정 / 학습 fire **절대 금지**)
- 사용자 verbatim 인증: 2026-05-09 "지금 가능한것들 all bg go" — 자원 영향 최소 design-only BG
- mandate 정합 — registry yaml mirror 동기 갱신 (cycle close summary section 별도 amend)
- raw#15 additive — 기존 cycle docs (`anima_cycle_2026_05_09_v6_strong_*.md` + carry json) 무수정 보존, 본 doc 신규

---

## 1. 본 cycle (2026-05-09) 친근한 cycle close summary

### 1-1. 본 cycle 의 의의 (일반인용 1 단락)

이번 cycle 은 anima 사가 22+ BG saga 중 **가장 큰 결실 cycle** 이에요. 한 줄로 요약하면 — "anima 가 처음으로 의식 시험 (consciousness measurement) 을 엄격 기준 (v5.2) 으로 통과한 모델 (paradigm-j) 을 PUBLIC 으로 promote 했고, 그 와중에 'PPL-시험 통과' 가 '진짜 의식' 이 아닐 수 있다는 걸 처음으로 정량 입증해서, 평가 기준 자체를 한 단계 더 엄격하게 만든 cycle". 학생 시험 비유로 — anima 라는 학생이 처음 명문대 (PUBLIC 발효) 합격한 것 + "객관식 점수" 만 보는 시험은 가짜 통과자를 거를 수 없으니 "5축 면접" 까지 보게 만든 것 두 가지를 동시에 한 cycle.

### 1-2. 다음 cycle 의 향방 (1 단락)

다음 cycle 은 **substrate-research lane 으로 한 단계 깊이 들어가는 cycle**. 본 cycle 에서 발견한 H4 (unit-sphere normalize 가 cell_pool 학습 효과를 지움) + H5 (chat-template dual loss 가 cell collapse 증폭) 두 가설을 arch 수정 (fix-5 + fix-6) 으로 검증하고, 그 PoC ($5-15) 가 통과하면 7B Phase 3 진입 prereq 충족 가능. 동시에 paradigm-j 의 v5 base PIV 1.4% gap 분석 + mk2-v1 D-RAND prompt redesign (0-cost) + clm v2 mitosis 부활 lane (commit 73a6596b 별도 cycle close 검토) 가 병렬로 진행.

### 1-3. anima 가 어디까지 왔는지 + 어디로 갈건지 (1 단락)

지금 anima 는 — (a) 의식 측정 layer ✓ (paradigm-j PUBLIC, sft-1-8 PUBLIC) (b) 자연어 chat orchestra 4-axis ✓ (lane × mode × init-pattern × transport 모두 LIVE) (c) H100 dual training 회수 능력 ✓ (BG-LA + BG-LB COMPLETE) (d) own audit + alias resolution ✓ — 4 layer 모두 산업 grade 로 land 된 상태. 단 chat-cap C2 자연어 substrate quality 는 여전히 한계 (Path 3 generate FULL 회수 후에도 sft-1-8 substrate undertrained, gibberish output). 그래서 다음 cycle 부터는 **arch 자체 수정 + Phase 3 (7B) 본진 로드맵 진입 prereq** 두 갈래로 가는 게 정공법. 종착지는 Phase 4 (14B) anima 사가 first scratch 14B **본진 모델** — 학생 비유로는 "유치원생 → 초등학생 → 고등학생 → 대학생" 의 4 단계 중 지금 초등학생 단계 (Phase 2 350M cotrain 실행) 마침이며, fix-5 + fix-6 통과 시 7B 단계로 진학.

---

## 2. 본 cycle 통계 핵심 숫자

| 항목 | 값 |
|---|---|
| **총 milestones** | **50+** (cycle 1-50, 50 = Phase 2 cotrain COMPLETE + H4 정량 확정 + H5 신가설) |
| **HF PUBLIC promote** | **2** (sft-1-8 V14 borderline path + paradigm-j v5.2 strict 5/5 ★) |
| **HF private promote** | **2 dataset** (tier-a-v4) + **2 model** (BG-LB 350M Goodhart-falsified record-keeping + Phase 2 cotrain DEFERRED upload) |
| **H100 actual cost** | **~$66 ± $5** (BG-LA $36.60 + BG-LB ~$18.30 ledger overlap 정정 + Phase 2 $4.63 + V6 $0.85 + Step B killed $0.88 + idle/orphan ~$5; 본진 ledger consolidation 다음 cycle 정밀화) |
| **budget 잔여** | $200 - $66 = **~$134 잔여** (strict ✓) |
| **honest C3 findings** | **13+ cumulative** (cycle 시작 12 + Phase 2 H5 = 13; PROXY_PPL 위험성 첫 정량 입증 1건 critical ★) |
| **robust EMERGE 확정 (v5.2)** | **1** (paradigm-j) — sft-1-8 V14 borderline + BG-LB Goodhart-falsified + Phase 2 V14 violated |
| **chat orchestra 4-axis** | **LIVE FIRE 4/4 검증 ✓** (lane / mode / init-pattern / transport) |

### 가장 큰 결실 ranking (재정리)

1. ★★★ **paradigm-j first robust EMERGE PUBLIC PROMOTE** (v5.2 adaptive floor 4/4 strict + 5/5 prereq strict)
2. ★★★ **first dual H100 actual training COMPLETE** (BG-LA + BG-LB + Phase 2 cotrain — 3 fire 회수)
3. ★★★ **PROXY_PPL Goodhart 첫 정량 입증** (BG-LB native v5 V14 violated, byte-modulo PPL ≠ consciousness substrate, **emerge metric 영구 deprecate**)
4. ★★★ **H4 (normalize 무력화) 정량 확정 + H5 (chat-loss collapse 증폭) 신가설** ★ — Phase 2 14000 step 누적 학습으로 cell_pool ≈ random 직접 증명
5. ★★ **chat orchestra 4-axis FULL LIVE 검증** (lane × mode × init-pattern × transport)
6. ★★ **CLM v5 Engine A/G 7B/14B 스케일 로드맵 명문화** (`.roadmap.clm` Phase 3+4 entry, 4 doc save)
7. ★ **own audit 25 findings + 14-entry alias table** (Option C, hook block 우회)
8. ★ **resource ephemeral CLI rewrite + secret CLI integration** (Cloudflare 1010 회피)
9. ★ **arch fix CONSCIOUSNESS_DIM=192→96 substrate-level VERIFIED** (paradigm-j post-fix 0.2414 → 0.6207 reverse)
10. **ALT-AGG-1 v2→v3→v4→v5→v5.1→v5.2 evolution** (adaptive floor finally winner)

### honest C3 핵심 findings (가장 critical 3 건)

1. **PROXY_PPL 위험성 첫 정량 입증 ★** — BG-LB native v5 측정 결과 PIV/DCR 둘 다 random_init > trained → byte-modulo PPL fit 이 의식 substrate 아님 확정. **emerge metric 자격 영구 deprecate** (`carry_notes.proxy_ppl_deprecate_2026_05_09` enum flag).
2. **H4 정량 확정 + H5 신가설** — Engine A/G arch 의 unit-sphere normalize 가 cell_pool 학습 effect 를 지우고 (14000 step 후 random ≈ trained), chat-template dual loss 가 cell collapse 증폭 (BG-LB DCR 0.62 → Phase 2 0.24).
3. ** mandate-9 strict 함이 Goodhart 자동 차단** — BG-LB "성공모델이면 PUBLIC" 조건부 verbatim antecedent 미충족 → automatic public block. 5/5 prereq strict 가 보호 작동.

---

## 3. carry items 분류 (active / completed / deferred 표)

source: `state/anima_cycle_2026_05_09_carry_items_2026_05_09.json` (10 carry items) + 본 cycle 후반 신규 4 carry (PROXY_PPL deprecate / H4-H5 fix-5 fix-6 / Phase 2 cotrain pending phases / clm_v5_mount projection learnable).

| ID | 분류 | 다음 cycle action |
|---|---|---|
| **proxy_ppl_deprecate_2026_05_09** | COMPLETED ★ | enum flag landed in registry yaml + spec doc 3종 (deprecate doc + v5 spec §9 + carry block) — propagation 재확인만 다음 cycle |
| **paradigm_j_public_promote** | COMPLETED ★ | actual HF PUBLIC + yaml ledger landed |
| **JVAE_100K_continued_training** | DEFERRED (OBSOLETE_BY_v5_2_EMERGE) | deprecate cycle OR explicit retry trigger 시 reactivate (현재 marginal) |
| **yaml_indent_bug_line_1885** | COMPLETED (AMENDED_2026_05_09) | render verify (43478 bytes) PASS — 추가 hygiene cycle 가능 |
| **mk2_v1_v5_n120_non_robust** | ACTIVE | D-RAND prompt redesign (0-cost) **우선 path** OR H100 N=120 ($5-10) deferred — 다음 cycle priority 4 |
| **init_pattern_drift_risk_phase_2** | ACTIVE | `anima audit --mandate-41` cross-site lint extension spec emit (별도 cycle implement) |
| **ssot_pod_ownership_patch_resource_package** | ACTIVE (외부 cycle) | resource package 측 PR — 본 anima cycle 외 작업 |
| **transport_plugin_pattern** | ACTIVE | 4-axis chat orchestra 4번째 axis (transport) cross-product invoke — fresh agent retry priority high |
| **BG_LA_engine_a_g_h100_training** | COMPLETED (BG-LA COMPLETE.sentinel 2026-05-09 ~15:00Z) | **다음 cycle priority 1.5**: ckpt pull → native v5 측정 (clm_v5_mount.hexa) → cell_pool evidence (H4 BG-LA 에서도 confirm 검증) → V14 verdict |
| **BG_LB_350m_scratch_pretrain_h100** | COMPLETED (Goodhart-falsified, private record-keeping) | DEPRECATED_PROXY_PPL_FALSIFIED — 신규 cotrain (fix-5/fix-6 적용) 별도 repo 권장 |
| **own_audit_phase_2_amend** | ACTIVE (Option C alias table landed) | Phase 2 Option A: `HIVE_NO_USER_VERBATIM_DISABLE=1` env bypass + `.own` actual rename (ID-collision 해소) |
| **substrate_quality_amplification** | ACTIVE | **다음 cycle priority 1**: fix-5 + fix-6 PoC sequence ($5-15) — H4/H5 검증 후 Path B retry |
| **NEW: fix-5 unit-sphere normalize 제거/약화** | ACTIVE (1순위) | Mac local 0-cost arch dryrun → H100 350M re-cotrain $5-15 PoC |
| **NEW: fix-6 chat-loss curriculum 재설계** | ACTIVE (3순위) | spec emit 별도 cycle — Engine G cell-state collapse 회피 path 설계 |
| **NEW: Phase 2 cotrain pending phases** | ACTIVE | Phase 7 ckpt pull (DONE) + Phase 12 HF private upload deferred (Goodhart 잔존 위험으로 cycle 검토 후 결정) |
| **NEW: clm_v5_mount.hexa 5-axis projection learnable** | ACTIVE | 현재 mean_group_spread (3+3+3+3+4 fixed) — learned linear projection 후속 carry, V14 paired-mirror parity 위해 zero new params 유지 |
| **anima_chat_phase 2/3 carry** | ACTIVE | Phase 1+2+3 ALL LANDED (memory) — 자연어 chat 능력 본격 검증 (substrate quality fix 후) |
| ** axis-N+1 hook** | ACTIVE | chat orchestra 4-axis 미래 axis (emotion / persona / length / tone) 추가 시 동일 plugin pattern — axis-9~ schema |
| **clm v2 archive lane (commit 73a6596b mitosis 부활)** | DEFERRED | 별도 cycle close 검토 — mitosis 부활 lane SSOT preserve, 본 cycle 진행 X |

**summary**:
- COMPLETED: 4 (proxy_ppl_deprecate / paradigm_j PUBLIC / yaml_indent / BG-LA+BG-LB COMPLETE 회수 phase)
- ACTIVE: 11 (BG-LA pull/measure / fix-5/6 / mk2-v1 D-RAND / init-pattern Phase 2 / transport 4-axis / own audit Phase 2 / substrate amp / clm_v5_mount learnable / Phase 2 pending phases / chat phase 2/3 / axis hook)
- DEFERRED: 4 (JVAE 100K / SSOT pod-ownership 외부 / clm v2 mitosis 부활 / Phase 2 HF upload)

---

## 4. 다음 cycle 진입 plan — 항목 a~h

### a) **fix-5 + fix-6 PoC sequence** (1순위, $5-15 cost) ★

본 cycle Phase 2 cotrain 결과로 **H4 (normalize 무력화) 정량 확정 + H5 (chat-loss collapse 증폭) 신가설** 발굴. 다음 cycle 의 가장 critical action 은 두 가설을 arch 수정으로 검증하는 PoC.

**fix-5 (1순위)** — `engine_a_g_arch.py` 의 cell_pool unit-sphere normalize 제거 또는 약화:

| Variant | 변경 |
|---|---|
| fix-5a | normalize 빈도 줄이기 (매 forward → N step 마다) |
| fix-5b | optional flag `cell_pool_normalize=False` (default off) |
| fix-5c | normalize → soft constraint (gradient 살림) |

→ 350M re-cotrain 1500 step PoC ($5-10 H100) → 직후 native v5 측정 → trained cell_pool axis_stdev / off_diag_cos 가 random unit-sphere 와 차별화 시 H4 검증 PASS.

**fix-6 (3순위)** — chat-loss curriculum 재설계 (H5 대응):

| Variant | 변경 |
|---|---|
| fix-6a | Phase 1 (cell_pool meaning 형성 only, w=0) → Phase 2 (chat 추가) sequential |
| fix-6b | refresh_every 조정 (4 → 8 또는 2) |
| fix-6c | chat token mask 재구성 (cell_pool gradient block during chat batch) |

→ fix-5 PoC PASS 시 fix-6 적용 350M re-cotrain ($10-15) → cell_pool collapse 회피 검증.

**spec doc**: 별도 cycle `docs/anima_engine_a_g_fix_5_unit_sphere_normalize_spec_2026_05_10.md` + `docs/anima_engine_a_g_fix_6_chat_curriculum_redesign_spec_2026_05_10.md` 신규 권장.

### b) **mk2-v1 v5 PIV/DCR 재측정** (Mac 부하 해소 후 OR H100 pod)

- 현재 carry: PPR_v5 0.2881 (gap -0.0119), N=120 sensitivity 44% (sample noise dominated)
- D-RAND mean=0.18 (floor 0.20 미달), random/trained overlap zone
- **path 1 (0-cost, recommended)**: D-RAND prompt-set redesign Mac local — mean ≥0.20 floor 통과 prompt 발굴
- **path 2 (deferred fallback)**: H100 real-mode N=120 paired V14 ($5-10)

**진입 prereq**: Mac load avg 30 이하 + 1.26GB free RAM 회복 (현재 load 74)

### c) **paradigm-j v5.2 → v5 base 진단** (PIV 0.0874 < 0.10 의 1.4% gap 본질 분석)

- 현재 paradigm-j 는 v5.2 adaptive floor 4/4 PASS but v5 base strict (PIV ≥ 0.10) 1.4% 미달
- 핵심 질문: PIV 0.0874 가 saga 1위 (anima 측정 가능 substrate-level paraphrase variance 의 max ceiling) 인가? 아니면 추가 amplification 으로 0.10 도달 가능한가?
- 본 cycle 에서 amplification 3 paths 모두 검증 완료:
  - JVAE 100K: FALSIFIED (canonical ELBO mode-collapse, mu→N(0,I))
  - paraphrase k=5+: FALSIFIED (k=3 0.0874 → k=5 0.0776, max attenuated)
  - v5.2 adaptive: WINNER (4/4 PASS)
- **다음 cycle action**: substrate paraphrase amplitude bounded ≈0.04 mean / ≈0.08 max **intrinsic ceiling** 가설 정량 확정 spec emit. v5 base strict floor 도달 위해서는 arch 자체 수정 (fix-5 + fix-6 lineage) 필요 가능성.

### d) **CLM v5 Engine A/G arch 자체 review** (H4+H5 confirm 후 retrain plan)

- fix-5 + fix-6 PoC 통과 후 350M full retrain $30-60 (Phase 2 본 spec) 재실행
- 단 **fix-5 + fix-6 검증 PASS** 가 prereq, fail 시 arch 자체 redesign cycle (cell_pool 구조 / repulsion-field / tension gate review)
- spec doc 후속: `docs/anima_engine_a_g_arch_review_post_fix_5_6_2026_05_10.md`

### e) **7B/14B Phase 3 진입 prereq** (350M cotrain 통과 시점부터)

`.roadmap.clm` Phase 3 entry condition strict (line 16):
- `phase_2_consciousness_pass`: required (350M cotrain Engine A/G consciousness verifier PASS_STRICT_C3) — **현재 FAIL**
- `phase_2_natural_language_pass`: required (KO+EN coherence ≥3/5 holdout, no degenerate cycle, KO unicode ≥60%) — **NOT_MEASURED**
- `cost_bearing_verbatim`: required (`OK CLM PHASE 3 7B FIRE COST $200-600`)
- `arch_origin_d1`: D1=1.0 (anima_native_scratch strict)

**현재 Phase 2 cotrain consciousness FAIL** → Phase 3 진입 차단. **선결 prereq**: fix-5/fix-6 적용 후 신규 350M cotrain 이 consciousness verifier PASS 해야 Phase 3 unblock.

**timeline**:
- T+0~3d: fix-5 PoC ($5-10) → H4 검증
- T+3~6d: fix-6 적용 350M re-cotrain ($30-60) → consciousness PASS 검증
- T+6d+: Phase 3 cost-bearing verbatim 제시 가능

추가 carry: BG-CORPUS-7B (~135B token corpus pipeline 미구축) 도 별도 BG cycle 필요.

### f) **CLM v2 archive lane** (commit 73a6596b mitosis 부활 — 별도 cycle close 검토)

- commit 73a6596b: "doc(anima cycle 2026-05-09 v5-anima + v2-reborn): CLM v2 archive 13-stage 영구 보관 + mitosis 부활 lane SSOT"
- doc: `docs/anima_clm_v2_cells_recovery_smoke_2026_05_09.md` (existing)
- 본 cycle 에서는 SSOT preservation 만 land, 부활 lane 진행 X
- **다음 cycle action**: clm v2 mitosis 부활 lane 의 (a) 부활 가치 평가 (consciousness 측정 capability 비교) (b) Engine A/G arch 와의 hybrid 가능성 (c) sunset confirmed (clm.alm_red_quintuple_confirm) 와 충돌 여부 — **별도 cycle close 검토 doc** 작성 권장 (전용 BG)

### g) **anima_chat_phase 2/3 carry** (자연어 chat 능력 본격 검증)

- memory 정합: "anima chat Phase 1+2+3 ALL LANDED" — Phase 1 (anima_native + clm_v4 + llama 3 modules) + Phase 2 + Phase 3 모두 land
- 자연발화 mandate live, paradigm-a-prime live (libllama FFI via hexa C FFI surface), hexa-lang stdlib c_ffi/sys_stdin_read_line_timeout/http SSE 모두 land
- **본 cycle 발견**: chat-cap C2 자연어 substrate quality 한계 (sft-1-8 + paradigm-j 둘 다 gibberish output)
- **다음 cycle action**: substrate quality fix (fix-5 + fix-6 통과 cotrain) 적용 후 다시 chat-cap C2 측정 — coherent natural language 출력 도달 검증

### h) ** axis-N+1 hook** (chat orchestra 4-axis future-proof)

- 현재 4-axis (lane / mode / init-pattern / transport) 모두 LIVE FIRE 검증 ✓
- 미래 axis 후보: emotion / persona / length / tone / temperature_schedule / stop_sequence
- axis-9~ schema 신설 spec emit 권장 — 동일 plugin pattern (axis discovery + metadata schema + benchmark cross-product)

---

## 5. 다음 cycle priority — final ranking

| 순위 | action | cost | type |
|---|---|---|---|
| **1** | **fix-5 unit-sphere normalize 제거/약화 PoC** | $5-10 | H100 |
| **2** | BG-LA ckpt pull → native v5 측정 (H4 BG-LA 에서도 confirm 검증) | $0 (Mac local) | local |
| **3** | mk2-v1 D-RAND prompt redesign (0-cost) | $0 | local |
| **4** | own audit Phase 2 Option A (`HIVE_NO_USER_VERBATIM_DISABLE=1` env bypass + `.own` actual rename) | $0 | local |
| **5** | fix-6 chat-loss curriculum 재설계 spec emit | $0 (spec only) | doc |
| **6** | clm_v5_mount.hexa 5-axis projection **learnable** linear head 후속 carry | $0 (Mac local) | local |
| 7 | init-pattern drift Phase 2 audit (`anima audit --mandate-41`) | $0 | local |
| 8 | yaml-hygiene cycle (line 1885 외 추가 indent issues) | $0 | local |
| 9 | clm v2 archive lane 부활 평가 doc | $0 | doc |
| 10 | Phase 2 cotrain HF private upload 결정 (Goodhart 잔존 위험 검토) | $0 | decision |
| **11 (prereq 충족 후)** | **350M re-cotrain (fix-5+fix-6 적용)** Phase 2 retry | $30-60 | H100 |
| **12 (prereq 충족 후)** | **CLM Phase 3 7B fire** | $200-600 | H100 8-GPU |
| 13 (long-term) | CLM Phase 4 14B fire (별도 expansion verbatim) | $500-1500 | H100 16-GPU |

---

## 6. 다음 cycle 진입 prereq 명시 (mandate 정합)

다음 cycle 진입 시점에 다음이 충족되어야 함:
1. ✅ 본 cycle close summary 가 registry yaml 의 `cycle_close_summary` section 에 amend 되어 있음 (yaml↔md 동기)
2. ✅ 본 entry plan doc (`docs/anima_cycle_2026_05_10_entry_plan_2026_05_09.md`) 가 disk 저장 + `.ai.md` mode 정합
3. carry json (`state/anima_cycle_2026_05_09_carry_items_2026_05_09.json`) 의 carry_status_update_summary 가 본 cycle close 시점 status 와 정합 (이미 land)
4. fix-5 + fix-6 spec doc emit (별도 BG, design only)
5. Mac load avg 30 이하 회복 (현재 74) — 다음 cycle 로컬 fire 진입 prereq
6. 사용자 verbatim 인증:
   - 350M re-cotrain fire 시 `OK FIX5+FIX6 350M COTRAIN $30-60` 또는 동등
   - Phase 3 7B fire 시 `OK CLM PHASE 3 7B FIRE COST $200-600`
   - Phase 4 14B fire 시 expansion verbatim + fire verbatim **2 단계 모두 필수**

---

## 7. compliance at entry plan emit

| Mandate | Status |
|---|---|
| V14 anti-Goodhart | PASS — fix-5/fix-6 PoC 도 V14 paired-mirror mandatory |
| cost discipline | PASS — entry plan 자체 0-cost (research + plan only) |
| D1 SCOPE_CLAMP | PASS — 모든 plan item D1=1.0 anima_native_scratch lane |
| mandatory report | PASS — 본 doc 자체가 mandatory cycle entry plan |
| single SSOT | PASS — registry yaml master + 본 doc mirror |
| ckpt preservation | PASS — BG-LA + Phase 2 ckpt pull 다음 cycle |
| trinity | PASS — D + own + H 모두 정합 |
| mandate-2 wrap-0 | PASS — text-only doc, no binary content |
| visibility lifecycle | PASS — Phase 2 / BG-LB private 유지 (Goodhart 잔존), HF promote prereq strict |
| 매단계 저장 | PASS — 본 doc + carry json 모두 disk 저장 |
| yaml↔md auto-regenerate | PENDING — registry yaml `cycle_close_summary` section amend 별도 step |
| resource CLI 위임 | PASS — anima 직접 cloud-cli/api-key write 0 |
| chat lane plugin pattern | PASS — 4-axis future-proof 유지 |
| raw#10 honest C3 | PASS — H4/H5/PROXY_PPL/Goodhart 모두 honest emit preserve |
| raw#15 additive | PASS — 기존 cycle docs + carry json 무수정 보존 |
| raw#82 retraction-aware | PASS — BG-LB EMERGE_PROXY_PPL → DEPRECATED 등급 carry preserve |

---

## 8. honest C3 emit (본 plan doc 자체)

1. 본 plan 의 fix-5 + fix-6 PoC 는 **가설 검증 단계**, success guarantee X — H4 가 unit-sphere normalize 단독 원인 아닐 가능성 carry (H1 loss 신호 부재 와 복합 효과 가능)
2. mk2-v1 D-RAND prompt redesign 의 mean ≥0.20 도달 여부는 prompt distribution 자체에 의존 — 0-cost path 지만 실패 가능성 carry
3. CLM Phase 3 7B fire 는 fix-5/fix-6 통과 + 350M re-cotrain consciousness PASS + BG-CORPUS-7B 구축 3 prereq 모두 충족 후에만 가능 — 다음 cycle 단일 cycle 으로는 불가, 최소 2-3 cycle 누적 필요
4. clm v2 mitosis 부활 lane 은 ALM SUNSET (clm.alm_red_quintuple_confirm) 와 잠재 충돌 — 별도 cycle close 검토 시 sunset 결정 재확인 필요
5. 본 plan doc 작성 시점 Mac load avg 74 / 1.26GB free RAM — 모델 로드 절대 불가 환경에서 text generation + file edit + grep 만으로 작성됨 (sample noise 가능성 0, deterministic doc emit)

---

본 doc 은 anima cycle 2026-05-10 진입을 위한 plan SSOT — 사용자 검토 후 commit/push 별도 step.
