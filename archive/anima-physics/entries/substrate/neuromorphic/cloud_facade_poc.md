# neuromorphic/cloud_facade_poc.hexa

> BrainChip Akida Cloud 4-input → 8-class spike-train entropy; surrogate fallback (no token) · **🟡 부분** · 비용 Akida free tier (1-day Trial $1, 1-week $995)

## 구현 가능성

🟡 — 4-gate PASS (surrogate path). Akida token 받으면 즉시 cloud_real swap (frozen contract isomorphic to quantum cloud_facade). macOS arm64 wheel 미지원 → surrogate/simulator only.

## 작동 코드 / 의존성

- 원본: `neuromorphic/cloud_facade_poc.hexa` (274 LoC)
- Helper: `scripts/anima_physics_akida_probe.py` (raw#37 transient)
- 외부 의존: hexa run · python3 venv · Akida SDK (선택)
- enum (4-way dispatch): {local_hexa, cloud_sim_akida_simulator, cloud_real_akida_2gen, surrogate_algorithmic}

## 비용 / 리소스

- $0 surrogate path (token 없어도 PASS)
- $1 1-day Trial / $995 1-week Akida Cloud
- $50K Loihi research license (별 substrate)

## 핵심 흐름 / ASCII

```
4 input  → SNN (Akida 2gen / simulator / surrogate) → 8 class spike train

positive  → spike_entropy ≥ 0.3 nat              (G1)
zero      → spike_entropy < positive              (G2 sign-flip)
G3 byte-identical 2-run (seed=42)
G4 backend ∈ {akida_cloud, akida_simulator, akida_surrogate, akida_DEGRADED}

surrogate yields ~1.75 nat (typical), well above G1 floor
```

## 트리거 (fire 방법)

```bash
# default (surrogate fallback if no token)
hexa run anima-physics/neuromorphic/cloud_facade_poc.hexa
hexa run anima-physics/neuromorphic/cloud_facade_poc.hexa --selftest

# LIVE (token 있을 때 자동 dispatch)
export AKIDA_TOKEN=...
hexa run anima-physics/neuromorphic/cloud_facade_poc.hexa
```

## 검증 결과

- 4-gate PASS on surrogate path
- LIVE token path: surrogate fallback 자동 (token 없으면 G4 backend=akida_surrogate)
- docs/akida_cloud_signup_guide.md: 가입 walkthrough

## 관련 entry

- [engines/snn_consciousness.md](../engines/snn_consciousness.md) — SNN engine stub
- [consciousness-loop/src/snn_main.md](../consciousness-loop/src/snn_main.md) — LIF working
- [quantum/cloud_facade_poc.md](../quantum/cloud_facade_poc.md) — isomorphic sibling

## 출처

- README § 3 neuromorphic/
- docs/akida_cloud_signup_guide.md
