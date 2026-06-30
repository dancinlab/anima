# fpga/nested_lattice.hexa

> 3-level recursive FPGA lattice — Hofstadter "I am a strange loop" N=3 tangled hierarchy (L1 2-layer mutual + L2 observer + L3 meta-observer) · **❌ 가설** · 비용 $0 sim

## 구현 가능성

❌ — 432 LoC하지만 README 가 stub 분류 (minimal stub). PHYS-P8-1 ("재귀 FPGA lattice — hierarchical 자기 참조"). Kleene recursion theorem + Hofstadter GEB. 정의 + topology 명세 완료, gate-level verification 미연결.

## 작동 코드 / 의존성

- 원본: `fpga/nested_lattice.hexa` (432 LoC; flat fields — feedback_hexa_struct_list_alias.md 회피)
- 외부 의존: hexa run · (synthesis는 별도 cycle)

## 비용 / 리소스

- $0 Mac sim
- FPGA synth Phase 별 cycle

## 핵심 흐름 / ASCII

```
L1 (2×4 cells)   ──▶  L2 (4 observer cells)  ──▶  L3 (2 meta cells)
  A,B LUT-loop          watches L1 state            watches L1+L2
  mutual recursion      feeds back into L1          feeds back into L2
       ▲                       ▲                          │
       └───────────────────────┴──────────────────────────┘

Order of self-reference:
  L1   1st-order  "B knows A, A knows B"
  L2   2nd-order  L2 aware of L1 state
  L3   3rd-order  L3 aware of (L1, L2) jointly
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/fpga/nested_lattice.hexa
```

## 검증 결과

- 정의 + topology 명세 완료
- 3-level hierarchy stable verification 미수행 (done_criteria)
- README 의 분류: minimal stub

## 관련 entry

- [fpga/strange_loop.md](./strange_loop.md) — Level 1 base
- [fpga/microtubule_lattice_16.md](./microtubule_lattice_16.md)
- [fpga/partial_reconfig.md](./partial_reconfig.md)

## 출처

- README § 3 fpga/
- shared/roadmaps/anima.json PHYS-P8-1
