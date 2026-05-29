# AURA A9 — REAL tractography prior (A8.4 문헌 ordinal 대체)

> A8.4는 per-position 결합 prior를 brainwire 문서의 **추정 계수**(DLPFC→VTA 0.75, entorhinal→hippo 0.60, insula→NTS 0.43, M1 0.10)로 뒀고, "subject tractography 아님 · 로컬 DWI/Allen 없음"이라 자인했다.
> A9는 그 자리에 **Allen Mouse Connectivity Atlas의 실측 투사강도**(`api.brain-map.org`, anterograde rAAV tracer, `ProjectionStructureUnionize.normalized_projection_volume`)를 live fetch 해 넣는다.
> 🟢 SUPPORTED-NUMERICAL · verdict `/Users/ghost/core/anima/.verdicts/a9-tractography/run.txt` verbatim (8/8 PASS).

---

## 1. 확보한 실제 데이터 (REAL, Allen Mouse Connectivity)

**소스**: Allen Institute Mouse Connectivity Atlas, `api.brain-map.org/api/v2/data/ProjectionStructureUnionize` — anterograde rAAV-EGFP tracer injection, voxel-level signal을 구조별로 union 한 `normalized_projection_volume` (NPV). 2026-05-30 live fetch.

각 피질 seed의 실제 injection 실험을 조회 → 문서화된 deep hub로의 NPV 추출:

| position | Allen exp (SectionDataSet) | hub target | NPV (실측) |
|---|---|---|---|
| entorhinal (ENTl) | 167212932 | HIP (해마, 관통로) | **0.265** |
| DLPFC (frontal/orbital) | 156741826 | VTA (중피질) | 0.108 |
| M1 (MOp) | 114292355 | VTA | 0.0130 |
| insula (AId) | 267397941 | NTS (자율신경 gateway) | 0.00151 |

> 로컬 검색 0건 — `find /Users/ghost/core -iname '*connectom*'/'*tractograph*'/'*allen*'` 은 RTSC 초전도체 "Allen-Dynes"(무관 물리)만 반환. DATASET/ 도 EEG/TMS/meditation 뿐 DWI/structural 없음. → 네트워크로 Allen API 직접 fetch가 유일한 실측 경로였고 **성공**.

## 2. 실측 가중 → big-Φ (n=4 exact, 무튜닝)

w_i를 NPV 그대로(rescale·tuning 없음) 결합가중으로 써서 big_phi 재계산:

| position | w(real) | big-Φ |
|---|---|---|
| entorhinal | 0.265 | **8.35615** |
| DLPFC | 0.108 | 3.14657 |
| M1 | 0.0130 | 0.367514 |
| insula | 0.00151 | 0.0424667 |

`Δ(entorhinal − insula) = 8.31368` · mixed-position 기판 = 0.773983

## 3. A8.4 순서를 확증? 변경? — **변경 (REVISES)**

| 명제 | 판정 |
|---|---|
| **Ha-REAL** (cluster, 본 주장): strong{ento,DLPFC} **둘 다** > weak{M1,insula} | ✅ **PASS** — dense>weak 클러스터 구조는 **실측에서도 유지** |
| **Hb-CONFIRM** A8.4 top-pair DLPFC ≥ ento | 🔴 **FLIPPED** — 실측은 entorhinal이 최강 (NPV 0.265 ≫ 0.108) |
| **Hb-CONFIRM** A8.4 insula > M1 | 🔴 **FLIPPED** — 실측은 M1 > insula (마우스 insula→NTS NPV 0.0015 ≪ taVNS 추정 0.43) |

| 순서 | A8.4 문헌 ordinal | A9 실측 (Allen) |
|---|---|---|
| | DLPFC > ento > insula > M1 | **entorhinal > DLPFC > M1 > insula** |

- **유지된 것**: "dense projection seed가 weak seed보다 Φ 높다"는 **클러스터 수준 주장**(A8.4 Ha)은 실측으로도 PASS. A7.2의 flat-identity 대비 per-position 차등화가 정당하다는 핵심 결론은 확증.
- **뒤집힌 것 1**: top pair. A8.4는 DLPFC를 최강으로 뒀으나(추정 0.75 vs 0.60), 실측 NPV는 **entorhinal→HIP 관통로가 압도적 최강**(0.265 vs 0.108). brainwire가 entorhinal을 "most direct c→hipp"이라 한 정성 서술과 정합 — 정량으로는 ento가 더 셈.
- **뒤집힌 것 2**: insula가 최약. A8.4의 0.43은 taVNS 효과크기에서 역산한 추정치였는데, 마우스 실측 insula(AId)→NTS는 거의 0(NPV 0.0015). insula는 NTS로의 직접 dense 투사가 약함 → A8.4가 insula 결합을 과대평가했음이 드러남.
- **scale-robust**: NPV를 top=0.75로 max-normalize(실측 비율 보존)해도 ordering 유지(ento 17.91 > DLPFC 9.78 > M1 1.05 > insula 0.12) → 주장은 절대 스케일 선택에 불변, **순서 자체가 결론**.

## 4. honest gap

- **종(species) 불일치**: Allen = **마우스** 실측, AURA 타깃(N1 인간 전극)은 인간. 마우스 cortico-subcortical 투사가 진화적으로 보존되나(ento→hippo, frontal→VTA) **정량은 transfer 비보장** (feedback_toy_scale_transfer 동류). 인간 HCP DWI tractography(예: ENEURO whole-cortex connectome)는 cortico-cortical 중심·deep-hub NPV 표 부재라 이번엔 미확보.
- **proxy 매핑**: "DLPFC"는 마우스에 직접 상동부 없어 frontal/orbital injection(156741826)으로 대리. NPV 절대값은 실험·voxel union 범위 의존.
- **단일 실험 대표값**: 각 pathway top/대표 1 실험 NPV. 다중 실험 평균·분산 미집계(Allen은 ENTl 99·AId 51·MOp 168 실험 보유). ordering robustness는 max-norm으로만 확인.
- **toy 한계**: synthetic TPM · n=4 exact · toy ≠ production 불변.
- **결론**: A8.4 **클러스터 주장은 실측 확증**, 그러나 **구체 4-way 순서는 실측이 DLPFC≈ento>insula>M1 → entorhinal>DLPFC>M1>insula 로 변경**. 정량 결합값이 이제 실측(마우스 NPV)에 grounded — A8.4의 "추정 계수" gap이 (마우스 범위 내) 해소됨. 인간 DWI 정량표는 여전히 미확보.
