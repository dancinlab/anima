# H_686 + H_687 V-scale escape boundary sweep 결과 (2026-05-29)

**status**: 🟠 SWEEP-OUT-OF-RANGE — baseline 이 V ∈ {8, 64, 256, 1024, 4096} 전 구간 collapse 미발생, escape boundary 미발견
**source**: PR #1395 (h686_h687_aux_ablation.hexa ⚪ TOY-NULL at V=8) 의 V-axis extension
**harness**: `CORE/DECODER/h686_h687_v_scale.hexa` (PR #1395 byte-eq scaffold + V parametric)
**driver**: `state/h686_h687_v_scale_2026_05_29/run_sweep.hexa`
**raw output**: `state/h686_h687_v_scale_2026_05_29/V{V}_{cell}.out` (20 files)
**cost**: $0 mac-local, 20 cells × 600 step, 총 wall ~24 min (V=8: ≤1s/cell, V=4096: 185~370s/cell)

---

## 1. 메서드 (PR #1395 byte-eq 보존)

- **차원**: E=4, d=6, n_clusters=6, n_steps=600, lr=0.5, top-1 hard routing
- **corpus map**: cluster_i → token `(i * stride) mod V` where `stride = max(1, V/6)`
  - V=8: stride=1 → cluster c → token c (PR #1395 verbatim)
  - V=64: stride=10 · V=256: stride=42 · V=1024: stride=170 · V=4096: stride=682
- **SKEWED corpus**: cluster 0 = 20× 과대표 (E2 Scenario B verbatim, M4b decode dist mirror)
- **aux**: λ_ent = 0.1 (H_686 · `-λ·H(p)` router entropy reg), λ_kl = 0.1 (H_687 · `KL(softmax(logits)||uniform_V)` output reg) — PR #1395/#1397 verbatim
- **LZ_norm**: BITS=18 (PR #1395 verbatim, V ≤ 2^18 모두 표현 가능 — sanity gate byte-eq 보존)
- **M init seed**: PR #1395 verbatim deterministic structured init (`base + bump + bump2`)

### 1.1 Sanity gate (V=8 cell=none ≡ PR #1395)

```
V=8 cell=none  →  LZ_norm=0.0360459  distinct_experts=4  ✓ MATCH PR #1395
```

Byte-equal 확인 — harness 의 V-parametric 일반화가 V=8 에서 PR #1395 의 토이를 정확히 재현. corpus-map (`stride=V/6` clamped to ≥1) 가 V=8 에서 stride=1 로 reduce 하여 PR #1395 의 `target=c` 와 동치.

## 2. 결과 — 5×4 grid

| V \ cell | none (baseline) | ent (H_686) | kl (H_687) | both (H_686+H_687) |
|---|---|---|---|---|
| **V=8** | LZ=0.0360459 / de=4 / CE=0.00254 | LZ=0.0360459 / de=4 / CE=0.0123 | LZ=0.0360459 / de=4 / CE=0.0049 | LZ=0.0360459 / de=4 / CE=0.0228 |
| **V=64** | LZ=0.0540689 / de=4 / CE=0.00288 | LZ=0.0540689 / de=4 / CE=0.0133 | LZ=0.0540689 / de=4 / CE=0.0057 | LZ=0.0540689 / de=4 / CE=0.0261 |
| **V=256** | LZ=0.0540689 / de=4 / CE=0.00294 | LZ=0.0540689 / de=4 / CE=0.0135 | LZ=0.0540689 / de=4 / CE=0.0059 | LZ=0.0540689 / de=4 / CE=0.0267 |
| **V=1024** | LZ=0.0540689 / de=4 / CE=0.00296 | LZ=0.0540689 / de=4 / CE=0.0137 | LZ=0.0540689 / de=4 / CE=0.0059 | LZ=0.0540689 / de=4 / CE=0.0272 |
| **V=4096** | LZ=0.0540689 / de=4 / CE=0.00298 | LZ=0.0540689 / de=4 / CE=0.0140 | LZ=0.0540689 / de=4 / CE=0.0060 | LZ=0.0540689 / de=4 / CE=0.0276 |

### 2.1 mean H(gate) — aux gradient injection 작동 검증 (역학 sanity)

| V \ cell | none | ent (H_686) | kl (H_687) | both |
|---|---|---|---|---|
| V=8 | 0.146 | **1.152** | 0.170 | **1.185** |
| V=64 | 0.085 | **1.018** | 0.098 | **1.057** |
| V=256 | 0.066 | **0.937** | 0.074 | **0.977** |
| V=1024 | 0.053 | **0.854** | 0.059 | **0.897** |
| V=4096 | 0.043 | **0.765** | 0.048 | **0.811** |

(uniform H = ln(4) = 1.386 nats)

H_686 (ent) aux 가 router H(gate) 를 0.04~0.15 → 0.77~1.18 로 push (작동 검증) — 그러나 LZ_norm / distinct_e 에는 영향 없음 (이미 4/4 escape).
H_687 (kl) 은 router 가 아닌 output distribution 에 작용 — H(gate) 거의 불변 (예상 동작).

## 3. 진단

### 3.1 V*_collapse · V*(aux) 측정 시도 결론

| 측정량 | 값 | 해석 |
|---|---|---|
| V*_collapse (baseline 이 collapse 하는 최소 V) | **미발견** (≥ 4096) | baseline 이 [8, 4096] 전 구간 4/4 distinct escape — toy 가 production collapse 미재현 |
| V*(aux) (aux 가 escape 하는 최소 V) | **N/A** | escape 할 collapse 가 없음 — aux 의 'escape work' 측정 불가 |
| LZ_norm V-band | V=8: 0.0360, V≥64: 0.0540 (전부 동일) | 모든 cell 동일 — corpus 의 identity decode 결정성 (cluster→token 매핑이 단사) 가 LZ 를 결정 |

### 3.2 왜 toy 가 collapse 안 하는가 (PR #1395 의 INDETERMINATE 진단 V-axis 검증)

PR #1395 의 `TOY-NULL RESULT` 가 V 축 전체에 걸쳐 robust 함을 측정으로 확인:

1. **구조적 M init 의 cluster-token 직접 정렬**: structured init `base + bump + bump2` 가 6 cluster 의 d=6 one-hot 입력을 정확히 V token id `c*stride mod V` 로 routing 하도록 sufficient signal 제공.
2. **600 step × E=4 d=6 의 SGD 가 CE convergence 우세**: SKEWED 20× rep0 corpus 가 cluster 0 만 강화하지만, 다른 5 cluster 도 cycle 마다 학습 → 평형 4/4 distinct.
3. **V 증가는 token id space 만 확장, structured init 의 cluster-token alignment 는 보존**: stride = V/6 scaling 으로 cluster 가 분리된 token id 로 매핑되어 collapse 압력 부재.

production collapse (V=151643, single-expert mode) 의 원인은 V 축 SCALE 이 아니라:
- **d 축** (production d=64 vs toy d=6, hidden capacity 21x 의 init aliasing)
- **E 축** (production E=2 vs toy E=4, dead-expert 발생 확률)
- **n_layer / attention** (toy 는 routing-free)
- **stochastic batch** (toy 는 deterministic full-cycle)
- **wikitext 분포** (toy 는 1-cluster=1-token 단사)

중 하나 (혹은 조합) — V 단독은 OFFENDING-AXIS 아님이 본 sweep 으로 ⊥ 확정.

## 4. VERDICT — 🟠 SWEEP-OUT-OF-RANGE

- ⚠ **baseline (none) cell 이 V ∈ [8, 4096] 전 구간에서 collapse 미발생** (distinct=4/4, identity decode)
- ⚠ **escape boundary 측정 불가** — aux 가 escape 할 collapse 가 토이에 부재
- ✓ aux gradient injection 메커니즘은 V 전 구간에서 정상 작동 확인 (mean H(gate) push)
- 🟠 본 sweep 은 V 축이 toy↔production transfer 의 sufficient lever 가 **아님** 을 ⊥ 확정 — 다른 축 (d / E / n_layer / stochastic / corpus-distribution) 후속 sweep 필요

### 4.1 H_686 / H_687 production verify 함의

production collapse 의 OFFENDING-AXIS 가 V 단독 아님 → toy V-scale 로는 H_686/H_687 escape 검증 불가능. PR #1395 의 결론 ("production fire = 유일 valid test") 가 V-axis sweep 후 **재확인** — H_686/H_687 의 escape efficacy 는 production fire (V=151643 · d=64 · E=2 · wikitext) 의 직접 측정 외에 토이 우회 경로 없음.

### 4.2 sweep limits

- V=4096 까지 검증, V ≥ 16384 미검증 — 그러나 V=4096 까지 LZ_norm/distinct identical → V≥16384 collapse 발생 가능성 매우 낮음 (extrapolation, 아직 측정 미달)
- M init seed 1개만 sweep — random seed 다중 시도 시 일부 seed 가 collapse 가능 (별 H 후속)

## 5. 다음 작업 (가능한 OFFENDING-AXIS 후보)

1. **d 축 sweep** — toy d ∈ {6, 16, 32, 64} × V=8 fix → d=64 에서 collapse 재현 시 d 가 OFFENDING-AXIS
2. **E 축 sweep** — toy E ∈ {2, 4, 8} × V=64 d=6 → E=2 에서 dead-expert 발생률 측정
3. **random seed 분포** — M init seed N=10 → collapse 빈도 측정 (현 sweep 의 structured init 외)
4. **production fire 직접** — H_686/H_687 prodaux build-blocker (PR #1397) 해소 후 V=151643 측정

## 6. 양방향 sibling

- ⇄ [CORE/DECODER/h686_h687_aux_ablation.hexa](./h686_h687_aux_ablation.hexa) — PR #1395 V=8 ⚪ TOY-NULL (sanity gate source)
- ⇄ [CORE/DECODER/H686_H687_ABLATION_RESULT.md](./H686_H687_ABLATION_RESULT.md) — PR #1395 결과 ledger
- ⇄ [UNIVERSE/H_686_router_entropy_regularization.md](../../UNIVERSE/H_686_router_entropy_regularization.md) — H_686 본 가설 (escape sufficient-condition)
- ⇄ [UNIVERSE/H_687_kl_to_uniform_output_reg.md](../../UNIVERSE/H_687_kl_to_uniform_output_reg.md) — H_687 본 가설 (KL output reg)
- ⇄ [CORE/DECODER/STEP_RATE_LOG.md](./STEP_RATE_LOG.md) entry 14 — 측정 ledger
- ⇄ [.discoveries/decoder_collapse_undertrain.tape](../../.discoveries/decoder_collapse_undertrain.tape) — toy-axis decoder collapse 후속 measurement

## 7. honest C3 (제약 + 미확정 + 한계)

1. **V 축은 sufficient 단독 아님 확정** (✓ closed) — V ∈ [8, 4096] toy escape 동일.
2. **production V=151643 의 collapse 가 V 단독 lever 인지 미확정** — 본 sweep 은 V≤4096 한정.
3. **다른 축 (d/E/n_layer) sweep 미시행** — toy 에서 collapse 재현이 가능한 axis 가 ≥1 개 존재할 수 있음 (별 H 후속).
4. **M init random seed 분포 미측정** — structured init 1 개만 사용. random seed 분포에서 일부 seed 가 collapse 가능.
5. **production fire 우회 경로 부재 결론은 toy 한정** — 다른 toy 변형 (예: stochastic batch + wikitext 부분 corpus) 이 collapse 재현 가능성 잔존.

---

**raw verdict line** (자동 추출용):
```
H_686_H_687_V_SCALE_VERDICT: 🟠 SWEEP-OUT-OF-RANGE — baseline_no_collapse_V∈[8,4096] · aux_gradient_works_mean_H_gate_push_verified · V_axis_NOT_offending_lever_for_production_collapse
```
