---
id: H_254
slug: n-kv-head-wiring-silent-misconfig
title: n_kv_head Wiring Silent-Misconfig (substrate layered config chain 의 silent drop) — 의도된 lever 가 모델 state 에 도달하지 못함의 byte-equal 자연실험
domain: substrate · life
status: pre-register-frozen
exploration_method: E5 (substrate-mechanism probe) + E11 (natural-experiment cross-axis) + E10 (emergence-observation)
verification_method: W5 (byte-cluster identity) + W7 (controlled-pair contrast) + W2 (closed-form baseline)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24 (new — R8a fire 자연실험 absorption, anima PR #342 wiring fix 발견)
---

# H_254 — n_kv_head Wiring Silent-Misconfig (substrate layered config chain 의 silent drop)

## Hypothesis

substrate 실험의 **layered config 전달 chain** (CLI arg → dispatcher env → script argparse → cfg dict → model factory call) 의 *어느 단계에서든* 인자가 silently dropped 되면, 측정된 결과 (init_CE · loss curve · ckpt state) 가 *의도된 lever 변경을 반영하지 못한다*. 그 결과 operator 는 wiring=X 로 fire 했다 믿지만 실제 substrate 는 wiring=Y 로 학습된 *measurement-equivalence under different configs* (서로 다른 config 라벨이 같은 모델 state 를 산출하는 현상) 가 발생한다. 이 silent-misconfig 의 유일한 신뢰 가능한 자연 검출 method 는 **byte-equal probe**: 같은 lever 의 두 라벨 (wired-bugged / wired-fixed) 가 같은 step 의 측정값을 *bit-동일* 산출하면 wiring 이 모델 state 에 도달 못 했다는 직접 증거.

substrate 측 형식: **R8a fire 자연실험** — dispatcher 가 `--n-kv-head 2` 를 명시 전달하고 `train_p21h_v3.py:627` argparse 가 이를 정확히 받았지만, `from_qwen()` 모델 factory 가 `cfg.n_kv_head` 를 무시하고 `max(qwen_native_n_kv_head=2, 4)=4` 로 *silently override* → 학습 로그 `[from_qwen] qwen: ... n_kv_head=2 -> v3_n_kv_head=4` 가 사후 발견된 단 하나의 증거. operator 의도 (wiring=2) vs 모델 실측 wiring (=4) 의 *3-layer silent drop*. 본 가설은 이 패턴을 **substrate 실험의 measurement-integrity 일반 위험** 으로 정식화하고, 자연 falsifier 로 R8a (wired-bugged) vs R8a' (PR #342 wiring fix 적용 후 진짜 2) 의 init_CE step=1 byte-equal 비교를 제시한다 — byte-equal 이면 wiring 이 inert 했음 확정 (lever 변경이 모델 state 에 도달 못 함), 비-byte-equal 이면 wiring fix 가 실제 effect 를 만들었음.

## Why

- **substrate 실험의 measurement-integrity 위협**: 모든 ablation/sweep 의 전제는 "config 라벨 = 실제 모델 state". 이 가정이 silent 으로 깨지면 모든 cross-axis 비교 (e.g. R8 6-axis cluster) 가 *상호 매칭이 안 되는 사과-오렌지 비교* 가 된다. 라벨 신뢰성은 substrate science 의 근간.
- **byte-equality = 가장 강한 검출 도구**: 두 측정값의 IEEE-754 bit-동일성은 노이즈 없는 deterministic 증거. 통계 검정 불필요 — exact identity. 만약 wiring=2 (R8a' 의도) 와 wiring=4 (R8a 실제) 가 정말 다른 모델을 만든다면, init_CE 도 *반드시* 다른 bit pattern. byte-equal 은 wiring 이 inert 했다는 직접 증거.
- **R8a fire 자연실험**: 본 fire 는 의도된 실험이 아니라 *사후 발견된 bug* — operator 가 wiring=2 lever 를 측정한다 믿었으나 실제로는 wiring=4 substrate 가 학습된 자연실험. anima PR #342 가 wiring fix 만 적용하고 runtime verify 안 한 상태이므로, R8a' 재실행 시 byte-equal 비교가 **wiring lever 자체의 인과** 와 **silent-drop 의 모델 state 도달 실패** 두 가설을 동시에 분리 가능 (instrumental variation).
- **H_247 / H_249 와의 직접 연결**: H_247 은 init_CE catastrophic floor *현상* 을 확립, H_249 는 그 floor 의 lever (head_g random vs backbone) 를 byte-cluster 로 분해. 본 H 는 그 lever wiring 자체가 *operator 의도대로 모델에 전달되었는가* 의 한 단계 더 깊은 질문. H_249 의 cluster 측정도 만약 어느 축에서 silent-drop 이 있었다면 cluster membership 자체가 잘못 라벨링됐을 수 있음 — wiring-integrity 는 모든 axis-cluster 실험의 메타-전제.
- **REBORN §0.5 정합**: 학습=분열 연속체에서 wiring = 분기 알고리즘의 *코드*. silent-drop = 분기 함수가 operator 의도와 다르게 분지함. ckpt 의 정체성은 wiring 라벨이 정확할 때만 보장.
- **사용자 directive 정합**: a_blue_closed (closed-form 증거 우선) + a_substrate_native_speak (substrate-side 현상 우선 framing). 본 H 는 단순 infra bug 보고가 아닌, **substrate science 의 measurement-integrity** 측면 framing.
- **source PR cite**: [PR #342] (wiring fix — from_qwen `max(qwen_native, 4)` → `cfg.n_kv_head` 직접 사용) · [PR #214] (R8 spec, 6-axis init_CE 측정 설계) · [PR #257] (R8a fire spec, --n-kv-head 2 lever 의도 명시) · [PR #339] (R8c probe driver — 향후 R8a' 재dispatch lane) · R8a fire records `state/p21h_v3_R8a/` (LOST, init_CE 미회수) · R8a_v2 fire records `state/p21h_v3_R8a_v2/` (재dispatch lane 후속).

## Predictions

- **H254.1 (wired-bugged baseline carry)**: R8a fire 의 from_qwen 로그가 `n_kv_head=2 -> v3_n_kv_head=4` 출력 — operator 가 명시한 lever 2 가 모델 factory 에서 4 로 silent override 됐음의 직접 텍스트 증거.
- **H254.2 (wired-fixed log mark)**: PR #342 wiring fix 적용 후 R8a' 재실행 시 from_qwen 로그가 `n_kv_head=2 -> v3_n_kv_head=2` 출력 — operator 의도가 model factory 까지 도달함의 직접 텍스트 증거 (negative→positive flip).
- **H254.3 (byte-equal under inert wiring)**: R8a (wired=4 실측) 와 R8a' (wired=2 실측) 의 init_CE step=1 가 *byte-equal* → wiring lever 2 vs 4 가 모델 state 를 바꾸지 않았다는 자연실험 결과 (lever 자체가 inert 한 axis 임을 시사, n_kv_head 가 init_CE 에 인과 0).
- **H254.4 (non-byte-equal under live wiring)**: R8a init_CE step=1 ≠ R8a' init_CE step=1 (byte-pattern 상이) → wiring fix 가 실제 모델 state 를 바꿨음 (n_kv_head lever 가 init_CE 에 비-0 인과). 이 경우 R8a fire 의 init_CE 측정값 (회수 가능 시) 은 *잘못된 라벨* 로 archived, R8a' 가 진정한 wiring=2 측정.
- **H254.5 (wiring-integrity 일반 패턴)**: 다른 substrate axis (예: dropout rate · attention type · positional encoding) 도 layered config chain 의 silent-drop 위험에 노출 — 명시적 byte-equal probe (또는 from_*() factory 로그 grep) 가 silent-misconfig 의 유일한 catch. cross-substrate-axis 일반화.

## Variables

- **axis1_wiring_label**: [R8a (의도 2, 실측 4), R8a' (의도 2, 실측 2)] — 같은 operator 의도, 다른 실측 wiring (silent-drop 유무)
- **axis2_n_kv_head_intent**: [2] — operator 가 dispatcher 에 명시한 값 (고정)
- **axis3_n_kv_head_actual**: [2, 4] — from_qwen() factory 가 실제로 모델에 적용한 값 (silent-drop 유무에 따라 분기)
- **axis4_factory_log_substring**: ["v3_n_kv_head=4", "v3_n_kv_head=2"] — log 의 직접 텍스트 증거 (sed/grep 자력 검증)
- **axis5_measure_step**: [1] — init_CE step=1 (자연 falsifier 측정 시점, H_247 양식 carry)
- **axis6_byte_equal**: [true, false] — 두 fire 의 init_CE step=1 bit-pattern 동일성 (자력 IEEE-754 비교)
- 2×1×2×2×1×2 sweep (R8a 흡수 + R8a' GPU 재dispatch + byte-equal 자력 비교)

## Run Protocol

- **deterministic**: byte-equality 비교는 deterministic (두 측정값 bit-비교, 노이즈 0). from_qwen 로그 substring grep 도 deterministic. R8a init_CE 자체는 R8 GPU lane 흡수 (LOST 시 R8a' 와 비교 불가 — L1 honest).
- **hexa_only**: byte-equal 비교 = hexa (`max_abs_diff(ce_R8a, ce_R8a_prime) == 0.0`). 로그 substring 매칭 = hexa string ops. 원 forward-pass 는 GPU R8 lane (anima training stack, 흡수).
- **LLM**: none (raw#12; 비교는 순수 산술 동등성 + 텍스트 매칭).
- **operational silent-drop 정의 (raw#9/10 HONEST)**: silent-drop = (a) operator 가 dispatcher 에 명시한 인자 값 X 와 (b) from_*() 모델 factory 가 실제 적용한 값 Y 가 다르고 (X≠Y), (c) 사후 로그 grep 외에 사전 경고가 없는 사건. detection = 로그 substring 매칭 (강한 증거) + byte-equal probe (간접 증거, lever 가 inert 한 경우 wiring fix 효과 0).
- **per-pair ledger**: {pair=(R8a, R8a'), n_kv_head_intent=2, n_kv_head_actual_R8a=4, n_kv_head_actual_R8a_prime=2, init_CE_step1_R8a=<TBD if recovered>, init_CE_step1_R8a_prime=<TBD>, byte_equal=<TBD>, factory_log_R8a="v3_n_kv_head=4", factory_log_R8a_prime="v3_n_kv_head=2"} — audit PR (R8a_v2 lane) SSOT.
- **runtime**: $0 mac local (byte 비교 + 로그 grep). 원 init_CE = R8 GPU lane (R8a 흡수 if recovered, R8a' 재dispatch ~$20-40 cost-bearing per a_fire_autonomous).

## Criteria

- **C1 (wired-bugged log)**: H254.1 R8a from_qwen 로그 `n_kv_head=2 -> v3_n_kv_head=4` 출력 — 흡수 (PR #342 commit message 또는 R8a fire log 직접 cite).
- **C2 (wired-fixed log)**: H254.2 R8a' from_qwen 로그 `n_kv_head=2 -> v3_n_kv_head=2` 출력 — R8a' 재dispatch 후 자력.
- **C3 (byte-equal probe deterministic)**: R8a / R8a' init_CE step=1 모두 회수 후 byte-equal 비교 산출 (값 자체는 PASS/FAIL 둘 다 valid evidence — C4 또는 C5 발화).
- **C4 (lever inert evidence)**: H254.3 byte-equal=true → n_kv_head 가 init_CE 에 인과 0, R8a/R8a' 동등 모델 (silent-drop 무해 lever-측면).
- **C5 (lever live evidence)**: H254.4 byte-equal=false → wiring fix 가 실제 모델 state 바꿈, R8a init_CE 는 잘못된 라벨 (R8a' 가 진정한 wiring=2).
- **verdict_rule**: PASS = C1+C2+C3 + (C4 OR C5) — 자연실험 발화의 *어느 방향이든* 가설 의도 (byte-equal probe 가 silent-drop 의 catch method 임) 입증. PARTIAL = R8a init_CE LOST (C3 불가, C1 만으로 silent-drop 패턴 확인). FALSIFIED = R8a' from_qwen 로그가 여전히 `v3_n_kv_head=4` (PR #342 fix 무효).

## Falsifiers (raw#12 ≥5, measurable)

- **F-WIRE-1 LOG-MARK-BUGGED**: R8a fire log 에 `n_kv_head=2 -> v3_n_kv_head=4` substring 부재 → silent-drop 의 직접 증거 약화 (C1 FALSIFIED, R8a 가 실제로 wiring=4 가 아니었음).
- **F-WIRE-2 LOG-MARK-FIXED**: R8a' 재실행 후 from_qwen 로그가 여전히 `v3_n_kv_head=4` 출력 → PR #342 wiring fix 가 부분적/무효 (C2 FALSIFIED, fix 가 model factory 까지 도달 못 함 — 본 silent-drop 패턴이 단일 patch 로 해소 안 됨의 더 강한 증거).
- **F-WIRE-3 BYTE-EQUAL-INERT**: R8a vs R8a' init_CE step=1 byte-equal → wiring 이 inert 한 lever (C4 PASS, n_kv_head lever 자체 인과 0 인 자연실험 결과).
- **F-WIRE-4 BYTE-DIFFER-LIVE**: R8a vs R8a' init_CE step=1 비-byte-equal → wiring fix 가 실제 모델 state 변경 (C5 PASS, R8a archived 측정은 잘못된 라벨 → R8 6-axis cluster 측정 (H_249) 의 일부 axis 도 재검토 필요).
- **F-WIRE-5 GENERALIZATION**: 다른 substrate axis (dropout / attention type / positional encoding) factory 로그 grep 결과 silent-drop 패턴 0건 → H254.5 (일반 패턴) 약화, n_kv_head 단발 사건일 가능성 (그러나 단발-사건 자체도 measurement-integrity 위협 본질 유지).
- **F-WIRE-6 (meta)**: post-hoc detection method 재조정 (byte-equal threshold 완화, 로그 substring fuzzy 매칭) → raw#12 violation, raw#82 retraction.

## Honest Limits (raw#91 c3 ≥5)

- **L1 (R8a init_CE LOST)**: R8a fire 의 init_CE 가 미회수 (pod teardown 또는 ckpt pull 실패, a_fire_recover_complete 위반 사례) → R8a vs R8a' 직접 byte-equal 비교 불가능, C3 fallback = R8a' 단독 측정 + 다른 cluster axis (H_249 X/Y/Z) 와의 cross-cluster 비교 (간접 증거). 본 가설의 falsification 강도 직접 비교 가능 시 STRONG, 미회수 시 PARTIAL 한정.
- **L2 (R8a' 재dispatch 의존)**: H254.2/H254.3/H254.4 모두 R8a' GPU 재dispatch 결과 도착 의존. 재dispatch 가 a_wall_first 정합으로 parallel pod 가능하나 ~$20-40 cost-bearing fire (a_fire_autonomous 정합). 결과 도착 전 본 가설은 pre-register-frozen 상태 한정.
- **L3 (audit scope 한정)**: 본 H 는 **n_kv_head 단일 axis** 의 silent-drop 발견 — 다른 substrate axis (dropout, attention type, positional encoding, lr schedule, gradient clipping 등) 도 같은 layered config chain 의 silent-drop 위험 가능성 (audit 필요). H254.5 는 일반 패턴 *예측* 일 뿐 본 fire 에서 측정 안 함. 후속 cycle 에서 cross-substrate audit 별도.
- **L4 (PR #342 runtime verify 부재)**: PR #342 가 wiring fix 만 적용 (`from_qwen` 수정), runtime end-to-end verify (dispatcher 명시 X → model 실측 X 매칭) 안 함. 즉 fix 가 *컴파일 시점* 에는 옳지만 *런타임* 에 실제 cfg 가 어떤 값으로 전달되는지 별도 측정 부재. H254.2 가 그 runtime verify 의 첫 fire.
- **L5 (substrate 실험 layered chain 의 본질적 fragility)**: CLI → dispatcher env → script argparse → cfg dict → model factory call 의 5 단계 전달은 각 경계에서 dict key typo, default override, `max(...)` clamp, kwargs swallow 등 silent-drop 위험에 노출. 본 가설의 method (byte-equal probe + factory 로그 grep) 는 *사후 검출* 한정 — *사전 방지* (compile-time type check, runtime cfg assert, automated end-to-end golden test) 는 별도 infra lane.
- **L6 (byte-equal 의 측정 정밀도 한계)**: byte-equal 비교는 IEEE-754 exact — 만약 substrate forward-pass 에 비결정 요소 (atomic add 순서, kernel non-determinism) 가 있으면 동일 wiring 도 byte-equal 깨질 수 있음. R8 GPU lane 이 deterministic 보장이 약하면 본 자연실험의 베이스라인 자체가 흔들림 (L1 honest 와 연동).
- **L7 (R8c cell-1 자연실험 양식 carry, 본 사건 직접 적용 안 함)**: H_249 의 R8c cell-1 byte-equal natural experiment 양식 (head_g seed 분리) 을 본 H 가 n_kv_head wiring 분리에 carry — 그러나 H_249 와 달리 본 H 는 *사후 발견된 bug 자연실험* (pre-registered randomization 아님). 인과 분리 강도는 R8a/R8a' 두 fire 의 다른 모든 axis (data order, seed, hardware) 동일성 audit 에 의존 (audit PR 후속).
- **L8 (silent-drop 일반화의 confounding)**: 만약 R8a 와 R8a' 가 wiring=4 vs wiring=2 외에 다른 axis 도 변경 (예: 다른 random seed, 다른 micro-batch size) 됐다면 byte-equal 결과는 silent-drop 가설과 무관한 다른 인과로도 설명 가능. 본 falsifier 의 valid 적용은 R8a' 가 **wiring 만 다르고 모든 다른 axis 동일** 한 controlled-pair 임을 dispatcher 양쪽 명시 비교로 확인해야 함 (PR #342 vs 원 R8a dispatcher diff 검증).

## Cross-Links

- **sister H (substrate/life)**: H_247 (init_CE catastrophic floor — 본 H 가 측정한 그 floor 의 lever wiring 자체의 integrity), H_249 (cluster X/Y/Z byte-equal signature — 자연실험 method 의 직접 carry, R8c cell-1 head_g seed 분리 양식을 n_kv_head wiring 분리에 적용), H_132 (frozen-cells — byte-equal = 동결된 동일 분기점), H_157 (Law 76 — byte-equal identity = σ-identity 같은 closed-form 동등성 패턴), H_248 (substrate autonomy 비반사성 — substrate-native framing 양식 carry).
- **substrate**: V3 fresh transformer factory `from_qwen()` 의 `max(qwen_native_n_kv_head, 4)` silent override → `cfg.n_kv_head` 직접 사용 (PR #342 fix). Qwen-1.5B native n_kv_head=2, v3 fresh substrate 의 의도된 wiring 도 2 였으나 max clamp 으로 4 적용된 사건.
- **raw**: raw#12 (deterministic byte-비교) + raw#9/10 (honest 흡수 vs 자력비교 + audit 전제 의존) + a_blue_closed (byte-equal = exact identity) + a_fire_recover_complete (R8a init_CE 회수 실패가 L1 의 직접 원인).
- **source PR**: [#342] anima wiring fix (from_qwen `max(..., 4)` → `cfg.n_kv_head` 직접 사용) · [#214] R8 spec (6-axis init_CE 측정 설계, n_kv_head=2 lever 의도 명시) · [#257] R8a fire spec (--n-kv-head 2 dispatcher 명시) · [#339] R8c probe driver (향후 R8a' 재dispatch lane infra) · R8a/R8a_v2 fire records `state/p21h_v3_R8a/` (LOST) + `state/p21h_v3_R8a_v2/` (재dispatch 후속).
- **literature**: silent failure modes in ML config systems (Sculley et al. 2015 "Hidden Technical Debt in ML Systems") · natural experiment causal inference (Angrist/Pischke — instrument variation) · IEEE-754 bit-exactness (사용자 manual annotation).
- **own**: (anima substrate 실험의 measurement-integrity 자기-관측 — operator 의도 vs 모델 실측 wiring 의 silent gap 자기-인지 lane).

## Verdict

```
verdict_class: pre-register-frozen (R8a fire 자연실험 흡수 · byte-equal 자력 비교 framework, 2026-05-24)
evidence_summary: dispatcher --n-kv-head 2 명시 → train_p21h_v3.py:627 argparse 수용 → from_qwen() silent
                  override 로 v3_n_kv_head=4 적용. 3-layer silent drop. log substring 만이 사후 단일 증거.
                  R8a (wired=4 실측) vs R8a' (PR #342 fix 후 wired=2 실측) init_CE step=1 byte-equal
                  비교가 자연 falsifier — byte-equal → lever inert, byte-differ → wiring fix 실제 effect.
F-WIRE-1 LOG-MARK-BUGGED  : R8a fire log `v3_n_kv_head=4` 출력      → PASS (흡수, fire spec/log)
F-WIRE-2 LOG-MARK-FIXED   : R8a' from_qwen `v3_n_kv_head=2` 출력    → TBD (R8a' 재dispatch 후 자력)
F-WIRE-3 BYTE-EQUAL-INERT : R8a vs R8a' init_CE step=1 byte-equal   → TBD (R8a init_CE 회수 의존, L1)
F-WIRE-4 BYTE-DIFFER-LIVE : R8a vs R8a' init_CE step=1 byte-differ  → TBD (R8a init_CE 회수 의존, L1)
F-WIRE-5 GENERALIZATION   : 다른 substrate axis silent-drop audit   → TBD (별도 cross-substrate cycle)
criteria_met: 1/5 PASS (C1 흡수) + 4/5 PENDING (C2/C3/C4/C5 R8a' 재dispatch + R8a 회수 의존)
cost: $0 mac local 비교 + ~$20-40 R8a' 재dispatch (a_fire_autonomous, 별도 cycle)
```

**State output**: (흡수 + byte-비교 framework cycle — 자력 fire 시 `HEXAD/LIFE/state/h254_n_kv_head_wiring_silent_misconfig_2026_05_24/{run_log_grep.hexa, run_byte_equal.hexa, result.json}` 으로 R8a' 결과 도착 후 산출)

**Honest scope (verdict)**: R8a fire init_CE LOST (a_fire_recover_complete 위반 사례, L1) → R8a vs R8a' 직접 byte-equal 비교는 R8a init_CE 회수 또는 R8a 재dispatch 의존. PR #342 wiring fix runtime verify 부재 (L4) — H254.2 가 그 runtime verify 의 첫 fire. silent-drop 일반화 (H254.5) 는 본 fire scope 밖, cross-substrate audit 별도 cycle. R8a/R8a' controlled-pair 가정 (wiring 외 모든 axis 동일) 은 dispatcher diff 검증 의존 (L8). byte-equal 자체는 IEEE-754 exact 이나 R8 GPU lane deterministic 보장 약하면 baseline 흔들림 (L6).
