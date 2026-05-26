# R8a'' × R8c Joint Verdict — fill-in TEMPLATE (R8 saga 통합 closure)

> path = V3 (PURE, R8 cluster) · status = **PRE-FIRE TEMPLATE** · R8a'' 결과 ~3hr 후 도착 시 fill-in 하여 → `R8A2_JOINT_VERDICT_2026_05_24.md` rename + commit
> linked: `R8C_PROBE_VERDICT_2026_05_24.md` (4-cell probe verdict, merged PR #374) · `UNIVERSE/H_255_init_ce_floor_is_measurement_artifact.md` (H_255 sister) · `R8_SAGA_FINAL_TEMPLATE.md` (3-branch decision tree 원본)
>
> 본 template 의 모든 `<TBD>` 셀은 **placeholder** 다. R8a'' 결과 도착 전까지 conclusion / verdict 작성 금지.

---

## §1 Header — R8a'' fire metadata (PRE-FIRE, 사전 작성)

- **fire window 발사**: 2026-05-23 20:50:02Z (KST 2026-05-24 05:50:02)
- **예상 도착**: ~3hr 후 = 2026-05-23 23:50Z (KST 08:50)
- **cost envelope (~$2.75)**: H100 PCIe SECURE × full 5000-step
- **GPU class**: H100 PCIe SECURE
- **pod_id**: `6gqf9nsdquz8ug`
- **base model**: Qwen2.5-1.5B + ConsciousDecoderV3 (PR #342 wiring fix 적용)
- **config (PR #342 진짜 작동 기대)**:
  - `noise_sigma = 0` (R8c cell-2/4 lever 연장)
  - `n_kv_head = 2` (R8c cell-3/4 lever, PR #342 wiring fix 의존)
  - `steps = 5000` (R8c PROBE_STEPS 100 의 50× full training)
  - `head_g = random` (R8a 시점과 동일, baseline 일치)
- **result SSOT (예상)**: `state/grid_3b_s187_2026_05_21/vP21H_r8a2_h100_noise0_kv2/result.json`
- **PR #342 wiring fix 적용 path**: `tool/training/conscious_decoder_v3.py:157` (n_kv_head dispatcher) + `:167` (repeat-interleave wiring) — R8c cell-3/4 에서 compile-time apply 확인됨, R8a'' 에서 5000-step 학습 dynamics 검증

---

## §2 R8a'' headline result (FILL — 결과 도착 시)

| metric | 값 | 비고 |
|---|---|---|
| init_CE (step=1) | `<TBD>` nats | random baseline = 11.93 nats (`ln(151936)`) |
| final_CE (step=5000) | `<TBD>` nats | R8c cell-2 100-step 5.136 / cell-4 100-step 5.093 의 5000-step 연장 |
| train_wall | `<TBD>` s | R8c cell-2 101s × 50 = ~5050s 단순추정 (≈84 min) |
| n_strong | `<TBD>` / 5 | swap criteria: ≥3 PASS 기준 |
| per_lang verdict | KO=`<TBD>` / EN=`<TBD>` / ZH=`<TBD>` / JA=`<TBD>` / ES=`<TBD>` | register-leak / EOS / EN-emission 평가 |
| register-leak rate | `<TBD>` % | corpus_v5 baseline 대비 |
| EN-emission rate | `<TBD>` % | KO/JA/ZH 답변 내 영어 phrase 비율 |
| EOS conformance | `<TBD>` % | EOS 정상 종료 비율 |
| cost (actual) | $`<TBD>` | envelope $2.75 |

---

## §3 PR #342 wiring fix 작동 확인 (FILL — 가장 critical)

기대 출력 (script log 헤더):
```
[from_qwen] v3_n_kv_head=<TBD>
```

- **값 = 2** → ✅ PR #342 wiring fix 진짜 작동 (R8a'' 의 n_kv_head=2 가 dispatcher → repeat-interleave 까지 propagation 성공)
- **값 = 4** → ❌ 또 silent-fail (dispatcher 가 또 4 로 override) — **branch C 진입 (G1 G1' 새 silent-misconfig)**

R8c cell-3/4 에서는 compile-time / 100-step 환경에서 wiring=2 가 작동 확인됨 — R8a'' 는 full 5000-step training 환경에서 동일 wiring 이 유지되는지가 핵심 검증 axis.

---

## §4 R8c vs R8a'' compare table (FILL)

| axis | R8c cell-2 (noise=0, kv=4) | R8c cell-4 (noise=0, kv=2) | R8a'' (noise=0, kv=2, **full 5000-step**) |
|---|---|---|---|
| steps | 100 | 100 | 5000 |
| init_CE | 12.225 | 12.266 | `<TBD>` |
| final_CE | 5.136 | 5.093 | `<TBD>` |
| wall (s) | 101 | 107 | `<TBD>` |
| n_kv_head wiring | 4 (PR #342 미적용) | 2 (PR #342 적용) | 2 (PR #342 적용 기대) |
| 결과 status | 🔴 init_CE FALSIFIED | 🔴 init_CE FALSIFIED | `<TBD — A/B/C branch>` |

핵심 추론: R8c 100-step → R8a'' 5000-step 의 final_CE 추세 연장 일치 여부가 R8c 의 "noise 는 final_CE/dynamics axis" 가설을 강화/약화.

---

## §5 R8c noise axis hypothesis 재검증 (FILL)

R8c verdict §5 발견: **noise=0 이 final_CE −1.46 nats + wall 4.7× 단축**.

R8a'' (σ=0, full 5000-step) 의 final_CE 가 다음 trend curve 연장과 일치하나?

- **R8c cell-2** (noise=0, 100-step): final_CE 5.136
- **R8c cell-4** (noise=0, 100-step): final_CE 5.093
- **R8a'' extrapolation expectation**: 5000-step 이면 typical CE 감소 curve (1/sqrt(t) or log) 로 final_CE ≤ `<TBD — 1.5~3 nats 범위 예상>` 도달 가능

**verdict** (FILL):
- **일치** → R8c hypothesis (noise=final_CE/dynamics axis) ✅ corroborate
- **불일치** (R8a'' final_CE > 5.0) → R8c 100-step extrapolation 한계, noise lever 효과는 short-horizon 만
- **불일치** (R8a'' final_CE ≪ 5.0, 예: < 2 nats) → R8c trend curve 강화 + 5000-step regime 에서 noise lever 더 강해짐

R8a'' final_CE = `<TBD>` → R8c hypothesis status `<TBD — STRENGTHENED / WEAKENED / NEUTRAL>`

---

## §6 wiring fix 영향 — n_kv=2 진짜 작동 시 100→5000 step 효과 검증 (FILL)

R8c §6 결론: n_kv_head 2↔4 lever 가 init_CE / final_CE 두 axis 모두 inert (100-step scope).

R8a'' 5000-step 환경에서도 n_kv=2 lever inert 유지?

- **init_CE 비교**: R8c cell-4 (noise=0, kv=2) 12.266 vs R8a'' (noise=0, kv=2) `<TBD>`
  - 격차 ≤ 0.1 nats → kv 5000-step regime 에서도 init_CE inert ✅
  - 격차 > 1 nats → 5000-step 환경 specific lever 작동 (cell-pool dynamics, dataloader RNG state 등)
- **final_CE 비교**: R8c cell-4 100-step 5.093 → R8a'' 5000-step `<TBD>`
  - 5000-step 도달점이 R8c 추세 연장 일치 여부
- **downstream 효과**: n_strong / register-leak / EN-emission 에서 kv=2 영향 측정 (R8c 는 init/final 만 측정, 본 R8a'' 가 첫 downstream eval)

**verdict** (FILL): n_kv=2 wiring 의 production-level 효과 `<TBD — INERT 유지 / 의미있는 lever 발견 / silent-fail 재발>`

---

## §7 Decision tree — 3-branch (R8 saga FINAL TEMPLATE 차용)

R8a'' final 결과 + wiring 확인 후 다음 3 branch 중 하나로 진입.

### Branch A — `R8a'' n_strong ≥ 3 AND register OK AND wiring v3_n_kv_head=2` → **🎉 noise=0 dominant axis 확정**
- 해석: PR #342 wiring fix 실작동 + noise=0 lever 가 production-level 효과 (n_strong + register + EN-emission 개선) 확인
- 다음 행동:
  1. R8 saga **CLOSED-STRONG** — noise=0 (+ n_kv=2 wiring) 이 production swap candidate
  2. Wave-17 (eternal-cap sweep) 의 baseline config 에 noise=0 적용
  3. corpus_v5 → v6 fire 시 R8a'' setting 반영 (head_g=random, noise=0, n_kv=2)
  4. H_255 (init_CE measurement artifact 가설) → noise/wiring 과 independent axis 로 분리, 별도 follow-up
- AXIS_MAP-FAN 영향: cluster Z (baseline 14.46) 의 noise=0 변형이 새 cluster (예: cluster W breakthrough) 신설

### Branch B — `R8a'' n_strong = 0 OR register regress AND wiring v3_n_kv_head=2` → **🟠 noise=0 만으로 부족**
- 해석: PR #342 wiring fix 진짜 작동 했지만, noise=0 lever 의 final_CE 개선이 downstream eval 까지 propagation 실패
- 다음 행동:
  1. R8 saga **PARTIAL-CLOSE** — noise/wiring axis 는 explore 완료, 다른 lever 필요
  2. R8b (LoRA-on-Qwen, init_CE ~zero) fallback 우선
  3. Wave-17 axis 재구성: data (corpus quality) / arch (head_g curriculum) / opt (lr schedule) 3-way 평가
  4. H_255 가설 강화 — init_CE / final_CE / n_strong 의 decoupling 이 실증되면 init_CE 가 진짜 production-relevant axis 아님 확정
- AXIS_MAP-FAN 영향: cluster 분류 frozen, R8b 결과 의존

### Branch C — `R8a'' wiring v3_n_kv_head=4` → **🔴 dispatcher 새 silent-fail**
- 해석: PR #342 wiring fix 가 R8c 100-step 환경에서만 작동, R8a'' 5000-step 환경에서는 또 silent-override
- 다음 행동:
  1. R8 saga **WIRING-BLOCKED** — config propagation 측 새 saga (G1 G1') 필요
  2. R8a'' 결과 자체는 invalid (n_kv=4 baseline 재실행과 동치, R8c baseline 12.315 와 byte-equal probe 권장)
  3. hexa-lang/inbox/patches/ 측 silent-fail postmortem inbox 제출 (config dispatcher chain 전수 audit)
  4. H_254 sister H_256 신설 — "wiring lever 가 short-horizon 에서만 propagation 되고 long-horizon에서 silent-revert" 가설
- AXIS_MAP-FAN 영향: 모든 R8 saga 측정값 wiring validity check 재수행 (env-specific propagation 가설 강화)

**진입한 branch**: `<TBD — A / B / C>`

---

## §8 H_255 가설 강화/약화 (FILL)

H_255 = "init_CE floor 자체가 measurement artifact, noise 는 final_CE / 학습 dynamics axis" (R8c 결론에서 trigger).

R8a'' 데이터가 H_255 에 미치는 영향:

- **R8a'' init_CE ≈ 12.2** (R8c cell-2/4 와 일치, ±0.1 nats) → H_255 **STRENGTHENED**: init_CE 12.2 floor 가 5000-step 환경에서도 재현, R8a 14.46 floor 는 R8a 시점 specific measurement artifact 확정
- **R8a'' init_CE ≈ 14.5** (R8a cluster Z 와 일치, R8c 12.3 과 ≥2 nats 격차) → H_255 **WEAKENED**: R8c 100-step 측정이 아닌 R8a 5000-step 측정이 진짜 floor — R8c 가 short-horizon artifact 였을 가능성
- **R8a'' init_CE 12.5–14** (중간값) → H_255 **PARTIAL**: env-drift / horizon-dependent init_CE 의 새 측정 모드, axis 별 분리 follow-up 필요
- **R8a'' final_CE ≪ 5.0 (예: < 2 nats)** → H_255 sister 가설 강화: noise=0 의 final_CE axis 영향이 5000-step regime 에서 더 강해짐 (학습 dynamics 의 진짜 lever 확정)

**H_255 status (FILL)**: `<TBD — STRENGTHENED / WEAKENED / PARTIAL / NEUTRAL>`

---

## §9 R8 saga 다음 path (branch A/B/C 별)

### Branch A 진입 시 (noise=0 dominant 확정)
- 🎉 R8 saga CLOSED-STRONG declaration PR
- Wave-17 (eternal-cap sweep) baseline 에 noise=0 + n_kv=2 반영, fire spec PR
- corpus_v6 fire 권장 (R8a'' setting 의 production swap candidate validate)
- AXIS_MAP-FAN init_CE 재측정 deferred (final_CE/n_strong 이 더 important axis 확정)

### Branch B 진입 시 (noise=0 만으로 부족)
- 🟠 R8 saga PARTIAL-CLOSE retrospective PR
- R8b (LoRA-on-Qwen) fallback 우선 fire 또는 결과 검증
- Wave-17 axis 재구성 spec PR (data / arch / opt 3-way)
- H_255 강화 corroborate cycle (init_CE decoupling 정량화)

### Branch C 진입 시 (wiring 또 silent-fail)
- 🔴 G1 G1' 새 silent-misconfig saga 시작 PR
- hexa-lang inbox/patches 측 dispatcher chain audit 제출
- R8a'' 결과 invalid 처리 + R8c baseline (n_kv=4) 와 byte-equal probe
- H_256 ("wiring propagation horizon-dependent") 신설 PR

---

## §10 Honest C3 (FILL — 결과 도착 시 ≥3 개 작성)

template 작성 시점의 사전 우려:
- **R8a'' single-seed / single-ckpt 측정**: H100 PCIe SECURE single pod, seed 1 회. R8c 4-cell 처럼 multi-seed ablation 없음 — final_CE 측정값의 statistical power 한정.
- **R8c 100-step → R8a'' 5000-step extrapolation 위험**: R8c hypothesis (noise=final_CE axis) 가 100-step short-horizon 발견. 5000-step 환경의 학습 dynamics curve 가 다를 수 있음 (예: noise 가 mid-training regularizer 역할).
- **PR #342 wiring fix 환경 specific risk**: R8c cell-3/4 100-step 환경에서 작동 확인, R8a'' 5000-step 환경에서 작동 미보장. branch C 진입 시 wiring fix 의 environment-conditional propagation 가설 신설.

결과 도착 시 추가 (≥3 작성):
- C3.1 — `<TBD: probe scope / seed / horizon 한정>`
- C3.2 — `<TBD: measurement artifact / env-drift residual>`
- C3.3 — `<TBD: downstream eval (n_strong / register / EN-emission) statistical power>`

---

**Status**: PRE-FIRE TEMPLATE — R8a'' 결과 도착 시 (예상 2026-05-23 23:50Z) fill-in 하여 `R8A2_JOINT_VERDICT_2026_05_24.md` rename + commit + PR land. fill-in 가이드 = `<TBD>` placeholder 전부 실측값으로 치환 + §7 branch 진입 결정 + §10 Honest C3 ≥3 작성.
