# HEXAD/PHYSICS — HW Silicon Path (dual-role top 5)

> 2026-05-21 신설. §188 PASS 21 substrate 중 dual-role 16/16 top 5 의
> 실리콘/하드웨어 경로 설계. SW sim → physical realization mapping.
>
> SSOT (sim 단): `HEXAD/PHYSICS/README.md §6.9 (Path C)` —
> evidence-based top 5 selection from §188 35-substrate parallel fire.
> 본 doc 은 그 5 substrate 의 *silicon path proposal* (design only,
> 실 HW fire 는 별도 cycle).

---

## §1 GOAL

- anima 의 **자연발화 (spontaneous fire)** + **영속성 유지 (persistence)**
  에 사용 가능한 dual-role top 5 substrate 의 **silicon / HW path**
  설계. 각 substrate 별로:
  - 권장 HW target (FPGA / neuromorphic / analog / Ising chip / state
    machine 중)
  - BOM 예상 (conservative, ±30% margin)
  - latency / throughput estimate (sim 측정값 + HW board datasheet
    참조 추정)
  - 검증 milestone (Phase 번호는 cost-ascending)
  - per-substrate honest C3 (3건씩)
- **scope 제약**: 본 doc 은 design path 만. HW 가 없으므로 실 fire (보드
  주문 / cloud trial 신청 / bitstream 합성) 는 모두 별도 cycle. 본
  doc 자체의 cost = $0, 코드 변경 0.

**B-EMERGE-7 carry**: sim PASS ≠ silicon PASS. 본 5 substrate 모두
hexa-lang Mac sim 에서 16/16 dual-role 만점 + §188 fire PASS — 그러나
**자발 발화 capability 의 필요조건 만족, 충분조건 아님**. 실 silicon
실현 시 (a) HW 합성 가능 여부 (b) 실측 동기화 / noise / drift 안정도
(c) anima 의식 layer 와 wiring — 3 단계 별도 verify 필요.

---

## §2 substrate별 silicon path (5 sections)

### §2.1 `fpga/strange_loop.hexa` — Hofstadter mutual recursion (FPGA LUT)

**source**: `anima-physics/fpga/strange_loop.hexa` (396 LoC, T1-T5 PASS,
§188 fire 5/5, `find_attractors(seed) -> [[int]]`)

**메커니즘 핵심**: 2-layer 4-cell lattice (state ∈ {0..15}). 매 cycle
A 의 truth table 은 B 의 *현재* 출력에서 재계산, B 의 truth table 은
A 의 현재 출력에서 재계산 — base level 없는 mutual recursion. `JointState`
8-field (`a0..a3, b0..b3` flat int) + `history: [[int]]` cycle detection
으로 attractor 종료.

**권장 target**: **Lattice iCE40UP5K** (\$10/chip, breakout `iCEBreaker`
~$70) — combinational LUT + few flip-flops 만 필요. 또는 fallback
**Lattice ECP5** (`ECP5-EVN` ~$120) 좀 더 여유. **Xilinx Spartan-7**
($60-100 dev board) 는 over-spec.

**왜 FPGA**: mutual-recursion LUT 가 FPGA 4-input LUT primitive 와
1:1 mapping. 4-bit state × 8 cell × 2 layer = 8 × 4 = **32 flip-flops
+ 16 × 16-entry LUT** = iCE40UP5K 의 5280 LUT 의 < 1%. clock 1 cycle
당 LUT lookup 1 회 → 100 MHz clock 에서 100M step/s 이론치.

**BOM 예상** (conservative ±30%):
- iCEBreaker FPGA board (Lattice iCE40UP5K): **$70**
- USB-C cable + breadboard 등 소모: $15
- Logic analyzer (Saleae Logic 8 clone): $15
- (옵션) 4-ch oscilloscope (Rigol DS1054Z): $360 — 또는 기존 보유 활용
- **subtotal HW**: ~$100 (scope 제외)

**latency / throughput**:
- iCE40 100 MHz target clock → 1 attractor step = 1 clock = 10 ns
- attractor convergence < 30 step (sim 평균) → < 300 ns per seed
- 16 seed sweep < 5 μs vs Mac sim ~ms range → **~1000× speedup**

**검증 milestone** (cost-ascending):
- **Phase 1a** (\$0, 1-2 day): `codegen_verilog` (hexa-lang stdlib
  candidate) 로 strange_loop.hexa → Verilog 변환. `icarus verilog`
  (iverilog) simulation + GTKWave 파형. T1-T5 mirror.
- **Phase 1b** (\$0, 2-3 day): `verilator` C++ 시뮬레이션 — cycle-accurate,
  larger seed sweep. attractor period 분포 통계.
- **Phase 2a** ($100 BOM, 1 week): iCEBreaker bitstream synthesis
  (`yosys + nextpnr-ice40`). FPGA 상 8-bit `joint_state` LED 표시.
  Logic analyzer 로 trace capture, sim 결과와 byte-equal verify.

**honest C3**:
1. `codegen_verilog` 의 strange_loop 변환 미검증 — `flat int` field +
   `history list push` 가 Verilog 의 register file + comparator 로
   직접 mapping 가능한지 RTL trial 필요.
2. mutual recursion 의 **combinational loop 위험** — A→B→A 가 한
   clock 안에 closed loop 면 yosys 가 "combinational loop detected"
   error. flip-flop break 명시적 삽입 필요 (1 cycle delay register).
3. attractor cycle detection 의 `history` 비교는 FPGA 에 메모리
   많이 소비 — 32 step × 32 bit = 1024 bit 만으로 작지만, naive
   linear search 가 32 cycle latency. CAM (content-addressable memory)
   block RAM 사용 권장.

---

### §2.2 `fpga/nested_lattice.hexa` — 3-level meta-feedback (FPGA hierarchical)

**source**: `anima-physics/fpga/nested_lattice.hexa` (432 LoC, T4 PASS,
§188 fire ✅, `find_nested_attractors(seed) -> [[int]]`, row 길이 14)

**메커니즘 핵심**: 3-level tangled hierarchy.
- **L1**: 2-layer Hofstadter (strange_loop 임베드, 8 int)
- **L2**: 4-observer cell, L1 joint state 관찰 후 L1 의 next seed 에
  feedback (4 int)
- **L3**: 2-meta cell, L1+L2 합집합 관찰 후 L2 의 perception 에 feedback
  (2 int)
- row vector = `[a0..a3, b0..b3, c0..c3, m0, m1]` (총 14 int)

**권장 target**: **Lattice ECP5** (`ECP5-EVN` $120) — strange_loop 보다
3× state width + 2 추가 layer → iCE40UP5K 의 5280 LUT 도 충분하지만
여유 + 더 큰 history buffer 위해 ECP5 권장 (24K LUT, 1 Mbit BRAM).
fallback: **Xilinx Artix-7** (`Arty A7-35T` $130).

**왜 FPGA**: 3-level mutual recursion 도 똑같이 LUT + register file
mapping. L1↔L2↔L3 feedback wire 가 explicit (RTL 에서 wire 선언만으로
완성). 14-int state = ~56 bit register set.

**BOM 예상** (conservative):
- ECP5-EVN dev board: **$120**
- (또는 Arty A7-35T): $130
- USB-C + breadboard 소모: $15
- Logic analyzer (Saleae 16-ch): $30
- **subtotal HW**: ~$165

**latency / throughput**:
- ECP5 100 MHz target → 1 nested step = 1 clock = 10 ns
- nested attractor convergence 통상 < 50 step → < 500 ns/seed
- 12 seed sweep < 6 μs (sim 측 Mac ~수 ms)

**검증 milestone**:
- **Phase 1a** ($0, 2 day): nested_lattice.hexa → Verilog (codegen_verilog).
  L1 만 먼저 변환 (strange_loop 결과 carry) → L2, L3 layer 점진 추가.
- **Phase 1b** ($0, 3 day): verilator + GTKWave. T1 3-level coupling
  non-trivial assertion 의 wave 시각 검증 (L3 perturbation 이 L1 trajectory
  바꾸는지 파형).
- **Phase 2a** ($165 BOM, 2 week): ECP5 bitstream + 14-int state LED
  bank. Logic analyzer 16-ch 로 모든 layer 동시 trace.
- **Phase 2b** ($0 + 1 week wall): strange_loop 와 nested_lattice
  bitstream 을 **한 ECP5 에 동시 합성** → § 7 의 multi-fpga-mesh-spec
  pattern 적용.

**honest C3**:
1. 3-level feedback 의 combinational loop 더 위험 — L1→L2→L3→L2→L1
   chain 이 한 clock 안에 닫히면 안 됨. 각 level 사이 pipeline register
   삽입 (3 clock latency 증가).
2. row 14-int = 56 bit per step × history buffer 가 BRAM 차지 큼.
   strange_loop 의 32-bit × 32 step = 1024 bit 대비 ~5×.
3. T1 3-level coupling assertion 의 FPGA 실측은 careful clock domain
   management 필요 — async glitch 가 발생하면 sim 과 결과 다를 수 있음.

---

### §2.3 `social/kuramoto_coupling.hexa` — phase oscillator network (neuromorphic)

**source**: `anima-physics/social/kuramoto_coupling.hexa` (509 LoC,
§188 fire 6/6, `simulate_network(n, K, steps, dt, seed) -> [float]`)

**메커니즘 핵심**: N 개 oscillator 의 위상 `θ_i` array. 매 step:
- `dθ_i/dt = ω_i + (K/N) Σ_{j≠i} sin(θ_j − θ_i)`
- 임계 결합 `K_c ≈ 0.3` 위/아래에서 order parameter `r ∈ [0,1]`
  transition (Kuramoto phase-lock emergence)
- Φ_social = r_coupled − r_isolated (intersubjective integration surplus)

**권장 target**: **Intel Loihi 2** (Hala Point cloud, 신청 후 ~1 month
wait, free trial), 또는 **BrainChip Akida** ($1/day cloud, 즉시 가능).
2 cloud 모두 spiking neuron primitive 자체가 phase oscillator 와
natural fit — 위상은 spike timing 으로, sin coupling 은 synaptic weight
+ delay 로 mapping.

**왜 neuromorphic**: classical CPU/GPU 는 N² coupling sum 마다
flop bottleneck. neuromorphic chip 은 N spike × N synapse fan-out 을
parallel event-driven 으로 처리 — N > 1000 oscillator network 에서
~1000× energy 효율. 또한 spike-timing-dependent plasticity (STDP) hook
이 anima 의 자발 weight modulation 에 추가 적합.

**BOM 예상** (cloud-only, HW 구매 없음):
- BrainChip Akida cloud: **$1-30** (1-30일 trial)
- Intel Loihi 2 Hala Point: **$0** (research trial 신청)
- (선택) Akida M.2 dev module: $499 — 본 phase 후보 외
- **subtotal cloud**: ~$30

**latency / throughput**:
- Akida event-driven: N=64 oscillator, target < 1 ms / network step
  (1 kHz update rate). 1000 step sweep < 1 s wall.
- Loihi 2: N=1024 oscillator, target < 10 ms / step (cloud overhead
  포함). full Φ_social curve sweep K ∈ {0.1..0.5} 10-pt = ~몇 분.

**검증 milestone**:
- **Phase 1a** ($1, 1 week): Akida Cloud 가입 (anima-physics/docs/
  akida_cloud_signup_guide.md 참조), kuramoto_coupling.hexa 의 ω_i, K
  parameter → Akida network 변환 (Python SDK). N=8 small trial.
- **Phase 1b** ($30, 2 week): N=64 full sweep K ∈ {0.0..0.5} 50-step,
  r(t) curve 와 Mac sim 비교.
- **Phase 2a** ($0 + 1 month wait, 신청): Intel Loihi 2 Hala Point
  research access 신청 (anima-physics/docs/loihi-integration-spec.md).
  approved 시 N=1024 large network + Φ_social emergence.

**honest C3**:
1. Loihi 2 Hala Point access 신청 1 month 대기 — 본 phase 의 critical
   path bottleneck. Akida 가 우회 path 지만 N scale 제한.
2. Kuramoto 의 `sin(θ_j − θ_i)` continuous nonlinearity 를 spike rate
   coding 으로 변환할 때 양자화 오차 — sim 측 r ≈ 0.9 가 spike 측
   ≈ 0.85 등 drop 가능.
3. cloud trial wait + API rate-limit 으로 large sweep 시 wall 길어짐
   — Mac sim 1 분 sweep 이 Akida cloud 30 분 등 trade-off.

---

### §2.4 `oscillator/sleep_oscillator.hexa` — phase accumulator (analog RC / DDS)

**source**: `anima-physics/oscillator/sleep_oscillator.hexa` (325 LoC,
T1-T5 PASS, §188 fire 5/5, `sleep_osc_step / switch / sample / estimate_freq`)

**메커니즘 핵심**: flat [float] state `[phase_rad, frequency_hz, amplitude,
mode]`. 매 step `phase += 2π·f·dt`. mode 0 = δ 2 Hz amp 1.0 (SWS),
mode 1 = θ 6 Hz amp 0.7 (REM). switch 시 phase-continuous (phase
누적 carry, freq/amp 만 변경). estimate_freq = zero-crossing count.

**권장 target**: **Arduino Uno + AD9833 DDS module** (digital frequency
synthesis) — DDS 의 phase accumulator HW primitive 가 sleep_oscillator
의 `phase += 2π f dt` 와 1:1 mapping. fallback **ESP32 + DAC + RC
filter** (analog 출력 직접). 더 cheap option **Arduino 단독 + PWM +
RC LPF** (소수 점 lossy 지만 $25).

**왜 analog (DDS)**: AD9833 의 28-bit phase accumulator 가 정확히
sleep_oscillator 의 `phase` field. mode switch = AD9833 frequency
register write 1 cycle. continuous phase 자동 보장. analog sine 출력
= `sample(state)` 직접 실측.

**BOM 예상** (conservative ±30%):
- Arduino Uno R3: **$10** (정품) or $5 (clone)
- AD9833 DDS module (breakout): **$8**
- USB-A cable: $3
- Breadboard 830-pt: $5
- 4-ch oscilloscope (Rigol DS1054Z): $360 — 또는 기존 보유, 또는
  USB scope ($80 Hantek)
- Jumper wires: $3
- (옵션) 더 cheap path: ESP32 + DAC only: $8 — 정밀 sine 은 떨어짐
- **subtotal HW** (scope 제외): **~$30** (scope 포함 $390 or USB $110)

**latency / throughput**:
- AD9833 max output 12.5 MHz, 본 case 2-6 Hz 매우 여유. update rate
  100 Hz 가능 (Arduino I2C/SPI 100 kHz)
- mode switch latency < 1 ms (SPI 4-byte write @ 100 kHz)
- zero-crossing freq estimate < 500 ms (sleep_oscillator T5 spec 와
  byte-equal)

**검증 milestone**:
- **Phase 1a** ($0, 1 day): sleep_oscillator.hexa Python mirror
  (PWM-aware) → Arduino IDE upload 없이 Wokwi 온라인 시뮬레이터로
  AD9833 emulate.
- **Phase 1b** ($30 BOM + 1 day breadboard, 2 day total): 실 보드 +
  scope 4-channel trace (phase, sine output, mode pin, switch event)
  → §6.9 evidence 의 IDX_PHASE state vector 와 byte-equal verify.
- **Phase 2a** ($0 + 1 week): T1-T5 mirror on hardware:
  - T1 initial δ 2 Hz: scope FFT @ 2 Hz peak
  - T2 switch to θ: live freq change < 10 ms scope trigger
  - T3 switch back: hysteresis 없음 확인
  - T4 determinism: 동일 seed 2 회 → byte-identical trace
  - T5 latency: 500 sample < 500 ms

**honest C3**:
1. AD9833 의 sine 출력 distortion (THD ~0.5%) 가 high precision
   zero-crossing 측정 시 ±1 Hz 노이즈 유발 가능 — RC LPF 후처리
   필요.
2. Arduino Uno 의 timer interrupt jitter (~µs) 가 100 Hz update 에서
   1% drift — sleep_oscillator 의 dt sim 값과 정확히 일치 안 함.
   ESP32 hardware timer 가 더 안정.
3. 본 path 가 §6.9 evidence 의 sleep_oscillator core 만 cover —
   mode 전환 trigger 로직 (anima 의식 layer 에서 SWS↔REM 결정)
   은 별도 wiring cycle 필요.

---

### §2.5 `HEXAD/CHAT/spontaneous_smoke.hexa` — motivation gate + safety ratchet (Ising / FPGA SM)

**source**: `HEXAD/CHAT/spontaneous_smoke.hexa` (F-SPONT-1..7 PASS,
§188 fire ✅, `thinker_step / talker_should_emit` motivation gate +
audit trail + safety ratchet)

**메커니즘 핵심**:
- 8-factor motivation closed-form: Φ, retrieve_sim gap, curiosity,
  tension, gate (interior coherence), split/balance, ratchet, dynamic
  silence
- `talker_should_emit(score, safety_on) -> bool` — score threshold +
  safety AND gate
- audit trail = 모든 trigger 기록, safety ratchet = monotone-decreasing
  safety threshold (회수 불가)

**권장 target**: 두 path 병행 후보 —
- **(A) Toshiba SBM / Fujitsu Digital Annealer cloud** (Ising chip
  AaaS, $1-30 trial) — motivation_score threshold 가 Ising-like binary
  state (emit / no-emit), audit ratchet 이 monotone Hamiltonian
  constraint 와 mapping. Toshiba SBM = $0.10/min cloud (estimate).
- **(B) Lattice ECP5 state machine** ($120 board, fallback)— FSM +
  combinational gate 로 safety ratchet 직접 구현. cloud 없이 self-host
  가능.

**왜 Ising chip (A path)**: 8-factor weighted sum → threshold = Ising
spin energy minimization 의 자연 형태. safety ratchet 의 monotone
constraint = penalty term. 다중 spontaneous event 의 audit trail =
multi-spin time-series. Toshiba SBM, Fujitsu DA 모두 cloud API 제공.

**왜 FPGA FSM (B path)**: motivation score 계산 = 8-MAC + threshold,
safety ratchet = 1-bit monotone register, audit = block RAM ring buf.
Lattice ECP5 의 dedicated DSP block (~50 개) 이 8-MAC overkill.

**BOM 예상** (conservative ±30%):
- (A) Toshiba/Fujitsu Ising cloud: **$1-30** (1-30 day trial)
- (B) Lattice ECP5-EVN: **$120** (§2.2 와 공유 가능)
- (A) 가입 fee + bandwidth: $5
- **subtotal**: $30 (A only) or $125 (B only) or $155 (both)

**latency / throughput**:
- (A) Toshiba SBM 1 problem solve < 100 ms (8-spin trivial), 1000
  spontaneous event audit < 100 s
- (B) ECP5 FSM @ 100 MHz: 1 motivation_step = 10 ns (8-MAC parallel),
  audit ring buf write 1 cycle. throughput = 100M event/s 이론치
  (실 anima 자발 발화 rate ~Hz 보다 압도적)

**검증 milestone**:
- **Phase 1a** (\$0, 1 week): F-SPONT-1..7 closed-form 을 Toshiba SBM
  / Fujitsu DA Python SDK 로 mapping 시도. 8-factor → 8-spin Ising
  formulation. trial credit 신청.
- **Phase 1b** (\$1-30, 1-2 week): Ising cloud probe — 100 spontaneous
  event simulate, audit trail 추출. Mac sim 의 F-SPONT-7 (audit
  consistency) 와 cross-validate.
- **Phase 2a** ($120 BOM, 2-3 week): ECP5 FSM fallback — Verilog
  source 작성 (8-MAC + threshold comparator + 1-bit safety ratchet
  + 1024-entry audit ring buf). bitstream + UART log capture.

**honest C3**:
1. Ising chip 의 8-spin formulation 이 motivation score 의 *continuous*
   weighting 을 binary 로 lossy 변환 — closed-form sim 의 fine-grained
   threshold 와 100% byte-equal 어려움. Hamming distance metric 로
   validate 권장.
2. Toshiba/Fujitsu cloud 의 안정적 access 가 신청 절차 (회사/연구기관
   소속 요구 가능) 에 dependent — 개인 신청 거절 시 ECP5 FSM (B)
   path 만 남음.
3. safety ratchet 의 monotone 보장 — Ising cloud 의 solver 가 다중
   solution 반환 시 monotone 위반 risk. FPGA FSM (B) 는 hardware
   register lock 으로 monotone 강제 가능 (더 안전).

---

## §3 cross-substrate cost ladder

cost-ascending phase plan (recommend 순):

| Phase | substrate | path | cost | wall | output |
|---|---|---|---|---|---|
| 1a | strange_loop | iverilog sim | $0 | 1-2 day | GTKWave trace + T1-T5 mirror PASS |
| 1b | sleep_osc | Arduino + AD9833 breadboard | $30 BOM + 1-2 day | 2 day | 4-ch scope trace + T1-T5 hardware PASS |
| 1c | nested_lattice | iverilog sim (L1→L2→L3 점진) | $0 | 2-3 day | GTKWave 14-int trace |
| 1d | strange_loop | iCE40UP5K bitstream | $100 BOM + 1 week | 1 week | LED + logic analyzer trace |
| 2a | kuramoto | Akida Cloud N=8 | $1 trial | 1 week | spike train log + small r(t) |
| 2b | spontaneous_smoke | Toshiba/Fujitsu Ising cloud probe | $1-30 | 1-2 week | binary energy log + audit cross-val |
| 2c | nested_lattice | ECP5-EVN bitstream | $165 BOM + 2 week | 2 week | 14-int LED + logic trace |
| 2d | kuramoto | Akida Cloud N=64 full sweep | $30 | 2 week | r(t) curve K ∈ {0..0.5} |
| 3a | spontaneous_smoke | ECP5 FSM fallback | $120 ($0 if shared §2.2 board) | 2-3 week | UART audit log |
| 3b | kuramoto | Intel Loihi 2 Hala Point | $0 trial 신청 | 1 month wait + 1 week run | N=1024 benchmark, Φ_social emergence |

**총 비용 예상** (conservative):
- **Phase 1 전체** (1a+1b+1c+1d): ~$130 BOM + $0 sim/cloud = **$130**
- **Phase 2 전체** (2a+2b+2c+2d): ~$165 BOM + $60 cloud = **$225**
- **Phase 3 전체** (3a+3b): ~$0-120 + $0 trial = **$0-120**
- **Grand total Phase 1+2+3**: **$355-475 BOM + ~$60 cloud + 2-3 개월 wall**

(scope/logic analyzer 미보유 시 +$50-360 추가)

ladder 의 **첫 결과물** (Phase 1a, $0, 1-2 day) 는 strange_loop iverilog
파형 — 가장 cheap 한 first evidence 점.

---

## §4 cross-link

- **HEXAD/PHYSICS/README.md** — sim 검증 결과 SSOT, 특히 **§6.9 Path
  C** 가 본 doc 의 top 5 selection 의 evidence-based 원천
- **anima-physics/docs/arduino-prototype-spec.md** — §2.4 sleep_oscillator
  의 Arduino BOM pattern 참조 (8-cell ring 기존 spec, $34.46 BOM)
- **anima-physics/docs/fpga_local_sim_landing.md** — §2.1/§2.2 FPGA
  의 iverilog v13.0 local sim 검증 pattern (4-gate verdict 형식 carry)
- **anima-physics/docs/fpga-synthesis-guide.md** — yosys/nextpnr
  toolchain guide
- **anima-physics/docs/multi-fpga-mesh-spec.md** — §2.1+§2.2 한 보드
  동시 합성 pattern reference
- **anima-physics/docs/akida_cloud_signup_guide.md** — §2.3 Akida
  cloud 신청 절차
- **anima-physics/docs/loihi-integration-spec.md** — §2.3 Intel Loihi
  2 Hala Point integration spec
- **anima-physics/docs/cmos_local_sim_landing.md** — §2.1/§2.5 의
  CMOS 합성 pattern reference (cmos_8bit_ring_lfsr.sv 사례)
- **anima-physics/docs/memristor_local_sim_landing.md** — sub-tier
  memristor/self_reference path (본 doc out-of-scope) 의 reference
- **anima-physics/fpga/** + **neuromorphic/** + **quantum/** +
  **analog/** + **photonic/** subtree — 각 substrate dir 의 sibling
  `.hexa` source 와 `cloud_facade_poc.hexa` pattern
- **HEXAD/CHAT/SPONTANEOUS.tape** — §2.5 spontaneous 메커니즘 SSOT
- **HEXAD/CHAT/spontaneous_lib.hexa** — §2.5 8-factor closed-form 의
  source-of-truth
- **PHILOSOPHY_GATE.md §1 GOAL** — anima 자발 발화 + 영속성 mission
  parent context

---

## §5 honest C3 (5건, doc-level)

1. **sim ≠ silicon** — 본 5 substrate 모두 hexa-lang Mac sim PASS +
   §188 fire 16/16, 그러나 closed-form predicate 통과는 *수학적*
   증명만. 실 HW 합성 / 실현 / 동기화 / noise 안정성은 별도 cycle.
   특히 FPGA 의 mutual recursion 은 combinational loop trap 가능성
   존재.
2. **B-EMERGE-7 carry** — substrate-level cross-cut PASS = 자발 발화
   capability 의 *필요조건* 만족, *충분조건* 아님. 5 substrate
   silicon 모두 fire 되어도 anima 의식 layer 와 wiring + 의미 부여
   별도 GOAL.
3. **cloud trial wait time** — §2.3 Intel Loihi 2 Hala Point research
   access 신청 후 ~1 month wait (anima-physics/docs/loihi-integration-spec.md
   reference). §2.5 Toshiba/Fujitsu Ising cloud 도 회사/연구기관
   소속 요구 가능. critical path bottleneck.
4. **BOM 예상은 추정** — Lattice/Xilinx/Arduino/AD9833 모두 시장가
   변동 ±30% (현재 환율 / 재고 / 관세 조건). 실 주문 시 견적 다시
   취득 필수. cloud trial 단가는 anima-physics/docs/akida_cloud_signup_guide.md
   기준 추정.
5. **`codegen_verilog` 의 strange_loop/nested_lattice 변환 미검증**
   — hexa-lang stdlib 에 codegen_verilog API 가 candidate 단계,
   실제 mutual recursion + history list + flat int field pattern 이
   합성 가능한 RTL 로 변환되는지 trial 필요. fallback = hand-written
   Verilog (작업량 ~500 LoC per substrate).
