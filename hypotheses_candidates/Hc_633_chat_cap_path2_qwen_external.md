---
id: Hc_633
slug: chat-cap-path2-qwen-25-05b-external
title: Path 2 — Qwen 2.5-0.5B external integration (sub-variant a pure / b Qwen-emit + CLM-Φ★ passive)
domain: clm-architecture
status: candidate-unverified
source_doc: docs/anima_chat_cap_path_4_candidate_ranking_2026_05_05.md
source_lines: 71-92
promoted_at: 2026-05-11
linked_h: BG-EC fluent 3-prompt, Φ* proxy hidden_dim 896 vs 768 (Hc_614 aliasing risk)
notes: anima-native NO. Sidesteps chat-on-anima-substrate question entirely. Cost $0.
---

## Hypothesis
Qwen/Qwen2.5-0.5B 가 chat-cap emit substrate, CLM v4 retained for Φ★ measurement only. Korean "안녕" 31 Korean tokens / 0 ASCII fluent, English Hello world 103 ASCII fluent, Φ★ proxy on Qwen hidden_dim 896 = 41.86 (drift -0.005 vs CLM v4).

## Falsifiable Tests
- F-Path2-1: Qwen 0.5B Instruct variant 가 Path 1/3/4 chat-quality 보다 측정 가능 lift
- F-Path2-2: Hc_614 aliasing — Φ* proxy on D=896 가 D=768 와 cross-substrate 비교 가능 (geometry-invariant Hc_615 needed)
- F-Path2-3: BG-CV aliasing 측정값 -0.005 가 noise floor 안 (single-substrate test 한계)

## Migration TODO
- [ ] HF Hub download
- [ ] sub-variant (b) Qwen-emit + CLM-Φ★ passive observer harness
