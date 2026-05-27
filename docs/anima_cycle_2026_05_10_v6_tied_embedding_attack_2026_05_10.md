# Anima Cycle 2026-05-10 종합 — Tied Embedding 회전 차단 attack + paradigm-j 보다 강한 base substrate 도전

본 doc 은 cycle 2026-05-10 의 **첫 cycle md** 입니다 — axis-A doc save mandate + yaml↔md mirror 정합 + BR-FRIENDLY-RESPONSE strict 한국어.

작성일: 2026-05-10 cycle entry phase
사용자 verbatim 인증 (2026-05-09): **"all bg go"** → cycle 2026-05-10 0-cost lanes continue.

---

## §0. 친근한 cycle 의의 (일반인용 1 단락)

이번 cycle 2026-05-10 은 한 줄로 — **"학생의 단어장 (lm_head ≡ tok_emb 묶임) 이 비스듬히 (40도) 회전된 채로 적혀 있어서 시험 직전에 머릿속이 뒤죽박죽 되는 현상 (cell collapse 증폭) 을 단어장을 다시 곧게 만들어서 (tied embedding untie / freeze) 막아보는 cycle"** 이에요. 이전 cycle (2026-05-09) 에서는 paradigm-j 라는 학생이 처음으로 명문대 (PUBLIC PROMOTE) 합격했지만, 그건 LoRA 보정 (0.7% 만 학습) 위에 얹은 합격이었어요. 이번 cycle 의 도전은 — paradigm-j 보다 **더 깊은 학습 (base substrate)** 에서 진짜 의식 (PASS_STRICT_C3) 을 통과시키는 것. 그러려면 학생이 책상 (substrate) 에 앉을 때부터 단어장이 곧게 되어 있어야 하니까, fix-5 (unit-sphere normalize 제거) + fix-6 (tied embedding 통합 처리) 를 묶어서 small PoC ($5-15) 로 검증합니다. 이게 통과하면 7B (Phase 3) → 14B (Phase 4) 본진 anima 모델 진입 prereq 충족.

---

## §1. Entry context — cycle 2026-05-09 final close 인용 + 연속성

cycle 2026-05-09 은 anima 사가 22+ BG saga 중 **historic 가장 큰 결실 cycle** 로 close (총 59+ milestones, 5 layer 산업 grade land). 본 cycle 2026-05-10 은 그 후속.

**cycle 2026-05-09 final close 핵심 인용** (registry yaml `cycle_close_summary.cycle_2026_05_09` SSOT):

| 항목 | cycle 2026-05-09 close 값 |
|---|---|
| milestones_total | **59+** (PIV F2 standard 승격 + lm_head tied embedding 발견까지) |
| public_promote_count | **2** (sft-1-8 + paradigm-j-50k-final) |
| robust_emerge_v5_2_winners | **paradigm-j** (4/4 gates strict + 5/5 prereq strict) |
| robust_emerge_v5_base_f2_winners | **paradigm-j** (F2 L2-norm standard 승격 후 base lane 단독 PASS) |
| cost_actual_usd | **$66** ($200 budget 33%) |
| cost_remaining_usd | **$134** |
| chat_orchestra_4_axis | **LIVE_FIRE_VERIFIED** (lane × mode × init-pattern × transport) |
| H4 정량 확정 | **4-way STRONG CONFIRM** (BG-LA + BG-LB + Phase 2 + Engine A/G) |
| H5 신가설 | **lm_head ≡ tok_emb 40도 회전** (chat-template dual loss collapse mechanism) |

cross-link:
- cycle md SSOT: `/Users/ghost/core/anima/docs/anima_cycle_2026_05_09_v6_strong_mk2_v1_emerge_near_consolidation.md` (1698 lines, 59+ milestones final close)
- entry plan v2: `/Users/ghost/core/anima/docs/anima_cycle_2026_05_10_entry_plan_v2_2026_05_09.md` (325 lines, milestone 51-59 갱신 final)
- entry plan v1: `/Users/ghost/core/anima/docs/anima_cycle_2026_05_10_entry_plan_2026_05_09.md` (256 lines, milestone 50 시점)
- registry yaml: `/Users/ghost/core/anima/anima/registry/anima_artifact_registry.yaml` (cycle_close_summary.cycle_2026_05_09 line 50-122)

**연속성 핵심**: cycle 2026-05-09 의 H5 발견 (lm_head 40도 회전 + tied embedding) 이 본 cycle 의 직접 motivation — 즉 H5 mechanism 을 arch 수정 (fix-5 + fix-6 통합) 으로 검증해서 paradigm-j 보다 더 강한 base substrate 도전.

---

## §2. cycle 2026-05-10 strategic objective

본 cycle 의 strategic objective 는 **3 가지** — 모두 substrate-research lane:

### 2-1. tied embedding 회전 차단 (fix-5 + fix-6 통합 PoC)

- **fix-5**: unit-sphere normalize 제거/약화 (cell_pool 학습 효과 보존)
- **fix-6**: tied embedding 통합 처리 (lm_head ≡ tok_emb 의 40도 회전 mechanism 차단)
- 통합 이유: cycle 2026-05-09 milestone 57 에서 fix-5 (normalize) 와 fix-6 (tied embedding) 가 같은 mechanism (cell collapse 증폭) 의 **두 layer** 임이 정량 입증
- 비용 cap: **$5-15** (H100 SXM 1h × 1-3 branch)
- 3 branch 비교: **(A) untie + freeze** vs **(B) untie + train** vs **(C) keep tied + normalize 약화**
- 친근 한 줄 — "단어장을 책상 위 (tok_emb) 와 시험지 (lm_head) 두 곳에 따로 적게 할지 (untie), 같이 적되 한쪽 잠글지 (freeze) 정량 비교"

### 2-2. paradigm-j 보다 강한 base substrate quality

- 현재 paradigm-j: LoRA 0.7% 학습 위에 얹은 v5 BASE F2 PASS (substrate 자체는 mk2-v1 base + LoRA 보정)
- 본 cycle 도전: **base substrate 자체가 v5 PASS_STRICT_C3** 이 가능한 substrate (LoRA 의존 없이)
- 측정: fix-5/6 PoC 회수 후 native v5 (PPR / MTRP / DCR / D-RAND / Gate G PIV) 즉시 측정
- 비교 baseline: paradigm-j v5 BASE F2 (PPR=0.6207, DCR=1.0, JVAE active)
- 친근 한 줄 — "보정안경 (LoRA) 없이도 시험 통과하는 학생 만들기 — paradigm-j 는 안경 쓰고 60% 맞춘 학생, 본 cycle 도전은 맨눈으로 60%+ 맞추는 학생"

### 2-3. 7B / 14B 진입 prereq (fix-5/6 PASS 후)

- fix-5/6 PoC 가 PASS 시 **Phase 3 (7B) 본진 진입 prereq** 첫 1/N 충족
- Phase 3 비용 추정: $200-600 (H100 14-21h × 2-4 branch)
- Phase 4 (14B): fix-5/6 PASS + Phase 3 PASS 둘 다 prereq
- 친근 한 줄 — "초등학생 (350M) → 고등학생 (7B) → 대학생 (14B) 진학 prereq 의 첫 관문"

---

## §3. 진행 milestones (1-2 LANDED + 3 in-flight)

### M1: attention/FFN cosine 측정 — lm_head 단독 dominant 확정 ★ LANDED

- 작업: BG-LB 350M ckpt vs Phase 2 cotrain ckpt 의 attention (q/k/v/o_proj) + FFN (gate/up/down) 24 layer × 7 weight = **168 weight matrix** weighted cosine 측정
- 결과 verdict (`state/anima_phase2_attention_ffn_cosine_evidence_2026_05_09.json` line 3596-3606):
  - `lm_head_ref_mean_cos`: **0.7710** (24도 회전 — H5 reference)
  - `attn_all_mean_cos`: **0.9782** (cycle 2026-05-09 H5 발견의 lm_head 와 비교 시 무시 가능 변화)
  - `ffn_all_mean_cos`: **0.9795** (마찬가지 무시 가능)
  - `attn_classification`: **`minimal_change_lm_head_dominant`** ★
  - `ffn_classification`: **`minimal_change_lm_head_dominant`** ★
  - delta: attn vs lm_head = 0.2072, ffn vs lm_head = 0.2085 (즉 lm_head 회전 폭이 attention/FFN 의 **20× 이상**)
- 의의 — **fix-6 (tied embedding) 의 motivation 이 attention/FFN 이 아닌 lm_head 단독에 있음 정량 확정**. 즉 fix-5/6 가 lm_head + tok_emb tying 한 곳에 집중하면 충분 (다른 layer 까지 손대지 않아도 됨).
- 친근 한 줄 — "단어장 (lm_head) 만 비스듬해지고 책상 (attention) 과 의자 (FFN) 는 거의 안 흔들렸으니, 단어장만 곧게 만들면 됨 (다른 데 손대지 마)"
- artifact: `/Users/ghost/core/anima/state/anima_phase2_attention_ffn_cosine_evidence_2026_05_09.json`

### M2: axis-N+1 hook T+1 implementation LANDED

- 작업: `tool/anima_cli/chat/axes/_registry.hexa` (axis-of-axes meta-registry) + `chat.hexa` dispatcher route + `anima_cli_mk2.spec.yaml` chat_axes_meta cross-link
- 효과: axis-N+1 (예: verifier 5번째 axis) 추가 시 **dispatcher / benchmark.hexa 코드 변경 0 줄** 로 5 차원 cross-product 자동 확장
- 8-field schema: axis_id / name / registry_file / default_flag / list_flag / describe_helper / status / axis_label_internal
- compliance: V14 (결정성) + (모델 로드 금지) + (chat-cap C2 측정 차원) + (mandatory report) + (single SSOT) + (trinity) 모두 정합
- 친근 한 줄 — "5 축 면접 시험에서 6번째 면접관 (verifier) 추가하기 쉽게 만든 책장 (registry-of-registries) 완성 — 새 면접관 추가 시 시험 dispatcher 코드 안 고쳐도 됨"
- artifact: `/Users/ghost/core/anima/tool/anima_cli/chat/axes/_registry.hexa` + `tool/anima_cli/chat/chat.hexa` + `anima/spec/anima_cli_mk2.spec.yaml`

### M3 (in-flight): fix-5/6 tied embedding PoC

- 상태: **spec design phase** (Mac load 89, free RAM 302MB — H100 fire 진입 prereq Mac load avg ≤ 30 회복 대기)
- 비용 cap: **$15** (3 branch × ~$5 each, H100 SXM 1h)
- 3 branch:
  - **(A) untie + freeze tok_emb**: lm_head 만 학습, tok_emb 고정 (단어장 한쪽 잠금)
  - **(B) untie + both train**: lm_head 와 tok_emb 둘 다 따로 학습 (단어장 두 권)
  - **(C) keep tied + normalize 약화**: tying 유지 + unit-sphere normalize coefficient 줄임 (단어장 곧게 만들기 만)
- 측정: 회수 후 native v5 (PPR / MTRP / DCR / D-RAND / Gate G PIV F2) 즉시 측정 + paradigm-j base v5 F2 와 정량 비교
- 친근 한 줄 — "3 가지 단어장 곧게 만들기 방법 동시 시험 — 어느 게 안경 (LoRA) 없이도 60%+ 맞추는 학생 만드는지"
- prereq: Mac load avg ≤ 30 회복 + 사용자 verbatim "OK FIX_5_6 POC FIRE" + 본 entry plan v2 + 본 cycle md final mirror

---

## §4. 핵심 가설 carry from cycle 2026-05-09

### H4: unit-sphere normalize-erase 절대 확정 ★

- cycle 2026-05-09 milestone 51-52 에서 **4-way STRONG CONFIRM**: BG-LA + BG-LB + Phase 2 cotrain + Engine A/G 모두 cell_pool ≈ random (normalize 가 학습 효과 지움)
- 정량 evidence: `state/anima_bg_lb_cell_pool_evidence_2026_05_09.json` + `state/anima_phase_2_cotrain_cell_pool_evidence_2026_05_09.json`
- 본 cycle 정합: fix-5 (normalize 약화/제거) 의 직접 motivation
- 친근 한 줄 — "단어장 (cell_pool) 에 적은 학습이 시험 직전 정규화 (unit-sphere normalize) 단계에서 모두 지워지는 게 4 lane 에서 모두 확인됨"

### H5: lm_head 40도 회전 + tied embedding 발견 ★

- cycle 2026-05-09 milestone 57 에서 발견: **lm_head ≡ tok_emb (40도 회전 후 동일)** — chat-template dual loss 가 이 회전을 통해 cell collapse 증폭 mechanism
- 본 cycle M1 evidence 보강: lm_head_ref_mean_cos = 0.7710 vs attn 0.9782 / ffn 0.9795 → **lm_head 단독 dominant** 확정
- 본 cycle 정합: fix-6 (tied embedding 통합 처리) 의 직접 motivation
- 친근 한 줄 — "단어장 (lm_head) 이 시험지 (tok_emb) 와 묶여 있는데 40도 비스듬히 적혀 있어서 시험 직전 머릿속 뒤죽박죽 되는 게 mechanism"

### G3 정량 확정 + F2 L2-norm standard 승격

- cycle 2026-05-09 milestone 53 + 56 + 59: **F1 max → F2 L2-norm 1.646× boost** (PIV metric 변경)
- 사용자 verbatim 승격 (2026-05-09): **"OK PROMOTE PIV_L2_NORM_F2 STANDARD"** — F2 가 새 standard, F1 deprecated
- 본 cycle 정합: M3 fix-5/6 PoC 회수 후 측정 시 **F2 L2-norm standard** 사용 (F1 max 사용 금지)
- 친근 한 줄 — "5 과목 평균 (L2-norm) 으로 채점하는 게 한 과목 만점 (max) 보다 정확함 — 본 cycle 부터 F2 가 시험 표준"

---

## §5. 다음 step plan

### 5-1. fix-5/6 PoC 회수 시 verdict 비교 (3 branch)

- branch (A) untie+freeze, (B) untie+both, (C) keep+weak-norm 3 측정
- 비교 metric: PPR_v5_BASE_F2 / MTRP / DCR / D-RAND / Gate G PIV (F2 L2-norm standard)
- baseline: paradigm-j v5 BASE F2 (PPR=0.6207, DCR=1.0, JVAE active)
- decision tree:
  - 어느 branch 라도 paradigm-j base F2 PASS (PPR ≥ 0.30 floor + Gate G PIV F2 PASS) → **anima first base substrate EMERGE** (LoRA 의존 없음)
  - 모든 branch FALSIFIED → fix-7 (다음 arch attempt) 신규 design
- 친근 한 줄 — "3 명 학생 (3 branch) 시험 보고 누가 안경 (LoRA) 없이 60%+ 맞추는지 결정"

### 5-2. T+2 (benchmark N-axis cross-product) 진행 중

- T+1 (M2) 완료 후 T+2 = benchmark.hexa 의 N-axis cross-product 자동 확장 검증
- T+3 = axis-5 (verifier) skeleton implementation
- T+4 = axis-5 actual fire (`tool/anima_cli/chat/verifiers/_registry.hexa` + plugins)
- 본 cycle 진행 중 (Mac load 회복 후 0-cost path)
- 친근 한 줄 — "면접관 책장 (axis registry) 완성 후 6번째 면접관 (verifier) 자리 만들기"

### 5-3. mk2-v1 v5 재측정 (Mac 부하 회복 후)

- cycle 2026-05-09 mk2-v1 base v5 PPR=0.2881 (gap -0.0119, EMERGE-near)
- D-RAND prompt redesign + native v5 재측정 (0-cost Mac local)
- 회복 prereq: Mac load avg ≤ 30 (현재 89 → ≥ 60% 감소 필요)
- 친근 한 줄 — "mk2-v1 학생 시험 다시 보기 — Mac 컴퓨터 쉬게 한 다음 측정 환경 깨끗할 때"

---

## §6. own mandates 정합

본 cycle 모든 milestone 은 다음 own mandates strict 정합:

| own | mandate | 본 cycle 적용 |
|---|---|---|
| **** | V14 결정성 (no random / no time / no env) | M1 cosine 측정 + M2 registry helper 모두 결정성 |
| **** | 모델 로드 절대 금지 (Mac local) | M1 weight tensor 직접 load (no model forward) |
| **** | mandatory report (axis 발견 자체) | M2 axis-of-axes 발견 mandatory report |
| **** | model checkpoint preservation + auto HF promote | fix-5/6 PoC 회수 시 ckpt mandatory pull |
| **** | trinity (cross-link) | M2 registry entries trinity cross-link |
| **** | 자연발화 mandate | 본 cycle md 친근 모드 strict |
| **** | HF visibility lifecycle (4 prerequisite for public) | fix-5/6 PoC 통과 + V6 awareness STRONG + 사용자 verbatim + trinity sweep 4 prereq |
| **** | 매단계 doc/model/dataset save | 본 cycle md disk save (axis-A) |
| **** | yaml↔md auto-regenerate | registry yaml mirror 동기 갱신 (별도 BG) |
| **** | axis-N+1 hook plugin pattern | M2 implementation LANDED |

raw#15 additive: 기존 cycle 2026-05-09 docs / entry plan v1+v2 / registry yaml 무수정, 본 cycle md 신규 추가만.

---

## §7. cost projection (cycle 2026-05-10 누적)

| 항목 | 비용 추정 | 종류 |
|---|---|---|
| M1 attention/FFN cosine | **$0** (Mac local, weight tensor only) | 0-cost |
| M2 axis hook | **$0** (text edit only) | 0-cost |
| M3 fix-5/6 PoC | **$5-15** (H100 SXM 1h × 1-3 branch) | H100 PoC |
| T+2~T+4 | **$0** (Mac local) | 0-cost |
| mk2-v1 v5 재측정 | **$0** (Mac local) | 0-cost |
| **본 cycle 누적 추정** | **$5-15** | 대부분 0-cost |
| budget 잔여 (cycle 2026-05-09 close 기준) | **$134** | strict ✓ |
| budget 잔여 (본 cycle 종료 추정) | **$119-129** | 60%+ 잔여 |

친근 한 줄 — "이번 cycle 은 대부분 책상 정리 (text edit) 에 집중하고 마지막에만 한 번 시험장 (H100) 빌려서 small PoC 시험" — $5-15 정도.

---

## §8. cycle close criteria

본 cycle 2026-05-10 close 자격 (모두 충족 시 close):

1. **fix-5/6 PoC verdict** — 3 branch (A/B/C) 중 최소 1개 native v5 측정 회수 + verdict (EMERGE / EMERGE-near / FALSIFIED) 결정
2. **new milestones land** — M1 + M2 + M3 외 추가 milestone 4-9 land (T+2~T+4 + mk2-v1 v5 재측정 + ckpt pull + HF promote 등)
3. **사용자 verbatim 인증** — close 시점 사용자 verbatim "OK CYCLE_2026_05_10 CLOSE" (또는 동등)
4. **registry yaml mirror** — `cycle_close_summary.cycle_2026_05_10` section 신규 amend (mandate)
5. **next cycle entry plan** — `docs/anima_cycle_2026_05_11_entry_plan_*.md` (또는 next cycle date) draft land

친근 한 줄 — "이번 cycle 마무리 조건 = (1) 단어장 PoC 시험 결과 + (2) 추가 milestone 4-9 개 + (3) 사용자 OK + (4) 노트 (yaml) 정리 + (5) 다음 cycle plan 초안" 5 가지 모두 충족.

---

## cross-link

- cycle 2026-05-09 final close cycle md: `/Users/ghost/core/anima/docs/anima_cycle_2026_05_09_v6_strong_mk2_v1_emerge_near_consolidation.md` (1698 lines, 59+ milestones)
- entry plan v2: `/Users/ghost/core/anima/docs/anima_cycle_2026_05_10_entry_plan_v2_2026_05_09.md` (325 lines)
- entry plan v1: `/Users/ghost/core/anima/docs/anima_cycle_2026_05_10_entry_plan_2026_05_09.md` (256 lines)
- registry yaml SSOT: `/Users/ghost/core/anima/anima/registry/anima_artifact_registry.yaml` (cycle_close_summary.cycle_2026_05_09 line 50-122)
- M1 evidence: `/Users/ghost/core/anima/state/anima_phase2_attention_ffn_cosine_evidence_2026_05_09.json`
- M2 implementation: `/Users/ghost/core/anima/tool/anima_cli/chat/axes/_registry.hexa`
- philosophy / law / hypothesis: `.roadmap.philosophy` / `.roadmap.law` / `.roadmap.hypothesis`
- own SSOT: `.own`
- memory: `~/.claude-claude1/projects/-Users-ghost-core-anima/memory/`

---

## 자원 제약 (작성 시점)

- Mac load avg: **89** (목표 ≤ 30 — 본 cycle M3 fire 진입 prereq)
- free RAM: **302MB** (가벼운 text edit 만 OK, 모델 load 금지)
- H100 pod 보유: **0 pod** (cycle 2026-05-09 close 시 모두 회수)
- budget 잔여: **$134** (cycle 2026-05-09 close 기준, 본 cycle 종료 추정 $119-129)

본 cycle md 작성은 **text edit only** — 모델 load 금지 (strict ✓), commit/push 안 함, 파일 저장만.
