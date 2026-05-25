# demiurge firmware producer integration — Step 1 (anima 측 bridge LANDED + 첫 record drop)

> anima `demiurge_firmware_bridge.py` 를 demiurge firmware verify producer 로
> wire 하고 첫 end-to-end record 를 demiurge exports/ 에 drop 한 cycle.
> Date: 2026-05-21
> Predecessor: `anima-physics/docs/demiurge_hw_verify_2026_05_21.md §2.1`
> (firmware 행이 ⏳ GATE_OPEN stub-only / record emit only 였던 시점).
> Pattern source: `anima-physics/docs/demiurge_brain_bridge_integration_2026_05_21.md`
> (6-step pattern, brain bridge cycle, 동일 일자).

## §1 GOAL

demiurge `firmware` 도메인의 verify gap (stub-only — QEMU mps2-an385
install-gated skip 만 emit, anima HW #4 sleep_oscillator 의 실 firmware
인용 부재) 를 anima 측에서 producer-skeleton + 첫 record drop 으로 메우는
**Step 1**.

- **Before**: `demiurge cli action verify firmware` →
  `firmware_verify@absent` producer + `qemu-system-arm missing`
  skipped_reason + 자기 boot-smoke 만 emit (anima 의 sleep_oscillator
  Phase 1a/1b LANDED 산출은 미인용).
- **After (this cycle)**: anima 측 producer skeleton + 첫 record dropped
  under `~/core/demiurge/exports/firmware/verify/<UTC>Z/`. 3 backend
  (local_sim · arduino_lint · arduino_compile) 모두 record JSON emit
  검증 PASS. demiurge `FirmwareVerifyProducer.swift` 가 anima record 를
  자동 scan-and-cite 하는 consumer-side cycle 은 별도 (현재 producer 는
  자기 verify.py 산출만 list, foreign-shape record 인용 미구현).
- **Status delta**: firmware row `⏳ GATE_OPEN (stub)` →
  `⏳ GATE_OPEN (stub + anima-bridge)` (record exists, 3-backend audit
  evidence, consumer scan-foreign TODO).

이번 cycle 은 **(a) anima 측 producer skeleton 패턴 4 번째 domain
적용 (brain 에 이어 firmware) + (b) 3-backend audit 첫 사례 + (c)
Phase 1b LANDED `.hex` 14 KB 실 산출의 demiurge namespace 등록**까지.
실 board flash + oscilloscope capture (`scope_capture` backend) 는
Phase 2 별도 cycle.

## §2 integration log (6 step 결과)

### Step 1 — bridge file 신설

```
/Users/ghost/core/anima/anima-physics/hw/sleep_oscillator_arduino/src/demiurge_firmware_bridge.py
(약 280 LoC)
```

- `class DemiurgeFirmwareBridge` dataclass — fields: `backend` /
  `firmware_path` / `flash_size_bytes` / `ram_size_bytes` /
  `falsifier_pass` / `sws_freq_hz` / `rem_freq_hz` /
  `switch_continuity_delta` / `absorbed` / `scope_caveats` /
  `gate_failures`.
- 3 backend 지원: `local_sim` (Python phase accumulator) ·
  `arduino_lint` (brace-balance + LoC) · `arduino_compile`
  (arduino-cli `.ino.hex`).
- `_main()` argparse CLI — `--backend` / `--firmware-path` /
  `--flash-size-bytes` / `--ram-size-bytes` / `--falsifier-pass` /
  `--sws-freq-hz` / `--rem-freq-hz` / `--switch-continuity-delta` /
  `--output`. 기본값은 `state/sim.log` F-HW-SO-1..5 5/5 PASS
  measurement (SWS 2.0002 Hz / REM 6.0006 Hz / δ=0.0 rad) + 
  `state/compile.log` flash 5038 B (15%) / RAM 235 B (11%).
- backend 별 자기 zero-out (lint/sim → flash=ram=0; compile only →
  실수치) g3 over-claim 방지.
- gate_failures 자기 audit (`.hex` 누락 / `.ino` 누락 시 자기 기재).

### Step 2 — bridge 직접 실행 + JSON output (3 backend smoke)

```bash
# (a) local_sim
python3 .../src/demiurge_firmware_bridge.py --backend local_sim \
    --output /tmp/firmware_record_local_sim.json
# (b) arduino_lint
python3 .../src/demiurge_firmware_bridge.py --backend arduino_lint \
    --falsifier-pass "3/3" --output /tmp/firmware_record_lint.json
# (c) arduino_compile (Phase 1b LANDED .hex 14 KB)
python3 .../src/demiurge_firmware_bridge.py --backend arduino_compile \
    --falsifier-pass "1/1" --output /tmp/firmware_record_compile.json
```

- 결과 JSON: 3 backend 모두 `interface=demiurge:firmware:ad9833-dds-record`,
  `producer=anima-sleep-oscillator-ad9833-bridge`, `measurement_gate=
  GATE_OPEN`, `absorbed=false`, `consumer_target=demiurge:firmware:
  VerifyProducer`, `atlas_cite_block` 포함, `gate_failures=[]`
  (모든 path 존재).
- record_id distinct: `sleep_oscillator_ad9833_local_sim` /
  `sleep_oscillator_ad9833_arduino_lint` /
  `sleep_oscillator_ad9833_arduino_compile`.
- **3/3 PASS** (py_compile clean + JSON well-formed + 인용 정확).

### Step 3 — anima record 를 demiurge exports/ 에 drop

```bash
RECORD_DIR=/Users/ghost/core/demiurge/exports/firmware/verify/2026-05-21T08-32-41Z
mkdir -p "$RECORD_DIR"
python3 .../src/demiurge_firmware_bridge.py --backend arduino_compile \
    --output "$RECORD_DIR/anima_sleep_oscillator_20260521T083241Z.json"
```

- 파일: `~/core/demiurge/exports/firmware/verify/2026-05-21T08-32-41Z/
  anima_sleep_oscillator_20260521T083241Z.json` (~1910 B).
- arduino_compile backend 채택 — Phase 1b LANDED `.hex` 14197 bytes
  (flash 5038 / 32256 B = 15%, RAM 235 / 2048 B = 11%) 실 산출 인용.
- **PASS**.

### Step 4 — demiurge re-verify with anima record present

```bash
demiurge cli action verify firmware
```

출력 요지:
- `[firmware+verify] wrote /Users/ghost/core/demiurge/exports/firmware/
  verify/2026-05-21T08-32-48Z/firmware_verify_20260521T083248Z.json`
- `GATE_OPEN / absorbed=false (g3)`
- `📸 new record ID(s): firmware_verify_20260521T083248Z`
- **PARTIAL PASS**: demiurge producer 가 자기 새 record 만 list — 본
  cycle 의 anima record (`anima_sleep_oscillator_*.json`) 는 같은
  `exports/firmware/verify/` namespace 에 존재하지만, 현재
  `FirmwareVerifyProducer.swift` 는 자기가 방금 쓴 `firmware_verify_*`
  prefix 만 scan (`$0.lastPathComponent.hasPrefix("firmware_verify_")`).
  brain bridge cycle 의 자동 인용 패턴과 차이.
- 추가 sanity: `demiurge cli show <path>` → `Decode failed`
  (demiurge 측 schema decoder 가 chip F1F2 shape 만 알고 firmware/
  brain shape 미등록 — brain cycle 과 동일 한계).

### Step 5 — anima docs 갱신

`demiurge_hw_verify_2026_05_21.md` 의 §2.1 firmware row + §3 매핑 행
+ §4 next-cycle 후보 #4 갱신:

| 위치 | Before | After |
|---|---|---|
| §2.1 firmware | ⏳ GATE_OPEN (stub) / record emit only / `firmware_verify_20260521T062442Z` | ⏳ GATE_OPEN (stub + anima-bridge) / 3-backend evidence / `firmware_verify_20260521T062442Z`, `sleep_oscillator_ad9833_arduino_compile` (anima-bridge) |
| §3 sleep_oscillator row | chip ✅ 12/12 · firmware ⏳ stub | chip ✅ 12/12 · firmware ⏳ GATE_OPEN (anima-bridge LANDED 2026-05-21) |
| §4 firmware next | sleep_oscillator DDS firmware demiurge firmware verify 통과 | anima-bridge LANDED 2026-05-21 / consumer scan-foreign + oracle parity (chip f1f2 12/12 pattern) 별도 cycle |

### Step 6 — 본 integration doc 신설

본 파일 (`anima-physics/docs/demiurge_firmware_bridge_integration_2026_05_21.md`)
— brain integration doc 7-section 패턴 답습 (GOAL · integration log
6-step · LANDED + cycle 후보 · honest C3 · key learning · SSOT
pointer).

## §3 anima 측 LANDED, demiurge 측 cycle 후보

### 이번 cycle 에서 anima 측에 LANDED

1. **`anima-physics/hw/sleep_oscillator_arduino/src/demiurge_firmware_bridge.py`** —
   CLI argparse + 3 backend (local_sim / arduino_lint / arduino_compile)
   + 기본값 = `state/sim.log` F-HW-SO-1..5 5/5 PASS + `state/compile.log`
   flash 5038 B / RAM 235 B measured. ~280 LoC.
2. **첫 record drop** —
   `~/core/demiurge/exports/firmware/verify/2026-05-21T08-32-41Z/
   anima_sleep_oscillator_20260521T083241Z.json` (~1910 B). arduino_compile
   backend 채택, Phase 1b LANDED `.hex` 14 KB 실 산출 인용.
3. **doc** —
   `anima-physics/docs/demiurge_firmware_bridge_integration_2026_05_21.md`
   (본 doc) + `demiurge_hw_verify_2026_05_21.md §2.1/§3/§4` 갱신
   (firmware row ⏳ GATE_OPEN (stub) → ⏳ GATE_OPEN (stub + anima-bridge),
   3-backend evidence path 명시).

### demiurge 측 별도 cycle 후보 (consumer)

`FirmwareVerifyProducer.swift` 의 record-discovery 로직 확장 →
`anima_*` / `<producer>_*` 등 foreign-shape record 도 같은
`exports/firmware/verify/` 디렉터리에서 scan-and-cite → schema
decoder 추가 (firmware `interface=demiurge:firmware:ad9833-dds-record`
shape 등록) → `demiurge cli show <firmware-record>` 가 정상 파싱 →
`(.verify, "firmware")` 케이스의 record-listing 부분이 anima record 도
gate 평가에 포함. 이 후속 cycle 의 PR 은 demiurge repo 측에서 별도
dispatch — brain cycle 의 `BrainVerifyProducer.swift` 신설과 동일
패턴 (단, 여기는 producer 가 이미 존재하므로 확장만).

### 추가 후속 (Phase 2 — 실 board flash / oscilloscope capture)

- USB-CDC upload (`./build.sh upload PORT=/dev/cu.usbmodem...`) →
  Arduino Uno R3 + AD9833 breakout 실 wire → `--backend scope_capture`
  추가 (Saleae Logic / Rigol DS1054Z trace) → SWS 2 Hz · REM 6 Hz ·
  phase-continuous switch 실측 emit → 새 record drop → demiurge
  consumer 가 oracle parity 정의 후 GATE_CLOSED_MEASURED upgrade.
- 비용: USB cable $0 (재고) · AD9833 breakout $5-15 · 오실로스코프 기
  보유 → marginal $5-15 + 0.5-1 hr wall.

## §4 honest C3

1. **skeleton only** — `to_record()` 의 measurement field 는 caller 인자
   의존 (기본값 = `state/sim.log` + `state/compile.log` 인용). bridge
   자체는 sim 을 다시 돌리지 않으며, caller 가 measurement 를 주입해야
   함. 실 board flash / scope capture 자동화는 별도 cycle.
2. **real consumer scan-foreign 부재** — demiurge 측
   `FirmwareVerifyProducer` 가 자기 verify.py 산출 (`firmware_verify_*`
   prefix) 만 list. 본 cycle 의 anima record (`anima_sleep_oscillator_*`)
   는 같은 namespace 에 존재하나 자동 인용 안 됨 → demiurge consumer
   cycle (Step 3 후속) 에서 producer 확장 필요. brain cycle 도 동일
   한계 (`gate_state=GATE_OPEN` 영구 — Phase 2 이전).
3. **3 backend 모두 GATE_OPEN** — `local_sim` / `arduino_lint` /
   `arduino_compile` 모두 silicon validation 아님 (sim · 정적 lint ·
   AVR toolchain compile only). 실 board flash + scope capture 가 첫
   `GATE_CLOSED_MEASURED` 후보 (Phase 2).
4. **`cli show` decode fail** — demiurge 측 schema decoder 가 chip F1F2
   shape 만 알고 firmware shape 미등록. brain cycle 과 동일 한계 —
   demiurge consumer cycle 에서 decoder 추가 필요.
5. **single .hex artifact only** — Phase 1b LANDED `.hex` 14197 B 한
   build 만 record 화. Multi-FQBN (Uno / Nano / Mega) sweep · 최적화
   level (`-O0` / `-O2` / `-Os`) sweep · code-size regression tracking
   별도 cycle.
6. **falsifier_pass 는 자유 문자열** — `"5/5"` / `"3/3"` / `"1/1"` 등
   caller 가 사람-읽기 형식 주입. 향후 structured 형 (`{passed: 5,
   total: 5, failed_ids: []}`) 으로 schema upgrade 권장.

## §5 key learning — anima-side producer skeleton 패턴 **4 도메인 확장**

본 cycle 에서 확정된 **2 번째 적용 사례** (brain 에 이어 firmware).
brain cycle § 5 의 6-step pattern 이 변경 없이 그대로 작동 — 다른
demiurge engine-gap / stub-only 도메인 (`aura` / `bio` / `chem` /
`grid` / `materials`) 도 동일 패턴으로 1-step 씩 메울 수 있음:

1. anima 측에 `<domain>_bridge.py` 추가 (skeleton dataclass +
   `to_record()` + `_main()` argparse + `--output`).
2. record JSON 의 `interface` 는 `demiurge:<domain>:<measurement>-record`
   네임스페이스.
3. provenance 6 키: `producer`, `backend`, `measurement_gate`,
   `consumer_target=demiurge:<domain>:VerifyProducer`, `scope_caveats`,
   `gate_failures`.
4. anima 측에서 직접 `~/core/demiurge/exports/<domain>/verify/<UTC>Z/`
   에 drop (mkdir 자동).
5. demiurge `cli action verify <domain>` 실행 → producer 가 (a) 자기
   record 추가 + (b) optional anima record 인용. (b) 는 producer 의
   scan-foreign 로직 유무에 따라 자동 (brain) / 수동 (firmware).
6. demiurge 측 consumer 확장 (`<Domain>VerifyProducer.swift` 의
   discovery 확장 + ActionDispatch case + schema decoder) 은 demiurge
   repo 별도 cycle.

이번 cycle 의 **delta from brain cycle**:
- brain 은 producer 부재 (`❌ no producer` → `⏳ GATE_OPEN`) — 1-step
  state transition.
- firmware 는 producer 존재 (stub) — `⏳ GATE_OPEN (stub)` →
  `⏳ GATE_OPEN (stub + anima-bridge)`. 둘 다 `⏳ GATE_OPEN` 이나
  evidence path 강화 (3-backend audit + Phase 1b LANDED `.hex` 인용).
- 3-backend audit 첫 사례 — 단일 substrate (sleep_oscillator) 가
  3 단계 evidence-ladder (sim → lint → compile → flash → scope)
  를 거치는 패턴 확립.

이 6-step skeleton + 3-backend pattern 으로 anima 측 단독 (cost $0,
Mac local) 으로 demiurge gap 4건 (aura / bio / chem / grid) + 1
upgrade 후보 (materials sibling-repo 라우팅) 도 같은 패턴으로 1-step
씩 메울 수 있음 — 단, 각 도메인의 atlas-registered SW source
(anima-physics 의 어느 hexa substrate 가 producer 의 측정 단위인지)
확정이 선행 조건.

## §6 SSOT pointer

- bridge code: `~/core/anima/anima-physics/hw/sleep_oscillator_arduino/src/demiurge_firmware_bridge.py`
- record drop: `~/core/demiurge/exports/firmware/verify/2026-05-21T08-32-41Z/anima_sleep_oscillator_20260521T083241Z.json`
- predecessor doc: `~/core/anima/anima-physics/docs/demiurge_hw_verify_2026_05_21.md` (§2.1 firmware 행 갱신됨)
- pattern source doc: `~/core/anima/anima-physics/docs/demiurge_brain_bridge_integration_2026_05_21.md`
- SW source: `~/core/anima/anima-physics/oscillator/sleep_oscillator.hexa` (§188 PASS 5/5)
- local sim source: `~/core/anima/anima-physics/hw/sleep_oscillator_arduino/src/sleep_oscillator_local_sim.py` (F-HW-SO-1..5 5/5)
- firmware source: `~/core/anima/anima-physics/hw/sleep_oscillator_arduino/src/sleep_oscillator.ino` + `ad9833_driver.{h,cpp}` (Phase 1b)
- Phase 1b compile artifact: `~/core/anima/anima-physics/hw/sleep_oscillator_arduino/state/build/sleep_oscillator.ino.hex` (14197 B)
- demiurge consumer cycle pointer: `~/core/demiurge/cockpit/Sources/DemiurgeCore/Loaders/FirmwareVerifyProducer.swift` — `runVerify()` 의 record-discovery 확장 (현재 `firmware_verify_*` prefix-only → `anima_*` 등 foreign-shape 포함)

## §7 G5 firmware status

- **Before**: ⏳ stub (QEMU mps2-an385 install-gated skip only).
- **After**: ⏳ **GATE_OPEN (anima-bridge LANDED)** — 3-backend evidence
  path + Phase 1b LANDED `.hex` 인용 + 6-step pattern 4-도메인 확장
  성립.
- **Next**: demiurge `FirmwareVerifyProducer` scan-foreign + oracle
  parity (chip f1f2 12/12 pattern) consumer-side cycle (별도 demiurge
  repo) → Phase 2 board flash + scope capture → 첫
  `GATE_CLOSED_MEASURED` upgrade.
