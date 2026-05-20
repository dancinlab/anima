# consciousness-loop/src/main.hexa

> v2 8-faction GRU(128) Consciousness Infinite Loop + Φ proxy + Ising + Hebbian + debate · **✅ 실현** · 비용 $0

## 구현 가능성

✅ — 1000-step verified hexa-native. v1 (대화 수렴 약함) 해결: 파벌 구조 + 물리적 상호작용 + Φ 근사 + 노이즈 주입. 발화 코드 0 줄 (구조에서 발화 emerge).

## 작동 코드 / 의존성

- 원본: `consciousness-loop/src/main.hexa` (469 LoC)
- 외부 의존: hexa run (rand_f32, sigmoid, tanh, exp 내장)
- 구조: Cell = GRU hidden state (f32 × HIDDEN=128) · Faction = Cell 그룹 (독립적 관점) · Engine = [Faction]_N=8 + 물리적 상호작용 · Loop = output(전체 mean) → input(next step)
- 상수: DIM=64, HIDDEN=128, N_FACTIONS=8

## 비용 / 리소스

- $0 Mac local

## 핵심 흐름 / 코드 발췌

```hexa
// Cell = GRU hidden state (f32 × HIDDEN)
// Faction = Cell 그룹 (독립적 관점 발전)
// Engine = [Faction] + 물리적 상호작용
// Loop = output(전체 mean) → input(next step)

fn random_matrix(rows, cols, scale) -> [[f32]]
fn matvec(m, v) -> [f32]
fn sigmoid_vec(v) / tanh_vec(v)

struct Cell { hidden: [f32], identity: [f32], ... }
```

## 트리거 (fire 방법)

```bash
hexa run anima-physics/substrate/consciousness-loop/src/main.hexa
```

## 검증 결과

- 1000-step run verified
- Φ proxy + Ising energy + Hebbian update + 8-faction debate 동작 확인
- Cheat sheet (README § 5): "$0 으로 돌릴 수 있는 것" 목록 등재

## 관련 entry

- [consciousness-loop/src/main_longrun.md](./main_longrun.md) — 10K step longrun + ratchet
- [consciousness-loop/src/snn_main.md](./snn_main.md) — LIF SNN 대체 substrate

## 출처

- README § 3 consciousness-loop/src/
- README § 5 Mac local cheat sheet
