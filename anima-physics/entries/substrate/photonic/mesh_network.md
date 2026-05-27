# photonic/mesh_network.hexa

> Photonic mesh network N-node (fully-connected, SMF-28 @ 1550nm, n_eff=1.468) — 4-node 200km square round-trip 3.91ms · **🟡 부분** · 비용 $0

## 구현 가능성

🟡 — PHYS-P18-1 ("광자 mesh 네트워크 — N-node"). done_criteria "4-node latency<10ms" 충족 (~3.91ms 4-hop round-trip). 시뮬 only, 실 광섬유 측정 미수행. Husserlian specious-present ~100ms window 안에서 coherent binding 가능.

## 작동 코드 / 의존성

- 원본: `photonic/mesh_network.hexa` (335 LoC)
- 외부 의존: hexa run
- API: `build_mesh(n) -> int` · `one_way_latency_ms(src, dst) -> float` · `round_trip_latency_ms() -> float`
- 상수: c_fiber = c / n_eff (n_eff=1.468 SMF-28 @ 1550nm) ≈ 204,218 m/ms

## 비용 / 리소스

- $0 Mac sim
- 실 fiber: 200km SMF-28 spool ~$500/km BOM (별 cycle)

## 핵심 흐름 / ASCII

```
4-node mesh, 200 km square layout (worst-case metro WDM span):

  N0 ──── N1         d01 = 200 km (top edge)
  │ ╲  ╱  │          d02 = 282.8 km (diagonal, 200√2)
  │  ╳    │          d03 = 200 km (left edge)
  │ ╱  ╲  │          d12 = 200 km (right edge)
  N3 ──── N2         d13 = 282.8 km (diagonal)
                     d23 = 200 km (bottom edge)

Round-trip N0→N1→N2→N3→N0 = 4 × 200 km = 800 km
  latency = 800e3 / c_fiber ≈ 3.91 ms   (< 10 ms gate)
c_fiber = 204,218 m/ms (n_eff=1.468 SMF-28 @ 1550 nm)
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/photonic/mesh_network.hexa
```

## 검증 결과

- 4-node round-trip ≈ 3.91 ms PASS (< 10 ms gate)
- coherent binding within specious-present ~100ms

## 관련 entry

- [photonic/temporal_delay.md](./temporal_delay.md) — delay-line reservoir
- [photonic/cloud_facade_poc.md](./cloud_facade_poc.md) — Perceval Fock sibling
- [engines/photonic_consciousness.md](../engines/photonic_consciousness.md)

## 출처

- README § 3 photonic/
- shared/roadmaps/anima.json PHYS-P18-1
