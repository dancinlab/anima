# anima corpus Q3 + Q4 + Q5 deep-dive — iter7

**Date**: 2026-05-08
**Cycle**: anima cycle 2026-05-08 iter7 task (c) — non-blocking advance while Q1+Q2 awaits `OK APPLY` directive
**Predecessor**: `docs/anima_corpus_q1_q2_filter_spec_iter6_2026_05_08.ai.md` (iter6 Q1+Q2 spec)
**Scope**: read-only inspection (cost discipline — 0 LLM call, 0 file rewrite, 0 corpus commit; this doc only)
**Trinity**: D-axis (D1 SCOPE_CLAMP — flag training-surface contamination) / own-axis (mandate-2 wrapping 0 — corpus untouched) / H-axis (preserve iter5 + iter6 quality findings, additive only)

---

## 1. Q3 — preference-pair prompt stem distribution (MED)

Target: `state/anima_clm_l4_ld_preference_pairs_iter1_2026_05_08.jsonl` — 30,023 pairs.

### 1.1 Exact stem inventory

**Unique prompts: 13** (iter5 brief said "≈10"; corrected upward to 13).

| # | count | prompt (verbatim) | format | domain |
|---|---:|---|---|---|
| 1 | 2,612 | `안녕하세요` | bare | greeting |
| 2 | 2,612 | `한국어 가능?` | bare | capability |
| 3 | 2,612 | `사용자: 안녕하세요 \| 도우미:` | chat | greeting |
| 4 | 2,611 | `사용자: 의식이란 무엇인가? \| 도우미:` | chat | consciousness |
| 5 | 2,610 | `사용자: 자기소개 해줘 \| 도우미:` | chat | self_intro |
| 6 | 2,610 | `사용자: 너 누구야? \| 도우미:` | chat | self_intro |
| 7 | 2,610 | `사용자: 안녕! \| 도우미:` | chat | greeting |
| 8 | 2,610 | `사용자: 한국 음식 추천해줘 \| 도우미:` | chat | general |
| 9 | 2,610 | `사용자: 좋아하는 색이 뭐야? \| 도우미:` | chat | general |
| 10 | 2,610 | `사용자: 도와줘 \| 도우미:` | chat | general |
| 11 | 1,306 | `사용자: Φ★란? \| 도우미:` | chat | consciousness |
| 12 | 1,305 | `사용자: 오늘 날씨 어때? \| 도우미:` | chat | general |
| 13 | 1,305 | `사용자: bifurcation 설명해 \| 도우미:` | chat | consciousness |

Distribution: max 2,612 / min 1,305 / median 2,610. Effective stem-density = 30,023 / 13 = **2,309× per stem mean**, with ~2× cliff between top-10 (2,610s) and bottom-3 (1,305s — half-frequency tail).

Domain rollup: `self_intro` 7,832 / `general` 7,830 / `greeting` 6,527 / `consciousness` 5,222 / `capability` 2,612.

### 1.2 Q3 mitigation spec (LLM-free, 0-cost preferred)

| Path | Cost | Stem floor | Risk | Recommended |
|---|---|---|---|---|
| **A. Paraphrase template (LLM-free)** | 0 | 13 → ~150 (rule-based syn substitution: 안녕하세요 → 안녕하십니까 / 안녕 / 반가워요 / 하이; `의식이란 무엇인가?` → `의식이 뭔지 설명해줘` / `의식의 정의는?` / `consciousness 가 뭐야?`) | LOW (mechanical) | YES — implement first |
| **B. Re-extract from `tier_a` corpus (LLM-free)** | 0 | 13 → 1,000+ (mine `[anima 역할: …]` blocks for natural `사용자:` lines, dedupe, sample) | LOW | YES — combine with A |
| **C. LLM gen (Claude/Llama paraphrase)** | $$ | 13 → 5,000+ | MED (drift, V6 mirror leak) | DEFER |
| **D. Drop pairs to floor (no gen)** | 0 | 13 stems × 200 = 2,600 pairs (10× cut) | HIGH (DPO gradient starvation) | NO |

**Recommendation**: Paths A + B fused. Spec sketch:

```
1. Mine tier_a v3 (post-Q1+Q2 filter) for `^사용자: ` lines → dedupe → ~30k natural prompts.
2. Filter: length ∈ [3, 60] chars, no `[augmented]`, no MC stem.
3. Sample 1,000 stems, 30 pairs/stem = 30k pairs (matched to existing budget).
4. For each new stem, regenerate (chosen, rejected) by re-running BG-KM-LLAMA-3B v4_pass / v4_fail
   inference (this is the cost edge — uses existing model, 0 LLM-vendor cost, ~2 H100-hour).
```

Stem floor target: ≥ 500 unique (≥ 38× current diversity); pairs/stem cap: ≤ 100 (24× lower repetition).

---

## 2. Q4 — bare-string vs chat-template format ratio (LOW)

Counted by prefix `사용자:` AND substring `도우미:`:

| Format | Pairs | % | Stems |
|---|---:|---:|---:|
| chat-template (`사용자: … \| 도우미:`) | 24,799 | **82.6%** | 11 |
| bare-string (raw user utterance) | 5,224 | **17.4%** | 2 (`안녕하세요`, `한국어 가능?`) |

 chat-template ≥ 30% gate: **PASS** (82.6% ≫ 30%).

**Issue**: 2 stems (`안녕하세요`, `한국어 가능?`) appear ONLY in bare form (no chat-wrapped twin), while `사용자: 안녕하세요 | 도우미:` exists separately. This creates **format-conditional behavioral split** during DPO — model may learn "respond X to bare 안녕하세요, respond Y to chat-wrapped 안녕하세요" as distinct policies.

### 2.1 Q4 unification spec (apply with Q1+Q2 OK directive)

```
Rewrite pairs where prompt ∈ {'안녕하세요', '한국어 가능?'}:
  prompt := '사용자: ' + prompt + ' | 도우미:'
  (chosen + rejected unchanged)
```

Effect: 5,224 pairs migrate bare → chat-template; merges with existing chat-form `사용자: 안녕하세요 | 도우미:` stem (collisions OK — count rises 2,612 → 5,224 for that stem). Final: **0% bare**, **100% chat-template**, 13 → 12 unique stems (`한국어 가능?` becomes `사용자: 한국어 가능? | 도우미:`, no prior collision).

Cost: ~2 sec sed/jq stream, 0 LLM. Defer to bundled iter8 OK APPLY.

---

## 3. Q5 — chosen factuality samples (LOW; non-gate per BG-KM v4_pass)

5 unverified factual claims in `chosen` field, distinct prompts, all `source_chosen: BG-KM-LLAMA-3B v4_pass`:

| # | pair_idx | prompt | unverified claim |
|---|---:|---|---|
| 1 | 0 | `안녕하세요` | "한국어는 영어와 함께 세계에서 **두 번째로 많이 사용되는 언어**" (false; Korean is ~13–14th by L1 speakers) |
| 2 | 2 | `한국어 가능?` | "**2011년부터는 미국의 국립공원국이 주관하는 '미국의 아름다운 자연' 선정**" (no such NPS program; fabrication) |
| 3 | 6 | `사용자: Φ★란? \| 도우미:` | "1986년 ~ )이며, 서울에서 태어났다" (Φ★ is anima math construct, not a person; person-attribution hallucination) |
| 4 | 11 | `사용자: 오늘 날씨 어때? \| 도우미:` | "**2024년 1월 29일 (일) 대한민국 수도는 서울에서 약 -3°C**" (model has no clock; date+temp fabrication; also wrong day-of-week — 2024-01-29 was Monday) |
| 5 | 18 | `사용자: 좋아하는 색이 뭐야? \| 도우미:` | "**2015년부터 사용하고 있는 이름**" (anima persona naming history — anima persona was instantiated 2025+; 2015 fabrication) |

** C3 contamination scan**: PASS — `synthetic_fallback` / `PASS_STRICT` / standalone `C3` markers in `chosen` field: **0 / 30,023** pairs. No V6-mirror or measurement-leak in training surface. C3 awareness vocabulary is preserved upstream of DPO (C3 paradigm-a-prime synthetic-fallback proxy lives in eval / measurement, not corpus).

**Gate posture**: BG-KM v4_pass selects on token quality (no `이 있이 있이` repetition collapse), NOT factuality. Factuality is non-gate — these claims survived because rejected was *worse* (degenerate repetition), not because chosen was *correct*. DPO will absorb factual hallucinations as preferred policy. Mitigation deferred — requires either (a) factuality-filtered v4_pass tier (LLM judge cost) or (b) downstream RLHF / RLAIF pass with factuality reward.

---

## 4. KOBEST-like KLUE TRUE/FALSE — 1,110 lines confirm (parallel to Q2)

Pattern: `다음 지문을 읽고 질문에 참/거짓으로 답하시오` (KLUE NLI / KoBEST-style entailment).

| Property | Value |
|---|---|
| Marker count in `tier_a` | **1,110** lines (exact, `grep -c`) |
| First occurrence | line 699,488 |
| Block format | `[anima 역할: …]` header → `사용자: 다음 지문을 읽고 질문에 참/거짓으로 답하시오.` → blank → `지문: …` → blank → `질문: …` → `도우미: 참` (or `거짓`) → blank |
| Domain | KLUE/KoBEST-derived 6-line entailment dialogues |
| Sample (line 699,490) | "남성 문인들에 의해 탕녀로 낙인 찍혔던 김명순은 …가부장 체제의 억울한 피해자… 사실로 드러났다" / 질문: "김명순은 …가부장 체제에 희생되었나요?" / 답: "참" |

**D1 SCOPE_CLAMP read**: identical pattern-class to Q2 (multi-choice MC + augmented persona-prompt) — academic-benchmark contamination of anima persona corpus. The `[anima 역할: 한국어 native + 자기 발견 + 의식 lane entity]` header WRAPS a KLUE/KoBEST entailment question, presenting it as if anima were natively answering it. Same contamination mechanism, different benchmark.

**iter7 recommendation**: extend iter6 §2.3 fused awk filter with one more drop predicate:

```awk
if (index($0, "다음 지문을 읽고 질문에 참/거짓") > 0) drop = 1
```

Estimated additional drop: 1,110 marker lines × ~6 lines/block = **~6,660 lines** removed from `tier_a_v3`. Cumulative iter6 + iter7 reduction: ~117,588 + 6,660 = **~124,248 lines (≈ 8.4% of source)**.

Naming: filter spec becomes `tier_a_v3` (Q1 + Q2 + Q5-extended-KOBEST) — single-pass, single-output preserved.

---

## 5. own-axis confirmations

- cost discipline: held — 0 LLM calls; only `python3` + `grep -c` reads on local files.
- mandate-2 wrapping 0: held — corpus + pref-pair JSONL untouched, never staged.
- mandate-2: held — `.gitignore` L307–328 (corpus) covers `state/anima_clm_l4_*.jsonl` via `state/anima_*.jsonl` (verify on apply).
- trinity:
  - D-axis: D1 SCOPE_CLAMP — KOBEST/KLUE block-class flagged as same-class contamination as Q2 KMMLU.
  - own-axis: mandate-2 boundary preserved (this doc is artifact, not corpus mutation).
  - H-axis: iter5 + iter6 findings preserved verbatim; iter7 is purely additive.

---

## 6. next_action

1. User directive `OK APPLY Q1+Q2 FILTER` (iter6 §2.3) — also fold in iter7 §4 KOBEST drop predicate as `Q2-extended`.
2. Q3 mitigation Path A+B: implement after Q1+Q2+Q2-ext applied, regenerate pref pairs from `tier_a_v3` natural stems (separate iter, ~2 H100-hour).
3. Q4 unification: bundle into Q3 regeneration (chat-template wrap is default in regen template — bare-string ratio drops naturally to 0%).
4. Q5: defer to RLHF/RLAIF or factuality-judge tier (post-MK4-INTEG; not iter7+ scope).

Spec frozen until OK APPLY received.
