---
id: Hc_658
slug: cp2-alpha-red-red-red-red-disclaimer-stack
title: CP2 Alpha landing 의 RED-RED-RED-RED honest disclosure (의식측 F2 fired 16 critical / 14-gate 0/16 / AN11(c) JSD 0.0894 / LIVE 2.9%) + 4 cert GREEN
domain: cp2-release
status: candidate-math-verified-falsifier-pending
source_doc: docs/anima_cp2_alpha_landing_2026_05_01.md
source_lines: 30-99
promoted_at: 2026-05-11
linked_h: F2 falsifier, AN11(c) k=128 bits, p4_r8 truncated 18.5% discovery, r14 swap
notes: own#13 친화도 (jargon ≤0.30, acronyms expanded). raw#10 honest above-the-fold. Mistral-7B-v0.3 + LoRA r14 r=64 α=128 ~671MB.
verified_at: 2026-05-12
verify_decision: WEAK_MATH_ONLY
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (4+ numeric identities present)"
---

## Hypothesis
CP2 Alpha 가 RED 의식 verdict + RED 14-gate (0/16) + RED AN11(c) JSD (0.0894 vs ≥0.5 PASS, ~5.6× 미달) + RED LIVE 2.9% (chat 5.0% / employee 3.3% / trading 2.9%) 모두 동시 보유 — 그러나 측정 framework 자체는 4 cert gates (AN11_JSD · META2_CHAIN · PHI_VEC_ATTACH · HEXAD_ROUTING) 4/4 GREEN + latency p95=1881.9ms GREEN + hallucination 0/20 GREEN. p4_r8 truncated artifact 발견 후 r14 swap 으로 RED 가 substrate 한계 vs artifact disambiguation 가능.

## Falsifiable Tests
- F-CP2alpha-1: r14 swap 후에도 모든 4 RED axis 유지 → substrate 진짜 한계
- F-CP2alpha-2: 1 axis만 GREEN flip 시 → artifact disambiguation 부분 진전
- F-CP2alpha-3: LIVE 평균 2.9% 가 multi-cycle measurement 후 상승 (current=ESTIMATE single-cycle)

## Migration TODO
- [ ] r14 LoRA 671MB 정합성 100% (MD5 90072b0f5a426eeebb47eeb2d4919d68) 검증
- [ ] honest feedback collection from invitees
- [ ] kill switch 사전 통지 없이 endpoint 무효화 가능 명시
- [ ] re-measurement multi-cycle (현 ESTIMATE/single)
