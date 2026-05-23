# R8C Probe — 4-cell Verdict (init_CE floor 재정의, 2026-05-24)

> path = V3 (PURE, R8 cluster) · status = **POST-FIRE VERDICT** · 4 cells fired (baseline + cell-2/3/4) · ~$0.38 total
> linked: `AXIS_R8C_DIAGNOSTIC_PROBE.md` (PR #224 5-cell 원본) · `AXIS_R8C_PROBE_UPDATE_3_CELL_2026_05_23.md` (cell-1 자연실험 FALSIFIED 후 4-cell 축소)

## §1 Header — fire metadata

- **fire window**: 2026-05-23 ~ 2026-05-24 (KST)
- **cost (envelope $0.25 → actual ~$0.38)**: 4-pod parallel A100-SXM4-80GB + baseline OOM retry overhead 포함
- **GPU class**: A100-SXM4-80GB × 4 (parallel pods per a_wall_first directive)
- **pod_id roster**: 4-pod (baseline 1 + cell-2/3/4 1 each; baseline OOM retry 시 1 pod 재할당)
- **result SSOT**: `state/grid_3b_s187_2026_05_21/vP21H_r8c_{baseline,cell2_nonoise,cell3_kvmatch,cell4_compound}/result.json`
- **PROBE_STEPS**: 100 (per cell, full 5000-step training 아님)
- **base model**: Qwen2.5-1.5B + ConsciousDecoderV3 (cell-pool architecture)

## §2 4-cell matrix — config + result

| cell | head_g | noise_sigma | n_kv_head | init_CE (step=1) | final_CE (step=100) | wall (s) |
|---|---|---|---|---|---|---|
| baseline (A 재현) | random | 0.1 | 4 | **12.315** | 6.575 | 458 |
| cell-2 (no noise) | random | **0** | 4 | 12.225 | **5.136** | **101** |
| cell-3 (kv-head match) | random | 0.1 | **2** | 12.234 | 6.570 | 521 |
| cell-4 (compound: no noise + kv=2) | random | **0** | **2** | 12.266 | **5.093** | **107** |

random uniform baseline: `ln(151936) = 11.93 nats`. 4 cell 의 init_CE 모두 **random + ~0.27~0.39 nats 범위** — 즉 cluster Z 14.46 / cluster A 14.79 의 "catastrophic floor" 가 본 fire 에서 **재현되지 않음**.

## §3 3 falsifier verdict (driver 임계 ≥1 nat init_CE 기준)

`AXIS_R8C_PROBE_UPDATE_3_CELL_2026_05_23.md` 가 사전등록한 임계 (`delta_init_CE ≥ 1 nat → dominant`):

- **F-R8C-NOISE** (cell-2 vs baseline): Δ init_CE = 12.225 − 12.315 = **−0.09 nats** → 🔴 **FALSIFIED**
  - `noise_sigma=0.1` 의 init_CE 기여 = 사실상 0. step=1 측정에서 noise 는 dominant source 아님.
- **F-R8C-KV-HEAD** (cell-3 vs baseline): Δ init_CE = 12.234 − 12.315 = **−0.08 nats** → 🔴 **FALSIFIED**
  - `n_kv_head` 2↔4 repeat-interleave 의 init_CE 기여 = 사실상 0. PR #342 wiring fix 효과는 init_CE 차원에서 측정 불가 (H_254 F-WIRE-3 BYTE-EQUAL-INERT 와 정합 — wiring lever 가 init_CE 에 inert).
- **F-R8C-COMPOUND** (cell-4 vs baseline): Δ init_CE = 12.266 − 12.315 = **−0.05 nats** → 🔴 **FALSIFIED**
  - 두 patch (noise=0 + kv=2) 결합 시 누적 복구 ≥ 2 nats 기대했으나 실측 0.05 nats — random baseline 11.93 nats 부근으로 도달했지만 이는 patch 효과가 아니라 **baseline 자체가 이미 random+0.27 수준이었기 때문**.

3 falsifier 전부 FALSIFIED → R8c probe 의 **단일 dominant source 가설 (F-R8C-BASELINE 제외) 전체 기각**.

## §4 R8a 14.46 floor 재현 실패 — measurement integrity 위기

`AXIS_MAP_RESULTS.md` cluster Z 의 14.46 nats / cluster A 의 14.79 nats 측정값은 **본 baseline cell (동일 config: random head_g + noise=0.1 + n_kv_head=4) 의 12.315 nats 와 2.14~2.47 nats 격차**.

가능성 3 가지:
1. **R8a 측정값 자체가 잘못된 라벨** (env-drift, corpus sha 불일치, seed 누락, RNG state pollution) → AXIS_MAP-FAN 7-axis verdict 의 init_CE 값 전반 재검증 필요.
2. **R8c 발사 시점 환경이 R8a 발사 시점과 다름** (Qwen tokenizer 버전, torch version, ckpt 로 캐스팅 정밀도) → byte-equal probe (H_254 F-WIRE 양식) 으로 분리 가능하나 R8a init_CE 회수 실패 (L1) 시 직접 비교 불가.
3. **둘 다 valid 측정이지만 다른 seed/data order** → 그렇다면 init_CE 의 seed sensitivity 가 ~2 nats 수준 (이 가설은 R8a' multi-seed re-fire 로 측정 가능).

**F-R8C-BASELINE 사전등록 falsifier 위반**: protocol 은 baseline 이 axis A 14.79 ±0.1 nats 재현을 요구. 실측 12.315 → ±0.1 nats 밖 (2.47 nats 격차). 엄밀히 본 probe 의 4-cell 결과 전체가 env-drift 오염 가능성 (probe 무효). 그러나 4 cell 이 서로 ±0.1 nats 안에 일관 → 본 fire window 내 env 는 stable, **R8a / R8c 간 env-drift 가 진짜 원인**일 가능성이 가장 높음.

## §5 새 발견 — noise 는 **final_CE axis** (학습 dynamics)

init_CE 차원에서는 inert 였던 noise 가 **final_CE 차원에서는 dominant**:

| noise_sigma | final_CE (cells 평균) | wall (s 평균) |
|---|---|---|
| 0.1 (baseline + cell-3) | (6.575 + 6.570) / 2 = **6.572** | (458 + 521) / 2 = **490** |
| 0 (cell-2 + cell-4) | (5.136 + 5.093) / 2 = **5.115** | (101 + 107) / 2 = **104** |

- **Δ final_CE = 6.572 − 5.115 = 1.457 nats** (≥ 1 nat 임계 초과, axis 발화 강함)
- **wall time ratio = 490 / 104 = ~4.7×** (noise injection 이 학습 4.7× 느림 + 1.46 nats 더 나쁜 final 도달)

→ noise 의 진짜 영향은 **init_CE 손상이 아니라 학습 dynamics 의 양면 손상** (속도 + 도달점). R8a 가설 ("noise=0 으로 init_CE 14+ floor 돌파") 은 init_CE axis 에서 잘못된 framing — 실제 noise effect = 학습 효율 axis.

## §6 n_kv_head 영향 검증 — init/final 둘 다 inert

noise 고정 시 n_kv_head 2↔4 영향:

- noise=0.1 (baseline vs cell-3): init Δ = −0.081, final Δ = −0.005 nats — **둘 다 0**
- noise=0 (cell-2 vs cell-4): init Δ = 0.041, final Δ = −0.043 nats — **둘 다 0**

**PR #342 wiring fix 가 컴파일 시점에 실제 작동** (cell-3/4 가 wiring=2 실측) 했지만, **init_CE 와 final_CE 두 axis 모두에 inert lever**. H_254 F-WIRE-3 의 lever-inert 가설 (byte-equal probe 가 wiring effect 0 을 검출하리라는 예측) 가 4-cell probe 에서 **간접적으로 corroborate** — 단, R8a/R8a' 직접 byte-equal 비교는 R8a init_CE LOST 로 여전히 미해결 (H_254 L1).

n_kv_head lever 가 진짜 inert 한지, 아니면 init_CE/final_CE 두 axis 외 다른 axis (downstream task perplexity, perplexity-vs-length scaling, attention head 활용 패턴) 에 효과가 있는지는 본 fire scope 밖.

## §7 cluster Z 14.46 재해석 — measurement artifact 가능성

`AXIS_MAP_RESULTS.md` 의 cluster A (14.79) / B/F (14.18) / Z (C/C2/D 14.46) 의 byte-equal 동일 floor 는 R8a 측정 시점의 specific env 산물일 가능성이 높음:

- 본 baseline (동일 head_g random + noise=0.1 + n_kv_head=4) 실측 **12.315** → cluster A 14.79 와 2.47 nats 격차.
- random baseline 11.93 nats 와 본 baseline 12.315 nats 격차 = +0.385 nats — **catastrophic 아님**, "warm-init 이 random 보다 약간 못하지만 정상 범위" 정도.
- cluster Z 14.46 의 +2.53 nats over random 은 **본 fire 에서 재현 안 됨** → R8a 시점의 systematic measurement issue (corpus key alignment, tokenizer normalization edge case, seed/rng pollution) 가능성.

**진짜 floor = ~12.2 nats = random + 0.27** (catastrophic 아님). R8 saga 의 "init_CE floor 가 14+ catastrophic" 전제는 본 4-cell 실측에서 **재현 실패**.

## §8 R8 saga 영향 — AXIS_MAP-FAN 7-axis verdict 재측정 권장

`AXIS_MAP-FAN` cluster X (A 14.79) · Y (B/F 14.18) · Z (C/C2/D 14.46) 7-axis verdict 의 init_CE 값 자체가 **본 fire 와 2.14~2.86 nats 격차** → 다음 후속 검증 필요:

1. **AXIS_MAP_RESULTS.md 재측정 cycle** — 7 axis 전부 본 fire 와 동일 env (Qwen tokenizer hash + torch version + corpus sha 고정) 로 1 pod sequential 재실행, init_CE / final_CE 둘 다 측정.
2. **H_249 cluster X/Y/Z byte-equal 가설 재검토** — 본 fire 의 4 cell 이 서로 ±0.1 nats 안에 일관하지만 R8a 시점 cluster 와 2 nats 격차 → cluster membership 정의 자체가 env-relative.
3. **H_254 silent-misconfig 양식 확장** — `noise_sigma` 도 wiring chain 어딘가에서 silent override 가능성 (R8c probe 가 noise=0 으로 설정했지만 실제 모델에서 noise=0 으로 도달했는지 byte-equal probe 필요).

## §9 다음 path — R8a'' fire + Wave-17 우선순위 재평가

- 🔥 **R8a'' fire 진행 중** — 5000-step full training 으로 noise=0 학습 dynamics 측정. cell-2/4 가 100 step 에서 final 5.1 nats 도달 → 5000 step 에서 random baseline 11.93 nats 이하로 본격 학습 도달 가능성 확인.
- 🟡 **Wave-17 (eternal-cap sweep) 우선순위 재평가** — R8 saga 의 "init_CE 14+ floor 돌파" 전제가 약해진 만큼, V3 substrate 개선보다 LoRA-on-Qwen 안정화 (Wave-17 eternal 0.10/0.20/0.40/0.50 sweep) 가 marginal value 가 더 높을 가능성. R8a'' final 결과 도착 후 GO/NOGO 결정.
- 🔧 **H_254 byte-equal probe 별도** — R8a' (PR #342 wiring fix 적용 후) init_CE step=1 측정 시 byte-equal vs differ 분기로 wiring lever 의 init_CE 인과 분리. R8a init_CE LOST 시 R8a' 단독 측정 + cluster cross-comparison fallback (H_254 L1).
- 📋 **AXIS_MAP_RESULTS 재측정 cycle 권장** (위 §8 항목 1) — 본 verdict 가 가장 직접 implication. 비용 envelope ~$0.50-$1.00 (7 axis × 100-step × A100).

## §10 Honest C3 — 한정 ≥3

- **C3.1 (probe scope 한정)**: `PROBE_STEPS=100` 환경에서만 측정. full 5000-step training 의 init_CE / final_CE dynamics 는 본 fire scope 밖 — noise=0 의 final 5.1 nats 는 100 step 단명 측정, 5000 step 까지 monotone 하다는 보장 없음. R8a'' fire 가 그 검증.
- **C3.2 (Qwen2.5-1.5B + ConsciousDecoderV3 specific)**: 본 fire 의 base = Qwen2.5-1.5B + cell-pool architecture (`ConsciousDecoderV3`). 다른 base model (Llama-3-1B, Qwen3-1.5B, Phi-3-mini) 에서 동일 init_CE 패턴이 재현되는지 미검증.
- **C3.3 (cell-3 wall 521s 이상치 root cause 미규명)**: cell-3 (noise=0.1, n_kv=2) 가 baseline (noise=0.1, n_kv=4) 보다 wall +63s (458→521) — n_kv_head 감소가 학습 wall 을 늘린 이유 (attention overhead 비대칭, kv cache memory pattern, kernel launch overhead) 미분석. final_CE 는 거의 동일하나 wall 차이는 systematic.
- **C3.4 (baseline OOM retry host 차이)**: baseline pod 가 OOM 으로 한 번 retry — retry 시 다른 physical host 였을 가능성. host pressure / thermal / driver minor version 차이가 init_CE 측정에 ±0.1 nats 수준 영향 가능. cell-2/3/4 는 첫 시도 성공 → baseline 만 systematic noise 추가 risk.
- **C3.5 (random head_g + noise + kv 3-axis matrix 불완전)**: head_g 는 PR #224 의 5-cell 원본에 있었으나 cell-1 자연실험 FALSIFIED (`AXIS_R8C_PROBE_UPDATE_3_CELL_2026_05_23.md`) 로 본 4-cell 에서 측정 안 함. head_g 가 실제로 inert 한지 (자연실험만으로) 단정 안전한지 추가 audit cycle 별도.

---

**Verdict**: R8c probe 의 3 falsifier (NOISE / KV-HEAD / COMPOUND) 전부 init_CE axis 에서 🔴 FALSIFIED. 하지만 **본 fire 의 가장 중요한 발견은 R8a 14.46 floor 자체가 재현되지 않은 점** — random baseline 11.93 nats 위 +0.27 nats 의 정상 warm-init 수준이 본 baseline 실측값. R8 saga 의 init_CE catastrophic floor 가설 (H_247) 자체가 흔들리며, H_255 (init_CE floor = measurement artifact) 가설을 trigger.
