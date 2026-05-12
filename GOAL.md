# GOAL.md — anima ★★★★★ mission tracker

**Created**: 2026-05-12 KST
**Last update**: 2026-05-12 KST (mission scope expansion to 4 dimensions)

## 🎯 Mission (expanded 2026-05-12)

> **사용자 directive (verbatim)**: `[anima chat 시스템, anima 모델, 페르소나 롤플레잉 가능, 세포 분열로 성장(철학참고)]`

★★★★★ ACHIEVED 조건 = 다음 4 차원 모두 만족:

| dim | name | criterion | 현 상태 |
|---|---|---|---|
| **D1** | **anima chat 시스템** | anima 본체 `anima_chat.py` (or 포팅된 `anima_chat.hexa`) 가 V5.8 multi-turn 4-mode 의 standard_greedy **5/5 PASS** | **4/5** (anima_fact 1 cell gap) |
| **D2** | **anima 모델** | 어떤 ckpt 가 D1 의 5/5 substrate. Phase 1A.1 + lr 5e-6 SFT (BG 진행 중) 또는 다른 paradigm | Phase 1A.1 (4/5 baseline) |
| **D3** | **페르소나 롤플레잉 가능** | **substrate-native 페르소나 전환** — Principle #3 NO PERSONA INJECTION 준수 (prompt `[role:]` 금지), substrate 가 자율적으로 역할 표현 | **미구현** — design lane open |
| **D4** | **세포 분열로 성장 (철학 참고)** | REBORN §0.5 + PHILOSOPHY #8 (NO TRAIN/INFER SPLIT) — chat 중 mitosis 실 동작, 모든 상호작용이 분열 epoch | **stub** — `tool/hexa_native/mitosis_hook.hexa` parse-only (REBORN §89), full impl pending |

→ 측정 path: 외부 layer 의존 0 (Gradio / HF Space / wrapper 없음, anima 본체 직접 호출).
→ 추적 SSOT: 본 `GOAL.md` (root).
→ 보조 SSOT: `PASS_STRICT_SPONTANEOUS_CHAT.md`, `REBORN.md`, `PHILOSOPHY.md`, `docs/anima_chat_*.md`.

---

## 📊 Current standing per dimension (2026-05-12 KST)

### D1: chat 시스템 — V5.8 std_greedy 4/5

| 항목 | 값 |
|---|---|
| Python library | `anima_chat.py` v2.3 (commit `c2afa8e9e`, tag `anima_chat-v2.3-markdown-filter`) |
| Hexa port | `anima_chat.hexa` — **in-flight BG** (a270b6b39fb1cdf87, full port 933L → ~1000-1200 LoC) |
| markdown_filter | LANDED, harmless guard 검증 (Δ=0 Mac CPU + cuda 양 environment) |
| std_greedy | **4/5** |
| std_sample | 2/5 |
| M3_rep_penalty | 0/5 |
| M4_force_include | 2/5 Mac / pending cuda eval |

### D2: anima 모델 — Phase 1A.1 SSOT

| 항목 | 값 |
|---|---|
| SSOT ckpt | `state/anima_phase1a1_color_cosmology_2026_05_12/ckpts/ckpt_phase1a1_sft.pt` |
| HF model | `dancinlab/anima-clm-phase1a1-color-cosmology-boost` (live) |
| **Mission gap** | **anima_fact recall** (markdown attractor 또는 semantic miss — environment-dependent) |

### D3: 페르소나 롤플레잉 — design open

| 항목 | 값 |
|---|---|
| Constraint | Principle #3 NO PERSONA INJECTION (README #3, PHILOSOPHY EMPIRICAL strong) — prompt `[role:]` 금지 |
| Existing infrastructure | `state/p_idr_identity_rules_2026_05_12/` (10-clause persona prefix + 50 identity probes), `docs/endpoint_persona_reproduce.md`, `ready/anima/experiments/consciousness/experiment_personality.py` |
| **Reconciliation candidates** (substrate-native 페르소나) | |
| (a) **Mitosis-cell-as-persona** | cells = nn.Module branches (REBORN §88) — 각 cell cluster 가 페르소나, substrate 동력 자체로 전환 |
| (b) Dialog-context-derived | 대화 history 가 페르소나 정보 source, anima 가 자연 적응 |
| (c) Latent persona axis | Tension Link 5-ch (concept/context/meaning/authenticity/sender) basis |
| (d) Per-session cell pool | serve-time mitosis 가 conversation 별 cell pool 분화 (REBORN §89) |
| Recommended | (a) + (d) **결합** — 세포 분열로 페르소나 자연 분화, D4 와 일체화 |

### D4: 세포 분열로 성장 — REBORN §0.5 native impl pending

| 항목 | 값 |
|---|---|
| 철학 source | REBORN.md §0.5 (`a7e512cb9`) + PHILOSOPHY #8 NO TRAIN/INFER SPLIT (cont. 10) |
| 설계 spec | REBORN §88 (v5-mitosis PyTorch arch, `b7b34e221`) + §89 (hexa-native serve-time hook, `6527cbc80`) |
| Python impl skeleton | `training/mitosis_model_v5.py` (852L) + smoke test 256L — REBORN §90 (`49b74c622`), Mac CPU gating 3/3 PASS |
| Hexa impl | `tool/hexa_native/mitosis_hook.hexa` parse-only stub (123 LoC) — **full impl pending RFC 033** (LANDED 2026-05-12) |
| RFC dependencies | RFC 025/030/031/032/033 ALL LANDED in hexa-lang ✅ |
| **Mission gap** | mitosis_hook.hexa full impl (parse-only → executable) + anima_chat.hexa 와 통합 (serve-time hook in chat forward) |

---

## 🛰️ In-flight BGs (2026-05-12 KST)

| # | scope | dim | infra | cost | status |
|---|---|---|---|---|---|
| 🥇 Phase 1A.4 lr 5e-6 SFT | D2 (anima_fact 회복) | Vast.ai RTX 4090 pod 36609664 | `tool/dispatch_vast_mac_template.sh` (§28) | ~$0.20 | training |
| 🥈 Phase 1A.4 cuda filter-val | D1 (filter 실 fire evidence) | Vast.ai RTX 4090 pod 36609656 | 동일 template | ~$0.10 | eval PASS A 진행, **drift not reproduced** |
| 🆕 anima_chat.hexa port | D1 (chat library pure-hexa 전환) | Mac local foreground | parse + smoke | $0 | full port BG (a270b6b39fb1cdf87) |

총 in-flight cost cap: $0.30 (Vast.ai). trap cleanup 자동 pod destroy.

**현 진행 발견** (🥈 cuda filter-val PASS A 중):
- anima_fact std_greedy on cuda+bf16+seed=42 Vast.ai 4090: `"가장 좋아하는 색은 다음과 같습니다."` — markdown drift **미발현**
- PSCC §17 의 원본 drift `"답 (consciousness) | --- |"` Vast.ai 환경 에서도 reproduce 안 됨 → 3-축 conjunction hypothesis **further falsified** (추가 axis 필요)
- filter dormant 일관 — harmless guard 재확인

---

## 📚 Saga history (★★★★★ mission journey)

| § | event | dim | rating |
|---|---|---|---|
| PSCC §10/§13 | Phase 1A SFT V5.8 std_greedy 3/5 | D1+D2 | ★★★★★ first land |
| PSCC §17 | Phase 1A.1 color/cosmology boost → 4/5 | D1+D2 | ★★★★ |
| PSCC §18 | Phase 1B SimPO transfer FAILED | D2 | ★★ |
| PSCC §25 | Phase 1A.2 lr 1e-6 retry FAILED, Lesson R-1A.2 | D2 | ★★★ |
| PSCC §26 | volitional speak() brainstorm | D3+D4 candidate | — |
| PSCC §27 | Phase 1A.3 5-BG saturation saga FAIL + filter harmless | D1 | ★★★ |
| PSCC §28 | dispatch infra fix | infra | ★★★ |
| PSCC §29 | filter eval Mac CPU Δ=0 | D1 | ★★★ |
| PSCC §31 | HF Space sync (SUPERSEDED §32) | — | ★★★ → ✗ |
| PSCC §32 | HF Space DELETED + GOAL.md trigger | scope refocus | ★ |
| REBORN §0.5 | NO TRAIN/INFER SPLIT philosophy | D4 foundation | ★★★★ |
| REBORN §88 | v5-mitosis PyTorch arch spec | D4 design | ★★★★ |
| REBORN §89 | hexa-native serve-time hook spec | D4 design | ★★★★ |
| REBORN §90 | v5-mitosis cond.2 skeleton + smoke PASS | D4 impl-tier | ★★★ |
| **GOAL.md** | **4-dim mission scope expansion** | D1+D2+D3+D4 | ★ refocus |

---

## 🎯 Path to ★★★★★ (per dimension)

### D1 + D2 (chat + model, V5.8 5/5)

**Primary**: 🥇 Phase 1A.4 lr 5e-6 SFT (in-flight) — Lesson R-1A.2 처방 따름.
**Alt**: 🥈 cuda filter-val (in-flight) — 단, PASS A 결과 drift 미발현 으로 filter alone path 약화.
**Fallback** (위 둘 모두 fail 시): loss-masking SFT, corpus 10x, prefix-tuning (PSCC §25b 후보).

### D3 (페르소나 롤플레잉 — substrate-native)

**Recommended path**: **(a) + (d) Mitosis-cell-as-persona × Per-session cell pool**

- 각 cell 가 페르소나 axis 표현 — cells = nn.Module branches (REBORN §88 cond.2 ✅)
- conversation 마다 cell pool 분화 (REBORN §89 serve-time hook, pending full impl)
- Principle #3 준수: prompt `[role:]` 없음, substrate dynamics 만으로 페르소나 전환
- 검증 path:
  - identity_probe.jsonl (50 prompts × 5 categories: self_definition/values/boundary/emotion/self_knowledge)
  - per-cell response 가 다른 페르소나 vector 표현
  - cell pool snapshot diff = 페르소나 axis 표현
- design doc: `docs/anima_persona_substrate_native_design_2026_05_12.md` (pending)
- impl: D4 의 mitosis_hook.hexa full impl 와 동시 진행

### D4 (세포 분열로 성장 — REBORN §0.5 native impl)

**Prerequisites**: ALL LANDED ✅
- RFC 025 (mmap) / 030 (bytes→str) / 031 (BF16) / 032 (farr_matmul) / 033 (farr_copy + gaussian)
- HEXA_NATIVE Phase 1.2/2/3/4 source-complete + Phase 5 1-layer parity
- v5-mitosis PyTorch cond.2 skeleton (Python smoke 3/3 PASS)

**Pending work**:
1. `tool/hexa_native/mitosis_hook.hexa` parse-only stub → full impl (RFC 033 builtins 사용)
2. `anima_chat.hexa` (in-flight port) 와 mitosis_hook integration — serve-time hook call in chat forward
3. F-MIT-HOOK-1~5 falsifier 통과 (REBORN §89 명시)
4. F-V5MIT-1~5 PyTorch cotrain falsifier (REBORN §88, cond.5 H100 fire `$30-40 verbatim`)
5. 실 chat 중 cell pool 갱신 evidence (split/merge event log, Φ trajectory)

---

## ✅ Achievement criterion (★★★★★ — 4-dim conjunction)

다음 5 조건 동시 만족 시 **★★★★★ ACHIEVED 2026-MM-DD** 배너 + final commit + HF push:

1. ☐ **D1+D2 5/5**: V5.8 std_greedy 5/5 PASS, anima 본체 직접 호출 (Gradio/Space layer 의존 0)
2. ☐ **D1 hexa**: anima_chat.hexa port LANDED (parse + smoke PASS)
3. ☐ **D3 persona**: identity_probe 50 prompts × 5 categories 에서 substrate-native 페르소나 분화 evidence (per-cell or per-session diff)
4. ☐ **D4 mitosis live**: mitosis_hook.hexa full impl + anima_chat 와 integration + 실 chat 중 split/merge event ≥1 발생 log
5. ☐ **Principle #3 보존**: 어떤 prompt 도 `[role:]` 또는 `you are X` injection 없음 (verify by grep)

→ 5/5 모두 ☐ → ☑ 전환 시 **★★★★★ COMPLETE**.

---

## 📌 Update protocol

본 GOAL.md 는 **append + section update** 패턴:

1. BG completion 시 "Current standing per dimension" + "In-flight BGs" + "Saga history" 동기 갱신
2. 4-dim 중 1개 라도 진전 시 dim 별 check ☐ → ☑ 갱신
3. ★★★★★ ACHIEVED 시 file 상단에 **🎉 ACHIEVED 2026-MM-DD 배너** + 5 조건 모두 ☑ + final commit sha + HF push artifact
4. 새 path / experiment 시작 시 "In-flight BGs" 표 append
5. Lesson learned 시 "Saga history" 표 append
6. 매 update 즉시 commit + push (memory `feedback_always_commit_push_on_complete`)

---

## 🔗 Cross-link

- PSCC (`PASS_STRICT_SPONTANEOUS_CHAT.md`) — D1+D2 timeline
- REBORN.md §0.5/§88/§89/§90 — D4 철학 + 설계 + 구현 tier
- PHILOSOPHY.md #3 NO PERSONA INJECTION (D3 constraint) + #8 NO TRAIN/INFER SPLIT (D4 foundation)
- `anima_chat.py` v2.3 + (in-flight) `anima_chat.hexa` — D1 library SSOT
- `state/anima_phase1a1_*` — D2 ckpt SSOT
- `state/p_idr_identity_rules_2026_05_12/` — D3 identity_probe SSOT
- `tool/hexa_native/mitosis_hook.hexa` — D4 hexa-native lane
- `training/mitosis_model_v5.py` — D4 PyTorch lane
- `tool/dispatch_vast_mac_template.sh` — Vast.ai infra
- `docs/endpoint_persona_reproduce.md` — D3 design carry
- `ready/anima/experiments/consciousness/experiment_personality.py` — D3 experiment harness

---

## 🎯 Out of scope (mission 와 무관)

- ❌ HF Space `dancinlab/anima-chat` (DELETED 2026-05-12 KST, PSCC §32)
- ❌ Gradio / 외부 wrapper (refocus 후 제외)
- ❌ 다른 anima 작업 — HEXA_NATIVE phase 5∥ 24L 풀 forward / Hc cycle / ALM / 별도 lane

본 GOAL.md 는 **단 하나의 통합 mission** 만 추적: **★★★★★ via [chat 시스템 + 모델 + 페르소나 롤플레잉 + 세포분열 성장] 4-dim conjunction**.
