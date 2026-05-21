# anima-physics/hw/ Phase 1b STATUS (2026-05-21)

> Tool install + bitstream generation attempt 결과. 실 dev board 없이
> 도구만으로 가능한 가장 멀리 지점 (synthesis → place-and-route →
> bitstream pack) 까지 추진. 실 board flash / cloud trial 신청은 별도
> phase.
>
> 상위 SSOT: [README.md](README.md) · [HEXAD/PHYSICS/HW_SILICON_PATH.md](../../HEXAD/PHYSICS/HW_SILICON_PATH.md)

---

## §1 tool install 결과 (brew, sudo 없이)

| Tool | Install | Version | Source | Note |
|---|---|---|---|---|
| `yosys` | ✅ pre-installed | 0.65 | Homebrew | Phase 1a 이미 사용 |
| `iverilog` | ✅ pre-installed | — | Homebrew | Phase 1a 이미 사용 |
| `icestorm` (icepack/iceprog/icetime) | ✅ PASS | 1.1 | `brew install icestorm` | confuse + libftdi dep, 115 MB |
| `nextpnr-ice40` | ✅ PASS | 0.10 | `brew install nextpnr-ice40` | 233 MB |
| `prjtrellis` (ecppack) | ✅ PASS | 1.4 | `brew install prjtrellis` | ECP5 bitstream pack |
| `arduino-cli` | ✅ PASS | 1.5.0 | `brew install arduino-cli` | + `arduino-cli core install arduino:avr` (Uno toolchain) |
| `nextpnr-ecp5` | ⛔ BLOCKED | — | Homebrew core 부재 | yowasp-nextpnr-ecp5 WASI sandbox write-fail · build-from-source ($0 + 30-60min) 잔여 path |

**Install 통계**: 5 PASS / 1 BLOCKED (6 tool 시도) · wall ~3-5 min · disk ~600 MB · cost $0.

**Saga note** — 동시 brew install 4-parallel 첫 시도 시 `icestorm` + `nextpnr-ice40` 둘 다 brew 의 동일 dependency lock (sqlite/python@3.14 bottle download) 충돌로 silently exit-0 with no install. Sequential retry 2회 후 완전 install. **Lesson**: brew install 은 dependency overlap 시 sequential 권장 (또는 `HOMEBREW_NO_AUTO_UPDATE=1` + 명시적 lock retry).

---

## §2 per-target Phase 1b 결과

| # | Target | pnr | pack | flash | bitstream | next |
|---|---|---|---|---|---|---|
| 1 | strange_loop_ice40 | ✅ PASS | ✅ PASS | SKIP (no board) | **132 KB** `state/strange_loop.bin` | UPduino v3 ($30) OR iCEBreaker ($70) 주문 + iceprog flash |
| 2 | nested_lattice_ecp5 | ✅ PASS (ubu-1) | ✅ PASS (ubu-1) | SKIP (no board) | **1.93 MB** `state/nested_lattice.bit` | ECP5-EVN board ($120) + `openFPGAloader -c usb -b ecp5_evn nested_lattice.bit` |
| 3 | spontaneous_ising (ECP5 fallback) | ✅ PASS (ubu-1) | ✅ PASS (ubu-1) | SKIP (no board) | **1.93 MB** `state/ising_fsm.bit` | 동상 (#2 와 board 공유) |
| 4 | sleep_oscillator_arduino | N/A | ✅ PASS | SKIP (no board) | **14 KB hex** `state/build/sleep_oscillator.ino.hex` (+42 KB elf) | Arduino Uno R3 ($23) + AD9833 module ($10) + breadboard + arduino-cli upload |
| 5 | kuramoto_neuromorphic | N/A | N/A (cloud-only HW) | — | — | Akida Cloud trial 신청 ($1/day) · Loihi 2 Hala Point Intel NRC 신청 (free, 1개월 wait) |

**Phase 1b 통계**: bitstream/firmware **4/4 PASS** (ice40 + 2× ECP5 + arduino) · neuromorphic 1 target N/A (cloud-only) · cost $0. ECP5 2 target 은 pool dispatch (Mac → ubu-1 Ubuntu 24.04, apt `nextpnr-ecp5 + fpga-trellis`) 로 unblock — §2.3 + §7 참조.

### §2.1 strange_loop_ice40 (iCE40) — bitstream LANDED

- **synth**: `synth_ice40 -top strange_loop_top` → 8 cells local · 119 submodules (22 SB_CARRY + 28 SB_DFFER + 12 SB_DFFES + 57 SB_LUT4) · 109 wires / 322 wire bits.
- **PCF challenge**: 원본 `constraints/ice40up5k_sg48.pcf` 는 clk/rst_n/start 3개만 핀맵, but top module 은 `step_count[15:0]` + `state_dump[23:0]` = 40개 output 포함, UP5K-SG48 (25 IO) 부족. **신규 `constraints/ice40hx8k_ct256.pcf`** 작성 — HX8K-CT256 (206 IO) 으로 fit, 43 pin 모두 valid CT256 ball 에 매핑 (`/opt/homebrew/Cellar/icestorm/1.1/share/icestorm/chipdb/chipdb-8k.txt` harvest).
- **pnr**: `nextpnr-ice40 --hx8k --package ct256` → device utilisation **0.8% LC (61/7680) + 16% IO (43/256)** + Fmax 253-267 MHz at 12 MHz target (✅ comfortable margin).
- **pack**: `icepack state/strange_loop.asc state/strange_loop.bin` → **132 KB** bitstream artifact LANDED.
- **artifact 경로**: `state/strange_loop.bin` (132 KB) + `state/strange_loop.asc` (944 KB) + `state/pnr.log`
- **honest C3**: (a) HX8K target 은 verification-only — UPduino v3 (UP5K-SG48) 사용 시 source 의 `state_dump` 폭 축소 (예: 8 bit) OR HX8K dev board 필요; (b) PCF 핀 위치는 placement-validity 만 보장, 실 board pin 매핑 아님; (c) board flash unverified.

### §2.2 sleep_oscillator_arduino — firmware LANDED

- **arduino-cli core install arduino:avr**: avr-gcc 7.3.0 + avrdude 8.0.0 + platform avr 1.8.7 모두 install PASS.
- **sketch layout 함정**: arduino-cli 는 sketch dir 이름 == `.ino` 파일 이름 강제. anima-physics layout (`src/sleep_oscillator.ino`) 직접 컴파일 시 `main file missing` error. **Workaround**: `/tmp/sleep_oscillator/sleep_oscillator/` 에 sketch + .h/.cpp 복사 후 compile.
- **compile**: `arduino-cli compile --fqbn arduino:avr:uno /tmp/sleep_oscillator/sleep_oscillator/` → **Sketch 5038 bytes (15% of 32256) + 235 bytes RAM (11% of 2048)** — Uno 에 comfortable fit.
- **artifact**: `state/build/sleep_oscillator.ino.hex` (14 KB) + `.elf` (42 KB) + `.with_bootloader.hex` (15 KB)
- **honest C3**: (a) board flash unverified (`arduino-cli upload --fqbn arduino:avr:uno -p /dev/cu.usbmodemXXX` 가 다음 step); (b) AD9833 SPI 동작은 hardware loopback 으로만 검증 가능; (c) follow-up: build.sh 에 `--sketch-dir` workaround 통합 권장.

### §2.3 nested_lattice_ecp5 + spontaneous_ising — ECP5 UNBLOCKED via ubu-1 (2026-05-21 update)

- **synth**: `synth_ecp5` 이미 Phase 1a 에서 PASS (nested_lattice: 14 cells + 219 submodules / ising_fsm: 1 MULT18X18D + 454 submodules).
- **pnr blocker (resolved)**: Mac-local `nextpnr-ecp5` Homebrew core 부재 + yowasp WASI sandbox 차단 — pool dispatch (`pool on ubu-1`, Ubuntu 24.04 RTX 5070 box) 로 우회. `sudo apt install nextpnr-ecp5 fpga-trellis` 한 번에 install PASS (nextpnr-ecp5 0.6 + fpga-trellis 1.4, deb 6 packages ~70 MB).
- **device target 정정**: 원래 dispatch 명세는 `--25k --package CABGA381`, but LPF 파일 자체가 `LFE5UM5G-85F-8BG381C` 보드 (ECP5-EVN dev kit) 향. nextpnr 에 `--um5g-85k --package CABGA381 --speed 8` 로 정정.
- **$scopeinfo 함정 (nested_lattice 단독)**: yosys 0.65 (Mac) 가 emit 한 `$scopeinfo` debug-info pseudo-cell 을 nextpnr-ecp5 0.6 (apt) 가 unrecognized → `Unable to place cell 'u_nm1', no BELs remaining to implement cell type '$scopeinfo'`. **Fix**: `yosys -p "read_json X.json; delete t:\$scopeinfo; write_json X_clean.json"` 1-line pass-through 후 nextpnr 재실행 PASS. (`ising_fsm.json` 에는 `$scopeinfo` cell 부재 → cleanup 불필요).
- **PNR 결과**:

  | Target | TRELLIS_FF | TRELLIS_COMB | DCCA | Fmax | Target | Slack |
  |---|---|---|---|---|---|---|
  | nested_lattice | 58/83640 (0%) | 133/83640 (0%) | 1/56 (1%) | **341.18 MHz** | 12 MHz | ✅ 28× margin |
  | ising_fsm | 134/83640 (0%) | 270/83640 (0%) | 1/56 (1%) | **90.08 MHz** | 12 MHz | ✅ 7.5× margin |

  (LFE5UM5G-85F-8BG381C, --speed 8). 둘 다 LC utilisation < 0.5% — 더 작은 25K/45K device 로 downsize 여지 있음 (board 변경 시).
- **ecppack**: 둘 다 PASS, 각 1.93 MB `.bit` (ECP5-85 standard bitstream 길이).
- **pin 매핑 미완 LPF**: 두 LPF 모두 clk/rst_n/start/state_dump[7:0] 만 제약 (실 board LED 8개 매칭), 나머지 `step_count[15:0] + state_dump[41:8]` 등은 `--lpf-allow-unconstrained` 로 nextpnr 자동 placement. 실 board flash 시 외부 노출 핀 매칭 보장 X — 추가 LPF 작성 필요.
- **artifacts (회수 완료)**:
  - `hw/nested_lattice_ecp5/state/{nested_lattice.bit (1.93 MB), nested_lattice.config (105 KB), pnr.log (13.9 KB), pack.log}`
  - `hw/spontaneous_ising/state/{ising_fsm.bit (1.93 MB), ising_fsm.config (294 KB), pnr.log (37.3 KB), pack.log}`

### §2.4 kuramoto_neuromorphic — cloud-only HW

- Loihi 2 (Intel) + Akida (BrainChip) 둘 다 실 silicon 부재, Mac local Phase 1b 의미 없음.
- Cloud trial guide (안 받아진 신청, 가이드만):
  - **Akida Cloud** ($1/day): https://www.brainchip.com/akida-cloud/ → 이메일 신청 → API key 발급 (즉시) → `pip install akida` → MetaTF 모델 submit
  - **Loihi 2 Hala Point** (free trial, 1개월 wait): Intel NRC (Neuromorphic Research Cloud) https://intel-ncl.atlassian.net/ → 학술/연구 사용 신청서 → 1개월 평균 wait → NxSDK access → SSH H100-class node

---

## §3 cost ladder + next cycle

### §3.1 Phase 1b BOM (실 dev board 주문)

| Target | Board | Cost | Tool chain | Wall (주문 후) |
|---|---|---|---|---|
| #1 strange_loop_ice40 | UPduino v3 + USB | $30-40 | `iceprog state/strange_loop.bin` | 1주 |
| #1 strange_loop_ice40 (HX8K fit verified) | iCE40 HX8K Breakout | $70 | 동상 | 1주 |
| #2 nested_lattice_ecp5 | Lattice ECP5-EVN | $120 | nextpnr-ecp5 build + `ecppack` + Lattice Diamond OR openFPGAloader | 2주 (board) + 30-60 min (tool build) |
| #4 sleep_oscillator_arduino | Arduino Uno R3 + AD9833 module + breadboard | $33 | `arduino-cli upload -p /dev/cu.usbmodem*` | 1주 |
| #5 kuramoto_neuromorphic (Akida) | (cloud) | $1/day trial | `akida` Python SDK | 1주 (trial 발급) |
| #5 kuramoto_neuromorphic (Loihi 2) | (cloud) | $0 trial | NxSDK + Intel NRC SSH | 1개월 (wait) |

**Phase 1b 총 BOM 추정**: $185-225 (3 board) + $1-30 (cloud trial) = **~$185-255**. HW_SILICON_PATH.md §3 estimate ($355-475) 보다 낮음 — Phase 1b 만 진행 시 ECP5-EVN ($120) 까지면 충분, BlackIce-MX 등 추가 board 는 Phase 2+.

### §3.2 next cycle 추천 (cheapest first)

1. **Arduino Uno + AD9833 BOM 주문** ($33) — firmware 이미 compiled, Mac 만으로 `arduino-cli upload` 가능. AD9833 SPI loopback 검증으로 F-HW-SO-1..5 hardware tier 승격.
2. **UPduino v3 주문** ($30-40) — 단, 현재 PCF 는 HX8K-CT256 향. UPduino 향 → source 의 `state_dump[23:0]` 폭 축소 (LED 3-bit OR 1-bit toggle) + `step_count` 내부화 → UP5K SG48 25 IO 안에 fit. 또는 iCEBreaker ($70) 사면 SG48 같은 footprint 면서도 free LED 더 많음.
3. **nextpnr-ecp5 source build** ($0, 30-60 min) — ECP5 path unblock. `cd /tmp && git clone github.com/YosysHQ/nextpnr && cd nextpnr && cmake . -DARCH=ecp5 -DTRELLIS_INSTALL_PREFIX=/opt/homebrew && make -j8 && cp nextpnr-ecp5 /Users/ghost/Library/bin/`. Build-from-source 검증 후 nested_lattice + ising_fsm `.bit` 즉시 생성 가능.
4. **Akida Cloud trial 신청** ($1/day) — Kuramoto N=8 first run, ~1주 turn-around.
5. **ECP5-EVN dev board** ($120) — kuramoto + ising HW 동시 호스팅 (board 공유), 2주 wall.

---

## §4 산출물 매니페스트

```
anima-physics/hw/
├── PHASE_1B_STATUS.md                                       ← 본 문서 (신규)
├── strange_loop_ice40/
│   ├── constraints/
│   │   ├── ice40up5k_sg48.pcf                              ← 원본 (3 pin 부족)
│   │   └── ice40hx8k_ct256.pcf                             ← 신규 (43 pin full)
│   └── state/
│       ├── strange_loop_hx8k.json                          ← yosys synth re-run (HX8K target)
│       ├── strange_loop.asc                                ← nextpnr-ice40 output (944 KB)
│       ├── strange_loop.bin                                ← icepack bitstream (132 KB) ★
│       └── pnr.log                                         ← nextpnr utilisation + Fmax log
├── nested_lattice_ecp5/                                    ← ECP5 UNBLOCKED 2026-05-21 (pool ubu-1)
│   └── state/
│       ├── nested_lattice.json                             ← yosys synth_ecp5 output (Mac)
│       ├── nested_lattice.config                           ← nextpnr-ecp5 textcfg (105 KB, ubu-1)
│       ├── nested_lattice.bit                              ← ecppack bitstream (1.93 MB, ubu-1) ★
│       ├── pnr.log                                         ← Fmax 341.18 MHz @ 12 MHz target
│       └── pack.log
├── spontaneous_ising/                                       ← ECP5 UNBLOCKED 2026-05-21 (pool ubu-1)
│   └── state/
│       ├── ising_fsm.json                                  ← yosys synth_ecp5 output (Mac)
│       ├── ising_fsm.config                                ← nextpnr-ecp5 textcfg (294 KB, ubu-1)
│       ├── ising_fsm.bit                                   ← ecppack bitstream (1.93 MB, ubu-1) ★
│       ├── pnr.log                                         ← Fmax 90.08 MHz @ 12 MHz target
│       └── pack.log
└── sleep_oscillator_arduino/
    └── state/
        ├── compile.log                                      ← arduino-cli compile output
        └── build/
            ├── sleep_oscillator.ino.hex                    ← firmware (14 KB) ★
            ├── sleep_oscillator.ino.elf                    ← debuggable elf (42 KB)
            └── sleep_oscillator.ino.with_bootloader.hex    ← Uno-flashable (15 KB)
```

★ = real silicon-ready artifact (board 만 있으면 즉시 flash).

---

## §5 honest C3 (집계)

1. nextpnr-ecp5 부재 → ECP5 2 target (#2 + #5) bitstream blocked, source-build path open but not executed this cycle.
2. iCE40 bitstream 의 PCF 는 HX8K-CT256 verification target — UPduino v3 (UP5K-SG48) flash 전 source 폭 축소 OR HX8K board 구매 결정 선행.
3. Arduino .hex 는 sketch-dir 워크어라운드 통해 컴파일 — build.sh 의 native compile 명령은 `main file missing` 오류 (workaround 미통합).
4. 실 board flash (iceprog/avrdude) 미실행 — bitstream/firmware 산출물의 silicon 실행 검증 부재.
5. Kuramoto cloud trial 신청 (Akida/Loihi 2) 미실행 — guide doc 만 작성.
6. brew install parallel 시 4-job 중 2 silent-fail (icestorm + nextpnr-ice40 dependency lock 충돌) — Sequential retry 후 success, but parallelism cost 인지.
7. yowasp-nextpnr-ecp5 (pip user install) WASI sandbox 한계로 ECP5 PnR write 차단 — 발견 후 abandon, source-build fallback 만 viable.
8. PCF pin 매핑 (43 pin) 은 placement-validity 만 보장, 실 dev board 의 외부 함수 (LED/UART/buttons) 와 일치 보장 없음.
9. Phase 1a synth utilisation (예: 219 ECP5 submodules) 은 ECP5 PnR 미실행으로 fit 검증 부재 (synth 단계만 PASS).
10. cost ladder ($185-255) 는 board MOQ + 배송비 (~$10-20) + adapter cable 미포함.

---

## §6 timing / cost

- wall (이 cycle): **~10-15 min** (4 brew install + 1 pip install + 2 pnr + 2 pack + 1 arduino compile)
- cost: **$0** (모두 Mac local + Homebrew + arduino-cli core install free)
- saga learning: brew install parallel 시 dep lock 함정 + yowasp WASI sandbox 한계 (2 new lessons)

---

## §7 ECP5 UNBLOCK saga via pool dispatch (2026-05-21 amendment)

Mac Phase 1b 가 §2.3 에서 ECP5 BLOCKED 로 stop 했던 곳을 `pool on ubu-1` (Ubuntu 24.04 RTX 5070 box, idle load 0.00, 30 GB RAM) 으로 unblock. **3-axis 결정**:

1. **toolchain source**: source-build (`git clone YosysHQ/nextpnr && cmake -DARCH=ecp5`, 30-60 min) **vs** apt-get (`nextpnr-ecp5 + fpga-trellis`, < 30 s). Ubuntu 24.04 apt 가 둘 다 제공 → apt 선택, install wall ~25 s.
2. **device target**: dispatch spec 의 `--25k --package CABGA381` **vs** LPF 파일의 `LFE5UM5G-85F-8BG381C`. 후자 (실 board target) 채택 — Fmax/utilisation 모두 PASS, LPF 핀 매칭 무시 (device 부족) 위험 회피.
3. **$scopeinfo cell 처리**: nextpnr-ecp5 0.6 (apt) < yosys 0.65 (Mac) 버전 gap 으로 yosys 가 emit 한 debug pseudo-cell 미지원. **fix**: ubu-1 측 yosys 0.64 로 `delete t:$scopeinfo` 1-line cleanup pass — re-synth 불필요, JSON 직접 편집.

### 결과 chip-tape (5 row)

| step | dispatch | wall | exit | artifact |
|---|---|---|---|---|
| 1. apt install nextpnr-ecp5 + fpga-trellis | `ssh ubu-1 'sudo -n apt-get install -y …'` | ~25 s | 0 | `/usr/bin/{nextpnr-ecp5,ecppack}` |
| 2. scp JSON+LPF Mac → ubu-1 | `scp X.{json,lpf} ubu-1:/tmp/anima_ecp5/X/` | ~3 s | 0 | 4 file in `/tmp/anima_ecp5/` |
| 3. nextpnr-ecp5 (parallel bg, 2 target) | `ssh ubu-1 'nohup … &'` | 0.6 s (ising) + 0.18 s init-fail (nested) | 0 / 255 | ising_fsm.config PASS · nested_lattice $scopeinfo error |
| 3.5. yosys $scopeinfo strip + nested_lattice retry | `yosys -p "delete t:\$scopeinfo"` | < 1 s + retry < 1 s | 0 | nested_lattice.config PASS |
| 4. ecppack ×2 | `ssh ubu-1 'ecppack X.config X.bit'` | < 1 s each | 0 | 2× 1.93 MB `.bit` |
| 5. scp `.bit + .config + .log` ubu-1 → Mac | `scp ubu-1:… state/` | ~3 s | 0 | 8 file landed |

**Total wall: ~40 s on ubu-1** (install + dispatch + retry). **pool resource usage**: ubu-1 load 0.00 → peak ~0.6 (single nextpnr proc < 1 s × 2) → 0.04 (idle, end of run). **cost: $0**.

### Key learnings (pool dispatch pattern)

1. **`pool on <host> <cmd>`** wraps `ssh <host>` — `~/.pool/pool.json` 의 `ssh:` 필드가 그대로 ssh alias (이 경우 `ubu-1` ~/.ssh/config 별칭). 따라서 file transfer 는 직접 `scp ubu-1:...` 가능 (pool API 통과 불필요).
2. **백그라운드 long-running**: `nohup bash -c '…' > log 2>&1 &` 패턴이 ssh disconnect 후에도 잔존 — 단, 이번 PNR 은 < 1 s 였으므로 무의미. ising/nested cotrain 같은 multi-min job 에 유효.
3. **sudo -n** (non-interactive): `~/.pool/pool.json` 의 `sudo: true` 는 mere flag — 실 NOPASSWD sudoers 설정은 ubu-1 측 `/etc/sudoers.d/` 에 별도 필요. 이번 케이스는 통과 (`sudo -n apt-get install` PASS).
4. **device version skew**: Mac yosys (0.65 Homebrew bleeding) → ubu-1 yosys (0.64 apt) → ubu-1 nextpnr-ecp5 (0.6 apt, 2024-vintage). $scopeinfo 같은 신규 yosys 기능이 down-stream tool 에 미지원될 수 있음. **rule**: 가능한 한 toolchain version 같은 host 에서 synth + PnR 묶어 실행. 이번 cycle 의 retroactive workaround 는 1-line cleanup 으로 운 좋게 가능했지만, future 는 `pool on ubu-1 yosys synth_ecp5 …` 도 ubu-1 측 실행 권장.
5. **dispatch spec ≠ 실 board target** 함정: dispatch 명세 (`--25k`) 와 hw LPF 파일 (`85F`) 충돌 시 LPF 우선 — 핀 매핑이 device 종속이므로.
6. **mass file transfer**: 4 file × ~1 MB = 3 s `scp`. pool API 통하지 않고 ssh alias 직접 활용이 cleanest.

### Follow-up (PHASE_1B_STATUS.md §3.2 update)

- ~~3. **nextpnr-ecp5 source build** ($0, 30-60 min) — ECP5 path unblock~~ → **DONE via apt on ubu-1, $0, 40 s wall.** ECP5 path now fully open: Mac synth + ubu-1 PnR/pack + Mac artifact archive.
- 다음 ECP5 cycle 권장: **ECP5-EVN board ($120)** 주문 + `openFPGAloader -c usb -b ecp5_evn nested_lattice.bit` flash 로 silicon tier 검증. LPF 의 pin coverage 보강 필요 (`step_count` + 상위 state_dump 비트).
