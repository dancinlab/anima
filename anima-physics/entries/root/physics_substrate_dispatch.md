# physics_substrate_dispatch.hexa

> `physics.hexa::quantum_engine_dispatch()` 의 operational 첫 호출지; 4-gate selftest · **✅ 실현** · 비용 $0 Mac local

## 구현 가능성

✅ 실현 — 4/4 PASS (BACKWARD_COMPAT / DISPATCH_ROUTES / OPERATIONAL_CALL_SITE / ENUM_CANONICAL). byte-identical 2-run. Round-13 declarative-only anti-pattern 회피.

## 작동 코드 / 의존성

- `anima-physics/orchestration/physics_substrate_dispatch.hexa` (12 KB, ~300 LoC)
- 의존: `physics.hexa` (enum SSOT + dispatch fn)
- selftest 분기에서 4 backend variant 모두 호출 → routing 행동 stdout emit

## 비용 / 리소스

- 비용: $0 Mac local
- 필요한 도구: `hexa run`

## 핵심 흐름 / 구조

```
mirror_dispatch(cells, backend) -> LocalDispatchProbe
  BK_LOCAL   → invoked=true, stub_reason=""
  BK_SIM     → script_exists? subprocess invoke : "sibling_probe_script_or_venv_python_absent"
  BK_REAL    → stub_reason="phase_2_ibmq_runtime_api_key_required_sibling_a"
  BK_PHOTON  → stub_reason="photonic_strawberryfields_sibling_b_owned"

4-gate selftest:
  G1 BACKWARD_COMPAT      — 기존 quantum_engine() signature 보존
  G2 DISPATCH_ROUTES      — 4 backend 모두 라우팅
  G3 OPERATIONAL_CALL_SITE — 본 파일이 dispatch 의 first caller
  G4 ENUM_CANONICAL       — enum 정의 site 단일 (physics.hexa)
```

## 트리거 (fire 방법)

```bash
hexa run /Users/ghost/core/anima/anima-physics/orchestration/physics_substrate_dispatch.hexa --selftest
hexa run /Users/ghost/core/anima/anima-physics/orchestration/physics_substrate_dispatch.hexa --demo
```

## 검증 결과

- 4/4 PASS
- byte-identical 2-run 검증
- marker: `state/v10_anima_physics_cloud_facade/integration_physics_hexa/marker.json`

## 관련 entry

- [physics](physics.md)
- [substrate_backend_dispatch_integration_landing](../docs/substrate_backend_dispatch_integration_landing.md)

## 출처 / 작성일

- 원본 파일 작성일: 2026-05-15
- README §1 참조
