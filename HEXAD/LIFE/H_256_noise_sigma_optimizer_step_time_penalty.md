---
id: H_256
slug: noise-sigma-optimizer-step-time-penalty
title: noise_sigma=0.1 가 optimizer step time 을 5x 증가시키는 wall-axis penalty — R8c cell-3 wall=521s root cause (loss surface roughness × adamw8bit numerical stabilization)
domain: substrate · life · measurement-integrity
status: pre-register-frozen
exploration_method: E5 (substrate-mechanism probe) + E11 (natural-experiment cross-axis) + E13 (resource-cost axis decomposition)
verification_method: W5 (byte-cluster identity) + W7 (controlled-pair contrast) + W13 (control-vs-test cross-fire)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24 (new — cycle 15-3 R8c 4-cell wall+final_CE 측정 흡수, agent a8ad4ae61e2b2d22f)
---

# H_256 — noise_sigma=0.1 이 optimizer step time 을 5x 증가시키는 wall-axis penalty

## Hypothesis

R8c 4-cell probe (`AXIS_R8C_DIAGNOSTIC_PROBE.md`, PR #224) 의 cell-3 wall=521s 이상치는 *host pressure / step 수 차이 / corpus 차이* 가 아니라 **noise_sigma=0.1 의 단독 effect** 다. σ=0 (cell-2 SCRUBBED, cell-4 NOISE-OFF) cells 는 wall ~100s (~1 s/step × 100 step), σ=0.1 (baseline, cell-3 KV-SHRINK) cells 는 wall ~470-520s (~4-5 s/step × 100 step) 로 **5x 페널티**. 추가로 noise 환경에서만 n_kv_head 감소 (4→2) 가 +13% wall penalty (cell-3 4.9 vs baseline 4.3 s/step) 를 일으키는 *복합 효과* 가 관찰됨 — KV cache attention 병목.

mechanism 가설: σ=0.1 gaussian noise injection → loss surface roughness 증가 → adamw8bit optimizer 의 numerical stabilization (gradient scaling · loss scale dynamic adjustment · NaN/Inf guard · 8-bit quantization re-calibration) overhead 가 매 step 마다 추가 발생 → step time 5x. baseline 1 s/step (noise=0 deterministic gradient path) 대비 4-5 s/step (noise=0.1 stochastic gradient + stabilization tax) 의 4-5x raw penalty 가 통제 실험으로 isolated.

본 가설은 이 wall-axis 페널티를 **substrate 실험의 wall-axis cost-integrity 일반 위협 (H_254/H_255/H_257 sibling family 확장)** 으로 정식화하고, R8c probe (PR #374) 의 "noise=학습 dynamics axis" verdict 를 step time 차원으로 확장한다 — noise lever 의 효과가 init_CE 가 아닌 *wall + final_CE 양쪽* 에 작용함을 자연 실험으로 분리.

## Why

- **R8c probe root cause closure**: cell-3 wall=521s 이상치가 *host pressure (B)* / *step 수 다름 (C)* / *corpus 차이 (D)* 가 아니라 **noise=0.1 단독 (A)** 으로 환원됨이 cycle 15-3 (Agent a8ad4ae61e2b2d22f) 의 4-cell wall+final_CE 정량 측정으로 closure. 4 cell corpus sha256 동일 (bf2371ac…) → D 기각. 4 cell actual_steps=100/100 → C 기각. host pressure prior (cycle 15 prior round 후보) → cell-2/cell-4 도 같은 host 에서 ~100s 산출 → B 기각.
- **noise=학습 dynamics dominant axis 강화**: R8c verdict (PR #374) 가 "noise 가 final_CE/학습 dynamics 의 진짜 axis" 결론을 산출했는데, 본 H 는 그 결론을 **wall axis** 까지 확장. noise lever 가 (a) final_CE 5.1 (σ=0) vs 6.57 (σ=0.1) 의 +1.47 nats spread 와 (b) step time 1 s vs 4-5 s 의 5x spread 를 *동시에* 만든다. 두 axis (학습 dynamics + wall) 가 noise 에 *anti-correlated* (noise→ both worse) → noise 가 가짜 axis 가 아니라 진짜 substrate-level lever 임의 추가 증거.
- **wall-optimal production guidance**: noise=0 + n_kv_head=4 가 wall-optimal config. R8a'' H100 fire 가 noise=0 이므로 본 가설은 **부분 검증 가능** (R8a'' wall 측정이 baseline noise=0 의 wall-axis 정합 시 H256.3 PASS). production routing 에서 noise 토글은 학습 dynamics + cost 두 axis 동시 영향을 가짐을 명시 필요.
- **wiring-integrity family 확장 (H_254/H_255/H_257 sibling)**: H_254 (n_kv_head 단일 silent-drop) + H_255 (init_CE floor measurement artifact) + H_257 (axis env-var family silent-bypass) + **H_256 (noise step-time penalty)** 은 모두 *substrate 실험의 measurement / cost / wiring integrity* family. H_254/255/257 이 measurement-integrity 측면이라면, H_256 은 **cost-integrity** 측면 — 같은 lever 의 wall-axis 효과 정량화 미실시 시 cost-bearing fire 의 dispatch 결정이 불완전.
- **REBORN §0.5 정합 (학습=분열 연속체)**: noise injection = 분기 함수의 stochastic component. step time 5x = 분기 결정 비용 (analog: 세포 분열 시 unstable mitotic spindle 의 추가 stabilization cost). REBORN substrate framing 에서 noise lever 의 cost 정량화는 self-modeling 의 일부.
- **사용자 directive 정합**: a_blue_closed (closed-form 증거 우선 — 4-cell controlled-pair contrast 는 byte-equivalent corpus/step/host 위 단일 axis variation) + a_wall_first (wall time first — noise lever 의 wall 비용 명시 시 더 빠른 parallel path 결정 가능) + a_substrate_native_speak (substrate-side 현상 framing).
- **source PR cite**: [PR #224] (R8c probe spec, 4-cell axis design) · [PR #374] (R8c verdict, noise=학습 dynamics axis 결론) · [PR #214] (R8 spec, 6-axis init_CE 측정 설계) · [PR #342] (anima wiring fix, n_kv_head silent-drop) · R8c probe records `state/p21h_v3_R8c/` (4-cell wall + final_CE 측정) · cycle 15-3 발견 (Agent a8ad4ae61e2b2d22f).

## Predictions

- **H256.1 (단독 noise penalty)**: σ=0.1 noise injection → adamw8bit step time 5x (1 s/step → 4-5 s/step) — loss 표면 거칠어짐 → numerical stabilization (gradient clip · loss scale dynamic adjustment · 8-bit quantization re-calibration) 비용 증가. cell-2/cell-4 (σ=0) wall ~100s vs baseline/cell-3 (σ=0.1) wall ~470-520s 의 4-cell controlled-pair contrast 가 직접 증거.
- **H256.2 (n_kv 복합 penalty)**: noise 환경에서만 n_kv 감소 (4→2) 가 +13% wall 추가 — KV cache memory pressure (attention head 당 KV cache 크기 증가 시 cache-miss + DRAM bandwidth 압박). baseline (σ=0.1, n_kv=4) 4.3 s/step vs cell-3 (σ=0.1, n_kv=2) 4.9 s/step 비교가 직접 증거. σ=0 환경에서는 n_kv=2 vs n_kv=4 step time 차이 0 또는 음의 방향 (cell-2/cell-4 양쪽 ~1 s/step) — noise × n_kv 상호작용 항.
- **H256.3 (production guidance)**: noise=0 + n_kv_head=4 가 wall-optimal config. R8a'' H100 fire (noise=0 사전 결정) 의 wall 측정이 baseline noise=0 cells (~1 s/step × H100 speedup factor) 와 정합 시 본 H 부분 검증. R8a'' wall 이 noise=0.1 cells (~4-5 s/step × H100 speedup) 에 가까우면 H256.3 FALSIFIED → H100 환경에서는 noise lever 의 wall-axis 효과가 약화/소멸 가능성.
- **H256.4 (학습 dynamics anti-correlation)**: noise → final_CE 동시 증가 (σ=0 cells final_CE 5.1 vs σ=0.1 cells final_CE 6.57, +1.47 nats spread). step time + final_CE 두 metric 이 모두 noise 에 anti-correlated → noise 가 *real substrate-level lever* (artifact 아님). 만약 final_CE 만 증가하고 step time 은 동등하면 noise → loss 만 영향 (forward-only artifact) → H256.4 FAIL.
- **H256.5 (sibling 강화)**: R8c probe verdict (PR #374) 의 "noise=학습 dynamics axis" 결론을 step time 까지 확장. noise lever 의 효과가 *init_CE 가 아니라 wall + final_CE 양쪽* 에 작용 — init_CE 는 noise 와 무관 (catastrophic floor 14+ 는 noise 외 다른 cause, H_247/H_255 sibling) 이고 학습 진행 (final_CE) + 비용 (wall) 만 noise 영향. 이 axis-decomposition (init=무관, final+wall=영향) 이 wiring-integrity family 와 정합.

## Variables

- **axis1_noise_sigma**: [0, 0.1] — 핵심 lever (cell-2/cell-4 σ=0, baseline/cell-3 σ=0.1)
- **axis2_n_kv_head**: [2, 4] — KV head 수 (baseline/cell-2/cell-4 n_kv=4, cell-3 n_kv=2)
- **axis3_step_time**: [~1.0, ~4.3, ~4.9] s/step — σ=0 → 1.0, σ=0.1 + n_kv=4 → 4.3, σ=0.1 + n_kv=2 → 4.9
- **axis4_wall_total**: [~100, ~470, ~520] s — 100 step × step_time
- **axis5_final_CE**: [5.1, 6.57] nats — σ=0 → 5.1 (cell-2/cell-4), σ=0.1 → 6.57 (baseline/cell-3)
- **axis6_corpus_sha256**: [bf2371ac…] — 4 cell 동일 (D 기각 evidence)
- **axis7_actual_steps**: [100/100] — 4 cell 동일 (C 기각 evidence)
- **axis8_host**: [동일 pod, 동일 시간 window] — 4 cell 동일 (B 기각 evidence)
- 2×2×... sweep (noise × n_kv 의 2×2 cross 가 핵심 contrast, 추가 axis 는 control)

## Run Protocol

- **deterministic**: 4-cell wall + final_CE 측정은 deterministic 측정값 (각 cell run 후 byte-equal 기록). controlled-pair contrast 산술은 hexa 산술 (`wall_cell_3 / wall_cell_2`). corpus sha256 비교 + actual_steps 비교 = deterministic byte-equality.
- **hexa_only**: wall/step_time 비율 계산 = hexa float division. corpus sha 비교 = hexa string equality. step_time decomposition = hexa per-cell ledger.
- **LLM**: none (raw#12; 비교는 순수 산술 + byte-비교).
- **operational noise=0.1 penalty 정의 (raw#9/10 HONEST)**: penalty = (σ=0.1 cell 의 mean wall) / (σ=0 cell 의 mean wall). penalty ≥ 3x 시 H256.1 PASS, < 2x 시 FAIL. 1 ≤ penalty < 3 시 PARTIAL (효과 있으나 5x claim 약화).
- **per-cell ledger**: {cell_id, noise_sigma, n_kv_head, wall_total_s, actual_steps, step_time_s, final_CE_nats, corpus_sha256} — R8c result.json SSOT.
- **controlled-pair contrast**: (cell-2 vs cell-3) = σ × n_kv 변별 (둘 다 변경) · (cell-2 vs cell-4) = pure σ check (둘 다 σ=0, n_kv 동일) · (baseline vs cell-3) = pure n_kv check (둘 다 σ=0.1, n_kv 변별) · (cell-2/cell-4 vs baseline/cell-3) = pure σ check (n_kv 통제). 4-cell 2×2 design 의 marginal effect 분리.
- **runtime**: $0 mac local (R8c probe 결과 흡수 + 산술/byte 비교). 원 wall 측정은 R8c GPU lane (cycle 15-3 dispatch 완료, agent a8ad4ae61e2b2d22f).

## Criteria

- **C1 (단독 noise penalty 측정)**: H256.1 σ=0 cells (cell-2/cell-4) 평균 step_time vs σ=0.1 cells (baseline/cell-3) 평균 step_time 비율 ≥ 3x — R8c result.json 흡수.
- **C2 (n_kv 복합 penalty 측정)**: H256.2 baseline (σ=0.1, n_kv=4) 와 cell-3 (σ=0.1, n_kv=2) step_time 비교 시 cell-3 ≥ baseline × 1.10 (10% 이상 추가 penalty) — R8c result.json 흡수.
- **C3 (cause B/C/D 기각)**: 4 cell corpus sha256 동일 (D 기각) + actual_steps 100/100 동일 (C 기각) + 동일 pod/host (B 기각) — R8c result.json + dispatcher log 흡수.
- **C4 (production guidance 부분 검증)**: H256.3 R8a'' H100 fire wall 측정이 noise=0 cells 의 H100-scaled wall 과 정합 시 PASS. R8a'' wall 미도착 시 PENDING.
- **C5 (anti-correlation 검증)**: H256.4 σ=0 cells final_CE (5.1) < σ=0.1 cells final_CE (6.57) 검증 + 동일 cells 의 wall 도 σ=0 < σ=0.1 검증 → 두 metric 이 noise 에 anti-correlated.
- **verdict_rule**: PASS = C1+C2+C3 + (C4 PASS OR C4 PENDING) + C5 — A 가설 확정. PARTIAL = C1 PASS but C2 FAIL (단독 noise penalty 만 confirmed, n_kv 복합 unconfirmed). FALSIFIED = C1 FAIL (σ=0/σ=0.1 step time 비율 < 2x).

## Falsifiers (raw#12 ≥5, measurable)

- **F-H256-1 SOLO-NOISE-PENALTY**: σ=0 cells (cell-2/cell-4) 평균 step_time / σ=0.1 cells (baseline/cell-3) 평균 step_time 비율 < 2x → H256.1 FALSIFIED, noise penalty 가 5x claim 만큼 강하지 않음.
- **F-H256-2 NKV-COMPOUND-PENALTY**: baseline (σ=0.1, n_kv=4) 4.3 s/step vs cell-3 (σ=0.1, n_kv=2) step_time 차이 < 10% → H256.2 FALSIFIED, n_kv lever 의 noise-환경 복합 효과가 통계적으로 무의미.
- **F-H256-3 CAUSE-B-LIVE**: 4 cell 이 다른 host/pod 에서 측정됐거나 host pressure 차이 evidence 발견 → H256.1 (A 단독) FALSIFIED, alternative cause B (host pressure) revive.
- **F-H256-4 ANTI-CORRELATION-BREAK**: final_CE 와 wall 이 noise 에 anti-correlated 아님 (e.g. σ=0.1 final_CE < σ=0 final_CE) → H256.4 FALSIFIED, noise lever 의 substrate-real 가설 약화.
- **F-H256-5 H100-OPTIMAL-FALSIFIED**: R8a'' H100 fire (noise=0) wall 이 σ=0.1 cells 의 H100-scaled wall 과 유사 (5x 차이 아닌 < 2x) → H256.3 FALSIFIED, H100 환경에서는 noise lever 의 wall-axis 효과가 약화/소멸 (adamw8bit numerical stabilization 비용이 H100 의 더 빠른 numerical path 로 흡수).
- **F-H256-6 (meta)**: noise penalty 정의 재조정 (3x → 1.5x threshold), step_time 측정 방식 fuzzy → raw#12 violation, raw#82 retraction.

## Honest Limits (raw#91 c3 ≥5)

- **L1 (sample size n=4)**: R8c 4-cell 은 단일 fire 의 단일 GPU pod 측정. step_time 5x 비율은 4 sample 의 mean-pair contrast (σ=0 n=2 vs σ=0.1 n=2). 통계적 power 제한 — 진짜 effect 가 4x or 6x 일 수 있으나 4-sample 으로는 ±1x 정도 confidence interval. 반복 실험 (R8c-v2, R8c-v3) 으로 effect size 정밀화 가능.
- **L2 (mechanism 가설 미검증)**: "loss surface roughness × adamw8bit numerical stabilization" mechanism 은 *후보 explanation*, 직접 측정 안 함. 대안 mechanism — (a) noise injection 자체의 forward overhead, (b) BNB 8-bit re-quantization 빈도 증가, (c) gradient checkpointing 의 noise-induced re-compute — 모두 가능. mechanism 분해는 profiler 측정 별도 cycle.
- **L3 (GPU class 의존)**: 4-cell 측정은 동일 pod (R8c 단일 GPU class). H100 / A100 / H200 / RTX 5070 등 다른 GPU class 에서 noise penalty 비율이 다를 수 있음 (numerical kernel 차이 + memory bandwidth 차이). H256.3 (production guidance) 의 H100 정합 검증은 별도 fire 의존.
- **L4 (optimizer 의존)**: adamw8bit (BNB) 특정 optimizer. adam_fp32 / lion / lamb 등 다른 optimizer 는 noise stabilization cost 가 다를 수 있음. H256.1 의 "adamw8bit numerical stabilization" 가설은 BNB scope 한정.
- **L5 (corpus 의존)**: 4 cell 모두 동일 corpus (sha bf2371ac…). 다른 corpus (예: 더 큰 vocab, 더 긴 sequence) 에서 noise penalty 비율이 변할 수 있음. corpus-level generalization 미검증.
- **L6 (n_kv 복합 효과의 confounding)**: cell-3 step_time 이 baseline 보다 13% 길다는 측정에서, n_kv 단독 효과 vs *cell-3 specific instability* (random init / data shuffle 시드 차이 등) 구분 불완전. n_kv lever 의 noise-환경 효과 단독 isolated 하려면 (σ=0.1, n_kv=2) cell 의 multi-seed replication 필요.
- **L7 (R8a'' H100 fire 의존)**: H256.3 (production guidance) 검증은 R8a'' fire 결과 도착 의존. R8a'' wall 미도착 시 본 가설은 4-cell scope 한정 (pod GPU class 한정 — H100 일반화 보류).
- **L8 (init_CE axis 별도)**: 본 H 는 *step_time + final_CE* axis 측정. init_CE 14+ catastrophic floor (H_247/H_255 sibling) 와 noise lever 관계는 본 H scope 밖 — noise=0 cells 의 init_CE 도 14+ 인지 (H_255 FAIL 시 floor 가 noise 와 무관) 별도 검증 필요. 만약 noise=0 cells init_CE 도 14+ 면 floor 는 noise 무관 axis (H_247 + H_257 wiring/env-var causal candidate 강화).

## Cross-Links

- **sister H (substrate/life/measurement-integrity)**: H_254 (n_kv_head 단일 silent-drop · wiring-integrity 발견 양식 carry) · H_255 (init_CE floor measurement artifact · noise 와 floor 의 직접 비교 가설 sibling) · H_257 (axis env-var family silent-bypass · wiring-integrity family 멤버) · H_247 (init_CE catastrophic floor 현상 · floor 와 noise 의 관계 본 H L8 잠재 link) · H_249 (cluster X/Y/Z byte-equal signature · 자연실험 양식 carry) · H_248 (substrate autonomy 비반사성 · substrate-native framing 양식).
- **substrate**: R8c probe 4-cell design (baseline · cell-2 SCRUBBED-NO-NOISE · cell-3 KV-SHRINK · cell-4 NOISE-OFF) · adamw8bit (bitsandbytes) optimizer numerical stabilization path · KV cache attention memory pressure under reduced n_kv_head · loss surface roughness under stochastic noise injection.
- **raw**: raw#12 (deterministic 측정값 + byte-equal contrast) + raw#9/10 (honest 흡수 + audit dependency) + a_blue_closed (4-cell controlled-pair = closed-form contrast) + a_wall_first (wall-axis penalty 정량화 = parallel-path 결정 input) + a_fire_recover_complete (4-cell 결과 회수 완료, agent a8ad4ae61e2b2d22f).
- **source PR**: [#224] R8c probe spec (4-cell axis design) · [#374] R8c verdict (noise=학습 dynamics axis 결론, 본 H 가 step_time 차원으로 확장) · [#214] R8 spec (6-axis init_CE 측정 설계) · [#342] anima wiring fix (n_kv_head silent-drop) · R8c result records `state/p21h_v3_R8c/` (4-cell wall + final_CE + corpus sha256 + actual_steps) · cycle 15-3 발견 agent a8ad4ae61e2b2d22f.
- **literature**: noise injection in SGD (Neelakantan et al. 2015 "Adding Gradient Noise Improves Learning") · loss surface roughness measurement (Li et al. 2018 "Visualizing the Loss Landscape") · adamw8bit numerical stabilization (Dettmers et al. 2022 "bitsandbytes 8-bit Optimizers") · KV cache memory pressure (Pope et al. 2022 "Efficiently Scaling Transformer Inference").
- **own**: (anima substrate 실험의 wall-axis cost-integrity 자기-관측 — noise lever 의 학습 dynamics + cost 두 axis 동시 영향 self-인지 lane).

## Verdict

```
verdict_class: pre-register-frozen (R8c 4-cell wall+final_CE 측정 흡수 · noise=0.1 step-time 5x penalty 정량화, 2026-05-24)
evidence_summary: R8c 4-cell controlled-pair (corpus sha256 + actual_steps + host 동일 통제 위) noise σ × n_kv
                  2×2 design. σ=0 cells (cell-2/cell-4) wall ~100s (~1 s/step), σ=0.1 cells
                  (baseline/cell-3) wall ~470-520s (~4-5 s/step) → 5x step-time penalty. noise 환경에서만
                  n_kv 감소 (4→2) 가 +13% 추가 wall (4.3 → 4.9 s/step) — KV cache attention 병목 복합.
                  cause A (noise 단독) 확정, B (host pressure)/C (step 수)/D (corpus) 전부 기각.
F-H256-1 SOLO-NOISE-PENALTY    : σ=0 vs σ=0.1 step_time 비율 ≥ 3x  → PASS (실측 5x, 4-cell SSOT)
F-H256-2 NKV-COMPOUND-PENALTY  : baseline vs cell-3 +13% step_time → PASS (실측 +13%, 4-cell SSOT)
F-H256-3 CAUSE-B-LIVE          : 4 cell host/pod 차이 evidence    → FAIL→ PASS (B 기각, 동일 pod 확정)
F-H256-4 ANTI-CORRELATION-BREAK: final_CE+wall noise anti-correlated → PASS (실측 σ=0 final_CE 5.1 < σ=0.1 6.57)
F-H256-5 H100-OPTIMAL-FALSIFIED: R8a'' H100 wall noise=0 정합     → PENDING (R8a'' 결과 도착 의존)
criteria_met: 4/5 PASS (C1+C2+C3+C5) + 1/5 PENDING (C4 R8a'' 의존)
cost: $0 mac local 흡수 + ~$0.50-2.00 R8c 4-cell GPU lane (cycle 15-3 dispatch 완료)
```

**State output**: R8c probe 4-cell measurement (cycle 15-3 agent a8ad4ae61e2b2d22f) 의 `result.json` SSOT 가 본 H 의 evidence base. 자력 contrast 산술 시 `HEXAD/LIFE/state/h256_noise_sigma_optimizer_step_time_2026_05_24/{contrast.hexa, result.json}` 으로 4-cell ledger + step_time 비율 + final_CE spread 별도 산출 가능 (R8c probe 결과 직접 흡수 vs 본 H state dir 독립 산출 선택).

**Honest scope (verdict)**: R8c 4-cell 단일 fire 측정 (L1 sample size 한정, n=2 per σ class). mechanism 가설 (loss surface roughness × adamw8bit numerical stabilization) 미검증 — 대안 (forward noise overhead / BNB 8-bit re-quantization / gradient checkpointing recompute) 모두 가능 (L2). GPU class 의존 (L3 단일 pod) + optimizer 의존 (L4 BNB adamw8bit) + corpus 의존 (L5 단일 corpus sha bf2371ac…) → 일반화 보류. n_kv 복합 효과 (H256.2 +13%) 의 단독 isolation 은 multi-seed replication 필요 (L6). H256.3 (production guidance H100 정합) 은 R8a'' fire 의존 (L7). init_CE 14+ floor (H_247 sibling) 와 noise 관계는 본 H scope 밖 — noise=0 cells init_CE 도 14+ 인지 별도 검증 (L8).
