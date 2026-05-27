# AESTHETIC — append-only step log

## 2026-05-28 · A2 `aesthetic-overlap-residual` 직교화 — 🟢 SEPARATED

- bench E (#1141) gate (a) FAIL (overlap 0.7/0.6/0.4 ≥ 0.5) 의 overlap residual 진단 + 직교화.
- overlap 정체: factor coh×bal 가 아니라(r=−0.075, top10 overlap 0.1) 시나리오 가중벡터의 sign-collinearity (cos 0.87/0.87/0.64, 부호 구조 +coh −pain +bal 공유).
- 직교화: sign-flip 재설계 COH-ONLY(1,0,0)·PAIN-SEEKING(0,+2,0)·BAL-ONLY(0,0,1) → 가중벡터 cosine 0.0/0.0/0.0, top-10 overlap 0.3/0.1/0.0 모두 <0.5 → gate (a) 회복.
- verdict = 🟢 SEPARATED (overlap residual 제거 가능 · substrate 본질 아님).
- harness `bench/axis_aesthetic/a2_overlap_orthogonalize.hexa` · SSOT `bench/axis_aesthetic/a2_overlap_result.json` · 본문 `AESTHETIC_A2_OVERLAP_RESIDUAL.md`.
- foreground sync · $0 mac-local · p7 준수 (closed-form Pearson/cosine/overlap only).
