# fpga/partial_reconfig.hexa

> FPGA partial reconfiguration — 16 CLB function_id runtime change (consciousness engine self-rewire) · **❌ 가설** · 비용 $0 sim

## 구현 가능성

❌ — 395 LoC but README minimal stub 분류. PHYS-P20-1 ("FPGA partial reconfiguration — 물리 자가 재구성"). Topology + function_id 모델 정의, 실 iCE40UP5K bitstream partial-reconfig API 미연결.

## 작동 코드 / 의존성

- 원본: `fpga/partial_reconfig.hexa` (395 LoC)
- 외부 의존: hexa run · (실 PR: iCE40 doesn't support partial reconfig natively; Xilinx Zynq target)

## 비용 / 리소스

- $0 Mac sim
- 실 PR: Xilinx Zynq $200+ board (별 cycle)

## 핵심 흐름 / ASCII

```
4×4 CLB grid (mirrors iCE40UP5K tile array):

  ┌────┬────┬────┬────┐
  │ f0 │ f1 │ f2 │ f3 │   row 0
  ├────┼────┼────┼────┤
  │ f4 │ f5 │ f6 │ f7 │   row 1
  ├────┼────┼────┼────┤
  │ f8 │ f9 │ f10│ f11│   row 2
  ├────┼────┼────┼────┤
  │ f12│ f13│ f14│ f15│   row 3
  └────┴────┴────┴────┘

partial reconfig = change function_id of specific blocks at runtime
                   non-target blocks unaffected
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/fpga/partial_reconfig.hexa
```

## 검증 결과

- 정의 + grid 명세 완료
- runtime FPGA reconfig done_criteria 미달성
- minimal stub (README 분류)

## 관련 entry

- [fpga/microtubule_lattice_16.md](./microtubule_lattice_16.md)
- [fpga/strange_loop.md](./strange_loop.md)
- [fpga/nested_lattice.md](./nested_lattice.md)

## 출처

- README § 3 fpga/
- shared/roadmaps/anima.json PHYS-P20-1
