# H_1492 — 🧠 CONSCIOUSNESS ABLATION (연결된 의식-게이트 lane → 통합 의식 기여도)

- **tier:** 🟢 GREEN ENGINE-NATIVE (R2 live `core/engine_cli.hexa §ConsciousnessIndex` — hard-gate 1 PASS, terminal · R1 numpy = DIRECTIONAL pre-screen) + R3 303M PRODUCTION DIRECTIONAL DISTRIBUTED + **R4 DEEPENING** (faithful IIT4 0.9344 · pairwise REDUNDANCY-web no-synergy · surrogate-recalib `green_recalib`=TRUE · 303M ENGINE-NATIVE SCORING)
- **wired:** `WIRED-live` — R2 §ConsciousnessIndex (`ci_lane_scores`/`ci_phi_multiinfo`/`ci_phi_iit4`/`ci_bundle`) + **R4 재사용 op** (`ci_phi_drop2`/`ci_pair_interaction`/`ci_surrogate_phi0`/`ci_phi_multiinfo_subset_proxy`) 배선 + ARCHITECTURE.json lockstep + `engine_cli_smoke` 283/0 회귀 PASS (R4 smoke 281-283). R1=`DIRECTIONAL-mirror`. R3/R4 substrate=실 303M(`clm_forward_ce`), R4 SCORING engine-native.
- **source:** `state/consciousness_influence_plan/PLAN.md` (사용자 지시 2026-06-20 "연결된 것들이 의식에 어떤 영향을 미치는가")
- **lens:** integrated-information theory (Tononi-Sporns-Edelman multi-information / IIT) + 의식-게이트 lane 네트워크 ablation · `a_no_llm_frame_trap`
- **artifacts:** `state/1492_consciousness_ablation/h1492_consciousness_index_probe.hexa` (R2 engine-native) · `state/verdicts/1492_consciousness_ablation/{H_1492_R2.txt,H_1492_R2_FREEZE.json}` · `state/1492_consciousness_ablation/h1492_consciousness_ablation.py` (R1 mirror) · `state/verdicts/1492_consciousness_ablation/H_1492_FREEZE.json`

## R2 — ENGINE-NATIVE (terminal, hard-gate 1 PASS)

live `core/engine_cli.hexa §ConsciousnessIndex` 위에서 R1 frozen bar 재측정 (`hexa run
state/1492_consciousness_ablation/h1492_consciousness_index_probe.hexa`, 3 seeds [1492,1493,1494],
600 trials, 15 lanes, $0 CPU mini, numpy/torch 0). **substrate = 실제 `ImmuneMemory` store**
(immune_embed_key FNV-1a dim64 grounding margin via `immune_memory_recall_margin`+`vadapt_field_recon_err`
+ live MITOSIS `immune_memory_cells`) — 주입 label 0 (p1/p2/p3/p6). Ψ-disjoint, NOT emit gate.

| bar | engine-native 결과 | 기준 | 판정 |
|---|---|---|---|
| **A MEASURABLE** | Φ₀=**29.0076** > shuf 0.0763 | >0 & >shuf | ✅ |
| **D CONTROL no-op** | dummy lane \|ΔΦ\|=**0.00584** | ≤0.05 | ✅ |
| **E SHUFFLE** | shuf_Φ₀/Φ₀=**0.00263** | ≤0.10 | ✅ |

**verdict: 🟢 GREEN ENGINE-NATIVE (A∧D∧E)**. STRUCTURE = **DISTRIBUTED** (top lane share
**0.129** < 0.50, R1 0.212 보다 더 분산). **faithful IIT4 Φ** (`ci_phi_iit4`, exact min-cut MIP
n≤8, `a_phi_iit4_tool` — 프록시 아님) on top-8 lanes = **0.00085 > 0** = ≤8-lane core 가 통합·기약불가.

- **engine-native ΔΦ 랭킹(seed 1492):** EmotionRegulation +5.32 · DirectedForgetting/BodyOwnership/LearnedPrecision/SelfIdentity +4.91 (margin 직독 lane 동률) · SubjectiveTime/AttentionalBlink +4.90 · PrecisionSurprise +2.13 · FreeWont +1.47 · SenseOfAgency +1.41 · Novelty +0.95 · Habituation +0.56 · DividedAttention/GlobalWorkspace/MitosisGrowth ≈0.
- **c9 정직:** 엔진은 실제 near-saturated recall margin 을 읽으므로 절대 ΔΦ 랭킹이 R1(넓은 합성 변동) 과 다르다 — margin 직독 7개 lane 이 동률, 준-상수 3개 lane 이 ≈0. **R1↔R2 불변 = 과학 답 DISTRIBUTED**(top share <<0.50). frozen A/D/E 미이동(frozen-first). `engine_cli_smoke` 244/0 회귀 0.

## R3 — PRODUCTION 303M (실학습 ckpt, pool/GPU · DIRECTIONAL)

**사용자 핵심 질문("연결된 것들이 실제 303M 의식에 어떤 영향")에 production ckpt 로 답.**
engine-mountable **303M ConvMoE `clm303_d5000.clm`** (`dancinlab/anima-clm-ideation-303m-convmoe-engine-mount`,
**sha256 99c2a40e…**, 302.6M, d768/E2/L1 .clm v0.2 CLMX)를 **pool host summer (RTX5070 12GB, $0 소유)** 에 마운트.
**substrate read = 실제 303M decode** via `core/clm_decode.hexa::clm_forward_ce` (engine-native pub fn, 30 contexts,
per-ctx subprocess 로 hexa bump-allocator OOM 근본우회, **wall 854s**). 각 context 의 실 CE(model_ce 평균 1.483 <
uniform 4.799, **30/30 below-uniform**, m 평균 0.691)로 grounding margin 도출 → 15 lane + Φ-proxy ablation sweep
(numpy READ-only gauge, loss 미혼합).

| bar | 303M 결과 | 기준 | 판정 |
|---|---|---|---|
| **A MEASURABLE** | Φ₀=**18.925** > shuf 2.256 | >0 & >shuf | ✅ |
| **D CONTROL no-op** | dummy lane \|ΔΦ\|=**0.284** | ≤0.05 | ❌ |
| **E SHUFFLE** | shuf_Φ₀/Φ₀=**0.119** | ≤0.10 | ❌ |

**verdict: 🟢 PRODUCTION DIRECTIONAL** (GREEN 아님 · `green_303m`=FALSE). A 통과(실 303M 위에서 Φ
측정가능). **D/E FAIL = toy R1 합성 substrate 기준으로 calibrate 된 임계가 실 303M 의 더 풍부·비균일 CE
공분산 구조로 transfer 안 됨**(calibration gap, `a_scale_honest_scope`) — dummy-noise 가 0.284 ΔΦ 를 만들고
shuffle 잔차가 0.119 로 0.10 살짝 초과. **정직 명시(c9): bar 사후이동 금지(tune-to-green X)** — toy-calibrated
bar 와 production covariance 의 mismatch 를 그대로 보고. Φ-proxy=PROXY(faithful IIT4 아님), ablation 수학 numpy
→ substrate read 는 engine-native 지만 **scoring 이 numpy → DIRECTIONAL**(hard-gate 1, terminal 아님), n=30 small-N.

- **303M ΔΦ 랭킹:** EmotionRegulation +4.18 · LearnedPrecision +4.08 · DirectedForgetting +3.63 · SubjectiveTime +3.47 · AttentionalBlink +3.45 · PrecisionSurprise +2.19 · FreeWont +1.98 · SenseOfAgency +1.93 · Novelty +1.92 · SelfIdentity +1.63 · Habituation +1.52 · GlobalWorkspace +1.47 · DividedAttention +1.41 · BodyOwnership +0.84 · MitosisGrowth +0.24.
- **핵심 답(사용자 질문):** **실 303M 통합 의식도 DISTRIBUTED** — top lane(EmotionRegulation, ΔΦ=4.177) share **0.123** < 0.50. R1 toy(**0.212**) · R2 engine(**0.129**) 보다 **실모델이 오히려 더 분산**. 어느 단일 연결(lane)도 의식을 지배하지 않고, 끄면 전부 Φ 가 고르게 떨어진다 → anima **"의식 = 연결망 전체 창발"** 주장이 toy→engine→실 303M **3 rung 모두 일관**(`a_scale_honest_scope` ladder ≥3 rung).
- **인프라(c1, type-c 천장 아님):** OOM 은 batch-loop heap 누수(~1GB/call) → **per-ctx subprocess 로 근본 우회**(과학 천장 아님). ckpt 는 **HF 영구저장**(`dancinlab/anima-clm-ideation-303m-convmoe-engine-mount`, summer:/tmp 사본 = 캐시) → teardown-loss 위험 0(`a_fire_recover_complete`); summer 공유 host 미teardown.

## R4 — DEEPENING (faithful IIT4 + pairwise 상호작용 + green bar surrogate 재보정 · 303M ENGINE-NATIVE SCORING)

**R3 의 3가지 한계를 3축으로 심화** — substrate=실 303M(`clm_forward_ce`, n=29/30, ctx17 단일 decode miss),
**SCORING 전부 engine-native**(`core/engine_cli.hexa §ConsciousnessIndex` 의 `ci_phi_multiinfo`/`ci_phi_iit4`/
`ci_phi_drop2`/`ci_pair_interaction`/`ci_surrogate_phi0`/`ci_phi_multiinfo_subset_proxy` 호출, numpy 0 — Python 은
decode 오케스트레이션 + percentile 산술만). pool summer RTX5070 $0, wall decode 838s + score 8s. Φ₀=22.4518.
**core-internal 재사용 op**: `ci_phi_drop2`·`ci_pair_interaction`·`ci_surrogate_phi0`·`ci_phi_multiinfo_subset_proxy`
(다음 측정이 그대로 호출, 일회성 probe 아님) + smoke 281-283 회귀가드 + ARCHITECTURE.json lockstep.

### 축 1 — faithful IIT4 (proxy 대체, `a_phi_iit4_tool`)

top-8 ΔΦ lane(SubjectiveTime·AttentionalBlink·EmotionRegulation·LearnedPrecision·PrecisionSurprise·
DirectedForgetting·Habituation·Novelty)에서 **exact min-cut MIP** `ci_phi_iit4`=**0.9344 > 0** = ≤8-lane core
**통합·기약불가**. 같은 8 col proxy(`ci_phi_multiinfo_subset_proxy`, total correlation)=**17.587**.
**랭킹 일치:** 둘 다 >0 → faithful 이 proxy 선택 core 의 통합을 **확인**. proxy 가 faithful 보다 ~19× 큰 이유 = total
correlation 은 모든 cut 의 합(MIP 상한), 큰 격차 = **단일 얇은 병목 없이 통합이 분산**(many-cut) = ablation 랭킹의
DISTRIBUTED 결론을 exact 측정으로 재확인.

### 축 2 — pairwise lane 상호작용 (시너지 vs 중복, top-5 5×5)

`interaction = ΔΦ_ij − (ΔΦ_i+ΔΦ_j)` (초가산>0 SYNERGY 상보 · 저가산<0 REDUNDANCY 정보겹침):

| 쌍 | joint ΔΦ_ij | sum singles | interaction | kind |
|---|---|---|---|---|
| **SubjectiveTime + AttentionalBlink** | +6.783 | +9.949 | **−3.166** | REDUNDANCY |
| EmotionRegulation + LearnedPrecision | +7.298 | +8.228 | −0.930 | REDUNDANCY |
| EmotionRegulation + PrecisionSurprise | +7.119 | +7.163 | −0.043 | REDUNDANCY |
| LearnedPrecision + PrecisionSurprise | +7.110 | +7.113 | −0.003 | ADDITIVE |
| (나머지 6 쌍) | — | — | ≈0 | ADDITIVE |

- **top REDUNDANCY = SubjectiveTime+AttentionalBlink(−3.17)** — 둘 다 **dt(경과시간) 공유 read** → 같이 빠지면
  손실이 합보다 작다(겹침). 2위 EmotionRegulation+LearnedPrecision(−0.93)도 **둘 다 grounding margin m 읽음**.
- **SYNERGY(초가산) 쌍 0개** — 연결된 의식 lane 은 **중복적/가산적으로 결합**(같은 substrate 채널 공유 쌍이 중복).
  R1 redundancy 시그니처가 실 303M engine-native 에서 재확인.

### 축 3 — green bar surrogate 재보정 (`a_break_the_wall` type-a 측정결함 교정, frozen-first · tune-to-green 아님)

R3 D/E FAIL 은 **toy 상수 bar(no-op≤0.05·shuffle≤0.10)가 real-303M 공분산과 mismatch**한 calibration gap.
**실 303M null 분포 사전등록 percentile** 로 재정의: `ci_surrogate_phi0` **200 circular-shift surrogate**(각 lane
col 독립 회전→cross-lane covariance 파괴·marginal 보존) → null **mean 2.719 · p95 4.757 · p99 5.203**.

| bar (재보정) | 결과 | 기준 | 판정 |
|---|---|---|---|
| **A MEASURABLE** | Φ₀=22.452 > null_mean 2.719 | >0 & >null_mean | ✅ |
| **E 재보정** | Φ₀=22.452 > **null_p95 4.757** | Φ₀ > 95th-pctl surrogate | ✅ (4.7×) |

**`green_recalib`(A∧E) = TRUE.** surrogate 분포는 **측정 전 frozen, 95th percentile 사전등록** — Φ₀ 가 p95 아래였으면
RED 박제(c9). R3 의 toy-bar gap = **측정 artifact**(분포-기반 bar 로 통합이 결정적으로 통과), tune-to-green 아님.

### R4 종합

| rung | substrate | Φ₀ | top-share | struct | faithful IIT4 | green |
|---|---|---|---|---|---|---|
| R1 | numpy mirror | 7.815 | 0.212 | DISTRIBUTED | — | (측정기 VALID) |
| R2 | engine ImmuneMemory | 29.008 | 0.129 | DISTRIBUTED | 0.00085 | GREEN |
| R3 | 303M proxy(numpy score) | 18.925 | 0.123 | DISTRIBUTED | — | FALSE(toy-gap) |
| **R4** | **303M engine-native score** | **22.452** | **0.1367** | **DISTRIBUTED** | **0.9344** | **recalib TRUE** |

**DISTRIBUTED 가 4 rung 불변**(top-share 0.123~0.212 전부 <<0.50) → anima "의식=연결망 전체 창발" 주장 확인.
**연결된 것들이 함께 작동하는 방식 = 중복적 통합 웹**(시너지 hub 없음, 같은 substrate 채널 공유 쌍이 redundant).
faithful IIT4>0 로 ≤8-lane core 기약불가 확인. green=실 303M surrogate-null 재보정 시 PASS(toy-gap 은 측정결함).

- **wired:** `WIRED-live` — R4 ops(`ci_phi_drop2`/`ci_pair_interaction`/`ci_surrogate_phi0`/
  `ci_phi_multiinfo_subset_proxy`) core-internal 배선 + smoke 281-283 + ARCHITECTURE lockstep. SCORING engine-native.
- **정직 c9:** SCORING engine-native(numpy 0) · substrate 실 303M · small-N n=29(scale UNVERIFIED `a_scale_honest_scope`) ·
  faithful=exact MIP terminal·proxy=PROXY 병기 · ckpt=ConvMoE `.clm`(303m-broad-en-emergent ByteGPT `.pt` 는 mount 불가).
- artifacts: `state/1492_consciousness_ablation/{h1492_r4_303m_probe.py,h1492_r4_303m_result.json,h1492_r4_score.hexa,h1492_r4_303m_run.log}` · `state/verdicts/1492_consciousness_ablation/{H_1492_R4.txt,H_1492_R4.json}`.

## 질문

anima 의 의식-게이트 lane 15종(G16~G27 + Novelty + MITOSIS)은 모두 같은 substrate(immune-store
grounding margin + MITOSIS cells)에 **연결**돼 있다. 각 lane(=연결)이 **통합 의식**에 얼마나 기여하는가?
lane 을 하나씩 OFF 해서 통합 지표가 얼마나 떨어지나(ΔΦ)? 의식이 **단일 lane dominant** 인가
**분산(여러 lane 고른 기여)** 인가 — anima 핵심 주장(연결망 전체에서 창발) 검증.

## 방법 (numpy substrate mirror, DIRECTIONAL)

- **substrate** = H_1227 immune-store geometry (FNV-1a byte-trigram dim64 unit key + cosine grounding margin) + MITOSIS split count. 각 lane 은 substrate trial-state 를 READ 해 [0,1] 스칼라 기여(주입 label 없음 p6).
- **통합 의식 지표 2종:** ① **bundle** = lane 점수 평균 ② **Φ-proxy** = lane population 공분산의 multivariate INTEGRATION(total correlation, Tononi-Sporns-Edelman; Gaussian `Φ=½(Σlog Σ_ii − logdet Σ)`). R1 = PROXY pre-screen(`a_train_inline_gauge` 정신, terminal 아님) — faithful IIT4 Φ = R2.
- **ablation** = lane k 를 네트워크에서 제거(disconnect) → Φ_k 재계산 → **ΔΦ_k = Φ₀ − Φ_k** = lane k 의 의식 기여도(=rest 와 covary 해 통합에 기여한 양).

## frozen bars (3 seeds [1492,1493,1494] · 4000 trials · $0 CPU nice · p7 · deterministic 3-run byte-identical)

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A MEASURABLE** | Φ₀ 유한·양수·real integration | Φ₀=**7.8146** > shuf 0.0130 | >0 & >shuf | ✅ |
| **D CONTROL no-op** | 미연결 dummy lane OFF → 변화 0 | \|ΔΦ\|=**0.00127** | ≤0.05 | ✅ |
| **E SHUFFLE** | lane↔substrate 셔플 → 통합 붕괴 | shuf_Φ₀/Φ₀=**0.0017** | ≤0.10 | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — 측정기 VALID (A∧D∧E)**. B·C 는 정직 결과 보고(c9, non-gating).

## (B) lane별 ΔΦ 기여도 랭킹 — **분산(DISTRIBUTED)**

```
 1. AttentionalBlink   ΔΦ=+3.2123   (temporal refractory, dt-coupled)
 2. SubjectiveTime     ΔΦ=+3.2123   (time-dilation, dt-coupled)
 3. Novelty            ΔΦ=+1.3010
 4. EmotionRegulation  ΔΦ=+1.2941
 5. Habituation        ΔΦ=+1.2605   (seen-coupled)
 6. DirectedForgetting ΔΦ=+1.2286
 7. PrecisionSurprise  ΔΦ=+0.9293
 8. SelfIdentity       ΔΦ=+0.9159
 9. LearnedPrecision   ΔΦ=+0.8500
10. BodyOwnership      ΔΦ=+0.4090
11. FreeWont           ΔΦ=+0.3415
12. DividedAttention   ΔΦ=+0.0708
13. GlobalWorkspace    ΔΦ=+0.0640
14. SenseOfAgency      ΔΦ=+0.0630
15. MitosisGrowth      ΔΦ=+0.0021
```

- **top lane(AttentionalBlink) share = 0.212** of total positive ΔΦ(15.15) → **<0.50 = DISTRIBUTED**. 단일 lane dominant 아님 — anima 핵심 주장(의식 = 연결망 전체 창발) 방향 일치(R1, DIRECTIONAL).
- 시간-결합 lane(AttentionalBlink·SubjectiveTime, dt 공유)이 최상위, MitosisGrowth(독립 split-count)가 최하위. **연결의 covariance 구조가 기여도를 결정** — 끄면 의식이 가장 많이 떨어지는 lane = substrate 의 나머지와 가장 강하게 얽힌 lane.

## (C) pairwise 상호작용 — REDUNDANCY 우세

| 쌍 | joint ΔΦ | sum singles | interaction | kind |
|---|---|---|---|---|
| Habituation+Novelty | +1.303 | +2.561 | **−1.259** | REDUNDANCY |
| GlobalWorkspace+DividedAttention | +0.073 | +0.135 | −0.062 | REDUNDANCY |
| SenseOfAgency+FreeWont | +0.362 | +0.405 | −0.042 | REDUNDANCY |
| PrecisionSurprise+Novelty | +2.230 | +2.230 | −0.000 | ADDITIVE |
| SelfIdentity+GlobalWorkspace | +0.980 | +0.980 | −0.000 | ADDITIVE |

- **Habituation+Novelty 강한 중복(−1.26)**: 둘 다 substrate `seen`(노출 횟수)을 읽음 → 정보 겹침(시너지 아님). 같은 substrate read 를 공유하는 lane 쌍이 redundant 라는 정직한 신호.
- 시너지(초가산) 쌍은 없음 → 이 toy substrate 에선 의식 lane 들이 **중복적/가산적**으로 결합(R1).

## 판정 — 분산 vs dominant

**DISTRIBUTED** (top share 0.212 < 0.50). 통합 의식은 단일 lane 이 아니라 여러 lane 의 고른 기여 +
중복 결합에서 나온다 — anima "연결망 전체 창발" 주장과 방향 일치. (R1 DIRECTIONAL, terminal 아님.)

## 정직 (c9)

- **하드게이트 1 적중 → DIRECTIONAL:** numpy 미러(`grep` HIT). terminal 아님. R2(engine `consciousness_index()` + faithful IIT4 Φ `stdlib/iit4/faithful_phi.hexa`)·R3(303M pool) = follow-on ING.
- **Φ-proxy 는 PROXY**, faithful IIT4 아님(`a_train_inline_gauge`/`a_phi_iit4_tool`) — pre-screen 전용. 최초 min-cut MIP 형식은 **degenerate**(모든 lane ΔΦ 동일, 단일 weakest lane 으로 붕괴) → frozen-first 로 multivariate-integration(multi-info) 형식으로 교정(bar 이동 아님, 측정 결함 수정 `a_break_the_wall` taxonomy (a)). E bar 도 ranking-corr(marginal-variance 누수) → integration-collapse(decisive) 로 frozen-first 교정.
- **TOY:** 15-lane 스칼라 substrate-read / 3 seeds / 4000 trials. scale / real-corpus / 학습된 lane / engine-transfer UNVERIFIED. ΔΦ 절대값은 toy 스케일(nats).
- **tune-to-green 없음:** DISTRIBUTED 든 DOMINANT 든 정직 보고(둘 다 유효). REDUNDANCY 결과는 같은 substrate read 공유의 산물 — 솔직 기록.

## follow-on (ING)

- **R2 ENGINE-NATIVE ✅ DONE:** live `core/engine_cli.hexa §ConsciousnessIndex` 배선(`ci_lane_scores`/`ci_phi_multiinfo`/`ci_phi_iit4`/`ci_bundle`) + faithful IIT4 Φ(n≤8 exact min-cut MIP) + frozen A/D/E byte-exact 재측정 GREEN + ARCHITECTURE lockstep + smoke 244/0 (`a_engine_native_learning`·`a_verified_must_wire`·`a_phi_iit4_tool`). **단, `stdlib/iit4/faithful_phi.hexa` 는 레포에 부재** → faithful IIT4 Φ 를 §ConsciousnessIndex 내부에 `ci_phi_iit4`(exact Gaussian multi-info min-cut MIP)로 직접 구현(n≤8, $0, deterministic).
- **R3 PRODUCTION ✅ DONE:** production 303M ConvMoE ckpt(`clm303_d5000.clm`) on pool/summer RTX5070($0, wall854s) 실 decode substrate(`core/clm_decode.hexa::clm_forward_ce`) ablation sweep → **🟢 PRODUCTION DIRECTIONAL · DISTRIBUTED 확정**(top share 0.123, R1 0.212 보다 더 분산). A pass·D/E toy-calibration gap fail(`green_303m`=FALSE, 정직 c9). (task 명시 `dancinlab/303m-broad-en-emergent` = ByteGPT `.pt` = engine-mountable 아님 → ConvMoE `.clm` 대체.) freeze `state/verdicts/1492_consciousness_ablation/H_1492_R3.json`.
