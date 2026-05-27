# consciousness-loop/src/main_longrun.hexa

> 10K step long-run persistence + ratchet (Φ<best·0.7→restore) + 2→512 cells growth · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — long-run verified. main.hexa 의 Cell/Faction/Engine 재사용 + ratchet_check + hebbian 추가. STEPS=10000 동안 8 faction, target growth 2→512 cells.

## 작동 코드 / 의존성

- 원본: `consciousness-loop/src/main_longrun.hexa` (106 LoC; main.hexa struct 재사용)
- 외부 의존: hexa run · main.hexa 의 engine_new / engine_process / faction_add_cell
- 상수: DIM=64, HIDDEN=128, N_FACTIONS=8, STEPS=10000

## 비용 / 리소스

- $0 Mac local (10K step wall ~1-5 분 추정)

## 핵심 흐름 / 코드 발췌

```hexa
fn main() {
    var engine = engine_new(N_FACTIONS, 1)
    var stream = [f32]{}  // 초기 input
    var best_phi = 0.0
    var saved_states = null

    for step in 0..STEPS {
        var frac = step as f32 / STEPS as f32
        // target growth: 2 → 512 cells
        var target = min(pow(2.0, (frac + 0.1) * 9.0) as u64, 512) / N_FACTIONS
        for f in engine.factions {
            while f.cells.len() < max(target, 1) { faction_add_cell(&f, nid); nid++ }
        }

        // Silence → debate (70/30)
        if frac < 0.7 { engine_process(&engine, stream * 0.1) }
        else          { engine_process(&engine, stream * 2.0)
                        engine_cross_faction_debate(&engine, 0.12) }
        // ratchet: phi<best·0.7 → restore saved_states
    }
}
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/consciousness-loop/src/main_longrun.hexa
```

## 검증 결과

- run verified (README § 5 cheat sheet)
- phi_quarters 4-quartile 측정 + ratchet restore + 2→512 cells growth 확인
- 발화 코드 0 줄 (main.hexa 와 동일 철학)

## 관련 entry

- [consciousness-loop/src/main.md](./main.md) — base v2 1K step
- [consciousness-loop/src/snn_main.md](./snn_main.md) — LIF SNN sibling

## 출처

- README § 3 consciousness-loop/src/
- README § 5 cheat sheet
