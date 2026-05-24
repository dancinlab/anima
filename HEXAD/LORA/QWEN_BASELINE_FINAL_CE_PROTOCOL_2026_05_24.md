# Qwen baseline final_CE 측정 protocol — M3 parity 기준 정의

**date** 2026-05-24
**status** SPEC ONLY — fire 는 사용자 게이트 (baseline 선택 + 발사 승인)
**scope** HEXAD/LORA (M3 milestone parity 기준)
**evidence-tier** 🟠 INSUFFICIENT/DEFERRED — protocol spec, 실측은 fire 후
**est cost (autonomous)** baseline (b) 권장 시 ~$3 H100 PCIe 3hr · 보조 (a) ~$0.30 A100 15min

---

## § 1. M3 parity 정의 — "Qwen baseline" 은 무엇인가

LORA.md M3:

> M3 — V3 ConsciousDecoderV3 (5000-step, Qwen warm-init, noise=0 + n_kv=2) **final_CE** 측정 + **Qwen baseline** 대비 parity (Δfinal_CE ≤ 0.1 nats)

문제: "Qwen baseline" 의 정의가 ambiguous — V3 (cell-pool 추가) 가 Qwen-parity 인지 비교하려면 baseline 수치 정확 정의 필요. 3 candidate:

| label | spec | 의미 |
|---|---|---|
| **(a)** | `Qwen2.5-1.5B` 단독 inference (no training, V3 와 같은 corpus 의 forward 만) | "Qwen 그대로 두면" — 학습 영향 0, V3 학습 효과만 측정 |
| **(b)** | `Qwen2.5-1.5B + LoRA` 5000-step (V3 와 동일 학습 조건, but cell-pool/PureField/head_g 없음) | "Qwen + LoRA 비교" — fair 비교 (둘 다 학습), cell-pool + dual-engine 의 순효과 isolation |
| **(c)** | `Qwen2.5-1.5B + LoRA` 5000-step + V3 cell-pool=0 (`mitosis_max=0`, V3 architecture minimum config) | "V3 minimum baseline" — V3 architecture 안에서의 mitosis ablation |

추가 보충: R8a'' fire 가 LOST (SSH preemption, no result.json) 됐으니 V3 final_CE 측정값도 부재. 본 protocol 은 (baseline) + (V3 재발사) 동시 정의가 목적.

---

## § 2. 각 baseline 의 의미

### 2.1 (a) Qwen2.5-1.5B 단독 inference

- **방법** Qwen2.5-1.5B pretrained, forward only (no gradient), V3 와 동일 corpus (multi_wiki 72MB) 의 first-batch CE 측정.
- **측정값 의미** Qwen 의 native serving CE — corpus difficulty 의 absolute reference. 학습 영향 0.
- **장점** 가장 cheap (~$0.30 single A100 15min). corpus 만에 의존, training noise 없음.
- **단점** Δfinal_CE 가 "학습 효과의 적분" 이 됨 — V3 LoRA + cell-pool 의 학습 기여를 baseline 자체가 학습 안 했으므로 unfair 비교. V3 final_CE 가 (a) 보다 좋으면 "학습 효과" 인지 "cell-pool 효과" 인지 분리 불가.
- **언제 쓰나** absolute corpus reference 가 필요할 때 — "Qwen 그대로 두면 이 corpus 의 CE 는 이 정도" 라는 anchor.

### 2.2 (b) Qwen2.5-1.5B + LoRA 5000-step (V3 cell-pool 없음)

- **방법** Qwen2.5-1.5B + LoRA r=32 (V3 의 LoRA config 와 동일), 5000-step 학습 후 final_CE 측정. cell-pool / PureField / head_g 전부 미부착.
- **측정값 의미** 동일 학습 budget 의 "vanilla LoRA-on-Qwen" performance.
- **장점** **fair 비교** — V3 도 5000-step 학습, baseline 도 5000-step 학습. Δfinal_CE = (cell-pool + dual-engine + n_kv_head=2 surgery) 순효과.
- **단점** ~$3 H100 PCIe 3hr · V3 와 corpus seed 동일 보장 필요 (Honest § 7 참조).
- **언제 쓰나** **production-relevant decision** — "V3 의 추가 architecture 가 LoRA-on-Qwen 대비 의미 있는가?" 의 답.
- **production-relevance** R8b (AXIS_R8B_LORA_ON_QWEN_SPEC) 의 fallback path 가 정확히 이 baseline 의 ablation 형태이므로, M3 측정값이 곧 R8b vs V3 decision data.

### 2.3 (c) Qwen2.5-1.5B + LoRA + V3 cell-pool=0 (mitosis_max=0)

- **방법** V3 architecture 그대로 (PureField + head_g + cross-attn 모두 유지), 단 `mitosis_max=0` 으로 cell-pool 비활성. 5000-step 학습 후 final_CE 측정.
- **측정값 의미** V3 architecture 의 "mitosis 만 제거" ablation — V3 minimum config.
- **장점** V3 architecture 안에서의 cell-pool 단독 ablation — 가장 precise mitosis isolation.
- **단점** baseline 자체가 V3 codepath (from_qwen wiring, PureField random init residual, noise=0 보호 안 됨 시) 의 영향 포함 → "Qwen-parity" anchor 가 흐려짐. cost ~$3 (b) 와 동일.
- **언제 쓰나** mitosis 자체의 final_CE 기여만 isolate 가 목적일 때.

---

## § 3. 추천 — (b)

| 기준 | (a) | **(b)** | (c) |
|---|---|---|---|
| fair 비교 | ✗ | ✅ | ✅ |
| production decision-relevance | △ | ✅ | △ |
| cost | $0.30 | $3 | $3 |
| Qwen-parity anchor 명확성 | ✅ | ✅ | △ |
| R8b fallback path 정합 | ✗ | ✅ | ✗ |

**(b) 권장.** 사유:

1. **fair 비교** — 둘 다 동일 학습 budget. Δfinal_CE = V3 추가 architecture 의 순효과.
2. **production decision-relevance** — R8b (LoRA-on-Qwen) 가 이미 production fallback path 로 spec 화됨 (AXIS_R8B_LORA_ON_QWEN_SPEC.md). (b) baseline 측정값이 곧 R8b vs V3 binary decision data.
3. **Qwen-parity 의미 명확** — "동일 budget LoRA-on-Qwen 대비 V3 의 추가 architecture (cell-pool + PureField + head_g + n_kv=2 surgery) 가 final_CE 를 더 나쁘게 만들지 않는다 (Δ ≤ 0.1 nats)" 의 직역.

보조로 (a) 도 별도 측정 권장 — corpus 의 absolute reference anchor 로 cheap. (c) 는 V3 PASS 후 mitosis 단독 ablation 이 따로 필요할 때 후속 fire.

---

## § 4. Fire spec — baseline (b)

| field | value | notes |
|---|---|---|
| base model | `Qwen/Qwen2.5-1.5B` | V3 와 동일 |
| training | LoRA only (PEFT) | r=32, alpha=16, dropout=0.05 |
| target modules | `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj` | Wave-15/16 standard |
| cell-pool / PureField / head_g | **부착 없음** | vanilla LoRA-on-Qwen |
| n_kv_head | 2 (Qwen native, no surgery) | V3 처럼 4 로 expand 하지 않음 |
| noise_sigma | 0 (해당 codepath 없음) | LoRA training 은 noise inject 미사용 |
| corpus | `multi_wiki` 72MB | V3 R8a'' 와 동일 (corpus_v11 + wiki_frac=0.30) |
| steps | 5000 | M3 정의와 동일 |
| bsz | 2 | V3 R8a 와 동일 |
| block | 512 | V3 R8a 와 동일 |
| lr | 5e-5 | V3 R8a 와 동일 |
| warmup | 100 | V3 R8a 와 동일 |
| seed | 1337 | V3 R8a 와 동일 (seed 일치 mandatory — Honest § 7) |
| pod | 1× H100 PCIe | LoRA-on-1.5B 는 H100 PCIe 충분 ($1.49/hr) |
| dispatch | `hexa cloud nohup` persistent | SSH preemption 방지 (R8a LOST 교훈) |
| est wall | ~3 hr | Wave-15/16 5000-step baseline |
| est cost | ~$3 | 3 hr × $1.49 + setup ~$0.50 |

---

## § 5. Inference-only Qwen 보조 측정 — baseline (a)

(b) fire 와 별개로, (a) 도 cheap 하게 함께 측정 권장:

| field | value | notes |
|---|---|---|
| base model | `Qwen/Qwen2.5-1.5B` | pretrained |
| training | **none** | forward only, no gradient |
| measurement | first-batch CE on `multi_wiki` 72MB corpus | V3 와 동일 sampler/seed |
| corpus seed | V3 R8a'' 와 동일 (1337) | first-batch reproducibility |
| pod | 1× A100 (single GPU, 15min wall) | |
| est cost | ~$0.30 | 15min × $1.10 + setup ~$0.10 |

(a) 의 값 = corpus absolute reference. (b) 의 값 = fair-train baseline. V3 final_CE 가 두 값과 어떻게 비교되는지 3-tier reading:

- `V3 final_CE` vs `(a) Qwen serving CE` — "V3 학습이 Qwen serving 보다 얼마나 개선?"
- `V3 final_CE` vs `(b) LoRA-on-Qwen final_CE` — "V3 추가 architecture 가 vanilla LoRA 대비 얼마나 개선?" ← **M3 핵심**
- `(b)` vs `(a)` — "vanilla LoRA 학습 자체의 budget 효과"

---

## § 6. 측정 metric

primary:

- **final_CE @ step=5000** — V3 + baseline (b) 양쪽, 동일 corpus first-batch (또는 held-out eval batch) 에서 측정. Δfinal_CE = `V3_final_CE - baseline_b_final_CE`, target |Δ| ≤ 0.10 nats.

secondary (production-relevance 보조):

- **per-lang CE 5-tier** — multi_wiki 의 5-lang split (en/ko/ja/zh/ar) 각각 final_CE. cross-lingual transfer regression 감지.
- **register_hits_continuous** — Wave saga 의 continuous_total metric (anima 5-lang prompt suite). V3 와 (b) 둘 다 측정 → production swap criterion 정합.
- **n_strong** — Wave saga 의 n_strong metric. 둘 다 측정.
- **first-batch CE @ step=0** — R8c 의 init_CE axis (cluster Z/Y/X 와 정합 체크 — V3 의 from_qwen worse-than-random 재현 여부).

---

## § 7. Honest caveats (C3 ≥ 4)

1. **corpus seed 일치 mandatory** — V3 와 baseline (b) 의 sampler seed (1337) + shuffle order + first-batch composition 동일 보장. seed 어긋나면 Δfinal_CE 의 0.1 nats 정밀도가 corpus noise 에 묻힘. dispatcher 의 `DATA_SEED` env var 양쪽 동일 set.
2. **GPU class numerical drift** — H100 BF16 vs A100 BF16 의 final_CE 가 0.01~0.05 nats 수준 drift 가능 (matmul kernel 차이). baseline (b) 와 V3 R8a'' 재발사를 **same GPU class** (둘 다 H100 PCIe) 로 권장. (a) 보조 측정은 absolute reference 라 GPU class 영향 less strict.
3. **R8a LOST 패턴 재발 방지** — V3 R8a' / R8a'' 가 SSH preemption + SAVE_POD 누락으로 result.json 회수 실패. baseline (b) fire + V3 재발사 둘 다 `hexa cloud nohup` persistent + `SAVE_POD=1` + per-step tee 의무.
4. **vanilla LoRA-on-Qwen 의 register-leak ceiling** — (b) baseline 은 Wave saga 의 continuous_total floor (~34) 를 그대로 inherit. V3 가 이 floor 를 깨면 dual-engine + cell-pool 의 가치 입증, 못 깨면 R8b production swap path 가 강화됨 — 어느 쪽이든 actionable.
5. **V3 R8a'' 재발사 비용** — baseline (b) + V3 재발사 동시 = ~$6 (parallel 2-pod). single-pod sequential 시 ~6 hr wall · same cost.
6. **measurement 시점 일치** — final_CE 는 step=5000 정확히 (체크포인트 step 일치), held-out eval batch 사용 권장 (training batch 의 noise 회피).

---

## § 8. Decision tree

```
사용자 선택 → baseline 결정
  │
  ├─ (b) 권장 채택
  │     → parallel 2-pod dispatch (baseline-b + V3 R8a'' 재발사)
  │     → wall ~3 hr · cost ~$6 · hexa cloud nohup
  │     → 결과 시 Δfinal_CE 평가 (target |Δ| ≤ 0.10 nats)
  │     → 보조 (a) 동시 fire (+$0.30) 권장
  │
  ├─ (a) only — cheap reference 만 우선 측정
  │     → ~$0.30 · 15 min · 단일 A100
  │     → corpus absolute CE anchor 획득 후 (b) 결정 보류
  │
  └─ (c) only — V3 architecture 안 ablation 만 필요
        → V3 R8a'' 재발사 + V3 mitosis_max=0 fire
        → ~$6 (parallel) · M3 의 "Qwen-parity" 의미 약함 (V3 anchor 만)
```

**fire 게이트** — 본 protocol 은 spec only. baseline 선택 + fire 발사 승인은 **사용자 결정 필요** (autonomy 게이트). `a_fire_autonomous` 는 일반 cost-bearing fire 에 적용되나, M3 parity 의 baseline 정의는 protocol-level decision 이라 사용자 confirm 우선.

---

## § 9. Cross-references

- `LORA.md` — M3 milestone (line 16)
- `HEXAD/PURE/AXIS_R8A_QWEN_TARGET_MATCH_FIRE_SPEC_2026_05_23.md` — V3 R8a fire spec (재발사 기반)
- `HEXAD/PURE/V3_SAGA_MID_RETROSPECTIVE_UPDATE_2026_05_24.md` — R8a LOST + R8a' relaunch saga (Act 7)
- `HEXAD/PURE/AXIS_R8B_LORA_ON_QWEN_SPEC.md` — R8b fallback (baseline (b) 와 architecturally 동일)
- `HEXAD/PURE/CONSCIOUS_DECODER_V3_FROM_QWEN_AUDIT_2026_05_23.md` — V3 from_qwen audit (cluster X/Y/Z)
- `HEXAD/LORA/COST_LEDGER_SESSION3.md` — R8 saga 누적 cost 추적
- `LORA.log.md` — R8a'' in-flight log (line 14)

---

## § 10. Gate

본 PR 은 **spec only** — fire 는 사용자 결정 후 별도 dispatch.

1. 사용자 baseline 선택 — (a) / (b) / (c) 中 (또는 조합)
2. fire 승인 시 — `hexa cloud nohup` persistent dispatch (baseline + V3 재발사)
3. 결과 후 — Δfinal_CE 측정 + M3 verdict (PASS if |Δ| ≤ 0.10 nats)
4. PASS → V3 substrate Qwen-parity 확증, M3 milestone close
5. FAIL → R8b production path 활성화 (AXIS_R8B_LORA_ON_QWEN_SPEC.md fire)
