# AUX — anima-physics 보조엔진 도메인 (index)

> anima 자연발화 (spontaneous fire) + 영속성 유지 (persistence) 의
> **하드웨어/소프트웨어 보조엔진 후보** general roadmap. 본 module
> 산하 모든 substrate × HW target 의 dual-role 평가 + cost ladder +
> 부팅 sequence 인덱스.
>
> Wilson #4 domain-meta-domain: AUX = "보조엔진" 단일 domain. 산하
> per-HW doc:
> [AKIDA pack](../../SUB_ENGINES/AKIDA/) — `/SUB_ENGINES/AKIDA/` 신규 pack (Pi 5 + AKD1000 도착예정, 사용자 directive 2026-05-21 root 분리) ·
> [`FPGA.md`](FPGA.md) (iCE40 + ECP5 bitstream LANDED) ·
> [`DDS.md`](DDS.md) (Arduino + AD9833 .hex LANDED) ·
> [`ISING.md`](ISING.md) (ECP5 fallback bitstream LANDED) ·
> [`LOIHI.md`](LOIHI.md) (NRC research access wait)
>
> SSOT: 본 `AUX/README.md` (index) + `../PLAN.md` (g_completion_8) + `../hw/<target>/` (HW realization).

---

## §1 GOAL

**Mission**: anima 의 자연발화 + 영속성 메커니즘을 외부 HW (또는 SW
보조엔진) 로 offload 하여 (a) 전력 효율 (Akida 1mW vs CPU 10W) (b) 진정한
물리적 비결정성 (TRNG/quantum) (c) 영속 메모리 (memristor/RTC) 확보.

**Non-goal**: 모델 학습 자체 (anima Tier ckpt training 별도 GOAL.md).
본 AUX 는 substrate 의 *물리 실현* 만 다룸.

## §2 보조엔진 dual-role matrix (HW × SW substrate)

상위 5 dual-role substrate (§188 16/16 score, HEXAD/PHYSICS/README.md §6.9 ref)
× 5 HW target (HW_SILICON_PATH.md §2):

| SW substrate | dual-role | 권장 HW target | meta-domain doc |
|---|---|---|---|
| `fpga/strange_loop` (Hofstadter mutual recursion) | 16/16 | Lattice iCE40UP5K FPGA | `FPGA+AUX.md` (TBD) |
| `fpga/nested_lattice` (3-level meta-feedback) | 16/16 | Lattice ECP5-EVN FPGA | `FPGA+AUX.md` (TBD) |
| `social/kuramoto_coupling` (Kuramoto phase sync) | 16/16 | **BrainChip Akida** / Intel Loihi 2 | **[/SUB_ENGINES/AKIDA/](../../SUB_ENGINES/AKIDA/)** ☑ · `LOIHI+AUX.md` (TBD) |
| `oscillator/sleep_oscillator` (SWS↔REM phase switch) | 16/16 | Arduino + AD9833 DDS | `DDS+AUX.md` (TBD) |
| `HEXAD/CHAT/spontaneous_smoke` (motivation gate) | 16/16 | Toshiba SBM / Fujitsu DA Ising / ECP5 | `ISING+AUX.md` (TBD) |

Sub-tier 8 score:
| `proprioception/feedback_loop` (3-DOF spring-damper) | 8 | Arduino/ESP32 sensor loop | `MCU+AUX.md` (TBD) |
| `memristor/self_reference` (history-dep G) | 8 | TiO2 memristor crossbar / **Akida on-chip learn** | `MEMRISTOR+AUX.md` (TBD) · [/SUB_ENGINES/AKIDA/](../../SUB_ENGINES/AKIDA/) ☑ |
| `thermodynamic/entropy_dissolution` (Langevin) | 8 | TRNG (Intel RDRAND) / Bell test source | `TRNG+AUX.md` (TBD) |

## §3 HW target × cost ladder (general)

`HEXAD/PHYSICS/HW_SILICON_PATH.md §3` aggregated:

| Tier | HW | Cost | Wall | Substrate coverage |
|---|---|---|---|---|
| **Phase 0** (Mac local) | iverilog + yosys + scikit-fem + Python | $0 | done | FPGA × 2 sim + Arduino DDS sim + Ising sim + Akida adapter syntax |
| **Phase 1a** (Mac local AOT) | hexa AOT binary + iverilog wave + yosys synth | $0 | done | 5/5 HW target sim + synth (commit `96c049344`) |
| **Phase 1b** (Mac local bitstream + flash binary) | icestorm + nextpnr + arduino-cli + pool ubu-1 ECP5 | $0 | done | 4/4 bitstream (iCE40 132KB + Arduino 14KB + 2× ECP5 1.93MB, commit `b2b26075d`) |
| **Phase 1c** (HW assembly) | UPduino dev board + Arduino Uno + ECP5-EVN + thermal | $225+$5 (Option B fin) | wait | 5/5 target physical board flash + scope/UART verify |
| **Phase 2** (cloud trial) | **BrainChip Akida Cloud** + Loihi 2 NRC + Toshiba SBM + Fujitsu DA | $1-62 | 1주-1개월 wait | neuromorphic + Ising path |
| **Phase 2.5** (real HW) | **Raspberry Pi 5 + AKD1000 Dev Kit** ($1495) | $1495 | 도착예정 | **[AKIDA pack](../../SUB_ENGINES/AKIDA/) ☑** (Day 1-7 boot plan + 50/50 mock PASS) |
| **Phase 3** (research) | Intel Loihi 2 Hala Point + IBM Q free + 추가 dev board | $50K research lic | 1+개월 | full neuromorphic + quantum |

## §4 dual-role priority (자연발화 + 영속성 모두 강한 후보)

본 모듈 최강 dual-role 보조엔진 (immediate fire 가능 도착 우선):

1. **AKD1000 + memristor self-ref hybrid** ([AKIDA pack](../../SUB_ENGINES/AKIDA/) §3.2)
   - 자연발화 = Akida spike threshold (1mW event-driven)
   - 영속성 = Akida on-chip Hebbian 1-shot learn (weights persist in chip)
   - HW: **Pi 5 + AKD1000 Dev Kit 도착예정**

2. **iCE40UP5K strange_loop bitstream** (`hw/strange_loop_ice40/`)
   - 자연발화 = mutual-recursion LUT auto-fire (every clock)
   - 영속성 = 24-FF state + history ring
   - HW: UPduino v3 board $70 BOM 주문 대기

3. **ECP5 nested_lattice bitstream** (`hw/nested_lattice_ecp5/`)
   - 자연발화 = 3-level meta-feedback L3→L2→L1 cycle
   - 영속성 = 14-int flat struct FF
   - HW: ECP5-EVN $120 BOM

4. **Arduino + AD9833 sleep_oscillator** (`hw/sleep_oscillator_arduino/`)
   - 자연발화 = DDS phase accumulator (continuous)
   - 영속성 = RTC TCXO + EEPROM
   - HW: Uno+AD9833 $33 BOM

5. **Toshiba SBM / Fujitsu DA spontaneous_ising** (`hw/spontaneous_ising/`)
   - 자연발화 = Ising annealing emission
   - 영속성 = cloud-saved energy log
   - HW: cloud trial $1-30

## §5 per-HW doc index (anima-physics/AUX/)

| File | Status | HW | LANDED phase |
|---|---|---|---|
| ☑ [AKIDA pack](../../SUB_ENGINES/AKIDA/) (`/SUB_ENGINES/AKIDA/`) | **priority #1** + pack LANDED | BrainChip AKD1000 + Pi 5 16GB | 11 adapter + runtime + 7 boot script + 4 doc + 1525 doc LoC, F-AKIDA-* 50/50 PASS Mac mock validation |
| ☑ [`FPGA.md`](FPGA.md) | LANDED | Lattice iCE40UP5K + ECP5-EVN | iverilog sim + yosys synth + 2 bitstream (iCE40 132 KB + ECP5 1.93 MB × 2) |
| ☑ [`DDS.md`](DDS.md) | LANDED | Arduino Uno + AD9833 | .ino sketch + AD9833 driver + arduino-cli .hex 14 KB |
| ☑ [`ISING.md`](ISING.md) | LANDED (FSM fallback) | Toshiba SBM / Fujitsu DA / ECP5 | iverilog FSM + yosys synth + ECP5 bitstream 1.93 MB |
| ☑ [`LOIHI.md`](LOIHI.md) | adapter | Intel Loihi 2 Hala Point | NxSDK adapter skeleton (cloud-only, NRC research access wait) |
| ☐ (TBD) | — | ESP32 / TiO2 memristor / TRNG | future cycles |

## §6 cross-link

- `PLAN.md` — anima-physics g_completion_8 (G6 HW silicon Phase 1 ☑)
- `README.md §0` — SW 공용 vs HW 전용 분할 원칙
- `HEXAD/PHYSICS/HW_SILICON_PATH.md` — 5 dual-role substrate × HW target + BOM
- `HEXAD/PHYSICS/README.md §6.9` — top 5 dual-role mapping (evidence-based)
- `docs/demiurge_hw_verify_2026_05_21.md` — demiurge 15 도메인 verify state
- `hw/PHASE_1B_STATUS.md` — Phase 1b 4/4 bitstream LANDED
- `hw/PHASE_2_CLOUD_TRIAL.md` — Akida + Loihi 2 + Toshiba/Fujitsu 신청 가이드

## §7 honest C3

1. **본 AUX 는 후보 list + roadmap 만** — 실 HW fire 는 각 meta-domain doc 의 Day-by-day plan 참고.
2. **dual-role score 16/16 은 §188 sim 기반** — 실 HW silicon 에서 동일 점수 보장 0 (B-EMERGE-7 carry).
3. **cost ladder 추정** — 실 BOM 주문 시 ±30% 변동 (BOM 갱신 시점 정보).
4. **Akida Cloud trial vs Pi 5 + AKD1000 Dev Kit** = 별도 path. 전자 = $1/day pre-arrival, 후자 = $1495 도착예정 (사용자 결정).
5. **meta-domain doc 5건 LANDED** (AKIDA pack 분리 + FPGA/DDS/ISING/LOIHI doc) — 나머지 후보 (MCU/MEMRISTOR/TRNG/PHOTONIC) 별도 cycle.

---

## ## Log

### 2026-05-21
- **AUX/ 도메인 신설** — anima-physics 보조엔진 root SSOT.
- AKD1000 + Pi 5 Dev Kit ($1495) 도착예정 → priority #1
- **AKIDA pack → `/SUB_ENGINES/AKIDA/` 루트 분리** (사용자 directive). 11 adapter + runtime + boot/INSTALL.sh + 4 doc + mocks/falsifiers + tests, Mac mock F-AKIDA-* 50/50 PASS. anima-physics/AUX/ = index + FPGA/DDS/ISING/LOIHI doc 유지.
- HW silicon Phase 1b 4/4 LANDED 후속 — Phase 1c HW assembly 대기 (UPduino/Arduino/ECP5-EVN BOM 주문 사용자 gate)
