# R8a'' × Qwen-parity Verdict — M3 final_CE 측정 closure (2026-05-25)

> path = V3 (PURE, R8 cluster) · status = **M3 PENDING (양측 미측정)** · cycle = LORA M3 (V3 ConsciousDecoderV3 Qwen-parity)
> linked: `R8A2_JOINT_VERDICT_TEMPLATE.md` (PR #375 MERGED, 본 doc 가 fill 대상이었으나 R8a'' LOST 로 measurement 미도착) · `R8A2_FILL_IN_GUIDE_2026_05_24.md` (5-step closure 매뉴얼) · `HEXAD/LIFE/H_255_init_ce_floor_is_measurement_artifact.md` (init_CE floor closure sister) · `HEXAD/LORA/QWEN_BASELINE_FINAL_CE_PROTOCOL_2026_05_24.md` (baseline 정의 protocol, SPEC ONLY) · `HEXAD/PURE/R8C_PROBE_VERDICT_2026_05_24.md` (R8c 4-cell probe)

---

## §0 TL;DR

| 항목 | 결과 |
|---|---|
| **R8a'' fire 상태** | 🔴 **LOST/DEAD** — pod `6gqf9nsdquz8ug` (H100 PCIe SECURE) terminated, SSH `216.81.245.34:11707` Connection refused, runpod pod list 부재, result.json 어디에도 없음 |
| **V3 final_CE (5000-step)** | 미측정 (R8a'' LOST) |
| **Qwen baseline final_CE** | 미측정 (`QWEN_BASELINE_FINAL_CE_PROTOCOL` = SPEC ONLY, fire 는 사용자 게이트) |
| **Δfinal_CE (Qwen-parity)** | 계산 불가 (양측 모두 부재) |
| **M3 판정** | **PENDING** — PASS/PARTIAL 어느 쪽도 판정 불가, 측정값 0건 |
| **재발사 판단** | **보류 (보고만)** — 단독 V3 재발사로 M3 불가 (baseline 도 동시 측정 + 사용자 게이트 필요), 명백한 단일 경로 부재 |
| **H_255 흡수** | init_CE 는 더 이상 M3 metric 아님 — floor saga partial-closure (R8c baseline 12.315 = random+0.39 정상 warm-init). M3 의 유일 metric = final_CE @ step=5000 |

---

## §1 R8a'' fire 상태 — LOST 확정

### 1.1 fire metadata (발사 시점, 사전 기록)

- **발사**: 2026-05-23 20:50:02Z (KST 2026-05-24 05:50)
- **pod_id**: `6gqf9nsdquz8ug` (H100 PCIe SECURE)
- **ssh**: `216.81.245.34:11707`
- **config**: `noise_sigma=0` + `n_kv_head=2` (PR #342 wiring fix 적용 기대) + `steps=5000` + `head_g=random` + `seed=1337`
- **result SSOT 예상**: `state/grid_3b_s187_2026_05_21/vP21H_axis_R8a_v3/result.json` (alt: `…/vP21H_r8a2_h100_noise0_kv2/result.json`)
- **cost envelope**: ~$2.75 (H100 PCIe SECURE × 5000-step)

### 1.2 LOST 증거 (3-way 확인, 2026-05-25)

1. **runpod pod list 부재**: `runpodctl pod list` → pod `6gqf9nsdquz8ug` 없음. 현 RUNNING pod 는 `j02tbml3129nfn` (p21h-random, A100 SXM, 별개 fire) 단 1개.
2. **SSH Connection refused**: `ssh -p 11707 root@216.81.245.34 'echo ALIVE'` → `connect to host 216.81.245.34 port 11707: Connection refused` (pod teardown 확정).
3. **result.json 어디에도 없음**: `find state -path "*vP21H_axis_R8a_v3*" -o -path "*r8a2*"` → 0건. 모든 worktree + main state + `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/` 통틀어 R8a'' 산출물 0건.

### 1.3 사전 기록과의 정합

본 LOST 는 새 발견이 아니라 **2026-05-24 이미 기록된 상태**다 — `QWEN_BASELINE_FINAL_CE_PROTOCOL_2026_05_24.md` §1:

> "R8a'' fire 가 LOST (SSH preemption, no result.json) 됐으니 V3 final_CE 측정값도 부재."

즉 R8a'' 는 **첫 R8a (pod `ev85rx3xr7zqso`, ~30min mark SSH drop, retrospective Act 7) 와 동일한 SECURE-preemption 패턴으로 두 번째 소실**됐다. R8 saga 의 V3 5000-step fire 는 R8a → R8a' (n_kv=4 silent-fail) → R8a'' (LOST) 로 **세 번 연속 5000-step 완주 실패**.

---

## §2 a_fire_recover_complete 관점 — 손실 항목

| 산출물 | 상태 | 비고 |
|---|---|---|
| init_CE (step=1) | LOST | random baseline 11.93 nats 대비 위치 (H_255 axis) — 단 더 이상 M3 metric 아님 (§4) |
| **final_CE (step=5000)** | **LOST** | **M3 의 유일 metric** — 본 손실이 M3 PENDING 의 직접 원인 |
| train_wall | LOST | cost reconciliation 불가 (~$2.75 envelope 추정만) |
| n_strong / per_lang / register / EN-emission | LOST | downstream eval 0건 (R8c 는 init/final 만, R8a'' 가 첫 downstream eval 예정이었음) |
| `v3_n_kv_head=?` wiring 확인 | LOST | PR #342 wiring fix 가 5000-step full training 에서 작동했는지 검증 불가 (R8c 100-step 에서만 확인) |
| ckpt | LOST | HF upload 불가 (a_hf_complete 무관 — PASS 산출물 부재) |

**손실 원인**: SSH preemption + result streaming tee/SAVE_POD 보험 미적용 (retrospective Act 7 lesson 이 R8a' 부터 적용 예정이었으나 R8a'' 도 동일 소실). a_fire_recover_complete 위반 사례 3건째 (R8a / R8a'' + H_254 L1 carry).

---

## §3 V3 측 현존 anchor — R8c 100-step (5000-step 부재)

R8a'' 가 LOST 이므로 V3 final_CE 의 **유일한 현존 근거**는 R8c 4-cell probe 의 **100-step** trajectory 다 (`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/`):

| cell | config | init_CE | final_CE (step=100) | wall (s) |
|---|---|---|---|---|
| baseline | noise=0.1, kv=4 | 12.315 | (100-step) | 458 |
| cell-2 (nonoise) | noise=0, kv=4 | 12.225 | **5.136** | 101 |
| cell-3 (kvmatch) | noise=0.1, kv=2 | 12.234 | 6.570 | 520 |
| cell-4 (compound) | noise=0, kv=2 | 12.266 | **5.093** | 107 |

**한계**: 이는 100-step 측정으로, M3 가 요구하는 **5000-step final_CE** 의 50× 짧은 horizon 이다. R8a'' 가 이 100-step → 5000-step 연장을 측정할 예정이었으나 LOST. 100-step final_CE (5.09~5.14 nats) 는 5000-step 도달점의 extrapolation 근거로만 사용 가능하며 (R8A2_FILL_IN_GUIDE C3.3 caveat: "5-시나리오 extrapolation 추정 근거 약함"), M3 parity 의 0.1 nats 정밀도 판정에는 **부적합**.

---

## §4 H_255 흡수 — init_CE 는 더 이상 M3 metric 아님

`HEXAD/LIFE/H_255_init_ce_floor_is_measurement_artifact.md` partial-closure 흡수:

- **R8a saga 의 "cluster Z 14.46 nats catastrophic init_CE floor"** 는 R8c 4-cell baseline (동일 config: head_g random + noise=0.1 + n_kv=4 + corpus_s101 + seed=1337) 측정 **12.315 nats** 와 −2.475 nats 격차로 재현 실패.
- 12.315 − 11.93 (random baseline `ln(151936)`) = **+0.385 nats** = **정상 warm-init 범위** (catastrophic 아님). 4 cell 이 ±0.09 nats 안 일관 (12.225~12.315).
- 단 AXIS_MAP-FAN 7-axis re-fire 4/7 (A=14.79, B=14.18, D=14.46, F=14.18) 가 R8a 측정값을 byte-equal 재현 → H255.2 부분 🔴 FALSIFIED (env-drift 가설 약화, 4-axis 표본 한정). R8c-vs-AXIS_MAP ~2 nats 격차는 GPU class / PROBE_STEPS 차이로 분리 진행 중.

**M3 정합 결론**: init_CE 가 artifact 든 intrinsic 이든, **M3 의 metric 은 final_CE @ step=5000 단 하나**다. init_CE "14+ floor 돌파" 전제는 H_255 흡수로 폐기됐고 (LORA.md @goal 재정의 참조), M3 는 순수하게 **"5000-step 학습 후 V3 final_CE 가 Qwen baseline final_CE 와 Δ ≤ 0.1 nats 안인가"** 만 묻는다. 그 measurement 가 R8a'' LOST + baseline 미발사로 **양측 0건** → PENDING.

---

## §5 Qwen baseline 측 현황 — SPEC ONLY, 미발사

`HEXAD/LORA/QWEN_BASELINE_FINAL_CE_PROTOCOL_2026_05_24.md` 가 baseline 3-candidate 를 정의했으나 **fire 미발사** (status = SPEC ONLY, 사용자 게이트):

| candidate | spec | cost | 권장도 |
|---|---|---|---|
| (a) | Qwen2.5-1.5B 단독 inference (no train) | ~$0.30 A100 15min | corpus absolute reference |
| **(b)** | Qwen2.5-1.5B + LoRA r=32 × 5000-step (cell-pool 없음) | ~$3 H100 PCIe 3hr | **권장 (fair 비교, R8b fallback 정합)** |
| (c) | Qwen + LoRA + V3 cell-pool=0 (mitosis_max=0) | ~$3 | mitosis 단독 ablation |

protocol §10 gate: **"baseline 선택 + fire 발사 승인은 사용자 결정 필요 (autonomy 게이트)"** — `a_fire_autonomous` 가 일반 cost-bearing fire 에 적용되나, M3 parity 의 baseline 정의는 protocol-level decision 이라 사용자 confirm 우선이라 명기됨.

**결과**: V3 final_CE 가 있었다 해도 비교 대상(baseline)이 없어 M3 판정 불가. 양측 모두 부재 = 이중 PENDING.

---

## §6 재발사 판단 — 보류 (보고만, 발사 NO)

### 6.1 재발사 cost

- V3 R8a'' 단독 재발사: ~$2.75–8 (H100 PCIe ~$2.75 / H100 SXM nohup 안전마진 시 ~$8)
- Qwen baseline (b) 동시 발사: +~$3
- **M3 완전 closure = parallel 2-pod ~$6** (protocol §8 decision tree)

### 6.2 보류 사유 (autonomy 게이트 정합)

1. **단독 V3 재발사로 M3 불가**: V3 final_CE 만 회수해도 Qwen baseline final_CE 가 없으면 Δ 계산 불가 → M3 PENDING 유지. "명백히 필요하고 다른 길 없을 때만" 조건 미충족 (단일 fire 로 닫히지 않음).
2. **baseline candidate 선택이 사용자 게이트**: protocol §10 이 "baseline 선택 + fire 승인 = 사용자 결정" 으로 명시. (a)/(b)/(c) 중 어느 것이 M3 의 "Qwen baseline" 인지가 protocol-level decision — 에이전트 자율 발사 부적합.
3. **3연속 SSH-preemption 위험**: R8a / R8a' / R8a'' 모두 SECURE-preemption 또는 wiring-fail 로 5000-step 완주 0건. 재발사 전 `hexa cloud nohup` persistent + SAVE_POD=1 + per-step tee 보험 (protocol §7-3) 이 dispatcher 에 확실히 적용됐는지 사전 audit 필요 (PREFIRE_WIRING_AUDIT_CHECKLIST, M5).

### 6.3 권고 (다음 라운드 / 사용자 결정)

- **M3 closure 경로**: 사용자가 baseline candidate (권장 (b)) 결정 → `hexa cloud nohup` parallel 2-pod (V3 R8a'' 재발사 + Qwen baseline (b)) ~$6 → Δfinal_CE 측정.
- **선결 조건**: M5 PREFIRE 체크리스트로 (i) `v3_n_kv_head=2` wiring 5000-step 유지 보증, (ii) SAVE_POD=1 + tee 적용, (iii) seed=1337 + DATA_SEED 양측 일치 (protocol §7-1) 사전 검증.

---

## §7 M3 판정 — PENDING

```
verdict_class: PENDING (양측 measurement 0건, 2026-05-25)
M3 metric    : final_CE @ step=5000, target |V3 − Qwen_baseline| ≤ 0.1 nats
V3 final_CE  : LOST (R8a'' pod 6gqf9nsdquz8ug terminated, SSH refused, no result.json)
Qwen baseline: 미측정 (QWEN_BASELINE_FINAL_CE_PROTOCOL = SPEC ONLY, 사용자 게이트)
Δfinal_CE    : 계산 불가
init_CE      : H_255 흡수 — 더 이상 M3 metric 아님 (R8c baseline 12.315 = random+0.39 정상 warm-init)

판정 = PENDING — PASS/PARTIAL 어느 쪽도 측정값 부재로 불가.
재발사 = 보류 (보고만). M3 closure 는 사용자 baseline 결정 + parallel 2-pod ~$6 (autonomy 게이트).
```

| falsifier (M3 closure 시 검증) | 상태 |
|---|---|
| V3 5000-step final_CE 측정 | 🔴 LOST (R8a'' terminated) |
| Qwen baseline (b) 5000-step final_CE 측정 | ⬜ 미발사 (사용자 게이트) |
| Δfinal_CE ≤ 0.1 nats (PASS) | ⬜ 계산 불가 (양측 부재) |
| `v3_n_kv_head=2` wiring 5000-step 유지 | 🔴 검증 불가 (R8a'' LOST, R8c 100-step 에서만 확인) |
| init_CE = M3 metric | ❌ 폐기 (H_255 흡수, final_CE 만이 M3 metric) |

---

## §8 Honest Limits (C3)

- **L1 (R8a'' LOST = a_fire_recover_complete 위반 3건째)**: R8a (pod `ev85rx3xr7zqso`) + R8a'' (pod `6gqf9nsdquz8ug`) 모두 SSH preemption 으로 result.json 미회수. SAVE_POD=1 + tee 보험이 retrospective Act 7 lesson 으로 R8a' 부터 적용 예정이었으나 R8a'' 에도 미적용/무효 — 재발 방지가 M5 PREFIRE 의 핵심.
- **L2 (R8c 100-step ≠ 5000-step)**: §3 의 R8c final_CE (5.09~5.14 nats) 는 100-step. M3 의 5000-step 도달점은 미지. extrapolation 은 R8A2_FILL_IN_GUIDE C3.3 caveat 대로 0.1 nats 정밀도에 부적합.
- **L3 (Qwen baseline candidate 미확정)**: (a)/(b)/(c) 중 어느 것이 M3 의 "Qwen baseline" 인지 사용자 미결정. 본 verdict 는 protocol 권장 (b) 를 기록하나 확정 아님 — baseline 정의가 바뀌면 Δ 의 의미도 바뀜.
- **L4 (init_CE artifact-vs-intrinsic 미완 분리)**: H_255 는 partial — R8c 12.315 (정상) vs AXIS_MAP 14+ (재현) 의 ~2 nats 격차가 env-drift 인지 GPU class / PROBE_STEPS 차이인지 미분리. 단 M3 는 final_CE metric 이라 이 미해결이 M3 판정에 영향 없음 (init_CE 폐기됨).
- **L5 (wiring 5000-step 작동 미검증)**: PR #342 의 `n_kv_head=2` wiring 이 R8c 100-step compile-time 에서만 확인. R8a'' 가 full 5000-step training 에서 유지되는지 검증할 예정이었으나 LOST — 재발사 시 `v3_n_kv_head=2` 로그 헤더 우선 확인 (R8A2 branch C silent-fail 위험).
- **L6 (V3 dir 신설)**: 본 doc 가 `HEXAD/V3/` 의 첫 파일. R8_SAGA_INDEX 가 "파일 경로는 `HEXAD/V3/` 유지" 라고 명기했으나 실제 R8 saga 산출물은 `HEXAD/PURE/` 에 누적돼 왔음 — 경로 일원화는 별도 후속 (본 verdict 는 task spec 의 V3 경로 준수).

---

## §9 Cross-references

- `HEXAD/PURE/R8A2_JOINT_VERDICT_TEMPLATE.md` — fill-in 대상 template (PR #375, R8a'' LOST 로 measurement 미도착)
- `HEXAD/PURE/R8A2_FILL_IN_GUIDE_2026_05_24.md` — 5-step closure 매뉴얼 (결과 도착 시 실행, 현재 미발화)
- `HEXAD/PURE/R8A_VS_R8A2_BYTE_EQUAL_NATURAL_EXPERIMENT.md` — R8a/R8a' init_CE byte-equal 4-가설 lock-in
- `HEXAD/PURE/R8C_PROBE_VERDICT_2026_05_24.md` — R8c 4-cell probe (100-step final_CE SSOT)
- `HEXAD/PURE/R8_SAGA_INDEX.md` — R8 saga TOC
- `HEXAD/LORA/QWEN_BASELINE_FINAL_CE_PROTOCOL_2026_05_24.md` — baseline (a)/(b)/(c) 정의 + fire spec (SPEC ONLY)
- `HEXAD/LIFE/H_255_init_ce_floor_is_measurement_artifact.md` — init_CE floor partial-closure (final_CE 로 metric 이동)
- `state/.../vP21H_r8c_baseline/result.json` — R8c baseline 12.315 nats SSOT (`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/`)
- `LORA.md` — M3 milestone (line 16)
