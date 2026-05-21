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


