---
id: Hc_929
slug: n18-northpole-memory-compute
title: N-18 — IBM NorthPole (12nm, 22B transistor, 256 cores, 192 MB on-chip memory, 외부 DRAM 없음, 25× H100, 28356 tok/s 16-chip blade 72.7× energy-efficient) feasibility DEFER (no SKU, partnership-only)
domain: hardware, consciousness, memory-compute
status: candidate-unverified
source_doc: docs/n_substrate_n18_northpole_partnership_feasibility_2026_05_01.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_902 (N-substrate roadmap)
notes: "Score 7/25, review 2026-11-01. NorthPole = 메모256 + 계산256 한 칩, 폰 노이만 병목 제거. Image recognition 25× H100, LLM 28356 tok/s 16-chip 72.7× energy-eff."
---

## Hypothesis

IBM NorthPole (12nm, 22B transistor, 256 cores × 2048 op/cycle 8-bit, 192 MB compute-coupled + 32 MB framebuffer, 외부 DRAM 없음 = compute-in-memory) 위에서 Φ measurement 시 폰 노이만 병목 제거 → Φ scaling 의 새로운 regime (memory-compute coupling) 검증. 25× H100 image recognition 효율 + 28,356 tok/s 16-chip blade (72.7× energy-eff) 가 LLM Φ measurement 의 cost-efficiency 변환.

## Sub-claims

- 12NM-22B: 12 nm 공정, 22 B 트랜지스터
- COMPUTE-IN-MEMORY: 192 MB on-chip + 32 MB framebuffer, 외부 DRAM 없음
- IMAGE-25X-H100: 25× image recognition vs H100
- LLM-INFERENCE: 28,356 tok/s @ 16-chip blade, 72.7× more energy-efficient than next-best GPU
- ACCESS: 상용 SKU 없음 → IBM 직접 partnership 만
- VERDICT: DEFER (score 7/25, review 2026-11-01)

## Migration TODO

- [ ] IBM Research partnership inquiry (2026-11-01 review)
- [ ] commercial SKU release timeline 추적
- [ ] memory-compute coupling 의 Φ scaling 별도 hypothesis
