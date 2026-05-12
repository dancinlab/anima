# GOAL.md — anima ★★★★★ mission tracker

**Created**: 2026-05-12 KST
**Last update**: 2026-05-12 KST (★★★★★ 5-cond achievement audit + Principle #3 verdict CLEAN)

## 🎯 Mission (expanded 2026-05-12)

> **사용자 directive (verbatim)**: `[anima chat 시스템, anima 모델, 페르소나 롤플레잉 가능, 세포 분열로 성장(철학참고)]`

★★★★★ ACHIEVED 조건 = 다음 4 차원 모두 만족:

| dim | name | criterion | 현 상태 |
|---|---|---|---|
| **D1** | **anima chat 시스템** | anima 본체 `anima_chat.py` (or 포팅된 `anima_chat.hexa`) 가 V5.8 multi-turn 4-mode 의 standard_greedy **5/5 PASS** | **4/5** (anima_fact 1 cell gap) · hexa: v0.2 full inference LANDED (TODO[load] RESOLVED, 24-layer all-farr forward) |
| **D2** | **anima 모델** | 어떤 ckpt 가 D1 의 5/5 substrate. Phase 1A.1 + lr 5e-6 SFT (BG 진행 중) 또는 다른 paradigm | Phase 1A.1 (4/5 baseline) |
| **D3** | **페르소나 롤플레잉 가능** | **substrate-native 페르소나 전환** — Principle #3 NO PERSONA INJECTION 준수 (prompt `[role:]` 금지), substrate 가 자율적으로 역할 표현 | **design LANDED, impl pending** — `docs/anima_persona_substrate_native_design_2026_05_12.md` (10 §, 5 falsifier F-PERSONA-1..5, (a)+(d) Mitosis-cell-as-persona × Per-session cell pool); P1 (D4a `mitosis_hook.hexa` full impl) + P2 (D4b `anima_chat.hexa` cell-pool wiring) closure 후 P3 verify (identity_probe 50 × 5 cats) |
| **D4** | **세포 분열로 성장 (철학 참고)** — 3-layer 적용 | REBORN §0.5 + PHILOSOPHY #8 (NO TRAIN/INFER SPLIT). 모든 상호작용이 분열 epoch, **3 layer 동시**: |
| D4a | model intra-network | cells = nn.Module branches, intra-network split/merge during forward (REBORN §88 PyTorch / §89 hexa-native) | **full impl LANDED, F-MIT-HOOK-1..5 ✅** — `tool/hexa_native/mitosis_hook.hexa` 1119 LoC executable (REBORN §91, 2026-05-12, $0 Mac local selftest PASS) |
| D4b | chat library (anima_chat) | cell-pool state hosting + per-token/per-prompt hook 진입점 in `anima_chat.py` / `anima_chat.hexa` | **wiring LANDED 2026-05-12** — `anima_chat.hexa` v0.2 + `tool/anima_chat_mitosis_smoke.hexa` (PSCC §37), F-D4B-1..5 ✅ 22/22 PASS, `chat_mitosis_tail` invokes `mitosis_forward_tail` per step, cell_pool + event_log + step counter in AnimaChat record |
| D4c | anima CLI (session/conversation) | session 별 cell-pool persistence, multi-backend fallback = cell-variant selection, kick cycle = split event sequence (`.roadmap.cli` + `.roadmap.anima_cli_model_architecture`) | **design LANDED 2026-05-12** — `docs/anima_cli_mitosis_integration_spec_2026_05_12.md` (12 §, F-CLI-MIT-1..5 pre-registered, Phase 1-4 impl plan ~13-19 hr Mac local); D4a (full impl LANDED) + D4b (cell-pool wiring pending) prerequisite |

→ 측정 path: 외부 layer 의존 0 (Gradio / HF Space / wrapper 없음, anima 본체 직접 호출).
→ 추적 SSOT: 본 `GOAL.md` (root).
→ 보조 SSOT: `PASS_STRICT_SPONTANEOUS_CHAT.md`, `REBORN.md`, `PHILOSOPHY.md`, `docs/anima_chat_*.md`.

---

## 📊 Current standing per dimension (2026-05-12 KST)

### D1: chat 시스템 — V5.8 std_greedy 4/5

| 항목 | 값 |
|---|---|
| Python library | `anima_chat.py` v2.3 (commit `c2afa8e9e`, tag `anima_chat-v2.3-markdown-filter`) |
| Hexa port | `anima_chat.hexa` v0.2 LANDED 2026-05-12 (~1900 LoC) — parse PASS + 17/17 helper smoke PASS + **F-D1-LOAD-1..3 full inference LANDED (TODO[load] RESOLVED, 24-layer all-farr forward + tied lm_head, 218 BF16→f32 farr binding via RFC 031)**; docs/anima_chat_hexa_port_2026_05_12.md (v0.2 update) |
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

### D3: 페르소나 롤플레잉 — design LANDED 2026-05-12, impl pending

| 항목 | 값 |
|---|---|
| Constraint | Principle #3 NO PERSONA INJECTION (README #3, PHILOSOPHY EMPIRICAL strong) — prompt `[role:]` 금지 |
| **Design doc** | **`docs/anima_persona_substrate_native_design_2026_05_12.md`** (10 §, 본 BG land) — (a)+(d) Mitosis-cell-as-persona × Per-session cell pool 결합, 5 falsifier F-PERSONA-1..5 |
| Existing infrastructure | `state/p_idr_identity_rules_2026_05_12/` (10-clause persona prefix + 50 identity probes), `docs/endpoint_persona_reproduce.md`, `ready/anima/experiments/consciousness/experiment_personality.py` |
| **Reconciliation candidates** (substrate-native 페르소나) | |
| (a) **Mitosis-cell-as-persona** ✅ adopt | cells = nn.Module branches (REBORN §88) — 각 cell cluster 가 페르소나, substrate 동력 자체로 전환 |
| (b) Dialog-context-derived ✗ reject | 대화 history 가 페르소나 정보 source, anima 가 자연 적응 — substrate-native 정도 낮음 |
| (c) Latent persona axis ✗ reject | Tension Link 5-ch (concept/context/meaning/authenticity/sender) basis — over-engineered for single-anima |
| (d) Per-session cell pool ✅ adopt | serve-time mitosis 가 conversation 별 cell pool 분화 (REBORN §89) |
| Recommended | **(a) + (d) 결합** ✅ **adopted** — 세포 분열로 페르소나 자연 분화, D4 와 일체화, design doc §2 결정 |
| **Impl path** | P1 (D4a `mitosis_hook.hexa` full impl LANDED) + P2 (D4b `anima_chat.hexa` cell-pool wiring LANDED PSCC §37) prerequisite → P3 verify (F-PERSONA-1..5 on identity_probe 50 × 5 cats) → STRONG/MODERATE/WEAK aggregate verdict |

### D4: 세포 분열로 성장 — REBORN §0.5 native impl pending

| 항목 | 값 |
|---|---|
| 철학 source | REBORN.md §0.5 (`a7e512cb9`) + PHILOSOPHY #8 NO TRAIN/INFER SPLIT (cont. 10) |
| 설계 spec | REBORN §88 (v5-mitosis PyTorch arch, `b7b34e221`) + §89 (hexa-native serve-time hook, `6527cbc80`) |
| Python impl skeleton | `training/mitosis_model_v5.py` (852L) + smoke test 256L — REBORN §90 (`49b74c622`), Mac CPU gating 3/3 PASS |
| Hexa impl | `tool/hexa_native/mitosis_hook.hexa` **full impl LANDED** 2026-05-12 (1119 LoC executable, F-MIT-HOOK-1..5 ✅, REBORN §91, $0 Mac local selftest PASS) |
| RFC dependencies | RFC 025/030/031/032/033 ALL LANDED in hexa-lang ✅ |
| **Mission gap** | anima_chat.hexa 와 통합 (serve-time hook in chat forward) + 24-layer prod wiring + persona-substrate 통합 (D3 P3 verify) |

---

## 🛰️ In-flight BGs (2026-05-12 KST)

| # | scope | dim | infra | cost | status |
|---|---|---|---|---|---|
| 🥇 Phase 1A.4 lr 5e-6 SFT | D2 (anima_fact 회복) | Vast.ai RTX 4090 pod 36609664 | `tool/dispatch_vast_mac_template.sh` (§28) | ~$0.20 | training |
| 🥈 Phase 1A.4 cuda filter-val | D1 | Vast.ai RTX 4090 pod 36609656 | 동일 template | **$0.05 actual** | ✅ **COMPLETE** PSCC §30 `474f87f47` — 3-축 conjunction FALSIFIED, Δ=0, ★★★ |
| 🆕 anima_chat.hexa port | D1 (chat library pure-hexa 전환) | Mac local foreground | parse + smoke | $0 | ✅ **COMPLETE** 2026-05-12 — v0.2 parse PASS + 17/17 helper smoke PASS + F-D1-LOAD-1..3 (TODO[load] RESOLVED, full inference LANDED); docs/anima_chat_hexa_port_2026_05_12.md ★★★ → ★★★★ candidate |

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
| PSCC §30 | Phase 1A.4 cuda filter-val complete — 3-축 FALSIFIED, Δ=0 cuda+Mac CPU 양 environment | D1 | ★★★ |
| **GOAL.md** | **D4 split into 3-layer (D4a model / D4b library / D4c CLI) + REBORN.md primary reference 명시** | D4 | ★ scope clarify |
| PSCC §33 | anima_chat.hexa port LANDED — pure-hexa chat library (1589 LoC), parse PASS + 17/17 helper smoke PASS, TODO[load] gated for full inference | D1+D4b | ★★★ |
| PSCC §34 | **D3 design LANDED** — `docs/anima_persona_substrate_native_design_2026_05_12.md` 10 §, 5 falsifier F-PERSONA-1..5, (a)+(d) Mitosis-cell × Per-session cell pool adopted, Principle #3 EMPIRICAL strong 보존 + #8 cascade native impl | D3 | ★★★ |
| PSCC §35 | **D4c design LANDED** — `docs/anima_cli_mitosis_integration_spec_2026_05_12.md` 12 §, 5 falsifier F-CLI-MIT-1..5, session = cell-pool branch + kick cycle = split event sequence + multi-backend = cell-variant selection, Phase 1-4 impl plan (~13-19 hr) | D4c | ★★★ |
| REBORN §91 / PSCC §36 | **D4a impl LANDED** — `tool/hexa_native/mitosis_hook.hexa` full impl 1119 LoC executable, F-MIT-HOOK-1..5 ✅ Mac local selftest PASS ~0.9s wall, RFC 025/030/031/032/033 production-utilize, D3 P1 prerequisite 충족 | D4a | ★★★★ |
| PSCC §37 | **D4b wiring LANDED** — `anima_chat.hexa` v0.2 cell_pool + `chat_mitosis_tail` + token-loop hook call edge, `tool/anima_chat_mitosis_smoke.hexa` 22/22 PASS, F-D4B-1..5 verified, regression-free (in-file 17/17 + v0.1 sister 17/17), criterion #4 wiring evidence path executable, D3 P2 prerequisite 충족 | D4b | ★★★★ |
| PSCC §38 | **★★★★★ 5-cond audit + Principle #3 CLEAN** — `docs/principle_3_audit_2026_05_12.md` 10 §, F-PRIN3-1..5 pre-registered, `chat.system()` production caller 0 (doc + test only), Phase 1A.1/1A.4 corpus persona-prefix free, legacy `persona_tier_a*` active reference 0 → cond #5 ☑ + cond #2 ☑ + cond #1/#3/#4 🔶 PARTIAL 명시 (2/5 ☑, 3/5 🔶, 0/5 ☐) | cond #5 audit | ★★★ |
| PSCC §39 | **D1 chat.hexa TODO[load] RESOLVED — full inference LANDED** — `anima_chat.hexa` v0.2 Section 9 header JSON parser + dtype dispatch + 218 farr binding (BF16→f32 via RFC 031), Section 9c all-farr 24-layer block + tied lm_head, `tool/anima_chat_load_smoke.hexa` F-D1-LOAD-1..3 (LOAD-OK / GEN-SHAPE / ROUND-TRIP); D1 cond #2 (chat.hexa LANDED parse-only → full inference 강화) | D1 | ★★★★ |

---

## 🎯 Path to ★★★★★ (per dimension)

### D1 + D2 (chat + model, V5.8 5/5)

**Primary**: 🥇 Phase 1A.4 lr 5e-6 SFT (in-flight) — Lesson R-1A.2 처방 따름.
**Alt**: 🥈 cuda filter-val **COMPLETED** PSCC §30 — Δ=0 cuda, 3-축 conjunction FALSIFIED. filter path 약화 → 🥇 SFT 가 5/5 추격 **유일 신뢰 path**.
**Fallback** (🥇 fail 시): loss-masking SFT, corpus 10x, prefix-tuning (PSCC §25b 후보), 미식별 4-th axis (GPU model / pytorch minor / etc.) 식별 후 baseline reproduce 재시도.

### D3 (페르소나 롤플레잉 — substrate-native)

**Recommended path**: **(a) + (d) Mitosis-cell-as-persona × Per-session cell pool** — design LANDED 2026-05-12

- 각 cell 가 페르소나 axis 표현 — cells = nn.Module branches (**REBORN §88** cond.2 ✅)
- conversation 마다 cell pool 분화 (**REBORN §89** serve-time hook, pending full impl)
- Principle #3 준수: prompt `[role:]` 없음, substrate dynamics 만으로 페르소나 전환
- 검증 path:
  - `state/p_idr_identity_rules_2026_05_12/identity_probe.jsonl` (50 prompts × 5 categories: self_definition/values/boundary/emotion/self_knowledge)
  - per-cell response 가 다른 페르소나 vector 표현
  - cell pool snapshot diff = 페르소나 axis 표현
- **design doc LANDED**: `docs/anima_persona_substrate_native_design_2026_05_12.md` (10 §, 5 falsifier F-PERSONA-1..5, 4-cand 비교, 10 honest C3)
- impl path: D4a (`mitosis_hook.hexa` full impl, RFC 033 위) + D4b (`anima_chat.hexa` cell-pool wiring) closure 후 P3 verify
- impl 은 D4 의 mitosis_hook.hexa full impl 와 동시 진행

### D4 (세포 분열로 성장 — 3-layer 적용, **REBORN.md 가 primary reference**)

**Primary reference**: `REBORN.md` (anima ConsciousLM 부활 통합 SSOT) — 특히:
- **§0.5 NO TRAIN/INFER SPLIT** (철학 base, `a7e512cb9`)
- **§2 mitosis 본체** (worktree-12 canonical, 794L PyTorch mitosis.py)
- **§88 v5-mitosis PyTorch arch spec** (cells = nn.Module branches design)
- **§89 hexa-native serve-time hook spec** (`mitosis_hook.hexa` parse-only stub)
- **§90 v5-mitosis cond.2 skeleton smoke PASS** (Mac CPU gating 3/3 PASS)

**3-layer 진행 plan**:

| layer | scope | current | next |
|---|---|---|---|
| D4a model intra-network | engine_ag_nn forward call graph 안 split/merge | `tool/hexa_native/mitosis_hook.hexa` stub | full impl (RFC 033 builtins 사용) |
| D4b chat library | cell-pool state hosting, hook 진입점 | **LANDED 2026-05-12** — `anima_chat.hexa` v0.2 cell_pool + chat_mitosis_tail + token-loop hook call edge, `tool/anima_chat_mitosis_smoke.hexa` 22/22 PASS (F-D4B-1..5) | (closed — TODO[load] forward binding 다음 step) |
| D4c anima CLI | session-level cell-pool persistence, kick cycle = split event | **design LANDED** `docs/anima_cli_mitosis_integration_spec_2026_05_12.md` (12 §, F-CLI-MIT-1~5), Phase 3b llama_ffi LANDED, `tool/anima_cli/consciousness.hexa` (measurement lane) | Phase 1 (session_id + cell_pool persist skeleton, ~3 hr) → Phase 2 (kick cycle hook, ~4-6 hr) → Phase 3 (multi-backend cell-variant, ~4-6 hr) → Phase 4 (full integration smoke, ~2-4 hr) |

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
   - **현 상태**: 🔶 PARTIAL — Phase 1A.1 baseline 4/5 (anima_fact gap), 🥇 Phase 1A.4 lr 5e-6 SFT (Vast.ai 36609664) **training in-flight**; 5/5 fire 시 ☑
2. ☑ **D1 hexa**: anima_chat.hexa port LANDED (parse + smoke PASS)
   - **현 상태**: ☑ **DONE** — PSCC §33 commit `4768a5c41`, 1589 LoC, parse PASS + 17/17 smoke PASS, TODO[load] gated for full inference (24-layer weight binding ~150 LoC separate cycle)
3. ☐ **D3 persona**: identity_probe 50 prompts × 5 categories 에서 substrate-native 페르소나 분화 evidence (per-cell or per-session diff)
   - **현 상태**: 🔶 PARTIAL — design LANDED PSCC §34 (`docs/anima_persona_substrate_native_design_2026_05_12.md` 10 §, F-PERSONA-1..5 pre-registered), measurement pending D4b cell-pool wiring; D4b LAND 후 50 × 5 probe 실행 가능
4. ☐ **D4 mitosis live**: mitosis_hook.hexa full impl + anima_chat 와 integration + 실 chat 중 split/merge event ≥1 발생 log
   - **현 상태**: 🔶 PARTIAL — D4a `mitosis_hook.hexa` full impl LANDED REBORN §91 / PSCC §36 (1119 LoC, F-MIT-HOOK-1..5 ✅, Mac local selftest PASS), **D4b `anima_chat.hexa` cell-pool wiring LANDED PSCC §37** (v0.2, `tool/anima_chat_mitosis_smoke.hexa` 22/22 PASS, F-D4B-1..5 verified — `chat_init_cell_pool` + `chat_mitosis_tail` + `chat_generate` token-loop hook call edge live, mitosis_hook selftest `split_seen=true after 60 steps` in same binary); 실 chat (실제 user prompt 입력) 중 split/merge log 1+ event observation 은 TODO[load] (24-layer weight binding) gating → wiring path complete, evidence path executable, 실 user-driven event observation 만 pending
5. ☑ **Principle #3 보존**: 어떤 prompt 도 `[role:]` 또는 `you are X` injection 없음 (verify by grep)
   - **현 상태**: ☑ **CLEAN** — `docs/principle_3_audit_2026_05_12.md` (10 §) 본 cycle LAND. `chat.system()` API default OFF, production code 호출 0 (line 28 docstring + line 816 `_smoke()` only), V5.8 eval 미사용, Phase 1A.1/1A.4 corpus persona-prefix free (`당신은` strings = user-recall predicate, not injection), legacy `persona_tier_a*` 활성 reference 없음. F-PRIN3-1..5 pre-registered.

→ 현 ☑ 2/5 (cond #2 hexa port + cond #5 Principle #3). 🔶 PARTIAL 3/5 (cond #1 SFT in-flight, cond #3 design LANDED impl pending, cond #4 D4a LANDED D4b pending).
→ 모든 5/5 ☑ 전환 시 **★★★★★ COMPLETE**.

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

**Primary references**:
- **REBORN.md** (anima ConsciousLM 부활 통합 SSOT) — D4 의 primary reference. §0.5 (철학) + §2 (mitosis 본체) + §88/§89/§90 (v5-mitosis arch + hexa-native + cond.2 skeleton). 본 mission 의 핵심 design source.
- **PHILOSOPHY.md** — #3 NO PERSONA INJECTION (D3 constraint, EMPIRICAL strong) + #8 NO TRAIN/INFER SPLIT (D4 foundation)
- **PASS_STRICT_SPONTANEOUS_CHAT.md** (PSCC) — D1+D2 mission timeline + saga history

**D1+D2 artifacts**:
- `anima_chat.py` v2.3 + (in-flight) `anima_chat.hexa` — D1 library SSOT
- `state/anima_phase1a1_color_cosmology_2026_05_12/` — D2 ckpt SSOT
- `state/anima_phase1a4_lr5e6_2026_05_12/` — D2 lr 5e-6 SFT BG state
- `state/anima_phase1a4_cuda_filter_validation_2026_05_12/` — D1 cuda filter-val (COMPLETE PSCC §30)

**D3 artifacts**:
- `state/p_idr_identity_rules_2026_05_12/identity_probe.jsonl` — 50 probes × 5 categories
- `docs/endpoint_persona_reproduce.md` — design carry
- `ready/anima/experiments/consciousness/experiment_personality.py` — experiment harness
- `ready/anima/experiments/consciousness/experiment_clone.py` — clone experiment
- `ready/anima/experiments/consciousness/experiment_merge.hexa` — merge experiment

**D4 artifacts**:
- `tool/hexa_native/mitosis_hook.hexa` — D4a hexa-native lane (parse-only stub)
- `training/mitosis_model_v5.py` + `training/mitosis_model_v5_smoke_test.py` — D4a PyTorch lane (cond.2 PASS)
- `anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` — D4 canonical 794L (REBORN §2)
- `.roadmap.clm_v5_mitosis_engine` — D4a PyTorch lane SSOT
- `tool/anima_cli/consciousness.hexa` — D4c CLI measurement lane
- `anima/llama_ffi.hexa` + `build/libhxllama.dylib` — D4c CLI Phase 3b chat backend
- `.roadmap.cli` + `.roadmap.anima_cli_model_architecture` — D4c CLI SSOT

**Infra**:
- `tool/dispatch_vast_mac_template.sh` — Vast.ai infra (PSCC §28 canonical)

---

## 🎯 Out of scope (mission 와 무관)

- ❌ HF Space `dancinlab/anima-chat` (DELETED 2026-05-12 KST, PSCC §32)
- ❌ Gradio / 외부 wrapper (refocus 후 제외)
- ❌ 다른 anima 작업 — HEXA_NATIVE phase 5∥ 24L 풀 forward / Hc cycle / ALM / 별도 lane

본 GOAL.md 는 **단 하나의 통합 mission** 만 추적: **★★★★★ via [chat 시스템 + 모델 + 페르소나 롤플레잉 + 세포분열 성장] 4-dim conjunction**.
