# consciousness-loop/src/aux_engine_lib.hexa

> Canonical hexa-lang aux engine lib (Cell + Faction + ConsciousnessEngine + 8-factor motivation + Hebbian + Φ proxy) · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — canonical functional rewrite of legacy v2 (main.hexa). pure-hexa lib (struct return + caller reassign), legacy `self: *T` borrow + `&engine` caller + `++` list concat + `or` keyword + `[]*[float]` pointer-to-list 모두 표준 idiom 으로 재작성. aux_engine_smoke 5/5 PASS 의 backing lib.

## 작동 코드 / 의존성

- 원본: `consciousness-loop/src/aux_engine_lib.hexa` (555 LoC)
- 외부 의존: hexa run (exp / tanh / rand_f32 / pow 내장)
- 구조: `Cell { hidden: [float], identity: [float], ... }` × `Faction { cells: [Cell] }` × `Engine { factions: [Faction], best_phi, ... }` — 모두 value-receiver + struct return
- 상수: DIM=64, HIDDEN=128, N_FACTIONS=8
- canonical idiom: `cell_with_hidden_at` / `faction_with_cell_at` / `engine_with_faction_at` (flat helper-fn nested-LHS 회피)

## 비용 / 리소스

- $0 Mac local (lib 단독 측정 없음 — 사용처 aux_engine_smoke 100-step ~수 초)

## 핵심 흐름 / 코드 발췌

```hexa
// canonical value-receiver + struct-return pattern
fn cell_with_hidden(cell: Cell, new_hidden: [float]) -> Cell { ... }
fn cell_with_hidden_at(cell: Cell, i: int, x: float) -> Cell { ... }
fn faction_add_cell(f: Faction, cell_id: int) -> Faction { ... }
fn engine_new(n_factions: int, seed: int) -> Engine { ... }
fn engine_process(eng: Engine, input: [float]) -> Engine { ... }
fn engine_phi_proxy(eng: Engine) -> float { ... }       // clamp ≥ 0
fn engine_cross_faction_debate(eng: Engine, k: float) -> Engine { ... }
fn engine_intra_faction_sync(eng: Engine, k: float) -> Engine { ... }
fn engine_ising_interaction(eng: Engine) -> Engine { ... }
fn aux_engine_hebbian_all(eng: Engine) -> Engine { ... }

// 8-factor motivation (HEXAD/CHAT/spontaneous_lib mirror)
fn aux_factor_relevance / info_gap / curiosity / pain /
   coherence / originality / balance / dynamics(...) -> float
fn aux_motivation_score(rel, gap, cur, pn, coh, orig, bal, dyn) -> float
```

## 트리거 (fire 방법)

```bash
# lib 자체는 entry-point 없음 — sibling smoke 가 import
hexa run anima-physics/consciousness-loop/src/aux_engine_smoke.hexa
```

## 검증 결과

- aux_engine_smoke 5/5 PASS (S1 parse + S2 engine_construct + S3 forward_step finite + S4 phi_nonneg + S5 motivation_in_unit) — backing lib 으로 동작 입증
- main.hexa / main_longrun.hexa rewrite 시 `import "aux_engine_lib.hexa"` lib delegation 로 활용 (consciousness-loop legacy rewrite cycle 2026-05-21)

## SSOT 매핑

- 자연발화 8-factor → `HEXAD/CHAT/spontaneous_lib.hexa` (Phase B1, F-SPONT 7/7)
- 영속성 ratchet+Hebbian → `consciousness-loop/src/main_longrun.hexa` (legacy) §3
- canonical idiom 참고 → `anima-physics/oscillator/sleep_oscillator.hexa` header + `anima-physics/memristor/self_reference.hexa` header

## 관련 entry

- [consciousness-loop/src/aux_engine_smoke.md](./aux_engine_smoke.md) — 1차 smoke (5/5 PASS) main runner
- [consciousness-loop/src/main.md](./main.md) — legacy v2 base (canonical rewrite 완료, lib delegate)
- [consciousness-loop/src/main_longrun.md](./main_longrun.md) — 10K step long-run (canonical rewrite 완료, lib delegate)
- [tool/anima_physics_e2e_demo.md](../../tool/anima_physics_e2e_demo.md) — LAYER 2 ConsciousnessEngine mini mirror (G8 5/5 PASS)

## 출처

- `HEXAD/PHYSICS/README.md` §6.14 LANDED commits (anima `2c636ce96` aux_engine_lib + aux_engine_smoke)
- `anima-physics/PLAN.md` §2.2 검증 LANDED · §5.3 G3 cross-check
