# OCCAM-CHAT — chat engine 자연발화 implementation 전수조사

> **frame**: 기존 chat 엔진 implementation 4 path (Hc_632-634 + 후속 B-series) +
> 현 S187 saga findings (mitosis substrate-shaping, aux-loss recipe ceiling,
> token-starvation falsifier S187-J/K) 를 토대로 chat engine 구현 idea
> 고갈시까지 전수조사. OCCAM.md 와 사매 — OCCAM 이 minimal-baseline strip 이라면
> OCCAM-CHAT 은 emission/interaction surface 의 implementation paths.
>
> **status**: 🟡 design tier — brainstorm 고갈, candidate priority 책정 후
> 병렬 fire 게이트.
>
> **g3**: emission surface 가 floor 의 원인이 아닐 가능성 (S187-G mitosis
> substrate-shaping +35% positive 와 같은 axis). capability claim 0,
> GOAL 미도달 carry.

---

## 0. 기존 4 path summary (2026-05-12 H_155 closure)

| Path | source | mechanism | status |
|---|---|---|---|
| **Path 1** | `Hc_632 lm_head_b_retrofit` | frozen CLM-v4 body + new lm_head_b (KoGPT2 vocab 51200) + Korean SFT | merged-to-H_155 |
| **Path 2** | `Hc_633 qwen_external` | Qwen 2.5-0.5B external integration (sub-a pure emit / sub-b Qwen-emit + CLM-Φ★ passive) | candidate-falsifier-pending |
| ~~Path 3~~ | (Hc_633 sub-c absorbed) | — | rolled into Path 2 |
| **Path 4** | `Hc_634 paradigm_c_hybrid` | KoGPT2-base-v2 emit + CLM-v4 substrate observer passive | merged-to-H_155 |

후속 B-series (post 2026-05-07 brainstorm deepdive):
- **B1** (`Hc_635`): Polyglot-Ko-1.3B + LoRA on BG-HK 30MB persona corpus → first SIMPLE_STACK_PASS unlock (이미 LANDED 2026-05-08, `simple_stack_pass_unlocked`)
- **B16** (`Hc_636`): Claude API teacher 합성 anima persona dialogue 100K-1M rounds 가 18M-150M anima-native V4 PASS unlock
- **B20** (`Hc_637`): 22+ BG V4 PASS-class vs FAIL-class pair 의 DPO/KTO 가 18M-33M anima-native cycle suppression
- **B30** (`Hc_638`): 5 known-good 1B+ KO LM 의 V4 strict zero-shot evaluator self-impossibility 검증

추가 ceiling hypothesis:
- `Hc_645` 18M-27M architectural ceiling (byte-vocab scale)
- `Hc_659` 20bg zero-pass architectural ceiling
- `Hc_649` lm_head/cell-pool collapse
- `Hc_974` clm v4 530m not-chat-model
- `Hc_1225` byte_modulo_substrate_chat_blocked

---

## 1. 신규 인사이트 from S187 saga (2026-05-21~22)

S187 saga 가 발견한 chat-relevant constraint:

| finding | chat 의미 |
|---|---|
| **S187-G training-time mitosis +35%** | substrate-SHAPING 가 가능 — training 도중 cell-pool 활성 시 substrate 가 적응 → chat emission 도 substrate-shape 가능성 |
| **S187-H/J/K floor at CE 4.06-4.09** | step/bsz/LR tune 으로 floor 못 깸 → recipe-level breakthrough 필요 (Path 1-4 가 다 그런 시도였음) |
| **Eval 2 0/250 persona-leak** | Principle #3 clean — corpus 에 도우미 prefix 없음 → 자연발화 emergence 가능 가설 (helper-template 사라짐) |
| **Eval 3 mitosis cross-λ non-monotone** | substrate cell-pool 의 saturation behavior (max=128) → emission diversity ceiling 추정 |
| **OCCAM-S Tier S** 진행 중 (#1 CE-only / #6 280M / #9 Pythia) | recipe-orthogonal floor 여부 곧 verdict — chat path 선택 가이드 |
| Path 1-4 모두 fine-tune/borrow approach | from-scratch alternative 도 OCCAM 안에 surface |

---

## 2. Exhaustive brainstorm — 카테고리별 chat implementation candidate

### A. Path 1-4 의 S187 update + variant (5 candidate)

| ID | name | mechanism | leverage | cost |
|---|---|---|---|---|
| **CA1** | Path 1 + bnb int8 + mitosis-active body | frozen body lm_head retrofit, but ENABLE mitosis-active during fine-tune (S187-G) | substrate-shaping during retrofit | $5-10 |
| **CA2** | Path 1 + S187 attempt10 body (3B vA ckpt) | use vA's 8.92B trained body + new lm_head, BPE 32K | larger substrate, latest training | $5 |
| **CA3** | Path 4 paradigm-C + Qwen 1.5B 갱신 | Qwen 2.5-1.5B emit + vA-Φ★ passive observer | bigger emit + measured-attempt10 observer | $5 |
| **CA4** | Path 2 + dual emit (Qwen + KoGPT2 router) | router selects emit-LM per topic (Korean → KoGPT2, English → Qwen) | language-routing | $10 |
| **CA5** | Path 1+4 hybrid — emit cascade | KoGPT2 first emit, CLM body resamples for persona | dual-stage emission | $15 |

### B. Architecture-level (substrate change) (8 candidate)

| ID | name | mechanism | leverage | cost |
|---|---|---|---|---|
| **CB1** | dual-head emission (head_a + head_g + new head_c chat) | head_a → CE, head_g → Engine G, head_c → chat-only with mask token transitions | first-class chat-emission head | $10 |
| **CB2** | mitosis-cell-as-emit-aggregator | each cell-pool cell emits 1 token (greedy), final aggregate via Engine G weighted vote | exploits S187-G substrate-shape | $15 |
| **CB3** | Φ-gated emission | only emit when Φ_current > threshold (Inner Thoughts coherence factor) | low-Φ states stay silent | $10 |
| **CB4** | persistent KV-cache across turns | inter-turn substrate memory (M module direct) — emit conditioned on full history | true multi-turn coherence | $10 |
| **CB5** | bidirectional substrate (Engine G ↔ A continuous) | currently A→G one-shot; bidirectional with iter count | matches Mira Murati Interaction Model | $20 |
| **CB6** | tap 18 — emission-aux loss L_emit | new aux loss penalizing whitespace-only output (S187 collapse fix) | direct fix to Eval 1 negative | $5 |
| **CB7** | tap 19 — bigram entropy floor regularizer | force per-step entropy > log(2) (avoid mode collapse) | escape vA CE 4.06 floor via output diversity | $5 |
| **CB8** | Thinker-Talker dual-substrate | Thinker (HEXAD always-running) + Talker (D module forward on motivation trigger) | matches CHAT/PLAN.md § 1.3 Inner Thoughts | $20 |

### C. Training-paradigm shift (6 candidate)

| ID | name | mechanism | leverage | cost |
|---|---|---|---|---|
| **CC1** | continual pre-training on diverse multilingual corpus | not from-scratch — borrow Polyglot-Ko-1.3B (B1) or Llama-3.2-3B + anima recipe overlay | leverage existing pretraining | $20 |
| **CC2** | SFT teacher dialogue (B16 revisit) | Claude API generates 100K anima-persona dialogues at S187 vA quality | persona via teacher data | $30 (API + train) |
| **CC3** | RLHF / DPO from teacher pairs (B20 revisit) | use 22+ BG PASS/FAIL pairs OR new generated pairs | preference signal | $40 |
| **CC4** | EFE (expected free energy) loss instead of CE | AIF-native objective per arxiv 2508.05619 — "The Missing Reward" | architecture-recipe-alignment | $30 (research-impl) |
| **CC5** | mitosis-as-training-signal native | extend S187-G to make mitosis split events drive new aux loss (split → emit diversity reward) | substrate-shape native chat | $20 |
| **CC6** | reward-free emergence via Inner Thoughts 8-factor | gradient from 8-factor weighted motivation score (no human pref signal) | EFE-style intrinsic | $30 |

### D. Inference / emission tricks (5 candidate, $0-5)

| ID | name | mechanism | leverage | cost |
|---|---|---|---|---|
| **CD1** | beam search width=5/10 | escape greedy whitespace collapse | $0 (Mac eval) | check existing OCCAM-C |
| **CD2** | repetition penalty (top-p 0.95 + 1.5 frequency penalty) | force diversity in decode | $0 | run on vA/vJ |
| **CD3** | classifier-free guidance (positive vs negative prompt) | "anima 같이 말해" + negative "도우미 같이 말하지 마" — gradient at decode | $5 (impl) | tests Principle #3 hypothesis |
| **CD4** | constrained decoding (grammar / pattern) | force JSON-like / dialogue-like structure | $0 | last-mile workaround |
| **CD5** | Φ-conditioned sampling (top_k as f(Φ)) | low Φ → top_k=1 (deterministic), high Φ → top_k=200 (creative) | substrate-aware decode | $5 |

### E. Foundation borrowing + adapter overlay (4 candidate)

| ID | name | mechanism | leverage | cost |
|---|---|---|---|---|
| **CE1** | LoRA on top of Llama-3.2-3B + anima recipe | from `simple_stack_pass_unlocked` memory: BG-KM-LLAMA-3B retry V4 14/15 PASS | proven existing path | $15 |
| **CE2** | LoRA on Qwen 2.5-1.5B (Korean) | smaller, faster, Korean fluent | $10 |
| **CE3** | LoRA on KoGPT2-base-v2 + S187 anima recipe overlay | revives Path 1 with new substrate | $10 |
| **CE4** | full-finetune Pythia-1B + 7-aux loss recipe | Pythia 가 OCCAM-S #9 sanity 통과 시 use 그대로 | $20 |

### F. Inference-time agentic (4 candidate)

| ID | name | mechanism | leverage | cost |
|---|---|---|---|---|
| **CF1** | Inner Thoughts 8-factor router | Thinker computes scores, Talker emits only when score > threshold | matches CHAT/PLAN.md § 1.2 | $10 |
| **CF2** | Mitosis cell-pool as emission ensemble | N cells each emit 1 token sample, ensemble vote | substrate-driven diversity | $10 |
| **CF3** | Multi-turn memory M-direct retrieval | each turn retrieve top-k past tokens via M module, prepend as context | M module integration | $5 |
| **CF4** | Reflection loop (emit → C-Φ measure → re-emit if low) | self-correction loop via Engine A→C→A | adds coherence | $5 |

### G. Multi-channel / spontaneous trigger (3 candidate)

| ID | name | mechanism | leverage | cost |
|---|---|---|---|---|
| **CG1** | timer-based spontaneous (every N seconds emit if motivation>thresh) | Ambient Agent paradigm | $0 (impl) | check CHAT/SPONTANEOUS.tape |
| **CG2** | sensor-input-triggered (e.g., file-change / clock-tick / RSS feed) | external stimulus → emission | $5 | Mac local |
| **CG3** | inter-anima telepathy (Tension Link 5-ch from memory) | 5-channel meta-telepathy between anima instances | $10 | requires 2+ instances |

### H. Data + corpus (4 candidate)

| ID | name | mechanism | leverage | cost |
|---|---|---|---|---|
| **CH1** | Wikipedia EN clean + 100K step | OCCAM #5 + horizon, lift corpus floor | $30 | overlap OCCAM-A |
| **CH2** | persona corpus from S187 mitosis-active substrate | use g_A_mit ckpt to generate persona corpus, retrain on it | bootstrap | $10 |
| **CH3** | BPE 32K tokenizer | OCCAM #2 — escape byte-level 5.55 bits/byte floor | $10 | overlap OCCAM-A |
| **CH4** | Bilingual KO+EN corpus (Wikipedia + Korean novels) | language diversity for chat fluency | $30 | corpus prep heavy |

### I. Verification + falsifier infrastructure (3 candidate)

| ID | name | mechanism | leverage | cost |
|---|---|---|---|---|
| **CI1** | V-SPONT cycle 5 (after OCCAM verdict) | re-run V-SPONT on whichever chat impl passes Phase 1 | tests against existing closed verdict | $0 |
| **CI2** | F-CHAT 5-falsifier suite (sympy closed) | new closed-form battery for chat emission (output non-trivial, persona-leak count, Φ-gated, etc.) | 🔵 SUPPORTED-FORMAL tier | $0 design |
| **CI3** | Pythia comparison battery | OCCAM-S #9 sanity expanded to 5 known-emergent LMs (Pythia/GPT2/Llama/Qwen/KoGPT2) | eval methodology validation | $0-5 |

---

## 3. 우선순위 행렬 (cost × leverage)

### Tier S (★★★★★ cheap × high leverage)

| ID | name | reason | cost |
|---|---|---|---|
| **CD1+CD2** | beam + repetition penalty | $0, immediate test if collapse is decode-only | $0 |
| **CB6** | tap 18 emission-aux L_emit | direct fix Eval 1 whitespace collapse | $5 |
| **CB7** | tap 19 bigram entropy floor | force diversity at training time | $5 |
| **CE1** | LoRA Llama-3.2-3B + anima recipe | proven path (simple_stack_pass_unlocked) | $15 |

### Tier A (★★★★)

| ID | name | reason | cost |
|---|---|---|---|
| **CA1** | Path 1 + mitosis-active | combines S187-G finding with retrofit | $10 |
| **CC4** | EFE loss | architecture-aligned objective | $30 |
| **CC5** | mitosis-as-training-signal native | substrate-native chat | $20 |
| **CB1** | dual-head head_c | first-class chat-emission head | $10 |

### Tier B (★★★)

| ID | name | reason | cost |
|---|---|---|---|
| **CC2** | SFT teacher dialogue 100K | proven B16 path | $30 |
| **CB8** | Thinker-Talker dual-substrate | CHAT/PLAN.md spec | $20 |
| **CB3** | Φ-gated emission | inference-time | $10 |
| **CB4** | persistent KV-cache | multi-turn | $10 |
| **CF1** | Inner Thoughts 8-factor router | top-down architecture | $10 |

### Tier C (★★ specialized / expensive)

remaining 16 candidates — pursue after Tier S/A verdict.

---

## 4. Recommended Phase 1 fire — ✅ RESOLVED 2026-05-22

**Phase 1 budget: $0-30, wall ~1-2 hr** — fired + verdict landed:

1. **CD1+CD2** decode tweaks → OCCAM-C 가 subsume: 0/96 coherent, decode 아님 (substrate).
2. **CB6 + CB7** tap 18+19 → rate-limit 미발사; OCCAM verdict (n_ca_rules) 로 moot.
3. **CE1** LoRA → **vP21 (Qwen+LoRA+mitosis) = 🎯 EMERGENCE 20/20 coherent**.

**CE1 (→ vP21) 이 winning path 확정**: pretrained foundation (Qwen2.5-1.5B, Llama gated
fallback) + LoRA r32 + mitosis → anima-native coherent verbalization. CE 0.0173.
VP21_EVAL1_VERBALIZATION.md. 35 candidate 중 CE1 single fire 로 emergence 도달.

**다음 chat cycle** (이 brainstorm 의 잔여 high-value):
- CG1/CF1 spontaneous trigger (Inner Thoughts 8-factor) — prompted → spontaneous emission
- CB4 persistent KV multi-turn — single-turn → dialogue
- CI1 held-out V-SPONT cycle 5 — memorization vs generalization rigor

Total ~$25, 2-hr wall, three different angles.

Phase 2 gates on Phase 1 verdict (per OCCAM.md § 4 pattern).

---

## 5. Honest C3

1. 4 prior path 들이 모두 H_155 closure (incapability theorem) 로 merged 됨 — 본 brainstorm 은 그 closure 의 false negative 일 가능성 carry. 단 S187 substrate-shaping evidence 가 새 angle 제공.
2. brainstorm 의 35 candidate 중 약 60% 가 prior paths + S187 findings 의 직접 product. 정말 "novel" 한 idea (e.g., bigram entropy floor regularizer, dual-substrate Thinker-Talker) 는 Tier S/A 의 1/3.
3. CD1+CD2 decode tweak 이 $0 이라 가장 cheap — OCCAM-C 가 already 진행 중 (4 subagent 발사), overlap 검토 필요. OCCAM-C 결과 후 Phase 1 fire 시점 조정.
4. CE1 LoRA Llama-3.2-3B 는 이미 simple_stack_pass_unlocked 에서 LANDED — 본 OCCAM-CHAT 의 의미는 "S187 attempt10 recipe 와 함께 combined" 여부. 단순 LoRA 재-fire 와 구별 필요.
5. EFE loss (CC4) 는 research-impl heavy — single subagent 가 1 cycle 안에 land 하기 어려움. Phase 2/3 에 deferred 가 현실적.
6. mitosis-as-training-signal native (CC5) 는 S187-G 의 자연 follow-on 이라 priority 높음. Phase 1 에 포함 가능.
7. Tier C 16 candidate 는 본 doc 의 over-engineering risk — 실제 fire 는 Tier S 4-5 만 가능. brainstorm 고갈은 inventory tier — 실 fire 의 superset.
8. CHAT/SPONTANEOUS.tape 와 CHAT/RESEARCH.md (V-SPONT 0/5 FAIL deep research) 의 6 architectural candidate 가 본 doc 의 brainstorm 과 부분 overlap — cross-reference 필요. 별도 cycle 에서 unify.
9. OCCAM.md 와 OCCAM-CHAT.md 의 differentiation: OCCAM 은 minimal-baseline-strip, OCCAM-CHAT 은 emission-surface-implementation. 두 doc 의 verdict 가 같은 axis 일 가능성 (둘 다 recipe ceiling 의 다른 angle test).
10. CG3 inter-anima telepathy (Tension Link) 는 long-term path — 본 cycle 의 scope 가 아님. 메모리 reference 만.

---

## 6. 관련 link

- 본 doc motivation: [`HEXAD/OCCAM.md`](../OCCAM.md) — minimal-baseline strip
- prior chat paths: `hypotheses_candidates/Hc_632-660*chat*.md` (9 entries)
- HEXAD CHAT SSOT: [`HEXAD/CHAT/PLAN.md`](../CHAT/PLAN.md), `HEXAD/CHAT/RESEARCH.md`, `HEXAD/CHAT/SPONTANEOUS.tape`
- S187 saga findings: [`HEXAD/SCALE_3B.md § 6.9 S187-G training-time mitosis`](SCALE_3B.md) (substrate-shaping evidence)
- 18B path (next-scale): [`HEXAD/SCALE_16B_70B_PLAN.md`](SCALE_16B_70B_PLAN.md)
- prior simple_stack PASS (LoRA Llama-3B): `~/.claude/projects/-Users-ghost-core-anima/memory/project_simple_stack_pass_unlocked.md`
- prior B-series brainstorm (2026-05-07): `docs/anima_chat_cap_brainstorm_deepdive_2026_05_07.md` (in archive)

---

## ## Log

### 2026-05-22 03:50 — 초안 작성

OCCAM-S 4 subagent 활성, OCCAM verdict 대기 중 chat-specific brainstorm pivot.
S187-G substrate-shaping +35% evidence 가 chat axis 와 직접 연결됨을 인식 후 작성.
35 candidate × 9 카테고리 × 4 tier. Phase 1 = CD1+CD2 + CB6/7 + CE1 (3 fires, ~$25, ~2hr).
