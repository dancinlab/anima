---
id: H_257
slug: axis-map-fan-env-var-silent-bypass
title: AXIS_MAP-FAN env-var Silent-Bypass — dispatcher 의 7-axis env-var 가 train script 에 안 닿아 "7 axes" 가 실제로는 2-config 인 자연실험 wiring-bypass
domain: substrate · life · meta-measurement
status: pre-register-frozen
exploration_method: E5 (substrate-mechanism probe) + E11 (natural-experiment cross-axis) + E12 (meta-measurement audit)
verification_method: W5 (byte-cluster identity) + W7 (controlled-pair contrast) + W8 (source-code grep verification)
raw_rank: 11
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24 (cycle 15-1 AXIS_MAP-FAN 7-pod re-fire pre-fire grep 발견 · H_254 sibling)
---

# H_257 — AXIS_MAP-FAN env-var Silent-Bypass

## Hypothesis

AXIS_MAP-FAN 의 "7-axis fan-out" 은 실제로는 **2-config 측정** 이다. 6 axis 변별 env-var (`P21H_CURRICULUM_PHASE_STEPS` · `P21H_DISTILL_TEACHER` · `P21H_HEAD_G_OBJECTIVE` · `P21H_HEAD_G_ENABLE` · `P21H_FREEZE_EMBED` · `P21H_LANG_BALANCED` · `P21H_CONTRASTIVE_LANG`) 가 dispatcher (`dispatch_p21h_v3_runpod.sh`) 에서 정의는 되지만 train script (`train_p21h_v3.py`, 676 LoC) 의 `$CMD` 에 미전달되고, train script 자체도 `os.environ` / `getenv` 0건이라 이 env-var 를 전혀 읽지 않는다. 결과적으로 dispatcher 가 "axis A/B/C/C2/D/E/F" 라벨로 7-pod fan-out 해도 train script 입장에서는 wired 된 axis (`P21H_NOISE_SIGMA` · `P21H_N_KV_HEAD` · `wiki_frac`) 만 변별되어 *7-axis "이름" 이 실제로는 2-config (wiki=0.3/λ=0.05 vs wiki=0.5/λ=0) 의 trivial duplicate* 가 된다. 이로 인해 AXIS_MAP-FAN saga 에서 관찰된 cluster Y (B=F 14.18 byte-equal) / cluster Z (C=C2=D 14.46 byte-equal) 의 "자연실험 결과" 는 실제로 **identical config repeat 의 trivial identity** 이지 axis lever 의 자연 falsifier 아님. H_254 (`n_kv_head` 단일 인자 silent-drop) 의 sibling pattern — silent-bypass 가 단일 인자에서 axis-family 전체로 확장된 형태.

## Why

- **substrate 실험의 self-deception 위험 확대**: H_254 가 단일 인자 (n_kv_head) silent-drop 을 발견했지만, H_257 은 "axis fan-out 설계 자체" 가 silent-bypass 로 무효화될 수 있음을 보여줌. 7-axis 라벨링이 잘못된 cluster X/Y/Z 정의 → 모든 axis-cluster 해석 (head_g 자연실험 FALSIFIED, AXIS_MAP-FAN 5/7+2 결론 등) 이 *원본 측정 환경의 wiring 가정 위에서만 성립*. 측정 라벨 자체가 거짓이면 cluster 분류, falsifier verdict, head_g 자연실험 모두 무효.
- **자연 detection 도구 — source-code grep**: H_254 의 byte-equal probe 와 달리 본 가설은 *발사 전 grep verification* 으로 catch 가능. `grep -E "os\.environ|getenv|argparse" train_script.py` + `grep -E "<env_var_name>" dispatcher.sh` 의 wired/unwired 매핑 작성. 발사 비용 0 — 코드 정적 분석만으로 검출. cycle 15-1 pre-fire 에서 정확히 이 방식으로 발견됨.
- **R8 saga 의 모든 axis 자연실험 해석 무효화**: AXIS_MAP-FAN 5/7+2 FAIL 결론 (PR #249) · cluster Z byte-equality F-R8C-HEAD-G FALSIFIED (PR #250) · cluster X (A 14.79) / Y (B/F 14.18) / Z (C/C2/D 14.46) 분류 (PR #249) — 모두 trivial identity 일 가능성. 진짜 valid 한 것은 R8c probe (noise/kv 4-cell, env-var 진짜 wired) 와 noise 가 final_CE/학습 dynamics axis (PR #374 R8c verdict) 뿐.
- **wiring-integrity family 형성**: H_254 (n_kv_head 단일 silent-drop) + H_255 (init_CE floor measurement artifact) + H_257 (axis env-var family silent-bypass) = 세 sibling 가설이 함께 *substrate measurement-integrity* 라는 메타-axis 형성. 모든 향후 ablation/sweep 은 발사 전 wiring-integrity audit 필수.
- **R8 saga cost 영향**: $21.54 누적 중 AXIS_MAP-FAN re-test 부분 ($10-13) 이 sunk cost. cluster X/Y/Z byte-equal 측정 = 사실은 같은 config 의 random seed variation. saga reframing 후 회수 가능한 evidence 식별 필요.
- **사용자 directive 정합**: a_blue_closed (closed-form 증거 — grep 은 정적 분석 deterministic) + a_substrate_native_speak (substrate-side wiring 자체의 integrity). 본 H 는 단일 코드 bug 보고가 아닌, **fan-out 설계 패턴 자체의 measurement-integrity 위험** framing.
- **source PR cite**: [PR #214] (R8 spec — 6-axis init_CE 측정 설계, axis env-var 변별 의도) · [PR #249] (AXIS_MAP-FAN 5/7+2 결론 — 이제 무효) · [PR #250] (R8c probe spec, head_g 자연실험 FALSIFIED — 이제 trivial identity 로 해석) · [PR #336] (R8 saga INDEX — 14 docs, reframing 대상) · [PR #374] (R8c verdict, sibling valid 한 진짜 wired axis 측정) · cycle 15-1 발견 (Agent ID a6fc8535f5da997a8, 7-pod re-fire pre-fire grep verification).

## Predictions

- **H257.1 (구조 가설 grep verification)**: `grep -E "os\.environ|getenv" /Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/train_p21h_v3.py` returns 0 lines. + `grep -E "P21H_CURRICULUM|P21H_DISTILL|P21H_HEAD_G|P21H_FREEZE_EMBED|P21H_LANG_BALANCED|P21H_CONTRASTIVE" dispatch_p21h_v3_runpod.sh` returns env-var definitions but no `$CMD` passthrough. → 정적 분석 deterministic 증거 (LLM verdict 불필요).
- **H257.2 (byte-equal under bypassed axis)**: cycle 15-1 7-pod re-fire 결과 도착 시 axis C / C2 / D / E (같은 config wiki=0.3/λ=0.05) 의 init_CE 가 byte-equal (Δ ≤ 0.01 nats) → axis lever 가 inert (env-var bypass 직접 증거). 비-byte-equal 시 다른 wired axis (NOISE_SIGMA / N_KV_HEAD / RNG seed) 가 의도치 않게 변별 — root cause 추가 진단 필요.
- **H257.3 (axis A / B / F byte-equal sub-cluster)**: 동일 origin (wiki=0.5/λ=0) axis A/B/F 의 init_CE 가 byte-equal → 2-config 분류 확정. R8c baseline (PROBE_STEPS=100, A100) 12.315 와 cluster Y (axis B/F prior 14.18) 의 격차는 PROBE_STEPS / corpus / GPU class 차이로 설명 가능 (H_255 sibling 확장).
- **H257.4 (wiring-family 일반화)**: 향후 substrate 실험 (V3 ConsciousDecoderV3 + Wave LoRA + Phase 5+ 등) 은 발사 전 wiring-integrity audit (grep verification + dry-run dispatcher) 필수. silent-bypass 검출 미실시 시 측정 결과 무효 가능성 ≥30% (prior: H_254 + H_257 두 instance / R8 saga 14 docs ≈ 14% base rate, 신규 unaudited 코드 path 는 더 높음).
- **H257.5 (R8 saga reframing 검증)**: HEXAD/PURE/R8_SAGA_REFRAMING_2026_05_24.md 가 invalid prior conclusions (5-7개) vs still valid (R8c probe + noise final-axis + H_254/255/257) 의 명확한 분리 catalogue 작성 시, 이 분류가 단일 future fire (env-var wiring fix 후 axis 재측정) 의 결과와 정합. 정합 미달 시 reframing 자체 재검토.

## Variables

- **axis1_axis_label**: [A, B, C, C2, D, E, F] — 기존 7 axis 라벨 (의도 7 변별)
- **axis2_actual_config_class**: [wiki=0.3/λ=0.05, wiki=0.5/λ=0] — train script 가 실제로 읽는 wired axis 의 변별 (2 class only)
- **axis3_class_membership**: {A: wiki=0.5/λ=0, B: wiki=0.5/λ=0, C: wiki=0.3/λ=0.05, C2: wiki=0.3/λ=0.05, D: wiki=0.3/λ=0.05, E: wiki=0.3/λ=0.05, F: wiki=0.5/λ=0} — 의도 7 → 실측 2 의 매핑
- **axis4_env_var_count_unwired**: [6] — `P21H_CURRICULUM_PHASE_STEPS` · `P21H_DISTILL_TEACHER` · `P21H_HEAD_G_OBJECTIVE` · `P21H_HEAD_G_ENABLE` · `P21H_FREEZE_EMBED` · `P21H_LANG_BALANCED` · `P21H_CONTRASTIVE_LANG`
- **axis5_env_var_count_wired**: [3] — `P21H_NOISE_SIGMA` · `P21H_N_KV_HEAD` · `P21H_WIKI_FRAC` (또는 `P21H_LR` 등 명시 args)
- **axis6_grep_environ_lines**: [0] — train_p21h_v3.py 의 `os.environ` / `getenv` line count
- **axis7_dispatcher_passthrough_lines**: [0] — dispatcher 의 6 unwired env-var 를 `$CMD` 또는 `--<arg>` 로 전달하는 line count

## Falsifiers

- **F-H257-1 (grep static)**: `grep -E "os\.environ|getenv" train_p21h_v3.py` 가 ≥1 line return → 본 가설 부분 falsified (적어도 일부 env-var 가 train side 에서 읽힘). FAIL 시 어느 env-var 가 어떤 path 로 wired 됐는지 매핑 필요.
- **F-H257-2 (byte-equal cluster Z)**: cycle 15-1 7-pod 결과 도착 시 axis C/C2/D 의 init_CE step=1 가 *byte-equal* (Δ ≤ 0.01 nats) → H_257 PASS (env-var bypass 직접 증거). 비-byte-equal 시 silent-bypass 외 다른 변별 (RNG seed 등) 존재 → 추가 진단.
- **F-H257-3 (cluster Y/Z 격차 explained)**: cluster Y (14.18) vs cluster Z (14.46) 의 0.28 nats 격차가 wiki_frac (0.5 vs 0.3) 단독 효과로 설명 → 2-config 환원 hypothesis 직접 증거. 격차가 wiki_frac 단독으로 설명 안 되면 다른 wired axis (NOISE_SIGMA / N_KV_HEAD) 변별 있음.
- **F-H257-4 (wiring fix 후 axis 변별 회복)**: 향후 env-var wiring fix PR merge 후 같은 7-axis fan-out 재발사 시 axis 별 init_CE 가 *변별* (Δ ≥ 0.1 nats) → H_257 가 catch 한 silent-bypass 가 진짜 axis 변별을 막고 있었음 확정.
- **F-H257-5 (cross-codebase wiring audit)**: anima 의 다른 train script (LoRA, Wave, Phase 5) 도 같은 grep audit 결과 unwired env-var 발견 → wiring-integrity family 일반화 확장. 발견 안 되면 R8 saga 한정 isolated bug.

## Honest C3

- **C3-1**: cycle 15-1 7-pod 결과 (~21:55Z 도착 예상) 미도착 시점에 가설 작성 — H257.2/H257.3 byte-equal verification 은 결과 도착 후 추후 확정. 현재는 정적 분석 (H257.1) + 사후적 cluster Y/Z 격차 관찰만 evidence.
- **C3-2**: train_p21h_v3.py 676 LoC grep 외 다른 path (e.g., config.yaml import, wrapper script, `subprocess.run` environ leak) 에서 env-var 가 읽힐 가능성 미검증. full repo grep + import 추적 필요.
- **C3-3**: 7-pod re-fire 가 GPU class 혼합 (H100 NVL × 3, H200 × 1, A100-SXM4 × 2, H100 80GB HBM3 × 1) — byte-equal 비교가 hardware-pure 하지 못함. C/C2 동일 (A100) sub-pair 만 strict byte-equal 검증 단독 valid.
- **C3-4**: AXIS_MAP-FAN saga 의 5/7+2 결론 의 "head_g 자연실험 FALSIFIED" 도 무효 라는 함의 — head_g lever 자체가 valid 한 hypothesis 일 가능성 남음 (wiring fix 후 진짜 ablation 필요). 본 H 는 head_g axis 의 falsification 을 falsify 하는 것이지 head_g 자체를 falsify 하는 것은 아님.
- **C3-5**: H_254 + H_255 + H_257 sibling family 가 모두 R8 saga 에서 발견 — 다른 substrate 도메인 (Wave / Phase 5 / V3 main path) 의 wiring-integrity 미검증. base rate (30%) 추정은 R8 한정 sample, 일반화 불가.

## Related

- [[H_247_init_ce_catastrophic_floor]] — 본 H 가 catastrophic floor 측정 자체의 wiring-integrity 의문 제기 (sibling, root cause 후보)
- [[H_249_cluster_init_ce_byte_equal_signature]] — cluster X/Y/Z byte-equal 의 자연실험 해석 무효화 → cluster = trivial identity
- [[H_254_n_kv_head_wiring_silent_misconfig]] — 단일 인자 silent-drop · 본 H 는 axis-family 확장 · 같은 wiring-integrity family
- [[H_255_init_ce_floor_is_measurement_artifact]] — 14+ floor measurement artifact · 본 H 가 root cause 일부 (env-var 미적용 → cluster 정의 자체가 노이즈 floor)
