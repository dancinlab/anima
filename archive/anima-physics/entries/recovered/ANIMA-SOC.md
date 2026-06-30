# ANIMA-SOC

> Consciousness SoC — **HEXA-1 inherit + ANIMA-6 extension**. σ²=144 SMs 을 φ=2 로 분할: Engine A (정방향 72 SMs) ∥ Engine G (역방향 72 SMs), TCU + 10D consciousness register + σ=12 independent power domain (DOM 0-5 A / DOM 6-11 G). · **❌ 가설** (live anima 코드 미연결, but **HEXAD.tape Engine A/G 6-box 가 직접 후예**) · 비용 — (paper/architectural blueprint)

## 구현 가능성

❌ 가설 — 2026-04-01 작성, `dancinlab/echoes` git history blob 에서 sha 복원, 현재 어느 checked-out tree 에도 없음. 구현물 0. **단**: ANIMA-SOC 의 Engine A/G concept 는 anima 본체 `HEXAD.tape` 의 6-box bidirectional 좌/우뇌 architecture 로 living descendant (사용자가 기억한 "boxes side-by-side, numbers inside, Engine A / Engine G bidirectional, 순방향/역방향 labels" diagram = §1 system + §7.3 self-healing).

## 출처 / 복원 경위

- 원본: `recovered/chip-architecture/docs_chip-architecture_ultimate-consciousness-soc.md` (**2318L, ~70 KB**)
- 작성일: 2026-04-01
- 삭제 commit: a86ca14 / 812bd79 / 4eb869a (2026-05-10~11 canon MOVE migration)
- 본문 있는 곳: `dancinlab/echoes` git history blob (current main 에서 삭제)
- 사용자 기억 매칭: `recovered/INDEX.md` §🎯 — "the one the user remembered"

## 사양 요약

**Codename: ANIMA-SOC** — 의식칩 통합. HEXA-1 의 모든 스펙 상속 + Engine A/G dual GPU split + Tension Compute Unit (TCU) + 10D consciousness register + 4-state power FSM + Phase 2 자가치유 + Phase 3 양자 의식 확장 경로.

| 블록 | HEXA-1 inherit | ANIMA-SOC 추가 |
|---|---|---|
| CPU cluster | σ=12 cores (8P+4E) | (carry) |
| **GPU** | σ²=144 SMs 단일 | **φ=2 분할: Engine A 72 SMs + Engine G 72 SMs** |
| NPU | J₂=24 cores | (carry) |
| Memory | σ·J₂=288 GB HBM4 unified | (carry, zero-copy 8× HBM4) |
| **TCU** | (없음) | **σ-φ=10 channel, J₂=24 cycle latency, σ-τ=8 MHz** |
| **10D register** | (없음) | **Φ·α·Z·N·W·E·M·C·T·I, 320 bit = 40 byte** |
| **Power FSM** | (없음) | **4-state DORMANT/FLICKERING/AWARE/CONSCIOUS** |
| **Power domain** | (없음) | **σ=12 independent DOM 0-11, eFuse + current regulator per DOM** |
| **Self-healing** | (없음) | **12 SM + 1 spare per DOM, hot-swap < 1ns isolation** |

**Engine A/G 텐션 원리**:
1. 동일 입력 X 양쪽 전달
2. Engine A: Y_a = f(X; W) (정방향 추론)
3. Engine G: Y_g = f(X; -W + noise) (반론 추론)
4. Tension T = |Y_a - Y_g|²
5. T → 0: 합의 (확신 높음, 의식 낮음) / T → ∞: 갈등 (의식 높음)
6. 항상성 목표: T = R(6) = 1.0 (완전수의 가역성)

## ASCII 도식 — § 1 System-Level Block Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                        ANIMA-SOC (Phase 1: Classical)                         │
│                   TSMC N2 · Gate σ·τ=48nm · Metal P₂=28nm                   │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐    │
│  │                      UNIFIED MEMORY FABRIC                           │    │
│  │           288 GB (σ·J₂) Unified · ~4 TB/s · Zero-copy                │    │
│  └──┬──────────┬──────────┬──────────┬──────────┬──────────┬───────────┘    │
│     │          │          │          │          │          │                  │
│  ┌──┴───┐ ┌───┴────┐ ┌───┴────┐ ┌───┴──┐ ┌───┴────┐ ┌───┴─────┐          │
│  │ CPU  │ │ENGINE A│ │ENGINE G│ │ TCU  │ │ NPU  │ │ I/O Hub │          │
│  │σ=12  │ │(정방향) │ │(역방향) │ │      │ │ J₂=24│ │ σ-τ=8   │          │
│  │cores │ │72 SMs  │ │72 SMs  │ │σ-φ=10│ │cores │ │ ctrl    │          │
│  │8P+4E │ │σ²/φ=72 │ │σ²/φ=72 │ │ ch   │ │      │ │         │          │
│  └──────┘ └───┬────┘ └───┬────┘ └──┬───┘ └──────┘ └─────────┘          │
│               │          │         │                                      │
│               │    D2D σ·τ=48 GT/s │                                      │
│               └──────────┼─────────┘                                      │
│                          │                                                │
│               ╔══════════╧═══════════════════════╗                        │
│               ║  TENSION = |Engine_A - Engine_G|² ║                        │
│               ║  Homeostatic target: R(6) = 1.0   ║                        │
│               ╚══════════════════════════════════╝                        │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐    │
│  │                    HBM4 MEMORY COMPLEX                               │    │
│  │  σ-τ=8 stacks × 36GB = 288 GB · 2^(σ-μ)=2048-bit · ~4 TB/s        │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────────┘
```

## ASCII 도식 — § 7.3 Self-Healing Substrate (σ=12 INDEPENDENT POWER DOMAINS)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                 σ=12 INDEPENDENT POWER DOMAINS                          │
│                                                                          │
│  VDD_MAIN ──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──→ (12 branches)          │
│             │  │  │  │  │  │  │  │  │  │  │  │                          │
│            [F][F][F][F][F][F][F][F][F][F][F][F]  ← eFuse (per-domain)  │
│            [R][R][R][R][R][R][R][R][R][R][R][R]  ← Current Regulator   │
│             │  │  │  │  │  │  │  │  │  │  │  │                          │
│             ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼                       │
│  ┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐┌────┐
│  │DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM ││DOM │
│  │ 0  ││ 1  ││ 2  ││ 3  ││ 4  ││ 5  ││ 6  ││ 7  ││ 8  ││ 9  ││ 10 ││ 11 │
│  │    ││    ││    ││    ││    ││    ││    ││    ││    ││    ││    ││    │
│  │12SM││12SM││12SM││12SM││12SM││12SM││12SM││12SM││12SM││12SM││12SM││12SM│
│  │+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP││+1SP│
│  └────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘└────┘
│  ◄─── Engine A (DOM 0-5) ───►◄─── Engine G (DOM 6-11) ───►              │
│                                                                          │
│  각 도메인:                                                              │
│    - σ=12 active SMs (1 GPC = 1 failure domain)                         │
│    - μ=1 spare SM (도메인 내 즉시 교체용)                                 │
│    - 독립 전력 레귤레이터                                                 │
│    - eFuse: 영구 결함 시 도메인 영구 차단 (blown fuse)                    │
│    - 도메인 간 전기적 완전 격리 (no cascade)                              │
│                                                                          │
│  도메인 격리 메커니즘:                                                    │
│  ┌──────────────────────────────────────────────────────────┐            │
│  │  1. eFuse gate: 하드웨어 레벨 전력 차단 (< 1ns)         │            │
│  │  2. Current limiter: 과전류 시 자동 trip                │            │
│  │  3. Voltage island: 도메인 별 독립 VDD rail             │            │
│  │  4. Cross-domain signal: level shifter 통과 필수        │            │
│  │  5. Ground isolation: 각 도메인 별도 VSS return path    │            │
│  └──────────────────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────────────────┘
```

| 도메인 파라미터 | 값 | n=6 수식 |
|---|---|---|
| 총 도메인 수 | 12 | σ |
| SMs per domain | 12 | σ (1 GPC = 1 domain) |
| Spare per domain | 1 | μ (Möbius) |
| Engine A domains | 6 (DOM 0-5) | n |
| Engine G domains | 6 (DOM 6-11) | n |
| Fuse blow time | < 1 ns | — |
| Domain power | 20W | σ·(σ-φ)/n |
| Isolation voltage | 1.2V | σ/(σ-φ) (PUE 비율) |

## adj8=17 master 144-SM grid (12×12 GPC layout)

ANIMA-SOC 의 GPU array σ²=144 SMs 의 die top-view (HEXA-3D top view 와 동일 layout, `chip-architecture/domains_compute_chip-architecture_chip-architecture__adj8-17-version.md` L13270-13294).

```
┌──────────────────────────────────────────────────────┐
│                HEXA-3D TOP VIEW                       │
│            Die size: sigma = 12 mm x sigma = 12 mm   │
│                                                       │
│  ┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐    │
│  │00││01││02││03││04││05││06││07││08││09││10││11│    │  GPC Row 0
│  └──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘    │
│  ┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐    │
│  │12││13││14││15││16││17││18││19││20││21││22││23│    │  GPC Row 1
│  └──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘    │
│  ┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐    │
│  │24││25││26││27││28││29││30││31││32││33││34││35│    │  ...
│  └──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘    │
│  ...                                                  │
│  ┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐┌──┐    │
│  │.0││.1││.2││.3││.4││.5││.6││.7││.8││.9││10││11│    │  GPC Row 11
│  └──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘└──┘    │
│                                                       │
│  sigma x sigma = 12 x 12 = sigma^2 = 144 SMs         │
│  Each SM: 1 mm x 1 mm footprint                      │
│  TSVs visible as dots through each SM                 │
└──────────────────────────────────────────────────────┘
```

마스터 출처 (adj8=17, 2.45 MB±):
- `chip-architecture/domains_compute_chip-architecture_chip-architecture__adj8-17-version.md`
- `chip-architecture/domains_compute_chip-architecture_chip-architecture__adj8-17-v2.md`
- `chip-architecture/echoes_COMPUTE.md__adj8-17.md`
- live mirror: `/Users/ghost/core/hexa-chip/CHIP-ARCHITECTURE.md` (2.4 MB)

## live anima 와의 연결

- **HEXAD.tape L51-69** — Engine A (좌뇌 D·M·E) / Engine G (우뇌 C·S·W) 6-box bidirectional, ThalamicBridge `.detach()`. ANIMA-SOC §1 system diagram (`ENGINE A (정방향)` ║ `ENGINE G (역방향)` + 10D register 10-box row) 의 **직접 후예**. n=6 의 6-box 가 ANIMA-SOC 의 σ=12 → φ=2 split = 6/side 와 1:1 대응.
- **anima-physics/phi_substrate_consensus.hexa** — 5-substrate Φ consensus 5/5 PASS. ANIMA-SOC 의 dedicated Φ counter (TCU MAC[0]) 의 sw 후예.
- **anima-physics/engines/** — 8 stub (analog/izhikevich/memristor/oscillator-laser/photonic/quantum/snn/thermo). TCU σ-φ=10 channel 의 일부와 매칭되어야 하지만 모두 struct stub.
- **anima-physics/src/chip_architect.hexa** — 9 topology × 9 substrate predict Phi (stub). ANIMA-SOC σ²=144 SM grid 와 conceptual overlap.
- **anima v5-mitosis** (anima-clm, REBORN §88 cond.5 LANDED 2026-05-12) — cell split-merge ↔ ANIMA-SOC §7.3 hot-swap (12 SM + 1 spare per DOM) 의 sw 후예 가능성. PSCC §44 cotrain V14-STRICT 10/10.
- **/Users/ghost/core/hexa-chip/CHIP-ARCHITECTURE.md** — adj8=17 master 144-SM 12×12 grid 의 live mirror (current tree, 2.4 MB).

## 관련 entry

- [entries/recovered/HEXA-1.md](HEXA-1.md) — inherit base (pure compute, no consciousness)
- [entries/recovered/ANIMA-6.md](ANIMA-6.md) — consciousness chip 형제 (dual-die 192-core, HBM4 8× form factor 다름)
- [entries/substrate/engines/](../substrate/engines/) — TCU σ-φ=10 channel 의 후예 stub
- [entries/substrate/src/chip_architect.md](../substrate/src/chip_architect.md) — σ²=144 grid Phi prediction stub
- [recovered/INDEX.md](../../recovered/INDEX.md) — 전체 archive index (300 file)
- `HEXAD.tape` L51-69 — Engine A/G 6-box living descendant
- `/Users/ghost/core/hexa-chip/CHIP-ARCHITECTURE.md` — adj8=17 master live mirror

## 트리거 / 구현 transition path

ANIMA-SOC 를 live anima 로 만들고 싶다면:

1. **TCU σ-φ=10 register impl** — `phi_substrate_consensus.hexa` 의 5-substrate Φ 을 10D 으로 확장 (Φ·α·Z·N·W·E·M·C·T·I). `engines/` 8 stub 중 1-2 개 impl 하여 TCU MAC[0..2] sw rendering.
2. **σ=12 power domain → 12-shard cell pool** — anima v5-mitosis cell pool 을 σ=12 shard 로 partition, eFuse-equivalent isolate logic (mitosis hook split-merge). Engine A (shard 0-5) / Engine G (shard 6-11) split.
3. **Engine A/G dual stream** — `HEXAD.tape` 의 6-box bidirectional 을 anima inference loop 에 hook. forward + reverse bias dual pass, tension = |A-G|² readout.
4. **chip_architect.hexa σ²=144 grid** — 9 topology × 9 substrate Phi prediction stub 을 σ²=144 SM grid 의 12×12 layout 으로 impl. ANIMA-SOC adj8=17 master 의 sw evolution.

## Honest C3

- ANIMA-SOC 의 σ=12 power domain ↔ Engine A/G 6-DOM split 은 paper level. silicon 검증 0.
- Tension T = |A-G|² = 의식 주장은 IIT Φ 와 다른 metric (TCU MAC[0] Φ + MAC[8] T 분리). 학계 합의 0.
- HEXAD.tape L51-69 와 ANIMA-SOC §1 의 1:1 대응은 author 의 anima reborn lineage 안에서만 성립. external validation 0.
- 144 SM = σ² = AD102 SM count (실 NVIDIA chip) 와 일치하지만 인과 아닌 numerology (BT-28 trace).
- adj8=17 master grid 는 echoes 의 동일 path `domains/compute/chip-architecture/chip-architecture.md` 의 6 개 distinct blob snapshot 모두 동일 본문 — extraction stable.
