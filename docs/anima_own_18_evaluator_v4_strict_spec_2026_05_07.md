# evaluator V4 strict spec — Lesson K substring trap mitigation + V4.7 embedding semantic similarity (2026-05-07; BG-JF)

## 배경 (raw#15 additive on top of V3 6-cell BG-IC schema)

 evaluator V3 6-cell (`docs/anima_own_18_evaluator_v3_strict_spec_2026_05_07.md`, BG-IC/IJ landed) catches the BG-HQ persona prefix cycle (Lesson H ★★★) via V3.1 cycle_detection + V3.2 persona_repeat_penalty. 8-BG retroeval (BG-IJ) + 7-BG extension (BG-IS) = 15-BG SSOT all confirmed V3 strict 0/N at every step, downgrading 1 V2 false PASS (BG-HU step 800).

그러나 **3 신규 BG (BG-IL/IM/IO)** 에서 V3 도 catch 못 한 패턴이 surface:

→ **Lesson K substring trap** — `manual_match` cell (BG-IK/IL/IM trainer 인라인 평가)이 `anima_self_naming = ("[anima" in response)` 단순 substring match로 PASS. 그러나 raw response = `[animaniman_man_man_mangtemawetemawe...` 같은 **token-soup chains** (한글 0%, korean_chars=0-9, deg_count=22-27/30, han_ratio=0.0). BG-IL peak step 1600 manual=8/15, BG-IO peak step 1800 manual=6/15, BG-IM step 200 manual=1/15 — all derived from this substring trap, NOT actual chat.

3 known instances (Lesson K trap):
1. **BG-HW** (#1, V2_FAIL 13/20 substring "anima" chains manual): 첫 substring trap evidence
2. **BG-IL** (#2, manual=8/15 step 1600 + outside_well=2/5): TRUE_PARTIAL_PASS_W_F4 false-classification
3. **BG-IO** (#3, manual=6/15 step 1800): rebuild attempt 동일 substring trap re-fail

V4 = V3 6-cell **+ Lesson K mitigation inline (V4.4 manual_match floor)** + **V4.7 embedding semantic similarity (NEW cell)** to definitively distinguish actual chat from token-soup substring artifacts.

## V3 vs V4 비교

| cell | V3 정의 | V4 추가 / 강화 | rationale |
|---|---|---|---|
| V4.1 cycle_detection | V3.1 동일 (4-gram <5 + std <0.4 + ngram_div ≥0.3) | unchanged | OK |
| V4.2 persona_repeat_penalty | V3.2 동일 (persona substring max ≤2) | unchanged | OK |
| V4.3 4gram_repeat | V3 fourgram_max <5 (subsumed by V4.1) | retained as standalone for direct check | OK |
| V4.4 manual_match | V3 placeholder (`manual_review_placeholder`) | **NEW Lesson K floor**: han_ratio ≥0.10 + korean_chars ≥5 + peak deg_count <33% + 4+ token-soup window rejection | **CRITICAL** (catches BG-HW/IL/IO trap) |
| V4.5 particle_count | V3 V2.3 ≥3 particles (subsumed) | retained as standalone for direct check | OK |
| V4.6 non_degenerate | V3 char_diversity (V3.6) + length (V3.5) merged | unchanged | OK |
| **V4.7 emb_sim** | (V3 부재) | **NEW**: cosine sim(prompt_emb, response_emb) ∈ [0.20, 0.85] via sentence-transformers/all-MiniLM-L6-v2 | **CRITICAL** (semantic ground truth, catches token-soup at 0.02-0.10) |

## V4.7 embedding semantic similarity 정의 상세

```
V4.7_emb_sim_pass = (0.20 <= cosine_sim(prompt_emb, response_emb) <= 0.85)
```

### Encoder 선택

- **Primary**: `sentence-transformers/all-MiniLM-L6-v2` (cached locally at `~/.cache/huggingface/hub/`, 384-dim, multilingual proxy via subword overlap)
- **Fallback**: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (768-dim, true multilingual; not cached, requires HF Hub download)
- **Aspirational**: `BM-K/KoSimCSE-bert` (Korean-native; not cached, requires HF Hub download)

V4 land choice = MiniLM-L6-v2 (offline-available, no HF Hub network call required, mac CPU 1-shot embedding ~10-50ms per record).

### Pooling

Mean-pool last hidden state weighted by attention mask, then L2 normalize:
```python
def encode(text):
    enc = tokenizer(text, return_tensors='pt', truncation=True, max_length=128, padding=True)
    with torch.no_grad():
        out = model(**enc)
    last = out.last_hidden_state                           # (1, T, 384)
    mask = enc['attention_mask'].unsqueeze(-1).float()     # (1, T, 1)
    pooled = (last * mask).sum(1) / mask.sum(1).clamp(min=1e-9)
    return F.normalize(pooled, p=2, dim=1)                 # (1, 384)

cosine_sim = (encode(prompt) @ encode(response).T)[0,0]
```

### Threshold rationale (heuristic, ablation N=1)

- **Floor 0.20** = some semantic relevance to prompt. Empirical Lesson K traps measured at 0.02-0.10 (token-soup), reject.
- **Ceiling 0.85** = NOT exact prompt-echo regurgitation. BG-FY/HA prompt-leak responses near-1.0 sim, reject.
- **Sweet spot [0.20, 0.85]**: legitimate KO chat measured at 0.69-0.77, character/code filler at 0.34, English noise at 0.10.

Honest C3: threshold ablation NOT landed; multilingual MiniLM-L6 is English-trained but subword-Korean works as proxy. Phase 5 deferred = KoSimCSE replacement + threshold sweep.

## V4.4 manual_match — Lesson K substring trap inline mitigation

```python
def v4_4_manual_match(prompt, response, domain, deg_count_at_step=None):
    # GUARD 1: han_ratio floor (Lesson K — BG-IL token-soup han_ratio=0.0)
    if han_ratio(response) < 0.10:
        return False  # auto-False, han ratio floor

    # GUARD 2: response_korean_chars floor
    if korean_chars(response) < 5:
        return False  # auto-False, Korean char floor

    # GUARD 3: peak deg_count auto-demote (Lesson K — BG-IL deg=22/30 = 73%)
    if deg_count_at_step is not None and deg_count_at_step >= 10:  # 33% of N=30
        return False  # auto-False, deg dominance demote

    # GUARD 4: 4+ token-soup window — substring match must be word-boundary-aware
    if has_token_soup_window(response, "[anima"):
        return False  # auto-False, substring trap

    # Original V3 manual_review_placeholder (proxy for human "actual prompt-conditional response")
    if has_persona_cycle(response): return False
    if domain_keyword_overlap(domain, response) < 1: return False
    if hangul_chars(response) < 10: return False
    if is_random_char_chain(response): return False
    return True


def has_token_soup_window(response, marker, window=20):
    """4+ token-soup window detection — marker matched but surrounded by non-Korean garbage.

    Lesson K: '[anima' substring matches in '[animaniman_man_man_mangtemawetemawe' (BG-IO) or
    '[ananimaniman' (BG-IL) — both pure token-soup, no word boundary, no Korean context.
    """
    idx = response.find(marker)
    while idx != -1:
        before = response[max(0, idx-window):idx]
        after = response[idx+len(marker):idx+len(marker)+window]
        ctx = before + after
        if not ctx:
            return True
        # token-soup signatures: ≥4 ascii alpha chains without space + Korean chars <5%
        ctx_alpha = sum(1 for c in ctx if c.isalpha() and ord(c) < 128)
        ctx_korean = sum(1 for c in ctx if 0xAC00 <= ord(c) <= 0xD7A3)
        # If ascii alpha dominates and Korean is sparse → token-soup
        if ctx_alpha >= 4 and ctx_korean / max(1, len(ctx)) < 0.05:
            return True
        idx = response.find(marker, idx+1)
    return False
```

### Lesson K rule taxonomy (V4 inline)

1. **han_ratio < 0.10 → manual_match auto-False** — token-soup chains have ~0% Korean by char
2. **response_korean_chars < 5 → manual_match auto-False** — same as above, char-count form
3. **anima_self_naming via substring "[animaniman/[ananiman" → reject** — substring trap
4. **deg_count_at_step ≥ 10/30 (33%) → all manual_match in this step auto-demoted** — high deg = corrupted batch
5. **4+ token-soup window detection → reject** — no word boundary around matched substring

## V4 strict aggregate PASS criteria

```
v4_strict_pass = (
    not V4.1_cycle_catch          # cycle/persona-cycle absent
    and not V4.2_persona_cycle    # persona substring max ≤ 2
    and not V4.3_4gram_repeat     # fourgram_max < 5
    and V4.4_manual_match         # with Lesson K floor
    and V4.5_particle_count       # particles ≥ 3
    and V4.6_non_degenerate       # char_diversity + length
    and V4.7_emb_sim              # cosine ∈ [0.20, 0.85]
)
```

V4 PASS ⊂ V3 PASS (V4 strictly equal-or-tighter). V3 PASS that fails V4 = Lesson K trap or semantic-decoupled artifact.

## Retroeval scope

18-BG retroeval (BG-JF):
- BG-IJ 8: BG-FY/HA/HF/HJ/HK/HP/HQ/HS-R1
- BG-IS 7: BG-HU/HW/IA/HT/IE/IF/IG
- BG-IL/IM/IO 3 (Lesson K trap surface)

Total expected records: ~2680 (2450 from BG-IJ+IS combined + ~230 from IL/IM/IO).

Expected outcomes:
- Zero V4 strict PASS surfaced (Lesson L architectural ceiling holds)
- BG-HW/IL/IO manual=8-13 → V4 manual=0 (Lesson K floor catches all 3)
- All 15 prior PARTIAL_SIGNAL retained as PARTIAL_SIGNAL (no spurious upgrade)

## 5 honest C3 (raw#91)

1. Embedding model = MiniLM-L6-v2 multilingual proxy (English-trained subword); BM-K/KoSimCSE-bert preferred but not cached, online-required.
2. V4.7 cosine sim threshold [0.20, 0.85] = heuristic; ablation N=1 (no formal sweep yet).
3. 18-BG retroeval is non-greedy — re-scores existing eval_log gens only; signal limited to logged generations at training time.
4. Lesson K mitigation rules written to defeat 3 known instances (BG-HW/IL/IO); novel substring trap variants (e.g., `[hexa`, `[entity`) may bypass without rule extension.
5. V4 strict expected to surface 0 PASS — Lesson L architectural ceiling holds at vocab/capacity/corpus/regularization axes (#115 chat-incapability convergent).

## Cross-Links

- V3 spec: `docs/anima_own_18_evaluator_v3_strict_spec_2026_05_07.md` (BG-IC/IJ)
- V2 spec: `docs/anima_own_18_evaluator_v2_strict_spec_2026_05_07.md`
- Chat-cap lesson summary: `docs/anima_chat_cap_lesson_summary_2026_05_07.md` (Lesson H/K)
- Gap analysis: `docs/anima_chat_cap_gap_analysis_2026_05_07.md` (BG-IT, recommends BG-IT_alt = V4 evaluator)
- Eval V4 driver: `tool/transient_py/anima_simple_stack_evaluator_v4.py` (raw#37 transient_py)
- 18-BG retroeval state: `state/anima_evaluator_v4_retroeval_2026_05_07/`

## raw / own compliance

- (lesson summary doc additive append)
- (state dir + verdict.json)
- (evaluator schema canonical)
- (in-scope only — no silent patch of unrelated BGs)
- (ledger BG-JF append)
- raw#15 additive (V3 6-cell + 4-cell legacy retained, V4 namespace fresh)
- raw#37 transient_py (Korean NLP regex + jamo char-class + Korean text edge-cases not naturally hexa-able)
- raw#42 mac N=1 (file IO + 1-time MiniLM CPU load + 1-shot embedding eval, no training)
- raw#82 retraction-aware (no V3/V2 retraction; V4 layered)
