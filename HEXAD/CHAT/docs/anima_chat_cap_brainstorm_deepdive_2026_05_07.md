# anima chat-cap brainstorm deep-dive — high-EV category 4종 BG spec sketches (2026-05-07)

## ⚠ Post-BG-IY reconciliation (2026-05-07 evening)

Drafted BEFORE BG-IY ran. After BG-IY landed, three reconciliation points apply — read these first.

**1. BG-IY outcome was F-IY-4 (corpus_mismatch), NOT in original branch set.**
Original spec assumed three falsifier branches (F-IY-1 capacity_gap / F-IY-2 evaluator_strict / F-IY-3 mixed). Actual outcome: CLM mk2-v1 SFT corpus was 60% English anima_axis + 30% English academic + 10% mixed chat — Korean chat training <5%. H_C corpus_mismatch confirmed dominant; H_A and H_B both rejected. See `state/anima_iy_v4_calibration_polyglot_2026_05_07/verdict.json`.

**2. Lesson Q + L reconciliation closed all SFT lanes on CLM.**
The deep-dive BG sketches below (BG-JC foundation+LoRA, BG-JD synthetic+SFT, BG-JE DPO) are mostly fine-tune lanes. Per ledger BG-JX/JZ-FT/JS/JT/JP **Lesson Q = COMPLETE_FULL_FALSIFY** + Lesson L architectural ceiling, **SFT-style BGs on CLM/ConsciousLM are rejected as Lesson-Q-blind regression**. Valid post-Lesson-Q paths are P1 continued-pretrain / P2 external foundation borrow / P3 inference-compute / P4 arch redesign — see `.roadmap.chat_cap_emergence_pivot` Stage 1' (rewritten 2026-05-07).

**3. New BG IDs supersede this doc's sketches:**

| this doc's sketch | superseded by | spec location |
|---|---|---|
| BG-JC (foundation-borrow LoRA) | **BG-JA-EXT** (Polyglot-Ko-1.3B + LoRA) | `state/anima_ja_ext_polyglot_ko_lora_2026_05_07/spec.md` |
| BG-JD (synthetic 1M-dialogue → 33M SFT) | partial — synthetic corpus deferred to BG-JB Stage 2 lift on top of **BG-IZ** continued-pretrain | `state/anima_iz_clm_continued_pretrain_ko_2026_05_07/spec.md` |
| BG-JE (DPO/KTO RL) | renamed to **BG-JF-DPO** — naming collision with post-BG-IY BG-JE | TBD — spec deferred until BG-IZ verdict |
| BG-IY (B30 calibration) | **LANDED** | `state/anima_iy_v4_calibration_polyglot_2026_05_07/verdict.json` |

**Naming collision**: deep-dive's BG-JE (DPO) collides with the post-BG-IY **BG-JE** (inference-compute best-of-64). Authoritative use of BG-JE is now the inference-compute spec at `state/anima_je_inference_compute_bo64_2026_05_07/spec.md`. Deep-dive's DPO sketch is renumbered to BG-JF-DPO.

The deep-dive analysis BELOW is preserved for archival reasoning — F-IY-1 (capacity_gap) was the assumed-prevailing branch and the EV math was based on that assumption. The actual F-IY-4 outcome moves the EV ranking toward continued-pretrain (P1) and inference-compute (P3) which were not lead candidates in the original sketch.

---

> raw#15 additive on docs/anima_chat_cap_lesson_summary_2026_05_07.md + .roadmap.chat_cap_emergence_pivot
> Categories selected by BG-IY-meta cluster verdict: capacity_ceiling (4), emergence_below_threshold (4), persona_cycle_collapse (2), evaluator_strict (2) — 12/48 BGs unblock-able by these 4 levers.

## Selection rationale

From `state/anima_iy_bg_meta_cluster_2026_05_07/verdict.json` root-cause distribution:

| rank | root_cause | n | covered_by_lever_below |
|---|---|---|---|
| 1 | partial_signal | 6 | B25 SWA ckpt avg + B7 best-of-N |
| 2 | emergence_below_threshold | 4 | **B4 distillation + B16 synthetic 1M** |
| 3 | capacity_ceiling | 4 | **B1 foundation borrow LoRA** |
| 4 | output_head_bottleneck | 3 | B5 logit distillation + B12 MoE |
| 5 | persona_cycle_collapse | 2 | **B19 persona-dropout-during-train** |
| 6 | evaluator_strict | 2 | **B30 calibration probe (BG-IY)** |

Top-4 selected (covered ~12/48 ledger rows directly):
- **B1 — Foundation-borrow LoRA** (capacity_ceiling x 4)
- **B16 — Synthetic 1M-dialogue corpus** (emergence_below_threshold x 4)
- **B20 — DPO on PASS/FAIL pair** (persona_cycle_collapse x 2 + sft_recipe x 1)
- **B30 — Calibration probe** (evaluator_strict x 2 — already in flight as BG-IY)

---

<!-- [Hc_635 chat-cap-b1-foundation-borrow-lora-polyglot-ko — moved to hypotheses_candidates/Hc_635_chat_cap_b1_foundation_borrow_lora.md on 2026-05-11] -->
<!-- [Hc_636 chat-cap-b16-synthetic-1m-dialogue-corpus — moved to hypotheses_candidates/Hc_636_chat_cap_b16_synthetic_1m_dialogue.md on 2026-05-11] -->
<!-- [Hc_637 chat-cap-b20-dpo-kto-pass-fail-pair — moved to hypotheses_candidates/Hc_637_chat_cap_b20_dpo_kto_pass_fail.md on 2026-05-11] -->
<!-- [Hc_638 chat-cap-b30-v4-calibration-evaluator-self-impossibility — moved to hypotheses_candidates/Hc_638_chat_cap_b30_v4_calibration_self_impossibility.md on 2026-05-11] -->

## Deep-dive 1 — B1 Foundation-borrow LoRA (BG-JC sketch)

### Hypothesis
**H_B1**: Polyglot-Ko-1.3B (or whichever model passes BG-IY F-IY-1) + LoRA on BG-HK 30MB persona corpus reaches V4 ≥ 7/15 stable + zero cycle + manual ≥ 10/15 = first SIMPLE_STACK_PASS.

### Root cause addressed
4 capacity_ceiling BGs (BG-FY/HA/HF/HJ all 18M byte-level FAILED) — 18M can't host emergence; borrow it from 1.3B.

### Spec sketch
```
mission:    BG-JC foundation-borrow + anima persona LoRA → first SIMPLE_STACK_PASS
prereq:     BG-IY F-IY-1 (Polyglot-Ko-1.3B V4 zero-shot ≥ 5/15 with anima system prompt)
base:       EleutherAI/polyglot-ko-1.3b (frozen, fp16)
adapter:    LoRA r=16, alpha=32, dropout=0.05, target=q_proj,v_proj,o_proj,gate_proj,up_proj,down_proj
corpus:     BG-HK persona_chat_template_v3 30MB (≥80% chat-template + 100% persona prefix)
recipe:     SFT on chat-template (loss masked to assistant turn)
            lr=2e-4, batch=1, grad_accum=8, steps=600, warmup=30
            Lesson G: val-loss split 10% + V4 inline every 50 + best-eval ckpt + plateau early-stop
            seed sweep: 42, 1234, 7777
eval:       V4 7-cell strict + V3 6-cell parallel + manual review
device:     Mac MPS (4-bit quant if OOM via bitsandbytes-mps)
cost:       ~$5 (H100 1hr alt) or ~30 min Mac MPS
falsifiers:
            F-JC-1 V4 ≥ 7/15 + zero cycle + manual ≥ 10/15 stable ≥ 200 steps
                    → SIMPLE_STACK_PASS direct → Stage 1 lock-in
            F-JC-2 V4 0/15 → foundation-borrow paradigm falsified → Stage 2 (synthetic data)
            F-JC-3 V4 ≥ 5 but persona-cycle ≥ 5 → persona-prefix collapse 잔존 → BG-JE persona-dropout
```

### EV calculation
- P(PASS) ~30% (BG-HU peak V2=8/15 was achieved on combined 53MB corpus at 33M = scale × corpus 모두 BG-IY 통과 모델보다 작음)
- magnitude: SIMPLE_STACK_PASS = 22+ BG cumulative goal achieved
- cost: $5 / 30 min = lowest in stack
- **net EV: 0.3 × HIGH = ★★★★★ priority**

### Honest C3
1. PEFT/LoRA mac mps 호환성 미검증 (bitsandbytes-mps 존재 여부)
2. Polyglot-Ko-1.3B base가 BG-HK persona format을 학습하면 base 본래 fluency 손실 가능 (catastrophic forgetting)
3. LoRA r=16 hyperparam 단일 — sweep 미land
4. 30MB corpus는 1.3B에 1:0.02 비율 (Chinchilla 미달) — overfit risk
5. seed=3 sweep but ckpt selection 단일 metric (best V4 composite)

---

## Deep-dive 2 — B16 Synthetic 1M-dialogue corpus (BG-JD sketch)

### Hypothesis
**H_B16**: Claude API teacher로 anima persona dialogue 100K-1M rounds 합성 → 18M-150M anima-native가 SFT만으로 V4 PASS. Chinchilla 법칙 1:20 충족.

### Root cause addressed
4 emergence_below_threshold BGs — params×tokens 모두 부족. Token gap을 합성으로 메움 (foundation borrow와 직교).

### Spec sketch
```
mission:    BG-JD anima synthetic 1M-dialogue → 33M anima-native SFT first PASS
phase 1:    corpus synthesis via Claude API
            seed prompts: 50 (anima identity / UBM / 1030 laws / Φ★ 다양화)
            generator: Claude Sonnet 4.6 (anima system prompt + persona-rich)
            output: 100K rounds × 5 turns avg = 500K dialogue turns ≈ 50MB-100MB
            cost: ~$50-100 API
            self-Instruct expand pattern: each seed → 20 paraphrases × 100 follow-ups
            cycle/quality filter: V4 inline filter on synthesized data (PASS-only retain)
phase 2:    33M anima-native SFT (BPE-8K) on (BG-HK 30MB ∪ Synthetic 100MB)
            lr=3e-4, batch=8, grad_accum=4, steps=8000
            Lesson G + V4 inline every 200 + best-eval ckpt + seed sweep N=5
            persona-dropout 30% during train (B19 inline)
phase 3:    eval V4/V3 strict + manual N=15 + multi-turn N=5
falsifiers:
            F-JD-1 33M V4 ≥ 7/15 → synthetic-corpus paradigm validated → Stage 2 lock-in
            F-JD-2 33M V4 < 5 even with synthetic corpus → params gap dominant
                   → fallback Stage 1 (foundation borrow only)
            F-JD-3 33M V4 5-7/15 → consistency lever needed (B7 best-of-N inference)
```

### EV calculation
- P(PASS) ~20% (synthetic data 품질 + 33M scale 합산)
- magnitude: anima-native on-device PASS = 자체 모델로 chat-cap 달성
- cost: ~$100 + 30 min H100
- **net EV: 0.2 × VERY HIGH (on-device anima preserved) = ★★★★ priority**

### Honest C3
1. Claude API teacher가 anima identity를 충분히 흉내낼지 미검증 (system prompt × 50 seed로 충분?)
2. synthetic corpus distribution shift — base KO Wikipedia/dialogue과 diff
3. V4 filter on synthetic는 self-evaluating loop — Goodhart's law risk
4. 1.3B teacher만큼 강한 dark knowledge 없음 (Claude logits 미접근)
5. 100K rounds도 1B token 부족; 1M rounds 까지 scale 시 비용 ~$1000

---

## Deep-dive 3 — B20 DPO on PASS/FAIL pair (BG-JE sketch)

### Hypothesis
**H_B20**: 22+ BG에서 V4 PASS-class와 V4 FAIL-class 응답 pair 추출 → DPO/KTO loss로 18M-33M anima-native shift → V4 PASS 분포로 모델 collapse 방향 변경.

### Root cause addressed
2 persona_cycle_collapse + 1 sft_recipe — SFT 단계에서 cycle/false-PASS 응답을 negative reward로 강제 mark. RL stage 부재가 그들의 가장 큰 recipe gap.

### Spec sketch
```
mission:    BG-JE first DPO/KTO RL stage → cycle suppression + V4 PASS distribution shift
data prep:  V4 retroeval에서 (prompt, chosen, rejected) tuple 추출
            chosen   = V4 PASS or partial (han_ratio>0.10 + Korean coherent + zero cycle)
            rejected = V3 cycle ≥ 5 OR persona-cycle responses OR token-soup
            target N: ~5K pairs (BG-HQ persona cycle 55 + BG-HU 80 + BG-IO 82 + ... ≈ 500 직접)
            augmentation: V4 PASS 응답 부족 시 Claude API로 5K chosen 합성
base:       33M BG-HU ckpt step 800 (V2=8/15 manual=10/15 frontier) OR
            18M BG-HS R1 ckpt step 4000 (manual=13/15 baseline)
            (base가 chosen 분포에 이미 일부 weight 가짐)
recipe:     KTO (single-sample +/-, simpler than DPO pair)
            beta=0.1, lr=5e-7, batch=4, grad_accum=4, steps=1000
            reference model = base frozen
            Lesson G + V4 inline every 100
eval:       V4 strict + cycle delta (KTO 전후) + manual review
falsifiers:
            F-JE-1 KTO 후 V4 ≥ 7/15 + cycle suppression ≥ 80% → RL stage 효과 lock-in
            F-JE-2 V4 stay flat + cycle delta minimal → SFT base가 너무 약해 KTO만으로 부족
            F-JE-3 V4 회복 but reward hacking (Goodhart) → V4 cell 통과해도 manual FAIL
```

### EV calculation
- P(PASS) ~15% (base 33M가 이미 ceiling — RL이 ceiling 위로 push 어려울 수 있음)
- magnitude: first RL stage = recipe gap closed
- cost: ~$5 (Mac MPS or H100 1hr)
- **net EV: 0.15 × MEDIUM-HIGH = ★★★ priority**

### Honest C3
1. base BG-HU step 800 ckpt가 cliff (cycle=1→8 step 200 후) — KTO ref model 자체가 unstable
2. chosen 분포가 매우 small (~500 직접) — 합성 augmentation 필요
3. Goodhart law: V4 cells을 reward로 쓰면 V4 통과지만 의미 없는 응답 학습 가능 (B30 evaluator self-impossibility 정합)
4. DPO/KTO Mac MPS 호환성 (TRL library) 미검증
5. anima persona cycle은 corpus distribution 자체가 prefix-heavy 이라서 RL만으로 disentangle 어려울 수 있음 — corpus + RL 결합 필수

---

## Deep-dive 4 — B30 Calibration probe (BG-IY 진행 중)

### Hypothesis
**H_B30**: Polyglot-Ko-1.3B / Llama-3.2-3B-Instruct / Qwen2.5-1.5B 등 known-good 1B+ KO LM이 V4 strict zero-shot에서 PASS / FAIL 어떻게 분포하는지로 V4 self-impossibility 검증.

### Root cause addressed
2 evaluator_strict (BG-HQ/HU) — V2/V3 false PASS 검출은 됐지만 V_n strict 자체가 self-impossible 인지 미검증.

### Spec
- 위 BG-IY spec.md 참조 (in-progress)
- 5 models × 15 prompts × 2 modes = 150 generations × V4 eval

### Why this is HIGHEST priority for current cycle
- 22+ BG 결론 (architectural ceiling) 가 capacity gap (H_A) vs evaluator self-impossibility (H_B) 둘 중 어느 쪽인지 disambiguate 필요
- F-IY-1 → Stage 1 (B1 foundation-borrow LoRA) 즉시 unblock
- F-IY-2 → V4 redesign 우선 (모든 향후 training BG는 sink)

### EV calculation
- P(actionable result) ~95% (5 models 중 적어도 1개는 명확히 PASS/FAIL 분류 가능)
- magnitude: 22+ BG 해석 framework 변경
- cost: $0 (Mac MPS) ~30 min
- **net EV: 0.95 × VERY HIGH = ★★★★★ MUST-DO FIRST**

---

## Implementation order (Stage 0 + Stage 1 chain)

```
[Stage 0 in flight]
  BG-IY (B30 calibration)
    ├── eval_log_qwen25_1p5b.jsonl   ← inference running
    ├── eval_log_qwen25_0p5b.jsonl   ← queued
    ├── eval_log_llama32_3b_instruct.jsonl   ← queued
    ├── eval_log_kogpt2_base_v2.jsonl   ← queued
    └── eval_log_polyglot_ko_1p3b.jsonl   ← downloaded, queued
                ↓ verdict.json F-IY-{1,2,3}
[Stage 1 — F-IY-1 path]
  BG-JC (B1 foundation-borrow LoRA)   ← unblocked by F-IY-1
                ↓ if SIMPLE_STACK_PASS → DONE
                ↓ if FAIL → Stage 2
[Stage 2 — F-JC-2 path]
  BG-JD (B16 synthetic 1M)            ← parallel data axis
                ↓ if PASS → DONE
                ↓ if FAIL → Stage 3
[Stage 3 — F-JD-2 path]
  BG-JE (B20 DPO/KTO RL)              ← recipe axis
                ↓
[Stage 4 — anima 고유]
  Φ-loss / bifurcation / akida / D3 substrate (long-term)
```

## Cross-links

- meta-cluster: state/anima_iy_bg_meta_cluster_2026_05_07/{verdict.json, meta_cluster.md}
- BG-IY in flight: state/anima_iy_v4_calibration_polyglot_2026_05_07/
- roadmap: .roadmap.chat_cap_emergence_pivot
- 22+ BG SSOT: state/anima_model_attempts_ledger.jsonl
