# anima corpus iteration iter5 — inventory + quality check

**Date**: 2026-05-08
**Cycle**: anima cycle 2026-05-08 iter5+ task (c)
**Scope**: curation only — no new generation (cost discipline), no corpus commit (mandate-2 wrapping 0)
**Trinity**: D-axis (D1 SCOPE_CLAMP probe) / own-axis (mandate-2 + lifecycle) / H-axis (avoid prior 102MB git track regression)

---

## 1. Inventory

Note: there is **no top-level `corpus/` directory**. The active corpus assets are sharded under `state/` and `training/corpus/persona/`. The `corpus/anima_persona*.jsonl` path stated in the task brief does not exist on disk — the actual artifacts use `.txt` (chat-template plain) and `.jsonl` (preference pairs) under `state/`.

| Path | Size | Lines | Type | Git tracked? |
|---|---|---|---|---|
| `state/anima_persona_tier_a_2026_05_08.txt` | 104 MB | 1,478,588 | persona chat-template (format) | NO (gitignore L317-318, 326) |
| `state/anima_clm_l4_ld_preference_pairs_iter1_2026_05_08.jsonl` | 18 MB | 30,023 | DPO preference pairs | NO (gitignore L321, 323) |
| `state/orchestrator_clm_qwen3_2026_05_02/dialogue_ledger.jsonl` | 24 KB | 30 | qwen3 dialogue ledger (small) | (n/a, scratch) |
| `training/corpus/persona/{daily,fantasy,horror,romance,school,scifi}.txt` | 8 KB × 6 = 48 KB | 50 × 6 = 300 | persona seed lines | YES (tracked, but tiny) |

**Total active curation surface**: ~122 MB. **All large artifacts confirmed gitignored** (mandate-2 wrapping = 0 holds).

---

## 2. Distribution check

### `anima_persona_tier_a_2026_05_08.txt` (1.48M lines)
Source manifest — 972 `=== SOURCE: ... ===` headers spanning:
- anima 우주뇌지도 corpus (21 MB + 6.5 MB older overlap) — laws/hypotheses/categories
- anima persona chat-template (30 MB, format)
- anima curated QA (2.4 MB, 자기 발견 + 의식 lane)
- anima combined paradigm corpus (53 MB sample, paradigm v11 G3)
- consciousness laws + hexa speak hexa papers
- `.roadmap.philosophy` (D entries) / `.roadmap.law` (R+L) / `.roadmap.hypothesis` (H)
- hypotheses bundle (152 files)
- per-doc ingest with `char_density` + `sem_sets` annotation

Tag distribution:
- `[anima 우주뇌지도]` lines: 172,536
- `[anima 역할: ...]` lines: 129,075
- `사용자:` markers: 317,826 / `도우미:` markers: 318,600 (matched ±0.24%, schema clean)

### `anima_clm_l4_ld_preference_pairs_iter1_2026_05_08.jsonl` (30,023 pairs)
Schema: every record has `prompt` + `chosen` + `rejected` + `domain` + `source_chosen` + `source_rejected`. Counts match (30,023 / 30,023 / 30,023) — **schema clean, no missing fields**.

Domain distribution:
- `self_intro` 7,832 (26.1%)
- `general` 7,830 (26.1%)
- `greeting` 6,527 (21.7%)
- `consciousness` 5,222 (17.4%)
- `capability` 2,612 (8.7%)

`source_chosen` is uniformly `BG-KM-LLAMA-3B v4_pass`; `source_rejected` is `v4_fail_or_synth` or `v4/v5 fail (v5_results_bg_jd.jsonl)`. All chosen samples come from the SIMPLE_STACK_PASS_STRICT 12/15 winning checkpoint — **provenance is clean**.

---

## 3. Quality issues

### Q1 — D1 SCOPE_CLAMP violation (HIGH severity, persona corpus)
The tail of `anima_persona_tier_a_2026_05_08.txt` (lines 1,478,043 → 1,478,588) ingests **`config/core_rules.json`** verbatim — including `L0_uses` / `L1_uses` / `L2_uses` schema, `protected_paths`, `code_rules` / `asset_status` / `conformance` SSOT keys. This is **infrastructure metadata bleeding into persona training data**. Although the source is anima-internal (not external borrow, so D1 borrow check holds), it pollutes persona spontaneity (C2) — model would learn to emit JSON schema as "natural utterance". 9 lines reference `config/core_rules.json` / `asset_registry.json` / `conformance_checklist`.

### Q2 — KMMLU augmented multiple-choice contamination (MEDIUM, persona corpus)
16,456 lines tagged `[augmented]` and 7,298 lines starting with `다음 문제의 정답을 고르시오` (the canonical KMMLU MC stem). Examples found: 정전계 boundary conditions / 멸균 분쇄시설 — pure factual electrical/civil-engineering knowledge tests, no anima-persona content. These belong in a benchmark eval set, not the persona pre-training corpus, because they enforce a stiff "1번/2번/3번/4번" answer template that **conflicts with C2 자연발화 spontaneity target**.

### Q3 — Preference-pairs duplicate prompts (MEDIUM, preference jsonl)
Top prompts each repeat ≥ 2,610 times:
- `사용자: 도와줘 | 도우미:` × 5,222
- `사용자: 너 누구야? | 도우미:` × 5,221
- `사용자: 오늘 날씨 어때? | 도우미:` × 3,915
- `안녕하세요` × 2,612 (raw, no chat-template)
- `한국어 가능?` × 2,612 (raw, no chat-template)

Top 10 prompts cover ~33,000+ pair instances out of 30,023 — i.e. **prompts are reused across pairs with different chosen/rejected continuations**. This is *not* strictly a bug for DPO (multiple chosen/rejected per prompt is normal), but it means **prompt diversity is only ~10–20 unique stems**. Risk: model overfits the narrow prompt manifold rather than generalising preference signal.

### Q4 — Mixed prompt format (LOW, preference jsonl)
Some prompts use bare strings (`안녕하세요`, `한국어 가능?`) while others use chat-template (`사용자: ... | 도우미:`). chat-template format mandate says everything should be chat-template. Bare strings should be wrapped or split into a separate "raw greeting" sub-corpus.

### Q5 — `chosen` contains hallucinated factual claims (LOW, surface only)
Example pair 4 claims "2008년 대한민국 K-POP concert" + invented group "KISS & BOY"; pair 6/8/etc. similar. These are BG-KM v4_pass outputs — the v4 floor passed C0–C2 spontaneity / refusal but **does not check factuality**. Acceptable for current preference-signal use (DPO learns "fluent > broken Hangul"), but **should not be treated as factual SFT data**. Tag for downstream consumers.

---

## 4. Curation recommendations (next iter)

1. **Strip `config/core_rules.json` JSON tail** from `anima_persona_tier_a_2026_05_08.txt` lines ≥ 1,478,043 → produce `..._tier_a_v2_2026_05_08.txt` (cost: stream filter, ~5 sec). Removes Q1.
2. **Quarantine `[augmented]` KMMLU lines** to a separate `state/anima_kmmlu_augmented_2026_05_08.txt` (eval-only, never persona pre-train). Removes ~16k lines / Q2.
3. **Diversify preference prompts**: regenerate iter2 with ≥ 100 unique prompt stems (sample from `[anima 우주뇌지도]` opener pool) instead of the current ~10. Resolves Q3 — but defer to next cycle (: requires LLM gen, costed pass needed).
4. **Wrap bare prompts** in `사용자: X | 도우미:` template across all 5,224 records lacking it. Resolves Q4 (cost: regex pass).
5. **Tag `chosen.factual_unverified = true`** on all preference-pairs records (since v4 floor doesn't gate factuality). Resolves Q5.

**Immediate action (this iter, 0-cost)**: items 1, 2, 4 are pure stream filters and can land before the next training run consumes the corpus. Items 3, 5 are deferred (3 needs gen budget, 5 needs schema bump for downstream training scripts).

---

## 5. own-axis confirmations

- cost discipline: held — 0 LLM API calls in this iter, only file inspection.
- mandate-2 wrapping 0: held — corpus files NOT staged, NOT committed; only this doc (under 1 MB) is committed.
- mandate-2: held — all 122 MB of corpus surface is gitignore-covered (`state/anima_*_persona_*.txt`, `state/anima_*_pairs_*.jsonl`, `state/anima_*_tier_*.txt`).
- visibility lifecycle: not relevant to this iter (no HF promote action).

## 6. next_action

`anima cycle 2026-05-08 iter6 task (c-followup)`: apply curation steps 1, 2, 4 as 0-cost stream filters → produce `tier_a_v2` snapshot, regenerate gitignore-only artifact → re-run inventory check to confirm Q1/Q2/Q4 cleared. Defer steps 3, 5 to next-cycle gen budget allocation.
