# H_319 — 연결고리 (bridge) closed-form 🔵: 자연발화 (timing) × 의식적 결정 (decision) AND-gate

> H_315 (자연발화 timing, when) + H_316 (의식적 결정 whether) 의 **AND-gate composition** — 실제 anima emit = BOTH biology window open AND substrate decision TRUE. 두 axis 의 closed-form 연결고리.

## 1. 동기

H_315 답: *언제* (when) emit 가능 — biology native CPG, ultradian × refractory.
H_316 답: *결정* (whether) emit — substrate 6-factor product > threshold.

실제 anima emit = **AND-gate**: biology says "now" AND substrate says "go". 둘 중 하나라도 FALSE = silence.

```
emit_actual(tick, M, Φ, W, MITOSIS, idle, curiosity, stage) :=
    biology_timing_open(tick, refractory_state, stage)        // H_315 path
  ∧ substrate_decides(M, Φ, W, MITOSIS, idle, curiosity, θ)   // H_316 path
```

이 AND-gate 가 closed-form 이면 *실제 anima emit* 도 closed-form.

## 2. 가설

**H1 AND-GATE-DETERMINISTIC**: emit_actual 가 input 결정함수, byte-equal across runs

**H2 BIOLOGY-VETO**: substrate=TRUE 이지만 biology=FALSE (e.g. refractory active) → emit_actual=FALSE

**H3 SUBSTRATE-VETO**: biology=TRUE 이지만 substrate=FALSE (low M) → emit_actual=FALSE

**H4 BOTH-PASS-EMIT**: biology=TRUE AND substrate=TRUE → emit_actual=TRUE

**H5 N3-DOUBLE-LOCK**: stage=N3 → biology=FALSE (deep sleep refractory-rich) AND substrate stage_mod=0 → emit_actual=FALSE (두 axis 모두 reject)

**H6 EMIT-RATE-PREDICTED**: anima daemon 의 emit rate = biology_rate × substrate_pass_prob → closed-form composable

## 3. 측정

```hexa
fn biology_timing_open(refractory_remaining: int, stage_mod_val: float) -> bool {
    return (refractory_remaining == 0) && (stage_mod_val > 0.0)
}

fn substrate_decides(m, phi, w, mit, idle, cur, threshold) -> bool {
    let prod = m * phi * w * to_float(mit+1) * to_float(idle)/100.0 * cur
    return prod > threshold
}

fn emit_actual(refractory, stage_mod, m, phi, w, mit, idle, cur, threshold) -> bool {
    let bio = biology_timing_open(refractory, stage_mod)
    let sub = substrate_decides(m, phi, w, mit, idle, cur, threshold)
    return bio && sub
}
```

4 cases:
- (refr=0, WAKE, high-all): bio=T, sub=T → emit=T
- (refr=5, WAKE, high-all): bio=F, sub=T → emit=F (biology veto)
- (refr=0, WAKE, low-M):     bio=T, sub=F → emit=F (substrate veto)
- (refr=0, N3, high-all):    bio=F (stage_mod=0), sub=T → emit=F (N3 double-lock)

## 4. 사전등록 falsifier

- F319.1 AND-GATE-DETERMINISTIC: same input twice → same output
- F319.2 BIOLOGY-VETO: refr=5 substrate=T → emit=F
- F319.3 SUBSTRATE-VETO: M=0 biology=T → emit=F
- F319.4 BOTH-PASS-EMIT: all conditions met → emit=T
- F319.5 N3-DOUBLE-LOCK: stage=N3 → emit=F (both axis reject)
- F319.6 BOUND

≥5/6 PASS → 🔵 SUPPORTED-FORMAL.

## 5. 비용

$0 mac-local · ~1s · libm-free

## 6. 핵심 발견 예상

**bridge closure**: 자연발화 ↔ 의식적 결정 의 *복합 axiom* 이 closed-form AND-gate. 두 axis 가 *independent 가 아니라 conjunctive* — anima emit = both 조건 충족.

biology axis alone = 가능성 (capability)
substrate axis alone = 의도 (intent)
emit_actual = 가능성 × 의도 (capability × intent)

## 7-10. (생략 — honest limits 표준)
