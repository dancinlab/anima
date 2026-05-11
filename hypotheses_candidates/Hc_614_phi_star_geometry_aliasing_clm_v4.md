---
id: Hc_614
slug: phi-star-geometry-aliasing-clm-v4-specific
title: 현재 phi-star proxy 가 CLM-v4-architecture-specific (8×192) 이고 cross-substrate phi 값은 aliasing-induced bias 로 비교 불가
domain: clm-architecture
status: candidate-math-verified-falsifier-pending
source_doc: docs/anima_phi_star_proxy_geometry_invariant_spec_2026_05_05.md
source_lines: 26-115
promoted_at: 2026-05-11
linked_h: BG-BN Pythia 70m smoke, BG-M cross-substrate audit
notes: D mod 192 에 따라 tile-replicate / partial-overlap / clean-disjoint 3-mode failure. BG-BN range 0.084 evidence.
verified_at: 2026-05-12
verify_decision: WEAK_MATH_ONLY
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (4+ numeric identities present)"
---

## Hypothesis
phi_star_compute 의 `start = (c * 192) % D` 가 D≠multiple of 192 substrate 에서 tile-replicate aliasing (D=768, cells 0&4, 1&5, 2&6, 3&7 +1.0 forced) 또는 partial-overlap (D=512) 또는 information loss (D=2048, 512 trailing 미사용) 유발. ±5% multiplicative wrap 도 envelope saturation. Cross-substrate phi 비교 의미 없음.

## Falsifiable Tests
- Test 1: D=multiple-of-192 substrate (e.g. D=1536) 에서 aliasing 사라지면 → bias 0
- Test 2: Pythia 70m 16-prompt phi 범위 ≥ 0.5 (현 0.084) → claim 일부 무효
- Test 3: 모든 substrate 에서 mean_pair_cos 분포가 D-independent → architecture claim FALSIFIED

## Migration TODO
- [ ] Option A (rank-invariant D/8 partition) 또는 Option D (PyPhi) 이행
- [ ] CLM v4 re-calibration cycle 포함 (Option A 도입 시)

## Cross-Links
- **sister H**: H_011 (iit-geometry — phi_star proxy substrate-validity), H_022 (consciousness-universe-map — cross-substrate comparability)
- **candidates linked**: Hc_628 (anima Φ★ proxy normalized → IIT 4.0 lower bound — DOWNSTREAM dependency), Hc_624/Hc_623 (Emerge D/E inject), Hc_662 (Mamba 130m phi=42.15), Hc_665 (RWKV 169m phi=42.14)
- **engineering**: phi_star_compute `start = (c * 192) % D` in phi_engine.hexa; BG-BN Pythia 70m smoke
- **literature**: Albantakis 2023 IIT 4.0; PyPhi 1.2+ formal Φ

## Falsifiers (≥5)

- Test 1: D=multiple-of-192 substrate (e.g. D=1536) 에서 aliasing 사라지면 → bias 0
- Test 2: Pythia 70m 16-prompt phi 범위 ≥ 0.5 (현 0.084) → claim 일부 무효
- Test 3: 모든 substrate 에서 mean_pair_cos 분포가 D-independent → architecture claim FALSIFIED
- **F4**: 3-mode failure (tile-replicate / partial-overlap / clean-disjoint) explicit categorization: if 16-prompt sweep on D ∈ {512, 768, 1024, 1536, 2048} produces phi_range that does NOT match the predicted 3-mode mapping → claim's structural model FALSIFIED
- **F5**: PyPhi formal IIT 3.0 on same architectures: if PyPhi Φ rankings reproduce anima phi_star rankings across substrates (Pythia 70m, Mamba 130m, RWKV 169m, CLM v4) → aliasing has not caused cross-substrate bias, anima proxy is valid as-is, Hc_614 claim FALSIFIED

## Honest Limits (≥5)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — phi_star formulation uses 8-cell architecture (Hc_401 atom; sopfr(8)=6 perfect-class diagonal). Aliasing concerns inherit the same perfect-class-trivial substrate; "CLM v4-specific" claim is partly because architecture choice was perfect-class-driven
- **L2**: **BG-BN single-substrate evidence (range 0.084)** — Hc_614 is grounded mostly on Pythia 70m 16-prompt range = 0.084 as evidence of "saturation envelope". One substrate evidence is anecdotal; need ≥3 substrates with range data
- **L3**: **PyPhi (Option D) not yet executed** — gold-standard cross-validation pending. Until PyPhi run completes, claim is "anima-internal proxy may be biased" without orthogonal anchor
- **L4**: **3-mode failure model is theoretical** — tile-replicate / partial-overlap / clean-disjoint is the predicted aliasing taxonomy; not yet empirically validated by sweeping D. Could be reduced to 2-mode or expanded to 5-mode after sweep
- **L5**: **start formula `(c * 192) % D` substrate choice** — uses 192 (=CLM v4 dim/8). For non-CLM-v4 architectures, choice of denominator (8) is arbitrary inheritance. If denominator changes (e.g., dim/16), aliasing pattern changes — claim is partially about the formula, partially about the constant 8
