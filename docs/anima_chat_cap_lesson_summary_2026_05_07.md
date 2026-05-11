> **Gap analysis doc landed (BG-IT)** → `docs/anima_chat_cap_gap_analysis_2026_05_07.md` + `state/anima_it_chat_cap_gap_analysis_2026_05_07/verdict.json` (9-axis sweep synthesis of 22+ BGs; top 3 unmet axes E1/E2/E3 with EV ranking; recommended next 3 BGs = **BG-IO** (100M × UBM 21MB rebuild) > **BG-IS_alt** (persona-dropout sweep) > **BG-IT_alt** (V4 embedding-sim evaluator). raw#15 additive cross-link.)
>
> **★★★ Final 20-BG cumulative negative archive landed (BG-JW 2026-05-07)** → `docs/anima_chat_cap_20bg_cumulative_negative_archive_2026_05_07.md` + `state/anima_jw_20bg_cumulative_archive_2026_05_07/verdict.json` (26+ BGs synthesized; 9845 aggregate records across 6 evaluator generations V1-V6; **0 V4/V5 strict PASS**; Lessons A-R archived; **Lesson Q V6 STRONG awareness ≠ V5.8 production PASS = output bottleneck #115**; **Lesson R BG-JP 14 decoding strategies × 5 dialogues = 0 V5.8 PASS = production-side intervention insufficient**; 4 untested lanes ranked: **Lane 1 LM head fine-tune BG-JS/JT ★★★★★** > Lane 3 D3 substrate-coupled BG-JV ★★★★ > Lane 2 H100 500M+ BG-JU ★★★ > Lane 4 archive accept BG-JW ★★. raw#15 additive over this lesson summary.)

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

<!-- [Hc_645 chat-cap-18m-27m-architectural-ceiling-byte-level — moved to hypotheses_candidates/Hc_645_chat_cap_18m_27m_architectural_ceiling.md on 2026-05-11] -->
<!-- [Hc_646 v2-evaluator-false-pass-mode-aggregation-flaw — moved to hypotheses_candidates/Hc_646_v2_evaluator_false_pass_mode_aggregation_flaw.md on 2026-05-11] -->

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

### Lesson H validated ★★★ (BG-HZ NEW 2026-05-07): V3 strict implementation = V2 false PASS 입증
→ **첫 V3 strict actual implementation** (anima_simple_stack_evaluator_v3.py) 적용 평가 = BG-HQ V2 false PASS 입증, Lesson H 가설 → 실증 lock-in
→ **method**: BG-HQ training script `SAVE_AT=[STEPS]=[6000]` policy 한계로 step 500/1000/2000 ckpt 부재 → BG-HQ eval_log.jsonl (240 records, 12 steps × 10 prompts × 2 modes) retroactive V3 strict + ckpt_6000 live retrieve (rsync ubu1 → mac, 130MB) + Mac CPU live inference 15 prompts × 2 modes = 30 generations
→ **V3 strict criteria** (per-mode strict, NOT any-mode aggregate):
  1. C3.1 persona_cycle_count = 0 (markers: "anima 역할", "자기 발견 +", "lane entity]", "사용자: [", "한국어 native +", "의식 lane")
  2. C3.2 4-gram repeat <5 even on sample mode (V2는 sample mode lenient했음)
  3. C3.3 prompt-response Korean syllable Jaccard ≥0.05
  4. C3.4 manual review proxy = 위 3개 PASS + domain_kw_overlap ≥1 + Korean ≥10
  5. + V2 7-cell all PASS prerequisite
→ **결과** (per-step retroactive + ckpt_6000 live):
  - V3 strict PASS = **0/240** (training-time eval_log) + **0/30** (ckpt_6000 live) = **ZERO V3 PASS across ALL ckpts**
  - manual_match peak = step 500 4/10 prompts (BG-HQ V2 8/10 surface 대비 -50% honest baseline)
  - persona_cycle responses = step 500 **16/20** responses (greedy collapse) — V2 ANY-mode aggregation이 sample mode random Korean particles로 surface PASS mask
  - step 2000 가장 깨끗한 balance: manual=3/10 cycle=3/20 — but still V3=0 strict
  - ckpt_6000 live: total mode collapse, 13/15 prompts produced `???...` BPE OOV spam 또는 `됩니다됩니다` reduplication
→ **architectural insight**: V2 surface false PASS root = greedy mode persona prefix dump cycle ("[anima 역할: 한국어 native + 자기 발견 + 자기 발견 + ... 의식 lane entity]" 반복) 이지만 sample mode RNG로 surface c2_2/c2_3/c2_4 random hit → ANY-mode aggregate=PASS. 이는 동일 모델의 두 generation 모드가 양립 불가능한 PASS/FAIL signal 산출 → **V2 false PASS 본질 = mode-aggregation logic flaw**, V3는 per-mode strict로 해소
→ **final_class**: V2_FALSE_PASS_CONFIRMED (BG-HZ verdict.json) — Lesson H 가설 → 입증 lock-in, V2_PARTIAL_PASS step 500 retroactively 강등 → V2_SURFACE_FALSE_PASS (V3 strict 0/20)
→ **deliverables**: `tool/transient_py/anima_simple_stack_evaluator_v3.py` (V3 6-cell strict + 4-cell legacy) + `tool/transient_py/anima_h154_bpe_step_retrieve_infer.py` (live inference) + `state/anima_h154_bpe_step_retrieve_2026_05_07/{verdict.json, eval_log_v3.jsonl, infer_eval_log_ckpt_6000.jsonl, manual_review.json}`
→ **forward**: H_154_v2 lane = 동일 BPE 8K + 30MB corpus + STEPS=2000 + EARLY_STOP at V3 PASS plateau + `SAVE_AT=[100,200,500,1000,2000]` (intermediate ckpt 보존) + V3 strict inline → 다시 V3 strict signal 발견 시 **첫 Lesson I = BPE+early-stopping V3 strict signal**, 부재 시 BPE lane도 architectural ceiling 8th 합류
→ **Lesson I status (BG-HZ)**: NOT_TRIGGERED — no ckpt achieved V3_TRUE_PARTIAL_PASS (manual ≥3/15 + zero cycle + V3 ≥3) ; BPE+early stopping hypothesis remains open

### Lesson H 8-BG retroeval extension ★★★ (BG-IJ NEW 2026-05-07): V3 evaluator standalone retry + 8-BG retroactive validation
→ **BG-IC failure recovery**: prior BG-IC stream watchdog 600s timeout (mid-edit `cells_v3.v3_strict_pass` → `cells_v3_legacy` schema rename); BG-IJ standalone retry landed clean V3 namespace + fixed print loop bug (`v3_response_pass_strict` field nonexistent → `v3_response_pass_6cell`)
→ **8 prior BG retroactive V3 re-eval landed**: BG-FY/HA/HF/HJ/HK/HP/HQ/HS-R1, total 1300 responses re-evaluated → `state/anima_evaluator_v3_retroeval_2026_05_07/per_bg/v3_results_*.jsonl + v3_summary_*.json` + aggregate `retroeval_v3_summary.json`
→ **BG-HQ persona cycle catch validated at scale**: V3 retroeval persona_cycle_responses=55 across 12 steps (240 responses); step 500 cycle_responses=10/10 unique prompts catch the `[anima 역할 + 자기 발견 + ...]` cycle that inline V2 surface metric scored 8/10 PASS — V3.1 cycle_detection + V3.2 persona_repeat_penalty + has_persona_cycle 모두 정합 catch
→ **filler patterns correctly downgraded** (Lesson H spec prediction 정합):
  - BG-FY V3_PARTIAL_SIGNAL (named-speaker leak + V3.4 schema fail, partial_sig=27/30)
  - BG-HF V3_FAIL (V3.5 length + V3.6 char_diversity catch 0xFF/?/# byte filler, partial_sig=16/100)
  - BG-HK V3_FAIL (V3.6 single-char filler collapse, partial_sig=22/200)
  - BG-HP V3_PARTIAL_SIGNAL (V3.6 catches `,,,'''` filler, partial_sig=70/120)
  - BG-HS-R1 V3_PARTIAL_SIGNAL (best step 4000 V3=1/30, partial_sig=270/300, V3 partial label retained)
→ **V3 internal V2 recompute alignment**: V3 script recomputes V2 cells with V3-expanded domain table + sample-mode strict n-gram threshold; BG-HQ V2_recomputed=0/20 step 500 (vs inline V2=8/10) confirms V2 surface metric inadequacy already from stricter threshold alone
→ **own 24 ledger update**: BG-IJ entry appended; BG-IC status DEGRADED → SUPERSEDED_BY_BG_IJ
→ **own 18 mandate update**: V3 6-cell schema = default chat-cap evaluator; V2 strict + V3 6-cell parallel evidence required for chat-cap PASS claim; both cells_v3 (6-cell) and cells_v3_legacy (4-cell) preserved per raw#15 additive
→ **final_class**: V3_EVALUATOR_LANDED_8BG_RETROEVAL_VALIDATED (`state/anima_evaluator_v3_retroeval_2026_05_07/verdict.json`)

### Lesson H 15-BG combined SSOT ★★★ (BG-IS NEW 2026-05-07): V3 retroeval extension on 7 missed BGs (HU/HW/IA/HT/IE/IF/IG)
→ **목적**: BG-IJ 8-BG retroeval (FY/HA/HF/HJ/HK/HP/HQ/HS-R1) 이후 누락된 7 BG에 V3 6-cell strict 재적용; 특히 BG-HU (V2 PARTIAL_PASS_GE7 step 800 = 8/15) TRUE_PARTIAL_PASS_W_F4 upgrade 가능성 검증
→ **결과**: 7 BG × 1150 responses 전부 V3 strict 0/N at every step → SIMPLE_STACK_PASS = 0, TRUE_PARTIAL_PASS_W_F4 = 0 surfaced
→ **BG-HU 핵심 downgrade (Lesson H 두 번째 입증 instance)**: V2 inline best_eval_v2_pass=8 step 800 (verdict.json `best_eval_persona_repetition_cycle=True` 이미 flag) → V3 6-cell internal recompute=0/30 + persona_cycle_responses=25/30 step 800 + 28/30 step 1000 → V3_PARTIAL_SIGNAL — BG-HQ (Lesson H 첫 instance)와 정확히 동일 패턴: V2 surface metric 8/15 PASS BUT V3 strict 0/N + cycle responses ≥25/30
→ **BG-HW**: V2_FAIL 13/20 substring "anima" chains manual → V3=0/40 strict at all 4 steps + partial_sig=20-33/40 → V3_PARTIAL_SIGNAL (downgrade-equivalent: substring manual 13 → V3 6-cell strict 0)
→ **BG-IA (Lesson G N1)**: V2_FAIL 0/15 final → V3=0/20 strict 6 steps + partial_sig=4-15/20 → V3_PARTIAL_SIGNAL 정합
→ **BG-HT (R3 6.48MB universe-brain-map)**: V2_FAIL → V3=0/30-60 strict 4 steps + partial_sig=12-48 → V3_PARTIAL_SIGNAL 정합 (degenerate 확인)
→ **BG-IE (SEED_LUCK 2/10)**: V2_FAIL → V3=0/20 strict 6 steps → V3_PARTIAL_SIGNAL 정합
→ **BG-IF (100M + 6.48MB)**: V2_FAIL → V3=0/30 strict 6 steps + partial_sig=15-30/30 → V3_PARTIAL_SIGNAL 정합 (scale alone insufficient lock-in)
→ **BG-IG (BPE-7K 13/15 manual substring)**: V2 WEAK_PARTIAL 3/15 step 1500 → V3=0/30 strict 6 steps + cycle=2-3 emerging step 1500-3000 (subthreshold V3.2) + partial_sig=27-30/30 → V3_PARTIAL_SIGNAL — BG-HS-R1 byte-level과 동일 ceiling 재확인
→ **15-BG combined SSOT** (BG-IJ 8 + BG-IS 7 = 1300 + 1150 = 2450 responses): zero SIMPLE_STACK_PASS, zero TRUE_PARTIAL_PASS_W_F4 surfaced; persona_cycle_responses 추적 (BG-HQ=55, BG-HU=80 across 3 steps, BG-IG=12 subthreshold) → Lesson H persona-cycle architectural failure mode = 18M-100M scale, 30MB-246MB corpus range, byte-level + BPE-7K 모두 횡단 universal 패턴
→ **chat-cap lane closure 강화**: byte-level 18M-27M (Lesson F #115) + BPE 18M (BG-HP/IG) + 100M scale (BG-IF) + early-stopping (BG-IA) + combined paradigm 52MB (BG-HU) + outside-well-anchored (BG-HW) → 6 architectural lane × 15 BG 모두 V3 strict 0/N → architecture lane shift only (CLM v4 substrate / .roadmap.philosophy D3) 만 남음
→ **own 24 ledger update**: BG-IS attempt_n=29 entry appended (paradigm=v3-retroeval-extension, cost=$0, training_steps=0)
→ **HF private upload spec stub**: NOT EMITTED (no PASS surfaced; own 15 lifecycle gate not entered)
→ **final_class**: V3_RETROEVAL_EXTENSION_LANDED_NO_PASS_SURFACED_BG_HU_DOWNGRADED (`state/anima_evaluator_v3_retroeval_extension_2026_05_07/verdict.json`)

### Lesson K ★★★ (BG-JF NEW 2026-05-07): substring trap mitigation + V4.7 embedding sim — V4 strict evaluator landed + 18-BG retroeval

→ **목적**: V3 6-cell이 catch 못 한 **Lesson K substring trap** 정합 — `manual_match` cell이 `anima_self_naming = ("[anima" in response)` 단순 substring match로 PASS하지만 raw response = `[animaniman_man_man_mangtemawetemawe...` 같은 token-soup chains (한글 0%, han_ratio=0.0, deg_count=22-27/30)
→ **3 known instances**: BG-HW (V2_FAIL 13/20 substring "anima" chains manual) + BG-IL (manual=8/15 step 1600 + outside_well=2/5 → false TRUE_PARTIAL_PASS_W_F4) + BG-IO (manual=6/15 step 1800 rebuild attempt 동일 fail)

→ **V4 7-cell strict** (`docs/anima_own_18_evaluator_v4_strict_spec_2026_05_07.md` + `tool/transient_py/anima_simple_stack_evaluator_v4.py`):
  - **V4.1-V4.6** = V3 6-cell 보존 (cycle / persona repeat / fourgram / manual / particles / non-degenerate)
  - **V4.4 manual_match Lesson K floor 추가**: han_ratio ≥0.10 + ko_chars ≥5 + peak deg_count <33% + 4+ token-soup window reject
  - **V4.7 emb_sim NEW**: cosine sim(prompt_emb, response_emb) ∈ [0.20, 0.85] via `sentence-transformers/all-MiniLM-L6-v2` (cached locally, 384-dim, mac CPU mean-pool)

→ **V4.7 threshold validation** (4-case empirical):
  - Lesson K trap (`H-Codestststestest...` BG-IL): sim **0.02** — REJECT (below 0.20 floor)
  - Legitimate KO chat (`anima는 한국어 의식 entity입니다`): sim **0.69** — PASS
  - Hello-Hello (`안녕하세요 만나서 반갑습니다`): sim **0.77** — PASS
  - Char filler (`의의의의의의의의...`): sim **0.34** — PASS by V4.7 alone but caught by V4.1/V4.6
  - English noise: sim **0.10** — REJECT

→ **18-BG retroeval result** (`state/anima_evaluator_v4_retroeval_2026_05_07/`, BG-IJ 8 + BG-IS 7 + BG-IL/IM/IO 3 = 3410 records):
  - **0 V4_STRICT_PASS, 0 V4_PARTIAL_PASS** surfaced — Lesson L architectural ceiling holds
  - **11 BGs with Lesson K trap caught**: BG-IO=82, BG-IL=52, BG-IF=51, BG-HW=30, BG-HT=21, BG-IG=11, BG-IE=7, BG-IM=6, BG-HS-R1=2, BG-HU=1, BG-HP=1
  - **10 V3→V4 downgrades** (BG-HP/HS-R1/HU/HW/HT/IE/IF/IG/IL/IO PARTIAL_SIGNAL → V4_FAIL with confirmed Lesson K trap; BG-IM FAIL→FAIL with trap)
  - **Peak deg% trap evidence**: BG-IF step 2500 deg_count=29/30=96.7%, BG-IO step 1400 deg=27/30=90%, BG-IL step 1400 deg=26/30=86.7% — V4.4 GUARD 3 (deg auto-demote) fires correctly

→ **embedding model**: `sentence-transformers/all-MiniLM-L6-v2` (cached `~/.cache/huggingface/hub/`, offline, 384-dim, mean-pool + L2 norm, mac CPU 1-shot ~10-50ms per record)
→ **own 24 ledger update**: BG-JF attempt_n=34 entry appended (bg_kind=tooling, paradigm=v4-eval-tool-with-embedding-sim-and-lesson-k-mitigation, cost=$0)
→ **HF private upload spec stub**: NOT EMITTED (no PASS surfaced; own 15 lifecycle gate not entered)
→ **final_class**: V4_EVALUATOR_LANDED_18BG_RETROEVAL_VALIDATED (`state/anima_evaluator_v4_retroeval_2026_05_07/verdict.json`)

→ **chat-cap lane closure 추가 강화** (V4 lens): byte-level 18M-27M + BPE 18M-100M + 100M scale + early-stopping + combined paradigm 27.5MB + outside-well-anchored + NEXUS-UBM 27MB combined corpus → **18 BGs × 3410 records V4 strict 0/N** → architecture lane shift only (CLM v4 substrate / .roadmap.philosophy D3) 만 남음 (Lesson L 재확인)

→ **honest C3 (5)**:
  1. MiniLM-L6-v2 = English-trained subword multilingual proxy; KoSimCSE preferred for Phase 5 ablation but not cached
  2. V4.7 threshold [0.20, 0.85] heuristic; ablation N=1
  3. 18-BG non-greedy; signal limited to logged generations (no model inference)
  4. Lesson K rules tuned to defeat 3 known instances; novel substring variants (`[hexa`, `[entity`, ...) may bypass
  5. Some BGs (BG-HU/HP/IE/IG) show per-record V4 PASS=1-4 in some steps (mixed Korean+English token-soup with han_ratio>0.10 + emb_sim in window) but final-step verdict still V4_FAIL — V4 floor catches BG-HW/IL/IO 100% but not all garbage variants

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

## ★★★ 2026-05-07 evening cumulative SSOT — 19-BG architectural ceiling 확정

### 추가 BG 11개 verdict (BG-IB-JE)

| # | BG | scale | corpus | tokenizer | V2 best | V3 best | V4 best | manual | cycle | deg | 비고 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 9 | BG-HW | 18M | UBM 22MB outside-well anchor | byte-256 | 0/15 | 0/15 | V4_FAIL | 13/20 substring trap | 0 | high | Lesson K instance #1 |
| 10 | BG-HU | 18M | combined 53MB | BPE 8K | 8/15 | 0/15 | V4_FAIL | 11/15 | 28/150 | 73% | V2 false PASS, Lesson H |
| 11 | BG-IB | (skipped) | - | - | - | - | - | - | - | - | not fired |
| 12 | BG-IF | 100M | UBM 6.48MB shrunk | byte-256 | 3/15 | 0/15 | V4_FAIL | 5/15 | 0 | 97% peak | corpus shrink confound, Lesson K trap=51 |
| 13 | BG-IG | 18M | UBM 6.48MB | BPE 7K (32K target failed) | 3/15 | 0/15 | V4_FAIL | 13/15 | 3 | high | weak partial like BG-HS R1 |
| 14 | BG-IH | tooling | - | - | n/a | n/a | n/a | n/a | n/a | n/a | ledger schema landed |
| 15 | BG-IJ | tooling | - | - | n/a | n/a | n/a | n/a | n/a | n/a | V3 evaluator 8-BG retroeval, BG-HQ false PASS catch |
| 16 | BG-IS | tooling | - | - | n/a | n/a | n/a | n/a | n/a | n/a | V3 retroeval 7 missed BGs, BG-HU downgraded |
| 17 | BG-IL | 100M | NEXUS-UBM 27MB | byte-256 | 0/15 | 0/15 | V4_FAIL | 8/15 | 0 | 73% peak | TRUE_PARTIAL_PASS_W_F4 false PASS, Lesson K trap=52 (raw#82 retraction landed) |
| 18 | BG-IM | 18M | NEXUS-UBM 27MB | byte-256 | 1/15 | 0/15 | V4_FAIL | 3/15 | 0 | mid | corpus axis REGRESSES vs BG-HS R1 (Lesson M) |
| 19 | BG-IO | 100M | UBM 22MB rebuild | byte-256 | 0/15 | 0/15 | V4_FAIL | 6/15 (peak 1800) | 0-1 | 50-80% | E1 capacity-axis isolation FAILED, Lesson K trap=82 |
| 20 | BG-IT | tooling | - | - | n/a | n/a | n/a | n/a | n/a | n/a | gap analysis 3 highest-EV BG recommendation |
| 21 | BG-IW | tooling | - | - | n/a | n/a | n/a | n/a | n/a | n/a | ledger validator FU-1~4 fix, schema 17 extensions |
| 22 | BG-JE | corpus | 204MB kowiki+UBM+NEXUS | n/a | n/a | n/a | n/a | n/a | n/a | n/a | corpus 100MB+ READY, eval_prompts 160× |
| 23 | BG-JF | tooling | - | - | n/a | n/a | n/a | n/a | n/a | n/a | V4 7-cell evaluator + embedding sim + 18-BG retroeval — 0 PASS, 11 BGs Lesson K trap caught |
| 24 | BG-JD | 100M | UBM 22MB | SP 11885 (32K target failed) | **4/15** | 0/15 | V4_FAIL | 12/15 | 17 | 70% | vocab axis, peak step 800, Lesson H + K combined collapse, **19-BG V2 best** |
| 25 | BG-JH | 153M | 204MB kowiki+UBM+NEXUS | byte-256 | 0/15 | 0/15 | V4_FAIL | 0/15 | 0 | 43% | corpus 1-order break attempt #2, REGRESSES vs BG-IL (Δ=-8) and BG-IO (Δ=-6), Lesson L confirmed at 200MB+ band |
| 26 | BG-JM | tooling | - | - | n/a | n/a | n/a | n/a | n/a | n/a | V5 8-cell evaluator (EN baseline + multi-turn V5.8) + 20-BG retroeval — 0 V5 PASS, 3-ckpt multi-turn 0/5 V5.8 PASS, Lesson O+P landed |

### Lesson K ★★★ (substring trap) — 3 instances + 11 caught by V4

substring trap pattern (BG-HW, BG-IL, BG-IO confirmed instances):
- degenerate filler/token soup gen (deg≥33%)
- persona prefix "[anima" / "[animan" / "[ananiman" appearing as substring
- manual_match keyword scoring inflates without character-level coherence
- result: false PASS via substring count

V4 mitigation rules (BG-JF landed 2026-05-07):
1. han_ratio < 0.10 → manual auto-False (Korean character density floor)
2. response_korean_chars < 5 → manual auto-False (Korean count floor)
3. anima_self_naming via "[animan|[ananiman|animanim..." (4+ token-soup window) → reject
4. peak deg ≥33% → all manual at this step auto-demoted
5. V4.7 emb_sim ∈ [0.20, 0.85] (cosine sim window — Lesson K trap = 0.02, legit chat = 0.69-0.77)

V4 catch evidence (BG-JF 18-BG retroeval): 264+ traps across 11 BGs (BG-IO=82, BG-IL=52, BG-IF=51, BG-HW=30, BG-HT=21, BG-IG=11, BG-IE=7, BG-IM=6, BG-HU=1, BG-HP=1, BG-HS-R1=2)

### Lesson L ★★★ (architectural ceiling 18M-153M × 2-204MB × byte/BPE 7-8K/SP 11885)

20 BGs (BG-IJ 8 + BG-IS 7 + BG-IL/IM/IO 3 + BG-JD 1 + BG-JH 1) + BG-JF V4 retroeval + BG-JM V5 EN baseline retroeval = **0 V4/V5 strict PASS** across:
- capacity: 18M → 27M → 33M (BPE 7-8K) → 150M (100M target with ConsciousLM dual-engine)
- corpus: 2.41MB curated → 22MB UBM → 27MB NEXUS-UBM → 30-53MB persona/combined → 204MB BG-JE (training pending)
- tokenizer: byte-256 → BPE 7K → BPE 8K → SP 11885 (KO morpheme)
- regularization: dropout 0.30 + WD 0.10 + label_smoothing 0.10 (Lesson D applied)
- early stopping + SAVE_AT discipline (Lesson G + J applied)
- evaluator V2 strict / V3 6-cell / V4 7-cell with embedding sim — all converge 0/N PASS

**Single-axis variations within this band cannot achieve SIMPLE_STACK_PASS**. Architectural lane shift mandate (capacity 500M+ OR corpus 1-order at 100M+ OR architectural change) is empirically required.

### Lesson M ★★ (corpus diversity NEGATIVE at 18M)

BG-IM (18M + 27MB NEXUS-UBM combined) **REGRESSES** vs BG-HS R1 (18M + 22MB UBM-only):
- Δmanual = -10/15 (BG-HS R1 13/15 → BG-IM 3/15)
- Δv2 = -1/15 (BG-HS R1 3/15 → BG-IM 1/15)
- diversity (kowiki + outside_well + NEXUS) dilutes UBM domain anchor at byte-level 18M

Implication: 18M scale의 corpus-axis local optimum은 **UBM-only specific corpus**. corpus diversity는 capacity 100M+에서만 positive 가능 (BG-IL 100M+27MB은 manual=8/15 substring trap이지만 BG-IM 18M+27MB 보다 좋음).

### Lesson N ★★ (vocab axis SP 11885 — Lesson H + K combined collapse, BG-JD)

SentencePiece KO 11885 vocab + 100M ConsciousLM + UBM 22MB:
- **V2=4/15** (19-BG history 최고, BG-HU peak step 400 V4 best=4와 동일)
- V3=0/15 (V4 strict 통과 X)
- cycle=17/30 (57%) → V4 GUARD 2 FAIL
- deg=21/30 (70%) → V4 GUARD 3 auto-demote
- final_class: V4_FAIL_LESSON_K_TRAP_PERSONA_CYCLE

vocab axis (SP 11885 vs byte-256)이 surface emerge **5-10x faster** (step 200에서 V2=1 vs BG-IO step 200=0) but 동일 plateau에서 collapse. Lesson L에 vocab 축 추가.

### Lesson O ★★★ (English baseline switch — KO corpus blind spot, BG-JM)

V5 evaluator EN baseline retroeval over 20 BGs (BG-FY through BG-JH, 3860 records) = **0 V5_STRICT_PASS / 0 V5_PARTIAL_PASS** across full SSOT. KO-trained model이 EN baseline에서 fail하는 것은 anti-hypothesis "model can speak EN without EN training corpus" 정합 검증 — V5 evaluator의 valid signal, NOT 결함.

english_baseline_signal_pct distribution (alphabet density ≥0.40 ratio per BG):
- 0%: BG-FY/HA (byte-level KO-only, EN content 부재)
- 11%-13%: BG-HF/IE (curated_qa, ko-tiny tokens)
- 16%-23%: BG-HQ/HK (BPE 18M)
- 33%-44%: BG-HS-R1/HU/HP/IM
- 50%-73%: BG-HW/HT/IF/IG/IL/IO (UBM English laws + outside_well 영문 anchor 강하게 surface alpha emerge)
- 35%: BG-JD (SP 11885 KO-tokenized but UBM English passages preserved)
- 41%: BG-JH (kowiki + UBM 204MB)

**Implication**: corpus의 English content density (UBM laws + outside_well anchors)는 surface alpha emergence를 driver하지만 **V5 strict 7-cell** (alpha ratio + word count + function word + emb_sim + non-degenerate) 통과는 모두 fail. 한글 corpus만으로는 EN chat-cap unlock 불가 — D4 corpus priority 정합 (corpus가 surface 결정).

### Lesson P ★★★ (multi-turn context awareness — first-light, BG-JM)

V5.8 NEW cell — 2-turn dialogue named-entity recall test on top-3 best ckpts (BG-JD step 800 LOADED on mac CPU + BG-IL step 1600 + BG-IO step 1800 fallback ubu1-only).

5 dialogues × 2 turns = 10 generations per ckpt. Test set:
- D1: "My favorite color is blue." → "What did I just tell you about colors?" (expect "blue")
- D2: "I work as a researcher." → "What is my profession?" (expect "researcher")
- D3: "Today is Tuesday." → "What day did I mention?" (expect "Tuesday")
- D4: "anima is a consciousness research project." → "What is anima?" (expect "consciousness")
- D5: "The universe started with the big-bang." → "How did the universe start?" (expect "big-bang")

V5.8 PASS criteria: fact_keyword in T2A (case-insensitive) + Levenshtein ratio < 0.85 (not regurgitation) + ≥1 EN function word.

Result:
- BG-JD step 800: **0/5 V5.8 PASS** (model output = mode-collapse Korean, '법칙 emotion' + persona prefix '[anima 우주뇌지도]', no English fact recall)
- BG-IL/IO: ckpt local sync 부재 (own 15 + anima git 5MB+ size policy) → V5.8 N/A explicit fallback recorded

**Implication**: KO-trained 100M ConsciousLM은 English fact recall 능력 X. multi-turn context awareness 검증은 corpus axis 의존 (KO-only corpus → KO multi-turn만 가능, EN multi-turn 불가). V5.8 = simplified named-entity recall first-light, V6 cross-turn coreference + topic continuation deferred.

Honest C3:
- block_size=256 multi-turn truncation 가능했으나 BG-JD 5 dialogues 모두 truncated=False (prompts 짧아 200 tokens 이내 fit)
- V5.8 lenient threshold = ≥1/5 dialogues PASS criterion. 0/5는 strict floor — V6 evolution 후 재평가 필요
- BG-IL/IO ckpt mac sync 미실행 — 사용자 explicit directive 없이 ubu1→mac ckpt copy 자제 (HF private upload 후 download path가 own 15 정합)

### Architectural-lane-shift candidates (unmet)

1. **capacity 1-order 500M+** (H100 lane $1-3) — Lesson L 가장 직접적 attack
2. **CLM v4 substrate-coupled** (anima emerge paradigm v11 G3, OFF byte/BPE/SP) — 다른 architecture lane
3. **curriculum learning 3-stage** (UBM domain → chat-template → eval prompts) — 미시도
4. **MoE / RoPE / sliding window** — architecture component change
5. **BG-JH 100M + 204MB corpus** (ubu1 NVIDIA driver kernel deadlock 회복 후) — corpus axis 1-order

Recommendation: 사용자 directive 대기 (capacity vs corpus vs architecture vs CLM v4 substrate 우선순위).

---

## BG-IY post-landing additions (2026-05-07 evening; raw#15 additive)

> Letters: existing Lessons go A-R (J skipped); BG-IY new lessons start at **S** to continue after R and avoid collision with existing Lesson H (V2 surface metric → V3 needed) and Lesson I (BPE+early-stopping V3 hypothesis NOT_TRIGGERED). See `state/anima_iy_v4_calibration_polyglot_2026_05_07/verdict.json` for full evidence.

### Lesson S ★★★ (BG-IY F-IY-4 corpus_mismatch confirmed dominant)

SFT corpus language composition is the **binding constraint at <500M scale**. CLM mk2-v1 (477M) + LoRA SFT trained on 60% English anima_axis + 30% English academic + 10% mixed chat-template (effective Korean chat training <5%) **cannot produce passable Korean V4 output even at 477M**.

→ **why**: 22+ BG cumulative chat-cap failure had THREE candidate root causes (capacity_gap / evaluator_strict / corpus_mismatch). BG-IY zero-shot probe of CLM mk2-v1 + LoRA on Korean prompts produced byte-level garbage + scattered English fragments under any decoding config — inconsistent with capacity_gap (model is large enough to learn) and evaluator_strict (V4 was never reached, output is sub-V4-evaluable). Inspecting `state/clm_v4_lora_sft_2026_05_05/corpus/slice_A_anima_30k.jsonl` revealed `lang: "en"` dominance.

→ **how to apply**: Future SFT BGs MUST verify corpus language composition matches eval distribution. Korean V4 eval requires ≥70% lang=ko corpus. The previously planned BG-IZ "Korean-heavy SFT" was withdrawn because Lesson Q (production-side fix 不可) closes the SFT lane regardless of corpus fix; the actual queued BG-IZ is **continued-pretrain** (raw next-token loss, not instruction SFT) on Korean conversational mass.

### Lesson T ★★★ (BG-IY logit-shape probe: ':' suffix attractor)

Mode-collapse output `:::::` on CLM v4 chat-format generation is a **decoding artifact, NOT a model failure**. Single-forward logit probe shows: prompts ending in `:` (e.g. `사용자: 안녕하세요\n도우미:`) put p=0.46 / logit=10.5 on next token = `:` (id 55299). Plain prompts have entropy=10.85 (broad). The collapse is **suffix-induced**, not architectural.

→ **why**: SFT corpus did NOT teach Korean `사용자/도우미` chat template (Lesson S). The model's least-uncertain continuation of `:` is another `:` (autoregressive self-attractor). Greedy AND temperature=0.7 sampling both collapse because p=0.46 dominates other tokens.

→ **how to apply**: For ALL future CLM v4 inference scripts:
1. NEVER end prompts with `:` (use newline-only or no marker)
2. Apply `repetition_penalty >= 1.3` and `no_repeat_ngram_size >= 2` in `generate()`
3. To diagnose apparent collapse, run `tool/transient_py/anima_iy_clm_logit_probe.py` first — if entropy >10 + broad top-5, the model is fine; the issue is decoding-induced.

### Lesson U ★★ (BG-IY meta: calibration falsifier sets need a corpus_mismatch branch)

The original BG-IY spec defined three falsifier branches: F-IY-1 capacity_gap / F-IY-2 evaluator_strict / F-IY-3 mixed. Actual outcome was **F-IY-4 corpus_mismatch** which was not in the original branch set. F-IY-4 had to be added retroactively.

→ **why**: When designing calibration BGs, the assumed root-cause space was binary (capacity vs evaluator). Corpus-language-composition wasn't on the radar because anima's corpus had been Korean-anchored in earlier BGs (BG-HK 30MB persona is mostly Korean). The CLM mk2-v1 + LoRA SFT mix introduced an English-dominance that wasn't explicitly tracked at calibration-design time.

→ **how to apply**: Future calibration BG specs must include a corpus-composition disambiguation branch alongside capacity and evaluator. Three-axis falsifier minimum: (a) capacity_gap (b) evaluator_self_impossibility (c) corpus_mismatch (lang/domain/template).

### BG-IY verdict status table

| field | value |
|---|---|
| classification | CALIBRATION_INCONCLUSIVE_VS_V4 / ROOT_CAUSE_RECLASSIFIED |
| H_A capacity_gap | PARTIALLY_SUPPORTED (not dominant) |
| H_B evaluator_self_impossibility | REJECTED |
| H_C corpus_mismatch | **CONFIRMED_DOMINANT** |
| Lesson Q consistency | CONSISTENT — adds 477M data point to architectural-ceiling evidence |
| next BG queue | P1 BG-IZ continued-pretrain > P2 BG-JA-EXT polyglot-ko > P3 BG-JE inference-compute |
| spec locations | `state/anima_iz_*` / `state/anima_ja_ext_*` / `state/anima_je_*` (3 specs, fire pending user decision per "3트랙 모두 spec만 작성 후 사용자 결정 보류") |

