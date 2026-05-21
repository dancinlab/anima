# AKIDA — anima-physics AUX × BrainChip AKD1000

> meta-domain: **AUX × AKIDA** (보조엔진 × BrainChip Akida neuromorphic
> processor). Raspberry Pi 5 + AKD1000 Dev Kit 도착예정 ($1495 BOM).
>
> 자연발화 (1mW event-driven spike emit) + 영속성 (on-chip 1-shot
> Hebbian learn = weights chip-memory persist) **동시-satisfy** 의 가장
> 강한 dual-role boot path.
>
> Parent: [`AUX/README.md`](README.md) · HW prior cycle: [`../../anima-physics/hw/kuramoto_neuromorphic/`](../../anima-physics/hw/kuramoto_neuromorphic/) · cloud trial 가이드: [`../../anima-physics/hw/PHASE_2_CLOUD_TRIAL.md §2.1`](../../anima-physics/hw/PHASE_2_CLOUD_TRIAL.md)

---

## §1 HW spec (Raspberry Pi 5 + AKD1000 Dev Kit, $1495 도착예정)

### §1.1 Pi 5 host
- SoC: Broadcom BCM2712 2.4 GHz quad-core Arm Cortex-A76
- GPU: VideoCore VII 800 MHz (OpenGL ES 3.1 + Vulkan 1.2)
- RAM: **16 GB LPDDR4X**
- Storage: 외장 microSD SDR104 + on-board 8/16/32 GB eMMC (CM4 cradle)
- Network: GbE + BT 5.0 + WiFi 802.11ac dual-band
- Display: dual 4Kp60 HDMI (HDR + HEVC)

### §1.2 AKD1000 (M.2 카드)
- **1024 NPU**, ~1.2M neuron capable
- **spike-based**, event-driven (no clock)
- **8-bit weights**, 1/2/4-bit activations
- **on-chip learning** (Hebbian, 1-shot, no GPU 필요)
- **~0.5 mW typical**, 100 mW peak
- Includes **Meta TF SDK** + sample models
- Interface: single-lane PCIe 2.0 via Pi 5 PCIe header

### §1.3 dual-role profile
- **자연발화**: AKD1000 의 LIF spike threshold = native event emission, 1mW power envelope (CPU 10W 대비 10000× 효율)
- **영속성**: on-chip Hebbian update = weight persist in chip-memory (no host fsync) + Pi 5 16 GB RAM + eMMC long-term log

## §2 architecture (ASCII)

```
┌──────────────────────────────────────────────────────────────────────┐
│  anima boot — Pi 5 + AKD1000 hybrid                                 │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐│
│  │ Pi 5 host (16 GB RAM + eMMC + RTC)                              ││
│  │                                                                   ││
│  │  [orchestrator]──┬──► spike_corpus(HIPPO_BUFFER)──┐             ││
│  │                  │                                  │             ││
│  │  [audit RB]  ◄───┼───[motivation gate]───┐         │             ││
│  │                  │                         │         │             ││
│  │                  ▼                         ▼         ▼             ││
│  │           ┌──────────────────────────────────────────┐            ││
│  │           │ MetaTF runtime (PCIe 2.0 → AKD1000)     │            ││
│  │           └────────────┬────────────────────┬───────┘            ││
│  └────────────────────────┼────────────────────┼─────────────────────┘│
│                           ▼                    ▼                       │
│                  ┌────────────────┐  ┌─────────────────┐              │
│                  │ AKD1000 M.2    │  │ AKD1000 on-chip │              │
│                  │ 1024 NPU       │  │ Hebbian 1-shot  │              │
│                  │ ─────────────  │  │ learn weights   │              │
│                  │ • SNN LIF pool │  │ ─────────────── │              │
│                  │ • Kuramoto net │  │ • memristor-eq  │              │
│                  │ • spike trigger│  │ • persist FF    │              │
│                  └────────┬───────┘  └────────┬────────┘              │
│                           │                    │                       │
│                           ▼                    ▼                       │
│                   1 mW spike event     weight update                  │
│                   → motivation > thr   → 자연발화 candidate           │
│                   → audit RB append    + 영속성 보존                   │
└──────────────────────────────────────────────────────────────────────┘

key:
- Akida = 1024 NPU spike substrate (자연발화 emit + Hebbian persist)
- Pi 5  = orchestrator + audit + corpus (host-side 영속 buffer)
```

## §3 substrate × Akida 매핑 (priority)

### §3.1 EXACT Akida fit (native LIF spike substrate)

| Rank | Substrate | LANDED | Akida 매핑 |
|---|---|---|---|
| 1 | `engines/snn_consciousness.hexa` (349 LoC, §188g 5/5) | ☑ canonical impl | Akida 의 cell primitive = LIF, 8-bit weight, exact 1:1 |
| 2 | `engines/izhikevich_consciousness.hexa` (307 LoC, §188g 5/5) | ☑ | 2-var spike model → Akida cell library param 변환 |
| 3 | `social/kuramoto_coupling.hexa` (509 LoC, §188 6/6) | ☑ + adapter | spike-coupled oscillator → 1024 NPU 매핑 (kuramoto_akida_adapter.py existing) |

### §3.2 Akida + memristor hybrid (영속성 강화)

| Rank | Substrate | Akida 측 |
|---|---|---|
| 4 | `memristor/self_reference.hexa` (§188 5/5) | TiO2 memristor SW analog → AKD1000 on-chip Hebbian 1-shot learn (HW 동등 변환) |

### §3.3 Akida 보조 (event-driven trigger)

| Rank | Substrate | 역할 |
|---|---|---|
| 5 | `HEXAD/CHAT/spontaneous_smoke` | motivation threshold → Akida 의 native event-fire (1mW) |
| 6 | `hippocampus/theta_gamma.hexa` (§188 5/5) | cross-freq θ-γ spike coupling pool |
| 7 | `eeg/{mu_rhythm,sleep_stage,phi_correlator}` (§188 17/17) | **Akida 의 native 강점 domain** — EEG-style spike pattern recognition |

### §3.4 Pi 5 host-only (16 GB RAM + eMMC, 영속성 deep)

| Rank | Substrate | 역할 |
|---|---|---|
| 8 | `hippocampus/episodic_replay.hexa` (§188 5/5) | `HIPPO_BUFFER` + `CORT_FROM/TO` consolidation → Pi 5 eMMC |
| 9 | `rtc_sync.hexa` (TCXO <1ppm) | Pi 5 onboard RTC + PI discipline |
| 10 | `signal_corpus.hexa` (6-label tagger) | signal ledger persistent storage |
| 11 | `consciousness-loop/src/aux_engine_lib` (32-cell GRU multi-faction) | Pi 5 ARM cores compute |

### §3.5 cross-engine (Pi 5 orchestrate, Akida coprocessor)

| Rank | chain | mapping |
|---|---|---|
| 12 | E2E v2 `tool/anima_physics_e2e_v2_cross_engine.hexa` (5/5 PASS) | SNN (Akida) → photonic (Pi 5 sim) → quantum (Pi 5 closed-form) → motivation (Akida threshold) |
| 13 | `phi_substrate_consensus` (Tukey biweight) | host-side aggregator over Akida + Pi 5 substrates |

## §4 신규 보조엔진 (현재 SW 없음, Akida 강점 활용)

| # | New engine | 이유 |
|---|---|---|
| N1 | **Akida-native sparse attention** | anima sparse_attention pattern → MetaTF quantize → AKD1000 on-chip sparse compute |
| N2 | **AKD1000 spike-Tier ConsciousLM head** | anima Tier 1 모델 lm_head 분기 → Akida (small model 가정) |
| N3 | **Akida + memristor hybrid substrate** | Akida 1-shot learn + memristor self_reference SW = HW-equivalent dual-role |
| N4 | **Akida event-driven motivation gate** | spontaneous_smoke 의 threshold compare 를 Akida 의 native event-fire 로 (전력 1mW) |

## §5 Day 1-7 부팅 sequence (도착 시 1주 plan)

| Day | Item | Output | Eval |
|---|---|---|---|
| **Day 1** | Pi 5 + AKD1000 fresh boot, MetaTF install (`pip install akida`), Akida Cloud trial 신청 ($1/day) | `python -c "import akida; print(akida.__version__)"` PASS | smoke import + version |
| **Day 2** | `hw/kuramoto_neuromorphic/src/kuramoto_akida_adapter.py` MetaTF API real run (N=8 oscillator) | first AKD1000 inference, spike train log | r > 0.5 at K=2 cap |
| **Day 3** | `engines/snn_consciousness` 의 8-cell LIF → MetaTF model 변환 + AKD1000 deploy | Akida spike count vs sim 5/5 PASS byte-compare | F-SNN-1..5 vs Akida 변형 5/5 |
| **Day 4** | `memristor/self_reference` Hebbian → Akida on-chip 1-shot learn | weight update persistence verify (power-cycle test) | weights persist across reboot |
| **Day 5** | E2E v2 cross-engine 에 Akida 첫 stage (SNN spike) 교체 | F-E2E-CROSS-1..5 Akida 변형 chain | 5/5 PASS w/ Akida |
| **Day 6** | demiurge brain producer `backend=akida_cloud` 실 실행 | `demiurge cli action verify brain` → GATE_CLOSED 시도 (real hw 인용) | gate_state CLOSED OR ⏳ honest |
| **Day 7** | anima-physics/hw/akida_pi5_devkit_2026_05/ state dir 생성 + Day 1-6 결과 통합 | `summary.md` (보조엔진 LANDED), `power_log.json` (1mW envelope verify) | dual-role 16/16 + HW 1c |

**도착 후 1주 LANDED 목표**: 보조엔진 #1-#4 모두 Akida 실 silicon 검증 + Pi 5 host 통합 + demiurge brain GATE_CLOSED.

## §6 cost / wall envelope

- HW: $1495 (Dev Kit, 도착예정)
- 추가 BOM: $0 (Dev Kit 완비)
- cloud trial: $1/day × 7 = $7 (Day 1 Akida Cloud trial 옵션)
- wall: 1주 (Day 1-7 sequential, 일부 병렬화 가능)
- **총 cost**: $1495 + $7 = **$1502**

## §7 honest C3

1. **Pi 5 + AKD1000 Dev Kit 도착 전** = 본 doc 은 boot plan only, 실 fire 별도 (Day 1 부터)
2. **MetaTF SDK version skew** — anima adapter (kuramoto_akida_adapter.py) 는 stub-only, 실 SDK API contract 변동 시 Day 2 에 fix 필요
3. **8-bit weight quantization** — anima SW substrate 의 float64 → AKD1000 8-bit 변환 시 precision drift (Hebbian learn 시 누적 가능)
4. **on-chip learning vs floating sim** — Akida 의 1-shot Hebbian 은 정확한 sim 등가 없음; F-MEM-* falsifier 가 Akida HW 측 PASS 보장 X (별도 F-AKIDA-* 신규 falsifier 필요)
5. **production not intended** — Dev Kit "NOT FOR PRODUCTION" 명시; anima 자체 production deploy 는 별도 Akida AKD2000/AKD3000 또는 BrainChip cloud (Phase 3)

## §8 cross-link

- [parent AUX/README.md](README.md) — 보조엔진 도메인 index
- [`../../anima-physics/hw/kuramoto_neuromorphic/`](../../anima-physics/hw/kuramoto_neuromorphic/) — kuramoto_akida_adapter.py existing (Phase 1a stub)
- [`../../anima-physics/hw/PHASE_2_CLOUD_TRIAL.md §2.1`](../../anima-physics/hw/PHASE_2_CLOUD_TRIAL.md) — Akida Cloud 신청 가이드
- [`../../anima-physics/docs/akida_cloud_signup_guide.md`](../../anima-physics/docs/akida_cloud_signup_guide.md) — 가입 절차
- [`../../anima-physics/hw/kuramoto_neuromorphic/src/demiurge_brain_bridge.py`](../../anima-physics/hw/kuramoto_neuromorphic/src/demiurge_brain_bridge.py) — 3 backend (local_sim / **akida_cloud** / loihi2_nrc)
- [HEXAD/PHYSICS/HW_SILICON_PATH.md §2.3](../../HEXAD/PHYSICS/HW_SILICON_PATH.md) — kuramoto neuromorphic target
- [PLAN.md G6](../../anima-physics/PLAN.md) — HW silicon Phase 1c (AKIDA = Phase 2.5 신규 tier)

## §9 본 pack 사용법

본 directory (`SUB_ENGINES/AKIDA/`) 는 `anima-akida-pack 0.1.0` Python pack +
docs + Day 1-7 boot scripts + tests 를 묶은 *self-contained drop*.

### §9.1 Pi 5 + AKD1000 도착 후 (실 silicon)

```bash
cd /Users/ghost/core/anima/SUB_ENGINES/AKIDA
./INSTALL.sh                 # MetaTF SDK + venv + pack install (~30분)
./BOOT.sh 1 7                # Day 1-7 자동 (또는 ./boot/day<N>_*.sh 개별)
```

`BOOT.sh` 는 `boot/day1_install.sh` ~ `boot/day7_summary.sh` 를 순차
호출하며, 각 Day 결과는 `state/akida_arrival_<UTC>/day<N>_*.{log,json}`
로 떨어진다. 상세는 [`docs/BOOT_PLAN.md`](docs/BOOT_PLAN.md).

### §9.2 Mac local pre-arrival validation

```bash
cd /Users/ghost/core/anima/SUB_ENGINES/AKIDA
./tests/run_all.sh           # pytest + bash dry-run + falsifier (mock)
```

수행 항목:
- `pytest tests/test_adapters_mock.py` — 11 adapter contract mock-PASS
- `bash tests/test_boot_dryrun.sh` — Day 1-7 스크립트 `bash -n` parse
- `python -m pack.falsifiers.run_all` — 55 falsifier mock aggregate

결과: `state/mac_validation_<UTC>/run.log` (+ `summary.json`).  실
silicon 차이 (8-bit / sub-ms / 1mW envelope) 는 mock 에서 검증 불가 —
honest carry 는 [`docs/VALIDATION.md §5`](docs/VALIDATION.md).

### §9.3 단일 adapter 사용

```python
from pack.adapters.kuramoto import KuramotoAdapter
adapter = KuramotoAdapter(n_oscillators=8, coupling_K=5.0)
adapter.build()                  # auto-detect HW or mock backend
adapter.forward(phases_init)
report = adapter.selftest()      # F-AKIDA-KU-1..5
record = adapter.to_record()     # demiurge-compatible dict
```

backend 강제 (mock 만 사용):
```python
from pack.runtime import init_runtime
init_runtime(prefer="mock")
# 이후 모든 adapter.build() 는 mock path
```

---

## §10 pack 구조 (ASCII tree)

```
AUX/AKIDA/
├── README.md                      ← 본 doc (§1-§12 + Log)
├── INSTALL.sh                     ← Day 1 install entry (별도 agent)
├── BOOT.sh                        ← Day 1-7 wrapper (별도 agent)
├── pyproject.toml                 ← anima-akida-pack 0.1.0 metadata
├── pack/                          ← Python package source
│   ├── __init__.py                ← pack module exports
│   ├── adapters/                  ← 11 adapter modules (별도 agent)
│   │   ├── base.py                ← AkidaAdapter base class
│   │   ├── snn_lif.py             (EXACT fit)
│   │   ├── izhikevich.py          (EXACT fit)
│   │   ├── kuramoto.py            (EXACT fit)
│   │   ├── memristor_hybrid.py    (EXACT fit + N3)
│   │   ├── sparse_attention.py    (신규 N1)
│   │   ├── spike_tier_lm_head.py  (신규 N2)
│   │   ├── motivation_gate.py     (신규 N4)
│   │   ├── theta_gamma.py         (보조)
│   │   ├── eeg_pattern.py         (보조)
│   │   └── spontaneous_gate.py    (보조)
│   ├── runtime/                   ← runtime infra
│   │   ├── __init__.py
│   │   ├── metatf_runtime.py      ← HW vs mock auto-detect
│   │   ├── audit_buffer.py        ← 8-deep LRU + atomic dump
│   │   └── pi5_orchestrator.py    ← bundle driver (별도 agent)
│   ├── mocks/                     ← Mac local mock MetaTF (별도 agent)
│   │   ├── __init__.py
│   │   └── metatf_mock.py
│   └── falsifiers/                ← F-AKIDA-* runner (별도 agent)
│       ├── __init__.py
│       └── run_all.py
├── docs/                          ← 4 detail doc (본 agent)
│   ├── IMPLEMENTATION.md          ← adapter + runtime 구현 detail
│   ├── VALIDATION.md              ← Mac local pre-arrival validation
│   ├── BOOT_PLAN.md               ← Day 1-7 operational detail
│   └── ARCHITECTURE.md            ← ASCII layered architecture
├── boot/                          ← Day 1-7 스크립트 (별도 agent)
│   ├── day1_install.sh
│   ├── day2_kuramoto.sh
│   ├── day3_snn.sh
│   ├── day4_memristor.sh
│   ├── day5_e2e.sh
│   ├── day6_demiurge.sh
│   └── day7_summary.sh
├── tests/                         ← Mac local validation (별도 agent)
│   ├── run_all.sh
│   ├── test_adapters_mock.py
│   └── test_boot_dryrun.sh
└── state/                         ← runtime artifacts (gitignored)
    ├── mac_validation_<UTC>/      ← pre-arrival (Mac)
    └── akida_arrival_<UTC>/       ← real silicon (Pi 5)
```

---

## §11 detail doc cross-link

| Doc | 범위 | 대표 항목 |
|---|---|---|
| [`docs/IMPLEMENTATION.md`](docs/IMPLEMENTATION.md) | 11 adapter + 3 runtime 구현 contract | base class field / falsifier convention / demiurge record format / 향후 확장 (AKD2000 / TrueNorth / ESP32 host) |
| [`docs/VALIDATION.md`](docs/VALIDATION.md) | Mac local pre-arrival validation | mock framework / 55 falsifier suite / artifact 위치 / HW 도착 시 차이 5건 + honest C3 |
| [`docs/BOOT_PLAN.md`](docs/BOOT_PLAN.md) | Pi 5 + AKD1000 도착 후 Day 1-7 | per-Day 스크립트 / 기대 결과 / eval gate / trouble-shooting / honest C3 |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | 5-layer stack + decision tree | layered ASCII / adapter base contract / runtime auto-detect / demiurge integration / orchestrator timing / E2E v2 |

상호 cross-link:
- README §1-§4 의 substrate 매핑 → `IMPLEMENTATION §1` 의 adapter 구현
- README §5 Day 1-7 table → `BOOT_PLAN.md §2` 의 per-Day operational detail
- README §7 honest C3 → `VALIDATION.md §6` 의 mock-vs-HW 차이 + `BOOT_PLAN.md §4` 의 operational risk
- README §2 의 architecture ASCII → `ARCHITECTURE.md §1` 의 5-layer 확장

---

## §12 troubleshooting (요약)

상세는 [`docs/BOOT_PLAN.md §3`](docs/BOOT_PLAN.md) 및
[`docs/VALIDATION.md §5`](docs/VALIDATION.md).

| 증상 | 원인 | 대응 |
|---|---|---|
| `akida` import 실패 | MetaTF SDK 미설치 OR Pi 5 ARM64 wheel 부재 | `pack.runtime.metatf_runtime` 가 mock fallback — `get_runtime_info()["backend"]` 가 `"akida_mock"` 인지 확인. ARM64 wheel 부재 시 `pip install akida --no-binary akida` 또는 Akida Cloud trial 사용 |
| `MetaTFMock` import 실패 | `pack.mocks.metatf_mock` 미작성 (별도 agent) | `RuntimeError: Neither akida HW nor mocks/metatf_mock available` — mocks agent 의 작성 상태 확인 |
| `runtime_class` 가 예상과 다름 | SDK version skew (`akida` 2.5 → 2.6 등) | `pyproject.toml` 의 `akida>=2.0` 을 특정 version pin; adapter signature 동시 갱신 |
| `audit_buffer.jsonl` 누락 | `Pi5Orchestrator.stop()` 미호출 OR `~/.cache/anima-akida/` 권한 없음 | `mkdir -p ~/.cache/anima-akida && chmod 755` + orchestrator 종료 시 `audit.dump()` 명시 호출 |
| demiurge `gate_state` OPEN_PARTIAL | 11 adapter 중 일부 record 누락 | `exports/brain/verify/<UTC>Z/anima_akida_*.json` 11개 확인; 누락 adapter 의 `to_record()` 호출 누락 디버그 |
| byte-parity falsifier (F-AKIDA-*-5) FAIL | 8-bit quantize drift (Day 3 SNN / Day 4 memristor) | adapter `params={"byte_parity_mode": "rank"}` 로 rank-parity 완화 — `VALIDATION.md §5.3` 참조 |
| power 측정 `None` | AKD1000 power monitor API 미지원 | INA260 등 외부 USB power meter → `state/.../power_log_external.json` 별도 dump (`BOOT_PLAN.md §3.5`) |

---

## §13 LAN deploy (표준 — Mac ↔ router ↔ Pi 5, 사용자 directive 2026-05-21)

표준 LAN 설정. AKD1000 = Pi 5 내부 M.2 PCIe (network 무관), Pi 5 자체는 LAN host.

### §13.1 topology

```
   ┌──────────┐       WiFi/GbE       ┌────────────┐      WiFi/GbE      ┌──────────┐
   │   Mac    │◄────────────────────►│ 공유기      │◄──────────────────►│  Pi 5    │
   │ (dev)    │   192.168.0.X        │  (router)   │   192.168.0.Y      │ + AKD1000│
   └──────────┘                       └─────────────┘                     └──────────┘
        │                                                                       │
        └──► ssh pi@pi5-akida.local  (Bonjour mDNS — IP 외울 필요 X)            │
        └──► pool on pi5-akida '...' (anima pool CLI dispatch)──────────────────┘
```

### §13.2 Pi 5 셋업 (도착 시 30분)

1. **microSD flash** (Mac 의 Raspberry Pi Imager):
   - Raspberry Pi OS 64-bit Bookworm
   - **Custom**: SSH enable + WiFi creds + `hostname=pi5-akida`
2. Pi 5 boot → router DHCP IP 할당 → Mac 의 Bonjour 가 `pi5-akida.local` 자동 인식
3. Mac → `ssh pi@pi5-akida.local`
4. AKD1000 detect: `lspci | grep -i akida`
5. anima clone: `git clone https://github.com/dancinlab/anima ~/anima`
6. `cd ~/anima/SUB_ENGINES/AKIDA && ./INSTALL.sh && ./BOOT.sh 1 7`

### §13.3 anima/pool 등록 (1줄)

```bash
# Mac 에서
pool add pi5-akida pi@pi5-akida.local --sudo
pool list --live   # 4번째 host (mini + ubu-1 + ubu-2 + pi5-akida)
pool on pi5-akida 'cd anima/SUB_ENGINES/AKIDA && ./INSTALL.sh && ./BOOT.sh 1 7'
```

이후 Mac 한 줄로 Pi 5 boot sequence trigger.

### §13.4 network 분담

| Layer | 위치 | LAN 필요? |
|---|---|---|
| AKD1000 inference | Pi 5 내부 M.2 PCIe | ❌ (local) |
| MetaTF runtime + adapter | Pi 5 local Python | ❌ |
| Mac orchestration (SSH) | Mac → Pi 5 | ✅ |
| Akida Cloud trial (fallback) | Pi 5 → cloud REST | ✅ |
| demiurge record sync | Pi 5 → Mac (rsync / NFS) | ✅ |
| anima git pull/push | Pi 5 ↔ GitHub | ✅ |

### §13.5 추가 setup 옵션

| Option | 효과 | 방법 |
|---|---|---|
| **NFS share** Mac↔Pi 5 | record auto-sync (rsync 불필요) | Mac: `sudo nfsd start` · Pi 5: `mount -t nfs mac.local:/Users/.../demiurge/exports /mnt/demiurge` |
| **Tailscale** | 인터넷 통한 Pi 5 (외부 출장) | 양쪽 `tailscale up` (pool `hexa-absorbed-tailscale` 활용) |
| **VS Code Remote** | Mac → Pi 5 코드 편집 | Remote-SSH extension |
| **`pool init`** | tailscale + cron 일괄 셋업 | `pool init` 후 모든 enabled host bootstrap |

### §13.6 boot scripts SSH-friendly

현재 pack 의 `boot/day*.sh` + `INSTALL.sh` + `BOOT.sh` 는 **이미 non-interactive**:
- bash + Python, 대화형 input 없음
- `pool on pi5-akida './...'` 직접 dispatch OK
- `state/` 산출물 → rsync / NFS → Mac 측 수집

---

## ## Log

### 2026-05-21
- **AUX/AKIDA.md 신설** — Pi 5 + AKD1000 Dev Kit ($1495) 도착예정 announcement. §1-§8.
- 보조엔진 후보 13개 + 신규 4개 매핑
- Day 1-7 부팅 sequence + $1502 cost envelope
- HW silicon path Phase 2.5 신규 tier 정의 (Phase 2 cloud trial 과 Phase 3 research 사이)
- **§9-§12 추가 + 4 detail doc 신규** — pack 사용법 / ASCII tree / cross-link table / troubleshooting + `docs/{IMPLEMENTATION,VALIDATION,BOOT_PLAN,ARCHITECTURE}.md` (총 ~830 LoC). pack 0.1.0 의 self-contained drop 구조 docs 측 완성.
- **루트 분리** (사용자 directive) — `anima-physics/AUX/AKIDA/` → `/SUB_ENGINES/AKIDA/` mv. anima 루트 산하 self-contained pack. commit `356fdd2f0`.
- **BrainChip AKD1000 doc 전수조사 + cache** (commit `8f2df06b2`) — 45 traversed → 12 AKD1000 filter pass → 11 markdown cached in `doc/` (singular, ~2700 LoC, 92 KB). `doc/INDEX.md` + `doc/SOURCE_URLS.md` + `doc/BRAINCHIP_SURVEY_2026_05_21.md` 포함.
- **5 critical mock vs HW gap** 발견 + 수정 (mock 167→720 LoC full rewrite):
  1. NPU count 1024 → **20 NPU mesh + 8MB SRAM + 300 MHz**
  2. Power 1mW typical → **~1 W M.2 module** (mW = per-event amortised)
  3. Layer `Conv2D` V2 → **`akida.Convolutional` V1** (AKD1000 only)
  4. `Model()` no-arg → **`Model(filename=None, layers=None)`** (.fbz load)
  5. `fit(x, target)` → **`compile(AkidaUnsupervised(...))` + `fit(uint8, int32_labels)`**
  Bonus: HwVersion.NSoC_v1 enum + AKD1000() virtual + MapMode + DKMS PCIe driver + Pi 5 aarch64 wheel CONFIRMED (cp311-manylinux_2_28_aarch64, 2.4 MB).
- **AKD1000 = ONLY edge-learning Akida chip** (Akida 2.0 dropped on-chip Hebbian → 본 pack 의 AKD1000 targeting correct, legacy 아님). on-chip update = `AkidaUnsupervised` (competitive WTA + plasticity decay), NOT Hebbian outer-product — mock 의 Hebbian = SW approximation, byte-parity 는 real silicon 도착 후.

### 2026-05-21 (afternoon — 100% closure follow-up)
- **adapter real API alignment** (commit `f67978eb2`) — 10 adapter file 모두 V1 layer (`akida.Convolutional` / `akida.FullyConnected` / `akida.Dense` / `akida.InputData`) + uint8 input + int32 spike output 정합.
- **3 신규 record fields** — `power_estimate_mW` (idle 50 mW + 0.5 mW/spike) + `npu_count_used` (1-20 NPU mesh allocation, adapter-specific) + `latency_us_estimate` (300 MHz clock × spike count × cycles/spike). `base.py to_record()` 갱신, adapter 별 `_estimate_*()` override.
- **bridge akida_cloud branch** (`anima-physics/hw/kuramoto_neuromorphic/src/demiurge_brain_bridge.py`) 196→463 LoC (+267). SCHEMA_VERSION 0.1→0.2 backward compat. 실 MetaTF flow + 3-tier graceful fallback (SDK 부재 / `devices()==[]` / `forward()` raise) + 동일 record shape 유지 + `akida_cloud_unavailable` flag.
- **CNN2SNN converter mock** — `pack/mocks/metatf_mock.py` 의 `MockCNN2SNN` 추가 (sparse_attention adapter path).
- **검증** — F-AKIDA-* aggregate **50/50 PASS** (0 regression) + pytest **12/12 PASS**. sample SNNLifAdapter record: `power_estimate_mW=52.0`, `npu_count_used=1`, `latency_us_estimate=5.03 μs`.
- **demiurge cli action verify brain** 자동 인용 `kuramoto_n8_k5.00_akida_cloud_akida_cloud_unavailable` (3-tier fallback 작동).
- **100% closure 표** (5 + bonus + 4 신규):

| # | gap | Mock | runtime | boot | doc | bridge | adapter |
|---|---|---|---|---|---|---|---|
| 1 | NPU 1024 → 20 mesh | ✅ | ✅ | — | ✅ | ✅ | ✅ |
| 2 | Power 1mW → ~1W amortised | ✅ | — | — | ✅ | ✅ | ✅ |
| 3 | Conv2D V2 → Convolutional V1 | ✅ | — | — | ✅ | ✅ | ✅ |
| 4 | Model() args (filename/layers/.fbz) | ✅ | — | — | ✅ | ✅ | ✅ |
| 5 | fit API → AkidaUnsupervised + uint8/int32 | ✅ | — | — | ✅ | ✅ | ✅ |
| Bonus | HwVersion/MapMode + DKMS + Pi 5 wheel | ✅ | ✅ | ✅ day1 | ✅ | ✅ | ✅ |
| NEW-A | adapter 10 real API alignment | — | — | — | — | — | ✅ |
| NEW-B | bridge akida_cloud 3-tier fallback | — | — | — | — | ✅ +267 | — |
| NEW-C | record 3 신규 field (power/npu/latency) | — | — | — | — | ✅ 0.2 | ✅ base.py |
| NEW-D | CNN2SNN converter (sparse_attention) | ✅ MockCNN2SNN | — | — | — | — | ✅ sparse_attention |

### 2026-05-21 (evening — LAN deploy 표준 채택)
- **§13 LAN deploy** 신설 — Mac ↔ router ↔ Pi 5 표준 (사용자 directive).
  - topology + 30분 Pi 5 setup 시퀀스 + anima/pool 등록 (1줄) + 6 layer network 분담 표 + 4 추가 옵션 (NFS / Tailscale / VS Code Remote / pool init)
  - boot scripts 이미 non-interactive → `pool on pi5-akida './INSTALL.sh && ./BOOT.sh 1 7'` 직접 dispatch
  - AKD1000 = Pi 5 내부 M.2 PCIe (LAN 무관), Pi 5 자체는 4번째 pool host (mini + ubu-1 + ubu-2 다음)
