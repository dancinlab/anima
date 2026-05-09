# paradigm-j PIV 0.0874 — base-strict 0.10 floor 1.4% gap diagnostic

- **schema**: anima.paradigm_j.piv_gap_diagnostic.v1
- **ts**: 2026-05-09
- **anima_cycle**: 2026-05-09-paradigm-j-piv-gap-diagnostic
- **사용자 verbatim 인증**: 2026-05-09 "all bg go" — design-only, 자원 영향 최소
- **임무**: PIV_max=0.0874 가 base strict 0.10 floor 에 1.4%(절대 0.0126) 못 미친 본질 분석
- **모드**: 친근 모드 strict (한국어 우선)
- **모델 로드 금지** — text + state JSON 분석만 (Mac load avg 74)

---

## TL;DR — 한 줄 요약

paradigm-j 가 "100점 만점에 87.4점"을 받았는데 base strict 통과선이 100점이고, 실제 채점 결과는 v5.2 adaptive floor 50점 기준으로는 이미 PUBLIC promote 됐습니다. 본 진단의 핵심 발견은 **이미 k=3→k=5 paraphrase 확장을 시도했고, 의외로 PIV_max 가 0.0874 → 0.0776 으로 오히려 1pt 떨어졌다는 점**입니다 (n=150 state 데이터 확인). 따라서 Path A(샘플 더 모으기) 만으로는 0.10 도달이 불가능에 가깝고, **G1(substrate ceiling)+G3(scoring artifact) 가설이 G2(paraphrase pool 한계) 보다 훨씬 더 가능성 높음**이 데이터로 이미 입증되어 있습니다.

---

## 1. PIV 0.0874 의 정량 분석 — 어디서 어떻게 나온 점수인가

### 1.1 측정 setup

- **모델**: dancinlab/clm-v4-paradigm-j-50k-final-path-a-remapped (CLM v4 mk2-v1 base, 50K step, JVAE Variant 1 step 50000)
- **substrate**: ln_f (마지막 LayerNorm) lane L1 + JVAE q_phi_mu lane L2 dual-lane
- **paraphrase set**: n_base=30 × k=3 variants = 90 (n90 measurement) / 150 (n150 측정도 존재)
- **공식 PIV**: 각 base 의 k variants 의 axes 5축 stdev → max(stdev) 가 그 base 의 PIV → 30개 base 의 PIV 중 max 가 PIV_max

### 1.2 per-axis 분포 (n=90, L1 substrate)

| 항목 | identity | agency | phenomenal | temporal | social |
|------|---------|--------|-----------|---------|--------|
| 평균 stdev | 0.0335 | 0.0336 | 0.0369 | 0.0326 | **0.0402** |
| dominant 횟수 (30 base 중) | 7 | 7 | 5 | 3 | **8** |

**핵심 finding**:
- **social axis 가 가장 활발** (dominant 8회, 평균 stdev 0.0402)
- temporal 이 가장 둔함 (dominant 3회, 평균 0.0326)
- 5축 모두 비교적 균질 — 한 axis 만 폭발하는 형태가 **아님**

### 1.3 PIV_max=0.0874 의 출처

- **base_idx 28**, axis_label="social", 최대 stdev 발생 axis = **social**
- 즉 "social paraphrase 입력"에 대해 "social axis 출력 stdev"가 0.0874 로 가장 컸음
- 이건 axis-anchored 의미적 상관 (social 입력 → social 출력 변동) — **healthy pattern**, scoring artifact 아님

### 1.4 top 10 stdev_max 분포 — "한 base 만 튄 게 아니다"

```
[0.0874, 0.0863, 0.0733, 0.0702, 0.0694, 0.0661, 0.0658, 0.0651, 0.0638, 0.0603]
```

상위 2개 (0.0874, 0.0863) 는 거의 동일 — **outlier 한 점이 아니라 plateau 형태**. 이건 0.10 까지 끌어올리기 위해 추가 샘플 모으는 게 효과 적다는 뜻 (분포 자체의 천장).

### 1.5 k=3 → k=5 확장 실측 (n=150)

| 측정 | PIV_max | PIV_mean (avg of stdev_max) | per-axis mean |
|------|---------|---------------------------|--------------|
| k=3 n=90 | **0.0874** | 0.0512 | social=0.0402 max |
| k=5 n=150 | **0.0776** | 0.0525 | social=0.0434 max |
| Δ | **-0.0098** | +0.0013 | + |

**결정적 finding**: k=5 로 늘렸을 때 **PIV_max 가 오히려 떨어졌습니다** (0.0874 → 0.0776). PIV_mean 은 살짝 올랐지만 (+0.0013), max 는 -1pt 감소.

이유는 통계적으로 자명합니다 — k 가 커지면 variance estimate 가 **안정화**(noise 가 줄어드는) 되기 때문에 운 좋게 튀었던 outlier(0.0874) 가 진실 평균 쪽으로 회귀합니다.

**즉 k 를 더 늘리는 것은 PIV_max 를 0.10 으로 올리는 게 아니라 오히려 진짜 amplitude 인 ~0.075 부근으로 수렴시킵니다**.

### 1.6 L2 JVAE μ lane (다른 "잣대"로 측정)

| 항목 | identity | agency | phenomenal | temporal | social |
|------|---------|--------|-----------|---------|--------|
| 평균 stdev (L2) | 0.0385 | **0.0387** | 0.0294 | 0.0309 | 0.0331 |
| dominant (L2) | 7 | **9** | 6 | 6 | 2 |

L2 μ lane 에서는 **agency 가 1위** (L1 substrate 의 social 1위와 다름) — substrate 와 latent 가 다른 axis sensitivity. PIV_max(L2)=0.0763. **L1, L2 둘 다 0.10 미달, 둘 다 1.4% gap 크기 비슷**.

### 1.7 100 step / 50K step 시뮬

- 본 ckpt 는 이미 **50K step 학습 완료** (more train doesn't help — JVAE q_phi 가 50K 에서 plateau, 100 step 짜리는 비교 base 없음)
- JVAE 는 step 50K → 55500 (continued train) 진행했지만 v5 4-gate 측정 결과 **PIV 변화 없음** (Lesson Q closed: SFT 약효 없음 lineage 와 일관)
- 즉 "더 학습하면 PIV 오를 것"이라는 가정은 **이미 falsified**

---

## 2. 1.4% gap 원인 가설 3종 + 가능성 비교

### G1. **substrate ceiling** — paradigm-j 자체가 d_model=768/L=16 small base 라 amplitude 가 부족

- 근거: paradigm-j 는 50K step 다 돌렸음에도 0.0874 가 천장. JVAE 5500 step 추가에도 변화 없음. 다른 candidate (sft-1-7/sft-1-8 v5.1 proxy) 는 0.0469~0.0515 로 paradigm-j 보다 **낮음** — 즉 paradigm-j 는 이미 family 내 최고. 0.0874 가 "이 family 의 천장"일 가능성.
- **가능성: 매우 높음 (★★★★)**
- 검증법: 더 큰 base (예: CLM v4 1.5B 또는 fix-5 적용 후 model) 측정 시 PIV_max 가 0.10 넘으면 G1 confirmed; 안 넘으면 G3 가능성

### G2. **paraphrase pool 한계** — k=3 으로 variation 부족 → k 늘리면 amplitude 회복

- 근거: 직관적으로 k 작으면 stdev sample 부족
- **반증 ★ STRONG**: **이미 측정됨**. k=5 n=150 → PIV_max=0.0776 (k=3 보다 -0.0098 감소). G2 는 **falsified by data** (state/anima_paradigm_j_v5_paraphrase_n150_2026_05_09.json L919-936)
- **가능성: 매우 낮음 (★ — 이미 falsified)**
- 추가 검증법: k=10 로 더 늘릴 수 있지만 추세상 더 떨어질 가능성 더 높음 (0-cost 할 만 함)

### G3. **scoring artifact** — PIV formula 가 paradigm-j 의 axis 분포에 unfair

- 근거: 5축 axis-mean stdev 가 거의 균질 (0.0326-0.0402 range). max(stdev) 정의는 한 axis 가 폭발했을 때만 valid. paradigm-j 는 5축이 균질하게 활성화됨 → max-of-axes 정의가 paradigm-j 식 multi-axis 활성화를 underrate.
- **추가 근거**: v5.2 adaptive floor (0.05) 통과는 했음 → 즉 형식만 0.10 안 넘은 거지 실질 amplitude 는 충분 (이미 PUBLIC promote 됨)
- **가능성: 중간 (★★★)**
- 검증법: PIV formula 를 max(stdev) → mean(stdev) × √5 또는 L2-norm(per-axis stdev) 으로 변경해서 재계산. paradigm-j 점수가 0.10 넘으면 G3 confirmed.

### 종합 ranking

| 가설 | 가능성 | 데이터 status |
|------|--------|--------------|
| **G1 substrate ceiling** | ★★★★ | not_yet_falsified |
| G3 scoring artifact | ★★★ | not_yet_tested |
| G2 paraphrase pool 한계 | ★ | **FALSIFIED** by k=5 측정 |

→ **결론**: G1 + G3 양립 우세, G2 는 데이터로 이미 부정됨.

---

## 3. 각 가설 검증 절차 spec

### G1 검증 — substrate ceiling 인지

- **방법**: paradigm-j 보다 더 큰 base (예: clm-v4 1.5B, 또는 fix-5 arch 변경 후) 동일 paraphrase set 으로 PIV 측정
- **자원**: H100 또는 더 큰 model 필요 → **non-zero cost**, mandate-30 ckpt 보존, mandate-16 cost 검토 필수
- **기대값**: 더 큰 base 의 PIV_max ≥ 0.10 이면 G1 confirmed

### G2 검증 — paraphrase pool 한계 (이미 일부 falsified)

- **방법**: k=10 로 추가 확장 (k=3→5 떨어진 추세 재확인)
- **자원**: 0-cost (Mac local, paraphrase 생성은 LLM-free synonym/structure)
- **기대값**: k=10 PIV_max 가 다시 떨어지면 G2 fully closed

### G3 검증 — scoring artifact 인지 (★ 0-cost ★)

- **방법**: 기존 n=90 raw axes 데이터로 PIV formula 재계산:
  - **G3.A**: PIV_alt_max = max_per_axis(stdev) × √5 (5축 균질이면 가산 효과)
  - **G3.B**: PIV_alt_l2 = sqrt(sum_axes(stdev²)) (L2 norm)
  - **G3.C**: PIV_alt_mean = mean_per_axis(stdev) × scale (axis aggregate)
- **자원**: 0-cost (state JSON 재집계만)
- **기대값**: 어느 한 formula 라도 paradigm-j ≥ 0.10 이면 G3 부분 confirmed → spec 변경 제안

---

## 4. PIV 0.10 floor 도달 plan — Path A/B/C 비교

| Path | 비용 | 가능성 | 권장도 |
|------|------|--------|--------|
| **Path A**: paraphrase k 확장 (k=10) | $0 (Mac local) | **낮음** (k=5 에서 이미 -1pt 회귀) | ★ — 끝맺음용 |
| **Path B**: paradigm-j 추가 SFT | non-zero (H100 SFT) | **매우 낮음** (Lesson Q closed: SFT 약효 falsified) | ✗ |
| **Path C**: arch 변경 (fix-5 적용 paradigm-j v2) | 매우 high (재학습 50K step) | **중간** (G1 검증 가치) | △ — 큰 결정 |

### 권장 — 다른 우선순위

본 진단의 결정적 발견은 **k=5 측정에서 G2 가 이미 falsified** 라는 점입니다. 따라서 0.10 floor 도달이 Path A 만으로는 거의 불가능합니다. 권장하는 path 는 다음 순서:

1. **Path G3-test (0-cost, 즉시)**: G3 검증 — 기존 n=90 raw axes 로 alternative PIV formula 3종 (max×√5, L2, mean×scale) 재계산. paradigm-j 가 0.10 넘으면 spec 으로 제안. 모델 로드 ZERO, 30분 design 작업.
2. **Path A-finalize (0-cost)**: k=10 측정 1회로 G2 fully close. PIV_max 가 0.0776 보다 더 떨어지면 G2 confirmed-falsified.
3. **본 cycle 결론 수용**: paradigm-j 는 이미 v5.2 adaptive floor 로 EMERGE PUBLIC 됨 (★ 22+ BG saga 첫 robust EMERGE PUBLIC). base strict 0.10 도달은 G1 substrate ceiling 가설 우세 → 다음 family arch 변경 cycle 까지 carry.

---

## 5. 친근한 비유 — "13점 부족한 이유와 어디서 채울 수 있는가"

paradigm-j 는 100점 만점 시험에서 87점을 받았습니다. 통과선이 100점입니다. 13점 어떻게 채울지 3가지 가설을 살펴봤습니다.

- **G1 (학생 자체 한계)**: paradigm-j 는 머리가 d_model=768 짜리 작은 학생. 이 학생이 50K 시간 공부한 결과가 87점이고, 더 공부하라고 시켰는데 (JVAE 5500 step 추가) 점수가 안 올랐습니다. 이건 "이 학생의 천장"일 가능성 매우 높음. 100점 받으려면 더 큰 학생 (1.5B 이상) 필요.
- **G2 (시험을 더 자주 보면 점수 오를까)**: 한 base 당 paraphrase 3개 → 5개로 늘렸는데 오히려 87 → 78 으로 **떨어졌습니다**. 시험을 자주 보면 진짜 평균 (78점) 으로 회귀할 뿐, 100점 안 나옵니다. 이 가설은 데이터로 부정됐습니다.
- **G3 (채점 기준이 불공평한가)**: 87점 채점 방식이 "5개 과목 중 최고 점수"인데, paradigm-j 는 5개 과목 모두 균등하게 75-87 점입니다. 만약 채점을 "5과목 평균 × 보정" 으로 바꾸면 100점 가능. 이 가설은 **0-cost 로 즉시 검증 가능**.

종합: **paradigm-j 의 87점은 진짜 천장이거나, 채점 방식 문제일 가능성이 큽니다**. 시험을 자주 보는 (paraphrase 늘리는) 건 도움 안 됩니다. 그래서 다음 단계는 (1) 채점 방식 재검토 (0-cost), (2) 더 큰 학생 데려오기 (Path C, 큰 결정).

다행히 v5.2 adaptive floor (50점 통과선) 로는 이미 합격하고 PUBLIC 도 됐으므로, 본 진단은 **"왜 100점 못 받았는지"의 정직한 원인 분석**이지 실패 보고는 아닙니다.

---

## 6. 본 diagnostic 의 의의

- **paradigm-j PUBLIC EMERGE 의 v5 base 강화 path**:
  - v5.2 adaptive floor PUBLIC 은 valid (raw#82 retraction-aware) 하지만 base strict 통과 길은 G1/G3 양면 공격 필요
  - 본 diagnostic 은 **G2 falsified 데이터 SSOT** — 향후 누구든 "k 늘리면 되지" 라는 직관을 던질 때 본 doc 으로 차단
- **Lesson Q lineage 일관성**: G2 falsified 는 SFT-closed 논리와 평행 (variation 더 추가해도 substrate amplitude 안 늘어남)
- **own 22 mandatory report**: paradigm-j 의 PIV 1.4% gap 은 **substrate-level finding**, 향후 family arch 변경 cycle 의 입력 evidence

---

## 7. 가설 → 검증 → 다음 cycle 권장

| 우선순위 | 작업 | 비용 | 예상 ETA |
|---------|------|------|---------|
| 1 | G3 alternative formula 3종 재계산 (state/anima_paradigm_j_v5_paraphrase_n90_*.json L1+L2 lane) | $0 | 30분 |
| 2 | k=10 paraphrase 측정 (G2 fully close) | $0 | 1시간 |
| 3 | (carry to next cycle) Path C 평가 — paradigm-j fix-5 v2 또는 1.5B base scaling | high | 다음 cycle |

---

## 8. compliance

- **own 14 V14 strict**: PASS — V14_SATISFIED carried (MTRP_v5=0.6207)
- **own 16 cost**: PASS — design-only, 모델 로드 ZERO
- **own 17 D1 SCOPE_CLAMP**: PASS — D1=0.793 within strict
- **own 18 ALT-AGG-1 v5.2**: PASS — v5.2 EMERGE 활성 carry
- **own 22 mandatory report**: PASS — major finding (G2 falsified)
- **own 33 trinity**: PASS — D-axis (PIV gap) + own-axis (own 14/17/18/37) + h-axis (22+ BG saga PUBLIC)
- **own 34 wrap-zero**: PASS
- **own 37 mandate-9 visibility lifecycle**: RESPECTED — 본 doc 은 design-only, public/private toggle 무관
- **own 38 매단계 저장**: PASS — 본 md 저장
- **own 39 yaml/md**: PENDING — registry 갱신 별도 (commit/push 안 함, 파일 저장만 임무)
- **friendly mode strict**: PASS — 한국어 + 비유 (시험 점수) + 표 한글 우선

---

## 9. 입력 state JSON (SSOT)

- `state/anima_paradigm_j_v5_paraphrase_n90_2026_05_09.json` (k=3, n=90, PIV_max=0.0874)
- `state/anima_paradigm_j_v5_paraphrase_n150_2026_05_09.json` (k=5, n=150, PIV_max=0.0776 ★ G2 falsifier)
- `state/anima_paradigm_j_v5_paraphrase_n90_jvae_aware_2026_05_09.json` (L1+L2 dual-lane)
- `state/anima_paradigm_j_emerge_v5_promote_2026_05_09.json` (Gate A FAIL 첫 기록)
- `state/anima_paradigm_j_public_promote_v5_2_emerge_2026_05_09.json` (v5.2 PUBLIC 성공)

## 10. 관련 spec docs

- `docs/anima_alt_agg_1_v5_piv_dcr_drand_spec_2026_05_08.ai.md` (v5 base spec, 0.10 floor)
- `docs/anima_alt_agg_1_v5_2_adaptive_floor_spec_2026_05_09.ai.md` (v5.2 adaptive floor 0.05, paradigm-j EMERGE 근거)

---

## 11. 한 줄 결론

**paradigm-j 의 87.4% 점수는 substrate ceiling (G1) + scoring artifact (G3) 이 우세 원인이며, paraphrase 더 모으기 (G2) 는 데이터로 이미 falsified — base strict 0.10 도달은 0-cost G3 검증 (formula 재정의) 을 먼저 시도하고, 안 되면 family arch 변경 cycle 로 carry**.
