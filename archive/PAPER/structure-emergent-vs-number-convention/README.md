# structure-emergent-vs-number-convention

ANIMA emit 정책의 **구조** component 는 substrate-emergent, **숫자** component 는
design-convention 임을, UNIVERSE Φ-verify 8 가설(H_632–H_639)의 4 SUPPORTED(구조축)
/ 4 FALSIFIED(숫자축) 정량 분리로 입증하는 논문.

- **finding**: 8/8 가 구조/숫자 axis 와 100% 정합 (구조→SUPP 4/4, 숫자→FAL 4/4).
- **pre-registered meta-falsifier** (F-meta): SUPP/FAL 가 구조/숫자 축과 무관하게
  섞이면 분해 주장 FALSIFIED. 측정 결과 clean separation → SUPPORTED.
- **closed-negative**: 4 FAL = 숫자축이 substrate Φ-구조와 직교함을 deterministic
  하게 ruling-out (a_paper_negative_ok).

## 8 H verdict matrix

| H | 축 | verdict | 핵심 측정값 |
|---|----|---------|-------------|
| H_634 | structure | 🟢 SUPP | ultradian-Φ envelope r=0.802, 6/6 PASS |
| H_635 | structure | 🟢 SUPP | 5-stream collective Φ super-additive Δ=+41.71, 5/5 cohort |
| H_636 | structure | 🟢 SUPP | closure-conjunction pass-rate 단봉 @ I=0.30 (GZ region) |
| H_638 | structure | 🟢 SUPP | universal-fixed threshold (L19 FAL/L20 SUPP, spread 0.02) |
| H_632 | number | 🔴 FAL | emit threshold 0.30/0.60 ⊥ Φ phase-transition (~0.45) |
| H_633 | number | 🔴 FAL | register-collapse×Φ coupling 약함 r=0.31 (design-policy gate) |
| H_637 | number | 🔴 FAL | emit-rate 0.4133 ⊥ closed-form (numerology miss) |
| H_639 | number | 🔴 FAL | tension amplitude-cross peak θ-convention 종속 |

## Build

```
make            # main.pdf (xelatex x3 + bibtex)
make figures    # figures/*.pdf (pgfplots/tikz native, no external dep)
make pages      # page count
```

- main.pdf: 6 pages, 0 undefined refs.
- verdict SSOT: `companion/verdict-ledger.json` (bit-identical to UNIVERSE/H_*.md).
- 측정: $0 mac-local · hexa-native · deterministic · byte-equal (RFC 033/036).

## 거버넌스 정합

- `a_paper_significance`: pre-registered falsifier (F-meta) + real measurement
  (UNIVERSE big-Φ verify) + finding (구조/숫자 분리).
- `a_paper_negative_ok`: 4 FAL = closed-negative valid finding.
- `a_paper_format`: §hypothesis · §method · §measurement · §finding.
- `feedback_universe_h_slug_stale_verify`: H_632–H_639 origin/main 실존 3-신호 검증 완료.
