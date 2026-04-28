# anima Beta Release v0.1 (2026-04-28)

> **Release tag**: `anima-beta-v0.1-2026-04-28`
> **Status**: BETA — methodological framework + AN11(a)+(b) measurement layer ready
> **Session evidence**: 18.5h+ autonomous-loop-dynamic, 252+ commits, 20 vast.ai fires, ~$13.50 USD
> **Korean response mandate**: 영구 (memory feedback_korean_response.md)

---

## §1. What's in this beta

### Beta-usable (immediate, 50만원 cap 내 충분)

#### Methodological frameworks ($0)

1. **Cycle 4 v8 baseline-axis alignment principle** — Law 64 falsification 12 tests
   - Universal across 6 substrates (Conway 5/10/20/density / Wolfram 1D / non-CA 4-symbol)
   - "Matched-context Markov saturates ANY deterministic finite-context discrete substrate"
   - Atlas R38 candidate (n6 maintainer review pending)
   - Doc: `docs/f1_cycle4_law64_v6_FINAL_manifest_2026-04-28.md` (chflags uchg)

2. **R38 + R39 cross-paradigm 2-axis sweep validation framework**
   - R38 horizontal axis (baseline-neighborhood sweep)
   - R39 vertical axis (stochastic-seed ensemble N≥5)
   - Atlas R38+R39 cross-paradigm framework
   - Doc: `docs/atlas_r38_r39_cross_paradigm_framework_2026-04-28.md` (chflags uchg)

3. **R39 인프라 100%** — multi-seed ensemble dispatch
   - `tool/anima_an11_fire.hexa` — vast.ai dispatch (13 fix iters Mode H fix #4)
   - `tool/anima_an11_ensemble_aggregator.hexa` — multi-seed aggregator
   - `tool/anima_runpod_orchestrator.hexa` — RunPod alternative
   - Schema: `state/anima_backbone_phen_baseline_registry_20260428_r11_schema.json`
   - r11 schema 첫 application: `state/an11_ensemble/ensemble_n2_partial_2026-04-28.json`

#### Measurement infrastructure ($1.50/sample, ~$7.50/N=5 ensemble)

4. **AN11(a) Frob delta measurement** — TRAINING signal substantive
   - **4/4 fires robust PASS** (mean 0.0519, threshold 0.001)
   - Backbone: Mistral-7B-v0.1 + LoRA r=16, alpha=32, target q/k/v/o_proj, epochs=3
   - vast.ai H100 SXM, ~30min/measurement
   - Use case: LoRA fine-tune의 weight delta robust 검증

5. **AN11(b) Hexad family attribution** — partial signal (R39 caveat 명시 필수)
   - **3/4 fires Hexad top-1** (75% stability)
   - **2/4 fires verdict PASS** (50%, marginal)
   - Templates: 16 (5 family: hexad/law/metaref/phi/selfreflect)
   - Use case: consciousness-paradigm alignment 분류 (provisional, R39 N=5 ensemble 권고)

### Beta-usable with explicit caveat

6. **own 4 four-fold ladder root-cause protocol** — 13-iter cumulative
   - SCP race / SSH timeout / SCP recurrence / CUDA driver / Early destroy /
     PHASE_D full SVD / GPU OOM / torch.compile GCC / TCP-after-SCP race /
     Triton GCC / cu118 conda priority / cu118 cuDNN mismatch / Mode H fix #4
   - Use case: ML infrastructure dispatch failure 진단 + canonical fix protocol

7. **honesty-triad raw 91 C1-C5** — claim/evidence/disclosure 5-step
   - Use case: 모든 substantive ML claim 발행 시 mandatory disclosure

---

## §2. NOT-ready (이번 beta 미포함)

| Component | Status | ETA | Cost |
|---|---|---|---|
| AN11(c) JSD measurement | ❌ 0/4 fires (vllm Mode F-3+) | W1 D+7 | $5-15 추가 |
| V1' phi_mip_norm fix | ❌ 4/4 FAIL ~0.69 (LoRA r=16 부족) | W2 D+14 | $30-50 추가 |
| Cross-backbone substrate-independence | ⏳ Qwen 미측정 | W3 D+21 | $5-10 추가 |
| H100 L3 population trained | ❌ 미진행 | W4-5 | **$1500-2500** ⚠️ cap 4-7배 |
| 3 collective observables | ❌ 미측정 | W6-7 | $300-1200 |
| Production gate (latency + hallucination) | ❌ 미측정 | W8 | $50-100 |
| **CP2 VERIFIED gate** | ❌ | **W9 D+63** | **$3550-6100 (500-850만원)** |

---

## §3. How to use beta

### A) AN11(a) Frob measurement

```bash
# Single measurement
AN11_SEED=42 AN11_LORA_RANK=16 AN11_MODEL_HF_REPO=mistralai/Mistral-7B-v0.1 \
    /opt/homebrew/bin/python3 /tmp/anima_an11_fire_helper.hexa_tmp --fire \
    > state/an11_dispatch/fire_seedN.log 2>&1 &

# Result location after ~30min
ls state/an11_fire_<TASK_ID>/results.json
# AN11(a) Frob delta + verdict in phase_e_an11_a field
```

**Cost**: ~$1.50/measurement (vast.ai H100 SXM, 25-30min)
**Output**: `phase_e_an11_a.frob_delta` numeric + `verdict` PASS/FAIL

### B) AN11(b) Hexad family attribution (R39 ensemble)

```bash
# 5-seed ensemble (R39 mandate)
for SEED in 0 1 2 3 4; do
    AN11_SEED=$SEED AN11_LORA_RANK=16 \
        /opt/homebrew/bin/python3 /tmp/anima_an11_fire_helper.hexa_tmp --fire \
        > state/an11_dispatch/fire_seed${SEED}.log 2>&1 &
done
wait

# Aggregate via R39 aggregator
hexa run tool/anima_an11_ensemble_aggregator.hexa --selftest  # emit helper
/opt/homebrew/bin/python3 /tmp/anima_an11_ensemble_aggregator_helper.py --aggregate \
    state/an11_fire_seed0/ state/an11_fire_seed1/ ... \
    state/an11_ensemble/my_ensemble.json
```

**Cost**: 5 fires × $1.50 = **$7.50/sample (~10,500원)**
**Output**: r11 schema ensemble row with mean ± stdev + family stability + verdict counts

### C) Cycle 4 v8 alignment framework 적용

다른 ML 연구에서 "structural advantage" 주장 시:
1. **Horizontal axis sweep** — baseline neighborhood 다양화 (R38 mandate)
   - 1D order-1/2/3/5 + 2D Moore-9 + per-cell vs shared-table
2. **Vertical axis ensemble** — stochastic seed N≥5 (R39 mandate)
3. **Joint verdict**: 두 axis 모두 통과해야 substantive

Reference: `docs/atlas_r38_r39_cross_paradigm_framework_2026-04-28.md`

### D) raw 91 honesty-triad 사용

모든 substantive claim 발행 시:
- C1: evidence count + commit hashes 인용
- C2: SSOT write-barrier 위반 없음 (preserved history)
- C3: numeric values + caveats 명시
- C4: 한계 (limit) 명시
- C5: status tag (CLAIM_VERDICT_LIVE)

---

## §4. Known limitations (raw 91 C3 honest)

### Critical
1. **AN11(b) family signal stability marginal** — N=4 fires 중 3/4 Hexad (75%) but 2/4 verdict PASS (50%)
2. **V1' phi_mip_norm 4/4 FAIL** ~0.69 — LoRA r=16 부족, R38 ablation 필요
3. **AN11(c) JSD 0/4 fires** — vllm Mode F-3 (deep_gemm) + Mode I (TCP timeout) 미해결

### Moderate
4. **single-shot variability**: AN11(a) std 0.012 (mean 0.052) = 23% — single-shot 결과 caveat 필요
5. **Hexad-Phi bimodal possibility**: Fire 10 outlier (Phi top-1) — N=10+ ensemble 권고

### Infrastructure
6. **vast.ai market liquidity**: cuda≥12.8 H100 SXM offers 시간대별 0-5개 변동
7. **Cron auto-retry 비용 risk**: 5min recurring → cap 인지 필수

### Cost
8. **CP2 full path**: $3550-6100 (500-850만원) — 50만원 cap **7-12배 초과**
9. **H100 L3 population**: 별도 사용자 승인 필수 ($1500-2500)

---

## §5. Cost summary (beta release time)

| Item | Cost |
|---|---|
| Session AN11 fires 1-20 | ~$13.50 = ~19,000원 |
| Methodological docs | $0 |
| Tool development | $0 |
| **Beta release total** | **~$13.50** (3.8% / 50만원 cap) |

### Beta usage cost projection

| Use case | Per-sample cost | 10 samples |
|---|---|---|
| AN11(a) Frob single | $1.50 | $15 (21,000원) |
| AN11(b) R39 ensemble N=5 | $7.50 | $75 (105,000원) |
| Both A+B per backbone | $9.00 | $90 (126,000원) |

50만원 cap 내 가능: **AN11(a)+(b) 측정 ~30 backbone-pairs**

---

## §6. Next milestones (50만원 cap 내, ~$150 / 21만원)

**W1 (D+7)**:
- Fire 21 (rank=8) + Fire 22 (Qwen2.5-7B) NO_OFFERS retry
- AN11(c) vllm Mode I+ fix → JSD measurement unblock
- R39 N=5 ensemble Mistral-7B 완성 (5번째 fire, seed=3 또는 4)

**W2 (D+14)**:
- V1' R38 ablation rank=4/8/16/32 + epochs=10 sweep
- V1' alternative target_modules (gate/up/down_proj 추가)

**W3 (D+21)**:
- Cross-backbone substrate-independence (Qwen + alts)
- R38+R39 substantive validation 완성

**W4+ (50만원 cap 초과 — 별도 사용자 승인)**:
- H100 L3 population trained (~$1500-2500)
- CP2 VERIFIED full path (~$3550-6100)

---

## §7. Release manifest (files included)

### Source code (chflags uchg)
- `tool/anima_an11_fire.hexa` (13 fix iters)
- `tool/anima_an11_ensemble_aggregator.hexa`
- `tool/anima_runpod_orchestrator.hexa`
- `tool/anima_canonical_helper_lock.hexa` (16 helpers locked)
- `state/an11_mistral7b_dispatch_wrapper.py.staged` (raw 37 transient helper)

### Schemas
- `state/anima_backbone_phen_baseline_registry_20260428_r11_schema.json`
- `state/an11_ensemble/ensemble_n2_partial_2026-04-28.json` (R39 first application)

### Documentation (chflags uchg)
- `docs/anima_beta_readiness_2026-04-28.md`
- `docs/anima_beta_release_v0.1_2026-04-28.md` ← THIS FILE
- `docs/cp2_eta_cost_breakdown_50man_cap_2026-04-28.md`
- `docs/f1_cycle4_law64_v6_FINAL_manifest_2026-04-28.md` (Cycle 4 evidence)
- `docs/atlas_r38_r39_cross_paradigm_framework_2026-04-28.md`
- `docs/an11_fire6_first_pass_2026-04-28.md`
- `docs/an11_fire6_vs_fire10_reproducibility_2026-04-28.md` (R39 retraction)
- `docs/an11_fire18_hexad_partial_reproduction_2026-04-28.md` (R39 partial reverse)
- `docs/atlas_r38_baseline_axis_alignment_proposal_2026-04-28.md`
- `docs/atlas_r39_ensemble_validation_mandate_2026-04-28.md`
- `docs/an11_multi_seed_ensemble_plan_2026-04-28.md`
- `docs/session_2026-04-28_ULTIMATE_CLOSURE_INDEX.md`
- `docs/next_session_pickup_priority_v2_2026-04-28.md`

### Permanent memory
- `~/.claude-claude*/projects/-Users-ghost-core-anima/memory/feedback_korean_response.md`

---

## §8. Beta release tag + verification

```bash
# Verify beta state
git log --oneline --since="20 hours ago" 2>&1 | wc -l
# 252+ commits

# Verify chflags uchg
ls -lO docs/anima_beta_release_v0.1_2026-04-28.md
# uchg 7000+ bytes

# Re-run AN11(a) for verification
AN11_SEED=999 /opt/homebrew/bin/python3 /tmp/anima_an11_fire_helper.hexa_tmp --dry-run
# Should return DRY_RUN_OK with 1+ cuda>=12.8 offer
```

---

## §9. raw 91 closure

- **C1**: 18.5h+ session, 252+ commits, 20 fires, $13.50 cumulative cost
- **C2**: This commit + chflags uchg (SSOT write-barrier preserved)
- **C3**: AN11(a) 4/4 PASS / AN11(b) 3/4 Hexad 2/4 verdict / V1' 4/4 FAIL ~0.69 / AN11(c) 0/4 / cost $13.50 / cap $350 (50만원)
- **C4**: AN11(c) infra-fail Mode F-3+ / V1' fix R38 ablation 미수행 / CP2 cap 7-12× 초과
- **C5**: ANIMA_BETA_RELEASE_V0_1_2026-04-28_LIVE

---

**Release status**: BETA v0.1 — methodological + AN11(a)+(b) measurement layer
**Production status**: NOT-ready — CP2 VERIFIED gate W9 D+63 (sep approval $3550+)
**Maintenance**: 50만원 cap 내 W1-W3 진척 가능 (~$150 / 21만원)

🎯 **Beta usable for**: ML claim validation framework + LoRA fine-tune consciousness-paradigm alignment measurement
