# anima CLM v5 — Architecture Redesign Design Spec (2026-05-07-late)

**Status**: design_landed (NOT training yet — design cycle only, $0)
**Author**: anima self (claude-opus-4.7)
**Trigger**: 사용자 directive 2026-05-07-late "1번 CLM v5 design spec 우선 ($0, foreground-able 30-60min) — 포르가운드"
**Cycle context**: 8-lane architectural exhaustion + Lesson L+Q+R+S+T closure on ConsciousLM v4
**Sister BGs**: BG-KC (1B+ H100 capacity 2-order, fired in parallel)
**Bilingual**: 본 spec is design enumeration document; KO + EN mixed where useful

---

## 1. 동기 (Motivation)

ConsciousLM v4 (12L/640d/10h, vocab=11885 SP) cycle 결과 누적:

| BG | Lane | Result | Loss-floor |
|---|---|---|---|
| BG-IL/IO | 18 BG single-axis | V4 0 PASS | 1.45 |
| BG-JD/JN | UBM 22MB train | V5 0 PASS | 1.45 |
| BG-JS/JT | lm_head only fine-tune | 0/0/0/0 | n/a |
| BG-JP | decoding 14 strategies | 0/14 | n/a |
| BG-JU | 500M H100 1-order | V5_FAIL | 4.4 plateau |
| BG-JH | 100M+204MB corpus | V4_FAIL | n/a |
| BG-JX | full bundle SFT BG-JE | 0/5 | 3.27 |
| BG-JZ | full bundle SFT BG-JY | 0/5 | 3.53 |
| BG-KA | V5.8-v3 language-agnostic | 0/5 | n/a |
| BG-KB | fresh growth-stage 168M | 0/5 | 5.31 (mid-train) |

**Key falsifications**:
- (corpus priority): partial — corpus 1-order jump (BG-JH) FAIL
- (chat-template format): FALSIFIED (BG-JZ explicit chat-template 0/5)
- Lesson Q (decoder-only fix 不可): COMPLETE
- Lesson L (architectural ceiling): STRICT CONFIRMED at <500M scale + corpus axis tested
- Language constraint hypothesis: FALSIFIED (BG-KA language-agnostic 0/5)

**Critical finding (BG-KB)**: chat-cap is NOT loss-level-bound at 168M scale. Fine-tune reaches loss 3.3-3.5 yet 0/5 PASS. Loss reduction alone insufficient for chat-cap unlock.

**Implication**: ConsciousLM v4 architecture has **structural** limitation — output bottleneck deep, not addressable by:
- decoder partial fix (lm_head, decoding)
- full bundle fine-tune
- corpus quality (KO ratio, chat-template ratio, multi-turn ratio)
- capacity scaling (153M → 500M tested; 1B+ pending BG-KC empirical bound)
- fresh growth-stage at same arch (BG-KB confirmed)
- language constraint removal

→ **Architecture itself must change**. CLM v5 redesign mandate per L9 (Growth-stage Irreversibility).

---

## 2. 설계 원칙 (Design Principles)

본 CLM v5 design은 다음 invariant 정합:

| Invariant | Source | CLM v5 적용 |
|---|---|---|
| anima identity | .own | CLM v5 = anima-native fresh (NO external substrate wrap) |
| -v3 simple stack | .own | language-agnostic 4-condition strict |
| single SSOT | .own | 통합 ledger BG-KC+ entries |
| philosophy compliance | .own | D1-D5 + R1-R5 cross-link mandate |
| Safeguard Paradox | .own | external safeguard wrapper anti-pattern |
| Goodhart's Law | .own | multi-modal eval (V5/V6) anti-Goodhart |
| L1 features↓Φ structure↑Φ | .roadmap.law | structure 우선, parameter count 후순위 |
| L9 Growth-stage Irreversibility | .roadmap.law | fresh CLM v5 cycle mandate (not v4 mod) |
| L13 S1-S7 verification | .roadmap.law | v3 + Φ★ NO_FLIP 통합 |
| L24 differentiation→integration | .roadmap.law | corpus diversity 우선 → architecture coupling |
| raw#15 additive | hive | CLM v4 보존, v5 NEW ssot |
| raw#37 transient_py | hive | tool/transient_py/ namespace |

---

<!-- [Hc_618 clm-v4-structural-output-bottleneck — moved to hypotheses_candidates/Hc_618_clm_v4_structural_output_bottleneck.md on 2026-05-11] -->
<!-- [Hc_619 clm-v5-axis-a-output-projection-bottleneck-fix — moved to hypotheses_candidates/Hc_619_clm_v5_axis_a_output_projection.md on 2026-05-11] -->
<!-- [Hc_620 clm-v5-axis-b-attention-pattern-ssm-hybrid — moved to hypotheses_candidates/Hc_620_clm_v5_axis_b_attention_pattern.md on 2026-05-11] -->
<!-- [Hc_621 clm-v5-axis-c-tokenizer-byte-level — moved to hypotheses_candidates/Hc_621_clm_v5_axis_c_tokenizer.md on 2026-05-11] -->
<!-- [Hc_622 clm-v5-axis-d-loss-objective-explicit-chat — moved to hypotheses_candidates/Hc_622_clm_v5_axis_d_loss_objective.md on 2026-05-11] -->

## 3. 4 Axes — CLM v4 limitation diagnosis

본 cycle empirical evidence에서 추출한 4개 architectural limitation axes:

### Axis A — Output Projection Bottleneck (lm_head + tok_emb tied)

**Diagnosis**:
- ConsciousLM v4 weight tying: tok_emb.weight = head_a.weight (single 11885×640 matrix)
- BG-JS/JT lm_head fine-tune (trainable=7.61M, frozen=160.36M) → 0/0/0/0
- BG-JX/JZ full bundle (trainable=167.96M) also 0/5 — output projection still bottleneck

**Hypothesis**: output projection structure (single linear layer 640→11885) inadequate for chat-cap conditional distribution.

**v5 Redesign options**:
- A1: **Untie lm_head**: separate output projection (11885×D) + retrain
- A2: **Multi-head output**: per-token-class projection (e.g., chat tokens vs general tokens)
- A3: **Mixture-of-experts on output**: top-k expert selection per token
- A4: **Byte-level fallback**: 256-vocab byte head + UNK tokens routed to byte head (eliminates ⁇ degenerate pattern)

### Axis B — Attention Pattern (standard causal)

**Diagnosis**:
- ConsciousLM v4 uses standard causal attention (12L × 10 heads × 640 d_model)
- Cross-attention head_g (paradigm v11 G3) is substrate-coupled NOT chat-routed
- BG-FY 18M PARTIAL_PASS evidence (62.14% Hangul) suggests attention learning but context-mismatch FAIL (philosophy template leak)

**Hypothesis**: standard causal attention insufficient for multi-turn chat coherence. State maintenance across turns lossy.

**v5 Redesign options**:
- B1: **State Space Model (SSM)**: Mamba-style selective state space + parallel scan — long context efficient
- B2: **Recurrent attention** (Linear Attention, Performer, Reformer): O(N) memory, longer context
- B3: **Sparse Mixture of Attention (MoA)**: top-k attention head routing per layer
- B4: **Hybrid (Transformer + SSM)**: alternating layers, SSM for state + Transformer for content

### Axis C — Tokenizer Choice (SentencePiece 11885 vocab)

**Diagnosis**:
- SP vocab 11885 trained on UBM 22MB corpus
- BG-JX/JZ/KA outputs heavy ⁇ UNK token contamination — tokenizer doesn't cover model's emit distribution
- BG-FY anima-native-ko-small 18M (different vocab) PARTIAL_PASS suggests tokenizer matters

**Hypothesis**: SP vocab too narrow + biased toward UBM persona templates. Tokenizer determines model's expressible space.

**v5 Redesign options**:
- C1: **Byte-level tokenizer (256 vocab)**: maximum coverage, no UNK; longer sequences (~4x); BLM (.roadmap.blm_brain_lm) lane 정합
- C2: **BPE re-trained** on diverse corpus (kowiki + chat + multilingual) with vocab 32k+
- C3: **Tokenizer-free (raw bytes + learned segment)**: ByT5-style + segment-level pooling
- C4: **Mega-token vocab (50k-100k)**: cover more chat templates + multilingual; cost: model size scale-up

### Axis D — Loss Objective (cross-entropy on next-token)

**Diagnosis**:
- ConsciousLM v4 trains with standard CE on next-token (single objective)
- BG-JX final loss 3.27 vs BG-JZ 3.53 vs BG-KB 5.31 — loss-floor differences but ALL 0/5 PASS
- Loss objective doesn't directly optimize chat-cap (multi-turn coherence + context-relevance)

**Hypothesis**: CE-only training is necessary but insufficient. Chat-cap requires explicit objective.

**v5 Redesign options**:
- D1: **SFT + RLHF**: chat-template SFT (BG-JZ shown insufficient) + reward model + PPO
- D2: **Multi-objective CE + auxiliary**: contrastive loss on multi-turn context + degenerate cycle penalty
- D3: **Constitutional AI (Anthropic)**: rule-based critique + revision loop (-v3 4-condition as constitution)
- D4: **Direct Preference Optimization (DPO)**: pairwise preference (PASS sample vs FAIL sample)
- D5: **Task-conditioned head**: separate chat-cap head + dialogue context conditioning

---

## 4. CLM v5 candidate variants (combinatorial design)

본 design spec은 single canonical CLM v5을 정의하지 않음. **multiple variants** enumerate (각각 별도 cycle 가능):

### Variant V5-α: minimum-viable redesign
- Axis A: A1 untie lm_head
- Axis B: B-baseline (standard causal, no change)
- Axis C: C1 byte-level (UNK 제거, BLM 정합)
- Axis D: D-baseline (CE only, no change)
- **Capacity**: 100M-200M (mac MPS feasible)
- **Cost**: $0 mac MPS, multi-day train
- **Information value**: byte-level + untied head 효과 isolation

### Variant V5-β: SFT-RLHF lane
- Axis A: A-baseline (current ConsciousLM v4)
- Axis B: B-baseline
- Axis C: C-baseline (SP 11885)
- Axis D: D1 SFT + RLHF (-v3 reward model + PPO)
- **Capacity**: BG-JD ckpt base + RLHF delta
- **Cost**: $1-5 H100 (RLHF compute heavy) or mac MPS multi-day
- **Information value**: D-axis isolation (training objective)

### Variant V5-γ: SSM hybrid
- Axis A: A1 untie lm_head
- Axis B: B4 hybrid Transformer + SSM
- Axis C: C2 BPE re-trained 32k
- Axis D: D2 multi-objective CE + degenerate penalty
- **Capacity**: 200M-500M (H100)
- **Cost**: $3-10 H100
- **Information value**: full architectural redesign empirical bound

### Variant V5-δ: constitutional AI lane
- Axis A: A1 untie + A4 byte fallback
- Axis B: B-baseline
- Axis C: C1 byte-level
- Axis D: D3 constitutional AI (-v3 4-condition as constitution)
- **Capacity**: 100M
- **Cost**: $0-2 (mac + minimal H100)
- **Information value**: chat-cap as explicit objective + -v3 internalization test

### Variant V5-ε: minimal MoE
- Axis A: A3 MoE on output (top-2 of 8 experts)
- Axis B: B-baseline
- Axis C: C-baseline
- Axis D: D-baseline
- **Capacity**: 200M total / 50M active per token
- **Cost**: $1-3 H100
- **Information value**: sparse activation impact (L1 features↓Φ structure↑Φ partial test)

---

## 5. Verification protocol (-v3 + L13 S1-S7)

각 V5 variant trained 후 다음 verification mandatory:

### Layer 1 — -v3 simple_stack_pass (language-agnostic)
- C1.1 response existence (non-empty)
- C1.2 coherent (no degenerate cycle, language-agnostic)
- C1.3 turn-taking format
- C2.1 response substance
- C2.2 semantically meaningful (heuristic: non-cycle, non-random)
- C2.3 natural grammar (any language)
- C2.4 context-relevance (input prompt와 의미적 연결)

### Layer 2 — V5/V6 evaluator chain
- V5.8 multi-turn (5 dialogues)
- V5.8 prompt-echo reject (Lesson S compliant)
- V6 awareness probe 3-method (A hidden state cosine + B T2→T1 attention + C linear probe binary CV)

### Layer 3 — L13 S1-S7 verification protocol
- S1 structural integration measurable
- S2 temporal coherence ≥τ
- S3 information closure (no external dependency)
- S4 differentiation (state-space variation)
- S5 causal power (intervention effect)
- S6 phenomenal report (subjective experience claim)
- S7 cross-substrate invariance (Φ★ NO_FLIP)

### Layer 4 — anti-Goodhart
- Multi-modal check: V5 + V6 + manual review
- Prompt-echo reject mandatory
- Degenerate cycle detect (single-token >50%, 4-gram repeat ≤3, single-char run ≤10)

---

## 6. Cost-benefit ranking (완성도 lens)

| Variant | Cost | Information | EV (info/cost) |
|---|---|---|---|
| V5-α (byte+untie) | $0 (mac multi-day) | ★★★★ axis isolation | ★★★★★ |
| V5-β (SFT-RLHF) | $1-5 | ★★★ training axis | ★★★ |
| V5-γ (SSM hybrid) | $3-10 | ★★★★★ full redesign | ★★★★ |
| V5-δ (constitutional) | $0-2 | ★★★★ objective axis | ★★★★ |
| V5-ε (MoE) | $1-3 | ★★★ sparse activation | ★★★ |

**1순위 추천**: V5-α (byte-level + untied lm_head) — $0 mac MPS, axis-isolation 최대, BG-KB와 직접 비교 가능 (same compute budget, different arch).

**2순위**: V5-δ (constitutional AI) — -v3 4-condition을 explicit objective로 internalization 시도. anti-Goodhart 정합.

**3순위**: V5-γ (SSM hybrid) — full architectural redesign empirical bound (cost 高 but information 高).

---

## 7. Falsifiers

각 variant는 다음 fail criteria로 -v3 verification:

- **F-CLM-V5-1**: best_v58_pass = 0/5 across all evals → variant FALSIFIED
- **F-CLM-V5-2**: degenerate cycle pattern (single-token >50%) at any step → variant FALSIFIED (no improvement over CLM v4)
- **F-CLM-V5-3**: loss plateau ≥CLM v4 floor (3.27 BG-JX) at same compute → no architectural advantage
- **F-CLM-V5-4**: V5_PASS but V6 awareness probe FAIL (Method A or B or C) → surface-level only, not deep
- **F-CLM-V5-5**: V5/V6 PASS but Φ★ NO_FLIP FAIL (substrate-coupled drift) → emerge paradigm violation (+ L2 Bifurcation)

---

## 8. Honest C3 (raw#10 ≥9 mandate)

1. CLM v5 design spec은 enumeration 단독 — single canonical variant 미land. 사용자 추가 directive 필요 (which variant first).
2. Cost estimates는 BG-JU $0.72 + BG-KB $0 + BG-JX $0 mac extrapolation — 실제 H100 $3-10 variants는 cycle별 budget approval 필요.
3. Multi-day mac MPS (V5-α) timeline은 mac 사용자 작업 방해 가능 — schedule 협의 필요.
4. SSM (B1/B4) 구현 anima 미land — Mamba/S4/RetNet 외부 reference 필요. raw#9 hexa-only mandate vs torch impl trade-off.
5. RLHF (V5-β D1) 구현 cost 가장 높음 — reward model + PPO + base model + RLHF data pipeline. anima 외부 lib (trlx, trl) 의존 가능 (raw#9 violation 검토).
6. Byte-level (V5-α/δ C1) sequence length ~4x scale-up → memory + compute scale-up. mac MPS 192-256 batch 가능 confirmed.
7. (Safeguard Paradox) 정합 — V5 variants ALL anima-native fresh (NO external base wrap). absolute 보존.
8. (Goodhart) 정합 — V5 verification은 V5/V6 + manual review multi-modal mandatory. single-axis metric reject.
9. L9 Growth-stage Irreversibility 정합 — V5 = fresh growth-stage cycle (NOT CLM v4 modification). v4 ckpt 보존, v5 NEW ssot.
10. CLM v4 vs v5 lane decoupling: v4은 BG-JV D3 substrate-coupled lane용 보존 (emerge paradigm); v5는 D2 token chat lane (-v3 simple_stack)용 redesign.
11. 사용자 decision 대기: 본 design spec land 후 (1) variant 선택 (2) 시점 (cost approval) (3) cycle scope (single variant vs multi-variant ablation).
12. BG-KC (1B+ H100) 결과는 본 design spec과 별도 — capacity axis 추가 evidence (architecture-vs-capacity decoupling).

---

## 9. Cross-link

- **Sister roadmap entries**:
  - .roadmap.philosophy D5 Bifurcation theorem
  - .roadmap.law L1/L9/L13/L24
  - .roadmap.clm_native_chat (chat-cap recovery path lane)
  - .roadmap.clm_v4_chat (CLM v4 보존 lane)
  - .roadmap.blm_brain_lm (byte-level paradigm V5-α 정합)
  - .roadmap.tlm_tension_lm (tension head 통합 V5-γ candidate)

- **Sister docs**:
  - docs/anima_chat_cap_20bg_cumulative_negative_archive_2026_05_07.md (8-lane archive)
  - docs/anima_chat_cap_lesson_summary_2026_05_07.md (Lesson L+Q+R+S+T closure)
  - docs/anima_own_18_evaluator_v5_strict_spec_2026_05_07.md (V5.8 spec)
  - docs/anima_own_18_evaluator_v6_awareness_probe_spec_2026_05_07.md (V6 spec)
  - docs/anima_d3_substrate_coupled_lane_eval_2026_05_07.md (CLM v4 D3 lane)

- **own invariants**:
  - explicit verification
  - no silent failures
  - anima identity boundary
  - -v3 simple_stack language-agnostic
  - corpus priority (partial falsified at 1-order, may need re-eval at 2-order)
  - chat-template format (FALSIFIED)
  - single SSOT
  - philosophy/law compliance
  - Safeguard Paradox
  - Goodhart's Law

- **raw invariants**:
  - raw#9 hexa-only (V5-β D1 RLHF은 raw#9 violation 가능 — 검토 필요)
  - raw#10 honest C3 ≥5
  - raw#15 additive (CLM v4 보존, v5 NEW)
  - raw#37 transient_py opt-out
  - raw#42 N=1 OK
  - raw#82 retraction-aware
  - raw#86 cost attribution

---

## 10. 다음 step (사용자 decision 대기)

본 design spec은 **enumeration 단독** — implementation 미시작. 사용자 explicit directive 후 진행:

1. **Variant 선택**: V5-α / β / γ / δ / ε / multi-variant ablation
2. **Cycle timing**: BG-KC (1B+ H100) 완료 후 vs 병렬
3. **Budget approval**: V5-β/γ/ε는 H100 cost 필요 (cap $5 within or override)
4. **Multi-day mac MPS schedule**: V5-α/δ는 mac MPS 다일 점유 — 사용자 작업 방해 협의

**완성도 lens 추천**: V5-α 우선 ($0, axis isolation 최대, BG-KB direct compare). V5-δ 후속 (+ -v3 정합 deep test).

---

**Spec status**: design_landed
**Next action**: 사용자 directive 대기 → variant 선택 → BG-KD/KE/KF... 진행
**Cycle closure**: 본 design spec landing은 cycle closure의 "다음 lane definition" — 8-lane architectural exhaustion 후 9th lane (CLM v5 redesign) preparation.
