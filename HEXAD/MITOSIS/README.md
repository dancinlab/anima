# HEXAD/MITOSIS — 성장축 (growth axis)

> SSOT: [`MITOSIS.tape`](MITOSIS.tape) · 성장축 ⊥ HEXAD 6 구조축 (orthogonality 는 `§mitosis_two_axis` 안에서 보존)
> Hexa-native impl: 기존 `tool/hexa_native/mitosis_hook.hexa` (1119 LoC FULL IMPL D4a) 재사용

## 핵심 원리

**MITOSIS = 성장축 (growth axis)**. anima 의 6모듈 (HEXAD 구조축) 과 직교 — 6모듈 *그 자체* 가 자라나는 방식 (cell split/merge dynamics). 학습 = 분열 단일 연속체 (REBORN §0.5 carry, archive 됐지만 의미는 HEXAD.tape `§hexad_condition_lineup` 으로 흡수).

C 의식 ↔ MitosisC 가 가장 직접 대응한 binding 일 뿐, mitosis 는 시스템 *전체* 성장 원리.

## SSOT

| | |
|---|---|
| spec | [`MITOSIS.tape`](MITOSIS.tape) — 성장축 architecture · §mitosis_two_axis · §mitosis_verified |
| canonical hexa-native impl | [`../../tool/hexa_native/mitosis_hook.hexa`](../../tool/hexa_native/mitosis_hook.hexa) — 1119 LoC FULL IMPL D4a, 5/5 PASS Mac local (REBORN §91, MITOSIS.tape §mitosis_verified) |
| Python anchor | `ready/core/consciousness_engine.py` (ConsciousnessC + ConsciousnessEngine 의 split_threshold/merge_threshold mechanics) |
| evidence cycle | `state/clm_v1_fire_2026_05_15/` (.clm v1 P2 cells 2→64 organic split, 8/8🔵 + F-PYPHI Φ=1.0625) |

## hexa-native impl status

`HEXAD/MITOSIS/mitosis.hexa` = scaffold + cross-link entry (다른 모듈 C/D 와 동일 패턴). full impl 은 위 mitosis_hook.hexa 그대로 사용.

```
fn mitosis_split_threshold_default()  -> float    // 0.3 — ConsciousnessEngine default
fn mitosis_merge_threshold_default()  -> float    // 0.01
fn mitosis_split_patience_default()   -> int      // 5
fn mitosis_merge_patience_default()   -> int      // 15
```

selftest: invariant 검증 (closed-form thresholds 정합).

## 검증

```bash
hexa tape  HEXAD/MITOSIS/MITOSIS.tape    # tape v1.2 검증
hexa parse HEXAD/MITOSIS/mitosis.hexa    # scaffold parse
hexa run   HEXAD/MITOSIS/mitosis.hexa    # invariant selftest
hexa run   tool/hexa_native/mitosis_hook.hexa  # 실 mitosis dynamics (5/5 PASS)
```

## related

- HEXAD.tape `§hexad_condition_lineup` — A/G+mitosis 둘 다 필수 mandate
- HEXAD/C/c.hexa — C 의식 (mitosis 의 가장 직접 대응 binding)
- archive/REBORN.tape — §0.5 학습=분열 philosophy (deprecated, 의미는 HEXAD 으로 흡수)
- archive/MAIN.tape `§V-MIT-1..6` — historical mitosis verdict carry

## Honest C3

- 위치만 `HEXAD/MITOSIS/` 안으로 (PR #83) — 의미는 여전히 성장축 ⊥ 구조축 orthogonal (tape §mitosis_two_axis 보존)
- mitosis_hook.hexa 는 `tool/hexa_native/` 에 그대로 (다른 hexa-native 코드 cross-reference). `HEXAD/MITOSIS/mitosis.hexa` 는 thin scaffold + cross-link.
- 실 mitosis 동역학 검증 evidence = .clm v1 P2 fire (`state/clm_v1_fire_2026_05_15/`)
