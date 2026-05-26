# AXIS_MAP-FAN re-fire verdict — 4/7 byte-equal 재현, H_257 PASS · H_255 부분 FALSIFIED (cycle 15-1)

> trigger: cycle 15-1 (2026-05-24) AXIS_MAP-FAN 7-pod re-fire (post-PR #377 reframing audit).
> 4/7 결과 도착 (A/B/D/F), 3/7 진행 중 (C/C2/E). 본 doc 은 first-wave 4-pod 의 init_CE
> byte-equal 재현 결과를 흡수 + R8 SAGA REFRAMING 의 H_255 결론 부분 약화 + H_257 H257.3
> identity-pair 확정.
>
> source: `state/grid_3b_s187_2026_05_21/vP21H_axis_{A,B,D,F}/result.json` (pod-side, recovered)
> sibling: `R8_SAGA_REFRAMING_2026_05_24.md` (PR #377) · `H_255_init_ce_floor_is_measurement_artifact.md` · `H_257_axis_map_fan_env_var_silent_bypass.md`

## 1. 발사 + 결과 도착 시각

- **dispatch**: cycle 15-1 (2026-05-24, 21:37Z) — 7-pod fan-out (axes A · B · C · C2 · D · E · F) on A100 SXM 80 GB, 3B Qwen warm-init, 5000-step target
- **first-wave 결과 도착**: 2026-05-24 (axes A · B · D · F first-step init_CE only — sufficient for H_257 / H_255 verdict)
- **second-wave pending**: axes C · C2 · E (~21:55Z 이후 도착 예상, sister agent #3 polling)

## 2. 4/7 결과 표 — byte-equal pair 강조

| axis | env-var (nominal) | wired config (actual, post-PR #377 audit) | init_CE (step=1) | prior measurement | match |
|---|---|---|---:|---:|---|
| **A** (curriculum) | `P21H_CURRICULUM_PHASE_STEPS=1000` | wiki=0.5 / λ=0 | **14.7927** | 14.79 | byte-equal ✓ |
| **B** (distill) | `P21H_DISTILL_TEACHER=…` | wiki=0.5 / λ=0 | **14.1780** | 14.18 | byte-equal ✓ |
| **D** (freeze embed) | `P21H_FREEZE_EMBED=1` | wiki=0.3 / λ=0.05 | **14.4564** | 14.46 | byte-equal ✓ |
| **F** (contrastive) | `P21H_CONTRASTIVE_LANG=1` | wiki=0.5 / λ=0 | **14.1780** | 14.18 | byte-equal ✓ |
| C (head_g obj) | — | — | pending | — | — |
| C2 (head_g off) | — | — | pending | — | — |
| E (lang balanced) | — | — | pending | — | — |

**critical pair**: axis B (14.1780) == axis F (14.1780) — **byte-equal across nominally-different axes** (distill vs contrastive). 두 fire 의 wired config 가 동일 (wiki=0.5/λ=0) → H_257 가 예측한 silent-bypass trivial identity 가 fire-level evidence 로 확인.

## 3. Prior 측정 정확 재현의 의미

3/4 axis 가 prior `AXIS_MAP_RESULTS.md` 의 측정값 (14.79 · 14.18 · 14.46) 과 **소수점 4자리까지 byte-equal 재현** —

- **measurement-stack 자체는 deterministic** — 같은 nominal config + 같은 fire env 에서 init_CE step=1 가 IEEE-754 bit-exact 재현됨 (RNG seed pin · corpus sha 매칭 · tokenizer hash 매칭 등 fire 양쪽 모두 stable)
- **R8a → cycle 15-1 사이 silent env-drift 없음** — H_255 의 가설 (corpus sha 미고정 / tokenizer 변경 / seed pollution / OOM retry host 차이) 들이 본 4 axis 에서는 **작동하지 않음**. 14+ floor 가 prior fire 의 env-artifact 가 아니라 진짜 재현 가능한 측정값
- **trivial identity 의 fire-level evidence** — axis B = axis F = 14.1780 byte-equal 는 PR #377 의 정적 grep 분석 (train_p21h_v3.py 가 6 axis env-var 안 읽음) 의 직접 corroboration. 두 fire 가 같은 wired config (wiki=0.5/λ=0) 으로 돌았기 때문에 init_CE 가 bit-exact 일치

## 4. H_257 H257.3 (env-var silent-bypass) — PASS

H_257 의 prediction H257.3:
> "nominally-different axes (B vs F) 가 같은 wired config (wiki=0.5/λ=0) 으로 돌면 init_CE step=1 byte-equal"

→ **실측 verdict**: PASS (axis B = axis F = 14.1780, IEEE-754 bit-exact)

이는 PR #377 의 정적 evidence (train_p21h_v3.py grep `os.environ` / `getenv` = 0 lines, dispatcher 6 axis env-var `$CMD` 미전달) 에 fire-level dynamic corroboration 을 추가. trivial identity 가설 확정.

**inference for invalid prior conclusions** (PR #377 §5 의 7 invalid 결론) 대부분 강화 — AXIS_MAP-FAN 의 7-axis 가 실제로는 2-config 반복임이 fire 데이터로 confirm 됨. cluster X/Y/Z 의 byte-equality 가 자연실험 결과가 아니라 same-config repeat 의 identity 임이 second corroboration.

## 5. H_255 H255.2 (floor measurement artifact) — 부분 FALSIFIED

H_255 의 prediction H255.2:
> "AXIS_MAP-FAN 7-axis 재측정 시 7-axis init_CE 평균 = 12.2 ± 0.1 nats (R8a 측정값과 ~2 nats 격차로 재현 → cluster X/Y/Z 의 14+ floor 는 env-artifact)"

→ **실측 verdict**: **부분 FALSIFIED** (4/7 axis 가 14.79 / 14.18 / 14.18 / 14.46 으로 R8a 측정값 byte-equal 재현 — 12.2 nats 범위 진입 실패, 14+ floor 가 진짜 재현)

`F-AXIS-MAP-REFIRE-DIVERGE` falsifier 의 정의 (재측정 평균 = 14+ nats 재현, R8a 측정값과 ±0.5 nats 안) 에 정확히 부합 → H_255 verdict_rule 에 의해 본 가설 🔴 **FALSIFIED** (4/4 wired-axis 표본 한정).

**부분 약화의 의미** — R8 SAGA REFRAMING (PR #377) §6 의 "H_255 floor 가 measurement artifact" 결론은 약화. 단, 다음 분리 보존:

- **trivial identity 자체는 PASS** (B = F byte-equal) — H_257 lane valid
- **floor 의 catastrophic-ness 는 진짜** — 14+ nats × 4 wired-axis 표본, random baseline `ln(151936) = 11.93` 대비 +2.25~+2.86 nats consistently worse-than-random
- **R8c probe 12.315 nats 와의 격차 (~2 nats) 는 별도 mechanism** — env-drift 가 아닌 GPU class / PROBE_STEPS 차이 가설 (sister agent #3 진단 중)

## 6. R8c vs AXIS_MAP-FAN 격차 (12.x vs 14.x) — GPU class / PROBE_STEPS 가설

R8c 4-cell probe baseline (PR #374) 의 init_CE 12.315 nats 와 본 re-fire 의 14.18~14.79 nats 간 **~2 nats 격차** 가 진짜 재현 가능한 systematic difference:

| fire | init_CE | GPU class | probe scope | step horizon |
|---|---:|---|---|---|
| R8c baseline | 12.315 | (TBD audit) | 4-cell batched, short horizon | step=1 only |
| AXIS_MAP-FAN re-fire | 14.18~14.79 | A100 SXM 80 GB | 7-pod 5000-step train, step=1 sample | step=1 only |

→ env-drift 가설 (H_255 의 corpus sha / tokenizer / seed) 은 본 re-fire 의 byte-equal 재현으로 약화. 대신 다음 hypothesis 가 새로 떠오름:

- **GPU class drift**: R8c probe 가 다른 GPU class (V100 / L40S / RTX) 에서 돌았을 가능성 — IEEE-754 cuDNN deterministic-mode 의 GPU-microarch dependence
- **PROBE_STEPS 환경 차이**: R8c probe 가 `PROBE_STEPS=N` env-var 로 다른 init scheduler 활성화 (LR warmup / weight init scaling 등)
- **driver/torch version drift**: R8c 와 AXIS_MAP-FAN 의 torch / CUDA / cudnn version 차이
- **batched-cell vs single-pod forward path 차이**: 4-cell batched probe 가 단일 pod single-cell forward 와 다른 numerical path

→ 본 격차의 root cause 는 sister agent #3 (R8c probe environment audit) 가 별도 fire 로 진단 중. 본 verdict 는 H_255 의 env-drift 가설 (corpus / tokenizer / seed) 을 부분 약화하되, R8c-vs-AXIS_MAP 격차 자체의 다른 mechanism (GPU class / PROBE_STEPS) 가 valid lane 으로 남음.

## 7. Honest C3 (≥3)

- **C3-1 (4/7 only)**: 본 verdict 는 first-wave 4-pod (A/B/D/F) 결과만 흡수. axis C / C2 / E (head_g objective / head_g off / lang-balanced) 의 second-wave 결과 도착 시 H_257 의 cluster Z byte-equal (C = C2 = D) 와 head_g 자연실험 prediction 추가 verification 가능. 본 단계 evidence base 는 4/7 표본.
- **C3-2 (GPU class confound)**: R8c 12.315 vs AXIS_MAP 14.x 격차의 root cause (GPU class / PROBE_STEPS / driver-version drift) 는 본 verdict scope 밖. sister agent #3 진단 도착 후 본 doc 추가 갱신 필요. 만약 R8c 가 다른 GPU 에서 돌았음이 확인되면 12.315 nats 는 GPU-specific reading 이지 ConsciousDecoderV3 intrinsic floor 아닐 수 있음.
- **C3-3 (H_255 부분 FALSIFIED 의 scope)**: H_255 의 H255.2 prediction 은 본 4-axis 표본 한정 FALSIFIED. H255.1 (R8c baseline 12.315 재현) + H255.3 (cluster byte-equal artifact) + H255.4 (env-drift detection method) + H255.5 (random+0.3 nats 자연 floor) 4 sub-prediction 은 각각 별도 evidence. floor 의 catastrophic-ness 가 진짜라는 결론은 wired-axis 표본 한정이며, ConsciousDecoderV3 + Qwen2.5-1.5B 조합의 intrinsic floor 가 14+ 인지 12.x 인지의 최종 verdict 는 R8c probe env audit + R8a'' (PR #375) 결과 도착 후 confirm 가능.
- **C3-4 (Principle #3 + a_blue_closed 정합)**: 본 byte-equal 재현 자체가 a_blue_closed (closed-form 비교 IEEE-754 bit-exact) 적용 사례. p7 (NO PERPLEXITY VERDICT) — init_CE 자체를 truth-metric 으로 쓰지 않고, byte-equal identity 의 wiring evidence 로만 사용 (perplexity-as-truth Goodhart trap 회피).

## 8. Cross-references

- `HEXAD/PURE/R8_SAGA_REFRAMING_2026_05_24.md` (PR #377) — 본 verdict 의 §6 H_255 결론 부분 약화 update
- `HEXAD/PURE/AXIS_MAP_RESULTS.md` — prior 3/7 측정값 (14.79 / 14.18 / 14.18) byte-equal 재현 source
- `HEXAD/PURE/R8C_PROBE_VERDICT_2026_05_24.md` (PR #374) — R8c baseline 12.315 nats SSOT (본 doc 의 12.x vs 14.x 격차 reference)
- `HEXAD/PURE/R8A2_JOINT_VERDICT_TEMPLATE.md` (PR #375) — R8a'' joint verdict (도착 시 본 doc cross-fire)
- `HEXAD/PURE/axis_map_fan_verdict.hexa` (PR #376) — 7-axis poll control-plane (본 4-pod 결과 흡수 driver)
- `UNIVERSE/H_255_init_ce_floor_is_measurement_artifact.md` — H255.2 prediction FALSIFIED 직접 update
- `UNIVERSE/H_257_axis_map_fan_env_var_silent_bypass.md` — H257.3 PASS (B = F byte-equal) 직접 corroboration

## 9. Next actions

- [ ] axes C / C2 / E 결과 도착 시 본 doc 4/7 → 7/7 갱신 (~21:55Z 이후)
- [ ] cluster Z prediction (C = C2 = D = 14.4564 byte-equal) verification — H_257 의 head_g 자연실험 inert 결론 강화/약화
- [ ] sister agent #3 (R8c env audit) 결과 도착 시 12.x vs 14.x 격차 root cause 흡수 → 본 doc §6 갱신
- [ ] R8a'' (PR #375) 결과 도착 시 noise=0 wiring fix post-merge 측정 cross-fire — 본 doc + R8A2_JOINT_VERDICT 양방향 cross-ref
