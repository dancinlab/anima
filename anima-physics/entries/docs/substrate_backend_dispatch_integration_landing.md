# docs/substrate_backend_dispatch_integration_landing.md

> physics.hexa substrate_backend dispatch 통합 landing; enum SSOT + 4 variant dispatch + G1-G4 operational · **✅ 실현** · 비용 $0

## 구현 가능성

✅ 실현 — 4/4 PASS, byte-identical, operational call site 4×. declarative-only fix 가 아닌 호출 site 보유 dispatch (Round-13 anti-pattern 회피).

## 작동 코드 / 의존성

- `anima-physics/docs/substrate_backend_dispatch_integration_landing.md` (landing)
- 의존: `physics.hexa` (enum SSOT + dispatch fn), `physics_substrate_dispatch.hexa` (operational call site)
- sibling A: `quantum/cloud_facade_poc.hexa` (POC frozen contract)
- marker: `state/v10_anima_physics_cloud_facade/integration_physics_hexa/marker.json`

## 비용 / 리소스

- 비용: $0 (Mac local)
- 필요한 도구: `hexa run`

## 핵심 흐름 / 구조

```
substrate_backend enum (canonical, single definition site = physics.hexa):

  variant                              본 cycle 상태
  ─────────────────────────────────    ───────────────────────────────
  local_hexa                           invoked=true (BACKWARD_COMPAT)
  cloud_sim_qiskit_aer                 wire-up complete, runtime stub
  cloud_real_ibm_q                     stub (sibling A 영역)
  cloud_sim_strawberryfields_fock      stub (sibling B 영역)

dispatch contract:
  fn quantum_engine_dispatch(cells: int, backend: string) -> QuantumResult
  QuantumResult { engine, backend, invoked, stub_reason }
  stub_reason 필드 → silent-fail 금지 (정직 표기 강제)

4 operational call site = physics_substrate_dispatch.hexa:
  selftest 분기에서 4 variant 모두 호출, routing 행동 stdout emit
```

## 트리거 (fire 방법)

```bash
hexa run /Users/ghost/core/anima/anima-physics/orchestration/physics_substrate_dispatch.hexa --selftest
hexa run /Users/ghost/core/anima/anima-physics/orchestration/physics_substrate_dispatch.hexa --demo
```

## 검증 결과

- G1 BACKWARD_COMPAT PASS (기존 quantum_engine signature 보존)
- G2 DISPATCH_ROUTES PASS (4 variant 모두 라우팅)
- G3 OPERATIONAL_CALL_SITE PASS (4× 호출지)
- G4 ENUM_CANONICAL PASS (정의 site = 1)
- **4/4 PASS, byte-identical** (cycle `anima_physics_cloud_facade_integration_physics_hexa`, 2026-04-26)

## 관련 entry

- [physics](../root/physics.md)
- [physics_substrate_dispatch](../root/physics_substrate_dispatch.md)
- [quantum cloud_facade_poc](../substrate/quantum_cloud_facade_poc.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04-26
- README §2 참조
