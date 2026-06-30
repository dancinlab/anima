---
id: Hc_672
slug: a26-sparse-ppmd-text-heavy-ceiling-47-to-55
title: A26 sparse PPM-D (order 0-5 + Howard 1993 D-escape) 가 text-heavy class CEILING 47% → ≥55% advance, 6-repo 78.05% → 80%+ Pareto frontier close
domain: hxc-deploy
status: candidate-sparse
source_doc: docs/hxc_phase12_p4_a26_sparse_ppmd_design.md
source_lines: 17-65
promoted_at: 2026-05-11
linked_h: 53c711eb 78.05% MEASURED, A18 v3-o2/v4/v6 d631a902, A23 8f8197d5 first-tick pattern
notes: PROJECTION not measurement. H_5 ≈ 0.65 bit/byte natural English Shannon entropy ≈ 92% asymptotic. +5-8pp lift on 79KB text-heavy = ≥0.4pp aggregate close.
cycle5_triage: "cycle #5 verify: FAIL — partial scaffolding (some F or L bullets) but no math identity; needs math axis OR atlas anchor to upgrade"
---

## Hypothesis (FALSIFIABLE)
sparse PPM-D = sparse high-order (5-6) context lookup with D escape mechanism (Howard 1993) tuned for text-heavy natural English. text-heavy class CEILING 47% saving (현 53c711eb baseline) 이 ≥55% advance. 6-repo byte-weighted aggregate 78.05% (raw 137 80% Pareto 1.95pp gap) 를 +0.4pp close. A18 byte-context-order saturation 이 natural English text 의 binding constraint 아닌 가능성.

## Falsifiable Tests
- F-A26-1: text-heavy class saving ≥ 55% (현 47%)
- F-A26-4: > 100MB memory 사용 → REJECT (A23 budget 65536 contexts/order × 6 orders)
- F-A26-bypass: A26 lift 가 A18 v3-o2/v4/v6 와 orthogonal (additive vs redundant)

## Migration TODO
- [ ] PASS 1: sparse context tree spec (hash-indexed FNV-1a 64-bit → 16-bit slot)
- [ ] PASS 2: encode/decode round-trip selftest fixtures (5/5 byte-eq)
- [ ] PASS 3: 79KB text-heavy slice measurement
- [ ] 6-repo full scope 측정 후 80% Pareto verdict update
