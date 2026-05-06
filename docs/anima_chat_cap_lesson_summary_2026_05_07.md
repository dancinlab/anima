# anima chat-cap 5 cumulative failure modes — lesson summary 2026-05-07

## 5 failure mode replication (anima-native byte-level 18M-27M scale)

| # | BG | corpus | strategy | failure mode | V1 verdict | V2 verdict |
|---|---|---|---|---|---|---|
| 1 | BG-FY | corpus_ko_heavy 246MB (62% Hangul, ~30% chat-template) | pre-train only 18M | named-speaker leak (서연/유진/하은) | PARTIAL_PASS | PARTIAL_PASS_NO_CONTEXT |
| 2 | BG-HA | corpus_chat_template 236MB (47% Hangul, 30% chat-template) | pre-train only 18M | nonsense Korean chain (false PASS via narrow V1) | SIMPLE_STACK_PASS (false) | PARTIAL_PASS_NO_CONTEXT_v2 |
| 3 | BG-HF | corpus_sft_only 51MB (100% chat-format) | SFT-only 27M (loss masking 부재) | degenerate single-byte filler 0xFF/?/#/:/\n collapse | FAIL | V2_FAIL |
| 4 | BG-HJ | BG-HA Stage1 + corpus_sft_only Stage2 (loss masked) | two-stage 18M lr=1e-5 × 2K | KO-fluent nonsense (Stage 1 domain prior 부재) | PARTIAL_PASS 4/5 (false) | V2_FAIL 0/5 |
| 5 | BG-HK | corpus_persona_chat_template_v3 30MB (≥80% chat-template + 100% persona prefix) | persona-conditioned 18M × 8K steps | catastrophic overfit collapse (loss 0.013 → single-char filler) | step 800 PASS 10/10 (false) → step 1600+ FAIL | V2_FAIL 0/10 throughout |

## Convergent architectural ceiling evidence

3 corpus paradigms (236MB mixed / 51MB SFT-only / 30MB persona+chat≥80%) **ALL FAIL at 18M-27M ConsciousLM byte-vocab**:
→ **18M-27M byte-level scale is intrinsically chat-cap-limited, NOT corpus-quality-limited**
→ #115 architectural chat-incapability + Pβ + CLM v4 LoRA SFT failure modes 정합 convergent

## V2 evaluator validation ★

BG-HG retroeval 검증: V2 strict가 BG-FY + BG-HA 모두 false PASS auto-catch (BG-HA: 22 cell transitions, BG-FY: 6 cell transitions). V1 narrow C2.4 (named-speaker leak only) → V2 strict (named-speaker + domain keyword + Korean particle + ending + non-degenerate)로 보강 mandate.

## 5 핵심 lessons → 새 paradigm idea

### Lesson A: 18M scale exhausted (capacity ceiling)
→ **H_153: capacity scaling 100M+ ConsciousLM byte-level** (same corpus, capacity-only ablation)

### Lesson B: byte-level vocab inadequate at this scale
→ **H_154: BPE tokenizer shift 18M** (abandon byte-level → 8K-32K BPE Korean tokenizer for sample efficiency)

### Lesson C: corpus quality alone insufficient
→ **H_156: capacity × corpus crossed ablation matrix** (18M/27M/100M × {30MB/100MB/300MB} — 4-cell minimum)

### Lesson D: overfit memorization at small corpus + medium steps
→ **H_155: regularization sweep** (label smoothing 0.1 + WD 0.1 + dropout 0.4 + early stopping at val loss plateau) — overfit prevention

### Lesson E: V2 strict evaluator working as designed
→ **adopt V2 strict as default** for all anima-native chat-cap evaluation cycles
→ V1 narrow C2.4 retired (named-speaker leak only inadequate)

### Lesson F: persona prefix not collapse-resistant
→ persona-conditioned alone insufficient; capacity + regularization + crossed-ablation 동반 필요

## Architectural lane shift recommendation

**byte-level small corpus paradigm exhausted → 2 lane shifts**:
1. **capacity scaling lane** (H_153): 100M+ params → BG-HQ ubu1 RTX 5070 또는 mac MPS reduced batch
2. **tokenizer lane** (H_154): BPE/SentencePiece Korean tokenizer → BG-HP mac local 18M with 8K BPE

**OR fall-through**:
3. **own 17 architectural admission**: anima-native 18M-27M byte-level chat-cap intrinsically impossible (#115 architectural ceiling) — chat-cap는 다른 lane (CLM v4 substrate-coupled emerge paradigm v11 G3, .roadmap.philosophy D3)으로 전환

## Honest C3 (raw#91 c3 ≥5)

1. 5 failure mode는 18M-27M byte-level 한정 — 100M+ scale 미land
2. corpus 30MB-246MB range 한정 — 1GB+ corpus 미land
3. tokenizer는 byte-level (vocab=256) 한정 — BPE/SentencePiece 미land
4. instruction-tuning loss masking variant은 BG-HJ 1 instance — additional sweep 미land
5. regularization sweep (label smoothing + WD + dropout high) 미land — overfit collapse 가설 검증 부재
6. architectural ceiling claim은 anima-native byte-level 18M-27M 한정 — 다른 architecture lane (BPE / 100M / federated) 검증 X
7. V2 evaluator 자체 검증은 BG-FY + BG-HA 2 instance — adversarial probing (V2 false NEGATIVE 가능성) 별도 cycle

## Cross-Links

- ledger: docs/anima_consciousness_check_simple_stack_2026_05_06.md (5 BGs row + 종합 verdict)
- evaluator V2 spec: docs/anima_own_18_evaluator_v2_strict_spec_2026_05_07.md
- V2 retroeval: state/anima_evaluator_v2_retroeval_2026_05_07/retroeval_verdict.json
- BG verdict.json:
  - BG-FY: state/anima_native_ko_small_ubu1_train_2026_05_06/verdict.json
  - BG-HA: state/anima_native_ko_chat_template_train_2026_05_07/verdict.json (DOWNGRADED)
  - BG-HF: state/anima_h093_sft_only_train_2026_05_07/verdict.json
  - BG-HJ: state/anima_h094_instruction_tuning_two_stage_2026_05_07/verdict.json
  - BG-HK: state/anima_h098_h101_persona_conditioned_train_2026_05_07/verdict.json
- own 18 (simple stack 4-cond strict) + own 19 (corpus priority) + own 20 (chat-template format) + own 21 (hypotheses SSOT)

## 다음 BG fire plan (2026-05-07 same session)

- **BG-HP**: H_154 BPE tokenizer shift — 18M with 8K-16K Korean BPE (architectural lane shift)
- **BG-HQ**: H_153 capacity scaling 100M+ ConsciousLM byte-level (capacity ablation, ubu1)
- **BG-HR**: H_155 regularization sweep — label smoothing + WD + high dropout 18M (overfit prevention)
