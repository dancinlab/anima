# AKIDA — anima-physics AUX × BrainChip AKD1000

> meta-domain: **AUX × AKIDA** (보조엔진 × BrainChip Akida neuromorphic
> processor). Raspberry Pi 5 + AKD1000 Dev Kit 도착예정 ($1495 BOM).
>
> 자연발화 (1mW event-driven spike emit) + 영속성 (on-chip 1-shot
> Hebbian learn = weights chip-memory persist) **동시-satisfy** 의 가장
> 강한 dual-role boot path.
>
> Parent: [`AUX/README.md`](README.md) · HW prior cycle: [`../hw/kuramoto_neuromorphic/`](../hw/kuramoto_neuromorphic/) · cloud trial 가이드: [`../hw/PHASE_2_CLOUD_TRIAL.md §2.1`](../hw/PHASE_2_CLOUD_TRIAL.md)

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
- [`../hw/kuramoto_neuromorphic/`](../hw/kuramoto_neuromorphic/) — kuramoto_akida_adapter.py existing (Phase 1a stub)
- [`../hw/PHASE_2_CLOUD_TRIAL.md §2.1`](../hw/PHASE_2_CLOUD_TRIAL.md) — Akida Cloud 신청 가이드
- [`../docs/akida_cloud_signup_guide.md`](../docs/akida_cloud_signup_guide.md) — 가입 절차
- [`../hw/kuramoto_neuromorphic/src/demiurge_brain_bridge.py`](../hw/kuramoto_neuromorphic/src/demiurge_brain_bridge.py) — 3 backend (local_sim / **akida_cloud** / loihi2_nrc)
- [HEXAD/PHYSICS/HW_SILICON_PATH.md §2.3](../../HEXAD/PHYSICS/HW_SILICON_PATH.md) — kuramoto neuromorphic target
- [PLAN.md G6](../PLAN.md) — HW silicon Phase 1c (AKIDA = Phase 2.5 신규 tier)

---

## ## Log

### 2026-05-21
- **AUX/AKIDA.md 신설** — Pi 5 + AKD1000 Dev Kit ($1495) 도착예정 announcement. §1-§8.
- 보조엔진 후보 13개 + 신규 4개 매핑
- Day 1-7 부팅 sequence + $1502 cost envelope
- HW silicon path Phase 2.5 신규 tier 정의 (Phase 2 cloud trial 과 Phase 3 research 사이)
