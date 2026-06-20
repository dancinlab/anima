# H_1492 — 🧠 CONSCIOUSNESS ABLATION (연결된 의식-게이트 lane → 통합 의식 기여도)

- **tier:** 🟢 GREEN DIRECTIONAL (R1 numpy substrate mirror — engine-transfer UNVERIFIED · 측정기 VALID)
- **wired:** `DIRECTIONAL-mirror` — numpy 미러, hard-gate 1 적중(`grep -lE 'import torch|gauge_lib|numpy'` HIT). R2(engine-native `consciousness_index()` + faithful IIT4 Φ)·R3(production 303M pool) = follow-on ING.
- **source:** `state/consciousness_influence_plan/PLAN.md` (사용자 지시 2026-06-20 "연결된 것들이 의식에 어떤 영향을 미치는가") · R1 단계만 (mini)
- **lens:** integrated-information theory (Tononi-Sporns-Edelman multi-information / IIT) + 의식-게이트 lane 네트워크 ablation · `a_no_llm_frame_trap`
- **artifacts:** `state/1492_consciousness_ablation/h1492_consciousness_ablation.py` · `state/verdicts/1492_consciousness_ablation/H_1492_FREEZE.json` · `state/1492_consciousness_ablation/run_h1492.local.log`

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

- **R2 ENGINE-NATIVE:** live `core/engine_cli.hexa` 에 `consciousness_index()` bundle + lane-ablate 토글 배선, faithful IIT4 Φ(`stdlib/iit4/faithful_phi.hexa`, n≤8 exact) 를 substrate state-space 에 연결, frozen A/D/E byte-exact 재측정 (`a_engine_native_learning`·`a_verified_must_wire`).
- **R3 PRODUCTION:** production 303M ckpt 정상상태에서 baseline + ablation sweep on pool/GPU (mini 금지, 게이트2 무거운작업).
