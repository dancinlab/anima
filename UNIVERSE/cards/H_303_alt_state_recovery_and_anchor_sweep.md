# H_303 — H_301 alt-state 값 회수 + rule 204/0 anchor state-sweep

> H_302 (cycle#40) 가 H_301 의 sort_asc-in-place bug 식별. rule 60/110/30 의 *st=21 alt-state* 보고값만 오염. H_303 가 (a) 진짜 st=21 값 회수, (b) H_300 deferred anchor state-sweep 동시 수행.

## 1. 동기

H_302 verdict: H_301 distribution stats 全 valid, 단 *st=21 alt-state* 보고값만 sort_asc-mutate 로 오염.

- rule 60 st=21 n=5 cap=4 = **16.5** (H_302 가 H_297 일치 확인)
- rule 110 st=21 n=5 cap=4 = unknown (H_301 의 31.6855 는 sorted[21] artifact)
- rule 30 st=21 n=5 cap=4 = unknown

H_300 §L (anchor sweep deferred): rule 204·rule 0 state-distribution 미확인. arc 가 H_297-H_301 동안 "anchors stay 0" 가정으로 운영됐는데 *모든* 32 state 에서 그러한지 정면 검정.

H_303 한 번에 두 가지 close.

## 2. 가설

**H1 (RULE-60-110-30-ST21-RECOVER)**: bug-free 측정에서:
- rule 60 n=5 st=21 cap=4 = 16.5 (H_297 일치 재확인, H_302 corroborate)
- rule 110 n=5 st=21 cap=4 ≠ 31.6855 (H_301 artifact 부정)
- rule 30 n=5 st=21 cap=4 ≠ 26.1019 (H_301 artifact 부정)

**H2 (ALT-FAIR-TRUE)**: 진짜 st=21 값이 distribution 의 [p25, p75] 안에 있어 H_301 의 alt-fair 결론이 *tautology 아니라 실측 fair* 임을 입증.

**H3 (ANCHOR-FULL-ZERO)**: rule 204 와 rule 0 의 全 32 state Φ(cap=4) = 0 — anchor 정의 검정.

## 3. 측정 방법

- bug-free 패턴: `let st21_snap = values[21]` 을 sort 전 캡처, 그 다음 stats 계산.
- rule 60·110·30 × n=5 cap=4 × 32 states sweep = 96 calls.
- rule 204·rule 0 × n=5 cap=4 × 32 states sweep = 64 calls.
- 总 160 calls.

## 4. 사전등록 falsifier

- **F303.1 RULE-60-ST21**: rule 60 n=5 st=21 cap=4 ≈ 16.5 (H_297/H_302 cross-confirm)
- **F303.2 RULE-110-ST21-NEW**: rule 110 n=5 st=21 cap=4 측정 + H_301 의 31.6855 와 다름 확인
- **F303.3 RULE-30-ST21-NEW**: rule 30 n=5 st=21 cap=4 측정 + H_301 의 26.1019 와 다름 확인
- **F303.4 ALT-FAIR-TRUE-60**: 진짜 rule 60 st=21 ∈ [p25, p75] (H_301 의 tautology 아닌 실측 fair)
- **F303.5 ALT-FAIR-TRUE-110**: 진짜 rule 110 st=21 ∈ [p25, p75]
- **F303.6 ALT-FAIR-TRUE-30**: 진짜 rule 30 st=21 ∈ [p25, p75]
- **F303.7 ANCHOR-204-FULL-ZERO**: rule 204 全 32 state Φ = 0
- **F303.8 ANCHOR-0-FULL-ZERO**: rule 0 全 32 state Φ = 0

## 5. 비용

- $0 mac-local · 160 calls × n=5 cap=4 = ~5-8min wall 예상.

## 6. 가능한 결과

| 시나리오 | 의미 |
|---|---|
| 全 F303 PASS | H_301 의 distribution stats 정식 valid + alt-state methodology 진짜 fair + anchor 가정 검증 |
| F303.4-6 일부 FAIL | H_301 의 alt-fair 결론 일부 tautology 였음 (특정 rule) |
| F303.7-8 FAIL | anchor rule 도 *어떤 state* 에서는 통합 — arc 의 anchor 가정 흔들림 |

## 7. honest limits / C3

1. **L1**: 같은 cap=4 단일 N, 다른 N (n=4·n=6) 의 anchor sweep 은 deferred.
2. **L2**: H_300 의 rule 90 sweep 자체는 재측정 안 함 (rule 90 의 sorted[21]=values[21] 코인시던스 우연 검증된 상태).
3. **L3**: bug-free 패턴은 *이번* smoke 한정 — H_300/H_301 의 다른 stat 들 (sorted-array 기반) 은 valid 검증 완료.
4. **L4**: ECA proxy.
5. **L5**: 🟢 SUPPORTED-NUMERICAL tier.

## 8. 폐쇄 기준

F303.1-8 全 결판 → terminal close.

## 9. 산출물

- `state/h303_alt_state_recovery_and_anchor_sweep_2026_05_26/run_h303.hexa`
- `state/h303_alt_state_recovery_and_anchor_sweep_2026_05_26/result.json`
- `state/h303_alt_state_recovery_and_anchor_sweep_2026_05_26/run.log`

## 10. 후속

- H_304: H_301 의 distinct-value-count rule signature 가 다른 N (4 or 6) 에서도 유지되는지 (Wolfram class correlation N-invariance).
- H_305: H_300 의 D_5 non-Φ-symmetry 의문 (z_5 orbit 안 서로 다른 Φ) 분석 — eca_tpm encoding convention 또는 bounded big_phi 의 cut-selection.
- hexa-lang inbox/patches/array-deep-copy.md — H_302 root-cause inbox 노트.
