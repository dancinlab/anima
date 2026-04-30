# CP2 도착 ETA — 7일-단위 + 비용 분해 + 50만원 cap 분석

> **session**: 2026-04-28T10:48Z (Fire 19 TCP_NOT_READY + Fire 20 in flight)
> **trigger**: 사용자 50만원 ($350 USD) cap 명시
> **status**: COST_CAP_50MAN_AWARE_ETA_BREAKDOWN_LIVE

> **AI-native ETA SSOT (2026-05-01)**: For any closure / roadmap ETA in this repo, the authoritative computation is `$HIVE/tool/closure_eta.hexa` (LoC × parallel + bg × ∞ frame, rate 50,000 LoC/day/agent default, par+ser schema, DAG critical path). Static "+N 달" / "+N month" markdown estimates anchored to human single-developer baseline are DEPRECATED for closure-scope decisions per hive raw 257 (`ai-native-eta-closure-mandate`). Reference fixture: `--module critical-path --example gamebox --target CM-30` = 0.22d ≈ 5.3h vs static 630d (×2863 compression).

---

## §1. CP2 도착 ETA (9주 / 63일)

| Week | Days | Phase | 핵심 deliverable | Fire/Run 수 | 누적 비용 |
|---|---|---|---|---|---|
| **W1** | D+0~D+7 | AN11 인프라 마무리 | R39 N=5 ensemble + Mode I+ fix | 5-10 fires | $20-30 |
| **W2** | D+7~D+14 | R38+V1' ablation | rank=4/8/16/32 + epochs sweep | 6-12 fires | $35-50 |
| **W3** | D+14~D+21 | Cross-backbone | Qwen + Llama + gemma alts | 6-10 fires | $50-70 |
| **W4** | D+21~D+28 | **H100 L3 population start** | 4× H100 sustained | (시간 ×) | **$1500-2500** |
| **W5** | D+28~D+35 | L3 population continue | 4× H100 sustained | continue | **$3000-5000** |
| **W6** | D+35~D+42 | 3 observables 측정 start | O1/O2/O3 GPU runs | 10-20 runs | $3300-5500 |
| **W7** | D+42~D+49 | observables continue | tomography + cross-validation | continue | $3500-6000 |
| **W8** | D+49~D+56 | Production gate | latency + hallucination | small fires | $3550-6100 |
| **W9** | D+56~D+63 | CP2 verification | closure + atlas integration | $0 docs | **$3550-6100 final** |

**Total CP2 cost projection**: **$3550-6100 USD ≈ 500-850만원** (env 의존)

## §2. 50만원 cap (~$350) 제약 분석

**현재 누적**: ~$15 USD = ~21,000원 (4.3% / 50만원)
**여유**: ~$335 USD = ~470,000원

### Cap 내 가능한 phase

| Cap 사용량 | Phase 도달 | CP2 진척 |
|---|---|---|
| ~$50 (7만원) | W1 완료 (AN11 인프라) | 11% |
| ~$100 (14만원) | W2 완료 (ablation) | 22% |
| ~$150 (21만원) | W3 완료 (cross-backbone) | 33% |
| ~$350 (50만원) | W3.5 (cross-backbone + 일부 W4 시작) | ~38% |
| **CP2 full** | **W9 (~$3550-6100, 500-850만원)** | **100%** |

→ **50만원 cap은 W3.5 (cross-backbone + W4 시작 일부)까지만 cover**
→ **H100 L3 population (W4-5) 자체가 $1500-2500 (210-350만원)으로 50만원 cap 7배 초과**

### Cap 내 substantive milestone (raw 91 honest)

50만원 ($350) 내 도달 가능:
- ✅ AN11(a) Frob 5-fire ensemble PASS (R39 substantive)
- ✅ AN11(b) Hexad family signal R39 verdict (4/5 또는 2/5)
- ✅ V1' phi_mip_norm R38 ablation (rank=4/8/16/32 + epochs=10) — partial fix 가능성
- ✅ AN11(c) JSD vllm Mode I+ fix + 측정 (인프라 완성)
- ✅ Cross-backbone substrate-universality (Qwen + alts)
- ✅ 2 atlas R-candidates substantive validation (R38 + R39)

50만원 내 도달 **불가능**:
- ❌ H100 L3 population trained (W4-5, $1500-2500 / 210-350만원)
- ❌ 3 collective observables 실측 (W6-7, $300-1200 추가)
- ❌ Production gate live measurement (W8, $50-100)
- ❌ CP2 VERIFIED gate

## §3. 비용 증가 추적 (7일 단위)

### 본 세션 누적 (단일 day Fire 1-20)

| 단위 | 시점 | Fires | 누적 cost | 비고 |
|---|---|---|---|---|
| Day 1 (오늘) | 18.5h+ session | 20 fires (1-20) | **~$15** | Fire 18 PARTIAL_PASS milestone |

→ Fire 1-20 dispatched, Fire 6+10+18 ($1.71+$1.71+$0.49 = $3.91), 나머지 fires NO_OFFERS or fail-fast = ~$11.

### W1-W9 누적 forecast (50만원 cap 인식 후)

| Week ending | Fires (cum) | Cost (cum) | 도달 milestone |
|---|---|---|---|
| W1 (D+7) | ~30 | $35-45 (5-6만원) | **AN11 인프라 안정화 완료** |
| W2 (D+14) | ~45 | $60-90 (8-12만원) | **R38 ablation + V1' 부분 fix** |
| W3 (D+21) | ~55 | $90-150 (12-21만원) | **Cross-backbone substrate-uni** |
| W4 (D+28) | ~65 + L3 sustained | **$1600-2700** (220-380만원) | **H100 L3 population start** ⚠️ cap 초과 |
| W9 (D+63) | full | **$3700-6100** (520-860만원) | **CP2 VERIFIED** ⚠️ cap 7-12× 초과 |

## §4. 권장 action plan (50만원 cap 준수)

### 단기 (W1-W3, $150 / 21만원 내)
1. R39 N=5 ensemble 완성 — 현재 Fire 20 in flight, Fire 21/22 retry 시
2. R38 ablation rank=4/8/16/32 — 4 fires × $1.50 = $6
3. Cross-backbone Qwen + 추가 — 3-5 fires × $1.50 = $4.50-7.50
4. AN11(c) vllm fix Mode I+ → JSD 측정 substantive

→ **50만원 cap 내 도달 가능 deliverables ROI 최대화**

### 중장기 (CP2 W4+ 진입 결정)
- H100 L3 population 별도 explicit 사용자 승인 필요 ($1500-2500 / 210-350만원)
- 또는 cluster grant / academic partnership / cloud credit 활용
- 또는 trained L3 population 단계를 reduced-scale (1 H100 × 5일 = ~$300) prototype부터

## §5. raw 91 honest summary

**확실** (cap 내 가능):
- AN11 인프라 + ablation + cross-backbone (W1-W3) 완성도 90%+ 달성
- 2 atlas R-candidates (R38 + R39) substantive validation
- CP2 critical path 33% 진척

**불확실 / cap 초과**:
- H100 L3 population (단일 phase $1500-2500)
- CP2 VERIFIED full gate (50만원 cap 7-12× 초과 필수)

**Anchor**:
- 50만원 cap 내 W3 도달 = ~3주 (D+21)
- CP2 VERIFIED 도달 = 9주 (D+63), but 500-850만원 cap 필요

---

**status**: CP2_ETA_7DAY_BREAKDOWN_50MAN_CAP_AWARE_LIVE
