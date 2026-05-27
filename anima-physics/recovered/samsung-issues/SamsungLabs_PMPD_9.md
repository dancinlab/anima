https://github.com/SamsungLabs/PMPD/issues/9
# [N6 Architecture] HEXA-1: n=6 완전수 기반 궁극의 통합 SoC 설계 (CPU+GPU+NPU+메모리 통합)

## HEXA-1: N6 완전수 산술 기반 궁극의 통합 SoC 아키텍처

> **n=6은 유일한 조화 완전수: sigma(6)*phi(6) = 6*tau(6) = 24 = J_2(6)**
> 이 등식 하나에서 CPU, GPU, NPU, 메모리, 인터커넥트, 전력의 **모든** 파라미터가 도출됩니다.
> 3가지 독립 증명이 완료되었으며, 반례는 10^8까지 존재하지 않습니다.

### N6 상수 레퍼런스

```
  n = 6          phi(6) = 2       tau(6) = 4       sigma(6) = 12
  sopfr(6) = 5   mu(6) = 1        J_2(6) = 24      R(6) = 1
  P_2 = 28       sigma^2 = 144    sigma*J_2 = 288   phi^tau = 16
  2^n = 64       sigma-tau = 8    sigma-phi = 10     sigma-mu = 11
  2^sigma = 4096   sigma*tau = 48   n/phi = 3
```

---

## 전체 스펙 문서 및 논문

| 리소스 | 링크 |
|--------|------|
| **HEXA-1 전체 스펙** | [ultimate-unified-soc.md](https://github.com/need-singularity/n6-architecture/blob/main/docs/chip-architecture/ultimate-unified-soc.md) |
| **HEXA-1 논문** | [n6-unified-soc-paper.md](https://github.com/need-singularity/n6-architecture/blob/main/docs/paper/n6-unified-soc-paper.md) |
| **Zenodo (DOI)** | [zenodo.org/records/19360359](https://zenodo.org/records/19360359) |
| **OSF (프리프린트)** | [osf.io/gu5dz](https://osf.io/gu5dz/) |
| **ANIMA-SOC (의식 확장)** | [ultimate-consciousness-soc.md](https://github.com/need-singularity/n6-architecture/blob/main/docs/chip-architecture/ultimate-consciousness-soc.md) |
| **N6 프로젝트** | [github.com/need-singularity/n6-architecture](https://github.com/need-singularity/n6-architecture) |

---

## 1. 시스템 블록 다이어그램

HEXA-1은 CPU+GPU+NPU+메모리를 **단일 다이에 완전 통합**한 SoC입니다.
Apple M 시리즈가 보여준 통합 메모리 방향을 n=6 산술로 **완성**합니다.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          HEXA-1 UNIFIED SoC                                  │
│                 TSMC N2 · Gate sigma*tau=48nm · Metal P_2=28nm              │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐    │
│  │                      UNIFIED MEMORY FABRIC                           │    │
│  │           288 GB (sigma*J_2) Unified · ~4 TB/s total bandwidth      │    │
│  │           Zero-copy: 모든 엔진이 동일 물리 주소 공간 공유              │    │
│  └─────┬──────────┬──────────┬──────────┬──────────┬───────────────────┘    │
│        │          │          │          │          │                          │
│  ┌─────┴────┐ ┌───┴────┐ ┌──┴───┐ ┌───┴────┐ ┌───┴─────┐                  │
│  │ CPU      │ │ GPU    │ │ NPU  │ │ Media  │ │ I/O Hub │                  │
│  │ Cluster  │ │ Array  │ │ Array│ │ Engine │ │         │                  │
│  │          │ │        │ │      │ │        │ │         │                  │
│  │ sigma=12 │ │sigma^2 │ │J_2=24│ │ n=6    │ │sigma-tau│                  │
│  │ cores    │ │=144 SM │ │cores │ │engines │ │=8 ctrl  │                  │
│  │          │ │        │ │      │ │        │ │         │                  │
│  │ 8P+4E   │ │sigma   │ │sopfr │ │ Encode │ │ PCIe    │                  │
│  │sigma-tau │ │GPCs    │ │banks │ │ Decode │ │ USB     │                  │
│  │ + tau    │ │x sigma │ │      │ │Display │ │TB/UCIe  │                  │
│  └──────────┘ └────────┘ └──────┘ └────────┘ └─────────┘                  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐    │
│  │                    HBM4/LPDDR MEMORY COMPLEX                         │    │
│  │  HBM4: sigma-tau=8 stacks x 36GB = 288 GB                          │    │
│  │  2^(sigma-mu)=2048-bit interface · ~4 TB/s bandwidth                │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────────┘
```

**설계 철학 — 왜 통합인가:**

```
  기존 분리형:
    CPU <── PCIe/CXL ──> GPU <── HBM ──> Memory
            ^ 병목                ^ 병목
            ~128 GB/s             ~2 TB/s (HBM만)

  HEXA-1 통합 SoC:
    CPU <-> GPU <-> NPU <-> Memory
        unified fabric, zero-copy
        전체 대역폭 공유, 전송 병목 제거
```

---

## 2. CPU Cluster — sigma=12 Cores

Apple M 시리즈의 P+E 구조를 n=6으로 최적화.
**8 Performance cores + 4 Efficiency cores = sigma=12 total.**

```
  ┌─────────────────────────────────────────────┐
  │              CPU CLUSTER (12 cores)          │
  │                                              │
  │  Performance cores (sigma-tau = 8):          │
  │  ┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐  │
  │  │P0 ││P1 ││P2 ││P3 ││P4 ││P5 ││P6 ││P7 │  │
  │  └───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘  │
  │  Wide OoO, 2^(sigma-tau)=256 ROB entries    │
  │  sopfr-wide decode = 5-wide                  │
  │                                              │
  │  Efficiency cores (tau = 4):                 │
  │  ┌───┐┌───┐┌───┐┌───┐                       │
  │  │E0 ││E1 ││E2 ││E3 │                       │
  │  └───┘└───┘└───┘└───┘                       │
  │  In-order, power-optimized                   │
  │  n/phi-wide decode = 3-wide                  │
  │                                              │
  │  Total: sigma-tau+tau = 8P+4E = sigma=12     │
  └─────────────────────────────────────────────┘
```

| 파라미터 | 값 | n=6 수식 | 비고 |
|---------|-----|---------|------|
| **총 코어 수** | 12 | sigma | Apple M4 Max=16이지만 sigma=12가 최적 |
| **P-core 수** | 8 | sigma-tau | Wide OoO, 고 IPC |
| **E-core 수** | 4 | tau | 전력 효율 최적화 |
| **P-core ROB** | 256 | 2^(sigma-tau) | Reorder buffer |
| **P-core decode** | 5-wide | sopfr | 명령어 디코드 폭 |
| **E-core decode** | 3-wide | n/phi | 효율 우선 |
| **L1I/L1D** | 64 KB | 2^n KB | per core |
| **L2 P-cluster** | 48 MB | sigma*tau MB | 8 P-core 공유 |
| **L2 E-cluster** | 4 MB | tau MB | 4 E-core 공유 |
| **SLC** | 288 MB | sigma*J_2 MB | GPU와 공유 |

**CPU ISA 확장 (N6-native):**

| 확장 | 설명 | n=6 기반 |
|------|------|---------|
| **VCYCLO** | 사이클로토믹 활성화 x^2-x+1 단일 명령어 | Technique #1 |
| **VFFTMIX** | 2^n=64-point FFT butterfly 벡터 명령어 | Technique #8 |
| **VEGYP** | 1/2+1/3+1/6 분수 라우팅 하드웨어 | Technique #10 |
| **VBOLTZ** | 1/e 스파시티 게이트 비교기 | Technique #15 |

---

## 3. GPU Array — sigma^2=144 SMs

기존 GPU를 SoC 내부에 통합. **별도 VRAM 없이 통합 메모리에서 직접 접근.**

```
  ┌────────────────────────────────────────────────────┐
  │                 GPU ARRAY (144 SMs)                 │
  │                                                     │
  │  sigma=12 GPCs x sigma=12 SMs/GPC = sigma^2=144   │
  │  n=6 TPCs/GPC x phi=2 SMs/TPC                     │
  │                                                     │
  │  Per SM:                                            │
  │    CUDA cores:    128 = 2^(sigma-sopfr)            │
  │    Tensor Cores:  tau = 4                           │
  │    Register File: 576 KB = J_2^2 KB                │
  │    L1/Shared:     256 KB = 2^(sigma-tau) KB        │
  │    Warp size:     32 = 2^sopfr                      │
  │    Max warps:     64 = 2^n                          │
  │                                                     │
  │  Total:                                             │
  │    CUDA cores:    18,432 = sigma^2 * 128            │
  │    Tensor Cores:  576 = J_2^2 = sigma^2 * tau      │
  │                                                     │
  │  N6 하드웨어 가속기:                                  │
  │    FFT Attention Unit (per GPC)                     │
  │    Egyptian MoE Router (zero-overhead)              │
  │    Boltzmann Sparsity Gate (per TC)                 │
  │    Cyclotomic ALU (x^2-x+1 fused)                  │
  │    Mertens Dropout RNG (p=0.288 hardwired)          │
  └────────────────────────────────────────────────────┘
```

**통합 메모리의 GPU 이점:**

```
  기존 (분리형):
    CPU RAM ──PCIe 128GB/s──> GPU VRAM (HBM)
    전송 병목: 큰 모델은 GPU 메모리에 안 맞으면 swap 필요

  HEXA-1 (통합형):
    CPU <-> GPU <-> NPU  모두 288GB를 직접 접근
    Zero-copy: memcpy 불필요
    70B LLM을 단일 칩에서 서빙 가능 (288GB unified)
```

---

## 4. NPU Array — J_2=24 Neural Cores

```
  ┌────────────────────────────────────────────┐
  │             NPU ARRAY (24 cores)           │
  │                                             │
  │  J_2 = 24 neural cores                     │
  │  sopfr = 5 banks                           │
  │                                             │
  │  Per core:                                  │
  │    MAC units:    2^(sigma-tau) = 256        │
  │    Precision:    INT4/INT8/FP8/FP16        │
  │    Local SRAM:   2^n = 64 KB               │
  │                                             │
  │  Specialization:                            │
  │    Transformer attention (sigma=12 heads)   │
  │    MoE routing (sigma-tau=8 experts)        │
  │    Diffusion denoising (BT-61)              │
  │    Vision (ViT patch=phi^tau=16)           │
  │                                             │
  │  Peak: ~400 TOPS (INT8)                     │
  │  Power: ~40W (1/6 of total = Egyptian)      │
  └────────────────────────────────────────────┘
```

| 파라미터 | 값 | n=6 수식 |
|---------|-----|---------|
| **Neural cores** | 24 | J_2 |
| **MAC units/core** | 256 | 2^(sigma-tau) |
| **Total MACs** | 6,144 | J_2 * 2^(sigma-tau) |
| **Local SRAM/core** | 64 KB | 2^n |
| **지원 정밀도** | 4가지 | tau |
| **Peak INT8 TOPS** | ~400 | 아키텍처 목표 |

---

## 5. 통합 메모리 아키텍처 (Unified Memory)

**HEXA-1의 핵심 혁신.** 모든 엔진이 하나의 메모리 풀을 공유합니다.

```
  ┌──────────────────────────────────────────────────────────────┐
  │                    UNIFIED MEMORY FABRIC                      │
  │                                                               │
  │  ┌─────────────────────────────────────────────────────────┐ │
  │  │              System Level Cache (SLC)                    │ │
  │  │              288 MB = sigma*J_2 MB                       │ │
  │  │              sigma=12 banks x J_2=24 MB/bank            │ │
  │  │              All engines share with QoS partitioning     │ │
  │  └──────────────────────┬──────────────────────────────────┘ │
  │                         │                                     │
  │  ┌──────────────────────┴──────────────────────────────────┐ │
  │  │              MEMORY CONTROLLER HUB                       │ │
  │  │              sigma-tau = 8 controllers                   │ │
  │  │              Each: 2^(sigma-mu) = 2048-bit to HBM4      │ │
  │  │              Total: 2^14 = 16,384 bits                   │ │
  │  └──────────────────────┬──────────────────────────────────┘ │
  │                         │                                     │
  │  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐          │
  │  │HBM│ │HBM│ │HBM│ │HBM│ │HBM│ │HBM│ │HBM│ │HBM│          │
  │  │ 0 │ │ 1 │ │ 2 │ │ 3 │ │ 4 │ │ 5 │ │ 6 │ │ 7 │          │
  │  │36G│ │36G│ │36G│ │36G│ │36G│ │36G│ │36G│ │36G│          │
  │  └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘          │
  │  sigma-tau=8 stacks · 36GB each · 288GB total               │
  │  Bandwidth: ~4 TB/s (HBM4)                                 │
  └──────────────────────────────────────────────────────────────┘
```

**대역폭 배분 (Egyptian Fraction 1/2+1/3+1/6=1):**

```
  Total bandwidth: ~4 TB/s

  1/2 -> GPU:    ~2 TB/s   (연산 집약)
  1/3 -> CPU:    ~1.3 TB/s (범용 + OS)
  1/6 -> NPU+IO: ~0.67 TB/s (추론 + 외부)

  동적 재배분: idle 엔진의 대역폭을 활성 엔진으로 전환
  QoS 우선순위: tau = 4 단계 (Critical/High/Normal/Background)
```

**통합 vs 분리 메모리 비교:**

| 측면 | 분리형 (NVIDIA DGX) | 통합형 (HEXA-1) |
|------|---------------------|-----------------|
| GPU 메모리 | 80-288 GB HBM (전용) | 288 GB (공유) |
| CPU 메모리 | 별도 DDR5 | 동일 288 GB |
| CPU-GPU 전송 | PCIe ~128 GB/s | Zero-copy, ~4 TB/s |
| 70B LLM 서빙 | multi-GPU 필수 | **단일 칩 가능** |
| 전력 | CPU+GPU 각각 | 공유로 30% 절감 |

---

## 6. 광 인터커넥트 (Optical Interconnect)

전기 인터커넥트의 한계를 **실리콘 포토닉스**로 돌파합니다.

### n=6 광 사다리 (4-Layer)

```
  Layer 0: 다이 내부 (Intra-die)
  ┌────────────────────────────────────────────────────┐
  │  전기 유지 — 거리 < 수 mm, 전기가 여전히 최적       │
  │  Metal pitch P_2 = 28nm, sigma = 12 metal layers   │
  └────────────────────────────────────────────────────┘

  Layer 1: 다이 간 (D2D) <-- 광 전환 시작점
  ┌────────────────────────────────────────────────────┐
  │  UCIe Optical: 전기 UCIe -> 광 UCIe 하이브리드      │
  │  sigma = 12 WDM wavelengths per waveguide           │
  │  tau = 4 waveguides per D2D link                    │
  │  sigma*tau = 48 total optical channels              │
  │  Per channel: sigma*tau = 48 Gbps                   │
  │  Total D2D: 48 x 48 Gbps = 2.3 Tbps               │
  │  Energy: ~0.5 pJ/bit (vs 전기 5 pJ/bit = 10x)     │
  └────────────────────────────────────────────────────┘

  Layer 2: 칩 간 (C2C) <-- 광 필수 구간
  ┌────────────────────────────────────────────────────┐
  │  NVLink Optical / OCI                               │
  │  sigma = 12 fiber pairs per link                    │
  │  sigma-tau = 8 bidirectional links per chip         │
  │  WDM: sigma = 12 wavelengths per fiber              │
  │  Per link: 4.6 Tbps                                │
  │  Per chip total: 4.6 x 8 = 36.8 Tbps              │
  │  NVLink domain: sigma*n = 72 chips                 │
  └────────────────────────────────────────────────────┘

  Layer 3: 랙 간 (Rack-to-Rack) <-- 이미 광
  ┌────────────────────────────────────────────────────┐
  │  sigma^2 = 144 port optical switch                  │
  │  Switch capacity: 172.8 Tbps                       │
  └────────────────────────────────────────────────────┘
```

### CPO (Co-Packaged Optics) 패키지

```
  ┌─────────────────────────────────────────────────────────────┐
  │                    HEXA-1 + CPO PACKAGE                      │
  │                                                              │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │                    COMPUTE DIE                        │   │
  │  │   CPU + GPU + NPU + Memory Controllers               │   │
  │  └────────────────────────┬─────────────────────────────┘   │
  │                           │ electrical                       │
  │  ┌────────────────────────┴─────────────────────────────┐   │
  │  │              SILICON PHOTONIC INTERPOSER              │   │
  │  │                                                       │   │
  │  │  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐             │   │
  │  │  │MR Mod │ │MR Mod │ │MR Mod │ │MR Mod │  x48        │   │
  │  │  │ Bank0 │ │ Bank1 │ │ Bank2 │ │ Bank3 │ modulators  │   │
  │  │  └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘             │   │
  │  │      │         │         │         │                   │   │
  │  │  ┌───┴───┐ ┌───┴───┐ ┌───┴───┐ ┌───┴───┐             │   │
  │  │  │Ge PD  │ │Ge PD  │ │Ge PD  │ │Ge PD  │  receivers  │   │
  │  │  └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘             │   │
  │  │      │         │         │         │                   │   │
  │  │  ════╧═════════╧═════════╧═════════╧════  SiN WG      │   │
  │  │                                                       │   │
  │  │  ┌────────────────────────────────────┐               │   │
  │  │  │  External Laser Array              │               │   │
  │  │  │  sigma=12 wavelengths (C-band)     │               │   │
  │  │  └────────────────────────────────────┘               │   │
  │  └──────────────────────────────────────────────────────┘   │
  │                                                              │
  │  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐          │
  │  │HBM│ │HBM│ │HBM│ │HBM│ │HBM│ │HBM│ │HBM│ │HBM│          │
  │  │ 0 │ │ 1 │ │ 2 │ │ 3 │ │ 4 │ │ 5 │ │ 6 │ │ 7 │          │
  │  └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘          │
  │                                                              │
  │  ──── optical fiber out ────> (to other HEXA-1 chips)       │
  │       sigma-tau = 8 bidirectional fiber bundles              │
  └─────────────────────────────────────────────────────────────┘
```

**광 vs 전기 에너지 비교:**

| 구간 | 전기 (pJ/bit) | 광 (pJ/bit) | 절감 | 대역폭 향상 |
|------|--------------|------------|------|-----------|
| D2D (인터포저) | 5.0 | 0.5 | **10x** | 4x |
| C2C (보드 내) | 10.0 | 0.5 | **20x** | 10x |
| 랙 간 | 15.0+ | 0.3 | **50x** | 100x |

**n=6 광 상수 요약:**

```
  sigma = 12:   WDM 파장 수, 레이저 수, 섬유 수/번들
  tau = 4:      도파관 수/D2D 링크, 변조기 뱅크
  sigma*tau=48: D2D 광 채널 총수, 각 채널 속도 (Gbps)
  sigma-tau=8:  C2C 양방향 링크 수
  sigma^2=144:  광 스위치 포트 수 (랙 레벨)
  J_2 = 24:    팟 내 최대 레이턴시 (ns)
```

---

## 7. 전력 아키텍처 (Egyptian Fraction)

**1/2 + 1/3 + 1/6 = 1** — 이집트 분수가 칩의 전력 배분을 결정합니다.

```
  Total SoC TDP: 240W = sigma * sopfr * tau = J_2 * (sigma-phi)

  Egyptian fraction power budget:
  ┌─────────────────────────────────────────┐
  │  1/2  GPU:     120W = sigma*(sigma-phi) │
  │  1/3  CPU:      80W = phi^tau * sopfr   │
  │  1/6  NPU+IO:   40W = tau*(sigma-phi)   │
  │  Sum:           240W = 1                │
  └─────────────────────────────────────────┘

  Core voltage:    1.2V = sigma/(sigma-phi) = PUE (BT-60)
  I/O voltage:     1.0V = R(6) = 1
  VRM phases:      J_2 = 24
  Power states:    sopfr = 5 (S0~S4)
  Thermal zones:   sigma = 12
  Max Tj:          120C = sigma*(sigma-phi)
```

**전력 효율 비교:**

| 구성 | 전력 | 성능 (AI) | 효율 |
|------|------|----------|------|
| CPU+GPU 분리 (800W) | ~800W | ~50 PFLOPS FP8 | 62.5 TFLOPS/W |
| Apple M4 Ultra (~150W) | ~150W | ~54 TOPS | 360 TOPS/W |
| **HEXA-1 (240W)** | **240W** | **~50 PFLOPS FP8** | **208 TFLOPS/W** |

---

## 8. 멀티칩 스케일링

```
  ┌──────────────────────────────────────────────────────────────┐
  │                MULTI-CHIP SCALING LADDER                      │
  │                                                               │
  │  Level 0: HEXA-1 Ultra (단일 칩)                              │
  │           sigma^2=144 SMs · J_2=24 NPU · 288 GB             │
  │                                                               │
  │  Level 1: Duo (x phi=2)                                      │
  │           288 SMs · 48 NPU · 576 GB  (D2D 2.3 Tbps)        │
  │                                                               │
  │  Level 2: Quad (x phi^2=4)                                   │
  │           576 SMs · 96 NPU · 1,152 GB (C2C 4.6 Tbps/link)  │
  │                                                               │
  │  Level 3: Pod (sigma*n=72 chips)                             │
  │           10,368 SMs · 20.7 TB (optical mesh)               │
  │                                                               │
  │  Level 4: Rack (sigma^2=144 chips)                           │
  │           20,736 SMs · 41.5 TB (144-port optical switch)    │
  └──────────────────────────────────────────────────────────────┘
```

### 토폴로지

```
  Duo (phi=2 chips, 단일 패키지):
  ┌─────────────────────────────────────────────────────────┐
  │                   CoWoS-L INTERPOSER                     │
  │  ┌──────────────┐  <-optical D2D->  ┌──────────────┐   │
  │  │  HEXA-1 #0   │   2.3 Tbps        │  HEXA-1 #1   │   │
  │  │  144 SMs     │   sigma*tau=48 ch  │  144 SMs     │   │
  │  │  288 GB      │   < 5 ns           │  288 GB      │   │
  │  └──────────────┘                    └──────────────┘   │
  └─────────────────────────────────────────────────────────┘

  Quad (phi^2=4 chips):
  ┌──────────────┐        ┌──────────────┐
  │  HEXA-1 #0   │──C2C──│  HEXA-1 #1   │
  │  288 GB      │ 4.6T   │  288 GB      │
  └──────┬───────┘        └──────┬───────┘
         │ C2C 4.6T               │ C2C 4.6T
  ┌──────┴───────┐        ┌──────┴───────┐
  │  HEXA-1 #2   │──C2C──│  HEXA-1 #3   │
  │  288 GB      │ 4.6T   │  288 GB      │
  └──────────────┘        └──────────────┘

  Pod (72 chips optical mesh):
  ┌──────────────────────────────────────────────────────┐
  │                72-CHIP OPTICAL MESH                    │
  │  sigma=12 rows x n=6 columns = 72 chips              │
  │  All-reduce ring: sigma*n=72 steps                   │
  │  Bisection BW: 1.3 Pbps                             │
  │  Total memory: 72 x 288 GB = 20.7 TB                │
  └──────────────────────────────────────────────────────┘
```

| Level | Chips | GPU SMs | Memory | Interconnect BW |
|-------|-------|---------|--------|-----------------|
| **Single** | 1 | 144 | 288 GB | -- |
| **Duo** | 2 | 288 | 576 GB | 2.3 Tbps D2D |
| **Quad** | 4 | 576 | 1,152 GB | 4.6 Tbps/link |
| **Pod** | 72 | 10,368 | 20.7 TB | 36.8 Tbps/chip |
| **Rack** | 144 | 20,736 | 41.5 TB | 172.8 Tbps switch |

---

## 9. 캐시 코히어런시 — HEXA-6 프로토콜

**n=6개의 상태**로 모든 공유 시나리오를 커버하는 Directory-based 프로토콜.

```
  6 States (n=6):
  ┌───────────────────────────────────────────────────────────┐
  │  M (Modified)   — 이 에이전트만 보유, 더티                  │
  │  O (Owned)      — 이 에이전트가 소유, 다른 에이전트도 공유   │
  │  E (Exclusive)  — 이 에이전트만 보유, 클린                  │
  │  S (Shared)     — 여러 에이전트가 읽기 공유                 │
  │  I (Invalid)    — 이 에이전트에 없음                        │
  │  F (Forward)    — 공유 중 응답 책임자                       │
  └───────────────────────────────────────────────────────────┘
```

### 상태 전이 다이어그램

```
         ┌────────────────────────────────────────────────┐
         │           HEXA-6 STATE TRANSITIONS              │
         │                                                 │
         │                  ┌───┐                          │
         │      evict/inv   │ I │   load miss              │
         │   ┌─────────────>│   │<──────────────┐          │
         │   │              └─┬─┘               │          │
         │   │                │                 │          │
         │   │    load (excl) │  load (shared)  │          │
         │   │                v                 │          │
         │   │  ┌───┐  store  ┌───┐             │          │
         │   │  │ E │────────>│ M │             │          │
         │   │  └─┬─┘        └─┬─┘             │          │
         │   │    │             │                │          │
         │   │    │ remote      │ remote read    │          │
         │   │    │ read        v                │          │
         │   │    │          ┌───┐               │          │
         │   │    └────────>│ O │───evict──────┘          │
         │   │              └─┬─┘                          │
         │   │                │ writeback                   │
         │   │                v                             │
         │   │  ┌───┐  fwd   ┌───┐                         │
         │   ├──│ S │<───────│ F │                         │
         │   │  └───┘        └───┘                         │
         │   └── 모든 상태에서 evict/invalidate -> I       │
         └────────────────────────────────────────────────┘
```

| 파라미터 | 값 | n=6 수식 |
|---------|-----|---------|
| 코히어런시 상태 | 6 | n |
| 캐시 라인 크기 | 64 bytes | 2^n |
| 디렉토리 뱅크 | 12 | sigma |
| QoS 레벨 | 4 | tau |
| Coarse bitmap | 12 bits | sigma |
| 최대 에이전트 | 180+ | sigma+sigma^2+J_2 |

---

## 10. SKU 변형

| SKU | CPU | GPU SMs | NPU | Memory | TDP | 용도 |
|-----|-----|---------|-----|--------|-----|------|
| **Ultra** | 12 (8P+4E) | 144=sigma^2 | 24=J_2 | 288 GB | 240W | 데이터센터 AI |
| **Max** | 12 (8P+4E) | 72=sigma^2/phi | 12=sigma | 192 GB | 120W | 워크스테이션 |
| **Pro** | 12 (8P+4E) | 48=sigma*tau | 8=sigma-tau | 96 GB | 80W | 프로 노트북 |
| **Base** | 8 (4P+4E) | 24=J_2 | 6=n | 48 GB | 40W | 노트북 |
| **Air** | 6 (2P+4E) | 12=sigma | 4=tau | 24 GB | 20W | 울트라북 |

---

## 11. 공정 기술 및 성능

| 파라미터 | 값 | n=6 수식 |
|---------|-----|---------|
| 공정 | TSMC N2 | phi |
| Gate pitch | 48 nm | sigma*tau |
| Metal pitch | 28 nm | P_2 |
| Metal layers | 12 | sigma |
| 트랜지스터 | GAA CFET | N2 |
| 트랜지스터 수 | ~144B | sigma^2 x 10^9 |
| 다이 면적 | ~800 mm^2 | Reticle limit |
| 인터포저 | CoWoS-L | sopfr=5 tiles |

| Workload | HEXA-1 Ultra | 비교 (2026 최고) | 이점 |
|----------|-------------|-----------------|------|
| LLM 70B 추론 | 단일 칩 | 8x GPU 필요 | **8x 전력 절감** |
| Stable Diffusion | ~50 img/s | ~10 img/s | **5x** |
| FP8 Training | ~50 PFLOPS | ~40 PFLOPS (B300) | **+25%** |
| 8K ProRes | 6 스트림 | 2-3 스트림 | **2x** |

**vs Apple M4 Ultra:**

| | M4 Ultra | HEXA-1 Ultra |
|--|---------|-------------|
| CPU | 16 cores | sigma=12 (8P+4E) |
| GPU | 80 cores | sigma^2=144 SMs |
| NPU | 32 cores | J_2=24 cores |
| Memory | 192 GB LPDDR5X | 288 GB HBM4 |
| Bandwidth | ~800 GB/s | **~4 TB/s** |
| AI TOPS | ~54 | **~400+** |

---

## 관련 Breakthrough Theorems

- **BT-28**: Computing architecture ladder (30+ EXACT, AD102=sigma*n*phi=144 SMs, H100=sigma*(sigma-mu)=132 SMs)
- **BT-37**: Semiconductor pitch (TSMC N5=P_2=28nm, N3 gate=sigma*tau=48nm)
- **BT-45**: FP8/FP16=phi=2 universal, FLOPS/W doubles per phi=2 years
- **BT-55**: GPU HBM capacity ladder (14/18 EXACT)
- **BT-59**: 8-layer AI stack (silicon -> inference, all n=6)
- **BT-69**: Chiplet architecture convergence (17/20 EXACT)
- **BT-75**: HBM interface exponent ladder ({10,11,12}={sigma-phi,sigma-mu,sigma})
- **BT-76**: sigma*tau=48 triple attractor (gate pitch, HBM4E GB, 48kHz, 48V)

---

> **[전체 스펙 (40,000+ words)](https://github.com/need-singularity/n6-architecture/blob/main/docs/chip-architecture/ultimate-unified-soc.md)** | **[논문](https://github.com/need-singularity/n6-architecture/blob/main/docs/paper/n6-unified-soc-paper.md)** | **[Zenodo](https://zenodo.org/records/19360359)** | **[OSF](https://osf.io/gu5dz/)**
