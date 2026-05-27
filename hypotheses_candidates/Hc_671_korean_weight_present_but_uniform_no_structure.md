---
id: Hc_671
slug: korean-weight-present-but-uniform-no-structure-clm-v4
title: CLM v4 Korean weight 가 rank-uniform within Korean subspace (no syntax, no prompt-coupling) — heuristic PASS vs semantic FAIL decoupling
domain: clm-architecture
status: candidate-unverified
source_doc: docs/anima_emerge_chat_korean_only_constraint_landed_2026_05_05.ai.md
source_lines: 11-80
promoted_at: 2026-05-11
linked_h: BG-CA Korean rank 197 uniform, BG-CO ban 0-1000 no Korean, #115 architectural, 5701 Korean ids vocab subspace
notes: Greedy collapse to `하이` (loanword "hi") across all 3 prompts incl. `Hello`. Top-k diverges to surface vocab without particle/verb agreement.
---

## Hypothesis (third-angle confirmation of #115)
CLM v4 Korean weight 가 substrate 에 존재하지만 rank-uniform within Korean subspace — top-k diverges to 수행/상태/자체/하이/... 없이 morphological agreement / syntactic coherence. Greedy 가 `하이` loanword interjection low-information attractor 로 collapse (EN prompt `Hello` 도 동일). 3 angle confirmation: (a) BG-CA Korean rank-1000 uniform (b) BG-CO ban 0-1000 no Korean (c) Korean-only forced still no semantic = Korean lacks structure at all levels (ranking + attractor + subspace-internal).

## Falsifiable Tests
- F-korean-1: 다른 substrate (Path A v2 Llama-3.2-3B) 가 Korean-only constraint 하에서 syntactic structure 보유
- F-korean-2: heuristic threshold `>=5 glyphs + <50% mono` 가 semantic test 와 dissociated (heuristic PASS / semantic FAIL)
- F-korean-3: H100 BF16 distribution 이 mac CPU fp32 와 substantively 다른 결과

## Migration TODO
- [ ] morphology / syntax validator (현 glyph-count heuristic 불충분)
- [ ] Korean-only forced + temperature sweep (token diversity isolation)
- [ ] prompt-language coupling test on Path A v2 baseline
