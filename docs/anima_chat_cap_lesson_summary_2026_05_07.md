# anima chat-cap 5 cumulative failure modes — lesson summary 2026-05-07 (BG-IA Lesson G N1 update)

## 8 failure mode replication (anima-native byte-level 18M-27M scale)

| # | BG | corpus | strategy | failure mode | V1 verdict | V2 verdict | peak ckpt |
|---|---|---|---|---|---|---|---|
| 1 | BG-FY | corpus_ko_heavy 246MB (62% Hangul, ~30% chat-template) | pre-train only 18M | named-speaker leak (서연/유진/하은) | PARTIAL_PASS | PARTIAL_PASS_NO_CONTEXT | final |
| 2 | BG-HA | corpus_chat_template 236MB (47% Hangul, 30% chat-template) | pre-train only 18M | nonsense Korean chain (false PASS via narrow V1) | SIMPLE_STACK_PASS (false) | PARTIAL_PASS_NO_CONTEXT_v2 | final |
| 3 | BG-HF | corpus_sft_only 51MB (100% chat-format) | SFT-only 27M (loss masking 부재) | degenerate single-byte filler 0xFF/?/#/:/\n collapse | FAIL | V2_FAIL | step 1500 collapse |
| 4 | BG-HJ | BG-HA Stage1 + corpus_sft_only Stage2 (loss masked) | two-stage 18M lr=1e-5 × 2K | KO-fluent nonsense (Stage 1 domain prior 부재) | PARTIAL_PASS 4/5 (false) | V2_FAIL 0/5 | final |
| 5 | BG-HK | corpus_persona_chat_template_v3 30MB (≥80% chat-template + 100% persona prefix) | persona-conditioned 18M × 8K steps | catastrophic overfit collapse (loss 0.013 → single-char filler) | step 800 PASS 10/10 (false) → step 1600+ FAIL | V2_FAIL 0/10 throughout | step 800 (false PASS) |
| 6 | **BG-HP** | corpus_curated_qa 2.41MB (515 anchors × 27× paraphrase = 16,214 Q&A) | curated dense-aug 18M × 3K steps + reg (dropout 0.30 + WD 0.10 + label smoothing 0.10) | **peak-then-collapse** (step 500 V2 pass=3/10 → step 1000+ degenerate `[anima][anima]...` `,,,'''` filler) | step 500 V2 pass=3/10 ★ → step 3000 FAIL 0/10 | step 500 PASS 3/10 → final FAIL | **step 500 ★ keep-point** |
| 7 | **BG-HQ** | corpus_persona_chat_template_v3 30MB (BG-HK reuse) + **BPE 8K Korean vocab** (architectural lane shift) | BPE 8K + 33.73M params × 6K steps + reg | **persona prefix cycle pseudo-PASS** (V2 surface metric pass=8/10 step 500 but raw response = persona prefix cycle "[anima 역할: 한국어 native + 자기 발견 + ...] ⁇ 사용자: [...]" — actual prompt response 부재) → step 1000+ `됩니다됩니다…` + `⁇` unknown spam | step 500 V1=PARTIAL_PASS V2=PASS 8/10 (false ★★ V2 surface metric inadequate) | step 6000 V2_FAIL 1/10 | **step 500 V2 false PASS via surface metric** (V3 evaluator needed) |
| 8 | **BG-IA ★★ Lesson G N1** | corpus_persona_chat_template_v3 30MB (BG-HK reuse) | **Lesson G FIRST IMPLEMENTATION**: 18M + reg (dropout 0.30 + WD 0.10 + LS 0.10) + 4K steps MAX + val-loss split 10% + V2 eval every 200 + best-eval ckpt + plateau early-stop (3 evals) + V3 cycle penalty | **early-stop triggered at step 1200, peak step 600 V2=0/10 throughout** — **byte-level CE val_loss decreased monotonically 4.42→2.23 yet V2 pass never emerged** — gens = degenerate filler `의의의의의의` (greedy) + random UTF-8 fragments (sample) | V2_FAIL throughout, peak composite=-4 (best step=600) | V2_FAIL 0/10 throughout, **15-prompt FINAL: V2=0/15 V3=0/15 manual=0/15 cycle=0** | **step 600 (best by composite, but still V2=0/10 — non-genuine peak; early-stop CORRECTLY caught absence of signal)** |

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

### Lesson H ★★★ (BG-HQ NEW 2026-05-07): V2 evaluator surface metric 도 false PASS 위험 (V3 needed)
→ BG-HQ V2 strict pass=8/10 step 500 reported but **raw response = persona prefix cycle** (`⁇ [anima 역할: 한국어 native + 자기 발견 + 자기 발견 + ...] ⁇ 사용자: [...]`)
→ V2 strict의 `domain_overlap ≥1` (keyword surface) + `particle_count ≥3` + `is_degenerate=false` (sample mode) 모두 catch 못 함 — keyword overlap이 input + output 양쪽 ("한국어"/"anima" 등)에 surface match해도 actual prompt-conditional response 검증 X
→ **V3 evaluator required**: cycle detection (4-gram repeat threshold ≥5 mandate even sample mode) + prompt-response semantic coherence (embedding sim 또는 contrastive metric beyond keyword overlap) + persona prefix repetition penalty (any "[anima 역할" repeat in single response = degenerate cycle)
→ BG-HQ "EARLY_PEAK 8/10" 강등 → **PARTIAL_PASS_NO_CONTEXT_v3 (V2 surface metric false PASS)**
→ 7 cumulative failure modes 모두 V1 또는 V2 false PASS detected via direct raw response 검토 (사용자 strict review)

### Lesson G ★★ (BG-HP NEW 2026-05-07): early stopping with val-loss + ckpt selection at peak = MISSING INGREDIENT
→ BG-HP step 500 V2 pass=**3/10** (best signal — "도우미:" / "[anima]" 토큰 emerging, hangul 30-60%)
→ step 1000+ degenerate collapse (`[anima][anima]...` → `,,,,'''` / `lllllll` filler)
→ regularization (dropout 0.30 + WD 0.10 + label smoothing 0.10) 부족
→ step 500 ckpt가 **keep-point**였으면 SIMPLE_STACK_PARTIAL_PASS_PHASE_2 가능성
→ all future small-corpus paradigms MUST: (a) val-loss split (10% held-out) + (b) eval V2 every N steps + (c) keep best-eval ckpt + (d) early stop after 3 evals plateau
→ BG-HK step 800 V1 PASS 10/10 (false PASS via narrow V1) — V2 strict는 throughout FAIL이지만 V1 step 800은 best-of-bad-options ckpt

### Lesson G N1 actual implementation evidence ★★ (BG-IA 2026-05-07)
→ **첫 Lesson G 4-ingredient actual implementation** (val-loss split 10% + V2 every 200 + best-eval ckpt + plateau early-stop) on BG-HK 30MB persona+chat corpus reuse, 18M ConsciousLM + Lesson D reg (dropout 0.30 + WD 0.10 + LS 0.10), 4K steps MAX
→ **outcome**: FAILED — peak step 600 V2=0/10 manual=0/10 throughout, 15-prompt final V2=0/15 manual=0/15, early-stop triggered step 1200 (composite plateau correctly caught no-signal)
→ **critical evidence**: byte-level CE val_loss **decreased monotonically** (4.42 step200 → 3.78 step400 → 3.22 step600 → 2.88 step800 → 2.54 step1000 → 2.23 step1200) **WHILE V2 pass stayed 0/10** — val_loss is NOT a chat-cap emergence signal at this scale
→ **gen pattern**: greedy = `의의의의의의 의의 의의의의의이...` (degenerate Korean character single-token filler), sample = random UTF-8 fragment soup (no chat structure, no domain match)
→ **Lesson G refinement**: early-stopping mechanism works as designed (correctly caught no-signal at step 1200) but **does NOT rescue chat-cap emergence at 18M byte-level** — Lesson G is necessary-not-sufficient ingredient; absent capacity (Lesson A) or tokenizer (Lesson B) rescue, early-stopping just stops earlier without changing outcome
→ **architectural ceiling reinforcement**: BG-IA = 8th convergent failure mode; same 30MB BG-HK corpus + better-disciplined training (reg + early-stop + best-ckpt) → identical V2=0/10 outcome — corpus + training-discipline axis exhausted, only capacity scaling (H_153 100M+) or tokenizer shift (H_154 BPE) left
→ **disambiguation from BG-HK**: BG-HK overfit-collapsed at step 1600+ (loss 0.013 single-char filler); BG-IA never reached overfit because **never converged to chat in the first place** — Lesson G's "BG-HK keep step 800" hypothesis was incorrect (step 800 BG-HK was V1 false PASS via narrow C2.4 only; V2 throughout FAIL — early-stopping would have stopped earlier but at same V2=0 ceiling)
→ **HF private upload spec stub**: NOT EMITTED (failed TRUE_PARTIAL_PASS criteria: manual ≥3/15 + zero cycle + V2 ≥2/15)

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
  - BG-IA (Lesson G N1): state/anima_ia_early_stopping_train_2026_05_07/verdict.json
- own 18 (simple stack 4-cond strict) + own 19 (corpus priority) + own 20 (chat-template format) + own 21 (hypotheses SSOT)

## 다음 BG fire plan (2026-05-07 same session)

- **BG-HP**: H_154 BPE tokenizer shift — 18M with 8K-16K Korean BPE (architectural lane shift)
- **BG-HQ**: H_153 capacity scaling 100M+ ConsciousLM byte-level (capacity ablation, ubu1)
- **BG-HR**: H_155 regularization sweep — label smoothing + WD + high dropout 18M (overfit prevention)
