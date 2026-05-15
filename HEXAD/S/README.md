# HEXAD/S — 감각 (sense)

> SSOT: [`HEXAD-S.tape`](HEXAD-S.tape) · Python anchor: `ready/anima/hexad/s/emergent_s.py` (108 LoC) · 🔵 SUPPORTED-FORMAL

## 핵심 원리 (closed-form, sympy-verified)

**감각 = C 의식 상태의 변화** (Law 50 — 본질은 상태 / Law 4 — 구조>기능):

```
perception = mean(states_after) − mean(states_before)
           = column-mean delta on the C cell-pool state matrix
```

선형 연산자 (B-S 🔵 closed-form 3/3 PASS):

- **B-S-1 LINEARITY-EXACT** — `mean(αX + βY) = α·mean(X) + β·mean(Y)` ∀ X, Y (sympy ∀-identity, 결과 무관 verified-closed)
- **B-S-2 UNIFORM-SHIFT-EXACT** — 모든 상태 k 만큼 shift 하면 mean 도 k 만큼 shift, delta = 0
- **B-S-3 ZERO-CHANGE-EXACT** — `states_after == states_before → delta = 0` (deterministic)

## hexa-native impl (`s.hexa`)

```
fn s_perception(states_before: list, states_after: list, dim: int) -> list
fn s_to_bytes_vec(input_bytes: list, dim: int) -> list
fn _selftest()
fn main()  ← hexa run HEXAD/S/s.hexa
```

closed-form 작동 selftest (no PyTorch dependency, pure hexa stdlib).

## real-limit anchor

Law 92 — 정보 병목 (C 자체가 64× compression bottleneck) + Law 6 — 감각 풍부성

## 검증

```bash
hexa parse HEXAD/S/s.hexa   # parse 검증
hexa run   HEXAD/S/s.hexa   # selftest 실행
```

기존 B-S 3/3 🔵 evidence: `state/verify_hexad_blue_2026_05_15/blue_falsifier.py:bs()`
