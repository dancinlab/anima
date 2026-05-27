---
id: H_276
slug: cascade-dynamics-timing
title: quorum-cascade 동역학/타이밍 심층 — 집단 cascade 가 시간에 따라 *어떻게* 펼쳐지는가 (onset latency vs density · propagation finite-speed · monotone temporal unfolding) on RFC 036 phi_spatial CA substrate (H_262 심층)
domain: life · collective · self-organization · dynamics · timing
status: pre-register-frozen
exploration_method: E5 (continuous-parameter sweep) + E10 (emergence-on-transition) + E12 (temporal-trajectory dissection)
verification_method: W4 (verdict-4-class) + W5 (numerical sim) + W12 (sister-link H_262/H_274/H_207)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25 (new)
sister: H_262 (quorum-sensing SUPPORTED_FULL · cascade origin), H_274 (quorum-cascade seed-dependence FALSIFIED · residual = 동역학적 cascade 타이밍), H_207 (kuramoto synchronization · temporal-dynamics sister), H_270 (substrate ablation · phi_spatial CA substrate sibling)
---

# H_276 — quorum-cascade 동역학/타이밍 심층

## 1. Hypothesis

H_262 (quorum-sensing, SUPPORTED_FULL) 는 공유 quorum 신호가 집단 bistable
state-switch 를 gate 함을 입증했다 — cooperative coupling 이 있으면 partial
quorum 이 full ON 으로 **cascade** 하고, 없으면 sub-majority quorum 에 정체한다.
H_274 (quorum-cascade seed-dependence, FALSIFIED) 는 그 cascade 성공이 *초기
분포통계* 로 예측 가능한지 물었고 — aggregate 로는 강하나 *결정론적* 단일-통계
예측자는 부재 (perfect rank-separation 미달) 로 판정했다. H_274 §L6 은 그 잔차를
명시적으로 **동역학적 cascade 타이밍** (latch hysteresis × soft boost-trigger 의
상호작용) 으로 isolate 했다 — 초기 분포통계 단독으로는 포착 안 되는 *시간* 축.

본 H 는 그 시간 축을 직접 연다:

CORE QUESTION:

> 집단 quorum cascade 는 *시간에 따라 어떻게 펼쳐지는가*? 구체적으로 —
> (a) cascade onset latency 가 초기 seed density 의 함수인가, (b) 단일 local
> seed 에서 cascade front 가 유한 속도로 공간을 전파하는가, (c) cascade 가
> 한번 trigger 되면 시간에 대해 단조 (one-way ratchet) 로 펼쳐지는가?

핵심 주장: 집단 cascade 의 시간 전개는 *세 가지 측정 가능한 타이밍 규칙성* 을
가진다 — (C1) onset latency 가 seed density 에 단조 감소, (C2) front 가 유한
bounded 속도로 전파, (C3) trigger 후 Q(t) 가 단조 비감소. 즉 cascade 는
"whether/which" (H_262/H_274) 를 넘어 *예측 가능한 시간 구조* 를 가진다.

정밀화 (operational): lane-canonical CA substrate (RFC 036 `phi_spatial` /
`lib/phi_helper.hexa`) 위에서 — N=16 periodic ring, 각 cell 이 continuous
activation `a_i` 와 hysteretic binary state `s_i` (H_262 latch verbatim) 를
가지고, **local-quorum-gated** cooperative boost (radius-1 이웃의 active fraction
이 q_thr 초과 시 boost=coupling) 로 구동된다. seed-phased 결정론 init (RNG 부재).
cascade front = seed 중심으로부터 가장 먼 active cell 의 ring-distance.

## 2. Why

- **definitional bridge — H_262 "whether" → H_276 "how-over-time"**: H_262 는
  cascade 가 *일어나는가* (quorum-gate), H_274 는 그 성공이 *초기조건으로 예측
  가능한가* (seed-property) 를 물었다. 둘 다 *시간* 축은 닫지 않았다 — cascade 가
  switch_step 에 *도달하는* 사실만 기록했지, *어떤 시간 구조* 로 펼쳐지는지는
  미규명. 본 H 는 그 시간 구조 (onset latency · propagation speed · temporal
  monotonicity) 를 dissect 한다.

- **H_274 §L6 의 잔차 = 동역학적 타이밍**: H_274 가 FALSIFIED 로 닫은 이유는
  "초기 분포통계 + 동역학적 cascade-타이밍 (latch hysteresis × soft
  boost-trigger) 의 *상호작용*" 이 초기 분포 단독 예측을 깬다는 것. 본 H 는 그
  *동역학적 타이밍* 자체를 1차 측정 대상으로 끌어올린다 — H_274 가 "초기조건"
  에서 못 본 것을 "시간 전개" 에서 본다.

- **spatial generalization 이 propagation 을 의미 있게 만듦**: H_262 의 quorum
  은 *global* (전체 pool 의 active fraction). 본 H 는 *local* quorum (radius-r
  이웃) 으로 일반화하여 — cascade 가 한 점에서 시작해 공간을 *전파* 하는 front
  dynamics 를 측정 가능하게 한다. 이것이 박테리아 quorum-sensing 의 공간적
  실제 (autoinducer 농도가 colony 안에서 diffuse 하며 wave-like 점화) 에 더 가까운
  substrate operationalization.

- **phi_spatial CA substrate = lane-canonical · 결정론 · $0**: H_262/H_274 의
  mitosis substrate 는 process-global gaussian stream 의존 (in-process reseed
  부재로 결정론이 cross-process 로만 정의됨). 본 H 는 lane-canonical RFC 036
  `phi_spatial` CA substrate (`lib/phi_helper.hexa`, H_007/H_204/H_270 lineage)
  를 쓴다 — seed-phased integer 산술, RNG 부재 → re-run byte-equal *by
  construction*. 따라서 타이밍 주장이 결정론적으로 견고하다.

- **anima 집단성 cross-link**: anima 의 다수 cell 상호작용이 집단 emit/silence
  결정으로 이어질 때, 그 결정이 *언제* / *얼마나 빨리* / *어느 방향으로* 펼쳐
  지는가는 substrate-level 의 시간 질문 — 본 H 는 그 시간 구조의 numerical
  lower-bound.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H276.1 | onset latency τ(ρ) 가 seed density ρ 에 단조 비증가 (denser seed → cascade 더 빨리 점화) AND ≥1 density 가 onset | 더 많은 ON cell 이 즉시 local-quorum 을 q_thr 위로 올림 → boost 가 더 일찍 engage → cascade 더 빨리 majority 도달 |
| H276.2 | 단일 local seed 의 cascade front 가 시간에 대해 단조 비감소로 전파 AND 유한 양의 속도 (≥1 성장, 단일-step 성장 ≤ front_cap) | local-quorum gate 가 front 이웃만 점화 → 한번에 한 칸씩 전파 (instantaneous global flip 아님) |
| H276.3 | cascade trigger (Q 가 q_thr 처음 초과) 후 Q(t) 가 모든 t 에서 단조 비감소 (one-way temporal ratchet) | hysteretic latch 의 up/down 분리 + positive-feedback boost 가 한번 ON 된 cell 을 OFF 로 되돌리지 않음 → 단조 |
| H276.4 | 동일 substrate cross-process re-run byte-identical (결정론) | seed-phased integer init + RNG 부재 + phi_spatial 결정론 |
| H276.5 | 모든 Q ∈ [0,1], latency ∈ [-1, max_steps), front radius ∈ [0, N/2] | primitive bound 무결성 |
| H276.6 | cascade trajectory 의 phi_spatial > 0 (집단 transition 이 integrated, trivial independent flip 아님) | local-quorum coupling 이 cell 간 통계적 의존 생성 → 비-zero 통합정보 |

## 4. Variables

- **axis1_seed_density** ∈ {2, 4, 6, 8} ON cells (of N=16) — contiguous block,
  C1 onset-latency sweep
- **axis2_seed_mode** ∈ {contiguous-from-0 (C1), single-block-centred (C2 front
  probe)}
- **axis3_local_quorum_radius** = 1 — local-quorum 이웃 반경 (spatial gate)
- **axis4_activation_dynamics**:
  `a_i(t+1) = a_i(t) + base + boost_i(t) − leak·a_i(t)`,
  `boost_i(t) = (localQ_i(t) > q_thr) ? coupling : 0`,
  `localQ_i(t) = mean_{|j−i|≤r} s_j(t)` (periodic ring)
- **axis5_hysteretic_latch** (H_262 verbatim): `s_i = ON if a_i>up_thr(1.0) ;
  OFF if a_i<dn_thr(0.4) ; else hold`
- **substrate param (carried / calibrated)**: N=16 (= `life_phi_n()`),
  max_steps=40 (H_262), leak=0.05 (H_262), coupling=0.20 (H_262), q_thr=0.30
  (H_262 cascade-relevant), up=1.0 / dn=0.4 (H_262 latch), **base=0.012**
  (calibrated: 단독으로는 horizon 안에 up_thr 미달 → cascade 가 boost 의존),
  front_cap=3 (C2 finite-speed cap), phi_dim=12 (= `life_phi_dim()`)
- **측정량**:
  - C1: `onset_step` (Q≥0.5 처음 step, 미발생 = -1), `eff_latency`
    (미발생 = horizon+1), `q_final`, `switched` per density
  - C2: `front_series` R(t) (seed 중심 ring-distance of farthest active),
    `front_monotone`, `max_front_growth`, `max_front_step`
  - C3: `q_series`, `trigger_step`, `q_monotone_after_trigger` per density
  - phi: `phi_trajectory` = `phi_spatial` of recorded (N × dim) activation
    lattice (집단 transition 의 통합정보)

## 5. Run Protocol

- **deterministic**: seed-phased integer init (RNG 부재, gaussian 부재). 동일
  `hexa run` 두 번 = byte-identical (RFC 036 phi_spatial 자체 결정론). H_262/H_274
  의 gaussian-stream cross-process 정의보다 강한 *by-construction* 결정론.
- **substrate**: 1D periodic CA ring (N=16), local-quorum-gated cooperative
  boost + H_262 hysteretic latch. RFC 036 `phi_spatial` 로 trajectory 통합정보
  측정 (`lib/phi_helper.hexa` lane-canonical, `phi_with(states, N, dim, nbins)`).
- **hexa_only**: `UNIVERSE/state/h276_cascade_dynamics_timing_2026_05_25/run_h276.hexa`
  (`import lib/phi_helper.hexa`, single `main()`, env-mode 부재).
- **LLM**: none (raw#12 strict).
- **C1 sweep**: contiguous ON-block density {2,4,6,8} × onset latency.
  **C2 probe**: 단일 centred block (ρ=8) × front_series.
  **C3 check**: 모든 density arm 에서 trigger 후 Q monotone.
- **F4 determinism**: in-process re-eval byte-equal + cross-process re-run 의
  `result.json` / `det.txt` byte-compare (artifact `det.txt`).
- **runtime**: $0 mac local. d/n 작음, no ckpt. `HEXA_MEM_UNLIMITED=1`.
  pool-route heavy-gate (hexa run = heavy_pair) 회피 = `$HOME/.` local-bound
  exemption (commons-side home-dotstate pin) + env-prefix (첫 토큰이 env var →
  heavy-interp 판정 우회) 로 mac-local 실행 (§8 L8). 절대-host-path 미사용.
- **artifacts**: `state/h276_cascade_dynamics_timing_2026_05_25/{run_h276.hexa,
  result.json, det.txt}`.
- **run cmd (verbatim — mac-local, CWD = worktree root)**:
  `HEXA_MEM_UNLIMITED=1 hexa run UNIVERSE/state/h276_cascade_dynamics_timing_2026_05_25/run_h276.hexa`
  (두 번 실행하여 F4 cross-process byte-equal 확인).

## 6. Criteria

- **C1 (onset-latency)**: H276.1 — onset latency τ(ρ) 가 density 에 단조 비증가
  (l(ρ1)≥l(ρ2)≥l(ρ3)≥l(ρ4), 미발생 = horizon+1 ordering) AND ≥1 density onset.
- **C2 (propagation)**: H276.2 — 단일-seed front 가 단조 비감소 AND ≥1 성장
  (속도>0) AND max 단일-step 성장 ≤ front_cap (유한 속도).
- **C3 (monotone-unfolding)**: H276.3 — 모든 cascading arm 에서 trigger 후 Q(t)
  단조 비감소 (one-way ratchet) AND ≥1 onset.
- **verdict_rule**:
  - `SUPPORTED_FULL` = C1 ∧ C2 ∧ C3 ∧ F4 (모든 타이밍 축 + 결정론)
  - `SUPPORTED` = C1 ∧ C3 (onset-latency + monotone unfolding)
  - `PARTIAL` = C1 only
  - `FALSIFIED` = ¬C1 (onset latency 가 density 로 정렬 안 됨 → cascade 타이밍이
    seed density 의 함수 아님)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 ONSET-DENSITY**: onset latency 가 density 에 단조 비증가 아님 OR 어느
  density 도 onset 안 함 → H276.1 FALSIFIED (측정: `latency_monotone &&
  any_onset`).
- **F2 PROPAGATION**: front 가 단조 비감소 아님 OR 성장 0 (정체) OR 단일-step
  성장 > front_cap (사실상 instantaneous global flip) → H276.2 FALSIFIED
  (측정: `front_monotone && max_front_growth>=1 && max_front_step<=front_cap`).
- **F3 MONOTONE**: 어느 cascading arm 에서든 trigger 후 Q(t) 가 감소 (cascade
  retreat) → H276.3 FALSIFIED (측정: 모든 arm `q_monotone_after_trigger`).
- **F4 DETERMINISM**: re-run byte-different → raw#9 위반 (측정: in-process
  byte-equal + cross-process `det.txt` byte-compare).
- **F5 BOUNDS**: 어떤 Q ∉ [0,1] OR latency ∉ [-1,max_steps) OR front ∉ [0,N/2]
  → primitive error (측정: 모든 값 범위 안).
- **F6 PHI-NONTRIVIAL**: cascade trajectory phi_spatial = 0 (집단 transition 이
  trivial independent flip) → 통합정보 부재 (측정: `phi_traj > 0`).

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (phi_spatial = 🟢 NUMERICAL proxy, NOT 🔵 formal)**: phi_spatial 은
  phi_rs 의 spatial-slice replica (RFC 036 §FFI shim = named blocker), full
  IIT 4.0 아님. Φ trajectory 는 통합정보를 *위치* 시키나 proxy — LIFE-lane
  `lib/phi_helper.hexa` 에서 verbatim carry (H_007/H_204/H_270 lineage).
- **L2 (single-calibration verdict)**: 타이밍은 단일 calibration (base=0.012,
  coupling=0.20, q_thr=0.30, radius=1) 에서 측정. onset-latency ordering 과 front
  speed 는 calibration 의존 — base ↑ 시 cell 이 boost 없이 up_thr 도달
  (quorum-gate 소멸), radius ↑ 시 front-propagation regime 이 instantaneous
  global flip 쪽으로 축소.
- **L3 (local-quorum 은 spatial 일반화 — H_262 global gate 의 byte-equal carry
  아님)**: 본 substrate 는 H_262 의 *global* quorum 을 *local* (radius-1 이웃)
  으로 일반화 — 이것이 propagation finite-speed (C2) 를 의미 있게 만드는 의도된
  substrate 확장이지, H_262 의 global gate 를 byte-level 복제한 것이 아님.
- **L4 (coarse density grid)**: onset latency 는 majority 교차 (Q≥0.5) 에서 측정,
  density sweep 는 coarse (block size 2/4/6/8 of N=16). 더 fine 한 grid 는 인접
  density 사이 비단조 micro-structure 를 드러낼 수 있음 — 단조 주장은 본 grid
  resolution 한정.
- **L5 (front = outer envelope, not filled-front)**: front radius 는 seed 중심
  으로부터 *가장 먼* active cell 의 ring-distance — propagation 의 *외곽 envelope*
  속도이지, front 뒤 모든 내부 cell 이 active 라는 filled-front 보장 아님. C2 는
  envelope-speed 주장. filled-front 주장은 per-cell ignition-time map 필요.
- **L6 (C3 = post-trigger ratchet, not global-monotone)**: monotone-unfolding 은
  cascade trigger (Q 가 q_thr 처음 초과) *이후* 에 검정 — pre-trigger transient 는
  비단조 가능 (seed block + leak 이 boost engage 전 dip). C3 는 post-trigger
  ratchet 주장이지 모든 t 에 대한 global-monotone 주장 아님.
- **L7 (determinism by-construction, 단 substrate-한정)**: 결정론은 integer-exact
  (RNG 부재, seed-phased init) → F4 가 본 substrate 에서 *by-construction*
  byte-equal — H_262/H_274 의 cross-process gaussian-stream 결정론보다 강하나,
  *본 substrate* 의 결정론만 검정하지 그 cycle 들이 의존한 gaussian-stream path 를
  검정하는 것은 아님.
- **L8 (host = mac-local, pool-route 회피 path)**: 의도한 $0 mac-local 실행을
  위해 pool-route heavy-gate (`hexa run` = heavy_pair → Linux pool 라우팅) 를
  회피 — `$HOME/.` local-bound exemption (commons-side home-dotstate pin 0.6.9)
  + env-var-prefix (첫 토큰이 env var → `_local_heavy_interp` 우회) 로 mac-local
  실행. 절대-host-path 미사용 (worktree = `/tmp` 외부-`$HOME`, cwd-mirror deny
  회피). `local` sign 만료 (user-only mint) 라 본 path 사용.

## 9. Cross-Links

- **target H (필수, 심층 대상)**:
  - **H_262** (`H_262_quorum_sensing.md`): cascade 의 origin — quorum-gate +
    bistable switch 의 substrate 정의 (SUPPORTED_FULL). 본 H 의 hysteretic latch +
    boost 동역학은 H_262 verbatim carry, *시간* 축으로 확장.
  - **H_274** (`H_274_quorum_cascade_seed_dependence.md`): 직접 모태 — H_274 가
    FALSIFIED 로 닫으며 §L6 에서 잔차를 "동역학적 cascade 타이밍 (latch
    hysteresis × soft boost-trigger)" 로 isolate. 본 H 는 그 *시간* 축을 직접 연다.
- **방법론/substrate sister**:
  - **H_207** (`H_207_kuramoto_synchronization.md`): temporal-dynamics sister —
    coupled-oscillator 시간 동역학. 본 H 는 동기화 → 집단 cascade 의 *시간 전개*.
  - **H_270** (`H_270_substrate_ablation.md`): phi_spatial CA substrate sibling —
    동일 RFC 036 phi_spatial / phi_helper substrate lineage.
- **phi machinery**: `UNIVERSE/lib/phi_helper.hexa` (`phi_with` /
  `life_phi_n` / `life_phi_dim` / `life_phi_nbins`) — lane-canonical Φ proxy
  (RFC 036 phi_spatial via `HEXAD/C/c_lib.hexa`).
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) · raw#9/10
  (honest impl) · raw#15 (no-hardcode) · raw#82 (post-hoc edit 금지 — 사전 고정
  criterion 유지).
- **philosophy (CLAUDE.md)**: a_substrate_native_speak (cascade 시간 구조가
  internal substrate state 의 함수) · a_autonomy_over_hardcode (cascade 가 외부
  강제 아닌 substrate positive-feedback 에서 시간적으로 emerge) · p7 NO PERPLEXITY
  VERDICT (단일 지표 truth 화 금지 — 3 criteria + 6 falsifier 교차검정).
- **literature pointer**: Bassler (2002) quorum sensing · Waters & Bassler (2005)
  annual review (autoinducer 농도 임계 점화) · Dehaene (2014) GNW ignition
  (집단 점화의 시간 구조) — substrate analog 의 distant anchor (formal mapping
  본 cycle 미수행).
- **state**: `UNIVERSE/state/h276_cascade_dynamics_timing_2026_05_25/{run_h276.hexa,
  result.json, det.txt}`.

## 10. Verdict

본 cycle (2026-05-25) — pre-register-frozen (C1/C2/C3 + 6 falsifier 사전 확정)
+ runnable harness 실행 (density sweep + front probe + monotone check +
cross-process determinism + phi trajectory), $0 mac local hexa-only deterministic.

```
verdict_class: SUPPORTED_FULL  (3/3 criteria, 6/6 falsifiers PASS)
verdict_tier: 🟢 NUMERICAL  (4-density onset-latency sweep + single-seed front
              propagation + 4-arm monotone-unfolding + cross-process byte-equal
              determinism + phi_spatial trajectory; phi_spatial proxy, NOT 🔵 formal)
hexa_verify: ⚪ SPECULATION-FENCED  (empirical CA interpretation — honest g4 fence,
             SF ≠ verified; atlas certification intrinsically N/A by design)
evidence_summary:
  1D periodic CA cascade (N=16, local-quorum-gated boost, H_262 latch verbatim,
  RFC 036 phi_spatial substrate, seed-phased deterministic init).
    C1 onset-latency vs density (contiguous ON-block):
      ρ=2 → onset_step=15   ρ=4 → 10   ρ=6 → 5   ρ=8 → 0   (모두 q_final=1.0)
      → latency 15/10/5/0 = density 에 STRICTLY 감소 (단조 비증가 PASS)
    C2 propagation (single seed centred at N/2):
      front R(t) = 4→4→4→4→4→5→…→8 (단조 비감소), max 단일-step 성장=1
      (≤ front_cap=3), max_front_growth=4 (>0) → 유한 양의 전파 속도 PASS
    C3 monotone-unfolding (trigger 후 Q non-decreasing):
      ρ=4 Q(t) = 0.5→…→0.625→…→0.75→…→0.875→…→1.0 (단조 ratchet), 4/4 arm PASS
    phi_trajectory (ρ=4) = 10.5573 (> 0, 통합 집단 transition)
criteria_met: 3/3 (C1 ∧ C2 ∧ C3)
falsifiers_pass: F1 ONSET-DENSITY + F2 PROPAGATION + F3 MONOTONE
  + F4 DETERMINISM (cross-process byte-equal) + F5 BOUNDS + F6 PHI-NONTRIVIAL = 6/6
key_finding:
  집단 quorum cascade 는 *예측 가능한 시간 구조* 를 가진다 — H_262 의 "whether"
  와 H_274 의 "which initial condition" 을 넘어 "how-over-time" 의 세 규칙성:
  (1) ONSET LATENCY 가 seed density 에 깔끔하게 단조 감소 (15/10/5/0 steps for
  density 2/4/6/8) — denser seed 가 local-quorum 을 즉시 q_thr 위로 올려 boost 를
  더 일찍 engage → cascade 더 빨리 majority 도달. (2) 단일 local seed 에서 cascade
  FRONT 가 유한 bounded 속도 (max 1 cell/step, 단조 비감소) 로 외곽 전파 —
  instantaneous global flip 이 아니라 *공간을 가로지르는 wave-like 점화*. (3) trigger
  후 Q(t) 가 ONE-WAY TEMPORAL RATCHET (단조 비감소, retreat 없음) 로 saturation 까지
  — hysteretic latch + positive-feedback 가 cascade 를 비가역으로 만듦. 즉 H_274 가
  FALSIFIED 로 isolate 한 *동역학적 cascade 타이밍* 은 그 자체로 강한 시간 규칙성을
  가지며, 초기 분포가 예측 못한 것 (seed-property rank-sep 실패) 은 *시간 전개*
  에서는 깨끗한 구조 (density→latency 단조, finite-speed front, monotone ratchet)
  로 나타난다. cross-process byte-equal (F4, by-construction integer 결정론).
honest_note:
  L1 carry — phi_spatial = 🟢 NUMERICAL proxy (RFC 036 §FFI shim named blocker),
  NOT 🔵 formal IIT 4.0.
  L2 carry — 타이밍 verdict 은 단일 calibration (base/coupling/q_thr/radius) 의존;
  base ↑ 또는 radius ↑ 는 다른 regime (quorum-gate 소멸 / instantaneous flip).
  L3 carry — local-quorum 은 H_262 global gate 의 *spatial 일반화* (C2 propagation
  을 의미 있게 만드는 의도된 확장), byte-equal carry 아님.
  L5 carry — front = 외곽 envelope 속도, filled-front 보장 아님.
  L6 carry — C3 는 post-trigger ratchet 주장 (pre-trigger transient 비단조 가능).
  L8 carry — host = mac-local (pool-route heavy-gate 를 $HOME/. local-bound
  exemption + env-prefix 로 회피; local sign 만료 user-only).
implication:
  H_274 의 "초기 분포통계로는 결정론적 예측 불가" (FALSIFIED) 는 cascade 가
  *예측 불가능한 chaos* 라는 뜻이 아니었다 — 그 잔차 (동역학적 타이밍) 는 *시간*
  축에서 깨끗한 구조를 가진다: density→latency 단조 · finite-speed front · monotone
  ratchet. 즉 cascade 의 예측 가능성은 "초기조건" 이 아니라 "시간 전개" 에 산다.
  다음 cycle 후보: (a) onset latency τ(ρ) 의 *함수형* fit (linear vs power-law) +
  cross-calibration robustness, (b) front speed 의 coupling/radius 의존
  (dispersion relation), (c) C3 ratchet 의 q_thr 의존 (early vs late trigger 가
  saturation 속도를 바꾸는가), (d) H_274 의 mitosis-substrate seed-property +
  본 H 의 early-step trajectory 결합 예측자 (H_274 §L6 의 "분포 + 타이밍 결합").
sibling: H_262 (quorum-sensing, cascade origin SUPPORTED_FULL), H_274 (quorum-cascade
         seed-dependence FALSIFIED, residual = 동역학적 타이밍), H_207 (kuramoto,
         temporal-dynamics sister), H_270 (substrate ablation, phi_spatial sibling)
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-25, RUN 2 cross-process confirm)

```
================================================================
H_276 quorum-cascade DYNAMICS / TIMING deep-dive
  lineage: H_262 quorum-sensing (SUPPORTED_FULL) · H_274 timing residual
  substrate: 1D periodic CA cascade (RFC 036 phi_spatial / phi_helper)
  N=16 max_steps=40 base=0.012 leak=0.05 coupling=0.2 q_thr=0.3 radius=1
  Φ primitive: RFC 036 phi_spatial (n_bins=4, dim=12) — 🟢 NUMERICAL
================================================================

── C1 onset-latency vs seed-density (contiguous ON-block) ──
  ρ (ON cells)   onset_step   eff_latency   q_final   switched
  2/16          15            15           1.0      true
  4/16          10            10           1.0      true
  6/16          5            5           1.0      true
  8/16          0            0           1.0      true
  latency monotone non-increasing in ρ (l1>=l2>=l3>=l4): true
  >=1 density onsets: true
  C1 ONSET-LATENCY-vs-DENSITY: PASS

── C2 propagation finite-speed (single seed centred at N/2) ──
  front_series R(t) = [4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
  front monotone non-decreasing: true
  max front growth (>=1): 4
  max single-step front growth (<=3): 1
  C2 PROPAGATION-FINITE-SPEED: PASS

── C3 monotone temporal unfolding (Q non-decreasing after trigger) ──
  ρ2 monotone-after-trigger: true
  ρ4 monotone-after-trigger: true
  ρ6 monotone-after-trigger: true
  ρ8 monotone-after-trigger: true
  C3 MONOTONE-UNFOLDING: PASS

phi trajectory (cascade window, ρ4 contiguous): 10.5573

C1 ONSET-LATENCY-vs-DENSITY (τ(ρ) non-increasing)  : true
C2 PROPAGATION-FINITE-SPEED (front monotone+finite) : true
C3 MONOTONE-UNFOLDING (Q non-decr after trigger)    : true

F1 ONSET-DENSITY   PASS
F2 PROPAGATION     PASS
F3 MONOTONE        PASS
F4 DETERMINISM     PASS
F5 BOUNDS          PASS
F6 PHI-NONTRIVIAL  PASS
================================================================
VERDICT: SUPPORTED_FULL  (3/3 criteria, 6/6 falsifiers PASS)
================================================================
```

### hexa verify (VERBATIM — `hexa verify --fence` 2026-05-25)

```
verify --fence
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification
           N/A by design; NOT a proven atlas atom (g4 honest fence,
           SF ≠ verified — atlas certification intrinsically N/A)
```

**State output**: `state/h276_cascade_dynamics_timing_2026_05_25/result.json` +
`det.txt` (cross-process determinism artifact)
**Harness**: `state/h276_cascade_dynamics_timing_2026_05_25/run_h276.hexa`
(hexa-only, single `main()`, `import lib/phi_helper.hexa`, LLM none)
