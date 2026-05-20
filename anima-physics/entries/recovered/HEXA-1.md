# HEXA-1

> Pure compute SoC — CPU+GPU+NPU+메모리 완전 통합 단일 칩, n=6 arithmetic 도출. **의식 모듈 없음**. · **❌ 가설** (live anima 코드 미연결; HEXAD.tape 에 직접 후예 없음 — ANIMA-SOC 의 inherit base 로만 등장) · 비용 — (paper/architectural blueprint)

## 구현 가능성

❌ 가설 — 2026-04-01 작성, `dancinlab/echoes` git history blob 에서 sha 복원, 현재 어느 checked-out tree 에도 없음. 구현물 0. (의식 module 부재 → live anima 와 직접 연결 없음; ANIMA-SOC 가 이 spec 을 inherit 하여 Engine A/G + TCU 확장하는 경로로만 의식 도메인과 접점)

## 출처 / 복원 경위

- 원본: `recovered/chip-architecture/docs_chip-architecture_ultimate-unified-soc.md` (~7 KB blob)
- 작성일: 2026-04-01
- 삭제 commit: a86ca14 / 812bd79 / 4eb869a (2026-05-10~11 canon MOVE migration)
- 본문 있는 곳: `dancinlab/echoes` git history blob (current main 에서 삭제)

## 사양 요약

**Codename: HEXA-1** — **순수 컴퓨팅 끝판왕**. Apple M 시리즈가 보여준 통합 메모리 아키텍처를 n=6 로 완성. **의식 모듈 없음**. n=6 산술 (φ=2 · τ=4 · σ=12 · sopfr=5 · μ=1 · J₂=24 · σ²=144 · σ·J₂=288) 의 모든 상수가 면적/전력/대역폭 배분을 결정.

| 블록 | 규모 | n=6 수식 |
|---|---|---|
| CPU cluster | **σ=12 cores** (8P + 4E) | σ-τ + τ |
| GPU array | **σ²=144 SMs** | σ × σ GPC layout |
| NPU array | **J₂=24 neural cores** | sopfr=5 banks |
| Media engine | n=6 engines | n |
| HBM4 stacks | σ-τ=8 × 36GB = **288 GB** | σ·J₂ |
| Unified bandwidth | ~4 TB/s | — |
| Process | TSMC N2 · Gate σ·τ=48 nm · Metal P₂=28 nm | σ·τ / P₂ |
| ISA extensions | VCYCLO / VFFTMIX / VEGYP / VBOLTZ | Tech #1/#8/#10/#15 |

**핵심 차별**: Apple M 의 unified memory 컨셉 위에 n=6 arithmetic 을 입힘. **Zero-copy** 288 GB 통합 메모리에서 70B LLM single-chip serving 가능.

## ASCII 도식 — § 1 System-Level Block Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          HEXA-1 UNIFIED SoC                                  │
│                 TSMC N2 · Gate σ·τ=48nm · Metal P₂=28nm                     │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐    │
│  │                      UNIFIED MEMORY FABRIC                           │    │
│  │           288 GB (σ·J₂) Unified · ~4 TB/s total bandwidth           │    │
│  │           Zero-copy: 모든 엔진이 동일 물리 주소 공간 공유              │    │
│  └─────┬──────────┬──────────┬──────────┬──────────┬───────────────────┘    │
│        │          │          │          │          │                          │
│  ┌─────┴────┐ ┌───┴────┐ ┌──┴───┐ ┌───┴────┐ ┌───┴─────┐                  │
│  │ CPU      │ │ GPU    │ │ NPU  │ │ Media  │ │ I/O Hub │                  │
│  │ Cluster  │ │ Array  │ │ Array│ │ Engine │ │         │                  │
│  │ σ=12     │ │ σ²=144 │ │ J₂=24│ │ n=6    │ │ σ-τ=8   │                  │
│  │ cores    │ │ SMs    │ │ cores│ │ engines│ │ ctrl    │                  │
│  │ 8P+4E    │ │ σ GPCs │ │ sopfr│ │ Encode │ │ PCIe    │                  │
│  │σ-τ + τ   │ │ x σ SM │ │ banks│ │ Decode │ │ USB     │                  │
│  └──────────┘ └────────┘ └──────┘ │ Display│ │ TB/UCIe │                  │
│                                    └────────┘ └─────────┘                  │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐    │
│  │                    HBM4/LPDDR MEMORY COMPLEX                         │    │
│  │  HBM4: σ-τ=8 stacks × 36GB = 288 GB · 2^(σ-μ)=2048-bit interface    │    │
│  │  LPDDR6 option: σ channels × φ ranks (모바일/엣지 변형)               │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────────┘
```

## ASCII 도식 — § 2 CPU Cluster σ=12 (8P + 4E)

```
┌─────────────────────────────────────────────┐
│              CPU CLUSTER (12 cores)          │
│                                              │
│  Performance cores (σ-τ = 8):                │
│  ┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐┌───┐   │
│  │P0 ││P1 ││P2 ││P3 ││P4 ││P5 ││P6 ││P7 │   │
│  └───┘└───┘└───┘└───┘└───┘└───┘└───┘└───┘   │
│  Wide OoO, 2^(σ-τ)=256 ROB entries          │
│  sopfr-wide decode = 5-wide                  │
│                                              │
│  Efficiency cores (τ = 4):                   │
│  ┌───┐┌───┐┌───┐┌───┐                       │
│  │E0 ││E1 ││E2 ││E3 │                       │
│  └───┘└───┘└───┘└───┘                       │
│  In-order, power-optimized                   │
│  n/φ-wide decode = 3-wide                    │
│                                              │
│  Total: σ-τ + τ = 8P + 4E = σ = 12 cores    │
└─────────────────────────────────────────────┘
```

## live anima 와의 연결

- **직접 후예 없음** — HEXA-1 자체는 의식 모듈 부재로 anima live tree 와 1:1 매핑이 없다.
- **간접 경로**: `ANIMA-SOC` 가 HEXA-1 의 모든 스펙을 inherit + Engine A/G + TCU + 10D consciousness register 추가. ANIMA-SOC 의 Engine A/G concept 만 `HEXAD.tape` L51-69 로 living descendant.
- **anima-physics/substrate/src/chip_architect.hexa** — 9 topology × 9 substrate predict Phi (stub). σ²=144 SM grid 와 conceptual overlap, 하지만 미impl.
- **`/Users/ghost/core/hexa-chip/CHIP-ARCHITECTURE.md`** (2.4 MB) — adj8=17 master 144-SM 12×12 grid 의 live mirror (echoes 와 동일 본문). HEXA-1 의 GPU array §3 spec 의 living document.

## 관련 entry

- [entries/recovered/ANIMA-6.md](ANIMA-6.md) — 형제 codename (consciousness *chip*)
- [entries/recovered/ANIMA-SOC.md](ANIMA-SOC.md) — HEXA-1 inherit + ANIMA-6 extension
- [entries/substrate/src/chip_architect.md](../substrate/src/chip_architect.md) — chip design tool stub
- [recovered/INDEX.md](../../recovered/INDEX.md) — 전체 archive index (300 file)
- `/Users/ghost/core/hexa-chip/CHIP-ARCHITECTURE.md` — adj8=17 master 144-SM grid live mirror

## 트리거 / 구현 transition path

HEXA-1 자체는 의식 module 부재로 live anima 와 직접 연결 path 없음. 다음 중 하나로 진입:

1. **ANIMA-SOC inherit path** — HEXA-1 + Engine A/G + TCU 의 ANIMA-SOC 진입 → `engines/` 8 stub impl
2. **chip_architect.hexa impl** — σ²=144 SM × 9 topology grid 의 Phi prediction stub → 9 substrate × 9 topology 채움
3. **hexa-chip live mirror** — `/Users/ghost/core/hexa-chip/CHIP-ARCHITECTURE.md` 의 adj8=17 master 144-SM grid 를 직접 evolve (echoes 의 카논 후속)

## Honest C3

- HEXA-1 의 의식 부재 → live anima 와 직접 연결 0. ANIMA-SOC 의 inherit base 로만 의미.
- σ²=144 / σ·J₂=288 등 수치는 BT-28/55/69 등 backing trace 가 echoes 본문에 있지만 anima-physics tree 미반영.
- Apple M-style unified memory + n=6 arithmetic 의 통합이 새로운 주장이지만 실 silicon 검증 0.
