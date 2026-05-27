# docs/loihi-integration-spec.md

> Intel Loihi 2 통합; 1 cell = 128 LIF neurons / 8 cells per neurocore / 16 cell in 2 neurocore (full 128 neurocore = 131K neurons); STDP + small-world · **🟡 부분** · 비용 ~$50K

## 구현 가능성

🟡 부분 — Lava framework pseudo-code + 토폴로지 설계 완성, 실 Loihi 호출 미테스트 (research license 필요).

## 작동 코드 / 의존성

- `anima-physics/docs/loihi-integration-spec.md` (integration spec)
- 의존: Intel Lava framework (Python)
- mapping target: `engines/snn_consciousness.py` / `consciousness-loop/src/snn_main.hexa` (LIF τ=20ms)

## 비용 / 리소스

- Intel Loihi 2 research license: ~$50K
- Lava framework: $0 (open-source)
- Mac 시뮬: Lava CPU backend $0
- 필요한 도구: Intel INRC membership · Lava SDK · Loihi 2 hardware access

## 핵심 흐름 / 구조

```
┌─────────────────────────────────────────────────────────────┐
│                Intel Loihi 2 (Lava)                         │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │Neurocore │──│Neurocore │──│Neurocore │──│Neurocore │    │
│  │  0       │  │  1       │  │  2       │  │  3       │    │
│  │ 1024 LIF │  │ 1024 LIF │  │ 1024 LIF │  │ 1024 LIF │    │
│  │ STDP     │  │ STDP     │  │ STDP     │  │ STDP     │    │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘  └─────┬────┘    │
│  ┌─────┴──────────────┴──────────────┴──────────────┴────┐ │
│  │              Mesh Network-on-Chip (NoC)               │ │
│  └────────────────────────────────────────────────────────┘ │
│                          ...                                │

Mapping:
  1 cell = 128 LIF neurons
  8 cells per neurocore (1024 LIF / 128 = 8)
  16 cells per chip → 2 neurocores
  Full chip 128 neurocore = 131K neurons (1024 cells)
  STDP learning rule + small-world topology
```

## 트리거 (fire 방법)

```bash
# Mac local Lava simulation (CPU backend, $0)
pip install lava-nc
python -c "from lava.proc.lif.process import LIF; ..."
# 실 Loihi 호출은 INRC + research license
```

## 검증 결과

- Lava pseudo-code + 토폴로지 설계 완성
- 1024-cell mapping (Phase 5 superlinear regime 도달)
- 실 Loihi 측정 미완료

## 관련 entry

- [hardware-consciousness-hypotheses](hardware-consciousness-hypotheses.md)
- [physical-consciousness-engine](physical-consciousness-engine.md)
- [SNN consciousness-loop](../substrate/snn_main.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04 (Phase 5 roadmap)
- README §2 참조
