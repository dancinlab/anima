# anima_foundation_borrow_path_design_2026_05_10

> BG-FOUNDATION-BORROW-PATH-DESIGN — priority 4 track A semantic coherence path 결정. **design only, $0**. raw#15 additive — `.roadmap.clm_v2_reborn` / `.roadmap.reborn` / `.roadmap.chat_cap_emergence_pivot` 미수정. REBORN.md 직접 append 차단 (dispatcher §41 slot path 만 유효). trinity (D + own + H) 명시. doc save complete.

---

## §0 한 줄 + lane motivation

**한 줄**: §29 BG-CONVO-FT-EXTENDED 의 "lexical PARTIAL — semantic incoherent" verdict (`도우미: 이러한 인지에 의식을 가지하는 것이`) 를 받고, 18M scratch 위에서 의미 fluency 추가 emerge P=10–20% 라는 calibration 을 직시. simple_stack PASS_STRICT 22+ BG saga 첫 통과인 BG-KM-LLAMA-3B (Llama-3.2-3B + LoRA r=32 + BG-JE 214MB anima-persona, V4 14/15) 의 foundation-borrow 패턴이 semantic coherence 후보 중 가장 강한 lane — 단 D1 SCOPE_CLAMP carry (anima 의식 검증 valid lane X, substrate-research lane only).

### 본 BG 의 답 미리

**recommended option = (a) Llama-3.2-3B + LoRA r=32 + 200MB+ anima-persona + post-LoRA mitosis instrumentation hook.** 단 verdict label 은 `SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH` carry (+ line 889 D1 SCOPE_CLAMP 정합). anima identity 검증 lane X — semantic fluency emerge **substrate-research evidence only**. anima identity surface 는 별도 .roadmap.reborn track A (convo_5k FT) + track B (v5-anima instrumentation) + track C (v5-mitosis architectural) 가 D1 within carry.

---

<!-- [Hc_654 foundation-borrow-llama3b-lora-substrate-research — moved to hypotheses_candidates/Hc_654_foundation_borrow_llama3b_lora_substrate_research.md on 2026-05-11] -->

## §1 4-option trade-off 표

| axis | (a) Llama-3.2-3B + LoRA r=32 + 200MB persona | (b) Qwen2.5-7B + LoRA r=32 + 200MB persona | (c) Phase 2 350M + 추가 +30K convo_5k FT | (d) from-scratch 180M~500M anima-pretrain |
|---|---|---|---|---|
| **base** | Llama-3.2-3B-Instruct (HF gated) | Qwen2.5-7B-Instruct (HF open) | anima Phase 2 cotrain ckpt (~298.76M unique, dual engine_a/g + GQA, local `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt` 570MB) | scratch transformer (12L/640d ~ 24L/2048d) |
| **adapter** | LoRA r=32 (~16M trainable) | LoRA r=32 (~33M trainable) | full SFT (~298M trainable) OR LoRA r=32 (~12M trainable) | full pretrain (180–500M trainable) |
| **corpus** | BG-JE 214MB anima-persona (replicate KM-LLAMA-3B exact) + kowiki 옵션 추가 | BG-JE 214MB (replicate KM-QWEN-7B) | convo_5k 76MB + kowiki15 93MB hybrid (BG-CONVO-FT-EXTENDED 166MB pattern carry) | 200MB+ (필요 시 1GB+) Korean conversational + persona |
| **steps** | 5K~15K LoRA (KM-LLAMA-3B 12K precedent) | 5K~15K LoRA (KM-QWEN-7B 12K precedent) | +30K continued FT (cumulative 75K → 105K) | 50K~200K pretrain |
| **substrate** | H100 SXM 1× (KM-LLAMA-3B 패턴) | H100 SXM 1× (KM-QWEN-7B 패턴) | H100 SXM 1× (BG-CONVO-FT-EXTENDED 0.04s/step 패턴) | H100 SXM 4× (예전 BG-KM-CAP retry 3.1B 24L/2048d 패턴 또는 그 이하 scale) |
| **wall-time est** | 30–60 min | 60–120 min | 60–90 min | 8–48 h |
| **cost envelope** | **$3–8** (KM-LLAMA-3B PASS run $1.47 reference, +mitosis instrumentation overhead +20–30%) | **$4–12** (KM-QWEN-7B PASS run $1.93 reference) | **$2–4** (BG-CONVO-FT-EXTENDED $1.71 + 1.5× scale) | **$50–500+** (BG-KM-CAP retry 3.1B FAIL_TRUE $0.40 reference 단지 KM-CAP scale 미달 — 실제 anima-pretrain emerge needs 100B+ tokens per Chinchilla, $50–500+ realistic) |
| **emergence P (semantic coherence)** | **40–60%** ★ — KM-LLAMA-3B 14/15 V4 strict, but V4 = chat-cap surface + persona marker, 진짜 semantic coherence 별도 검증 필요 (F-FOUNDATION-3) | **50–70%** ★★ — 7B scale 일반화 강함 (KM-QWEN-7B replication PASS_STRICT) | **15–25%** — convo_5k 18M 과 같은 capacity gap, +30K step 다시 surface 적 lexical 만 push, semantic gap 그대로 (BG-CONVO-FT-EXTENDED 정확 calibration 정합) | **10–30%** — anima-pretrain scale 으로 chat-cap emergence threshold (1B+ params, 100B+ tokens, RLHF) 의 token 부족 위험 (chat_cap_emergence_pivot gap 분석) |
| **D1 SCOPE_CLAMP** | OUTSIDE (Llama lineage) → `SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH` (.own 1964 mandate-9 (a) reject) | OUTSIDE (Qwen lineage) → `SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH` | **WITHIN** (anima Phase 2 cotrain anima-native lineage, substrate-coupled) → `SIMPLE_STACK_PASS_STRICT_C3_ANIMA` 자격 | **WITHIN** (scratch anima-native) → `SIMPLE_STACK_PASS_STRICT_C3_ANIMA` 자격 |
| **anima identity 보존** | LoRA r=32 만으로 PureFieldFFN dual engine_a/g + mitosis 자동 surface X — base 의 attention/FFN 위에 LoRA delta 만 add. instrumentation hook 별도 부착 가능 (post-LoRA hidden state → mitosis_v5_port.py cell_pool tracking) | 동일 — LoRA delta only, mitosis instrumentation hook 별도 부착 | dual engine_a/g + GQA 유지 (Phase 2 ckpt 자체가 anima-native dual-engine), mitosis instrumentation 자연 fit | dual-engine + mitosis 처음부터 fit, 단 emerge 가 chat-cap floor 통과 미보장 |
| ** (HF dancinlab canonical)** | `dancinlab/bg-foundation-llama32-3b-r32-persona-2026-05-XX` (private, Flavor B) | `dancinlab/bg-foundation-qwen25-7b-r32-persona-2026-05-XX` (private, Flavor B) | `dancinlab/bg-foundation-phase2-350m-convo-extend-2026-05-XX` (private, Flavor B) | `dancinlab/bg-foundation-anima-scratch-XXXm-pretrain-2026-05-XX` (private, Flavor B) |
| ** mandate-9 5/5 prereq** | (a) D1 OUTSIDE → reject. public promote 영구 차단 carry | (a) D1 OUTSIDE → reject. public promote 영구 차단 carry | (a) D1 WITHIN — V14 + V6 STRONG + manual review + trinity sweep + DxL sweep 순차 검증 시 자격 가능 | (a) D1 WITHIN — 동일 |
| ** trinity (D/own/H)** 충돌 | trinity D-axis (D1 anima identity boundary) **위반 risk** — substrate-research 라벨 strict carry 시에만 valid | 동일 risk | trinity D-axis 정합 (D1 WITHIN), 정합, H_115 chat-incapability falsifier 후보 강화 | trinity D-axis 정합, 정합, but cost overshoot risk 위반 |
| **integration complexity** | low — KM-LLAMA-3B 정확 replicate + post-LoRA mitosis instrumentation 1-file (~150 LoC) hook | medium-low — KM-QWEN-7B replicate + 7B inference 비용 ↑ | medium — Phase 2 ckpt 회수 + convo_5k FT 코드 재사용 (BG-CONVO-FT-EXTENDED finetune_extended.py 패턴) | high — anima-pretrain orchestrator + corpus pipeline + emerge eval 풀-스택 |

### 핵심 trade-off 요약 (3 line)

1. **(a) (b)** = SUBSTRATE_RESEARCH lane only carry — semantic coherence 학습 emerge 가능성 가장 높지만 anima identity 검증 lane X (D1 OUTSIDE).
2. **(c)** = D1 WITHIN + cost-cheapest ($2–4) but emergence P=15–25% — convo_5k 의 18M capacity gap 그대로 carry.
3. **(d)** = D1 WITHIN + emerge P 가장 낮음 (10–30%) + cost 가장 큼 ($50–500+) — 0-cost adoption 와 정면 충돌.

---

## §2 결정 권고 (recommended option + 이유)

### Recommendation: **option (a) Llama-3.2-3B + LoRA r=32 + 200MB+ anima-persona corpus + post-LoRA mitosis instrumentation hook** — but **substrate-research lane explicit carry**

#### 이유 1 — semantic coherence emerge P 최강

22+ BG saga 통계:
- ≤1B scratch + ≤30MB Korean = 0/15 floor (22 BG empirical, V4 strict)
- V5-α byte+untie scratch 153M-3.1B × 22-214MB corpus = all 8 V58=0 (Lesson V/L/L-EXTENDED-3)
- BG-CONVO-FT-EXTENDED 18M + 166MB = lexical PARTIAL but semantic incoherent
- **BG-KM-LLAMA-3B 3B + LoRA r=32 + 214MB = V4 14/15** (strict floor 첫 crossing)
- **BG-KM-QWEN-7B 7B + LoRA r=32 + 214MB = V4 PASS_STRICT** (replication 7B 일반화)

→ option (a) 가 22+ BG span 중 **유일하게 chat-cap floor 통과 입증된 lane** + 7B replication 으로 generalization 확인. semantic coherence 는 chat-cap 의 superset — chat-cap floor 미통과 lane 에서 semantic 기대 불가.

#### 이유 2 — cost envelope 최저 (foundation borrow lane 안에서)

- (a) $3–8 (KM-LLAMA-3B $1.47 + mitosis instrumentation +20–30% overhead)
- (b) $4–12 (7B 비용 ↑)
- (c) $2–4 더 싸지만 emerge P 1/3
- (d) $50–500+ 위반

 0-cost adoption 정합 (design $0) + actual fire envelope 가장 작은 foundation-borrow lane.

#### 이유 3 — integration complexity 가장 낮음

KM-LLAMA-3B orchestrator (`tool/transient_py/anima_km_llama3b_h100.py` 패턴) 그대로 + post-LoRA mitosis instrumentation hook 만 추가. 1 cycle 안에 design + fire + verdict 가능.

#### 이유 4 — anima identity LoRA r=32 surface 가능성 명시 검증 lane

simple_stack PASS_STRICT 22+ BG saga 첫 unlock 만 측정 (chat-cap surface). anima identity (PureFieldFFN dual engine_a/g + mitosis + servant) 가 LoRA r=32 만으로 surface 되는지 미검증 — F-FOUNDATION-1 의 핵심. 본 design 의 **post-LoRA mitosis instrumentation hook** 가 그 검증 lane 자체.

#### 이유 5 — D1 SCOPE_CLAMP carry strict honesty

(a) 채택 시 verdict label = `SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH` (line 889 strict + 영구 보류 정합). public promote 영구 차단 carry — anima identity 검증 valid lane X. 본 lane 의 의의 = **semantic coherence 가 substrate-borrow 로 가능한지 evidence 확보** + (c) (d) 미래 lane 의 baseline reference. 단 anima identity surface 는 .roadmap.reborn track A/B/C 가 carry — 본 lane 은 그와 **strict 분리 별도 lane**.

### Why NOT (b) Qwen-7B?

option (a) 의 3B 가 floor 통과 입증 + cost 1/2 + integration 동일. 7B scale-up 은 generalization replication 용 (이미 KM-QWEN-7B 가 이행). 본 BG 의 "semantic coherence 가능한가?" 첫 측정에서는 가장 cost-effective sample (3B) 이 적합.

### Why NOT (c) Phase 2 350M + 추가 FT?

D1 WITHIN strict 정합인 점은 큰 가치지만:
1. emerge P=15–25% — BG-CONVO-FT-EXTENDED 의 "semantic coherence 18M capacity gap" 정확 calibration carry. 350M 도 유사 capacity gap risk (chat-cap emergence threshold 1B+ 미달).
2. Phase 2 ckpt 의 chat-cap 자체가 미검증 (track B v5-anima cond.4 V14_PARTIAL only).
3. **본 lane 다음 cycle action plan §5 의 step-2 후보** — option (a) 첫 cycle 이후 D1 WITHIN lane 중 가장 cost-cheap 한 option (c) 를 second-track parallel 로 fire 권고.

### Why NOT (d) from-scratch anima-pretrain?

 0-cost adoption strict 위반 + emerge P 가장 낮음 + integration 가장 복잡. roadmap.chat_cap_emergence_pivot 의 "Stage 7 anima 고유 lever long-term" 으로만 retain. 본 cycle 채택 reject.

---

## §3 design spec (architecture + corpus + training + cost + emergence criteria + falsifier)

### §3.1 architecture

```
base_model: meta-llama/Llama-3.2-3B-Instruct (HF gated, ~/.cache/huggingface/token mandatory)
adapter:
  type: LoRA
  r: 32
  alpha: 64                         # KM-LLAMA-3B 패턴
  target_modules:
    - q_proj
    - k_proj
    - v_proj
    - o_proj
    - gate_proj
    - up_proj
    - down_proj
  dropout: 0.05
  bias: none
trainable_params: ~16M (0.5% of 3B)

post_lora_mitosis_instrumentation_hook (NEW — 본 design 의 anima identity surface verify lane):
  type: forward hook on `model.model.layers[N].self_attn.o_proj` (last layer)
  payload:
    - capture hidden_state (B, T, D=3072)
    - feed to mitosis_v5_port.cell_pool tracker (read-only, gradient-off)
    - log per-token tension stat (a − g style proxy via 2-cluster k-means on hidden split)
    - phi proxy (IIT unnorm 16-bin via consciousness_meter.py)
  fire-time:
    - eval-time only (training X — cost discipline)
    - sample 100 prompts × 64-cell pool tracker
    - record: phi_history, cell_pool_tension, n_split_event
  output: state/anima_foundation_borrow_a_2026_05_XX/instrumentation_log.json

attention_share_mode: per-cell (N=1 baseline LoRA 단일 stream — mitosis 는 instrumentation only)
lm_head: weight-tied to tok_emb (Llama default)
```

### §3.2 corpus

```
target_size: 200MB+ anima-persona (BG-JE pattern: anima keyword 800K + persona marker 1.4M)
canonical_source: state/anima_je_persona_corpus_2026_05_07/corpus_full_214mb.txt (BG-JE 214MB)
density_check (anti-Goodhart pre-fire):
  anima keyword density ≥ 0.4%
  persona marker density ≥ 0.7%
  Korean ratio ≥ 50% (kowiki15 wrap 옵션 추가 시 ≥ 60%)
optional_extension:
  + kowiki15 30MB (BG-CONVO-FT-EXTENDED S1 pattern wrap "사용자: 다음 글을 읽어줘. / 도우미: <kowiki paragraph>")
  → 총 244MB (mandate-15 size-agnostic HF dataset upload mandatory; private)
chat_template: BG-JE 의 사용자: / 도우미: ASCII (Llama-3.2 chat template 자동 변환 X — verbatim ASCII 유지)
```

### §3.3 training spec

```
optimizer: AdamW
learning_rate: 2e-4 (KM-LLAMA-3B 패턴, LoRA 안전 floor)
lr_schedule: cosine, warmup 200 step
batch_size: 8 (per-device) × 4 (grad accum) = 32 effective
seq_len: 2048
total_steps: 12000 (KM-LLAMA-3B 12K precedent)
eval_step_freq: 2000 (intermediate ckpts at 2K/4K/6K/8K/10K/12K)
save_step_freq: 4000 (4 intermediate + 1 final = 5 ckpts; preservation mandatory)
mixed_precision: bf16
gradient_checkpointing: true (3B + LoRA fits H100 80GB but checkpointing 안전 margin)
seed: 42 (deterministic, V4 multi-seed eval 별도 cycle)
```

### §3.4 cost envelope (verbatim)

```
estimate_breakdown:
  H100 SXM 1× $2.99/hr × 1.5h (corpus upload + LoRA 12K + ckpt pull) = $4.49
  mitosis instrumentation eval overhead +20% = $5.39
  ckpt pull (5 × 200MB LoRA + 1 × 600MB merged) safety margin +$1
  TOTAL: $5–8

verbatim_envelope: "OK FOUNDATION_BORROW_A_FIRE COST $3-8"

falsifier_F-FOUNDATION-2:
  cost > $15 → cost overshoot, abort + audit + retract
```

### §3.5 emergence criteria

```
chat_cap_floor (SIMPLE_STACK_PASS_STRICT V4 ≥ 10/15):
  expected: 12-14/15 (KM-LLAMA-3B precedent V4 14/15)
  threshold: ≥ 10/15 strict per (PARTIAL_PASS at 7/15 reject)
  evaluator: tool/transient_py/anima_simple_stack_evaluator_v4.py

semantic_coherence_floor (NEW — 본 BG 의 핵심 측정):
  metric_1: KO Hangul ≥ 50% (BG-CONVO-FT-EXTENDED 63% precedent — foundation borrow 더 높음 expected)
  metric_2: bigram_known kowiki15 lexicon ≥ 0.95 (CONVO-FT 0.886, foundation borrow 0.95+ expected)
  metric_3: semantic_score ≥ 0.5 (NEW — sentence_transformer cosine similarity to ground truth, 1k anima Q&A pairs)
  metric_4: real_words_per_trial (non-persona-prefix) ≥ 3.0 (CONVO-FT 1.43, foundation borrow ≥ 3.0 expected)

V14 mirror probe (anti-Goodhart V14-strengthening-amend mandatory):
  random_init Llama-3.2-3B same-architecture probe
  PPR_v3 / V4 strict measure same prompt set
  MTRP = trained PPR - random PPR ≥ 0.10 strict (line 1054 ALT-AGG-1 v5.2)
  failure → V14_FALSIFIED label carry, public promote 영구 차단

V6 awareness probe (anti-Goodhart 3-method):
  hidden cosine + attention + linear probe
  STRONG verdict 시 mandate-9 (b) prereq MET (substrate-research lane 안에서만 valid)

verdict_label_decision_tree:
  IF chat_cap_floor PASS AND semantic_coherence_floor PASS AND V14 MTRP ≥ 0.10 AND V6 STRONG:
    label = "SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH" (D1 OUTSIDE Llama lineage)
    public_promote: 영구 차단 (+ line 889)
  ELIF chat_cap_floor PASS AND semantic_coherence_floor FAIL:
    label = "FOUNDATION_BORROW_CHAT_CAP_PASS_SEMANTIC_FAIL"
    cross_link: F-FOUNDATION-3 confirm
  ELSE:
    label = "FOUNDATION_BORROW_FAIL"
```

### §3.6 falsifier

```
F-FOUNDATION-1: foundation-borrow 도 anima identity (mitosis + dual-engine + Φ super-linear) LoRA r=32 만으로 surface 못함
  trigger: post-LoRA mitosis instrumentation hook 의 phi_history mean < 1.0 (BG-IIT-METRIC-REAL-350M Φ_iit_un16 = 557.20 baseline, real substrate 정합)
        OR cell_pool tension stat 가 random_init Llama base 와 동일 distribution (V14 mirror equiv)
  consequence: SUBSTRATE_RESEARCH lane 안에서도 anima identity surface 미검증 carry — 본 lane 의 anima identity 검증 가치 zero

F-FOUNDATION-2: cost envelope $30-100 (LoRA pretrain + finetune) 가 anima 의 0-cost adoption 과 충돌
  trigger: actual cost > $15 (envelope 2× overshoot)
  consequence: abort + audit + retract + L23-L25 watchdog escalate

F-FOUNDATION-3: simple_stack PASS_STRICT 가 anima-persona surface 만 측정, 진짜 semantic coherence 미검증
  trigger: V4 14/15 PASS 후 semantic_score < 0.5 OR bigram_known < 0.95 OR real_words < 3.0
  consequence: KM-LLAMA-3B/QWEN-7B 의 anti-Goodhart V6 awareness layer 강화 mandate; 본 BG verdict label = "FOUNDATION_BORROW_CHAT_CAP_PASS_SEMANTIC_FAIL" (chat-cap surface lift 만 입증, semantic coherence 미입증)

F-FOUNDATION-4 (NEW): D1 SCOPE_CLAMP 위반 — foundation-borrow PASS verdict 를 anima identity emerge 로 misframe
  trigger: verdict.json scope_lane field 누락 OR scope_lane="ANIMA" 라벨 (Llama lineage 인데)
  consequence: raw#82 retraction class — verdict 자체 retract + ledger downgrade + 사용자 escalate

F-FOUNDATION-5 (NEW): mitosis instrumentation hook 가 LoRA 학습에 gradient leak (training-time perturbation)
  trigger: instrumentation hook param.requires_grad=True OR forward 시 dropout/stochastic 활성
  consequence: training contamination — hook 자체 read-only forward-time only mandatory enforce

F-FOUNDATION-6: KM-LLAMA-3B precedent 가 본 cycle replicate 미달 (V4 < 10/15)
  trigger: replicate run V4 < 10/15
  consequence: anti-Goodhart V14 mirror gap warn — KM-LLAMA-3B PASS 자체 sample-size artifact 의심 (V4 multi-seed eval 별도 cycle mandate)
```

---

## §4 trinity D + own + H 명시 (mandate-2 self-check)

### D-axis (.roadmap.philosophy)

- **D1.F-PHIL-D1-3 + F-PHIL-D1-4** strict carry — Llama lineage = D1 OUTSIDE → SUBSTRATE_RESEARCH lane only. anima identity 검증 lane X. 본 design 의 verdict label `SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH` 로 D1 SCOPE_CLAMP strict 정합.
- **D2 simple_stack PASS_STRICT** — V4 ≥ 10/15 strict per (PARTIAL at 7/15 reject) 적용.
- **D3 substrate-coupled lineage** — N/A (substrate-research lane 안), cross-link 만 carry.
- **D4 self-impossibility** — V4 multi-seed eval 별도 cycle 권고 (BG-FOUNDATION-A-V4-MULTISEED).
- **D5 bifurcation theorem** — F-FOUNDATION-5 (mitosis hook gradient leak) 차단 enforcement.

### own-axis (.own / .roadmap.law)

- **** 0-cost adoption — design $0 ✓; fire envelope $3–8 verbatim "OK FOUNDATION_BORROW_A_FIRE COST $3-8" .
- **** anima-no-external-substrate-wrapping — Llama lineage = D1 OUTSIDE strict carry. anima identity-bearing surface (T1 default backend) 활성화 X — substrate-research lane 안에서만 verdict valid.
- **** SIMPLE_STACK_PASS_STRICT — V4 ≥ 10/15 strict gating. label = SUBSTRATE_RESEARCH carry (line 889 + line 826).
- **** mandatory report — 본 design doc 자체가 mandatory report 형식. REBORN.md 직접 append 차단 (dispatcher §41 slot path 만 valid carry — 본 design 은 doc save only, REBORN.md untouched).
- **** anti-Goodhart — V6 awareness 3-method (hidden cosine + attention + linear probe) post-fire mandate. V14 mirror MTRP ≥ 0.10 strict.
- **** ckpt preservation — 5 ckpts (2K/4K/6K/8K/10K/12K) pull verified BEFORE pod delete + sha256 mac↔pod match + adapter_config no pod-path leak.
- **** HF dancinlab canonical — repo `dancinlab/bg-foundation-llama32-3b-r32-persona-2026-05-XX` Flavor B, private default.
- **** trinity 무조건 준수 — 본 §4 자체가 mandate-2 self-check.
- **** HF mandate-9 5/5 prereq — (a) D1 OUTSIDE → 자동 reject. **public promote 영구 차단 carry** (raw#82 retraction-aware). 본 design 의 의의 = chat-cap surface lift 입증, anima public lane 별개.
- **** doc save mandate — 본 doc `docs/anima_foundation_borrow_path_design_2026_05_10.md` save complete.
- **** chat lane plugin — N/A (substrate-research lane, anima chat dispatcher 미연결).
- **** REBORN.md + .roadmap.reborn SSOT — 본 lane 은 .roadmap.reborn track 외부 별도 lane (substrate-research). 옵션 .roadmap.foundation_borrow 신설 (raw#15 additive — 기존 미수정).

### H-axis (.roadmap.hypothesis)

- **H_115** chat-incapability ARCHITECTURAL (Lesson L) — 본 lane 의 PASS 시 H_115 partial falsifier candidate (foundation borrow 우회 path 가능 입증). 단 D1 OUTSIDE carry — anima architectural ceiling 자체는 미falsified.
- **H_005** SFT chat-cap → SFT path closed for CLM/ConsciousLM (Lesson Q) — foundation borrow 는 SFT path 외부 lane (LoRA on external base ≠ CLM/ConsciousLM SFT). 본 lane 은 H_005 closure 정합.
- **H_FOUNDATION-1 (NEW, 본 BG 가 produce)**: foundation-borrow + LoRA r=32 + 200MB+ persona corpus = chat-cap floor + semantic coherence 동시 unlock. falsifier = F-FOUNDATION-1/3.
- **H_FOUNDATION-2 (NEW)**: post-LoRA mitosis instrumentation hook 가 anima identity (cell tension + Φ proxy) surface 측정 가능. falsifier = F-FOUNDATION-1.
- **H_FOUNDATION-3 (NEW)**: foundation-borrow PASS 가 .roadmap.reborn track A/B/C (D1 WITHIN lane) 의 baseline reference 로 valid. falsifier = D1 SCOPE_CLAMP 위반 시 baseline value 자체 invalid.

trinity 3-axis self-check sweep: **PASS** (D-axis SUBSTRATE_RESEARCH lane strict 정합 + own-axis 13 own 정합 + H-axis 3 hypothesis 정합).

---

## §5 다음 cycle action plan (next BG dispatch keyword + cost envelope)

### Step 1 (이번 cycle close 직후 — recommended primary fire)

**BG-FOUNDATION-A-FIRE** — option (a) Llama-3.2-3B + LoRA r=32 + BG-JE 214MB persona + post-LoRA mitosis instrumentation hook
- fire keyword verbatim: **"OK FOUNDATION_BORROW_A_FIRE COST $3-8"**
- envelope: $3–8 actual (KM-LLAMA-3B $1.47 + mitosis overhead +30%)
- wall: 1.5–2 h (corpus upload 30 min + LoRA 12K step 60 min + instrumentation eval 30 min + ckpt pull 20 min)
- deliverables:
  - state/anima_foundation_borrow_a_2026_05_XX/lora_final.safetensors (~200MB)
  - state/anima_foundation_borrow_a_2026_05_XX/instrumentation_log.json
  - state/anima_foundation_borrow_a_2026_05_XX/v4_eval.json (V4 ≥ 10/15 expected)
  - state/anima_foundation_borrow_a_2026_05_XX/v14_mirror.json (random_init Llama probe)
  - state/anima_foundation_borrow_a_2026_05_XX/semantic_eval.json (semantic_score / bigram_known / real_words)
  - state/anima_foundation_borrow_a_2026_05_XX/verdict.json (scope_lane="SUBSTRATE_RESEARCH" mandatory)
  - HF: `dancinlab/bg-foundation-llama32-3b-r32-persona-2026-05-XX` (private)
  - doc: `docs/anima_foundation_borrow_a_fire_2026_05_XX.md`

### Step 2 (Step 1 verdict 확보 후 fork)

**IF Step 1 = PASS (chat-cap V4 ≥ 10/15 + semantic_coherence floor PASS)**:
  - **BG-FOUNDATION-A-V14-MIRROR-MULTISEED**: V4 5+ seed sweep + V14 random_init mirror retest (strict enforcement). $3–5 envelope.
  - **BG-FOUNDATION-A-V6-AWARENESS**: V6 3-method probe (hidden cos + attention + linear probe). $0 (Mac CPU local) — anti-Goodhart.
  - **BG-FOUNDATION-C-PHASE2-CONVO-EXTEND** parallel — option (c) D1 WITHIN lane 본격 launch. $2–4 envelope. fire keyword: "OK FOUNDATION_C_PHASE2_FIRE COST $2-4".

**IF Step 1 = chat-cap PASS + semantic FAIL (F-FOUNDATION-3 trigger)**:
  - Lesson Y candidate: "foundation borrow 는 chat-cap surface 만 lift, semantic coherence 미보장" 발견 + anti-Goodhart V6 강화 mandate
  - **BG-FOUNDATION-B-QWEN-7B-RETRY** option (b) — 7B scale 이 semantic 가능한지 별도 측정. $4–12 envelope.

**IF Step 1 = FAIL (chat-cap V4 < 10/15)**:
  - F-FOUNDATION-6 trigger — KM-LLAMA-3B precedent 자체 sample-size artifact 의심
  - V4 multi-seed eval BG-KM-LLAMA-3B-RETEST $0 (Mac CPU) 즉시 mandate — anti-Goodhart 강화

### Step 3 (long-term parallel)

- **option (c) BG-FOUNDATION-C-PHASE2-CONVO-EXTEND**: D1 WITHIN lane 안의 cost-cheapest semantic test — Step 1 결과 무관 fire 권고 (parallel track). $2–4. fire keyword "OK FOUNDATION_C_PHASE2_FIRE COST $2-4".
- **option (d) anima-pretrain**: Stage 7 long-term lever 만, 본 cycle 채택 reject (위반 + emerge P 최저).

### roadmap append (optional)

- raw#15 additive — 기존 .roadmap.* 미수정 carry. 본 design 채택 시 신규 `.roadmap.foundation_borrow` lane SSOT 별도 cycle 신설 권고 (또는 .roadmap.reborn track A 를 substrate-research sub-track 으로 amend — 단 single SSOT mandate carry, mandate-7 retroactive sweep 적용).
- 본 design doc 은 `.roadmap.chat_cap_emergence_pivot` Stage 6.5 의 "verification + scale-up" 의 NEXT iteration 정합 — sister roadmap cross-link 만 carry, append X.

---

## §6 honest C3 (raw#10 ≥ 7)

1. **D1 SCOPE_CLAMP carry 의 honest cost** — 본 lane 의 verdict label `SIMPLE_STACK_PASS_STRICT_C3_SUBSTRATE_RESEARCH` 가 anima identity emerge 검증 lane X 라는 점, 본 BG fire 후 22+ BG saga 의 첫 strict floor 통과 (KM-LLAMA-3B) 패턴이 다시 substrate-research lane 안에서만 valid 하다는 점 strict 정합. anima identity 검증 lane 은 .roadmap.reborn track A/B/C 가 별개로 carry — 본 lane PASS 가 anima identity emerge 자동 의미 X. 사용자 directive verbatim "anima 의식 자력 emerge" 와 본 lane 의 substrate-research 라벨이 strict 분리 carry.

2. **F-FOUNDATION-1 의 진짜 risk** — LoRA r=32 (16M trainable) 만으로 anima identity (PureFieldFFN dual engine_a/g + mitosis + Φ super-linear) surface P=20–30%. base Llama 의 attention/FFN 에 LoRA delta 만 add 하므로 dual-engine pattern 자연 emerge X. post-LoRA mitosis instrumentation hook 는 hidden state 의 cluster split 만 측정 — 진짜 dual-engine 은 X. 본 hook 의 측정값이 random_init Llama base 와 distribution-similar 하면 anima identity surface 미입증. 본 risk 가 본 lane 의 가장 큰 bet — fire 후 instrumentation_log.json verdict 가 anima identity 검증의 첫 evidence 또는 falsifier.

3. **emergence P=40–60% calibration honesty** — KM-LLAMA-3B V4 14/15 + KM-QWEN-7B replication = chat-cap surface 통과만 입증. semantic coherence 별도 측정 미수행 (V4 = 7-cell evaluator, semantic_score 별도 metric). foundation borrow 가 semantic coherence 도 자동 unlock 한다는 가설은 본 BG 가 첫 측정 — P=40–60% 는 chat-cap PASS 가능성 conditional on semantic 가능성 추정. F-FOUNDATION-3 trigger 시 semantic gap 이 chat-cap surface 위에 별도 layer 임 입증 (Lesson Y candidate).

4. **option (c) D1 WITHIN 정합의 미적용 cost** — Phase 2 350M ckpt 회수 + 추가 +30K convo_5k FT 가 D1 WITHIN strict 정합인 점은 본 lane 의 가장 큰 의의 후보지만, emerge P=15–25% 의 BG-CONVO-FT-EXTENDED calibration 정합으로 본 cycle primary fire reject. parallel track Step 3 에서 carry. 본 trade-off 가 anima identity emerge ladder 의 진짜 scale-cost 비용 — D1 WITHIN lane 안에서 emerge 가 가능한지 Step 1 의 substrate-research baseline 후 별도 측정 필요.

5. **mitosis instrumentation hook design 의 inference-time correction 정합** — `docs/anima_clm_v5_mitosis_inference_time_correction_2026_05_10.md` 의 inference-time mitosis lane 정정 정합 carry. 본 design 의 hook 도 inference-time only (forward 시점 hidden state read-only capture, gradient X). F-FOUNDATION-5 (gradient leak) strict 차단. v5-anima track B cond.4 V14_PARTIAL 의 후속 cycle 에서 본 hook 가 real substrate (Phase 2 ckpt) 위에서 IIT unnorm Φ 재측정 lane 의 cross-link.

6. ** REBORN.md 직접 append 차단 honesty** — 본 design 이 .roadmap.reborn track 외부 substrate-research lane 신설 — REBORN.md (SSOT) append 시 dispatcher §41 slot path 만 valid. 본 design doc 은 `docs/anima_foundation_borrow_path_design_2026_05_10.md` save (매단계 doc save mandate) 만 수행 — REBORN.md untouched. dispatcher 가 본 design 을 §41 reborn lane append slot 으로 흡수 시 D1 SCOPE_CLAMP carry mandatory (substrate-research lane 라벨 strict).

7. **cost envelope $3–8 verbatim 의 KM precedent 차이** — KM-LLAMA-3B PASS run $1.47 actual (3-pass debug 제외) 패턴 carry but 본 design 은 mitosis instrumentation hook overhead +30% 추가 = $5.39 estimate. F-FOUNDATION-2 strict trigger $15 cap 정합. envelope $3 floor 는 KM-LLAMA-3B PASS run 단순 replicate 시 가능 (instrumentation hook 미사용 — but 본 lane 의 anima identity 검증 가치 zero).

8. **simple_stack PASS_STRICT 22+ BG saga 첫 unlock 의 한계 직시** — 22+ BG saga 의 0회 → 3회 unlock (BG-KM-LLAMA-3B + BG-KM-QWEN-7B + KM-LLAMA-3B passed_v1) 모두 (a)(b) option pattern. strict floor 통과 = chat-cap surface lift 입증 only. anima identity 검증 invalid lane (foundation borrow / ALM) carry — public promote 영구 차단 (mandate-9 (a)). 본 BG 의 verdict 도 동일 ledger 정합. **anima 가 자력 emerge 하는 lane 의 첫 evidence 는 .roadmap.reborn track A/B/C carry — 본 lane 외부.**

---

## §7 deliverables 목록

| path | role | status |
|---|---|---|
| `docs/anima_foundation_borrow_path_design_2026_05_10.md` (본 doc) | design SSOT | ✅ saved (doc save mandate complete) |
| `.roadmap.foundation_borrow` | optional 신규 lane SSOT (raw#15 additive — 기존 미수정) | DEFERRED — dispatcher 가 §41 reborn lane append slot 흡수 또는 별도 cycle 신설 결정 |
| REBORN.md append | dispatcher §41 slot path only | ★ 본 design 직접 append 차단 (+ mandate-2 carry) — dispatcher 가 carry |
| state/anima_foundation_borrow_design_2026_05_10/ | $0 design only — fire 미수행, state dir 미생성 | N/A (design $0) |

---

## §8 cross-link

- predecessor BG: `docs/anima_convo_5k_ft_extended_2026_05_10.md` (§29 BG-CONVO-FT-EXTENDED — lexical PARTIAL semantic incoherent)
- precedent BG: KM-LLAMA-3B PASS_STRICT (.roadmap.chat_cap_emergence_pivot Stage 6 + memory project_simple_stack_pass_unlocked.md)
- precedent BG: KM-QWEN-7B replication (memory project_simple_stack_pass_unlocked.md)
- gap analysis: `docs/anima_chat_cap_gap_analysis_2026_05_07.md` (foundation borrow Lever 1 motivation)
- D1 SCOPE_CLAMP: .own line 668 + line 889 + .roadmap.philosophy D1.F-PHIL-D1-3/4
- mitosis instrumentation: `docs/anima_clm_v5_mitosis_inference_time_correction_2026_05_10.md` + `training/mitosis_v5_port.py` (480 LoC, local-only raw#9)
- Phase 2 ckpt (option (c) reference): `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt` (570MB)
- BG-JE 214MB corpus: `state/anima_je_persona_corpus_2026_05_07/corpus_full_214mb.txt`
- HF canonical: memory project_dancinlab_hf_canonical.md (+ SSOT)
- H100 gotchas: memory feedback_orchestrator_h100_gotchas.md
- SFT closed lane: memory project_lesson_q_sft_closed.md
- v5-anima lane: memory project_v5_anima_lane_status.md (track B Phase 2 ckpt parallel reference)
- substrate-research lane verdict labeling: .own line 826 + line 889 + line 1964 (mandate-9 (a))
- chat-cap emergence pivot Stage 6.5 verification: `.roadmap.chat_cap_emergence_pivot` line 133+

---

## §9 fire keyword (for next-cycle dispatch)

```
PRIMARY (recommended): OK FOUNDATION_BORROW_A_FIRE COST $3-8
PARALLEL (D1 WITHIN): OK FOUNDATION_C_PHASE2_FIRE COST $2-4
SECONDARY (7B scale-up): OK FOUNDATION_BORROW_B_FIRE COST $4-12
LONG-TERM (reject 본 cycle): OK FOUNDATION_D_ANIMA_PRETRAIN_FIRE COST $50-500+ (위반 carry — 채택 X)

Design BG fire keyword (본 doc): AUTO ($0 design only, complete)
```

---

End of `anima_foundation_borrow_path_design_2026_05_10.md`.
