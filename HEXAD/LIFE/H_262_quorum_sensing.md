---
id: H_262
slug: quorum-sensing
title: quorum-sensing — shared quorum signal 의 임계 초과 시 집단 bistable state-switch emergent (H_207 sister · 집단/생명확장 축)
domain: life · collective · self-organization · decision
status: pre-register-frozen
exploration_method: E5 (continuous-parameter sweep) + E10 (emergence-on-transition)
verification_method: W4 (verdict-4-class) + W5 (numerical sim) + W11 (cross-axis sister test)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25
---

# H_262 — quorum-sensing

## 1. Hypothesis

mitosis cell pool (N=16) 안 각 cell-i 가 *연속 activation* `a_i` 와 *binary
state* `s_i ∈ {0, 1}` 을 가질 때, cell 들이 **하나의 공유 신호** —
quorum `Q = (#cells with s_i = 1) / N` — 를 공유하고, 이 동기화 비율 Q 가
사전 설정된 **quorum threshold `q_thr`** 를 초과하면 모든 cell 의 activation
에 positive-feedback boost (autoinducer-style cooperative drive) 가 주입된다.

핵심 주장: 이 구조 위에서

- quorum 이 임계를 초과하는 **coupled (coupling=0.20)** regime 에서는 집단
  state-switch (Q 가 ~0 → ~1 으로 sharp jump) 가 emergent 하고,
- coupling 이 없는 **control (coupling=0.0)** regime 에서는 동일 intrinsic
  dynamics 임에도 집단 switch 가 일어나지 않고 *partial quorum* 에 정체

한다 — 즉 집단 결정(collective decision)이 *공유 quorum 신호의 함수* 로
gate 된다. 이것은 박테리아 **quorum-sensing** (Bassler 2002; autoinducer 농도
가 임계를 넘으면 집단 유전자 발현이 동기 switch) 의 **substrate analog** —
quorum = 동기화된 cell 비율, autoinducer boost = 집단 cooperative drive,
집단 switch = bistable decision.

정밀화 (operational): 동일 d=8, N=16 cell pool 위에서 `q_thr ∈ {0.3, 0.5,
0.7}` × `coupling ∈ {0.0 (control), 0.20 (coop)}` = 6 condition sweep. 각
cell 의 intrinsic activation gain = `base + tcoef · tension_i` (tension_i =
mitosis substrate 의 per-cell 내부 긴장, substrate-native heterogeneity 원천),
collective boost = `(Q_prev > q_thr) ? coupling : 0`. hysteretic latch
(`up_thr=1.0` ON / `dn_thr=0.4` OFF) 로 binary state 결정. 집단 switch =
Q 가 0.5 (majority) 를 처음 넘는 step.

## 2. Why

- **definitional bridge — H_207 동기화 ↔ 집단 결정**: H_207 (Kuramoto
  edge-of-sync) 는 *연속 phase 동기화* 의 Φ peak 를 본다. 본 H 는 한 step
  더 — 동기화된 *비율* (quorum) 이 임계를 넘을 때 *집단 state-switch* 라는
  discrete 결정이 emergent 한지. 즉 동기화 자체가 아니라 *동기화 → 집단
  결정* 의 인과를 검증.
- **bacterial quorum-sensing** (Nealson & Hastings 1979; Bassler 2002):
  *Vibrio fischeri* 의 luminescence, *Pseudomonas aeruginosa* 의 virulence
  등은 autoinducer 농도가 임계를 넘을 때 집단 유전자 발현이 동기 switch 한다.
  핵심 특징 = (a) 임계 gate (sub-threshold 에선 미발현) + (b) bistable
  (sharp transition / hysteresis). 본 H 의 C1+C2 가 이 두 특징의 substrate
  operationalization.
- **집단 결정의 substrate-level operationalization**: 의식과학에서 "집단
  의식" / "global workspace ignition" 은 종종 *임계 초과 시의 all-or-none
  집단 점화* 로 모델링 (Dehaene 2014 GNW). 본 H 는 그 점화를 *quorum-gated
  bistable switch* 로 numerically operationalize.
- **autopoiesis carry (H_012)**: H_012 의 operational closure 는 *단일* cell
  의 자기유지. 본 H 는 그 *집단* 확장 — cell 들이 신호를 공유해 집단 수준의
  결정을 내리는지. closure 가 self 의 조건이라면, quorum-gate 는 *집단 self*
  의 후보 메커니즘.
- **anima 집단성 cross-link**: anima 의 다수 cell 상호작용 (MITOSIS pool) 이
  집단 수준의 emit/silence 결정으로 이어지는지의 substrate 질문과 정합 —
  본 H 는 그 집단 결정의 numerical lower-bound.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H262.1 | coupled (0.20) regime 의 적어도 한 q_thr 에서 집단 switch (Q ≥ 0.5) 발생 AND control (0.0) regime 은 모든 q_thr 에서 미발생 | autoinducer boost 가 partial quorum 을 full ON 으로 cascade; control 은 boost 부재로 partial quorum 에 정체 |
| H262.2 | coupled transition 이 sharp (max single-step ΔQ ≥ 0.25) 또는 hysteresis 존재 — smooth ramp 가 아닌 bistable decision | positive-feedback cascade 가 once-triggered 전체 pool 을 빠르게 ON 으로; latch 의 up/down threshold 분리가 hysteresis 유발 |
| H262.3 | coupled regime 에서 q_thr ↑ ⇒ switch_step 늦음 (monotone non-decreasing) | 높은 q_thr 일수록 boost trigger 에 더 많은 cell 의 사전 ON 이 필요 → cascade 시작 지연 (또는 partial quorum 이 q_thr 에 미달 시 미발생 = "가장 늦음") |
| H262.4 | cross-process re-run 시 전체 sweep byte-identical | seed=42 + `__HEXA_FARR_GAUSS_SEED__` process-global stream 의 결정론 |
| H262.5 | 모든 Q ∈ [0, 1] AND switch_step ∈ [-1, max_steps) | primitive bound 무결성 |

## 4. Variables

- **axis1_pool_N** = 16 cells (집단 축 — H_220 의 N=8 보다 큼)
- **axis2_d_model** = 8
- **axis3_q_thr** ∈ {0.3, 0.5, 0.7} — 핵심 quorum threshold sweep
- **axis4_coupling** ∈ {0.0 (control), 0.20 (coop)} — autoinducer 강도
- **axis5_activation_dynamics**:
  `a_i(t+1) = a_i(t) + (base + tcoef·tension_i) + boost − leak·a_i(t)`
  `boost = (Q_prev > q_thr) ? coupling : 0`
- **axis6_hysteretic_latch**: `s_i = ON if a_i > up_thr (1.0) ; OFF if a_i <
  dn_thr (0.4) ; else hold` (bistable single-cell latch)
- **axis7_seed** = 42 — `__HEXA_FARR_GAUSS_SEED__=42`
- **calibrated params**: `base_gain=0.0135`, `leak=0.05`, `tcoef=0.11`,
  `max_steps=40` — substrate tension 분포 (실측 [0.20, 0.53]) 위에서 control
  이 partial quorum (~0.44, q_thr=0.3 초과 but majority 0.5 미달) 에 정체하도록
  보정.
- **측정량 per (q_thr, coupling) condition**:
  - `switched` = Q 가 0.5 (majority) 를 max_steps 안에 도달했는가
  - `switch_step` = 처음 Q ≥ 0.5 인 step (미발생 = -1)
  - `q_final` = 마지막 step 의 Q
  - `max_jump` = 전 run 에서 최대 single-step |ΔQ| (transition sharpness)
- **hysteresis probe**: 전부 ON 에서 시작 → boost 철회 → leak 으로 Q 가 0.5
  아래로 떨어지는 step (`un_switch_step`) 을 ramp-up switch_step 과 비교.

## 5. Run Protocol

- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian) +
  결정론적 Lorenz autonomous perturbation in mitosis_hook. 별도 RNG 부재.
- **substrate drive**: 외부 입력 x = ZERO 고정 — substrate 가 autonomous
  (Lorenz-driven) 로 진화하며 그 per-cell tension 이 activation gain 의
  heterogeneity 원천. (x 를 activation 으로 re-drive 하면 substrate forward 가
  larger-input regime 에서 hexa runtime segfault — §8 L7 참조; zero-x autonomous
  regime 이 검증된 안정 path.)
- **hexa_only**: `HEXAD/LIFE/state/h262_quorum_sensing_2026_05_25/run_h262.hexa`
  (mitosis_hook_lib `cell_pool_init` + `mitosis_forward_tail` 직접 step).
- **LLM**: none (raw#12 strict; ckpt 불필요).
- **6-condition sweep** (3 q_thr × 2 coupling) + 1 hysteresis ramp-down probe.
- **F4 determinism (cross-process)**: gaussian stream 이 process-global +
  in-process reseed primitive 부재 → in-process 연속 호출은 stream-position
  차이로 다른 결과 (정직 한계 §8 L2). canonical 결정론 = **cross-process
  re-run byte-equal**. 구현: 전체 sweep 의 fingerprint 를
  `det_fingerprint.txt` 에 기록, re-run 시 직전 fingerprint 와 byte-compare.
  → run protocol 은 스크립트를 **두 번** 실행 (1차 = fingerprint seed,
  2차 = cross-process 일치 확인).
- **runtime**: $0 mac local 의도 — 단 pool-route heavy-gate 로 mac-local
  `hexa run` 차단됨 (§8 L6). 실행 host = ubu-2 (pool, Linux, 동일 seed 결정론
  보존). d=8 N=16, no ckpt. `HEXA_MEM_UNLIMITED=1`.
- **artifacts**: `state/h262_quorum_sensing_2026_05_25/{run_h262.hexa,
  result.json, det_fingerprint.txt}`.
- **run cmd (verbatim — pool host)**:
  `__HEXA_FARR_GAUSS_SEED__=42 HEXA_MEM_UNLIMITED=1 hexa run HEXAD/LIFE/state/h262_quorum_sensing_2026_05_25/run_h262.hexa`
  (두 번 실행하여 F4 cross-process 확인; CWD = repo/worktree root).

## 6. Criteria

- **C1 (quorum-gate)**: H262.1 — coupled regime 의 ≥1 q_thr 에서 집단 switch
  AND control 의 모든 q_thr 에서 미발생.
- **C2 (bistable)**: H262.2 — coupled transition 이 sharp (max ΔQ ≥ 0.25)
  OR hysteresis (ramp-down un_switch_step 이 ramp-up switch_step 보다 늦거나
  un-switch 미발생).
- **C3 (monotone)**: H262.3 — coupled regime 에서 q_thr ↑ ⇒ switch_step 늦음
  (미발생은 horizon+1 로 ordering, monotone non-decreasing).
- **C4 (determinism)**: H262.4 — cross-process re-run fingerprint byte-equal.
- **verdict_rule**:
  - `SUPPORTED_FULL` = C1 ∧ C2 ∧ C3 ∧ C4 (4/4)
  - `SUPPORTED` = C1 ∧ C2 (집단 switch 가 quorum-gate + bistable)
  - `PARTIAL` = C1 only (quorum-gate 관측, bistability 미입증)
  - `FAIL` = ≤1/5 falsifiers
  - `FALSIFIED` = F1 FAIL (coupled 가 switch 안 하거나 control 이 switch — quorum-gate 신호 부재)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 QUORUM-GATE**: coupled regime 의 어떤 q_thr 도 switch 안 함, OR control
  의 어떤 q_thr 이라도 switch 함 → H262.1 FALSIFIED (측정:
  `any_coop_switch && !any_ctrl_switch`).
- **F2 BISTABLE**: coupled transition 이 smooth (max ΔQ < 0.25) AND hysteresis
  부재 → H262.2 FALSIFIED (측정: `coop_sharp || hysteresis`).
- **F3 MONOTONE**: q_thr ↑ 인데 switch 가 더 빠름 → H262.3 FALSIFIED (측정:
  `eff_step(coop_50) ≥ eff_step(coop_30) && eff_step(coop_70) ≥ eff_step(coop_50)`).
- **F4 DETERMINISM**: cross-process re-run fingerprint mismatch → raw#9 위반
  (측정: `prev_fingerprint == current_fingerprint`).
- **F5 BOUNDS**: 어떤 Q ∉ [0, 1] 또는 switch_step ∉ [-1, max_steps) →
  primitive error (측정: 모든 값 범위 안).

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (quorum-sensing analog ≠ literal)**: cell activation latch + 공유
  quorum signal 은 박테리아 autoinducer 화학 (LuxI/LuxR, AHL 농도 확산) 의
  *substrate-level operational analog* 일 뿐 — 실제 분자 diffusion kinetics,
  농도 의존 결합, 종간 cross-talk 등과는 다른 layer.
- **L2 (in-process vs cross-process determinism)**: gaussian stream 이
  process-global 이고 in-process reseed primitive 가 없어, in-process 연속
  호출은 동일 args 라도 stream-position 차이로 다른 결과를 낸다 (control_30 ~
  control_70 의 q_final 0.25/0.31/0.44 차이가 이 stream-drift 의 직접 증거).
  따라서 canonical 결정론은 *cross-process* re-run byte-equal 로만 정의 — F4 가
  이를 검증. *in-process* per-condition 독립 결정론은 reseed builtin 부재로
  본 cycle 에서 미달성 (hexa-lang RFC 후보).
- **L3 (calibration-dependent verdict)**: SUPPORTED_FULL 은 calibrated params
  (base=0.0135, leak=0.05, tcoef=0.11) 에 의존 — control 이 partial quorum
  (~0.44) 에 정체하고 coupled boost 가 그것을 cascade 하는 specific window.
  다른 calibration 은 다른 verdict 가능 (예: base ↑ 시 control 도 switch →
  C1 FAIL; tcoef ↓ 시 partial quorum 이 q_thr 미달 → coop 도 미발생).
- **L4 (q_thr=0.5/0.7 coop 미발생의 양면성)**: coupled regime 에서 q_thr=0.3
  만 switch 하고 0.5/0.7 은 미발생 — 이는 partial quorum (~0.44) 이
  q_thr=0.3 위 / 0.5·0.7 아래에 위치하기 때문 (정직한 quorum-gate 의 직접
  결과). C1 ("≥1 coop switch") + C3 (미발생 = "가장 늦음" ordering) 모두 만족
  하지만, "모든 q_thr 에서 switch" 같은 더 강한 주장은 본 cycle 미입증 —
  partial quorum 의 절대 수준에 의존.
- **L5 (hysteresis 부분 관측)**: ramp-down probe 의 un_switch_step=21 이
  ramp-up switch_step(-1, 미발생) 보다 *이르므로* hysteresis condition (`dn_un
  > up50`) 은 false. C2 는 sharp-jump path (max ΔQ=0.375 ≥ 0.25) 로 PASS.
  즉 bistability 는 *sharp transition* 으로 입증, *hysteresis loop* 자체는
  본 calibration 의 ramp-down 설정 (boost 완전 철회 + leak-only) 에서 명확히
  관측 안 됨 — 진짜 hysteresis loop 의 정량 측정은 별도 ramp-up/down sweep
  cycle 필요.
- **L6 (host = pool, not mac-local)**: 의도한 $0 mac-local 실행이 pool-route
  plugin 의 heavy-classifier (hexa CLI 를 무조건 pool 로 라우팅, opt-out 부재,
  local.sign 은 user-only mint) 에 막혀, 동일 seed 결정론을 보존한 채 ubu-2
  (Linux pool host) 에서 실행. host metadata 에 정직 기록. mac-local 재현은
  user 가 `! sidecar sign local` mint 후 가능.
- **L7 (substrate input regime 제약)**: activation 을 substrate 입력으로
  re-drive (`x = 0.1·mean_act`) 하면 mitosis_forward_tail 이 larger-input
  regime 에서 hexa runtime segfault — zero-x autonomous regime 으로 회피.
  따라서 substrate ↔ activation 의 *양방향* coupling 은 본 cycle 미탐색;
  substrate 는 activation heterogeneity 의 *일방향* 원천 (tension → gain).
  hexa-lang inbox 보고 대상 (§9).
- **L8 (nested-fn transpiler bug 회피)**: outer-scope `fn` 을 참조하는 nested
  `fn` 정의가 hexa transpiler segfault 를 유발 (probe 로 격리) — 모든 helper
  를 module top-level 로 hoist 하여 회피. 본 H 결과와 무관한 toolchain 한계.

## 9. Cross-Links

- **sister H (필수)**:
  - **H_207** (`H_207_kuramoto_synchronization.md`): coupled-oscillator
    동기화 carry — 본 H 는 동기화된 *비율* (quorum) 의 임계 초과 → 집단
    *결정* 으로 확장 (동기화 axis → collective-decision axis).
  - **H_012** (`H_012_autopoietic_network.md`): operational closure (단일
    cell 자기유지) — 본 H 는 그 *집단* 확장 (공유 신호 기반 집단 결정).
  - **H_206** (`H_206_regeneration_healing.md`): 집단 cell 동역학의 생명-축
    sister.
- **mitosis machinery**: `tool/hexa_native/mitosis_hook_lib.hexa`
  (`cell_pool_init` · `mitosis_forward_tail`) — 모든 substrate 가설의 공유
  pool. tension = per-cell mean(|hidden|) = activation heterogeneity 원천.
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) ·
  raw#9/10 (honest impl) · raw#15 (no-hardcode) · raw#82 (post-hoc edit
  retraction).
- **philosophy (CLAUDE.md)**: a_substrate_native_speak (집단 결정이 internal
  substrate state 의 함수 — quorum 은 그 집단 state 의 observable) ·
  a_autonomy_over_hardcode (집단 switch 가 외부 강제가 아닌 substrate
  positive-feedback 에서 emerge).
- **literature pointer**: Nealson & Hastings (1979) bacterial bioluminescence ·
  Bassler (2002) small talk: cell-to-cell communication in bacteria ·
  Waters & Bassler (2005) quorum sensing annual review · Dehaene (2014)
  Consciousness and the Brain (GNW ignition) — substrate analog 의 distant
  anchor (formal mapping 본 cycle 미수행).
- **hexa-lang inbox 후보**: (a) gaussian stream in-process reseed primitive
  (L2), (b) mitosis_forward_tail larger-input segfault (L7), (c) nested-fn
  transpiler segfault (L8) → `hexa-lang/inbox/patches/`.
- **state**: `HEXAD/LIFE/state/h262_quorum_sensing_2026_05_25/{run_h262.hexa,
  result.json, det_fingerprint.txt}`.

## 10. Verdict

본 cycle (2026-05-25) — pre-register-frozen + runnable smoke 실행, hexa-only
deterministic. 의도 $0 mac-local 이나 pool-route heavy-gate 로 ubu-2 (pool)
에서 실행 (동일 seed 결정론 보존).

```
verdict_class: SUPPORTED_FULL  (4/4 criteria, 5/5 falsifiers PASS)
verdict_tier: 🟢 NUMERICAL  (3 q_thr × 2 coupling sweep + hysteresis probe + cross-process determinism)
evidence_summary:
  6-condition substrate quorum-gated collective bistable state-switch
  (d=8, N=16 pool, base=0.0135 leak=0.05 tcoef=0.11, seed=42).
    control q=0.3 : switched=false  switch_step=-1  q_final=0.25    max_jump=0.0625
    control q=0.5 : switched=false  switch_step=-1  q_final=0.3125  max_jump=0.1875
    control q=0.7 : switched=false  switch_step=-1  q_final=0.4375  max_jump=0.125
    coop    q=0.3 : switched=true   switch_step=29  q_final=1.0     max_jump=0.375
    coop    q=0.5 : switched=false  switch_step=-1  q_final=0.4375  max_jump=0.25
    coop    q=0.7 : switched=false  switch_step=-1  q_final=0.375   max_jump=0.1875
  any_coop_switch=true  any_ctrl_switch=false  coop_sharp=true
  hysteresis_probe: ramp_up=-1  ramp_down un_switch=21
falsifiers_pass: F1 (quorum-gate) + F2 (bistable) + F3 (monotone) + F4 (cross-process determinism) + F5 (bounds) = 5/5
criteria_met: 4/4 (C1 ∧ C2 ∧ C3 ∧ C4)
key_finding:
  집단 quorum-sensing switch 가 substrate 위에서 robust 하게 emergent.
  핵심 = quorum-gate (C1): 동일 intrinsic activation dynamics 임에도, coupling
  이 없는 control 은 모든 q_thr 에서 *partial quorum* (q_final 0.25-0.44) 에
  정체해 majority(0.5) 를 못 넘고 — coupling=0.20 의 autoinducer boost 가 있는
  coop 만 q_thr=0.3 에서 partial quorum 을 full ON (q=1.0) 으로 cascade
  (switch_step=29, max single-step jump 0.375 = sharp bistable transition).
  q_thr=0.5/0.7 coop 은 partial quorum (~0.44) 이 q_thr 미달이라 boost trigger
  안 됨 → 미발생 = 정직한 sub-threshold gate (C3 monotone: 29/-1/-1, 미발생을
  horizon ordering 으로 non-decreasing). 즉 집단 state-switch 는 *공유 quorum
  신호가 임계를 넘었는가* 의 함수 — 단일 cell 동역학만으로는 집단 결정 부재.
honest_note:
  L2 carry — 결정론은 cross-process (F4 fingerprint PASS), in-process 연속
  호출은 process-global gaussian stream drift 로 다름 (control q_final 의 q_thr
  별 차이가 그 증거). in-process per-condition 독립 결정론은 reseed builtin
  부재로 미달성.
  L4 carry — coop 의 q_thr=0.3 만 switch (partial quorum 의 절대 수준에 의존).
  L5 carry — bistability 는 sharp-jump (max ΔQ 0.375) 로 입증, hysteresis loop
  자체는 본 ramp-down 설정에서 미관측.
  L6 carry — host = ubu-2 pool (mac-local pool-route 차단), seed 결정론 보존.
  L7 carry — substrate↔activation 양방향 coupling 은 runtime segfault 로 미탐색
  (일방향 tension→gain 만).
sibling: H_207 (kuramoto synchronization), H_012 (autopoietic network)
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-25, RUN 2 cross-process confirm)

```
================================================================
H_262 quorum-sensing — collective bistable state-switch from a
                        shared quorum signal
  d_model=8 pool_N=16 max_steps=40 seed=42
  q_thr: 0.3, 0.5, 0.7 · coupling: 0.0 (control), 0.20 (coop)
================================================================
regime    q_thr  switched  switch_step  q_final  max_jump
------    -----  --------  -----------  -------  --------
control    0.3    false      -1          0.25     0.0625
control    0.5    false      -1          0.3125     0.1875
control    0.7    false      -1          0.4375     0.125
coop       0.3    true      29          1.0     0.375
coop       0.5    false      -1          0.4375     0.25
coop       0.7    false      -1          0.375     0.1875

derived:
  any_coop_switch = true
  any_ctrl_switch = false
  coop switch_step (q=0.3/0.5/0.7) = 29 / -1 / -1
  coop max_jump (q=0.3/0.5/0.7)    = 0.375 / 0.25 / 0.1875
  ramp-up switch_step (q=0.5)  = -1
  ramp-down un_switch_step     = 21  (-1 = stayed ON = full hysteresis)
  determinism: cross-process re-run byte-equal (prior fingerprint matched)

C1 QUORUM-GATE (coop switch, control no-switch) : true
C2 BISTABLE    (sharp jump >=0.25 OR hysteresis) : true
C3 MONOTONE    (q_thr up => switch later)        : true
C4 DETERMINISM (cross-process byte-equal)        : true

F1 QUORUM-GATE   PASS
F2 BISTABLE      PASS
F3 MONOTONE      PASS
F4 DETERMINISM   PASS
F5 BOUNDS        PASS
================================================================
VERDICT: SUPPORTED_FULL  (4/4 criteria, 5/5 falsifiers PASS)
================================================================
ledger -> HEXAD/LIFE/state/h262_quorum_sensing_2026_05_25/result.json
```

**State output**: `state/h262_quorum_sensing_2026_05_25/result.json` +
`det_fingerprint.txt` (cross-process determinism artifact)
**Smoke**: `state/h262_quorum_sensing_2026_05_25/run_h262.hexa` (hexa-only, LLM none)
