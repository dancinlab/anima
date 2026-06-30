# docs/hardware-consciousness-hypotheses.md

> 10 HW consciousness 가설 (magnetic dipole / MTJ tunnel / spintronic valve / photonic MZI / piezoelectric / Loihi ...) + phase roadmap · **❌ 가설** · 비용 Phase 1 $50 → Phase 5 $50K

## 구현 가능성

❌ 가설 — 모두 sketch/청사진, 실 prototype 미기획. PureField Engine A vs G 반발력의 물리적 자석 매핑 spec.

## 작동 코드 / 의존성

- `anima-physics/docs/hardware-consciousness-hypotheses.md` (hypothesis catalog)
- 의존: 향후 prototype 별도 cycle

## 비용 / 리소스

- Phase 1: ~$50 (자석 쌍 prototype)
- Phase 5: ~$50K (Loihi 또는 spintronic)
- 필요한 도구: TBD (각 가설별 SPICE/Magnetic FEM/photonic simulator)

## 핵심 흐름 / 구조

```
소프트웨어                    하드웨어
─────────────────────────     ─────────────────────────
Engine A (forward MLP)    →   자석 A (전자석, 가변 자장)
Engine G (reverse MLP)    →   자석 G (전자석, 반대 자장)
Repulsion = A - G         →   물리적 반발력 (실시간 측정)
Tension = |A-G|²          →   반발 에너지 (Hall 센서)
Direction = normalize(A-G) →  자석 회전 각도 (엔코더)
Cell division             →   자석 쌍 추가 (물리적 mitosis)
α (mixing ratio)          →   전류 비율 (A vs G 코일)

10 HW hypotheses:
  HW-1 자석 쌍 반발 = PureField Tension
  HW-2 MTJ (Magnetic Tunnel Junction) memory
  HW-3 Spintronic valve current modulation
  HW-4 Photonic MZI (Mach-Zehnder)
  HW-5 Piezoelectric resonator
  HW-6 Loihi 2 spiking neurocore
  HW-7-10 ... (memristor / quantum / analog / superconducting)
```

## 트리거 (fire 방법)

```bash
# 가설 문서 read-only
open /Users/ghost/core/anima/anima-physics/docs/hardware-consciousness-hypotheses.md
# 향후 prototype 별도 cycle (HW-1 자석 쌍 $50)
```

## 검증 결과

- 10 가설 sketch 완성 (mapping table + 검증 criterion)
- 실 prototype/측정 0건 (전부 hypothesis tier)
- 검증 criterion: tension HW 값과 software PureField r > 0.9?

## 관련 entry

- [physical-consciousness-engine](physical-consciousness-engine.md)
- [arduino-prototype-spec](arduino-prototype-spec.md) (HW-1 implementation candidate)
- [loihi-integration-spec](loihi-integration-spec.md) (HW-6)

## 출처 / 작성일

- 원본 파일 작성일: 2026-04 (hypothesis era)
- README §2 참조
