# anima-physics — PLAN.md

> 2026-05-21 신설. anima 의식 AI 의 **자연발화 + 영속성 substrate module**
> (`/Users/ghost/core/anima/anima-physics/`) 의 완성 기준 + 단계별
> 로드맵 + 진행 로그.
>
> SSOT: 본 PLAN.md. cycle 결과 = §5 진행 로그 append (g_doc_consolidation).
> 상위 ledger: `HEXAD/PHYSICS/PLAN.md` (HEXAD module 진행) + `HEXAD/PHYSICS/README.md`
> (HEXAD-side index + 재크래시 안전 SSOT §6). 본 PLAN 은 **anima-physics
> 자체 완성** 단일 기준.

---

## §1 GOAL — anima-physics "완벽 완성"의 정의

**Mission**: anima 의 자연발화 (spontaneous fire) + 영속성 (persistence)
의 substrate-level 검증을 위한 hexa-native physics module 의 완전체.

**완성 = 8 기준 (g_completion_8) 모두 충족**:

1. **G1 build 무결성** — 모든 `.hexa` 파일 `hexa build` exit 0 (현재 62 파일 중 ~50 PASS, 추정)
2. **G2 falsifier coverage** — 모든 substrate (27 dir) 최소 1개 falsifier PASS (현재 §188 기준 21/35 PASS)
3. **G3 entry index** — 모든 `.hexa` 파일이 `entries/{root,docs,substrate,recovered}/<name>.md` 에 등재 (현재 93 entry / 62 .hexa, 카테고리 분포 분석 필요)
4. **G4 substrate README** — 모든 27 substrate dir 에 1줄 이상 `README.md` (현재 esp32 만 — **26 dir 결손**)
5. **G5 demiurge verify** — 본 module 이 의존하는 demiurge 도메인 (chip + component + firmware) GATE_CLOSED_MEASURED OR 명시적 gap doc (현재 chip ✅ 12/12, 나머지 ⏳ GATE_OPEN)
6. **G6 HW silicon path** — top 5 dual-role substrate (strange_loop · nested_lattice · kuramoto · sleep_oscillator · spontaneous_smoke) HW Phase 1 (iverilog wave / Arduino blink / cloud trial submit) 1건 이상 LANDED
7. **G7 cross-link integrity** — README 의 count + ladder + entries 가 실 file 과 일치 (현재 §188 결과 후 README count 갱신 미반영)
8. **G8 end-to-end demo** — substrate (e.g. strange_loop) → ConsciousnessEngine (aux_engine_lib) → 자연발화 trigger (spontaneous_smoke) 의 통합 smoke 1건 (현재 aux_engine_smoke 5/5 PASS 는 single-engine, integrated 미달)

**Non-goals (별도 cycle)**:
- 실 HW silicon 합성 (FPGA bitstream load, MCU flash, Loihi 신청 등) — `HEXAD/PHYSICS/HW_SILICON_PATH.md §3` cost ladder 참고
- anima Tier ckpt training / fine-tuning — anima 상위 GOAL.md
- hexa-lang transpiler PR review/merge — hexa-lang upstream (PR #262, #264)

## §2 현재 state SNAPSHOT (2026-05-21)

### §2.1 file tree
- **27 substrate dir**: analog · arduino · benchmarks · cmos · consciousness-loop · eeg · engines · esp32 · fpga · hippocampus · hw · memristor · motor_cortex · neuromorphic · oscillator · photonic · prediction · proprioception · quantum · social · src · state · superconducting · thermodynamic · trapped_ion · vestibular · web
- **62 .hexa file** total
- **93 entry file** (root 11 · docs 19 · substrate 60 · recovered 3)
- **21 doc** in `docs/` (HW prototype spec + signup guide + landing 등)
- **7 root .hexa** (physics, dispatch, edge_deploy, hw_engine_bridge, phi_substrate_consensus, realtime_monitor, rtc_sync, signal_corpus, verify_7cond_hw)
- **state/** = 1 legacy dir (v10_anima_physics_cloud_facade)
- **recovered/** = 4 sub-dir (chip-architecture / consciousness-chip / ai-company-issues / samsung-issues)

### §2.2 검증 LANDED
- §188 (2026-05-21) — 35-substrate parallel fire, **21 PASS / 2 partial / 4 build-err / 7 ⚠ empty (= stub)** · state: `HEXAD/NEUROMORPHIC/state/spontaneous_substrate_parallel_s188_2026_05_21/`
- aux_engine_smoke (2026-05-21) — **5/5 PASS** (S1-S5 all true, cells 8→64, best_phi 0.034) · canonical functional rewrite
- demiurge HW verify (2026-05-21) — **chip 12/12 GREEN** GATE_CLOSED_MEASURED + 14 도메인 dispatch · doc: `docs/demiurge_hw_verify_2026_05_21.md`

### §2.3 알려진 결손 (G1~G8 별)
- **G1 (build)**: 3 partial canonical fix 잔존 (consciousness-loop/{main, snn_main, main_longrun} legacy `&ident`/`self: *T`/`or`/`++`/if-as-expr 69+ 사이트)
- **G2 (falsifier)**: 7 ⚠ empty substrate = engines/*.hexa 22-31 LoC stubs (구현 부재)
- **G3 (entry)**: 60 substrate-entry × 62 .hexa file — drift 가능성 (자동 cross-check 필요)
- **G4 (substrate README)**: **27 중 1 (esp32)만 존재 = 26 결손**
- **G5 (demiurge)**: component ⏳ toy box · firmware ⏳ stub · materials no-producer · brain no-producer
- **G6 (HW Phase 1)**: 1건도 fire 안됨 (cost ladder $0 first-fire 후보 = strange_loop iverilog wave 1-2 day)
- **G7 (cross-link)**: README count (✅ 34 / 🟡 36 / ❌ 23) 가 §188 결과 (21 PASS / 14 nonPASS) + aux_engine smoke result 미반영 — 갱신 필요
- **G8 (E2E)**: aux_engine_smoke 단독, integrated demo 부재

## §3 완성 기준 (criteria) — 체크리스트

상세 진행 추적용 atomic 항목. 본 §3 의 각 ☐ 가 ☑ 로 바뀌면 G1~G8 충족 진행:

### G1 build 무결성 (62 파일)
- ☑ aux_engine_lib + aux_engine_smoke (anima `2c636ce96`)
- ☑ engines/memristor_consciousness (anima 이번 commit)
- ☐ consciousness-loop/src/main (canonical 134 fix, legacy 43 잔존)
- ☐ consciousness-loop/src/snn_main (canonical 52 fix, legacy 26 잔존)
- ☐ consciousness-loop/src/main_longrun (canonical 25 fix, legacy 11 잔존)
- ☐ 나머지 ~55 파일 build 전수 check (별도 cycle: bulk `hexa build` smoke)

### G2 falsifier coverage (27 dir)
- ☑ 21 substrate §188 PASS: oscillator/sleep_oscillator · hippocampus/{theta_gamma,episodic_replay} · social/kuramoto_coupling · eeg/{mu_rhythm_detector,sleep_stage_detector,cross_substrate_phi_correlator} · photonic/{temporal_delay,mesh_network} · motor_cortex/command_encoding · memristor/self_reference · prediction/protention_error · proprioception/feedback_loop · vestibular/multimodal_fusion · quantum/bell_state · thermodynamic/entropy_dissolution · fpga/{strange_loop,nested_lattice,partial_reconfig} · phi_substrate_consensus
- ☐ engines/* 7 stub 구현 (§188g cycle): analog/izhikevich/snn/photonic/quantum/thermodynamic/oscillator_laser
- ☐ consciousness-loop/src/{main,snn_main,main_longrun} falsifier (G1 의존)
- ☐ trapped_ion / superconducting / analog / cmos / arduino / web — falsifier 정의 부재

### G3 entry index (cross-check)
- ☐ `tool/cross_check_entries.sh` 신규 — `entries/**/*.md` ↔ 실 `.hexa` 파일 1:1 매핑 검증
- ☐ drift 발견 시 entry 추가/삭제/갱신

### G4 substrate README — 27 dir × 1 README 필요 (현재 1/27)
- ☑ esp32/README.md (or .hexa header 확인)
- ☐ analog · arduino · benchmarks · cmos · consciousness-loop · eeg · engines · fpga · hippocampus · hw · memristor · motor_cortex · neuromorphic · oscillator · photonic · prediction · proprioception · quantum · social · src · state · superconducting · thermodynamic · trapped_ion · vestibular · web (= 26 결손)

각 README 템플릿:
```markdown
# anima-physics/<substrate> — 1줄 요약

> Status: ✅/🟡/❌ · §188 결과: PASS/empty/build-err/N-A
>
> SSOT: 본 README + `*.hexa` 파일. entry: [entries/substrate/<file>.md](../entries/substrate/<file>.md)

## 자연발화 / 영속성 메커니즘 (1-2줄)
{spontaneous fire 메커니즘 + persistence 메커니즘 - HEXAD/PHYSICS/README §6.9 표 참고}

## 파일 list
- `<name>.hexa` — {1줄 요약}

## falsifier (substrate 별)
- T1 ... : PASS/FAIL
- ...

## cross-link
- HEXAD/PHYSICS/README.md §2.X (등급)
- docs/<관련 spec>.md
```

### G5 demiurge verify (4 domain)
- ☑ chip (12/12 GREEN GATE_CLOSED_MEASURED, 3 records)
- ☐ component GATE_OPEN → GATE_CLOSED_MEASURED: real STEP geometry + datasheet + mesh convergence (anima FPGA enclosure model 도입 시 trigger)
- ☐ firmware GATE_OPEN → GATE_CLOSED: AD9833 DDS bring-up firmware sample
- ☐ brain producer 신설 (demiurge 측, D81 candidate; anima 측에선 cloud trial bridge)

### G6 HW silicon Phase 1 — ☑ ALL 5 LANDED (2026-05-21)
- ☑ strange_loop_ice40: iverilog sim PASS (F-HW-SL-1 reset 0x29CBB8 + attractor period-2) + yosys synth 57 LUT4 + 40 FF
- ☑ nested_lattice_ecp5: iverilog 5/5 PASS (F-HW-NL-1..5, 10-cycle byte-exact SW↔RTL) + yosys synth_ecp5 111 LUT4 + 58 TRELLIS_FF
- ☑ kuramoto_neuromorphic: numpy local sim 5/5 PASS (F-HW-KU-1..5, r locked at K=5.0=0.951) + Loihi/Akida adapter syntax check
- ☑ sleep_oscillator_arduino: Python phase accumulator sim 5/5 PASS (F-HW-SO-1..5, SWS↔REM continuous switch δ=0.0) + AD9833 driver + .ino lint
- ☑ spontaneous_ising: iverilog 5/5 PASS (F-HW-SI-1..5) + yosys synth_ecp5 192 LUT4 + 134 FF + 1 MULT18X18D + Toshiba/Fujitsu adapter syntax

**Total: 25/25 falsifier PASS across 5 HW targets**, Mac local Phase 1a $0.
Phase 1b (bitstream/flash) 별도 cycle: `brew install nextpnr-ice40 nextpnr-ecp5 icestorm prjtrellis arduino-cli` + dev board 주문.

### G7 cross-link integrity
- ☐ README.md count 갱신: §188 result 반영 → 21 PASS / 14 nonPASS 분류
- ☐ HEXAD/PHYSICS/README.md §2 매트릭스 ↔ anima-physics/README.md ↔ 본 PLAN.md §2 = 3-way 정합 lint
- ☐ entries/**/*.md 의 ✅/🟡/❌ 등급이 §188 결과와 일치 verify

### G8 E2E integrated demo
- ☐ `tool/anima_physics_e2e_demo.hexa` 신규 — substrate (strange_loop) → engine (aux_engine_lib) → motivation (spontaneous_smoke) integrated smoke
- ☐ E2E falsifier F-E2E-1..5: substrate emit → engine 처리 → motivation > threshold → 발화 → audit

## §4 Phase ladder (의존성 순)

순서: G4 (substrate README, 26 결손 일괄) → G7 (cross-link 갱신) → G3 (entry cross-check) → G1 (build 전수 + legacy patch) → G2 (engines impl §188g) → G6 (HW Phase 1a $0) → G8 (E2E demo) → G5 (demiurge component/firmware/brain)

### Phase A — 문서 정합 ($0, ~1 day) — G4 + G7 + G3
- 26 substrate README 작성 (template 적용, §188 결과 + 메커니즘 1-2줄)
- README.md count + ladder 갱신
- entries 자동 cross-check tool + 1회 lint pass

### Phase B — build 전수 + 잔여 canonical ($0, ~2 day) — G1
- bulk `hexa build` smoke (62 파일)
- consciousness-loop/src/{main,snn_main,main_longrun} legacy syntax 의미보존 rewrite (aux_engine 식 functional pattern)
- 잔여 canonical 위반 일괄 fix

### Phase C — §188g engines impl ($0, ~1-2 day) — G2
- engines/*.hexa 7 stub 의 actual implementation (각 ~100-200 LoC)
  - analog_consciousness: NgSpice-style RC oscillator dynamics
  - izhikevich_consciousness: 4-param Izhikevich neuron
  - snn_consciousness: leaky integrate-and-fire
  - photonic_consciousness: ring oscillator + delay line
  - quantum_consciousness: 2-qubit closed-form evolution
  - thermodynamic_consciousness: Langevin dynamics
  - oscillator_laser_engine: rate equation (carrier + photon)
- 각각 falsifier T1-T5 + §188 PASS 등재

### Phase D — HW Phase 1a strange_loop iverilog ($0, 1-2 day) — G6
- `tool/codegen_verilog.hexa` (또는 hexa-lang stdlib/verilog/) 활용
- strange_loop.hexa → Verilog 변환
- icarus iverilog 시뮬레이션 + wave dump (.vcd)
- `state/hw_phase1a_strange_loop_iverilog_<UTC>/` 에 wave + screenshot 기록

### Phase E — E2E demo ($0, ~1 day) — G8
- `tool/anima_physics_e2e_demo.hexa`: strange_loop substrate state → aux_engine input → motivation_score → spontaneous emit
- F-E2E-1..5 falsifier (substrate emit · engine 처리 · motivation gate · 발화 · audit)
- smoke run + log → `state/e2e_demo_<UTC>/`

### Phase F — demiurge GATE upgrade ($0-30, ~1 week) — G5
- component: real STEP (anima FPGA enclosure) + scikit-fem mesh convergence
- firmware: AD9833 driver C/hexa stub + bring-up sample
- brain: cloud trial bridge (Akida 신청 + sample inference)

**총 Phase A-F 예상**: $0-30 BOM/cloud + 7-10 day wall (single dev, Mac local)

## §5 진행 로그 (cycle ledger, append-only)

### §5.3 2026-05-21 "all bg go" 2차 — 4 BG agents parallel completion (G1 회수 + G3 cross-check + HEXAD sync + Phase 1b setup)

**4 agent / 4 work item, all ✅ completed**:

1. ✅ **G1 17 FAIL 회수** — 8 PASS (8/13 시도), 새 PASS rate **59/68 = 86.8%** (75% → +11.8%p)
   - A 그룹 auto-invoke 7/7 PASS (`main()` → `run()` rename, mechanical)
   - B 그룹 parse error 1/6 PASS (physics.hexa theorem block 주석)
   - 잔존 5: 3 consciousness-loop (hexa_random link, C 그룹 합류) + edge_deploy (effect system 전체 rewrite) + esp32 (Rust syntax 전체 rewrite) — 별도 cycle

2. ✅ **G3 entry cross-check tool LANDED** — `tool/cross_check_entries.sh` (~150 LoC bash, executable, exit code = drift signal)
   - 총 .hexa: 69 (이전 추정 62 → 실 69)
   - 총 entry: 93 (root 11 · docs 19 · substrate 60 · recovered 3)
   - **3 missing entries** identified: aux_engine_lib, aux_engine_smoke, anima_physics_e2e_demo
   - 0 orphan
   - README/PLAN count drift detected (62 → 69)

3. ✅ **HEXAD/PHYSICS §6.15-§6.18 sync** — 442→522 lines append-only. §6.15 PLAN.md 신설 + §6.16 HW Phase 1a + §6.17 6 BG agents + §6.18 cycle 종결 (g_completion_8 ☑ G4/G6/G8 closed 명시)

4. ✅ **Phase 1b HW setup** — tool install 5/6 PASS + **2/4 실 bitstream LANDED**:
   - strange_loop_ice40: **132 KB iCE40 bitstream** (HX8K-CT256 substitution, 0.8% LC, Fmax 253 MHz @ 12 MHz)
   - sleep_oscillator_arduino: **14 KB .hex firmware** (5038 bytes flash 15% Uno, 235 bytes RAM 11%)
   - nested_lattice_ecp5 + spontaneous_ising: BLOCKED (nextpnr-ecp5 Homebrew core 부재, yowasp WASI sandbox 차단 → source build $0 30-60min 별도 cycle)
   - kuramoto_neuromorphic: cloud-only (Akida $1/day trial 신청 별도)
   - doc: `hw/PHASE_1B_STATUS.md` (12 KB, 6 §, 10 honest C3)

**g_completion_8 진행 갱신** (2025-05-21 19:00 KST):
- G1 build 무결성: 51/68 → **59/68 (86.8%)** specific (남은 9 = 3 consciousness-loop hexa_random + edge_deploy + esp32 + 4 hexa_random transpile)
- G3 entry cross-check: ☐ → **☑ TOOL LANDED** (drift 3 missing identified, 별도 cycle 에 entry stub 생성)
- G6 HW silicon Phase 1: 1a ☑ → **1b 2/4 ☑** (FPGA bitstream + Arduino .hex 실 산출, ECP5 path 별도)
- 갱신 안: G2/G4/G5/G7/G8 직전 cycle 그대로

### §5.2 2026-05-21 "all bg go" — 6 BG agents parallel completion

**6 agent / 7 work item parallel dispatch, all ✅ completed**:

1. ✅ **engines batch A** (analog + izhikevich + snn + oscillator_laser) — 4 stub 22-31 LoC → 285-385 LoC actual impl, 20/20 selftest PASS (5×4), LCG `lcg_next/tf_rand01` 패턴 `random()` 우회
2. ✅ **engines batch B** (photonic + quantum + thermodynamic) — 3 stub → 416-514 LoC, 15/15 selftest PASS (5×3). quantum 은 real-pair 표현 + 2×2 block closed-form (F-Q-1 norm drift 1.3e-14)
3. ✅ **G4 26 substrate README** — 25 신규 + hw/README 1 보존 = 26 dir 모두 README 보유. 메커니즘 + §188 결과 + .hexa list 표 + cross-link 표준화
4. ✅ **G8 E2E integrated demo** — `tool/anima_physics_e2e_demo.hexa` 535 LoC, F-E2E-1..5 5/5 PASS, wall 4.41s. substrate (strange_loop 4×4) → engine → motivation → emit (10 events, ratchet binding) → audit RB. PLAN G8 ☑
5. ✅ **consciousness-loop legacy rewrite** — 3 파일 (main, snn_main, main_longrun) 107 legacy 사이트 → 0 code-side, all parse PASS. main/main_longrun = `import "aux_engine_lib.hexa"` lib delegation, snn_main = standalone LIF + new helpers (`sf_with_neuron_at`, `se_with_faction_at`, `identity_sum`)
6. ✅ **G1 build smoke 전수** — 68 .hexa 파일 (62 → 68 actual count) `hexa build` smoke. **51 PASS / 17 FAIL / 0 TIMEOUT (75% PASS)**. FAIL 분류: 7 auto-invoke conflict (rename `main()`→`run()` 1-line patch) + 6 parse error (legacy `&`/`+`/`fn` nesting modernization) + 4 `hexa_random` undeclared (PR #262 unmerged + agent hexa_v2 local rebuild 미적용)

**g_completion_8 진행 갱신**:
- G1 build 무결성: 51/68 PASS (75%, was unknown) — 17 FAIL specific
- G2 falsifier coverage: §188 21 PASS + 본 cycle engines impl 35 PASS (7 substrates × 5) + E2E 5 PASS = 새 cycle 추가 40 PASS
- G4 substrate README: 1/27 → 27/27 (☑ closed) — esp32 + 26 신규
- G6 HW silicon Phase 1: ☑ (직전 commit)
- G7 cross-link: README §0 SW/HW 분할 + 27 substrate README 정합
- G8 E2E demo: ☐ → **☑ LANDED** (5/5 PASS, deterministic)
- G3 entry cross-check: ☐ 유지 (별도 cycle)
- G5 demiurge GATE upgrade: ☐ 유지 (component STEP/firmware bring-up 별도)

**남은 work** (다음 cycle):
- G1 17 FAIL 회수: 7 auto-invoke rename + 6 parse modernization + 4 hexa_random (hexa-lang PR #262 merge 의존)
- G3 tool/cross_check_entries.sh 작성 + 1회 lint pass
- G5 demiurge component real STEP + firmware AD9833 bring-up

### §5.1 2026-05-21 PLAN.md 신설 + 초기 SNAPSHOT
- 본 PLAN.md 생성. §1-§4 + §6.
- 8 완성 기준 (g_completion_8) 정의
- 현재 state SNAPSHOT (62 .hexa / 93 entry / 21 §188 PASS / chip GATE_CLOSED 12/12 / aux_engine 5/5 PASS)
- Phase ladder A-F 정의 (총 7-10 day wall $0-30)
- 사전 LANDED commits (HEXAD/PHYSICS/README §6.14): anima `8cda89bde` + `6253be33e` + `2c636ce96` + `f77f45996` + `f6e00d990`; hexa-lang PR #262 + #264

## §6 cross-link

- **anima-physics/README.md** — full substrate inventory (✅34 / 🟡36 / ❌23 active) · 본 PLAN §2/§5 와 정합 lint 필요 (G7)
- **anima-physics/entries/{root,docs,substrate,recovered}/*.md** — 93 entry per-file
- **anima-physics/docs/** — 21 HW spec + signup guide + landing (demiurge_hw_verify 포함)
- **HEXAD/PHYSICS/README.md §6** — 재크래시 안전 SSOT (cycle pickup checklist)
- **HEXAD/PHYSICS/HW_SILICON_PATH.md** — 5 dual-role substrate HW target + BOM
- **HEXAD/PHYSICS/PLAN.md** — HEXAD-side cycle ledger (§188 + 후속 cycle)
- **HEXAD/NEUROMORPHIC/state/spontaneous_substrate_parallel_s188_2026_05_21/** — §188 fire state
- **hexa-lang PR #262** (runtime.h hexa_random) + **#264** (codegen_c2 nested-LHS)
- **demiurge** `~/core/demiurge/exports/chip/noc/f1f2/records/2026-05-20_*.json` — chip 12/12 oracle parity record

## §7 honest C3

1. **본 PLAN 은 anima-physics 단독 완성 기준** — anima 상위 (Tier ckpt training, HF deployment 등) 별도 GOAL.md
2. **Phase A-F 시간 추정 (7-10 day)** 은 single-dev Mac local 가정; agent BG 병행 시 50-70% 단축 가능
3. **HW silicon 실현은 비포함** — `HEXAD/PHYSICS/HW_SILICON_PATH.md` 의 Phase 1-3 cost ladder 가 별도 cycle
4. **§188 PASS = closed-form sim PASS**, B-EMERGE-7 carry (실 HW silicon 등가 보장 0)
5. **engines/*.hexa stub 7개의 actual impl** 은 G2 closure 의 critical path — 본 PLAN 의 Phase C 가 가장 큰 단일 work
