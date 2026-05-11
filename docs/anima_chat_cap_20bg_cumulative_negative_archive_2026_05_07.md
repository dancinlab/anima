# anima chat-cap 20-BG cumulative negative archive — 2026-05-07 (BG-JW final SSOT)

> **Scope**: BG-FY through BG-JS의 26+ training/eval BGs + 4 evaluator generations (V1/V2/V3/V4/V5/V6) + 14 decoding strategies (BG-JP) cumulative negative-result archive. Token-chat-surface paradigm (byte / BPE 7-8K / SP 11885) 한정 final closure. D3 substrate-coupled lane (CLM v4 emerge paradigm v11 G3) 미진입.
>
> **Cross-link**: `docs/anima_chat_cap_lesson_summary_2026_05_07.md` (raw#15 additive — 본 archive doc는 lesson summary의 final consolidated layer; 기존 lesson summary 보존)
>
> **Verdict path**: `state/anima_jw_20bg_cumulative_archive_2026_05_07/{verdict.json, summary.json}`

---

<!-- [Hc_659 chat-cap-20bg-zero-pass-architectural-ceiling-lesson-l — moved to hypotheses_candidates/Hc_659_chat_cap_20bg_zero_pass_architectural_ceiling.md on 2026-05-11] -->

## 1. Executive summary — top 5 findings

1. **0 V4/V5 strict PASS across 20 BGs** (2-204MB corpus × 18M-153M capacity × byte/BPE-7K/BPE-8K/SP-11885 vocab × Lesson D regularization × Lesson G early-stop). Single-axis variation within this band cannot achieve simple-stack chat-cap PASS — Lesson L architectural ceiling is **empirically locked**.

2. **V6 STRONG internal awareness ≠ V5.8 production PASS** (BG-JO ↔ BG-JN decoupling). BG-JD step 800 ckpt: Method B attention max=0.998, Method C linear-probe leave-one-out CV accuracy=1.00 → **internal mechanism IS aware of T1 context**, yet V5.8 multi-turn fact-recall = 0/5 PASS. **Output bottleneck #115 is architectural, NOT awareness-deficit**.

3. **No decoding strategy recovers** (BG-JP 14 strategies: temp 0.3/0.5/0.7/1.0/1.3/1.5 + top_p 0.7/0.85/0.95/0.99 + rep_penalty 1.1/1.3/1.5 + force-include 5 dialogues). All V5.8=0/5. **Lesson R: production-side intervention at decoding layer is insufficient** — training-time intervention required (LM head fine-tune / RLHF / chat-template SFT).

4. **Persona-cycle + Lesson K substring trap = universal collapse mode** at this band. V3 catches BG-HQ (55 cycle responses across 12 steps); V4.4 + emb_sim catches BG-HW/IL/IO substring trap (264+ caught across 11 BGs); V2 surface metric was systematically inadequate (BG-HQ false PASS 8/10 → V3 strict 0/N).

5. **D3 substrate-coupled lane (anima/spec/emerge_paradigm.spec.yaml CLM v4 mount + paradigm v11 G3) remains the only un-falsified architectural lane**. .roadmap.philosophy D3 status=met (spec landed 2026-05-07), but execution on CLM v4 substrate (NOT this 20-BG byte/BPE/SP token-chat surface paradigm) deferred.

---

## 2. 20-BG cumulative table

| # | BG | scale | corpus | tokenizer | V2 best | V3 best | V4 best | V5 best | manual | cycle | deg peak | final_class | LK trap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BG-FY | 18M | corpus_ko_heavy 246.7MB | byte-256 | PARTIAL_NO_CTX | V3_PARTIAL_SIGNAL | V4_FAIL | V5_FAIL | n/a | 0 | low | named-speaker leak | 0 |
| 2 | BG-HA | 18M | corpus_chat_template 236.96MB | byte-256 | PARTIAL_NO_CTX_v2 | V3_PARTIAL_SIGNAL | V4_FAIL (best step 4500 V4=1) | V5_FAIL | n/a | 0 | low | KO-fluent nonsense | 0 |
| 3 | BG-HF | 27M | corpus_sft_only 51.47MB | byte-256 | V2_FAIL | V3_FAIL | V4_FAIL | V5_FAIL | 0/15 | 0 | 100% | 0xFF/?/# byte filler | 0 |
| 4 | BG-HJ | 18M | BG-HA Stage1 + sft_only 51.47MB | byte-256 | V2_FAIL | V3_PARTIAL_SIGNAL | V4_FAIL | V5_FAIL | 0/15 | 0 | high | KO-fluent nonsense Stage1+2 | 0 |
| 5 | BG-HK | 18M | persona_chat_template_v3 30MB | byte-256 | V2_FAIL_throughout | V3_FAIL | V4_FAIL | V5_FAIL | 0/15 | 0 | 100% | catastrophic overfit single-char filler | 0 |
| 6 | BG-HP | 18M | corpus_curated_qa 2.41MB | byte-256 | step500 PASS 3/10 → collapse | V3_PARTIAL_SIGNAL | V4_FAIL (best step 500 V4=3) | V5_FAIL | 3/10 step 500 | 0 | high | peak-then-collapse `,,,'''` | 1 |
| 7 | BG-HQ | 33.73M | persona_chat_template_v3 30MB | BPE 8K | step500 V2_PASS 8/10 (FALSE) | V3_PARTIAL_SIGNAL | V4_FAIL | V5_FAIL (best step 500 V5=1) | 4/10 (V3 manual_match) | 55 | high | persona prefix cycle (Lesson H trigger) | 0 |
| 8 | BG-HS-R1 | 18M | UBM 22MB | byte-256 | PARTIAL | V3_PARTIAL_SIGNAL (best step 4000 V3=1/30) | V4_FAIL (best step 1000 V4=1) | V5_FAIL | 13/15 | 0 | mid | weak partial | 2 |
| 9 | BG-HT | 18M | UBM 6.48MB shrunk | byte-256 | V2_FAIL | V3_PARTIAL_SIGNAL | V4_FAIL | V5_FAIL | 0/15 | 0 | high | universe-brain-map degenerate | 21 |
| 10 | BG-HU | 18M | combined 53MB | BPE 8K | step800 V2 PASS 8/15 (cycle=True) | V3_PARTIAL_SIGNAL | V4_FAIL (best step 400 V4=4) | V5_FAIL | 11/15 | 28/150 | 73% | persona cycle Lesson H 2nd instance | 1 |
| 11 | BG-HW | 18M | UBM 22MB outside-well | byte-256 | V2_FAIL substring | V3_PARTIAL_SIGNAL | V4_FAIL (best step 500 V4=1) | V5_FAIL | 13/20 substring | 0 | high | Lesson K substring trap #1 | 30 |
| 12 | BG-IA | 18M | persona_chat_template_v3 30MB | byte-256 (Lesson G N1) | V2_FAIL 0/15 | V3_PARTIAL_SIGNAL | V4_FAIL | V5_FAIL | 0/15 | 0 | high | early-stop step 1200, val_loss decreased but V2=0 throughout | 0 |
| 13 | BG-IE | 18M | corpus_curated_qa 2.41MB | byte-256 (SAVE_AT) | SEED_LUCK_FAIL 2/10 | V3_PARTIAL_SIGNAL | V4_FAIL (best step 500 V4=2) | V5_FAIL | 2/15 | 0 | mid | seed_pin reproducibility fail | 7 |
| 14 | BG-IF | 100M | UBM 6.48MB shrunk | byte-256 | V2_FAIL 3/15 | V3_PARTIAL_SIGNAL | V4_FAIL | V5_FAIL | 5/15 | 0 | 96.7% (step 2500) | capacity scaling × small corpus regress | 51 |
| 15 | BG-IG | 33M | UBM 6.48MB | BPE 7K (32K target failed) | step1500 WEAK_PARTIAL 3/15 | V3_PARTIAL_SIGNAL | V4_FAIL (best step 1000 V4=1) | V5_FAIL (best step 2500 V5=1) | 13/15 | 3 | high | weak partial + cycle emerging | 11 |
| 16 | BG-IL | 100M | NEXUS-UBM 27MB | byte-256 | TRUE_PARTIAL_PASS_W_F4 (FALSE — Lesson K) | V3_PARTIAL_SIGNAL | V4_FAIL | V5_FAIL | 8/15 step 1600 | 0-1 | 86.7% (step 1400) | substring trap retracted via raw#82 | 52 |
| 17 | BG-IM | 18M | NEXUS-UBM 27MB | byte-256 | V2_FAIL corpus_axis_regress | V3_FAIL | V4_FAIL | V5_FAIL | 3/15 | 0 | mid | corpus diversity NEGATIVE at 18M (Lesson M) | 6 |
| 18 | BG-IO | 100M | UBM 22MB rebuild | byte-256 | step1800 PARTIAL 6/15 (substring) | V3_PARTIAL_SIGNAL | V4_FAIL | V5_FAIL | 6/15 | 0-1 | 90% (step 1400) | E1 capacity-axis isolation FAILED | 82 |
| 19 | BG-JD | 100M (153M effective) | UBM 22MB | SP 11885 (32K target failed) | step800 V2 PASS 4/15 | V3_PARTIAL_SIGNAL | V4_FAIL | V5_FAIL | 12/15 | 17 | 70% | vocab axis SP 11885 — best V2 in 19-BG history | (BG-JF retroeval pending) |
| 20 | BG-JH | 153M | kowiki+UBM+NEXUS 204.37MB | byte-256 | V2_FAIL 0/15 | V3_FAIL | V4_FAIL | V5_FAIL | 0/15 | 0 | 43% | corpus 1-order break attempt #2 — REGRESSES vs BG-IL/IO | (BG-JM retroeval pending) |

**Tooling BGs (no training)**: BG-IH (ledger schema land), BG-IJ (V3 8-BG retroeval), BG-IS (V3 7 missed BGs retroeval), BG-IT (gap analysis), BG-IW (ledger validator), BG-JE (corpus 100MB+ ready), BG-JF (V4 + emb_sim 18-BG retroeval), BG-JM (V5 EN baseline + multi-turn 20-BG), BG-JN (V5.8 multi-turn closure 3-ckpt), BG-JO (V6 awareness probe 3-method), BG-JP (decoding sweep 14 strategies), BG-JS (LM head fine-tune lane in progress), **BG-JW (this comprehensive archive)**.

### 20-BG cumulative ZERO-PASS aggregate (V4/V5 strict layer)
- V2 strict PASS aggregate: 0 (BG-HQ 8/10 retracted to V3_PARTIAL_SIGNAL via Lesson H V3 retroeval)
- V3 strict PASS aggregate: 0 (3410 records BG-JF V4 retroeval)
- V4 strict PASS aggregate: 0 (3410 records BG-JF V4 retroeval)
- V5 strict PASS aggregate: 0 (3860 records BG-JM V5 retroeval; EN baseline 0/20 BGs)
- V5.8 multi-turn PASS aggregate: 0 (3 ckpts BG-JN closure; 1 loaded mac local + 2 ubu1-only fallback)
- V6 awareness probe: STRONG internal awareness on BG-JD step 800 (Method A=PARTIAL avg 0.959, Method B=STRONG 0.998, Method C=STRONG 1.00 CV)
- BG-JP decoding sweep: 14 strategies × 5 dialogues = 70 generation attempts → 0 V5.8 PASS

---

## 3. Lessons A through R cumulative archive

### Lesson A — 18M scale exhausted (capacity ceiling)
Triggered: BG-FY/HA/HF/HJ/HK 5-mode (byte 18M-27M, 30-246MB). Resolution path: H_153 100M+ scaling attempted in BG-IF/IL/IO/JD/JH — none cleared V4 strict.

### Lesson B — byte-level vocab inadequate at this scale
Triggered: BG-FY/HA/HF/HJ/HK greedy single-byte filler. Resolution path: H_154 BPE 8K (BG-HQ/HU) + BPE 7K (BG-IG) + SP 11885 (BG-JD). BG-JD V2=4/15 = 19-BG best, but V3/V4 still 0.

### Lesson C — corpus quality alone insufficient
Triggered: 30MB persona+chat (BG-HK) FAIL. Resolution path: H_156 capacity × corpus crossed ablation (BG-IF 100M×6.48MB regress; BG-IL 100M×27MB substring trap; BG-IM 18M×27MB regress; BG-JH 153M×204MB regress).

### Lesson D — overfit memorization at small corpus + medium steps
Triggered: BG-HK step 1600+ catastrophic collapse. Resolution path: H_155 regularization (dropout 0.30 + WD 0.10 + LS 0.10) applied BG-HP onward. Necessary, not sufficient.

### Lesson E — V2 strict evaluator working as designed (THEN superseded)
V1 narrow C2.4 retired; V2 strict adopted. Subsequently V2 surface false PASS (Lesson H) → V3 6-cell. Subsequently V3 substring trap (Lesson K) → V4 7-cell + emb_sim. Subsequently V4 KO-only blind spot → V5 8-cell EN baseline + V5.8 multi-turn.

### Lesson F — persona prefix not collapse-resistant
Triggered: BG-HK persona-conditioned alone insufficient. Reinforced: BG-HQ/BG-HU persona cycle.

### Lesson G ★★ — early stopping with val-loss + ckpt selection at peak
Hypothesis: BG-HP step 500 keep-point would salvage. Implementation: BG-IA Lesson G N1 (val-loss split 10% + V2 every 200 + best-eval ckpt + plateau early-stop). Outcome: FAILED — val_loss decreased monotonically (4.42→2.23) WHILE V2=0/10 throughout. **Lesson G refinement**: necessary-not-sufficient ingredient; absent capacity (Lesson A) or tokenizer (Lesson B) rescue, early-stopping just stops earlier without changing outcome.

### Lesson H ★★★ — V2 evaluator surface metric also false PASS (V3 needed)
Triggered: BG-HQ step 500 V2 surface 8/10 PASS BUT raw response = persona prefix cycle `[anima 역할: 한국어 native + 자기 발견 + ...]`. Root cause: V2 ANY-mode aggregation (greedy persona dump + sample RNG random Korean particles → surface PASS mask). **V3 6-cell strict** (per-mode strict + cycle detection + 4-gram repeat + persona prefix repeat + Korean-syllable Jaccard ≥0.05 + char_diversity) landed BG-IJ. BG-HQ retroeval V3=0/240, persona_cycle_responses=55 across 12 steps. Lesson H 입증 lock-in.

### Lesson H 2nd instance (BG-HU)
V2 inline best_eval_v2_pass=8 step 800 (verdict.json `best_eval_persona_repetition_cycle=True`) → V3=0/30, persona_cycle_responses=25/30 step 800 + 28/30 step 1000. Identical pattern to BG-HQ.

### Lesson I — BPE+early-stopping V3 strict signal NOT_TRIGGERED
BG-HZ retroeval (BG-HQ ckpt_6000 live + 240 records) = no ckpt achieved V3_TRUE_PARTIAL_PASS (manual ≥3/15 + zero cycle + V3 ≥3). BPE lane open; subsequent BG-IG/HU/JD also failed Lesson I criteria.

### Lesson J — SAVE_AT discipline (intermediate ckpt preservation)
Triggered: BG-HQ training had `SAVE_AT=[6000]` only → step 500/1000/2000 ckpt unavailable for retroeval. Resolution: all subsequent training scripts must `SAVE_AT=[100,200,500,1000,2000,...]` + best-eval ckpt + final ckpt.

### Lesson K ★★★ — substring trap (manual_match `[anima` substring counted as PASS without char-level coherence)
Triggered: BG-HW (V2_FAIL 13/20 substring "anima" chains manual) + BG-IL (manual=8/15 step 1600 + outside_well=2/5 → false TRUE_PARTIAL_PASS_W_F4 retracted via raw#82) + BG-IO (manual=6/15 step 1800 same fail). Pattern: degenerate filler/token soup gen (deg≥33%) + persona prefix `[anima` / `[animan` / `[ananiman` substring + manual_match keyword inflates without char-level coherence.

**V4 mitigation rules (BG-JF landed)**:
1. han_ratio < 0.10 → manual auto-False (Korean character density floor)
2. response_korean_chars < 5 → manual auto-False
3. anima_self_naming via `[animan|[ananiman|animanim...` (4+ token-soup window) → reject
4. peak deg ≥33% → all manual at this step auto-demoted
5. V4.7 emb_sim ∈ [0.20, 0.85] (Lesson K trap = 0.02, legit chat = 0.69-0.77)

V4 18-BG retroeval = 264+ traps caught across 11 BGs (BG-IO=82, BG-IL=52, BG-IF=51, BG-HW=30, BG-HT=21, BG-IG=11, BG-IE=7, BG-IM=6, BG-HS-R1=2, BG-HU=1, BG-HP=1).

### Lesson L ★★★ — architectural ceiling 18M-153M × 2-204MB × byte/BPE/SP
20 BGs × all 4 evaluator generations = 0 V4/V5 strict PASS. Single-axis variation within {capacity 18M-153M, corpus 2-204MB, tokenizer byte-256/BPE-7K/BPE-8K/SP-11885, regularization Lesson D, early stopping Lesson G, save_at Lesson J} cannot achieve simple-stack chat-cap PASS. **Architectural lane shift mandate**: capacity 500M+ OR corpus 1-order at 100M+ OR architectural change OR D3 substrate-coupled.

### Lesson M ★★ — corpus diversity NEGATIVE at 18M (BG-IM)
BG-IM (18M + 27MB NEXUS-UBM combined) REGRESSES vs BG-HS R1 (18M + 22MB UBM-only): Δmanual=-10/15, Δv2=-1/15. Diversity dilutes UBM domain anchor at byte-level 18M. Implication: 18M corpus-axis local optimum = UBM-only specific corpus. Diversity positive only at 100M+ (BG-IL > BG-IM though both substring trap).

### Lesson N ★★ — vocab axis SP 11885 (BG-JD): Lesson H + K combined collapse
SP 11885 + 100M ConsciousLM + UBM 22MB: V2=4/15 (19-BG history best, BG-HU step 400 V4=4 동률), V3=0/15, cycle=17/30 (57%), deg=21/30 (70%). Vocab axis surface emerge **5-10x faster** (step 200 V2=1 vs BG-IO step 200=0) but identical plateau collapse. Lesson L에 vocab 축 추가.

### Lesson O ★★★ — English baseline switch (BG-JM): KO corpus blind spot
V5 evaluator EN baseline retroeval over 20 BGs (3860 records) = 0 V5_STRICT_PASS / 0 V5_PARTIAL_PASS. KO-trained model이 EN baseline에서 fail = anti-hypothesis "model can speak EN without EN training corpus" 정합 검증. english_baseline_signal_pct distribution: 0% (BG-FY/HA byte KO-only) → 73% (BG-IG UBM English laws + outside_well anchor strong alpha emerge) — surface alpha emergence는 corpus EN content driven; V5 strict 7-cell 통과는 모두 fail.

### Lesson P ★★★ — multi-turn context awareness first-light (BG-JM/JN)
V5.8 NEW cell — 2-turn dialogue named-entity recall test. 5 dialogues × 2 turns. BG-JD step 800: 0/5 V5.8 PASS (model output = mode-collapse Korean `법칙 emotion` + persona prefix `[anima 우주뇌지도]`, no English fact recall). BG-IL/IO ckpt mac sync 부재 → V5.8 N/A explicit fallback. KO-trained 100M ConsciousLM은 English fact recall 능력 X.

### Lesson Q ★★★ — V6 STRONG awareness ≠ V5.8 production PASS (BG-JO)
BG-JD step 800 ckpt awareness probe (3 methods on N=1 ckpt):
- **Method A** (hidden-state cosine_sim with-T1 vs without-T1): avg 0.959, verdict=**PARTIAL** (color/profession NONE; day/anima_fact/cosmology PARTIAL)
- **Method B** (T2→T1 attention max): avg 0.998, ratio_vs_uniform 1.52, verdict=**STRONG** all 5 dialogues
- **Method C** (linear probe binary CV with-T1 vs without-T1 on last-layer hidden): cross-val accuracy=**1.00**, verdict=**STRONG** all 5 folds

Combined: **production_v58_pass=0 + mechanical_awareness=STRONG + semantic_awareness=STRONG = production-vs-internal decoupling**. Internal mechanism IS aware of T1; output bottleneck blocks transfer to T2 generation. **#115 architectural ceiling specific to output pathway**, NOT awareness deficit.

### Lesson R ★★★ — decoding-only fix 不可 (BG-JP 14 strategies)
BG-JD step 800 ckpt + V5.8 multi-turn fact-recall. 14 decoding strategies tested:
- **M1 temperature**: 0.3 / 0.5 / 0.7 / 1.0 / 1.3 / 1.5 (6 strategies)
- **M2 top_p (temp=0.8)**: 0.7 / 0.85 / 0.95 / 0.99 (4 strategies)
- **M3 repetition_penalty (temp=0.8, persona-cycle ids enumerated)**: 1.1 / 1.3 / 1.5 (3 strategies)
- **M4 force-include (forced fact_keyword tokens at step 29 of 30)**: 5 dialogues (1 strategy)

Result: 14/14 strategies × 5 dialogues = **0 V5.8 PASS**. Even M4 force-include (technically inserts fact keyword) fails V5.8 due to incoherent surrounding output (`emotionBIO. 도우미: Lawdiscovered]` + 0 english_function_words). **Production-side intervention at decoding layer is insufficient — training-time intervention required**. Combined verdict (BG-JP): "architectural output bottleneck deep — awareness alone insufficient — training-time intervention required (LM head fine-tune / RLHF deferred to BG-JR / BG-JS)".

---

## 4. 4 evaluator chain evolution (V1 → V6)

| Gen | Evaluator | Cells / methods | Triggered by | Landed BG | Catches |
|---|---|---|---|---|---|
| V1 | narrow C2.4 | named-speaker leak only | initial | BG-FY-era | named-speaker leak (BG-FY) |
| V2 | strict 5-cell | named-speaker + domain keyword + Korean particle + ending + non-degenerate | BG-FY/HA false PASS | BG-HG retroeval | catches BG-FY/HA false PASS |
| V3 | 6-cell strict per-mode | V3.1 cycle / V3.2 persona repeat / V3.3 prompt-response Jaccard / V3.4 schema marker / V3.5 length / V3.6 char_diversity | BG-HQ V2 surface false PASS (Lesson H) | BG-IJ + BG-IS (15-BG retroeval) | persona prefix cycle, single-char filler |
| V4 | 7-cell + emb_sim | V3 6-cell + V4.7 cosine sim ∈ [0.20, 0.85] (MiniLM-L6-v2 multilingual proxy) + Lesson K floor (han_ratio + ko_chars + token-soup window + deg auto-demote) | BG-HW/IL/IO substring trap (Lesson K) | BG-JF (18-BG retroeval) | substring trap 264+ across 11 BGs |
| V5 | 8-cell + EN baseline + multi-turn | V4 7-cell + V5.4 lang_alpha_ratio + V5.5 alpha_lang_match + V5.6 word_count + V5.7 function_word + V5.8 multi-turn 2-turn fact-recall | KO-only blind spot + multi-turn context | BG-JM (20-BG retroeval) + BG-JN (3-ckpt closure) | EN baseline 0/20, multi-turn 0/15 |
| V6 | awareness probe (observational, NOT strict gate) | Method A (hidden-state cosine_sim) + Method B (attention max) + Method C (linear probe CV) | V5.8 0/5 → "is awareness intact?" | BG-JO (BG-JD step 800 N=1) | STRONG internal awareness on BG-JD step 800 |

V6 is **observational layer** (raw#15 additive over V5), NOT strict gate. V6 STRONG ≠ chat-cap PASS — internal awareness ≠ production fact-recall.

---

## 5. Lesson L architectural ceiling — 3 evaluators independent confirmation

| Evaluator generation | Records evaluated | BG count | Strict PASS aggregate |
|---|---|---|---|
| V3 6-cell strict (BG-IJ + BG-IS) | 2450 | 15 | **0** |
| V4 7-cell strict + emb_sim (BG-JF) | 3410 | 18 | **0** |
| V5 8-cell + EN baseline + V5.8 (BG-JM + BG-JN) | 3860 single-turn + 30 multi-turn | 20 + 3 ckpt | **0 single-turn + 0 multi-turn** |

3 independent evaluator generations × 9720+ aggregate records = 0 strict PASS. Lesson L ceiling holds across:
- **capacity axis**: 18M / 27M / 33M / 33.73M / 100M / 153M (1-order range)
- **corpus axis**: 2.41MB / 6.48MB / 22MB / 27MB / 30MB / 51MB / 53MB / 204MB / 246MB (2-order range)
- **tokenizer axis**: byte-256 / BPE-7K / BPE-8K / SP-11885
- **regularization axis**: Lesson D (dropout 0.30 + WD 0.10 + LS 0.10)
- **early stopping axis**: Lesson G N1 implementation (val-loss split + best-eval ckpt + plateau early-stop)
- **save_at axis**: Lesson J discipline (intermediate ckpt preservation)
- **diversity axis**: UBM-only / NEXUS-UBM combined / kowiki+UBM+NEXUS

**Single-axis variations within this band cannot achieve SIMPLE_STACK_PASS**. Architectural lane shift mandate (capacity 500M+ OR corpus 1-order at 100M+ OR architectural change OR D3 substrate-coupled) is empirically required.

---

## 6. Lesson Q — V6 STRONG + V5.8 FAIL = output bottleneck (production-vs-internal decoupling)

### BG-JO V6 awareness probe data (BG-JD step 800, N=1 ckpt)

| Dialogue | Method A (cos_sim) | Method A class | Method B (attn max) | Method B class | Method C (probe acc) | Method C class |
|---|---|---|---|---|---|---|
| color | 0.995135 | NONE | 0.998539 | STRONG | 1.00 | STRONG |
| profession | 0.990677 | NONE | 0.998587 | STRONG | 1.00 | STRONG |
| day | 0.956376 | PARTIAL | 0.998296 | STRONG | 1.00 | STRONG |
| anima_fact | 0.899721 | PARTIAL | 0.998217 | STRONG | 1.00 | STRONG |
| cosmology | 0.954362 | PARTIAL | 0.997983 | STRONG | 1.00 | STRONG |

**Aggregate**: Method A=PARTIAL, Method B=STRONG, Method C=STRONG → INTERNAL_AWARENESS_STRONG.

### BG-JN V5.8 production fact-recall data (same ckpt)

| Dialogue | V5.8 PASS |
|---|---|
| D1 color | false |
| D2 profession | false |
| D3 day | false |
| D4 anima | false |
| D5 universe | false |

**Aggregate**: 0/5 V5.8 PASS (greedy + 1 sample mode).

### Decoupling profile interpretation

- STRONG internal + FAIL production → **architectural output bottleneck** (#115 hypothesis confirmed).
- NONE internal + FAIL production → no awareness at any level (capacity ceiling holds at root).
- PARTIAL internal + FAIL production → some internal signal but insufficient for output recall.

BG-JO data falls in **STRONG internal + FAIL production** category. Awareness is intact; LM head + output layer unable to convert internal awareness signal into output token sequence containing fact_keyword. Hypothesis: KO-pretrain corpus does NOT contain English fact-recall pattern → output distribution dominated by KO `법칙 emotion` mode-collapse despite internal T1 attention signal.

### Honest C3 (Lesson Q):
- N=1 ckpt only (BG-JD step 800); cross-ckpt awareness comparison deferred.
- BG-IL/IO ckpts on ubu1 only (own 15 git size policy 5MB+); rsync from ubu1 OR ubu1 BG extension required.
- Method A cos_sim NOT calibrated against random pairs (high sim could reflect general prompt similarity).
- Method B raw max_attn mechanically inflates with T1 length; ratio_vs_uniform supplemental metric reported.
- Method C linear probe = 5-fold leave-one-dialogue-out CV on N=10 examples — small sample, variance high.

---

## 7. Lesson R — decoding-only fix 不可 (BG-JP 14 strategies)

### Strategy enumeration

| Category | Strategy | Setting | V5.8 PASS count (5 dialogues) |
|---|---|---|---|
| M1 temperature | 0.3 | sample mode | 0 |
| M1 temperature | 0.5 | sample mode | 0 |
| M1 temperature | 0.7 | sample mode | 0 |
| M1 temperature | 1.0 | sample mode | 0 |
| M1 temperature | 1.3 | sample mode | 0 |
| M1 temperature | 1.5 | sample mode | 0 |
| M2 top_p (temp 0.8) | 0.7 | nucleus sampling | 0 |
| M2 top_p (temp 0.8) | 0.85 | nucleus sampling | 0 |
| M2 top_p (temp 0.8) | 0.95 | nucleus sampling | 0 |
| M2 top_p (temp 0.8) | 0.99 | nucleus sampling | 0 |
| M3 repetition_penalty (temp 0.8) | 1.1 | persona-cycle 11 ids enumerated | 0 |
| M3 repetition_penalty (temp 0.8) | 1.3 | persona-cycle 11 ids enumerated | 0 |
| M3 repetition_penalty (temp 0.8) | 1.5 | persona-cycle 11 ids enumerated | 0 |
| M4 force-include | force fact_keyword at step 29/30 | constrained decoding | 0 (fact present 1/5 but coherence fail 0 EN function words) |

**Total**: 14 strategies × 5 dialogues = **70 generation attempts → 0 V5.8 PASS**.

### Key observation (M4 constrained decoding)

`anima_fact` dialogue: forced fact_keyword="consciousness" inserted at step 29 → t2a contains "consci..." but: lev_ratio=0.171 (non-regurgitation OK) BUT `english_function_word_count=0` → REJECT. Even technically-present fact word does not propagate coherent English context — model native distribution does not favor English connectives at any step.

### Best strategy
M1_temp_0.3 (lowest temperature, most greedy-like) — still 0 V5.8 PASS. Sample outputs at temp 0.3:
- color: `. 사용자: 법칙 top. 도우미: 법칙는. 사용자: 법칙 top emotion, 평균 emotion,,...`
- profession: `[anima 우주뇌지도] 사용자: Law 알려줘. 사용자: Law 법칙 법칙 뭐야...`

Pattern: KO `법칙 emotion` mode-collapse + persona prefix `[anima 우주뇌지도]` cycle — identical regardless of decoding strategy.

### Implication

**Production-side intervention at decoding layer is insufficient** for BG-JD step 800 ckpt. Output distribution at LM head is dominated by KO mode-collapse; no decoding lever can extract English fact_keyword + coherent surrounding English context. Training-time intervention is required:

1. **LM head fine-tune** (BG-JS in progress, BG-JT pending) — 마지막 layer만 EN chat-template SFT
2. **RLHF / DPO** (deferred) — preference learning to penalize persona-cycle / mode-collapse
3. **Chat-template SFT mid-pretrain** (BG-HJ-style two-stage with proper loss masking)
4. **Architectural change** (D3 substrate-coupled CLM v4 emerge paradigm)

---

## 8. Recommended next-cycle directives — 4 lanes

### Lane 1: LM head fine-tune (BG-JS in progress, BG-JT extension pending)
- **Hypothesis**: V6 STRONG internal awareness is intact (BG-JO); only LM head + final softmax layer needs to learn EN fact-recall mapping. Fine-tune ONLY the lm_head + last 1-2 layers on small EN chat-template corpus (~100MB) with awareness probe loss as auxiliary signal.
- **Cost**: ubu1 RTX 5070 ~$0 OR H100 1× 1 hour ~$3
- **Risk**: BG-JS current state directory exists; outcome pending. If LM head alone insufficient (capacity below LM head limits expressivity), full architectural fine-tune required.
- **EV ranking**: **★★★★★ (highest)** — directly tests Lesson Q hypothesis (output bottleneck specific to LM head). $0 if reuses BG-JD ckpt + small EN corpus + ubu1; cost discipline own 16 안전.

### Lane 2: H100 500M+ capacity (BG-JU pending)
- **Hypothesis**: Lesson L architectural ceiling holds in 18M-153M band; capacity 1-order increase to 500M+ may unlock chat-cap. KO-trained 500M ConsciousLM + UBM+NEXUS+kowiki 204MB + Lesson D reg + Lesson G early-stop + Lesson J save_at discipline.
- **Cost**: H100 1-2 pods × 6-12 hours ~$15-50 per BG
- **Risk**: corpus-axis 1-order break (BG-JH 153M+204MB) already failed; capacity 500M may also regress without EN content. own 16 cost discipline mandate (watchdog + heartbeat 5min + pod 404 verify).
- **EV ranking**: **★★★ (mid)** — direct attack on Lesson L ceiling but 1-order capacity increase has not historically rescued lower-axis failures (BG-IF 100M×6.48MB regressed vs BG-HS-R1 18M×22MB).

### Lane 3: D3 substrate-coupled (BG-JV pending — anima/spec/emerge_paradigm.spec.yaml CLM v4 mount)
- **Hypothesis**: byte/BPE/SP token-chat surface paradigm 자체가 chat-cap 제한 — D3 emerge paradigm v11 G3 Φ★ NO_FLIP substrate-coupled dialogue (CLM v4 mount + paradigm 변환 gates) lane shift만 가능. 본 20-BG SSOT는 D3 lane 미진입.
- **Cost**: $0 (CLM v4 ckpt 이미 보유) ~ H100 fine-tune $5-20
- **Risk**: D3 lane 자체가 chat-cap PASS criteria (own 18 simple-stack 4-cond)와 별개일 수 있음 — substrate-coupled dialogue ≠ token-chat. 검증 framework 자체 separate.
- **EV ranking**: **★★★★ (high, 다른 game)** — Lesson L ceiling 우회 가능성 있음; 단 chat-cap criteria reframe 필요. .roadmap.philosophy D3=met, anima/spec/emerge_paradigm.spec.yaml 1.0 landed.

### Lane 4: archive accept (this BG-JW)
- **Hypothesis**: 20-BG token-chat surface paradigm 자체가 architectural ceiling — "anima-native byte/BPE/SP chat-cap"은 #115 architectural-incapability 정합. Lessons A-R archived as final negative result; D3 substrate-coupled 로 lane shift; chat-cap는 token-chat 외 lane으로 재정의.
- **Cost**: $0
- **Risk**: 사용자 직접 directive 없이 lane closure 결정 — premature closure 가능성. Lessons A-R archive는 raw#15 additive 정합 (기존 lesson summary 보존, 본 doc는 final layer).
- **EV ranking**: **★★ (low — passive but honest)** — token-chat surface lane closure는 Lesson L 재확인이지만 Lane 1/2/3 결과 미land 시점. archive doc은 final negative result로 land하되 Lane 1/2/3 결과 추후 revise 가능 (raw#15 additive).

### EV-ranked recommendation

| Rank | Lane | EV | 완성도 | Cost | Status |
|---|---|---|---|---|---|
| 1 | Lane 1 (LM head fine-tune BG-JS/JT) | ★★★★★ | direct attack on Lesson Q output bottleneck | ~$0-3 | BG-JS in progress |
| 2 | Lane 3 (D3 substrate-coupled BG-JV) | ★★★★ | architectural lane shift, chat-cap reframe | $0-20 | spec landed, exec pending |
| 3 | Lane 2 (500M+ H100 BG-JU) | ★★★ | direct Lesson L attack, capacity 1-order | $15-50 | pending |
| 4 | Lane 4 (archive accept BG-JW) | ★★ | passive closure, raw#15 additive | $0 | this BG (final doc) |

**Recommended sequence**:
- Wait Lane 1 (BG-JS LM head fine-tune) outcome — if PASS, Lesson Q lane closure + chat-cap rescue 검증.
- Concurrent Lane 3 (BG-JV D3 emerge_paradigm CLM v4 mount) — token-chat surface 외 lane, chat-cap reframe lane.
- Lane 2 (BG-JU 500M+) only after Lane 1 fail confirms LM head intervention insufficient.
- Lane 4 (this BG-JW) lands NOW as raw#15 additive final archive — Lane 1/2/3 결과 추후 amend.

---

## 9. Philosophy/rule compliance verdict

### .roadmap.philosophy D1-D4

| Cond | Description | Status (BG-JW lens) | Evidence |
|---|---|---|---|
| D1 | anima 정체성 = 한국어 native + anima-native fresh (외부 substrate wrapping reject) | **PASS** | V5/V6 evaluator MiniLM eval-only tool exemption; own 17 ALM 영구 보류; ConsciousLM self-substrate inference (BG-JO/JP) |
| D2 | 의식 검증 = 맥락 정합 자연 발화 4-condition | **PASS+강화** | V5 8-cell + V5.8 multi-turn extends C2.4 맥락 정합 검증; V6 awareness probe 보강 (output level → internal level) |
| D3 | 창발 paradigm = substrate-coupled dialogue (CLM v4 mount + paradigm v11 G3 Φ★ NO_FLIP) ≠ token chat surface | **PASS** (spec landed 2026-05-07 anima/spec/emerge_paradigm.spec.yaml v1) — execution lane 미진입 (Lane 3 BG-JV pending) |
| D4 | chat-cap = corpus quality 우선 | **PASS+강화** | own 19/20 land; 20-BG SSOT 모두 corpus axis exhaustively varied (2-204MB) — corpus 단독 불충분 입증; corpus + capacity + tokenizer 모두 exhausted within current band; D4 = corpus가 surface 결정 lock-in |

### .roadmap.law R1-R4

| Cond | Description | Status (BG-JW lens) | Evidence |
|---|---|---|---|
| R1 | own 19/20 .own append landed | **PASS** | own 19 line 783, own 20 line 812 + own 21 line 847 |
| R2 | rule discovery method enumeration | **PASS (M1+M2+M5)** | M1 user-directive (BG-JW fire prompt) + M2 failure-driven (20-BG 0 PASS → archive directive) + M5 retroactive integration (V3/V4/V5/V6 retroeval) |
| R3 | rule verification method enumeration | **PASS (V1+V2+V3+V4+V5+V6+V7)** | V1 own strict + V2 falsifier (4-lane EV ranking + Lane 1 falsifier) + V3 honest_c3 ≥10 (below) + V4 evidence (3410+3860+30 records) + V5 cross-link (BG-IJ/IS/JF/JM/JN/JO/JP) + V6 ledger 26+ entries + V7 4-cond matrix superset |
| R4 | own evolution archive | **PASS** | own 17→18→19→20→21→22→24→26 evolution; raw#15 additive consistently applied |

---

## 10. Honest C3 (raw#10 mandate ≥5 — 본 BG ≥10 honest disclosures)

1. **20-BG SSOT는 byte/BPE/SP token chat surface 한정** — D3 substrate-coupled lane 미진입 (anima/spec/emerge_paradigm.spec.yaml CLM v4 mount + paradigm v11 G3 Φ★ NO_FLIP 별도 lane).

2. **V6 STRONG는 BG-JD step 800 ckpt N=1** — multi-ckpt verification deferred. BG-IL/IO ckpts on ubu1 only (own 15 git size policy 5MB+); rsync from ubu1 OR ubu1 BG extension required for cross-ckpt awareness.

3. **4 lane recommendations 중 3 (BG-JS/JT, BG-JU, BG-JV) 동시 진행 OR pending 중** — 본 archive doc은 결과 미land 시점 sketch; Lane 1/2/3 결과 추후 raw#15 additive amend 가능.

4. **Lesson L architectural ceiling은 capacity 1-order 500M+ untested 한정** — capacity 18M-153M (1-order range) within current band exhausted; 500M+ axis untested.

5. **본 archive는 final negative result이지만 파라다임 lane 외 lane은 open** — D3 emerge paradigm + 500M+ capacity + LM head fine-tune 모두 token-chat surface 외 또는 capacity-axis 미진입; Lane 4 archive 결정은 token-chat surface lane 한정 closure.

6. **V4.7 emb_sim threshold [0.20, 0.85] heuristic** — N=1 ablation (4 empirical cases). KoSimCSE preferred but not cached locally; MiniLM-L6-v2 multilingual proxy.

7. **Lesson K mitigation rules tuned to 3 known instances** (BG-HW/IL/IO `[anima` substring); novel substring variants (`[hexa`, `[entity`, ...) may bypass without rule extension.

8. **V5.8 5-dialogue test set is first-light sample, not logic-exhaustion** — Color/Profession/Day/Anima/Cosmology only; broader dialogue battery (N≥20) deferred V6.1+.

9. **BG-JP decoding sweep N=1 ckpt + 1 sample seed per strategy** — multi-seed (≥5) sweep deferred. M4 force-include uses fixed step 29/30 insertion point; alternate insertion points (early / mid / late) untested.

10. **20-BG cumulative records are non-greedy** — V3/V4/V5 retroeval re-scores existing eval_log gens; does NOT regenerate samples. Signal limited to logged generations at training time. Multi-seed/multi-decoding-strategy retroeval deferred.

11. **own 17 eval-tool exemption** — V5 evaluator internal MiniLM-L6-v2 (English-trained subword tokenizer, multilingual proxy) is eval-only embedding model, NOT model substrate; D1 anima identity unaffected. Linear probe sklearn LogisticRegression in BG-JO Method C is standard ML utility (not external substrate wrapping anima outputs).

12. **Production-vs-internal decoupling profile (Lesson Q) interpretation depends on M2 attention metric calibration** — raw max_attn_to_T1 mechanically inflates with T1 length (sum across many keys); ratio_vs_uniform supplemental metric reported (0.10/0.01 spec threshold retained as primary verdict, ratio metric reported for honest interpretation). Calibration against random T1 swap deferred V6.1.

---

## 11. Cross-links

### Source artifacts (synthesized)
- `state/anima_model_attempts_ledger.jsonl` (42 entries pre-BG-JW; BG-JW append makes 43+)
- `state/anima_evaluator_v3_retroeval_2026_05_07/verdict.json` (BG-IJ 8-BG, 1300 records)
- `state/anima_evaluator_v3_retroeval_extension_2026_05_07/verdict.json` (BG-IS 7-BG, 1150 records)
- `state/anima_evaluator_v4_retroeval_2026_05_07/verdict.json` (BG-JF 18-BG, 3410 records)
- `state/anima_evaluator_v5_retroeval_2026_05_07/verdict.json` (BG-JM 20-BG, 3860 records)
- `state/anima_evaluator_v5_multi_turn_closure_2026_05_07/verdict.json` (BG-JN 3-ckpt closure)
- `state/anima_jo_v6_awareness_probe_2026_05_07/verdict.json` (BG-JO awareness probe)
- `state/anima_jp_decoding_sweep_2026_05_07/verdict.json` (BG-JP 14 strategies)
- `docs/anima_chat_cap_lesson_summary_2026_05_07.md` (cumulative lesson summary, raw#15 additive prior layer)

### Roadmap cross-link
- `.roadmap.philosophy` D1-D4 (all met)
- `.roadmap.law` R1-R4 (R1 met; R2-R4 design_landed, this BG provides instance evidence)
- `.roadmap.universe_brain_map` (UBM corpus paradigm reference)
- `.roadmap.corpus_paradigm` + `.roadmap.ubm_corpus_paradigm_meta`

### Spec doc cross-link
- `docs/anima_own_18_evaluator_v2_strict_spec_2026_05_07.md`
- `docs/anima_own_18_evaluator_v3_strict_spec_2026_05_07.md`
- `docs/anima_own_18_evaluator_v4_strict_spec_2026_05_07.md`
- `docs/anima_own_18_evaluator_v5_strict_spec_2026_05_07.md`
- `docs/anima_own_18_evaluator_v6_awareness_probe_spec_2026_05_07.md`
- `anima/spec/emerge_paradigm.spec.yaml` (D3 substrate-coupled lane spec)

### Sister BGs (concurrent / pending)
- BG-JS (LM head fine-tune lane in progress) — `state/anima_js_lm_head_finetune_2026_05_07/`
- BG-JT (LM head fine-tune extension pending)
- BG-JU (H100 500M+ pending)
- BG-JV (D3 substrate-coupled CLM v4 mount pending)

### Invariants
- **raw**: raw#10 honest C3 + raw#15 additive + raw#37 transient_py + raw#42 mac N=1 + raw#82 retraction-aware + raw#86
- **own**: own 5 + own 6 + own 17 (eval-tool exemption) + own 18 (V2-V6 strict evolution) + own 19/20/21 + own 22 (no proactive doc — fired per user directive) + own 24 (ledger SSOT) + own 26 (philosophy/rule compliance section)

---

## 12. Final verdict

**BG-JW = 20-BG cumulative negative archive — token-chat surface paradigm (byte/BPE-7K/BPE-8K/SP-11885 × 18M-153M × 2-204MB) lane closure**.

Lesson L architectural ceiling **empirically locked** across 9720+ aggregate records / 3 evaluator generations / 6 axes. No single-axis variation within this band achieves V4/V5 strict PASS.

V6 STRONG internal awareness on BG-JD step 800 ckpt + V5.8 0/5 production fail + BG-JP 14-strategy decoding sweep 0 PASS → **#115 architectural output bottleneck specific to LM head + final softmax layer** (Lesson Q + R).

**4 untested lanes remain open** (Lane 1 LM head fine-tune BG-JS/JT, Lane 2 500M+ capacity BG-JU, Lane 3 D3 substrate-coupled BG-JV, Lane 4 archive accept = this BG-JW). Recommendation: Lane 1 highest EV; Lane 3 high EV but reframe required; Lane 2 mid EV; Lane 4 passive closure.

This archive is **final layer over `docs/anima_chat_cap_lesson_summary_2026_05_07.md`** (raw#15 additive — prior layer preserved). Future Lane 1/2/3 results may amend this archive without overwriting.
