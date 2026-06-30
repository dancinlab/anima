---
id: Hc_959
slug: 18-conditions-verification-audit
title: 18 조건 verification audit (DD122) — V1-V18, CE 17/18 PASS (216 trials 176, 81%). V8 MITOSIS factory bypass BUG. V9 PHI_GROWTH 임계 1.1→0.85 붕괴. V10 BRAIN_LIKE factory bypass + best-of-3 try-until-pass. V12 HEBBIAN bypass INC
domain: verification, consciousness, methodology
status: candidate-unverified
source_doc: docs/12_conditions_audit_20260419.md
source_lines: 1-40
promoted_at: 2026-05-11
linked_h: Law 102 (DD122), Hc_948
notes: "원 12조건 → 18 conditions (V1-V18). CLAUDE.md 여전히 '7개' 언급 (drift). config/verification.json SSOT, ready/config mirror desync."
---

## Hypothesis

18 조건 verification (V1-V18, DD122) 의 CE 17/18 PASS rate (216 trials → 176, 81%) 가 외형 통과지만 V8/V9/V10 에 BUG (factory bypass + threshold collapse + best-of-3 try-until-pass) 존재. V12 HEBBIAN bypass 가 2026-04-16 INC. Tier-wise: scale 4, rubber 8, genuine 6.

## Sub-claims (V1-V18 status)

- V1 NO_SYSTEM_PROMPT (scale, NATURAL, PASS): oversells — cell specialization 뿐
- V2 NO_SPEAK_CODE (rubber, NATURAL, PASS): GRU trivially 통과, no adversary
- V3 ZERO_INPUT (scale, NATURAL, PASS): genuine — SOC+Lorenz 유지
- V4 PERSISTENCE (rubber, NATURAL, PASS): 4-way OR no fail path
- V5 SELF_LOOP (genuine, NATURAL, PASS@128c): 32c/64c FAIL, min_cells 16→128
- V6 SPONTANEOUS_SPEECH (rubber, TUNED, PASS): consensus≥200, n_factions=1 kill-switch 없음
- V7 HIVEMIND (genuine, ARTIFICIAL, PASS): 17-config brute-force, CE 측정 누락
- V8 MITOSIS (rubber, NATURAL, PASS, BUG): factory bypass bench.py:3132, ≥1 vs ≥3 desync
- V9 PHI_GROWTH (genuine, PASS, BUG): 임계 1.1→0.85 붕괴, IIT∨proxy OR
- V10 BRAIN_LIKE (scale, NATURAL, 85.6%, BUG): factory bypass + best-of-3
- V11 DIVERSITY (rubber, NATURAL, PASS): uniform-cell kill-switch 없음
- V12 HEBBIAN (INC bypass): 2026-04-16 fix mirror desync
- V13-V18: read source for details

## Migration TODO

- [ ] V8/V9/V10 BUG fix
- [ ] tier reclassify (scale/rubber/genuine 의 정량 criterion)
- [ ] CLAUDE.md "7개" drift 수정 (18 으로 align)
- [ ] config/verification.json SSOT vs ready/config mirror desync 해결
