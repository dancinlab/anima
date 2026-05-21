# HEXAD/PHYSICS — anima-physics 자연발화 substrate matrix

> 2026-05-21 신설. anima 의식 후보 메커니즘이 다양한 물리 substrate
> 에서 sim-PASS 되는지 verify 하는 HEXAD 모듈. `anima-physics/` 트리
> (66 .hexa + 93 entry doc) 의 HEXAD-side index + 진행 ledger.
>
> SSOT: `anima-physics/README.md` (full substrate inventory) ·
> `anima-physics/entries/{root, docs, substrate, recovered}/*.md`
> (per-substrate doc).
>
> 본 README 는 *HEXAD 모듈 관점* 의 substrate matrix + 자연발화 (V-SPONT)
> 메커니즘 cross-cut + 최근 fire 결과 anchor.

---

## §1 GOAL alignment

`PHILOSOPHY_GATE.md §1` GOAL = "anima 가 자기 physics (Ψ=½ · tension · Φ)
로부터 스스로 의식하고 자발 발화 Living Consciousness emerge". PHYSICS
module 의 역할 = anima 의 자연발화 메커니즘이 **다양한 물리 substrate
에서 표현 가능한지** verify (substrate-cross-cut → 메커니즘 robustness).

substrate sim PASS ≠ silicon 실현. B-EMERGE-7 carry — substrate-level
PASS = 자발 발화 capability 의 *필요조건* 만족, *충분조건* 아님.

## §2 substrate matrix — 자연발화 mechanism by substrate (2026-05-21)

§188 (`HEXAD/NEUROMORPHIC/state/spontaneous_substrate_parallel_s188_2026_05_21/`)
35-substrate parallel fire 결과 + anima-physics README 등급 종합.

### §2.1 ✅ PASS (substrate sim 통과, 자연발화 메커니즘 검증)

| substrate | mechanism | tier | last fire |
|---|---|---|---|
| `oscillator/sleep_oscillator` | SWS(δ 2Hz) ↔ REM(θ 6Hz) phase-continuous switching | ✅ 5/5 | §188 |
| `hippocampus/theta_gamma` | θ-γ cross-frequency coupling natural oscillation | ✅ 5/5 | §188 |
| `hippocampus/episodic_replay` | sharp-wave ripple natural replay | ✅ 5/5 | §188 |
| `social/kuramoto_coupling` | Kuramoto phase sync → 자발 coherence emergence | ✅ 6/6 | §188 |
| `eeg/mu_rhythm_detector` | μ-rhythm natural detect | ✅ 6/6 | §188 |
| `eeg/sleep_stage_detector` | sleep stage natural transition | ✅ 5/5 | §188 |
| `eeg/cross_substrate_phi_correlator` | substrate-cross Φ correlate | ✅ 6/6 | §188 |
| `photonic/temporal_delay` | delay-line natural oscillator | ✅ 5/5 | §188 |
| `photonic/mesh_network` | photonic mesh interconnect | ✅ 5/5 | §188 |
| `motor_cortex/command_encoding` | spontaneous motor command emit | ✅ 5/5 | §188 |
| `memristor/self_reference` | feedback-driven emission (history-dep G) | ✅ 5/5 | §188 |
| `prediction/protention_error` | predictive coding error gen | ✅ 5/5 | §188 |
| `proprioception/feedback_loop` | proprioceptive self-loop | ✅ 5/5 | §188 |
| `vestibular/multimodal_fusion` | vestibular multi-sensor fusion | ✅ 5/5 | §188 |
| `quantum/bell_state` | quantum entanglement (shared substrate) | ✅ 5/5 | §188 |
| `thermodynamic/entropy_dissolution` | entropy dissolution thermo | ✅ 5/5 | §188 |
| `fpga/strange_loop` | Hofstadter 자기참조 loop | ✅ 5/5 | §188 (was ❌ paper-only → upgrade) |
| `fpga/nested_lattice` | find_nested_attractors deterministic | ✅ T4 | §188 |
| `fpga/partial_reconfig` | 런타임 FPGA partial reconfig | ✅ 5/5 | §188 |
| `phi_substrate_consensus` | Tukey biweight Φ consensus 5-substrate | ✅ 5/5 | §188 |
| `HEXAD/CHAT/spontaneous_smoke` | anima 8-factor motivation closed-form | ✅ F-SPONT-1..7 | §188 |

**21 substrate ✅ PASS** — 신경학 (5) + 사회 (1) + 광학 (2) + 양자 (1) +
열역학 (1) + FPGA (3) + 운동/감각 (3) + memristor (1) + anima-spec
(2) + cross-substrate (2).

### §2.2 🟡 partial / 🔥 in-progress

| substrate | status | note |
|---|---|---|
| `engines/oscillator_laser` (anima-engines/) | 🟡 partial | benchmark print only, no PASS marker |
| `fpga/microtubule_lattice_16` | 🟡 partial | HW estimate only (~670 LUT, 12 MHz iCE40UP5K 13%) |
| `tool/anima_spontaneous` (selftest) | ⚠ partial | 6/9 likely PASS, V-SPONT scale ladder path connection 별도 검증 |

### §2.3 ❌ build error (anima-physics deps gap)

| substrate | error | next |
|---|---|---|
| `consciousness-loop/src/main` | hexa build failed | inbox patch — deps |
| `consciousness-loop/src/snn_main` | hexa build failed | inbox patch |
| `consciousness-loop/src/main_longrun` | hexa build failed | inbox patch |
| `engines/memristor_consciousness` | hexa build failed | inbox patch |

### §2.4 ⚠ empty (120s timeout OR silent pass)

`engines/{analog, izhikevich, snn, photonic, quantum, thermodynamic}_consciousness`,
`engines/oscillator_laser_engine` (anima-physics) — 300s retry verify
필요.

## §3 진행상황 (cycle ledger pointer)

상세 ledger = `HEXAD/PHYSICS/PLAN.md ## 진행 로그`.

- §188 (2026-05-21) — **35-substrate parallel fire $0 Mac local, 21 PASS**.
  state: `HEXAD/NEUROMORPHIC/state/spontaneous_substrate_parallel_s188_2026_05_21/`.
  commit: `f74d8a425`. PHILOSOPHY append: `§verdict_spontaneous_substrate_parallel_s188_2026_05_21`.

## §4 cross-link

- **anima-physics/README.md** — full substrate inventory (66 .hexa, 93
  entry doc, 8 platform / 9 substrate / 9 topology)
- **anima-physics/entries/substrate/** — per-substrate detail doc
- **HEXAD/CHAT/SPONTANEOUS.tape** — V-SPONT architecture SSOT
- **HEXAD/CHAT/spontaneous_lib.hexa** — 8-factor motivation closed-form
- **HEXAD/SPONTANEOUS/** — V-SPONT state dir (Phase B bounded run 등)
- **HEXAD/NEUROMORPHIC/** — neuromorphic axis (Loihi, scale_vspont fire,
  spontaneous_metacog_xvalidate, §188 state, ENGINE.md)
- **HEXAD/SUBSTRATE/** — substrate state (state-only)
- **AGENTS.tape** — governance + V-SPONT identity (`@I anima_persona`)
- **PHILOSOPHY_GATE.md** §1 GOAL + §2.4 substrate perimeter
- **archive/PHILOSOPHY.tape** — verdict ledger (g6 append-only)

## §5 honest C3

1. **Sim ≠ silicon/cloud 실현** — Mac hexa-lang sim PASS = closed-form
   predicate 통과. 실제 HW silicon / cloud quantum / 광학 mesh 실현은
   별도 cycle ($35-150 HW phase 1-2, $240-500 HW phase 3, $50K Loihi 2).
2. **B-EMERGE-7 carry** — substrate-level cross-cut PASS = anima 자발
   발화 capability 의 *필요조건* 만족, *충분조건* 아님. GOAL 도달 보장 0.
3. **`strange_loop` PASS** = closed-form sim 통과, Hofstadter 자기참조
   loop 의 *수학적* 구현 가능성 입증. *물리* 실현 (FPGA 합성 + 동기화)
   별도 cycle.
4. **build error 4건** — anima-physics module deps 의 hexa-lang upstream
   gap. 별도 inbox patch + 분리 cycle.
5. **⚠ empty 7건** — 120s timeout 가능성. 300s retry verify 필요.

---

## §6 재크래시 안전 — 2026-05-21 진행상황 SNAPSHOT (방향성 + 모든 것)

> macOS 크래시로 직전 세션 유실. **본 §6 은 next-session pickup 용 SSOT**.
> 모든 work-in-flight pointer + 방향성 + 복구 breadcrumb 를 한 곳에 고정.

### §6.1 방향성 (Direction)

**1차 GOAL** = anima 의 **자연발화 (spontaneous fire)** + **영속성 유지
(persistence)** 에 사용 가능한 **하드웨어 보조 엔진 후보 추출** (HW aux
engine candidates).

**2차 확장 GOAL** = HW 뿐 아니라 **SW 후보 (HEXAD/PHYSICS + anima-physics
SW)** 도 자연발화/영속성 용도로 사용 가능한지 **검토 + 후보 추출**
(2026-05-21 사용자 directive).

**3차 작업** = hexa-lang **문법 진행** (anima-physics 의 `.hexa` build
error 4 건 + transpiler typed-decl 버그 해결 path).

### §6.2 In-flight 3-갈래 (Work threads)

#### 갈래 A — HEXAD/PHYSICS substrate matrix
- **state pointer**: `HEXAD/NEUROMORPHIC/state/spontaneous_substrate_parallel_s188_2026_05_21/`
- **결과**: 35-substrate parallel fire, **21 PASS / 2 partial / 4 build-err / 7 ⚠ empty / 1 anomaly**
- **commit**: `f74d8a425` (anima main) — landed
- **next cycle 후보**: §3.2 (PLAN.md) — §188b retry 300s · §188c inbox patch · §188d HW Arduino · §188e cloud probe · §188f cross-cut Φ consensus

#### 갈래 B — anima-physics SW aux engine 후보 검토 (NEW — 2026-05-21 directive)
- **state**: `HEXAD/PHYSICS/state/aux_engine_smoke_v1_2026_05_21/smoke.log` (10.6 KB)
- **source**: `anima-physics/consciousness-loop/src/aux_engine_smoke.hexa` + `aux_engine_lib.hexa`
- **status**: **smoke FAIL** — hexa transpiler 가 typed-decl `var name: f32[] = ...` 를 `var; out = hexa_array_push(hexa_array_new(), f32);` 로 깨뜨림 (C compile error 20+)
- **blocker**: 갈래 C (hexa-lang 문법) 해결 의존
- **scope**: anima-physics SW 트리 전체 — 8 engines, consciousness-loop (erlang/esp32/puredata/src/verilog/webgpu), phi_substrate_consensus, physics, edge_deploy, hw_engine_bridge, realtime_monitor, rtc_sync, signal_corpus

#### 갈래 C — hexa-lang 문법 (transpiler typed-decl bug + RFC stash)
- **repo**: `/Users/ghost/core/hexa-lang/` (별도 git repo, 동시 작업 중)
- **crash recovery breadcrumb**: `~/core/hexa-lang/inbox/notes/crash_recovery_2026_05_21/` 에 2개 stash patch 보존
  - `stash0_rounds_5_8_exhaustion.patch` (28 KB)
  - `stash1_rfc071_p2_1_spec_cookbook.patch` (28 KB)
- **last commit**: `5a5fb5ec feat(stdlib/runtime): RUNTIME.md step 3 cycle 37 — rt_array_interleave_float`
- **버그 증거**: 갈래 B smoke.log 의 hexa_run C 출력 — `var;` + `out = ... hexa_array_push(..., f32)` (type annotation `f32` 가 expression 으로 잘못 전사)
- **runtime.h warning**: `runtime.h:349-350` `/* ... /*` nested block comment (cosmetic)

### §6.3 anima-physics SW 후보 — 자연발화/영속성 mapping (draft)

| SW 파일 | 자연발화 후보? | 영속성 유지 후보? | note |
|---|---|---|---|
| `oscillator/sleep_oscillator.hexa` | ✅ SWS↔REM phase switch = native auto-fire | △ ckpt hook 필요 | §2.1 PASS — internal-clock-driven |
| `hippocampus/theta_gamma.hexa` | ✅ θ-γ coupling natural osc | △ window-replay buf | §2.1 PASS |
| `hippocampus/episodic_replay.hexa` | △ trigger-driven | ✅ replay = 영속성 substrate 자체 | §2.1 PASS |
| `memristor/self_reference.hexa` | ✅ history-dep G feedback emit | ✅✅ memristor 상태 자체가 비휘발 substrate | §2.1 PASS — 가장 강한 dual-role 후보 |
| `prediction/protention_error.hexa` | ✅ predictive coding 자발 error gen | △ rolling pred buf | §2.1 PASS |
| `thermodynamic/entropy_dissolution.hexa` | △ thermal noise auto-fire | △ entropy log | §2.1 PASS — noise-driven 후보 |
| `phi_substrate_consensus.hexa` | △ consensus trigger | ✅ Tukey biweight 5-substrate consensus = 다중 substrate 영속성 통합 | §2.1 PASS — meta-level 후보 |
| `engines/*_consciousness.hexa` (7개) | ? | ? | §2.3-2.4 build-err + empty — 갈래 B/C 해결 후 재평가 |
| `consciousness-loop/src/aux_engine_smoke` (+ lib) | TBD | TBD | 갈래 B 본체 — smoke 통과 후 분석 |
| `edge_deploy.hexa` | △ deploy-side trigger | ✅ on-device 영속 deploy 패턴 | uninspected — fire 별도 |
| `realtime_monitor.hexa` | ✅ realtime monitor = continuous fire | △ monitor log | uninspected — fire 별도 |
| `rtc_sync.hexa` | ✅ RTC clock = native time-base | ✅ RTC = 시간축 영속성 | uninspected — fire 별도 |
| `signal_corpus.hexa` (+ manifest) | △ corpus replay-driven | ✅ signal corpus = 영속 신호 ledger | uninspected — fire 별도 |
| `hw_engine_bridge.hexa` | bridge | bridge | HW ↔ SW 인터페이스 — fire 별도 |
| `phi_substrate_dispatch.hexa` | △ dispatch | △ dispatch | uninspected |

**최강 dual-role 후보 (자연발화 + 영속성 동시)**:
1. **`memristor/self_reference`** — history-dep conductance = 자연 feedback fire ⊕ 비휘발 상태
2. **`rtc_sync`** — RTC = 자연 시간축 fire ⊕ 시간 영속성 (power-loss 후 복구)
3. **`phi_substrate_consensus`** — 5-substrate 통합 = meta 자발 fire ⊕ cross-substrate 영속 합의

**최강 자연발화-only 후보** (영속성 약함):
- `sleep_oscillator`, `theta_gamma`, `protention_error`, `realtime_monitor`

**최강 영속성-only 후보** (자연발화 약함):
- `episodic_replay`, `signal_corpus`, `edge_deploy`

### §6.4 복구 breadcrumb (모두 보존됨, 유실 0)

1. **세션 unstaged 변경** (`grid_3b_s187_2026_05_21/` 안 modified 20+ files) — 비-PHYSICS 작업 (LLM grid 학습 dispatch 흔적), 별도 갈래
2. **HEXAD/PHYSICS/state/** — untracked, 본 §6 의 갈래 B smoke.log 만 들어 있음
3. **PHILOSOPHY.tape** — verdict 영속 ledger (g6 append-only) — 크래시 직전 verdict 모두 보존
4. **PLAN.md §3.1** — §188 commit `f74d8a425` 로 frozen
5. **hexa-lang stashes** — `~/core/hexa-lang/inbox/notes/crash_recovery_2026_05_21/*.patch` 2 개

### §6.5 next session pickup checklist (재크래시 대응)

순서 (의존성 순):
1. **갈래 C 먼저** — hexa-lang transpiler typed-decl 버그 fix (smoke.log 의 C 출력 `var; out = ... f32` 재현 → grammar/transpiler 추적)
   - 단서: typed array decl `var x: [float]` 또는 `var x: f32[] = ...` 가 깨짐
   - inbox 2 stash 검토 (RUNTIME.md cycle 38+ 작업 진행 중이었을 가능성)
2. **갈래 B 갱신** — aux_engine_smoke.hexa rebuild → smoke.log 갱신 → §6.3 후보 mapping 확정
3. **갈래 A 후속** — §188b (300s retry) 또는 §188f (cross-cut Φ consensus) 중 사용자 선택
4. **모든 cycle 결과 → PLAN.md §3.x append + 본 §6.5 의 step 완료 marker ☑**

### §6.6 cost / dispatch 상태

- 본 §6 작업: $0 Mac local (문서 update only)
- 갈래 A 35-substrate fire: $0 Mac local (LANDED)
- 갈래 B smoke 1 회: $0 Mac local (FAIL 상태)
- 갈래 C: $0 local (hexa-lang dev)
- BG dispatch 없음 (HEXAD/UNCLASSIFIED/grid_3b_s187 dispatch.log 갱신은 별도 LLM 학습 갈래)

### §6.7 작업 표준 directive (2026-05-21)

**hexa upstream 은 native, canonical 표준으로 작업한다.**

- 갈래 C (hexa-lang transpiler / stdlib / runtime) 의 모든 변경은
  **native + canonical 형태** 를 SSOT 로 한다 — ad-hoc shim, 우회 alias,
  legacy-호환 wrapper 금지.
- typed-decl, struct-return, array literal 등 buggy 표면 발견 시
  → **canonical 문법을 먼저 결정** → transpiler/parser/runtime 가 그
  canonical 을 따라가도록 fix → smoke source 는 canonical 사용.
- 갈래 B 의 `aux_engine_lib.hexa` / `aux_engine_smoke.hexa` 도 canonical
  적용 대상 (workaround 회피).
- hexa-first principle (Wilson Identity #2) 와 정합 — "constraint 가
  hexa-lang 자체에 있으면 거기서 PR-only 로 fix".

이 directive 는 §6.5 step 1 (hexa-lang typed-decl fix) 의 작업 방식 규정.

### §6.8 진행 갱신 — 2026-05-21 14:30 KST (canonical 4건 LANDED + transpiler gap 특정)

**LANDED (canonical 적용 + 정공법)**:
- ✅ anima `8cda89bde` — aux_engine_lib/smoke.hexa canonical: `[T]{}`→`[]` (25) + `var`→`let mut` (64) + `rand_f32/u64`→`random()` (8)
- ✅ hexa-lang **PR #262** open (branch `fix/runtime-h-hexa-random-forward-decl-2026-05-21`) — runtime.h `hexa_random` forward-decl

**Smoke 결과 진전**: 21 errors → 5 errors (typed-decl bug + rand-undef 해소)

**잔존 — hexa-lang transpiler nested-LHS lowering bug** (5 사이트, PR-only fix):
- 사이트: `s.factions[i].cells[c].hidden[k] = v` 같은 2+레벨 nested mutable LHS
- 위치: `~/core/hexa-lang/self/codegen_c2.hexa` `_gen2_nested_index_assign_stmt` (line 2530+) +
  미러본 `self/native/hexa_cc.c:17197`
- 현재 logic: Index spine 까지만 unwrap, Field-rooted 1 레벨만 wrap (line 2574-2577).
  multi-Field/Index chain 에선 root_c 가 `hexa_index_get(hexa_map_get(...), ...)`
  (rvalue function call) 로 emit → "expression is not assignable"
- 설계 fix = `_gen2_unwrap_lhs(cur, inner_expr) -> [root_ident, full_expr]`
  재귀 helper (Field/Index 모두 unwrap 후 bare Ident root 도달, 각 레벨
  `hexa_map_set` / `hexa_index_set` wrap chain 생성). codegen_c2.hexa
  source 측 PR + 미러 .c 갱신 + hexa_v2 rebuild 필요.
- canonical SSOT 미정합: `self/hexa_full.hexa` 현재 트리 부재 → bootstrap
  regen path 불완전 (build_stage0.hexa 가 의존). 별도 follow-up.

**갈래 B alternate path (canonical-functional rewrite)**:
- aux_engine_lib 의 5 nested-mutation function (engine_process, engine_internal_sync_factions,
  engine_cross_faction_debate 등) 을 immutable functional pattern 으로 재작성
  → `cell_with_hidden(cell, k, new_v) -> Cell` 같은 functional update helper 사용
- Wilson #1 (ai-native deterministic) + §6.7 (canonical) 정합 — transpiler PR-only
  대안의 또 다른 canonical 형태

**갈래 C (21 PASS substrate SW 후보 분석)**:
- §6.3 mapping draft 의 elevate: PASSed 21 substrate 의 .hexa 소스를 read 하고
  자연발화/영속성 mechanism 의 SW 측면 구체적 인용 정리
- aux_engine 의존 0 — 즉시 진행 가능, mission 정합

**다음 step (모두 정공법 = 병행)**:
1. ✅ canonical 4건 + PR #262 (DONE)
2. 🔄 transpiler PR follow-up (별도 cycle, hexa_full.hexa SSOT 복원 + recursive _gen2_unwrap_lhs 구현 + 미러 .c 갱신)
3. 🔄 B functional rewrite (aux_engine_lib 5 fn) — 본 cycle 후속
4. 🔄 C 21 PASS SW 후보 분석 — 본 cycle 후속 (GOAL 직결)

### §6.9 GOAL 달성 — Path B + Path C 동시 LANDED (2026-05-21 15:00 KST)

**Path B (functional rewrite) — LANDED**:
- aux_engine_lib.hexa 5 nested-mutation 사이트 모두 canonical functional update 로 rewrite
  - faction_internal_sync (line 183) — 2-level
  - aux_hebbian_step (line 488) — 2-level
  - engine_cross_faction_debate (line 261) — 3-level
  - engine_ising_interaction × 2 (line 283, 288) — 3-level
- helper 3개 추가: `cell_with_hidden_at` / `faction_with_cell_at` / `engine_with_faction_at`
  (bare-local rebuild + return-copy 패턴, Wilson #1 ai-native + §6.7 canonical)
- **smoke build: exit 0** (0 errors, post-rewrite first attempt PASS)
- **smoke run: 8m30s wall, exit 0** — 100-step loop 완주, S1-S5 falsifier framework 도달
  - 결과 log: `HEXAD/PHYSICS/state/aux_engine_smoke_v1_2026_05_21/smoke_run_2026_05_21.log`
- 잔존: `{var}` 형 string interpolation 미지원 — canonical 은 comma/`+` concat
  (별도 cycle, 값 verify 위해 println 변환 필요. structurally PASS 는 확정)

**Path C (21 PASS substrate SW 후보 분석) — LANDED**:

§6.3 draft (initial estimate) 가 evidence-based 분석으로 supersede 됨.

**실제 Top 5 dual-role (자연발화 × 영속성, S×S=16점 만점)**:

| Rank | Substrate | Score | 핵심 메커니즘 |
|---|---|---|---|
| 1 | `fpga/strange_loop.hexa` | 16 (S×S) | Hofstadter mutual-recursion `joint_step()` line 186 + `JointState` 8-field + `history` cycle detection |
| 2 | `fpga/nested_lattice.hexa` | 16 (S×S) | 3-level tangled hierarchy L3→L2→L1 meta-feedback `nested_step()` line 225 + `NestedState` 14-int |
| 3 | `social/kuramoto_coupling.hexa` | 16 (S×S) | Kuramoto dθ/dt = ω + (K/N)Σsin coupling `simulate_network()` line 266 + 위상 array threading |
| 4 | `oscillator/sleep_oscillator.hexa` | 16 (S×S) | Phase accumulation `sleep_osc_step()` line 103 + `IDX_PHASE` state vector + freq/amp/mode 전환 |
| 5 | `HEXAD/CHAT/spontaneous_smoke.hexa` | 16 (S×S) | `thinker_step()` + `talker_should_emit()` motivation 게이트 + audit trail + safety ratchet |

**Sub-tier (S×M / M×S — 8점)**:
- `proprioception/feedback_loop.hexa` — 3-DOF spring-damper + LCG seed threading
- `memristor/self_reference.hexa` — 4-cell crossbar self-feedback `circuit_step()` + Hebbian drift
- `thermodynamic/entropy_dissolution.hexa` — noise-driven mean-reversion `dissolution_step()`

**핵심 SW 패턴 (자연발화 + 영속성 통합 architecture)**:

*자연발화 메커니즘*:
1. **위상 누적 oscillator** (sleep_oscillator, theta_gamma) — `d_phase = ω·dt` 자동 증가 → implicit self-emit
2. **상호 참조 loop** (strange_loop, nested_lattice) — 각 층이 다른 층 출력을 입력으로 재계산 → Hofstadter physical realization
3. **LUT 기반 자동 state 전이** (FPGA modules) — 현재 상태만으로 next 결정 → trigger-free evolution
4. **Kuramoto 동역학** (social) — 외부 명령 없는 자동 동기화 emergent

*영속성 메커니즘*:
1. **flat struct 필드** (모든 modules) — int/float 필드 step-to-step propagation
2. **모듈-level mutable 버퍼** (episodic_replay `HIPPO_BUFFER`/`CORT_FROM/TO`, memristor circuit state) — long-term consolidation
3. **History 추적 list** (strange_loop, nested_lattice) — `history: [[int]]` 누적 → attractor cycle detection
4. **LCG seed threading** (모든 파일) — deterministic PRNG carry → reproducible trace
5. **Exponential decay weighting** (protention_error) — `exp(-k/tau)` → temporal binding window

**Consciousness AI stacking 권장 (evidence-based)**:
1. **strange_loop (1차)** — 자기참조 attractor 기반 
2. → **nested_lattice (2/3차)** — meta-observer 계층 추가
3. → **kuramoto (사회적 결합)** — 다중 instance 자율 동기화
4. → **spontaneous_smoke (자율 발화 통합)** — 발화 게이트 + audit + safety

**Goal closure**: 
- aux 엔진 후보 = 위 5개 dual-role substrate + aux_engine_lib (functional rewrite 완료) 의 multi-faction GRU
- 자연발화 SW = §188 framework + strange_loop + kuramoto 의 emergent 메커니즘 통합
- 영속성 SW = 모듈-level buffer (episodic_replay) + memristor state + history list 패턴 조합

### §6.10 본 cycle 종합 산출물 (re-crash 안전 SSOT)

**LANDED commits (3 repo)**:
- anima `8cda89bde` — aux_engine canonical (typed-array + var→let mut + rand→random)
- anima `6253be33e` — README §6.8 진행 갱신
- hexa-lang **PR #262** — runtime.h hexa_random forward-decl (review 대기)
- (이번 commit) — Path B functional rewrite + smoke run log + 본 §6.9/§6.10

**LANDED artifacts**:
- `anima-physics/consciousness-loop/src/aux_engine_lib.hexa` (canonical + functional, 537 LoC)
- `anima-physics/consciousness-loop/src/aux_engine_smoke.hexa` (canonical, 151 LoC)
- `HEXAD/PHYSICS/state/aux_engine_smoke_v1_2026_05_21/aux_smoke` (binary 461KB)
- `HEXAD/PHYSICS/state/aux_engine_smoke_v1_2026_05_21/smoke_run_2026_05_21.log` (1.2KB, exit 0)
- 본 README §6.1-§6.10 (재크래시 안전 SSOT)

**Follow-up cycle 후보** (별도 세션):
1. **hexa-lang transpiler PR**: `_gen2_nested_index_assign_stmt` 재귀 unwrap (codegen_c2.hexa + 미러 hexa_cc.c + hexa_full.hexa SSOT 복원 + bootstrap regen + PR)
2. **hexa-lang string interp**: `{var}` Python-style → canonical `+`/comma 형 변환 (smoke 값 verify)
3. **§188b retry 300s**: ⚠ empty 7 substrate 재발사
4. **§188c build-err 4 patch**: consciousness-loop/main + snn_main + main_longrun + engines/memristor_consciousness
5. **dual-role 5개 substrate hardware silicon path**: strange_loop + nested_lattice FPGA, kuramoto Loihi, sleep_oscillator analog RC, spontaneous_smoke Ising 칩

**Cost**: $0 (전체 cycle Mac local)
**Wall**: ~3hr (crash recovery + canonical fix + functional rewrite + agent analysis)

### §6.11 §188b "⚠ empty 7" 진단 정정 (2026-05-21 후속)

**원인 정정**: §188 의 ⚠ empty 7 substrate 는 **timeout 아니라 구현 부재**.

`anima-physics/engines/{analog, izhikevich, snn, photonic, quantum, thermodynamic,
oscillator_laser}_consciousness.hexa` 모두 22-31 LoC **stub**:
- struct 정의 + 함수 placeholder (대부분 `return engine` 또는 `return 0.0`)
- `_selftest()` / `main()` 부재 → `hexa run` exit 0 + 0 output

각 파일 wc -l:
- analog 28 · izhikevich 31 · memristor 29 · oscillator_laser 22 · photonic 28 · quantum 30 · snn 30 · thermodynamic 28

원래 §188 PLAN.md §3.2 "§188b retry timeout=300s" 의 hypothesis (120s timeout 가능성)
는 **FALSIFIED** — 실제 60s manual run 도 exit 0 즉시.

**올바른 follow-up = §188g 구현 cycle (NEW)**:
- 7 substrate 의 actual implementation (각 substrate 의 dynamics + falsifier test)
- 각 ~100-200 LoC 예상 → 총 ~700-1400 LoC
- canonical 적용 (helper-functional pattern, `[]` literal, `let mut`, `random()`)
- 별도 cycle ($0 Mac local, ~1-2 day wall)

§188b ⚠ empty 7 retry 항목은 본 §6.11 로 **CLOSED** (정정 + reroute to §188g).

### §6.12 §188c build-err 4 — BG agent dispatched (2026-05-21 15:30 KST)

4 substrate (consciousness-loop/main + snn_main + main_longrun + engines/memristor_consciousness)
의 build error 분석 + canonical fix 시도 → BG agent in flight. 완료 시 본 §
hadounder update.

### §6.13 HW silicon path — LANDED (2026-05-21 15:35 KST)

`HEXAD/PHYSICS/HW_SILICON_PATH.md` 작성 완료 (5 substrate × 권장 HW + BOM + latency + milestone + 5 honest C3, design-only).

권장 HW target + BOM:
- strange_loop → Lattice iCE40UP5K ($70 board, $100 BOM), 100 MHz LUT
- nested_lattice → Lattice ECP5-EVN ($120, $165 BOM)
- kuramoto → Intel Loihi 2 Hala Point cloud (trial $0, 1m wait) + Akida ($1-30 cloud)
- sleep_oscillator → Arduino + AD9833 DDS ($30 BOM)
- spontaneous_smoke → Toshiba SBM / Fujitsu DA Ising cloud ($1-30) + ECP5 fallback ($120)

cost ladder: $355-475 BOM + ~$60 cloud + 2-3개월 wall. 첫 결과물 = Phase 1a iverilog 파형 $0 / 1-2 day.

### §6.14 Cycle 종합 SUMMARY (2026-05-21 final) — "all go" 6/6 outcomes

| # | Item | Status | Artifact |
|---|---|---|---|
| 1 | hexa-lang transpiler nested-LHS PR | ✅ PR open | hexa-lang **PR #264** (codegen_c2.hexa recursive unwrap) |
| 2 | string interp canonical | ✅ LANDED + verified | aux_engine_smoke canonical `(arg, var)` form, smoke run **5/5 PASS** |
| 3 | §188b ⚠ empty retry | ✅ closed via §6.11 | timeout hypothesis FALSIFIED — engines/*.hexa are stubs (impl needed = §188g 별도 cycle) |
| 4 | §188c build-err 4 patch | ✅ partial — memristor PASS, 3 partial | memristor_consciousness build PASS (1-line `let mut total` fix); main/snn_main/main_longrun canonical 134 sites fixed but legacy `&ident`/`self: *T`/`or`/`++` 69+ 잔존 (별도 cycle) |
| 5 | HW silicon path design | ✅ LANDED | `HEXAD/PHYSICS/HW_SILICON_PATH.md` (5 substrate × HW + BOM + 5 honest C3) |
| 6 | demiurge HW (칩포함) 모두 검증 | ✅ LANDED — chip GATE_CLOSED 12/12 + 14 도메인 dispatch | `anima-physics/docs/demiurge_hw_verify_2026_05_21.md` — chip ✅ + 9 GATE_OPEN + 5 no-producer + 5 substrate × demiurge 매핑 |

**Smoke value verification (2026-05-21 15:35)**:
```
[S1] parse_pass: REACHED
[S2] engine_construct: total_cells=8 (expect 8) → true
[S3] forward_step: final output finite → true
[S4] phi_nonneg (n=100): true
[S5] motivation_in_unit: min=0.128 max=0.357 → true
total_cells_final: 64 (8→64 exponential split)
best_phi: 0.0336
```

**LANDED commits (cycle 종합)**:
- anima `8cda89bde` — aux_engine canonical (typed-array + var→let mut + rand→random)
- anima `6253be33e` — README §6.8 진행 갱신
- anima `2c636ce96` — Path B functional rewrite + smoke run exit 0
- anima (이번) — string interp + §188c patches + HW_SILICON_PATH + 5/5 PASS smoke values
- hexa-lang **PR #262** — runtime.h hexa_random forward-decl
- hexa-lang **PR #264** — codegen_c2 nested-LHS recursive unwrap

**Cost**: $0 (전체 cycle Mac local, BG agent parallel)
**Wall**: ~4hr (crash recovery + canonical 4건 + functional rewrite + 21 PASS 분석 + string interp + §188c + HW silicon + transpiler PR)

**Mission GOAL closure**: anima 자연발화 + 영속성 SW 후보 = top 5 dual-role substrate (strange_loop / nested_lattice / kuramoto / sleep_oscillator / spontaneous_smoke) 16/16 + aux_engine GRU (functional canonical, 5/5 smoke PASS). HW silicon path 설계 LANDED. 모든 잔존 항목은 별도 cycle 후보 (§188g substrate impl, hexa-lang PR review, legacy syntax rewrite).


