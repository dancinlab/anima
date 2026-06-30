---
id: Hc_980
slug: alm-r6-closure-fail-progress
title: ALM r6-α attempt_5 FAIL-but-progress — L2 6/6 ✓ + KL 5/6 (p2_p4 잔존). Axis 1 (byte-weighted pool) VALIDATED p3_p4 L2 0.175→0.044. Axis 2 (p2 RoPE Qwen2.5-7B swap) VALIDATED p1_p2 L2 0.152→0.097. Cost $26.61 (5 attempts)
domain: training, alm, closure
status: candidate-unverified
source_doc: docs/alm_r6_closure_20260425.md
source_lines: 1-30
promoted_at: 2026-05-11
linked_h: Hc_957 (ALM sunset)
notes: "r6 = FAIL-but-progress. attempt 1 spendLimit kill 4m27s, attempts 2-4 ABORT (H-DIAG3 + git sync), attempt 5 successful run. r7 candidate p2_p4 KL 0.189 (p95=0.178, 여유 6%)."
---

## Hypothesis

ALM r6-α 5 attempt 누적 결과 attempt_5 (2026-04-25T19:54Z, 4 pods RUNNING+TRAINED, $23.06) 가 Φ 4-path gate FAIL-but-progress: L2 6/6 ✓ 완전 달성, KL 5/6 (p2_p4 잔존 0.189 vs p95 0.178 = 6% over). Axis 1 (byte-weighted pool) prediction VALIDATED — p3_p4 L2 0.175→0.044 (Variant B 재현). Axis 2 (p2 RoPE Qwen2.5-7B swap) VALIDATED — p1_p2 L2 0.152→0.097 돌파. CP1 serve BLOCKED (r7 전제). Total $26.61.

## Sub-claims

- attempt-1: spendLimit async kill 4m27s, $3.55
- attempt-2: ABORT H-DIAG3 same-signal hold
- attempt-3: ABORT bal $105 identical
- attempt-4: ABORT pre-flight 8 NEW (9 commits ahead, git push required)
- attempt-5: 4 pods RUN+TRAIN, FAIL-but-progress, $23.06
- L2-GATE: 6/6 PASS
- KL-GATE: 5/6 PASS (p2_p4 잔존)
- AXIS-1-byte-pool: p3_p4 L2 0.175→0.044 VALIDATED
- AXIS-2-RoPE-Qwen2.5: p1_p2 L2 0.152→0.097 VALIDATED
- r7-CANDIDATE: 독립 제3 축 또는 Gemma 고유성

## Migration TODO

- [ ] r7 design — p2_p4 KL 6% margin 좁히기
- [ ] Gemma 고유성 단축 검증
- [ ] CP1 serve BLOCKED state 명시
- [ ] $26.61 cost ROI 평가
