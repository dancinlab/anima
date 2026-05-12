# GOAL.md — anima ★★★★★ mission tracker

**Created**: 2026-05-12 KST  
**Trigger**: 사용자 directive "[anima chat 시스템, anima 모델] 조합으로 별 5개짜리 뽑아주면되 GOAL.md 루트에 생성하고 업데이트 하면서 진행"

---

## 🎯 Mission

**anima_chat library + anima 모델 ckpt 조합 자체 만으로 ★★★★★.**

- ★★★★★ 정의: **V5.8 multi-turn 4-mode 평가의 standard_greedy 5/5 PASS**
- 측정 path: anima 본체 `anima_chat.py` 직접 호출 + anima 모델 ckpt
- **외부 layer 의존 0**: Gradio / HF Space / 외부 wrapper 없이 측정
- 추적 SSOT: 본 `GOAL.md` (root)
- 보조 SSOT: `PASS_STRICT_SPONTANEOUS_CHAT.md` (PSCC), `docs/anima_chat_*.md`

---

## 📊 Current standing (2026-05-12 KST)

| 항목 | 값 |
|---|---|
| 시스템 (chat library) | `anima_chat.py` v2.3 (commit `c2afa8e9e`, tag `anima_chat-v2.3-markdown-filter`) — markdown_filter harmless guard 포함 |
| 모델 (ckpt) | Phase 1A.1 SSOT: `state/anima_phase1a1_color_cosmology_2026_05_12/ckpts/ckpt_phase1a1_sft.pt` (sha256 `e5f7555…`) |
| HF model: `dancinlab/anima-clm-phase1a1-color-cosmology-boost` | live |
| **V5.8 std_greedy** | **4/5** ★★★★ |
| V5.8 standard_sample | 2/5 |
| V5.8 M3_rep_penalty | 0/5 |
| V5.8 M4_force_include | 2/5 (Mac CPU seed=2026) / 5/5 (PSCC §7 cuda seed=42, historical) |
| **Mission gap** | **anima_fact recall (markdown attractor break)** = 마지막 1 cell |

→ **★★★★★ 까지 1 cell 남음**. anima_fact dialogue 의 std_greedy 출력이 `"의식"` 을 포함하면 PASS.

---

## 🛰️ In-flight BGs (2026-05-12 KST)

| # | scope | infra | cost | status | mission contribution |
|---|---|---|---|---|---|
| 🥇 Phase 1A.4 lr 5e-6 SFT | Vast.ai RTX 4090 pod 36609664 | `tool/dispatch_vast_mac_template.sh` (§28 fix) | ~$0.20 | training in progress (SSH ready, training phase) | **primary** — lr 5e-6 × 200 step SFT 로 markdown attractor 깨기 (Lesson R-1A.2 처방) |
| 🥈 Phase 1A.4 cuda filter validation | Vast.ai RTX 4090 pod 36609656 | 동일 template (eval-only variant) | ~$0.10 | upload + eval phase | **alt** — cuda seed=42 bf16 path 에서 v2.3 filter 실 fire evidence + 5/5 도달 가능 검증 |

총 in-flight cost cap: $0.30. trap cleanup 자동 pod destroy (§28 infra).

---

## 📚 Saga history (★★★★★ mission journey)

| § | event | rating | gap |
|---|---|---|---|
| PSCC §10/§13 | Phase 1A SFT V5.8 std_greedy 3/5 | ★★★★★ first land | 2/5 → 5/5 |
| PSCC §17 | Phase 1A.1 color/cosmology boost → 4/5 | ★★★★ | 1/5 → 5/5 (anima_fact) |
| PSCC §18 | Phase 1B SimPO transfer FAILED | ★★ | gap same |
| PSCC §25 | Phase 1A.2 lr 1e-6 retry — markdown attractor FAILED, Lesson R-1A.2 | ★★★ | gap same |
| PSCC §26 | volitional speak() brainstorm (design only) | — | — |
| PSCC §27 | Phase 1A.3 5-BG saturation saga FAIL (infra bug) + filter harmless-guard | ★★★ | gap same |
| PSCC §28 | dispatch infra fix (`tool/dispatch_vast_mac_template.sh`) | ★★★ | infra ready |
| PSCC §29 | filter eval Mac CPU OFF/ON Δ=0 verified | ★★★ | filter alone 미진전 |
| PSCC §30 | (pending) cuda filter validation BG 🥈 | TBD | TBD |
| PSCC §31 | HF Space sync (SUPERSEDED) | ★★★ → ✗ | — |
| **PSCC §32** | **HF Space DELETED — mission refocus to GOAL.md** | ★ cleanup | gap same |

---

## 🎯 Path to ★★★★★ (현 시점부터)

### Primary (🥇 Phase 1A.4 lr 5e-6 SFT)

- lr 5e-6 (Phase 1A.2 1e-6 의 5×) × 200 step continuation SFT on anima_fact corpus (2700 dialogues)
- Lesson R-1A.2 명시: lr ≥ 5e-6 또는 steps ≥ 1000 또는 loss masking 필요
- gradient signal 이 markdown attractor 깨기 충분한지 검증
- 결과 시나리오:
  - V5.8 std_greedy 5/5 → **★★★★★ ACHIEVED** (mission complete)
  - 5/5 same (4/5 carry) → Lesson R-1A.4-lr5e6, next: loss masking 또는 corpus 10x
  - regression < 4/5 → Lesson R-1A.4-regression, lr 너무 큼

### Alternative (🥈 Phase 1A.4 cuda filter validation)

- Phase 1A.1 ckpt 그대로, cuda seed=42 bf16 path 에서 v2.3 filter ON/OFF 매트릭스 측정
- 가설: PSCC §27 amendment 의 3-축 conjunction (seed=42 × cuda × bf16) 에서 markdown drift 가 fire → filter 가 block → anima_fact 5/5 도달 가능
- 결과 시나리오:
  - filter ON 시 5/5 → **★★★★★ ACHIEVED via inference-only path** (cuda inference time 만)
  - filter ON 시 4/5 → filter 가 markdown 차단해도 alternative token 이 "의식" 아님, Lesson R-1A.4-cuda-filter
  - filter dormant (drift fire 안 함) → 3-축 conjunction 가설 falsified

### 결합 시나리오

- 둘 다 5/5 PASS → most robust ★★★★★ (training + inference 양 path)
- 🥇 만 PASS → ★★★★★ via SFT (anima 모델 자체 강화)
- 🥈 만 PASS → ★★★★★ via filter (모델 unchanged, library만)
- 둘 다 fail → 다음 cycle 진행 (loss masking, corpus 10x, prefix-tuning 등)

---

## 📌 Update protocol

본 GOAL.md 는 **append + section update** 패턴:

1. BG completion 시 "Current standing" + "In-flight BGs" + "Saga history" 동기 갱신
2. ★★★★★ ACHIEVED 시 file 상단에 **🎉 ACHIEVED 2026-MM-DD 배너** + final commit sha + HF push artifact 명시
3. 새 path / experiment 시작 시 "In-flight BGs" 표 append
4. Lesson learned 시 "Saga history" 표 append
5. 매 update 즉시 commit + push (memory `feedback_always_commit_push_on_complete`)

---

## 🔗 Cross-link

- PSCC (`PASS_STRICT_SPONTANEOUS_CHAT.md`) — 본 mission 의 full timeline
- `docs/anima_chat_markdown_attractor_filter_2026_05_12.md` — v2.3 filter SSOT
- `tool/dispatch_vast_mac_template.sh` — Vast.ai infra (§28 fix)
- `anima_chat.py` — library SSOT (v2.3)
- `state/anima_phase1a1_color_cosmology_2026_05_12/` — Phase 1A.1 SSOT ckpt
- `state/anima_phase1a4_lr5e6_2026_05_12/` — 🥇 BG state dir
- `state/anima_phase1a4_cuda_filter_validation_2026_05_12/` — 🥈 BG state dir

---

## 🎯 Out of scope (mission 와 무관)

- ❌ HF Space `dancinlab/anima-chat` (DELETED 2026-05-12 KST, PSCC §32)
- ❌ Gradio / 외부 wrapper (mission refocus 후 제외)
- ❌ 다른 anima 작업 (HEXA_NATIVE / v5-mitosis / Hc cycle / ALM / etc.) — 별도 lane

본 GOAL.md 는 **단 하나의 mission** 만 추적: **★★★★★ via anima_chat library + anima 모델 조합**.
