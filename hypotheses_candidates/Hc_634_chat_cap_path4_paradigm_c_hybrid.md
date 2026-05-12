---
id: Hc_634
slug: chat-cap-path4-paradigm-c-hybrid-kogpt2-clm
title: Path 4 — paradigm-C hybrid (KoGPT2-base-v2 emit + CLM v4 substrate observer passive)
domain: clm-architecture
status: candidate-needs-scaffolding
source_doc: docs/anima_chat_cap_path_4_candidate_ranking_2026_05_05.md
source_lines: 123-149, 194-200
promoted_at: 2026-05-11
linked_h: BG-CG PASS_KOREAN_HYBRID_REPL_VIABLE, BG-BX VIABLE-English → ACHIEVABLE_NOW Korean
notes: Rank 2 — ACHIEVABLE_NOW. UX-grade not architectural. ±0.04 drift ≪ 0.1% of 41.86. Tension peak layer modal = layer 2.
cycle5_triage: "cycle #5 verify: WEAK_MATH_ONLY — math identity present, falsifier+honest scaffolding missing; needs F-list/L-list before re-verify can reach PROMOTE_READY"
---

## Hypothesis
KoGPT2-base-v2 (125M) emit Korean dialogue + CLM v4 mk2 re-encode (prompt+emit) 으로 Φ★ trajectory passive observe. Networks 가 gradient-coupled 아닌 UX bridge. 3 auto-fire turns × Korean prompts: 3/3 Korean coherent (100%), Φ★ drift ±0.0425, tension peak modal layer 2 consistent.

## Falsifiable Tests
- F-Path4-1: 5+ turn 시 100% Korean coherent rate ≥ 80% 유지
- F-Path4-2: substrate 가 KoGPT2 hidden 못보고 re-tokenized text 만 봄 → joint dialogue 가 아닌 read-only artifact
- F-Path4-3: emit unconditioned Korean prior (anima-axis-conditioned 아님) — 차이 측정 가능

## Migration TODO
- [ ] tool/transient_py/anima_emerge_chat_hybrid_repl.py harness 확장
- [ ] anima-axis-conditioned emit (KoGPT2 inject)
- [ ] joint gradient coupling 옵션 검토
