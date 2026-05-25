---
id: Hc_626
slug: emerge-candidate-g-h-tension-logits-g-revival
title: Emerge Candidate G+H — 16-layer tension trajectory + head_g prev-byte head 가 HF wrapper shim:999 에서 discard, revival 가능
domain: clm-architecture
status: candidate-sparse
source_doc: docs/anima_emerge_candidate_g_h_consolidated_revival_spec_2026_05_05.md
source_lines: 14-80
promoted_at: 2026-05-11
linked_h: Hc_623, decoder_v3.py:166-175, CausalLMOutputWithPast
notes: Discarded mechanism = single line (shim:999) + HF protocol shape mismatch. Both must be addressed.
cycle5_triage: "cycle #5 verify: FAIL — partial scaffolding (some F or L bullets) but no math identity; needs math axis OR atlas anchor to upgrade"
---

## Hypothesis
decoder_v3.py:166-171 의 tensions `List[Tensor[B,T]]` length 16 + decoder_v3.py:174-175 의 head_g prev-byte head 의 logits_g `[B,T,64000]` 가 HF wrapper shim:999 에서 `_logits_g, _tensions` 로 GC-eligible drop. CausalLMOutputWithPast 가 tensions field 없고 hidden_states shape mismatch ([B,T] scalar vs [B,T,D]) 가 직접 reuse 차단. Revival path 는 wrapper return path 수정 또는 새 OutputDataclass.

## Falsifiable Tests
- F-CAND-G-1: 16-layer tension trajectory variance > 0.1 (non-trivial)
- F-CAND-H-1: head_g logits_g 가 head_a logits_a 와 distinct (cosine < 0.95)
- F-G-H-revival: shim modify 후 (logits_a, logits_g, tensions) 모두 propagate

## Migration TODO
- [ ] shim:999 return 확장
- [ ] custom Output dataclass 정의 (HF protocol-compat)
- [ ] psi_direction = (1+cos(logits_a, logits_g))/2 surface
