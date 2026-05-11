---
id: Hc_655
slug: hxc-3wave-d1p2-batch-rollout-cadenced-safe
title: HXC D1 P2 3-wave cadenced rollout (Wave 1 audit-only A4 / Wave 2 A4+A16 entropy / Wave 3 anima state A4+A19 federation) 이 flag-day land 없이 안전 마이그레이션
domain: hxc-deploy
status: candidate-falsifier-only-math-pending
source_doc: docs/hxc_deploy_d1_p2_batch_proposal_20260428.md
source_lines: 14-79
promoted_at: 2026-05-11
linked_h: raw 154 hxc-deploy-rollout-mandate, raw 155 hxc-consumer-adapter-mandate, D1 P1 canary a3ac440a
notes: forward-spec. D1 P2 entry gated on D1 P1 7-day canary clean. 2,405 LoC bracketed ±50%. A4 LIVE / A16-A19 selftest-only.
verified_at: 2026-05-12
verify_decision: WEAK_FALSIFIER_ONLY
verify_note: "verify_hc2 2026-05-12 — F=4"
---

## Hypothesis
3-wave cadenced rollout: Wave 1 (audit-only A4 chain LIVE-verified, +6 LoC, LOW risk) → Wave 2 (audit-only A4+A16 entropy selftest-only, +8 LoC, MEDIUM, subprocess latency variance) → Wave 3 (anima state ledger readers A4+A19 federation, ~435 callsites, ~1,300 LoC, HIGH, F9 federation fix dep). Auto-triggered on D1 P1 success without fresh design cycle (parallel readiness mandate).

## Falsifiable Tests
- F-D1P2-1: Wave 1 canary 7d clean → Wave 2 auto-enter
- F-D1P2-2: A16/A19 LIVE-FIRE 가 selftest-pass 후 entropy-coded real corpora 에서 round-trip 성공
- F-D1P2-3: Wave 3 anima state regression surface (~435 callsites) 측정 가능 incident
- F-D1P2-4: ±50% bracket 가 실제 LoC delta (Wave 3 1,300 LoC 의 variance) 안

## Migration TODO
- [ ] Wave 1 fire: audit_ledger_lint + honesty_triad_lint
- [ ] Wave 2 prereq: A16 entropy encoder LIVE-FIRE real corpora 0/3 → ≥ 2/3
- [ ] Wave 3 prereq: F9 federation fix
- [ ] D2 paired track: nexus/n6/airgenome/hexa-lang cross-repo
