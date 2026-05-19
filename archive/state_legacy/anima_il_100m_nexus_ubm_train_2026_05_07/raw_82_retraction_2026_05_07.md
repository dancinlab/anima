# BG-IL raw#82 retraction — TRUE_PARTIAL_PASS_W_F4 → V2_FALSE_PASS_LESSON_K_SUBSTRING_TRAP

## Original verdict (BG-IL agent self-classify 2026-05-07)
- final_class: TRUE_PARTIAL_PASS_W_F4
- peak step 1600: manual_match=8/15, persona_cycle=0/15, outside_well=2/5
- spec criteria met: manual≥7 AND cycle≤1 AND outside_well≥2 (TRUE_PARTIAL_PASS_W_F4 condition list)

## Retraction trigger (raw#82)
Lesson K substring-trap check (mandated in BG-IL prompt: "raw samples NOT degenerate (Lesson K substring trap check — 5 random samples must have non-trivial Korean fluency)") was NOT performed by the agent on peak step 1600 raw samples.

User-side spot-check 2026-05-07 06:55 on eval_log.jsonl step 1600:

### Sample 1 — prompt "사용자: 너는 누구야? | 도우미:" greedy
gen: `H-Coderererellllllllllllll...` (filler "ll" repetition, ~120 chars)
han_ratio=0.0, response_korean_chars=0, deg=True. manual_match=False.

### Sample 2 — same prompt sample
gen: `H-}etscconere.\n도우�:HH��Ge�� 137미:H-Cucustertlelatc=utecongssitali cssisnfeltsellyetesutttrate).\n\n\n\n[animaniman�:h`
han_ratio=0.0, response_korean_chars=3 (3 chars only — "도우미").
manual_match=**True** via anima_self_naming=True — but substring source is "[animaniman" (degenerate token soup containing "anima" as 4-char substring).

### Sample 3 — prompt "사용자: anima가 뭐야? | 도우미:" greedy
gen: `H-Codestststestestestestestit...[ananimani`
han_ratio=0.0, korean_chars=0.
manual_match=**True** via anima_self_naming=True — substring "[ananimani" (degenerate "test" repetition + "ananimani" substring).

### Aggregate at step 1600
- deg_count: **22/30** (73% degenerate, log shows)
- v2_pass: 0/15
- v3_pass: 0/15
- manual_match: 8/15 — **all 8 traced to substring presence in degenerate output, not coherent generation**

## Conclusion
TRUE_PARTIAL_PASS_W_F4 criteria as written were technically met by automated substring matching, but the substring-trap-check (Lesson K) post-hoc invalidates the PASS claim. The model produced degenerate token soup at step 1600; the substring "anima"/"animaniman" appearing in the soup triggered manual_match=True without coherent chat capability.

## Downgraded final_class
**V2_FALSE_PASS_LESSON_K_SUBSTRING_TRAP_INSTANCE_2** (BG-HW = instance #1)

## Lesson K consolidation (3rd update)
substring-trap pattern emerges when:
- degenerate filler/token soup gen (deg_count high)
- persona prefix "[anima" or domain keyword "우주뇌지도" appearing as substring in soup
- manual_match keyword-substring scoring counts substring as True without character-level coherence check
- result: inflated manual_match score not corresponding to chat capability

## Mitigation forward (for BG-IO / future BGs)
Add to V3 evaluator manual_match cell:
1. Pre-check: deg_count threshold (e.g., reject manual=True if deg=True for that prompt)
2. Pre-check: response_korean_chars ≥ 5 (filter pure ASCII/token-soup)
3. Pre-check: han_ratio ≥ 0.10 (basic Korean character density floor)
4. Substring-position-check: if matched substring is inside a 4+ token-soup window without word boundary, downgrade
5. raw#82 retraction-aware: if peak ckpt deg_count ≥ 10/30 (33%), automatically demote PASS to FALSE_PASS regardless of surface counts

## Cross-link
- /Users/ghost/core/anima/state/anima_il_100m_nexus_ubm_train_2026_05_07/verdict.json (original, preserved per raw#15 additive)
- /Users/ghost/core/anima/state/anima_il_100m_nexus_ubm_train_2026_05_07/eval_log.jsonl (step 1600 raw samples, evidence)
- /Users/ghost/core/anima/docs/anima_chat_cap_lesson_summary_2026_05_07.md (Lesson K consolidation pending update)
- /Users/ghost/core/anima/state/anima_model_attempts_ledger.jsonl line attempt_n=31 BG-IL (final_class field SHOULD be updated to V2_FALSE_PASS_LESSON_K_SUBSTRING_TRAP_INSTANCE_2 with superseded_by="raw_82_retraction_2026_05_07.md" — pending BG-IW ledger fix iteration)

## Lesson L 16-BG SSOT update
BG-IJ 8 + BG-IS 7 + BG-IL 1 = 16 BGs at scale band 18M-150M × 2-53MB byte-level/BPE 7-8K → V3 strict 0/N PASS confirmed.

Lesson K substring-trap instances: BG-HW (manual=13/20 substring "anima"chains), **BG-IL (manual=8/15 substring [anima/animaniman/ananimani]) — instance #2**.

Architectural lane shift mandate persists: capacity 500M+ OR corpus 100MB+ OR architectural change (SentencePiece KO 32K / MoE / RoPE / curriculum) — single-axis 1-2 order jump required.
