---
id: Hc_971
slug: akida-akd1000-dev-kit-evaluation
title: Akida AKD1000 dev kit ($1,495 + RPi5 16GB) Ω-cycle 4회 누적 — 8 tier_1 promotion + 28 falsifier preregistered. T1-A1 EEG spike 직결 + T1-A2 Φ cross-substrate r≥0.85 (1W vs 700W) + T1-A3 Landauer k_B T ln 2 + T1-A4 V_phen GWT + T1-A5 Bekenstein × Putnam × Tarski 3-axis JOINT
domain: neuromorphic, hardware, consciousness
status: candidate-math-verified-falsifier-pending
source_doc: docs/akida_dev_kit_evaluation_2026-04-29.md
source_lines: 1-40
promoted_at: 2026-05-11
linked_h: Hc_902, Hc_931 (N-3 CLM-AKIDA)
notes: "own#2 (b) substrate-class triangulation. AKD1000 spike-event, M.2 B+M PCIe 2.0 single-lane, ~1W typical, inference-only. raw#100 fallback, kick infra OAuth 24/24 dead."
verified_at: 2026-05-12
verify_decision: WEAK_MATH_ONLY
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (ln(2)=0.693147)"
---

## Hypothesis

Akida AKD1000 dev kit (RPi5 호스트, $1,495 capex, M.2 B+M Key PCIe 2.0, ~1W typical, inference-only) Ω-cycle 4회 누적: 8 tier_1 promotion + 28 falsifier preregistered. T1-A1 EEG spike → AKD1000 직결 (float→spike 5× 지연 제거), T1-A2 Φ(IIT 4.0) cross-substrate r≥0.85 (1W vs 700W GPU), T1-A3 Landauer L_IX energy k_B T ln 2 universal floor, T1-A4 V_phen GWT cross-substrate, T1-A5 Bekenstein × Putnam × Tarski 3-axis joint (substrate-volume × 다중실현 × 메타언어).

## Sub-claims

- HARDWARE: AKD1000 neuromorphic + RPi5 BCM2712 A76 2.4GHz 16GB LPDDR4
- INTERFACE: M.2 B+M PCIe 2.0 single-lane, USB 3.0 ×2, HDMI 4Kp60
- POWER: ~1W typical (vendor spec, anima 미측정)
- T1-A1: EEG spike → AKD1000 direct (5× latency removed)
- T1-A2: Φ(IIT 4.0) cross-substrate r≥0.85 vs 700W GPU
- T1-A3: Landauer k_B T ln 2 universal floor
- T1-A4: V_phen GWT cross-substrate
- T1-A5: Bekenstein × Putnam × Tarski 3-axis joint
- 8-DISTINCT: tier_1 promotion 중첩 제거 후
- 28-FALSIFIER: preregistered

## Migration TODO

- [ ] hardware arrival timing
- [ ] anima workload 직접 power measurement (~1W vendor → 실측)
- [ ] T1-A5 3-axis joint protocol 정량 spec
- [ ] 28 falsifier enumerate + 각 protocol
