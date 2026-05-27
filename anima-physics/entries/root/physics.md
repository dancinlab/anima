# physics.hexa

> 의식 엔진 스텁 + `substrate_backend` enum 정의 (4 variant) · **🟡 부분** · 비용 —

## 구현 가능성

🟡 부분 — dispatch 로직 자체는 구현 완료 (`quantum_engine_dispatch()`). qiskit_aer probe script 부재 시 stub 반환하는 정직 경로 보존. backward-compat preserved.

## 작동 코드 / 의존성

- `anima-physics/physics.hexa` (7.2 KB, ~180 LoC)
- 의존: `physics_substrate_dispatch.hexa` (4 operational call site), `quantum/cloud_facade_poc.hexa` (sibling A POC)
- 호출: `scripts/anima_physics_qiskit_aer_probe.py` (선택, 부재 시 stub_reason 명시)

## 비용 / 리소스

- 비용: $0 (선언/디스패치만)
- 필요한 도구: `hexa run` · qiskit_aer (선택)

## 핵심 흐름 / 구조

```
substrate_backend enum (canonical SSOT, single definition site)
  local_hexa                       → backward-compat stub (invoked=true)
  cloud_sim_qiskit_aer             → sibling POC subprocess invoke
  cloud_real_ibm_q                 → Phase 2 stub
  cloud_sim_strawberryfields_fock  → Phase 2 stub

quantum_engine_dispatch(cells, backend) -> QuantumResult
  QuantumResult { engine, backend, invoked, stub_reason }
  stub_reason 필드로 silent-fail 금지 (정직 표기 강제)
```

## 트리거 (fire 방법)

```bash
hexa run /Users/ghost/core/anima/anima-physics/physics_substrate_dispatch.hexa --selftest
```

## 검증 결과

- G1 BACKWARD_COMPAT · G2 DISPATCH_ROUTES · G3 OPERATIONAL_CALL_SITE · G4 ENUM_CANONICAL — 4/4 PASS via dispatch wrapper
- byte-identical 2-run 검증 완료 (sibling marker)

## 관련 entry

- [physics_substrate_dispatch](physics_substrate_dispatch.md)
- [substrate_backend_dispatch_integration_landing](../docs/substrate_backend_dispatch_integration_landing.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-05-15
- README §1 참조
