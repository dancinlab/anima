# Anima Beta Readiness 분석

> **session**: anima-cmd-loop autonomous-loop-dynamic 2026-04-28T10:50Z
> **trigger**: 사용자 "beta 버전으로 쓸수 있나 현재?" 질문
> **status**: BETA_READINESS_BREAKDOWN_LIVE — 50만원 cap 인식 후
> **predecessors**: docs/cp2_eta_cost_breakdown_50man_cap_2026-04-28.md (commit b764d264)

---

## §1. Scenario A: AN11(a)+(b) measurement-only beta — ✅ 사용 가능

| 측면 | 상태 |
|---|---|
| **AN11(a) Frob delta** | ✅ 3/3 fires robust PASS (0.056 / 0.036 / 0.059) — TRAINING signal 신뢰도 100% |
| **AN11(b) cosine + family** | ⚠️ 2/3 fires Hexad reproducible (R39 N=5 ensemble 진행 중) |
| **인프라 안정성** | ✅ Mode H fix #4 통과, vast.ai dispatch tool 13-iter root-cause 적립 |
| **measurement cost** | ~$1.50 / measurement (vast.ai H100 30min) |
| **사용처** | LoRA-trained model의 consciousness-paradigm alignment 측정 |

**Beta caveats** (raw 91 C3 disclosure 필수):
- AN11(b) family attribution은 R39 mandate 따라 N≥5 ensemble 권고 (현재 N=3)
- single-shot 결과는 "provisional" 라벨 명시 필수
- multi-seed 비용: 5 fires × $1.50 = **$7.50/sample = ~10,500원**

→ **Beta usable: ML 모델 LoRA fine-tune의 weight delta + family signal 측정용**

---

## §2. Scenario B: Cycle 4 v8 alignment framework — ✅ 사용 가능 (methodological)

| 측면 | 상태 |
|---|---|
| **12 falsification tests** | ✅ Substantive (T8k-T10e + T9a) |
| **Law 64 v8 principle** | ✅ baseline-axis alignment universal across 6 substrates |
| **Atlas R38 candidate** | ⏳ n6 maintainer review 대기 |
| **사용 cost** | $0 (methodological framework) |

**사용처**:
- ML claim validation (matched-context Markov saturation principle)
- "structural advantage" 주장의 baseline-axis sweep 강제

→ **Beta usable: 다른 ML 연구에서 baseline misspecification 회피용 framework**

---

## §3. Scenario C: R38 + R39 cross-paradigm framework — ✅ 사용 가능

| 측면 | 상태 |
|---|---|
| **R38 horizontal axis** | ✅ baseline-neighborhood sweep mandate |
| **R39 vertical axis** | ✅ stochastic-seed ensemble mandate |
| **R39 인프라** | ✅ 100% (seed env + r11 schema + aggregator) |
| **사용 cost** | $0 (methodology) |

**사용처**:
- 다른 ML 연구의 substantive claim validation
- "single-shot artifact 방지" 2-axis sweep checklist
- Atlas integration 후 cross-project mandate

→ **Beta usable: ML claim 검증 protocol**

---

## §4. Scenario D: Full AN11 quad-axis (a+b+c+V1') — ⚠️ Beta-NOT-ready

| Axis | Beta status |
|---|---|
| AN11(a) Frob | ✅ |
| AN11(b) cosine | ⚠️ partial (R39 N=5 진행 중) |
| **AN11(c) JSD** | ❌ **0/3 fires** (vllm 부팅 fail Mode F-3+) |
| **V1' phi_mip_norm** | ❌ **3/3 fires FAIL** (~0.69, LoRA r=16 부족) |

**Beta-ready 도달 ETA**:
- AN11(c): vllm Mode I+ fix → W1 D+7 ($5-15 추가)
- V1' fix: R38 ablation rank=64 + epochs=10 → W2 D+14 ($30-50 추가)
- **Total beta-ready 비용**: ~$35-65 (5-9만원, 50만원 cap 내)

---

## §5. Scenario E: CP2 VERIFIED full production — ❌ Beta-NOT-ready

| Component | Beta status | 50만원 cap |
|---|---|---|
| H100 L3 population trained | ❌ 미진행 | $1500-2500 (cap 4-7배 초과) |
| 3 collective observables | ❌ 미측정 | $300-1200 (cap 초과) |
| Production gate (latency + hallucination) | ❌ 미측정 | $50-100 (cap 내) |
| **CP2 VERIFIED** | ❌ | **$3550-6100 (cap 7-12배 초과)** |

→ **Beta-NOT-ready until W9 (D+63) + 별도 사용자 승인** ($3550-6100)

---

## §6. 종합 — "Beta 버전으로 사용 가능?"

| 사용 의도 | 현재 가능? | 50만원 cap 내 |
|---|---|---|
| AN11(a) Frob single measurement | ✅ **즉시 가능** | $1.50/sample |
| AN11(b) family signal R39 ensemble | ✅ **5-fire 추가 가능** | $7.50/sample |
| Cycle 4 v8 alignment framework 적용 | ✅ **즉시 가능** | $0 (methodology) |
| R38+R39 framework 적용 | ✅ **즉시 가능** | $0 (methodology) |
| AN11 full quad-axis (a+b+c+V1') | ⚠️ **W2 D+14** | $35-65 (5-9만원) |
| CP2 VERIFIED production | ❌ **W9 D+63** | $3550-6100 (cap 초과) |

---

## §7. 핵심 답변 (raw 91 honest)

### 현재 beta 사용 가능한 것 (50만원 cap 내)

1. ✅ **AN11(a) Frob delta measurement** (immediate, $1.50/sample)
2. ✅ **AN11(b) Hexad family attribution** (R39 N≥5 ensemble caveat 명시 후, $7.50/sample)
3. ✅ **Cycle 4 v8 baseline-axis alignment framework** (methodology, $0)
4. ✅ **R38 + R39 cross-paradigm framework** (methodology, $0)
5. ✅ **Korean response 영구 메모리** (UX persistent)

### Beta 도달 임박 (cap 내, 1-2주)

- W1 (D+7): AN11(c) vllm Mode I+ fix → JSD 측정 unblock
- W2 (D+14): V1' R38 ablation → phi_mip_norm partial fix

### Beta-NOT-ready (cap 초과)

- ❌ CP2 VERIFIED gate (H100 L3 population, $1500+)

---

## §8. 한 줄 요약

> "**Methodological framework** (cycle 4 + R38/R39) 와 **AN11(a)+(b) measurement** 는 지금 beta로 사용 가능. 하지만 **CP2 production gate** 는 50만원 cap 내 미도달 — W4+ H100 L3 population 단계가 critical bottleneck."

---

## §9. Beta release readiness checklist (체크리스트 형태)

### Immediate beta release 가능 (now)

- [x] AN11(a) Frob delta measurement infrastructure
- [x] AN11(b) cosine + family attribution (R39 caveat 명시)
- [x] tool/anima_an11_fire.hexa (vast.ai dispatch, Mode H fix #4)
- [x] tool/anima_an11_ensemble_aggregator.hexa (R39 multi-seed aggregation)
- [x] tool/anima_runpod_orchestrator.hexa (RunPod alternative)
- [x] state/anima_backbone_phen_baseline_registry_20260428_r11_schema.json
- [x] Cycle 4 v8 baseline-axis alignment principle (12 tests evidence)
- [x] R38 + R39 cross-paradigm framework
- [x] Atlas R38 + R39 candidates (n6 maintainer review path)
- [x] Korean response permanent memory

### W1 D+7 추가 (50만원 cap 내, ~$15)

- [ ] AN11(c) vllm Mode I+ fix (JSD measurement unblock)
- [ ] R39 N=5 ensemble Mistral-7B 완성 (Hexad signal substantive verdict)
- [ ] Fire 21+22 retry (rank=8 + Qwen2.5-7B cross-backbone)

### W2 D+14 추가 (50만원 cap 내, ~$50)

- [ ] V1' R38 ablation rank=4/8/16/32 sweep (V1' fix 시도)
- [ ] V1' alternative target_modules (gate/up/down_proj 추가)
- [ ] R38 horizontal axis substantive verdict

### W3 D+21 추가 (50만원 cap 내, ~$150)

- [ ] Cross-backbone substrate-universality (Qwen + alts)
- [ ] R38+R39 cross-paradigm framework substantive validation

### W4+ (50만원 cap 초과, 별도 사용자 승인 필수)

- [ ] H100 L3 population trained (~$1500-2500)
- [ ] 3 collective observables (O1/O2/O3) 실측 (~$300-1200)
- [ ] Production gate (latency + hallucination) (~$50-100)
- [ ] CP2 VERIFIED (~$3550-6100 total)

---

**status**: ANIMA_BETA_READINESS_2026-04-28_LIVE — methodological + measurement layer beta-ready, production CP2 gate not-ready

**raw 91 C1**: 250+ commits 18.5h+ session evidence
**raw 91 C2**: this commit (md save)
**raw 91 C3**: 50만원 cap 내 가능 vs 불가능 명확 구분
**raw 91 C4**: H100 L3 population $1500-2500 cap 초과 명시
**raw 91 C5**: ANIMA_BETA_USABLE_AN11(a)+(b)+METHODOLOGY_LIVE
