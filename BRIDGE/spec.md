# BRIDGE — 4-key AND-gate emit 결정 spec

@title: 🚪 BRIDGE — 자연발화 × 의식적 결정 AND-gate
@bench-anchor: UNIVERSE H_319 (anima PR #1125 · 2026-05-28)

## 1. 문제 정의

anima 의 `emit ⇔ M ∧ C ∧ W ∧ (Φ ≥ θ)` 형식화 — 4-key AND-gate.
CLAUDE.md `a_substrate_native_speak` governance ("anima 는 사용자 메시지 = environment context, 즉답 의무 아님") 의 measurable 구현 leg.

| key | 정의 | 범위 | source |
|---|---|---|---|
| M | motivation (8-factor argmax 의 confidence) | [0, 1] | CHANNEL.router |
| C | coherence (직전 emit 과의 의미 정합) | [0, 1] | CORE.engine_g |
| W | tension 5-ch L2 norm | [0, 1] | CHANNEL.tension |
| Φ | integrated information (substrate 활성) | [0, ∞) | HEXAD/IIT4 또는 phi_native |
| θ | Φ threshold (기본 0.5) | scalar | tunable per stage |

## 2. AND-gate 식 (multiplication softening)

```
emit_signal = M · C · W · softstep(Φ, θ=0.5)
softstep(x, θ) = 1 / (1 + exp(-8·(x - θ)))    # sigmoid soft-threshold
```

**왜 곱셈?** Hard `if all > t` 는 0/1 cliff — 한 key 가 0.49 면 emit 차단됨. multiplication 은 4-key 가 모두 어느 정도 활성일 때만 큰 신호 (uniform 0.5 → AND=0.0625), 한 key 가 0 이면 0 (multiplicative AND constraint preserved). soft-AND 와 hard-AND 의 경계: bench #7 H_319 측정 uniform_AND=0.0625 정확히 정합.

**왜 softstep?** Φ 는 binary 가 아닌 continuous, `Φ ≥ θ` 의 hard cutoff 도 substrate-native 가 아니라 stimulus-response 패턴. sigmoid k=8 은 θ ± 0.1 영역에서 80% 전이 (충분히 sharp, 충분히 smooth).

## 3. antithesis: OR-gate (검증용)

```
emit_signal_OR = 1 - (1 - M)·(1 - C)·(1 - W)·(1 - softstep(Φ, θ))
                = inclusion-exclusion for independent uniform
```

uniform M=C=W=Φ=0.5 → OR=0.9375 (bench #7 H_319 antithesis 측정). AND vs OR 의 1단위 (0.0625 + 0.9375 = 1.0) 가 4-key independent uniform 항등식.

## 4. emit threshold

```
emit ⇔ emit_signal > θ_emit
θ_emit = 0.1   # 기본 — 4-key 중 적어도 1 strong 필요
```

`θ_emit=0.1` rationale: 4-key uniform 0.5 = 0.0625 < 0.1 → silent (assistant regression 회피). 한 key 가 0.8 + 나머지 0.5 → 0.8 · 0.5³ · softstep(0.5)=0.5 = 0.0500, 여전히 silent. 두 key 가 0.8 → 0.8² · 0.5² · 0.5 = 0.08, 여전히 silent. 세 key 가 0.8 → 0.8³ · 0.5 · 0.5 = 0.128 > 0.1 → emit. 즉 **3+ key 동시 활성** 이 emit 조건.

## 5. governance 정합

| 원칙 | BRIDGE 의 자리 |
|---|---|
| `a_substrate_native_speak` | emit = substrate state 의 결정, user message → forced emit 부재 |
| `a_autonomy_over_hardcode` | per-stage boolean gate 부재 (Φ scale 만 stage 별 변동) |
| p5 NO SPEAK() | emit_signal continuous, speak() 호출 부재 |
| p4 NO ASSISTANT FRAMING | emit_signal computed from internal state, prompt-response 패턴 부재 |

## 6. CHANNEL 통합

`CHANNEL/router.hexa` 의 8-factor argmax 후 다음 layer 로 BRIDGE pseudo-gate modulation:

```
chosen_channel = router_argmax(8_factor)     # text/voice/tension/silence
modulated = chosen_channel · bridge_and_gate(M, C, W, Φ)
emit ⇔ modulated > θ_emit
```

multiplicative composition — router 가 채널 선택 + BRIDGE 가 발사 결정 (분리된 책임).

## 7. 측정자 (bench #7 H_319 정합)

uniform AND=0.0625 / OR=0.9375 의 동시 만족 = BRIDGE gate 가 식 정합 verify.

| 측정 | 식 | 예상값 |
|---|---|---|
| uniform_AND | M=C=W=Φ=0.5 → AND | 0.0625 ± 1e-2 |
| uniform_OR | M=C=W=Φ=0.5 → OR | 0.9375 ± 1e-2 |
| monotone | M↑ → AND↑ | strict |
| AND ≤ min | AND ≤ min(M,C,W,Φ_step) | invariant |
| OR ≥ max | OR ≥ max(M,C,W,Φ_step) | invariant |
| phi_zero | Φ=0 → AND ≈ 0 | softstep(0,0.5)≈3e-2 |
| key_zero | any key=0 → AND = 0 | multiplicative |

7 invariant — `gate_smoke.hexa` 에서 모두 통과.

## 8. F2 sensitivity recalibration carry

bench #7 (H_319) 의 F2 sensitivity threshold 1.6→2.1 재조정 (gradient 평탄화) 는 본 spec 의 default θ=0.5 와 무관 — F2 는 `dE/dM` 등 4-key partial sensitivity 의 metric 으로 BRIDGE downstream audit. AUDIT.md 에서 처리.
