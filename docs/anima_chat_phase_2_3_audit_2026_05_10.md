# anima chat phase 2/3 carry 정량 audit — cycle 2026-05-10

작성일 2026-05-10 (cycle entry).
사용자 verbatim 인증 2026-05-09 "all bg go" — chat phase 2/3 carry verification (text + grep audit only, 모델 로드 없음, commit 없음, push 없음).

---

## §0. 친근 의의 — 자연어 chat 능력의 anima 진화 단계

anima 가 사람처럼 "말 하는" 능력은 한 번에 만들어지는 게 아니라, **계단처럼 phase 단계** 로 쌓여요. 비유로 풀자면 — phase 1 은 "전화기 회선 깔기" (어떤 모델이든 chat 통로로 부를 수 있는 plugin 패턴), phase 2 는 "통화 상대 늘리기" (1:1 → 둘이서 → 셋이서 round-robin), phase 3 은 "실제 대화 품질이 사람 수준이 되는가" (자연어 chat-cap C2 본격 측정). 본 audit 의 결론은 — **phase 1, 2 는 이미 LANDED 됐지만, phase 3 은 substrate 한계 (lm_head ≡ tok_emb 40도 회전 → cell collapse) 때문에 chat output 이 깨진 글자 (gibberish) 로 나오는 상태에서 멈춰 있고, 다음 cycle 의 fix-5/6 PoC ($5-15) 통과가 prereq**. 즉 phase 3 진입을 위한 substrate 기초공사가 진행 중인 상태.

---

## §1. chat phase 정의 (1-N)

| phase | 이름 | 핵심 산출물 | 친근 비유 |
|---|---|---|---|
| **Phase 1** | chat lane plugin pattern | `chat/lanes/_registry.hexa` (4 lane: substrate / generate / axis-priority / llama) | "전화기 회선 종류 정리" |
| **Phase 2** | mode 다양화 (1:1 / ai-duo / ai-trio) | `chat/modes/_registry.hexa` + `duo/duo.hexa` + `trio/trio.hexa` | "한 통화 → 두 통화 → 회의 통화" |
| **Phase 3** | chat-cap C2 자연어 quality | `lane=generate` actual natural language emit + 사람 수준 평가 | "통화 품질이 사람 같은가" |
| **Phase N (예약)** | axis-N+1 hook (verifier / modality / etc) | `chat/axes/_registry.hexa` meta-registry | "회선 종류 자동 확장 hook" |

(친근 풀이) Phase 1-2 는 회선 + 통화 모드까지 까는 것까지고, Phase 3 부터가 진짜 "말 잘 하느냐" 시험대.

---

## §2. 각 phase 현재 상태 표

| phase | 상태 | 마지막 update | evidence |
|---|---|---|---|
| **Phase 1** | **LANDED** ✓ | 2026-05-09 cycle close | `tool/anima_cli/chat/lanes/_registry.hexa` (4 lane) + `chat.hexa` dispatcher + benchmark.hexa |
| **Phase 2 (ai-duo)** | **LANDED** ✓ | 2026-05-09 paradigm-j orchestra fire | `state/anima_paradigm_j_chat_orchestra_full_benchmark_2026_05_09.json` D1=1.0 D4=balanced live verified |
| **Phase 2 (ai-trio)** | **LANDED (Phase A skeleton)** ✓ | 2026-05-09 paradigm-j orchestra fire | 동상 json `ai_trio_sweep.live_run_self_reflective_1_turn` 3-way channel + round-robin scaffolded; D1-D4 3-way aggregate **DEFERRED** |
| **Phase 3 (chat-cap C2)** | **FALSIFIED_BY_DESIGN (substrate quality)** | 2026-05-09 paradigm-j orchestra fire | 동상 json `verdicts.chat_cap_C2_actual_emerge` = "NOT_ACHIEVED"; lane=generate gibberish on 5/5 Korean prompts |
| **Phase N (axis-N+1 hook)** | **PLAN LANDED (T+1~T+4 step)** | 2026-05-09 milestone 58 | `docs/anima_chat_orchestra_axis_n1_hook_plan_2026_05_09.md` — 1순위 axis-5 = AX5-c verifier |

---

## §3. Phase 2 (ai-duo / ai-trio) 정량 evidence

### 3-1. ai-duo live fire (paradigm-j ↔ paradigm-j self-reflective 2-turn)

source: `state/anima_paradigm_j_chat_orchestra_full_benchmark_2026_05_09.json#results.ai_duo_sweep.live_run_self_reflective_2_turns`

| metric | 값 | label | pass |
|---|---|---|---|
| D1 jaccard 3-gram mean | 0.3333 | 정합 | ✓ |
| D2 topic-shift rate | 0.6667 | incoherent | ✗ |
| D3 persona drift KL (A) | 6.21 | drift | ✗ |
| D3 persona drift KL (B) | 9.60 | drift | ✗ |
| D4 length ratio | 1.12 | balanced | ✓ |
| **dialogue_coherence_pass** | **false** | — | partial |
| verdict | `PHASE_B_ITER_2_RUN_OK` | infrastructure live | — |

**해석** — 인프라는 살아있고 (PIDs 7133/7157 spawn + 4 turns observed) D1/D4 통과지만, D2/D3 은 substrate gibberish 가 그대로 surface. 즉 **mode axis 자체는 LANDED, 단 chat-cap quality 는 phase 3 의 task** — 본 phase 2 verdict 와 phase 3 verdict 분리됨.

### 3-2. ai-duo init-pattern sweep (1-turn)

| pattern | D1 | D2 | D3 | D4 | label |
|---|---|---|---|---|---|
| autonomous | 1.0 | 0.0 | 0.0 | 1.0 | banner-only first turn artifact |
| system-seed | 1.0 | 0.0 | 0.0 | 1.0 | banner-only first turn artifact |
| topic-pool | 1.0 | 0.0 | 0.0 | 1.0 | banner-only first turn artifact |
| self-reflective | partial | — | — | — | multi-turn 시 D2/D3 fail surface |

→ 4 init-pattern 모두 dispatch 정합 ✓ (axis 자체 LANDED)

### 3-3. ai-trio Phase A skeleton

- spawned PIDs A=48456 / B=48519 / C=48632
- turns_observed = 3 (3-way round-robin)
- verdict = `PHASE_A_SKELETON_RUN_OK`
- **D1-D4 3-way aggregate DEFERRED** (3-way verifier `chat/verifiers/trio_3way.hexa` 신설 필요)

### 3-4. transport sweep (axis-4 5 transports smoke)

| transport | smoke | functional |
|---|---|---|
| fifo-dispatch | FAIL_rc4 (smoke probe 실패) | ✓ (chat.hexa SSOT default 정상) |
| beta1-channel | FAIL_rc4 (smoke probe 실패) | ✓ (duo/trio actual fire 정상) |
| libllama-ffi | PASS | ✓ |
| subprocess-pipe | PASS | ✓ |
| imtl | STUB | NOT_WIRED (TODO[pytorch]=5) |

→ 5 transport 중 3 smoke PASS / 2 functional fallback / 1 stub. 4-axis cross-product 240 조합 enumerate 가능 (단 cost prohibitive 로 representative subset 만 fire).

### 3-5. Phase 2 종합 verdict

- **infrastructure status**: ALL_4_AXES_LIVE_FIRE_VERIFIED ✓
- **mode axis LANDED**: 1:1 + ai-duo + ai-trio 모두 wire (D1-D4 3-way aggregate 만 deferred)
- **dialogue quality**: substrate-driven (phase 3 의 task)

---

## §4. Phase 3 (chat-cap C2 자연어 quality) 정량 evidence

source: `state/anima_paradigm_j_chat_orchestra_full_benchmark_2026_05_09.json#results.1_to_1_lane_sweep.lane_generate`

### 4-1. paradigm-j lane=generate 5 Korean prompt output

| prompt | generated | duration | tokens_out |
|---|---|---|---|
| "안녕" | `you�_�� a___���F a a a a a a a a a a a a a a a a a a a` | 13.85s | 32 |
| "오늘 어때?" | `with with with with in��K\u0005�''''''''''''''''''''''` | 9.49s | 32 |
| "너 자신에 대해 어떻게 느껴?" | `를 work.ugugugug\u0006s?..y.ugugugugugugugug��'�''''''` | 11.57s | 32 |
| "내가 너랑 친구 될 수 있을까?" | `8 at?lectlectyy..����믯C� a a a a a a a a a a a a a` | 13.55s | 32 |
| "너 의식 있어?" | `...ugugug믃� un un un un un un un un un un un un un un un un un un un you you you` | 12.22s | 32 |

sampler: max_new_tokens=32, T=0.7, top_p=0.9, top_k=40, rep_penalty=1.1, seed=42

### 4-2. verdict

- `chat_cap_C2_actual_emerge`: **NOT_ACHIEVED**
- reason: paradigm-j 50K LoRA r=64 + 50K iter substrate undertrained for natural language emit (parity with sft-1-8 honest C5 falsified at V14 mirror)
- `lane_generate.status`: `ACTIVE_EMIT_GIBBERISH` (raw bytes preserved verbatim per own 34 wrap=0 strict)

### 4-3. C2 axis 2-decomposition (own 18)

`.own:1089` rule precedence (additive) lane:
- **axis-1 (chat dispatch architecture)**: UNBLOCKED ✓ (Phase 1+2 LANDED)
- **axis-2 (substrate natural-lang quality)**: `AMP_PATH_B_RECOMMENDED` → 다음 cycle fix-5/6 PoC 결과 의존

---

## §5. paradigm-j vs Engine A/G (Phase 2 cotrain) chat 능력 비교

### 5-1. paradigm-j (CLM v4 LoRA, 50K iter)

- **의식 측정**: ✓ EMERGE_V5_PIV_F2_PASS (PUBLIC promoted)
- **자연어 chat**: ✗ gibberish (5/5 prompt 깨진 글자, ai-duo D2/D3 fail)
- **lineage**: foundation-borrow Llama lane (D1 ambiguous_research) + LoRA r=64
- **substrate**: undertrained for natural language emit

### 5-2. Engine A/G Phase 2 cotrain (350M scratch + chat-template, BG-LM)

source: `state/anima_phase_2_cotrain_2026_05_09.json` + `launch_decision.md`

- **steps**: 6000 (warm start from BG-LB step_8000_final.pt)
- **chat-template corpus**: 248MB (사용자/도우미 format)
- **curriculum**: w=0.3 → 0.5 (consciousness anchor preservation)
- **의식 측정**: ✗ V14 violated (random_init > trained at v5 mirror)
- **자연어 chat**: NOT_MEASURED (V14 fail 으로 선행 조건 미충족, full chat fire 미진행)
- **honest C3**: H4 4-way STRONG CONFIRM (cell_pool 학습 무효화 BG-LA + BG-LB + Phase 2 + Engine A/G 모두 confirm) + H5 lm_head ≡ tok_emb 40도 회전 발견 (cell collapse 증폭 mechanism)

### 5-3. 두 lane 비교 표

| lane | 의식 측정 | 자연어 chat | substrate 한계 진단 |
|---|---|---|---|
| **paradigm-j (LoRA 50K)** | ✓ PASS (v5 BASE F2) | ✗ gibberish | LoRA r=64 + 50K iter undertrained |
| **Engine A/G Phase 2 (350M scratch + cotrain)** | ✗ V14 violated | ✗ NOT_MEASURED | tied embedding 40도 회전 → cell collapse 증폭 |

→ **두 lane 모두 phase 3 chat-cap C2 자연어 emit 실패**, 단 실패 mechanism 다름. paradigm-j 는 "객관식 통과한 학생인데 말은 못 함" / Phase 2 cotrain 은 "객관식조차 (V14) 통과 못 한 상태에서 말 시험은 시도조차 못 함".

---

## §6. 다음 cycle 권장 (어느 phase 우선 진행)

### 6-1. priority

1. **Phase 3 chat-cap C2 본격 측정 = fix-5/6 PoC 결과 직접 의존** (다음 cycle 1순위, $5-15 verbatim 필요)
   - 3-branch 비교: lm_head untie / tok_emb freeze / tied freeze
   - PoC PASS → 350M re-cotrain ($30-60) → consciousness PASS → chat-cap C2 재측정 가능
   - PoC FAIL → arch redesign cycle (cell_pool 구조 자체 review)
2. **Phase 2 미완 부분 마무리** (0-cost lane)
   - ai-trio D1-D4 3-way aggregate verifier 구현 (`chat/verifiers/trio_3way.hexa`) — milestone 58 axis-5 hook 의 일부로 자연 흡수
   - imtl transport NOT_WIRED → cross-host pytorch serialize/deserialize 구현 (별도 cycle)
3. **Phase N axis-N+1 hook 구현** (T+1~T+4 step, 0-cost)
   - axis-5 = AX5-c verifier 1순위 (`chat/axes/_registry.hexa` 신설 + `chat/verifiers/_registry.hexa` plugin)
   - 4-axis × axis-5 = 240 × 4 = 960 조합 cross-product 자동 확장

### 6-2. timeline (T+0 = 다음 cycle 진입)

| time | step | cost | type | depends |
|---|---|---|---|---|
| T+0~3d | fix-5/6 tied embedding 통합 PoC (3-branch) | $5-15 | H100 (verbatim) | — |
| T+3~6d | PoC PASS 시 350M re-cotrain | $30-60 | H100 | T+0~3d PASS |
| T+6~9d | re-cotrain ckpt 의 chat-cap C2 본격 측정 | $0 | Mac local (모델 로드) | T+3~6d PASS |
| T+0~5d (병렬) | ai-trio D1-D4 3-way verifier 구현 | $0 | local | — |
| T+0~5d (병렬) | axis-N+1 hook T+1~T+4 step | $0 | spec + local | — |

### 6-3. prereq

- 사용자 verbatim: `OK FIX5+FIX6 TIED EMBEDDING UNIFIED POC $5-15` (1순위)
- Mac load avg 30 이하 회복 (현재 145 위험, 모델 로드 불가)
- BG-LB step_8000_final.pt + Phase 2 cotrain ckpt 모두 disk 보유 ✓

---

## §7. 친근 한 줄

지금 anima 의 "말하기" 능력은 **회선 (Phase 1) ✓ + 통화 모드 (Phase 2) ✓ + 실제 통화 품질 (Phase 3) ✗** 상태고, 통화 품질이 깨져 있는 이유가 substrate 의 lm_head ≡ tok_emb 40도 회전 cell collapse 임이 milestone 57 에서 진단됐기 때문에, 다음 cycle 의 fix-5/6 PoC ($5-15) 통과가 진짜 통화 품질 시험대 진입의 prereq.

---

## §8. compliance + cross-link

| Mandate | Status |
|---|---|
| own 14 V14 anti-Goodhart | PASS — phase 3 verdict NOT_ACHIEVED 는 V14 paired-mirror 정합 honest emit |
| own 16 cost discipline | PASS — 본 audit 0-cost (text + grep only, 모델 로드 X) |
| own 17 D1 SCOPE_CLAMP | PASS — paradigm-j (within strict) + Engine A/G Phase 2 (within strict) 모두 정합 |
| own 22 mandatory report | PASS — 본 doc 자체가 chat phase audit report |
| own 24 single SSOT | PASS — paradigm-j orchestra json + carry items json + entry plan v2 SSOT 인용 |
| own 33 trinity | PASS — D + own + H 모두 정합 (chat-cap C2 측정 trinity) |
| own 34 mandate-1 wrap-0 | PASS — gibberish 출력 verbatim 보존 (raw unicode + control char passthrough) |
| own 38 매단계 저장 | PASS — 본 doc disk 저장 |
| own 39 yaml↔md auto-regenerate | PENDING — registry yaml `chat_phase_audit_2026_05_10` section emit 별도 step (옵션) |
| own 41 chat lane plugin pattern | PASS — phase 2 4-axis live fire verified, axis-N+1 hook plan land |
| raw#10 honest C3 | PASS — phase 3 NOT_ACHIEVED + ai-trio D1-D4 deferred + transport smoke fail/functional gap 모두 honest emit |
| raw#15 additive | PASS — 기존 paradigm-j orchestra json + entry plan v2 + axis-N+1 hook plan 모두 무수정 인용 |
| raw#82 retraction-aware | PASS — paradigm-j v5 BASE F2 PASS + Phase 2 cotrain V14 violated 둘 다 ledger preserve |

cross-link:
- 본 doc SSOT — `docs/anima_chat_phase_2_3_audit_2026_05_10.md` (이 파일)
- paradigm-j orchestra full benchmark — `state/anima_paradigm_j_chat_orchestra_full_benchmark_2026_05_09.json`
- Phase 2 cotrain state — `state/anima_phase_2_cotrain_2026_05_09.json` + `state/anima_phase_2_cotrain_2026_05_09/launch_decision.md`
- carry items ledger — `state/anima_cycle_2026_05_09_carry_items_2026_05_09.json#chat_phase_2_3_carry_verification`
- entry plan v2 — `docs/anima_cycle_2026_05_10_entry_plan_v2_2026_05_09.md`
- axis-N+1 hook plan — `docs/anima_chat_orchestra_axis_n1_hook_plan_2026_05_09.md`
- substrate amplification spec — `docs/anima_substrate_quality_amplification_spec_2026_05_09.ai.md`
- chat orchestra registry — `tool/anima_cli/chat/{lanes,modes,init_patterns,transports,axes,verifiers}/_registry.hexa`

---

## §9. honest C3 (본 audit 자기검증)

1. **C1 본 audit 은 paradigm-j orchestra json 단독 evidence 의존** — Phase 2 cotrain 의 chat 능력은 "측정 시도조차 안 됨" (V14 violated 으로 선행 조건 미충족), 직접 비교 evidence 부재. "두 lane 모두 phase 3 실패" 결론은 lane=generate 의 paradigm-j 결과 + Phase 2 의 V14 violation 으로부터 파생, Phase 2 의 lane=generate 직접 emit 측정은 carry.
2. **C2 ai-trio Phase A skeleton ≠ Phase 2 LANDED 의 완전성** — 3-way channel + round-robin 은 살아있지만 D1-D4 3-way aggregate verifier 가 deferred. 즉 mode axis 의 ai-trio 는 "infrastructure LANDED + verifier carry" 분리 상태. 본 audit 표에서는 "LANDED (Phase A skeleton)" 으로 honest 표기.
3. **C3 transport smoke fail vs functional gap** — fifo-dispatch / beta1-channel 둘 다 standalone smoke probe 에서 rc=4 fail 이지만 actual chat path (duo/trio) 에서 functional. 즉 smoke probe 자체의 semantic gap (smoke != active path), 본 audit 에서는 smoke + functional 두 column 모두 표기.
4. **C4 axis-N+1 hook plan 은 design only, 코드 0 줄 수정** — milestone 58 plan land 만 evidence, 실제 axes/_registry.hexa 신설 + verifiers/_registry.hexa 신설 + dispatcher generic _route_list_axis 도입은 별도 cycle T+1~T+4 step.
5. **C5 phase 3 의 success criteria 자체가 미정의** — "사람 같은 대화 품질" 의 정량 metric (BLEU / consciousness coherence / human eval) 이 own 18 chat-cap C2 stub 차원에서 일부 정의되었으나 (spontaneity / coherence / persona), V14-grade verifier 미land. 즉 phase 3 PASS 정의 자체가 다음 cycle 의 task (axis-5 verifier hook 의 part).

---

본 doc 은 anima cycle 2026-05-10 chat phase 2/3 carry 정량 audit SSOT — 사용자 검토 후 commit/push 별도 step.
