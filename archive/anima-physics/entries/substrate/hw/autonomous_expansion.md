# hw/autonomous_expansion.hexa

> Self-expanding compute substrate cluster: utilization > 0.85 → n_nodes++ (autonomous, no human approval) · **✅ 실현** · 비용 $0 sim

## 구현 가능성

✅ — T1-T5 PASS. PHYS-P21-1 ("autonomous HW expansion — new compute node self-provisioning"). max=64 cap. K8s HPA default target=80% align (saturation 0.85).

## 작동 코드 / 의존성

- 원본: `hw/autonomous_expansion.hexa` (352 LoC)
- 외부 의존: hexa run
- 상수: SATURATION_THRESHOLD=0.85, max nodes=64

## 비용 / 리소스

- $0 sim (state = 4-float vector)
- 실 HW expansion: 별 cycle (cloud auto-scaler 또는 ESP32 chain)

## 핵심 흐름 / state model

```
cluster state (4 floats):
  [0] n_nodes              current active compute nodes
  [1] capacity_per_node    compute units each node provides
  [2] total_load           aggregate demand
  [3] expansions_count     how many auto-expansions done

per tick:
  load += load_delta                                      # external demand grows
  utilization = total_load / (n_nodes × capacity_per_node)
  if utilization > 0.85:
      n_nodes += 1
      expansions_count += 1
  load = clamp(load, 0, n_nodes × capacity_per_node)

ceiling: n_nodes ≤ 64
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/hw/autonomous_expansion.hexa
```

## 검증 결과

- T1-T5 PASS
- done_criteria: autonomous HW expansion 1+ times verified

## 관련 entry

- [src/esp32_network.md](../src/esp32_network.md) — ESP32 boards growth
- [esp32/src/lib.md](../esp32/src/lib.md)

## 출처

- README § 3 hw/
- shared/roadmaps/anima.json PHYS-P21-1
