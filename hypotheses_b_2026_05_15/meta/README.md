# hypotheses_b_2026_05_15 — 옵션 B 격리 (2026-04-30 이후 2주+ cut)

> **목적**: 옵션 B 격리 — 2026-04-30 이후 ~2주 cut 의 H_* 가설. 사용자
> directive 2026-05-15 "all bg go" — V8 GPU + v5-mitosis PyPhi + B 격리 병행.

## 폴더 구조

```
hypotheses_b_2026_05_15/
├── H_promoted/      ← 107 가설 (since: 2026-04 + 2026-05, copy from legacy)
└── meta/            ← 본 README
```

## Scope

- 2026-04: 63 files (since:2026-04)
- 2026-05: 44 files (since:2026-05, 옵션 A 이미 mv 된 10 제외)
- **Total: 107 H_*.md** (옵션 B = "2주 이상 cut" 의 보수적 해석 → 사실상 1.5개월 cut)

## A 와 차이

- A: 10 H_182~H_191 (cycle #7/#8 promoted, 2026-05-12 burst) + 10 Hc_1276~Hc_1285 (cycle #9 draft)
- **B: 107 H_*.md** (2026-04-30 ~ 2026-05-11 span, A 와 *non-overlapping*)
- C: H_178+ (3.5주 cut)
- D: 2026-03+ 전부 (165)

## A 와의 검증 protocol 일관성

VERIFY.tape §6 progress pattern 적용 — A 의 Stage 1+2+3 protocol 동일:
- Stage 1 수학적 (W2 + W5 math): sympy + closed-form
- Stage 2 물리학적 (W5 + W7): PyPhi / Kuramoto / V8 sweep
- Stage 3 cross-meta (W11 + W9): family cohesion + sibling consistency

A verdict aggregate (참고):
- 5 SUPPORTED (25%) — Hc_1282 / Hc_1285 / H_189 / Hc_1279 / Hc_1280
- 10 PARTIAL (50%) — Hc_1281 H_184 H_190 H_188 H_191 Hc_1283 + Hc_1276/77/78/84
- 5 INSUFFICIENT (25%) — V8 family H_182/183/185/186/187

## Honest C3

- since field 가 month 단위 — "정확히 2026-04-30 이후" 매칭 불가, 보수적 해석 (since 2026-04 + 2026-05 합산)
- Hc_*.md 는 since field 없음 — 본 B 폴더 = H_* only. Hc 별도 격리 cycle 필요
- A 와 *non-overlapping* (옵션 A 10 H_182~H_191 제외)
- 본 폴더 = *복제* 만 — 원본 hypotheses_legacy_2026_05_15/ 변경 없음

## Next

VERIFY.tape §6 protocol 적용:
1. Stage 1 수학적 audit (sympy + closed-form, $0)
2. Stage 2 물리학적 audit (PyPhi + Kuramoto + V8, $0 ~ $600)
3. Stage 3 cross-meta (W11 + W9, $0)
