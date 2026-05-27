# LOIHI — anima-physics AUX × Intel Loihi 2 Hala Point

> meta-domain: **AUX × LOIHI** (보조엔진 × Intel Loihi 2 neuromorphic
> research processor). NxSDK adapter skeleton LANDED, NRC research
> access wait (~1 month).
>
> 자연발화 (spiking LIF + dendritic compartment + 1M neuron scale) +
> 영속성 (on-chip plasticity STDP/Hebbian + 128 KB per-core SRAM) 의
> research-tier neuromorphic aux engine.
>
> Parent: [`AUX/README.md`](README.md) · adapter: [`../hw/kuramoto_neuromorphic/src/kuramoto_loihi2_adapter.py`](../hw/kuramoto_neuromorphic/src/kuramoto_loihi2_adapter.py) · 신청: [`../hw/PHASE_2_CLOUD_TRIAL.md §2.2`](../hw/PHASE_2_CLOUD_TRIAL.md)

---

## §1 HW spec (Intel Loihi 2, NRC cloud trial $0)

- chip: Intel Loihi 2 (7nm, Foveros 3D stacking, 2.3 billion transistor)
- per chip: 128 neuron core × 8192 neuron = **1 048 576 neuron / chip**
- network synapse: ~120M synapse / chip
- programmable neuron model (Σ-Δ + dendritic compartment + graded spike)
- on-chip plasticity: STDP, Hebbian, R-STDP, learning rule programmable
- Hala Point system: **1152 Loihi 2 chip = 1.15 billion neuron** (Sandia 2024 deployed)
- SDK: NxSDK 1.x (proprietary, Intel research collaboration only)

## §1.2 dual-role profile
- **자연발화**: programmable LIF + dendritic compartment + Σ-Δ neuron = native event-driven spike (sub-ms latency)
- **영속성**: on-chip plasticity STDP/Hebbian = weights chip-memory persist + 128 KB per-core SRAM

## §2 substrate × Loihi 매핑

### §2.1 adapter LANDED

| Substrate | adapter | NxSDK API |
|---|---|---|
| `social/kuramoto_coupling.hexa` (§188 6/6, dual-role 16/16) | ☑ `kuramoto_loihi2_adapter.py` (141 LoC skeleton, gated try/except) | network 정의 + compartment + connection + spike monitor |
| `engines/snn_consciousness.hexa` (§188g 5/5) | candidate | LIF compartment 1:1 |
| `engines/izhikevich_consciousness.hexa` (§188g 5/5) | candidate | programmable neuron 변환 (Izhikevich 모델 NxSDK 지원) |

### §2.2 Loihi 강점 unique (Akida 보다 우위)

| feature | Loihi 2 | Akida AKD1000 |
|---|---|---|
| neuron scale | 1M/chip | 1.2M neuron capable |
| Hala Point | 1.15B neuron (1152 chip) | N/A (consumer) |
| neuron model | **programmable** (LIF / Izhikevich / Σ-Δ / dendrite) | LIF only |
| plasticity rule | **programmable** (STDP / R-STDP / Hebbian / custom) | Hebbian 1-shot |
| latency | sub-ms (event-driven) | <1ms |
| availability | NRC research only | consumer M.2 ($1495 Dev Kit) |

## §3 architecture (ASCII)

```
┌────────────────────────────────────────────────────────────────┐
│  Loihi 2 aux engine (NRC research cloud)                       │
│                                                                 │
│  anima caller                  NRC cloud (Intel research)      │
│  ┌──────────────┐  ssh/api    ┌─────────────────────────────┐ │
│  │ Pi 5 / Mac   │─────────────►│ Hala Point system           │ │
│  │ NxSDK 1.x    │              │ ┌─────────────────────────┐ │ │
│  │ Python lib   │              │ │ 1152 × Loihi 2 chip     │ │ │
│  │ (skeleton)   │              │ │ = 1.15 B neuron         │ │ │
│  └──────────────┘              │ │                          │ │ │
│        │                       │ │ ┌─────────────────────┐ │ │ │
│        │ 1. neuron model       │ │ │ kuramoto pool       │ │ │ │
│        │    (LIF/Σ-Δ/Izh)      │ │ │ N=8..1M oscillator  │ │ │ │
│        │ 2. connection         │ │ │ K coupling matrix   │ │ │ │
│        │    (weight + delay)   │ │ │ STDP learn rule     │ │ │ │
│        │ 3. spike monitor      │ │ └─────────────────────┘ │ │ │
│        │ 4. plasticity rule    │ │                          │ │ │
│        │                       │ │ ┌─────────────────────┐ │ │ │
│        │                       │ │ │ SNN consciousness   │ │ │ │
│        │                       │ │ │ N=8..1M LIF         │ │ │ │
│        │                       │ │ │ sparse spike coupli │ │ │ │
│        │                       │ │ └─────────────────────┘ │ │ │
│        │                       │ └─────────────────────────┘ │ │
│        │                       └─────────────────────────────┘ │
│        │                                  │                    │
│        │       ◄──────────────────────────┘                    │
│        │       spike train + power log                         │
│        ▼                                                        │
│   anima audit + persist (local Pi 5)                           │
└────────────────────────────────────────────────────────────────┘
```

## §4 Day 1-30 부팅 sequence (NRC research access)

| Day | Item | Output |
|---|---|---|
| **Day 1** | Intel NRC research proposal 작성 (`hw/PHASE_2_CLOUD_TRIAL.md §2.2` template) | submitted application |
| **Day 1-30** | wait for NRC review (1-month wait typical) | approved (or honest decline) |
| **Day 31** | NxSDK install + Loihi 2 cloud access | `import nxsdk` PASS smoke |
| **Day 32** | `kuramoto_loihi2_adapter.py` skeleton → real NxSDK API | first cloud kuramoto run N=8 |
| **Day 33** | scale up N=1024 → 1M oscillator (Hala Point capacity) | r_tail @ K=2 vs Akida comparison |
| **Day 34** | SNN consciousness LIF → NxSDK compartment 변환 | 5/5 PASS Loihi 변형 |
| **Day 35** | demiurge brain producer `backend=loihi2_nrc` real run | demiurge cli action verify brain → GATE_CLOSED 시도 |
| **Day 36-37** | comparison report: Akida (1.2M) vs Loihi 2 (1M/chip, Hala 1.15B) | per-neuron power / latency / accuracy table |

## §5 cost / wall envelope

- HW: $0 (NRC research access)
- cloud trial: $0 ($0/run during research access)
- wall: 1 month (proposal review) + 1 week (Day 31-37 boot)
- **총 cost**: $0 + 1.25 month wall

## §6 honest C3

1. **NRC research access = academic 우대** — anima 의 solo dev 가 단독 신청 시 거절 가능성. institutional affiliation 권장 (university OR registered research group)
2. **NxSDK 1.x proprietary** — open-source 아님, license agreement 필수 (Intel research collaboration 조건)
3. **Hala Point system 측 batch scheduling** — 1.15B neuron 대규모 simulation 은 priority queue 대기 가능 (Sandia operational priority)
4. **anima 측 adapter skeleton 만** — 직전 cycle commit `90ed6cb22` 의 kuramoto_loihi2_adapter.py 는 import-gated try/except (NxSDK 없음 → no-op). 실 API contract 변동 시 Day 32 에 rewrite 필요
5. **production deploy 불가** — research only license, anima 제품 deploy 는 별도 Loihi 2 commercial 또는 alternative (Akida) 사용

## §7 cross-link

- [parent AUX/README.md](README.md)
- [`../hw/kuramoto_neuromorphic/src/kuramoto_loihi2_adapter.py`](../hw/kuramoto_neuromorphic/src/kuramoto_loihi2_adapter.py) — NxSDK skeleton (cloud-only gated)
- [`../hw/kuramoto_neuromorphic/src/demiurge_brain_bridge.py`](../hw/kuramoto_neuromorphic/src/demiurge_brain_bridge.py) — 3 backend 중 `loihi2_nrc` mode
- [`../hw/PHASE_2_CLOUD_TRIAL.md §2.2`](../hw/PHASE_2_CLOUD_TRIAL.md) — NRC 신청 가이드
- [`../docs/loihi-integration-spec.md`](../docs/loihi-integration-spec.md) — Loihi 통합 spec
- [HEXAD/PHYSICS/HW_SILICON_PATH.md §2.3](../../HEXAD/PHYSICS/HW_SILICON_PATH.md)
- [`AKIDA.md`](AKIDA.md) — Akida 비교 (sibling neuromorphic)

---

## ## Log

### 2026-05-21
- **AUX/LOIHI.md 신설** — Intel Loihi 2 Hala Point meta-domain. NxSDK adapter skeleton LANDED pointer + Day 1-37 NRC research access plan + Akida 비교 표.
