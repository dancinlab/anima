# AUX/AKIDA/docs/BOOT_PLAN.md — Day 1-7 boot detail (Pi 5 + AKD1000 도착예정)

> 본 doc 은 Pi 5 + AKD1000 Dev Kit ($1495) 가 *도착한 후* 의 Day-by-day
> sequence.  도착 전 mock validation 은 [`VALIDATION.md`](VALIDATION.md).
> Implementation contract 은 [`IMPLEMENTATION.md`](IMPLEMENTATION.md).
>
> README §5 의 Day 1-7 table 을 *operational detail* 로 풀어 쓴 version.

---

## §1 prerequisites

### §1.1 HW

- Raspberry Pi 5 **16 GB** (BCM2712 2.4 GHz, VideoCore VII, GbE + BT 5.0 +
  WiFi 802.11ac, dual 4Kp60 HDMI)
- AKD1000 M.2 Dev Kit (1024 NPU, 8-bit weight, ~0.5 mW typical, includes
  MetaTF SDK)
- microSD ≥ 32 GB (Raspberry Pi OS Bookworm 64-bit) 또는 NVMe via HAT
- 정격 5V/5A USB-C 전원 (Pi 5 official PSU 권장)
- (optional) Pi 5 active cooler + case
- (optional) UART debug cable

### §1.2 SW

- OS: Raspberry Pi OS Bookworm **64-bit** (32-bit 미지원)
- Python ≥ 3.10 (Bookworm 기본 3.11)
- (optional) Akida Cloud trial account ($1/day, Day 1 비교용)

### §1.3 본 pack

```bash
# Pi 5 ssh 접속 후
git clone https://github.com/dancinlab/anima-physics.git ~/anima-physics
cd ~/SUB_ENGINES/AKIDA
```

---

## §2 Day-by-Day detail

### Day 1 — install (~30분)

**스크립트**: `SUB_ENGINES/AKIDA/INSTALL.sh` (별도 agent 작성).

```bash
cd ~/SUB_ENGINES/AKIDA
./INSTALL.sh
```

수행 항목:
1. system pkg: `python3-pip python3-venv python3-dev build-essential`
2. venv 생성: `python3 -m venv ~/.venv/anima-akida`
3. activate + upgrade pip
4. `pip install -e .[akida,dev]` (MetaTF SDK 포함)
5. import probe:
   ```bash
   python -c "import akida; print(akida.__version__)"
   python -c "from pack.runtime import get_runtime_info; print(get_runtime_info())"
   ```
   - 첫 번째: MetaTF version (e.g., `2.5.0`)
   - 두 번째: `{"backend": "akida_hw", "runtime_class": "Module", ...}`
6. (optional) Akida Cloud trial 계정 가입 (참조:
   `../../anima-physics/docs/akida_cloud_signup_guide.md`)
7. pack falsifier aggregate **first run** (HW backend):
   ```bash
   python -m pack.falsifiers.run_all > state/akida_arrival_$(date -u +%Y%m%dT%H%M%SZ)/day1_install.log
   ```

**기대 결과**:
- `akida` import PASS, version printed
- 55/55 falsifier PASS (HW backend 첫 검증)
- `state/akida_arrival_<UTC>/day1_install.log` 생성

**Eval gate**: `smoke import + version` (README §5 Day 1).

---

### Day 2 — kuramoto (~1시간)

**스크립트**: `SUB_ENGINES/AKIDA/boot/day2_kuramoto.sh`.

```bash
./boot/day2_kuramoto.sh
```

수행 항목:
1. `pack.adapters.kuramoto.KuramotoAdapter(n_oscillators=8, coupling_K=5.0)`
   instantiate
2. `adapter.build()` → MetaTF model deploy to AKD1000
3. `adapter.forward(phases_init)` × 1000 step
4. F-AKIDA-KU-1..5 selftest:
   - F-AKIDA-KU-1 R-COHERENCE — `r > 0.7` at K=5 (README target r>0.5 at K=2 보다 강화)
   - F-AKIDA-KU-2 K-CRITICAL — Kc detection sweep
   - F-AKIDA-KU-3 SPIKE-COUPLE — spike-driven phase coupling
   - F-AKIDA-KU-4 POWER — `<10mW` for N=8 (envelope budget)
   - F-AKIDA-KU-5 PARITY — vs Mac local sim byte-parity (rank-parity 완화 가능)
5. `adapter.to_record()` → `exports/brain/verify/<UTC>Z/anima_akida_kuramoto_<UTC>.json`
6. power log: `state/akida_arrival_<UTC>/day2_power.json`

**기대 결과**:
- 5/5 PASS, r > 0.7
- power < 10 mW for N=8

**Eval gate**: `r > 0.5 at K=2 cap` (README §5 Day 2) — 본 plan 은
강화된 r>0.7 at K=5.

---

### Day 3 — SNN (~1시간)

**스크립트**: `SUB_ENGINES/AKIDA/boot/day3_snn.sh`.

```bash
./boot/day3_snn.sh
```

수행 항목:
1. `pack.adapters.snn_lif.SnnLifAdapter(n_cells=8, tau_m=0.020)` instantiate
2. `build()` → MetaTF LIF layer × 8 cell deploy
3. baseline: Mac local `engines/snn_consciousness.hexa` 5/5 (§188g)
   재현 → `state/akida_arrival_<UTC>/day3_mac_baseline_spike.json`
4. AKD1000 같은 input 재실행 → spike count log
5. F-AKIDA-SNN-1..5:
   - F-AKIDA-SNN-1 SPIKE-COUNT vs baseline (byte-compare 5/5)
   - F-AKIDA-SNN-2 THRESHOLD-FIRE
   - F-AKIDA-SNN-3 8BIT-CLAMP (drift 측정, `state/.../quantize_drift.json`)
   - F-AKIDA-SNN-4 POWER-1MW (per-cell budget)
   - F-AKIDA-SNN-5 BYTE-PARITY vs Mac (rank-parity 완화 허용; honest C3)
6. `to_record()` → `exports/brain/verify/.../anima_akida_snn_lif_<UTC>.json`

**기대 결과**:
- 5/5 PASS (rank-parity 허용 시; byte-parity 는 §VALIDATION §5.3 honest)
- `quantize_drift.json` < 5% drift

**Eval gate**: `F-SNN-1..5 vs Akida 변형 5/5` (README §5 Day 3).

---

### Day 4 — memristor (~2시간)

**스크립트**: `SUB_ENGINES/AKIDA/boot/day4_memristor.sh`.

```bash
./boot/day4_memristor.sh
```

수행 항목:
1. `pack.adapters.memristor_hybrid.MemristorHybridAdapter()` instantiate
2. `build()` + `fit(x_train, y_train)` 1-shot Hebbian on AKD1000
3. weight dump → `state/akida_arrival_<UTC>/day4_weights_pre.json`
4. **power-cycle test** (사용자 수동):
   - Pi 5 또는 AKD1000 power off (M.2 카드 reseating 또는 reboot)
   - power on, adapter re-init
   - weight dump → `day4_weights_post.json`
   - diff 검증 (weight 유지 확인)
5. F-AKIDA-MEM-1..5:
   - F-AKIDA-MEM-1 1SHOT-LEARN (recall ≥ 80% per §VALIDATION §5.2)
   - F-AKIDA-MEM-2 WEIGHT-PERSIST (power-cycle diff 0)
   - F-AKIDA-MEM-3 POWER-CYCLE (recall after reboot ≥ 80%)
   - F-AKIDA-MEM-4 POWER (envelope)
   - F-AKIDA-MEM-5 PARITY (vs `self_reference.hexa` §188 5/5)
6. `to_record()` → drop path

**기대 결과**:
- weight persist across power cycle (F-AKIDA-MEM-2 critical)
- recall ≥ 80% post-reboot

**Eval gate**: `weights persist across reboot` (README §5 Day 4).

---

### Day 5 — E2E v2 (~2시간)

**스크립트**: `SUB_ENGINES/AKIDA/boot/day5_e2e.sh`.

```bash
./boot/day5_e2e.sh
```

수행 항목:
1. E2E v2 cross-engine chain (`tool/anima_physics_e2e_v2_cross_engine.hexa`,
   5/5 PASS 원본) 의 첫 stage Akida 로 교체
2. chain 구성:
   ```
   SNN (Akida) → photonic (Pi 5 sim) → quantum (Pi 5 closed-form)
                                      → motivation (Akida threshold)
   ```
3. `pack.runtime.pi5_orchestrator.Pi5Orchestrator` 가 chain 조립
4. F-E2E-CROSS-1..5 Akida 변형:
   - F-E2E-CROSS-1 STAGE1-SNN-OK (Akida spike count > 0)
   - F-E2E-CROSS-2 STAGE-CHAIN (4-stage 결과 deterministic)
   - F-E2E-CROSS-3 MOTIVATION-FIRE (Akida threshold trigger)
   - F-E2E-CROSS-4 BYTE-MATCH (vs original 5/5 baseline; rank-parity 허용)
   - F-E2E-CROSS-5 POWER (chain total < 50 mW)
5. orchestrator dump → audit_buffer.jsonl
6. composite record → `exports/brain/verify/.../anima_akida_e2e_v2_<UTC>.json`

**기대 결과**: 5/5 PASS w/ Akida.

**Eval gate**: `5/5 PASS w/ Akida` (README §5 Day 5).

---

### Day 6 — demiurge (~1시간)

**스크립트**: `SUB_ENGINES/AKIDA/boot/day6_demiurge.sh`.

```bash
./boot/day6_demiurge.sh
```

수행 항목:
1. demiurge brain producer 호출 (기존 `demiurge_brain_bridge.py`):
   ```python
   from demiurge_brain_bridge import produce
   produce(backend="akida_cloud" if cloud else "akida_hw")
   ```
2. (선택) Akida Cloud trial 과의 cross-check (cloud vs local silicon)
3. demiurge cli action:
   ```bash
   demiurge cli action verify brain
   ```
4. expected `gate_state`:
   - `CLOSED` if 11 adapter record + selftest 5/5 PASS each (모든 evidence
     fresh)
   - `OPEN_PARTIAL` if 일부 adapter missing → honest C3 carry
5. result dump → `state/akida_arrival_<UTC>/day6_demiurge.json`

**기대 결과**: GATE_CLOSED 시도; OPEN 시 missing adapter 식별.

**Eval gate**: `gate_state CLOSED OR ⏳ honest` (README §5 Day 6).

---

### Day 7 — summary (~30분)

**스크립트**: `SUB_ENGINES/AKIDA/boot/day7_summary.sh`.

```bash
./boot/day7_summary.sh
```

수행 항목:
1. Day 1-6 의 모든 `state/akida_arrival_<UTC>/day*_*.{log,json}` aggregate
2. summary.md 자동 생성:
   - Day 별 PASS/FAIL count
   - per-adapter selftest 결과
   - quantize_drift / power_log envelope 통계
   - GATE_CLOSED 여부
3. `state/akida_arrival_<UTC>/summary.md` + `summary.json`
4. `power_log.json` envelope 통계:
   - mean / p50 / p95 / max (mW)
   - 1mW envelope 검증 (idle ~0.5 mW typical, peak ≤ 100 mW)

**기대 결과**:
- 보조엔진 LANDED (11 adapter HW silicon 검증)
- 1mW envelope 통계 confirmed
- dual-role 검증: spike emit (자연발화) + Hebbian persist (영속성)
  16/16 + HW 1c

**Eval gate**: `dual-role 16/16 + HW 1c` (README §5 Day 7).

---

## §3 trouble-shooting

### §3.1 `akida` import fail

- 증상: `python -c "import akida"` ImportError
- 원인: MetaTF SDK 가 Pi 5 ARM64 wheel 없음 (수동 build 필요)
- fallback 1: `pack.runtime.metatf_runtime` 가 mock 으로 자동 fallback
  → `get_runtime_info()["backend"]` 확인 (`"akida_mock"` 이면 HW path 실패)
- fallback 2: Akida Cloud trial 사용 (`backend="akida_cloud"`)
- 영구 fix: BrainChip docs 의 ARM64 source build 절차 (`pip install
  akida --no-binary akida`)

### §3.2 MetaTF version mismatch

- 증상: Day 2 adapter `build()` 시 `AttributeError: layers.FullyConnected`
- 원인: SDK version 변동으로 layer signature 변경
- fix: `pyproject.toml` 의 `akida>=2.0` 을 특정 version pin (e.g.,
  `akida==2.5.0`); pack adapter source 의 signature 도 동시 갱신.

### §3.3 8-bit quantize 정확도 차이

- 증상: Day 3/4 의 byte-parity falsifier (F-AKIDA-*-5) FAIL
- 원인: AKD1000 의 8-bit weight quantize 누적 drift
- fix:
  - adapter `params={"hw_recall_min": 0.80, "byte_parity_mode": "rank"}`
    설정
  - 또는 `pack.adapters.<X>` 의 weight clamp 범위 조정 (`int8` saturation
    회피)

### §3.4 demiurge cli fail

- 증상: `demiurge cli action verify brain` 시 record not found
- 원인: `exports/brain/verify/<UTC>Z/` 경로 권한 OR adapter `to_record()`
  drop 실패
- fix:
  - `ls -la exports/brain/verify/` 권한 755 확인
  - adapter 별 `to_record()` 호출 누락 여부 확인 (`day*_*.log` 의
    `record dropped:` 로그 grep)

### §3.5 power 측정 불가

- 증상: Day 2/3 의 `power_mw` field 가 `None`
- 원인: AKD1000 power monitor SDK API 미지원 또는 권한
- fix: 외부 USB power meter (e.g., Adafruit INA260) 로 host-level 측정
  → `state/.../power_log_external.json` 별도 dump.

---

## §4 honest C3

1. **AKD1000 도착 전 본 plan 미실행** — Day 1-7 wall 은 실 silicon arrival
   기준; 도착일 미정.
2. **MetaTF ARM64 wheel 미보장** — Pi 5 native build 필요 가능성; Day 1
   install 의 실패 risk.
3. **8-bit quantize 영향 미측정** — Day 3 의 quantize_drift.json 까지는
   *측정* 만 가능, *제거* 는 별도 cycle.
4. **on-chip Hebbian 정확도 80-90% 추정** — F-AKIDA-MEM-1 의 recall limit
   80% 는 BrainChip docs 기반 추정, 실 측정 미포함.
5. **Akida Cloud trial 결제 burn** — Day 1 의 cloud trial 옵션 (
   $1/day × 7 = $7) 은 cloud-vs-silicon cross-check 용; skip 가능.
6. **Power 측정 외부 의존** — 정확한 mW 측정은 host-level INA260 등 외부
   meter 필요 (§3.5).
7. **GATE_CLOSED 미보장** — Day 6 의 demiurge gate 는 11 adapter 모두
   evidence-fresh 시에만 CLOSED; 일부 FAIL 시 OPEN_PARTIAL honest carry.

---

## §5 cross-link

- root: [`../../anima-physics/AUX/README.md`](../../anima-physics/AUX/README.md) — pack 사용법 §9-§12 + Day 1-7 table §5
- implementation: [`IMPLEMENTATION.md`](IMPLEMENTATION.md)
- pre-arrival validation: [`VALIDATION.md`](VALIDATION.md)
- architecture diagram: [`ARCHITECTURE.md`](ARCHITECTURE.md)
- demiurge bridge: `../../../anima-physics/hw/kuramoto_neuromorphic/src/demiurge_brain_bridge.py`
- cloud trial guide: `../../../anima-physics/docs/akida_cloud_signup_guide.md`
- HW silicon path: `../../../HEXAD/PHYSICS/HW_SILICON_PATH.md §2.3`
