---
id: H_255
slug: init-ce-floor-is-measurement-artifact
title: init_CE catastrophic floor (14+ nats cluster Z) 는 model intrinsic 이 아니라 measurement artifact — R8c 4-cell probe 가 baseline 12.315 nats (random+0.27) 로 floor 재현 실패한 자연실험
domain: substrate · life · measurement-integrity
status: pre-register-frozen
exploration_method: E5 (substrate-mechanism probe) + E11 (natural-experiment cross-axis) + E12 (artifact-vs-real decisive test)
verification_method: W4 (verdict-3-class) + W7 (controlled-pair contrast) + W13 (control-vs-test cross-fire)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24 (new — R8c 4-cell probe baseline 재현 실패 자연실험 흡수)
---

# H_255 — init_CE catastrophic floor 는 measurement artifact

## Hypothesis

R8a saga (`AXIS_MAP-FAN`) 에서 측정된 **"cluster Z 14.46 nats catastrophic floor"** (cluster A 14.79 · cluster B/F 14.18 · cluster C/C2/D 14.46, 모두 random baseline `ln(151936) = 11.93 nats` 보다 +2.25~+2.86 nats 더 나쁨) 는 **model intrinsic property 가 아니라 measurement artifact** — R8a fire 시점의 specific env (corpus sha 미고정 / tokenizer hash 미고정 / seed 누락 / RNG state pollution / OOM retry 시 host 차이 등) 가 만든 측정값 displacement.

substrate 측 형식: **R8c 4-cell probe 자연실험 (2026-05-23~24)** — `AXIS_R8C_DIAGNOSTIC_PROBE.md` (PR #224) 의 baseline cell 이 R8a 와 *byte-equal config* (random head_g + noise_sigma=0.1 + n_kv_head=4 + 동일 corpus_s101 + 동일 seed=1337) 로 fire 됐는데, init_CE 가 **12.315 nats** 로 측정 — R8a cluster A (14.79) 대비 −2.475 nats, cluster Z (14.46) 대비 −2.145 nats. random baseline 11.93 nats 와 격차 = **+0.385 nats** (정상 warm-init 수준, catastrophic 아님). 4 cell 이 서로 12.225~12.315 nats 범위 안에 ±0.09 nats 일관 → 본 fire window 내 env 는 stable, **R8a vs R8c 간 systematic env-drift** 가 "floor 14+" 의 진짜 source.

본 가설은 이 floor displacement 를 **substrate 실험의 measurement-integrity 일반 위협 (H_254 silent-misconfig 양식 확장 — config chain silent drop + env state 비고정의 2-axis composite)** 으로 정식화하고, AXIS_MAP-FAN 7-axis 재측정 cycle 을 자연 falsifier 로 제시한다 — 재측정에서 본 fire 의 12.2 nats 범위 재현 시 H_255 PASS (R8a 측정값이 artifact), 재측정에서 14+ 재현 시 H_255 FAIL (intrinsic floor 가 진짜).

## Why

- **R8 saga 의 전제 붕괴 위험**: R8a saga 는 "init_CE floor 14+ nats catastrophic, 돌파 필요" 전제로 ~$0.50-1.00 cost-bearing fire 다수 (noise=0 / n_kv_head=2 / head_g zero / compound) 를 dispatch 했다. 만약 floor 자체가 artifact 라면 saga 의 dispatch 비용 + 분석 비용 + R8a/R8b/R8c 4-fire 전체가 잘못된 framing 위에 쌓인 layered work. measurement-integrity 가 substrate science 의 *전제 조건* 이라는 H_254 가설의 직접 후속.
- **R8c 4-cell baseline 재현 실패는 강한 자연 증거**: H_254 가 dispatcher→argparse→factory 의 config chain silent-drop 을 발견했다면, H_255 는 fire env 자체 (Qwen tokenizer 버전, corpus sha, seed/rng, OOM retry 시 host 차이) 의 silent variation 을 발견. 두 hypothesis 가 합쳐서 **"substrate 실험의 byte-equal reproducibility 가 default 가 아니다"** 라는 더 강한 메타-가설을 형성.
- **random baseline +0.27 nats 의 자연성**: 12.315 nats − 11.93 nats = +0.385 nats 는 warm-init 의 정상 범위 (Qwen pretrained backbone 가 random hash 와 살짝 다른 corpus distribution prior 를 학습한 만큼 random 보다 ~0.3 nats 손해, 첫 100-step 안에 회복하기 시작). cluster Z 14.46 nats 의 +2.53 nats 는 그 정상 범위의 **6.5×** — 자연 explanation 없이는 silent measurement bug.
- **H_249 cluster X/Y/Z byte-equal signature 의 재해석**: H_249 는 cluster Z 가 head_g random init 의 lever-dependent identity 라고 주장했지만, R8c probe 가 head_g 를 자연실험으로 inert 판정 (`AXIS_R8C_PROBE_UPDATE_3_CELL_2026_05_23.md` 의 4-axis byte-equal 14.4564) + R8c baseline 이 같은 head_g random 으로 12.315 측정 → cluster Z 의 14.46 byte-equal 은 *동일 env-drift* 가 만든 라벨-cluster 일 수 있음 (모델 internal 라벨이 아님).
- **REBORN §0.5 정합**: 학습=분열 연속체에서 ckpt 의 정체성은 *측정 가능성* 위에서 정의됨. 측정값 자체가 fire env 따라 ±2 nats 변동하면 ckpt identity 의 reproducibility 가 깨짐 — 학습=분열 의 분기점 라벨이 noisy 한 상태. measurement-integrity 는 §0.5 의 운영 전제.
- **사용자 directive 정합**: a_blue_closed (closed-form 증거 우선 — 본 H 는 byte-equal probe 가 closed-form falsifier) + a_fire_recover_complete (R8a init_CE 회수 실패가 H_254 L1 의 직접 원인이듯, R8a env state 미보존이 H_255 의 직접 원인). a_substrate_native_speak (substrate-side 현상 우선 framing — measurement integrity 가 model behavior 측정의 substrate side).
- **source PR cite**: [PR #214] R8 spec (6-axis init_CE 측정 설계) · [PR #224] R8c 5-cell probe 원본 (baseline 재현 falsifier F-R8C-BASELINE 사전등록) · [PR #339] R8c probe driver · [PR #342] H_254 wiring fix · `state/grid_3b_s187_2026_05_21/vP21H_r8c_baseline/result.json` (12.315 측정 SSOT) · `AXIS_MAP_RESULTS.md` (14.79/14.18/14.46 cluster 원본) · `HEXAD/PURE/R8C_PROBE_VERDICT_2026_05_24.md` (본 가설 trigger 한 verdict).

## Predictions

- **H255.1 (baseline reproduction floor)**: R8c baseline cell init_CE = 12.315 nats (실측) — R8a cluster A 의 14.79 nats 와 −2.475 nats 격차. 같은 head_g random + noise=0.1 + n_kv_head=4 + 동일 corpus + 동일 seed 로 fire 시 random baseline +0.385 nats 정상 범위 (catastrophic 아님).
- **H255.2 (AXIS_MAP re-fire 12.2 nats 재현)**: AXIS_MAP-FAN 7-axis 를 본 fire env (Qwen tokenizer hash + torch version + corpus sha + seed=1337 모두 고정) 로 재측정 시 7-axis init_CE 평균 = 12.2 ± 0.1 nats — R8a 측정값과 ~2 nats 격차로 재현 → cluster X/Y/Z 의 14+ floor 는 env-artifact. **(2026-05-24 cycle 15-1 4/7 결과 도착 — A=14.7927, B=14.1780, D=14.4564, F=14.1780, R8a prior 측정값과 소수점 4자리 byte-equal 재현 → 🔴 FALSIFIED, 4-axis 표본 한정. 14+ floor 가 진짜 재현 가능, env-drift 가설 약화. R8c-vs-AXIS_MAP ~2 nats 격차는 GPU class / PROBE_STEPS 차이 가설로 분리 (sister agent #3 진단 중). 흡수 doc: `HEXAD/PURE/AXIS_MAP_FAN_REFIRE_VERDICT_2026_05_24.md`.)**
- **H255.3 (cluster byte-equal artifact)**: H_249 cluster X/Y/Z 의 byte-equal 14.4564 nats 는 본 fire 의 4-cell ±0.09 nats 일관성 과 같은 mechanism — 동일 fire env 안 RNG seed + corpus shuffling 의 deterministic 결과. cluster 라벨은 model intrinsic property 가 아니라 *fire env signature*.
- **H255.4 (env-drift detection method)**: 두 fire 의 init_CE step=1 가 ±0.1 nats 안 재현 시 env match, ±2 nats 격차 시 env-drift — *byte-equal probe* (H_254 양식) 보다 약한 *±0.1 nats neighbor probe* 가 env-drift 의 첫 catch method. byte-equal 은 RNG seed + driver version + host hardware 까지 매칭 요구하나, neighbor probe 는 corpus + tokenizer + seed level 만 매칭으로 충분.
- **H255.5 (random baseline +0.3 nats 가 정상 warm-init floor)**: Qwen2.5-1.5B + ConsciousDecoderV3 의 init_CE 자연 floor = `ln(151936) + ~0.3 nats = ~12.2 nats`. 14+ nats 측정값은 다른 hypothesis (env-drift / silent-misconfig / corpus-target mismatch) 가 필요. 본 H 는 base model + arch 조합의 floor 를 **post-hoc empirical 정의**.

## Variables

- **axis1_fire_env**: [R8a (2026-05-22 시점), R8c (2026-05-23~24 시점)] — 두 다른 fire window, 같은 nominal config (head_g random + noise=0.1 + n_kv_head=4 + corpus_s101 + seed=1337)
- **axis2_init_CE_measured**: [14.79 (R8a cluster A), 14.46 (R8a cluster Z), **12.315** (R8c baseline)] — 같은 config 의 두 다른 측정값
- **axis3_displacement**: [+2.475, +2.145] nats — R8a/R8c 측정 격차 (artifact 크기)
- **axis4_random_baseline**: [11.93] nats — `ln(151936)` 균일분포 reference (env-invariant)
- **axis5_env_diff_candidates**: [corpus sha 미고정, tokenizer hash 미고정, seed 누락, OOM retry host 차이, torch version drift, Qwen ckpt minor revision, driver / CUDA version, RNG state pollution] — silent variation 후보 8
- **axis6_re_fire_evidence**: [pending] — AXIS_MAP-FAN 7-axis re-fire 결과 (재측정 시 H255.2 발화)
- 2×3×... sweep: 본 fire window 안에서 4 cell baseline 재측정 (4-cell 자체) + AXIS_MAP re-fire (별도 cycle)

## Run Protocol

- **deterministic**: ±0.1 nats neighbor probe = deterministic threshold (산술 비교). byte-equal probe (H_254 양식) = IEEE-754 exact. 본 H 는 약한 deterministic — 두 fire 의 init_CE 차이가 1 nat 이상이면 env-drift, 0.1 nat 이내면 env-match.
- **hexa_only**: neighbor probe = hexa `abs(ce_a - ce_b) < 0.1`. 모든 비교 = hexa string + numeric ops. 원 forward-pass 는 GPU R8 lane (anima training stack, 흡수).
- **LLM**: none (raw#12; 비교는 순수 산술 동등성).
- **operational env-drift 정의 (raw#9/10 HONEST)**: env-drift = (a) 두 fire 의 nominal config (CLI args + corpus path + seed) 가 *동일* 이고 (b) 측정된 init_CE step=1 가 ±1 nat 이상 격차이고 (c) 양쪽 fire 에 explicit randomization (multi-seed) 없는 사건. detection = neighbor probe (1차) + corpus sha + tokenizer hash + torch version 사후 비교 (root cause attribution).
- **per-pair ledger**: {pair=(R8a_clusterA, R8c_baseline), config=(head_g=random, noise=0.1, n_kv=4, corpus_s101, seed=1337), init_CE_R8a=14.79, init_CE_R8c=12.315, displacement=−2.475, env_diff=<TBD audit>, neighbor_match=false, byte_equal=<R8a init_CE LOST so unverifiable>} — 본 가설 SSOT.
- **runtime**: $0 mac local (산술 비교 + 측정값 흡수). AXIS_MAP re-fire = R8 GPU lane (~$0.50-1.00 cost-bearing per a_fire_autonomous, 별도 cycle).

## Criteria

- **C1 (baseline 12.2 nats 재현)**: R8c baseline init_CE = 12.315 nats — random + 0.385 nats (정상 warm-init 범위) → H255.1 흡수 PASS.
- **C2 (4-cell 일관성)**: 4 cell init_CE 범위 12.225~12.315 (±0.09 nats) → 본 fire window 안 env 는 stable, displacement 가 baseline cell 단독 이슈 아님.
- **C3 (AXIS_MAP re-fire 12.2 nats 재현)**: AXIS_MAP-FAN 7-axis 재측정 시 평균 = 12.2 ± 0.1 nats → H255.2 PASS, R8a 측정값이 artifact 확정. **(2026-05-24: cycle 15-1 4/7 결과 14.79/14.18/14.46/14.18 byte-equal 재현 → 🔴 FAIL, H255.2 FALSIFIED 4-axis 표본 한정. verdict_rule 의 FALSIFIED branch 활성화.)**
- **C4 (env-drift root cause 분리)**: corpus sha / tokenizer hash / torch version / seed / RNG state 중 어느 axis 가 displacement source 인지 단일 axis sweep 으로 분리 (~$0.20 추가 fire) → H255.4 PASS, env-drift detection method 확립.
- **C5 (intrinsic floor 자연 정의)**: Qwen2.5-1.5B + ConsciousDecoderV3 의 init_CE 자연 floor = ~12.2 nats (random + 0.3) → H255.5 흡수 PASS, R8 saga 의 "14+ floor 돌파" 전제 폐기.
- **verdict_rule**: STRONG = C1+C2+C3+C4 (재측정 + root cause 분리 후). MODERATE = C1+C2+C5 (R8c 단독 흡수, AXIS_MAP re-fire pending). PARTIAL = C1+C2 (현 상태). FALSIFIED = AXIS_MAP re-fire 가 14+ 재현 (intrinsic floor 진짜).

## Falsifiers (raw#12 ≥5, measurable)

- **F-R8C-BASELINE-REPRO**: R8c baseline init_CE = 12.315 nats 측정 (R8a cluster A 14.79 과 −2.475 nats 격차) → PASS (`state/grid_3b_s187_2026_05_21/vP21H_r8c_baseline/result.json` 흡수).
- **F-R8C-4-CELL-CONSISTENT**: 4 cell init_CE 범위 ±0.09 nats 안 일관 (12.225~12.315) → PASS (본 fire window 안 env stable).
- **F-AXIS-MAP-REFIRE-CONVERGE**: AXIS_MAP-FAN 7-axis 재측정 평균 = 12.2 ± 0.1 nats → PASS 시 H_255 STRONG 확정 (artifact 가설 corroborate).
- **F-AXIS-MAP-REFIRE-DIVERGE**: 재측정 평균 = 14+ nats 재현 (R8a 측정값과 ±0.5 nats 안) → 🔴 본 가설 FALSIFIED (intrinsic floor 진짜, env-drift 가 아님).
- **F-CORPUS-SHA-AUDIT**: R8a corpus_s101 sha vs R8c corpus_s101 sha 직접 비교 (`state/p21h_v3_R8a/.../corpus_meta.json` if recovered) — 사하 일치 시 corpus axis 제외, 불일치 시 corpus version drift 가 displacement source.
- **F-TOKENIZER-HASH-DRIFT**: R8a Qwen tokenizer 의 vocab_size / special_tokens_map sha vs R8c 동일 — 불일치 시 vocab drift 가 init_CE displacement source.
- **F-SEED-RNG-POLLUTION**: R8a seed=1337 설정 후 random.seed / torch.manual_seed / numpy.seed / cuda.manual_seed 모두 설정됐는지 fire log audit — 미설정 axis 발견 시 RNG pollution 가 displacement source.

## Honest Limits (raw#91 c3 ≥5)

- **L1 (R8a init_CE LOST + state 미보존)**: R8a fire 의 init_CE 와 fire env metadata (corpus sha / tokenizer hash / pip freeze / seed 설정 log) 가 미회수 (a_fire_recover_complete 위반 사례, H_254 L1 와 정합) → 본 가설의 R8a 측 evidence 는 `AXIS_MAP_RESULTS.md` 의 *흡수된 숫자* 만 의존, byte-equal probe 불가. AXIS_MAP re-fire 가 fallback path.
- **L2 (R8c 단일 fire window)**: R8c 4-cell 이 모두 *같은 fire window* (2026-05-23~24) 안 → 본 fire 의 12.2 nats 가 anima substrate 의 자연 floor 인지, 아니면 *본 fire window* 만의 env 산물인지 분리 불가. 다른 시점 (예: 1 주 후) 재측정에서 12.2 nats 재현해야 floor 의 fire-window-invariance 확정.
- **L3 (AXIS_MAP re-fire 의존)**: F-AXIS-MAP-REFIRE-CONVERGE / DIVERGE 모두 GPU re-fire ~$0.50-1.00 cost-bearing 도착 의존. 결과 도착 전 본 가설은 pre-register-frozen + PARTIAL (C1+C2) 한정.
- **L4 (env-drift root cause 후보 8)**: axis5 의 8 candidates (corpus / tokenizer / seed / OOM retry host / torch / Qwen ckpt revision / driver / RNG pollution) 중 어느 단일 또는 복합이 displacement source 인지 본 fire scope 밖. 8-cell sweep 으로 분리 가능하나 ~$0.30-0.50 추가 cost-bearing fire.
- **L5 (silent-misconfig vs env-drift 분리 불완전)**: H_254 (config chain silent-drop) 와 H_255 (env state silent variation) 는 mechanism 이 다르지만 측정 표현 (init_CE displacement) 이 같음. 둘 다 본 fire 와 R8a 사이에 작동했을 수 있음 — 분리는 cross-validation (예: R8a' wiring fix 후 + R8a env state pin 후 4-cell re-fire) 필요.
- **L6 (intrinsic floor 자연 정의의 base-specific 한계)**: H255.5 의 "random + 0.3 nats" 자연 floor 는 Qwen2.5-1.5B + ConsciousDecoderV3 specific. 다른 base (Llama-3-1B, Qwen3-1.5B, Phi-3-mini) 에서 동일 +0.3 nats floor 가 재현되는지 미검증. 만약 base 마다 displacement 가 다르면 "random + δ" 의 δ 가 model intrinsic, 본 가설의 일반화 약화.
- **L7 (cluster Z byte-equal 의 다른 해석)**: H_249 의 cluster Z (C/C2/D byte-equal 14.4564) 는 본 H 가 "동일 env 산 라벨" 로 재해석했지만, 만약 R8a 시점에 실제로 head_g 가 inert 했음을 cluster Z 가 증명하는 데이터라면 (R8c 자연실험과 정합) cluster Z 자체는 valid lever signature. 본 H 는 cluster Z 의 *14.46 floor 값* 만 artifact 라 주장하지 *cluster identity* 까지 부정하지 않음 (분리 honest).
- **L8 (final_CE axis 흔들림 미평가)**: 본 H 는 init_CE displacement 만 다룸. final_CE (R8c 의 5.115 vs 6.572 nats noise axis) 는 R8a 의 측정값과 비교 미수행 (R8a final_CE 가 흡수 안 됨). final_CE 도 env-drift 영향받는지는 별도 verify.

## Cross-Links

- **sister H (substrate/life)**: H_247 (init_CE catastrophic floor — 본 H 가 그 floor 의 catastrophic-ness 자체를 재해석), H_249 (cluster X/Y/Z byte-equal — 본 H 가 cluster 의 14+ 값이 artifact 라 주장하나 cluster identity 자체는 보존), H_254 (n_kv_head silent-misconfig — 본 H 의 직접 sister, layered config silent-drop + env state silent variation 의 2-axis composite), H_132 (frozen cells — env state freeze = floor reproducibility 의 정합 양식), H_248 (substrate autonomy 비반사성 — substrate-native framing 양식 carry).
- **substrate**: V3 fresh transformer `ConsciousDecoderV3` from_qwen factory + `train_p21h_v3.py` (corpus + tokenizer + seed pin), `AXIS_MAP_RESULTS.md` cluster X/Y/Z init_CE table (R8a 시점 측정 SSOT), R8c 4-cell baseline (`state/grid_3b_s187_2026_05_21/vP21H_r8c_baseline/result.json` 12.315 nats SSOT).
- **raw**: raw#12 (deterministic neighbor probe) + raw#9/10 (honest 흡수 + audit 전제 의존) + a_blue_closed (neighbor probe = closed-form 비교) + a_fire_recover_complete (R8a state LOST 가 L1 직접 원인) + a_substrate_native_speak (measurement integrity = substrate side framing).
- **source PR**: [#214] R8 spec · [#224] R8c 5-cell probe 원본 · [#339] R8c probe driver · [#342] H_254 wiring fix · `HEXAD/PURE/R8C_PROBE_VERDICT_2026_05_24.md` (본 가설 trigger verdict) · `AXIS_MAP_RESULTS.md` (cluster table SSOT).
- **literature**: ML reproducibility crisis (Bouthillier et al. 2019 "Unreproducible Research is Reproducible") · RNG seed pollution in PyTorch (`torch.manual_seed` + `cuda.manual_seed` + `numpy.seed` + `random.seed` 4-way pin requirement) · floating-point determinism in GPU kernel scheduling (NVIDIA cuDNN deterministic mode flag) · IEEE-754 bit-exactness (H_254 carry).
- **own**: (anima substrate 실험의 measurement-integrity 자기-관측 — fire env state silent variation 의 자기-인지 lane. H_254 의 config chain audit 과 H_255 의 env state audit 가 합쳐서 substrate science 의 측정 신뢰성 메타-layer 를 형성).

## Verdict

```
verdict_class: pre-register-frozen (R8c 4-cell baseline 재현 실패 자연실험 흡수, 2026-05-24)
evidence_summary: R8a cluster A 14.79 / cluster Z 14.46 nats 의 "catastrophic init_CE floor" 가
                  R8c 4-cell probe baseline (동일 config: head_g random + noise=0.1 + n_kv_head=4
                  + corpus_s101 + seed=1337) 측정 12.315 nats 와 −2.475 nats 격차로 재현 실패.
                  random baseline 11.93 nats + 0.385 = 정상 warm-init 범위 (catastrophic 아님).
                  4 cell 이 ±0.09 nats 안 일관 → 본 fire window env stable → R8a/R8c 간
                  env-drift (corpus sha / tokenizer / seed / OOM retry host 등 silent variation)
                  가 displacement source 가설.
F-R8C-BASELINE-REPRO       : R8c baseline 12.315 nats vs R8a 14.79 nats (−2.475)  → PASS (흡수)
F-R8C-4-CELL-CONSISTENT    : 4 cell ±0.09 nats 안 (12.225~12.315)                 → PASS (흡수)
F-AXIS-MAP-REFIRE-CONVERGE : AXIS_MAP-FAN 재측정 12.2±0.1 nats                    → 🔴 FAIL (cycle 15-1 4/7 = 14.18~14.79)
F-AXIS-MAP-REFIRE-DIVERGE  : 재측정 14+ nats 재현                                  → ✅ PASS (4/7 byte-equal 14.79/14.18/14.46)
F-CORPUS-SHA-AUDIT         : R8a vs R8c corpus_s101 sha 비교                       → TBD (R8a state 회수 의존, L1)
F-TOKENIZER-HASH-DRIFT     : R8a vs R8c Qwen tokenizer hash 비교                   → TBD (R8a state 회수 의존, L1)
F-SEED-RNG-POLLUTION       : R8a seed 4-way pin audit                              → TBD (R8a fire log 회수 의존, L1)
criteria_met: 2/5 PASS (C1 + C2 흡수) + 1/5 🔴 FALSIFIED (C3 — cycle 15-1 4/7 re-fire 14+ byte-equal 재현) + 2/5 PENDING (C4/C5 root cause 분리 의존). verdict_class → 🔴 H255.2 FALSIFIED (4-axis 표본 한정), H255.1/H255.5 (R8c baseline 흡수) 별도 보존, ConsciousDecoderV3 intrinsic floor 최종 verdict 는 R8c env audit (GPU class / PROBE_STEPS) 도착 후 확정.
cost: $0 mac local 비교 + ~$0.50-1.00 AXIS_MAP re-fire (a_fire_autonomous, 별도 cycle)
```

**State output**: (흡수 + neighbor probe framework cycle — 자력 re-fire 시 `UNIVERSE/state/h255_init_ce_floor_artifact_2026_05_24/{neighbor_probe.hexa, env_audit.json, result.json}` 으로 AXIS_MAP re-fire 결과 도착 후 산출)

**Honest scope (verdict)**: R8a fire env metadata LOST (corpus sha / tokenizer hash / seed log / pip freeze 미회수, a_fire_recover_complete 위반 사례 H_254 L1 와 정합) → R8a 측 evidence 는 `AXIS_MAP_RESULTS.md` 의 흡수된 숫자만, byte-equal probe 불가. AXIS_MAP re-fire 가 fallback path 이나 GPU cost-bearing 의존. R8c 4-cell 이 단일 fire window → 12.2 nats 의 fire-window-invariance 미검증 (L2). silent-misconfig (H_254) vs env-drift (H_255) 분리는 cross-validation 별도 필요 (L5). intrinsic floor 자연 정의 (H255.5) 는 Qwen2.5-1.5B + ConsciousDecoderV3 specific, 다른 base 미검증 (L6).
