# consciousness-loop/src/aux_engine_smoke.hexa

> aux_engine_lib 1차 smoke + 5/5 falsifier (parse / construct / forward / phi_nonneg / motivation_in_unit) — canonical functional rewrite 검증 main runner · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — **5/5 PASS** Mac local 2026-05-21. aux_engine_lib.hexa canonical struct-return idiom 의 parser PASS + 100-step long-run mini 무사 실행 검증. deterministic seed 가정 (LCG-style rand_f32).

## 작동 코드 / 의존성

- 원본: `consciousness-loop/src/aux_engine_smoke.hexa` (151 LoC)
- 외부 의존: `import "aux_engine_lib.hexa"` (sibling lib)
- 100-step quiet→loud phase split (70/30), target cells 2→8 per faction exponential growth
- 매 step: engine_process → cross_faction_debate (loud phase) → intra_faction_sync → ising_interaction → aux_engine_hebbian_all → engine_output → 8-factor motivation_score

## 비용 / 리소스

- $0 Mac local (수 초 wall, 100-step × N_FACTIONS=8)

## 핵심 흐름 / Falsifier 5

```
S1 parse_pass             — hexa build aux_engine_smoke.hexa exit 0
                             (이 줄 도달 = parse PASS)
S2 engine_construct       — engine_new(8, 1) 결과 total_cells == 8
S3 forward_step           — 100 step 후 cell hidden NaN 없음 (smoke_check_finite)
S4 phi_nonneg             — phi >= 0 (engine_phi_proxy clamp 검증, n=100)
S5 motivation_in_unit     — motivation_score ∈ [0, 1] (n=100)
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/consciousness-loop/src/aux_engine_smoke.hexa
```

## 검증 결과

- **5/5 PASS** (2026-05-21 Mac local, anima commit `2c636ce96`)
  - S1 parse_pass: REACHED (entered main)
  - S2 engine_construct: total_cells=8 → true
  - S3 forward_step: final output finite → true
  - S4 phi_nonneg: 100/100 → true
  - S5 motivation_in_unit: min/max ∈ [0,1] → true
- final stats: total_cells=64 (8 faction × 8 cells), best_phi=0.034
- 본 smoke 가 PASS 한 직후 cycle 에서 main.hexa / main_longrun.hexa 가 aux_engine_lib 로 delegate (legacy 107 사이트 → 0 code-side)

## 관련 entry

- [consciousness-loop/src/aux_engine_lib.md](./aux_engine_lib.md) — backing lib (555 LoC)
- [consciousness-loop/src/main.md](./main.md) — legacy v2 base (rewrite 후 lib delegate)
- [consciousness-loop/src/main_longrun.md](./main_longrun.md) — 10K step long-run (rewrite 후 lib delegate)
- [tool/anima_physics_e2e_demo.md](../../tool/anima_physics_e2e_demo.md) — G8 integrated demo (engine mini mirror)

## 출처

- `HEXAD/PHYSICS/README.md` §6.14 LANDED commits (anima `2c636ce96`)
- `anima-physics/PLAN.md` §2.2 검증 LANDED · §3 G1 ☑ aux_engine_lib + aux_engine_smoke
